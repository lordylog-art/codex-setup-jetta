"""Disposable resume indexes over the V2 controller; never restore tracker state."""
import json
import os
from pathlib import Path
import subprocess

from controller import atomic, canonical, digest, require


def git_state(root):
    result = {}
    for key, args in [('head', ['rev-parse', 'HEAD']), ('branch', ['symbolic-ref', '--short', '-q', 'HEAD']),
                      ('status', ['status', '--porcelain=v1', '--untracked-files=normal'])]:
        try:
            p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True, encoding='utf-8', timeout=5)
            result[key] = p.stdout.strip() if p.returncode == 0 else None
        except (OSError, subprocess.TimeoutExpired):
            result[key] = None
    return result


def checkpoint(controller, state, resources):
    """Caller holds state.lock, then resources.lock. Immutable blob before latest pointer."""
    c = controller
    require(digest(canonical(json.loads(c.plan_path.read_text(encoding='utf-8-sig')))) == c.hash,
            'plan changed; explicit migration required')
    skill = Path(__file__).resolve().parent.parent
    rules = [c.root / 'AGENTS.md']
    rules += [skill / p for p in
              ('SKILL.md', 'references/planning-contract.md', 'references/quality-gates.md',
               'references/controller.md', 'references/continuity.md')]
    blob = {'version': 1, 'run_id': os.environ.get('CODEX_THREAD_ID') or state['owner'],
            'execution_id': state['owner'], 'feature': c.plan['feature'], 'closed': state['closed'],
            'sequence': len(state['history']), 'root': str(c.root), 'git': git_state(c.root),
            'sources': {'plan': {'path': str(c.plan_path), 'sha256': digest(c.plan_path.read_bytes()), 'contract_hash': c.hash},
                        'state': {'path': str(c.path), 'sha256': digest(c.path.read_bytes())},
                        'resources': str(c.resources / 'resources.json')},
            'spec': c.plan['spec'], 'contracts': c.plan['shared_contracts'], 'criteria': c.plan['criteria'],
            'rules': {str(p): digest(p.read_bytes()) for p in rules if p.is_file()},
            'history_ref': str(c.path) + '#/history',
            'tickets': {i: {'stage': r['stage'], 'reason': r.get('reason'),
                            'owner': c.tickets[i]['author'], 'integration_owner': c.tickets[i].get('integration_owner'),
                            'ticket_ref': c.tickets[i]['ticket'], 'dependencies': c.tickets[i].get('dependencies', []),
                            'evidence': {g: {p: {'artifact': e['artifact'], 'fingerprints': e['fingerprints'],
                                                 'valid': c.valid(e)} for p, e in proofs.items()}
                                         for g, proofs in r['evidence'].items()},
                            'details_ref': str(c.path) + '#/tickets/' + i} for i, r in state['tickets'].items()},
            'leases': {k: v for k, v in resources['leases'].items() if v['owner'] == state['owner']},
            'next_step': 'Reconcile controller status and schedule; retain only currently valid evidence.'}
    key = digest(canonical(blob))
    path = c.directory / 'checkpoints' / (key + '.json')
    if path.exists():
        require(digest(canonical(json.loads(path.read_text(encoding='utf-8')))) == key, 'checkpoint corrupt')
    else:
        atomic(path, blob)
    pointer = {'version': 1, 'path': str(path), 'sha256': key, 'execution_id': state['owner'], 'sequence': len(state['history'])}
    atomic(c.directory / 'checkpoints/latest.json', pointer)
    return pointer


def recover(c):
    # The controller recomputes validity against live files; the checkpoint grants no rights.
    state = c.execute('status')
    pointer = c.execute('checkpoint')
    blob = json.loads(Path(pointer['path']).read_text(encoding='utf-8'))
    require(digest(canonical(blob)) == pointer['sha256'], 'checkpoint corrupt')
    require(blob['execution_id'] == state['owner'], 'checkpoint execution mismatch')
    return {'checkpoint': {**pointer, 'valid': True}, 'state_path': str(c.path),
            'tickets': {i: {k: r[k] for k in ('stage', 'gate_validity', 'acceptance_current', 'acceptance_invalid_reason') if k in r}
                        for i, r in state['tickets'].items()},
            'accepted': [i for i, r in state['tickets'].items() if r['acceptance_current']],
            'remaining': [i for i, r in state['tickets'].items() if not r['acceptance_current']],
            'schedule': c.execute('schedule')}


