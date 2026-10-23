# Checklist: Auth & Session

> ⚡ **Before using:** Run `check-5s.md` to ensure this depth is necessary.

Validate against this list when changes touch authentication or session.

- [ ] Auth enforced on backend, not just UI
- [ ] Password hashing uses bcrypt/argon2 with proper cost
- [ ] Session tokens are random, HttpOnly, Secure, SameSite
- [ ] Session invalidation on logout/password change
- [ ] Brute-force protection: rate limit + lockout
- [ ] Password reset tokens expire and are single-use
- [ ] OAuth flows validate state parameter
- [ ] JWT: verify signature, expiration, issuer, audience
- [ ] No credentials in logs, URLs, or error responses
- [ ] MFA enforced on admin/sensitive operations (if applicable)
