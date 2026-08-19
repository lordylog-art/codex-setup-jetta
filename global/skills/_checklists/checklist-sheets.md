# Checklist: Google Sheets & Apps Script

> ⚡ **Before using:** Run `check-5s.md` to ensure this depth is necessary.

Validate against this list when changes touch Sheets, Script Properties, or Apps Script services.

- [ ] Batch getValues/setValues (no cell-by-cell loops)
- [ ] LockService used for concurrent trigger access
- [ ] Script properties: no secrets in code, use PropertiesService
- [ ] Input from google.script.run validated server-side
- [ ] Trigger function names not renamed (breaks installable triggers)
- [ ] appsscript.json scopes reviewed for minimal permissions
- [ ] Error handling returns user-meaningful messages
- [ ] HTTP integrations: retries, non-2xx handling, auth header centralized
- [ ] No hardcoded spreadsheet IDs in code (use config/properties)
- [ ] Time-driven triggers respect 6min execution limit
