"""Validate declared Super QA provenance and counts, not authenticity."""

from pathlib import Path

from delivery_snapshot import safe_file, timestamp


REPORTERS = {"tap", "jest", "vitest", "playwright"}


def qualify(report, root, required, started_after):
    try:
        return _qualify(report, root, required, started_after)
    except (OSError, RuntimeError, TypeError):
        raise ValueError("invalid report or project files") from None


def _qualify(report, root, required, started_after):
    if (not isinstance(required, list) or not required
            or any(not isinstance(item, str) or not item.strip() for item in required)
            or len(set(required)) != len(required)):
        raise ValueError("required suites must be distinct nonempty IDs")
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("invalid project root")
    cutoff = timestamp(started_after)
    if cutoff.utcoffset().total_seconds() != 0:
        raise ValueError("capture timestamp must be UTC")
    if not isinstance(report, dict) or report.get("status") != "PASS":
        raise ValueError("report must PASS")
    project = report.get("project")
    if not isinstance(project, str) or not Path(project).is_absolute() or Path(project).resolve() != root:
        raise ValueError("report project mismatch")
    for key in ("runId", "configHash", "sourceFingerprint"):
        if not isinstance(report.get(key), str) or not report[key].strip():
            raise ValueError("report missing provenance")
    if not timestamp(report.get("finishedAt")) >= timestamp(report.get("startedAt")) >= cutoff:
        raise ValueError("report predates capture or has invalid chronology")
    if report.get("sourceChanged", False) is not False or report.get("unregistered") != []:
        raise ValueError("report source changed or inventory is incomplete")
    results = report.get("results")
    if not isinstance(results, list) or not results:
        raise ValueError("report results are missing")
    summary = {}
    for result in results:
        if not isinstance(result, dict):
            raise ValueError("malformed suite result")
        identity = result.get("id")
        if not isinstance(identity, str) or not identity.strip() or identity in summary:
            raise ValueError("suite IDs must be unique nonempty strings")
        if (result.get("status") != "PASS" or not isinstance(result.get("reporter"), str)
                or result["reporter"] not in REPORTERS):
            raise ValueError("suite must PASS with a supported reporter")
        passed = result.get("passed")
        if type(passed) is not int or passed <= 0:
            raise ValueError("suite requires positive passed count")
        for counter in ("failed", "skipped", "todo", "flaky"):
            if counter in result and (type(result[counter]) is not int or result[counter] != 0):
                raise ValueError("suite contains failures or skipped tests")
        members, paths = result.get("members"), result.get("memberPaths")
        if (type(members) is not int or members <= 0 or not isinstance(paths, list)
                or members != len(paths)):
            raise ValueError("invalid suite membership")
        checked = set()
        for path in paths:
            member = safe_file(root, path)
            if member in checked:
                raise ValueError("duplicate suite member")
            checked.add(member)
        summary[identity] = {"id": identity, "passed": passed, "members": members,
                             "memberPaths": paths, "reporter": result["reporter"]}
    if not set(required).issubset(summary):
        raise ValueError("required suite is missing")
    return [summary[identity] for identity in required]
