# REPORT_T025 - Windows rehearsal of build step 2 (package STEP2_Research_Engine_v1r2): the install in a task clone, then the first research fill in a scratch tree on D:

RESULT: STOP at step 20 (the scratch tree's create_venv.bat refused: a virtual environment was already active in the runner's shell). Steps 1 to 19 passed; steps 21 to 29 were not run; the clean-up (step 30) passed.

- Task file: inbox/TASK_T025.md at main-repository commit 5ed656a6a3cd2c8d1654769580768ce6166913c0
- Run by: Claude Code (local runner), 23 November 2026, from 22:17 +1030
- Owner options used: none (the task file offers none; E2R-T12 approved by the giving of the task)
- Machine: Windows-11-10.0.26300-SP0; Python 3.15.2 at E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
- Rulebook: v0.7 (RAT-44). Section 2A applies to steps 17 to 29 only, in D:\DELETE_ME\a_p_r_i_r\T025\

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | Python | 0 | venv Python 3.15.2, Windows-11-10.0.26300-SP0 |
| 2 | The main repository's state (read-only) | 0, 0, 0 | clean; HEAD 5ed656a6a3cd2c8d1654769580768ce6166913c0 |
| 3 | The scratch folder check | 0 | SCRATCH CHECK PASS |
| 4 | Make the task clone | 0 | MAKE PASS |
| 5 | Check and extract the reviewed package | 0 | UNZIP PASS: 41 files extracted |
| 6 | The clone's evidence folder | 0 | no output |
| 7 | (long) The suite as it is today: the baseline | 0 | DONE: 45 modules, 571 tests ran; RUNNER EXIT CODE 0; FAILED only on the two known modules |
| 8 | The verifier, before the copy | 0 | PRE PASS |
| 9 | Copy the package 35 files into the clone | 0 | OVERLAY PASS: 35 files (33 new, 2 replaced) |
| 10 | The verifier, after the copy | 0 | POST PASS |
| 11 | (long) The suite again | 0 | DONE: 52 modules, 762 tests ran; RUNNER EXIT CODE 0; the seven research modules OK |
| 12 | The comparison of the two suite runs | tool 1; greps 0 and 0 | tests in both runs: 571; with the same result: 571; three FAILS IN BOTH RUNS; 198 new tests |
| 13 | Whether the link tests ran or were skipped | 0 | both link tests skipped: this account cannot create symbolic links |
| 14 | Stage the package files in the clone | 0, 0 | GUARD PASS; 33 lines A, 2 lines M, nothing else |
| 15 | Commit in the clone | 0 | GUARD PASS (after); git commit exit code 0 |
| 16 | The verifier, after the commit | 0 | COMMITTED PASS: 33 added, 2 modified, 0 deleted |
| 17 | The scratch folders | 0 | no output |
| 18 | (long) Copy the clone into the scratch tree | 0 | TREE COPY DONE |
| 19 | The scratch tree settings file | 0 | SETTINGS COPIED |
| 20 | (long) Build the scratch tree own Python environment | 3 | STOP: [VENV] ERROR: A virtual environment is already active |
| 21 to 29 | not run (the task stopped at step 20) | - | - |
| 30 | Clean-up: remove the task clone | 0, 0 | TASK FOLDER PRESENT; REMOVE PASS |


## Outputs

### Step 1
Command:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.platform())"
```
Output:
```
E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
3.15.2 (tags/v3.15.2:5e58eaa, Oct 25 2026, 17:27:03) [MSC v.1951 64 bit (AMD64)]
Windows-11-10.0.26300-SP0
```
Exit code: 0

### Step 2
Commands:
```
git status --short
git rev-parse HEAD
git log -1 --format=%s
```
Output:
```
(git status --short printed nothing)
5ed656a6a3cd2c8d1654769580768ce6166913c0
exchange: EX_292 received - the reviewer's PASS for the text of TASK_T025 r1; decision log entry 201
```
Exit codes: 0, 0, 0

### Step 3
Command:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import os, sys; p = r'D:\DELETE_ME'; t = r'D:\DELETE_ME\a_p_r_i_r\T025'; j = getattr(os.path, 'isjunction', lambda x: False); ok = os.path.isdir(p) and not os.path.islink(p) and not j(p) and os.path.normcase(os.path.realpath(p)) == os.path.normcase(p) and not os.path.lexists(t); print('real path:', os.path.realpath(p)); print('task folder there already:', os.path.lexists(t)); print('SCRATCH CHECK PASS' if ok else 'SCRATCH CHECK STOP'); sys.exit(0 if ok else 1)"
```
Output:
```
real path: D:\DELETE_ME
task folder there already: False
SCRATCH CHECK PASS
```
Exit code: 0

### Step 4
Command:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T025
```
Output:
```
cloning from https://github.com/hydra3333/analysing_perceived_randomness_in_reality
GUARD PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\r is a task clone with no remote and a refusing pre-push hook
git remote -v: ''
clone HEAD: 5ed656a6a3cd2c8d1654769580768ce6166913c0
main repository HEAD: 5ed656a6a3cd2c8d1654769580768ce6166913c0
core.autocrlf in the clone: true
MAKE PASS
```
Exit code: 0

### Step 5
Command:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T025 --zip exchange/CLAUDE_WEB_TOOLS/step2/package_v1r2/STEP2_Research_Engine_v1r2.zip --sha256 a6c1842c3b5a67f2fcf4d7dc9aa386638582bbef15e1ee4fe2bcde602cb673ac
```
Output:
```
ZIP SHA-256: a6c1842c3b5a67f2fcf4d7dc9aa386638582bbef15e1ee4fe2bcde602cb673ac
UNZIP PASS: 41 files extracted into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\p
```
Exit code: 0

### Step 6
Command:
```
mkdir -p "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e"
```
Output: none
Exit code: 0

### Step 7 (long)
Command:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\p\STEP2_Research_Engine_v1r2\tools\run_suite.py" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\r" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\e\suite_before" > "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e/suite_before_output.txt" 2>&1; echo "RUNNER EXIT CODE $?" >> "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e/suite_before_output.txt"
```
Wall clock: 22:17:47 to 22:42:48 +1030 (25 min 1 s).

The whole file `scratch/T025/e/suite_before_output.txt`:
```
test_code3_retirement	exit=0	ran=12	OK
test_e1_align	exit=0	ran=5	OK
test_e1_standalone	exit=0	ran=13	OK
test_e1r2_revision2	exit=0	ran=13	OK
test_e1r3_revision3	exit=0	ran=8	OK
test_e2r_contract	exit=0	ran=53	OK
test_e2r_dispatch	exit=0	ran=18	OK
test_e2r_prefix	exit=0	ran=1	OK
test_e2r_runner	exit=0	ran=34	OK (skipped=1)
test_e3_e4_polynomial	exit=0	ran=13	OK
test_e6_beta_bernoulli	exit=0	ran=20	OK
test_mhupa_gates	exit=0	ran=12	OK
test_mhupa_install_records	exit=0	ran=9	OK
test_mhupa_launchers	exit=1	ran=10	FAILED (failures=1)
test_mhupa_master_versions	exit=0	ran=15	OK
test_mhupa_method_mode_h_cli	exit=0	ran=2	OK
test_mhupa_mode_h	exit=0	ran=20	OK
test_mhupa_process_check	exit=0	ran=8	OK
test_mhupa_updater_v0_2	exit=0	ran=15	OK
test_multigame_console_and_synthetic_scorer	exit=0	ran=7	OK
test_multigame_exit_receipt	exit=0	ran=18	OK (skipped=1)
test_multigame_launch_and_manifest	exit=0	ran=11	OK
test_multigame_reader_contracts	exit=1	ran=10	FAILED (failures=7, skipped=1)
test_multigame_science_allowlist	exit=0	ran=6	OK
test_multigame_static_and_timing	exit=0	ran=6	OK
test_multigame_windows_lifecycle_review	exit=0	ran=6	OK
test_occurrence_counts	exit=0	ran=8	OK
test_perf1_numerics	exit=0	ran=7	OK
test_polynomial_fits	exit=0	ran=19	OK
test_recurrence_gaps	exit=0	ran=12	OK
test_rel1_release	exit=0	ran=5	OK
test_t05_hardening	exit=0	ran=2	OK
test_wave1_frequency	exit=0	ran=18	OK
test_wave2_recurrence	exit=0	ran=19	OK
test_wf1a_walk_forward	exit=0	ran=22	OK
test_wf1b_crossplatform	exit=0	ran=1	OK
test_wf1b_divisions	exit=0	ran=17	OK
test_wf1b_measures	exit=0	ran=33	OK
test_wf1b_n1_generator	exit=0	ran=8	OK
test_wf1b_n1_replay	exit=0	ran=3	OK
test_wf1b_numerics	exit=0	ran=21	OK
test_wf1b_outcome_reader	exit=0	ran=6	OK (skipped=1)
test_wf1b_report	exit=0	ran=10	OK
test_wf1b_seed_policy	exit=0	ran=11	OK
test_wf1b_static	exit=0	ran=4	OK
DONE: 45 modules, 571 tests ran
RUNNER EXIT CODE 0
```
Exit code (the file's last line): 0

### Step 8
Command:
```
"...\.venv\Scripts\python.exe" "...\scratch\T025\p\STEP2_Research_Engine_v1r2\VERIFY_STEP2_INSTALL.py" --repo "...\scratch\T025\r" --phase pre
```
Output:
```
HEAD: 5ed656a6a3cd2c8d1654769580768ce6166913c0 (descends from base 469f088)
28 guarded files unchanged in Git HEAD
PRE PASS: clean tree; 33 new paths absent; 2 files to replace and 0 to delete at their base version. Nothing was changed.
Read-only: no project code imported, nothing run, nothing changed.
```
Exit code: 0

### Step 9
Command:
```
"...\.venv\Scripts\python.exe" -I "...\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T025 --src "...\scratch\T025\p\STEP2_Research_Engine_v1r2\repo_overlay" --plan CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T025_overlay_plan.txt
```
Output:
```
plan CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T025_overlay_plan.txt: 2 REPLACE, 0 REMOVE; SHA-256 a8ab9f4153bd9192040878b9158c06502909350d7f7292e9e828a737bc3c3943
OVERLAY PASS: 35 files copied into E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\r (33 new, 2 replaced); 0 tracked file(s) removed with git rm
```
Exit code: 0

### Step 10
Command:
```
"...\.venv\Scripts\python.exe" "...\scratch\T025\p\STEP2_Research_Engine_v1r2\VERIFY_STEP2_INSTALL.py" --repo "...\scratch\T025\r" --phase post
```
Output:
```
HEAD: 5ed656a6a3cd2c8d1654769580768ce6166913c0 (descends from base 469f088)
28 guarded files unchanged in Git HEAD
POST PASS: exactly the 33 expected new paths, 2 modified files and 0 staged deletions, all with the expected bytes.
Read-only: no project code imported, nothing run, nothing changed.
```
Exit code: 0

### Step 11 (long)
Command:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -B "...\scratch\T025\p\STEP2_Research_Engine_v1r2\tools\run_suite.py" "...\scratch\T025\r" "...\scratch\T025\e\suite_after" > ".../scratch/T025/e/suite_after_output.txt" 2>&1; echo "RUNNER EXIT CODE $?" >> ".../scratch/T025/e/suite_after_output.txt"
```
Wall clock: 22:43:37 to 23:12:18 +1030 (28 min 41 s).

The whole file `scratch/T025/e/suite_after_output.txt`:
```
test_code3_retirement	exit=0	ran=12	OK
test_e1_align	exit=0	ran=5	OK
test_e1_standalone	exit=0	ran=13	OK
test_e1r2_revision2	exit=0	ran=13	OK
test_e1r3_revision3	exit=0	ran=8	OK
test_e2r_contract	exit=0	ran=53	OK
test_e2r_dispatch	exit=0	ran=18	OK
test_e2r_prefix	exit=0	ran=1	OK
test_e2r_runner	exit=0	ran=34	OK (skipped=1)
test_e3_e4_polynomial	exit=0	ran=13	OK
test_e6_beta_bernoulli	exit=0	ran=20	OK
test_mhupa_gates	exit=0	ran=12	OK
test_mhupa_install_records	exit=0	ran=9	OK
test_mhupa_launchers	exit=1	ran=10	FAILED (failures=1)
test_mhupa_master_versions	exit=0	ran=15	OK
test_mhupa_method_mode_h_cli	exit=0	ran=2	OK
test_mhupa_mode_h	exit=0	ran=20	OK
test_mhupa_process_check	exit=0	ran=8	OK
test_mhupa_updater_v0_2	exit=0	ran=15	OK
test_multigame_console_and_synthetic_scorer	exit=0	ran=7	OK
test_multigame_exit_receipt	exit=0	ran=18	OK (skipped=1)
test_multigame_launch_and_manifest	exit=0	ran=11	OK
test_multigame_reader_contracts	exit=1	ran=10	FAILED (failures=7, skipped=1)
test_multigame_science_allowlist	exit=0	ran=6	OK
test_multigame_static_and_timing	exit=0	ran=6	OK
test_multigame_windows_lifecycle_review	exit=0	ran=6	OK
test_occurrence_counts	exit=0	ran=8	OK
test_perf1_numerics	exit=0	ran=7	OK
test_polynomial_fits	exit=0	ran=19	OK
test_recurrence_gaps	exit=0	ran=12	OK
test_rel1_release	exit=0	ran=5	OK
test_research_forecasts	exit=0	ran=26	OK
test_research_identity	exit=0	ran=25	OK (skipped=1)
test_research_job	exit=0	ran=48	OK (skipped=1)
test_research_manifest	exit=0	ran=9	OK
test_research_ov1_and_checks	exit=0	ran=34	OK
test_research_ov1_numeric	exit=0	ran=21	OK
test_research_records	exit=0	ran=28	OK
test_t05_hardening	exit=0	ran=2	OK
test_wave1_frequency	exit=0	ran=18	OK
test_wave2_recurrence	exit=0	ran=19	OK
test_wf1a_walk_forward	exit=0	ran=22	OK
test_wf1b_crossplatform	exit=0	ran=1	OK
test_wf1b_divisions	exit=0	ran=17	OK
test_wf1b_measures	exit=0	ran=33	OK
test_wf1b_n1_generator	exit=0	ran=8	OK
test_wf1b_n1_replay	exit=0	ran=3	OK
test_wf1b_numerics	exit=0	ran=21	OK
test_wf1b_outcome_reader	exit=0	ran=6	OK (skipped=1)
test_wf1b_report	exit=0	ran=10	OK
test_wf1b_seed_policy	exit=0	ran=11	OK
test_wf1b_static	exit=0	ran=4	OK
DONE: 52 modules, 762 tests ran
RUNNER EXIT CODE 0
```
Exit code (the file's last line): 0

### Step 12
Commands: the comparison tool into `scratch/T025/e/comparison.txt`, then the two `grep` commands of the task file.

Output of the first grep (every line that is not about a new test):
```
before: 45 modules; unittest ran 571 tests; identified here: 571
after: 52 modules; unittest ran 762 tests; identified here: 762
tests in both runs: 571; with the same result: 571
FAILS IN BOTH RUNS (1 failure(s); FAILURE LINES DIFFER, compare by eye): test_mhupa_launchers.LauncherStatics.test_gitignore_lines
    before: ["AssertionError: 'results/real/holdout/scores/' not found in {'', '#   can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore', 'results/real/holdout/contract_r"]
    after:  ["AssertionError: 'results/real/holdout/scores/' not found in {'', '.env', '.pypirc', 'build/', '.coverage.*', '# poetry.toml', '#   commonly ignored for libraries.', '*.mhtml', '# PEP 582; used by e.g."]
FAILS IN BOTH RUNS (2 failure(s), the same failure lines): test_multigame_reader_contracts.V011ReaderTests.test_master_source_and_ledger_file_hashes
FAILS IN BOTH RUNS (5 failure(s), the same failure lines): test_multigame_reader_contracts.V011ReaderTests.test_only_legacy_e1_allowed_at_boundary
RESULT: DIFFERENCES FOUND - each needs an explanation
COMPARE EXIT CODE 1
```
Exit code of the first grep: 0

Output of the second grep (count of new tests):
```
198
```
Exit code of the second grep: 0

The comparison tool's own exit code, from the file's last line: 1 (as the task file expects).

### Step 13
Command:
```
grep -n -i "skip" ".../scratch/T025/e/suite_after/test_research_job.txt" ".../scratch/T025/e/suite_after/test_research_identity.txt"
```
Output:
```
test_research_job.txt:47:test_the_writer_refuses_a_staged_name_that_is_a_link_to_a_file_elsewhere (test_research_job.TheStagingFolderIsTheTreesOwn.test_the_writer_refuses_a_staged_name_that_is_a_link_to_a_file_elsewhere) ... skipped 'this account cannot make a symbolic link to a file'
test_research_job.txt:53:OK (skipped=1)
test_research_identity.txt:8:test_a_path_through_a_link_refuses (test_research_identity.SettingsFile.test_a_path_through_a_link_refuses) ... skipped 'this account cannot create a symbolic link'
test_research_identity.txt:30:OK (skipped=1)
```
Exit code: 0. (The full paths of the two files are as in the command; the file names are shortened here only in this block.) Both link tests were skipped: this account cannot create symbolic links.

### Step 14
First command: `cc_clone.py git --task T025 -- add .gitignore deploy src tests Run_Research.bat Withdraw_Variant.bat ENVIRONMENT.example.ini`
Output: 33 Git warnings "LF will be replaced by CRLF the next time Git touches it" (one per text file added or modified), then:
```
GUARD PASS (before)
GUARD PASS (after); git add exit code 0
```
Exit code: 0

Second command: `cc_clone.py git --task T025 -- status --short`
Output:
```
M  .gitignore
A  ENVIRONMENT.example.ini
A  Run_Research.bat
A  Withdraw_Variant.bat
A  deploy/INFRA_MANIFEST.ini
A  src/research/__init__.py
A  src/research/code_identity.py
A  src/research/derived_check.py
A  src/research/forecast_engine.py
A  src/research/game_state.py
A  src/research/job_lock.py
A  src/research/method_api.py
A  src/research/ov1_ledger.py
A  src/research/ov1_numeric.py
A  src/research/reader.py
A  src/research/readout.py
A  src/research/reports.py
A  src/research/research_job.py
A  src/research/results_step.py
A  src/research/scoring.py
A  src/research/settings.py
A  src/research/status_file.py
A  src/research/variant_folders.py
A  src/research/variant_lists.py
A  src/research/withdraw.py
A  src/research_command.py
A  tests/research_fixtures.py
M  tests/test_mhupa_master_versions.py
A  tests/test_research_forecasts.py
A  tests/test_research_identity.py
A  tests/test_research_job.py
A  tests/test_research_manifest.py
A  tests/test_research_ov1_and_checks.py
A  tests/test_research_ov1_numeric.py
A  tests/test_research_records.py
GUARD PASS (before)
GUARD PASS (after); git status exit code 0
```
Exit code: 0. Counted: 33 lines beginning A, 2 beginning M, nothing else.

### Step 15
Command: `cc_clone.py git --task T025 -- commit -q -m "T025 rehearsal: BUILD STEP 2 in a task clone"`
Output:
```
GUARD PASS (before)
GUARD PASS (after); git commit exit code 0
```
Exit code: 0

### Step 16
Command: the verifier with `--phase committed`
Output:
```
HEAD: a5e8a578fe17523e3d138448237bf65cdf3a3b7b (descends from base 469f088)
28 guarded files unchanged in Git HEAD
COMMITTED PASS: the last commit (a5e8a57) added exactly 33 files, modified 2 and deleted 0; all Git blobs match.
Read-only: no project code imported, nothing run, nothing changed.
```
Exit code: 0

### Step 17
Command:
```
mkdir -p "D:/DELETE_ME/a_p_r_i_r/T025/evidence"
```
Output: none. Exit code: 0

### Step 18 (long)
Command: the `shutil.copytree` command of the task file (the clone into `D:\DELETE_ME\a_p_r_i_r\T025\tree`, ignoring `.git`).

The whole file `D:\DELETE_ME\a_p_r_i_r\T025\evidence\tree_copy.txt`:
```
TREE COPY DONE
COPY EXIT CODE 0
```
Exit code (the file's last line): 0

### Step 19
Command: the `shutil.copyfile` command of the task file (TASK_T025_ENVIRONMENT.ini into the scratch tree as ENVIRONMENT.ini).
Output:
```
SETTINGS COPIED
```
Exit code: 0

### Step 20 (long) - STOP
Command:
```
"D:/DELETE_ME/a_p_r_i_r/T025/tree/create_venv.bat" > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/venv_create.txt" 2>&1; echo "VENV EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/venv_create.txt"
```
Wall clock: 23:14:16 to 23:14:22 +1030 (6 s).

The whole file `D:\DELETE_ME\a_p_r_i_r\T025\evidence\venv_create.txt`:
```
[VENV] ERROR: A virtual environment is already active: "e:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv" 
[VENV] Deactivate it before creating a new project venv. 
VENV EXIT CODE 3
```
Exit code (the file's last line): 3

Expected by the task file: a line `[VENV] SUCCESS: "D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv"`, no line with `ERROR`, and as the last line `VENV EXIT CODE 0`. The file holds an `ERROR` line, no `SUCCESS` line, and `VENV EXIT CODE 3`. **STOP at step 20** (rulebook rule 10). The script was not run again, nothing was deactivated, changed or undone, and no other way of making the environment was tried.

Steps 21 to 29 were not run.

### Step 30 (clean-up)
First command:
```
"...\.venv\Scripts\python.exe" -I -c "import os; print(... CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025 ...)"
```
Output:
```
TASK FOLDER PRESENT
```
Exit code: 0

Second command:
```
"...\.venv\Scripts\python.exe" -I "...\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T025
```
Output:
```
REMOVE PASS: E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025 deleted
```
Exit code: 0

## Clean-up

The task clone, the extracted package and the clone's evidence folder were removed with `cc_clone.py remove --task T025` (`REMOVE PASS`).

Folders this task created under `D:\DELETE_ME\`, **all left in place, none removed** (the task file: the scratch folder is not removed by this task; rulebook section 2A item 9 on a STOP):

- `D:\DELETE_ME\a_p_r_i_r\T025`
- `D:\DELETE_ME\a_p_r_i_r\T025\tree`
- `D:\DELETE_ME\a_p_r_i_r\T025\evidence` (holding `tree_copy.txt` and `venv_create.txt`)

Also recorded: `D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv` does not exist (step 20 created no environment before it refused). The scratch tree holds the copied clone files and the `ENVIRONMENT.ini` of step 19.

The main repository's `git status --short` after step 30:

```
?? CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T025.md
```

In step 2 it printed nothing. The one difference is this report file, which is untracked until step 32 commits it. Nothing else in the main repository changed, and the main `.venv` was not touched.

## Wall-clock times

Step 31 asks for the wall-clock time of steps 7, 11, 21, 23, 24 and 27.

| Step | Started | Finished | Duration |
|---|---|---|---|
| 7 | 22:17:47 +1030 | 22:42:48 +1030 | 25 min 1 s |
| 11 | 22:43:37 +1030 | 23:12:18 +1030 | 28 min 41 s |
| 20 | 23:14:16 +1030 | 23:14:22 +1030 | 6 s (the STOP) |
| 21, 23, 24, 27 | not run | not run | not run |

All on 23 November 2026.

## Deviations

- Every command under test was run exactly as the task file writes it. For recording, some step lines were preceded in the same Git Bash line by `cd` to MAIN (the task file requires each command to run from MAIN) and, for the long steps, by a `date` stamp; and for the steps that the task file does not itself give an `echo ... EXIT CODE $?` for, that `echo` was appended so the step's own exit code is recorded. In every case the recorded exit code is the program's own `$?` taken immediately after it, and no command under test was piped into another program.
- The long steps (7, 11, 18, 20) were each run as one background command in one shell, as the task file's Recording section requires, and each exit status in this report is the one that same shell wrote on the last line of the step's own file.
- No line had to be withheld: no output of this task showed a draw outcome or a path under `C:\Users\`.
- While this report was being written, one shell line that appended text to it was mis-quoted and wrote a mangled paragraph and lost three Deviations bullets into the report file. The report file was repaired here (truncated at that paragraph and rewritten from it). No command of the task was affected, nothing was re-run, and no other file was touched.
- Steps 21 to 29 were not run because of the STOP at step 20. Nothing was retried, repaired, reordered or undone.

## Observations

Plain facts that may matter to the Claude web chat:

1. The Git Bash shell this runner works in had the environment variable `VIRTUAL_ENV` already set to `e:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv` when the task began. It was not set by this task, and nothing was done about it. The scratch tree's `create_venv.bat` checks for an active virtual environment and refuses while one is set, which is the STOP at step 20. (The lower-case drive letter `e:` is as the script printed it.)
2. Steps 1 to 19 printed exactly what the task file expects, including every count: 41 files extracted; 35 copied (33 new, 2 replaced); 45 modules and 571 tests before; 52 modules and 762 tests after; 571 tests in both runs with the same result; 198 new tests; 33 added and 2 modified files in the clone's commit.
3. The three failures the task file names as failing before the task were the only failures in both suite runs, and the comparison's `FAILURE LINES DIFFER` entry for `test_gitignore_lines` appeared, as the task file foresaw.
4. Two tests were skipped in the new modules because this Windows account cannot create symbolic links: `test_research_job.TheStagingFolderIsTheTreesOwn.test_the_writer_refuses_a_staged_name_that_is_a_link_to_a_file_elsewhere` and `test_research_identity.SettingsFile.test_a_path_through_a_link_refuses`.
5. Git printed 33 warnings "LF will be replaced by CRLF the next time Git touches it" when the package's files were staged in the clone (`core.autocrlf` is `true` there).
