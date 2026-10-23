"""Local deterministic workflow ledger. No daemon, dependencies, or product mutation."""
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import uuid

STAGES = ['PLANNED', 'IN_PROGRESS', 'CODE_READY', 'REVIEW_READY', 'REVIEWED', 'INTEGRATION_READY', 'ACCEPTED']
DEPENDENCIES = {'contract': 'CODE_READY', 'implementation': 'CODE_READY', 'review': 'REVIEWED', 'integration': 'ACCEPTED', 'validation': 'REVIEWED'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


@contextlib.contextmanager
def lock(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        if stream.tell() == 0:
            stream.write(b'0')
            stream.flush()
        stream.seek(0)
        if os.name == 'nt':
            import msvcrt
            deadline = time.monotonic() + 10
            while True:
                try:
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    require(time.monotonic() < deadline, 'lock unavailable after 10 seconds; operation aborted')
                    time.sleep(.025)
        else:
            import fcntl
            deadline = time.monotonic() + 10
            while True:
                try:
                    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    require(time.monotonic() < deadline, 'lock unavailable after 10 seconds; operation aborted')
                    time.sleep(.025)
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == 'nt':
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.write-')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class Controller:
    def __init__(self, plan, root, state_root=None, resources_root=None):
        self.root = Path(root).resolve()
        self.plan_path = Path(plan).resolve()
        self.plan = json.loads(self.plan_path.read_text(encoding='utf-8-sig'))
        self.validate()
        self.tickets = {t['id']: t for t in self.plan['tickets']}
        self.hash = digest(canonical(self.plan))
        self.directory = Path(state_root).resolve() if state_root else self.root / '.local' / 'orchestration' / self.plan['feature']
        self.path = self.directory / 'state.json'
        self.resources = Path(resources_root).resolve() if resources_root else Path.home() / '.codex' / 'orchestration' / 'resources'

    def validate(self):
        p = self.plan
        require(p.get('version') == 2, 'plan version must be 2')
        require(re.fullmatch(r'[A-Za-z0-9_-]+', p.get('feature', '')), 'invalid feature identifier')
        require(p.get('spec') and p.get('tickets') and p.get('criteria'), 'spec, tickets and criteria required')
        require(isinstance(p.get('shared_contracts'), list) and all(isinstance(ref, str) and ref.strip() for ref in p['shared_contracts']), 'shared_contracts must be a list of nonempty references; empty list allowed')
        ids = [t['id'] for t in p['tickets']]
        require(len(ids) == len(set(ids)), 'duplicate tickets')
        by_id = {t['id']: t for t in p['tickets']}
        graph = {i: [] for i in ids}
        for t in p['tickets']:
            require(t.get('ticket') and t.get('author') and t.get('scope'), 'ticket reference, author and scope required')
            maturity = t.get('maturity')
            require(isinstance(maturity, dict), 'maturity object required')
            require(isinstance(maturity.get('expected'), str) and maturity['expected'].strip(), 'maturity.expected must be nonblank')
            require(isinstance(maturity.get('incomplete'), list), 'maturity.incomplete must be a list of future criterion pointers')
            require(all(isinstance(maturity.get(flag), bool) for flag in ('functional_review', 'final_qa')), 'maturity functional_review and final_qa must be booleans')
            gates = t.get('gates', [])
            require(gates and len({g['id'] for g in gates}) == len(gates), 'unique gates required')
            for g in gates:
                require(g.get('stage') in STAGES[2:], 'invalid gate stage')
                require(isinstance(g.get('required'), bool), 'gate required must be boolean')
                require(g.get('scope') and g.get('artifacts'), 'gate scope and proof IDs required')
                require('final_qa' not in g or isinstance(g['final_qa'], bool), 'gate final_qa must be boolean')
                if g.get('kind') == 'review':
                    require(STAGES.index(g['stage']) >= STAGES.index('REVIEWED'), 'functional review gates must be REVIEWED or later')
                if g.get('kind') == 'integration':
                    require(STAGES.index(g['stage']) >= STAGES.index('INTEGRATION_READY'), 'integration gates must be INTEGRATION_READY or later')
                    require(isinstance(t.get('integration_owner'), str) and t['integration_owner'].strip(), 'integration gates require a named integration_owner')
            for d in t.get('dependencies', []):
                require(d.get('ticket') in by_id and d['ticket'] != t['id'], 'unknown/self dependency')
                require(d.get('type') in DEPENDENCIES, 'unknown dependency type')
                require(d.get('source_stage', DEPENDENCIES[d['type']]) in STAGES, 'invalid dependency source stage')
                require(d.get('target_stage', self.target(d)) in STAGES, 'invalid dependency target stage')
                require(d.get('condition', 'stage_reached') == 'stage_reached', 'unsupported dependency condition')
                if d.get('gate'):
                    require(d['gate'] in {g['id'] for g in by_id[d['ticket']]['gates']}, 'unknown dependency gate')
                graph[t['id']].append(d['ticket'])
            require(t.get('estimate_minutes') is None or isinstance(t['estimate_minutes'], (int, float)) and t['estimate_minutes'] > 0, 'estimate must be positive or null')
        capacity = p.get('capacity', {'implementation': 1, 'validation': 1})
        require(all(isinstance(capacity.get(k), int) and not isinstance(capacity[k], bool) and capacity[k] > 0 for k in ('implementation', 'validation')), 'positive implementation/validation capacities required')
        visiting, seen = set(), set()
        def visit(i):
            require(i not in visiting, 'dependency cycle')
            if i in seen:
                return
            visiting.add(i)
            for dep in graph[i]:
                visit(dep)
            visiting.remove(i)
            seen.add(i)
        for i in ids:
            visit(i)
        criteria_ids = set()
        for c in p['criteria']:
            require(c['id'] not in criteria_ids, 'duplicate criterion')
            criteria_ids.add(c['id'])
            require(c.get('ticket') in by_id, 'criterion unknown ticket')
            gate = next((g for g in by_id[c['ticket']]['gates'] if g['id'] == c.get('gate')), None)
            require(gate and gate['required'] and c['id'] in gate.get('criteria', []), 'mandatory criterion must map to required gate')
        by_criterion = {c['id']: c for c in p['criteria']}
        for t in p['tickets']:
            for future in t['maturity']['incomplete']:
                require(isinstance(future, dict), 'future obligation must be a criterion/ticket/gate pointer')
                criterion = by_criterion.get(future.get('criterion'))
                require(criterion and future.get('ticket') == criterion['ticket'] and future.get('gate') == criterion['gate'], 'future obligation must reference its declared mandatory criterion ticket and gate')
        require(any(g['required'] and g.get('kind') == 'integration' and g['stage'] == 'ACCEPTED' and g.get('final_qa', True) and any(c['ticket'] == t['id'] and c['gate'] == g['id'] for c in p['criteria']) for t in p['tickets'] for g in t['gates']), 'feature requires a mandatory final integrated acceptance gate mapped to a criterion')

    @staticmethod
    def target(dep):
        return 'CODE_READY' if dep['type'] in ('contract', 'implementation') else 'INTEGRATION_READY'

    def event(self, state, action, **data):
        state['history'].append({'sequence': len(state['history']) + 1, 'at': time.time(), 'action': action, **data})

    def load(self):
        require(self.path.exists(), 'initialize first')
        state = json.loads(self.path.read_text(encoding='utf-8'))
        require(state['plan_hash'] == self.hash, 'plan changed; explicit migration required')
        require(state['root'] == str(self.root), 'state belongs to another worktree')
        return state

    def file(self, path):
        p = Path(path)
        return p.resolve() if p.is_absolute() else (self.root / p).resolve()

    def fingerprint(self, paths):
        result = {}
        for path in paths:
            p = self.file(path)
            require(p.is_file(), 'missing fingerprint file: ' + str(p))
            result[str(p)] = digest(p.read_bytes())
        require(result, 'fingerprint inputs required')
        return result

    def valid(self, evidence):
        return evidence.get('status') == 'PASS' and not evidence.get('invalidated') and all(Path(p).is_file() and digest(Path(p).read_bytes()) == h for p, h in evidence['fingerprints'].items())

    def gate_pass(self, state, ticket, gate):
        evidence = state['tickets'][ticket]['evidence'].get(gate['id'], {})
        return all(a in evidence and self.valid(evidence[a]) for a in gate['artifacts'])

    def prerequisites(self, state, ticket, destination):
        for d in self.tickets[ticket].get('dependencies', []):
            if STAGES.index(destination) < STAGES.index(d.get('target_stage', self.target(d))):
                continue
            other = state['tickets'][d['ticket']]
            require(other['stage'] != 'BLOCKED' and STAGES.index(other['stage']) >= STAGES.index(d.get('source_stage', DEPENDENCIES[d['type']])), 'dependency pending: ' + d['ticket'])
            self.ready(state, d['ticket'], d.get('source_stage', DEPENDENCIES[d['type']]))
            if d.get('gate'):
                gate = next(g for g in self.tickets[d['ticket']]['gates'] if g['id'] == d['gate'])
                require(self.gate_pass(state, d['ticket'], gate), 'dependency proof stale or missing')

    def ready(self, state, ticket, destination):
        self.prerequisites(state, ticket, destination)
        definition = self.tickets[ticket]
        if STAGES.index(destination) >= STAGES.index('REVIEW_READY'):
            require(definition.get('maturity', {}).get('functional_review') is True, 'increment is not declared mature for functional review')
        if destination == 'ACCEPTED':
            require(not any(f['status'] == 'open' for f in state['tickets'][ticket]['findings'].values()), 'unresolved findings')
        for gate in definition['gates']:
            if gate['required'] and STAGES.index(gate['stage']) <= STAGES.index(destination):
                require(self.gate_pass(state, ticket, gate), 'required evidence missing/stale: ' + gate['id'])

    def execute(self, command, **args):
        with lock(self.directory / 'state.lock'):
            if command == 'init':
                if self.path.exists():
                    state = self.load()
                    self.save_checkpoint(state)
                    return state
                state = {'version': 2, 'owner': str(uuid.uuid4()), 'root': str(self.root), 'plan_hash': self.hash, 'closed': False, 'tickets': {i: {'stage': 'PLANNED', 'evidence': {}, 'attempts': [], 'findings': {}} for i in self.tickets}, 'history': []}
                self.event(state, 'init')
                self.persist(state)
                return state
            state = self.load()
            if command == 'checkpoint':
                return self.save_checkpoint(state)
            if command == 'status':
                self.save_checkpoint(state)
                snapshot = json.loads(json.dumps(state))
                for i, r in snapshot['tickets'].items():
                    r['gate_validity'] = {g['id']: self.gate_pass(state, i, g) for g in self.tickets[i]['gates']}
                    r['acceptance_current'] = False
                    if r['stage'] == 'ACCEPTED':
                        try:
                            self.ready(state, i, 'ACCEPTED')
                            r['acceptance_current'] = True
                        except ValueError as error:
                            r['acceptance_invalid_reason'] = str(error)
                return snapshot
            if command == 'schedule':
                return self.schedule(state)
            if command == 'context-end':
                if not state.get('context_operation') and any(e['action'] == 'context-end' and e.get('operation_id') == args['operation_id'] for e in state['history']):
                    return state
                require(state.get('context_operation') == args['operation_id'], 'context operation mismatch')
                state.pop('context_operation')
                self.event(state, command, **args)
                self.persist(state)
                return state
            if command == 'context-begin':
                require(args.get('operation_id'), 'context operation id required')
                if state.get('context_operation') == args['operation_id']:
                    return state
                require(not state.get('context_operation'), 'context operation already pending')
                require(not any(r['stage'] in ('IN_PROGRESS', 'REVIEW_READY', 'INTEGRATION_READY') for r in state['tickets'].values()), 'critical ticket stage active')
                with lock(self.resources / 'resources.lock'):
                    ledger = self.resource_ledger()
                    require(not any(r['owner'] == state['owner'] for r in ledger['leases'].values()), 'resources still reserved')
                    state['context_operation'] = args['operation_id']
                    self.event(state, command, **args)
                    self.persist(state, ledger)
                return state
            require(not state.get('context_operation'), 'compaction pending; reconcile native completion before mutation')
            require(not state['closed'] or command == 'release', 'execution closed')
            ticket = args.get('ticket')
            if ticket:
                require(ticket in self.tickets, 'unknown ticket')
            record = state['tickets'].get(ticket)
            if command == 'transition':
                destination = args['to']
                require(record['stage'] in STAGES and destination in STAGES and STAGES.index(destination) == STAGES.index(record['stage']) + 1, 'invalid transition')
                self.ready(state, ticket, destination)
                record['stage'] = destination
            elif command == 'evidence':
                require(args.get('result') in ('PASS', 'FAIL'), 'explicit evidence result PASS or FAIL required')
                gate = next((g for g in self.tickets[ticket]['gates'] if g['id'] == args['gate']), None)
                require(gate, 'unknown gate')
                require(args['proof'] in gate['artifacts'], 'undeclared proof ID')
                require(args.get('actor'), 'evidence actor required')
                if gate.get('independent'):
                    require(args['actor'] != self.tickets[ticket]['author'], 'independent reviewer must differ from author')
                if gate.get('kind') == 'review':
                    require(record['stage'] in STAGES and STAGES.index(record['stage']) >= STAGES.index('REVIEW_READY'), 'functional review evidence requires mature increment')
                if gate.get('kind') == 'integration':
                    require(args['actor'] == self.tickets[ticket]['integration_owner'], 'integration evidence actor must be the declared integration_owner')
                    require(record['stage'] in STAGES and STAGES.index(record['stage']) >= STAGES.index('REVIEWED'), 'integration evidence requires integration readiness: completed review')
                    if gate.get('final_qa', gate['stage'] == 'ACCEPTED'):
                        require(self.tickets[ticket].get('maturity', {}).get('final_qa') is True, 'final QA maturity is not declared')
                    self.prerequisites(state, ticket, 'INTEGRATION_READY')
                for category in ('code', 'config', 'env'):
                    require(args.get(category), category + ' fingerprints required')
                fingerprints = self.fingerprint(args['code'] + args['config'] + args['env'] + [args['artifact']])
                # Evidence scope must cover the declared files; semantic proof quality remains the reviewer's decision.
                require(all(str(self.file(p)) in fingerprints for p in gate['scope']), 'evidence omits gate scope')
                record['evidence'].setdefault(gate['id'], {})[args['proof']] = {'status': args['result'], 'actor': args['actor'], 'fingerprints': fingerprints, 'scope': gate['scope'], 'artifact': str(self.file(args['artifact']))}
            elif command == 'change':
                require(args.get('paths'), 'changed paths required')
                if args['kind'] == 'security':
                    require(any(g['required'] and g.get('kind') == 'security' for g in self.tickets[ticket]['gates']), 'security change requires a mandatory security gate; revise plan explicitly')
                affected = set(str(self.file(p)) for p in args['paths'])
                invalid = []
                for gate in self.tickets[ticket]['gates']:
                    broad = args['kind'] == 'structural' or args['kind'] == 'security' and gate.get('kind') in ('security', 'review', 'integration')
                    for evidence in record['evidence'].get(gate['id'], {}).values():
                        if broad or affected.intersection(evidence['fingerprints']):
                            evidence['invalidated'] = args['kind']
                            invalid.append(gate['stage'])
                if args['kind'] in ('structural', 'security') and not invalid:
                    invalid = [g['stage'] for g in self.tickets[ticket]['gates'] if g['required']]
                if invalid:
                    earliest = min(STAGES.index(s) for s in invalid)
                    current = record.get('previous_stage') if record['stage'] == 'BLOCKED' else record['stage']
                    rewind = STAGES[min(STAGES.index(current), max(1, earliest - 1))]
                    if record['stage'] == 'BLOCKED':
                        record['previous_stage'] = rewind
                    else:
                        record['stage'] = rewind
                args['invalidated_stages'] = sorted(set(invalid))
            elif command == 'block':
                require(record['stage'] != 'BLOCKED' and args.get('reason'), 'block needs reason and unblocked state')
                record.update(previous_stage=record['stage'], stage='BLOCKED', reason=args['reason'])
            elif command == 'resume':
                require(record['stage'] == 'BLOCKED', 'ticket is not blocked')
                record['stage'] = record.pop('previous_stage')
                record.pop('reason')
            elif command in ('reserve', 'release'):
                return self.lease(state, command, args)
            elif command == 'attempt':
                require(args.get('failure'), 'failure signature required')
                progress = self.fingerprint([args['progress']]) if args.get('progress') else None
                previous = next((a for a in reversed(record['attempts']) if a['failure'] == args['failure']), None)
                if previous:
                    require(args.get('hypothesis') and args['hypothesis'] != previous.get('hypothesis') or args.get('information') and args['information'] != previous.get('information') or progress and progress != previous.get('progress'), 'stagnation: provide a new discriminating hypothesis or information')
                record['attempts'].append({**{k: args.get(k) for k in ('failure', 'hypothesis', 'information')}, 'progress': progress})
            elif command == 'finding':
                require(args.get('evidence'), 'finding evidence required')
                proof = self.fingerprint([args['evidence']])
                previous = record['findings'].get(args['id'])
                require(not previous or previous['status'] != 'resolved' or args['status'] != 'open' or previous['fingerprint'] != proof, 'resolved finding cannot reopen without new evidence')
                record['findings'][args['id']] = {'status': args['status'], 'fingerprint': proof}
            elif command == 'close':
                for i, r in state['tickets'].items():
                    require(r['stage'] == 'ACCEPTED', 'ticket not accepted: ' + i)
                    self.ready(state, i, 'ACCEPTED')
                with lock(self.resources / 'resources.lock'):
                    ledger = self.resource_ledger()
                    require(not any(r['owner'] == state['owner'] for r in ledger['leases'].values()), 'release exclusive resources before close')
                state['closed'] = True
            else:
                raise ValueError('unknown command')
            self.event(state, command, **args)
            self.persist(state)
            return state

    def persist(self, state, resources=None):
        atomic(self.path, state)
        self.save_checkpoint(state, resources)

    def save_checkpoint(self, state, resources=None):
        from continuity import checkpoint
        if resources is not None:
            return checkpoint(self, state, resources)
        with lock(self.resources / 'resources.lock'):
            return checkpoint(self, state, self.resource_ledger())

    def resource_ledger(self):
        path = self.resources / 'resources.json'
        return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'leases': {}, 'history': []}

    def lease(self, state, command, args):
        resource = args['resource']
        require(resource in self.tickets[args['ticket']].get('resources', []), 'resource not declared for ticket')
        with lock(self.resources / 'resources.lock'):
            ledger = self.resource_ledger()
            current = ledger['leases'].get(resource)
            if command == 'reserve':
                require(state['tickets'][args['ticket']]['stage'] != 'BLOCKED', 'blocked ticket cannot reserve resource')
                require(not current or current['owner'] != state['owner'] or current['ticket'] != args['ticket'], 'duplicate reservation: original operation owns this resource; reserve is not idempotent')
                if current and (current['owner'] != state['owner'] or current['ticket'] != args['ticket']):
                    r = state['tickets'][args['ticket']]
                    r.update(previous_stage=r['stage'], stage='BLOCKED', reason='resource unavailable: ' + resource)
                    self.event(state, 'resource_blocked', resource=resource, owner=current['owner'], ticket=args['ticket'])
                    self.persist(state, ledger)
                    raise ValueError('resource unavailable; ticket BLOCKED')
                ledger['leases'][resource] = {'owner': state['owner'], 'root': str(self.root), 'ticket': args['ticket'], 'since': time.time()}
            else:
                require(current, 'resource is not reserved')
                require(current['owner'] == state['owner'] and current['ticket'] == args['ticket'] or args.get('confirm_owner') == current['owner'], 'lease owner mismatch; manual release requires exact confirmed owner UUID')
                del ledger['leases'][resource]
            ledger['history'].append({'at': time.time(), 'command': command, 'resource': resource, 'actor_owner': state['owner'], 'previous': current})
            atomic(self.resources / 'resources.json', ledger)
            self.event(state, command, **args)
            self.persist(state, ledger)
            return ledger

    def schedule(self, state):
        lengths = {}
        with lock(self.resources / 'resources.lock'):
            reservations = self.resource_ledger()['leases']
        successors = {i: [] for i in self.tickets}
        for i, t in self.tickets.items():
            for d in t.get('dependencies', []):
                successors[d['ticket']].append(i)
        def remaining(i):
            if i in lengths:
                return lengths[i]
            stage = state['tickets'][i]['stage']
            estimate = self.tickets[i].get('estimate_minutes') if stage == 'PLANNED' else 0 if stage == 'ACCEPTED' else None
            tail = [remaining(s) for s in successors[i]]
            lengths[i] = None if estimate is None or any(x is None for x in tail) else estimate + max(tail, default=0)
            return lengths[i]
        result = []
        for i, r in state['tickets'].items():
            if r['stage'] == 'ACCEPTED':
                continue
            next_stage = STAGES[STAGES.index(r['stage']) + 1] if r['stage'] in STAGES[:-1] else None
            eligible, reason = False, r.get('reason')
            if next_stage:
                try:
                    self.ready(state, i, next_stage)
                    eligible = True
                except ValueError as error:
                    reason = str(error)
            resources = self.tickets[i].get('resources', [])
            available = all(name not in reservations or reservations[name]['owner'] == state['owner'] and reservations[name]['ticket'] == i for name in resources)
            result.append({'ticket': i, 'stage': r['stage'], 'next': next_stage, 'eligible': eligible, 'reason': reason, 'resources': resources, 'resources_available': available, 'critical_path_estimate_minutes': remaining(i), 'estimate_kind': 'estimate' if remaining(i) is not None else 'unknown'})
        result.sort(key=lambda x: (not x['eligible'], x['critical_path_estimate_minutes'] is None, -(x['critical_path_estimate_minutes'] or 0), x['ticket']))
        capacity = self.plan.get('capacity', {'implementation': 1, 'validation': 1})
        active = [i for i, r in state['tickets'].items() if r['stage'] == 'IN_PROGRESS']
        free = {'implementation': max(0, capacity['implementation'] - len(active)), 'validation': max(0, capacity['validation'] - sum(r['stage'] in ('REVIEW_READY', 'INTEGRATION_READY') for r in state['tickets'].values()))}
        dispatch, used = [], set()
        for item in result:
            lane = 'implementation' if item['next'] == 'IN_PROGRESS' else 'validation'
            if item['eligible'] and item['resources_available'] and free[lane] > 0 and not used.intersection(item['resources']):
                dispatch.append(item['ticket'])
                used.update(item['resources'])
                free[lane] -= 1
        return {'queue': result, 'suggested_dispatch': dispatch, 'capacity_advisory': capacity, 'active': active, 'waiting': [i for i, r in state['tickets'].items() if r['stage'] == 'BLOCKED'], 'parallelism_policy': 'conservative until expected benefit exceeds measured coordination overhead'}


def status_view(state, path, after=0, limit=10):
    """Bounded CLI status; state, gate evaluation and evidence files are unchanged."""
    require(type(after) is int and 0<=after<=len(state['history']), 'invalid event cursor')
    require(type(limit) is int and 1<=limit<=100, '1 <= limit <= 100 required')
    fields=('stage','previous_stage','reason','gate_validity','acceptance_current','acceptance_invalid_reason','findings')
    page=state['history'][after:after+limit]
    return {'closed':state['closed'],'state_path':str(Path(path).resolve()),
            'tickets':{k:{x:v[x] for x in fields if x in v} for k,v in state['tickets'].items()},
            'cursor':len(state['history']),'next_cursor':after+len(page),
            'has_more':after+len(page)<len(state['history']),'events':page,
            'detail':'Full evidence/fingerprints/attempts remain in state; status without --summary returns the complete view.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', required=True)
    parser.add_argument('--root', required=True)
    parser.add_argument('--state-root')
    parser.add_argument('--resources-root')
    sub = parser.add_subparsers(dest='command', required=True)
    for cmd in ('init', 'status', 'schedule', 'close', 'checkpoint', 'recover'):
        p = sub.add_parser(cmd)
        if cmd == 'status':
            p.add_argument('--summary', action='store_true')
            p.add_argument('--limit', type=int, default=10)
            p.add_argument('--after', type=int, default=0)
    for cmd in ('context-begin', 'context-end'):
        p = sub.add_parser(cmd)
        p.add_argument('--operation-id', required=True)
    for cmd in ('transition', 'evidence', 'change', 'block', 'resume', 'reserve', 'release', 'attempt', 'finding'):
        p = sub.add_parser(cmd)
        p.add_argument('--ticket', required=True)
        if cmd == 'transition':
            p.add_argument('--to', choices=STAGES, required=True)
        elif cmd == 'evidence':
            for option in ('gate', 'proof', 'artifact', 'actor'):
                p.add_argument('--' + option, required=True)
            for option in ('code', 'config', 'env'):
                p.add_argument('--' + option, nargs='+', required=True)
            p.add_argument('--result', choices=['PASS', 'FAIL'], required=True)
        elif cmd == 'change':
            p.add_argument('--kind', choices=['focused', 'structural', 'security'], required=True)
            p.add_argument('--paths', nargs='+', required=True)
        elif cmd == 'block':
            p.add_argument('--reason', required=True)
        elif cmd in ('reserve', 'release'):
            p.add_argument('--resource', required=True)
            if cmd == 'release':
                p.add_argument('--confirm-owner')
        elif cmd == 'attempt':
            p.add_argument('--failure', required=True)
            p.add_argument('--hypothesis')
            p.add_argument('--information')
            p.add_argument('--progress')
        elif cmd == 'finding':
            p.add_argument('--id', required=True)
            p.add_argument('--evidence', required=True)
            p.add_argument('--status', choices=['open', 'resolved'], required=True)
    a = vars(parser.parse_args())
    command = a.pop('command')
    c = Controller(**{k: a.pop(k) for k in ('plan', 'root', 'state_root', 'resources_root')})
    if command == 'recover':
        from continuity import recover
        result = recover(c)
    elif command == 'status':
        result = c.execute(command)
        require(a['after'] >= 0, 'event cursor must be nonnegative')
        if a['summary']:
            result = status_view(result, c.path, a['after'], a['limit'])
    else:
        result = c.execute(command, **a)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
