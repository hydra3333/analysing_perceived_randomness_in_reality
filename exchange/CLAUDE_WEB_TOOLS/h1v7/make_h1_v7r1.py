"""Build H-1 v7r1 and its blurb (CANDIDATE; 19 November 2026): H-1 v7's candidate bytes with exactly the two corrections
the owner relayed from the reviewer (23:11), plus the identity lines an r1 needs.
Usage: python3 -I make_h1_v7r1.py REPO_ROOT OUT_DIR

Reads the v7 candidate and its blurb from REPO_ROOT/exchange/CLAUDE_WEB_TOOLS/h1v7/out/ (asserted by SHA-256), applies
counted edits (each old text must occur exactly once), asserts section 2A unchanged, writes the two files to OUT_DIR.
"""
import hashlib, os, sys
assert len(sys.argv) == 3, 'usage: make_h1_v7r1.py REPO_ROOT OUT_DIR'
REPO, OUT = sys.argv[1], sys.argv[2]
V7 = '300fbe80b49c84bb0a44c083dd666522991aa66d2be61cb61b84dae7281c3ea2'
V7B = '5deecde096cb023f3a91077ae9bdebd418fb0d2d0da27d1aa1cd1858778fb155'
D = 'exchange/CLAUDE_WEB_TOOLS/h1v7/out/'


def rd(path, want):
    b = open(os.path.join(REPO, path), 'rb').read()
    assert hashlib.sha256(b).hexdigest() == want, f'{path}: not the v7 candidate bytes'
    t = b.decode('ascii'); assert '\r' not in t
    return t
def one(s, old, new, label):
    n = s.count(old); assert n == 1, f'{label}: expected one occurrence, found {n}'
    return s.replace(old, new)
def section(s, start, end):
    return s[s.index(start):s.index(end)]


s = rd(D + 'Claude_Primary_Handover_H1_v7_CANDIDATE.md', V7)
b = rd(D + 'Claude_Primary_Handover_H1_v7_CANDIDATE_introductory_blurb.md', V7B)
S2A = section(s, '### 2A. ', '## 3. Project in one paragraph')

# --- identity of the revision
s = one(s, 'Predictive Randomness project, v7\n', 'Predictive Randomness project, v7r1\n', 'title')
s = one(s, '**Version:** v7, 19 November 2026, evening (Adelaide, UTC+10:30).',
        '**Version:** v7r1, 19 November 2026, late evening (Adelaide, UTC+10:30): v7 with two narrow corrections the reviewer asked for before ratification (Appendix B.4); nothing else changed. v7 was:', 'version')
s = one(s, '**Status:** CANDIDATE, written on 19 November 2026 at the owner\'s go (decision log entry 105).',
        '**Status:** CANDIDATE (v7r1), written on 19 November 2026 at the owner\'s go (decision log entry 105), corrected at 23:11 as the owner relayed from the reviewer.', 'status')
s = one(s, 'It then goes into `doc/HANDOVER/` as `Claude_Primary_Handover_H1_v7.md` with its blurb,',
        'It then goes into `doc/HANDOVER/` as `Claude_Primary_Handover_H1_v7r1.md` with its blurb,', 'B.2 install name')

# --- correction 1: section 0 steps 1 and 3 (the obsolete prohibition on reading source_data/ and records; RAT-34)
s = one(s, 'except the two master hashes in section 7.5 (never open `source_data/`) and the computed E_1 digests in section 7.3 (run outputs, not files).',
        'including the two master hashes in section 7.5 (since RAT-34 Claude may read `source_data/` and `results/`, never write there), except the computed E_1 digests in section 7.3 (run outputs, not files).', 'step 1')
s = one(s, 'which may tell you that an opening record or a Mode H record was committed; never open those files.',
        'which may tell you that an opening record or a Mode H record was committed; since RAT-34 Claude may also read those files (never write them; section 0B item 4).', 'step 3')

# --- correction 2: section 7.5 (the updater has run live)
s = one(s, '`update` has never run live and is not authorised; it is Approval 2 of each game (section 5.1).',
        '`update` ran live once per game, on each game\'s authorised Approval 2 (15 and 16 November 2026; both masters are at version 2, next bullet); every further run needs the owner\'s own go (section 5.1).', '7.5')

# --- Appendix B.4
s = one(s, '\n**Review:** a documentary look by the reviewer is welcome, not required; the owner ratifies.\n',
        '\n**Review:** a documentary look by the reviewer is welcome, not required; the owner ratifies.\n\n'
        '### B.4 r1 (19 November 2026, late evening)\n\n'
        'The reviewer examined v7, supported its content and ratification, and asked (relayed by the owner at 23:11) for two '
        'narrow corrections only, made by `exchange/CLAUDE_WEB_TOOLS/h1v7/make_h1_v7r1.py` from v7\'s candidate bytes '
        '(`300fbe80...1c3ea2`): (1) section 0, steps 1 and 3: the obsolete prohibition on reading `source_data/` and the '
        'committed records is removed, consistent with RAT-34; (2) section 7.5: the updater\'s `update` ran live once per game '
        '(15 and 16 November 2026), so "has never run live" is corrected. Besides those, only the identity lines changed (the '
        'title, the version and status lines, the installed file name in B.2, this section, and the blurb\'s file names). '
        'Section 12.3 still says "Claude never opens those folders itself", the same obsolete prohibition; it was not named in '
        'the request and is left for the next edition. Decisions 103 to 105 and all other v7 content are unchanged.\n', 'B.4')

assert section(s, '### 2A. ', '## 3. Project in one paragraph') == S2A, 'section 2A changed'
assert '\r' not in s and s.endswith('\n') and not s.endswith('\n\n')
s.encode('ascii')

# --- the blurb: file names only
b = one(b, '- goes with H-1 v7\n', '- goes with H-1 v7r1\n', 'blurb title')
b = one(b, '- the handover **H-1 v7** (`exchange/CLAUDE_WEB_TOOLS/h1v7/out/Claude_Primary_Handover_H1_v7_CANDIDATE.md` while it is a\n  candidate; `doc/HANDOVER/Claude_Primary_Handover_H1_v7.md` once ratified;',
        '- the handover **H-1 v7r1** (`exchange/CLAUDE_WEB_TOOLS/h1v7/out_r1/Claude_Primary_Handover_H1_v7r1_CANDIDATE.md` while it is a\n  candidate; `doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md` once ratified;', 'blurb paths')
b.encode('ascii'); assert '\r' not in b

os.makedirs(OUT, exist_ok=True)
for name, text in (('Claude_Primary_Handover_H1_v7r1_CANDIDATE.md', s), ('Claude_Primary_Handover_H1_v7r1_CANDIDATE_introductory_blurb.md', b)):
    data = text.encode('ascii'); open(os.path.join(OUT, name), 'wb').write(data)
    print(name, len(data), hashlib.sha256(data).hexdigest())
