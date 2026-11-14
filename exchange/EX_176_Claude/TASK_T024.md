# TASK_T024 - after the owner's dependency change: the environment freeze check and the whole suite on Windows, in a task clone (no change to the main repository)

**Task ID:** T024. **Date:** 14 November 2026. **Author:** the Claude web chat. Rulebook v0.5; section 2A (T016 only) does not apply.

**Purpose.** On 14 November 2026 the project owner ran his edited dependency installer, which installed or upgraded many packages in the project venv. The project rule after any dependency change is to stop until the offline suite passes, and Mode H freezes the venv at Approval 1, refusing any file under site-packages that no package RECORD lists. This task checks both on Windows, with the venv as it now is: (a) the environment freeze check, read-only, exactly as Mode H's `manifest` would make it; (b) the whole suite (571 tests) in a disposable task clone of `main` that cannot push. It changes no package and no file of the main repository.

**What it does not do.** It changes nothing in the main repository (only this task's report is committed there). It runs no launcher, coordinator, updater, Mode H command, process tool, records tool, report tool or `.bat`, and no other program than the ones below (the tests themselves start the updater's offline self-test and small Python workers on invented data, as they are written to). It reads no real data itself and contacts no website. "No change" means the main repository: the clone and the tests write to their own temporary folders. It never runs `pip` or any installer, and changes no venv.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish by themselves) runs in step 7. The project owner approves it for this run by giving this task.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| TOOLS | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools` |
| CLONE (the task clone) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T024\r` |
| PKG (the extracted T023 package; its runner only) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T024\p\MHUPA_TESTFIX_r1` |

Run each command from MAIN, exactly as written. On anything other than the expected output and exit code 0: **STOP**, record the output, and go to step 9 (clean-up). Step 6 is the one exception, as it says. Never retry, repair or reorder a step.

**Recording** (so that nothing improvised is needed):
- Write `CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T024.md` as you go: after each step, add its command, its exit code and its full output, before starting the next step.
- Exit codes: the program's own. Do not pipe a command into another program (no `| tee`); in Git Bash, `echo $?` straight after the command gives its exit code.
- Step 7 is longer than the shell's foreground limit, so its command line already carries its own recording: run that exact line as one background command in Git Bash, and wait until the background command has finished. Its output and, on the last line, the suite runner's own exit status (`RUNNER EXIT CODE <n>`, written by the same shell straight after the runner ends) are in `scratch\T024\suite_output.txt`. Copy the whole file into the report before step 8. If that last line is missing or is not `RUNNER EXIT CODE 0`, that is a STOP: never infer a pass from the other lines, and never take an exit status from another shell or from the launch of the background command. The file goes with the clean-up.

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
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T024
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines (the same commit), the `core.autocrlf` line, then `MAKE PASS`.

**4. Extract the suite runner** (from the clone's own copy of the reviewed T023 package; only its runner is used, nothing is put into the clone).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T024 --zip exchange/CLAUDE_WEB_TOOLS/mhupa/postinstall/fix_tests_r1/MHUPA_TESTFIX_r1.zip --sha256 839a31c3fc7ed75a27fbe66c2323ad0450411449f3fe9e6701ea6f0dcb2d452e
```
Expected: `ZIP SHA-256: 839a31c3fc7ed75a27fbe66c2323ad0450411449f3fe9e6701ea6f0dcb2d452e`, then `UNZIP PASS: 3 files extracted into ...`.

**5. Module origin** (the tests must use the clone's code, not the main repository's).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T024\r"
```
Expected: every module line starts `ok`, then `ORIGIN PASS`.

**6. The environment freeze check** (read-only; the clone's copy of the check; it reads the venv and its base Python only, and prints package names, versions, file names and one digest).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T024\r\exchange\CLAUDE_WEB_TOOLS\deps_2026_11_14\env_freeze_check.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T024\r"
```
Expected: either `ENV PASS: <n> distributions, no orphan, ...; environment digest <64 hex>` with exit code 0, or `ENV REFUSED: ...` followed by a list of problems, with exit code 3. **Both are findings, not a STOP:** record the whole output and go on to step 7. Any other output or exit code (a traceback, `USAGE`) is a STOP.

**7. All 571 tests, including E2R-T12** (about 25 minutes; run this one line as a single background command in Git Bash; see "Recording").
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T024\p\MHUPA_TESTFIX_r1\tools\RUN_MHUP_A_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T024\r" > "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T024/suite_output.txt" 2>&1; echo "RUNNER EXIT CODE $?" >> "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T024/suite_output.txt"
```
Expected, in the file `scratch\T024\suite_output.txt` once the command has ended: as its last line `RUNNER EXIT CODE 0` (the suite runner's own exit status, written by the same shell straight after it); before it, one line per module, then `total ran 571 (expected 571); ...` and `SUITE PASS: all 571 tests ran and passed; only the allowed symlink skips, if any.` Up to 4 symlink skips are allowed on Windows; the runner itself decides. Record the whole output as printed. If it prints failure detail, copy it exactly (test names and messages only; if any line appears to contain a draw's numbers, put `[line withheld: possible data value]` instead and say so under Deviations).

**8. The clone has no tracked change and no new untracked file** (read-only; Git-ignored files are not examined).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T024 -- status --short
```
Expected: nothing between the GUARD lines; then `GUARD PASS (after); git status exit code 0`. Any other line: STOP and report it; never delete anything to obtain a pass.

## Clean-up (always, whether the task passed or stopped)

**9. Remove the task clone and the extracted package.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T024
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, do not run step 11, and tell the project owner.

## Report

**10. Finish** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T024.md` in the format of `outbox\README.md` (the step table and the RESULT line at the top). Also record:
- the wall-clock time of step 7;
- whether the main repository's `git status --short` after step 9 is the same as in step 2 (run it again and include it).

## Finish

**11. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T024
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**12. Tell the project owner** the RESULT line, the report's path, and: "please push".
