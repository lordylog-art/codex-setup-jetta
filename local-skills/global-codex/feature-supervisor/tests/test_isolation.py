"""Real helper/adapter subprocesses with an audited, temporary write boundary."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'scripts' / 'feature_supervisor.py'
ADAPTER = Path('D:/newmove/.agents/skills/spec-workspace/scripts/spec_workspace.py')

# This child runs the actual CLI; the audit hook observes/rejects Python filesystem writes.
CHILD = r'''
import json, os, pathlib, runpy, sys
sys.dont_write_bytecode = True
sandbox, report, helper, mode, *arguments = sys.argv[1:]
root = pathlib.Path(sandbox).resolve()
events = []
def audit(event, args):
    paths = []
    if event == 'open':
        name, mode, flags = args
        writable = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (
            isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if writable:
            paths = [name]
    elif event in {'os.rename', 'os.link', 'os.symlink'}:
        paths = list(args[:2])
    elif event in {'os.remove', 'os.rmdir', 'os.mkdir', 'os.chmod', 'os.chown', 'os.utime', 'os.truncate'}:
        paths = [args[0]]
    if not paths:
        return
    resolved = []
    for value in paths:
        if not isinstance(value, (str, bytes, os.PathLike)):
            raise PermissionError('Unattributable filesystem mutation rejected')
        resolved.append(str(pathlib.Path(os.fsdecode(value)).resolve()))
    allowed = all(pathlib.Path(p) == root or root in pathlib.Path(p).parents for p in resolved)
    events.append({'event': event, 'paths': resolved, 'allowed': allowed})
    if not allowed:
        raise PermissionError('Audit boundary rejected filesystem mutation: ' + ', '.join(resolved))
sys.addaudithook(audit)
exit_code = 0
try:
    if mode == 'probe':
        pathlib.Path(arguments[0]).write_text('must not escape', encoding='utf-8')
    else:
        sys.argv = [helper, *arguments]
        runpy.run_path(helper, run_name='__main__')
except SystemExit as exc:
    exit_code = exc.code if isinstance(exc.code, int) else 1
except PermissionError as exc:
    print(str(exc), file=sys.stderr)
    exit_code = 77
finally:
    with open(report, 'w', encoding='utf-8') as stream:
        json.dump({'pid': os.getpid(), 'exit_code': exit_code, 'events': events}, stream, indent=2)
raise SystemExit(exit_code)
'''


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture(root):
    (root / 'Tickets').mkdir(parents=True)
    (root / 'Index.md').write_text('[[Tickets/t01]]\n', encoding='utf-8')
    (root / 'Tickets' / 't01.md').write_text(
        '---\ntype: ticket\nticket_status: open\ntriage_role: ready-for-agent\n'
        'blocked_by: []\n---\n\n## Acceptance Criteria\n\n- [ ] Synthetic result\n', encoding='utf-8')


class IsolationTests(unittest.TestCase):
    def test_real_cli_writes_stay_in_sandbox_and_restart_retains_checkpoint(self):
        originals = [HELPER, ADAPTER, ROOT / 'SKILL.md', *sorted((ROOT / 'references').glob('*.md'))]
        before = {str(p): digest(p) for p in originals}
        runs = []
        with tempfile.TemporaryDirectory(prefix='feature-supervisor-isolation-') as temporary:
            outer = Path(temporary)
            sandbox = outer / 'allowed'
            sandbox.mkdir()
            workspace = sandbox / 'feature'
            fixture(workspace)
            adapter = sandbox / 'spec_workspace.py'
            shutil.copyfile(ADAPTER, adapter)
            self.assertEqual(digest(adapter), before[str(ADAPTER)])
            protected = outer / 'protected-erp-and-tickets'
            fixture(protected)
            (protected / 'erp-source.txt').write_text('protected ERP stand-in\n', encoding='utf-8')
            protected_before = {str(p): digest(p) for p in protected.rglob('*') if p.is_file()}
            child = sandbox / 'audit_child.py'
            child.write_text(CHILD, encoding='utf-8')

            def invoke(label, command, target=workspace, expected=0, mode='cli'):
                report = sandbox / f'audit-{len(runs)}.json'
                arguments = command if mode == 'probe' else [
                    '--adapter', str(adapter), '--workspace', str(target), *command]
                process = subprocess.run(
                    [sys.executable, '-B', str(child), str(sandbox), str(report), str(HELPER), mode, *arguments],
                    capture_output=True, text=True, timeout=30, cwd=sandbox)
                self.assertEqual(process.returncode, expected, process.stdout + process.stderr)
                observation = json.loads(report.read_text(encoding='utf-8'))
                self.assertEqual(observation['exit_code'], expected)
                runs.append({'label': label, 'exit_code': process.returncode,
                             'stdout': process.stdout.strip(), 'stderr': process.stderr.strip(), **observation})
                return json.loads(process.stdout) if process.stdout.strip().startswith('{') else None

            inspect = invoke('initial read-only inspection', ['inspect'])
            self.assertEqual(inspect['frontier'], ['t01'])
            flags = ['--ticket', 't01', '--owner', 'isolated-owner', '--run', 'isolated-run']
            claimed = invoke('claim in process one', ['claim', *flags])
            self.assertEqual(claimed['attempts'], 1)
            checkpoint = sandbox / 'checkpoint.json'
            checkpoint.write_text(json.dumps({'status': 'RUNNING', 'agent': 'isolated-native-id',
                'checkpoint': 'Persisted before process exit', 'next_action': 'Resume same ticket'}), encoding='utf-8')
            running = invoke('checkpoint in process two', ['checkpoint', *flags, '--data', str(checkpoint)])
            ticket = workspace / 'Tickets' / 't01.md'
            persisted = ticket.read_bytes()
            recovered = invoke('new process reconstructs persisted state', ['inspect'])
            self.assertEqual(recovered['tickets'][0]['checkpoint'], running)
            replay = invoke('new process idempotent claim', ['claim', *flags, '--agent', 'isolated-native-id'])
            self.assertEqual(replay, running)
            self.assertEqual(ticket.read_bytes(), persisted)
            self.assertEqual(ticket.read_text(encoding='utf-8').count('feature-supervisor:checkpoint '), 2)
            self.assertNotEqual(runs[1]['pid'], runs[2]['pid'])
            self.assertNotEqual(runs[2]['pid'], runs[3]['pid'])
            self.assertFalse(list(workspace.rglob('*.lock')))

            invoke('outside workspace claim blocked before write', ['claim', *flags], target=protected, expected=2)
            invoke('explicit outside file mutation blocked', [str(protected / 'erp-source.txt')],
                   expected=77, mode='probe')
            self.assertEqual(protected_before,
                {str(p): digest(p) for p in protected.rglob('*') if p.is_file()})
            self.assertEqual(before, {str(p): digest(p) for p in originals})
            self.assertEqual(digest(adapter), before[str(ADAPTER)])
            self.assertTrue(all(e['allowed'] for run in runs[:5] for e in run['events']))
            self.assertTrue(any(e['event'] == 'open' and e['allowed'] for run in runs[:5] for e in run['events']))
            self.assertTrue(all(any(not e['allowed'] for e in run['events']) for run in runs[5:]))
            self.assertTrue(all(not e['allowed'] for run in runs[5:] for e in run['events']
                                if any(str(protected) in p for p in e['paths'])))
            evidence = {'result': 'PASS', 'scope': 'Actual Python helper CLI and byte-identical copied native adapter',
                'sandbox': str(sandbox), 'source_hashes_before': before,
                'source_hashes_after': {str(p): digest(p) for p in originals},
                'protected_standins_before': protected_before,
                'protected_standins_after': {str(p): digest(p) for p in protected.rglob('*') if p.is_file()},
                'copied_adapter_sha256': digest(adapter), 'runs': runs,
                'restart': 'Separate child processes exited normally; persisted claim/checkpoint reread with no duplicate',
                'limits': ['No real ERP tickets or data were mutated or snapshotted',
                    'Audit hook covers observed Python filesystem mutations; not an OS security sandbox',
                    'No Codex App/chat closure, machine restart, forced crash or native agent restart was tested']}
        destination = ROOT / 'evidence' / 'isolation-audit.json'
        destination.parent.mkdir(exist_ok=True)
        destination.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    unittest.main()
