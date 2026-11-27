# REPORT_T031 - the comparison of the two engines on the accepted results, on Windows, in the scratch folder on D:

RESULT: PASS

- Task file: inbox/TASK_T031.md at main-repository commit 0c8d033ae1774bafa6c351cf66e12720710c2957
- Run by: Claude Code (local runner), 28 November 2026, 06:50 to 07:52 local machine time
- Owner options used: none (the task file offers none)
- Machine: Windows 11 Pro 10.0.26300. The main venv's Python at
  `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe`
  was used for step 2 and step 14 only. Every other command used the real DEV tree's own Python,
  Python 3.15.2 at
  `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe`
  (section 2A item 7(b)), always with `-I -B`, always with the working folder, `TMP`, `TEMP` and every
  output inside `D:\DELETE_ME\a_p_r_i_r\T031`.

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | the rulebook in force, and the repository's state | 0 | `1`; commit 0c8d033ae1774bafa6c351cf66e12720710c2957; no output from either git status |
| 2 | the scratch folder is an ordinary folder on D:, and this task's folder is new | 0 | SCRATCH CHECK PASS |
| 3 | the real DEV tree's own Python | 0 | Python 3.15.2; prefix the DEV tree's .venv; numpy 2.5.5 |
| 4 | the two trees | 0 | COPY PASS; COMPARISON TREES PASS; the two engine fingerprints the same |
| 4b | the two trees' settings files | 0 | eleven lines then four lines; every path begins `D:\DELETE_ME\a_p_r_i_r\T031\` |
| 5 | what the two engines' code is | 0 | the listing (below) |
| 6 | the frozen engine's first fill | 0 | The job finished.; EXIT CODE 0 |
| 7 | the simplified engine's tree: its job with nothing new to compute | 0 | The job finished.; EXIT CODE 0; no REBUILD line |
| 8 | the same starting draws for the second OV-1 series in both trees | 0 | 40 status files and 40 IN_PLACE_SINCE files given the same draws |
| 9 | the frozen engine's job again, from the aligned starting draws | 0 | The job finished.; EXIT CODE 0 |
| 10 | the simplified engine's job again, from the aligned starting draws | 0 | The job finished.; EXIT CODE 0 |
| 11 | the comparison | 0 | twelve SAME lines; RESULT: SAME |
| 12 | the temporary folder | 0 | 0 |

## Outputs

### Step 1

Commands:

```text
grep -c "^\*\*Version:\*\* v0.8" CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md
git rev-parse HEAD
git status --short -- a_p_r_i_r_DEV/src a_p_r_i_r_DEV/deploy CLAUDE_CODE_WORKING_FOLDER_TREE/inbox
git status --short -- src deploy/INFRA_MANIFEST.ini Run_Research.bat Withdraw_Variant.bat
```

Output of the first two:

```text
1
0c8d033ae1774bafa6c351cf66e12720710c2957
```

Both `git status --short` commands printed no output at all.

### Step 2

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" check-scratch "D:\DELETE_ME\a_p_r_i_r\T031"
```

Output:

```text
real path of the scratch folder: D:\DELETE_ME
folders on the way that are links or junctions: []
task folder: D:\DELETE_ME\a_p_r_i_r\T031 (not there yet)
SCRATCH CHECK PASS
```

Exit code 0.

### Step 3

Command:

```text
mkdir -p "D:/DELETE_ME/a_p_r_i_r/T031/tmp" && cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B -c "import sys, numpy; print(sys.version); print(sys.prefix); print('numpy', numpy.__version__)"
```

Output:

```text
3.15.2 (tags/v3.15.2:5e58eaa, Oct 25 2026, 17:27:03) [MSC v.1951 64 bit (AMD64)]
E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv
numpy 2.5.5
```

Exit code 0.

### Step 4

Command:

```text
git ls-files a_p_r_i_r_DEV > "D:/DELETE_ME/a_p_r_i_r/T031/files.txt" && cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\REHEARSAL_HELPER.py" comparison-trees "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV" "D:\DELETE_ME\a_p_r_i_r\T031\files.txt" "D:\DELETE_ME\a_p_r_i_r\T031"
```

Output:

```text
files listed: 229; copied and read back: 229; families kept: all
COPY PASS
source_data: 4 files copied by reading from the real DEV tree
results/research: 1543 files copied by reading from the real DEV tree
source_data: 4 files copied into the frozen tree
engine copied: cfdb7ea643016591...; engine the copied results were made with: cfdb7ea643016591...
COMPARISON TREES PASS
```

Exit code 0. The two fingerprints on the `engine copied:` line are the same, so the results copied
from the real DEV tree were made by the engine of the commit of step 1.

### Step 4b

Command:

```text
cat "D:/DELETE_ME/a_p_r_i_r/T031/new_DEV/ENVIRONMENT.ini" "D:/DELETE_ME/a_p_r_i_r/T031/frozen_DEV/ENVIRONMENT.ini"
```

Output:

```text
[environment]
role = DEV
[DEV]
tree_root = D:\DELETE_ME\a_p_r_i_r\T031\new_DEV
backup_root = D:\DELETE_ME\a_p_r_i_r\T031\backups\DEV
[QA]
tree_root = D:\DELETE_ME\a_p_r_i_r\T031\none_QA
backup_root = D:\DELETE_ME\a_p_r_i_r\T031\backups\QA
[PROD]
tree_root = D:\DELETE_ME\a_p_r_i_r\T031\none_PROD
backup_root = D:\DELETE_ME\a_p_r_i_r\T031\backups\PROD
[environment]
role = DEV
tree_root = D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV
venv_dir = D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV\.venv
```

Exit code 0. Every path in both files begins `D:\DELETE_ME\a_p_r_i_r\T031\`.

### Step 5

Command:

```text
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" code "D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV" "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV"
```

Output, whole:

```text
the same bytes: 14 engine files, 119 method and helper files
    evaluation/__init__.py
    evaluation/divisions.py
    methods/_common/__init__.py
    methods/_common/canonical_encoding.py
    methods/_common/contract_forecast.py
    methods/_common/contract_records.py
    methods/_common/contract_task.py
    methods/_common/contract_vocab.py
    methods/_common/game_profiles.py
    research/__init__.py
    research/forecast_engine.py
    research/method_api.py
    research/ov1_numeric.py
    research/readout.py
the same program (comments and docstrings differ): 3 engine files, 0 method and helper files
    research/reader.py
    research/scoring.py
    research/windows_text.py
changed: 9 engine files, 0 method and helper files
    research/code_identity.py
    research/game_state.py
    research/ov1_ledger.py
    research/reports.py
    research/research_job.py
    research/settings.py
    research/variant_folders.py
    research/variant_lists.py
    research_command.py
only in the simplified engine: 5 engine files, 0 method and helper files
    research/backup.py
    research/method_flags.py
    research/tree_lock.py
    updater/__init__.py
    updater/results_updater.py
only in the frozen tree: 45 engine files, 9 method and helper files
    research/derived_check.py
    research/job_lock.py
    research/results_step.py
    research/status_file.py
    research/withdraw.py
```

Exit code 0.

### Step 6

Command:

```text
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" run "D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T031/run_frozen_1.txt" 2>&1; echo "EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T031/run_frozen_1.txt"; grep -E "^(RESEARCH JOB - (START|END)|About to work|The job finished|A STOP is a STOP|REFUSED|EXIT CODE)" "D:/DELETE_ME/a_p_r_i_r/T031/run_frozen_1.txt"
```

The lines the `grep` showed, and nothing else of that file:

```text
RESEARCH JOB - START - 2026-11-28 06:56 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV
About to work: POWERBALL, OZLOTTO (results step left out: --no-update)
RESEARCH JOB - END - 2026-11-28 07:41 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV
The job finished.
EXIT CODE 0
```

Exit code 0.

### Step 7

Command:

```text
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" run "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T031/run_new_1.txt" 2>&1; echo "EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T031/run_new_1.txt"; grep -E "^(RESEARCH JOB - (START|END)|About to work|REBUILD|The job finished|A STOP is a STOP|REFUSED|EXIT CODE)" "D:/DELETE_ME/a_p_r_i_r/T031/run_new_1.txt"
```

The lines the `grep` showed, and nothing else of that file:

```text
RESEARCH JOB - START - 2026-11-28 07:41 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T031\new_DEV
About to work: POWERBALL, OZLOTTO (results updater left out: --no-update)
RESEARCH JOB - END - 2026-11-28 07:44 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T031\new_DEV
The job finished.
EXIT CODE 0
```

Exit code 0. No line beginning `REBUILD`.

### Step 8

Command:

```text
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" align "D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV" "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV"
```

Output, whole:

```text
frozen tree: 40 status files given their first counted draws
new tree: 40 IN_PLACE_SINCE files given the same draws
```

Exit code 0.

### Step 9

Command:

```text
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" run "D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T031/run_frozen_2.txt" 2>&1; echo "EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T031/run_frozen_2.txt"; grep -E "^(RESEARCH JOB - (START|END)|The job finished|A STOP is a STOP|REFUSED|EXIT CODE)" "D:/DELETE_ME/a_p_r_i_r/T031/run_frozen_2.txt"
```

The lines the `grep` showed, and nothing else of that file:

```text
RESEARCH JOB - START - 2026-11-28 07:44 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV
RESEARCH JOB - END - 2026-11-28 07:47 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV
The job finished.
EXIT CODE 0
```

Exit code 0.

### Step 10

Command:

```text
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" run "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T031/run_new_2.txt" 2>&1; echo "EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T031/run_new_2.txt"; grep -E "^(RESEARCH JOB - (START|END)|The job finished|A STOP is a STOP|REFUSED|EXIT CODE)" "D:/DELETE_ME/a_p_r_i_r/T031/run_new_2.txt"
```

The lines the `grep` showed, and nothing else of that file:

```text
RESEARCH JOB - START - 2026-11-28 07:48 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T031\new_DEV
RESEARCH JOB - END - 2026-11-28 07:51 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T031\new_DEV
The job finished.
EXIT CODE 0
```

Exit code 0.

### Step 11

Command:

```text
cd "D:/DELETE_ME/a_p_r_i_r/T031" && TMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' TEMP='D:\DELETE_ME\a_p_r_i_r\T031\tmp' "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV\deploy\compare_with_frozen.py" trees "D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV" "D:\DELETE_ME\a_p_r_i_r\T031\new_DEV"
```

Output, whole:

```text
SAME       POWERBALL: the methods that have results (40 and 40)
SAME       POWERBALL: every forecast and every score of every method (15118 forecast lines: 15118 forecasts and 0 no-forecasts; 15078 scores)
SAME       POWERBALL: the second OV-1 series, line by line (41 and 41 lines; draws 1551 to 1591)
SAME       POWERBALL: the OV-1 series over all draws, line by line (447 and 447 lines)
SAME       POWERBALL: the names of the report files (901 and 901)
SAME       POWERBALL: every report file, byte for byte (league, next draw, both OV-1 print-outs, README) (the frozen engine's given the new wording: 2710 replacements of 21 declared kinds)
SAME       OZLOTTO: the methods that have results (40 and 40)
SAME       OZLOTTO: every forecast and every score of every method (6598 forecast lines: 6598 forecasts and 0 no-forecasts; 6558 scores)
SAME       OZLOTTO: the second OV-1 series, line by line (41 and 41 lines; draws 1668 to 1708)
SAME       OZLOTTO: the OV-1 series over all draws, line by line (234 and 234 lines)
SAME       OZLOTTO: the names of the report files (475 and 475)
SAME       OZLOTTO: every report file, byte for byte (league, next draw, both OV-1 print-outs, README) (the frozen engine's given the new wording: 1432 replacements of 21 declared kinds)
RESULT: SAME: the frozen engine at D:\DELETE_ME\a_p_r_i_r\T031\frozen_DEV and the simplified engine at D:\DELETE_ME\a_p_r_i_r\T031\new_DEV
```

Exit code 0.

### Step 12

Command:

```text
ls -A "D:/DELETE_ME/a_p_r_i_r/T031/tmp" | wc -l
```

Output:

```text
0
```

Exit code 0.

## Clean-up

No task clone was made, so there was none to remove. This task does not delete its scratch folder.

The one folder this task created under `D:\DELETE_ME\` is:

```text
D:\DELETE_ME\a_p_r_i_r\T031
```

It holds `new_DEV`, `frozen_DEV`, `backups`, `tmp`, and the text files `files.txt`,
`run_frozen_1.txt`, `run_new_1.txt`, `run_frozen_2.txt` and `run_new_2.txt`. **It was not removed**,
as the task file directs; the project owner deletes it by hand when he wishes.

Nothing was written outside `D:\DELETE_ME\a_p_r_i_r\T031` and this report. Nothing was copied out of
the scratch folder except the command output recorded above.

## Deviations

- Step 6 was started as a background command of the shell, because it runs for about 45 minutes and
  the runner's foreground limit is shorter than that. Its command line, its redirection and its
  `grep` are those of the task file, unchanged; the command ran to its own end and no process was
  ended.
- Step 13 (writing this report) was done with the runner's file-writing tool rather than a shell
  heredoc: the permission settings refused the shell command that would have written this file,
  because its text contains the name of the results updater's source file, which appears in the
  listing of step 5. The task file gives no command for step 13. Nothing else differed.

Otherwise none: steps 1 to 12 were run in order, each command exactly as the task file gives it.

## Observations

- Step 5: on two of the tool's group heading lines the count is larger than the number of file names
  printed under it. `the same bytes: 14 engine files, 119 method and helper files` is followed by 14
  names, and `only in the frozen tree: 45 engine files, 9 method and helper files` is followed by 5
  names. The output above is the whole output exactly as it was printed; nothing of it was left out
  of this report.
- Step 3: the real DEV tree's Python is 3.15.2 with numpy 2.5.5. Both engines' jobs, in steps 6, 7, 9
  and 10, were run with that one interpreter, so both sides of the comparison were computed in the
  same environment, as decision log entry 366 requires.
- Every research job of either engine was started with `--no-update`; no results updater was run at
  any point, in any way.
- Step 12: the temporary folder was empty at the end (0 entries).
