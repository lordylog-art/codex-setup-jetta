# Testing and Clasp

## Local Testing

- Test pure helpers in Node whenever possible.
- Mock Apps Script globals instead of coupling unit tests to the live platform.
- If the repo already uses `vm`, fixture files, or runtime stubs, extend that harness instead of replacing it.
- Cover auth flows, payload transformation, pagination, and error normalization first for API-heavy projects.

## Review Focus

- Check for hidden runtime dependencies on Apps Script globals.
- Check for trigger breakage caused by renamed functions.
- Check for quota-heavy loops and repeated remote calls.
- Check manifest changes in `appsscript.json` for scope or deployment impact.

## Clasp Workflow

- Read `.clasp.json` before changing deployment assumptions.
- Keep source layout aligned with how `clasp push` expects files.
- Avoid introducing generated artifacts unless the repo already commits them.
- If a build step exists, update the source of truth rather than only editing generated output.

## Manual Verification

Use a concrete validation path when automated tests are incomplete:

1. Identify the entrypoint function, trigger, or web app route.
2. Verify required script properties, user properties, or secrets.
3. Run the smallest realistic scenario.
4. Confirm logs, returned payloads, and persisted side effects.
