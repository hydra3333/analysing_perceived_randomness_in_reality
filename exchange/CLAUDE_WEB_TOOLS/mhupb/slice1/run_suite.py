"""Run the offline suite of a tree, one module per process (python -B -m unittest -v), without class T12Determinism
(E2R-T12 starts worker processes; that run context is asked separately). Cloud workspace tool.
Usage: python3 -I run_suite.py TREE OUT_DIR [JOBS] [module-substring ...]"""
import ast, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 2
only = sys.argv[4:]
mods = sorted('tests.' + p.stem for p in (tree / 'tests').glob('test_*.py'))
if only:
    mods = [m for m in mods if any(o in m for o in only)]
env = dict(os.environ); env['PYTHONPATH'] = os.pathsep.join(str(tree / d) for d in ('src', 'src/methods', 'tests'))
env['PYTHONDONTWRITEBYTECODE'] = '1'


def one(mod):
    args = [mod]
    if mod == 'tests.test_e2r_contract':
        t = ast.parse((tree / 'tests' / 'test_e2r_contract.py').read_text(encoding='utf-8'))
        args = [f'{mod}.{c.name}' for c in t.body if isinstance(c, ast.ClassDef) and c.name != 'T12Determinism'
                and any(isinstance(f, ast.FunctionDef) and f.name.startswith('test') for f in c.body)]
    t0 = time.time()
    r = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', *args], cwd=tree, env=env, capture_output=True, text=True)
    (out / (mod + '.log')).write_text(r.stdout + '\n--- stderr ---\n' + r.stderr, encoding='utf-8')
    m = re.search(r'^Ran (\d+) tests? in', r.stderr, re.M)
    bad = re.findall(r'^(FAIL|ERROR): (\S+) \(([^)]+)\)', r.stderr, re.M)
    return mod, int(m.group(1)) if m else -1, r.returncode, bad, len(re.findall(r'\.\.\. skipped', r.stderr)), time.time() - t0


with ThreadPoolExecutor(jobs) as ex:
    rows = list(ex.map(one, mods))
total = sum(max(r[1], 0) for r in rows)
failing = [r for r in rows if r[2] != 0 or r[1] < 0]
for mod, ran, rc, bad, skips, secs in rows:
    print(f'{ran:5d} {"ok  " if rc == 0 else "FAIL"} {skips:2d} skipped {secs:7.1f}s  {mod}')
    for kind, name, where in bad:
        print(f'        {kind}: {where}.{name}' if False else f'        {kind}: {name} ({where})')
print(f'python {sys.version.split()[0]}; modules {len(rows)}; tests run {total}; modules failing {len(failing)}; '
      f'failing tests {sum(len(r[3]) for r in rows)}')
