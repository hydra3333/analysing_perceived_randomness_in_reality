# T016 owner sheet - F2 rows 8 and 9: the project owner's results (13 November 2026)

Run by the project owner at the real project root, 13 November 2026, about 17:26-17:35 Australia/Adelaide, by
`OWNER_ROWS_8_9.md`, with the frozen package extracted to `E:\TEMP\MHUPA_Install_v1` (zip SHA-256
`9d8b74657880917bf8a367b083c5e5926bc6803ee989f74c934afdf98156cf76`, checked by certutil). Recorded by the Claude web
chat from the owner's pasted console output, unchanged except that blank prompt lines are left out. Nothing was ended
by any tool or by hand.

**RESULT: row 8 PASS; row 9 PASS.**

## Row 8 - the install check on the ordinary desktop

```
E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality>"%CD%\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=%CD%\transitory_data\no_pycache_ever" "E:\TEMP\MHUPA_Install_v1\repo_overlay\src\package_tools\process_check.py" check-no-runs --root "%CD%" --install "E:\TEMP\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json"
CLEAN
```

## Row 9 - a live launcher child is listed, then CLEAN after it ends by itself

Order of events, as the owner reported it, including two false starts (both harmless; recorded for completeness):
1. A first probe run with id `poc-T016-row9-202611131730` was started out of the sheet's order and was not checked while
   alive. Starting the same id again was refused by the probe's own guard before it did anything:
   `FileExistsError: Probe run already used: poc-T016-row9-202611131730`.
2. Two check runs with no probe alive (the windows swapped): both `CLEAN` (row 8 again). In between, the precondition:
   `dir transitory_data\poc_runs\UNRESOLVED_ORPHAN.json` -> `File Not Found`.
3. The row itself, run id `poc-T016-row9-202611131740`:

Window A:
```
E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality>Run_Experiment.bat POC_Coordinator_Probe.py --poc --case=sleep-timeout --sleep-seconds 120 --run-id poc-T016-row9-202611131740
BEGIN POC_Coordinator_Probe case=sleep-timeout run=poc-T016-row9-202611131740
RESULT {"case":"sleep-timeout","completed":true,"duration_requested_seconds":120.0,"engineering_only":true,"environment":{"sys_prefix":"E:\\SOFTWARE-Win11\\powerball\\analysing_perceived_randomness_in_reality\\.venv"},"probe":"POC_Coordinator_Probe","threads":{"MKL_NUM_THREADS":"1","NUMEXPR_NUM_THREADS":"1","OMP_NUM_THREADS":"1","OPENBLAS_NUM_THREADS":"1"}}
DIGEST a0e34938b0258f9587ed7c39c244e8519eb0dc7567110953fafed1393948b2bb
FINISH POC_Coordinator_Probe SUCCESS
```

Window B, while the probe slept:
```
E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality>"%CD%\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=%CD%\transitory_data\no_pycache_ever" "E:\TEMP\MHUPA_Install_v1\repo_overlay\src\package_tools\process_check.py" check-no-runs --root "%CD%" --install "E:\TEMP\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json"
  PID 23124 created 2026-11-13T07:02:10.279709+00:00 parents [25812 > 26316 > 10000 > 2728 > 2568 > 2420] exe 'C:\\Users\\u\\AppData\\Local\\Programs\\Python\\Python315\\python.exe' cwd 'E:\\SOFTWARE-Win11\\powerball\\analysing_perceived_randomness_in_reality\\src\\methods' cmdline ['E:\\SOFTWARE-Win11\\powerball\\analysing_perceived_randomness_in_reality\\.venv\\Scripts\\python.exe', '-u', 'POC_Coordinator_Probe.py', '--poc', '--case=sleep-timeout', '--sleep-seconds', '120', '--run-id', 'poc-T016-row9-202611131740']: executable is the project venv or its base interpreter; current directory under the project root; command line names the project root
  PID 25812 created 2026-11-13T07:02:10.272370+00:00 parents [26316 > 10000 > 2728 > 2568 > 2420] exe 'E:\\SOFTWARE-Win11\\powerball\\analysing_perceived_randomness_in_reality\\.venv\\Scripts\\python.exe' cwd 'E:\\SOFTWARE-Win11\\powerball\\analysing_perceived_randomness_in_reality\\src\\methods' cmdline ['E:\\SOFTWARE-Win11\\powerball\\analysing_perceived_randomness_in_reality\\.venv\\Scripts\\python.exe', '-u', 'POC_Coordinator_Probe.py', '--poc', '--case=sleep-timeout', '--sleep-seconds', '120', '--run-id', 'poc-T016-row9-202611131740']: executable is the project venv or its base interpreter; current directory under the project root; command line names the project root
REFUSED: 2 project Python process(es) listed above (a human lets each end or closes it through its own console; this tool never terminates anything)
```

Window B, after `FINISH ... SUCCESS`:
```
E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality>"%CD%\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=%CD%\transitory_data\no_pycache_ever" "E:\TEMP\MHUPA_Install_v1\repo_overlay\src\package_tools\process_check.py" check-no-runs --root "%CD%" --install "E:\TEMP\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json"
CLEAN
```

## What it shows

- The live child is listed with its PID and start time, both as the venv's redirector (PID 25812) and as the base
  interpreter it starts (PID 23124), each by all three rules of design 6.1: executable, folder under the root, command line
  naming the root. After the probe ended by itself the check is `CLEAN` again.
- The probe wrote only its own Git-ignored folders under `transitory_data\poc_runs\` (the two run ids above); they stay.
- PRE on the current `main` (`138e185`) with the frozen package, checked by the Claude web chat in a clone: PRE PASS (the
  later commits to `.claude/`, `doc/`, `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/` are listed for information).
