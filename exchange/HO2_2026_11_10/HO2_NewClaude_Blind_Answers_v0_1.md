# HO-2 - replacement Claude chat: blind answers to the reviewer's Q1-Q9 (10 November 2026)

Project: hydra3333/analysing_perceived_randomness_in_reality
Checkpoint: main c48ac3c393d2eab30014e6200d427b76d90f47ac
Answering: HO2_NewClaude_Blind_Questions_v0_1.md (the reviewer's questions only; no answer key or assessment seen)
Status: takeover answers; NOT an EX message; no authority to run or install. US-ASCII, CRLF.

Method: answered from the repository at the checkpoint, read-only. Nothing was built, executed, committed or pushed; no data
folder was opened. One read-only static check was made for Q7 (named there). Where something is my reading rather than a
recorded decision, I say so.

## Q1 - Current position and scientific status

**Installed and runnable now** (each real run only under the owner's separate authorisation):
- 40 released (`SUPPORTED`) variants in each game: the 39 revision-1 variants of E_2-E_4, E_6-E_10 and E_17-E_19 (REL-1,
  `6a1bed9`), and E_1 revision 2 (E1R2, `86d12ea`).
- The walk-forward driver (WF-1A, `0d98706`), the contract runner, and the WF-1B scorer and ranking report with PERF-1
  (`24d192f`, `3fce327`).
- `ENABLE_CONTRACT_REAL_DEVELOPMENT` is True, for development draws only. The three other switches are False and the allowlist
  is empty (checked in `src/` at the checkpoint).
- `src/` and `tests/` are byte-identical to PERF-1 at the checkpoint. The installed suite is recorded as 471 tests (H-1 v1r8
  7.4); I have not run it.

**Implemented and independently reviewed, but not installed:** MHUP-A. Slice 1 PASS (EX_146); slice 2 v1r2 PASS (EX_152, which
permits preparing one integrated install candidate for its own review, nothing more). None of its files exist on `main`
(`process_check.py`, `install_records.py`, `master_versions.py`, `owner_records.py`, `Method_Mode_H.py`, `Run_Evaluation.bat`
and the updater v0.2 are all absent; `results_master_v0_1.py` is still present).

**Designed and ratified, not implemented:** MHUP-B (design v0.1r6 section 6: the weekly session, CATCH_UP and FINAL_NEXT_DRAW,
the ledgers, the orchestrator, the A1 section 6 corrective route) and the operating procedures of section 7. Also WF-1C's
direction (WORKERS-1), whose design is not yet written.

**The three kinds of test evidence, kept apart:**
- **T022 (Windows, Python 3.15.2, owner-reported):** the reviewed slice 2 candidate v1r2, on its old base, in a task clone
  with the owner's then `src/GAIS/` present: 570 tests, PASS, 4 allowed symlink skips. It is evidence for the reviewed
  candidate's code on Windows, not for the final integrated package.
- **8 November preliminary run (Linux, Python 3.13.18 and 3.15.0b4, the previous Claude chat):** the reviewed code rebuilt on
  `009c985`; 570 ran on each Python, 569 passed, one expected failure each (`test_e1r3_revision3`, which pinned the old
  candidates' date); after the build's counted date edit, only that 8-test module was rerun (8/8 on each). Labelled
  preliminary; logs kept unaltered in `integrated/evidence/`.
- **Required on the final package:** the full suite on both Linux Pythons, both mutation chains, LF and CRLF end-to-end
  rehearsals with every negative STOPping, and T016 on Windows, all on the one date-frozen final candidate. The suite count
  must come from the tools (570 today; it changes if the final package adds tests).

**Scientific conclusion:** only a descriptive one, as development evidence. In both games nothing departs from fair draws
under the reported measures (Oz Lotto family Bonferroni P 0.090, N1 maximum P 0.067; Powerball main family Bonferroni P 1.0,
N1 maximum P 0.73; the smallest single figures are what about 80 figures give by chance). It is walk-forward over development
draws only, with no holdout draw read, and covers 40 simple variants. It is not proof of randomness, says nothing about the
other 50 catalogue methods, and is not Mode H or prospective evidence.

## Q2 - Ratified A1: the scoring order

Precondition: `BATCH_COMPLETE` exists and the scorer has verified the exact planned roster (every pair, each with its DONE
ticket).
1. `SCORING_STARTED`: written before any outcome read; it fixes the score attempt id, the roster digest and the digest of the
   scoring plan (with its `MODE_H_REPORT` search-log row).
2. One read of the ten targets' outcomes, through the outcome reader under the freeze-before-outcome rule (design 5.3).
3. Compute every score line and every MR5 rank-position line of the attempt from that one read.
4. Publish the whole ledger `mode_h_score_ledger.jsonl` once, create-only (bytes written and synced to a temporary file, then
   linked to the final name), so it either does not exist or exists complete.
5. Validate the published ledger as it stands: exactly the lines this scorer writes for the roster's frozen forecasts, given
   the drawn numbers the ledger itself records; every identity once, nothing missing, duplicated or foreign; drawn numbers
   consistent across a draw's lines; every line rebuilt byte for byte; Oz Lotto supplementary counts checked for range and
   division (the supplementaries themselves are never stored).
6. `SCORE_COMPLETE`, holding the ledger digest (and, per B05, the game, attempt, parent-plan digest and line count).
7. The report from the accepted lines only, its three files published or resumed one by one.
8. `MODE_H_SEALED`, holding the attempt id, ledger digest and report digest.

**No outcome re-read** from the moment the ledger exists (step 4): its lines are validated from their own recorded drawn
numbers. After `SCORE_COMPLETE` the outcome reader refuses every holdout target.

**If validation fails:** a STOP for the owner and the reviewer. The published ledger is kept as it is (never overwritten,
repaired or deleted), no `SCORE_COMPLETE` is written, and no new routine attempt is started.

## Q3 - Ratified A1: crashes and attempts

- **(a) Before the complete ledger is published** (including a crash while computing or writing the temporary file): the rerun
  finds `SCORING_STARTED`, re-verifies the roster and the frozen scoring plan, reads the same pinned outcomes again, computes
  and publishes the whole ledger. This is permitted because no outcome of the attempt has been accepted. A leftover temporary
  file is never read.
- **(b) After publication, before `SCORE_COMPLETE`:** no outcome is read. It validates the existing ledger, then writes
  `SCORE_COMPLETE`, or STOPs if the ledger is not exactly the scorer's.
- **(c) After `SCORE_COMPLETE`:** no outcome is read. It checks that `SCORE_COMPLETE` names this game, attempt, plan, ledger
  digest and line count (B05), resumes the report file by file (verifying any file already written), then writes the seal.
  After the seal, routine `score` refuses.

**Fixed across retries:** the attempt id, the roster digest, the scoring plan frozen by `SCORING_STARTED` and its search-log
row, the pinned master version, and (once published) the ledger bytes. A retry is a resumption of the same attempt, never a
second one.

**Why skip-already-scored-pairs no longer applies:** that rule served per-pair lines, where "some lines written" was a possible
state. With one create-only publication there are only "no ledger" and "complete ledger", so there is nothing partial to skip.

**Corrective scoring** belongs to MHUP-B (A1 section 6; owner decision IIIB-1): after the seal only, a new attempt beside the
first, with its own scoring policy id and `amendment_of` naming the sealed attempt and ledger digest, under an extended,
reviewed release rule, published create-only, never touching the first ledger, `SCORE_COMPLETE` or seal. MHUP-A provides none
of it.

## Q4 - C01-EFF and final evidence identity

**The rule:** E_1 revision 3's `effective_date` is the date the integrated package is prepared and frozen for review. It is not
the install, admission or release date. The release record alone dates a release (its local date at Appendix J step 16).

**When:** chosen once, when the final candidate is frozen (the DATE argument to `integrated/build_dev_integrated.sh`), after
the tools and verifier exist and after the owner's R-020 (g) decision, and before any final evidence is produced.

**What it changes:** the two `entry_0003.json` registry files (POWERBALL and OZLOTTO), `archive/methods/E_001/r2/README.md`,
and the date `test_e1r3_revision3` pins (set by the build's counted edit). Through them it changes every identity built on
those bytes: the registry entries' digests and chain, the package manifest's SHA-256 values, the install record's manifest
digest, and the package zip.

**If anything changes after the final evidence** (the date, the base commit, the baseline record or any package byte): it is a
new candidate. Every piece of final evidence is produced again on it (suites, both mutation chains, LF/CRLF rehearsals, T016),
and the review covers those bytes. Evidence from earlier bytes is preliminary only.

## Q5 - DEP-1 and GAIS-1 at the freezes

**(a) The Mode H environment freeze (Approval 1, design 4.1):** it records the interpreter's files and every installed
distribution's `RECORD` with per-file hashes, and checks them at every later Mode H step.
- **DEP-1:** `pyahocorasick` is an approved dependency, installed in the owner's venv. It is frozen like any other
  distribution. Nothing in `src/` or `tests/` imports it. I have not seen the owner's venv, so its actual files are not
  established by me.
- `install_upgrade_dependencies_into_venv.bat`, changed by the owner for DEP-1, is part of the closure, so its current bytes are
  what Approval 1 freezes.
- **Any later change to the venv** (a pip run, an upgrade) after Approval 1 makes every Mode H step refuse. No dependency change
  is allowed between freeze and scoring.
- **An unexpected file in `site-packages/`** that no `RECORD` lists (a stray `.pth`, a sourceless `.pyc` outside
  `__pycache__/`) makes the manifest refuse and name it. That refusal is a STOP. The fix is a reviewed, owner-approved step,
  never a hand deletion and never a loosened check. The Windows branch of the inventory first runs on the owner's machine at
  T016.

**(b) The MHUP-A code closure:** every file under `src/` (any extension, `__pycache__/` aside), every root `.bat`,
`requirements.txt` and the dependency installer.
- **GAIS-1** moved GAIS out of `src/` to the top-level `GAIS/`, so it is outside the closure. y-cruncher is untracked by
  `.gitignore`.
- **The owner's root `create_venv.bat`** is a root `.bat`, so it is inside the closure. It also changes the venv the freeze
  records, so it joins rulebook rule 7 (delta 7 item 5).
- **The owner's `.gitignore` lines** must survive: the package's `.gitignore` is the current one with the MHUP-A block
  appended (R-020 (d)).
- **My reading, to confirm at Approval 1:** the closure is enumerated from the disk, so an untracked file under `src/` on the
  owner's PC would be in it (or refused, for a sourceless `.pyc`).

**What to check when building on the current `main`:**
1. `git fetch`; list everything that changed outside `exchange/` since the last base (delta section 8).
2. `src/` and `tests/` are unchanged from the base the overlay's replaced files expect; nothing has come back under
   `src/GAIS/`.
3. `.gitignore` and the root files (`.bat`, `install_*`, `README.md`) are checked against the overlay's members.
4. The package's base commit is the `main` the candidate is frozen on.

At the checkpoint, since `009c985` the only change outside `exchange/`, `GAIS/`, `doc/` and the Claude Code folder is the root
`README.md`, which is not one of the overlay's 70 files.

## Q6 - R-020 (g), T016 and command controls

**Decided (owner, 10 November 2026, about 18:30), option (i):** Claude Code's rulebook v0.5 may allow `process_check.py` and
`install_records.py`:
- only inside T016's synthetic, non-pushing task clone;
- only run from the package's staging folder;
- only under the T016 task file;
- with the reviewer's EX_157 section 3 conditions: every other safeguard unchanged; the `.claude/settings.json` denials not
  bypassed; `check_task_commands.py` passing on the actual task; no change to the main repository; the rule change reviewed
  with the integrated package.

**What it does not authorise:**
- T016 itself (it needs the owner's separate go);
- those two tools anywhere else (the main repository, any other task, the owner's live install);
- any other rule 7 program (`Run_Experiment.bat`, `Run_Evaluation.bat`, `Method_Mode_H.py`, the updater, the report tool);
- edits to `.claude/settings.json`;
- data reads, real runs or a push.
Rulebook v0.5 is not written yet. It comes with the package (item 5) and is reviewed with it.

**How the controls fit together:**
- **The denials** match command text (for example `git -C *`, `git add*`, `git commit*`, `git rm*`, `*results_master*`,
  `*.bat*`, data-folder reads). The permission layer enforces them.
- **`check_task_commands.py`** is my pre-check, not the enforcement: it matches every fenced command line of a task file
  against the Bash deny patterns, and a task is committed only on PASS.
- **Git steps in the clone** therefore go through `cc_clone.py git`.
- **Files with denied names** (the updater, the `.bat` launchers) are copied by the package's copy tool from the manifest or a
  plan file, never named on a command line.
- **The staging folder** is the package zip unpacked in the task's scratch folder with its SHA-256 checked. PRE checks
  `process_check.py`'s SHA-256 against the manifest. The tools run with the venv's Python `-I -B -X pycache_prefix=<the
  never-existing folder>`.
- **The disposable clone** is made by `cc_clone.py make`: origin removed, a refusing pre-push hook, under `scratch/`. Step 19
  (push) is omitted, and steps 3 and 18 act on the clone's own lock path, never the main repository's.

**An uncertainty to settle now, not assume:**
- Register v0.24 future action 1 has the owner add deny lines for MHUP-A's tools.
- If a Bash deny line naming `process_check` or `install_records` exists when T016 runs, the denials would refuse T016's steps,
  and the conditions forbid working around them.
- No such line exists today (the only related entry is `*results_master*`).
- So the order of the owner's deny-line edit relative to T016, or the exact wording of those lines, must be settled with the
  rulebook v0.5 change, in the open and reviewed. I will not choose a wording that slips past a denial.

**If the conditions cannot be met cleanly:** fall back to option (ii): the owner runs T016's steps himself, and Claude Code only
prepares the clone and reports. I would report and ask, not improvise.

## Q7 - Package installation and actual release

**The step 6 gate files:** the import closure of `contract_dispatch.py`, restricted to files the package changes or adds.
- Eight changed: `contract_dispatch.py`, `contract_forecast.py`, `contract_receipts.py`, `contract_records.py`,
  `contract_runner.py`, `contract_task.py`, `contract_vocab.py`, `game_draws_reader.py`.
- Two new: `master_versions.py`, `owner_records.py`.
- All are under `src/methods/_common/`.
- **Read-only static check today:** I parsed the reviewed v1r2 overlay's imports, without executing anything, and compared them
  with `main` at the checkpoint. It gives exactly these ten. This is preliminary; the builder must redo it on the final tree.

**Why derive and assert it, not copy a count:**
- The count was once written wrongly (11; EX_157 C02).
- The base has moved.
- Step 6 must swap in a self-consistent new gate in one short copy. A missed module leaves new gate code importing an old one
  (or failing at import) during the window. An extra file needlessly widens what changes before P protects it.
- So the builder computes the closure from the final tree and asserts it equals the manifest's `gate_files`, and the copy tool
  copies exactly that list (`--part gate`).

**Two commits, two records (design 4.3, Appendix J):**
- **Package commit (step 12):**
  - after POST and the suite, the record tool writes `INSTALL_MHUP_A_V1.json`: the package, the manifest SHA-256, the UTC time
    and local date, and the registry entries added;
  - this records code arrival only;
  - the listed paths are staged, `git status --short` must show exactly them, and the commit is made.
- **COMMITTED (step 13):** the commit changes exactly the overlay's paths (including the deletion of `results_master_v0_1.py`)
  plus the install record, and every blob matches the manifest.
- **Then:**
  - step 14, the install check again;
  - step 15, delete E, then P;
  - step 16, the record tool writes `RELEASE_MHUP_A_V1.json`: E_1 revision 3 for both games, the local date of this step and
    the install record's digest. It refuses while P exists, before COMMITTED PASS, with a session lock, or (roster-changing)
    with an unfinished weekly set;
  - step 17, the release record alone is staged and committed.
- **The `released` phase** checks that:
  - the release commit's only parent is the package commit;
  - it adds exactly `RELEASE_MHUP_A_V1.json`;
  - the record names E_1 revision 3 for both games, the install record's digest, and a local date not before the install
    record's;
  - E and P are absent and U still holds this package's content;
  - the records agree with the repository (EX_148 (ix)).
- **Step 18** releases U (only if its content names MHUP_A). **Step 19** pushes both commits.

**Before E_1 revision 3 is released:**
- the release record above must exist and validate;
- the package manifest's `release_entries` names revision 3 for both games (R-020 (a));
- the baseline record `RELEASE_BASELINE_20261031_V1.json` lists the 39 variants and E_1 revision 2 as superseded;
- after release the runnable cohort is 39 plus revision 3 = 40 per game.

**Until then:**
- revision 3 is installed but unreleased, with no CATCH-UP standing;
- E makes E_1 refuse;
- P makes every dispatch-gated run refuse;
- U makes the updater (old and new) and session opening refuse;
- a STOP after POST leaves an install record and no release record, which qualifies nothing.
From step 6 on, a STOP follows the restore rule: barriers kept until a fresh `CLEAN`, nothing terminated by a tool, then
Claude's reviewed restore steps, with U released last.

## Q8 - Mode H boundaries and deferred decisions

**Why it is a historical holdout evaluation, not a pre-draw prediction:**
- The ten holdout draws per game (Powerball 1577-1586, Oz Lotto 1694-1703) have already been drawn and published.
- Under option A the updater brings them all into the master before the Mode H batch runs.
- When each forecast is made, its outcome already exists in the system. It is kept from the method by the reader (prefix-only
  parse, T-05, the B1 rule), not by time.
- What is precommitted is everything else, frozen before opening: the study plan, cohort, targets, measures, families, seed
  policy, code closure and environment. All planned attempts are frozen before any scoring process reads a holdout outcome.
- So it is "a precommitted holdout evaluation with N-1 isolation, not pre-draw forecasting".
- Powerball 1585 and 1586 also carry an exposure flag (HX-1): a reviewer chat once displayed them. They are scored and counted
  in full.

**Still open:**
- **Q7:** whether, after a game's Mode H is scored, the display restriction on holdout draws is relaxed. The recommendation is
  to keep it. It must be decided before Approval 2. Until then every current restriction stays in force.
- **MHUP-B timing:** installed before Approval 1 or only after that game's Mode H is sealed, never while a holdout is opened and
  unsealed (design 4.4). The owner chooses, and the integrated install plan states the route.

**Separate from MHUP-A's PASS and install, each the owner's own decision:**
1. T016's go.
2. Which offline tests the reviewer may run.
3. The install approval itself.
4. At that approval: whether to rerun the Windows POC suite after the `Run_Experiment.bat` change or accept it unrun, and
   confirming the backup of `results/` and `source_data/` (R-015).
5. MHUP-B's own design-to-code review and install.
6. Per game: Approval 1 (study manifest and opening record), the updater's offline self-test under Python 3.15, then Approval 2
   (the first update, which must reach `holdout_last` or write nothing), Approval 3 (the Mode H batch), Approval 4 (score,
   report, seal).
7. The GOAL-1 "developed" declaration.
8. Each weekly session (after GOAL-1 the owner's own deliberate run is that week's authorisation; R-018 (h)).
9. Any dependency change, any further real-data batch or report, and any master update.

## Q9 - Exact immediate work and authority

**Immediate unfinished task:** delta section 7 item 2, the package builder `integrated/build_mhupa_pkg.py`. It writes
`repo_overlay/`, the JSON manifest, the copy tool, the verifier (`pre`, `post`, `committed`, and the new `released`), the suite
runner and `INSTALL_INSTRUCTIONS.md` (Appendix J steps 0-19 as exact CMD lines). PLAN.md's checkpoint stops at "Next: item 2".

**What must be refreshed first (item 1):**
- The previous chat's trees are gone, so they must be rebuilt anyway, and `main` has moved from `009c985` to `c48ac3c` (or
  later by then).
- Rebuild on the current `main` with `build_dev_integrated.sh`, and re-check the 66-of-70 identity with the reviewed overlay
  and the expected four differences (`.gitignore` and the three date files).
- Re-check `.gitignore` and the root files, and recompute the gate closure.
- Optionally rerun the full suite as preliminary evidence.
- Fetch again immediately before the freeze.

**Order after that:**
1. Item 3: the `released` phase, the two-commit and barrier-order proofs, the verifier's own negatives, and a fresh-helper cold
   read of the instructions against Appendix J (on Fable, after the owner's go to switch).
2. Item 5: rulebook v0.5 to option (i), with the deny-line ordering question of Q6 settled.
3. Item 6: freeze the date and the base, and build the final candidate. Then all final evidence on it: the full suite on both
   Linux Pythons, both mutation chains, LF and CRLF rehearsals (steps 0-18, step 19 omitted, each negative STOPping), then T016
   on Windows under the owner's go.
4. Item 7: the review message at the next free EX number (EX_163 if nothing intervenes), with the ZIP and manifests, base and
   target identities, test and mutant inventories with logs, T022 and T016 evidence, DEP-1 and GAIS-1, A1 cited, the MHUP-B
   route, and the owner's list of tests the reviewer may execute. If T016 has to follow the review, the review is provisional as
   to Windows and an evidence recheck comes before install.
5. Item 8: after PASS and the owner's separate approval, the owner's install (two commits); my verification from GitHub;
   register v0.27; then full H-1 and H-2 editions.

**Authorisations:**
- **Before normal work:** the owner's explicit "go", after the reviewer has checked my takeover reply and these answers. I do
  nothing before it.
- **E2R-T12:** the owner approved it today (10 November 2026) for suite runs in my cloud workspace, once normal work is
  authorised. Any new run context (T016 on Windows, the reviewer's own reproduction, another machine) needs its own approval.
- **T016:** rulebook v0.5 reviewed with the package; any settings deny lines being the owner's edit (ordered as in Q6);
  `check_task_commands.py` PASS on the task file; then the owner's separate go.
- **Any real-data operation:** each its own owner approval after independent review: the install, Approvals 1-4, the updater,
  any batch or report, each weekly session before GOAL-1, any dependency change. Nothing is inferred from a PASS or a
  ratification.

**On a STOP:** stop there.
- No retry, rerun, reset, workaround or deletion.
- Capture the exact output and report it to the owner in plain words.
- Diagnose the cause, suggesting a switch to Fable if it is unexplained.
- Propose the recovery.
- The owner authorises each retry (R-018 (a)). A retry under an existing approval is allowed only when the refusal came before
  any change and its cause is positively identified within the original operation; otherwise the recovery steps are separately
  reviewed and approved.
- For an install STOP from step 6 on, the restore rule applies.
- The orphan marker is never touched, and no process is ever terminated by me or by a tool.

End of answers.
