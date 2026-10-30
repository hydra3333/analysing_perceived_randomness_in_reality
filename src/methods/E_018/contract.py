"""E_18 revision 1 through the E_2-readiness contract: compute() and verify() for the shared runner.

The shared standalone runner has already checked the release rule and loaded the prefix-only view before
compute() is called. compute() reads only the view and the frozen task it is given; the contract assembles,
ranks, applies ties and validates the record (E2R-R07). Specification: doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md section 4.4.
Mixture of recurrence modes: a fixed library of four gap laws (FAST, FAIR, SLOW, REGULAR); per-label weights
by an exact minimum chi-square fit of the label's binned completed gaps (shrunk by c fair pseudo-gaps) over
the simplex, every support tried; s_j = the mixture hazard at the projected age G_j.
Scores only: no probability vector is published (owner decision W2-4).
With fewer eligible draws than the variant's minimum, nothing is returned and the contract records
INSUFFICIENT_HISTORY. verify() recomputes by a second, differently written route and refuses any difference.
"""
from __future__ import annotations

from fractions import Fraction

from E_018.variants import VARIANTS
from _common import recurrence_gaps as RG
from _common.contract_forecast import BarrelOutput, MethodOutput, ScoredRanking
from _common.game_profiles import get_profile

METHOD_ID = 'E_18'
OBSERVATION_VIEW = 'UNORDERED_SET'
PUBLISHES_PROBABILITIES = False
PROVENANCE = 'E_18 r1 (Mixtures of Recurrence Modes): exact rational arithmetic, each value rounded once to float64'


def _config(task):
    if task.method_id != METHOD_ID:
        raise ValueError(f'this module computes {METHOD_ID} only')
    if task.variant_id not in VARIANTS:
        raise ValueError(f'unknown {METHOD_ID} variant {task.variant_id!r}')
    if task.observation_view != OBSERVATION_VIEW or task.include_dates:
        raise ValueError(f'{METHOD_ID} uses the unordered view without dates')
    return VARIANTS[task.variant_id]


def _barrel_draws(view, barrel_id):
    """The labels drawn in one barrel at each eligible draw, oldest first."""
    rows = view.simple_rows()
    if barrel_id == 'MAIN':
        return [list(r['main']) for r in rows]
    return [[r['powerball']] for r in rows]


def _surv_geom(p, G):
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
    return out


def _exact(task, view, second: bool):
    """{barrel_id: {label: exact score}}, or None when the history is shorter than the variant's minimum."""
    cfg = _config(task)
    barrels = get_profile(task.game_id).barrels
    if len(view.simple_rows()) < cfg[-1]:
        return None
    return {b.barrel_id: _scores(_barrel_draws(view, b.barrel_id), b, cfg, second) for b in barrels}


def compute(task, view) -> MethodOutput:
    exact = _exact(task, view, second=False)
    if exact is None:
        return MethodOutput(barrels={})                    # the contract records INSUFFICIENT_HISTORY
    out = {}
    for bid, s in exact.items():
        floats = {j: float(v) for j, v in s.items()}        # correctly rounded, once
        out[bid] = BarrelOutput(ranking=ScoredRanking(floats))
    return MethodOutput(barrels=out)


def verify(task, view, forecast, diagnostic) -> None:
    """Raise ValueError unless the record equals the second route's recomputation."""
    if diagnostic is not None:
        raise ValueError(f'{METHOD_ID} declares no diagnostic record')
    if forecast is None:
        raise ValueError(f'{METHOD_ID} always has a forecast record')
    exact = _exact(task, view, second=True)
    if exact is None:
        if forecast['record_status'] != 'INSUFFICIENT_HISTORY':
            raise ValueError(f'{METHOD_ID} check: too few draws, but the record is not INSUFFICIENT_HISTORY')
        return
    if set(forecast['barrels']) != set(exact):
        raise ValueError(f'{METHOD_ID} check: barrels differ')
    for bid, s in exact.items():
        b = next(x for x in get_profile(task.game_id).barrels if x.barrel_id == bid)
        want = [float(s[j]) for j in range(b.low, b.high + 1)]
        rec = forecast['barrels'][bid]
        if rec['scores'] != want:
            raise ValueError(f'{METHOD_ID} check: the record differs from the recomputation in barrel {bid}')
        if rec['probability'] != {'kind': 'NONE'}:
            raise ValueError(f'{METHOD_ID} check: a score-only method published a probability in barrel {bid}')
