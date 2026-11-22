# TIDY1_Method_Comments_v1 - light tidy-up package (headers and comments of the existing method files; RAT-40 note 3): install and run sheet

**Only after the owner's own go for each part.** Windows CMD, in the repository root
(`E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`). Nothing of the project running.
**Save the ZIP to `E:\TEMP`, not into the repository,** delete any earlier `E:\TEMP\TIDY1_Method_Comments_v1` folder, and extract it so that
`E:\TEMP\TIDY1_Method_Comments_v1\VERIFY_TIDY1_INSTALL.py` exists. Base commit: `7be6b3aa8115d6a44edd9ab59180c1cdcfcda674`.

**What this package does.** It replaces 37 existing method files with the same files carrying fuller
headers and comments. No file is added, moved or deleted, and no line of code changes: part 2 proves that for
every file, and part 4 runs the equivalence check of build step 1 again.

**A STOP is a STOP.** If any step prints `STOP`, `FAIL`, an error, or anything other than what is expected: do not
go on, do not retry, do not reset or undo anything. Send Claude the whole output.
**The one exception** is the test suite's own report of the failures that exist today: the word `FAILED` on a
module's line in parts 1 and 3, and the lines `FAILS IN BOTH RUNS` in part 3, are expected for as long as part 3's
comparison ends with its `RESULT: every test that ran was identified; no module and no test changed ...` line.
A failure that is new, a `CHANGED` line, or any STOP from the verifier, the comments-only check or the
equivalence check still stops.

Nothing here contacts a lottery website, changes the PC's date or time, or ends a process. The suite and the
equivalence check read the results masters and the old records; they write only under `E:\TEMP\TIDY1_evidence`
(the suite's reports) and Python's own temporary folders. Your ZIP of the project folder made before build
step 1 remains the way back to the old system; no new ZIP is needed, because this package touches no data and no
run folder.

## Part 1. Update, and the suite as it is today (the baseline; about 25 minutes)

```bat
git status --short
git pull --ff-only
.venv\Scripts\python.exe -B "E:\TEMP\TIDY1_Method_Comments_v1\tools\run_suite.py" . "E:\TEMP\TIDY1_evidence\suite_before"
git status --short
```

Expected: the first `git status --short` prints nothing; the pull says `Fast-forward` or `Already up to date`; one
line for each test module, some of them `FAILED` (two modules are known to fail today; that is the baseline, not a
STOP); a last line `DONE: 45 modules, ... tests ran`; and the second `git status --short` prints nothing.

## Part 2. Check, copy, check, and the proof that only comments changed (about a minute)

```bat
.venv\Scripts\python.exe "E:\TEMP\TIDY1_Method_Comments_v1\VERIFY_TIDY1_INSTALL.py" --repo . --phase pre
xcopy "E:\TEMP\TIDY1_Method_Comments_v1\repo_overlay\*" . /E /Y
.venv\Scripts\python.exe "E:\TEMP\TIDY1_Method_Comments_v1\VERIFY_TIDY1_INSTALL.py" --repo . --phase post
.venv\Scripts\python.exe -B "E:\TEMP\TIDY1_Method_Comments_v1\tools\check_comments_only.py" --tree .
```

Expected: `PRE PASS`; `37 File(s) copied`; `POST PASS` (0 new paths, 37 modified files, 0 staged
deletions); then 37 lines beginning `comments only:`, a line `compared with commit ...: N Python files
under src and tests; 37 with changed text; 0 with a problem`, and the last line
**`RESULT: PASS - in all 37 changed files only comments and docstrings differ; the code Python runs is identical.`**
A line beginning `CODE CHANGED`, `ADDED`, `REMOVED` or `NOT READABLE`, or `RESULT: STOP`, is a STOP.

## Part 3. The same suite again, and the comparison (about 25 minutes)

```bat
.venv\Scripts\python.exe -B "E:\TEMP\TIDY1_Method_Comments_v1\tools\run_suite.py" . "E:\TEMP\TIDY1_evidence\suite_after"
.venv\Scripts\python.exe -B "E:\TEMP\TIDY1_Method_Comments_v1\tools\compare_suite_reports.py" "E:\TEMP\TIDY1_evidence\suite_before" "E:\TEMP\TIDY1_evidence\suite_after"
```

Expected, from the comparison: two lines `before: 45 modules; unittest ran N tests; identified here: N` and
`after: ...` with the same N four times; `tests in both runs: N; with the same result: N`; some lines
`FAILS IN BOTH RUNS` (the failures that exist today; the words `FAILURE LINES DIFFER` on `test_gitignore_lines` are
expected, because that test prints a set in a different order each run); **no line beginning `CHANGED`,
`DISAPPEARED`, `NEW`, `MODULE`, `NOT ALL TESTS IDENTIFIED` or `NO SUMMARY`;** and the last line
`RESULT: every test that ran was identified; no module and no test changed its result, disappeared or appeared`.
Any other result is a STOP.

## Part 4. The equivalence check again (reads only; about 40 minutes; leave the window alone)

```bat
.venv\Scripts\python.exe -B "E:\TEMP\TIDY1_Method_Comments_v1\tools\check_layout_equivalence.py" --tree .
```

It is the same check, byte for byte, that you ran for build step 1: it computes every old development forecast
again with the tidied code, in memory, and compares content digests.
Expected: for each game a line `coverage: the batch records list N published forecasts; an old digest was found
for N of them; MISSING: 0; ...`; one line for each variant, `n of n equal`; and the last line
**`RESULT: PASS - COMPLETE - both games; every forecast the batch records list was found, computed again ... the
same content digest.`**
Anything else is a STOP: a line beginning `DIFFERENT` or `FAILED`, `RESULT: STOP`, a `MISSING` count above 0, or
`RESULT: PARTIAL` (it names what was not covered). Change nothing and send Claude the output.
(Optional, to save time: four CMD windows, each with the same command and one of `--part 1/4`, `--part 2/4`,
`--part 3/4`, `--part 4/4`. Each then ends `RESULT: PARTIAL` giving `--part was used` as its only reason; all four
must end so, each with `MISSING: 0` for both games and no `DIFFERENT` or `FAILED`.)

## Part 5. Stage, commit, check, and only then push

```bat
git add src
git status --short
git commit -m "LIGHT TIDY-UP (RAT-40 note 3): headers, dependency lists and missing comments in the existing method files; no calculation change"
.venv\Scripts\python.exe "E:\TEMP\TIDY1_Method_Comments_v1\VERIFY_TIDY1_INSTALL.py" --repo . --phase committed
```

Expected: `git status --short` lists 37 lines starting with `M`, all under `src/methods/`, and nothing else;
then `COMMITTED PASS`. Git's "LF will be replaced by CRLF" warnings are harmless.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

## Part 6. What to send Claude

The commit ID; the text of part 2's comments-only check, of the comparison (part 3) and of the equivalence check
(part 4), copied from the window; and, if anything was unexpected, the folder `E:\TEMP\TIDY1_evidence`. Claude then verifies the
commit from GitHub.
