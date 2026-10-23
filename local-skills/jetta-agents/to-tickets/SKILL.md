---
name: to-tickets
description: "Plan cohesive tickets from a SPEC or plan, preserving dependencies and the Smart Orchestrator validation contract. Handle trivial changes directly."
disable-model-invocation: true
---

## V2 integration

For multi-ticket features, also read `C:/Users/caila/.agents/skills/smart-orchestrator/references/planning-contract.md`. Prepare `execution-plan.json` in the existing canonical artifact, covering acceptance criteria, gates, maturity, dependencies and evidence without duplicating the SPEC. Link the plan from the relevant tickets/Index after the approval required below. When execution is authorized, hand its canonical path and approved queue to Smart Orchestrator. Planning does not authorize implementation. Preserve this skill's tracker, Spec Workspace adapter, partitioning and approval rules.

# To Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

## Optional Obsidian workspace

Use [the shared Spec Workspace Adapter](../spec-workspace/SKILL.md) when the input explicitly references Obsidian or the source spec is already inside a `Spec Driven`/`Specdriven` workspace. Otherwise keep the original tracker paths and process below. Resolve from the source spec path so later invocations inherit that workspace. In Obsidian mode, `Tickets/` is the canonical local tracker: create one note per approved ticket, preserve dependency-order numbering and blocking links, link each ticket to the spec and relevant context, add ticket links to the spec, and update `Index.md`. Do not publish the same tickets to the configured external tracker. Read only the Index and related notes.

The issue tracker and triage label vocabulary should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

For Obsidian tickets, use the metadata and link conventions in the shared adapter rather than the local `.scratch` template below; keep one note per ticket and preserve the user's approved breakdown.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, read the contract and directly related decisions/comments; expand history only to resolve a concrete ambiguity.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Identify integration risks and prerequisites of the slice. Refactor only where necessary for the approved behavior; do not create preparatory tickets by default.

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Size by demonstrable behavior and integration risk, not context-window size. Keep internal proof steps within the ticket; do not add tickets per technical layer.

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. Distinguish code prerequisites from acceptance still pending on the preceding ticket. No blockers alone does not establish runtime readiness.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping the required local checks passing batch to batch (CI remains prohibited in ERP Jetta) because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

Within each existing ticket, make behavior, invariants, acceptance proof, cheapest refuting example and integration risks observable. Use 1–5 prioritized examples to start, proportional to risk, without limiting total acceptance coverage. A compound criterion may remain, but name its important obligations separately: CAS, rollback, audit and idempotency cannot receive one check from a happy-path test. Link to [TDD](../tdd/SKILL.md) for proof strength; do not copy its protocol. Preserve vertical slices and ticket count unless behavior truly requires another delivery.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown.

### 5. Publish the tickets to the configured tracker

Publish the approved tickets. **How** depends on the tracker `/setup-matt-pocock-skills` configured; the tickets are the same either way, only the shape of the blocking edges changes:

No ERP Jetta, tickets contêm escopo, riscos específicos, critérios, dependências/estado e referências. Aponte para [Implement](../implement/SKILL.md) como processo canônico e para contratos comuns existentes; não copie catálogos de skills, sequência de gates ou protocolo visual em cada ticket. Preserve integralmente os requisitos aprovados e acrescente apenas exceções específicas, sem reduzir gates.

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file's "Blocked by" lists the numbers/titles it depends on. Use the per-ticket file template below: one ticket per file, never a single combined file.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the platform's native blocking / sub-issue relationship where it has one; otherwise set each ticket's "Blocked by" to the blocking issues. Apply `ready-for-agent` only when behavior, decisive examples, dependencies and required capabilities are resolved; otherwise record the actual blocker. Approval of prose alone is not runtime readiness.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

Do NOT close or modify any parent issue.

<local-ticket-template>

# <NN>: <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

**Blocked by:** the numbers/titles of the tickets that gate this one, or "None (can start immediately)".

**Status:** <ready-for-agent or concrete blocker>

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

**Decisive example / invariant / integration risk:** <compact examples tied to the criteria; proof surface and unresolved prerequisites>.

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

**Decisive example / invariant / integration risk:** <compact examples tied to the criteria; proof surface and unresolved prerequisites>.

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)".

</issue-template>

In either form, avoid specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.
