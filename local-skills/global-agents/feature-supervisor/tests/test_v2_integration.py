"""Isolated integration of the installed Smart V2 controller and canonical adapter.

Actor identities and semantic PASS judgments are synthetic protocol inputs here.
This suite verifies the real mechanisms; it does not certify native-agent review.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
SMART = Path('C:/Users/caila/.agents/skills/smart-orchestrator/scripts')
ADAPTER = Path('D:/newmove/.agents/skills/spec-workspace/scripts/spec_workspace.py')
sys.path.insert(0, str(SMART))
from controller import Controller, canonical, digest
from continuity import recover
from test_controller import example

adapter_spec = importlib.util.spec_from_file_location('v2_native_workspace_adapter', ADAPTER)
adapter = importlib.util.module_from_spec(adapter_spec)
adapter_spec.loader.exec_module(adapter)


class V2IntegrationTests(unittest.TestCase):
    observations = []

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='feature-supervisor-v2-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / 'Spec Driven'
        self.workspace.mkdir()
        self.ticket = adapter.write_artifact(
            self.workspace, 'ticket', 'Synthetic increment',
            '## Acceptance Criteria\n\n- [ ] Increment returns the next integer.\n',
            {'artifact_id': 'T1', 'block': 'B01'})
        self.plan = copy.deepcopy(example())
        self.plan['feature'] = 'feature_supervisor_v2_synthetic'
        self.plan['tickets'][0]['ticket'] = self.ticket.relative_to(self.root).as_posix()
        self.plan_path = self.root / 'execution-plan.json'
        self.plan_path.write_text(json.dumps(self.plan), encoding='utf-8')
        (self.root / 'AGENTS.md').write_text('Synthetic validation only. No external effects.\n', encoding='utf-8')
        (self.root / 'SPEC.md').write_text('Increment an integer by one. Synthetic controller protocol fixture.\n', encoding='utf-8')
        (self.root / 'contract.md').write_text('increment(int) -> int; stable() -> str.\n', encoding='utf-8')
        (self.root / 'code.py').write_text('def increment(value):\n    return value + 1\n', encoding='utf-8')
        (self.root / 'other.py').write_text('def stable():\n    return "stable"\n', encoding='utf-8')
        (self.root / 'config.json').write_text('{"fixture": "synthetic"}', encoding='utf-8')
        (self.root / 'env.json').write_text(json.dumps({'python': platform.python_version(), 'scope': 'isolated synthetic'}), encoding='utf-8')
        validation = subprocess.run(
            [sys.executable, '-B', '-c',
             'from code import increment; from other import stable; '
             'assert increment(-1) == 0; assert increment(0) == 1; '
             'assert increment(41) == 42; assert stable() == "stable"; print("PASS: four fixture assertions")'],
            cwd=self.root, capture_output=True, text=True, encoding='utf-8', timeout=15)
        self.assertEqual(validation.returncode, 0, validation.stderr)
        (self.root / 'artifact.txt').write_text(validation.stdout, encoding='utf-8')
        self.c = Controller(self.plan_path, self.root, state_root=self.root / 'v2-state',
                            resources_root=self.root / 'v2-resources')
        self.initial = self.c.execute('init')

    def cli(self, command):
        result = subprocess.run(
            [sys.executable, '-B', str(SMART / 'controller.py'), '--plan', str(self.plan_path),
             '--root', str(self.root), '--state-root', str(self.root / 'v2-state'),
             '--resources-root', str(self.root / 'v2-resources'), command],
            capture_output=True, text=True, encoding='utf-8', timeout=20)
        return result, json.loads(result.stdout) if result.returncode == 0 else None

    def proof(self, gate):
        definition = next(g for g in self.plan['tickets'][0]['gates'] if g['id'] == gate)
        return self.c.execute('evidence', ticket='T1', gate=gate, proof=definition['artifacts'][0],
                              artifact='artifact.txt', actor='integrator' if gate == 'integration' else 'reviewer',
                              code=definition['scope'], config=['config.json'], env=['env.json'], result='PASS')

    def integration_ready(self):
        adapter.transition_ticket(self.ticket, 'claimed')
        adapter.append_comment(self.ticket, 'Synthetic V2 run: canonical claim; Controller owns operational stages.')
        self.c.execute('transition', ticket='T1', to='IN_PROGRESS')
        for gate in ('local', 'unaffected'):
            self.proof(gate)
        self.c.execute('transition', ticket='T1', to='CODE_READY')
        self.c.execute('transition', ticket='T1', to='REVIEW_READY')
        for gate in ('standards', 'spec', 'security'):
            self.proof(gate)
        self.c.execute('transition', ticket='T1', to='REVIEWED')
        self.c.execute('transition', ticket='T1', to='INTEGRATION_READY')
        self.proof('integration')

    def mark_criteria_checked(self):
        with adapter._exclusive_lock(self.ticket):
            text = self.ticket.read_text(encoding='utf-8')
            self.ticket.write_text(text.replace('- [ ]', '- [x]'), encoding='utf-8')

    def test_v2_acceptance_checkpoint_and_fresh_process_canonical_sync(self):
        self.assertEqual(adapter._ticket_status(self.ticket), 'open')
        self.assertEqual(adapter.frontier(self.workspace), [self.ticket])
        self.integration_ready()
        self.assertEqual(adapter._ticket_status(self.ticket), 'claimed')
        self.c.execute('transition', ticket='T1', to='ACCEPTED')
        self.mark_criteria_checked()
        pointer = self.c.execute('checkpoint')
        blob = json.loads(Path(pointer['path']).read_text(encoding='utf-8'))
        self.assertEqual(digest(canonical(blob)), pointer['sha256'])
        self.assertEqual(blob['tickets']['T1']['stage'], 'ACCEPTED')
        self.assertTrue(all(e['valid'] for proofs in blob['tickets']['T1']['evidence'].values() for e in proofs.values()))
        before = self.c.path.read_bytes()
        result, recovered = self.cli('recover')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(recovered['accepted'], ['T1'])
        self.assertEqual(recovered['remaining'], [])
        self.assertEqual(before, self.c.path.read_bytes(), 'Recovery must never restore a checkpoint over the ledger')
        # Orchestrator decision uses current Controller validity; no direct helper ledger.
        self.assertTrue(recovered['tickets']['T1']['acceptance_current'])
        adapter.transition_ticket(self.ticket, 'resolved')
        adapter.append_comment(self.ticket, 'Synthetic V2 acceptance: fresh-process recover confirms current gates.')
        self.assertEqual(adapter._ticket_status(self.ticket), 'resolved')
        self.assertEqual(adapter.frontier(self.workspace), [])
        self.assertNotIn('feature-supervisor:checkpoint', self.ticket.read_text(encoding='utf-8'))
        self.assertTrue(self.c.execute('close')['closed'])
        self.observations.append({'case': self._testMethodName, 'canonical': ['open', 'claimed', 'resolved'],
                                  'fresh_process_accepted': recovered['accepted'], 'checkpoint_hash_verified': True,
                                  'controller_closed': True, 'direct_helper_ledger': False})

    def test_stale_proof_blocks_acceptance_and_fresh_process_recovery(self):
        self.integration_ready()
        self.c.execute('checkpoint')
        (self.root / 'code.py').write_text('def increment(value):\n    return value + 2\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'missing/stale'):
            self.c.execute('transition', ticket='T1', to='ACCEPTED')
        result, recovered = self.cli('recover')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(recovered['accepted'], [])
        self.assertEqual(recovered['remaining'], ['T1'])
        self.assertFalse(recovered['tickets']['T1']['gate_validity']['local'])
        self.assertEqual(adapter._ticket_status(self.ticket), 'claimed')
        self.observations.append({'case': self._testMethodName, 'canonical': 'claimed',
                                  'accepted': recovered['accepted'], 'remaining': recovered['remaining'],
                                  'stale_local_gate': not recovered['tickets']['T1']['gate_validity']['local']})

    def test_previously_accepted_stale_proof_is_not_recovered_as_current(self):
        self.integration_ready()
        self.c.execute('transition', ticket='T1', to='ACCEPTED')
        self.mark_criteria_checked()
        self.assertTrue(self.c.execute('status')['tickets']['T1']['acceptance_current'])
        adapter.transition_ticket(self.ticket, 'resolved')
        self.c.execute('checkpoint')
        (self.root / 'env.json').write_text('{"fixture":"changed environment"}', encoding='utf-8')
        result, recovered = self.cli('recover')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(recovered['accepted'], [])
        self.assertEqual(recovered['remaining'], ['T1'])
        self.assertFalse(recovered['tickets']['T1']['acceptance_current'])
        self.assertIn('stale', recovered['tickets']['T1']['acceptance_invalid_reason'])
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.c.execute('close')
        # Canonical transitions are monotonic: stale proof does not authorize rewriting history.
        self.assertEqual(adapter._ticket_status(self.ticket), 'resolved')
        self.observations.append({'case': self._testMethodName, 'canonical_historical': 'resolved',
                                  'acceptance_current': False, 'remaining': recovered['remaining'],
                                  'requires_reconciliation': True})

    def test_init_reuses_owner_and_plan_mutation_cannot_resume(self):
        second = self.c.execute('init')
        self.assertEqual(second['owner'], self.initial['owner'])
        self.assertEqual(len(second['history']), 1)
        self.c.execute('checkpoint')
        self.plan['tickets'][0]['estimate_minutes'] = 11
        self.plan_path.write_text(json.dumps(self.plan), encoding='utf-8')
        result, _ = self.cli('recover')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('plan changed', result.stderr)
        self.assertEqual(adapter._ticket_status(self.ticket), 'open')
        self.observations.append({'case': self._testMethodName, 'idempotent_init': True,
                                  'changed_plan_recovery_rejected': True, 'canonical': 'open'})

    def test_missing_gate_evidence_does_not_advance_canonical_ticket(self):
        adapter.transition_ticket(self.ticket, 'claimed')
        self.c.execute('transition', ticket='T1', to='IN_PROGRESS')
        with self.assertRaisesRegex(ValueError, 'missing/stale'):
            self.c.execute('transition', ticket='T1', to='CODE_READY')
        (self.root / 'artifact.txt').unlink()
        with self.assertRaisesRegex(ValueError, 'missing'):
            self.proof('local')
        self.assertEqual(self.c.execute('status')['tickets']['T1']['stage'], 'IN_PROGRESS')
        self.assertEqual(adapter._ticket_status(self.ticket), 'claimed')
        self.observations.append({'case': self._testMethodName, 'missing_gate_rejected': True,
                                  'missing_artifact_rejected': True, 'canonical': 'claimed'})

    def test_checkpoint_is_not_a_replacement_for_missing_controller_state(self):
        self.integration_ready()
        pointer = self.c.execute('checkpoint')
        checkpoint_path = Path(pointer['path'])
        checkpoint_bytes = checkpoint_path.read_bytes()
        self.c.path.unlink()
        result, _ = self.cli('recover')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('initialize first', result.stderr)
        self.assertFalse(self.c.path.exists())
        self.assertEqual(checkpoint_path.read_bytes(), checkpoint_bytes)
        self.assertEqual(adapter._ticket_status(self.ticket), 'claimed')
        self.observations.append({'case': self._testMethodName, 'checkpoint_restored_missing_ledger': False,
                                  'recovery_rejected': True, 'canonical': 'claimed'})


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(V2IntegrationTests))
    sources = [Path(__file__), SMART / 'controller.py', SMART / 'continuity.py', SMART / 'test_controller.py', ADAPTER]
    report = {'status': 'PASS' if result.wasSuccessful() else 'FAIL', 'tests_run': result.testsRun,
              'failures': [str(t) for t, _ in result.failures], 'errors': [str(t) for t, _ in result.errors],
              'skipped': [str(t) for t, _ in result.skipped], 'observations': V2IntegrationTests.observations,
              'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
              'apis': ['test_controller.example', 'Controller.execute(init/evidence/transition/status/checkpoint/close)',
                       'continuity.recover via actual controller.py recover subprocess',
                       'spec_workspace.write_artifact/transition_ticket/append_comment/frontier/_exclusive_lock'],
              'limits': ['Synthetic actors and semantic PASS inputs; not native-agent semantic review.',
                         'Canonical sync uses installed adapter primitives under orchestrator control; no installed automatic sync API.',
                         'Already resolved canonical notes retain history when Controller acceptance becomes stale; reconcile explicitly.',
                         'No real feature, ERP writes, production, CI, network or external sends.']}
    output = Path(__file__).parent / 'evidence' / 'v2-results.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(not result.wasSuccessful())
