# Checklist: Admin & Privileged Operations

> ⚡ **Before using:** Run `check-5s.md` to ensure this depth is necessary.

Validate against this list when changes touch admin panels, roles, or elevated permissions.

- [ ] Admin routes require role check on backend
- [ ] No admin functionality reachable via URL manipulation
- [ ] Privilege escalation: user cannot assign themselves higher roles
- [ ] Admin actions logged with actor, action, target, timestamp
- [ ] Destructive ops require confirmation + are reversible or audited
- [ ] Default admin credentials do not exist in production
- [ ] Admin API endpoints are not exposed publicly
- [ ] Role changes propagate to active sessions immediately
