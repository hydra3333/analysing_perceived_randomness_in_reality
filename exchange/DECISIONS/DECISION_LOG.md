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
