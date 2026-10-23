---
name: implement-ticket
description: Implement one approved ticket with evidence, review, and selective local commits.
---

# Implement the approved ticket

## Project protocol first

When the checkout contains `.agents/skills/implement/SKILL.md`, read and follow that local protocol; do not also execute the generic checklist below. Use the current user decisions and proportional delivery policy. A missing JSON/controller or test runtime does not prevent safe coding against a known contract; keep the affected proof/activation pending. Prefer automated tests by persona; interactive ERP/browser only for appearance or a demonstrated automation gap.

The remaining sections are the fallback when no project implementation skill exists. Mapping and proof records may stay compact in the existing ticket; do not generate a separate matrix/report by default. Preserve security/data safeguards and external-action permissions.

Deliver the exact approved scope. Do not add features, weaken requirements,
or stop at a plan. Execute routine authorized steps without asking to continue.

## 1. Ground

Read the ticket, applicable AGENTS.md, and relevant existing code.

Record:

- BASE (`git rev-parse HEAD`)
- current branch
- existing working-tree changes
- relevant repository patterns
- affected seams and tests

Preserve unrelated work.

Reuse repository patterns, dependencies, architecture, and commands unless the
ticket explicitly requires changing them.

Do not redesign adjacent systems merely because a different implementation
appears cleaner.

---

## 2. Map

Before editing, map every acceptance criterion and explicit prohibition.

| Requirement | Observable surface | Trigger / precondition | Proof + expected result | Status |
| --- | --- | --- | --- | --- |
| Exact requirement | UI / API / data / artifact | What causes the behaviour | Command or repeatable flow | PENDING |

Include regression checks for existing behaviour your changes could affect.

Do not:

- omit difficult criteria;
- collapse multiple independent criteria into vague proof;
- invent additional requirements;
- treat implementation structure as proof of user-visible behaviour.

Each proof must identify:

- precondition;
- trigger;
- expected state transition;
- observable postcondition.

`Test exists` is not evidence.

---

## 3. Design the proof

Before implementation, design the minimum tests that can falsify each important
requirement.

For every critical test, determine internally:

- What exact behaviour does this test prove?
- What single mechanism causes the observed result?
- What production bug would make this test fail?
- Could the test still pass if the required wiring were removed?
- Is a mock bypassing the behaviour being proved?
- Is another event or mechanism capable of producing the same final state?

A test is invalid evidence if it can pass because:

- test data is mutated directly into the expected result;
- another trigger causes the same behaviour;
- the assertion observes only the final appearance without proving its cause;
- mocked code replaces the production seam being tested;
- the expected state is manually injected rather than produced by the behaviour.

### Test isolation rules

Test one trigger at a time when multiple mechanisms can produce the same result.

Examples:

- midnight timer must be tested without focus or visibility events;
- focus revalidation must be tested without advancing the midnight timer;
- visibility revalidation must be tested separately;
- reload persistence must require a real reload/refetch path;
- optimistic UI must separately prove pending, success, and rollback;
- concurrency must create actual competing operations;
- idempotency must repeat the same operation, not merely inspect a UNIQUE index;
- route integration must not mock the service when proving route → service → DB.

Do not combine independent mechanisms in one test when either mechanism alone
could make the assertion pass.

### State-transition tests

When a requirement describes a transition, assert both sides.

Example:

`future → eligible`

Prove:

1. before boundary: future=true and control disabled;
2. trigger only the specified boundary;
3. after boundary: future=false and control enabled.

Similarly:

`pending → completed`

Prove:

1. pending state;
2. user action;
3. persistence in-flight state if relevant;
4. completed state after success.

And for failure:

1. previous persisted state;
2. optimistic local change;
3. persistence failure;
4. rollback to previous persisted state;
5. control becomes usable again;
6. error appears at the correct surface.

Do not infer a transition from only its final state.

### Counterfactual check

For critical acceptance criteria, verify that the proof would fail if the
required behaviour were removed or bypassed.

Prefer one of:

- test-first red state before implementation;
- temporarily disable the relevant wiring and observe test failure;
- inspect the test structure and verify no alternate path can satisfy it.

Do not commit deliberate breakage used for this check.

If a test would still pass after removing the behaviour it supposedly proves,
the test is insufficient and must be strengthened.

### Mock discipline

Mocks may control:

- time;
- external systems;
- network failures;
- authentication fixtures;
- deterministic dependencies.

Mocks must not simulate the result that production code is supposed to cause.

Bad:

- mutate returned data manually and then assert UI updated;
- fire several refresh triggers and assert that refresh happened;
- mock service return values when proving route → service → DB;
- mark an item completed in the fixture after click and call that persistence proof;
- directly replace server-derived timezone output with the desired final date.

Good:

- expose a controlled clock;
- count actual reload/refetch calls;
- resolve or reject a pending request explicitly;
- use real route + real service + local DB for integration seams;
- query persisted state after the operation;
- compare state before and after the real trigger.

Use the highest real surface required by the criterion.

---

## 4. Implement

Work in small, complete slices:

`inspect → change → focused test → inspect diff`

Use `/tdd` where the seam is pre-agreed or where a behaviour is sufficiently
isolated to benefit from red → green.

Run focused tests and affected typechecking regularly.

Fix introduced failures before stacking further changes.

Complete required wiring and integration.

Do not leave:

- disconnected components;
- required-behaviour TODOs;
- fake success paths;
- disabled checks;
- weakened assertions;
- tests that only validate mocks;
- production code added solely to satisfy a test fixture.

Prefer the smallest implementation that satisfies the approved ticket.

Do not advance blocked or future tickets.

---

## 5. Persist and prove

On errors:

1. reproduce;
2. inspect diagnostics;
3. identify the failing seam;
4. attempt a safe fix;
5. re-run the smallest relevant proof.

After two unsuccessful fixes, gather new evidence instead of guessing.

Escalate only genuine missing:

- access;
- authority;
- capability;
- product decision;
- external dependency.

Continue independent safe work whenever possible.

Never silently reduce scope.

### Evidence standard

Validate the actual required surface.

Unit tests cannot prove:

- real UI behaviour;
- permissions;
- route wiring;
- persistence;
- integration;
- concurrency;
- generated artifacts;
- responsive or visual behaviour.

Use the authenticated local ERP when the criterion requires its real surface.

PASS requires observed results, not plausible code.

Record actual commands or repeatable flows and their outcomes.

Invalidate previous evidence when relevant implementation changes.

### Evidence integrity

A passing test counts only if:

- it exercises the intended seam;
- its setup does not pre-create the expected result;
- no alternate trigger can satisfy the assertion;
- the assertion observes the requirement directly;
- relevant production wiring participates in the test.

For integration criteria, prefer real composition over deep mocks.

For persistence criteria, verify persisted state after reload/refetch.

For concurrency criteria, create actual overlapping operations.

For timezone/date criteria, fix the instant and prove the resulting civil date.

For retry/idempotency criteria, repeat the same operation and verify the same
semantic result without duplication.

For loading criteria, prove both:

- stale/incorrect state is not shown;
- final state appears only after the load/revalidation completes.

---

## 6. Sync acceptance criteria

After an acceptance criterion passes, check its matching GitHub checkbox:

```powershell
python C:\Users\caila\.agents\skills\implement\scripts\sync_issue_acceptance.py <issue> --criterion "<criterion copied verbatim>" --apply --close-when-complete
