#!/usr/bin/env python3
"""Make register v0.30 from the installed register v0.29 by two counted insertions (Claude, 15 November 2026): the version
line, and the new section (register_v30_section.md) before "## Interpretation and verification". Nothing of v0.29 is
changed or removed. The section's @H1V3@ and @H1V3B@ placeholders are filled with the SHA-256 of H-1 v3 and its blurb.
Usage: python3 -I make_register_v30.py V0_29_FILE SECTION_FILE H1V3_FILE H1V3_BLURB_FILE OUT_FILE
Refuses any other argument count, and an OUT_FILE that is one of its inputs."""
import hashlib, os, sys

SRC_SHA = '03efd2bac52272494a177a2654f6bcc852a3337eb5f506a73a2784064042f752'      # v0.29 as installed at 5a8527b
assert len(sys.argv) == 6, 'expected exactly 5 arguments (see the usage line)'
src, sec, h1, h1b, out = sys.argv[1:6]
assert not any(os.path.exists(p) and os.path.exists(out) and os.path.samefile(out, p) for p in (src, sec, h1, h1b)), 'OUT_FILE is an input'
s = open(src, 'rb').read()
assert hashlib.sha256(s).hexdigest() == SRC_SHA, 'v0.29 is not the installed bytes'
s = s.decode('utf-8')
section = open(sec, 'rb').read().decode('ascii')
assert '\r' not in section and all(section.count(k) == 1 for k in ('@H1V3@', '@H1V3B@'))
section = (section.replace('@H1V3@', hashlib.sha256(open(h1, 'rb').read()).hexdigest())
                  .replace('@H1V3B@', hashlib.sha256(open(h1b, 'rb').read()).hexdigest()))
EDITS = [
    ('version', '**Register version:** v0.29, 14 November 2026, OWNER-RATIFIED',
     '**Register version:** v0.30, 15 November 2026, OWNER-RATIFIED 15 November 2026, about 09:10 (RAT-32, with H-1 v3; '
     'written by Claude from the records; reviewed in EX_190 to EX_192), recording the documentation install of RAT-31 '
     '(`5a8527b`), the owner\'s dependency change (`cc0ab73`) and TASK_T024, EX_176 to EX_190, the replacement reviewer chat, the '
     'owner\'s decisions of 14 November 2026 (C02, D1-D7, the working approach P0-P6, OUTLANDISH_01\'s methods, B01 as a scoped '
     'W-23 acceptance) and the POC rerun and updater self-test (both PASS); v0.29, 14 November 2026, OWNER-RATIFIED'),
    ('section', '\n## Interpretation and verification\n', '\n' + section + '## Interpretation and verification\n'),
]
for label, old, new in EDITS:
    n = s.count(old)
    assert n == 1, f'{label}: expected one occurrence, found {n}'
    s = s.replace(old, new)
open(out, 'wb').write(s.encode('utf-8'))
print(f'{len(EDITS)} counted insertions; SHA-256 {hashlib.sha256(s.encode("utf-8")).hexdigest()}')
