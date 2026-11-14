# OUTLANDISH_01 — operational handover v0.9 (Q1 PASS / legacy retirement prepared)

**Date:** 14 November 2026, Australia/Adelaide. **Scope:** operational handback, not an amendment to the ratified scientific design. **Recommended location:** `GAIS/OUTLANDISH_01/`. **Status:** prepared for owner review and installation; no deletion, registry migration, Git commit, REAL scan or parent-method admission has yet been executed by this document.

**Relationship to v0.8:** This short v0.9 supersedes v0.8 only for the *now-completed Q1 comparison and legacy audit*. Keep v0.8 (all detailed generation/receipt/hardware provenance), the living decisions/progress record, consolidated handover v7/rev0.7, original historical CSVs and scanners, ratified matching/reporting v0.2, and unratified postmatch forecasting v0.1. Do not delete or overwrite those earlier documents.

## 1. Six immutable production inputs are ready

On **Ryzen 3900X**, the six published sources reside under `G:\OUTLANDISH_01\large_artifacts\digits\`. Each is **5,000,000,000 bytes**, **10,000,000,000 logical decimal digits including the integer digit**, format `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`, high-first nibbles and no header, with same-basename `.wsl-receipt.json`. All six SHA-256 values were established through owner-reported verified production and checks on the Ryzen; a second independent mathematical computation of the full 10^10 digits was consciously waived.

| Constant | Packed filename | Recorded destination SHA-256 |
|---|---|---|
| pi | `digits_pi_10_to_10.packed.bin` | `62ab5b9a511eb0fcf5d09717df9ee51f8bd29ea09acf379e6f1045c537ababe2` |
| phi | `digits_golden_ratio_10_to_10.packed.bin` | `dd80be0c3fdb330fe4e1780c2d53bf03bde297a5dea83b5785cd3349838ad36d` |
| e | `digits_e_10_to_10.packed.bin` | `522f088b013432f775098df863b851ad87a4f5d0f0296b54cb00d6f13f72720f` |
| log2 | `digits_log2_10_to_10.packed.bin` | `6993b8b6c6f46ae13b5e213aae0d46e784c8acae510f10e6862aecde83a15694` |
| gamma | `digits_gamma_10_to_10.packed.bin` | `68e4a47d27759632dd8c608af973fa5bd22fb2aa7290d5e92f59e485ceb85e6a` |
| lemniscate *half-perimeter* | `digits_lemniscate_10_to_10.packed.bin` | `958210dcda823fd1951b8487fbfe3cb98aeda9748c2b0dea4db9684608d21369` |

**Production provenance:** Four earlier results (pi/phi/e/log2) from the Ryzen WSL/Windows workflows, gamma and lemniscate from **native Windows 10/i5-4670 with 16 GiB RAM**, `y-cruncher -verify:1`, manual transfer to Ryzen and independent destination digest checks. Lemniscate generation **14 Nov 11:01–15:12** used `-M:12g`, T: HDD scratch, G: HDD decimal output. Source is y-cruncher FULL perimeter `5.244115...`, divided by two with the validated streaming converter to target HALF perimeter `2.6220575542921198104648395898911...`. The Ryzen's prefix and SHA matched the receipt. Six completed sources do not mean new scientific matching is qualified. Preserve receipts, reports, and original generation logs; the i5 full-decimal input remains subject to separately reviewed eventual cleanup.

## 2. Q1 saved-event reconciliation: PASS on 14 November 2026

The user ran `OUTLANDISH_01_Q1_Reconcile_Saved_Phi_Events.py` against two **saved historical CSVs**, with no repeat 5GB scan:

- Old 1e9 numeric-byte φ saved CSV: `GAIS/OUTLANDISH_01/OUTLANDISH_01_results/run_20261105_231343/digits_golden_ratio_10_to_9_matches.csv`, **25** baseline P3 rows, SHA-256 `c067b95d7171ca4669724985842e153e747c18adf255cafbe76d5512d564b580`.
- 1e10 packed φ historical output: `G:\OUTLANDISH_01\large_artifacts\results\packed_run_20261108T012705Z_43564c3c\matches.csv`, **227** baseline P3 rows, SHA-256 `7a4315d66b028a2664413f0b3017714c10653110a1d79af7102d8ea09bbb5c83`.
- **Q1 STATUS: PASS.** At derived end `<=10^8`, P1/P2/P3 old vs packed `0/0`, `0/0`, `3/3`; at `<=10^9`, `0/0`, `0/0`, `25/25`. Zero old-only or packed-only tuples; no duplicate identities or end discrepancies. Three previously known 100m φ P3 starts confirmed: draw 1244 at `20,048,101`, 1274 at `71,806,090`, 1373 at `95,105,831`.
- The pre-existing code parsers were inspected and consume `Drawn_1` through `Drawn_7` in operator order without silently sorting before drawn-order matching. The isolated Powerball drawset is exactly modern historical draws **1144..1576**, exclusive holdout cutoff **1577**.

**Scientific qualification boundary:** This resolves the previously suspicious prefix **saved-event discrepancy**. It does **not** independently validate the existing scanner or 227 as a reliable scientific statistic. Follow Q2–Q4 before qualified REAL scans.

## 3. Legacy 1e9 state and two-stage cleanup

Owner-run independent audit `OUTLANDISH_01_Legacy_1e9_Readonly_Audit.py --full-hash` returned `HASHED_PASS` for **all six** old `digits_*_10_to_9.bin`, each exactly **1,000,000,000 bytes**, matching the six `[state.active]` entries. Exact audited TOML SHA-256 `1718ab895a0479d437ac1f376585a3aea6cb864b722d96d2487ad21ac4236fe5`. Those old state records and binaries remain present **until the owner executes cleanup**.

The new `OUTLANDISH_01_Legacy_1e9_Retirement_v0_1.py` has three intentionally distinct modes, documented in the ZIP's README:

1. **Read-only PREVIEW**: requires exact saved-Q1 PASS, verified six new packed receipts and expected old-file names/sizes. Prints explicit plan; no changes.
2. `--deactivate --confirm-idle`: require all processes using old data are idle; archive exact old TOML plus evidence under `G:\OUTLANDISH_01\large_artifacts\logs\legacy_1e9_retirement_...`, then rehash all six old binaries and atomically clear the **old numeric-byte** `[state.active]` and empty `[state.pending_retirement]` via existing config API. Files retained in this stage.
3. `--delete --manifest "<actual printed evidence.json path>" --confirm-idle`: separately rehash surviving old files, verify archive, empty registry and new packed receipts/sizes; unlink **only** six exact old filenames; tolerate safe partial retry. No wildcards and no changes to the six new packed datasets.

**Do not call the old `outlandish_artifacts.py retire` method** with a packed replacement: old and packed formats are incompatible and old retire requires a compatible active successor. After migration the old TOML active state is intentionally **empty**, not a false packed registration. Existing legacy `scan_1e9.cmd` / `scan_1e10.cmd` must not be used after reset. This cleanup helper passed a small-file simulated end-to-end test, but has **not yet been executed on the owner's Windows files**. Failure/mismatch means STOP, no manual wildcard cleanup.

## 4. Science begins: Q2 in progress, Q3–Q5 still gated

`OUTLANDISH_01_Q2_Independent_Oracle_v0_1.py --self-test` is a minimal stdlib-only independent decimal-string oracle and synthetic fixture set, implementing fixed-width PB P1/P2/P3 and Oz O1/O2/O3 classifications. Initial self-test **PASS** in the assistant's environment (zero/odd offsets, EOF, PB equals main, main-7 >20, main/supplementary roles, special slots, shifted same-draw inclusions, known-hit tuple subsets, high-first BCD/odd padding). It does **not** read any REAL outcome or packed source and does **not** run the existing scanner; hence Q2 remains **IN PROGRESS**.

**Next scientific action:** compare unchanged old packed Powerball scanner with independent oracle on deliberately planted synthetic `.packed.bin` fixtures under an isolated test-only output directory; verify exact event sets, boundary ownership, duplicate refusal, shortened 12/14/16-digit family EOF masks, invalid nibble, and mutation canaries. Adapt Oz after confirming its already-validated isolated modern-era drawset and independent holdout, not by guessing a cutoff. Preserve historical source scanner and old reports. Q3 is a new minimal shared reader/index/classifier only **after** Q2 provides correctness evidence; Q4 adds REAL/NULL and reporting guards. Q5 requires Q1–Q4 PASS, owner approval of final implementation spec and new create-only production scans. Never access parent holdout or combine games, and do not enable the unratified adaptive forecasting proposal merely because generation completed.

**Current source authority:** `GAIS/OUTLANDISH_01/OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md`. The 10-Nov forecasting spec stays **FOR OWNER REVIEW / PARKED**. Maintain `OUTLANDISH_01_Living_Decisions_and_Progress.md` as the single up-to-date operational status/decision record. Preserve the v0.8 historical handover, both saved φ CSVs, and i5 generation evidence. Neither this document nor the provided scripts performs Git writes, deletes old files by itself, starts a real scan, or changes scientific research rules.
