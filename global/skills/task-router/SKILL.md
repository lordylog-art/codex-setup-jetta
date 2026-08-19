---
name: task-router
description: Gatekeeper that classifies tasks, selects skill, model, and execution mode before spending tokens.
---

# Task Router (Gatekeeper)
 
## Skill Path Rules
 
- Resolve every relative path in this skill from `C:\Users\Jetta\.codex\skills\task-router\`.
- Shared checklists live in `C:\Users\Jetta\.codex\skills\_checklists\`; from this skill, reference them as `../_checklists/...`.
- If this skill cites a checklist path, script path, or reference file, open and run it before substantial work.
- If a required file is missing, say that clearly and stop assuming it should be resolved from the project workspace.

Run this BEFORE any skill. It decides what to do and how much to spend.

## Step 0: CHECK 5s

Run `../_checklists/check-5s.md` first. If the answer is "resolve locally", stop here.

## Step 1: Classify

| Input | Simple | Medium | Complex |
|-------|--------|--------|---------|
| Files impacted | 1-2 | 3-5 | 6+ |
| Side-effects | None | Some | Auth/DB/money/destructive |
| Domain | UI, config, typo | Feature, bug fix | Architecture, security, multi-system |

## Step 2: Decide execution mode

| Classification | Action | Prompt style |
|----------------|--------|-------------|
| **Simple** | Resolve directly. No skill, no long prompt. | None " just do it |
| **Medium** | Use skill with compact prompt. Patch mode. | Minimal: task + files + constraint |
| **Complex** | Skill + review. Consider external AI. | Full: task + objective + files + constraints + acceptance + delivery |

## Step 3: Select skill

| Domain | Skill |
|--------|-------|
| Apps Script / Sheets code | `appscript` |
| Web app (frontend + backend) | `web-builder` |
| Architecture / planning | `architect-handoff` |
| Code review / security audit | `reviewer` (offensive mode auto-activates for auth/API/data scope) |
| Spreadsheet files | `spreadsheet` |

## Step 4: Select model

| Classification | Recommended model |
|----------------|-------------------|
| Simple | Current model (Codex local) |
| Medium | Current model or GPT |
| Complex | Claude / strongest available |

## Step 5: Select review level

| Classification | Review |
|----------------|--------|
| Simple | None |
| Medium | Self-review with checklist |
| Complex | Invoke `reviewer` after implementation |

## Risk escalators (always upgrade level)

- Touches auth/permissions ' min Medium, usually Complex
- Input validation / File handling boundaries ' Complex
- Database migration ' Complex
- Payment/money ' Complex
- Destructive/irreversible ' Complex
- Public API contract change ' Medium+
- Regras de restricao, elegibilidade, alocacao manual/automatica, ou qualquer logica que decide se um candidato entra ou fica de fora ' Medium+, normalmente Complex se tocar endpoint real

## Checklists (load only when relevant)

- `../_checklists/checklist-auth.md` " auth & session changes
- `../_checklists/checklist-admin.md` " admin & privilege changes
- `../_checklists/checklist-api.md` " API & endpoint changes
- `../_checklists/checklist-sheets.md` " Sheets & Apps Script changes

## Context rules

- Fixed context (skill rules): loaded once, never repeated.
- Variable context: only impacted files, not full codebase.
- Never use complex approach for simple task.
## Mandatory Automated Testing Policy
- Automated testing is mandatory for every behavior-changing code change.
- Route implementation tasks under the standard in `../_shared/tdd-decente.md`.
- Prefer executors that can protect the real regression surface, not only produce low-level tests.
- For React/UI tasks with layout toggles or imperative DOM enhancers, route with an explicit requirement to test the real transition path.
- If the task changes operational restrictions, eligibility, candidate selection, or assignment blocking, route with an explicit practical validation requirement against a real local endpoint or real flow when safe.

## Automated Test Selection
- Run the automated tests and validations that directly match the changed area and risk.
- Prefer native project commands such as `npm run test --workspace @erp-jetta/api`, `npm run test --workspace @erp-jetta/web`, `npm run lint`, or `npm run build` when they are the clearest coverage for the task.
- Do not require the project Python automation runner for routine implementation or review work.
- Use the central automation runner only when the user explicitly asks for it or when a deploy/ship script being executed requires it.
- If relevant tests cannot be run, report the exact validation gap instead of substituting the Python runner by default.