"""WF-1B: the R3 stage-2 ranking measures MR0, MR1/MR1-T, MR4, MR5, MR7 and MR16 (R3 17.6; design 6.5).

Pure functions on invented or already-scored per-target codes. Nothing here reads a file or an outcome; every
input is passed in by the caller. N1 is not run here (design 7.1, 7.4): MR1's N1_CALIBRATED p-value and MR5's
N1 reference figure are fields set to None with label `N1_NOT_RUN` unless the caller passes them in.

INPUT CONTRACT (every measure function)
---------------------------------------
    mrX(game, targets, track_status, *, invalid_cells=None, ...)

- `game`: 'POWERBALL' or 'OZLOTTO' (otherwise ValueError).
- `targets`: a list (or tuple) of dicts, one per valid scored grid cell of ONE analysis unit, in strictly ascending
  `draw_number` order (a repeated or descending draw number raises ValueError: R3 17.3.1 fixes the order).
  * MR0, MR1, MR4, MR7, MR16 (analysis unit READOUT_TRACK) need, per target:
      `draw_number` int; `main_matches` int 0..7; `division` int (0 = none);
      Powerball: `powerball_match` int 0..1;   Oz Lotto: `supplementary_matches` int 0..min(3, 7 - m).
    `division` must equal `divisions.division(...)` of those codes.
  * MR5 (analysis unit METHOD_VARIANT_RANKING) needs, per target:
      `draw_number` int;
      `mean_rank_main`: int or Fraction, the mean of the 7 drawn labels' frozen mid-ranks (R3 3.1);
      `fair_var_main`: int or Fraction >= 0, the target's fair variance of that mean given the frozen mid-rank
          vector r: var_pop(r) x (N - 7) / (7 x (N - 1)) (R3 17.6 MR5); see `mr5_target_fields`;
      Powerball also: `rank_powerball` (int or Fraction, the drawn Powerball's mid-rank) and `fair_var_pb`
          (int or Fraction >= 0, the population variance of the 20 Powerball mid-ranks).
    The fair expectation is (N + 1)/2 per target (18 or 24 main; 10.5 Powerball), the mean of any complete
    mid-rank vector.
  A per-target value of the wrong type or out of range, or a division that disagrees with its codes, makes every
  sub-measure's status `MR_NUMERIC_INVALID` (with a `reason`) and no figure is computed (R3 17.3.7).
- `track_status`: 'GRID_COMPLETE', 'GRID_INCOMPLETE' or 'GRID_EMPTY' (design 6.2A; otherwise ValueError;
  'GRID_EMPTY' with any target is a ValueError).
- `invalid_cells`: optional {reason: count} for a GRID_INCOMPLETE track; copied to the result.
- MR1: `n1=None` or {'p_up': Fraction, 'p_lo': Fraction (optional), 'ci': (lo, hi) (optional), 'R': int}.
- MR5: `n1=None` or {'MR5.MAIN': {...}, 'MR5.PB': {...}} with the same fields (a reference figure only).

OUTPUT (every measure function)
-------------------------------
    {'measure', 'game', 'analysis_unit', 'track_status', 'n', 'first_draw', 'last_draw', 'flags',
     'invalid_cells', 'status', 'reason', 'sub_measures': {sub_measure_id: result}}

Each sub-measure result has at least: 'sub_measure', 'status' ('OK', 'MR_INSUFFICIENT_DATA',
'MR_NUMERIC_INVALID' or 'NULL_VARIANCE_ZERO'), 'n', 'flags' ('LOW_N' when 0 < n < 30; 'SELECTION_UNVERIFIED'
when the track is GRID_INCOMPLETE), 'calibration' (the label of its significance figure, or NOT_A_P_VALUE),
'descriptive_key' and 'descriptive_order' (for `rank_table`; None when the measure has no descriptive table),
'significance' (a block, below, or None) and 'significance_key' (None when undefined).

A significance block from exact tails: {'label', 'P_up', 'P_lo' (Fractions), 'P_up_output', 'P_lo_output'
(numerics.p_output), 'Z_plus', 'Z_minus' (numerics.z_plus / z_minus dicts), 'sigma_level' (0..5 or '>= 6'),
'confidence_pct' (exact Fraction 100 x (1 - P_up); display with `confidence_display`)}.
A block from a normal approximation: {'label': 'APPROX_UNCALIBRATED', 'Z' (float), 'Z_plus', 'Z_minus' (the same
dict shape), 'sigma_level'}. n = 0 gives {'label': 'MR_INSUFFICIENT_DATA'} with every figure None: no p-value and
never zero sigma.

Ranking: `rank_table(rows, key, descending=True)` gives standard competition ranks (R3 17.10.4).

READINGS (where R3 or the design needed a reading; each is listed in the WF-1B coding report):
- M-R1 Labels on a GRID_INCOMPLETE track: R3 17.3.7A downgrades "EXACT_LOCAL, N1_CALIBRATED, guaranteed
  Bonferroni" to SELECTION_UNVERIFIED. Those labels are replaced; APPROX_UNCALIBRATED, N1_FIXED_FORECAST_REFERENCE
  and NOT_A_P_VALUE keep their label (they claim no calibration) and the sub-measure carries the flag
  SELECTION_UNVERIFIED. n = 0 (any status) gives MR_INSUFFICIENT_DATA.
- M-R2 Significance keys are the float Z_plus (R3: "Z_plus descending"; 17.10.4: floats compared at full float64
  equality). MR4 breaks ties by k_S descending. A SIGMA_ABOVE_BOUND sigma sorts as +infinity.
- M-R3 Undefined keys (None: MR_INSUFFICIENT_DATA, MR_NUMERIC_INVALID, NULL_VARIANCE_ZERO) are never sorted as
  zero: `rank_table` lists them after every defined row, sharing one rank, flagged 'undefined'.
- M-R4 MR0's key is (W_1, ..., W_D, MR1). WF-1's tables are OWN_SET (design WF1-6), where R3 breaks equal V by MR1
  descending; on a common set equal V implies equal MR1, so the same key serves both.
- M-R5 MR1 is a sum of logarithms; it is compared exactly by `MR1Key` (design 7.4: products of p_d powers), with
  an 80-digit decimal shortcut used only when the decimal difference is far from zero.
- M-R6 MR4 sub-measures: X.d and C.d for every d, plus B.2-3. The owner's C.3 (R8) and X.3 (R10) are the same
  tests as the generic C.3 and X.3, so they are one row each, tagged 'owner_ref'; B.2-3 is tagged R9. The owner's
  sets are produced in both games, as R3 lists them without a game restriction.
- M-R7 MR5: the per-target expectation is (N + 1)/2 (mid-ranks of a complete ranking always average that). The PB
  channel uses R3's main formula with K = 1, which is the population variance of the 20 Powerball mid-ranks.
  Z = (sum expected - sum observed)/sqrt(sum variances), so ranking drawn numbers higher (lower ranks) is positive;
  Z_plus = max(0, Z), Z_minus = max(0, -Z). A zero variance sum gives NULL_VARIANCE_ZERO with no sigma.
- M-R8 MR7 above n = 1000: the exact figure is labelled MR_EXACT_BOUND_EXCEEDED (P_up, P_lo None) and the normal
  approximation Z = (S - n x mean0)/sqrt(n x Var0) (no continuity correction, no p-value) is shown beside it,
  labelled APPROX_UNCALIBRATED; the significance key then uses that Z_plus. The PB channel stays exact (binomial).
- M-R9 MR16's 3-sigma threshold uses R3's literal 0.00134990 (as the design's reference script does), not Q(3).
  If no k <= n reaches it, k_3, the threshold ratio and the powers are None with 'k_3_status' MR_UNDEFINED.
- M-R10 MR16 shows P_up and Z_plus only (R3's output list). Its division events are the same tests as MR4
  (PDd/ODd = MR4.X.d; ANYDIV = MR4.C.D) and MR16.PB is the same tail as MR7.PB; such rows carry 'same_test_as'
  and 'counts_in_M': False (R3 17.6 MR16; 17.3.4A "each distinct hypothesis is counted once in M").
- M-R11 MR1-T uses the exact weights 90/100, 7/100, 3/100. MR1 and MR1-T raw scores are NOT_A_P_VALUE; MR1's Z is
  APPROX_UNCALIBRATED and its significance key is the N1 Z_plus when an N1 p-value is passed, else the approximate.
- M-R12 MR5's analysis unit is METHOD_VARIANT_RANKING; the other five are READOUT_TRACK (R3 17.3.4A).
"""
from __future__ import annotations

import math
from decimal import Context, Decimal
from fractions import Fraction
from functools import lru_cache

from . import divisions as DV
from . import numerics as NU

TRACK_STATUSES = ('GRID_COMPLETE', 'GRID_INCOMPLETE', 'GRID_EMPTY')
LOW_N_THRESHOLD = 30                          # MRD-19
MR7_EXACT_MAX_N = 1000                        # design 6.6
THREE_SIGMA_P_UP = Fraction('0.00134990')     # R3 17.6 MR16 (M-R9)
MR1T_WEIGHTS = (Fraction(90, 100), Fraction(7, 100), Fraction(3, 100))
DIV_PREFIX = {DV.POWERBALL: 'PD', DV.OZLOTTO: 'OD'}
OWNER_MR4 = {'MR4.C.3': 'R8', 'MR4.B.2-3': 'R9', 'MR4.X.3': 'R10'}

_DEC = Context(prec=80)


def _dec(x) -> Decimal:
    if isinstance(x, Fraction):
        return _DEC.divide(Decimal(x.numerator), Decimal(x.denominator))
    return Decimal(x)


_LN2 = _DEC.ln(Decimal(2))


def _bits(p: Fraction) -> Decimal:
    """-log2 p at 80 digits."""
    return _DEC.divide(-_DEC.ln(_dec(p)), _LN2)


# ---------------------------------------------------------------- MR1 constants (R3 17.6 MR1)

BITS = {g: {d: _bits(p) for d, p in DV.division_probabilities(g).items()} for g in DV.GAMES}


def _e0_sd(game: str) -> tuple[Decimal, Decimal]:
    p = DV.division_probabilities(game)
    e0 = sum((_dec(p[d]) * BITS[game][d] for d in p), Decimal(0))
    e2 = sum((_dec(p[d]) * BITS[game][d] * BITS[game][d] for d in p), Decimal(0))
    return e0, _DEC.sqrt(e2 - e0 * e0)


MR1_E0 = {g: _e0_sd(g)[0] for g in DV.GAMES}   # 0.153679 (Powerball), 0.131326 (Oz Lotto) bits per draw
MR1_SD = {g: _e0_sd(g)[1] for g in DV.GAMES}   # 1.025914, 0.931722


class MR1Key:
    """Exact comparison key for MR1 = (1/n) x sum_d W_d x (-log2 p_d) (design 7.4; M-R5).

    MR1_a > MR1_b  <=>  sum_d e_d x (-log2 p_d) > 0 with e_d = W_a,d x n_b - W_b,d x n_a
                   <=>  prod_d p_d ** e_d < 1, decided with exact Fractions when the decimal value is near 0."""

    __slots__ = ('game', 'counts', 'n')
    __hash__ = None  # type: ignore[assignment]

    def __init__(self, game: str, counts, n: int):
        if game not in DV.GAMES or type(n) is not int or n < 1:
            raise ValueError('MR1Key needs a game and n >= 1')
        self.game, self.counts, self.n = game, tuple(counts), n

    def _cmp(self, other: 'MR1Key') -> int:
        if not isinstance(other, MR1Key) or other.game != self.game:
            raise TypeError('MR1Key compares only with an MR1Key of the same game')
        e = [a * other.n - b * self.n for a, b in zip(self.counts, other.counts)]
        if not any(e):
            return 0
        bits = BITS[self.game]
        est = sum((ed * bits[d] for d, ed in enumerate(e, 1)), Decimal(0))
        if abs(est) > Decimal('1e-50'):
            return 1 if est > 0 else -1
        p = DV.division_probabilities(self.game)
        prod = Fraction(1)
        for d, ed in enumerate(e, 1):
            if ed:
                prod *= p[d] ** ed
        return 0 if prod == 1 else (1 if prod < 1 else -1)

    def __eq__(self, other):
        return self._cmp(other) == 0 if isinstance(other, MR1Key) else NotImplemented

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __le__(self, other):
        return self._cmp(other) <= 0

    def __gt__(self, other):
        return self._cmp(other) > 0

    def __ge__(self, other):
        return self._cmp(other) >= 0

    def value(self) -> float:
        tot = sum((w * BITS[self.game][d] for d, w in enumerate(self.counts, 1)), Decimal(0))
        return float(_DEC.divide(tot, Decimal(self.n)))

    def __repr__(self) -> str:
        return f'MR1Key({self.game}, {self.counts}, n={self.n})'


# ---------------------------------------------------------------- input checks and shared blocks

def _num_ok(v) -> bool:
    return type(v) is int or type(v) is Fraction


def _prepare(game: str, targets, track_status: str, kind: str, invalid_cells) -> dict:
    if game not in DV.GAMES:
        raise ValueError(f'unknown game {game!r}')
    if track_status not in TRACK_STATUSES:
        raise ValueError(f'unknown track status {track_status!r}')
    if not isinstance(targets, (list, tuple)) or any(type(t) is not dict for t in targets):
        raise ValueError('targets must be a list of dicts')
    prev = None
    for t in targets:
        dn = t.get('draw_number')
        if type(dn) is not int:
            raise ValueError('every target needs an int draw_number')
        if prev is not None and dn <= prev:
            raise ValueError('targets must be in strictly ascending draw_number order')
        prev = dn
    n = len(targets)
    if track_status == 'GRID_EMPTY' and n:
        raise ValueError('a GRID_EMPTY track has no valid cell, so no target')
    reason = _check_match(game, targets) if kind == 'match' else _check_rank(game, targets)
    flags = []
    if 0 < n < LOW_N_THRESHOLD:
        flags.append('LOW_N')
    if track_status == 'GRID_INCOMPLETE':
        flags.append('SELECTION_UNVERIFIED')
    status = 'MR_NUMERIC_INVALID' if reason else ('MR_INSUFFICIENT_DATA' if n == 0 else 'OK')
    return {'game': game, 'track_status': track_status, 'n': n, 'flags': flags, 'status': status,
            'reason': reason, 'first_draw': targets[0]['draw_number'] if n else None,
            'last_draw': targets[-1]['draw_number'] if n else None,
            'invalid_cells': dict(invalid_cells) if invalid_cells else {}}


def _check_match(game: str, targets) -> str | None:
    for t in targets:
        try:
            if game == DV.POWERBALL:
                d = DV.division(game, t.get('main_matches'), powerball_match=t.get('powerball_match'))
            else:
                d = DV.division(game, t.get('main_matches'), supplementary_matches=t.get('supplementary_matches'))
        except ValueError as exc:
            return f"draw {t['draw_number']}: {exc}"
        if type(t.get('division')) is not int or t['division'] != d:
            return f"draw {t['draw_number']}: division {t.get('division')!r} disagrees with its codes ({d})"
    return None


def _check_rank(game: str, targets) -> str | None:
    big_n = DV.MAIN_POOL[game]
    for t in targets:
        r, v = t.get('mean_rank_main'), t.get('fair_var_main')
        if not (_num_ok(r) and 1 <= r <= big_n and (Fraction(r) * 14).denominator == 1):
            return f"draw {t['draw_number']}: invalid mean_rank_main {r!r}"
        if not (_num_ok(v) and v >= 0):
            return f"draw {t['draw_number']}: invalid fair_var_main {v!r}"
        if game == DV.POWERBALL:
            q, w = t.get('rank_powerball'), t.get('fair_var_pb')
            if not (_num_ok(q) and 1 <= q <= DV.PB_POOL and (Fraction(q) * 2).denominator == 1):
                return f"draw {t['draw_number']}: invalid rank_powerball {q!r}"
            if not (_num_ok(w) and w >= 0):
                return f"draw {t['draw_number']}: invalid fair_var_pb {w!r}"
    return None


def _result(measure: str, unit: str, ctx: dict) -> dict:
    return {'measure': measure, 'game': ctx['game'], 'analysis_unit': unit, 'track_status': ctx['track_status'],
            'n': ctx['n'], 'first_draw': ctx['first_draw'], 'last_draw': ctx['last_draw'],
            'flags': list(ctx['flags']), 'invalid_cells': dict(ctx['invalid_cells']), 'status': ctx['status'],
            'reason': ctx['reason'], 'sub_measures': {}}


def _sub(sub_id: str, ctx: dict, calibration: str, descriptive_order: str | None) -> dict:
    return {'sub_measure': sub_id, 'status': ctx['status'], 'n': ctx['n'], 'flags': list(ctx['flags']),
            'calibration': _label(calibration, ctx), 'descriptive_key': None,
            'descriptive_order': descriptive_order, 'significance': None, 'significance_key': None}


def _label(base: str, ctx: dict) -> str:
    if base == 'NOT_A_P_VALUE':
        return base
    if ctx['status'] == 'MR_INSUFFICIENT_DATA':
        return 'MR_INSUFFICIENT_DATA'
    if ctx['status'] == 'MR_NUMERIC_INVALID':
        return 'MR_NUMERIC_INVALID'
    if base in ('EXACT_LOCAL', 'N1_CALIBRATED') and ctx['track_status'] == 'GRID_INCOMPLETE':
        return 'SELECTION_UNVERIFIED'
    return base


def sigma_level(z: dict | None):
    """floor(Z_plus) shown as 0..5 or '>= 6' (R3 17.5.1); None when there is no sigma."""
    if z is None or z.get('sigma') is None:
        return None
    if z.get('label') == 'SIGMA_ABOVE_BOUND' or z['sigma'] >= 6:
        return '>= 6'
    return int(math.floor(z['sigma']))


def _sigma_key(z: dict | None):
    if z is None or z.get('sigma') is None:
        return None
    if z.get('label') == 'SIGMA_ABOVE_BOUND':
        return math.inf
    return z['sigma']


def _empty_block(label: str) -> dict:
    return {'label': label, 'P_up': None, 'P_lo': None, 'P_up_output': None, 'P_lo_output': None,
            'Z_plus': None, 'Z_minus': None, 'sigma_level': None, 'confidence_pct': None}


def _exact_block(p_up: Fraction, p_lo: Fraction | None, base: str, ctx: dict) -> dict:
    zp = NU.z_plus(p_up)
    return {'label': _label(base, ctx), 'P_up': p_up, 'P_lo': p_lo,
            'P_up_output': NU.p_output(p_up), 'P_lo_output': NU.p_output(p_lo) if p_lo is not None else None,
            'Z_plus': zp, 'Z_minus': NU.z_minus(p_lo) if p_lo is not None else None,
            'sigma_level': sigma_level(zp), 'confidence_pct': 100 * (1 - p_up)}


def _approx_block(num: Decimal, den: Decimal, ctx: dict) -> dict:
    """Z = num / den with den > 0, at 80 digits, converted once to float64 (APPROX_UNCALIBRATED)."""
    z = float(_DEC.divide(num, den))
    zp = {'sigma': max(0.0, z) + 0.0, 'label': None}
    zm = {'sigma': max(0.0, -z) + 0.0, 'label': None}
    return {'label': _label('APPROX_UNCALIBRATED', ctx), 'Z': z, 'Z_plus': zp, 'Z_minus': zm,
            'sigma_level': sigma_level(zp)}


def _n1_block(n1: dict | None, base: str, ctx: dict) -> dict:
    if n1 is None or ctx['status'] != 'OK':
        out = _empty_block('N1_NOT_RUN' if ctx['status'] == 'OK' else _label(base, ctx))
        out.update({'ci': None, 'R': None, 'k': None})
        return out
    p_up = n1['p_up']
    if not isinstance(p_up, Fraction) or not 0 < p_up <= 1:
        raise ValueError('an N1 p-value must be a Fraction in (0, 1]')
    out = _exact_block(p_up, n1.get('p_lo'), base, ctx)
    out.update({'ci': n1.get('ci'), 'R': n1.get('R'), 'k': n1.get('k')})
    return out


def confidence_display(p_up: Fraction, decimals: int = 5) -> str:
    """One-sided reference confidence 100 x (1 - P_up)%, rounded DOWN (R3 17.5.1), so a nonzero P_up is never
    shown as 100%."""
    if not isinstance(p_up, Fraction) or not 0 <= p_up <= 1:
        raise ValueError('p_up must be a Fraction in [0, 1]')
    scaled = (100 * (1 - p_up)) * 10 ** decimals
    q = scaled.numerator // scaled.denominator
    whole, frac = divmod(q, 10 ** decimals)
    return f'{whole}.{frac:0{decimals}d}%' if decimals else f'{whole}%'


def bonferroni(p_up: Fraction, m: int) -> dict:
    """P_Bonf = min(1, M x P_up) and its Z_plus (R3 17.5.3). The label (guaranteed or
    BONFERRONI_REFERENCE_UNCALIBRATED) depends on the family and is set by the caller (design 6.2A)."""
    if type(m) is not int or m < 1:
        raise ValueError('M must be an int >= 1')
    p = min(Fraction(1), m * p_up)
    return {'M': m, 'P_bonf': p, 'P_bonf_output': NU.p_output(p), 'Z_plus': NU.z_plus(p)}


def _division_counts(game: str, targets) -> tuple[int, ...]:
    w = [0] * DV.DIVISION_COUNT[game]
    for t in targets:
        if t['division']:
            w[t['division'] - 1] += 1
    return tuple(w)


# ---------------------------------------------------------------- MR0 - division win profile

def mr0(game: str, targets, track_status: str, *, invalid_cells=None) -> dict:
    """MR0: V = (W_1..W_D); ranking V descending, lexicographic, then MR1 descending (M-R4). NOT_A_P_VALUE."""
    ctx = _prepare(game, targets, track_status, 'match', invalid_cells)
    res = _result('MR0', 'READOUT_TRACK', ctx)
    sub = _sub('MR0', ctx, 'NOT_A_P_VALUE', 'descending')
    n = ctx['n']
    if ctx['status'] == 'OK':
        w = _division_counts(game, targets)
        p = DV.division_probabilities(game)
        sub.update({'W': w, 'expected': {d: n * p[d] for d in p},
                    'descriptive_key': w + (MR1Key(game, w, n),)})
    res['sub_measures']['MR0'] = sub
    return res


# ---------------------------------------------------------------- MR1 and MR1-T

def mr1(game: str, targets, track_status: str, *, invalid_cells=None, n1: dict | None = None) -> dict:
    """MR1 (mean surprisal bits per draw) with its APPROX_UNCALIBRATED Z and the N1 slot; MR1-T (90/7/3)."""
    ctx = _prepare(game, targets, track_status, 'match', invalid_cells)
    res = _result('MR1', 'READOUT_TRACK', ctx)
    n = ctx['n']
    e0, sd = MR1_E0[game], MR1_SD[game]
    s1 = _sub('MR1', ctx, 'NOT_A_P_VALUE', 'descending')
    s1.update({'E0': float(e0), 'sd0': float(sd), 'MR1': None, 'difference': None, 'sum_bits': None,
               'approx': _empty_block(_label('APPROX_UNCALIBRATED', ctx)), 'n1': _n1_block(None, 'N1_CALIBRATED', ctx)})
    st = _sub('MR1-T', ctx, 'NOT_A_P_VALUE', 'descending')
    st.update({'MR1-T': None, 'MR1-T_float': None})
    if ctx['status'] == 'OK':
        w = _division_counts(game, targets)
        total = sum((wd * BITS[game][d] for d, wd in enumerate(w, 1)), Decimal(0))
        mr1v = _DEC.divide(total, Decimal(n))
        approx = _approx_block(total - n * e0, _DEC.sqrt(Decimal(n)) * sd, ctx)
        n1b = _n1_block(n1, 'N1_CALIBRATED', ctx)
        sig = n1b if n1 is not None else approx
        s1.update({'W': w, 'MR1': float(mr1v), 'difference': float(mr1v - e0), 'sum_bits': float(total),
                   'approx': approx, 'n1': n1b, 'significance': sig, 'calibration_significance': sig['label'],
                   'descriptive_key': MR1Key(game, w, n), 'significance_key': _sigma_key(sig['Z_plus'])})
        mr1t = (MR1T_WEIGHTS[0] * w[0] + MR1T_WEIGHTS[1] * w[1] + MR1T_WEIGHTS[2] * w[2]) / n
        st.update({'MR1-T': mr1t, 'MR1-T_float': float(mr1t), 'descriptive_key': mr1t})
    res['sub_measures']['MR1'] = s1
    res['sub_measures']['MR1-T'] = st
    return res


# ---------------------------------------------------------------- MR4 - division sigma

def mr4_sets(game: str) -> list[tuple[str, frozenset]]:
    """[(sub-measure ID, division set)]: X.1..X.D, C.1..C.D, B.2-3 (M-R6)."""
    dmax = DV.DIVISION_COUNT[game]
    out = [(f'MR4.X.{d}', frozenset({d})) for d in range(1, dmax + 1)]
    out += [(f'MR4.C.{d}', frozenset(range(1, d + 1))) for d in range(1, dmax + 1)]
    out.append(('MR4.B.2-3', frozenset({2, 3})))
    return out


def mr4(game: str, targets, track_status: str, *, invalid_cells=None) -> dict:
    """MR4: k_S wins in division set S, X ~ Binomial(n, p_S); exact P_up and P_lo (EXACT_LOCAL)."""
    ctx = _prepare(game, targets, track_status, 'match', invalid_cells)
    res = _result('MR4', 'READOUT_TRACK', ctx)
    n = ctx['n']
    for sid, dset in mr4_sets(game):
        sub = _sub(sid, ctx, 'EXACT_LOCAL', None)
        p_s = DV.division_set_probability(game, dset)
        sub.update({'divisions': tuple(sorted(dset)), 'p_S': p_s, 'owner_ref': OWNER_MR4.get(sid),
                    'k_S': None, 'expected': n * p_s if n else None,
                    'significance': _empty_block(_label('EXACT_LOCAL', ctx))})
        if ctx['status'] == 'OK':
            k = sum(1 for t in targets if t['division'] in dset)
            blk = _exact_block(NU.binom_upper(n, p_s, k), NU.binom_lower(n, p_s, k), 'EXACT_LOCAL', ctx)
            sub.update({'k_S': k, 'significance': blk, 'significance_key': (_sigma_key(blk['Z_plus']), k)})
        res['sub_measures'][sid] = sub
    return res


# ---------------------------------------------------------------- MR5 - rank position

def mid_ranks_from_groups(groups, n_labels: int) -> dict[int, Fraction]:
    """R3 3.1 / 2.x: mid-ranks from frozen ranked tie groups (best first). A group of g labels occupying
    positions s..s+g-1 gives each label the rank s + (g - 1)/2. Every label 1..n_labels must appear once."""
    out: dict[int, Fraction] = {}
    pos = 1
    for g in groups:
        g = list(g)
        if not g:
            raise ValueError('empty tie group')
        r = Fraction(2 * pos + len(g) - 1, 2)
        for label in g:
            if type(label) is not int or not 1 <= label <= n_labels or label in out:
                raise ValueError(f'invalid or repeated label {label!r}')
            out[label] = r
        pos += len(g)
    if len(out) != n_labels:
        raise ValueError('the groups must cover every label exactly once')
    return out


def _check_mid_ranks(ranks: dict, n_labels: int) -> list[Fraction]:
    if set(ranks) != set(range(1, n_labels + 1)):
        raise ValueError('mid-ranks must cover every label exactly once')
    vals = sorted(Fraction(ranks[j]) for j in ranks)
    i = 0
    while i < n_labels:
        j = i
        while j + 1 < n_labels and vals[j + 1] == vals[i]:
            j += 1
        if vals[i] != Fraction(2 * (i + 1) + (j - i), 2):
            raise ValueError('not a valid mid-rank vector')
        i = j + 1
    return vals


def _pop_var(vals: list[Fraction]) -> Fraction:
    m = sum(vals, Fraction(0)) / len(vals)
    return sum(((v - m) ** 2 for v in vals), Fraction(0)) / len(vals)


def mr5_target_fields(game: str, main_mid_ranks: dict, drawn_main, pb_mid_ranks: dict | None = None,
                      drawn_pb: int | None = None) -> dict:
    """The per-target MR5 inputs from one frozen mid-rank vector and one opened draw (R3 3.1; R3 17.6 MR5):
    mean_rank_main, fair_var_main = var_pop(r) x (N - 7)/(7 x (N - 1)); Powerball also rank_powerball and
    fair_var_pb = var_pop(q). `main_mid_ranks` and `pb_mid_ranks` map label -> mid-rank (int or Fraction)."""
    if game not in DV.GAMES:
        raise ValueError(f'unknown game {game!r}')
    big_n = DV.MAIN_POOL[game]
    vals = _check_mid_ranks(main_mid_ranks, big_n)
    drawn = DV._labels(drawn_main, 'drawn_main', 7, big_n)
    out = {'mean_rank_main': sum((Fraction(main_mid_ranks[j]) for j in drawn), Fraction(0)) / 7,
           'fair_var_main': _pop_var(vals) * (big_n - 7) / (7 * (big_n - 1))}
    if game == DV.POWERBALL:
        qv = _check_mid_ranks(pb_mid_ranks or {}, DV.PB_POOL)
        dpb = DV._int(drawn_pb, 'drawn_pb', 1, DV.PB_POOL)
        out['rank_powerball'] = Fraction(pb_mid_ranks[dpb])
        out['fair_var_pb'] = _pop_var(qv)
    elif pb_mid_ranks is not None or drawn_pb is not None:
        raise ValueError('Oz Lotto has no Powerball channel')
    return out


def mr5(game: str, targets, track_status: str, *, invalid_cells=None, n1: dict | None = None) -> dict:
    """MR5.MAIN (and MR5.PB): mean frozen mid-rank of the drawn labels; Z APPROX_UNCALIBRATED; N1 reference slot
    (N1_FIXED_FORECAST_REFERENCE, never N1_CALIBRATED). Analysis unit METHOD_VARIANT_RANKING."""
    ctx = _prepare(game, targets, track_status, 'rank', invalid_cells)
    res = _result('MR5', 'METHOD_VARIANT_RANKING', ctx)
    n = ctx['n']
    chans = [('MR5.MAIN', 'mean_rank_main', 'fair_var_main', Fraction(DV.MAIN_POOL[game] + 1, 2))]
    if game == DV.POWERBALL:
        chans.append(('MR5.PB', 'rank_powerball', 'fair_var_pb', Fraction(DV.PB_POOL + 1, 2)))
    for sid, fobs, fvar, expect in chans:
        sub = _sub(sid, ctx, 'APPROX_UNCALIBRATED', 'ascending')
        sub.update({'expectation': expect, 'MR5': None, 'MR5_float': None, 'sum_variance': None,
                    'significance': _empty_block(_label('APPROX_UNCALIBRATED', ctx)),
                    'n1_reference': _n1_block(None, 'N1_FIXED_FORECAST_REFERENCE', ctx)})
        if ctx['status'] == 'OK':
            obs = sum((Fraction(t[fobs]) for t in targets), Fraction(0))
            var = sum((Fraction(t[fvar]) for t in targets), Fraction(0))
            mean = obs / n
            sub.update({'MR5': mean, 'MR5_float': float(mean), 'sum_variance': var, 'descriptive_key': mean,
                        'n1_reference': _n1_block((n1 or {}).get(sid), 'N1_FIXED_FORECAST_REFERENCE', ctx)})
            if var == 0:
                sub['status'] = 'NULL_VARIANCE_ZERO'
                sub['calibration'] = 'NULL_VARIANCE_ZERO'
                sub['significance'] = _empty_block('NULL_VARIANCE_ZERO')
            else:
                blk = _approx_block(_dec(n * expect - obs), _DEC.sqrt(_dec(var)), ctx)
                sub.update({'significance': blk, 'significance_key': _sigma_key(blk['Z_plus'])})
        res['sub_measures'][sid] = sub
    return res


# ---------------------------------------------------------------- MR7 - total main-match excess

def mr7(game: str, targets, track_status: str, *, invalid_cells=None) -> dict:
    """MR7.MAIN: S = sum of m_t with the exact null A_G(z)^n (n <= 1000); MR7.PB: B ~ Binomial(n, 1/20)."""
    ctx = _prepare(game, targets, track_status, 'match', invalid_cells)
    res = _result('MR7', 'READOUT_TRACK', ctx)
    n = ctx['n']
    mean0, var0 = DV.MEAN0[game], DV.VAR0[game]
    sub = _sub('MR7.MAIN', ctx, 'EXACT_LOCAL', 'descending')
    sub.update({'S': None, 'S_per_draw': None, 'mean0': mean0, 'var0': var0, 'excess': None,
                'significance': _empty_block(_label('EXACT_LOCAL', ctx)), 'approx': None})
    if ctx['status'] == 'OK':
        s = sum(t['main_matches'] for t in targets)
        excess = s - n * mean0
        sub.update({'S': s, 'S_per_draw': Fraction(s, n), 'excess': excess, 'descriptive_key': excess})
        tails = None
        if n <= MR7_EXACT_MAX_N:
            try:
                tails = NU.mr7_tails(game, n, s)
            except ValueError as exc:
                if 'MR_EXACT_BOUND_EXCEEDED' not in str(exc):
                    raise
        if tails is not None:
            blk = _exact_block(tails[0], tails[1], 'EXACT_LOCAL', ctx)
            sub.update({'significance': blk, 'significance_key': _sigma_key(blk['Z_plus'])})
        else:
            approx = _approx_block(_dec(excess), _DEC.sqrt(_dec(n * var0)), ctx)
            sub.update({'status': 'MR_EXACT_BOUND_EXCEEDED', 'calibration': 'MR_EXACT_BOUND_EXCEEDED',
                        'significance': _empty_block('MR_EXACT_BOUND_EXCEEDED'), 'approx': approx,
                        'significance_key': _sigma_key(approx['Z_plus'])})
    res['sub_measures']['MR7.MAIN'] = sub
    if game == DV.POWERBALL:
        p = DV.PB_HIT_PROBABILITY
        pb = _sub('MR7.PB', ctx, 'EXACT_LOCAL', 'descending')
        pb.update({'B': None, 'B_per_draw': None, 'mean0': p, 'var0': DV.PB_HIT_VARIANCE, 'excess': None,
                   'significance': _empty_block(_label('EXACT_LOCAL', ctx))})
        if ctx['status'] == 'OK':
            b = sum(t['powerball_match'] for t in targets)
            blk = _exact_block(NU.binom_upper(n, p, b), NU.binom_lower(n, p, b), 'EXACT_LOCAL', ctx)
            pb.update({'B': b, 'B_per_draw': Fraction(b, n), 'excess': b - n * p, 'descriptive_key': b - n * p,
                       'significance': blk, 'significance_key': _sigma_key(blk['Z_plus'])})
        res['sub_measures']['MR7.PB'] = pb
    return res


# ---------------------------------------------------------------- MR16 - hit-rate estimate

def _mr16_events(game: str) -> list[tuple[str, Fraction, object, str | None]]:
    """[(sub-measure ID, fair p, event(target) -> bool, same_test_as)]."""
    dmax = DV.DIVISION_COUNT[game]
    pre = DIV_PREFIX[game]
    pd = DV.division_probabilities(game)
    ev = [('MR16.ANYDIV', DV.any_division_probability(game), lambda t: t['division'] >= 1, f'MR4.C.{dmax}')]
    for d in range(1, dmax + 1):
        ev.append((f'MR16.{pre}{d}', pd[d], (lambda t, d=d: t['division'] == d), f'MR4.X.{d}'))
    for j in (2, 3, 4):
        ev.append((f'MR16.M{j}', DV.main_match_at_least(game, j), (lambda t, j=j: t['main_matches'] >= j), None))
    if game == DV.POWERBALL:
        ev.append(('MR16.PB', DV.PB_HIT_PROBABILITY, lambda t: t['powerball_match'] == 1, 'MR7.PB'))
    return ev


@lru_cache(maxsize=4096)
def mr16_threshold(n: int, p: Fraction) -> dict:
    """k_3 = the smallest k with P(X >= k) <= 0.00134990, X ~ Binomial(n, p); the threshold ratio k_3/(n p); the
    power P(X >= k_3) at min(1, c p) for c = 1.5 and 2 (R3 17.6 MR16; M-R9). Depends only on (n, p)."""
    if type(n) is not int or n < 1 or not isinstance(p, Fraction) or not 0 < p < 1:
        raise ValueError('mr16_threshold needs n >= 1 and 0 < p < 1')
    if NU.binom_upper(n, p, n) > THREE_SIGMA_P_UP:
        return {'k_3': None, 'k_3_status': 'MR_UNDEFINED', 'threshold_ratio': None,
                'power_1_5x': None, 'power_2x': None}
    lo, hi = 0, n            # P(X >= lo) > T (lo = 0 gives 1), P(X >= hi) <= T
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if NU.binom_upper(n, p, mid) <= THREE_SIGMA_P_UP:
            hi = mid
        else:
            lo = mid
    k3 = hi

    def power(c: Fraction) -> Fraction:
        q = min(Fraction(1), c * p)
        return Fraction(1) if q == 1 else NU.binom_upper(n, q, k3)
    return {'k_3': k3, 'k_3_status': 'OK', 'threshold_ratio': Fraction(k3) / (n * p),
            'power_1_5x': power(Fraction(3, 2)), 'power_2x': power(Fraction(2))}


def mr16(game: str, targets, track_status: str, *, invalid_cells=None) -> dict:
    """MR16: per success event, k/n with the Clopper-Pearson 95% interval, exact P_up (EXACT_LOCAL), k_3, the
    threshold ratio and the power at 1.5x and 2x."""
    ctx = _prepare(game, targets, track_status, 'match', invalid_cells)
    res = _result('MR16', 'READOUT_TRACK', ctx)
    n = ctx['n']
    for sid, p, event, same in _mr16_events(game):
        sub = _sub(sid, ctx, 'EXACT_LOCAL', 'descending')
        sub.update({'p': p, 'expected': n * p if n else None, 'k': None, 'rate': None, 'interval': None,
                    'interval_label': 'CONSTANT_RATE_REFERENCE_INTERVAL', 'same_test_as': same,
                    'counts_in_M': same is None, 'k_3': None, 'k_3_status': None, 'threshold_ratio': None,
                    'power_1_5x': None, 'power_2x': None,
                    'significance': _empty_block(_label('EXACT_LOCAL', ctx))})
        if ctx['status'] == 'OK':
            k = sum(1 for t in targets if event(t))
            ci = NU.clopper_pearson(k, n)
            blk = _exact_block(NU.binom_upper(n, p, k), None, 'EXACT_LOCAL', ctx)
            sub.update({'k': k, 'rate': Fraction(k, n), 'interval': ci, 'descriptive_key': ci[0],
                        'significance': blk, 'significance_key': _sigma_key(blk['Z_plus'])})
            sub.update(mr16_threshold(n, p))
        res['sub_measures'][sid] = sub
    return res


# ---------------------------------------------------------------- league-table ranks (R3 17.10.4)

def rank_table(rows, key, descending: bool = True) -> list[dict]:
    """Standard competition ranking ("1=, 1=, 3"), ties listed by track ID (R3 17.10.4).

    `rows`: dicts each with a unique str 'track_id'. `key`: a field name or a callable(row) -> key; keys are
    compared exactly (ints, Fractions, tuples, MR1Key; floats at full float64 equality). A None key is undefined:
    such rows follow every defined row, share one rank and are flagged 'undefined' (never sorted as zero; M-R3).
    Returns [{'rank', 'display', 'tied', 'undefined', 'track_id', 'key', 'row'}] in table order."""
    rows = list(rows)
    ids = [r.get('track_id') if isinstance(r, dict) else None for r in rows]
    if any(type(i) is not str for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('every row needs a unique str track_id')
    get = key if callable(key) else (lambda r: r.get(key))
    keyed = [(get(r), r) for r in rows]
    for k, _ in keyed:
        if isinstance(k, float) and math.isnan(k):
            raise ValueError('a ranking key may not be NaN')
    defined = sorted((x for x in keyed if x[0] is not None), key=lambda x: x[1]['track_id'])
    defined.sort(key=lambda x: x[0], reverse=descending)          # stable: ties stay in track-ID order
    undefined = sorted((x for x in keyed if x[0] is None), key=lambda x: x[1]['track_id'])
    out: list[dict] = []
    for i, (k, r) in enumerate(defined):
        rank = out[-1]['rank'] if i and k == defined[i - 1][0] else i + 1
        out.append({'rank': rank, 'key': k, 'row': r, 'track_id': r['track_id'], 'undefined': False})
    base = len(defined) + 1
    for k, r in undefined:
        out.append({'rank': base, 'key': None, 'row': r, 'track_id': r['track_id'], 'undefined': True})
    counts: dict[int, int] = {}
    for e in out:
        counts[e['rank']] = counts.get(e['rank'], 0) + 1
    for e in out:
        e['tied'] = counts[e['rank']] > 1
        e['display'] = f"{e['rank']}=" if e['tied'] else str(e['rank'])
    return out
