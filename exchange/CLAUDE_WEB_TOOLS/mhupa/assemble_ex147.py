"""Assemble EX_147 (Claude): MHUP-A review slice 2, candidate v1. Builds MHUPA_Slice2_Review_v1/ (overlay of every changed
or new file of the development tree against the base, the build and check tools, the Linux evidence), zips it, writes the
complete diff (base -> slice 2) and the slice 1 -> slice 2 diff, the EX markdown with its member table (CRLF, ASCII) and the
EX zip, and stages it all into the repository's exchange/.
Usage: python3 assemble_ex147.py SCRATCHPAD REPO   (after the suite logs and the mutation output exist)"""
import hashlib, re, shutil, subprocess, sys
from pathlib import Path

S, R = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
BASE, DEV, T = S / 'BASE', S / 'DEV', S / 'tools'
MZ = R / 'exchange/CLAUDE_WEB_TOOLS/doc11/make_zip.py'
NAME = 'MHUPA_Slice2_Review_v1'
X = S / 'ex147'
V1 = S / 'ex145' / 'zsrc' / 'MHUPA_Slice1_Review_v1r2' / 'overlay'     # EX_145's overlay (the reviewed slice 1 candidate v1r2)
ST, ZS = X / 'stage', X / 'zsrc'
for d in (ST, ZS):
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
pkg = ZS / NAME
DIFF_SUFFIXES = ('.py', '.sh', '.bat', '.md', '.txt', '.json')

# 1. the overlay: every file that differs from or is absent in the base tree; the one removed file is listed
changed = []
for p in sorted(DEV.rglob('*')):
    if not p.is_file() or '__pycache__' in p.parts:
        continue
    rel = p.relative_to(DEV)
    b = BASE / rel
    if not b.exists() or b.read_bytes() != p.read_bytes():
        changed.append(rel)
        dst = pkg / 'overlay' / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(p, dst)
removed = [p.relative_to(BASE) for p in BASE.rglob('*') if p.is_file() and '__pycache__' not in p.parts
           and not (DEV / p.relative_to(BASE)).exists()]
assert removed == [Path('src/results_master_v0_1.py')], removed
(pkg / 'REMOVED_FILES.txt').write_text('src/results_master_v0_1.py  (replaced by src/results_master_v0_2.py; design 7)\n', encoding='ascii')

# 2. the tools
(pkg / 'tools').mkdir()
for f in ('build_dev_slice1.sh', 'make_e1r3.py', 'apply_slice1.py', 'edit_tests_slice1.py', 'make_e1_r2_reference.py',
          'build_dev_slice2.sh', 'make_updater_v0_2.py', 'apply_slice2.py', 'edit_tests_slice2.py',
          'mhupa_slice1_mutations.py', 'mhupa_slice2_mutations.py'):
    shutil.copy(T / f, pkg / 'tools' / f)
for d in ('slice1_new', 'slice1_edited', 'slice2_new', 'slice2_edited'):
    shutil.copytree(T / d, pkg / 'tools' / d, ignore=shutil.ignore_patterns('__pycache__'))
shutil.copy(S / 'pkg_slice2' / 'RUN_MHUPA_SLICE2_SUITE.py', pkg / 'tools' / 'RUN_MHUPA_SLICE2_SUITE.py')
shutil.copy(S / 'MHUP_A_work_item_card_v1.md', pkg / 'MHUP_A_work_item_card_v5.md')

# 3. the evidence
(pkg / 'evidence').mkdir()
for src, dst in (('suite_slice2_py313.log', 'mhupa_slice2_suite_py313.txt'), ('suite_slice2_py315.log', 'mhupa_slice2_suite_py315.txt'),
                 ('mutations_slice2_py313.txt', 'mhupa_slice2_mutations_py313.txt')):
    text = (S / src).read_text(encoding='utf-8')
    assert text.isascii(), src
    text = text.replace(str(S), '<scratchpad>')
    (pkg / 'evidence' / dst).write_text(text, encoding='ascii')
    assert ('SUITE PASS' in text) or ('0 survived' in text), src

readme = f"""# {NAME} - MHUP-A review slice 2, candidate v1 (Claude, 5 November 2026)

A REVIEW package, not an install candidate: nothing here is to be installed. See EX_147 (EX_141-EX_146 are slice 1).

- `overlay/` - every file of the development tree that differs from or is absent in the base tree (`main` at 2061055):
  {len(changed)} files, at their repository paths (slice 1's reviewed files included, unchanged except the two test lines
  EX_147 section 1 names). `REMOVED_FILES.txt` lists the one file the tree removes.
- `tools/` - the scripts that build the development tree from the base by counted edits (slice 1 then slice 2), the
  updater v0.2 maker, the suite runner (expected counts) and both slices' mutation tools.
- `evidence/` - the Linux suite runs (Python 3.13 and 3.15.0b4, E2R-T12 included) and the slice 2 mutation output.
- `MHUP_A_work_item_card_v5.md` - the work-item card.

No file under source_data/, results/ or transitory_data/ is in this package or was read to make it.
"""
(pkg / 'README.md').write_text(readme, encoding='ascii')

# 3b. the reviewer's EX_146, unchanged (as received)
ex146 = Path('/mnt/user-data/attachments/05ef2f64-c028-5b8b-a9c5-1bd6b3c075ae/d00ee482-EX_146_ChatGPT.md').read_bytes()
assert ex146.isascii()
assert ex146 == (R / 'exchange' / 'EX_146_ChatGPT.md').read_bytes()
(ST / 'EX_146_ChatGPT.md').write_bytes(ex146)

# 4. the zip and its members
subprocess.run([sys.executable, '-I', str(MZ), str(pkg), str(ST / f'{NAME}.zip'), str(ST / f'{NAME}_zip_members.txt')], check=True)


def tree_diff(a_of, label, out_name, header):
    dd = X / out_name.replace('.', '_')
    shutil.rmtree(dd, ignore_errors=True)
    rels = [r for r in changed if r.suffix in DIFF_SUFFIXES or r.name == '.gitignore'] + removed
    for rel in rels:
        for side, src in (('a', a_of(rel)), ('b', DEV / rel)):
            if src is not None and src.exists():
                (dd / side / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, dd / side / rel)
    d = subprocess.run(['diff', '-ruN', '--binary', 'a', 'b'], cwd=dd, capture_output=True).stdout
    d = re.sub(rb'(\n(?:---|\+\+\+) [^\t\n]+)\t[^\n]*', rb'\1', b'\n' + d)[1:]
    assert d.isascii(), out_name
    (ST / out_name).write_bytes(header + d)


# 5. the complete diff: base -> slice 2
listed = '\n'.join(f'#   {r.as_posix()}' for r in changed if not (r.suffix in DIFF_SUFFIXES or r.name == '.gitignore'))
tree_diff(lambda rel: BASE / rel, 'base', 'mhupa_slice2_src_tests.diff',
          b'# MHUP-A review slice 2: the complete diff, base main@2061055 -> development tree (.py, .sh, .bat, .md, .txt, .json, .gitignore;\n'
          b'# .bat files are CRLF and shown with --binary). Added files outside this diff (in the overlay, digests in the members list):\n'
          + (listed.encode('ascii') + b'\n' if listed else b'#   (none)\n'))

# 5b. the diff from the reviewed slice 1 candidate (EX_145 v1r2) to this candidate: side a = base with v1r2's overlay on top
tree_diff(lambda rel: (V1 / rel) if (V1 / rel).exists() else (BASE / rel), 'v1r2', 'mhupa_slice1_to_slice2.diff',
          b'# MHUP-A review slice 2: the diff from the reviewed slice 1 candidate (EX_145, MHUPA_Slice1_Review_v1r2) to this candidate\n'
          b'# (what slice 2 adds or changes; .bat files are CRLF and shown with --binary).\n')

# 6. the EX markdown
body = (S / 'ex147_body.md').read_text(encoding='ascii')
mut_text = (S / 'mutations_slice2_py313.txt').read_text(encoding='ascii')
m = re.search(r'^(\d+) of (\d+) mutants caught; (\d+) equivalent.*; (\d+) survived', mut_text, re.M)
assert m and m.group(4) == '0', mut_text[-300:]
body = body.replace('@@MUT@@', f'{m.group(2)} planted defects, one per rule of the slice: **{m.group(1)} caught, {m.group(3)} equivalent '
                               f'(each with its printed reason), {m.group(4)} survived**, on Python 3.13')
ex = 'EX_147_Claude.md'
members = sorted(p.name for p in ST.iterdir() if p.is_file())
rows = []
for mem in members:
    b = (ST / mem).read_bytes()
    if not mem.endswith('.zip'):
        assert b.isascii(), mem
    rows.append(f'| `{mem}` | `{hashlib.sha256(b).hexdigest()}` | `{hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()}` |')
body = body.replace('@@CONTENTS@@', ', '.join([ex] + members))
table = '| File | SHA-256 as stored | SHA-256 after CRLF to LF |\n|---|---|---|\n' + '\n'.join(rows) + '\n'
txt = body.replace('@@TABLE@@', table).replace('\r\n', '\n')
assert txt.isascii() and '@@' not in txt
(ST / ex).write_bytes(txt.replace('\n', '\r\n').encode('ascii'))

# 7. stage into the repository: exchange/EX_147_Claude/ and exchange/EX_147_Claude.zip
dest = R / 'exchange' / 'EX_147_Claude'
shutil.rmtree(dest, ignore_errors=True)
shutil.copytree(ST, dest)
subprocess.run([sys.executable, '-I', str(MZ), str(dest), str(R / 'exchange' / 'EX_147_Claude.zip'),
                str(X / 'EX_147_members_unused.txt'), 'flat'], check=True)
print('staged', len(members) + 1, 'members into', dest, f'; overlay {len(changed)} files')
for mem in [ex] + members:
    print(f'{hashlib.sha256((dest / mem).read_bytes()).hexdigest()}  {mem}')
