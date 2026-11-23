# TASK_T026 - Windows rehearsal of build step 2, second part: the two launchers, the first research fill and the comparison, in the scratch tree that TASK_T025 left on D:

**Task ID:** T026. **Date:** 23 November 2026. **Author:** the Claude web chat. Rulebook v0.7 (RAT-44). **Section 2A applies to steps 3 to 11, in the folder `D:\DELETE_ME\a_p_r_i_r\T025\`** (the folder of TASK_T025, kept for this purpose).

**Purpose.** TASK_T025 passed its steps 1 to 19 (the install sheet's parts 1 to 4, in a task clone) and stopped at its step 20, because the runner's shell already had the main `.venv` active and the scratch tree's `create_venv.bat` refuses then (report `outbox\REPORT_T025.md`, main `99465ff`). It left the scratch tree `D:\DELETE_ME\a_p_r_i_r\T025\tree` in place: the repository's files with build step 2 installed, and its settings file. The project owner then built that tree's own `.venv` himself, in a plain CMD window, with the tree's own two scripts (`[DEPS] SUCCESS. All 39 direct requirements installed`). This task runs the steps of TASK_T025 that did not run, on that tree as it stands: the launchers' first real use, the first fill of both games on the real results, a second job, and the comparison with the old records (the install sheet's parts 5 to 7). **Steps 4 to 11 are steps 22 to 29 of TASK_T025 r1 (the text the reviewer passed in EX_292), with the same commands.** **What a scratch run computes is a rehearsal, not a result of the project.**

**What it does not do.** It makes no task clone and changes nothing in the main repository (only this task's report is committed there) and nothing in the main `.venv`. It builds no Python environment and runs no environment script: no `create_venv.bat`, no `install_upgrade_dependencies_into_venv.bat`, no activation, no `pip`. It runs no coordinator, no old launcher, no results updater, no scraper, no Mode H command, and it contacts no website: it has no network use at all. It ends no process and changes no date, time or time zone. It names no real QA or PROD tree.

**Before the owner starts this task (the owner, not the runner):** `git pull --ff-only` has been done and this is a new Claude Code conversation; nothing of the project is running; `D:\DELETE_ME\a_p_r_i_r\T025` is as TASK_T025 and his own two commands left it. The task takes about an hour, most of it unattended.

## Owner options

- None.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| SCRATCH (the scratch folder) | `D:\DELETE_ME\a_p_r_i_r\T025` |
| TREE (the scratch tree) | `D:\DELETE_ME\a_p_r_i_r\T025\tree` |
| SEV (the scratch evidence folder) | `D:\DELETE_ME\a_p_r_i_r\T025\evidence` |
| SPY (the scratch tree's own Python) | `D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv\Scripts\python.exe` |

Run each command in Git Bash, from MAIN, exactly as written. On anything other than the expected output and exit code: **STOP**, record the output, and go to step 12. Never retry, repair or reorder a step. **After a STOP, leave `D:\DELETE_ME\a_p_r_i_r\T025` exactly as it is** (rulebook section 2A item 9).

**Recording** (so that nothing improvised is needed):
- Write `CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T026.md` as you go: after each step, add its command, its exit code and its output, before starting the next step.
- Exit codes: the program's own. Do not pipe a command under test into another program. Where a step below itself pipes a recorded file through `tr`, `grep`, `tail` or `wc`, that is only to show parts of the file.
- **What you may add to a task line, and nothing else:** `cd` to MAIN before it; and, for a line that does not itself write an `EXIT CODE` line, `echo "EXIT CODE $?"` straight after it. Neither is a deviation. For the time of a long step you may run `date +%H:%M:%S` in Git Bash as a command of its own before and after it: with a format it only prints the time. Never run `date` or `time` in CMD.
- **Steps marked (long)** can run longer than the shell's foreground limit, so each such command line carries its own recording: run that exact line as one background command, and wait until it has finished. Its output and, on the last line, its own exit status (`... EXIT CODE <n>`, written by the same shell straight after the program ends) are in the file the line names. If that last line is missing or shows another number than the step expects, that is a STOP: never infer a pass from the other lines, and never take an exit status from another shell or from the launch of the background command.
- **What goes into the report from a recorded file** is said at each step. Files under `D:\DELETE_ME\a_p_r_i_r\T025` stay there; only the text a step names is copied into the report, under a heading that names the file it came from (rulebook section 2A item 4 and section 7).
- **Never copy into the report:** a line that shows numbers drawn in any draw, or a line that shows a path under `C:\Users\`. Put `[line withheld: possible data value]` or `[line withheld: a user folder path]` in its place and say so under Deviations. The commands of this task print counts, draw numbers (which draw, not what was drawn), times and check lines.

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

**3. The scratch folder is an ordinary folder on D:, and the scratch tree is as this task needs it** (rulebook section 2A item 2; read-only): its settings file, its two launchers, the command program and its own Python are there, its evidence folder is there, and no research job has run in it yet.
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import os, sys; p = r'D:\DELETE_ME'; t = r'D:\DELETE_ME\a_p_r_i_r\T025\tree'; j = getattr(os.path, 'isjunction', lambda x: False); missing = [n for n in ('ENVIRONMENT.ini', 'Run_Research.bat', 'Withdraw_Variant.bat', r'src\research_command.py', r'.venv\Scripts\python.exe') if not os.path.isfile(os.path.join(t, n))]; early = [n for n in (r'results\research', 'records') if os.path.lexists(os.path.join(t, n))]; ok = os.path.isdir(p) and not os.path.islink(p) and not j(p) and os.path.normcase(os.path.realpath(p)) == os.path.normcase(p) and os.path.isdir(r'D:\DELETE_ME\a_p_r_i_r\T025\evidence') and not missing and not early; print('real path:', os.path.realpath(p)); print('missing:', missing); print('there already:', early); print('SCRATCH CHECK PASS' if ok else 'SCRATCH CHECK STOP'); sys.exit(0 if ok else 1)"
```
Expected: `real path: D:\DELETE_ME`, `missing: []`, `there already: []`, then `SCRATCH CHECK PASS`.

**4. The scratch tree's Python.**
```
"D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv\Scripts\python.exe" -I -c "import sys, platform; print(sys.prefix); print(sys.version); print(platform.platform())"
```
Expected: `D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv`, a Python version, and a Windows platform line.

**5. (long) The first fill: the research job on both games** (the launcher's first real use; half an hour to an hour).
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

**6. (long) The same job once more** (it has nothing new to compute; a few minutes).
```
"D:/DELETE_ME/a_p_r_i_r/T025/tree/Run_Research.bat" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/second_job.txt" 2>&1; echo "JOB EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/second_job.txt"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/second_job.txt"
```
Expected: for each game a line with `written: 0 forecasts, 0 scores, 0 prevailing lines, 0 eligibility draws, 0 report files`; no line with `WARNING`, `REFUSED` or `STOP`; the line `The job finished.`; and as the last line `JOB EXIT CODE 0`. Copy the whole output into the report.

**7. The withdrawal launcher starts** (`--help` only prints the command's help; it names no variant and changes nothing).
```
"D:/DELETE_ME/a_p_r_i_r/T025/tree/Withdraw_Variant.bat" --help > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/withdraw_help.txt" 2>&1; echo "WITHDRAW EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/withdraw_help.txt"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/withdraw_help.txt"
```
Expected: a first line beginning `usage: Withdraw_Variant.bat`, a line `Withdraw a defective variant (specification 11).`, and as the last line `WITHDRAW EXIT CODE 0`. Anything else (a line with `REFUSED`, a Windows "not recognized" message, another exit code) is a STOP. Copy the whole output into the report.

**8. (long) Copy the old system's development run folders from the main repository into the scratch tree, by reading** (rulebook section 2A item 3; nothing is written in the main repository; these folders are ignored by Git and exist only on this PC).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import os, shutil; p = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\results\real\development'; d = r'D:\DELETE_ME\a_p_r_i_r\T025\tree\results\real\development\contract_runs'; names = [n for n in os.listdir(p) if n.lower() == 'contract_runs']; names and shutil.copytree(os.path.join(p, names[0]), d); print('OLD RUN FOLDERS COPIED' if names else 'OLD RUN FOLDERS NOT PRESENT')" > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/old_runs_copy.txt" 2>&1; echo "COPY EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/old_runs_copy.txt"
```
The command lists the folder `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\results\real\development` and looks for the name `contract_runs` in that list. Expected, in `old_runs_copy.txt`: `OLD RUN FOLDERS COPIED`, or `OLD RUN FOLDERS NOT PRESENT` when the list holds no such name (only that case is "not present"; step 11 says what each means); then `COPY EXIT CODE 0`. Copy the whole file into the report. **A STOP is: the permission system refusing this command; a traceback or any error in the file (a folder that cannot be listed or read, a copy that fails); or any other exit code. Do not look for another way to make the copy.**

**9. (long) The early comparison with the old development records** (it reads only; a few minutes).
```
"D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv\Scripts\python.exe" -B "D:\DELETE_ME\a_p_r_i_r\T025\tree\exchange\EX_288_Claude\STEP2_Research_Engine_v1r2\tools\compare_fill_with_old_records.py" --tree "D:\DELETE_ME\a_p_r_i_r\T025\tree" > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt" 2>&1; echo "COMPARE EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt"
```

**10. The comparison's lines that are not per-variant lines, and the count of per-variant lines.**
```
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt" | grep -v -e " equal$" -e "^DIFFERENT"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt" | grep -c " equal$"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt" | grep -c "^DIFFERENT"
```
Copy the output of the three commands into the report. Lines beginning `DIFFERENT` are counted and never copied (they may show numbers drawn). **The exit codes of the second and third commands:** `grep -c` prints its count and exits 0 when the count is above 0, and exits 1 when the count it prints is exactly 0. For these two commands an exit code 1 together with a printed `0` is therefore not an error. An exit code 2, no number printed, or an exit code that does not fit the number printed, is a STOP. Whether the numbers themselves are the right ones is step 11.

**11. What step 10 must show.**
- **If step 8 said `OLD RUN FOLDERS COPIED`:** for each game one line `part 1: old score records (TOP and WORST): N; equal in the new score lists: N; DIFFERENT: 0`, one line beginning `part 2: old development forecasts read from the run folders:` with `DIFFERENT: 0`, and one line `part 2: forecasts named by the tracked rank ledgers: N; of those not among the old forecasts compared: 0`; a line beginning **`RESULT: PASS - COMPLETE - both games; all 34800 old score records equal the new score lists`**; `COMPARE EXIT CODE 0`; the second command prints **160**; the third prints **0**.
- **If step 8 said `OLD RUN FOLDERS NOT PRESENT`:** the two `part 1` lines as above with `DIFFERENT: 0`; a line beginning `RESULT: PARTIAL - nothing differed (34800 old scores were compared in part 1)`; `COMPARE EXIT CODE 3`; the third command prints **0**. Record the second command's number, whatever it is.
- Anything else is a STOP: a `DIFFERENT:` count above 0, a third number above 0, `RESULT: STOP` or `RESULT: REFUSED`.

## Clean-up

**12. Nothing to remove.** This task makes no task clone. **The scratch folder `D:\DELETE_ME\a_p_r_i_r\T025` is not removed by this task.** It is left as it is, whether the task passed or stopped; the project owner deletes it himself when the Claude web chat says it is no longer needed.

## Report

**13. Finish** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T026.md` in the format of `outbox\README.md` (the step table and the RESULT line at the top). Also record:
- the wall-clock time of each of steps 5, 6 and 9 (for steps 5 and 6 the job's own `RESEARCH JOB - START` and `RESEARCH JOB - END` lines give it);
- that this task created no folder under `D:\DELETE_ME\`, and that `D:\DELETE_ME\a_p_r_i_r\T025` was left in place, not removed;
- whether the main repository's `git status --short` at the end is the same as in step 2 (run it again and include it).

## Finish

**14. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T026
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**15. Tell the project owner** the RESULT line, the report's path, and: "please push".
