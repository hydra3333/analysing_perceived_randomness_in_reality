# OUTLANDISH_01 — 14 Nov 2026: Q1 PASS, safe 10^9 retirement, Q2 oracle

**Scope:** supplementary update to the already supplied `OUTLANDISH_01_Operational_Handover_2026-11-14_v0_8.md`. Keep the original handover, ratified matching v0.2 and saved run CSVs. Extract this ZIP at the repository ROOT on the Ryzen, preserving its directory structure. No files are installed to G: by extraction; all large files remain outside Git.

## Confirmed starting point

- 14 Nov 2026 owner-run Q1 tool: `Q1 STATUS: PASS` across all six Powerball category/prefix comparisons. Packed φ 227 saved baseline events, first 1e8 has 3 P3, first 1e9 has 25 P3, zero old-only/new-only, all known offset checks PASS.
- Owner-run legacy 6-file audit: `HASHED_PASS`, each old 1GB file matches its old active TOML record. Audited TOML SHA `1718ab895a0479d437ac1f376585a3aea6cb864b722d96d2487ad21ac4236fe5`.
- Six 5GB packed BCD files are present with receipts; no new production scan is needed for legacy cleanup. The `outlandish.local.toml` legacy registry is deliberately kept separate from packed BCD receipts.

## 1. Read-only preview on Ryzen

Close all old OUTLANDISH scanners/generators and ensure no other process is using the old 1GB files. From the repository root:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Legacy_1e9_Retirement_v0_1.py"
```

Expected: Q1 PASS, six known packed file/receipt identity checks, six old files present and correct sizes; `PREVIEW PASS`. This mode doesn't write, hash 6GB, deactivate or delete.

## 2. Archive + deactivate ONLY the legacy registry (old binaries retained)

After preview PASS, run:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Legacy_1e9_Retirement_v0_1.py" --deactivate --confirm-idle
```

This reruns exact Q1, rehashes all six old 1GB files, checks six new packed receipts/sizes, creates a unique small archive on `G:\OUTLANDISH_01\large_artifacts\logs\legacy_1e9_retirement_*\` containing the exact original TOML and `retirement_evidence.json`, then uses the existing `outlandish_config.save_generated_state({}, {})` locked atomic writer to clear only the legacy generated active records. The old 1GB files are **still on disk**. Existing automatic `.toml.bak` remains. If anything fails, stop and inspect without manually editing files.

Check new registry state:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\outlandish_artifacts.py" status
```

Expected: `active=NONE` for all six, pending NONE. This **does not mean** the 10^10 packed files vanished; the new scanner reads its receipts, not this incompatible old registry.

## 3. Physical deletion — separate explicit action

Only after archived evidence exists and registry is empty: the script printed a complete single-line `--delete --manifest ... --confirm-idle` command containing the actual unique G: evidence file path. Run THAT printed command, without guessing the folder name. It rehashes the six surviving old binaries, rechecks the six packed file/receipt identities, and unlinks **only** the exact six legacy `.bin` paths. It never removes a receipt, newer packed file, CSV, scientific result, validation report, or any other file. Partial deletion can be retried with the SAME manifest; mismatched old file content blocks all further deletions. No wildcards.

Finally run:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\outlandish_artifacts.py" validate
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\outlandish_artifacts.py" status
```

Expected after success: zero legacy active/pending records. Review `git status --short` and intentionally decide whether to commit the changed TOML; no G: large binaries should enter Git. Do **not** run the legacy `scan_1e9.cmd` or `scan_1e10.cmd` after registry deactivation.

**Important:** this script was static-checked and exercised in a simulated small-file environment (normal path, tampering refusal, exact deletion, retry). It has NOT yet been executed on Windows or the real G: files. Its apply phase is deliberately gated to the exact TOML SHA and known paths from the owner's current audit. If any file/settings changes, it refuses rather than guessing.

## 4. Q2 independent oracle — no production activity

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q2_Independent_Oracle_v0_1.py" --self-test
```

This is the start of Q2: a small independent pure-Python decimal-string reference for PB P1/P2/P3 and Oz O1/O2/O3, with synthetic planted fixtures, actual-order/subsequence flags, PB/main equality, special-slot tests, zero/odd/EOF checks and BCD padding. It creates no result files and reads no REAL draws or 5GB digits. Its self-test passed in the assistant's container.

Q2 is **NOT yet complete**: next compare exact synthetic event tuples against the *unchanged* prior packed scanner, using only an isolated TEST result location, then expand required mutation canaries and source/hold-out refusal tests. No Q5 production scans, no future forecasting method integration.
