"""Capture, seal and check local delivery evidence. Acceptance stays manual."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from delivery_evidence import qualify
from delivery_snapshot import capture, changed, project_root


PACKET_KEYS = {"version", "status", "snapshot", "report", "required", "summary"}
REPORT_KEYS = {"path", "sha256"}


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("invalid JSON constant")


def read_json(path):
    raw = Path(path).read_bytes()
    try:
        value = json.loads(raw, object_pairs_hook=_object, parse_constant=_invalid_constant)
    except (ValueError, UnicodeError):
        raise ValueError("invalid JSON document") from None
    return value, hashlib.sha256(raw).hexdigest()


def require_current(root, snapshot):
    if changed(root, snapshot):
        raise ValueError("candidate files changed")


def write_new(root, output, value):
    output = Path(output).absolute()
    resolved = output.resolve()
    if resolved.is_relative_to(root):
        relative = resolved.relative_to(root).as_posix()
        if not relative.startswith(".local/"):
            raise ValueError("project output must be in ignored .local")
        ignored = subprocess.run(["git", "-C", str(root), "check-ignore", "--quiet", "--", relative],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tracked = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--", relative],
                                 check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ignored.returncode != 0 or tracked.stdout:
            raise ValueError("output must be outside the Git inventory")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=True, sort_keys=True)
        handle.write("\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("capture", "seal", "check"):
        sub = commands.add_parser(command)
        sub.add_argument("--project", required=True)
        if command in ("capture", "seal"):
            sub.add_argument("--out", required=True)
        if command == "seal":
            sub.add_argument("--candidate", required=True)
            sub.add_argument("--report", required=True)
            sub.add_argument("--suite", action="append", required=True)
        if command == "check":
            sub.add_argument("--packet", required=True)
    args = parser.parse_args(argv)
    try:
        root = project_root(args.project)
        if args.command == "capture":
            snapshot = capture(root)
            write_new(root, args.out, snapshot)
            require_current(root, snapshot)
            result = {"status": "CAPTURED"}
        elif args.command == "seal":
            snapshot, _ = read_json(args.candidate)
            require_current(root, snapshot)
            report, digest = read_json(args.report)
            summary = qualify(report, root, args.suite, snapshot["createdAt"])
            packet = {"version": 1, "status": "REVIEW_REQUIRED", "snapshot": snapshot,
                      "report": {"path": str(Path(args.report).resolve()), "sha256": digest},
                      "required": args.suite, "summary": summary}
            require_current(root, snapshot)
            write_new(root, args.out, packet)
            require_current(root, snapshot)
            result = {"status": "REVIEW_REQUIRED"}
        else:
            packet, _ = read_json(args.packet)
            if (not isinstance(packet, dict) or set(packet) != PACKET_KEYS
                    or type(packet.get("version")) is not int or packet["version"] != 1
                    or packet["status"] != "REVIEW_REQUIRED"):
                raise ValueError("invalid packet schema")
            origin = packet["report"]
            if (not isinstance(origin, dict) or set(origin) != REPORT_KEYS
                    or not isinstance(origin["path"], str) or not Path(origin["path"]).is_absolute()
                    or not isinstance(origin["sha256"], str) or len(origin["sha256"]) != 64
                    or any(char not in "0123456789abcdef" for char in origin["sha256"])):
                raise ValueError("invalid report origin")
            require_current(root, packet["snapshot"])
            report, digest = read_json(origin["path"])
            if digest != origin["sha256"]:
                raise ValueError("report content changed")
            summary = qualify(report, root, packet["required"], packet["snapshot"]["createdAt"])
            if json.dumps(packet["summary"], sort_keys=True) != json.dumps(summary, sort_keys=True):
                raise ValueError("packet summary mismatch")
            require_current(root, packet["snapshot"])
            result = {"status": "CURRENT", "acceptance": "MANUAL_REVIEW_REQUIRED"}
        print(json.dumps(result, separators=(",", ":")))
        return 0
    except ValueError as error:
        print(json.dumps({"status": "ERROR", "error": str(error)}, separators=(",", ":")))
        return 2
    except (OSError, RuntimeError, subprocess.SubprocessError, TypeError, KeyError):
        print('{"status":"ERROR","error":"cannot read, validate or write delivery files"}')
        return 2


if __name__ == "__main__":
    sys.exit(main())
