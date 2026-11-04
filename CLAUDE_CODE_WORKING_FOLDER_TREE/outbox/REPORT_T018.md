# REPORT_T018 - Windows suite run of the reviewed MHUP-A slice 1 code, in a task clone (read-only check)

RESULT: PASS

- Task file: inbox/TASK_T018.md at main-repository commit 83543d32504e2aa5e71453b04517eccd5b4b6bf6
- Run by: Claude Code (local runner), 5 November 2026, 02:48 to 03:00 local time, +10:30 (reported by the shell as CAST)
- Owner options used: defaults (the task file offers none; E2R-T12 run in step 8 as the task directs)
- Machine: Windows-11-10.0.26300-SP0; Python 3.15.2 at E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe

All nine steps (1 to 9) ran and passed, then the clean-up (step 10) passed. Step 8 printed `SUITE PASS: all 507 tests ran and passed; only the allowed symlink skips, if any.`, with `total ran 507 (expected 507); skips 4` - four symlink skips, the maximum the task allows.

The five evidence lines asked for in step 8 are:

```text
tests.test_multigame_reader_contracts                ran  10 (expected 10)  skipped 1  OK (skipped=1)  (0.8 s)
tests.test_wf1a_walk_forward                         ran  22 (expected 22)  skipped 0  OK  (57.6 s)
tests.test_mhupa_master_versions                     ran  15 (expected 15)  skipped 0  OK  (1.6 s)
tests.test_mhupa_gates                               ran  12 (expected 12)  skipped 0  OK  (31.5 s)
tests.test_e1r3_revision3                            ran   8 (expected  8)  skipped 0  OK  (13.7 s)
```

Step 8's wall-clock time: 10 minutes 25 seconds (start 2026-11-05T02:49:53+1030, end 2026-11-05T03:00:18+1030).

The main repository's `git status --short` after step 10 is the same as in step 2: both runs printed no output (a clean working tree), and both exited 0. The main repository's HEAD was 83543d32504e2aa5e71453b04517eccd5b4b6bf6 before and after.

Nothing was installed, staged, committed in the clone, verified, reported, batched or updated; no program other than the tests was run.

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | Python | 0 | venv path; 3.15.2; Windows-11-10.0.26300-SP0 |
| 2 | Main repository state (read-only) | 0, 0, 0 | no status lines (clean); HEAD 83543d32504e2aa5e71453b04517eccd5b4b6bf6 |
| 3 | Make the task clone | 0 | GUARD PASS; git remote -v: ''; MAKE PASS |
| 4 | Check and extract the candidate | 0 | ZIP SHA-256 matched; UNZIP PASS: 75 files extracted |
| 5 | Copy the overlay | 0 | OVERLAY PASS: 46 files copied (20 new, 26 replaced) |
| 6 | Module origin | 0 | ORIGIN PASS: every checked module and the contract data come from the task clone |
| 7 | The slice 1 code is in place (read-only) | 0 | True True True True |
| 8 | All 507 tests, including E2R-T12 | 0 | SUITE PASS: all 507 tests ran and passed; only the allowed symlink skips, if any. (total ran 507 (expected 507); skips 4) |
| 9 | The clone is otherwise unchanged by the run (read-only) | 0 | 26 lines, each ` M`; GUARD PASS (before); GUARD PASS (after); git status exit code 0 |
| 10 | Remove the task clone (clean-up) | 0 | REMOVE PASS |
| 11 | Main repository state again (for the report) | 0, 0 | no status lines (clean); HEAD 83543d32504e2aa5e71453b04517eccd5b4b6bf6 |

## Outputs

### Step 1

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.platform())"
```

Output (exit code 0):

```text
E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
3.15.2 (tags/v3.15.2:5e58eaa, Oct 25 2026, 17:27:03) [MSC v.1951 64 bit (AMD64)]
Windows-11-10.0.26300-SP0
```

### Step 2

Commands (run in the main repository):

```text
git status --short
git rev-parse HEAD
git log -1 --format=%s
```

Output of `git status --short` (exit code 0) - no output, the working tree is clean:

```text
```

Output of `git rev-parse HEAD` (exit code 0):

```text
83543d32504e2aa5e71453b04517eccd5b4b6bf6
```

Output of `git log -1 --format=%s` (exit code 0):

```text
CLAUDE_CODE_WORKING_FOLDER_TREE: TASK_T018 - Windows suite run (507 tests, E2R-T12 included) of the reviewed MHUP-A slice 1 candidate v1r2 in a task clone, read-only: shows the committed development ledgers pass the full ledger grammar; installs and commits nothing (T016/T017 stay reserved for the MHUP-A/MHUP-B install rehearsals); roadmap
```

### Step 3

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T018
```

Output (exit code 0):

```text
cloning from https://github.com/hydra3333/analysing_perceived_randomness_in_reality
GUARD PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r is a task clone with no remote and a refusing pre-push hook
git remote -v: ''
clone HEAD: 83543d32504e2aa5e71453b04517eccd5b4b6bf6
main repository HEAD: 83543d32504e2aa5e71453b04517eccd5b4b6bf6
core.autocrlf in the clone: true
MAKE PASS
```

### Step 4

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T018 --zip exchange/EX_145_Claude/MHUPA_Slice1_Review_v1r2.zip --sha256 5fbaaae1c51a325017b03593d75a09753e4e584bb5e6816ec6480cf78765fb7b
```

Output (exit code 0):

```text
ZIP SHA-256: 5fbaaae1c51a325017b03593d75a09753e4e584bb5e6816ec6480cf78765fb7b
UNZIP PASS: 75 files extracted into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\p
```

### Step 5

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T018 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\p\MHUPA_Slice1_Review_v1r2\overlay" --replace src/evaluation/outcome_reader.py src/evaluation/report.py src/methods/E_001/multigame_e1.py src/methods/E_001_Historical_Appearance_Frequency.py src/methods/Method_Contract_Runner.py src/methods/_common/contract_dispatch.py src/methods/_common/contract_forecast.py src/methods/_common/contract_receipts.py src/methods/_common/contract_records.py src/methods/_common/contract_runner.py src/methods/_common/contract_task.py src/methods/_common/contract_vocab.py src/methods/_common/game_draws_reader.py src/methods/_common/walk_forward.py src/methods/contract_adapters/e_001.py tests/test_code3_retirement.py tests/test_e1r2_revision2.py tests/test_e2r_dispatch.py tests/test_e2r_runner.py tests/test_e6_beta_bernoulli.py tests/test_multigame_reader_contracts.py tests/test_rel1_release.py tests/test_t05_hardening.py tests/test_wf1a_walk_forward.py tests/test_wf1b_outcome_reader.py tests/test_wf1b_static.py
```

Output (exit code 0):

```text
OVERLAY PASS: 46 files copied into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r (20 new, 26 replaced)
```

### Step 6

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r"
```

Output (exit code 0):

```text
python: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe 3.15.2
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Lib\site-packages
ok   _common.contract_vocab               E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\contract_vocab.py
ok   _common.contract_records             E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\contract_records.py
ok   _common.contract_task                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\contract_task.py
ok   _common.contract_forecast            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\contract_forecast.py
ok   _common.contract_receipts            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\contract_receipts.py
ok   _common.contract_registry            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\contract_registry.py
ok   _common.canonical_encoding           E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\canonical_encoding.py
ok   _common.game_profiles                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\game_profiles.py
ok   _common.game_draws_reader            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\game_draws_reader.py
ok   E_001.multigame_e1                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\E_001\multigame_e1.py
ok   e2r_fixtures                         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\tests\e2r_fixtures.py
ok   _common.contract_dispatch            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\contract_dispatch.py
ok   _common.contract_publication         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\contract_publication.py
ok   _common.contract_runner              E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\contract_runner.py
ok   contract_adapters.e_001              E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\contract_adapters\e_001.py
ok   e2r_code2_fixtures                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\tests\e2r_code2_fixtures.py
contract_data: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r\src\methods\_common\contract_data
contract_data files: 368, with CRLF line endings: 364
registry loaded: 84 declarations, 202 registry chains
ORIGIN PASS: every checked module and the contract data come from the task clone
```

### Step 7

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import pathlib; r = pathlib.Path(r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r'); t = (r / 'src' / 'methods' / '_common' / 'master_versions.py').read_text(encoding='ascii'); print('strict=True' in t, '_render' in t, (r / 'src' / 'methods' / '_common' / 'owner_records.py').is_file(), (r / 'archive' / 'methods' / 'E_001' / 'r2' / 'README.md').is_file())"
```

Output (exit code 0):

```text
True True True True
```

### Step 8

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\p\MHUPA_Slice1_Review_v1r2\tools\RUN_MHUPA_SLICE1_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018\r"
```

Output (exit code 0), as printed:

```text
environment: Windows 11 Python 3.15.2 E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
tests.test_multigame_reader_contracts                ran  10 (expected 10)  skipped 1  OK (skipped=1)  (0.8 s)
    skip: test_reject_symlinks_and_hardlinks_and_dateload_mismatch (tests.test_multigame_reader_contracts.V011ReaderTests.test_reject_symlinks_and_hardlinks_and_dateload_mismatch) (link='symlink') ... skipped '
tests.test_multigame_static_and_timing               ran   6 (expected  6)  skipped 0  OK  (0.6 s)
tests.test_multigame_launch_and_manifest             ran  11 (expected 11)  skipped 0  OK  (3.7 s)
tests.test_multigame_exit_receipt                    ran  18 (expected 18)  skipped 1  OK (skipped=1)  (3.6 s)
    skip: test_symlink_receipts_directory_is_refused (tests.test_multigame_exit_receipt.ReceiptTests.test_symlink_receipts_directory_is_refused) ... skipped 'platform disallows symlinks'
tests.test_multigame_science_allowlist               ran   6 (expected  6)  skipped 0  OK  (2.6 s)
tests.test_multigame_console_and_synthetic_scorer    ran   7 (expected  7)  skipped 0  OK  (1.1 s)
tests.test_t05_hardening                             ran   2 (expected  2)  skipped 0  OK  (3.9 s)
tests.test_e1_align                                  ran   5 (expected  5)  skipped 0  OK  (0.4 s)
tests.test_e1_standalone                             ran  13 (expected 13)  skipped 0  OK  (2.1 s)
tests.test_multigame_windows_lifecycle_review        ran   6 (expected  6)  skipped 0  OK  (1.5 s)
tests.test_e2r_contract                              ran  53 (expected 53)  skipped 0  OK  (5.4 s)
tests.test_e2r_prefix                                ran   1 (expected  1)  skipped 0  OK  (3.5 s)
tests.test_e2r_dispatch                              ran  18 (expected 18)  skipped 0  OK  (25.3 s)
tests.test_e2r_runner                                ran  34 (expected 34)  skipped 1  OK (skipped=1)  (20.4 s)
    skip: test_dangling_symlink_target_is_refused (tests.test_e2r_runner.AtomicCreateOnly.test_dangling_symlink_target_is_refused) ... skipped 'platform disallows symlinks'
tests.test_e6_beta_bernoulli                         ran  20 (expected 20)  skipped 0  OK  (15.2 s)
tests.test_polynomial_fits                           ran  19 (expected 19)  skipped 0  OK  (0.9 s)
tests.test_e3_e4_polynomial                          ran  13 (expected 13)  skipped 0  OK  (46.1 s)
tests.test_occurrence_counts                         ran   8 (expected  8)  skipped 0  OK  (0.4 s)
tests.test_wave1_frequency                           ran  18 (expected 18)  skipped 0  OK  (32.6 s)
tests.test_recurrence_gaps                           ran  12 (expected 12)  skipped 0  OK  (0.8 s)
tests.test_wave2_recurrence                          ran  19 (expected 19)  skipped 0  OK  (50.8 s)
tests.test_rel1_release                              ran   5 (expected  5)  skipped 0  OK  (31.9 s)
tests.test_wf1a_walk_forward                         ran  22 (expected 22)  skipped 0  OK  (57.6 s)
tests.test_code3_retirement                          ran  12 (expected 12)  skipped 0  OK  (2.8 s)
tests.test_e1r2_revision2                            ran  13 (expected 13)  skipped 0  OK  (27.2 s)
tests.test_wf1b_numerics                             ran  21 (expected 21)  skipped 0  OK  (2.5 s)
tests.test_wf1b_n1_generator                         ran   8 (expected  8)  skipped 0  OK  (0.7 s)
tests.test_wf1b_divisions                            ran  17 (expected 17)  skipped 0  OK  (0.2 s)
tests.test_wf1b_measures                             ran  33 (expected 33)  skipped 0  OK  (7.2 s)
tests.test_wf1b_outcome_reader                       ran   6 (expected  6)  skipped 1  OK (skipped=1)  (0.8 s)
    skip: A master that is a symbolic link is refused. Skipped where the platform cannot make a symlink (Windows ... skipped 'platform disallows symlinks'
tests.test_wf1b_report                               ran  10 (expected 10)  skipped 0  OK  (149.6 s)
tests.test_wf1b_static                               ran   4 (expected  4)  skipped 0  OK  (0.3 s)
tests.test_wf1b_crossplatform                        ran   1 (expected  1)  skipped 0  OK  (19.5 s)
tests.test_wf1b_seed_policy                          ran  11 (expected 11)  skipped 0  OK  (0.2 s)
tests.test_wf1b_n1_replay                            ran   3 (expected  3)  skipped 0  OK  (10.9 s)
tests.test_perf1_numerics                            ran   7 (expected  7)  skipped 0  OK  (45.5 s)
tests.test_mhupa_master_versions                     ran  15 (expected 15)  skipped 0  OK  (1.6 s)
tests.test_mhupa_gates                               ran  12 (expected 12)  skipped 0  OK  (31.5 s)
tests.test_e1r3_revision3                            ran   8 (expected  8)  skipped 0  OK  (13.7 s)
total ran 507 (expected 507); skips 4
SUITE PASS: all 507 tests ran and passed; only the allowed symlink skips, if any.
```

No failure detail was printed. No line appeared to contain a draw's numbers, so no line was withheld.

Wall-clock time: 10 minutes 25 seconds (start 2026-11-05T02:49:53+1030, end 2026-11-05T03:00:18+1030).

### Step 9

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T018 -- status --short --untracked-files=no
```

Output (exit code 0):

```text
 M src/evaluation/outcome_reader.py
 M src/evaluation/report.py
 M src/methods/E_001/multigame_e1.py
 M src/methods/E_001_Historical_Appearance_Frequency.py
 M src/methods/Method_Contract_Runner.py
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

That is 26 lines, each starting ` M`, and they are exactly the 26 replacements named in step 5.

### Step 11 (the main repository's state again, for the report)

Commands (run in the main repository, after step 10):

```text
git status --short
git rev-parse HEAD
```

Output of `git status --short` (exit code 0) - no output, the working tree is clean, the same as in step 2:

```text
```

Output of `git rev-parse HEAD` (exit code 0):

```text
83543d32504e2aa5e71453b04517eccd5b4b6bf6
```

## Clean-up

### Step 10

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T018
```

Output (exit code 0):

```text
REMOVE PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T018 deleted
```

## Deviations

None.

## Observations

- Step 8 was run as a background command in the runner's shell, so that its full output could be captured; the command itself was the one in the task file, unchanged, and it ran to completion with exit code 0.
- Two of the four skip detail lines in step 8's output end mid-text, as printed by the runner: the `tests.test_multigame_reader_contracts` line ends `... skipped '`, and the `tests.test_wf1b_outcome_reader` line ends `(Windows ... skipped 'platform disallows symlinks'`. They are copied exactly as printed; nothing was removed from them.
- The four skips are the maximum of four symlink skips the task allows, in `tests.test_multigame_reader_contracts`, `tests.test_multigame_exit_receipt`, `tests.test_e2r_runner` and `tests.test_wf1b_outcome_reader`.
- No warnings other than the skip lines were printed by any step.
