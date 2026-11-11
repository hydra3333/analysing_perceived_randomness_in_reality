# Amendments to design v0.1r6 Appendix J and section 4.3 (MHUP-A install) - RATIFIED 11 November 2026

**RATIFIED by the project owner, 11 November 2026** (`exchange/HO2_2026_11_10/MHUPA_Owner_Ratification_Rulebook_v05_AppJ_2026_11_11.md`),
after the reviewer's R-2 focused PASS of the r2 draft (commit 19e45ff). J-1 and J-2 change the normal path (step 10).
J-3 and J-4 do not: they apply only after a STOP at step 13 or step 17 and can be ratified separately. Nothing here supersedes the ratified text until the owner ratifies it. The design file itself is not
edited now; on ratification the amendments are recorded in the register and carried into the design at its next
edition. Each item gives the ratified text, the proposed text and the reason.

## A. Amendments that change what Appendix J requires

**J-1. Step 10, Action** (N5 option A; owner's yes in principle, 11 November 2026).
- Ratified: "The suite (the barrier paths are module constants the harness patches, so the suite passes with P
  present)".
- Proposed: "The suite, run by the package's suite runner in `--shadow` mode: after a fresh POST PASS on the live tree,
  it copies the installed files byte for byte into a new temporary folder without the barrier files, together with only
  the six development data files the accepted tests read (for each game: the results master, its ledger and its INIT
  verification record), and runs the suite there; the live tree keeps U, E and P throughout and is checked again
  afterwards (POST, and no file gained, ignored files included); the temporary folder is then removed, and a folder that
  cannot be removed is a STOP."
- Why: with the barriers in place the installed tree refuses every run, which is their purpose; several accepted tests
  use the real gate and root, so the ratified premise ("the harness patches it") does not hold for them (N5).

**J-2. The negative-test sentence for step 10.**
- Ratified: "the suite fails if P is absent at step 10 in the rehearsal (proving the harness patches it, not the absence
  of the barrier)".
- Proposed: "the step 10 runner STOPs before copying if the live P (or E, or U) is missing or foreign; STOPs if the copy
  differs from the live tree or the import path reaches into the live tree (the live tree's own `.venv` excepted);
  STOPs if the live tree gains any file during the suite, ignored or not; and STOPs if its temporary folder cannot be
  removed; P's own refusals are tested in `test_mhupa_gates` and `test_e2r_dispatch`."

**Exceptional recovery only (J-3 and J-4).** Neither is part of the normal path, and neither is ever a runner action or
automatic: each case is proposed by Claude for that exact state, reviewed, and approved by the owner before any change.
A fresh install check showing `CLEAN` comes before any code or Git change; nothing is reset, rewritten or deleted; U
stays held until the very end.

**J-3. Step 13, STOP handling** (reviewer's point B and REC-C01).
- Ratified: "stop; do not push; E, P and U stay (fail closed: the code is committed but not released); Claude writes the
  fix (a further small package commit, or a reviewed revert commit), COMMITTED is rerun, then steps 14-19".
- Proposed: "stop; do not push; E, P and U stay (fail closed). No fix forward in place: the recovery is proposed by
  Claude for that exact state, checked by the reviewer and approved by the owner. The normal route is abandon and
  rebuild: a fresh install check showing `CLEAN` before any change; reviewed `git revert` commits, newest first
  (nothing is reset, rewritten or deleted; every commit and record stays in the history); E and P removed after another
  `CLEAN`; U released last; a new package, with its own name and records, built and reviewed on the resulting commit."
- Why: the verifier proves only the two-commit shape, on purpose (no verifier for arbitrary histories; KISS).

**J-4. Step 17, STOP handling after the release commit exists.**
- Ratified: "stop; re-create P; after the fix, delete P and rerun from step 17".
- Proposed: "stop; U stays held; re-create P. If the release commit was not made, Claude's fix is applied, P removed and
  step 17 rerun (unchanged). If the release commit was made, do not continue: the recovery is as step 13's (abandon
  and rebuild, approved for that exact state; the release record already committed stays in the history)."

## B. Stricter than the ratified table (recorded for information; no requirement is relaxed)

| Step | Ratified | The package's instructions and tools |
|---|---|---|
| 12 and 17 | stage; `git status --short` shows exactly them; commit | stage from the package's path list; the verifier's `staged` phase must PASS; then commit |
| 15 | delete E, then P | the copy tool removes E only if the verifier's COMMITTED phase passes at that moment, then P |
| 16 | the record tool's refusals as listed | also refuses unless U is held by this package and no released method's E flag exists (reviewer's point A) |
| 18 | release U | U is released only if the `released` phase passes at that moment |
| 0 | `git status`; `git pull` | step 0a (names for the window; repeatable after a closed window), then status, then pull |

## C. Two wording points in design section 4.3 (no change of behaviour)

**C-1.** "The baseline record ... 40 entries" -> "40 entries per game (80 in all)". The record holds the 39 released
variants and E_1 revision 2 for each game.

**C-2.** The install record's time: "the UTC time and local date of the POST PASS" -> "the UTC time and local date at
which it is written (step 12, after POST PASS and the suite)". The field keeps its name `post_pass_utc` and the record its schema for this package (no migration); the verifier
checks that it is not earlier than the
taking of U and not later than the release record.

## D. Related, not an Appendix J amendment

- **Appendix K, row "Rulebook rule 7; `.claude/settings.json` deny patterns".** Rule 7 already names `process_check.py`
  and `install_records.py` (rulebook v0.4). Rulebook v0.5 section 2A is the owner's T016-only exception (R-020(g)
  option (i)); it does not change Appendix K. The matching deny lines (F1) are added by the owner after T016 and before
  the live install's step 0 (see the cover note).
- **Rehearsal evidence.** T016 rehearses steps 0 to 18 on Windows in a full task clone (step 0 as a clean-tree and HEAD
  check, step 19 omitted), step 10 included. No further live end-to-end owner rehearsal is proposed; F2 rows 8 and 9 are
  the owner's own real-root checks.
