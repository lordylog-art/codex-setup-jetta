---
name: qa-suite
description: Set up or maintain a reviewed Super QA runner registry, register new tests and diagnose missing coverage, conditional skips or incomplete aggregate results across native test stacks.
---

# QA Suite

Before planning or running, apply [QA learning](../super-qa/references/learning.md): retrieve same-project strategies through the chat’s existing ai-memory connection, read relevant full pages, and prioritize known regressions. After meaningful runs, confirm any authorized sanitized outcome save; report memory failures separately from test results.

When discovery is needed, use the project CLI `inventory` or inspect native test globs; inspect project manifests, scripts and runner configuration before execution. Choose existing commands for Node, Python, .NET, Java, Go or Rust as appropriate. Naming hints suggest candidates; they never establish that a command is safe or covers a test.

For a new language adapter or registry, read [native runner examples](references/native-runners.md); confirm each command against that project's installed tools.

Maintain `.super-qa.json` in the project with explicit reviewed `suites`: each entry has `id`, `command` as an argv array, `cwd`, `include` globs and `reporter`. Supported reporter names are `jest`, `vitest`, `playwright`, `tap` and `exit`; consult the installed engine for their exact output contract. Optional `reportArgs`, `timeoutMs`, `requires` (environment variable names) and `isolation` (`local`, `external`, `production`) describe real execution needs. Store no secret values. Set command and report arguments for the installed runner version; never invent a generic command from the language alone.

For runners without a supported structured reporter, reuse a maintained adapter. The bundled Python adapter runs unittest files; other Python frameworks need their own existing reporter/adapter. An `exit` entry records a command but remains BLOCKED because it cannot prove membership or skip accounting. TAP approval requires the native Node test runner and `{tests}`; JSON reporters must identify every registered file using exact paths relative to `reportRoot`/`cwd` or absolute project paths. Registration is not execution coverage.

After adding or changing tests, run CLI `check` to find discovered tests outside the registry, conditional skips and other gaps. `check` inspects registration; it does not execute tests. Unregistered tests fail coverage accounting until resolved. Inspect each gap and fix the owning runner/test rather than hiding it by broadening globs or changing reporter modes. Keep permanent tests in the repository and reachable through its global aggregate.

Use the project CLI `check` when registration needs verification, execute `run --project <absolute-root> --suites <reviewed-ids>` and read the returned run’s `result.json`; otherwise use the native runners and their reports directly. No persistent Super QA server is required. Run only trusted commands within current authorization. A timeout, missing prerequisite/report, empty expected suite, skipped test or unexecuted selected suite is BLOCKED; a failing assertion/process is FAIL. An intentionally excluded suite remains outside the proven scope and must be disclosed. Preserve raw logs/reports and actual counts; reruns do not erase prior failures without explanation.

Do not install missing toolchains or change operational scheduler settings merely to make QA green. State what dependency or permission prevents execution and continue independently useful checks.
