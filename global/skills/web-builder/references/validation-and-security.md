# Validation And Security

## Minimum Quality Gate Per Change

1. Confirm the intended behavior and trust boundary.
2. Add or update the most relevant automated test.
3. Run targeted tests first, then the smallest useful smoke suite.
4. Check whether the backend independently validates:
   - input shape
   - permissions
   - ownership
   - state transition rules
5. Confirm failure cases return safe errors.

## Preferred Test Layers

- Unit tests for pure business rules, mappers, validators, parsers, and calculations.
- Integration tests for repositories, services, auth flows, and domain modules.
- Request or e2e smoke tests for critical API paths.
- Frontend tests for risky client logic, but never as a substitute for backend validation.

## Security Review Prompts

- Can a user read or mutate another user's data by changing an ID?
- Is any permission enforced only in the UI?
- Does the server trust client-calculated totals, statuses, or ownership?
- Are inputs constrained before query building or persistence?
- Are secrets and internal errors excluded from responses and logs?
- Would this endpoint be vulnerable to brute force or enumeration?
- Does this new dependency increase attack surface more than it reduces risk?

## Reporting Standard

State:
- what was tested
- what was smoke-tested manually
- what security checks were reviewed
- what remains unverified
