# MHUP-A install instructions (design v0.1r6 Appendix J, steps 0 to 19) - DRAFT, NOT FOR USE

**DRAFT (items 2 and 3 of the integrated package work list). Do not run any of this.** It is not reviewed, the package
is not frozen, and no install is authorised. It exists so that the reviewer can check the steps against Appendix J
before the final package is frozen. Written by Claude for the project owner.

- Package: `MHUPA_Install_v1`; manifest `PACKAGE_MANIFEST_MHUP_A.json`, SHA-256 `ab71cf22d34e6f972aa995c76a6a19d1db6a42dfb30f324ed4acacc9409b3dc4`.
- Base commit: `c48ac3c393d2eab30014e6200d427b76d90f47ac` (`c48ac3c`). E_1 revision 3's `effective_date`: `2026-11-10` (C01-EFF).
- The package: 37 new files, 34 replaced files and 1 deletion (`src/results_master_v0_1.py`,
  replaced by v0.2). Step 6 copies 10 gate files; step 8 copies the other 61 and makes the deletion.
- The suite: 571 tests in 45 modules (about 25 minutes). It includes E2R-T12, which starts up to six
  ordinary Python workers that finish by themselves: your approval for this run is needed, as for every install.
- Two commits: the package commit (step 12) and the release commit (step 17). Push only at step 19.

**How to run it.** One Windows command window, used for every step: CMD, not PowerShell (press Win+R, type `cmd`,
Enter). Paste each step's block, then compare the output with "Expect". Lines joined by `&&` stop by themselves at the
first failure. **A STOP is a STOP:** on any output other than the expected one, stop, do not run the next step, do not
push, reset or delete anything, and send Claude the whole window. The "If it STOPs" line says what stays in place.
Nothing in these steps ever terminates a process; if a check lists one, you let it end, or close it through its own
console. If you ran a step twice by mistake, it STOPs without changing anything: say so when you send the output; it is
not a reason to restore. If the window is closed part-way, open a new CMD window and paste the "Step 0a" block again
(it only sets names; it runs no Git command), then carry on at the step you had reached.

**Barriers (Appendix J).** U = the updater's own lock `source_data\.results_master.lock`; E = E_1's
`src\methods\E_001\IN_DEVELOPMENT.txt`; P = `src\methods\_common\contract_data\INSTALL_IN_PROGRESS.txt`. U is taken
first (step 3) and released last (step 18). None is ever committed (the new `.gitignore` lists them). While U exists
the updater refuses: if it says to "delete the lock by hand", do NOT: only step 18 or Claude's reviewed restore
steps remove it. The tools enforce the order: the copy tool refuses to create E or P without U, to copy any file
without U, E and P, and to remove E or P before the package commit; the verifier checks the barrier state at every
phase (PRE: none; POST and COMMITTED: all three; RELEASED: U only).

## Before you start (not an Appendix J step)

- Nothing of the project is running: no experiment, report, walk-forward run, coordinator or updater; close VS Code's
  Python terminals at the repository.
- The zip is saved in `E:\TEMP`, never in the repository. Its SHA-256 is in Claude's EX message.

```
cd /d E:\TEMP
certutil -hashfile MHUPA_Install_v1.zip SHA256
tar -xf MHUPA_Install_v1.zip
```
Expect: the SHA-256 from Claude's message; then a folder `E:\TEMP\MHUPA_Install_v1`.

## Step 0a - names for this window (repeat this block in any new window)

```
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
set "REPO=%CD%"
set "PKG=E:\TEMP\MHUPA_Install_v1"
set "PY=%REPO%\.venv\Scripts\python.exe"
set "NOPYC=%REPO%\transitory_data\no_pycache_ever"
set "PC=%PKG%\repo_overlay\src\package_tools\process_check.py"
set "IR=%PKG%\repo_overlay\src\package_tools\install_records.py"
set "MAN=%PKG%\PACKAGE_MANIFEST_MHUP_A.json"
set "VER=%PKG%\VERIFY_MHUP_A.py"
set "COPYTOOL=%PKG%\MHUPA_COPY.py"
echo %REPO% and %PKG%
```
Expect: the last line prints the repository folder and `E:\TEMP\MHUPA_Install_v1`.

## Step 0 - clean tree, latest main

```
git status --short
```
Expect: nothing printed. If anything is printed: STOP (nothing has changed); send the output. Then:
```
git pull --ff-only && git status --short && git log -1 --format=%H
```
Expect: the pull says "Already up to date." or fast-forwards; `git status --short` prints nothing; the last line is the
commit you are installing on (`c48ac3c...` or a later one of yours).
If it STOPs: nothing has changed; send the output.

## Step 1 - PRE (the verifier; read-only)

```
"%PY%" -I -B "%VER%" --repo "%REPO%" --phase pre
```
Expect: `PRE PASS: ...` (it also checks the staged `process_check.py` against the manifest, and that no updater lock
exists yet: before step 3 no lock at all is allowed).
If it STOPs: nothing has changed; send the output.

## Step 2 - preflight install check (before U exists)

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" check-no-runs --root "%REPO%" --install "%MAN%"
```
Expect: `CLEAN`.
If it STOPs (`REFUSED`): nothing has changed. The output lists each project Python process; let it end, or close it
through its own console (for example a VS Code Python terminal), then rerun this step. A session lock: resume and
close that session first. An unfinished weekly set: run the weekly session to finish it first. An updater lock: send
the output.

## Step 3 - take U (the updater's lock)

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" take-install-lock --root "%REPO%" --package MHUP_A
```
Expect: `CLEAN; install lock taken for MHUP_A`.
If it STOPs: U already existed. Content naming an install: an earlier install did not finish; content of an update:
an update is running or crashed. Either way stop and send the output.

## Step 4 - create barriers E and P

```
"%PY%" -I -B "%COPYTOOL%" barrier --create E --repo "%REPO%" && "%PY%" -I -B "%COPYTOOL%" barrier --create P --repo "%REPO%"
```
Expect: `BARRIER PASS: E created ...` then `BARRIER PASS: P created ...`.
If it STOPs: send the output. The handling is: remove E and P, then release U; Claude gives those exact lines (the copy
tool's `--remove ... --restore`, then `release-install-lock`).

## Step 5 - install check, immediately before the gate copy

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" check-no-runs --root "%REPO%" --install "%MAN%"
```
Expect: `CLEAN`.
If it STOPs: let the listed process end; rerun this step.

## Step 6 - copy the 10 new dispatch-gate files

```
"%PY%" -I -B "%COPYTOOL%" copy --part gate --repo "%REPO%"
```
Expect: `COPY PASS: part gate: 10 files written and read back`.
If it STOPs: from here on the restore rule applies: keep every copied file and E, P and U; send the output; Claude
gives the install check to repeat until `CLEAN`, then the reviewed restore steps.

## Step 7 - install check, after the gate copy

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" check-no-runs --root "%REPO%" --install "%MAN%"
```
Expect: `CLEAN`.
If it STOPs: keep E, P, U and the copied files in place; let the listed process end, or close it through its own
console; rerun this step. (Restore only if you abandon the install; Claude gives the steps.)

## Step 8 - copy the rest and make the deletion

```
"%PY%" -I -B "%COPYTOOL%" copy --part rest --repo "%REPO%"
```
Expect: `COPY PASS: part rest: 61 files written and read back, 1 deleted`.
If it STOPs: as step 6.

## Steps 9 and 10 - POST, then the suite (one line; the suite starts only if POST passes; do not skip it)

```
"%PY%" -I -B "%VER%" --repo "%REPO%" --phase post && "%PY%" -I "%PKG%\RUN_MHUP_A_SUITE.py" --repo "%REPO%" --shadow
```
Expect: `POST PASS: ...`; then the suite runner checks POST again, makes a barrier-free copy of the installed files in a
temporary folder (your repository stays barred: U, E and P stay in place), runs the module lines there, checks your
repository again, removes the copy, and ends with `SUITE PASS: all 571 tests ran and passed; ...` (at most the four
symlink skips). About 25 minutes. Do not click inside the window while it runs (a click can pause the output; Esc
releases it).
If it STOPs: as step 6. Do not commit. (Why a copy: with the barriers in place the installed tree refuses every run, which
is the point of the barriers, so the tests run on an exact copy without them: N5, decided in principle on 11 November
2026; the matching amendment of Appendix J step 10 is for ratification with the package.)

## Step 11 - install check

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" check-no-runs --root "%REPO%" --install "%MAN%"
```
Expect: `CLEAN`. If it STOPs: let the listed process end; rerun this step.

## Step 12 - the install record and the package commit

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%IR%" install-record --root "%REPO%" --package MHUP_A --manifest "%MAN%"
```
Expect: `INSTALL RECORD PASS: ...`. If it STOPs: E, P and U stay; send the output. Then:
```
git add --pathspec-from-file="%PKG%\STAGE_PACKAGE_COMMIT.txt" && "%PY%" -I -B "%VER%" --repo "%REPO%" --phase staged && git commit -q -m "MHUP-A install, package commit (design v0.1r6 Appendix J step 12)"
```
Expect: `git add` may print "LF will be replaced by CRLF" warnings (harmless); then `STAGED PASS: the index holds exactly
the package commit (73 paths) ...`; the commit prints nothing. The commit is made only if STAGED passes.
If it STOPs: E, P and U stay; nothing is committed; send the output; Claude writes the fix, and this second block is
rerun (not the install-record line: the record exists and is kept).

## Step 13 - COMMITTED (the verifier)

```
"%PY%" -I -B "%VER%" --repo "%REPO%" --phase committed
```
Expect: `COMMITTED PASS: ...`.
If it STOPs: do not push; E, P and U stay (the code is committed but not released); send the output and do not
continue. Recovery is not part of these steps: Claude proposes one for that exact state, the reviewer checks it and you
approve it. The normal route is abandon and rebuild: a fresh install check showing `CLEAN` before any change, then
reviewed `git revert` commits (nothing is reset, rewritten or deleted; every commit and record stays in the history),
then E and P removed after another `CLEAN`, U released last, and a new package built and reviewed on the resulting
commit.

## Step 14 - install check

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" check-no-runs --root "%REPO%" --install "%MAN%"
```
Expect: `CLEAN`. If it STOPs: let the listed process end; rerun this step.

## Step 15 - remove E, then P

```
"%PY%" -I -B "%COPYTOOL%" barrier --remove E --repo "%REPO%" && "%PY%" -I -B "%COPYTOOL%" barrier --remove P --repo "%REPO%"
```
Expect: `BARRIER PASS: E removed ...` then `BARRIER PASS: P removed ...`. (Removing E first re-runs the COMMITTED check
and refuses unless it passes.)
If it STOPs: send the output.

## Step 16 - the release record

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%IR%" release-record --root "%REPO%" --package MHUP_A --manifest "%MAN%"
```
Expect: `RELEASE RECORD PASS: ...`.
If it STOPs saying "the install barrier P still exists": step 15 was missed; run step 15, then this step.
If it STOPs for any other reason: re-create P (`"%PY%" -I -B "%COPYTOOL%" barrier --create P --repo "%REPO%"`); send the
output; after the fix, remove P and rerun this step (the record carries the date of the step that writes it).

## Step 17 - the release commit and the `released` phase

```
git add --pathspec-from-file="%PKG%\STAGE_RELEASE_COMMIT.txt" && "%PY%" -I -B "%VER%" --repo "%REPO%" --phase staged && git commit -q -m "MHUP-A install, release commit (design v0.1r6 Appendix J step 17)"
```
Expect: `STAGED PASS: the index holds exactly the release commit (1 paths) ...`; the commit prints nothing. Then:
```
"%PY%" -I -B "%VER%" --repo "%REPO%" --phase released
```
Expect: `RELEASED PASS: two commits proved: ...`.
If either STOPs: do NOT run step 18 (U stays held) and do not push; re-create P
(`"%PY%" -I -B "%COPYTOOL%" barrier --create P --repo "%REPO%"`); send the output. If the release commit was NOT made
(the first block stopped), Claude's fix is applied, P removed, and this step rerun. If the release commit WAS made,
do not continue: the recovery is as step 13's (abandon and rebuild, approved for that exact state; the release record
stays in the history).

## Step 18 - release U

```
"%PY%" -I -B "%VER%" --repo "%REPO%" --phase released && "%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" release-install-lock --root "%REPO%" --package MHUP_A
```
Expect: `RELEASED PASS: ...` again, then `CLEAN; install lock released for MHUP_A`. (U is released only if RELEASED
passes at that moment.)
If it STOPs: nothing else is removed; send the output.

## Step 19 - push both commits

```
git push
```
Then tell Claude, who verifies the install from GitHub.

## Not yet in this draft

- Claude's reviewed restore steps for a STOP from step 6 on, as exact commands (the copy tool already has the
  `--remove ... --restore` form they end with).
- The final package identity: the frozen date, the base commit and the zip's SHA-256.
- Git 2.26 or later is assumed (`git add --pathspec-from-file`).
