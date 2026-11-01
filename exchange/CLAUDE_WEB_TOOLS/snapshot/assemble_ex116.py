"""Assemble EX_116 (Claude): the package zip, its member list, the EX md with its member table and EX_116_Claude.zip,
all under /home/claude/work/snap/final/ex116/. Nothing is copied into the repository unless --to-exchange is given.
Usage: python3 assemble_ex116.py [--to-exchange]"""
import hashlib, re, shutil, subprocess, sys
from pathlib import Path

H = Path('/home/claude/work/snap/final')
R = Path('/home/claude/analysing_perceived_randomness_in_reality')
MZ = R / 'exchange/EX_019_Claude/make_zip.py'
X = H / 'ex116'
ST, ZS = X / 'stage', X / 'zsrc'
for d in (ST, ZS):
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
assert not list((H / 'pkg').rglob('__pycache__'))
shutil.copytree(H / 'pkg', ZS / 'DOC10_Snapshot_v1')


def sha(b): return hashlib.sha256(b).hexdigest()


def lfsha(b): return sha(b.replace(b'\r\n', b'\n'))


subprocess.run([sys.executable, '-I', str(MZ), str(ZS / 'DOC10_Snapshot_v1'), str(ST / 'DOC10_Snapshot_v1_candidate.zip'),
                str(ST / 'DOC10_Snapshot_v1_zip_members.txt')], check=True)
shutil.copy(H / 'e2e_doc10.txt', ST / 'e2e_doc10.txt')
shutil.copy(H / 'suite_doc10_py313.txt', ST / 'suite_doc10_py313.txt')
shutil.copy('/home/claude/work/snapshot/probe_findings.md', ST / 'cold_read_probe_findings.md')
shutil.copy(H / 'cold_read_h1_gaps.md', ST / 'cold_read_h1_gaps.md')
e2e = (H / 'e2e_doc10.txt').read_text()
assert e2e.count('COMMITTED PASS') == 2 and e2e.count('VERIFICATION STOP') >= 7 and e2e.rstrip().endswith('end'), 'rehearsal evidence incomplete'
suite = (H / 'suite_doc10_py313.txt').read_text()
m = re.search(r'SUITE PASS: all (\d+) tests ran and passed', suite)
assert m and m.group(1) == '471', 'suite evidence incomplete'
man = (H / 'pkg/repo_overlay/review/DOC10_Snapshot_v1/INSTALL_MANIFEST_SHA256.txt').read_text()
nnew = sum(1 for ln in man.splitlines() if ln.startswith('A ')) + 1          # + the manifest itself
nmod = sum(1 for ln in man.splitlines() if ln.startswith('M '))
t = (H / 'ex116.in').read_text()
OV = H / 'pkg/repo_overlay'
for ph, rel in (('@@H_REG@@', 'doc/RATIFICATION_REGISTER_v0_23.md'), ('@@H_H1@@', 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r7.md'),
                ('@@H_HX@@', 'doc/HOLDOUT_EXPOSURE_RECORD_v0_3.md'), ('@@H_H2@@', 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8.md'),
                ('@@H_ARCH@@', 'doc/Predictive_Randomness_Software_Architecture_Discussion_v0_9.md'),
                ('@@H_README@@', 'README.md'), ('@@H_RULE@@', 'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md'), ('@@H_GA@@', '.gitattributes')):
    t = t.replace(ph, lfsha((OV / rel).read_bytes()))
t = (t.replace('@@NNEW@@', str(nnew)).replace('@@NMOD@@', str(nmod))
      .replace('@@SUITE@@', 'SUITE PASS, all 471 tests (Python 3.13, an LF clone of `608025c` with the overlay copied in, '
               'run with PERF-1\'s runner)'))
rows = []
for f in sorted(p for p in ST.iterdir() if p.name != 'EX_116_Claude.md'):
    b = f.read_bytes()
    rows.append(f'| `{f.name}` | `{sha(b)}` | `{lfsha(b)}` |')
t = t.replace('@@MEMBERS@@', '\n'.join(rows))
assert '@@' not in t and all(ord(c) < 128 for c in t)
(ST / 'EX_116_Claude.md').write_bytes(t.replace('\n', '\r\n').encode('ascii'))
subprocess.run([sys.executable, '-I', str(MZ), str(ST), str(X / 'EX_116_Claude.zip'), str(X / 'members.txt'), 'flat'],
               check=True)
if '--to-exchange' in sys.argv[1:]:
    out = R / 'exchange/EX_116_Claude'
    shutil.rmtree(out, ignore_errors=True); out.mkdir()
    for f in ST.iterdir():
        shutil.copy(f, out / f.name)
    shutil.copy(X / 'EX_116_Claude.zip', R / 'exchange/EX_116_Claude.zip')
print('package zip', sha((ST / 'DOC10_Snapshot_v1_candidate.zip').read_bytes()))
print('EX zip', sha((X / 'EX_116_Claude.zip').read_bytes()))
