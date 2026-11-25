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
- **C-Q1, OPEN, FOR THE OWNER: where `Verify_Tree.bat` finds DEV's tests.** Design 7 has `Verify_Tree.bat` run in
  the tree and run "the suite, if the tree's infrastructure is file for file DEV's". A QA or PROD tree's settings
  file does not say where DEV is (design 1), and the tests live only in DEV. Three ways: (a) the owner names DEV
  when he wants the suite, `Verify_Tree.bat --dev <DEV's folder>`; nothing stored, no ratified text touched;
  without it the suite is not run and the summary says so in capitals; (b) a `[dev]` line in the tree's own
  settings file, written by `Init_Tree` (a one-line amendment of ratified design section 1, and a change to slice
  A's reviewed settings reader); (c) DEV's folder kept in `records/INIT_RECORD.json` (cannot be corrected by hand if
  DEV moves). In every one, a tree must be verifiable with no DEV on the PC (after a restore onto a new PC), so
  an absent DEV can never refuse. **Built so far: (a),** the recommendation; another answer changes only how
  `tree_verify.main` learns the folder. The folder named is checked: its own settings must say DEV and name this
  tree for this tree's role.
- **For part C2, fixed here:** the tree asks DEV's tool `deploy/suite_for_tree.py --tree <tree root>`, started with
  the tree's Python (`-I -B -u`, no time limit). Its exit codes: 0 the suite passed; 1 it failed; 3 not run, because
  DEV's infrastructure is not file for file this tree's (the tool says which files); anything else counts as
  failed. The tool is not written yet.

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
  `checks`), `Verify_Tree.bat`, `tests/test_trees_verify.py` (35 tests). Changed: `src/research/tree_checks.py`
  (reading game by game; `run_checks`; the `checks` command), `deploy/INFRA_MANIFEST.ini` (three lines). Passing
  with them: `test_trees_checks` (27), `test_file_form`, `test_research_manifest`, `test_trees_readiness`,
  `test_trees_launch_guard`, `test_trees_installed_files`. **Part C1 is whole except for one thing that belongs to
  C2:** DEV's tool `deploy/suite_for_tree.py` (section 3 fixes how the tree asks it). The whole suite and the
  planted-fault run for C1 are made next; their result is added here.
- **Next: C2** (what every install shares), beginning with the suite on a temporary copy (`suite_for_tree.py`),
  for which the first thing to settle is what the temporary copy holds (which of DEV's files the tests need).
- **Workspace (a convenience only):** LF copies of slice C's new files are in `/home/claude/work/slicec/`, and
  `/home/claude/work/fix/wire_c1.py` copies them into the overlay as CRLF and makes the edits of reviewed files
  through `fix/ed.py` (now also `tree_verify.py`, `tree_checks_command.py`, `Verify_Tree.bat`,
  `test_trees_verify.py`). If the workspace is gone, take the overlay's files (strip the CR) and go on.
- **Seen, to carry into the joined package (not slice C's):** Python 3.15 warns on
  `src/research/environment_marker.py` line 17, a docstring that holds `Lib\site-packages` with a single
  backslash ("\s" is an invalid escape sequence; a SyntaxWarning now, an error in some later Python). One
  character to double, in a file slice A reviewed.

## 5. Costs on the owner's PC, to be told plainly when the slice is put to him

- `Init_Tree` and `Reinstall_Infra` run the whole suite with the target's Python on a temporary copy (about ten
  minutes in the cloud; the owner's own figure on Windows is in his install reports).
- Every install is preceded and followed by a whole backup of the target (slice B's cost, twice).
- An infrastructure reinstall recomputes every score and the whole prevailing ledger twice (before the question, and
  after the overwrite).
