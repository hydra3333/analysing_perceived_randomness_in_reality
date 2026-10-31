# TASK_T011 - Windows rehearsal of the CODE-3 and E_1 revision 2 install (five steps behind a barrier), in a task clone

**Task ID:** T011. **Date:** 31 October 2026. **Author:** the Claude web chat. The pattern of T009 and T010, for the CODE-3 and E_1 revision 2 package (`E1R2_Install_v3`, base: the project owner's WF-1A install commit `0d98706`), whose install runs in five steps behind a temporary barrier (design v0.1r2 section 5, owner decision ER-2r1): E_1's `IN_DEVELOPMENT.txt` is copied first and deleted last. The package adds 31 files and 2 release entries and replaces 7 files (named in step 8 with `--replace`); it deletes nothing that Git tracks. As in T009 and T010, step 17 asks for the whole status output, copied as printed.

**Purpose.** Run the package (`exchange/EX_096_Claude/E1R2_Install_v3.zip`) on the owner's Windows machine, in a disposable task clone that cannot push, so the main repository is not changed at all. It shows each of the verifier's six phases on a real Windows checkout before the owner's own install. It is a rehearsal only: it installs nothing, releases nothing, runs no batch and reads no real data. It is not the owner's install or the reviewer's RECHECK, and it may run while that RECHECK is pending.

It differs from the owner's real install in three ways: it runs in a task clone; files are copied by `tools\cc_clone.py overlay` (not `xcopy`) and the barrier is deleted with `del` inside the clone; and there is no `git pull` and no push. All 350 tests run, including E2R-T12.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish normally) is run in step 15, as in T008 to T010. The project owner approves it for this rehearsal by giving this task.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| TOOLS | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools` |
| CLONE (the task clone) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\r` |
| PKG (the extracted package) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\p\E1R2_Install_v3` |

The commands below are written out in full. Run each from MAIN (your normal workspace folder). On anything other than the expected PASS line, or a non-zero exit code: **STOP**, record the output, and go to step 21 (clean-up).

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
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T011
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines, the `core.autocrlf` line, then `MAKE PASS`.

**4. Check and extract the package** (from the clone's own copy of EX_096).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T011 --zip exchange/EX_096_Claude/E1R2_Install_v3.zip --sha256 8547fd37fea6e5dc6a1f1941322cc5844031f2351bd50fb4c1ee1179086a2394
```
Expected: `ZIP SHA-256: 8547fd37...2394`, then `UNZIP PASS: 44 files extracted ...`.

**5. PRE check** (step 0 of the install).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" guard --task T011
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\p\E1R2_Install_v3\VERIFY_E1R2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\r" --phase pre
```
Expected: `GUARD PASS`, then `PRE PASS`.

**6. Step 1: copy the barrier** (one new file).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T011 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\p\E1R2_Install_v3\barrier_overlay"
```
Expected: `OVERLAY PASS: 1 files copied into ... (1 new, 0 replaced)`.

**7. BARRIER check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\p\E1R2_Install_v3\VERIFY_E1R2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\r" --phase barrier
```
Expected: `BARRIER PASS: E_1 is closed by its IN_DEVELOPMENT.txt flag; nothing else has changed.`.

**8. Step 2: copy the code** (31 new files, and the 7 named replacements).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T011 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\p\E1R2_Install_v3\repo_overlay" --replace src/methods/E_001/multigame_e1.py src/methods/E_001_Historical_Appearance_Frequency.py src/methods/_common/walk_forward.py src/methods/contract_adapters/e_001.py tests/test_e2r_dispatch.py tests/test_rel1_release.py tests/test_wf1a_walk_forward.py
```
Expected: `OVERLAY PASS: 38 files copied into ... (31 new, 7 replaced)`.

**9. CODE check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\p\E1R2_Install_v3\VERIFY_E1R2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\r" --phase code
```
Expected: `CODE PASS: the barrier is in place; exactly the 31 new paths and 7 modified files, with the expected bytes; the archive equals the base commit; no release entry yet.`.

**10. Step 3: copy the release entries** (2 new files).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T011 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\p\E1R2_Install_v3\release_overlay"
```
Expected: `OVERLAY PASS: 2 files copied into ... (2 new, 0 replaced)`.

**11. RELEASE check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\p\E1R2_Install_v3\VERIFY_E1R2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\r" --phase release
```
Expected: `RELEASE PASS: the barrier is in place; the 2 release entries are present, linked and name revision 2; everything else as in the code phase.`.

**12. Step 4: delete the barrier** (inside the task clone only; Windows CMD).
```
del "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\r\src\methods\E_001\IN_DEVELOPMENT.txt"
```
Expected: no output, exit code 0. (If your shell is PowerShell, run it as `cmd /c del "..."` with the same path.)

**13. POST check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\p\E1R2_Install_v3\VERIFY_E1R2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\r" --phase post
```
Expected: `POST PASS: the barrier is gone; exactly the 31 new paths, 2 release entries and 7 modified files, all with the expected bytes; the archive equals the base commit.`.

**14. Module origin** (the tests must use the clone's code, not the main repository's).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\r"
```
Expected: every module line starts `ok`, the contract-data and registry lines (now 82 declarations and 202 registry chains), then `ORIGIN PASS`.

**15. All 350 tests, including E2R-T12** (the package's own runner).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\p\E1R2_Install_v3\RUN_E1R2_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\r"
```
Expected: `SUITE PASS: all 350 tests ran and passed`. Up to 3 symlink skips are allowed on Windows; the runner itself decides, so record its output as printed, including each module's time.

**16. Stage in the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T011 -- add archive doc review src tests
```
Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git add exit code 0`.

**17. Status in the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T011 -- status --short
```
Expected: 40 lines: 33 starting with `A` and 7 starting with `M`, no `IN_DEVELOPMENT.txt`, and `git status exit code 0`. In the report, copy the whole output exactly as printed, all 40 lines. Do not redirect the output to a file and do not count it with another command; Claude checks the counts from the report.

**18. Commit in the clone** (this commit exists only in the task clone and is deleted with it).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T011 -- commit -q -m "E1R2 rehearsal (task clone T011 only; never pushed)"
```
Expected: `git commit exit code 0`.

**19. COMMITTED check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\p\E1R2_Install_v3\VERIFY_E1R2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T011\r" --phase committed
```
Expected: `COMMITTED PASS: ... added exactly 33 files and modified 7; all Git blobs match; no barrier; the archive equals the base commit.`.
(In a task clone, if this STOPs, the identity report's "upstream" lines will say there is no upstream; that is expected and is not the cause.)

**20. Final state of the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T011 -- log --oneline -2
```
Expected: the rehearsal commit on top of the clone's starting commit, and `git log exit code 0`.

## Clean-up (always, whether the task passed or stopped)

**21. Remove the task clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T011
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, and do not run step 23; tell the project owner.

## Report

**22. Write** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T011.md` in the format of `outbox\README.md`, with every step's command, exit code and full output (step 17 as described there). Also record:
- the wall-clock time step 15 took;
- whether the main repository's `git status --short` after step 21 is the same as in step 2 (run it again and include it).

## Finish

**23. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T011
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**24. Tell the project owner** the RESULT line, the report's path, and: "please push".
