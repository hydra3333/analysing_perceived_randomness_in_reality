"""Workspace helper (not project code): build H-1 v15 and its introductory blurb from the installed H-1 v14's Git
bytes. Usage: python make_h1_v15.py candidate   (writes out/..._CANDIDATE files)
              python make_h1_v15.py final <RAT>  (writes out/..._FINAL files, for doc/HANDOVER/, naming the RAT)
The texts written afresh are in h1_v15_texts.py beside this file. It edits no existing file."""
import hashlib, re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; REPO = HERE.parents[2]; OUT = HERE / 'out'
sys.path.insert(0, str(HERE)); import h1_v15_texts as T
def git(*a): return subprocess.run(['git', *a], capture_output=True, cwd=REPO, check=True).stdout
head = git('rev-parse', 'HEAD').decode().strip()
V14 = 'doc/HANDOVER/Claude_Primary_Handover_H1_v14.md'
V14_SHA = '24cc0579fec0f1b025216d969451457e378d1987eef96bf31f9a3bb924b5a6ac'
old = git('show', f'HEAD:{V14}'); assert hashlib.sha256(old).hexdigest() == V14_SHA
def now_sha(path):
    try:
        return hashlib.sha256(git('show', f'HEAD:{path}')).hexdigest()
    except subprocess.CalledProcessError:
        return None
def crlf(text): assert text.isascii() and '\r' not in text, [l for l in text.splitlines() if not l.isascii()][:3]; return text.replace('\n', '\r\n').encode('ascii')
def cut(a, b):
    assert old.count(a) == 1 and (b is None or old.count(b) == 1), (a, b)
    return old[old.index(a):(old.index(b) if b else len(old))]
rest = cut(b'## 0A. Things that trip', None)
END = b'\r\nEnd of H-1 v14.\r\n'; assert rest.endswith(END)
before_hist, hist = rest[:rest.index(b'# HISTORY (not live)')], rest[rest.index(b'# HISTORY (not live)'):-len(END)]
protected = cut(b'## 1. Roles and workflow', b'## 3. Project in one paragraph')
made = []
def fix(block, where, old_text, new_text, what):
    o, n = crlf(old_text), crlf(new_text)
    assert block.count(o) == 1, (where, old_text[:60], block.count(o))
    made.append(f'- **{where}:** {what}')
    return block.replace(o, n)

def hash_rows(block):
    """Every table row of a block that names a path and a SHA-256, as (path, sha)."""
    return re.findall(r'\| `([^`]+)` \| `([0-9a-f]{64})`', block.decode('ascii'))

def standing(block):
    """Which of a block's hashes equal today's bytes, and which do not (with the reason)."""
    rows = hash_rows(block)
    same = [p for p, h in rows if now_sha(p) == h]
    differ = [(p, 'not on main now' if now_sha(p) is None else 'an older identity') for p, h in rows if now_sha(p) != h]
    return rows, same, differ

b = before_hist
b = fix(b, 'Section 0C, its opening', '''They are H-1 v7r1's text, byte for byte, because they hold the roles,''',
        '''They are H-1 v7r1's text ((v15) the reviewer's H14-C02: byte for byte H-1 v13's and v14's, and the same as
H-1 v7r1's only after line endings are normalised, v7r1 being LF and this file CRLF), because they hold the roles,''',
        'what "byte for byte" means for sections 1, 2 and 2A (H14-C02).')
sec4 = b[b.index(b'## 4. Governing documents'):b.index(b'## 5. Settled decisions')]
rows, same, differ = standing(sec4)
b = fix(b, 'Section 4, its opening', 'SHA-256 values are of the Git content (LF), computed by the builder from `HEAD`.',
        'SHA-256 values are of the Git content, computed by the builder from `HEAD` when each was written. (v15, the '
        f'reviewer\'s H14-C01: at this edition\'s baseline {len(same)} of the {len(rows)} hashes in this section equal '
        'the file\'s bytes on `main` today' + ('; ' + '; '.join(f'`{p}`: {why}' for p, why in differ) if differ else '')
        + '. An older identity identifies the bytes it was taken of, at its commit; chapter 0, section 0.1 step 1.)',
        f'which hashes of section 4 are today\'s bytes, computed ({len(same)} of {len(rows)}; H14-C01).')
appA = b[b.index(b'## Appendix A. Identities'):b.index(b'## Appendix B.')]
rows, same, differ = standing(appA)
b = fix(b, 'Appendix A, its opening', '''SHA-256 of the Git content at `HEAD` (LF unless noted), computed by the builder.''',
        f'''SHA-256 of the Git content at `HEAD` (LF unless noted), computed by the builder of the edition that wrote each row.
(v15, the reviewer's H14-C01 and its observation: at this edition's baseline {len(same)} of the {len(rows)} hashes in
this appendix equal the file's bytes on `main` today. The others are older identities, each of the bytes it was
taken of at its commit, and are not expected to equal today's: {', '.join(f'`{p}`' for p, _ in differ) or 'none'}.)''',
        f'which hashes of Appendix A are today\'s bytes, computed ({len(same)} of {len(rows)}; H14-C01 and the observation).')
b = fix(b, 'Section 9, OUTLANDISH_01', '''The owner's OUTLANDISH_01 method family is in this project's backlog,
"probably first" (owner, 14 November 2026), and comes in only by this route; its own runs are not evidence here.''',
        '''(v15) OUTLANDISH_01 is closed (owner, 25 November 2026;
entry 295): completed, null under the matching criteria investigated, and not integrated into this project. It is
not a method family to be built here and is no longer in the backlog; its own runs are not evidence here.''',
        'OUTLANDISH_01 closed (entry 295; the reviewer\'s cold read, section 5).')
b = fix(b, 'Section 10, item 6', "new methods and waves; OUTLANDISH_01's family; the housekeeping of section 12.8.",
        "new methods and waves; the housekeeping of section 12.8. (v15: OUTLANDISH_01 is closed, entry 295.)",
        'OUTLANDISH_01 taken out of the order of work.')
b = fix(b, 'Section 10, what is genuinely open', "the identities, form and order of OUTLANDISH_01's methods; each",
        "(v15: OUTLANDISH_01 is closed, entry 295, and its methods are no longer open); each",
        'OUTLANDISH_01 taken out of what is open.')
b = fix(b, 'Section 11', 'ending a project process; clearing or bypassing the orphan marker; flipping',
        'ending a project process; clearing or bypassing the orphan marker in place ((v15) the reviewer\'s H14-C03: the one '
        'ratified exception is the restore\'s, deployment design section 12, with all four of its conditions; it sets the '
        'marker aside as evidence; chapter 0, section 0.1); flipping',
        'the restore\'s one ratified exception named beside the orphan rule (H14-C03).')
b = fix(b, 'Appendix C, its first paragraph', '''**Carried byte for byte from H-1 v13** (the builder asserts each): sections 1, 2 and 2A (H-1 v7r1's text); and''',
        '''**Carried byte for byte from H-1 v13** (the builder asserts each): sections 1, 2 and 2A (H-1 v7r1's text; (v15)
the same as v7r1's only after line endings are normalised, H14-C02); and''', 'the same precision (H14-C02).')
assert b.count(protected) == 1, 'sections 1, 2 and 2A are carried byte for byte'
assert hist == old[old.index(b'# HISTORY (not live)'):-len(END)]

mode = sys.argv[1]
h2v9 = now_sha('doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v9_20261125.md')
header = T.HEADER.format(v14_sha=V14_SHA, head=head)
if mode == 'final':
    header = header.replace('''**This edition: v15, 25 November 2026 (Adelaide, UTC+10:30). A CANDIDATE for the owner's ratification** (decision
log entry 315). It goes into `doc/HANDOVER/` only once he has ratified it; the reviewer has not read it.''',
                            f'''**This edition: v15, 25 November 2026 (Adelaide, UTC+10:30). RATIFIED BY THE OWNER ({sys.argv[2]}).** The reviewer had not
read it when it was installed; its cold read is owed when the owner asks.''')
    assert 'RATIFIED BY THE OWNER' in header
appD = crlf(T.APPENDIX_D.format(made='\n'.join(made)))
text = crlf(header + T.CHAPTER0.format(h2v9_sha=h2v9)) + b + appD + hist + b'\r\nEnd of H-1 v15.\r\n'
assert text.count(protected) == 1 and b'\r\r' not in text and text.count(b'\n') == text.count(b'\r\n')
OUT.mkdir(exist_ok=True)
tag = 'CANDIDATE' if mode == 'candidate' else 'FINAL'
doc = OUT / f'Claude_Primary_Handover_H1_v15_{tag}.md'
doc.write_bytes(text)
sha = hashlib.sha256(text).hexdigest()
rat = 'a candidate, not yet ratified' if mode == 'candidate' else sys.argv[2]
blurb = crlf(T.BLURB.format(rat=rat, sha=sha))
(OUT / f'Claude_Primary_Handover_H1_v15_{tag}_introductory_blurb.md').write_bytes(blurb)
print(tag, sha, hashlib.sha256(blurb).hexdigest(), len(text.splitlines()), 'lines')
print('\n'.join(made))
