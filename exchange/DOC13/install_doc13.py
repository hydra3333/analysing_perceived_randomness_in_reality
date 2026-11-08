#!/usr/bin/env python3
"""DOC-13: install the ratified documents (RAT-27, 8 November 2026) into doc/ and the repository root. Owner-run; re-runnable.

Usage, from the repository root (Windows: the venv's python.exe; any Python 3.8+ works):
    python exchange/DOC13/install_doc13.py copy     # writes the 8 files, overwriting each time (LF), and checks each SHA-256
    python exchange/DOC13/install_doc13.py move     # git mv's the 34 superseded editions; already-moved ones are skipped
    python exchange/DOC13/install_doc13.py check    # before committing: every file in place with its bytes; every move done
    python exchange/DOC13/install_doc13.py verify   # after committing: HEAD's blobs, and the moved files' old paths gone
Each prints PASS or STOP with the reason, and lists what it did. Touches only the listed paths. Claude, 8 November 2026.
"""
import hashlib, subprocess, sys
from pathlib import Path

FILES = {  # target path -> SHA-256 of the LF content (the source is exchange/DOC13/files/<target path>)
    'README.md': '030de52691b04e84f8e03f3926c0cfbbf50bddc95517402ff6e9d6953d222d05',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r10_delta.md': '35a5c70a4c02793caae27e21bfbdc53baf5777b16b89efa34c4458cc4fb49fe2',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r10_introductory_blurb.md': 'f30dd7792215107d4e2c310a4e11c1ec1051e0b56d353a6909e4ad1e6034ad37',
    'doc/METHOD_TEMPLATE/CHANGES.md': '25d5a3638f9eae62b5a2b27821ed4d90bf6059f3b579b4577ab864229fe0de73',
    'doc/METHOD_TEMPLATE/METHOD_SPECIFICATION_TEMPLATE.md': '54d15e8f1fe42bdc51b87a57cfc1869bb3693465d5a88ec84cc3e543ddc33661',
    'doc/METHOD_TEMPLATE/README.md': '9adfd6f17ac22675cb562c8b970650292b7009af25e0b2bdfb951b6018595841',
    'doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r6.md': '7332dd6c1b3f6d9ef858b1881333ded56782bc595b7f894f04a75255909beb9d',
    'doc/RATIFICATION_REGISTER_v0_26.md': '366e966d6584d86681891eb84fe5363ae94ecac00f2943daab8fbc01ca125414',
}
MOVES_LIST = 'exchange/DOC13/MOVES.txt'
EXPECTED_MOVES = 34


def stop(msg):
    print('STOP:', msg)
    sys.exit(1)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(*args, check=True):
    r = subprocess.run(['git', *args], capture_output=True)
    if check and r.returncode != 0:
        stop('git ' + ' '.join(args) + ' failed: ' + r.stderr.decode(errors='replace')[:300])
    return r


def tracked(path):
    return git('ls-files', '--error-unmatch', '--', path, check=False).returncode == 0


def moves(root):
    out = []
    for line in (root / MOVES_LIST).read_text(encoding='ascii').splitlines():
        if line.startswith('#') or ' -> ' not in line:
            continue
        a, b = (x.strip() for x in line.split(' -> '))
        out.append((a, b))
    if len(out) != EXPECTED_MOVES:
        stop(f'{MOVES_LIST} lists {len(out)} moves, expected {EXPECTED_MOVES}')
    return out


root = Path.cwd()
if not (root / '.git').exists() or not (root / 'exchange' / 'DOC13').is_dir():
    stop('run this from the repository root')
mode = sys.argv[1] if len(sys.argv) > 1 else ''

if mode == 'copy':
    for target, want in FILES.items():
        data = (root / 'exchange' / 'DOC13' / 'files' / target).read_bytes().replace(b'\r\n', b'\n')
        if sha(data) != want:
            stop(f'the package copy of {target} is not the expected file')
        dest = root / target
        before = dest.read_bytes().replace(b'\r\n', b'\n') if dest.exists() else None
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        if sha(dest.read_bytes()) != want:
            stop(f'{target} did not write correctly')
        print(('unchanged ' if before == data else 'written   ') + target)
    print('DOC13 COPY PASS')

elif mode == 'move':
    done = skipped = 0
    for a, b in moves(root):
        if tracked(a) and not (root / b).exists():
            (root / b).parent.mkdir(parents=True, exist_ok=True)
            git('mv', '--', a, b)
            print('moved     ', a, '->', b)
            done += 1
        elif not (root / a).exists() and (root / b).exists():
            print('already   ', b)
            skipped += 1
        else:
            stop(f'cannot move {a} -> {b}: the source or the destination is not as expected')
    print(f'DOC13 MOVE PASS ({done} moved, {skipped} already moved)')

elif mode == 'check':
    for target, want in FILES.items():
        p = root / target
        if not p.is_file() or sha(p.read_bytes().replace(b'\r\n', b'\n')) != want:
            stop(f'{target} is missing or not the expected content; run copy')
        print('ok        ', target)
    for a, b in moves(root):
        if (root / a).exists() or not (root / b).is_file():
            stop(f'{a} is not moved to {b}; run move')
    print(f'ok         {EXPECTED_MOVES} moves')
    print('DOC13 CHECK PASS')

elif mode == 'verify':
    for target, want in FILES.items():
        r = git('show', 'HEAD:' + target, check=False)
        if r.returncode != 0 or sha(r.stdout) != want:
            stop(f'HEAD:{target} is missing or not the expected content')
        print('ok        ', target)
    for a, b in moves(root):
        if git('cat-file', '-e', 'HEAD:' + a, check=False).returncode == 0:
            stop(f'HEAD still has {a}')
        if git('cat-file', '-e', 'HEAD:' + b, check=False).returncode != 0:
            stop(f'HEAD lacks {b}')
    print(f'ok         {EXPECTED_MOVES} moves in HEAD')
    print('DOC13 VERIFY PASS')

else:
    stop('say copy, move, check or verify')
