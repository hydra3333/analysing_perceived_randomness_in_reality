# REPORT_T026 - Windows rehearsal of build step 2, second part: the two launchers, the first research fill and the comparison, in the scratch tree that TASK_T025 left on D:

RESULT: STOP at step 11

- Task file: inbox/TASK_T026.md at main-repository commit 23f3c99506b120e73654caa05de171c72e7f8e60
- Run by: Claude Code (local runner), 23 November 2026 23:33 to 24 November 2026 00:27, the PC's own local time (the time zone was not read: the task file permits only `date +%H:%M:%S`)
- Owner options used: none (the task file offers none)
- Machine: Windows-11-10.0.26300-SP0; Python 3.15.2 at E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | Python | 0 | the main venv's Python 3.15.2, Windows-11-10.0.26300-SP0 |
| 2 | the main repository's state (read-only) | 0, 0, 0 | clean; HEAD 23f3c99506b120e73654caa05de171c72e7f8e60 |
| 3 | the scratch folder and tree are as the task needs | 0 | `SCRATCH CHECK PASS` |
| 4 | the scratch tree's Python | 0 | `D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv`, Python 3.15.2, Windows |
| 5 (long) | the first fill: the research job on both games | 0 | `The job finished.`; `JOB EXIT CODE 0`; as expected |
| 6 (long) | the same job once more | 0 | all counts `0`; `The job finished.`; `JOB EXIT CODE 0`; as expected |
| 7 | the withdrawal launcher starts (`--help`) | 0 | `WITHDRAW EXIT CODE 0`; as expected |
| 8 (long) | copy the old development run folders in, by reading | 0 | `OLD RUN FOLDERS COPIED`; `COPY EXIT CODE 0` |
| 9 (long) | the early comparison with the old development records | 1 | `RESULT: STOP`; `COMPARE EXIT CODE 1` |
| 10 | the comparison's lines and the two counts | 0, 0, 0 | 160 per-variant `equal` lines; 20 `DIFFERENT` lines |
| 11 | what step 10 must show | - | **STOP**: part 2 `DIFFERENT: 2802` for both games, 20 `DIFFERENT` lines, `RESULT: STOP`, `COMPARE EXIT CODE 1` |
| 12 | clean-up | - | nothing to remove; `D:\DELETE_ME\a_p_r_i_r\T025` left in place |

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

Commands:

```text
git status --short
git rev-parse HEAD
git log -1 --format=%s
```

Output:

```text
EXIT CODE 0
23f3c99506b120e73654caa05de171c72e7f8e60
EXIT CODE 0
exchange: the owner decides to run TASK_T026 now; decision log entry 204
EXIT CODE 0
```

`git status --short` printed nothing (the working tree is clean).

### Step 3

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import os, sys; p = r'D:\DELETE_ME'; t = r'D:\DELETE_ME\a_p_r_i_r\T025\tree'; j = getattr(os.path, 'isjunction', lambda x: False); missing = [n for n in ('ENVIRONMENT.ini', 'Run_Research.bat', 'Withdraw_Variant.bat', r'src\research_command.py', r'.venv\Scripts\python.exe') if not os.path.isfile(os.path.join(t, n))]; early = [n for n in (r'results\research', 'records') if os.path.lexists(os.path.join(t, n))]; ok = os.path.isdir(p) and not os.path.islink(p) and not j(p) and os.path.normcase(os.path.realpath(p)) == os.path.normcase(p) and os.path.isdir(r'D:\DELETE_ME\a_p_r_i_r\T025\evidence') and not missing and not early; print('real path:', os.path.realpath(p)); print('missing:', missing); print('there already:', early); print('SCRATCH CHECK PASS' if ok else 'SCRATCH CHECK STOP'); sys.exit(0 if ok else 1)"
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
"D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv\Scripts\python.exe" -I -c "import sys, platform; print(sys.prefix); print(sys.version); print(platform.platform())"
```

Output:

```text
D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv
3.15.2 (tags/v3.15.2:5e58eaa, Oct 25 2026, 17:27:03) [MSC v.1951 64 bit (AMD64)]
Windows-11-10.0.26300-SP0
EXIT CODE 0
```

### Step 5 (long) - the first fill: the research job on both games

Start time 23:33:30, end time 00:19:33 (the shell's clock, before and after the command); the job's own lines give 2026-11-23 23:33 to 2026-11-24 00:19, that is 46 minutes.

Command (run as one background command and waited for):

```text
"D:/DELETE_ME/a_p_r_i_r/T025/tree/Run_Research.bat" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/first_job.txt" 2>&1; echo "JOB EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/first_job.txt"
```

#### From the recorded file D:\DELETE_ME\a_p_r_i_r\T025\evidence\first_job.txt - the lines that matter

Command:

```text
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/first_job.txt" | grep -n -e "RESEARCH JOB" -e "About to work" -e "finished" -e "written:" -e "WARNING" -e "REFUSED" -e "STOP" -e "EXIT CODE"
```

Output:

```text
1:RESEARCH JOB - START - 2026-11-23 23:33 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T025\tree
2:About to work: POWERBALL, OZLOTTO (results step left out: --no-update)
22:POWERBALL: finished. Results on file through draw 1591; written: 15118 forecasts, 15078 scores, 0 prevailing lines, 0 eligibility draws, 900 report files. prevailing OV-1: not started; waiting for a successful results step
34:OZLOTTO: finished. Results on file through draw 1708; written: 6598 forecasts, 6558 scores, 0 prevailing lines, 0 eligibility draws, 474 report files. prevailing OV-1: not started; waiting for a successful results step
35:RESEARCH JOB - END - 2026-11-24 00:19 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T025\tree
36:POWERBALL: finished. Results on file through draw 1591; written: 15118 forecasts, 15078 scores, 0 prevailing lines, 0 eligibility draws, 900 report files. prevailing OV-1: not started; waiting for a successful results step
37:OZLOTTO: finished. Results on file through draw 1708; written: 6598 forecasts, 6558 scores, 0 prevailing lines, 0 eligibility draws, 474 report files. prevailing OV-1: not started; waiting for a successful results step
38:The job finished.
39:JOB EXIT CODE 0
EXIT CODE 0
```

#### From the recorded file D:\DELETE_ME\a_p_r_i_r\T025\evidence\first_job.txt - the end of the file

Command:

```text
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/first_job.txt" | tail -n 12
```

Output:

```text
OZLOTTO: worked through draw 1599 of 1708; so far 2444 forecasts and 2444 scores written
OZLOTTO: worked through draw 1624 of 1708; so far 3369 forecasts and 3369 scores written
OZLOTTO: worked through draw 1649 of 1708; so far 4294 forecasts and 4294 scores written
OZLOTTO: worked through draw 1674 of 1708; so far 5219 forecasts and 5219 scores written
OZLOTTO: worked through draw 1699 of 1708; so far 6198 forecasts and 6198 scores written
OZLOTTO: the results step was left out (--no-update)
OZLOTTO: finished. Results on file through draw 1708; written: 6598 forecasts, 6558 scores, 0 prevailing lines, 0 eligibility draws, 474 report files. prevailing OV-1: not started; waiting for a successful results step
RESEARCH JOB - END - 2026-11-24 00:19 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T025\tree
POWERBALL: finished. Results on file through draw 1591; written: 15118 forecasts, 15078 scores, 0 prevailing lines, 0 eligibility draws, 900 report files. prevailing OV-1: not started; waiting for a successful results step
OZLOTTO: finished. Results on file through draw 1708; written: 6598 forecasts, 6558 scores, 0 prevailing lines, 0 eligibility draws, 474 report files. prevailing OV-1: not started; waiting for a successful results step
The job finished.
JOB EXIT CODE 0
EXIT CODE 0
```

#### From the recorded file D:\DELETE_ME\a_p_r_i_r\T025\evidence\first_job.txt - its length

Command:

```text
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/first_job.txt" | wc -l
```

Output:

```text
39
EXIT CODE 0
```

### Step 6 (long) - the same job once more

Start time 00:20:03, end time 00:23:12 (the shell's clock, before and after the command); the job's own lines give 2026-11-24 00:20 to 2026-11-24 00:23, that is 3 minutes.

Command (run as one background command and waited for):

```text
"D:/DELETE_ME/a_p_r_i_r/T025/tree/Run_Research.bat" --game BOTH --no-update > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/second_job.txt" 2>&1; echo "JOB EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/second_job.txt"
```

#### From the recorded file D:\DELETE_ME\a_p_r_i_r\T025\evidence\second_job.txt - the whole file

Command:

```text
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/second_job.txt"
```

Output:

```text
RESEARCH JOB - START - 2026-11-24 00:20 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T025\tree
About to work: POWERBALL, OZLOTTO (results step left out: --no-update)
POWERBALL: results on file through draw 1591; 40 variants installed
POWERBALL: the results step was left out (--no-update)
POWERBALL: finished. Results on file through draw 1591; written: 0 forecasts, 0 scores, 0 prevailing lines, 0 eligibility draws, 0 report files. prevailing OV-1: not started; waiting for a successful results step
OZLOTTO: results on file through draw 1708; 40 variants installed
OZLOTTO: the results step was left out (--no-update)
OZLOTTO: finished. Results on file through draw 1708; written: 0 forecasts, 0 scores, 0 prevailing lines, 0 eligibility draws, 0 report files. prevailing OV-1: not started; waiting for a successful results step
RESEARCH JOB - END - 2026-11-24 00:23 - the DEV tree at D:\DELETE_ME\a_p_r_i_r\T025\tree
POWERBALL: finished. Results on file through draw 1591; written: 0 forecasts, 0 scores, 0 prevailing lines, 0 eligibility draws, 0 report files. prevailing OV-1: not started; waiting for a successful results step
OZLOTTO: finished. Results on file through draw 1708; written: 0 forecasts, 0 scores, 0 prevailing lines, 0 eligibility draws, 0 report files. prevailing OV-1: not started; waiting for a successful results step
The job finished.
JOB EXIT CODE 0
EXIT CODE 0
```

### Step 7 - the withdrawal launcher starts

Commands:

```text
"D:/DELETE_ME/a_p_r_i_r/T025/tree/Withdraw_Variant.bat" --help > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/withdraw_help.txt" 2>&1; echo "WITHDRAW EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/withdraw_help.txt"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/withdraw_help.txt"
```

#### From the recorded file D:\DELETE_ME\a_p_r_i_r\T025\evidence\withdraw_help.txt - the whole file

Output:

```text
usage: Withdraw_Variant.bat [-h] --game {POWERBALL,OZLOTTO,BOTH}
                            --reason REASON
                            <family> <variant> [<family> <variant> ...]

Withdraw a defective variant (specification 11).

positional arguments:
  <family> <variant>    the variant, as two words; several variants may follow
                        one another

options:
  -h, --help            show this help message and exit
  --game {POWERBALL,OZLOTTO,BOTH}
  --reason REASON       why the variant is wrong, in a few words
WITHDRAW EXIT CODE 0
EXIT CODE 0
```

### Step 8 (long) - copy the old system's development run folders into the scratch tree, by reading

Command (run as one background command and waited for):

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import os, shutil; p = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\results\real\development'; d = r'D:\DELETE_ME\a_p_r_i_r\T025\tree\results\real\development\contract_runs'; names = [n for n in os.listdir(p) if n.lower() == 'contract_runs']; names and shutil.copytree(os.path.join(p, names[0]), d); print('OLD RUN FOLDERS COPIED' if names else 'OLD RUN FOLDERS NOT PRESENT')" > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/old_runs_copy.txt" 2>&1; echo "COPY EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/old_runs_copy.txt"
```

#### From the recorded file D:\DELETE_ME\a_p_r_i_r\T025\evidence\old_runs_copy.txt - the whole file

```text
OLD RUN FOLDERS COPIED
COPY EXIT CODE 0
```

No traceback and no error in the file; the permission system did not refuse the command.

### Step 9 (long) - the early comparison with the old development records

Start time 00:24:45, end time 00:27:14 (the shell's clock, before and after the command), that is 2 minutes 29 seconds.

Command (run as one background command and waited for):

```text
"D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv\Scripts\python.exe" -B "D:\DELETE_ME\a_p_r_i_r\T025\tree\exchange\EX_288_Claude\STEP2_Research_Engine_v1r2\tools\compare_fill_with_old_records.py" --tree "D:\DELETE_ME\a_p_r_i_r\T025\tree" > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt" 2>&1; echo "COMPARE EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt"
```

### Step 10 - the comparison's lines that are not per-variant lines, and the count of per-variant lines

#### From the recorded file D:\DELETE_ME\a_p_r_i_r\T025\evidence\early_comparison.txt - the lines that are not per-variant lines

Command:

```text
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt" | grep -v -e " equal$" -e "^DIFFERENT"
```

Output:

```text
POWERBALL: part 1: old score records (TOP and WORST): 22884; equal in the new score lists: 22884; DIFFERENT: 0
POWERBALL: part 2: old development forecasts read from the run folders: 17280 (for 17280 variant and target pairs); equal in the new lists: 14478; DIFFERENT: 2802; lines the new lists hold for other targets (never forecast by the old development runs): -2162
POWERBALL: part 2: forecasts named by the tracked rank ledgers: 11442; of those not among the old forecasts compared: 0
OZLOTTO: part 1: old score records (TOP and WORST): 11916; equal in the new score lists: 11916; DIFFERENT: 0
OZLOTTO: part 2: old development forecasts read from the run folders: 8760 (for 8760 variant and target pairs); equal in the new lists: 5958; DIFFERENT: 2802; lines the new lists hold for other targets (never forecast by the old development runs): -2162
OZLOTTO: part 2: forecasts named by the tracked rank ledgers: 5958; of those not among the old forecasts compared: 0
RESULT: STOP - at least one old score or old development forecast is not in the new lists with the same content. Change nothing and send Claude this whole output.
COMPARE EXIT CODE 1
EXIT CODE 0
```

#### The count of per-variant lines ending " equal"

Command:

```text
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt" | grep -c " equal$"
```

Output:

```text
160
EXIT CODE 0
```

#### The count of lines beginning "DIFFERENT"

Command:

```text
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison.txt" | grep -c "^DIFFERENT"
```

Output:

```text
20
EXIT CODE 0
```

The 20 lines beginning `DIFFERENT` were counted and are not copied into this report (task file step 10: they may show numbers drawn).

### Step 11 - what step 10 must show: STOP

Step 8 said `OLD RUN FOLDERS COPIED`, so step 11's first case applies. What step 10 showed, against it:

| What step 11 requires | What step 10 showed |
|---|---|
| per game, `part 1: ... DIFFERENT: 0` | yes, both games: POWERBALL 22884/22884, OZLOTTO 11916/11916, `DIFFERENT: 0` |
| per game, a `part 2: old development forecasts read from the run folders:` line with `DIFFERENT: 0` | no: both games show `DIFFERENT: 2802` |
| per game, `part 2: forecasts named by the tracked rank ledgers: N; of those not among the old forecasts compared: 0` | yes, both games: `0` |
| a line beginning `RESULT: PASS - COMPLETE - both games; all 34800 old score records equal the new score lists` | no: the line is `RESULT: STOP - at least one old score or old development forecast is not in the new lists with the same content. Change nothing and send Claude this whole output.` |
| `COMPARE EXIT CODE 0` | no: `COMPARE EXIT CODE 1` |
| the second command prints 160 | yes: 160 |
| the third command prints 0 | no: 20 |

Step 11 says anything else is a STOP, naming a `DIFFERENT:` count above 0, a third number above 0, and `RESULT: STOP`. All three are present. **STOP at step 11.** Nothing was retried, repaired or reordered.

## Clean-up

Step 12: nothing to remove. This task made no task clone.

- This task created no folder under `D:\DELETE_ME\`. It wrote only inside `D:\DELETE_ME\a_p_r_i_r\T025\`, which TASK_T025 created: five files in the existing `evidence` folder (`first_job.txt`, `second_job.txt`, `withdraw_help.txt`, `old_runs_copy.txt` and `early_comparison.txt`), and what the tree's own programs wrote inside `D:\DELETE_ME\a_p_r_i_r\T025\tree\` (the research results and records of steps 5 and 6, and the copy of step 8 at `tree\results\real\development\contract_runs`).
- `D:\DELETE_ME\a_p_r_i_r\T025` was **left in place, not removed**, as step 12 requires and as rulebook section 2A item 9 requires after a STOP. It is left exactly as the STOP left it.
- Nothing was copied out of `D:\DELETE_ME\` except the text this report quotes, under headings that name the file each piece came from.

## Final state of the main repository (step 13)

Command:

```text
git status --short
```

Output:

```text
?? CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T026.md
```

This differs from step 2 (where `git status --short` printed nothing) only by this report file, which is untracked until step 14 commits it. No other file of the main repository was added, changed or removed.

## Wall-clock times (step 13)

| Step | Start | End | Duration |
|---|---|---|---|
| 5 (first fill, both games) | 2026-11-23 23:33 | 2026-11-24 00:19 | 46 minutes (the job's own `RESEARCH JOB - START` and `- END` lines) |
| 6 (the same job once more) | 2026-11-24 00:20 | 2026-11-24 00:23 | 3 minutes (the job's own `RESEARCH JOB - START` and `- END` lines) |
| 9 (the early comparison) | 00:24:45 | 00:27:14 | 2 minutes 29 seconds (the shell's clock before and after the command) |

## Deviations

None.

- No line was withheld. No output copied into this report shows numbers drawn in any draw or a path under a Windows user folder. The 20 lines beginning `DIFFERENT` were counted only, as task file step 10 directs, and are not copied; that is what the task file asks for, not a deviation.
- The only additions to task lines were those the task file permits: `cd` to MAIN before each line, `echo "EXIT CODE $?"` after a line that does not itself write an `EXIT CODE` line, and `date +%H:%M:%S` as a command of its own before and after steps 5, 6 and 9.
- The four steps marked (long) - 5, 6, 8 and 9 - were each run as one background command and waited for, as the task file's recording rules require. Each recorded file carries its own last line with the program's own exit status.

## Observations

- Step 5's job printed no `WARNING`, `REFUSED` or `STOP` line; steps 5, 6, 7 and 8 all met what the task file expected, exit code 0 each.
- The comparison's own `RESULT: STOP` line asks for the whole output to be sent to the Claude web chat. The whole output is not copied here: task file step 10 names what to copy, and says that the lines beginning `DIFFERENT` are counted and never copied (they may show numbers drawn); the 160 per-variant lines ending ` equal` were likewise filtered out by step 10's own first command and only counted by its second. The whole file is at `D:\DELETE_ME\a_p_r_i_r\T025\evidence\early_comparison.txt`, left in place.
- Both games show exactly the same part 2 numbers for the shape of the difference: `DIFFERENT: 2802` and `lines the new lists hold for other targets (never forecast by the old development runs): -2162`. Both games' part 1 comparisons (34800 old score records in total: 22884 + 11916) were equal with `DIFFERENT: 0`, and for both games `of those not among the old forecasts compared: 0`.
