---
name: qa-api-data
description: Validate changed APIs, real persistence, migrations, background jobs and controlled integration boundaries with durable regression tests.
---

# QA API and Data

Trace the changed flow from public entry through authentication, validation, transaction, persistence and any job or integration. Choose tests at the boundaries where the claim lives. Exercise actual request parsing and authorization for HTTP claims; reopen/query the real isolated database for durability claims.

Reuse the project's database engine, migration tooling, bootstrap and cleanup helpers. Assert the observable transition plus rejection/rollback relevant to the change. Migration tests use representative pre-migration records, run the actual migration and verify retained data and compatibility; test rollback only where supported or required. Never apply test migrations to the user's operational database.

For jobs, exercise enqueue/dequeue and worker/bootstrap where these are part of the claimed behavior. Calling a worker function directly cannot prove scheduling or startup recovery. Verify operation/tenant identity through continuations when applicable.

Use controlled local transports or provider sandboxes for integrations within authorized scope. Mark the boundary precisely: local protocol evidence differs from actual provider acceptance/delivery. Preserve configured integrations and activation settings in the user's instance. External sends, costs and production changes need the project's specific authorization.

Store regressions in native runners and register them through [QA Suite](../qa-suite/SKILL.md). Report actual engine/entrypoint tested and blocked dependencies. A mock of the boundary under review cannot establish that boundary's real behavior.
