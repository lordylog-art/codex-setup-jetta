# Preflight Gates

Use this reference before commit and before deploy.

## Minimum Gates

- relevant tests for the changed feature
- broader regression checks when the blast radius is not local
- build or typecheck if the project requires it
- review of staged files

## Stronger Gates For Risky Changes

Add more checks when the change touches:

- authentication
- billing
- background jobs
- database writes
- public APIs
- shared framework code

In these cases, prefer:

- targeted tests
- one broader suite
- smoke startup validation

## Commit Gate

Do not commit if:

- the change is partially understood
- the relevant tests are red
- staged files include unrelated work
- the feature still lacks basic coverage where expected

## Deploy Gate

Do not deploy if:

- push failed
- the target branch is unclear
- the VPS target is ambiguous
- the restart path is uncertain
- the success signal for the feature is undefined
