"""Real ledger, filesystem, CLI restart, and multiprocess lease behavior tests."""
import copy
import json
import multiprocessing
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from controller import Controller, STAGES


def example():
    return {'version': 2, 'feature': 'synthetic', 'spec': 'SPEC.md', 'shared_contracts': ['contract.md'], 'criteria': [{'id': 'C1', 'ticket': 'T1', 'gate': 'integration'}], 'capacity': {'implementation': 1, 'validation': 1}, 'tickets': [{'id': 'T1', 'ticket': 'tickets/T1.md', 'author': 'implementer', 'scope': ['code.py', 'other.py'], 'integration_owner': 'integrator', 'maturity': {'functional_review': True, 'expected': 'complete local increment', 'incomplete': [], 'final_qa': True}, 'dependencies': [], 'resources': ['browser'], 'estimate_minutes': 10, 'gates': [
        {'id': 'local', 'stage': 'CODE_READY', 'kind': 'test', 'required': True, 'scope': ['code.py'], 'artifacts': ['local-proof'], 'criteria': []},
        {'id': 'unaffected', 'stage': 'CODE_READY', 'kind': 'test', 'required': True, 'scope': ['other.py'], 'artifacts': ['other-proof'], 'criteria': []},
        {'id': 'standards', 'stage': 'REVIEWED', 'kind': 'review', 'required': True, 'independent': True, 'scope': ['code.py'], 'artifacts': ['standards-proof'], 'criteria': []},
        {'id': 'spec', 'stage': 'REVIEWED', 'kind': 'review', 'required': True, 'independent': True, 'scope': ['code.py'], 'artifacts': ['spec-proof'], 'criteria': []},
        {'id': 'security', 'stage': 'REVIEWED', 'kind': 'security', 'required': True, 'independent': True, 'scope': ['code.py'], 'artifacts': ['security-proof'], 'criteria': []},
        {'id': 'integration', 'stage': 'ACCEPTED', 'kind': 'integration', 'required': True, 'scope': ['code.py'], 'artifacts': ['integration-proof'], 'criteria': ['C1']}
    ]}]}


def contender(plan, root, resources, barrier, queue):
    c = Controller(plan, root, resources_root=resources)
    c.execute('init')
    barrier.wait()
    try:
        c.execute('reserve', ticket='T1', resource='browser')
        queue.put('reserved')
    except ValueError:
        queue.put('blocked')


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.plan = example()
        self.path = self.root / 'plan.json'
        for name in ('code.py', 'other.py', 'config.json', 'env.json', 'artifact.txt', 'finding.txt'):
            (self.root / name).write_text('synthetic ' + name, encoding='utf-8')
        self.write_plan()
        self.c = Controller(self.path, self.root, resources_root=self.root / 'leases')
        self.c.execute('init')

    def tearDown(self):
        self.temp.cleanup()

    def write_plan(self):
        self.path.write_text(json.dumps(self.plan), encoding='utf-8')

    def proof(self, gate, actor='reviewer'):
        g = next(g for g in self.plan['tickets'][0]['gates'] if g['id'] == gate)
        if g.get('kind') == 'integration' and actor == 'reviewer':
            actor = 'integrator'
        return self.c.execute('evidence', ticket='T1', gate=gate, proof=g['artifacts'][0], artifact='artifact.txt', actor=actor, code=g['scope'], config=['config.json'], env=['env.json'], result='PASS')

    def local(self):
        self.c.execute('transition', ticket='T1', to='IN_PROGRESS')
        self.proof('local')
        self.proof('unaffected')
        self.c.execute('transition', ticket='T1', to='CODE_READY')

    def review(self):
        self.local()
        self.c.execute('transition', ticket='T1', to='REVIEW_READY')
        for g in ('standards', 'spec', 'security'):
            self.proof(g)
        self.c.execute('transition', ticket='T1', to='REVIEWED')

    def accepted(self):
        self.review()
        self.c.execute('transition', ticket='T1', to='INTEGRATION_READY')
        self.proof('integration')
        self.c.execute('transition', ticket='T1', to='ACCEPTED')

    def test_01_incomplete_no_final_qa(self):
        with self.assertRaisesRegex(ValueError, 'requires mature'):
            self.proof('spec')
        with self.assertRaisesRegex(ValueError, 'invalid transition'):
            self.c.execute('transition', ticket='T1', to='REVIEW_READY')
        with self.assertRaisesRegex(ValueError, 'integration readiness'):
            self.proof('integration')

    def test_02_mature_contextual_review(self):
        self.local()
        self.c.execute('transition', ticket='T1', to='REVIEW_READY')
        with self.assertRaisesRegex(ValueError, 'differ'):
            self.proof('spec', 'implementer')
        self.proof('spec')

    def test_03_focused_correction_delta(self):
        self.review()
        state = self.c.execute('change', ticket='T1', kind='focused', paths=['code.py'])
        self.assertEqual(state['tickets']['T1']['stage'], 'IN_PROGRESS')
        self.assertTrue(self.c.gate_pass(state, 'T1', self.plan['tickets'][0]['gates'][1]))
        self.assertFalse(self.c.gate_pass(state, 'T1', self.plan['tickets'][0]['gates'][0]))

    def test_04_structural_requires_broad_validation(self):
        self.review()
        state = self.c.execute('change', ticket='T1', kind='structural', paths=['code.py'])
        self.assertFalse(self.c.gate_pass(state, 'T1', self.plan['tickets'][0]['gates'][1]))

    def test_05_security_preserves_required_gate(self):
        self.review()
        state = self.c.execute('change', ticket='T1', kind='security', paths=['config.json'])
        gate = next(g for g in self.plan['tickets'][0]['gates'] if g['id'] == 'security')
        self.assertFalse(self.c.gate_pass(state, 'T1', gate))
        with self.assertRaises(ValueError):
            self.c.execute('transition', ticket='T1', to='REVIEWED')

    def test_06_future_dependency_blocks_relevant_gate_only(self):
        t2 = copy.deepcopy(self.plan['tickets'][0])
        t2.update(id='T2', ticket='tickets/T2.md')
        self.plan['tickets'].append(t2)
        self.plan['tickets'][0]['dependencies'] = [{'ticket': 'T2', 'type': 'integration', 'source_stage': 'REVIEWED', 'target_stage': 'INTEGRATION_READY', 'condition': 'stage_reached'}]
        self.write_plan()
        self.c = Controller(self.path, self.root, state_root=self.root / 'dep-state', resources_root=self.root / 'leases')
        self.c.execute('init')
        self.review()
        with self.assertRaisesRegex(ValueError, 'dependency pending'):
            self.c.execute('transition', ticket='T1', to='INTEGRATION_READY')

    def test_07_runner_block_resume_no_false_acceptance(self):
        self.c.execute('block', ticket='T1', reason='runner unavailable')
        with self.assertRaises(ValueError):
            self.c.execute('transition', ticket='T1', to='ACCEPTED')
        state = self.c.execute('resume', ticket='T1')
        self.assertEqual(state['tickets']['T1']['stage'], 'PLANNED')

    def test_08_real_cross_worktree_browser_race(self):
        root2 = self.root / 'worktree2'
        root2.mkdir()
        barrier = multiprocessing.Barrier(2)
        queue = multiprocessing.Queue()
        processes = [multiprocessing.Process(target=contender, args=(str(self.path), str(root), str(self.root / 'leases'), barrier, queue)) for root in (self.root, root2)]
        for p in processes:
            p.start()
        results = [queue.get(timeout=20) for _ in processes]
        for p in processes:
            p.join(20)
            self.assertEqual(p.exitcode, 0)
        self.assertEqual(sorted(results), ['blocked', 'reserved'])
        ledger = self.c.resource_ledger()
        self.assertEqual(len(ledger['leases']), 1)

    def test_09_resolved_finding_needs_new_evidence(self):
        self.c.execute('finding', ticket='T1', id='F1', evidence='finding.txt', status='open')
        self.c.execute('finding', ticket='T1', id='F1', evidence='finding.txt', status='resolved')
        with self.assertRaisesRegex(ValueError, 'new evidence'):
            self.c.execute('finding', ticket='T1', id='F1', evidence='finding.txt', status='open')
        (self.root / 'finding.txt').write_text('new observed failure')
        self.c.execute('finding', ticket='T1', id='F1', evidence='finding.txt', status='open')

    def test_10_all_gates_close(self):
        with self.assertRaises(ValueError):
            self.c.execute('close')
        self.accepted()
        state = self.c.execute('close')
        self.assertTrue(state['closed'])
        with self.assertRaisesRegex(ValueError, 'closed'):
            self.c.execute('attempt', ticket='T1', failure='optional audit')

    def test_13_subprocess_restart_preserves_state(self):
        self.review()
        command = [sys.executable, str(Path(__file__).with_name('controller.py')), '--plan', str(self.path), '--root', str(self.root), '--resources-root', str(self.root / 'leases'), 'status']
        output = subprocess.check_output(command, text=True, encoding='utf-8')
        state = json.loads(output)
        self.assertEqual(state['tickets']['T1']['stage'], 'REVIEWED')
        self.assertEqual(state, self.c.execute('status'))

    def test_14_changed_evidence_requires_refresh(self):
        self.accepted()
        (self.root / 'code.py').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.c.execute('close')

    def test_15_unaffected_proof_reusable(self):
        self.review()
        (self.root / 'code.py').write_text('changed')
        state = self.c.execute('status')
        self.assertTrue(self.c.gate_pass(state, 'T1', self.plan['tickets'][0]['gates'][1]))

    def test_missing_artifact_is_never_pass(self):
        (self.root / 'artifact.txt').unlink()
        with self.assertRaisesRegex(ValueError, 'missing'):
            self.proof('local')

    def test_plan_mutation_and_cycles_rejected(self):
        self.plan['tickets'][0]['estimate_minutes'] = 20
        self.write_plan()
        c = Controller(self.path, self.root)
        with self.assertRaisesRegex(ValueError, 'plan changed'):
            c.execute('status')
        self.plan['tickets'][0]['dependencies'] = [{'ticket': 'absent', 'type': 'contract'}]
        self.write_plan()
        with self.assertRaisesRegex(ValueError, 'unknown'):
            Controller(self.path, self.root)

    def test_stagnation_requires_new_discrimination(self):
        self.c.execute('attempt', ticket='T1', failure='test-X', hypothesis='bad input')
        with self.assertRaisesRegex(ValueError, 'stagnation'):
            self.c.execute('attempt', ticket='T1', failure='test-X', hypothesis='bad input')
        self.c.execute('attempt', ticket='T1', failure='test-X', hypothesis='environment differs')

    def test_leases_owner_required_no_ttl_reclaim(self):
        self.c.execute('reserve', ticket='T1', resource='browser')
        with self.assertRaises(ValueError):
            self.c.execute('close')
        other = self.root / 'other-root'
        other.mkdir()
        c = Controller(self.path, other, resources_root=self.root / 'leases')
        c.execute('init')
        with self.assertRaisesRegex(ValueError, 'owner mismatch'):
            c.execute('release', ticket='T1', resource='browser')
        owner = self.c.execute('status')['owner']
        c.execute('release', ticket='T1', resource='browser', confirm_owner=owner)

    def test_unknown_gate_unmapped_criterion_and_invalid_fingerprint(self):
        with self.assertRaises(ValueError):
            self.c.execute('evidence', ticket='T1', gate='unknown')
        self.plan['tickets'][0]['gates'][-1]['required'] = False
        self.write_plan()
        with self.assertRaisesRegex(ValueError, 'mandatory criterion'):
            Controller(self.path, self.root)

    def test_unknown_estimates_and_capacity_are_advisory(self):
        schedule = self.c.execute('schedule')
        self.assertEqual(schedule['queue'][0]['critical_path_estimate_minutes'], 10)
        self.assertEqual(schedule['capacity_advisory']['implementation'], 1)

    def test_contract_frozen_gate_releases_early_coding(self):
        t2 = copy.deepcopy(self.plan['tickets'][0])
        t2.update(id='T2', ticket='tickets/T2.md')
        t2['gates'][0]['kind'] = 'contract'
        self.plan['tickets'].append(t2)
        self.plan['tickets'][0]['dependencies'] = [{'ticket': 'T2', 'type': 'contract', 'source_stage': 'PLANNED', 'target_stage': 'IN_PROGRESS', 'condition': 'stage_reached', 'gate': 'local'}]
        self.write_plan()
        self.c = Controller(self.path, self.root, state_root=self.root / 'contract-state', resources_root=self.root / 'leases')
        self.c.execute('init')
        with self.assertRaisesRegex(ValueError, 'dependency proof'):
            self.c.execute('transition', ticket='T1', to='IN_PROGRESS')
        self.c.execute('evidence', ticket='T2', gate='local', proof='local-proof', artifact='artifact.txt', actor='contract-reviewer', code=['code.py'], config=['config.json'], env=['env.json'], result='PASS')
        self.c.execute('transition', ticket='T1', to='IN_PROGRESS')

    def test_maturity_declarations_are_enforced(self):
        self.plan['tickets'][0]['maturity']['functional_review'] = False
        self.write_plan()
        self.c = Controller(self.path, self.root, state_root=self.root / 'immature')
        self.c.execute('init')
        self.local()
        with self.assertRaisesRegex(ValueError, 'not declared mature'):
            self.c.execute('transition', ticket='T1', to='REVIEW_READY')

    def test_same_owner_other_ticket_resource_cannot_overlap(self):
        t2 = copy.deepcopy(self.plan['tickets'][0])
        t2.update(id='T2', ticket='tickets/T2.md')
        self.plan['tickets'].append(t2)
        self.write_plan()
        self.c = Controller(self.path, self.root, state_root=self.root / 'two-tickets', resources_root=self.root / 'leases')
        self.c.execute('init')
        self.c.execute('reserve', ticket='T1', resource='browser')
        with self.assertRaisesRegex(ValueError, 'BLOCKED'):
            self.c.execute('reserve', ticket='T2', resource='browser')
        state = self.c.execute('status')
        self.assertEqual(state['tickets']['T2']['previous_stage'], 'PLANNED')
        self.assertEqual(state['tickets']['T2']['stage'], 'BLOCKED')
        self.c.execute('release', ticket='T1', resource='browser')
        self.c.execute('resume', ticket='T2')
        self.c.execute('reserve', ticket='T2', resource='browser')

    def test_stagnation_progress_requires_changed_real_artifact(self):
        self.c.execute('attempt', ticket='T1', failure='X', progress='artifact.txt')
        with self.assertRaisesRegex(ValueError, 'stagnation'):
            self.c.execute('attempt', ticket='T1', failure='X', progress='artifact.txt')
        (self.root / 'artifact.txt').write_text('observed changed behavior')
        self.c.execute('attempt', ticket='T1', failure='X', progress='artifact.txt')

    def test_real_dependency_cycle_rejected(self):
        t2 = copy.deepcopy(self.plan['tickets'][0])
        t2.update(id='T2', ticket='tickets/T2.md', dependencies=[{'ticket': 'T1', 'type': 'implementation'}])
        self.plan['tickets'].append(t2)
        self.plan['tickets'][0]['dependencies'] = [{'ticket': 'T2', 'type': 'implementation'}]
        self.write_plan()
        with self.assertRaisesRegex(ValueError, 'cycle'):
            Controller(self.path, self.root)

    def test_same_worktree_concurrent_events_not_lost(self):
        command = [sys.executable, str(Path(__file__).with_name('controller.py')), '--plan', str(self.path), '--root', str(self.root), '--resources-root', str(self.root / 'leases'), 'attempt', '--ticket', 'T1', '--failure']
        processes = [subprocess.Popen(command + ['distinct-' + str(i)], stdout=subprocess.PIPE, stderr=subprocess.PIPE) for i in range(5)]
        for p in processes:
            _, errors = p.communicate(timeout=20)
            self.assertEqual(p.returncode, 0, errors)
        state = self.c.execute('status')
        self.assertEqual(len(state['tickets']['T1']['attempts']), 5)
        self.assertEqual(len(state['history']), 6)
        self.assertEqual([e['sequence'] for e in state['history']], list(range(1, 7)))

    def test_stale_predecessor_cannot_release_successor(self):
        t2 = copy.deepcopy(self.plan['tickets'][0])
        t2.update(id='T2', ticket='tickets/T2.md', dependencies=[{'ticket': 'T1', 'type': 'implementation', 'source_stage': 'CODE_READY', 'target_stage': 'CODE_READY'}])
        self.plan['tickets'].append(t2)
        self.write_plan()
        self.c = Controller(self.path, self.root, state_root=self.root / 'stale-dep')
        self.c.execute('init')
        self.local()
        self.c.execute('transition', ticket='T2', to='IN_PROGRESS')
        (self.root / 'code.py').write_text('externally changed')
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.c.execute('transition', ticket='T2', to='CODE_READY')

    def test_status_exposes_accepted_but_stale_and_remaining_unknown(self):
        self.accepted()
        self.assertTrue(self.c.execute('status')['tickets']['T1']['acceptance_current'])
        (self.root / 'env.json').write_text('new environment')
        state = self.c.execute('status')
        self.assertFalse(state['tickets']['T1']['acceptance_current'])
        self.assertIn('stale', state['tickets']['T1']['acceptance_invalid_reason'])

    def test_active_remaining_estimate_is_unknown(self):
        self.c.execute('transition', ticket='T1', to='IN_PROGRESS')
        self.assertIsNone(self.c.execute('schedule')['queue'][0]['critical_path_estimate_minutes'])

    def test_security_change_without_gate_rejected(self):
        self.plan['tickets'][0]['gates'] = [g for g in self.plan['tickets'][0]['gates'] if g['kind'] != 'security']
        self.write_plan()
        self.c = Controller(self.path, self.root, state_root=self.root / 'no-security')
        self.c.execute('init')
        with self.assertRaisesRegex(ValueError, 'mandatory security gate'):
            self.c.execute('change', ticket='T1', kind='security', paths=['code.py'])

    def test_local_acceptance_without_full_qa_feature_still_pending(self):
        t2 = copy.deepcopy(self.plan['tickets'][0])
        t2.update(id='T2', ticket='tickets/T2-final.md', dependencies=[{'ticket': 'T1', 'type': 'integration'}])
        self.plan['tickets'].append(t2)
        self.plan['criteria'].append({'id': 'C2', 'ticket': 'T2', 'gate': 'integration'})
        t2['gates'][-1]['criteria'] = ['C2']
        self.plan['tickets'][0]['maturity']['final_qa'] = False
        self.plan['tickets'][0]['gates'][-1]['final_qa'] = False
        self.write_plan()
        self.c = Controller(self.path, self.root, state_root=self.root / 'local-acceptance')
        self.c.execute('init')
        self.accepted()
        with self.assertRaisesRegex(ValueError, 'not accepted: T2'):
            self.c.execute('close')

    def test_no_final_feature_gate_rejected(self):
        self.plan['tickets'][0]['gates'][-1]['final_qa'] = False
        self.write_plan()
        with self.assertRaisesRegex(ValueError, 'final integrated acceptance'):
            Controller(self.path, self.root)

    def test_local_integration_gate_can_be_satisfied_before_transition(self):
        self.plan['tickets'][0]['gates'].append({'id': 'local-integration', 'stage': 'INTEGRATION_READY', 'kind': 'integration', 'required': True, 'scope': ['code.py'], 'artifacts': ['local-integration-proof'], 'criteria': [], 'final_qa': False})
        self.write_plan()
        self.c = Controller(self.path, self.root, state_root=self.root / 'local-integration')
        self.c.execute('init')
        self.review()
        with self.assertRaisesRegex(ValueError, 'local-integration'):
            self.c.execute('transition', ticket='T1', to='INTEGRATION_READY')
        self.proof('local-integration')
        self.c.execute('transition', ticket='T1', to='INTEGRATION_READY')

    def test_same_state_multiprocess_reservation_is_not_idempotent(self):
        command = [sys.executable, str(Path(__file__).with_name('controller.py')), '--plan', str(self.path), '--root', str(self.root), '--resources-root', str(self.root / 'leases'), 'reserve', '--ticket', 'T1', '--resource', 'browser']
        processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        results = [p.communicate(timeout=20) for p in processes]
        self.assertEqual(sorted(p.returncode for p in processes), [0, 2])
        self.assertTrue(any(b'duplicate reservation' in error for _, error in results))
        state = self.c.execute('status')
        self.assertEqual(state['tickets']['T1']['stage'], 'PLANNED')
        self.assertEqual([e['action'] for e in state['history']], ['init', 'reserve'])
        self.assertEqual(len(self.c.resource_ledger()['history']), 1)

    def test_integration_actor_must_be_declared_owner(self):
        self.review()
        with self.assertRaisesRegex(ValueError, 'integration_owner'):
            self.proof('integration', actor='another-integrator')
        self.proof('integration', actor='integrator')

    def test_integration_gate_requires_owner(self):
        self.plan['tickets'][0].pop('integration_owner')
        self.write_plan()
        with self.assertRaisesRegex(ValueError, 'integration_owner'):
            Controller(self.path, self.root)

    def test_missing_verdict_never_becomes_pass(self):
        args = dict(ticket='T1', gate='local', proof='local-proof', artifact='artifact.txt', actor='author', code=['code.py'], config=['config.json'], env=['env.json'])
        with self.assertRaisesRegex(ValueError, 'explicit evidence result'):
            self.c.execute('evidence', **args)
        self.assertEqual(self.c.execute('status')['tickets']['T1']['evidence'], {})
        command = [sys.executable, str(Path(__file__).with_name('controller.py')), '--plan', str(self.path), '--root', str(self.root), 'evidence', '--ticket', 'T1', '--gate', 'local', '--proof', 'local-proof', '--artifact', 'artifact.txt', '--actor', 'author', '--code', 'code.py', '--config', 'config.json', '--env', 'env.json']
        result = subprocess.run(command, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'--result', result.stderr)

    def test_future_obligation_unknown_criterion_rejected(self):
        self.plan['tickets'][0]['maturity']['incomplete'] = [{'criterion': 'MISSING', 'ticket': 'T999', 'gate': 'MISSING'}]
        self.write_plan()
        with self.assertRaisesRegex(ValueError, 'future obligation'):
            Controller(self.path, self.root)

    def test_future_obligation_wrong_ticket_or_gate_rejected(self):
        for future in ({'criterion': 'C1', 'ticket': 'T999', 'gate': 'integration'}, {'criterion': 'C1', 'ticket': 'T1', 'gate': 'local'}):
            with self.subTest(future=future):
                self.plan['tickets'][0]['maturity']['incomplete'] = [future]
                self.write_plan()
                with self.assertRaisesRegex(ValueError, 'future obligation'):
                    Controller(self.path, self.root)

    def test_future_obligation_valid_mandatory_pointer(self):
        self.plan['tickets'][0]['maturity']['incomplete'] = [{'criterion': 'C1', 'ticket': 'T1', 'gate': 'integration'}]
        self.write_plan()
        Controller(self.path, self.root, state_root=self.root / 'future-valid').execute('init')

    def test_maturity_and_contract_reference_types_rejected(self):
        original = copy.deepcopy(self.plan)
        for key, value in (('expected', ''), ('incomplete', 'later'), ('functional_review', 'true'), ('final_qa', None)):
            with self.subTest(key=key):
                self.plan = copy.deepcopy(original)
                self.plan['tickets'][0]['maturity'][key] = value
                self.write_plan()
                with self.assertRaises(ValueError):
                    Controller(self.path, self.root)
        for refs in ('contract.md', [None], [''], None):
            with self.subTest(refs=refs):
                self.plan = copy.deepcopy(original)
                self.plan['shared_contracts'] = refs
                self.write_plan()
                with self.assertRaisesRegex(ValueError, 'shared_contracts'):
                    Controller(self.path, self.root)
        self.plan = copy.deepcopy(original)
        self.plan.pop('shared_contracts')
        self.write_plan()
        with self.assertRaisesRegex(ValueError, 'shared_contracts'):
            Controller(self.path, self.root)
        self.plan['shared_contracts'] = []
        self.write_plan()
        Controller(self.path, self.root)

    def test_checkpoint_uses_installed_rules_without_global_session_writes(self):
        home = self.root / 'isolated-home'
        home.mkdir()
        with patch.dict('os.environ', {'CODEX_HOME': str(home), 'CODEX_THREAD_ID': 'offline-test'}):
            self.c.execute('transition', ticket='T1', to='IN_PROGRESS')
            pointer = self.c.execute('checkpoint')
        self.assertEqual(list(home.iterdir()), [])
        blob = json.loads(Path(pointer['path']).read_text(encoding='utf-8'))
        skill = Path(__file__).resolve().parent.parent
        self.assertIn(str(skill / 'SKILL.md'), blob['rules'])
        self.assertIn(str(skill / 'references/quality-gates.md'), blob['rules'])
        self.assertEqual(blob['run_id'], 'offline-test')

    def test_recover_rechecks_acceptance_and_preserves_local_context_guard(self):
        from continuity import recover
        self.accepted()
        self.assertEqual(recover(self.c)['accepted'], ['T1'])
        (self.root / 'code.py').write_text('changed after acceptance', encoding='utf-8')
        self.assertEqual(recover(self.c)['remaining'], ['T1'])
        self.c.execute('context-begin', operation_id='local-boundary')
        with self.assertRaisesRegex(ValueError, 'compaction pending'):
            self.c.execute('change', ticket='T1', kind='focused', paths=['code.py'])
        self.c.execute('context-end', operation_id='local-boundary')
        self.c.execute('change', ticket='T1', kind='focused', paths=['code.py'])
        self.assertEqual(recover(self.c)['accepted'], [])


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(WorkflowTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    output = Path(__file__).with_name('test-results.json')
    output.write_text(json.dumps({'tests_run': result.testsRun, 'failures': [str(t) for t, _ in result.failures], 'errors': [str(t) for t, _ in result.errors], 'status': 'PASS' if result.wasSuccessful() else 'FAIL', 'surface': 'real Python filesystem/controller/CLI/multiprocess; no semantic agent validation'}, indent=2), encoding='utf-8')
    sys.exit(not result.wasSuccessful())
