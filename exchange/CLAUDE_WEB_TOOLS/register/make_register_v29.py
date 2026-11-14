#!/usr/bin/env python3
"""Make register v0.29 from the installed register v0.28 by two counted insertions (Claude, 14 November 2026): the version
line, and the new section (register_v29_section.md) before "## Interpretation and verification". Nothing of v0.28 is
changed or removed. The section's @H1V2@ and @H1V2B@ placeholders are filled with the SHA-256 of H-1 v2 and its blurb.
Usage: python3 -I make_register_v29.py V0_28_FILE SECTION_FILE H1V2_FILE H1V2_BLURB_FILE H2V2_FILE H2V2_BLURB_FILE OUT_FILE
(the H-2 v2 placeholders @H2V2@ and @H2V2B@ are filled the same way). Refuses any other argument count, and an OUT_FILE
that is one of its inputs."""
import hashlib, sys

SRC_SHA = '79ff491ffebae33715f1d434104324ff8301e6adf78177080c784e5f18a38e62'      # v0.28 as installed at cce4858
assert len(sys.argv) == 8, 'expected exactly 7 arguments (see the usage line)'
src, sec, h1, h1b, h2, h2b, out = sys.argv[1:8]
import os
assert not any(os.path.exists(p) and os.path.samefile(out, p) for p in (src, sec, h1, h1b, h2, h2b)), 'OUT_FILE is an input'
s = open(src, 'rb').read()
assert hashlib.sha256(s).hexdigest() == SRC_SHA, 'v0.28 is not the installed bytes'
s = s.decode('utf-8')
section = open(sec, 'rb').read().decode('ascii')
assert '\r' not in section and all(section.count(k) == 1 for k in ('@H1V2@', '@H1V2B@', '@H2V2@', '@H2V2B@'))
section = (section.replace('@H1V2@', hashlib.sha256(open(h1, 'rb').read()).hexdigest())
                  .replace('@H1V2B@', hashlib.sha256(open(h1b, 'rb').read()).hexdigest())
                  .replace('@H2V2@', hashlib.sha256(open(h2, 'rb').read()).hexdigest())
                  .replace('@H2V2B@', hashlib.sha256(open(h2b, 'rb').read()).hexdigest()))
EDITS = [
    ('version', '**Register version:** v0.28, 13 November 2026, OWNER-APPROVED',
     '**Register version:** v0.29, 14 November 2026, CANDIDATE (written by Claude from the records; documentation of decisions '
     'already taken, not a new ratification), recording the owner\'s decisions of 13 November 2026 (Mode H first, then MHUP-B; '
     'the fixed cohort; CATCH_UP; the freeze; Q7 decided; R-015 (b) and (c)), the Mode H readiness reviews (EX_167, EX_168 '
     'PASS; nothing authorised), the reviewer\'s full handover H-2 v2 (EX_169 to EX_172) and the full Claude handover '
     'H-1 v2 (EX_171, EX_172); v0.28, 13 November 2026, OWNER-APPROVED'),
    ('section', '\n## Interpretation and verification\n', '\n' + section + '## Interpretation and verification\n'),
]
for label, old, new in EDITS:
    n = s.count(old)
    assert n == 1, f'{label}: expected one occurrence, found {n}'
    s = s.replace(old, new)
open(out, 'wb').write(s.encode('utf-8'))
print(f'{len(EDITS)} counted insertions; SHA-256 {hashlib.sha256(s.encode("utf-8")).hexdigest()}')
