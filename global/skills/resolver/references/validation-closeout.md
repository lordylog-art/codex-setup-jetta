# Validation Closeout

Use this reference before declaring the review findings resolved.

## Minimum Validation

Always try to provide:

- targeted test command
- result of the targeted command
- broader regression command when practical
- statement of what remains unverified

## Validation Ladder

Run in this order:

1. focused test for the changed behavior
2. file or module suite
3. nearest broader regression suite
4. manual verification only when automation is insufficient

## Diff Sanity Check

Before closing:

- confirm no unrelated files were changed without need
- confirm the fix matches the review finding
- confirm tests express the corrected contract
- confirm no obvious `linguicao` was added while fixing

## Closeout Format

Summarize in compact form:

- `Addressed`: which findings were fixed
- `Root cause`: what actually caused the issue
- `Tests`: what was added or run
- `Validation`: what passed
- `Residual risk`: what is still unknown or intentionally deferred
