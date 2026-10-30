"""Mutation checks for the wave 1 package (E_7, E_8, E_9, E_10 and their shared helper; Claude-side evidence;
disposable copies only).

Usage: python3 -I w1_mutations.py TREE
For each planted defect a temporary copy of src/ and tests/ is changed and the named test must FAIL; the
unchanged copy (control) must pass. The tree itself is never changed and no bytecode is written to it.
A `new` of None deletes the file.
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
H = 'src/methods/_common/occurrence_counts.py'
M7, M8, M9, M10 = (f'src/methods/E_0{n}/' for n in ('07', '08', '09', '10'))
TH = 'tests.test_occurrence_counts.'
T = 'tests.test_wave1_frequency.'
CFG = "    return VARIANTS[task.variant_id]"
FIRST = "    return next(iter(VARIANTS.values()))"
MUTANTS = [
    # the shared helper
    ('window counts take one draw too many', H, "    for d in draws[len(draws) - S:]:", "    for d in draws[len(draws) - S - 1:]:",
     TH + 'WorkedExamples'),
    ('the prefix-sum route off by one', H, "        out[j] = prefix[len(draws)] - prefix[len(draws) - S]",
     "        out[j] = prefix[len(draws)] - prefix[len(draws) - S + 1]", TH + 'TwoRoutesAgree'),
    ('decay weights anchored at the oldest draw', H, "        w = lam ** (newest - i)", "        w = lam ** i",
     TH + 'WorkedExamples'),
    ('the decay recursion weighs the new draw by lambda', H,
     "        out = {j: lam * s + (1 if j in present else 0) for j, s in out.items()}",
     "        out = {j: s + lam * (1 if j in present else 0) for j, s in out.items()}", TH + 'WorkedExamples'),
    ('periods counted from the oldest draw', H, "    start = len(draws) - n * P", "    start = 0", TH + 'WorkedExamples'),
    ('the period-index route off by one', H, "        back = (newest - i) // P", "        back = (newest - i + 1) // P",
     TH + 'TwoRoutesAgree'),
    ('a float lambda accepted', H, "    if type(lam) is not Fraction or not 0 < lam < 1:", "    if not 0 < lam < 1:",
     TH + 'Refusals'),
    ('a repeated label accepted', H, "        if len(set(d)) != len(d) or any(", "        if any(", TH + 'Refusals'),
    # the methods
    ('E_7 prior not centred on the fair rate', M7 + 'contract.py', "        return {j: (c * r + k[j]) / (c + size) for j in k}",
     "        return {j: (c / 2 + k[j]) / (c + size) for j in k}", T + 'WorkedExamples'),
    ('E_7 window ignored', M7 + 'contract.py', "    size = len(draws) if M is None else M", "    size = len(draws)",
     T + 'EachVariantsOwnRule'),
    ('E_7 every variant computed as the first', M7 + 'contract.py', CFG, FIRST, T + 'EachVariantsOwnRule'),
    ('E_8 every variant computed as the first', M8 + 'contract.py', CFG, FIRST, T + 'EachVariantsOwnRule'),
    ('E_9 every variant computed as the first', M9 + 'contract.py', CFG, FIRST, T + 'EachVariantsOwnRule'),
    ('E_10 every variant computed as the first', M10 + 'contract.py', CFG, FIRST, T + 'EachVariantsOwnRule'),
    ('E_10 sign flipped', M10 + 'contract.py',
     "    return {j: Fraction(k_short[j], S) - Fraction(k_long[j] - k_short[j], long - S) for j in k_short}",
     "    return {j: Fraction(k_long[j] - k_short[j], long - S) - Fraction(k_short[j], S) for j in k_short}",
     T + 'WorkedExamples'),
    ('E_10 long window overlaps the short one', M10 + 'contract.py',
     "    return {j: Fraction(k_short[j], S) - Fraction(k_long[j] - k_short[j], long - S) for j in k_short}",
     "    return {j: Fraction(k_short[j], S) - Fraction(k_long[j], long) for j in k_short}", T + 'WorkedExamples'),
    ('E_8 weight not clamped below at 0', M8 + 'contract.py',
     "    t = min(max(Fraction(0), sum(excess, Fraction(0)) / L), r * (1 - r))",
     "    t = min(sum(excess, Fraction(0)) / L, r * (1 - r))", T + 'WorkedExamples'),
    ('E_8 leans towards the oldest period', M8 + 'contract.py', "            m[j], latest[j] = mj, p[-1]",
     "            m[j], latest[j] = mj, p[0]", T + 'WorkedExamples'),
    ('E_8 variance divided by n, not n - 1 (compute only)', M8 + 'contract.py',
     "            V = sum(((x - mj) ** 2 for x in p), Fraction(0)) / (n - 1)",
     "            V = sum(((x - mj) ** 2 for x in p), Fraction(0)) / n", T + 'EachVariantsOwnRule'),
    ('E_9 verify() compares nothing', M9 + 'contract.py', "        if rec['scores'] != want:", "        if False:",
     T + 'ThroughTheContract'),
    ('E_7 verify() ignores the probability vector', M7 + 'contract.py',
     "        if rec['probability'].get('vector') != want:", "        if False:", T + 'ThroughTheContract'),
    ('E_7 compute() accepts the drawn-order view', M7 + 'contract.py',
     "    if task.observation_view != OBSERVATION_VIEW or task.include_dates:", "    if task.include_dates:",
     T + 'ThroughTheContract'),
    ('E_10 minimum history ignored', M10 + 'contract.py', "    if len(view.simple_rows()) < cfg[-1]:", "    if False:",
     T + 'InsufficientHistory'),
    ('E_9 factor changed', M9 + 'variants.py', "    'EXP_DECAY_18_19_V1': (Fraction(18, 19), 1),",
     "    'EXP_DECAY_18_19_V1': (Fraction(17, 18), 1),", T + 'Variants'),
    ('E_7 full-history minimum changed', M7 + 'variants.py', "    'BETA_SHRINK_FULL_C52_V1': (None, Fraction(52), 1),",
     "    'BETA_SHRINK_FULL_C52_V1': (None, Fraction(52), 52),", T + 'Variants'),
    ('the method opens a file (it could read beyond its view)', M8 + 'contract.py',
     "    rows = view.simple_rows()\n", "    rows = view.simple_rows()\n    open(__file__).close()\n", T + 'FolderGuards'),
    ('the runner does not list E_10', 'src/methods/Method_Contract_Runner.py',
     "            'E_10': e_010}", "            }", T + 'AsInstalled'),
    ('the E_9 IN_DEVELOPMENT flag deleted without a release', M9 + 'IN_DEVELOPMENT.txt', None, None, T + 'AsInstalled'),
    ('an E_8 entry installed as SUPPORTED', 'src/methods/_common/contract_data/registry/OZLOTTO/E_8/'
     'HIER_PERIODS_P52_V1/entry_0001.json', '"registry_status":"FORMULA_OPEN"', '"registry_status":"SUPPORTED"',
     T + 'AsInstalled'),
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
with tempfile.TemporaryDirectory(prefix='w1_mut_') as t:
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
