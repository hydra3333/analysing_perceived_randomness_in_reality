# TASK_T005 - Windows rehearsal of the E_6 install, in a task clone

**Task ID:** T005. **Date:** 30 October 2026. **Author:** the Claude web chat. The same steps as T004, for the FINAL E_6 package v2 (E_6 revision 1 installed non-runnable, the new-method template and register v0.15, owner-ratified), with E2R-T12, which the project owner approved for this rehearsal on 30 October 2026. The package replaces 3 existing files, named in step 6 with `--replace`.

**Purpose.** Run the final E_6 install package v2 (`exchange/EX_054_Claude/E6_Install_v2.zip`) on the owner's Windows machine, but in a disposable task clone that cannot push, so the main repository is not changed at all. This shows how the package's checks and tests behave on a real Windows checkout before the owner's own install. It is a rehearsal only: it installs nothing, authorises nothing, and is not the owner's install or the reviewer's RECHECK.

It differs from the owner's real install in three ways: it runs in a task clone, not the main repository; files are copied by `tools\cc_clone.py overlay`, not `xcopy`; and there is no `git pull` and no push. All 210 tests run, including E2R-T12.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish normally) is run in step 9; the project owner approved it for this rehearsal on 30 October 2026.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| TOOLS | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools` |
| CLONE (the task clone) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T005\r` |
| PKG (the extracted package) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T005\p\E6_Install_v2` |

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
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" make --task T005
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines, the `core.autocrlf` line, then `MAKE PASS`.

**4. Check and extract the package** (from the clone's own copy of EX_054).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" unzip --task T005 --zip exchange/EX_054_Claude/E6_Install_v2.zip --sha256 eea8e4442285a6569c9060f8076bbebef42a936acae63daf4d15eb1a5bcf3e29
```
Expected: `ZIP SHA-256: eea8e444...3e29`, then `UNZIP PASS: ... files extracted`.

**5. PRE check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" guard --task T005
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T005\p\E6_Install_v2\VERIFY_E6_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T005\r" --phase pre
```
Expected: `GUARD PASS`, then `PRE PASS`.

**6. Copy the overlay into the clone** (40 new files, and the 3 named replacements).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" overlay --task T005 --src "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T005\p\E6_Install_v2\repo_overlay" --replace src/methods/Method_Contract_Runner.py tests/test_e2r_contract.py tests/test_e2r_dispatch.py
```
Expected: `OVERLAY PASS: 43 files copied into ... (40 new, 3 replaced)`.

**7. POST check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T005\p\E6_Install_v2\VERIFY_E6_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T005\r" --phase post
```
Expected: `POST PASS`.

**8. Module origin** (the tests must use the clone's code, not the main repository's).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\check_module_origin.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T005\r"
```
Expected: every module line starts `ok`, the contract-data and registry lines (now 8 declarations and 130 registry chains), then `ORIGIN PASS`.

**9. All 210 tests, including E2R-T12** (the package's own runner).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T005\p\E6_Install_v2\RUN_E6_SUITE.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T005\r"
```
Expected: `SUITE PASS: all 210 tests ran and passed`. Up to 3 symlink skips are allowed on Windows; the runner itself decides, so record its output as printed.

**10. Stage in the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T005 -- add doc review src tests
```
Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git add exit code 0`.

**11. Status in the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T005 -- status --short
```
Expected: 43 lines, 40 starting with `A` and 3 starting with `M` (the 3 replaced files), and `git status exit code 0`. In the report, give the count of lines, the count starting with `A`, and every line that does not start with `A` (do not paste all 43 lines).

**12. Commit in the clone** (this commit exists only in the task clone and is deleted with it).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T005 -- commit -q -m "E_6 rehearsal (task clone T005 only; never pushed)"
```
Expected: `git commit exit code 0`.

**13. COMMITTED check.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T005\p\E6_Install_v2\VERIFY_E6_INSTALL.py" --repo "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T005\r" --phase committed
```
Expected: `COMMITTED PASS`. (In a task clone, if this STOPs, the identity report's "upstream" lines will say there is no upstream; that is expected and is not the cause.)

**14. Final state of the clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" git --task T005 -- log --oneline -2
```
Expected: the rehearsal commit on top of the clone's starting commit, and `git log exit code 0`.

## Clean-up (always, whether the task passed or stopped)

**15. Remove the task clone.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" remove --task T005
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, and do not run step 17; tell the project owner.

## Report

**16. Write** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T005.md` in the format of `outbox\README.md`, with every step's command, exit code and full output (step 11 as described there). Also record:
- the wall-clock time step 9 took;
- whether the main repository's `git status --short` after step 15 is the same as in step 2 (run it again and include it).

## Finish

**17. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T005
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**18. Tell the project owner** the RESULT line, the report's path, and: "please push".
