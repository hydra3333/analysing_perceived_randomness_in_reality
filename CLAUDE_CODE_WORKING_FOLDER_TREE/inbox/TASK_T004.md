# TASK_T004 - Windows rehearsal of the E2R-CODE-2 install, in a task clone

**Task ID:** T004. **Date:** 29 October 2026. **Author:** the Claude web chat. The same steps as T003, for the FINAL E2R-CODE-2 package (register v0.13 owner-ratified), with E2R-T12, which the project owner approved for this rehearsal on 29 October 2026. New in this task: the package replaces 3 existing files, so step 6 names them with `--replace` (`tools\cc_clone.py` v0.2).

**Purpose.** Run the final E2R-CODE-2 install package v3 (`exchange/EX_046_Claude/E2R_CODE2_Install_v3.zip`) on the owner's Windows machine, but in a disposable task clone that cannot push, so the main repository is not changed at all. This shows how the package's checks and tests behave on a real Windows checkout before the owner's own install. It is a rehearsal only: it installs nothing, authorises nothing, and is not the owner's install or the reviewer's RECHECK.

It differs from the owner's real install in three ways: it runs in a task clone, not the main repository; files are copied by `tools\cc_clone.py overlay`, not `xcopy`; and there is no `git pull` and no push. All 190 tests run, including E2R-T12.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish normally) is run in step 9; the project owner approved it for this rehearsal on 29 October 2026.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| TOOLS | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools` |
| CLONE (the task clone) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T004\r` |
| PKG (the extracted package) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T004\p\E2R_CODE2_Install_v3` |

The commands below are written out in full. Run each from MAIN (your normal workspace folder). On anything other than the expected PASS line, or a non-zero exit code: **STOP**, record the output, and go to step 15 (clean-up).

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
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T004
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines, the `core.autocrlf` line, then `MAKE PASS`.

**4. Check and extract the package** (from the clone's own copy of EX_046).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T004 --zip exchange/EX_046_Claude/E2R_CODE2_Install_v3.zip --sha256 ec643ceab097ca69630594e42551a2c7c4fc5ef5b4d8e6e593a7489a694c6969
```
Expected: `ZIP SHA-256: ec643cea...6969`, then `UNZIP PASS: ... files extracted`.

**5. PRE check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" guard --task T004
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T004\p\E2R_CODE2_Install_v3\VERIFY_E2R_CODE2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T004\r" --phase pre
```
Expected: `GUARD PASS`, then `PRE PASS`.

**6. Copy the overlay into the clone** (22 new files, and the 3 named replacements).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T004 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T004\p\E2R_CODE2_Install_v3\repo_overlay" --replace src/methods/E_001_Historical_Appearance_Frequency.py src/methods/_common/multigame_method_registry.py src/methods/_common/multigame_standalone_contract.py
```
Expected: `OVERLAY PASS: 25 files copied into ... (22 new, 3 replaced)`.

**7. POST check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T004\p\E2R_CODE2_Install_v3\VERIFY_E2R_CODE2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T004\r" --phase post
```
Expected: `POST PASS`.

**8. Module origin** (the tests must use the clone's code, not the main repository's).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T004\r"
```
Expected: every module line starts `ok` (now including CODE-2's five modules), the contract-data and registry lines, then `ORIGIN PASS`.

**9. All 190 tests, including E2R-T12** (the package's own runner).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T004\p\E2R_CODE2_Install_v3\RUN_E2R_CODE2_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T004\r"
```
Expected: `SUITE PASS: all 190 tests ran and passed`. Up to 3 symlink skips are allowed on Windows; the runner itself decides, so record its output as printed.

**10. Stage in the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T004 -- add doc review src tests
```
Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git add exit code 0`.

**11. Status in the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T004 -- status --short
```
Expected: 25 lines, 22 starting with `A` and 3 starting with `M` (the 3 replaced files), and `git status exit code 0`. In the report, give the count of lines, the count starting with `A`, and every line that does not start with `A` (do not paste all 25 lines).

**12. Commit in the clone** (this commit exists only in the task clone and is deleted with it).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T004 -- commit -q -m "E2R-CODE-2 rehearsal (task clone T004 only; never pushed)"
```
Expected: `git commit exit code 0`.

**13. COMMITTED check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T004\p\E2R_CODE2_Install_v3\VERIFY_E2R_CODE2_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T004\r" --phase committed
```
Expected: `COMMITTED PASS`. (In a task clone, if this STOPs, the identity report's "upstream" lines will say there is no upstream; that is expected and is not the cause.)

**14. Final state of the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T004 -- log --oneline -2
```
Expected: the rehearsal commit on top of the clone's starting commit, and `git log exit code 0`.

## Clean-up (always, whether the task passed or stopped)

**15. Remove the task clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T004
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, and do not run step 17; tell the project owner.

## Report

**16. Write** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T004.md` in the format of `outbox\README.md`, with every step's command, exit code and full output (step 11 as described there). Also record:
- the wall-clock time step 9 took;
- whether the main repository's `git status --short` after step 15 is the same as in step 2 (run it again and include it).

## Finish

**17. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T004
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**18. Tell the project owner** the RESULT line, the report's path, and: "please push".
