# REPORT_T030 - the simple scheme's commands on three scratch trees with invented results, in the scratch folder on D:

RESULT: PASS

- Task file: inbox/TASK_T030.md at main-repository commit d1a43bd1c553b58124828bebc65fd2c0f1fed8bd
- Run by: Claude Code (local runner), 2026-11-27 20:30 to 20:40 Cen. Australia Summer Time (UTC+1030)
- Owner options used: none (the task file offers none)
- Machine: Windows-11-10.0.26300-SP0; Python 3.15.2 at E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
- Section 2A folder: D:\DELETE_ME\a_p_r_i_r\T030 (created by this task; not removed, see Clean-up)

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | the rulebook in force | 0, 0, 0 | `1`; commit d1a43bd1c553b58124828bebc65fd2c0f1fed8bd; no output - PASS |
| 2 | the scratch folder is an ordinary folder on D: | 0 | `SCRATCH CHECK PASS` |
| 3 | the scratch DEV tree, families E_001 and E_002 | 0 | `COPY PASS` (files listed: 189; copied and read back: 87) |
| 4 | the scratch DEV tree's settings file | 0 | `SETTINGS PASS`; every path begins D:\DELETE_ME\a_p_r_i_r\T030\ |
| 5 | (long) the scratch DEV tree's own Python environment | 0, 0 | `VENV EXIT CODE 0`; `[DEPS] SUCCESS. ...`; `PACKAGES EXIT CODE 0` |
| 6 | invented results for both games | 0 | `INVENTED RESULTS WRITTEN` |
| 7 | the scratch DEV tree's first research job | 0 | `The job finished.` (155 forecasts, 151 scores in each game) |
| 8 | Make_Installable ALL INFRA | 0 | four methods and the infrastructure flagged; `Done.` |
| 9 | Create_Tree QA | 0 | `The QA tree is created. ...` (53 files, 4 results files) |
| 10 | the new QA tree's settings file names only scratch places | 0 | `role = QA`; the same six paths as step 4 |
| 11 | (long) the QA tree's own Python environment | 0, 0 | `VENV EXIT CODE 0`; `[DEPS] SUCCESS. ...`; `PACKAGES EXIT CODE 0` |
| 12 | the QA tree's first research job | 0 | `The job finished.` (155 forecasts, 151 scores in each game) |
| 13 | a change to one method, and its flag | 0, 0 | `EDIT PLANTED`; `flagged: E_002/RECUR_MEDIAN_ALL_V1 (...)`; `Done.` |
| 14 | Install QA --show | 0 | `--show: nothing was changed.` |
| 15 | Install QA (the destination's own job under the lock held) | 0 | `Install finished: the QA tree has the software and its results are up to date with it.` |
| 16 | no lock is left in either tree | 0 | `JOB_LOG.jsonl` only in each records folder |
| 17 | Install QA again | 0 | `Nothing to install: the QA tree already has every part that is flagged in DEV.` |
| 18 | Create_Tree PROD, and the new tree's settings file | 0, 0 | `The PROD tree is created. ...`; `role = PROD`; the same six paths |
| 19 | (long) the PROD tree's own Python environment | 0, 0 | `VENV EXIT CODE 0`; `[DEPS] SUCCESS. ...`; `PACKAGES EXIT CODE 0` |
| 20 | the PROD tree's first research job | 0 | `The job finished.` (155 forecasts, 151 scores in each game) |
| 21 | a method changed and not flagged again is not installed | 0, 0 | `EDIT PLANTED`; `NOT INSTALLED: E_001/FULL_HISTORY_RAW_COUNTS_V1 ...`; `--show: nothing was changed.` |
| 22 | Backup.bat in the QA tree | 0 | `Backup made of the QA tree ... QA_20261127_203836_on_demand.zip` |
| 23 | Retire one method in every tree | 0 | `Retired: E_002/RECUR_MEAN_LAST8_V1 (rehearsal of a retirement). ...` |
| 24 | the PROD tree's job applies the retirement | 0 | `The job finished.` (both games remade from the retirement draw) |
| 25 | Copy_From_PROD both QA | 0 | `Copy finished: the QA tree's results are up to date with what it now holds.` (0 forecasts, 0 scores) |
| 26 | Restore QA from the backup of step 22 | 0 | `Restored: the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA is now as the backup holds it. ...` (563 files; the tree set aside) |
| 27 | the folders after the restore, and the restored settings file | 0, 0 | the expected entries with one s_QA_set_aside_<time>; `role = QA`; the same six paths |
| 28 | (a refusal planted on purpose) the restored QA tree has no Python environment | 2 | `REFUSED: this tree's Python was not found ...` - PASS |
| 29 | (a refusal planted on purpose) nothing runs in the tree set aside | 2 | `REFUSED: ... which does not end with QA.` - PASS |
| 30 | (a refusal planted on purpose) a tree is created only into a folder that is absent or empty | 2 | `REFUSED: D:\DELETE_ME\a_p_r_i_r\T030\s_QA already holds something. ...` - PASS |
| 31 | Who_Uses | 0 | `3 of 4 methods use "_shared/recurrence_gaps_v1.py". ...` |

## Outputs

### Step 1

Command:
```
grep -c "^\*\*Version:\*\* v0.8" CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md
```
Exit code 0. Output:
```
1
```

Command:
```
git rev-parse HEAD
```
Exit code 0. Output:
```
d1a43bd1c553b58124828bebc65fd2c0f1fed8bd
```

Command:
```
git status --short --untracked-files=no -- a_p_r_i_r_DEV CLAUDE_CODE_WORKING_FOLDER_TREE/inbox
```
Exit code 0. Output: no output at all.

### Step 2

Command:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" check-scratch "D:\DELETE_ME\a_p_r_i_r\T030"
```
Exit code 0. Output:
```
real path of the scratch folder: D:\DELETE_ME
folders on the way that are links or junctions: []
task folder: D:\DELETE_ME\a_p_r_i_r\T030 (not there yet)
SCRATCH CHECK PASS
```

### Step 3

Command:
```
mkdir -p "D:/DELETE_ME/a_p_r_i_r/T030" && git ls-files a_p_r_i_r_DEV > "D:/DELETE_ME/a_p_r_i_r/T030/files.txt" && "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" copy-dev "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality" "D:\DELETE_ME\a_p_r_i_r\T030\files.txt" "D:\DELETE_ME\a_p_r_i_r\T030\s_DEV" --families E_001,E_002
```
Exit code 0. Output:
```
files listed: 189; copied and read back: 87; families kept: ['E_001', 'E_002']
COPY PASS
```

### Step 4

Command:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" settings "D:\DELETE_ME\a_p_r_i_r\T030\s_DEV" DEV
```
Exit code 0. Output:
```
[environment]
role = DEV
[DEV]
tree_root = D:\DELETE_ME\a_p_r_i_r\T030\s_DEV
backup_root = D:\DELETE_ME\a_p_r_i_r\T030\backups\DEV
[QA]
tree_root = D:\DELETE_ME\a_p_r_i_r\T030\s_QA
backup_root = D:\DELETE_ME\a_p_r_i_r\T030\backups\QA
[PROD]
tree_root = D:\DELETE_ME\a_p_r_i_r\T030\s_PROD
backup_root = D:\DELETE_ME\a_p_r_i_r\T030\backups\PROD
every path above lies under D:\DELETE_ME
SETTINGS PASS
```
Checked by eye: all six paths begin `D:\DELETE_ME\a_p_r_i_r\T030\`.

### Step 5 (the `tail` lines only, as the task file says)

Command:
```
mkdir -p "D:/DELETE_ME/a_p_r_i_r/T030/tmp_env" "D:/DELETE_ME/a_p_r_i_r/T030/pip_cache" && ( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T030\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/create_venv.bat" > "D:/DELETE_ME/a_p_r_i_r/T030/venv_DEV_1.txt" 2>&1 ); echo "VENV EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T030/venv_DEV_1.txt"; tail -n 2 "D:/DELETE_ME/a_p_r_i_r/T030/venv_DEV_1.txt"
```
Exit code 0. Output:
```
Python VIRTUAL_ENV=D:\DELETE_ME\a_p_r_i_r\T030\s_DEV\.venv
VENV EXIT CODE 0
```

Command:
```
( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T030\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/install_upgrade_dependencies_into_venv.bat" INSTALL > "D:/DELETE_ME/a_p_r_i_r/T030/venv_DEV_2.txt" 2>&1 ); echo "PACKAGES EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T030/venv_DEV_2.txt"; tail -n 2 "D:/DELETE_ME/a_p_r_i_r/T030/venv_DEV_2.txt"
```
Exit code 0. Output:
```
[DEPS] SUCCESS. All 39 direct requirements installed; research compatibility tests remain required.
PACKAGES EXIT CODE 0
```

### Step 6

Command:
```
"D:\DELETE_ME\a_p_r_i_r\T030\s_DEV\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" invented "D:\DELETE_ME\a_p_r_i_r\T030\s_DEV" 115
```
Exit code 0. Output:
```
POWERBALL: invented results through draw 1259
OZLOTTO: invented results through draw 1589
INVENTED RESULTS WRITTEN
```

### Step 7

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Run_Research.bat" --no-update
```
Exit code 0. Output:
```
RESEARCH JOB - START - 2026-11-27 20:32 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T030\s_DEV
About to work: POWERBALL, OZLOTTO (results updater left out: --no-update)
POWERBALL: results on file through draw 1259; 4 methods in the tree
POWERBALL: worked through draw 1169 of 1259; so far 25 forecasts and 25 scores written
POWERBALL: worked through draw 1194 of 1259; so far 50 forecasts and 50 scores written
POWERBALL: worked through draw 1219 of 1259; so far 75 forecasts and 75 scores written
POWERBALL: worked through draw 1244 of 1259; so far 100 forecasts and 100 scores written
POWERBALL: finished. Results on file through draw 1259; written: 155 forecasts, 151 scores, 2 series files, 236 report files. prevailing OV-1: starts at draw 1260; no line yet
OZLOTTO: results on file through draw 1589; 4 methods in the tree
OZLOTTO: worked through draw 1499 of 1589; so far 25 forecasts and 25 scores written
OZLOTTO: worked through draw 1524 of 1589; so far 50 forecasts and 50 scores written
OZLOTTO: worked through draw 1549 of 1589; so far 75 forecasts and 75 scores written
OZLOTTO: worked through draw 1574 of 1589; so far 100 forecasts and 100 scores written
OZLOTTO: finished. Results on file through draw 1589; written: 155 forecasts, 151 scores, 2 series files, 236 report files. prevailing OV-1: starts at draw 1590; no line yet
Backup made: D:\DELETE_ME\a_p_r_i_r\T030\backups\DEV\DEV_20261127_203220_after_job.zip
RESEARCH JOB - END - 2026-11-27 20:32 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T030\s_DEV
POWERBALL: finished. Results on file through draw 1259; written: 155 forecasts, 151 scores, 2 series files, 236 report files. prevailing OV-1: starts at draw 1260; no line yet
OZLOTTO: finished. Results on file through draw 1589; written: 155 forecasts, 151 scores, 2 series files, 236 report files. prevailing OV-1: starts at draw 1590; no line yet
The job finished.
```

### Step 8

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Make_Installable.bat" ALL INFRA
```
Exit code 0. Output:
```
flagged: E_001/FULL_HISTORY_RAW_COUNTS_V1 (fingerprint b86315c8ce9e...)
flagged: E_002/RECUR_MEAN_ALL_V1 (fingerprint 6214b45fbcab...)
flagged: E_002/RECUR_MEAN_LAST8_V1 (fingerprint 4a9cec6cb75c...)
flagged: E_002/RECUR_MEDIAN_ALL_V1 (fingerprint 6be9053a6c02...)
flagged: the infrastructure (engine cfdb7ea64301..., updater 69f204cea1c2..., launchers 3dea97596ab5...)
Done.
```

### Step 9

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Create_Tree.bat" QA
```
Exit code 0. Output:
```
CREATE the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA, from DEV (D:\DELETE_ME\a_p_r_i_r\T030\s_DEV):
  copied: the infrastructure and 4 methods (53 files), and DEV's accepted results (4 files). The settings file was written last.
The QA tree is created. It has no Python environment and no results of its own yet. Next, in D:\DELETE_ME\a_p_r_i_r\T030\s_QA: run create_venv.bat, then install_upgrade_dependencies_into_venv.bat, then Run_Research.bat --no-update (its first job computes everything, which takes a while).
```

### Step 10

Command:
```
cat "D:/DELETE_ME/a_p_r_i_r/T030/s_QA/ENVIRONMENT.ini"
```
Exit code 0. Output:
```
; The settings of this tree (the simple scheme v0.2, section 3.1). Written by Create_Tree.bat in DEV.
; The same form in every tree; only the role differs. Never copy this file into another tree.
[environment]
role = QA
[DEV]
tree_root = D:\DELETE_ME\a_p_r_i_r\T030\s_DEV
backup_root = D:\DELETE_ME\a_p_r_i_r\T030\backups\DEV
[QA]
tree_root = D:\DELETE_ME\a_p_r_i_r\T030\s_QA
backup_root = D:\DELETE_ME\a_p_r_i_r\T030\backups\QA
[PROD]
tree_root = D:\DELETE_ME\a_p_r_i_r\T030\s_PROD
backup_root = D:\DELETE_ME\a_p_r_i_r\T030\backups\PROD
```

### Step 11 (the `tail` lines only, as the task file says)

Command:
```
( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T030\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T030/s_QA/create_venv.bat" > "D:/DELETE_ME/a_p_r_i_r/T030/venv_QA_1.txt" 2>&1 ); echo "VENV EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T030/venv_QA_1.txt"; tail -n 2 "D:/DELETE_ME/a_p_r_i_r/T030/venv_QA_1.txt"
```
Exit code 0. Output:
```
Python VIRTUAL_ENV=D:\DELETE_ME\a_p_r_i_r\T030\s_QA\.venv
VENV EXIT CODE 0
```

Command:
```
( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T030\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T030/s_QA/install_upgrade_dependencies_into_venv.bat" INSTALL > "D:/DELETE_ME/a_p_r_i_r/T030/venv_QA_2.txt" 2>&1 ); echo "PACKAGES EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T030/venv_QA_2.txt"; tail -n 2 "D:/DELETE_ME/a_p_r_i_r/T030/venv_QA_2.txt"
```
Exit code 0. Output:
```
[DEPS] SUCCESS. All 39 direct requirements installed; research compatibility tests remain required.
PACKAGES EXIT CODE 0
```

### Step 12

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_QA/Run_Research.bat" --no-update
```
Exit code 0. Output:
```
RESEARCH JOB - START - 2026-11-27 20:34 - the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA
About to work: POWERBALL, OZLOTTO (results updater left out: --no-update)
POWERBALL: results on file through draw 1259; 4 methods in the tree
POWERBALL: worked through draw 1169 of 1259; so far 25 forecasts and 25 scores written
POWERBALL: worked through draw 1194 of 1259; so far 50 forecasts and 50 scores written
POWERBALL: worked through draw 1219 of 1259; so far 75 forecasts and 75 scores written
POWERBALL: worked through draw 1244 of 1259; so far 100 forecasts and 100 scores written
POWERBALL: finished. Results on file through draw 1259; written: 155 forecasts, 151 scores, 2 series files, 236 report files. prevailing OV-1: starts at draw 1260; no line yet
OZLOTTO: results on file through draw 1589; 4 methods in the tree
OZLOTTO: worked through draw 1499 of 1589; so far 25 forecasts and 25 scores written
OZLOTTO: worked through draw 1524 of 1589; so far 50 forecasts and 50 scores written
OZLOTTO: worked through draw 1549 of 1589; so far 75 forecasts and 75 scores written
OZLOTTO: worked through draw 1574 of 1589; so far 100 forecasts and 100 scores written
OZLOTTO: finished. Results on file through draw 1589; written: 155 forecasts, 151 scores, 2 series files, 236 report files. prevailing OV-1: starts at draw 1590; no line yet
Backup made: D:\DELETE_ME\a_p_r_i_r\T030\backups\QA\QA_20261127_203503_after_job.zip
RESEARCH JOB - END - 2026-11-27 20:35 - the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA
POWERBALL: finished. Results on file through draw 1259; written: 155 forecasts, 151 scores, 2 series files, 236 report files. prevailing OV-1: starts at draw 1260; no line yet
OZLOTTO: finished. Results on file through draw 1589; written: 155 forecasts, 151 scores, 2 series files, 236 report files. prevailing OV-1: starts at draw 1590; no line yet
The job finished.
```

### Step 13

Command:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" plant-edit "D:\DELETE_ME\a_p_r_i_r\T030\s_DEV\src\methods\E_002\RECUR_MEDIAN_ALL_V1\method.py"
```
Exit code 0. Output:
```
D:\DELETE_ME\a_p_r_i_r\T030\s_DEV\src\methods\E_002\RECUR_MEDIAN_ALL_V1\method.py: SHA-256 27328fb40573707d... -> 608894810fdd4737...
EDIT PLANTED
```

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Make_Installable.bat" E_002/RECUR_MEDIAN_ALL_V1
```
Exit code 0. Output:
```
flagged: E_002/RECUR_MEDIAN_ALL_V1 (fingerprint 2d3fa40f8cbb...)
Done.
```

### Step 14

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Install.bat" QA --show
```
Exit code 0. Output:
```
INSTALL from DEV (D:\DELETE_ME\a_p_r_i_r\T030\s_DEV) into the QA tree (D:\DELETE_ME\a_p_r_i_r\T030\s_QA):
  replace: E_002/RECUR_MEDIAN_ALL_V1 (its results in the QA tree are made again)
--show: nothing was changed.
```

### Step 15

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Install.bat" QA
```
Exit code 0. Output:
```
INSTALL from DEV (D:\DELETE_ME\a_p_r_i_r\T030\s_DEV) into the QA tree (D:\DELETE_ME\a_p_r_i_r\T030\s_QA):
  replace: E_002/RECUR_MEDIAN_ALL_V1 (its results in the QA tree are made again)
Backup made of the QA tree: D:\DELETE_ME\a_p_r_i_r\T030\backups\QA\QA_20261127_203527_before_install.zip
Installed into the QA tree: 0 infrastructure files, 1 methods.
Now the QA tree's own research job (results updater left out), under the lock held:
RESEARCH JOB - START - 2026-11-27 20:35 - the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA
About to work: POWERBALL, OZLOTTO (results updater left out: --no-update)
REBUILD: POWERBALL: E_002/RECUR_MEDIAN_ALL_V1: its stored results were made by other files than the method has now
POWERBALL: results on file through draw 1259; 4 methods in the tree
POWERBALL: finished. Results on file through draw 1259; written: 13 forecasts, 12 scores, 0 series files, 0 report files. prevailing OV-1: starts at draw 1260; no line yet
REBUILD: OZLOTTO: E_002/RECUR_MEDIAN_ALL_V1: its stored results were made by other files than the method has now
OZLOTTO: results on file through draw 1589; 4 methods in the tree
OZLOTTO: finished. Results on file through draw 1589; written: 13 forecasts, 12 scores, 0 series files, 0 report files. prevailing OV-1: starts at draw 1590; no line yet
Backup made: D:\DELETE_ME\a_p_r_i_r\T030\backups\QA\QA_20261127_203534_after_job.zip
RESEARCH JOB - END - 2026-11-27 20:35 - the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA
POWERBALL: finished. Results on file through draw 1259; written: 13 forecasts, 12 scores, 0 series files, 0 report files. prevailing OV-1: starts at draw 1260; no line yet
OZLOTTO: finished. Results on file through draw 1589; written: 13 forecasts, 12 scores, 0 series files, 0 report files. prevailing OV-1: starts at draw 1590; no line yet
REBUILT (said again): POWERBALL: E_002/RECUR_MEDIAN_ALL_V1: its stored results were made by other files than the method has now
REBUILT (said again): OZLOTTO: E_002/RECUR_MEDIAN_ALL_V1: its stored results were made by other files than the method has now
The job finished.
Install finished: the QA tree has the software and its results are up to date with it.
```

### Step 16

Command:
```
ls "D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/records" "D:/DELETE_ME/a_p_r_i_r/T030/s_QA/records"
```
Exit code 0. Output:
```
D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/records:
JOB_LOG.jsonl

D:/DELETE_ME/a_p_r_i_r/T030/s_QA/records:
JOB_LOG.jsonl
```

### Step 17

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Install.bat" QA
```
Exit code 0. Output:
```
INSTALL from DEV (D:\DELETE_ME\a_p_r_i_r\T030\s_DEV) into the QA tree (D:\DELETE_ME\a_p_r_i_r\T030\s_QA):
  Nothing to install: the QA tree already has every part that is flagged in DEV.
```

### Step 18

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Create_Tree.bat" PROD
```
Exit code 0. Output:
```
CREATE the PROD tree at D:\DELETE_ME\a_p_r_i_r\T030\s_PROD, from DEV (D:\DELETE_ME\a_p_r_i_r\T030\s_DEV):
  copied: the infrastructure and 4 methods (53 files), and DEV's accepted results (4 files). The settings file was written last.
The PROD tree is created. It has no Python environment and no results of its own yet. Next, in D:\DELETE_ME\a_p_r_i_r\T030\s_PROD: run create_venv.bat, then install_upgrade_dependencies_into_venv.bat, then Run_Research.bat --no-update (its first job computes everything, which takes a while).
```

Command:
```
cat "D:/DELETE_ME/a_p_r_i_r/T030/s_PROD/ENVIRONMENT.ini"
```
Exit code 0. Output:
```
; The settings of this tree (the simple scheme v0.2, section 3.1). Written by Create_Tree.bat in DEV.
; The same form in every tree; only the role differs. Never copy this file into another tree.
[environment]
role = PROD
[DEV]
tree_root = D:\DELETE_ME\a_p_r_i_r\T030\s_DEV
backup_root = D:\DELETE_ME\a_p_r_i_r\T030\backups\DEV
[QA]
tree_root = D:\DELETE_ME\a_p_r_i_r\T030\s_QA
backup_root = D:\DELETE_ME\a_p_r_i_r\T030\backups\QA
[PROD]
tree_root = D:\DELETE_ME\a_p_r_i_r\T030\s_PROD
backup_root = D:\DELETE_ME\a_p_r_i_r\T030\backups\PROD
```

### Step 19 (the `tail` lines only, as the task file says)

Command:
```
( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T030\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T030/s_PROD/create_venv.bat" > "D:/DELETE_ME/a_p_r_i_r/T030/venv_PROD_1.txt" 2>&1 ); echo "VENV EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T030/venv_PROD_1.txt"; tail -n 2 "D:/DELETE_ME/a_p_r_i_r/T030/venv_PROD_1.txt"
```
Exit code 0. Output:
```
Python VIRTUAL_ENV=D:\DELETE_ME\a_p_r_i_r\T030\s_PROD\.venv
VENV EXIT CODE 0
```

Command:
```
( unset VIRTUAL_ENV; TMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' TEMP='D:\DELETE_ME\a_p_r_i_r\T030\tmp_env' PIP_CACHE_DIR='D:\DELETE_ME\a_p_r_i_r\T030\pip_cache' "D:/DELETE_ME/a_p_r_i_r/T030/s_PROD/install_upgrade_dependencies_into_venv.bat" INSTALL > "D:/DELETE_ME/a_p_r_i_r/T030/venv_PROD_2.txt" 2>&1 ); echo "PACKAGES EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T030/venv_PROD_2.txt"; tail -n 2 "D:/DELETE_ME/a_p_r_i_r/T030/venv_PROD_2.txt"
```
Exit code 0. Output:
```
[DEPS] SUCCESS. All 39 direct requirements installed; research compatibility tests remain required.
PACKAGES EXIT CODE 0
```

### Step 20

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_PROD/Run_Research.bat" --no-update
```
Exit code 0. Output:
```
RESEARCH JOB - START - 2026-11-27 20:38 - the PROD tree at D:\DELETE_ME\a_p_r_i_r\T030\s_PROD
About to work: POWERBALL, OZLOTTO (results updater left out: --no-update)
POWERBALL: results on file through draw 1259; 4 methods in the tree
POWERBALL: worked through draw 1169 of 1259; so far 25 forecasts and 25 scores written
POWERBALL: worked through draw 1194 of 1259; so far 50 forecasts and 50 scores written
POWERBALL: worked through draw 1219 of 1259; so far 75 forecasts and 75 scores written
POWERBALL: worked through draw 1244 of 1259; so far 100 forecasts and 100 scores written
POWERBALL: finished. Results on file through draw 1259; written: 155 forecasts, 151 scores, 2 series files, 236 report files. prevailing OV-1: starts at draw 1260; no line yet
OZLOTTO: results on file through draw 1589; 4 methods in the tree
OZLOTTO: worked through draw 1499 of 1589; so far 25 forecasts and 25 scores written
OZLOTTO: worked through draw 1524 of 1589; so far 50 forecasts and 50 scores written
OZLOTTO: worked through draw 1549 of 1589; so far 75 forecasts and 75 scores written
OZLOTTO: worked through draw 1574 of 1589; so far 100 forecasts and 100 scores written
OZLOTTO: finished. Results on file through draw 1589; written: 155 forecasts, 151 scores, 2 series files, 236 report files. prevailing OV-1: starts at draw 1590; no line yet
Backup made: D:\DELETE_ME\a_p_r_i_r\T030\backups\PROD\PROD_20261127_203817_after_job.zip
RESEARCH JOB - END - 2026-11-27 20:38 - the PROD tree at D:\DELETE_ME\a_p_r_i_r\T030\s_PROD
POWERBALL: finished. Results on file through draw 1259; written: 155 forecasts, 151 scores, 2 series files, 236 report files. prevailing OV-1: starts at draw 1260; no line yet
OZLOTTO: finished. Results on file through draw 1589; written: 155 forecasts, 151 scores, 2 series files, 236 report files. prevailing OV-1: starts at draw 1590; no line yet
The job finished.
```

### Step 21

Command:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" plant-edit "D:\DELETE_ME\a_p_r_i_r\T030\s_DEV\src\methods\E_001\FULL_HISTORY_RAW_COUNTS_V1\method.py"
```
Exit code 0. Output:
```
D:\DELETE_ME\a_p_r_i_r\T030\s_DEV\src\methods\E_001\FULL_HISTORY_RAW_COUNTS_V1\method.py: SHA-256 a5fb2075c5e78933... -> d20ee53688cfc1f7...
EDIT PLANTED
```

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Install.bat" PROD --show
```
Exit code 0. Output:
```
INSTALL from DEV (D:\DELETE_ME\a_p_r_i_r\T030\s_DEV) into the PROD tree (D:\DELETE_ME\a_p_r_i_r\T030\s_PROD):
  NOT INSTALLED: E_001/FULL_HISTORY_RAW_COUNTS_V1: in DEV it is flagged, but its flag is older than its files; Make_Installable.bat makes the flag.
  Nothing to install: the PROD tree already has every part that is flagged in DEV.
--show: nothing was changed.
```

### Step 22

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_QA/Backup.bat"
```
Exit code 0. Output:
```
Backup made of the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA: D:\DELETE_ME\a_p_r_i_r\T030\backups\QA\QA_20261127_203836_on_demand.zip
```

### Step 23

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Retire.bat" E_002/RECUR_MEAN_LAST8_V1 rehearsal of a retirement
```
Exit code 0. Output:
```
Backup made of the DEV tree: D:\DELETE_ME\a_p_r_i_r\T030\backups\DEV\DEV_20261127_203841_before_retire.zip
Backup made of the QA tree: D:\DELETE_ME\a_p_r_i_r\T030\backups\QA\QA_20261127_203841_before_retire.zip
Backup made of the PROD tree: D:\DELETE_ME\a_p_r_i_r\T030\backups\PROD\PROD_20261127_203841_before_retire.zip
  DEV: E_002/RECUR_MEAN_LAST8_V1 is retired from POWERBALL draw 1260, OZLOTTO draw 1590. That tree's next research job drops what it had from there on and remakes the reports.
  QA: E_002/RECUR_MEAN_LAST8_V1 is retired from POWERBALL draw 1260, OZLOTTO draw 1590. That tree's next research job drops what it had from there on and remakes the reports.
  PROD: E_002/RECUR_MEAN_LAST8_V1 is retired from POWERBALL draw 1260, OZLOTTO draw 1590. That tree's next research job drops what it had from there on and remakes the reports.
Retired: E_002/RECUR_MEAN_LAST8_V1 (rehearsal of a retirement). In DEV the file I_AM_RETIRED beside the method is kept in Git: commit it. Deleting the file in a tree brings the method back there.
```

### Step 24

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_PROD/Run_Research.bat" --no-update
```
Exit code 0. Output:
```
RESEARCH JOB - START - 2026-11-27 20:38 - the PROD tree at D:\DELETE_ME\a_p_r_i_r\T030\s_PROD
About to work: POWERBALL, OZLOTTO (results updater left out: --no-update)
REBUILD: POWERBALL: E_002/RECUR_MEAN_LAST8_V1: retired from draw 1260: 1 forecasts and 0 scores for that draw or later dropped
POWERBALL: results on file through draw 1259; 4 methods in the tree
POWERBALL: finished. Results on file through draw 1259; written: 0 forecasts, 0 scores, 0 series files, 232 report files. prevailing OV-1: starts at draw 1260; no line yet
REBUILD: OZLOTTO: E_002/RECUR_MEAN_LAST8_V1: retired from draw 1590: 1 forecasts and 0 scores for that draw or later dropped
OZLOTTO: results on file through draw 1589; 4 methods in the tree
OZLOTTO: finished. Results on file through draw 1589; written: 0 forecasts, 0 scores, 0 series files, 232 report files. prevailing OV-1: starts at draw 1590; no line yet
Backup made: D:\DELETE_ME\a_p_r_i_r\T030\backups\PROD\PROD_20261127_203854_after_job.zip
RESEARCH JOB - END - 2026-11-27 20:38 - the PROD tree at D:\DELETE_ME\a_p_r_i_r\T030\s_PROD
POWERBALL: finished. Results on file through draw 1259; written: 0 forecasts, 0 scores, 0 series files, 232 report files. prevailing OV-1: starts at draw 1260; no line yet
OZLOTTO: finished. Results on file through draw 1589; written: 0 forecasts, 0 scores, 0 series files, 232 report files. prevailing OV-1: starts at draw 1590; no line yet
REBUILT (said again): POWERBALL: E_002/RECUR_MEAN_LAST8_V1: retired from draw 1260: 1 forecasts and 0 scores for that draw or later dropped
REBUILT (said again): OZLOTTO: E_002/RECUR_MEAN_LAST8_V1: retired from draw 1590: 1 forecasts and 0 scores for that draw or later dropped
The job finished.
```

### Step 25

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Copy_From_PROD.bat" both QA
```
Exit code 0. Output:
```
COPY FROM PROD (D:\DELETE_ME\a_p_r_i_r\T030\s_PROD) into the QA tree (D:\DELETE_ME\a_p_r_i_r\T030\s_QA): both.
Backup made of the QA tree: D:\DELETE_ME\a_p_r_i_r\T030\backups\QA\QA_20261127_203901_before_copy_from_PROD.zip
  software: the QA tree's src folder and launchers are now PROD's.
  data: 4 files of accepted results and 497 files of computed results are now PROD's.
Now the QA tree's own research job (results updater left out), under the lock held:
RESEARCH JOB - START - 2026-11-27 20:39 - the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA
About to work: POWERBALL, OZLOTTO (results updater left out: --no-update)
POWERBALL: results on file through draw 1259; 4 methods in the tree
POWERBALL: finished. Results on file through draw 1259; written: 0 forecasts, 0 scores, 0 series files, 236 report files. prevailing OV-1: starts at draw 1260; no line yet
OZLOTTO: results on file through draw 1589; 4 methods in the tree
OZLOTTO: finished. Results on file through draw 1589; written: 0 forecasts, 0 scores, 0 series files, 236 report files. prevailing OV-1: starts at draw 1590; no line yet
Backup made: D:\DELETE_ME\a_p_r_i_r\T030\backups\QA\QA_20261127_203909_after_job.zip
RESEARCH JOB - END - 2026-11-27 20:39 - the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA
POWERBALL: finished. Results on file through draw 1259; written: 0 forecasts, 0 scores, 0 series files, 236 report files. prevailing OV-1: starts at draw 1260; no line yet
OZLOTTO: finished. Results on file through draw 1589; written: 0 forecasts, 0 scores, 0 series files, 236 report files. prevailing OV-1: starts at draw 1590; no line yet
The job finished.
Copy finished: the QA tree's results are up to date with what it now holds.
```

### Step 26

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Restore.bat" QA "$("E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" one-backup "D:\DELETE_ME\a_p_r_i_r\T030\backups\QA" _on_demand.zip)"
```
Exit code 0. Output:
```
RESTORE the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA from D:\DELETE_ME\a_p_r_i_r\T030\backups\QA\QA_20261127_203836_on_demand.zip:
Backup made of the QA tree: D:\DELETE_ME\a_p_r_i_r\T030\backups\QA\QA_20261127_203918_before_restore.zip
  unpacked: 563 files into a fresh folder.
  the tree as it was is kept at D:\DELETE_ME\a_p_r_i_r\T030\s_QA_set_aside_20261127_203918. Nothing can run in it; delete it by hand when it is no longer wanted.
Restored: the QA tree at D:\DELETE_ME\a_p_r_i_r\T030\s_QA is now as the backup holds it. It has no Python environment: in that folder run create_venv.bat, then install_upgrade_dependencies_into_venv.bat, then Run_Research.bat --no-update.
```

### Step 27

Command:
```
ls "D:/DELETE_ME/a_p_r_i_r/T030"
```
Exit code 0. Output:
```
backups
files.txt
pip_cache
s_DEV
s_PROD
s_QA
s_QA_set_aside_20261127_203918
tmp_env
venv_DEV_1.txt
venv_DEV_2.txt
venv_PROD_1.txt
venv_PROD_2.txt
venv_QA_1.txt
venv_QA_2.txt
```

Command:
```
cat "D:/DELETE_ME/a_p_r_i_r/T030/s_QA/ENVIRONMENT.ini"
```
Exit code 0. Output:
```
; The settings of this tree (the simple scheme v0.2, section 3.1). Written by Create_Tree.bat in DEV.
; The same form in every tree; only the role differs. Never copy this file into another tree.
[environment]
role = QA
[DEV]
tree_root = D:\DELETE_ME\a_p_r_i_r\T030\s_DEV
backup_root = D:\DELETE_ME\a_p_r_i_r\T030\backups\DEV
[QA]
tree_root = D:\DELETE_ME\a_p_r_i_r\T030\s_QA
backup_root = D:\DELETE_ME\a_p_r_i_r\T030\backups\QA
[PROD]
tree_root = D:\DELETE_ME\a_p_r_i_r\T030\s_PROD
backup_root = D:\DELETE_ME\a_p_r_i_r\T030\backups\PROD
```

### Step 28 (a refusal planted on purpose; the refusal is this step's PASS)

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_QA/Run_Research.bat" --no-update
```
Exit code 2. Output:
```
REFUSED: this tree's Python was not found at D:\DELETE_ME\a_p_r_i_r\T030\s_QA\.venv\Scripts\python.exe. Build the tree's .venv first. 
```

### Step 29 (a refusal planted on purpose; the refusal is this step's PASS)

Command:
```
"$(ls -d D:/DELETE_ME/a_p_r_i_r/T030/s_QA_set_aside_*)/Run_Research.bat" --no-update
```
Exit code 2. Output:
```
REFUSED: D:\DELETE_ME\a_p_r_i_r\T030\s_QA_set_aside_20261127_203918\ENVIRONMENT.ini [environment] role: the file says QA, but the folder it lies in is named "s_QA_set_aside_20261127_203918", which does not end with QA. This folder is not the tree its file says: nothing is done here. (A tree that was copied or renamed, or a settings file from another tree, is refused.)
```

### Step 30 (a refusal planted on purpose; the refusal is this step's PASS)

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Create_Tree.bat" QA
```
Exit code 2. Output:
```
REFUSED: D:\DELETE_ME\a_p_r_i_r\T030\s_QA already holds something. A tree is created only into a folder that is absent or empty; nothing was changed. If that folder is a QA tree, use Install.bat; if it is the rest of a creation that did not finish, delete it by hand and run Create_Tree.bat QA again.
```

### Step 31

Command:
```
"D:/DELETE_ME/a_p_r_i_r/T030/s_DEV/Who_Uses.bat" _shared/recurrence_gaps_v1.py
```
Exit code 0. Output:
```
E_002/RECUR_MEAN_ALL_V1    uses _shared/recurrence_gaps_v1.py
E_002/RECUR_MEAN_LAST8_V1    uses _shared/recurrence_gaps_v1.py
E_002/RECUR_MEDIAN_ALL_V1    uses _shared/recurrence_gaps_v1.py
3 of 4 methods use "_shared/recurrence_gaps_v1.py". A change to a helper changes the fingerprint of every method that uses it: each is rebuilt.
```

## Clean-up

One folder was created under `D:\DELETE_ME\`:

- `D:\DELETE_ME\a_p_r_i_r\T030`, holding the three scratch trees (`s_DEV`, `s_QA`, `s_PROD`), the tree set aside by the restore (`s_QA_set_aside_20261127_203918`), their backup folders (`backups\DEV`, `backups\QA`, `backups\PROD`), the temporary and package-cache folders (`tmp_env`, `pip_cache`), `files.txt` and the six `venv_*.txt` files.

**It was not removed.** The task file says this task does not delete its scratch folder; the project owner deletes it by hand when he wishes.

Nothing was copied or moved out of `D:\DELETE_ME\`: what the commands printed is in this report, and nothing else.

## Deviations

None in what was run. All 31 steps ran in order, exactly as the task file gives them, and each printed what the task file expects. The three planted refusals (steps 28, 29 and 30) each printed their expected `REFUSED` line with exit code 2, which is their PASS.

One note on how this report was written, not on a step: the first attempt to write this file with a shell heredoc was refused by the permission settings, so it was written with the runner's own file-writing tool instead, into `CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\` as section 3 allows. No step of the task was affected.

## Observations

- Step 3 copied the counts the task file names as those at its writing: files listed 189, copied and read back 87. Steps 9 and 18 each copied 53 files, also as named.
- Step 15's install printed two `REBUILD:` lines (one per game) before the `REBUILT (said again):` lines the task file names, and the install's child job wrote 13 forecasts and 12 scores in each game.
- Step 25's copy printed `data: 4 files of accepted results and 497 files of computed results are now PROD's.`
- Steps 5, 11 and 19 each ended with `[DEPS] SUCCESS. All 39 direct requirements installed; research compatibility tests remain required.`
- No `TREE.lock` was present in either tree at step 16.
- Step 28's `REFUSED` line ends with a trailing space, copied here as printed.
