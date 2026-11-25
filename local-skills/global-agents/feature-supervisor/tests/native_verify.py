"""Fixture-only independent acceptance check; never use this on product tickets."""
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
base = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('supervisor', base.parent / 'scripts/feature_supervisor.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)
workspace = base / 'evidence/native'
n = int(sys.argv[1])
assert n in (1, 2, 3)
name = f'T{n:02}'
artifact = workspace / f'artifacts/{name}.txt'
assert artifact.read_bytes() == f'{n}\n'.encode(), 'Incorrect candidate bytes'
result = json.loads((workspace / f'artifacts/{name}-result.json').read_text(encoding='utf-8-sig'))
assert result.get('result') == 'PASS' and result.get('exit_code') == 0
ticket = workspace / f'Tickets/{name}.md'
with s.sw._exclusive_lock(ticket):
    content = ticket.read_text(encoding='utf-8')
    content = content.replace(f'- [ ] artifacts/{name}.txt', f'- [x] artifacts/{name}.txt')
    ticket.write_text(content, encoding='utf-8')
proofs = [f'artifacts/{name}.txt', f'artifacts/{name}-result.json']
data = {'status': 'READY', 'checkpoint': 'Independent byte equality assertion passed',
        'next_action': 'Accept and inspect next ticket', 'evidence': proofs,
        'validators': [{'name': 'native_verify byte equality', 'status': 'PASS', 'evidence': proofs}],
        'supervisor_review': {'status': 'PASS', 'summary': 'Compared actual bytes to exact ticket criterion independently of executor report.', 'evidence': proofs}}
s.checkpoint(workspace, name, 'native-supervisor', 'native-20261102', data)
accepted = s.accept(workspace, name, 'native-supervisor', 'native-20261102')
snapshot = s.inspect(workspace)
report = {'accepted': accepted, 'after': snapshot}
(workspace / f'artifacts/{name}-accepted.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps({'ticket': name, 'result': 'PASS', 'frontier': snapshot['frontier']}))
