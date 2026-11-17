"""Baseline run of the offline suite in a disposable clone (cloud workspace only), without E2R-T12.
Usage: python -I baseline_suite.py CLONE RUNNER_WITH_EXPECTED OUT_DIR
Each module runs in its own process (python -B -m unittest -v), as the package runners do. Nothing is fixed or skipped
except class T12Determinism (it starts worker processes; the owner's approval of that run context has not been asked)."""
import ast, os, re, subprocess, sys, time, json
from pathlib import Path
clone, runner, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
exp = {}
for n in ast.parse(runner.read_text(encoding='utf-8')).body:
    if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'EXPECTED':
        exp = dict(ast.literal_eval(n.value))
mods = sorted('tests.' + p.stem for p in (clone / 'tests').glob('test_*.py'))
env = dict(os.environ); env['PYTHONPATH'] = os.pathsep.join(str(clone / d) for d in ('src', 'src/methods', 'tests'))
env['PYTHONDONTWRITEBYTECODE'] = '1'
summary = []
for mod in mods:
    args = [mod]
    if mod == 'tests.test_e2r_contract':
        tree = ast.parse((clone / 'tests' / 'test_e2r_contract.py').read_text(encoding='utf-8'))
        args = [f'{mod}.{c.name}' for c in tree.body if isinstance(c, ast.ClassDef) and c.name != 'T12Determinism'
                and any(isinstance(f, ast.FunctionDef) and f.name.startswith('test') for f in c.body)]
    t = time.time()
    r = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', *args], cwd=clone, env=env, capture_output=True, text=True)
    secs = time.time() - t
    (out / (mod + '.log')).write_text(r.stdout + '\n--- stderr ---\n' + r.stderr, encoding='utf-8')
    err = r.stderr
    m = re.search(r'^Ran (\d+) tests? in', err, re.M); ran = int(m.group(1)) if m else -1
    last = err.strip().splitlines()[-1] if err.strip() else '(no output)'
    bad = re.findall(r'^(FAIL|ERROR): (\S+) \(([^)]+)\)', err, re.M)
    skips = len(re.findall(r'\.\.\. skipped', err))
    row = dict(module=mod, ran=ran, expected=exp.get(mod), exit=r.returncode, last=last, skipped=skips,
               bad=[f'{k} {c}.{n}' if False else f'{k}: {n} ({c})' for k, n, c in bad], secs=round(secs, 1))
    summary.append(row)
    print(f"{mod:<50} ran {ran:4d} exp {str(exp.get(mod)):>4} skip {skips} exit {r.returncode} {last} ({secs:.0f}s)", flush=True)
    for b in row['bad']: print('    ' + b, flush=True)
(out / 'summary.json').write_text(json.dumps(summary, indent=1), encoding='utf-8')
print('TOTAL ran', sum(max(r['ran'], 0) for r in summary), 'modules', len(summary), 'modules with failures', sum(1 for r in summary if r['exit']), flush=True)
print('BASELINE DONE', flush=True)
