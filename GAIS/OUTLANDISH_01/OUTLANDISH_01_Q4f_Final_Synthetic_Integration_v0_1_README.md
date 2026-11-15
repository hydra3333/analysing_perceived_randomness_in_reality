# OUTLANDISH_01 — Q4f six-constant synthetic integration v0.1

**16 November 2026 (Australia/Adelaide). SYNTHETIC qualification only. Not a production runner or Q5 authorisation.**

## Current evidence, in sequence

The owner has reported Windows PASS for all prior stages:

- Q1: saved phi prefix/historical reconciliation PASS, legacy retirement completed.
- Q2: independent PB/Oz oracle and historical-scanner adversarial qualification PASS.
- Q3 v0.4: 51 synthetic streaming/oracle/v0.3 regressions PASS, 4,000,000 packed-byte default.
- Q4a: 4 synthetic isolated runs, 53 refusals, 51 regressions.
- Q4b: synthetic published-source/profile validation PASS; **69** Windows refusals (one optional symbolic-link test unavailable); no production scan or REAL-history read.
- Q4c: Windows `--self-test` 10 refusals; `--run` 4 synthetic runs / 26 refusals.
- Q4d: Windows `--self-test` 1,025 hand checks / 13 refusals; `--run` 1,025 hand checks / 13 refusals / 4 synthetic scans / 2 fixture reports.
- Q4e: Windows `--self-test` 10 refusals; `--run` 4 synthetic source runs / 4 reports / 39 refusals. Both reported `production-scans=0 REAL-history-reads=0`.

These are test qualifications at the **synthetic** level. They do not establish readiness for Q5.

## This package

One **new** stdlib-oriented synthetic qualification script:

- `OUTLANDISH_01_Q4f_Final_Synthetic_Integration_v0_1.py`

The script imports the already-installed Q4b, Q4c, Q4d, Q4e modules and the Q3 matcher/classifier those modules already require. No change to those source files. No new dependencies.

`--run` builds a **temporary** marked sandbox, then exercises the Cartesian product of:

- 2 games: Powerball, Oz Lotto
- 6 constant IDs: pi, phi, e, log2, gamma, lemniscate
- 2 typed run kinds: `TEST_REAL`, `TEST_NULL`

Thus **24** small independent TEST runs and **24** immutable derived TEST reports. Each constant has a distinct artificial BCD source digest and correctly recomputed converter-compatible sample receipt. No actual constant digits, REAL histories, published receipt files, production result roots or parent-project files are read or written.

Additional checks: fixed input identity and full tiny-source hash before `COMPLETE`; complete checked manifests; distinct game/type/scoped output roots; create-only source and report refusals; 6-constant Holm roster *separately by game* (including N/A values); verified REAL-like vs NULL-like **summary-count-only** comparison; cross-game/cross-constant/cross-type report replay refusal; and verified replay of all 24 reports with all six artificial BCD inputs temporarily unavailable. An upstream manifest digest tamper must be refused. Zero-event decoys are valid and must not be mistaken for failed scans.

### Run in Windows CMD from repository root

Extract into the repository root, preserving the `GAIS\OUTLANDISH_01\` paths. This package adds **only the two files listed**; keep the downloaded ZIP outside the repository and review `git status` before staging.

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4f_Final_Synthetic_Integration_v0_1.py" --self-test
```

Expected:

```text
Q4F SYNTHETIC BOUNDARIES PASS: guard-refusals=7 source-runs=0 reports=0 games=2 constants=6 production-scans=0 REAL-history-reads=0
```

Then:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4f_Final_Synthetic_Integration_v0_1.py" --run
```

Expected:

```text
Q4F SYNTHETIC INTEGRATION PASS: guard-refusals=92 source-runs=24 reports=24 games=2 constants=6 production-scans=0 REAL-history-reads=0
```

Local `--run` rehearsal using temporary Q3 scanner/classifier **test doubles** passed; the Windows command above is the actual installed-Q3 integration qualification. **Do not call this a Windows PASS until owner output confirms it.**

## Scientific and operational gates remaining after synthetic PASS

1. **No authorised REAL/NULL production run CLI exists.** The current Q4c/e implementation is intentionally TEST-only; the separate production runner must be designed, reviewed and ratified before Q5. Synthetic PASS cannot be relabelled as production readiness.
2. **Oz modern-era isolated REAL profile/cutoff and source columns remain unconfirmed.** The REAL Oz profile deliberately refuses. Do not substitute parent master histories or invent holdout boundaries.
3. The six real 5 GB inputs and converter receipts have **not** been opened by these synthetic tests. Production sample-plan compatibility and complete 5 GB source digests must be verified at the future authorised run, before `COMPLETE` status. Preserve original files and prior evidence.
4. The six-constant Holm calculation has been independently tested as a pure function and is exercised as an aggregate in this fixture harness, but **a final immutable cross-constant report/manifest and orchestration** are not yet qualified. 10,000 Monte Carlo permutations, stable seed policy and N/A convention must be checked at production-scale feasibility, without a real scan during development.
5. Retain the owner's option to veto/change the proposed P3-any/O3-any primary statistic **before** qualified REAL runs. Null decoy size K and execution cost remain benchmark decisions; the fixture K=2 is deliberately not production K=19/99.
6. A final focused design review and separate explicit owner authority are prerequisites to any Q5 real scan. There is no parent E-method registration or forecast implementation in this work.

## Guardrails

- Only `GAIS/OUTLANDISH_01/` files belong in this package. The parent project has unrelated uncommitted work; do not use `git add .` or a repository-wide cleanup.
- Do not modify the six published packed constants, receipts, old results, production histories or Q1–Q4 evidence.
- Maintain the living decisions/progress record as the authoritative working status after the owner reports Q4f Windows output. Do not overwrite local owner edits to that document with a downloaded older copy.
