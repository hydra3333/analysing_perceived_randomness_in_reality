# OUTLANDISH_01 Q3 — post-match classification + direct overlap counting, v0.1

**Status:** new fixture-only implementation slice, not a REAL or NULL entry point, not a Q3/Q4 qualification sign-off. Prepared following the owner's 14 November Windows `Q3 SHARED ENGINE PASS` at commit `a74cfd9`.

## Purpose

The shared packed BCD matcher already emits raw events in the ratified four-column schema. This slice independently **replays** each raw event against its draw record (without reading any packed constant) and derives:

- PB P1/P2 drawn order vs reordered, PB P3 six-ball drawn subsequence vs reordered, omitted main and actual PB; historical PB baseline membership retained distinctly from any-order raw event membership.
- Oz O1 drawn order vs reordered, O3 six-ball drawn subsequence vs reordered, O2 one chosen supplementary with its literal slot `0..6`, original supplementary chronology index `0..2`, supplementary-last and full chronological drawn-subsequence (and their disjoint difference/subset flags). O2 never receives an ambiguous bare `reordered_only` classification.
- Direct, **same-draw** overlap counts of `[start,end)` physical logical-digit intervals; count all legitimate pairs, including nested and shifted occurrences, while excluding pairs that merely share position across *different* draws. The production-style count is a sweep algorithm; tiny-fixture tests compare it with an independent O(n²) enumerator. These are pairwise counts, **not** connected-component counts.

No change to raw four-column CSV or to ratified science v0.2. No classified CSV format is imposed now; `Classified` is a pure in-memory result for replay/verification. The planned Q4 qualified loader must verify event file + manifest + drawset digests and correct REAL/NULL provenance **before** calling this classifier. One giant run's classifications/reports must be bounded-memory or external-sorted; this first fixture slice does not claim whole-production scalability.

## Installation and execution on the Ryzen

Extract ZIP at repository root, preserving `GAIS/OUTLANDISH_01/`. Do not copy any files to the published `G:` digit or REAL-result roots. Existing scanner, historical scanner and independent oracle must stay unchanged.

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q3_Classification_Qualification_v0_1.py" --self-test
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q3_Classification_Qualification_v0_1.py" --run
```

Expected `Q3 CLASSIFIER PASS`, following exact independent-oracle event/flag comparison and refusals. The harness creates only small synthetic packed files/CSVs under OS `TEMP`, with automatic removal. It **does not** touch production 5 GB constants, REAL lottery histories, receipts, result directories or registry.

Two new Python files and this README can be committed. Do not commit the ZIP. If a test fails, report the first traceback rather than guessing or editing the ratified spec.

## Next gate

Following owner-run PASS, Q3 needs (i) a reviewed, bounded-memory production path for streamed events and reproducible classification without rescanning 5 GB inputs, (ii) actual-profile integration and Oz era/cutoff verification, (iii) Q4 REAL/NULL firewall and integrity manifests, and (iv) scientific reporter qualification. Q5 requires its separate owner approval.
