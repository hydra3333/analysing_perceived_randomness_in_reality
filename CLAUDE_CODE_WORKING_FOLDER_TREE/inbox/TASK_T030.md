# TASK_T030 - the simple scheme's commands on three scratch trees with invented results, in the scratch folder on D:

**Task ID:** T030. **Date:** 27 November 2026. **Author:** the Claude web chat. **Rulebook v0.8 (needs it ratified and installed; step 1 checks).** **Section 2A applies to steps 3 to 31, in the folder `D:\DELETE_ME\a_p_r_i_r\T030`** (new; this task creates it). Run it after TASK_T029 has passed, with no `SKIPPED:` line but the three it names (or with any other assessed by the web chat). (r1: the reviewer's corrections of its reading at `3c765bb`, decision log entry 369. r2: the environment steps unset `VIRTUAL_ENV` for their commands, as TASK_T029 r3 does; decision log entry 376.)

**Purpose.** Item 2 of the owner's work order (decision log entry 365), second part: the commands of the simple scheme, run on the owner's Windows PC as he will run them, on three scratch trees (`s_DEV`, `s_QA`, `s_PROD`) with **invented results** (the owner's decision, entry 366: this task qualifies the commands, not the science; TASK_T031 establishes the science). It covers: a research job; `Make_Installable`; `Create_Tree` QA and PROD; each new tree building its own Python environment and running its first job; `Install --show` and `Install` (whose child process, the destination's own job under the lock the install holds, is the part only Windows can show); a part whose flag is out of date left alone; `Backup`; `Retire` in all three trees; `Copy_From_PROD both`; `Restore` (the rename of a whole tree aside, the other part only Windows can show); three refusals planted on purpose; and `Who_Uses`. The scratch DEV tree keeps two of the 12 method families (E_001 and E_002, four methods), so that every job takes seconds. Every step's expected lines below were taken from a dry run of the same sequence in the cloud.

**What it does not do.** It never runs the results updater: every research job is started with `--no-update`, and the commands that run a tree's job start it with `--no-update` themselves. It reads no real draw, no `source_data` and no `results` of the repository or of a real tree. It changes nothing in the main repository (only this task's report is committed there), nothing in the main `.venv`, nothing of the real DEV tree, and nothing on the `T:` or `G:` drives. It ends no process and presses no Ctrl+C. It changes no date, time or time zone.

**Programs.** The scratch trees' own launchers (`.bat` files at each scratch tree's root), each with that tree's own Python; and `inbox\REHEARSAL_HELPER.py` (the rehearsal's shared helper; it writes only under `D:\DELETE_ME\`), with the main venv's Python except in step 6.

**Before the owner starts this task (the owner, not the runner):** TASK_T029 has passed; `git pull --ff-only` has been done and this is a new Claude Code conversation; nothing of the project is running. The task takes about 30 to 50 minutes, most of it the package downloads of three Python environments (steps 5, 11 and 19), and writes about 3 GB into the scratch folder.

## Owner options

- None.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| HELPER (read only) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py` |
| SCRATCH (this task's folder) | `D:\DELETE_ME\a_p_r_i_r\T030` |
| DEV, QA, PROD (the scratch trees) | `D:\DELETE_ME\a_p_r_i_r\T030\s_DEV`, `...\s_QA`, `...\s_PROD` |
| BACKUPS (their backup folders) | `D:\DELETE_ME\a_p_r_i_r\T030\backups\DEV`, `...\QA`, `...\PROD` |

Run each command in Git Bash, from MAIN, exactly as written. Each step gives its expected exit code and the lines that must appear (a step's output may hold more lines; paths in it are the scratch paths above, and `<time>` stands for a date and time). On anything else: **STOP**, record the output, and go to step 32. Never retry, repair or reorder a step. Three steps (28, 29, 30) expect a refusal on purpose and say so (step 29 is of rulebook section 2A item 5 kind (ii): you are authorised to attempt it); a refusal anywhere else is a STOP. **After a STOP, leave `D:\DELETE_ME\a_p_r_i_r\T030` exactly as it is.** This task does not delete its scratch folder; the owner deletes it by hand when he wishes.

- **What goes into the report:** every step's command, exit code and whole output, except steps 5, 11 and 19 (the `tail` lines only). The files under the scratch folder stay there.

## Steps

**1. The rulebook in force.**
```
grep -c "^\*\*Version:\*\* v0.8" CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md
git rev-parse HEAD
git status --short --untracked-files=no -- a_p_r_i_r_DEV CLAUDE_CODE_WORKING_FOLDER_TREE/inbox
```
Expected: `1`; one commit hash (record it); then no output at all. Anything else: STOP.

**2. The scratch folder is an ordinary folder on D:, and this task's folder is new.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" check-scratch "D:\DELETE_ME\a_p_r_i_r\T030"
```
Expected: `SCRATCH CHECK PASS`; exit code 0.

**3. The scratch DEV tree: the living system's files, keeping the method families E_001 and E_002.**
```
mkdir -p "D:/DELETE_ME/a_p_r_i_r/T030" && git ls-files a_p_r_i_r_DEV > "D:/DELETE_ME/a_p_r_i_r/T030/files.txt" && "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" copy-dev "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality" "D:\DELETE_ME\a_p_r_i_r\T030\files.txt" "D:\DELETE_ME\a_p_r_i_r\T030\s_DEV" --families E_001,E_002
```
Expected: `files listed: N; copied and read back: M; families kept: ['E_001', 'E_002']` (N and M as at the commit of step 1; 189 and 87 when this task was written), then `COPY PASS`; exit code 0.

**4. The scratch DEV tree's settings file.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" settings "D:\DELETE_ME\a_p_r_i_r\T030\s_DEV" DEV
```
Expected: eleven lines naming `D:\DELETE_ME\a_p_r_i_r\T030\s_DEV`, `...\s_QA`, `...\s_PROD` and `D:\DELETE_ME\a_p_r_i_r\T030\backups\DEV`, `...\QA`, `...\PROD`; `every path above lies under D:\DELETE_ME`; `SETTINGS PASS`; exit code 0. Check by eye that every path begins `D:\DELETE_ME\a_p_r_i_r\T030\`; if one does not: STOP.

**5. (long) The scratch DEV tree's own Python environment** (`TMP`, `TEMP` and `PIP_CACHE_DIR` inside the scratch folder, here and in steps 11 and 19). Each of the two commands runs in a subshell that first unsets `VIRTUAL_ENV` for that command alone: the shell Claude Code is given may have the main repository's `.venv` active, and the script refuses to make an environment while another is active. Nothing is deactivated and no environment is changed by this; the scratch tree's scripts activate its own environment inside their own process, as they do for the owner.
```
mkdir -p "D:/DELETE_ME/a_p_r_i_r/T030/tmp_env" "D:/DELETE_ME/a_p_r_i_r/T030/pip_cache" && ( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T030\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/create_venv.bat" > "D:/DELETE_ME/a_p_r_i_r/T030/venv_DEV_1.txt" 2>&1 ); echo "VENV EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T030/venv_DEV_1.txt"; tail -n 2 "D:/DELETE_ME/a_p_r_i_r/T030/venv_DEV_1.txt"
( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T030\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/install_upgrade_dependencies_into_venv.bat" INSTALL > "D:/DELETE_ME/a_p_r_i_r/T030/venv_DEV_2.txt" 2>&1 ); echo "PACKAGES EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T030/venv_DEV_2.txt"; tail -n 2 "D:/DELETE_ME/a_p_r_i_r/T030/venv_DEV_2.txt"
```
Expected: `VENV EXIT CODE 0`; then `[DEPS] SUCCESS. ...` and `PACKAGES EXIT CODE 0`.

**6. Invented results for both games** (a seeded generator; no real draw), with the scratch tree's own Python.
```
"D:\DELETE_ME\a_p_r_i_r\T030\s_DEV\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" invented "D:\DELETE_ME\a_p_r_i_r\T030\s_DEV" 115
```
Expected: `POWERBALL: invented results through draw 1259`, `OZLOTTO: invented results through draw 1589`, `INVENTED RESULTS WRITTEN`; exit code 0.

**7. The scratch DEV tree's first research job.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Run_Research.bat" --no-update
```
Expected exit code 0, and among the lines: `RESEARCH JOB - START - <time> - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T030\s_DEV`; `About to work: POWERBALL, OZLOTTO (results updater left out: --no-update)`; `Backup made: D:\DELETE_ME\a_p_r_i_r\T030\backups\DEV\DEV_<time>_after_job.zip`; `POWERBALL: finished. Results on file through draw 1259; written: 155 forecasts, 151 scores, 2 series files, 236 report files. ...`; the same for `OZLOTTO` through draw 1589; and the last line `The job finished.`

**8. Make_Installable for every method and the infrastructure.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Make_Installable.bat" ALL INFRA
```
Expected exit code 0: four lines `flagged: E_001/FULL_HISTORY_RAW_COUNTS_V1 (...)`, `flagged: E_002/RECUR_MEAN_ALL_V1 (...)`, `flagged: E_002/RECUR_MEAN_LAST8_V1 (...)`, `flagged: E_002/RECUR_MEDIAN_ALL_V1 (...)`; `flagged: the infrastructure (engine ..., updater ..., launchers ...)`; `Done.`

**9. Create_Tree QA.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Create_Tree.bat" QA
```
Expected exit code 0: `CREATE the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA, from DEV (...)`; `  copied: the infrastructure and 4 methods (53 files), and DEV's accepted results (4 files). The settings file was written last.` (53 when this task was written); a last line beginning `The QA tree is created.`

**10. The new QA tree's settings file names only scratch places** (it is a scratch tree's file, rulebook section 2A item 5).
```
cat "D:/DELETE_ME/a_p_r_i_r/T030/s_QA/ENVIRONMENT.ini"
```
Expected: two comment lines, then `[environment]`, `role = QA`, and the same six paths as step 4, all beginning `D:\DELETE_ME\a_p_r_i_r\T030\`. Otherwise: STOP.

**11. (long) The QA tree's own Python environment.**
```
( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T030\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T030/s_QA/create_venv.bat" > "D:/DELETE_ME/a_p_r_i_r/T030/venv_QA_1.txt" 2>&1 ); echo "VENV EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T030/venv_QA_1.txt"; tail -n 2 "D:/DELETE_ME/a_p_r_i_r/T030/venv_QA_1.txt"
( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T030\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T030/s_QA/install_upgrade_dependencies_into_venv.bat" INSTALL > "D:/DELETE_ME/a_p_r_i_r/T030/venv_QA_2.txt" 2>&1 ); echo "PACKAGES EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T030/venv_QA_2.txt"; tail -n 2 "D:/DELETE_ME/a_p_r_i_r/T030/venv_QA_2.txt"
```
Expected: `VENV EXIT CODE 0`; then `[DEPS] SUCCESS. ...` and `PACKAGES EXIT CODE 0`.

**12. The QA tree's first research job.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_QA/Run_Research.bat" --no-update
```
Expected exit code 0: `the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA`; the same two `finished.` lines as step 7 (155 forecasts, 151 scores in each game); last line `The job finished.`

**13. A change to one method in the scratch DEV tree, and its flag.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" plant-edit "D:\DELETE_ME\a_p_r_i_r\T030\s_DEV\src\methods\E_002\RECUR_MEDIAN_ALL_V1\method.py"
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Make_Installable.bat" E_002/RECUR_MEDIAN_ALL_V1
```
Expected: `EDIT PLANTED` (exit code 0); then `flagged: E_002/RECUR_MEDIAN_ALL_V1 (...)` and `Done.` (exit code 0).

**14. Install QA --show: the plan, and nothing changed.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Install.bat" QA --show
```
Expected exit code 0, exactly: `INSTALL from DEV (D:\DELETE_ME\a_p_r_i_r\T030\s_DEV) into the QA tree (D:\DELETE_ME\a_p_r_i_r\T030\s_QA):`, `  replace: E_002/RECUR_MEDIAN_ALL_V1 (its results in the QA tree are made again)`, `--show: nothing was changed.`

**15. Install QA: the backup, the copy, and the QA tree's own job as another process under the lock the install holds** (the part only Windows can show).
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Install.bat" QA
```
Expected exit code 0, and among the lines, in this order: the same first two lines as step 14; `Backup made of the QA tree: D:\DELETE_ME\a_p_r_i_r\T030\backups\QA\QA_<time>_before_install.zip`; `Installed into the QA tree: 0 infrastructure files, 1 methods.`; `Now the QA tree's own research job (results updater left out), under the lock held:`; then the QA job's own lines, among them `RESEARCH JOB - START - <time> - the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA`, two lines `REBUILT (said again): POWERBALL: E_002/RECUR_MEDIAN_ALL_V1: its stored results were made by other files than the method has now` (and the same for `OZLOTTO`), and `The job finished.`; and the last line `Install finished: the QA tree has the software and its results are up to date with it.`

**16. No lock is left in either tree.**
```
ls "D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/records" "D:/DELETE_ME/a_p_r_i_r/T030/s_QA/records"
```
Expected: in each folder `JOB_LOG.jsonl` only (no `TREE.lock`).

**17. Install QA again: nothing to install.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Install.bat" QA
```
Expected exit code 0, exactly: the `INSTALL from DEV ...` line and `  Nothing to install: the QA tree already has every part that is flagged in DEV.`

**18. Create_Tree PROD, and the new tree's settings file.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Create_Tree.bat" PROD
cat "D:/DELETE_ME/a_p_r_i_r/T030/s_PROD/ENVIRONMENT.ini"
```
Expected exit code 0: `CREATE the PROD tree at D:\DELETE_ME\a_p_r_i_r\T030\s_PROD, ...`; `  copied: the infrastructure and 4 methods (53 files), and DEV's accepted results (4 files). ...`; a last line beginning `The PROD tree is created.` Then the settings file: `role = PROD` and the same six paths as step 4, all beginning `D:\DELETE_ME\a_p_r_i_r\T030\`. Otherwise: STOP.

**19. (long) The PROD tree's own Python environment.**
```
( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T030\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T030/s_PROD/create_venv.bat" > "D:/DELETE_ME/a_p_r_i_r/T030/venv_PROD_1.txt" 2>&1 ); echo "VENV EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T030/venv_PROD_1.txt"; tail -n 2 "D:/DELETE_ME/a_p_r_i_r/T030/venv_PROD_1.txt"
( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T030\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T030/s_PROD/install_upgrade_dependencies_into_venv.bat" INSTALL > "D:/DELETE_ME/a_p_r_i_r/T030/venv_PROD_2.txt" 2>&1 ); echo "PACKAGES EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T030/venv_PROD_2.txt"; tail -n 2 "D:/DELETE_ME/a_p_r_i_r/T030/venv_PROD_2.txt"
```
Expected: `VENV EXIT CODE 0`; then `[DEPS] SUCCESS. ...` and `PACKAGES EXIT CODE 0`.

**20. The PROD tree's first research job.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_PROD/Run_Research.bat" --no-update
```
Expected exit code 0: `the PROD tree at D:\DELETE_ME\a_p_r_i_r\T030\s_PROD`; the same two `finished.` lines as step 7; last line `The job finished.`

**21. A method changed in DEV and not flagged again is not installed.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" plant-edit "D:\DELETE_ME\a_p_r_i_r\T030\s_DEV\src\methods\E_001\FULL_HISTORY_RAW_COUNTS_V1\method.py"
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Install.bat" PROD --show
```
Expected: `EDIT PLANTED` (exit code 0); then, exit code 0, exactly: `INSTALL from DEV (...) into the PROD tree (D:\DELETE_ME\a_p_r_i_r\T030\s_PROD):`, `  NOT INSTALLED: E_001/FULL_HISTORY_RAW_COUNTS_V1: in DEV it is flagged, but its flag is older than its files; Make_Installable.bat makes the flag.`, `  Nothing to install: the PROD tree already has every part that is flagged in DEV.`, `--show: nothing was changed.`

**22. Backup.bat in the QA tree.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_QA/Backup.bat"
```
Expected exit code 0, one line: `Backup made of the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA: D:\DELETE_ME\a_p_r_i_r\T030\backups\QA\QA_<time>_on_demand.zip`

**23. Retire one method in every tree.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Retire.bat" E_002/RECUR_MEAN_LAST8_V1 rehearsal of a retirement
```
Expected exit code 0: three lines `Backup made of the DEV tree: ...\DEV_<time>_before_retire.zip` (then QA, then PROD); three lines `  DEV: E_002/RECUR_MEAN_LAST8_V1 is retired from POWERBALL draw 1260, OZLOTTO draw 1590. ...` (then `  QA:`, then `  PROD:`, the same draws); last line `Retired: E_002/RECUR_MEAN_LAST8_V1 (rehearsal of a retirement). In DEV the file I_AM_RETIRED beside the method is kept in Git: commit it. ...`

**24. The PROD tree's job applies the retirement.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_PROD/Run_Research.bat" --no-update
```
Expected exit code 0: `REBUILT (said again): POWERBALL: E_002/RECUR_MEAN_LAST8_V1: retired from draw 1260: 1 forecasts and 0 scores for that draw or later dropped` (and the same for `OZLOTTO` from draw 1590); last line `The job finished.`

**25. Copy_From_PROD both QA: QA becomes PROD's twin, and its job then finds nothing to compute.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Copy_From_PROD.bat" both QA
```
Expected exit code 0, among the lines: `COPY FROM PROD (D:\DELETE_ME\a_p_r_i_r\T030\s_PROD) into the QA tree (D:\DELETE_ME\a_p_r_i_r\T030\s_QA): both.`; `Backup made of the QA tree: ...\QA_<time>_before_copy_from_PROD.zip`; `  software: the QA tree's src folder and launchers are now PROD's.`; `  data: ...`; the QA job's lines with `written: 0 forecasts, 0 scores` in both games and `The job finished.`; last line `Copy finished: the QA tree's results are up to date with what it now holds.`

**26. Restore QA from the backup of step 22: the tree is renamed aside, never deleted** (the other part only Windows can show).
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Restore.bat" QA "$("E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" one-backup "D:\DELETE_ME\a_p_r_i_r\T030\backups\QA" _on_demand.zip)"
```
Expected exit code 0: `RESTORE the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA from D:\DELETE_ME\a_p_r_i_r\T030\backups\QA\QA_<time>_on_demand.zip:`; `Backup made of the QA tree: ...\QA_<time>_before_restore.zip`; `  unpacked: <number> files into a fresh folder.`; `  the tree as it was is kept at D:\DELETE_ME\a_p_r_i_r\T030\s_QA_set_aside_<time>. ...`; last line beginning `Restored: the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA is now as the backup holds it.`

**27. The folders after the restore, and the restored tree's settings file.**
```
ls "D:/DELETE_ME/a_p_r_i_r/T030"
cat "D:/DELETE_ME/a_p_r_i_r/T030/s_QA/ENVIRONMENT.ini"
```
Expected: `backups`, `files.txt`, `pip_cache`, `s_DEV`, `s_PROD`, `s_QA`, one `s_QA_set_aside_<time>`, `tmp_env` and the `venv_*.txt` files; then the settings file: `role = QA` and the same six paths as step 4, all beginning `D:\DELETE_ME\a_p_r_i_r\T030\`. Otherwise: STOP.

**28. (A refusal planted on purpose.) The restored QA tree has no Python environment: its launcher refuses.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_QA/Run_Research.bat" --no-update
```
Expected exit code 2 and the line `REFUSED: this tree's Python was not found at D:\DELETE_ME\a_p_r_i_r\T030\s_QA\.venv\Scripts\python.exe. Build the tree's .venv first.` This is the PASS of this step.

**29. (A refusal planted on purpose, rulebook section 2A item 5 kind (ii).) Nothing runs in the tree set aside: its folder name no longer ends with its role.**
```
"$(ls -d D:/DELETE_ME/a_p_r_i_r/T030/s_QA_set_aside_*)/Run_Research.bat" --no-update
```
Expected exit code 2 and a line beginning `REFUSED: D:\DELETE_ME\a_p_r_i_r\T030\s_QA_set_aside_<time>\ENVIRONMENT.ini [environment] role: the file says QA, but the folder it lies in is named "s_QA_set_aside_<time>", which does not end with QA.` This is the PASS of this step.

**30. (A refusal planted on purpose.) A tree is created only into a folder that is absent or empty.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Create_Tree.bat" QA
```
Expected exit code 2 and a line beginning `REFUSED: D:\DELETE_ME\a_p_r_i_r\T030\s_QA already holds something.` This is the PASS of this step.

**31. Who_Uses.**
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Who_Uses.bat" _shared/recurrence_gaps_v1.py
```
Expected exit code 0: three lines `E_002/RECUR_MEAN_ALL_V1    uses _shared/recurrence_gaps_v1.py` (then `RECUR_MEAN_LAST8_V1`, `RECUR_MEDIAN_ALL_V1`) and `3 of 4 methods use "_shared/recurrence_gaps_v1.py". ...`

**32. The report.** Write `outbox\REPORT_T030.md` in the format of `outbox\README.md`, with: the commit of step 1; each step's command, exit code and output as said above; and, at the end, the folder this task created under `D:\DELETE_ME\` (`D:\DELETE_ME\a_p_r_i_r\T030` with the scratch trees, the tree set aside, their backups and the text files), saying that it was not removed.

**33. Finish.** Commit the report:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T030
```
Then tell the project owner the result line, the report's path, and "please push".
