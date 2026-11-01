"""PERF-1 mutation checks (Claude, 1 Nov 2026): each planted defect must make a test fail.
Usage: python3 -I perf1_mutations.py DEV_TREE"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

DEV = Path(sys.argv[1]).resolve()
N = 'src/evaluation/numerics.py'
T = ['test_perf1_numerics']
MUTANTS = [
    ('binary splitting: the halves combined with the wrong power', N,
     "        return part(l, m) * _pow(cpow, c, h - m) + _pow(apow, a, m + 1 - l) * part(m + 1, h)",
     "        return part(l, m) * _pow(cpow, c, h - m - 1) + _pow(apow, a, m + 1 - l) * part(m + 1, h)", T),
    ('binary splitting: the binomial recurrence off by one', N,
     "        binoms.append(binoms[-1] * (n - j) // (j + 1))",
     "        binoms.append(binoms[-1] * (n - j + 1) // (j + 1))", T),
    ('binary splitting: the short-range Horner skips a term', N,
     "            for j in range(h - 1, l - 1, -1):", "            for j in range(h - 1, l, -1):", T),
    ('guided search: the midpoint rule inverted', N,
     "    return hi if at_mid is False else lo\n\n\ndef clopper_pearson",
     "    return lo if at_mid is False else hi\n\n\ndef clopper_pearson", T),
    ('guided search: never confirmed with the exact tails', N,
     "    if not confirmed:\n        return _bisect_float(exact)", "    if False:\n        return _bisect_float(exact)", T),
    ('guided search: confirms the wrong side', N,
     "        confirmed = hi == 1.0 or exact(Fraction(hi)) is True",
     "        confirmed = lo == 0.0 or exact(Fraction(lo)) is False", T),
    ('decimal guide: one term too many (the guided path would fall back)', N,
     "    for j in range(lo, hi):\n        t = t * r * (n - j) / (j + 1)",
     "    for j in range(lo, hi + 1):\n        t = t * r * (n - j) / (j + 1)", T),
    ('lower-bound exact predicate compares the wrong way', N,
     "    return _upper_num(n, q.numerator, q.denominator, k) * half.denominator > half.numerator * q.denominator ** n",
     "    return _upper_num(n, q.numerator, q.denominator, k) * half.denominator < half.numerator * q.denominator ** n", T),
    ('a progress line shows a value, not a count', 'src/evaluation/report.py',
     "    progress(f'ledgers written: {len(scores)} score records, {len(ranks)} rank records')",
     "    progress(f'ledgers written: {len(scores)} score records, {ranks[:1]} rank records')", T),
]


def run(tree: Path, mods) -> bool:
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(tree / p) for p in ('src', 'src/methods', 'tests'))
    r = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-f'] + [f'tests.{m}' for m in mods], cwd=tree, env=env,
                       capture_output=True, text=True, timeout=1200)
    return r.returncode == 0


ok = run(DEV, sorted({m for x in MUTANTS for m in x[4]}))
print('baseline (unmutated) passes:', ok)
caught = 0
for name, rel, old, new, mods in MUTANTS:
    with tempfile.TemporaryDirectory() as td:
        tree = Path(td) / 't'
        shutil.copytree(DEV, tree, ignore=shutil.ignore_patterns('__pycache__'))
        f = tree / rel
        text = f.read_text(encoding='utf-8')
        if text.count(old) != 1:
            print(f'MUTANT NOT APPLIED ({text.count(old)} matches): {name}')
            continue
        f.write_text(text.replace(old, new), encoding='utf-8')
        passed = run(tree, mods)
        caught += not passed
        print(('CAUGHT   ' if not passed else 'SURVIVED ') + name)
print(f'{caught} of {len(MUTANTS)} mutants caught')
