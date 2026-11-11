"""Write the DRAFT TASK_T016.md (CRLF, US-ASCII) from one table of paths (Claude web chat, 11 November 2026).
Usage: python3 -I make_task_t016.py OUT   The placeholders <EX_FOLDER>, <ZIP_SHA256> and the draft counts are fixed
at the package freeze; nothing else changes then."""
import sys

MAIN = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality'
WF = MAIN + r'\CLAUDE_CODE_WORKING_FOLDER_TREE'
PY = MAIN + r'\.venv\Scripts\python.exe'
CC = WF + r'\tools\cc_clone.py'
T = WF + r'\scratch\T016'
CLONE = T + r'\r'
PKG = T + r'\p\MHUPA_Install_v1'
MAN = PKG + r'\PACKAGE_MANIFEST_MHUP_A.json'
NOPYC = CLONE + r'\transitory_data\no_pycache_ever'
HARN = CLONE + r'\exchange\CLAUDE_WEB_TOOLS\mhupa\t016\T016_ENV_HARNESS.py'
ZIP = 'exchange/<EX_FOLDER>/MHUPA_Install_v1.zip'

py = f'"{PY}"'
cc = f'{py} -I "{CC}"'
pcx = f'{py} -I -B -X "pycache_prefix={NOPYC}" "{PKG}\\repo_overlay\\src\\package_tools\\process_check.py"'
irx = f'{py} -I -B -X "pycache_prefix={NOPYC}" "{PKG}\\repo_overlay\\src\\package_tools\\install_records.py"'
ver = f'{py} -I -B "{PKG}\\VERIFY_MHUP_A.py" --repo "{CLONE}" --phase'
cp = f'{py} -I -B "{PKG}\\MHUPA_COPY.py"'
check = f'{pcx} check-no-runs --root "{CLONE}" --install "{MAN}"'
cgit = f'{cc} git --task T016 --'

steps = []          # (title, [commands], expected text)
def S(title, cmds, expect):
    steps.append((title, cmds if isinstance(cmds, list) else [cmds], expect))

CLEAN = 'Expected: `CLEAN` (and nothing listed).'
S('Python.', f'{py} -I -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.platform())"',
  'Expected: the venv path, a Python version, and a Windows platform line.')
S("The main repository's state** (read-only; record the output; this step does not stop the task).**",
  ['git status --short', 'git rev-parse HEAD', 'git log -1 --format=%s'], '')
S('Make the task clone.', f'{cc} make --task T016',
  'Expected: `GUARD PASS`, `git remote -v: \'\'`, the two HEAD lines (the same commit), the `core.autocrlf` line (either value is fine; record it), then `MAKE PASS`.')
S('Check and extract the package** (from the clone\'s own copy).**',
  f'{cc} unzip --task T016 --zip {ZIP} --sha256 <ZIP_SHA256>',
  'Expected: `ZIP SHA-256: <ZIP_SHA256>`, then `UNZIP PASS: 80 files extracted ...` (draft count; fixed at the freeze).')
S('Appendix J step 0, task-clone form: the clone is clean** (no pull: the clone is fresh).**', f'{cgit} status --short',
  'Expected: `GUARD PASS (before)`, nothing else from Git, then `GUARD PASS (after); git status exit code 0`.')
S('Appendix J step 0, task-clone form: the commit being installed on.', f'{cgit} rev-parse HEAD',
  'Expected: the same full hash as the `clone HEAD:` line of step 3, then `GUARD PASS (after); git rev-parse exit code 0`.')
S('Appendix J step 1: PRE (the verifier; read-only).', f'{ver} pre',
  'Expected: the last lines `PRE PASS: package intact; clean tree; 37 new paths absent; 34 files to replace and 1 to delete at their base version. Nothing was changed.` and `Read-only: ...`.')
S('Appendix J step 2: preflight install check (before U exists).', check, CLEAN)
S('Appendix J step 3: take U (the updater lock, in the clone).', f'{pcx} take-install-lock --root "{CLONE}" --package MHUP_A',
  'Expected: `CLEAN; install lock taken for MHUP_A`.')
S('EXPECTED REFUSAL (rulebook section 2A, A5): take U a second time.', f'{pcx} take-install-lock --root "{CLONE}" --package MHUP_A',
  'Expected (all three, section 2A, A5): a non-zero exit code; a line that **begins with** `REFUSED: the updater lock already names an install (INSTALL MHUP_A ` (followed by the time of step 9 and `an earlier install did not finish`); no `Traceback`. Anything else: STOP. That the lock is unchanged is checked by steps 11 and 17 (they need U held by this package).')
S('Appendix J step 4: create barrier E.', f'{cp} barrier --create E --repo "{CLONE}"',
  'Expected: `BARRIER PASS: E created (src/methods/E_001/IN_DEVELOPMENT.txt)`.')
S('Appendix J step 4: create barrier P.', f'{cp} barrier --create P --repo "{CLONE}"',
  'Expected: `BARRIER PASS: P created (src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt)`.')
S('Appendix J step 5: install check, before the gate copy.', check, CLEAN)
S('Appendix J step 6: copy the 10 dispatch-gate files.', f'{cp} copy --part gate --repo "{CLONE}"',
  'Expected: `COPY PASS: part gate: 10 files written and read back`.')
S('Appendix J step 7: install check, after the gate copy.', check, CLEAN)
S('Appendix J step 8: copy the rest and make the deletion.', f'{cp} copy --part rest --repo "{CLONE}"',
  'Expected: `COPY PASS: part rest: 61 files written and read back, 1 deleted`.')
S('Appendix J step 9: POST.', f'{ver} post',
  'Expected: `POST PASS: exactly the 37 expected new paths, 34 modified files and 1 deletion, all with the expected bytes.`')
S('Appendix J step 10: the suite on a barrier-free copy (`--shadow`; about 25 minutes or more).',
  f'{py} -I "{PKG}\\RUN_MHUP_A_SUITE.py" --repo "{CLONE}" --shadow',
  'Expected: the runner\'s POST and copy lines, one line per module, its checks after the suite, the removal of its temporary folder, and finally `SUITE PASS: all 571 tests ran and passed; ...` (draft count; at most the four allowed symlink skips; the runner decides). E2R-T12 runs here (owner options). Record the whole output as printed, with each module\'s time; if it prints failure detail, copy it exactly (it carries test names and messages only; section 2A, A3 says what to do with a line that appears to contain a draw\'s numbers).')
S('EXPECTED REFUSAL (section 2A, A5): remove E before the package commit.', f'{cp} barrier --remove E --repo "{CLONE}"',
  'Expected (all three, section 2A, A5): a non-zero exit code; a line that **begins with** `COPY STOP: barrier E is removed only after COMMITTED PASS (step 15), and the verifier\'s committed phase does not pass now`; no `Traceback`. Anything else: STOP. That E is still in place is checked by steps 23 and 25 (`E present`).')
S('Appendix J step 11: install check.', check, CLEAN)
S('Appendix J step 12: the install record.', f'{irx} install-record --root "{CLONE}" --package MHUP_A --manifest "{MAN}"',
  'Expected: `INSTALL RECORD PASS: ` and the record\'s path in the clone, ending `install_records\\INSTALL_MHUP_A_V1.json`.')
S('Appendix J step 12: stage the package commit** (the paths are read from the package\'s list).**',
  f'{cgit} add "--pathspec-from-file={PKG}\\STAGE_PACKAGE_COMMIT.txt"',
  'Expected: `GUARD PASS (before)`, possibly `warning: ... LF will be replaced by CRLF ...` lines (harmless; record them), then `GUARD PASS (after); git add exit code 0`.')
S('Appendix J step 12: STAGED (the verifier; before the commit).', f'{ver} staged',
  'Expected: `STAGED PASS: the index holds exactly the package commit (73 paths) and nothing else is changed. Commit now.`')
S('Appendix J step 12: the package commit (in the clone only; it never leaves the clone).',
  f'{cgit} commit -q -m "T016 rehearsal: MHUP-A package commit (Appendix J step 12)"',
  'Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git commit exit code 0`.')
S('Appendix J step 13: COMMITTED.', f'{ver} committed',
  'Expected: `COMMITTED PASS: the package commit (<7 characters>) added exactly 37 files and the install record, modified 34 and deleted 1; all Git blobs match; the install record names this package and manifest; barriers U, E and P in place.`')
S('Appendix J step 14: install check.', check, CLEAN)
S('EXPECTED REFUSAL (section 2A, A5): the release record while E and P still exist.',
  f'{irx} release-record --root "{CLONE}" --package MHUP_A --manifest "{MAN}"',
  'Expected (all three, section 2A, A5): a non-zero exit code; a line that **begins with** `RELEASE RECORD STOP: the install barrier P still exists; the release record follows COMMITTED PASS and the removal of E and P`; no `Traceback`. Anything else: STOP. That no record was written is checked by step 30 (the record is create-only: it STOPs if one exists) and step 32 (the release commit holds exactly 1 path).')
S('Appendix J step 15: remove E** (it re-runs the COMMITTED check first).**', f'{cp} barrier --remove E --repo "{CLONE}"',
  'Expected: `BARRIER PASS: E removed (src/methods/E_001/IN_DEVELOPMENT.txt)`.')
S('Appendix J step 15: remove P.', f'{cp} barrier --remove P --repo "{CLONE}"',
  'Expected: `BARRIER PASS: P removed (src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt)`.')
S('Appendix J step 16: the release record.', f'{irx} release-record --root "{CLONE}" --package MHUP_A --manifest "{MAN}"',
  'Expected: `RELEASE RECORD PASS: ` and the record\'s path in the clone, ending `install_records\\RELEASE_MHUP_A_V1.json`.')
S('Appendix J step 17: stage the release commit.', f'{cgit} add "--pathspec-from-file={PKG}\\STAGE_RELEASE_COMMIT.txt"',
  'Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git add exit code 0`.')
S('Appendix J step 17: STAGED.', f'{ver} staged',
  'Expected: `STAGED PASS: the index holds exactly the release commit (1 paths) and nothing else is changed. Commit now.`')
S('Appendix J step 17: the release commit (in the clone only).',
  f'{cgit} commit -q -m "T016 rehearsal: MHUP-A release commit (Appendix J step 17)"',
  'Expected: `GUARD PASS (before)`, then `GUARD PASS (after); git commit exit code 0`.')
S('Appendix J step 17: RELEASED.', f'{ver} released',
  'Expected: a line starting `RELEASED PASS: two commits proved: the release commit (`; record the whole output.')
S('Appendix J step 18: RELEASED again** (U is released only if this passes).**', f'{ver} released',
  'Expected: the same `RELEASED PASS: ...` line as step 34.')
S('Appendix J step 18: release U.', f'{pcx} release-install-lock --root "{CLONE}" --package MHUP_A',
  'Expected: `CLEAN; install lock released for MHUP_A`. (Appendix J step 19, the push, is not part of this task: a task clone never pushes.)')
S('F2 row 5 (N1, N4, N4b on Windows Git): the attributes and line ends of the five byte-checked items.',
  f'{cgit} ls-files --eol -- .gitattributes src/methods/_common/contract_data/install_records src/package_tools/process_check.py "src/results*_v0_2.py" "tests/fixtures/*_v0_1_reference.py.txt"',
  'Expected: 7 Git lines between the GUARD lines: `.gitattributes`; the three files under `install_records/` (the baseline record, `INSTALL_MHUP_A_V1.json`, `RELEASE_MHUP_A_V1.json`); `process_check.py`; the updater v0.2; the v0.1 reference fixture. Each line but the first must show `i/lf`, `w/lf` and `attr/-text`. Any `w/crlf` on those six, or a missing `-text`: STOP. Copy the whole output.')
S('F2 row 5: the project reader validates the records.', f'{irx} validate --root "{CLONE}"',
  'Expected: `RECORDS PASS: 1 install record(s), 2 release record(s), 80 released unretired entries`.')
S('The clone after the rehearsal: clean, with the two commits on top.', [f'{cgit} status --short', f'{cgit} log --format=%s -3'],
  'Expected: the first command prints nothing between its GUARD lines; the second prints the release commit\'s subject, the package commit\'s subject, then the subject of the commit of step 6. Copy both outputs.')
S('F2 row 10: the byte-code folder was never created.',
  f'{py} -I -c "import os; p=r\'{NOPYC}\'; print(\'NO_PYCACHE_EVER ABSENT\' if not os.path.lexists(p) else \'NO_PYCACHE_EVER PRESENT\')"',
  'Expected: `NO_PYCACHE_EVER ABSENT`.')
S('F2 row 6: the environment inventory on the real Windows interpreter** (reads the main venv and its base Python; writes nothing).**',
  f'{py} -I "{HARN}" inventory --src "{CLONE}\\src"',
  'Expected: the closure module\'s path (in the clone), the venv and base paths, the Python and platform line, one line of counts, the environment digest, then `ENV INVENTORY PASS`. `ENV INVENTORY STOP: ...` names the first orphan or mismatch: that is a STOP to report as printed (never delete or change anything in the venv).')
S('F2 row 7: a planted orphan is refused** (in a scratch copy; the real venv is only read).**',
  f'{py} -I "{HARN}" orphan --src "{CLONE}\\src" --scratch "{T}\\e"',
  'Expected: `copied <name>.dist-info: ...`, `control PASS: 1 distribution, no orphan`, `refused: 1 file(s) under site-packages that no RECORD lists, the first: T016_PLANTED_ORPHAN.txt`, then `ORPHAN CHECK PASS: the planted file was refused by name`.')

out = []
w = out.append
w('# TASK_T016 - MHUP-A install rehearsal in a task clone (Appendix J steps 0 to 18), with F2 rows 5, 6, 7 and 10')
w('')
w('**DRAFT r2 for RECHECK (11 November 2026; the reviewer\'s T016-C02, C04 and C05 applied). Not for use: not installed in the inbox, no go given.** At the package freeze: `<EX_FOLDER>` and `<ZIP_SHA256>` are replaced by the pinned ZIP and its SHA-256, the counts marked "draft count" by the frozen ones, and `<date of the go>` is filled in; then `check_task_commands.py` is rerun on the final file against the settings as they are then (the F1 deny lines come only after T016: they would deny 13 of these commands). Before T016 runs: rulebook v0.5 (section 2A) is ratified and installed, this file is committed to `inbox\\` (its commit named in the go), and the project owner gives T016 its own go.')
w('')
w('**Task ID:** T016. **Date:** <date of the go>. **Author:** the Claude web chat. Rulebook v0.5, section 2A, is the allowance this task runs under.')
w('')
w('**Purpose.** Rehearse the whole MHUP-A installation on the owner\'s Windows machine, exactly as `INSTALL_INSTRUCTIONS.md` gives it, but in a disposable task clone that cannot push: the package\'s own tools (process check, copy tool, verifier, suite runner, records tool) run from the extracted package against the clone; the two install commits are made in the clone only. Step 0 is replaced by a clean-tree and HEAD check (the clone is fresh, so there is no pull); step 19 (the push) is omitted. Three EXPECTED REFUSAL steps check on Windows that the tools refuse out-of-order actions. After the install, the task checks the line ends and attributes of the five byte-checked items on Windows Git (F2 row 5), that the byte-code folder was never made (row 10), and the environment inventory on the real interpreter, with a planted-orphan refusal in a scratch copy (rows 6 and 7).')
w('')
w('**This is not the installation.** The main repository is not changed (only this task\'s report is committed there, as always). Nothing is pushed. No program runs at the main repository\'s root: F2 rows 8 and 9 are the project owner\'s own checks, on a separate sheet. No launcher, coordinator, updater, Mode H, report tool or `.bat` runs; no process is terminated; no lottery website is contacted; nothing here has a browser. The clone holds the development masters; only the suite runner touches them, as rulebook section 2A, A3 says.')
w('')
w('## Owner options')
w('')
w('- None. E2R-T12 (one test that starts up to six ordinary Python worker processes, which finish by themselves) runs inside step 18\'s suite. The project owner approves it for this run by giving this task.')
w('')
w('## Paths')
w('')
w('| Name | Full path |')
w('|---|---|')
for n, v in (('MAIN (the main repository)', MAIN), ("PY (the main venv's Python)", PY), ('TOOLS', WF + r'\tools'),
             ('CLONE (the task clone)', CLONE), ('PKG (the extracted package)', PKG), ('MAN (its manifest)', MAN),
             ('E (the harness scratch folder of step 42)', T + r'\e')):
    w(f'| {n} | `{v}` |')
w('')
w('The commands below are written out in full. Run each from MAIN. A step passes only with its expected output and exit code 0, except the three steps marked **EXPECTED REFUSAL**, which pass only as rulebook section 2A, A5 says (a non-zero exit code, a line beginning with the refusal text given, and no traceback). On anything else: **STOP**, record the output, and go to step 43 (clean-up). Never rerun, skip or reorder a step, and never repair, inspect or recover anything in the clone. **Record as you go** (rulebook section 2A, A6): step 43 removes `scratch\\T016` before the report is written, so save each step\'s exact command, exit code and full output as soon as it ends; on a STOP, also note which step stopped and what it and the steps before it printed about the barriers U, E and P and the records. "Step N" alone means this task\'s step N; "Appendix J step N" means the step of the install instructions it rehearses.')
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
w(f'**{n + 1}. Remove the task clone, the extracted package and the harness folder** (all under `scratch\\T016`).')
w('```')
w(f'{cc} remove --task T016')
w('```')
w(f'Expected: `REMOVE PASS`. If it STOPs, leave the folder as it is, say so in the report, do not run step {n + 3}, and tell the project owner.')
w('')
w('## Report')
w('')
w(f'**{n + 2}. Write** `{WF}\\outbox\\REPORT_T016.md` in the format of `outbox\\README.md`, with every step\'s command, exit code and full output. Also record:')
w('- the wall-clock time of step 18;')
w('- for each EXPECTED REFUSAL step (10, 19 and 27), its exit code and its refusal line, in the step table\'s Result column;')
w('- on a STOP: the step that stopped, its output, and the barrier and record state the outputs up to it showed (from your notes; the clone is gone);')
w('- whether the main repository\'s `git status --short` after step 43 is the same as in step 2 (run it again and include it).')
w('')
w('## Finish')
w('')
w(f'**{n + 3}. Commit the report** (one file; not pushed).')
w('```')
w(f'{cc} commit-report --task T016')
w('```')
w('Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.')
w('')
w(f'**{n + 4}. Tell the project owner** the RESULT line, the report\'s path, and: "please push".')
text = '\r\n'.join(out) + '\r\n'
text.encode('ascii')
open(sys.argv[1], 'wb').write(text.encode('ascii'))
print(f'{len(steps)} steps written to {sys.argv[1]}')
