"""Workspace helper (not project code): build H-1 v14, the consolidated edition, and its introductory blurb from the
installed H-1 v13's Git bytes. Usage: python make_h1_v14.py candidate   (writes out/..._CANDIDATE files)
The texts written afresh are in h1_v14_texts.py beside this file. It edits no existing file."""
import hashlib, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; REPO = HERE.parents[2]; OUT = HERE / 'out'
sys.path.insert(0, str(HERE)); import h1_v14_texts as T
def git(*a): return subprocess.run(['git', *a], capture_output=True, cwd=REPO, check=True).stdout
head = git('rev-parse', 'HEAD').decode().strip()
V13, V13B = 'doc/HANDOVER/Claude_Primary_Handover_H1_v13.md', 'doc/HANDOVER/Claude_Primary_Handover_H1_v13_introductory_blurb.md'
old = git('show', f'HEAD:{V13}'); assert hashlib.sha256(old).hexdigest() == '37aa0196e828ddf012c83d61c66c49f814892341ffe88d1dc976609da289bbae'
shaf = lambda p: hashlib.sha256(git('show', f'HEAD:{p}')).hexdigest()
def crlf(text): assert text.isascii() and '\r' not in text; return text.replace('\n', '\r\n').encode('ascii')
def cut(a, b):
    assert old.count(a) == 1 and (b is None or old.count(b) == 1), (a, b)
    return old[old.index(a):(old.index(b) if b else len(old))]
s0A, hist, s0C = cut(b'## 0A. Things that trip', b'## 0B. The state'), cut(b'## 0B. The state', b'## 0C. Sections 1, 2 and 2A'), cut(b'## 0C. Sections 1, 2 and 2A', b'## 1. Roles and workflow')
s1_2, rest = cut(b'## 1. Roles and workflow', b'## 3. Project in one paragraph'), cut(b'## 3. Project in one paragraph', None)
END = b'\r\nEnd of H-1 v13.\r\n'; assert rest.endswith(END); rest = rest[:-len(END)]
made = []
def fix(block, where, old_text, new_text, what):
    o, n = crlf(old_text), crlf(new_text)
    assert block.count(o) == 1, (where, old_text[:50], block.count(o))
    made.append(f'- **{where}:** {what}')
    return block.replace(o, n)
s0A = fix(s0A, 'Section 0A item 1', 'its trees, installs, backups and laboratory tools are **not coded**.',
          '(v14) of its trees, installs and backups, slice A of build step 3 is written and reviewed but not installed (chapter 0, section 0.5); the rest of build step 3 and the laboratory tools are **not coded**.',
          'what is coded of the new system (EX_317 H13-C04).')
s0A = fix(s0A, 'Section 0A item 3', '''Register v0.32 (section 4.4) is the newest edition; it records
   RAT-34's install to RAT-40 and its own ratification. For anything later the decision log is the record. Read the
   log for the last RAT number, the last entry number and the last EX number before using a new one. At this
   edition (v11): the last RAT is RAT-48 (this handover); the newest EX is EX_307 (the reviewer's focused PASS
   of this edition); the newest decision log entry is 244 (RAT-48).''',
          '''(v14) Register v0.33 (RAT-53) is the newest edition; for anything later
   (RAT-54 onward) the decision log is the record. Read the log for the last RAT number, the last entry number and
   the last EX number before using a new one (chapter 0, section 0.3).''', 'the newest register, and the numbers of v11 removed (entry 270 point f).')
s0C = fix(s0C, 'Section 0C item 1', '''   the same rights and independence.
2. **Section 1.1, the local runner.**''', '''   the same rights and independence. **(v14) That chat ended on 25 November 2026 at its maximum length, after EX_321
   (entry 282); the present one is started by the owner from H-2 v9 (chapter 0, section 0.3).**
2. **Section 1.1, the local runner.**''', 'the reviewer chats brought up to date.')
s0C = fix(s0C, 'Section 0C item 4', '''Register v0.32 is still the newest (RAT-41; section 4.4); the next
   edition is owed (section 12.8).''', '''(v14) Register v0.33 is the newest (RAT-53); its next
   edition is owed for RAT-54 onward (chapter 0, section 0.3).''', 'the newest register (entry 270 point f).')
rest = fix(rest, 'Section 3', "ratified; of it, only the method files' layout is built (build step 1).",
           "ratified; (v14) of it, the method files' layout (build step 1) and the research engine in DEV (build step 2) are installed, and build step 3 (the trees, the installs, the backups and the new updater) is being coded (chapter 0).",
           'what is built (entry 270 point c).')
rest = fix(rest, 'Section 4.4', '- **The reviewer\'s handover (H-2).** **Previously in force (RAT-41), now history: H-2 v4,',
           f'''- **(v14) In force now:** the reviewer's handover is H-2 v9, `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v9_20261125.md`
  (`{shaf('doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v9_20261125.md')}`; RAT-57; chapter 0, section 0.3), and the newest
  register is v0.33 (RAT-53). What this section says below about which edition is in force is history.
- **The reviewer's handover (H-2).** **Previously in force (RAT-41), now history: H-2 v4,''', 'the reviewer\'s handover and the register in force now.')
rest = fix(rest, 'Section 5.1, the two-site checker', '(decision TSC-1: it stays unchanged and is never used again; probe finding A5).',
           '(decision TSC-1: it stays unchanged and is never used again; probe finding A5). (v14, EX_317 O01: the conversion of 25 November 2026 changed its form and two of its lines and gave no permission to run it; it is retired machinery and is not maintained.)',
           'the checker is no longer byte for byte unchanged (EX_317 O01).')
rest = fix(rest, 'Section 5.1, `.gitattributes`', '`source_data/** -text`; never change it.',
           '`source_data/** -text`; never change it. (v14: since the conversion `.gitattributes` holds the file-form standard\'s three lines instead, `* -text` first; that Git converts nothing now holds for every file.)',
           'the three lines of the standard (entry 270 point e).')
rest = fix(rest, 'Section 5.3', 'No install or release records, and no Git, outside DEV.',
           'No install or release records, and no Git, outside DEV. (v14, EX_317 H13-C03: read this as no release registry and no Git there; `records\\INSTALLED_FILES.json` and `records\\INSTALL_LOG.jsonl` are required in every installed tree, deployment design section 2.)',
           'the records an installed tree does hold (EX_317 H13-C03).')
rest = fix(rest, 'Section 7.1', 'the package `src/research/`, 20 files;',
           'the package `src/research/`, 20 files when it was installed and (v14) 21 since the conversion added `windows_text.py`;', 'the engine is 21 files (EX_317 H13-C04).')
rest = fix(rest, 'Section 7.3', 'byte for byte, as `src/research/ov1_numeric.py` (a test asserts the',
           'byte for byte at its installation, as `src/research/ov1_numeric.py` ((v14) since the conversion that file is the same kernel with CRLF line endings, equal to the reviewed one once CRLF is read as LF; the install manifest pinned its hash and no test of the suite compares the two, where earlier editions said that a test asserts the',
           'the OV-1 kernel and the test that was said to assert it (entry 270 point h; EX_317 H13-C01).')
rest = fix(rest, 'Section 10', '## 10. Next work, in order (planned; the owner decides each step)\n',
           '## 10. Next work, in order (planned; the owner decides each step)\n\n**(v14) Chapter 0, section 0.4, is the present order and prevails. What follows was written for H-1 v9 to v13 and is\nkept for its detail of each step.**\n', 'a line that sends the reader to chapter 0.')
rest = fix(rest, 'Section 12.8', '### 12.8 Open items at this edition (v12: 25 November 2026; section 0E item 10 is the current list and prevails)\n',
           '### 12.8 Open items at this edition (v12: 25 November 2026; section 0E item 10 is the current list and prevails)\n\n**(v14) No longer so: chapter 0, section 0.4, is the present list and prevails. What follows is of the morning of\n25 November 2026 and earlier.**\n', 'a line that sends the reader to chapter 0.')
assert old.count(s1_2) == 1 and old.count(hist) == 1
# the manifest with the slice, and on main, counted from the files themselves
def manifest(data):
    counts, section = {}, None
    for line in data.decode('ascii').splitlines():
        line = line.strip()
        if line.startswith('['): section = line.strip('[]')
        elif line and not line.startswith(('#', ';')) and section:
            key = line.split('=')[1].strip() if section == 'files' else 'install_tool'
            counts[key] = counts.get(key, 0) + 1
    files = sum(v for k, v in counts.items() if k != 'install_tool')
    return f'{files} files in `[files]` (forecast {counts.get("forecast", 0)}, derived {counts.get("derived", 0)}, other {counts.get("other", 0)})' + (f' and {counts["install_tool"]} install-tool files' if 'install_tool' in counts else '')
OV = 'exchange/CLAUDE_WEB_TOOLS/step3/overlay/'
overlay = git('ls-files', OV).decode().split()
assert len(overlay) == 26 and sum(1 for f in overlay if (REPO / f[len(OV):]).is_file()) == 10
entry = max(int(line.split(b'.')[0][3:]) for line in git('show', 'HEAD:exchange/DECISIONS/DECISION_LOG.md').split(b'\n') if line.startswith(b'## ') and line[3:4].isdigit())
status = sys.argv[1]
STATUS = {'candidate': 'CANDIDATE: not reviewed, not ratified, not installed; written at the owner\'s request (decision log entry 284).'}[status]
fill = lambda text, **k: [text := text.replace('{' + key + '}', str(value)) for key, value in k.items()][-1]
header = fill(T.HEADER, STATUS=STATUS, HEAD=head, ENTRY=entry)
chapter = fill(T.CHAPTER_0, H2V9=shaf('doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v9_20261125.md'), OVERLAY=len(overlay),
               MANIFEST=manifest(git('show', f'HEAD:{OV}deploy/INFRA_MANIFEST.ini')), MANIFEST_MAIN=manifest(git('show', 'HEAD:deploy/INFRA_MANIFEST.ini')))
appendix = fill(T.APPENDIX_C, CORRECTIONS='\n'.join(made))
assert '{' not in header + chapter.replace('{', '', 0) or True
HISTORY = '''# HISTORY (not live): sections 0B, 0D and 0E of H-1 v13, byte for byte

**Nothing below this line says what is true now.** These are the three layers that H-1 v9 to v13 added one upon
another: the state at 24 November 2026 (0B), what followed that afternoon and evening (0D), and the night of 24 and
the morning of 25 November 2026 (0E). They are kept whole because they hold the detailed record of build step 2's
rehearsal and first fill, the file-form standard and the conversion of DEV, the probe TASK_T028 and slice A's
beginnings, and because other sections refer to their items by number. Where they say what is in force, what is
next or what waits, chapter 0 prevails.

'''
doc = crlf(header) + crlf(chapter) + s0A + s0C + s1_2 + rest + b'\r\n' + crlf(appendix) + crlf(HISTORY) + hist.rstrip(b'\r\n') + b'\r\n\r\nEnd of H-1 v14.\r\n'
assert doc.count(b'\n') == doc.count(b'\r\n') and s1_2 in doc and hist.rstrip(b'\r\n') in doc
for word in (b'{STATUS}', b'{HEAD}', b'{H2V9}', b'{MANIFEST', b'{OVERLAY}', b'{CORRECTIONS}', b'{ENTRY}'): assert word not in doc, word
name = 'Claude_Primary_Handover_H1_v14' + ('_CANDIDATE' if status == 'candidate' else '')
OUT.mkdir(exist_ok=True); (OUT / f'{name}.md').write_bytes(doc)
d = hashlib.sha256(doc).hexdigest()
# ---- the blurb: H-1 v13's, with its title, its second and third paragraphs replaced; the rest byte for byte
b13 = git('show', f'HEAD:{V13B}')
a, b = b13.index(b'The previous Claude chat left you a handover, H-1 v13'), b13.index(b'THEN give me your first substantive reply')
title = b'# Introductory blurb for H-1 v13:'; assert b13.count(title) == 1
final_path = 'doc/HANDOVER/Claude_Primary_Handover_H1_v14.md'
where = f'exchange/CLAUDE_WEB_TOOLS/h1v14/out/{name}.md' if status == 'candidate' else final_path
middle = f'''The previous Claude chat left you a handover, H-1 v14 ({'a candidate, not yet ratified by me' if status == 'candidate' else 'ratified by me'}; SHA-256
{d}). It is a consolidated edition: its chapter 0 is the whole
live position, and the layered sections of earlier editions are kept at its end as history. The project was
redesigned from the root in November 2026. The new design was ratified on 22 November 2026 (RAT-40). Build step 1
(the method files' new layout), the light tidy-up and build step 2 (the research engine, in DEV) are installed and
proved. A standard for the form of every file is in force (doc/FILE_FORM_STANDARD_v0_2.md, RAT-49): every text file
of the living project is CRLF, every .jsonl file is LF, and Git converts nothing. Build step 3 has my go for its
design and cloud coding only. Its slice A (foundations) is written and has passed independent review (EX_321); it
lies as working files under exchange/CLAUDE_WEB_TOOLS/step3/overlay/ and is not installed. Slice B (backups, the
recovery kit, restore) is next and needs my go. There is no QA and no PROD tree yet, and the old system's code is
still in src/ beside the new engine. The reviewer chat that reviewed slice A ended on 25 November 2026 at its
maximum length; its handover H-2 v9 was written by the previous Claude chat at my request, and a new reviewer chat
starts from it.

DO THIS FIRST, and nothing else: add the repository (you will need push access for documents and records), then read
{where} and follow its chapter 0, section 0.1 (its reading order and the staged takeover).
Verify what you read against the repository; do not take summaries on trust.
'''
blurb = b13[:a].replace(title, b'# Introductory blurb for H-1 v14:') + crlf(middle) + b13[b:]
assert blurb.count(b'\n') == blurb.count(b'\r\n')
(OUT / f'{name}_introductory_blurb.md').write_bytes(blurb)
print(name, d, len(doc), 'bytes;', doc.count(b'\r\n'), 'lines; v13 had', old.count(b'\r\n'))
print('blurb', hashlib.sha256(blurb).hexdigest(), len(blurb), 'bytes;', len(made), 'corrections in place; entry', entry, 'head', head[:7])
