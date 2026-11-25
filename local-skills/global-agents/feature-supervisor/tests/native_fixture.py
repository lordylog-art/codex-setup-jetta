"""Create an isolated, persistent fixture for the native-agent integration protocol."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent / 'evidence' / 'native'

def setup():
    if ROOT.exists():
        raise SystemExit('Fixture already exists; preserve evidence and use a new explicitly named directory')
    (ROOT / 'Tickets').mkdir(parents=True)
    (ROOT / 'artifacts').mkdir()
    (ROOT / 'Index.md').write_text('# Synthetic feature\n\n## B01\n[[Tickets/T01]]\n[[Tickets/T02]]\n## B02\n[[Tickets/T03]]\n', encoding='utf-8')
    for n in range(1, 4):
        deps = '[]' if n == 1 else '\n  - "[[Tickets/T%02d]]"' % (n - 1)
        (ROOT / 'Tickets' / f'T{n:02}.md').write_text(
            f'---\ntype: ticket\ntriage_role: ready-for-agent\nticket_status: open\nblock: B0{1 if n < 3 else 2}\nblocked_by: {deps}\n---\n\n# T{n:02}\n\n'
            f'Deliver artifacts/T{n:02}.txt containing exactly ticket number {n} followed by newline. '
            'Executor writes only its artifact and result JSON, never tracker status.\n\n'
            f'## Acceptance Criteria\n- [ ] artifacts/T{n:02}.txt is exactly {n} followed by newline.\n', encoding='utf-8')
    print(ROOT)

def snapshot(name):
    paths = []
    repo = Path('D:/newmove')
    files = subprocess.check_output(['git', 'ls-files', '-c', '-o', '--exclude-standard', '--', 'apps', '.agents/skills/spec-workspace', 'AGENTS.md', '.super-qa.json'], cwd=repo, text=True).splitlines()
    paths.extend(repo / f for f in files)
    for root in [Path('C:/Users/caila/.agents/skills/smart-orchestrator'), Path('C:/Users/caila/.codex/plugins/cache/newmove-automation/smart-orchestrator/0.1.0/skills'), Path('D:/Obsidian/Obsidian/New move/Projetos/Templates interativos')]:
        paths.extend(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    result = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
    target = ROOT.parent / f'{name}.json'
    target.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({'snapshot': str(target), 'files': len(result)}))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        snapshot(sys.argv[1])
    else:
        setup()
