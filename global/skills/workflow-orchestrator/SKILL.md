---
name: workflow-orchestrator
description: Orquestra criacao e correcao de codigo com multiplos agentes (builder, resolver, reviewers), executando validacoes de seguranca, codigo e layout em ciclos iterativos ate aprovacao final.
---

# Workflow Orchestrator

## Skill Path Rules

- Resolve every relative path in this skill from `C:\Users\Jetta\.codex\skills\workflow-orchestrator\`.
- Reuse existing skills instead of re-describing their workflows: `../architect-handoff/`, `../web-builder/`, `../resolver/`, `../designer-resolver/`, `../reviewer/`, `../hacker-safado/`, `../layout-reviewer/`, `../designer/`, `../ux-performance-auditor/`, `../severino/`.
- Enforce the shared TDD standard in `../_shared/tdd-decente.md` whenever any executor or resolver edits behavior.
- For React/UI mode switches or imperative DOM enhancers, require at least one executor or reviewer pass to verify the real transition regression exists.
- If a required skill path is missing, state the blocker clearly and stop the orchestration instead of improvising a substitute.
- Load only the minimum context needed: task, impacted files, relevant constraints, current findings, and latest diff.

## Goal

Executar um ciclo automatizado de implementacao -> review -> consolidacao -> correcao -> revalidacao com multiplos agentes especializados, minimizando tokens e evitando retrabalho, ate aprovacao final ou limite de 3 iteracoes.

## When To Use

Use this skill when the request benefits from orchestration across multiple specialized agents, especially for:

- full-stack changes
- non-trivial bug fixes
- UI work that still needs code/security review
- risky changes with auth, API, sensitive data, integrations, or critical logic
- tasks where implementation and review should iterate with minimal manual supervision

Do not use for:

- one-file trivial edits with no meaningful review surface
- pure brainstorming or architecture-only work
- tasks where the user explicitly wants a single-agent/manual workflow

## Non-Negotiables

- Never allow reviewers to edit production code. Reviewers review; executor and resolver edit.
- Never ignore a critical confirmed finding.
- Never loop indefinitely. Hard stop at `max_iterations = 3`.
- Never send duplicate findings to remediation.
- Never treat hypothetical or absurd security scenarios as confirmed vulnerabilities.
- Never re-read or re-send broad context when the latest diff and impacted files are sufficient.

## Execution Mode

Set one internal mode before spawning agents:

- `fast`
- `standard`
- `strict`

Mode rules:

- `fast`: 1 review/remediation cycle maximum, compact security review, always run a lightweight input/output sanitization check, skip non-essential depth
- `standard`: 2 review/remediation cycles maximum, normal review depth, include layout review when UI exists
- `strict`: 3 review/remediation cycles maximum, deeper security review, stricter validation, use for high-risk scope

Suggested selection:

- `fast`: trivial or low-risk isolated implementation
- `standard`: default for most non-trivial delivery work
- `strict`: critical logic, auth, sensitive data, destructive operations, money, complex integrations

## Step 0 - Build the execution frame

Before any execution or review agent work, run `architect-handoff` first to produce the compact execution frame and handoff.

Then define internally:

1. Goal
2. Impacted files/modules
3. Constraints
4. Done criteria

If any item is missing, infer it from the repository and task before orchestration starts.

`architect-handoff` contract:

- always runs before classification, execution, or review
- outputs the smallest useful handoff/plan for the current task
- must not be skipped, even in compact or trivial workflows
- should reduce ambiguity, sharpen acceptance, and name the likely execution surface

## Step 1 - Analyze the task

Classify the task into exactly one primary type:

- `trivial`
- `bugfix`
- `ui-only`
- `backend-only`
- `full-stack`
- `complexa`

Detection rules:

- `trivial`: small isolated change, low risk, 1-2 files, no auth/data/integration impact
- `bugfix`: user reports broken behavior, regression, error, or failing scenario
- `ui-only`: visual/component/page changes with no meaningful backend contract change
- `backend-only`: API, service, data, jobs, permissions, validation, scripts, or infra logic without UI impact
- `full-stack`: UI + backend/data/API contract are both materially touched
- `complexa`: cross-cutting scope, high-risk domain, many files, unclear root cause, or multiple subsystems

Also detect boolean risk flags:

- `has_interface`
- `has_critical_logic`
- `has_external_integration`
- `has_sensitive_data`

Escalate to `complexa` when any combination creates high blast radius:

- auth/permissions + API/data changes
- money, destructive ops, migrations, or privilege boundaries
- external integration + weak observability
- sensitive data + public surface

## Step 2 - Choose the executor

Select one primary executor:

- `web-builder` for `ui-only` and implementation-oriented `full-stack` work
- `resolver` for `bugfix`, remediation, and `backend-only` work centered on critical logic, validation, correction, or integration repair
- `designer-resolver` for visual remediation work driven by `designer`/`layout-reviewer` findings where the dominant problem is polish, responsividade, hierarchy, spacing, contrast, or component consistency
- For `complexa`, choose the primary executor by dominant surface:
  - implementation-heavy or feature work -> `web-builder`
  - correction-heavy or review-driven remediation -> `resolver`
  - visual-remediation-heavy after a UI review -> `designer-resolver`

Selection rule:

- If the task starts from findings, failures, regressions, or known errors, prefer `resolver`.
- If the task starts from confirmed visual findings and the main work is to repair UI quality rather than business logic, prefer `designer-resolver`.
- If the task starts from feature delivery, UI construction, or end-to-end implementation, prefer `web-builder`.
- If the task is `backend-only`, default to `resolver` unless it is clearly new implementation work with low corrective risk.

## Step 3 - Spawn the agents

Create these subagents:

1. `architect`
   - skill: `architect-handoff`
   - ownership: compact execution framing before all other agents
2. `executor`
   - skill: `web-builder`, `resolver`, or `designer-resolver`
   - ownership: implementation and direct validation for the requested task
3. `reviewer`
   - skill: `reviewer`
   - ownership: quality, correctness, architecture, duplication, regressions
4. `security-reviewer`
   - skill: `hacker-safado`
   - ownership: real security issues only; confirm evidence before escalating
5. `layout-reviewer`
   - skill: `layout-reviewer`
   - create only when `has_interface = true`
6. `designer`
   - skill: `designer`
   - ownership: acabamento visual, consistencia de componentes, hierarquia, tipografia, contraste e polish geral
   - create when `has_interface = true` and the task is UI-heavy, design-sensitive, customer-facing, or the user explicitly asks for design review/polish
7. `ux-performance-auditor`
   - skill: `ux-performance-auditor`
   - ownership: perceived performance, fluidez, loading UX, blocking feedback, heavy interactions, user-facing slowdown
   - create when `has_interface = true`, when the user mentions slowness/travamento/loading, or when the surface is dashboard/table/form/modal heavy
8. `severino`
   - skill: `severino`
   - ownership: triage, ambiguity reduction, maintenance framing, risk clarification
   - create for non-trivial tasks by default; may be skipped only on compact trivial path if there is no ambiguity and no meaningful maintenance risk

Spawn rules:

- `architect-handoff` runs first and informs the prompts for the remaining agents.
- Fork context only when it materially saves tokens; otherwise pass compact task-specific context.
- Give each agent only the files, diff, risk flags, constraints, and acceptance criteria it needs.
- Reuse the same reviewer agents across iterations whenever possible.
- Tell workers they are not alone in the codebase and must not revert unrelated edits.
- Assign Brazilian meme-style nicknames to subagents in every run. Use this default mapping unless there is a strong task-specific reason to rename:
  - `architect` -> `Nazare Tatica`
  - `executor` -> `Pedrinho Executor`
  - `reviewer` -> `Cala Boca Galvao Review`
  - `security-reviewer` -> `X9 do Firewall`
  - `layout-reviewer` -> `Bela, Recatada e Responsiva`
  - `designer` -> `Pinterest do Senai`
  - `designer-resolver` -> `Trena de Ouro`
  - `ux-performance-auditor` -> `Vrum Vrum da UX`
  - `severino` -> `Trote da Triagem`
- When respawning or reusing threads, preserve the same meme nickname for the same role during the whole workflow to avoid confusion in follow-up cycles.

## Step 3.5 - Compact path for trivial tasks

If `task_type = trivial` and all risk flags are false:

- still run `architect-handoff` first
- do not spawn the full workflow
- run a single executor
- run one compact `reviewer` pass
- run compact `security-reviewer` only if the touched surface still includes input handling, data flow, or public output
- skip `severino` and `ux-performance-auditor` only if the task is clearly no-risk and no-interface/perceived-performance concern exists
- skip `designer` on trivial path unless the task is visibly UI-facing or the user explicitly asks for visual polish
- skip iterative remediation unless a blocking finding is confirmed

Use this path to minimize token cost and latency.

## Step 4 - Initial execution

Run `architect-handoff` first, then `executor`.

Executor contract:

- understand root task and impacted files
- implement the minimum complete change
- avoid duplicate logic and speculative abstractions
- add/update automated tests for changed behavior
- if the change introduces a new code path or fixes a bug, require at least one test that covers the changed behavior
- require the test level to match the real regression surface; do not accept helper-only coverage for flow bugs
- for UI loading-state work, require the real rendered branch to avoid visible loading copy when a silent placeholder is practical, and require a regression test that proves that behavior
- run the narrowest relevant validation first
- when the change touches restrictions, eligibility, assignment blocking, or candidate selection, require a practical local endpoint/flow smoke test in addition to automated tests when safe
- when the executor is `designer-resolver` and runtime is available, require screenshots before and after in `375`, `768`, and `1280`
- when the executor is `designer-resolver`, require explicit validation for overflow horizontal, elements outside viewport, and broken grid on the touched screens
- return: changed files, summary of changes, tests added/updated, validation run, known gaps

Do not start review until the executor has produced a concrete diff or validated no code change is needed.

## Step 5 - Parallel review

After the initial implementation, run active reviewers in parallel on the latest diff and impacted files:

- `reviewer`: bugs, correctness, architecture drift, duplication, weak tests
- `security-reviewer`: XSS, injection, auth flaws, privilege gaps, data exposure, insecure trust boundaries, unsafe secrets/logging, real attack paths
- `layout-reviewer`: alignment, responsiveness, visual consistency, semantic UI, layout integrity, interaction clarity
- `designer`: visual polish, hierarchy, spacing rhythm, typography, contrast, component consistency, overall perceived craft
- `ux-performance-auditor`: perceived latency, loading behavior, fluidity, interaction cost, visual blocking, user-facing performance regressions
- `severino`: whether ambiguity, maintenance framing, or acceptance drift still remain after implementation
- when the change touches loading UX, reviewers must check that the initial state does not masquerade as an empty state and that placeholders preserve the final layout geometry

Reviewer output contract:

- `verdict`: `APROVADO`, `APROVADO COM AJUSTES`, or `REPROVADO`
- findings ordered by severity
- file references
- evidence level: `confirmed`, `probable`, or `static evidence only`
- `confidence`: `high`, `medium`, or `low`
- `blocking`: `true` or `false`
- required correction, not vague preference

Security reviewer scope guardrails:

- inspect only the changed surface and its immediate trust boundaries
- do not model DDoS, infra abuse, or platform-level attacks when the diff does not touch those layers
- do not assume a privileged attacker without repository evidence
- do not raise speculative chains that depend on missing, unmodified infrastructure
- prefer confirmed boundary failures over broad hardening wishlists
- if the diff is UI-only, focus on client-side injection, unsafe rendering, auth exposure in the UI contract, and data leakage actually reachable from the changed code

## Step 6 - Consolidate findings

If any active reviewer is not `APROVADO`, consolidate all findings before editing again.

Consolidation rules:

- if any reviewer finds a confirmed critical blocking issue that invalidates the implementation, fail fast:
  - skip minor and derivative findings for that cycle
  - send only the critical root issue to `resolver` first
  - rerun reviewers after that root issue is corrected before processing secondary findings
- merge duplicates by root cause, not wording
- keep the strongest severity when duplicates overlap
- remove style-only noise that does not affect correctness, UX, security, or maintainability
- apply reviewer weight during prioritization:
  - security blocking issues override all other findings
  - correctness blocking issues override layout issues
  - confirmed UX/performance flow breakages outrank non-blocking layout polish
  - confirmed `designer` polish issues outrank style nitpicks but stay below correctness, security, and broken UX
  - layout issues never outrank confirmed blocking security or correctness issues
- prioritize in this order:
  1. confirmed critical correctness or data risk
  2. confirmed security exposure
  3. confirmed broken UX/layout
  4. missing or weak automated coverage
  5. maintainability issues that materially affect safety

Produce one remediation packet with:

- normalized problem statement
- affected files
- severity
- evidence
- required fix
- validation expectation

Routing rule for remediation packet:

- use `designer-resolver` when the packet is dominated by confirmed visual/design findings from `designer` or `layout-reviewer`
- use `resolver` when the packet is dominated by correctness, security, data, API, or mixed logic issues
- if the packet mixes visual and logic findings on the same surface, choose the dominant root cause; prefer `resolver` when a logic fix is prerequisite for the UI to become correct

## Step 7 - Correct in one pass

Send the consolidated remediation packet to `resolver` or `designer-resolver`, based on the routing rule above.

Resolver contract:

- address all confirmed findings in one pass when they share the same touched surface
- group findings by impacted surface such as `UI`, `API`, `validation`, or `data`
- resolve each surface group coherently to reduce cross-regression and conflicting partial fixes
- fix root causes, not visible symptoms only
- do not modify files outside `impacted_files` unless a confirmed finding explicitly requires it
- preserve working behavior outside the target scope
- update/add automated tests for the corrected behavior
- reject remediation that only adds low-level coverage when the bug lives in orchestration, UI flow, permissions, or module interaction
- rerun targeted validation before handing control back

Designer-resolver contract:

- address all confirmed visual findings in one coherent pass per touched screen/surface
- group findings by `layout`, `hierarchy`, `components`, `responsiveness`, `states`, or `contrast`
- fix root causes, not one-off cosmetic patches
- preserve the established design system when it is coherent; consolidate it when it is fragmented
- capture baseline and post-fix screenshots when runtime is available
- validate `375`, `768`, and `1280` for the affected screens
- confirm whether overflow horizontal, out-of-viewport elements, and broken grid were eliminated
- add tests when the visual fix changes behavior, interaction, state transitions, or rendering branches
- rerun targeted validation before handing control back

If a finding is disproven by repository evidence, mark it as rejected with brief justification instead of editing blindly.

## Step 8 - Validation loop

Repeat review after each remediation pass.

Loop algorithm:

1. increment `iteration_count`
2. rerun active reviewers on the new diff
3. if all active reviewers return `APROVADO`, stop immediately with success regardless of mode
4. if reviewers still find issues and `iteration_count < mode_limit`, consolidate again and send one new remediation packet to `resolver`
5. if `iteration_count = mode_limit` and issues remain, stop and mark as failed or partial

Loop rules:

- `mode_limit` is:
  - `1` for `fast`
  - `2` for `standard`
  - `3` for `strict`
- if any agent exceeds the time budget for the current cycle, cancel that iteration and mark the workflow as partial
- always early-exit after the first fully approved review pass, even in `strict`
- do not restart from scratch
- do not resend unchanged findings that were already fixed
- prefer diff-aware revalidation over full repo reprocessing
- if only UI files changed, avoid unnecessary backend review depth
- if only backend files changed, skip layout review
- when the bug is user-observed in a real flow, require at least one review pass to verify that a regression test exists near that flow
- when the bug or feature changes operational restriction logic, require evidence of a practical endpoint/flow smoke test or an explicit blocker explaining why it could not be run

## Step 9 - Finalize

Return a compact technical closeout with:

1. `Resumo tecnico`
2. `Tipo de task detectada`
3. `Sinais de risco detectados`
4. `Agentes utilizados`
5. `Erros encontrados`
6. `Correcoes aplicadas`
7. `Status final`
8. `Next action`
9. `Riscos remanescentes`

Status rules:

- `APROVADO`: all active reviewers approved with no blocking finding
- `APROVADO COM RESSALVAS`: no blocking issue remains, but there are explicit non-critical gaps, unverified edges, or missing minimum coverage for a new code path or bugfix
- `REPROVADO`: iteration limit reached with blocking findings still open

Next action rules:

- `none`: no manual action needed
- `manual review needed`: residual uncertainty remains and human inspection is the right next gate
- `user decision needed`: unresolved tradeoff, product choice, or risk acceptance is required

Repository closeout gate:

If `Status final = APROVADO`, include:

- generated commit message in conventional commits format
- list of changed files
- concise test summary

Do not generate a commit message when the final status is not `APROVADO`.

## Token and Performance Strategy

- Keep a fixed orchestration frame and avoid re-sending it every cycle.
- Pass only diff, impacted files, risk flags, and outstanding findings into later iterations.
- Reuse existing agent threads when context continuity is cheaper than respawn.
- Run reviewers in parallel, never sequentially, once implementation is available.
- Consolidate findings before any remediation so the resolver edits once per cycle.
- downgrade to compact path automatically for trivial no-risk work
- cache the last reviewer findings by impacted surface and reuse them when later diffs do not touch that same surface
- Skip inactive reviewers:
  - no UI -> no `layout-reviewer`
  - no UI or no meaningful visual/design surface -> no `designer`
  - no UI and no perceived-performance angle -> no `ux-performance-auditor`
  - no security-relevant surface -> still run `security-reviewer` in compact mode, not deep mode
- Prefer narrow validation first, broader validation only when risk justifies it.

## Guardrails

- Avoid overengineering and abstraction sprawl during remediation.
- Avoid duplicate prompts, duplicate findings, and duplicate code.
- Avoid asking the user for confirmation unless the task is blocked by missing requirements with real consequence.
- Avoid turning review agents into implementers.
- Avoid presenting a task as approved if any confirmed critical finding remains unresolved.

## Prompting Pattern

Use compact prompts.

Executor prompt must include only:

- task objective
- impacted files
- constraints
- done criteria
- detected task type
- risk flags

Reviewer prompts must include only:

- latest diff or changed files
- task type
- risk flags
- review scope
- prior findings already fixed, if relevant

Resolver prompt must include only:

- consolidated remediation packet
- changed files
- constraints
- required validation

Designer-resolver prompt must include only:

- consolidated remediation packet
- changed files
- constraints
- required visual validation
- runtime target or screenshots when available

## Minimal Orchestration Template

Internal sequence:

1. run `architect-handoff`
2. classify
3. choose executor
4. spawn `executor` + active reviewers + `severino`
5. run executor
6. run reviewers in parallel
7. consolidate findings
8. send one remediation packet to `resolver`
9. rerun reviewers
10. stop on approval or after 3 iterations

## Output Style

- linguagem tecnica
- objetiva e direta
- findings primeiro quando houver reprovacao
- sem storytelling
- sem repetir contexto ja estabelecido
- foco em execucao, evidencia e status
