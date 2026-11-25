# Local delivery evidence

Python stdlib and Git are required. Capture the finished source candidate **before**
running Super QA, then seal its completed result:

```text
python -B scripts/delivery.py capture --project ROOT --out ROOT/.local/candidate.json
python -B scripts/delivery.py seal --project ROOT --candidate ROOT/.local/candidate.json --report ROOT/.super-qa/RUN/result.json --suite delivery --out ROOT/.local/packet.json
python -B scripts/delivery.py check --project ROOT --packet ROOT/.local/packet.json
```

Repeat `--suite` for each required suite. Outputs must be new files outside the
project or inside its already ignored `.local/`; existing files are never replaced.
No command runs tests, changes Git, updates tickets or grants acceptance.

Snapshot v1 has `version`, absolute `project`, UTC `createdAt`, `environment`
(`python`, `platform`) and `files` (relative POSIX path → SHA256 of bytes).
Packet v1 has `version`, `status=REVIEW_REQUIRED`, `snapshot`, `report`
(`path`, `sha256`), `required` and `summary`. Schemas are defined in the modules;
malformed or stale inputs fail with exit 2. `CURRENT` / `MANUAL_REVIEW_REQUIRED`
only confirms equivalent inventoried files, report bytes and recorded environment.

All tracked and nonignored untracked files count, including binary/config files.
Links, directories and missing capture members are rejected. Ignored runtime data,
external environment, DB, browser, credentials and semantic test sufficiency are
not certified. Report provenance is declared metadata, not cryptographic authenticity.
This tool does not infer dependencies, and concurrent edits require a fresh check.

Native tests use temporary local Git repositories and subprocess CLI calls:

```text
python -B -m unittest discover -s scripts -p test_delivery_*.py
```
