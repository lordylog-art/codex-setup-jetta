import concurrent.futures
from pathlib import Path
import subprocess
import tempfile
import unittest

from integration_lock import IntegrationLock, LockError


class IntegrationLockTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name) / 'base'
        self.base.mkdir()
        self.git('init')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '--allow-empty', '-m', 'base')
        self.other = Path(self.temp.name) / 'other'
        self.git('worktree', 'add', '--detach', str(self.other))

    def git(self, *args):
        return subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(self.base), *args], encoding='utf-8', stderr=subprocess.PIPE)

    def test_competing_worktrees_have_exactly_one_owner(self):
        def acquire(pair):
            base, owner = pair
            lock = IntegrationLock(base, owner)
            try:
                return lock, lock.acquire()
            except LockError:
                return None
        with concurrent.futures.ThreadPoolExecutor() as pool:
            results = list(pool.map(acquire, [(self.base, 'one'), (self.other, 'two')]))
        winners = [x for x in results if x]
        self.assertEqual(len(winners), 1)
        lock, data = winners[0]
        lock.release(data['token'])

    def test_foreign_owner_and_wrong_token_cannot_release(self):
        lock = IntegrationLock(self.base, 'one')
        data = lock.acquire()
        with self.assertRaises(LockError):
            IntegrationLock(self.base, 'two').release(data['token'])
        with self.assertRaises(LockError):
            lock.release('wrong')
        self.assertTrue(lock.path.exists())
        lock.release(data['token'])

    def test_dirty_base_keeps_lock(self):
        lock = IntegrationLock(self.base, 'one')
        data = lock.acquire()
        (self.base / 'change.txt').write_text('ação', encoding='utf-8')
        with self.assertRaises(LockError):
            lock.release(data['token'])
        self.assertTrue(lock.path.exists())

    def test_legacy_lock_blocks_new_owner(self):
        lock = IntegrationLock(self.base, 'one')
        legacy = lock.directory / 'integration-28.lock'
        legacy.write_text('', encoding='utf-8')
        with self.assertRaises(LockError):
            lock.acquire()
        self.assertTrue(legacy.exists())
        self.assertFalse(lock.path.exists())

    def test_git_operation_blocks_release_even_without_diff(self):
        lock = IntegrationLock(self.base, 'one')
        data = lock.acquire()
        (self.base / '.git' / 'CHERRY_PICK_HEAD').write_text(self.git('rev-parse', 'HEAD').strip() + '\n', encoding='utf-8')
        with self.assertRaises(LockError):
            lock.release(data['token'])
        self.assertTrue(lock.path.exists())

    def test_empty_canonical_lock_is_not_stolen(self):
        lock = IntegrationLock(self.base, 'one')
        lock.path.write_text('', encoding='utf-8')
        with self.assertRaises(LockError):
            lock.acquire()
        with self.assertRaises(LockError):
            lock.release('anything')
        self.assertTrue(lock.path.exists())


if __name__ == '__main__':
    unittest.main()
