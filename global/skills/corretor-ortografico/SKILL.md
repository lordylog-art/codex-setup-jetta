---
name: corretor-ortografico
description: Extract user-facing strings directly from source files, check Portuguese Brazil copy with a local LanguageTool install, and apply safe copy fixes back to the same files. Use when Codex needs to audit/correct PT-BR spelling, accents, grammar, or punctuation in project strings without opening the site, especially React/Next.js pages, TypeScript modules, UI labels, messages, and operational dashboards.
---

# Corretor Ortografico

## Core Workflow

1. Run `scripts/audit-source-copy.mjs` from the project root against source paths.
2. Read the generated report, which includes file, line, column, original text, suggestions, and `suggestedText`.
3. Separate safe fixes from risky suggestions.
4. Edit source strings manually with `apply_patch`; do not blindly apply every LanguageTool suggestion.
5. Rerun the audit for the affected paths and run the closest practical tests.

## Audit Script

Use the bundled script:

```powershell
node C:\Users\Jetta\.codex\skills\corretor-ortografico\scripts\audit-source-copy.mjs `
  --path apps\web\src `
  --language pt-BR `
  --language-tool .\tools\LanguageTool `
  --out .\tmp\corretor-ortografico-report.json
```

For multiple areas, repeat `--path`:

```powershell
node C:\Users\Jetta\.codex\skills\corretor-ortografico\scripts\audit-source-copy.mjs `
  --path apps\web\src\app `
  --path apps\web\src\components `
  --path apps\api\src
```

Useful options:

- `--max-items 200`: cap LanguageTool checks while iterating.
- `--include-tests`: include `.spec.*` and `.test.*` files.
- `--min-length 2`: catch shorter labels, with more noise.

The script:

- reads source files directly; it does not use Playwright or open the site;
- extracts string literals, template literal text, and JSX text via the TypeScript parser;
- skips obvious technical strings such as imports, `className`, URLs, paths, IDs, and test IDs;
- starts the local LanguageTool HTTP server when needed;
- checks each unique extracted string with `language=pt-BR`;
- writes a JSON report with source occurrences, `matches`, `replacements`, and `suggestedText`.

## Fix Policy

Apply automatically only when the fix is obviously safe:

- missing accent in common Portuguese words: `Nao` -> `Não`, `possivel` -> `possível`;
- clear UI copy typo with one strong suggestion;
- punctuation spacing issues that do not change meaning.

Review manually before applying:

- names, brands, route labels, vehicle classes, client names, acronyms, IDs;
- domain terms from logistics, Greenmile, SAC, ERP, spreadsheet imports;
- suggestions inside numbers, addresses, plate codes, emails, URLs, or technical tokens;
- any replacement that changes sentence meaning.

Never edit generated build output such as `.next`, `dist`, logs, or reports. Fix source files only.

## Validation

After fixes:

1. Rerun `audit-source-copy.mjs` for the same source path.
2. Run the closest tests for changed files. For UI copy changes, prefer render/interaction tests when text is part of the user flow.
3. If a string controls behavior, labels an accessible element, or appears in a modal/stateful flow, follow the repo's TDD policy and protect the real flow, not only a helper.

Pure copy/accent corrections can be validated by the audit plus existing render tests unless the text controls behavior.
