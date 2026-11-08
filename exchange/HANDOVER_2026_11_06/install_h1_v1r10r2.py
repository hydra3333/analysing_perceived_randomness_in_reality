#!/usr/bin/env python3
"""Install the Claude handover H-1 v1r10r2 delta and blurb into doc/HANDOVER/ and move the r1 copies to doc/HANDOVER/superseded/.
Owner-run, re-runnable (copy overwrites; a move already done is skipped). From the repository root:
    python exchange/HANDOVER_2026_11_06/install_h1_v1r10r2.py copy|move|check|verify
Claude, 8 November 2026."""
import hashlib, subprocess, sys
from pathlib import Path
SRC = 'exchange/HANDOVER_2026_11_06/'
FILES = {'doc/HANDOVER/Claude_Primary_Handover_H1_v1r10r2_delta.md': 'b68c25f779d0a3f8a8522f77bd5954d5bc0fc3ac231dd9c596deada89d69d470',
         'doc/HANDOVER/Claude_Primary_Handover_H1_v1r10r2_introductory_blurb.md': '45f8b97b6177aebc2b4c302126a6240b6c4aec9841f7cd8bfa7abcfbacd72f8c'}
MOVES = [('doc/HANDOVER/Claude_Primary_Handover_H1_v1r10r1_delta.md', 'doc/HANDOVER/superseded/Claude_Primary_Handover_H1_v1r10r1_delta.md'),
         ('doc/HANDOVER/Claude_Primary_Handover_H1_v1r10r1_introductory_blurb.md', 'doc/HANDOVER/superseded/Claude_Primary_Handover_H1_v1r10r1_introductory_blurb.md')]
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
