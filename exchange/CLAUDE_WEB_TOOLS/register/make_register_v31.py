#!/usr/bin/env python3
"""Make register v0.31 from the installed register v0.30 by two counted insertions (Claude, 17 November 2026): the version
line, and the new section (register_v31_section.md) before "## Interpretation and verification". Nothing of v0.30 is
changed or removed. The section's @H1V4@ and @H1V4B@ placeholders are filled with the SHA-256 of H-1 v4 and its blurb.
Usage: python3 -I make_register_v31.py V0_30_FILE SECTION_FILE H1V4_FILE H1V4_BLURB_FILE OUT_FILE
Refuses any other argument count, and an OUT_FILE that is one of its inputs."""
import hashlib, os, sys

SRC_SHA = '2a6fe7b6758d882b46a6829cff6c73ddefa5381f9fe3851b72720ab40ccdd56c'      # v0.30 as installed at 5b4df41
assert len(sys.argv) == 6, 'expected exactly 5 arguments (see the usage line)'
src, sec, h1, h1b, out = sys.argv[1:6]
assert not any(os.path.exists(p) and os.path.exists(out) and os.path.samefile(out, p) for p in (src, sec, h1, h1b)), 'OUT_FILE is an input'
s = open(src, 'rb').read()
assert hashlib.sha256(s).hexdigest() == SRC_SHA, 'v0.30 is not the installed bytes'
s = s.decode('utf-8')
section = open(sec, 'rb').read().decode('ascii')
assert '\r' not in section and all(section.count(k) == 1 for k in ('@H1V4@', '@H1V4B@'))
section = (section.replace('@H1V4@', hashlib.sha256(open(h1, 'rb').read()).hexdigest())
                  .replace('@H1V4B@', hashlib.sha256(open(h1b, 'rb').read()).hexdigest()))
EDITS = [
    ('version', '**Register version:** v0.30, 15 November 2026, OWNER-RATIFIED',
     '**Register version:** v0.31, 17 November 2026, CANDIDATE for the owner\'s ratification (RAT-34, with H-1 v4; written by '
     'Claude from the records; for review in EX_214), recording the RAT-32 install (`5b4df41`), Mode H run and sealed in both '
     'games, the two readings and the record of the study, D5 (`c7622fa`), the closing of the holdout exposure record, the '
     'approach the owner agreed on 16 November 2026, RAT-33 (the MHUP-B design supplement) and EX_193 to EX_213; '
     'v0.30, 15 November 2026, OWNER-RATIFIED'),
    ('section', '\n## Interpretation and verification\n', '\n' + section + '## Interpretation and verification\n'),
]
for label, old, new in EDITS:
    n = s.count(old)
    assert n == 1, f'{label}: expected one occurrence, found {n}'
    s = s.replace(old, new)
open(out, 'wb').write(s.encode('utf-8'))
print(f'{len(EDITS)} counted insertions; SHA-256 {hashlib.sha256(s.encode("utf-8")).hexdigest()}')
