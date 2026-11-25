import importlib.util
from contextlib import contextmanager
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'feature_supervisor.py'
spec = importlib.util.spec_from_file_location('feature_supervisor', SCRIPT)
fs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fs)


class SupervisorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'Tickets').mkdir()
        (self.root / 'Index.md').write_text('\n'.join(
            f'- [[Tickets/{name}]]' for name in ('b02-t03', 'b01-t02', 'b01-t01')), encoding='utf-8')
        for name, blocker in [('b01-t01', None), ('b01-t02', 'b01-t01'), ('b02-t03', 'b01-t02')]:
            dependency = f'blocked_by:\n  - "[[Tickets/{blocker}]]"' if blocker else 'blocked_by: []'
            (self.root / 'Tickets' / (name + '.md')).write_text(
                f'---\ntype: ticket\nticket_status: open\ntriage_role: ready-for-agent\n{dependency}\n---\n\n'
                f'# {name}\n\n## Acceptance Criteria\n\n- [ ] User sees expected result\n', encoding='utf-8')

    def claim(self, name=None):
        return fs.claim(self.root, 'owner', 'run', 'native-agent-1', name)

    def update(self, data, name='b01-t01'):
        return fs.checkpoint(self.root, name, 'owner', 'run', data)

    def passing(self, name='b01-t01'):
        path = self.root / 'Tickets' / (name + '.md')
        path.write_text(path.read_text(encoding='utf-8').replace('- [ ]', '- [x]'), encoding='utf-8')
        (self.root / 'evidence.txt').write_text('actual local validation output', encoding='utf-8')
        return {'status': 'READY', 'checkpoint': 'Checks completed', 'next_action': 'Supervisor accepts',
                'evidence': ['evidence.txt'],
                'validators': [{'name': 'focused unittest', 'status': 'PASS', 'evidence': ['evidence.txt']}],
                'supervisor_review': {'status': 'PASS', 'summary': 'Reviewed evidence against requested outcome and criteria',
                                      'evidence': ['evidence.txt']}}

    def test_discovery_is_read_only_ordered_and_dependencies_release(self):
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(fs.inspect(self.root)['frontier'], ['b01-t01'])
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
        for name, next_name in [('b01-t01', 'b01-t02'), ('b01-t02', 'b02-t03'), ('b02-t03', None)]:
            self.assertEqual(self.claim()['ticket'], name)
            self.update(self.passing(name), name)
            fs.accept(self.root, name, 'owner', 'run')
            self.assertEqual(fs.inspect(self.root)['frontier'], [next_name] if next_name else [])

    def test_claim_idempotent_restart_and_wrong_owner_rejected(self):
        first = self.claim()
        self.assertEqual(self.claim('b01-t01'), first)
        with self.assertRaises(fs.Error):
            fs.claim(self.root, 'other', 'run', 'native-agent-1', 'b01-t01')
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--workspace', str(self.root),
                                 'inspect'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['tickets'][0]['checkpoint'], first)

    def test_retry_budget_persists_and_blocked_never_reclaims(self):
        self.claim()
        retry = {'status': 'RETRY', 'checkpoint': 'Failure one', 'next_action': 'Retry narrow fix'}
        self.assertEqual(self.update(retry)['attempts'], 2)
        path = self.root / 'Tickets' / 'b01-t01.md'
        before = path.read_bytes()
        self.assertEqual(self.update(retry)['attempts'], 2)
        self.assertEqual(path.read_bytes(), before)
        self.update({'status': 'RUNNING', 'checkpoint': 'Attempt two', 'next_action': 'Validate'})
        blocked = self.update({**retry, 'checkpoint': 'Failure two'})
        self.assertEqual(blocked['status'], 'BLOCKED')
        self.assertEqual(fs.sw._ticket_status(path), 'claimed')
        self.assertEqual(self.claim('b01-t01'), blocked)
        with self.assertRaises(fs.Error):
            self.update(retry)
        with self.assertRaises(fs.Error):
            self.claim()

    def test_two_real_processes_only_one_claims(self):
        commands = [[sys.executable, '-B', str(SCRIPT), '--workspace', str(self.root), 'claim',
                     '--ticket', 'b01-t01', '--owner', owner, '--run', 'run', '--agent', 'agent']
                    for owner in ('first', 'second')]
        processes = [subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for c in commands]
        results = [(*p.communicate(timeout=15), p.returncode) for p in processes]
        self.assertEqual(sorted(r[2] for r in results), [0, 2], results)
        self.assertEqual((self.root / 'Tickets' / 'b01-t01.md').read_text(encoding='utf-8').count(fs.MARKER), 1)
        self.assertFalse(list(self.root.rglob('*.lock')))

    def test_blocked_ticket_allows_independent_work_and_stops_when_none_remain(self):
        independent = self.root / 'Tickets' / 'b02-t03.md'
        independent.write_text(independent.read_text(encoding='utf-8').replace(
            'blocked_by:\n  - "[[Tickets/b01-t02]]"', 'blocked_by: []'), encoding='utf-8')
        self.claim('b01-t01')
        self.update({'status': 'BLOCKED', 'checkpoint': 'Credential unavailable',
                     'next_action': 'Human intervention required'})
        self.assertEqual(fs.inspect(self.root)['frontier'], ['b02-t03'])
        self.claim('b02-t03')
        self.update(self.passing('b02-t03'), 'b02-t03')
        fs.accept(self.root, 'b02-t03', 'owner', 'run')
        snapshot = fs.inspect(self.root)
        self.assertEqual(snapshot['frontier'], [])
        self.assertNotEqual({t['ticket_status'] for t in snapshot['tickets']}, {'resolved'})
        with self.assertRaises(fs.Error):
            self.claim()

    def test_failed_claim_is_recoverable_without_mutation(self):
        before = (self.root / 'Tickets' / 'b01-t02.md').read_bytes()
        with self.assertRaises(fs.Error):
            self.claim('b01-t02')
        self.assertEqual(before, (self.root / 'Tickets' / 'b01-t02.md').read_bytes())
        self.assertEqual(self.claim()['ticket'], 'b01-t01')

    def test_unsupported_dependency_and_index_formats_fail_closed(self):
        path = self.root / 'Tickets' / 'b01-t02.md'
        original = path.read_text(encoding='utf-8')
        for dep in ('blocked_by: ["[[Tickets/b01-t01]]"]', 'blocked_by:\n  - b01-t01',
                    'blocked_by:\n  - "[[Tickets/missing]]"'):
            path.write_text(original.replace('blocked_by:\n  - "[[Tickets/b01-t01]]"', dep), encoding='utf-8')
            with self.assertRaises(fs.Error):
                self.claim()
        path.write_text(original, encoding='utf-8')
        index = self.root / 'Index.md'
        original_index = index.read_text(encoding='utf-8')
        for link in ('[[Tickets/b01-t01.md]]', '[[Tickets/b01-t01|alias]]', '[T01](Tickets/b01-t01.md)',
                     '[[Tickets/missing]]'):
            index.write_text(original_index.replace('[[Tickets/b01-t01]]', link), encoding='utf-8')
            with self.assertRaises(fs.Error):
                fs.inspect(self.root)

    def test_accept_requires_checks_evidence_validator_and_semantic_review(self):
        self.claim()
        data = self.passing()
        path = self.root / 'Tickets' / 'b01-t01.md'
        path.write_text(path.read_text(encoding='utf-8').replace('- [x]', '- [ ]'), encoding='utf-8')
        self.update(data)
        with self.assertRaises(fs.Error):
            fs.accept(self.root, 'b01-t01', 'owner', 'run')
        for patch in ({'evidence': [], 'validators': [], 'supervisor_review': None},
                      {'validators': []}, {'supervisor_review': None},
                      {'validators': [{'name': 'test', 'status': 'FAIL', 'evidence': ['evidence.txt']}]}):
            self.update({**self.passing(), **patch})
            with self.assertRaises(fs.Error):
                fs.accept(self.root, 'b01-t01', 'owner', 'run')
        self.update(self.passing())
        first = fs.accept(self.root, 'b01-t01', 'owner', 'run')
        before = path.read_bytes()
        self.assertEqual(fs.accept(self.root, 'b01-t01', 'owner', 'run'), first)
        self.assertEqual(before, path.read_bytes())

    def test_missing_and_stale_evidence_and_changed_ticket(self):
        self.claim()
        with self.assertRaises(fs.Error):
            self.update({**self.passing(), 'evidence': ['missing.txt']})
        for mode in ('changed', 'removed', 'ticket'):
            self.update(self.passing())
            if mode == 'changed':
                (self.root / 'evidence.txt').write_text('changed output', encoding='utf-8')
            elif mode == 'removed':
                (self.root / 'evidence.txt').unlink()
            else:
                path = self.root / 'Tickets' / 'b01-t01.md'
                path.write_text(path.read_text(encoding='utf-8').replace('User sees', 'User always sees'), encoding='utf-8')
            with self.assertRaises(fs.Error):
                fs.accept(self.root, 'b01-t01', 'owner', 'run')

    def test_checkpoint_idempotence_and_comment_safety(self):
        self.claim()
        data = {'status': 'RUNNING', 'checkpoint': 'Contains --> and Unicode ação', 'next_action': 'Continue'}
        self.update(data)
        path = self.root / 'Tickets' / 'b01-t01.md'
        before = path.read_bytes()
        self.assertEqual(self.update(data)['checkpoint'], data['checkpoint'])
        self.assertEqual(before, path.read_bytes())

    def test_unchecked_alternate_checkbox_and_unknown_status_fail_closed(self):
        self.claim()
        data = self.passing()
        path = self.root / 'Tickets' / 'b01-t01.md'
        path.write_text(path.read_text(encoding='utf-8').replace('- [x] User', '* [ ] User'), encoding='utf-8')
        self.update(data)
        with self.assertRaises(fs.Error):
            fs.accept(self.root, 'b01-t01', 'owner', 'run')
        path.write_text(path.read_text(encoding='utf-8').replace('ticket_status: claimed', 'ticket_status: blocked'), encoding='utf-8')
        with self.assertRaises(fs.Error):
            fs.inspect(self.root)

    def test_stale_accepted_predecessor_blocks_successor_and_replay(self):
        self.claim()
        self.update(self.passing())
        fs.accept(self.root, 'b01-t01', 'owner', 'run')
        self.assertEqual(fs.inspect(self.root)['frontier'], ['b01-t02'])
        (self.root / 'evidence.txt').write_text('changed after acceptance', encoding='utf-8')
        with self.assertRaises(fs.Error):
            self.claim('b01-t02')
        with self.assertRaises(fs.Error):
            fs.accept(self.root, 'b01-t01', 'owner', 'run')

    def test_unmanaged_resolved_predecessor_requires_reconciliation(self):
        path = self.root / 'Tickets' / 'b01-t01.md'
        path.write_text(path.read_text(encoding='utf-8').replace('ticket_status: open', 'ticket_status: resolved'), encoding='utf-8')
        with self.assertRaises(fs.Error):
            fs.inspect(self.root)

    def test_dispatch_identity_and_block_metadata_are_persistent(self):
        path = self.root / 'Tickets' / 'b01-t01.md'
        path.write_text(path.read_text(encoding='utf-8').replace('type: ticket', 'type: ticket\nblock: B01'), encoding='utf-8')
        value = fs.claim(self.root, 'owner', 'run')
        self.assertEqual(value['agent'], 'pending-dispatch')
        self.assertEqual(value['block'], 'B01')
        self.assertEqual(value['dependencies'], [])
        self.assertTrue(value['timestamp'])
        result = self.update({'status': 'RUNNING', 'agent': 'native-id-123', 'checkpoint': 'Dispatched', 'next_action': 'Wait'})
        self.assertEqual(result['agent'], 'native-id-123')
        self.assertEqual(fs.latest(path)['agent'], 'native-id-123')
        with self.assertRaises(fs.Error):
            self.update({'status': 'BLOCKED', 'agent': 'cannot-change', 'checkpoint': 'Stop', 'next_action': 'Human'})

    def test_missing_adapter_cli_has_clear_recoverable_error(self):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--workspace', str(self.root),
                                 '--adapter', str(self.root / 'missing.py'), 'inspect'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('adapter missing', result.stderr)

    def test_accept_rereads_native_writer_edit_before_ticket_lock(self):
        self.claim()
        self.update(self.passing())
        target = self.root / 'Tickets' / 'b01-t01.md'
        original_lock = fs.sw._exclusive_lock
        edited = []

        @contextmanager
        def native_edit_then_lock(path):
            if path == target and not edited:
                with original_lock(path):
                    text = path.read_text(encoding='utf-8')
                    path.write_text(text.replace('- [x] User sees expected result',
                                                 '- [x] User sees expected result\n- [ ] New unmet criterion'), encoding='utf-8')
                    edited.append(True)
            with original_lock(path):
                yield

        with patch.object(fs.sw, '_exclusive_lock', native_edit_then_lock):
            with self.assertRaises(fs.Error):
                fs.accept(self.root, 'b01-t01', 'owner', 'run')
        self.assertEqual(fs.sw._ticket_status(target), 'claimed')
        self.assertEqual(fs.latest(target)['status'], 'READY')

    def test_checkpoint_rereads_native_writer_status_before_ticket_lock(self):
        self.claim()
        target = self.root / 'Tickets' / 'b01-t01.md'
        original_lock = fs.sw._exclusive_lock
        edited = []

        @contextmanager
        def native_transition_then_lock(path):
            if path == target and not edited:
                with original_lock(path):
                    fs.sw._transition_ticket(path, 'resolved')
                    edited.append(True)
            with original_lock(path):
                yield

        with patch.object(fs.sw, '_exclusive_lock', native_transition_then_lock):
            with self.assertRaises(fs.Error):
                self.update({'status': 'RUNNING', 'checkpoint': 'Old state', 'next_action': 'Continue'})
        self.assertEqual(fs.latest(target)['status'], 'CLAIMED')

    def test_accept_rechecks_changed_dependencies_after_fresh_ready(self):
        self.claim()
        target = self.root / 'Tickets' / 'b01-t01.md'
        text = target.read_text(encoding='utf-8')
        target.write_text(text.replace('blocked_by: []', 'blocked_by:\n  - "[[Tickets/b02-t03]]"'), encoding='utf-8')
        self.update(self.passing())
        with self.assertRaises(fs.Error):
            fs.accept(self.root, 'b01-t01', 'owner', 'run')
        self.assertEqual(fs.sw._ticket_status(target), 'claimed')

    def test_feature_identity_distinguishes_sibling_workspaces(self):
        self.assertNotEqual(fs.feature(self.root / 'first'), fs.feature(self.root / 'second'))
        self.assertEqual(fs.inspect(self.root)['feature'], str(self.root.resolve()))

    def test_explicit_adoption_reconciles_resolved_history_idempotently(self):
        target = self.root / 'Tickets' / 'b01-t01.md'
        target.write_text(target.read_text(encoding='utf-8').replace('ticket_status: open', 'ticket_status: resolved'), encoding='utf-8')
        data = self.passing()
        with self.assertRaises(fs.Error):
            fs.inspect(self.root)
        first = fs.adopt(self.root, 'b01-t01', 'owner', 'run', data)
        self.assertEqual(first['status'], 'ACCEPTED')
        self.assertEqual(fs.sw._ticket_status(target), 'resolved')
        self.assertEqual(fs.inspect(self.root)['frontier'], ['b01-t02'])
        before = target.read_bytes()
        self.assertEqual(fs.adopt(self.root, 'b01-t01', 'owner', 'run', data), first)
        self.assertEqual(target.read_bytes(), before)

    def test_adoption_rejects_unchecked_missing_stale_or_foreign_proof(self):
        target = self.root / 'Tickets' / 'b01-t01.md'
        target.write_text(target.read_text(encoding='utf-8').replace('ticket_status: open', 'ticket_status: resolved'), encoding='utf-8')
        data = self.passing()
        target.write_text(target.read_text(encoding='utf-8').replace('- [x]', '- [ ]'), encoding='utf-8')
        with self.assertRaises(fs.Error):
            fs.adopt(self.root, 'b01-t01', 'owner', 'run', data)
        data = self.passing()
        with self.assertRaises(fs.Error):
            fs.adopt(self.root, 'b01-t01', 'owner', 'run', {**data, 'evidence': ['absent.txt']})
        fs.adopt(self.root, 'b01-t01', 'owner', 'run', data)
        with self.assertRaises(fs.Error):
            fs.adopt(self.root, 'b01-t01', 'foreign', 'run', data)
        (self.root / 'evidence.txt').write_text('changed', encoding='utf-8')
        with self.assertRaises(fs.Error):
            fs.adopt(self.root, 'b01-t01', 'owner', 'run', data)

    def test_adoption_only_resolved_and_checks_dependencies(self):
        data = self.passing()
        with self.assertRaises(fs.Error):
            fs.adopt(self.root, 'b01-t01', 'owner', 'run', data)
        self.claim()
        with self.assertRaises(fs.Error):
            fs.adopt(self.root, 'b01-t01', 'owner', 'run', data)
        target = self.root / 'Tickets' / 'b01-t02.md'
        target.write_text(target.read_text(encoding='utf-8').replace('ticket_status: open', 'ticket_status: resolved'), encoding='utf-8')
        with self.assertRaises(fs.Error):
            fs.adopt(self.root, 'b01-t02', 'owner', 'run', self.passing('b01-t02'))

    def test_adoption_recovers_exact_ready_owner_after_resolved_transition_crash(self):
        self.claim()
        data = self.passing()
        ready = self.update(data)
        target = self.root / 'Tickets' / 'b01-t01.md'
        fs.sw.transition_ticket(target, 'resolved')
        with self.assertRaises(fs.Error):
            fs.adopt(self.root, 'b01-t01', 'other-owner', 'run', data)
        value = fs.adopt(self.root, 'b01-t01', 'owner', 'run', data)
        self.assertEqual(value['attempts'], ready['attempts'])
        self.assertEqual(value['status'], 'ACCEPTED')

    def test_adoption_handles_multiple_historical_resolved_in_dependency_order(self):
        for name in ('b01-t01', 'b01-t02'):
            target = self.root / 'Tickets' / (name + '.md')
            target.write_text(target.read_text(encoding='utf-8').replace('ticket_status: open', 'ticket_status: resolved'), encoding='utf-8')
        with self.assertRaises(fs.Error):
            fs.adopt(self.root, 'b01-t02', 'owner', 'run', self.passing('b01-t02'))
        fs.adopt(self.root, 'b01-t01', 'owner', 'run', self.passing())
        fs.adopt(self.root, 'b01-t02', 'owner', 'run', self.passing('b01-t02'))
        self.assertEqual(fs.inspect(self.root)['frontier'], ['b02-t03'])

    def test_adoption_cli_and_changed_replay_are_controlled(self):
        target = self.root / 'Tickets' / 'b01-t01.md'
        target.write_text(target.read_text(encoding='utf-8').replace('ticket_status: open', 'ticket_status: resolved'), encoding='utf-8')
        data = self.passing()
        data_path = self.root / 'adoption.json'
        data_path.write_text(json.dumps(data), encoding='utf-8')
        command = [sys.executable, '-B', str(SCRIPT), '--workspace', str(self.root), 'adopt',
                   '--ticket', 'b01-t01', '--owner', 'owner', '--run', 'run', '--data', str(data_path)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'ACCEPTED')
        before = target.read_bytes()
        with self.assertRaises(fs.Error):
            fs.adopt(self.root, 'b01-t01', 'owner', 'run', {**data, 'checkpoint': 'Different decision'})
        self.assertEqual(before, target.read_bytes())


if __name__ == '__main__':
    unittest.main()
