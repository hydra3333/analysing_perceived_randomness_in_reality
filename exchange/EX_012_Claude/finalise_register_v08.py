"""Finalise register v0.8 after the owner's ratification (Claude, 28 Oct 2026).

Applies exactly four counted edits to the reviewed candidate r2 (aac76fa0...1671):
  1. the version line: RATIFICATION CANDIDATE -> OWNER-RATIFIED 28 October 2026;
  2. the DOC-2 paragraph: the owner's acceptance of the two-commit delivery as an exception, and the
     reviewer's DOC2-RD-04 (EX_011), as a new bullet;
  3. the post-v0.7 owner decisions: the owner's register v0.8 ratification is implied by (1); a new
     bullet records the Python 3.14.10 upgrade and dependency update, as reported by the owner;
  4. nothing else. Inserted text is ASCII.
Usage: python3 -I finalise_register_v08.py CANDIDATE OUT_FINAL
"""
import hashlib, sys

src, out = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == 'aac76fa0cbc22c332e55ce6c985f99f4829d7bbf83c327513a76439e29e71671'
t = raw.decode('utf-8')
EX011 = 'review/Independent_ChatGPT_EX_011_DOC2_Register_v0_8_NAMES1_Final_Recheck.md'
EX011_SHA = '8c632dbc29916cded75efedecf6e3eea8918f07157e198e9fed2a72e34af6d0e'
EDITS = [
    ('**Register version:** v0.8 RATIFICATION CANDIDATE (drafted 28 October 2026), recording',
     '**Register version:** v0.8 OWNER-RATIFIED 28 October 2026, recording'),
    ('The owner pushed after Claude confirmed that.\n',
     'The owner pushed after Claude confirmed that.\n'
     '- **The owner accepted the two-commit delivery as a one-off exception (28 October 2026; OWNER-DECIDED).** '
     'It is not a precedent: a STOP remains a STOP. The installer STOP results are not recast as PASS. '
     f'The reviewer accepted the installed DOC-2 content on this evidence (DOC2-RD-04, in `{EX011}`, LF copy, `{EX011_SHA}`).\n'),
    ('- **Phone exchange protocol:**',
     '- **Python 3.14.10 and the dependency update** (approved by the owner). The project venv was upgraded from Python 3.14.8 to 3.14.10 with `venv --upgrade`. '
     "The owner's dependency updater then changed no package versions: numpy 2.5.4, scipy 1.18.1, psutil 7.2.2, threadpoolctl 3.7.0, requests 2.34.2, beautifulsoup4 4.15.0 and selenium 4.51.0. "
     'Before NAMES-1, the owner re-ran the current suite on Windows: 60 tests OK with 2 skips, and the other 19 OK. '
     'Moving to Python 3.15 is a separate, later owner decision.\n'
     '- **Phone exchange protocol:**'),
]
for old, new in EDITS:
    assert t.count(old) == 1, old[:60]
    assert all(ord(c) < 128 for c in new)
    t = t.replace(old, new)
open(out, 'wb').write(t.encode('utf-8'))
print(out, hashlib.sha256(t.encode()).hexdigest())
