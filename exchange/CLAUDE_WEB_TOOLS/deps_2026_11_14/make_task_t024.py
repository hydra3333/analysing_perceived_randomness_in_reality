"""Write TASK_T024.md (CRLF, US-ASCII) from one table of paths (Claude web chat, 14 November 2026)."""
import sys

MAIN = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality'
WF = MAIN + r'\CLAUDE_CODE_WORKING_FOLDER_TREE'
PY = MAIN + r'\.venv\Scripts\python.exe'
CC = WF + r'\tools\cc_clone.py'
T = WF + r'\scratch\T024'
CLONE = T + r'\r'
PKG = T + r'\p\MHUPA_TESTFIX_r1'
FIX = 'exchange/CLAUDE_WEB_TOOLS/mhupa/postinstall/fix_tests_r1'
ENVCHK = r'exchange\CLAUDE_WEB_TOOLS\deps_2026_11_14\env_freeze_check.py'
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
S('Make the task clone.', f'{cc} make --task T024',
  "Expected: `GUARD PASS`, `git remote -v: ''`, the two HEAD lines (the same commit), the `core.autocrlf` line, then `MAKE PASS`.")
S("Extract the suite runner** (from the clone's own copy of the reviewed T023 package; only its runner is used, nothing is put into the clone).**",
  f'{cc} unzip --task T024 --zip {FIX}/MHUPA_TESTFIX_r1.zip --sha256 {ZIP_SHA}',
  f'Expected: `ZIP SHA-256: {ZIP_SHA}`, then `UNZIP PASS: 3 files extracted into ...`.')
S("Module origin** (the tests must use the clone's code, not the main repository's).**",
  f'{py} -I "{WF}\\tools\\check_module_origin.py" --repo "{CLONE}"',
  'Expected: every module line starts `ok`, then `ORIGIN PASS`.')
S("The environment freeze check** (read-only; the clone's copy of the check; it reads the venv and its base Python only, and prints package names, versions, file names and one digest).**",
  f'{py} -I -B "{CLONE}\\{ENVCHK}" --repo "{CLONE}"',
  'Expected: either `ENV PASS: <n> distributions, no orphan, ...; environment digest <64 hex>` with exit code 0, or `ENV REFUSED: ...` followed by a list of problems, with exit code 3. **Both are findings, not a STOP:** record the whole output and go on to step 7. Any other output or exit code (a traceback, `USAGE`) is a STOP.')
OUTF = (T + r'\suite_output.txt').replace('\\', '/')
S('All 571 tests, including E2R-T12** (about 25 minutes; run this one line as a single background command in Git Bash; see "Recording").**',
  f'{py} -I "{PKG}\\tools\\RUN_MHUP_A_SUITE.py" --repo "{CLONE}" > "{OUTF}" 2>&1; echo "RUNNER EXIT CODE $?" >> "{OUTF}"',
  'Expected, in the file `scratch\\T024\\suite_output.txt` once the command has ended: as its last line `RUNNER EXIT CODE 0` (the suite runner\'s own exit status, written by the same shell straight after it); before it, one line per module, then `total ran 571 (expected 571); ...` and `SUITE PASS: all 571 tests ran and passed; only the allowed symlink skips, if any.` Up to 4 symlink skips are allowed on Windows; the runner itself decides. Record the whole output as printed. If it prints failure detail, copy it exactly (test names and messages only; if any line appears to contain a draw\'s numbers, put `[line withheld: possible data value]` instead and say so under Deviations).')
S('The clone has no tracked change and no new untracked file** (read-only; Git-ignored files are not examined).**',
  f'{cc} git --task T024 -- status --short',
  'Expected: nothing between the GUARD lines; then `GUARD PASS (after); git status exit code 0`. Any other line: STOP and report it; never delete anything to obtain a pass.')

w, out = None, []
w = out.append
w('# TASK_T024 - after the owner\'s dependency change: the environment freeze check and the whole suite on Windows, in a task clone (no change to the main repository)')
w('')
w('**Task ID:** T024. **Date:** 14 November 2026. **Author:** the Claude web chat. Rulebook v0.5; section 2A (T016 only) does not apply.')
w('')
w('**Purpose.** On 14 November 2026 the project owner ran his edited dependency installer, which installed or upgraded many packages in the project venv. The project rule after any dependency change is to stop until the offline suite passes, and Mode H freezes the venv at Approval 1, refusing any file under site-packages that no package RECORD lists. This task checks both on Windows, with the venv as it now is: (a) the environment freeze check, read-only, exactly as Mode H\'s `manifest` would make it; (b) the whole suite (571 tests) in a disposable task clone of `main` that cannot push. It changes no package and no file of the main repository.')
w('')
w('**What it does not do.** It changes nothing in the main repository (only this task\'s report is committed there). It runs no launcher, coordinator, updater, Mode H command, process tool, records tool, report tool or `.bat`, and no other program than the ones below (the tests themselves start the updater\'s offline self-test and small Python workers on invented data, as they are written to). It reads no real data itself and contacts no website. "No change" means the main repository: the clone and the tests write to their own temporary folders. It never runs `pip` or any installer, and changes no venv.')
w('')
w('## Owner options')
w('')
w('- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish by themselves) runs in step 7. The project owner approves it for this run by giving this task.')
w('')
w('## Paths')
w('')
w('| Name | Full path |')
w('|---|---|')
for n, v in (('MAIN (the main repository)', MAIN), ("PY (the main venv's Python)", PY), ('TOOLS', WF + r'\tools'),
             ('CLONE (the task clone)', CLONE), ('PKG (the extracted T023 package; its runner only)', PKG)):
    w(f'| {n} | `{v}` |')
w('')
w('Run each command from MAIN, exactly as written. On anything other than the expected output and exit code 0: **STOP**, record the output, and go to step 9 (clean-up). Step 6 is the one exception, as it says. Never retry, repair or reorder a step.')
w('')
w('**Recording** (so that nothing improvised is needed):')
w('- Write `CLAUDE_CODE_WORKING_FOLDER_TREE\\outbox\\REPORT_T024.md` as you go: after each step, add its command, its exit code and its full output, before starting the next step.')
w('- Exit codes: the program\'s own. Do not pipe a command into another program (no `| tee`); in Git Bash, `echo $?` straight after the command gives its exit code.')
w('- Step 7 is longer than the shell\'s foreground limit, so its command line already carries its own recording: run that exact line as one background command in Git Bash, and wait until the background command has finished. Its output and, on the last line, the suite runner\'s own exit status (`RUNNER EXIT CODE <n>`, written by the same shell straight after the runner ends) are in `scratch\\T024\\suite_output.txt`. Copy the whole file into the report before step 8. If that last line is missing or is not `RUNNER EXIT CODE 0`, that is a STOP: never infer a pass from the other lines, and never take an exit status from another shell or from the launch of the background command. The file goes with the clean-up.')
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
w(f'**{n + 1}. Remove the task clone and the extracted package.**')
w('```')
w(f'{cc} remove --task T024')
w('```')
w(f'Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, do not run step {n + 3}, and tell the project owner.')
w('')
w('## Report')
w('')
w(f'**{n + 2}. Finish** `{WF}\\outbox\\REPORT_T024.md` in the format of `outbox\\README.md` (the step table and the RESULT line at the top). Also record:')
w('- the wall-clock time of step 7;')
w(f'- whether the main repository\'s `git status --short` after step {n + 1} is the same as in step 2 (run it again and include it).')
w('')
w('## Finish')
w('')
w(f'**{n + 3}. Commit the report** (one file; not pushed).')
w('```')
w(f'{cc} commit-report --task T024')
w('```')
w('Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.')
w('')
w(f'**{n + 4}. Tell the project owner** the RESULT line, the report\'s path, and: "please push".')
text = '\r\n'.join(out) + '\r\n'
open(sys.argv[1], 'wb').write(text.encode('ascii'))
print(f'{n} steps written to {sys.argv[1]}')
