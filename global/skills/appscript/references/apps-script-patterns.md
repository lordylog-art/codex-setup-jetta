# Apps Script Patterns

## Runtime Rules

- Assume V8 syntax is available unless the repo proves otherwise.
- Do not introduce Node-only APIs into runtime code.
- Do not introduce ESM `import` or `export` into raw Apps Script files unless the project has a build step that transforms them.
- Preserve function names used by installable triggers, menus, web apps, or library consumers.

## Service Boundaries

- Wrap `UrlFetchApp`, `SpreadsheetApp`, `DriveApp`, `GmailApp`, and similar globals behind focused helpers when logic grows.
- Keep business logic pure when possible so it can be tested outside Apps Script.
- Centralize auth headers, cookie handling, retries, and non-2xx failures for HTTP integrations.

## Sheets and Workspace Performance

- Batch `getValues` and `setValues` operations.
- Avoid cell-by-cell loops when range operations are possible.
- Cache metadata or auth state when repeated calls are likely.
- Use `LockService` for shared state or trigger concurrency.

## HtmlService

- Keep templating simple and explicit.
- Validate all server-call parameters from `google.script.run`.
- Keep client-side JavaScript separate from server-side Apps Script logic.
- If a page depends on server data, define a clear server entrypoint that returns plain JSON-ready objects.

## Error Handling

- Throw direct, user-meaningful errors for validation failures.
- Normalize external API failures into a consistent message shape.
- Log enough context to debug without leaking secrets.
