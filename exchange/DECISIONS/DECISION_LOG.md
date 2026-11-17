# Decision log (living; append only)

Started 14 November 2026 (EX_182 P2, as modified by EX_183). One entry per owner decision: date and time
(Australia/Adelaide), the owner's exact words, where they were given, status, and links. A correction is a new entry,
never an edit of an old one. The earlier files in this folder keep their authority; so do the ratification register and
the installed documents. This log is not a separate approval process.

## 1. 14 November 2026, about 20:17 - working approach P0-P6 adopted on consensus

- **Where:** the owner's message in the Claude chat, quoting what he had told the ChatGPT reviewer after EX_183.
- **Owner's words (to the reviewer):** "This is looking good to me. once you and claude arrive and consensus then we'll
  adopt. Suggest that after each  at every substantial project milestone that we perform a claude/chatgpt review of how
  this new process went and whether I did/did-not suggest changes (I like to display your thinking in case I discover
  something important which I actually do from time to time)."
- **Owner's words (to Claude):** "yes to:" the reviewer's framing of that suggestion (P6): keep it lightweight, part of the
  normal milestone handback; Claude and the reviewer each give their own assessment before a joint recommendation;
  changes to binding rules remain the owner's to approve; record the outcome briefly in CONTINUITY_NOW.md; explain the
  reasoning, alternatives and uncertainties.
- **Consensus:** EX_183 (reviewer) modified P0-P5; EX_184 (Claude) accepts every modification unchanged and agrees P6.
- **Status:** ADOPTED as working guidance. Where it differs from the installed handovers, they govern until their next
  editions. Reviewer rights and RECHECK areas unchanged; Mode H, D1-D7 and the freeze unchanged.
- **Links:** exchange/EX_182_Claude.md; exchange/EX_182_owner_QUERY_01.txt; exchange/EX_183_ChatGPT.md;
  exchange/EX_184_Claude.md; exchange/CONTINUITY_NOW.md.

## 2. Earlier today (pointers only; recorded in their own files)

- Replacement reviewer accepted; EX_177 C02 closed; D1-D7 decided as recommended; OUTLANDISH_01 notice:
  exchange/DECISIONS/OWNER_DECISIONS_2026_11_14b_C02_AND_REVIEWER.md.
- Documentation round ratified (RAT-31): exchange/DECISIONS/OWNER_DECISIONS_2026_11_14_DOC_ROUND_RAT31.md.
- No further package installs planned; the owner will ask Claude first (Claude chat, 19:48).

## 3. 14 November 2026, about 20:32 - OUTLANDISH_01 methods go first in the "still to do" list; go for task 1 if the reviewer agrees

- **Where:** the owner's message in the Claude chat.
- **Owner's words:** "outlandish will go into the "Still to do" even though these will have been developed and run they
  will not be in a form usable by this project and will need to be reviewed and changed accordingly, probably as the first
  ones in the "Still to do" list.  OK. lets start the process form #1 if chatgpt agrees now (al;so tell chatgpt about the
  updated "Still to do" list then we go)"
- **Status:** (a) DECIDED: OUTLANDISH_01's method family joins this project's method backlog, probably first among the
  methods still to do (after Mode H, MHUP-B and WF-1C, as the existing order puts all new methods). It enters only through
  this project's normal route: identity decision (new numbers E_63 onward need an owner decision and a catalogue
  amendment), design review, N-1 isolation, rework into this project's method contract, release, and the Q7 raw-value
  restriction. Its OUTLANDISH runs are not evidence for this project. (b) GO, CONDITIONAL on the reviewer's agreement:
  task 1, the POC rerun (R-015 (b)), exactly as `exchange/CLAUDE_WEB_TOOLS/modeh_readiness/OWNER_POC_RERUN_R015b_DRAFT.md`
  r3 (Git blob 1105ff1c6c37f8be9bbb99e8b833dfd8dfa0a097; passed in EX_168; unchanged since), without `--with-timeout`.

## 4. 14 November 2026, 22:32 - condition met: the POC rerun may run

- **Where:** the reviewer's agreement (EX_185, relayed by the owner).
- **Status:** entry 3 (b)'s condition is met. GO for the POC rerun r3 (blob 1105ff1c...), default route, no
  `--with-timeout`. This POC only; nothing else is authorised. The reviewer also acknowledged entry 3 (a).

## 5. 14 November 2026, about 22:45 - B01: scoped W-23 acceptance of the dependency change

- **Where:** the question tool in the Claude chat, after EX_186 (Claude) and EX_187 (reviewer).
- **Question (Claude):** "B01: do you accept T024 plus tonight's POC rerun as enough evidence for your 14 November
  dependency change (cc0ab73) only? This is recorded as a 'scoped W-23 acceptance', never 'W-23 PASS'. Not tested on the
  new packages: the timeout/cleanup case, Ctrl+C, memory stress and the other lifecycle tests. You'd be accepting that
  their risk can't be measured (the reviewer's correction to my 'low'). Both AIs recommend accepting."
- **Owner's answer:** "Yes, accept (Recommended)".
- **As decided:** Scoped W-23 acceptance for the dependency change of 14 November 2026 (cc0ab73) only: TASK_T024 (ENV
  PASS, 90 distributions, environment digest 5bf4eb8a36dd...; 571 tests PASS, 4 permitted skips) and the R-015 (b) POC
  rerun of 14 November 2026 (PASS; EX_186, EX_187) are accepted as sufficient. Not run: the timeout and process-tree
  cleanup case (`--with-timeout`), Ctrl+C, memory stress and the other W-suite lifecycle cases. Residual risk accepted:
  those paths are unverified on the new environment, and that risk cannot be reliably quantified. This is not
  "W-23 PASS" and authorises no further test or operation.
- **Status:** EX_177 B01 CLOSED. EX_177 has no open item left.

## 6. 15 November 2026, about 09:10 - RAT-32: H-1 v3, its blurb and register v0.30 ratified

- **Where:** the question tool in the Claude chat, after EX_190 (Claude), EX_191 (the reviewer: PASS WITH CORRECTIONS; H-2
  needs no new edition) and EX_192 (the corrections applied), and the owner's relay of EX_192 to the reviewer.
- **Question (Claude):** "Do you ratify the three reviewed files for installation: H-1 v3, its blurb, and register v0.30
  (RAT-32)? H-1 v2 would stay in doc/HANDOVER/ as history, like last time. This authorises only the documentation install
  tonight, nothing for Mode H."
- **Owner's answer:** "Yes, ratify all three (Recommended)".
- **Status:** RATIFIED. Only the status wording changed after the review (`exchange/CLAUDE_WEB_TOOLS/doc_round_rat32/finalise_rat32.py`
  and its two diffs). Final SHA-256: H-1 v3 `ddefe7006aa17cfd0a9a8996bd7122aed537d8d66accee92b2e5d737aefbaa54`, its blurb
  `d1df63bf18bc7becc96212ac0d76d519a2a5c4d6b367251116b294382573dd4d`, register v0.30
  `2a6fe7b6758d882b46a6829cff6c73ddefa5381f9fe3851b72720ab40ccdd56c`. The install is owner-run
  (`exchange/CLAUDE_WEB_TOOLS/doc_round_rat32/INSTALL_RAT32.md`), before the day of the first Approval 1. H-2 v2 r1 stays.

## 7. 15 November 2026, about 18:06 - the RAT-32 documentation install

- **Where:** the owner's CMD window, pasted into the Claude chat (blocks 2 and 3 of
  `exchange/CLAUDE_WEB_TOOLS/doc_round_rat32/INSTALL_RAT32.md`; block 1 reported done).
- **Result:** ZIP PASS, POST PASS, COMMITTED PASS; pushed as **`5b4df41`**. Claude's check from GitHub: the commit adds exactly
  the three files, each with its ratified SHA-256; no file under `src/`, no root `.bat` and no `requirements.txt` has changed
  since `cc0ab73`. H-1 v3 (with its blurb) is now the installed Claude handover; H-2 v2 r1 stays the reviewer's; register
  v0.30 is the installed register. The next register edition records `5b4df41`.

## 8. 15 November 2026, about 18:15 - tonight: Oz Lotto only, streamlined review

- **Where:** the owner's message in the Claude chat, with the reviewer's agreement (EX_193).
- **Owner's words:** "ok per your recommendations lets start and do only OzLotto tonight. Yes to "1. Ask the reviewer to agree
  tonight's exact blocks once, upfront"". (`results\` is about 181 MB.)
- **Status:** DECIDED for tonight only: Oz Lotto from the official-page check to its seal, following readiness sheet r2c
  (blob `b544438f...` at this edition's check) exactly; each step on the owner's own go after Claude has checked the previous
  output; the reviewer reviews the whole recorded sequence afterwards, or at any STOP (EX_193's five safeguards). Powerball on
  another evening, on its own gos. D1-D7 unchanged.

## 9. 15 November 2026, about 18:17 - STOP at the official-page check (prerequisite 3)

- **What happened:** the check exited 1 with `FAIL` for both games: "parsed 9 draw(s) 1576-1568 ... equal to the master 9/9",
  then "FAIL: expected exactly draws 1568-1576 (9); the parser returned 9" (Oz Lotto the same with 1693-1685). Window recorded
  unchanged: `exchange/RUNS/GOV_SMOKE_2026_11_15_owner_window.txt`. Nothing was written (clean status before and after); nothing
  opened; no approval given.
- **Status:** STOP (EX_193 safeguard 4; sheet prerequisite 3). No rerun, no repair, no Approval 1 tonight until Claude proposes
  a response, the reviewer reviews it and the owner authorises it.

## 10. 15 November 2026, about 18:37 - the owner's own look at the 26-draw pages

- **Where:** the owner's message in the Claude chat, after EX_194.
- **Owner's words:** "yes both show 26 draws.  no "load more" or similar."
- **Status:** an owner observation (not a check run, not a go): the two pre-quarantine pages the check r2 will load
  (31 January to 31 July 2026) each show all 26 draws, with no paging or "load more". Waiting: the reviewer's EX_195.

## 11. 15 November 2026, about 18:50 - prerequisite 3 with the check r2: PASS

- **Where:** the owner's new go in the Claude chat ("ok go I'll do those step 1 commands again now"), after EX_195; his CMD
  window recorded unchanged: `exchange/RUNS/GOV_SMOKE_r2_2026_11_15_owner_window.txt`.
- **Result:** clean status before and after; both blob lines `449b5cd3...`; the seven `[GOV-SMOKE]` lines identical to sheet
  r2d's expected lines (26 draws per game, listed newest first, weekly rule 26/26, equal to the master 26/26); EXIT 0.
  **PASS** (checked by Claude line by line). Approval 1 for Oz Lotto must follow on the same day (15 November 2026).

## 12. 15 November 2026, about 19:01 - prerequisite 4: backups confirmed

- **Where:** the owner's CMD window (robocopy to `G:\BACKUPS\powerball_modeh_2026-11-15\`, another drive), recorded unchanged:
  `exchange/RUNS/BACKUP_2026_11_15_owner_window.txt`.
- **Result:** `source_data` 6 files and `results` 78,148 files (181.94 MB) copied, FAILED 0, exit 1 each (robocopy's "copied,
  no errors"); the two list-only checks found Copied 0, Mismatch 0, FAILED 0, exit 0 each. **Backups confirmed (R-015 (c)).**

## 13. 15 November 2026, about 19:10 - prerequisites 5 and 6: tree check PASS

- **Where:** the owner's CMD window (pasted in the chat; recorded as `exchange/RUNS/TREE_CHECK_2026_11_15_owner_window.txt`,
  the pull's file list abbreviated, every check line unchanged).
- **Result:** clean status; only `__pycache__/` folders ignored under `src/`; no change to `src/`, root `.bat` or
  `requirements.txt` since `cc0ab73`; both masters at their version-1 SHA-256 (Oz Lotto `4a6cecc2...`, Powerball
  `ce0ae7e7...`); no orphan marker. **PASS.** The owner is asked to confirm that Claude Code and VS Code's Python terminals
  are closed. Claude holds its own pushes from here until the owner's witness push after Approval 1.

## 14. 15 November 2026, about 19:18 - Oz Lotto Approval 1, part 1: the study manifest

- **Where:** the owner's go and CMD window in the Claude chat.
- **Output (verbatim):** `[MODE-H] MANIFEST written for OZLOTTO: 40 variants, targets 1694-1703, frozen master version 1,
  closure 497 files, digest ed6e569ce560..., environment digest 5bf4eb8a36dd...`
- **Claude's check:** 40 variants, targets 1694-1703, master version 1, 497 closure files, environment digest `5bf4eb8a36dd`
  (T024's): all as sheet r2d expects. **PASS.** The freeze holds from here until both games are sealed. Next: the opening
  record (permanent), on the owner's go.

## 15. 15 November 2026, about 19:19 - Oz Lotto Approval 1, part 2: the holdout OPENED

- **Where:** the owner's go and CMD window in the Claude chat; the fixed owner statement given verbatim.
- **Output (verbatim):** `[MODE-H] HOLDOUT OPENED for OZLOTTO: freeze version 1; the opening record is permanent. The display
  rule is unchanged: no outcome of a holdout draw is shown or computed with outside the sealed Mode H score.`
- **Claude's check:** as sheet r2d expects. **Oz Lotto's holdout (1694-1703) is OPENED; the opening record is permanent.**
  No results update has run; no holdout draw has been read. Next: the D3 witness push, on its own go, before Approval 2.

## 16. 15 November 2026, about 19:21 - the D3 witness push

- **Where:** the owner's go and CMD window in the Claude chat (staging checked by Claude before the commit).
- **Result:** commit **`9eb5e33c5bf19409a1ea3c9d6e5058e70a410eee`** ("Mode H OZLOTTO: study manifest and opening record (Approval
  1)"), exactly three paths: `results/audit/SEARCH_LOG.csv` (modified), `results/real/holdout/OZLOTTO/MODE_H_STUDY_MANIFEST_V1.json`
  and `source_data/HOLDOUT_OPENED_OZLOTTO.json` (added); no master, no ledger. Pushed `510a37f..9eb5e33`. GitHub's event record
  shows the push received at **2026-11-15T08:51:04Z** (19:21:04 Adelaide); the commit's own time stamp (19:20:59 +10:30) is set by
  the PC and is not the stronger item. What it shows: the study record existed on GitHub before the project first ingested any
  holdout result. Not proof of pre-draw forecasting (the draws were already public). Next: Approval 2, on its own go.

## 17. 15 November 2026, about 19:23 - Oz Lotto Approval 2: the first results update

- **Where:** the owner's go and CMD window in the Claude chat (with the read-only state snapshot, run as information).
- **Output (verbatim):** `[MASTER] OZLOTTO: checked 9 overlapping draws (all matched), added 15 (1694..1708), warnings 0` and
  `[MASTER]   grab kept: OZLOTTO_grab_draws_1685-1708_as_at_20261115_085242Z.csv; backup: OZLOTTO_master_draws_1474-1693_as_at_20261115_085242Z.csv`.
- **Snapshot:** ` M` for the Oz Lotto master and ledger only (expected; D5: left uncommitted); no lock; no `.part-` file;
  one grab and one backup, both of this run; master SHA-256 now `63e3349333f8aa0485b7b067abe70249e39de81c6d02cda1a5710cf1041a4e9e`
  (version 2).
- **Claude's check:** overlap 9, all matched; 15 added (1694-1708, the holdout and five later draws); no warnings; every
  snapshot line as a clean success leaves it. **PASS.** The holdout draws are now in the local master; no AI has seen any
  value. Next: Approval 3 (the plan), on its own go.

## 18. 15 November 2026, about 19:26 - Oz Lotto Approval 3, part 1: the plan

- **Output (verbatim):** `[WALK-FORWARD] MODE H PLAN wf-5af149aef7444336a38e469146c95a20: OZLOTTO targets 1694-1703, 40 variants,
  master version 2 63e3349333f8...` and the `next:` line naming
  `Run_Experiment.bat Method_Walk_Forward.py run --game OZLOTTO --batch wf-5af149aef7444336a38e469146c95a20`.
- **Claude's check:** targets 1694-1703, 40 variants, master version 2 with the hash from Approval 2. **PASS.** Batch id
  **`wf-5af149aef7444336a38e469146c95a20`** (400 planned pairs). Next: the batch run, on its own go.

## 19. 15 November 2026, about 19:50 - Oz Lotto Approval 3, part 2: the batch

- **Where:** the owner's go and CMD window (recorded unchanged: `exchange/RUNS/OZLOTTO_MODEH_BATCH_2026_11_15_owner_window.txt`;
  value-free: counts and attempt states only).
- **Output:** `BATCH_COMPLETE written: every planned pair has its DONE ticket` and `COMPLETE: 400 run(s) in this invocation;
  every pair of the plan is done`; the read-only status: 40 variants, each `attempts 10, done 10, pending 0`, every attempt
  `DONE: SUCCESS, consumable, under this plan's pins`; ignored attempt lines 0; lifecycle marker BATCH_COMPLETE.
- **Claude's check** (counted with a tool): 40 variants x 10 = 400 forecasts, all successful; no method failure. **PASS.**
  Next: Approval 4 (the one score and the seal), on its own go.

## 20. 15 November 2026, about 19:54 (09:23:52 UTC) - Oz Lotto Approval 4: scored and SEALED

- **Where:** the owner's go and CMD window (recorded unchanged: `exchange/RUNS/OZLOTTO_MODEH_SCORE_2026_11_15_owner_window.txt`;
  value-free).
- **Output:** study and batch verified (roster of 400 pairs); attempt `mh-ba0c301be2fb4c459492697d0137e7ed`, search-log row 8;
  outcomes read once; score ledger 800 score lines, 400 rank lines; N1 simulation; measures for 80 tracks and 40 variants;
  report files txt, csv and json written; **`MODE_H_SEALED written; the study is closed`**.
- **Claude's check:** every line as sheet r2d expects, with 800 and 400 (every forecast succeeded). **PASS. The Oz Lotto Mode H
  study is SEALED.** No AI has seen any draw value or the report. Per D6 the report files are shared after Powerball is
  sealed too (not committed now). Next for Oz Lotto: a second backup (D5); then the reviewer's review of tonight's whole
  sequence (EX_193). Powerball on another evening, on its own gos, with a new page check on its Approval 1 day.

## 21. 15 November 2026, about 19:55-20:01 - the backup after Oz Lotto's seal (D5)

- **Where:** the owner's CMD window, pasted in the chat at 22:02 (robocopy to
  `G:\BACKUPS\powerball_modeh_2026-11-15_after_ozlotto_seal\`).
- **Result:** `source_data` 9 files (42.7 kB) and `results` 79,362 files (188.95 MB) copied, FAILED 0 and Mismatch 0 in both
  summaries; the first exit line `ROBOCOPY EXIT 1`; the second exit line's value was not in the pasted text (the summary shows
  no failure). **Backup after the seal confirmed.**

## 22. 15 November 2026, about 22:07 - the reviewer's audit of the Oz Lotto sequence (EX_196)

- **Result:** EX_196: **PASS WITH EVIDENCE LIMITATIONS**; no blocking discrepancy; MODE_H_SEALED as recorded; no replay,
  extra fetch or correction warranted; EX_193's arrangement was for Oz Lotto only (Powerball gets its own).
- **Its main limitation:** several windows were quoted in this log, not stored as standalone files. Claude has now stored
  the owner's windows exactly as pasted into the Claude chat (manifest, opening, witness push, first update with its
  snapshot and the plan, and the backup after the seal) in `exchange/RUNS/` (`OZLOTTO_APPROVAL1_MANIFEST_...`,
  `OZLOTTO_APPROVAL1_OPEN_...`, `OZLOTTO_WITNESS_PUSH_...` (Parts A and B together), `OZLOTTO_APPROVAL2_UPDATE_AND_PLAN_...`,
  `BACKUP_AFTER_OZLOTTO_SEAL_...`). They are the chat pastes, not reconstructions; where a paste was cut off (the second
  backup's last exit line), the file ends where the paste ended. Lesson carried: store each window as it arrives.

## 23. 16 November 2026, about 18:39 - the OUTLANDISH_01 pre-holdout Oz Lotto export

- **Where:** the owner's go and CMD window in the Claude chat, after the reviewer's blocking finding on the tool (module not
  registered before execution) was fixed as r3 (`8c4bec69...`, commit `76d1c6d`).
- **Certificate (from the window):** source the committed version-1 master `4a6cecc2...`; draws 1474 (17 May 2022, the current
  format) to 1693; exclusive cutoff 1694 (the parent project's Oz Lotto holdout 1694-1703); 220 rows; every row 10 distinct
  values in 1-47; no gaps or duplicates; dates off the weekly rule 0; order check: mains already ascending 0/220, supplementaries
  ascending 36/220 (about 37 expected for an unsorted order), so the page's stored order is NOT a sorted order; read only the
  committed Git bytes. File `GAIS/OUTLANDISH_01/OZLOTTO_preholdout_only.csv`, 9,829 bytes, LF, SHA-256 `82557ea5...c44c`;
  committed by the owner at `c528be4` (Git stores the LF bytes; checked by Claude by hash only, no value read).
- **Status:** done. No holdout draw is in the file. This concerns the side project only; it changes nothing in Mode H or the
  freeze.

## 24. 16 November 2026, about 19:05-19:30 - Powerball tonight; the annex reviewed; the arrangement extended

- **Owner's words (19:04, with the reviewer):** "I will persist with this tonight !" (Powerball Mode H tonight if practical, with
  breaks; OUTLANDISH development paused meanwhile, 19:24).
- **EX_197 / EX_198:** the expected-state annex r1 to sheet r2d (blob `cc00da36...`): PASS WITH NONBLOCKING CLARIFICATIONS (E0
  is the pre-Powerball status; after the witness commit the search log's modified mark clears until a later step changes it
  again). The reviewer extends EX_193's arrangement to Powerball's session of 16 November 2026, on the same terms: the owner's
  own go per step; Claude checks every output first and stores each window in exchange/RUNS/ as it arrives; the reviewer
  reviews the whole record afterwards or any STOP. The page check and Approval 1 on the same Adelaide day; breaks allowed.
- **Status:** the arrangement is agreed; nothing is authorised by it. Each step waits for the owner's go.

## 25. 16 November 2026, about 20:05 - Powerball prerequisite 3 (the page check, Powerball only): PASS

- **Where:** the owner's go and CMD window (`exchange/RUNS/POWERBALL_GOV_SMOKE_r2_2026_11_16_owner_window.txt`, as pasted).
- **Result:** nothing incoming before the pull; `git status --short` exactly E0 (annex r1), identical before and after; both
  blob lines `449b5cd3...`; the four `[GOV-SMOKE]` lines identical to the annex (26 draws 1551-1576, listed newest first, weekly
  rule 26/26, equal to the master 26/26); EXIT 0. **PASS** (compared with a tool). Powerball's Approval 1 must follow on
  16 November 2026. Claude holds its pushes from here until the owner's witness push.

## 26. 16 November 2026, about 20:17 - Powerball prerequisite 4: backups confirmed

- **Where:** the owner's CMD window, stored unchanged: `exchange/RUNS/POWERBALL_BACKUP_BEFORE_2026_11_16_owner_window.txt`
  (to `G:\BACKUPS\powerball_modeh_2026-11-16_before_powerball\`).
- **Result:** `source_data` 9 files and `results` 79,362 files (188.95 MB) copied, FAILED 0, exit 1 each; both list-only
  checks Copied 0, Mismatch 0, FAILED 0, exit 0 each. **Backups confirmed.** (Held locally until the witness push.)

## 27. 16 November 2026, about 20:18 - Powerball prerequisites 5 and 6: tree check PASS

- **Where:** the owner's CMD window, stored as pasted: `exchange/RUNS/POWERBALL_TREE_CHECK_2026_11_16_owner_window.txt`.
- **Result:** `git status --short` exactly E0; only `__pycache__/` ignored under `src/`; no change to `src/`, root `.bat` or
  `requirements.txt` since `cc0ab73`; Oz Lotto master `63e33493...` (version 2), Powerball master `ce0ae7e7...` (version 1);
  no orphan marker. **PASS** (annex r1). (Held locally until the witness push.)

## 28. 16 November 2026, about 20:25 - Powerball Approval 1, part 1: the study manifest

- **Output (verbatim, stored in exchange/RUNS/):** `[MODE-H] MANIFEST written for POWERBALL: 40 variants, targets 1577-1586,
  frozen master version 1, closure 497 files, digest ed6e569ce560..., environment digest 5bf4eb8a36dd...`
- **Claude's check:** 40 variants; targets 1577-1586; version 1; 497 files; environment digest `5bf4eb8a36dd`. The closure
  digest `ed6e569ce560` is the same as Oz Lotto's manifest of 15 November: the frozen code is unchanged between the two studies.
  **PASS.** Next: the opening record (permanent), on the owner's go.

## 29. 16 November 2026, about 20:26 - Powerball Approval 1, part 2: the holdout OPENED

- **Output (verbatim, stored in exchange/RUNS/):** `[MODE-H] HOLDOUT OPENED for POWERBALL: freeze version 1; the opening record
  is permanent. The display rule is unchanged: no outcome of a holdout draw is shown or computed with outside the sealed Mode H
  score.`
- **Claude's check:** as expected. **Powerball's holdout (1577-1586) is OPENED; permanent.** No results update yet. Next: the
  D3 witness push, on its own go.

## 30. 16 November 2026, about 20:28 - the Powerball D3 witness push

- **Where:** the owner's gos (Parts A and B; staging checked by Claude before the commit); window stored as
  `exchange/RUNS/POWERBALL_WITNESS_PUSH_2026_11_16_owner_window.txt`.
- **Result:** commit **`c302871dfd0860320c0f898c093beded9e14cc4c`**, exactly three paths: `results/audit/SEARCH_LOG.csv`
  (modified; it also carries Oz Lotto's later value-free rows), `results/real/holdout/POWERBALL/MODE_H_STUDY_MANIFEST_V1.json`
  and `source_data/HOLDOUT_OPENED_POWERBALL.json` (added); no master, ledger or report. Pushed `50472b4..c302871`. GitHub's
  repository activity record shows the push received at **2026-11-16T09:58:02Z** (20:28:02 Adelaide), before any Powerball
  holdout result was fetched. Status afterwards: E0 without the search-log line (EX_198 note 2). Next: Approval 2.

## 31. 16 November 2026, about 20:37 (10:00:04 UTC) - Powerball Approval 2: the first results update

- **Output (verbatim, stored in exchange/RUNS/):** `[MASTER] POWERBALL: checked 9 overlapping draws (all matched), added 15
  (1577..1591), warnings 0` and `[MASTER]   grab kept: POWERBALL_grab_draws_1568-1591_as_at_20261116_100004Z.csv; backup:
  POWERBALL_master_draws_1144-1576_as_at_20261116_100004Z.csv`.
- **Claude's check:** exactly as annex r1 expects (9 overlap all matched; 15 added 1577-1591, the holdout and five later draws;
  no warnings; grab and backup of this run). **PASS.** The read-only snapshot was requested next, before the plan.
- **Snapshot (about 20:43; stored as `exchange/RUNS/POWERBALL_APPROVAL2_SNAPSHOT_2026_11_16_owner_window.txt`):** ` M` for both
  games' masters and ledgers only; no lock; no `.part-` file; one grab and one backup per game, Powerball's of this run;
  Powerball master SHA-256 now **`e4f2feb8b18fc2dbe389583a189fa26127a648f4da940dd76219ee282170f3e0`** (version 2). Clean.
  Next: Approval 3 (the plan), on its own go.

## 32. 16 November 2026, about 20:44 - Powerball Approval 3, part 1: the plan

- **Output (verbatim, stored in exchange/RUNS/):** `MODE H PLAN wf-5085cd8feaf54cffb22823ab5869d5a8: POWERBALL targets 1577-1586,
  40 variants, master version 2 e4f2feb8b18f...` and the `next:` run line.
- **Claude's check:** targets 1577-1586, 40 variants, master version 2 with Approval 2's hash. **PASS.** Batch id
  **`wf-5085cd8feaf54cffb22823ab5869d5a8`** (400 planned pairs). Next: the batch run, on its own go.

## 33. 16 November 2026, about 20:49 - Powerball Approval 3, part 2: the batch

- **Where:** the owner's go and CMD window (stored unchanged: `exchange/RUNS/POWERBALL_MODEH_BATCH_2026_11_16_owner_window.txt`).
- **Output:** `BATCH_COMPLETE written` and `COMPLETE: 400 run(s) in this invocation; every pair of the plan is done`; the status:
  40 variants, each attempts 10, done 10, pending 0, every attempt `DONE: SUCCESS, consumable, under this plan's pins`; ignored
  attempt lines 0; marker BATCH_COMPLETE.
- **Claude's check** (counted with a tool): 400 of 400 forecasts SUCCESS; no method failure. **PASS.** Next: Approval 4.

## 34. 16 November 2026, about 20:53 (10:22:23 UTC) - Powerball Approval 4: scored and SEALED; Mode H complete

- **Where:** the owner's go and CMD window (stored unchanged: `exchange/RUNS/POWERBALL_MODEH_SCORE_2026_11_16_owner_window.txt`).
- **Output:** study and batch verified (roster 400); attempt `mh-24b3eb05319d4051be2f5e6ae1e6c8b8`, search-log row 12; outcomes
  read once; 800 score lines, 400 rank lines; N1; measures for 80 tracks and 40 variants; txt, csv and json written;
  **`MODE_H_SEALED written; the study is closed`**; the SEALED line names batch `wf-5085cd8f...`.
- **Claude's check:** every line as expected. **PASS. The Powerball Mode H study is SEALED. With Oz Lotto's (entry 20), both
  games are sealed: Mode H is complete and the freeze (r2d section 7) ends here.** No AI has seen a drawn value or a report.
- **Next:** a backup after the seal (D5); the reviewer's review of tonight's sequence; then D6 (both value-free reports shared
  together), the register recording the study, the holdout exposure record, the handovers refreshed, and the owner's separate
  D5 decision on committing the updated masters, ledgers and records; then MHUP-B.

## 35. 16 November 2026, about 20:54-21:00 - the backup after Powerball's seal (D5)

- **Where:** the owner's CMD window, stored as pasted: `exchange/RUNS/POWERBALL_BACKUP_AFTER_SEAL_2026_11_16_owner_window.txt`
  (to `G:\BACKUPS\powerball_modeh_2026-11-16_after_powerball_seal\`).
- **Result:** `source_data` 12 files (61.6 kB) and `results` 80,576 files (196.85 MB) copied, FAILED 0, exit 1 each. **Backup
  after the seal confirmed.** Both games' sealed states are now backed up on `G:`.

## 36. 16 November 2026, about 21:08 - the reviewer's audit of the Powerball sequence (EX_199)

- **Result:** EX_199: **PASS WITH EVIDENCE LIMITATIONS**; Powerball SEALED accepted; **Mode H execution complete; the freeze
  ended**. C01 (nonblocking): the after-seal backup's read-only `/L` comparison is not recorded; proposed as an optional step
  on its own go. C02 (nonblocking): stale clauses in CONTINUITY_NOW.md; fixed the same evening. D5 and D6 still govern.

## 37. 16 November 2026, about 21:09 - EX_199 C01 closed: the after-seal backup checked

- **Where:** the owner's go and CMD window, stored as pasted:
  `exchange/RUNS/POWERBALL_BACKUP_AFTER_SEAL_CHECK_2026_11_16_owner_window.txt`.
- **Result:** both read-only `/L` comparisons of `G:\BACKUPS\powerball_modeh_2026-11-16_after_powerball_seal\`: `source_data`
  12 files and `results` 80,576 files, Copied 0, Mismatch 0, FAILED 0, exit 0 each. The copy matches the original. **C01 closed.**

## 38. 16 November 2026, about 21:13 - D6: both Mode H reports given to Claude; Claude's reading sealed until the reviewer's

- **Where:** the owner uploaded the two value-free report `.txt` files to the Claude chat (D6: both together, after both seals).
  Oz Lotto report SHA-256 `68112928b332666c8e2da6504b06e93a81295cf21682cd076d0a85e754ebd0e6` (585,497 bytes); Powerball report
  SHA-256 `1bad6295f5af67845412983c3c37ae48156530dad3b12ce24ad3234cf4177ffc` (750,084 bytes), as uploaded. Claude has not
  committed the reports (their commit is the owner's D5 decision).
- **Status:** Claude's independent reading is written (EX_201, on Fable) and given to the owner in the chat. It is NOT yet
  published here, so that the reviewer's own reading (EX_200) stays independent. Its SHA-256 (CRLF bytes, 13,202 bytes) is
  `8e350fe7385cd4b94f976ae823c8fbc0fa657cf5b6e536305d4ff8777c235dbd`; Claude publishes the file unchanged, with its reading
  tools, once EX_200 has been given, and then compares the two readings.

## 39. 16 November 2026, about 21:36 - D6: the reviewer's reading (EX_200) given; EX_201 published unchanged; the two compared

- **Where:** the owner gave Claude the reviewer's independent reading at 21:36 with the words: "ok for this part of the
  experiment ...". Recorded unchanged: `exchange/EX_200_ChatGPT.md` (13,507 bytes, SHA-256
  `bff769e209acc08b4968f6f36c2ad36e67d93d4be3a7c4ccc3d040939332bd98`).
- **Published:** `exchange/EX_201_Claude.md`, byte-identical to the fingerprint of entry 38 (`8e350fe7...`, 13,202 bytes), with
  the four reading tools and a README in `exchange/CLAUDE_WEB_TOOLS/modeh_reading/`.
- **The comparison (EX_202):** the two readings, written without sight of each other, agree on the result and on every figure
  they share: **null at the 5% level in each of the three predeclared MR7 families** (Bonferroni P 1.000 Oz Lotto main
  numbers, 0.672 Powerball main numbers, 0.920 Powerball number). They differ in coverage and in two points of wording,
  where Claude adopts the reviewer's: the Bonferroni figure is the family result and the N1 maximum figure is a reference
  only; and "no advantage detected", not "no sign". The reviewer also raised that the three families are not adjusted
  against each other (Claude had missed it; no effect, since none passes its own 5%). Every figure EX_200 quotes was checked
  against the reports: all match.
- **Open with the reviewer (EX_202):** Q1 the wording proposed for the record; Q2 whether EX_201's exploratory sections 3.3
  and 3.4 stand, are qualified or are withdrawn; Q3 the dispositions of EX_201's suggestions (the "watch-items" withdrawn as
  a separate step; the aggregate measure carried to the MHUP-B design as an option; the development-report comparison to the
  ideas backlog).
- **Not yet decided:** how Mode H is worded in the register is the owner's decision after the reviewer's reply (level 1).
  Nothing was rerun, rescored or changed; no raw draw value, master, ledger or forecast entered either chat.

## 40. 16 November 2026, about 21:49 - the reviewer's assessment of EX_201 (EX_203): AGREE, three nonblocking qualifications

- **Where:** pasted by the owner into the Claude chat at 21:49; recorded unchanged below a two-line header as
  `exchange/EX_203_ChatGPT.md`. Claude's reply: `exchange/EX_204_Claude.md`.
- **Result:** EX_200 and EX_201 are "consistent independent scientific readings"; no blocking disagreement, no alteration of
  either sealed study, no rerun. Three qualifications, all accepted by Claude (EX_204): (1) "about three independent bets"
  and its one-sigma reading stay provisional and exploratory; (2) the 1/2,081 comparison illustrates multiple testing and is
  not a calibration; (3) record wording: "No statistically significant predictive advantage was demonstrated under the
  predeclared Mode H tests."
- **EX_202's questions:** EX_203 does not mention EX_202 (they crossed). Claude reads it as answering Q2 (EX_201 sections 3.3
  and 3.4 stand, labelled exploratory) and Q3 in substance (hypotheses kept for prospective examination only with definitions
  and treatment fixed before new outcomes: MHUP-B design work); Q1's wording comes to the reviewer inside register v0.31.
  The reviewer may still say otherwise.
- **The reviewer's broader point (the development evidence):** agreed. Counts checked against register v0.30: Powerball 432
  targets (17,280 runs), Oz Lotto 219 targets (8,760 runs), 26,040 in all. Precision: Powerball's ranking report scored the
  report window 1286-1576 (291 draws). Those development reports (H-1 v3 section 7.5; 1 November 2026) also showed nothing
  departing from fair draws (Oz Lotto family Bonferroni P 0.090; Powerball main numbers 1.0). The tiers stay separate.
- **Not yet decided:** the record wording is the owner's decision when register v0.31 is ratified (level 1).

## 41. 16 November 2026, about 21:54 - the reviewer's reply to EX_202 (its own EX_203): Q1 accept, Q2 retain qualified, Q3 agree; a numbering correction

- **Numbering correction (read this first):** the reviewer's own `EX_203_ChatGPT.md` (its reply to EX_202) arrived five
  minutes after Claude had filed the reviewer's unnumbered pasted assessment of EX_201 under that number (entry 40, commit
  `f41f380`). The reviewer's file keeps its number: `exchange/EX_203_ChatGPT.md` (5,360 bytes, SHA-256
  `155eeae629dfaf772c0a584c0314f1cfab63b7c2630c628d961cd66f1e1201b0`), recorded unchanged. The pasted assessment is now
  `exchange/EX_203A_ChatGPT.md` (the reviewer's text unchanged; only Claude's header lines differ). **Where entry 40 and
  EX_204 say "EX_203", they mean EX_203A.** Entry 40 and EX_204 are not edited.
- **Where:** the owner uploaded the file to the Claude chat at 21:54. Claude's reply: `exchange/EX_205_Claude.md`.
- **Result (EX_203):** Q1 ACCEPT WITH WORDING PRECISION (state the pass thresholds as counts, 21 Oz Lotto and 25 Powerball
  main-number matches, "not a formal power calculation"; say "Bonferroni family-adjusted P" and "no statistically significant
  advantage detected"). Q2 RETAIN WITH FURTHER QUALIFICATION (EX_201 sections 3.3 and 3.4 stay as historical post hoc
  exploration and are not rewritten; the descriptive counts are kept; "about three independent bets", "roughly one sigma",
  "one time in six" and the cross-game "one-in-two" are not calibrated and do not enter the record). Q3 AGREE (no separate
  watch-items step; the aggregate statistic is an MHUP-B design option only; the development-report comparison goes to the
  ideas backlog).
- **Claude (EX_205):** accepted in full. The same threshold-not-power caveat applies to EX_201 section 4, to EX_204 section 3
  and to Claude's summaries to the owner. The record wording as it now stands (r2) is EX_205 section 5.
- **Not yet decided:** the record wording is the owner's decision when register v0.31 is ratified (level 1). Nothing was
  rerun, rescored or changed.

## 42. 16 November 2026, about 22:12 - the owner's question: full-history walk-forward ranking, and where it sits in the plan

- **Where:** the owner's note to the Claude chat, with his two queries to the reviewer and the reviewer's brief for Claude
  (provisional name ALL_WALKFORWARD_RANKING_EVALUATING). Recorded unchanged:
  `exchange/DECISIONS/OWNER_REQUEST_2026_11_16_ALL_WALKFORWARD_RANKING_EVALUATING.txt`.
- **The owner's two questions, in his words:** "(i) can we display the ranking stats for last 3 draws ? (ii) where the ranking
  and performance vs chance reports fit into the forward plan ?" He asked for a brief reply. The brief states: "this is a
  fact-finding and planning request only. No development, execution, rescoring, file modification or release is authorised."
- **Claude's answer (in the chat; facts checked in the roadmap, R3 17.3.6 and the report tool's code):**
  - The objective as the owner recalls it is roadmap item 10 (WF-1A and WF-1B), done 31 October to 1 November 2026: every past
    draw forecast from the draws before it (Powerball 432 targets, Oz Lotto 219; 40 variants), scored, ranked and compared
    with chance. The two development reports exist (Oz Lotto window 1474-1693; Powerball window 1286-1576, R3's default
    start at the first draw of 2021). The figures of EX_200 to EX_205 are the ten-draw holdouts only.
  - "Last 3 draws": the report tool ranks over any window inside a batch, so the last three development draws can be
    reported with the existing tool as new owner-run report operations (a non-registered window has no family-adjusted
    figure). The sealed holdouts cannot be re-windowed. The last three draws in the dataset (after the holdouts) have not
    been forecast: that is MHUP-B's catch-up. The tool does not print a table after every draw; that is one run per draw.
  - The plan: done, item 10 and Mode H; next, MHUP-B (weekly update, catch-up, scoring, a new dated league table each time);
    then WF-1C; later, item 21b (one consolidated report with development, Mode H, catch-up and prospective kept separate).
- **Open:** which three draws the owner means; whether he uploads the two development `.txt` reports for a plain summary;
  whether item 21b is brought forward (a roadmap change: the owner's decision after review). Nothing is authorised.

## 43. 16 November 2026, about 22:19 - the owner's two questions on the sealed holdouts and on Claude's access to `results\` (open)

- **The owner's words:** "a deeper dive on holdouts - now that we have looked at them (1) why can't we now treat them as a
  normal part of the dataset (which we must eventually anyway since the holdouts only purpose is now achieved) ? (2) why
  can you not yet access results\ since I think we are entering the next phase of processing full draws and results ongoing ?"
- **Claude's answer (in the chat):**
  - (1) They already are ordinary history under the ratified design (Mode H design v0.1r7: "a sealed holdout is ordinary
    history"; the weekly scope starts at `holdout_last + 1` and trains on everything before it). Three things stay special:
    the Mode H scores keep their own label and are shown beside, never pooled with, the other tiers; a later method's
    forecasts of those ten draws count as development evidence only (the owner's own condition of 13 November); the sealed
    records are not rescored. What is missing is code, not permission: the report tool's Phase 1 cap (R3 17.3.6: L <= 1576
    and 1693) and the catch-up and weekly machinery, which is MHUP-B.
  - (2) It is the owner's decision Q7 of 13 November 2026, not a technical limit. Its first reason (blindness before
    Mode H) has lapsed for the ten holdout draws; two reasons remain (one simple rule for folders that will hold every
    future draw and forecast; the method designer should not browse outcomes and per-draw scores). The rule is wider than
    those reasons need: the value-free `.txt` reports under `results\method_rankings\` are already committed and public.
- **Options put to the owner (not decided; level 1, after the reviewer's view):** A keep Q7 as it is (the owner uploads the
  reports); **B (Claude's recommendation)** a narrow amendment: the AI chats may read the committed value-free `.txt`
  report files under `results/method_rankings/`, and nothing else in `results/`, `source_data/` or `transitory_data/`;
  C open the folders fully (not recommended). If B is decided it is written into H-1 v4; the local runner's rulebook is
  unchanged.

## 44. 16 November 2026, about 22:26 - the owner's preference: drop the raw-draw-value restriction (Q7); fix the code gap "asap"

- **The owner's words:** "\"There is no automatic table after every draw over the history\" seems like a gap. into the future
  every new draw (and sometimes we will miss some draws and have a min-catchup) that will be required. OK, (1) \"What stops
  us today is missing code, not a rule\" needs to be fixed asap (2) I see the risk associated with \"I design the method\" as
  extremely low and acceptable on the basis that I assess that you are very much smarter and more ethical than letting
  knowledge of draw numbers interfere with designing and programming algorithms to assess and use the individual draw
  numbers, so lets get rid of that rule. We treat all draws the same is my preference unless you have a very strong
  objection."
- **Claude's position (in the chat): no strong objection to (2).** The reason is the design's structure, not Claude's
  character: every future forecast is frozen before its draw exists, so having seen past draws cannot leak a future one,
  and results on already-seen draws are development evidence by rule. Knowing the data can still shape what is designed
  without anyone intending it; the cost falls only on evidence that is already non-confirmatory.
- **What Claude recommends stays, whatever is decided on Q7:** (a) the AIs never contact lottery websites or search for
  results (a separate rule; the owner's updater stays the only source); (b) evidence comes only from the reviewed programs
  and their logged runs, and anything an AI computes from raw draws in a chat is exploratory and is never quoted as a
  result; (c) Claude writes only under `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`, the sealed Mode H records are
  untouched, and the local runner's rulebook is left as it is (the runner needs no draw value).
- **Status: NOT YET IN FORCE.** Q7 is a ratified rule and the reviewer earlier leaned to keeping it (EX_125 O03, EX_127 O01),
  so under P1 (level 1) the reviewer's view is sought first; then the owner confirms. Until then Claude keeps Q7 exactly.
  If confirmed it is recorded in register v0.31 and H-1 v4, and the practical step is the owner's D5 commit of the updated
  masters, ledgers and reports (Claude's clone sees only what is on GitHub).
- **On (1):** the table after every new draw, catch-ups included, is already in the ratified design (Mode H, update and
  prospective design v0.1r7 section 6.6: each session writes the dated cumulative league table) and is MHUP-B's scope
  (marked HIGH). Not designed anywhere: the same table over the past history; raising the report tool's Phase 1 cap
  (R3 17.3.6). Claude proposes both as items for the MHUP-B design. The MHUP-B design starts on the owner's "go".

## 45. 16 November 2026, about 22:39 - the owner on catch-ups, no future holdouts, re-rankings, and the three rules to keep

- **The owner's words (as written):** "Every forward forecast is frozen before its draw exists, so my having seen old draws can’t leak a future one" and "Old draws are already non-confirmatory" ... nearly ... catchups for missing a few weeks are the edge case and I accept the associated risks, I still assess you are better than letting such things interfere even in the absence of "admin" and rules. we do not need holdouts for future method development in my view.  New methods will by the nature of our project of course cause re-rankings and re-[performance vs chance] of all draws up to the latest in the dataset, replacing prior now-obsolete rankings etc.     OK 1. No lottery websites or results searches by the AIs.  2. "Evidence comes only from the reviewed programs and their logged runs"  ... although it can and must be clearly stated as suggestive as it may lead to now and novel methods 3. "My write limits and the local runner’s rulebook stay as they are" I do not understand this one, whatever they are they need reviewing and possibleo chnage to align with what we are discussing here and KISS and least-admin unless there is a "safety" issue of some kind in your view which we can explore and decide on.
- **Claude's reading:** (a) catch-up forecasts of already-public draws are the edge case to "the future protects itself";
  the owner accepts that risk, and the design already labels them CATCH-UP (retrospective). (b) No holdout for future method
  development: consistent with the ratified design (a later method never gets a fresh holdout; forward forecasts are its
  test). (c) Re-ranking over all draws when a method is added: consistent with "a league table is a dated view"; the new
  table is the current one and earlier dated reports stay on file. One design question follows: a single all-history table
  beside the labelled tiers (for the MHUP-B design, with the reviewer). (d) Rules 1 and 2 agreed, rule 2 with the owner's
  addition: what an AI computes in a chat is "suggestive", stated as such, and may lead to new methods.
- **Rule 3 explained and reviewed, as the owner asked:** `exchange/DECISIONS/RULES_AFTER_Q7_DRAFT_r1.md` lists every current
  restriction with DROP, KEEP or CHANGE and the reason. Claude's view: there is a safety reason for two things and only two:
  Claude's write limits (an AI mistake cannot damage the data or the sealed records; nothing reaches the code without the
  reviewer and the owner) and the operating rules of the local runner, which sits on the owner's PC beside the real data.
  Neither is about seeing draws. The runner's two draw-visibility rules (4 and 5) have no safety reason left and are
  proposed for removal inside MHUP-B's rulebook edition, with no separate round.
- **Status: NOT YET IN FORCE.** The draft goes to the reviewer; the owner then confirms. Until then Q7 stands.

## 46. 16 November 2026, about 22:51 - OWNER DECISIONS: Claude's write limit removed (conditional); the runner's rules kept; the league table

- **The owner's words (as written):** yes. re "A single table over all draws" lets clarify that ... if it is a single table showing all results for all draws in descending order, historical results/rankings could perhaps be kept in separate files (filename by game and draw number and 5 digit version or something) and maybe when requested simply be appended together or something into one report; nice columns or csv or something may be useful, I don't know, see what you can design for a dummy human. If it is something else please clarify what you mean.  I am more interested in the latest ranking/performance which i think we had agreed was based on hit-rates or something of all previous draws (I may be wrong) ? If I'm wrong please say so and clarify why. I hereby remove the limitation "I can only put files in `exchange\` and the runner’s folder" as long as you are always careful not to destroy anything - if you must, do good archiving or something.  Yes keep runners rules for Claude Code. yes to your proposal for "Runner’s two draw rules" as long as it never kills nor interferes with any other data.
- **Decided by the owner:**
  1. **Claude's write limit is removed**, on his condition: always careful not to destroy anything; archive if something
     must go.
  2. **The local runner's rules are kept.**
  3. **The runner's two draw-visibility rules (4 and 5)** are dropped or reworded inside MHUP-B's rulebook edition, on his
     condition that the runner "never kills nor interferes with any other data".
- **How Claude will use decision 1** (`exchange/DECISIONS/RULES_AFTER_Q7_DRAFT_r2.md` section 2A; Claude's own working rule,
  open to the owner's correction): documents may be committed directly once reviewed and ratified by SHA-256; code and tests
  keep the reviewed-package route with the Windows rehearsal and the owner's install; the data folders are never written by
  Claude; nothing is deleted or overwritten (a superseded file moves to `superseded/` or `archive/`); and Claude does not use
  the wider permission before the owner has seen the reviewer's reply to the draft. Decision 1 was made before the
  reviewer's view (P1, level 1): the reviewer is asked in r2's question Q5.
- **Read by Claude as the owner's go for the MHUP-B design (design only):** "yes." and "see what you can design for a dummy
  human", after Claude's request to say "go MHUP-B". The owner may correct this reading. No code, install or run is authorised.
- **The league table, clarified:** the owner's recollection is right: the ranking is cumulative, by each method's hits over
  all scored draws, against chance. By "a single table over all draws" Claude meant one added column giving each method one
  figure over every scored draw, beside the separate kinds of evidence. The owner's ideas (numbered files per game and draw,
  joined on request, CSV, a plain layout) and a first sketch are in
  `exchange/DECISIONS/MHUPB_DESIGN_INPUTS_2026_11_16.md` (design inputs D-1 to D-10; not a design, not reviewed).
- **Still not in force:** the draw-visibility rules (Q7) stand until the owner confirms after the reviewer's reply.

## 47. 16 November 2026, about 23:07 - OWNER DECISION: the approach agreed (seven lines); D5 now; documents first, then the reviewer

- **Before it (22:58 and 22:59), the owner's words:** "I like the sketch as a starting point for your design , it could include
  all methods not only the top "n"." and "I have not pasted anything of this discussion with chatgpt yet and dio not plan to
  until we agree we have workable approach."
- **The owner's words at 23:07 (as written), replying to Claude's seven-line summary:** ok. 2. unless I agree to something on a case by case basis only. 3. archiving may need to consider date/time appended to filename or something in case multiples in a session or day.  5. I hope this considers and takes into account this discussion.  6. perhaps stays on file means each superseded ranking gets archived somehow (see above) ?7. I don't know what this means but if you say it's good then lets do it.   "Your D5 commit of the updated results files" please lead me through doing that now. ok to "When a new method’s back-history gets built (roadmap item 21b). I’d settle that inside the MHUP-B design."  I thin you should update your handover-to-new-claude document(s) and all other documents that need updating right now for risk management, then we tell/consult chatgpt about all this.
- **Recorded as:** `exchange/DECISIONS/AGREED_APPROACH_2026_11_16.md` (the seven lines with his amendments: exceptions to the
  three protections only case by case; archive names carry the date and time; each superseded ranking is its own archived
  file; the close-out runs alongside MHUP-B).
- **D5 DECIDED:** the owner commits the updated results files now, led step by step by Claude, named paths only.
- **Order set by the owner:** documents updated first for risk management, then the reviewer is told and consulted. So the
  owner has decided before the reviewer's view; the reviewer's reply may still lead him to adjust.
- **Documents tonight:** this log, the agreed-approach page, the recovery page (rewritten) and the roadmap's top note. The
  formal editions (register v0.31, H-1 v4) need review and ratification and are the next sitting's work.

## 48. 16 November 2026, about 23:11-23:15 - D5 DONE: the owner committed and pushed the Mode H results (commit c7622fa)

- **Where:** the owner's go and CMD windows, stored as pasted: `exchange/RUNS/D5_STEP1_PULL_AND_STATUS_2026_11_16_owner_window.txt`
  and `exchange/RUNS/D5_STEPS_2_3_ADD_COMMIT_PUSH_2026_11_16_owner_window.txt`.
- **Before:** `git pull --ff-only` to `e17fcc9`; status 5 modified and 20 untracked files, all Mode H, nothing else.
- **Commit `c7622fa`** (named paths only, 25 files): both results masters and their ledgers (version 2), the search log, the
  six Mode H report files, the two `MODE_H_BATCH_ID.json` records, and each game's batch folder (plan, segment record,
  `BATCH_COMPLETE`, `SCORING_STARTED`, `SCORE_COMPLETE`, `MODE_H_SEALED`). Pushed `e17fcc9..c7622fa`; the tree is clean.
- **Claude's check from GitHub (fingerprints only):** the committed Oz Lotto master (`63e33493...`), Powerball master
  (`e4f2feb8...`) and the two report `.txt` files (`68112928...`, `1bad6295...`) are byte-identical to the SHA-256 values
  recorded at the seals and in entry 38. Nothing outside `source_data/` and `results/` is in the commit. **PASS.**
- **Not committed, by design:** the git-ignored run folders, attempts ledgers and score ledgers (they stay on the owner's PC
  and in his backups on `G:`).

## 49. 16 November 2026, about 23:17-23:30 - documents first; then unattended design work on the remaining Fable allowance

- **The owner's words:** "I'd prefer it tonight please, for some reason I feel shaky that we may lose all this good work."
  (23:11); "the doc updates are #1 priority though" (23:18); "brilliant. is there something you would like to start tonight
  since i have 25% fable left to use before 11:30 am tomorrow ? preferably unattended by me." (23:30).
- **Done for risk management:** the H-1 v4 DRAFT and its blurb draft (`exchange/CLAUDE_WEB_TOOLS/h1v4/out/`; commit
  `21b7220`), built from H-1 v3's ratified bytes; `exchange/CONTINUITY_NOW.md` says how to start a new chat from them.
  Not reviewed, not ratified.
- **Done unattended (design only, as authorised in entry 46):** `exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_DRAFT_v0_1.md`,
  a first draft applying the owner's inputs D-1 to D-10 to the ratified design v0.1r7. Its main points: the ratified
  section 6 is not reopened; the league table's layout, files and history; planning arithmetic on how long forward testing
  takes; and a recommendation that MHUP-B carry no scope that can wait (a new method's back-history and the report window
  cap go to a small follow-on package), because each week without the weekly session is a forward draw lost for good.
  Nothing in it is decided: it lists five questions for the reviewer and four decisions for the owner.

## 50. 17 November 2026, about 09:46 - the reviewer's view on the agreed approach (EX_206): AGREE WITH CONDITIONS

- **Where:** the owner gave Claude `EX_206_ChatGPT.md`; recorded unchanged as `exchange/EX_206_ChatGPT.md`.
- **Result:** the reviewer supports the owner's seven-line approach of 16 November 2026 and answers the five questions of
  `RULES_AFTER_Q7_DRAFT_r2.md`: Q1 agree (the AI chats may read draw values and results; N-1 isolation, forecast identities
  and append-only evidence kept; chat computation is suggestive; evaluation on already-known draws is development evidence,
  never prospective); Q2 agree to the all-history descriptive table with every method, a forward-only column beside it and
  the kinds identified; backfilled rankings never shown as if they existed earlier; Q3 agree to close the exposure record in
  register v0.31, keeping the HX-1 and HX-2 facts; Q4 the runner's rules 4 and 5 stay binding until MHUP-B's reviewed
  rulebook edition; Q5 agree with conditions that match section 2A (named paths, hash checks, collision-proof archive names,
  coordination with the owner's Git activity; code by package; no writes to the data folders, `GAIS/` or protected
  settings; no reset, clean, overwrite or force push).
- **Also:** the owner authorised the reviewer to commit its own H-2 handover files; it committed an H-2 v3 CANDIDATE and its
  blurb to `doc/HANDOVER/` (commits `5204c41` and `e631380`). Not ratified; H-2 v2 r1 stays the installed handover.
- **Status:** the approach is now agreed by the owner and reviewed. The owner keeps the final say on its wording and
  effective date. The MHUP-B design supplement draft is still to be reviewed under the normal rules.

## 51. 17 November 2026, about 09:49 - OWNER PREFERENCE: both kinds of measure; MHUP-B as full as possible, not small

- **The owner's words:** "BRIEFLY PLS CLARIFY IN PRACTISE WEHAT THIS MEANS "Fixing one overall measure in advance, instead of
  testing 80 tickets at once,"" (09:46) and "can we have both one measure as well as all the other measures ? My preference
  is to implement as much as possible as fast as possible rather than Keep MHUP-B small so it can start sooner." (09:49).
- **Claude's answer:** yes to both measures: one overall measure, fixed in advance as the primary forward test, with every
  existing measure and the 80-track family kept beside it (how the two share the 5% is a question for the reviewer).
- **On scope, Claude withdraws the recommendation of the supplement's section 7.** By the supplement's own arithmetic
  (section 5) a few forward draws more or less change little against the hundreds needed, and one package means one design
  review and one install round. So MHUP-B is to carry: the ratified weekly session; the league table, files and history;
  the one overall measure; a new method's back-history; the report window cap lifted; the consolidated report (roadmap 21b);
  and the scoring of Powerball targets 1145 to 1285. The cost is a larger review and rehearsal, to be built in tested layers.
- **Next:** the supplement revised to v0.2 on that basis (Fable, High; on the owner's go), then to the reviewer.

## 52. 17 November 2026, about 09:51-09:56 - the owner's "go" for design v0.2; the reviewer's review of v0.1 (EX_207)

- **The owner's words:** "go" (09:51, to Claude's "Suggest switching to Fable (High) for this"), and at 09:56, with the
  reviewer's file: "fyi, chatgpt assessment of your last post in case that helps:".
- **EX_207** (recorded unchanged as `exchange/EX_207_ChatGPT_REVISED_20261117.md`): CONDITIONAL PASS ON DIRECTION on draft
  v0.1, revised by the reviewer for entry 51 before it was relayed. It accepts the full MHUP-B in independently tested
  layers with the live forecast and score path isolated; supports one overall primary forward measure in principle, with
  its formula, null calibration, error budget and repeated-look policy still to be specified; prefers one confirmatory
  test at 5% with the 80-track family secondary; corrects the reading of v0.1's power figures; and asks for a cross-source
  read contract, zero-score variants shown, LOW_N under 30, `LATE_PRE_DRAW` stated, and past-draw rankings labelled as a
  reconstruction. It requires its own review of v0.2's actual bytes.
- **Done on that go (design only):** `exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_DRAFT_v0_2.md`, with
  `overall_measure_check.py` and its output. v0.2 answers each EX_207 point (its section 1), sets out eight layers with
  acceptance gates and the isolation rule, and defines the overall measure OV-1: per forward draw, the summed weight of the
  drawn numbers (methods favouring minus methods disfavouring each number), divided by its exact fair-draw spread; both
  games together; two-sided; read formally five times only (52, 104, 208, 416, 832 forward draws) at 1% each; everything
  else secondary. Claude withdrew v0.1's claim that one measure would be more than twice as fast.
- **Not decided:** v0.2 lists seven questions for the reviewer and four decisions for the owner. Nothing is authorised.

## 53. 17 November 2026, about 11:49 - OWNER DECISION: the holdout draws opened to re-forecasting; the sealed forecasts kept as history

- **The owner's words** (on v0.2's decision 3, "the 40 current variants can never be re-forecast on the holdout draws"):
  "For 3. Retain current forecasts as separate history but specifically open up holdouts to reforecasting ... so everything
  draws and methods all get treated the same."
- **Claude's view: agreed, with three guard rails,** built into draft v0.3 section 7: (1) the sealed Mode H forecasts,
  scores, markers and reports stay exactly as they are, as separate history; (2) every re-forecast of a holdout draw is
  development evidence, for any variant, and can never be called holdout or forward evidence; (3) each variant's result for
  a draw is counted once in any total: the all-draws column takes the walk-forward record and shows the Mode H result
  beside it. Re-forecasting cannot make a second blind test and does not weaken the first; it makes the pipeline uniform.
- **A gain:** where the method revision is unchanged, the re-forecast should equal the sealed forecast exactly, so the
  batch report compares them (v0.3 section 7.2 rule 7): a reproducibility check of Mode H.
- **Recorded as:** `exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_DRAFT_v0_3.md` (replaces v0.2; v0.1 and v0.2 kept).
  The reviewer has yet to review it (question R-6 asks about this decision). Nothing is authorised to run.

## 54. 17 November 2026, midday - the reviewer's review of v0.2 (EX_208): recheck required on four points; draft v0.4

- **The owner, 11:52:** "Ps i am on my phone so can only give short responses".
- **EX_208** was committed to `exchange/` by the reviewer itself (commit `613da3d`). Disposition: RECHECK REQUIRED BEFORE
  RATIFICATION; it supports the eight-layer full MHUP-B, the isolated live path, the descriptive league and the OV-1
  concept. Four points: (1) OV-1's zero mean needs complete TOP and WORST pairs; (2) five readings at 2.576 are nominal,
  not a guaranteed 5% (an exact counterexample: 1.0718% at one reading); (3) pooling the games conflicts with ratified
  R3 17.3.1 and needs the owner's explicit choice; (4) back-history misses weekly targets closed before a variant's release,
  and de-duplication must not be by scoring policy. Also: no OV-1 on the sealed holdout draws by default; the local-clock
  class is acceptable for the formal sample if its limitation is printed.
- **Claude checked the counterexample** (`ov1_eprocess_check.py`): reproduced to every printed digit. The reviewer is right.
- **Draft v0.4** (`exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_DRAFT_v0_4.md`, commit `980004d`; v0.1 to v0.3
  kept) answers all four and keeps entry 53: complete-pair eligibility; the five readings replaced by an exact evidence
  score (a test martingale from the exact fair-draw distribution of each draw's weights; the chance of ever reaching the
  bar is at most 5% however often it is looked at); per game (bar 40) or joint (bar 20, needing an exception to R3 17.3.1)
  put to the owner; rule 2A for closed weekly targets; de-duplication by target and readout with one approved policy.
- **Correction of a commit message:** commit `980004d` says it holds entries 53-54 and a CONTINUITY_NOW update; entry 53 was
  already in `02f97cd`, and entry 54 and the CONTINUITY_NOW update are in the commit after it.
- **Open:** the owner's choice of Option P or J; the reviewer's review of v0.4 (six questions). Nothing is authorised.

## 55. 17 November 2026, about 12:55 - OWNER DECISION: the overall measure is scored per game (Option P)

- **Where:** Claude's tap question in the chat (the owner was on his phone). Asked: should the overall measure be scored per
  game or for both games together? Offered: "Per game (Recommended)", "Both games together", "Ask ChatGPT first".
- **The owner's answer:** "Per game (Recommended)".
- **So:** OV-1 has one evidence score for Powerball and one for Oz Lotto, each with a bar of 40 (2.5% each, 5% in all). No
  exception to R3 17.3.1 is needed; games are never pooled. The joint figure may be shown as secondary. Draft v0.4 section
  6.3 still shows both options; the next revision (after the reviewer's review of v0.4) will state Option P as decided.

## 56. 17 November 2026, about 12:09 - OWNER: the reviewer may commit its replies to `exchange/`

- **The owner's words:** "Ok. Fyi chatgpt can now commit to exchange for you to read a respinse from there."
- **So:** the reviewer's EX messages may arrive as its own commits under `exchange/` (as EX_208 did, commit `613da3d`), besides
  its H-2 handover files in `doc/HANDOVER/` (EX_206). The owner no longer has to carry each file across.
- **Claude's practice from now:** fetch and fast-forward before reading or writing anything; take the next free EX number
  only after fetching (the EX_203 lesson); rebase and push by named paths; never edit a file the reviewer committed.

## 57. 17 November 2026, about 12:37 - the reviewer's recheck of v0.4 (EX_209): pass with corrections; draft v0.5 (EX_210)

- **The owner's words:** "Good. Please check." Claude fetched and read `exchange/EX_209_ChatGPT.md` (the reviewer's own commit
  `44c75bb`).
- **EX_209:** PASS WITH CORRECTIONS; a focused recheck before ratification. The mathematics of the evidence score is passed
  (a genuine test martingale; the chance a game's score ever reaches 40 is at most 2.5%; 5% in all by the union bound).
  Corrections: B01 register the test before its first contributing draw; B02 a numerical contract so the bound holds for
  the program; C01 compare forecast content, not whole records, with the sealed forecasts; C02 a score or typed status per
  eligible target; C03 name each writer and path; C04 bind the OV-1 ledger to the freeze line and outcome pin; C05 record
  Option P as decided and make no joint figure; and bind the selected score version by identity (R-5). The reviewer
  expects to recommend ratification if these are made.
- **Draft v0.5** (`exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_DRAFT_v0_5.md`) applies all of them; EX_210 is the
  covering note with the table of where each landed. v0.1 to v0.4 are kept. Nothing is authorised.

## 58. 17 November 2026, about 14:15-14:20 - the owner's clarifying questions, and his input on a "current" folder

- **The owner asked (14:15)** how catch-up works after missed rounds, and what happens when a method is modified or added.
  Claude's answers, from the design: catch-up takes only the missed draws, oldest first, each forecast from the draws before
  it, then freezes the next forecast; nothing earlier is redone. A new or modified method (a new revision) is walked forward
  from its first valid draw to the latest as development evidence; only the new or changed variants are computed; every
  other method's frozen forecasts and scores are reused; a new league table becomes the current one.
- **The owner's words (14:20):** ""The earlier tables stay as their own dated files; nothing is overwritten." good, perhaps in
  a superseded folder or something so that "current" are easily identifiable by being the only set of results/rankings in
  a main or "current" folder. Yes "marked retired" is the righ thing to do so method versions results are never mixed up.
  I'll read the decisions after chatgpt's review."
- **Design input D-11 (for the next revision of the supplement, after the reviewer's recheck of v0.5):** every table is
  written once, create-only, into a permanent archive folder and logged there; a `current` folder holds a copy of the
  newest set only, replaced each time. The archive is the record and never moves (so no logged path ever changes); the
  `current` copy is a convenience and the only thing that is ever replaced. A failed copy never affects the archive.
- **Confirmed by the owner:** a modified method's old revision is marked retired and its results are never mixed with the
  new revision's.

## 59. 17 November 2026, about 14:27 - the reviewer's recheck of v0.5 (EX_211): design pass; draft v0.6; the owner on the four decisions

- **EX_211** (the reviewer's commit `3f6a4b5`): FOCUSED DESIGN PASS WITH TWO NARROW CLARIFICATIONS AND CODE-ROUND GATES. F01: a
  missing pre-outcome eligibility line must stop the primary stream openly, never silently. F02: the lower-bound guarantee
  must cover every running component, the mixture and the comparison with 40. Also a wording precision on C03, and the
  owner's D-11 accepted with a whole-set integrity rule. It recommends ratification once these are recorded; the numerical
  implementation and source-schema checks are gates of the code round.
- **The owner's words (14:27):** "please check for ex_211, also noting chatgpt's advice on the decisions "What I would do I
  recommend approving O-1, O-2 and O-3 together when Claude's next corrected supplement has passed its focused recheck.
  Those are design decisions, not permission to start programming or running experiments. For O-4, approve the objective
  now, but retain the separate execution authorisation until the command has been checked. That avoids an unnecessarily
  early real-data operation. The two outstanding EX_211 points-pre-outcome OV-1 eligibility recording and conservative
  numerical comparison with threshold 40-are narrow and should not require reconsidering your scientific approach. Bottom
  line: I support all four proposals. Three can proceed as design approvals following the final recheck; the fourth needs
  a later, specific run approval." which I accept unless you have other views in which case we will discuss."
- **Claude's view:** no other view; agreed. So: O-1, O-2 and O-3 are to be approved together when v0.6 has passed its
  check; O-4's objective is approved, its run needing a separate go once the command is reviewed. Design approvals are not
  permission to write code or run anything.
- **Draft v0.6** (`exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_DRAFT_v0_6.md`; EX_212 is the covering note)
  records F01, F02, the C03 wording and D-11. Nothing else changed from v0.5.

## 60. 17 November 2026, about 14:40 - the reviewer's final recheck (EX_213): design pass, ratification recommended with RC-1

- **The owner's words:** "Wonderful, I like what you have done. Thanks. I'll past that blurb to chatgpt now." (14:38) and
  "check" (14:40). Claude fetched and read `exchange/EX_213_ChatGPT.md` (the reviewer's commit `1b8d34a`).
- **EX_213:** FOCUSED DESIGN PASS on v0.6; it recommends the owner ratify the supplement with one narrow condition, RC-1: after
  a stopped primary stream, a new registration gets no automatic new 2.5% allowance and needs an explicit reviewed
  error-budget allocation; a recovery after the outcome may continue the original stream only under a rule fixed in
  advance and independent of the outcome. The code round's gates remain (numerical implementation, source schemas,
  de-duplication tests, eligibility restart tests, live-path isolation, the Windows rehearsal).
- **Claude:** RC-1 accepted and written into section 6.8. The ratification candidate is
  `exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_v0_7_RATIFICATION_CANDIDATE.md` (38,428 bytes; SHA-256
  `04c4f68a638fff7d93f06d25084d1454bdfc443e9aab6b0b12ffdfd8b5323d26`; Git blob `7acd172c586aba407200cc0b2abcbbcb1fb2aa71`):
  v0.6 with RC-1 and a status header, nothing else changed.
- **Awaiting:** the owner's explicit ratification of that file and his approval of O-1 to O-3 (and O-4's objective).

## 61. 17 November 2026, 14:48 - OWNER RATIFICATION: the MHUP-B design supplement v0.7; O-1 to O-3 approved; O-4's objective approved

- **Where:** Claude's tap question in the chat. Asked: "Do you ratify the design (supplement v0.7) and approve O-1, O-2 and
  O-3, with O-4's objective approved and its run needing a separate go? This approves the design only: no code, run or
  install." Offered: "Yes, ratify (Recommended)", "Not yet".
- **The owner's answer:** "Yes, ratify (Recommended)".
- **Ratified:** `exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_v0_7_RATIFICATION_CANDIDATE.md`, SHA-256
  `04c4f68a638fff7d93f06d25084d1454bdfc443e9aab6b0b12ffdfd8b5323d26` (38,428 bytes; Git blob
  `7acd172c586aba407200cc0b2abcbbcb1fb2aa71`; commit `9f7625e`), after the reviewer's design pass and recommendation
  (EX_213), with its condition RC-1 included. To be numbered and recorded in register v0.31 (the next number after RAT-32),
  and copied into `doc/` unchanged with that register.
- **Approved with it:** O-1 the league table, its files, the `current` folder and the archive; O-2 OV-1 as the one
  confirmatory forward test for each game (evidence score, bar 40), everything else secondary; O-3 the window contract and
  the re-forecasting rules; O-4 the objective of scoring Powerball targets 1145-1285 (the run needs a separate go once its
  command is reviewed).
- **Not authorised by this:** any code, package, install, run, rescore, re-forecast or registration of the primary test.
  The code round's gates listed in the supplement's header stand.
- **P6 note (Claude, on how this round went):** six drafts in a day, each answering a specific review. The reviewer found
  two real faults (a cut-off that did not guarantee its error rate; back-history that missed closed weekly targets) and
  both were fixed by simpler mechanisms than the ones they replaced. The reviewer committing its replies to `exchange/`
  removed the relay step. Claude's slips: one inaccurate commit message (corrected in entry 54) and one claim about
  numerical loss stated before it was shown (withdrawn). Lesson kept: check a guarantee by exact computation before
  writing the word.

## 62. 17 November 2026, about 14:54 - the paperwork before the code round: register v0.31 and H-1 v4 (EX_214)

- **The owner's words:** "re "I recommend doing the paperwork first and then starting the code work in a fresh Claude chat.
  This chat is very long, and the code round is the worst place to lose one. Everything a new chat needs is on GitHub now;
  the finished H-1 v4 would make the takeover cleaner." ok, great call. I assume just before we do the actual handover you
  will have re-checked and updated the handover and/or blurb if required. SO, yes to I give chatgpt the blurb then you do
  the paperwork."
- **Done (on Opus):** register v0.31 (`exchange/CLAUDE_WEB_TOOLS/register/RATIFICATION_REGISTER_v0_31.md`, SHA-256
  `465dc50a55120e8afdd983475c7d94b8ac0ff654e46507df96532862ac7fb5f2`) and H-1 v4 with its blurb
  (`exchange/CLAUDE_WEB_TOOLS/h1v4/out/`, SHA-256 `0f34ec4c...2c2` and `2cfa6cf5...67be`), each built by a counted-edit builder
  from the installed bytes and reproduced from scratch. Sent for the reviewer's documentary review as EX_214. Register
  v0.31 records RAT-33 and asks for RAT-34 (register v0.31, H-1 v4 and its blurb, and the approach of 16 November 2026 in
  force with them).
- **Claude's commitment (the owner's assumption, confirmed):** just before the handover to a new Claude chat, Claude
  re-checks H-1 v4, its blurb and `exchange/CONTINUITY_NOW.md` against GitHub and updates them if anything has moved.

## 63. 17 November 2026, about 15:15 - RAT-34: register v0.31, H-1 v4 and its blurb ratified; the approach of 16 November in force

- **The owner's words (15:14):** "check ex_215 whilst also noting: chatgpt "My recommendation: You can proceed with RAT-34 for
  register v0.31, H-1 v4 and its blurb, with the previously ratified MHUP-B v0.7 supplement installed alongside them. Claude
  should verify the final ratified-file hashes after the limited status updates. Keep H-2 v3 for a separate update and
  ratification. This need not delay the fresh Claude chat or its subsequent readiness check.""
- **EX_215** (the reviewer's commit `ebfe97d`; as stored `3f16bfd0c4bb756834731fd46c2fc9013f92a808fa63b333d02c279a31e9203f`):
  DOCUMENTARY PASS; it recommends RAT-34; it agrees RAT-34 is the right point for the approach of 16 November to take effect,
  with the EX_206 conditions as written; it agrees the closing of the exposure record; it recommends H-2 v3 be updated by the
  reviewer and ratified separately, not with RAT-34. A note for the successor chat: "nothing is tested again on the sealed
  holdouts" means the sealed study is never reopened; it does not forbid the new development re-forecasts of RAT-33.
- **Claude's tap question:** "Do you ratify register v0.31, H-1 v4 and its blurb, with your approach of 16 November coming
  into force with them? The ratified MHUP-B design goes into doc/ alongside. H-2 v3 waits for ChatGPT to update it, as it
  advises. This authorises no code, run or install." **The owner's answer:** "Yes, ratify (Recommended)".
- **RAT-34 is recorded. The approach of 16 November 2026 is in force from now**, with the EX_206 conditions.
- **The status-only changes** (`exchange/CLAUDE_WEB_TOOLS/doc_round_rat34/finalise_rat34.py`; the candidate-to-final diffs in
  its `final/` folder): H-1 v4's status line; the register's version line, its RAT-34 paragraph and two status cells. Final
  SHA-256: register v0.31 `c6369a72753ebda016f758e623df7a40bcb7a1300a49d503ccbb93be1b3cae6d`; H-1 v4
  `cc52ed4f988d9a4044d3699de7626717b4a0fd760e927aa1ad582187edbc8d3d`; its blurb (unchanged)
  `2cfa6cf521aabee3bbef257eb8a917caea92c73ddac54e90ddda79464ecd67be`; the RAT-33 supplement (unchanged)
  `04c4f68a638fff7d93f06d25084d1454bdfc443e9aab6b0b12ffdfd8b5323d26`.
- **Committed by Claude directly into `doc/`** (the first use of the wider write permission): `doc/RATIFICATION_REGISTER_v0_31.md`,
  `doc/HANDOVER/Claude_Primary_Handover_H1_v4.md`, its blurb, `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_7.md`.
  New files only; nothing existing was changed or removed. Checked from GitHub after the push (CONTINUITY_NOW records the
  commit). The owner only pulls.

## 64. 17 November 2026, about 15:23-16:01 - HO-2: the new Claude chat's takeover; PASS; OWNER AUTHORISATION of normal work and of the MHUP-B code plan

- **The takeover (H-1 v4 section 0, item 4).** The owner started a fresh Claude chat at about 15:23 from the H-1 v4 blurb. It
  read and checked first (101 of H-1 v4's quoted file hashes match Git; one historical row, see below) and gave its first
  substantive reply to the owner, uncommitted.
- **Two narrow exceptions to "no commit before authorisation".** Asked by tap question whether the reply could be committed so
  the reviewer could read it from GitHub, the owner answered "Yes, as EX_216 (Recommended)" (about 15:40), and for the blind
  answers "Yes, as EX_218 (Recommended)" (about 15:50). **Correction (EX_219 section 4): EX_218's cover says "about 16:00";
  the time was about 15:50.** The owner: "for me "about 16:00" reads as close enough to 15:50 in this specific case so no
  need to update it." EX_218 is not edited.
- **The exchange:** EX_216 (Claude's first reply, commit `7243599`); EX_217 (the reviewer's five questions only, `6db4827`);
  EX_218 (Claude's blind answers, `0070640`); **EX_219 (the reviewer, `a18ac58`): HO-2 TAKEOVER PASS**, no further quiz, with
  two cautions for the code plan: C1, no convenient alpha-recycling after a stopped OV-1 stream (default: stay in PRIMARY
  STREAM STOP; any distinct fresh test needs a reviewed argument preserving the programme's 5% and the owner's decision);
  C2, take the actual test baseline on current `main` before fixing anything, and keep T024's 571 as dated history.
- **The owner's words (16:01):** "EX_219 is available for you to read. I authorise you as the new Claude chat to resume
  normal work and have changed your model to Fable (High) for the MHUP-B eight-layer code plan. That plan must return to
  the chatgpt Reviewer for independent review before implementation code is written. Thanks and welcome here !"
- **So:** normal work is authorised; the code plan is authorised on Fable (High); no implementation code before its review.
  As EX_219 says, this approves no code, package, install, runner task, real-data run, OV-1 registration or weekly session.
- **Discrepancies the new chat reported (EX_216 section 6; none blocking):** D1 the recovery page pointed to the older H-2 v3
  starter text (corrected in CONTINUITY_NOW with this entry); D2 H-1 v4 Appendix A quotes the readiness sheet's r2c hash at a
  path that now holds r2d (r2c is at commit `454921f`); D3 `exchange/README.md` v0.5 predates RAT-34's write rules (a v0.6
  to be proposed for review); D4 "87 Bash deny patterns" in H-1 is 84 deny plus 3 allow; D5 H-1 says E_2 has six variants
  (it has three; the total of 40 is right); D6 the roadmap and reminders were last refreshed on 16 November; D7 the
  supplement in `doc/` is stored CRLF, deliberately. D2, D4 and D5 are for the next H-1 edition.
- **P6 note (Claude, on how the takeover went):** H-1 v4 with CONTINUITY_NOW was enough to take over from the repository
  alone. The friction was in side files not refreshed at each milestone and in commits made after the blurb's anchor.
  Suggestion: at each ratification CONTINUITY_NOW names the newest starter files by path.

## 65. 17 November 2026, about 18:15 - the MHUP-B code plan, draft v0.1, sent for review (EX_220); the baseline taken; no owner decision

- **Done under entry 64's authorisation (Fable, High; plan only, no implementation code):**
  `exchange/CLAUDE_WEB_TOOLS/mhupb/codeplan/MHUPB_CODE_PLAN_DRAFT_v0_1.md`, sent to the reviewer as EX_220.
- **The baseline (EX_219 C2; cloud workspace, a disposable clone of `b30919d`, E2R-T12 left out):** Python 3.13.18 and
  3.15.0b4 each ran 570 tests in 45 modules; two tests fail, both in `tests/test_multigame_reader_contracts.py`
  (`test_master_source_and_ledger_file_hashes`, `test_only_legacy_e1_allowed_at_boundary`), both the documented
  version-1-master failures (readiness F-2). No unexpected failure. Nothing was fixed or relabelled.
- **What reading the installed code showed (plan section 2):** MHUP-A already installed most of the weekly gate plumbing;
  but the mode-to-pin rule of design 3.4(a) is enforced nowhere yet; development plans, requests and reports stop at the
  old cap in three places; no outcome after the holdout is released to any scorer; and a development report over exactly
  the holdout window would load the Mode H families. Each is a planned, reviewed change.
- **OV-1's arithmetic (plan section 6; the probe `ov1_lower_bound_probe.py`, invented data):** integers only, every
  rounding against a crossing, exact sums across draws, and a per-draw check that the stored factors average at most 1
  under fair draws. Loss about 1e-30 per draw; about 0.1 s per draw at 40 variants; identical output on both Pythons.
- **Waiting for the owner later, after the review (plan section 12; none decided, none assumed):** OD-1 (a development
  batch that names its variants: declined as ER-6 on 31 October 2026, but needed by the supplement's rule 2A); OD-2 (a
  missed week and OV-1); OD-3 (the cut-off for OV-1's pre-draw record); OD-4 (no recovery after a stop: recommended);
  OD-5 (a read-only census of the real score records before the install); OD-6 (three review slices).
- **Model (MC-1):** the Fable task is finished. Opus is enough until the reviewer replies; Fable again for any plan
  revision that touches OV-1's arithmetic, the release rules or the gates.

## 66. 17 November 2026, about 16:50 - correction of entry 65's time

- Entry 65's heading says "about 18:15". **The time was about 16:45.** Claude's slip: a step that was to correct the time
  in two files stopped after the first, and the commit went ahead (commit `2b050e4`). `exchange/CONTINUITY_NOW.md` has the
  right time. Nothing else in entry 65 is affected. Lesson kept: when a correction touches several files, check each
  before committing; this log holds the owner's words as written, which are not all US-ASCII, so it is opened as bytes.

## 67. 17 November 2026, about 16:54 - OWNER INSTRUCTION: no MHUP-B coding until the plan is complete and ratified, and a specific go

- **The owner's words:** "when you get the chatgpt review, please do not commence coding using it until I give specific
  authorization, we need to ensure the plan in complete and ratified before that."
- **So:** after the reviewer's review of the code plan (EX_220), Claude only reads it, revises the plan and puts the
  decisions (OD-1 to OD-6) to the owner. The plan is to be complete and owner-ratified first; implementation code starts
  only on the owner's specific authorisation after that. A review PASS is not that authorisation.
- **Also (16:50):** the owner asked Claude to name the model to select before each piece of evaluation or work; Claude
  does so at the start of each piece (MC-1). The permission mode stays on Auto (16:52); the project's own go points are
  unchanged by it.

## 68. 17 November 2026, about 18:24 - the reviewer's review of code plan v0.1: EX_223 (supersedes EX_221 and EX_222)

- **The owner's words (18:24):** "ok EX_223 supersedes both EX_221 and EX_222, so read and use EX_223 whilst also noting the
  in-place "minimum admin overhead" agreement."
- **EX_223** (the reviewer's commit `b5678d8`; as stored `8f1b86d3...5c`; EX_221 at `0114ee1` and EX_222 at `4e73031` kept
  as history): PASS WITH REQUIRED CORRECTIONS; not yet ready for ratification or code. B01 a precise OV-1 missed-week and
  noon-cut-off rule (needs a design amendment); B02 the league table's archive and search-log row made crash-consistent;
  B03 the same-day release gap closed by the release instant; B04 two kinds of development rerun (ROUTINE_FILL and
  EXPLORATORY_RERUN), which the owner asked for; C01 one initiator and one writer per ledger; C02 OV-1's failure
  semantics; C03 the one small tracked LEAGUE_SOURCES file, no extra chain; C04 the plan audited against the
  minimum-administration approach (P0-P6, entry 1; "KISS and least-admin", entry 45). Recommendations on OD-1 to OD-6
  given; the owner has decided none of them yet.
- **The owner's two questions to the reviewer after EX_221** (as EX_222 records them): whether the recommendations let any
  eligible method be re-run over eligible history for development, and whether the plan keeps to the minimum-admin
  approach without weakening review or science.
- **Next:** code plan v0.2 and the smallest design amendment, then a focused recheck, then the owner's ratification of the
  complete plan; no code before a specific go (entry 67).

## 69. 17 November 2026, about 18:43 - OWNER DIRECTIONS on OD-1 to OD-4 and OD-6 (code plan section 12; EX_223 section 3); OD-5 open

- **Where:** the owner's message in the Claude chat, after Claude set out each decision with its own and the reviewer's
  recommendation (which agreed on all six).
- **The owner's words:** "OD-1 yes to A. OD-2 yes to B conditionally as reviewer indicated. OD-3 yes to B. OD-4 yes to A.
  OD-5 I don't understand it nor why the secrecy/controls around it as we are now past that need (eg holdouts), feel
  free to discuss after OD-6 is noted. OD-6 yes to A. Please do not progress anything else until OD-1 through 6 are all
  formally agreed."
- **So (directions for plan v0.2 and the design amendment; the exact wording returns to the owner for ratification):**
  - **OD-1 = A:** two kinds of development run: routine fill (a new method's own variants and gaps) and exploratory rerun
    (any runnable method, variants or the whole cohort, over any eligible past draws, on the owner's request). Separate
    immutable attempts; never counted twice; the main league's one score per key chosen by a fixed rule; sealed Mode H
    untouched. This is a new, narrow exception to the full-cohort choice of 31 October 2026 (ER-6 declined).
  - **OD-2 = B, conditionally as the reviewer indicated (EX_223 B01):** a draw with no qualifying frozen set counts as a
    neutral factor of 1 under a rule fixed at registration, decided by the program from the complete chained records and
    provably blind to the outcome; a frozen set without its pre-draw entry is still a stop; if such a rule cannot be
    specified and proved, option A (stop) applies.
  - **OD-3 = B:** noon Adelaide time on the draw day as the last moment for OV-1's pre-draw entry; the forecast deadline
    stays midnight. Open point: the owner's confirmation that both games are drawn in the evening.
  - **OD-4 = A:** after a genuine stop the stream stays stopped; no restart or second registration in MHUP-B.
  - **OD-6 = A:** three technical review slices, one integrated review, one install; no extra owner approvals per slice.
  - **OD-5: OPEN.** The owner questions the need and the controls; to be discussed.
- **Nothing else is progressed until all six are agreed (the owner's instruction).**

## 70. 17 November 2026, about 19:03 - OD-5 agreed and done; OD-3's fact confirmed; OD-1 to OD-6 ALL AGREED

- **OD-5, the owner's words:** (18:47) "my answer: before. why cant we pop them into github as far as I can tell they are open
  info and you can see them from there if you like and any programs can read them whenever they like (am I wrong ?) ?";
  (18:50) "lets fix that now so it never gets lost - which 2 lines ?"; (19:03) "both close at 7.30pm (AEST) . pushed."
- **Claude's answer:** he is right. Since RAT-34 the score records are open to both AIs; they were git-ignored for bulk and
  for the old rule against sharing the Mode H score ledger, which no longer applies. The earlier wording about printing
  "only counts and field names" was habit and is withdrawn.
- **Done by the owner (commit `cc665ce`):** the development score records (two report attempts: the score ledger, the rank
  ledger and the scoring plan each) and the two Mode H score ledgers with their scoring plans, ten files, committed
  unchanged; and `.gitignore` with both `scores/` lines commented out.
- **Claude's check from GitHub (the one-time census of OD-5; `exchange/CLAUDE_WEB_TOOLS/mhupb/codeplan/score_census.py` and its
  output in `evidence/`): PASS.** Every file is canonical with no CR byte; both Mode H score ledgers equal the SHA-256 in
  their `SCORE_COMPLETE` and `MODE_H_SEALED` markers (1,200 lines each); every scoring plan matches its search-log row;
  every (track, draw) key is unique; the record fields are the ones the installed writers define. Worth knowing for the
  plan: the development scores of E_1 are for revision 2 (now superseded); E_1 revision 3 has no development score yet,
  so a routine fill for it is among the first runs MHUP-B makes possible.
- **A side effect, known and accepted for now:** Claude had advised leaving the `results/real/holdout/scores/` line in
  place because `tests/test_mhupa_launchers.py` (`test_gitignore_lines`) requires it; with the line commented out that one
  test fails. So the baseline on `main` from `cc665ce` is three known failing tests: the two of entry 65 and this one.
  The MHUP-B package updates that test with the ignore list (tests only); nothing is relabelled as a skip.
- **OD-3's fact, the owner's words:** "both close at 7.30pm (AEST)". Noon Adelaide time is 11:30 or 12:30 AEST, at least
  seven hours earlier. The registration will record this as the owner's statement.
- **ALL SIX AGREED (directions; the exact wording returns for ratification with the complete plan):** OD-1 A; OD-2 B
  conditionally as the reviewer indicated; OD-3 B; OD-4 A; OD-5 the check before the install, done as above; OD-6 A.
- **Next, on the owner's go:** code plan v0.2 and the design supplement's next full edition (Fable, High), then the
  reviewer's focused recheck, then the owner's ratification; no code before a specific go (entry 67).

## 71. 17 November 2026, about 19:07-20:10 - the owner's "go"; code plan v0.2 and supplement v0.8 sent for the recheck (EX_224)

- **The owner's word (19:07):** "go" (to Claude's request to start plan v0.2 and the supplement's next full edition on
  Fable, High). No code is covered by it (entry 67).
- **Done (plan and design text only):** `exchange/CLAUDE_WEB_TOOLS/mhupb/codeplan/MHUPB_CODE_PLAN_DRAFT_v0_2.md` (a full
  edition; its section 1A maps every point of EX_223) and
  `exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_v0_8_AMENDMENT_CANDIDATE.md` (a full edition built from the
  ratified v0.7's bytes by 21 counted edits; its section 1A lists them). Sent to the reviewer as EX_224 for a focused
  recheck. v0.7 stays the ratified supplement until the owner ratifies v0.8.
- **One point for the owner at ratification (R-1):** OD-3's "noon Adelaide time" is written as a fixed instant, 01:30 UTC
  on the draw date. That is noon in Adelaide during daylight saving and 11:00 in standard time: never later than noon,
  one hour stricter for about half the year, and with no time-zone rule in the code.
- **For the owner's ratification of v0.8 (its section 13):** O-5 the opportunity rule, the cut-off and the failure rules;
  O-6 the two kinds of development run and the canonical rule; O-7 the writer, source-file and publication wording.
- **Model (MC-1):** the Fable task is finished. Opus is enough to read the reviewer's recheck.

## 72. 17 November 2026, about 19:21 - correction of entry 71's time

- Entry 71's heading says "about 19:07-20:10". **The work ran from about 19:07 to about 19:20.** Claude wrote the end time
  without reading the clock, the same slip as entry 65. From now on every time Claude writes into a record is read from
  the clock by the command that writes it.

## 73. 17 November 2026, about 19:49-19:53 - EX_225 read; its two corrections applied; ratification candidates sent (EX_226)

- **The owner's word (19:49):** "go EX_225 let me know if you need fable for any of it". Claude judged Opus enough: the
  reviewer passed the arithmetic, and both corrections are precise wording and tests.
- **EX_225:** focused pass with two corrections before ratification: RC-225-1 (the missed rule rests on stated operating
  assumptions; a verified chain is local evidence, not proof of absence; reconcile with earlier records, else block) and
  RC-225-2 (a repeated admission of the same attempt is a no-op; one search-log row per publication). R-1 (the cut-off as
  01:30 UTC) accepted, to be shown to the owner as a conservative choice; R-5 (the report-only form) accepted.
- **Done:** both applied by counted edits (`make_ratification_candidates.py`):
  `exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_v0_8_RATIFICATION_CANDIDATE.md` and
  `exchange/CLAUDE_WEB_TOOLS/mhupb/codeplan/MHUPB_CODE_PLAN_v0_3_RATIFICATION_CANDIDATE.md`, with their diffs. Sent as EX_226
  for the reviewer's check of the corrections only.
- **Next:** the reviewer's check; then the owner ratifies both together (O-5 to O-7); no code until his separate go
  (entry 67).
