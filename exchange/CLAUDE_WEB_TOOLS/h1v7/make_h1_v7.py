"""Build H-1 v7 and its blurb (CANDIDATE; written 19 November 2026 at the owner's go, decision log entry 105).
Usage: python3 -I make_h1_v7.py REPO_ROOT OUT_DIR

Reads doc/HANDOVER/Claude_Primary_Handover_H1_v6.md and its blurb from REPO_ROOT (both asserted by SHA-256: the RAT-38
bytes), applies counted edits (each old text must occur exactly once) and whole-part replacements from the fragments
beside this script, asserts that section 2A is unchanged byte for byte, computes the identity rows from the repository's
own files, and writes the handover and the blurb to OUT_DIR. Reads nothing else; writes nothing else.
"""
import hashlib, os, sys
assert len(sys.argv) == 3, 'usage: make_h1_v7.py REPO_ROOT OUT_DIR'
REPO, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
V6 = '6dc8185a72006861c860773a18887ad51135f2bd129bce7a549879a17e280353'
V6B = 'd78249b94ba1af56dd0a2c9cd20fde803ded069098ea4bed04a50b039b97c47c'
H2R4 = 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r4_RATIFICATION_CANDIDATE_20261118.md'
H2R6 = 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r6_RATIFICATION_CANDIDATE_20261118.md'


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


s = rd('doc/HANDOVER/Claude_Primary_Handover_H1_v6.md', V6)
b = rd('doc/HANDOVER/Claude_Primary_Handover_H1_v6_introductory_blurb.md', V6B)
S2A = section(s, '### 2A. ', '## 3. Project in one paragraph')
V6_1211 = section(s, '### 12.11 ', '\n---\n\n## Appendix A')

# --- header
s = one(s, '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v6\n',
        '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v7\n', 'title')
s = one(s, line_starting(s, '**Version:** v6, 18 November 2026', 'version'),
        '**Version:** v7, 19 November 2026, evening (Adelaide, UTC+10:30). A **full edition** built from H-1 v6\'s ratified bytes (RAT-38) by counted edits and whole-part replacements (`exchange/CLAUDE_WEB_TOOLS/h1v7/make_h1_v7.py`), as the owner prefers. It folds in what was decided after v6 was written (section 0B item 13): EX_244 on restore and replay, the owner\'s restore method, Python 3.15 only, no monthly restore test, no replay comparison, the takeover of 19 November 2026 and RAT-38, and the stale lines the takeover found.\n', 'version line')
s = one(s, line_starting(s, '**Status:** CANDIDATE, written on 18 November 2026', 'status'),
        '**Status:** CANDIDATE, written on 19 November 2026 at the owner\'s go (decision log entry 105). Not yet ratified. Until the owner ratifies it, the installed handover is H-1 v6 (RAT-38), whose header still reads CANDIDATE as frozen history; for the decisions since v6 (decision log entries 99 to 105) the authority is the decision log, with `exchange/EX_244_ChatGPT.md` governing restore and replay. On ratification only this status line changes. `exchange/CONTINUITY_NOW.md` says which edition is in force.\n', 'status line')
s = one(s, '**Baseline described:** `main` on 18 November 2026.', '**Baseline described:** `main` on 19 November 2026.', 'baseline')
s = one(s, line_starting(s, '**Replaces, for future roles:**', 'replaces'),
        '**Replaces, for future roles:** once ratified, H-1 v6 and its blurb (RAT-38), which stay in `doc/HANDOVER/` as history; and, as before, H-1 v5, v4, v3, v2, v1r8, its deltas and the older editions listed in v1r3\'s header. D-1 and ADD-2 are inputs, not authority.\n', 'replaces line')

# --- section 0
s = one(s, 'Claude_Primary_Handover_H1_v6_introductory_blurb.md', 'Claude_Primary_Handover_H1_v7_introductory_blurb.md', 'blurb name')
a = s.index("H-2 (the reviewer's handover: its own full edition `ChatGPT_Reviewer_Handover_H2_v2.md`")
z = s.index('its rights)', a) + len('its rights)')
assert s.count("H-2 (the reviewer's handover: its own full edition") == 1 and z - a < 400
s = s[:a] + ("H-2 (the reviewer's handover: the operative edition is H-2 v3r4, `%s`, RAT-36, whose word CANDIDATE is frozen "
             "history; its v3r6 is a candidate; `exchange/CONTINUITY_NOW.md` names any later one: what the reviewer checks "
             "and its rights)" % H2R4) + s[z:]
s = one(s, '(register v0.30 and later;', '(register v0.31, then the decision log for RAT-35 onward, and register v0.30;', 'register in item 2')
s = one(s, "If this file's or the newest register's status line still reads CANDIDATE, stop and ask the owner which handover is in force.",
        "If this file's or the newest register's status line still reads CANDIDATE, stop and ask the owner which handover is in force (`exchange/CONTINUITY_NOW.md` says; H-1 v6 was ratified with its header still reading CANDIDATE, RAT-38).", 'item 3')

# --- section 0B
s = one(s, '## 0B. The state at this edition (18 November 2026): read this', '## 0B. The state at this edition (19 November 2026): read this', '0B title')
s = one(s, 'entries 92 to 98 are the owner\'s decisions on how production is deployed and run). Register v0.31',
        'entries 92 to 98 are the owner\'s decisions on how production is deployed and run; entries 99 to 105 cover the H-1 v4 blurb\'s restore, the takeover of 19 November 2026, RAT-38, EX_244, the restore method, Python 3.15 only, no monthly restore test, no replay comparison and the go for this edition). Register v0.31', '0B pointer')
s = one(s, 'the owner has asked the reviewer to update it with the decisions of item 12.',
        'the owner has asked the reviewer to update it with the decisions of item 12; it has since written H-2 v3r5 and then the v3r6 CANDIDATE, which supersedes v3r5 (item 13).', '0B item 10')
s = one(s, '- **Rollback = restore from backup.** No other rollback machinery.',
        '- **Rollback = restore from backup.** No other rollback machinery. How a restore is done, and what it means for the research, was settled on 19 November 2026: item 13 prevails.', '0B rollback')
s = one(s, 'the deployment design note (section 12.11).\n\n---\n\n## 1. Roles and workflow',
        'the deployment design note (section 12.11).\n' + frag('frag_0B_13.md') + '\n---\n\n## 1. Roles and workflow', '0B item 13')

# --- sections 1 to 11
s = one(s, 'and in and under `CLAUDE_CODE_WORKING_FOLDER_TREE/` (owner, 28 and 29 October 2026; section 8.6). Nothing else.',
        'and in and under `CLAUDE_CODE_WORKING_FOLDER_TREE/` (owner, 28 and 29 October 2026; section 8.6); and, since RAT-34, reviewed and ratified documents into `doc/` (section 1.6). Nothing else.', '1.1')
a = s.index('At this edition the installed register is **v0.29**')
z = s.index('records it.', a) + len('records it.')
assert s.count('At this edition the installed register is **v0.29**') == 1 and z - a < 300
s = s[:a] + ('At this edition the installed register is **v0.31** (`doc/RATIFICATION_REGISTER_v0_31.md`, `%s`, RAT-34); RAT-35 to RAT-38 '
             'and the decisions since are in the decision log, for register v0.32, which travels with the MHUP-B package. Registers '
             'v0.30 and v0.29 are history.' % sha('doc/RATIFICATION_REGISTER_v0_31.md')) + s[z:]
s = one(s, 'the 39 revision-1 variants of E_2, E_3, E_4 (six each), E_6, E_7, E_8, E_9, E_10, E_17, E_18 and E_19 (three each)',
        'the 39 revision-1 variants of E_3 and E_4 (six each) and E_2, E_6, E_7, E_8, E_9, E_10, E_17, E_18 and E_19 (three each)', '5.3 E_2')
s = one(s, '### 7.4 Tests\n\n', '### 7.4 Tests\n\n- **From 19 November 2026: Python 3.15 only** (decision log entry 103). Claude\'s cloud runs use one Python 3.15 build; the authoritative runs are the owner\'s 3.15.2 under Windows (Claude Code task files, T017). Figures below quoted on two Pythons are dated history.\n', '7.4')
s = one(s, '**Claude may not open `results/`;** the owner attaches the `.txt` reports to the chat to share them.',
        'Since RAT-34 (the approach of 16 November 2026) Claude may read `results/` and `source_data/`, never write there; the owner may also attach the `.txt` reports.', '7.5')
s = one(s, "- Run the suite on Linux on the project's Python line (3.13 and a 3.15 build), and the install run-through",
        "- Run the suite on Linux on one Python 3.15 build (owner, 19 November 2026, decision log entry 103; the authoritative runs are on the owner's 3.15.2 under Windows), and the install run-through", '8.3')
s = one(s, '87 Bash deny patterns at this edition.', '84 Bash deny patterns, and three allow lines, at this edition (editions to v6 said 87).', '8.6')
row = line_starting(s, '- **Test what binds one record to another.**', '8.8 last')
s = one(s, row, row + frag('frag_8_8_add.md'), '8.8 lessons')
s = one(s, 'written only after the takeover is accepted and on the owner\'s go;',
        'on the owner\'s go (the takeover of 19 November 2026 was accepted, decision log entry 102; H-1 v7 is not a prerequisite);', '10 item 2')
s = one(s, 'no commit by Claude outside `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`.',
        'no commit by Claude outside `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`, except reviewed and ratified documents into `doc/` (section 1.6).', '11')

# --- section 12
s = one(s, 'At this edition the newest is EX_243 (Claude: the owner\'s decisions on production deployment, for the reviewer\'s record).',
        'At this edition the newest is EX_246 (Claude: the blind answers of the takeover of 19 November 2026); EX_244 (the reviewer: restore and replay) governs the deployment work.', 'EX numbering')
s = one(s, 'run the suite on both Pythons, the mutation checks', 'run the suite on the Python 3.15 build (decision log entry 103), the mutation checks', '12.1 code round')
s = one(s, 'on the system Python 3.13 and on a Python 3.15 venv with the project\'s dependencies.',
        'on one Python 3.15 venv with the project\'s dependencies (owner, 19 November 2026, decision log entry 103: the routine 3.13 runs ended).', '12.3 suite')
s = one(s, '(about 25 minutes per Python)', '(about 25 minutes)', '12.3 time')
s = one(s, '- **Before sending:** both Pythons pass,', '- **Before sending:** the suite passes on the 3.15 build,', '12.3 before sending')
s = one(s, 'on both Pythons, and check the count', 'on the Python 3.15 build (decision log entry 103), and check the count', '12.9')
s = one(s, 'The second interpreter: `uv python install 3.15`',
        'The interpreter (Python 3.15 only, decision log entry 103; use the newest 3.15 build `uv` offers, and run the suite and the tools with it rather than the system `python3`): `uv python install 3.15`', '12.10 interpreter')
s = one(s, 'A full suite takes about twenty minutes on each interpreter;', 'A full suite takes about twenty minutes;', '12.10 time')
s = part(s, '### 12.8 Open items at this edition (18 November 2026)', '- **In the bullets below, carried from v3,', frag('frag_12_8.md'), '12.8 head')
owner_wants = line_starting(V6_1211, '- **What the owner wants, in his terms:**', 'owner wants')
to_check = line_starting(V6_1211, '- **To check on the owner\'s PC, not assume:**', 'to check')
new_1211 = frag('frag_12_11.md')
new_1211 = one(new_1211, '@@OWNER_WANTS@@\n', owner_wants, 'owner wants slot')
new_1211 = one(new_1211, '@@TO_CHECK@@\n', to_check, 'to check slot')
s = part(s, '### 12.11 The production deployment work (new in v6)', '\n---\n\n## Appendix A', new_1211, '12.11')

# --- Appendix A
s = one(s, '; its blurb `bc46c07a1705aa49738ba6b8d8797f46df40cbc7996e4ba22a25eaefdab73240` |',
        '; its blurb (now in `doc/HANDOVER/superseded/`) `bc46c07a1705aa49738ba6b8d8797f46df40cbc7996e4ba22a25eaefdab73240` |', 'v1r7 blurb')
s = one(s, '; its blurb `17633e4ec5413d12ed3c2909819b9f899a156af22631a31ee3e1b6f145ea0d2a` |',
        '; its blurb (now in `doc/HANDOVER/superseded/`) `17633e4ec5413d12ed3c2909819b9f899a156af22631a31ee3e1b6f145ea0d2a` |', 'H2 v1r8 blurb')
s = one(s, '(`138e185`, 87 Bash deny patterns)', '(`138e185`, 84 Bash deny patterns and 3 allow lines)', 'settings row')
assert sha('.claude/settings.json') == '9c345a3ef3c970323967dbd8abe5edcf02ce5acc0312f23c8b7710d9554821b6'
old_row = line_starting(s, '| MHUP-B staged code (not installed; all three slices passed) |', 'staged code row')
rows = (old_row +
    '| H-1 v6 (predecessor; OWNER-RATIFIED 19 November 2026, RAT-38, byte for byte; its header reads CANDIDATE) | `doc/HANDOVER/Claude_Primary_Handover_H1_v6.md`, `%s`; its blurb `%s` |\n' % (V6, V6B) +
    '| H-2 v3r4 (the operative reviewer handover; RAT-36) | `%s`, `%s` |\n' % (H2R4, sha(H2R4)) +
    '| H-2 v3r6 (the reviewer\'s CANDIDATE, not ratified; supersedes the v3r5 candidate) | `%s`, `%s` |\n' % (H2R6, sha(H2R6)) +
    '| The restore and replay clarification (governs; decision log entry 101) | `exchange/EX_244_ChatGPT.md`, `%s` |\n' % sha('exchange/EX_244_ChatGPT.md') +
    '| The takeover of 19 November 2026 (decision log entries 100 to 102; as stored, CRLF) | `exchange/EX_245_Claude.md`, `%s`; `exchange/EX_246_Claude.md`, `%s` |\n' % (sha('exchange/EX_245_Claude.md'), sha('exchange/EX_246_Claude.md')))
s = one(s, old_row, rows, 'app A rows')
s = part(s, '## Appendix B. Changes in v6', '*End of H-1.*', frag('frag_appB.md'), 'appendix B')

assert section(s, '### 2A. ', '## 3. Project in one paragraph') == S2A, 'section 2A changed'
assert '\r' not in s and s.endswith('\n') and not s.endswith('\n\n')
for k in ('## 0B. ', '## Appendix B. Changes in v7\n', '### 12.10 ', '### 12.11 ', '**12. Where production runs', '**13. Since H-1 v6 was written'):
    assert s.count(k) == 1, k
assert 'Python 3.13 and on a' not in s and 'both Pythons pass' not in s
s.encode('ascii')

# --- the blurb, by counted edits from v6's
b = one(b, '- goes with H-1 v6\n', '- goes with H-1 v7\n', 'blurb title')
b = one(b, 'Written by Claude late on 18 November 2026 with H-1 v6, a full new edition written at the owner\'s instruction after he\ndecided how production is to be deployed and run (its status, candidate or ratified, is in H-1 v6\'s own header and in\n`exchange/CONTINUITY_NOW.md`).',
        'Written by Claude on 19 November 2026 with H-1 v7, a full new edition written at the owner\'s go after the takeover of that\nday and his decisions on restore and testing (its status, candidate or ratified, is in H-1 v7\'s own header and in\n`exchange/CONTINUITY_NOW.md`).', 'blurb written-by')
b = one(b, '(Claude\'s recommendation, 18 November 2026)', '(Claude\'s recommendation, 19 November 2026)', 'blurb model date')
b = one(b, '- the handover **H-1 v6** (`exchange/CLAUDE_WEB_TOOLS/h1v6/out/Claude_Primary_Handover_H1_v6_CANDIDATE.md` while it is a\n  candidate; `doc/HANDOVER/Claude_Primary_Handover_H1_v6.md` once ratified; H-1 v5 in `doc/HANDOVER/` is the installed\n  edition until then), one complete file: **read its section 0B first** (item 12 above all),',
        '- the handover **H-1 v7** (`exchange/CLAUDE_WEB_TOOLS/h1v7/out/Claude_Primary_Handover_H1_v7_CANDIDATE.md` while it is a\n  candidate; `doc/HANDOVER/Claude_Primary_Handover_H1_v7.md` once ratified; H-1 v6 in `doc/HANDOVER/` is the installed\n  edition until then), one complete file: **read its section 0B first** (items 12 and 13 above all),', 'blurb handover')
b = one(b, '(`mhupb/slice1/`, `mhupb/slice2/` and their READMEs)', '(`mhupb/slice1/`, `mhupb/slice2/`, `mhupb/slice3/` and their READMEs)', 'blurb slices')
b = one(b, 'then H-1 v6 in full, section 0B first.', 'then H-1 v7 in full, section 0B first.', 'blurb read v7')
b = one(b, '(**entries 92 to 98 are the owner\'s decisions on production deployment**); `exchange/EX_243_Claude.md` and any reply to\n   it;',
        '(**entries 92 to 98 are the owner\'s decisions on production deployment; 99 to 105 the later ones**);\n   `exchange/EX_243_Claude.md` and `exchange/EX_244_ChatGPT.md` (EX_244 governs restore and replay); `exchange/EX_245_Claude.md`\n   and `EX_246_Claude.md` (the last takeover);', 'blurb log')
b = one(b, '**Where things stood late on 18 November 2026 (H-1 v6 section 0B has the detail; CONTINUITY_NOW.md is newer).**',
        '**Where things stood on 19 November 2026 (H-1 v7 section 0B has the detail; CONTINUITY_NOW.md is newer).**', 'blurb where')
b = one(b, '  ruled out installing now and changing later.** None of it is designed yet.\n',
        '  ruled out installing now and changing later.** None of it is designed yet.\n'
        '- **Restore and replay (EX_244; the owner, 19 November 2026).** A restore renames the old production tree aside (kept) and\n'
        '  unpacks a verified snapshot into a fresh, empty tree at the standard path. Replaying the N-1 walk-forward afterwards,\n'
        '  with OV-1\'s numbers recomputed, is valid research: no research STOP, timestamp proof or special recovery procedure.\n'
        '  Only the formal registered OV-1 claim keeps its own assumptions. No monthly restore test; no comparison of a replay\n'
        '  with the originals.\n'
        '- **Testing: Python 3.15 only** (the owner, 19 November 2026): one 3.15 build in the cloud; the authoritative runs are on\n'
        '  the owner\'s 3.15.2 under Windows, through Claude Code and T017.\n', 'blurb restore')
b = one(b, 'Since 18 November 2026: <"see exchange/CONTINUITY_NOW.md", plus anything newer>.',
        'Since 19 November 2026: <"see exchange/CONTINUITY_NOW.md", plus anything newer>.', 'blurb since')
assert '\r' not in b and b.endswith('\n')
b.encode('ascii')

os.makedirs(OUT, exist_ok=True)
for name, text in (('Claude_Primary_Handover_H1_v7_CANDIDATE.md', s), ('Claude_Primary_Handover_H1_v7_CANDIDATE_introductory_blurb.md', b)):
    data = text.encode('ascii'); open(os.path.join(OUT, name), 'wb').write(data)
    print(name, len(data), hashlib.sha256(data).hexdigest())
