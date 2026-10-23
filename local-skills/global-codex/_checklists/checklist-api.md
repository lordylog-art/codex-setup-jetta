# Checklist: API & Endpoints

> ⚡ **Before using:** Run `check-5s.md` to ensure this depth is necessary.

Validate against this list when changes touch API routes, controllers, or integrations.

- [ ] Input validated and sanitized server-side
- [ ] DTOs/schemas reject unknown fields
- [ ] Ownership check: user can only access own resources
- [ ] Pagination enforced (no unbounded queries)
- [ ] Rate limiting on public/auth-sensitive endpoints
- [ ] Error responses do not leak internals (stack traces, SQL, paths)
- [ ] CORS restricted to expected origins
- [ ] Content-Type enforced and validated
- [ ] Idempotency for mutating operations where applicable
- [ ] Versioning strategy does not break existing consumers
