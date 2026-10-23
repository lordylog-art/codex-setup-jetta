"""Uma trava de integração por repositório, compartilhada por todas as worktrees."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import uuid


class LockError(RuntimeError):
    pass


def git(base, *args):
    return subprocess.check_output(
        ['rtk', 'proxy', 'git', '-C', str(base), *args],
        encoding='utf-8', errors='strict', stderr=subprocess.PIPE,
    ).strip()


class IntegrationLock:
    def __init__(self, base, owner):
        if not owner:
            raise LockError('CODEX_THREAD_ID ausente; não invente identidade.')
        self.base = Path(git(base, 'rev-parse', '--show-toplevel')).resolve()
        common = Path(git(self.base, 'rev-parse', '--git-common-dir'))
        if not common.is_absolute():
            common = self.base / common
        self.directory = common.resolve() / 'ticket-dispatch'
        self.directory.mkdir(exist_ok=True)
        self.path = self.directory / 'integration.lock'
        self.owner = owner

    def read(self):
        try:
            data = json.loads(self.path.read_text(encoding='utf-8'))
            if data.get('version') != 1 or not data.get('token') or not data.get('owner'):
                raise ValueError('registro inválido')
            return data
        except (OSError, ValueError, AttributeError) as exc:
            raise LockError('Trava ausente, legada ou inválida; reconciliar com o dono.') from exc

    def clean(self):
        if git(self.base, 'status', '--porcelain'):
            raise LockError('Base com alterações; preserve a trava e resolva com o dono.')
        for name in ('CHERRY_PICK_HEAD', 'MERGE_HEAD', 'REVERT_HEAD', 'rebase-merge', 'rebase-apply', 'sequencer'):
            path = Path(git(self.base, 'rev-parse', '--git-path', name))
            if not path.is_absolute():
                path = self.base / path
            if path.exists():
                raise LockError('Operação Git pendente: ' + name)

    def check(self, token):
        data = self.read()
        if data['owner'] != self.owner or data['token'] != token or Path(data['base']).resolve() != self.base:
            raise LockError('Trava pertence a outra tarefa, base ou sessão.')
        return data

    def acquire(self):
        token = uuid.uuid4().hex
        data = dict(version=1, owner=self.owner, token=token, base=str(self.base))
        try:
            with self.path.open('x', encoding='utf-8') as stream:
                json.dump(data, stream, ensure_ascii=False)
        except FileExistsError as exc:
            raise LockError('Base reservada; consulte status e coordene com o dono.') from exc
        try:
            legacy = [p.name for p in self.directory.glob('integration*.lock') if p != self.path]
            if legacy:
                raise LockError('Travas legadas presentes: ' + ', '.join(legacy))
            self.clean()
        except Exception:
            self.check(token)
            self.path.unlink()
            raise
        return data

    def release(self, token):
        self.check(token)
        self.clean()
        self.check(token)
        self.path.unlink()
        return {'released': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['acquire', 'check', 'release', 'status'])
    parser.add_argument('--base', required=True)
    parser.add_argument('--token')
    args = parser.parse_args()
    try:
        lock = IntegrationLock(args.base, os.environ.get('CODEX_THREAD_ID'))
        if args.action == 'acquire':
            result = lock.acquire()
        elif args.action == 'status':
            result = {k: v for k, v in lock.read().items() if k != 'token'}
        else:
            if not args.token:
                raise LockError('--token retornado por acquire é obrigatório.')
            result = getattr(lock, args.action)(args.token)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (LockError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
