# OUTLANDISH_01 — Q4d synthetic statistical qualification v0.1

**15 November 2026 (Australia/Adelaide).** This is a **synthetic-only qualification slice**, not Q4 complete, an alteration of ratified matching/reporting v0.2, a REAL production report, or Q5 authorisation. No parent project source or existing OUTLANDISH file is overwritten. No new registry, permission system or source catalogue.

## Package (two Python files and this README)

- `OUTLANDISH_01_Q4d_Statistical_Core_v0_1.py`: pure statistics/functions with **no source reads, file writes, production runner, or CLI**. Input is assumed to have passed Q4c verified replay and Q3 classification. It performs minimal internal sanity checks but does not replace provenance/firewall validation.
- `OUTLANDISH_01_Q4d_Statistics_Qualification_v0_1.py`: isolated hand-calculated tests and optional full integration through already-installed Q3 v0.4, Q4b and Q4c. Only this test harness creates scratch reports, under a newly marked `TemporaryDirectory`.

## Windows CMD from repository root

First:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4d_Statistics_Qualification_v0_1.py" --self-test
```

Expected:

```
Q4D SYNTHETIC ARITHMETIC PASS: hand-checks=1025 guard-refusals=13 synthetic-scans=0 fixture-reports=0 production-scans=0 REAL-history-reads=0
```

Then (requires existing qualifying files from Q3 v0.4, Q4b and Q4c):

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4d_Statistics_Qualification_v0_1.py" --run
```

Expected:

```
Q4D SYNTHETIC INTEGRATION PASS: hand-checks=1025 guard-refusals=13 synthetic-scans=4 fixture-reports=2 production-scans=0 REAL-history-reads=0
```

**Important**: The second result is not yet verified on the owner's Windows machine. Locally the pure statistics were tested directly; the four-run rehearsal used explicitly non-authoritative Q3 scanner/classifier **test doubles**. The Windows command uses the original installed Q3 v0.4/actual Q4c integration and is the meaningful qualification. If it fails, return the **first traceback**, not a modified local Q3 file.

## Exact conventions implemented

1. Category views: distinct **draw-attributed events**, distinct offset starts, distinct draw IDs; never equate these denominators. Analytical `D * S * max(0,N-L+1)/10**L` and conditional-order `n*q` (binomial two-sided probability-order model p, labelled conditional/approximate because of dependence). Nested views are not summed.
2. **Same-draw physical overlap**: direct interval intersections `[start,start+L)` including shifted and same-start intersections. The integration harness independently compares to existing Q3 interval-sweep results including each family pair, not transitive overlap components. Different-draw same-offset coincidences are preserved but **not** counted as same-draw overlaps.
3. **Adjacent W→W+1**: all consecutive eligible draw positions retained, including empty positions; select pair by `(abs(b-a), b-a, a, b)`, with a negative signed gap winning exact magnitude ties. Keep zero-distance cross-draw coincidences. `median(minimum absolute gap)` only over evaluable pairs, with numerator/denominator stated.
4. **Permutation**: default `10,000` whole-set shuffles including empty positions, deterministic explicit seed, record number of valid and undefined permutations and range of evaluable-pair counts. Undefined medians excluded from p-value denominator; observed undefined or no valid permutations yields **N/A**. For `R_valid>0`: center at median of valid shuffled medians, count distances `>=` observed centered distance inclusive, `(1+b)/(R_valid+1)`. Upper/lower inclusive tails are descriptive. **The P3-any/O3-any median remains owner-vetoable before Q5.**
5. **Holm**: exactly six named constants **within one game**, never pooled. Undefined hypotheses are conservatively represented as p=1 for the six-member family and displayed as N/A (not silently dropped). Q4 final reporting must present raw and adjusted values with this policy explicitly labelled.
6. **NULL**: retain decoy provenance in Q4c; reporting compares only per-decoy **summary counts** to REAL count with inclusive `(1+tail)/(K+1)`, not an event-level REAL/NULL join.

## Qualification coverage and remaining work

Hand tests include 961 independent exhaustive comparisons of the fast closest-pair algorithm to the brute-force definition, all 24 ordered arrangements of a tiny four-draw permutation test, overlap counts and shifted relations, exact tie direction, empty W rows, zero-distance events, all-empty N/A, valid/undefined permutation counts, fixed six-member Holm including an unavailable constant, Oz O2 nested order, expectation arithmetic, and 13 explicit refusals.

The `--run` mode creates **four** genuine tiny Q4c scanner runs in a temporary marked sandbox: PB `TEST_REAL`/`TEST_NULL` and Oz `TEST_REAL`/`TEST_NULL`. Q4c verification and classifier run before statistical calculations. Two scratch reports (`category_summary.csv`, `transitions.csv`, `summary.json`) are written create-only under `q4d_synthetic_reports` and destroyed with the sandbox. REAL-like transitions are not calculated from NULL. No G:\\ source access or REAL historical reads.

**Still pending before final Q4 qualification**: production reporter/replay loader and immutable report-digest binding to COMPLETE manifests; six-constant per-game report integration (the 6-member Holm core is already tested); exact approved Oz modern drawset bounds; formal owner checkpoint on primary P3/O3 statistic and undefined permutation convention; production root controls and failure cleanup; independent full end-to-end synthetic qualification and owner review. None of these gaps permits a Q5 scan.

Keep the v0.2 science spec, Q1/Q2/Q3 evidence, all production datasets and receipts unchanged. After reporting Windows PASS, inspect `git status --short` and stage only `GAIS/OUTLANDISH_01/` source/doc files; do not stage the overarching project's unrelated uncommitted work.
