#!/usr/bin/env python3
"""Small local JSONL memory and Folder Status adapter for bug-resolver."""
import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path


def read_entries(index):
    if not index.exists():
        return
    with index.open(encoding="utf-8") as stream:
        for number, raw in enumerate(stream, 1):
            if not raw.strip():
                continue
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at line {number}: {exc}") from exc
            if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
                raise ValueError(f"JSONL line {number} must be an object with string id")
            yield entry


def search(index, terms, limit):
    needles = [term.casefold() for term in terms if term.strip()]
    capacity = min(limit, 3)
    if not needles or capacity < 1:
        return []
    ranked = []
    for position, entry in enumerate(read_entries(index) or ()):
        haystack = json.dumps(entry, ensure_ascii=False, sort_keys=True).casefold()
        score = sum(haystack.count(term) for term in needles)
        if score:
            candidate = (score, -position, entry)
            if len(ranked) < capacity:
                ranked.append(candidate)
            else:
                worst = min(range(len(ranked)), key=lambda i: (ranked[i][0], ranked[i][1]))
                if candidate[:2] > ranked[worst][:2]:
                    ranked[worst] = candidate
    ranked.sort(key=lambda row: (-row[0], -row[1]))
    return [entry for _, _, entry in ranked]


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def upsert(index, entry):
    if not isinstance(entry, dict) or not isinstance(entry.get("id"), str) or not entry["id"]:
        raise ValueError("entry must be a JSON object with a non-empty string id")
    entries = list(read_entries(index) or ())
    output = []
    inserted = False
    for current in entries:
        if current["id"] == entry["id"]:
            if not inserted:
                output.append(entry)
                inserted = True
        else:
            output.append(current)
    if not inserted:
        output.append(entry)
    atomic_write(index, "".join(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n" for item in output))


def supported_statuses(plugin_source):
    source = plugin_source.read_text(encoding="utf-8")
    match = re.search(r"const\s+STATUSES\s*=\s*\[([^\]]*)\]", source)
    if not match:
        raise ValueError("Cannot verify Folder Status allowlist in main.js")
    statuses = re.findall(r"['\"]([a-z][a-z0-9_-]*)['\"]", match.group(1))
    if not statuses:
        raise ValueError("Folder Status allowlist is empty or unsupported")
    return set(statuses)


def set_status(args):
    technical = {"production": "production", "completed": "implemented"}[args.status]
    statuses = supported_statuses(args.plugin_source)
    if technical not in statuses:
        raise ValueError(f"Plugin does not support required status: {technical}")
    if args.status == "completed":
        if not (args.root_cause_confirmed and args.tests_passed and args.regressions_passed and args.documentation_saved):
            raise ValueError("completed requires confirmed cause, passing tests/regressions, and saved documentation")
    data = json.loads(args.data.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("folders"), dict):
        raise ValueError("Unsupported Folder Status data schema")
    data["folders"][args.folder] = technical
    atomic_write(args.data, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"folder": args.folder, "status": technical, "semantic_status": args.status}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    query = sub.add_parser("search", help="Search index only; returns at most three matches")
    query.add_argument("--index", type=Path, required=True)
    query.add_argument("--term", action="append", default=[])
    query.add_argument("--limit", type=int, default=3)
    write = sub.add_parser("upsert", help="Append or replace one bug ID in JSONL")
    write.add_argument("--index", type=Path, required=True)
    write.add_argument("--entry", type=Path, required=True, help="JSON file containing one object")
    status = sub.add_parser("set-status", help="Safely update existing Folder Status plugin data")
    status.add_argument("--plugin-source", type=Path, required=True)
    status.add_argument("--data", type=Path, required=True)
    status.add_argument("--folder", required=True)
    status.add_argument("--status", choices=("production", "completed"), required=True)
    for flag in ("root-cause-confirmed", "tests-passed", "regressions-passed", "documentation-saved"):
        status.add_argument(f"--{flag}", action="store_true", dest=flag.replace("-", "_"))
    args = parser.parse_args()
    try:
        if args.command == "search":
            print("\n".join(json.dumps(item, ensure_ascii=False, separators=(",", ":")) for item in search(args.index, args.term, args.limit)))
        elif args.command == "upsert":
            upsert(args.index, json.loads(args.entry.read_text(encoding="utf-8")))
        else:
            set_status(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
