# TASK_T019 - Windows suite run of the MHUP-A slice 2 candidate (slice 1 included), in a task clone (read-only check)

**Task ID:** T019. **Date:** 5 November 2026 (after T018 PASSED). **Author:** the Claude web chat. (T016 and T017 stay reserved by the ratified MHUP-1 design for the Windows rehearsals of the MHUP-A and MHUP-B install packages; this task is neither.)

**Purpose.** Run the whole test suite on the owner's Windows machine with the MHUP-A slice 2 candidate applied (it includes the reviewed slice 1 code), in a disposable task clone that cannot push, so the main repository is not changed at all. Slice 2 has been sent for review as EX_147 (5 November 2026); this run does not wait for that review and does not depend on it. The code is the candidate `exchange/EX_147_Claude/MHUPA_Slice2_Review_v1.zip`, whose `overlay/` folder holds 36 new files and 33 replacements of tracked files; the candidate also removes one tracked file, `src/results_master_v0_1.py` (replaced by `src/results_master_v0_2.py`), which step 6 does in the clone with the clone tool's `git rm`.

What this checks that the Claude web chat cannot check from its own workspace: slice 2's 54 new tests on Windows with the project's own Python 3.15 (the updater v0.2's offline self-test and its emitted-bytes reconciliation, the byte-code-cache rule with the Windows interpreter, the process tool's mocked tables under Windows path rules, the records tool on temporary Git repositories, the Mode H study on invented masters in temporary folders), together with slice 1's 507 tests again. A failure is a STOP and is reported; nothing is relaxed or worked around.

This is **not an install rehearsal**. It installs nothing, stages nothing, commits nothing in the clone, runs no verifier, no report tool, no batch, no updater and no program other than the tests (the tests themselves start the updater's offline `--self-test` and small Python child processes on invented data, as they are written to), and reads no real data itself. No lottery website is contacted; nothing here has a browser.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish normally) is run in step 9, as in T008 to T018. The project owner approves it for this run by giving this task. The Mode H test module runs about four 60-run synthetic batches and takes several minutes on its own.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| TOOLS | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools` |
| CLONE (the task clone) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T019\r` |
| PKG (the extracted candidate) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T019\p\MHUPA_Slice2_Review_v1` |

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
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T019
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines, the `core.autocrlf` line, then `MAKE PASS`.

**4. Check and extract the candidate** (from the clone's own copy).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T019 --zip exchange/EX_147_Claude/MHUPA_Slice2_Review_v1.zip --sha256 94fd6c0751dcd46c724d27d95031dcb5d0207727fb7c2ac279e03ef24aa2db96
```
Expected: `ZIP SHA-256: 94fd6c07...`, then `UNZIP PASS: 127 files extracted ...`.

**5. Copy the overlay** (36 new files and the 33 named replacements).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T019 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T019\p\MHUPA_Slice2_Review_v1\overlay" --replace .gitignore Run_Experiment.bat Run_Results_Updater.bat src/evaluation/collect.py src/evaluation/outcome_reader.py src/evaluation/registry/FAMILY_REGISTRY_V1.json src/evaluation/report.py src/evaluation/report_writer.py src/methods/E_001/multigame_e1.py src/methods/E_001_Historical_Appearance_Frequency.py src/methods/Method_Contract_Runner.py src/methods/Method_Walk_Forward.py src/methods/_common/contract_dispatch.py src/methods/_common/contract_forecast.py src/methods/_common/contract_receipts.py src/methods/_common/contract_records.py src/methods/_common/contract_runner.py src/methods/_common/contract_task.py src/methods/_common/contract_vocab.py src/methods/_common/game_draws_reader.py src/methods/_common/walk_forward.py src/methods/contract_adapters/e_001.py tests/test_code3_retirement.py tests/test_e1r2_revision2.py tests/test_e2r_dispatch.py tests/test_e2r_runner.py tests/test_e6_beta_bernoulli.py tests/test_multigame_reader_contracts.py tests/test_rel1_release.py tests/test_t05_hardening.py tests/test_wf1a_walk_forward.py tests/test_wf1b_outcome_reader.py tests/test_wf1b_static.py
```
Expected: `OVERLAY PASS: 69 files copied into ... (36 new, 33 replaced)`.

**6. Remove the old updater file in the clone** (the candidate replaces it; through the clone tool, which checks the clone first).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T019 -- rm -q src/results_master_v0_1.py
```
Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git rm exit code 0`.

**7. Module origin** (the tests must use the clone's code, not the main repository's).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T019\r"
```
Expected: every module line starts `ok`, then `ORIGIN PASS`.

**8. The slice 2 code is in place** (read-only).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import pathlib; r = pathlib.Path(r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T019\r'); print((r / 'src' / 'results_master_v0_2.py').is_file(), not (r / 'src' / 'results_master_v0_1.py').exists(), (r / 'src' / 'evaluation' / 'Method_Mode_H.py').is_file(), (r / 'src' / 'package_tools' / 'process_check.py').is_file(), (r / 'Run_Evaluation.bat').is_file(), 'results_master_v0_2' in (r / 'Run_Results_Updater.bat').read_text(encoding='ascii'))"
```
Expected: `True True True True True True`.

**9. All 561 tests, including E2R-T12** (the candidate's own runner).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T019\p\MHUPA_Slice2_Review_v1\tools\RUN_MHUPA_SLICE2_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T019\r"
```
Expected: `SUITE PASS: all 561 tests ran and passed; only the allowed symlink skips, if any.` Up to 4 symlink skips are allowed on Windows; the runner itself decides, so record its output as printed, including each module's time. Record exactly the lines for `tests.test_mhupa_updater_v0_2`, `tests.test_mhupa_launchers`, `tests.test_mhupa_mode_h`, `tests.test_mhupa_process_check`, `tests.test_mhupa_install_records` and `tests.test_mhupa_method_mode_h_cli`. If the runner prints failure detail, copy it exactly as printed (it carries test names and messages only; if any line appears to contain a draw's numbers, replace that line with `[line withheld: possible data value]` and say so under Deviations).

**10. The clone is otherwise unchanged by the run** (read-only).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T019 -- status --short --untracked-files=no
```
Expected: 34 lines: 33 starting ` M` (the replacements of step 5) and one `D  src/results_master_v0_1.py` (step 6), and `git status exit code 0`. Copy the whole output exactly as printed.

## Clean-up (always, whether the task passed or stopped)

**11. Remove the task clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T019
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, and do not run step 13; tell the project owner.

## Report

**12. Write** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T019.md` in the format of `outbox\README.md`, with every step's command, exit code and full output (step 9 as described there). Also record:
- the wall-clock time step 9 took;
- whether the main repository's `git status --short` after step 11 is the same as in step 2 (run it again and include it).

## Finish

**13. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T019
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**14. Tell the project owner** the RESULT line, the report's path, and: "please push".
