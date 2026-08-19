#!/usr/bin/env python3
"""Scan and safely fix mojibake in Brazilian Portuguese text."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from charset_normalizer import from_bytes
from ftfy import fix_text


SUSPECT_MARKERS = ("Ã", "Â", "â€™", "â€œ", "â€", "�", "ðŸ")
DEFAULT_EXTENSIONS = {
    ".cjs",
    ".css",
    ".csv",
    ".html",
    ".js",
    ".jsx",
    ".json",
    ".mjs",
    ".prisma",
    ".py",
    ".sql",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}
DOC_EXTENSIONS = {".md", ".mdx", ".rst"}
SKIP_DIRS = {
    ".git",
    ".next",
    ".turbo",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "logs",
    "node_modules",
    "out",
    "tmp",
}
TEST_NAME_MARKERS = (".spec.", ".test.", "__tests__")


@dataclass
class Issue:
    file: str
    line: int
    original: str
    fixed: str
    changed: bool


@dataclass
class FileReport:
    file: str
    encoding: str
    lines_with_issues: int
    lines_changed: int
    issues: list[Issue]


def has_marker(text: str) -> bool:
    return any(marker in text for marker in SUSPECT_MARKERS)


def marker_count(text: str) -> int:
    return sum(text.count(marker) for marker in SUSPECT_MARKERS)


def looks_better(original: str, fixed: str) -> bool:
    if original == fixed:
        return False
    if not has_marker(original):
        return False
    original_score = marker_count(original)
    fixed_score = marker_count(fixed)
    if fixed_score >= original_score:
        return False
    return True


def decode_bytes(data: bytes) -> tuple[str, str, bool]:
    had_bom = data.startswith(b"\xef\xbb\xbf")
    try:
        return data.decode("utf-8-sig"), "utf-8-sig" if had_bom else "utf-8", had_bom
    except UnicodeDecodeError:
        matches = from_bytes(data)
        best = matches.best()
        if best and best.encoding:
            return str(best), best.encoding, had_bom
        return data.decode("utf-8", errors="replace"), "utf-8-replace", had_bom


def should_skip_path(path: Path, include_tests: bool, include_docs: bool) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIRS:
        return True
    suffix = path.suffix.lower()
    allowed = set(DEFAULT_EXTENSIONS)
    if include_docs:
        allowed |= DOC_EXTENSIONS
    if suffix not in allowed:
        return True
    path_text = str(path)
    if not include_tests and any(marker in path_text for marker in TEST_NAME_MARKERS):
        return True
    return False


def iter_files(paths: Iterable[Path], include_tests: bool, include_docs: bool) -> list[Path]:
    files: list[Path] = []
    for input_path in paths:
        path = input_path.resolve()
        if path.is_file():
            if not should_skip_path(path, include_tests, include_docs):
                files.append(path)
            continue
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and not should_skip_path(child, include_tests, include_docs):
                    files.append(child)
    return sorted(set(files))


def analyze_text(text: str, file_label: str) -> tuple[list[str], FileReport]:
    output_lines: list[str] = []
    issues: list[Issue] = []
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines, start=1):
        if has_marker(line):
            fixed = fix_text(line)
            changed = looks_better(line, fixed)
            issues.append(
                Issue(
                    file=file_label,
                    line=index,
                    original=line.rstrip("\r\n"),
                    fixed=fixed.rstrip("\r\n"),
                    changed=changed,
                )
            )
            output_lines.append(fixed if changed else line)
        else:
            output_lines.append(line)
    report = FileReport(
        file=file_label,
        encoding="text",
        lines_with_issues=len(issues),
        lines_changed=sum(1 for issue in issues if issue.changed),
        issues=issues,
    )
    return output_lines, report


def analyze_file(path: Path, apply_fix: bool) -> FileReport | None:
    data = path.read_bytes()
    if b"\x00" in data[:4096]:
        return None
    text, encoding, had_bom = decode_bytes(data)
    if not has_marker(text):
        return FileReport(str(path), encoding, 0, 0, [])
    fixed_lines, report = analyze_text(text, str(path))
    report.encoding = encoding
    if apply_fix and report.lines_changed:
        fixed_text = "".join(fixed_lines)
        prefix = "\ufeff" if had_bom else ""
        path.write_text(prefix + fixed_text, encoding="utf-8", newline="")
    return report


def format_report(reports: list[FileReport], mode: str, scope: list[str]) -> str:
    analyzed = len(reports)
    affected = [report for report in reports if report.lines_with_issues]
    changed = [report for report in reports if report.lines_changed]
    total_issue_lines = sum(report.lines_with_issues for report in reports)
    total_changed_lines = sum(report.lines_changed for report in reports)
    changed_files_label = "Arquivos alterados" if mode == "fix" else "Arquivos com correção segura"
    changed_lines_label = "Linhas corrigidas" if mode == "fix" else "Linhas corrigíveis"
    per_file_changed_label = "corrigida(s)" if mode == "fix" else "corrigível(is)"
    lines = [
        "# Relatório de Mojibake PT-BR",
        "",
        f"- Modo: `{mode}`",
        f"- Escopo: {', '.join(scope)}",
        f"- Arquivos analisados: {analyzed}",
        f"- Arquivos com suspeita: {len(affected)}",
        f"- {changed_files_label}: {len(changed)}",
        f"- Linhas com problema: {total_issue_lines}",
        f"- {changed_lines_label}: {total_changed_lines}",
    ]
    if affected:
        lines.extend(["", "## Arquivos"])
        for report in affected:
            lines.append(
                f"- `{report.file}`: {report.lines_with_issues} linha(s) suspeita(s), "
                f"{report.lines_changed} {per_file_changed_label}"
            )
    examples: list[Issue] = []
    for report in affected:
        examples.extend(issue for issue in report.issues if issue.changed)
    if examples:
        lines.extend(["", "## Exemplos"])
        for issue in examples[:10]:
            lines.append(f"- `{issue.file}:{issue.line}`")
            lines.append(f"  - Antes: {issue.original[:180]}")
            lines.append(f"  - Depois: {issue.fixed[:180]}")
    manual = [
        issue
        for report in affected
        for issue in report.issues
        if not issue.changed
    ]
    if manual:
        lines.extend(["", "## Pendências Manuais"])
        for issue in manual[:20]:
            lines.append(f"- `{issue.file}:{issue.line}`: {issue.original[:180]}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit and fix PT-BR mojibake.")
    parser.add_argument("mode", choices=["scan", "fix"])
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--text")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--include-tests", action="store_true")
    parser.add_argument("--include-docs", action="store_true")
    args = parser.parse_args()

    reports: list[FileReport]
    scope: list[str]
    if args.text is not None or args.stdin:
        input_text = args.text if args.text is not None else sys.stdin.read()
        _, report = analyze_text(input_text, "<texto>")
        reports = [report]
        scope = ["trecho informado"]
    else:
        input_paths = [Path(path) for path in (args.path or [os.getcwd()])]
        files = iter_files(input_paths, args.include_tests, args.include_docs)
        reports = []
        for file_path in files:
            report = analyze_file(file_path, apply_fix=args.mode == "fix")
            if report is not None:
                reports.append(report)
        scope = [str(path) for path in input_paths]

    if args.json_out:
        payload = {
            "mode": args.mode,
            "scope": scope,
            "reports": [
                {
                    **asdict(report),
                    "issues": [asdict(issue) for issue in report.issues],
                }
                for report in reports
            ],
        }
        Path(args.json_out).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    print(format_report(reports, args.mode, scope))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
