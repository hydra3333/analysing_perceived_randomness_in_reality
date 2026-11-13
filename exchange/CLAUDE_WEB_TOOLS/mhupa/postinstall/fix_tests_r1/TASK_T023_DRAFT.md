# TASK_T023 - Windows suite run of the reviewed MHUP-A post-install test fix r1, in a task clone (no change to the main repository)

**Task ID:** T023. **Date:** 13 November 2026. **Author:** the Claude web chat. Rulebook v0.5; section 2A (T016 only) does not apply.

**Purpose.** MHUP-A is installed (commits `2860e86` and `effc179`). Eight tests then failed on `main` because they copied the repository's live install records and assumed the state before the install. The reviewed fix r1 (EX_165, R-2 PASS) changes only `tests/test_mhupa_install_records.py` and `tests/mhupa_slice2_fixtures.py`. This task runs the whole suite on Windows with those two files put into a disposable task clone that cannot push. If it passes, the project owner commits the two files himself, under his own separate approval.

**What it does not do.** It changes nothing in the main repository (only this task's report is committed there). It runs no launcher, coordinator, updater, Mode H command, process tool, records tool, report tool or `.bat`, and no other program than the ones below (the tests themselves start the updater's offline self-test and small Python workers on invented data, as they are written to). It reads no real data itself and contacts no website. "No change" means the main repository: the clone and the tests write to their own temporary folders.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish by themselves) runs in step 9. The project owner approves it for this run by giving this task.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| TOOLS | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools` |
| CLONE (the task clone) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r` |
| PKG (the extracted fix) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\p\MHUPA_TESTFIX_r1` |

Run each command from MAIN, exactly as written. On anything other than the expected output and exit code 0: **STOP**, record the output, and go to step 11 (clean-up). Never retry, repair or reorder a step.

**Recording** (so that nothing improvised is needed):
- Write `CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T023.md` as you go: after each step, add its command, its exit code and its full output, before starting the next step.
- Exit codes: the program's own. Do not pipe a command into another program (no `| tee`); in Git Bash, `echo $?` straight after the command gives its exit code.
- Step 9 is longer than the shell's foreground limit, so its command line already carries its own recording: run that exact line as one background command in Git Bash, and wait until the background command has finished. Its output and, on the last line, the suite runner's own exit status (`RUNNER EXIT CODE <n>`, written by the same shell straight after the runner ends) are in `scratch\T023\suite_output.txt`. Copy the whole file into the report before step 10. If that last line is missing or is not `RUNNER EXIT CODE 0`, that is a STOP: never infer a pass from the other lines, and never take an exit status from another shell or from the launch of the background command. The file goes with the clean-up.

## Steps

**1. Python.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.platform())"
```
Expected: the venv path, a Python version, and a Windows platform line.

**2. The main repository's state** (read-only; record the output; this step does not stop the task).
```
git status --short
git rev-parse HEAD
git log -1 --format=%s
```

**3. Make the task clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T023
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines (the same commit), the `core.autocrlf` line, then `MAKE PASS`.

**4. Check and extract the reviewed fix** (from the clone's own copy).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T023 --zip exchange/CLAUDE_WEB_TOOLS/mhupa/postinstall/fix_tests_r1/MHUPA_TESTFIX_r1.zip --sha256 839a31c3fc7ed75a27fbe66c2323ad0450411449f3fe9e6701ea6f0dcb2d452e
```
Expected: `ZIP SHA-256: 839a31c3fc7ed75a27fbe66c2323ad0450411449f3fe9e6701ea6f0dcb2d452e`, then `UNZIP PASS: 3 files extracted into ...`.

**5. Put the two reviewed test files into the clone** (the plan file names the two tracked files they replace).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T023 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\p\MHUPA_TESTFIX_r1\overlay" --plan exchange/CLAUDE_WEB_TOOLS/mhupa/postinstall/fix_tests_r1/TASK_T023_overlay_plan.txt
```
Expected: `plan ...: 2 REPLACE, 0 REMOVE; SHA-256 ...`, then `OVERLAY PASS: 2 files copied into ... (0 new, 2 replaced); 0 tracked file(s) removed with git rm`.

**6. The two files are in place** (read-only).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" verify-overlay --task T023 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\p\MHUPA_TESTFIX_r1\overlay" --plan exchange/CLAUDE_WEB_TOOLS/mhupa/postinstall/fix_tests_r1/TASK_T023_overlay_plan.txt
```
Expected: `plan ...: 2 REPLACE, 0 REMOVE; ...`, then `VERIFY-OVERLAY PASS: 2 overlay files identical in the clone; 0 removed file(s) absent`.

**7. The two files' SHA-256 in the clone** (read-only; the clone's copy of each file the fix carries).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import hashlib, pathlib; r = pathlib.Path(r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r'); o = pathlib.Path(r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\p\MHUPA_TESTFIX_r1') / 'overlay'; [print(hashlib.sha256((r / f.relative_to(o)).read_bytes()).hexdigest(), f.relative_to(o).as_posix()) for f in sorted(o.rglob('*.py'))]"
```
Expected exactly: `a0923a5ba576a0c48c72b05ca982b156ffd4510616dba92780c8993811e9c44e tests/mhupa_slice2_fixtures.py` and `c82231a1e33e1ecc1d2bbda790baf3f80e1c7bfcdf3ec573befa992e2d432b47 tests/test_mhupa_install_records.py` (the values the reviewer checked, EX_165). Any other value: STOP.

**8. Module origin** (the tests must use the clone's code, not the main repository's).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r"
```
Expected: every module line starts `ok`, then `ORIGIN PASS`.

**9. All 571 tests, including E2R-T12** (about 25 minutes; run this one line as a single background command in Git Bash; see "Recording").
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\p\MHUPA_TESTFIX_r1\tools\RUN_MHUP_A_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r" > "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T023/suite_output.txt" 2>&1; echo "RUNNER EXIT CODE $?" >> "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T023/suite_output.txt"
```
Expected, in the file `scratch\T023\suite_output.txt` once the command has ended: as its last line `RUNNER EXIT CODE 0` (the suite runner's own exit status, written by the same shell straight after it); before it, one line per module, then `total ran 571 (expected 571); ...` and `SUITE PASS: all 571 tests ran and passed; only the allowed symlink skips, if any.` Up to 4 symlink skips are allowed on Windows; the runner itself decides. Record the whole output as printed. If it prints failure detail, copy it exactly (test names and messages only; if any line appears to contain a draw's numbers, put `[line withheld: possible data value]` instead and say so under Deviations).

**10. The clone has no other tracked change and no new untracked file** (read-only; Git-ignored files are not examined).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T023 -- status --short
```
Expected: between the GUARD lines exactly two lines, ` M tests/mhupa_slice2_fixtures.py` and ` M tests/test_mhupa_install_records.py`, and nothing else (no other changed file, no `??` line); then `GUARD PASS (after); git status exit code 0`. Any other line: STOP and report it; never delete anything to obtain a pass.

## Clean-up (always, whether the task passed or stopped)

**11. Remove the task clone and the extracted fix.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T023
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, do not run step 13, and tell the project owner.

## Report

**12. Finish** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T023.md` in the format of `outbox\README.md` (the step table and the RESULT line at the top). Also record:
- the wall-clock time of step 9;
- whether the main repository's `git status --short` after step 11 is the same as in step 2 (run it again and include it).

## Finish

**13. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T023
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**14. Tell the project owner** the RESULT line, the report's path, and: "please push".
