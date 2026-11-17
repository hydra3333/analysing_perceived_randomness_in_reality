"""Build H-1 v5 and its blurb (CANDIDATE; written 18 November 2026 at the owner's request).
Usage: python3 -I make_h1_v5.py REPO_ROOT OUT_DIR

Reads doc/HANDOVER/Claude_Primary_Handover_H1_v4.md from REPO_ROOT (asserted by SHA-256), applies counted edits (each old
text must occur exactly once) and whole-part replacements from the fragments beside this script, asserts that section 2A
is unchanged byte for byte, computes the identity rows from the repository's own files, and writes the handover and the
blurb (a full new text, blurb_v5.md) to OUT_DIR. Reads nothing else; writes nothing else.
"""
import hashlib, os, sys
assert len(sys.argv) == 3, 'usage: make_h1_v5.py REPO_ROOT OUT_DIR'
REPO, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
V4 = 'cc52ed4f988d9a4044d3699de7626717b4a0fd760e927aa1ad582187edbc8d3d'
V4B = '2cfa6cf521aabee3bbef257eb8a917caea92c73ddac54e90ddda79464ecd67be'


def sha(path):
    return hashlib.sha256(open(os.path.join(REPO, path), 'rb').read()).hexdigest()
def rd(path, want):
    b = open(os.path.join(REPO, path), 'rb').read()
    assert hashlib.sha256(b).hexdigest() == want, f'{path}: not the ratified bytes'
    t = b.decode('utf-8'); assert '\r' not in t
    return t
def frag(name):
    t = open(os.path.join(HERE, name), encoding='utf-8', newline='').read(); assert '\r' not in t
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


s = rd('doc/HANDOVER/Claude_Primary_Handover_H1_v4.md', V4)
assert sha('doc/HANDOVER/Claude_Primary_Handover_H1_v4_introductory_blurb.md') == V4B
S2A = section(s, '### 2A. ', '## 3. Project in one paragraph')

s = one(s, '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v4\n',
        '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v5\n', 'title')
s = one(s, line_starting(s, '**Version:** v4, 17 November 2026', 'version'),
        '**Version:** v5, 18 November 2026 (Adelaide, UTC+10:30). A **full edition** built from H-1 v4\'s ratified bytes by counted edits and whole-part replacements (`exchange/CLAUDE_WEB_TOOLS/h1v5/make_h1_v5.py`), as the owner prefers. It brings the handover to the state of the MHUP-B code round: the code plan v0.3 and the design supplement v0.8 ratified (RAT-35), slice 1 passed, slice 2 built, reviewed and corrected, the joint working principle, and **the owner\'s clarified research model of 18 November 2026**. **Section 0B is rewritten and prevails over older statements below it**; section 12.10 is new; Appendix B lists what changed.\n', 'version line')
s = one(s, line_starting(s, '**Status:** OWNER-RATIFIED 17 November 2026', 'status'),
        '**Status:** CANDIDATE, written on 18 November 2026 at the owner\'s request so that no knowledge is lost if the chat ends. Not yet reviewed or ratified. Until the owner ratifies it, the installed handover is H-1 v4 (RAT-34), which stays authoritative for the standing rules; for the state of the work and the owner\'s decisions since 17 November 2026 the authority is the decision log (entries 64 on), the records in `exchange/DECISIONS/` and the EX messages, which this edition summarises. `exchange/CONTINUITY_NOW.md` says which edition is in force.\n', 'status line')
s = one(s, line_starting(s, '**Baseline described:**', 'baseline'),
        '**Baseline described:** `main` on 18 November 2026. The installed code is unchanged since H-1 v4: MHUP-A (package commit `2860e86`, release commit `effc179`, 13 November 2026) with the test-only fix `87c4219` and the owner\'s dependency change `cc0ab73`; no file under `src/`, no root `.bat` and no `requirements.txt` has changed since. **MHUP-B\'s code exists only as staged slices under `exchange/CLAUDE_WEB_TOOLS/mhupb/` and is not installed.** The data: both masters at version 2, the sealed Mode H records (`c7622fa`) and the development score records the owner committed on 17 November 2026 (`cc665ce`, which also changed `.gitignore`).\n', 'baseline line')
s = one(s, line_starting(s, '**Replaces, for future roles:**', 'replaces'),
        '**Replaces, for future roles:** once ratified, H-1 v4 and its blurb (RAT-34), which stay in `doc/HANDOVER/` as history; and, as before, H-1 v3, v2, v1r8, its deltas and the older editions listed in v1r3\'s header. D-1 and ADD-2 are inputs, not authority.\n', 'replaces line')
s = one(s, 'Claude_Primary_Handover_H1_v4_introductory_blurb.md', 'Claude_Primary_Handover_H1_v5_introductory_blurb.md', 'blurb name')
s = part(s, '## 0B. The state at this edition (17 November 2026)', '## 1. Roles and workflow (agreed position v0.1r1, ratified)\n', frag('frag/frag_0B.md'), 'section 0B')
s = one(s, line_starting(s, '**Read section 0B first.** Both holdouts are now opened', '5.1 lead'), frag('frag/frag_5_1.md'), '5.1 lead line')
row = line_starting(s, '- **Keep the live path and the reporting apart** (MHUP-B supplement section 2)', '8.8 last')
s = one(s, row, row + frag('frag/frag_8_8_add.md'), '8.8 lessons')
s = part(s, '1. **Done since v3 (15 to 17 November 2026; section 0B has the detail):**', '5. **WF-1C** (WORKERS-1; roadmap item 10d)', frag('frag/frag_10_head.md'), 'section 10 items 1-4')
s = one(s, line_starting(s, '**At this edition (section 0B):** Mode H\'s gates are behind us;', '11 lead'), frag('frag/frag_11_lead.md'), '11 lead line')
s = one(s, 'At this edition the newest is EX_214 (Claude: this edition and register v0.31 for review).',
        'At this edition the newest is EX_236 (Claude: the corrected slice 2).', 'EX numbering')
s = part(s, '### 12.8 Open items at this edition (17 November 2026)', '- **The reminders** (`exchange/OWNER_REMINDERS.md`', frag('frag/frag_12_8.md'), '12.8 head')
s = one(s, '\n---\n\n## Appendix A. Identities (non-self-referential)\n', '\n' + frag('frag/frag_12_10.md') + '---\n\n## Appendix A. Identities (non-self-referential)\n', '12.10')
rows = (
    '| H-1 v4 (predecessor; OWNER-RATIFIED 17 November 2026, RAT-34) | `doc/HANDOVER/Claude_Primary_Handover_H1_v4.md`, `%s`; its blurb `%s` |\n' % (V4, V4B) +
    '| MHUP-B code plan v0.3 (RAT-35, 17 November 2026) | `doc/Predictive_Randomness_MHUPB_Code_Plan_v0_3.md`, `%s` |\n' % sha('doc/Predictive_Randomness_MHUPB_Code_Plan_v0_3.md') +
    '| MHUP-B design supplement v0.8 (RAT-35; governs; v0.7 is history) | `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md`, `%s` |\n' % sha('doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md') +
    '| The joint working principle (18 November 2026; decision log entry 81) | `exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md`, `%s` |\n' % sha('exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md') +
    '| The owner\'s clarified research model: the change note (18 November 2026; decision log entry 84) | `exchange/DECISIONS/OWNER_CLARIFICATION_2026_11_18_EQUAL_DRAWS_AND_OV1_USES.md`, `%s` |\n' % sha('exchange/DECISIONS/OWNER_CLARIFICATION_2026_11_18_EQUAL_DRAWS_AND_OV1_USES.md') +
    '| The reviewer\'s slice 2 review and its record of the owner\'s clarifications | `exchange/EX_233_ChatGPT.md`, `%s`; `exchange/EX_234_ChatGPT.md`, `%s`; `exchange/EX_235_ChatGPT.md`, `%s` |\n' % (sha('exchange/EX_233_ChatGPT.md'), sha('exchange/EX_234_ChatGPT.md'), sha('exchange/EX_235_ChatGPT.md')) +
    '| MHUP-B staged code (not installed) | `exchange/CLAUDE_WEB_TOOLS/mhupb/slice1/` (EX_231 PASS) and `slice2/` (EX_236); each slice message carries its file table and tree digest |\n')
s = one(s, '| The history clean-up crosswalk (6 November 2026) |', rows + '| The history clean-up crosswalk (6 November 2026) |', 'app A rows')
s = part(s, '## Appendix B. Changes in v4', '*End of H-1.*', frag('frag/frag_appB.md'), 'appendix B')

assert section(s, '### 2A. ', '## 3. Project in one paragraph') == S2A, 'section 2A changed'
assert '\r' not in s and s.endswith('\n') and not s.endswith('\n\n')
assert s.count('## 0B. ') == 1 and s.count('## Appendix B. Changes in v5\n') == 1 and s.count('### 12.10 ') == 1
assert '@@' not in s, 'an unfilled token'
s.encode('ascii')

b = frag('frag/blurb_v5.md')
assert b.endswith('\n') and '@@' not in b
os.makedirs(OUT, exist_ok=True)
for name, text in (('Claude_Primary_Handover_H1_v5_CANDIDATE.md', s), ('Claude_Primary_Handover_H1_v5_CANDIDATE_introductory_blurb.md', b)):
    data = text.encode('utf-8'); open(os.path.join(OUT, name), 'wb').write(data)
    print(name, len(data), hashlib.sha256(data).hexdigest())
