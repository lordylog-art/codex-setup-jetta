import copy
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from delivery_snapshot import capture, changed


def make_repo(root):
    subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
    (root / ".gitignore").write_text(".local/\n", encoding="utf-8")
    (root / "a.txt").write_text("initial\n", encoding="utf-8")
    (root / "b.bin").write_bytes(b"\x00\xff\x80")
    subprocess.run(["git", "-C", str(root), "add", ".gitignore", "a.txt", "b.bin"],
                   check=True, capture_output=True)


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        make_repo(self.root)

    def test_capture_binary_and_untracked_then_mutation_addition_deletion(self):
        (self.root / "config.json").write_text("{}", encoding="utf-8")
        candidate = capture(self.root)
        self.assertIn("b.bin", candidate["files"])
        self.assertIn("config.json", candidate["files"])
        self.assertEqual(changed(self.root, candidate), [])
        (self.root / "a.txt").write_text("changed", encoding="utf-8")
        (self.root / "new.txt").write_text("new", encoding="utf-8")
        (self.root / "b.bin").unlink()
        self.assertEqual(changed(self.root, candidate), ["a.txt", "b.bin", "new.txt"])
        with self.assertRaises(ValueError):
            capture(self.root)

    def test_ignored_outputs_do_not_change_identity(self):
        candidate = capture(self.root)
        (self.root / ".local").mkdir()
        (self.root / ".local" / "result.json").write_text("{}", encoding="utf-8")
        self.assertEqual(changed(self.root, candidate), [])

    def test_new_indexed_missing_dependency_changes_identity(self):
        candidate = capture(self.root)
        dependency = self.root / "new_dependency.py"
        dependency.write_text("value = 1\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "new_dependency.py"],
                       check=True, capture_output=True)
        dependency.unlink()
        self.assertEqual(changed(self.root, candidate), ["new_dependency.py"])
        with self.assertRaises(ValueError):
            capture(self.root)

    def test_subdirectory_and_non_repository_rejected(self):
        child = self.root / "child"
        child.mkdir()
        for root in (child, self.root / "missing", self.root / "a.txt"):
            with self.subTest(root=root), self.assertRaises(ValueError):
                capture(root)
        with tempfile.TemporaryDirectory() as other:
            with self.assertRaises(ValueError):
                capture(other)

    def test_snapshot_metadata_is_validated(self):
        original = capture(self.root)
        mutations = {"version": True, "project": "relative", "createdAt": "yesterday",
                     "environment": {}, "files": {"../escape": "0" * 64}}
        for key, value in mutations.items():
            candidate = copy.deepcopy(original)
            candidate[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                changed(self.root, candidate)

    def test_directory_replacing_file_rejected(self):
        candidate = capture(self.root)
        (self.root / "a.txt").unlink()
        (self.root / "a.txt").mkdir()
        with self.assertRaises(ValueError):
            changed(self.root, candidate)

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as external:
            target = Path(external) / "secret"
            target.write_text("outside", encoding="utf-8")
            try:
                (self.root / "escape").symlink_to(target)
            except OSError:
                if os.name != "nt":
                    raise
                subprocess.run(["cmd", "/d", "/c", "mklink", "/J",
                                str(self.root / "escape"), external],
                               check=True, capture_output=True)
            with self.assertRaises(ValueError):
                capture(self.root)


if __name__ == "__main__":
    unittest.main()
