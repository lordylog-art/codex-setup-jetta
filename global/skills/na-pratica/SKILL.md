---
name: na-pratica
description: Validar na pratica o que foi implementado com testes reais de ponta a ponta, baixo gasto de tokens e foco em seguranca e funcionalidade. Use quando Codex precisar executar o fluxo real de uma feature, integracao ou automacao, observar o resultado concreto, corrigir falhas e repetir ate funcionar com evidencias.
---

# Na Pratica

## Skill Path Rules

- Resolve every relative path in this skill from `C:\Users\Jetta\.codex\skills\na-pratica\`.
- Shared checklists live in `C:\Users\Jetta\.codex\skills\_checklists\`; from this skill, reference them as `../_checklists/...`.
- If this skill cites a checklist path, script path, or reference file, open and run it before substantial work.
- If a required file is missing, say that clearly and stop assuming it should be resolved from the project workspace.

## Before executing

If routed here via `task-router`, skip `check-5s.md` " classification already done.
Define the smallest real-world check that can prove the implementation works.

## Goal

Provar o comportamento implementado no uso real, com o menor contexto possivel, sem confiar apenas em leitura de codigo ou em "parece certo".

## Workflow

1. Restate the user flow in one sentence.
2. Choose the safest real execution target available: local, sandbox, staging, test account, fake inbox, seeded data.
3. Define success evidence before running anything: response, side effect, log, database change, received email, rendered page, webhook delivery.
4. Execute the real flow end to end.
5. Inspect the observed result, not just command exit codes.
6. If it failed, isolate the smallest plausible cause, patch only that slice, and rerun the same real check.
7. Repeat until the observed result matches the expected outcome.
8. Finish with concise proof: what was executed, what happened, and what safety checks were confirmed.

## Safety gates

- Prefer test recipients, sandbox credentials, mock payment providers, local webhooks, and staging endpoints.
- Do not send real emails, messages, payments, or destructive writes to production targets without explicit user approval.
- Redact secrets in logs and outputs.
- If the real action is risky, reduce blast radius first: smaller dataset, disposable account, draft mode, or a harmless noop path that still proves the integration.
- Validate relevant hardening, not just happy path behavior.

## Token discipline

- Prefer direct execution and concrete evidence over long reasoning.
- Load only the files needed for the failing slice.
- Use targeted logs, curl requests, CLI calls, screenshots, inbox checks, and focused tests.
- Avoid full-suite runs unless the failing area is unclear or the change is broad.

## Validation depth

- For APIs and integrations, validate `../_checklists/checklist-api.md`.
- For auth, session, or user-bound actions, validate `../_checklists/checklist-auth.md`.
- If a feature can succeed while still being unsafe, treat that as incomplete.
- For restriction, eligibility, or assignment logic, prefer real endpoint calls that prove both a blocked case and a non-blocked case when safe.

## Output rules

- Report only the essential evidence.
- State the real action performed and the environment used.
- If execution was blocked, state exactly what prevented the practical test.
- Do not claim success without an observed effect.
## Mandatory Automated Testing Policy
- Automated testing is mandatory for every behavior-changing code change.
- Follow `../_shared/tdd-decente.md` as the quality bar.
- For React/UI issues with imperative DOM mutation or layout toggles, require a regression on the real transition path before trusting practical validation.
- Real-world validation is required here, but it complements automated regression coverage instead of replacing it.
## Automated Test Selection
- Run the automated tests and validations that directly match the changed area and risk.
- Prefer native project commands such as `npm run test --workspace @erp-jetta/api`, `npm run test --workspace @erp-jetta/web`, `npm run lint`, or `npm run build` when they are the clearest coverage for the task.
- Do not require the project Python automation runner for routine implementation or review work.
- Use the central automation runner only when the user explicitly asks for it or when a deploy/ship script being executed requires it.
- If relevant tests cannot be run, report the exact validation gap instead of substituting the Python runner by default.