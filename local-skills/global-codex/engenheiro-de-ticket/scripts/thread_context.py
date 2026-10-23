"""Read only the latest recorded model/cwd for one local Codex task."""
import argparse
import json
import ntpath
import os
from pathlib import Path
import uuid


def resolve(thread_id, root):
    thread_id = str(uuid.UUID(thread_id))
    matches = list((root / "sessions").rglob(f"*{thread_id}.jsonl"))
    if len(matches) != 1:
        raise ValueError("Expected exactly one session recording for this task")
    latest = None
    with matches[0].open(encoding="utf-8") as source:
        for line in source:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue  # A concurrent writer may not have finished the last line.
            if record.get("type") == "turn_context":
                latest = record.get("payload", {})
    if not latest or not latest.get("model") or not latest.get("cwd"):
        raise ValueError("Latest turn has no verifiable model/cwd")
    return {"threadId": thread_id, "model": latest["model"],
            "thinking": latest.get("effort"), "cwd": latest["cwd"],
            "turnId": latest.get("turn_id"), "source": str(matches[0])}


def resolve_current(root, runtime_thread_id, cwd, requested_id=None):
    if not runtime_thread_id:
        raise ValueError("Current task identity CODEX_THREAD_ID is unavailable")
    current = str(uuid.UUID(runtime_thread_id))
    if requested_id and str(uuid.UUID(requested_id)) != current:
        raise ValueError("Requested task differs from current task CODEX_THREAD_ID")
    result = resolve(current, root)
    def normalize(value):
        return ntpath.normcase(ntpath.normpath(str(value).removeprefix('\\\\?\\')))
    if normalize(result['cwd']) != normalize(cwd):
        raise ValueError("Recorded cwd differs from current working directory")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("thread_id", nargs="?")
    parser.add_argument("--inspect", action="store_true",
                        help="Read another task for diagnostics only, never for dispatch")
    args = parser.parse_args()
    root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    if args.inspect:
        if not args.thread_id:
            parser.error("--inspect requires a task ID")
        result = resolve(args.thread_id, root)
        result['inspectionOnly'] = True
    else:
        result = resolve_current(root, os.environ.get("CODEX_THREAD_ID"),
                                 Path.cwd(), args.thread_id)
    print(json.dumps(result, ensure_ascii=False))
