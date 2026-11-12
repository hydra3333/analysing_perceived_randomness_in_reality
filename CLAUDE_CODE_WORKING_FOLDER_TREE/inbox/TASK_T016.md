# TASK_T016 - MHUP-A install rehearsal in a task clone (Appendix J steps 0 to 18), with F2 rows 5, 6, 7 and 10

**Final (package frozen 11 November 2026, gate A).** The package is `exchange/EX_163_Claude/MHUPA_Install_v1.zip`, SHA-256 `9d8b74657880917bf8a367b083c5e5926bc6803ee989f74c934afdf98156cf76`. Before T016 runs: rulebook v0.5 (section 2A) is installed together with this file (gate B), and the project owner gives T016 its own go, naming that commit. `check_task_commands.py` was run on this file against the settings in force at the freeze (PASS); the F1 deny lines come only after T016 (they would deny 13 of these commands).

**Task ID:** T016. **Date:** 11 November 2026 (written at the package freeze). **Author:** the Claude web chat. Rulebook v0.5, section 2A, is the allowance this task runs under.

**Purpose.** Rehearse the whole MHUP-A installation on the owner's Windows machine, exactly as `INSTALL_INSTRUCTIONS.md` gives it, but in a disposable task clone that cannot push: the package's own tools (process check, copy tool, verifier, suite runner, records tool) run from the extracted package against the clone; the two install commits are made in the clone only. Step 0 is replaced by a clean-tree and HEAD check (the clone is fresh, so there is no pull); step 19 (the push) is omitted. Three EXPECTED REFUSAL steps check on Windows that the tools refuse out-of-order actions. After the install, the task checks the line ends and attributes of the six byte-checked files on Windows Git (F2 row 5), that the byte-code folder was never made (row 10), and the environment inventory on the real interpreter, with a planted-orphan refusal in a scratch copy (rows 6 and 7).

**This is not the installation.** The main repository is not changed (only this task's report is committed there, as always). Nothing is pushed. No program runs at the main repository's root: F2 rows 8 and 9 are the project owner's own checks, on a separate sheet. No launcher, coordinator, updater, Mode H, report tool or `.bat` runs; no process is terminated; no lottery website is contacted; nothing here has a browser. The clone holds the development masters; only the suite runner touches them, as rulebook section 2A, A3 says.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish by themselves) runs inside step 18's suite. The project owner approves it for this run by giving this task.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| TOOLS | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools` |
| CLONE (the task clone) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r` |
| PKG (the extracted package) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1` |
| MAN (its manifest) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json` |
| E (the harness scratch folder of step 42) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\e` |

The commands below are written out in full. Run each from MAIN. A step passes only with its expected output and exit code 0, except the three steps marked **EXPECTED REFUSAL**, which pass only as rulebook section 2A, A5 says (a non-zero exit code, a line beginning with the refusal text given, and no traceback). On anything else: **STOP**, record the output, and go to step 43 (clean-up). Never rerun, skip or reorder a step, and never repair, inspect or recover anything in the clone. **Record as you go** (rulebook section 2A, A6): step 43 removes `scratch\T016` before the report is written, so save each step's exact command, exit code and full output as soon as it ends; on a STOP, also note which step stopped and what it and the steps before it printed about the barriers U, E and P and the records. "Step N" alone means this task's step N; "Appendix J step N" means the step of the install instructions it rehearses.

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

**3. Make the task clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T016
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines (the same commit), the `core.autocrlf` line (either value is fine; record it), then `MAKE PASS`.

**4. Check and extract the package** (from the clone's own copy).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T016 --zip exchange/EX_163_Claude/MHUPA_Install_v1.zip --sha256 9d8b74657880917bf8a367b083c5e5926bc6803ee989f74c934afdf98156cf76
```
Expected: `ZIP SHA-256: 9d8b74657880917bf8a367b083c5e5926bc6803ee989f74c934afdf98156cf76`, then `UNZIP PASS: 80 files extracted into ...`.

**5. Appendix J step 0, task-clone form: the clone is clean** (no pull: the clone is fresh).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T016 -- status --short
```
Expected: `GUARD PASS (before)`, nothing else from Git, then `GUARD PASS (after); git status exit code 0`.

**6. Appendix J step 0, task-clone form: the commit being installed on.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T016 -- rev-parse HEAD
```
Expected: the same full hash as the `clone HEAD:` line of step 3, then `GUARD PASS (after); git rev-parse exit code 0`.

**7. Appendix J step 1: PRE (the verifier; read-only).**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\VERIFY_MHUP_A.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --phase pre
```
Expected: the last lines `PRE PASS: package intact; clean tree; 37 new paths absent; 34 files to replace and 1 to delete at their base version. Nothing was changed.` and `Read-only: ...`.

**8. Appendix J step 2: preflight install check (before U exists).**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\repo_overlay\src\package_tools\process_check.py" check-no-runs --root "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --install "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json"
```
Expected: `CLEAN` (and nothing listed).

**9. Appendix J step 3: take U (the updater lock, in the clone).**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\repo_overlay\src\package_tools\process_check.py" take-install-lock --root "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --package MHUP_A
```
Expected: `CLEAN; install lock taken for MHUP_A`.

**10. EXPECTED REFUSAL (rulebook section 2A, A5): take U a second time.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\repo_overlay\src\package_tools\process_check.py" take-install-lock --root "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --package MHUP_A
```
Expected (all three, section 2A, A5): a non-zero exit code; a line that **begins with** `REFUSED: the updater lock already names an install (INSTALL MHUP_A ` (followed by the time of step 9 and `an earlier install did not finish`); no `Traceback`. Anything else: STOP. That U remains valid and held by this package is checked by steps 11 and 17.

**11. Appendix J step 4: create barrier E.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\MHUPA_COPY.py" barrier --create E --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r"
```
Expected: `BARRIER PASS: E created (src/methods/E_001/IN_DEVELOPMENT.txt)`.

**12. Appendix J step 4: create barrier P.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\MHUPA_COPY.py" barrier --create P --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r"
```
Expected: `BARRIER PASS: P created (src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt)`.

**13. Appendix J step 5: install check, before the gate copy.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\repo_overlay\src\package_tools\process_check.py" check-no-runs --root "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --install "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json"
```
Expected: `CLEAN` (and nothing listed).

**14. Appendix J step 6: copy the 10 dispatch-gate files.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\MHUPA_COPY.py" copy --part gate --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r"
```
Expected: `COPY PASS: part gate: 10 files written and read back`.

**15. Appendix J step 7: install check, after the gate copy.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\repo_overlay\src\package_tools\process_check.py" check-no-runs --root "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --install "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json"
```
Expected: `CLEAN` (and nothing listed).

**16. Appendix J step 8: copy the rest and make the deletion.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\MHUPA_COPY.py" copy --part rest --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r"
```
Expected: `COPY PASS: part rest: 61 files written and read back, 1 deleted`.

**17. Appendix J step 9: POST.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\VERIFY_MHUP_A.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --phase post
```
Expected: `POST PASS: exactly the 37 expected new paths, 34 modified files and 1 deletion, all with the expected bytes.`

**18. Appendix J step 10: the suite on a barrier-free copy (`--shadow`; about 25 minutes or more).**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\RUN_MHUP_A_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --shadow
```
Expected: the runner's POST and copy lines, one line per module, its checks after the suite, the removal of its temporary folder, and finally `SUITE PASS: all 571 tests ran and passed; ...` (at most the four allowed symlink skips; the runner decides). E2R-T12 runs here (owner options). Record the whole output as printed, with each module's time; if it prints failure detail, copy it exactly (it carries test names and messages only; section 2A, A3 says what to do with a line that appears to contain a draw's numbers).

**19. EXPECTED REFUSAL (section 2A, A5): remove E before the package commit.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\MHUPA_COPY.py" barrier --remove E --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r"
```
Expected (all three, section 2A, A5): a non-zero exit code; a line that **begins with** `COPY STOP: barrier E is removed only after COMMITTED PASS (step 15), and the verifier's committed phase does not pass now`; no `Traceback`. Anything else: STOP. That E is still in place is checked by steps 23 and 25 (`E present`).

**20. Appendix J step 11: install check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\repo_overlay\src\package_tools\process_check.py" check-no-runs --root "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --install "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json"
```
Expected: `CLEAN` (and nothing listed).

**21. Appendix J step 12: the install record.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\repo_overlay\src\package_tools\install_records.py" install-record --root "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --package MHUP_A --manifest "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json"
```
Expected: `INSTALL RECORD PASS: ` and the record's path in the clone, ending `install_records\INSTALL_MHUP_A_V1.json`.

**22. Appendix J step 12: stage the package commit** (the paths are read from the package's list).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T016 -- add "--pathspec-from-file=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\STAGE_PACKAGE_COMMIT.txt"
```
Expected: `GUARD PASS (before)`, possibly `warning: ... LF will be replaced by CRLF ...` lines (harmless; record them), then `GUARD PASS (after); git add exit code 0`.

**23. Appendix J step 12: STAGED (the verifier; before the commit).**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\VERIFY_MHUP_A.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --phase staged
```
Expected: `STAGED PASS: the index holds exactly the package commit (73 paths) and nothing else is changed. Commit now.`

**24. Appendix J step 12: the package commit (in the clone only; it never leaves the clone).**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T016 -- commit -q -m "T016 rehearsal: MHUP-A package commit (Appendix J step 12)"
```
Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git commit exit code 0`.

**25. Appendix J step 13: COMMITTED.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\VERIFY_MHUP_A.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --phase committed
```
Expected: `COMMITTED PASS: the package commit (<7 characters>) added exactly 37 files and the install record, modified 34 and deleted 1; all Git blobs match; the install record names this package and manifest; barriers U, E and P in place.`

**26. Appendix J step 14: install check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\repo_overlay\src\package_tools\process_check.py" check-no-runs --root "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --install "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json"
```
Expected: `CLEAN` (and nothing listed).

**27. EXPECTED REFUSAL (section 2A, A5): the release record while E and P still exist.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\repo_overlay\src\package_tools\install_records.py" release-record --root "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --package MHUP_A --manifest "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json"
```
Expected (all three, section 2A, A5): a non-zero exit code; a line that **begins with** `RELEASE RECORD STOP: the install barrier P still exists; the release record follows COMMITTED PASS and the removal of E and P`; no `Traceback`. Anything else: STOP. That no record was written is checked by step 30 (the record is create-only: it STOPs if one exists) and step 32 (the release commit holds exactly 1 path).

**28. Appendix J step 15: remove E** (it re-runs the COMMITTED check first).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\MHUPA_COPY.py" barrier --remove E --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r"
```
Expected: `BARRIER PASS: E removed (src/methods/E_001/IN_DEVELOPMENT.txt)`.

**29. Appendix J step 15: remove P.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\MHUPA_COPY.py" barrier --remove P --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r"
```
Expected: `BARRIER PASS: P removed (src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt)`.

**30. Appendix J step 16: the release record.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\repo_overlay\src\package_tools\install_records.py" release-record --root "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --package MHUP_A --manifest "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json"
```
Expected: `RELEASE RECORD PASS: ` and the record's path in the clone, ending `install_records\RELEASE_MHUP_A_V1.json`.

**31. Appendix J step 17: stage the release commit.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T016 -- add "--pathspec-from-file=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\STAGE_RELEASE_COMMIT.txt"
```
Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git add exit code 0`.

**32. Appendix J step 17: STAGED.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\VERIFY_MHUP_A.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --phase staged
```
Expected: `STAGED PASS: the index holds exactly the release commit (1 paths) and nothing else is changed. Commit now.`

**33. Appendix J step 17: the release commit (in the clone only).**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T016 -- commit -q -m "T016 rehearsal: MHUP-A release commit (Appendix J step 17)"
```
Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git commit exit code 0`.

**34. Appendix J step 17: RELEASED.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\VERIFY_MHUP_A.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --phase released
```
Expected: a line starting `RELEASED PASS: two commits proved: the release commit (`; record the whole output.

**35. Appendix J step 18: RELEASED again** (U is released only if this passes).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\VERIFY_MHUP_A.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --phase released
```
Expected: the same `RELEASED PASS: ...` line as step 34.

**36. Appendix J step 18: release U.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\repo_overlay\src\package_tools\process_check.py" release-install-lock --root "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r" --package MHUP_A
```
Expected: `CLEAN; install lock released for MHUP_A`. (Appendix J step 19, the push, is not part of this task: a task clone never pushes.)

**37. F2 row 5 (N1, N4, N4b on Windows Git): the attributes and line ends of the six byte-checked files.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T016 -- ls-files --eol -- .gitattributes src/methods/_common/contract_data/install_records src/package_tools/process_check.py "src/results*_v0_2.py" "tests/fixtures/*_v0_1_reference.py.txt"
```
Expected: 7 Git lines between the GUARD lines: `.gitattributes`; the three files under `install_records/` (the baseline record, `INSTALL_MHUP_A_V1.json`, `RELEASE_MHUP_A_V1.json`); `process_check.py`; the updater v0.2; the v0.1 reference fixture. Each line but the first must show `i/lf`, `w/lf` and `attr/-text`. Any `w/crlf` on those six, or a missing `-text`: STOP. Copy the whole output.

**38. F2 row 5: the project reader validates the records.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\p\MHUPA_Install_v1\repo_overlay\src\package_tools\install_records.py" validate --root "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r"
```
Expected: `RECORDS PASS: 1 install record(s), 2 release record(s), 80 released unretired entries`.

**39. The clone after the rehearsal: clean, with the two commits on top.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T016 -- status --short
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T016 -- log --format=%s -3
```
Expected: the first command prints nothing between its GUARD lines; the second prints the release commit's subject, the package commit's subject, then the subject of the commit of step 6. Copy both outputs.

**40. F2 row 10: the byte-code folder was never created.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import os; p=r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\transitory_data\no_pycache_ever'; print('NO_PYCACHE_EVER ABSENT' if not os.path.lexists(p) else 'NO_PYCACHE_EVER PRESENT')"
```
Expected: `NO_PYCACHE_EVER ABSENT`.

**41. F2 row 6: the environment inventory on the real Windows interpreter** (reads the main venv and its base Python; writes nothing).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\exchange\CLAUDE_WEB_TOOLS\mhupa\t016\T016_ENV_HARNESS.py" inventory --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\src"
```
Expected: the closure module's path (in the clone), the venv and base paths, the Python and platform line, one line of counts, the environment digest, then `ENV INVENTORY PASS`. `ENV INVENTORY STOP: ...` names the first orphan or mismatch: that is a STOP to report as printed (never delete or change anything in the venv).

**42. F2 row 7: a planted orphan is refused** (in a scratch copy; the real venv is only read).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\exchange\CLAUDE_WEB_TOOLS\mhupa\t016\T016_ENV_HARNESS.py" orphan --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\r\src" --scratch "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T016\e"
```
Expected: `copied <name>.dist-info: ...`, `control PASS: 1 distribution, no orphan`, `refused: 1 file(s) under site-packages that no RECORD lists, the first: T016_PLANTED_ORPHAN.txt`, then `ORPHAN CHECK PASS: the planted file was refused by name`.

## Clean-up (always, whether the task passed or stopped)

**43. Remove the task clone, the extracted package and the harness folder** (all under `scratch\T016`).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T016
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, do not run step 45, and tell the project owner.

## Report

**44. Write** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T016.md` in the format of `outbox\README.md`, with every step's command, exit code and full output. Also record:
- the wall-clock time of step 18;
- for each EXPECTED REFUSAL step (10, 19 and 27), its exit code and its refusal line, in the step table's Result column;
- on a STOP: the step that stopped, its output, and the barrier and record state the outputs up to it showed (from your notes; the clone is gone);
- whether the main repository's `git status --short` after step 43 is the same as in step 2 (run it again and include it).

## Finish

**45. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T016
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**46. Tell the project owner** the RESULT line, the report's path, and: "please push".
