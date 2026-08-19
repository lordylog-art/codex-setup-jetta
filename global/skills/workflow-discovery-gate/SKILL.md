---
name: workflow-discovery-gate
description: Gate obrigatorio de discovery, fechamento de escopo, analise de risco e liberacao de handoff antes de qualquer implementacao. Use when Codex needs to preparar uma feature, bug estrutural, integracao, refactor sensivel ou tela operacional antes de codar; fazer perguntas em lotes pequenos, consolidar entendimento com confirmacao explicita, atacar a solucao por risco real e liberar apenas um handoff tecnico pronto para architect, builder, reviewer e fixer quando nao houver lacunas criticas.
---

# Workflow Discovery Gate

## Skill Path Rules

- Resolve every relative path in this skill from `C:\Scripts\ERP JETTA\tools\skills\workflow-discovery-gate\`.
- Reuse stricter project rules from `AGENTS.md` when present. This skill is a gate, not a replacement for project policy.
- Enforce the behavioral change standard in `C:\Users\Jetta\.codex\skills\_shared\tdd-decente.md` in every implementation handoff.
- Treat this skill as planning-only. Never implement, patch files, or suggest "just code it" before the execution gate is open.
- If a required contract, source of truth, integration boundary, or ownership detail materially changes architecture, treat it as a critical gap instead of guessing.

## Goal

Force disciplined discovery before implementation. Close the problem statement, lock the understanding, attack the solution by risk, and release execution only when the remaining unknowns no longer threaten architecture, acceptance, or operational reliability.

## Best Fit

Use this skill for:

- new features with ambiguous scope
- bugs where the visible symptom may hide a structural cause
- external integrations, sync jobs, imports, exports, webhooks, queues, and schedulers
- sensitive refactors with real blast radius
- operational screens, dashboards, tables, modals, and flows where stale and error semantics matter

Do not use this skill for:

- trivial edits already fully specified and low-risk
- pure copy tweaks with no architecture consequence
- post-implementation review; use reviewer or fixer flows instead

## Default Operating Mode

Default to `standard`.

- `compact`: use only when the task is narrow, low-risk, and already close to closed scope; still run every phase, but keep discovery to 1-2 rounds.
- `standard`: default for most features, bugs, integrations, and operational screens; allow 2-3 discovery rounds.
- `strict`: use for auth, money, destructive operations, concurrency-heavy flows, schedulers, external sync, or stale-sensitive operations; allow 3-4 discovery rounds and deeper destruction.

## Non-Negotiables

- Never implement during this skill.
- Never skip the understanding lock.
- Never release a final handoff while a critical gap remains.
- Ask structural questions before cosmetic questions.
- Ask in small batches: prefer 2-4 questions, max 5.
- Label `FATO`, `PREMISSA`, `LIMITACAO`, `DUVIDA ABERTA`, and `NAO BLOQUEANTE` explicitly.
- Stop discovery when only non-blocking details remain.
- If the user pushes for implementation early, still run at least the compact gate first.
- Avoid infinite loops: max 2 rounds in `compact`, 3 in `standard`, 4 in `strict`. If the gap survives the round budget, either convert it into an explicit conservative assumption or keep the work `BLOQUEADO`.

## Critical vs Non-Blocking Gaps

Treat as critical:

- objective unclear
- structural problem vs symptom unclear
- source of truth unclear
- primary entity or stable identity unclear
- entry condition unclear
- exit condition unclear
- fallback unclear
- stale semantics unclear
- error semantics unclear
- external dependency contract unclear
- expected volume, cadence, or SLA unknown when it changes architecture

Treat as non-blocking unless the user says otherwise:

- naming
- copy
- minor visual polish
- low-impact telemetry niceties
- secondary filters and sorts
- optional future automation

## Question Policy

1. Start with the highest blast-radius unknowns: objective, source of truth, entity identity, entry and exit, failure semantics, cadence, and integrations.
2. Ask only what can change architecture, public behavior, test strategy, or operational burden.
3. Use small batches. Prefer 2-4 questions. Use 5 only when one tightly related cluster is cheaper than another round trip.
4. After each answer, restate the new facts and decide whether another round is still necessary.
5. If the user does not know an answer, offer a bounded conservative assumption or a small set of options.
6. Do not repeat the same question more than twice. On the second miss, either convert it into a `PREMISSA` or mark the work `BLOQUEADO`.
7. Stop discovery when the remaining unknowns would not change the architecture, acceptance criteria, or mandatory test strategy.

## Output Labels

- `FATO:` confirmed by user, code, logs, docs, or runtime evidence.
- `PREMISSA:` conservative assumption made to keep progress.
- `LIMITACAO:` known constraint or evidence gap.
- `DUVIDA ABERTA:` unresolved item still relevant.
- `NAO BLOQUEANTE:` unresolved detail that does not block architecture.

## Standard Response Order

Use the phases in order. Do not collapse them into one vague blob.

- During discovery rounds, answer with `Mapa atual`, `Lacunas criticas`, and `Perguntas desta rodada`.
- During the understanding lock, answer with the full lock structure and ask for confirmation.
- During destruction, answer with findings by severity, impact, required correction, additional questions, and verdict.
- During the execution gate, answer with the checklist status and gate verdict.
- Only after the gate is open, emit the architect handoff and optional orchestration prompts.

## Phase 1 - Discovery

### Objective

Extract the real context before proposing implementation.

### Mandatory Discovery Surface

Identify explicitly:

- objective real
- structural problem vs visible symptom
- source of truth
- primary domain entity
- stable identity of that entity
- entry criteria
- exit criteria
- cadence or SLA
- fallback
- stale semantics
- error semantics
- expected volume
- external dependencies
- expected failure behavior
- operational ownership
- manual steps that still exist
- UX obligations that reflect the real backend state

### Discovery Procedure

1. Map current behavior vs expected behavior.
2. Prioritize the smallest set of questions that can change architecture.
3. Ask the next round in a small batch.
4. After each answer, publish:
   - `Mapa atual`
   - `Lacunas criticas`
   - `Perguntas desta rodada` or `Motivo para seguir`
5. If only non-blocking details remain, mark them as `NAO BLOQUEANTE` and advance.

### Discovery Guardrails

- Do not dump 20-30 questions at once.
- Do not ask cosmetic UI questions before the structural flow is closed.
- Do not confuse "what the user saw" with "where the defect actually lives".
- Do not accept "we can see later" for source of truth, identity, fallback, or stale/error behavior.

## Phase 2 - Understanding Lock

### Objective

Freeze the current understanding before any implementation proposal.

### Mandatory Output

Emit exactly this structure:

`UNDERSTANDING LOCK`

- resumo do problema:
- objetivo:
- escopo:
- fora de escopo:
- premissas assumidas:
- regras fechadas:
- decisoes ja tomadas:
- duvidas ainda abertas:
- criterios de aceitacao preliminares:

Then ask explicitly:

`Confirma este lock? Se nao, corrija o que esta errado antes de prosseguir.`

### Lock Rules

- Do not proceed to phase 3 without explicit confirmation or explicit user correction followed by an updated lock.
- If the user corrects something material, rewrite the lock instead of hand-waving the delta.
- Keep facts and assumptions separated inside the lock.

## Phase 3 - Destruction / Stress Test

### Objective

Attack the direction before implementation.

### Mandatory Attack Surface

Try to break the idea across:

- architecture failure
- fragile dependency
- weak or split source of truth
- ambiguous identity
- duplication risk
- stale risk
- hidden operational error
- scale or cost risk
- external integration load
- concurrency risk
- lock based on wrong assumption
- UX lying about the real state
- manual flow disguised as automation
- solution that looks good in design and bad in production

### Mandatory Output

Emit a `DESTRUCTION REPORT` with:

- findings by severity
- impact
- required correction
- additional questions if still needed
- verdict: `BLOQUEADO`, `APROVADO COM AJUSTES`, or `APROVADO`

Use this finding format:

`[SEVERITY] titulo curto -> impacto -> correcao exigida -> base (FATO|PREMISSA|LIMITACAO)`

### Verdict Rules

- `BLOQUEADO`: unresolved gap can invalidate architecture, hide operational failure, or make acceptance unverifiable.
- `APROVADO COM AJUSTES`: core direction survives, but corrections must enter the handoff.
- `APROVADO`: core direction survives and no critical gap remains.

## Phase 4 - Execution Gate

### Objective

Release implementation only when the minimum contract is closed.

### Mandatory Checklist

Do not open the gate until each item is `OK` as `FATO` or safe `PREMISSA`:

- objective clear
- source of truth defined
- entity identity defined
- entry condition defined
- exit condition defined
- fallback defined
- stale and error semantics defined
- expected volume defined
- cadence or SLA defined
- main risks surfaced
- acceptance criteria closed

### Gate Rules

- If any mandatory item is missing, do not generate the final handoff.
- Ask only the smallest next question needed to close the missing item.
- If the user cannot answer a critical item and a safe assumption would still change architecture, keep the gate `BLOQUEADO`.
- If the remaining gaps are only `NAO BLOQUEANTE`, open the gate and carry those limits into the handoff.

### Mandatory Output

Emit:

`EXECUTION GATE`

- checklist status per item
- remaining blockers
- verdict: `LIBERADO` or `BLOQUEADO`

## Phase 5 - Architect Handoff

### Objective

Generate one implementation-ready handoff.

### Mandatory Output

Emit exactly this structure:

`ARCHITECT HANDOFF`

- titulo:
- objetivo:
- problema estrutural:
- decisao arquitetural:
- fluxo novo resumido:
- arquivos provaveis a alterar:
- constraints:
- riscos conhecidos:
- testes obrigatorios:
- criterios de aceite:
- limites assumidos:
- proximos passos:

### Handoff Rules

- Keep the handoff ready for execution, not as another brainstorming pass.
- Separate `FATO` from `PREMISSA` wherever that distinction matters.
- In `testes obrigatorios`, name the regression surface, the minimum test layer, the relevant negative path, and any practical validation expected near real usage.
- Reference `C:\Users\Jetta\.codex\skills\_shared\tdd-decente.md` as the minimum quality bar for behavior changes.
- If `AGENTS.md` or project policy imposes stricter validation, inherit it instead of restating a weaker rule.
- Prefer the smallest reliable cut over a sophisticated redesign unless the smaller cut fails the destruction phase.

## Phase 6 - Optional Orchestration Handoff

### Objective

Prepare compact follow-on prompts for specialized agents without making the skill depend on them.

### When To Emit

Emit this section when:

- the user asks for multi-agent follow-up
- the task is large enough to benefit from separated roles
- the repo already uses architect, builder, reviewer, and fixer flows

### Suggested Agent Mapping

- `Architect` -> `architect-handoff`
- `Builder` -> `web-builder` for feature-heavy work, `resolver` for bugfix or backend-heavy correction
- `Reviewer` -> `reviewer`
- `Fixer` -> `resolver`, or `designer-resolver` when the dominant issue is visual remediation

### Prompt Rules

- Keep prompts cohesive and low-redundancy.
- Give each agent only the context it needs.
- Do not repeat the full discovery transcript.
- Carry forward only locked scope, risks, constraints, acceptance, and current blockers.

### Mandatory Output Shape

When emitted, answer with:

- `Prompt para Architect`
- `Prompt para Builder`
- `Prompt para Reviewer`
- `Prompt para Fixer`

Each prompt must be short, role-specific, and consistent with the same locked scope.

- `Prompt para Architect`: validate or tighten the approved direction, name file surfaces, constraints, main risk, and done criteria. No implementation.
- `Prompt para Builder`: implement only the locked scope, follow the mandatory tests, avoid speculative refactor, and escalate if a hidden blocker violates the gate assumptions.
- `Prompt para Reviewer`: review the resulting diff against the locked scope, risks, regressions, and test adequacy. Prefer confirmed findings over style chatter.
- `Prompt para Fixer`: fix only confirmed findings, preserve the approved scope, rerun the required tests, and report residual risk if anything stays unresolved.

## Stop Conditions

Stop discovery and move forward when:

- the mandatory gate checklist is closed
- remaining unknowns are clearly `NAO BLOQUEANTE`
- more questioning would only polish wording, naming, or low-impact details

Stop and block when:

- the source of truth is still disputed
- identity is ambiguous
- the entry or exit condition is not knowable yet
- stale or error behavior is undefined
- a hidden manual dependency still decides success
- acceptance cannot be tested without guessing

## Recommended Composition With Project Policy

- Let `AGENTS.md` define the global bar for testing, approval, and repo-specific constraints.
- Let this skill own the pre-implementation gate.
- Let execution skills own code changes after the gate opens.
- Let review and fixer skills operate only after a concrete diff exists.

## Ready Invocation Examples

- `Use $workflow-discovery-gate before implementing a new scheduling flow for route sync.`
- `Use $workflow-discovery-gate to clarify a structural bug where the UI says synced but the external API still failed.`
- `Use $workflow-discovery-gate to gate a sensitive refactor of an operational dashboard before any coding starts.`
- `Use $workflow-discovery-gate to close scope, stress-test risks, and prepare handoff for architect, builder, reviewer, and fixer.`
