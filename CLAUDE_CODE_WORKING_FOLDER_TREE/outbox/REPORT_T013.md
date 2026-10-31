# REPORT_T013 - Windows rehearsal of the WF-1B install (the scorer and ranking report), in a task clone

RESULT: STOP at step 11

- Task file: inbox/TASK_T013.md at main-repository commit bde56b6780321070c2d60e3d618f66068d778d35
- Run by: Claude Code (local runner), 1 November 2026, 07:32 to 07:42 local time, +10:30 (reported by the shell as CAST)
- Owner options used: defaults (the task file offers none)
- Machine: Windows-11-10.0.26300-SP0; Python 3.15.2 at E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe

Steps 1 to 10 all passed, including the step T012 could not run: step 9 printed one name and was not refused by the permission layer.

Step 11 (the whole suite) ran to the end and printed `SUITE STOP`. It reported `total ran 463 (expected 463); skips 3`, and one module failed:

```text
  tests.test_wf1b_outcome_reader: exit 1, ran 5 expected 5, "FAILED (errors=1)"
```

The runner's exit code was 1. Every other module printed `OK` or `OK (skipped=1)`. The runner printed no further detail about the error, and the suite was not rerun (rulebook section 2, rule 10).

The cross-platform evidence line asked for in step 11 is:

```text
tests.test_wf1b_crossplatform                        ran   1 (expected  1)  skipped 0  OK  (21.8 s)
```

Steps 12 to 16 were therefore not run.

Step 11's wall-clock time: 8 minutes 48 seconds (start 2026-11-01T07:33:33+1030, end 2026-11-01T07:42:21+1030).

Clean-up (step 17) ran and passed; the task clone is gone.

The main repository's `git status --short` after step 17 is the same as in step 2: empty (no output) both times. Both runs exited 0. The main repository's HEAD was bde56b6780321070c2d60e3d618f66068d778d35 before and after.

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | Python | 0 | venv path; 3.15.2; Windows-11-10.0.26300-SP0 |
| 2 | Main repository state (read-only) | 0, 0, 0 | empty status; HEAD bde56b6780321070c2d60e3d618f66068d778d35 |
| 3 | Make the task clone | 0 | MAKE PASS |
| 4 | Check and extract the package | 0 | ZIP SHA-256 matched; UNZIP PASS: 42 files extracted |
| 5 | PRE check (guard, then VERIFY --phase pre) | 0, 0 | GUARD PASS; PRE PASS |
| 6 | Copy the overlay | 0 | OVERLAY PASS: 39 files copied (38 new, 1 replaced) |
| 7 | POST check | 0 | POST PASS: exactly the 38 expected new paths, 1 modified files and 0 staged deletions, all with the expected bytes. |
| 8 | Module origin | 0 | ORIGIN PASS: every checked module and the contract data come from the task clone |
| 9 | The new report wrapper is in place (read-only, by pattern) | 0 | one name, the expected one (step 9's output below) |
| 10 | Record the clone's Python files under src\evaluation | 0 | 12 names listed |
| 11 | All 463 tests, including E2R-T12 | 1 | STOP - total ran 463 (expected 463); skips 3; SUITE STOP: tests.test_wf1b_outcome_reader: exit 1, ran 5 expected 5, "FAILED (errors=1)" |
| 12 | Stage in the clone | (not run) | - |
| 13 | Status in the clone | (not run) | - |
| 14 | Commit in the clone | (not run) | - |
| 15 | COMMITTED check | (not run) | - |
| 16 | Final state of the clone | (not run) | - |
| 17 | Remove the task clone (clean-up) | 0 | REMOVE PASS |
| 18 | Main repository state again (for the report) | 0, 0 | empty status; HEAD bde56b6780321070c2d60e3d618f66068d778d35 |

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

The local time printed immediately before this command was `2026-11-01T07:32:12+1030 (CAST)`.

### Step 2

Command:

```text
git status --short
```

Output (exit code 0): no output (empty).

Command:

```text
git rev-parse HEAD
```

Output (exit code 0):

```text
bde56b6780321070c2d60e3d618f66068d778d35
```

Command:

```text
git log -1 --format=%s
```

Output (exit code 0):

```text
TASK_T013 (Windows rehearsal of WF1B_Install_v2; replaces T012, which stopped at step 9 on the .bat deny entry); roadmap item 10 condensed, items 10b-10d; reminders R-004 and R-005 closed, R-007 to R-009 added
```

### Step 3

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T013
```

Output (exit code 0):

```text
cloning from https://github.com/hydra3333/analysing_perceived_randomness_in_reality
GUARD PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r is a task clone with no remote and a refusing pre-push hook
git remote -v: ''
clone HEAD: bde56b6780321070c2d60e3d618f66068d778d35
main repository HEAD: bde56b6780321070c2d60e3d618f66068d778d35
core.autocrlf in the clone: true
MAKE PASS
```

### Step 4

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T013 --zip exchange/EX_110_Claude/WF1B_Install_v2_candidate.zip --sha256 e1efc0498be08dc045a601ad4412b9bcdb5d54a6f12310532d17d22cdfded727
```

Output (exit code 0):

```text
ZIP SHA-256: e1efc0498be08dc045a601ad4412b9bcdb5d54a6f12310532d17d22cdfded727
UNZIP PASS: 42 files extracted into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\p
```

### Step 5

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" guard --task T013
```

Output (exit code 0):

```text
GUARD PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r is a task clone with no remote and a refusing pre-push hook
```

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\p\WF1B_Install_v2\VERIFY_WF1B_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r" --phase pre
```

Output (exit code 0):

```text
HEAD: bde56b6780321070c2d60e3d618f66068d778d35 (descends from base 0c8799d)
17 guarded files unchanged in Git HEAD
PRE PASS: clean tree; 38 new paths absent; 1 files to replace and 0 to delete at their base version. Nothing was changed.
Read-only: no project code imported, nothing run, nothing changed.
```

### Step 6

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T013 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\p\WF1B_Install_v2\repo_overlay" --replace .gitignore
```

Output (exit code 0):

```text
OVERLAY PASS: 39 files copied into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r (38 new, 1 replaced)
```

### Step 7

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\p\WF1B_Install_v2\VERIFY_WF1B_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r" --phase post
```

Output (exit code 0):

```text
HEAD: bde56b6780321070c2d60e3d618f66068d778d35 (descends from base 0c8799d)
17 guarded files unchanged in Git HEAD
POST PASS: exactly the 38 expected new paths, 1 modified files and 0 staged deletions, all with the expected bytes.
Read-only: no project code imported, nothing run, nothing changed.
```

### Step 8

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r"
```

Output (exit code 0):

```text
python: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe 3.15.2
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Lib\site-packages
checked .pth files in E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv
ok   _common.contract_vocab               E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\contract_vocab.py
ok   _common.contract_records             E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\contract_records.py
ok   _common.contract_task                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\contract_task.py
ok   _common.contract_forecast            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\contract_forecast.py
ok   _common.contract_receipts            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\contract_receipts.py
ok   _common.contract_registry            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\contract_registry.py
ok   _common.canonical_encoding           E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\canonical_encoding.py
ok   _common.game_profiles                E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\game_profiles.py
ok   _common.game_draws_reader            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\game_draws_reader.py
ok   E_001.multigame_e1                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\E_001\multigame_e1.py
ok   e2r_fixtures                         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\tests\e2r_fixtures.py
ok   _common.contract_dispatch            E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\contract_dispatch.py
ok   _common.contract_publication         E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\contract_publication.py
ok   _common.contract_runner              E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\contract_runner.py
ok   contract_adapters.e_001              E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\contract_adapters\e_001.py
ok   e2r_code2_fixtures                   E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\tests\e2r_code2_fixtures.py
contract_data: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r\src\methods\_common\contract_data
contract_data files: 364, with CRLF line endings: 364
registry loaded: 82 declarations, 202 registry chains
ORIGIN PASS: every checked module and the contract data come from the task clone
```

### Step 9

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import pathlib; r = pathlib.Path(r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r'); print(sorted(p.name for p in r.glob('Run_Method_Rankings.*')))"
```

Output (exit code 0):

```text
['Run_Method_Rankings.bat']
```

That is the one name the task file gives as expected.

### Step 10

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import pathlib; r = pathlib.Path(r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r') / 'src' / 'evaluation'; print(sorted(p.name for p in r.glob('*.py')))"
```

Output (exit code 0):

```text
['Method_Rankings_Report.py', '__init__.py', 'collect.py', 'divisions.py', 'measures.py', 'n1.py', 'n1_generator.py', 'numerics.py', 'outcome_reader.py', 'report.py', 'report_writer.py', 'seed_policies.py']
```

### Step 11 - STOP

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\p\WF1B_Install_v2\RUN_WF1B_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013\r"
```

Output (exit code 1), copied as printed:

```text
environment: Windows 11 Python 3.15.2 E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
tests.test_multigame_reader_contracts                ran  10 (expected 10)  skipped 1  OK (skipped=1)  (0.7 s)
    skip: test_reject_symlinks_and_hardlinks_and_dateload_mismatch (tests.test_multigame_reader_contracts.V011ReaderTests.test_reject_symlinks_and_hardlinks_and_dateload_mismatch) (link='symlink') ... skipped '
tests.test_multigame_static_and_timing               ran   6 (expected  6)  skipped 0  OK  (0.6 s)
tests.test_multigame_launch_and_manifest             ran  11 (expected 11)  skipped 0  OK  (3.6 s)
tests.test_multigame_exit_receipt                    ran  18 (expected 18)  skipped 1  OK (skipped=1)  (3.5 s)
    skip: test_symlink_receipts_directory_is_refused (tests.test_multigame_exit_receipt.ReceiptTests.test_symlink_receipts_directory_is_refused) ... skipped 'platform disallows symlinks'
tests.test_multigame_science_allowlist               ran   6 (expected  6)  skipped 0  OK  (2.6 s)
tests.test_multigame_console_and_synthetic_scorer    ran   7 (expected  7)  skipped 0  OK  (1.1 s)
tests.test_t05_hardening                             ran   2 (expected  2)  skipped 0  OK  (3.6 s)
tests.test_e1_align                                  ran   5 (expected  5)  skipped 0  OK  (0.4 s)
tests.test_e1_standalone                             ran  13 (expected 13)  skipped 0  OK  (2.1 s)
tests.test_multigame_windows_lifecycle_review        ran   6 (expected  6)  skipped 0  OK  (1.4 s)
tests.test_e2r_contract                              ran  53 (expected 53)  skipped 0  OK  (4.9 s)
tests.test_e2r_prefix                                ran   1 (expected  1)  skipped 0  OK  (3.5 s)
tests.test_e2r_dispatch                              ran  18 (expected 18)  skipped 0  OK  (23.8 s)
tests.test_e2r_runner                                ran  34 (expected 34)  skipped 1  OK (skipped=1)  (19.7 s)
    skip: test_dangling_symlink_target_is_refused (tests.test_e2r_runner.AtomicCreateOnly.test_dangling_symlink_target_is_refused) ... skipped 'platform disallows symlinks'
tests.test_e6_beta_bernoulli                         ran  20 (expected 20)  skipped 0  OK  (15.0 s)
tests.test_polynomial_fits                           ran  19 (expected 19)  skipped 0  OK  (1.0 s)
tests.test_e3_e4_polynomial                          ran  13 (expected 13)  skipped 0  OK  (45.2 s)
tests.test_occurrence_counts                         ran   8 (expected  8)  skipped 0  OK  (0.4 s)
tests.test_wave1_frequency                           ran  18 (expected 18)  skipped 0  OK  (32.9 s)
tests.test_recurrence_gaps                           ran  12 (expected 12)  skipped 0  OK  (0.8 s)
tests.test_wave2_recurrence                          ran  19 (expected 19)  skipped 0  OK  (51.1 s)
tests.test_rel1_release                              ran   5 (expected  5)  skipped 0  OK  (31.4 s)
tests.test_wf1a_walk_forward                         ran  22 (expected 22)  skipped 0  OK  (56.6 s)
tests.test_code3_retirement                          ran  11 (expected 11)  skipped 0  OK  (2.6 s)
tests.test_e1r2_revision2                            ran  13 (expected 13)  skipped 0  OK  (25.5 s)
tests.test_wf1b_numerics                             ran  21 (expected 21)  skipped 0  OK  (2.4 s)
tests.test_wf1b_n1_generator                         ran   8 (expected  8)  skipped 0  OK  (0.7 s)
tests.test_wf1b_divisions                            ran  17 (expected 17)  skipped 0  OK  (0.2 s)
tests.test_wf1b_measures                             ran  33 (expected 33)  skipped 0  OK  (7.5 s)
tests.test_wf1b_outcome_reader                       ran   5 (expected  5)  skipped 0  FAILED (errors=1)  (0.7 s)
tests.test_wf1b_report                               ran  10 (expected 10)  skipped 0  OK  (148.8 s)
tests.test_wf1b_static                               ran   4 (expected  4)  skipped 0  OK  (0.3 s)
tests.test_wf1b_crossplatform                        ran   1 (expected  1)  skipped 0  OK  (21.8 s)
tests.test_wf1b_seed_policy                          ran  11 (expected 11)  skipped 0  OK  (0.2 s)
tests.test_wf1b_n1_replay                            ran   3 (expected  3)  skipped 0  OK  (11.1 s)
total ran 463 (expected 463); skips 3
SUITE STOP:
  tests.test_wf1b_outcome_reader: exit 1, ran 5 expected 5, "FAILED (errors=1)"
```

The local times printed immediately before and after this command were `2026-11-01T07:33:33+1030 (CAST)` and `2026-11-01T07:42:21+1030 (CAST)`: a wall-clock time of 8 minutes 48 seconds.

The task file's expected line is `SUITE PASS: all 463 tests ran and passed`. The runner printed `SUITE STOP` and exited 1, so the task stopped here and went to step 17. The suite was not rerun, and no test or module was run on its own.

### Steps 12 to 16

Not run, because of the STOP at step 11.

## Clean-up

### Step 17

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T013
```

Output (exit code 0):

```text
REMOVE PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T013 deleted
```

The local time printed immediately before this command was `2026-11-01T07:42:32+1030 (CAST)`.

### Step 18 - the main repository after the clean-up

Command:

```text
git status --short
```

Output (exit code 0): no output (empty). This is the same as in step 2.

Command:

```text
git rev-parse HEAD
```

Output (exit code 0):

```text
bde56b6780321070c2d60e3d618f66068d778d35
```

## Deviations

- No step was repeated, retried or rerun, and no step was skipped before the STOP. Steps 1 to 11 and 17 were run with the command text from the task file unchanged, from the MAIN folder.
- The shell used for every step was Git Bash, not CMD or PowerShell.
- Step 11's start and end times were printed by two `date` commands in the same shell line as the task file's command, before and after it, so that the wall-clock time asked for in step 18 could be reported. The task file's command itself was unchanged, and nothing was redirected to a file.
- This report file could not be written through the shell: the attempt (a single shell command whose text contained the whole report) was refused by the permission layer, because the report's own text contains the wrapper's file name, which the deny entry `Bash(*.bat*)` in `.claude\settings.json` matches. The file was therefore written with Claude Code's own file-writing tool instead, to the path the task file gives, inside `CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\`. No other file was written.

## Observations

- Step 9, one of the two commands T013 changed from T012, ran and was not refused by the permission layer; it printed exactly one name. Step 12, the other changed command, was not reached.
- Step 11's own totals line says the expected number of tests ran: `total ran 463 (expected 463); skips 3`. The three skips are the symlink skips, in `tests.test_multigame_reader_contracts`, `tests.test_multigame_exit_receipt` and `tests.test_e2r_runner`.
- The module that failed, `tests.test_wf1b_outcome_reader`, reported `errors=1` rather than a failed assertion, and the runner recorded that all 5 of its expected tests ran. The runner printed no traceback and no test name for that error, so this report has none.
- The line for `tests.test_wf1b_crossplatform` printed `OK`.
- The first skip line printed by the runner ends mid-text, after `... skipped '`, with no closing quote and no reason; it is copied above exactly as printed. The other two skip lines printed a complete reason.
- Step 4 printed `UNZIP PASS: 42 files extracted`, while the task file's expected line is `UNZIP PASS: ... files extracted ...` with the count left open. The ZIP SHA-256 matched the value the task file gives.
- Steps 5 and 7 both printed two extra lines before the PASS line (`HEAD: ... (descends from base 0c8799d)` and `17 guarded files unchanged in Git HEAD`) and one after (`Read-only: no project code imported, nothing run, nothing changed.`). The task file quotes only the PASS lines.
- Step 8 printed its two `checked .pth files in ...` lines in the opposite order to the same step in REPORT_T012; every module line was `ok`.
- The clone's HEAD and the main repository's HEAD were both bde56b6780321070c2d60e3d618f66068d778d35, which the verifier reported as descending from the package's base `0c8799d`.
- No other warnings or errors were printed by any step that ran.
