# OUTLANDISH_01 Q4l — two pre-Q5 housekeeping items (16 November 2026)

**Authorised scope:** documentation of D4/D5 plus a **prepared but not yet executable against REAL evidence** phi known-answer set comparator. This package does **not** authorise or start Q5, does not alter any scan/report/statistical code or the production switch, and does not touch the parent project's `source_data/` or `results/`.

**Source:** GitHub `main` at `4b1faac705a8152b476d7a320eff620d578f5463`, after Claude Review 006 `d036859` and the Q4k code `b5f2ada`. Progress patch anchors were checked against the published living-file text; on Windows use the explicit `git apply --check` before applying.

## Installation on the owner's Windows checkout

Unpack this ZIP at the repository root. It creates the Q4l comparator, this README and the temporary patch, all under `GAIS/OUTLANDISH_01/`. It does not overwrite any existing production code.

Run in CMD at the repository root:

```bat
git pull --ff-only
git apply --check "GAIS/OUTLANDISH_01/OUTLANDISH_01_Q4l_Progress_Amendment.patch"
git apply "GAIS/OUTLANDISH_01/OUTLANDISH_01_Q4l_Progress_Amendment.patch"
del "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4l_Progress_Amendment.patch"
".venv\Scripts\python.exe" -B "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4l_Phi_Known_Answer_Compare_v0_1.py" --self-test
".venv\Scripts\python.exe" -B "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4i_Production_Entry_v0_1.py" status
```

Expected from self-test: `Q4L SYNTHETIC PHI SET-COMPARISON PASS: exact/missing/extra/guard; production-reads=0`; Q5 switch must print `DISABLED`.

**Stage only these three files** (never the parent project or results folders):

```bat
git add -- "GAIS/OUTLANDISH_01/OUTLANDISH_01_Living_Decisions_and_Progress.md" "GAIS/OUTLANDISH_01/OUTLANDISH_01_Q4l_Phi_Known_Answer_Compare_v0_1.py" "GAIS/OUTLANDISH_01/OUTLANDISH_01_Q4l_PreQ5_Housekeeping_README_v0_1.md"
git diff --cached --name-status
```

Expected: one modified living file and two new files. After confirming, owner may commit/push this documentation-and-preparation checkpoint. Do NOT change the Q5 switch as part of that commit.

## What the comparator does later (ONLY after separate Q5 approval and a COMPLETE REAL phi scan)

The comparator has **no scanner** and accepts no alternate production root or CSV path. Its `--run-id` branch requires a `COMPLETE` `REAL` Powerball `phi` run manifest with fixed 10^10-digit and known source/history identities. It checks the manifest's raw event SHA-256 and saved legacy CSV's pinned SHA-256 before calling Q1 `parse_evidence` on the saved legacy matches and the new four-column event CSV. Comparison is **only** a set equality check of `(draw, start offset, matched digits)` for P3/K6S. Its complete result is matched/missing/extra counts and the rows that differ; **no** gaps, offsets subtracted, adjacent-pair calculations, medians, geometric means, p-values or statistical tests. All reads are confined to the fixed G: OUTLANDISH root. No packed binary, converter receipt, lottery history or report file is opened.

When the owner later authorises Q5, phi is the **first** genuine REAL scan. Only after its scan manifest is COMPLETE, run:

```bat
".venv\Scripts\python.exe" -B "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4l_Phi_Known_Answer_Compare_v0_1.py" --run-id REAL_<actual-phi-run-id>
```

Replace the placeholder with the exact new **complete** REAL run ID (do not type the angle-bracket placeholder literally). Expected pass: `matched=227`, `missing=0`, `extra=0`; if any difference, **STOP** the sequence and investigate without assuming either scanner is correct. This later command is **not authorised now**.

## Scientific status and limitations

D4 primary and median secondary, independent Holm families, and D5 fixed disclosure have been implemented and verified in Q4k (`b5f2ada`). Claude's focused Review 006 (`d036859`) found no blocker, and the owner ran Claude's end-to-end v0.2 script on Windows with results identical to Linux. The package makes no new statistical choices and does not open, reinterpret or reanalyse the five legacy signed gaps or the saved 227-row phi data before an authorised comparison.
