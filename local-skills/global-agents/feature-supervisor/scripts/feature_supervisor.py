#!/usr/bin/env python3
"""Small direct-mode adapter; canonical state and checkpoints remain in ticket Markdown."""
from __future__ import annotations

import argparse
from contextlib import contextmanager, ExitStack
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ADAPTER = Path('D:/newmove/.agents/skills/spec-workspace/scripts/spec_workspace.py')
sw = None
Error = ValueError


def load_adapter(path):
    global sw, Error
    require(Path(path).is_file(), f'Spec workspace adapter missing: {path}; pass --adapter PATH')
    spec = importlib.util.spec_from_file_location('spec_workspace', path)
    sw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sw)
    Error = sw.ResolutionError
MARKER = 'feature-supervisor:checkpoint '
STATUSES = {'CLAIMED', 'RUNNING', 'READY', 'RETRY', 'BLOCKED', 'ACCEPTED'}


def require(value, message):
    if not value:
        raise Error(message)


if ADAPTER.is_file():
    load_adapter(ADAPTER)


def feature(workspace):
    return str(Path(workspace).resolve())


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def field(frontmatter, name):
    matches = re.findall(r'^' + re.escape(name) + r':[ \t]*(.*)$', frontmatter, re.M)
    require(len(matches) == 1, f'Missing or duplicate {name}')
    return matches[0].strip().strip('\"\'')


def discover(workspace, reconcile=None):
    workspace = Path(workspace).resolve()
    index = workspace / 'Index.md'
    require(index.is_file(), 'Workspace needs an existing Index.md')
    content = index.read_text(encoding='utf-8')
    # The native adapter only follows extensionless workspace-relative wiki links.
    for link in re.findall(r'\[\[([^]]+)\]\]', content):
        if re.search(r'(?i)(?:^|[/\\])Tickets[/\\]', link):
            require(re.fullmatch(r'Tickets/[^/\\|#\[\]]+', link) and not link.endswith('.md'),
                    f'Unsupported ticket Index link: {link}')
            require((workspace / (link + '.md')).is_file(), f'Missing indexed ticket: {link}')
    require(not re.search(r'\]\([^\n)]*(?i:Tickets)[/\\]', content),
            'Markdown ticket links are unsupported; use [[Tickets/stem]]')
    tickets = sw._index_ticket_paths(workspace)
    require(tickets, 'Index has no supported tickets')
    require(set((workspace / 'Tickets').glob('*.md')) == set(tickets),
            'Missing or unindexed ticket; reconcile Index first')
    states = {}
    for path in tickets:
        require(path.resolve().parent == workspace / 'Tickets', 'Ticket escapes workspace')
        fm, _ = sw._frontmatter(path)
        require(field(fm, 'type') == 'ticket', f'Not a ticket: {path}')
        status = field(fm, 'ticket_status')
        require(status in {'open', 'claimed', 'resolved'}, f'Unsupported ticket status: {status}')
        role = field(fm, 'triage_role')
        require(role in {'needs-triage', 'needs-info', 'ready-for-agent', 'ready-for-human', 'wontfix'},
                f'Unsupported triage role: {role}')
        blockers = []
        matches = re.findall(r'^blocked_by:[ \t]*(.*)$', fm, re.M)
        require(len(matches) <= 1, 'Duplicate blocked_by')
        if matches:
            require(matches[0] in {'', '[]'}, 'Inline blocked_by is unsupported; use a wiki-link YAML list')
            block = re.search(r'^blocked_by:[ \t]*\n((?:[ \t]+.*(?:\n|$))*)', fm, re.M)
            if block:
                for line in block.group(1).splitlines():
                    match = re.fullmatch(r'\s+- [\"\']?\[\[Tickets/([^/|#\[\]]+)\]\][\"\']?\s*', line)
                    require(match, 'Unsupported blocked_by entry')
                    blockers.append(match.group(1).casefold())
        key = path.stem.casefold()
        require(key not in states, 'Duplicate ticket stem')
        block = re.findall(r'^block:[ \t]*(.*)$', fm, re.M)
        require(len(block) <= 1, 'Duplicate block')
        states[key] = {'path': path, 'status': status, 'blockers': blockers,
                       'block': block[0].strip().strip('\"\'') if block else None}
    for state in states.values():
        require(all(key in states for key in state['blockers']), 'Unknown dependency')
        if state['status'] == 'resolved' and reconcile is None:
            value = latest(state['path'])
            require(value and value['status'] == 'ACCEPTED',
                    'Resolved ticket lacks supervisor acceptance; historical proof needs explicit reconciliation')
            verify_evidence(workspace, state['path'], value)
    # Validate dependency syntax above before invoking the native frontier with its inline-list hole.
    ready = sw.frontier(workspace)
    return workspace, states, ready


def latest(path):
    values = re.findall(r'<!-- ' + re.escape(MARKER) + r'(.+?) -->', path.read_text(encoding='utf-8'))
    if not values:
        return None
    try:
        result = json.loads(values[-1])
        require(result['version'] == 1 and result['status'] in STATUSES, 'Unsupported checkpoint')
        require(isinstance(result['attempts'], int) and result['attempts'] >= 1, 'Invalid attempts')
        return result
    except (ValueError, KeyError, TypeError) as exc:
        raise Error('Malformed checkpoint; reconcile manually') from exc


def append(path, value):
    # JSON escaping prevents comment termination from user-supplied checkpoint text.
    encoded = json.dumps(value, ensure_ascii=True, separators=(',', ':')).replace('--', '\\u002d\\u002d')
    sw._append_comment(path, '<!-- ' + MARKER + encoded + ' -->')


def revision(path):
    fm, body = sw._frontmatter(path)
    fm = re.sub(r'^ticket_status:.*$', '', fm, flags=re.M)
    body = body.split('## Comments', 1)[0]
    return hashlib.sha256((fm.strip() + '\n' + body.strip()).encode()).hexdigest()


def ticket(states, name):
    key = name.removesuffix('.md').casefold()
    require(key in states, 'Ticket is not in Index')
    return states[key]['path']


def identity(value, owner, run):
    require(value and value.get('owner') == owner and value.get('run') == run, 'Claim owner/run mismatch')


@contextmanager
def workspace_write_lock(workspace):
    # Native writers lock tickets without the Index: protect dependency reads too.
    with sw._exclusive_lock(workspace / 'Index.md'):
        with ExitStack() as locks:
            for path in sorted(sw._index_ticket_paths(workspace)):
                require(path.resolve().parent == workspace / 'Tickets', 'Ticket escapes workspace')
                locks.enter_context(sw._exclusive_lock(path))
            yield


def inspect(workspace):
    workspace, states, ready = discover(workspace)
    return {'workspace': str(workspace), 'feature': feature(workspace), 'mode': 'direct', 'frontier': [p.stem for p in ready],
            'tickets': [{'ticket': p.stem, 'block': state['block'], 'dependencies': state['blockers'],
                         'ticket_status': state['status'], 'checkpoint': latest(p)}
                        for state in sorted(states.values(), key=lambda s: s['path'].name.casefold())
                        for p in [state['path']]]}


def claim(workspace, owner, run, agent='pending-dispatch', name=None, max_attempts=2):
    require(all(isinstance(v, str) and v.strip() for v in (owner, run, agent)), 'Owner, run and agent are required')
    require(type(max_attempts) is int and 1 <= max_attempts <= 10, 'max_attempts must be 1..10')
    workspace = Path(workspace).resolve()
    require((workspace / 'Index.md').is_file(), 'Index is missing')
    with workspace_write_lock(workspace):
        _, states, ready = discover(workspace)
        if name:
            path = ticket(states, name)
            previous = latest(path)
            if states[path.stem.casefold()]['status'] == 'claimed':
                identity(previous, owner, run)
                require(previous['agent'] == agent, 'Agent mismatch')
                return previous
            require(path in ready, 'Ticket is outside dependency frontier')
        else:
            require(ready, 'No ticket available in frontier')
            path = ready[0]
        require(latest(path) is None, 'Open ticket has prior checkpoint; reconcile manually')
        value = {'version': 1, 'ticket': path.stem, 'owner': owner, 'run': run, 'agent': agent,
                 'feature': feature(workspace), 'block': states[path.stem.casefold()]['block'],
                 'dependencies': states[path.stem.casefold()]['blockers'], 'timestamp': timestamp(),
                 'attempts': 1, 'max_attempts': max_attempts, 'status': 'CLAIMED',
                 'evidence': [], 'validators': [], 'supervisor_review': None,
                 'checkpoint': 'Claimed', 'next_action': 'Execute ticket', 'ticket_revision': revision(path)}
        sw._transition_ticket(path, 'claimed')
        append(path, value)
        return value


def evidence_paths(workspace, paths):
    require(isinstance(paths, list), 'Evidence must be a list of workspace-relative files')
    result = []
    for name in paths:
        require(isinstance(name, str) and name, 'Invalid evidence path')
        path = (workspace / name).resolve()
        require(sw.inside(path, workspace) and path.is_file(), f'Missing or outside evidence: {name}')
        result.append({'path': path.relative_to(workspace).as_posix(),
                       'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    return result


def verify_evidence(workspace, path, value):
    require(value['ticket_revision'] == revision(path), 'Ticket changed since checkpoint; evidence is stale')
    require(value['evidence'], 'Actual evidence files required')
    require(value['validators'] and all(v['status'] == 'PASS' for v in value['validators']), 'PASS validators required')
    require(value['supervisor_review'] and value['supervisor_review']['status'] == 'PASS', 'Semantic supervisor PASS review required')
    for entry in value['evidence']:
        current = evidence_paths(workspace, [entry['path']])[0]
        require(current == entry, f'Stale evidence: {entry["path"]}')


def checked_criteria(path):
    _, body = sw._frontmatter(path)
    section = re.search(r'^## (?:Acceptance Criteria|Critérios de aceite)\s*\n(.*?)(?=^## |\Z)', body, re.M | re.S | re.I)
    require(section, 'Explicit Acceptance Criteria section required')
    checks = re.findall(r'^\s*(?:[-+*]|\d+[.)]) \[([ xX])\] .+', section.group(1), re.M)
    require(checks and all(c.lower() == 'x' for c in checks), 'Acceptance criteria remain unchecked')


def proof_bundle(value):
    evidence = {e['path'] for e in value['evidence']}
    for validator in value['validators']:
        require(isinstance(validator, dict) and set(validator) == {'name', 'status', 'evidence'}, 'Invalid validator')
        require(isinstance(validator['name'], str) and validator['name'].strip(), 'Validator name required')
        require(validator['status'] in {'PASS', 'FAIL', 'BLOCKED'}, 'Invalid validator status')
        require(isinstance(validator['evidence'], list) and validator['evidence'] and
                all(isinstance(p, str) and p in evidence for p in validator['evidence']), 'Validator needs recorded evidence')
    review = value['supervisor_review']
    if review is not None:
        require(isinstance(review, dict) and set(review) == {'status', 'summary', 'evidence'}, 'Invalid supervisor review')
        require(review['status'] in {'PASS', 'FAIL', 'BLOCKED'} and isinstance(review['summary'], str)
                and review['summary'].strip(), 'Semantic supervisor review required')
        require(isinstance(review['evidence'], list) and review['evidence'] and
                all(isinstance(p, str) and p in evidence for p in review['evidence']), 'Review needs recorded evidence')


def checkpoint(workspace, name, owner, run, data):
    workspace = Path(workspace).resolve()
    require((workspace / 'Index.md').is_file(), 'Index is missing')
    with workspace_write_lock(workspace):
        _, states, _ = discover(workspace)
        path = ticket(states, name)
        require(states[path.stem.casefold()]['status'] == 'claimed', 'Ticket is not claimed')
        prior = latest(path)
        identity(prior, owner, run)
        require(prior['status'] != 'BLOCKED', 'Blocked ticket requires human reconciliation; no automatic retry')
        allowed = {'status', 'checkpoint', 'next_action', 'evidence', 'validators', 'supervisor_review', 'agent'}
        require(isinstance(data, dict) and set(data) <= allowed, 'Unknown checkpoint fields')
        require(data.get('status') in {'RUNNING', 'READY', 'RETRY', 'BLOCKED'}, 'Invalid update status')
        if 'agent' in data:
            require(data['status'] == 'RUNNING' and isinstance(data['agent'], str) and data['agent'].strip(),
                    'Agent identity can only be updated with RUNNING')
        if data['status'] == 'READY':
            require({'evidence', 'validators', 'supervisor_review'} <= set(data), 'READY needs fresh evidence, validators and review')
        require(all(isinstance(data.get(k), str) and data[k].strip() for k in ('checkpoint', 'next_action')),
                'Checkpoint and next_action are required')
        value = dict(prior)
        value.update(data)
        if data['status'] == 'RETRY':
            # Exact replay does not consume another attempt, including after restart.
            if prior['status'] == 'RETRY' and all(prior.get(k) == v for k, v in data.items() if k not in {'evidence'}):
                return prior
            if prior['attempts'] >= prior['max_attempts']:
                value['status'] = 'BLOCKED'
                value['next_action'] = 'Human reconciliation required: retry budget exhausted'
            else:
                value['attempts'] += 1
        if 'evidence' in data:
            value['evidence'] = evidence_paths(workspace, data['evidence'])
        proof_bundle(value)
        value['ticket_revision'] = revision(path)
        if value == prior:
            return prior
        value['timestamp'] = timestamp()
        append(path, value)
        return value


def accept(workspace, name, owner, run):
    workspace = Path(workspace).resolve()
    require((workspace / 'Index.md').is_file(), 'Index is missing')
    with workspace_write_lock(workspace):
        _, states, _ = discover(workspace)
        path = ticket(states, name)
        value = latest(path)
        identity(value, owner, run)
        require(all(states[key]['status'] == 'resolved' for key in states[path.stem.casefold()]['blockers']),
                'Ticket dependencies are not resolved with current accepted evidence')
        if states[path.stem.casefold()]['status'] == 'resolved' and value['status'] == 'ACCEPTED':
            return value
        require(states[path.stem.casefold()]['status'] == 'claimed' and value['status'] == 'READY', 'Ticket is not READY')
        verify_evidence(workspace, path, value)
        checked_criteria(path)
        require(value['validators'] and all(v['status'] == 'PASS' for v in value['validators']), 'PASS validators required')
        require(value['supervisor_review'] and value['supervisor_review']['status'] == 'PASS', 'Semantic supervisor PASS review required')
        value = {**value, 'status': 'ACCEPTED', 'timestamp': timestamp(), 'next_action': 'Select next dependency frontier ticket'}
        sw._transition_ticket(path, 'resolved')
        append(path, value)
        return value


def adopt(workspace, name, owner, run, data, agent='supervisor-reconciliation'):
    """Explicitly verify resolved history, never reopen or automatically import it."""
    require(all(isinstance(v, str) and v.strip() for v in (owner, run, agent)), 'Owner, run and agent required')
    require(isinstance(data, dict) and set(data) == {'status', 'checkpoint', 'next_action', 'evidence', 'validators', 'supervisor_review'}
            and data['status'] == 'READY', 'Adoption requires a complete READY proof bundle')
    require(all(isinstance(data[k], str) and data[k].strip() for k in ('checkpoint', 'next_action')),
            'Checkpoint and next_action are required')
    workspace = Path(workspace).resolve()
    require((workspace / 'Index.md').is_file(), 'Index is missing')
    with workspace_write_lock(workspace):
        _, states, _ = discover(workspace, reconcile=name.removesuffix('.md').casefold())
        path = ticket(states, name)
        state = states[path.stem.casefold()]
        require(state['status'] == 'resolved', 'Only already-resolved tickets may be adopted')

        def current_dependencies(key, visiting):
            require(key not in visiting, 'Dependency cycle requires reconciliation')
            for blocker in states[key]['blockers']:
                dependency = states[blocker]
                proof = latest(dependency['path'])
                require(dependency['status'] == 'resolved' and proof and proof['status'] == 'ACCEPTED',
                        'Dependencies are not currently accepted; adopt predecessors first')
                verify_evidence(workspace, dependency['path'], proof)
                current_dependencies(blocker, visiting | {key})

        current_dependencies(path.stem.casefold(), set())
        prior = latest(path)
        if prior:
            identity(prior, owner, run)
            require(prior['status'] in {'READY', 'ACCEPTED'}, 'Existing checkpoint is not READY or ACCEPTED')
            verify_evidence(workspace, path, prior)
        value = dict(prior) if prior else {
            'version': 1, 'ticket': path.stem, 'owner': owner, 'run': run, 'agent': agent,
            'feature': feature(workspace), 'block': state['block'], 'dependencies': state['blockers'],
            'attempts': 1, 'max_attempts': 2, 'timestamp': timestamp(), 'ticket_revision': revision(path)}
        value.update(data)
        value['evidence'] = evidence_paths(workspace, data['evidence'])
        value['status'] = 'ACCEPTED'
        proof_bundle(value)
        verify_evidence(workspace, path, value)
        checked_criteria(path)
        if prior:
            # Recovery can certify the same READY candidate; changed proof is a new decision.
            expected = {**prior, 'status': 'ACCEPTED'}
            require(value == expected, 'Adoption replay differs from existing proof/checkpoint')
            if prior['status'] == 'ACCEPTED':
                return prior
        value['timestamp'] = timestamp()
        append(path, value)
        return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True, type=Path)
    parser.add_argument('--adapter', type=Path, default=ADAPTER)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('inspect')
    for command in ('claim', 'checkpoint', 'accept', 'adopt'):
        p = sub.add_parser(command)
        p.add_argument('--ticket', required=command != 'claim')
        p.add_argument('--owner', required=True)
        p.add_argument('--run', required=True)
        if command == 'claim':
            p.add_argument('--agent', default='pending-dispatch')
            p.add_argument('--max-attempts', type=int, default=2)
        if command == 'adopt':
            p.add_argument('--agent', default='supervisor-reconciliation')
        if command in {'checkpoint', 'adopt'}:
            p.add_argument('--data', required=True, type=Path)
    args = parser.parse_args()
    try:
        load_adapter(args.adapter)
        if args.command == 'inspect':
            result = inspect(args.workspace)
        elif args.command == 'claim':
            result = claim(args.workspace, args.owner, args.run, args.agent, args.ticket, args.max_attempts)
        elif args.command == 'checkpoint':
            result = checkpoint(args.workspace, args.ticket, args.owner, args.run, json.loads(args.data.read_text(encoding='utf-8')))
        elif args.command == 'adopt':
            result = adopt(args.workspace, args.ticket, args.owner, args.run, json.loads(args.data.read_text(encoding='utf-8')), args.agent)
        else:
            result = accept(args.workspace, args.ticket, args.owner, args.run)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (Error, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc), 'recoverable': True}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
