# OUTLANDISH_01 — Q4i shared Powerball mode v0.1

**16 November 2026. Windows qualification required. Synthetic-only testing; Q5 switch remains OFF.**

This is the Review B follow-up, based on Claude's `REVIEW/OUTLANDISH_REVIEW_003_Claude_to_ChatGPT.md`. It does **not** ratify a production run, inspect genuine 5 GB packed files, read genuine Powerball history or access the parent project's holdout. Only files under `GAIS/OUTLANDISH_01/` are included.

## Files in this overlay

The existing Q4h runner, reporter and aggregator are *updated in place*, **not copied** into a second REAL stack:

- `OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1.py` — same run/science path for TEST_REAL and REAL; scan launch checks the Q5 switch inside the runner, even on direct calls.
- `OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1.py` — 10,000 fixed permutations; existing synthetic fixture seed `271828`; production deterministic seed derived per `(game, constant)`; report load uses recorded digests; optional explicit audit.
- `OUTLANDISH_01_Q4h_Powerball_Test_Aggregate_v0_1.py` — six REAL reports produce Holm without NULL; aggregates live under the existing guarded `results/` root; ordinary load verifies six report digests rather than regenerating the whole aggregate. Historical synthetic aggregate IDs map to the new guarded location to preserve the existing tests.

New small files:

- `OUTLANDISH_01_Q4i_Mode_v0_1.py` — immutable mode, with exactly two constructors: `synthetic(roots,profile,digits)` and `production_powerball()`. The latter is read-only at construction and usable for loading completed results with the Q5 switch OFF; it does **not** start a scan.
- `OUTLANDISH_01_Q4i_Production_Entry_v0_1.py` — one entry point and one `ENABLE_Q5_PRODUCTION_SCANS = False` switch. The owner's eventual reviewed commit changing it to `True` is the explicit Q5 scan authorisation record. There is **no** command-line or environment bypass. `status` is safe; `scan` refuses while OFF; report/aggregate of already qualified REAL results do not require the switch.
- `OUTLANDISH_01_Q4i_Targeted_Qualification_v0_1.py` — test-mode and unsampled-source-corruption checks, including four temporary guard-removal canaries. All artifacts are under Python `TemporaryDirectory`; mocked guard removal is restored before exit.
- This README.

**Excluded deliberately:** no rewrite of Q3 or Q4d; no rewrite of Q4a–Q4g; no extra registry; no Oz profile guessed; no new NULL scanner; no separate 433-draw test; no additional approval machinery.

## Fixed seed rule — owner decision D1

For a qualified REAL Powerball report, the exact seed is the first 8 bytes, interpreted as an unsigned big-endian integer, of SHA-256 applied to the ASCII string:

`OUTLANDISH_01|powerball|<constant>|PRIMARY_W_TO_W1|V1`

where `<constant>` is one of `pi, phi, e, log2, gamma, lemniscate`. The report records **both the original text label and the resulting integer seed**. The same rule is implemented for future `oz` although there is no Oz REAL adapter yet. Existing synthetic reviewer comparisons retain seed `271828` and 10,000 permutations.

## Run these Windows CMD checks (repository root)

First, verify the Q5 gate is still OFF:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4i_Production_Entry_v0_1.py" status
```

Expected: `Q5 PRODUCTION POWERBALL SCANS: DISABLED`.

Next, run the existing Q4h checks **unchanged**:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4h_Powerball_Test_Qualification_v0_1.py" --self-test
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4h_Powerball_Test_Qualification_v0_1.py" --run
```

Expected final line for `--run`: `Q4H POWERBALL SYNTHETIC INTEGRATION PASS: runs=6 reports=6 aggregates=1 guard-refusals=27 permutations-per-report=10000 production-scans=0 REAL-history-reads=0`.

Run the **new narrowly targeted** safety checks:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4i_Targeted_Qualification_v0_1.py" --self-test
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4i_Targeted_Qualification_v0_1.py" --run
```

Expected last line for `--run`: `Q4I SYNTHETIC TARGETED PASS: refusals=6 canaries=4 unsampled-fixture-bytes=150000 unsampled-offset=5001 Q5-switch=OFF production-scans=0 REAL-history-reads=0`.

Finally, **reuse Claude's existing realistic 433-draw independent check** — do NOT write another version:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\REVIEW\OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_1.py" --run
```

Expected terminal headline: `REVIEWER Q4H END-TO-END PASS: constants=6 draws=433 permutations=10000 aggregate=REAL-only positive-control=detected corruption=refused`. That script is original independent reviewer work and remains unchanged. Its old synthetic entry-point names continue to call the updated shared implementation.

## Specific integrity check

The Q4i large fixture is **150,000 packed bytes**. Receipt preflight uses its normal twelve 4096-byte samples. The test modifies an **unsampled** byte, confirms that receipt validation still passes, then verifies that the real shared scanner refuses the full-file SHA mismatch, leaves the new TEST_REAL run `INCOMPLETE`, and removes the raw event CSV. A synthetic-only negative canary temporarily disables both stream digest comparisons to prove the test would then detect acceptance of the corrupted file. This is **never run on a real file**.

The other negative canaries temporarily disable the history SHA comparison, mode identity validation, or duplicate event classification, always in temporary synthetic fixtures. They restore the original callable after each negative control. No synthetic run can create a genuine REAL output root.

## Limits and next stage

A local rehearsal with temporary stand-ins for the Q3 engine/classifier passed both Q4h commands and the new Q4i targeted commands. **This is not a substitute for the owner's Windows tests using the actual Q3 v0.4 files.** Claude's independent 433-draw script must also be rerun against the updated code on Windows. No production-mode scan has been executed or enabled.

The upcoming reviewer point C considers this design together with Windows results, safety boundaries, KISS and remaining inputs. A separate owner authorisation is required before a genuine 5 GB Q5 scan. Powerball's proposed P3_any primary remains owner-vetoable; Oz's production drawset/era/cutoff remains unavailable. The six genuine conversion receipts have not received the separately permissioned read-only preflight.
