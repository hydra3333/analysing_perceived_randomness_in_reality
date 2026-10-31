# TASK_T009 - Windows rehearsal of the REL-1 install, in a task clone

**Task ID:** T009. **Date:** 31 October 2026. **Author:** the Claude web chat. The same pattern as T008, for the FINAL REL-1 package v2 (`REL1_Install_v2`: it releases the 39 variants of E_2, E_3, E_4, E_6, E_7, E_8, E_9, E_10, E_17, E_18 and E_19 in both games; WF-1 design v0.1r1; register v0.21, owner-ratified 31 October 2026). Unlike T008, this package also **deletes 11 files** (the `IN_DEVELOPMENT.txt` flags), done in step 7 with `git rm` through `tools\cc_clone.py git` (allowed from `cc_clone.py` v0.3, committed with this task). As in T008, step 12 asks for the whole status output, copied as printed.

**Purpose.** Run the final REL-1 install package (`exchange/EX_086_Claude/REL1_Install_v2.zip`) on the owner's Windows machine, but in a disposable task clone that cannot push, so the main repository is not changed at all. This shows how the package's checks and tests behave on a real Windows checkout before the owner's own install. It is a rehearsal only: it installs nothing, releases nothing, authorises nothing, and is not the owner's install.

It differs from the owner's real install in three ways: it runs in a task clone, not the main repository; files are copied by `tools\cc_clone.py overlay` and deleted by `tools\cc_clone.py git -- rm`, not `xcopy` and plain `git rm`; and there is no `git pull` and no push. All 304 tests run, including E2R-T12.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish normally) is run in step 10, as in T008. The project owner approves it for this rehearsal by giving this task.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| TOOLS | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools` |
| CLONE (the task clone) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r` |
| PKG (the extracted package) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\p\REL1_Install_v2` |

The commands below are written out in full. Run each from MAIN (your normal workspace folder). On anything other than the expected PASS line, or a non-zero exit code: **STOP**, record the output, and go to step 16 (clean-up).

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
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T009
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines, the `core.autocrlf` line, then `MAKE PASS`.

**4. Check and extract the package** (from the clone's own copy of EX_086).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T009 --zip exchange/EX_086_Claude/REL1_Install_v2.zip --sha256 3ca731fe22ffc10a2dd4f59fd5f5725f9f6c88553a426f12eea395795e1e4b36
```
Expected: `ZIP SHA-256: 3ca731fe...4b36`, then `UNZIP PASS: ... files extracted`.

**5. PRE check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" guard --task T009
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\p\REL1_Install_v2\VERIFY_REL1_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r" --phase pre
```
Expected: `GUARD PASS`, then `PRE PASS`.

**6. Copy the overlay into the clone** (92 new files, and the 5 named replacements).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T009 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\p\REL1_Install_v2\repo_overlay" --replace tests/test_e2r_dispatch.py tests/test_e3_e4_polynomial.py tests/test_e6_beta_bernoulli.py tests/test_wave1_frequency.py tests/test_wave2_recurrence.py
```
Expected: `OVERLAY PASS: 97 files copied into ... (92 new, 5 replaced)`.

**7. Delete the 11 flags in the clone** (one command).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T009 -- rm -q -- src/methods/E_002/IN_DEVELOPMENT.txt src/methods/E_003/IN_DEVELOPMENT.txt src/methods/E_004/IN_DEVELOPMENT.txt src/methods/E_006/IN_DEVELOPMENT.txt src/methods/E_007/IN_DEVELOPMENT.txt src/methods/E_008/IN_DEVELOPMENT.txt src/methods/E_009/IN_DEVELOPMENT.txt src/methods/E_010/IN_DEVELOPMENT.txt src/methods/E_017/IN_DEVELOPMENT.txt src/methods/E_018/IN_DEVELOPMENT.txt src/methods/E_019/IN_DEVELOPMENT.txt
```
Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git rm exit code 0`.

**8. POST check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\p\REL1_Install_v2\VERIFY_REL1_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r" --phase post
```
Expected: `POST PASS: exactly the 92 expected new paths, 5 modified files and 11 staged deletions, all with the expected bytes.`

**9. Module origin** (the tests must use the clone's code, not the main repository's).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r"
```
Expected: every module line starts `ok`, the contract-data and registry lines (80 declarations and 202 registry chains), then `ORIGIN PASS`.

**10. All 304 tests, including E2R-T12** (the package's own runner).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\p\REL1_Install_v2\RUN_REL1_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r"
```
Expected: `SUITE PASS: all 304 tests ran and passed`. Up to 3 symlink skips are allowed on Windows; the runner itself decides, so record its output as printed, including each module's time.

**11. Stage in the clone** (the deletions are already staged by step 7).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T009 -- add doc review src tests
```
Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git add exit code 0`.

**12. Status in the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T009 -- status --short
```
Expected: 108 lines: 92 starting with `A`, 5 starting with `M` (the five test files) and 11 starting with `D` (the flags), and `git status exit code 0`. In the report, copy the whole output exactly as printed, all 108 lines. Do not redirect the output to a file and do not count it with another command; Claude checks the counts from the report.

**13. Commit in the clone** (this commit exists only in the task clone and is deleted with it).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T009 -- commit -q -m "REL-1 rehearsal (task clone T009 only; never pushed)"
```
Expected: `git commit exit code 0`.

**14. COMMITTED check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\p\REL1_Install_v2\VERIFY_REL1_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T009\r" --phase committed
```
Expected: `COMMITTED PASS`. (In a task clone, if this STOPs, the identity report's "upstream" lines will say there is no upstream; that is expected and is not the cause.)

**15. Final state of the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T009 -- log --oneline -2
```
Expected: the rehearsal commit on top of the clone's starting commit, and `git log exit code 0`.

## Clean-up (always, whether the task passed or stopped)

**16. Remove the task clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T009
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, and do not run step 18; tell the project owner.

## Report

**17. Write** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T009.md` in the format of `outbox\README.md`, with every step's command, exit code and full output (step 12 as described there). Also record:
- the wall-clock time step 10 took;
- whether the main repository's `git status --short` after step 16 is the same as in step 2 (run it again and include it).

## Finish

**18. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T009
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**19. Tell the project owner** the RESULT line, the report's path, and: "please push".
