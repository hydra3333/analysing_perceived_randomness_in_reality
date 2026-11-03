"""Register v0.24 from the installed register v0.23 by counted in-place edits (Claude, 3 Nov 2026).

Records: the DOC-10 installation and the owner's settings deny line; the chat switch (HO-1) and the previous chat's
retirement; the stock-take of 2 November 2026 (ST-1 to ST-5) with its correction note; the direction document
(DIR-1); the owner's process decisions MC-1 and KISS-1; the MHUP-1 design reviews (EX_123 to EX_132), the owner's
decisions during them (MHUP-Q10, -Q1, -B02, -C03, -B04, -Q11, -D1, -D2, -D3) and the ratification of design v0.1r5
(MHUP-R); the rules the ratification amends; Q7 open; the future actions with when each falls due; six review
copies; the out-of-date statements; and the document table, which identifies the DOC-10 files by hash.
Every old string must occur exactly once; inserted text is ASCII. Input: the Git blob of
doc/RATIFICATION_REGISTER_v0_23.md (7502b755...c6bb). The new section's text is the file reg24_section.md beside this
builder. STATUS selects the version line: CANDIDATE (for the reviewer's content check) or RATIFIED.
Usage: python3 -I make_register_v24.py REGISTER_v0_23 SECTION_MD OUT_v0_24 CANDIDATE|RATIFIED [H1_SHA H1B_SHA]
"""
import hashlib, sys

src, sec, out, status = sys.argv[1:5]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '7502b75556c56f4c9b91e9022829ee18f05d02591260e87bfe053ec1c79bb6c2'
t = raw.decode('utf-8')
assert '\r' not in t
NEW_SECTION = open(sec, 'rb').read().decode('ascii')
assert '\r' not in NEW_SECTION and NEW_SECTION.endswith('\n\n')

if status == 'CANDIDATE':
    h1 = 'CANDIDATE for the owner\'s ratification with this register; installed with DOC-11, identified at installation'
    ver = ('**Register version:** v0.24 CANDIDATE 3 November 2026 for the ChatGPT reviewer chat\'s content check and '
           'the owner\'s ratification (not yet ratified)')
elif status == 'RATIFIED':
    h1s, h1b = sys.argv[5:7]
    h1 = f'OWNER-RATIFIED with this register; installed with DOC-11; `{h1s}`; blurb `{h1b}`'
    ver = '**Register version:** v0.24 OWNER-RATIFIED @@DATE@@ (content reviewed in @@EX@@)'
else:
    raise SystemExit('STATUS must be CANDIDATE or RATIFIED')
NEW_SECTION = NEW_SECTION.replace('@@H1STATUS@@', h1)
assert '@@' not in NEW_SECTION

EDITS = [
    ('**Register version:** v0.23 OWNER-RATIFIED 1 November 2026 (content reviewed in EX_117, EX_119 and EX_121), recording',
     ver + ", recording the DOC-10 installation, the chat switch, the stock-take of 2 November 2026 with the owner's "
     "decisions ST-1 to ST-5 and its correction, the direction document (DIR-1), the owner's process decisions MC-1 "
     "and KISS-1, the MHUP-1 design reviews EX_123 to EX_132 with the owner's decisions MHUP-Q10, MHUP-Q1, MHUP-B02, "
     "MHUP-C03, MHUP-B04, MHUP-Q11 and MHUP-D1 to MHUP-D3, the ratification of the MHUP-1 design v0.1r5 (MHUP-R) and "
     "the rules it amends, the staged AI handover (HO-2), and H-1 v1r8 with its introductory blurb; v0.23 OWNER-RATIFIED 1 November "
     "2026 (content reviewed in EX_117, EX_119 and EX_121), recording"),
    ('Register v0.23 is installed with the snapshot package, by the document-only procedure, in one commit identified after installation.',
     'Register v0.23 is installed with the snapshot package, by the document-only procedure, in one commit identified after installation. '
     'For v0.24, the DOC-10 installation commit `7bb0bfd`, the owner\'s commits `905ecee` and `f47ce14` to `6de0d99`, and the exchange '
     'records from `446bf38` onward were verified by Claude from GitHub; the Windows results are owner-reported. Register v0.24 is '
     'installed with DOC-11, the Claude handover package (document-only, with a verifier), in one commit identified after installation, after the reviewer\'s Step 1.1 review of that package (HO-2).'),
    ('\n## Interpretation and verification\n\n- **Current status (register v0.23; read this first, EX_117 C01).**',
     '\n' + NEW_SECTION + '## Interpretation and verification\n\n'
     '- **Current status (register v0.24; read this first).** Since register v0.23 no code was installed and no '
     'real-data run, results update or report took place. The MHUP-1 design is ratified (MHUP-R) and authorises '
     'nothing by itself. First comes the staged Claude handover (HO-2): the reviewer\'s review of the handover '
     'package, the replacement Claude chat\'s verified takeover and the owner\'s authorisation to resume; then '
     'MHUP-A\'s and MHUP-B\'s code reviews and installs, then the owner\'s Approvals 1 to 4 per game, each separately. The bullet below, from register v0.23, still describes the '
     'position on past runs and on permissions.\n'
     '- **Current status (register v0.23; read this first, EX_117 C01).**'),
]
for old, new in EDITS:
    n = t.count(old)
    assert n == 1, (n, old[:80])
    assert all(ord(c) < 128 for c in new), old[:60]
    t = t.replace(old, new)
open(out, 'wb').write(t.encode('utf-8'))
print(out, hashlib.sha256(t.encode()).hexdigest(), len(t.splitlines()), 'lines')
