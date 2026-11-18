"""Build H-1 v6 and its blurb (CANDIDATE; written 18 November 2026 at the owner's instruction).
Usage: python3 -I make_h1_v6.py REPO_ROOT OUT_DIR

Reads doc/HANDOVER/Claude_Primary_Handover_H1_v5.md from REPO_ROOT (asserted by SHA-256), applies counted edits (each old
text must occur exactly once) and whole-part replacements from the fragments beside this script, asserts that section 2A
is unchanged byte for byte, computes the identity rows from the repository's own files, and writes the handover and the
blurb (blurb_v6.md) to OUT_DIR. Reads nothing else; writes nothing else.
"""
import hashlib, os, sys
assert len(sys.argv) == 3, 'usage: make_h1_v6.py REPO_ROOT OUT_DIR'
REPO, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
V5 = '3f0c0b1adef03947c05c180b2f3081efd2111f735b753abcea22ec01f555a3ae'
V5B = '11387112c91238cf20ff15b629c5b7bc778ec3f3999685aeea5a1b23f757b8aa'


def sha(path):
    return hashlib.sha256(open(os.path.join(REPO, path), 'rb').read()).hexdigest()
def rd(path, want):
    b = open(os.path.join(REPO, path), 'rb').read()
    assert hashlib.sha256(b).hexdigest() == want, f'{path}: not the ratified bytes'
    t = b.decode('ascii'); assert '\r' not in t
    return t
def frag(name):
    t = open(os.path.join(HERE, 'frag', name), encoding='ascii', newline='').read(); assert '\r' not in t
    return t
def one(s, old, new, label):
    n = s.count(old); assert n == 1, f'{label}: expected one occurrence, found {n}'
    return s.replace(old, new)
def line_starting(s, start, label):
    assert s.count(start) == 1, label
    i = s.index(start)
    return s[i:s.index('\n', i) + 1]
def part(s, start, end, new, label):
    assert s.count(start) == 1 and s.count(end) == 1, label
    a, b = s.index(start), s.index(end); assert a < b, label
    return s[:a] + new + s[b:]
def section(s, start, end):
    return s[s.index(start):s.index(end)]


s = rd('doc/HANDOVER/Claude_Primary_Handover_H1_v5.md', V5)
assert sha('doc/HANDOVER/Claude_Primary_Handover_H1_v5_introductory_blurb.md') == V5B
S2A = section(s, '### 2A. ', '## 3. Project in one paragraph')

s = one(s, '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v5\n',
        '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v6\n', 'title')
s = one(s, line_starting(s, '**Version:** v5, 18 November 2026', 'version'),
        '**Version:** v6, 18 November 2026, late evening (Adelaide, UTC+10:30). A **full edition** built from H-1 v5\'s ratified bytes by counted edits and whole-part replacements (`exchange/CLAUDE_WEB_TOOLS/h1v6/make_h1_v6.py`), as the owner prefers. It brings the handover to the state after the MHUP-B code round\'s three slices passed review (EX_231, EX_237, EX_242) and after **the owner\'s decisions of the evening of 18 November 2026 on how production is deployed and run** (section 0B item 12): a separate production folder with no Git at all, one re-runnable deploy tool, end-of-run ZIP snapshots, rollback by restore, and nothing installed until that is designed, reviewed and built.\n', 'version line')
s = one(s, line_starting(s, '**Status:** OWNER-RATIFIED 18 November 2026', 'status'),
        '**Status:** CANDIDATE, written on 18 November 2026 at the owner\'s instruction for the next Claude chat. Not yet reviewed or ratified. Until the owner ratifies it, the installed handover is H-1 v5 (RAT-37), which stays authoritative for the standing rules; for the owner\'s decisions since it (decision log entries 92 to 98) the authority is the decision log and `exchange/EX_243_Claude.md`, which this edition summarises. `exchange/CONTINUITY_NOW.md` says which edition is in force.\n', 'status line')
s = one(s, line_starting(s, '**Replaces, for future roles:**', 'replaces'),
        '**Replaces, for future roles:** once ratified, H-1 v5 and its blurb (RAT-37), which stay in `doc/HANDOVER/` as history; and, as before, H-1 v4, v3, v2, v1r8, its deltas and the older editions listed in v1r3\'s header. D-1 and ADD-2 are inputs, not authority.\n', 'replaces line')
s = one(s, 'Claude_Primary_Handover_H1_v5_introductory_blurb.md', 'Claude_Primary_Handover_H1_v6_introductory_blurb.md', 'blurb name')
s = part(s, '## 0B. The state at this edition (18 November 2026)', '## 1. Roles and workflow (agreed position v0.1r1, ratified)\n', frag('frag_0B.md'), 'section 0B')
row = line_starting(s, '- **The owner sometimes settles a question in his conversation with the reviewer.**', '8.8 last')
s = one(s, row, row + frag('frag_8_8_add2.md'), '8.8 lessons')
s = part(s, '1. **Done since v4 (17 and 18 November 2026; section 0B has the detail):**', '5. **WF-1C** (WORKERS-1; roadmap item 10d)', frag('frag_10_head.md'), 'section 10 items 1-4')
s = one(s, 'At this edition the newest is EX_237 (the reviewer: slice 2 PASS).',
        'At this edition the newest is EX_243 (Claude: the owner\'s decisions on production deployment, for the reviewer\'s record).', 'EX numbering')
s = part(s, '### 12.8 Open items at this edition (18 November 2026)', '- **The reminders** (`exchange/OWNER_REMINDERS.md`', frag('frag_12_8.md'), '12.8 head')
s = one(s, '\n---\n\n## Appendix A. Identities (non-self-referential)\n', '\n' + frag('frag_12_11.md') + '\n---\n\n## Appendix A. Identities (non-self-referential)\n', '12.11')
old_row = line_starting(s, '| MHUP-B staged code (not installed) |', 'staged code row')
rows = (
    '| H-1 v5 (predecessor; OWNER-RATIFIED 18 November 2026, RAT-37) | `doc/HANDOVER/Claude_Primary_Handover_H1_v5.md`, `%s`; its blurb `%s` |\n' % (V5, V5B) +
    '| The owner\'s decisions on production deployment: the record sent to the reviewer (18 November 2026; decision log entries 92 to 98) | `exchange/EX_243_Claude.md`, `%s` |\n' % sha('exchange/EX_243_Claude.md') +
    '| The reviewer\'s passes of the three slices | `exchange/EX_231_ChatGPT.md`, `%s`; `exchange/EX_237_ChatGPT.md`, `%s`; `exchange/EX_242_ChatGPT.md`, `%s` |\n' % (sha('exchange/EX_231_ChatGPT.md'), sha('exchange/EX_237_ChatGPT.md'), sha('exchange/EX_242_ChatGPT.md')) +
    '| MHUP-B staged code (not installed; all three slices passed) | `exchange/CLAUDE_WEB_TOOLS/mhupb/slice1/` (EX_231 PASS), `slice2/` (EX_236; EX_237 PASS) and `slice3/` (EX_241; EX_242 PASS; tree digest `ef2b67e04c500ee940b765bb5a427666430f73ea70fc3a2b1f3e24a1f50e9d13`, recipe in `slice3/README.md`) |\n')
s = one(s, old_row, rows, 'app A rows')
s = part(s, '## Appendix B. Changes in v5', '*End of H-1.*', frag('frag_appB.md'), 'appendix B')

assert section(s, '### 2A. ', '## 3. Project in one paragraph') == S2A, 'section 2A changed'
assert '\r' not in s and s.endswith('\n') and not s.endswith('\n\n')
assert s.count('## 0B. ') == 1 and s.count('## Appendix B. Changes in v6\n') == 1 and s.count('### 12.10 ') == 1 and s.count('### 12.11 ') == 1
assert s.count('**12. Where production runs') == 1
s.encode('ascii')

b = frag('blurb_v6.md')
assert b.endswith('\n')
os.makedirs(OUT, exist_ok=True)
for name, text in (('Claude_Primary_Handover_H1_v6_CANDIDATE.md', s), ('Claude_Primary_Handover_H1_v6_CANDIDATE_introductory_blurb.md', b)):
    data = text.encode('ascii'); open(os.path.join(OUT, name), 'wb').write(data)
    print(name, len(data), hashlib.sha256(data).hexdigest())
