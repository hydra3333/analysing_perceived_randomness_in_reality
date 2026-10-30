"""Write the four wave 2 method folders (E_002, E_017, E_018, E_019) into TREE. Claude, 30 Oct 2026.
Usage: python3 -I write_wave2_methods.py TREE. Creates files; refuses to overwrite."""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
SPEC = 'doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md'

M = {
 'E_2': dict(folder='E_002', name='Expected Recurrence-Interval Alignment', sec='4.1',
   doc='Recurrence-interval alignment: c_j is the mean or median of the label\'s completed gaps (all, or its last\n'
       'n), or the fair mean gap L/K if it has none; s_j = -|G_j - c_j| / c_j, G_j being its projected age.',
   table='''# variant_id: (statistic 'mean' or 'median'; the last n gaps, or None for all; minimum history)
VARIANTS = MappingProxyType({
    'RECUR_MEAN_ALL_V1': ('mean', None, 104),
    'RECUR_MEDIAN_ALL_V1': ('median', None, 104),
    'RECUR_MEAN_LAST8_V1': ('mean', 8, 104),
})''',
   rule='''def _median_by_sorting(g):
    s = sorted(g)
    n = len(s)
    return Fraction(s[n // 2]) if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)


def _median_by_counting(g):
    """The median from a count of each gap length, without sorting the gaps."""
    counts = {}
    for x in g:
        counts[x] = counts.get(x, 0) + 1
    n, seen, lower = len(g), 0, None
    for value in range(1, max(counts) + 1):
        seen += counts.get(value, 0)
        if lower is None and seen >= (n + 1) // 2:
            lower = value
        if seen >= n // 2 + 1:
            return Fraction(lower + value, 2) if n % 2 == 0 else Fraction(lower)
    raise ValueError('median not found')


def _scores(draws, b, cfg, second):
    stat, last_n, _minimum = cfg
    fair_gap = Fraction(b.high - b.low + 1, b.selected)
    app = RG.appearances(draws, b.low, b.high)
    ages = RG.projected_ages(len(draws), app)
    out = {}
    if not second:
        gaps = RG.completed_gaps(app)
        for j in app:
            g = gaps[j][-last_n:] if last_n else gaps[j]
            if not g:
                c = fair_gap
            elif stat == 'mean':
                c = Fraction(sum(g), len(g))
            else:
                c = _median_by_sorting(g)
            out[j] = -abs(ages[j] - c) / c
        return out
    # second route: the mean by telescoping the appearance positions; the median by counting; gaps by a scan
    scanned = RG.gaps_by_scan(draws, b.low, b.high)
    for j, p in app.items():
        if len(p) < 2:
            c = fair_gap
        elif stat == 'mean':
            q = p[-(last_n + 1):] if last_n else p
            c = Fraction(q[-1] - q[0], len(q) - 1)
        else:
            c = _median_by_counting(scanned[j][-last_n:] if last_n else scanned[j])
        out[j] = -abs(ages[j] - c) / c
    return out'''),
 'E_17': dict(folder='E_017', name='Discrete Recurrence Hazard Curves', sec='4.2',
   doc='Discrete recurrence hazard (Method A as E_17). Binned: h_b = (E_b + c r)/(R_b + c) over seven log-spaced age\n'
       'bins, s_j = h at the bin of the projected age G_j. Log-age sign (Method A\'s predictor, exactly in its\n'
       'ranking): sigma = the certified sign of sum_k (n E_k - e R_k) ln k, s_j = sigma * G_j.',
   table='''# variant_id: (form 'bins' or 'logage'; prior strength c, or None; window in draws, or None for all; minimum history)
VARIANTS = MappingProxyType({
    'HAZARD_BINS_C100_V1': ('bins', Fraction(100), None, 52),
    'HAZARD_BINS_W208_C100_V1': ('bins', Fraction(100), 208, 208),
    'HAZARD_LOGAGE_SIGN_V1': ('logage', None, None, 52),
})''',
   rule='''def binned_hazard(draws, b, c, window, second):
    """[h_b] for the barrel's bins, and the bin edges. Route 1 sums per-age counts from the per-draw walk into
    bins; route 2 counts directly into bins from the gaps route."""
    L = b.high - b.low + 1
    r = Fraction(b.selected, L)
    edges = RG.bin_edges(L, b.selected)
    nb = len(edges) + 1
    Rb, Eb = [0] * nb, [0] * nb
    if not second:
        R, E = RG.pooled(RG.label_exposures_by_walk(draws, b.low, b.high, window))
        for k, n in R.items():
            Rb[RG.bin_of(k, edges)] += n
        for k, n in E.items():
            Eb[RG.bin_of(k, edges)] += n
    else:
        for Rj, Ej in RG.label_exposures_from_gaps(draws, b.low, b.high, window).values():
            for k, n in Rj.items():
                Rb[RG.bin_of(k, edges)] += n
            for k, n in Ej.items():
                Eb[RG.bin_of(k, edges)] += n
    return [(Eb[i] + c * r) / (Rb[i] + c) for i in range(nb)], edges


def _scores(draws, b, cfg, second):
    form, c, window, _minimum = cfg
    ages = RG.projected_ages(len(draws), RG.appearances(draws, b.low, b.high))
    if form == 'bins':
        h, edges = binned_hazard(draws, b, c, window, second)
        return {j: h[RG.bin_of(g, edges)] for j, g in ages.items()}
    if not second:
        a = RG.log_age_coefficients(*RG.pooled(RG.label_exposures_by_walk(draws, b.low, b.high)))
        sigma = RG.log_sign_route_1(a)
    else:
        a = RG.log_age_coefficients(*RG.pooled(RG.label_exposures_from_gaps(draws, b.low, b.high)))
        sigma = RG.log_sign_route_2(a)
    return {j: Fraction(sigma * g) for j, g in ages.items()}'''),
 'E_19': dict(folder='E_019', name='Periodic Recurrence-Hazard Peaks', sec='4.3',
   doc='Periodic recurrence hazard: E_17\'s binned hazard b(k) (prior c, all draws) as the trend, times a per-label\n'
       'factor in age mod T shrunk by d towards the pooled one, with the label\'s overall level divided out:\n'
       's_j = b(G_j) psi_{j, G_j mod T}.',
   table='''# variant_id: (cycle T; trend prior c; shrinkage d; minimum history)
VARIANTS = MappingProxyType({
    'PERIODIC_T2_V1': (2, Fraction(100), Fraction(20), 104),
    'PERIODIC_T3_V1': (3, Fraction(100), Fraction(20), 104),
    'PERIODIC_T4_V1': (4, Fraction(100), Fraction(20), 104),
})''',
   rule='''def _trend(per_label, b, c):
    """E_17's binned hazard with prior c over all draws, from the given per-label counts."""
    L = b.high - b.low + 1
    r = Fraction(b.selected, L)
    edges = RG.bin_edges(L, b.selected)
    nb = len(edges) + 1
    Rb, Eb = [0] * nb, [0] * nb
    R, E = RG.pooled(per_label)
    for k, n in R.items():
        Rb[RG.bin_of(k, edges)] += n
    for k, n in E.items():
        Eb[RG.bin_of(k, edges)] += n
    h = [(Eb[i] + c * r) / (Rb[i] + c) for i in range(nb)]
    return lambda k: h[RG.bin_of(k, edges)]


def _scores(draws, b, cfg, second):
    T, c, d, _minimum = cfg
    per_label = (RG.label_exposures_from_gaps if second else RG.label_exposures_by_walk)(draws, b.low, b.high)
    trend = _trend(per_label, b, c)
    O = {j: [0] * T for j in per_label}
    X = {j: [Fraction(0)] * T for j in per_label}
    for j, (Rj, Ej) in per_label.items():
        for k, n in Rj.items():
            X[j][k % T] += n * trend(k)
        for k, n in Ej.items():
            O[j][k % T] += n
    if not second:
        Op = [sum(O[j][q] for j in O) for q in range(T)]
        Xp = [sum((X[j][q] for j in X), Fraction(0)) for q in range(T)]
    else:                                            # pooled by residue straight from the pooled counts
        R, E = RG.pooled(per_label)
        Op, Xp = [0] * T, [Fraction(0)] * T
        for k, n in R.items():
            Xp[k % T] += n * trend(k)
        for k, n in E.items():
            Op[k % T] += n
    phi = [(Op[q] + d) / (Xp[q] + d) for q in range(T)]
    ages = RG.projected_ages(len(draws), RG.appearances(draws, b.low, b.high))
    out = {}
    for j, g in ages.items():
        level = (sum(O[j]) + d) / (sum(X[j], Fraction(0)) + d)
        q = g % T
        out[j] = trend(g) * ((O[j][q] + d * phi[q]) / (X[j][q] + d)) / level
    return out'''),
 'E_18': dict(folder='E_018', name='Mixtures of Recurrence Modes', sec='4.4',
   doc='Mixture of recurrence modes: a fixed library of four gap laws (FAST, FAIR, SLOW, REGULAR); per-label weights\n'
       'by an exact minimum chi-square fit of the label\'s binned completed gaps (shrunk by c fair pseudo-gaps) over\n'
       'the simplex, every support tried; s_j = the mixture hazard at the projected age G_j.',
   table='''# variant_id: (window in draws for the completed gaps, or None for all; prior pseudo-gaps c; minimum history)
VARIANTS = MappingProxyType({
    'MIX4_ALL_C10_V1': (None, Fraction(10), 104),
    'MIX4_W208_C10_V1': (208, Fraction(10), 208),
    'MIX4_W104_C10_V1': (104, Fraction(10), 104),
})''',
   rule='''def _surv_geom(p, G):
    return (1 - p) ** (G - 1)


def _surv_nb2(p, G):
    return Fraction(1) if G <= 1 else (1 - p) ** (G - 1) + (G - 1) * p * (1 - p) ** (G - 2)


def components(r):
    """FAST, FAIR, SLOW, REGULAR as survival functions S(G) = P(gap >= G), for the fair rate r."""
    return (lambda G: _surv_geom(2 * r, G), lambda G: _surv_geom(r, G),
            lambda G: _surv_geom(r / 2, G), lambda G: _surv_nb2(2 * r, G))


def _pmf_and_survival_by_summation(i, r, G):
    """(P(gap = G), 1 - sum of P(gap = g) for g < G) for law i, from its probability formula alone, summed one
    gap length at a time (verify()'s second route for the survival values)."""
    p = (2 * r, r, r / 2, 2 * r)[i]
    below, power = Fraction(0), Fraction(1)          # power = (1 - p)^(g - 1) for geometric, ^(g - 2) for REGULAR
    for g in range(1, G + 1):
        if i == 3:
            pmf = Fraction(0) if g < 2 else (g - 1) * p * p * power
            if g >= 2:
                power *= 1 - p
        else:
            pmf = p * power
            power *= 1 - p
        if g == G:
            return pmf, 1 - below
        below += pmf


def _solve(A, rhs):
    n = len(A)
    M = [row[:] + [rhs[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = next((i for i in range(col, n) if M[i][col] != 0), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        for i in range(n):
            if i != col and M[i][col] != 0:
                f = M[i][col] / M[col][col]
                M[i] = [x - f * y for x, y in zip(M[i], M[col])]
    return [M[i][n] / M[i][i] for i in range(n)]


def _objective(q, P, Pf, w):
    return sum(((q[b] - sum(w[c] * P[c][b] for c in range(len(P)))) ** 2 / Pf[b] for b in range(len(q))), Fraction(0))


def fit_weights(q, P, Pf):
    """Minimise sum_b (q_b - sum_c w_c P_c(b))^2 / Pf_b over the simplex, exactly: the equality-constrained solution
    on every support, keeping the feasible one with the smallest objective (the objective is strictly convex)."""
    C = len(P)
    best = None
    for mask in range(1, 2 ** C):
        S = [c for c in range(C) if mask >> c & 1]
        A = [[sum((P[a][b] * P[s][b] / Pf[b] for b in range(len(q))), Fraction(0)) for s in S] + [Fraction(1)] for a in S]
        A.append([Fraction(1)] * len(S) + [Fraction(0)])
        rhs = [sum((P[a][b] * q[b] / Pf[b] for b in range(len(q))), Fraction(0)) for a in S] + [Fraction(1)]
        sol = _solve(A, rhs)
        if sol is None or any(x < 0 for x in sol[:len(S)]):
            continue
        w = [Fraction(0)] * C
        for s, x in zip(S, sol):
            w[s] = x
        F = _objective(q, P, Pf, w)
        if best is None or F < best[0]:
            best = (F, w)
    return best[1]


def kkt_holds(q, P, Pf, w):
    """The exact optimality certificate: w on the simplex, and the objective's gradient equal on the support and no
    smaller off it (the conditions for the minimum of a convex quadratic on the simplex)."""
    if any(x < 0 for x in w) or sum(w) != 1:
        return False
    C, B = len(P), len(q)
    resid = [q[b] - sum(w[c] * P[c][b] for c in range(C)) for b in range(B)]
    grad = [-2 * sum((P[c][b] * resid[b] / Pf[b] for b in range(B)), Fraction(0)) for c in range(C)]
    on = {grad[c] for c in range(C) if w[c] > 0}
    if len(on) != 1:
        return False
    level = on.pop()
    return all(grad[c] >= level for c in range(C) if w[c] == 0)


def _scores(draws, b, cfg, second):
    window, c, _minimum = cfg
    L = b.high - b.low + 1
    r = Fraction(b.selected, L)
    edges = RG.bin_edges(L, b.selected)
    comps = components(r)
    ranges = RG.bin_ranges(edges)
    P = [[S(lo) - (S(hi + 1) if hi is not None else 0) for lo, hi in ranges] for S in comps]
    Pf = P[1]
    app = RG.appearances(draws, b.low, b.high)
    ages = RG.projected_ages(len(draws), app)
    gaps = (RG.gaps_by_scan(draws, b.low, b.high, window) if second
            else RG.gaps_in_window(app, len(draws), window))
    out = {}
    for j in app:
        o = [0] * len(Pf)
        for g in gaps[j]:
            o[RG.bin_of(g, edges)] += 1
        q = [(o[i] + c * Pf[i]) / (len(gaps[j]) + c) for i in range(len(Pf))]
        w = fit_weights(q, P, Pf)
        G = ages[j]
        if not second:
            num = sum((w[i] * (comps[i](G) - comps[i](G + 1)) for i in range(4)), Fraction(0))
            den = sum((w[i] * comps[i](G) for i in range(4)), Fraction(0))
        else:
            if not kkt_holds(q, P, Pf, w):
                raise ValueError('E_18 check: the fitted weights fail the optimality certificate')
            parts = [_pmf_and_survival_by_summation(i, r, G) for i in range(4)]
            num = sum((w[i] * parts[i][0] for i in range(4)), Fraction(0))
            den = sum((w[i] * parts[i][1] for i in range(4)), Fraction(0))
        out[j] = num / den
    return out'''),
}

CONTRACT = '''"""{mid} revision 1 through the E_2-readiness contract: compute() and verify() for the shared runner.

The shared standalone runner has already checked the release rule and loaded the prefix-only view before
compute() is called. compute() reads only the view and the frozen task it is given; the contract assembles,
ranks, applies ties and validates the record (E2R-R07). Specification: {spec} section {sec}.
{doc}
Scores only: no probability vector is published (owner decision W2-4).
With fewer eligible draws than the variant's minimum, nothing is returned and the contract records
INSUFFICIENT_HISTORY. verify() recomputes by a second, differently written route and refuses any difference.
"""
from __future__ import annotations

from fractions import Fraction

from {folder}.variants import VARIANTS
from _common import recurrence_gaps as RG
from _common.contract_forecast import BarrelOutput, MethodOutput, ScoredRanking
from _common.game_profiles import get_profile

METHOD_ID = '{mid}'
OBSERVATION_VIEW = 'UNORDERED_SET'
PUBLISHES_PROBABILITIES = False
PROVENANCE = '{mid} r1 ({name}): exact rational arithmetic, each value rounded once to float64'


def _config(task):
    if task.method_id != METHOD_ID:
        raise ValueError(f'this module computes {{METHOD_ID}} only')
    if task.variant_id not in VARIANTS:
        raise ValueError(f'unknown {{METHOD_ID}} variant {{task.variant_id!r}}')
    if task.observation_view != OBSERVATION_VIEW or task.include_dates:
        raise ValueError(f'{{METHOD_ID}} uses the unordered view without dates')
    return VARIANTS[task.variant_id]


def _barrel_draws(view, barrel_id):
    """The labels drawn in one barrel at each eligible draw, oldest first."""
    rows = view.simple_rows()
    if barrel_id == 'MAIN':
        return [list(r['main']) for r in rows]
    return [[r['powerball']] for r in rows]


{rule}


def _exact(task, view, second: bool):
    """{{barrel_id: {{label: exact score}}}}, or None when the history is shorter than the variant's minimum."""
    cfg = _config(task)
    barrels = get_profile(task.game_id).barrels
    if len(view.simple_rows()) < cfg[-1]:
        return None
    return {{b.barrel_id: _scores(_barrel_draws(view, b.barrel_id), b, cfg, second) for b in barrels}}


def compute(task, view) -> MethodOutput:
    exact = _exact(task, view, second=False)
    if exact is None:
        return MethodOutput(barrels={{}})                    # the contract records INSUFFICIENT_HISTORY
    out = {{}}
    for bid, s in exact.items():
        floats = {{j: float(v) for j, v in s.items()}}        # correctly rounded, once
        out[bid] = BarrelOutput(ranking=ScoredRanking(floats))
    return MethodOutput(barrels=out)


def verify(task, view, forecast, diagnostic) -> None:
    """Raise ValueError unless the record equals the second route's recomputation."""
    if diagnostic is not None:
        raise ValueError(f'{{METHOD_ID}} declares no diagnostic record')
    if forecast is None:
        raise ValueError(f'{{METHOD_ID}} always has a forecast record')
    exact = _exact(task, view, second=True)
    if exact is None:
        if forecast['record_status'] != 'INSUFFICIENT_HISTORY':
            raise ValueError(f'{{METHOD_ID}} check: too few draws, but the record is not INSUFFICIENT_HISTORY')
        return
    if set(forecast['barrels']) != set(exact):
        raise ValueError(f'{{METHOD_ID}} check: barrels differ')
    for bid, s in exact.items():
        b = next(x for x in get_profile(task.game_id).barrels if x.barrel_id == bid)
        want = [float(s[j]) for j in range(b.low, b.high + 1)]
        rec = forecast['barrels'][bid]
        if rec['scores'] != want:
            raise ValueError(f'{{METHOD_ID}} check: the record differs from the recomputation in barrel {{bid}}')
        if rec['probability'] != {{'kind': 'NONE'}}:
            raise ValueError(f'{{METHOD_ID}} check: a score-only method published a probability in barrel {{bid}}')
'''

for mid, m in M.items():
    d = tree / 'src' / 'methods' / m['folder']
    d.mkdir()
    files = {
        '__init__.py': f'"""{mid} - {m["name"]} (revision 1; wave 2).\n\nSpecification: {SPEC}. `variants` holds the fixed variant table and `contract` connects the method to\nthe shared contract runner. The gaps, exposures, bins and log-age sign are in the shared, reviewed helper\n_common/recurrence_gaps.py (revision 1), which E_2, E_17, E_18 and E_19 all use. Nothing here reads a file,\nstarts a process or touches orchestration.\n"""\n',
        'variants.py': f'"""{mid} revision 1: the fixed variants (design note v0.1r2 section 6). Changing or adding one is a new revision."""\nfrom fractions import Fraction\nfrom types import MappingProxyType\n\n{m["table"]}\n',
        'IN_DEVELOPMENT.txt': f'{mid} is in development: the dispatch gate refuses every {mid} request while this file exists (E2R-R57).\n\nRelease is a separate, small, reviewed package that deletes this file and appends a SUPPORTED registry\nentry (E2R-R58). Deleting this file alone releases nothing.\n',
        'contract.py': CONTRACT.format(mid=mid, spec=SPEC, sec=m['sec'], doc=m['doc'], folder=m['folder'],
                                       name=m['name'], rule=m['rule']),
    }
    for name, text in files.items():
        assert text.isascii(), (mid, name)
        with (d / name).open('x') as fh:
            fh.write(text)
    print(mid, sorted(files))
