#!/usr/bin/env python3
"""DOC-14: make register v0.27 from the installed register v0.26 by counted insertions (Claude, 13 November 2026).

register v0.27 = v0.26 with only: (a) the new version line in front of v0.26's; (b) the section register_v27_section.md
before "## Interpretation and verification", with design v0.1r7's SHA-256 filled in; (c) a "Current status (register v0.27)"
bullet at the head of that section's list. Nothing of v0.26 is changed or removed.
Usage: python3 -I make_register_v27.py V0_26_FILE SECTION_FILE DESIGN_V0_1R7_FILE OUT_FILE
"""
import hashlib, sys

SRC_SHA = '366e966d6584d86681891eb84fe5363ae94ecac00f2943daab8fbc01ca125414'      # v0.26 as installed (RAT-27)
src, sec, design, out = sys.argv[1:5]
s = open(src, 'rb').read()
assert hashlib.sha256(s).hexdigest() == SRC_SHA, 'v0.26 is not the ratified bytes'
assert b'\r' not in s
s = s.decode('utf-8')
section = open(sec, 'rb').read().decode('ascii')
assert '\r' not in section
dsha = hashlib.sha256(open(design, 'rb').read()).hexdigest()
assert section.count('@@DESIGN_SHA@@') == 1
section = section.replace('@@DESIGN_SHA@@', dsha)

EDITS = [
    ('version', '**Register version:** v0.26 OWNER-RATIFIED 8 November 2026',
     '**Register version:** v0.27, 13 November 2026, FOR THE OWNER\'S APPROVAL as DOC-14 (written by Claude from the records; '
     'documentation of decisions already ratified, not a new ratification), recording the integrated MHUP-A package from its '
     'start to its install and closure on 13 November 2026, rulebook v0.5 and the Appendix J amendments (RAT-28), design '
     'v0.1r7, the post-install test fix and the owner\'s decisions of 13 November 2026; v0.26 OWNER-RATIFIED 8 November 2026'),
    ('section', '\n## Interpretation and verification\n', '\n' + section + '## Interpretation and verification\n'),
    ('status', '\n- **Current status (register v0.26; read this first).**\n',
     '\n- **Current status (register v0.27; read this first).**\n'
     '  - MHUP-A is installed and released (13 November 2026; commits `2860e86` and `effc179`), and its post-install test fix is\n'
     '    committed (`87c4219`); the suite on `main` passes 571/571. E_1 revision 3 is released for both games, dated 2026-11-13.\n'
     '  - No real-data science run, results update, report, holdout opening or Mode H took place. None of the owner\'s Approvals 1\n'
     '    to 4 has been given.\n'
     '  - Next: the MHUP-B assessment for the owner (decision 3 of 13 November 2026).\n'
     '- **Current status (register v0.26; read this first).**\n'),
]
for label, old, new in EDITS:
    n = s.count(old)
    assert n == 1, f'{label}: expected one occurrence, found {n}'
    s = s.replace(old, new)
open(out, 'wb').write(s.encode('utf-8'))
print(f'{len(EDITS)} counted insertions; design v0.1r7 SHA-256 {dsha}; SHA-256 {hashlib.sha256(s.encode("utf-8")).hexdigest()}')
