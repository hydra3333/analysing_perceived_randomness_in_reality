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

## 132. 21 November 2026, 18:02 - the new ChatGPT reviewer chat's HO-2 takeover answers assessed by Claude; advice to the owner: ready; the owner's acceptance is awaited

- The owner started a new ChatGPT reviewer chat with the H-2 v3r10 blurb and relayed Claude's eight takeover
  questions; its answers came back at 18:01 (relayed in the Claude chat; not a committed file).
- **Claude's assessment: all eight answers are correct against the repository, and the new chat is in a position to
  work.** Points checked by Claude with a tool, not taken on trust: its stated main HEAD (`45f9951`) was the HEAD; its
  v3r10 SHA-256 is the committed file's; its claim that sections 1 to 19 of v3r10 equal the ratified v3r4's is true
  (73,606 bytes identical; Claude had not made that comparison itself and had said so in the handover).
- **Signs of independence:** it read past the handover to the decision log and reported, unprompted, that the
  handover's section 0 is out of date on choices A to D (decided in entries 130 and 131, after the handover was
  written); it states it will not issue an EX without the owner's approval and will not start reviewing EX_266
  before the owner accepts the takeover.
- **One reservation:** asked to name something in Claude's drafts it would challenge, it chose R5-F01, which the
  previous reviewer had already found. That shows accurate reading, not yet an independent finding. EX_266's review
  will show the latter.
- **Not a decision:** accepting the takeover and authorising normal review work is the owner's.

## 133. 21 November 2026, 18:08 - a takeover note and blurb for a new Claude chat; the owner agrees the next steps

- The owner (18:07): "ok to the next steps" (accept the new reviewer's takeover; a short Claude takeover note; EX_266 in
  a new Claude chat on his go), and asked whether Claude's handover documents are fully up to date.
- **Claude's answer:** the decision log, CONTINUITY_NOW, the two drafts, the EX files and the reviewer's handover v3r10
  are current. **The installed Claude handover H-1 v7r1 is not:** its hard rules, roles and protocol still bind, but
  its design sections describe the system being replaced. A full H-1 v8 is due after ratification. To close the gap
  now: `exchange/CLAUDE_TAKEOVER_NOTE_2026_11_21.md` (reading order; state; the decisions and findings EX_266 must
  answer; design leads; things to remember; working method; lessons) and `exchange/CLAUDE_TAKEOVER_NOTE_2026_11_21_blurb.md`
  (the text to paste into a new Claude chat, with the hard rules). Neither is reviewed or ratified; neither replaces
  H-1 v7r1. The ratification register, the roadmap and the reminders file were not updated in this cycle (no
  ratification has occurred since RAT-39).
- The new Claude chat follows HO-2: read and verify first; a first substantive reply; the reviewer's blind questions;
  the owner's acceptance.

## 134. 21 November 2026, 19:20 - HO-2: the new Claude chat's takeover accepted by the owner; normal operations authorised; his answers on numbering, commit rights, the new reviewer and the drafts

- **How it went (no EX numbers, at the owner's choice):** the new Claude chat started from
  `exchange/CLAUDE_TAKEOVER_NOTE_2026_11_21.md` at main `cf4c602`, read the note's reading order, checked it with tools,
  and gave its first substantive reply in the chat. The new ChatGPT reviewer chat (entry 132) sent eight blind questions
  (Q1 to Q8), relayed by the owner at 19:12; Claude answered from the repository before seeing any assessment. The
  reviewer's assessment, relayed at 19:18: **"PASS - Ready for EX_266"**, all eight answers PASS, "no further blind
  takeover questions". Neither chat committed anything during the takeover.
- **The owner's answers to Claude's first reply, 19:11 (his words):** "4. no EX numbers this time. Record the takeover in
  the decision log, as was done for the reviewer's takeover today. 5. yes after acceptance. 6. after acceptance lets
  explore this briefly together 7. New reviewer is accepted and working and awaiting instruction from me to query you.
  re \"Passages in the drafts that later decisions contradict\" later decisions prevail, although after you are accepted
  please create a .md for Reviewer to consider which outlines the contradictions from each and provenance, as a double
  check and seeking advice by reviewer to you and I."
- **Recorded as decided:**
  1. This takeover uses no EX numbers. The next EX is still **EX_266 (Claude)**, as every record says.
  2. Claude's commit rights (H-1 v7r1 section 0B item 4) apply from the acceptance.
  3. **The new ChatGPT reviewer chat is accepted and working** (closes entry 132's "acceptance is awaited").
  4. **Where a passage of the specification DRAFT v0.3 or the deployment design DRAFT v0.9 contradicts a later owner
     decision, the later decision prevails.** Claude writes a document for the reviewer listing each contradiction with
     its provenance, as a double check, asking the reviewer's advice to the owner and Claude.
  5. R5-F04 (item 6 of Claude's reply) is to be explored briefly with the owner: still OPEN.
- **The owner, 19:18 (his words):** "I accept that the handover is complete and you are now authorised for normal
  operations." He added that he is "slightly disconcerted that seemingly decisions may be ahead of some documentation
  (I had asked both chats to ensure it was up to date) but that is much better clarified than left dangling."
- **The reviewer's three observations (its views, not owner decisions):** (1) R5-F04: entry 128 is the latest explicit
  decision record and is the current design direction unless the owner corrects it; Claude should not silently weaken
  the recovery safeguard. (2) Earlier committed records stay as historical evidence; no new Git-export requirement is
  authorised (EX_265 section 8). (3) Withdrawal stays strictly owner-controlled: never by `Make_Successors`, an
  installation or a helper inspection; successor folders are unmarked candidates for human inspection (EX_264 Q8).
- **Record slips found by the new chat** (none changes a decision): the takeover note's "next entry 133" (133 was the
  note's own entry; this is 134); the lower sections of `exchange/CONTINUITY_NOW.md` were stale (brought up to date with
  this entry); H-2 v3r10 section 0.8 says A to D are open (true when written; decided in entries 130 and 131; the
  reviewer's file, not edited); entry 128 item 5 records "with none, the overwrite is refused" as owner-agreed, where
  EX_265 section 5 has that sentence as the reviewer's recommendation (open, item 5 above).
- **Traced by the new chat, for the record:** the 4 November 2026 decision that choice A changed is E4 in register v0.31
  ("The results updater stays a separate operation"). The 16 and 17 November decisions to commit records (D5, entries 47
  and 48, commit `c7622fa`; OD-5, entry 70, commit `cc665ce`) were one-off commits of existing records, not a standing
  export rule.
- **Model:** the owner set Opus 5.5 at 19:18. EX_266 is Fable (High) work and waits for his go.

## 135. 21 November 2026, 20:52 - the owner's new decisions from his discussion with the reviewer (handback `exchange/ChatGPT_to_Claude_QA_and_EX266_Decisions_2026_11_21.md`, main `9f5c132`): QA's role; a QA software reset from PROD; the research-data reseed required; complete reset/replay; `FORWARD_FROM` renamed; R5-F04 changed

- **Source and status.** The reviewer's handback, committed by the owner at `9f5c132` (SHA-256
  `64c9bc2bff9eb98ed2622980499a484550a088dc38bae909817c2a44dbd97215`), relayed to Claude by the owner at 20:50 ("I hope
  the referenced md goes some way to clarifying outstanding matters which affect the design and perhaps 266"). It is
  not an EX and not a ratified design. It labels each point OWNER - NEW, OWNER - EXISTING, REVIEWER ADVICE or DESIGN TO
  RESOLVE; the owner's own words are not quoted in it. Only the OWNER - NEW points are recorded here as decisions.
- **The owner's new decisions (handback sections in brackets):**
  1. **QA is an independently managed experimental laboratory** (s1): not a replica of PROD and not a gate for PROD. It
     may hold exactly PROD's software, PROD's plus new variants or infrastructure, more or fewer variants, or different
     infrastructure, and be returned to a PROD-equivalent baseline when the owner chooses.
  2. **A new required operation: reset QA's installed SOFTWARE from PROD** (s2), owner-invoked, wipe-and-replace of
     QA's relevant software with what PROD has installed. PROD strictly read-only. QA keeps its own `ENVIRONMENT.ini`,
     `.venv`, role, root and backup location. No research data is copied by it.
  3. **Three operations, never conflated** (s1): (A) the QA software reset from PROD; (B) the complete research-data
     reseed from PROD into QA or DEV; (C) reset/replay in a chosen tree. None invokes another.
  4. **(B) is a required capability** (s3), its use manual and optional. **No passive-export mode.** Wipe-and-replace of
     the destination's active research data; no permanent reference or import folder. If "warn, ignore, continue"
     (entry 129) would need complex machinery, the owner may reconsider: Claude explains the cost first.
  5. **(C) must reconstruct ALL dependent scientific results consistently** (s4): scores, cumulative leagues and
     reports, pending forecasts, prevailing and exploratory OV-1; or say truthfully that results after N were cut and
     need a later catch-up. One confirmation.
  6. **`FORWARD_FROM` gets a descriptive name** saying it controls eligibility for the prevailing OV-1 (s5). Its PROD
     meaning (choice B, entry 130) is unchanged. **No extra prospective-boundary ceremony in QA or DEV;** their
     recomputations are sandbox and never claim to be formal prospective evidence.
  7. **R5-F04 CHANGED (s6): this supersedes entry 128 item 5 ("with none, the overwrite is refused").** A destructive
     infrastructure overwrite may proceed with no programmatic check that a backup exists or is verified. The tool
     shows a prominent warning asking the owner to ensure a valid backup exists, and asks for confirmation **defaulting to
     NO**; only an explicit YES proceeds. The warning covers: a failure may need a manual whole-tree restore from a
     backup he chooses (no automatic rollback); restoring an older backup reinstates exactly that state, with nothing
     later put back; a changed Python or `.venv` may affect usability or scientific equivalence; with no valid backup,
     recovery may not be possible.
- **Confirmed unchanged (s7):** choices A, C (the owner's own full ZIP of the E: project folder; no `Cold_Copy`; no second
  GitHub ZIP), D with R5-F01, F; R5-F02, R5-F03, R5-F05; every scientific safeguard.
- **The reviewer's dispositions of Claude's questions Q-a to Q-f (s8):** no material misattribution in S1 to S12 and D1 to
  D8; Q-f closed (no GitHub ZIP). The reviewer's advice and the DESIGN TO RESOLVE items are not owner decisions.
- **Open: Claude's clarifying questions to the owner of 21 November 2026, about 21:00,** before EX_266. EX_266 still
  needs the owner's explicit go (Fable, High).

## 136. 21 November 2026, 22:21 - the owner's directions from the reviewer's second handback (main `a8bcfaa`): DEV and QA run the installed science exactly as PROD does; a variant's status is visible beside its software; his answers to Claude's questions Q1 to Q4

- **Source and status.** `exchange/ChatGPT_to_Claude_QA_Scientific_Equivalence_Variant_Status_Q1_Q4_2026_11_21.md`,
  committed by the owner at `a8bcfaa` (SHA-256 `1e1a632239131ae89e13ee0ae060665e45b0eeda2ffcf99bf77ef0390e734713`), and
  his covering message in the Claude chat at 22:19. Not an EX, not a ratified design. It labels each point OWNER
  DIRECTION, REVIEWER RECOMMENDATION or DESIGN OPEN; only the first kind is recorded here as decided.
- **The owner's own words, in the Claude chat at 21:24 (what he had told the reviewer):** "Q1 (a) and (b) and (d) verify
  nothing crashes, including bugfixed etc OV1 calcs, before installing into prod. Part of the thinking is incorrect - If
  QA is a mirror of PROD (and at points it deliberately should be) then by definition no facility exists to make a
  clearly labelled sandbox prevailing OV1 ... it is a predecessor of prod undergoing testing or it isn't, and must not be
  a halfway mangled house." He clarified: "unless that house is in the process of verifying new things associated with
  the project experiments rather than extra software-admin overhead controls." On wording: "what is reset/replay this is
  not normal terminology, we have always referred to restoring from backups or walkforwards or catchups and we should
  strive for consistency to avoid ambiguity induced decisions and bugs."
- **Decided by the owner (handback sections in brackets):**
  1. **One science in every tree (s1, s5).** DEV and QA act on their installed software and their own
     `ENVIRONMENT.ini`, exactly as PROD does. No special QA version of the scientific software, no separate QA rules for
     OV-1, no QA-only eligibility mechanism, no extra administration because a tree is QA. QA's purposes: reproduce PROD
     when deliberately set up as its mirror; try new, corrected or changed methods and infrastructure (corrected OV-1
     calculations included); and check that everything works and nothing crashes, before an install into PROD. QA is
     still not a gate for PROD (entry 126).
  2. **No "sandbox prevailing OV-1" (s1, s5).** This withdraws the sandbox wording of entry 135 item 6 and of Claude's
     questions. What stays, in every tree alike: a result recomputed after its draw is known is never presented as a
     forecast recorded before it, and a copied record stays attributable to where it was computed.
  3. **Words (s2).** Restore from backup; catch-up; walk-forward. "Reset/replay" is not to be used. The handback's term
     for an owner-requested recomputation of past draws is "historical walk-forward rerun".
  4. **Same software and same status give the same behaviour in every tree (s2):** a variant withdrawn from draw 1601
     is treated identically in PROD, QA and DEV, in a catch-up and in a historical walk-forward rerun.
  5. **A variant's operational status is plainly visible in a human-readable file in the same folder as its installed
     software (s3).** In the handback's words for his: "A method's status is intrinsically tied directly to its software
     and must always be clearly visible in the same place its software is - no having to extra search outside places or
     inside unfindable-to-human files." Not buried in the forecast history, not in a registry elsewhere. **This
     supersedes the placement in entry 130 D (a `WITHDRAWN_FROM` line in the forecast file); the meaning of withdrawal,
     its effective draw and the keeping of earlier results are unchanged.** The scientific files stay immutable; an
     owner-authorised status change is a narrow, stated exception to "nothing in an installed variant folder changes",
     and it does not change the variant's scientific fingerprint.
  6. **Which operation carries a withdrawal (s4).** The status travels with the installed software: the QA software
     replacement from PROD brings each variant's status; the research-data reseeding does not change the destination's
     status files. This reverses Claude's Q3 recommendation of 21:00.
  7. **Backups at an install (s6).** (i) The usual pre-change whole-tree backup is still attempted before an
     infrastructure overwrite; a failure is reported plainly and is not a refusal. (Claude's "it costs nothing" was
     wrong: a backup takes time and space.) (ii) If the recovery kit cannot be written, the install no longer stops:
     a warning, a confirmation defaulting to NO, and YES proceeds; the same for an infrastructure reinstall. (iii) QA
     uses the same warning and confirmation as PROD, being the same software. (iv) No "newest backup" line in the
     warning; an on-demand, read-only list of backup ZIP paths may be useful, is not required, and verifies nothing.
  8. **EX_266 opens with a short traceability index** (his message, 22:19: "I agree with the suggestion"), and no
     further consolidated summary is written as a new authority.
- **Not decided (the reviewer's recommendations and DESIGN OPEN items; Claude's to design, the reviewer's to check):** the
  status file's name, format and integrity check; how its history is kept; where the first draw counted in the
  prevailing OV-1 is recorded and what it is called (the owner wants a descriptive name; entry 135 item 6); how copied
  lists that disagree with the destination's software or status are skipped and later recomputed; the exact file sets
  of the QA software replacement; the proportionate tests after an infrastructure change.
- **Confirmed unchanged (s7):** choices A, B, C, E, F; D's meaning; R5-F01, F02, F03, F05; the three separate
  owner-invoked operations of entry 135 item 3 (now named: QA software replacement from PROD; research-data reseeding
  from PROD; historical walk-forward rerun).
- **EX_266:** still subject to the owner's explicit go.

## 137. 21 November 2026, 22:47 - the owner's yes to Claude's three design intentions; the reviewer's assessment (pass in principle, four qualifications); THE OWNER'S GO FOR EX_266

- **The owner, in the Claude chat at 22:39 (his words),** on the three intentions Claude put to him at 22:25 (entry 136's
  continuity note): on the historical walk-forward rerun being part of the installed software in every tree, and in
  PROD only on its own explicit confirmation: "yes to this, in PROD it is an in-last-resort mechanism which may prove
  invaluable one day." On a withdrawal being one-way: "2. yes." On one status file per variant, written only by the
  project's commands, a hand edit detected: "3. yes." And: **"I think we can safely say GO for 266 now."**
- **Decided:** (1) the historical walk-forward rerun exists in DEV, QA and PROD alike; in PROD it is a last resort, run
  only by a separate, explicit owner command with a warning and a confirmation naming PROD; recomputed lines record
  that they were computed after the result was known. (2) A withdrawn variant stays withdrawn; a method comes back only
  as a new variant, or by restoring a backup made before the withdrawal. (3) One human-readable status file per variant
  beside its software holds, per game, the status and the first draw counted in the prevailing OV-1; it is written only
  by the project's commands and a hand edit is detected.
- **The reviewer's assessment, relayed by the owner in the same message (pasted; not a committed file): "PASS IN
  PRINCIPLE for proceeding to EX_266 design", with qualifications (its views; to be shown in EX_266):** a rerun is never
  started automatically by an infrastructure installation; original forecasts and prospective evidence stay
  distinguishable from results later corrected with newer software, and are not silently rewritten; a restore keeps
  its meaning (exactly the chosen backup, then the owner's catch-up, nothing later reinstated); the status file shows
  each game's status, effective draw, reason and eligibility draw, changes nothing in the scientific files or their
  fingerprint, and stays consistent with the installed-file checks, restores and walk-forwards; **an eligibility draw
  already established and copied from PROD into QA is preserved** (PROD's 1601 never becomes 1701 because QA received
  more results later). It recommends going straight to the complete EX_266, opening with the traceability index.
- **Go (design only):** EX_266, the corrected complete system specification and deployment design, for independent
  review. Fable (High). No code, install, run, backup, restore, copy or deletion is authorised.

## 138. 21 November 2026, 22:59 - the system specification DRAFT v0.4 and the deployment design DRAFT v0.10 sent for independent review (EX_266); no owner decision

- **Done under entry 137's go (Fable, High; design only, no code):** `exchange/CLAUDE_WEB_TOOLS/simplify/SYSTEM_SPECIFICATION_DRAFT_v0_4.md`
  (SHA-256 `e9a3befeda9382015dc1b0512040aee297937b5f2e2fc2e35a8333ac545c5358`) and
  `exchange/CLAUDE_WEB_TOOLS/simplify/DEPLOYMENT_DESIGN_DRAFT_v0_10.md` (SHA-256
  `3176998dfd2c04123f7ae7e1f26779363ee25111927b1770ebb7bd50999d5c39`), full new editions with exact diffs from v0.3 and
  v0.9 beside them (each diff applied by `patch` and compared byte for byte). Sent as `exchange/EX_266_Claude.md`, which
  opens with the traceability index (every owner decision of entries 122 to 137, every finding of EX_264 and request
  of EX_265 and the two handbacks, and every draft contradiction S1 to S12 and D1 to D8, each with its section).
- **The design, in short:** `VARIANT_STATUS.ini` beside each variant's software holds, per game, the withdrawal and the
  first draw counted in the prevailing OV-1 (`prevailing_ov1_first_eligible_draw`), each set once, written only by
  the project's commands, with a check line; the lists carry no status lines. One science in every tree: the same
  code, rules, warnings and questions; each line's envelope says where it was computed, whether its result was on
  file, and whether a rerun wrote it. A list that does not fit a tree's software or status is foreign: warned about,
  ignored, its variant held until the owner clears it. The job checks every score and the prevailing ledger in full
  at its start and withholds a game's derived results from the first differing draw. Infrastructure files have a
  class (forecast, derived, other); a reinstall says before overwriting what it would change, never recomputes
  history and never starts a rerun; `Check_Forecasts.bat --all` is the owner's to run. The historical walk-forward
  rerun (`Rerun_Walk_Forward.bat`) sets old lines aside in the tree, rebuilds every dependent result, leaves status
  files untouched, and is confirmed by typing the tree's role. The QA software replacement and the research-data
  reseeding each read PROD twice with every file hashed and never write it. Backups and the recovery kit are
  attempted and reported exactly, then one question defaulting to NO.
- **Mechanisms Claude chose where no decision exists, each with a leaner alternative (specification section 19; for
  the review and the owner's ratification):** a rerun sets aside in every tree; the derived check at every job; an
  infrastructure change that alters stored results is installable after a plain statement and YES (a change from v0.3
  and EX_262 section 2.3); in DEV an edited variant's list waits for a rerun; the suite runs in a target only when its
  infrastructure is DEV's.
- **Not done:** nothing was run; no timing is known; no independent cold read before sending (the reviewer's review
  is it).
- **Next:** the reviewer's reply, EX_267. Then corrections until PASS; the owner's ratification (RAT-40); H-1 v8.
- **Model (MC-1):** the Fable task is finished. Opus until the reviewer replies.

## 139. 21 November 2026, 23:11 - OWNER: the phase 1 file list is to be folded into the specification itself

- **The owner asked (23:09)** whether the restructuring of every method into the family and variant folder layout, with
  the Python import work that goes with it, in DEV first, is early in the new plan. **Claude's answer:** yes; it is
  phase 1, the first implementation step, in DEV only (specification v0.4 sections 3.2 and 17.3), after ratification,
  H-1 v8 and the owner's ZIP. Claude pointed out a weakness: section 17.3 only points to section 10 of the superseded
  simplification design v0.1 for the file-by-file list, and one line of that list is out of date ("installed in the E:
  clone by the existing procedure").
- **The owner's decision (23:10, his words):** "yes to folding the phase 1 list into the specification, corrected, in
  the revision that answers the reviewer's EX_267, so the \"complete\" specification really is complete on this point."
- **To do, in the revision that answers EX_267:** specification section 17.3 gains the corrected phase 1 list (E_2 to
  E_19: `contract.py` and the family's own modules become the family's core file, one folder per variant with
  `method.py`; E_1's adapter becomes `E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py`; the three shared helpers move to
  `_shared/` with `_v1` names; imports follow, tests included; the runner's table of methods is built from the folder
  tree), with the phase 2 list checked at the same time, and the pointer to the design v0.1 removed.

## 140. 21 November 2026, 23:24 - EX_267 (R-6 RECHECK of the specification v0.4 and the deployment design v0.10: R6-F01 to R6-F07, N01 to N06) read and recorded; Claude accepts all seven; one owner decision is needed (R6-F01)

- **Source.** `exchange/EX_267_ChatGPT.md`, committed by the reviewer's route at main `2fae39e` (SHA-256
  `d54a3c4ab5c4a7161b98307092b546d404ba4e00436485cc29377619768d51c1`). It confirms the four member hashes of EX_266.
  **Disposition: RECHECK.** It passes in principle: one science in every tree; the status file and one-way withdrawal;
  the two read-only copies from PROD; manual rollback; the testing direction; no automatic rewrite of history at an
  install; the traceability index (P01 to P07).
- **The findings (the reviewer's; none is an owner decision):**
  - **R6-F01:** specification 12.4 lets one ordinary YES install an infrastructure change that is known to change the
    FORECASTS of an existing variant. A variant's fingerprint does not cover the shared code its forecast passes
    through, so the same name would then mean two different forecasters. Correcting derived results (scores, OV-1)
    from stored forecasts is a different and acceptable case. The reviewer objects to the first without a separate,
    explicit path, and says that if a policy choice is involved it goes to the owner with its consequence stated.
  - **R6-F02:** say exactly which fields the derived check compares (scientific content, not the provenance that
    legitimately varies, such as the results file's hash at scoring time or a code digest); and stop reports that are
    no longer current from sitting in the active reports folder looking current.
  - **R6-F03:** the rerun's modes need exact, separate sets of files they may change; as written, a derived-only rerun
    could be read as shortening forecast lists, which would replace a forecast made before its result was known.
  - **R6-F04:** the installed-file list holds status files by name only, yet the QA software replacement says every
    listed file is hashed against the list; a status file changed during the copy could pass unnoticed.
  - **R6-F05:** the destination of a reseeding (and of the QA software replacement) is checked to be quiet long before
    its barrier is written; a job started in between could have its data removed under it.
  - **R6-F06:** specification 12.3 makes any derived difference a stop, while 12.4 allows an accepted correction that
    is known to differ: the two contradict each other.
  - **R6-F07:** a withdrawal must be serialised against a running job and a results step, so that the draw shown to
    the owner is still the right one when the status file is written.
  - Notes N01 (file classes are hints; when unsure, class a file as forecast), N02 (a held cohort member blocks the
    prevailing line: say so plainly), N03 ("NO changes nothing" is not literally true: a backup ZIP and a log line
    may have been written), N04, N05, N06 (measure the costs in the rehearsal).
- **Claude's assessment, given to the owner at once:** all seven are right and are accepted; each has a small
  correction that adds no administration. R6-F01 needs the owner: what the system does when a correction to shared
  forecasting code would change what existing variants forecast. His own direction of entry 122 item 4 already says a
  changed shared helper must not change an earlier variant and that only behaviour-invariant infrastructure stays
  shared; the open point is the exception for a real defect in code that cannot be versioned per variant.
- **Held for the owner's answer on R6-F01 and his go (MC-1: Fable, High):** EX_268, the specification v0.5 and the
  deployment design v0.11, with a disposition table for R6-F01 to F07 and N01 to N06, and the phase 1 file list of
  entry 139. No code.

## 141. 21 November 2026, 23:50 - R6-F01: the owner's preference, conditional on the reviewer's and Claude's agreement: correct defective shared code in place, then recompute ("the brute-force slipstream")

- **The owner, in the Claude chat at 23:42 (his words), on R6-F01:** "I tried to argue this case R6-F01 with previous chats
  but did not prevail, I wanted to make it easy by a slipstream fixed code and then everything gets fixed, but the nub
  of it is different forecasts etc may arise ... the problem is not only global shared code across methods but also
  shared code within a family having the same issues. there is no good answer perhaps other than the brute-force one
  which is not such a bad idea after all : slipstream the fix, delete all data/reports perhaps except draws dataset and
  walk-forward recalculating everything on the basis it is only history anyway - from then on everything is good".
- **Claude's assessment (23:45):** sound, and better than the "marked correction" Claude had recommended, which is
  withdrawn. It leaves no mixed history, so one name is again one forecaster; it is the historical walk-forward rerun
  already designed, plus one rule: after a correction to shared code nothing affected counts until the rerun is done.
  Costs told to him: in PROD, past draws lose their made-before-the-result character, shown in the reports' counts;
  the computing time is unmeasured; it is for a defect, not for a changed idea (which still means successor variants).
  Claude recommended setting the old lines aside, not deleting them.
- **The owner, at 23:50 (his words):** "I think sub-question recommended option (a) to the brute-force slipstream fix
  method for fixing global helper code and family shared code. Unless someone finds a good reason not to, I like the
  easiness and shape of the brute force slipstream approach. We would still retain [Who_Uses.bat, Make_Successors.bat,
  batch marking, unmarking and withdrawal] since one day we'll need them. ... if chatgpt agrees and you agree then we
  fold it into the design."
- **Status: a stated preference, conditional.** Claude agrees. It becomes a decision when the reviewer has given its
  view and the owner confirms. **If confirmed it replaces entry 127 item 3 for defects** ("no in-place update of an
  installed helper"): defective shared code (system-wide forecasting code, `_shared` helpers, a family's core file)
  is corrected in place by its own explicit command and confirmation, never by the ordinary install question; every
  variant it can affect is held until the owner runs the walk-forward rerun over its whole history; old lines are set
  aside; the names stay. Unchanged: a variant's own files never change (a corrected method is a new variant); a
  changed idea in shared code is a new versioned helper with successor variants; the three DEV conveniences stay.

## 142. 22 November 2026, 00:12 - the reviewer supports the owner's R6-F01 preference (handback at main `dd39845`); the OV-1 timing point re-closed; a correction archive ZIP; the owner's explicit confirmation is awaited

- **Source.** `exchange/ChatGPT_to_Claude_R6_F01_Slipstream_Correction_OV1_Reclosed_2026_11_22.md` (main `dd39845`; SHA-256
  `78547cd90144db934219e986378b05717944b98201f94a0ffeba104148d90c8c`); not an EX, not a ratified design. Relayed by the
  owner at 00:11.
- **The reviewer's position (its views):** SUPPORT for "correct defective shared code in place, then recompute by a
  historical walk-forward rerun", as a narrow exception for genuine defects in shared forecast-producing
  infrastructure, `_shared` helpers and a family's shared core. Its conditions for EX_268: the affected variants are
  every one whose forecast CAN depend on the corrected code (when unsure, include it); held means truly not current;
  the whole history of the AFFECTED variants is recomputed and every dependent game-level result is rebuilt, while
  unaffected variants' forecasts are kept; names stay and fingerprints honestly change, and corrected forecast-class
  infrastructure must make old lists incompatible by a persistent identity check even if a sample happens to match;
  it is never a route for a changed idea; its own science-specific warning and confirmation; no correction mark in
  the status file, which a correction never resets; nothing half-corrected is runnable.
- **OV-1, recorded so that it is not reopened:** the reviewer had added a condition (C2) that a recomputed prevailing
  OV-1 could not carry the conditional 2.5% statement merely because it was computed after the draws. The owner
  objected that this was settled; the reviewer withdrew C2. The established position stands: the time of execution
  is not by itself a condition of the bound; the claim stays conditional as specification 10.6 words it; one engine
  in every tree; truthful provenance. No new rule, mode or start ceremony.
- **The owner's suggestion, relayed in the handback:** superseded results are saved in a very clearly named ZIP before
  anything is deleted or recomputed. The reviewer supports one verified ZIP with a small readable manifest per
  correction, made before any active record is shortened; if it cannot be made or verified, nothing is shortened. It
  is not a whole-tree backup. The reviewer corrects Claude's phrase "past draws lose their made-before-the-result
  character": the original forecasts keep that property, in the archive; the replacements are the retrospective ones.
- **The owner, 00:11 (his words), on the process:** "I am forming a view that we may be starting to enter a phase which
  may be useful but delaying actual design and development, correcting things that maybe should have been decided
  better in the past. ... We all have spent most of our time (literally) on this project examining non core experiment
  matters."
- **Awaited from the owner:** his explicit confirmation of the defect-only exception to entry 127 item 3 (entry 141
  recorded a conditional preference; Claude and the reviewer now both support it). Then EX_268 on his go.

## 143. 22 November 2026, 00:16 - OWNER DECISIONS: the defect-only correction of shared code in place (replaces entry 127 item 3 for defects); the four-step build order; EX_268 to proceed

- **The owner, in the Claude chat at 00:14 (his words),** to Claude's two questions: "1. yes. 2. yes. I am just keen to get
  on with it. blurb given to reviewer now."
- **Decided (1): the correction of defective shared code in place** (entries 141, 142; the reviewer supports it).
  Defective shared code (forecast-producing infrastructure, `_shared` helpers, a family's core file) is corrected in
  place by its own explicit command and confirmation, never by the ordinary install question. Every variant the
  corrected code can affect is held until the owner runs the historical walk-forward rerun over its whole history;
  what the rerun replaces is first saved in a verified, clearly named ZIP; the names stay. **This replaces entry 127
  item 3 ("no in-place update of an installed helper") for defects only.** Unchanged: a variant's own files never
  change (a corrected method is a new variant); a changed idea in shared code is a new versioned helper with
  successor variants, old and new both running; `Who_Uses.bat`, `Make_Successors.bat` and batch marking, unmarking and
  withdrawal stay.
- **Decided (2): one ratified design, built in four steps, each on its own go:** (i) the folder layout (phase 1);
  (ii) the research engine in DEV (the lists, the job, scoring, the reports, both OV-1 scores, the status file and
  withdrawal); (iii) trees, installs, backups and restore, so that PROD exists and forecasts every week; (iv) the
  laboratory tools (the QA software replacement, the research-data reseeding, the rerun, the correction).
- **Go:** Claude takes "I am just keen to get on with it", after his "address the findings in the usual exchange
  process" of 23:22, as the go for EX_268 (Fable, High; design only) and has told him so.
- **Claude's closure plan for EX_268 (so that it is not lost if this chat ends; design intentions, not decisions):**
  R6-F01: a new command `Correct_Shared_Code.bat`; every list's header records the identity of the shared forecasting
  code (the digest of the manifest's `forecast`-class files) beside the variant's fingerprint, and a list whose header
  does not match what is installed is foreign and held; the ordinary infrastructure reinstall refuses any plan that
  changes a `forecast`-class file. R6-F02: the derived check compares a defined list of scientific fields only; one
  small cutoff file per game says from which draw derived results are not current, and report files from that draw on
  are moved out of the active reports folder. R6-F03: a table of exactly which files each rerun mode may change;
  derived-only changes no forecast byte and takes only a game and a first draw; every rerun first writes one verified
  archive ZIP of what it will replace, and does nothing if that fails. R6-F04: every file read from PROD, status files
  included, hashed at the first reading and again at the second; "no program writes to PROD", with Windows'
  last-access times named as outside that promise. R6-F05: the copy takes the destination's job lock before reading
  PROD and holds it to the end. R6-F06: an unexpected derived difference stops; an accepted, named derived correction
  is reported and leaves those results not current. R6-F07: a withdrawal holds the job lock and the updater's lock
  from display to write. Also: the phase 1 file list (entry 139) and the four-step build order in section 17.

## 144. 22 November 2026, 00:21 - the reviewer agrees the archive ZIP and the build order, with two safeguards; the owner's go; EX_268 sent (the specification DRAFT v0.5 and the deployment design DRAFT v0.11)

- **The reviewer's assessment, relayed by the owner at 00:18 (pasted; not a committed file; its views):** AGREE with one
  verified ZIP before a historical recomputation, replacing the set-aside folder, and with the four-step build order.
  **Two safeguards:** the original bytes of corrected shared code are preserved before they are overwritten, since the
  rerun's ZIP is made later; and an interrupted rerun keeps and reuses its first verified archive, never archiving
  records already shortened. Also: a defect found before the correction tools exist is stopped or held, not
  improvised around; the OV-1 timing question stays closed.
- **On priorities, in the same message (the owner's observation, which the reviewer shares):** disproportionate time has
  gone to peripheral operational mechanisms; from here KISS, practical implementation and measured testing, with
  review effort on scientific correctness, data integrity, reproducibility and material safety; no new
  administrative machinery, speculative edge-case process or decision round without shown practical need. "The aim is
  a scientifically credible, functioning research system - not an indefinitely refined deployment framework."
- **The owner's go (his words):** "IF YOU THINK IT ALIGNS WITH MY INTRENT THEN LETS GET ON WITH IT." Claude judged that it
  does and proceeded.
- **Done (Fable, High; design only, no code):** `exchange/CLAUDE_WEB_TOOLS/simplify/SYSTEM_SPECIFICATION_DRAFT_v0_5.md`
  (SHA-256 `19999abf697ec522ad9ad6bf10723de0793c4c06ca77e8f716a5eb2f556e5b28`) and
  `exchange/CLAUDE_WEB_TOOLS/simplify/DEPLOYMENT_DESIGN_DRAFT_v0_11.md` (SHA-256
  `9b7911ee10aaae703a6e83b98af57f9cbf26471fc286b3ce1aa80d248e7e4711`), built from v0.4 and v0.10 by counted replacements,
  with exact diffs (each applied by `patch` and compared byte for byte). Sent as `exchange/EX_268_Claude.md`, which
  opens with the disposition of R6-F01 to R6-F07, N01 to N06, the handback's conditions and the two safeguards.
- **What changed, in short:** a new command `Correct_Shared_Code.bat` (specification 12.8; deployment 6C); every list's
  header holds the identity of the shared forecasting code as well as the variant's fingerprint, so a list made
  under other code is foreign and its variant held; the ordinary infrastructure reinstall refuses a plan holding a
  `forecast`-class file; the derived check compares a stated list of scientific fields, and a cutoff file
  (`NOT_CURRENT_FROM.json`) with stale reports moved out of the active folder marks what is not current; a table of
  what each rerun mode may change (derived-only changes no forecast byte); one verified, clearly named ZIP before any
  rerun replaces anything; both copies from PROD take the destination's job lock first and hash every PROD file,
  status files included, at two readings; a withdrawal holds the job lock and the updater's lock; the phase 1 file
  list (17.3) and the four-step build order (17.4).
- **Next:** the reviewer's recheck, EX_269. After a PASS: the owner's ratification (RAT-40), H-1 v8, the owner's ZIP of
  the project folder, then build step 1. **Model (MC-1):** the Fable task is finished. Opus until the reviewer replies.

## 145. 22 November 2026, 12:59 - EX_269 (R-7 RECHECK: four focused corrections) read; all accepted; EX_270 sent (the specification DRAFT v0.6 and the deployment design DRAFT v0.12); no owner decision

- **EX_269** (`exchange/EX_269_ChatGPT.md`, main `5d22683`; SHA-256
  `ea7badb1a8ae2e2160e1b971bbd3c852d2be01775d9221f2f3550b67c9284581`): RECHECK, substantially favourable. It accepts the
  correction of shared code, the header identities and the hold, the compared fields and the cutoff file, the mode
  table, the copies from PROD, and "any forecast-class change holds every variant until a rerun" as the current
  rule. Four findings: R7-F01 a rerun stopped at draw N left a cutoff that the ordinary job could never clear; R7-F02
  a change to report code, and the QA software replacement, could leave stale reports in view; R7-F03 a continued
  rerun could shorten lists a second time; R7-F04 an ordinary install had a gap between its quiet check and its
  barrier. Notes N01 to N04. It asks for no science-policy decision; OV-1 stays closed; the build order stands.
- **The owner, relaying it at 12:56:** "Please read EX_269 in full and address these using the existing cutoff, barrier
  and job-lock mechanisms. ... The objective is to achieve a scientifically correct, implementable design and move into
  development without further unnecessary design rounds."
- **Done (design only; counted changes; no new mechanism):** `exchange/CLAUDE_WEB_TOOLS/simplify/SYSTEM_SPECIFICATION_DRAFT_v0_6.md`
  and `exchange/CLAUDE_WEB_TOOLS/simplify/DEPLOYMENT_DESIGN_DRAFT_v0_12.md`, with exact diffs from v0.5 and v0.11; sent as
  `exchange/EX_270_Claude.md` (hashes in its member table). The cutoff file has two reasons (`MISMATCH`;
  `AWAITING_CATCH_UP`, which the ordinary job catches up and clears); print-outs are made again when report code
  changes; the QA software replacement and the reseeding mark what is not current before they release the tree; the
  rerun's barrier holds a stage so that lists are shortened once; an ordinary install takes the target's job lock
  with a fresh process check before it changes anything; one archive ZIP for each game.
- **Next:** the reviewer's recheck, EX_271. After a PASS: the owner's ratification (RAT-40); H-1 v8 and, on Claude's
  advice, a new Claude chat; the owner's ZIP of the project folder; build step 1.

## 146. 22 November 2026, 13:17 - EX_271: the reviewer's PASS (DESIGN) of the specification DRAFT v0.6 and the deployment design DRAFT v0.12; the ratification decision (RAT-40) is put to the owner

- **EX_271** (`exchange/EX_271_ChatGPT.md`, main `7492846`; SHA-256
  `a80f1b61ed04938510a272ec9d6f0e5fcdb9ebbddb27113edab39dc947b8ca10`): **"PASS (DESIGN), with one non-blocking
  implementation oracle. No further design recheck requested."** R7-F01 to R7-F04 and R7-N01 to N04 each PASS; the
  correction of shared code, the identities and the hold, and the closed OV-1 question stand. It confirms the member
  hashes of EX_270. It is a pass of a design, not of tested code.
- **The one oracle to carry into build step 4 (EX_271 section 3; not a ratification blocker):** after a QA software
  replacement or a research-data reseeding, the report files in the active folder must be right for the destination
  or plainly not current as soon as the command returns, without a research job being run first, including when
  only the report code or a variant's status differs and every number agrees. To be shown with the existing render
  and move routines; no new mechanism.
- **The reviewer recommends** the owner's consideration of RAT-40, then the four build steps, each on its own go.
- **Passed for ratification:** `exchange/CLAUDE_WEB_TOOLS/simplify/SYSTEM_SPECIFICATION_DRAFT_v0_6.md` (SHA-256
  `9c2cab96954a14ba53e3fedf16e2ad7371577c0a6a6ecaa23882b1f018a7e5e5`) and
  `exchange/CLAUDE_WEB_TOOLS/simplify/DEPLOYMENT_DESIGN_DRAFT_v0_12.md` (SHA-256
  `e20143102185cdf24a13b74baae8e279328000d164dda2c180a9a3c205e35714`).
- **Not a decision:** ratification is the owner's. Claude has put to him what RAT-40 would cover and what it would not
  authorise.

## 147. 22 November 2026, 13:34 - RAT-40: THE OWNER RATIFIES the system specification v0.6 and the deployment design v0.12, with notes: warnings, coding practices, a light tidy-up of the existing method files

- **The owner's words.** At 13:22, on the mechanisms Claude had chosen: "ok as long as a warning message is emitted at the
  right place" (for "any change to shared forecasting code holds every variant until a full rerun" and for "results
  made under edited code wait for a rerun command"); and: "both are nearly ratified pending agreement on these
  clarifications and notes about good coding practices." At 13:26: "lets briefly explore good coding practices, eg good
  commenting inside code eg outlining the purpose of the .py and list any of our developed dependencies and what they
  are used for, each function or self-contained block of code has good commenting clarifying in english what is
  happening, good variable naming aligning with its purpose with minimal generic naming". **At 13:33:** "also good use of
  constants which are declared at or near the top of the PY and well commented and parameters well commented, and
  function returned data well commented with a good example, checks for critical data not found from .ini file(s) etc,
  meaningful error messages saying what occurred where and why and advising likely what to do about it. yes to a light
  tidy-up of the existing method files after step 1 is proved and before anything is installed into QA or PROD. yes to
  yes, kept light. If you think of any more light-touch good coding practices let me know otherwise ratified now."
- **RAT-40 (22 November 2026, 13:33).** Ratified, after the reviewer's PASS (DESIGN) in EX_271 (entry 146): the system
  specification v0.6 and the deployment design v0.12, each the reviewed candidate with its status paragraph alone
  changed, placed by Claude in `doc/` (SHA-256 of the installed files):
  `doc/Predictive_Randomness_System_Specification_v0_6.md` `ee7199d0c17e8bcf877d49e25c6db1a009105c3f8da75ff1ec28b15726216ad0`;
  `doc/Predictive_Randomness_Deployment_Design_v0_12.md` `e9f778d86c0c1a8a73bfbebf21982aec897a3afdb1296c3029f2ba1da9b58b3d`.
  The ratification covers what Claude set out to him at 13:16 (entry 146's reply): the two documents as the one
  authority, the earlier design documents as history with their science kept by reference (specification 1.2, 1.3);
  the orphan-marker exception at a restore, which amends Architecture 5C by ratification (deployment design 12); the
  mechanisms of specification section 19; the four-step build order (17.4).
- **The notes of ratification (binding on the code):**
  1. **Warnings.** Wherever variants are held or results are not current, the job says so plainly at its start and at
     its end, names the cause, and gives the exact command to run.
  2. **Coding practices:** `doc/CODING_PRACTICES_v0_1.md` (SHA-256 `d64f0101a4fdb21998b2871765bd9b3f06ccb6c7409c7a2d0e9f230cebbd7ddd`), his points set out as a one-page checklist;
     two items added by Claude at his invitation are marked there and may be struck by him.
  3. **A light tidy-up of the existing method files** after build step 1 is proved and before anything is installed
     into QA or PROD: headers, dependency lists, comments where plainly missing; no calculation changes; the
     equivalence check run again. (A variant's files can never change once installed.)
  4. **EX_271 section 3's oracle** is owed in build step 4.
- **Clarified by Claude before he ratified (no document change):** no tree behaves differently from another, DEV
  included: the "wait for a rerun" rule is the same everywhere; and the test suite is run against a tree only when
  that tree's system code is the same as DEV's, because the tests live in DEV and belong to DEV's system code.
- **RAT-40 authorises no code, source move, install, tree, run, copy, backup or restore.** Next: H-1 v8 (and the
  reviewer's own H-2 edition); whether build step 1 starts in this chat or a new one; the owner's ZIP of the project
  folder when Claude says it is time; build step 1 on his go. The next ratification number is RAT-41. The
  ratification register's next edition (v0.32) is still to be written; until then this entry is the record.

## 148. 22 November 2026, 13:51 - the H-1 v8 CANDIDATE and its blurb written on the owner's go; the reviewer's own H-2 v4 candidate noted; no owner decision beyond the go

- **The owner's words.** At 13:36, on Claude's paste block for the reviewer: "ok. does the blurb also mention for chatgpt
  to fully update its handover docs now as you will be doing yours next ?" Claude gave him a firmer block asking the
  reviewer to update its own handover fully now, at this milestone. At 13:37: "yes please H-1v8 now while I paste that
  to chatgpt".
- **Written (candidates; not reviewed, not ratified; they authorise nothing):**
  `exchange/CLAUDE_WEB_TOOLS/h1v8/out/Claude_Primary_Handover_H1_v8.md` (SHA-256 `983f27ec645a7b22083f7f4a19493306b55323ac626d2ecc10b77174e71a1ae5`; 109698 bytes; US-ASCII, LF) and
  `exchange/CLAUDE_WEB_TOOLS/h1v8/out/Claude_Primary_Handover_H1_v8_introductory_blurb.md` (SHA-256 `586ececea64fca65b1ef3872a9fec60f1d7c659e0da408eb61e62d996d556d66`), built by
  `exchange/CLAUDE_WEB_TOOLS/h1v8/make_h1_v8.py` (`241b866fff4545067a4fb4d3601c875d4f651ba4fef882dd83b0db5c34cb29a0`) from `H1_v8_template.md` (`e75f0cf6bd01f3180968811b9fe026ea8d971247b9d91d98b5d225443fe01d51`) beside it.
- **What kind of edition.** A full edition, restructured and shortened (H-1 v7r1 section 8.5 allows it), for the system
  ratified as RAT-40. H-1 v7r1's sections 1, 2 and 2A (the roles, the reviewer's rights, the review procedure, the Git
  rules, the owner's working preferences and his foundational points) are carried byte for byte, with a short list
  of where they are out of date placed before them; 34 further single lines are carried whole from v7r1 (the results
  source, the scientific contract, process safety, the dependency rule that specification section 13 cites as "H-1
  5.4", verified technical facts). Everything else is rewritten around the three ratified `doc/` files, by pointer.
  Its Appendix B lists, section by section, what was dropped and where it now lives, and what Claude did and did
  not re-read or verify. The blurb is the blurb of 21 November 2026 with counted changes; the owner's hard rules are
  his words, unchanged.
- **Also committed with it:** the builders of the last three editions of the design, which had been only in the
  cloud workspace: `exchange/CLAUDE_WEB_TOOLS/simplify/build_v0_4_v0_10.py`, `build_v0_5_v0_11.py`, `build_v0_6_v0_12.py`, with
  `spec_v0_4_template.md` and `deploy_v0_10_template.md`. Run again before committing, the three reproduced the committed
  drafts v0.4 to v0.6 and v0.10 to v0.12 with no byte changed.
- **The reviewer's handover.** While this was being written the reviewer committed its own full edition current to
  RAT-40: `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md` (SHA-256 `d537263c02acbc69e787d17cb715e2d8e1768e4a7e40f3a699eba2f06ba7c828`; main `30826be`) and
  its blurb (main `18ce192`). A candidate until the owner ratifies it. Claude read its section 0 only: it states the
  position, the four notes of ratification, the build order and the next numbers as Claude's records do. H-1 v8
  names it in its section 4.4.
- **Not an EX message** (the owner's rule: an EX only when he asks). The candidate goes to the reviewer by a pointer in
  the owner's paste; the reviewer replies as the owner directs.
- **Next:** the reviewer's review of the H-1 v8 candidate; the owner's ratification of it (and of H-2 v4, as he
  chooses); installation in `doc/HANDOVER/` with only the status paragraph changed; then his choice of chat for build
  step 1, and his ZIP when Claude says. The next EX is EX_272; the next ratification is RAT-41.

## 149. 22 November 2026, 14:02 - EX_272: the reviewer's PASS of the H-1 v8 candidate with one pointer correction (FIX AND PROCEED), applied exactly; the owner decides a new Claude chat after v8 is ratified

- **EX_272** (`exchange/EX_272_ChatGPT.md`, main `63dfeb0`, SHA-256 `eea85a848c32a8d212d0f2793c3d000f967ea71edc07f67b9a4d36555cc3592a`), relayed by the owner at 14:00. Disposition: "H-1 v8:
  PASS WITH ONE NARROW DOCUMENTARY CORRECTION, assigned REVIEWER-DECIDED FIX AND PROCEED". The reviewer verified the
  102-line carried region and all 34 carried lines against H-1 v7r1, and the candidate, blurb, builder and template
  hashes. Appendix B, section 0C note 7, sections 5.2 and 5.3, the build order and the blurb passed. No further full
  review of H-1 is asked for. The OV-1 timing question stays closed.
- **H1-v8-C01, applied exactly as worded.** In section 4.4 only, "commits `30826be` and `18ce192`, with its blurb" became
  "commits `30826be` (full candidate) and `6316767` (current introductory blurb)". Made in the template; rebuilt by the
  builder against the reviewed commit `4967598`; `diff` of the old and new candidate shows those two lines and nothing
  else; the blurb is byte-identical. **The corrected candidate:**
  `exchange/CLAUDE_WEB_TOOLS/h1v8/out/Claude_Primary_Handover_H1_v8.md`, SHA-256 `9e8717cd758caf2e6e075b86911619bf0e04d67ec8c418347c32741ae172d335` (109,728 bytes); the blurb unchanged,
  `586ececea64fca65b1ef3872a9fec60f1d7c659e0da408eb61e62d996d556d66`; the template now `51b1f09ca426631515cd24ffaf915ab0ab164558e6453fc70623cf28f44d993f`. The earlier candidate (`983f27ec...1a1ae5`) is in Git at `4967598`.
- **An observation, not acted on (outside what was authorised).** EX_272 says H-1's Appendix A "already names the
  current H-2 blurb hash". It does not: Appendix A's row for the H-2 v4 blurb holds `436f0814...116cf3`, the bytes at
  `18ce192`; the blurb at `6316767` is `24ecfd6cb517ca11a2af9ead57229e9adba44b6d0d7ef25ebf9708a03abc2d75`. Appendix A's list of commits also still says `18ce192`. And the
  reviewer's own owed clarification of H-2 v4 (R-8 to R-11 already owner-ratified, 27 October 2026) will change the
  H-2 v4 file's hash, which section 4.4 and Appendix A cite. Claude's suggestion, put to the reviewer through the
  owner: once the reviewer has corrected H-2 v4, one build of H-1 v8 against that commit, changing only the H-2 v4
  identifiers (two hashes and the commit names), reported with its exact diff. Until the reviewer authorises that,
  nothing more is changed.
- **Also recorded by the reviewer in EX_272, about its own file:** H-2 v4 needs a clarification outside its protected
  rights text that R-8 to R-11 are already ratified. H-1 v8's section 1.4 states that correctly. Not an H-1 defect.
- **The owner's words, 14:00:** "\"Chat for build step 1\" ok yes a new Claude chat to be created once v8 is ratified.
  Register v0.32 I'm unsure what you are asking ... as long as it is up to date now using your experience then yes
  to your recommendation."
- **DECIDED (owner):** a new Claude chat takes over once H-1 v8 is ratified; build step 1 starts there.
- **Not yet settled: register v0.32.** Claude's question was unclear to him. The fact: the register in `doc/` is v0.31
  and does not hold RAT-35 to RAT-40; the decision log holds them all and is up to date. Claude puts the question
  again in plain words (write a short v0.32 now, in this chat, to travel with the handovers; or leave it to the
  first code package).
- **Next:** the reviewer's correction of H-2 v4 and its answer on the pointers; then the owner's ratification of both
  handovers (RAT-41), installation in `doc/HANDOVER/` with the status paragraph alone changed, and the new chat.

## 150. 22 November 2026, 16:56 - the register v0.32 CANDIDATE written at the owner's choice (option 1); the reviewer's correction of H-2 v4 noted; one practical point for the build recorded

- **The owner's words.** At 14:07, after Claude put the register question again as three options: "yes Register v0.32
  option 1 please now." (Option 1: Claude writes a short v0.32 now, in this chat, to go to the reviewer with the
  handovers.) The work was interrupted; at 16:53: "please continue".
- **Written (a candidate; not reviewed, not ratified; it authorises nothing):**
  `exchange/CLAUDE_WEB_TOOLS/register/RATIFICATION_REGISTER_v0_32.md` (SHA-256 `2fd091f34ea47399693b30f51b2a677d3d4cf348d028435cbd9639366d99135c`; 369666 bytes), built by `make_register_v32.py`
  (`f786db005a7dee0bd6536ca8fbbd0990a08574821971b4089014a3baff510858`) from the installed register v0.31 (`c6369a72...3cae6d`, asserted) by two counted insertions: the version line, and one
  new section, `register_v32_section.md` (`c3cdb445376973fa8c96ed650f7b7f4a2487717825e72bf7c3ba76c1a11a6031`), placed before "Interpretation and verification". Nothing of v0.31 is
  changed or removed. `REGISTER_v0_31_TO_v0_32.diff` (`5137f365ba8dbf48c462f9d5ef3df45e0547a50e45aa7b33a465e33449d0634b`) is exact (applied to v0.31 with `patch` and compared with `cmp`):
  one line replaced, 162 added.
- **What the new section holds, kept short:** the position at this edition; a table of RAT-34's install to RAT-40 with each
  entry and commit; twelve numbered items indexing entries 62 to 150; RAT-40 with its four notes; what is carried into
  the build; the out-of-date statements (above all, which documents specification 1.3 makes history and which clauses
  1.2 keeps); a table of 27 file hashes filled from Git by the builder; and the future actions. Checked by tool: every
  hash the decision log recorded for those files equals the builder's; every commit named exists; an EX file exists for
  every number from 216 to 272; `cc665ce` holds ten record files and `.gitignore`.
- **A practical point found while writing, recorded in the register and NOT a decision.** The owner decided on
  18 November 2026 (entry 92, decision 2) that the two Mode H archive checks left in the installed code be removed; that
  was for the MHUP-B package, which was not built. Checked today in the installed code: the opening record
  `source_data/HOLDOUT_OPENED_<GAME>.json` is still consulted by `src/methods/_common/master_versions.py` and
  `contract_dispatch.py`, and the updater `src/results_master_v0_2.py` refuses an update for a game without one. The
  ratified specification and deployment design do not name that record. So build steps 2 and 3 must settle, in their
  own packages, how reused code treats it and whether a new tree's `source_data\` holds it. **H-1 v8 does not carry
  this point;** Claude proposes adding one line (below).
- **The reviewer corrected its own H-2 v4 candidate** at 14:08 and 14:09 (main `23f02d6`, `9f99c76`): a clarification, outside
  the protected rights text, that R-8 to R-11 were already owner-ratified on 27 October 2026; and its blurb refreshed.
  The files are now `e24481b7dd088edef35080a8d98252f3da3114826c2b510589b048b7660b3c75` and (blurb) `2f93f042b81e6e3de7614ffe53119c47fb9bcb2395c99c80b7bb33454cf38768`. **So the H-2 v4 hashes inside the H-1 v8 candidate are stale** (section 4.4
  and Appendix A; as entry 149 foresaw). The register candidate cites the current ones.
- **Proposed by Claude, waiting for the reviewer's authorisation and the owner's word; nothing changed yet:** one rebuild
  of the H-1 v8 candidate that changes only (a) the H-2 v4 identifiers (two hashes, the commit names); (b) the four
  statements that say register v0.32 is still owed (section 0A item 3, section 0C note 4, section 4.4, section 12.8
  item 6); (c) one added line carrying the opening-record point into section 10. Reported with its exact diff.
- **Not an EX message** (the owner's rule). The register candidate goes to the reviewer by a pointer in the owner's paste.
- **Next:** the reviewer's review of the register and its answer on the H-1 v8 rebuild; then the owner's ratification of
  the register and both handovers (the next free number is RAT-41), their installation in `doc/`, and the new Claude chat.

## 151. 22 November 2026, 17:08 - correction of a count in entry 150 (found by the reviewer): the register diff adds 174 lines, not 162

- **The reviewer's interim finding, relayed by the owner at 17:07:** "I found a small count discrepancy in Claude's
  description: the diff shows 174 net added lines, not 162."
- **The reviewer is right.** Recounted with `git diff --no-index --numstat` and `wc -l`: register v0.31 has 2,490 lines and the
  v0.32 candidate 2,664; the diff removes 1 line and adds 175 (the replaced version line, and the 174 lines of the new
  section, 13 of them blank). Net: 174 lines added. Entry 150's "one line replaced, 162 added" should read "one line
  replaced, 174 lines added".
- **Cause (Claude's):** the count was taken with a pattern that matched only added lines with text on them, so the 13
  blank lines of the section were not counted. The same wrong figure went into Claude's chat reply and its paste block
  for the reviewer.
- **No file is affected.** The register candidate, its section, its builder and its diff are unchanged
  (`2fd091f3...6d99135c`); the diff is exact, as proved by `patch` and `cmp` in entry 150. Only the description was wrong.
- **Lesson, kept:** count with the tool that counts what the sentence says (`--numstat` for "lines added"), not with a
  hand-made pattern.

## 152. 22 November 2026, 17:29 - EX_273: the register v0.32 candidate PASSED (documentary); the authorised final rebuild of H-1 v8 made; the register's dependent hashes refreshed; three documents ready for the owner's consideration of RAT-41

- **EX_273** (`exchange/EX_273_ChatGPT.md`, main `6532258`, SHA-256 `dfd261eed588ece51158fe6205bb7a14e864e93608f39b3ddd818b8a48331ca9`), relayed by the owner at 17:27. **Register v0.32:
  DOCUMENTARY PASS** as candidate content (its hashes, v0.31 preserved, the one 174-line section, the RAT table against
  entries 63, 74, 87, 92, 101, 106 and 147, the out-of-date list), "subject to routine final identifier refresh". **H-1 v8:
  FIX AND PROCEED** for one final rebuild confined to A, B and C below. The reviewer also updated its own H-2 v4
  candidate and blurb (main `70719f5`, `03217df`, `adfd973`): R-8 to R-11 already owner-ratified; register v0.32 written.
- **The opening-record point (entry 150) is confirmed by the reviewer as "an IMPLEMENTATION COMPATIBILITY WATCHPOINT, not a
  new science policy"** (EX_273 section 2), with its guidance for build steps 2 and 3: say which old checks no longer
  apply, test and settle it in the normal code reviews; fresh DEV, QA and PROD trees must work under RAT-40 with no
  Mode H opening or seal as a prerequisite; "do not silently copy the obsolete study marker into a newly built tree
  merely to satisfy old code, and do not remove genuine source/ledger checks". No design change.
- **The H-1 v8 rebuild, exactly as authorised (main `a11db09`).** A: the H-2 v4 identifiers (section 4.4; Appendix A's two rows
  and its commit list). B: the four statements that register v0.32 was still owed (0A item 3, 0C note 4, 4.4, 12.8
  item 6) now say it is a written candidate, with its hash at the reviewed commit `a30b19a`. C: one paragraph in section
  10, the watchpoint. Made in the template; the builder gained one line so that a hash can be taken at a named commit.
  **Old candidate `9e8717cd758caf2e6e075b86911619bf0e04d67ec8c418347c32741ae172d335`; new candidate
  `2fd38130415f4c3602ac86f6f2b4250781f27f25bf204f66269424ea2c54a1f4`** (111,330 bytes). The exact diff is `exchange/CLAUDE_WEB_TOOLS/h1v8/H1_v8_C01_TO_EX273.diff`
  (`git diff --numstat`: 31 lines added, 14 removed; seven hunks, all inside A, B and C). The carried region is unchanged
  (102 lines, `80987a07...51764427`); **the blurb is unchanged, `586ececea64fca65b1ef3872a9fec60f1d7c659e0da408eb61e62d996d556d66`.**
- **Seen and left alone, being outside what was authorised:** section 0A item 3 still says "the newest EX is EX_271; the
  newest decision log entry is 148", and section 12.8's "Waiting on" lines do not name the register. Both are dated
  "at this edition" and the same item tells the reader to read the log first. The finalisation at ratification changes
  the status paragraph only.
- **The register's dependent hashes refreshed, as EX_273 section 1 asks.** Rebuilt by the same builder from the same
  section file (unchanged, `c3cdb445...1a11a6031`) against the commit above. `REGISTER_v0_32_a30b19a_TO_REFRESHED.diff` shows
  two lines changed and nothing else: the row for H-1 v8 (`9e8717cd...` to `2fd38130...`; its blurb's hash the same) and the
  row for H-2 v4 (to `8fa44f67fe37679c3039ae2c9676f86d2bc1269204a9e342f423e157d0612ba8` and, for its blurb, `700ca5da32494bd4d7f8da1d1c26e8ee96f784bf45501d220bff5e4b03b15a46`). Register v0.31 is not rewritten: `REGISTER_v0_31_TO_v0_32.diff` is again
  exact by `patch` and `cmp` (175 lines added, 1 removed). **Register v0.32 candidate, refreshed: SHA-256 `f508f7714693a7cfcd821ac714a475ae67f3dbc723e7924c8b2eb35168f25229`**
  (the reviewed snapshot at `a30b19a` was `2fd091f3...6d99135c`, which is the value H-1 v8 quotes, labelled as such).
- **Ready for the owner's consideration of RAT-41** (the reviewer's recommendation; the owner alone ratifies):
  1. `exchange/CLAUDE_WEB_TOOLS/h1v8/out/Claude_Primary_Handover_H1_v8.md` with its blurb (hashes above);
  2. `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md` with its blurb (the reviewer's files);
  3. `exchange/CLAUDE_WEB_TOOLS/register/RATIFICATION_REGISTER_v0_32.md` (hash above).
  On his ratification Claude finalises H-1 v8 and the register by their status lines and the register's table cells
  only, installs them in `doc/`, verifies the installed bytes from GitHub, and records it. Then the new Claude chat.
- **Authorised by none of this:** code, a build step, a run, anything on the owner's PC.

## 153. 22 November 2026, 17:37 - RAT-41: THE OWNER RATIFIES H-1 v8, the reviewer's H-2 v4 and register v0.32 together; his standing instruction on out-of-date statements; H-1 v8 and the register installed in doc/

- **The owner's words (17:34), in answer to Claude's question with "ratify all three together as RAT-41" as the recommended
  option 1:** "overriding instruction: when you detect out of date things like 'I left two small things in H-1 v8 alone
  because they were outside what the reviewer authorised. Section 0A still names EX_271 and entry 148 as the newest, and
  section 12.8's "waiting on" lines do not mention the register' please strongly consider fixing them. Option 1
  approved ... all three are ratified. Can I tell chatgpt to check/update their handover docs now ensuring they
  reference the latest versions (if so please provide an updated blurb after you have ensured everything is up to date
  and committed)".
- **RAT-41 is recorded** (RAT-40 was the last number used). Ratified: **H-1 v8 and its blurb** (candidate
  `2fd38130...2c54a1f4`; the reviewer's PASS in EX_272 and EX_273); **the reviewer's H-2 v4 and its blurb**
  (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md`, SHA-256 `8fa44f67fe37679c3039ae2c9676f86d2bc1269204a9e342f423e157d0612ba8`, main `70719f5`; blurb
  `700ca5da32494bd4d7f8da1d1c26e8ee96f784bf45501d220bff5e4b03b15a46`, main `adfd973`; the file's name still says CANDIDATE, frozen wording); **register v0.32** (candidate
  `f508f771...68f25229`; documentary PASS in EX_273). **H-1 v8 is the installed Claude handover** (H-1 v7r1, RAT-39, stays as
  history). **H-2 v4 is the reviewer's handover in force** (H-2 v3r4, RAT-36, stays as history).
- **STANDING INSTRUCTION (owner, binding on Claude from now):** when Claude detects out-of-date statements, it is to
  "strongly consider fixing them", and not leave them because a reviewer's authorisation was narrower. Claude's
  reading: fix them, show the exact difference, and say plainly what was changed beyond the reviewed text, so that the
  reviewer can look.
- **Finalised under that instruction** (`exchange/CLAUDE_WEB_TOOLS/h1v8/finalise_rat41.py`: counted replacements on the
  reviewed candidates, each asserted by SHA-256; nothing overwritten):
  - `doc/HANDOVER/Claude_Primary_Handover_H1_v8.md`, SHA-256 `8230e3dfecca528d185153e46a2173ef8a7a4d8fbc41695cc3b2bbbfcb20c45e`. Changed from the candidate
    (`exchange/CLAUDE_WEB_TOOLS/h1v8/H1_v8_CANDIDATE_TO_FINAL.diff`; `git diff --numstat`: 37 lines added, 32 removed): the
    status paragraph; "Replaces"; and the statements the ratification itself made out of date: the reading list's
    entry numbers; 0A item 3 (the newest numbers: RAT-41, EX_273, entry 153; the register is no longer behind); 0B item
    8; 0C note 4; section 4.4's two paragraphs on H-2 and on the register; section 10 items 1 and 2 (done; the new
    chat); section 12.8's two "waiting on" lines and its item 6. The carried sections 1, 2 and 2A are unchanged (102
    lines, `80987a07...51764427`, still one unbroken piece of H-1 v7r1). **These changes go beyond the reviewed text and
    carry no reviewer PASS of their own;** the reviewer is told and may look.
  - `doc/HANDOVER/Claude_Primary_Handover_H1_v8_introductory_blurb.md`, SHA-256 `586ececea64fca65b1ef3872a9fec60f1d7c659e0da408eb61e62d996d556d66`: the candidate's bytes, unchanged.
  - `doc/RATIFICATION_REGISTER_v0_32.md`, SHA-256 `f59d1911279e7e95a952a14c3a0c68422ba0f4e67f91ffd5369eb73c606c9acb`. Changed from the candidate
    (`exchange/CLAUDE_WEB_TOOLS/register/REGISTER_v0_32_CANDIDATE_TO_FINAL.diff`; 23 lines added, 14 removed): the version
    line; the RAT-41 paragraph; the status cells of four table rows (H-1 v8, H-2 v4, and H-1 v7r1 and H-2 v3r4 as
    superseded); item 12; the entry range (62 to 153); future actions 1 and 2. Register v0.31 is preserved inside it
    byte for byte outside the version line and the new section (checked by tool).
- **So that the hashes stop chasing each other:** H-1 v8 names the register by path only and cites H-2 v4 "as
  ratified", saying that a later commit may refresh its references; the register cites the final H-1 v8 and the
  ratified H-2 v4. Neither ratified file is edited again.
- **The owner's question, answered yes:** the reviewer can now check and update its own handover documents to name the
  installed editions. If that changes H-2 v4's bytes, the refreshed file is the reviewer's own next state of its
  handover; whether RAT-41 extends to it is for the owner to say, and Claude records what he says.
- **Also brought up to date with this entry:** `exchange/CONTINUITY_NOW.md` (its top block, "Reviewer status", "If a chat
  ends", "Installed handovers" and "Full order from here").
- **RAT-41 authorises no code, build step, run or install on the owner's PC.** Next: the owner starts the new Claude
  chat with `doc/HANDOVER/Claude_Primary_Handover_H1_v8_introductory_blurb.md`; this chat stops committing once it starts.
  The next ratification number is RAT-42; the next EX is EX_274.

## 154. 22 November 2026, 17:46 - OWNER: RAT-41 covers the reviewer's refreshed H-2 v4; his request that Claude bring the working lists, the two README files and, if possible, the local runner's rulebook up to date before the chat switch

- **The owner's words (17:45):** "chatgpt Reviewer \"recommendation: accept these reference-only updates under RAT-41
  without another handover review round\" so yes I accept them. Also yes I value your experience so please do update
  \"the first two now if you want them done before the switch\" (roadmap and reminders lists, Two README files under
  exchange/) and if possible the third as well (The local runner's rulebook)."
- **DECIDED (owner): RAT-41 extends to the reviewer's refreshed handover.** The reviewer committed it after RAT-41 at the
  owner's request (entry 153): `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md`, main `79406e4`,
  SHA-256 `b2837f08f8fd89134aebfbbed5815ca28b00f0ccebd1cb54c92f2f13c50cea2b`; its blurb, main `35a2ebf`, SHA-256 `5f113e4c4dca8648ccbf2a05e9a192bebf76d4473ad21e02c58de0b54a6bfcd5`. **These are the bytes of H-2 v4 in force.** Checked by Claude from
  Git: every changed line of the handover is above its "HISTORICAL INHERITED H-2 CHAPTERS" heading, so the inherited
  chapters and the rights text are untouched. (The earlier bytes, `8fa44f67...0612ba8` at `70719f5`, are the ones H-1 v8 and
  register v0.32 cite "as ratified"; both say that a later commit may refresh H-2 v4's references. Neither is edited.)
- **Asked of Claude, before the new Claude chat starts:** bring `exchange/OWNER_ROADMAP.md` and `exchange/OWNER_REMINDERS.md` up
  to date; bring `exchange/README.md` and `exchange/CLAUDE_WEB_TOOLS/README.md` up to date; and, if possible, the local
  runner's rulebook. The rulebook is a ratified rule document (RAT-30) that the runner obeys, so Claude writes a
  CANDIDATE of a new edition for the reviewer and the owner and does not change the installed file.

## 155. 22 November 2026, 17:52 - done at the owner's request of entry 154: the roadmap and reminders, the two README files, and a local runner rulebook v0.6 CANDIDATE (not installed)

- **The owner's two working lists** (`exchange/OWNER_ROADMAP.md`, `exchange/OWNER_REMINDERS.md`; main `25868f9`). Nothing was
  deleted. The roadmap: a new opening paragraph; a new section "The road from 22 November 2026" (steps A to I: the
  design and the handovers done; the new chat; his ZIP; the four build steps; then new methods); the old items' status
  words brought up to date (10c done in part, then replaced; 10d on hold; 21b overtaken). The reminders: every item
  that was not DONE has an update line dated 22 November 2026, with a summary table at the top; five status words
  changed where the item's own record showed it was finished or overtaken (R-012, R-015, R-018, R-026, R-028); **two
  are PROPOSED only and wait for the owner's word: R-007 (dropped) and R-017 (done);** one new reminder, **R-030**, lists
  what Claude must raise during the build and when (his ZIP first). Three lines of the reminders file that had LF
  endings were made CRLF, as its header says.
- **`exchange/README.md` is now v0.6** (main `25868f9`): brought into line with practice since RAT-34 (the reviewer commits
  its own files; Claude also commits ratified documents into `doc/`; most messages are one `.md` naming its documents
  by path and hash; not every message is an EX message; the decision log and the continuity page). It changes no
  rule. The takeover of 17 November 2026 had noted a v0.6 "to be proposed for review" (entry 64, D3); it was written
  directly on the owner's instruction, and the reviewer is told. H-1 v8's carried section 1.6 still says "v0.5": the
  ratified file is not edited; this entry is the note.
- **`exchange/CLAUDE_WEB_TOOLS/README.md`** (main `25868f9`): three stale statements corrected and one section added
  describing every folder since 14 November 2026 (`simplify/`, `h1v8/`, `register/`, the MHUP-B slices and where the
  OV-1 kernel is, and the rest) and how the document rounds were built.
- **The local runner's rulebook: a v0.6 CANDIDATE, and no change to the installed file.**
  `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_6/CLAUDE_v0_6_CANDIDATE.md` (SHA-256 `9d2cae3c780344797e6054b1eeeee875db5efc84aa8384ea7b4fa53ca4e8830f`), built by `make_rulebook_v0_6.py` from the
  installed v0.5 (`fa7a5fe2...acd5200`, asserted) by removing the ended section 2A whole and nine counted edits;
  `CLAUDE_v0_5_TO_v0_6_CANDIDATE.diff` is exact (13 lines added, 34 removed); `COVER_NOTE.md` (`db8bea751dad6cb8251a510d38aa4b295ea6b0dbe18530cd60ac827208fe09af`) gives each change with
  its reason, what was deliberately left alone, three questions for the reviewer and the owner, and three proposed
  deny lines for `.claude/settings.json` (the owner's file; not touched). It loosens nothing: it removes the T016
  allowance that had ended, widens rule 4 to every draw, names the new system's seventeen commands as never run,
  and adds rule 11 (QA, PROD and their backups are never touched) and rule 12 (the PC's date and time). **The runner
  obeys only the installed v0.5 until the owner ratifies a new edition after review.** Claude's recommendation in the
  note: install before build step 2, when the new commands first appear in the clone.
- **Still not brought up to date, on purpose:** `CLAUDE_CODE_WORKING_FOLDER_TREE/README.md` (the owner's page for the
  runner; it is accurate for the installed rulebook) and `doc/METHOD_TEMPLATE/` (a new draft is owed after build step
  3, when the new layout exists).
- Nothing here authorises code, a build step, a run or anything on the owner's PC.

## 156. 22 November 2026, 18:06 - RAT-42: THE OWNER RATIFIES the local runner rulebook v0.6 after the reviewer's PASS (EX_274); installed by Claude with the status change only

- **EX_274** (`exchange/EX_274_ChatGPT.md`, main `cd40f40`, SHA-256 `972cc2551ec5cd12f44dcc6f19ef27dfa4cd3ebe21c0402fc524d2ef8fc937f5`): "PASS. Recommend owner ratification and
  installation as RAT-42 now, before the new Claude chat takes over." The reviewer checked the candidate
  (`9d2cae3c...a4e8830f`), the cover note, the installed v0.5 and the exact diff; found "no new affirmative executable
  permission"; and answered the cover note's three questions: keep the broader rule 4; rule 11 is explicit enough; ratify
  and install now. It adds: do not generalise the old expected-refusal permission now; when a future owner-authorised
  task truly needs runner access, "write a narrowly scoped reviewed amendment"; and `.claude/settings.json` is not to be
  altered under EX_274.
- **The owner's words (18:05):** "I ratify the local runner rulebook v0.6 as RAT-42, following ChatGPT's PASS in EX_274.
  Claude may install the reviewed rulebook with only the necessary status change, verify the installed SHA-256, and
  record the decision. This authorises documentation-only installation. It does not authorise build step 1, a runner
  rehearsal, scientific execution, or any other operation. We can then proceed with the new Claude chat using H-1 v8."
- **RAT-42 is recorded** (RAT-41 was the last number used). **Installed:** `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`,
  **SHA-256 `f92f17f60db63990fc10a663778ec8d6a2b0737c9232895f1ee0af76ffdfa632`** (12,541 bytes), written by `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_6/finalise_rat42.py` from the reviewed
  candidate (asserted by hash) over the installed v0.5 (asserted by hash; Git keeps it). **One line differs from the
  reviewed candidate, the version line's status words** (`CLAUDE_v0_6_CANDIDATE_TO_FINAL.diff`; `git diff --numstat`: 1 added,
  1 removed): "v0.6 CANDIDATE ... NOT installed and not in force until then" became "v0.6, 22 November 2026, ratified by the
  project owner the same day (RAT-42) after the reviewer's PASS (EX_274)". No rule text differs from what was reviewed.
- **What v0.6 is:** a restrictive baseline. It allows nothing new. It removes the ended T016 allowance; rule 4 covers
  every draw; rule 7 names the new system's seventeen commands as never run; rule 11 (QA, PROD and their backup
  folders are never touched; no `ENVIRONMENT.ini`); rule 12 (the PC's date, time and zone).
- **For the owner, when he chooses (his file; not changed by anyone else):** the three deny lines proposed in
  `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_6/COVER_NOTE.md` section 5 for `.claude/settings.json`. **A running Claude Code
  conversation keeps the rulebook it started with:** after `git pull --ff-only`, start a new Claude Code conversation
  before the next task.
- **Overtaken by this entry, in ratified files that are not edited:** H-1 v8 section 8.6 and section 12.8 item 4, and
  register v0.32's future action 5, say a new rulebook edition is owed before the first rehearsal. The baseline
  edition now exists; what is still owed before a rehearsal is the narrowly scoped amendment for that rehearsal.
  Brought up to date with this entry: reminder R-030 (f), the roadmap's step B, the tools README, CONTINUITY_NOW.
- **RAT-42 authorises the documentation-only installation and nothing else:** not build step 1, a runner rehearsal,
  scientific execution or any other operation. The next ratification number is RAT-43; the next EX is EX_275.
- **This is the outgoing Claude chat's last planned entry.** The owner starts the new Claude chat with
  `doc/HANDOVER/Claude_Primary_Handover_H1_v8_introductory_blurb.md`; this chat stops committing once it starts.

## 157. 22 November 2026, 18:34 - HO-2: the new Claude chat's takeover (from H-1 v8) accepted by the owner after the reviewer's PASS; normal work authorised with the same GitHub rights; the reviewer's clarifications recorded

- **How it went (no EX numbers, as in entry 134):** the new Claude chat started from
  `doc/HANDOVER/Claude_Primary_Handover_H1_v8_introductory_blurb.md`, cloned `main` at `4229a13` with full history, read H-1
  v8 section 0's list and checked it with tools: H-1 v8 `8230e3df...20c45e`; its carried region 102 lines, 28,169 bytes,
  `80987a07...51764427`, found once in v7r1; 39 of the 43 hashes in its tables equal `HEAD`, the other four (the runner's
  rulebook, H-2 v4 and its blurb, `exchange/README.md`) changed by entries 154 to 156; `src/`, `tests/`, the root `.bat`
  files and `requirements.txt` unchanged since `cc0ab73`; the three switches False and the allowlist empty; the masters
  448 rows (1144 to 1591) and 235 rows (1474 to 1708), consecutive. Its first reply and its answers to the reviewer's
  three blind questions (step 1's permissions, preservation, baseline and equivalence evidence; telling old test
  failures from regressions; an obsolete Mode H gate against a still-binding source check) were given in the chat
  and relayed by the owner. Neither chat committed anything during the takeover.
- **The reviewer's assessment, pasted by the owner at 18:33 (not a committed file; its views, not owner decisions):**
  "HO-2 BLIND-QUESTION REVIEW: PASS." "I recommend that the owner accept your takeover and authorise ordinary
  documentary/planning work. No further HO-2 questions are required." Its clarifications, accepted by Claude:
  1. Keep the simplification: the simplest implementation that satisfies RAT-40; no obsolete MHUP-B machinery,
     ceremonial approvals, redundant checks, new record formats or supplementary bookkeeping without a concrete
     failure consequence; no weakening of N-1, scientific equivalence, data integrity, no-kill or owner approval.
  2. Step 1's scope also includes what specification 17.3 names: the method table built from the folder tree, the
     `closure.py` folder list, and the variant folders with `method.py` and `VARIANT.json`. Structural only; no change
     to calculations, seeds, views, ranking or TOP and WORST; moved code unchanged except imports; shown in the
     ordinary package diff.
  3. One real baseline run of the suite before the move and the same suite in the same environment after; compare
     test identities, results and substantive failure causes (incidental wording is not by itself a regression); the
     ordinary test reports, no separate per-test tracking. The equivalence check stays strict: every old development
     forecast target, every existing variant, both games, its original `canonical_content_digest` reproduced exactly.
     Running the unmoved code as a control is only for investigating a failure, not a mandatory extra round.
  4. The owner's full E: ZIP (with `.git` and the ignored old forecast records) made and checked before phase 1 moves
     source on his PC, kept off E:. The equivalence check by an owner-run, reviewed run sheet, read-only against the
     old records, so no runner permission changes for it; no separate ceremony for each command of an approved sheet.
  5. **One genuine later owner question:** the updater still refuses an update without a Mode H opening record, but
     specification 7.1 says it runs "unchanged". The reviewer prefers a narrowly reviewed correction in build step 3
     removing ONLY the obsolete Mode H precondition, keeping every Lotterywest-GOV source, overlap, chronology,
     record, ledger and concurrency check; a fresh PROD must work without fabricated or copied opening or seal
     records. The owner decides before it is implemented; it does not hold up step 1.
  6. Stale references settled: RAT-41 covers the refreshed H-2 v4 (entry 154; its "PENDING" wording is superseded);
     rulebook v0.6 is installed and only a narrow amendment may be needed for a future rehearsal; `exchange/README.md`
     is v0.6; the specification 17.3 pointer to the simplification design v0.1 is settled in the step-2 package; line
     endings are handled where byte-bound markers are built (step 2 or 3), without rewriting every source file as
     housekeeping.
- **The owner's words (18:33):** "per chatgpt assessment below, you are approved to commence work with all github access
  rights as previously approved. Please also pay attention to not letting undue \"overhead\" requirements creep back
  into the specs given that we had very recently spent a great deal of effort stripping them out (eg \"software
  process/controls/admin overheads\")."
- **DECIDED (owner):** the takeover is accepted; this Claude chat is the primary designer and coder, with normal work
  and the same commit rights as before (H-1 v8 section 0B item 4). The outgoing Claude chat commits nothing further.
- **Standing direction restated by the owner:** no undue overhead (software process, controls, administration) is to
  creep back into the specifications or the code. Claude applies it with the joint working principle
  (`exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md`).
- **Still open, put to the owner in the chat at 18:13:** whether the coding practices apply to the small amount of
  genuinely new code in build step 1 (the equivalence check's run sheet program, the folder-built method table, the
  `VARIANT.json` files), or only from build step 2 as `doc/CODING_PRACTICES_v0_1.md` says.
- **Not authorised by this entry:** build step 1, any run on the owner's PC (the baseline included), any install. Next
  numbers: EX_275, entry 158, RAT-43.

## 158. 22 November 2026, 18:37 - OWNER: THE GO FOR BUILD STEP 1 (the folder layout); the coding practices apply to all coding, step 1 included

- **The owner's words (18:36, repeated at 18:37):** "please apply Coding practices including step 1 i.e. all coding. Go now."
- **DECIDED (owner): `doc/CODING_PRACTICES_v0_1.md` applies to all new code, build step 1's included** (the document's own
  "Applies to" line says from build step 2; this entry extends it; the ratified file is not edited). In step 1 that is
  the newly written files only: the equivalence check program, the method table built from the folder tree, the
  `VARIANT.json` files. **The moved method files are not touched beyond their import lines** (specification 17.3); their
  headers and comments come in the light tidy-up after step 1 is proved (RAT-40 note 3).
- **GO (owner): build step 1** (specification 17.3 phase 1 and 17.4 step 1). As put to him at 18:34, the go covers
  Claude's work in its own cloud workspace: a rehearsal run of the existing suite, and building the step 1 package
  for the reviewer. **It covers nothing on the owner's PC:** the suite baseline there, his ZIP of the E: project
  folder before he installs, the install, and his read-only equivalence run sheet are each asked of him at their
  moment.
- **Model:** the owner selected Fable 5.2 at 18:37. Claude's standing suggestion for step 1 is Opus (H-1 v8 section 10);
  said to him in the chat.
- Next numbers: EX_275, entry 159, RAT-43.

## 159. 22 November 2026, 19:59 - OWNER: the worker-process test E2R-T12 may run in Claude's cloud workspace runs of the suite

- **The owner's words (19:59):** "\"The worker-process test (E2R-T12\" yes happy for it to stay in your cloud runs."
- **DECIDED (owner):** E2R-T12 (`tests/test_e2r_contract.py`; it starts ordinary worker processes) runs as part of the
  suite in Claude's own cloud workspace, so the before-and-after comparisons stay complete. Claude reported that it
  had already run in the step 1 runs (an exclusion that did not take effect; draft note v0.1). This covers the cloud
  workspace only: a run on the owner's PC is still asked of him with its run sheet or task.
- **Also asked:** whether to relay the step 1 progress paste to the reviewer now or with EX_275. Claude's answer:
  hold it and send everything once, as EX_275, with the install package (one review round).
- Next numbers: EX_275, entry 160, RAT-43.

## 160. 22 November 2026, 20:23 - EX_275 sent at the owner's request: the build step 1 install package for independent review; no owner decision beyond the request

- **The owner's words (20:03):** "please per your \"build the install package and your run sheet, then send everything to
  the reviewer once as EX_275\" do whatever you need to generate a good EX_275 now." He stays on Fable 5.2 for now (a
  usage reset is available to him for it and not for Opus).
- **Sent:** `exchange/EX_275_Claude.zip` (SHA-256 `be199e65637e5f0f19cf45c5132d445b2c20e0347380e14e6b38ea2edffd39e2`), extracted
  for reading in `exchange/EX_275_Claude/`. Its members: `EX_275_Claude.md`; the install package
  `STEP1_Layout_Install_v1.zip` (SHA-256 `8c23dfe29695fc1b1042fba1712f281a1cc234821228e4e2ec56c34847ca575e`; 117 members) and its
  member list. The package was built by `exchange/CLAUDE_WEB_TOOLS/step1/build_step1_pkg.py` from base `05e9afd`: an
  overlay of 95 new paths and 15 modified files, a list of 16 deletions, the read-only verifier (the reviewed template
  `wf1/verifier_template.py`, filled in), the three tools, the manifest and `INSTALL_AND_RUN_SHEET.md`.
- **Evidence since entry 158, all in `exchange/CLAUDE_WEB_TOOLS/step1/evidence/`:** the existing suite gives the same result
  before and after the move (45 modules, 571 tests; the same two known failing modules); the equivalence check PASSED
  on the moved code for every scored development forecast in the tracked rank ledgers (Powerball 11,442; Oz Lotto
  5,958); two planted faults were caught; the install was rehearsed in an LF and a CRLF clone (PRE, POST, COMMITTED
  PASS; four planted cases each STOP). `STEP1_PACKAGE_NOTE_v0_2.md` beside it has the card, the seven choices with
  their alternatives and the not-tested list.
- **The sheet's order, for the owner when the time comes (each part on his own go):** his ZIP of the project folder; the
  suite as it is today; PRE, copy, delete, POST; the same suite and the comparison; the equivalence check (which on
  his PC also covers the never-scored forecasts in the old run folders); stage, commit, COMMITTED; push.
- **Not authorised by this entry:** anything on the owner's PC. Next: the reviewer's reply, EX_276. Next numbers:
  EX_276 (the reviewer's), entry 161, RAT-43.

## 161. 22 November 2026, 20:48 - EX_276 (RECHECK: four narrow corrections, the layout accepted) read; all four accepted and corrected; EX_277 sent with package v2 at the owner's request; no owner decision

- **EX_276** (`exchange/EX_276_ChatGPT.md`, main `c0e3104`, SHA-256 `c45b3bda77ace3f9269870ea0ab96abb96d711731e5ccbef6147600edd5599c3`), relayed by the
  owner at 20:40. Disposition: RECHECK, narrowly. The 15 moves, the 40 variant folders, the per-variant dispatch, the
  helper relocation and the test updates are accepted, and the reviewer agrees with all five of EX_275's questions.
  Findings: **C01** the equivalence check could report a complete PASS without the never-scored forecasts, or for
  one game; **C02** the suite comparison identified 563 of the 571 tests; **C03** the two equivalence logs named in
  EX_275 were not on GitHub; **C04** the sheet said any FAIL is a STOP while expecting today's known test failures.
  Also: the reader-contract module has seven failed assertions today, not "two tests".
- **The owner's words (20:40):** "Please read `exchange/EX_276_ChatGPT.md` at commit `c0e3104` and address findings C01-C04.
  Keep the corrections narrow and follow the reviewer's KISS guidance. Return the corrected package for focused
  recheck."
- **Done, all four accepted (no file of `src/` or `tests/` differs from EX_275):**
  - C01: the check now takes the list of every published run from the tracked batch segments (17,280 Powerball,
    8,760 Oz Lotto) and requires an old digest for each; it prints listed, found and MISSING per game;
    `RESULT: PASS - COMPLETE` only for both games with nothing missing; otherwise PARTIAL with its reasons. Shown in
    a probe (complete; one game; one run folder removed; a missing receipt). The cloud's scored-only result is
    now correctly called PARTIAL: the complete result can only come from the owner's PC.
  - C02: the comparison identifies all 571 tests, compares each module's test count and verdict, and fails closed
    when it cannot identify every test. On the existing reports: nothing changed. Today's failures, accurately:
    three tests, eight failed assertions (`test_gitignore_lines` one; the reader-contract module seven).
  - C03: Claude's error: `.gitignore` has `*.log` and `git add` skipped the two files silently. The original bytes
    are committed as `.txt` with the hashes EX_275 gave. The EX assembly tool now hashes from Git's own bytes.
  - C04: one paragraph in the sheet; parts 3 and 4 quote the corrected tools; no step added.
- **Sent:** `exchange/EX_277_Claude.zip` (SHA-256 `e24782fac29e17230bfc5ee92f81eb60ab24b43c44bc4c817f1552715eb154c0`), extracted in
  `exchange/EX_277_Claude/`; the package `STEP1_Layout_Install_v2.zip` (SHA-256
  `f8fa81054e00f0b3ca908b8f89130f024b2ded1aec2d7973762ee0081e405051`; base `c0e3104`); package note v0.3. v2 differs from v1 only
  in two tools, the sheet, the package's name and the verifier's base commit; rehearsed again in an LF and a CRLF
  clone.
- **Not authorised by this entry:** anything on the owner's PC. Next: the reviewer's focused recheck, EX_278. Next
  numbers: EX_278 (the reviewer's), entry 162, RAT-43.

## 162. 23 November 2026, 06:47 - EX_278: the reviewer's focused RECHECK PASS of the build step 1 package v2 (STEP1-C01 to C04 closed); the owner holds every go for his PC

- **EX_278** (`exchange/EX_278_ChatGPT.md`, main `e64b401`, SHA-256 `53f6251128ab5ad1f7b089d4f0f09b68d70bf0fbba61599df451e63a6a3bddad`), relayed by the
  owner on 23 November 2026 at 06:46. Disposition: **PASS** ("reviewed package suitable for owner consideration").
  STEP1-C01, C02, C03 and C04 are closed; no new correction is asked; EX_275's five layout choices stay accepted. The
  reviewer recomputed both ZIP hashes and four evidence hashes from GitHub (all match) and compared the v1 and v2
  package ZIPs member by member: only five members differ (the sheet, the manifest's header, the verifier's base
  commit, and the two corrected tools); the overlay is identical. (Its "177 members, 168 overlay entries" counts the
  ZIP's folder entries too: 117 files and 60 folders; 110 overlay files and 58 folders. Checked with a tool.)
- **The reviewer's conditions and limits (its words in substance; none is an owner decision):** it is a review PASS, not
  an installed or scientifically verified one; the owner's ZIP of the whole E: project folder first; on his
  Windows Python 3.15.2 the suite baseline, the install under the sheet, the same suite with all test outcomes
  compared, and the strict equivalence check over both games ending `RESULT: PASS - COMPLETE` with `MISSING: 0` for
  each; "any new or unexplained Windows-only baseline failure should be reported before proceeding; do not
  automatically relabel it a known failure"; a differing digest is a STOP, with the unmoved-code control only for
  diagnosis; no additional machinery, QA or PROD creation or wider design round.
- **The owner's words (06:46):** "Focused RECHECK PASS. STEP1-C01 through C04 are closed. The v2 package is approved for
  owner consideration. Await my separate authorisation before any operation on my PC."
- **How the Windows-baseline condition is met without changing the reviewed package (Claude; told to the owner):** in
  part 1 of the sheet the expected failing modules are exactly the two that fail on `main` in the cloud
  (`test_mhupa_launchers`, `test_multigame_reader_contracts`). If the owner's baseline shows any other module FAILED,
  he pauses there and sends the output before part 2; nothing has been changed on his PC at that point.
- **State:** build step 1's package is REVIEWED (PASS). Not installed; not run on Windows. **Nothing on the owner's PC
  is authorised:** his ZIP and each part of `INSTALL_AND_RUN_SHEET.md` wait for his own go. Next numbers: EX_279,
  entry 163, RAT-43.

## 163. 23 November 2026, 07:30 - OWNER-REPORTED: part 0 of the step 1 sheet is done (his ZIP of the whole E: project folder, on four external drives); his listing of results/ checked against the batch records; no cleanup before the install

- **The owner's words (07:30):** "'E:\\SOFTWARE-Win11\\powerball\\analysing_perceived_randomness_in_reality' fully zipped and copied
  to 4 external USB3 drives. looking at the run sheet now." Evidence state: OWNER-REPORTED (Claude cannot see it). This is
  part 0 of `INSTALL_AND_RUN_SHEET.md` and reminder R-030 (a); the ZIP is the preserved copy of the old system and of
  the old forecast records that Git ignores (specification 17.2).
- **Before it (07:26 to 07:29), his question whether the E: tree needed a cleanup first,** because a `dir /s /b` of
  `results` was over 20 MB. He uploaded the listing (paths only). Checked by Claude with a tool: 107,665 lines; the
  development run folders are 17,280 (Powerball) and 8,760 (Oz Lotto), every one of the 26,040 run IDs in the tracked
  batch segments is present and no other is, each folder holds exactly its three files; 400 and 400 Mode H run
  folders. So there are no reruns and nothing is missing by name; the listing is long because every forecast has its
  own folder. **Claude's advice, which he followed: no cleanup before the install,** since those folders are what the
  equivalence check must read. A cleanup is safe after the transition check of build step 3, as his own act on his
  own say-so, with the ZIP as the archive. Not decided: when, or whether.
- **Not authorised by this entry:** parts 1 to 5 of the sheet; each waits for his go. Next numbers: EX_279, entry 164,
  RAT-43.

## 164. 23 November 2026, 09:41 - BUILD STEP 1 INSTALLED by the owner (main `0aea10a`): every part of the reviewed sheet passed on his PC, including the complete equivalence check; verified by Claude from GitHub

- **What the owner ran, 23 November 2026, 08:07 to 09:40, on his own go part by part** (`exchange/EX_277_Claude/STEP1_Layout_Install_v2/INSTALL_AND_RUN_SHEET.md`;
  his outputs, unedited, in `exchange/CLAUDE_WEB_TOOLS/step1/evidence/owner_pc_2026_11_23/`):
  - part 1, the suite as it was: 45 modules, 571 tests; FAILED exactly the two expected modules (`test_mhupa_launchers`
    1 failure; `test_multigame_reader_contracts` 7); four skips, the four symlink tests his Windows account cannot
    run (H-1 v8 section 6); the clone clean before and after;
  - part 2: `PRE PASS`; 110 files copied; `POST PASS` (95 new paths, 15 modified, 16 staged deletions; 25 guarded files
    unchanged);
  - part 3: the same suite on the moved code, the same module lines; the comparison identified all 571 tests in both
    runs, the same result for all 571, and "no module and no test changed" (`test_gitignore_lines` printed its
    set in another order, as expected);
  - **part 4, the equivalence check: `RESULT: PASS - COMPLETE`.** Powerball 17,280 of 17,280 and Oz Lotto 8,760 of 8,760
    old development forecasts found (MISSING: 0 in both; 5,838 and 2,802 of them only in his old run folders),
    computed again with the moved code and equal by content digest; 80 variants. About 31 and 9 minutes;
  - part 5: `COMMITTED PASS` ("added exactly 95 files, modified 15 and deleted 16; all Git blobs match"); pushed;
    `main` `0aea10a16ad26c7e5317430994cc76e2953ef89c`.
- **Verified by Claude from GitHub after his push:** `0aea10a` changes only `src/` and `tests/`; all 126 manifest entries
  match the pushed commit (95 added and 15 modified with their hashes; 16 deleted absent); its `src/` and `tests/` are
  identical to the tree that passed the suite and the equivalence check in the cloud.
- **State: build step 1 is INSTALLED, OWNER-WINDOWS-TESTED and complete** under specification 17.3 phase 1 (RAT-40;
  go in entry 158; the reviewer's PASS of the package in EX_278). The owner's ZIP of the old project folder (entry 163)
  remains the way back to the old system (specification 17.2).
- **Next, each on the owner's own go:** the light tidy-up of the existing method files (RAT-40 note 3; headers,
  dependency lists and missing comments; no calculation change; the equivalence check run again); then build step 2.
  The old run folders stay until build step 3's transition check (entry 163).
- **The owner's words (09:38):** "thank you. you are doing a good job leading me in this."
- Next numbers: EX_279, entry 165, RAT-43.

## 165. 23 November 2026, 10:21 - OWNER: THE GO FOR THE LIGHT TIDY-UP of the existing method files (RAT-40 note 3); built and proved in the cloud; not yet reviewed, not installed

- **The owner's words (09:44):** "thanks. go the next step which you suggest is tidy up"
- **What the go covers:** the work in the cloud (the wording, the builder, the proofs, the package). It authorises no
  operation on the owner's PC; the install is on his own separate go, after the reviewer's review.
- **Built by Claude** under `exchange/CLAUDE_WEB_TOOLS/tidy1/` (base `7be6b3a`; `src/` and `tests/` as build step 1 left
  them): 37 existing method files get the header of the coding practices, a comment on each of the 64 functions (of
  130) that had none, and notes on their constants; the earlier headers are kept word for word. No file added, moved
  or deleted; 1,385 lines added and 259 removed, all comment or docstring lines. Every new word is in one file,
  `tidy_texts.py`; `make_tidy_up.py` applies it and refuses on anything unexpected.
- **Left alone, with the reason:** six of E_1's own modules, whose exact bytes the old system's archive tests pin
  (`tests/test_code3_retirement.py`, `tests/test_e1r3_revision3.py`); the package's verifier guards them. **This is a
  choice for the owner** (package note section 6; Claude recommends leaving them).
- **Proved in the cloud:**
  - the comments-only check (`check_comments_only.py`, new): 211 Python files under `src` and `tests` compared with the
    base; 37 with changed text; in all 37 the code with comments and docstrings removed is identical; `RESULT: PASS`;
  - the suite before and after, test by test: 45 modules, 571 tests, the same result for all 571 (the same three known
    failing tests);
  - the equivalence check of build step 1 run again on the tidied tree: 17,400 of 17,400 scored forecasts equal
    (Powerball 11,442; Oz Lotto 5,958); no `DIFFERENT`, no `FAILED`; **`RESULT: PARTIAL`, as it must be in the cloud**
    (the never-scored forecasts are only in the owner's run folders). The complete evidence is the owner's run;
  - the install rehearsed in an LF clone and a `core.autocrlf=true` clone; five planted faults all STOP.
- **The package:** `exchange/CLAUDE_WEB_TOOLS/tidy1/package/TIDY1_Method_Comments_v1.zip`, SHA-256
  `a8d2f1136a41a361e665ef2b16e2f3ce073dff64b52e697f4588971fc812ad4c`, 44 files; its sheet beside it. The note is
  `exchange/CLAUDE_WEB_TOOLS/tidy1/TIDY1_PACKAGE_NOTE_v0_1.md`.
- **Corrections found by checking each citation against its document while writing:** none reached a file; four draft
  citations and one draft comment (an error type) were corrected before the proofs were run.
- **State:** the tidy-up is BUILT and CLOUD-PROVED; NOT REVIEWED; NOT INSTALLED. No EX has been issued.
- **Next, each on the owner's word:** his answer on E_1's six modules; EX_279 to the reviewer when he asks for it; then
  his install by the sheet, on his own go.
- Next numbers: EX_279, entry 166, RAT-43.

## 166. 23 November 2026, 11:03 - OWNER: E_1's six pinned modules stay as they are; EX_279 issued to the reviewer; H-1 to be refreshed after the tidy-up's install

- **The owner's words (11:01):** ""six of E_1's own modules get no new comments. Is that acceptable?" Yes I accept your
  judgement in that matter. Yes to issue EX_279 to the reviewer. now please. Yes to refreshing the H-1 handover once
  the tidy-up is installed, before step 2 starts."
- **Decided:** the tidy-up leaves E_1's six own modules (`E_001/__init__.py`, `e1_common_reader_bridge.py`,
  `e1_historical_appearance_frequency.py`, `e1_standalone_contract.py`, `e1_training_view.py`, `multigame_e1.py`)
  byte for byte as they are, because the old system's archive tests pin their bytes (package note v0.1 section 6,
  the recommended option). RAT-40 note 3 is met for the other 37 files.
- **Issued:** EX_279 (`exchange/EX_279_Claude.zip` and `exchange/EX_279_Claude/`), the tidy-up package
  `TIDY1_Method_Comments_v1` (unchanged, SHA-256 `a8d2f1136a41...8ad4c`) for the reviewer's review; reply as EX_280.
- **Agreed for later:** Claude refreshes the H-1 handover once the tidy-up is installed and before build step 2 starts.
- **State:** the tidy-up is BUILT, CLOUD-PROVED and WITH THE REVIEWER; NOT INSTALLED. No operation on the owner's PC is
  authorised.
- Next numbers: EX_280 (the reviewer), entry 167, RAT-43.

## 167. 23 November 2026, 11:14 - REVIEWER: EX_280 PASS of the light tidy-up package TIDY1_Method_Comments_v1; no changes requested

- **The owner's words (11:12):** "EX_280 is committed at e045f98. Independent review PASS. Please read the full
  disposition. No changes requested; await my installation GO."
- **EX_280 (main `e045f98`):** PASS, for the owner's consideration; no RECHECK. Hashes recomputed from GitHub match
  EX_279. Answers: (1) the comments-only check is sufficient as the direct proof, with the suite and the equivalence
  check as complementary evidence; (2) no material error found in the new headers or comments; (3) no change needed
  to the sheet. One point for the install: a baseline failure other than the three known failing tests, or a
  materially different one, is referred before going on (the sheet's existing STOP rule covers it). No new ZIP of the
  project folder is needed.
- **State:** the tidy-up is BUILT, CLOUD-PROVED and REVIEWED (PASS); NOT INSTALLED. The install waits for the owner's
  own go; then Claude refreshes H-1 before build step 2 (entry 166).
- Next numbers: EX_281, entry 168, RAT-43.

## 168. 23 November 2026, 11:17 - OWNER: THE GO FOR THE INSTALL of the tidy-up package TIDY1_Method_Comments_v1 on his PC

- **The owner's words (11:16):** "ok go", replying to Claude's recommendation to install first and refresh H-1 after.
- **What the go covers:** the reviewed sheet `exchange/EX_279_Claude/TIDY1_Method_Comments_v1/INSTALL_AND_RUN_SHEET.md`,
  parts 1 to 5, in order, on the owner's PC, with EX_280's point: a baseline failure other than the three known
  failing tests is referred to Claude before going on. A STOP is a STOP.
- **Claude pushes nothing to `main` from now until the owner has pushed the install commit**, so that his push in part 5
  stays a fast-forward.
- Next numbers: EX_281, entry 169, RAT-43.

## 169. 23 November 2026, 14:44 - THE LIGHT TIDY-UP INSTALLED by the owner (main `c7e6ed8`): every part of the reviewed sheet passed on his PC, including the complete equivalence check; verified by Claude from GitHub

- **The owner's words (13:15, during part 3):** "I AM VERY PLEASED WITH YOUR WORK ON THIS, THANK YOU."
- **On his PC, by the sheet of EX_279 (go in entry 168), outputs unedited in
  `exchange/CLAUDE_WEB_TOOLS/tidy1/evidence/owner_pc_2026_11_23/`:**
  - part 1: the first try found no package files (Windows "Extract all" had nested the folder one level deeper);
    nothing ran and nothing changed; after re-extracting, the baseline suite: 45 modules, 571 tests, the two known
    failing modules (three tests, eight assertions) and the four Windows symlink skips, as in build step 1;
  - part 2: `PRE PASS` (HEAD `31db13b`, the reviewer's H-2 v5 candidate commits on top of the base, `doc/HANDOVER/`
    only); 37 files copied; `POST PASS`; the comments-only check: 211 Python files, 37 changed, 0 problems,
    `RESULT: PASS`;
  - part 3: the suite again, the comparison 571 of 571 with the same result, "no module and no test changed";
  - **part 4: `RESULT: PASS - COMPLETE`**: Powerball 17,280 of 17,280 and Oz Lotto 8,760 of 8,760 old development
    forecasts equal by content digest, `MISSING: 0` in both;
  - part 5: commit `c7e6ed8ec854ab50e32559062e8b73c5c5e9abd1`; `COMMITTED PASS` (0 added, 37 modified, 0 deleted);
    pushed (`31db13b..c7e6ed8`).
- **Verified by Claude from GitHub:** `c7e6ed8`'s parent is `31db13b`; it modifies exactly 37 files, all under
  `src/methods/`; all 37 match the package manifest; `tests/` unchanged since the base; its `src/` equals the tree that
  passed in the cloud.
- **State: the light tidy-up (RAT-40 note 3) is INSTALLED, OWNER-WINDOWS-TESTED and complete.** Nothing is now
  between the code and build step 2 but the H-1 refresh the owner agreed (entry 166).
- **For later sheets:** say "extract to `E:\TEMP`" (the ZIP holds its own top folder), so that Windows does not nest it.
- **Next:** Claude refreshes the H-1 handover (agreed, entry 166); then build step 2 on the owner's own go
  (Fable (High) suggested for its core).
- Next numbers: EX_281, entry 170, RAT-43.

## 170. 23 November 2026, 14:47 - the H-1 v9 CANDIDATE written (the refresh the owner agreed in entry 166); not reviewed, not ratified

- **What it is:** H-1 v8 brought up to date after build step 1 and the light tidy-up were installed. Built from the
  installed H-1 v8's Git bytes (`8230e3df...20c45e`, asserted) by `exchange/CLAUDE_WEB_TOOLS/h1v9/make_h1_v9.py` (SHA-256
  `53ef31454652b3db3123f529d0ab55815c23001e23ae7fb58a7a11067d198010`) with counted replacements; sections 1, 2 and 2A are still H-1 v7r1's bytes (102 lines, `80987a07...51764427`,
  asserted); Appendix A rebuilt from `HEAD`. Out: `exchange/CLAUDE_WEB_TOOLS/h1v9/out/Claude_Primary_Handover_H1_v9.md`
  (SHA-256 `125549f5522555cb30e1a2a5ce6bc4ba68d34b000ddea2a0a96554ca4c74413b`) and its blurb (`1cbe95bedb9741a610760b25de80e24eb3c798d9814287a4d28d8256c551dbe5`), with the exact diffs `H1_v8_TO_v9.diff` (304 lines added, 203 removed) and
  `H1_v8_TO_v9_blurb.diff`, each shown to reproduce its candidate by `patch` and `cmp`.
- **What changed** (its Appendix B): the state (0B: build step 1 and the tidy-up installed); what exists (7: the
  layout, the suite's known result, the records and run folders); next work (10: from build step 2, with what each
  step must settle, and the updater watchpoint as the owner's question); the runner (8.6: rulebook v0.6 and the narrow
  amendment); eight lessons from the build (8.8); the build practice (12.3) and tools (12.2); open items (12.8); two new
  traps (0A items 10, 11); smaller updates in 0, 0C, 3, 4.4, 5.3, 6, 9, 12.1, 12.6, 12.9; Appendix A and B.
- **Checked while writing:** that `src/`, `tests/`, the root `.bat` files and `requirements.txt` differ from `cc0ab73` only by
  step 1's and the tidy-up's changes; the updater's `holdout_opened` (line 157) and its uses (lines 243, 721, 817); the
  layout's counts (40 `VARIANT.json`, 40 `method.py`).
- **State:** CANDIDATE, NOT REVIEWED, NOT RATIFIED. H-1 v8 stays the installed handover. Nothing is authorised.
- **Next, on the owner's word:** the reviewer's check (EX_281, when he asks); then his ratification (RAT-43) and its
  installation in `doc/HANDOVER/`; then build step 2 on his go.
- Next numbers: EX_281, entry 171, RAT-43.

## 171. 23 November 2026, 15:09 - OWNER IDEA, for after implementation: a short operations manual; no decision, no work now

- **The owner's words (15:09):** "while we are waiting,  i wonder about, afte implementation., an operations manual of
  some kind with table of contents and sections/subsections of things which can be done eg perhaps on section
  Migrations of infrastructure and methods and data (eg dev->QA, dev->prod, prod<-QA, prod<-dev), another maybe Normal
  day-to-day PROD Operations (subsections maybe to include What are Catchups and how to do them), and maybe Restoration
  of PROD from backup, and perhaps How to do Development/testing and Install to QA and to Prod and to Decommisions one,
  etc etc and/or some structured thing which tells a user how to do all the things that need doing ... and a final
  section along the lines of What is a Method and how to develop/test/QA/implement one which also mentions
  \"contracts\" and interfaces with runners, and at least one appendix briefly outlining the structure of the system in
  terms of draw data, infrastructure, runners, methods, data etc and how they interface ? Perhaps  you and  Reviewer at
  the right point in time could negotiate the structure of the document and what things are in or not (it must be
  brief human oriented \"how to\" not huge slabs of prose ). No need for a response now."
- **Noted, not decided:** after implementation (the natural point is once build step 3 is proved, with the commands
  real; the laboratory tools of step 4 then add their sections), Claude and the reviewer propose the manual's
  structure and contents for the owner to decide. Brief, task-oriented "how to"; the specification and the deployment
  design stay the authority, and the manual uses their operations and words (for example the QA software replacement
  from PROD and the research-data reseeding from PROD; nothing run for QA or DEV writes to PROD). It would also
  replace the owed new draft of `doc/METHOD_TEMPLATE/` for the method section, or point to it.
- Next numbers: EX_281 (the reviewer's reply on H-1 v9), entry 172, RAT-43.

## 172. 23 November 2026, 15:14 - EX_281: the reviewer's PASS of the H-1 v9 candidate with one narrow correction (FIX AND PROCEED), applied by Claude on the owner's word; the reviewer chat lost; Claude to refresh the reviewer's H-2 v5

- **EX_281** (`exchange/EX_281_ChatGPT.md`, main `f613ae7`): "PASS WITH ONE NARROW TEXT CORRECTION; FIX AND PROCEED." It
  reproduced both diffs exactly and found sections 1, 2 and 2A unchanged. **H1V9-C01:** section 8.6 said "The runner
  can still run the existing suite in a task clone, as task T024 did", but under rulebook v0.6 rule 10 the runner
  must STOP on the suite's known FAILED results. **Count correction:** the v8-to-v9 diff of the reviewed candidate
  added 307 lines and removed 222, not 304 and 203 as entry 170 says (Claude's count left out blank lines). Entry 170
  is not edited; this entry is the correction. Section 5: the reviewer's H-2 v5 candidate predates the tidy-up's
  install and needs a status refresh before any joint ratification.
- **The owner's words (15:13):** "OK. chatgpt reviewer just died without warning again. Before it died, two things (1)
  EX_281 is committed at f613ae7. PASS WITH ONE NARROW TEXT CORRECTION; FIX AND PROCEED. Please read the complete
  review, apply the precise H-1 section 8.6 correction, and provide the resulting hash and exact diff. No broader
  redesign or review round is required. me: so I trust you to enact it without reviewer. (2) chatgpt handover and
  blurb were only partially completed \"There is also one separate continuity matter: my H-2 v5 candidate needs a short
  status refresh to recognise the completed tidy-up before it could be ratified jointly with H-1 v9\", so I need you
  to review and update them for my use in initiating a new chatgpt reviewer chat after doing (1). If you do not
  object lets do these now please."
- **(1) Done:** the sentence replaced with the reviewer's wording (marked "EX_281 H1V9-C01"), and the matching row of
  Appendix B updated so that its change list stays true. Nothing else changed: the blurb and its diff are unchanged;
  the carried region is unchanged (asserted). **H-1 v9 candidate, corrected: SHA-256
  `943077447a2b05c6eecd4a22381cf9a6591685211ec45dd1697db2d8861948b6`** (120,172 bytes); the exact difference from the reviewed
  candidate is `exchange/CLAUDE_WEB_TOOLS/h1v9/out/H1_v9_EX281_CORRECTION.diff` (4 lines added, 2 removed); the v8-to-v9
  diff is regenerated (310 added, 222 removed) and both diffs reproduce the candidate by `patch` and `cmp`. Builder:
  `make_h1_v9.py`, SHA-256 `6b3a79abf5970d87fbd6d82cd3722b786330f2ce7056d20db4192f96ac534444`.
- **(2) Next, at the owner's request:** with the reviewer chat lost, Claude writes a refreshed reviewer handover
  candidate from the reviewer's own H-2 v5, as it did on 21 November 2026 (the v3r10 continuity candidate). The
  reviewer's files are not edited; the refresh is a new file.
- **State:** H-1 v9 is a reviewed CANDIDATE (EX_281 PASS, the correction applied), not ratified; H-1 v8 stays installed.
- Next numbers: EX_282, entry 173, RAT-43.

## 173. 23 November 2026, 15:16 - the reviewer chat ended; at the owner's request Claude refreshes the reviewer's H-2 v5 candidate and blurb as H-2 v5r1, for starting a new reviewer chat

- **The owner's words:** see entry 172, item (2), and at 15:15: "i may have those version numbers wrong, also please check
  they are the \"latest\"."
- **Checked against `main` (`578eb1a`):** the newest editions are the specification v0.6, the deployment design v0.12, the
  coding practices v0.1, register v0.32, the runner rulebook v0.6, `exchange/README.md` v0.6; H-1 v8 installed and H-1 v9 the
  newest candidate; H-2 v4 in force (refreshed bytes `b2837f08...`, entry 154) and H-2 v5 the newest candidate
  (`54ce9f3b...`, the reviewer's commit `23689ef`; blurb `5c8686db...`, `31db13b`); EX_281 the newest EX. The reviewer
  committed nothing after EX_281. The owner's version numbers are right.
- **What Claude does, as on 21 November 2026 (the v3r10 continuity candidate):** a new file, H-2 v5r1, built from the
  reviewer's own H-2 v5 bytes by `exchange/CLAUDE_WEB_TOOLS/h2v5r1/make_h2_v5r1.py` with counted replacements of section 0's
  status statements only (the tidy-up installed; the H-1 v9 candidate, EX_281 and its correction; the reviewer chat
  ended; next numbers); the historical chapters 1-19 and the rights text byte-identical (asserted). The blurb likewise,
  and its broken deployment-design link (`hydra333`, one `3` missing) corrected. **The reviewer's files are not changed;**
  the candidate stays under `exchange/` until the owner ratifies it. The blurb tells the new reviewer chat that Claude
  wrote this refresh and that it should verify it against the repository itself.
- Next numbers: EX_282, entry 174, RAT-43.

## 174. 23 November 2026, 15:20 - RAT-43: THE OWNER RATIFIES H-1 v9 and H-2 v5r1; both installed in doc/HANDOVER/ with status statements changed

- **The owner's words (15:18):** "ratified since i have not a lot of choise."
- **Read by Claude as RAT-43 covering both candidates** (Claude's previous message offered H-1 v9 alone or the two
  together), said in the chat before installing. Claude also said that he does have a choice and that ratifying closes
  nothing off: H-1 v9 has the reviewer's PASS (EX_281) with its correction; H-2 v5r1 is the part without an independent
  check, because Claude wrote it after the reviewer chat ended; if the new reviewer chat finds a problem in it, that
  becomes a later refresh.
- **Ratified (RAT-43, 15:18):** the H-1 v9 candidate (SHA-256 `943077447a2b05c6eecd4a22381cf9a6591685211ec45dd1697db2d8861948b6`) and the H-2 v5r1 candidate
  (`4703f51af2bb2fa5f7144ecc209a720adada2902ce51cc5fa9a0b0a28acc3d84`) with their blurbs (`1cbe95bedb9741a610760b25de80e24eb3c798d9814287a4d28d8256c551dbe5`, `c3335aa814dfbbc2424c0e0edec67092cd3a59666c1ff5702d9664832e5a1634`).
- **Installed by Claude** with `exchange/CLAUDE_WEB_TOOLS/rat43/finalise_rat43.py` (each candidate asserted by hash; counted
  replacements of the status statements and of the statements RAT-43 itself made out of date, under the owner's
  standing instruction of entry 153):
  - `doc/HANDOVER/Claude_Primary_Handover_H1_v9.md`, SHA-256 **`8c28f82c0662be75d683bd37b13d6b0596b3b6424584d5674f09f1d965b182b1`** (`H1_v9_CANDIDATE_TO_FINAL.diff`:
    24 lines added, 14 removed: the version and status lines, "Replaces", the newest numbers, the chats, section
    4.4's handover in force, section 10 item 2, section 12.8's waiting items); its carried sections 1, 2 and 2A unchanged
    (`80987a07...51764427`);
  - `doc/HANDOVER/Claude_Primary_Handover_H1_v9_introductory_blurb.md`, the candidate's bytes unchanged (`1cbe95be...51dbe5`);
  - `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5r1_20261123.md`, SHA-256 **`234e5917c2b980cc50a1a0f08fc77af320febdd0ee05f595abff32564714edc8`**
    (`H2_v5r1_CANDIDATE_TO_FINAL.diff`: 7 added, 4 removed, all in the status paragraph and section 0.10, 0.11 and the
    next numbers); its historical chapters 1-19 and rights text unchanged (asserted);
  - `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5r1_20261123_introductory_blurb.md`, SHA-256 **`f195212e0de626608b2fb7f96c71d3244b3770394baa28eb372449707f6f20aa`**
    (`H2_v5r1_blurb_CANDIDATE_TO_FINAL.diff`: 7 and 7): it now links to the installed handover and names its hash.
  Each diff reproduces its installed file by `patch` and `cmp`.
- **In force from now:** H-1 v9 and H-2 v5r1. H-1 v8, H-2 v4 and the reviewer's H-2 v5 stay where they are as history.
  The next register edition records RAT-41's install to RAT-43 (owed, H-1 v9 section 12.8).
- **Next, on the owner's word:** he starts a new ChatGPT reviewer chat by pasting the installed H-2 v5r1 blurb; its
  takeover reply; then build step 2 on his own go (Fable (High) suggested for its core).
- **RAT-43 authorises the documentary installation and nothing else.** Next numbers: EX_282, entry 175, RAT-44.

## 175. 23 November 2026, 15:38 - OWNER: the new ChatGPT reviewer chat's takeover (from H-2 v5r1) accepted; reviewer-role continuity, not a ratification and not a GO

- **How it went (no EX numbers, as in entries 134 and 157):** the owner started a new ChatGPT reviewer chat with
  `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5r1_20261123_introductory_blurb.md`. Its first reply (in the chat, relayed by the
  owner; not a committed file): "Initial repository verification PASS"; it computed the SHA-256 of H-2 v5r1, H-1 v9, the
  three RAT-40 documents, register v0.32, H-1 v8 and rulebook v0.6 itself at `main` `e454f36`; it read H-2 v5r1 in full, the
  governing documents, the exchange protocol, the working principle, H-1 v9, EX_281 and the decision log through entry
  174; it found chapters 1-19 and sections 0.4 and 0.5 byte-identical to the ratified H-2 v4; "Disposition: TAKEOVER
  PASS"; no clarification questions, so no EX; EX_282 still free.
- **Checked by Claude before advising the owner:** `e454f36` is `main`; chapters 1-19 of H-2 v5r1 (73,602 bytes from "## 1.
  Reviewer" to the end) and its sections 0.4 and 0.5 are identical to H-2 v4 (`b2837f08...`). Claude's advice: comfortable;
  no blind-question round needed this time; its first real review will test it; record as an owner acceptance, not a RAT.
- **The owner's words (15:38), as he gave them to the reviewer:** "OWNER DECISION - 23 November 2026 / The owner explicitly
  approves the new ChatGPT reviewer chat commencing its role as independent scientific and technical REVIEWER of
  hydra3333/analysing_perceived_randomness_in_reality, following the independently verified RAT-43 H-2 v5r1 takeover. /
  The reviewer retains all previously owner-ratified rights R-1 through R-11, reviewer-decided latitude, and existing
  authorised GitHub repository access and permissions, subject to the established scope and safeguards. / Claude remains
  primary designer/coder; the owner remains sole ratifier and authority for consequential operations. / This is
  reviewer-role continuity approval, not a separate GO for build step 2, implementation, installation, real-data
  operations or other gated actions. / Claude is requested to record this owner decision as decision-log entry 175,
  subject to confirming the current sequence. No new ratification number is required."
- **DECIDED (owner):** the new reviewer chat is the independent reviewer, with rights R-1 to R-11, its latitude and its
  repository access as before. Sequence confirmed: entry 174 was the last; this is 175; no RAT number used.
- **Not authorised by this entry:** build step 2, any implementation, install, real-data operation or other gated action.
- Next numbers: EX_282, entry 176, RAT-44.

## 176. 23 November 2026, 15:46 - OWNER: THE GO FOR BUILD STEP 2 (the research engine, in DEV), on Fable (High)

- **The owner's words (15:45):** "switched to fable (High) now ... please go now !"
- **What the go covers:** build step 2 of specification 17.4, in the cloud workspace: the lists, the research job with
  its fill and catch-up, scoring, the reports, both OV-1 scores, the status file and withdrawal, with RAT-40's notes and
  the coding practices; its tests; its package for review. As for build step 1 and the tidy-up, **it authorises no
  operation on the owner's PC:** every install and run there is on his own separate go, after the reviewer's review.
- **Model:** Fable (High), as suggested for the core of step 2 (H-1 v9 section 10); Claude says when the Fable part is
  finished.
- Next numbers: EX_282, entry 177, RAT-44.

## 177. 23 November 2026, 15:59 - build step 2: the plan committed; OWNER: DEV's research results stay out of Git; review in slices is Claude's choice

- **The plan:** `exchange/CLAUDE_WEB_TOOLS/step2/STEP2_BUILD_PLAN_v0_1.md` (main `1b1713a`): a new package `src/research/` beside
  the old system, which is not edited; three slices (A identity and records; B the job and OV-1; C reports and
  launchers); nine choices marked RECOMMENDED with their alternatives; two questions put to the owner.
- **The owner's words (15:54):** "1. \"Should DEV's research results be left out of Git\" Yes, we call always copy results
  back from PROD or PROD backups when needed.  2. your choice."
- **DECIDED (owner):** DEV's research results are not tracked by Git (`.gitignore` lines travel in the step 2 package).
  **Claude's choice, as he allowed:** review in slices as each is ready, one install at the end on his own go.
- **Progress (cloud):** the first seven modules of slice A are written; the new forecast engine gives the same view
  digest, scores, ranking, TOP and WORST as the old assembly for all 40 variants in both games at two targets each
  (160 forecasts, no difference; an ad hoc check, to become a test of the package).
- Next numbers: EX_282, entry 178, RAT-44.

## 178. 23 November 2026, 17:23 - build step 2 is CODE-COMPLETE and PROVED IN THE CLOUD; package STEP2_Research_Engine_v1 built; EX_282 waits for the owner's word

- **What exists** (`exchange/CLAUDE_WEB_TOOLS/step2/`; code and tools at main `cc8398c`, the package, note and evidence
  in the commit that carries this entry): the engine `src/research/` (20 files), `src/research_command.py`, the
  launchers `Run_Research.bat` and `Withdraw_Variant.bat`, `deploy/INFRA_MANIFEST.ini` (32 files with their classes),
  `ENVIRONMENT.example.ini`, 7 test modules with 179 tests. 33 new files and 2 edited (`.gitignore`; one line of data
  in the old static test `tests/test_mhupa_master_versions.py`); nothing deleted; no file of the old system's code or
  of any method changed. The package note is `STEP2_PACKAGE_NOTE_v0_1.md`; the plan as built is
  `STEP2_BUILD_PLAN_v0_2.md` (v0.1 kept).
- **Evidence (cloud; `evidence/`):** the engine's 179 tests pass; the whole suite before and after: all 571 old tests
  give the same result, 52 modules and 750 tests after; the suite again on the tree after a first fill: all 750 the
  same; 26 of 26 planted faults caught by the test named for the rule; the install rehearsed in an LF clone and a
  `core.autocrlf=true` clone, with six cases that must STOP.
- **Real, and only SUGGESTIVE (computed by Claude in the cloud from the real results; counts for nothing until the
  owner's own run):** the new engine filled both games (Powerball 22 minutes, Oz Lotto 7; a job with nothing new 71
  and 32 seconds); all 34,800 old development score records that Git tracks equal the new score lists (numbers drawn,
  matches, prize division; 40 variants, TOP and WORST, both games); for two Powerball variants whose old forecast
  records were made again with the old code path, 582 of 582 equal in view digest, scores, ranking, TOP and WORST.
- **Settled in the package note, as H-1 v9 section 10 asks:** the exact clause list for E2R-1 section 7 (note section
  6); specification 17.3's pointer to the simplification design v0.1 (note section 3: the list of what the engine
  imports, copies and leaves out, computed from the imports); line endings left to step 3, with the reason (note
  section 5).
- **Choices made while building, each RECOMMENDED with its alternative** (note section 5), among them: reports made
  again at every job and written only where the bytes differ; the job lock as a file made by an exclusive create (the
  deployment design's wording); the job classed `derived`; until build step 4 no command clears a held variant or a
  mismatch (in DEV the untracked `results/research/` folder is deleted by hand and filled again).
- **Not tested:** nothing has run on Windows; the `.bat` files have never been executed. The owner's sheet
  (`package/INSTALL_AND_RUN_SHEET.md`) installs and proves the install in parts 1 to 5, and runs DEV's first fill only
  in part 6, on his separate go.
- **Nothing is authorised on the owner's PC.** EX_282 (body and assembler ready beside the package) is issued to the
  reviewer only on the owner's word.
- **Model:** the Fable (High) part of build step 2 is finished; the owner may switch back to Opus.
- Next numbers: EX_282, entry 179, RAT-44.

## 179. 23 November 2026, 18:14 - OWNER: issue EX_282; EX_282 ISSUED (build step 2, package STEP2_Research_Engine_v1, for full review)

- **The owner's words (18:13):** "Yes, now. I assemble and commit EX_282 and give you the paste block." (his choice
  of the first of the three options put to him after entry 178.)
- **EX_282** (`exchange/EX_282_Claude.zip`, SHA-256 `2e0df75a459cfaa7e2b8ccffbd498893bbb03bf1cffb017f1b9fc6c1f75da7a7`,
  and the folder `exchange/EX_282_Claude/`): the message, the package ZIP `STEP2_Research_Engine_v1.zip` (SHA-256
  `829e2687842e715c9d8dcd61dcb4185d4219457e0def7acc20118b28b3855116`, byte for byte the committed package) and its
  member list. Base `cc8398c`. Risk tier HIGH; a full review is asked, with ten questions (Q1 to Q10); the reply is
  to be EX_283. Assembled by `exchange/CLAUDE_WEB_TOOLS/step2/assemble_ex282.py`; every hash computed, none typed.
- **Noted:** the owner's commit `5574d86` put a copy of the package note at
  `doc/how_things_work/STEP2_PACKAGE_NOTE_v0_1.md`. It changes nothing under `src/` or `tests/`, so the package's base
  stays valid. The working original remains `exchange/CLAUDE_WEB_TOOLS/step2/STEP2_PACKAGE_NOTE_v0_1.md`; if the
  review changes the note, the copy is the owner's to refresh.
- **Nothing is authorised on the owner's PC.** After EX_283: his own go for the install (sheet parts 1 to 5), and a
  separate go for DEV's first fill (part 6).
- Next numbers: EX_283 (the reviewer's reply), entry 180, RAT-44.

## 180. 23 November 2026, 18:53 - OWNER: answers for build step 3 (the updater's Mode H remnant; line endings; where QA, PROD and the backups live; who may rehearse); no parallel runner now

- **The owner's words (18:52):** "A multi-threaded runner, OK to Recommendation: not now.  \"Decisions waiting for you in
  step 3\":  1. re \"The updater's leftover Mode H precondition\" I thought we had got rid of mode H stuff ? What is
  your advice ? ... my lean is clean-sheet, no hangovers.  2. yes to whatever your recommendation is as long as  we
  are consistent.  3.  I have changed my mind,  PROD on G:\a_p_r_i_r, QA on T:\a_p_r_i_r , BACKUPS on T: in the folder
  name we agreed to.  4. I am happy if you ask chatgpt to run them as well as you if you feel the need, or even ask
  chatgpt to try to run them instead and report back to you, so as to save your resources - I trust that you will
  make the right choices; also available and \"free\" and I am happy to do it if it is well logged etc is claude in my
  VSCODE to test-install et al stuff maybe in under a D:\DELETE_ME\a_p_r_i_r  folder or something on my D: SSD drive so
  it is \"quick\"."
- **DECIDED (owner):** no parallel or multi-threaded runner now; looked at again only if the timings from his PC call
  for it.
- **The updater (item 1): the owner's lean is a clean sheet, no hangovers. Claude's advice, given in the chat, to be
  confirmed by him and put to the reviewer with step 3:** a new edition of the updater for the new trees, with every
  Mode H state taken out (the opening record, the seal, the quarantine dates, the session lock, the first-update
  rule), so that it has one behaviour, the ordinary update; every Lotterywest-GOV source, parsing, overlap,
  chronology, ledger and lock check kept character for character and proved so by comparison; `results_master_v0_2.py`
  left untouched in DEV. Read on 23 November: as installed, the updater refuses outright for a game with no opening
  record, so a fresh PROD could not update with it. The reviewer's stated preference (H-1 v9 section 10) is narrower:
  remove only the precondition. Not yet decided.
- **DECIDED (owner): line endings (item 2):** Claude's recommendation, applied consistently. The recommendation is
  to pin LF for the project's code in `.gitattributes` as part of step 3, before the first tree is created, by a
  proved sheet; DEV's research results are then filled again once.
- **DECIDED (owner): the places (item 3), replacing the examples of deployment design v0.12 section 1:** PROD at
  `G:\a_p_r_i_r`; QA at `T:\a_p_r_i_r`; backups on `T:` under the agreed name (`T:\a_p_r_i_r_backups`). **Open, asked in
  the chat:** each tree needs its own backup root (specification 18, "QA and PROD backups land in their own roots");
  Claude proposes `T:\a_p_r_i_r_backups\PROD` and `T:\a_p_r_i_r_backups\QA`.
- **DECIDED (owner): rehearsals (item 4):** Claude chooses who runs what. The reviewer may be asked to run things in
  its own workspace; Claude Code on the owner's PC may rehearse installs in a scratch folder such as
  `D:\DELETE_ME\a_p_r_i_r`, provided it is well logged. **That needs a reviewed and ratified edition of the runner's
  rulebook first** (v0.6 rules 3, 7 and 11 forbid it today); Claude prepares it with step 3.
- Nothing here authorises any operation on the owner's PC.
- Next numbers: EX_283 (the reviewer's reply), entry 181, RAT-44.

## 181. 23 November 2026, 19:27 - OWNER: the step 3 answers confirmed; EX_283 received (RECHECK, two crash-recovery blockers); both fixed, package STEP2_Research_Engine_v1r1 built; EX_284 waits for the owner's word

- **The owner's words (19:06):** "1. The updater and Mode H : yes to your advice/recommendation \"My advice: your clean
  sheet, done as a new edition.\"      EX_283 is available to consider in conjunction with our subsequent dialogue
  here. 2. yes to your line endings recommendation 3.  yes to your recommendations on where things live.  Yes, I will
  be doing regular backups of those folders (xcopy of files changed/newer) to 2 or 3 USB3 external drives; if you can
  suggest a guaranteed safe and better robocopy line then that'd be good eg F:\a_p_r_i_r_PROD_BACKUP\ containing the
  backup of prevailing prod (non backup) tree and F:\a_p_r_i_r_QA_BACKUP\ containing the backup of prevailing QA (non
  backup) tree  ... my xcopy are non-deleting cumulative so guaranteed nothing is ever accidentally deleted (not
  ideal but all my backups go there and I want to be 100% safe for my huge backup trees on those USB3 drives and
  other drives); other USB drives F: I: Y: .   go ahead and create a new edition of the runner's rulebook but
  allowing it to only do specific things on a specified drive (in this case D: for the run of those things?). re
  \"Different bytes under that name\" didn't we agree on in-place install overwriting recently ?"
- **DECIDED (owner), for build step 3:** (1) the updater: a clean sheet, as a new edition with every Mode H state
  removed and every genuine source, parsing, overlap, chronology, ledger and lock check kept and proved unchanged;
  `results_master_v0_2.py` stays untouched in DEV; to be put to the reviewer, whose stated preference was narrower.
  (2) Line endings: LF pinned for the project's code in `.gitattributes` in step 3, before the first tree is created.
  (3) The places: PROD `G:\a_p_r_i_r`; QA `T:\a_p_r_i_r`; backup roots `T:\a_p_r_i_r_backups\PROD` and
  `T:\a_p_r_i_r_backups\QA`. His own copies to USB drives are his, outside the system; advice given in the chat.
  (4) A new edition of the runner's rulebook is to be drafted, allowing named things only, in one named folder on
  D:; for review and ratification (RAT-44) before it has any force.
- **EX_283 (reviewer; main `0c4b5dd`): RECHECK, not PASS.** Two BLOCKER findings in crash windows, both accepted as
  found. F283-B01: the status file's temporary copy lay in the variant folder, so an interrupted write left an
  undeclared file that disabled the variant. F283-B02: an interrupted results copy could put the new ledger beside
  the old results. Q1 to Q10 answered (accepted, some with scope; Q10 held for the corrected package).
- **Corrected (code at main `465758d`):** the status file is staged in `<tree>/records/status_staging/` and leftovers are
  removed under the job lock; the results copy stages results then ledger, replaces results then ledger, and puts a
  staged ledger in place only if it names the results on file. **A third fault, found by the oracle the reviewer
  asked for, is fixed too:** the league reports are made again at the end of each job, so that an eligibility draw
  written at the end shows in that job's reports.
- **Package `STEP2_Research_Engine_v1r1`** (`exchange/CLAUDE_WEB_TOOLS/step2/package_v1r1/`, base `465758d`; six files differ
  from the reviewed v1, which is kept in `exchange/EX_282_Claude/`). Note v0.2 beside v0.1. Evidence
  (`evidence_v1r1/`): 185 engine tests pass; all 571 old tests the same, 756 after; 31 of 31 planted faults caught;
  the install rehearsed in an LF and a CRLF clone with seven STOP cases; the corrected engine run over the cloud's
  real fill computes nothing and rewrites no report (suggestive only).
- **EX_284** (body and assembler ready) is issued to the reviewer only on the owner's word. Nothing is authorised on
  the owner's PC.
- Next numbers: EX_284 (Claude), entry 182, RAT-44.

## 182. 23 November 2026, 20:13 - OWNER: issue EX_284; EX_284 ISSUED (build step 2 corrected, package STEP2_Research_Engine_v1r1, for RECHECK); the runner's rulebook v0.7 CANDIDATE drafted; two items for the operations manual

- **The owner's words (20:11):** "i agree yes please issue EX_284 for the recheck.  ok to \"Didn't we agree on in-place
  overwriting?\" and thanks for clarifying ... something that needs to to go ito the operations manual so all are
  clear (and how the installable and flag files work). thanks for those robocopies.  rulebook: ok yes  to your
  recommendations although maybe read/write/delete anywhere under 'D:\DELETE_ME\' with anything you see fit from
  .bat files and code through to data and reports, anything at all if you see fit for a purpose, usually under
  '`D:\DELETE_ME\a_p_r_i_r`'; yes let the runner run create_venv.bat or better still
  install_upgrade_dependencies_into_venv.bat which apparently calls that i no venv exists and adds dependencies which
  are probably required anyway - if you object lets discuss it."
- **EX_284** (`exchange/EX_284_Claude.zip`, SHA-256 `00be6dea33816fc36d7744bc220eeaa7c557f856a994cf462d355375a7533696`,
  and the folder `exchange/EX_284_Claude/`): the message, the package ZIP `STEP2_Research_Engine_v1r1.zip` (SHA-256
  `93bafc41d749328d63cc3eb3cd18eb0b3bd25ec9962a31738d3f171a3c25e7a1`, byte for byte the committed package) and its
  member list. Base `465758d`. It replies to EX_283: F283-B01 and F283-B02 accepted and fixed, with the oracles asked
  for; the reply is to be EX_285. Every hash computed, none typed; the message's table of the six changed files
  gives for v1 the same hashes the reviewer computed independently in EX_283 section 6.
- **For the operations manual (entry 171), noted at the owner's wish:** (a) what is and is not overwritten: an
  install never overwrites; shared code (forecasting infrastructure, `_shared` helpers, a family's own helpers) is
  corrected in place only by `Correct_Shared_Code.bat` on its own question, and the affected variants are then held
  until the rerun; a variant's own files are never overwritten (a corrected method is a new variant). (b) How the
  markers and flag files work: the readiness marker `I_AM_INSTALLABLE.json` (marked once in DEV, bound to the files,
  serves every tree), the environment marker `ENVIRONMENT_VERIFIED.json`, the status file, the job lock, the
  install barrier and the not-current marker.
- **The runner's rulebook, DECIDED (owner):** the scratch folder is `D:\DELETE_ME\` (anything under it, for a
  purpose; usually `D:\DELETE_ME\a_p_r_i_r`); the runner may build a scratch tree's Python environment itself.
  **Claude does not object, with two conditions written into the candidate:** only a scratch tree's own copies of
  the two environment scripts are run (each works on the folder it lies in), never this repository's copies, so
  that the main `.venv` of the owner's real runs is never changed; and invented results only, as already agreed.
  **A correction of fact:** `install_upgrade_dependencies_into_venv.bat` does not create a missing environment (it
  stops if there is none), so the runner runs `create_venv.bat` first and then it.
- **The candidate:** `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_7/CLAUDE_v0_7_CANDIDATE.md` (SHA-256 `08b1df22...f4d841`), made
  from the installed v0.6 by `make_rulebook_v0_7.py` (nine counted edits; the exact diff beside it): a new section
  2A and pointers to it in rules 3, 7, 9 and 10 and sections 3 and 5; rule 10 gains the one exception for the test
  suite's known failures. **It has no force:** the installed rulebook is unchanged and stays v0.6 until the
  reviewer has reviewed the candidate and the owner has ratified it (RAT-44). It names the commands of build step
  3 ahead of their existence; it is to be read again when that step's package is built.
- Nothing here authorises any operation on the owner's PC.
- Next numbers: EX_285 (the reviewer's reply), entry 183, RAT-44.

## 183. 23 November 2026, 20:24 - OWNER: the order of the next steps (EX_285, then the rulebook reviewed and ratified, then the rest); H-1 v10 after step 2 is installed

- **The owner's words (20:24):** "how about Waiting on the reviewer's EX_285. then reviewer check The runner's rulebook
  and we ratify it, then the other steps." and "ok to a full H-1 v10 once step 2 is installed".
- **DECIDED (owner), the order:** (1) the reviewer's EX_285 on package STEP2_Research_Engine_v1r1; (2) the rulebook
  v0.7 candidate reviewed by the reviewer and ratified by the owner (RAT-44); (3) then the other steps.
- **Claude's proposal within that order, awaiting the owner's word:** after RAT-44, a Windows rehearsal of step 2 by
  the runner (the suite in a task clone; a scratch tree on invented results under `D:\DELETE_ME\a_p_r_i_r\` running the
  real launchers, with a planted interruption), before the owner's own install of step 2 and DEV's first fill. For
  it the candidate needs one amendment: a scratch tree on D: receives code only, never `source_data`, `results` or
  `transitory_data`; the suite stays in task clones under the existing rules.
- **DECIDED (owner): H-1 v10,** a full refresh of the primary handover, is written once step 2 is installed.
- Nothing here authorises any operation on the owner's PC.
- Next numbers: EX_285 (the reviewer's reply), entry 184, RAT-44.

## 184. 23 November 2026, 20:28 - OWNER: real results may be used in the runner's scratch folder; the rulebook v0.7 candidate amended

- **The owner's words (20:27):** "section 2A says no real draw may be copied into the scratch folder - so lets remove
  that and related limitations instead, there is no good reason for that can see for such things introduce
  additional overheads we do not need."
- **DECIDED (owner):** the candidate's "invented results only" limit and the limits that followed from it are
  removed. Claude does not object: the limit was a carry-over of the former holdout rule, and the project's own
  rule that only the owner's runs of the reviewed programs count already covers what a scratch run computes.
- **The candidate as amended** (`exchange/CLAUDE_WEB_TOOLS/rulebook_v0_7/CLAUDE_v0_7_CANDIDATE.md`, SHA-256 `8edb63d8...95e8d5`;
  `make_rulebook_v0_7.py`, now twelve counted edits; the diff beside it): a task may copy this repository's accepted
  results and records into a scratch tree by reading, and under `D:\DELETE_ME\` the runner may read anything and run
  the system on real draws; rules 4, 5 and 9 and section 7 point to section 2A for that folder only. **Kept, because
  they protect real things and cost nothing:** nothing is ever written to this repository's `source_data`, `results`
  or `transitory_data`; a scratch run is a rehearsal, never a result of the project, and nothing of it but the report
  enters the repository; never the updater or any lottery website; never the real QA or PROD; the real DEV tree only
  as a place to copy from; the main `.venv` never changed.
- **It has no force** until the reviewer has reviewed it and the owner has ratified it (RAT-44); the installed
  rulebook stays v0.6.
- Next numbers: EX_285 (the reviewer's reply), entry 185, RAT-44.

## 185. 23 November 2026, 20:30 - OWNER: nothing ever leaves the runner's scratch folder; the rulebook v0.7 candidate amended

- **The owner's words (20:30):** "yes software and data etc and anything else in and created within DELETE_ME only every
  stays within that tree and/or is deleted, it never exfiltrates."
- **DECIDED (owner):** everything in `D:\DELETE_ME\` and everything created there stays there until it is deleted
  there; nothing of it is copied, moved or sent anywhere else (not into the repository or a task clone, not to
  another drive, not over the network). A step that would is a STOP. **Claude's reading, written into the candidate:**
  the runner's report in `outbox\`, which records what the commands printed, is the one thing that leaves; without it
  no rehearsal could be checked. The owner may say otherwise.
- **The candidate** (`exchange/CLAUDE_WEB_TOOLS/rulebook_v0_7/CLAUDE_v0_7_CANDIDATE.md`, SHA-256 `7b4c424d...14d882`): a new item
  4 of section 2A says this; the items after it are renumbered. Still no force until review and RAT-44.
- Next numbers: EX_285 (the reviewer's reply), entry 186, RAT-44.

## 186. 23 November 2026, 20:32 - OWNER: the runner's report, and anything else Claude names, may leave the scratch folder into outbox; the rulebook v0.7 candidate amended

- **The owner's words (20:32):** "i AGREE the runner's report AND anything else you specify as needed at any time may
  go into in `outbox\ upon your decision to do so.`"
- **DECIDED (owner):** what leaves `D:\DELETE_ME\` is the runner's report and anything else the web chat names in a
  task file, and only into `outbox\`. Everything else stays there until it is deleted there.
- **How, without new machinery:** what is named is copied into the report itself, as text under a heading that
  names where each came from. The runner's commit tool (`tools\cc_clone.py commit-report`) commits the one report file
  and nothing else; files beside the report wait until that tool is extended, which Claude does when a task first
  needs it.
- **The candidate** (`exchange/CLAUDE_WEB_TOOLS/rulebook_v0_7/CLAUDE_v0_7_CANDIDATE.md`, SHA-256 `52797e44...e4bcdf`): section 2A
  item 4 says this. Still no force until review and RAT-44.
- Next numbers: EX_285 (the reviewer's reply), entry 187, RAT-44.

## 187. 23 November 2026, 20:53 - EX_285 received (the two EX_283 blockers CLOSED; one new blocker F285-B01); fixed; package STEP2_Research_Engine_v1r2 built; EX_287 waits for the owner's word; EX_286 reserved for the rulebook review

- **The owner's message (20:35), relaying the reviewer:** "ChatGPT has completed EX_285 and committed it at `b5a167a`.
  The two original EX_283 blockers are CLOSED, and the league-report correction is accepted. EX_285 identifies one
  new blocker, F285-B01: unrestricted deletion from `records/status_staging`, including possible deletion outside the
  tree through a linked directory. Please consider EX_285 and prepare the smallest safe correction, with targeted
  synthetic tests. Do not install or run anything on the owner's PC. Meanwhile, ChatGPT is separately reviewing the
  Claude Code runner rulebook v0.7 candidate at `6a5d770`, as requested by the owner. Its review is to be EX_286, so
  please reserve that number for the rulebook review and use the next available number for any STEP2 correction
  exchange. The installed runner rulebook remains v0.6. Neither the candidate nor this message authorises runner
  activity or other PC operations."
- **Numbers:** EX_286 is reserved for the reviewer's review of the rulebook v0.7 candidate. The step 2 correction is
  **EX_287** (EX_285 itself said "reply as EX_286"; the owner's instruction governs).
- **F285-B01, accepted as found:** the cleanup added for F283-B01 removed every file in `records/status_staging`
  without checking the folder or the files; through a linked folder it could have deleted files outside the tree.
  **Corrected (code at main `469f088`):** `job_lock.check_real_folder` refuses a folder that is or lies under a link or
  a junction or whose real place is not inside the tree; the cleanup removes only files named as the status writer
  names them, for a variant folder the tree holds, and refuses with nothing deleted if anything else is there; the
  writer makes the same check and refuses a staged name that is a link. One step beyond the finding, put to the
  reviewer: the same check for the five working folders before the job lock is taken, in the job and the withdrawal.
- **Package `STEP2_Research_Engine_v1r2`** (`exchange/CLAUDE_WEB_TOOLS/step2/package_v1r2/`, base `469f088`; six files differ
  from v1r1). Note v0.3. Evidence (`evidence_v1r2/`): 191 engine tests pass; all 571 old tests the same, 762 after; 36
  of 36 planted faults caught; the install rehearsed in an LF and a CRLF clone with seven STOP cases; the corrected
  engine run over the cloud's real fill computes nothing and rewrites no report (suggestive only). **Packages v1 and
  v1r1 are superseded: not to be installed.**
- **Not executed by Claude:** Windows junctions. The check does not rest on one call, and the suite exercises
  whichever kind of link the owner's account can make when he runs the sheet.
- EX_287 (body and assembler ready) is issued only on the owner's word. Nothing is authorised on the owner's PC.
- Next numbers: EX_286 (the reviewer, the rulebook), EX_287 (Claude, step 2), entry 188, RAT-44.

## 188. 23 November 2026, 20:54 - EX_286 received (the rulebook v0.7 candidate: RECHECK, three narrow corrections of wording); the v0.7r1 candidate made

- **EX_286 (reviewer; main `10108e2`):** RECHECK, not PASS for RAT-44 as written; the scratch-runner capability is
  supported subject to three corrections of text. F286-B01 (BLOCKER): rule 11 still said "Never read or edit an
  ENVIRONMENT.ini file. Never create a tree", which section 2A's scratch trees contradict. F286-C01: section 7's
  exception was narrower than the owner's decision of entry 186. F286-C02: say that what the two scratch
  environment scripts call themselves (activation, pip) is part of running them. The four questions put to it were
  accepted: the D: boundary in principle, the package downloads, the rule 10 exception, the step 3 names as inert.
- **All three accepted and made:** `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_7/CLAUDE_v0_7r1_CANDIDATE.md` (SHA-256
  `a0fd3526...dceb11`), by `make_rulebook_v0_7r1.py` (seven counted edits to the v0.7 candidate as reviewed, checked by
  its hash), with the exact diffs from the installed v0.6 and from the v0.7 candidate. Rule 11 now names the owner's
  real QA and PROD trees, keeps them out of reach without exception, and has the one scratch-only qualification
  for a tree and its settings file, in the reviewer's words. **Two additions of Claude's:** rule 11's example places
  are brought up to date (entry 181: `T:\a_p_r_i_r`, `G:\a_p_r_i_r`, `T:\a_p_r_i_r_backups`); and section 2A says that a
  command's name in the list is no permission by itself (the reviewer's answer (d)).
- **It has no force.** The installed rulebook stays v0.6 until the owner ratifies a candidate (RAT-44). EX_286 leaves
  to the owner whether a focused textual recheck comes first.
- Next numbers: EX_287 (Claude, step 2, on the owner's word), entry 189, RAT-44.

## 189. 23 November 2026, 21:05 - EX_288 issued on the owner's word (build step 2 corrected, package v1r2, for recheck); the link tests stay in

- **The owner, 20:57, in answer to the two things waiting on him** (1: issue the step 2 message; 2: the five tests
  that make a link or a junction in Python's temporary folder, recommendation to leave them in): "RE 1. ok go
  please. 2. 2. ok to your recommendation. chatgpt is considering your blurb now."
- **The number is EX_288, not EX_287.** While the message waited, the reviewer took EX_287 for its focused recheck of
  the rulebook (main `4b50be8`; entry 190). A number is never reused (exchange/README.md), so the step 2 message
  takes the next free one. New files `EX_288_body.md` and `assemble_ex288.py` (`exchange/CLAUDE_WEB_TOOLS/step2/`) were
  made from the unissued drafts `EX_287_body.md` and `assemble_ex287.py`, which stay in the repository as they were:
  **they were never issued and are not a message.**
- **Issued:** `exchange/EX_288_Claude.zip` (SHA-256 `a714e930f966701ce4663f653d1a01c29e890ac1cfff62efbc49a6287e5554e2`) and the
  folder `exchange/EX_288_Claude/` with the message, the package ZIP `STEP2_Research_Engine_v1r2.zip` (SHA-256
  `a6c1842c3b5a67f2fcf4d7dc9aa386638582bbef15e1ee4fe2bcde602cb673ac`, the committed package byte for byte), its member list
  and the package extracted (41 files, each equal to the member list by hash). It replies to EX_285 and asks a
  recheck of F285-B01. Base `469f088`.
- **The link tests stay in (owner's decision).** Five tests of the package make a link or a junction: four of the
  class `TheStagingFolderIsTheTreesOwn` (new in v1r2) and one in `tests/test_research_identity.py` (there since v1).
  Each works only inside Python's own temporary folder and skips if the account can make neither. The message
  says so to the reviewer.
- Nothing is authorised on the owner's PC. A PASS, when it comes, authorises no install or run.
- Next numbers: the reviewer's reply to EX_288 takes the next free number; entry 190; RAT-44.

## 190. 23 November 2026, 21:06 - EX_287 received (the rulebook v0.7r1: the three findings of EX_286 CLOSED; one last correction of wording, F287-C01); the v0.7r2 candidate made

- **EX_287 (reviewer; main `4b50be8`):** F286-B01, C01 and C02 CLOSED; the seven edits, both diffs and the hash
  verified by its own application of the patches; the two additions of entry 188 accepted. **One erratum,
  F287-C01:** rule 11 ended "If a task step names one of these places, that is a STOP", and "these places" included
  the real DEV tree, so a step that names DEV as the place to copy from by reading (section 2A item 3; owner, entry
  184) would be a STOP. The reviewer says the wording came partly from its own suggestion in EX_286. Also: section
  2A item 5 still said "(rule 11 is unchanged)". It asks a corrected candidate with a diff and a hash; no wider
  review and no test on the PC.
- **The owner, 21:01, relaying it:** "I'll ratify this as soon as you tell me to".
- **Made:** `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_7/CLAUDE_v0_7r2_CANDIDATE.md` (SHA-256
  `faed89593e49c60f67789955a7e54f4bf3dd7a79c3cd5e76d4d7fdc71dc00e43`), by `make_rulebook_v0_7r2.py`: three counted edits to the
  v0.7r1 candidate as reviewed (checked by its hash): the version line; rule 11's last two sentences; the
  parenthesis in section 2A item 5. Diffs: `CLAUDE_v0_7r1_TO_v0_7r2_CANDIDATE.diff` (3 hunks) and
  `CLAUDE_v0_6_TO_v0_7r2_CANDIDATE.diff` (8 hunks); each, applied with `patch`, gives the candidate byte for byte.
- **Rule 11 now ends:** "This exception never permits a write to the owner's real DEV tree beyond what sections 3
  and 4 allow, any access to his real QA or PROD trees or their backup folders, or reading or editing a real
  tree's `ENVIRONMENT.ini`. A task step that asks for any of those is a STOP. Copying from the real DEV tree into a
  scratch tree by reading, which section 2A item 3 permits, is not."
- **One phrase beyond the reviewer's example, Claude's:** "beyond what sections 3 and 4 allow". Without it the
  sentence would, read to the letter, make the runner's own report in `outbox\` (a write in DEV that section 3
  allows) a STOP: the same kind of fault as the one being corrected.
- **It has no force.** The installed rulebook stays v0.6 (SHA-256 begins `f92f17f60db63990`) until the owner ratifies
  (RAT-44). EX_287 says he may ratify the corrected bytes, after a focused verification if he wishes.
- Next numbers: the reviewer's reply to EX_288 takes the next free number; entry 191; RAT-44.

## 191. 23 November 2026, 21:08 - The two unissued EX_287 drafts removed at the owner's request

- **The owner, 21:06:** "re two unissued drafts named `EX_287_body.md` and `assemble_ex287.py` are still in the
  repository, untouched, and the decision log says they were never a message - please remove them."
- **Removed** from `exchange/CLAUDE_WEB_TOOLS/step2/`: `EX_287_body.md` and `assemble_ex287.py` (entry 189: Claude's drafts
  of the step 2 message under the number the reviewer then took; never issued). Git keeps them in its history
  (last present at main `bf0251b`). Their content, corrected, is `EX_288_body.md` and `assemble_ex288.py`, from which
  EX_288 was made. Nothing else is removed. The only EX_287 is the reviewer's, `exchange/EX_287_ChatGPT.md`.
- Next numbers: the reviewer's reply to EX_288 takes the next free number; entry 192; RAT-44.

## 192. 23 November 2026, 21:12 - RAT-44: THE OWNER RATIFIES the local runner rulebook v0.7 (the candidate v0.7r2); installed by Claude with the status change only

- **The owner's words (21:06):** "I ratify v0.7r2 (RAT-44)". Before them (21:01, entry 190): "I'll ratify this as soon
  as you tell me to".
- **What was ratified:** `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_7/CLAUDE_v0_7r2_CANDIDATE.md`, SHA-256
  `faed89593e49c60f67789955a7e54f4bf3dd7a79c3cd5e76d4d7fdc71dc00e43` (entry 190).
- **What the reviewer had read, stated exactly:** the v0.7 candidate (EX_286: RECHECK, three corrections) and the
  v0.7r1 candidate (EX_287: those three CLOSED, one correction of wording, F287-C01, and "The owner may then consider
  RAT-44 on the corrected bytes, after a focused verification if desired"). **The reviewer has not read v0.7r2's three
  edits** (the version line; rule 11's last two sentences, with Claude's phrase "beyond what sections 3 and 4 allow";
  section 2A item 5's parenthesis). The owner was told so and offered the reviewer's look first; he ratified. The
  reviewer is told of the final bytes by the paste block.
- **RAT-44 is recorded** (RAT-43 was the last number used). **Installed:** `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`,
  **SHA-256 `3e6125f137e12266a3979c4fe173d8752207bf7163ac53c11bf6f6cf14bb121f`** (21,032 bytes), written by
  `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_7/finalise_rat44.py` from the ratified candidate (asserted by hash) over the
  installed v0.6 (asserted by hash, `f92f17f6...fdfa632`; Git keeps it). **One line differs from the ratified
  candidate, the version line's status words** (`CLAUDE_v0_7r2_CANDIDATE_TO_FINAL.diff`, one hunk; applied to the
  candidate with `patch` it gives the installed file byte for byte; every line after the version line is identical).
  No rule text differs from what was ratified.
- **What v0.7 adds:** section 2A, the scratch folder `D:\DELETE_ME\` for rehearsals of the new system's commands,
  only when a task file says so; real results may be copied in and used there; nothing leaves it but the report
  and the text a task file names; a scratch tree's own Python environment; rule 10's one exception for the suite's
  known failures; rule 11 for the owner's real QA and PROD trees with its one scratch-only qualification.
- **RAT-44 authorises the documentation-only installation and nothing else:** no runner task, no rehearsal, no
  install or run of step 2, nothing on the owner's PC. A rehearsal needs a task file and the owner's own go.
- **A fact for the rehearsal's design, found while installing (not acted on):** the owner's `.claude/settings.json`,
  which only he changes, still denies the runner every command that contains `.bat`, `install_upgrade_dependencies`
  or `activate_venv`, every `rm`, `rmdir`, `del` and `Remove-Item`, and reading any `source_data` or `results` folder
  wherever it lies. So the rulebook now allows a scratch rehearsal that those settings would still stop. How the
  rehearsal is to be run (the owner changes named lines of his file; or one reviewed Python program of the task
  runs the scratch tree's launchers; or the owner runs it from a sheet) is the owner's decision, to be put to him
  with the task file's design. Nothing is to be worked around.
- **A running Claude Code conversation keeps the rulebook it started with:** after `git pull --ff-only`, start a new
  Claude Code conversation before the next task.
- **Owed at the next register edition:** RAT-41's install, RAT-42, RAT-43 and RAT-44 (register v0.32 is not edited).
- Next numbers: the reviewer's reply to EX_288 takes the next free number; entry 193; RAT-45.

## 193. 23 November 2026, 21:16 - Claude's mistake in the RAT-44 commit put right: three record files had lost their CRLF line endings

- **What happened.** The commit of entry 192 (main `063630f`) changed five lines of `exchange/OWNER_REMINDERS.md`, two of
  `exchange/OWNER_ROADMAP.md` and one of `exchange/CLAUDE_WEB_TOOLS/README.md`, and Claude's script wrote all three back
  with LF line endings where they hold CRLF. Git therefore showed nearly every line of them as changed. No wording
  was lost or altered beyond the lines of entry 192. Claude saw it in the size of the commit, straight after the push.
- **Put right in the next commit:** the three files are CRLF again, every line. Checked with `git diff --numstat`
  against the commit before entry 192 (`d73ed80`): 5 lines added in the reminders, 2 added and 1 removed in the
  roadmap, 1 added in the tools README, and nothing else. The rulebook, the decision log and the continuity page
  were not affected (they are LF and stayed LF).
- **Why it was not caught before the push:** Claude looked at the list of changed files and not at the count of
  changed lines. The count is looked at before every commit from now on.
- Next numbers: the reviewer's reply to EX_288 takes the next free number; entry 194; RAT-45.

## 194. 23 November 2026, 21:20 - EX_289 received: the reviewer's FOCUSED RECHECK PASS on the exact v0.7r2 bytes the owner ratified

- **EX_289 (reviewer; main `0a4ec56`, committed 21:08, two minutes after the owner's ratification):** "FOCUSED RECHECK
  PASS. F287-C01 is CLOSED." It computed the candidate's SHA-256 itself (`faed8959...1dc00e43`, the ratified bytes),
  applied both diffs and got the candidate exactly, and found no unreported change. Of Claude's added phrase it
  says: "a sensible improvement over my example in EX_287: it preserves the runner's already authorised outbox report
  and checked commit-report operation." It read the repository at `bf0251b`, where the installed file was still v0.6;
  the install of entry 192 came after.
- **So entry 192's statement is overtaken:** it said the reviewer had not read v0.7r2's three edits. That was true when
  the owner ratified; the reviewer has since read and passed them. Every byte of the ratified rulebook has now been
  reviewed.
- **One line of the installed rulebook says the old thing.** Its version line reads "(the candidate v0.7r2; its last
  three edits, which EX_287 asked for, were ratified without a further review)". No rule is affected. Changing an
  installed, ratified rulebook is not Claude's to do unasked: put to the owner, with the recommendation to change
  those status words to name the PASS of EX_289.
- **Numbers:** EX_289 is the reviewer's, on the rulebook. EX_288 (step 2) is still unanswered; its reply takes the
  next free number.
- Nothing is authorised on the owner's PC. A rehearsal needs a task file and the owner's own go (entry 192).
- Next numbers: the reviewer's reply to EX_288 takes the next free number; entry 195; RAT-45.

## 195. 23 November 2026, 21:13 - The installed rulebook's version line corrected at the owner's word (it now names the PASS of EX_289); no rule text touched

- **The owner, 21:11, to the two things of entry 194:** "thing 1 - yes. thing 2 - tell me precisely what to change in
  which file." Thing 1 was the version line; thing 2 is his `.claude/settings.json` and the scratch rehearsal (answered
  in the chat; no file of his is changed by Claude).
- **Done for thing 1:** `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_7/correct_rat44_status.py` checked the installed rulebook by
  hash (`3e6125f1...14bb121f`) and made one replacement that matched once. The version line's words "(the candidate
  v0.7r2; its last three edits, which EX_287 asked for, were ratified without a further review)" are now "(the
  candidate v0.7r2), and passed by the reviewer in those exact bytes the same evening (EX_289)".
- **Installed now:** `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`, **SHA-256
  `4416c4b574567f57f40d19ba9d58a765ce7dce551cf06937430aced730325456`** (21,021 bytes). `git diff --numstat`: 1 line added, 1
  removed. Every line after the version line equals the ratified candidate v0.7r2 (checked with `diff`). The exact
  change is `CLAUDE_v0_7_STATUS_CORRECTION.diff`.
- It is still rulebook v0.7 under RAT-44: a correction of a statement of fact in its status words, not a new edition.
- **A correction of times, Claude's:** the headings of entries 192, 193 and 194 say 21:12, 21:16 and 21:20. Claude wrote
  those times by estimate and not from the clock; they run some minutes ahead. By the clock the three were
  committed between 21:07 and 21:12 Australia/Adelaide (Git holds each commit's time). The entries are not edited.
  From this entry on, a heading's time is read from the clock when the entry is written.
- Next numbers: the reviewer's reply to EX_288 takes the next free number; entry 196; RAT-45.

## 196. 23 November 2026, 21:14 - The owner's settings file and the scratch rehearsal: what was checked, one statement of entry 192 corrected, the choice put to the owner

- **The owner, 21:11:** "thing 2 - tell me precisely what to change in which file." And at 21:13: "please give me a new
  blurb for chatgpt when you are ready" (for EX_288; given in the chat).
- **Checked against Claude Code's own documentation** (code.claude.com/docs/en/permissions and /tools-reference, read
  23 November 2026), not from memory: a deny rule is matched before any allow rule and an allow rule cannot make an
  exception to it; a `Bash(...)` rule is matched against the text of the command as the runner types it, `*` standing
  for any text; it does not reach what a program started by that command does; `Read(...)` and `Edit(...)` rules
  written without a leading `/` or `//` apply under the current directory.
- **Correction to entry 192** (and to the lines written from it in the continuity page and reminder R-030 (f), now put
  right): it said the settings deny "reading any `source_data` or `results` folder wherever it lies". Not so. Those
  three `Read(**/...)` lines bind the runner's own file tools under the folder it works in, which is the
  repository. They do not reach `D:\DELETE_ME\`, and they never bound a program the runner starts. What does stand in
  the way of a scratch rehearsal is two lines: `"Bash(*.bat*)"` and `"Bash(*install_upgrade_dependencies*)"` (the
  delete lines matter only for the clean-up).
- **What the project already does about such lines:** `CLAUDE_CODE_WORKING_FOLDER_TREE/tools/cc_clone.py` is a checked
  helper that the runner starts with one Python command and that itself does `git clone`, `git add`, `git commit`
  and the deletion of a task clone, each of which the same settings file denies when typed; its own header says a
  denied path "is never typed". Rulebook section 4 requires it. The deny lines stop typed commands; the project's
  checked tools do the work after checking where they are.
- **The choice put to the owner (his decision; nothing done):** (A) he deletes those two lines from
  `.claude/settings.json`, which also removes the hard block on the same typed commands in the real tree, since a
  pattern cannot tell `D:` from `E:` reliably; or (B) no change to his file, and Claude writes one more checked helper
  in the pattern of `cc_clone.py`, which refuses any tree whose root is not under a real `D:\DELETE_ME\` and runs that
  tree's own launchers; it goes to the reviewer with the task file. Claude recommends (B).
- Next numbers: the reviewer's reply to EX_288 takes the next free number; entry 197; RAT-45.

## 197. 23 November 2026, 21:25 - The owner chose option A: two deny lines removed from his `.claude/settings.json`; EX_288's blurb sent to the reviewer

- **The owner, 21:24:** "i did option A. blurb sent to chatgpt."
- **Checked on GitHub (his commit `664f5d3`, merged at main `92a343c`):** `.claude/settings.json` lost exactly two lines of its
  deny list, `"Bash(*install_upgrade_dependencies*)"` and `"Bash(*.bat*)"`; nothing else in the file changed; it is valid
  JSON with 109 deny lines. Claude changed nothing in it.
- **What that means from now on.** The runner can type a command that names a `.bat` or the dependency script. In the
  real tree such a command is now stopped by the rulebook (rules 7 and 9) and by the owner's own answer to the
  approval prompt, no longer by a hard deny. The deny lines for the old coordinator, the experiment and evaluation
  launchers, the results updater, `activate_venv`, `pip`, every delete, every push and the rest stand as before.
- **For the task file's design:** the delete lines stand, so a scratch folder is cleaned up by the owner or left; a
  typed command must still avoid every remaining denied word (for example `results_master`, `pip`, `conda`).
- **Not authorised by this:** any runner task. A rehearsal needs a task file, the reviewer's PASS of what it runs
  (rulebook section 2A item 5: "reviewed and installed"), and the owner's own go.
- Next numbers: the reviewer's reply to EX_288 takes the next free number (EX_290 as of now); entry 198; RAT-45.

## 198. 23 November 2026, 21:31 - EX_290 received: PASS for build step 2, package STEP2_Research_Engine_v1r2 (F285-B01 CLOSED; the five-folder check accepted)

- **EX_290 (reviewer; main `540a778`; `exchange/EX_290_ChatGPT.md`, SHA-256
  `9903cafccc4d23ee1ce43c0c8024733db8ad82f776cec9d9b5802313a79b7378`):** "PASS - F285-B01 CLOSED." and "ACCEPT the
  five-working-folder preflight in EX_288 section 2." It checked for itself: of the 35 files of `repo_overlay`, exactly
  six differ from v1r1 and 29 are byte-identical; the six hashes; the outer ZIP (`a714e930...5554e2`) and the package
  ZIP (`a6c1842c...b673ac`) from the bytes GitHub holds. It read the diff, the guards, the launch sites and the six
  new tests. "No code-change request or another reviewer recheck is outstanding for this exact package."
- **What it did not do, in its own words:** it did not run the suite, the new tests, the Windows launchers or any
  real-data run. The 191 tests, the 571 unchanged, the 36 planted faults and the install rehearsals are Claude's
  cloud evidence, inspected as artefacts. Two limits it names: the guard is for one writer under the job lock, not
  for another process swapping folders during the check; and the five-folder check covers those five folders, no
  more.
- **The owner, 21:30, relaying it:** "Please record EX_290's PASS and proceed according to the owner's decisions and
  existing installation gates."
- **So the review of build step 2 is finished after three rounds** (EX_283, EX_285, EX_290). The package to install is
  `exchange/CLAUDE_WEB_TOOLS/step2/package_v1r2/STEP2_Research_Engine_v1r2.zip` with its `INSTALL_AND_RUN_SHEET.md`;
  base `469f088`. Packages v1 and v1r1 stay superseded.
- **The gates that remain, each the owner's own go, none given:** (1) a rehearsal by the runner in the scratch
  folder, if he wants one first (Claude's proposal; three points put to him at 21:26, not yet answered); (2) the
  install in DEV, sheet parts 1 to 5; (3) separately, DEV's first fill, sheet part 6, then part 7. After the
  install: H-1 v10 (entry 183).
- A PASS authorises no install or run. Nothing is authorised on the owner's PC.
- Next numbers: EX_291; entry 199; RAT-45.

## 199. 23 November 2026, 21:40 - The owner chooses to rehearse first; TASK_T025 written (the step 2 rehearsal on Windows); not started, not authorised to run

- **The owner, 21:32, to the choice of entry 198 (a rehearsal by the runner first, or the install in DEV now):** "lets
  do rehearse first". He did not answer the two points put with it (the scope; whether the reviewer looks at the
  task file first), so Claude took its own proposals: the scope as proposed, and one short look by the reviewer
  unless the owner says otherwise.
- **Written:** `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T025.md` (SHA-256 `a360c8fc2c82d14d5f90de1fbd62ca2b2c095e794ba67df0dd35d0b63f3aa5b2`), with
  `TASK_T025_overlay_plan.txt` and `TASK_T025_ENVIRONMENT.ini`; made by `exchange/CLAUDE_WEB_TOOLS/t025/make_task_t025.py` from
  `TASK_T025_template.md` (each long path defined once). 33 steps, about two hours on the owner's PC.
- **What it does.** Steps 1 to 16, in a task clone with the main Python and the existing clone tool, as earlier
  tasks: the suite as it is today, the package's verifier before the copy, the 35 files copied in, the verifier
  after, the suite again and its comparison, the commit in the clone, the verifier's committed phase (the sheet's
  parts 1 to 4). Steps 17 to 29, under `D:\DELETE_ME\a_p_r_i_r\T025\` by rulebook v0.7 section 2A: the clone's files
  copied to a scratch tree, its own `.venv` built by its own two scripts, `Run_Research.bat --game BOTH --no-update`
  twice (the first fill on the real results, then a job with nothing new), `Withdraw_Variant.bat` started with no
  variant, the old run folders copied from DEV by reading, and the comparison with the old records (parts 5 to 7).
- **What it leaves out, and why.** A planted interruption: on Windows it would mean ending a process, which the
  owner's rules forbid; the suite covers crash recovery on invented data. The clean-up of the scratch folder: the
  owner's settings deny the runner every delete, so the owner deletes `D:\DELETE_ME\a_p_r_i_r\T025` himself later.
- **Checked by Claude, in the cloud:** the six Python one-liners compile; the 33 steps are in order; no command
  contains a word the owner's settings deny; every D: path lies under `D:\DELETE_ME\`. **Not executed by Claude:**
  any command of the task on Windows. A `.bat` started from Git Bash by its full path, and whether the settings'
  `Read` lines stop the copy of step 26, are the two things most likely to stop it; step 26 says what to do if
  refused.
- **Not authorised by this:** running the task. It needs the owner's own go ("Do inbox\TASK_T025.md" to the runner),
  after his `git pull --ff-only` and in a new Claude Code conversation.
- Next numbers: EX_291; entry 200; RAT-45.

## 200. 23 November 2026, 22:00 - EX_291 received (TASK_T025 cold read: RECHECK, four corrections of the task's text); all four made (TASK_T025 r1)

- **EX_291 (reviewer; main `6541c9c`), relayed by the owner at 21:58 with a clarification:** the rehearsal's design is
  accepted (the clone and scratch separation, the scratch settings, the copy from DEV by reading, the verifier, the
  tests, the report); no safety objection; four corrections before the owner's go. F291-B01: step 25 made an
  argument error on purpose and then passed over it, against rule 10. F291-B02: step 26 treated a refusal by the
  permission system as if the old run folders were absent. F291-C01: step 28's two `grep -c` commands exit 1 when
  the right count is 0. F291-C02: step 30 tried to remove a clone that an early STOP never made, which would block
  the report's commit.
- **All four accepted and made, and nothing else changed:**
  1. Step 25 runs `Withdraw_Variant.bat --help`; expected the help text and exit code 0 (the text was checked by
     running the command's `--help` in the cloud); anything else is a STOP.
  2. Step 26 lists the parent folder `results\real\development` and looks for the name `contract_runs` in the list.
     Only a list without that name gives `OLD RUN FOLDERS NOT PRESENT`. A refusal by the permission system, a folder
     that cannot be listed or read, a failed copy or another exit code is a STOP. The logic was run in the cloud in
     three cases: present (copied, exit 0), absent (not present, exit 0), parent missing (error, exit 1).
  3. Step 28 says that for its two count commands exit code 1 with a printed `0` is not an error; exit code 2, no
     number, or a code that does not fit the number is a STOP. The comparison's own criteria (step 29) are unchanged.
  4. Step 30 first prints whether the task's folder exists; if not, "nothing to remove" is recorded and the report
     follows; otherwise the existing guarded removal. The scratch folder on D: is left alone in every case.
- **Files:** `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T025.md` (SHA-256 `c9482a9a5c87edf57834d5d1118309dbab44aea553baae3ba3e1018dc5215fb5`; its header says r1); the exact
  change `exchange/CLAUDE_WEB_TOOLS/t025/TASK_T025_TO_r1.diff` (SHA-256 `cec4a4734d43cef026c815f50a3d90b2f71c821a85f77f053b709363fabd211c`; 14 lines added, 10 removed); the plan
  file and the settings file are unchanged. 33 steps as before.
- **How the process went (Claude's note):** B01 and B02 were the same fault, twice: I wrote "this is not a STOP" to save
  a round trip, where the rulebook I had just had ratified says a STOP is a STOP. The cold read caught both.
- **Not authorised by this:** running the task. Only the owner's go to the runner starts it.
- Next numbers: EX_292; entry 201; RAT-45.

## 201. 23 November 2026, 22:13 - EX_292 received: PASS for the text of TASK_T025 r1; the task waits for the owner's go

- **EX_292 (reviewer; main `6796f95`; `exchange/EX_292_ChatGPT.md`, SHA-256
  `13a2bfd95e7989f1b737bcfe36c094d7e09ec60be875847427e764ddb3d53845`):** "PASS for the text of TASK_T025 r1. F291-B01,
  F291-B02, F291-C01 and F291-C02 are CLOSED." It verified both hashes and rebuilt the corrected task from the diff.
  A cold read only: it ran no command and no Windows test.
- **The task as passed:** `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T025.md`, SHA-256
  `c9482a9a5c87edf57834d5d1118309dbab44aea553baae3ba3e1018dc5215fb5` (unchanged since main `b963cdd`; checked at `6796f95`).
- **Still the owner's own go, not given by this:** "Do inbox\TASK_T025.md" to the runner, after `git pull --ff-only`, in a
  new Claude Code conversation, with the folder `D:\DELETE_ME` existing and nothing of the project running. About
  two hours. Afterwards: he pushes the report; Claude reads it; he deletes `D:\DELETE_ME\a_p_r_i_r\T025` when Claude
  says so. Then his own install in DEV (sheet parts 1 to 5) and, separately, DEV's first fill.
- Next numbers: EX_293; entry 202; RAT-45.

## 202. 23 November 2026, 23:19 - TASK_T025 ran on the owner's go: STOP at step 20 (the scratch tree's environment script refused); steps 1 to 19 PASSED, the install sheet's parts 1 to 4 on Windows

- **The owner gave the runner the task at about 22:17** (after it answered his question on the rulebook: v0.7, RAT-44,
  section 2A and `D:\DELETE_ME\`), and pushed its report at 23:18: `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T025.md`,
  main `99465ff`, SHA-256 `37df8e8a6163ded0d21f15c21eea5c985d02f2578c9494ba3511e3ce69710992`. Task file at main `5ed656a` (r1, the text passed in EX_292). Windows 11, Python
  3.15.2 in the main `.venv`.
- **PASSED, each with the exact text and counts the task expects (steps 1 to 19):** the scratch check; the clone; 41
  files extracted; the suite as it is today (45 modules, 571 tests, 25 min 1 s); `PRE PASS`; 35 files copied (33
  new, 2 replaced); `POST PASS`; the suite again (52 modules, 762 tests, 28 min 41 s; the seven research modules
  `OK`); the comparison (`tests in both runs: 571; with the same result: 571`; the three known failures and no
  other; 198 new lines); 33 files added and 2 modified in the clone's commit; `COMMITTED PASS` (with
  `core.autocrlf` true); the clone's files copied to `D:\DELETE_ME\a_p_r_i_r\T025\tree`; the settings file copied.
  **So the sheet's parts 1 to 4 are proved on the owner's Windows PC, in a clone.**
- **The link tests on Windows.** Two tests skipped, both of which need a symbolic link, which this account cannot
  make: `...test_the_writer_refuses_a_staged_name_that_is_a_link_to_a_file_elsewhere` and
  `test_research_identity...test_a_path_through_a_link_refuses`. The other three link tests of
  `TheStagingFolderIsTheTreesOwn` did not skip and passed; as the account cannot make a symbolic link, they ran
  with a junction (the fixture's second choice). An inference from the skip counts, not a line of the report.
- **STOP at step 20:** `create_venv.bat` of the scratch tree printed `[VENV] ERROR: A virtual environment is already
  active` and ended with code 3, having created nothing. The runner's Git Bash shell already had `VIRTUAL_ENV` set
  to the main `.venv` before the task began (the runner's observation 1); the script refuses while any environment
  is active, as it is written to. The runner retried nothing. **The cause is known; it is not a fault of the
  package.** Steps 21 to 29 (the scratch `.venv`, the two launchers, the first fill, the second job, the comparison
  with the old records) did not run: **the launchers and a real fill are still not proved on Windows.**
- **Left in place:** `D:\DELETE_ME\a_p_r_i_r\T025` with `tree` (the clone's files after the install, and its
  `ENVIRONMENT.ini`; no `.venv`) and `evidence`. The task clone on E: was removed (`REMOVE PASS`). The main
  repository and the main `.venv` were not changed.
- **The runner's own deviations, as it reports them:** it put `cd` to MAIN and, for the long steps, a `date` stamp
  before some command lines, and added an `echo` of the exit code where the task gave none; and one of its own
  lines mangled a paragraph of the report, which it rewrote. No command of the task was affected. For the next
  task: give the recording of every exit code in the task's own lines, so that nothing is added.
- **For the operations manual and build step 3 (a finding of this rehearsal):** a tree's `.venv` is built from a plain
  CMD window with no environment active, not from a VS Code terminal or from the runner's shell.
- **Put to the owner (his decision):** how to finish the rehearsal. Claude recommends that he builds the scratch
  tree's `.venv` himself with its two scripts in a plain CMD window, and that a short second task then runs the
  steps that did not run, on the scratch tree as it stands.
- Next numbers: EX_293; entry 203; RAT-45.

## 203. 23 November 2026, 23:27 - The owner built the scratch tree's `.venv` himself; TASK_T026 written (the steps of TASK_T025 that did not run); not started

- **The owner, 23:25, taking the recommendation of entry 202:** "just did: cd /d D:\DELETE_ME\a_p_r_i_r\T025\tree
  create_venv.bat install_upgrade_dependencies_into_venv.bat INSTALL ... [DEPS] Generated environment snapshot:
  "D:\DELETE_ME\a_p_r_i_r\T025\tree\transitory_data\dependency_snapshots\environment_12633_6520.txt" [DEPS] SUCCESS.
  All 39 direct requirements installed; research compatibility tests remain required." (His own commands, in his own
  CMD window, in the scratch tree only.)
- **Written:** `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T026.md` (SHA-256 `473cd1ef8889247767603a6b107cd7891612fb62a7f82520a5a1a72413630cd8`), by
  `exchange/CLAUDE_WEB_TOOLS/t026/make_task_t026.py` from `TASK_T026_template.md`. 15 steps, about an hour. It works in
  TASK_T025's scratch folder `D:\DELETE_ME\a_p_r_i_r\T025\`, makes no task clone, builds no environment and has no
  network use.
- **Its steps 4 to 11 are TASK_T025 r1's steps 22 to 29**, the text the reviewer passed in EX_292: the scratch tree's
  Python; `Run_Research.bat --game BOTH --no-update` (the first fill); the same once more; `Withdraw_Variant.bat
  --help`; the old run folders copied from DEV by reading; the comparison with the old records and its criteria.
  The builder asserts that the 14 command lines of steps 4 to 10 equal those of the passed task, character for
  character, and that the passed task has the hash of EX_292.
- **New in it:** step 3 checks, before anything is written, that `D:\DELETE_ME` is an ordinary folder, that the
  scratch tree holds its settings file, its two launchers, the command program and its own Python, and that no
  research job has run in it yet; and the recording rules now say what the runner may add to a task line (`cd` to
  MAIN, an `echo` of the exit code, `date` with a format in Git Bash to print the time), after entry 202's deviations.
- **Already known from TASK_T025's step 20:** a `.bat` started from Git Bash by its full path runs and returns its
  own exit code (it printed its refusal and code 3).
- **Not authorised by this:** running the task. It needs the owner's own go to the runner, after `git pull --ff-only`,
  in a new Claude Code conversation. Whether the reviewer looks at it first is the owner's choice.
- Next numbers: EX_293; entry 204; RAT-45.

## 204. 23 November 2026, 23:31 - The owner decides to run TASK_T026 now, without a further look by the reviewer

- **The owner, 23:31, to the choice of entry 203 (run now, or the reviewer first):** "run now".
- **What that covers:** his go for TASK_T026 as committed at main `28e0bf5` (SHA-256
  `473cd1ef8889247767603a6b107cd7891612fb62a7f82520a5a1a72413630cd8`), which he gives to the runner himself, after
  `git pull --ff-only` and in a new Claude Code conversation. The reviewer has not read this task file; its commands
  under test are those of TASK_T025 r1, which it passed (EX_292).
- **Not covered:** the install of build step 2 in DEV, and DEV's first fill. Each is still his own separate go.
- Next numbers: EX_293; entry 205; RAT-45.

## 205. 24 November 2026, 05:50 - TASK_T026 ran: the launchers and the first fill PASSED on Windows; STOP at step 11 (the comparison tool); the cause found: a fault of Claude's comparison tool, not of the engine

- **The report:** `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T026.md`, main `dc0f532`, SHA-256
  `3b009412faea0169399f36203aafe584131c195f1e2cf3f9875f349e39838799`; run 23 November 23:33 to 24 November 00:27; the owner
  relayed the runner's result at 05:47. No deviations.
- **PASSED (steps 1 to 8), the things never before run on Windows:** `Run_Research.bat --game BOTH --no-update` from the
  scratch tree's own Python: the first fill of both games in 46 minutes, `The job finished.`, exit code 0, no
  `WARNING`, `REFUSED` or `STOP`; written POWERBALL 15118 forecasts and 15078 scores, OZLOTTO 6598 and 6558, **the same
  four counts as the cloud's fill**. The same job again: every count 0, 3 minutes. `Withdraw_Variant.bat --help`:
  the help text, exit code 0. The old run folders copied from DEV by reading (the settings did not refuse it).
- **The comparison (steps 9 to 11): STOP.** Part 1: all 34800 old score records equal the new score lists, `DIFFERENT: 0`
  (22884 and 11916). Part 2, POWERBALL: 17280 old forecasts read from the run folders, 14478 equal, `DIFFERENT: 2802`;
  OZLOTTO: 8760 read, 5958 equal, `DIFFERENT: 2802`; `RESULT: STOP`, exit code 1. The 20 `DIFFERENT` lines were counted
  and, as the task says, not copied.
- **The cause, worked out by Claude from the report's numbers and the cloud's copy of the same fill (not from the
  `DIFFERENT` lines, which Claude has not seen):** the old system kept a record, status `INSUFFICIENT_HISTORY`, for every
  target of its development walk-forward at which a variant did not yet have enough earlier draws. The new lists,
  as specification v0.6 section 5 says ("`TARGET` lines ... one per draw from `first_target`"), begin at each
  variant's `first_target` and hold no line before it. The comparison tool asked for a `NO_FORECAST` line for each
  such old record and so called it different. **The count fits exactly, in both games:** the forty variants' first
  targets lie 0 (8 variants), 25 (1), 51 (14), 103 (14) and 207 (3) draws after the old walk-forward's first target
  (read from the list headers of the cloud's fill: 1145, 1170, 1196, 1248, 1352 for POWERBALL; 1475, 1500, 1526, 1578,
  1682 for OZLOTTO), and 25 + 14 x 51 + 14 x 103 + 3 x 207 = 2802. The other number fits too: the new lists hold 16
  targets per variant that the old development runs never had (the 15 draws of the former holdout and the next
  draw), 640 lines, and 640 - 2802 = -2162, the tool's "lines the new lists hold for other targets".
- **What follows, if that is right:** every forecast the old system actually computed and kept (14478 and 5958,
  20436 in all) is in the new lists with the same view digest, scores, ranking, TOP and WORST. The engine did what
  the specification says. **The fault is in `tools/compare_fill_with_old_records.py`, Claude's:** that branch was never
  run on real run folders, because the cloud has none. **It is an inference until the corrected tool is run on the
  owner's run folders.**
- **Consequence for the package:** the tool is in `STEP2_Research_Engine_v1r2.zip`, and the install sheet's part 7
  expects `RESULT: PASS - COMPLETE`, so part 7 would stop in DEV as it did here. The engine's 35 files are not
  affected. Proposed to the owner: correct the tool (an old `INSUFFICIENT_HISTORY` record below the variant's
  `first_target` agrees when the new list has no line for it, and is counted apart), issue it to the reviewer as a
  new package revision with `repo_overlay` byte for byte unchanged, then rerun the comparison alone in the scratch
  tree. An EX is issued only on his word.
- **The scratch folder `D:\DELETE_ME\a_p_r_i_r\T025` stays:** it holds the fill and the copied run folders the rerun needs.
- **What a scratch run computes is a rehearsal, not a result of the project.**
- Next numbers: EX_293; entry 206; RAT-45.

## 206. 24 November 2026, 06:00 - The comparison tool corrected; package STEP2_Research_Engine_v1r3 built (the engine's 35 files unchanged); EX_293 issued on the owner's word

- **The owner, 05:54, to the recommendation of entry 205** (correct the tool; issue it to the reviewer as a package
  revision with the engine's files unchanged; after the PASS, rerun the comparison alone in the scratch tree; then
  his install in DEV): "yes to your recommendation".
- **The correction** (`exchange/CLAUDE_WEB_TOOLS/step2/compare_fill_with_old_records.py`, SHA-256 `b4135af7ea925caba020bcbc77185999f51837bff0dcedddeb295ff0d241ada6`): a new
  function reads each new list's `first_target` from its header; in part 2 an old `INSUFFICIENT_HISTORY` record whose
  target lies below that first target, and for which the new list has no line, agrees and is counted apart; every
  other case is judged as before. The part 2 line and the result line say the count; "lines the new lists hold for
  other targets" is now a count of lines and can no longer go negative. Part 1 and the exit codes are unchanged.
  The rule is specification v0.6 section 5.2 (a list's `TARGET` lines run from `first_target`).
- **The cause is now reproduced in the cloud:** the tool as passed (package v1r2), run on old run folders made up in
  the old form from the cloud's fill, prints the Windows report's seven lines number for number (17280 and 14478,
  8760 and 5958, `DIFFERENT: 2802` twice, `-2162` twice, 160 per-variant lines, 20 `DIFFERENT` lines, each with the
  reason "the new list has no line for it"). Still an inference about the owner's own folders until the rerun.
- **Evidence for the corrected tool** (`evidence_v1r3/`; cloud, Claude's): `check_compare_tool.py` gives
  `PASS - COMPLETE` on the made-up records (14478 and 5958 forecasts equal; 2802 and 2802 counted apart;
  `DIFFERENT: 0`; 640 new lines for other targets in each game) and reports each of four differences planted one at
  a time. The install rehearsed again with the new package: LF and CRLF clones, PRE, POST and COMMITTED PASS; seven
  STOP cases stop.
- **Package `STEP2_Research_Engine_v1r3`** (`exchange/CLAUDE_WEB_TOOLS/step2/package_v1r3/`; ZIP SHA-256 `e80e87ae4d0d9e9baaa15b8f2a405df717f66eb6be7de4126b734ad374bc6926`; base
  `469f088`): three files differ from v1r2 as passed: the tool, the sheet (the package's name in its paths; part 7's
  expected text) and the manifest's first line (the name). `repo_overlay` is byte for byte the 35 files passed in
  EX_290; the verifier is the same file. **Package v1r2 is superseded: the owner installs from v1r3's sheet.**
- **Issued:** `exchange/EX_293_Claude.zip` (SHA-256 `80fb7343d23ae79d9a60f23d3dd487f0039869583592a9bd3e1698d3f2fce2ef`) and the folder `exchange/EX_293_Claude/` (the message, the
  package ZIP, its member list, the package extracted: 41 files, each equal to the member list by hash). It asks a
  recheck of the tool's diff and of one question: whether counting those old records as agreeing is right, or
  whether they should keep the result `PARTIAL`. It says that the reviewer has not read TASK_T026.
- **Next, each the owner's own go:** after a PASS, a short task that reruns only the comparison in the scratch tree
  (`D:\DELETE_ME\a_p_r_i_r\T025`, which stays in place); then his install in DEV from v1r3's sheet; then,
  separately, DEV's first fill.
- Next numbers: EX_294 (the reviewer's); entry 207; RAT-45.

## 207. 24 November 2026, 06:10 - EX_294 received: PASS for package STEP2_Research_Engine_v1r3 (the corrected comparison tool); TASK_T027 written (the comparison alone, once more); not started

- **EX_294 (reviewer; main `7d74ee1`; `exchange/EX_294_ChatGPT.md`, SHA-256
  `9f59ae4fd1318e6c36bd639221df442ec9566222b40723975b99ed08ba5c8ce1`), relayed by the owner at 06:08:** "FOCUSED RECHECK
  PASS for v1r3's comparison tool, revised install sheet and one-line manifest revision." It verified the
  three-file diff, that the 35 files of `repo_overlay` are unchanged, and both ZIP hashes. **On the question of
  EX_293 section 3: yes.** An old `INSUFFICIENT_HISTORY` record below the new list's `first_target`, with no new line
  there, is reconciled, not different; such records stay counted apart, as v1r3 does, need not force `PARTIAL`, and
  are not claimed as matching forecasts. **The cause of the 2802 remains an inference** until the corrected tool has
  read the owner's real run folders: "do not relabel the result". It has not read TASK_T026 as a task file.
- **So the package to install is `STEP2_Research_Engine_v1r3`** (`exchange/CLAUDE_WEB_TOOLS/step2/package_v1r3/`, ZIP
  SHA-256 `e80e87ae4d0d9e9baaa15b8f2a405df717f66eb6be7de4126b734ad374bc6926`), with its own sheet.
- **Written, as the reviewer recommends:** `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T027.md` (SHA-256 `a2252015fc88ee8cf9ee98d533425dd2644d9988927be567d207ccc1964bf1cd`), by
  `exchange/CLAUDE_WEB_TOOLS/t027/make_task_t027.py`. 11 steps, about ten minutes, in the scratch folder
  `D:\DELETE_ME\a_p_r_i_r\T025\` as TASK_T026 left it. It checks the scratch tree; copies the corrected tool from the
  repository's `exchange\EX_293_Claude\` into the scratch evidence folder and checks its hash (`b4135af7...241ada6`
  after CRLF is made LF: the tool the reviewer passed); runs it with the scratch tree's own Python; and requires
  the exact lines, with their numbers: 17280 and 8760 read, 14478 and 5958 equal, 2802 and 2802 before the first
  target, `DIFFERENT: 0`, 640 and 640, `RESULT: PASS - COMPLETE` with 34800, 20436 and 5604, exit code 0, 160
  per-variant lines, no `DIFFERENT` line. Any other number is a STOP. The builder asserts that those expected lines
  are the lines the corrected tool printed in the cloud's check. It runs no research job and no launcher.
- **Not authorised by this:** running the task; the install in DEV; DEV's first fill. Each is the owner's own go.
- Next numbers: EX_295; entry 208; RAT-45.

## 208. 24 November 2026, 06:29 - TASK_T027 PASSED: the corrected comparison tool on the owner's real run folders gives PASS - COMPLETE; the cause of TASK_T026's stop is confirmed; the Windows rehearsal of build step 2 is complete

- **The report:** `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T027.md`, main `815bda8`, SHA-256
  `66c0579d26beb3d2bfabec68e29dd0d9ad42df6a12aa7b162f23674d9aae38df`; task file at main `a7cb779`; run 24 November 06:21
  to 06:24; the owner relayed the result at 06:29. The reviewer had not read this task file (the owner ran it on
  his own go, as TASK_T026).
- **What it shows.** The tool copied into the scratch folder has the hash of the tool the reviewer passed
  (`b4135af7ea925caba020bcbc77185999f51837bff0dcedddeb295ff0d241ada6` after CRLF is made LF). Run on the scratch tree's fill
  and on the old run folders copied from DEV, it printed, in 2 minutes 8 seconds, exactly the eight lines the task
  required, every number included: POWERBALL 17280 old records read, 14478 forecasts equal, 2802 `INSUFFICIENT_HISTORY`
  records before the variant's first target, `DIFFERENT: 0`, 640 new lines for other targets; OZLOTTO 8760, 5958,
  2802, 0, 640; part 1 as before (22884 and 11916 old scores, all equal); `RESULT: PASS - COMPLETE - both games; all
  34800 old score records ...; all 20436 old development forecasts ...; the 5604 old INSUFFICIENT_HISTORY records all
  lie before their variants' first targets`; exit code 0; 160 per-variant lines; no `DIFFERENT` line.
- **So entry 205's explanation is no longer an inference:** the 2802 of TASK_T026 were the old system's
  insufficient-history records, 2802 in each game, and nothing else. Every forecast the old development runs kept
  on the owner's PC is in the new lists with the same view digest, scores, ranking, TOP and WORST.
- **One deviation, the runner's own:** it wrote its report in two blocks and not after each step. No command was
  changed.
- **The Windows rehearsal of build step 2 is complete (TASK_T025, T026, T027):** the install sheet's parts 1 to 4 in
  a clone; both launchers; the first fill of both games in 46 minutes with the cloud's counts; a second job with
  nothing to do in 3 minutes; the comparison with the old records, complete. Three things it found: the runner's
  shell has the main `.venv` active, so a tree's `.venv` is built from a plain CMD window; the comparison tool's
  fault (corrected in package v1r3); and that the first fill takes 46 minutes on this PC.
- **What a scratch run computes is a rehearsal, not a result of the project.** DEV has no research results yet.
- **The scratch folder `D:\DELETE_ME\a_p_r_i_r\T025`** is no longer needed by any task. Claude's suggestion: keep it
  until DEV's own first fill has passed the sheet's part 7, then the owner deletes it.
- **Next, each the owner's own go, none given:** the install in DEV from the sheet of package v1r3
  (`exchange/CLAUDE_WEB_TOOLS/step2/package_v1r3/`), parts 1 to 5; separately DEV's first fill (part 6) and part 7;
  then H-1 v10 (entry 183).
- Next numbers: EX_295; entry 209; RAT-45.

## 209. 24 November 2026, 12:37 - The owner began the install of build step 2 in DEV (package v1r3); parts 1 to 3 as far as the suite PASSED; the sheet's comparison command names the wrong folder (Claude's defect)

- **The owner, 12:35, sent his console output** (his own go, by doing it): in DEV at main `2b5087d`, a clean tree, the
  pull up to date, `git diff --stat c7e6ed8 HEAD -- src tests` printing nothing; `PRE PASS`; `35 File(s) copied`;
  `POST PASS`; the suite after the copy: `DONE: 52 modules, 762 tests ran`, the seven research modules `OK`, `FAILED`
  only on `test_mhupa_launchers` (1 failure) and `test_multigame_reader_contracts` (7), the known ones. He made no new
  baseline run, which the sheet allows when `E:\TEMP\TIDY1_evidence\suite_after` exists.
- **Then the sheet's comparison command failed to start:** `can't open file
  'E:\\TEMP\\STEP2_Research_Engine_v1r2\\tools\\compare_suite_reports.py'`. He stopped and sent the output, as the sheet
  says. Nothing of the project ran in that command; the 35 files are copied and not committed.
- **The cause is a defect in the sheet of package v1r3, Claude's:** part 3's comparison command names the folder of
  package v1r2. The command's text comes from `comparison_expected.md`, which held that folder's name written out
  and was not changed when the package's name changed; the builder did not check. One place only (the rest of the
  sheet names v1r3 throughout; checked). The reviewer's EX_294 passed the sheet with it. The tool itself,
  `tools\compare_suite_reports.py`, is byte for byte the same file in both packages.
- **Also in his command:** the word `BASELINE` stood where the sheet asks for the baseline folder to be typed.
- **What Claude told the owner:** the same command with the two things put right, which is the sheet's own command
  for package v1r3: the tool from `E:\TEMP\STEP2_Research_Engine_v1r3\tools\`, the baseline
  `E:\TEMP\TIDY1_evidence\suite_after`. It reads two report folders and writes one text file under `E:\TEMP`. Whether
  to go on with it now is the owner's decision; the departure from the passed sheet is recorded here and the
  reviewer is told.
- **Put right for later packages, not rebuilt now:** `comparison_expected.md` takes the folder from the builder, and
  `build_step2_pkg.py` now refuses a sheet that names any package but its own. Built again with that change, the
  sheet differs from the issued one in that one path only (checked with `diff`). **Package v1r3 as issued and passed
  is not replaced:** its 35 files and its tools are right; only that line of its sheet is wrong.
- Next numbers: EX_295; entry 210; RAT-45.

## 210. 24 November 2026, 13:43 - BUILD STEP 2 IS INSTALLED IN DEV: the owner's commit `5f16b35`, `COMMITTED PASS`, pushed; verified by Claude from GitHub

- **The owner did the sheet's parts 1 to 4 himself** (package `STEP2_Research_Engine_v1r3`), sending his console output
  at 12:35, 13:08, 13:38, 13:40, 13:42 and 13:43. In order: `PRE PASS`; `35 File(s) copied`; `POST PASS`; the suite
  after (52 modules, 762 tests; `FAILED` only on the two known modules); the comparison; `git pull --ff-only`;
  33 files added and 2 modified staged; the commit; **`COMMITTED PASS: the last commit (5f16b35) added exactly 33
  files, modified 2 and deleted 0; all Git blobs match.`**; the push `ba2cfae..5f16b35`.
- **The commit:** `5f16b354b78bc608eefaef440042b159140a2c7d`, "BUILD STEP 2: the research engine in DEV (src/research, the two
  launchers, the manifest, its tests); the old system is not changed"; 35 files, 8253 lines added and 1 removed
  (the same numbers as Claude's rehearsal commits of the same files).
- **Verified by Claude from GitHub at that commit:** the package's verifier, committed phase, gives `COMMITTED PASS`
  and "28 guarded files unchanged"; each of the 35 files of the package's `repo_overlay` equals the committed blob.
- **Three departures from the sheet, all recorded here:**
  1. **The comparison command's folder** (entry 209): the sheet named package v1r2's folder; the owner ran the same
     command from v1r3's folder.
  2. **The baseline.** `E:\TEMP\TIDY1_evidence\suite_after` no longer existed and no baseline had been made before
     the copy. On Claude's recommendation the owner made it from a clean clone of the repository as committed
     (`git clone . "E:\TEMP\STEP2_baseline_clone"`, then the package's `run_suite.py` on it with the main Python):
     `DONE: 45 modules, 571 tests ran`, `FAILED` only on the two known modules. The comparison of that run with DEV's
     run after the copy: `tests in both runs: 571; with the same result: 571`; the three known `FAILS IN BOTH RUNS`
     and no other; `RESULT: DIFFERENCES FOUND` (the new tests); 198 new lines: all as the sheet expects. Before that,
     Claude had found DEV's 52 module lines equal to the rehearsal's run in a clone (TASK_T025), line for line.
  3. **One `git pull --ff-only` before the commit**, to bring in the commit of entry 209 that Claude had pushed while
     the install was under way. Claude should not have pushed then, and pushed nothing more until the owner's
     commit was on GitHub.
- **The owner's question, 13:38, before committing:** "No committing or especially pushing for the moment, I have
  lost trust in the actual state of my local git ... how sure are you that my local git is "good" ?" Claude's
  answer: no Git command had failed (the two failures were a Python "can't open file" and a `dir`); nothing run
  since `POST PASS` writes into the repository; and four read-only checks to make it a fact. He ran them: `git
  status --short` printed the 16 expected lines exactly; `HEAD` was `2b5087d`; GitHub was at `ba2cfae`; the verifier
  printed `POST PASS` again. He then went on.
- **Not yet done:** part 5 (this PC's `ENVIRONMENT.ini`, a copy of the example); part 6, DEV's first fill, which is
  the owner's own separate go; part 7. DEV holds the engine and no research results. Then H-1 v10 (entry 183).
- **Told to the reviewer by paste block:** the sheet's erratum (entry 209) and, with this entry, the install.
- Next numbers: EX_295; entry 211; RAT-45.

## 211. 24 November 2026, 13:56 - The owner's observation on `ENVIRONMENT.example.ini`: the example's comments mislead and its commented paths are out of date; to be rewritten in build step 3

- **The owner, 13:55, at the sheet's part 5 (the settings file open in Notepad):** "This does not look right in a couple
  of ways." (1) `[environment]` holds `role`, `tree_root` and `venv_dir` but no `backup_root`, while `[QA]` and `[PROD]` hold
  no `role` but `tree_root`, `venv_dir` and `backup_root`. (2) "The text says "The sections below are added" ... but that
  cannot be true since if this becomes PROD's ini then the [environment] ... changes ... and role changed to PROD
  presumably but there is no [DEV] section values which are then lost. It look mangled as an example."
- **What the ratified design says (deployment design v0.12 section 1), which the file follows:** each tree has its
  own settings file. `[environment]` is always the tree the file lies in. DEV has no backups, hence no `backup_root`
  there. `[QA]` and `[PROD]` exist in DEV's file only: they are where DEV's tools find the other two trees, and the
  section's name is the role. `[results] copy_from` is the tree whose accepted results this tree copies. A QA or
  PROD tree's file is not made by editing this one: `Init_Tree.bat` writes it once, in that tree's folder, from DEV's
  entry for that role, with that role in `[environment]`. So nothing of DEV is lost: DEV's file stays in DEV.
- **Where the owner is right:** the example's comments do not say any of that, and "the sections below are added
  when the QA and PROD trees are created" reads as if this file turned into another tree's. And its commented
  example paths are out of date: `D:\TEST_BED` for QA, where the owner decided `T:\a_p_r_i_r` with backups under
  `T:\a_p_r_i_r_backups\QA` and `\PROD` (entry 181). Claude's wording, in a reviewed and installed file.
- **For today:** DEV's file needs the `[environment]` section only, and the example's three lines are right for this
  PC. The lines that begin with `;` are comments and are not read. Nothing to change in part 5.
- **For build step 3 (when `Init_Tree.bat` and the `[QA]` and `[PROD]` sections become real):** the example is rewritten
  through that step's reviewed package: its head says what each section is and whose file it is, shows a QA tree's
  file beside DEV's, and carries the owner's real places. `Check_Tree.bat` prints how a file is read.
- Next numbers: EX_295; entry 212; RAT-45.

## 212. 24 November 2026, 15:02 - BUILD STEP 2 IS COMPLETE IN DEV: the settings file made, DEV's first fill run by the owner, the comparison with the old records PASS - COMPLETE

- **Part 5 (the owner, 13:59):** after `git pull --ff-only` (to main `ef1f0e2`), `copy ENVIRONMENT.example.ini
  ENVIRONMENT.ini`, the file looked at in Notepad and left as it is, `git status --short` printing nothing. His
  observation on the example's wording is entry 211.
- **Part 6, DEV's first fill, on the owner's own go** ("let me proceed with stuff under the notepad command"; he ran it
  himself and sent the output at 15:01). `Run_Research.bat --game BOTH --no-update`, 14:01 to 14:48 (47 minutes), in
  the DEV tree: `POWERBALL: finished. Results on file through draw 1591; written: 15118 forecasts, 15078 scores, 0
  prevailing lines, 0 eligibility draws, 900 report files`; `OZLOTTO: finished. Results on file through draw 1708;
  written: 6598 forecasts, 6558 scores, 0 prevailing lines, 0 eligibility draws, 474 report files`; each
  `prevailing OV-1: not started; waiting for a successful results step`; no `WARNING`, `REFUSED` or `STOPPED`; last line
  `The job finished.` **The same counts as the cloud's fill and as the rehearsal's, and the same progress lines.**
- **The same job once more,** 14:50 to 14:53 (3 minutes): for each game `written: 0 forecasts, 0 scores, 0 prevailing
  lines, 0 eligibility draws, 0 report files`; `The job finished.`; then `git status --short` printing nothing
  (everything the job wrote is ignored by Git).
- **Part 7, the comparison with the old development records, with the corrected tool of package v1r3:** the seven
  lines the sheet expects. POWERBALL: 22884 old scores, all equal; 17280 old records read from the run folders,
  14478 forecasts equal, 2802 `INSUFFICIENT_HISTORY` records before the variant's first target, `DIFFERENT: 0`, 640
  new lines for other targets; 11442 forecasts named by the tracked rank ledgers, none missing. OZLOTTO: 11916;
  8760, 5958, 2802, `DIFFERENT: 0`, 640; 5958, none missing. **`RESULT: PASS - COMPLETE - both games; all 34800 old
  score records equal the new score lists; all 20436 old development forecasts ... the same view digest, scores,
  ranking, TOP and WORST; the 5604 old INSUFFICIENT_HISTORY records all lie before their variants' first targets`.**
  160 per-variant lines. Every number equals the rehearsal's (entry 208).
- **So build step 2 is complete:** reviewed (EX_283, EX_285, EX_290, EX_294), rehearsed on Windows (TASK_T025, T026,
  T027), installed in DEV (commit `5f16b35`, entry 210) and run. DEV now holds its own research results under
  `results\research\` (ignored by Git): the lists of forty variants for each game, the scores and the reports
  (start with `results\research\POWERBALL\reports\README.txt`). **What they are:** DEV's development results, from the
  reviewed programs run by the owner. The prevailing OV-1 has not started in DEV and cannot until a tree exists to
  copy results from (build step 3). Nothing here is a claim about the lottery: the comparison shows that the new
  engine computes what the old one computed.
- **The scratch folder `D:\DELETE_ME\a_p_r_i_r\T025` and `E:\TEMP\STEP2_baseline_clone`** are no longer needed; the owner
  may delete both.
- **Next:** H-1 v10 (the owner, entry 183: "ok to a full H-1 v10 once step 2 is installed"), then build step 3.
- Next numbers: EX_295; entry 213; RAT-45.

## 213. 24 November 2026, 15:22 - the H-1 v10 CANDIDATE written, on the owner's word; not reviewed, not ratified

- **The owner, 15:16:** "ok please do H-1 v10 now." (His standing word was entry 183: "ok to a full H-1 v10 once step 2
  is installed".)
- **Written:** `exchange/CLAUDE_WEB_TOOLS/h1v10/out/Claude_Primary_Handover_H1_v10.md` (1308 lines; SHA-256 `41a1ab749556c94e20b7ee28705b664b52183b995a140c1ebe7aec1b1164f8db`)
  and its blurb `Claude_Primary_Handover_H1_v10_introductory_blurb.md` (SHA-256 `6c0ab5cf4133628edcfbe602e2aa7b362b13c2f9f331054bba9cf4fd4761cfb9`), built from the installed
  H-1 v9's and its blurb's Git bytes (both asserted by hash) by `exchange/CLAUDE_WEB_TOOLS/h1v10/make_h1_v10.py` with the
  words of `h1_v10_texts.py`: 15 short replacements, 2 insertions and 9 whole sections replaced, each old text or
  marker found exactly once in v9; Appendix A rebuilt with every hash computed from Git at `HEAD` (v9's rows, H-1 v9
  in place of H-1 v8, and 29 new rows). **Sections 1, 2 and 2A are carried byte for byte** (asserted). The exact
  difference is `H1_v9_TO_v10.diff` (SHA-256 `3b2f331e2bc676dcfb32abb18140aa50e098d0c89f3d56256eb2baf42f16f10f`); applied to v9 with `patch` it gives the candidate (checked).
- **What it brings up to date:** build step 2 reviewed, rehearsed, installed and run (sections 0B, 7 and 10); the
  runner's rulebook v0.7, the owner's settings change and the three tasks (8.6, 12.4); the owner's decisions for
  build step 3 (entries 180, 181); ten lessons from build step 2 (8.8); the tools, the practice and the owner's
  machine (12.2, 12.3, 12.6); the open items (12.8). Its Appendix B lists every section's change.
- **Its own limit, stated in it:** written by the chat that did the work, late in a long conversation; the
  reviewer's cold read against the repository is the check on it.
- **State:** a CANDIDATE with no force. H-1 v9 (RAT-43) stays the installed Claude handover. The reviewer's reply is
  expected as EX_295; then the owner's ratification (RAT-45) and the install in `doc/HANDOVER/` by a script.
- Next numbers: EX_295 (the reviewer's reply on H-1 v10); entry 214; RAT-45.

## 214. 24 November 2026, 15:32 - EX_295 received (the H-1 v10 candidate: RECHECK, three corrections of wording); all three made; the corrected candidate committed

- **EX_295 (reviewer; main `c98bec9`; SHA-256 `983f748344d41f07207f8fdc14b185264622b2817015bf6e9810947d58a6e641`), relayed by
  the owner at 15:30:** it verified both hashes, rebuilt v10 from the installed v9 with the diff, and confirmed that
  sections 1, 2 and 2A are unchanged; "No binding scientific, safety, role, review-rights or owner-approval rule was
  found missing." Three corrections. **H1V10-C01:** passages carried from v9 call all 26,040 old development records
  "forecasts" and say 5,838 and 2,802 "forecasts were never scored", which contradicts the new text. **H1V10-C02:**
  section 4.4 says "In force" of both H-2 v4 and H-2 v5r1, and Appendix A lacks H-2 v5r1 and its blurb. **H1V10-C03:**
  section 0C item 1 points to "0B item 8" for the reviewer chat, which in v10 is build step 2.
- **All three made, and nothing else** (the owner's relay: "Please make only these corrections"):
  1. **C01.** "Target record" where all the old records are meant: section 0B item 6, section 6 (one phrase), and
     section 7.2's two carried items; the never-scored statement put right; and Claude's own last item of 7.2
     rewritten as the exact count. Powerball: 17,280 target records = 14,478 forecasts + 2,802
     `INSUFFICIENT_HISTORY` records; 11,442 forecasts scored, so 3,036 forecasts never scored and 5,838 records with no
     score. Oz Lotto: 8,760 = 5,958 forecasts, all scored, + 2,802. In all 26,040 = 20,436 + 5,604. It also says what
     build step 2's comparison did and did not compare for the 5,604.
  2. **C02.** Section 4.4: H-2 v4 is "previously in force (RAT-41), now history"; H-2 v5r1 is "the one installed
     reviewer handover now". Appendix A gains H-2 v5r1 and its blurb, with hashes computed by the builder; they equal
     the two values the reviewer computed (`234e5917...714edc8`, `f195212e...6f20aa`). No reviewer file was touched.
  3. **C03.** Section 0C item 1: the chat of 21 November is history; the present reviewer chat took over from H-2
     v5r1 on 23 November 2026 (entry 175; 0B item 13). The carried section 1.1 is not changed.
  With them: the status line says the candidate is corrected; section 0A item 3's newest numbers; Appendix B's rows
  for the sections touched; `exchange/EX_295_ChatGPT.md` added to Appendix A.
- **The corrected candidate:** `exchange/CLAUDE_WEB_TOOLS/h1v10/out/Claude_Primary_Handover_H1_v10.md` (1322 lines; SHA-256
  `a769316d0f886595966a73e1d047173036dd4523a362921cdf18bfd15b07960b`). The blurb is unchanged (`6c0ab5cf4133628edcfbe602e2aa7b362b13c2f9f331054bba9cf4fd4761cfb9`). `H1_v10_EX295_CORRECTION.diff` (SHA-256 `4ca460064f853941617cf9b3ca00fa56a2162fa1c10e57ce30dc3b1286108028`; 15 hunks) is the
  exact difference from the candidate the reviewer read (`41a1ab74...1164f8db`, main `5ce22e8`); `H1_v9_TO_v10.diff` (SHA-256
  `43486967d9174bc6fabac5517cce8b27bd28bed7f86d54b5d462eaad4cccc8cf`) is rebuilt. Both, applied with `patch`, give the corrected candidate (checked). Built by the same builder:
  22 short replacements, 2 insertions, 9 sections replaced; sections 1, 2 and 2A carried byte for byte (asserted).
- **State:** a CANDIDATE with no force, waiting for the reviewer's focused recheck; then the owner's ratification
  (RAT-45). H-1 v9 stays installed.
- Next numbers: EX_296 (the reviewer's recheck); entry 215; RAT-45.

## 215. 24 November 2026, 15:42 - RAT-45: THE OWNER RATIFIES H-1 v10 after the reviewer's focused PASS (EX_296); installed in doc/HANDOVER/ with its status statements changed

- **EX_296 (reviewer; main `aabe46f`; SHA-256 `e5412f53e81ca05486fa44901e169574a4fc60521b1fd24b316aacbcd9db1361`):** the
  focused recheck of the corrected candidate at `6e13bbe`: PASS; the three findings of EX_295 CLOSED; the 15 hunks of
  the correction rebuild the corrected candidate exactly; the hashes match; sections 1, 2 and 2A unchanged.
- **The owner's ratification.** EX_296 records his words to the reviewer: "If this is any good then I ratify it now".
  The reviewer passed it, and the owner relayed that to Claude at 15:40 with the request to record RAT-45 and
  install the handover, adding in his own words: "I am getting really excited now, a live prod coming soon !".
  **Claude took the relay as his ratification:** it is his own message, it carries his own words of ratification,
  and it asks for the install. Had he meant otherwise, the install is a document only and Git keeps H-1 v9.
- **RAT-45 is recorded** (RAT-44 was the last number used). **Installed:**
  `doc/HANDOVER/Claude_Primary_Handover_H1_v10.md`, **SHA-256 `824e7f251d0ae43a8c045c42495537fa6a8a242c531eb677132882ccb467a69b`** (1332 lines), and its blurb
  `doc/HANDOVER/Claude_Primary_Handover_H1_v10_introductory_blurb.md`, SHA-256 `6c0ab5cf4133628edcfbe602e2aa7b362b13c2f9f331054bba9cf4fd4761cfb9` (the candidate's blurb, bytes
  unchanged). Written by `exchange/CLAUDE_WEB_TOOLS/rat45/finalise_rat45.py` from the candidate the reviewer passed
  (`a769316d...5b07960b`, asserted by hash).
- **Five passages differ from the passed candidate,** each a statement the ratification itself made out of date
  (`H1_v10_CANDIDATE_TO_FINAL.diff`, SHA-256 `7a79e5f31143d1d76b89aa75b001e8dd16c4898d055dd3366d149fdb7879233b`; 5 hunks; applied to the candidate with `patch` it gives the
  installed file, checked): the status paragraph; section 0A item 3's newest numbers; section 10 item 2 (this
  edition is ratified; the reviewer's H-2 v6 is a candidate); section 12.8's "waiting on" lines; section 12.8
  item 9. Sections 1, 2 and 2A are carried byte for byte (asserted). No rule or fact was changed.
- **H-1 v9 and its blurb stay in `doc/HANDOVER/` as history.** A new Claude chat starts from the v10 blurb.
- **The reviewer's H-2 v6** (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_CANDIDATE_20261124.md` and its blurb, with
  exact diffs under `exchange/ChatGPT_REVIEWER_H2V6/`; main `154d30b` to `f53a223`) is the reviewer's own CANDIDATE.
  **Not ratified, not installed; H-2 v5r1 (RAT-43) stays the installed reviewer handover.** Claude has not changed
  those files. The owner asked whether to ratify it; Claude's answer is in the chat (yes, as the reviewer's own
  act, once it has brought its statements about H-1 v10 up to date).
- **RAT-45 authorises the documentary installation and nothing else:** not build step 3, a runner task, or anything
  on the owner's PC.
- Next numbers: EX_297; entry 216; RAT-46.

## 216. 24 November 2026, 15:52 - OWNER: RAT-45 confirmed in his own words; RAT-46: THE OWNER RATIFIES the reviewer's handover H-2 v6, installed by the reviewer

- **The owner, 15:52, to Claude:** "i ratify rat45 and rat46." That confirms entry 215 (H-1 v10, which Claude had
  installed on his relay) in his own words, and ratifies the reviewer's handover.
- **RAT-46.** EX_297 (reviewer; main `e431192`; SHA-256 `fe1139ad4ace1a9d656888ea4b02a721ddbc0760033b2aaa0820c1571802fbd1`) records his words to the reviewer on the corrected
  candidate H-2 v6r1 and its blurb: "I ratify it". **RAT-46 is recorded** (RAT-45 was the last number used).
- **The reviewer made the documentary installation itself,** of its own files (commits `8d7bb1e` to `2938f52`):
  `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124.md`, SHA-256 `588c52b9c08781956330676a3c13bda99b0c8fd90211139f74c26503adf174a1`, and its blurb
  `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124_introductory_blurb.md`, SHA-256 `58c8f5b2b13dabc63f3739c04a42dd6bb30784fcf9c40b504e65da72c8c8efe3`. Claude computed both
  hashes from the repository at `e431192`; they equal the values in EX_297. The candidate-to-final diffs are the
  reviewer's, under `exchange/ChatGPT_REVIEWER_H2V6/`. Claude changed none of the reviewer's files.
- **In force now:** for a Claude chat, H-1 v10 (RAT-45); for the reviewer, **H-2 v6 (RAT-46)**. H-1 v9, H-2 v5r1 and
  the H-2 v6 candidates stay in `doc/HANDOVER/` as history.
- **Overtaken by this entry, in a ratified file that is not edited:** H-1 v10 says, in its section 4.4, section 10
  item 2 and section 12.8, that H-2 v5r1 is the installed reviewer handover and that H-2 v6 is a candidate awaiting
  the owner's decision. That was true when H-1 v10 was installed, half an hour earlier. The decision log and the
  continuity page prevail (H-1 v10's own "Authority" line).
- **Not authorised by either ratification:** build step 3, a runner task, or anything on the owner's PC. No new chat
  has been started.
- Next numbers: EX_298; entry 217; RAT-47.

## 217. 24 November 2026, 15:53 - OWNER: THE GO FOR BUILD STEP 3 (trees, installs, backups and restore; then the transition check and PROD's first job)

- **The owner, 15:53,** after Claude's "Suggest switching to Fable (High) for this" and its statement that it would
  hold until he said go and would begin with a short build plan before any code: "Build step 3, go now please."
- **What the go covers:** designing within the ratified documents, coding in the cloud workspace, testing there, and
  preparing the reviewed packages of build step 3 (specification 12.1 to 12.6, 13 and 14.1; deployment design
  v0.12). **What it does not cover:** any install, run, tree creation, backup, restore or runner task on his PC.
  Each of those is his own separate go, as before.
- **First deliverable:** the build plan, for the owner and the reviewer, before any code.
- Next numbers: EX_298; entry 218; RAT-47.

## 218. 24 November 2026, 15:56 - build step 3: the build plan written (v0.1); four decisions put to the owner; no code yet

- **Written:** `exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1.md` (SHA-256 `d91def21015da725c786aadf88fb54463f293bde8ccdec53b2a90086c74105d2`), from the specification
  (12.1 to 12.6, 13, 14.1, 17.3, 17.4) and the deployment design v0.12 (sections 1 to 12 and 15), read again for it.
  A working plan, not a design and not a rule.
- **What it says.** Step 3 delivers `Make_Installable`, `Check_Tree`, `Init_Tree`, `Install`, `Reinstall_Infra`,
  `Verify_Tree`, the launch guard, backups, the recovery kit and `Restore`, the clean-sheet updater, the results step
  in each role, the transition check and PROD's first job. **Recommended: four code slices, each reviewed by
  itself** (A foundations; B backups, the kit and restore; C trees and installs; D the updater), then E, the
  transition; each rehearsed by the runner in scratch trees; **one install into DEV at the end.** It lists the
  owner's decisions already given (entries 180, 181, 211), how the updater's clean sheet is proved, and what is not
  known until it runs on Windows.
- **Put to the owner:** (1) four slices and one install at the end, or an install per slice; (2) a short probe task
  first (what the standard library reads of Windows' processes; a rename over an open file; the time and size of a
  backup with its `.venv`); (3) QA before PROD, as the specification recommends; (4) whether the plan goes to the
  reviewer before slice A is coded.
- No code is written. Nothing is authorised on the owner's PC.
- Next numbers: EX_298; entry 219; RAT-47.

## 219. 24 November 2026, 16:03 - OWNER: the four decisions of the build plan (one install at the end; the probe first; QA before PROD; the plan to the reviewer)

- **The owner, 16:03, to Claude,** on the four questions of the build plan v0.1 section 7 (entry 218): "1 One install
  into DEV at the end, or one per slice? answer: one at the end. 2 yes to your recommendation.  3 yes to your
  recommendation 4 yes to your recommendation. blurb sent to  chatgpt."
- **So decided:** (1) four reviewed slices, and **one install into DEV at the end**; (2) **a short probe task
  first** (TASK_T028); (3) **QA before PROD**: `Init_Tree QA` and the transition check there before PROD is created;
  (4) the plan goes to the reviewer before slice A is coded (he sent the paste; the reviewer answered with EX_299
  and EX_300, entry 221).
- **Not decided by this:** any run on his PC. The probe's run, every install, every tree and PROD's first job are
  each his own go, as before.
- **A number moved.** The reviewer has since used EX_298, EX_299 and EX_300. Claude's next number is EX_301.
- Next numbers: EX_301; entry 220; RAT-47.

## 220. 24 November 2026, 16:23 - OWNER (through the reviewer, EX_298): what the short operations manual is to be; clarifies entries 171 and 182; deferred work, no gate

- **The owner, 16:10, to Claude:** "after you have finished doing what you are doing now and about await the next
  post from me, please consider [EX_298 - Operations manual requirements and clarifications] ... Only then please
  consider [EX_299 - Build-step-3 plan review] ..." and, at 16:19: "ex299 is supplemented by ex300."
- **EX_298** (reviewer; main `61c5662`; SHA-256 `72a23e0dbf025e96abb9ad44042723762a3399a34718deb6c7f3811ef408b4c0`) records the owner's clarification to the
  reviewer of his idea of 23 November (entry 171; two items added in entry 182). In summary, faithfully:
  - **The topics he named are examples of the least it should cover, as they apply,** not a closed list of chapters
    and not a list of commands he insists on: migration, ordinary PROD use and catch-up, backup and restore, the
    DEV, QA and PROD installations, decommissioning, methods, contracts and runners, a short architecture appendix.
    The real contents and command names come from the finished, installed system; some of his earlier examples of
    directions may not be permitted operations.
  - **Reports are a necessary topic:** where each report is and how to read and interpret it, rankings and OV-1
    included, and where it applies the other reports and what says whether results are current.
  - **A short command cheat sheet in an appendix is to be considered:** exact command names, one or two lines each,
    and a pointer to the full procedure. He notes that a second summary means maintaining two things when a command
    changes. The reviewer recommends it as an index only (no copied procedure or options), amended whenever a
    procedure is, and no generator or other mechanism built for it; a stale cheat sheet is worse than none.
  - **The manual is short, for a human, a practical how-to:** a table of contents, sections, the operator's actual
    actions, what he should see, and the warnings that matter. Not a second specification.
  - **Claude and the reviewer propose its structure and contents together, for the owner's approval,** at the right
    time: its first version after build step 3 is finished and proved, when the commands exist; the laboratory
    procedures of step 4 added when they exist. Nothing is written now.
- EX_298's section 2 gives nine headings as a starting point for that later discussion only; it is not a table of
  contents and approves nothing.
- **Claude agrees,** and adds one thing it will bring to that discussion: the reports' own `README.txt` files (one
  per game, written by the research job) already say where each report is; the manual should point to them and
  explain how to read the reports, so that the places are stated once.
- **No decision on contents, no code, and no gate on build step 3.** The work item stays in the continuity page.
- Next numbers: EX_301; entry 221; RAT-47.

## 221. 24 November 2026, 16:23 - the reviewer's check of the build plan (EX_299, narrowed by EX_300): four corrections accepted and made (plan v0.1r1); TASK_T028 written, not run; one question open for the owner

- **EX_299** (reviewer; main `4264b59`; SHA-256 `a125e79a990d095fa569b4ba15c28ca7531ec346ad9ef8734e9c4059cc790879`): the four slices and the one install at the end are
  supported; four focused corrections of the plan. **EX_300** (main `ac85564`; SHA-256 `7aad9e853c92848e593054f632069acbcb06c32411560bfff68b7e6977771539`) narrows the second after the
  owner asked the reviewer whether the process tools really must be standard library only ("do they really ? I
  can pop those things into my per-user python dependencies and so if it is too hard consider my approach
  instead.", as EX_300 quotes him).
- **Claude accepts all four; each was a fault of the plan v0.1:**
  - **S3P-C01 (the updater's proof).** v0.1 promised byte-identical ledgers between `v0_2` and `v0_3` and a
    syntax-tree comparison. A ledger row holds the tool's version and its own SHA-256 and times, which must differ,
    and a clean-sheet rewrite cannot be equal by syntax tree. Corrected: the master equal byte for byte; the ledger
    and verification records compared field by field with a written list of the only provenance fields allowed to
    differ; old `v0_2` rows left as they are under new `v0_3` rows; no Mode H record read, written or asked for; a
    check-by-check table with normal, edge and planted-fault cases.
  - **S3P-C02 (the process check).** `src\package_tools\process_check.py` reads through psutil and holds the old
    system's lock clearances; it cannot be the new system's check as a file. Kept: its rule and its refusals.
  - **S3P-C03 (the transition).** v0.1's sequence left out QA's first fill: `Init_Tree QA` copies no forecast, so
    the transition check would have had nothing to compare. Corrected: QA's `.venv`; `Init_Tree QA` again;
    `Run_Research.bat --game BOTH --no-update` in QA; then the check, read-only, with the 5,604 old
    `INSUFFICIENT_HISTORY` records counted apart from the 20,436 forecasts.
  - **S3P-C04 (the slices joined).** A new section says what is shown, on the exact joined files in scratch trees,
    before the one install into DEV is put to the owner.
- **Written:** `exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md` (SHA-256 `6eb18f0e38279a9b68e88dec304dbea205a64b62bc8e80bfc8dc9723c39b3195`), made from v0.1 by
  `make_plan_v0_1r1.py` (each change one replacement that must match exactly once), with the exact difference
  `STEP3_BUILD_PLAN_v0_1_TO_v0_1r1.diff`. v0.1 is unchanged. The owner's decisions of entry 219 are in its section 7.
- **One question is open for the owner (plan section 4A and section 7 item 5): how Windows' processes are read.**
  Two different questions are asked of the process table. The restore asks whether any Python program at all is
  running: program names, parents and start times, which the standard library reads directly. Every other rule asks
  whether another Python process of this tree is running, which needs another process's working folder and command
  line: psutil reads those; the standard library does not, short of hand-written reading of another process's
  memory. **Claude recommends:** the restore stays standard library only, as ratified (the kit, the backup and any
  installed Python); every other check uses psutil, which every tree's environment and DEV's already hold; and
  one narrow amendment of the deployment design section 2 ("standard library only" for the install tools, against
  the same design's section 9, which gives them the rule that needs psutil), for ratification. The alternatives:
  psutil for the restore too (one reader; a restore then needs a Python with psutil, checked before anything is
  touched); or the standard library for everything (advised against). **Not decided.** Best answered after the
  probe's report; needed before slice A's guard goes to the reviewer.
- **TASK_T028 is written, and has not run.** `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028.md` (SHA-256 `b2c3ce9477aa93f383775639304cbd2653ceff76f7d85c74142d223b7ff63778`, CRLF) and
  its probe `inbox/TASK_T028_probe.py` (SHA-256 `1f58ac1dc7685e7d5c2ad443f7d0d7f30e770db3950ccb58e0e89e1f5c7f3211`, LF; standard library, psutil only for the comparison);
  builder and template in `exchange/CLAUDE_WEB_TOOLS/t028/`. Rulebook v0.7 section 2A, in a new folder
  `D:\DELETE_ME\a_p_r_i_r\T028`. Three parts: how Windows answers a rename, a replacement and a removal when a file
  is open or another program sits in the folder; the size and time of a backup ZIP (Deflate level 9, each file
  hashed, read back, the source read twice; level 6 beside it for comparison) of the scratch tree of TASK_T025 if
  it is still there, otherwise of the main `.venv` alone; and what psutil and the standard library each read of the
  PC's Python processes. It runs no program of the project, ends no process (its helper program ends by itself),
  reads nothing under the main repository's data folders and prints no path under a user's folder.
- **Tried in the cloud:** all three parts on Linux with a made-up tree of the real size (8,086 files, 337 MB: level
  9 in 30 seconds to 101 MB; level 6 in 12 seconds to 102 MB; those times say nothing of the owner's drives). The
  part that calls Windows itself cannot be run in the cloud; it was exercised through a stand-in for the Windows
  calls, and read line by line. A fault in it would stop the task's last step, after the other two parts are
  recorded.
- **Before it runs:** the reviewer asked to read a probe task first (EX_299 section 2 item 2), and its run is the
  owner's own go. **No code of build step 3 is written yet.** Nothing is authorised on the owner's PC.
- Next numbers: EX_301; entry 222; RAT-47.

## 222. 24 November 2026, 16:40 - OWNER: the process readers decided (option A; B at Claude's discretion if A proves too hard); the scratch tree of TASK_T025 is deleted; slice A begun (the settings of the three trees)

- **The owner, 16:34, to Claude:** "D:\DELETE_ME\a_p_r_i_r\T025 is deleted.  ok to A (recommended) and if that proves
  to be too hard then consider adopting B at your discretion. blurb given to chatgpt."
- **DECIDED (owner), the question of entry 221 and plan v0.1r1 section 4A: option A.** The restore stays standard
  library only, with its own small reader of Windows' process table; every other process check uses psutil. **If A
  proves too hard, Claude may adopt B** (psutil for the restore too; a restore then needs a Python that has psutil,
  checked before anything is touched). Claude will say so, with the reason, before it does.
- **Still to come, either way:** the narrow amendment of the deployment design (section 2's "standard library only"
  for the install tools; under B also sections 11 and 12) is put to the reviewer with slice A and then to the owner
  for ratification. His words above decide the direction; they are not that ratification.
- **The scratch tree of TASK_T025 is gone,** so TASK_T028's step 6 will measure the main `.venv` folder alone, read
  only. The task file already provides for that and is not changed (it is with the reviewer). In the cloud's
  made-up tree of the real size the `.venv` was 257 of 337 MB and 5,912 of 8,086 files, about three quarters of a
  tree; the rest is scaled from the cloud's figures, and a whole tree is measured later, at the rehearsal.
- **Slice A begun, in the cloud** (`exchange/CLAUDE_WEB_TOOLS/step3/overlay/`; working files, not a package, not
  reviewed, nothing installed): `src/research/settings.py` now also reads DEV's file as DEV's tools need it (its
  `[QA]` and `[PROD]` entries) and makes the deployment design's section 1 checks across the three trees: three
  separate tree roots; backup roots outside every tree and different for QA and PROD; each environment inside its
  own tree; a tree is what its own file says, with both values printed when DEV's entry and the tree's file
  disagree; the same-volume warning. `ENVIRONMENT.example.ini` is rewritten as entry 211 asked: whose file it is,
  what each section is, that `Init_Tree.bat` writes QA's and PROD's files, a QA file shown for comparison, and the
  owner's real places. **Tested:** `tests/test_trees_settings.py`, 32 tests, each named for its rule; 12 of 12
  faults planted in the reader were caught; the engine's 25 identity tests and 48 job tests still pass.
- **Not yet in slice A:** the LF pin, the readiness markers and `Make_Installable`, the import check and the
  manifest's `[install_tool]` list, `INSTALLED_FILES.json`, the environment's digest over the fixed inventory,
  `Check_Tree`, and the launch guard.
- Nothing is authorised on the owner's PC. TASK_T028 has not run.
- Next numbers: EX_301; entry 223; RAT-47.

## 223. 24 November 2026, 16:44 - EX_301 (reviewer): the plan v0.1r1 FOCUSED PASS; TASK_T028 cold read RECHECK, three findings, all corrected (TASK_T028 r1); not run

- **EX_301** (reviewer; main `89728ff`; SHA-256 `191a06637d5a642f991c82e445855a7c36b6f19e4c3c6e51d63d02492dd82518`), read after entry 222 was written.
  **So Claude's next number is EX_302,** not EX_301 as entries 219 to 222 say.
  - **The build plan v0.1r1: FOCUSED PASS.** It closes EX_299's C01, C03 and C04; C02 is rightly an owner's choice.
    A working plan, not a design and no authority on the owner's PC.
  - **Plan section 4A: the reviewer recommends the split Claude proposed** (the restore standard library only;
    psutil for the other checks; one narrow amendment of the deployment design section 2, to be ratified; the probe
    to inform its wording). The owner had chosen it meanwhile (entry 222). The amendment is not yet ratified, and
    nothing here says it is.
  - **TASK_T028: RECHECK, not cleared to run.** Three findings, all accepted as found.
- **T028-F01 (corrected).** Step 3 checked `D:\DELETE_ME` but not the folder between it and the task's folder, which
  could have been a link leading elsewhere. Now every existing folder above the task's folder must be an ordinary
  folder (no link, junction or other reparse point), the task's folder must resolve to where its name says, and
  step 4 checks the folder it has just made the same way before it copies anything.
- **T028-F02 (corrected).** The task said "run as a background command and wait" over a line that holds neither.
  Now it says exactly what the line is (an ordinary line that records its own output and, last, the probe's own
  exit status), that it is started with the runner's shell tool's run-in-background option (the way the long steps
  of TASK_T025 to T027 ran on this PC; a shell `&` with `wait` cannot span the runner's separate shell calls), and
  that the end of step 6 is proved by the file: step 7 first reads the file's last line, which may be repeated
  while it is not yet `ZIP EXIT CODE <n>`, with a STOP after 30 minutes.
- **T028-F03 (corrected, in the probe).** The part "processes" could finish as made with psutil absent. Now psutil
  absent, or either reading not showing the probe and its own helper program, is a measurement NOT MADE: exit code
  1, a STOP. Other programs starting or ending between the readings, and unreadable details of other processes,
  stay findings.
- **The ZIP measurement is named for what it now is** (EX_301 section 2; the scratch tree of TASK_T025 is deleted):
  **an environment-only proxy,** the main `.venv` alone, read only; not a whole tree, not `source_data` or
  `results`, not a backup. The command no longer names the deleted tree. A whole tree is measured in the joined
  rehearsal.
- **Written:** `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028.md` r1 (SHA-256 `96e2a6cf86873a9f6a1df1f9e9d3ec2c884e3a8f19b767395498b7ab7f88b02c`, CRLF) and
  `inbox/TASK_T028_probe.py` r1 (SHA-256 `57fde59dc4f56526c1a73e95e006fee63b80bbffa223206740ee64776c6128bf`, LF), in place, as TASK_T025 r1 was (entry 200): neither had
  run. The exact differences: `exchange/CLAUDE_WEB_TOOLS/t028/TASK_T028_TO_r1.diff` and `TASK_T028_probe_TO_r1.diff`.
- **Tried in the cloud:** steps 3 and 4 as written, on made-up folders: pass with and without the middle folder;
  STOP when the middle folder is a link, when the task's folder is there already, and when the probe's bytes
  differ. The probe's new refusals, each with a planted case: psutil cannot be imported; psutil's reading lacks the
  helper; the standard-library reading lacks the probe; an empty standard-library table. The part that calls
  Windows itself still cannot be run in the cloud.
- **A fault of Claude's in the record, stated:** commit `d103011` (pushed) carries TASK_T028 r1, the two
  differences, entry 222 and the slice A working files, and its message names "entries 222 and 223", but this
  entry was not in it: the script that was to write it stopped (it read this log as ASCII, and an earlier entry
  holds a character that is not), and the commit command ran all the same. This entry and the continuity page's
  line follow in the next commit. Nothing else was affected; the files of `d103011` are as described here.
- **Waiting on:** the reviewer's short cold recheck of r1, then the owner's go for this task. Nothing has run.
- Next numbers: EX_302; entry 224; RAT-47.

## 224. 24 November 2026, 16:54 - EX_302 (reviewer): TASK_T028 r1 cold recheck PASS; the owner's go for the task is still his own

- **The owner, 16:53, to Claude:** "ex302 is in".
- **EX_302** (reviewer; main `d73c875`; SHA-256 `f519706227c64b68af1a1e2912190cabab5ecaba0d79cde38a21e6d452caa91a`): **PASS, as a cold review only,** of TASK_T028 r1 and
  its probe at main `25d63dd`, with the hashes of entry 223 computed again by the reviewer and both files rebuilt
  byte for byte from the originals and the two committed differences. T028-F01, F02 and F03 are each closed; the
  ZIP measurement is rightly named an environment-only proxy.
- **What the PASS is not:** it does not say that any Windows call, ZIP timing or rename has run or succeeded, and
  it is not the owner's go. The deployment-design amendment for the process readers (entry 222) is not ratified
  and comes with slice A.
- **The reviewer has used EX_302.** Claude's next number is EX_303.
- **Waiting on:** the owner's own go to run TASK_T028 r1 (a quarter of an hour; `git pull --ff-only`, a new Claude
  Code conversation, `Do inbox\TASK_T028.md`). Nothing has run.
- Next numbers: EX_303; entry 225; RAT-47.

## 225. 24 November 2026, 17:04 - slice A continued in the cloud: readiness (the two markers, the static import check, Make_Installable); the owner's line-ending figures for DEV

- **The owner, 16:55, to Claude** (three read-only commands he ran in the project folder, at Claude's request):
  `git config core.autocrlf` gave `true`; of the files Git tracks under `src` and `deploy`, **3 have CRLF line
  endings on his disk and 584 have LF.**
- **What that means for the LF pin (not yet designed in full):** almost all of DEV's code already lies on his disk
  as LF, as the packages delivered it. With `core.autocrlf=true` and no pin, any Git operation that rewrites a file
  would give it CRLF, change its hash, and with it a marker or the identity of the forecasting code. The pin stops
  that. **Which three files are CRLF matters:** if one is a file the forecasting code's identity or a variant's
  fingerprint is computed from, making it LF changes that identity in DEV. Claude has asked the owner for their
  names.
- **Written in the cloud** (working files in `exchange/CLAUDE_WEB_TOOLS/step3/overlay/`; not a package, not reviewed,
  nothing installed):
  - `deploy/install_import_check.py`: the static import check of specification 3.4. It reads import statements and
    runs nothing; relative imports are resolved; any use of `importlib`, `__import__`, `exec`, `eval` or `sys.path`
    in a variant's file or a helper is a fault; an import of a project file that is on none of the variant's lists
    and not infrastructure is a fault; and for the infrastructure, a project file it imports that is not on the
    manifest is a fault ("an imported module not listed").
  - `deploy/install_readiness.py`: the two markers. A variant's `I_AM_INSTALLABLE.json` (its fingerprint and the
    hashed list it was computed from) and `deploy/INFRA_IS_INSTALLABLE.json` (the manifest, every `[files]` file
    with its class, every `[install_tool]` file, one fingerprint). The same files always give the same bytes; a
    marker never lists itself; a marker made by hand counts only if it holds exactly what the tool would write; a
    marker is written whole in `records/marker_staging/` and put in place by one rename, so an interrupted write
    leaves no undeclared file in a variant folder (the lesson of EX_283 F283-B01).
  - `deploy/make_installable.py`, `deploy/deploy_command.py` and `Make_Installable.bat`: the command, in DEV only:
    `INFRA`; `<family> <variant>`; several as `family/variant`; `--unmark`. One refusal does not stop the others.
  - `src/research/code_identity.py`: also gives the manifest's `[install_tool]` list. `deploy/INFRA_MANIFEST.ini`:
    that section added, with the five tool files.
- **Two interpretations made, to be put to the reviewer with slice A:** (1) a variant may import its own listed
  files as well as its helpers (specification 3.4 names "the helpers list or the infrastructure"; a second file
  on a variant's `files` list would otherwise be unusable); (2) an infrastructure file a variant imports must be of
  class `forecast`, refused by the tool itself and not only by the suite's test.
- **Tested:** `tests/test_trees_readiness.py`, 38 tests, each named for its rule. Run on the real repository: the
  40 real variants pass the import check with no fault, and the real infrastructure imports nothing that is not
  on the real manifest. 32 faults were planted in the three files; all were caught (two only after a test was made
  to look at the reason's words). The engine's identity (25) and manifest (9) tests and the settings tests (32)
  still pass.
- **A small question for the owner:** whether the markers are tracked by Git or ignored. The ratified documents do
  not say. Claude recommends ignored, like `VARIANT_STATUS.ini`: a marker is his act on his PC, is made again in
  seconds, and Git could otherwise deliver one he did not make.
- **Still to come in slice A:** the LF pin, `INSTALLED_FILES.json`, the environment's digest over the fixed
  inventory, `Check_Tree`, the launch guard, and the design amendment's wording (entry 222).
- Nothing is authorised on the owner's PC. TASK_T028 r1 waits for his go.
- Next numbers: EX_303; entry 226; RAT-47.

## 226. 24 November 2026, 17:16 - the three CRLF files in DEV named; one of them is shared forecasting code; a question for the owner on how line endings are pinned

- **The owner, 17:14, to Claude** (the output of `git ls-files --eol src deploy | find "w/crlf"`): the three files that
  have CRLF line endings on his disk and LF in Git are `src/methods/E_001/e1_standalone_contract.py`,
  `src/methods/_common/game_profiles.py` and `src/scrape_australian_powerball_history_from_2018_04_19_v0_3.py`.
- **What each is.** `game_profiles.py` is on the infrastructure manifest with the class `forecast`: it is part of
  the identity of the forecasting code, which every list's header records. The other two are on no manifest and
  on no variant's lists (Claude searched the manifest and every `VARIANT.json`): they affect nothing.
- **What follows, from the ratified specification.** DEV's lists were made with `game_profiles.py` as it lies on
  the owner's disk, with CRLF. If that file's bytes changed in DEV (to LF, say), the identity of the forecasting
  code would change, every list in DEV would be foreign and every variant held in both games (specification
  5.6A), and no command clears a held variant before build step 4. The way out would be to remove DEV's research
  results by hand and fill again (47 minutes). **`Init_Tree` copies DEV's bytes as they lie,** so whatever DEV holds
  when QA and PROD are created is what they hold.
- **Two ways of pinning, both tried by Claude in a throwaway Git repository made to match the owner's state**
  (`core.autocrlf=true`; a file Git itself wrote with CRLF; the stored copy LF):
  - **As it lies (`-text` for `src/**` and `deploy/**`):** Git converts nothing, ever, in either direction. Git then
    shows the three files as changed; committed (after `git add --renormalize`), Git holds exactly the bytes on
    the owner's disk, and a fresh clone with `core.autocrlf=true` gets the same bytes and the same hashes. DEV is
    untouched: no identity changes, nothing is held. Three files keep their CRLF.
  - **To LF (`text eol=lf`), as entry 181 worded it:** Git writes LF on every checkout. A file that is CRLF on disk
    stays CRLF until it is checked out again, and Git calls it unchanged meanwhile: disk and repository can
    differ without notice. Making `game_profiles.py` LF in DEV has the consequence above.
- **Claude recommends "as it lies"**, as the stronger guarantee for a system whose identities are hashes of bytes
  on disk (disk, repository and every clone equal, also after a hand edit), and because it changes nothing in
  DEV. It departs from the wording of the owner's decision of entry 181 ("LF pinned"), not from its purpose, so
  it is his to decide. Before either is packaged Claude runs the whole suite in the cloud with the file as the
  owner has it.
- **Not decided.** Nothing was changed anywhere; `.gitattributes` is as it was.
- Next numbers: EX_303; entry 227; RAT-47.

## 227. 24 November 2026, 17:17 - OWNER: Git is never an operational gatekeeper or checker; what Claude takes from it for the two open questions of entries 225 and 226

- **The owner, 17:16, to Claude,** on the two questions put to him (markers tracked by Git or ignored; how line
  endings are pinned): "git should never be used as an operational gatekeeper/checker nor for gating/checking
  deployments etc, github is a tool for managing commits and project statuses."
- **It is already the ratified rule, and the new system keeps it.** Specification v0.6 section 2: "Git and GitHub
  are DEV conveniences only (owner). No install, run, copy, backup or restore needs them". Deployment design v0.12
  section 0: "Installs copy named files from the DEV folder on this PC. No Git, no network." Claude searched the
  engine and the step 3 working files for any use of Git: there is none (one refusal's advice mentions it). What
  decides readiness, identity and a tree's integrity is the project's own tools reading bytes on disk: the
  markers, the identity recorded in each list, and the list of installed files.
- **A fault in how Claude put entry 226, corrected here.** It argued for a pin by saying that disk, repository and
  every clone would then hold the same bytes, which reads as if Git were the assurance. It is not. The only
  purpose of a line-ending setting is to keep Git from altering DEV's files behind the tools' backs, which would
  make a marker stop matching or, for an installed variant, be refused as "different bytes".
- **What Claude takes from his words, and works on unless he says otherwise:**
  1. **The markers are not tracked by Git.** They are the state of one tree, made by his own command on his PC;
     `.gitignore` gets two lines for them, as it has for the status files.
  2. **Git is set to store the code exactly as it lies and never to convert it** (`-text` for `src/**` and
     `deploy/**`; entry 226's first way): Git as a plain store, doing nothing to the files. The three files that are
     CRLF on his disk are committed as they are, once. Nothing in DEV changes. This replaces the wording "LF
     pinned" of entry 181; its purpose is kept.
  3. **No tool of the new system consults Git, and none will.** The sheets that install a package into DEV go on
     using Git for what it is for: committing.
- He has not said "option 1" in so many words; item 2 is Claude's reading of his principle and is his to overturn.
  Nothing is installed or changed by it: it reaches his PC only in a reviewed package, on his own go.
- Next numbers: EX_303; entry 228; RAT-47.

## 228. 24 November 2026, 17:19 - OWNER: no halfway house on line endings; entry 227's item 2 is overturned; Claude's proposal for consistent LF, checked by the project's own tools

- **The owner, 17:18, to Claude,** on entry 227's item 2 (store the code as it lies, three files staying CRLF):
  "option 1 leaves things in a halfway house which will most definitely catch us out later; I prefer being
  consistent if possible."
- **So item 2 of entry 227 is overturned.** Items 1 and 3 stand (the markers are not tracked by Git; no tool of the
  new system consults Git).
- **Consistency is possible.** Claude checked the repository: every one of the 587 non-empty files Git tracks
  under `src` and `deploy` is stored with LF, and all 28 batch files are held as CRLF by the existing rule. Only
  the three working copies on the owner's disk differ (entry 226).
- **Claude's proposal, in line with his principle of entry 227 (the project's own tools check, not Git):**
  1. **One rule: the project's code is LF, batch files are CRLF, no exceptions.** The three files are made LF on
     his disk, once, by a step of the install sheet.
  2. **The project's own tool enforces it:** `Make_Installable` refuses to mark a variant or the infrastructure
     ready if a listed `.py`, `.json`, `.ini` or `.txt` file holds a carriage return, or a listed `.bat` file a
     line that does not end CRLF, naming the file. Nothing with the wrong line endings can then be marked, so
     nothing with them can be installed. Git is not asked.
  3. **Git is only told to keep LF** (`text eol=lf` for `src/**` and `deploy/**`, the batch files' rule and the
     existing byte-for-byte lines kept), so that Git itself never hands out a CRLF copy. That is the "LF pinned"
     of entry 181.
- **Its one cost, stated before he decides.** `src/methods/_common/game_profiles.py` is shared forecasting code and
  is one of the three. Making it LF changes the identity of the forecasting code in DEV, so every list DEV holds
  becomes foreign and every variant held (specification 5.6A), and nothing clears that before build step 4. On
  the day step 3 is installed in DEV, DEV's research results (`results\research\`, ignored by Git, made by the
  first fill of entry 212) would therefore be removed by hand and filled again: about 47 minutes, unattended. QA
  and PROD are not affected: they are created afterwards and start clean. No forecast changes: the comparison
  with the old records compares scientific content, and line endings change no calculation.
- **Waiting on the owner:** his yes to that cost (the removal of DEV's research results is a deletion, which needs
  his own approval, given again on the day).
- Next numbers: EX_303; entry 229; RAT-47.

## 229. 24 November 2026, 17:34 - OWNER (thinking it through, not yet a decision): Windows-native line endings for everything a person writes or reads; all code to be checked against the standard once set

- **The owner, 17:25, to Claude:** "let's think this through first.  We are running on Windows 11.  What is the
  standard for Win10/win11 files especially .bat and .py files, if there are standards or usual expectations ...
  what do we break and/or miss out on (eg vscode, VS, editors like notrpad, norepad++, running them, viewing
  reports, printing files, etc)  ?"
- **The owner, 17:31,** after Claude's answer (Windows-native text is CRLF; only batch files need it; modern Windows
  tools handle LF; a new file made in a Windows editor defaults to CRLF): "if .bat should be crlf then I suggest so
  should code files like py  json ini etc etc and reports logs txt files  etc (I do not have a full list of what are
  created/used in this project I guess you will) too - I do not know enough about data files to suggest for
  those.  Especially since a new file created in a Windows editor defaults to CRLF and I may or may not be doing
  that all the time.  At one level, the number like 584 is not relevant since we need to get it right and be
  consistent (not only the files themselves but also the git stuff which specifies converting things to/from one
  or the other)."
- **The owner, 17:32:** "I suppose we will need to check all out code to ensure we follow whatever standard we
  establish."
- **So entry 228's proposal (code LF) is not accepted;** the direction under discussion is CRLF for what people
  write and read. Nothing is decided and nothing has been changed.
- **Facts Claude gathered for it (from the repository, by tool):**
  - Tracked under `src`: 172 `.py` files and 415 `.json` files; all LF in Git. Of these the new system hashes and
    installs about 150: 32 infrastructure files, 80 files of the 40 variants (a declaration and a method each) and
    39 helpers. 28 batch files, CRLF on disk by the existing rule, LF inside Git.
  - **The data files are already as their writers made them, and Git stores them untouched:** each game's results
    master and its ledger are CRLF; the verification and opening records are LF. Their bytes are fingerprinted
    (a ledger records its master's SHA-256), so nothing may ever convert them.
  - The engine writes its lists, ledgers, status files and reports with LF, by explicit choice in the code.
  - Byte-pinned files of the old system must stay as they are: `src/package_tools/process_check.py` and
    `src/results_master_v0_2.py` (tests check their bytes), the install records, the old run records under
    `results/`, the sealed Mode H records. Several old tests already compare source files with CRLF made LF first.
  - Documents and exchange files are mixed in Git today (about 1,990 LF, 920 CRLF, 10 mixed); no tool hashes them.
- **Claude's view, put to the owner in the chat:** his point about the editors' default is the deciding one: the
  person's ordinary tools should produce conforming files, and the machine side (Claude's packages, made on Linux)
  can be made to conform and checked. Two kinds of file, one rule each: **text that people write or read** (code,
  declarations, manifests, settings, batch files, reports, logs, read-me files): CRLF; **records whose bytes are
  the record** (results and ledgers, lists, the OV-1 ledger, status files, markers, sealed and install records):
  exactly as their format defines, written only by programs, never converted. **Git converts nothing** in the
  operational folders, so that the bytes on disk are the bytes committed and the bytes GitHub shows. **The
  project's own checker** enforces it. Proposed next step, on his word: a one-page standard with the full
  inventory of file kinds, and a trial conversion in the cloud with the whole suite before and after, before he
  decides.
- Next numbers: EX_303; entry 230; RAT-47.

## 230. 24 November 2026, 18:02 - OWNER: a written standard for the form of every kind of file, everything to conform, Git and GitHub settings to match; the draft standard v0.1 and the cloud's trial conversion

- **The owner, 17:42, to Claude:** "OK. we should create a spec or add to an existing spec for this - expressly have
  a list of file types and/or data types and exactly which type they use so that there is never any ambiguity (and
  add a section to the operations manual "standards"). "Sealed and byte-pinned old-system files stay as they are"
  ... no they don't, everything confirms to the standards, I do not care whatsoever if it means
  conversions/editings in-place with regenerations of fingerprints or whatever ...; whatever it takes to get it
  done (safely) then we do it eg a conversion program and manifest or whatever you need. Also ensure our git
  settings files stuff and github settings all do the right thing."
- **The owner, 17:43:** "PS I dop not currently care about obsoleted Mode H stuff."
- **So directed (owner):** a written standard, listing each kind of file and its exact form; everything conforms,
  by conversion in place and regeneration where needed, done safely (a conversion program and its list); the Git
  settings files and GitHub's settings to do the right thing; a "Standards" section in the operations manual (added
  to that deferred work item, entry 220).
- **Written, a DRAFT for his reading and decisions:** `exchange/CLAUDE_WEB_TOOLS/standards/FILE_FORM_STANDARD_v0_1_DRAFT.md`
  (SHA-256 `06947f8470796418f4e20e280423033792535552f4277cb3e28f142dcd625cd9`). In short: every text file of the living project is CRLF, whoever wrote it; the one
  exception by its nature is the hash-chained record lists (`.jsonl`), each line of which is the canonical encoding
  of a record whose bytes, ending included, the chain and the content digests hash; every program names the line
  ending it writes (Python's default differs between the owner's PC and the cloud); Git converts nothing
  (`* -text`); the project's own checker enforces it in the suite, in `Make_Installable` and in `Check_Tree`; the
  conversion is made by a program from a list with each file's SHA-256 before and after. Frozen history (the
  exchange, the reviews, the archive, the ratified documents, the old system's own records) is left as it is.
- **The trial in the cloud** (`TRIAL_CRLF_SUITE_COMPARISON.txt` beside the draft, SHA-256 `8baac6b033e2b60fb9f5f1ed6bb2f666bae4e455d7779b9db906c4da9d2e26af`): 669 text files
  under `src`, `deploy`, `tests` and the root made CRLF in a copy; the whole suite before and after. **732 of 762
  tests gave the same result; 30 changed from passing to failing, all in five modules of the retired Mode H release
  machinery; every test of the new engine and of the methods' arithmetic passed unchanged.** The 30 trace to six
  files that tests pin to their bytes (the three install and release records; `process_check.py`;
  `results_master_v0_2.py` and the reference copy of its predecessor). With those six put back, all five modules
  passed again and the three known failures were as before.
- **Five open points are put to the owner** (the draft's section 8): the scope (frozen history left alone,
  recommended); the `.jsonl` lists staying LF (recommended); `* -text` for the whole repository (recommended; one
  refresh of his working copy on the day); the results' verification records; and the six pinned files of the
  retired machinery (recommended: named as frozen and left, which also keeps entry 181's "`results_master_v0_2.py`
  stays untouched in DEV"; his words of 17:42 point the other way, his words of 17:43 this way: his to say).
- **A binding rule is not touched by any of this without his express word:** the sealed Mode H records are never
  altered. The draft leaves them, and all the old system's records, exactly as they are.
- **Effect on build step 3:** the standard and the conversion come before slice A is packaged, because the markers
  and the list of installed files hash these bytes. Slice A's working files so far stand. It adds a review round
  and an install day before the first tree, at the one time it is cheap: no tree exists yet.
- **Not done:** nothing is converted anywhere but in Claude's trial copy; no code of the engine is changed;
  `.gitattributes` is as it was; what GitHub's web editor does to line endings is still to be confirmed from
  GitHub's documentation.
- Next numbers: EX_303; entry 231; RAT-47.

## 231. 24 November 2026, 18:30 - OWNER: the five open points of the file-form standard decided; the standard's CANDIDATE v0.1 written for the reviewer

- **The owner, 18:28, to Claude:** "1. ok yes to your recommendation scope freezing historical documents that are not
  "actively used" in a DEV/QA/PROD program running sense, assuming they are "only documents to read".    2.  yes to
  your recommendation  the `.jsonl` record lists stay LF as long as they are noted as such in the standard and
  operations manual. 3 yes to recommendation `* -text` for the whole repository . 4. yes to your recommendations
  converting things like results' verification records even if hashed (redo the hashes if and when needed) 5.  yes
  to your recommendation ignoring retired machinery and we should note that in the standard.  As a principle for
  this mass conversion, if hashes need redoing then do it even if fudging is somehow necessary - our priority is to
  safely convert and move toward making everything operational."
- **DECIDED (owner):** (1) frozen history is left as it is: what people only read and no program running in DEV, QA
  or PROD uses; (2) the `.jsonl` record lists stay LF, noted as such in the standard and in the operations manual;
  (3) `* -text` for the whole repository; (4) the results' verification records are converted with everything
  else, hashes redone where needed; (5) the retired Mode H release machinery is left out, noted by name in the
  standard. **The principle:** where a hash must be redone for the conversion it is redone; the priority is a safe
  conversion and an operational system.
- **How Claude carries out the principle, said plainly so that it is his to correct:** a hash is redone openly. The
  conversion's own record keeps each file's SHA-256 before beside its SHA-256 after, so any hash recorded earlier
  can still be checked by anyone; nothing is made to look as if it had always been so, and no record of the frozen
  history is rewritten to match. Claude does not expect anything beyond that to be needed.
- **Written:** `exchange/CLAUDE_WEB_TOOLS/standards/FILE_FORM_STANDARD_v0_1_CANDIDATE.md` (SHA-256 `00ec02b005813b88927ae22d2afef9e83f22efae3555d760363174248c236872`), made from the
  draft of entry 230 (kept). New in it: the status; section 3A, which names the six files of the retired machinery
  that stay as they are, and says that the sealed Mode H records and the old system's other records are frozen
  history and that the binding rule on the sealed records is untouched; the owner's five decisions in his words
  (section 8); how a hash is redone (section 7); section 11, what is still to be established before the
  conversion is packaged.
- **Established for decision 4:** the new reader names a game's verification record and takes no hash of it; the
  old system's runner recorded that file's SHA-256 in its run records, which are frozen history and keep the old
  value. The results masters and their ledgers are CRLF already.
- **Not established:** what GitHub's editor in the browser does to a file's line endings (Claude searched; nothing
  authoritative for GitHub). The candidate therefore says that no file of the living project is edited or created
  in the browser, and that the project's own checker is what finds a wrong form.
- **Next:** the reviewer's reading of the candidate; then the owner's ratification (RAT-47); then the conversion
  program and its list, the engine's writers, the checker, the Git settings, the sheet, the runner's rehearsal.
  Nothing is converted anywhere. TASK_T028 r1 still waits for the owner's go.
- Next numbers: EX_303; entry 232; RAT-47.

## 232. 24 November 2026, 18:48 - the reviewer chat ended after EX_303; at the owner's request Claude refreshes the reviewer's installed H-2 v6 as the H-2 v6r2 CANDIDATE, for starting a new reviewer chat

- **The owner, 18:44, to Claude:** "before you look at ex_303, chatgpt has just died on us yet again without notice.  As
  a priority can you please check for it's latest handover doc(s) and update them to be current so we can do a
  handover asap; once the handover is complete, please proceed with ex_303."
- **Checked against `main` (`27a18a2`):** the reviewer's newest handover is the installed H-2 v6 (RAT-46, entry 216;
  SHA-256 `588c52b9c08781956330676a3c13bda99b0c8fd90211139f74c26503adf174a1`) with its blurb (`58c8f5b2b13dabc63f3739c04a42dd6bb30784fcf9c40b504e65da72c8c8efe3`); the reviewer committed
  nothing after EX_303 (`27a18a2`, SHA-256 `bb88b1ca53c560c20360d949550843907c94c4b66c97e5b170b2a1fc6f90172c`). H-2 v6's evidence cutoff is entry 215; it knows
  nothing of entries 216 to 231 or of EX_297 to EX_303.
- **What Claude did, as on 21 and 23 November 2026 (H-2 v3r10, H-2 v5r1; entry 173): a new file, the reviewer's
  files not changed.** `exchange/CLAUDE_WEB_TOOLS/h2v6r2/make_h2_v6r2.py` with `h2_v6r2_texts.py` reads the installed
  H-2 v6 and its blurb from Git (each asserted by SHA-256), makes ten counted replacements of status statements in
  chapter 0 (the title; a refresh notice; RAT-46 recorded as entry 216; build step 3's GO; the superseded "pin
  LF" sentence; the housekeeping paragraph; section 0.12's first sentence), each marked "v6r2", and adds **one new
  section, 0.13,** with everything since: the records; build step 3's GO and plan, its review and the owner's
  decisions; the process readers; TASK_T028 r1; the operations manual; slice A's working files; the owner's
  principle on Git; line endings and the file-form standard with its trial and his five decisions; EX_303 and its
  four clarifications; Mode H; the state of his PC; the order of work. Sections 0.4 and 0.5 and the historical
  chapters 1-19 are byte-identical (asserted). The blurb likewise, by seven counted replacements.
- **Written, under `exchange/CLAUDE_WEB_TOOLS/h2v6r2/out/`:**
  - `ChatGPT_Reviewer_Handover_H2_v6r2_CANDIDATE_20261124.md`, SHA-256 `b078323351f37d370980d9a75dfcae98834f7cec7d94d0e1e6fb894da3617621`;
  - `ChatGPT_Reviewer_Handover_H2_v6r2_CANDIDATE_20261124_introductory_blurb.md`, SHA-256 `c227314861daa9994bf9e6ff9da455759ee76a89d564ed04c47816754221215b`;
  - `H2_v6_TO_v6r2.diff` and `H2_v6_TO_v6r2_blurb.diff`: each, applied with `patch` to the installed file, gives the
    candidate byte for byte (checked with `cmp`). Every SHA-256 quoted in section 0.13 was checked against its
    file by a script.
- **Its standing:** a CANDIDATE written by Claude; not ratified; no reviewer has checked it; the blurb and the
  refresh notice say so and ask the new reviewer chat to verify it against H-2 v6, the decision log and the
  repository. **In force for the reviewer: still H-2 v6 (RAT-46).** The owner can start the new chat from the
  candidate's blurb at once; ratifying and installing it in `doc/HANDOVER/` is his to choose, now or after the new
  reviewer has checked it, and would take the next RAT number.
- **EX_303** (FOCUSED RECHECK of the file-form standard's wording before ratification; four clarifications, FFS-C01
  to FFS-C04): read for this refresh only; Claude answers it next, as the owner asked. **The reviewer has used
  EX_303; Claude's next number is EX_304.**
- Next numbers: EX_304; entry 233; RAT-47.

## 233. 24 November 2026, 18:51 - EX_303 (reviewer, its last message): the file-form standard FOCUSED RECHECK, four clarifications, all accepted; the candidate v0.1r1; one point put to the owner

- **EX_303** (reviewer; main `27a18a2`; SHA-256 `bb88b1ca53c560c20360d949550843907c94c4b66c97e5b170b2a1fc6f90172c`): the standard's policy is supported; a FOCUSED
  RECHECK of the candidate's wording before ratification; the six named exceptions of section 3A accepted; four
  clarifications asked. Answered at the owner's request after the handover (entry 232).
- **All four accepted as found, and made in v0.1r1:**
  - **FFS-C01.** "Everything a tree holds" took in a tree's `.venv`, which is other people's packages. Now the
    standard covers the project's own files, in named places; `.venv`, `.git`, Python's caches and what tests write
    in temporary folders are never converted and never checked by it. And it says what becomes of DEV's own
    untracked files at the conversion: `ENVIRONMENT.ini` is converted by rule, its hashes recorded; DEV's research
    results, its status files and leftovers in `records\` are removed on the owner's go and written afresh (a
    status file holding anything but `ACTIVE` stops the program for his decision); the results masters and ledgers
    (CRLF already), the updater's grabs and backups, the Mode H opening records, the old system's records,
    `transitory_data\`, the six files and `.venv` are untouched, the masters' and ledgers' hashes shown unchanged;
    any other text file found stops the program. The program walks the folders itself and never calls Git. The
    checker's three uses each have a written scope.
  - **FFS-C02.** A row for Git's own settings files and `LICENSE` (CRLF; Claude tried Git 2.43 with CRLF `.gitignore`
    and `.gitattributes`: both are read correctly); every `.jsonl` file is LF, the reason being the hash-chained
    lists, without calling the logs chained; a new section 3B says exactly what conforms (no bare LF and no bare
    CR in a CRLF file; no CR in a `.jsonl`; an empty file conforms; a last line without an ending is allowed and
    left; a text kind must read as UTF-8 with no zero byte or it is refused, never excused as binary; binary by
    kind alone; an unnamed kind is refused until the owner's recorded decision extends the table).
  - **FFS-C03.** The root `* -text` does not govern `GAIS\`, which has two attribute files of its own; the standard
    now says so. Commits come from the owner's PC or from Claude's cloud workspace, each checked for the form of
    the staged bytes: a check of a commit, never of a tree's readiness.
  - **FFS-C04.** A listed file whose hash is the list's "after" is passed over, "before" is converted, any third
    value is a STOP, so an interrupted run is simply run again; it can be undone from the same list; it holds the
    job lock and the updater's lock; the owner makes his own copy first; old lists are removed, not repaired; what
    the cloud's trial did and did not prove is stated.
- **Written:** `exchange/CLAUDE_WEB_TOOLS/standards/FILE_FORM_STANDARD_v0_1r1_CANDIDATE.md` (SHA-256 `5a4d8a234a02951635e1c01032007d84ee82f80befacd2806098ea4a89f8485c`), made from
  v0.1 (`00ec02b0...236872`, asserted) by `make_standard_v0_1r1.py`; the exact difference
  `FILE_FORM_STANDARD_v0_1_TO_v0_1r1.diff` (SHA-256 `e5dffbe3ea0db3f32ab19a78f6004c0e29b10f5ff60c0d3a490041f12a065437`) rebuilds it with `patch` (checked with `cmp`). v0.1 and
  the trial's evidence are unchanged.
- **One point is put to the owner (v0.1r1 section 8 item 6):** his decision 3 of entry 231 was "`* -text` for the
  whole repository"; the root file cannot govern `GAIS\`, and Claude never writes there. Recommended: he assents to
  "nothing converts anywhere in this project; `GAIS\` keeps that other project's own rules".
- **Next:** the new reviewer chat's focused recheck of v0.1r1, when the owner asks; then his ratification. Nothing
  is converted; no code is changed.
- Next numbers: EX_304; entry 234; RAT-47.

## 234. 24 November 2026, 18:59 - OWNER: `GAIS\` is out of the file-form standard's scope and keeps its own Git rules; a new reviewer chat is started

- **The owner, 18:59, to Claude,** on the one point put to him (entry 233; the standard v0.1r1 section 8 item 6):
  "re "One question for you" I was referring to yes to your recommendation, ok "`GAIS\`" tree is out of scope as
  historical subproject, so yes to your recommendation. New blurb pasted to chatgpt now."
- **DECIDED (owner):** the statement of the standard's section 5 stands: Git converts nothing anywhere in this
  project; `GAIS\`, a historical subproject outside the standard's scope, keeps its own Git attribute files and
  their rules. Nobody changes anything under `GAIS\` for this.
- **The candidate is not reissued for it.** v0.1r1 (`5a4d8a23...f8485c`) is with the reviewer as it is; its section 8
  item 6 says "put to the owner, not yet answered". That status line is brought up to date when the ratified
  text is installed, by a script with its exact difference, as is done for the handovers.
- **A new reviewer chat is started:** the owner pasted the blurb of the H-2 v6r2 candidate (entry 232). In force
  for the reviewer: still H-2 v6 (RAT-46); v6r2 is Claude's unratified refresh, which the new chat is asked to
  verify.
- **Waiting on:** the new reviewer's takeover and its focused recheck of the standard v0.1r1; then the owner's
  ratification of the standard; the owner's go for TASK_T028 r1.
- Next numbers: EX_304; entry 235; RAT-47.

## 235. 24 November 2026, 19:03 - EX_304 (the new reviewer chat): the standard v0.1r1 rechecked, three PASS, one narrow correction; made as v0.1r2

- **The owner, 19:02, to Claude:** "EX_304_ChatGPT.md is committed at main 87c0a9b2cd537e5faa11ebd7c028947b4bd16822.
  FFS-C01, C02 and C03 PASS, including owner entry 234. FFS-C04 requires one narrow correction: remove the
  unsupported independent undo promise and rely on the verified pre-conversion copy. No broader review or policy
  change requested. Please read EX_304."
- **EX_304** (the new reviewer chat's first message; main `87c0a9b`; SHA-256 `3e518407042125dde2a6aa33241870567fb5cfbf572152bb402be0d63df58908`): FFS-C01, FFS-C02 and
  FFS-C03 PASS (the owner's assent of entry 234 noted; section 8 item 6's status to be brought up to date at the
  documentary installation, with no candidate made for that alone). **FFS-C04: one narrow correction.** v0.1r1 said
  the conversion "can be undone from the same list". The reviewer: making line endings uniform is many-to-one (a
  file with LF then CRLF and one with CRLF then LF become the same bytes), so a path and two SHA-256 values do not
  give back the original; the "before" hash can verify a recovery, not make one. It recommends RAT-47 after the
  correction, with the exact difference for confirmation.
- **Accepted as found: a fault of Claude's.** The claim was true only of a file that was uniform before, and the
  standard stated it of every file.
- **Written:** `exchange/CLAUDE_WEB_TOOLS/standards/FILE_FORM_STANDARD_v0_1r2_CANDIDATE.md` (SHA-256 `4f515726bceb31e6d92df422c8b4c0c1e8df349a780430d28bcbf40bd9204f51`), made from
  v0.1r1 (`5a4d8a23...f8485c`, asserted) by `make_standard_v0_1r2.py`; the exact difference
  `FILE_FORM_STANDARD_v0_1r1_TO_v0_1r2.diff` (SHA-256 `51b15aa9d64c4b1f9d678b901e5fdcde48f51805ea09a4ba605b52eacc6972d7`; three hunks) rebuilds it with `patch` (checked
  with `cmp`). **What changed, and nothing else:** the title and a note of the revision; the undo promise removed;
  in its place: recovery is from the owner's pre-conversion copy, which the program checks before it changes
  anything (every file to be converted or removed is in the copy with the same SHA-256 as in the tree); the
  recorded "before" hashes verify a recovery afterwards; the conversion list is not a backup; no undo is built;
  the copy is the one way back, also for DEV's settings file and the derived outputs that are removed.
- **Not changed in v0.1r2, as the reviewer asked:** section 8 item 6 still reads "put to the owner, not yet
  answered"; it is decided (entry 234) and is brought up to date when the ratified text is installed.
- **The reviewer has used EX_304.** Claude's next number is EX_305.
- **Next:** the reviewer's confirmation of the difference; then the owner's ratification (RAT-47). Nothing is
  converted; no code is changed.
- Next numbers: EX_305; entry 236; RAT-47.

## 236. 24 November 2026, 19:36 - EX_305 (reviewer): the file-form standard v0.1r2 FOCUSED PASS, recommended for ratification; the owner's ratification is still his to give

- **The owner, 19:36, to Claude** (relaying the reviewer): "EX_305_ChatGPT.md is committed at main
  ad682d45e39297acdd3445d1bf90af0c021fa75a. FOCUSED PASS of File Form Standard v0.1r2. All four SHA-256 checks and
  exact three-hunk diff reconstruction PASS. FFS-C01 through FFS-C04 are CLOSED. The reviewer recommends the exact
  v0.1r2 candidate for owner ratification under RAT-47. No further candidate revision or policy review requested.
  One implementation watchpoint, not a ratification gate: on interrupted conversion resumption, verify the backup
  against the original recorded before hashes, not the already-converted live files. Update section 8 item 6's
  status at documentary installation to reflect entry 234. Existing implementation review and owner GO
  requirements remain. Next EX: EX_306. Please read EX_305."
- **EX_305** (reviewer; main `ad682d4`; SHA-256 `37f0642c24eb1eb59500dd2eac542a329b908d31595fd968cdeafa09f1187360`), read in full: FOCUSED PASS; all four findings of
  EX_303 closed; the exact candidate v0.1r2 (`4f515726bceb31e6d92df422c8b4c0c1e8df349a780430d28bcbf40bd9204f51`) recommended for the owner's ratification as RAT-47.
- **The watchpoint, taken into the conversion program's design:** when an interrupted conversion is run again, the
  owner's copy is checked against the "before" hashes recorded at the first run, not against the tree's files,
  some of which are by then converted.
- **Not ratified yet.** The message above relays the reviewer's recommendation; it is not the owner's own
  ratification, and Claude installs nothing on it (the lesson of entry 215). On his word Claude installs the
  ratified text in `doc/` by a script, with the status lines and section 8 item 6 (decided, entry 234) brought up
  to date and the exact difference kept.
- **The reviewer has used EX_305.** Claude's next number is EX_306.
- Next numbers: EX_306; entry 237; RAT-47.

## 237. 24 November 2026, 19:38 - RAT-47: THE OWNER RATIFIES the file-form standard (the candidate v0.1r2); installed as doc/FILE_FORM_STANDARD_v0_1.md

- **The owner, 19:36, to Claude, in his own words:** "I ratify the file-form standard v0.1r2 (RAT-47)."
- **RAT-47 is recorded** (RAT-46 was the last number used). Ratified: the exact candidate
  `exchange/CLAUDE_WEB_TOOLS/standards/FILE_FORM_STANDARD_v0_1r2_CANDIDATE.md`, SHA-256 `4f515726bceb31e6d92df422c8b4c0c1e8df349a780430d28bcbf40bd9204f51`, which has the
  reviewer's FOCUSED PASS (EX_305, entry 236).
- **Installed by Claude** with `exchange/CLAUDE_WEB_TOOLS/rat47/finalise_rat47.py` (the candidate asserted by hash; the
  statements the ratification made out of date changed by replacements that each match exactly once; the installed
  file must not exist already): **`doc/FILE_FORM_STANDARD_v0_1.md`, SHA-256
  `97034474f1a7e9c54a14b9554b45666cb1fa031d566545433a0412d4312f8335`.** The exact difference from the candidate:
  `exchange/CLAUDE_WEB_TOOLS/rat47/FILE_FORM_STANDARD_v0_1r2_CANDIDATE_TO_FINAL.diff` (SHA-256 `12fd942ce72441750b0b9708857a3e4d090a2e2009e55d7b5da2da2d002bc535`), which rebuilds the
  installed text with `patch` (checked with `cmp`). **What differs, and nothing else:** the title; the status
  paragraph (ratified, RAT-47, this entry; where the draft, the candidates and the evidence are kept); "one point
  was put to the owner; he has decided it"; **section 8 item 6, now recorded as decided by him in entry 234, with
  his words** (as the reviewer asked in EX_304 and EX_305); section 5's pointer to it; the path of the trial's
  evidence. The candidate is unchanged.
- **What RAT-47 is:** a note of ratification to the specification v0.6, beside the coding practices. It replaces the
  words "LF pinned" of entry 181 and the specification's section 20 advice on pinning line endings in
  `.gitattributes`. **What it is not:** it converts nothing and authorises no conversion, install or run; each is
  the owner's own go.
- **The installed file's own line endings.** It is written with LF, like every document Claude has committed so
  far. The standard's section 5 has Claude's own new files in CRLF "from then on", that is from the day of the
  conversion, when `* -text` is in place and the owner's working copy is refreshed; a single CRLF document
  committed before that day would be the halfway house the standard exists to end.
- **In force now:** the specification v0.6, the deployment design v0.12, the coding practices v0.1 (RAT-40) and
  **the file-form standard v0.1 (RAT-47)**; the runner's rulebook v0.7 (RAT-44); H-1 v10 (RAT-45); H-2 v6
  (RAT-46), with Claude's unratified refresh H-2 v6r2 in use by the new reviewer chat.
- **A refresh of the handovers is due** (Claude's assessment): H-1 v10 knows nothing of build step 3's plan and
  decisions or of this standard; the continuity page and H-2 v6r2's section 0.13 carry them meanwhile.
- **Next for Claude, in the cloud:** the conversion list and program (the reviewer's watchpoint of entry 236 taken
  in), the engine's writers, the checker, the Git settings, the sheet and the runner's rehearsal; then slice A.
- Next numbers: EX_306; entry 238; RAT-48.

## 238. 24 November 2026, 19:44 - at the owner's request Claude brings its own handover up to date: the H-1 v11 CANDIDATE and its blurb

- **The owner, 19:40, to Claude,** after Claude said a refresh of the handovers was due (entry 237): "yes please
  update your handover stuff right now."
- **Why now:** H-1 v10 was installed this morning (RAT-45) and knows nothing of entries 216 to 237: build step 3's go
  and plan, the owner's decisions on it, the probe task, the process readers, his principle on Git, the file-form
  standard (RAT-47), the change of reviewer chat. This chat is long.
- **What Claude did:** `exchange/CLAUDE_WEB_TOOLS/h1v11/make_h1_v11.py` with `h1_v11_texts.py` reads the installed
  H-1 v10 and its blurb from Git (each asserted by SHA-256), makes nineteen counted replacements of status
  statements, each marked "v11" (the title and edition; what is authorised; the superseded "LF pinned" in three
  places; the fourth ratified document in the reading list and in section 4.1; the reviewer chats and the
  reviewer's handover in force; section 10 items 2 and 3; section 12.8), and inserts **one new section, 0D,** after
  section 0B, with everything since H-1 v10 in seventeen items: the records; the go; the plan and its review; the
  owner's decisions; the process readers; TASK_T028; slice A's working files; his principle on Git; the file-form
  standard; the conversion as the next work, with the reviewer's watchpoint; what the trial showed and did not;
  Mode H; the operations manual; the reviewer chats; the state of his PC; what waits; and seven lessons of the
  day. It ends with a table of nine identities whose SHA-256 the builder computes from Git. Sections 1, 2 and 2A
  are byte-identical (asserted). The blurb likewise, by five counted replacements.
- **Written, under `exchange/CLAUDE_WEB_TOOLS/h1v11/out/`:**
  - `Claude_Primary_Handover_H1_v11.md`, SHA-256 `71b3f08c369dd38ccbe40690fa947e8ef4e2094a33a9419e1739beb43b94e2e5`;
  - `Claude_Primary_Handover_H1_v11_introductory_blurb.md`, SHA-256 `1ebcb8eae3660d49647004f59078900281c5c6538ab8a354d7439ae459606495`;
  - `H1_v10_TO_v11.diff` and `H1_v10_TO_v11_blurb.diff`: each, applied with `patch` to the installed file, gives the
    candidate byte for byte (checked with `cmp`).
- **Its standing:** a CANDIDATE; not ratified; the reviewer has not read it. In force for a Claude chat: still H-1
  v10 (RAT-45). **If this chat ended now, a new Claude chat can be started from the candidate's blurb at once:** it
  points at the candidate and tells the new chat to check it against H-1 v10. The usual course: the reviewer reads
  the difference, then the owner ratifies (that would be RAT-48), then Claude installs it in `doc/HANDOVER/`.
- **Its limits, stated:** it is a refresh, not a rewrite. Older sections (0B, 7, 10, 12, the appendices) keep H-1
  v10's text where today changed nothing in them, and where today did, they carry a "v11" note that points to
  section 0D. A full rewrite is due after the conversion and slice A, when the installed code has changed.
- Next numbers: EX_306; entry 239; RAT-48.

## 239. 24 November 2026, 19:47 - the owner's GO for TASK_T028 r1 on his PC; the runner instructions given; the H-1 v11 blurb is with the reviewer

- **The owner, 19:46, to Claude:** "first, GO to execute TASK_T028 r1 on my Windows PC, exactly as reviewed and
  passed in EX_302, under the existing RAT-44 runner rules. Please provide the runner instructions.   I have pasted
  the blurb to chatgpt."
- **What the go covers:** the one run of `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028.md` r1 by the local runner,
  with its probe `inbox/TASK_T028_probe.py` r1, under rulebook v0.7. Nothing else: no install, no tree, no
  conversion, no other task.
- **Checked by Claude before giving the instructions (computed, at `main` `8309961`):** the task file's SHA-256 is
  `96e2a6cf86873a9f6a1df1f9e9d3ec2c884e3a8f19b767395498b7ab7f88b02c` and the probe's is
  `57fde59dc4f56526c1a73e95e006fee63b80bbffa223206740ee64776c6128bf`, in the working copy and in Git alike: the two
  values EX_302 passed. Neither file has changed since.
- **The instructions given to the owner** (the task file's own "before the owner starts"): nothing of the project
  running; the folder `D:\DELETE_ME` existing and `D:\DELETE_ME\a_p_r_i_r\T028` not; `git pull --ff-only` in the main
  repository; a new Claude Code conversation there; then `Do inbox\TASK_T028.md`; afterwards `git push`, and the
  scratch folder left in place whatever the result.
- **What to expect, said beforehand:** about ten to fifteen minutes; two ZIP files of perhaps 100 to 300 MB each in
  the scratch folder; the words `WINDOWS SAID NO` in step 5 are answers, not failures; step 8's reading of Windows
  through the standard library has run nowhere, so a STOP there is possible and harmless (the other two parts are
  recorded by then); on any STOP nothing is retried and the folder stays as it is.
- **Claude pushes nothing from now until the owner's push of the report is on `main`,** so that his push cannot be
  refused. Meanwhile Claude works in the cloud on the conversion program and the checker, uncommitted.
- **The blurb pasted to the reviewer** is the paste block of entry 238 (the H-1 v11 candidate's difference to read).
  Its answer, if one comes, would be EX_306.
- Next numbers: EX_306; entry 240; RAT-48.

## 240. 24 November 2026, 20:03 - TASK_T028 r1 ran on the owner's PC: PASS, every measurement made; what it found and what follows for build step 3; one thing the report leaves out

- **The run:** by the local runner, 19:50 to 20:00, at `main` `070b7c4`; report
  `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T028.md` (SHA-256
  `69315a498ac59f5cb558786a89d8b5bbd8c1ba98f87d3e3660c00bfc4a5be7a5`), committed by the runner as `b31ec37` and pushed
  by the owner. RESULT: PASS; the three parts each ended `FINISHED` with exit code 0; deviations: none stated.
- **The owner, 20:00, while it ran:** "looks like a python error somewhere near "check the local timezone", lets see
  what the report says I suppose." **At 20:02 he pasted what he had seen:** the output `+1030 CAST`, then a Python
  line of the runner's own, not from the task file, that was to look through the finished report for non-ASCII
  characters and for a user-folder path, and failed with `SyntaxError: (unicode error) 'unicodeescape' codec can't
  decode bytes in position 2-3` (it wrote `C:\Users` in an ordinary string); exit code 1.
- **What that was, as far as the paste shows:** two commands of the runner's own, after the task's steps: one that
  printed the PC's offset and zone abbreviation, and a self-check of its report that never ran (a syntax error
  stops Python before anything is done). Neither wrote anything; neither is the probe; **nothing changed the date,
  the time or the time zone** (the probe's own start times, the runner's `date` times and the owner's messages
  agree throughout). **But the report does not record them:** its Observations name two commands outside the
  numbered steps and say no unexpected message was printed. The measurements are not affected. Claude does not
  edit the runner's report; this entry is the record. **Claude's part in it:** `outbox\README.md` asks for the time
  "with time zone" while the task file allowed only `date +%H:%M:%S`, and no task file gives the runner a command
  to check its own report; the next task file will say how the time is to be written and give that check as a
  written command, so that nothing needs inventing.
- **Renames (step 5; scratch folder on D:).** Windows refused, every time, a folder's rename while a file inside
  it was open (code 5) or while another process had its working folder inside it (code 5); it refused the
  replacement of an open file (code 5) and its removal (code 32); the same operations went through at once after
  the file was closed or the other process had ended. Write-a-temporary-file-then-replace, 1,000 times: never
  refused; 0.34 seconds without forcing to disk, 1.42 seconds with `os.fsync` each time.
- **The environment as a ZIP (steps 6 and 7; the main `.venv` alone, an environment-only proxy).** 19,059 files,
  508.9 MB, longest full path 199 characters, no links, no file dated before 1980. The environment digest's fixed
  inventory (specification 13): 11,997 files, 362.5 MB; **read and hashed in 150.6 seconds the first time, 5.2
  seconds when lately read.** ZIP at Deflate level 9: 80.1 seconds, 180.2 MB (35.4%); at level 6: 20.7 seconds,
  184.5 MB (36.2%). Read back and compared: 1.8 seconds, no difference. Source read a second time: 10.5 seconds,
  nothing changed.
- **Processes (step 8).** psutil 7.2.2 and the standard library's reading (never run before today) each saw 237
  processes and the same four Python ones; the start time of Windows and the probe's own start time agree between
  the two to the last figure shown. **Every Python program started from an environment is two processes on this
  PC:** the environment's `python.exe`, and under it the base Python's `python.exe` (the helper appeared twice, the
  probe likewise with its "ancestor"). psutil could not read the command lines of 125 other programs, none of
  them Python. No `pythonw.exe` or `py.exe` was running.
- **What follows for build step 3 (Claude's reading; coding consequences within the ratified design, no change
  to it):**
  1. **Process readers: option A stands** (entry 222). The standard library gives names, parents, program paths
     and start times, and agrees with psutil. Option B is not needed.
  2. **Two processes for one program:** every process rule counts a pair as one program and leaves out the
     checking tool's own pair. A tree's own Python is recognised by the environment's `python.exe`; the base
     Python under it has a program file outside every tree, so it is recognised through its parent, its working
     folder or its command line. The old `process_check.py` already reasons this way (its rule 6.1).
  3. **A rename that Windows refuses is whole:** nothing has moved. The swaps of the design's sections 5 to 8 can
     treat a refusal of the first rename as a clean stop with nothing changed, and say plainly that something is
     open in the folder (a command window standing in it is enough: the process check, which looks at Python
     only, does not see that). The tools keep no file open and do not stand in a folder they rename. The restore
     must not be run with the tree's own Python or from inside the tree: the design already has it run from the
     recovery kit with the standard library.
  4. **The digest at the start of every job** (specification 13) may take two to three minutes when the files
     have not been read lately, which for a weekly job is the usual case: the job says what it is doing while it
     does it. On T: and G: the time may differ; the joined rehearsal measures it.
  5. **Each backup holds the environment** (design section 10): about 180 MB and about a minute and a half for
     that part alone at level 9. Level 6 would save about a minute for about 4 MB more. The design says level 9;
     Claude proposes no change now and puts the figures before the owner. A whole tree's backup is measured in
     the joined rehearsal.
- **Limits of the evidence:** one run, one evening, drive D: for the renames and drive E: for the environment; the
  first reading's slowness has no cause shown (the report cannot tell a cold cache from a virus scanner); 1,000
  replacements without a refusal do not show that one can never happen, and the tools keep treating a refusal as
  a stop.
- **The scratch folder `D:\DELETE_ME\a_p_r_i_r\T028` is no longer needed** by Claude; deleting it is the owner's.
- **The H-1 v11 candidate (entry 238) says in section 0D item 6 that this task has not run.** That is now out of
  date by this one entry; the candidate itself says the decision log prevails. Claude corrects it when the
  reviewer's reading is in, in the same step.
- Next numbers: EX_306; entry 241; RAT-48.

## 241. 24 November 2026, 20:04 - the exact line behind the error of entry 240, from the owner; it confirms that entry

- **The owner, 20:04:** "THIS WAS THE ORIGI9NATING COMMAND THOUJGH:" followed by the line, which was one shell line
  of three parts joined by `&&`: `cd` to the main repository; `date +"%z %Z"`; and the main venv's Python, by its
  full path and with `-I`, running a one-line program that opens `outbox\REPORT_T028.md` for reading, lists its
  lines holding a character above code 126, and counts mentions of a user folder.
- **What it shows:** entry 240 called these "two commands"; they were one line. `date` with a format only prints
  (that is the `+1030 CAST`). The Python part only reads the runner's own report and prints. It failed because the
  line wrote the user-folder label with four backslashes and Python received one (the error message shows
  `C:\Users`), which Python reads as the start of a Unicode escape: a quoting slip between Git Bash and Windows,
  caught before anything ran. Because the parts were joined by `&&`, the exit code 1 is that failure's.
- **Nothing in entry 240's reading changes:** nothing was written; the probe and its measurements are not
  involved; the report still does not record the line; the remedy is still Claude's (the next task file says how
  the time is written and gives the report check as a written, tested command).
- Next numbers: EX_306; entry 242; RAT-48.

## 242. 24 November 2026, 20:11 - the reviewer's first remarks on TASK_T028 (informal, relayed by the owner); two things put to the owner; the conversion's rule module begun

- **Relayed by the owner at 20:07, the reviewer's words, "without conducting a formal review":** the run is "useful
  Windows evidence for build step 3"; process detection "supports retaining option A"; "ZIP compression: level 6
  appears preferable under our KISS principle. Approximately four times faster for only 2.4% additional storage";
  the digest's cold and warm times are "worth retaining for deployment performance considerations. It does not
  justify weakening verification"; the file locking "should inform interrupted-operation and recovery testing"; the
  two unrecorded runner commands "constitute a procedural and reporting discrepancy, not an identified defect in
  the measurements ... I see no reason on the supplied facts to request a rerun"; "The process-reader design
  amendment remains subject to ratification"; "EX_306 remains uncommitted; the H-1 v11 review findings have
  already been provided"; "No new review or EX issued."
- **Put to the owner by Claude (his to decide):**
  1. **The backup's compression level.** The ratified deployment design (section 10) says Deflate level 9. On his PC
     level 6 took 20.7 seconds against 80.1 for 4.2 MB more (entry 240). In entry 240 Claude proposed no change
     for now; the reviewer prefers level 6. Claude now recommends level 6, **carried in the same narrow amendment
     of the design as the process readers** (entry 222), which has to go to the reviewer and to him anyway, so it
     costs no step of its own. Until he decides, the design's level 9 stands.
  2. **The reviewer's findings on the H-1 v11 candidate have not reached Claude.** The reviewer says they were
     given; nothing is committed (`main` checked: no EX_306) and nothing was relayed. Claude asked the owner to
     paste them or have the reviewer commit them.
- **The conversion, begun in the cloud (working files; not a package, not reviewed, nothing installed):**
  `exchange/CLAUDE_WEB_TOOLS/conversion/overlay/deploy/file_form.py`, the one piece of code that holds the standard's
  rule (the list of kinds; the six files left out by name; what conforms means; changing line endings and nothing
  else, refusing a carriage return that ends no CRLF instead of guessing; and the search of Python code for a write
  that names no line ending), and `overlay/tests/test_file_form.py`: 44 tests. In a fresh clone 42 pass, and the two
  that check the real tree fail as they must before any conversion (every file under `src`, `deploy` and `tests`
  is named as LF).
- **Found by the search of section 4, and how it differs from the standard's "17":** in the project's programs
  (`src`, `deploy`, the runner's tools) outside the six files left out by name, **two writes** name no line ending,
  both in the self-test of the old `src/two_site_results_check_v0_7.py`. Sixteen more are in
  `src/results_master_v0_2.py`, which the standard's section 3A leaves exactly as it is, so they stay; its
  successor conforms. The standard's "17 ... to be corrected" counted those as correctable: a point for the
  reviewer when the package goes to it.
- **A reading Claude will put to the reviewer with the package:** the search covers the project's programs, not the
  tests' own code. The tests write their made-up files in temporary folders about 130 times without naming a line
  ending, and the standard's section 2 puts "whatever a test writes in a temporary folder" outside itself.
- Next numbers: EX_306; entry 243; RAT-48.

## 243. 24 November 2026, 20:18 - the owner keeps Deflate level 9; EX_306 (H-1 v11: PASS for continuity, two narrow corrections); the candidate H-1 v11r1

- **The owner, 20:15, on the question of entry 242:** "yes to stay at level 9." The ratified deployment design's
  section 10 stands as it is; no amendment for the compression level. (The narrow amendment for the process
  readers, entry 222, is still to be put.)
- **In the same message:** "EX_306_ChatGPT.md is now committed at main 5c6ab268c16b377af85cdc550a6d29f4bbee27ea.
  Read-back verification PASS." and "The owner has confirmed continuation of the reviewer's established commit
  rights." Claude read `exchange/EX_306_ChatGPT.md` (SHA-256
  `e8a2813a9dc1cf4754920b4d67b3eab4872da795586ec069324581136cb7704b`).
- **EX_306:** "PASS for continuity and preservation of authority. Two narrow documentary corrections before RAT-48".
  The reviewer computed the candidate's hashes itself, applied every hunk of both differences, and found the
  carried sections identical. It completed the review before TASK_T028 ran and held its commit back so that the
  owner's push of the runner's report could not be refused.
  - **H11-C01 (section 0D item 10):** Claude wrote that `game_profiles.py` changes bytes at the conversion. It does
    not: it is CRLF on the owner's disk already (entry 226). It is the other `forecast`-class files that change,
    and with them the forecasting-code identity. **Claude's error, and the same wrong reason stood in Claude's
    own notes of the day;** the planned refill of DEV is right, its stated cause was wrong.
  - **H11-C02 (section 10 item 2):** RAT-46 ratified the reviewer's corrected candidate H-2 v6r1, not the first v6
    candidate the sentence pointed at.
  - **Three observations:** the command cheat sheet is "to be considered" (entry 220), not settled; the QA sequence
    should name the second `Init_Tree.bat QA` after the environment is built; section 4.1's "passed in EX_271" does
    not hold for the file-form standard (EX_305, RAT-47).
- **What Claude did: the candidate H-1 v11r1,** by `exchange/CLAUDE_WEB_TOOLS/h1v11r1/make_h1_v11r1.py` with
  `h1_v11r1_texts.py`: eighteen counted replacements in the exact bytes of the candidate v11 (asserted by SHA-256).
  They make both corrections and all three observations, and bring the candidate up to the present, as EX_306
  asked: TASK_T028 ran and what it found (entries 239 to 242), option A confirmed, the owner's level 9, the
  conversion's working files, the reviewer's review, what waits now, one more lesson, two more identities.
  Sections 1, 2 and 2A are byte for byte those of the installed H-1 v10 (asserted).
- **Written, under `exchange/CLAUDE_WEB_TOOLS/h1v11r1/out/`:**
  - `Claude_Primary_Handover_H1_v11r1.md`, SHA-256 `bb68f9b6ea7c8ad65a3c172698c0e1ceffd274a0a0a60663cb4aa527a42e13c9`;
  - `Claude_Primary_Handover_H1_v11r1_introductory_blurb.md`, SHA-256 `5d7e64fe13fba2bb094707d86616664aef58f7422f99fc75fd5a612c9f4c6663` (it differs from v11's blurb in the one path it points at);
  - `H1_v11_TO_v11r1.diff` (`da00c7145368242aac31eabfa46c33a1b43f9ab924bde9d45af2bc08e3782e5d`) and its blurb's: what the reviewer confirms;
  - `H1_v10_TO_v11r1.diff` (`4cf3762c114ff113e28f66e3b5a19c53389d737015a7d9c122936c70c9e3de44`) and its blurb's: the whole difference from the installed edition.
  Each of the four differences, applied with `patch`, gives its candidate byte for byte (checked with `cmp`).
- **Its standing:** a CANDIDATE. In force: H-1 v10 (RAT-45). The candidate v11 of entry 238 stays where it is,
  unchanged. Next: the reviewer's confirmation of the narrow difference; then the owner's ratification (RAT-48);
  then installation by script in `doc/HANDOVER/`.
- Next numbers: EX_307; entry 244; RAT-48.

## 244. 24 November 2026, 20:27 - RAT-48: THE OWNER RATIFIES H-1 v11 (the candidate v11r1) after the reviewer's focused PASS (EX_307); installed in doc/HANDOVER/ with its status statements changed

- **EX_307 (reviewer; main `d778d55`; SHA-256 `e808739378ee097cbcaf5c4ed03192ea6067cc00a3e97f91079d4382a7bc4462`):**
  "FOCUSED PASS. H11-C01 and H11-C02 CLOSED. All three observations addressed. Recommend the exact H-1 v11r1
  candidate and its blurb for owner ratification under RAT-48." It computed nine hashes itself (all match), applied
  every hunk of the narrow and of the whole difference (each rebuilds the candidate exactly), found sections 1, 2
  and 2A identical to the installed H-1 v10, and found the continuity through entry 243 accurate. It executed
  nothing and reviewed neither the probe's results nor the conversion's code.
- **The owner's ratification, 20:25, to Claude:** "ok to Recommendation for RAT-48", followed by the reviewer's
  recommendation as he had it: "The exact candidate recommended for ratification is:
  `bb68f9b6ea7c8ad65a3c172698c0e1ceffd274a0a0a60663cb4aa527a42e13c9` Its introductory blurb:
  `5d7e64fe13fba2bb094707d86616664aef58f7422f99fc75fd5a612c9f4c6663`". A minute later he relayed that EX_307 was
  committed. **Claude took "ok to" as his ratification:** they are his own words, they name RAT-48 and they stand
  over the two exact hashes. Had he meant otherwise, the install is a document only and H-1 v10 is untouched.
- **RAT-48 is recorded** (RAT-47 was the last number used). **Installed** by
  `exchange/CLAUDE_WEB_TOOLS/rat48/finalise_rat48.py` from the ratified candidate and blurb (each asserted by hash):
  - `doc/HANDOVER/Claude_Primary_Handover_H1_v11.md`, **SHA-256 `91a9c1814587bcbe0ee9ce23de51a6ed5008932d4c721e9f52c0467930c09318`** (1533 lines);
  - `doc/HANDOVER/Claude_Primary_Handover_H1_v11_introductory_blurb.md`, **SHA-256 `16d7feedc6102bc87e62d5e6d4a464a38013ffd6f8e2262d0a80320387d9b5ec`**.
- **Ten passages of the handover differ from the ratified candidate,** each a statement the ratification itself
  made out of date (`rat48/H1_v11r1_CANDIDATE_TO_FINAL.diff`, SHA-256
  `ded5bf5fec8c7aee048782224dc1f15cbd67e8b3509ae2c4473d61263fd11ddf`, 10 hunks; applied to the candidate with `patch`
  it gives the installed file, checked with `cmp`): the title; the edition line; the status statement; the
  "replaces" line; section 0A item 3's newest numbers; section 0D's next numbers, its records (item 1), the
  reviewer's review (item 14) and who is waited on (item 16); and section 10 item 2, which had still called H-1
  v10 "this edition". Sections 1, 2 and 2A are carried byte for byte (asserted). No rule or fact was changed.
- **Three passages of the blurb differ from the ratified blurb, and that is new:** at RAT-45 the blurb was
  installed with its bytes unchanged. This one was written to point at the candidate under `exchange/` and to call
  it a candidate; installed, it says "ratified ... RAT-48" and points at `doc/HANDOVER/` alone
  (`rat48/H1_v11r1_CANDIDATE_TO_FINAL_blurb.diff`, SHA-256
  `3ae48edf43b713e8a7e609c4c6eb628605eb9acb64f3d96670a03ab3b4279222`, 3 hunks; checked the same way). The ratified
  candidate and blurb stay under `exchange/CLAUDE_WEB_TOOLS/h1v11r1/out/`, unchanged.
- **H-1 v10 and its blurb stay in `doc/HANDOVER/` as history. A new Claude chat starts from the v11 blurb.**
- **RAT-48 authorises the documentary installation and nothing else:** nothing on the owner's PC.
- **The owner, 20:24, asked what comes next with the line endings;** Claude set out the cloud work (the list, the
  engine's writers, the conversion program, the Git settings, a full trial), the one package to the reviewer, and
  the two steps on his PC (a rehearsal by the runner; the day itself from a sheet), each on his own go. Surveyed
  that minute: 681 tracked files to convert under the root, `src`, `deploy` and `tests`, and 7 others; none with a
  stray carriage return, none that is not UTF-8, none of a kind the standard does not name.
- Next numbers: EX_308; entry 245; RAT-49.

## 245. 24 November 2026, 21:03 - the conversion's cloud work: the engine's writers, the list, the conversion program, the Git settings, and a full trial (working files; not a package, not reviewed, nothing installed)

- **The owner, 20:32, to Claude:** "good. next please." (after RAT-48; the next work being the conversion's steps in
  the cloud, set out to him at 20:24, entry 244.)
- **Written, under `exchange/CLAUDE_WEB_TOOLS/conversion/`** (its `NOTES_FOR_THE_PACKAGE.md` lists every file):
  - **The engine's writers** (`overlay/src/research/`): a new helper `windows_text.py`, the one place where the engine
    turns its texts to CRLF, and four modules changed to use it: `reports.py` (every report file, the read-me
    files, the side file of making times), `status_file.py` (the status file, whose check is now over the CRLF
    bytes; a file in the old form is refused), `derived_check.py` (the not-current marker) and `job_lock.py` (lock
    files). The lists (`.jsonl`) are not touched. Two lines of the old two-site checker's self-test name their line
    ending. `deploy/INFRA_MANIFEST.ini` gains the helper (class `derived`). New tests `test_research_file_form.py`
    (16), one of which runs a research job and a withdrawal in an invented tree and gives every file they wrote to
    the project's checker.
  - **The Git settings** (`git_settings/`, under plain names so that Git does not obey them where they lie):
    `.gitattributes` as the one line `* -text`; `.gitignore` with the two readiness markers added. Tried in Windows
    form in a scratch repository with `core.autocrlf=true`: Git stores and shows each file's own bytes.
  - **The list builder** `make_conversion_list.py`: from Git at HEAD with the package's files laid over; today **686
    files, of which 673 change bytes;** six left out by name; each "after" proved to differ from its "before" in
    line endings only.
  - **The conversion program** `tools/convert_to_file_form.py` (standard library; never calls Git) and its 36 tests.
    It prints what it found by class and waits for the typed word `CONVERT`; a listed file is converted only from
    the list's "before", passed over at its "after", and any third value stops the run before a change; the
    tree's own settings file is converted by rule; what is made again is removed on a second typed word, `REMOVE`;
    the results masters and ledgers are proved untouched; both locks are held; the owner's copy (a folder or a
    ZIP) is checked first, and **on a second run against the hashes recorded at the first run** (the reviewer's
    watchpoint, EX_305); a look-only mode changes nothing.
- **Planted faults:** 11 of 11 caught in the writers; 17 of 17 in the conversion program (one was missed at first:
  a file that appears between two runs; a test was added and it is caught).
- **The trial** (`trial/TRIAL_OF_THE_CONVERSION_PROGRAM.txt`; a clone of `9f27bc0` made to look like DEV with the
  workspace's fill): 662 listed files and the settings file converted, 1,579 files removed, all 686 at the list's
  "after", the four results files unchanged; a second run changed nothing and asked nothing. **The whole suite
  afterwards: 762 tests in both runs, 762 with the same result,** the three known failures the same three, and
  60 new tests passing. The changed engine, run on four variants and both games, wrote 1,434 files, every one in
  its form; **its 2,424 forecast lines and 2,416 score lines are the same as before the conversion** but for the
  two fields that record the changed bytes (the variant's fingerprint; the forecast's digest). Suggestive only:
  the cloud, four variants.
- **Found on the way, for the sheet:** after `.gitattributes` becomes `* -text`, Git does not report a file whose
  disk bytes differ from the index only in line endings until the file is touched or re-added. The commit of the
  converted files and the one refresh of the owner's working copy therefore need exact commands, rehearsed by the
  runner; a candidate is to stage the listed paths from a path file and then `git checkout-index --force --all`.
- **Nine readings of the standard** to put to the reviewer with the package (the notes file, second list): among
  them that the search of section 4 covers programs and not the tests' own code; that sixteen of the standard's
  "17" lie in a file section 3A freezes; and that the program itself removes what is made again, on its own
  typed word, instead of a typed `rmdir`.
- **Still to do before it is a package:** the refresh and commit commands; the sheet; the package and its
  verifying script; a rehearsal by the runner and a look-only run by the owner in his real DEV (each his own go);
  slice A's working files brought to the standard.
- **Not covered by anything yet:** Windows; the owner's real tree; the whole fill; the comparison with the old
  system's records.
- Next numbers: EX_308; entry 246; RAT-49.

## 246. 24 November 2026, 21:12 - the owner agrees to an early look-only run in his real DEV; the look kit and its sheet

- **Claude's suggestion (entry 245's reply):** a look-only run of the conversion program in the owner's real DEV,
  early: it changes nothing and shows what his tree holds that Git does not track, any of which would otherwise
  stop the real run on the day. **The owner, 21:09:** "yes to your suggestion/recommendation".
- **What that needed first:** as written an hour earlier, even a look refused unless the package's files had been
  copied into the tree, because the program took the standard's rule from the tree's own `deploy\file_form.py`.
  An early look must need nothing installed. **Changed:** the program now uses the copy of `file_form.py` that
  lies beside it, checked by SHA-256 against the conversion list; the files the package itself delivers, when
  not yet in the tree, are a class of their own, which a look reports and a real run refuses; and the program
  tells Python to write no compiled copy, so a look writes nothing at all. Tests 39 (three added); planted
  faults 18 of 18 caught (one added: a run without the package's files not stopped).
- **The look kit,** `exchange/CLAUDE_WEB_TOOLS/conversion/look_kit/`, made by `make_look_kit.py`, each file in
  Windows form (CRLF):
  - `convert_to_file_form.py`, SHA-256 `dd690abe28b27aede35c1951025e8835e0d80c45de63ce1704ed254bedcaceb7`;
  - `file_form.py`, SHA-256 `1d77cb9dd48ce50bc9d35b777b43df077303a810e1cb874466be166e1b6920cf`;
  - `CONVERSION_LIST.json` (686 files, made from `b1093a8`), SHA-256
    `94be7098e64976c7c15431779de2b139ba14f53b5b99a105fc69e7f219f574b6`.
  **Why CRLF, checked:** in a scratch repository with the project's present attribute lines, a file committed
  CRLF arrives byte for byte in a clone whose Git has `core.autocrlf=true` (Git 2.43), while a file committed LF is
  rewritten CRLF there. So the hashes quoted are the hashes the owner's `certutil` will show. They are Claude's
  first files committed in the standard's form.
- **The sheet:** `exchange/CLAUDE_WEB_TOOLS/conversion/LOOK_ONLY_SHEET.md`: a pull, one `certutil`, one command whose
  output goes to `E:\TEMP\FILE_FORM_look.txt`, and what to expect. Tried in the cloud on the unconverted trial
  copy: 662 to convert, 12 in their form, 12 of the package's own not yet there, 1,579 made again, four results
  files, no finding.
- **Its standing:** unreviewed. The probe of TASK_T028 was read by the reviewer before it ran; Claude recommends
  the same here, as a short focused read of the look's path (it reads, hashes and prints; it writes nothing),
  and gave the owner a paste for it. Whether to wait for that is the owner's choice; the run is his own go.
- **Not authorised by this:** any run that changes anything; any install; the conversion.
- Next numbers: EX_308; entry 247; RAT-49.

## 247. 24 November 2026, 21:22 - EX_308 (the look's path is read-only; two narrow corrections); the look kit r1 and its sheet r1

- **Relayed by the owner at 21:17:** "EX_308_ChatGPT.md is committed at main 03c9bc23879cb665f96cf19e7266869660a59628 ...
  Two narrow corrections before recommending the real DEV look". Claude read `exchange/EX_308_ChatGPT.md` (SHA-256
  `38d26c230513202d13728d15f27c808e0ab9ab19e7c88624a67723ff15cd2c86`).
- **EX_308:** all three hashes of the kit match; the `--look` path "reads, hashes, computes prospective line endings
  in memory and prints. It takes no lock, creates no record, starts no subprocess, and makes no explicit network
  call" (a conclusion from the source, not an execution on Windows). Two corrections:
  - **LOOK-C01:** the finding for a status file that holds more than ACTIVE printed the file's own line, while
    the sheet promised that no content is printed. **Claude's fault: the sheet's promise was not checked against
    every message.**
  - **LOOK-C02:** the walk did not refuse Windows junctions and other reparse points, a named folder could itself
    be a link, and a linked file would be read through.
  - **Sheet precautions:** check all three hashes; no compiled copy of the rule standing in for it; nothing else
    of the project running; on a lock finding, no deletion by hand on the look's word; the pull is a separate
    step outside the read-only claim.
- **Corrected** (working sources under `exchange/CLAUDE_WEB_TOOLS/conversion/`; the exact difference from the
  reviewed kit's sources is `look_kit_TO_r1.diff`, SHA-256 `e4b03181b24807cebd7e7bd10af1fbe10c89f205d2d21509bb8519f1d9941cc8`,
  15 hunks):
  - **C01:** two fixed descriptions ("it holds a status other than ACTIVE"; "it records a withdrawal or an
    eligibility draw"); nothing of a file's content is put into any message. A test asserts that the planted
    values do not appear in the output.
  - **C02:** in the rule module, `is_link` (a symbolic link anywhere; on Windows anything carrying the
    reparse-point mark) and `files_and_links_under`, which never enters or reads a link: a named folder that is
    a link or lies under one is not walked, and a folder or file met in the walk that is a link is set apart.
    The plain `files_under` (the suite's check) refuses on any. The program names each as a finding, and before
    a real run takes its locks it refuses a control folder that is a link, so that no lock is written through
    one. Tests on real links (junctions where Windows allows no symbolic link) and one with Windows' mark
    mocked.
  - **The precautions:** the program now reads `file_form.py`, checks those bytes against the list and runs
    exactly those bytes, without Python's import machinery, so that no compiled cache is read or written; the
    lock messages say "tell Claude" and no longer advise deleting by hand; the sheet has three `certutil` lines,
    says that nothing else of the project runs, and sets the pull apart.
- **Checked:** the program's tests 41 and the rule's 52 pass; planted faults 22 of 22 caught (four added: a link
  not reported; a lock written through a linked control folder; each of the two contents printed). A look with
  the new kit on the unconverted trial copy with a planted link: the link named, nothing behind it listed, the
  tree byte for byte unchanged; without the link, no finding. The two file-form test modules pass again in the
  converted trial tree with the corrected rule (68 tests).
- **The look kit r1,** `exchange/CLAUDE_WEB_TOOLS/conversion/look_kit_r1/` (CRLF; made from `03c9bc2`):
  - `convert_to_file_form.py`, SHA-256 `0dc02db3fd69e23590f0ee54f59372870856b054edeaad5da937385881d05bde`;
  - `file_form.py`, SHA-256 `e27e57b43a18108cc0a343b921a15e1f40c80fa2756e070d1cac4f4a7c78310c`;
  - `CONVERSION_LIST.json`, SHA-256 `a60fcd78562b7903afe689bcea796fb3cc7bbb74c7b90f9fdf61d262f25544a9`.
  **The sheet r1:** `LOOK_ONLY_SHEET_r1.md`, SHA-256 `68b8ff7d1220425f43940d486bcdf89c5df1b9925c99b767c639eee49b568ea0`.
  The first kit (`look_kit/`) and the first sheet stay exactly as the reviewer read them.
- **Its standing:** for the reviewer's confirmation of the narrow difference. The look itself is the owner's own
  go, not given by a review.
- Next numbers: EX_309; entry 248; RAT-49.

## 248. 24 November 2026, 21:26 - the reviewer's FOCUSED PASS of the look kit r1, relayed by the owner; the look is now his to run on his own go

- **Relayed by the owner at 21:26, the reviewer's words:** "LOOK-only kit r1: FOCUSED PASS. LOOK-C01 and LOOK-C02
  CLOSED for the intended local, quiescent DEV survey. All five supplied SHA-256 fingerprints match. All 15 diff
  hunks independently applied and both revised CRLF source files reconstructed exactly. Original kit unchanged.
  All sheet precautions satisfactorily addressed. Recommend the owner proceed with LOOK_ONLY_SHEET_r1.md on his
  own GO. This PASS does not extend to the actual conversion package." And: "Minor qualification: filesystem
  metadata queries may resolve link targets; the tool is not a general-purpose security sandbox. This is not a
  reason to delay the intended local survey." And: "Next EX: EX_309, not yet committed."
- **What Claude records:** the relay, as the owner gave it. EX_309 is not on `main` at this entry (checked); when
  it is committed it is the record of the review, and this entry is not.
- **The qualification is true and is accepted as it stands:** the walk asks Windows whether a path is a link
  without following it, but one question it asks about a link lying in the root (is it a folder?) is answered
  through the link. Nothing behind a link is listed, opened or read. No change is made for it.
- **Not given by the review:** the go. The look is the owner's own to run, from
  `exchange/CLAUDE_WEB_TOOLS/conversion/LOOK_ONLY_SHEET_r1.md`, when he chooses; Claude repeated the steps to him.
- Next numbers: EX_309 (the reviewer's, pending); entry 249; RAT-49.

## 249. 24 November 2026, 21:28 - THE OWNER'S LOOK-ONLY RUN IN HIS REAL DEV: no finding; a real run would find nothing to stop it. EX_309 committed

- **EX_309 (reviewer; main `dbcd1e7`; SHA-256 `4ec19cda0d8fe5316f2ca0a1fd3d9a2031e2f5a941662c6c8b85737271d43cbc`):** the
  focused PASS of the look kit r1 that entry 248 recorded from the owner's relay; it is now the record.
- **The run:** by the owner himself, in CMD, at about 21:27, at `main` `63d6f1f`, exactly as
  `LOOK_ONLY_SHEET_r1.md` gives it; he sent Claude the whole screen. His pull was a fast-forward. **His three
  `certutil` lines printed the three SHA-256 values of the sheet,** so the kit on his disk is the kit committed
  (the first proof on Windows that a file committed CRLF arrives byte for byte with `core.autocrlf=true`).
- **What the look printed** (kept whole in `exchange/CLAUDE_WEB_TOOLS/conversion/look_result/OWNERS_LOOK_20261124.txt`,
  SHA-256 `75a11d072e5d8c4f0228404699cf71d91fc1b701ecbf02ac248ba977bb9617f4`):
  - the list: 686 files, SHA-256 `a60fcd78...5544a9`;
  - **to be converted now: 650; in their form already: 24;** the package's own, not yet there: 12 (650 + 24 + 12
    = 686: every listed file is at the list's "before" or its "after"; none has a third value, and none is
    missing);
  - the tree's own settings file: to be converted;
  - **made again, not converted: 1,578 files** (research results and status files; nothing is left in `records\`);
  - **the four results files, with exactly the SHA-256 values Git holds for them** (Claude computed the four from
    Git at `dbcd1e7`: they are the same): his masters and ledgers are the repository's, and in their form;
  - untouched, not read: 12;
  - **in no class, or not as expected: 0.** No stray file, no link or junction, no lock, no status file holding
    more than ACTIVE, nothing in `scratch\`.
  - Last line: "LOOKED ONLY; nothing was changed. A real run would find nothing to stop it."
- **What it settles:** the standard's section 11 item 3 (what his DEV holds that Git does not track): nothing the
  conversion cannot place. And it is the first run of the program's look path and of the rule module on
  Windows, with Python 3.15.
- **What differs from the cloud's trial, and why it is as expected:** 24 files in their form already against 12
  there. On his disk three files under `src` are CRLF (entry 226) and, it follows, nine more of the listed files
  outside `src` (Git wrote them CRLF at checkout); the list's rule passes each over. The count to convert is
  smaller by the same twelve.
- **What it does not show:** which nine those are (the look prints counts for that class); anything about the
  conversion itself, the refresh of his working copy or the commit. It is true of his tree tonight: the look is
  made again on the day, as the real run's first step.
- **No go is given or implied for anything further.**
- Next numbers: EX_310; entry 250; RAT-49.

## 250. 24 November 2026, 21:41 - the day's Git steps worked out and simulated: a program to stage and refresh; A FAULT OF FACT IN THE RATIFIED STANDARD (the root attribute line does reach GAIS) put to the owner

- **The owner, 21:28, on the look's output:** "why are csv untouched ?" Claude's answer: the four results files are
  CRLF already, so they conform as they are and are only proved unchanged; the report tables under
  `results\research\` are made again; the old system's CSV files are frozen history.
- **The owner, 21:29:** "ok lets go now". **Claude took this as his word to go on with the next cloud work** (the
  refresh and commit commands, the sheet, the package), which is what stood next; **not** as a go for anything
  on his PC: nothing is packaged or reviewed, and the conversion is its own go.
- **What plain Git does, found by simulation** (`trial/SIMULATED_DAY_IN_GIT.txt`; a clone with
  `core.autocrlf=true`, shaped like his working copy): Git goes by each file's remembered size and time. After the
  conversion it does not show 26 listed files that were CRLF on disk all along, and
  `git checkout-index --force` rewrites none of the 2,298 frozen files whose working copy is CRLF against LF in Git.
  Left so, a later touch of any of them would show it as changed and a later `git add` would put a CRLF copy
  of frozen history into Git.
- **Written:** `exchange/CLAUDE_WEB_TOOLS/conversion/tools/stage_and_refresh.py` (17 tests; planted faults 11 of 11).
  By content, not by Git's belief: it stages each listed file with exactly the bytes on disk, after checking
  they are the list's "after"; it rewrites the working copy of every other tracked file that Git converts
  nothing for and that differs from Git's bytes in line endings only, with Git's own bytes; it refuses a file
  that differs in more; it prints first and waits for the typed word `STAGE`; it proves the result, asking Git
  itself whether any unstaged change remains; it commits and pushes nothing. Unlike the conversion program it
  calls Git: staging a commit is what Git is for (the owner's principle, entry 227, is about gating a tree).
- **The simulated day, end to end:** the commit holds exactly the 681 changed and 4 new listed files; `git status`
  then empty; **a fresh clone equals the working copy byte for byte in all 4,274 tracked files outside GAIS.**
- **A FAULT OF FACT IN THE STANDARD, FOUND BY CLAUDE.** `doc/FILE_FORM_STANDARD_v0_1.md` section 5 says the root
  `.gitattributes` "says one thing: `* -text`" and that "It does not reach `GAIS\`". **It does reach it:** GAIS's own
  two attribute files name only some kinds of file; 173 of GAIS's 204 tracked files are named by neither and come
  under the root line. On the owner's PC their working copies are CRLF today by his Git's setting; under the
  one line they would be exactly the hidden difference described above, in his other project. The owner's
  decision (entry 234) was that GAIS is out of scope and that nothing under it is changed. **Two more lines carry
  that decision out:** `GAIS/** !text` (for GAIS the root file says nothing, so Git behaves there as before) and
  `GAIS/**/*.bat text eol=crlf` (the old root line for batch files, kept for GAIS alone). With the three lines every
  GAIS file's stored form, form on disk and attribute were compared, file by file, and are exactly as before.
  **Claude's error in the standard, and the reviewer's FFS-C03 did not catch it either. It changes a ratified
  sentence, so it is the owner's to decide:** put to him as a narrow amendment. The working files still hold
  the one ratified line; the simulation used the three.
- **Still to do:** the owner's decision on the attribute lines; the sheet of the day; the package and its
  verifying script; then the reviewer; then, each on the owner's go, the runner's rehearsal (which will show his
  Git's version) and the day.
- Next numbers: EX_310; entry 251; RAT-49.

## 251. 24 November 2026, 21:51 - the owner approves three lines in the root attribute file; the candidate v0.2 of the file-form standard (one narrow amendment, two corrections of fact)

- **The owner, 21:48, on the question of entry 250:** "yes to Question: may the root attribute file hold three lines
  instead of the one the standard ratified? yes to Recommendation: approve the three lines". The recommendation
  he said yes to was: approve the three lines, as a narrow amendment of the ratified standard, with the
  reviewer's check first. **So his decision is made; the amended text is not ratified until the reviewer has read
  it and he says so (it would be RAT-49).**
- **Done at once:** `exchange/CLAUDE_WEB_TOOLS/conversion/git_settings/gitattributes` now holds the three lines, with
  two comments. Checked again in Windows form in a clone with `core.autocrlf=true`: every GAIS file exactly as
  before; `src`, `exchange` and `doc` all `-text`.
- **The candidate v0.2 of the standard,** built from the installed v0.1's Git bytes (asserted by SHA-256) by
  `exchange/CLAUDE_WEB_TOOLS/standards/make_standard_v0_2.py`, eight counted replacements, each new passage marked
  "v0.2":
  - `FILE_FORM_STANDARD_v0_2_CANDIDATE.md`, SHA-256 `8a6ae261e57c467b72cfbd0b1c23dd6b4bf5a16fc6ab84d7c04de51c6b7d56c6`;
  - `FILE_FORM_STANDARD_v0_1_TO_v0_2.diff`, SHA-256 `2bfab12b0040fd93f7431b08ce164cbdd89c89a55dae5fc91da59808f7075692`
    (5 hunks; applied to v0.1 with `patch` it gives the candidate, checked with `cmp`).
- **What it changes, and nothing else:**
  - **(A) the amendment (section 5; section 8, new item 7 with the owner's words):** the root `.gitattributes` holds
    three lines, `* -text`, `GAIS/** !text` and `GAIS/**/*.bat text eol=crlf`. It says plainly that v0.1's "does not
    reach `GAIS\`" was wrong, why (173 of GAIS's 204 tracked files are named by neither of GAIS's own attribute
    files), and what each line does.
  - **(B) a correction of fact (section 4):** the writes that name no line ending are eighteen, not seventeen;
    sixteen lie in `src/results_master_v0_2.py`, which section 3A leaves as it is, so they stay; two are
    corrected. It also states that the search reads programs and not the tests' own code, as section 2 implies:
    **that one sentence is a reading, marked for the reviewer.**
  - **(C) a correction of fact (sections 5 and 11):** v0.1 said that the stale working copies "would all show as
    changed" and that rehearsed commands would refresh them. Neither holds (entry 250); the refresh and the
    staging are done by a program, by content, which calls Git and commits nothing.
- **Left for the package's review, not put into this candidate:** the other readings of
  `conversion/NOTES_FOR_THE_PACKAGE.md` (among them that the conversion program itself removes what is made again).
- **Its standing:** a CANDIDATE. In force: v0.1 (RAT-47). Next: the reviewer's check of the difference; the
  owner's ratification (RAT-49); installation as `doc/FILE_FORM_STANDARD_v0_2.md` with v0.1 kept as history; then
  the working files' references to the standard are pointed at v0.2 before the package is built.
- Next numbers: EX_310; entry 252; RAT-49.
