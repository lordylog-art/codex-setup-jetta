# Maintainability Repair

Use this reference when fixing the review item risks adding more `linguicao`.

## Signals Of Code Sprawl

- one function is doing orchestration, validation, transformation, and persistence together
- the same business rule is patched in multiple branches or files
- names hide intent
- nesting is deep enough that the happy path is hard to read
- a new conditional was added where a better abstraction should own the rule
- "temporary" logic is becoming permanent

## Repair Moves

Choose the smallest move that improves the area:

- extract one coherent helper
- collapse duplicated conditionals into one policy point
- isolate side effects from pure decision logic
- rename for business meaning
- split orchestration from computation
- delete dead paths that conflict with the corrected behavior

## Guardrails

- do not redesign the whole module unless the fix is impossible otherwise
- keep call sites stable when practical
- avoid introducing extra layers that only rename complexity
- prefer obvious structure over clever abstractions

## Definition Of Better

The code is better when:

- the main path is easier to read
- the business rule has one clear home
- tests map cleanly to the behavior
- the next editor can change it with lower fear
