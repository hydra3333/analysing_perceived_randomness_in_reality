# OUTLANDISH_01 — Q4g verified six-constant synthetic aggregation v0.1

**16 November 2026 (Australia/Adelaide). SYNTHETIC TEST ONLY. Not Q4 production qualification and not Q5 authorisation.**

## Current owner evidence

The owner reported **Q4f Windows PASS** with exact expected counts:

- `Q4F SYNTHETIC BOUNDARIES PASS: guard-refusals=7 source-runs=0 reports=0 games=2 constants=6 production-scans=0 REAL-history-reads=0`
- `Q4F SYNTHETIC INTEGRATION PASS: guard-refusals=92 source-runs=24 reports=24 games=2 constants=6 production-scans=0 REAL-history-reads=0`

Earlier Q1/Q2 completed and Q3/Q4a–Q4e have their existing recorded PASS evidence. **Q4f closed its synthetic 24-run matrix, not the REAL production implementation review.** No original production constant, real history or result was read by those tests.

## Files added (no existing file replaced)

- `OUTLANDISH_01_Q4g_Verified_Synthetic_Aggregate_v0_1.py` — verified *single-game* six-constant report aggregation; one fixed six-constant Holm family per game; summary-count-only comparisons with the paired verified synthetic NULL reports. Reconstructs every input using Q4e's existing read-only verified reporter before accepting it.
- `OUTLANDISH_01_Q4g_Verified_Aggregate_Qualification_v0_1.py` — artificial fixture qualification, importing the already-installed Q4f matrix. `--run` performs 24 small synthetic source runs and reports, followed by two new game-specific create-only aggregate manifests and adversarial refusal tests. Replays both aggregates while all six artificial packed files are temporarily unavailable.
- This README.

**Scope:** only `GAIS/OUTLANDISH_01/`. Previous Q3/Q4 files, historical results, receipts, real data and parent repository changes are *not* edited. The ZIP is a distribution artifact; leave the ZIP outside the repo, extract the contained paths only. It is intentionally not a new production run entry point or registry.

## Windows CMD qualification

From the repository root (venv active is optional when using the explicit executable):

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4g_Verified_Aggregate_Qualification_v0_1.py" --self-test
```

Expected:

```text
Q4G SYNTHETIC GUARDS PASS: guard-refusals=10 source-runs=0 upstream-reports=0 verified-game-aggregates=0 games=2 constants=6 production-scans=0 REAL-history-reads=0
```

Then:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4g_Verified_Aggregate_Qualification_v0_1.py" --run
```

Expected:

```text
Q4G SYNTHETIC INTEGRATION PASS: guard-refusals=23 source-runs=24 upstream-reports=24 verified-game-aggregates=2 games=2 constants=6 production-scans=0 REAL-history-reads=0
```

**Local test scope:** both modes passed in a temporary Linux/Python 3.13 environment using explicitly labelled local Q3 scanner/classifier stand-ins. The real Windows Q3 v0.4 integration is **not** claimed until the owner actually runs the two commands. No source binaries, real histories, or production directories are selected by either mode.

## What is being qualified

1. **Exact six named constants, independently per game.** Each aggregate has one game-specific fixed historical-draw fixture digest and a common logical prefix length. The six packed TEST source digests must be distinct. REAL-like and NULL-like reports for the same constant must agree on the source SHA, while cross-game/type/constant substitutions are rejected by the verified Q4e manifest reader. A run-ID's spelling is not accepted as proof of origin.
2. **Correct cross-constant statistic.** Collect the Q4d centered two-sided primary p-value for P3-any (`K6S`) or O3-any (`K6`), retain undefined/N/A cases, then apply Holm across **exactly six constants within that game**. The owner's option to change/veto the proposed primary statistic is retained. Nothing is pooled between the games.
3. **NULL comparisons.** For each constant, compare verified TEST_REAL category counts only with the corresponding verified TEST_NULL *per-decoy summary counts*. NULL raw event rows are never joined into the aggregate. Store each NULL seed and synthetic history hash, explicitly recording whether all six used the same decoy histories; do not assume they did.
4. **Provenance and replay.** Store verified upstream report and manifest hashes, implementation module hashes, a create-only `INCOMPLETE` → `COMPLETE` aggregate manifest, and the aggregate SHA. Replay recomputes all 12 constituent reports (6 REAL-like + 6 NULL-like) through the qualified Q4e reader and reproduces the aggregate **without reopening the packed binary**.
5. **Adversarial tests.** Refuse duplicate or incomplete group identity, unknown or missing constants, cross-game/roster injection, altered source reports/manifests and altered aggregate digest/body. An injected crash before completion leaves the group INCOMPLETE. Existing upstream Q4e source reports must remain byte-for-byte unchanged.

**Performance limits:** synthetic fixture N=10,001 logical digits, K=2 decoy histories and 48 permutations per REAL-like report. These deliberately do *not* qualify 10-billion-digit production execution, K=19/99 null comparisons, or the 10,000-permutation final analysis.

## Remaining Q4/Q5 gates after a Windows Q4g PASS

- **Production runner implementation and focused review remain outstanding.** The only runnable entries provided in Q4b–Q4g are marked synthetic tests. No REAL/NULL production scan or published-result path is enabled. Approved published-root and receipt checks must be integrated with actual production runner(s) and a fail-closed status lifecycle; each 5 GB source hash will be checked during its *future authorised run*, not during this qualification.
- **Oz approved modern-era isolated profile is unresolved** in the material reviewed. Its genuine source path, layout and cutoff must be established from approved evidence. Do not invent them and do not open the parent Oz master/holdout for this test.
- **Owner's pre-Q5 decisions:** owner may veto or replace P3-any/O3-any as the proposed primary W→W+1 statistic; settle bounded NULL K, Monte Carlo seed and run-cost conventions before qualifying production. Report and aggregate provenance must meet the ratified v0.2 design. No forecast implementation or automatic E-method adoption.
- **Final review and separate owner authorisation** are mandatory before any REAL Q5 scan. Keep the living progress document updated with the *returned* Windows PASS/FAIL evidence, rather than asserting that a local test proves user-host qualification.

Before committing, inspect `git status` and stage only `GAIS/OUTLANDISH_01/` changes; do not stage or clean unrelated parent-project work. Do not overwrite locally edited living documents, preserve all prior evidence, and keep distribution ZIPs outside the repository.
