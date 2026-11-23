# STEP2_Research_Engine_v1 - build step 2 package (the research engine, in DEV; specification v0.6 sections 3 to 11): install and run sheet

**Only after the owner's own go for each part.** Windows CMD, in the repository root
(`E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`). Nothing of the project running.
**Save the ZIP to `E:\TEMP`, not into the repository,** delete any earlier `E:\TEMP\STEP2_Research_Engine_v1` folder, and extract it
**to `E:\TEMP`** (the ZIP holds its own top folder), so that `E:\TEMP\STEP2_Research_Engine_v1\VERIFY_STEP2_INSTALL.py` exists. Base commit: `cc8398c58f55580be2112f73a55805a9d7f2503f`.

**What this package does.** It adds the new research engine beside the old system: 33 new files
(`src\research\`, the program `src\research_command.py`, the launchers `Run_Research.bat` and
`Withdraw_Variant.bat`, `deploy\INFRA_MANIFEST.ini`, `ENVIRONMENT.example.ini` and 7 test modules with their
fixtures). It replaces two existing files: `.gitignore` (six patterns added, so that Git ignores this PC's settings
file, DEV's research results, the status files and the `records` and `scratch` folders) and one old test,
`tests\test_mhupa_master_versions.py` (its list of the files allowed to name the results files gains the new
reader). **No file of the old system's code or of any method is changed,** and nothing is deleted.

**A STOP is a STOP.** If any step prints `STOP`, `FAIL`, `REFUSED`, an error, or anything other than what is
expected: do not go on, do not retry, do not reset or undo anything. Send Claude the whole output.
**The one exception** is the test suite's own report of the failures that exist today: the word `FAILED` on a
module's line in parts 1 and 3, and the lines `FAILS IN BOTH RUNS` in part 3, are expected for as long as part 3's
comparison ends as part 3 says.

Nothing here contacts a lottery website, changes the PC's date or time, or ends a process. Parts 1 to 5 read the
results masters and write only under `E:\TEMP\STEP2_evidence` (the suite's reports) and Python's own temporary folders. Part 6, on
its own go, is the first run of the new engine on the real results: it writes DEV's own research results under
`results\research\`, the status file in each variant folder, `records\` and nothing else; Git ignores all of
them. Your ZIP of the project folder made before build step 1 remains the way back to the old system.

## Part 1. Update, and the suite as it is today (the baseline; about 25 minutes, or none)

```bat
git status --short
git pull --ff-only
git diff --stat c7e6ed8 HEAD -- src tests
```

Expected: `git status --short` prints nothing; the pull says `Fast-forward` or `Already up to date`; the third
command prints nothing (`src` and `tests` are exactly as the tidy-up left them on 23 November).

**If the folder `E:\TEMP\TIDY1_evidence\suite_after` still exists** (the "after" run of the tidy-up on 23 November, made on
exactly these files), it is the baseline: skip the next command and use that folder as the "before" in part 3.
**Otherwise** make the baseline now:

```bat
.venv\Scripts\python.exe -B "E:\TEMP\STEP2_Research_Engine_v1\tools\run_suite.py" . "E:\TEMP\STEP2_evidence\suite_before"
git status --short
```

Expected: one line for each test module, some of them `FAILED` (two modules are known to fail today; that is the
baseline, not a STOP); a last line `DONE: 45 modules, 571 tests ran`; and `git status --short` prints nothing.

## Part 2. Check, copy, check (about a minute)

```bat
.venv\Scripts\python.exe "E:\TEMP\STEP2_Research_Engine_v1\VERIFY_STEP2_INSTALL.py" --repo . --phase pre
xcopy "E:\TEMP\STEP2_Research_Engine_v1\repo_overlay\*" . /E /Y
.venv\Scripts\python.exe "E:\TEMP\STEP2_Research_Engine_v1\VERIFY_STEP2_INSTALL.py" --repo . --phase post
```

Expected: `PRE PASS`; `35 File(s) copied`; `POST PASS` (33 new paths, 2 modified files, 0 staged
deletions).

## Part 3. The suite again, and the comparison (about 30 minutes)

```bat
.venv\Scripts\python.exe -B "E:\TEMP\STEP2_Research_Engine_v1\tools\run_suite.py" . "E:\TEMP\STEP2_evidence\suite_after"
```

Expected: a last line `DONE: 52 modules, 750 tests ran`, and the 7 new modules
(`test_research_forecasts`, `test_research_identity`, `test_research_job`, `test_research_manifest`, `test_research_ov1_and_checks`, `test_research_ov1_numeric`, `test_research_records`) each ending `OK`.

Then the comparison. It prints one line for every new test, so put it in a file and look at the rest. **In the first
command, type the baseline folder of part 1 in place of `BASELINE`** (`E:\TEMP\TIDY1_evidence\suite_after`, or
`E:\TEMP\STEP2_evidence\suite_before` if you made a new one):

```bat
.venv\Scripts\python.exe -B "E:\TEMP\STEP2_Research_Engine_v1\tools\compare_suite_reports.py" "BASELINE" "E:\TEMP\STEP2_evidence\suite_after" > "E:\TEMP\STEP2_evidence\comparison.txt"
findstr /v /b /c:"NEW: " /c:"MODULE NEW: " "E:\TEMP\STEP2_evidence\comparison.txt"
find /c "NEW: " "E:\TEMP\STEP2_evidence\comparison.txt"
```

Expected from `findstr` (every line that is not about a new test), exactly these:
`before: 45 modules; unittest ran 571 tests; identified here: 571`;
`after: 52 modules; unittest ran 750 tests; identified here: 750`;
**`tests in both runs: 571; with the same result: 571`**;
three entries `FAILS IN BOTH RUNS` (the failures that exist today: `test_gitignore_lines`, with the words
`FAILURE LINES DIFFER` and its two long lines, which is expected because that test prints a set in a different
order each run; and two tests of `test_multigame_reader_contracts`);
and the last line `RESULT: DIFFERENCES FOUND - each needs an explanation`. **Here that last line is expected:** the
only differences are the 7 new test modules and their 179 new tests. `find /c` prints **186** (179 lines `NEW:` and
7 lines `MODULE NEW:`).
**A STOP is any line beginning `CHANGED`, `DISAPPEARED`, `MODULE CHANGED`, `MODULE DISAPPEARED`,
`NOT ALL TESTS IDENTIFIED` or `NO SUMMARY`, a `tests in both runs` line whose two numbers differ, or a count other
than 186.**

```bat
git status --short
```

Expected: only the files of part 2: 2 lines starting ` M` and the new paths starting `??`. The suite has left
nothing else behind.

## Part 4. Stage, commit, check, and only then push

```bat
git add .gitignore deploy src tests Run_Research.bat Withdraw_Variant.bat ENVIRONMENT.example.ini
git status --short
git commit -m "BUILD STEP 2: the research engine in DEV (src/research, the two launchers, the manifest, its tests); the old system is not changed"
.venv\Scripts\python.exe "E:\TEMP\STEP2_Research_Engine_v1\VERIFY_STEP2_INSTALL.py" --repo . --phase committed
```

Expected: `git status --short` lists 33 lines starting with `A` and 2 starting with `M`, and nothing else; then
`COMMITTED PASS`. Git's "LF will be replaced by CRLF" warnings are harmless.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

## Part 5. This PC's settings file (a minute)

```bat
copy ENVIRONMENT.example.ini ENVIRONMENT.ini
notepad ENVIRONMENT.ini
git status --short
```

In Notepad, check that `tree_root` is this folder and `venv_dir` is its `.venv`; the example already holds this
PC's paths, so there should be nothing to change. Leave the commented lines as they are (they belong to build
step 3). Save and close. `git status --short` prints nothing: Git ignores `ENVIRONMENT.ini`.

**Parts 1 to 5 install the engine and prove the install. They run nothing on real results. Stop here if you wish.**

## Part 6. DEV's first fill - only on your own separate go (half an hour to an hour; leave the window alone)

```bat
Run_Research.bat --game BOTH --no-update
```

What it does: for each game it gives every variant a status file (`ACTIVE`), computes every variant's forecast for
every draw it has enough earlier draws for, scores each against the result on file, saves the reports, and
forecasts the next draw. It says how far it has got every 25 draws. `--no-update` because DEV has no other tree
to copy results from yet; the results in DEV are still brought up to date by `Run_Results_Updater.bat`, as today.

Expected, at the end: for each game a line beginning
`POWERBALL: finished. Results on file through draw` (and the same for `OZLOTTO`), each ending
`prevailing OV-1: not started; waiting for a successful results step`; no line beginning `WARNING`; and the last
line **`The job finished.`** A line with `REFUSED` or `STOPPED`, or the last line `A STOP is a STOP: ...`, is a STOP:
change nothing and send Claude the whole output. (If the window is closed or the PC restarts part-way, the same
command continues where it stopped; if it then says `a process of this tree is running`, read what it says and
ask Claude before deleting anything.)

Then the same command once more, into a file (a few minutes; this second job has nothing new to compute, and its
time is the time of an ordinary week's job without new draws):

```bat
echo %TIME%
Run_Research.bat --game BOTH --no-update > "E:\TEMP\STEP2_evidence\second_job.txt" 2>&1
echo %TIME%
type "E:\TEMP\STEP2_evidence\second_job.txt"
git status --short
```

Expected: for each game `written: 0 forecasts, 0 scores, 0 prevailing lines, 0 eligibility draws, 0 report files`;
the last line `The job finished.`; and `git status --short` prints nothing (everything the job wrote is ignored
by Git).

## Part 7. The early comparison with the old development records (reads only; a few minutes)

```bat
.venv\Scripts\python.exe -B "E:\TEMP\STEP2_Research_Engine_v1\tools\compare_fill_with_old_records.py" --tree . > "E:\TEMP\STEP2_evidence\early_comparison.txt" 2>&1
findstr /v /e /c:" equal" "E:\TEMP\STEP2_evidence\early_comparison.txt"
findstr /e /c:" equal" "E:\TEMP\STEP2_evidence\early_comparison.txt" | find /c /v ""
```

It compares DEV's new lists with what the old system recorded, and computes and writes nothing. Part 1: every score
the old development walk-forward recorded must be in the new score lists with the same numbers drawn, matches and
prize division. Part 2: every development forecast the old system kept in its run folders must be in the new
forecast lists with the same view digest, scores, ranking, TOP and WORST.
Expected from `findstr` (every line that is not a per-variant line), exactly seven lines: for each game one line
`part 1: old score records (TOP and WORST): N; equal in the new score lists: N; DIFFERENT: 0`, one line
`part 2: old development forecasts read from the run folders: N ... DIFFERENT: 0 ...` and one line
`part 2: forecasts named by the tracked rank ledgers: N; of those not among the old forecasts compared: 0`; and the
last line **`RESULT: PASS - COMPLETE - both games; all N old score records equal the new score lists; all N old
development forecasts in the run folders were found in the new lists ...`** (the first N is 34800 for the score
records that Git tracks). The third command prints **160** (for each of the 40 variants of each game, one `scores`
line and one `forecasts` line, each `n of n equal`).
Anything else is a STOP: a line beginning `DIFFERENT`, a `DIFFERENT:` count above 0, `RESULT: STOP`,
`RESULT: PARTIAL` or `RESULT: REFUSED`. Change nothing and send Claude the file.

## Part 8. What to send Claude

The commit ID of part 4; the comparison's text (part 3); the last twenty lines of the first job's window and the
two times and the file `E:\TEMP\STEP2_evidence\second_job.txt` (part 6); the file `E:\TEMP\STEP2_evidence\early_comparison.txt` (part 7); roughly
how long the first job took;
and, if anything was unexpected, the folder `E:\TEMP\STEP2_evidence`. Claude then verifies the commit from GitHub.
The reports to look at, if you wish: `results\research\POWERBALL\reports\` (start with `README.txt`).
