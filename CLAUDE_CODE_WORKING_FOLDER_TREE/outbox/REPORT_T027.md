# REPORT_T027 - Windows rehearsal of build step 2, third part: the comparison with the old records once more, with the corrected tool of package v1r3, in the scratch tree on D:

RESULT: PASS

- Task file: inbox/TASK_T027.md at main-repository commit a7cb7790d13473c49345ef4aefbc024c4e22bed5
- Run by: Claude Code (local runner), 24 November 2026, 06:21 to 06:24, the PC's own local time (the time zone was not read: the task file permits only `date +%H:%M:%S`)
- Owner options used: none (the task file offers none)
- Machine: Windows-11-10.0.26300-SP0; Python 3.15.2 at E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | Python | 0 | the main venv's Python 3.15.2, Windows-11-10.0.26300-SP0 |
| 2 | the main repository's state (read-only) | 0, 0, 0 | clean; HEAD a7cb7790d13473c49345ef4aefbc024c4e22bed5 |
| 3 | the scratch folder is an ordinary folder on D: and the tree is as the task needs it | 0 | `SCRATCH CHECK PASS` |
| 4 | copy the corrected tool in by reading, and check its SHA-256 | 0 | `TOOL COPY PASS`; SHA-256 (LF) as the task file gives |
| 5 (long) | the comparison with the old development records, with the corrected tool | 0 | `RESULT: PASS - COMPLETE - both games`; `COMPARE EXIT CODE 0` |
| 6 | the comparison's lines that are not per-variant lines, and the two counts | 0; 0; 1 (printed `0`) | the eight lines; 160 per-variant `equal` lines; 0 `DIFFERENT` lines |
| 7 | what step 6 must show | - | **PASS**: all eight lines and all numbers exactly as the task file requires; 160 and 0 |
| 8 | clean-up | - | nothing to remove; `D:\DELETE_ME\a_p_r_i_r\T025` left in place |
| 9 | the report | - | written; final `git status --short` recorded below |

Wall-clock time of step 5: started 06:21:46, finished 06:23:54, about 2 minutes 8 seconds.

## Outputs

### Step 1

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.platform())"
```

Output:

```text
E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe
3.15.2 (tags/v3.15.2:5e58eaa, Oct 25 2026, 17:27:03) [MSC v.1951 64 bit (AMD64)]
Windows-11-10.0.26300-SP0
EXIT CODE 0
```

### Step 2

Commands (each run on its own, with `echo "EXIT CODE $?"` after it):

```text
git status --short
git rev-parse HEAD
git log -1 --format=%s
```

Output:

```text
EXIT CODE 0
```

```text
a7cb7790d13473c49345ef4aefbc024c4e22bed5
EXIT CODE 0
```

```text
exchange: EX_294 received (PASS for package STEP2_Research_Engine_v1r3); runner: TASK_T027 written - the comparison alone with the corrected tool, in the scratch tree; not started; decision log entry 207
EXIT CODE 0
```

`git status --short` printed nothing: the working tree is clean.

### Step 3

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import os, sys; p = r'D:\DELETE_ME'; t = r'D:\DELETE_ME\a_p_r_i_r\T025\tree'; e = r'D:\DELETE_ME\a_p_r_i_r\T025\evidence'; j = getattr(os.path, 'isjunction', lambda x: False); missing = [n for n in (r'.venv\Scripts\python.exe', r'results\research\POWERBALL\variants', r'results\research\OZLOTTO\variants', r'results\real\development\contract_runs\POWERBALL', r'results\real\development\contract_runs\OZLOTTO') if not os.path.exists(os.path.join(t, n))]; early = [n for n in ('compare_fill_with_old_records_v1r3.py', 'early_comparison_v1r3.txt') if os.path.lexists(os.path.join(e, n))]; ok = os.path.isdir(p) and not os.path.islink(p) and not j(p) and os.path.normcase(os.path.realpath(p)) == os.path.normcase(p) and os.path.isdir(e) and not missing and not early; print('real path:', os.path.realpath(p)); print('missing:', missing); print('there already:', early); print('SCRATCH CHECK PASS' if ok else 'SCRATCH CHECK STOP'); sys.exit(0 if ok else 1)"
```

Output:

```text
real path: D:\DELETE_ME
missing: []
there already: []
SCRATCH CHECK PASS
EXIT CODE 0
```

### Step 4

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import hashlib, shutil, sys; s = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\exchange\EX_293_Claude\STEP2_Research_Engine_v1r3\tools\compare_fill_with_old_records.py'; d = r'D:\DELETE_ME\a_p_r_i_r\T025\evidence\compare_fill_with_old_records_v1r3.py'; shutil.copyfile(s, d); h = hashlib.sha256(open(d, 'rb').read().replace(b'\r\n', b'\n')).hexdigest(); ok = h == 'b4135af7ea925caba020bcbc77185999f51837bff0dcedddeb295ff0d241ada6'; print('TOOL SHA-256 (LF):', h); print('TOOL COPY PASS' if ok else 'TOOL COPY STOP'); sys.exit(0 if ok else 1)"
```

Output:

```text
TOOL SHA-256 (LF): b4135af7ea925caba020bcbc77185999f51837bff0dcedddeb295ff0d241ada6
TOOL COPY PASS
EXIT CODE 0
```

### Step 5 (long)

Command (run as one background command line, exactly as the task file gives it):

```text
"D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv\Scripts\python.exe" -B "D:\DELETE_ME\a_p_r_i_r\T025\evidence\compare_fill_with_old_records_v1r3.py" --tree "D:\DELETE_ME\a_p_r_i_r\T025\tree" > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison_v1r3.txt" 2>&1; echo "COMPARE EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison_v1r3.txt"
```

The command's own output went to `D:\DELETE_ME\a_p_r_i_r\T025\evidence\early_comparison_v1r3.txt`; step 6 shows its lines. Its last line in that file is `COMPARE EXIT CODE 0`, written by the same shell straight after the program ended.

`date +%H:%M:%S` before the step: `06:21:46`. `date +%H:%M:%S` after it: `06:23:54`.

### Step 6

First command:

```text
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison_v1r3.txt" | grep -v -e " equal$" -e "^DIFFERENT"
```

Output (from the file `D:\DELETE_ME\a_p_r_i_r\T025\evidence\early_comparison_v1r3.txt`):

```text
POWERBALL: part 1: old score records (TOP and WORST): 22884; equal in the new score lists: 22884; DIFFERENT: 0
POWERBALL: part 2: old development forecasts read from the run folders: 17280 (for 17280 variant and target pairs); equal in the new lists: 14478; INSUFFICIENT_HISTORY records before the variant's first target, where the new list has no line: 2802; DIFFERENT: 0; lines the new lists hold for other targets (never forecast by the old development runs): 640
POWERBALL: part 2: forecasts named by the tracked rank ledgers: 11442; of those not among the old forecasts compared: 0
OZLOTTO: part 1: old score records (TOP and WORST): 11916; equal in the new score lists: 11916; DIFFERENT: 0
OZLOTTO: part 2: old development forecasts read from the run folders: 8760 (for 8760 variant and target pairs); equal in the new lists: 5958; INSUFFICIENT_HISTORY records before the variant's first target, where the new list has no line: 2802; DIFFERENT: 0; lines the new lists hold for other targets (never forecast by the old development runs): 640
OZLOTTO: part 2: forecasts named by the tracked rank ledgers: 5958; of those not among the old forecasts compared: 0
RESULT: PASS - COMPLETE - both games; all 34800 old score records equal the new score lists; all 20436 old development forecasts in the run folders were found in the new lists with the same view digest, scores, ranking, TOP and WORST; the 5604 old INSUFFICIENT_HISTORY records all lie before their variants' first targets, where the new lists hold no line; every forecast the tracked rank ledgers name is among them.
COMPARE EXIT CODE 0
EXIT CODE 0
```

Second command:

```text
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison_v1r3.txt" | grep -c " equal$"
```

Output:

```text
160
EXIT CODE 0
```

Third command:

```text
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison_v1r3.txt" | grep -c "^DIFFERENT"
```

Output:

```text
0
EXIT CODE 1
```

The third command printed `0` and exited 1. The task file (step 6) says that `grep -c` exits 1 when the count it prints is exactly 0, and that an exit code 1 together with a printed `0` is therefore not an error.

No line was withheld: none of the copied lines shows numbers drawn in any draw, and none shows a path under `C:\Users\`.

### Step 7 - what step 6 must show

Every one of the eight required lines was present, with exactly the numbers the task file requires:

- `POWERBALL: part 1: ... 22884; ... 22884; DIFFERENT: 0` - as required.
- POWERBALL part 2: `17280 (for 17280 variant and target pairs)`; `equal in the new lists: 14478`; `INSUFFICIENT_HISTORY records before the variant's first target, where the new list has no line: 2802`; `DIFFERENT: 0;`; ends `(never forecast by the old development runs): 640` - as required.
- `POWERBALL: part 2: forecasts named by the tracked rank ledgers: 11442; of those not among the old forecasts compared: 0` - as required.
- `OZLOTTO: part 1: ... 11916; ... 11916; DIFFERENT: 0` - as required.
- OZLOTTO part 2: `8760 (for 8760 variant and target pairs)`; `equal in the new lists: 5958`; `INSUFFICIENT_HISTORY ... : 2802`; `DIFFERENT: 0;`; ends `(never forecast by the old development runs): 640` - as required.
- `OZLOTTO: part 2: forecasts named by the tracked rank ledgers: 5958; of those not among the old forecasts compared: 0` - as required.
- `RESULT: PASS - COMPLETE - both games; all 34800 old score records equal the new score lists; all 20436 old development forecasts in the run folders were found in the new lists ...`, holding `the 5604 old INSUFFICIENT_HISTORY records all lie before their variants' first targets` - as required.
- `COMPARE EXIT CODE 0` - as required.

The second command of step 6 printed `160`, the third printed `0`, as required. No `DIFFERENT:` count was above 0, no third number was above 0, and the result line is neither `RESULT: STOP`, `RESULT: PARTIAL` nor `RESULT: REFUSED`.

## Clean-up

Step 8: nothing to remove. This task made no task clone.

- Folders created under `D:\DELETE_ME\` by this task: **none**.
- Files written under `D:\DELETE_ME\` by this task: two, both in `D:\DELETE_ME\a_p_r_i_r\T025\evidence` - `compare_fill_with_old_records_v1r3.py` (the copy of the corrected tool, step 4) and `early_comparison_v1r3.txt` (the comparison's recorded output, step 5).
- `D:\DELETE_ME\a_p_r_i_r\T025` was **left in place, not removed**, as the task file requires.

Nothing was copied out of `D:\DELETE_ME\` other than the text this report quotes under the headings above, which name the file it came from.

## The main repository's state at the end

Command:

```text
git status --short
```

Output:

```text
?? CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T027.md
EXIT CODE 0
```

This differs from step 2 (which printed nothing) only by this report file, which did not exist when step 2 ran. No other file in the main repository changed.

## Deviations

- Recording order: the report file was written in two blocks rather than after each single step. Steps 1 to 4 were written into it while step 5 was running (step 5 is a long step whose own output goes to a file in the scratch tree), and steps 5 to 9 were written after step 5 finished. No command was changed, skipped, reordered or repeated.
- Nothing else. Every command was run exactly as the task file gives it, from the main repository in Git Bash, with only `cd` to the main repository before it and `echo "EXIT CODE $?"` after it where the task file permits, and `date +%H:%M:%S` on its own before and after step 5.

## Observations

- The task file's step 6 note about `grep -c` applied: the third command printed `0` and exited 1.
- No warning or extra output appeared in any step.
