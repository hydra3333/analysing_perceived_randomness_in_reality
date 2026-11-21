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

## 74. 17 November 2026, about 20:06 - RAT-35: MHUP-B code plan v0.3 and design supplement v0.8 ratified together

- **EX_227 (the reviewer, commit `12877cb`):** PASS on RC-225-1 and RC-225-2; it recommends that the owner ratify the exact
  two candidates together, without further edits. It recomputed both SHA-256 values from GitHub.
- **The owner's words (20:06):** "I ratify MHUP-B code plan v0.3 and design supplement v0.8, exact files as listed in
  EX_227."
- **RAT-35 is recorded.** Ratified, byte for byte:
  - code plan v0.3, SHA-256 `d5c2b3180ffbdb28f28da95fcfc3b0ebfe87ef19653457a6c7d4a07d546d0169`;
  - design supplement v0.8, SHA-256 `e3d977e16c910dfb0c3c37b440760f3d4c6ac4588c06af519aa0f9c9be97c27e`, including the
    owner's decisions O-5 (the opportunity rule, the 01:30 UTC cut-off as a conservative choice, the failure rules and the
    missed rule's operating assumptions), O-6 (two kinds of development run; the canonical rule) and O-7 (writers, the
    source file, publication).
- **Installed by Claude (approach of 16 November 2026: ratified documents committed directly):** the same bytes as
  `doc/Predictive_Randomness_MHUPB_Code_Plan_v0_3.md` and `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md`.
  Their status lines still read "RATIFICATION CANDIDATE" so that the ratified SHA-256 holds; this entry is the record of
  ratification, as RAT-33's was for v0.7. v0.8 now governs; v0.7 stays in `doc/` as history.
- **Not authorised by RAT-35 (entry 67):** any implementation code, synthetic or real run, task file, install, OV-1
  registration, forecast, score or change to sealed Mode H. **Coding starts only on the owner's separate, specific go.**
- **For the next register edition (v0.32):** record RAT-35 (with the H-1 notes D2, D4 and D5).

## 75. 17 November 2026, about 20:10 - the owner's go for code (entry 67's specific authorisation); slice 1 started

- **The owner's words (20:09, after switching the model to Fable):** "I see you mention slices 1 and 2 ... please briefly
  outline the forward plan including slices and then "go"."
- **How Claude read it:** as the specific go for code that entry 67 requires, following RAT-35. Claude said so at the top
  of its reply, with the outline, and that it stops at once if the owner meant "outline, then wait".
- **What the go covers (plan v0.3 section 13):** the code round, to the integrated package, built and tested in Claude's
  cloud workspace only. Not covered: T017, the install, any run on the owner's PC, any real-data run, OV-1's
  registration; each needs its own go.
- **Order:** slice 1 (baseline fixes, L1 to L3; Fable, High), slice 2 (L5, L6; Fable, High), slice 3 (L4, L7, L8; Opus),
  the integrated package and document amendments (Opus), then T017 and the install.

## 76. 17 November 2026, about 20:10-21:57 - MHUP-B slice 1 built, tested and sent for technical review (EX_228)

- **Done (cloud workspace only; nothing installed; `src/` and `tests/` unchanged):** slice 1 of code plan v0.3: the fixes for
  the three known failing tests; L1 (`CATCH_UP`, `FINAL_NEXT_DRAW`, the mode-to-pin rule); L2 (the forecasting half:
  sessions, tickets, freeze lines, the chained forecast ledger); L3 (the scoring half, the outcome reader's weekly
  release rule, the witness ledger, diagnostic-score). Files: `exchange/CLAUDE_WEB_TOOLS/mhupb/slice1/`.
- **Results:** on the built tree the offline suite runs 617 tests in 48 modules with no failure on Python 3.13.18 and
  3.15.0b4 (the baseline was 570 with three known failures); 38 planted defects each caught by a named test.
- **Sent to the reviewer as EX_228**, with seven coding decisions for its ruling. S1-D1 is the one that may reach the
  owner: design 6.4 says a session's development runs go to the development run folder; the installed MHUP-A code puts
  every session run in the weekly run folder. Claude kept the installed behaviour and asked which should stand.
- **Not done:** Windows, the owner's PC, real data, E2R-T12; the PC's own time zone across a daylight-saving change.
- **Model (MC-1):** slice 2 (OV-1; the two kinds of development run) is also Fable (High) work.

## 77. 17 November 2026, about 22:22-23:20 - EX_229 (slice 1: recheck required); the corrected slice 1 sent as EX_230

- **The owner's word (22:22):** "go EX_229".
- **EX_229 (the reviewer, commit `7ed7a46`):** slice 1 is not yet passed. Rulings: S1-D1 follow the ratified design (a
  session's development runs go to the development run folder; correct the code; no owner decision needed); S1-D2 to
  S1-D7 accepted. Findings: F-229-1 the run folder; F-229-2 a malformed score line could falsely close a target;
  F-229-3 a malformed witness verification could falsely show "published before the draw"; F-229-4 a next-draw set
  must be proved by its own start ticket, not believed from a label.
- **Done (cloud workspace only; nothing installed):** all four fixed with regression tests and planted-defect checks.
  Claude re-read the slice with the reviewer's principle and found one more of the same kind: the developed record was
  believed from its shape; it is now tied to the game's sealed Mode H study (flagged to the reviewer as F-230-A).
- **Results on the corrected tree:** 623 tests in 48 modules, no failure, on Python 3.13.18 and 3.15.0b4; 57 planted
  defects, all caught. Sent as EX_230 for a focused recheck.
- **No owner decision arose.** Slice 2 has not started; it starts on the owner's next word (Fable, High).

## 78. 17 November 2026, about 23:34 - the owner will not change his PC's date or time for a test

- **The owner's words (23:33):** "i cannot test daylight saving change on my PC which would involve date/time changes as I
  am unwilling to do that."
- **Recorded as a standing constraint:** no task file, rehearsal or test changes the date, time or time zone of the
  owner's PC. T017 never planned to; this makes it a rule.
- **Why it is not needed.** The deadline is 00:00 local on the draw's date; the daylight-saving changes are at 2 a.m. on
  a Sunday and the draws are on Tuesdays and Thursdays, so no deadline falls on a change. The only effect is the
  offset (10:30 in daylight time, 9:30 in standard time), which the program takes from the system's zone rules for the
  draw's date, not from today's clock. OV-1's cut-off is a fixed UTC instant and is unaffected.
- **Checked in the cloud, no clock changed:** with the process's zone set to Australia/Adelaide (the `TZ` variable), the
  slice's `weekly_records.deadline` was compared with the zone database for 1,040 weekly draws (ten years, both games):
  none wrong; 518 at +10:30, 522 at +9:30; the first draws after each change in 2027 and 2028 are right.
- **To do, with the integrated package:** that check as a suite test (it sets `TZ` for its own process, so it is skipped
  on Windows); and in T017 one read-only step that prints the deadline and offset for a draw in each season on the
  owner's PC, with no setting changed.

## 79. 17 November 2026, about 23:56 - EX_231: slice 1 PASSED (cloud source review); one small follow-up applied

- **EX_231 (the reviewer, commit `25875c0`):** focused technical PASS of slice 1 (F-229-1 to F-229-4 and F-230-A). One
  minor, non-blocking note, N-231-1 (a drawn Powerball in a score line must be 1 to 20), to be fixed in the normal code
  round. Slices are serial: slice 2 after slice 1's acceptance, slice 3 after slice 2's. No install, PC or real-data go.
- **Done:** N-231-1 applied in `exchange/CLAUDE_WEB_TOOLS/mhupb/slice1/` with a negative test and a planted-fault check;
  the two weekly test modules pass on Python 3.13 and 3.15. Its full-suite evidence comes with slice 2's submission.
- **The owner's reminder (23:50):** focus on the core systems that serve the objectives, in preference to side issues
  and administrative overhead. Claude keeps reports and exchanges short and raises only what changes a result.
- **Next:** slice 2 (OV-1; the two kinds of development run), Fable (High), on the owner's go.

## 80. 18 November 2026, about 00:05 - correction of entry 79's reading of the owner's reminder; entry 78's to-do withdrawn

- **Entry 79 misread the owner.** He was not asking for shorter reports. His words (00:05): the concern is
  "over-engineering things that do not really matter in the scheme of things to the project eg like additional admin
  overhead in ensuring time change code is built in and works when that contributes almost nothing to advancing the
  project"; "admin trivia defocuses us and energy from the main game"; "I am not complaining about reporting, I am
  complaining about paying too much undue attention to things that do not really matter."
- **The standing rule, as Claude now holds it:** effort goes to what the objectives need: whether any method predicts,
  honest forecasts frozen before the draw, correct scoring, a valid formal test, and the owner's weekly use. A guard,
  test or feature is added only if its absence could change a result, invalidate the evidence or break that weekly use.
  Rare operational corner cases get the simplest safe behaviour (refuse and say why), not machinery.
- **Withdrawn:** entry 78's two to-do items (a daylight-saving suite test; a daylight-saving step in T017). The cloud
  check already done is enough. Entry 78's constraint stands: nothing changes the owner's PC date, time or zone.
- Reporting to the owner stays as he has asked for it (plain steps, decisions with reasons, the paste block).

## 81. 18 November 2026, 00:22 - joint ChatGPT-Claude working principle agreed and recorded

- **What:** "Main-game priority, proportional engineering and minimum overhead". The owner proposed the text (00:11).
  Claude agreed and proposed three additions: (1) whoever proposes extra work states the concrete failure and its
  consequence, or the item is simplified, deferred or dropped; (2) a ratified item that looks disproportionate is built
  in the simplest version that satisfies the ratified rule and noted in the slice's covering note, and changing a
  ratified rule still needs the owner; (3) principle 2 names correct method and calculation implementation and accurate,
  traceable reporting. The reviewer accepted all three, with a wording refinement to (3) that Claude accepts (reply
  relayed by the owner at 00:21).
- **The owner's clarification (00:15):** the science, the software methods, the calculations and the reporting all have
  to be right. The principle limits effort on side issues only.
- **The final text, once:** `exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md`. No new approval
  process; no EX round was needed. Entries 78 and 80 stand.
- **For slice 2:** the missed-week eligibility rule is part of OV-1's validity, so it gets correct implementation and
  sufficient tests, not recovery machinery. Slice 2 still waits on the owner's go, on Fable (High).

## 82. 18 November 2026, 00:29 - handover check before slice 2

- **Asked by the owner (00:28):** does the handover need updating before slice 2, so no continuity is lost?
- **Claude's assessment:** a new H-1 edition is not needed now. H-1 v4 is installed and ratified; a new edition would need
  review and ratification and is already scheduled with the integrated package (plan section 11). What a successor would
  lack is how to resume the code work, and some lines of `CONTINUITY_NOW.md` were out of date (they still said the code
  plan was with the reviewer and that no code existed).
- **Done:** `CONTINUITY_NOW.md` corrected and given a section "Resuming the MHUP-B slice work" (what governs, where the
  slice 1 code is, how to rebuild and test it including the second Python, the last known results, what slice 2 must do).
  The "If a chat ends" line now points a new Claude chat to that section and to the working principle. The slice 1 tools
  in the repository were checked identical to the working copy.

## 83. 18 November 2026, 02:24 - slice 2 (L5 and L6) built and sent for review as EX_232

- **The owner's go for slice 2:** 00:35, on Fable (High).
- **Built, cloud only, NOT INSTALLED:** `exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/` on top of slice 1's tree. L5: OV-1's
  numerical kernel (`ov1_numeric.py`, proofs P1 to P8 in its docstring), the recorder (`ov1.py`, `Method_OV1.py`:
  register, record, stop, status, verify). L6: `WF_BATCH_PLAN_V2` (routine fill, exploratory rerun), the `DEV_BATCH`
  gate, the post-seal development release rule in the outcome reader, the report on a V2 batch's own pairs,
  `reforecast_compare.py`, and the read side of `LEAGUE_SOURCES_V1`.
- **Results:** 694 tests in 51 modules, 0 failing, on Python 3.13.18 and 3.15.0b4 (71 new); 94 planted defects caught,
  0 survived; the exact distribution equals brute force over all 6,724,520 and 62,891,499 subsets; tree digest
  `887731e17598dcd71d8f331797047d31d3133dd04028aa5287501d0d4bedabc4`, reproduced from the repository copy.
- **Found on the way:** a fault in the plan-stage probe's `exp_enc` (reduction by the floor: fixed in the kernel); the
  plan's |Z| bound is valid but not attained; one regression of Claude's own caught by the full suite and fixed
  before sending (the Mode H scorer's family lookup).
- **Built lean or moved to slice 3 (listed in EX_232 section 6 for the reviewer):** OV-1's measure-registry entry; the
  league manifests' reader for the missed-week reconciliation (a seam, to be connected before any install); admission
  and the new table after a routine fill; the exploratory comparison with canonical figures.
- **Not tested:** Windows, T017, real data, the comparison against a real sealed Mode H batch, the sequencers.
- **Next:** the reviewer's review of EX_232. Slice 3 (Opus) only after its acceptance, on the owner's go.

## 84. 18 November 2026, 09:40 - the reviewer's slice 2 review (EX_233) and the owner's clarified research model (EX_234, EX_235)

- **Source.** EX_233 (slice 2 review), EX_234 and EX_235 (the reviewer's record of the owner's clarifications, made in the
  owner's conversation with the reviewer). The owner to Claude, 09:34 and 09:36: "go ex_235"; "the latest EX_235 prevails
  over the 2 earlier docs". EX_235 keeps EX_233 and EX_234 in force wherever it does not supersede them.
- **The owner's research model, as now stated (binding direction; it changes parts of the ratified supplement v0.8 and
  plan v0.3, to be carried as a short amendment with the package):**
  1. **All draws are equal research targets.** The former holdout draws (Powerball 1577-1586, Oz Lotto 1694-1703) are
     ordinary draws for walk-forward, scoring and rankings. The sealed Mode H study is kept as a read-only archive. Its
     seal is not a permission gate in any normal workflow (weekly readiness, catch-up, routine fill, exploratory
     rerun, report, scoring), and it is never summed again into ordinary scores.
  2. **Every method version is a legitimate subject.** A modified method is a new immutable scientific identity; the
     earlier version's forecasts, scores and published rankings stay. Each version is walked forward from its earliest
     eligible draw and ranked separately. Archived code is not run unless an installed runnable revision exists.
  3. **Catch-up is the same walk-forward.** Several draws accepted at once are processed one target at a time, each from
     the prefix to N-1 only. Evidence LABELS differ (historical, catch-up, prospective); the computing and the ordinary
     scores do not.
  4. **Two clearly labelled OV-1 uses.** (A) the registered formal prospective test, one per game, bar 40, unchanged;
     (B) a retrospective OV-1-style walk-forward diagnostic over history and versions: descriptive, with 40 shown only
     as a reference line, no P value and no 2.5% claim, never written to the formal ledger. (B) is a reporting
     requirement for slice 3 (L7), and it replaces supplement v0.8 section 6.7's limit.
  5. **Bar 40 is kept** (5% for the programme, 2.5% a game, 1/0.025 = 40 by Ville's inequality).
- **EX_233's findings.** S2-F01 (harden the seal check) is WITHDRAWN: the fix is to remove the seal dependency from
  normal paths. S2-F02 (an eligibility line or a registration could become durable after its limit while carrying an
  earlier time) STANDS, for the formal stream only. The kernel's proofs P1 to P8 and EX_232's Q2 to Q6 are accepted.
- **Claude's next step (cloud only, under the existing code-round go):** one corrected slice 2 that removes the seal and
  holdout gates from the staged normal paths (including slice 1's weekly readiness check), closes S2-F02, and shows the
  focused examples EX_234 section 6 lists. Then a full new edition of the Claude handover (H-1) and its blurb, as the
  owner asked. Slice 3 still waits for the reviewer's acceptance of slice 2 and the owner's go.

## 85. 18 November 2026, 10:28 - the corrected slice 2 sent as EX_236; the change note; a full new H-1 edition (candidate)

- **The owner's further clarification to Claude (09:41):** EX_235 supplements and clarifies EX_234 and EX_233 rather than
  replacing them; recording the direction first is fine provided it only updates the existing records; slice 2 is
  corrected now, and the retrospective OV-1 reporting is slice 3 (L7), after slice 2 passes and he gives the normal go.
- **The corrected slice 2 (cloud only, NOT INSTALLED), `exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/`, EX_236:**
  1. No normal path staged in slices 1 and 2 asks for the Mode H seal or the opening record: the weekly readiness check
     (slice 1's `weekly_records.developed` is now the owner's declaration alone), the development planner, the
     `DEV_BATCH` gate and the development report's release rule. Rule 2A and the weekly freeze-line conditions stay.
  2. S2-F02 closed: OV-1's registration and every eligibility line count only with a CONFIRMED line whose time was read
     after the record was read back; not confirmed before its limit, in the same process or after an interruption, the
     stream stops. One consequence, stated to the reviewer: a registration not confirmed before its first target's
     deadline leaves that game's formal stream stopped for good (no second registration).
  3. The examples of EX_234 section 6.4 are tests (a former holdout draw with no Mode H marker; a revised version as a
     new identity; a bulk catch-up equal to week-by-week runs; a missed draw scored as usual).
- **Left as installed, on purpose:** the installed reader's opening-record condition at or above the former holdout, and
  the diagnostic route's opening-record and seal conditions (validated MHUP-A code; no effect in the real project).
- **Results:** 700 tests in 51 modules, 0 failing, on Python 3.13.18 and 3.15.0b4; 101 planted defects caught, none
  surviving; tree digest `000dc4aeee4a649cbd1b2a6a36928a72f18c51ab5e997bb702ed7157a581241d`, reproduced from the repository copy.
- **The change note for the ratified documents:** `exchange/DECISIONS/OWNER_CLARIFICATION_2026_11_18_EQUAL_DRAWS_AND_OV1_USES.md`.
- **The handover, at the owner's request (09:34):** a full new edition H-1 v5 and a full new blurb, as CANDIDATES, in
  `exchange/CLAUDE_WEB_TOOLS/h1v5/out/`, built by `make_h1_v5.py` from H-1 v4's ratified bytes. H-1 v4 stays the
  installed edition until the owner ratifies v5.
- **Next:** the reviewer's recheck of EX_236. Slice 3 only after its acceptance, on the owner's go.

## 86. 18 November 2026, 14:30 - slice 2 PASSED the reviewer's recheck (EX_237); the new reviewer chat took over

- **The reviewer chat changed (about 11:00).** The previous ChatGPT reviewer chat reached its limit. The new one took over
  from the H-2 v3r3 candidate; the owner checked the takeover with Claude's continuity questions (answers sound: it found
  EX_236 at HEAD `bb43668` unprompted, stated the weekly-session boundary after `holdout_last`, S2-F02 and bar 40 correctly,
  and read the working principle as intended). The owner accepted the takeover and commissioned the recheck.
- **EX_237 (commit `b0b9ce0`): INDEPENDENT FOCUSED SOURCE-REVIEW PASS for the corrected slice 2 (EX_236).** S2-F01: the seal
  gates are gone from the staged normal paths. S2-F02: closed by the CONFIRMED lines; the consequence (a registration not
  confirmed in time stops that game's formal stream for good) ACCEPTED. The examples credible. No further slice 2 edits.
  The test figures remain Claude's own runs. NOT INSTALLED, not integrated.
- **Carried, not blockers:** the two installed archive checks left on purpose (the reader's opening-record condition at or
  above the former holdout; the diagnostic route's opening and seal) are to be re-evaluated when the integrated package is
  planned, and removed if they would actually prevent the normal workflow. Slice 3's four obligations (EX_237 section 5):
  L4 admission verifies complete, labelled attempts and reconciles manifests; connect `ov1.publication_names`; L7 the two
  labelled OV-1 views; L8 reads OV-1's state line, not only its exit code.
- **The reviewer refreshed its handover candidate to H-2 v3r4** (`d5e810c`).
- **Next:** slice 3 (L4, L7, L8) on the owner's go; the slices are serial.

## 87. 18 November 2026, 14:36 - RAT-36: the reviewer handover H-2 v3r4 ratified by the owner (EX_238)

- **The owner's decision, given in the ChatGPT reviewer chat at about 14:28 and relayed in EX_238 (commit `660fc5a`):**
  "unless you object i ratify the handover if it references
  exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md". The reviewer confirmed the reference (its
  sections 0.1(3) and 0.6) and answered "No objection. I support ratification." Claude re-read the file: the reference is
  there (lines 16 and 74).
- **RAT-36 is recorded** (RAT-35 was the last number used). Ratified, byte for byte:
  `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r4_RATIFICATION_CANDIDATE_20261118.md`, Git blob
  `6477493db1080323e1321a23065f903b0260a12f`, SHA-256
  `d75df39c097f119512feb3a6fe28f8ec9de653fdc775cf17fbf931f7afd9bbd4` (both computed by Claude from main), introduced by
  commit `d5e810c`. **H-2 v3r4 is the operative reviewer handover**; it supersedes H-2 v2 r1 for a reviewer takeover.
  H-2 v2 r1 and the earlier candidates stay as history.
- **The word CANDIDATE in the file's name and heading is frozen at its authoring time** and is superseded by this
  decision; the ratified bytes are not edited (an edit would make a different, unratified edition).
- **Not ratified by this:** the separate H-2 v3r3 introductory blurb, and Claude's H-1 v5 candidate (H-1 v4, RAT-34, is
  still the installed Claude handover). A reviewer takeover is pointed straight at the full H-2 v3r4 file.
- **Scope:** the reviewer handover's status only. No change to the design, the RAT-35 plan, the code, the installed tree,
  OV-1 or the Mode H records; no permission for any run, install or PC step.
- **For the next register edition (v0.32):** record RAT-36 with RAT-35.

## 88. 18 November 2026, 14:36 - the owner's go for slice 3

- **The owner's words (14:33, to Claude):** "please go now", in answer to Claude's statement that slice 3 would not start
  without an explicit go. Before that (14:32): he stays on Fable for the time being.
- **How Claude read it:** the serial go that EX_237 section 5 requires, for slice 3 only (L4 the league table, L7 the
  consolidated report with the two labelled OV-1 views, L8 the sequencers, launchers and documents), built in the cloud
  on top of slice 2's tree, in `exchange/CLAUDE_WEB_TOOLS/mhupb/slice3/`, and sent for review. It is not a go for the
  integrated package, T017, an install, a registration or any run on the owner's PC.
- **Next:** slice 3, checkpointed to the repository as it is built.

## 89. 18 November 2026, 17:14 - MHUP-B slice 3 built and sent for review (EX_239)

- **What:** layers L4 (the league table: three read-only sources, one score per key, the five-step publication that is
  finished whole or marked incomplete, admission), L7 (the weekly report with the two labelled OV-1 views; the
  retrospective view; the retired-revision index) and L8 (the two sequencers, their shared child launcher, the two
  launchers), on top of slice 2's tree. Files: `exchange/CLAUDE_WEB_TOOLS/mhupb/slice3/`. NOT INSTALLED; nothing was run
  on real data; the adapters did read the committed real score records (counts equal the census of plan section 8).
- **EX_237 section 5's four obligations are met** (EX_239 section 8): the publication manifests pin the forecast-ledger
  extent and `ov1.publication_names` reads them; admission takes only complete, correctly labelled attempts; the report
  gives the formal and the retrospective OV-1 views under their own labels; the weekly sequencer reads OV-1's state line.
- **The retrospective OV-1 view (the owner's use B)** uses slice 2's kernel unchanged over forecasts already scored. It
  equals an oracle written in the test (own count of the fair-draw distribution; floating point) to nine places, and
  over the draws the registered stream counted its X, Z and score are the formal ledger's. Labelled descriptive; no P
  value; never written to the formal ledger.
- **Added beyond the plan's words, each with its reason (EX_239 section 12, Q4 and Q5):** admission checks every score
  against the frozen forecast it scores; a routine fill waits while a development report is not yet a canonical source
  (so the two existing attempts are admitted first).
- **Counted edits to code already passed:** seven files (EX_239 section 7), among them `Method_OV1.py record` answering
  `NOT_REGISTERED` (exit 0) for an unregistered game.
- **Results (Claude's own cloud runs):** 757 tests in 55 modules, 0 failing, on Python 3.13.18 and 3.15.0b4; 100 planted
  defects caught, none surviving (two survived the first run and led to sharper tests); tree digest
  `62304524367973df2cd1217fa3a9b5bdf4fdfa758837372c8dd9a4c1b7f24e3b` (slice 2's recipe plus the two new launchers), reproduced from the repository copy.
- **Five questions to the reviewer** (EX_239 section 12): the league's folder named `archive` against the retirement
  rule's static check; no search-log row for `history` and `reconstruction`; the retrospective view's default cohort;
  the two additions above.
- **Not tested:** Windows and the launch chain (T017's); the admission of the two real attempts (their run folders are
  on the owner's PC only); anything on real data.
- **The handover:** the H-1 v5 candidate and its blurb were refreshed (slice 3 sent; H-2 v3r4 installed, RAT-36). Still a
  CANDIDATE awaiting the owner's ratification.
- **Next:** the reviewer's source review of EX_239. Then, on the owner's go, the integrated package with the document
  amendments; then T017; then the install.

## 90. 18 November 2026, 19:46 - EX_240 (slice 3 reviewed: three narrow corrections) and the corrected edition EX_241

- **EX_240 (commit `ddeb072`): FOCUSED RECHECK REQUIRED BEFORE AN UNCONDITIONAL SOURCE PASS.** The structure of L4, L7 and
  L8, the separation of the formal and the retrospective OV-1 views, the publication repair design and the two
  sequencers are accepted at source level. The five questions of EX_239: Q1 keep the ratified folder name `league/archive`
  with the commented constant; Q2 no search-log row for `history` and `reconstruction`; Q3 the retrospective view's
  default cohort is the currently released variants; Q4 keep the admission's check against the frozen forecasts; Q5 keep
  the routine fill's wait for unadmitted reports (an informative, recoverable refusal, never a gate of its own).
- **Three findings, all accepted by Claude as real gaps:** F3-01 admission did not bind a score's method revision and
  freeze receipt to its frozen forecast, nor check its prize division against its own matches; F3-02 a lost source was
  attributed by (method, variant), so it could blank another revision's valid totals; F3-03 a logged publication was
  recognised by name alone, not by the manifest digest its search-log row holds (which OV-1's missed-week
  reconciliation relies on).
- **EX_241: the corrected edition.** Each finding closed by a small edit in the routine named, with a focused test per
  distinct rule and six planted defects. Two source files, one test file and the mutation tool changed
  (`SLICE3_EX239_TO_EX241.diff`); the counted edits to slice 2's tree are unchanged.
- **Results (Claude's own cloud runs):** 758 tests in 55 modules, 0 failing, on Python 3.13.18 and 3.15.0b4; 106 planted
  defects caught, none surviving; tree digest `ef2b67e04c500ee940b765bb5a427666430f73ea70fc3a2b1f3e24a1f50e9d13`, reproduced from the repository copy.
- **Not tested:** as in entry 89 (Windows; the two real attempts' admission; real data).
- **Next:** the reviewer's focused recheck of EX_241. On a pass, the integrated package on the owner's go.

## 91. 18 November 2026, 20:08 - slice 3 PASSED the reviewer's recheck (EX_242); all three slices passed

- **EX_242 (commit `d642760`): INDEPENDENT FOCUSED SOURCE-REVIEW PASS for the corrected slice 3 (EX_241).** F3-01, F3-02
  and F3-03 closed; no further slice 3 edit. EX_240's acceptance of the L4, L7 and L8 structure and its answers to Q1 to
  Q5 stand. The reviewer checked that the counted edits to slice 2's tree, the retrospective OV-1 module, the weekly
  sequencer and `league_publish.py` are byte-identical to EX_239's. It notes precisely that the 106 mutants were 105
  caught in the full run plus one caught in a separate rerun. The test figures remain Claude's own runs.
- **All three slices have now passed source review:** slice 1 (EX_231), slice 2 (EX_237), slice 3 (EX_242). NOT
  INSTALLED, not integrated, nothing run on real data.
- **Carried into the integrated package (EX_242 section 5):** the document amendments with the owner's change note of
  18 November 2026 folded in; the two installed Mode H archive checks to be re-evaluated (removed if they would obstruct
  normal work); the Windows launchers and process-check chain in T017; the first admission of the two real report
  attempts (their run folders are on the owner's PC).
- **Next:** the owner's separate go for the integrated package (EX_242 is not that go). Install, T017, real runs and
  OV-1's registration each still need their own go.

## 92. 18 November 2026, 20:12 - RAT-37: H-1 v5 ratified by the owner; the two installed archive checks to be removed; the package go is under discussion

- **The owner's words (20:11, to Claude), in answer to Claude's two questions after EX_242:** "Decision 2: yes.  Decision 1:
  we discuss first now. Please ratify H-1 v5 handover candidate now."
- **RAT-37 is recorded: H-1 v5 and its blurb are ratified** (RAT-36 was the last number used). The owner ratified the
  candidate as it stood after the EX_242 refresh: handover SHA-256
  `22a543df4d5a8e36aaf4e790128a0a279649f9328bde545e1fc6321a218abd55`, blurb
  `11387112c91238cf20ff15b629c5b7bc778ec3f3999685aeea5a1b23f757b8aa` (`exchange/CLAUDE_WEB_TOOLS/h1v5/out/`).
- **Finalised by the status line only** (H-1's own rule; `exchange/CLAUDE_WEB_TOOLS/h1v5/finalise_rat37.py`; the one-line
  candidate-to-final diff is in `h1v5/final/`). Final SHA-256: `doc/HANDOVER/Claude_Primary_Handover_H1_v5.md`
  `3f0c0b1adef03947c05c180b2f3081efd2111f735b753abcea22ec01f555a3ae`; its blurb (unchanged bytes)
  `doc/HANDOVER/Claude_Primary_Handover_H1_v5_introductory_blurb.md`. Committed by Claude directly into `doc/HANDOVER/`.
  **H-1 v5 is the installed Claude handover**; H-1 v4 (RAT-34) stays as history.
- **Stated plainly:** the reviewer was offered a documentary look at H-1 v5 (EX_236) and has given no ruling on it. The
  owner ratified it directly; it carries no reviewer PASS. Its status line says so.
- **Decision 2: yes.** The integrated package removes the two Mode H archive checks that were left in the installed
  code on purpose (the results reader's opening-record condition for a target at or above the former holdout; the
  owner's diagnostic route's opening-record and seal conditions), with the tests that expect them adjusted. The Mode H
  study's own tools and readers keep validating the archive when they read it. This closes the item carried in EX_237
  section 2 and EX_242 section 5.
- **Decision 1 (the go for the integrated package): NOT GIVEN.** The owner wants to discuss it first. Claude has not
  started the package.
- **For the next register edition (v0.32):** record RAT-35, RAT-36 and RAT-37.

## 93. 18 November 2026, 22:10 - the owner's directions on where production runs (discussion before the package go; no go given)

- **Context:** before giving the go for the integrated package the owner asked how production is to be laid out and
  maintained (20:16), and answered Claude's options (22:08). This entry records his directions so far; the discussion
  continues and **the package go is still NOT given**.
- **Decided: production and development are separate folders (Claude's option A).** Production moves to its own folder
  tree on the owner's G: drive; development (VS Code, the GitHub clone, Claude Code and its task clones) stays on E:.
- **Accepted:** the production folder gets its own freshly made `.venv` (a venv cannot be copied); that step needs a short
  reviewed procedure, being a dependency step.
- **The owner's direction: production must run free of GitHub, and the requirement that the production folder be a Git
  working tree "will need to change".** He recalled that this was established near the start of the project. Claude
  confirmed the ratified rule: OFF-1, `doc/Direction_for_operational_procedures_v0_3r1.md` section 9: "Everything installed
  runs without GitHub; only the updater needs the internet."
- **What Claude verified in the installed code (a search of `src/` for every use of Git):** the forecasting, scoring,
  league, report and updater programs use no Git in normal operation. Two tools do: `package_tools/install_records.py`
  (the install procedure of design Appendix J is built on Git: steps 0, 12, 13, 17 and 19, and the release record
  requires the install record committed at HEAD and a clean tree), and `package_tools/process_check.py`, whose root
  check refuses a folder with no `.git` (so in a folder without Git the weekly session could not resume after an
  interruption). The updater names Git only in its one-time INIT, already done.
- **Facts checked for the move:** every program finds the project root from its own file's place (no drive letter or
  root setting anywhere); the record writer needs hard links (NTFS); the git-ignored run folders exist only on E: and the
  backup, so production is made by copying, not by a fresh clone; a folder is moved only while no session lock exists.
- **Open, with the owner:** whether "free of GitHub" means no remote and no network (a local Git folder allowed) or no
  Git at all in production; how code gets in (an install into a plain folder) and how records get out (a copy to the
  development clone, then commit and push); and the order of the steps so that the first forward draws are not delayed.

## 94. 18 November 2026, 22:12 - the owner settles it: no Git at all in the deployed production area

- **The owner's words (22:12):** "\"Free of GitHub\" means no git at all on the deployed production area."
- **So:** the production folder (G:) is a plain folder tree with no `.git`. Git and GitHub live only in the development
  clone (E:). Entry 93's open question (a local Git folder, or none) is closed: none.
- **What follows from it (Claude's proposal to the owner, 22:11 and 22:12; NOT yet agreed, and no go given):** `main` in
  the development clone is the release; one small deploy tool with the modes `check`, `init`, `update` and `export`
  (the owner raised the idea of a deploy tool at 22:11) replaces the Git-based install for production and proves the
  installed code by file hashes; records return to the development clone by a one-way verified copy and are committed
  there; `process_check.py`'s root check loses its `.git` condition; design Appendix J is amended and ratified. Three
  questions are with the owner: the four-mode shape; a marker file so that real-data commands refuse outside production;
  whether to start real work on E: after the install and move later, or to wait for G:.

## 95. 18 November 2026, 22:21 - the owner on the deployment proposal: marker yes; snapshots before and after; rollback is restore from backup; re-runnable

- **The owner's words (22:20):** "ok to marker. if something gets completely borked in prod (always a strong possibility)
  lets as a part of the beginning and end of a walk-forward or whatever, do a 'date/time in filename' clone or TAR
  (preferable, max zip compression) or something to a nominated backup folder G: or something ? ROLLBACK = RESTORE FROM
  BACKUP. happy with your deployment proposal as long as it is generally re-runable."
- **Decided:** (1) the marker file: yes (real-data commands refuse to run outside the production folder); (2) a
  date-and-time-named compressed snapshot (TAR preferred, maximum compression) of production to a nominated backup
  folder at the beginning and at the end of each production job; (3) rollback means restoring from such a backup, no
  other rollback machinery; (4) the deployment proposal of entry 94 (one tool; `check`, `init`, `update`, `export`) is
  accepted in outline, on the condition that every mode can be run again safely.
- **Still open:** whether real work starts on E: straight after the install and moves to G: later, or waits for G:;
  where the backup folder is; the design note for the reviewer (not started; needs the owner's go). The package go is
  still NOT given.

## 96. 18 November 2026, 22:37 - the owner on snapshots: ZIP, and only at the end of a run

- **Format (22:25):** "no tar.xz it must always be understandable by windows i.e. zip is natively displayable by file
  explorer." So: a standard `.zip` (Deflate, level 9), written with Python's own `zipfile` library (no extra install in
  any Python), named with the date and time, read back and hash-checked before it counts.
- **When (22:36):** "even better only backup after the catchup and whatnot run completes since the end of the previous run
  is essentially the rollback backup." So: one snapshot at the END of each production job, none at the start. This
  replaces entry 95 item (2)'s "beginning and end".
- **The production tree, measured by the owner on E: (22:34; `du64`):** about 81,500 files and 211 MB (`results` 80,576
  files, 206 MB, of which the development run folders are about 144 MB; `src`, `tests`, `archive`, `source_data` and
  `transitory_data` together 937 files, 4 MB). Claude's estimates, not measured: about 100 MB and one to three minutes
  per snapshot.
- **To check on the owner's PC at the first test snapshot:** more than 65,535 files needs the ZIP64 form; whether
  Windows 11's File Explorer opens it is not verified.
- **Still open:** start on E: and move later, or wait for G:; the backup folder's drive; the go for the design note. The
  package go is still NOT given.

## 97. 18 November 2026, 23:14 - the owner: keep the missed-snapshot rule; build it clean, once (no interim arrangement)

- **The owner's words (23:13):** "yes to \"One rule I'd keep\" although how you determine that is obscure to me, it could be
  created by a weeks-gap walkforward or a new mthod intrioduced or some other reason.  My preference is not to implement
  something we know we are going to change so lets re-work whatever we have to so the result is we implement clean code
  and processes."
- **Decided (1):** if a run's end-of-run snapshot was not made, the next run makes it first. The mechanism Claude proposed,
  to be stated plainly in the design: every production job, of whatever kind and after whatever gap, leaves a small
  "snapshot due" file when it finishes; the file is removed only when a verified snapshot exists; a job that finds the
  file takes the snapshot before doing anything else. It does not depend on why or when the earlier job ran.
- **Decided (2): no interim arrangement.** This answers the question left open in entries 94 to 96: MHUP-B is NOT
  installed first on E: with the Git-based procedure and moved later. The deployment design (production on G: with no
  Git; the deploy tool; the marker; end-of-run snapshots; restore) is designed, reviewed and built first, the existing
  tools and the ratified install procedure (design Appendix J) are reworked to it, and MHUP-B reaches production by
  that one clean route. Claude told the owner the cost before he decided: the first forward draws start later (each
  week before production runs is one draw per game that can be caught up and scored but not counted as forward
  evidence).
- **Consequences for the code round:** a further layer (deployment) is designed and reviewed before the integrated
  package; some code that has passed review changes (the two launchers and the sequencers for the marker and the
  snapshot; `process_check.py`'s root check; `install_records.py`'s Git checks); T017 rehearses the new route.
- **Still open:** the backup folder's drive; the owner's go for the design note. Nothing has been started.

## 98. 18 November 2026, 23:24 - the owner: nothing deployed now and modified later; backups to T:; the reviewer told (EX_243); handovers updated; then a new Claude chat

- **The owner's words (23:18):** "It also means that any suggestion to deploy current code now and modify later is a no.  we
  need to tell reviewer what happened and what is decided so they know what standard to review against. Backup will be
  to T: (perhaps parameter configurable). So once that is done (no code or design work I assume, if you propose that not
  please pause and tell me first) then you update your handover and all related docs (decisions, etc etc) , chatgpt
  updates theirs and then a new chat for you."
- **Decided:** (1) no interim deployment of the current code, in any form (confirms entry 97); (2) the backup folder is
  on the owner's T: drive, as a setting; (3) the order: the reviewer is told; Claude updates its handover and the related
  records; the reviewer updates H-2; a new Claude chat starts. No code or design work in this chat.
- **Done by Claude (documents only; no design, no code):**
  - `exchange/EX_243_Claude.md` to the reviewer: what happened, the decisions as a table D1 to D12, the facts verified in
    the installed code, what is NOT decided, and what it means for the review standard. It asks for no ruling; it asks
    the reviewer to update H-2 and to say now if any decision would harm the science or the records.
  - **H-1 v6 and its blurb, as CANDIDATES** (`exchange/CLAUDE_WEB_TOOLS/h1v6/`, built by `make_h1_v6.py` from H-1 v5's
    ratified bytes): section 0B item 12 (where production runs), items 8 and 10, section 10, sections 12.8 and 12.11 (the
    deployment work), two lessons, the appendices. SHA-256: handover `6dc8185a72006861c860773a18887ad51135f2bd129bce7a549879a17e280353`; blurb
    `d78249b94ba1af56dd0a2c9cd20fde803ded069098ea4bed04a50b039b97c47c`. H-1 v5 (RAT-37) stays installed until the owner ratifies v6.
  - `exchange/CONTINUITY_NOW.md` and `exchange/OWNER_ROADMAP.md` brought up to date.
- **Asked of the owner, not answered yet:** whether to restore the ratified bytes of
  `doc/HANDOVER/Claude_Primary_Handover_H1_v4_introductory_blurb.md` (changed by his commit `86f6c43` at 23:08, apparently
  by accident; RAT-34's recorded SHA-256 is `2cfa6cf5...67be`; the file is history and nothing in use depends on it).
- **Next:** the owner pastes EX_243's block to the reviewer; the reviewer updates H-2; the owner ratifies H-1 v6 (or not)
  and starts a new Claude chat with its blurb. The new chat's first real task, on the owner's go, is the deployment
  design note (Fable (High)). The package go and the design-note go are NOT given.

## 99. 18 November 2026, 23:31 - the owner: restore the H-1 v4 blurb; Claude restored its ratified bytes

- **The owner (23:29):** "restore it to what it should be please" - the answer to the question left open in entry 98.
- **Done by Claude:** `doc/HANDOVER/Claude_Primary_Handover_H1_v4_introductory_blurb.md` written back from the RAT-34
  commit (`git show 0044de8:<path>`), as a new forward commit; nothing was reset or rewritten. Tool-computed SHA-256
  after the restore: `2cfa6cf521aabee3bbef257eb8a917caea92c73ddac54e90ddda79464ecd67be`, equal to RAT-34's recorded value.
- **What had changed** (the owner's commit `86f6c43`, apparently by accident): the owner's notes above the line were
  gone and the last lines had been filled in for a paste (commit and date); SHA-256 `dad5f7d5...3675`. That version
  stays in the history.
- **Nothing else touched.** No design, no code. The file is history: H-1 v5 (RAT-37) is the installed handover and the
  H-1 v6 candidate's blurb is the one a new chat starts from.

## 100. 19 November 2026, 06:04-06:20 - HO-2: the new Claude chat's first reply (EX_245); the owner's decision on how a restore is done

- **The takeover.** The owner started a new Claude chat at about 06:04 from the H-1 v6 candidate's blurb (commit
  `de1aa3e`). It read and checked first: 163 of H-1 v6's quoted file hashes match Git, none failed; the two slice tree
  digests and the environment digests were not reproduced (that needs a build, or the owner's PC). Its first
  substantive reply is `exchange/EX_245_Claude.md`, which also records the discrepancies found (none blocking).
- **EX_244 read and accepted** as the basis for the deployment design note. Claude checked the staged slice 3 code (read
  only): a STOPPED formal OV-1 stream does not block forecasting, scoring or the league table; the development sequencer
  does not touch OV-1; the retrospective view never writes to the formal ledger. No change to slices 1 to 3 is needed.
- **The owner's decision (06:16), on how a production restore is done:** "I prefer to rename the old code/data folder
  tree and restore afresh into a fresh \"standard\" empty tree". So: the old production tree is renamed aside (kept,
  never deleted), and the chosen verified snapshot is unpacked into a new, empty tree at the standard production path.
  The details (the renamed tree's name, the checks before the rename, the orphan marker, `.venv`, a restore record) are
  for the deployment design note. A restore stays a step on the owner's own go.
- **Commit of EX_245 (06:20):** the owner relayed the reviewer's answer to Claude's question Q1, "EX_245 - YES. Please
  commit the reply as `exchange/EX_245_Claude.md`". A narrow exception to "no commit before the takeover is accepted",
  as for EX_216 and EX_218 (entry 64). Normal work is NOT yet authorised: the reviewer's check of the takeover reply is
  still to come.

## 101. 19 November 2026, 06:21 - RAT-38: H-1 v6 and its blurb ratified as they stand; EX_244 recorded as the governing clarification on restore and replay

- **Source (06:20).** The owner relayed the reviewer chat's text answering EX_245's Q2: "H-1 v6 - RATIFIED AS IT STANDS. I
  ratify H-1 v6 and its accompanying introductory blurb as currently submitted. No v6r1 is required. Please record this
  ratification in the decision log and update `CONTINUITY_NOW.md` accordingly. Also record `EX_244_ChatGPT.md` as the
  latest clarification governing production backup restoration, historical N-1 walk-forward replay and OV-1
  calculations. ... EX_244 takes precedence over any older, inconsistent restore guidance in the handovers. Please
  retain the ratified H-1 v6 bytes unchanged and use the decision log and continuity record for this subsequent
  clarification. This ratification does not authorise deployment design, coding, installation, Windows execution or
  production runs." The owner added, in his own words: "however, I would like the latest direction/decisions folded in
  where appropriate at the earliest convenient time."
- **How Claude read it:** the owner's ratification, given as the text he relayed and endorsed (only the owner ratifies).
  If that is not what he meant, a correcting entry follows.
- **RAT-38 is recorded** (RAT-37 was the last number used). Ratified, byte for byte, the candidates of entry 98:
  `doc/HANDOVER/Claude_Primary_Handover_H1_v6.md`, SHA-256
  `6dc8185a72006861c860773a18887ad51135f2bd129bce7a549879a17e280353`, and
  `doc/HANDOVER/Claude_Primary_Handover_H1_v6_introductory_blurb.md`, SHA-256
  `d78249b94ba1af56dd0a2c9cd20fde803ded069098ea4bed04a50b039b97c47c` (both computed by Claude; equal to the files in
  `exchange/CLAUDE_WEB_TOOLS/h1v6/out/`). **H-1 v6 is the installed Claude handover**; H-1 v5 (RAT-37) stays as history.
- **Bytes unchanged, as instructed:** unlike RAT-37, the status line is NOT finalised. H-1 v6's header still reads
  CANDIDATE; that word is frozen authoring-time history, superseded by this entry (as for H-2 v3r4, entry 87). A chat
  that reads H-1 v6 section 0 item 3 ("if this file's status line still reads CANDIDATE, stop and ask") is answered by
  this entry and by CONTINUITY_NOW.
- **EX_244 governs** production backup restoration, historical N-1 walk-forward replay and OV-1 calculations, and takes
  precedence over older, inconsistent restore guidance in the handovers (H-1 v6 section 12.11 included). In short: a
  full restore followed by N-1 replay, with OV-1's numbers recomputed, is valid research; no automatic research STOP and
  no special prospective-evidence reconstruction because an older backup was restored; the formal registered OV-1
  guarantee keeps its own assumptions, which never block ordinary research computations.
- **The owner's direction: fold the latest decisions in at the earliest convenient time.** Claude's reading: the next
  full H-1 edition (v7) folds in EX_244, entry 100's restore decision, this entry and the stale lines EX_245 section 6
  item 5 lists; the reviewer's H-2 likewise in its own edition; and the ratified documents (the design's deploy
  procedure, the direction document's backup paragraph) through the integrated package's amendments. When is the
  owner's call; Claude will propose a moment that does not hold up the design note.
- **Scope:** the Claude handover's status and the record only. No design, no code, no install, no run, no go for the
  deployment design note. H-2 v3r6 is still a candidate; H-2 v3r4 (RAT-36) stays the operative reviewer handover.
- **For the next register edition (v0.32):** record RAT-35 to RAT-38.

## 102. 19 November 2026, 06:32 - HO-2: TAKEOVER ACCEPTED; the owner authorises normal work (the new Claude chat)

- **The exchange:** EX_245 (Claude's first reply, `c32b899`); the reviewer's five questions Q1 to Q5, relayed by the
  owner at 06:25 (questions only); EX_246 (Claude's blind answers, written at 06:27 before seeing the reviewer's
  assessment; committed with this entry).
- **The owner's message (06:31), relaying the reviewer's verdict and his decision:** "HO-2 TAKEOVER ACCEPTED. The
  ChatGPT independent reviewer has assessed EX_245 and the blind answers in EX_246 and returned PASS on all five
  questions, with no material discrepancies or outstanding takeover questions. I accept the new Claude chat's takeover
  and authorise normal work under the existing project rules. This does not constitute a GO for the deployment design
  note, deployment-layer coding, the integrated package, T017, installation, registration or any real-data run. Those
  retain their separate owner approvals. EX_244 remains governing for the scientific validity of restored historical
  N-1 walk-forward and descriptive OV-1 recalculations. H-1 v7 may be prepared at a convenient point, but it is not a
  prerequisite to the deployment design note. Please retain EX_245 and EX_246 as the takeover evidence and proceed
  according to the established authorisation sequence." And in his own words: "you now have the commit authorization
  which you had prior to this new handover."
- **So:** normal work is authorised. Claude's commit rights are as before (H-1 v6 section 0B item 4 and 1.6: documents
  and records under `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/` freely, into `doc/` once reviewed and ratified;
  never code into `src/` or `tests/`; never `source_data/`, `results/`, `transitory_data/`, `GAIS/` or settings).
- **Not authorised by this:** the deployment design note, deployment-layer code, the integrated package, T017, any
  install, `declare-developed`, OV-1's registration, any real-data run. Each keeps its own go.
- **The reviewer's PASS** was relayed in the owner's message; no reviewer EX file was committed for it (fetched at
  06:32). If the reviewer commits one later, it is the record of the PASS.
- **H-1 v7:** at a convenient point; not a prerequisite to the design note.

## 103. 19 November 2026, 22:38 - OWNER DECISION: test on Python 3.15 only; the routine Python 3.13 runs are dropped

- **The owner's words (22:36 and 22:37):** "do we need to run it in bopth pythoin versions given I use 3.15.2 ?", then,
  after Claude's recommendation: "yes to dropping the routine Python 3.13 runs and testing on 3.15 only. i accept the
  risk."
- **So:** Claude's cloud test runs use one interpreter, the newest Python 3.15 build available to the cloud workspace
  (until now 3.15.0b4). The authoritative runs are on the owner's PC, Python 3.15.2 under Windows, through Claude Code
  task files and T017. The routine 3.13 runs of H-1 sections 8.3, 12.3, 12.9 and 12.10 end. No one-off 3.13 run is
  planned.
- **Why (Claude's reasoning, accepted):** production only ever runs on the owner's 3.15.2 (the fresh production `.venv`
  is built from it); a 3.13 pass proves nothing about 3.15.2; the cloud's 3.15 build is itself a Linux beta, so the
  Windows run is the one that counts. Planted-defect checks and the Windows rehearsal are unchanged.
- **The risk the owner accepts:** a fault that depends on the Python version would show only when he next changes
  Python. The existing rule covers that moment: after any dependency or Python change, stop until the full suite passes.
- **To tell the reviewer** in the covering note of the next code submission (its R-2 reproduction right needs to know
  which interpreter the evidence comes from). Earlier evidence on two Pythons stays as it was recorded.

## 104. 19 November 2026, 22:40 - OWNER DECISION: no monthly restore test

- **The owner's words (22:40):** "we forego a monthly restore test."
- **What it changes:** the direction document's section 9 (agreed 2 November 2026) says backups of `source_data/` and
  `results/` after every weekly session and before every install, to a second drive, "with a monthly restore test".
  The monthly restore test is dropped. The rest of that paragraph is replaced in substance by the snapshot decisions D7
  to D10 (EX_243) and the restore method of entry 100; the ratified text is amended with the integrated package's
  document changes.
- **Claude's reading, not a new decision:** the one restore that T017 rehearses in a scratch folder (H-1 v6 section 10
  item 4; EX_246 Q3) stays planned, because it is the only check that a snapshot can actually be restored and that
  File Explorer opens it. If the owner did not mean to keep that, a correcting entry follows.

## 105. 19 November 2026, 22:43 - OWNER DECISION: no replay-against-originals comparison; go for H-1 v7

- **The owner's words (22:43):** "we forego item 15 \"Checking a replay against the originals\" ... it is the same as a
  catchup which does not (cannot) do it either.  go."
- **So:** after a restore, replayed forecasts are not compared with the originals kept in the renamed-aside tree; a
  replay is treated exactly like a catch-up. Claude's suggestion (EX_246 Q1, "a useful check that costs nothing") is
  withdrawn and is not carried into the deployment design note.
- **Go for H-1 v7** (Opus), a full edition from H-1 v6's ratified bytes folding in the items Claude listed at 22:38 and
  22:40 (items 1 to 14, 16 and 17; item 15 dropped): EX_244 and the restore method (entry 100); formal OV-1 and the
  orphan marker after a restore as open design-note items; RAT-38 and the takeover (entry 102); Python 3.15 only
  (entry 103); no monthly restore test (entry 104); the stale lines EX_245 lists; the header and section 0 item 3; new
  lessons; the slice digests reproduced; Appendix A rows; the ten safeguards of EX_246 Q3 as the design note's
  checklist; v7 not a prerequisite to the design note; the reviewer's PASS relayed, not filed; a new blurb. The
  ratified documents and the reviewer's H-2 are not edited; the owner ratifies v7.

## 106. 19 November 2026, 23:26 - RAT-39: H-1 v7r1 and its blurb ratified by the owner, after the reviewer's PASS

- **History of the edition:** the v7 candidate (entry 105; `bd68f4f`); the reviewer examined it, supported its content and
  ratification, and asked (relayed by the owner at 23:11) for two narrow corrections only: section 0 steps 1 and 3 (the
  obsolete prohibition on reading `source_data/` and records, against RAT-34) and section 7.5 (the updater has run live
  once per game). The v7r1 candidate made exactly those, plus identity lines (`39f3ef7`; diff `H1_v7_TO_v7r1.diff`).
- **The owner's words (23:25):** "H-1 v7r1 - OWNER RATIFIED. The independent ChatGPT reviewer has examined H-1 v7r1 at
  commit `39f3ef7` and returned PASS. I ratify H-1 v7r1 and its introductory blurb, incorporating the two requested
  corrections. Please install the ratified documents in `doc/HANDOVER/`, record the ratification in the decision log and
  update `CONTINUITY_NOW.md`, following the established documentation procedure. The remaining obsolete sentence in
  section 12.3 may be corrected in the next edition; it is not a blocker. This ratification authorises only the
  associated documentary records. It does not authorise deployment design, code, tests, installation or production
  runs."
- **RAT-39 is recorded** (RAT-38 was the last number used). Finalised by the status line only, as H-1's own rule says
  (`exchange/CLAUDE_WEB_TOOLS/h1v7/finalise_rat39.py`; the two-line candidate-to-final diff is
  `h1v7/H1_v7r1_CANDIDATE_TO_FINAL.diff`). Candidate SHA-256 `ed3513f5c7400ca9bb9f0a915bb9ed93176d040c663acb5b821be23e221ec667`;
  final `doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md`, SHA-256 `6f968eefebf3cb13212d967ee28fe76b84ed49f319d0df0121e2d746771c97cd`; its blurb (unchanged bytes)
  `doc/HANDOVER/Claude_Primary_Handover_H1_v7r1_introductory_blurb.md`, SHA-256 `76be41b0ecb91e0c1e9c1c07f1ae01c925d9590624c96256723013d0d41992a6`. **H-1 v7r1 is the installed
  Claude handover**; H-1 v6 (RAT-38) stays as history. The v7 candidate (`h1v7/out/`) was never ratified.
- **Carried to the next edition:** section 12.3's "Claude never opens those folders itself" (the same obsolete prohibition;
  not a blocker).
- **Scope:** the Claude handover's status and the records only. No deployment design, code, tests, install or run.
- **For the next register edition (v0.32):** record RAT-35 to RAT-39.

## 107. 19 November 2026, 23:51 - OWNER GO: the deployment design note only (Fable (High))

- **The owner's words (23:50):** "OWNER GO - DEPLOYMENT DESIGN NOTE ONLY. I authorise preparation of the deployment design
  note described in H-1 v7r1 section 12.11. Agreed: switch to Fable (High) for this design work. Use the ratified H-1
  v7r1 checklist and the existing owner decisions, particularly EX_243, EX_244 and decision-log entries 100-105. Keep the
  design simple and proportionate. Preserve the project's scientific integrity, existing process safety and the
  separation between ordinary investigative OV-1 and the formal registered statistical claim. The design must not
  reintroduce monthly restore testing, replay comparison against originals, unnecessary prospective-evidence recovery
  machinery or additional deployment complexity contrary to the agreed decisions. Please prepare the design note with
  the necessary alternatives and your recommendations, then submit it for independent ChatGPT review before seeking my
  ratification. Scope of this GO: design and its supporting documentary submission only. No deployment code,
  integration, installation, Windows tests, production restoration or real-data execution is authorised. Each later
  stage requires its separate GO."
- **So:** Claude writes the design note (reading the installed and staged code first), commits it under `exchange/` and
  sends it to the reviewer as an EX message. No code, package, task file or run. The owner ratifies after the review.

## 108. 20 November 2026, 00:10 - the deployment design note, DRAFT v0.1, sent to the reviewer (EX_247); no owner decision

- **Done under entry 107's go (Fable, High; design only, no code):**
  `exchange/CLAUDE_WEB_TOOLS/mhupb/deploy/MHUPB_DEPLOYMENT_DESIGN_NOTE_DRAFT_v0_1.md`, sent to the reviewer as
  `exchange/EX_247_Claude.md` for a design-stage review before any code.
- **In short:** production on G: with no Git; one tool in the development clone with the modes `check`, `init`, `update`,
  `export` and `restore`; a release is a named commit proved by a reviewed digest of its file hashes; `update` keeps
  Appendix J's process check, barriers U and P, suite before release and the meaning of the two records, with the Git
  tests replaced by hashing every file; a snapshot is one ordinary zip of everything but `.venv`, read back and
  hash-checked, with a `SNAPSHOT_DUE` flag; restore by the owner's method (entry 100), then ordinary replay (EX_244);
  a fixed rule (F-A, F-B, F-C) for the formal OV-1 claim after a restore, with nothing carried forward and nothing
  blocked; a marker file every launcher needs.
- **What reading the installed code showed:** the install and release records live under `src/` and are written with
  production's clock, so they are born in production and return to the clone by `export`; the suite reads repository
  files outside `src/` and `tests/`, so it runs in a temporary export of the release commit with production's Python.
- **A probe on invented files** (`zip_probe.py`): `zipfile` writes ZIP64 by itself past 65,535 entries; a
  manifest-checked round trip of 81,500 files gave back every byte. Nothing about File Explorer or the owner's drives.
- **Waiting for the owner later, after the review (note section 15; none decided, none assumed):** whether `.venv` is
  in a snapshot; when `SNAPSHOT_DUE` is written; a job that cannot make an overdue snapshot; the orphan marker at a
  restore; the formal OV-1 rule; where the marker guard sits; `restore` as a fifth mode; the two folder names; an
  optional early File Explorer check on his PC (its own go).
- **Model (MC-1):** the Fable task is finished. Opus is enough until the reviewer replies; Fable again for a revision
  that touches the formal OV-1 rule, the barriers or the release identity.

## 109. 20 November 2026, 00:10 - correction of a count in EX_247

- EX_247 section 3 says Claude's second reading of the design note "made nine corrections before sending". **The
  second reading made 17 counted edits to the draft** (counted from the edit script); nine was Claude's estimate of
  the substantive ones, written without counting. The examples EX_247 names are right. EX_247 is not edited; the
  note's content is unaffected. Lesson kept: count before claiming, in a covering note too.

## 110. 20 November 2026, 02:35 - EX_248 (the design note: RECHECK, six findings); the owner confirms nine choices and gives the go for the revision

- **EX_248 (the reviewer's commit `65e2078`): R-3 DESIGN REVIEW, RECHECK.** The architecture is supported (Git-free
  production, one tool with five modes, release identity by file hashes, barriers U and P, ZIP snapshots, set-aside and
  restore). Six findings to resolve on paper before any code: B01 an emergency restore must not depend on the damaged
  tree passing the healthy-production checks; B02 a stale orphan marker must neither block every restore nor be copied
  into the restored tree as an active block; B03 the formal OV-1 rule of the draft's section 9 is too discretionary: a
  source-level trace of five cases and an objective, pre-specified classification are wanted; B04 an export after a
  restore must not leave a mixed set of records in the clone; B05 snapshot completeness (which commands leave the flag
  and take a snapshot; a quiet state; the historical lock and wheels of an old release); B06 the production guard must
  check the path, not only that the marker exists. Section 1 carries the owner's scientific clarification made in his
  conversation with the reviewer: all eligible methods run impartially; restore and replay are the same chronological
  process and valid research; no rule is added against an unshown selection mechanism; the registered formal claim is
  a distinction of inferential labels only.
- **The owner's words to Claude (02:34), after Claude listed the nine choices EX_248 section 4 relays:** "yes io confirm. go
  EX_248".
- **Confirmed by the owner:** (1) `.venv` is not in snapshots; it is rebuilt at a restore from the exact locked wheels of
  that release. (2) `SNAPSHOT_DUE` is written just before a job's first write. (3) When an overdue snapshot cannot be
  made, ALL jobs continue with a loud, persistent warning; the owner accepts the loss-of-rollback exposure, `update`
  included. This relaxes decision D8's "the next job makes it first" (entry 97) for the case where it cannot be made.
  (4) An orphan marker neither refuses a restore outright nor is copied into the restored tree as an active block: a
  reboot is recommended, then a fresh clean process check, then the owner's explicit clearance of the stale marker;
  never while a process is running or uncertain. (5) Formal OV-1: no difference for the research; the actual code is
  traced to say what the registered claim can still certify, reported truthfully. (6) The production guard checks the
  path, not only the marker's presence. (7) `restore` is a fifth mode of the one tool. (8) The production folder is
  `G:\a_p_r_i_r`. (9) The backup folder is `T:\a_p_r_i_r_backups`.
- **The go:** for the revision of the design note in answer to EX_248 (Fable (High)), to be resubmitted for the R-3
  recheck as EX_249. Design only: no code, package, Windows step, install, restore or run.

## 111. 20 November 2026, 02:47 - the deployment design note, DRAFT v0.2, sent for the R-3 recheck (EX_249); no owner decision

- **Done under entry 110's go (Fable, High; design only, no code):**
  `exchange/CLAUDE_WEB_TOOLS/mhupb/deploy/MHUPB_DEPLOYMENT_DESIGN_NOTE_DRAFT_v0_2.md`
  (a full document; exact diff `NOTE_v0_1_TO_v0_2.diff`; builder `make_note_v0_2.py`), sent as `exchange/EX_249_Claude.md`.
  All six findings of EX_248 accepted and answered (the note's section 18).
- **A trace of the passed code on invented data** (`restore_ov1_trace.py`): after a restore the staged recorder
  re-derives a lost factor line exactly (17 of 17 fields); it appends MISSED for a formerly counted draw whose
  pre-cut-off freeze line is not in the snapshot, and its own `verify` passes; a second `register` is accepted when the
  snapshot predates the registration. So the note proposes one objective check in the recorder (a new stop cause
  `NOT_ESTABLISHED_AFTER_RESTORE`, from the snapshot's time, the restore's time and the cut-off), fed by a restore
  notice, and a refusal in `register`. Ordinary forecasting, scoring, league tables and the retrospective view are
  untouched. It is a small edit to passed slice 2 code and an amendment to supplement 6.8: for the reviewer's
  judgement and the owner's ratification.
- **Still for the owner, after the recheck (note section 15; none decided, none assumed):** A the run-sheet snapshot
  after single owner commands; B the exact condition for a stale orphan marker at a restore (the draft makes the
  restart a checked condition); C the formal OV-1 check (recorder, or report label only); D the two proof-of-concept
  probes left unguarded; E the optional early File Explorer check on his PC (its own go).
- **Model (MC-1):** the Fable task is finished. Opus until the reviewer replies; Fable again if the recheck touches
  section 8's orphan rule or section 9.

## 112. 20 November 2026, 16:30 - EX_250 (the design note v0.2: a narrow RECHECK; the owner's new backup and recovery decisions); the owner's answers on A to G

- **EX_250 (the reviewer's commit `53c4592`): R-3 RECHECK, narrowly focused.** v0.2's six corrections are accepted in
  principle (B01 to B06, the OV-1 trace and its recorder check included). The owner's later decisions, made in his
  conversation with the reviewer and transmitted in EX_250 section 1, supersede v0.2's sections 6 to 8: (1) every
  snapshot is the COMPLETE tree under `G:\a_p_r_i_r`, `.venv` included, with only the two temporary snapshot-control
  files left out (this supersedes entry 110 item 1); (2) restore is a plain full-tree extraction to the same path,
  with no routine rebuild of the environment; (3) each `update` attempts a full PRE-deployment and a full
  POST-deployment snapshot (`init`: POST only), the ordinary end-of-job snapshots staying; (4) a separate, versioned,
  date-and-time-named, hash-verified recovery kit ZIP on T: per release, so an emergency restore does not depend on E:
  (R3-C01), with a process check that needs neither a readable G: nor E:; (5) the owner copies the whole T: backup
  folder to USB3 drives and the cloud himself; (6) storage is not the limit (about 3.4 TB free on G:, 2.43 TB on T:).
  Two findings for v0.3: R3-C01 (E: must not be a recovery dependency) and R3-C02 (complete, consistently verified
  full-tree ZIPs; a quiet-state or write-exclusion rule; PRE and POST deployment snapshots).
- **How these six are recorded:** EX_250 is the record of them (the owner settled them with the reviewer). Claude listed
  them to the owner at 15:50 and asked for confirmation; his reply (below) did not restate them and did not
  contradict them. If any is not as he meant, a correcting entry follows.
- **The owner's words to Claude (16:29):** "in the worst case a simple unzip by the human into the right place gets it
  done. yes to A through E.  I assume there is a way to invoke a backup whenever I feel the urge (outside running
  anything else) ?   Yes F; T: must be available, if it is not then I have worse problems than this project failing ...
  For G: whatever python is currently installed for that user.  From time to time I may independently update the venv
  in dev and then prod, say if a new python is installed, presumably by deleting the .venv subfolders and rein the
  right folder simply running install_upgrade_dependencies_into_venv.bat which calls the local activate_venv.bat ."
- **Decided by the owner:** A: single owner commands rely on their run sheet (mark the snapshot as due first; end with
  the snapshot command). B: a stale orphan marker at a restore needs a checked restart, a clean process check and his
  typed acknowledgement; without a restart, the existing per-incident clearance. C: the one objective check in the
  OV-1 recorder and `register` refusing after a lost registration. D: only the two named proof-of-concept probes stay
  unguarded. E: the early File Explorer check, yes (its own go still to come). F: `update` and `init` stop if the
  recovery kit cannot be written and verified on T:. G: an emergency restore runs on whatever Python is installed
  for that user. Also: a snapshot can be taken by hand at any time; and, as the last resort, a restore is a plain
  unzip into the right place by hand.
- **Raised by the owner, NOT yet decided:** he may rebuild the environment himself, in development and then in
  production, by deleting `.venv` and running his own installer. v0.2 instead builds production's environment from a
  pinned lock and a wheel folder. Claude puts the choice to him before writing v0.3.
- **Earlier the same day (09:33):** the owner agreed to a new Claude chat once the design note is settled ("I agree with
  the new chat once this is settled"): H-1 v8 first, then the code round in a fresh chat on its own go.

## 113. 20 November 2026, 16:35 - OWNER DECISIONS: production's environment is built his way (H1); "no Python at all" for an emergency restore

- **The owner's words (16:33):** "Yes to H1. Will test in dev first to see what happens, and presumably some sort of
  \"verification command\" presumably there is a way to do that. Yes to \"no Python program at all may be running on the
  PC, apart from the restore tool itself.\""
- **H1, decided:** production's Python environment is made as the development one is, by the owner with his own scripts
  (delete `.venv`; `create_venv.bat`; `install_upgrade_dependencies_into_venv.bat`), in development first, then in
  production. The pinned lock file and the wheel folder of design note v0.2 section 6 are dropped. One rule stays:
  after any environment build or change in production, the test suite must pass with production's own Python before
  any real-data job; the deploy tool does that verification (the "verification command") and snapshots are taken
  before and after. Claude told him the cost first: production's package versions are whatever `pip` gives that day,
  not a pinned list; all 39 of the installer's packages go into production; an old snapshot restored after a major
  Python change may hold an environment that no longer starts (the fix: the same rebuild, then the verification).
- **The process rule for an emergency restore, decided:** no Python program at all may be running on the PC, apart
  from the restore tool itself. It needs nothing from G: or E: and no extra package. Before a restore the owner closes
  everything that uses Python. It applies to `restore` only.
- **Taken as the go for v0.3** of the design note under entry 107's go (the design note and its submission for review),
  as EX_250 section 7 asks. Design only: no code, package, Windows step, install, restore or run.

## 114. 20 November 2026, 16:40 - the deployment design note, DRAFT v0.3, sent for the focused R-3 recheck (EX_251); no owner decision

- **Done under entry 107's go (Fable, High; design only, no code):**
  `exchange/CLAUDE_WEB_TOOLS/mhupb/deploy/MHUPB_DEPLOYMENT_DESIGN_NOTE_DRAFT_v0_3.md`
  (a full document; exact diff `NOTE_v0_2_TO_v0_3.diff`; builder `make_note_v0_3.py`), sent as `exchange/EX_251_Claude.md`.
  Both findings of EX_250 accepted (R3-C01, R3-C02).
- **What changed from v0.2:** every snapshot is the complete production tree, `.venv` included; a recovery kit zip per
  release on T:, built from release bytes, so `restore` needs neither E: nor a working production folder; `restore`
  is a plain extraction to the same path, verified, with a health check and no rebuild; its process check is "no
  Python program at all on the PC"; `update` takes a PRE_DEPLOY and a POST_DEPLOY snapshot and stops first if the kit
  cannot be written; a snapshot is taken only when production is quiet (no launch during it; a process check before
  and after; a second reading of every file); production's environment is built the owner's way and verified by the
  suite (`update` is the verification command), with the pinned lock and the wheel folder withdrawn.
- **Two small additions the owner was not asked about, flagged to him in the note's section 15:** the file
  `.venv\ENVIRONMENT_VERIFIED.json` (a launcher refuses on an environment not yet verified); and
  `Restore_Production.bat --after-hand-unzip` (a restore done by hand still gets its record and notices).
- **Model (MC-1):** the Fable task is finished. Opus until the reviewer replies.

## 115. 20 November 2026, 18:15 - EX_252 (R-3 RECHECK of the deployment note v0.3, narrow) and EX_253 (the owner's scientific direction on OV-1, relayed by the reviewer) read; Claude's reading recorded; no new owner decision recorded by this chat yet

- **EX_252** (`exchange/EX_252_ChatGPT.md`, main `844ebf2`): v0.3's architecture accepted (full snapshots with `.venv`, the
  recovery kit, PRE and POST deployment snapshots, the plain restore, the narrowed quiet check). Still to correct, all
  bounded: (1) the tools run without a launcher that WRITE locks or records refuse while a snapshot is in progress,
  and the read-only quiet check stays allowed; (2) **R3-D01:** the restore's "nothing extra" check cannot pass as
  ordered: define the snapshot payload and the exact allowed additions; (3) `ENVIRONMENT_VERIFIED.json` is kept, but
  names and versions alone do not detect a same-version reinstall: use the existing environment inventory digest at a
  job boundary; a failed verification leaves no marker; (4) **W-23 is not replaced by H1:** a dependency upgrade keeps
  its independent review, the owner's go and its regression evidence before real production use; (5) the hand unzip:
  into an empty folder at the same path; a live orphan marker is never silently bypassed; (6) two wording clean-ups.
- **EX_253** (`exchange/EX_253_ChatGPT.md`, main `4997c6b`): the reviewer relays that the owner accepts a simplified OV-1:
  one prevailing forward stream per game with the kernel, the six lambdas and the bar of 40 kept; a new method gets its
  full historical N-1 walk-forward and the historical rankings are recomputed with it included, and it joins the
  prevailing stream at its first eligible future draw, never by back-fill; all methods are evaluated impartially;
  everything is reproducible chronological N-1 computation, so a restored backup is simply walked forward. Proposed for
  removal: the registration ceremony, the pre-draw eligibility witness, the wall-clock cut-off with MISSED and STOP,
  the restore notices and the after-hand-unzip reconciliation. **It is a direction, not a ratification; supplement
  v0.8's rules stand until a reviewed amendment is ratified. It supersedes only the formal-OV-1 part of EX_252.**
  It asks Claude for a focused scientific design amendment (its section 5, A to F) before the code round.
- **What Claude found on reading the ratified design and the passed code (a finding, not a decision):** the weekly
  session already separates, for a draw caught up after the fact, a variant released before that draw's date (run mode
  `CATCH_UP`) from one released on or after it (`REAL_DEVELOPMENT`): `weekly_session.py`, by the release record's date.
  So an objective participation rule for one prevailing stream exists without any new clock rule: a variant counts at a
  target if its one weekly-tier record for it is a complete pair of class `PROSPECTIVE`, `LATE_PRE_DRAW` or `CATCH_UP`.
  Under that rule a missed week, and a draw lost and replayed after a restore, are counted in the ordinary way; no
  target is "missed" because of the clock; a new method's back-history never enters.
- **Proposed next step, held for the owner's go in this chat (MC-1: Fable, High; a statistical design):** one amendment
  to supplement v0.8 sections 6 and 7 with worked invented examples, and the deployment note v0.4 carrying EX_252's
  corrections with its OV-1 restore section removed; both to the reviewer as EX_254. No code.

## 116. 20 November 2026, 18:35 - the owner's decisions on the OV-1 simplification and on EX_252's two open points; go for the amendment and the deployment note v0.4 (design only)

The owner, in the Claude web chat at 18:33, answering Claude's five points (his words in quotation marks):

1. **Caught-up draws count in the one prevailing score:** "yes if reviewer concurs". (A method counts at a draw if it
   was released before that draw and forecast it under N-1 isolation, whether before the draw or afterwards by
   catch-up.)
2. **The start, and the timeline:** "dates are useless, we already decided ages ago that draw numbers (for a game) are in
   fact our timeline (please ensure Reviewer knows this, it was settled near beginning of project IIRC)". So the
   stream's start is a draw number for each game, and the rule is stated on the draw-number axis. (The ratified text is
   R3 v0.5, MRD-12: "The time axis is the draw number ... Dates are never used for ordering or arithmetic.")
3. **Reversing three decisions of 17 November 2026 in supplement v0.8** (a missed week counts as neutral; a stopped
   formal test stays stopped; the owner's `register` and `stop` commands): "confirmed". They fall away when the
   amendment is ratified, not before.
4. **W-23 is kept** for every dependency upgrade ("yes to recommendation"): the reviewer's look at the test evidence and
   the owner's go before real production use; one step in the run sheet.
5. **One line may be added to `install_upgrade_dependencies_into_venv.bat`** to remove the "environment verified" marker
   before it changes anything: "yes".

"Cool we have a way forward." Taken as the go for the two design documents Claude proposed in entry 115 (Fable, High):
the OV-1 amendment and the deployment note v0.4, to the reviewer as EX_254. **Design only. No code, package, task file,
Windows step, install or run is authorised.** Supplement v0.8 stays in force until the amendment is reviewed and
ratified.

## 117. 20 November 2026, 18:41 - the OV-1 simplification amendment (DRAFT v0.1) and the deployment design note (DRAFT v0.4) sent for independent review (EX_254); no owner decision

- **Done under entry 116's go (Fable, High; design only, no code):**
  `exchange/CLAUDE_WEB_TOOLS/mhupb/ov1_simplify/MHUPB_OV1_SIMPLIFICATION_AMENDMENT_DRAFT_v0_1.md` (with `ov1_prevailing_examples.py` and its output: invented draws and toy methods through the passed kernel);
  `exchange/CLAUDE_WEB_TOOLS/mhupb/deploy/MHUPB_DEPLOYMENT_DESIGN_NOTE_DRAFT_v0_4.md` (exact diff `NOTE_v0_3_TO_v0_4.diff`; builder `make_note_v0_4.py`). Sent as `exchange/EX_254_Claude.md`.
- **The amendment's rule:** one prevailing score per game; a variant counts at a target if its one weekly-tier record for
  it is a complete pair of class `PROSPECTIVE`, `LATE_PRE_DRAW` or `CATCH_UP`; the start is a draw number per game fixed
  at ratification (Oz Lotto 1710, Powerball 1593 if before 24 November 2026); every draw once, in order; factor 1 only
  for no counted pair or V = 0; one append-only line per draw that must equal its rebuild; blocked, never stopped.
  Deleted: registration, the pre-outcome witness line, the cut-off, MISSED, STOP, every restore-specific rule. A new
  variant's back-history goes to the league table, the reconstruction file (made automatic) and the exploratory view,
  never into the score. The guarantee is stated under four conditions (isolation; released first; every draw once;
  honest operation, including that the choice of backup is never made to move a score).
- **The note v0.4:** EX_252's corrections (the restore's payload and exact allowed difference; the environment marker
  with the full digest at each job boundary; W-23 as five ordered steps; the snapshot-lock refusals; the hand unzip);
  section 9 replaced by "nothing special"; it depends on the amendment and is to be ratified with it or after it.
- **The owner's condition on point 1 (caught-up draws count "if reviewer concurs") is put to the reviewer in EX_254.**
- **Model (MC-1):** the Fable task is finished. Opus until the reviewer replies.

## 118. 20 November 2026, 19:07 - EX_255 (R-3 RECHECK of the OV-1 amendment v0.1 and the deployment note v0.4) read and recorded; an owner clarification relayed in it; Claude holds for the owner's go

- **EX_255** (`exchange/EX_255_ChatGPT.md`, main `4c5e361`): the simplification is accepted in principle (one prevailing
  score per game; the kernel; full historical walk-forward and recomputed rankings for a new method, the automatic
  reconstruction file; the exploratory view; the removal of registration, the witness line, the cut-off, MISSED, STOP
  and the restore rules; the deployment architecture of v0.4). The reviewer concurs IN PRINCIPLE that caught-up draws
  count, conditionally (below). Four findings:
  - **R3-E01 (blocker):** participation in the score must rest on immutable DRAW NUMBERS, not on the release record's
    day compared with a draw's derived date. An `effective_first_draw_number` per game for each released variant, and
    an end number for a retired or superseded one, in the existing release records; a reinstated release keeps its
    original numbers; the existing date test in the staged weekly code must not remain as a hidden science gate.
  - **R3-E02 (blocker to an unconditional 2.5% claim):** the as-of-target cohort and the version used for a delayed
    draw must be fixed by pre-target records, not by today's roster; "honest operation" is an ordinary assumption and
    not a substitute; say exactly when the bound is supported and when a line is of lesser evidential standing.
  - **R3-E03 (major):** the start as two explicit draw numbers fixed at the reviewed freeze of the complete
    implementation (the reviewer's preference), not at ratification.
  - **R3-E04 (major):** the deployment note must not say a restore leaves the score unchanged without conditions (the
    amendment's own examples 5b and 5c differ). Plus one test oracle in the note still says "nothing extra".
- **The owner's clarification to the reviewer, relayed in EX_255 section 0:** YES to an effective starting draw number
  for each method, revision and game, fixed when it is released, to decide when it joins the prevailing score. Dates
  and times may be kept for backups and administrative evidence but are not used in normal scientific calculations,
  because the actual time of a draw cannot be guaranteed even when its schedule is known.
- **Claude's note:** EX_254 question 6 described the date test as merely placing a release on the draw-number axis.
  The reviewer and the owner read it as a scientific gate; that reading is accepted. The note v0.4's "the score is
  the same" overstated what the amendment's own example 5b showed.
- **Held for the owner's go (MC-1: Fable, High):** the corrected amendment (v0.2) and deployment note (v0.5), to be
  EX_256. No code.

## 119. 20 November 2026, 19:42 - the owner's decisions on EX_255's open points; go for the amendment v0.2 and the note v0.5 (design only)

The owner, in the Claude web chat at 19:40 (his words in quotation marks):

1. **The Python environment is not pinned for a delayed draw.** "why ? it maybe gets tested and implemented in a
   methodical way (eg dev the[n] prod) independently of draws. A restore could prompt the human to re-create the venv
   with the latest python/pypi-stuff before proceeding or even do it automatically. this project pinning environments
   begs trouble eg when an older python has been uninstalled perhaps for no-project related reasons. I think the
   release environment should live with what it receives ... changing it basically at will - if it breaks we restore
   and do something different."
2. **The start of the prevailing score (EX_255 E03): the draw after the implementation.** "ok to decision 1 - via its
   walk-forward at implementation it should have a valid prediction 'for real' and scored/ranked/ov-1 on the draw after
   implementation."
3. **A release's effective first draw number: the next available draw, worked out at the release, after its
   walk-forward and catch-up; not typed by the owner as the default.** "after a walk-forward/catchup at implementation
   the next available draw (perhaps implementation does a walkforward and then a catchup, I suppose, maybe even
   potentially talking into account implementing a nominated bunch of new methods or newly versioned methods, in one
   go)." One release may carry several new methods or revisions.

Taken with EX_255's relayed clarification (entry 118: draw numbers, not dates, decide when a method joins the score)
as the go for the corrected amendment (v0.2) and deployment note (v0.5), to the reviewer as EX_256 (Fable, High).
**Design only.** Entry 116 item 4 (W-23 kept for every dependency upgrade) is not changed by this entry; Claude asks
the owner separately whether he wants it revisited, which would be a rule change for the reviewer.

## 120. 20 November 2026, 19:47 - the OV-1 amendment DRAFT v0.2 and the deployment note DRAFT v0.5 sent for the recheck (EX_256); no owner decision

- **Done under entry 119's go (Fable, High; design only, no code):** `exchange/CLAUDE_WEB_TOOLS/mhupb/ov1_simplify/MHUPB_OV1_SIMPLIFICATION_AMENDMENT_DRAFT_v0_2.md`
  (exact diff `AMENDMENT_v0_1_TO_v0_2.diff`; `ov1_prevailing_examples_v2.py` and its output) and
  `exchange/CLAUDE_WEB_TOOLS/mhupb/deploy/MHUPB_DEPLOYMENT_DESIGN_NOTE_DRAFT_v0_5.md` (exact diff `NOTE_v0_4_TO_v0_5.diff`; builder `make_note_v0_5.py`).
  Sent as `exchange/EX_256_Claude.md`. All four findings of EX_255 accepted.
- **E01:** one field in the existing release record, `effective_first_draw` (a number for each game): where its variants
  start and where the variants it retires or supersedes stop; set by the release step as the last draw on file plus
  one, after the catch-up; never recomputed; kept when a release is put back after a restore; the two existing
  records named in the code with 1587 and 1704. The date test is removed as a gate in every place it occurs
  (`weekly_session.py`, `weekly_records.py`, `contract_dispatch.py`, `walk_forward.py`; inventory in the amendment's
  section 5). Dates stay for labels, backups and administration.
- **E02:** each line's standing, SUPPORTED or QUALIFIED, by an objective rule, derived from the line and the release
  records and never stored; nothing stops; the report says whether the 2.5% bound is supported or not certified from a
  named draw. The guarantee has four software-checked conditions and separately listed ordinary assumptions.
  **The environment is not pinned (the owner, entry 119): stated as an ordinary assumption; the reviewer is asked to
  judge whether the claim can stand on that.**
- **E03:** the start is the first-draw numbers of the release that first installs the recorder in production.
- **E04:** the note states when a replay equals the lost score and when it does not, and the order after a restore.
- **Open with the owner (asked in the chat, not decided):** whether he wants W-23 itself revisited. Until he says so
  it stands as in entry 116.
- **Model (MC-1):** the Fable task is finished. Opus until the reviewer replies.

## 121. 20 November 2026, 20:43 - EX_257 (RECHECK: F01, F02) and EX_258 (the owner's course correction) read; the owner's six decisions recorded from the reviewer's permanent record; Claude holds for the owner's go

- **The permanent record, to be read in full by any chat taking over:** `exchange/DECISIONS/OWNER_DIRECTION_2026_11_20_OV1_RESTORE_METHOD_CONTINUITY.md`
  (committed by the reviewer at main `12f8f9a`; companion to `exchange/EX_258_ChatGPT.md`, main `aac75e9`). It separates
  the owner's direction from the reviewer's analysis. It is a direction and a review-cycle record, not a ratified
  design; the ratified documents stand until reviewed amendments are ratified.
- **The owner's decisions, as that record lists them (its section 7; relayed by the reviewer, not said in this chat):**
  1. **No method and no earlier revision is retired** because another revision is released or because its performance
     is unremarkable. "Leave them ALL working." A new revision is additional to its predecessor.
  2. The complete historical N-1 assessment, the recomputed rankings and the TOP and WORST inspection are kept for every
     method and revision; sustained positive or inverse signals are both of interest.
  3. One prevailing, continuous, draw-number-based OV-1 per game; new identities join from their effective next
     future draw; no back-fill into the prevailing score.
  4. **A restore recreates exactly the selected verified snapshot** as the known working state. Later releases are not
     applied automatically, nothing is retired, replaced or activated from Git or a set-aside tree, and the environment
     is not rebuilt automatically. The lost draws are caught up in draw-number order with the snapshot's own methods
     and revisions. Any later method or software change is a separate owner decision after that. The owner's words on
     putting later releases back first: "that isn't a restore it is a restore being mangled."
  5. No Python environment pinned per draw; dependencies change through the ordinary reviewed route. (W-23 is not
     changed by this.)
  6. Future evolutionary additions or combinations of methods are of interest; no automated retirement, culling or
     selection engine is authorised.
- **What this withdraws from Claude's drafts sent as EX_256:** in the amendment v0.2, a release's first draw as the
  point where superseded variants stop (2.3), the examples 6a and 6b, and "put later releases back first" as the way
  to keep lines supported; in the note v0.5, the same order in sections 8 and 9 and `check`'s printing of it. The
  reviewer withdraws its acceptance of example 6b as the normal case and its assumption that later releases are
  reinstated (EX_258 section 2).
- **EX_257** (`exchange/EX_257_ChatGPT.md`, main `b55ceb9`): the draw-number design is accepted in principle. **F01:** the
  2.5% bound is a CONDITIONAL claim; a structurally SUPPORTED line is software evidence, not proof of the
  non-anticipation assumption; the report must not print "the 2.5% bound is supported" from the four checks alone; no
  environment pin and not alternative 2b. **F02:** give an executable order of commands for a batch of new methods
  (history, catch-up, one activation boundary), resolving that the staged `--fill` expects released variants.
- **Claude's first reading of the code for "keep all revisions" (a finding, not a decision):** the installed registry
  holds one active entry per (game, method, variant) chain, and `active_entry` is read in the dispatch gate, the
  walk-forward driver, the weekly session, the report writer and Mode H; a method's code is replaced in place at a
  revision rollover. So "old revisions keep running" is either a change through all of those, or it is met by
  releasing a changed method as an additional variant with its own code, leaving the registry as it is.
- **Held for the owner's go (MC-1: Fable, High):** the amendment v0.3 and the note v0.6, to be EX_259. No code.

## 122. 21 November 2026, 11:36 - the owner's course correction of 21 November 2026 (EX_259): families and variants only, a clean new baseline, one install-is-release workflow, minimum administrative software; go for the redesign documents (design only)

**Sources.** `exchange/EX_259_ChatGPT.md` (main `ae4d690`; the primary instruction, self-contained), read with EX_258 and
`exchange/DECISIONS/OWNER_DIRECTION_2026_11_20_OV1_RESTORE_METHOD_CONTINUITY.md`; and the owner's message in the Claude
web chat of 21 November 2026, 11:32. Background only, not authority:
`doc/Review_Checkpoint_Predictive_Randomness_EX256_EX258_2026-11-21.md` (the owner: "historical discussion context
ONLY, not governing authority"). Where they conflict, EX_259 governs. The reviewer's updated handover candidate is
H-2 v3r8 (main `ef32c7b`, `c62bc12`).

**The owner's decisions (EX_259 marks these as owner-ratified directions; the mechanisms are for Claude and the
reviewer to design and for the owner to ratify afterwards):**

1. **Every E-method is a family, even a family of one.** One uniform source-tree structure for all. The directory
   convention is delegated to Claude and the reviewer.
2. **The revision is eliminated as a separate scientific identity.** A changed implementation is a new, uniquely
   identified, independent variant of its family (or a new family if the hypothesis changes). Deliberate, even though
   it is more redesign than keeping the old field.
3. **Every old and new variant stays runnable and is evaluated at every draw.** No supersession, no latest-wins, no
   culling, no automatic retirement. TOP and WORST are both kept; an inverse deviation is as interesting as a direct
   one. Why: draws accumulate slowly, so "nothing seen yet" is not evidence of no effect.
4. **A changed shared helper must not change an earlier variant.** A new variant embeds its own copy or uses a distinct
   immutable versioned helper. Truly behaviour-invariant infrastructure may stay shared.
5. **Two separately testable implementation phases:** (1) the uniform source layout, with behavioural-equivalence
   oracles for the existing variants' forecasts; (2) the identity, registry, dispatch, forecast, score, ranking and
   OV-1 contracts migrated and simplified.
6. **A clean new scientific baseline.** The sealed Mode H study and the revision-based records are earlier, indicative
   research. They are not a schema or a freeze the future system must inherit. The compatible history is recomputed
   under the new identity. No permanent legacy reader or crosswalk. **Nothing is deleted now:** before any code,
   migration or destructive step the owner downloads a source ZIP from GitHub, and a complete verified cold copy of
   the old functioning state is kept. The accepted official draw masters and their provenance are retained.
   Recomputed history is never labelled as published at the original time.
7. **Installation is release.** One owner-approved installation of one or more variants, then four stages: install;
   automatic missing-only historical walk-forward through the last accepted draw M, with the per-draw league reports
   and the exploratory OV-1 regenerated, and a forecast of the assumed-pending M+1; the one reviewed Lotterywest-GOV
   results updater; chronological catch-up over M+1..N for all installed variants, a saved cumulative league report
   after each target, the prevailing OV-1 for each target, and always an attempt at N+1. A catch-up of zero draws is
   normal. A long history fill may span a real draw; that is accepted. No clock deadline suppresses a forecast.
8. **Saved per-draw cumulative league reports,** for every historical and every weekly draw, showing TOP and WORST,
   with plain game and draw-number file names. When variants join, the current reports and the exploratory OV-1 are
   recomputed; earlier derived editions are obsolete and need not be kept.
9. **Two uses of OV-1:** one continuous prevailing score per game (new variants join from an objective first forward
   draw number; earlier factors never rewritten; kernel, six lambdas and the bar of 40 unchanged), and a separately
   labelled exploratory score rebuilt from the whole current population at any time. The 2.5% claim is conditional on
   fair draws and on non-anticipation; software checks do not prove the second.
10. **Minimum freeze and administrative software: protect against bugs, not fraud.** "On his own PC he could
   edit/bypass local protections, but would have no reason to commit scientific fraud." Kept, as function: a
   canonical forecast and score per (game, family, variant, target) with TOP and WORST; idempotent reuse; no duplicate
   score and no partial write taken as complete; bounded crash resume; enough provenance to reproduce a surprise.
   The process, orphan and no-kill safeguards stay. A target-wide weekly freeze set is not intrinsically necessary.
11. **Backups and restore:** the complete verified production ZIP (code, data, results, records and `.venv`), the
   recovery kit, and the exact-snapshot restore with no later release put back automatically (entry 121, decision 4),
   stand. The deployment note v0.5's "update first reinstates later releases" is an error to remove.
12. **Proportion:** an owner-operated home-PC investigation; a real null result is acceptable; stronger evidence
   standards can be added if an extraordinary result ever warrants outside scientists.

**In the Claude chat (the owner's words):** "Please critically assess the proposals rather than simply accepting every
implementation suggestion. Where a simpler solution satisfies the scientific requirements, prefer it. Where a genuine
mathematical, operational or safety concern exists, identify it clearly and propose the least complicated satisfactory
solution." "I approve the design work only, including the requested two separately verifiable implementation phases
and associated test proposals. No source-code implementation, installation, production operation, real-data run,
migration or deletion is authorised at this stage." "My overriding intention remains: maximise useful scientific
research capability, reproducibility and recoverability while minimising unnecessary administrative software
complexity."

**What this supersedes.** Entry 121 decision 1's "new revision is additional" becomes "there are no revisions"; the
two questions Claude put to the owner on 20 November (a new version as a named variant; the batch order) are answered
by decisions 2 and 7. The OV-1 amendment v0.2 and the deployment note v0.5 are superseded as drafts. **The ratified
documents (design v0.1r7, supplement v0.8, the code plan, R3, E2R-1, H-1 v7r1) stay in force until the redesign is
reviewed and ratified;** the three MHUP-B slices stay uninstalled.

**Go:** the redesign documents for independent review as EX_260 (Fable, High). Design only.

## 123. 21 November 2026, 11:44 - the research system simplification design (DRAFT v0.1) and the deployment design note (DRAFT v0.6) sent for independent review (EX_260); no owner decision

- **Done under entry 122's go (Fable, High; design only, no code):** `exchange/CLAUDE_WEB_TOOLS/simplify/RESEARCH_SYSTEM_SIMPLIFICATION_DESIGN_DRAFT_v0_1.md`
  (a new full document; supersedes the OV-1 amendment drafts v0.1 and v0.2) and `exchange/CLAUDE_WEB_TOOLS/mhupb/deploy/DEPLOYMENT_DESIGN_NOTE_DRAFT_v0_6.md`
  (exact diff `NOTE_v0_5_TO_v0_6.diff`; builder `make_note_v0_6.py`). Sent as `exchange/EX_260_Claude.md`.
- **The design, in short:** identity is game, family, variant, target; one source layout for every family
  (`src/methods/<family>/<variant>/method.py`); family folders and `_shared/` are add-only, checked by the deploy tool;
  the registry is the folder tree; the canonical record is two append-only lists per variant per game (forecasts,
  scores); one job (`Run_Research.bat`) is the four stages and is safe to rerun; a saved cumulative league report for
  every draw with TOP and WORST; the prevailing OV-1 counts a variant from its `FORWARD_FROM` draw (the first draw
  whose result had not been published when the job last read the official source), the exploratory OV-1 is rebuilt
  over all history; the 2.5% sentence is conditional; the new system writes under `results/research/` in a new
  production tree, so the clean baseline destroys nothing; the old records are used once, by a transition checker;
  phase 1 (moves only) and phase 2 (contracts), each with an equivalence check.
- **The note v0.6:** nothing is put back after a restore; section 0A; `init` copies `source_data/` only; one
  deployment-log line per release; the add-only check.
- **Four choices put to the owner for ratification (design section 14):** the job runs the updater itself (a change to
  his decision of 4 November 2026); `FORWARD_FROM` as designed or the simpler "plus one at installation"; the cold
  copy of the whole E: clone by a small reviewed script or by hand; one new system specification or amendments.
- **Claude's advice on the chats (given to the owner in the chat):** finish this design round here; after
  ratification write H-1 v8 and start the two code phases in a new Claude chat.
- **Model (MC-1):** the Fable task is finished. Opus until the reviewer replies.

## 124. 21 November 2026, 13:00 - EX_261 (R-4 RECHECK of the simplification design v0.1 and the note v0.6: F01 to F07) and EX_262 (the owner's supplement: DEV, QA and PROD; local-file installs; REINSTALL INFRA: F08 to F10); the owner's decisions, including mandatory QA before every PROD installation

**Sources.** `exchange/EX_261_ChatGPT.md` (main `4484006`), `exchange/EX_262_ChatGPT.md` (main `918ddc6`; "SUPPLEMENTS EX_261;
it does not close, supersede or soften any of its required findings"), and the owner's message in the Claude web chat
of 21 November 2026, 12:54. The reviewer's handover candidate is now H-2 v3r9 (main `0ad1e23`, `6eeaa63`).

**The reviewer's disposition (EX_261):** the direction of EX_260 passes in principle (P01 to P07). RECHECK on details:
F01 the list invariants do not cover FAILED and INSUFFICIENT_HISTORY lines or metadata lines; F02 an explicit
owner-only withdrawal must be specified; F03 `FORWARD_FROM` wording, the first job and a failed updater; F04 the cold
copy is the PROJECT CLONE only, and "E: stays whole" was untrue once phase 1 moves code there; F05 the note v0.6 still
gave executable steps for records that no longer exist; F06 a whole-results-file hash is audit provenance, never a
model input or part of the forecast content identity; F07 one complete system specification.

**Owner decisions (relayed in EX_261 and EX_262; the mechanisms are Claude's to propose and the owner's to ratify):**

1. **One new COMPLETE, authoritative system specification** of the redesigned active system ("one new complete system
   specification sounds better"), not a short overview that needs five obsolete documents beside it.
2. **A defective variant may be explicitly withdrawn by the owner** through a reviewed mechanism, from a future draw
   number. Never automatic, never by performance; code and history are kept; the corrected method is a new variant.
3. **In QA and PROD the installed variant folder tree is the registry.** DEV differs on purpose: it must allow
   unfinished, work-in-progress variants to be tried without touching PROD.
4. **Readiness is a small DEV-side marker in the variant's folder** (tentatively `I_AM_INSTALLABLE.json`), made by a
   small utility or by hand if it validates. It is not a version, a registration or a release step.
5. **INSTALL QA and INSTALL PROD discover by themselves** the marked-ready DEV variants that the chosen target does not
   yet hold. An optional filter is fine. Unfinished source is never swept up because it shares a folder.
6. **Three separate trees: DEV on E:, a real, isolated QA test bed (TEST_BED, on D:), and PROD on G:.** Each has its own
   root, data, results, Python environment and backup root, set in a plain INI. All paths are configuration. QA
   backups may sit on D: outside the QA tree; PROD stays `G:\a_p_r_i_r` with backups in `T:\a_p_r_i_r_backups`. One
   installer, research engine, backup and restore serve every role.
7. **Deployment does not depend on Git commits or on GitHub.** The verified files in the local DEV tree are the source.
   Git stays an optional development convenience. Nothing copies all tracked source into PROD.
8. **Helpers are not scored variants.** Keep them inside variant folders where practical; otherwise stable, immutable,
   versioned family or cross-family helpers. No dependency solver.
9. **Shared INFRASTRUCTURE is updated by a separate, explicit command** (the owner's name: REINSTALL INFRA, because
   infrastructure may legitimately be overwritten). Variants and versioned helpers stay add-only through every route.
10. **DEV's documents, exchange, tests and experiments are never installed** into QA or PROD merely because they exist.
    No production operation by an ordinary DEV research command.

**The owner's decision in the Claude chat, 21 November 2026, 12:54 (his words):** "Successful QA verification is required
before every ordinary PROD installation, including both new variant batches and REINSTALL INFRA. PROD must verify
that the source files and required helper/infrastructure files match the exact versions successfully tested in QA.
Changes after QA verification require another QA pass. Do not implement a QA-bypass mechanism at this stage. All
other instructions in EX_261 and EX_262 remain unchanged. Please incorporate this decision into the complete system
specification and deployment design." (This settles the one point EX_262 section 2.2 left open.)

**Still for the owner at ratification (EX_261 section 4; not decided):** A, whether the research job runs the official
updater itself; B, the corrected `FORWARD_FROM` rule; C, the scope of the cold copy of the old project clone; D, the
file mechanics of a withdrawal.

**Go:** the complete system specification and a coherent deployment design, for independent review as EX_263 (design
only; Fable, High). No code, layout change, backup, results fetch, QA or PROD creation, install, run, migration,
deletion or restore is authorised.

## 125. 21 November 2026, 13:08 - the complete system specification (DRAFT v0.1) and the deployment design (DRAFT v0.7) sent for independent review (EX_263); no owner decision

- **Done under entry 124's go (Fable, High; design only, no code):** `exchange/CLAUDE_WEB_TOOLS/simplify/SYSTEM_SPECIFICATION_DRAFT_v0_1.md`
  (the one complete specification of the active system; replaces the simplification design v0.1 as a draft) and
  `exchange/CLAUDE_WEB_TOOLS/simplify/DEPLOYMENT_DESIGN_DRAFT_v0_7.md` (a complete document, not a diff). Sent as `exchange/EX_263_Claude.md`.
  F01 to F10 accepted; the specification's section 21 maps each.
- **The owner's QA decision as designed:** a QA operation ends by testing QA as a whole (the suite with QA's Python;
  regression of what was installed; the research job in QA) and writes a pass listing every installed file with its
  hash and the tests and tool used. Every PROD operation makes five checks against the pass before touching anything
  (QA unchanged since the pass; DEV's bytes are the passed bytes; PROD's infrastructure equals the pass's; every PROD
  variant and helper is in the pass; the tests and tool are the passed ones). No option skips them.
- **Also in the design:** three trees set by `ENVIRONMENT.ini` (a tree is what its own file says); the readiness marker
  bound to file hashes; `Install.bat` (ready-and-absent, never overwrites), `Reinstall_Infra.bat` (an explicit manifest;
  a full regression in QA), `Init_Tree.bat`, `Verify_Tree.bat`, `Withdraw_Variant.bat` (one line in the variant's own
  file); a forecast line is `FORECAST` or `NO_FORECAST`; content and envelope; an explicit start for the prevailing
  OV-1; the updater in PROD only, with QA and DEV receiving results by a checked copy; the coordinator in DEV only;
  the cold copy of the project clone folder with a dry run; rollback only from an unpacked cold copy.
- **Five choices for the owner at ratification (specification section 19), not decided:** A the job runs the updater
  itself; B `FORWARD_FROM` as corrected; C the cold copy's scope; D the withdrawal mechanics; E nothing copied back
  from PROD to DEV or Git (changes the decisions of 16 and 17 November 2026 to commit results and score records).
- **Model (MC-1):** the Fable task is finished. Opus until the reviewer replies.

## 126. 21 November 2026, 13:22 - the owner replaces mandatory QA with the DEV readiness marker alone; his question on the settings files; EX_263 revised under the same number at his request

- **The owner, in the Claude web chat at 13:18 (his words):** "'Only if all of that succeeds is a QA pass written, listing
  every installed file with its hash' etc is great and I've been there as a DEV manager and later a QA manager and
  know the overheads well, however I am seeking an abbreviated QA mechanism that satisfies only me, and so I'd prefer
  revert to only using 'i am installable' marker in dev for installing to prod. Also, how do the .ini files get
  created/configured initially and then not overwritten somehow by .bat or .py later ? can you update the EX (same
  number) and pop the outstanding decisions options in that and update the blurb for reviewer ?"
- **Decision recorded:** this **replaces the QA part of entry 124** (mandatory QA verification of the exact files before
  every PROD installation, no bypass). PROD is installed on the DEV readiness marker alone. QA remains as the owner's
  own optional test bed. The rest of entry 124 stands.
- **Done (design only):** the system specification DRAFT v0.2 and the deployment design DRAFT v0.8, each built from the
  previous draft by counted replacements with an exact diff (`exchange/CLAUDE_WEB_TOOLS/simplify/`): the QA pass record and the five checks
  are withdrawn; each install checks itself in the tree it installs into (markers match; add-only; the suite with
  that tree's Python; a sample regression after variants, a full one after infrastructure); a marker for
  infrastructure is proposed (choice F). The settings files: DEV's is made once by the owner from a tracked example
  and ignored by Git; a tree's is written once, create-only, by `Init_Tree.bat`; it is on no manifest and no program
  writes it afterwards, except a restore writing the backup's own copy into a fresh tree; a later change is the
  owner's hand edit.
- **`exchange/EX_263_Claude.md` was rewritten in place at the owner's request,** before any reply; the first version is
  at main `2e5c1c0`. It now lists the owner's six outstanding choices with their options (A the updater inside the
  job; B `FORWARD_FROM`; C the cold copy's scope; D withdrawal mechanics; E nothing copied back to Git; F a marker for
  infrastructure). None is decided.
- **Claude's note:** the first design took "QA verification is required" as a gate between trees; the owner wanted a
  place to look. A clarifying question first would have saved a round.

## 127. 21 November 2026, 15:10 - the owner's decisions on the infrastructure marker, the manifest's name, helpers and the DEV conveniences; EX_263 revised a second time at his request

In the Claude web chat, 14:45 to 15:08, before passing EX_263 to the reviewer, the owner asked how marking, the
infrastructure list and shared code work, and decided (his words in quotation marks):

1. **A readiness marker for the infrastructure: yes.** "I like it." (Former choice F of EX_263 is closed.)
2. **The infrastructure list is `deploy\INFRA_MANIFEST.ini`:** "that would be deploy\INFRA_MANIFEST.ini to denote it as
   not just another human deleteable txt file." It is first written with the phase 2 package and reviewed, then
   edited by hand to add or remove a file.
3. **Helpers stay strictly add-only; no in-place update of an installed helper,** and a wrong helper is corrected by a
   new versioned file with successor variants: "so we make new variants referencing the new helpers, retiring the old
   ones and removing their I_AM_INSTALLABLE. OK. yes to option 1 Keep the rule, add three small DEV conveniences."
   The conveniences: a listing of the variants that declare a helper; a generator of unmarked successor folders for
   his review; batch marking, unmarking and withdrawal. (Claude had offered, as the alternative, an owner-ordered
   correction in place with the history recomputed under the same names; not chosen. A narrower "proved harmless"
   in-place update was also described and is not adopted now; it can be added later if needed.)
4. **A withdrawn variant's marker is removed in DEV,** so that no tree created later receives it. (This reverses the
   sentence in the specification v0.2 section 11 that a new tree would install it.)

**Done (design only):** the system specification DRAFT v0.3 and the deployment design DRAFT v0.9, by counted
replacements with exact diffs (`exchange/CLAUDE_WEB_TOOLS/simplify/`); `exchange/EX_263_Claude.md` rewritten in place a second time, before
any reply (earlier versions at main `2e5c1c0` and `e3a7935`). **Five owner choices remain open:** A the updater inside
the job; B `FORWARD_FROM`; C the cold copy's scope; D withdrawal mechanics; E nothing copied back to Git.

## 128. 21 November 2026, 17:28 - the ChatGPT reviewer chat has ended (reached its limit); EX_264 and EX_265 read and recorded; the owner's decisions relayed in EX_265

- **The reviewer chat ended on 21 November 2026 after committing EX_265** (the owner, in the Claude chat at 17:27: it
  "reached its limit and suddenly and permanently ceased to function"). Its last committed files: `exchange/EX_264_ChatGPT.md`
  (main `1dc9916`), `exchange/EX_265_ChatGPT.md` (main `147257d`), and the handover candidate
  `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r9_RATIFICATION_CANDIDATE_20261121.md` with its blurb (main `0ad1e23`,
  `6eeaa63`; current only to EX_262). **A new reviewer chat is needed before any further review.**
- **EX_264 (R-5 RECHECK of the specification v0.3 and the deployment design v0.9):** the architecture is accepted
  (P01 to P06). Findings: **F01** a withdrawal must override later scoring of a pending forecast; **F02** the markers'
  exact hash closure (each marker excluded from its own hash; no cache or editor files; the same for
  `ENVIRONMENT_VERIFIED.json`); **F03** every newly installed variant must itself be exercised by a small smoke case in
  the destination; **F04** never promise a rollback to a backup that failed, and a destructive infrastructure overwrite
  needs a verified restorable point; **F05** a full regression of everything at every infrastructure reinstall is not
  proportionate. Notes N01 to N05 (among them the syntax of `INFRA_MANIFEST.ini`). The reviewer's views on the open
  choices: A1, B1, C1 (or C2), D1 with F01.
- **The owner's decisions relayed in EX_265 (it says they are owner-decided design directions; the mechanisms are still
  to be designed, reviewed and ratified):**
  1. **Choice E is decided: an optional, complete, read-only-from-PROD copy of the research data** (accepted draws and
     their provenance, forecasts, scores, league reports, both OV-1 records) **into DEV or QA, directly replacing the
     destination's active research data** after a printed summary and one confirmation. PROD is never written by it,
     not even a marker, lock or log. No Git. Program code, `.venv`, settings and control records are not copied.
     ("I mean a copy-from type utility should only read from prod never write to it.")
  2. **F01 agreed:** a forecast pending at the withdrawal draw stays as history and is never scored.
  3. **F02 agreed, with the least machinery:** one small utility and an ordinary hash list; no receipts or resolver.
  4. **F03 agreed:** small, isolated smoke tests of each new variant with the destination's own environment, writing
     only to that tree's scratch folder and never a canonical forecast, score, report or OV-1 line.
  5. **F04 agreed: rollbacks are manual:** the owner chooses a verified last-good backup, restores exactly it, then runs
     the updater and the catch-up. Before a destructive infrastructure reinstall the tool states truthfully which
     verified backups exist; with none, the overwrite is refused (ordinary research jobs still go on).
  6. **F05: no automatic full-history recomputation in PROD at an infrastructure reinstall.** Claude is to propose a
     proportionate, science-safe rule. **A small reset/replay utility** for a chosen tree (DEV, QA; PROD only as a
     separate, explicitly selected operation): whole derived results, or a game's draws from J onward with an
     optional end N, one confirmation, downstream results kept consistent.
  7. **QA is optional only in that PROD installation never refers to it;** it is to be a capable laboratory.
  8. **Process:** no new EX is to be issued during a discussion with the owner until he agrees to issue it.
- **Still open for the owner:** A (the job runs the updater), B (`FORWARD_FROM`), C (the cold copy's scope), D (withdrawal
  mechanics); EX_265 says he agrees with the recommendations in principle but has not formally chosen.
- **Requested of Claude by EX_265:** a corrected complete specification and deployment design as EX_266. **Not started;
  held for the owner's go** (MC-1: Fable, High), and it needs a reviewer to go to.

## 129. 21 November 2026, 17:45 - the owner instructs Claude to bring the reviewer's handover up to date in a new edition; his decision on results left over after a copy from PROD

- **The owner, in the Claude web chat at 17:42 (his words):** "go please fix chatgpt handover stuff now into new versions, I
  trust you will do an 'independent frame of mind' job of - it we cannot progress without you updating those docs and
  we have done this elsewhere. then we will commence handover with you asking a few question of the new chat as usual
  and assessing their answers and advising me if they are in a position to start working effectively."
  **This is a one-off, explicit exception to the rule that Claude never edits the reviewer's files.** Claude created NEW
  files and edited none: `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r10_CONTINUITY_CANDIDATE_20261121.md`
  (SHA-256 `29b853ef246cfdb7fba212c06bf70b07bd7d8278ad297759ee010c32b685e44b`) and its `_introductory_blurb.md`. Only the header and
  section 0 are new (through EX_265, each statement citing its committed source; three subsections carried verbatim
  from v3r9 and marked so; a list of where Claude's own drafts are weakest). Sections 1 to 19 were copied byte for
  byte from v3r9 by a script and checked: 73,606 bytes, SHA-256 `ddb656f3...1af1c313`; sections 2 and 3 are 7,676 bytes
  with the protected SHA-256 `70e50dc3...bc72db`. Both files say plainly that Claude, the reviewed party, prepared them
  and that the new reviewer must verify against the sources. H-2 v3r4 (RAT-36) remains the operative ratified handover.
- **Decision:** after a copy of PROD's research data into DEV or QA, results for variants the destination does not
  have installed, or has in a different form: "I'd be happy with warn about them, ignore them and continue."
- **Next:** the owner starts a new ChatGPT reviewer chat with the blurb; Claude supplies takeover questions and assesses
  the answers (HO-2, as before). The owner will then formally choose A to D. EX_266 is not started.

## 130. 21 November 2026, 17:51 - the owner formally chooses A, B, C and D

The owner, in the Claude web chat at 17:50 (his words): "choice A yes to your recommendation. choice B yes to your
recommendation. choice C let me know when to do it and I will manually download a ZIP of the prevailing github project
and save it with the date. choice D yes to your recommendation."

- **A (decided): the research job runs the reviewed Lotterywest-GOV updater itself in PROD,** through the updater's own
  unchanged launcher, with `--no-update` to leave it out. This changes his decision of 4 November 2026 that the updater
  stays separately controlled.
- **B (decided): `FORWARD_FROM`** is the first draw not present in the accepted results on file after a successful check
  of the official source (specification v0.3 sections 10.2, 10.3).
- **C (decided): the owner will himself download a ZIP of the GitHub project and save it with the date, when Claude
  tells him it is time** (before phase 1 moves any source file in DEV). No cold-copy script is to be designed or built.
  **Claude's caveat, put to the owner:** a GitHub ZIP holds tracked files only. The old run folders that Git ignores
  (they hold the old forecast records that the phase 1 oracle and the transition check compare against) are not in
  it; they then exist only in the E: clone. Phase 1 does not touch them, but there would be one copy. Copying the old
  `results` and `transitory_data` folders by hand at the same time would cover that; it is the owner's call.
- **D (decided): withdrawal** by one `WITHDRAWN_FROM` line in the variant's own file, by one command with one typed
  confirmation; the owner unmarks the variant in DEV (specification v0.3 section 11), with EX_264 R5-F01's correction.
- With E decided in EX_265 (entry 128) and F in entry 127, **no owner choice remains open** on the drafts. All of it is
  still design: the specification and the deployment design are to be corrected (EX_266), reviewed and ratified.
- The owner is starting the new ChatGPT reviewer chat with H-2 v3r10's blurb and Claude's takeover questions.

## 131. 21 November 2026, 17:57 - choice C revised by the owner: a full ZIP of the project folder on E:, made by him

The owner, in the Claude web chat at 17:57, after the caveat of entry 130 (his words): "I will instead do a full ZIP of
the project folder tree on E: instead and save that instead." **This replaces entry 130's C.** The owner makes the ZIP
himself, by hand, of the whole project clone folder (ignored run folders and `.git` included), when Claude tells him
it is time: before phase 1 moves any source file in DEV. No cold-copy script is designed or built. That ZIP is then
the preserved copy of the old system and of the old forecast records, and the rollback of the specification's
section 17.2 (unpack it into a new folder, never over the clone).
