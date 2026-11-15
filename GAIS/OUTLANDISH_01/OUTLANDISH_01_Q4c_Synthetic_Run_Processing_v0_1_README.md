# OUTLANDISH_01 — Q4b Windows checkpoint / Q4c synthetic processing slice v0.1

**15 November 2026 (Australia/Adelaide).** Qualification and implementation support only. Does **not** authorise or enable a production REAL/NULL scan, Q5 or forecasting. Ratified consolidated matching/reporting specification v0.2 remains binding.

## Q4b Windows result supplied by the owner

`Q4 PUBLISHED-SOURCE ADAPTER SYNTHETIC PASS: refusals=69 real-production-scans=0 real-history-reads=0`

**Interpretation: PASS on Windows.** The Q4b harness has 69 unconditional refusal cases and one optional symbolic-link negative case. The author reproduced 70 on Linux with symlink creation available; the Windows result of 69 is consistent with no permission to create the test symlink, which the harness deliberately skips. It is *not* evidence of a failed mandatory check. The full source/receipt/era preflight remains synthetic-only: no 5 GB production source was opened by this qualification. The distinct production-source preflight and genuine Powerball drawset will require integration/validation at Q4 final checks.

This Q4c overlay is incremental: it does not replace or rewrite the three Q4b files. Keep Q4b and older Q4a/Q3 source and evidence.

## New files

- `OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1.py` — a strictly **synthetic-only** run module using the pre-existing Q4b published-format receipt guard, the Q3 v0.4 streaming matcher, and existing strict event loader and event classifier. There is **no command-line scientific run mode** and the API refuses non-test `FixedRoots` and REAL/NULL types.
- `OUTLANDISH_01_Q4c_Synthetic_Processing_Qualification_v0_1.py` — temporary-sandbox qualification, two modes.
- This README.

No existing file is overwritten. All three belong inside `GAIS/OUTLANDISH_01/`.

## Windows commands from repository root

First the independently runnable, standard-library-only guard mode:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4c_Synthetic_Processing_Qualification_v0_1.py" --self-test
```

Author's local output:

`Q4C SYNTHETIC GUARDS PASS: isolated-runs=0 guard-refusals=10 production-scans=0 REAL-history-reads=0`

Then the full synthetic integration (requires already installed Q3 v0.4, Q3 event interface/classifier, NumPy, and Q4b):

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4c_Synthetic_Processing_Qualification_v0_1.py" --run
```

**Target output if the actual Q3 modules pass the integration:**

`Q4C SYNTHETIC INTEGRATION PASS: isolated-runs=4 guard-refusals=26 production-scans=0 REAL-history-reads=0`

Do not claim that second line as owner-verified until executed on Windows. Locally, the author exercised 4 processing runs and 26 refusals using *temporary standalone Q3 test doubles only* to check the Q4c plumbing; the real Q3 matcher/classifier was **not** imported for that local integration run. The Q4c guard-only mode did run against the actual Q4b validator source. An owner Windows run is therefore essential, and differences are to be investigated, not waived.

## Slice guarantees and qualification target

1. **No actual production inputs:** `TEST_REAL` and `TEST_NULL` only. The marked synthetic root contains newly created `digits`, `histories`, `results` and `results_null`. Exact six original constant filename templates and production receipt sample-plan schema are exercised using an artificial 10,001-digit high-first BCD source, with a canonical pad nibble and physical source SHA validated by the Q3 streaming engine. Neither `G:` nor an isolated genuine lottery history is opened by the harness.
2. **Inputs and file separation:** TEST_REAL consumes fixed three-row artificial PB or Oz history with integer IDs 11–13 / 21–23; TEST_NULL **generates independent random decoy outcomes** from an explicit integer seed, with 1–8 separate three-draw histories per NULL run. `DECOY-0001-0001` etc. remain text identifiers in NULL `raw_events.csv`, never REAL numeric IDs. No REAL drawset is admitted into the NULL index. NULL stores `decoy_histories.csv` bytes plus SHA-256, seed, K, generator label and scan evidence; replay checks the preserved bytes without re-generating them.
3. **Lifecycle:** New run directories only; manifest starts `INCOMPLETE`. The scanner returns full input-file SHA/byte count; Q4b receipt gate checks them. The runner verifies the output CSV SHA, sorted identity/EOF using the existing strict event reader, semantic matches using the existing classifier, event counts, and game/type/drawset/decoy identity **before** replacing the manifest atomically with `COMPLETE`. Injected post-scan error stays INCOMPLETE; replay refuses it.
4. **Read-only replay:** TEST_REAL rechecks the original artificial history digest; TEST_NULL rechecks its stored decoy bytes/digest and reconstructs private numeric IDs in memory solely for existing strict event/classifier validation. Neither opens the source BCD. One positive test temporarily moves the packed binary out of the synthetic fixture tree to prove this.
5. **Adversarial checks:** creation collisions; changed REAL event/history/receipt; changed NULL decoy/event bytes; type/identity spoof; incomplete manifest; wrong seed/type. Four isolated runs exercise each game × each test type. Synthetic planted K7/K7S/K7mix and decoy matches require positive events, avoiding vacuous zero-only tests.

## Limits, gates and next steps

This is **Q4c synthetic plumbing**, not final Q4 or a production runner. Real published-root execution remains absent; no actual 5 GB whole-file SHA was performed. Q4b's Oz REAL profile remains **blocked**, because the approved isolated modern-era Oz file and bounds have not yet been confirmed. No arbitrary path overrides, no production registry, no Q5 and no forecasting features have been added. K=8 maximum is deliberately a temporary *synthetic-harness* bound, **not** a decision changing proposed K=19/K=99 real NULL study settings.

After Windows PASS, preserve the exact output and update the existing `OUTLANDISH_01_Living_Decisions_and_Progress.md` as a dated checkpoint (do not replace earlier evidence). Remaining Q4: approved Oz history identification; audited production history/receipt preflight binding; actual separately authorised source adapters and scientific REAL/NULL run modes; full reporting (overlap, expectations, chronology, permutations/Holm), independent tiny oracles, final Q3/Q4 owner review. Retain owner's veto option for the primary W→W+1 metric before any qualified REAL scan.

Before any Git write on the user's Windows checkout, inspect `git status --short` and stage **only** `GAIS/OUTLANDISH_01/`. Other parent-project uncommitted files must not be staged, modified or cleaned. This package creates no Git commit or production file automatically.
