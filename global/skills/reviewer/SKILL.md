---
name: reviewer
description: Severity-based production review with strict verdicts. Covers correctness, regressions, architecture drift, security, and performance/cost optimization when the change touches hot paths, queries, rendering, batching, or infrastructure-sensitive flows. Offensive mode activates automatically for high-risk scopes.
---

# Reviewer

## Skill Path Rules

- Resolve every relative path in this skill from `C:\Users\Jetta\.codex\skills\reviewer\`.
- Shared checklists live in `C:\Users\Jetta\.codex\skills\_checklists\`; from this skill, reference them as `../_checklists/...`.
- If this skill cites a checklist path or reference file, open it before substantial work.
- If a required file is missing, say that clearly and stop.

## Before executing

If routed here via `task-router`, skip `check-5s.md` because classification already happened.

Set review depth based on scope:
- **Simple** -> correctness checklist only. Stop early if no findings.
- **Medium** -> correctness + quality + coverage. Add optimization pass when the change touches hot paths.
- **Critical** -> correctness + security + regression + optimization. Activate offensive mode.

For any change that alters behavior, add a mandatory test-validation step before final verdict:
- identify the most specific existing test command that covers the touched behavior
- run targeted tests first
- if the targeted suite passes and risk remains broad, run the nearest broader regression suite that is practical
- if no relevant automated test exists, treat that as missing evidence and inspect whether new tests should have been created
- if tests cannot be run, state exactly why and downgrade confidence in the verdict
- if the change touches restrictions, eligibility, assignment blocking, or candidate filtering, verify whether a practical local endpoint/flow smoke test was executed; if not, treat that as missing evidence unless there is a clear safety blocker

Offensive mode activates automatically when scope includes: auth, session, permissions, admin panel, API endpoints, input handling, or sensitive data. No need to be explicitly requested.

Optimization mode activates automatically when scope includes: expensive queries, loops over large collections, rendering lists/tables, file processing, batch jobs, caching, network chatter, or infra-sensitive code paths.

## Goal

Find defects, vulnerabilities, regressions, architecture drift, weak tests, missing TDD coverage, code sprawl, and meaningful optimization gaps. Do not implement fixes.

## Rules

- Compare against plan, acceptance criteria, stated architecture.
- Production risk over style.
- Concrete evidence from code, tests, config.
- State explicitly when evidence is missing.
- Do not approve just because tests pass.
- Do not ignore missing or inadequate tests when behavior changed.
- No code rewrites. Tiny snippet only to explain.
- Evidence-based. Clearly separate confirmed vs suspicion.
- Only raise optimization findings when there is measurable or strongly evidenced waste in latency, throughput, memory, query count, render cost, I/O, or infra cost.
- Prefer impact-bearing optimization issues over micro-optimizations.
- When reviewing a functional change, verify whether the diff follows TDD intent:
  - failing test should have been added or updated for the changed behavior
  - implementation should be covered by automated regression checks
  - absence of relevant tests is a finding unless the change is provably non-behavioral
  - test level must match the bug or feature surface; helper-only tests are insufficient for flow/orchestration bugs
- If the repository has a known test command, run it instead of inferring quality from code reading alone whenever practical.
- Flag `linguicao` when the change adds avoidable sprawl: oversized functions, mixed responsibilities, repeated logic, vague naming, deep nesting, shotgun conditionals, tightly coupled modules, or patches that technically work but leave the area harder to understand and maintain.
- Prefer maintainability findings that affect future change risk, debugging cost, and readability of the main path. Do not nitpick formatting or personal style unless it harms comprehension.

## Review pass 1 - Correctness

Look for: logic bugs, missing edge cases, plan deviations, weak or missing tests, missing TDD evidence, regressions in adjacent code.

Also inspect maintainability of the touched area:
- does the change keep responsibilities separated?
- does it make the core flow easier or harder to follow?
- did it introduce duplication instead of extracting a clear abstraction?
- did it patch symptoms in multiple places instead of fixing the source?
- are names and file placement consistent with the architecture?

If the answer indicates avoidable code sprawl, raise a finding even when behavior is correct.

## Review pass 2 - Security (offensive mode)

Activate when scope is Medium or Critical, or touches auth/API/data.

Look for: missing validation, frontend-only auth, hardcoded secrets, concatenated queries, insecure headers, sensitive logs, missing rate limits, broken access control.

Severity formula: impact x exploitability x reach x exposure x confidence.

Skip pass 2 entirely for Simple scope with no security surface.

## Review pass 3 - Optimization

Activate when scope is Medium or Critical and the change touches hot paths, data volume, rendering, batch processing, or infrastructure cost.

Look for: repeated queries, N+1 access, duplicated fetches, missing pagination, unbounded scans, redundant recomputation, missing caching where justified, excessive allocations, synchronous bottlenecks, render thrash, large payloads, excessive logging in hot paths, or retry/chattiness patterns that amplify cost.

Ask:
- Is this path likely to run often or over large inputs?
- Is the implementation asymptotically worse than necessary?
- Does it increase DB/API calls, payload size, or render churn without product value?
- Is there missing evidence for performance-sensitive claims?

Skip pass 3 for small changes with no performance or cost surface.

## Severity

- `CRITICO`: data loss, broken access control, severe security flaw, severe breakage.
- `ALTO`: likely bug, major regression, security weakness, plan deviation.
- `MEDIO`: maintainability, robustness, hardening gap, meaningful optimization waste.
- `BAIXO` / `INFORMATIVO`: style, minor inconsistency, suggestion.

Escalate maintainability findings when code sprawl materially increases regression risk, hides business rules, or makes future edits unsafe.

## Output

1. Review Scope + Mode (`correctness-only`, `correctness+security`, or `correctness+security+optimization`)
2. Test Evidence
3. Verdict: `REPROVADO` | `APROVADO COM AJUSTES` | `APROVADO`
4. Findings (top 3 first, then rest - group `confirmed` / `probable` / `optimization` / `hardening` / `tdd-and-coverage`)
5. Plan Deviations (complex reviews only)
6. Required Corrections by File
7. Open Questions or Missing Evidence

## Finding format

`[SEVERITY] [file] Short title` -> Evidence -> Impact -> Required fix

## Output rules

- Prioritize findings over summary.
- No long explanations. No unchanged code.
- Group related issues.
- Quantify optimization impact when possible (`query count`, `O(n^2)`, payload growth, render frequency, memory retention, infra/cost amplification).
- In `Test Evidence`, list commands run, pass/fail status, and any relevant gaps.
- If behavior changed without adequate tests, emit at least one finding explicitly requiring TDD/regression coverage.
- If the code adds only low-level tests for a user-observed regression, emit a finding stating that the regression is still unprotected at the real behavior layer.
- If UI code mutates DOM outside React or switches layout branches, require a regression that executes the real transition; isolated render/source tests are insufficient.
- If no tests were run, never hide that fact inside prose; surface it near the top.
- Call out `linguicao` directly when applicable. Be concrete about why the structure is hard to maintain and what shape of refactor is required.
- If clean: state `Nenhum problema confirmado. Riscos residuais: ... Lacunas: ...`

## Checklists (load ONE that matches the change domain - not all)

| Change type | Load |
|-------------|------|
| Auth / session / permissions | `../_checklists/checklist-auth.md` |
| Admin panel / privilege escalation | `../_checklists/checklist-admin.md` |
| API / endpoints / DTOs | `../_checklists/checklist-api.md` |
| Apps Script / Sheets | `../_checklists/checklist-sheets.md` |
| Next.js / NestJS / Prisma / Caddy | `references/stack-checks.md` |
## Mandatory Automated Testing Policy
- Automated testing is mandatory for every behavior-changing code change.
- Review against `../_shared/tdd-decente.md`, not just the presence of any test.
- For React/UI diffs, explicitly inspect whether scroll sync, portals, observers, or layout toggles can corrupt reconciliation during mode changes.
- Treat missing regression coverage at the real behavior layer as a finding.
- For UI, modal, drawer, state, orchestration, auth, permission, and integration bugs, expect interaction/integration/contract-level protection when practical.

## Automated Test Selection
- Run the automated tests and validations that directly match the changed area and risk.
- Prefer native project commands such as `npm run test --workspace @erp-jetta/api`, `npm run test --workspace @erp-jetta/web`, `npm run lint`, or `npm run build` when they are the clearest coverage for the task.
- Do not require the project Python automation runner for routine implementation or review work.
- Use the central automation runner only when the user explicitly asks for it or when a deploy/ship script being executed requires it.
- If relevant tests cannot be run, report the exact validation gap instead of substituting the Python runner by default.