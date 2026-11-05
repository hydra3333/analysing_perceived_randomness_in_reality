# REPORT_T020 - Windows suite run of the MHUP-A slice 2 candidate (slice 1 included), in a task clone (read-only check)

RESULT: PASS

- Task file: inbox/TASK_T020.md at main-repository commit d2c5a184c839bfc60b57f96e60b895dcc64e066f
- Run by: Claude Code (local runner), 5 November 2026, 11:17 to 11:40 +1030 (Australian Central Daylight Time)
- Owner options used: none (the task file offers none; E2R-T12 approved for this run by the task being given)
- Machine: Windows-11-10.0.26300-SP0; Python 3.15.2 at E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | Python | 0 | the venv path, 3.15.2, Windows-11-10.0.26300-SP0 |
| 2 | Main repository state (read-only) | 0, 0, 0 | `git status --short` printed nothing; HEAD d2c5a184c839bfc60b57f96e60b895dcc64e066f |
| 3 | Make the task clone | 0 | MAKE PASS |
| 4 | Check and extract the candidate | 0 | UNZIP PASS: 127 files extracted |
| 5 | Copy the overlay | 0 | OVERLAY PASS: 69 files copied (36 new, 33 replaced); 1 tracked file(s) removed with git rm |
| 6 | Module origin | 0 | ORIGIN PASS |
| 7 | The slice 2 code is in place (read-only) | 0 | VERIFY-OVERLAY PASS: 69 overlay files identical in the clone; 1 removed file(s) absent |
| 8 | All 561 tests, including E2R-T12 | 0 | SUITE PASS: all 561 tests ran and passed; only the allowed symlink skips, if any. |
| 9 | The clone is otherwise unchanged (read-only) | 0 | 33 lines starting ` M` and one `D ` line; git status exit code 0 |
| 10 | Remove the task clone | 0 | REMOVE PASS |

Wall-clock time of step 8: 1015 seconds (16 minutes 55 seconds), from 11:21:47 +1030 to 11:38:42 +1030.

The main repository's `git status --short` after step 10 is the same as in step 2: it printed nothing in both. It was run again after step 10 and its output is under "Clean-up" below. HEAD after step 10 is still d2c5a184c839bfc60b57f96e60b895dcc64e066f.

## Outputs

### Step 1

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.platform())"
```

Exit code: 0

```text
E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
3.15.2 (tags/v3.15.2:5e58eaa, Oct 25 2026, 17:27:03) [MSC v.1951 64 bit (AMD64)]
Windows-11-10.0.26300-SP0
```

### Step 2

Commands (run from MAIN):

```text
git status --short
git rev-parse HEAD
git log -1 --format=%s
```

Exit codes: 0, 0, 0

`git status --short` printed no output at all.

`git rev-parse HEAD`:

```text
d2c5a184c839bfc60b57f96e60b895dcc64e066f
```

`git log -1 --format=%s`:

```text
CLAUDE_CODE_WORKING_FOLDER_TREE: TASK_T020 replaces T019 (which STOPPED correctly at step 5: its commands named paths the repository's .claude/settings.json Bash deny list refuses on any command line - a .bat, Run_Experiment, Run_Results_Updater, results_master); tools/cc_clone.py v0.4: overlay --plan reads REPLACE/REMOVE paths from a plan file in the clone (git rm in the task clone only) and verify-overlay checks the result read-only, rehearsed on Linux with four negatives; the plan file for EX_147's candidate; exchange/CLAUDE_WEB_TOOLS/check_task_commands.py checks a task file's commands against the deny list (it reproduces T019's three refused lines; T020 has none); roadmap
```

### Step 3

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T020
```

Exit code: 0

```text
cloning from https://github.com/hydra3333/analysing_perceived_randomness_in_reality
GUARD PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r is a task clone with no remote and a refusing pre-push hook
git remote -v: ''
clone HEAD: d2c5a184c839bfc60b57f96e60b895dcc64e066f
main repository HEAD: d2c5a184c839bfc60b57f96e60b895dcc64e066f
core.autocrlf in the clone: true
MAKE PASS
```

### Step 4

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T020 --zip exchange/EX_147_Claude/MHUPA_Slice2_Review_v1.zip --sha256 94fd6c0751dcd46c724d27d95031dcb5d0207727fb7c2ac279e03ef24aa2db96
```

Exit code: 0

```text
ZIP SHA-256: 94fd6c0751dcd46c724d27d95031dcb5d0207727fb7c2ac279e03ef24aa2db96
UNZIP PASS: 127 files extracted into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\p
```

### Step 5

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T020 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\p\MHUPA_Slice2_Review_v1\overlay" --plan CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T020_overlay_plan.txt
```

Exit code: 0

```text
plan CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T020_overlay_plan.txt: 33 REPLACE, 1 REMOVE; SHA-256 aa995fb1a40cceae18643263799a2180d2843adcb0500a4f881d5cf625018836
OVERLAY PASS: 69 files copied into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r (36 new, 33 replaced); 1 tracked file(s) removed with git rm
```

### Step 6

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r"
```

Exit code: 0

```text
python: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe 3.15.2
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Lib\site-packages
ok   _common.contract_vocab               E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\contract_vocab.py
ok   _common.contract_records             E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\contract_records.py
ok   _common.contract_task                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\contract_task.py
ok   _common.contract_forecast            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\contract_forecast.py
ok   _common.contract_receipts            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\contract_receipts.py
ok   _common.contract_registry            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\contract_registry.py
ok   _common.canonical_encoding           E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\canonical_encoding.py
ok   _common.game_profiles                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\game_profiles.py
ok   _common.game_draws_reader            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\game_draws_reader.py
ok   E_001.multigame_e1                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\E_001\multigame_e1.py
ok   e2r_fixtures                         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\tests\e2r_fixtures.py
ok   _common.contract_dispatch            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\contract_dispatch.py
ok   _common.contract_publication         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\contract_publication.py
ok   _common.contract_runner              E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\contract_runner.py
ok   contract_adapters.e_001              E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\contract_adapters\e_001.py
ok   e2r_code2_fixtures                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\tests\e2r_code2_fixtures.py
contract_data: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r\src\methods\_common\contract_data
contract_data files: 369, with CRLF line endings: 364
registry loaded: 84 declarations, 202 registry chains
ORIGIN PASS: every checked module and the contract data come from the task clone
```

### Step 7

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" verify-overlay --task T020 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\p\MHUPA_Slice2_Review_v1\overlay" --plan CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T020_overlay_plan.txt
```

Exit code: 0

```text
plan CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T020_overlay_plan.txt: 33 REPLACE, 1 REMOVE; SHA-256 aa995fb1a40cceae18643263799a2180d2843adcb0500a4f881d5cf625018836
VERIFY-OVERLAY PASS: 69 overlay files identical in the clone; 1 removed file(s) absent
```

### Step 8

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\p\MHUPA_Slice2_Review_v1\tools\RUN_MHUPA_SLICE2_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020\r"
```

Exit code: 0. Wall-clock time 1015 seconds (16 minutes 55 seconds), 11:21:47 +1030 to 11:38:42 +1030.

```text
environment: Windows 11 Python 3.15.2 E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
tests.test_multigame_reader_contracts                ran  10 (expected 10)  skipped 1  OK (skipped=1)  (0.7 s)
    skip: test_reject_symlinks_and_hardlinks_and_dateload_mismatch (tests.test_multigame_reader_contracts.V011ReaderTests.test_reject_symlinks_and_hardlinks_and_dateload_mismatch) (link='symlink') ... skipped '
tests.test_multigame_static_and_timing               ran   6 (expected  6)  skipped 0  OK  (0.6 s)
tests.test_multigame_launch_and_manifest             ran  11 (expected 11)  skipped 0  OK  (3.6 s)
tests.test_multigame_exit_receipt                    ran  18 (expected 18)  skipped 1  OK (skipped=1)  (3.6 s)
    skip: test_symlink_receipts_directory_is_refused (tests.test_multigame_exit_receipt.ReceiptTests.test_symlink_receipts_directory_is_refused) ... skipped 'platform disallows symlinks'
tests.test_multigame_science_allowlist               ran   6 (expected  6)  skipped 0  OK  (2.6 s)
tests.test_multigame_console_and_synthetic_scorer    ran   7 (expected  7)  skipped 0  OK  (1.1 s)
tests.test_t05_hardening                             ran   2 (expected  2)  skipped 0  OK  (3.7 s)
tests.test_e1_align                                  ran   5 (expected  5)  skipped 0  OK  (0.4 s)
tests.test_e1_standalone                             ran  13 (expected 13)  skipped 0  OK  (2.1 s)
tests.test_multigame_windows_lifecycle_review        ran   6 (expected  6)  skipped 0  OK  (1.5 s)
tests.test_e2r_contract                              ran  53 (expected 53)  skipped 0  OK  (5.2 s)
tests.test_e2r_prefix                                ran   1 (expected  1)  skipped 0  OK  (3.5 s)
tests.test_e2r_dispatch                              ran  18 (expected 18)  skipped 0  OK  (23.9 s)
tests.test_e2r_runner                                ran  34 (expected 34)  skipped 1  OK (skipped=1)  (19.8 s)
    skip: test_dangling_symlink_target_is_refused (tests.test_e2r_runner.AtomicCreateOnly.test_dangling_symlink_target_is_refused) ... skipped 'platform disallows symlinks'
tests.test_e6_beta_bernoulli                         ran  20 (expected 20)  skipped 0  OK  (15.0 s)
tests.test_polynomial_fits                           ran  19 (expected 19)  skipped 0  OK  (0.9 s)
tests.test_e3_e4_polynomial                          ran  13 (expected 13)  skipped 0  OK  (45.3 s)
tests.test_occurrence_counts                         ran   8 (expected  8)  skipped 0  OK  (0.4 s)
tests.test_wave1_frequency                           ran  18 (expected 18)  skipped 0  OK  (32.9 s)
tests.test_recurrence_gaps                           ran  12 (expected 12)  skipped 0  OK  (0.8 s)
tests.test_wave2_recurrence                          ran  19 (expected 19)  skipped 0  OK  (52.2 s)
tests.test_rel1_release                              ran   5 (expected  5)  skipped 0  OK  (31.6 s)
tests.test_wf1a_walk_forward                         ran  22 (expected 22)  skipped 0  OK  (56.7 s)
tests.test_code3_retirement                          ran  12 (expected 12)  skipped 0  OK  (2.9 s)
tests.test_e1r2_revision2                            ran  13 (expected 13)  skipped 0  OK  (26.1 s)
tests.test_wf1b_numerics                             ran  21 (expected 21)  skipped 0  OK  (2.4 s)
tests.test_wf1b_n1_generator                         ran   8 (expected  8)  skipped 0  OK  (0.7 s)
tests.test_wf1b_divisions                            ran  17 (expected 17)  skipped 0  OK  (0.2 s)
tests.test_wf1b_measures                             ran  33 (expected 33)  skipped 0  OK  (7.2 s)
tests.test_wf1b_outcome_reader                       ran   6 (expected  6)  skipped 1  OK (skipped=1)  (0.8 s)
    skip: A master that is a symbolic link is refused. Skipped where the platform cannot make a symlink (Windows ... skipped 'platform disallows symlinks'
tests.test_wf1b_report                               ran  10 (expected 10)  skipped 0  OK  (147.9 s)
tests.test_wf1b_static                               ran   4 (expected  4)  skipped 0  OK  (0.4 s)
tests.test_wf1b_crossplatform                        ran   1 (expected  1)  skipped 0  OK  (19.4 s)
tests.test_wf1b_seed_policy                          ran  11 (expected 11)  skipped 0  OK  (0.2 s)
tests.test_wf1b_n1_replay                            ran   3 (expected  3)  skipped 0  OK  (10.8 s)
tests.test_perf1_numerics                            ran   7 (expected  7)  skipped 0  OK  (45.7 s)
tests.test_mhupa_master_versions                     ran  15 (expected 15)  skipped 0  OK  (1.6 s)
tests.test_mhupa_gates                               ran  12 (expected 12)  skipped 0  OK  (30.7 s)
tests.test_e1r3_revision3                            ran   8 (expected  8)  skipped 0  OK  (13.7 s)
tests.test_mhupa_updater_v0_2                        ran  15 (expected 15)  skipped 0  OK  (8.2 s)
tests.test_mhupa_launchers                           ran  10 (expected 10)  skipped 0  OK  (0.7 s)
tests.test_mhupa_mode_h                              ran  14 (expected 14)  skipped 0  OK  (318.1 s)
tests.test_mhupa_process_check                       ran   7 (expected  7)  skipped 0  OK  (0.4 s)
tests.test_mhupa_install_records                     ran   6 (expected  6)  skipped 0  OK  (20.3 s)
tests.test_mhupa_method_mode_h_cli                   ran   2 (expected  2)  skipped 0  OK  (48.4 s)
total ran 561 (expected 561); skips 4
SUITE PASS: all 561 tests ran and passed; only the allowed symlink skips, if any.
```

The six module lines the task file asks to be recorded exactly, as printed in the run above:

```text
tests.test_mhupa_updater_v0_2                        ran  15 (expected 15)  skipped 0  OK  (8.2 s)
tests.test_mhupa_launchers                           ran  10 (expected 10)  skipped 0  OK  (0.7 s)
tests.test_mhupa_mode_h                              ran  14 (expected 14)  skipped 0  OK  (318.1 s)
tests.test_mhupa_process_check                       ran   7 (expected  7)  skipped 0  OK  (0.4 s)
tests.test_mhupa_install_records                     ran   6 (expected  6)  skipped 0  OK  (20.3 s)
tests.test_mhupa_method_mode_h_cli                   ran   2 (expected  2)  skipped 0  OK  (48.4 s)
```

The runner printed no failure detail. It reported four skips, all symlink skips, within the four allowed, and printed SUITE PASS.

### Step 9

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T020 -- status --short --untracked-files=no
```

Exit code: 0

```text
 M .gitignore
 M Run_Experiment.bat
 M Run_Results_Updater.bat
 M src/evaluation/collect.py
 M src/evaluation/outcome_reader.py
 M src/evaluation/registry/FAMILY_REGISTRY_V1.json
 M src/evaluation/report.py
 M src/evaluation/report_writer.py
 M src/methods/E_001/multigame_e1.py
 M src/methods/E_001_Historical_Appearance_Frequency.py
 M src/methods/Method_Contract_Runner.py
 M src/methods/Method_Walk_Forward.py
 M src/methods/_common/contract_dispatch.py
 M src/methods/_common/contract_forecast.py
 M src/methods/_common/contract_receipts.py
 M src/methods/_common/contract_records.py
 M src/methods/_common/contract_runner.py
 M src/methods/_common/contract_task.py
 M src/methods/_common/contract_vocab.py
 M src/methods/_common/game_draws_reader.py
 M src/methods/_common/walk_forward.py
 M src/methods/contract_adapters/e_001.py
D  src/results_master_v0_1.py
 M tests/test_code3_retirement.py
 M tests/test_e1r2_revision2.py
 M tests/test_e2r_dispatch.py
 M tests/test_e2r_runner.py
 M tests/test_e6_beta_bernoulli.py
 M tests/test_multigame_reader_contracts.py
 M tests/test_rel1_release.py
 M tests/test_t05_hardening.py
 M tests/test_wf1a_walk_forward.py
 M tests/test_wf1b_outcome_reader.py
 M tests/test_wf1b_static.py
GUARD PASS (before)
GUARD PASS (after); git status exit code 0
```

That is 34 status lines: 33 starting ` M` and one starting `D `, as the task file expects.

## Clean-up

### Step 10

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T020
```

Exit code: 0

```text
REMOVE PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T020 deleted
```

### The main repository after step 10

Commands:

```text
git status --short
git rev-parse HEAD
```

Exit codes: 0, 0

`git status --short` printed no output at all, the same as in step 2.

`git rev-parse HEAD`:

```text
d2c5a184c839bfc60b57f96e60b895dcc64e066f
```

## Deviations

- Steps 1 to 10 were run with the command lines exactly as written in the task file, from MAIN, in the order given, with nothing added, skipped, reordered or combined.
- Step 8 was started as a background command of the runner's shell, with its console output captured to a temporary file outside the repository, because the runner's foreground command limit is ten minutes and this run took about seventeen. The command, its arguments and its exit code are unchanged; the output above is that captured output, copied exactly as printed.
- No line of any output appeared to contain a draw's numbers, so nothing was withheld.

## Observations

- This report file (step 11) was written with the runner's file-writing tool rather than a shell redirection, because the report's own text quotes paths that this repository's `.claude\settings.json` denies on any Bash command line (the same deny list that stopped T019); the first attempt to write it through a shell heredoc was refused for that reason.
- In step 8's output, the skip lines for `tests.test_multigame_reader_contracts` and `tests.test_wf1b_outcome_reader` end mid-text (`... skipped '` and `(Windows ... skipped 'platform disallows symlinks'`). The runner printed them that way; nothing was shortened here.
- Step 6 printed `contract_data files: 369, with CRLF line endings: 364` and `registry loaded: 84 declarations, 202 registry chains`.
- No step printed a warning.
- Step 8's four longest modules, as printed: `tests.test_mhupa_mode_h` 318.1 s, `tests.test_wf1b_report` 147.9 s, `tests.test_wf1a_walk_forward` 56.7 s, `tests.test_wave2_recurrence` 52.2 s.
