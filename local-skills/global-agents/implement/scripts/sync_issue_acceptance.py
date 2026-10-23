#!/usr/bin/env python3
"""Check one GitHub Issue acceptance criterion and close the issue when complete."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")


HEADING = re.compile(r"^#{1,6}\s+acceptance criteria\s*$", re.IGNORECASE)
NEXT_HEADING = re.compile(r"^#{1,6}\s+")
CHECKBOX = re.compile(r"^(\s*[-*+]\s+\[)( |x|X)(\]\s+)(.*?)(\s*)$")


def run(command: list[str]) -> str:
    result = subprocess.run(command, text=True, encoding="utf-8", capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "gh command failed")
    return result.stdout


def normalize(value: str) -> str:
    return " ".join(value.split()).casefold()


def acceptance_checkboxes(body: str) -> list[tuple[int, re.Match[str]]]:
    lines = body.splitlines(keepends=True)
    start = next((index + 1 for index, line in enumerate(lines) if HEADING.match(line.strip())), None)
    if start is None:
        raise ValueError("Issue body has no 'Acceptance criteria' section.")

    entries: list[tuple[int, re.Match[str]]] = []
    for index in range(start, len(lines)):
        if NEXT_HEADING.match(lines[index].strip()):
            break
        match = CHECKBOX.match(lines[index].rstrip("\r\n"))
        if match:
            entries.append((index, match))
    if not entries:
        raise ValueError("Acceptance criteria contains no Markdown checkboxes.")
    return entries


def gh_issue_command(action: list[str], issue: str, repo: str | None) -> list[str]:
    command = ["gh", "issue", action[0], issue, *action[1:]]
    if repo:
        command.extend(["--repo", repo])
    return command


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("issue", help="GitHub issue number or URL")
    parser.add_argument("--criterion", required=True, help="Acceptance checkbox text, copied verbatim from the issue")
    parser.add_argument("--repo", help="Optional OWNER/REPO override")
    parser.add_argument("--apply", action="store_true", help="Write the checked box and close the completed issue")
    parser.add_argument("--close-when-complete", action="store_true", help="Close an open issue when every acceptance checkbox is checked")
    args = parser.parse_args()

    try:
        payload = json.loads(run(gh_issue_command(["view", "--json", "body,state,url"], args.issue, args.repo)))
        body = payload["body"]
        lines = body.splitlines(keepends=True)
        matches = acceptance_checkboxes(body)
        wanted = normalize(args.criterion)
        selected = [(index, match) for index, match in matches if normalize(match.group(4)) == wanted]
        if len(selected) != 1:
            raise ValueError("Criterion must match exactly one checkbox in Acceptance criteria.")

        index, match = selected[0]
        already_checked = match.group(2).casefold() == "x"
        if not already_checked:
            line_ending = "\r\n" if lines[index].endswith("\r\n") else "\n" if lines[index].endswith("\n") else ""
            lines[index] = f"{match.group(1)}x{match.group(3)}{match.group(4)}{match.group(5)}{line_ending}"
        updated_body = "".join(lines)
        all_checked = all(("x" if item_index == index else item_match.group(2)).casefold() == "x" for item_index, item_match in matches)

        checked = False
        if args.apply and not already_checked:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", delete=False, suffix=".md") as file:
                file.write(updated_body)
                body_path = Path(file.name)
            try:
                run(gh_issue_command(["edit", "--body-file", str(body_path)], args.issue, args.repo))
            finally:
                body_path.unlink(missing_ok=True)
            checked = True

        closed = False
        if args.apply and args.close_when_complete and all_checked and payload["state"].upper() != "CLOSED":
            run(gh_issue_command(["close", "--reason", "completed"], args.issue, args.repo))
            closed = True

        print(json.dumps({
            "issue": payload["url"],
            "criterion": match.group(4).strip(),
            "checked": checked,
            "already_checked": already_checked,
            "all_acceptance_criteria_checked": all_checked,
            "closed": closed,
            "dry_run": not args.apply,
        }, ensure_ascii=False))
        return 0
    except (RuntimeError, ValueError, json.JSONDecodeError, KeyError) as error:
        print(f"sync_issue_acceptance: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
