---
name: resolver
description: Resolve findings raised by reviewer-style code reviews with direct, professional execution. Use when Codex needs to take a review report, reproduce the issue, add or repair TDD coverage, implement the minimum correct fix, remove code sprawl, rerun relevant tests, and close the problem without creating regressions or new architecture drift.
---

# Resolver

## Overview

Take reviewer findings as execution input, not as discussion material. Convert each approved finding into a verified correction with tests, disciplined scope control, and maintainable code structure.

Optimize for: correctness first, regression protection second, maintainability always. Do not answer findings with cosmetic edits, speculative refactors, or partial fixes that leave the risky area unstable.

## Operating Mode

Work as a remediation skill, not a review skill.

- accept the review findings as the starting contract
- verify the problem in code and behavior before editing
- fix the root cause, not just the visible symptom
- add or update automated tests for changed behavior
- leave the touched area cleaner than it was
- rerun the relevant test surface before closing

If a finding appears incorrect, verify it with evidence before changing code. Do not blindly obey a bad review comment.

## Inputs

Expect some combination of:

- review findings or comments
- failing scenarios
- target files or modules
- expected behavior
- test failures or gaps
- architecture constraints from the project

If the input is incomplete, reconstruct the missing context from the repository before making edits.

## Primary Workflow

### 1. Normalize the finding

Rewrite the issue internally into this structure:

`problem -> evidence -> affected behavior -> expected correction -> proof of done`

For each finding, determine:

- is it confirmed or still needs validation
- is it correctness, TDD/coverage, maintainability, security, or optimization
- what user-visible or system-visible behavior is at risk
- which file is likely the source of truth

If multiple findings exist, order them by dependency and blast radius. Fix foundational problems before derivative ones.

For triage patterns, read [references/finding-triage.md](references/finding-triage.md).

### 2. Reproduce before editing

Before changing code, gather concrete evidence:

- inspect the relevant code path
- inspect existing tests for the behavior
- run the narrowest test command that should expose the problem
- if no test exists, define the failing behavior precisely

Do not skip reproduction just because the reviewer sounded confident. A wrong diagnosis leads to wrong fixes.

### 3. Enforce TDD repair

If behavior is changing, create or update a test first whenever practical.

Default sequence:

1. write or update the test that should fail for the current bug
2. confirm the failure or at least confirm the gap
3. implement the minimal correct fix
4. rerun the targeted tests
5. rerun the nearest practical regression suite

If true test-first is impossible because the harness is broken or the case is untestable at that layer, state the reason explicitly and still add the strongest automated coverage available.

For TDD-specific rules, read [references/tdd-remediation.md](references/tdd-remediation.md).
Also enforce the cross-skill quality bar in [../_shared/tdd-decente.md](../_shared/tdd-decente.md).
If the bug lives in a React/UI transition around imperative DOM mutation or layout switching, require coverage for the real mode change, not isolated renders.

### 4. Fix the source, not the smoke

Prefer a correction that simplifies the system:

- repair the invariant
- centralize duplicated business rules
- reduce branching where possible
- move logic closer to the correct abstraction boundary
- remove dead or conflicting paths exposed by the finding

Avoid "defensive piles" of extra conditionals unless they are the true design requirement.

### 5. Eliminate `linguicao`

When touching a risky area, improve structure enough that the fix is maintainable:

- split oversized or mixed-responsibility functions
- replace duplicated patches with a single clear abstraction
- rename vague or misleading identifiers
- reduce deep nesting and shotgun conditionals
- keep file placement consistent with the architecture

Do not use a review fix as an excuse for broad speculative refactors. Clean only the area needed to make the correction robust and readable.

For refactor discipline, read [references/maintainability-repair.md](references/maintainability-repair.md).

### 6. Validate like a closer

Before considering the task done:

- run the targeted tests for the fixed behavior
- run the broader regression suite that covers adjacent risk, when practical
- verify no previously failing case still reproduces
- confirm the diff matches the finding and did not drift into unrelated work
- if the fix touches restrictions, eligibility, assignment blocking, or candidate filtering, run a practical local endpoint/flow smoke test when safe and report the observed result

If tests cannot run, say exactly what blocked execution and what remains unverified.

For validation standards, read [references/validation-closeout.md](references/validation-closeout.md).

## Decision Rules

### When to push back on the review

Push back only with evidence. Examples:

- the reported bug is not reproducible and the code already enforces the invariant
- the proposed correction would violate architecture or break a stronger contract
- the review comment confuses style preference with a real issue

When pushing back, show the evidence briefly and avoid code churn.

### When to refactor during the fix

Refactor only if at least one is true:

- the current structure prevents a safe fix
- duplication would otherwise increase
- the finding itself is caused by bad separation of responsibilities
- the touched code is too tangled to test reliably without cleanup

If not, keep the change smaller.

### When multiple findings collide

Use this order:

1. broken behavior or data risk
2. security exposure
3. missing tests
4. maintainability / `linguicao`
5. optimization

Still try to add tests before or alongside the implementation for the top items.

## Output

When reporting completion, include:

1. Findings addressed
2. Root cause
3. Tests added or updated
4. Validation run
5. Residual risk or open constraint

Keep it direct. The value is in the correction and proof, not in storytelling.

## Anti-Patterns

Do not:

- patch around the symptom in multiple places
- mark a review item as fixed without running relevant tests
- ignore missing TDD because the change "looks obvious"
- add broad cleanup unrelated to the finding
- preserve ugly structure when a small targeted cleanup would reduce future risk
- silently skip a finding that was not actually resolved
- trust the review comment more than repository evidence

## References

Read only what helps the current fix:

- [references/finding-triage.md](references/finding-triage.md): use when the review contains multiple findings or vague comments
- [references/tdd-remediation.md](references/tdd-remediation.md): use when tests are missing, weak, or need to be written first
- [references/maintainability-repair.md](references/maintainability-repair.md): use when the fix risks becoming `linguicao`
- [references/validation-closeout.md](references/validation-closeout.md): use when preparing final verification and closure
## Mandatory Automated Testing Policy
- Automated testing is mandatory for every behavior-changing code change.
- Follow `../_shared/tdd-decente.md` as the minimum acceptable standard.
- For UI reconciliation bugs, do not close the finding without a regression that crosses the failing branch transition.
- Resolver must prefer regression protection at the level where the bug actually manifests.
- If the defect is user-visible in a flow, permission gate, or integration boundary, helper-only coverage is insufficient by default.
- If the repository cannot support the ideal test layer, say that explicitly and record the missing protection as residual risk.
## Automated Test Selection
- Run the automated tests and validations that directly match the changed area and risk.
- Prefer native project commands such as `npm run test --workspace @erp-jetta/api`, `npm run test --workspace @erp-jetta/web`, `npm run lint`, or `npm run build` when they are the clearest coverage for the task.
- Do not require the project Python automation runner for routine implementation or review work.
- Use the central automation runner only when the user explicitly asks for it or when a deploy/ship script being executed requires it.
- If relevant tests cannot be run, report the exact validation gap instead of substituting the Python runner by default.