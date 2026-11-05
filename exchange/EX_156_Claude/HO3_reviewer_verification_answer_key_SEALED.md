# HO-3 reviewer verification - Claude's answer key (SEALED until the reviewer has answered)

Claude, 6 November 2026. This key belongs to EX_154. EX_154 records this file's SHA-256 (CRLF bytes as committed), so the key is
shown to have been written before the reviewer answered. Claude commits the key to `exchange/` only after the owner has relayed
the reviewer's answers. If this chat ends first, a new Claude chat rebuilds the key from the cited records, and EX_154 says so.

Each answer gives the expected substance and its source. A reviewer answer that differs is checked against the source, not
against this key. The key can be wrong.

## Part A - status

Q1.
- **Installed:** the last reviewed code package installed is PERF-1 (`3fce327`, 1 November 2026); 471 tests on main; all 40
  variants `SUPPORTED` and released in both games.
- **Reviewed but not installed:** MHUP-A slice 1 (EX_146 PASS) and slice 2 (EX_152 PASS, candidate v1r2,
  `exchange/EX_151_Claude/MHUPA_Slice2_Review_v1r2.zip` `67701220...`).
- **Ratified:** design v0.1r5 (MHUP-R, 3 November 2026), A1 (5 November 2026), direction v0.3r1 (4 November 2026), register
  v0.24 (4 November 2026).
- **Not even designed in code:** MHUP-B.
- **Owner material, unreviewed:** `src/GAIS/`, `doc/GASI_thought_experiments/outlandish_01/`, and the `pyahocorasick` line.

Sources: register v0.24 and v0.25 candidate 2; EX_146; EX_152.

Q2.
- **What EX_152 permits:** preparing the one integrated MHUP-A install candidate (slice 1 plus slice 2, A1 cited) for its own
  independent review.
- **What it does not permit:** an integrated PASS, an install, disabling development or interlock flags, reading production
  outcomes or the holdout, Mode H opening or scoring, or any real-data run.
- **Which review depth applies:** the integrated review must assess the assembled behaviour, not infer it from the slice PASSes.

Source: EX_152 sections 0 and 5.

Q3.
- **Status:** T021 (v1r1, 569 tests) and T022 (v1r2, 570 tests) are pending; their reports are not in the repository.
- **Order:** they come before integration.
- **On a failure:** a STOP is a STOP. The runner stops and reports; Claude diagnoses the cause (Fable if it is unexplained); a
  corrected candidate goes to the reviewer before integration if the code changes. Nobody retries without the owner's go.

Sources: EX_152 section 4 ("address any platform-specific failures before integration or installation"); rulebook rule 10;
R-018 (a).

## Part B - decisions

Q4.
- **The order:** read the plan's targets' outcomes once (freeze-before-outcome rule, 5.3); compute every score and MR5
  rank-position record; publish the whole `mode_h_score_ledger.jsonl` once, create-only (temporary file, fsync, link); validate
  the published ledger as it stands; then `SCORE_COMPLETE` with the ledger digest; the report (three files, resumed one by one);
  `MODE_H_SEALED`.
- **The states:** (i) no ledger: the rerun re-verifies the roster and reads the outcomes again, which is permitted because
  nothing has been accepted; a leftover temporary file is never read. (ii) The complete ledger without `SCORE_COMPLETE`: no
  outcome is read; the ledger is validated and completed, or refused, and a refusal is a STOP for the owner and the reviewer.
  (iii) After `SCORE_COMPLETE`: no outcome is read; the report is resumed; the seal.
- **Validation failure after publication:** a STOP. Nothing is completed, and the ledger is not overwritten or deleted.

Source: A1 sections 2 to 4.

Q5.
- **The decision:** the integrated package's actual preparation date, set before its final review freezes the registry bytes
  and digests; never the admission or release date. The release record alone dates a release.
- **The consequence:** it changes E_1 revision 3's registry and declaration bytes and digests, so everything depending on
  them is rebuilt and the tests and mutants are rerun after it is set. A review that froze digests with another date would be
  invalidated.

Sources: EX_142 C01, EX_143, EX_146 item 4, R-019 (d).

Q6.
- **IIIB-1:** deferred to MHUP-B.
- **The route (A1 section 6):** its own attempt folder and scoring plan; a new scoring policy id and `amendment_of`; the release
  rule extended for it; published beside the first, never touching the first ledger, `SCORE_COMPLETE` or the seal; shown in
  reports as an amendment.
- **Approvals:** separate design review and owner approval.
- **MHUP-A today:** `score` refuses after the seal.

Source: A1 section 6; EX_149 section 1.

Q7.
- **The rule:** a STOP is always a STOP. Claude reports, diagnoses the cause and proposes the recovery, and the owner explicitly
  authorises each retry.
- **When a retry fits the existing Approval 2:** only if the refusal came before admission (master and ledger unchanged) and the
  cause is positively identified as within the original operation (for example an insufficient window fixed with
  `--months-back`).
- **Otherwise:** if the cause is uncertain, there is partial transaction state, or the retry would exceed the approval, STOP
  for separately reviewed recovery steps and the owner's approval.

Source: R-018 (a); EX_140.

Q8.
- **When it applies:** after GOAL-1 and the required installs and approvals.
- **What it means:** the owner's deliberate run of the reviewed `Run_Weekly_Session.bat` is that week's authorisation.
- **What it excludes:** unattended scheduling, unusual recovery, bypassing a STOP, and operations outside the approved scope.
  The results updater stays a separate operation.

Source: Q9-E4 (EX_140; register v0.25 candidate).

Q9.
- **Q7 is OPEN:** whether, after a game's holdout is opened and its Mode H scored, the restriction on displaying or computing
  with Powerball draws from 1577 and Oz Lotto from 1694 is relaxed.
- **The recommendation:** keep the restriction on raw draw values in the AI chats.
- **When it is decided:** before Approval 2 (the first results update).
- **Meanwhile:** every rule stays as it is.

Source: register v0.24 Q7 and future action 4.

Q10.
- **The Mode H targets:** Powerball 1577-1586 and Oz Lotto 1694-1703, ten per game.
- **Option A:** the study plan, code and environment are frozen before the holdout is opened; the holdout is added once; one
  Mode H batch forecasts all ten, each from the draws before it; every planned run is DONE before any scoring reads an outcome;
  then the ten are scored once.
- **HX-1:** Powerball 1585 and 1586 are flagged for the recorded exposure, still scored and counted.
- **HX-2 interpretation (EX_134 C03):** 1587 and 1588 are evaluated in the weekly chronological pass with their flags. For the
  31 October cohort that is development evidence, not the `CATCH_UP` tier.

Sources: register v0.24 MHUP-Q1, HX-1 and HX-2; design 4.

Q11.
- **Its timing:** MHUP-B is installed before Approval 1, or only after the game's Mode H seal, never while a holdout is opened
  and unsealed (design 4.4). The owner chooses, and the integrated install plan should state it.
- **The four approvals per game (design 4.4 items 2 to 5):**
  - Approval 1: freeze the study manifest and write the opening record. The owner is first shown the exposure consequence of
    4.2.
  - Approval 2: the first results update, which brings in the holdout and every later draw in one version, `v_a`, or writes
    nothing.
  - Approval 3: the Mode H batch.
  - Approval 4: the Mode H score and report; `SCORE_COMPLETE` and `MODE_H_SEALED` close the study.
- **Between Approval 2 and the seal:** the updater refuses for that game.
- **Then:** GOAL-1 and the weekly session.

Source: design v0.1r5 section 4.4.

## Part C - the integrated package

Q12. Its contents:
- installer and verifier (Appendix J steps 0-19, the verifier's `released` phase);
- LF and CRLF rehearsals; T016 on Windows;
- E_1 r3 `effective_date` = preparation date (C01);
- the manifest's `release_entries` naming E_1 r3 for both games (R-020 (a));
- the orphan-file rule of the environment freeze (R-020 (b));
- the owner's POC rerun choice (R-020 (c));
- the rebase onto current main, the `.gitignore` lines, `pyahocorasick` and `src/GAIS` (R-020 (d)-(f));
- R-019 (a), (d) and (e) in the assembled behaviour;
- EX_148 (ix): COMMITTED PASS proves both commits, the barrier order, and that the records agree with the repository;
- A1 cited;
- the rulebook and deny-list additions (the settings file is the owner's edit);
- the MHUP-B route statement.

Sources: EX_152 section 5; R-019; R-020; register v0.24 future actions 1 and 2.

Q13.
- **The count:** 40 per game = the 39 unretired baseline variants plus E_1 revision 3 (revision 2 superseded).
- **The record:** the install's release record (Appendix J step 16), written after COMMITTED PASS, releases E_1 r3. Until it
  exists, E_1 r3 has an install record only and is not released for CATCH-UP.
- **The check:** `_check_release_authority` refuses a Mode H manifest unless the registry's runnable cohort equals the
  validated released set, in both directions.

Sources: R-020 (a); EX_149 B03 row.

Q14.
- **What the freeze covers:** the interpreter's files and the SHA-256 that pip's `RECORD` holds for every installed file.
- **Orphans:** a file in site-packages that no `RECORD` lists refuses the `manifest` command, naming it; the fix is a reviewed
  step, never a hand deletion.
- **`pyahocorasick`:** if installed, it becomes part of the frozen environment, and the owner must state whether the dependency
  change is approved (OPEN).
- **`src/GAIS/`:** inside `src/`, so inside the code closure (including about 153 MB of third-party y-cruncher executables
  committed at `54d161f`). The owner decides whether to move or untrack it, or exclude it by a reviewed rule, before Approval 1.

Sources: R-020 (b), (e) and (f); MHUP-B04 (b); this chat's check of `54d161f`.

Q15. Open-ended. Expected: R-2 reproduction of the authorised offline nondestructive suite in its own environment if feasible
(Python 3.13 or 3.15, the candidate ZIP attached directly, invented masters only, E2R-T12 noted), plus static review and
specification-first oracles where justified (R-4). It states what was reproduced and what was only inspected, and may ask for
owner-run evidence.

## Part D - boundaries and process

Q16.
- **What Claude commits:** only in `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`, named paths, never `git add -A`.
- **What Claude Code does:** runs task files in clones that cannot push (`cc_clone.py` v0.4) and commits only its report.
- **What it never runs:** the rulebook rule 7 programs.
- **The deny list:** the owner's `.claude/settings.json` denies command lines by their text, so denied paths go in plan files;
  T019 stopped correctly on that.

Sources: H-1 v1r8; rulebook v0.4; T019.

Q17.
- **Canonical identity:** the Git-stored content (LF for these markdown files, but CRLF for files stored with CRLF, such as A1
  and the EX messages).
- **Why CRLF copies appear:** a Windows checkout or `git archive` with `core.autocrlf=true` produces CRLF copies.
- **How to verify:** with `git show HEAD:<path> | sha256sum`, or after converting CRLF to LF where the Git blob is LF.
- **The A1 label:** A1's recorded digest is of stored CRLF bytes (TAKEOVER-C04).

Sources: register "Interpretation and verification"; EX_153 O01.

Q18.
- **The copies:** the files at `doc/HANDOVER/HANDOVER_2026_11_06/` and `doc/RATIFICATION_REGISTER_v0_25_CANDIDATE.md`
  (owner commit `929eff5`) are candidate 1 copies, not ratified.
- **What stays operative:** H-2 v1r8 and register v0.24.
- **What is still needed:** candidate 2 to replace them, and ratification by the owner after review. Placing a file in `doc/` is
  not ratification.

Sources: register v0.24 "Authority"; H-2 reading rule.

Q19. A reasonable answer names the three most valuable checks and why, for example:
- A1's state machine (a crash at each boundary; a refused ledger; the twin byte identity);
- the release-gating rule (the registry chain and release records in both directions; E_1 r3 not runnable for CATCH-UP before
  its release record);
- the installer and verifier's two-commit order with COMMITTED PASS and the barrier, under CRLF checkouts.

Any well-argued set is acceptable.
