#!/usr/bin/env python3
"""OUTLANDISH_01 reviewer's independent checks, v0.1 (Claude, review point A).

Purpose
    Re-runnable evidence behind OUTLANDISH_REVIEW_002_Claude_to_ChatGPT.md.
    Written by the independent reviewer, NOT by the implementer, and sharing
    no matching, classification or statistics code with the modules it tests.

What it checks
    1. Matcher v0.4 + classifier v0.1 against a deliberately slow brute-force
       oracle: random digit strings with planted Powerball / Oz hits, many
       chunk sizes, prefix scans, multi-draw keys. Exact event tuple sets,
       canonical order, full-file SHA-256, order/slot flags and same-draw
       interval-overlap counts.
    2. Q4d statistics: signed-gap tie rule, centred two-sided permutation p,
       Holm over six constants, expectation table, conditional q values and
       the exact two-sided binomial.
    3. Optional (--timing): wall time of one 10,000-permutation primary test
       at Powerball-like and illustrative Oz-like event densities.

What it does NOT do
    No REAL data: it never opens the published packed constants, receipts,
    POWERBALL_preholdout_only.csv, any results folder or any parent-project
    path. Synthetic files go to a TemporaryDirectory that is deleted on exit.
    Writes nothing into the repository (bytecode writing is disabled).
    A PASS here is reviewer evidence about synthetic behaviour only. It is
    not Q4 production qualification and not Q5 authorisation.

Usage (Windows CMD, from the repository root)
    ".venv\\Scripts\\python.exe" "GAIS\\OUTLANDISH_01\\REVIEW\\OUTLANDISH_REVIEW_Claude_Independent_Checks_v0_1.py" --run
    add --timing for the optional permutation timing (about 1-3 minutes).

Expected final line
    REVIEWER INDEPENDENT CHECKS PASS: matcher-trials=60 events=... classified=... stats=PASS

Requires the same project venv as the Q3/Q4 suites (NumPy, for matcher v0.4).
Last run by the reviewer at commit a3339901746ab8645dc63a94fd30421cdc69e4d5
(Linux, Python 3.13.18, NumPy 2.5.3).
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import math
import random
import statistics
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
PROJECT = Path(__file__).absolute().parent.parent   # GAIS/OUTLANDISH_01
sys.path.insert(0, str(PROJECT))

LENGTHS = {'K7S': 16, 'K7': 14, 'K6S': 14, 'K7mix': 14, 'K6': 12}


# ---------------------------------------------------------------- helpers

def pack(digits: str) -> bytes:
    """Independent high-nibble-first packing; odd length gets a zero pad nibble."""
    if len(digits) % 2:
        digits += '0'
    return bytes.fromhex(digits)


def fixed2(values) -> str:
    return ''.join(f'{v:02d}' for v in values)


def fields(ds: str, k: int, count: int) -> list[int]:
    return [int(ds[k + 2*i:k + 2*i + 2]) for i in range(count)]


def is_subsequence(short, long) -> bool:
    it = iter(long)
    return all(x in it for x in short)


# ---------------------------------------------------------------- oracles

def oracle_powerball(ds: str, n: int, draws: list[dict]) -> set:
    """Literal v0.2 A3.1 rules, every start, per-family end bound k+L<=n."""
    out = set()
    for k in range(n):
        for d in draws:
            mains = set(d['mains'])
            if k + 14 <= n:
                w = fields(ds, k, 7)
                if len(set(w)) == 7 and set(w) == mains:
                    out.add((d['id'], 'K7', k, ds[k:k+14]))
                if len(set(w[:6])) == 6 and set(w[:6]) <= mains and w[6] == d['pb']:
                    out.add((d['id'], 'K6S', k, ds[k:k+14]))
            if k + 16 <= n:
                w = fields(ds, k, 8)
                if len(set(w[:7])) == 7 and set(w[:7]) == mains and w[7] == d['pb']:
                    out.add((d['id'], 'K7S', k, ds[k:k+16]))
    return out


def oracle_oz(ds: str, n: int, draws: list[dict]) -> set:
    """Literal v0.2 A3.2 rules: K6, K7 and K7mix (supplementary in any slot)."""
    out = set()
    for k in range(n):
        for d in draws:
            mains, supps = set(d['mains']), set(d['supps'])
            if k + 12 <= n:
                w = fields(ds, k, 6)
                if len(set(w)) == 6 and set(w) <= mains:
                    out.add((d['id'], 'K6', k, ds[k:k+12]))
            if k + 14 <= n:
                w = fields(ds, k, 7)
                if len(set(w)) == 7:
                    if set(w) == mains:
                        out.add((d['id'], 'K7', k, ds[k:k+14]))
                    if len(set(w) & mains) == 6 and len(set(w) & supps) == 1:
                        out.add((d['id'], 'K7mix', k, ds[k:k+14]))
    return out


# ---------------------------------------------------------------- check 1

def random_draws(rng: random.Random, game: str) -> list[dict]:
    draws = []
    for i in range(rng.randint(2, 6)):
        if game == 'powerball':
            mains = rng.sample(range(1, 36), 7)
            low = [m for m in mains if m <= 20]
            # Half the time force PB equal to a main (legal in v0.2) when possible.
            pb = rng.choice(low) if low and rng.random() < 0.5 else rng.randint(1, 20)
            draws.append(dict(id=i + 1, mains=mains, pb=pb))
        else:
            balls = rng.sample(range(1, 48), 10)
            draws.append(dict(id=i + 1, mains=balls[:7], supps=balls[7:]))
    if len(draws) > 1 and rng.random() < 0.3:
        # Same canonical key on two draws: every attribution must be kept.
        draws[1] = dict(draws[0], id=2, mains=rng.sample(draws[0]['mains'], 7))
    return draws


def planted_string(rng: random.Random, game: str, draws: list[dict], n: int) -> str:
    digits = [str(rng.randrange(10)) for _ in range(n)]
    for _ in range(rng.randint(3, 14)):
        d = rng.choice(draws)
        perm = rng.sample(d['mains'], 7)
        kind = rng.randrange(4)
        if game == 'powerball':
            text = [fixed2(perm + [d['pb']]), fixed2(perm),
                    fixed2(perm[:6] + [d['pb']]), fixed2(d['mains'] + [d['pb']])][kind]
        else:
            six, sup, slot = perm[:6], rng.choice(d['supps']), rng.randrange(7)
            text = [fixed2(perm), fixed2(six), fixed2(six[:slot] + [sup] + six[slot:]),
                    fixed2(d['mains'])][kind]
        pos = rng.choice([0, max(0, n - len(text)), rng.randrange(0, max(1, n - len(text) + 1))])
        if pos + len(text) <= n:
            digits[pos:pos + len(text)] = list(text)
    return ''.join(digits)


def check_matcher_and_classifier(work: Path, trials: int = 60) -> tuple[int, int]:
    import OUTLANDISH_01_Q3_Packed_Matcher_v0_4 as M
    import OUTLANDISH_01_Q3_Packed_Matcher_v0_2 as M2      # classifier's record classes
    import OUTLANDISH_01_Q3_Event_Classifier_v0_1 as C

    rng = random.Random(20261116)
    total_events = total_classified = 0
    for trial in range(trials):
        game = 'powerball' if trial % 2 == 0 else 'oz'
        draws = random_draws(rng, game)
        n = rng.randint(40, 700)
        ds = planted_string(rng, game, draws, n)
        eff = rng.choice([n, n, rng.randint(max(1, n - 20), n)])   # some prefix scans
        path = work / f'trial_{trial}.packed.bin'
        path.write_bytes(pack(ds))
        expected = (oracle_powerball if game == 'powerball' else oracle_oz)(ds, eff, draws)
        file_sha = hashlib.sha256(path.read_bytes()).hexdigest()

        got = None
        for chunk in (1, 2, 3, 7, 16, 4_000_000):
            if game == 'powerball':
                recs = [M.PBRecord(d['id'], tuple(d['mains']), d['pb']) for d in draws]
                res = M.scan_packed(path, physical_digits=n, effective_digits=eff,
                                    draws=recs, chunk_bytes=chunk)
            else:
                recs = [M.OzRecord(d['id'], tuple(d['mains']), tuple(d['supps'])) for d in draws]
                res = M.scan_packed_oz(path, physical_digits=n, effective_digits=eff,
                                       draws=recs, chunk_bytes=chunk)
            got = [(e.draw_number, e.family, e.start_digit_offset, e.matched_digits)
                   for e in res.events]
            if set(got) != expected or len(got) != len(set(got)):
                raise AssertionError(f'matcher/oracle mismatch trial={trial} game={game} '
                                     f'chunk={chunk}: {sorted(set(got) ^ expected)[:5]}')
            if got != sorted(got, key=lambda t: (t[2], t[1], t[0])):
                raise AssertionError(f'non-canonical event order trial={trial} chunk={chunk}')
            if res.sha256_full_packed != file_sha or res.bytes_hashed != len(pack(ds)):
                raise AssertionError(f'full-file digest wrong trial={trial} chunk={chunk}')
        total_events += len(expected)

        # Classifier: order, subsequence and supplementary-slot flags.
        if game == 'powerball':
            crecs = [M2.PBRecord(d['id'], tuple(d['mains']), d['pb']) for d in draws]
        else:
            crecs = [M2.OzRecord(d['id'], tuple(d['mains']), tuple(d['supps'])) for d in draws]
        cevents = [M2.RawEvent(*t) for t in got]
        by_id = {d['id']: d for d in draws}
        for c in C.classify_events(game, cevents, crecs, effective_digits=eff):
            d = by_id[c.event.draw_number]
            v = fields(c.event.matched_digits, 0, len(c.event.matched_digits) // 2)
            fam = c.event.family
            if fam in ('K7S', 'K7'):
                ok = c.drawn_order == (v[:7] == d['mains']) and c.reordered_only == (not c.drawn_order)
            elif fam in ('K6S', 'K6'):
                sub = is_subsequence(v[:6], d['mains'])
                ok = c.drawn_subsequence_order == sub and c.reordered_only == (not sub)
            else:
                slots = [i for i, x in enumerate(v) if x in d['supps']]
                sub = is_subsequence(v, d['mains'] + d['supps'])
                ok = (len(slots) == 1 and c.supplementary_slot == slots[0]
                      and c.supplementary_last == (slots[0] == 6)
                      and c.drawn_subsequence_order == sub
                      and (not sub or c.supplementary_last))   # O2 nesting
            if not ok:
                raise AssertionError(f'classifier flag mismatch trial={trial}: {c}')
            total_classified += 1

        # Same-draw direct interval overlaps against all-pairs brute force.
        summary = C.summarize_same_draw_overlaps(cevents, game=game)
        brute = sum(1 for a, b in itertools.combinations(got, 2)
                    if a[0] == b[0] and a[2] < b[2] + LENGTHS[b[1]] and b[2] < a[2] + LENGTHS[a[1]])
        if summary.direct_same_draw_pairs != brute:
            raise AssertionError(f'overlap mismatch trial={trial}: {summary} vs {brute}')
    return total_events, total_classified


# ---------------------------------------------------------------- check 2

def brute_median_gap(sets):
    gaps = [min(abs(y - x) for x in a for y in b) for a, b in zip(sets, sets[1:]) if a and b]
    return statistics.median(gaps) if gaps else None


def check_statistics() -> None:
    import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S
    rng = random.Random(7)

    # Signed-gap tie rule (abs(b-a), b-a, a, b).
    for _ in range(20_000):
        a = [rng.randrange(60) for _ in range(rng.randint(0, 5))]
        b = [rng.randrange(60) for _ in range(rng.randint(0, 5))]
        ref = min(((abs(y - x), y - x, x, y) for x in a for y in b), default=None)
        if S.closest_gap(a, b) != ref:
            raise AssertionError(f'closest_gap tie rule a={a} b={b}')

    # Permutation p: same shuffle stream, independent median/centre/count.
    for t in range(300):
        sets = [tuple(sorted({rng.randrange(1000) for _ in range(rng.choice([0, 0, 1, 2, 3]))}))
                for _ in range(rng.randint(2, 9))]
        out = S.permutation_test(sets, seed=t, iterations=200)
        shuffler, valid = random.Random(t), []
        for _ in range(200):
            trial = list(sets)
            shuffler.shuffle(trial)               # every draw, empties included
            m = brute_median_gap(trial)
            if m is not None:
                valid.append(m)
        observed = brute_median_gap(sets)
        if observed is None or not valid:
            if out['centered_two_sided_p'] is not None or not out['undefined_reason']:
                raise AssertionError('undefined case must give N/A, not a p-value')
            continue
        centre = statistics.median(valid)
        b = sum(abs(v - centre) >= abs(observed - centre) for v in valid)
        if (out['centered_two_sided_p'] != (1 + b) / (len(valid) + 1)
                or out['valid_permutations'] != len(valid)
                or out['undefined_permutations'] != 200 - len(valid)):
            raise AssertionError(f'permutation p mismatch case {t}')

    # Holm over exactly six constants; N/A stays in the family, adjusted as p=1.
    for _ in range(5_000):
        p = {c: (None if rng.random() < 0.15 else rng.random()) for c in S.CONSTANTS}
        adj = S.holm_six_constants(p)
        running, ref = 0.0, {}
        for i, (v, c) in enumerate(sorted(((1.0 if x is None else x), c) for c, x in p.items())):
            running = max(running, min(1.0, (6 - i) * v))
            ref[c] = running
        for c in S.CONSTANTS:
            if (adj[c] is None) != (p[c] is None) or (p[c] is not None and abs(adj[c] - ref[c]) > 1e-15):
                raise AssertionError(f'Holm mismatch {p}')

    # Expectations: v0.2 B5.1 table, Powerball D=433, N=10^10.
    table = {'P1_drawn': 0.00043, 'P1_any': 2.18, 'P2_drawn': 0.0433, 'P2_any': 218.23,
             'P3_subsequence': 0.3031, 'P3_any': 218.23}
    rules = {r[0]: r for r in S.VIEW_RULES['powerball']}
    for view, value in table.items():
        _, family, _, seqs, _ = rules[view]
        L = S.FAMILY_LENGTHS[family]
        e = 433 * seqs * (10**10 - L + 1) / 10**L
        if abs(e - value) > 0.006 * max(value, 0.01):
            raise AssertionError(f'expectation {view}: {e} vs spec {value}')

    # Conditional q: v0.2 B5.2.
    q_spec = {('powerball', 'P1_drawn'): 1/5040, ('powerball', 'P2_drawn'): 1/5040,
              ('powerball', 'P3_subsequence'): 1/720, ('oz', 'O1_drawn'): 1/5040,
              ('oz', 'O3_subsequence'): 1/720, ('oz', 'O2_supplementary_last'): 1/7,
              ('oz', 'O2_subsequence'): 1/720}
    for (game, view), q in q_spec.items():
        r = {x[0]: x for x in S.VIEW_RULES[game]}
        _, _, _, s, parent = r[view]
        if abs(s / r[parent][3] - q) > 1e-15:
            raise AssertionError(f'conditional q {game} {view}')

    # Exact two-sided binomial against direct enumeration.
    for n, k, q in [(10, 0, 1/720), (227, 1, 1/720), (50, 12, 1/7), (30, 3, 1/7), (5, 5, 0.5)]:
        pmf = [math.comb(n, i) * q**i * (1 - q)**(n - i) for i in range(n + 1)]
        ref = min(1.0, sum(x for x in pmf if x <= pmf[k] * (1 + 1e-9)))
        if abs(S.binomial_two_sided(n, k, q) - ref) > 1e-9:
            raise AssertionError(f'binomial n={n} k={k} q={q}')


# ---------------------------------------------------------------- check 3

def timing() -> None:
    import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S

    def sets_for(draws: int, mean: float, seed: int = 1):
        r = random.Random(seed)
        out = []
        for _ in range(draws):
            k = sum(r.random() < mean / 1000 for _ in range(1000))   # ~Poisson(mean)
            out.append(tuple(sorted({r.randrange(10**10) for _ in range(k)})))
        return out

    cases = [('Powerball K6S, 433 draws, ~0.5 events/draw', 433, 0.504),
             ('Oz K6, ILLUSTRATIVE 200 draws, ~50 events/draw', 200, 50.4),
             ('Oz K6, ILLUSTRATIVE 250 draws, ~50 events/draw', 250, 50.4)]
    for label, draws, mean in cases:
        sets = sets_for(draws, mean)
        start = time.perf_counter()
        S.permutation_test(sets, seed=271828, iterations=1_000)
        seconds = time.perf_counter() - start
        print(f'TIMING {label}: events={sum(map(len, sets))} '
              f'1,000 perms {seconds:.2f}s -> 10,000 perms about {10 * seconds:.0f}s')
    print('TIMING NOTE: Oz draw counts are illustrative; the approved Oz era is unconfirmed.')


# ---------------------------------------------------------------- main

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--run', action='store_true', required=True,
                        help='run the synthetic independent checks')
    parser.add_argument('--timing', action='store_true',
                        help='also time one 10,000-permutation test (slower)')
    args = parser.parse_args()
    print(f'PROJECT: {PROJECT}')
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_REVIEW_INDEPENDENT_') as tmp:
        events, classified = check_matcher_and_classifier(Path(tmp))
    print(f'PASS: matcher v0.4 + classifier vs reviewer oracle, events={events}')
    check_statistics()
    print('PASS: Q4d gap/permutation/Holm/expectation/q/binomial vs reviewer re-implementation')
    if args.timing:
        timing()
    print(f'REVIEWER INDEPENDENT CHECKS PASS: matcher-trials=60 events={events} '
          f'classified={classified} stats=PASS')
    print('  SYNTHETIC ONLY; no REAL constants, receipts, histories or results read.')
    print('  Not Q4 production qualification; not Q5 authorisation.')


if __name__ == '__main__':
    main()
