#!/usr/bin/env python3
"""RAT-32 finalisation (Claude, 15 November 2026): the owner ratified H-1 v3, its blurb and register v0.30 at about 09:10.
Changes only status wording, as RAT-31's round did: H-1 v3's status line (reviewed candidate asserted by SHA-256), and in
register v0.30's builder inputs its version line and the section's status sentence and table rows. Then rebuild v0.30.
Usage: python3 -I finalise_rat32.py REPO_ROOT"""
import hashlib, os, subprocess, sys
assert len(sys.argv) == 2
repo = sys.argv[1]
T = os.path.join(repo, 'exchange/CLAUDE_WEB_TOOLS')
def edit(path, pairs, sha=None):
    b = open(path, 'rb').read()
    if sha: assert hashlib.sha256(b).hexdigest() == sha, f'{path}: not the reviewed bytes'
    s = b.decode('ascii')
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:70], s.count(old)); s = s.replace(old, new)
    open(path, 'wb').write(s.encode('ascii'))
h1 = os.path.join(T, 'h1v3/out/Claude_Primary_Handover_H1_v3.md')
edit(h1, [("**Status:** CANDIDATE, 15 November 2026, for the reviewer's documentary review (EX_190) and the owner's "
           "ratification; once ratified and installed it replaces H-1 v2 (RAT-31), which stays in `doc/HANDOVER/` as history.",
           "**Status:** OWNER-RATIFIED 15 November 2026, about 09:10 (RAT-32; register v0.30; record "
           "`exchange/DECISIONS/DECISION_LOG.md`, entry 6), after the reviewer's documentary review (EX_191) and the corrections "
           "it asked for (EX_192); installed by the owner's documentation commit, which the next register edition records. It "
           "replaces H-1 v2 (RAT-31), which stays in `doc/HANDOVER/` as history.")],
     sha='016b809ef8a8dad18a91d8e7f92884846eb6ee6370576ad789e1be96d1244818')
edit(os.path.join(T, 'register/register_v30_section.md'), [
    (" Its status and this\nregister's become final only on the owner's ratification (the next RAT number is RAT-32).\n",
     "\n\n**RAT-32 (owner, 15 November 2026, about 09:10).** Record: `exchange/DECISIONS/DECISION_LOG.md`, entry 6. Asked whether he\n"
     "ratifies \"the three reviewed files for installation: H-1 v3, its blurb, and register v0.30 (RAT-32)\", with H-1 v2 staying in\n"
     "`doc/HANDOVER/` as history, the owner answered \"Yes, ratify all three\". H-1 v3 replaces H-1 v2 as the operative Claude\n"
     "handover; H-2 v2 r1 stays the reviewer's. Only H-1 v3's status line, and this register's version line, this paragraph and\n"
     "its table's status cells, changed after the review. The ratification authorises the documentation install only, nothing for\n"
     "Mode H. The install commit cannot be named here; the next register edition records it.\n"),
    ("| CANDIDATE (EX_190); `@H1V3@` |", "| OWNER-RATIFIED 15 Nov 2026 (RAT-32); `@H1V3@` |"),
    ("| CANDIDATE (EX_190); `@H1V3B@` |", "| OWNER-RATIFIED 15 Nov 2026 (RAT-32); `@H1V3B@` |"),
])
edit(os.path.join(T, 'register/make_register_v30.py'), [
    ("'**Register version:** v0.30, 15 November 2026, CANDIDATE (written by Claude from the records; for the reviewer\\'s '\n"
     "     'documentary review, EX_190, and the owner\\'s ratification with H-1 v3), recording",
     "'**Register version:** v0.30, 15 November 2026, OWNER-RATIFIED 15 November 2026, about 09:10 (RAT-32, with H-1 v3; '\n"
     "     'written by Claude from the records; reviewed in EX_190 to EX_192), recording")])
r = subprocess.run([sys.executable, '-I', os.path.join(T, 'register/make_register_v30.py'), os.path.join(repo, 'doc/RATIFICATION_REGISTER_v0_29.md'),
                    os.path.join(T, 'register/register_v30_section.md'), h1,
                    os.path.join(T, 'h1v3/out/Claude_Primary_Handover_H1_v3_introductory_blurb.md'),
                    os.path.join(T, 'register/RATIFICATION_REGISTER_v0_30.md')], capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip()); assert r.returncode == 0
for p in (h1, os.path.join(T, 'h1v3/out/Claude_Primary_Handover_H1_v3_introductory_blurb.md'), os.path.join(T, 'register/RATIFICATION_REGISTER_v0_30.md')):
    print(hashlib.sha256(open(p, 'rb').read()).hexdigest(), os.path.basename(p))
