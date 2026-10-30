"""Mutation checks for the E_3/E_4 package (Claude-side evidence; disposable copies only).

Usage: python3 -I e34_mutations.py TREE
For each planted defect a temporary copy of src/ and tests/ is changed and the named test must FAIL; the
unchanged copy (control) must pass. The tree itself is never changed and no bytecode is written to it.
A `new` of None deletes the file.
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
H = 'src/methods/_common/polynomial_fits.py'
M3, M4 = 'src/methods/E_003/', 'src/methods/E_004/'
TH = 'tests.test_polynomial_fits.'
T = 'tests.test_e3_e4_polynomial.'
MUTANTS = [
    # the shared helper
    ('the target placed inside the window (t = -M+1..0)', H,
     "    return [Fraction(i - window) for i in range(window)]",
     "    return [Fraction(i - window + 1) for i in range(window)]", TH + 'WorkedExamples'),
    ('smoothing not clipped (always divides by 2H + 1)', H,
     "                     min(n, i + half_width + 1) - max(0, i - half_width)) for i in range(n)]",
     "                     2 * half_width + 1) for i in range(n)]", TH + 'WorkedExamples'),
    ('a wrong normal matrix', H,
     "    normal = [[sum(p[a + b] for p in powers)", "    normal = [[sum(p[a + b] + p[a] for p in powers)",
     TH + 'LeastSquares'),
    ('a wrong recurrence coefficient (beta inverted)', H,
     "            nxt = axpy(nxt, -(norm / norms[k - 1]), prev)", "            nxt = axpy(nxt, -(norms[k - 1] / norm), prev)",
     TH + 'LeastSquares'),
    ('Newton divided differences off by one level', H,
     "            dd[i] = (dd[i] - dd[i - 1]) / (ts[i] - ts[i - level])",
     "            dd[i] = (dd[i] - dd[i - 1]) / (ts[i] - ts[i - 1])", TH + 'Interpolation'),
    ('minimax stops before the levelled error is reached', H,
     "        if abs(errors[worst]) <= abs(h):", "        if abs(errors[worst]) <= 2 * abs(h):", TH + 'Minimax'),
    ('the exchange swaps the wrong neighbour', H,
     "            if s == sigma(k):\n                ref[k] = worst", "            if s != sigma(k):\n                ref[k] = worst",
     TH + 'Minimax'),
    ('the certificate accepts D + 1 alternations', H,
     "    if alternations < degree + 2:", "    if alternations < degree + 1:", TH + 'Minimax'),
    ('the largest error taken at its highest index (tie rule reversed)', H,
     "        worst = max(range(n), key=lambda i: (abs(errors[i]), -i))",
     "        worst = max(range(n), key=lambda i: (abs(errors[i]), i))", TH + 'Minimax'),
    ('the exchange cap ignored (returns the last fit)', H,
     "    raise RuntimeError('minimax exchange did not converge within the cap')",
     "    return coeffs, abs(h), ref", TH + 'Minimax'),
    ('floating point in the helper', H,
     "    value = Fraction(0)\n    for c in reversed(coeffs):", "    value = float(0)\n    for c in reversed(coeffs):",
     TH + 'StaticGuards'),
    # the methods
    ('E_3 scores the slope', M3 + 'contract.py', "SCORE_COEFFICIENT = 0 ", "SCORE_COEFFICIENT = 1 ",
     T + 'EachVariantsOwnFit'),
    ('E_4 scores the value', M4 + 'contract.py', "SCORE_COEFFICIENT = 1 ", "SCORE_COEFFICIENT = 0 ",
     T + 'EachVariantsOwnFit'),
    ('the window drops the newest draw (off by one)', M3 + 'contract.py',
     "for r in rows[-window:]]", "for r in rows[-window - 1:-1]]", T + 'EachVariantsOwnFit'),
    ('minimax fitted to the raw series (smoothing skipped)', M4 + 'contract.py',
     "                s = PF.smoothed(y, half)\n", "                s = y\n", T + 'EachVariantsOwnFit'),
    ('interpolation through the raw series', M3 + 'contract.py',
     "            smooth = {j: PF.smoothed(y, half) for j, y in series.items()}",
     "            smooth = dict(series)", T + 'EachVariantsOwnFit'),
    ('every variant computed as the first', M4 + 'contract.py',
     "    return VARIANTS[task.variant_id]", "    return VARIANTS['POLY_LS_W52_D2_V1']", T + 'EachVariantsOwnFit'),
    ('an interpolation node moved', M3 + 'variants.py', "(50, 40, 26, 11, 1)", "(50, 41, 26, 10, 1)", T + 'Variants'),
    ('the two tables differ (E_4 window 100)', M4 + 'variants.py',
     "    'POLY_LS_W104_D3_V1': ('LS', 104, 3, None, None),", "    'POLY_LS_W104_D3_V1': ('LS', 100, 3, None, None),",
     T + 'Variants'),
    ('too few draws not recognised', M3 + 'contract.py',
     "    if len(rows) < window:\n        return None", "    if not rows:\n        return None", T + 'InsufficientHistory'),
    ('the MAIN series also counts the Powerball number', M3 + 'contract.py',
     "    drawn = [set(r['main']) if barrel.barrel_id == 'MAIN' else {r['powerball']} for r in rows[-window:]]",
     "    drawn = [set(r['main']) | {r.get('powerball')} if barrel.barrel_id == 'MAIN' else {r['powerball']}\n             for r in rows[-window:]]",
     T + 'CrossLabelInvariant'),
    ('verify() compares nothing', M4 + 'contract.py',
     "        if forecast['barrels'][bid]['scores'] != want:", "        if False:", T + 'ThroughTheContract'),
    ('compute() accepts the drawn-order view', M3 + 'contract.py',
     "    if task.observation_view != OBSERVATION_VIEW or task.include_dates:", "    if task.include_dates:",
     T + 'ThroughTheContract'),
    ('the method opens a file (it could read beyond its view)', M4 + 'contract.py',
     "    rows = view.simple_rows()\n", "    rows = view.simple_rows()\n    open(__file__).close()\n", T + 'FolderGuards'),
    ('the runner does not list E_3', 'src/methods/Method_Contract_Runner.py',
     "ADAPTERS = {'E_1': e_001, 'E_3': e_003, 'E_4': e_004, 'E_6': e_006}",
     "ADAPTERS = {'E_1': e_001, 'E_4': e_004, 'E_6': e_006}", T + 'AsInstalled'),
    ('the E_4 IN_DEVELOPMENT flag deleted without a release', M4 + 'IN_DEVELOPMENT.txt', None, None, T + 'AsInstalled'),
    ('an E_3 entry installed as SUPPORTED', 'src/methods/_common/contract_data/registry/OZLOTTO/E_3/'
     'POLY_MINIMAX_W52_D3_H4_V1/entry_0001.json', '"registry_status":"FORMULA_OPEN"',
     '"registry_status":"SUPPORTED"', T + 'AsInstalled'),
]


def run(root, test):
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(root / p) for p in ('src', 'src/methods', 'tests'))
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return subprocess.run([sys.executable, '-B', '-m', 'unittest', '-q', test], cwd=root, env=env,
                          capture_output=True, text=True).returncode


def copy(tmp, name):
    d = tmp / name
    for part in ('src', 'tests'):
        shutil.copytree(tree / part, d / part, ignore=shutil.ignore_patterns('__pycache__'))
    return d


fails = 0
with tempfile.TemporaryDirectory(prefix='e34_mut_') as t:
    tmp = Path(t)
    c = copy(tmp, 'control')
    for test in sorted({m[4] for m in MUTANTS}):
        ok = run(c, test) == 0
        print(('PASS' if ok else 'FAIL'), 'control passes', test)
        fails += not ok
    for i, (what, rel, old, new, test) in enumerate(MUTANTS):
        d = copy(tmp, f'm{i}')
        p = d / rel
        if old is None:
            p.unlink()
        else:
            s = p.read_text(encoding='utf-8')
            assert s.count(old) == 1, (what, old[:40])
            p.write_text(s.replace(old, new), encoding='utf-8')
        failed = run(d, test) != 0
        print(('PASS' if failed else 'FAIL'), f'mutation: {what} -> {test} fails')
        fails += not failed
print('RESULT', 'PASS' if not fails else f'FAIL ({fails})')
sys.exit(1 if fails else 0)
