import copy
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest

from delivery_evidence import qualify
from test_delivery_snapshot import make_repo


def good_report(root, started_after):
    started = datetime.fromisoformat(started_after) + timedelta(seconds=1)
    return {"status": "PASS", "project": str(root), "runId": "run-1",
            "configHash": "config-hash", "sourceFingerprint": "source-hash",
            "startedAt": started.isoformat(), "finishedAt": (started + timedelta(seconds=1)).isoformat(),
            "sourceChanged": False, "unregistered": [],
            "results": [{"id": "delivery", "status": "PASS", "passed": 3,
                         "failed": 0, "skipped": 0, "todo": 0, "flaky": 0,
                         "members": 1, "memberPaths": ["a.txt"], "reporter": "jest"}]}


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        make_repo(self.root)
        self.cutoff = datetime.now(timezone.utc).isoformat()
        self.report = good_report(self.root, self.cutoff)

    def test_valid_pass_and_optional_zero_counts(self):
        summary = qualify(self.report, self.root, ["delivery"], self.cutoff)
        self.assertEqual(summary[0]["passed"], 3)
        self.report.pop("sourceChanged")
        self.report["results"][0].pop("skipped")
        self.assertEqual(qualify(self.report, self.root, ["delivery"], self.cutoff), summary)

    def test_report_failures_and_incomplete_provenance(self):
        mutations = {"status": "FAIL", "project": str(self.root.parent), "runId": "",
                     "configHash": None, "sourceFingerprint": " ", "sourceChanged": True,
                     "unregistered": ["orphan.py"], "results": [],
                     "startedAt": "2000-01-01T00:00:00Z", "finishedAt": "2020-01-01",
                     "startedAt_naive": "2020-01-01T00:00:00"}
        for key, value in mutations.items():
            report = copy.deepcopy(self.report)
            report["startedAt" if key == "startedAt_naive" else key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                qualify(report, self.root, ["delivery"], self.cutoff)

    def test_missing_and_duplicate_suites(self):
        with self.assertRaises(ValueError):
            qualify(self.report, self.root, ["other"], self.cutoff)
        self.report["results"].append(copy.deepcopy(self.report["results"][0]))
        with self.assertRaises(ValueError):
            qualify(self.report, self.root, ["delivery"], self.cutoff)

    def test_all_results_and_counts_must_pass(self):
        mutations = [("status", "FAIL"), ("passed", True), ("passed", 0), ("passed", "3"),
                     ("failed", 1), ("skipped", 1), ("todo", 1), ("flaky", 1),
                     ("failed", False), ("reporter", "unknown"), ("reporter", []),
                     ("members", True), ("members", 2), ("memberPaths", ["a.txt", "a.txt"])]
        for key, value in mutations:
            report = copy.deepcopy(self.report)
            report["results"][0][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                qualify(report, self.root, ["delivery"], self.cutoff)
        extra = copy.deepcopy(self.report["results"][0])
        extra.update(id="extra", status="FAIL")
        self.report["results"].append(extra)
        with self.assertRaises(ValueError):
            qualify(self.report, self.root, ["delivery"], self.cutoff)

    def test_member_paths_must_be_existing_relative_files(self):
        for path in ("../a.txt", "/a.txt", "C:/a.txt", "child/../a.txt", "missing", ".", "a\\b", None):
            report = copy.deepcopy(self.report)
            report["results"][0]["memberPaths"] = [path]
            with self.subTest(path=path), self.assertRaises(ValueError):
                qualify(report, self.root, ["delivery"], self.cutoff)

    def test_required_ids_are_distinct_and_typed(self):
        for required in ([], ["delivery", "delivery"], [True], "delivery"):
            with self.subTest(required=required), self.assertRaises(ValueError):
                qualify(self.report, self.root, required, self.cutoff)


if __name__ == "__main__":
    unittest.main()
