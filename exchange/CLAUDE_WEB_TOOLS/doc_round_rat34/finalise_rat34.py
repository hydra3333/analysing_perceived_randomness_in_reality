#!/usr/bin/env python3
"""Finalise the RAT-34 files (Claude, 17 November 2026). Reads the reviewed candidates (asserted by SHA-256), makes only the
status changes the register's RAT-34 paragraph allows (H-1 v4's status line; the register's version line, its RAT-34
paragraph and its table's status cells), and writes the four files for doc/ into OUT_DIR, with the ratified supplement
copied unchanged. Usage: python3 -I finalise_rat34.py REPO_ROOT OUT_DIR"""
import hashlib, os, sys
assert len(sys.argv) == 3, 'usage: finalise_rat34.py REPO_ROOT OUT_DIR'
R, OUT = sys.argv[1:3]
sha = lambda b: hashlib.sha256(b).hexdigest()
def rd(rel, want):
    b = open(os.path.join(R, rel), 'rb').read(); assert sha(b) == want, f'{rel}: not the reviewed bytes'; return b
H1 = rd('exchange/CLAUDE_WEB_TOOLS/h1v4/out/Claude_Primary_Handover_H1_v4.md', '0f34ec4c3a826ef18a840b0492d9903ea92c0356527c96970d0aa2b7566f2717').decode('utf-8')
H1B = rd('exchange/CLAUDE_WEB_TOOLS/h1v4/out/Claude_Primary_Handover_H1_v4_introductory_blurb.md', '2cfa6cf521aabee3bbef257eb8a917caea92c73ddac54e90ddda79464ecd67be')
REG = rd('exchange/CLAUDE_WEB_TOOLS/register/RATIFICATION_REGISTER_v0_31.md', '465dc50a55120e8afdd983475c7d94b8ac0ff654e46507df96532862ac7fb5f2').decode('utf-8')
SUP = rd('exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_v0_7_RATIFICATION_CANDIDATE.md', '04c4f68a638fff7d93f06d25084d1454bdfc443e9aab6b0b12ffdfd8b5323d26')
def one(s, old, new, label):
    n = s.count(old); assert n == 1, f'{label}: expected one occurrence, found {n}'; return s.replace(old, new)
def line(s, start):
    assert s.count(start) == 1, start; i = s.index(start); return s[i:s.index('\n', i) + 1]
H1 = one(H1, line(H1, '**Status:** CANDIDATE for the owner\'s ratification with register v0.31 (RAT-34)'),
         '**Status:** OWNER-RATIFIED 17 November 2026, about 15:15 (RAT-34; register v0.31; record `exchange/DECISIONS/DECISION_LOG.md`, entry 63), after the reviewer\'s documentary review (EX_214; **EX_215: DOCUMENTARY PASS**). It replaces H-1 v3, which stays in `doc/HANDOVER/` as history. Committed into `doc/` by Claude directly (section 0B, item 4); the next register edition records the commit.\n', 'H-1 status')
h1b = H1.encode('utf-8'); h1_sha = sha(h1b); h1b_sha = sha(H1B)
REG = one(REG, "**Register version:** v0.31, 17 November 2026, CANDIDATE for the owner's ratification (RAT-34, with H-1 v4; written by "
               "Claude from the records; for review in EX_214)",
          "**Register version:** v0.31, 17 November 2026, OWNER-RATIFIED 17 November 2026, about 15:15 (RAT-34, with H-1 v4; written by "
          "Claude from the records; reviewed in EX_214 and EX_215)", 'version line')
REG = one(REG, line(REG, '**RAT-34 (pending).**') + line(REG, '16 November 2026 comes into force with them. On ratification,')
          + line(REG, "table's status cells, and H-1 v4's status line, change;") + line(REG, 'register, H-1 v4 and its blurb, and the RAT-33 supplement) and checks them from GitHub.'),
          "**RAT-34 (owner, 17 November 2026, about 15:15).** Record: `exchange/DECISIONS/DECISION_LOG.md`, entry 63. After the\n"
          "reviewer's documentary review (**EX_215: DOCUMENTARY PASS**; ratification recommended; H-2 v3 to be updated by the reviewer\n"
          "and ratified separately), asked whether he ratifies \"register v0.31, H-1 v4 and its blurb, with your approach of 16 November\n"
          "coming into force with them\", the owner answered \"Yes, ratify (Recommended)\". **The approach of 16 November 2026, with the\n"
          "EX_206 conditions as recorded above, is in force from RAT-34.** H-1 v4 replaces H-1 v3 as the operative Claude handover;\n"
          "H-2 v2 r1 stays the reviewer's. Only H-1 v4's status line, and this register's version line, this paragraph and its table's\n"
          "status cells, changed after the review. Claude commits the ratified files into `doc/` directly (this register, H-1 v4 and\n"
          "its blurb, and the RAT-33 supplement) and checks them from GitHub; the next register edition records that commit. RAT-34\n"
          "authorises no code, run, install, re-forecast, score or registration of OV-1.\n", 'RAT-34 paragraph')
REG = one(REG, '| CANDIDATE for RAT-34; `0f34ec4c3a826ef18a840b0492d9903ea92c0356527c96970d0aa2b7566f2717` |',
          f'| OWNER-RATIFIED 17 Nov 2026 (RAT-34); `{h1_sha}` |', 'H-1 cell')
REG = one(REG, '| CANDIDATE for RAT-34; `2cfa6cf521aabee3bbef257eb8a917caea92c73ddac54e90ddda79464ecd67be` |',
          f'| OWNER-RATIFIED 17 Nov 2026 (RAT-34); `{h1b_sha}` |', 'blurb cell')
regb = REG.encode('utf-8')
os.makedirs(os.path.join(OUT, 'HANDOVER'), exist_ok=True)
for rel, b in (('RATIFICATION_REGISTER_v0_31.md', regb), ('HANDOVER/Claude_Primary_Handover_H1_v4.md', h1b),
               ('HANDOVER/Claude_Primary_Handover_H1_v4_introductory_blurb.md', H1B),
               ('Predictive_Randomness_MHUPB_Design_Supplement_v0_7.md', SUP)):
    open(os.path.join(OUT, rel), 'wb').write(b); print(f'{sha(b)}  doc/{rel}  ({len(b)} bytes)')
