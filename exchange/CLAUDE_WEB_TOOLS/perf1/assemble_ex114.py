"""Assemble EX_114 (Claude): package zip, members, source/test diff, EX md with member table, EX zip; stage into the
repo's exchange/. Run after ev_done.txt exists. Usage: python3 assemble_ex114.py"""
import hashlib, re, shutil, subprocess, sys
from pathlib import Path

H = Path('/home/claude/work/perf1code')
S = Path('/tmp/claude-0/-home-claude/5e241a26-14db-516d-9aeb-bda4dbe85524/scratchpad')
R = Path('/home/claude/analysing_perceived_randomness_in_reality')
MZ = R / 'exchange/EX_019_Claude/make_zip.py'
X = H / 'ex114'
ST, ZS = X / 'stage', X / 'zsrc'
for d in (ST, ZS):
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
assert not list((H / 'pkg').rglob('__pycache__'))
shutil.copytree(H / 'pkg', ZS / 'PERF1_Install_v1')


def sha(b): return hashlib.sha256(b).hexdigest()


def lfsha(b): return sha(b.replace(b'\r\n', b'\n'))


# the complete source/test diff, base tree -> dev tree
dd = S / 'dd'
shutil.rmtree(dd, ignore_errors=True)
for side, tree in (('a', S / 'perf1_base'), ('b', S / 'perf1_dev')):
    for rel in ('src/evaluation/numerics.py', 'src/evaluation/report.py', 'src/evaluation/Method_Rankings_Report.py',
                'tests/test_perf1_numerics.py'):
        src = tree / rel
        if src.exists():
            (dd / side / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dd / side / rel)
d = subprocess.run(['diff', '-ruN', 'a', 'b'], cwd=dd, capture_output=True).stdout
d = re.sub(rb'(\n(?:---|\+\+\+) [^\t\n]+)\t[^\n]*', rb'\1', b'\n' + d)[1:]          # drop timestamps
(ST / 'perf1_src_tests.diff').write_bytes(
    b'# PERF-1: the complete source and test diff, WF1B_Install_v3 (installed; base 209db44) to PERF1_Install_v1.\n' + d)

subprocess.run([sys.executable, '-I', str(MZ), str(ZS / 'PERF1_Install_v1'), str(ST / 'PERF1_Install_v1_candidate.zip'),
                str(ST / 'PERF1_Install_v1_zip_members.txt')], check=True)
shutil.copy(H / 'e2e_perf1_py313.txt', ST / 'e2e_perf1_v1_py313.txt')
shutil.copy(H / 'e2e_perf1_py315.txt', ST / 'e2e_perf1_v1_py315.txt')
shutil.copy(H / 'ev/perf1_timings.txt', ST / 'perf1_timings.txt')


def verdict(t):
    s = (H / t).read_text()
    ok = s.count('SUITE PASS') == 2 and s.count('COMMITTED PASS') == 2 and s.count('VERIFICATION STOP') == 7
    assert ok, t
    return 'LF and CRLF each PRE, POST, SUITE (471) and COMMITTED PASS'


mut = (H / 'ev/mutations_perf1_v1_py313.txt').read_text().strip().splitlines()[-1]
assert mut == '9 of 9 mutants caught', mut
tim = (H / 'ev/perf1_timings.txt').read_text()


def stage_line(header):
    block = tim.split(header, 1)[1].splitlines()
    m = re.search(r'N1 runner ([0-9.]+) s; measures ([0-9.]+) s', block[2])
    return f'{float(m.group(1)) + float(m.group(2)):.0f} s'


t = (H / 'ex114.in').read_text()
t = (t.replace('@@BASE@@', '209db44').replace('@@MUT@@', '9 of 9 mutants caught').replace('@@SUITE@@', '471')
      .replace('@@E313@@', verdict('e2e_perf1_py313.txt')).replace('@@E315@@', verdict('e2e_perf1_py315.txt'))
      .replace('@@T1000@@', stage_line('## After (PERF-1), Oz Lotto shape, R = 1,000'))
      .replace('@@T10000@@', stage_line('## After (PERF-1), Oz Lotto shape, R = 10,000'))
      .replace('@@TPB@@', stage_line('## After (PERF-1), Powerball shape, R = 10,000') + ' for the whole stage'))
rows = []
for f in sorted(p for p in ST.iterdir() if p.name != 'EX_114_Claude.md'):
    b = f.read_bytes()
    rows.append(f'| `{f.name}` | `{sha(b)}` | `{lfsha(b)}` |')
t = t.replace('@@MEMBERS@@', '\n'.join(rows))
assert '@@' not in t and all(ord(c) < 128 for c in t)
(ST / 'EX_114_Claude.md').write_bytes(t.replace('\n', '\r\n').encode('ascii'))
subprocess.run([sys.executable, '-I', str(MZ), str(ST), str(X / 'EX_114_Claude.zip'), str(X / 'members.txt'), 'flat'],
               check=True)
out = R / 'exchange/EX_114_Claude'
shutil.rmtree(out, ignore_errors=True); out.mkdir()
for f in ST.iterdir():
    shutil.copy(f, out / f.name)
shutil.copy(X / 'EX_114_Claude.zip', R / 'exchange/EX_114_Claude.zip')
print('package zip', sha((ST / 'PERF1_Install_v1_candidate.zip').read_bytes()))
print('EX zip', sha((X / 'EX_114_Claude.zip').read_bytes()))
