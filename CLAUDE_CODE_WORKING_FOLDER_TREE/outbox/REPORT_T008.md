# REPORT_T008 - Windows rehearsal of the wave 2 install, in a task clone

RESULT: PASS

- Task file: inbox/TASK_T008.md at main-repository commit 654985f8220b113475c597fcdb4c8eb64457fd31
- Run by: Claude Code (local runner), 30 October 2026, 21:30 to 21:35 +1030 (Australian Central Daylight Time)
- Owner options used: none (the task file offers none); E2R-T12 was run in step 9, as the task file requires
- Machine: Windows-11-10.0.26300-SP0; Python 3.15.2 at E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | Python identity | 0 | venv path, 3.15.2, Windows-11-10.0.26300-SP0 |
| 2 | Main repository state (read-only) | 0 | `git status --short` printed nothing; HEAD 654985f8220b113475c597fcdb4c8eb64457fd31 |
| 3 | Make the task clone | 0 | `MAKE PASS` |
| 4 | Check and extract the package | 0 | `UNZIP PASS: 93 files extracted ...` |
| 5 | PRE check | 0 | `GUARD PASS`, then `PRE PASS` |
| 6 | Copy the overlay into the clone | 0 | `OVERLAY PASS: 90 files copied ... (87 new, 3 replaced)` |
| 7 | POST check | 0 | `POST PASS` |
| 8 | Module origin | 0 | `ORIGIN PASS` (80 declarations, 202 registry chains) |
| 9 | All 299 tests, including E2R-T12 | 0 | `SUITE PASS: all 299 tests ran and passed; only the allowed symlink skips, if any.` |
| 10 | Stage in the clone | 0 | `GUARD PASS (before)`, then `GUARD PASS (after); git add exit code 0` |
| 11 | Status in the clone | 0 | 90 lines: 87 starting `A`, 3 starting `M`; `git status exit code 0` |
| 12 | Commit in the clone | 0 | `GUARD PASS (after); git commit exit code 0` |
| 13 | COMMITTED check | 0 | `COMMITTED PASS` |
| 14 | Final state of the clone | 0 | rehearsal commit 7add481 on top of 654985f; `git log exit code 0` |
| 15 | Remove the task clone (clean-up) | 0 | `REMOVE PASS` |

Wall-clock time for step 9: 3 minutes 18 seconds (started 2026-10-30T21:31:17+1030, ended 2026-10-30T21:34:35+1030).

The main repository's `git status --short` after step 15 is the same as in step 2: it printed nothing in both cases. The re-run is recorded under "Main repository after clean-up" below.

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

Commands, run in the main repository:

```text
git status --short
git rev-parse HEAD
git log -1 --format=%s
```

Output of `git status --short` (exit code 0) - no lines were printed:

```text
```

Output of `git rev-parse HEAD` (exit code 0):

```text
654985f8220b113475c597fcdb4c8eb64457fd31
```

Output of `git log -1 --format=%s` (exit code 0):

```text
exchange: EX_076 (final wave 2 package, register v0.19 final); Claude Code: TASK_T008 (Windows rehearsal of the final wave 2 package in a task clone, with E2R-T12)
```

### Step 3

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T008
```

Output (exit code 0):

```text
cloning from https://github.com/hydra3313/analysing_perceived_randomness_in_reality
GUARD PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r is a task clone with no remote and a refusing pre-push hook
git remote -v: ''
clone HEAD: 654985f8220b113475c597fcdb4c8eb64457fd31
main repository HEAD: 654985f8220b113475c597fcdb4c8eb64457fd31
core.autocrlf in the clone: true
MAKE PASS
```

### Step 4

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T008 --zip exchange/EX_076_Claude/W2_Install_v1.zip --sha256 57ef34b67b8aa6cc023c5ea3d78c2940ab1a9875c3141626c5016355da53c429
```

Output (exit code 0):

```text
ZIP SHA-256: 57ef34b67b8aa6cc023c5ea3d78c2940ab1a9875c3141626c5016355da53c429
UNZIP PASS: 93 files extracted into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\p
```

### Step 5

First command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" guard --task T008
```

Output (exit code 0):

```text
GUARD PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r is a task clone with no remote and a refusing pre-push hook
```

Second command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\p\W2_Install_v1\VERIFY_W2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r" --phase pre
```

Output (exit code 0):

```text
HEAD: 654985f8220b113475c597fcdb4c8eb64457fd31 (descends from base 8f44d50)
54 guarded files unchanged in Git HEAD
PRE PASS: clean tree; 87 new paths absent; 3 files at their base version. Nothing was changed.
Read-only: no project code imported, nothing run, nothing changed.
```

### Step 6

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T008 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\p\W2_Install_v1\repo_overlay" --replace src/methods/Method_Contract_Runner.py doc/METHOD_TEMPLATE/README.md doc/METHOD_TEMPLATE/METHOD_SPECIFICATION_TEMPLATE.md
```

Output (exit code 0):

```text
OVERLAY PASS: 90 files copied into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r (87 new, 3 replaced)
```

### Step 7

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\p\W2_Install_v1\VERIFY_W2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r" --phase post
```

Output (exit code 0):

```text
HEAD: 654985f8220b113475c597fcdb4c8eb64457fd31 (descends from base 8f44d50)
54 guarded files unchanged in Git HEAD
POST PASS: exactly the 87 expected new paths and 3 modified files, all with the expected bytes.
Read-only: no project code imported, nothing run, nothing changed.
```

### Step 8

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r"
```

Output (exit code 0):

```text
python: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe 3.15.2
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Lib\site-packages
ok   _common.contract_vocab               E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\contract_vocab.py
ok   _common.contract_records             E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\contract_records.py
ok   _common.contract_task                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\contract_task.py
ok   _common.contract_forecast            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\contract_forecast.py
ok   _common.contract_receipts            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\contract_receipts.py
ok   _common.contract_registry            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\contract_registry.py
ok   _common.canonical_encoding           E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\canonical_encoding.py
ok   _common.game_profiles                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\game_profiles.py
ok   _common.game_draws_reader            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\game_draws_reader.py
ok   E_001.multigame_e1                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\E_001\multigame_e1.py
ok   e2r_fixtures                         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\tests\e2r_fixtures.py
ok   _common.contract_dispatch            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\contract_dispatch.py
ok   _common.contract_publication         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\contract_publication.py
ok   _common.contract_runner              E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\contract_runner.py
ok   contract_adapters.e_001              E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\contract_adapters\e_001.py
ok   e2r_code2_fixtures                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\tests\e2r_code2_fixtures.py
contract_data: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r\src\methods\_common\contract_data
contract_data files: 282, with CRLF line endings: 234
registry loaded: 80 declarations, 202 registry chains
ORIGIN PASS: every checked module and the contract data come from the task clone
```

### Step 9

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\p\W2_Install_v1\RUN_W2_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r"
```

Started 2026-10-30T21:31:17+1030, ended 2026-10-30T21:34:35+1030; wall-clock 3 minutes 18 seconds.

Output (exit code 0):

```text
environment: Windows 11 Python 3.15.2 E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
tests.test_multigame_reader_contracts                ran  10 (expected 10)  skipped 1  OK (skipped=1)
    skip: test_reject_symlinks_and_hardlinks_and_dateload_mismatch (tests.test_multigame_reader_contracts.V011ReaderTests.test_reject_symlinks_and_hardlinks_and_dateload_mismatch) (link='symlink') ... skipped '
tests.test_multigame_static_and_timing               ran   6 (expected  6)  skipped 0  OK
tests.test_multigame_launch_and_manifest             ran  11 (expected 11)  skipped 0  OK
tests.test_multigame_exit_receipt                    ran  18 (expected 18)  skipped 1  OK (skipped=1)
    skip: test_symlink_receipts_directory_is_refused (tests.test_multigame_exit_receipt.ReceiptTests.test_symlink_receipts_directory_is_refused) ... skipped 'platform disallows symlinks'
tests.test_multigame_science_allowlist               ran   6 (expected  6)  skipped 0  OK
tests.test_multigame_console_and_synthetic_scorer    ran   7 (expected  7)  skipped 0  OK
tests.test_t05_hardening                             ran   2 (expected  2)  skipped 0  OK
tests.test_e1_align                                  ran   5 (expected  5)  skipped 0  OK
tests.test_e1_standalone                             ran  13 (expected 13)  skipped 0  OK
tests.test_multigame_windows_lifecycle_review        ran   6 (expected  6)  skipped 0  OK
tests.test_e2r_contract                              ran  53 (expected 53)  skipped 0  OK
tests.test_e2r_prefix                                ran   1 (expected  1)  skipped 0  OK
tests.test_e2r_dispatch                              ran  18 (expected 18)  skipped 0  OK
tests.test_e2r_runner                                ran  34 (expected 34)  skipped 1  OK (skipped=1)
    skip: test_dangling_symlink_target_is_refused (tests.test_e2r_runner.AtomicCreateOnly.test_dangling_symlink_target_is_refused) ... skipped 'platform disallows symlinks'
tests.test_e6_beta_bernoulli                         ran  20 (expected 20)  skipped 0  OK
tests.test_polynomial_fits                           ran  19 (expected 19)  skipped 0  OK
tests.test_e3_e4_polynomial                          ran  13 (expected 13)  skipped 0  OK
tests.test_occurrence_counts                         ran   8 (expected  8)  skipped 0  OK
tests.test_wave1_frequency                           ran  18 (expected 18)  skipped 0  OK
tests.test_recurrence_gaps                           ran  12 (expected 12)  skipped 0  OK
tests.test_wave2_recurrence                          ran  19 (expected 19)  skipped 0  OK
total ran 299 (expected 299); skips 3
SUITE PASS: all 299 tests ran and passed; only the allowed symlink skips, if any.
```

### Step 10

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T008 -- add doc review src tests
```

Output (exit code 0):

```text
warning: in the working copy of 'doc/METHOD_TEMPLATE/METHOD_SPECIFICATION_TEMPLATE.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'doc/METHOD_TEMPLATE/README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/Method_Contract_Runner.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'doc/RATIFICATION_REGISTER_v0_19.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/Independent_ChatGPT_Wave1_R2_and_Register_v18_Review_v0_1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/Independent_ChatGPT_Wave2_R3_Review_v0_1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/Independent_ChatGPT_Wave2_v0_1r1_R3_RECHECK_v0_1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/Independent_ChatGPT_Wave2_v0_1r2_Focused_RECHECK_v0_1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/INSTALL_MANIFEST_SHA256.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/design_probes_v0_1r2.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/mutations_py313.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/replaced_files_base_to_v1.diff', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/suite_py313.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/suite_py315.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/template_trial_v3.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/tools/edit_runner.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/tools/make_template_draft3.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/tools/make_wave2_contract_data.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/tools/reference_wave2.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/tools/template_trial_v3.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/tools/w2_mutations.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/W2_Install_v1/tools/write_wave2_methods.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_002/IN_DEVELOPMENT.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_002/__init__.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_002/contract.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_002/variants.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_017/IN_DEVELOPMENT.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_017/__init__.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_017/contract.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_017/variants.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_018/IN_DEVELOPMENT.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_018/__init__.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_018/contract.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_018/variants.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_019/IN_DEVELOPMENT.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_019/__init__.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_019/contract.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/E_019/variants.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_17/HAZARD_BINS_C100_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_17/HAZARD_BINS_W208_C100_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_17/HAZARD_LOGAGE_SIGN_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_18/MIX4_ALL_C10_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_18/MIX4_W104_C10_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_18/MIX4_W208_C10_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_19/PERIODIC_T2_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_19/PERIODIC_T3_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_19/PERIODIC_T4_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_2/RECUR_MEAN_ALL_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_2/RECUR_MEAN_LAST8_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_2/RECUR_MEDIAN_ALL_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_17/HAZARD_BINS_C100_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_17/HAZARD_BINS_W208_C100_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_17/HAZARD_LOGAGE_SIGN_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_18/MIX4_ALL_C10_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_18/MIX4_W104_C10_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_18/MIX4_W208_C10_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_19/PERIODIC_T2_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_19/PERIODIC_T3_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_19/PERIODIC_T4_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_2/RECUR_MEAN_ALL_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_2/RECUR_MEAN_LAST8_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_2/RECUR_MEDIAN_ALL_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_17/HAZARD_BINS_C100_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_17/HAZARD_BINS_W208_C100_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_17/HAZARD_LOGAGE_SIGN_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_18/MIX4_ALL_C10_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_18/MIX4_W104_C10_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_18/MIX4_W208_C10_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_19/PERIODIC_T2_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_19/PERIODIC_T3_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_19/PERIODIC_T4_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_2/RECUR_MEAN_ALL_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_2/RECUR_MEAN_LAST8_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_2/RECUR_MEDIAN_ALL_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_17/HAZARD_BINS_C100_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_17/HAZARD_BINS_W208_C100_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_17/HAZARD_LOGAGE_SIGN_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_18/MIX4_ALL_C10_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_18/MIX4_W104_C10_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_18/MIX4_W208_C10_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_19/PERIODIC_T2_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_19/PERIODIC_T3_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_19/PERIODIC_T4_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_2/RECUR_MEAN_ALL_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_2/RECUR_MEAN_LAST8_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_2/RECUR_MEDIAN_ALL_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/recurrence_gaps.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_recurrence_gaps.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_wave2_recurrence.py', LF will be replaced by CRLF the next time Git touches it
GUARD PASS (before)
GUARD PASS (after); git add exit code 0
```

### Step 11

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T008 -- status --short
```

Output (exit code 0), the whole output exactly as printed:

```text
M  doc/METHOD_TEMPLATE/METHOD_SPECIFICATION_TEMPLATE.md
M  doc/METHOD_TEMPLATE/README.md
A  doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md
A  doc/RATIFICATION_REGISTER_v0_19.md
A  review/Independent_ChatGPT_Wave1_R2_and_Register_v18_Review_v0_1.md
A  review/Independent_ChatGPT_Wave2_R3_Review_v0_1.md
A  review/Independent_ChatGPT_Wave2_v0_1r1_R3_RECHECK_v0_1.md
A  review/Independent_ChatGPT_Wave2_v0_1r2_Focused_RECHECK_v0_1.md
A  review/W2_Install_v1/INSTALL_MANIFEST_SHA256.txt
A  review/W2_Install_v1/design_probes_v0_1r2.txt
A  review/W2_Install_v1/mutations_py313.txt
A  review/W2_Install_v1/replaced_files_base_to_v1.diff
A  review/W2_Install_v1/suite_py313.txt
A  review/W2_Install_v1/suite_py315.txt
A  review/W2_Install_v1/template_trial_v3.txt
A  review/W2_Install_v1/tools/edit_runner.py
A  review/W2_Install_v1/tools/make_template_draft3.py
A  review/W2_Install_v1/tools/make_wave2_contract_data.py
A  review/W2_Install_v1/tools/reference_wave2.py
A  review/W2_Install_v1/tools/template_trial_v3.py
A  review/W2_Install_v1/tools/w2_mutations.py
A  review/W2_Install_v1/tools/write_wave2_methods.py
A  src/methods/E_002/IN_DEVELOPMENT.txt
A  src/methods/E_002/__init__.py
A  src/methods/E_002/contract.py
A  src/methods/E_002/variants.py
A  src/methods/E_017/IN_DEVELOPMENT.txt
A  src/methods/E_017/__init__.py
A  src/methods/E_017/contract.py
A  src/methods/E_017/variants.py
A  src/methods/E_018/IN_DEVELOPMENT.txt
A  src/methods/E_018/__init__.py
A  src/methods/E_018/contract.py
A  src/methods/E_018/variants.py
A  src/methods/E_019/IN_DEVELOPMENT.txt
A  src/methods/E_019/__init__.py
A  src/methods/E_019/contract.py
A  src/methods/E_019/variants.py
M  src/methods/Method_Contract_Runner.py
A  src/methods/_common/contract_data/declarations/OZLOTTO/E_17/HAZARD_BINS_C100_V1/r1.json
A  src/methods/_common/contract_data/declarations/OZLOTTO/E_17/HAZARD_BINS_W208_C100_V1/r1.json
A  src/methods/_common/contract_data/declarations/OZLOTTO/E_17/HAZARD_LOGAGE_SIGN_V1/r1.json
A  src/methods/_common/contract_data/declarations/OZLOTTO/E_18/MIX4_ALL_C10_V1/r1.json
A  src/methods/_common/contract_data/declarations/OZLOTTO/E_18/MIX4_W104_C10_V1/r1.json
A  src/methods/_common/contract_data/declarations/OZLOTTO/E_18/MIX4_W208_C10_V1/r1.json
A  src/methods/_common/contract_data/declarations/OZLOTTO/E_19/PERIODIC_T2_V1/r1.json
A  src/methods/_common/contract_data/declarations/OZLOTTO/E_19/PERIODIC_T3_V1/r1.json
A  src/methods/_common/contract_data/declarations/OZLOTTO/E_19/PERIODIC_T4_V1/r1.json
A  src/methods/_common/contract_data/declarations/OZLOTTO/E_2/RECUR_MEAN_ALL_V1/r1.json
A  src/methods/_common/contract_data/declarations/OZLOTTO/E_2/RECUR_MEAN_LAST8_V1/r1.json
A  src/methods/_common/contract_data/declarations/OZLOTTO/E_2/RECUR_MEDIAN_ALL_V1/r1.json
A  src/methods/_common/contract_data/declarations/POWERBALL/E_17/HAZARD_BINS_C100_V1/r1.json
A  src/methods/_common/contract_data/declarations/POWERBALL/E_17/HAZARD_BINS_W208_C100_V1/r1.json
A  src/methods/_common/contract_data/declarations/POWERBALL/E_17/HAZARD_LOGAGE_SIGN_V1/r1.json
A  src/methods/_common/contract_data/declarations/POWERBALL/E_18/MIX4_ALL_C10_V1/r1.json
A  src/methods/_common/contract_data/declarations/POWERBALL/E_18/MIX4_W104_C10_V1/r1.json
A  src/methods/_common/contract_data/declarations/POWERBALL/E_18/MIX4_W208_C10_V1/r1.json
A  src/methods/_common/contract_data/declarations/POWERBALL/E_19/PERIODIC_T2_V1/r1.json
A  src/methods/_common/contract_data/declarations/POWERBALL/E_19/PERIODIC_T3_V1/r1.json
A  src/methods/_common/contract_data/declarations/POWERBALL/E_19/PERIODIC_T4_V1/r1.json
A  src/methods/_common/contract_data/declarations/POWERBALL/E_2/RECUR_MEAN_ALL_V1/r1.json
A  src/methods/_common/contract_data/declarations/POWERBALL/E_2/RECUR_MEAN_LAST8_V1/r1.json
A  src/methods/_common/contract_data/declarations/POWERBALL/E_2/RECUR_MEDIAN_ALL_V1/r1.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_17/HAZARD_BINS_C100_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_17/HAZARD_BINS_W208_C100_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_17/HAZARD_LOGAGE_SIGN_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_18/MIX4_ALL_C10_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_18/MIX4_W104_C10_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_18/MIX4_W208_C10_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_19/PERIODIC_T2_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_19/PERIODIC_T3_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_19/PERIODIC_T4_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_2/RECUR_MEAN_ALL_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_2/RECUR_MEAN_LAST8_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_2/RECUR_MEDIAN_ALL_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_17/HAZARD_BINS_C100_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_17/HAZARD_BINS_W208_C100_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_17/HAZARD_LOGAGE_SIGN_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_18/MIX4_ALL_C10_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_18/MIX4_W104_C10_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_18/MIX4_W208_C10_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_19/PERIODIC_T2_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_19/PERIODIC_T3_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_19/PERIODIC_T4_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_2/RECUR_MEAN_ALL_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_2/RECUR_MEAN_LAST8_V1/entry_0001.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_2/RECUR_MEDIAN_ALL_V1/entry_0001.json
A  src/methods/_common/recurrence_gaps.py
A  tests/test_recurrence_gaps.py
A  tests/test_wave2_recurrence.py
GUARD PASS (before)
GUARD PASS (after); git status exit code 0
```

### Step 12

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T008 -- commit -q -m "Wave 2 rehearsal (task clone T008 only; never pushed)"
```

Output (exit code 0):

```text
GUARD PASS (before)
GUARD PASS (after); git commit exit code 0
```

### Step 13

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\p\W2_Install_v1\VERIFY_W2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008\r" --phase committed
```

Output (exit code 0):

```text
HEAD: 7add481cd561ab27aca9df6f93e2d3315ce4d997 (descends from base 8f44d50)
54 guarded files unchanged in Git HEAD
COMMITTED PASS: the last commit (7add481) added exactly 87 files and modified 3; all Git blobs match.
Read-only: no project code imported, nothing run, nothing changed.
```

### Step 14

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T008 -- log --oneline -2
```

Output (exit code 0):

```text
7add481 Wave 2 rehearsal (task clone T008 only; never pushed)
654985f exchange: EX_076 (final wave 2 package, register v0.19 final); Claude Code: TASK_T008 (Windows rehearsal of the final wave 2 package in a task clone, with E2R-T12)
GUARD PASS (before)
GUARD PASS (after); git log exit code 0
```

## Clean-up

### Step 15

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T008
```

Output (exit code 0):

```text
REMOVE PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T008 deleted
```

The task clone was removed. `CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\` holds no entries again.

### Main repository after clean-up

Commands, run in the main repository after step 15:

```text
git status --short
git rev-parse HEAD
```

Output of `git status --short` (exit code 0) - no lines were printed:

```text
```

Output of `git rev-parse HEAD` (exit code 0):

```text
654985f8220b113475c597fcdb4c8eb64457fd31
```

This is the same as in step 2: `git status --short` printed nothing in both cases, and HEAD is unchanged at 654985f8220b113475c597fcdb4c8eb64457fd31.

## Deviations

None. Steps 1 to 15 were run in the order written, with the commands copied from the task file and not edited. Each was run from the MAIN folder.

## Observations

Plain facts from the run.

1. Step 9 printed `total ran 299 (expected 299); skips 3` and took 3 minutes 18 seconds. The 3 skips are the symlink skips the task file allows: `test_reject_symlinks_and_hardlinks_and_dateload_mismatch` (in `tests.test_multigame_reader_contracts`), `test_symlink_receipts_directory_is_refused` (in `tests.test_multigame_exit_receipt`) and `test_dangling_symlink_target_is_refused` (in `tests.test_e2r_runner`).

2. The first skip line in step 9's output ends with an opening single quote and no reason text: `... (link='symlink') ... skipped '`. The line is copied above exactly as printed. The other two skip lines print a complete reason, `skipped 'platform disallows symlinks'`.

3. E2R-T12 ran inside step 9's `tests.test_e2r_runner` group, which reported `ran 34 (expected 34) skipped 1 OK (skipped=1)`. The runner finished with exit code 0 and the command returned to the prompt; no worker process or console window was left behind.

4. Step 10 (`git add`) printed 90 `warning: in the working copy of '<path>', LF will be replaced by CRLF the next time Git touches it` lines, one for each of the 90 overlay paths, before the two GUARD PASS lines. The clone's `core.autocrlf` was reported as `true` in step 3. The exit code was 0 and both GUARD PASS lines printed.

5. Step 8 printed `contract_data files: 282, with CRLF line endings: 234`, with `registry loaded: 80 declarations, 202 registry chains`.

6. Step 4 reported `93 files extracted`, which is 3 more than the 90 files the overlay copies in step 6.
