# TDD Remediation

Use this reference when the review found weak, missing, or outdated tests.

## Core Rule

Behavior change without automated coverage is incomplete.

Read this together with `../_shared/tdd-decente.md`. The goal is not just "some test", but a test that can really detect the regression.

## Preferred Sequence

1. identify the exact behavior to protect
2. find the closest existing test file or test layer
3. add or update a test that should fail before the fix
4. confirm the failure or the missing assertion gap
5. implement the code change
6. rerun the targeted suite
7. run the nearest broader regression suite

## If A Failing Test Is Hard To Produce

Use the strongest valid fallback:

- add assertion coverage to the nearest existing test
- add an integration test instead of a unit test
- add a regression test around the public behavior
- if the bug is in UI flow or orchestration, add an interaction/integration test instead of only validating helpers
- if the bug involves layout switching or DOM mutation outside the framework reconciler, make the test execute that transition explicitly
- if the bug was user-reported, prefer reproducing the reported scenario or a state-equivalent scenario
- document exactly why the harness could not expose the failure before the fix

Do not skip coverage just because the test setup is inconvenient.

## Coverage Quality Checks

Good remediation tests:

- fail for the right reason
- assert the contract, not implementation trivia
- cover the bug path and at least one nearby edge
- stay readable

Weak remediation tests:

- only snapshot the whole object without intent
- mirror implementation branches line by line
- assert nothing meaningful about the bug

## Closeout

A finding about missing TDD is only resolved when relevant automated coverage exists and passes.
A finding is not resolved when the added test cannot catch the real regression surface.
