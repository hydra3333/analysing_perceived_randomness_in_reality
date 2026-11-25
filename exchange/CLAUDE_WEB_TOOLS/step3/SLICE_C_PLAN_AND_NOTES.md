# Build step 3, slice C (creating a tree, the installs, verifying a tree): plan and working notes

**Date:** 25 November 2026. **Author:** the Claude web chat (on Fable, the owner's go: decision log entry 301).
**Status:** working notes, kept up to date as the slice is written. Not reviewed, not ratified. It authorises nothing.
**If a chat resumes or a new one starts:** read this file, then the files it names under `overlay/`, then go on from
section 4 ("Where it stands"). Slices A and B are reviewed (EX_321, EX_327) and lie in the same overlay (34 files).

## 0. On resuming after a stop (the owner, decision log entry 302): check before any further work

1. `git fetch`, then `git status -sb` in the commit clone: nothing ahead, nothing behind, nothing uncommitted that
   matters. If something is ahead, look at it (`git show --stat`) and push it; if something uncommitted lies under
   `overlay/`, compare it with section 4 before keeping or dropping it.
2. The decision log's last line gives the next numbers; the last entry is the last thing recorded. Anything the
   owner said after it is recorded first.
3. Section 4 below says which parts are finished (committed with their tests) and what was in hand. A part that
   section 4 does not call finished is treated as unfinished: its tests are run again before anything is built on
   it.
4. The cloud workspace (`/home/claude/work`) is a convenience only. If it is still there, its disposable clone for
   slice C is `dev12` (made from `main` with the overlay laid over it by `sync_and_test.sh`). If it is gone, make it
   again: nothing that matters lives only there.
5. Then say to the owner, in a few lines, what was found and what is next.

## 1. What governs the slice (all ratified; nothing here is a new design)

- Deployment design v0.12: section 3 (what can be installed; what every install checks), 4 (`Init_Tree`), 5
  (`Install`), 6 (`Reinstall_Infra`), 7 (`Verify_Tree`), 8 (an operation stopped half-way), 9 (the process rules of
  the install tools: "the existing rule of design 6.1, applied to the target tree, the tool's own chain excepted"),
  2 (the install tools live in DEV; with RAT-56, psutil for the process rule only).
- Specification v0.6: section 12.1 to 12.6 (12.3 the checks and the smoke case; 12.4 the question of an
  infrastructure reinstall, in full), 13 (the environment), 3.4 and 3.5 (variants and the status file).
- The build plan v0.1r1 sections 4 and 6; EX_301.
- Out of this slice: `Correct_Shared_Code`, the QA software replacement, the reseeding, the rerun (build step 4);
  the updater (slice D). Their states of design section 8 are recognised and refused, not carried out.
- The working principle: the smallest thing that carries out those clauses. "The same command again" is the only
  resumption; no repair; no new record.

## 2. The parts, in the order they are written

**C1. The checks that travel with the installed software** (design 3.3 items 4, 6, 7; specification 12.3 items 2, 4,
5). New infrastructure in every tree, run with the tree's own Python: the smoke case of a variant for a game (an
invented results table from a fixed seed, long enough for the variant's declared minimum history; the ordinary
engine; passes only on a complete FORECAST; writes only under `<tree>/scratch/`; removed on success, left and named
on failure); the fixed sample of stored forecasts recomputed and compared by content; the derived results in full
(the existing check of specification 5.8). One entry point that a tool in DEV can start with the target's Python
and read the result of. **And `Verify_Tree.bat`** (design 7), which is those checks, the environment's marker, and a
backup attempted before and after.

**C2. What every install shares** (new `deploy/` module): the plan (every file to copy with its hash, from the
markers and the manifest); copying a file (temporary name, hash, rename; no existing file opened for writing); the
barrier `records/INSTALL_IN_PROGRESS.json` holding the plan, and the comparison of a barrier found with the plan now
(design 8); the reservation of the target (its job lock by exclusive create, then the process check under it; the
updater's lock; `SNAPSHOT_DUE`); the recovery kit and the backup attempted, and the one question with their results
said exactly; `INSTALLED_FILES.json`; the log line in `records/INSTALL_LOG.jsonl`; the suite on a temporary copy with
the target's Python when the target's infrastructure is file for file DEV's.

**C3. `Init_Tree.bat QA|PROD`** (design 4, nine steps; it stops at step 6 for the owner to build `.venv`, and the
same command goes on).

**C4. `Install.bat QA|PROD [--only ...]`** (design 5, eleven steps; add-only).

**C5. `Reinstall_Infra.bat QA|PROD [--replace-unfinished]`** (design 6, eleven steps; refuses any forecast-class
file; says what it would change before it asks; the cutoff file when a change from draw X was accepted).

## 3. Readings taken (for the reviewer; RECOMMENDED unless marked)

- **C-R1, the smoke case's table and target.** The table runs from the game's first draw to the first draw the
  variant declares it can forecast, and that draw is the target: the declared minimum history, and not one draw
  more, must be enough. (The target's own row is in the table; the N-1 view does not show it.) Any answer but a
  complete FORECAST fails, and so does any error at all while the method is imported or run.
- **C-R2, "a fixed sample of stored forecasts".** Of each installed variant's stored lines that hold a FORECAST, in
  each game: the first, the middle and the last. Fixed by rule, the same on every run; three a variant a game.
- **C-R3, the derived results at an install are read as the job reads them, and nothing is written.** The reading
  half of the job's `open_game` is now its own function `read_game` (one reviewed file changed,
  `src/research/research_job.py`: a pure extraction); the checks call it. The check never writes or changes
  `NOT_CURRENT_FROM.json`. A difference at or after a draw the tree's own marker already names as a MISMATCH is
  reported as known; where a catch-up is awaited, only the draws before it are compared, as the job does.
- **C-R4, software and data in two folders.** Each check takes the software's folder and the data's tree
  separately, for design 6 step 3 (the software as it would be, against the target's data, writing nothing in the
  tree). Status files are read where the software lies and are never created by a check, in any role.
- **C-R5, what withholds the environment's marker at `Verify_Tree`, and what is only reported.** Design 7 names
  two things that write no marker and remove an older one: a failed smoke case and a failed suite. It has the
  forecast sample's differences reported. For the derived results it says only "in full". Reading taken: a derived
  result that is not what the software computes here is said in capitals and does NOT withhold the marker, because
  the tree's own remedy for it (the research job marks it not current; the owner runs the rerun) cannot start
  without a verified environment; withholding would leave the tree with no command that works. The same for a
  game whose stored records the job itself would refuse: said, not compared, marker written, and the job refuses
  that game as it always would. `Verify_Tree` never writes `NOT_CURRENT_FROM.json`.
- **C-R6, a refusal of `Verify_Tree` leaves the marker as it was** (settings, DEV tree, an unfinished operation,
  the orphan marker, another Python process of the tree, a held job lock, software that is not what was
  installed, a status file that fails its check). Only a verdict removes or writes it. The tree's note that a
  backup is owed (`SNAPSHOT_DUE`) is written before the first smoke case; one line goes into
  `records/INSTALL_LOG.jsonl` for either verdict (`VERIFICATION`, `VERIFIED` or `NOT_VERIFIED`).
- **C-R7, the `checks` command only finds and tells.** `src/tree_checks_command.py checks --data <tree> --result
  <file> [--smoke ALL|NONE|ids] [--sample] [--derived]` is started by DEV's install tools with the target's Python
  while they hold the target's lock. It writes what it found as one line of JSON to a file that must not exist,
  and ends with 0 whatever it found; what stops an install is the tool's to decide. It refuses a Python that is
  not the environment the data tree's settings name.
- **C-Q1 IS DECIDED: OPTION 1 (the owner, 25 November 2026; decision log entry 305): `Verify_Tree.bat` does not
  run the test suite.** The code is brought to exactly that; the hook for a suite is removed. **Owed: an
  amendment of two ratified clauses, to go to the reviewer with slice C and be ratified by the owner after his
  view (RAT-59).** Proposed wording:
  - *Deployment design section 7, first paragraph, to read:* "Process check; a backup attempted; the structure;
    every installed variant's smoke case; the fixed forecast sample, whose differences after an environment change
    are **reported** for the W-23 review and do not by themselves refuse; the derived results in full, reported
    likewise; `ENVIRONMENT_VERIFIED.json`; a backup attempted. **The test suite is not run by `Verify_Tree`:** the
    tests live in DEV and the installed software starts no program; the command says so every time. A failed smoke
    case writes no marker and removes an older one." (The rest of the paragraph unchanged.)
  - *Specification section 13, "Verified before use", to read:* "`Verify_Tree.bat`, run in the tree, makes the
    checks of 12.3 that travel with the installed software (items 1, 4 and 5, and every installed variant's smoke
    case) with that tree's Python and, on success, writes ..." (the rest unchanged); and item 3 of 12.3 gains: "The
    suite is run by the install tools in DEV (at a tree's creation and at an infrastructure reinstall), never by
    `Verify_Tree`."
  The record of how the question stood before the decision follows.
- **C-Q1 as it was put to the owner: the test suite at `Verify_Tree.bat`.** Design 7 has `Verify_Tree.bat` run in the
  tree and run "the suite, if the tree's infrastructure is file for file DEV's". Two facts stand against doing
  that plainly. (1) The tests live only in DEV, and a QA or PROD tree's settings do not say where DEV is (design
  1). (2) **The project's own rule is that the engine starts no program** (`tests/test_research_job.py`,
  `test_the_engine_starts_no_program_and_opens_no_connection`, over every file of `src/research/`): the whole
  suite failed on the first writing of `tree_verify.py`, which started DEV's tool with `subprocess`. The code was
  corrected, not the rule. The ways on:
  - **(1) RECOMMENDED, the simplest: `Verify_Tree` does not run the suite, and says so in capitals every time.** It
    rests on every installed variant's smoke case, the forecast sample and the derived results in full. The suite
    is still run with the target's Python at `Init_Tree` and at every `Reinstall_Infra` (DEV's tools start the
    target's Python by design). Needs a short amendment of design 7 and specification 13 (RAT-59) and the
    reviewer's view. Why it is safe for the main game: the scores and the ledger are recomputed in full and the
    forecasts sampled, so what the suite would add at that moment is protection against a later STOP, not against
    wrong science; W-23 already has DEV rebuilt first and the suite's evidence produced there; and a tree must be
    verifiable with no DEV on the PC (after a restore onto a new PC), so the suite could never be required.
    Uncertainty: PROD's `.venv` is built on its own day and may get another build of a package than DEV's; this
    way leaves that case to the smoke cases and the stored-result checks.
  - **(2) keeps the ratified words:** the owner names DEV (`Verify_Tree.bat --dev <DEV's folder>`); the tree's
    program (`src/tree_checks_command.py`, not the engine) starts DEV's tool with the tree's Python; the project's
    test is widened to watch that program and allow that one call. One named exception to "the installed
    software starts no program". Written once already (commit `d2cb640`: `check_dev_folder`, `suite_from_dev`, five
    tests) and taken out again; DEV's tool would still be to write. Without `--dev` the suite is not run, so in
    practice it runs when the owner remembers the path.
  - (3) the batch file runs DEV's tool first and hands the verdict to the verification: the order of design 7
    is lost and a verdict travels on a command line. Not recommended.
  (Before the decision the code took the suite's answer from a function its caller gave; that hook is gone.)
- **C-R8, what "the suite" of an install is, and what its temporary copy holds** (design 17: "the code round lists
  exactly what the suite needs from the repository ... that list sits beside the infrastructure manifest. Tests
  that served only the old system are not part of the new suite"). The list is `deploy/SUITE_MANIFEST.ini`: the
  19 test modules whose subject is on the infrastructure manifest (`test_file_form`, every `test_research_*`,
  every `test_trees_*`); a test in `test_trees_suite` holds the list to exactly those that exist. The copy is not
  a second list: it is what the project's own walk already calls the project (`deploy/file_form.py`,
  `files_under`: every file under `src/`, `deploy/`, `tests/` and the files directly in the root), except
  `ENVIRONMENT.ini`, which no tool ever writes anywhere. Found by trial: 16 of the modules pass on a copy holding
  only the manifest's files and the fixtures; the other three need more of DEV (`test_file_form` and
  `test_trees_readiness` read the living project and its real variants; `test_research_forecasts` compares the
  new reader with the first system's). Each module is run in a process of its own with the Python named, in the
  copy; a module that fails, or that ran no test, fails the suite; the copy is removed on a pass and left, with
  each module's output, on a failure. No time limit is put on a module.
- **C-R9, TO BE TAKEN IN C5, FOR THE REVIEWER: the job lock and the backup at an infrastructure reinstall.** Design 6
  has the target's job lock "taken and held to the end" at step 2 and the `PRE_INFRA` backup attempted at step 4.
  Slice B's reviewed rule is that no backup is made while a job lock lies in the tree (the lock file would be
  inside the ZIP, and a restored tree would refuse every job). Reading to take: `Reinstall_Infra` holds the lock
  for step 3 (what it would change), lets it go for steps 4 and 5 (the kit, the backup, the question), and takes
  it again at step 6 by an exclusive create with a fresh process check, exactly as an ordinary install does at
  its step 6; a job that began meanwhile refuses the reinstall there, nothing having been overwritten. Step 9's
  full comparison is made under that second hold, so nothing a job wrote in between goes unchecked. The other
  way (teaching the backup to leave out a lock its caller holds) changes reviewed slice B code and the restore's
  exact set, and is not proposed.
- **C-R10, the order at the end of an install.** Design 5 step 10: "`INSTALLED_FILES.json`; the log line; the
  updater's lock released; the barrier removed, last". Built so: `finish` writes the list and the log line, calls
  what releases the updater's lock, and removes the barrier; the job lock is let go after that. If the block
  that holds the updater's lock ends any other way (a failed check, a fault), that lock is released and the
  barrier stays.
- **C-R11, "YES".** Only the three capitals, with nothing else on the line but spaces, proceed. "yes", "Y", Enter and
  an input that has ended are NO.
- **C-R12, what stops an ordinary install after copying** (design 3.3 items 4, 6, 7): any failed smoke case; a game
  whose stored records the job itself would refuse; any difference in the forecast sample; a derived difference
  the tree does not already mark as not current. A difference the tree already marks is the known one and is
  reported, not a stop. If the `checks` program ends with any exit code but 0, or leaves no result of its kind,
  nothing is known and nothing passes.
- **C-R13, readings taken in `Init_Tree`** (design 4; specification 12.5).
  (a) *The environment's marker is written by the tree's own Python, not by DEV's:* the marker lists what the
  Python that writes it has installed, and the digest takes that Python's base. So the `checks` command gained
  `--write-marker`, which writes it only after every variant's smoke case passed, in the tree itself; `Init_Tree`
  asks for it only after the suite passed.
  (b) *The accepted results of a game* are three files: the results, their version ledger, and their verification
  record (`<GAME>_results_master_init_verification.json`). All three must be ordinary files in the source, and the
  results must pass the engine's own reading, before anything is created. The retired opening records
  (`HOLDOUT_OPENED_*`) are not copied.
  (c) *"From PROD, or from DEV while no PROD exists":* a PROD tree exists when the folder DEV's file names holds a
  settings file; it is then checked to be what DEV's file says, and is not read while an install is unfinished
  there or a results update holds its lock. Each source file is hashed before the copy and again after it.
  (d) *A QA tree's own `[results] copy_from`* is PROD's folder as DEV's file names it, also before PROD exists; a
  QA tree created while DEV's file has no `[PROD]` section gets no `[results]` section, and the owner adds it by
  hand when PROD exists (design 1: "to change a setting later").
  (e) *The recovery kit is attempted before the list and the log line,* not after them as step 8 lists, so that
  an answer of NO to "finish without a kit" leaves nothing of step 8 written. The barrier is still removed last.
  (f) *A continued creation asks no question* (the owner confirmed this same plan), keeps the results it copied,
  and checks them against `INIT_RECORD.json`. If DEV changed since it began, the plans differ and it is refused
  with both shown; the refusal says that the owner may delete the half-made folder himself and begin anew.
  (g) *The pause for the environment ends with exit code 3,* with the barrier in place.
  (h) *The four environment scripts* (`create_venv.bat`, `install_upgrade_dependencies_into_venv.bat`,
  `activate_venv.bat`, `deactivate_venv.bat`) are now on the manifest's `[files]`, class `other`: a change to the
  owner's dependency script therefore reaches a tree by `Make_Installable.bat INFRA` and `Reinstall_Infra.bat`.
- **C-R14, readings taken in `Install`** (design 5).
  (a) *A helper the target holds with other bytes refuses the whole command,* before any backup, naming the helper
  and the variants that list it, and saying that the others can be installed by naming them after `--only`. It is
  not one more "left out" reason: design 5 step 1 lists it apart from those.
  (b) *`--only` takes identities,* `<family>/<variant>`, one or more; a name that is no variant folder of DEV
  refuses.
  (c) *Software that does not match the tree's own list refuses before the backup* (design 8, last row), every
  difference named.
  (d) *Step 2 is a look:* the reservation is taken and let go at once (job lock by exclusive create, process
  check, orphan marker, updater's lock, another unfinished operation), because the backup of step 4 is made only
  of a tree whose lock is free. Step 6 takes it again and holds it.
  (e) *A continued install* (its barrier holds this same plan) attempts no new backup or kit and asks nothing: the
  owner said YES to this plan, and a backup of a half-installed tree is no rollback point. It still attempts the
  backup after. If the stop came after the list was written and before the barrier was removed, the list as it
  was before is worked out from the barrier's plan (`list_before`), so that the plan now is the barrier's.
  (f) *The suite at an install* is run only when DEV's infrastructure is marked ready and is file for file the
  tree's; otherwise the line says which, and the install goes on, as specification 12.3 item 3 has it.
  (g) *NO ends with exit code 2;* a backup and a kit may by then exist, and the closing line says so.

## 4. Where it stands

- 25 November 2026: the ratified clauses read (design 2 to 8; specification 12.3); this plan written; no code yet.
  Next: C1. Before coding C1, read what the engine already offers: `src/research/derived_check.py` (the full
  check), `forecast_engine.py` and `reader.py` (how one forecast is computed from a view), `variant_lists.py` (how a
  stored forecast is read), `variant_folders.py` (a variant's declared minimum history and games).
- **Found in the engine, for C1 (25 November 2026):**
  - `reader.ResultsOnFile(game_id, raw, sha256, first_draw, last_draw, version)` is a plain record holding the
    results file's bytes. **The smoke case needs no file:** it builds invented results bytes in memory (header
    `reader.header_for(game)`; one row a draw from the game's first draw, as `tests/research_fixtures.invented_row`
    does with `random.Random` and a fixed seed, `profile.derived_date(draw)`, `profile.barrels[0].high`), checks
    them with `reader.check_results_bytes`, and makes a `ResultsOnFile` of them.
  - `forecast_engine.compute_target(variant, method, results, target)` returns `(content, detail)`; a complete
    forecast is `content['status'] == 'FORECAST'` with `content['barrels']`. The target for a smoke case:
    `reader.first_target(game, <the variant's declared minimum history>)` plus a few draws.
  - `variant_folders.read_variant(methods_folder, family, name)`, `.supports(game)`, `load_method`.
  - The fixed sample: `variant_lists.read_list(path, kind)` gives the stored lines; a stored forecast is
    recomputed with `compute_target` on `reader.results_on_file(tree, game)` and compared by
    `forecast_engine.content_digest`.
  - The derived results in full: `derived_check.first_mismatch(records)` on a game's `GameRecords`
    (`research_job.open_game(job, game)` builds them; see how the job makes its `Job`).
  - The tests' own invented-results generator is in `tests/`, which is not installed in QA or PROD: the smoke
    case carries its own small generator in the infrastructure.

- **25 November 2026, part C1, first half: FINISHED and committed.** New in the overlay:
  `src/research/tree_checks.py` (the smoke case, the forecast sample, the derived results; class `other` on the
  manifest) and `tests/test_trees_checks.py` (27 tests, all pass, with `test_file_form`, `test_research_manifest`,
  `test_research_ov1_and_checks`, `test_trees_snapshot`, `test_trees_readiness`, `test_trees_launch_guard`).
  Changed: `src/research/research_job.py` (`read_game` extracted from `open_game`), `deploy/INFRA_MANIFEST.ini`
  (one line). The whole suite has NOT yet been run on this state, and no planted-fault run has been made.
- **25 November 2026, part C1, second half: FINISHED and committed** (after a resume; section 0's checks were
  made first and found nothing lost: the repository and `origin/main` agreed, the workspace's files equalled the
  overlay's, the 27 tests of the first half passed again). New in the overlay: `src/research/tree_verify.py`
  (`Verify_Tree`, design 7 in its order; class `other`), `src/tree_checks_command.py` (the program: `verify` and
  `checks`), `Verify_Tree.bat`, `tests/test_trees_verify.py` (35 tests at first; see the next item). Changed: `src/research/tree_checks.py`
  (reading game by game; `run_checks`; the `checks` command), `deploy/INFRA_MANIFEST.ini` (three lines). Passing
  with them: `test_trees_checks` (27), `test_file_form`, `test_research_manifest`, `test_trees_readiness`,
  `test_trees_launch_guard`, `test_trees_installed_files`.
- **25 November 2026, part C1 PROVED, with one correction on the way.** The whole suite on the state of commit
  `d2cb640`: 63 modules, 1150 tests; the three known failing tests, and ONE NEW failure,
  `test_research_job.TheResultsStep.test_the_engine_starts_no_program_and_opens_no_connection`: `tree_verify.py`
  imported `subprocess` to start DEV's suite tool. Corrected in the code (section 3, C-Q1): `tree_verify.py`
  starts nothing; `check_dev_folder`, `suite_from_dev` and `--dev` are gone; `tests/test_trees_verify.py` is now
  32 tests (five for the DEV folder removed, one added that no file of the tree's checks starts a program, one
  added by the planted faults). Run again after the correction: `test_research_job` (48, OK),
  `test_trees_verify` (32, OK), `test_file_form`, `test_trees_readiness`. **The whole suite has not been run again
  on the corrected state;** it is run on the slice's final bytes. Planted faults
  (`mutation_check_slice_c1.py`, beside this file): 49 planted in the three new source files, 48 caught at once;
  the one that survived (a fault while a game's records are read, taken for a refusal the job understands) is
  caught by the test added for it.
- **25 November 2026, after the owner's decision of C-Q1 (entry 305):** `tree_verify.py` no longer has a hook for
  a suite; its closing lines always say that the suite is not run by this command. `tests/test_trees_verify.py`
  is 30 tests (all pass, with `test_file_form`); the planted-fault script is brought into step (47 faults; the
  23 planted in `tree_verify.py` and in the program were run again on this state, and all 23 were caught; the
  24 in `tree_checks.py`, which did not change, were caught in the run before).
- **25 November 2026, part C2, first piece: FINISHED and committed: the suite on a temporary copy.** New in the
  overlay: `deploy/SUITE_MANIFEST.ini`, `deploy/suite_on_copy.py` (both on the manifest's `[install_tool]` list),
  `tests/test_trees_suite.py` (15 tests, pass; with `test_file_form`, `test_trees_readiness`,
  `test_research_manifest`). **Proved with the tool itself in the cloud:** `run_suite` on the slice C tree with
  the workspace's Python: a copy of 718 files, 19 modules, 589 tests, all passed, the copy removed; about three
  and a half minutes. Planted faults (`mutation_check_slice_c2a.py`): 17, all caught (one only after a test was
  made independent of the exit code). The whole suite has not been run on this state.
- **25 November 2026, part C2, second piece: FINISHED and committed: the file machinery every install shares.**
  New in the overlay: `deploy/install_common.py` (on the manifest's `[install_tool]` list) and
  `tests/test_trees_install_common.py` (41 tests, pass; the module is on the suite's list). What it holds: what
  DEV offers (`dev_infrastructure`, `dev_variants`: exactly what the two kinds of marker cover); the plan in one
  form (`make_plan`, `plan_lines`); the barrier (`read_barrier`, `check_barrier`, `write_barrier`,
  `remove_barrier`: this install continued, another plan refused with both shown, `--replace-unfinished` only from
  one infrastructure reinstall to another, an operation of build step 4 refused by its name); the copying
  (`copy_into_place`: temporary name, the copy hashed, one rename, no installed file changed unless the plan
  overwrites it; `carry_out`: additions and overwrites, then removals, each passed over if already done);
  `create_status_files`; the tree's software against the plan (`expected_list`, `software_differences`,
  `status_file_faults`); the ending (`log_line`, `finish`: the list, the log line, the barrier removed last).
  Planted faults (`mutation_check_slice_c2b.py`): 37, all caught (two only after tests were added). The whole
  suite has not been run on this state.
- **25 November 2026, part C2, third piece: FINISHED and committed. PART C2 IS WHOLE.** Added to
  `deploy/install_common.py`: `reserved` (the job lock by an exclusive create, the process check under it, the
  orphan marker, another unfinished operation, a held updater's lock); `changing` (the barrier, the updater's
  lock, `SNAPSHOT_DUE`, in that order; the barrier stays if the block fails); `attempt_rollback_point`,
  `question_lines`, `owner_says_yes`; `target_python`; `infrastructure_differences`, `suite_if_it_is_the_trees`;
  `checks_with_target_python` (starts `src/tree_checks_command.py checks` isolated, no time limit, reads its
  result file from a temporary folder outside every tree); `faults_that_stop`. `tests/test_trees_install_common.py`
  is now 69 tests (pass, with `test_file_form`, `test_trees_readiness`, `test_trees_suite`). Planted faults in
  the whole file (`mutation_check_slice_c2b.py`): 73, all caught. **Not yet proved in the cloud: the real start
  of the target's own Python on the `checks` program** (the unit tests stand in for the start; the program
  refuses any Python but the tree's own, and an invented tree's environment is not a Python that runs). It is
  proved with C3, by a creation run end to end on a tree whose `.venv` is a real one. The whole suite has not
  been run on this state.
- **25 November 2026, part C3: WRITTEN and committed; its proof (planted faults; the real start of a tree's own
  Python) is next.** New in the overlay: `deploy/init_tree.py`, `Init_Tree.bat`, `tests/test_trees_init.py` (32
  tests, pass). Changed: `deploy/deploy_command.py` (the word `init-tree`; a reviewed slice A file),
  `deploy/INFRA_MANIFEST.ini` (the four environment scripts under `[files]`; the two new tool files),
  `deploy/SUITE_MANIFEST.ini` (`test_trees_init`; the list is now 21 modules), `src/research/tree_checks.py` and
  `deploy/install_common.py` (`--write-marker`), `tests/test_trees_verify.py` (33 tests). Passing with them:
  `test_trees_suite`, `test_file_form`, `test_trees_readiness`, `test_research_manifest`,
  `test_trees_install_common` (69), `test_trees_check_tree`, `test_trees_installed_files`, `test_trees_checks`.
- **25 November 2026, part C3 PROVED in the cloud.** Planted faults (`mutation_check_slice_c3.py`): 39 in
  `init_tree.py` and in the marker's writing; 36 caught at once, the other three by tests added for them
  (`tests/test_trees_init.py` is now 34 tests). **The real start of a tree's own Python, which the unit tests
  only stand in for, was made in the cloud** (`slice_c/evidence/cloud_creation_*`): a creation run from the slice C
  tree with its REAL software, to its pause (infrastructure and all 40 real variants marked and planned; 168 files
  copied, 40 status files, the six results files); the same command again (168 already in place, the results
  kept by their record); then a real Python environment built inside that tree and
  `install_common.checks_with_target_python` started on it for real: the `checks` program ran isolated under the
  tree's own Python, **every one of the 40 real variants gave a complete forecast for both games on the invented
  table with exactly its declared minimum history (80 smoke cases, about ten seconds),** nothing was left in
  `scratch`, and the same call with another Python was refused by the program. **Not provable in the cloud, kept
  for the Windows rehearsal:** the second half of a creation with a real environment (the marker's digest takes
  the Windows layout `Scripts` and `Lib\site-packages`), `python.exe` by its Windows path, the launcher, and the
  whole suite run by the tool with a tree's Windows Python. The whole suite has not been run on this state.
- **25 November 2026, part C4: WRITTEN and committed; its planted faults are next.** New in the overlay:
  `deploy/install.py`, `Install.bat`, `tests/test_trees_install.py` (28 tests, pass, with `test_trees_suite`,
  `test_file_form`, `test_trees_readiness`, `test_research_manifest`, `test_trees_init`). Changed:
  `deploy/deploy_command.py` (the word `install`), `deploy/INFRA_MANIFEST.ini` (two tool lines),
  `deploy/SUITE_MANIFEST.ini` (`test_trees_install`; 22 modules).
- **25 November 2026, part C4 PROVED.** Planted faults (`mutation_check_slice_c4.py`): 31 in `install.py`; 30 caught
  at once, the last by a test added for it (`tests/test_trees_install.py` is now 29 tests). The whole suite has
  not been run on this state.
- **NEXT: C5, `Reinstall_Infra.bat QA|PROD [--replace-unfinished]`** (design 6, eleven steps; specification 12.4).
  What it needs, so that a chat that resumes can begin at once:
  - *Read first:* specification 12.4 in full (the warning's exact text and the one question); specification 5.8
    (the cutoff file `NOT_CURRENT_FROM.json`, moving stale reports out); `src/research/derived_check.py`
    (`write_cutoff`, `settle`, `read_cutoff`), `src/research/reports.py` (how the league report, the next-draw
    report and the OV-1 print-out are made, for step 9's "made again with the new code"), and how the research
    job moves stale reports out when it marks a game not current.
  - *Step 1, the plan:* the difference between DEV's manifest files (`install_common.dev_infrastructure`) and the
    target's infrastructure on its list: add, overwrite (both hashes), remove, each with its class; the text
    differences shown; no path under a family folder or `_shared`; no difference ends; **any `forecast`-class
    file in the plan refuses** ("this changes code that makes forecasts: use `Correct_Shared_Code.bat`").
  - *Step 3, before anything is overwritten:* the software as it would be, assembled in a temporary folder (the
    target's installed files with the plan applied); with the target's Python: the suite
    (`suite_if_it_is_the_trees`, which is DEV's by construction), then `checks_with_target_python(python,
    <temporary folder>, <tree>, NO_VARIANT, sample=True, derived=True)`. A sample difference is a fault and
    stops. The statement: "No stored result changes", or "This changes stored scores or OV-1 lines, for <game>
    from draw X". It goes into the plan (`statement`) and the barrier.
  - *Reading C-R9* for the lock around steps 3 to 6.
  - *Steps 6 to 10* with `install_common` (`reserved`, `check_barrier(..., replace_unfinished)`, `changing`,
    `carry_out`, `software_differences`, `finish`); step 9's smoke case of every installed variant, the suite,
    and the derived results: agree again where nothing was foretold; where a change from X was accepted, write
    the cutoff for X, move the stale reports out, and check that this was done; if a `derived`-class file was in
    the plan and the results agree, make every report again.
  - *Step 11:* `POST_INFRA`; if a change from X was accepted, name the command owed:
    `Rerun_Walk_Forward.bat --game <game> --from <X> --derived-only`.
  - *`--replace-unfinished`:* shows the unfinished plan and the new one and asks the same question.
- **Workspace (a convenience only):** LF copies of slice C's new files are in `/home/claude/work/slicec/`, and
  `/home/claude/work/fix/wire_c1.py` copies them into the overlay as CRLF and makes the edits of reviewed files
  through `fix/ed.py` (now also `tree_verify.py`, `tree_checks_command.py`, `Verify_Tree.bat`,
  `test_trees_verify.py`). If the workspace is gone, take the overlay's files (strip the CR) and go on.
- **Seen, to carry into the joined package (not slice C's):** Python 3.15 warns on
  `src/research/environment_marker.py` line 17, a docstring that holds `Lib\site-packages` with a single
  backslash ("\s" is an invalid escape sequence; a SyntaxWarning now, an error in some later Python). One
  character to double, in a file slice A reviewed.

## 5. Costs on the owner's PC, to be told plainly when the slice is put to him

- `Init_Tree` and `Reinstall_Infra` run the new system's suite (19 modules, not the first system's tests) with the
  target's Python on a temporary copy: about three and a half minutes in the cloud; the owner's PC's own figure
  comes from the rehearsal. `Verify_Tree` does not run it (entry 305).
- Every install is preceded and followed by a whole backup of the target (slice B's cost, twice).
- An infrastructure reinstall recomputes every score and the whole prevailing ledger twice (before the question, and
  after the overwrite).
