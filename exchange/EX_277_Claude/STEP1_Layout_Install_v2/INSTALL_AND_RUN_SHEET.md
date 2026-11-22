# STEP1_Layout_Install_v2 - build step 1 package (the folder layout; specification 17.3 phase 1): install and run sheet

**Only after the owner's own go for each part.** Windows CMD, in the repository root
(`E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`). Nothing of the project running.
**Save the ZIP to `E:\TEMP`, not into the repository,** delete any earlier `E:\TEMP\STEP1_Layout_Install_v2` folder, and extract it so that
`E:\TEMP\STEP1_Layout_Install_v2\VERIFY_STEP1_INSTALL.py` exists. Base commit: `c0e31043200caf34616c5dfe86baa3a77eb9f6d0`.

**A STOP is a STOP.** If any step prints `STOP`, `FAIL`, an error, or anything other than what is expected: do not
go on, do not retry, do not reset or undo anything. Send Claude the whole output.
**The one exception** is the test suite's own report of the failures that exist today: the word `FAILED` on a
module's line in parts 1 and 3, and the lines `FAILS IN BOTH RUNS` in part 3, are expected for as long as part 3's
comparison ends with its `RESULT: every test that ran was identified; no module and no test changed ...` line.
A failure that is new, a `CHANGED` line, or any STOP from the verifier or the equivalence check still stops.

Nothing here contacts a lottery website, changes the PC's date or time, or ends a process. The suite and the
equivalence check read the results masters and the old records; they write only under `E:\TEMP\STEP1_evidence`
(the suite's reports) and Python's own temporary folders.

## Part 0. Your own ZIP of the project folder (before anything else)

Make one full ZIP of the whole project folder on E: by hand, with `.git` and the old run folders included
(`.venv` is your choice). Keep it off E:. Open it once to see that it reads. **It is the only other copy of the
old forecast records that Git does not track, and it is the way back to the old system** (specification 17.2).

## Part 1. Update, and the suite as it is today (the baseline; about 25 minutes)

```bat
git status --short
git pull --ff-only
.venv\Scripts\python.exe -B "E:\TEMP\STEP1_Layout_Install_v2\tools\run_suite.py" . "E:\TEMP\STEP1_evidence\suite_before"
git status --short
```

Expected: the first `git status --short` prints nothing; the pull says `Fast-forward` or `Already up to date`; one
line for each test module, some of them `FAILED` (two modules are known to fail today; that is the baseline, not a
STOP); a last line `DONE: 45 modules, ... tests ran`; and the second `git status --short` prints nothing.

## Part 2. Check, copy, delete, check

```bat
.venv\Scripts\python.exe "E:\TEMP\STEP1_Layout_Install_v2\VERIFY_STEP1_INSTALL.py" --repo . --phase pre
xcopy "E:\TEMP\STEP1_Layout_Install_v2\repo_overlay\*" . /E /Y
git rm -q --pathspec-from-file="E:\TEMP\STEP1_Layout_Install_v2\DELETE_PATHS.txt"
.venv\Scripts\python.exe "E:\TEMP\STEP1_Layout_Install_v2\VERIFY_STEP1_INSTALL.py" --repo . --phase post
```

Expected: `PRE PASS`; `110 File(s) copied`; the `git rm` prints nothing; `POST PASS`.
(The 15 moved files arrive at their new paths in the overlay and leave their old paths in the `git rm`.)

## Part 3. The same suite again, and the comparison (about 25 minutes)

```bat
.venv\Scripts\python.exe -B "E:\TEMP\STEP1_Layout_Install_v2\tools\run_suite.py" . "E:\TEMP\STEP1_evidence\suite_after"
.venv\Scripts\python.exe -B "E:\TEMP\STEP1_Layout_Install_v2\tools\compare_suite_reports.py" "E:\TEMP\STEP1_evidence\suite_before" "E:\TEMP\STEP1_evidence\suite_after"
```

Expected, from the comparison: two lines `before: 45 modules; unittest ran N tests; identified here: N` and
`after: ...` with the same N four times; `tests in both runs: N; with the same result: N`; some lines
`FAILS IN BOTH RUNS` (the failures that exist today; the words `FAILURE LINES DIFFER` on `test_gitignore_lines` are
expected, because that test prints a set in a different order each run); **no line beginning `CHANGED`,
`DISAPPEARED`, `NEW`, `MODULE`, `NOT ALL TESTS IDENTIFIED` or `NO SUMMARY`;** and the last line
`RESULT: every test that ran was identified; no module and no test changed its result, disappeared or appeared`.
Any other result is a STOP.

## Part 4. The equivalence check (reads only; about 30 to 60 minutes; leave the window alone)

```bat
.venv\Scripts\python.exe -B "E:\TEMP\STEP1_Layout_Install_v2\tools\check_layout_equivalence.py" --tree .
```

It computes every old development forecast again with the moved code, in memory, and compares content digests.
The tracked batch records list every forecast the old system published; the check must find an old record for
each of them (in the rank ledgers or in your old run folders) and reproduce it.
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
git add src tests
git status --short
git commit -m "BUILD STEP 1: the folder layout (specification 17.3 phase 1): method files to the family and variant layout, shared helpers to _shared, the runner table built from the folder tree"
.venv\Scripts\python.exe "E:\TEMP\STEP1_Layout_Install_v2\VERIFY_STEP1_INSTALL.py" --repo . --phase committed
```

Expected: `git status --short` lists 15 lines starting with `R` (moved), 80 starting with `A`,
15 starting with `M` and 1 starting with `D`, and nothing else; then
`COMMITTED PASS`. Git's "LF will be replaced by CRLF" warnings are harmless.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

## Part 6. What to send Claude

The commit ID; the text of the comparison (part 3) and of the equivalence check (part 4), copied from the
window; and, if anything was unexpected, the folder `E:\TEMP\STEP1_evidence`. Claude then verifies the commit from GitHub.
