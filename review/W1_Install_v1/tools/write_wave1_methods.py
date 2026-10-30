"""Write the four wave-1 method folders (E_007, E_008, E_009, E_010) into TREE. Claude, 30 Oct 2026.
Usage: python3 -I write_wave1_methods.py TREE. Creates files; refuses to overwrite."""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
SPEC = 'doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md'

M = {
 'E_7': dict(folder='E_007', name='Bayesian Frequency Shrinkage', probs=True, sec='3.1',
   doc='Beta shrinkage over a window: s_j = (c r + k_j(M)) / (c + M), the posterior mean of a Beta(c r, c(1 - r))\n'
       'prior updated by the window\'s counts (r = K/L, the fair-draw rate). The values sum to K exactly.',
   table='''# variant_id: (window M, or None for all eligible draws; prior strength c; minimum history)
VARIANTS = MappingProxyType({
    'BETA_SHRINK_W52_C52_V1': (52, Fraction(52), 52),
    'BETA_SHRINK_W104_C52_V1': (104, Fraction(52), 104),
    'BETA_SHRINK_FULL_C52_V1': (None, Fraction(52), 1),
})''',
   rule='''def _scores(draws, b, cfg, second):
    M, c, _minimum = cfg
    size = len(draws) if M is None else M
    r = Fraction(b.selected, b.high - b.low + 1)
    if not second:
        k = OC.window_counts(draws, b.low, b.high, size)
        return {j: (c * r + k[j]) / (c + size) for j in k}
    # second route: the posterior built by sequential Beta updates, one draw at a time
    alpha = {j: c * r for j in range(b.low, b.high + 1)}
    beta = {j: c * (1 - r) for j in alpha}
    for d in draws[len(draws) - size:]:
        present = set(d)
        for j in alpha:
            if j in present:
                alpha[j] += 1
            else:
                beta[j] += 1
    return {j: alpha[j] / (alpha[j] + beta[j]) for j in alpha}'''),
 'E_8': dict(folder='E_008', name='Hierarchical Dirichlet-Multinomial Propensity', probs=True, sec='3.4',
   doc='Hierarchical rates across periods (beta-binomial, method of moments): the newest n*P draws in n periods\n'
       'of P; the between-period excess variance, pooled over labels and clamped to [0, r(1 - r)], gives one\n'
       'weight w for the latest period; s_j = w p_{j,latest} + (1 - w) m_j. The values sum to K exactly.',
   table='''# variant_id: (period length P, minimum history = 2P)
VARIANTS = MappingProxyType({
    'HIER_PERIODS_P13_V1': (13, 26),
    'HIER_PERIODS_P26_V1': (26, 52),
    'HIER_PERIODS_P52_V1': (52, 104),
})''',
   rule='''def _scores(draws, b, cfg, second):
    P, _minimum = cfg
    L = b.high - b.low + 1
    r = Fraction(b.selected, L)
    if not second:                                   # two-pass formula, in rates
        counts = OC.period_counts(draws, b.low, b.high, P)
        n = len(next(iter(counts.values())))
        m, latest, excess = {}, {}, []
        for j, cs in counts.items():
            p = [Fraction(x, P) for x in cs]
            mj = sum(p, Fraction(0)) / n
            V = sum(((x - mj) ** 2 for x in p), Fraction(0)) / (n - 1)
            excess.append((V - (mj * (1 - mj) + V / n) / P) * Fraction(P, P - 1))
            m[j], latest[j] = mj, p[-1]
    else:                                            # second route: integer counts, sum-of-squares formula
        counts = OC.period_counts_by_index(draws, b.low, b.high, P)
        n = len(next(iter(counts.values())))
        m, latest, excess = {}, {}, []
        for j, cs in counts.items():
            total = sum(cs)
            mj = Fraction(total, n * P)
            V = Fraction(sum(x * x for x in cs) * n - total * total, n * (n - 1) * P * P)
            excess.append((V - (mj * (1 - mj) + V / n) / P) * Fraction(P, P - 1))
            m[j], latest[j] = mj, Fraction(cs[-1], P)
    t = min(max(Fraction(0), sum(excess, Fraction(0)) / L), r * (1 - r))
    w = (P * t) / ((P - 1) * t + r * (1 - r))
    return {j: w * latest[j] + (1 - w) * m[j] for j in m}'''),
 'E_9': dict(folder='E_009', name='Exponentially Decayed Occurrence Rates', probs=False, sec='3.2',
   doc='Exponentially decayed counts: s_j = the sum over the eligible draws containing j of lambda**age, the\n'
       'newest draw weighing 1. Scores only: a weighted count is not a chance.',
   table='''# variant_id: (factor lambda, minimum history)
VARIANTS = MappingProxyType({
    'EXP_DECAY_5_6_V1': (Fraction(5, 6), 1),
    'EXP_DECAY_18_19_V1': (Fraction(18, 19), 1),
    'EXP_DECAY_37_38_V1': (Fraction(37, 38), 1),
})''',
   rule='''def _scores(draws, b, cfg, second):
    lam, _minimum = cfg
    method = OC.decayed_counts_by_recursion if second else OC.decayed_counts
    return method(draws, b.low, b.high, lam)'''),
 'E_10': dict(folder='E_010', name='Multi-Horizon Frequency Contrasts', probs=False, sec='3.3',
   doc='Two-window contrast: s_j = k_j(S)/S - (k_j(Lw) - k_j(S))/(Lw - S), the rate in the newest S draws minus\n'
       'the rate in the Lw - S draws before them. Scores only: a difference of rates is not a chance.',
   table='''# variant_id: (short window S; long window Lw, or None for all eligible draws; minimum history)
VARIANTS = MappingProxyType({
    'CONTRAST_S13_L104_V1': (13, 104, 104),
    'CONTRAST_S26_L208_V1': (26, 208, 208),
    'CONTRAST_S52_FULL_V1': (52, None, 104),
})''',
   rule='''def _scores(draws, b, cfg, second):
    S, Lw, _minimum = cfg
    long = len(draws) if Lw is None else Lw
    counts = OC.window_counts_by_prefix if second else OC.window_counts
    k_short = counts(draws, b.low, b.high, S)
    k_long = counts(draws, b.low, b.high, long)
    return {j: Fraction(k_short[j], S) - Fraction(k_long[j] - k_short[j], long - S) for j in k_short}'''),
}

CONTRACT = '''"""{mid} revision 1 through the E_2-readiness contract: compute() and verify() for the shared runner.

The shared standalone runner has already checked the release rule and loaded the prefix-only view before
compute() is called. compute() reads only the view and the frozen task it is given; the contract assembles,
ranks, applies ties and validates the record (E2R-R07). Specification: {spec} section {sec}.
{doc}
With fewer eligible draws than the variant's minimum, nothing is returned and the contract records
INSUFFICIENT_HISTORY. verify() recomputes by a second, differently written route and refuses any difference.
"""
from __future__ import annotations

from fractions import Fraction

from {folder}.variants import VARIANTS
from _common import occurrence_counts as OC
from _common.contract_forecast import BarrelOutput, MethodOutput, {pv}ScoredRanking
from _common.game_profiles import get_profile

METHOD_ID = '{mid}'
OBSERVATION_VIEW = 'UNORDERED_SET'
PUBLISHES_PROBABILITIES = {probs}
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
{compute_tail}
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
{verify_tail}'''

TAIL_P = '''        out[bid] = BarrelOutput(ranking=ScoredRanking(floats),
                                probability=ProbabilityVector([floats[j] for j in sorted(floats)], PROVENANCE))'''
TAIL_S = '''        out[bid] = BarrelOutput(ranking=ScoredRanking(floats))'''
VTAIL_P = '''        if sum(s.values()) != b.selected:
            raise ValueError(f'{METHOD_ID} check: barrel {bid} does not sum to {b.selected} exactly')
        if rec['probability'].get('vector') != want:
            raise ValueError(f'{METHOD_ID} check: the probability vector differs in barrel {bid}')
'''
VTAIL_S = '''        if rec['probability'] != {'kind': 'NONE'}:
            raise ValueError(f'{METHOD_ID} check: a score-only method published a probability in barrel {bid}')
'''

for mid, m in M.items():
    d = tree / 'src' / 'methods' / m['folder']
    d.mkdir()
    files = {
        '__init__.py': f'"""{mid} - {m["name"]} (revision 1; wave 1).\n\nSpecification: {SPEC}. `variants` holds the fixed variant table and `contract` connects the method to\nthe shared contract runner. The counting is in the shared, reviewed helper _common/occurrence_counts.py\n(revision 1), which E_7, E_8, E_9 and E_10 all use. Nothing here reads a file, starts a process or touches\norchestration.\n"""\n',
        'variants.py': f'"""{mid} revision 1: the fixed variants (design note v0.1r1 section 6). Changing or adding one is a new revision."""\nfrom fractions import Fraction\nfrom types import MappingProxyType\n\n{m["table"]}\n',
        'IN_DEVELOPMENT.txt': f'{mid} is in development: the dispatch gate refuses every {mid} request while this file exists (E2R-R57).\n\nRelease is a separate, small, reviewed package that deletes this file and appends a SUPPORTED registry\nentry (E2R-R58). Deleting this file alone releases nothing.\n',
        'contract.py': CONTRACT.format(mid=mid, spec=SPEC, sec=m['sec'], doc=m['doc'], folder=m['folder'],
                                       pv='ProbabilityVector, ' if m['probs'] else '', probs=m['probs'],
                                       name=m['name'], rule=m['rule'],
                                       compute_tail=TAIL_P if m['probs'] else TAIL_S,
                                       verify_tail=VTAIL_P if m['probs'] else VTAIL_S),
    }
    for name, text in files.items():
        assert text.isascii(), (mid, name)
        with (d / name).open('x') as fh:
            fh.write(text)
    print(mid, sorted(files))
