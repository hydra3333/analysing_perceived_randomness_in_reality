# TASK_T031 - the comparison of the two engines on the accepted results, on Windows, in the scratch folder on D:

**Task ID:** T031. **Date:** 27 November 2026. **Author:** the Claude web chat. **Rulebook v0.8 (needs it ratified and installed; step 1 checks), including section 2A item 7(b), which this task uses.** **Section 2A applies to steps 3 to 12, in the folder `D:\DELETE_ME\a_p_r_i_r\T031`** (new; this task creates it). **Run it only after the owner has made DEV's first fill** (item 3 of the work order, decision log entry 365), with the software of the commit this task checks.

**Purpose.** Item 4 of the owner's work order: the proof of the simple scheme's section 9, made on the owner's PC. From the same accepted results, the simplified engine must give the same forecasts, scores, both OV-1 series and report files (through the declared wording changes) as the frozen engine at the top level of the repository. The simplified engine's side is DEV's own first fill, computed in DEV with DEV's own Python; this task copies it into the scratch folder by reading (the owner's decision, entry 365: nothing leaves the scratch folder, and the comparison's artificial alignment never touches DEV). The frozen engine's side is computed here, **with the real DEV tree's own Python as the interpreter** (entry 366), so that both sides are computed in the same environment.

**The restrictions of entry 366 on that Python, every one of them kept by every step below:** always `-I -B`; the working folder, `TMP`, `TEMP` and every output inside `D:\DELETE_ME\a_p_r_i_r\T031`; no package installed or upgraded (no `pip`, no `-m pip`); nothing of DEV or of its environment changed; no updater run (every research job of either engine here is started with `--no-update`).

**What it does not do.** It writes nothing in the real DEV tree and never reads its `ENVIRONMENT.ini`; it reads only DEV's software as committed (through `git ls-files`) and, by copying, DEV's `source_data` and `results\research`. It changes nothing in the main repository (only this task's report is committed there) and nothing in any `.venv`. It ends no process. It changes no date, time or time zone. **It copies no figure of the results into the report:** only the exit codes, the start and end lines of each job and the comparison's SAME or DIFFERENT lines, which hold counts only.

**Before the owner starts this task (the owner, not the runner):** DEV's first fill has finished (`Run_Research.bat --no-update` in DEV, ending `The job finished.`); `git pull --ff-only` has been done and this is a new Claude Code conversation; nothing of the project is running. The task takes about 60 to 75 minutes, most of it the frozen engine's first fill (step 6), and writes about 1 GB into the scratch folder.

## Owner options

- None.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| DEVTREE (the real DEV tree; read only) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV` |
| DPY (the real DEV tree's own Python; section 2A item 7(b)) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe` |
| HELPER (read only) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py` |
| SCRATCH (this task's folder) | `D:\DELETE_ME\a_p_r_i_r\T031` |
| NEW, FROZEN (the two trees) | `D:\DELETE_ME\a_p_r_i_r\T031\new_DEV`, `D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV` |
| TOOL (the comparison tool, in the new tree) | `D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py` |

Run each command in Git Bash exactly as written. The commands that use DPY begin by changing to SCRATCH and set `TMP` and `TEMP` to `D:\DELETE_ME\a_p_r_i_r\T031\tmp` for that command alone. On anything other than the expected lines and exit code of a step: **STOP**, record the output, and go to step 13. Never retry, repair or reorder a step. **After a STOP, leave `D:\DELETE_ME\a_p_r_i_r\T031` exactly as it is.** This task does not delete its scratch folder; the owner deletes it by hand when he wishes.

## Steps

**1. The rulebook in force, and the repository's state.**
```
grep -c "^\*\*Version:\*\* v0.8" CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md
git rev-parse HEAD
git status --short --untracked-files=no -- a_p_r_i_r_DEV/src a_p_r_i_r_DEV/deploy CLAUDE_CODE_WORKING_FOLDER_TREE/inbox
```
Expected: `1`; one commit hash (record it); then no output at all (DEV's software is as committed; DEV's own `IN_PLACE_SINCE` files may be uncommitted, and are not looked at). Anything else: STOP.

**2. The real DEV tree's own Python** (only its version and place are printed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B -c "import sys, numpy; print(sys.version); print(sys.prefix); print('numpy', numpy.__version__)"
```
Expected: a Python version; `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv`; a numpy version.

**3. The scratch folder is an ordinary folder on D:, and this task's folder is new.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" check-scratch "D:\DELETE_ME\a_p_r_i_r\T031"
```
Expected: `SCRATCH CHECK PASS`; exit code 0.

**4. The two trees** (DEV's committed software; DEV's `source_data` and `results\research` copied by reading; the frozen engine from the repository's top level; then the check that DEV's results were made by the engine of this commit).
```
mkdir -p "D:/DELETE_ME/a_p_r_i_r/T031/tmp" && git ls-files a_p_r_i_r_DEV > "D:/DELETE_ME/a_p_r_i_r/T031/files.txt" && cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" comparison-trees "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV" "D:\DELETE_ME\a_p_r_i_r\T031\files.txt" "D:\DELETE_ME\a_p_r_i_r\T031"
```
Expected: `COPY PASS`; `source_data: 4 files copied by reading from the real DEV tree`; `results/research: <number> files copied by reading from the real DEV tree`; `source_data: 4 files copied into the frozen tree`; a line `engine copied: ...; engine the copied results were made with: ...` with the two the same; `COMPARISON TREES PASS`; exit code 0. **A line `STOP: the results copied from the real DEV tree were not made by the engine of this commit.` means DEV's first fill was made with other software than this commit's: STOP** (the owner then fills DEV again with this commit's software, or the web chat is asked).

**5. What the two engines' code is** (a listing; this step does not stop the task unless its exit code is not 0).
```
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" code "D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV" "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV"
```
Expected: the tool's listing of each source file as the same, the same but for comments, changed, or in one tree only; exit code 0. Copy it whole into the report.

**6. (long, about 50 minutes) The frozen engine's first fill.**
```
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" run "D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T031/run_frozen_1.txt" 2>&1; echo "EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T031/run_frozen_1.txt"; grep -E "^(RESEARCH JOB - (START|END)|About to work|The job finished|A STOP is a STOP|REFUSED|EXIT CODE)" "D:/DELETE_ME/a_p_r_i_r/T031/run_frozen_1.txt"
```
Expected: `RESEARCH JOB - START - ...`, `About to work: POWERBALL, OZLOTTO (results step left out: --no-update)`, `RESEARCH JOB - END - ...`, `The job finished.`, `EXIT CODE 0`. Show only these lines in the report.

**7. The simplified engine's tree: its job with nothing new to compute.**
```
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" run "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T031/run_new_1.txt" 2>&1; echo "EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T031/run_new_1.txt"; grep -E "^(RESEARCH JOB - (START|END)|About to work|REBUILD|The job finished|A STOP is a STOP|REFUSED|EXIT CODE)" "D:/DELETE_ME/a_p_r_i_r/T031/run_new_1.txt"
```
Expected: `RESEARCH JOB - START - ... - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T031\new_DEV`, `About to work: ...`, `RESEARCH JOB - END - ...`, `The job finished.`, `EXIT CODE 0`, and **no line beginning `REBUILD`** (the results copied were made by this engine). A `REBUILD` line: STOP.

**8. The same starting draws for the second OV-1 series in both trees** (the comparison's alignment; it changes `IN_PLACE_SINCE` in the two scratch trees only).
```
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" align "D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV" "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV"; echo "EXIT CODE $?"
```
Expected: `EXIT CODE 0`. Copy the output whole into the report.

**9. The frozen engine's job again, from the aligned starting draws.**
```
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" run "D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T031/run_frozen_2.txt" 2>&1; echo "EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T031/run_frozen_2.txt"; grep -E "^(RESEARCH JOB - (START|END)|The job finished|A STOP is a STOP|REFUSED|EXIT CODE)" "D:/DELETE_ME/a_p_r_i_r/T031/run_frozen_2.txt"
```
Expected: the start and end lines, `The job finished.`, `EXIT CODE 0`.

**10. The simplified engine's job again, from the aligned starting draws.**
```
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" run "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T031/run_new_2.txt" 2>&1; echo "EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T031/run_new_2.txt"; grep -E "^(RESEARCH JOB - (START|END)|The job finished|A STOP is a STOP|REFUSED|EXIT CODE)" "D:/DELETE_ME/a_p_r_i_r/T031/run_new_2.txt"
```
Expected: the start and end lines, `The job finished.`, `EXIT CODE 0`.

**11. The comparison.**
```
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" trees "D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV" "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV"; echo "EXIT CODE $?"
```
Expected: twelve lines beginning `SAME` (six for each game: the methods that have results; every forecast and every score; the second OV-1 series; the series over all draws; the names of the report files; every report file, byte for byte, with its count of declared wording replacements), then `RESULT: SAME: the frozen engine at ... and the simplified engine at ...`, then `EXIT CODE 0`. Copy the output whole into the report. **A line beginning `DIFFERENT`, or `RESULT: DIFFERENT`: STOP** (the scratch folder is then left exactly as it is, for the web chat to ask what it holds).

**12. The temporary folder.**
```
ls -A "D:/DELETE_ME/a_p_r_i_r/T031/tmp" | wc -l
```
Record the number (not a STOP).

**13. The report.** Write `outbox\REPORT_T031.md` in the format of `outbox\README.md`, with: the commit of step 1; each step's command, exit code and output as said above (steps 6, 7, 9 and 10: the lines their `grep` shows; nothing else of those files); and, at the end, the folder this task created under `D:\DELETE_ME\` (`D:\DELETE_ME\a_p_r_i_r\T031`, with `new_DEV`, `frozen_DEV`, `tmp` and the text files), saying that it was not removed.

**14. Finish.** Commit the report:
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T031
```
Then tell the project owner the result line, the report's path, and "please push".
