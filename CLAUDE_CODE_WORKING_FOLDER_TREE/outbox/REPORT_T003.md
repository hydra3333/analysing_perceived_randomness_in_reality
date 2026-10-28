# REPORT_T003 - Windows rehearsal of the E2R-CODE-1 install, in a task clone

RESULT: PASS

- Task file: inbox/TASK_T003.md at main-repository commit a6a92d724fb36c84b18e03e83309e5105dcc1121
- Run by: Claude Code (local runner), 29 October 2026, 01:20 to 01:23 local time (UTC+10:30)
- Owner options used: none (the task file offers none; E2R-T12 was run in step 9, as the task file requires)
- Machine: Windows-11-10.0.26300-SP0; Python 3.15.2 at E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | Python | 0 | venv path, 3.15.2, Windows-11-10.0.26300-SP0 |
| 2 | Main repository state (read-only) | 0 | clean tree; HEAD a6a92d72 |
| 3 | Make the task clone | 0 | MAKE PASS |
| 4 | Check and extract the package | 0 | UNZIP PASS: 159 files extracted |
| 5 | PRE check | 0 | GUARD PASS, then PRE PASS |
| 6 | Copy the overlay into the clone | 0 | OVERLAY PASS: 156 files copied |
| 7 | POST check | 0 | POST PASS |
| 8 | Module origin | 0 | ORIGIN PASS |
| 9 | All 138 tests, including E2R-T12 | 0 | SUITE PASS: all 138 tests ran and passed |
| 10 | Stage in the clone | 0 | GUARD PASS (after); git add exit code 0 |
| 11 | Status in the clone | 0 | 156 status lines, all starting with A; git status exit code 0 |
| 12 | Commit in the clone | 0 | GUARD PASS (after); git commit exit code 0 |
| 13 | COMMITTED check | 0 | COMMITTED PASS |
| 14 | Final state of the clone | 0 | 5c2179f on top of a6a92d7; git log exit code 0 |
| 15 | Remove the task clone | 0 | REMOVE PASS |

Step 9 wall-clock time: 14 seconds (started 01:21:26, ended 01:21:40, local time UTC+10:30).

Main repository `git status --short` after step 15: the same as in step 2 (no output; the working tree is clean), and HEAD is still a6a92d724fb36c84b18e03e83309e5105dcc1121. The re-run is recorded under "Clean-up" below.

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

Commands (read-only, in the main repository):

```text
git status --short
git rev-parse HEAD
git log -1 --format=%s
```

Exit codes: 0, 0, 0

`git status --short` printed no output at all (the working tree is clean).

`git rev-parse HEAD`:

```text
a6a92d724fb36c84b18e03e83309e5105dcc1121
```

`git log -1 --format=%s`:

```text
CLAUDE_CODE_WORKING_FOLDER_TREE: report for task T002 (Claude Code local runner)
```

### Step 3

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T003
```

Exit code: 0

```text
cloning from https://github.com/hydra3333/analysing_perceived_randomness_in_reality
GUARD PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r is a task clone with no remote and a refusing pre-push hook
git remote -v: ''
clone HEAD: a6a92d724fb36c84b18e03e83309e5105dcc1121
main repository HEAD: a6a92d724fb36c84b18e03e83309e5105dcc1121
core.autocrlf in the clone: true
MAKE PASS
```

### Step 4

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T003 --zip exchange/EX_037_Claude/E2R_CODE1_Install_v2.zip --sha256 5a2b978c96d82e3159cc50e8c24a2f29a944a39d29b7452452f8b484b9a23a11
```

Exit code: 0

```text
ZIP SHA-256: 5a2b978c96d82e3159cc50e8c24a2f29a944a39d29b7452452f8b484b9a23a11
UNZIP PASS: 159 files extracted into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\p
```

### Step 5

First command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" guard --task T003
```

Exit code: 0

```text
GUARD PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r is a task clone with no remote and a refusing pre-push hook
```

Second command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\p\E2R_CODE1_Install_v2\VERIFY_E2R_CODE1_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r" --phase pre
```

Exit code: 0

```text
HEAD: a6a92d724fb36c84b18e03e83309e5105dcc1121 (descends from base 2f4e84e)
10 guarded files unchanged in Git HEAD
PRE PASS: clean tree; 156 new paths absent. Nothing was changed.
Read-only: no project code imported, nothing run, nothing changed.
```

### Step 6

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T003 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\p\E2R_CODE1_Install_v2\repo_overlay"
```

Exit code: 0

```text
OVERLAY PASS: 156 files copied into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r (new files only)
```

### Step 7

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\p\E2R_CODE1_Install_v2\VERIFY_E2R_CODE1_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r" --phase post
```

Exit code: 0

```text
HEAD: a6a92d724fb36c84b18e03e83309e5105dcc1121 (descends from base 2f4e84e)
10 guarded files unchanged in Git HEAD
POST PASS: exactly the 156 expected new paths, all with the expected bytes.
Read-only: no project code imported, nothing run, nothing changed.
```

### Step 8

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r"
```

Exit code: 0

```text
python: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe 3.15.2
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Lib\site-packages
ok   _common.contract_vocab               E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r\src\methods\_common\contract_vocab.py
ok   _common.contract_records             E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r\src\methods\_common\contract_records.py
ok   _common.contract_task                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r\src\methods\_common\contract_task.py
ok   _common.contract_forecast            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r\src\methods\_common\contract_forecast.py
ok   _common.contract_receipts            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r\src\methods\_common\contract_receipts.py
ok   _common.contract_registry            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r\src\methods\_common\contract_registry.py
ok   _common.canonical_encoding           E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r\src\methods\_common\canonical_encoding.py
ok   _common.game_profiles                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r\src\methods\_common\game_profiles.py
ok   _common.game_draws_reader            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r\src\methods\_common\game_draws_reader.py
ok   E_001.multigame_e1                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r\src\methods\E_001\multigame_e1.py
ok   e2r_fixtures                         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r\tests\e2r_fixtures.py
contract_data: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r\src\methods\_common\contract_data
contract_data files: 126, with CRLF line endings: 0
registry loaded: 2 declarations, 124 registry chains
ORIGIN PASS: every checked module and the contract data come from the task clone
```

### Step 9

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\p\E2R_CODE1_Install_v2\RUN_E2R_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r"
```

Exit code: 0

Wall-clock time: 14 seconds (started 01:21:26, ended 01:21:40, local time UTC+10:30).

```text
environment: Windows 11 Python 3.15.2 E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
tests.test_multigame_reader_contracts                ran  10 (expected 10)  skipped 1  OK (skipped=1)
    skip: test_reject_symlinks_and_hardlinks_and_dateload_mismatch (tests.test_multigame_reader_contracts.V011ReaderTests.test_reject_symlinks_and_hardlinks_and_dateload_mismatch) (link='symlink') ... skipped '
tests.test_multigame_static_and_timing               ran   6 (expected  6)  skipped 0  OK
tests.test_multigame_launch_and_manifest             ran  11 (expected 11)  skipped 0  OK
tests.test_multigame_exit_receipt                    ran  18 (expected 18)  skipped 1  OK (skipped=1)
    skip: test_symlink_receipts_directory_is_refused (tests.test_multigame_exit_receipt.ReceiptTests.test_symlink_receipts_directory_is_refused) ... skipped 'platform disallows symlinks'
tests.test_multigame_science_allowlist                ran   6 (expected  6)  skipped 0  OK
tests.test_multigame_console_and_synthetic_scorer    ran   7 (expected  7)  skipped 0  OK
tests.test_t05_hardening                             ran   2 (expected  2)  skipped 0  OK
tests.test_e1_align                                  ran   5 (expected  5)  skipped 0  OK
tests.test_e1_standalone                             ran  13 (expected 13)  skipped 0  OK
tests.test_multigame_windows_lifecycle_review        ran   6 (expected  6)  skipped 0  OK
tests.test_e2r_contract                              ran  53 (expected 53)  skipped 0  OK
tests.test_e2r_prefix                                ran   1 (expected  1)  skipped 0  OK
total ran 138 (expected 138); skips 2
SUITE PASS: all 138 tests ran and passed; only the allowed symlink skips, if any.
```

### Step 10

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T003 -- add doc review src tests
```

Exit code: 0

```text
warning: in the working copy of 'doc/Predictive_Randomness_E2R_Code_Scope_v0_1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'doc/RATIFICATION_REGISTER_v0_11.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_EX034_Corrections_v0_1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_Implementation_Notes_v0_1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_Install_v2/INSTALL_MANIFEST_SHA256.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_Install_v2/code_v1_to_v2.diff', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_Install_v2/e2r_mutation_checks_linux.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_Install_v2/r4_oracle_agreement_linux.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_Install_v2/suite_e2r_linux_py313.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_Install_v2/suite_e2r_linux_py315b4.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_Install_v2/tools/build_contract_data.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_Install_v2/tools/e2r_mutations.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_Install_v2/tools/e2r_oracle_export.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_Install_v2/tools/make_register_v11.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/E2R_CODE1_Install_v2/tools/r2_method_names.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/Independent_ChatGPT_E1ALIGN_Code_RECHECK_v0_1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/Independent_ChatGPT_E2R_CODE1_HIGH_RECHECK_v0_1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/Independent_ChatGPT_E2R_Code_Scope_Review_v0_1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/Independent_ChatGPT_Register_v0_10_Review_v0_1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/Independent_E2R_T05_Oracle_Plan_v0_1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/Independent_E2R_T05_Oracle_v0_1.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/OZLOTTO/E_1/FULL_HISTORY_RAW_COUNTS_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/declarations/POWERBALL/E_1/FULL_HISTORY_RAW_COUNTS_V1/r1.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_1/FULL_HISTORY_RAW_COUNTS_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_10/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_11/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_12/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_13/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_14/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_15/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_16/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_17/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_18/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_19/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_2/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_20/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_21/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_22/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_23/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_24/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_25/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_26/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_27/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_28/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_29/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_3/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_30/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_31/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_32/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_33/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_34/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_35/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_36/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_37/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_38/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_39/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_4/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_40/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_41/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_42/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_43/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_44/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_45/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_46/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_47/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_48/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_49/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_5/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_50/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_51/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_52/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_53/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_54/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_55/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_56/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_57/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_58/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_59/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_6/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_60/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_61/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_62/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_7/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_8/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_9/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_1/FULL_HISTORY_RAW_COUNTS_V1/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_10/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_11/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_12/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_13/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_14/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_15/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_16/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_17/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_18/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_19/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_2/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_20/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_21/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_22/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_23/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_24/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_25/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_26/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_27/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_28/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_29/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_3/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_30/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_31/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_32/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_33/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_34/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_35/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_36/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_37/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_38/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_39/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_4/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_40/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_41/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_42/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_43/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_44/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_45/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_46/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_47/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_48/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_49/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_5/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_50/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_51/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_52/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_53/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_54/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_55/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_56/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_57/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_58/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_59/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_6/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_60/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_61/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_62/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_7/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_8/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_9/NOT_YET_SPECIFIED/entry_0001.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_forecast.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_receipts.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_records.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_registry.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_task.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_vocab.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/e2r_fixtures.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_e2r_contract.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_e2r_prefix.py', LF will be replaced by CRLF the next time Git touches it
GUARD PASS (before)
GUARD PASS (after); git add exit code 0
```

### Step 11

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T003 -- status --short
```

Exit code: 0

As the task file directs, the 156 status lines are not pasted. Counts:

- Total lines printed by the command: 158
- Status lines: 156
- Status lines starting with `A`: 156
- Status lines not starting with `A`: 0 (there were none to list)

The two remaining lines of the command's output are the tool's own lines, printed in full here:

```text
GUARD PASS (before)
GUARD PASS (after); git status exit code 0
```

### Step 12

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T003 -- commit -q -m "E2R-CODE-1 rehearsal (task clone T003 only; never pushed)"
```

Exit code: 0

```text
GUARD PASS (before)
GUARD PASS (after); git commit exit code 0
```

### Step 13

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\p\E2R_CODE1_Install_v2\VERIFY_E2R_CODE1_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003\r" --phase committed
```

Exit code: 0

```text
HEAD: 5c2179f1fc36a7d5b04bc3dd999c2daa07e5fa85 (descends from base 2f4e84e)
10 guarded files unchanged in Git HEAD
COMMITTED PASS: the last commit (5c2179f) added exactly 156 files; all Git blobs match.
Read-only: no project code imported, nothing run, nothing changed.
```

### Step 14

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T003 -- log --oneline -2
```

Exit code: 0

```text
5c2179f E2R-CODE-1 rehearsal (task clone T003 only; never pushed)
a6a92d7 CLAUDE_CODE_WORKING_FOLDER_TREE: report for task T002 (Claude Code local runner)
GUARD PASS (before)
GUARD PASS (after); git log exit code 0
```

## Clean-up

### Step 15

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T003
```

Exit code: 0

```text
REMOVE PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T003 deleted
```

The task clone was removed, so nothing was left in place.

### The main repository after step 15

Commands (read-only, in the main repository):

```text
git status --short
git rev-parse HEAD
```

Exit codes: 0, 0

`git status --short` printed no output at all. This is the same as in step 2: the working tree was clean before the task and is clean after it.

`git rev-parse HEAD`:

```text
a6a92d724fb36c84b18e03e83309e5105dcc1121
```

(The same commit as in step 2. This report file is committed afterwards, in step 17.)

## Deviations

None.

## Observations

- Step 9 printed two skips, both of them the allowed symlink skips the runner's own PASS line permits: one in `tests.test_multigame_reader_contracts` and one in `tests.test_multigame_exit_receipt`. The first skip line ends after `skipped '`, with no reason text following it on that line or the next; this is exactly what the runner printed, and the same line appeared in the same form in task T002.
- Step 10 printed 156 `warning: in the working copy of '...', LF will be replaced by CRLF the next time Git touches it` lines, one for each of the 156 overlay files. The task clone was made with `core.autocrlf` set to `true` (step 3 reports this), and the POST check in step 7 and the COMMITTED check in step 13 both passed, so these warnings did not affect any check.
- Step 9 ran in 14 seconds, with E2R-T12 included. E2R-T12's worker processes finished on their own; nothing had to be waited for or stopped.
