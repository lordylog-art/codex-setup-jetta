---
name: qa-personas
description: Validate roles, tenant or operation isolation, anonymous access and actor transitions when changed behavior depends on identity or scope.
---

# QA Personas

Read the changed endpoint/action and its authorization source. Derive relevant identities from the product: allowed user, denied user, anonymous or expired session, and another tenant/operation where isolation matters. Distinguish role/module visibility from exact action grants and record scope. Use synthetic identities in an isolated test database with known ownership.

Persist the smallest meaningful tests in native runners. Exercise the real authentication/authorization boundary, assert both returned data and side effects, and verify a denied mutation left storage unchanged. UI hiding alone does not prove denial. Use distinct authenticated sessions for actors; direct service calls with injected identities prove only that service layer.

Where scope survives queues, retries, caches or scheduled jobs, trace and test that continuation. Add concurrent actors, permission revocation or session refresh only when the affected flow makes them relevant. Preserve a failing case for an identified escape or privilege regression.

Register tests through [QA Suite](../qa-suite/SKILL.md). Report tested persona/action/scope combinations and explicit omissions. A representative matrix is scoped evidence; do not claim every persona or operation was tested.
