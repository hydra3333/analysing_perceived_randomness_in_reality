"""Build the H-1 v4 DRAFT and its blurb draft. Usage: python3 -I make_h1_v4.py REPO_ROOT OUT_DIR

Reads doc/HANDOVER/Claude_Primary_Handover_H1_v3.md and its blurb from REPO_ROOT (asserted by SHA-256), applies counted
edits (each old text must occur exactly once) and whole-part replacements from the fragments beside this script, asserts
that section 2A is unchanged byte for byte, and writes the two drafts to OUT_DIR. Reads nothing else; writes nothing else.
"""
import hashlib, os, sys
assert len(sys.argv) == 3, 'usage: make_h1_v4.py REPO_ROOT OUT_DIR'
REPO, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = 'ddefe7006aa17cfd0a9a8996bd7122aed537d8d66accee92b2e5d737aefbaa54'
V3B = 'd1df63bf18bc7becc96212ac0d76d519a2a5c4d6b367251116b294382573dd4d'

def rd(path, sha):
    b = open(os.path.join(REPO, path), 'rb').read()
    assert hashlib.sha256(b).hexdigest() == sha, f'{path}: not the ratified bytes'
    t = b.decode('utf-8'); assert '\r' not in t
    return t
def frag(name):
    t = open(os.path.join(HERE, name), encoding='utf-8', newline='').read(); assert '\r' not in t
    return t
def one(s, old, new, label):
    n = s.count(old); assert n == 1, f'{label}: expected one occurrence, found {n}'
    return s.replace(old, new)
def line_starting(s, start, label):
    i = s.index(start); assert s.count(start) == 1, label
    return s[i:s.index('\n', i) + 1]
def part(s, start, end, new, label):
    assert s.count(start) == 1 and s.count(end) == 1, label
    a, b = s.index(start), s.index(end); assert a < b, label
    return s[:a] + new + s[b:]
def section(s, start, end):
    return s[s.index(start):s.index(end)]

s = rd('doc/HANDOVER/Claude_Primary_Handover_H1_v3.md', V3)
S2A = section(s, '### 2A. ', '## 3. Project in one paragraph')

s = one(s, '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v3\n',
        '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v4 (DRAFT)\n', 'title')
s = one(s, line_starting(s, '**Version:** v3, 15 November 2026', 'version'),
        '**Version:** v4 DRAFT, 16 November 2026, night (Adelaide, UTC+10:30). Built from H-1 v3\'s ratified bytes by counted edits and whole-part replacements (`exchange/CLAUDE_WEB_TOOLS/h1v4/make_h1_v4.py`). It brings the handover to the state after Mode H: both games sealed and read, D5 done, and the approach the owner agreed on 16 November 2026. **Section 0B is new and prevails over older statements below it**; Appendix B says what this draft rewrites and what it does not yet.\n', 'version line')
s = one(s, line_starting(s, '**Status:** OWNER-RATIFIED 15 November 2026', 'status'),
        '**Status:** **DRAFT. Not reviewed and not ratified.** Written at the owner\'s request on the night of 16 November 2026 for risk management, so that a new chat can take over if this one ends. Until it is reviewed and ratified, the installed handover is H-1 v3 (RAT-32; register v0.30), read together with `exchange/CONTINUITY_NOW.md`. When ratified it replaces H-1 v3.\n', 'status line')
s = one(s, 'Never display, paste or compute with an outcome for Powerball >= 1577 or Oz Lotto >= 1694.\n\n---\n\n## 0. First actions',
        'The older rule against displaying or computing with an outcome for Powerball >= 1577 or Oz Lotto >= 1694 was replaced by the approach the owner agreed on 16 November 2026 (section 0B, item 4), which the reviewer had still to be consulted on; check `exchange/CONTINUITY_NOW.md`.\n\n---\n\n## 0. First actions', 'holdout discipline')
s = one(s, 'Claude_Primary_Handover_H1_v3_introductory_blurb.md', 'Claude_Primary_Handover_H1_v4_introductory_blurb.md', 'blurb name')
s = one(s, '## 1. Roles and workflow (agreed position v0.1r1, ratified)\n', frag('frag_0B.md') + '## 1. Roles and workflow (agreed position v0.1r1, ratified)\n', 'insert 0B')
s = one(s, '### 5.1 Data and holdout\n\n',
        '### 5.1 Data and holdout\n\n**Read section 0B first.** Both holdouts are now opened, scored and sealed, and their draws are ordinary history. The bullets below are kept as the record of how the data was protected up to the seals. Where they forbid the AI chats to see draw values (the quarantine\'s display rule; Q7) they are replaced by the approach the owner agreed on 16 November 2026. Still in force: Lotterywest-GOV as the only source through the owner\'s updater, and no lottery-results searches by any AI. Out of date: "the updater has never run live" (it ran each game\'s first update on 15 and 16 November 2026; both masters are at version 2).\n\n', '5.1 lead')
s = part(s, '1. **Done since v2 (14 November 2026, afternoon and evening):**', '5. **WF-1C** (WORKERS-1; roadmap item 10d)', frag('frag_10_head.md'), 'section 10 items 1-4')
s = one(s, '## 11. Gates that stay closed\n\n',
        '## 11. Gates that stay closed\n\n**At this edition (section 0B):** Mode H\'s gates are behind us; the sealed studies are never reopened or rescored. Still closed until the owner\'s own go, each separately: every install; every real-data run, results update, catch-up and weekly session; every walk-forward batch and report run; Windows lifecycle and destructive tests; any dependency change. The paragraph below is v3\'s and describes the gates as they stood before Mode H.\n\n', '11 lead')
s = part(s, '### 12.8 Open items at this edition (15 November 2026)', '- **The reminders** (`exchange/OWNER_REMINDERS.md`', frag('frag_12_8.md'), '12.8 head')
s = part(s, '## Appendix B. Changes in v3', '*End of H-1.*', frag('frag_appB.md'), 'appendix B')

assert section(s, '### 2A. ', '## 3. Project in one paragraph') == S2A, 'section 2A changed'
assert '\r' not in s and s.endswith('\n') and not s.endswith('\n\n')
assert s.count('## 0B. ') == 1 and s.count('## Appendix B. Changes in v4 (DRAFT)') == 1

b = rd('doc/HANDOVER/Claude_Primary_Handover_H1_v3_introductory_blurb.md', V3B)
b = one(b, '- goes with H-1 v3\n', '- goes with H-1 v4 (DRAFT)\n', 'blurb title')
b = one(b, line_starting(b, 'Written by Claude on 15 November 2026 with H-1 v3', 'blurb written'),
        'Written by Claude on 16 November 2026 (night) with the H-1 v4 DRAFT. **Both are drafts, not reviewed or ratified**; the\n'
        'installed pair is H-1 v3 and its blurb. If this chat is started from this draft, say so in your first reply.\n', 'blurb written line')
b = one(b, '- the handover **H-1 v3** (`doc/HANDOVER/Claude_Primary_Handover_H1_v3.md`), one complete file: read all of it, including\n',
        '- the handover **H-1 v4 DRAFT** (`exchange/CLAUDE_WEB_TOOLS/h1v4/out/Claude_Primary_Handover_H1_v4_DRAFT.md`; once ratified,\n'
        '  `doc/HANDOVER/Claude_Primary_Handover_H1_v4.md`), one complete file: **read its section 0B first**, then all of it, including\n', 'blurb handover name')
b = one(b, '   Read H-1 v3 in full.', '   Read H-1 v4 (draft) in full, section 0B first.', 'blurb read')
b = one(b, 'Check the hashes H-1 quotes with a tool. Never open\n   anything under `source_data/`, `results/` or `transitory_data/`.',
        'Check the hashes H-1 quotes with a tool. Since 16 November\n   2026 the owner\'s agreed approach lets the AI chats read `source_data/` and `results/` (H-1 section 0B, item 4); never write there.', 'blurb open rule')
b = one(b, '**Where things stood on 15 November 2026.**\n',
        '**Where things stood on the night of 16 November 2026 (this overrides the older bullets below; H-1 section 0B has the detail).**\n'
        '- **Mode H is complete:** Oz Lotto sealed 15 November, Powerball 16 November; both reports read independently by the reviewer\n'
        '  and Claude, and the readings agree: no statistically significant predictive advantage was demonstrated under the predeclared\n'
        '  Mode H tests (EX_200 to EX_205). The freeze has ended. The owner committed the results at `c7622fa` (D5).\n'
        '- **The owner agreed a new approach on 16 November 2026** (`exchange/DECISIONS/AGREED_APPROACH_2026_11_16.md`): all draws are\n'
        '  treated the same and the AI chats may see draw values and results; no lottery websites or results searches by the AIs;\n'
        '  results count only from the reviewed programs (chat calculations are "suggestive"); nothing runs without his go; Claude may\n'
        '  commit documents directly once reviewed and ratified, code still goes by reviewed package and his Windows install, Claude\n'
        '  never writes the data folders, nothing is deleted. The reviewer had still to be consulted: check `exchange/CONTINUITY_NOW.md`.\n'
        '- **Next:** MHUP-B is the priority (design only authorised; inputs in `exchange/DECISIONS/MHUPB_DESIGN_INPUTS_2026_11_16.md`),\n'
        '  with register v0.31 and the ratification of H-1 v4 alongside.\n'
        '\n**Where things stood on 15 November 2026 (history).**\n', 'blurb where things stood')
b = one(b, '- Never display, paste or compute with an outcome for Powerball draw 1577 or later, or Oz Lotto draw 1694 or later. Never open\n  `source_data`, `results` or `transitory_data`.\n',
        '- (Replaced on 16 November 2026 by the owner\'s agreed approach, pending the reviewer\'s consultation: the AI chats may now see\n  draw values and read `source_data` and `results`. They never write there, and they never fetch results themselves.)\n', 'blurb display rule')
b = one(b, 'Since 15 November 2026: <"see exchange/CONTINUITY_NOW.md", plus anything newer>.', 'Since 16 November 2026: <"see exchange/CONTINUITY_NOW.md", plus anything newer>.', 'blurb since')
assert '\r' not in b and b.endswith('\n')

os.makedirs(OUT, exist_ok=True)
for name, text in (('Claude_Primary_Handover_H1_v4_DRAFT.md', s), ('Claude_Primary_Handover_H1_v4_DRAFT_introductory_blurb.md', b)):
    data = text.encode('utf-8'); open(os.path.join(OUT, name), 'wb').write(data)
    print(name, len(data), hashlib.sha256(data).hexdigest())
