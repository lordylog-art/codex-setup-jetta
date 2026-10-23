---
name: to-spec
description: "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed."
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

## Optional Obsidian workspace

Use [the shared Spec Workspace Adapter](../spec-workspace/SKILL.md) when the invocation includes an explicit Obsidian note, folder, URI, or vault-relative path, or when its source is already inside that workspace. Without one, preserve every step and output of the original skill below. In Obsidian mode, the workspace temporarily acts as the local Markdown tracker: create the canonical spec in `Specs/`, link its source and relevant decisions, and update `Index.md`; do not publish it to the configured external tracker. Keep feature-local decisions in this workspace and repo-wide domain docs in their normal locations.

The issue tracker and triage label vocabulary should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Choose the cheapest seam containing the mechanism under risk, following [TDD](../tdd/SKILL.md). A single seam is useful only if it can observe the required behavior.

Reuse approved boundaries; ask only about material scope or contract decisions that remain unresolved.

3. Write the spec using the template below, then publish it to the project issue tracker. Mark ready only when behavior, critical examples and dependencies are resolved; record any unresolved prerequisite explicitly.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A concise numbered list of distinct user behaviors. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Cover the approved scope without repeating stories or adding speculative capabilities. Link decisions rather than duplicating them.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
