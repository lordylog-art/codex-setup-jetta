"""Conservative Git working-tree identity; no source contents are copied."""

import hashlib
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import platform
import stat
import subprocess
from datetime import datetime, timezone


SNAPSHOT_KEYS = {"version", "project", "createdAt", "environment", "files"}


def timestamp(value):
    if not isinstance(value, str) or not value:
        raise ValueError("invalid timestamp")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("invalid timestamp") from None
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("timestamp requires timezone")
    return result


def environment():
    return {"python": platform.python_version(), "platform": platform.platform()}


def _git(root, *args):
    try:
        return subprocess.run(["git", "-C", str(root), *args], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    except (OSError, subprocess.CalledProcessError):
        raise ValueError("cannot inspect Git repository") from None


def project_root(root):
    try:
        result = Path(root).resolve(strict=True)
        if not result.is_dir():
            raise ValueError("project must be a directory")
        git_root = Path(os.fsdecode(_git(result, "rev-parse", "--show-toplevel")).strip()).resolve(strict=True)
        if result != git_root:
            raise ValueError("project must be the exact Git root")
        return result
    except (OSError, TypeError, RuntimeError):
        raise ValueError("invalid project root") from None


def relative_path(value):
    if (not isinstance(value, str) or not value or "\\" in value or "\0" in value
            or PurePosixPath(value).is_absolute() or PureWindowsPath(value).drive
            or any(part in ("", ".", "..") for part in value.split("/"))):
        raise ValueError("invalid relative path")
    return value


def safe_file(root, name, missing=False):
    relative_path(name)
    target = root.joinpath(*name.split("/"))
    current = root
    for part in name.split("/"):
        current = current / part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            if missing:
                return None
            raise ValueError("inventory file is missing") from None
        if (stat.S_ISLNK(metadata.st_mode)
                or getattr(metadata, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
            raise ValueError("links are not supported")
    if not target.is_file() or not target.resolve().is_relative_to(root):
        raise ValueError("inventory member must be a regular project file")
    return target


def _files(root, missing=False):
    inventory = _git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    names = sorted({os.fsdecode(name) for name in inventory.split(b"\0") if name})
    result = {}
    for name in names:
        path = safe_file(root, name, missing=missing)
        result[name] = hashlib.sha256(path.read_bytes()).hexdigest() if path is not None else None
    if not result and not missing:
        raise ValueError("empty Git inventory")
    return result


def capture(root):
    root = project_root(root)
    return {"version": 1, "project": str(root),
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "environment": environment(), "files": _files(root)}


def validate(snapshot, root):
    if (not isinstance(snapshot, dict) or set(snapshot) != SNAPSHOT_KEYS
            or type(snapshot.get("version")) is not int or snapshot["version"] != 1):
        raise ValueError("invalid snapshot schema")
    if not isinstance(snapshot["project"], str) or not Path(snapshot["project"]).is_absolute():
        raise ValueError("invalid snapshot project")
    if Path(snapshot["project"]).resolve() != root:
        raise ValueError("snapshot project mismatch")
    if timestamp(snapshot["createdAt"]).utcoffset().total_seconds() != 0:
        raise ValueError("snapshot timestamp must be UTC")
    if snapshot["environment"] != environment():
        raise ValueError("snapshot environment mismatch")
    files = snapshot["files"]
    if not isinstance(files, dict) or not files:
        raise ValueError("invalid snapshot inventory")
    for name, digest in files.items():
        relative_path(name)
        if (not isinstance(digest, str) or len(digest) != 64
                or any(char not in "0123456789abcdef" for char in digest)):
            raise ValueError("invalid snapshot digest")


def changed(root, snapshot):
    root = project_root(root)
    validate(snapshot, root)
    current = _files(root, missing=True)
    previous = snapshot["files"]
    return sorted(name for name in current.keys() | previous.keys()
                  if name not in current or name not in previous or current[name] != previous[name])
