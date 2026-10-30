"""Mutation checks for the wave 2 package (E_2, E_17, E_18, E_19 and their shared helper; Claude-side evidence;
disposable copies only).

Usage: python3 -I w2_mutations.py TREE
For each planted defect a temporary copy of src/ and tests/ is changed and the named test must FAIL; the
unchanged copy (control) must pass. The tree itself is never changed and no bytecode is written to it.
A `new` of None deletes the file.
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
H = 'src/methods/_common/recurrence_gaps.py'
M2, M17, M18, M19 = (f'src/methods/E_0{n}/contract.py' for n in ('02', '17', '18', '19'))
TH = 'tests.test_recurrence_gaps.'
T = 'tests.test_wave2_recurrence.'
CFG = "    return VARIANTS[task.variant_id]"
FIRST = "    return next(iter(VARIANTS.values()))"
VERIFY = "        if rec['scores'] != want:"
MUTANTS = [
    # the shared helper
    ('projected age one short', H, "    return {j: W + 1 - (p[-1] if p else 0) for j, p in app.items()}",
     "    return {j: W - (p[-1] if p else 0) for j, p in app.items()}", TH + 'WorkedExamples'),
    ('a never-seen label aged W, not W + 1', H, "    return {j: W + 1 - (p[-1] if p else 0) for j, p in app.items()}",
     "    return {j: W + 1 - (p[-1] if p else 1) for j, p in app.items()}", TH + 'Censoring'),
    ('exposures counted before the first appearance', H, "                if p is not None:\n                    k = i - p",
     "                if True:\n                    k = i - (p or 0)", TH + 'Censoring'),
    ('the open stretch left out of the gaps route', H,
     "        if p:\n            for k in range(max(1, start - p[-1]), W - p[-1] + 1):",
     "        if False:\n            for k in range(max(1, start - p[-1]), W - p[-1] + 1):", TH + 'WorkedExamples'),
    ('the walk window one draw short', H, "        if i >= start:", "        if i > start:", TH + 'Censoring'),
    ('gaps_in_window admits a gap starting just outside', H, " for a, b in zip(p, p[1:]) if a > lo]",
     " for a, b in zip(p, p[1:]) if a >= lo]", TH + 'Censoring'),
    ('bin edges rounded down', H, "        e = -((-x.numerator) // x.denominator)", "        e = x.numerator // x.denominator",
     TH + 'WorkedExamples'),
    ('an age on an edge put in the next bin', H, "    return sum(1 for e in edges if k > e)",
     "    return sum(1 for e in edges if k >= e)", TH + 'WorkedExamples'),
    ('log-age coefficients with the wrong sign', H, "    return {k: n * E.get(k, 0) - e * r for k, r in R.items()}",
     "    return {k: e * r - n * E.get(k, 0) for k, r in R.items()}", TH + 'WorkedExamples'),
    ('trial division takes each prime once', H, "            while n % d == 0:\n                out[d] = out.get(d, 0) + c",
     "            if n % d == 0:\n                out[d] = out.get(d, 0) + c", TH + 'TwoRoutesAgree'),
    ('the sieve stops short of a square', H, "    while i * i <= top:", "    while i * i < top:", TH + 'LogSign'),
    ('a positive sign read from the upper bound', H, "        if lo > 0:\n            return 1",
     "        if hi > 0:\n            return 1", TH + 'LogSign'),
    ('route 2 without its exact-zero test', H, "    if not prime_exponents_by_sieve(a):\n        return 0",
     "    if False:\n        return 0", TH + 'LogSign'),
    ('route 1 bounds an empty map', H, "    return 0 if not e else bounded_sign(e)", "    return bounded_sign(e)",
     TH + 'LogSign'),
    ('a repeated label accepted', H, "        if len(set(d)) != len(d) or any(", "        if any(", TH + 'Refusals'),
    # E_2
    ('E_2 fallback is not the fair mean gap', M2, "    fair_gap = Fraction(b.high - b.low + 1, b.selected)",
     "    fair_gap = Fraction(b.high - b.low + 1, b.selected + 1)", T + 'WorkedExamples'),
    ('E_2 absolute, not relative, distance', M2, "            out[j] = -abs(ages[j] - c) / c\n        return out",
     "            out[j] = -abs(ages[j] - c)\n        return out", T + 'WorkedExamples'),
    ('E_2 median takes the upper middle only', M2,
     "    return Fraction(s[n // 2]) if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)",
     "    return Fraction(s[n // 2])", T + 'WorkedExamples'),
    ('E_2 telescoping one gap short (verify route)', M2, "            q = p[-(last_n + 1):] if last_n else p",
     "            q = p[-last_n:] if last_n else p", T + 'WorkedExamples'),
    ('E_2 every variant computed as the first', M2, CFG, FIRST, T + 'EachVariantsOwnRule'),
    ('E_2 verify() compares nothing', M2, VERIFY, "        if False:", T + 'ThroughTheContract'),
    # E_17
    ('E_17 bins shrunk towards one half', M17, "    return [(Eb[i] + c * r) / (Rb[i] + c) for i in range(nb)], edges",
     "    return [(Eb[i] + c / 2) / (Rb[i] + c) for i in range(nb)], edges", T + 'WorkedExamples'),
    ('E_17 window ignored (compute route)', M17,
     "        R, E = RG.pooled(RG.label_exposures_by_walk(draws, b.low, b.high, window))",
     "        R, E = RG.pooled(RG.label_exposures_by_walk(draws, b.low, b.high))", T + 'EachVariantsOwnRule'),
    ('E_17 log-age sign reversed', M17, "    return {j: Fraction(sigma * g) for j, g in ages.items()}",
     "    return {j: Fraction(-sigma * g) for j, g in ages.items()}", T + 'WorkedExamples'),
    ('E_17 every variant computed as the first', M17, CFG, FIRST, T + 'EachVariantsOwnRule'),
    ('E_17 verify() compares nothing', M17, VERIFY, "        if False:", T + 'ThroughTheContract'),
    # E_19
    ('E_19 level not divided out', M19, "        out[j] = trend(g) * ((O[j][q] + d * phi[q]) / (X[j][q] + d)) / level",
     "        out[j] = trend(g) * ((O[j][q] + d * phi[q]) / (X[j][q] + d))", T + 'WorkedExamples'),
    ('E_19 residue of the wrong age', M19, "        q = g % T", "        q = (g + 1) % T", T + 'WorkedExamples'),
    ('E_19 shrunk towards 1, not the pooled factor', M19,
     "        out[j] = trend(g) * ((O[j][q] + d * phi[q]) / (X[j][q] + d)) / level",
     "        out[j] = trend(g) * ((O[j][q] + d) / (X[j][q] + d)) / level", T + 'WorkedExamples'),
    ('E_19 every variant computed as the first', M19, CFG, FIRST, T + 'EachVariantsOwnRule'),
    # E_18
    ('E_18 FAST law at three times the fair rate', M18,
     "    return (lambda G: _surv_geom(2 * r, G), lambda G: _surv_geom(r, G),",
     "    return (lambda G: _surv_geom(3 * r, G), lambda G: _surv_geom(r, G),", T + 'WorkedExamples'),
    ('E_18 prior pseudo-gaps shaped as FAST, not FAIR', M18,
     "        q = [(o[i] + c * Pf[i]) / (len(gaps[j]) + c) for i in range(len(Pf))]",
     "        q = [(o[i] + c * P[0][i]) / (len(gaps[j]) + c) for i in range(len(Pf))]", T + 'WorkedExamples'),
    ('E_18 negative weights accepted', M18, "        if sol is None or any(x < 0 for x in sol[:len(S)]):",
     "        if sol is None:", T + 'EachVariantsOwnRule'),
    ('E_18 optimality certificate not checked', M18, "            if not kkt_holds(q, P, Pf, w):",
     "            if False:", T + 'ThroughTheContract.test_e18_verify_refuses_weights_that_are_not_optimal'),
    ('E_18 certificate ignores the off-support gradients', M18,
     "    return all(grad[c] >= level for c in range(C) if w[c] == 0)", "    return True",
     T + 'ThroughTheContract.test_e18_verify_refuses_weights_that_are_not_optimal'),
    ('E_18 hazard read one gap too far', M18,
     "            num = sum((w[i] * (comps[i](G) - comps[i](G + 1)) for i in range(4)), Fraction(0))",
     "            num = sum((w[i] * (comps[i](G) - comps[i](G + 2)) for i in range(4)), Fraction(0))", T + 'WorkedExamples'),
    ('E_18 every variant computed as the first', M18, CFG, FIRST, T + 'EachVariantsOwnRule'),
    # the runner and the installed state
    ('the runner does not list E_18', 'src/methods/Method_Contract_Runner.py', "'E_17': e_017, 'E_18': e_018,",
     "'E_17': e_017,", T + 'AsInstalled'),
    ('E_19 flag file deleted', 'src/methods/E_019/IN_DEVELOPMENT.txt', None, None, T + 'AsInstalled'),
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
with tempfile.TemporaryDirectory(prefix='w2_mut_') as t:
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
