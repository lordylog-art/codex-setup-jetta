# Native runner adapters

These are argv starting points, not commands to execute blindly. Prefer the repository's existing aggregate script, lockfile, runtime and test discovery. Review configuration and expected side effects first. Adapt paths, environment prerequisites and supported reporter arguments to the installed versions.

| Stack | Candidate `command` argv | Check before registration |
| --- | --- | --- |
| Node | `["node", "--test", "--test-reporter=tap", "{tests}"]` | Explicit registered test paths and TAP handling; setup owned by existing scripts needs a counted adapter. |
| Python | `["python", "-m", "pytest", "tests"]` | Project virtualenv, plugins, markers, skips and database fixtures; the runner needs an adapter for structured counts. |
| .NET | `["dotnet", "test", "Project.sln", "--no-restore"]` | Dependencies already restored, target framework, test filtering and TRX/count adapter. |
| Java/Maven | `["mvn", "test"]` | Repository wrapper/toolchain, Surefire versus integration-test/Failsafe stages and XML/count adapter. |
| Java/Gradle | `["gradle", "test"]` | Prefer the project's wrapper, selected modules, integration tasks and XML/count adapter. |
| Go | `["go", "test", "./..."]` | Workspace modules/build tags, cache policy, external dependencies and JSON/count adapter. |
| Rust | `["cargo", "test", "--workspace"]` | Features, ignored tests, doctests, toolchain and structured-count adapter. |

An initial explicit exit-based registry entry can use:

```json
{
  "suites": [
    {
      "id": "python-unit",
      "command": ["python", "-m", "pytest", "tests/unit"],
      "cwd": ".",
      "include": ["tests/unit/test_*.py", "tests/unit/**/*_test.py"],
      "reporter": "exit",
      "isolation": "local",
      "timeoutMs": 120000
    }
  ]
}
```

Replace the illustrative paths with actual discovered tests. Verify nested and alternate naming conventions against collected tests before accepting the globs. The `exit` reporter intentionally returns BLOCKED even for zero exit: it does not establish counts, skip absence, all selected test execution or a real database/provider boundary. Reuse or implement a maintained adapter that fails on missing/empty reports and skipped/unexecuted expectations, and test it against failed, skipped and malformed output. Do not relabel opaque output as TAP/JSON merely to obtain PASS.
