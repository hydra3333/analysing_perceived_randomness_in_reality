# OUTLANDISH_01 — Q2 unchanged-scanner/independent-oracle comparison

**Date:** 14 November 2026. **Status:** test aid; NOT a new ratified specification, not a qualified REAL run. Keep the unchanged historical `OUTLANDISH_WSL/wsl_scan_packed_powerball.py` unchanged.

## Installation

Extract the ZIP at your existing Git repository root on the **Ryzen 3900X**, preserving `GAIS/OUTLANDISH_01/`. The ZIP contains this README and **one new Python script**, and does not overwrite the existing independent Q2 oracle.

## Run (Windows CMD from repository root)

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q2_LegacyScanner_Comparison_v0_1.py" --self-test
```

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q2_LegacyScanner_Comparison_v0_1.py" --run
```

Both commands verify **exact tracked Git blob identities** of the reference scanner and Q2 oracle; if either differs, the harness refuses until we review the change. The first command does not run the old scanner or create any files. `--run` then:

- Creates tiny artificial digit streams and a deliberately synthetic drawset in a temporary directory (not any REAL drawset or 10^10 constant).
- Sets the first 32 artificial digits to the recognised **phi prefix** solely because the unchanged old scanner enforces a known-prefix check. **The synthetic file is not a mathematical constant**, is labelled `Q2_SYNTHETIC_ONLY`, and is destroyed after testing.
- Supplies a self-contained test-only conversion receipt so that the unchanged scanner's existing validation code can be exercised.
- Uses the old scanner's configurable 32-digit chunk size to test odd/even starts, crossed boundaries, independent family EOF, repeated matching keys, Powerball equal to a main, main >20, multiple draw attributions, and exact saved event strings.
- Compares the scanner's original P1/P2/P3 outputs with the independent plain-Python oracle's original-baseline views, **by exact (draw, category, start, digits) tuple**, without changing the original scanner.
- Deliberately refuses invalid BCD, wrong whole-file SHA and disallowed draw ID 1577.
- Checks the `G:\OUTLANDISH_01\large_artifacts\results` directory listing and metadata before/after to verify that REAL outputs were not changed. It never opens or scans the 5GB production files.

## Important anticipated Q2 finding

Source inspection suggests a **prefix eligibility defect** in the historical scanner: when `--prefix-digits` is less than the whole-file digit count, the scanner's lookahead comes from the **full file** rather than stopping at the requested prefix. It may incorrectly report a match whose **start lies inside the prefix but end lies outside it**. The scenario `PREFIX_END_EOF_ELIGIBILITY` tests precisely this boundary. If it reports `Q2 FINDING` and the overall exit is 1, that is a **scientific qualification finding**, not a reason to rerun the 5GB scan or modify the unchanged historical scanner. Record the exact extra rows; the Q3 shared engine must implement the correct per-family `start+length<=effective_N` limit.

If all scenarios pass, **Q2 still remains open** until the other ratified mutations and boundary tests are reviewed. A full Q2 PASS is never declared merely from this one test aid.

## Reporting back

Paste the `Q2 HARNESS SELF-TEST` line, then the `PASS:` / `Q2 FINDING:` lines and the final `Q2 ...` summary from `--run`. Full logs and successful row dumps are unnecessary. Preserve prior Q1 and original scientific CSVs; no further legacy data cleanup is needed. Add the final Q2 outcome to the one living decisions/progress record after inspection, rather than rewriting it after each small test.
