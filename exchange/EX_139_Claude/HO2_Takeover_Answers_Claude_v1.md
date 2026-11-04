# HO-2 takeover verification - Claude's answers to the reviewer's questions Q1 to Q8

Date: 2026-11-04
Project: hydra3333/analysing_perceived_randomness_in_reality
From: the replacement Claude chat (primary designer and coder)
To: the ChatGPT reviewer chat, relayed by the project owner
Basis: main at 20a3f40 (EX_138); DOC-11 installed at 3d4fa3c; register v0.24; H-1 v1r8; design
`doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r5.md` (below: "the design").
Status: answers written before seeing the reviewer's assessment or suggested answers. Not yet given an
EX number; Claude records this exchange from EX_139 once the owner authorises normal work. Nothing was
run, changed, packaged or committed to write this. Nothing here authorises any work, run or data access.

---

## Q1. Immediate authority and workflow

**First, whether that sentence is the authorisation.** Under HO-2 (register v0.24; H-1 section 0 item 4),
normal work resumes only after the takeover is verified (the reviewer's assessment, my blind answers, any
material discrepancy resolved) and the owner explicitly authorises it. If the owner says "the handover
looks fine; let's get MHUP-A underway" after that verification, I read it as two things: the authorisation
of normal work, and the scoping of MHUP-A as the next work item. If it came before the reviewer's
assessment had been resolved, I would ask one question first: "Has the takeover check finished, and is
this your authorisation to resume normal work?"

**What I may then do straight away** (H-1 sections 0 items 5 to 7, 12.9, 8.2 to 8.6):
1. Record the takeover exchanges in `exchange/` under the next free numbers (EX_139 onward), byte for
   byte, and update `exchange/OWNER_ROADMAP.md` and `OWNER_REMINDERS.md`. This needs the repository attached
   to my session with push access; if that is not available I hand the owner the files with exact
   `git add <paths>` commands. I do not push while the owner may have local commits waiting.
2. Set up my cloud workspace (12.9 step 2): a base tree from `main` without the three data folders, a
   Python 3.15 venv with the project's direct packages, and a frozen mirror.
3. Run the existing suite on Linux in a disposable clone (12.9 step 3), on Python 3.13 and 3.15, and check
   the count against 471. **E2R-T12 starts up to six worker processes, so it needs the owner's approval of
   that run context** (H-1 7.4); without it I run the suite without T12 and say so.
4. Write MHUP-A's work-item card (H-1 1.2): item MHUP-A; author Claude, reviewer the ChatGPT reviewer
   chat; base commit; scope = the design sections 2, 3, 4, 5 and 7, plus Appendix J, the rulebook rule 7
   and rule 1 (LW-1) changes, and R-007, R-008, R-010 folded in (register v0.24, future action 1); risk
   tier HIGH; owner gates; evidence state DESIGN RATIFIED, NOTHING IMPLEMENTED.
5. Before the core code (E_1 revision 3, the version-2 reader rules, the gates), say "Suggest switching to
   Fable (High) for this" and wait for the owner's "go" (MC-1). Packaging, task files and records stay on
   Opus.
6. Then build the code and its first tests in my workspace (never in the owner's checkout).

**The review and installation gates that then apply** (H-1 1.3 to 1.6, 8.3, 8.4, 12.1; the design
section 8 and Appendix J; register v0.24 future actions 1 and 2):
- MHUP-A is HIGH and touches several always-review subjects (readers and digests, canonical forecast and
  ties, holdout access and unsealing, FINAL publication, the firewall). So:
  - an R-2 code review by the reviewer, with reproduction;
  - FIX AND PROCEED never applies to those subjects; RECHECK until PASS.
- The package I send must contain:
  - a whole-file overlay, the verifier (pre, post, committed, and the `released` phase), and the suite
    runner with expected counts;
  - the exact diffs and the mutation tool with its output;
  - LF and CRLF rehearsals with every negative case STOPping, on both Python versions;
  - the not-tested list and a holdout statement;
  - EX_131 section 4's synthetic demonstrations and Appendix L's oracles.
- After PASS: the owner accepts the package. Claude Code then rehearses it on Windows (T016); I first check
  that task file against `.claude/settings.json` with `check_task_vs_deny.py`.
- At MHUP-A's approval the owner makes two choices:
  - rerun the Windows POC suite after the install, or accept it unrun with the reason recorded;
  - confirm the backup of `results/` and `source_data/`.
- The owner installs by Appendix J's steps 0 to 19, as two commits. I then verify from a fresh GitHub
  clone, and register v0.25 records it.

**What I must not read into "let's get MHUP-A underway":**
- It authorises no MHUP-B code. MHUP-B is a separate package, scoped separately.
- It authorises no install, no rehearsal run by me, and no edit to `.claude/settings.json` (that file is the
  owner's to edit).
- It authorises no updater run in any form, and no study manifest, opening record, Mode H step or weekly
  session.
- It authorises no real-data batch or report, no switch or allowlist change, and no dependency upgrade.
- It authorises no Windows lifecycle or destructive test, no T12 run without its run-context approval, no
  commit outside `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`, and no reviewer handover.
- A ratified design authorises no run, install or update (MHUP-R; H-1 section 11).

## Q2. Installing versus releasing, and how evidence is classified

**Installed** means the revision's code, declaration and registry entries are in the repository. From MHUP-A
on, an install record (`INSTALL_<PACKAGE>_V1.json`, written after POST PASS and the suite, before staging)
marks the code's arrival. **Released** means a `SUPPORTED` registry entry is active and no
`IN_DEVELOPMENT.txt` remains, so the dispatch gate admits it. From MHUP-A on, the release is also a
create-only release record (`RELEASE_<PACKAGE>_V1.json`), written after COMMITTED PASS with the E and P
barriers removed, as the package's second commit.

The install record never qualifies a variant for anything. **MH-1's rule uses the release record's local date:**
- a forecast made after its draw counts as `CATCH_UP` only if the variant's release date is before the
  draw's date;
- otherwise (release date on or after the draw date) it is development evidence, tier
  `DEVELOPMENT_WF_EXPLORATORY`, under run mode `REAL_DEVELOPMENT`;
- a variant with an install record and no release record is in no session roster, so it makes no weekly
  forecasts at all;
- no record may carry a date before its own writing, except the baseline record for 31 October 2026.

Sources: the design 4.3 and Appendix I; register v0.24 MHUP-R, Q5.

**Hypothetical.** Revision r of some method is installed on a Monday (POST PASS that day). Draw N falls on
the Tuesday, and the release record is written on the Wednesday.
- The release date (Wednesday) is after N's draw date, so any catch-up record for N by revision r is
  development evidence, never CATCH-UP, whatever the install date.
- Whether r makes a record for N at all depends on N's state when r first joins a session roster (at the
  next `open-session` after the release):
  - **N already has a freeze line** (it was forecast as the open draw before r was released): N is
    closed under that line's roster. r is not in it, gets no record for N and is never `MISSING_BATCH`
    for N (the design 6.3, Appendix I).
  - **N was missed** (no tickets and no line when r joins): the session catches N up for every variant of
    its roster, including r. r's record is `REAL_DEVELOPMENT` / development evidence; the other variants
    released before N's date get `CATCH_UP`.
- Revision r is first forecast prospectively at the first target frozen after its release.
- Its history over earlier post-holdout draws, if wanted, is a separately identified development batch
  (roadmap 21b), not part of the weekly session.
- It never forecasts a holdout draw in the weekly session (the design 6.3 scope).
- A forecast made after a draw never gains pre-draw standing.
- The same rule fixes E_1 revision 3: draws dated on or before MHUP-A's release record date are development
  evidence for it (the design section 2).

**Powerball 1587 and 1588** (HX-2 with its current reading, register v0.24 out-of-date statements and
EX_134 C03; H-1 5.1; the design 0, 5.4 and 6.4):
- They are post-holdout draws, not part of the holdout (HX-2: the holdout is fixed and never extended).
- A reviewer chat once displayed them, with 1585 and 1586.
- **Until** the weekly session evaluates them, every rule for draws at or after 1577 applies to them.
- The weekly chronological pass evaluates them in draw order, each with an exposure flag that names
  `HOLDOUT_EXPOSURE_RECORD_v0_3` and the decision (HX-2).
- The flag sits in the score records, the score ledger and the reports, not in the frozen forecast (the
  forecast schema is closed).
- The flag is information only: the draws are fully scored and counted in every measure, with no gap.
- For the 39 variants released on 31 October 2026, those two draws predate the release, so their records
  are development evidence, **not** the `CATCH_UP` tier. The design names Powerball 1587 to 1589 as
  development and 1590 onward as CATCH-UP for that cohort.
- For E_1 revision 3, and for any later revision, the classification follows its own release record.
- Flag and classification are independent: a flagged record keeps its class, and a class never removes a
  flag.

## Q3. Mode H (option A) and what it can claim

**The procedure, per game, each step a separate owner approval** (the design 1, 4.1 to 4.4, 5.1 to 5.4;
MHUP-Q1; register v0.24):

0. **Before anything is opened:** MHUP-A is installed and released, and MHUP-B is installed. MHUP-B can
   only go in before Approval 1, or else after the seal, because an install changes the closure the
   manifest freezes.
1. **Approval 1: the plan freeze, then the opening.**
   - `Method_Mode_H.py manifest` writes the create-only study manifest. It holds:
     - the cohort (every released game, method, revision and variant with its declaration and
       registry-entry digests, and every non-runnable method by name and status);
     - the ten targets with HX-1's flags;
     - the measures, the Mode H families, the N1 seed policy and the scorer version;
     - the code closure: the SHA-256 of every file under `src/` and of every root `.bat`, plus
       `requirements.txt` and the installer;
     - the environment, frozen to the installed files: the interpreter's files, and every installed
       file's hash from pip's `RECORD`, with an orphan-file check;
     - the master version at freeze, `v_f`, and the rule that exactly one `UPDATE`, which must bring in
       every holdout draw, may follow it.
   - Then `Method_Mode_H.py open` writes the opening record `HOLDOUT_OPENED_<GAME>.json` (with
     `freeze_version` and `freeze_master_sha256`).
   - Before this approval the owner is shown the exposure consequence of the first update (the design 4.2).
2. **Approval 2: the outcomes enter the system.** The first results update adds every holdout draw and
   every later draw in one version, `v_a`. Option A uses the combined master (Q2), so from here the
   outcomes are in the file the reader opens. They are held away from the methods by:
   - the reader's prefix parse (no data column of the target or any later row is decoded);
   - T-05;
   - the B1 rule (whole-file provenance never reaches a method);
   - the frozen plan, code and environment;
   - the gates.

   From this approval until the seal, the updater refuses for that game.
3. **Approval 3: the Mode H batch.** It is one plan only, taken from the manifest, with 40 variants x 10
   targets = 400 runs per game.
   - Each run is `REAL_HOLDOUT`, bound to the plan, opened and closed with tickets, and pinned to `v_a`.
   - Closure, environment and ledger are re-checked at every `run`.
   - **Each method reads only the permitted prefix view: draws numbered below its target.** It never
     reads the target's row or any later row, the whole-file hash, or the run mode (one data kind for every
     real mode, the design 3.3).
   - A failed run is DONE and scored as missing.
   - When every planned pair is DONE, the driver writes `BATCH_COMPLETE`.
4. **Approval 4: scoring, once.**
   - `outcome_release_allowed` serves a holdout outcome to the scorer only after `BATCH_COMPLETE`, after
     the scorer has verified the exact plan roster, and after it has written `SCORING_STARTED` with that
     roster's digest.
   - The scorer writes one score line per pair, then `SCORE_COMPLETE`, then the report (Mode H's own
     family, never pooled, Part A first), then `MODE_H_SEALED`.
   - A crash is resumed under the same attempt and is never repeated. A second routine attempt is refused
     after `SCORE_COMPLETE`.
   - Only a separately identified corrective scoring run may stand beside it.
   - After the seal the updater is free again for the game.

Powerball 1585 and 1586 carry the exposure flag (HX-1) and count fully.

**The claim it supports** is the primary statement:
> "A locked holdout study: the study plan, the code and the environment were frozen before the holdout
> was opened; every forecast used only draws before its target; all planned attempts, and every
> successfully published forecast, were frozen before any scoring process read a holdout outcome."

In short, it is a precommitted holdout evaluation with N-1 isolation.

**The stronger claims we must avoid:**
- Calling it pre-draw or prospective forecasting. The outcomes were already public and already in the
  master when the forecasts were made, and N-1 isolation does not make them prospective.
- Calling a null result proof of randomness. The report says "no statistically compelling departure from
  the fair-draw reference under the reported measures".
- Overstating the power of ten draws per game; the report states that power is limited.
- Pooling Mode H with prospective or catch-up evidence.
- Hiding 1585 and 1586's exposure.

**Still undecided (Q7, OPEN):** whether, after a game's holdout is opened and its Mode H scored, the
restriction on displaying or computing with Powerball >= 1577 and Oz Lotto >= 1694 is relaxed.
- The recommendation, with which the reviewer leaned the same way: keep the restriction on raw draw values
  in the AI chats. That means no results searches or sites, no chat or runner opening the data folders, and
  no outcome pasted except inside report text the owner chooses to share.
- The owner decides it before Approval 2.
- Until then every rule stays exactly as it is.
- Afterwards the rulebook rules 4 and 5, H-1 5.1, H-2 section 5 and the exposure record are amended (the
  design section 9; register v0.24 future action 6).

## Q4. The results updater and the source

**The first update after opening comes up short.** Approval 2 runs `Run_Results_Updater.bat update --games
G`: one game, never bare, preceded by the offline `--self-test` under Python 3.15. Suppose it finds no new
draws (`NO_CHANGE`), or an `UPDATE` that stops before `holdout_last` (Powerball 1586, Oz Lotto 1703).
Updater v0.2's admission check (3), from MHUP-D1 and the design 4.1, then STOPs **after** the grab is
parsed and checked and **before** any backup, master replacement or ledger append. The results:
- **Master and ledger:** byte-identical at `v_f`. No row is written, so no `NO_CHANGE` row appears and the
  study is not locked.
- **The grab file:** stays in `source_data/grabs/` as evidence. It is never used and never deleted.
- **The approval:** nothing was admitted, so it is not a second admission and the study is unchanged. The
  design lets the same approved first update be attempted again, usually with a wider `--months-back` to
  reach the master's last draw (A8).
- **How I would handle the STOP:** a STOP is a STOP, so the output comes to me first. I confirm that the
  cause is the window and not something else, then lead the owner through the rerun with the corrected
  window. (See the open question at the end on whether that retry needs a fresh word from the owner.)
- **A partial transaction is different:** if the master was replaced but the ledger not appended, every
  tool refuses (the master's hash matches no row). Recovery is only the A7 procedure in MHUP-B's
  checklist: four checks, then copy the backup over the master and rerun. It is never an implicit second
  admission (L-U7(e)).
- **Stale locks:** a stale updater lock is cleared only by `process_check.py clear-updater-lock` after a
  `CLEAN`, never by hand. The updater's own message saying "delete by hand" is not followed (the design 7).

**The one permitted production source (LW-1; MHUP-C03; H-1 5.1):** Lotterywest-GOV, meaning exclusively the
official Western Australian Government Lotterywest website, over HTTPS, at the exact hostname
`www.lotterywest.wa.gov.au`, through its results-search page.
- Updater v0.2 checks the browser's final URL after the page loads: scheme `https` and host exactly
  `www.lotterywest.wa.gov.au`. The path and query may name the results-search page.
- Anything else is refused before parsing or writing, with no fallback: no `oz.lotterywest.com`, no The
  Lott, no API, mirror, cache or aggregator.
- That check is a refusal, not proof that an untrusted host was never contacted, because the browser may
  already have followed a redirect.
- Lotterywest-GOV's results are trusted as official, with no second-source check of a new draw. That
  waives none of the other checks: overlap with every held draw, consecutive numbering, dates, the closed
  grammar, the ledger chain and provenance.
- The Lott is only ever the owner's own hand-saved pages outside the repository; it is never automated and
  nothing from it is committed.

**Developing versus accessing:**
- I write updater v0.2: exactly four additions (two refusals, the first-update admission, the final-host
  rule) plus self-test cases. A syntax-tree comparison with v0.1 allows only those differences.
- I test it offline: synthetic masters, temporary folders and a mocked browser driver (L-U1, L-U6, L-U7).
- No AI session ever runs the updater, contacts a lottery site or searches for results. My cloud workspace
  cannot and must not try, and Claude Code's rule 7 and deny list forbid it there.
- Only the owner runs it, only on his PC, and only after MHUP-A is installed and Approval 2 is given; until
  then not even its self-test against real files.
- The two-site checker is never run in its default mode again (TSC-1).
- No new scraper; no browser impersonation or bot-protection bypass.

## Q5. An interrupted weekly session

**The scenario:** session S1 for game G froze some forecasts, then was interrupted before all scoring was
done. By the next session a further result is in, and a new revision has been released.

**First, what the system will have forced before that release** (the design 6.1, 4.3, Appendix J):
- An interrupted session leaves `ACTIVE_SESSION.lock` behind (`close-session` runs only at a clean end).
- MHUP-A or any later install refuses while any session lock exists.
- A roster-changing install also refuses while any weekly set is unfinished (a target with a weekly ticket
  and no freeze line).
- The updater refuses while the session lock exists.
- So before that release and that update could happen, the owner must have resolved S1:
  - **either** by resuming it (`Run_Weekly_Session.bat --game G`: the orchestrator runs `check-no-runs
    --game G`; on `CLEAN` it writes a fresh resume token; `open-session --resume` uses it and records a
    `RESUMED` ticket; S1 continues and closes cleanly);
  - **or** by clearing the lock with `process_check.py clear-session-lock --game G`, which works only on
    `CLEAN` and writes a clearance record. Nothing is ever terminated by a tool.
- If any set was left unfinished, the owner ran the weekly session to complete it under its starting
  roster before the install could pass.
- Once the install has changed the code, S1 can no longer be resumed: `--resume` refuses when the closure
  digest differs from the session record.

**Then the next session S2** (the design 6.3 and 6.5, Appendices F and I):
1. `open-session` pins the current last ledger row v' (which now includes the new result) and records
   S2's roster: every released, unretired variant at that moment, now including the new revision.
2. `next` re-derives the state from the create-only records only. It finds the lowest target above
   `holdout_last` that has an accepted result and is not closed, and never looks at N + 1 while such an N
   exists.
3. **If N has a freeze line from S1:** `next` exits `FROZE N` and runs nothing. `score --target N` then
   verifies, before reading the outcome:
   - each named record's session record and digest;
   - its DONE ticket in S1's attempts ledger;
   - that the training pin v is a verified prefix of v', and that N <= last_draw(v').

   It then scores only the named records that have no score line yet. The score binds to S1's line and
   records. S2 and the outcome pin v' are kept as provenance; the records keep their S1 binding and pin v.
4. **The changed roster:** a target is closed under its line roster, fixed when the line was written. The
   new revision is not in S1's lines, so it gets no record for those targets and is never `MISSING_BATCH`
   for them. The current roster never reopens a closed target.
5. **A target with an accepted result and no line** (for example, a missed draw): `next` does three things.
   - It first settles any open tickets for it in any session's ledger: DONE if the run folder proves a
     completed run, otherwise `FAILED_TO_START` (that run id is never reused).
   - It then runs one ticketed contract run for each S2-roster variant that has no DONE ticket for it in
     **any** attempts ledger of the game. The new revision is included, classified by its release date as
     in Q2; the others are `CATCH_UP` if released before the draw date.
   - It then writes the freeze line, and scoring follows.
6. **The newly available result** is the open forecast M that S1 froze (as `FINAL_NEXT_DRAW`), if there was
   one. It is scored in strict draw order, after any lower unclosed draw, under its own line roster.
7. **When nothing is left to catch up:**
   - for the next draw, `next` writes `SET_STARTED`, runs the `FINAL_NEXT_DRAW` set for S2's roster (the
     new revision's first forecast) and writes the line, then exits `FROZE_NEXT` - but only if at least an
     hour remains before the deadline and no set or line exists for that draw;
   - otherwise it exits `OPEN M` or `NONE`;
   - `close-session` then removes the lock and the status block is printed.

**How accepted records stay intact and nothing is scored twice:**
- Every record is create-only, and nothing accepted is rewritten.
- A pair with a DONE ticket in any ledger is never run again.
- A target with a freeze line is never re-forecast.
- The score ledger refuses a second routine line for the same scientific identity (game, method, revision,
  variant, target, record digest, scoring policy id), whatever the score run id (L-S1).
- A torn last line in any ledger is ignored, reported, and completed by the next writer, with the fragment
  kept.
- Only a separately identified corrective scoring run, with its own policy id and `amendment_of`, may
  stand beside an accepted score.
- If the master grows during S2, `next` exits `STALE`. A new session continues from the same records,
  running only the missing variants.

## Q6. Installation and process safety

**The barriers** (Appendix J; MHUP-D2; Q10):
- **E** is E_1's own `IN_DEVELOPMENT.txt`. E_1 refuses while it exists.
- **P** is the package-wide `INSTALL_IN_PROGRESS.txt`. The new dispatch gate refuses every dispatch-gated
  run while it exists, like the orphan marker.
- **U** is the updater's own lock, `source_data/.results_master.lock`, with the content
  `INSTALL <package> <utc>`. It is taken at step 3 by `take-install-lock` and released at step 18 by
  `release-install-lock`, which deletes it only if it names this package. While U exists, the old and new
  updaters both refuse, and so does `open-session`.
- None of the three is ever committed.

**The install check:** `process_check.py check-no-runs --install <package>`, run from the staging folder
for MHUP-A, at steps 2, 5, 7, 11 and 14. It reports `CLEAN` only when all of these hold:
- no project Python process exists by the rule of 6.1;
- no session lock exists for either game;
- no updater lock exists other than this package's U (from step 3);
- for a roster-changing package, no weekly set is unfinished.

A Python process whose details cannot be read is a refusal, not `CLEAN`. The tool lists processes and never
acts on any.

**If an operation fails with a process running or of uncertain identity:**
- **Before step 6:** stop; remove E and P; release U (step 4). A check that is not `CLEAN` at step 2 or 5
  means waiting for the process to end and rerunning that step.
- **From step 6 onward, the restore rule (EX_131, mandatory):**
  - the install STOPs and the output comes to me;
  - every copied file stays, and E, P and U stay;
  - nobody retries, resets, deletes or reverts anything by hand;
  - the process is resolved manually and safely: the owner lets it finish, or ends it through its own
    console, which is a human action. No project tool or AI terminates anything (Architecture 5C, strict
    no-status/no-kill);
  - **only after a fresh install check reports `CLEAN`** are my exact reviewed restore steps followed, in
    order: `git checkout --` of the manifest's listed changed paths, deletion of its added paths, removal
    of E and P, and U released last, so the updater stays shut until the restoration is complete;
  - the restoration of the gate files carries the same seconds-long straddle risk as the forward copy.
- **Steps 12 and 13** (the commit and COMMITTED fail): the system fails closed. The code is committed but
  not released; nothing is pushed; E, P and U stay. I write a fix (a further small commit or a reviewed
  revert commit), and the step is rerun.
- **Steps 15 to 18** have their own STOPs: P is re-created if the release record or the release commit
  fails; U is released only if it names this package.
- **Other locks and markers:**
  - The orphan marker is never touched by any of this.
  - The updater's "delete the lock by hand" advice is never followed during an install.
  - A file one of the D3 programs left behind, seen by step 12's `git status`, is a STOP that comes to me.
    The file is disclosed and never deleted by hand; I write a reviewed addendum naming it, and step 12 is
    rerun.

**The residual risks the owner accepted, and their limits** (MHUP-D3, extended the same day):
- The owner does not launch the coordinator's POC path, the WF-1B report tool or the WF-1A driver during an
  install. No barrier stops them, but the install checks STOP the install if one is running at a check.
- **Residual (i):** one of those programs starts and finishes entirely between two checks.
- **Residual (ii):** a contract run started after step 5's check and finished before step 7's could read a
  mix of old and new gate modules during step 6's copy, which lasts seconds. Any record it published is an
  ordinary development record of today's kinds. The restore copy carries the same risk.
- **Bounds:** neither residual can change the master, the ledger, or any Mode H or weekly record. At most
  one leaves a search-log row or a plan, segment or report file, which is disclosed.
- **The process tool's own limits:**
  - an unrelated Python started from the same base installation is a known false positive, which the
    owner closes;
  - the controls protect against mistakes and against the AI chats and the runner, not against someone
    with write access to the owner's own machine (EX_127 C01).
- **Nothing beyond these is accepted.** In every failure state before recovery: no dispatch-gated run
  publishes (P holds until step 15), no updater writes and no session opens (U holds until step 18).

## Q7. E_1 revision 3, and what testing is mine and what is not

**Why it is needed** (the design section 2; MHUP-Q10):
- E_1 revision 2's own code (`src/methods/E_001/multigame_e1.py` lines 30 to 34) refuses any data kind
  other than `SYNTHETIC_CONTRACT_TEST` or `REAL_DEVELOPMENT`, and any target outside the development
  prefix.
- Every Mode H, catch-up or prospective run would therefore end in `RUNTIME_FAILURE METHOD_FAILED` for E_1.
- Changing a released method's code is a new revision (E2R-R14A).
- Revision 3 keeps revision 2's counting, ranking and tie order exactly. It takes the **view data kind**
  (one kind, `REAL_HISTORICAL_DEVELOPMENT`, for every real mode), and the adapter passes
  `view_data_kind(task.run_mode)`, so the method never sees a run mode.
- Its target admission moves to the shared target and mode gates; it keeps only
  `len(records) == target - first_draw`.
- Revision 2 is archived unchanged under `archive/methods/E_001/r2/` and never executed. Revision 3 has a
  new declaration and registry entries.
- The legacy forecast-only 1577 record stays as it is and is never scored. The Mode H forecast for 1577 is
  a separate revision 3 record. The two should coincide label for label, which gives a free R-4 oracle.

**The one-package arrangement:**
- ER-2r1 (register v0.23, 31 October 2026) put E_1 revision 2 and CODE-3 in one package, behind E_1's own
  `IN_DEVELOPMENT.txt`, copied first, deleted last and never committed. That was an exception to E2R-R58's
  recommended separate code and release packages, for E_1 only.
- MHUP-Q10 extends it to revision 3 inside MHUP-A.
- MHUP-A also changes the shared readers, validators, dispatch gate and evaluator used by the other 39
  variants, so the extension carries Appendix J's whole-package safety argument:
  - barrier E for E_1, barrier P for every dispatch-gated run, and U for the updater and sessions;
  - the checks at steps 2, 5, 7, 11 and 14;
  - the restore rule;
  - the install record at step 12, and the release record after COMMITTED PASS with E and P removed, as
    the second commit.
- E_1 revision 3's release date is the local date of MHUP-A's release record.
- MHUP-A also ships the baseline release record (the 39 variants released on 31 October 2026, plus E_1
  revision 2 marked superseded by revision 3), as an ordinary reviewed member.

**Review and synthetic evidence before the owner installs:**
- HIGH, with R-2 by the reviewer (reproduction of the authorised offline tests), RECHECK until PASS; no FIX
  AND PROCEED for the always-review subjects.
- The identity proof: a frozen reference fixture, `tests/fixtures/e1_r2_reference_v1.json`, computed at
  the base outside the repository. Revision 3 must match it label for label, for every ranking and tie
  output:
  - in both games;
  - on invented prefixes, under the synthetic and the real view kinds;
  - identically under each new real mode on the same prefix.
- Appendix L's oracles and tests:
  - L-G gates, L-H Mode H, L-U updater and environment, L-I and L-D install;
  - the existing tests that change (`test_code3_retirement.py` line 91, `test_e1r2_revision2.py` lines
    223 to 239, `test_wf1b_static.py`).
- EX_131 section 4's synthetic demonstrations:
  - the first-update admission;
  - the old and new updater lock;
  - failure-state restoration;
  - the unfinished-set refusal;
  - byte-code discipline, direct and nested;
  - the two-commit release order;
  - the stated rehearsals and owner choices.
- Mutation checks: one planted defect per rule, each caught by a named test.
- LF and CRLF install rehearsals with every negative case STOPping.
- Claude Code rehearsal T016 on Windows. It must also show the install preflight prints `CLEAN` on the
  owner's ordinary desktop with Claude Code and a console open, and that a live `Run_Experiment.bat` child
  is detected.

**Linux tests (mine, after authorisation) versus everything else:**
- **Mine:**
  - the unit suites, mutation runs and LF/CRLF rehearsals in my cloud workspace;
  - on synthetic, invented data, in disposable clones of a frozen mirror, on Python 3.13 and a 3.15 venv.
  - Some accepted older tests read the development masters through the project's reader (rulebook rule
    2.5). That is what they are written to do; I never open those folders myself.
  - E2R-T12 needs its run-context approval.
  - No test reads a holdout result, and nothing is destructive or terminates a process.
- **Not mine:**
  - the Windows rehearsal: a task file I write, which the owner starts in a new Claude Code conversation,
    in a throw-away clone that cannot push; its report is owner-machine evidence, not acceptance;
  - the owner's own Windows checks (the POC suite rerun if he chooses it, and the byte-code check of 4.1);
  - every real-data operation (the updater, the manifest, the opening, the Mode H batch and score,
    `declare-developed`, weekly sessions), which the owner runs on his PC, each with its own approval.

## Q8. The path ahead, decisions still needed, and the deferred items

**The order** (H-1 section 10; register v0.24 future actions; the design 4.4, 8; ORD-1; roadmap):
1. The takeover verified, and the owner's explicit authorisation of normal work. The takeover exchanges are
   recorded (EX_139 onward), the workspace set up, and the suite run on Linux.
2. **MHUP-A:** design sections 2 to 5 and 7. Code, tests, mutations and rehearsals; then R-2 review
   rounds; then T016; then the owner's acceptance and the two choices; then the two-commit install; then
   verification.
3. **MHUP-B:** design section 6 and the section 7 checklist, by the same route, with T017. T017 includes
   the first production contract run launched from a Python parent. MHUP-B is installed before Approval 1.
4. **Per game, each step separate:** Q7 decided and the updater's self-test under 3.15 (before Approval 2);
   Approval 1 (manifest, opening record); Approval 2 (first update); Approval 3 (Mode H batch); Approval 4
   (score, report, seal).
5. **GOAL-1:** the owner's `declare-developed` record, then the first weekly session: the catch-up from
   Oz Lotto 1704 and Powerball 1587, then the first forecasts frozen before their draws. The planning
   target is Oz Lotto 1709 (17 November) and Powerball 1592 (19 November); under FB-1 it slips a week
   rather than any review being cut. Register v0.25 records all of this.
6. **WF-1C**, the workers change (WORKERS-1), carrying EX_101's four obligations and EX_105's B01 and
   C02 to C05.
7. **Then the efficiency items of roadmap 21b, and the waves:**
   - wave 3 (E_27, E_45 = Method B, E_26, E_28);
   - the NL-means discussion (R-002);
   - waves 4 to 11;
   - Method A's diagnostics A1 to A5 as their own package;
   - the ensembles E_55 and E_56 last.

   Each new method follows the specification, code package, release package, batch and session route.

**Decisions and approvals still needed from the owner:**
- the takeover verdict and the authorisation of normal work;
- the T12 run context for the suite;
- the "go" for Fable at the MHUP-A core;
- acceptance of MHUP-A after review and T016;
- the Windows POC suite choice, and confirmation of the backup (asked 2 November);
- adding the deny entries for the new tools to `.claude/settings.json` (his edit) before task files touch
  them;
- acceptance of MHUP-B;
- Q7, before Approval 2;
- Approvals 1 to 4 per game;
- the GOAL-1 developed declaration;
- each weekly session (H-1 10.8 lists them as permission-gated);
- any change to the planning dates;
- ratification of register v0.25;
- later: the ChatGPT reviewer handover (R-016), WF-1C's open choices, walk-forward preregistration, the
  allowlist, and each new method's specification.

**The deferred items:**
- **The cross-batch report** (ranking across batches by reusing frozen records), with the retired index and
  a later method's back-history batch: roadmap 21b, ratified 2 November as after WF-1C and not before Mode
  H. I raise it when WF-1C is done; the owner scopes and approves it as its own package.
- **KISS-1, the simplicity review:** after full implementation and the method waves, and only when the
  owner explicitly asks; never started automatically (R-014).
- **The performance study** (`doc/Deferred_Performance_Engineering_Proposal_v0_1.md`): the very last stage
  (roadmap 22, R-006), after all implementation, holdout work and clean-up. It is scheduled but not active,
  and only the owner activates it. PERF-1 was the one item brought forward.

## Unresolved questions or contradictions found while answering

1. **Retrying a first update that STOPs.** The design (4.1, 4.4 step 3, and section 7's checklist) lets "the
   same approved first update" be run again with a wider window. The standing rule is "a STOP is a STOP:
   nobody retries; the output comes to Claude". My reading: the output comes to me first, and once I have
   confirmed the cause, the owner reruns under the same Approval 2. **For the owner to confirm:** may that
   rerun proceed under Approval 2, or should each retry get his fresh word?
2. **The direction document, section 3** (already raised in my first reply). Its "installed before that
   draw" and "install date" wording should read "released", meaning the release record's date, to match the
   design 4.3. This is a fifth place where the direction document is looser than the design, beyond the four
   register v0.24 lists. It makes no difference for the current cohort.
3. **The template README** reads "draft 4" in its title and "DRAFT 3" in its status line. Cosmetic; it can
   be fixed at the next template edit.
4. **An observation, not a contradiction.** After any install that changes the code, an interrupted
   session can no longer be resumed (`--resume` refuses on a changed closure); its lock must be cleared
   instead. The install check already refuses while a lock exists, so in practice an interrupted session
   is always resolved before an install. The owner's checklist (MHUP-B) should say so plainly.

Nothing else I checked disagreed with the repository. I start no development until the owner decides
whether the takeover has passed.

End of answers.
