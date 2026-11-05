# TASK_T021 - Windows suite run of the MHUP-A slice 2 candidate (slice 1 included), in a task clone (read-only check)

**Task ID:** T021. **Date:** 5 November 2026. **Author:** the Claude web chat. The same read-only Windows suite run as TASK_T020 (PASS, `cba73e5`), for the corrected slice 2 candidate v1r1 sent as EX_149 after the reviewer's EX_148. The paths to replace and to remove are again read by the clone tool from a plan file, `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T021_overlay_plan.txt`. (T016 and T017 stay reserved for the install rehearsals.)

**Purpose.** Run the whole test suite on the owner's Windows machine with the MHUP-A slice 2 candidate applied (it includes the reviewed slice 1 code), in a disposable task clone that cannot push, so the main repository is not changed at all. Candidate v1r1 has been sent for review as EX_149 (5 November 2026); this run does not wait for that review and does not depend on it. The code is the candidate `exchange/EX_149_Claude/MHUPA_Slice2_Review_v1r1.zip`, whose `overlay/` folder holds 37 new files and 33 replacements of tracked files; the candidate also removes one tracked file, `src/results_master_v0_1.py` (replaced by `src/results_master_v0_2.py`), which the clone tool's overlay command removes in the clone (`git rm`, inside the task clone only) because the plan file says `REMOVE` for it.

What this checks that the Claude web chat cannot check from its own workspace: slice 2's 62 new tests on Windows with the project's own Python 3.15 (the updater v0.2's offline self-test and its emitted-bytes reconciliation, the byte-code-cache rule with the Windows interpreter, the process tool's mocked tables under Windows path rules, the records tool on temporary Git repositories, the Mode H study on invented masters in temporary folders), together with slice 1's 507 tests again. A failure is a STOP and is reported; nothing is relaxed or worked around.

This is **not an install rehearsal**. It installs nothing, stages nothing, commits nothing in the clone, runs no verifier, no report tool, no batch, no updater and no program other than the tests (the tests themselves start the updater's offline `--self-test` and small Python child processes on invented data, as they are written to), and reads no real data itself. No lottery website is contacted; nothing here has a browser.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish normally) is run in step 8, as in T008 to T018. The project owner approves it for this run by giving this task. The Mode H test module runs about four 60-run synthetic batches and takes several minutes on its own.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| TOOLS | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools` |
| CLONE (the task clone) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T021\r` |
| PKG (the extracted candidate) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T021\p\MHUPA_Slice2_Review_v1r1` |

The commands below are written out in full. Run each from MAIN (your normal workspace folder). On anything other than the expected PASS line, or a non-zero exit code: **STOP**, record the output, and go to step 10 (clean-up).

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
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T021
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines, the `core.autocrlf` line, then `MAKE PASS`.

**4. Check and extract the candidate** (from the clone's own copy).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T021 --zip exchange/EX_149_Claude/MHUPA_Slice2_Review_v1r1.zip --sha256 0b6d9d28636459d72cb4aafabb1ef8a8dd8bc2c2923c1db927a8a2498e548fde
```
Expected: `ZIP SHA-256: 0b6d9d28...`, then `UNZIP PASS: 133 files extracted ...`.

**5. Copy the overlay** (37 new files, the 33 replacements and the one removal named in the plan file).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T021 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T021\p\MHUPA_Slice2_Review_v1r1\overlay" --plan CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T021_overlay_plan.txt
```
Expected: `plan ...: 33 REPLACE, 1 REMOVE; SHA-256 ...`, then `OVERLAY PASS: 70 files copied into ... (37 new, 33 replaced); 1 tracked file(s) removed with git rm`.

**6. Module origin** (the tests must use the clone's code, not the main repository's).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T021\r"
```
Expected: every module line starts `ok`, then `ORIGIN PASS`.

**7. The slice 2 code is in place** (read-only; the clone tool compares every overlay file with the clone and checks the removal).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" verify-overlay --task T021 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T021\p\MHUPA_Slice2_Review_v1r1\overlay" --plan CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T021_overlay_plan.txt
```
Expected: `plan ...: 33 REPLACE, 1 REMOVE; ...`, then `VERIFY-OVERLAY PASS: 70 overlay files identical in the clone; 1 removed file(s) absent`.

**8. All 569 tests, including E2R-T12** (the candidate's own runner).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T021\p\MHUPA_Slice2_Review_v1r1\tools\RUN_MHUPA_SLICE2_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T021\r"
```
Expected: `SUITE PASS: all 569 tests ran and passed; only the allowed symlink skips, if any.` Up to 4 symlink skips are allowed on Windows; the runner itself decides, so record its output as printed, including each module's time. Record exactly the lines for `tests.test_mhupa_updater_v0_2`, `tests.test_mhupa_launchers`, `tests.test_mhupa_mode_h`, `tests.test_mhupa_process_check`, `tests.test_mhupa_install_records` and `tests.test_mhupa_method_mode_h_cli`. If the runner prints failure detail, copy it exactly as printed (it carries test names and messages only; if any line appears to contain a draw's numbers, replace that line with `[line withheld: possible data value]` and say so under Deviations).

**9. The clone is otherwise unchanged by the run** (read-only).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T021 -- status --short --untracked-files=no
```
Expected: 34 lines: 33 starting ` M` (the replacements of step 5) and one `D ` line for the file the plan removes (step 5), and `git status exit code 0`. Copy the whole output exactly as printed.

## Clean-up (always, whether the task passed or stopped)

**10. Remove the task clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T021
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, and do not run step 12; tell the project owner.

## Report

**11. Write** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T021.md` in the format of `outbox\README.md`, with every step's command, exit code and full output (step 9 as described there). Also record:
- the wall-clock time step 8 took;
- whether the main repository's `git status --short` after step 10 is the same as in step 2 (run it again and include it).

## Finish

**12. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T021
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**13. Tell the project owner** the RESULT line, the report's path, and: "please push".
