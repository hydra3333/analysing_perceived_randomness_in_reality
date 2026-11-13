"""Write TASK_T023.md (CRLF, US-ASCII) from one table of paths (Claude web chat, 13 November 2026)."""
import sys

MAIN = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality'
WF = MAIN + r'\CLAUDE_CODE_WORKING_FOLDER_TREE'
PY = MAIN + r'\.venv\Scripts\python.exe'
CC = WF + r'\tools\cc_clone.py'
T = WF + r'\scratch\T023'
CLONE = T + r'\r'
PKG = T + r'\p\MHUPA_TESTFIX_r1'
FIX = 'exchange/CLAUDE_WEB_TOOLS/mhupa/postinstall/fix_tests_r1'
ZIP_SHA = '839a31c3fc7ed75a27fbe66c2323ad0450411449f3fe9e6701ea6f0dcb2d452e'
H1, H2 = ('a0923a5ba576a0c48c72b05ca982b156ffd4510616dba92780c8993811e9c44e',
          'c82231a1e33e1ecc1d2bbda790baf3f80e1c7bfcdf3ec573befa992e2d432b47')
py, cc = f'"{PY}"', f'"{PY}" -I "{CC}"'
steps = []
def S(t, c, e):
    steps.append((t, c if isinstance(c, list) else [c], e))
S('Python.', f'{py} -I -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.platform())"',
  'Expected: the venv path, a Python version, and a Windows platform line.')
S("The main repository's state** (read-only; record the output; this step does not stop the task).**",
  ['git status --short', 'git rev-parse HEAD', 'git log -1 --format=%s'], '')
S('Make the task clone.', f'{cc} make --task T023',
  "Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines (the same commit), the `core.autocrlf` line, then `MAKE PASS`.")
S("Check and extract the reviewed fix** (from the clone's own copy).**",
  f'{cc} unzip --task T023 --zip {FIX}/MHUPA_TESTFIX_r1.zip --sha256 {ZIP_SHA}',
  f'Expected: `ZIP SHA-256: {ZIP_SHA}`, then `UNZIP PASS: 3 files extracted into ...`.')
S('Put the two reviewed test files into the clone** (the plan file names the two tracked files they replace).**',
  f'{cc} overlay --task T023 --src "{PKG}\\overlay" --plan {FIX}/TASK_T023_overlay_plan.txt',
  'Expected: `plan ...: 2 REPLACE, 0 REMOVE; SHA-256 ...`, then `OVERLAY PASS: 2 files copied into ... (0 new, 2 replaced); 0 tracked file(s) removed with git rm`.')
S('The two files are in place** (read-only).**',
  f'{cc} verify-overlay --task T023 --src "{PKG}\\overlay" --plan {FIX}/TASK_T023_overlay_plan.txt',
  'Expected: `plan ...: 2 REPLACE, 0 REMOVE; ...`, then `VERIFY-OVERLAY PASS: 2 overlay files identical in the clone; 0 removed file(s) absent`.')
S("The two files' SHA-256 in the clone** (read-only; the clone's copy of each file the fix carries).**",
  f'{py} -I -c "import hashlib, pathlib; r = pathlib.Path(r\'{CLONE}\'); o = pathlib.Path(r\'{PKG}\') / \'overlay\'; [print(hashlib.sha256((r / f.relative_to(o)).read_bytes()).hexdigest(), f.relative_to(o).as_posix()) for f in sorted(o.rglob(\'*.py\'))]"',
  f'Expected exactly: `{H1} tests/mhupa_slice2_fixtures.py` and `{H2} tests/test_mhupa_install_records.py` (the values the reviewer checked, EX_165). Any other value: STOP.')
S("Module origin** (the tests must use the clone's code, not the main repository's).**",
  f'{py} -I "{WF}\\tools\\check_module_origin.py" --repo "{CLONE}"',
  'Expected: every module line starts `ok`, then `ORIGIN PASS`.')
S('All 571 tests, including E2R-T12** (about 25 minutes; see "Recording" for how to run it).**',
  f'{py} -I "{PKG}\\tools\\RUN_MHUP_A_SUITE.py" --repo "{CLONE}"',
  'Expected: one line per module, then `total ran 571 (expected 571); ...` and `SUITE PASS: all 571 tests ran and passed; only the allowed symlink skips, if any.` Up to 4 symlink skips are allowed on Windows; the runner itself decides. Record the whole output as printed. If it prints failure detail, copy it exactly (test names and messages only; if any line appears to contain a draw\'s numbers, put `[line withheld: possible data value]` instead and say so under Deviations).')
S('The clone is otherwise unchanged by the run** (read-only).**',
  f'{cc} git --task T023 -- status --short --untracked-files=no',
  'Expected: exactly two lines, ` M tests/mhupa_slice2_fixtures.py` and ` M tests/test_mhupa_install_records.py`, then `GUARD PASS (after); git status exit code 0`.')

w, out = None, []
w = out.append
w('# TASK_T023 - Windows suite run of the reviewed MHUP-A post-install test fix r1, in a task clone (no change to the main repository)')
w('')
w('**Task ID:** T023. **Date:** 13 November 2026. **Author:** the Claude web chat. Rulebook v0.5; section 2A (T016 only) does not apply.')
w('')
w('**Purpose.** MHUP-A is installed (commits `2860e86` and `effc179`). Eight tests then failed on `main` because they copied the repository\'s live install records and assumed the state before the install. The reviewed fix r1 (EX_165, R-2 PASS) changes only `tests/test_mhupa_install_records.py` and `tests/mhupa_slice2_fixtures.py`. This task runs the whole suite on Windows with those two files put into a disposable task clone that cannot push. If it passes, the project owner commits the two files himself, under his own separate approval.')
w('')
w('**What it does not do.** It changes nothing in the main repository (only this task\'s report is committed there). It runs no launcher, coordinator, updater, Mode H command, process tool, records tool, report tool or `.bat`, and no other program than the ones below (the tests themselves start the updater\'s offline self-test and small Python workers on invented data, as they are written to). It reads no real data itself and contacts no website. "No change" means the main repository: the clone and the tests write to their own temporary folders.')
w('')
w('## Owner options')
w('')
w('- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish by themselves) runs in step 9. The project owner approves it for this run by giving this task.')
w('')
w('## Paths')
w('')
w('| Name | Full path |')
w('|---|---|')
for n, v in (('MAIN (the main repository)', MAIN), ("PY (the main venv's Python)", PY), ('TOOLS', WF + r'\tools'),
             ('CLONE (the task clone)', CLONE), ('PKG (the extracted fix)', PKG)):
    w(f'| {n} | `{v}` |')
w('')
w('Run each command from MAIN, exactly as written. On anything other than the expected output and exit code 0: **STOP**, record the output, and go to step 11 (clean-up). Never retry, repair or reorder a step.')
w('')
w('**Recording** (so that nothing improvised is needed):')
w('- Write `CLAUDE_CODE_WORKING_FOLDER_TREE\\outbox\\REPORT_T023.md` as you go: after each step, add its command, its exit code and its full output, before starting the next step.')
w('- Exit codes: the program\'s own. Do not pipe a command into another program (no `| tee`); in Git Bash, `echo $?` straight after the command gives its exit code.')
w('- Step 9 is longer than the shell\'s foreground limit. Run it in the background with its output redirected to `CLAUDE_CODE_WORKING_FOLDER_TREE\\scratch\\T023\\suite_output.txt` (`> <that file> 2>&1`), with nothing else added; wait until it ends; then put its exit code and the whole file into the report before step 10. The file goes with the clean-up.')
w('')
w('## Steps')
w('')
for i, (title, cmds, expect) in enumerate(steps, 1):
    if title.endswith('**'):
        head, tail = title.split('**', 1)
        w(f'**{i}. {head}**{tail[:-2]}')
    else:
        w(f'**{i}. {title}**')
    w('```')
    for c in cmds:
        w(c)
    w('```')
    if expect:
        w(expect)
    w('')
n = len(steps)
w('## Clean-up (always, whether the task passed or stopped)')
w('')
w(f'**{n + 1}. Remove the task clone and the extracted fix.**')
w('```')
w(f'{cc} remove --task T023')
w('```')
w(f'Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, do not run step {n + 3}, and tell the project owner.')
w('')
w('## Report')
w('')
w(f'**{n + 2}. Finish** `{WF}\\outbox\\REPORT_T023.md` in the format of `outbox\\README.md` (the step table and the RESULT line at the top). Also record:')
w('- the wall-clock time of step 9;')
w(f'- whether the main repository\'s `git status --short` after step {n + 1} is the same as in step 2 (run it again and include it).')
w('')
w('## Finish')
w('')
w(f'**{n + 3}. Commit the report** (one file; not pushed).')
w('```')
w(f'{cc} commit-report --task T023')
w('```')
w('Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.')
w('')
w(f'**{n + 4}. Tell the project owner** the RESULT line, the report\'s path, and: "please push".')
text = '\r\n'.join(out) + '\r\n'
open(sys.argv[1], 'wb').write(text.encode('ascii'))
print(f'{n} steps written to {sys.argv[1]}')
