#!/usr/bin/env python3
"""DOC-12: install the ratified H-2 v1r9 and register v0.25 into doc/ (owner-run; document-only route). Claude, 6 November 2026.

Usage, from the repository root (Windows: the venv's python.exe):
    python exchange/DOC12/install_doc12.py copy      # writes the three files into doc/ (LF), checks their SHA-256
    (then the owner's git commands in exchange/DOC12/README.md)
    python exchange/DOC12/install_doc12.py verify    # after the commit: checks HEAD's blobs and that the old copies are gone
Prints DOC12 COPY PASS / DOC12 VERIFY PASS, or STOP with the reason. Touches nothing outside doc/.
"""
import hashlib, subprocess, sys
from pathlib import Path

FILES = {  # target path -> SHA-256 of the LF content
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r9.md': '99a84910b3333345e1ec5c9497fb77506d9f936e301f3a732897651c130fde69',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r9_introductory_blurb.md': '2d9744fe47c2e783ac4b7e0f75a81a73874324dea1374423ce1ff8c90f45d664',
    'doc/RATIFICATION_REGISTER_v0_25.md': '2ef9d17cfbc76c556e00d659677e411686c60aab263e1b0f0ef002930ee6d874',
}
GONE = ['doc/RATIFICATION_REGISTER_v0_25_CANDIDATE.md', 'doc/HANDOVER/HANDOVER_2026_11_06']

def stop(msg):
    print('STOP:', msg); sys.exit(1)

def sha(b):
    return hashlib.sha256(b).hexdigest()

root = Path.cwd()
if not (root / '.git').exists() or not (root / 'exchange' / 'DOC12').is_dir():
    stop('run this from the repository root')
mode = sys.argv[1] if len(sys.argv) > 1 else ''
if mode == 'copy':
    for target, want in FILES.items():
        src = root / 'exchange' / 'DOC12' / target
        data = src.read_bytes().replace(b'\r\n', b'\n')
        if sha(data) != want:
            stop(f'{src} is not the expected file ({sha(data)})')
        (root / target).parent.mkdir(parents=True, exist_ok=True)
        (root / target).write_bytes(data)
        if sha((root / target).read_bytes()) != want:
            stop(f'{target} did not write correctly')
        print('copied', target)
    print('DOC12 COPY PASS')
elif mode == 'verify':
    for target, want in FILES.items():
        r = subprocess.run(['git', 'show', 'HEAD:' + target], capture_output=True)
        if r.returncode != 0 or sha(r.stdout) != want:
            stop(f'HEAD:{target} missing or not the expected content')
        print('ok', target)
    for p in GONE:
        r = subprocess.run(['git', 'ls-tree', '-r', '--name-only', 'HEAD', '--', p], capture_output=True, text=True)
        if r.stdout.strip():
            stop(f'{p} is still in HEAD')
        print('gone', p)
    print('DOC12 VERIFY PASS')
else:
    stop('say copy or verify')
