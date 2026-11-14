#!/usr/bin/env python3
"""Read-only checks for the RAT-31 documentation install (five new files). Claude web chat, 14 November 2026.

Run with the project venv's Python, isolated, from the repository root:
    "%CD%\\.venv\\Scripts\\python.exe" -I -B exchange\\CLAUDE_WEB_TOOLS\\doc_round_rat31\\verify_doc_round.py zip E:\\TEMP\\DOC_ROUND_RAT31.zip
    "%CD%\\.venv\\Scripts\\python.exe" -I -B exchange\\CLAUDE_WEB_TOOLS\\doc_round_rat31\\verify_doc_round.py post
    "%CD%\\.venv\\Scripts\\python.exe" -I -B exchange\\CLAUDE_WEB_TOOLS\\doc_round_rat31\\verify_doc_round.py committed
Prints one line ending PASS, or lines starting STOP. Writes nothing; Git is called with --no-optional-locks.
"""
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

EXPECTED = {   # path: SHA-256 of the LF bytes (the bytes Git stores)
    'doc/HANDOVER/Claude_Primary_Handover_H1_v2.md': '8f15109ff6e789e5760f704e8b9177ba3e745838889008151a51a40234938a30',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v2_introductory_blurb.md': 'f5a0e35df5ef9361c063cb0772827214120fdfff85cea289a4961afc4c8695b5',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v2.md': 'dee6e106957e0c4f918349510fe948e98d180c7d784159eecfae9ee166045803',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v2_introductory_blurb.md': 'e607f114d8ee00cea623180136a0980aee08c9512c00ef76b341ee407098ca11',
    'doc/RATIFICATION_REGISTER_v0_29.md': '03efd2bac52272494a177a2654f6bcc852a3337eb5f506a73a2784064042f752',
}
ROOT = Path(__file__).resolve().parents[3]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(*args):
    r = subprocess.run(['git', '--no-optional-locks', '-C', str(ROOT), *args], capture_output=True)
    if r.returncode:
        raise SystemExit(f'STOP: git {" ".join(args)} failed: {r.stderr.decode(errors="replace").strip()}')
    return r.stdout


def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else ''
    bad = []
    if phase == 'zip' and len(sys.argv) == 3:
        with zipfile.ZipFile(sys.argv[2]) as z:
            names = [i.filename for i in z.infolist() if not i.is_dir()]
            if sorted(names) != sorted(EXPECTED):
                bad.append(f'the zip holds {sorted(names)}, expected exactly the five paths')
            else:
                bad += [f'{p}: wrong bytes in the zip' for p in EXPECTED if sha(z.read(p)) != EXPECTED[p]]
        ok = 'ZIP PASS: exactly the five expected files, every one with the expected bytes'
    elif phase == 'post' and len(sys.argv) == 2:
        for p, h in EXPECTED.items():
            f = ROOT / p
            if not f.is_file():
                bad.append(f'{p}: missing')
            elif sha(f.read_bytes().replace(b'\r\n', b'\n')) != h:
                bad.append(f'{p}: wrong bytes')
        status = git('status', '--porcelain', '--untracked-files=all').decode().splitlines()
        others = [s for s in status if s[3:] not in EXPECTED]
        if others:
            bad.append(f'other changes in the tree: {others[:5]}')
        ok = 'POST PASS: the five files are in place with the expected bytes, and nothing else changed'
    elif phase == 'committed' and len(sys.argv) == 2:
        changed = git('diff-tree', '--no-commit-id', '--name-status', '-r', 'HEAD').decode().splitlines()
        if sorted(changed) != sorted(f'A\t{p}' for p in EXPECTED):
            bad.append(f'the last commit changed {changed}, expected exactly the five paths added')
        for p, h in EXPECTED.items():
            if sha(git('show', f'HEAD:{p}')) != h:
                bad.append(f'{p}: the committed bytes differ')
        ok = 'COMMITTED PASS: the last commit adds exactly the five files, with the expected bytes'
    else:
        raise SystemExit('usage: verify_doc_round.py zip ZIPFILE | post | committed')
    if bad:
        for b in bad:
            print('STOP:', b)
        return 1
    print(ok)
    return 0


if __name__ == '__main__':
    sys.exit(main())
