# Stack-Specific Review Checks

Load this file only when reviewing code in these stacks.

## Next.js

- Auth/permissions not enforced only in client.
- Sensitive data not exposed through props, public env vars, or client bundles.
- Forms/mutations do not trust client-side validation alone.
- Loading/error/empty states do not hide breakage.
- Route handling, caching, client/server boundaries checked for exposure.

## NestJS

- DTO validation, guards, pipes, authorization boundaries.
- Controllers reject over-broad payloads.
- Services enforce business rules independently of frontend.
- Auth flows checked for brute-force, token misuse, insecure defaults, missing ownership.
- Exception handling does not leak internals.

## Prisma / PostgreSQL

- No invalid trust in user-provided IDs or state.
- Migrations: uniqueness, referential integrity, safe defaults.
- Queries: ownership/tenant boundaries enforced.
- Seed/bootstrap: no insecure initial credentials.

## Caddy / Operations

- Reverse-proxy rules do not expose internal routes.
- Environment, secrets, CORS, headers, deployment assumptions checked.
- Windows dev ↔ Linux production portability when required.
