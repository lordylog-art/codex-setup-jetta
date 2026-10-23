import json
from pathlib import Path
import tempfile
import unittest

from thread_context import resolve_current

SELF = '01a0a561-7a95-74d1-ba06-22166c81205f'
PARENT = '01a0a52c-a9dc-71b2-b61b-13ad60944104'


class CurrentContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'sessions').mkdir()
        for ident, model, cwd in [(SELF, 'gpt-5.6-terra', 'C:\\worktree'),
                                  (PARENT, 'gpt-6-astra', 'C:\\main')]:
            record = {'type': 'turn_context', 'payload': {
                'model': model, 'effort': 'medium', 'cwd': cwd}}
            (self.root / 'sessions' / f'rollout-{ident}.jsonl').write_text(
                json.dumps(record), encoding='utf-8')

    def test_inherits_executor_not_parent(self):
        result = resolve_current(self.root, SELF, 'C:\\worktree')
        self.assertEqual(result['model'], 'gpt-5.6-terra')
        self.assertEqual(result['thinking'], 'medium')
        self.assertEqual(result['threadId'], SELF)

    def test_rejects_foreign_id(self):
        with self.assertRaisesRegex(ValueError, 'task'):
            resolve_current(self.root, SELF, 'C:\\worktree', PARENT)

    def test_rejects_wrong_worktree(self):
        with self.assertRaisesRegex(ValueError, 'cwd'):
            resolve_current(self.root, SELF, 'C:\\main')

    def test_rejects_missing_identity(self):
        with self.assertRaises(ValueError):
            resolve_current(self.root, None, 'C:\\worktree', SELF)


if __name__ == '__main__':
    unittest.main()
