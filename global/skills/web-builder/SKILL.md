---
name: web-builder
description: Build web systems incrementally with backend-first security, TDD, and polished UI.
---

# Web Builder

## Skill Path Rules

- Resolve every relative path in this skill from `C:\Users\Jetta\.codex\skills\web-builder\`.
- Shared checklists live in `C:\Users\Jetta\.codex\skills\_checklists\`; from this skill, reference them as `../_checklists/...`.
- The TDD workflow lives in `tdd/` inside this skill. Read it before any code change that can be tested.
- The cross-skill TDD standard lives in `../_shared/tdd-decente.md`. Read it together with `tdd/README.md` before any behavior-changing code.
- The review gate lives in `review/` inside this skill. Read it before delivery.
- If this skill cites a checklist path, script path, or reference file, open and run it before substantial work.
- If a required file is missing, say that clearly and stop assuming it should be resolved from the project workspace.

## Before executing

If routed here via `task-router`, skip `check-5s.md` " classification already done.
Otherwise: is this simple + non-critical + no plan needed? Resolve directly without loading references.

## Workflow

1. Restate target in technical terms.
2. Split into smallest verifiable slice.
3. Ask only when ambiguity affects: schema, auth, destructive ops, or materially different UX.
4. Define acceptance checks before coding.
5. TDD is mandatory: follow `tdd/README.md` and do not skip the red step.
6. Smoke test: lint, typecheck, targeted tests, runtime check.
7. Run the local review gate in `review/` before handing off.
8. Validate against relevant `../_checklists/`.
9. If the change affects restrictions, eligibility, assignment blocking, or candidate selection, run a practical endpoint/flow smoke in local environment when safe.

## TDD Rules (mandatory)

- Always use the local `tdd/` guidance for test-first work.
- Always enforce `../_shared/tdd-decente.md`; local TDD steps do not override the stronger behavior-first rule.
- Always create or update a relevant automated test before editing production code.
- Run the targeted test before the code change and confirm the failing state.
- Only then implement the minimum production change needed.
- Run the targeted tests again after the code change and confirm they pass.
- If a test cannot be added or executed, say so explicitly before proceeding.

## Review Rules (mandatory)

- Read `review/README.md` before delivery.
- Do a self-review after implementation and after tests pass.
- Compare the result against the request, acceptance criteria, and adjacent code.
- Look specifically for correctness gaps, regressions, weak tests, and security or permission assumptions.
- If the change touches auth, API, permissions, or sensitive data, perform a reviewer-style pass before delivery.
- If the review finds an issue, fix it or explain the blocker before handing off.

## Patch mode (mandatory)

- Return only changed code, not full files.
- Prefer diff/patch format.
- Never rewrite unchanged sections.

## Security

- Backend = source of truth. Never trust frontend.
- Re-validate all input server-side.
- Enforce permissions on backend.
- Validate against `../_checklists/checklist-auth.md` and `../_checklists/checklist-api.md` when relevant.

## Mandatory Practical Validation For Restriction Logic

When the change touches:

- blocked regions
- blocked weekdays
- daily delivery caps
- temporary operational windows
- manual or automatic assignment eligibility
- any rule that causes the system to choose, skip, ignore, or reject a driver

you must validate at least one real local flow or endpoint call in addition to automated tests, when a safe local environment exists.

Minimum bar:

- prove one allowed case when relevant
- prove one blocked/ignored case for each changed restriction type when practical

Use seeded/local accounts and clean up temporary rules after the smoke test.

## UI

- Modern, intentional, usable.
- Stable libraries only with purpose.
- Meaningful motion. Accessible. Responsive.
- For initial page loading states, do not use explicit loading copy as the primary visible state when a silent placeholder is practical.
- Prefer skeletons/placeholders that preserve the final layout geometry over text like `Carregando...`.
- Do not let the initial loading state look like a real empty state such as `0 itens` / `nenhum resultado` before data resolves.
- For UI loading bugfixes, require a regression test on the real rendered branch that proves the loading copy is absent and the placeholder state is present.

## Output rules

- No unchanged code in response.
- No long explanations. Max objectivity.
- Prefer patch/diff over full file rewrites.

## References (load only when needed)

- `references/ui-research.md` " only for new visual components or redesigns, not for logic/patch changes.
- `references/validation-and-security.md` " test coverage and hardening.
- `../_shared/tdd-decente.md` " required TDD quality bar for behavior changes.
- `../_checklists/checklist-api.md` " API changes.
- `../_checklists/checklist-auth.md` " auth changes.
## Mandatory Automated Testing Policy
- Automated testing is mandatory for every behavior-changing code change.
- The minimum acceptable standard is `../_shared/tdd-decente.md`.
- A unit test alone is not sufficient when the bug or feature lives in orchestration, UI flow, permission boundaries, or module interaction.
- For bugfixes, require a regression test for the reported scenario or an equivalent reproduced state.
- For UI/state changes, require at least one interaction or flow-level test whenever that is the lowest practical level that can catch the regression.
- For React/UI mode switches or imperative DOM enhancers, require a test that crosses the real transition path and can fail with reconciliation/runtime errors.
- If only lower-level coverage is possible, state the missing higher-level protection explicitly as residual risk.
## Automated Test Selection
- Run the automated tests and validations that directly match the changed area and risk.
- Prefer native project commands such as `npm run test --workspace @erp-jetta/api`, `npm run test --workspace @erp-jetta/web`, `npm run lint`, or `npm run build` when they are the clearest coverage for the task.
- Do not require the project Python automation runner for routine implementation or review work.
- Use the central automation runner only when the user explicitly asks for it or when a deploy/ship script being executed requires it.
- If relevant tests cannot be run, report the exact validation gap instead of substituting the Python runner by default.