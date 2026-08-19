# Post-Deploy Verification

Use this reference to validate the feature on the deployed environment in the spirit of na-pratica.

## Core Rule

Deployment is not done until the real feature behavior is observed.

## Verification Ladder

1. confirm service health
2. execute the real feature flow
3. inspect the actual result
4. inspect the relevant side effect
5. inspect logs only as support, not as the primary proof

## Good Evidence

- HTTP response with the corrected behavior
- rendered page showing the expected state
- webhook delivered
- job executed successfully
- database change matching the feature
- email or notification received in a safe test target

## Weak Evidence

- process is online
- deploy command exited with code 0
- no error appeared in the console
- local test passed

## If The Feature Fails

Loop back cleanly:

1. capture the real failing evidence
2. patch locally
3. rerun preflight tests
4. recommit if needed
5. push
6. redeploy
7. revalidate the same real flow
