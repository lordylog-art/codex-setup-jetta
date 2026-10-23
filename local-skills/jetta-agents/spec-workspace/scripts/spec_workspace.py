#!/usr/bin/env python3
"""Resolve one explicit Obsidian reference to its Spec Driven workspace."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import parse_qs, urlparse


WORKSPACE_NAMES = {"specdriven"}
ICONS = {
    "Spec Driven": "lucide:files",
    "Context": "lucide:notebook-pen",
    "Specs": "lucide:clipboard-list",
    "Tickets": "lucide:list-checks",
    "Decisions": "lucide:git-branch",
    "Research": "lucide:search",
    "Validation": "lucide:badge-check",
    "Diagnostics": "lucide:bug",
    "Handoffs": "lucide:send",
    "Questionnaires": "lucide:clipboard-list",
    "Wayfinder": "lucide:map",
}
CATEGORIES = {
    "context": "Context", "decision": "Decisions", "diagnostic": "Diagnostics",
    "handoff": "Handoffs", "map": "Wayfinder", "questionnaire": "Questionnaires",
    "research": "Research", "spec": "Specs", "ticket": "Tickets", "validation": "Validation",
}
GENERATED_START = "<!-- spec-workspace:generated:start -->"
GENERATED_END = "<!-- spec-workspace:generated:end -->"


class ResolutionError(ValueError):
    pass


def default_config() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library/Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "obsidian" / "obsidian.json"


def load_vaults(config: Path) -> list[tuple[str, Path]]:
    try:
        data = json.loads(config.read_text(encoding="utf-8"))
        entries = data["vaults"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise ResolutionError(f"Cannot read Obsidian vault configuration: {config}") from exc
    vaults = []
    for vault_id, info in entries.items():
        path = info.get("path") if isinstance(info, dict) else None
        if path:
            vaults.append((vault_id, Path(path).expanduser().resolve()))
    return vaults


def extract_target(reference: str) -> tuple[str | None, str]:
    value = reference.strip()
    markdown_link = re.search(r"\[[^\]]*\]\(<([^>]+)>\)|\[[^\]]*\]\(([^)]+)\)", value)
    if markdown_link:
        value = markdown_link.group(1) or markdown_link.group(2)
        value = value.strip()
    elif not value.startswith("obsidian://"):
        uri = re.search(r"obsidian://[^\s<>\]]+", value)
        wiki = re.search(r"!?\[\[([^\]]+)\]\]", value)
        if uri:
            value = uri.group(0)
        elif wiki:
            value = f"[[{wiki.group(1)}]]"
        else:
            absolute_paths = re.findall(r"(?<![A-Za-z0-9_.-])(?:[A-Za-z]:[\\/]|/)[^<>\"`\r\n]+", value)
            if len(absolute_paths) == 1:
                value = absolute_paths[0].strip().rstrip(" .,:;)")
            elif len(absolute_paths) > 1:
                raise ResolutionError("Obsidian reference has multiple absolute paths; pass one note or folder")
            else:
                value = value.splitlines()[0].strip().strip("<>")
    if value.startswith("obsidian://"):
        query = parse_qs(urlparse(value).query)
        vault = query.get("vault", [None])[0]
        note = query.get("file", [""])[0]
        if not note:
            raise ResolutionError("Obsidian URI has no file or folder path")
        return vault, note
    if value.startswith("[[") and value.endswith("]]"):
        value = value[2:-2].split("|", 1)[0].split("#", 1)[0]
    return None, value


def inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_target(reference: str, vaults: list[tuple[str, Path]]) -> tuple[Path, Path]:
    vault_hint, target = extract_target(reference)
    candidates = vaults
    if vault_hint:
        candidates = [
            (vault_id, root)
            for vault_id, root in vaults
            if vault_hint.casefold() in {vault_id.casefold(), root.name.casefold(), str(root).casefold()}
        ]
        if len(candidates) != 1:
            raise ResolutionError(f"Obsidian vault reference is missing or ambiguous: {vault_hint}")

    found = []
    raw_path = Path(target).expanduser()
    for _, root in candidates:
        path = raw_path.resolve() if raw_path.is_absolute() else (root / target).resolve()
        options = [path]
        if not path.suffix:
            options.append(path.with_suffix(".md"))
        for option in options:
            if inside(option, root) and option.exists():
                found.append((option, root))
    unique = {(str(path).casefold(), str(root).casefold()): (path, root) for path, root in found}
    if len(unique) != 1:
        reason = "not found" if not unique else "ambiguous across vaults"
        raise ResolutionError(f"Obsidian reference {reason}: {target}")
    return next(iter(unique.values()))


def workspace_ancestor(path: Path, vault: Path) -> Path | None:
    for parent in (path, *path.parents):
        if not inside(parent, vault):
            break
        if re.sub(r"[^a-z]", "", parent.name.casefold()) in WORKSPACE_NAMES:
            return parent
    return None


def existing_workspace(root: Path) -> Path:
    matches = [
        child for child in root.iterdir()
        if child.is_dir() and re.sub(r"[^a-z]", "", child.name.casefold()) in WORKSPACE_NAMES
    ] if root.is_dir() else []
    if len(matches) > 1:
        raise ResolutionError(f"Multiple Spec Driven workspaces under {root}")
    return matches[0] if matches else root / "Spec Driven"


def source_from_index(workspace: Path, vault: Path) -> str | None:
    index = workspace / "Index.md"
    if not index.is_file():
        return None
    content = index.read_text(encoding="utf-8")
    match = re.search(r"^source:\s*\"?\[\[([^]|]+)", content, re.MULTILINE)
    if not match:
        return None
    source = match.group(1).strip()
    candidate = vault / source
    if candidate.exists():
        return source
    if not candidate.suffix and candidate.with_suffix(".md").exists():
        return candidate.with_suffix(".md").relative_to(vault).as_posix()
    return None


def register_style(vault: Path, paths: list[str], status: str | None = None) -> None:
    plugin_root = vault / ".obsidian" / "plugins"
    folder_status = plugin_root / "folder-status" / "data.json"
    if folder_status.is_file():
        with _exclusive_lock(folder_status):
            data = json.loads(folder_status.read_text(encoding="utf-8"))
            folders = data.setdefault("folders", {})
            root = paths[0] if paths else None
            if root:
                if status:
                    folders[root] = status
                elif root not in folders:
                    folders[root] = "pending"
            write_json(folder_status, data)

    index_path = vault / paths[1] if len(paths) > 1 and paths[1].endswith("/Index.md") else None
    if status and index_path and index_path.is_file():
        frontmatter, body = _frontmatter(index_path)
        if frontmatter:
            frontmatter = _set_field(frontmatter, "status", status)
            temp = index_path.with_suffix(".md.tmp")
            temp.write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8")
            temp.replace(index_path)

    icon_file = plugin_root / "iconocolor" / "data.json"
    if icon_file.is_file():
        with _exclusive_lock(icon_file):
            data = json.loads(icon_file.read_text(encoding="utf-8"))
            configs = data.setdefault("folderConfigs", {})
            for item in paths:
                name = Path(item).name
                icon = ICONS.get(name)
                if icon and item not in configs:
                    configs[item] = {"icon": icon, "inheritBaseColor": True, "applyToSubfolders": True}
            write_json(icon_file, data)

    colors_file = plugin_root / "obsidian-file-color" / "data.json"
    if colors_file.is_file():
        with _exclusive_lock(colors_file):
            data = json.loads(colors_file.read_text(encoding="utf-8"))
            palette = {item.get("id") for item in data.get("palette", []) if isinstance(item, dict)}
            if "especificacoes" in palette:
                colors = data.setdefault("fileColors", [])
                known = {item.get("path") for item in colors if isinstance(item, dict)}
                for item in paths:
                    if item.lower().endswith(".md") and item not in known:
                        colors.append({"path": item, "color": "especificacoes"})
                write_json(colors_file, data)


def write_json(path: Path, data: dict) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


@contextmanager
def _exclusive_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + ".lock")
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise ResolutionError(f"Artifact is being updated by another workflow; retry after checking {lock}") from exc
    try:
        os.write(descriptor, f"pid={os.getpid()}\n".encode("ascii"))
        yield
    finally:
        os.close(descriptor)
        lock.unlink(missing_ok=True)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "artifact"


def artifact_path(workspace: Path, artifact_type: str, preferred_name: str, artifact_id: str | None = None) -> Path:
    category = CATEGORIES.get(artifact_type.casefold())
    if not category:
        raise ResolutionError(f"Unsupported artifact type: {artifact_type}")
    safe_name = Path(preferred_name).name
    if safe_name.casefold().endswith(".md"):
        safe_name = safe_name[:-3]
    if not safe_name.strip():
        raise ResolutionError("Artifact name cannot be empty")
    folder = workspace / category
    if artifact_type.casefold() == "map":
        return folder / "Map.md"
    if artifact_id:
        return folder / f"{slugify(artifact_id)}.md"
    # A stable title-derived path makes repeated writes idempotent; the folder stays lazy.
    exact = folder / f"{safe_name}.md"
    slug = folder / f"{slugify(safe_name)}.md"
    return exact if exact.exists() else slug


def _wikilink(path: str) -> str:
    if path.startswith("[[") and path.endswith("]]"):
        return path
    return f"[[{Path(path).with_suffix('').as_posix()}]]"


def _link_key(path: str) -> str:
    if path.startswith("[[") and path.endswith("]]" ):
        path = path[2:-2].split("|", 1)[0].split("#", 1)[0]
    return Path(path).with_suffix("").as_posix().casefold()


def update_index(workspace: Path, groups: dict[str, list[str]], summary: str = "") -> Path:
    index = workspace / "Index.md"
    with _exclusive_lock(index):
        return _update_index(workspace, groups, summary)


def _update_index(workspace: Path, groups: dict[str, list[str]], summary: str = "") -> Path:
    index = workspace / "Index.md"
    if index.exists():
        content = index.read_text(encoding="utf-8")
    else:
        content = f"---\ntype: spec-driven-index\nstatus: pending\n---\n\n# {workspace.parent.name} — Spec Driven\n"
    existing_groups: dict[str, list[str]] = {}
    current = re.search(re.escape(GENERATED_START) + r"(.*?)" + re.escape(GENERATED_END), content, re.DOTALL)
    if current:
        active_group = None
        for line in current.group(1).splitlines():
            heading = re.match(r"^## (.+)$", line)
            if heading:
                active_group = heading.group(1)
                existing_groups.setdefault(active_group, [])
            elif active_group:
                link = re.match(r"- \[\[([^]]+)\]\]", line)
                if link:
                    existing_groups[active_group].append(link.group(1))
        if not summary:
            prior_summary = re.search(r"^## Summary\s*\n(.*?)(?=^## |\Z)", current.group(1), re.MULTILINE | re.DOTALL)
            if prior_summary:
                summary = prior_summary.group(1).strip()
    merged = {key: list(values) for key, values in existing_groups.items()}
    for key, values in groups.items():
        links = merged.get(key, [])
        known = {_link_key(link) for link in links}
        for link in values:
            if _link_key(link) not in known:
                links.append(link)
                known.add(_link_key(link))
        merged[key] = links
    rendered = []
    if summary:
        rendered.extend(["## Summary", "", summary, ""])
    order = ("Source", "Context", "Decisions", "Specs", "Tickets", "Research", "Wayfinder", "Questionnaires", "Diagnostics", "Handoffs", "Validation")
    order += tuple(key for key in merged if key not in order)
    for group in order:
        links = merged.get(group, [])
        if links:
            rendered.extend([f"## {group}", ""])
            rendered.extend(f"- {_wikilink(link)}" for link in dict.fromkeys(links))
            rendered.append("")
    section = f"{GENERATED_START}\n" + "\n".join(rendered).rstrip() + f"\n{GENERATED_END}"
    pattern = re.compile(re.escape(GENERATED_START) + r".*?" + re.escape(GENERATED_END), re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(lambda _: section, content, count=1)
    else:
        content = content.rstrip() + "\n\n" + section + "\n"
    index.parent.mkdir(parents=True, exist_ok=True)
    temp = index.with_suffix(".md.tmp")
    temp.write_text(content, encoding="utf-8")
    temp.replace(index)
    return index


def _frontmatter(path: Path) -> tuple[str, str]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return "", content
    end = content.find("\n---", 4)
    if end < 0:
        return "", content
    return content[4:end], content[end + 4:].lstrip("\n")


def _set_field(frontmatter: str, key: str, value: str | list[str]) -> str:
    if isinstance(value, list):
        line = f"{key}:" + ("\n" + "\n".join(f"  - {item}" for item in value) if value else " []")
    else:
        line = f"{key}: {value}"
    pattern = re.compile(rf"^{re.escape(key)}:.*(?:\r?\n[ \t]+-.*)*", re.MULTILINE)
    if pattern.search(frontmatter):
        return pattern.sub(lambda _: line, frontmatter, count=1)
    return (frontmatter.rstrip() + "\n" + line).strip()


def transition_ticket(path: Path, status: str) -> None:
    with _exclusive_lock(path):
        _transition_ticket(path, status)


def _transition_ticket(path: Path, status: str) -> None:
    allowed = {"open": {"claimed"}, "claimed": {"resolved"}}
    frontmatter, body = _frontmatter(path)
    if not frontmatter:
        raise ResolutionError(f"Ticket has no frontmatter: {path}")
    kind = re.search(r"^type:\s*([^\n]+)", frontmatter, re.MULTILINE)
    if not kind or kind.group(1).strip().strip("\"'") != "ticket":
        raise ResolutionError(f"Not a ticket note: {path}")
    role = re.search(r"^triage_role:\s*([^\n]+)", frontmatter, re.MULTILINE)
    if status == "claimed" and (not role or role.group(1).strip().strip("\"'") != "ready-for-agent"):
        raise ResolutionError("Only ready-for-agent tickets can be claimed")
    current = re.search(r"^ticket_status:\s*([^\n]+)", frontmatter, re.MULTILINE)
    old = current.group(1).strip().strip("\"'") if current else "open"
    if status not in allowed.get(old, set()):
        raise ResolutionError(f"Invalid ticket transition: {old or 'unset'} -> {status}")
    frontmatter = _set_field(frontmatter, "ticket_status", status)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8")
    temp.replace(path)


def transition_triage_role(path: Path, role: str) -> None:
    with _exclusive_lock(path):
        _transition_triage_role(path, role)


def _transition_triage_role(path: Path, role: str) -> None:
    transitions = {
        "": {"needs-triage"},
        "needs-triage": {"needs-info", "ready-for-agent", "ready-for-human", "wontfix"},
        "needs-info": {"needs-triage"},
        "ready-for-agent": {"needs-triage", "ready-for-human", "wontfix"},
        "ready-for-human": {"needs-triage", "ready-for-agent", "wontfix"},
        "wontfix": {"needs-triage"},
    }
    frontmatter, body = _frontmatter(path)
    current = re.search(r"^triage_role:\s*([^\n]+)", frontmatter, re.MULTILINE)
    old = current.group(1).strip().strip("\"'") if current else ""
    if role not in transitions.get(old, set()):
        raise ResolutionError(f"Invalid triage transition: {old or 'unset'} -> {role}")
    frontmatter = _set_field(frontmatter, "triage_role", role)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8")
    temp.replace(path)


def append_comment(path: Path, comment: str) -> None:
    with _exclusive_lock(path):
        _append_comment(path, comment)


def _append_comment(path: Path, comment: str) -> None:
    if not comment.strip():
        raise ResolutionError("Comment cannot be empty")
    content = path.read_text(encoding="utf-8")
    marker = "## Comments"
    if marker not in content:
        content = content.rstrip() + "\n\n" + marker + "\n"
    content = content.rstrip() + "\n\n" + comment.strip() + "\n"
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(content, encoding="utf-8")
    temp.replace(path)


def _index_ticket_paths(workspace: Path) -> list[Path]:
    index = workspace / "Index.md"
    if not index.is_file():
        return []
    content = index.read_text(encoding="utf-8")
    paths = []
    for target in re.findall(r"\[\[([^]|#]+)", content):
        candidate = workspace / f"{target}.md"
        if candidate.parent == workspace / "Tickets" and candidate.is_file():
            paths.append(candidate)
    return list(dict.fromkeys(paths))


def _ticket_status(path: Path) -> str:
    frontmatter, _ = _frontmatter(path)
    match = re.search(r"^ticket_status:\s*([^\n]+)", frontmatter, re.MULTILINE)
    return match.group(1).strip().strip("\"'") if match else "open"


def frontier(workspace: Path) -> list[Path]:
    tickets = _index_ticket_paths(workspace)
    states = {path.stem.casefold(): _ticket_status(path) for path in tickets}
    ready = []
    for path in tickets:
        status = states[path.stem.casefold()]
        if status != "open":
            continue
        frontmatter, _ = _frontmatter(path)
        role = re.search(r"^triage_role:\s*([^\n]+)", frontmatter, re.MULTILINE)
        if not role or role.group(1).strip().strip("\"'") != "ready-for-agent":
            continue
        block = re.search(r"^blocked_by:[ \t]*\r?\n((?:[ \t]+-.*(?:\r?\n|$))*)", frontmatter, re.MULTILINE)
        blockers = re.findall(r"\[\[([^]|#]+)", block.group(1)) if block else []
        if all(states.get(Path(item).stem.casefold()) == "resolved" for item in blockers):
            ready.append(path)
    return sorted(ready, key=lambda item: item.name.casefold())


def workflow_status(ticket_statuses: list[str], validated: bool = False) -> str:
    if ticket_statuses and all(status == "resolved" for status in ticket_statuses) and validated:
        return "implemented"
    if any(status == "claimed" for status in ticket_statuses) or (ticket_statuses and all(status == "resolved" for status in ticket_statuses)):
        return "production"
    return "pending"


def write_artifact(workspace: Path, artifact_type: str, title: str, body: str,
                   metadata: dict[str, str | list[str]] | None = None) -> Path:
    artifact_id = metadata.get("artifact_id") if metadata else None
    path = artifact_path(workspace, artifact_type, title, artifact_id if isinstance(artifact_id, str) else None)
    with _exclusive_lock(path):
        return _write_artifact(workspace, artifact_type, title, body, metadata)


def _write_artifact(workspace: Path, artifact_type: str, title: str, body: str,
                    metadata: dict[str, str | list[str]] | None = None) -> Path:
    category = CATEGORIES.get(artifact_type.casefold())
    artifact_id = metadata.get("artifact_id") if metadata else None
    path = artifact_path(workspace, artifact_type, title, artifact_id if isinstance(artifact_id, str) else None)
    frontmatter, old_body = _frontmatter(path) if path.exists() else ("", "")
    start, end = "<!-- spec-workspace:artifact:start -->", "<!-- spec-workspace:artifact:end -->"
    section = f"{start}\n# {title}\n\n{body.rstrip()}\n{end}"
    if old_body and start in old_body and end in old_body:
        old_body = re.sub(re.escape(start) + r".*?" + re.escape(end), section, old_body, count=1, flags=re.DOTALL)
    elif old_body:
        old_body = old_body.rstrip() + "\n\n" + section + "\n"
    else:
        old_body = f"{section}\n"
    fields = {"type": artifact_type.casefold(), **(metadata or {})}
    if artifact_type.casefold() == "ticket":
        fields.setdefault("triage_role", "ready-for-agent")
        fields.setdefault("ticket_status", "open")
        fields.setdefault("status", "pending")
    else:
        fields.setdefault("status", "pending")
    for key, value in fields.items():
        encoded = value if isinstance(value, list) else (f'"{value}"' if any(char in value for char in ":#[]{}\n") else value)
        frontmatter = _set_field(frontmatter, key, encoded)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(f"---\n{frontmatter}\n---\n\n{old_body.lstrip()}", encoding="utf-8")
    temp.replace(path)
    group = {"spec": "Specs", "ticket": "Tickets"}.get(artifact_type.casefold(), category)
    update_index(workspace, {group: [path.relative_to(workspace).as_posix()]})
    return path


def resolve(reference: str, config: Path, status: str | None = None, style_paths: list[str] | None = None) -> dict:
    if not reference.strip():
        return {"mode": "default", "sourceType": "none", "sourcePath": None, "sourceNote": None,
                "rootDirectory": None, "specDrivenDirectory": None}
    vaults = load_vaults(config)
    path, vault = resolve_target(reference, vaults)
    workspace = workspace_ancestor(path, vault)
    if workspace:
        root = workspace.parent
        source = source_from_index(workspace, vault)
        result = {"mode": "obsidian", "sourceType": "artifact", "sourcePath": path.relative_to(vault).as_posix(),
                  "sourceNote": source, "rootDirectory": root.relative_to(vault).as_posix(),
                  "specDrivenDirectory": workspace.relative_to(vault).as_posix(), "vaultRoot": str(vault)}
    else:
        if path.is_file() and path.suffix.casefold() == ".md":
            source_type, root, source = "note", path.parent, path.relative_to(vault).as_posix()
        elif path.is_dir():
            source_type, root, source = "folder", path, None
        else:
            raise ResolutionError(f"Reference must be an existing Markdown note or folder: {path}")
        workspace = existing_workspace(root)
        workspace.mkdir(parents=True, exist_ok=True)
        result = {"mode": "obsidian", "sourceType": source_type, "sourcePath": path.relative_to(vault).as_posix(),
                  "sourceNote": source, "rootDirectory": root.relative_to(vault).as_posix(),
                  "specDrivenDirectory": workspace.relative_to(vault).as_posix(), "vaultRoot": str(vault)}

    source_link = result["sourceNote"]
    if source_link:
        source_folder = Path(result["specDrivenDirectory"])
        source_rel = Path(source_link)
        relative_source = os.path.relpath(source_rel, source_folder).replace("\\", "/")
        update_index(workspace, {"Source": [relative_source]})
        index = workspace / "Index.md"
        if index.is_file():
            with _exclusive_lock(index):
                frontmatter, body = _frontmatter(index)
                if not re.search(r"^source:", frontmatter, re.MULTILINE):
                    frontmatter = _set_field(frontmatter, "source", f'"[[{source_link}]]"')
                    temp = index.with_suffix(".md.tmp")
                    temp.write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8")
                    temp.replace(index)
    elif not (workspace / "Index.md").exists():
        update_index(workspace, {})
    paths = [result["specDrivenDirectory"], result["specDrivenDirectory"] + "/Index.md", *(style_paths or [])]
    register_style(vault, paths, status)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", default="")
    parser.add_argument("--obsidian-config", type=Path, default=default_config())
    parser.add_argument("--status", choices=("pending", "production", "implemented"))
    parser.add_argument("--style-path", action="append", default=[], help="additional vault-relative paths to style")
    args = parser.parse_args()
    try:
        print(json.dumps(resolve(args.reference, args.obsidian_config, args.status, args.style_path), ensure_ascii=False))
        return 0
    except (ResolutionError, OSError, ValueError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
