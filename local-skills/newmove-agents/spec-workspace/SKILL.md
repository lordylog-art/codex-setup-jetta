---
name: spec-workspace
description: Resolve and maintain an Obsidian workspace for the Matchbot Spec Driven workflow, only when the user provides an explicit Obsidian reference.
---

# Spec Workspace Adapter

Use this shared adapter whenever any engineering skill receives or inherits an Obsidian Spec Driven artifact.

## Mode selection

- No explicit Obsidian URI, vault note/folder path, or instruction to work in a named Obsidian note/folder: do not call the resolver. Run the original skill unchanged, including its output path, tracker, prompts, and sequence.
- With an explicit reference, pass only that reference to `scripts/spec_workspace.py`. A relative path counts only when it resolves to an existing path inside a configured Obsidian vault. Never infer Obsidian mode from a vault merely being installed.
- Supported references: `obsidian://open?...`, Obsidian wikilinks, Markdown links, and absolute or vault-root-relative paths to an existing Markdown note or folder. Handle Windows paths, spaces, brackets, accents, parentheses, and angle-bracket links. Do not guess missing paths or select among ambiguous vaults.
- If the input points inside an existing `Spec Driven` or legacy `Specdriven` folder, reuse that workspace. Read its `Index.md` to recover the source note. If the Index is absent, preserve the current workspace and use its parent as the feature context.
- The resolver creates only the workspace folder. Create category folders only when the workflow writes an artifact there.

## Tracker override and artifact routing

An explicit or inherited Obsidian workspace temporarily replaces the configured issue tracker for that workflow. `Tickets/` and `Wayfinder/` Markdown are canonical for this effort; do not also publish their spec, tickets, map, or state to GitHub/GitLab. The repository tracker remains unchanged and resumes on the next invocation without an Obsidian reference.

Use `scripts/spec_workspace.py` as the shared resolver and file adapter. `artifact_path(workspace, type, title)` routes `context`, `decision`, `diagnostic`, `handoff`, `map`, `questionnaire`, `research`, `spec`, `ticket`, and `validation` to their matching folders, without creating empty folders. `write_artifact(...)` reuses stable title-derived paths, preserves manual note sections, and updates `Index.md`; `update_index(workspace, groups)` changes only generated pointers. Before creating, check the Index and related category for the same semantic artifact; supply stable `artifact_id`, source, or tracker identity when available. If a matching manual note exists, add/update only the generated section. Never overwrite it. Keep Index low resolution; point to artifacts rather than copying their contents.

The Obsidian tracker keeps Matchbot's semantics: one ticket per file; `triage_role` for its five canonical roles; `ticket_status` for `open`/`claimed`/`resolved`; `blocked_by` wikilinks; comments under `## Comments`; and map/child pointers. Claim before work. `frontier(workspace)` reads only Index-linked, ready-for-agent, open and unblocked tickets. `transition_ticket`, `transition_triage_role`, and `append_comment` reread the target note and atomically update it. Per-file locks reject concurrent writers; if a process leaves a `.lock` after crashing, check its recorded PID before removing it. In Obsidian-mode tickets, use these fields; the local `.scratch` template's single `Status:` field cannot represent all three state dimensions. Keep ticket fields separate from folder status (`pending`, `production`, `implemented`). `workflow_status(statuses, validated)` returns `implemented` only when every ticket is resolved and validation is complete.

Feature-local context and decisions belong in this workspace. Repo-wide glossary/ADR changes stay in the project's configured domain docs; link to them instead of copying them. Code, tests, prototypes, screenshots, binaries, logs, and build outputs remain in their technical locations.

## Workspace layout

New workspaces use this shallow layout; create only categories with actual artifacts:

```text
Spec Driven/
├── Index.md
├── Context/       # Context.md only when a concise context artifact is needed
├── Specs/         # canonical spec for this Obsidian workflow
├── Tickets/       # one Markdown file per ticket
├── Decisions/     # only recorded decisions
├── Research/      # discovery, research, architecture notes, plans, prototypes, handoffs
└── Validation/    # validation plans and reports
```

Keep implementation source, tests, generated application docs, and other files required by the software in the repository. Markdown notes created as part of the Spec Driven workflow belong in this workspace.

For an existing `Spec Driven` or `Specdriven` workspace, preserve its files and paths. Reuse a matching `SPEC.md`, `spec.md`, or equivalent before creating another spec. Keep existing ticket files in place and link them from the Index; new artifacts may use the category layout above. Never rename, move, delete, or replace user-authored content to normalize the layout.

## Links, metadata, and idempotency

- `Index.md` is the concise entry point. Keep its source, spec, tickets, decisions, research, and validation links current. Use vault-root-relative wikilinks.
- New Index frontmatter uses the existing property vocabulary: `type: spec-driven-index`, `status: pending`, and `source: "[[<vault-relative source note>]]"` when a source note exists. Its generated section should have a short feature summary/status and links grouped by Spec, Tickets, Decisions, Research, and Validation. Omit empty groups.
- Specs use `type: spec`, a note `status`, and source/decision links. Tickets use `type: ticket`, `triage_role`, `ticket_status`, `spec`, relevant `context`, and `blocked_by` links. Keep ticket content aligned with the approved Matchbot process without copying the complete spec/context.
- Create frontmatter using existing vault properties: `type` and `status`. Add relationship properties such as `source`, `spec`, `context`, and `ticket` as wikilinks. Do not copy full context into each artifact.
- A spec links back to its source context and forward to its tickets. Each ticket links to its spec and relevant context. Decisions link to the affected context/spec. Validation notes link to the validated spec or ticket.
- Before writing, search the workspace Index and the relevant category only. Match by type, source/spec relationship, tracker URL or ID, and semantic title. Update the matching generated section; preserve manual sections. Never recursively load the workspace.
- Use stable names and one file per artifact. Preserve Matchbot's dependency-order numbering. In this mode the workspace is canonical for specs, tickets, maps, and workflow state; retain external references only when the user explicitly supplied them as source context.
- Update generated parts of `Index.md` within `<!-- spec-workspace:generated:start -->` and `<!-- spec-workspace:generated:end -->`; leave other text intact. Include a short feature summary and current workflow status.

## Obsidian metadata and appearance

The current vault uses `type`/`status` note properties; Folder Status values are `pending`, `production`, and `implemented`. Preserve Matchbot ticket states in ticket notes. Map workspace progress to the folder values: pending before implementation, production while implementation is active, implemented when the workflow is complete. Do not set a completion state from a single ticket completion.

After creating or updating the workspace or its artifact folders/files, call `python .agents/skills/spec-workspace/scripts/spec_workspace.py --reference "<explicit reference or workspace artifact path>" --style-path "<vault-relative category or Markdown path>"`. Repeat `--style-path` for additional paths. Use `--status pending|production|implemented` only for a direct workspace status transition. The helper adds missing plugin entries and preserves existing customization. It reuses the installed Folder Status, Iconocolor, and Obsidian File Color data when present; it installs no plugins. Existing style entries win.

Use existing semantic palette `especificacoes` for workflow notes when present. Folder icons: workspace `lucide:files`, Context `lucide:notebook-pen`, Specs `lucide:clipboard-list`, Tickets `lucide:list-checks`, Decisions `lucide:git-branch`, Research `lucide:search`, Validation `lucide:badge-check`. Inherit the vault's existing base color. Do not put emoji in names.

## Skill handoff

Pass the resolver result (workspace path, source link, and mode) in the current workflow context to the next skill. A later skill may recover it from the input artifact's location and `Index.md`; do not require the user to repeat the Obsidian reference. This is per-workflow context, never global state. A later invocation without an Obsidian reference follows its original skill behavior.

Use this adapter for:

- `setup-matt-pocock-skills`, `grill-with-docs`, `domain-modeling`, `to-spec`, `to-tickets`, `wayfinder`, and `triage` to route feature-local context and use the temporary local tracker override;
- `implement-spec`, `implement`, and Luna orchestration to read only the Index, relevant spec, and ready tickets, then place generated Markdown notes in this workspace;
- `ask-matt`, `code-review`, `diagnosing-bugs`, `tdd`, `research`, `prototype`, `improve-codebase-architecture`, `handoff`, `to-questionnaire`, and validation skills only when they receive an artifact from or produce an artifact for this workflow. Method-only skills keep their original behavior and remain stateless unless their original process reads workspace context.

Research, prototype, and implementation source code that must run stays in its normal technical location. Store Markdown findings, decisions, handoffs, questionnaires, diagnostics, and validation reports in the workspace.
