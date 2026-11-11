#!/usr/bin/env python3
"""Dry run, on Linux, of the DRAFT TASK_T016 sequence (Claude web chat, 11 November 2026; a working tool, not for the runner).

  t016_dryrun.py REPO PKG WORK PYTHON lf|crlf [--no-suite] [--harness-python=P]
  (--harness-python: a venv made by `python -m venv` for rows 6 and 7; the uv-made test venvs carry uv's own
  _virtualenv.pth and _virtualenv.py, which no RECORD lists, and are refused by the inventory, as they should be)

Clones REPO (its HEAD) into WORK/CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T016/r, copies PKG to .../T016/p/<name>, and
runs T016 part B and part C in order, with the tools, options and expected texts the task file gives (the three
expected refusals included), then the rows 6 and 7 harness. Any other result ends the run with DRY RUN STOP: nothing
after it is run. Nothing is pushed; WORK is the only place written.
"""
import shutil, subprocess, sys
from pathlib import Path

GITID = ['-c', 'user.name=Claude Code task clone', '-c', 'user.email=task-clone@invalid']


def sh(cmd):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return r.returncode, r.stdout


def main():
    repo_src, pkg_src, work, py, mode = sys.argv[1:6]
    suite = '--no-suite' not in sys.argv
    hpy = next((x.split('=', 1)[1] for x in sys.argv if x.startswith('--harness-python=')), py)
    work = Path(work)
    shutil.rmtree(work, ignore_errors=True)
    t = work / 'CLAUDE_CODE_WORKING_FOLDER_TREE' / 'scratch' / 'T016'
    r, pkg = t / 'r', t / 'p' / Path(pkg_src).name
    t.mkdir(parents=True)
    extra = ['-c', 'core.autocrlf=true'] if mode == 'crlf' else []
    rc, out = sh(['git', *extra, 'clone', '-q', repo_src, str(r)])
    assert rc == 0, out
    if mode == 'crlf':
        sh(['git', '-C', str(r), 'config', 'core.autocrlf', 'true'])
    shutil.copytree(pkg_src, pkg)
    R, man = str(r), str(pkg / 'PACKAGE_MANIFEST_MHUP_A.json')
    P = [py, '-I', '-B']
    PX = P + ['-X', f'pycache_prefix={r}/transitory_data/no_pycache_ever']
    PC = PX + [str(pkg / 'repo_overlay/src/package_tools/process_check.py')]
    IR = PX + [str(pkg / 'repo_overlay/src/package_tools/install_records.py')]
    VER = P + [str(pkg / 'VERIFY_MHUP_A.py'), '--repo', R, '--phase']
    CP = P + [str(pkg / 'MHUPA_COPY.py')]
    G = ['git', '-C', R, *GITID]
    check = PC + ['check-no-runs', '--root', R, '--install', man]
    harness = r / 'exchange/CLAUDE_WEB_TOOLS/mhupa/t016/T016_ENV_HARNESS.py'
    if not harness.is_file():                     # before the drafts are committed: the copy beside this tool
        harness = Path(__file__).resolve().parent / 'T016_ENV_HARNESS.py'
        print(f'(the harness is not in the clone yet; using {harness})')
    H = [hpy, '-I', str(harness)]
    # (label, command, expected exit: 0 or 'nonzero', text the output must contain)
    steps = [
        ('B0a status', G + ['status', '--short'], 0, ''),
        ('B0b HEAD', G + ['rev-parse', 'HEAD'], 0, ''),
        ('B1 PRE', VER + ['pre'], 0, 'PRE PASS'),
        ('B2 install check', check, 0, 'CLEAN'),
        ('B3 take U', PC + ['take-install-lock', '--root', R, '--package', 'MHUP_A'], 0, 'CLEAN; install lock taken'),
        ('B3x EXPECTED REFUSAL: take U again', PC + ['take-install-lock', '--root', R, '--package', 'MHUP_A'], 'nonzero', 'REFUSED: the updater lock already names an install (INSTALL MHUP_A '),
        ('B4a create E', CP + ['barrier', '--create', 'E', '--repo', R], 0, 'BARRIER PASS: E created'),
        ('B4b create P', CP + ['barrier', '--create', 'P', '--repo', R], 0, 'BARRIER PASS: P created'),
        ('B5 install check', check, 0, 'CLEAN'),
        ('B6 copy gate', CP + ['copy', '--part', 'gate', '--repo', R], 0, 'COPY PASS: part gate: 10 files'),
        ('B7 install check', check, 0, 'CLEAN'),
        ('B8 copy rest', CP + ['copy', '--part', 'rest', '--repo', R], 0, 'COPY PASS: part rest: 61 files'),
        ('B9 POST', VER + ['post'], 0, 'POST PASS'),
    ]
    if suite:
        steps.append(('B10 suite --shadow', [py, '-I', str(pkg / 'RUN_MHUP_A_SUITE.py'), '--repo', R, '--shadow'], 0, 'SUITE PASS'))
    steps += [
        ('B10x EXPECTED REFUSAL: remove E before the package commit', CP + ['barrier', '--remove', 'E', '--repo', R], 'nonzero', "COPY STOP: barrier E is removed only after COMMITTED PASS (step 15), and the verifier's committed phase does not pass now"),
        ('B11 install check', check, 0, 'CLEAN'),
        ('B12a install record', IR + ['install-record', '--root', R, '--package', 'MHUP_A', '--manifest', man], 0, 'INSTALL RECORD PASS'),
        ('B12b stage', G + ['add', f'--pathspec-from-file={pkg / "STAGE_PACKAGE_COMMIT.txt"}'], 0, ''),
        ('B12c STAGED', VER + ['staged'], 0, 'STAGED PASS'),
        ('B12d commit', G + ['commit', '-q', '-m', 'T016 rehearsal: MHUP-A package commit (Appendix J step 12)'], 0, ''),
        ('B13 COMMITTED', VER + ['committed'], 0, 'COMMITTED PASS'),
        ('B14 install check', check, 0, 'CLEAN'),
        ('B14x EXPECTED REFUSAL: release record before step 15', IR + ['release-record', '--root', R, '--package', 'MHUP_A', '--manifest', man], 'nonzero', 'RELEASE RECORD STOP: the install barrier P still exists; the release record follows COMMITTED PASS and the removal of E and P'),
        ('B15a remove E', CP + ['barrier', '--remove', 'E', '--repo', R], 0, 'BARRIER PASS: E removed'),
        ('B15b remove P', CP + ['barrier', '--remove', 'P', '--repo', R], 0, 'BARRIER PASS: P removed'),
        ('B16 release record', IR + ['release-record', '--root', R, '--package', 'MHUP_A', '--manifest', man], 0, 'RELEASE RECORD PASS'),
        ('B17a stage', G + ['add', f'--pathspec-from-file={pkg / "STAGE_RELEASE_COMMIT.txt"}'], 0, ''),
        ('B17b STAGED', VER + ['staged'], 0, 'STAGED PASS'),
        ('B17c commit', G + ['commit', '-q', '-m', 'T016 rehearsal: MHUP-A release commit (Appendix J step 17)'], 0, ''),
        ('B17d RELEASED', VER + ['released'], 0, 'RELEASED PASS'),
        ('B18a RELEASED again', VER + ['released'], 0, 'RELEASED PASS'),
        ('B18b release U', PC + ['release-install-lock', '--root', R, '--package', 'MHUP_A'], 0, 'CLEAN; install lock released'),
        ('C1 N1 attributes and line ends', G + ['ls-files', '--eol', '--', '.gitattributes', 'src/methods/_common/contract_data/install_records',
                                                 'src/package_tools/process_check.py', 'src/results*_v0_2.py', 'tests/fixtures/*_v0_1_reference.py.txt'], 0, ''),
        ('C2 records validate', IR + ['validate', '--root', R], 0, 'RECORDS PASS'),
        ('C3a status', G + ['status', '--short'], 0, ''),
        ('C3b log', G + ['log', '--format=%s', '-3'], 0, 'release commit'),
        ('C4 byte-code folder', [py, '-I', '-c', f"import os; p=r'{r}/transitory_data/no_pycache_ever'; print('NO_PYCACHE_EVER ABSENT' if not os.path.lexists(p) else 'NO_PYCACHE_EVER PRESENT')"], 0, 'ABSENT'),
        ('D1 row 6 inventory', H + ['inventory', '--src', str(r / 'src')], 0, 'ENV INVENTORY PASS'),
        ('D2 row 7 orphan', H + ['orphan', '--src', str(r / 'src'), '--scratch', str(t / 'e')], 0, 'ORPHAN CHECK PASS'),
    ]
    print(f'T016 DRY RUN (DRAFT package; Linux; {mode}; {py}); step 10 ' + ('INCLUDED' if suite else 'OMITTED'), flush=True)
    for label, cmd, want_rc, want in steps:
        rc, out = sh(cmd)
        keep = [ln for ln in out.splitlines() if not ln.startswith('warning: in the working copy')]
        print(f'--- {label} (exit {rc})\n' + '\n'.join('    ' + ln[:240] for ln in keep[-40:]), flush=True)
        if want_rc == 0:
            ok = rc == 0 and want in out
        else:                                        # rulebook v0.5 section 2A, A5: anchored text, no traceback
            ok = rc != 0 and any(ln.startswith(want) for ln in out.splitlines()) and 'Traceback' not in out
        if label == 'B0a status' and out.strip():
            ok = False
        if label == 'C3a status' and out.strip():
            ok = False
        if not ok:
            print(f'DRY RUN STOP at {label}')
            return 1
    print('DRY RUN PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
