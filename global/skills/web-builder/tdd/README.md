# TDD Workflow

This folder exists only for test-driven development instructions.

Read this together with `../_shared/tdd-decente.md`. If they differ, follow the stricter rule.

## Non-negotiable loop

1. Identify the smallest behavior change.
2. Write or update the most relevant automated test first.
3. Run that test and confirm it fails for the expected reason.
4. Implement the minimum production change.
5. Run the same test again and confirm it passes.
6. Run the smallest useful nearby smoke tests if the change has side effects.
7. Refactor only after the green state is stable.

## Rules

- Do not touch production code before a test exists for the behavior.
- Do not claim TDD unless the red phase was actually executed.
- Prefer the narrowest test that proves the behavior.
- Prefer the lowest test level that actually catches the real regression, not the easiest isolated helper to assert.
- If the bug is in flow/orchestration, use integration or interaction coverage instead of hiding behind unit-only tests.
- If the bug involves layout switching or DOM mutation outside the framework reconciler, make the test cross that transition explicitly.
- Keep fixes minimal until the test is green.
- If a test cannot be run, state the blocker before continuing.

## Practical checklist

- Behavior is stated in one sentence.
- Test file is added or updated first.
- Red run is captured and understood.
- Production change is the minimum needed.
- Green run is captured.
- Follow-up smoke checks are planned or executed.
- The chosen test level matches where the bug really lives.
- Bugfixes include a regression case for the reported scenario.
