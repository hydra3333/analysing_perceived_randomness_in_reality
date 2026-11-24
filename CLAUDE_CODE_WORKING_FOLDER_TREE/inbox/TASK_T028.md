# TASK_T028 - a probe before build step 3 is coded: three facts about this Windows PC (renames when something is open; the size and time of a backup ZIP; what Python can read of other processes), in the scratch folder on D:

**Task ID:** T028. **Date:** 24 November 2026 (r1: the three corrections of the reviewer's EX_301, to steps 3 and 4, to steps 6 and 7 and to step 8's probe; and step 6 is now said to be what it is, an environment-only proxy, since the owner has deleted the scratch tree of TASK_T025). **Author:** the Claude web chat. Rulebook v0.7 (RAT-44). **Section 2A applies to steps 3 to 8, in the folder `D:\DELETE_ME\a_p_r_i_r\T028`** (new; this task creates it). Step 6 also reads, and only reads, the main repository's `.venv` folder.

**Purpose.** Build step 3 (trees, installs, backups and restore) has the owner's go to be designed and coded in the cloud (decision log entry 217), and the owner agreed to this probe first (entry 219). Three things about it cannot be learned in the cloud, and its install, backup and restore logic is designed around them: (1) how Windows answers a rename, a replacement or a removal when a file is open or another program sits in the folder; (2) how large a ZIP of a Python environment is and how long it takes to write, to read back and to read the source twice (**an environment-only proxy:** the owner has deleted the scratch tree of TASK_T025, so no whole tree is measured; this says nothing of a whole QA or PROD tree, of `source_data` or `results`, or of a real backup, which is measured later in the joined rehearsal); (3) what a Python program can read of the other processes on this PC, with psutil and with the standard library alone. **This task measures; it checks nothing and decides nothing.** The answers go to the Claude web chat in the report.

**What it does not do.** It runs no program of the project's software: no launcher, no research job, no command of the new system, no test suite. It makes no task clone, builds no Python environment and has no network use. It changes nothing in the main repository (only this task's report is committed there) and nothing in the main `.venv`. It ends no process: the probe starts one small helper program of its own, twice, and each time the helper ends by itself. It changes no date, time or time zone. It names no real QA or PROD tree. It reads no file under the main repository's `source_data`, `results` or `transitory_data`.

**The one program it runs** is the probe `inbox\TASK_T028_probe.py` (revision r1), written for this task (standard library; it also reads the process table through psutil, which the main venv has, so that the two readings can be compared; nothing is installed if psutil is missing: that is then a measurement not made, and a STOP). The task copies it into the scratch folder and runs the copy with the main venv's Python. The probe writes only under `D:\DELETE_ME\a_p_r_i_r\T028`. It prints counts, sizes, times, program names (such as `python.exe`) and Windows' answers; it prints no file's contents and no path under a user's folder.

**Before the owner starts this task (the owner, not the runner):** `git pull --ff-only` has been done and this is a new Claude Code conversation; nothing of the project is running; the folder `D:\DELETE_ME` exists. The task takes about ten to fifteen minutes and writes two ZIP files of perhaps 100 to 300 MB each into the scratch folder.

## Owner options

- None.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| PROBE (the probe, in the main repository; read only) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\TASK_T028_probe.py` |
| SCRATCH (this task's scratch folder; created in step 4) | `D:\DELETE_ME\a_p_r_i_r\T028` |
| SPROBE (the copy of the probe that this task makes) | `D:\DELETE_ME\a_p_r_i_r\T028\TASK_T028_probe.py` |
| VENV (the main repository's Python environment folder; read only in step 6) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv` |
| ZIPOUT (the recorded output of step 6) | `D:\DELETE_ME\a_p_r_i_r\T028\zip_part_output.txt` |

Run each command in Git Bash, from MAIN, exactly as written. On anything other than the expected last line and exit code of a step: **STOP**, record the output, and go to step 9. Never retry, repair or reorder a step. **After a STOP, leave `D:\DELETE_ME\a_p_r_i_r\T028` exactly as it is** (rulebook section 2A item 9).

**How the three probe steps (5, 6 and 8) are judged.** Each prints a first line `PROBE PART <name>: STARTED ...`, then its numbered measurement lines (`R..`, `Z..` or `P..`), then one last line. **The step passes only if that last line is exactly `PROBE PART <name>: FINISHED` and the exit code is 0.** A last line that says `REFUSED` or `FINISHED WITH ... NOT MADE`, a Python traceback, a missing last line or another exit code is a STOP. The measurement lines between are what this task is run to learn: no answer in them is expected or unexpected, and none of them passes or stops the step. In particular the words `WINDOWS SAID NO (...)` in a line of step 5 are Windows' answer to a question the probe asks on purpose.

**Recording** (so that nothing improvised is needed):
- Write `CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T028.md` as you go: after each step, add its command, its exit code and its output, before starting the next step.
- Exit codes: the program's own. Do not pipe a command under test into another program. Where step 7 pipes a recorded file through `tr`, that is only to show the file.
- **What you may add to a task line, and nothing else:** `cd` to MAIN before it; and, for a line that does not itself write an `EXIT CODE` line, `echo "EXIT CODE $?"` straight after it. Neither is a deviation. For the time of a step you may run `date +%H:%M:%S` in Git Bash as a command of its own before and after it: with a format it only prints the time. Never run `date` or `time` in CMD.
- **Step 6 is marked (long): how it is started, and how its end is known.** Its command line is an ordinary shell line, complete as written: it runs the probe, sends everything the probe prints into the file ZIPOUT, and when the probe has ended the same shell appends the probe's own exit status as the file's last line, `ZIP EXIT CODE <n>`. The line holds no `&` and none is to be added. Because it can run longer than your shell tool's foreground time limit, **start that exact line with your shell tool's own run-in-background option** (the same way the long steps of TASK_T025, TASK_T026 and TASK_T027 were run on this PC), and do nothing else until the tool reports that the command has ended. **The end of step 6 is proved by the file, not by the tool's report:** step 7 says how. Never take an exit status from another shell, from the tool's report or from the launch of the command.
- **What goes into the report:** the whole output of every step, exactly as printed (steps 5, 7 and 8 print some tens of lines in all). Files under `D:\DELETE_ME\a_p_r_i_r\T028` stay there; only the text that step 7 shows from ZIPOUT is copied into the report, under a heading that names that file (rulebook section 2A item 4 and section 7).
- **Never copy into the report** a line that shows a path under `C:\Users\`. Put `[line withheld: a user folder path]` in its place and say so under Deviations. The probe is written to print none.

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

**3. The scratch folder is an ordinary folder on D:; so is every folder between it and this task's folder that exists already; this task's folder would lie where its name says; and it is not there yet** (rulebook section 2A item 2; read-only). The folder `D:\DELETE_ME\a_p_r_i_r` may or may not exist: if it exists it must be an ordinary folder, not a link, a junction or another reparse point.
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import os, sys; p = r'D:\DELETE_ME'; m = r'D:\DELETE_ME\a_p_r_i_r'; t = r'D:\DELETE_ME\a_p_r_i_r\T028'; same = lambda d: os.path.normcase(os.path.realpath(d)) == os.path.normcase(d); plain = lambda d: os.path.isdir(d) and not os.path.islink(d) and not (getattr(os.lstat(d), 'st_file_attributes', 0) & 0x400) and same(d); notplain = [d for d in (p, m) if os.path.lexists(d) and not plain(d)]; ok = os.path.isdir(p) and not notplain and same(t) and not os.path.lexists(t); print('real path of the scratch folder:', os.path.realpath(p)); print('existing folders above the task folder that are not ordinary folders:', notplain); print('real path the task folder would have:', os.path.realpath(t)); print('task folder there already:', os.path.lexists(t)); print('SCRATCH CHECK PASS' if ok else 'SCRATCH CHECK STOP'); sys.exit(0 if ok else 1)"
```
Expected: `real path of the scratch folder: D:\DELETE_ME`, `existing folders above the task folder that are not ordinary folders: []`, `real path the task folder would have: D:\DELETE_ME\a_p_r_i_r\T028`, `task folder there already: False`, then `SCRATCH CHECK PASS`. (`0x400` is the mark Windows puts on a link, a junction or any other reparse point.)

**4. Make this task's scratch folder; check, before anything is copied, that the folder just made lies where its name says; then copy the probe into it from the main repository by reading, and check that it is the probe this task was written for** (its SHA-256 after CRLF is made LF, so that Git's line endings do not matter).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import hashlib, os, shutil, sys; s = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\TASK_T028_probe.py'; t = r'D:\DELETE_ME\a_p_r_i_r\T028'; d = r'D:\DELETE_ME\a_p_r_i_r\T028\TASK_T028_probe.py'; os.makedirs(t); r = os.path.realpath(t); print('real path of the task folder:', r); os.path.normcase(r) == os.path.normcase(t) or sys.exit('PROBE COPY STOP: the task folder is not where its name says; nothing was copied'); shutil.copyfile(s, d); h = hashlib.sha256(open(d, 'rb').read().replace(b'\r\n', b'\n')).hexdigest(); ok = h == '57fde59dc4f56526c1a73e95e006fee63b80bbffa223206740ee64776c6128bf'; print('PROBE SHA-256 (LF):', h); print('PROBE COPY PASS' if ok else 'PROBE COPY STOP'); sys.exit(0 if ok else 1)"
```
Expected: `real path of the task folder: D:\DELETE_ME\a_p_r_i_r\T028`, `PROBE SHA-256 (LF): 57fde59dc4f56526c1a73e95e006fee63b80bbffa223206740ee64776c6128bf`, then `PROBE COPY PASS`.

**5. The probe's part "rename"** (a few seconds; it works in its own new folder `D:\DELETE_ME\a_p_r_i_r\T028\rename_part`).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T028\TASK_T028_probe.py" rename --work "D:\DELETE_ME\a_p_r_i_r\T028"
```
Passes only as said above: last line `PROBE PART rename: FINISHED`, exit code 0. Copy the whole output into the report.

**6. (long) The probe's part "zip": an environment-only proxy** (several minutes; it reads the main `.venv` folder, VENV, and nothing else of the main repository, and writes two ZIP files into its own new folder `D:\DELETE_ME\a_p_r_i_r\T028\zip_part`; it changes nothing it reads). Start this exact line with your shell tool's run-in-background option, as said under Recording, and wait for the tool's report that it has ended.
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T028\TASK_T028_probe.py" zip --work "D:\DELETE_ME\a_p_r_i_r\T028" --otherwise-environment-of "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality" > "D:/DELETE_ME/a_p_r_i_r/T028/zip_part_output.txt" 2>&1; echo "ZIP EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T028/zip_part_output.txt"
```

**7. Whether step 6 has ended, and what it recorded.** First this line, which only reads:
```
tail -n 1 "D:/DELETE_ME/a_p_r_i_r/T028/zip_part_output.txt" | tr -d '\r'
```
- If it prints a line beginning `ZIP EXIT CODE`, step 6 has ended: go on to the second line below.
- If it prints anything else, or the file is not there yet, step 6 is still running: **that is neither a pass nor a STOP.** Wait a minute and run this same line again; it changes nothing. Record in the report how many times you ran it. **If no `ZIP EXIT CODE` line has appeared 30 minutes after step 6 was started, that is a STOP;** end nothing (rulebook section 2A item 6), and say in the report that the command of step 6 may still be running.

Then, once only:
```
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T028/zip_part_output.txt"
```
Passes only as said above: the last two lines are `PROBE PART zip: FINISHED` and `ZIP EXIT CODE 0`. Any other number after `ZIP EXIT CODE` is a STOP. Copy the whole output into the report, under the heading `From the file D:\DELETE_ME\a_p_r_i_r\T028\zip_part_output.txt (an environment-only proxy: the main .venv folder alone, not a whole tree and not a backup)`.

**8. The probe's part "processes"** (a few seconds; it reads Windows' process table, once with psutil and once with the standard library alone, and starts and waits for its own helper program; it ends no process). The part finishes as made only if psutil could be imported and each of the two readings showed this probe and its own helper program; otherwise its last line says `FINISHED WITH ... NOT MADE`, the exit code is 1, and that is a STOP like any other.
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T028\TASK_T028_probe.py" processes --work "D:\DELETE_ME\a_p_r_i_r\T028" --scratch-root "D:\DELETE_ME"
```
Passes only as said above: last line `PROBE PART processes: FINISHED`, exit code 0. Copy the whole output into the report.

## Clean-up

**9. Nothing to remove.** This task makes no task clone. **The scratch folder `D:\DELETE_ME\a_p_r_i_r\T028` is not removed by this task,** whether the task passed or stopped; the project owner deletes it himself when the Claude web chat says it is no longer needed. Nothing under the main `.venv` was changed.

## Report

**10. Finish** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T028.md` in the format of `outbox\README.md` (the step table and the RESULT line at the top). Also record:
- the wall-clock time of step 6, and that its figures are an environment-only proxy (the main `.venv` alone), not the size or time of a whole tree's backup;
- that this task created the folder `D:\DELETE_ME\a_p_r_i_r\T028` under `D:\DELETE_ME\` (with the probe's copy, the recorded output of step 6 and the probe's three part folders in it) and that it was left in place, not removed;
- whether the main repository's `git status --short` at the end is the same as in step 2 (run it again and include it).

## Finish

**11. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T028
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**12. Tell the project owner** the RESULT line, the report's path, and: "please push".
