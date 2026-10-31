"""WF-1B: per-draw match record, prize-division classification and fair-draw moments (R3 17.4; R2 2.5; R3 17.8).

Evaluator-only code. It reads no file and no outcome: callers pass the numbers in. Every probability is an exact
`fractions.Fraction` built from integer combinatorial counts (R3 17.11; design 6.6).

Contents:
- the game constants (R3 17.3.4: Powerball 7 of 35 plus 1 of 20; Oz Lotto 7 of 47, with 3 supplementaries drawn
  from the same barrel);
- the exact division probabilities p_d and integer outcome counts (R3 17.4.2, 17.4.3);
- `division(game, main_matches, powerball_match=None, supplementary_matches=None)`, 0 = no prize;
- `match_record(game, ticket_main, ticket_pb, drawn_main, drawn_pb_or_supps)`, the per-draw match record. For
  Oz Lotto the drawn supplementaries determine only `supplementary_matches` and the division; they are never
  returned or stored (R2 2.5, R3 17.8, design 6.3);
- the one-draw main-match law and the fair-draw moments of R3 17.4.4 (mean0, Var0, the Powerball hit law).

The classifier agrees with the installed `validate_score_record` (src/methods/_common/contract_receipts.py):
Powerball division 0..9 from (m, b); Oz Lotto division 0..7 from (m, s) with 0 <= s <= min(3, 7 - m).

READINGS (where R3's text needed a reading; each is listed in the WF-1B coding report):
- D-R1: Oz Lotto OD2 is "m = 6, s = 1" and OD4/OD7 are "s >= 1". With m = 6 only s <= 1 is possible, so OD2 is
  classified as m = 6 and s >= 1, which is the same set.
- D-R2: `match_record` returns only the three per-draw codes (main_matches, powerball_match or
  supplementary_matches, division). The caller adds identity fields (game_id, draw_number, track_id, mode, ...)
  and, for the local score ledger only, the drawn main numbers; no drawn number is in the returned dict.
- D-R3: invalid inputs (wrong type, out of range, repeated labels, supplementaries overlapping the drawn main
  numbers, s > 7 - m) raise ValueError (MRT-02: invalid s > 7 - m is rejected). bool is not accepted as an int.
"""
from __future__ import annotations

from fractions import Fraction
from math import comb

POWERBALL = 'POWERBALL'
OZLOTTO = 'OZLOTTO'
GAMES = (POWERBALL, OZLOTTO)

ENTRY_SIZE = 7                                   # main numbers per entry and per draw, both games
MAIN_POOL = {POWERBALL: 35, OZLOTTO: 47}         # main barrel size N
PB_POOL = 20                                     # Powerball barrel (Powerball only)
SUPP_COUNT = 3                                   # Oz Lotto supplementaries per draw
DIVISION_COUNT = {POWERBALL: 9, OZLOTTO: 7}      # D

# ---------------------------------------------------------------- validation helpers


def _game(game: object) -> str:
    if game not in GAMES:
        raise ValueError(f'unknown game {game!r}')
    return game  # type: ignore[return-value]


def _int(v: object, name: str, low: int, high: int) -> int:
    if type(v) is not int or not low <= v <= high:
        raise ValueError(f'{name} must be an int in {low}..{high}, got {v!r}')
    return v


def _labels(v: object, name: str, size: int, high: int) -> frozenset:
    try:
        items = list(v)  # type: ignore[call-overload]
    except TypeError:
        raise ValueError(f'{name} must be a collection of {size} labels') from None
    if len(items) != size or any(type(x) is not int or not 1 <= x <= high for x in items) or len(set(items)) != size:
        raise ValueError(f'{name} must be {size} distinct ints in 1..{high}')
    return frozenset(items)


# ---------------------------------------------------------------- one-draw main-match law (R3 17.4.4)

def main_match_weights(game: str) -> tuple[int, ...]:
    """Integer weights C(7,m) x C(N-7, 7-m) for m = 0..7; they sum to C(N, 7)."""
    n = MAIN_POOL[_game(game)]
    return tuple(comb(7, m) * comb(n - 7, 7 - m) for m in range(8))


def main_match_probabilities(game: str) -> tuple[Fraction, ...]:
    """p_G,m = C(7,m) x C(N-7,7-m) / C(N,7), m = 0..7 (hypergeometric; R3 17.4.4)."""
    w = main_match_weights(game)
    total = comb(MAIN_POOL[game], 7)
    return tuple(Fraction(x, total) for x in w)


def main_match_at_least(game: str, m: int) -> Fraction:
    """P0(main matches >= m), exact; m = 0..8 (m = 8 gives 0)."""
    _int(m, 'm', 0, 8)
    return sum(main_match_probabilities(game)[m:], Fraction(0))


# ---------------------------------------------------------------- the classifier (R3 17.4.2, 17.4.3)

def division(game: str, main_matches: int, powerball_match: int | None = None,
             supplementary_matches: int | None = None) -> int:
    """The single prize division won by one entry (0 = none). Each entry wins at most one division, the highest
    it qualifies for, so this is a function of (m, b) for Powerball and (m, s) for Oz Lotto."""
    _game(game)
    m = _int(main_matches, 'main_matches', 0, 7)
    if game == POWERBALL:
        if supplementary_matches is not None:
            raise ValueError('Powerball has no supplementary numbers')
        b = _int(powerball_match, 'powerball_match', 0, 1)
        return _PB_TABLE.get((m, b), 0)
    if powerball_match is not None:
        raise ValueError('Oz Lotto has no Powerball')
    s = _int(supplementary_matches, 'supplementary_matches', 0, min(SUPP_COUNT, 7 - m))
    if m == 7:
        return 1
    if m == 6:
        return 2 if s >= 1 else 3
    if m == 5:
        return 4 if s >= 1 else 5
    if m == 4:
        return 6
    if m == 3 and s >= 1:
        return 7
    return 0


# (m, b) -> Powerball division, SA Lotteries Powerball game rules rule 9.4 (R3 17.4.2). Operator prize order:
# PD7 (5 + 0) is more likely than PD6 (4 + 1).
_PB_TABLE = {(7, 1): 1, (7, 0): 2, (6, 1): 3, (6, 0): 4, (5, 1): 5, (4, 1): 6, (5, 0): 7, (3, 1): 8, (2, 1): 9}


def classification_cells(game: str) -> tuple[tuple[int, int], ...]:
    """Every valid (m, b) for Powerball or (m, s) for Oz Lotto (used by the exhaustive tests, MRT-02)."""
    if _game(game) == POWERBALL:
        return tuple((m, b) for m in range(8) for b in (0, 1))
    return tuple((m, s) for m in range(8) for s in range(min(SUPP_COUNT, 7 - m) + 1))


def cell_count(game: str, m: int, x: int) -> int:
    """Number of equally likely outcomes giving the cell (m, b) or (m, s) to one fixed entry.

    Powerball: C(7,m) x C(28,7-m) x (1 if b = 1 else 19), out of C(35,7) x 20 = 134,490,400.
    Oz Lotto: C(7,m) x C(3,s) x C(37,7-m-s), out of C(47,7) = 62,891,499 (R3 17.4.3 formula: the entry's other
    7-m-s numbers avoid all ten drawn numbers)."""
    if _game(game) == POWERBALL:
        _int(x, 'b', 0, 1)
        return comb(7, m) * comb(28, 7 - m) * (1 if x == 1 else PB_POOL - 1)
    if x > 7 - m:
        return 0
    return comb(7, m) * comb(SUPP_COUNT, x) * comb(47 - 10, 7 - m - x)


def outcome_total(game: str) -> int:
    """Total equally likely outcomes per entry: 134,490,400 (Powerball), 62,891,499 (Oz Lotto)."""
    return comb(35, 7) * PB_POOL if _game(game) == POWERBALL else comb(47, 7)


def _division_counts(game: str) -> tuple[int, ...]:
    counts = [0] * (DIVISION_COUNT[game] + 1)
    for m, x in classification_cells(game):
        if game == POWERBALL:
            d = division(game, m, powerball_match=x)
        else:
            d = division(game, m, supplementary_matches=x)
        counts[d] += cell_count(game, m, x)
    if sum(counts) != outcome_total(game):
        raise AssertionError('division counts do not cover the outcome space')
    return tuple(counts)


# Index 0 is "no division"; index d is division d.
DIVISION_OUTCOME_COUNTS = {g: _division_counts(g) for g in GAMES}


def division_outcome_counts(game: str) -> tuple[int, ...]:
    """Integer outcome counts for divisions 1..D (R3 17.4.2: 1, 19, 196, ...; 17.4.3: 1, 21, 259, ...)."""
    return DIVISION_OUTCOME_COUNTS[_game(game)][1:]


def division_probabilities(game: str) -> dict[int, Fraction]:
    """{d: p_d} for d = 1..D, exact Fractions (R3 17.4.2, 17.4.3)."""
    total = outcome_total(game)
    c = DIVISION_OUTCOME_COUNTS[game]
    return {d: Fraction(c[d], total) for d in range(1, DIVISION_COUNT[game] + 1)}


def division_probability(game: str, d: int) -> Fraction:
    """p_d for one division d = 1..D."""
    _int(d, 'division', 1, DIVISION_COUNT[_game(game)])
    return division_probabilities(game)[d]


def no_division_probability(game: str) -> Fraction:
    return Fraction(DIVISION_OUTCOME_COUNTS[_game(game)][0], outcome_total(game))


def any_division_probability(game: str) -> Fraction:
    """P(any division): 611573/26898080 (Powerball), 416512/20963833 (Oz Lotto)."""
    return sum(division_probabilities(game).values(), Fraction(0))


def division_set_probability(game: str, divisions) -> Fraction:
    """p_S = the exact sum of p_d over a set S of divisions (MR4)."""
    p = division_probabilities(game)
    s = set(divisions)
    if not s or any(d not in p for d in s):
        raise ValueError(f'invalid division set {sorted(s)!r} for {game}')
    return sum((p[d] for d in sorted(s)), Fraction(0))


# ---------------------------------------------------------------- fair-draw moments (R3 17.4.4)

def _moments(game: str) -> tuple[Fraction, Fraction]:
    p = main_match_probabilities(game)
    mean = sum((m * p[m] for m in range(8)), Fraction(0))
    var = sum((m * m * p[m] for m in range(8)), Fraction(0)) - mean * mean
    return mean, var


MEAN0 = {g: _moments(g)[0] for g in GAMES}       # 7/5 (Powerball), 49/47 (Oz Lotto)
VAR0 = {g: _moments(g)[1] for g in GAMES}        # 392/425 (Powerball), 39200/50807 (Oz Lotto)
PB_HIT_PROBABILITY = Fraction(1, PB_POOL)        # 1/20
PB_HIT_VARIANCE = PB_HIT_PROBABILITY * (1 - PB_HIT_PROBABILITY)   # 19/400 = 0.0475


def fair_moments(game: str) -> dict:
    """The fair-draw moments of R3 17.4.4 as exact Fractions."""
    out = {'mean0': MEAN0[_game(game)], 'var0': VAR0[game],
           'p_main_at_least': tuple(main_match_at_least(game, m) for m in range(8))}
    if game == POWERBALL:
        out['pb_hit_probability'] = PB_HIT_PROBABILITY
        out['pb_hit_variance'] = PB_HIT_VARIANCE
    return out


# ---------------------------------------------------------------- the per-draw match record (R3 17.4.1)

def match_record(game: str, ticket_main, ticket_pb, drawn_main, drawn_pb_or_supps) -> dict:
    """The per-draw match codes of one entry against one opened target draw.

    Powerball: ticket_main (7 distinct of 1..35), ticket_pb (1..20), drawn_main (7 distinct of 1..35),
    drawn_pb_or_supps = the drawn Powerball (1..20). Returns {main_matches, powerball_match, division}.

    Oz Lotto: ticket_main (7 distinct of 1..47), ticket_pb must be None (methods never forecast supplementaries
    and Oz Lotto has no Powerball), drawn_main (7 distinct of 1..47), drawn_pb_or_supps = the 3 drawn
    supplementaries (distinct, none equal to a drawn main number). Returns {main_matches, supplementary_matches,
    division}. The supplementaries are used only here and are not in the result (R2 2.5; R3 17.8)."""
    _game(game)
    n = MAIN_POOL[game]
    entry = _labels(ticket_main, 'ticket_main', ENTRY_SIZE, n)
    drawn = _labels(drawn_main, 'drawn_main', ENTRY_SIZE, n)
    m = len(entry & drawn)
    if game == POWERBALL:
        tpb = _int(ticket_pb, 'ticket_pb', 1, PB_POOL)
        dpb = _int(drawn_pb_or_supps, 'drawn_powerball', 1, PB_POOL)
        b = 1 if tpb == dpb else 0
        return {'main_matches': m, 'powerball_match': b, 'division': division(game, m, powerball_match=b)}
    if ticket_pb is not None:
        raise ValueError('Oz Lotto entries have no Powerball; ticket_pb must be None')
    supps = _labels(drawn_pb_or_supps, 'drawn_supplementaries', SUPP_COUNT, n)
    if supps & drawn:
        raise ValueError('drawn supplementaries must differ from the drawn main numbers')
    s = len(entry & supps)
    return {'main_matches': m, 'supplementary_matches': s,
            'division': division(game, m, supplementary_matches=s)}
