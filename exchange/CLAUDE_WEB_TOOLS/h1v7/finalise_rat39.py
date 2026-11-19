"""Finalise H-1 v7r1 after the owner's ratification (RAT-39, 19 November 2026, 23:25): the status line only.
Usage: python3 -I finalise_rat39.py REPO_ROOT
Reads the v7r1 candidate and its blurb (asserted by SHA-256), replaces the one status line, and writes
doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md and doc/HANDOVER/Claude_Primary_Handover_H1_v7r1_introductory_blurb.md
(the blurb's bytes unchanged). Writes nothing else.
"""
import hashlib, os, sys
assert len(sys.argv) == 2
R = sys.argv[1]
C = 'ed3513f5c7400ca9bb9f0a915bb9ed93176d040c663acb5b821be23e221ec667'
CB = '76be41b0ecb91e0c1e9c1c07f1ae01c925d9590624c96256723013d0d41992a6'
D = os.path.join(R, 'exchange/CLAUDE_WEB_TOOLS/h1v7/out_r1')
s = open(os.path.join(D, 'Claude_Primary_Handover_H1_v7r1_CANDIDATE.md'), 'rb').read()
b = open(os.path.join(D, 'Claude_Primary_Handover_H1_v7r1_CANDIDATE_introductory_blurb.md'), 'rb').read()
assert hashlib.sha256(s).hexdigest() == C and hashlib.sha256(b).hexdigest() == CB
t = s.decode('ascii')
i = t.index('**Status:** CANDIDATE (v7r1)'); j = t.index('\n', i)
assert t.count('**Status:** ') == 1
new = ("**Status:** OWNER-RATIFIED 19 November 2026, 23:25 Australia/Adelaide (RAT-39; decision log entry 106), after the "
       "reviewer's PASS of this candidate at commit `39f3ef7`; finalised by this status line only (candidate SHA-256 "
       "`ed3513f5...e221ec667`). It is the installed Claude handover; H-1 v6 (RAT-38) stays in `doc/HANDOVER/` as history. "
       "For anything decided after it, the decision log and `exchange/CONTINUITY_NOW.md` are the authority.")
t = t[:i] + new + t[j:]
t.encode('ascii')
H = os.path.join(R, 'doc/HANDOVER')
for name, data in (('Claude_Primary_Handover_H1_v7r1.md', t.encode('ascii')), ('Claude_Primary_Handover_H1_v7r1_introductory_blurb.md', b)):
    p = os.path.join(H, name); assert not os.path.exists(p), p
    open(p, 'wb').write(data); print(name, hashlib.sha256(data).hexdigest())
