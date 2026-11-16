# OUTLANDISH_01 Q4k D4/D5 Powerball reporting correction v0.1

Date: 16 November 2026 (Australia/Adelaide)
Baseline: Q4j commit `103d274`, Claude D4 review memo 005/handover v0.5 (`8b7eaa2`).
Owner decisions: D4 (geometric-mean primary, median secondary); D5 (corrected historical exposure, freeze, no exclusions).
This is an implementation overlay, **not** a REAL scan authorisation. `ENABLE_Q5_PRODUCTION_SCANS` remains `False` and the production entry point is not changed.

## Contents

- `OUTLANDISH_01_Q4d_Statistical_Core_v0_1.py`: D4 math, one permutation loop for both summaries, same seed, 12-place rounded mean log10(g+1), retained median outputs, and observed primary transition summary. Oz remains on its existing median-only route until separately decided.
- `OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1.py`: V3 report schema, explicit primary/secondary IDs, fixed D5 text, strict loader identity validation. All historical median fields remain, including the old top-level median permutation fields for reviewer compatibility; **the new primary p is under `permutation.geometric_primary.centered_two_sided_p`.**
- `OUTLANDISH_01_Q4h_Powerball_Test_Aggregate_v0_1.py`: V3 aggregate, distinct six-constant Holm corrections for primary and exploratory median secondary, fixed D5 text, strict primary identity validation.
- `OUTLANDISH_01_Q4h_Powerball_Test_Qualification_v0_1.py`: strengthened existing TEST_REAL synthetic integration assertions for both p families and D5, no genuine files.
- `OUTLANDISH_01_Q4k_D4_Statistics_Qualification_v0_1.py`: independent brute-force 10,000-shuffle synthetic oracle, hand-checked zero gap, all-empty N/A, original median compatibility, two separate Holm families.

## Qualified tests and limits

Ran locally (stdlib only):

- Q4d `--self-test`: PASS, 1025 hand-checks/13 refusals.
- Q4k focused synthetic statistical test: PASS, including independent 10,000-permutation oracle.
- Mocked synthetic full report/aggregate persistence, six reports and two Holm families: PASS (four provenance-tamper refusals). The mocked integration is a development check, not a substitute for the existing installed Q4h test.
- `py_compile` of all changed modules: PASS.

**Not yet run here:** the full Q4h `--run` and Q4i `--run` integration, because the container copy lacked installed Q3 source modules. Those tests must run in the owner's complete Windows checkout before install is accepted. No REAL, legacy-history or G: source was opened for these tests.

## Suggested owner Windows commands, after installing overlay in repo root

```
".venv\Scripts\python.exe" -B "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4k_D4_Statistics_Qualification_v0_1.py"
".venv\Scripts\python.exe" -B "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4h_Powerball_Test_Qualification_v0_1.py" --run
".venv\Scripts\python.exe" -B "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4i_Targeted_Qualification_v0_1.py" --run
".venv\Scripts\python.exe" -B "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4i_Production_Entry_v0_1.py" status
```

Then stage only the five source/test files and this README within `GAIS/OUTLANDISH_01/`. Do not stage parent project data, results, or local G:/T: artifacts. Confirm Q5 remains DISABLED before commit. Claude should perform the promised one focused check of the changed statistical/reporting modules before the owner makes the separate Q5 decision.

## D5 scientific record

The corrected fixed disclosure string is stored once as `D5_LEGACY_EXPOSURE_DISCLOSURE` in the report module and reused unchanged in all six reports and their aggregate. It explicitly acknowledges five signed legacy P3->P3 gaps already printed in historical draft §5.2. It does not assert the legacy dataset was wholly blind or that no gaps were calculated.

The freeze bars further legacy positional analysis until qualified REAL Q5 reports exist. The known-answer exception permits only direct set comparison of `(draw, start offset, matched digits)` for the saved 227 phi P3 rows against the first genuine phi K6S events, outputting matched/missing/extra counts and differing rows; **no new gap calculations or summaries**. No changes to scanner, match event storage, receipt guards, P1/P2 summaries or six-constant inclusion.

Add the D4/D5 decisions and corrected disclosure to `OUTLANDISH_01_Living_Decisions_and_Progress.md` before any owner Q5-authorisation commit. Claude's v0.6 handover is complementary; neither this overlay nor the handover authorises scanning.
