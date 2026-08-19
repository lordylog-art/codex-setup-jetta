---
name: ship-prod-vps
description: "Promote a verified branch to the production VPS and validate the live environment with real end-to-end evidence. Use when Codex needs to take a change that already passed localhost and staging, publish it to production safely, confirm health on the official domain, and report the live result with rollback-aware discipline."
---

# Ship Prod VPS

## Overview

Promote verified work to production with explicit caution. This skill starts after the change is already proven locally and in the test environment, and it ends only when the live production flow is validated with real evidence.

Production is not the place to discover basic breakage. If localhost or staging proof is missing, stop and recover that evidence first.

## Operating Principles

- promote only from a verified branch
- require localhost proof before production
- require staging proof before production
- push before touching production
- deploy with the smallest safe blast radius
- validate the real production feature after rollout
- if production verification fails, diagnose, patch locally, and decide between rollback or forward-fix explicitly

## Preconditions

Before changing production, confirm or discover:

- the target git branch and pushed revision
- the evidence that localhost validation passed
- the evidence that staging validation passed
- the production VPS access path and deploy method
- the production service names or process manager
- the exact user flow to validate after deploy
- the safest real production check that proves success without unnecessary destructive writes

When the repository has local test credentials in `.env`, prefer reusing them instead of asking again. In this project, use:

- `TEST_LOGIN_EMAIL`
- `TEST_LOGIN_PASSWORD`

Use them only if they are safe for production verification. Never print the raw password in the final report.

If the production path is unknown, inspect repository docs, scripts, CI files, process files, and shell history before asking for help.

Use the references from `../ship-vps/references/` when needed.

## Repository Default

When this repository contains `tools/codex-ship-vps.ps1`, treat it as the default production ship entrypoint.

For this repository:

- `tools/codex-ship-staging.ps1` is the staging path
- `tools/codex-ship-vps.ps1` is the production path
- `www.ciadm.com.br` is the live verification target
- `http://50.62.183.82` is not the production success signal

Default execution order for this project:

1. inspect workspace and stage only intended changes
2. verify localhost evidence exists and is still relevant
3. verify staging evidence exists and is still relevant
4. run the required automated validation
5. commit and push explicitly
6. execute `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\tools\codex-ship-vps.ps1`
7. review deploy and smoke evidence on production
8. validate the live flow on `https://www.ciadm.com.br`
9. only fall back to manual production commands if the script is missing or fails in a way that requires direct diagnosis

## Primary Workflow

### 1. Verify readiness

Inspect the current diff before committing.

- check `git status`
- identify unrelated changes
- confirm the branch
- confirm the change is already proven in staging

Do not accidentally commit unrelated local work. If the worktree is dirty beyond the requested feature, stage only the intended files.

Do not proceed if staging proof is missing.

### 2. Reconfirm automated safety

Run the smallest relevant validation that still protects the production risk:

- targeted tests for the changed behavior
- broader regression tests when the risk surface is larger
- build or typecheck if the stack depends on it

If the feature was supposed to follow TDD, make sure the protecting tests exist and pass before production.
Protecting tests must satisfy `../_shared/tdd-decente.md`.

If localhost proof or staging proof is stale relative to the new diff, re-run them before production.

### 3. Create the commit

Stage only the intended files. Then create a direct commit message that reflects the shipped behavior.

Commit rules:

- no vague messages
- no mixed-purpose commits
- no hidden unfinished work
- no commit if preflight evidence is weak

### 4. Push cleanly

Push the branch after the commit succeeds.

- confirm the remote target
- push the current branch explicitly
- if the branch is new, publish it with upstream
- verify the push actually succeeded

Do not proceed to production deployment with local-only history.

### 5. Deploy to production safely

Use the repository's real production path instead of inventing one. Prefer existing scripts or documented flows.

For this repository specifically:

- prefer `tools/codex-ship-vps.ps1` as the first production deployment command
- treat lower-level VPS scripts as building blocks, not the default first choice
- expect the production rollout to target the live site and the production PM2 processes
- if the higher-level ship script fails, inspect whether the failure belongs in:
  - local validation or push
  - remote production bootstrap
  - runtime remediation on the VPS
  - post-deploy smoke verification

Typical deployment sequence:

1. connect to the correct production VPS target
2. update the right production working tree or release directory
3. pull the pushed branch or checkout the target revision
4. install or sync dependencies if needed
5. run migrations only when required and safe
6. build assets or binaries if the stack requires it
7. restart or reload the production services through the proper process manager
8. confirm service health before feature validation

Do not improvise a restart command if the project already encodes the correct method.

### 6. Validate the production feature in practice

After deploy, switch into `na-pratica` behavior with production caution:

- define the exact live flow to execute
- prefer read-only or low-risk validation paths first
- observe actual outputs, side effects, pages, logs, webhooks, emails, or database effects
- verify the feature, not just the process status

If the shipped change touches authentication or session behavior:

- first verify public reachability on `https://www.ciadm.com.br`
- then exercise the real login flow using `TEST_LOGIN_EMAIL` and `TEST_LOGIN_PASSWORD` from the local `.env` when available and safe
- if the bug involved login failure semantics, explicitly verify the expected status code or redirect outcome

Success means observed behavior on the live production domain. A healthy process with a broken feature is not a success.

### 7. Close with evidence

Report:

1. commit created
2. branch pushed
3. production target and deploy action performed
4. health checks and feature checks executed
5. observed result on the live domain
6. residual risk, follow-up, or rollback concern

Keep it factual. Production shipping is proved by outcomes.

## Failure Handling

If anything fails, stop the rollout from drifting.

### Commit or push failed

- fix the local issue
- rerun the necessary tests
- recommit or push again

### Production deploy failed

- inspect the failing step directly
- collect the minimal logs needed
- fix only the blocking issue
- redeploy from the same verified branch

### Feature failed after production deploy

- reproduce on production with the safest practical path
- identify the narrowest cause
- patch locally
- prove the fix on localhost again
- prove the fix on staging again when the risk justifies it
- rerun preflight checks
- commit, push, redeploy, and retest
- if user impact is active and rollback is safer than forward-fix, say that explicitly

Do not claim completion while the production feature still fails.

## Safety Rules

- avoid destructive production operations without necessity
- prefer read-only or reversible production checks first
- do not run migrations blindly
- redact secrets in logs and outputs
- verify the target host, directory, and live domain before pulling or restarting anything
- if rollout risk is ambiguous, stop and reduce uncertainty first
- if the task is only to test or preview a change, use `$ship-vps` instead

## Anti-Patterns

Do not:

- publish to production before staging proof exists
- use production as the first place to test a new fix
- trust a process restart as proof of feature success
- skip live verification because staging passed
- change production when the branch on origin is not the exact intended revision
- hide rollback risk or user impact in the final report

## References

Read only what helps the current delivery:

- [../ship-vps/references/deploy-discovery.md](../ship-vps/references/deploy-discovery.md)
- [../ship-vps/references/preflight-gates.md](../ship-vps/references/preflight-gates.md)
- [../ship-vps/references/vps-deploy-patterns.md](../ship-vps/references/vps-deploy-patterns.md)
- [../ship-vps/references/post-deploy-verification.md](../ship-vps/references/post-deploy-verification.md)

## Mandatory Automated Testing Policy

- Automated testing is mandatory for every behavior-changing code change before shipping.
- Follow `../_shared/tdd-decente.md` as the minimum bar for release readiness.
- Smoke evidence complements automated coverage; it does not replace missing regression tests.

## Automated Test Selection
- Run the automated tests and validations that directly match the changed area and risk.
- Prefer native project commands such as `npm run test --workspace @erp-jetta/api`, `npm run test --workspace @erp-jetta/web`, `npm run lint`, or `npm run build` when they are the clearest coverage for the task.
- Do not require the project Python automation runner for routine implementation or review work.
- Use the central automation runner only when the user explicitly asks for it or when a deploy/ship script being executed requires it.
- If relevant tests cannot be run, report the exact validation gap instead of substituting the Python runner by default.