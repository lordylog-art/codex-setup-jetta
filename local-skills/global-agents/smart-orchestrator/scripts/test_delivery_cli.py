import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_delivery_evidence import good_report
from test_delivery_snapshot import make_repo


CLI = Path(__file__).with_name("delivery.py").resolve()


class DeliveryCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        make_repo(self.root)
        self.candidate = self.root / ".local" / "candidate.json"
        self.report = self.root / ".local" / "report.json"
        self.packet = self.root / ".local" / "packet.json"

    def run_cli(self, *args, expected=0):
        process = subprocess.run([sys.executable, "-B", str(CLI), *args,
                                  "--project", str(self.root)], capture_output=True, text=True)
        self.assertEqual(process.returncode, expected, process.stdout + process.stderr)
        self.assertNotIn("Traceback", process.stderr + process.stdout)
        return json.loads(process.stdout)

    def prepare(self):
        self.run_cli("capture", "--out", str(self.candidate))
        candidate = json.loads(self.candidate.read_text(encoding="utf-8"))
        report = good_report(self.root, candidate["createdAt"])
        self.report.write_text(json.dumps(report), encoding="utf-8")
        return report

    def seal(self, expected=0):
        return self.run_cli("seal", "--candidate", str(self.candidate), "--report", str(self.report),
                            "--suite", "delivery", "--out", str(self.packet), expected=expected)

    def test_real_cli_happy_path_keeps_manual_acceptance(self):
        self.prepare()
        self.assertEqual(self.seal()["status"], "REVIEW_REQUIRED")
        result = self.run_cli("check", "--packet", str(self.packet))
        self.assertEqual(result, {"status": "CURRENT", "acceptance": "MANUAL_REVIEW_REQUIRED"})

    def test_report_drift_and_missing_report(self):
        self.prepare()
        self.seal()
        original = self.report.read_bytes()
        self.report.write_bytes(original + b" ")
        self.run_cli("check", "--packet", str(self.packet), expected=2)
        self.report.unlink()
        self.run_cli("check", "--packet", str(self.packet), expected=2)

    def test_source_drift_on_seal_and_check(self):
        self.prepare()
        self.seal()
        (self.root / "a.txt").write_text("drift", encoding="utf-8")
        self.run_cli("check", "--packet", str(self.packet), expected=2)
        self.packet.unlink()
        self.seal(expected=2)
        self.assertFalse(self.packet.exists())

    def test_old_evidence_rejected(self):
        report = self.prepare()
        report["startedAt"] = "2000-01-01T00:00:00Z"
        self.report.write_text(json.dumps(report), encoding="utf-8")
        self.seal(expected=2)
        self.assertFalse(self.packet.exists())

    def test_new_indexed_missing_dependency_rejects_check_and_seal(self):
        self.prepare()
        self.seal()
        dependency = self.root / "new_dependency.py"
        dependency.write_text("value = 1\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "new_dependency.py"],
                       check=True, capture_output=True)
        dependency.unlink()
        with self.subTest(command="check"):
            result = self.run_cli("check", "--packet", str(self.packet), expected=2)
            self.assertEqual(result["status"], "ERROR")
        self.packet.unlink()
        with self.subTest(command="seal"):
            self.assertEqual(self.seal(expected=2)["status"], "ERROR")
            self.assertFalse(self.packet.exists())

    def test_outputs_are_exclusive_and_cannot_change_inventory(self):
        self.prepare()
        saved = self.candidate.read_bytes()
        self.run_cli("capture", "--out", str(self.candidate), expected=2)
        self.assertEqual(self.candidate.read_bytes(), saved)
        self.run_cli("capture", "--out", str(self.root / "output.json"), expected=2)
        self.assertFalse((self.root / "output.json").exists())
        self.seal()
        saved_packet = self.packet.read_bytes()
        self.seal(expected=2)
        self.assertEqual(self.packet.read_bytes(), saved_packet)

    def test_outside_output_allowed_but_not_when_local_is_unignored(self):
        with tempfile.TemporaryDirectory() as outside:
            self.run_cli("capture", "--out", str(Path(outside) / "nested" / "candidate.json"))
        (self.root / ".gitignore").write_text("", encoding="utf-8")
        self.run_cli("capture", "--out", str(self.candidate), expected=2)
        self.assertFalse(self.candidate.exists())

    def test_malformed_packet_and_candidate_fail_closed(self):
        self.prepare()
        self.seal()
        original = json.loads(self.packet.read_text(encoding="utf-8"))
        for packet in (None, {}, {**original, "version": True}, {**original, "summary": []}):
            self.packet.write_text(json.dumps(packet), encoding="utf-8")
            self.run_cli("check", "--packet", str(self.packet), expected=2)
        self.candidate.write_text('{"version":1,"version":1}', encoding="utf-8")
        self.seal(expected=2)

    def test_summary_types_cannot_be_substituted(self):
        report = self.prepare()
        report["results"][0]["passed"] = 1
        self.report.write_text(json.dumps(report), encoding="utf-8")
        self.seal()
        packet = json.loads(self.packet.read_text(encoding="utf-8"))
        packet["summary"][0]["passed"] = True
        self.packet.write_text(json.dumps(packet), encoding="utf-8")
        self.run_cli("check", "--packet", str(self.packet), expected=2)


if __name__ == "__main__":
    unittest.main()
