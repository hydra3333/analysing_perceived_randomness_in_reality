"""Assemble EX_112 (Claude): package zip, members, EX md with member table, EX zip; stage into the repo's exchange/.
Run after ev4_done.txt exists. Usage: python3 assemble_ex112.py"""
import hashlib, re, shutil, subprocess, sys
from pathlib import Path

H = Path('/home/claude/work/wf1bcode')
R = Path('/home/claude/analysing_perceived_randomness_in_reality')
MZ = R / 'exchange/EX_019_Claude/make_zip.py'
X = H / 'ex112'
ST = X / 'stage'
ZS = X / 'zsrc'
for d in (ST, ZS):
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
shutil.copytree(H / 'pkg', ZS / 'WF1B_Install_v3')


def sha(b): return hashlib.sha256(b).hexdigest()


def lfsha(b): return sha(b.replace(b'\r\n', b'\n'))


subprocess.run([sys.executable, '-I', str(MZ), str(ZS / 'WF1B_Install_v3'), str(ST / 'WF1B_Install_v3_candidate.zip'),
                str(ST / 'WF1B_Install_v3_zip_members.txt')], check=True)
shutil.copy(H / 'ev4_e2e_py313.txt', ST / 'e2e_wf1b_v3_py313.txt')
shutil.copy(H / 'ev4_e2e_py315.txt', ST / 'e2e_wf1b_v3_py315.txt')
for f in ('wf1b_v2_to_v3.diff', 'simulated_windows_probe.txt', 'runner_detail_probe.txt'):
    shutil.copy(X / f, ST / f)


def verdict(t):
    s = (H / t).read_text()
    ok = s.count('SUITE PASS') == 2 and s.count('COMMITTED PASS') == 2 and s.count('VERIFICATION STOP') == 6
    assert ok, t
    return 'LF and CRLF each PRE, POST, SUITE (464) and COMMITTED PASS'


mut = (H / 'ev/mutations_wf1b_v3_py313.txt').read_text().strip().splitlines()[-1]
assert mut == '23 of 23 mutants caught', mut
base = re.search(r"BASE = '([0-9a-f]{40})'", (H / 'pkg/VERIFY_WF1B_INSTALL.py').read_text()).group(1)
t = (H / 'ex112.in').read_text()
t = (t.replace('@@BASE@@', base[:7]).replace('@@MUT@@', '23 of 23 mutants caught')
      .replace('@@E313@@', verdict('ev4_e2e_py313.txt')).replace('@@E315@@', verdict('ev4_e2e_py315.txt')))
rows = []
for f in sorted(p for p in ST.iterdir() if p.name != 'EX_112_Claude.md'):
    b = f.read_bytes()
    rows.append(f'| `{f.name}` | `{sha(b)}` | `{lfsha(b)}` |')
t = t.replace('@@MEMBERS@@', '\n'.join(rows))
assert '@@' not in t and all(ord(c) < 128 for c in t)
(ST / 'EX_112_Claude.md').write_bytes(t.replace('\n', '\r\n').encode('ascii'))
subprocess.run([sys.executable, '-I', str(MZ), str(ST), str(X / 'EX_112_Claude.zip'), str(X / 'members.txt'), 'flat'],
               check=True)
out = R / 'exchange/EX_112_Claude'
shutil.rmtree(out, ignore_errors=True); out.mkdir()
for f in ST.iterdir():
    shutil.copy(f, out / f.name)
shutil.copy(X / 'EX_112_Claude.zip', R / 'exchange/EX_112_Claude.zip')
print('package zip', sha((ST / 'WF1B_Install_v3_candidate.zip').read_bytes()))
print('EX zip', sha((X / 'EX_112_Claude.zip').read_bytes()))
