# OUTLANDISH_01 — Q4e synthetic reporting and provenance integration v0.1

**15 November 2026 (Australia/Adelaide). Synthetic-only qualification, not Q5 authorization.**

## Current checkpoint

Owner-reported Windows results **PASS** for Q4d:

- `Q4D SYNTHETIC ARITHMETIC PASS: hand-checks=1025 guard-refusals=13 synthetic-scans=0 fixture-reports=0 production-scans=0 REAL-history-reads=0`
- `Q4D SYNTHETIC INTEGRATION PASS: hand-checks=1025 guard-refusals=13 synthetic-scans=4 fixture-reports=2 production-scans=0 REAL-history-reads=0`

Earlier Q4a/Q4b/Q4c synthetic Windows results also passed. This does **not** qualify a REAL scientific run. Q5 is still blocked pending final integration correctness, implementation ratification and explicit owner authorization. The proposal for primary W->W+1 significance remains owner-vetoable before any REAL run.

## Scope and components

Three **new** files in `GAIS/OUTLANDISH_01/`, preserving earlier Q1–Q4 evidence and scripts:

- `OUTLANDISH_01_Q4e_Synthetic_Report_Bundle_v0_1.py`: no runnable production entry point; uses Q4c verified COMPLETE TEST runs. Re-derives Q4d summaries and physical overlaps from verified raw events and historical test drawset, or returns strictly grouped NULL decoy summary counts. All computations are without reading the packed source again. Materializes create-only `report.json` and `report_manifest.json` under separate TEST-only `reports_test_real/` and `reports_test_null/` paths inside the **marked temporary sandbox**. `INCOMPLETE` until run and report source and code/file SHA checks pass. The report replay checks current implementation SHA digests and recomputes report bytes from the persisted verified sources. The REAL–NULL comparator loads independently verified summaries, never combines or joins raw events.
- `OUTLANDISH_01_Q4e_Synthetic_Report_Qualification_v0_1.py`: pure guards and four synthetic end-to-end runs, source-proof replay, mutations, and failed-run refusals.
- This README.

**No new production registry, no production REAL/NULL scanner/report CLI, no parent-project changes, no G:/T: access, no genuine drawset reads, no 5-GB input scans, and no Q5.** Q4e depends only on the already-installed Q3 v0.4, Q4b, Q4c and Q4d source files plus Python/NumPy dependencies already used by the project.

## Windows CMD qualification

Unzip into the checkout root, preserving the `GAIS\OUTLANDISH_01\` folder structure. Then run from the checkout root:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4e_Synthetic_Report_Qualification_v0_1.py" --self-test
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4e_Synthetic_Report_Qualification_v0_1.py" --run
```

Expected last lines:

```text
Q4E SYNTHETIC GUARDS PASS: source-runs=0 reports=0 guard-refusals=10 production-scans=0 REAL-history-reads=0
Q4E SYNTHETIC INTEGRATION PASS: source-runs=4 reports=4 guard-refusals=39 production-scans=0 REAL-history-reads=0
```

**Qualification evidence precision:** Local tests completed with Python 3.13 and temporary synthetic *Q3 scanner/classifier stand-ins*; those were **not** part of this ZIP. The `--run` command on the owner's Windows installation will test Q4e with the **actual** installed Q3 v0.4 matcher, Q3 event classifier and Q4b/Q4c/Q4d implementations. Do not claim the Windows result before it is received.

## Refusals/evidence preserved

The harness checks: exact TEST type and output isolation; create-only report folders; independently reconstructed REAL versus NULL summary counts; recorded source manifest, receipt, events, decoys and code digests; original Q4c output files unchanged; changed report with a recomputed SHA still rejected by semantic replay; INCOMPLETE-derived report refused; four existing TEST runs replayable even with packed input physically absent. All tests use `TemporaryDirectory` and synthetic marker; no external files are modified.

## After Windows PASS

1. Record the Windows result in `OUTLANDISH_01_Living_Decisions_and_Progress.md` as a new dated progress entry **without rewriting earlier evidence**. Do not mark full Q4 or production readiness PASS just from this synthetic slice.
2. Independently review remaining final integration gaps, particularly approved isolated Oz modern drawset/era/cutoff, provenance boundaries, actual REAL/NULL production entry-point design and failure handling, reporting all-empty and six-constant family conventions.
3. Obtain the owner's final implementation ratification and separate approval before any Q5 scientific production scan. Don't infer approval from the testing result.
4. Before committing, inspect `git status --short`; stage **only** `GAIS/OUTLANDISH_01/` after the owner is satisfied. Parent project has unrelated uncommitted work.

This packaging is intentionally not a license to run REAL published data. The previous v0.2 ratified matching/reporting science remains binding.
