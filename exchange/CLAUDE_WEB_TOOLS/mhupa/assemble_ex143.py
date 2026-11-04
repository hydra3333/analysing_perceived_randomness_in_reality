"""Assemble EX_143 (Claude): MHUP-A review slice 1, revision r1 after EX_142 (B01-B03, C01-C03). Builds MHUPA_Slice1_Review_v1/ (overlay of every changed or new
file, the build and check tools, the Linux evidence), zips it, writes the complete src/tests diff, the EX markdown with
its member table (CRLF, ASCII) and the EX zip, and stages it all into the repository's exchange/.
Usage: python3 assemble_ex141.py SCRATCHPAD REPO   (after the suite logs and mutation outputs exist)"""
import hashlib, re, shutil, subprocess, sys
from pathlib import Path

S, R = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
BASE, DEV, T = S / 'BASE', S / 'DEV', S / 'tools'
MZ = R / 'exchange/CLAUDE_WEB_TOOLS/doc11/make_zip.py'
NAME = 'MHUPA_Slice1_Review_v1r1'
X = S / 'ex143'
V1 = S / 'ex141_overlay' / 'MHUPA_Slice1_Review_v1' / 'overlay'      # EX_141's overlay, unzipped from the committed zip
ST, ZS = X / 'stage', X / 'zsrc'
for d in (ST, ZS):
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
pkg = ZS / NAME

# 1. the overlay: every file that differs from or is absent in the base tree
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
assert not removed, removed

# 2. the tools
(pkg / 'tools').mkdir()
for f in ('build_dev_slice1.sh', 'make_e1r3.py', 'apply_slice1.py', 'edit_tests_slice1.py', 'make_e1_r2_reference.py',
          'mhupa_slice1_mutations.py', 'run_e2r_suite_without_t12.py'):
    shutil.copy(T / f, pkg / 'tools' / f)
shutil.copytree(T / 'slice1_new', pkg / 'tools' / 'slice1_new', ignore=shutil.ignore_patterns('__pycache__'))
shutil.copytree(T / 'slice1_edited', pkg / 'tools' / 'slice1_edited', ignore=shutil.ignore_patterns('__pycache__'))
shutil.copy(S / 'pkg_slice1' / 'RUN_MHUPA_SLICE1_SUITE.py', pkg / 'tools' / 'RUN_MHUPA_SLICE1_SUITE.py')
shutil.copy(S / 'MHUP_A_work_item_card_v1.md', pkg / 'MHUP_A_work_item_card_v3.md')

# 3. the evidence
(pkg / 'evidence').mkdir()
for src, dst in (('suite_slice1r1_py313.log', 'mhupa_slice1r1_suite_py313.txt'), ('suite_slice1r1_py315.log', 'mhupa_slice1r1_suite_py315.txt'),
                 ('mutations_slice1r1_py313.txt', 'mhupa_slice1r1_mutations_py313.txt'),
                 ('mutations_slice1r1_py315.txt', 'mhupa_slice1r1_mutations_py315.txt')):
    text = (S / src).read_text(encoding='utf-8')
    assert text.isascii(), src
    text = text.replace(str(S), '<scratchpad>')
    (pkg / 'evidence' / dst).write_text(text, encoding='ascii')
    assert ('SUITE PASS' in text) or ('0 survived' in text), src

readme = f"""# {NAME} - MHUP-A review slice 1, revision r1 after EX_142 (Claude, 4 November 2026)

A REVIEW package, not an install candidate: nothing here is to be installed. See EX_143 (and EX_141, the first candidate; EX_142, its review).

- `overlay/` - every file of the development tree that differs from or is absent in the base tree (`main` at 2061055):
  {len(changed)} files, at their repository paths.
- `tools/` - the scripts that build the development tree from the base by counted edits, the E_1 revision-2 reference
  maker, the slice's suite runner (expected counts) and the mutation tool.
- `evidence/` - the Linux suite runs (Python 3.13 and 3.15.0b4, E2R-T12 excluded) and the mutation outputs.
- `MHUP_A_work_item_card_v3.md` - the work-item card.

No file under source_data/, results/ or transitory_data/ is in this package or was read to make it.
"""
(pkg / 'README.md').write_text(readme, encoding='ascii')

# 3b. the reviewer's EX_142, unchanged (ASCII, CRLF as received)
ex142 = Path('/mnt/user-data/attachments/05ef2f64-c028-5b8b-a9c5-1bd6b3c075ae/ed4ff621-EX_142_ChatGPT.md').read_bytes()
assert hashlib.sha256(ex142).hexdigest() == '3cb225bf9c307eb3c081916819f1c19db4d48d21b777a187085bccc15e2c4cdc' and ex142.isascii()
(ST / 'EX_142_ChatGPT.md').write_bytes(ex142)

# 4. the zip and its members
subprocess.run([sys.executable, '-I', str(MZ), str(pkg), str(ST / f'{NAME}.zip'), str(ST / f'{NAME}_zip_members.txt')], check=True)

# 5. the complete src/tests diff
dd = X / 'dd'
shutil.rmtree(dd, ignore_errors=True)
for side, tree in (('a', BASE), ('b', DEV)):
    for rel in changed:
        if rel.parts[0] in ('src', 'tests') and rel.suffix in ('.py', '.sh', '.bat', '.md', '.txt'):
            for t, s in ((side, tree),):
                src = s / rel
                if src.exists():
                    (dd / t / rel).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(src, dd / t / rel)
d = subprocess.run(['diff', '-ruN', 'a', 'b'], cwd=dd, capture_output=True).stdout
d = re.sub(rb'(\n(?:---|\+\+\+) [^\t\n]+)\t[^\n]*', rb'\1', b'\n' + d)[1:]
listed = '\n'.join(f'#   {r.as_posix()}' for r in changed if not (r.parts[0] in ('src', 'tests') and r.suffix in ('.py',)))
head = (b'# MHUP-A review slice 1: the complete diff of src/ and tests/ (.py), base main@2061055 -> development tree.\n'
        b'# Added files outside this diff (in the overlay, digests in the members list):\n' + listed.encode('ascii') + b'\n')
assert d.isascii()
(ST / 'mhupa_slice1_src_tests.diff').write_bytes(head + d)

# 5b. the diff from EX_141's candidate (v1) to this one (v1r1): side a is the base with v1's overlay on top
dd2 = X / 'dd2'
shutil.rmtree(dd2, ignore_errors=True)
for rel in changed:
    if not (rel.parts[0] in ('src', 'tests') and rel.suffix == '.py'):
        continue
    a_src = (V1 / rel) if (V1 / rel).exists() else (BASE / rel)
    for side, src in (('a', a_src), ('b', DEV / rel)):
        if src.exists():
            (dd2 / side / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dd2 / side / rel)
d2 = subprocess.run(['diff', '-ruN', 'a', 'b'], cwd=dd2, capture_output=True).stdout
d2 = re.sub(rb'(\n(?:---|\+\+\+) [^\t\n]+)\t[^\n]*', rb'\1', b'\n' + d2)[1:]
assert d2.isascii()
(ST / 'mhupa_slice1_v1_to_v1r1.diff').write_bytes(
    b'# MHUP-A review slice 1: the diff of src/ and tests/ (.py) from the EX_141 candidate (v1) to this candidate (v1r1).\n'
    b'# The two entry_0003.json files also changed (their registry_status_reason; digests in the members list).\n' + d2)

# 6. the EX markdown
body = (S / 'ex143_body.md').read_text(encoding='ascii')
ex = 'EX_143_Claude.md'
members = sorted(p.name for p in ST.iterdir() if p.is_file())
rows = []
for m in members:
    b = (ST / m).read_bytes()
    if not m.endswith('.zip'):
        assert b.isascii(), m
    rows.append(f'| `{m}` | `{hashlib.sha256(b).hexdigest()}` | `{hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()}` |')
body = body.replace('@@CONTENTS@@', ', '.join([ex] + members))
table = '| File | SHA-256 as stored | SHA-256 after CRLF to LF |\n|---|---|---|\n' + '\n'.join(rows) + '\n'
txt = body.replace('@@TABLE@@', table).replace('\r\n', '\n')
assert txt.isascii() and '@@' not in txt
(ST / ex).write_bytes(txt.replace('\n', '\r\n').encode('ascii'))

# 7. stage into the repository: exchange/EX_143_Claude/ and exchange/EX_143_Claude.zip
dest = R / 'exchange' / 'EX_143_Claude'
shutil.rmtree(dest, ignore_errors=True)
shutil.copytree(ST, dest)
subprocess.run([sys.executable, '-I', str(MZ), str(dest), str(R / 'exchange' / 'EX_143_Claude.zip'),
                str(X / 'EX_143_members_unused.txt'), 'flat'], check=True)
print('staged', len(members) + 1, 'members into', dest)
for m in [ex] + members:
    print(f'{hashlib.sha256((dest / m).read_bytes()).hexdigest()}  {m}')
