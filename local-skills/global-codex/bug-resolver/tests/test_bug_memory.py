import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "bug-memory.py"
SPEC = importlib.util.spec_from_file_location("bug_memory", SCRIPT)
bug_memory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bug_memory)


class BugMemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.index = self.root / "Bugs" / "_index" / "bugs.jsonl"
        self.plugin = self.root / ".obsidian" / "plugins" / "folder-status" / "main.js"
        self.data = self.root / ".obsidian" / "plugins" / "folder-status" / "data.json"
        self.plugin.parent.mkdir(parents=True)
        self.plugin.write_text('const STATUSES = ["pending", "production", "implemented"];', encoding="utf-8")
        self.data.write_text('{"version":1,"folders":{"Bugs/other":"pending"}}', encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def set_status(self, status, **evidence):
        args = type("Args", (), {
            "status": status, "plugin_source": self.plugin, "data": self.data,
            "folder": "Bugs/BUG-1", "root_cause_confirmed": False,
            "tests_passed": False, "regressions_passed": False,
            "documentation_saved": False,
        })()
        for key, value in evidence.items():
            setattr(args, key, value)
        bug_memory.set_status(args)

    def test_empty_index_returns_no_candidates_and_ignores_sibling_notes(self):
        note = self.root / "Bugs" / "BUG-old" / "RESOLUCAO.md"
        note.parent.mkdir(parents=True)
        note.write_text("sync overlap", encoding="utf-8")
        self.assertEqual([], bug_memory.search(self.index, ["sync overlap"], 3))
        self.assertFalse(self.index.exists())

    def test_search_returns_only_relevant_candidates_and_caps_at_three(self):
        entries = [
            {"id": f"BUG-{n}", "symptoms": ["polling stopped" if n < 5 else "unrelated"]}
            for n in range(1, 7)
        ]
        self.index.parent.mkdir(parents=True)
        self.index.write_text("".join(json.dumps(e) + "\n" for e in entries), encoding="utf-8")
        found = bug_memory.search(self.index, ["polling stopped"], 99)
        self.assertEqual(["BUG-1", "BUG-2", "BUG-3"], [e["id"] for e in found])
        self.assertEqual([], bug_memory.search(self.index, ["database deadlock"], 3))

    def test_upsert_replaces_existing_id_without_duplicate_or_reordering_others(self):
        self.index.parent.mkdir(parents=True)
        self.index.write_text('{"id":"A","v":1}\n{"id":"B"}\n{"id":"A","v":2}\n', encoding="utf-8")
        bug_memory.upsert(self.index, {"id": "A", "v": 3})
        rows = list(bug_memory.read_entries(self.index))
        self.assertEqual([{"id": "A", "v": 3}, {"id": "B"}], rows)

    def test_upsert_adds_new_id_as_one_valid_jsonl_line(self):
        bug_memory.upsert(self.index, {"id": "BUG-1", "status": "completed"})
        self.assertEqual([{"id": "BUG-1", "status": "completed"}], list(bug_memory.read_entries(self.index)))

    def test_failed_tests_cannot_set_final_status(self):
        before = self.data.read_text(encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "requires confirmed cause"):
            self.set_status("completed", root_cause_confirmed=True, tests_passed=False,
                            regressions_passed=True, documentation_saved=True)
        self.assertEqual(before, self.data.read_text(encoding="utf-8"))

    def test_final_status_maps_to_plugin_supported_implemented(self):
        self.set_status("completed", root_cause_confirmed=True, tests_passed=True,
                        regressions_passed=True, documentation_saved=True)
        data = json.loads(self.data.read_text(encoding="utf-8"))
        self.assertEqual("implemented", data["folders"]["Bugs/BUG-1"])
        self.assertEqual("pending", data["folders"]["Bugs/other"])

    def test_start_status_uses_existing_production_value(self):
        self.set_status("production")
        data = json.loads(self.data.read_text(encoding="utf-8"))
        self.assertEqual("production", data["folders"]["Bugs/BUG-1"])

    def test_unsupported_status_fails_without_mutating_plugin_data(self):
        before = self.data.read_text(encoding="utf-8")
        self.plugin.write_text('const STATUSES = ["pending", "production"];', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "does not support"):
            self.set_status("completed", root_cause_confirmed=True, tests_passed=True,
                            regressions_passed=True, documentation_saved=True)
        self.assertEqual(before, self.data.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
