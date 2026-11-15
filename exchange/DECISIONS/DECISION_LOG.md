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
