---
name: appscript
description: Maintain, debug, and build Apps Script/Sheets with TDD, minimal patches, and strict validation.
---

# Apps Script
 
## Skill Path Rules
 
- Resolve every relative path in this skill from `C:\Users\Jetta\.codex\skills\appscript\`.
- Shared checklists live in `C:\Users\Jetta\.codex\skills\_checklists\`; from this skill, reference them as `../_checklists/...`.
- If this skill cites a checklist path, script path, or reference file, open and run it before substantial work.
- If a required file is missing, say that clearly and stop assuming it should be resolved from the project workspace.

## Before executing

If routed here via `task-router`, skip `check-5s.md` " classification already done.
Otherwise: is this simple + non-critical + no plan needed? Resolve directly without loading references.

## Rules

- Read only files in execution path.
- Red ' Green ' Refactor for non-trivial changes.
- Fix root cause, not symptom.
- Smallest safe patch. No duplicate helpers.
- Batch service calls. Validate inputs early.
- Separate service calls from pure logic.
- V8 compatible. No Node-only APIs. No ESM unless build step.
- Reuse existing patterns.

## Patch mode (mandatory)

- Return only changed code, not full files.
- Prefer diff/patch format.
- Never rewrite unchanged sections.

## Workflow

1. Understand problem and affected flow.
2. Write/adjust tests before code.
3. Implement minimum fix.
4. Run relevant tests.
5. Validate against relevant `../_checklists/`.

## Output rules

- No unchanged code in response.
- No long explanations. Max objectivity.
- Short report: problem ' root cause ' test(s) ' change ' validation ' remaining risk.

## Deploy

Do not run `clasp push` without explicit user approval.
If applicable, ask: `Deseja que eu execute clasp push agora?`

## References (load only when needed)

- `references/apps-script-patterns.md` " runtime, service, Sheets, HtmlService patterns.
- `references/testing-and-clasp.md` " local testing, clasp workflow, manual verification.
- `../_checklists/checklist-sheets.md` " validation checklist.
- `../_checklists/checklist-auth.md` " if auth is involved.
## Mandatory Automated Testing Policy
- Automated testing is mandatory for every behavior-changing code change.
- Follow `../_shared/tdd-decente.md` as the quality bar.
- When the issue lives in trigger flow, sheet orchestration, or HTTP integration behavior, do not accept pure helper-only coverage.
- If the delivered surface includes UI mode switching or imperative DOM enhancement, carry the same transition-regression rule from `../_shared/tdd-decente.md`.
## Automated Test Selection
- Run the automated tests and validations that directly match the changed area and risk.
- Prefer native project commands such as `npm run test --workspace @erp-jetta/api`, `npm run test --workspace @erp-jetta/web`, `npm run lint`, or `npm run build` when they are the clearest coverage for the task.
- Do not require the project Python automation runner for routine implementation or review work.
- Use the central automation runner only when the user explicitly asks for it or when a deploy/ship script being executed requires it.
- If relevant tests cannot be run, report the exact validation gap instead of substituting the Python runner by default.