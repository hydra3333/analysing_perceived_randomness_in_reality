# TASK_T025 - Windows rehearsal of build step 2 (package STEP2_Research_Engine_v1r2): the install in a task clone, then the first research fill in a scratch tree on D:

**Task ID:** T025. **Date:** 23 November 2026. **Author:** the Claude web chat. Rulebook v0.7 (RAT-44). **Section 2A applies to steps 17 to 29, and only there, in the folder `D:\DELETE_ME\a_p_r_i_r\T025\`.**

**Purpose.** Build step 2 (the new research engine) has the reviewer's PASS (EX_290) and has never run on Windows. Before the project owner installs it in the real tree, this task does what his install sheet does, where nothing real can be harmed: parts 1 to 4 of the sheet in a disposable task clone that cannot push (the suite before and after, the verifier, the commit), and parts 5 to 7 in a scratch tree under `D:\DELETE_ME\` with its own Python environment (the two launchers' first real use, the first fill of both games on the real results, a second job, and the comparison with the old records). **What a scratch run computes is a rehearsal, not a result of the project.**

**What it does not do.** It changes nothing in the main repository (only this task's report is committed there) and nothing in the main `.venv`. It runs no coordinator, no old launcher, no results updater, no scraper, no Mode H command, and it contacts no lottery website. It ends no process and changes no date, time or time zone. It names no real QA or PROD tree. Its only network use is the task clone (step 4) and the package downloads of the scratch tree's own two environment scripts (steps 20 and 21).

**Before the owner starts this task (the owner, not the runner):** the folder `D:\DELETE_ME` exists; `git pull --ff-only` has been done and this is a new Claude Code conversation; nothing of the project is running. The whole task takes about two hours, most of it unattended.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish by themselves) runs inside both suite runs. The project owner approves it for this run by giving this task.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| CLONE (the task clone) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\r` |
| PKG (the extracted package) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\p\STEP2_Research_Engine_v1r2` |
| EV (the clone's evidence folder) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\e` |
| SCRATCH (this task's scratch folder) | `D:\DELETE_ME\a_p_r_i_r\T025` |
| TREE (the scratch tree) | `D:\DELETE_ME\a_p_r_i_r\T025\tree` |
| SEV (the scratch evidence folder) | `D:\DELETE_ME\a_p_r_i_r\T025\evidence` |
| SPY (the scratch tree's own Python) | `D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv\Scripts\python.exe` |

Run each command in Git Bash, from MAIN, exactly as written. On anything other than the expected output and exit code: **STOP**, record the output, and go to step 30 (clean-up). Never retry, repair or reorder a step. **After a STOP, leave `D:\DELETE_ME\a_p_r_i_r\T025` exactly as it is** (rulebook section 2A item 9).

**The one exception to "a STOP is a STOP" (rulebook rule 10), for steps 7, 11 and 12 only.** Three tests fail in the repository today, before this task: `test_mhupa_launchers.LauncherStatics.test_gitignore_lines`, `test_multigame_reader_contracts.V011ReaderTests.test_master_source_and_ledger_file_hashes` and `test_multigame_reader_contracts.V011ReaderTests.test_only_legacy_e1_allowed_at_boundary`. So the word `FAILED` on the lines of the two modules `test_mhupa_launchers` and `test_multigame_reader_contracts` in steps 7 and 11, and the three entries `FAILS IN BOTH RUNS` for those three tests in step 12, are not a STOP. `FAILED` on any other module's line, any other failing test, or any line beginning `CHANGED`, `DISAPPEARED`, `MODULE CHANGED`, `MODULE DISAPPEARED`, `NOT ALL TESTS IDENTIFIED` or `NO SUMMARY`, is a STOP.

**Recording** (so that nothing improvised is needed):
- Write `CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T025.md` as you go: after each step, add its command, its exit code and its output, before starting the next step.
- Exit codes: the program's own. Do not pipe a command under test into another program. Where a step below itself pipes a recorded file through `tr`, `grep`, `tail` or `wc`, that is only to show parts of the file.
- **Steps marked (long)** can run longer than the shell's foreground limit, so each such command line carries its own recording: run that exact line as one background command, and wait until it has finished. Its output and, on the last line, its own exit status (`... EXIT CODE <n>`, written by the same shell straight after the program ends) are in the file the line names. If that last line is missing or shows another number than the step expects, that is a STOP: never infer a pass from the other lines, and never take an exit status from another shell or from the launch of the background command.
- **What goes into the report from a recorded file** is said at each step. Files under `D:\DELETE_ME\a_p_r_i_r\T025` stay there; only the text a step names is copied into the report, under a heading that names the file it came from (rulebook section 2A item 4 and section 7).
- **Never copy into the report:** a line that shows numbers drawn in any draw, or a line that shows a path under `C:\Users\`. Put `[line withheld: possible data value]` or `[line withheld: a user folder path]` in its place and say so under Deviations. The commands of this task print counts, draw numbers (which draw, not what was drawn), times and check lines.

## Steps

### Preparations

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

**3. The scratch folder is an ordinary folder on D:, and this task's folder is not there yet** (rulebook section 2A item 2; read-only).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import os, sys; p = r'D:\DELETE_ME'; t = r'D:\DELETE_ME\a_p_r_i_r\T025'; j = getattr(os.path, 'isjunction', lambda x: False); ok = os.path.isdir(p) and not os.path.islink(p) and not j(p) and os.path.normcase(os.path.realpath(p)) == os.path.normcase(p) and not os.path.lexists(t); print('real path:', os.path.realpath(p)); print('task folder there already:', os.path.lexists(t)); print('SCRATCH CHECK PASS' if ok else 'SCRATCH CHECK STOP'); sys.exit(0 if ok else 1)"
```
Expected: `real path: D:\DELETE_ME`, `task folder there already: False`, then `SCRATCH CHECK PASS`.

**4. Make the task clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T025
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines (the same commit), the `core.autocrlf` line, then `MAKE PASS`.

**5. Check and extract the reviewed package** (from the clone's own copy).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T025 --zip exchange/CLAUDE_WEB_TOOLS/step2/package_v1r2/STEP2_Research_Engine_v1r2.zip --sha256 a6c1842c3b5a67f2fcf4d7dc9aa386638582bbef15e1ee4fe2bcde602cb673ac
```
Expected: `ZIP SHA-256: a6c1842c3b5a67f2fcf4d7dc9aa386638582bbef15e1ee4fe2bcde602cb673ac`, then `UNZIP PASS: 41 files extracted into ...`.

**6. The clone's evidence folder.**
```
mkdir -p "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e"
```
Expected: no output.

### The install sheet's parts 1 to 4, in the task clone

**7. (long) The suite as it is today: the baseline** (about 25 minutes).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\p\STEP2_Research_Engine_v1r2\tools\run_suite.py" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\r" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\e\suite_before" > "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e/suite_before_output.txt" 2>&1; echo "RUNNER EXIT CODE $?" >> "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e/suite_before_output.txt"
```
Expected, in `suite_before_output.txt`: one line for each test module; `FAILED` only on the lines of `test_mhupa_launchers` and `test_multigame_reader_contracts` (the exception above); the line `DONE: 45 modules, 571 tests ran`; and as the last line `RUNNER EXIT CODE 0`. Copy the whole file into the report.

**8. The verifier, before the copy.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\p\STEP2_Research_Engine_v1r2\VERIFY_STEP2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\r" --phase pre
```
Expected: a line beginning `PRE PASS`.

**9. Copy the package's 35 files into the clone** (the plan file names the two tracked files they replace).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T025 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\p\STEP2_Research_Engine_v1r2\repo_overlay" --plan CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T025_overlay_plan.txt
```
Expected: `plan ...: 2 REPLACE, 0 REMOVE; SHA-256 ...`, then `OVERLAY PASS: 35 files copied into ... (33 new, 2 replaced); 0 tracked file(s) removed with git rm`.

**10. The verifier, after the copy.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\p\STEP2_Research_Engine_v1r2\VERIFY_STEP2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\r" --phase post
```
Expected: a line beginning `POST PASS`.

**11. (long) The suite again** (about 30 minutes).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\p\STEP2_Research_Engine_v1r2\tools\run_suite.py" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\r" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\e\suite_after" > "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e/suite_after_output.txt" 2>&1; echo "RUNNER EXIT CODE $?" >> "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e/suite_after_output.txt"
```
Expected, in `suite_after_output.txt`: `FAILED` only on the lines of `test_mhupa_launchers` and `test_multigame_reader_contracts`; the seven lines of `test_research_forecasts`, `test_research_identity`, `test_research_job`, `test_research_manifest`, `test_research_ov1_and_checks`, `test_research_ov1_numeric` and `test_research_records` each ending `OK` (or `OK (skipped=<n>)`); the line `DONE: 52 modules, 762 tests ran`; and as the last line `RUNNER EXIT CODE 0`. Copy the whole file into the report.

**12. The comparison of the two suite runs.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\p\STEP2_Research_Engine_v1r2\tools\compare_suite_reports.py" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\e\suite_before" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\e\suite_after" > "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e/comparison.txt" 2>&1; echo "COMPARE EXIT CODE $?" >> "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e/comparison.txt"
grep -v -e "^NEW: " -e "^MODULE NEW: " "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e/comparison.txt"
grep -c "NEW: " "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e/comparison.txt"
```
Expected from the first `grep` (every line that is not about a new test), exactly these: `before: 45 modules; unittest ran 571 tests; identified here: 571`; `after: 52 modules; unittest ran 762 tests; identified here: 762`; **`tests in both runs: 571; with the same result: 571`**; three entries `FAILS IN BOTH RUNS`, for the three tests named in the exception above (the entry for `test_gitignore_lines` carries the words `FAILURE LINES DIFFER` and two long lines, which is expected: that test prints a set in a different order each run); the line `RESULT: DIFFERENCES FOUND - each needs an explanation` (expected here: the differences are the new tests); and `COMPARE EXIT CODE 1`. The second `grep` prints **198**. A `tests in both runs` line whose two numbers differ, a count other than 198, or any line the exception above calls a STOP, is a STOP. Copy the output of both `grep` commands into the report.

**On a STOP at step 7, 11 or 12 only:** before the clean-up, for each module that a STOP line names, copy that module's report file (`<module>.txt` in `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\e\suite_before` or `suite_after`) into the report: test names and messages only.

**13. Whether the link tests ran or were skipped** (record the output; this step does not stop the task; `grep` exits 1 if it finds nothing).
```
grep -n -i "skip" "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e/suite_after/test_research_job.txt" "E:/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T025/e/suite_after/test_research_identity.txt"
```

**14. Stage the package's files in the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T025 -- add .gitignore deploy src tests Run_Research.bat Withdraw_Variant.bat ENVIRONMENT.example.ini
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T025 -- status --short
```
Expected from the second command, between the GUARD lines: 33 lines starting with `A` and 2 starting with `M`, and nothing else; then `GUARD PASS (after); git status exit code 0`. Git's "LF will be replaced by CRLF" warnings are harmless.

**15. Commit in the clone** (the clone cannot push).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T025 -- commit -q -m "T025 rehearsal: BUILD STEP 2 in a task clone"
```
Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git commit exit code 0`.

**16. The verifier, after the commit.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\p\STEP2_Research_Engine_v1r2\VERIFY_STEP2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\r" --phase committed
```
Expected: a line beginning `COMMITTED PASS`.

### The install sheet's parts 5 to 7, in the scratch tree on D: (rulebook section 2A)

**17. The scratch folders.**
```
mkdir -p "D:/DELETE_ME/a_p_r_i_r/T025/evidence"
```
Expected: no output.

**18. (long) Copy the clone's files, without its `.git` folder, into the scratch tree.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import shutil; shutil.copytree(r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T025\r', r'D:\DELETE_ME\a_p_r_i_r\T025\tree', ignore=shutil.ignore_patterns('.git')); print('TREE COPY DONE')" > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/tree_copy.txt" 2>&1; echo "COPY EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/tree_copy.txt"
```
Expected, in `tree_copy.txt`: `TREE COPY DONE`, then `COPY EXIT CODE 0`. Copy the whole file into the report.

**19. The scratch tree's settings file** (a copy of this task's own file, inside the scratch tree).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import shutil; shutil.copyfile(r'D:\DELETE_ME\a_p_r_i_r\T025\tree\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\TASK_T025_ENVIRONMENT.ini', r'D:\DELETE_ME\a_p_r_i_r\T025\tree\ENVIRONMENT.ini'); print('SETTINGS COPIED')"
```
Expected: `SETTINGS COPIED`.

**20. (long) Build the scratch tree's own Python environment** (its own script, by its full path).
```
"D:/DELETE_ME/a_p_r_i_r/T025/tree/create_venv.bat" > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/venv_create.txt" 2>&1; echo "VENV EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/venv_create.txt"
```
Expected, in `venv_create.txt`: a line `[VENV] SUCCESS: "D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv"`, no line with `ERROR`, and as the last line `VENV EXIT CODE 0`. Copy the whole file into the report.

**21. (long) Install the packages into the scratch tree's environment** (its own script, by its full path; it downloads packages; several minutes).
```
"D:/DELETE_ME/a_p_r_i_r/T025/tree/install_upgrade_dependencies_into_venv.bat" INSTALL > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/venv_packages.txt" 2>&1; echo "PACKAGES EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/venv_packages.txt"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/venv_packages.txt" | grep -n -e "\[DEPS\]" -e "EXIT CODE"
```
Expected from `grep`: a line `[DEPS] SUCCESS. All 39 direct requirements installed; research compatibility tests remain required.`; no line with `INCOMPLETE`, `FAILED` or `ERROR`; and the last line `PACKAGES EXIT CODE 0`. Copy the output of `grep` into the report (not the whole file).

**22. The scratch tree's Python.**
```
"D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv\Scripts\python.exe" -I -c "import sys, platform; print(sys.prefix); print(sys.version); print(platform.platform())"
```
Expected: `D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv`, a Python version, and a Windows platform line.

**23. (long) The first fill: the research job on both games** (the launcher's first real use; half an hour to an hour).
```
"D:/DELETE_ME/a_p_r_i_r/T025/tree/Run_Research.bat" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/first_job.txt" 2>&1; echo "JOB EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/first_job.txt"
```
Then show the lines that matter, the end of the file, and its length:
```
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/first_job.txt" | grep -n -e "RESEARCH JOB" -e "About to work" -e "finished" -e "written:" -e "WARNING" -e "REFUSED" -e "STOP" -e "EXIT CODE"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/first_job.txt" | tail -n 12
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/first_job.txt" | wc -l
```
Expected: a line beginning `RESEARCH JOB - START` that names the DEV tree at `D:\DELETE_ME\a_p_r_i_r\T025\tree`; for each game a line beginning `POWERBALL: finished. Results on file through draw` (and the same for `OZLOTTO`), each ending `prevailing OV-1: not started; waiting for a successful results step`; no line with `WARNING`, `REFUSED` or `STOP`; the line **`The job finished.`**; and as the last line `JOB EXIT CODE 0`. Copy the output of the three commands into the report (not the whole file).

**24. (long) The same job once more** (it has nothing new to compute; a few minutes).
```
"D:/DELETE_ME/a_p_r_i_r/T025/tree/Run_Research.bat" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/second_job.txt" 2>&1; echo "JOB EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/second_job.txt"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/second_job.txt"
```
Expected: for each game a line with `written: 0 forecasts, 0 scores, 0 prevailing lines, 0 eligibility draws, 0 report files`; no line with `WARNING`, `REFUSED` or `STOP`; the line `The job finished.`; and as the last line `JOB EXIT CODE 0`. Copy the whole output into the report.

**25. The withdrawal launcher answers** (it is given no variant, so it changes nothing; this shows only that the second launcher starts on Windows).
```
"D:/DELETE_ME/a_p_r_i_r/T025/tree/Withdraw_Variant.bat" > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/withdraw_usage.txt" 2>&1; echo "WITHDRAW EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/withdraw_usage.txt"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/withdraw_usage.txt"
```
Record the output; **this step does not stop the task** whatever it prints. Expected: a usage or refusal message of the program (not a Windows "not recognized" message), and `WITHDRAW EXIT CODE 2`. Copy the whole output into the report.

**26. (long) Copy the old system's development run folders from the main repository into the scratch tree, by reading** (rulebook section 2A item 3; nothing is written in the main repository; these folders are ignored by Git and exist only on this PC).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import os, shutil; s = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\results\real\development\contract_runs'; d = r'D:\DELETE_ME\a_p_r_i_r\T025\tree\results\real\development\contract_runs'; there = os.path.isdir(s); there and shutil.copytree(s, d); print('OLD RUN FOLDERS COPIED' if there else 'OLD RUN FOLDERS NOT PRESENT')" > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/old_runs_copy.txt" 2>&1; echo "COPY EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/old_runs_copy.txt"
```
Expected, in `old_runs_copy.txt`: `OLD RUN FOLDERS COPIED` or `OLD RUN FOLDERS NOT PRESENT` (either is accepted; step 29 says what each means), then `COPY EXIT CODE 0`. Copy the whole file into the report. **If the permission system refuses this command, do not look for another way: record the refusal, count it as `OLD RUN FOLDERS NOT PRESENT`, and go on to step 27.** That is the one case in this task where a refused command is not a STOP; the comparison then says that its second part compared nothing.

**27. (long) The early comparison with the old development records** (it reads only; a few minutes).
```
"D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv\Scripts\python.exe" -B "D:\DELETE_ME\a_p_r_i_r\T025\tree\exchange\EX_288_Claude\STEP2_Research_Engine_v1r2\tools\compare_fill_with_old_records.py" --tree "D:\DELETE_ME\a_p_r_i_r\T025\tree" > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt" 2>&1; echo "COMPARE EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt"
```

**28. The comparison's lines that are not per-variant lines, and the count of per-variant lines.**
```
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt" | grep -v -e " equal$" -e "^DIFFERENT"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt" | grep -c " equal$"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt" | grep -c "^DIFFERENT"
```
Copy the output of the three commands into the report. Lines beginning `DIFFERENT` are counted and never copied (they may show numbers drawn).

**29. What step 28 must show.**
- **If step 26 said `OLD RUN FOLDERS COPIED`:** for each game one line `part 1: old score records (TOP and WORST): N; equal in the new score lists: N; DIFFERENT: 0`, one line beginning `part 2: old development forecasts read from the run folders:` with `DIFFERENT: 0`, and one line `part 2: forecasts named by the tracked rank ledgers: N; of those not among the old forecasts compared: 0`; a line beginning **`RESULT: PASS - COMPLETE - both games; all 34800 old score records equal the new score lists`**; `COMPARE EXIT CODE 0`; the second command prints **160**; the third prints **0**.
- **If step 26 said `OLD RUN FOLDERS NOT PRESENT`, or its command was refused:** the two `part 1` lines as above with `DIFFERENT: 0`; a line beginning `RESULT: PARTIAL - nothing differed (34800 old scores were compared in part 1)`; `COMPARE EXIT CODE 3`; the third command prints **0**. Record the second command's number, whatever it is.
- Anything else is a STOP: a `DIFFERENT:` count above 0, a third number above 0, `RESULT: STOP` or `RESULT: REFUSED`.

## Clean-up (always, whether the task passed or stopped)

**30. Remove the task clone, the extracted package and the clone's evidence folder.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T025
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, do not run step 32, and tell the project owner.

**The scratch folder `D:\DELETE_ME\a_p_r_i_r\T025` is not removed by this task.** It is left as it is, whether the task passed or stopped; the project owner deletes it himself when the Claude web chat says it is no longer needed.

## Report

**31. Finish** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T025.md` in the format of `outbox\README.md` (the step table and the RESULT line at the top). Also record:
- the wall-clock time of each of steps 7, 11, 21, 23, 24 and 27;
- every folder this task created under `D:\DELETE_ME\` (`D:\DELETE_ME\a_p_r_i_r\T025`, `D:\DELETE_ME\a_p_r_i_r\T025\tree`, `D:\DELETE_ME\a_p_r_i_r\T025\evidence`) and that each was left in place, not removed;
- whether the main repository's `git status --short` after step 30 is the same as in step 2 (run it again and include it).

## Finish

**32. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T025
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**33. Tell the project owner** the RESULT line, the report's path, and: "please push".
