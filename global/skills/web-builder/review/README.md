# Review Gate

This folder exists only for pre-delivery review instructions.

## Purpose

Catch the kinds of issues that would normally show up only after a separate reviewer pass.

## Mandatory pass before delivery

1. Re-read the request and acceptance criteria.
2. Compare the final change against the intended behavior.
3. Look for correctness bugs, regressions, missing edge cases, and weak tests.
4. Check whether the change relies on frontend-only checks for anything the backend should enforce.
5. Check whether auth, permissions, validation, or sensitive data handling changed.
6. Confirm the smallest relevant tests were run and actually cover the behavior.
7. Fix confirmed issues before delivering.

## What to flag

- Behavior that can fail on empty, null, duplicate, or concurrent inputs.
- Hidden dependency on client-side enforcement.
- Missing or insufficient tests for the changed path.
- Logic that works only for the happy path.
- Any security or trust-boundary assumption not enforced server-side.

## Exit criteria

- No confirmed defects remain.
- Remaining risks are explicitly called out.
- Any missing evidence is stated, not guessed.
