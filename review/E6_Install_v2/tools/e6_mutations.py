"""Mutation checks for the E_6 package (Claude-side evidence; disposable copies only).

Usage: python3 -I e6_mutations.py TREE
For each planted defect (design note section 6.7, plus the gaps found while writing this tool), a temporary
copy of src/ and tests/ is changed and the named test must FAIL; the unchanged copy (control) must pass.
The tree itself is never changed and no bytecode is written to it. A `new` of None deletes the file.
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
M = 'src/methods/E_006/'
T = 'tests.test_e6_beta_bernoulli.'
MUTANTS = [
    ('a prior not centred on the fair-draw rate', M + 'beta_bernoulli.py',
     "    r = Fraction(selected, high - low + 1)\n    newest = len(draws) - 1",
     "    r = Fraction(1, 2)\n    newest = len(draws) - 1", T + 'WorkedExample'),
    ('a prior worth two draws (the sums stay exact)', M + 'beta_bernoulli.py',
     "    p = {j: (r + k[j]) / (1 + total) for j in k}", "    p = {j: (2 * r + k[j]) / (2 + total) for j in k}",
     T + 'WorkedExample'),
    ('weights anchored at the oldest draw', M + 'beta_bernoulli.py',
     "        w = lam ** (newest - i)", "        w = lam ** i", T + 'WorkedExample'),
    ('ages off by one (the newest draw weighs lambda)', M + 'beta_bernoulli.py',
     "        w = lam ** (newest - i)", "        w = lam ** (newest - i + 1)", T + 'WorkedExample'),
    ('a float power in place of the exact power', M + 'beta_bernoulli.py',
     "        w = lam ** (newest - i)", "        w = float(lam) ** (newest - i)", T + 'AsInstalled'),
    ('a variant factor changed', M + 'beta_bernoulli.py',
     "    'BETA_BERNOULLI_DECAY_74_75_V1': Fraction(74, 75),", "    'BETA_BERNOULLI_DECAY_74_75_V1': Fraction(73, 75),",
     T + 'WorkedExample'),
    ('every variant computed as full memory', M + 'contract.py',
     "    return VARIANTS[task.variant_id]", "    return VARIANTS['BETA_BERNOULLI_FULL_MEMORY_V1']",
     T + 'ExactNormalisation'),
    ('verify() compares nothing', M + 'contract.py',
     "        if rec['scores'] != want or rec['probability'].get('vector') != want:", "        if False:",
     T + 'ThroughTheContract'),
    ('the probability vector out of label order', M + 'contract.py',
     "probability=ProbabilityVector([floats[j] for j in sorted(floats)], PROVENANCE))",
     "probability=ProbabilityVector(sorted(floats.values()), PROVENANCE))", T + 'ThroughTheContract'),
    ('the method opens a file (it could read beyond its view)', M + 'contract.py',
     "    rows = view.simple_rows()\n", "    rows = view.simple_rows()\n    open(__file__).close()\n", T + 'AsInstalled'),
    ('compute() accepts the drawn-order view', M + 'contract.py',
     "    if task.observation_view != OBSERVATION_VIEW or task.include_dates:", "    if task.include_dates:",
     T + 'ThroughTheContract'),
    ('the runner does not list E_6', 'src/methods/Method_Contract_Runner.py',
     "ADAPTERS = {'E_1': e_001, 'E_6': e_006}", "ADAPTERS = {'E_1': e_001}", T + 'AsInstalled'),
    ('the IN_DEVELOPMENT flag deleted without a release', M + 'IN_DEVELOPMENT.txt', None, None, T + 'AsInstalled'),
    ('an E_6 entry installed as SUPPORTED', 'src/methods/_common/contract_data/registry/POWERBALL/E_6/'
     'BETA_BERNOULLI_FULL_MEMORY_V1/entry_0001.json', '"registry_status":"FORMULA_OPEN"',
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
with tempfile.TemporaryDirectory(prefix='e6_mut_') as t:
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
