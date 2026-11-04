# TASK_T018 - Windows suite run of the reviewed MHUP-A slice 1 code, in a task clone (read-only check)

**Task ID:** T018. **Date:** 5 November 2026. **Author:** the Claude web chat. (T016 and T017 stay reserved by the ratified MHUP-1 design for the Windows rehearsals of the MHUP-A and MHUP-B install packages; this task is neither.)

**Purpose.** Run the whole test suite on the owner's Windows machine with the MHUP-A slice 1 code applied, in a disposable task clone that cannot push, so the main repository is not changed at all. Slice 1 passed the reviewer's focused recheck (EX_146, 5 November 2026). The code is the reviewed candidate `exchange/EX_145_Claude/MHUPA_Slice1_Review_v1r2.zip`, whose `overlay/` folder holds 20 new files and 26 replacements of tracked files.

The one fact this checks that the Claude web chat cannot check from its own workspace: slice 1 applies the full ledger grammar to every master ledger, and the project's accepted tests read the two committed development masters and their ledgers through the project's reader (rulebook rule 2.5). So a passing suite here shows that the real committed ledgers pass the new, stricter rules on Windows. A refusal is a STOP and is reported; nothing is relaxed or worked around.

This is **not an install rehearsal**. It installs nothing, stages nothing, commits nothing in the clone, runs no verifier, no report, no batch, no updater and no program other than the tests, and reads no real data itself.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish normally) is run in step 8, as in T008 to T015. The project owner approves it for this run by giving this task.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| TOOLS | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools` |
| CLONE (the task clone) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r` |
| PKG (the extracted candidate) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\p\MHUPA_Slice1_Review_v1r2` |

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
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T018
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines, the `core.autocrlf` line, then `MAKE PASS`.

**4. Check and extract the candidate** (from the clone's own copy).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T018 --zip exchange/EX_145_Claude/MHUPA_Slice1_Review_v1r2.zip --sha256 5fbaaae1c51a325017b03593d75a09753e4e584bb5e6816ec6480cf78765fb7b
```
Expected: `ZIP SHA-256: 5fbaaae1...fb7b`, then `UNZIP PASS: 75 files extracted ...`.

**5. Copy the overlay** (20 new files and the 26 named replacements).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T018 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\p\MHUPA_Slice1_Review_v1r2\overlay" --replace src/evaluation/outcome_reader.py src/evaluation/report.py src/methods/E_001/multigame_e1.py src/methods/E_001_Historical_Appearance_Frequency.py src/methods/Method_Contract_Runner.py src/methods/_common/contract_dispatch.py src/methods/_common/contract_forecast.py src/methods/_common/contract_receipts.py src/methods/_common/contract_records.py src/methods/_common/contract_runner.py src/methods/_common/contract_task.py src/methods/_common/contract_vocab.py src/methods/_common/game_draws_reader.py src/methods/_common/walk_forward.py src/methods/contract_adapters/e_001.py tests/test_code3_retirement.py tests/test_e1r2_revision2.py tests/test_e2r_dispatch.py tests/test_e2r_runner.py tests/test_e6_beta_bernoulli.py tests/test_multigame_reader_contracts.py tests/test_rel1_release.py tests/test_t05_hardening.py tests/test_wf1a_walk_forward.py tests/test_wf1b_outcome_reader.py tests/test_wf1b_static.py
```
Expected: `OVERLAY PASS: 46 files copied into ... (20 new, 26 replaced)`.

**6. Module origin** (the tests must use the clone's code, not the main repository's).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r"
```
Expected: every module line starts `ok`, then `ORIGIN PASS`.

**7. The slice 1 code is in place** (read-only).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import pathlib; r = pathlib.Path(r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r'); t = (r / 'src' / 'methods' / '_common' / 'master_versions.py').read_text(encoding='ascii'); print('strict=True' in t, '_render' in t, (r / 'src' / 'methods' / '_common' / 'owner_records.py').is_file(), (r / 'archive' / 'methods' / 'E_001' / 'r2' / 'README.md').is_file())"
```
Expected: `True True True True`.

**8. All 507 tests, including E2R-T12** (the candidate's own runner).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\p\MHUPA_Slice1_Review_v1r2\tools\RUN_MHUPA_SLICE1_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r"
```
Expected: `SUITE PASS: all 507 tests ran and passed; only the allowed symlink skips, if any.` Up to 4 symlink skips are allowed on Windows; the runner itself decides, so record its output as printed, including each module's time. Record exactly the lines for `tests.test_multigame_reader_contracts`, `tests.test_wf1a_walk_forward`, `tests.test_mhupa_master_versions`, `tests.test_mhupa_gates` and `tests.test_e1r3_revision3`. If the runner prints failure detail, copy it exactly as printed (it carries test names and messages only; if any line appears to contain a draw's numbers, replace that line with `[line withheld: possible data value]` and say so under Deviations).

**9. The clone is otherwise unchanged by the run** (read-only).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T018 -- status --short --untracked-files=no
```
Expected: 26 lines, each starting ` M` (the 26 replacements of step 5), and `git status exit code 0`. Copy the whole output exactly as printed.

## Clean-up (always, whether the task passed or stopped)

**10. Remove the task clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T018
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, and do not run step 12; tell the project owner.

## Report

**11. Write** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T018.md` in the format of `outbox\README.md`, with every step's command, exit code and full output (step 8 as described there). Also record:
- the wall-clock time step 8 took;
- whether the main repository's `git status --short` after step 10 is the same as in step 2 (run it again and include it).

## Finish

**12. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T018
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**13. Tell the project owner** the RESULT line, the report's path, and: "please push".
