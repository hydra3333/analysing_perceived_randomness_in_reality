"""Write TASK_T012 (Claude Code rehearsal of the WF-1B install). Usage: make_t012.py ZIP_REPO_PATH ZIP_SHA256 N_NEW N_MOD SUITE_N BASE OUT"""
import sys
zp, zsha, nnew, nmod, suite, base, out = sys.argv[1:8]
M = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality'
PY = M + r'\.venv\Scripts\python.exe'
T = M + r'\CLAUDE_CODE_WORKING_FOLDER_TREE\tools'
C = M + r'\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T012\r'
P = M + r'\CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\T012\p\WF1B_Install_v2'
total = int(nnew) + int(nmod)
text = f"""# TASK_T012 - Windows rehearsal of the WF-1B install (the scorer and ranking report), in a task clone

**Task ID:** T012. **Date:** 31 October 2026. **Author:** the Claude web chat. The pattern of T009 and T010, for the WF-1B package (`WF1B_Install_v2`, base `{base[:7]}`). The package adds {nnew} files and replaces {nmod} (`.gitignore`); it deletes nothing. As in T009 to T011, step 13 asks for the whole status output, copied as printed.

**Purpose.** Run the package (`{zp}`) on the owner's Windows machine, in a disposable task clone that cannot push, so the main repository is not changed at all. It shows the verifier's three phases and the whole suite on a real Windows checkout before the owner's own install. It is a rehearsal only: it installs nothing, runs no report and no batch, and reads no real data itself (the project's accepted tests read what they are written to read, rulebook rule 2.5). It may run while the reviewer's code review is pending.

It differs from the owner's real install in three ways: it runs in a task clone; files are copied by `tools\\cc_clone.py overlay` (not `xcopy`); and there is no `git pull` and no push. All {suite} tests run, including E2R-T12 and the new cross-platform test, whose result is the first Windows evidence that the scorer's figures are byte-identical to Linux.

## Owner options

- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish normally) is run in step 11, as in T008 to T011. The project owner approves it for this rehearsal by giving this task.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `{M}` |
| PY (the main venv's Python) | `{PY}` |
| TOOLS | `{T}` |
| CLONE (the task clone) | `{C}` |
| PKG (the extracted package) | `{P}` |

The commands below are written out in full. Run each from MAIN (your normal workspace folder). On anything other than the expected PASS line, or a non-zero exit code: **STOP**, record the output, and go to step 17 (clean-up).

## Steps

**1. Python.**
```
"{PY}" -I -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.platform())"
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
"{PY}" -I "{T}\\cc_clone.py" make --task T012
```
Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines, the `core.autocrlf` line, then `MAKE PASS`.

**4. Check and extract the package** (from the clone's own copy).
```
"{PY}" -I "{T}\\cc_clone.py" unzip --task T012 --zip {zp} --sha256 {zsha}
```
Expected: `ZIP SHA-256: {zsha[:8]}...{zsha[-4:]}`, then `UNZIP PASS: ... files extracted ...`.

**5. PRE check.**
```
"{PY}" -I "{T}\\cc_clone.py" guard --task T012
"{PY}" -I "{P}\\VERIFY_WF1B_INSTALL.py" --repo "{C}" --phase pre
```
Expected: `GUARD PASS`, then `PRE PASS`.

**6. Copy the overlay** ({nnew} new files and the one named replacement).
```
"{PY}" -I "{T}\\cc_clone.py" overlay --task T012 --src "{P}\\repo_overlay" --replace .gitignore
```
Expected: `OVERLAY PASS: {total} files copied into ... ({nnew} new, {nmod} replaced)`.

**7. POST check.**
```
"{PY}" -I "{P}\\VERIFY_WF1B_INSTALL.py" --repo "{C}" --phase post
```
Expected: `POST PASS: exactly the {nnew} expected new paths, {nmod} modified files and 0 staged deletions, all with the expected bytes.`.

**8. Module origin** (the tests must use the clone's code, not the main repository's).
```
"{PY}" -I "{T}\\check_module_origin.py" --repo "{C}"
```
Expected: every module line starts `ok`, then `ORIGIN PASS`.

**9. The new report wrapper is in place** (read-only listing).
```
dir "{C}\\Run_Method_Rankings.bat" "{C}\\src\\evaluation"
```
Expected: the wrapper and the `src\\evaluation` folder's files are listed. (If your shell is PowerShell, run it as `cmd /c dir ...` with the same paths.)

**10. Record the clone's Python files under `src\\evaluation`** (read-only).
```
"{PY}" -I -c "import pathlib; r = pathlib.Path(r'{C}') / 'src' / 'evaluation'; print(sorted(p.name for p in r.glob('*.py')))"
```

**11. All {suite} tests, including E2R-T12** (the package's own runner).
```
"{PY}" -I "{P}\\RUN_WF1B_SUITE.py" --repo "{C}"
```
Expected: `SUITE PASS: all {suite} tests ran and passed`. Up to 3 symlink skips are allowed on Windows; the runner itself decides, so record its output as printed, including each module's time. The line for `tests.test_wf1b_crossplatform` is the cross-platform evidence: record it exactly.

**12. Stage in the clone.**
```
"{PY}" -I "{T}\\cc_clone.py" git --task T012 -- add .gitignore Run_Method_Rankings.bat doc review src tests
```
Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git add exit code 0`.

**13. Status in the clone.**
```
"{PY}" -I "{T}\\cc_clone.py" git --task T012 -- status --short
```
Expected: {total} lines: {nnew} starting with `A` and {nmod} starting with `M`, and `git status exit code 0`. In the report, copy the whole output exactly as printed, all {total} lines. Do not redirect the output to a file and do not count it with another command; Claude checks the counts from the report.

**14. Commit in the clone** (this commit exists only in the task clone and is deleted with it).
```
"{PY}" -I "{T}\\cc_clone.py" git --task T012 -- commit -q -m "WF1B rehearsal (task clone T012 only; never pushed)"
```
Expected: `git commit exit code 0`.

**15. COMMITTED check.**
```
"{PY}" -I "{P}\\VERIFY_WF1B_INSTALL.py" --repo "{C}" --phase committed
```
Expected: `COMMITTED PASS: the last commit (...) added exactly {nnew} files, modified {nmod} and deleted 0; all Git blobs match.`.
(In a task clone, if this STOPs, the identity report's "upstream" lines will say there is no upstream; that is expected and is not the cause.)

**16. Final state of the clone.**
```
"{PY}" -I "{T}\\cc_clone.py" git --task T012 -- log --oneline -2
```
Expected: the rehearsal commit on top of the clone's starting commit, and `git log exit code 0`.

## Clean-up (always, whether the task passed or stopped)

**17. Remove the task clone.**
```
"{PY}" -I "{T}\\cc_clone.py" remove --task T012
```
Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, and do not run step 19; tell the project owner.

## Report

**18. Write** `{M}\\CLAUDE_CODE_WORKING_FOLDER_TREE\\outbox\\REPORT_T012.md` in the format of `outbox\\README.md`, with every step's command, exit code and full output (step 13 as described there). Also record:
- the wall-clock time step 11 took;
- whether the main repository's `git status --short` after step 17 is the same as in step 2 (run it again and include it).

## Finish

**19. Commit the report** (one file; not pushed).
```
"{PY}" -I "{T}\\cc_clone.py" commit-report --task T012
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**20. Tell the project owner** the RESULT line, the report's path, and: "please push".
"""
open(out, 'wb').write(text.replace('\n', '\r\n').encode('ascii'))
print('wrote', out)
