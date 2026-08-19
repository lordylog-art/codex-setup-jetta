# Finding Triage

Use this reference to turn review comments into an execution plan.

## Triage Table

For each finding, classify:

- `type`: correctness, security, tdd-and-coverage, maintainability, optimization
- `confidence`: confirmed, likely, unclear
- `blast radius`: local, adjacent, systemic
- `proof needed`: code read, targeted test, broader regression, manual reproduction

## Translation Pattern

Turn vague review language into actionable work.

Examples:

- "this may break edge cases"
  becomes
  "identify the edge cases, write tests for them, verify actual failure or gap, then fix"

- "this is linguisticao"
  becomes
  "identify where responsibilities are mixed or duplicated and clean only enough to make the fix stable"

- "missing TDD"
  becomes
  "add a failing or gap-exposing automated test before implementation whenever practical"

## Ordering Logic

Fix in this order:

1. correctness or safety breakage
2. test coverage needed to safely continue
3. maintainability blockers that make a safe fix hard
4. optimization issues unless they are causing breakage

## Scope Guard

For each finding, define:

- what must change
- what may change
- what must not change

This prevents review remediation from turning into uncontrolled refactoring.
