# REPORT_T023 - Windows suite run of the reviewed MHUP-A post-install test fix r1, in a task clone (no change to the main repository)

RESULT: PASS

- Task file: inbox/TASK_T023.md at main-repository commit 95c35cae742ab53acf5e8588e4d8628b381b3e64
- Run by: Claude Code (local runner), 13 November 2026, started 20:58 local time (UTC+10:30)
- Owner options used: none (the task file lists no owner options; E2R-T12 is approved for this run by the task being given)
- Machine: Windows-11-10.0.26300-SP0; Python 3.15.2 at E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | Python | 0 | venv path, Python 3.15.2, Windows platform line |
| 2 | Main repository state (read-only) | 0, 0, 0 | one `??` line (this report); HEAD 95c35cae742ab53acf5e8588e4d8628b381b3e64 |
| 3 | Make the task clone | 0 | MAKE PASS |
| 4 | Check and extract the reviewed fix | 0 | UNZIP PASS: 3 files extracted |
| 5 | Overlay the two reviewed test files | 0 | OVERLAY PASS: 2 files copied (0 new, 2 replaced) |
| 6 | Verify the overlay | 0 | VERIFY-OVERLAY PASS: 2 overlay files identical |
| 7 | SHA-256 of the two files in the clone | 0 | both values as given in the task file |
| 8 | Module origin | 0 | ORIGIN PASS |
| 9 | All 571 tests, including E2R-T12 | 0 | SUITE PASS: all 571 tests ran and passed; 4 allowed symlink skips; RUNNER EXIT CODE 0 |
| 10 | The clone has no other change | 0 | exactly the two expected ` M` lines; GUARD PASS (after) |
| 11 | Clean-up: remove the task clone | 0 | REMOVE PASS |
| 12 | Main repository status after clean-up | 0 | the same as step 2 |

## Outputs

### Step 1

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.platform())"
```

Output:

```text
E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
3.15.2 (tags/v3.15.2:5e58eaa, Oct 25 2026, 17:27:03) [MSC v.1951 64 bit (AMD64)]
Windows-11-10.0.26300-SP0
```

Exit code: 0

### Step 2

Read-only; this step does not stop the task.

Command:

```text
git status --short
```

Output:

```text
?? CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T023.md
```

Exit code: 0

Command:

```text
git rev-parse HEAD
```

Output:

```text
95c35cae742ab53acf5e8588e4d8628b381b3e64
```

Exit code: 0

Command:

```text
git log -1 --format=%s
```

Output:

```text
TASK_T023 into the inbox after EX_166 (T023-C01: the runner's own exit status recorded by the same shell; T023-C02: status without --untracked-files=no)
```

Exit code: 0

Note: the one `??` line is this report file, which the task requires to be written as the run proceeds.

### Step 3

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T023
```

Output:

```text
cloning from https://github.com/hydra3333/analysing_perceived_randomness_in_reality
GUARD PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r is a task clone with no remote and a refusing pre-push hook
git remote -v: ''
clone HEAD: 95c35cae742ab53acf5e8588e4d8628b381b3e64
main repository HEAD: 95c35cae742ab53acf5e8588e4d8628b381b3e64
core.autocrlf in the clone: true
MAKE PASS
```

Exit code: 0

### Step 4

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T023 --zip exchange/CLAUDE_WEB_TOOLS/mhupa/postinstall/fix_tests_r1/MHUPA_TESTFIX_r1.zip --sha256 839a31c3fc7ed75a27fbe66c2323ad0450411449f3fe9e6701ea6f0dcb2d452e
```

Output:

```text
ZIP SHA-256: 839a31c3fc7ed75a27fbe66c2323ad0450411449f3fe9e6701ea6f0dcb2d452e
UNZIP PASS: 3 files extracted into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\p
```

Exit code: 0

### Step 5

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T023 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\p\MHUPA_TESTFIX_r1\overlay" --plan exchange/CLAUDE_WEB_TOOLS/mhupa/postinstall/fix_tests_r1/TASK_T023_overlay_plan.txt
```

Output:

```text
plan exchange/CLAUDE_WEB_TOOLS/mhupa/postinstall/fix_tests_r1/TASK_T023_overlay_plan.txt: 2 REPLACE, 0 REMOVE; SHA-256 f1e4a50ff558713753ec1ee890ad4d6ea3ffdb37bbb755b0e8530f61d54e6170
OVERLAY PASS: 2 files copied into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r (0 new, 2 replaced); 0 tracked file(s) removed with git rm
```

Exit code: 0

### Step 6

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" verify-overlay --task T023 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\p\MHUPA_TESTFIX_r1\overlay" --plan exchange/CLAUDE_WEB_TOOLS/mhupa/postinstall/fix_tests_r1/TASK_T023_overlay_plan.txt
```

Output:

```text
plan exchange/CLAUDE_WEB_TOOLS/mhupa/postinstall/fix_tests_r1/TASK_T023_overlay_plan.txt: 2 REPLACE, 0 REMOVE; SHA-256 f1e4a50ff558713753ec1ee890ad4d6ea3ffdb37bbb755b0e8530f61d54e6170
VERIFY-OVERLAY PASS: 2 overlay files identical in the clone; 0 removed file(s) absent
```

Exit code: 0

### Step 7

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import hashlib, pathlib; r = pathlib.Path(r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r'); o = pathlib.Path(r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\p\MHUPA_TESTFIX_r1') / 'overlay'; [print(hashlib.sha256((r / f.relative_to(o)).read_bytes()).hexdigest(), f.relative_to(o).as_posix()) for f in sorted(o.rglob('*.py'))]"
```

Output:

```text
a0923a5ba576a0c48c72b05ca982b156ffd4510616dba92780c8993811e9c44e tests/mhupa_slice2_fixtures.py
c82231a1e33e1ecc1d2bbda790baf3f80e1c7bfcdf3ec573befa992e2d432b47 tests/test_mhupa_install_records.py
```

Exit code: 0

Both values are the ones the task file gives (EX_165).

### Step 8

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r"
```

Output:

```text
python: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe 3.15.2
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Lib\site-packages
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv
ok   _common.contract_vocab               E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\contract_vocab.py
ok   _common.contract_records             E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\contract_records.py
ok   _common.contract_task                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\contract_task.py
ok   _common.contract_forecast            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\contract_forecast.py
ok   _common.contract_receipts            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\contract_receipts.py
ok   _common.contract_registry            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\contract_registry.py
ok   _common.canonical_encoding           E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\canonical_encoding.py
ok   _common.game_profiles                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\game_profiles.py
ok   _common.game_draws_reader            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\game_draws_reader.py
ok   E_001.multigame_e1                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\E_001\multigame_e1.py
ok   e2r_fixtures                         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\tests\e2r_fixtures.py
ok   _common.contract_dispatch            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\contract_dispatch.py
ok   _common.contract_publication         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\contract_publication.py
ok   _common.contract_runner              E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\contract_runner.py
ok   contract_adapters.e_001              E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\contract_adapters\e_001.py
ok   e2r_code2_fixtures                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\tests\e2r_code2_fixtures.py
contract_data: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r\src\methods\_common\contract_data
contract_data files: 371, with CRLF line endings: 368
registry loaded: 84 declarations, 202 registry chains
ORIGIN PASS: every checked module and the contract data come from the task clone
```

Exit code: 0

### Step 9

Command (run as one background command in Git Bash, as the task file requires):

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\p\MHUPA_TESTFIX_r1\tools\RUN_MHUP_A_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023\r" > "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T023/suite_output.txt" 2>&1; echo "RUNNER EXIT CODE $?" >> "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T023/suite_output.txt"
```

Wall-clock time of step 9: started 21:02:06, ended 21:25:10 local time (UTC+10:30); 23 minutes 4 seconds. The runner's own elapsed figure on its total line is 1375 s.

The whole of `scratch\T023\suite_output.txt`, as printed (its last line is the suite runner's own exit status, written by the same shell straight after the runner ended):

```text
environment: Windows 11 Python 3.15.2 E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
tests.test_code3_retirement                          ran  12 (expected 12)  skipped 0  OK  (3.9 s)
tests.test_e1_align                                  ran   5 (expected  5)  skipped 0  OK  (0.4 s)
tests.test_e1_standalone                             ran  13 (expected 13)  skipped 0  OK  (2.1 s)
tests.test_e1r2_revision2                            ran  13 (expected 13)  skipped 0  OK  (26.1 s)
tests.test_e1r3_revision3                            ran   8 (expected  8)  skipped 0  OK  (13.4 s)
tests.test_e2r_contract                              ran  53 (expected 53)  skipped 0  OK  (4.8 s)
tests.test_e2r_dispatch                              ran  18 (expected 18)  skipped 0  OK  (26.3 s)
tests.test_e2r_prefix                                ran   1 (expected  1)  skipped 0  OK  (3.8 s)
tests.test_e2r_runner                                ran  34 (expected 34)  skipped 1  OK (skipped=1)  (19.2 s)
    skip: test_dangling_symlink_target_is_refused (tests.test_e2r_runner.AtomicCreateOnly.test_dangling_symlink_target_is_refused) ... skipped 'platform disallows symlinks'
tests.test_e3_e4_polynomial                          ran  13 (expected 13)  skipped 0  OK  (45.5 s)
tests.test_e6_beta_bernoulli                         ran  20 (expected 20)  skipped 0  OK  (15.0 s)
tests.test_mhupa_gates                               ran  12 (expected 12)  skipped 0  OK  (31.0 s)
tests.test_mhupa_install_records                     ran   9 (expected  9)  skipped 0  OK  (32.1 s)
tests.test_mhupa_launchers                           ran  10 (expected 10)  skipped 0  OK  (0.7 s)
tests.test_mhupa_master_versions                     ran  15 (expected 15)  skipped 0  OK  (1.6 s)
tests.test_mhupa_method_mode_h_cli                   ran   2 (expected  2)  skipped 0  OK  (46.3 s)
tests.test_mhupa_mode_h                              ran  20 (expected 20)  skipped 0  OK  (664.4 s)
tests.test_mhupa_process_check                       ran   8 (expected  8)  skipped 0  OK  (0.4 s)
tests.test_mhupa_updater_v0_2                        ran  15 (expected 15)  skipped 0  OK  (8.1 s)
tests.test_multigame_console_and_synthetic_scorer    ran   7 (expected  7)  skipped 0  OK  (1.1 s)
tests.test_multigame_exit_receipt                    ran  18 (expected 18)  skipped 1  OK (skipped=1)  (3.5 s)
    skip: test_symlink_receipts_directory_is_refused (tests.test_multigame_exit_receipt.ReceiptTests.test_symlink_receipts_directory_is_refused) ... skipped 'platform disallows symlinks'
tests.test_multigame_launch_and_manifest             ran  11 (expected 11)  skipped 0  OK  (3.5 s)
tests.test_multigame_reader_contracts                ran  10 (expected 10)  skipped 1  OK (skipped=1)  (0.6 s)
    skip: test_reject_symlinks_and_hardlinks_and_dateload_mismatch (tests.test_multigame_reader_contracts.V011ReaderTests.test_reject_symlinks_and_hardlinks_and_dateload_mismatch) (link='symlink') ... skipped '
tests.test_multigame_science_allowlist               ran   6 (expected  6)  skipped 0  OK  (2.5 s)
tests.test_multigame_static_and_timing               ran   6 (expected  6)  skipped 0  OK  (0.3 s)
tests.test_multigame_windows_lifecycle_review        ran   6 (expected  6)  skipped 0  OK  (1.4 s)
tests.test_occurrence_counts                         ran   8 (expected  8)  skipped 0  OK  (0.4 s)
tests.test_perf1_numerics                            ran   7 (expected  7)  skipped 0  OK  (46.3 s)
tests.test_polynomial_fits                           ran  19 (expected 19)  skipped 0  OK  (0.9 s)
tests.test_recurrence_gaps                           ran  12 (expected 12)  skipped 0  OK  (0.7 s)
tests.test_rel1_release                              ran   5 (expected  5)  skipped 0  OK  (32.7 s)
tests.test_t05_hardening                             ran   2 (expected  2)  skipped 0  OK  (3.4 s)
tests.test_wave1_frequency                           ran  18 (expected 18)  skipped 0  OK  (32.6 s)
tests.test_wave2_recurrence                          ran  19 (expected 19)  skipped 0  OK  (50.4 s)
tests.test_wf1a_walk_forward                         ran  22 (expected 22)  skipped 0  OK  (57.4 s)
tests.test_wf1b_crossplatform                        ran   1 (expected  1)  skipped 0  OK  (19.5 s)
tests.test_wf1b_divisions                            ran  17 (expected 17)  skipped 0  OK  (0.2 s)
tests.test_wf1b_measures                             ran  33 (expected 33)  skipped 0  OK  (7.1 s)
tests.test_wf1b_n1_generator                         ran   8 (expected  8)  skipped 0  OK  (0.7 s)
tests.test_wf1b_n1_replay                            ran   3 (expected  3)  skipped 0  OK  (10.8 s)
tests.test_wf1b_numerics                             ran  21 (expected 21)  skipped 0  OK  (2.4 s)
tests.test_wf1b_outcome_reader                       ran   6 (expected  6)  skipped 1  OK (skipped=1)  (0.8 s)
    skip: A master that is a symbolic link is refused. Skipped where the platform cannot make a symlink (Windows ... skipped 'platform disallows symlinks'
tests.test_wf1b_report                               ran  10 (expected 10)  skipped 0  OK  (150.1 s)
tests.test_wf1b_seed_policy                          ran  11 (expected 11)  skipped 0  OK  (0.2 s)
tests.test_wf1b_static                               ran   4 (expected  4)  skipped 0  OK  (0.4 s)
total ran 571 (expected 571); skips 4; elapsed 1375 s
SUITE PASS: all 571 tests ran and passed; only the allowed symlink skips, if any.
RUNNER EXIT CODE 0
```

Exit code: 0 (the runner's own exit status, from the last line of the file).

### Step 10

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T023 -- status --short
```

Output, exactly as printed:

```text
 M tests/mhupa_slice2_fixtures.py
 M tests/test_mhupa_install_records.py
GUARD PASS (before)
GUARD PASS (after); git status exit code 0
```

Exit code: 0

The whole output is four lines: the two expected ` M` lines and the two GUARD lines. There is no other changed file and no `??` line. Git's own two lines appear before both GUARD lines rather than between them; that is the order in which this tool's output reaches the console on this machine (the same order appears in the step outputs of REPORT_T002 and REPORT_T003), not an extra or missing line.

## Clean-up

### Step 11

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T023
```

Output:

```text
REMOVE PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T023 deleted
```

Exit code: 0

The task clone, the extracted fix and `scratch\T023\suite_output.txt` went with the removed folder, as the task file says.

## The main repository after the clean-up (step 12)

Command:

```text
git status --short
```

Output:

```text
?? CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T023.md
```

Exit code: 0

This is the same as in step 2: the one line is this report file, which did not exist before the task began. Nothing else in the main repository changed.

## Deviations

None. Every step ran in order with the task file's exact command lines, and every step gave its expected output and exit code 0.

## Observations

- Step 9's wall-clock time was 23 minutes 4 seconds (21:02:06 to 21:25:10 local time, UTC+10:30); the runner's own total line gives `elapsed 1375 s`. Its last line was `RUNNER EXIT CODE 0`, written by the same shell straight after the runner ended.
- Step 9 reported 4 skips, all of them the symlink skips the task file allows (in `tests.test_e2r_runner`, `tests.test_multigame_exit_receipt`, `tests.test_multigame_reader_contracts` and `tests.test_wf1b_outcome_reader`), with the reason `platform disallows symlinks`. The runner itself judged them allowed and printed `SUITE PASS`.
- `tests.test_mhupa_install_records` ran 9 of 9 and passed, and `tests.test_mhupa_mode_h` (which uses `tests/mhupa_slice2_fixtures.py`) ran 20 of 20 and passed.
- In step 10 the two lines of Git's own output appear before both GUARD lines rather than between them. The same order appears in earlier reports (REPORT_T002, REPORT_T003) for this tool, so it is how its output reaches the console on this machine; the output still has exactly the four lines and no other.
- No step printed any draw value, and nothing was withheld from this report.
