---
name: ship-vps
description: "Commit, push, deploy to the staging VPS, and validate a feature with real end-to-end evidence. Use when Codex needs to turn finished work into a tested staging rollout: verify the workspace, run relevant tests, create a clean commit, push the branch, update the staging environment safely, confirm service health, and validate the feature in practice before any production promotion."
---

# Ship VPS

## Overview

Ship completed work to the test environment with operational discipline. This skill exists for the full delivery path from local change to staging validation on the VPS, with evidence at every stage.

Treat deployment as incomplete until the feature works in the real staging environment. Passing local tests and a successful push are necessary, not sufficient.

This skill is for `ambiente de teste` only. Do not use it to deploy directly to production.

## Operating Principles

- ship only from a verified workspace
- prove the feature on localhost before touching staging
- commit only scoped, intentional changes
- push before touching the VPS
- deploy to staging with the smallest safe blast radius
- validate the real feature after deployment
- if verification fails, diagnose, patch, redeploy, and retest

Staging is the proving ground. Production promotion is a separate decision and a separate skill.

## Preconditions

Before doing anything destructive or external, confirm or discover:

- the target git branch
- the relevant test commands
- the staging VPS access path and deploy method
- the staging service names or process manager
- the feature to validate after deploy
- the safest real environment available: localhost, staging VPS, test user, seeded account, sandbox credentials

When the repository has local test credentials in `.env`, prefer reusing them instead of asking again. In this project, use:

- `TEST_LOGIN_EMAIL`
- `TEST_LOGIN_PASSWORD`

Treat these as runtime secrets for validation only. Use them to prove real login flows after deploy, but never print the raw password in the final report.

If the staging VPS or deploy method is unknown, inspect repository docs, scripts, CI files, process files, and shell history before asking for help.

For environment and rollout decisions, read [references/deploy-discovery.md](references/deploy-discovery.md).

## Repository Default

When this repository contains `tools/codex-ship-staging.ps1`, treat it as the default staging ship entrypoint.

For this repository, localhost is a mandatory pre-deploy gate. Do not treat unit tests or build success as a substitute for localhost smoke evidence.
The project staging ship script is expected to run the Python automation hub, recover localhost when needed, execute localhost smoke first, push the current branch, and only then tell the staging VPS to deploy that exact branch.

Default execution order for this project:

1. inspect workspace and stage only intended changes
2. run the required automated validation
3. bring localhost up to date and healthy
4. run localhost smoke and prove the feature locally
5. if localhost smoke fails, fix locally, retest, and only continue once it passes
6. commit and push explicitly
7. execute `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\tools\codex-ship-staging.ps1`
8. review its deploy and smoke evidence
9. only fall back to manual staging VPS commands if that script is missing or fails in a way that requires direct diagnosis

Do not bypass this project script just because you know the manual steps. Prefer improving the script when you discover new deploy drift so the next staging ship is easier and safer.

## Primary Workflow

### 1. Verify the workspace

Inspect the current diff before committing.

- check `git status`
- identify unrelated changes
- confirm the branch
- understand which files belong to the feature

Do not accidentally commit unrelated local work. If the worktree is dirty beyond the requested feature, stage only the intended files.

### 2. Prove local safety first

Run the smallest relevant validation before commit:

- targeted tests for the changed behavior
- broader regression tests when the risk surface is larger
- build or typecheck if the stack depends on it

If the feature was supposed to follow TDD, make sure the protecting tests exist and pass before shipping.
Protecting tests must satisfy `../_shared/tdd-decente.md`; localhost smoke does not excuse weak regression coverage.
For React/UI fixes with imperative DOM mutation or layout switches, do not ship until tests cover the real mode transition, not only the destination render.

For validation depth, read [references/preflight-gates.md](references/preflight-gates.md).

### 2.5. Force localhost into a shippable state

Before any staging deploy, verify the local app is actually running and current on:

- `http://localhost:3000`
- `http://localhost:3001/api/health`

If localhost is down, stale, or clearly not reflecting the current branch, recover it instead of skipping ahead.

For this repository, prefer these recovery actions:

1. use `powershell -ExecutionPolicy Bypass -File .\tools\start-erp.ps1` to restart the local stack
2. let the script rebuild/restart the local API and web services
3. if the app is still stale or broken, diagnose the blocking issue locally and fix it before continuing

Do not deploy to staging from an unproven localhost state.

### 3. Create the commit

Stage only the intended files. Then create a direct commit message that reflects the shipped behavior.

Commit rules:

- no vague messages
- no mixed-purpose commits
- no hidden unfinished work
- no commit if preflight evidence is weak

If the repo uses conventional commits or another house style, follow it.

### 4. Push cleanly

Push the branch after the commit succeeds.

- confirm the remote target
- push the current branch explicitly
- if the branch is new, publish it with upstream
- verify the push actually succeeded

Do not proceed to staging deployment with local-only history.

### 5. Deploy to staging safely

Use the repository's real staging path instead of inventing one. Prefer existing scripts or documented flows.

For this repository specifically:

- prefer `tools/codex-ship-staging.ps1` as the first deployment command
- treat `tools/vps-bootstrap-staging.ps1` and `tools/codex-vps-smoke.ps1` as lower-level building blocks, not the default first choice
- expect staging deployment to target the test environment on the VPS, not `www.ciadm.com.br`
- if the higher-level ship script fails, inspect whether the failure belongs in:
  - local validation or push
  - remote staging bootstrap
  - runtime remediation on the staging VPS
  - post-deploy smoke verification
- if you fix recurring deploy friction, encode that fix back into the project script rather than keeping it as tribal knowledge

Typical deployment sequence:

1. connect to the correct staging VPS target
2. update the right staging working tree or release directory
3. pull the pushed branch or checkout the target revision
4. install or sync dependencies if needed
5. run migrations only when required and safe
6. build assets or binaries if the stack requires it
7. restart or reload the staging services through the proper process manager
8. confirm service health before feature validation

Examples of valid process managers and surfaces:

- `pm2`
- `systemd`
- Docker Compose
- custom deploy shell scripts

Do not improvise a restart command if the project already encodes the correct method.

For VPS rollout details, read [references/vps-deploy-patterns.md](references/vps-deploy-patterns.md).

### 6. Validate the feature in practice

Localhost validation comes first, staging validation comes second.

Before the staging rollout, execute a localhost smoke flow that proves the actual feature on the machine running the change.

For this repository, prefer:

- `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\tools\codex-vps-smoke.ps1 -SkipSsh -WebUrl http://localhost:3000 -ApiUrl http://localhost:3001/api`

If localhost smoke fails:

- do not continue to staging
- reproduce locally
- identify the narrowest cause
- patch locally
- rerun the required automated checks
- rerun localhost smoke
- only continue after localhost smoke passes

After deploy, switch into `na-pratica` behavior:

- define the exact real flow to execute
- use staging as the highest-risk target allowed by this skill
- observe actual outputs, side effects, pages, logs, webhooks, emails, or database effects
- verify the feature, not just the process status

If the shipped change touches authentication or session behavior:

- first verify health and public reachability
- then exercise the real login flow using `TEST_LOGIN_EMAIL` and `TEST_LOGIN_PASSWORD` from the local `.env` when available
- if the bug involved login failure semantics, explicitly verify the expected status code or redirect outcome
- prefer proving both the negative case and the happy path when safe

If those env vars are missing, discover another safe test account from repository context or stop and report the missing credential as a blocker instead of inventing one.

Success means observed behavior in staging. A healthy service with a broken feature is not a success.

Success also requires observed behavior on localhost first. Staging is not the first debugger.

For real-world validation rules, read [references/post-deploy-verification.md](references/post-deploy-verification.md).

### 7. Close with evidence

Report:

1. commit created
2. branch pushed
3. staging target and deploy action performed
4. health checks and feature checks executed
5. observed result
6. residual risk or blocked verification before production promotion

Keep it factual. Shipping to staging is proved by outcomes.

## Failure Handling

If anything fails, stop the rollout from drifting.

### Commit or push failed

- fix the local issue
- rerun the necessary tests
- recommit or push again

### Staging deploy failed

- inspect the failing step directly
- collect the minimal logs needed
- fix only the blocking issue
- redeploy from the same verified branch

### Feature failed after staging deploy

- reproduce on the staging environment
- identify the narrowest cause
- patch locally
- prove the fix on localhost again
- rerun preflight checks
- commit, push, redeploy to staging, and retest

Do not claim completion while the staged feature still fails.

## Safety Rules

- avoid production-destructive operations without necessity
- prefer staged verification, test accounts, and reversible actions
- do not run migrations blindly
- redact secrets in logs and outputs
- verify the target host and directory before pulling or restarting anything
- if a deploy is risky and the rollout path is ambiguous, stop and reduce uncertainty first
- if the task is actually to publish to production, stop using this skill and switch to `$ship-prod-vps`

## Anti-Patterns

Do not:

- commit without testing
- push code you did not inspect
- deploy from uncommitted local state
- skip localhost smoke and use staging as the first validation target
- assume `git pull` in any random directory is the right deploy
- trust a process restart as proof of feature success
- skip real verification because local tests passed
- bury a broken deploy under new commits without identifying the actual cause
- use this skill to change `www.ciadm.com.br` directly

## References

Read only what helps the current delivery:

- [references/deploy-discovery.md](references/deploy-discovery.md): use when the repository or staging rollout path is unclear
- [references/preflight-gates.md](references/preflight-gates.md): use when deciding which tests and checks are mandatory before shipping
- [references/vps-deploy-patterns.md](references/vps-deploy-patterns.md): use when deploying through systemd, pm2, docker, or shell scripts
- [references/post-deploy-verification.md](references/post-deploy-verification.md): use when validating the feature with real evidence like na-pratica

## Mandatory Automated Testing Policy

- Automated testing is mandatory for every behavior-changing code change before shipping.
- Follow `../_shared/tdd-decente.md` as the minimum bar for release readiness.
- If the bug involved `table/grid`, portal/inline, or any DOM enhancer outside React, require one practical click-through on the real transition before release.
- Do not ship a fix that only has helper-level coverage when the regression lives in UI flow, orchestration, permission, or integration behavior.
- Smoke evidence complements automated coverage; it does not replace missing regression tests.

## Automated Test Selection
- Run the automated tests and validations that directly match the changed area and risk.
- Prefer native project commands such as `npm run test --workspace @erp-jetta/api`, `npm run test --workspace @erp-jetta/web`, `npm run lint`, or `npm run build` when they are the clearest coverage for the task.
- Do not require the project Python automation runner for routine implementation or review work.
- Use the central automation runner only when the user explicitly asks for it or when a deploy/ship script being executed requires it.
- If relevant tests cannot be run, report the exact validation gap instead of substituting the Python runner by default.