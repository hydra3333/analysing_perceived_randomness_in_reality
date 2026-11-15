# OUTLANDISH_01 — Q3 v0.4 / Q4 synthetic run guards v0.1

**15 November 2026 — synthetic qualification only.** The owner-approved uniform **4,000,000 packed-byte default** replaces automatic RAM-based selection. **8,000,000 packed bytes** remains available through the `chunk_bytes` override. Existing v0.3 files remain unchanged.

## Contents

- `OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py` — shared Powerball/Oz engine with fixed 4 MB default and preserved streaming semantics.
- `OUTLANDISH_01_Q4_Fixture_Run_Guards_v0_1.py` — *synthetic fixture* source/receipt/drawset/manifest and result-type isolation proof of concept; **no REAL or NULL production entry point**.
- `OUTLANDISH_01_Q4_Fixture_Guards_Qualification_v0_1.py` — temporary artificial qualification harness.
- This README.

The three Python files use the already-installed Q2/Q3 scripts and NumPy; no new dependencies. Tests never select the real lottery histories, published G:/T: packed constants, REAL results or parent-project working files. Do not invoke the fixture APIs directly on production files.

## Run from the repository root in Windows CMD

Extract the ZIP into your repository root, preserving the `GAIS\OUTLANDISH_01\` paths. Keep distribution ZIPs outside the repository.

Self-test:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4_Fixture_Guards_Qualification_v0_1.py" --self-test
```

Full fixture-only qualification:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4_Fixture_Guards_Qualification_v0_1.py" --run
```

Expected final line starts:

`Q4 FIXTURE GUARDS PASS: isolated-scope-runs=4 guard-refusals=53 v0.4-oracle-regressions=51`

Please return the final PASS line or first traceback. The source need not be committed until the Windows tests pass.

## What this proves and does not prove

- **Four temporary runs:** fictional `TEST_REAL` and `TEST_NULL` histories for both Powerball and Oz. `TEST_REAL` has synthetic integer draw IDs 1–3, never actual Powerball-era IDs; `TEST_NULL` produces typed text `DECOY-0001`–`DECOY-0003` labels in a completely separate fixture result root. These are test analogues, not approved real/null inputs.
- **Receipt and whole-input SHA:** synthetic high-first packed BCD receipt fields must agree with the input format, identity, size and hash. A tiny fixture deliberately uses one entire-file SHA sample. Production receipt sampling and source selection remain to be implemented separately.
- **Incomplete-to-complete lifecycle:** each new test run writes an `INCOMPLETE` manifest, verifies the source while streaming a create-only CSV, and atomically marks the manifest `COMPLETE` only on success. Interrupted runs remain ineligible for replay.
- **Read-only event replay:** the loader verifies stored receipt identity, original drawset SHA, manifest type and counts, and event CSV hash/order/identity/EOF. It reclassifies from events + draw records without opening the packed source. A positive test deliberately removes the binary before replay.
- **Adversarial cases:** 53 refusal checks cover type cross-feeds, tampered hashes/records, duplicate and out-of-order events even with updated event digest, prefix EOF, bad identifiers, incomplete runs, illegal chunk overrides and path/profile substitutions. The new matcher and old v0.3 produce byte-identical event files and independent-oracle-equal tuples in 51 synthetic comparisons.

**Not Q4 COMPLETE:** no published-root selection, official receipt sample-plan validator, installed Powerball/Oz exact era drawset adapters, NULL K-history generation, REAL report reader, analytical/permutation tests or Q5 production access. Tests and source were constructed for **small temporary synthetic inputs only**. Ratified matching/reporting v0.2 continues to govern. The next stage will implement the actual source/profile guards separately and qualify them before any production run.

After Windows PASS, review `git status`, then stage **OUTLANDISH only**:

```bat
git add GAIS/OUTLANDISH_01/
git commit -m "OUTLANDISH Q3 v0.4 and Q4 fixture run guards"
git push
```

Do not commit downloaded distribution ZIPs. The overarching project's unrelated working files must remain untouched.
