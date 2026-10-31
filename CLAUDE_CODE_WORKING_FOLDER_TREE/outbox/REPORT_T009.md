# REPORT_T009 - Windows rehearsal of the REL-1 install, in a task clone

RESULT: PASS

- Task file: inbox/TASK_T009.md at main-repository commit b997d0842213c09ca466e2aa00933ee17311406f
- Run by: Claude Code (local runner), 31 October 2026, 13:38 to 13:46 local time, +10:30 (reported by the shell as CAST)
- Owner options used: defaults (the task file offers none; E2R-T12 was run in step 10, as the task file gives it)
- Machine: Windows-11-10.0.26300-SP0; Python 3.15.2 at E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe

Wall-clock time for step 10 (the 304-test suite): 252 seconds (4 minutes 12 seconds), from 2026-10-31T13:41:33+10:30 to 2026-10-31T13:45:45+10:30.

The main repository's `git status --short` after step 16 is the same as in step 2: empty (no output) both times. Both runs exited 0.

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | Python | 0 | venv path; 3.15.2; Windows-11-10.0.26300-SP0 |
| 2 | Main repository state (read-only) | 0, 0, 0 | empty status; HEAD b997d0842213c09ca466e2aa00933ee17311406f |
| 3 | Make the task clone | 0 | MAKE PASS |
| 4 | Check and extract the package | 0 | UNZIP PASS: 100 files extracted |
| 5 | PRE check (guard, then VERIFY --phase pre) | 0, 0 | GUARD PASS; PRE PASS |
| 6 | Copy the overlay into the clone | 0 | OVERLAY PASS: 97 files copied (92 new, 5 replaced) |
| 7 | Delete the 11 flags in the clone | 0 | GUARD PASS (after); git rm exit code 0 |
| 8 | POST check | 0 | POST PASS: exactly the 92 expected new paths, 5 modified files and 11 staged deletions, all with the expected bytes. |
| 9 | Module origin | 0 | ORIGIN PASS |
| 10 | All 304 tests, including E2R-T12 | 0 | SUITE PASS: all 304 tests ran and passed; only the allowed symlink skips, if any. |
| 11 | Stage in the clone | 0 | GUARD PASS (after); git add exit code 0 |
| 12 | Status in the clone | 0 | 108 lines: 92 A, 5 M, 11 D; git status exit code 0 |
| 13 | Commit in the clone | 0 | GUARD PASS (after); git commit exit code 0 |
| 14 | COMMITTED check | 0 | COMMITTED PASS |
| 15 | Final state of the clone | 0 | edbcbe4 on top of b997d08; git log exit code 0 |
| 16 | Remove the task clone (clean-up) | 0 | REMOVE PASS |

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

Command:

```text
git status --short
```

Exit code: 0

```text
(no output)
```

Command:

```text
git rev-parse HEAD
```

Exit code: 0

```text
b997d0842213c09ca466e2aa00933ee17311406f
```

Command:

```text
git log -1 --format=%s
```

Exit code: 0

```text
exchange: roadmap and R-005 - CODE-3 and E_1 r2 design v0.1r2 owner-ratified (31 October 2026); coding started
```

### Step 3

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T009
```

Exit code: 0

```text
cloning from https://github.com/hydra3333/analysing_perceived_randomness_in_reality
GUARD PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r is a task clone with no remote and a refusing pre-push hook
git remote -v: ''
clone HEAD: b997d0842213c09ca466e2aa00933ee17311406f
main repository HEAD: b997d0842213c09ca466e2aa00933ee17311406f
core.autocrlf in the clone: true
MAKE PASS
```

### Step 4

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T009 --zip exchange/EX_086_Claude/REL1_Install_v2.zip --sha256 3ca731fe22ffc10a2dd4f59fd5f5725f9f6c88553a426f12eea395795e1e4b36
```

Exit code: 0

```text
ZIP SHA-256: 3ca731fe22ffc10a2dd4f59fd5f5725f9f6c88553a426f12eea395795e1e4b36
UNZIP PASS: 100 files extracted into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\p
```

### Step 5

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" guard --task T009
```

Exit code: 0

```text
GUARD PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r is a task clone with no remote and a refusing pre-push hook
```

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\p\REL1_Install_v2\VERIFY_REL1_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r" --phase pre
```

Exit code: 0

```text
HEAD: b997d0842213c09ca466e2aa00933ee17311406f (descends from base d15183e)
28 guarded files unchanged in Git HEAD
PRE PASS: clean tree; 92 new paths absent; 5 files to replace and 11 to delete at their base version. Nothing was changed.
Read-only: no project code imported, nothing run, nothing changed.
```

### Step 6

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T009 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\p\REL1_Install_v2\repo_overlay" --replace tests/test_e2r_dispatch.py tests/test_e3_e4_polynomial.py tests/test_e6_beta_bernoulli.py tests/test_wave1_frequency.py tests/test_wave2_recurrence.py
```

Exit code: 0

```text
OVERLAY PASS: 97 files copied into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r (92 new, 5 replaced)
```

### Step 7

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T009 -- rm -q -- src/methods/E_002/IN_DEVELOPMENT.txt src/methods/E_003/IN_DEVELOPMENT.txt src/methods/E_004/IN_DEVELOPMENT.txt src/methods/E_006/IN_DEVELOPMENT.txt src/methods/E_007/IN_DEVELOPMENT.txt src/methods/E_008/IN_DEVELOPMENT.txt src/methods/E_009/IN_DEVELOPMENT.txt src/methods/E_010/IN_DEVELOPMENT.txt src/methods/E_017/IN_DEVELOPMENT.txt src/methods/E_018/IN_DEVELOPMENT.txt src/methods/E_019/IN_DEVELOPMENT.txt
```

Exit code: 0

```text
GUARD PASS (before)
GUARD PASS (after); git rm exit code 0
```

### Step 8

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\p\REL1_Install_v2\VERIFY_REL1_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r" --phase post
```

Exit code: 0

```text
HEAD: b997d0842213c09ca466e2aa00933ee17311406f (descends from base d15183e)
28 guarded files unchanged in Git HEAD
POST PASS: exactly the 92 expected new paths, 5 modified files and 11 staged deletions, all with the expected bytes.
Read-only: no project code imported, nothing run, nothing changed.
```

### Step 9

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r"
```

Exit code: 0

```text
python: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe 3.15.2
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Lib\site-packages
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv
ok   _common.contract_vocab               E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\contract_vocab.py
ok   _common.contract_records             E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\contract_records.py
ok   _common.contract_task                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\contract_task.py
ok   _common.contract_forecast            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\contract_forecast.py
ok   _common.contract_receipts            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\contract_receipts.py
ok   _common.contract_registry            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\contract_registry.py
ok   _common.canonical_encoding           E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\canonical_encoding.py
ok   _common.game_profiles                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\game_profiles.py
ok   _common.game_draws_reader            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\game_draws_reader.py
ok   E_001.multigame_e1                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\E_001\multigame_e1.py
ok   e2r_fixtures                         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\tests\e2r_fixtures.py
ok   _common.contract_dispatch            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\contract_dispatch.py
ok   _common.contract_publication         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\contract_publication.py
ok   _common.contract_runner              E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\contract_runner.py
ok   contract_adapters.e_001              E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\contract_adapters\e_001.py
ok   e2r_code2_fixtures                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\tests\e2r_code2_fixtures.py
contract_data: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r\src\methods\_common\contract_data
contract_data files: 360, with CRLF line endings: 282
registry loaded: 80 declarations, 202 registry chains
ORIGIN PASS: every checked module and the contract data come from the task clone
```

### Step 10

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\p\REL1_Install_v2\RUN_REL1_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r"
```

Exit code: 0

Wall-clock time: 252 seconds (4 minutes 12 seconds), from 2026-10-31T13:41:33+10:30 to 2026-10-31T13:45:45+10:30.

```text
environment: Windows 11 Python 3.15.2 E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
tests.test_multigame_reader_contracts                ran  10 (expected 10)  skipped 1  OK (skipped=1)  (0.7 s)
    skip: test_reject_symlinks_and_hardlinks_and_dateload_mismatch (tests.test_multigame_reader_contracts.V011ReaderTests.test_reject_symlinks_and_hardlinks_and_dateload_mismatch) (link='symlink') ... skipped '
tests.test_multigame_static_and_timing               ran   6 (expected  6)  skipped 0  OK  (0.6 s)
tests.test_multigame_launch_and_manifest             ran  11 (expected 11)  skipped 0  OK  (3.7 s)
tests.test_multigame_exit_receipt                    ran  18 (expected 18)  skipped 1  OK (skipped=1)  (3.7 s)
    skip: test_symlink_receipts_directory_is_refused (tests.test_multigame_exit_receipt.ReceiptTests.test_symlink_receipts_directory_is_refused) ... skipped 'platform disallows symlinks'
tests.test_multigame_science_allowlist               ran   6 (expected  6)  skipped 0  OK  (2.7 s)
tests.test_multigame_console_and_synthetic_scorer    ran   7 (expected  7)  skipped 0  OK  (1.1 s)
tests.test_t05_hardening                             ran   2 (expected  2)  skipped 0  OK  (3.9 s)
tests.test_e1_align                                  ran   5 (expected  5)  skipped 0  OK  (0.4 s)
tests.test_e1_standalone                             ran  13 (expected 13)  skipped 0  OK  (2.1 s)
tests.test_multigame_windows_lifecycle_review        ran   6 (expected  6)  skipped 0  OK  (1.5 s)
tests.test_e2r_contract                              ran  53 (expected 53)  skipped 0  OK  (5.1 s)
tests.test_e2r_prefix                                ran   1 (expected  1)  skipped 0  OK  (3.5 s)
tests.test_e2r_dispatch                              ran  18 (expected 18)  skipped 0  OK  (24.0 s)
tests.test_e2r_runner                                ran  34 (expected 34)  skipped 1  OK (skipped=1)  (19.7 s)
    skip: test_dangling_symlink_target_is_refused (tests.test_e2r_runner.AtomicCreateOnly.test_dangling_symlink_target_is_refused) ... skipped 'platform disallows symlinks'
tests.test_e6_beta_bernoulli                         ran  20 (expected 20)  skipped 0  OK  (15.7 s)
tests.test_polynomial_fits                           ran  19 (expected 19)  skipped 0  OK  (0.9 s)
tests.test_e3_e4_polynomial                          ran  13 (expected 13)  skipped 0  OK  (45.5 s)
tests.test_occurrence_counts                         ran   8 (expected  8)  skipped 0  OK  (0.5 s)
tests.test_wave1_frequency                           ran  18 (expected 18)  skipped 0  OK  (32.8 s)
tests.test_recurrence_gaps                           ran  12 (expected 12)  skipped 0  OK  (0.7 s)
tests.test_wave2_recurrence                          ran  19 (expected 19)  skipped 0  OK  (50.7 s)
tests.test_rel1_release                              ran   5 (expected  5)  skipped 0  OK  (31.6 s)
total ran 304 (expected 304); skips 3
SUITE PASS: all 304 tests ran and passed; only the allowed symlink skips, if any.
```

### Step 11

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T009 -- add doc review src tests
```

Exit code: 0

```text
warning: in the working copy of 'tests/test_e2r_dispatch.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_e3_e4_polynomial.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_e6_beta_bernoulli.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_wave1_frequency.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_wave2_recurrence.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'doc/Predictive_Randomness_Releases_and_WF1_Design_v0_1r1.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'doc/RATIFICATION_REGISTER_v0_21.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/Independent_ChatGPT_WF1_Design_Focused_RECHECK_EX080.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/Independent_ChatGPT_WF1_Design_R3_Review_EX078.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/REL1_Install_v2/INSTALL_MANIFEST_SHA256.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/REL1_Install_v2/mutations_rel1_py313.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/REL1_Install_v2/replaced_files_base_to_v1.diff', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/REL1_Install_v2/suite_rel1_py313.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/REL1_Install_v2/suite_rel1_py315.txt', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/REL1_Install_v2/tools/edit_tests_rel1.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/REL1_Install_v2/tools/make_register_v21.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/REL1_Install_v2/tools/make_rel1_release.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'review/REL1_Install_v2/tools/wf1_mutations.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_10/CONTRAST_S13_L104_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_10/CONTRAST_S26_L208_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_10/CONTRAST_S52_FULL_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_17/HAZARD_BINS_C100_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_17/HAZARD_BINS_W208_C100_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_17/HAZARD_LOGAGE_SIGN_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_18/MIX4_ALL_C10_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_18/MIX4_W104_C10_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_18/MIX4_W208_C10_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_19/PERIODIC_T2_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_19/PERIODIC_T3_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_19/PERIODIC_T4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_2/RECUR_MEAN_ALL_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_2/RECUR_MEAN_LAST8_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_2/RECUR_MEDIAN_ALL_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_3/POLY_INTERP_W52_D4_H4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_3/POLY_LS_W104_D3_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_3/POLY_LS_W52_D2_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_3/POLY_LS_W52_D3_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_3/POLY_MINIMAX_W52_D2_H4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_3/POLY_MINIMAX_W52_D3_H4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_4/POLY_INTERP_W52_D4_H4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_4/POLY_LS_W104_D3_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_4/POLY_LS_W52_D2_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_4/POLY_LS_W52_D3_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_4/POLY_MINIMAX_W52_D2_H4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_4/POLY_MINIMAX_W52_D3_H4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_6/BETA_BERNOULLI_DECAY_149_150_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_6/BETA_BERNOULLI_DECAY_74_75_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_6/BETA_BERNOULLI_FULL_MEMORY_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_7/BETA_SHRINK_FULL_C52_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_7/BETA_SHRINK_W104_C52_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_7/BETA_SHRINK_W52_C52_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_8/HIER_PERIODS_P13_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_8/HIER_PERIODS_P26_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_8/HIER_PERIODS_P52_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_9/EXP_DECAY_18_19_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_9/EXP_DECAY_37_38_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/OZLOTTO/E_9/EXP_DECAY_5_6_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_10/CONTRAST_S13_L104_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_10/CONTRAST_S26_L208_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_10/CONTRAST_S52_FULL_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_17/HAZARD_BINS_C100_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_17/HAZARD_BINS_W208_C100_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_17/HAZARD_LOGAGE_SIGN_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_18/MIX4_ALL_C10_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_18/MIX4_W104_C10_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_18/MIX4_W208_C10_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_19/PERIODIC_T2_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_19/PERIODIC_T3_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_19/PERIODIC_T4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_2/RECUR_MEAN_ALL_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_2/RECUR_MEAN_LAST8_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_2/RECUR_MEDIAN_ALL_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_3/POLY_INTERP_W52_D4_H4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_3/POLY_LS_W104_D3_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_3/POLY_LS_W52_D2_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_3/POLY_LS_W52_D3_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_3/POLY_MINIMAX_W52_D2_H4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_3/POLY_MINIMAX_W52_D3_H4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_4/POLY_INTERP_W52_D4_H4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_4/POLY_LS_W104_D3_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_4/POLY_LS_W52_D2_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_4/POLY_LS_W52_D3_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_4/POLY_MINIMAX_W52_D2_H4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_4/POLY_MINIMAX_W52_D3_H4_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_6/BETA_BERNOULLI_DECAY_149_150_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_6/BETA_BERNOULLI_DECAY_74_75_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_6/BETA_BERNOULLI_FULL_MEMORY_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_7/BETA_SHRINK_FULL_C52_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_7/BETA_SHRINK_W104_C52_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_7/BETA_SHRINK_W52_C52_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_8/HIER_PERIODS_P13_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_8/HIER_PERIODS_P26_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_8/HIER_PERIODS_P52_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_9/EXP_DECAY_18_19_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_9/EXP_DECAY_37_38_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'src/methods/_common/contract_data/registry/POWERBALL/E_9/EXP_DECAY_5_6_V1/entry_0002.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_rel1_release.py', LF will be replaced by CRLF the next time Git touches it
GUARD PASS (before)
GUARD PASS (after); git add exit code 0
```

### Step 12

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T009 -- status --short
```

Exit code: 0

The whole output, exactly as printed:

```text
A  doc/Predictive_Randomness_Releases_and_WF1_Design_v0_1r1.md
A  doc/RATIFICATION_REGISTER_v0_21.md
A  review/Independent_ChatGPT_WF1_Design_Focused_RECHECK_EX080.md
A  review/Independent_ChatGPT_WF1_Design_R3_Review_EX078.md
A  review/REL1_Install_v2/INSTALL_MANIFEST_SHA256.txt
A  review/REL1_Install_v2/mutations_rel1_py313.txt
A  review/REL1_Install_v2/replaced_files_base_to_v1.diff
A  review/REL1_Install_v2/suite_rel1_py313.txt
A  review/REL1_Install_v2/suite_rel1_py315.txt
A  review/REL1_Install_v2/tools/edit_tests_rel1.py
A  review/REL1_Install_v2/tools/make_register_v21.py
A  review/REL1_Install_v2/tools/make_rel1_release.py
A  review/REL1_Install_v2/tools/wf1_mutations.py
D  src/methods/E_002/IN_DEVELOPMENT.txt
D  src/methods/E_003/IN_DEVELOPMENT.txt
D  src/methods/E_004/IN_DEVELOPMENT.txt
D  src/methods/E_006/IN_DEVELOPMENT.txt
D  src/methods/E_007/IN_DEVELOPMENT.txt
D  src/methods/E_008/IN_DEVELOPMENT.txt
D  src/methods/E_009/IN_DEVELOPMENT.txt
D  src/methods/E_010/IN_DEVELOPMENT.txt
D  src/methods/E_017/IN_DEVELOPMENT.txt
D  src/methods/E_018/IN_DEVELOPMENT.txt
D  src/methods/E_019/IN_DEVELOPMENT.txt
A  src/methods/_common/contract_data/registry/OZLOTTO/E_10/CONTRAST_S13_L104_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_10/CONTRAST_S26_L208_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_10/CONTRAST_S52_FULL_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_17/HAZARD_BINS_C100_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_17/HAZARD_BINS_W208_C100_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_17/HAZARD_LOGAGE_SIGN_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_18/MIX4_ALL_C10_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_18/MIX4_W104_C10_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_18/MIX4_W208_C10_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_19/PERIODIC_T2_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_19/PERIODIC_T3_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_19/PERIODIC_T4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_2/RECUR_MEAN_ALL_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_2/RECUR_MEAN_LAST8_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_2/RECUR_MEDIAN_ALL_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_3/POLY_INTERP_W52_D4_H4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_3/POLY_LS_W104_D3_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_3/POLY_LS_W52_D2_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_3/POLY_LS_W52_D3_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_3/POLY_MINIMAX_W52_D2_H4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_3/POLY_MINIMAX_W52_D3_H4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_4/POLY_INTERP_W52_D4_H4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_4/POLY_LS_W104_D3_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_4/POLY_LS_W52_D2_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_4/POLY_LS_W52_D3_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_4/POLY_MINIMAX_W52_D2_H4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_4/POLY_MINIMAX_W52_D3_H4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_6/BETA_BERNOULLI_DECAY_149_150_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_6/BETA_BERNOULLI_DECAY_74_75_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_6/BETA_BERNOULLI_FULL_MEMORY_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_7/BETA_SHRINK_FULL_C52_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_7/BETA_SHRINK_W104_C52_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_7/BETA_SHRINK_W52_C52_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_8/HIER_PERIODS_P13_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_8/HIER_PERIODS_P26_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_8/HIER_PERIODS_P52_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_9/EXP_DECAY_18_19_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_9/EXP_DECAY_37_38_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/OZLOTTO/E_9/EXP_DECAY_5_6_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_10/CONTRAST_S13_L104_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_10/CONTRAST_S26_L208_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_10/CONTRAST_S52_FULL_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_17/HAZARD_BINS_C100_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_17/HAZARD_BINS_W208_C100_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_17/HAZARD_LOGAGE_SIGN_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_18/MIX4_ALL_C10_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_18/MIX4_W104_C10_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_18/MIX4_W208_C10_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_19/PERIODIC_T2_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_19/PERIODIC_T3_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_19/PERIODIC_T4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_2/RECUR_MEAN_ALL_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_2/RECUR_MEAN_LAST8_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_2/RECUR_MEDIAN_ALL_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_3/POLY_INTERP_W52_D4_H4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_3/POLY_LS_W104_D3_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_3/POLY_LS_W52_D2_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_3/POLY_LS_W52_D3_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_3/POLY_MINIMAX_W52_D2_H4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_3/POLY_MINIMAX_W52_D3_H4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_4/POLY_INTERP_W52_D4_H4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_4/POLY_LS_W104_D3_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_4/POLY_LS_W52_D2_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_4/POLY_LS_W52_D3_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_4/POLY_MINIMAX_W52_D2_H4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_4/POLY_MINIMAX_W52_D3_H4_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_6/BETA_BERNOULLI_DECAY_149_150_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_6/BETA_BERNOULLI_DECAY_74_75_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_6/BETA_BERNOULLI_FULL_MEMORY_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_7/BETA_SHRINK_FULL_C52_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_7/BETA_SHRINK_W104_C52_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_7/BETA_SHRINK_W52_C52_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_8/HIER_PERIODS_P13_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_8/HIER_PERIODS_P26_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_8/HIER_PERIODS_P52_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_9/EXP_DECAY_18_19_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_9/EXP_DECAY_37_38_V1/entry_0002.json
A  src/methods/_common/contract_data/registry/POWERBALL/E_9/EXP_DECAY_5_6_V1/entry_0002.json
M  tests/test_e2r_dispatch.py
M  tests/test_e3_e4_polynomial.py
M  tests/test_e6_beta_bernoulli.py
A  tests/test_rel1_release.py
M  tests/test_wave1_frequency.py
M  tests/test_wave2_recurrence.py
GUARD PASS (before)
GUARD PASS (after); git status exit code 0
```

### Step 13

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T009 -- commit -q -m "REL-1 rehearsal (task clone T009 only; never pushed)"
```

Exit code: 0

```text
GUARD PASS (before)
GUARD PASS (after); git commit exit code 0
```

### Step 14

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\p\REL1_Install_v2\VERIFY_REL1_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r" --phase committed
```

Exit code: 0

```text
HEAD: edbcbe498d8ad019c70594583d0df6bf912e3f5a (descends from base d15183e)
28 guarded files unchanged in Git HEAD
COMMITTED PASS: the last commit (edbcbe4) added exactly 92 files, modified 5 and deleted 11; all Git blobs match.
Read-only: no project code imported, nothing run, nothing changed.
```

### Step 15

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T009 -- log --oneline -2
```

Exit code: 0

```text
edbcbe4 REL-1 rehearsal (task clone T009 only; never pushed)
b997d08 exchange: roadmap and R-005 - CODE-3 and E_1 r2 design v0.1r2 owner-ratified (31 October 2026); coding started
GUARD PASS (before)
GUARD PASS (after); git log exit code 0
```

## Clean-up

### Step 16

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T009
```

Exit code: 0

```text
REMOVE PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009 deleted
```

### Main repository status after step 16

Command:

```text
git status --short
```

Exit code: 0

```text
(no output)
```

This is the same as step 2: empty in both cases.

## Deviations

None. Every command was run exactly as written in the task file, from MAIN, in the order given.

## Observations

- Step 12 printed 108 status lines: 92 beginning with `A`, 5 beginning with `M` (the five replaced test files) and 11 beginning with `D` (the flags), as the task file expected. The output above was copied as printed and was not redirected to a file or counted by another command.
- Step 10 reported 3 skips, all symlink-related (`test_reject_symlinks_and_hardlinks_and_dateload_mismatch`, `test_symlink_receipts_directory_is_refused`, `test_dangling_symlink_target_is_refused`), within the up to 3 allowed on Windows. The runner itself printed `SUITE PASS`.
- The first skip line printed by the runner in step 10 ends mid-text with an unclosed single quote (`... ... skipped '`); it is copied above exactly as printed. The other two skip lines print a complete reason.
- Step 11 printed 97 `warning: in the working copy of ... LF will be replaced by CRLF the next time Git touches it` lines before the two guard lines, one for each of the 97 files the overlay had copied. The clone reported `core.autocrlf: true` in step 3. The step still exited 0 and steps 12 to 14 passed, including the blob comparison in step 14.
- Step 4 reported 100 files extracted from the ZIP (the task file's expected line gives no count).
- Nothing was run from `src\`, no coordinator, launcher or experiment program was started, and no `source_data`, `results` or `transitory_data` folder was opened by this runner. The only network use was the `git clone` from GitHub inside `cc_clone.py make` in step 3.
