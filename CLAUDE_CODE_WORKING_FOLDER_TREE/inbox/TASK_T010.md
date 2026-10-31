# TASK_T010 - Windows rehearsal of the WF-1A install, in a task clone

**Task ID:** T010. **Date:** 31 October 2026. **Author:** the Claude web chat. The same pattern as T009, for the FINAL WF-1A package v2 (`WF1A_Install_v2`: the walk-forward driver, and the contract's real-development switch turned on, owner decision WF1-3), built on the project owner's REL-1 install commit `6a1bed9`. It adds 10 files and replaces 5 (named in step 6 with `--replace`, `.gitignore` among them); it deletes nothing. As in T009, step 11 asks for the whole status output, copied as printed.

**Purpose.** Run the final WF-1A install package (`CLAUDE_CODE_WORKING_FOLDER_TREE/packages/WF1A_Install_v2.zip`) on the owner's Windows machine, but in a disposable task clone that cannot push, so the main repository is not changed at all. It is a rehearsal only: it installs nothing, turns nothing on in the main repository, runs no batch and reads no real data. The suite's walk-forward tests run invented batches in temporary folders only.

It differs from the owner's real install in three ways: it runs in a task clone, not the main repository; files are copied by `tools\cc_clone.py overlay`, not `xcopy`; and there is no `git pull` and no push. All 326 tests run, including E2R-T12.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish normally) is run in step 9, as in T008 and T009. The project owner approves it for this rehearsal by giving this task.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| TOOLS | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools` |
| CLONE (the task clone) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T010\r` |
| PKG (the extracted package) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T010\p\WF1A_Install_v2` |

The commands below are written out in full. Run each from MAIN (your normal workspace folder). On anything other than the expected PASS line, or a non-zero exit code: **STOP**, record the output, and go to step 15 (clean-up).

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
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T010
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines, the `core.autocrlf` line, then `MAKE PASS`.

**4. Check and extract the package** (from the clone's own copy).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T010 --zip CLAUDE_CODE_WORKING_FOLDER_TREE/packages/WF1A_Install_v2.zip --sha256 9fa6577ab95d5a16931a6df7c056764f06a61282e2f78a497b2292610a9e3c06
```
Expected: `ZIP SHA-256: 9fa6577a...3c06`, then `UNZIP PASS: 18 files extracted ...`.

**5. PRE check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" guard --task T010
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T010\p\WF1A_Install_v2\VERIFY_WF1A_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T010\r" --phase pre
```
Expected: `GUARD PASS`, then `PRE PASS`.

**6. Copy the overlay into the clone** (10 new files, and the 5 named replacements).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T010 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T010\p\WF1A_Install_v2\repo_overlay" --replace src/methods/_common/contract_runner.py src/methods/Method_Contract_Runner.py .gitignore tests/test_e2r_runner.py tests/test_e2r_dispatch.py
```
Expected: `OVERLAY PASS: 15 files copied into ... (10 new, 5 replaced)`.

**7. POST check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T010\p\WF1A_Install_v2\VERIFY_WF1A_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T010\r" --phase post
```
Expected: `POST PASS: exactly the 10 expected new paths, 5 modified files and 0 staged deletions, all with the expected bytes.`

**8. Module origin** (the tests must use the clone's code, not the main repository's).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T010\r"
```
Expected: every module line starts `ok`, the contract-data and registry lines (80 declarations and 202 registry chains), then `ORIGIN PASS`.

**9. All 326 tests, including E2R-T12** (the package's own runner).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T010\p\WF1A_Install_v2\RUN_WF1A_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T010\r"
```
Expected: `SUITE PASS: all 326 tests ran and passed`. Up to 3 symlink skips are allowed on Windows; the runner itself decides, so record its output as printed, including each module's time.

**10. Stage in the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T010 -- add .gitignore review src tests
```
Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git add exit code 0`.

**11. Status in the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T010 -- status --short
```
Expected: 15 lines: 10 starting with `A` and 5 starting with `M` (`.gitignore`, the two runner files and the two test files), and `git status exit code 0`. In the report, copy the whole output exactly as printed, all 15 lines. Do not redirect the output to a file and do not count it with another command; Claude checks the counts from the report.

**12. Commit in the clone** (this commit exists only in the task clone and is deleted with it).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T010 -- commit -q -m "WF-1A rehearsal (task clone T010 only; never pushed)"
```
Expected: `git commit exit code 0`.

**13. COMMITTED check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T010\p\WF1A_Install_v2\VERIFY_WF1A_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T010\r" --phase committed
```
Expected: `COMMITTED PASS`. (In a task clone, if this STOPs, the identity report's "upstream" lines will say there is no upstream; that is expected and is not the cause.)

**14. Final state of the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T010 -- log --oneline -2
```
Expected: the rehearsal commit on top of the clone's starting commit, and `git log exit code 0`.

## Clean-up (always, whether the task passed or stopped)

**15. Remove the task clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T010
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, and do not run step 17; tell the project owner.

## Report

**16. Write** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T010.md` in the format of `outbox\README.md`, with every step's command, exit code and full output (step 11 as described there). Also record:
- the wall-clock time step 9 took;
- whether the main repository's `git status --short` after step 15 is the same as in step 2 (run it again and include it).

## Finish

**17. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T010
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**18. Tell the project owner** the RESULT line, the report's path, and: "please push".
