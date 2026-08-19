---
name: architect-handoff
description: Plan architecture and generate compact execution prompts for implementers.
---

# Architect Handoff

## Ideia First

When the user brings a feature idea, evaluate the idea before generating any plan or handoff.

Use this forced classification:

- `IDEIA BOSTA`: weak idea, high waste potential, bad tradeoff, unclear value, or likely to create complexity without enough payoff.
- `MEIA BOMBA`: usable direction, but undercooked, risky, generic, or missing key product/technical definition.
- `IDEIA DO CARALHO`: strong idea, clear value, solid leverage, or unusually good strategic/product fit.

Behavior by classification:

- If `IDEIA BOSTA`:
  - say clearly that the idea is bad
  - explain briefly why
  - suggest stronger alternatives or improvements
  - if the idea is beyond rescue, explicitly recommend dropping it
  - do not generate handoff unless the user asks to salvage it
- If `MEIA BOMBA`:
  - say clearly that it has potential but needs improvement
  - point out the main weaknesses
  - suggest concrete improvements
  - only generate the handoff after the user accepts the improved direction
- If `IDEIA DO CARALHO`:
  - say clearly that the idea is strong
  - suggest a few improvements only if they materially help
  - then generate the handoff or plan if the user asks for execution prep

Tone rule for idea evaluation:

- Be blunt, concise, and useful.
- Do not soften the classification.
- Do not be rude without adding value.
- Use the exact labels above when classifying.

## Skill Path Rules

- Resolve every relative path in this skill from `C:\Users\Jetta\.codex\skills\architect-handoff\`.
- Shared checklists live in `C:\Users\Jetta\.codex\skills\_checklists\`; from this skill, reference them as `../_checklists/...`.
- If this skill cites a checklist path, script path, or reference file, open and run it before substantial work.
- If a required file is missing, say that clearly and stop assuming it should be resolved from the project workspace.

## Before executing

If routed here via `task-router`, skip `check-5s.md` " classification already done.
Default to the smallest useful output.
**Full Plan is opt-in only** " use it when the user explicitly says "full plan", "architecture detail", "tradeoff analysis", or "multi-phase". Otherwise use Direct Handoff or Compact Plan.

If the input is a feature idea instead of an already-approved task:

1. classify the idea first
2. improve or reject it when needed
3. only move to planning or handoff after the idea is accepted or clearly worth pursuing

## Mode: Direct Handoff (simple tasks)

Skip architecture. Generate one compact prompt:
- Task
- Objective
- Files
- Constraints
- Acceptance
- Delivery format

## Mode: Compact Plan (default for non-simple tasks)

Output only:

1. Objective
2. Files/Modules
3. Key Constraints
4. Main Risk
5. Next Step

Limits:

- Max 5 bullets total when possible.
- No long background sections.
- No repeated facts.
- No examples unless asked.
- No production code.

## Mode: Full Plan (only when explicitly requested)

### Rules

- Read only files needed.
- Scope bounded and explicit.
- Mark `ASSUMPTION:`, `MANDATORY:`, `DO NOT:` clearly.
- Bullets over prose. No production code. No vague language.

### Output

1. Technical Problem Statement
2. Facts, Constraints, Assumptions, Unknowns
3. Requirements (functional + non-functional)
4. Out of Scope
5. Architecture + Module/File Targets
6. Flows + Contracts
7. TDD Strategy
8. Checklist + Acceptance Criteria
9. Risks and Mitigations

## Mode: Handoff (after approved plan)

- Do not re-architect.
- Do not repeat background.
- Generate one compact prompt: Task, Objective, Files, Constraints, TDD, Acceptance, Delivery, Escalation.

## Output rules

- Terse bullets. No duplicate wording.
- Collapse similar items. No examples unless asked.
- No long explanations. Max objectivity.
- Prefer `Direct Handoff` or `Compact Plan`.
- Do not emit long sectioned plans unless the user explicitly asks for depth.
- For feature ideas, start with the classification line before any plan.
## Mandatory Automated Testing Policy
- Automated testing is mandatory for every behavior-changing code change.
- Handoffs must reference `../_shared/tdd-decente.md` as the implementation quality bar.
- TDD sections in handoffs must name the regression surface and the expected test layer, not just say "add tests".
- If the change touches React/UI mode switches or imperative DOM enhancers, the handoff must call out the transition path that needs regression coverage.

## Automated Test Selection
- Run the automated tests and validations that directly match the changed area and risk.
- Prefer native project commands such as `npm run test --workspace @erp-jetta/api`, `npm run test --workspace @erp-jetta/web`, `npm run lint`, or `npm run build` when they are the clearest coverage for the task.
- Do not require the project Python automation runner for routine implementation or review work.
- Use the central automation runner only when the user explicitly asks for it or when a deploy/ship script being executed requires it.
- If relevant tests cannot be run, report the exact validation gap instead of substituting the Python runner by default.