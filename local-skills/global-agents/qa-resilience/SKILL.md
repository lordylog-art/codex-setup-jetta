---
name: qa-resilience
description: Test recovery, retries, idempotency, concurrency and time or money boundaries when the changed flow has those concrete failure risks.
---

# QA Resilience

Locate the actual failure window in the changed flow and choose a durable observable invariant: no duplicate effect, no lost accepted work, correct ownership, consistent balance or valid lifecycle. Use the project's existing fault injection and native runners; add the smallest regression that crosses the relevant boundary.

For an external acceptance/local receipt gap, use a controlled transport that records acceptance durably, terminate a real child process after acceptance but before the local receipt, then restart through the real bootstrap/recovery path. Assert effects and stored state after recovery. An exception inside a mocked function or direct reconciliation call does not prove process-crash or startup recovery. Keep all effects within the authorized isolated test surface.

Where relevant, coordinate concurrent workers/actors with a barrier and assert the final database/transport result, then test retry/deduplication using the real key and persistence boundary. Cover timezone/DST, rounding/currency or numeric limits only when the flow uses those rules. Use deterministic clocks or controlled inputs without replacing the boundary whose behavior is being claimed.

Reuse installed property, fuzz or load tools when the risk calls for them; constrain inputs and record seed, workload and invariant. One load run is scoped evidence, not an SLA. Missing process/bootstrap/database access leaves that claim BLOCKED; report the narrower evidence honestly.

Persist tests and register them through [QA Suite](../qa-suite/SKILL.md). Preserve user runtime, data and saved activations throughout fault experiments.
