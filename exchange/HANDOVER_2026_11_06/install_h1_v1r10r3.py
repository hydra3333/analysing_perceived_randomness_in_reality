#!/usr/bin/env python3
"""Install the Claude handover H-1 v1r10r3 delta and blurb into doc/HANDOVER/ and move the r1 copies to doc/HANDOVER/superseded/.
Owner-run, re-runnable (copy overwrites; a move already done is skipped). From the repository root:
    python exchange/HANDOVER_2026_11_06/install_h1_v1r10r3.py copy|move|check|verify
Claude, 10 November 2026 (from the r2 installer)."""
import hashlib, subprocess, sys
from pathlib import Path
SRC = 'exchange/HANDOVER_2026_11_06/'
FILES = {'doc/HANDOVER/Claude_Primary_Handover_H1_v1r10r3_delta.md': '40429eb5cb5b55d137dfb51e364aff52b37765f9e623cd9d2644a236d350fd01',
         'doc/HANDOVER/Claude_Primary_Handover_H1_v1r10r3_introductory_blurb.md': 'dcc67bf84c27ff830a5d286f446e244b93bbadd3e3ef95f88fb9d3b7e8e2801e'}
MOVES = [('doc/HANDOVER/Claude_Primary_Handover_H1_v1r10r2_delta.md', 'doc/HANDOVER/superseded/Claude_Primary_Handover_H1_v1r10r2_delta.md'),
         ('doc/HANDOVER/Claude_Primary_Handover_H1_v1r10r2_introductory_blurb.md', 'doc/HANDOVER/superseded/Claude_Primary_Handover_H1_v1r10r2_introductory_blurb.md')]
def stop(m): print('STOP:', m); sys.exit(1)
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*a): return subprocess.run(['git', *a], capture_output=True)
root = Path.cwd()
if not (root / '.git').exists() or not (root / SRC).is_dir(): stop('run this from the repository root')
mode = sys.argv[1] if len(sys.argv) > 1 else ''
if mode == 'copy':
    for t, want in FILES.items():
        data = (root / SRC / Path(t).name).read_bytes().replace(b'\r\n', b'\n')
        if sha(data) != want: stop(f'the source of {t} is not the expected file')
        (root / t).write_bytes(data); print('written   ', t)
    print('H1 COPY PASS')
elif mode == 'move':
    for a, b in MOVES:
        if (root / a).exists() and not (root / b).exists():
            if git('mv', '--', a, b).returncode: stop(f'git mv {a} failed')
            print('moved     ', a)
        elif not (root / a).exists() and (root / b).exists(): print('already   ', b)
        else: stop(f'cannot move {a}')
    print('H1 MOVE PASS')
elif mode in ('check', 'verify'):
    for t, want in FILES.items():
        b = (root / t).read_bytes().replace(b'\r\n', b'\n') if mode == 'check' and (root / t).exists() else (git('show', 'HEAD:' + t).stdout if mode == 'verify' else b'')
        if sha(b) != want: stop(f'{t} missing or not the expected content')
        print('ok        ', t)
    for a, b in MOVES:
        if mode == 'check' and ((root / a).exists() or not (root / b).exists()): stop(f'{a} not moved')
        if mode == 'verify' and (git('cat-file', '-e', 'HEAD:' + a).returncode == 0 or git('cat-file', '-e', 'HEAD:' + b).returncode != 0): stop(f'{a} not moved in HEAD')
    print('H1 ' + mode.upper() + ' PASS')
else: stop('say copy, move, check or verify')
