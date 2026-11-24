"""The new words of H-1 v10: every passage that replaces or joins a passage of H-1 v9.

What this file is for
    make_h1_v10.py builds H-1 v10 from the installed H-1 v9 by counted replacements. This file holds only the
    words: HEADER, the whole-section texts, and SMALL, the list of short replacements. `@@SHA:<path>@@` in a text
    is filled by the builder with the SHA-256 of that file's Git content at HEAD, so no hash is typed here.

Which part of the specification it carries out
    None; H-1 is the Claude chat's handover (agreed roles position v0.1r1, section 9 item 4).

Which of the project's own modules it uses
    None.

What uses it
    make_h1_v10.py, beside it.
"""

HEADER = r'''# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v10

**Document:** H-1 under the agreed roles position v0.1r1, section 9 item 4.
**Version:** v10, 24 November 2026 (Adelaide, UTC+10:30). **H-1 v9 brought up to date** after build step 2 (the
research engine) was reviewed, rehearsed on Windows, installed in DEV and run, as the owner agreed (decision log
entries 183 and 213). Built from the installed H-1 v9's Git bytes by `exchange/CLAUDE_WEB_TOOLS/h1v10/make_h1_v10.py`,
with counted replacements; `H1_v9_TO_v10.diff` beside it is the exact difference. **Sections 1, 2 and 2A are still
H-1 v7r1's bytes, unchanged** (the builder asserts it against v9). The sections rewritten are listed in Appendix B;
everything else is v9's text.
**Status:** CANDIDATE, 24 November 2026, for the reviewer's review and the owner's ratification (RAT-45). Until it
is ratified, H-1 v9 (RAT-43) is the installed Claude handover, and `exchange/CONTINUITY_NOW.md` with the decision log
carries whatever is newer. It authorises nothing.
**Audience:** any later Claude chat that takes over as primary designer and coder; the ChatGPT reviewer chat; the
project owner.
**Repository:** `hydra3333/analysing_perceived_randomness_in_reality`, public GitHub, branch `main`.
**Baseline described:** `main` on 24 November 2026 after build step 2's install (`5f16b35`) and its record (entry
212). **The new system's research engine is installed in DEV and has run** (`src/research/`, the program
`src/research_command.py`, the launchers `Run_Research.bat` and `Withdraw_Variant.bat`). The old system's code is still
there beside it, unchanged. The trees QA and PROD, the installs, the backups and the laboratory tools are not coded.
**Replaces:** H-1 v9 and its blurb (RAT-43), which stay where they are as history.
**Authority:** the ratified documents and the decision log prevail over this handover wherever they differ. This file
summarises and points to them.
**Draw values:** none appear in this file.
'''

STATE_ITEMS = r'''8. **Build step 2, the research engine, is INSTALLED in DEV and has run** (the owner's go, entry 176; entries 176 to
   212; `main` `5f16b35`, 24 November 2026). A new package `src/research/` beside the old system, which is not edited: the lists, the job
   (`Run_Research.bat`: start, fill, results, catch-up, end), scoring, the reports, both OV-1 scores, each variant's
   status file and the withdrawal (`Withdraw_Variant.bat`). Reviewed in four rounds: EX_283 (two crash-recovery
   blockers), EX_285 (one, in the first correction), EX_290 PASS, and EX_294 PASS for package v1r3, which changed one
   tool. The package is `STEP2_Research_Engine_v1r3` (`exchange/CLAUDE_WEB_TOOLS/step2/package_v1r3/`); its note is
   `STEP2_PACKAGE_NOTE_v0_3.md`. **On the owner's PC:** the install sheet's parts 1 to 4 (`PRE`, `POST` and
   `COMMITTED PASS`; the suite 571 tests before and 762 after, every old test with the same result); DEV's first
   fill of both games in 47 minutes (Powerball 15,118 forecasts and 15,078 scores; Oz Lotto 6,598 and 6,558); a
   second job with nothing to do in 3 minutes; and the comparison with the old records **`RESULT: PASS - COMPLETE`**:
   all 34,800 old score records and all 20,436 forecasts the old development runs kept are in the new lists with
   the same view digest, scores, ranking, TOP and WORST. Section 7 has what exists; section 7.5 what has not run.
9. **Before the install, a rehearsal on Windows by the local runner** (TASK_T025, T026 and T027; entries 199 to 208),
   in a task clone and in a scratch tree under `D:\DELETE_ME\`, under **the runner's rulebook v0.7** (RAT-44, entry
   192; section 8.6). It found three things where nothing real could be harmed: the runner's shell has the main
   `.venv` active, so a tree's own `.venv` is built from a plain CMD window; a fault in Claude's comparison tool
   (corrected in package v1r3); and the time of a first fill.
10. **The owner's decisions for build step 3, already given** (entries 180 and 181; 23 November 2026): no parallel
    or multi-threaded runner now; the results updater as a **clean-sheet new edition** (`results_master_v0_3.py`: every
    Mode H state removed, every genuine source, parse, overlap, chronology, ledger and lock check kept and proved
    unchanged, `v0_2` left untouched in DEV), to be put to the reviewer, whose stated preference was narrower; line
    endings pinned to LF for the project's code in `.gitattributes`, in step 3, before the first tree is made; the
    places: PROD `G:\a_p_r_i_r`, QA `T:\a_p_r_i_r`, backups `T:\a_p_r_i_r_backups\PROD` and `\QA`; rehearsals as Claude
    chooses, the runner in the scratch folder on D:.
11. **What is authorised now:** documents and records. Build step 3 needs the owner's own go (section 10); so does
    every install and every run on his PC.
12. **What is owed** is listed once, in section 12.8.
13. **The chats.** This Claude chat took over on 22 November 2026 from H-1 v8 (HO-2 accepted, entry 157) and did build
    step 1, the tidy-up and build step 2. A new ChatGPT reviewer chat took over from H-2 v5r1 on 23 November 2026
    (entry 175) and reviewed EX_282 to EX_294. The owner has not decided on a Claude chat switch; this edition is written so that one
    can happen at any time (the chat is long).

'''

INSTALLED_CODE = r'''- **The research engine of the new system** (build step 2, `5f16b35`): the package `src/research/`, 20 files; the
  program `src/research_command.py` behind both launchers; `Run_Research.bat` and `Withdraw_Variant.bat` in the root;
  `deploy/INFRA_MANIFEST.ini` (the 32 infrastructure files in three classes: forecast 13, derived 16, other 3);
  `ENVIRONMENT.example.ini`; seven test modules `tests/test_research_*.py` with `tests/research_fixtures.py`. The
  install added 33 files and changed two (`.gitignore`, and one list in `tests/test_mhupa_master_versions.py`).
  **It imports the old system's shared files and does not change them.** What each module does, and the choices made
  in it, are in `exchange/CLAUDE_WEB_TOOLS/step2/STEP2_PACKAGE_NOTE_v0_3.md`; every file's own header says what it is
  for. In short: `variant_lists.py` (the two chained, append-only lists per variant per game), `code_identity.py` and
  `variant_folders.py` (the two header identities), `forecast_engine.py` and `reader.py` (one forecast from the N-1
  view), `scoring.py`, `game_state.py`, `research_job.py` (the job; fill and catch-up are one function,
  `complete_draw`), `derived_check.py` (the check of specification 5.8 and the marker `NOT_CURRENT_FROM.json`),
  `ov1_numeric.py` and `ov1_ledger.py`, `reports.py` (made again in memory at every job, written only when the bytes
  differ), `status_file.py`, `withdraw.py`, `settings.py`, `job_lock.py`, `results_step.py`.
- **A tree's settings are `ENVIRONMENT.ini`,** beside the launchers; Git ignores it. In DEV the owner made it by
  copying the example (entry 212). The launchers refuse without it, and refuse a Python that is not the tree's own
  `.venv`. **The example's comments mislead and its commented paths are out of date** (the owner's observation,
  entry 211): it is rewritten in build step 3.
- **Everything else** under `src/` and `tests/`, the root `.bat` files and `requirements.txt` is the old system, as at
  `cc0ab73`, apart from step 1's changes named above and the lines it changed in 14 test files for the moved paths.
- **The suite's known result** (owner's PC and cloud, 24 November 2026): **52 modules, 762 tests** (the old 45
  modules and 571 tests, and the engine's 7 modules and 191 tests); **three tests fail, with eight failed
  assertions**, on `main` since before step 1: `test_mhupa_launchers` `test_gitignore_lines` (one; it prints a set, in
  a different order each run) and in `test_multigame_reader_contracts` `test_master_source_and_ledger_file_hashes`
  (two sub-tests, pinned to the version-1 masters) and `test_only_legacy_e1_allowed_at_boundary` (five). On Windows
  the old symlink tests skip (section 6), and two of the engine's link tests skip where the account cannot make a
  symbolic link; its three folder-link tests then run with a junction. Compare before and after with
  `compare_suite_reports.py` (section 12.2), test by test. The two suite runs take about 25 and 29 minutes on the
  owner's PC.
'''

DEV_RESULTS = r'''- **DEV's research results** (24 November 2026; ignored by Git, on the owner's PC only): `results\research\<GAME>\`
  with `variants\<family>\<variant>\forecasts.jsonl` and `scores.jsonl`, the reports under `reports\` (start with
  `README.txt`), and `records\`. Forty variants in each game. A list begins at its variant's `first_target` and holds
  no line before it (specification 5.2). **The prevailing OV-1 has not started in DEV** and cannot until a tree
  exists to copy accepted results from (build step 3); the job says so at its end. The cloud workspace's own fill
  gave the same counts; it is suggestive only and is gone with the workspace.
- **Of the old development records, 2,802 in each game are not forecasts:** the old system kept a record
  `INSUFFICIENT_HISTORY` for each target at which a variant did not yet have enough earlier draws. The comparison tool
  counts them apart (entries 205 to 208). The old system therefore kept 14,478 Powerball and 5,958 Oz Lotto
  development forecasts, and all of them are in the new lists.
'''

NOT_TESTED = r'''### 7.5 What has run, and what has not been tested by anyone

**Has run on the owner's PC, from reviewed programs:** the research job in DEV, twice (a first fill and a job with
nothing new), and the engine's 191 tests; in a scratch tree, the same, and `Withdraw_Variant.bat --help`.

**Has not run anywhere but in the engine's own tests, on invented data:** a job with a new draw on file (a real
catch-up); the results step (DEV has no tree to copy from); the prevailing OV-1 ledger on real results; a
withdrawal; a crash and its resume on Windows (a planted interruption would mean ending a process, which the owner's
rules forbid; the tests cover it); a held variant; the marker `NOT_CURRENT_FROM.json`.

**Known limits of build step 2, recorded in its note (section 9):** until build step 4 no command clears a held
variant or a `MISMATCH` (in DEV the interim is to delete the untracked `results\research\` by hand, on the owner's
word, and fill again); a job that is killed leaves its lock file, which the owner deletes by hand after reading what
the launcher says; an interrupted withdrawal of several variants leaves the first withdrawn (run it again without
that one); the guard against linked working folders covers five named folders and one writer under the job lock,
no more (EX_290).

**Nothing of the trees, the installs, the backups, the restore or the laboratory tools has been coded or run.** The
specification's section 20 and the deployment design's section 17 list the uncertainties; the costs still to
measure are a `Check_Forecasts --all`, a historical walk-forward rerun, and a backup of a whole tree with its
environment. Measured so far, on the owner's PC: a first fill of both games 46 to 47 minutes (nearly all of it inside
the methods' exact-fraction fits, E_3, E_4 and E_18); a job with nothing new 3 minutes; the comparison with the old
records 2 minutes.

---

'''

RUNNER = r'''### 8.6 The Claude Code local runner

- **What it is:** Claude Code on the owner's Windows PC carries out task files that Claude writes and reports what
  happened. Its rulebook is `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`, **v0.7 (RAT-44, entry 192; its version line
  corrected in entry 195)**. Its reports are owner-machine evidence, not reviewer evidence and not acceptance.
- **Rulebook v0.7 adds section 2A, the scratch folder `D:\DELETE_ME\`** (reviewed in EX_286, EX_287 and EX_289), and
  changes nothing else of substance. Only when a task file says "section 2A": anything under `D:\DELETE_ME\` may be
  created, read, changed and deleted; real results may be copied in by reading and used there; the new system's
  commands may be run against a tree whose root lies there; a scratch tree's own `.venv` may be built with that
  tree's own two scripts. Nothing leaves the scratch folder but the report and the text a task file names to be
  copied into it. **Never, even there:** the results updater, any scraper, the old coordinator and its launchers, a
  push, the PC's clock, ending a process. The owner's real QA and PROD trees and their backups stay out of reach
  without exception (rule 11). Rule 10 has one exception, which a task file must state: the suite's known failing
  tests, named one by one. A scratch run is a rehearsal, never a result of the project.
- **The owner's `.claude/settings.json` is his file.** On 23 November 2026 he removed two deny lines from it, the ones
  that matched every `.bat` and the dependency script (entry 197), so that a scratch tree's launchers can be typed.
  Its other deny lines stand: every delete, every push, `pip`, the updater, the old launchers and more. So a task
  cannot delete: the owner deletes a scratch folder himself. Its `Read` lines for `results` and `source_data` bind
  the runner's own file tools under the repository; they did not stop a Python command that copies those folders.
- **How a task runs:** Claude writes `inbox/TASK_Tnnn.md` with every command in full, the expected line of each step,
  a clean-up step and a report step, and commits it. The owner pulls, starts a **new** Claude Code conversation
  (a running one keeps the rulebook it started with) and types `Do inbox\TASK_Tnnn.md`. The runner commits
  `outbox/REPORT_Tnnn.md`; the owner pushes; Claude reads the report from GitHub. A STOP is a STOP. To check that the
  runner has the right rulebook, the owner asks it which version and ratification number it works under and what
  its section 2A allows (entry 201).
- **The runner's shell is Git Bash inside VS Code, and it has the main `.venv` active** (`VIRTUAL_ENV` is set). The
  project's `create_venv.bat` and dependency script refuse then, as they are written to (TASK_T025's stop). **A
  tree's `.venv` is built by the owner from a plain CMD window.** A `.bat` started from Git Bash by its full path
  does run and returns its own exit code.
- **The three tasks of 23 and 24 November 2026** are the worked example (section 12.4): TASK_T025 (the install
  sheet's parts 1 to 4 in a task clone, then a scratch tree; stopped at the `.venv`), T026 (the launchers, the first
  fill and the comparison; stopped on the comparison tool's fault) and T027 (the corrected comparison; PASS). The
  reviewer cold-read T025 (EX_291 asked four corrections of its text; EX_292 PASS); the owner ran T026 and T027 on
  his own go without a further look. T001 to T024 are in H-1 v7r1 section 8.6.
- **The owner favours running heavy, repeatable things there** (test suites, rehearsals), because they cost few
  tokens. Let that guide what goes to the runner. Never ask the runner to judge: give the exact expected lines and
  numbers, and say that anything else is a STOP.

'''

LESSONS = r'''**From build step 2 (23 and 24 November 2026):**

- **A path that cannot be run where you work is the path that fails.** Three faults of this step were in code written
  with care and never executed: a crash point between two writes (EX_283), a cleanup that deleted what it had not
  checked (EX_285), and a comparison against records that exist only on the owner's PC (TASK_T026). **Make the
  unrunnable runnable first:** build made-up records in the real form (`check_compare_tool.py` did, afterwards, and
  reproduced the owner's output number for number), and plant the interruption in a test.
- **A correction can carry a new fault.** Both EX_285's blocker and the stale folder in package v1r3's sheet came in
  with a correction. For every new `unlink`, `replace` or `truncate`, ask what it could reach if its assumptions were
  false; after renaming a package, search every text for the old name (the builder now refuses a sheet that names
  another package).
- **"This is not a STOP" is never written to save a round trip.** TASK_T025's first text did it twice and the
  reviewer caught both (EX_291). A refusal, an error or an unexpected number stops the task.
- **Require the exact numbers, not only PASS.** TASK_T027 required every count; a bare PASS would not have told a
  right explanation from a tool that now forgave too much. Take the numbers from a tool's output, never from memory.
- **Never type a hash; never type a time.** A hash is computed by the builder or the assembler. A decision log
  heading's time is read from the clock in the command that writes it (entries 192 to 194 carry estimated times,
  corrected in entry 195).
- **Look at the count of changed lines before every commit** (`git diff --cached --numstat`). A script once wrote
  three CRLF files back as LF and Git showed nearly every line changed (entry 193). Section 0A item 12.
- **Push nothing while the owner is in the middle of an install.** A record pushed then put GitHub one commit ahead
  of his uncommitted tree and cost him a pull and his trust in his local Git (entry 210). When he doubts his
  repository, give read-only checks with the exact expected output, not reassurance.
- **A sheet says what must exist before it starts, and its builder checks every path.** The install met a baseline
  folder that had been deleted and a command that named the old package (entries 209, 210).
- **Fetch immediately before taking an EX number.** The reviewer took EX_287 while a message of that number waited
  (entry 189).
- **State what a claim rests on.** The cause of TASK_T026's stop was called an inference, with its arithmetic, until
  the corrected tool had read the real records; the reviewer asked for exactly that (EX_294).

'''

NEXT_WORK = r'''## 10. Next work, in order (planned; the owner decides each step)

1. **Done:** H-1 v8, H-2 v4 and register v0.32 ratified (RAT-41); rulebook v0.6 (RAT-42); the takeover of this chat
   (entry 157); **build step 1** (entry 164, `0aea10a`); **the light tidy-up** (entry 169, `c7e6ed8`); H-1 v9 and
   H-2 v5r1 (RAT-43, entry 174); the runner's rulebook v0.7 (RAT-44, entry 192); **build step 2** (entries 176 to
   212, `5f16b35`).
2. **This edition:** to the reviewer, then the owner's ratification (RAT-45).
3. **Build step 3: trees, installs, backups and restore** (specification 12.1 to 12.6, 13, 14.1), then the transition
   check and PROD's first job, on the owner's own go. **Already decided by the owner** (section 0B item 10): the
   updater as a clean-sheet new edition, put to the reviewer before it is coded; LF pinned in `.gitattributes` before
   the first tree; the places on G: and T:; no parallel runner. **To settle or carry in that package:** the rewrite
   of `ENVIRONMENT.example.ini` (entry 211); that `Init_Tree.bat` stops for the owner to build the tree's `.venv` from a
   plain CMD window; rehearsals by the runner in scratch trees under `D:\DELETE_ME\`, each tree with a rehearsal role;
   the measurements of section 7.5. The old run folders stay until the transition check (section 7.2). **After this
   step PROD exists and forecasts every week, and new methods can be added: the main game.**
4. **Build step 4: the laboratory tools** (specification 12.7, 14.2, 7A, 12.8, `Check_Forecasts`), with the test of
   EX_271 section 3. Until it is built, a fault found in shared code is not improvised around: the affected work is
   held, or the owner restores a backup (specification 17.4); build step 2's limits in section 7.5 apply.
5. **The operations manual, after build step 3** (the owner, entries 171 and 182): its skeleton is agreed with the
   reviewer first. It must say what is and is not overwritten (an install never overwrites; shared code is
   corrected in place only by `Correct_Shared_Code.bat`; a variant's own files never, a corrected method is a new
   variant name) and how the markers and flag files work (`I_AM_INSTALLABLE.json`, `ENVIRONMENT_VERIFIED.json`, the
   status file, the job lock, the install barrier, the not-current marker).
6. **Then, in the owner's order:** new methods and waves; OUTLANDISH_01's family; the housekeeping of section 12.8.

**The updater and Mode H (the watchpoint of H-1 v9, now decided).** The installed code still has checks from the
Mode H study that the ratified design does not make a gate: `src/methods/_common/contract_dispatch.py` and
`master_versions.py` consult the opening record `source_data/HOLDOUT_OPENED_<GAME>.json`, and the updater
`src/results_master_v0_2.py` refuses an update for a game that has none. The reviewer preferred a narrow correction
that removes only that precondition. **The owner chose a clean-sheet new edition** (entry 181; section 0B item 10).
Put it to the reviewer as the owner's decision, with the proof that every genuine check is kept. Fresh trees must
work with no Mode H opening or seal as a prerequisite; the obsolete record is not copied into a new tree to satisfy
old code; no genuine source or ledger check is removed.

**Models (MC-1; suggestions, the owner decides):** Opus for packaging, sheets, task files, records and handovers.
**Fable (High) for the state machines of step 3** (the install and its barrier, the backup, the restore), for the
rerun and correction steps of step 4, and for any unexplained STOP. Cold reads before a review round may be helpers
on Opus. The owner switches models himself; say when a Fable task is finished.

'''

TASK_FILES = r'''### 12.4 Claude Code task files

As practised for TASK_T025 to T027 (`inbox/`, with their builders in `exchange/CLAUDE_WEB_TOOLS/t025/`, `t026/`, `t027/`):

- **Build the task file from a template** in which each long path is defined once; write it with CRLF, as the
  other task files are. Check before committing: every Python one-liner compiles; the steps are numbered in order;
  no command holds a word the owner's settings deny (for example `results_master`, `pip`, `conda`, `rmtree`); every
  D: path lies under `D:\DELETE_ME\`. `exchange/CLAUDE_WEB_TOOLS/check_task_commands.py` is the older check.
- **Each step gives the exact command, the exact expected lines and numbers, and what is a STOP.** A long step
  writes its output and its own exit code into a file (`...; echo "EXIT CODE $?" >> file`) and runs in the background;
  the task then shows named parts of the file. Say what the runner may add to a task line (`cd`, an `echo` of the
  exit code, `date +%H:%M:%S` in Git Bash) and nothing else. `grep -c` exits 1 when its count is 0: say so.
- **A section 2A task** names its folder, checks first that `D:\DELETE_ME` is an ordinary folder, never deletes, and
  says which text may be copied into the report. Lines that may show numbers drawn are counted, never copied.
- **A task that follows another** takes its commands from the earlier, reviewed task by its builder, which asserts
  that they are the same, character for character (T026).
- Read the whole report: every step's command, exit code and output, and its Deviations and Observations.

'''

OPEN_ITEMS = r'''### 12.8 Open items at this edition (24 November 2026)

The live state is `exchange/CONTINUITY_NOW.md`; it overtakes this list.

- **Waiting on the reviewer:** its review of this candidate.
- **Waiting on the owner:** RAT-45 for this edition; his go for build step 3; his word on reminders R-007 (proposed
  dropped) and R-017 (proposed done) (entry 155).
- **Owed by Claude, in order of need:**
  1. Build steps 3 and 4, each on its go, with what section 10 says each must settle.
  2. The clean-sheet updater put to the reviewer as the owner's decision, before it is coded (section 10).
  3. The rewrite of `ENVIRONMENT.example.ini` (entry 211) and the LF pin in `.gitattributes`, in build step 3.
  4. The test of EX_271 section 3, in build step 4.
  5. The next register edition, when a code package or a handover next travels (section 1.6): it records RAT-41's
     install, RAT-42, RAT-43, RAT-44, build steps 1 and 2, the tidy-up and what follows.
  6. The operations manual's skeleton, agreed with the reviewer, after build step 3 (section 10 item 5).
  7. A new draft of `doc/METHOD_TEMPLATE/` for the new layout, after build step 3.
  8. The measurements still open in section 7.5.
  9. The reviewer's handover: H-2 v5r1 describes the state before build step 2; the reviewer writes its own.
- **Done since H-1 v9:** build step 2, reviewed, rehearsed, installed and run (section 0B items 8 and 9); the narrow
  rulebook amendment (v0.7, RAT-44); the owner's answer on the updater (entry 181).
- **Later, and only when the owner asks:** the deferred performance study (R-006;
  `doc/Deferred_Performance_Engineering_Proposal_v0_1.md`: profile real run times before choosing any speed-up; a
  first fill's time is inside three families' exact-fraction fits) and the simplicity review after full
  implementation (KISS-1).
- **Small leftovers the owner may choose to clear:** the scratch folder `D:\DELETE_ME\a_p_r_i_r\T025` and
  `E:\TEMP\STEP2_baseline_clone` (no longer needed, entry 212); deleting `venv.bak` and Python 3.14; the duplicate
  exploration note in `doc/`; the old EX copies in `review/`; after step 3's transition check, the old run folders.

'''

APPENDIX_B = r'''## Appendix B. What changed from H-1 v9

### B.1 What changed from H-1 v9

| v9 section | In v10 |
|---|---|
| Header | rewritten for the state after build step 2; status CANDIDATE |
| 0 First actions | item 2: the newer entries, build step 2's note and the reviewer's findings on it added to the reading list; the rulebook's edition |
| 0A Things that trip a new chat | item 1: the research engine is installed; item 3: the newest numbers; items 12 to 15 added (CRLF record files and the changed-line count; no push during an install; the reviewer takes EX numbers; the old system's insufficient-history records) |
| 0B The state | heading's date; items 1 to 7 kept; items 8 to 10 replaced by items 8 to 13 (build step 2; the rehearsal and rulebook v0.7; the owner's decisions for step 3; what is authorised; what is owed; the chats) |
| 0C Notes on sections 1, 2, 2A | item 2: rulebook v0.7 |
| 1, 2, 2A | **carried byte for byte** (still H-1 v7r1's bytes) |
| 2B, 3, 4, 5, 6, 8.1 to 8.5, 8.7, 9, 11, 12.1, 12.5, 12.9 | unchanged |
| 7.1 The installed code | the research engine, the settings file and the suite's new known result (52 modules, 762 tests) |
| 7.2 Data and records | two items added: DEV's research results; the old insufficient-history records |
| 7.3 Staged work | one sentence: the OV-1 kernel is carried into `src/research/` byte for byte |
| 7.4 The build's record | `step2/`, `rulebook_v0_7/` and the three task folders added |
| 7.5 Not tested | rewritten: what has run, what has run only in tests, build step 2's known limits, what is still to measure |
| 8.6 The local runner | rewritten: rulebook v0.7 and its section 2A, the owner's settings change, the runner's shell, the three tasks |
| 8.8 Lessons | ten lessons from build step 2 added at the top; the rest unchanged |
| 10 Next work | rewritten: step 2 done; step 3 with the owner's decisions; the operations manual; the updater decided |
| 12 intro, 12.2, 12.3, 12.6 | brought up to date (the step 2 tools; what step 2 added to building a package; the owner's places, his scratch folder and the measured times) |
| 12.4 Task files | rewritten as the practice of TASK_T025 to T027 |
| 12.8 Open items | rewritten |
| Appendix A | rebuilt from HEAD: v9's files with their hashes computed again, H-1 v9 in place of H-1 v8, and the files a new chat now needs |
| Appendix B | this one |

Nothing binding was dropped: every v9 passage that was replaced described a state that has since moved on, and the
decision log entries 175 to 213 hold the record.

### B.2 Known limits

- **Verified with tools for this edition:** every hash in Appendix A (computed by the builder from `HEAD`); that
  sections 1, 2 and 2A equal v9's bytes; that every replacement's old text is found exactly once in v9; the counts
  and times of section 0B item 8 and section 7 (the owner's unedited console outputs and the runner's three reports).
- **Not re-checked for this edition:** the hashes written in sections 4.2 and 4.3 (v9's text, unchanged files);
  statements about the owner's PC other than those in his outputs and the runner's reports; H-2 v5r1, which is the
  reviewer's.
- **Written by the chat that did the work,** late in a long conversation: the reviewer's cold read of this edition
  against the repository is the check on it.

### B.3 Integrity

US-ASCII; LF; one final newline. The carried sections 1, 2 and 2A are identical to H-1 v9's (the builder asserts
it). Every replacement's old text is found exactly once in H-1 v9. The builder refuses on any failure.

End of H-1 v10.
'''

# (old text, new text, what it is): each old text is found exactly once in H-1 v9.
SMALL = (
    ('entries 158 to 169 are build step 1 and the tidy-up);',
     'entries 158 to 169 are build step 1 and the tidy-up; entry 174\n     is RAT-43 and entry 175 the new reviewer chat\'s takeover; entries 176 to 212 are build step 2, with the\n     runner\'s rulebook v0.7 (RAT-44, entry 192) and the rehearsal on Windows (entries 199 to 208));',
     'section 0 item 2: the decision log entries'),
    ('with the reviewer\'s findings on the first (`exchange/EX_276_ChatGPT.md`) and its passes (`EX_278`, `EX_280`);',
     'with the reviewer\'s findings on the first (`exchange/EX_276_ChatGPT.md`) and its passes (`EX_278`, `EX_280`);\n   - build step 2\'s note, `exchange/CLAUDE_WEB_TOOLS/step2/STEP2_PACKAGE_NOTE_v0_3.md`, with the reviewer\'s findings on\n     that step (`exchange/EX_283_ChatGPT.md`, `EX_285_ChatGPT.md`) and its passes (`EX_290`, `EX_294`);',
     'section 0 item 2: build step 2\'s note'),
    ('     runner\'s rulebook, v0.6; section 8.6).', '     runner\'s rulebook, v0.7; section 8.6).', 'section 0 item 2: the rulebook'),
    ('The ratified design\'s engine, trees and commands\n   are **not coded at all**.',
     'The ratified design\'s **research engine is installed\n   beside it** (`src/research/`, build step 2); its trees, installs, backups and laboratory tools are **not coded**.',
     'section 0A item 1'),
    ('At this\n   edition: the last RAT is RAT-43 (this handover and H-2 v5r1); the newest EX is EX_281; the newest decision log\n   entry is 174 (RAT-43).',
     'At this\n   edition: the last RAT is RAT-44 (the runner\'s rulebook v0.7); the newest EX is EX_294, and EX_295 is expected to\n   be the reviewer\'s reply on this candidate; the newest decision log entry is 213 (this candidate written).',
     'section 0A item 3'),
    ('    build every hash table from the bytes Git holds (`git show :<path>`), never from the working copy (EX_276 C03).\n',
     '    build every hash table from the bytes Git holds (`git show :<path>`), never from the working copy (EX_276 C03).\n'
     '12. **Some record files are CRLF and some are LF.** `exchange/OWNER_REMINDERS.md`, `exchange/OWNER_ROADMAP.md`,\n'
     '    `exchange/CLAUDE_WEB_TOOLS/README.md` and the task files in `inbox/` are CRLF; the decision log, `CONTINUITY_NOW.md` and\n'
     '    the runner\'s rulebook are LF. Edit a file\'s bytes and keep its endings, and **look at\n'
     '    `git diff --cached --numstat` before every commit** (entry 193).\n'
     '13. **Push nothing while the owner is in the middle of an install** (entry 210): his tree then holds uncommitted\n'
     '    files and a commit of yours on GitHub costs him a pull he did not expect. Hold the records until his commit\n'
     '    is pushed.\n'
     '14. **The reviewer takes EX numbers too.** Fetch immediately before taking one, and never reuse one (entry 189).\n'
     '15. **The old system kept a record for a target it could not forecast** (`INSUFFICIENT_HISTORY`); a new list simply\n'
     '    begins later, at `first_target`. Anything that compares old records with new lists must count those apart\n'
     '    (entries 205 to 208).\n',
     'section 0A: items 12 to 15'),
    ('## 0B. The state at this edition (23 November 2026)', '## 0B. The state at this edition (24 November 2026)', 'section 0B: the heading'),
    ('2. **Section 1.1, the local runner.** The rulebook is now v0.6 (RAT-42, entry 156): a restrictive baseline that\n   names the new system\'s commands as never run. A narrowly scoped, reviewed amendment is owed before any runner\n   rehearsal of the new system (section 8.6).',
     '2. **Section 1.1, the local runner.** The rulebook is now v0.7 (RAT-44, entry 192): it names the new system\'s\n   commands as never run, except against a scratch tree under `D:\\DELETE_ME\\` when a task file says so (section\n   8.6).',
     'section 0C item 2'),
    ('Build step 2 carries it into the new system: reuse it, do not rewrite it; any',
     'Build step 2 carried it into the new system byte for byte, as `src/research/ov1_numeric.py` (a test asserts the\n  equality): do not rewrite it; any',
     'section 7.3: the kernel'),
    ('  evidence, including the owner\'s own outputs (`evidence/owner_pc_2026_11_23/` in each). Section 12.2.\n',
     '  evidence, including the owner\'s own outputs (`evidence/owner_pc_2026_11_23/` in each). Section 12.2.\n'
     '- `exchange/CLAUDE_WEB_TOOLS/step2/`: build step 2. The engine\'s files as they went into the tree (`overlay/`), the\n'
     '  builder and its tools, the four packages (`package/`, `package_v1r1/`, `package_v1r2/` are superseded; `package_v1r3/`\n'
     '  is the one installed), the three notes, the build plans, and the evidence of each round (`evidence*/`). The\n'
     '  owner\'s own install outputs of 24 November 2026 are in the decision log entries 209 to 212, in his words.\n'
     '- `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_7/`: the three candidates of the runner\'s rulebook v0.7, their diffs and\n'
     '  builders, and the two scripts that installed it. `t025/`, `t026/`, `t027/`: the three task files\' builders.\n',
     'section 7.4: build step 2\'s record'),
    ('This section describes practice, not rules. Section 12.3 is now the practice of build step 1 and the tidy-up, both\ninstalled; section 12.4 is carried from H-1 v7r1 in short form and was not exercised by this chat.',
     'This section describes practice, not rules. Section 12.3 is the practice of build step 1, the tidy-up and build\nstep 2, all installed; section 12.4 is the practice of the three runner tasks of 23 and 24 November 2026.',
     'section 12: the opening lines'),
    ('The workspace paths inside older scripts are a previous chat\'s; change them at the top before use.',
     '- **`step2/`** (build step 2): `build_step2_pkg.py <repo> <base> <out> <engine tests>` (the package from a clean clone\n'
     '  at the base commit and `overlay/`; it writes the verifier, the manifest and the sheet, and refuses a sheet that\n'
     '  names another package), `apply_edits.py` (the two counted edits to existing files), `sync_and_test.sh`,\n'
     '  `mutation_check.py` (36 planted faults), `scan_practices.py`, `rehearse_install.sh` (an LF and a CRLF clone, seven\n'
     '  cases that must STOP), `compare_fill_with_old_records.py` (a first fill against the old score records and the old\n'
     '  run folders; `PASS - COMPLETE` only for both games with the run folders present), `check_compare_tool.py` (that\n'
     '  tool on made-up old records, with planted differences), and the assemblers `assemble_ex*.py` (an EX message with\n'
     '  every hash computed).\n'
     '- **`rulebook_v0_7/`**, **`t025/`, `t026/`, `t027/`** and **`h1v10/`**: the rulebook\'s builders, the task files\' builders\n'
     '  (section 12.4) and this edition\'s.\n'
     'The workspace paths inside older scripts are a previous chat\'s; change them at the top before use.',
     'section 12.2: the step 2 tools'),
    ('- **Coding practices:** every package says "coding practices met" or lists the exceptions with their reasons.\n',
     '- **Coding practices:** every package says "coding practices met" or lists the exceptions with their reasons.\n'
     '- **What build step 2 added to this practice:** a code-bearing package goes to the reviewer as an EX ZIP made by an\n'
     '  assembler (the message, the package ZIP unchanged, its member list), with the package also extracted in the\n'
     '  `exchange/EX_nnn_Claude/` folder; a corrected package is a new name (`v1r1`, `v1r2`, `v1r3`) with the exact diff\n'
     '  from the one reviewed and a table of the files that differ; **a rehearsal on Windows by the runner comes before\n'
     '  the owner\'s install** (section 8.6); the sheet\'s baseline is made in the same sitting or its folder is checked\n'
     '  to exist; and **nothing is pushed while the owner installs** (section 0A item 13). The cloud workspace of this\n'
     '  chat kept a filled copy of the tree, which let made-up records in the real form be built (section 8.8).\n',
     'section 12.3: what build step 2 added'),
    ('**QA** will be `D:\\TEST_BED` (backups `D:\\TEST_BED_backups`) and **PROD** `G:\\a_p_r_i_r` (backups\n  `T:\\a_p_r_i_r_backups`): the deployment design\'s examples; each tree\'s `ENVIRONMENT.ini` decides. Neither exists yet.',
     '**PROD** will be `G:\\a_p_r_i_r` and **QA** `T:\\a_p_r_i_r`, with backups under `T:\\a_p_r_i_r_backups\\PROD`\n  and `\\QA` (the owner, entry 181; the deployment design\'s own examples are older); each tree\'s `ENVIRONMENT.ini`\n  decides. Neither exists yet. DEV has its `ENVIRONMENT.ini` (entry 212).\n'
     '- **The scratch folder is `D:\\DELETE_ME\\`** (an SSD), for the runner\'s rehearsals (section 8.6). The owner deletes\n'
     '  what is left there himself.\n'
     '- **A plain CMD window** (from the Start menu) is where the owner runs a sheet and builds a `.venv`. A VS Code\n'
     '  terminal has the main `.venv` active.\n'
     '- **Measured there (24 November 2026):** the suite 25 minutes (571 tests) and 29 minutes (762); a first fill of\n'
     '  both games 46 to 47 minutes; a job with nothing new 3 minutes; the comparison with the old records 2 minutes.',
     'section 12.6: the places, the scratch folder and the times'),
    ('Commits named in this file: `c7e6ed8` (the tidy-up installed)',
     'Commits named in this file: `5f16b35` (build step 2 installed); `c7e6ed8` (the tidy-up installed)',
     'Appendix A: the commits'),
)
