---
name: bug-resolver
description: Resolve reported software bugs end to end when the user asks to debug or fix a bug, with selective Obsidian bug memory and verified closure.
---

# Bug Resolver

Orchestrate a reported bug from triage through a verified fix and Obsidian closeout. Keep bug history as searchable local memory. Never treat an old resolution as proof.

## Locate and mark the bug

1. Identify the exact bug folder and the smallest relevant project context. Do not scan the whole `Bugs` tree.
2. Resolve the active Obsidian vault from `%APPDATA%/obsidian/obsidian.json` (`vaults.*.path` with `open: true` when available). Use its existing `Bugs` folder; do not create a parallel vault structure. If the active vault or target bug folder is ambiguous, ask before changing status.
3. Inspect `.obsidian/plugins/folder-status/main.js` and its `data.json` before changing status. Use only statuses supported by the installed plugin. Set the target folder to `production` when beginning work. The current plugin uses `implemented` for its final state; call this `completed` in the resolution note and report. Never add a plugin status.
4. Do not edit `AGENTS.md` or plugin source. Preserve existing folder data and update only the target folder's entry. If the plugin schema or status list differs from what the available updater can safely handle, use the plugin's Obsidian folder context menu or stop before changing status.

## Recover bug memory cheaply

Build a short fingerprint from available details: exact error/message/code, endpoint, function/component, module, file, key symptoms, expected/current behavior, technology, and integration. Omit unavailable fields.

The index is `<vault>/Bugs/_index/bugs.jsonl`. Do not create it until resolving a bug. If it does not exist, proceed without historical candidates.

Search only this index. Use the local `scripts/bug-memory.py search` helper or `rg` with a few specific fingerprint terms. Read it as a stream; never print or load the whole index. Search in this order: exact error/message, error code, endpoint, component/function, module, symptom combination, related tags. Return at most 3 candidates. Open a candidate resolution note only when its indexed terms make it plausibly related. If no candidate is relevant, open no old notes. Treat any prior cause/fix as a hypothesis to re-check against current code.

## Diagnose and fix

After memory lookup, locate and invoke the existing `diagnosing-bugs` skill (the repo skill commonly lives at `.agents/skills/diagnosing-bugs/SKILL.md`). Follow it; do not copy or replace its diagnostic method. Pass relevant historical evidence as a hypothesis only.

That skill requires a deterministic, red-capable feedback loop before hypotheses. Respect that gate. If the bug cannot be reproduced or its cause cannot be confirmed, stop without claiming resolution or setting a final status. Show the concise, falsifiable hypotheses checkpoint it requests. Inspect callers and current code, identify the root cause, apply the smallest fix, and run the focused regression signal plus relevant regressions. Do not change tests to bless incorrect behavior.

If any required test fails, continue diagnosis when useful, but never close the bug as completed. If validation is unavailable, report the blocker and leave the folder in `production`.

## Document and close

Only after root cause is confirmed, the fix is applied, focused and relevant regression tests pass, and the resolution note is saved:

1. Create or update `<bug-folder>/RESOLUCAO.md`, following any existing note convention. Use concise sections for Problema, Sintomas, Diagnóstico, Causa raiz, Correção, Testes, and Prevenção where useful. Record only tests actually run. Frontmatter uses `type: bug-resolution` and semantic `status: completed`. End with `[!success] Resolução`; use no decorative emoji.
2. Upsert one compact JSON object for this bug in `Bugs/_index/bugs.jsonl` using `scripts/bug-memory.py upsert`. Reuse the bug ID already assigned in the vault or index; if none exists, use the existing bug folder's stable name. Do not invent a competing ID. Include available title, area/module, components/files/endpoints, normalized symptoms/signatures, cause/fix tags, technology/integration, semantic status `completed`, and relative note path. Keep one line per bug, update an existing ID in place, preserve other lines/order, and do not duplicate IDs.
3. As the final approval state change, set this folder through the existing Folder Status plugin's storage contract. Use `scripts/bug-memory.py set-status` only if its source/schema checks pass. Require explicit evidence flags for confirmed root cause, passing required tests, passing relevant regressions, and saved documentation. The helper maps semantic `completed` to the plugin's existing `implemented` identifier. If any condition is false, do not set the final status. Confirm the persisted target entry.

## Report

Keep the final report short:

```text
Bug:
Causa raiz:
Correção:
Testes:
Bug semelhante:
Documentação:
Status da pasta:
```

State exact status identifier if useful (`implemented`, semantic `completed`). Never claim success without test evidence.
