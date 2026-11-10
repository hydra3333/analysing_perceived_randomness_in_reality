# MHUP-A install instructions (design v0.1r6 Appendix J, steps 0 to 19) - DRAFT, NOT FOR USE

**DRAFT (item 2 of the integrated package work list). Do not run any of this.** It is not reviewed, the verifier's
`released` phase (step 17) is not built yet (item 3), and no install is authorised. It exists so that the reviewer can
check the steps against Appendix J before the final package is frozen. Written by Claude for the project owner.

- Package: `@@PKG@@`; manifest `PACKAGE_MANIFEST_MHUP_A.json`, SHA-256 `@@MANIFEST_SHA256@@`.
- Base commit: `@@BASE@@` (`@@BASE7@@`). E_1 revision 3's `effective_date`: `@@DATE@@` (C01-EFF).
- The package: @@N_NEW@@ new files, @@N_MOD@@ replaced files and @@N_DEL@@ deletion (`src/results_master_v0_1.py`,
  replaced by v0.2). Step 6 copies @@N_GATE@@ gate files; step 8 copies the other @@N_REST@@ and makes the deletion.
- The suite: @@N_TESTS@@ tests in @@N_MODULES@@ modules (about 25 minutes). It includes E2R-T12, which starts up to six
  ordinary Python workers that finish by themselves: your approval for this run is needed, as for every install.
- Two commits: the package commit (step 12) and the release commit (step 17). Push only at step 19.

**How to run it.** One Windows command window (CMD, not PowerShell), opened at the repository, used for every step.
Paste each step's block, then compare the output with "Expect". **A STOP is a STOP:** on any output other than the
expected one, stop, do not run the next step, do not push, reset or delete anything, and send Claude the whole window.
The "If it STOPs" line says what stays in place. Nothing in these steps ever terminates a process; if a check lists one,
you let it end, or close it through its own console.

**Barriers (Appendix J).** U = the updater's own lock `source_data\.results_master.lock`; E = E_1's
`src\methods\E_001\IN_DEVELOPMENT.txt`; P = `src\methods\_common\contract_data\INSTALL_IN_PROGRESS.txt`. U is taken
first (step 3) and released last (step 18). None is ever committed (the new `.gitignore` lists them). While U exists
the updater refuses: if it says to "delete the lock by hand", do NOT: only step 18 or Claude's reviewed restore
steps remove it.

## Before you start (not an Appendix J step)

- Nothing of the project is running: no experiment, report, walk-forward run, coordinator or updater; close VS Code's
  Python terminals at the repository.
- The zip is saved in `E:\TEMP`, never in the repository. Its SHA-256 is in Claude's EX message.

```
cd /d E:\TEMP
certutil -hashfile @@PKG@@.zip SHA256
tar -xf @@PKG@@.zip
```
Expect: the SHA-256 from Claude's message; then a folder `E:\TEMP\@@PKG@@`.

## Step 0 - clean tree, latest main

```
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
set "REPO=%CD%"
set "PKG=E:\TEMP\@@PKG@@"
set "PY=%REPO%\.venv\Scripts\python.exe"
set "NOPYC=%REPO%\transitory_data\no_pycache_ever"
set "PC=%PKG%\repo_overlay\src\package_tools\process_check.py"
set "IR=%PKG%\repo_overlay\src\package_tools\install_records.py"
set "MAN=%PKG%\PACKAGE_MANIFEST_MHUP_A.json"
git status --short
git pull --ff-only
git status --short
git log -1 --format=%H
```
Expect: both `git status --short` print nothing; the pull says "Already up to date." or fast-forwards; the last line
is the commit you are installing on (`@@BASE7@@...` or a later one of yours).
If it STOPs: nothing has changed; send the output.

## Step 1 - PRE (the verifier; read-only)

```
"%PY%" -I -B "%PKG%\VERIFY_MHUP_A.py" --repo "%REPO%" --phase pre
```
Expect: `PRE PASS: ...` (it also checks the staged `process_check.py` against the manifest).
If it STOPs: nothing has changed; send the output.

## Step 2 - preflight install check (before U exists)

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" check-no-runs --root "%REPO%" --install "%MAN%"
```
Expect: `CLEAN`.
If it STOPs (`REFUSED`): nothing has changed. The output lists each project Python process; let it end, or close it
through its own console (for example a VS Code Python terminal), then rerun this step. A session lock or an updater
lock: send the output.

## Step 3 - take U (the updater's lock)

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" take-install-lock --root "%REPO%" --package MHUP_A
```
Expect: `CLEAN; install lock taken for MHUP_A`.
If it STOPs: U already existed. Content naming an install: an earlier install did not finish; content of an update:
an update is running or crashed. Either way stop and send the output.

## Step 4 - create barriers E and P

```
"%PY%" -I -B "%PKG%\MHUPA_COPY.py" barrier --create E --repo "%REPO%"
"%PY%" -I -B "%PKG%\MHUPA_COPY.py" barrier --create P --repo "%REPO%"
```
Expect: `BARRIER PASS: E created ...` then `BARRIER PASS: P created ...`.
If it STOPs: send the output; Claude gives the removal of E and P and the release of U.

## Step 5 - install check, immediately before the gate copy

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" check-no-runs --root "%REPO%" --install "%MAN%"
```
Expect: `CLEAN`.
If it STOPs: let the listed process end; rerun this step.

## Step 6 - copy the @@N_GATE@@ new dispatch-gate files

```
"%PY%" -I -B "%PKG%\MHUPA_COPY.py" copy --part gate --repo "%REPO%"
```
Expect: `COPY PASS: part gate: @@N_GATE@@ files written and read back`.
If it STOPs: from here on the restore rule applies: keep every copied file and E, P and U; send the output; Claude
gives the install check to repeat until `CLEAN`, then the reviewed restore steps.

## Step 7 - install check, after the gate copy

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" check-no-runs --root "%REPO%" --install "%MAN%"
```
Expect: `CLEAN`.
If it STOPs: keep everything in place; let the listed process end; rerun this step.

## Step 8 - copy the rest and make the deletion

```
"%PY%" -I -B "%PKG%\MHUPA_COPY.py" copy --part rest --repo "%REPO%"
```
Expect: `COPY PASS: part rest: @@N_REST@@ files written and read back, 1 deleted`.
If it STOPs: as step 6.

## Steps 9 and 10 - POST, then the suite (one block; do not skip the suite)

```
"%PY%" -I -B "%PKG%\VERIFY_MHUP_A.py" --repo "%REPO%" --phase post
"%PY%" -I "%PKG%\RUN_MHUP_A_SUITE.py" --repo "%REPO%"
```
Expect: `POST PASS: ...`, then module lines and `SUITE PASS: all @@N_TESTS@@ tests ran and passed; ...` (at most the four
symlink skips).
If it STOPs: as step 6. Do not commit.

## Step 11 - install check

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" check-no-runs --root "%REPO%" --install "%MAN%"
```
Expect: `CLEAN`. If it STOPs: let the listed process end; rerun this step.

## Step 12 - the install record and the package commit

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%IR%" install-record --root "%REPO%" --package MHUP_A --manifest "%MAN%"
git add --pathspec-from-file="%PKG%\STAGE_PACKAGE_COMMIT.txt"
git status --short --no-renames
```
Expect: `INSTALL RECORD PASS: ...`; `git add` may print "LF will be replaced by CRLF" warnings (harmless); `git status
--short --no-renames` shows exactly @@N_STAGE1@@ lines, each starting `A `, `M ` or `D `, and nothing else
(`--no-renames` keeps the deleted updater v0.1 and the new v0.2 on separate lines). Then:
```
git commit -q -m "MHUP-A install, package commit (design v0.1r6 Appendix J step 12)"
```
If it STOPs: E, P and U stay; send the output; Claude writes the fix, and the step is rerun.

## Step 13 - COMMITTED (the verifier)

```
"%PY%" -I -B "%PKG%\VERIFY_MHUP_A.py" --repo "%REPO%" --phase committed
```
Expect: `COMMITTED PASS: ...`.
If it STOPs: do not push; E, P and U stay (the code is committed but not released); send the output.

## Step 14 - install check

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" check-no-runs --root "%REPO%" --install "%MAN%"
```
Expect: `CLEAN`. If it STOPs: let the listed process end; rerun this step.

## Step 15 - remove E, then P

```
"%PY%" -I -B "%PKG%\MHUPA_COPY.py" barrier --remove E --repo "%REPO%"
"%PY%" -I -B "%PKG%\MHUPA_COPY.py" barrier --remove P --repo "%REPO%"
```
Expect: `BARRIER PASS: E removed ...` then `BARRIER PASS: P removed ...`.
If it STOPs: send the output.

## Step 16 - the release record

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%IR%" release-record --root "%REPO%" --package MHUP_A --manifest "%MAN%"
```
Expect: `RELEASE RECORD PASS: ...`.
If it STOPs: re-create P (`"%PY%" -I -B "%PKG%\MHUPA_COPY.py" barrier --create P --repo "%REPO%"`); send the output;
after the fix, remove P and rerun this step (the record carries the date of the step that writes it).

## Step 17 - the release commit and the `released` phase

```
git add --pathspec-from-file="%PKG%\STAGE_RELEASE_COMMIT.txt"
git status --short --no-renames
git commit -q -m "MHUP-A install, release commit (design v0.1r6 Appendix J step 17)"
"%PY%" -I -B "%PKG%\VERIFY_MHUP_A.py" --repo "%REPO%" --phase released
```
Expect: `git status --short --no-renames` shows exactly one line, `A  src/methods/_common/contract_data/install_records/RELEASE_MHUP_A_V1.json`;
then `RELEASED PASS: ...`. **In this DRAFT the `released` phase is not built (item 3) and always STOPs.**
If it STOPs: re-create P; send the output; after the fix, remove P and rerun from this step.

## Step 18 - release U

```
"%PY%" -I -B -X "pycache_prefix=%NOPYC%" "%PC%" release-install-lock --root "%REPO%" --package MHUP_A
```
Expect: `CLEAN; install lock released for MHUP_A`.
If it STOPs: nothing else is removed; send the output.

## Step 19 - push both commits

```
git push
```
Then tell Claude, who verifies the install from GitHub.

## Not yet in this draft (item 3 and later)

- The `released` phase: the release commit's only parent is the package commit; it adds exactly the release record;
  the record names E_1 revision 3 for both games, the install record's digest and a date not before it; E and P
  absent; U still this package's; the records agree with the repository (EX_148 (ix)).
- The barrier-order proof and the verifier's own negatives.
- Claude's reviewed restore steps for a STOP from step 6 on.
- A cold read of these steps against Appendix J by a fresh helper.
