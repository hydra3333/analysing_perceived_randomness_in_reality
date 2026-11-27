# TASK_T029 - the living system's test suite on Windows, in a scratch DEV tree with its own Python environment, in the scratch folder on D:

**Task ID:** T029. **Date:** 27 November 2026. **Author:** the Claude web chat. **Rulebook v0.8 (needs it ratified and installed, with the permission settings of the same edition; step 1 checks).** **Section 2A applies to steps 3 to 11, in the folder `D:\DELETE_ME\a_p_r_i_r\T029`** (new; this task creates it). (r1: the reviewer's corrections of its reading at `3c765bb`, decision log entry 369. r2: step 3 probes every form of the drive guard, after the first run stopped there because the settings did not refuse `T:\`; decision log entry 372. r3: step 8 unsets `VIRTUAL_ENV` for its two commands, after the third run stopped there because the runner's shell has the main `.venv` active; decision log entry 376.)

**Purpose.** The simple scheme's living system (`a_p_r_i_r_DEV`) has been built and tested only in the cloud, on Linux. This task is item 2 of the owner's work order (decision log entry 365), first part: the whole test suite of the living system on the owner's Windows PC, in a scratch copy of the DEV tree that builds its own Python environment with its own two scripts, exactly as the owner will build his. Among the tests are those that start a tree's research job as another process with that tree's own Python, that press Ctrl+C while such a job runs, and that make links and junctions. Every test runs on invented draws and toy methods; none lets the results updater reach any website (each replaces the browser with one that refuses). It also checks, harmlessly, that the new permission settings refuse what they are meant to refuse.

**What it does not do.** It runs no command of the system (no launcher, no research job, no install). It changes nothing in the main repository (only this task's report is committed there), nothing in the main `.venv`, and nothing of the real DEV tree, which it reads only through `git ls-files` and by copying its tracked files. It reads no `ENVIRONMENT.ini` of a real tree, no `source_data` and no `results`. It makes no task clone. It ends no process. It changes no date, time or time zone.

**The one program of this task** is `inbox\REHEARSAL_HELPER.py` (the rehearsal's shared helper; it writes only under `D:\DELETE_ME\` and refuses any other place). Steps 4 to 7 run it with the main venv's Python; step 10 runs it with the scratch tree's own Python, because the tests need that environment's packages.

**Before the owner starts this task (the owner, not the runner):** `git pull --ff-only` has been done and this is a new Claude Code conversation; nothing of the project is running; the folder `D:\DELETE_ME` exists; **and if a folder `D:\DELETE_ME\a_p_r_i_r\T029` is left from an earlier run of this task that stopped, the owner has deleted it** (step 4 stops if it is there). The task takes about 15 to 25 minutes, most of it the package downloads of step 8, and writes about 1 GB into the scratch folder (the scratch tree's `.venv`).

## Owner options

- None.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| HELPER (read only) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py` |
| SCRATCH (this task's folder; made in step 5) | `D:\DELETE_ME\a_p_r_i_r\T029` |
| TREE (the scratch DEV tree) | `D:\DELETE_ME\a_p_r_i_r\T029\s_DEV` |
| TPY (the scratch tree's own Python; made in step 8) | `D:\DELETE_ME\a_p_r_i_r\T029\s_DEV\.venv\Scripts\python.exe` |
| TMPDIR (the tests' temporary folder) | `D:\DELETE_ME\a_p_r_i_r\T029\tmp` |

Run each command in Git Bash, from MAIN, exactly as written. On anything other than the expected lines and exit code of a step: **STOP**, record the output, and go to step 12. Never retry, repair or reorder a step. **After a STOP, leave `D:\DELETE_ME\a_p_r_i_r\T029` exactly as it is** (rulebook section 2A item 9). This task does not delete its scratch folder; the owner deletes it by hand when he wishes.

- **What goes into the report:** the whole output of every step, except steps 8 and 10, whose outputs are long: for them the lines the step says to show. The files under `D:\DELETE_ME\a_p_r_i_r\T029` stay there.

## Steps

**1. Python, and the rulebook and permission settings in force.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import sys, platform; print(sys.version); print(platform.platform())"
grep -c "^\*\*Version:\*\* v0.8" CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md
grep -c "results_upd" .claude/settings.json
```
Expected: a Python version and a Windows platform line; then `1`; then `1`. Anything else (the rulebook or the settings are not those of v0.8): STOP.

**2. The repository's state** (read only).
```
git rev-parse HEAD
git status --short --untracked-files=no -- a_p_r_i_r_DEV CLAUDE_CODE_WORKING_FOLDER_TREE/inbox
```
Expected: one commit hash (record it), then no output at all (the living system and the task files are as committed). Any output from the second command: STOP.

**3. (Refusals planted on purpose, rulebook section 2A item 5 kind (i).) The permission settings refuse what they are meant to** (seven harmless commands; each would only print its own words if it ran). You are authorised to attempt them; their refusal is the PASS of this step. **Attempt all seven, one at a time, even if one of them runs,** and record for each what happened; only then decide the step.
```
echo results_updater
echo 'T:\a_p_r_i_r_QA'
echo 't:\a_p_r_i_r_QA'
echo 'G:\a_p_r_i_r_PROD'
echo 'g:\a_p_r_i_r_PROD'
echo T:/a_p_r_i_r_QA
echo /g/a_p_r_i_r_PROD
```
Expected for each: **refused by the permission settings, and not run** (Claude Code says the permission was denied). Record what Claude Code said for each. If any of the seven ran (printed its words): STOP after the seventh, and list in the report which ran.

**4. The scratch folder is an ordinary folder on D:, and this task's folder is new** (rulebook section 2A item 2).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" check-scratch "D:\DELETE_ME\a_p_r_i_r\T029"
```
Expected: `real path of the scratch folder: D:\DELETE_ME`, `folders on the way that are links or junctions: []`, the task folder `(not there yet)`, then `SCRATCH CHECK PASS`; exit code 0.

**5. The list of the living system's files** (read only in MAIN; the list is written into the scratch folder).
```
mkdir -p "D:/DELETE_ME/a_p_r_i_r/T029" && git ls-files a_p_r_i_r_DEV > "D:/DELETE_ME/a_p_r_i_r/T029/files.txt" && wc -l < "D:/DELETE_ME/a_p_r_i_r/T029/files.txt"
```
Expected: one number, the count of the living system's tracked files (record it; 189 when this task was written).

**6. The scratch DEV tree: a copy of those files, each read back.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" copy-dev "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality" "D:\DELETE_ME\a_p_r_i_r\T029\files.txt" "D:\DELETE_ME\a_p_r_i_r\T029\s_DEV"
```
Expected: `files listed: N; copied and read back: N; families kept: all` with N the number of step 5, then `COPY PASS`; exit code 0.

**7. The scratch tree's settings file** (every path in it under `D:\DELETE_ME\`; rulebook section 2A item 5).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" settings "D:\DELETE_ME\a_p_r_i_r\T029\s_DEV" DEV
```
Expected: the file's eleven lines (`[environment]`, `role = DEV`, then for DEV, QA and PROD a `tree_root` of `D:\DELETE_ME\a_p_r_i_r\T029\s_<ROLE>` and a `backup_root` of `D:\DELETE_ME\a_p_r_i_r\T029\backups\<ROLE>`), the line `every path above lies under D:\DELETE_ME`, then `SETTINGS PASS`; exit code 0. Check by eye that every path printed begins `D:\DELETE_ME\a_p_r_i_r\T029\`; if one does not: STOP.

**8. (long) The scratch tree's own Python environment, built by its own two scripts** (rulebook section 2A item 7(a); the package downloads are this task's one network use; `TMP`, `TEMP` and `PIP_CACHE_DIR` point inside the scratch folder for both scripts). Each of the two commands runs in a subshell that first unsets `VIRTUAL_ENV` for that command alone: the shell Claude Code is given may have the main repository's `.venv` active, and the script refuses to make an environment while another is active. Nothing is deactivated and no environment is changed by this; the scratch tree's scripts activate its own environment inside their own process, as they do for the owner.
```
mkdir -p "D:/DELETE_ME/a_p_r_i_r/T029/tmp_env" "D:/DELETE_ME/a_p_r_i_r/T029/pip_cache" && ( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T029\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T029\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T029\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T029/s_DEV/create_venv.bat" > "D:/DELETE_ME/a_p_r_i_r/T029/venv_create.txt" 2>&1 ); echo "VENV EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T029/venv_create.txt"; tail -n 4 "D:/DELETE_ME/a_p_r_i_r/T029/venv_create.txt"
( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T029\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T029\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T029\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T029/s_DEV/install_upgrade_dependencies_into_venv.bat" INSTALL > "D:/DELETE_ME/a_p_r_i_r/T029/venv_packages.txt" 2>&1 ); echo "PACKAGES EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T029/venv_packages.txt"; tail -n 4 "D:/DELETE_ME/a_p_r_i_r/T029/venv_packages.txt"
```
Expected: the first ends `VENV EXIT CODE 0`; the second shows `[DEPS] SUCCESS. All 39 direct requirements installed; research compatibility tests remain required.` and ends `PACKAGES EXIT CODE 0`. Show in the report only the lines the two `tail` commands print.

**9. The scratch tree's Python.**
```
"D:\DELETE_ME\a_p_r_i_r\T029\s_DEV\.venv\Scripts\python.exe" -I -c "import sys, numpy, selenium; print(sys.version); print(sys.prefix); print('numpy', numpy.__version__, 'selenium', selenium.__version__)"
```
Expected: a Python version; `D:\DELETE_ME\a_p_r_i_r\T029\s_DEV\.venv`; the two package versions. A `sys.prefix` elsewhere: STOP.

**10. (long) The whole test suite, with the scratch tree's own Python and every temporary file inside the scratch folder** (rulebook section 2A item 5; a few minutes).
```
"D:\DELETE_ME\a_p_r_i_r\T029\s_DEV\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" run-tests "D:\DELETE_ME\a_p_r_i_r\T029\s_DEV" "D:\DELETE_ME\a_p_r_i_r\T029\tmp" > "D:/DELETE_ME/a_p_r_i_r/T029/tests.txt" 2>&1; echo "TESTS EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T029/tests.txt"; head -n 1 "D:/DELETE_ME/a_p_r_i_r/T029/tests.txt"; grep -E "^(TESTS RUN|SKIPPED|TESTS EXIT CODE|FAIL:|ERROR:)" "D:/DELETE_ME/a_p_r_i_r/T029/tests.txt"
```
Expected: the first line names TPY's Python and the temporary folder `D:\DELETE_ME\a_p_r_i_r\T029\tmp`; then `TESTS RUN 280; FAILURES 0; ERRORS 0; SKIPPED 3` (280 when this task was written); three `SKIPPED:` lines, each saying either `the frozen engine is not beside this tree` or `the first system's updater is kept in the repository only` (these tests need the repository's top level, which a scratch tree does not have); and `TESTS EXIT CODE 0`. Any `FAIL:` or `ERROR:` line, a FAILURES or ERRORS count other than 0, or an exit code other than 0: STOP, and copy the whole of `tests.txt` into the report under the heading `From D:\DELETE_ME\a_p_r_i_r\T029\tests.txt`. A `SKIPPED:` line for another reason is not a STOP: record it under Observations, and say in the report's first lines that TASK_T030 waits until the web chat has assessed it.

**11. The tests left no temporary file behind.**
```
ls -A "D:/DELETE_ME/a_p_r_i_r/T029/tmp" | wc -l
```
Expected: `0`. Another number is not a STOP: record it under Observations.

**12. The report.** Write `outbox\REPORT_T029.md` in the format of `outbox\README.md`, with: the commit of step 2; each step's command, exit code and output as said above; and, at the end, the folder this task created under `D:\DELETE_ME\` (`D:\DELETE_ME\a_p_r_i_r\T029`, with `s_DEV`, its `.venv`, `tmp`, `tmp_env`, `pip_cache`, and the files `files.txt`, `venv_create.txt`, `venv_packages.txt` and `tests.txt`), saying that it was not removed.

**13. Finish.** Commit the report:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T029
```
Then tell the project owner the result line, the report's path, and "please push".
