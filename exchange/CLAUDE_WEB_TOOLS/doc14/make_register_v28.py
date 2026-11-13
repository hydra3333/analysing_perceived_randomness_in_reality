#!/usr/bin/env python3
"""Make register v0.28 from the installed register v0.27 by two counted insertions (Claude, 13 November 2026): the version
line, and the correction section (register_v28_section.md) before "## Interpretation and verification". Nothing of v0.27 is
changed or removed. Usage: python3 -I make_register_v28.py V0_27_FILE SECTION_FILE OUT_FILE"""
import hashlib, sys

SRC_SHA = 'fee014c148c2cca10f12e4418d17a04b20d932645f3c0162b1f32e43285d70aa'      # v0.27 as installed at b8600d0
src, sec, out = sys.argv[1:4]
s = open(src, 'rb').read()
assert hashlib.sha256(s).hexdigest() == SRC_SHA, 'v0.27 is not the installed bytes'
s = s.decode('utf-8')
section = open(sec, 'rb').read().decode('ascii')
assert '\r' not in section
EDITS = [
    ('version', '**Register version:** v0.27, 13 November 2026, OWNER-APPROVED',
     '**Register version:** v0.28, 13 November 2026, FOR THE OWNER\'S APPROVAL (written by Claude; a correction, not a new '
     'decision): register v0.27\'s "RAT-28" for the ratification of 11 November 2026 is read as RAT-30, and the ratifications '
     'RAT-28 (H-1 v1r10r2, 8 November 2026) and RAT-29 (H-1 v1r10r3, 10 November 2026) are recorded; v0.27, 13 November 2026, '
     'OWNER-APPROVED'),
    ('section', '\n## Interpretation and verification\n', '\n' + section + '## Interpretation and verification\n'),
]
for label, old, new in EDITS:
    n = s.count(old)
    assert n == 1, f'{label}: expected one occurrence, found {n}'
    s = s.replace(old, new)
open(out, 'wb').write(s.encode('utf-8'))
print(f'{len(EDITS)} counted insertions; SHA-256 {hashlib.sha256(s.encode("utf-8")).hexdigest()}')
