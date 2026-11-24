# REPORT_T028 - a probe before build step 3 is coded: three facts about this Windows PC (renames when something is open; the size and time of a backup ZIP; what Python can read of other processes), in the scratch folder on D:

RESULT: PASS

- Task file: inbox/TASK_T028.md at main-repository commit 070b7c4628b1ef9dfde512f43726a2cb3b3016f6
- Run by: Claude Code (local runner), 24 November 2026, from 19:50:25 to 20:00 local time (the PC reports the offset +1030 and the abbreviation CAST)
- Owner options used: defaults (the task file offers none)
- Machine: Windows-11-10.0.26300-SP0; Python 3.15.2 at E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | Python | 0 | the venv path, Python 3.15.2, Windows-11-10.0.26300-SP0 |
| 2 | The main repository's state (read-only; does not stop the task) | 0, 0, 0 | clean working tree; HEAD 070b7c4628b1ef9dfde512f43726a2cb3b3016f6 |
| 3 | The scratch folder is an ordinary folder on D:, and the task folder is not there yet | 0 | SCRATCH CHECK PASS |
| 4 | Make the task scratch folder, copy the probe in by reading, check its SHA-256 | 0 | PROBE COPY PASS |
| 5 | The probe's part "rename" | 0 | PROBE PART rename: FINISHED |
| 6 | (long) The probe's part "zip": an environment-only proxy | 0 (from the file: ZIP EXIT CODE 0) | the command printed nothing to the shell; everything went into zip_part_output.txt |
| 7 | Whether step 6 has ended, and what it recorded | 0 | last two lines PROBE PART zip: FINISHED and ZIP EXIT CODE 0 |
| 8 | The probe's part "processes" | 0 | PROBE PART processes: FINISHED |
| 9 | Clean-up: nothing to remove | - | the scratch folder is left in place, as the task file requires |
| 10 | Finish the report | - | this file |
| 11 | Commit the report (one file; not pushed) | see below | see below |

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
```

EXIT CODE 0

### Step 2
Commands and outputs:

```text
git status --short
EXIT CODE 0
```

(no output: the working tree is clean)

```text
git rev-parse HEAD
070b7c4628b1ef9dfde512f43726a2cb3b3016f6
EXIT CODE 0
```

```text
git log -1 --format=%s
exchange: decision log entry 239, the owner's GO for TASK_T028 r1 and the runner instructions; continuity updated
EXIT CODE 0
```

### Step 3
Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import os, sys; p = r'D:\DELETE_ME'; m = r'D:\DELETE_ME\a_p_r_i_r'; t = r'D:\DELETE_ME\a_p_r_i_r\T028'; same = lambda d: os.path.normcase(os.path.realpath(d)) == os.path.normcase(d); plain = lambda d: os.path.isdir(d) and not os.path.islink(d) and not (getattr(os.lstat(d), 'st_file_attributes', 0) & 0x400) and same(d); notplain = [d for d in (p, m) if os.path.lexists(d) and not plain(d)]; ok = os.path.isdir(p) and not notplain and same(t) and not os.path.lexists(t); print('real path of the scratch folder:', os.path.realpath(p)); print('existing folders above the task folder that are not ordinary folders:', notplain); print('real path the task folder would have:', os.path.realpath(t)); print('task folder there already:', os.path.lexists(t)); print('SCRATCH CHECK PASS' if ok else 'SCRATCH CHECK STOP'); sys.exit(0 if ok else 1)"
```

Output:

```text
real path of the scratch folder: D:\DELETE_ME
existing folders above the task folder that are not ordinary folders: []
real path the task folder would have: D:\DELETE_ME\a_p_r_i_r\T028
task folder there already: False
SCRATCH CHECK PASS
```

EXIT CODE 0

### Step 4
Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import hashlib, os, shutil, sys; s = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\inbox\TASK_T028_probe.py'; t = r'D:\DELETE_ME\a_p_r_i_r\T028'; d = r'D:\DELETE_ME\a_p_r_i_r\T028\TASK_T028_probe.py'; os.makedirs(t); r = os.path.realpath(t); print('real path of the task folder:', r); os.path.normcase(r) == os.path.normcase(t) or sys.exit('PROBE COPY STOP: the task folder is not where its name says; nothing was copied'); shutil.copyfile(s, d); h = hashlib.sha256(open(d, 'rb').read().replace(b'\r\n', b'\n')).hexdigest(); ok = h == '57fde59dc4f56526c1a73e95e006fee63b80bbffa223206740ee64776c6128bf'; print('PROBE SHA-256 (LF):', h); print('PROBE COPY PASS' if ok else 'PROBE COPY STOP'); sys.exit(0 if ok else 1)"
```

Output:

```text
real path of the task folder: D:\DELETE_ME\a_p_r_i_r\T028
PROBE SHA-256 (LF): 57fde59dc4f56526c1a73e95e006fee63b80bbffa223206740ee64776c6128bf
PROBE COPY PASS
```

EXIT CODE 0

### Step 5
Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T028\TASK_T028_probe.py" rename --work "D:\DELETE_ME\a_p_r_i_r\T028"
```

Output:

```text
PROBE PART rename: STARTED 2026-11-24 19:51:25; work folder D:\DELETE_ME\a_p_r_i_r\T028; platform win32
R00 this part works in D:\DELETE_ME\a_p_r_i_r\T028\rename_part
R01 rename a folder that holds files, nothing open: DONE
R02 rename a folder while a file inside it is open for reading in this program: WINDOWS SAID NO (permission refused, Windows code 5)
R03 the same rename after the file is closed: DONE
R04 replace a file (os.replace) while it is open for reading in this program: WINDOWS SAID NO (permission refused, Windows code 5)
R05 remove a file while it is open for reading in this program: WINDOWS SAID NO (permission refused, Windows code 32)
R06 rename a folder while another process has its working folder inside it: WINDOWS SAID NO (permission refused, Windows code 5)
R07 replace a file (os.replace) while another process has it open for reading: WINDOWS SAID NO (permission refused, Windows code 5)
R08 remove a file while another process has it open for reading: WINDOWS SAID NO (permission refused, Windows code 32)
R09 the helper program ended by itself, exit code 0
R10 the rename of R06 again, after the other process has ended: DONE
R11 write a temporary file then replace the real one, 1000 times, without forcing to disk: 1000 done; Windows said no: never; 0.34 seconds
R12 write a temporary file then replace the real one, 1000 times, each file forced to disk first (os.fsync): 1000 done; Windows said no: never; 1.42 seconds
PROBE PART rename: FINISHED
```

EXIT CODE 0

### Step 6 (long)
Started 19:51:41, ended 19:56:22 (local time): a wall-clock time of 4 minutes 41 seconds, measured by `date +%H:%M:%S` run as a command of its own before and after. Started with the shell tool's run-in-background option, as the task file's Recording section requires; nothing else was run until the tool reported that the command had ended.

Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T028\TASK_T028_probe.py" zip --work "D:\DELETE_ME\a_p_r_i_r\T028" --otherwise-environment-of "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality" > "D:/DELETE_ME/a_p_r_i_r/T028/zip_part_output.txt" 2>&1; echo "ZIP EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T028/zip_part_output.txt"
```

The command printed nothing to the shell: everything it printed went into the file, and the probe's own exit status was appended to that file as its last line. The exit code of step 6 is the one in that file (`ZIP EXIT CODE 0`), shown by step 7, not one taken from the shell tool.

### Step 7
First line, which only reads (run once; the `ZIP EXIT CODE` line was already there at the first reading, so no waiting and no repetition was needed):

```text
tail -n 1 "D:/DELETE_ME/a_p_r_i_r/T028/zip_part_output.txt" | tr -d '\r'
```

Output:

```text
ZIP EXIT CODE 0
```

Then, once only:

```text
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T028/zip_part_output.txt"
```

EXIT CODE 0

#### From the file D:\DELETE_ME\a_p_r_i_r\T028\zip_part_output.txt (an environment-only proxy: the main .venv folder alone, not a whole tree and not a backup)

```text
PROBE PART zip: STARTED 2026-11-24 19:51:47; work folder D:\DELETE_ME\a_p_r_i_r\T028; platform win32
Z00 ENVIRONMENT-ONLY PROXY: the source is the `.venv` folder alone of E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality, read only (no whole tree with its own .venv was named, or it is not there). This measures an environment's size and ZIP time. It does NOT measure a whole QA or PROD tree, its source_data or results, or a real backup.
Z02 what the ZIP will hold: 19,059 files, 508.9 MB (508,945,768 bytes); 1 empty folders; largest file 20.6 MB (20,589,056 bytes); longest full path 199 characters
Z03 links, junctions or other reparse points found: 0; folders that could not be listed: 0; files dated before 1980, whose time a ZIP cannot hold: 0
Z04 free space on the work drive: 582208.4 MB (582,208,397,312 bytes)
Z05 the environment digest (specification 13): 11,997 files, 362.5 MB (362,521,202 bytes); read and hashed in 150.6 seconds (the first reading in this run)
Z06 the ZIP at Deflate level 9 (the design's level), each file hashed as it is compressed: 80.1 seconds; 180.2 MB (180,209,930 bytes); 35.4% of the source
Z07 the ZIP read back, every member hashed and compared: 1.8 seconds; members that differ: 0
Z08 every source file read and hashed a second time: 10.5 seconds; files that changed between the two readings: 0
Z09 for comparison only, the ZIP at Deflate level 6: 20.7 seconds; 184.5 MB (184,457,007 bytes); 36.2% of the source
Z10 the environment digest once more, the files now lately read: 5.2 seconds
Z11 the two ZIPs are left in D:\DELETE_ME\a_p_r_i_r\T028\zip_part; this probe removes nothing
PROBE PART zip: FINISHED
ZIP EXIT CODE 0
```

### Step 8
Command:

```text
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "D:\DELETE_ME\a_p_r_i_r\T028\TASK_T028_probe.py" processes --work "D:\DELETE_ME\a_p_r_i_r\T028" --scratch-root "D:\DELETE_ME"
```

Output:

```text
PROBE PART processes: STARTED 2026-11-24 19:56:53; work folder D:\DELETE_ME\a_p_r_i_r\T028; platform win32
P00 this probe is process 7364; started as python.exe of the environment that runs this probe; Python 3.15.2
P01 the helper program was started with the same Python; the process ID Windows gave for it: 28264
P10 psutil 7.2.2: 237 processes; 4 with a Python program name; command lines of other programs it could not read: 125
P11 psutil: python.exe: this probe; its program file: the base Python of that environment; details it could not read: none; working folder is the helper's folder: no
P11 psutil: python.exe: an ancestor of this probe; its program file: the environment that runs this probe; details it could not read: none; working folder is the helper's folder: no
P11 psutil: python.exe: the helper program; its program file: the base Python of that environment; details it could not read: none; working folder is the helper's folder: yes
P11 psutil: python.exe: the helper program; its program file: the environment that runs this probe; details it could not read: none; working folder is the helper's folder: yes
P12 psutil: the helper program appears as 2 Python process(es)
P13 psutil: Windows was started at 2026-11-22 16:09:58 (local time)
P20 standard library (the Toolhelp snapshot): 237 processes; 4 with a Python program name; every program name that begins "py", with its count: {'python.exe': 4}
P21 standard library: python.exe: this probe; its program file: the base Python of that environment; its start time: read
P21 standard library: python.exe: an ancestor of this probe; its program file: the environment that runs this probe; its start time: read
P21 standard library: python.exe: the helper program; its program file: the base Python of that environment; its start time: read
P21 standard library: python.exe: the helper program; its program file: the environment that runs this probe; its start time: read
P22 standard library: of the 4 Python processes, program path read for 4, start time read for 4
P23 standard library: the helper program appears as 2 Python process(es)
P24 standard library: this probe and what started it, by program name: python.exe <- python.exe <- bash.exe <- bash.exe <- bash.exe <- claude.exe <- Code.exe <- Code.exe <- explorer.exe
P25 standard library (the tick count): Windows was started at 2026-11-22 16:09:58 (local time); running for 2 days 3 hours 46 minutes
P26 the two readings name the same Python processes: yes; their start times of Windows differ by 0.0 seconds
P27 this probe's own start time by the two readings differs by 0.000 seconds
P30 the helper program ended by itself, exit code 0
PROBE PART processes: FINISHED
```

EXIT CODE 0

### The main repository's state at the end (step 10)
Command:

```text
git status --short
```

Output:

```text
?? CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T028.md
```

EXIT CODE 0

This differs from step 2 in one way and one way only: this report file, which did not exist at step 2, is now present and untracked. Nothing else in the main repository changed, and nothing under the main `.venv` was changed (step 6 read it only).

### The wall-clock time of step 6, and what its figures are (step 10)
Step 6 ran from 19:51:41 to 19:56:22 local time: 4 minutes 41 seconds of wall-clock time. **Its figures are an environment-only proxy** - the main repository's `.venv` folder alone, read only. They are not the size or the time of a whole tree's backup, and they say nothing of a whole QA or PROD tree, of `source_data` or `results`, or of a real backup. The probe says this itself in its line Z00.

## Clean-up

**Step 9: nothing to remove.** No task clone was made, so there was none to remove. The scratch folder `D:\DELETE_ME\a_p_r_i_r\T028` **was left in place, not removed**, as the task file requires (the project owner deletes it himself when the Claude web chat says it is no longer needed).

Folders created by this task under `D:\DELETE_ME\` (a read-only listing of `D:\DELETE_ME\a_p_r_i_r`, made to satisfy rulebook section 2A item 8; all are still there, none removed):

```text
D:/DELETE_ME/a_p_r_i_r
D:/DELETE_ME/a_p_r_i_r/T028
D:/DELETE_ME/a_p_r_i_r/T028/processes_part
D:/DELETE_ME/a_p_r_i_r/T028/processes_part/helper_flags
D:/DELETE_ME/a_p_r_i_r/T028/processes_part/helper_working_folder
D:/DELETE_ME/a_p_r_i_r/T028/rename_part
D:/DELETE_ME/a_p_r_i_r/T028/rename_part/helper_flags
D:/DELETE_ME/a_p_r_i_r/T028/rename_part/r11_cycles
D:/DELETE_ME/a_p_r_i_r/T028/rename_part/r12_cycles
D:/DELETE_ME/a_p_r_i_r/T028/rename_part/r1_tree_SET_ASIDE
D:/DELETE_ME/a_p_r_i_r/T028/rename_part/r1_tree_SET_ASIDE/inner
D:/DELETE_ME/a_p_r_i_r/T028/rename_part/r2_tree_SET_ASIDE
D:/DELETE_ME/a_p_r_i_r/T028/rename_part/r2_tree_SET_ASIDE/inner
D:/DELETE_ME/a_p_r_i_r/T028/rename_part/r4_files
D:/DELETE_ME/a_p_r_i_r/T028/rename_part/r6_tree_SET_ASIDE
D:/DELETE_ME/a_p_r_i_r/T028/rename_part/r6_tree_SET_ASIDE/inner
D:/DELETE_ME/a_p_r_i_r/T028/rename_part/r7_files
D:/DELETE_ME/a_p_r_i_r/T028/zip_part
```

The task folder `D:\DELETE_ME\a_p_r_i_r\T028` holds, besides those part folders, the copy of the probe (`TASK_T028_probe.py`, made in step 4) and the recorded output of step 6 (`zip_part_output.txt`). The two ZIP files of step 6 are in `zip_part`, left there by the probe (its line Z11). Whether `D:\DELETE_ME\a_p_r_i_r` itself existed before this task is not recorded by any check this task ran: step 3 only checked that, if it existed, it was an ordinary folder, and step 4's `os.makedirs` created it if it was not there. Everything from `T028` downwards was created by this task.

Nothing was copied, moved or sent out of `D:\DELETE_ME\`. The one text copied out is the content of `zip_part_output.txt`, shown by step 7 under the heading that names that file, as the task file directs (rulebook section 2A item 4 and section 7).

## Deviations

None. Every command was run in Git Bash from MAIN, exactly as written in the task file. The only additions were the ones the task file's Recording section permits: `cd` to MAIN before a line, `echo "EXIT CODE $?"` after a line that does not itself write an `EXIT CODE` line, and `date +%H:%M:%S` as a command of its own before and after step 6. Step 6 was started with the shell tool's run-in-background option, as that section requires. No line that shows a path under a user folder appeared in any step's output, so none was withheld.

## Observations

Plain facts only:

- Step 7's first line was run once: the `ZIP EXIT CODE` line was already in the file at the first reading, so no waiting and no repetition was needed.
- Step 6 wrote nothing to the shell; its whole output is the file shown in step 7.
- Two read-only commands were run that are not numbered steps of the task file: the final `git status --short`, which step 10 asks for, and the `find ... -type d` listing of `D:\DELETE_ME\a_p_r_i_r` above, which rulebook section 2A item 8 and step 10 require for the list of folders created. Both only read.
- No warning or unexpected message was printed by any step.
