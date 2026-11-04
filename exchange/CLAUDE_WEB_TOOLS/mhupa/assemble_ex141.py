"""Assemble EX_141 (Claude): MHUP-A review slice 1. Builds MHUPA_Slice1_Review_v1/ (overlay of every changed or new
file, the build and check tools, the Linux evidence), zips it, writes the complete src/tests diff, the EX markdown with
its member table (CRLF, ASCII) and the EX zip, and stages it all into the repository's exchange/.
Usage: python3 assemble_ex141.py SCRATCHPAD REPO   (after the suite logs and mutation outputs exist)"""
import hashlib, re, shutil, subprocess, sys
from pathlib import Path

S, R = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
BASE, DEV, T = S / 'BASE', S / 'DEV', S / 'tools'
MZ = R / 'exchange/CLAUDE_WEB_TOOLS/doc11/make_zip.py'
NAME = 'MHUPA_Slice1_Review_v1'
X = S / 'ex141'
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
shutil.copy(S / 'pkg_slice1' / 'RUN_MHUPA_SLICE1_SUITE.py', pkg / 'tools' / 'RUN_MHUPA_SLICE1_SUITE.py')
shutil.copy(S / 'MHUP_A_work_item_card_v1.md', pkg / 'MHUP_A_work_item_card_v2.md')

# 3. the evidence
(pkg / 'evidence').mkdir()
for src, dst in (('suite_slice1_py313.log', 'mhupa_slice1_suite_py313.txt'), ('suite_slice1_py315.log', 'mhupa_slice1_suite_py315.txt'),
                 ('mutations_slice1_py313.txt', 'mhupa_slice1_mutations_py313.txt'),
                 ('mutations_slice1_py315.txt', 'mhupa_slice1_mutations_py315.txt')):
    text = (S / src).read_text(encoding='utf-8')
    assert text.isascii(), src
    text = text.replace(str(S), '<scratchpad>')
    (pkg / 'evidence' / dst).write_text(text, encoding='ascii')
    assert ('SUITE PASS' in text) or ('0 survived' in text), src

readme = f"""# {NAME} - MHUP-A review slice 1 (Claude, 4 November 2026)

A REVIEW package, not an install candidate: nothing here is to be installed. See EX_141.

- `overlay/` - every file of the development tree that differs from or is absent in the base tree (`main` at 2061055):
  {len(changed)} files, at their repository paths.
- `tools/` - the scripts that build the development tree from the base by counted edits, the E_1 revision-2 reference
  maker, the slice's suite runner (expected counts) and the mutation tool.
- `evidence/` - the Linux suite runs (Python 3.13 and 3.15.0b4, E2R-T12 excluded) and the mutation outputs.
- `MHUP_A_work_item_card_v2.md` - the work-item card.

No file under source_data/, results/ or transitory_data/ is in this package or was read to make it.
"""
(pkg / 'README.md').write_text(readme, encoding='ascii')

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

# 6. the EX markdown
body = (S / 'ex141_body.md').read_text(encoding='ascii')
ex = 'EX_141_Claude.md'
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

# 7. stage into the repository: exchange/EX_141_Claude/ and exchange/EX_141_Claude.zip
dest = R / 'exchange' / 'EX_141_Claude'
shutil.rmtree(dest, ignore_errors=True)
shutil.copytree(ST, dest)
subprocess.run([sys.executable, '-I', str(MZ), str(dest), str(R / 'exchange' / 'EX_141_Claude.zip'),
                str(X / 'EX_141_members_unused.txt'), 'flat'], check=True)
print('staged', len(members) + 1, 'members into', dest)
for m in [ex] + members:
    print(f'{hashlib.sha256((dest / m).read_bytes()).hexdigest()}  {m}')
