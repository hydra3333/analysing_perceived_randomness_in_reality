"""N1, the fair-draw null simulator, as WF-1B uses it (releases and WF-1 design v0.1r1 section 7; R3 17.5A).

With an APPROVED seed policy, it regenerates R = 10,000 simulated fair histories for the report's targets (the
generator of n1_generator, keyed by (replicate, target), so every table shares the same histories) and replays
every track's frozen tickets against them. It computes:
- MR1's N1_CALIBRATED p-value (a hit-sequence statistic; exact even under adaptive walk-forward), compared exactly;
- MR5's reference figure per variant (N1_FIXED_FORECAST_REFERENCE), compared exactly in doubled integer ranks;
- each family's maximum statistic (N1_FIXED_FORECAST_REFERENCE): the share of replicates whose smallest exact MR7
  P_up over the roster is at most the observed smallest one.
The Monte Carlo contract is (k + 1)/(R + 1), with the Clopper-Pearson 95% interval on k/R (R3 17.5A).

Replicates and their scores are NULL_CALIBRATION artefacts: held in memory only, never written to any ledger,
never read by a method (design 7.5). NumPy is used only for exact integer arithmetic (bit masks, counts, sums).
"""
from __future__ import annotations

from fractions import Fraction
from math import log2

import numpy as np

from . import divisions as DV
from . import measures as MS
from . import n1_generator as G
from . import numerics as NU

R = 10_000


def _popcount(a: np.ndarray) -> np.ndarray:
    if hasattr(np, 'bitwise_count'):
        return np.bitwise_count(a).astype(np.int64)
    b = a.view(np.uint8).reshape(a.shape + (8,))
    table = np.array([bin(i).count('1') for i in range(256)], dtype=np.int64)
    return table[b].sum(axis=-1)


def _mask(labels) -> int:
    m = 0
    for x in labels:
        m |= 1 << x
    return m


def simulate(policy: dict, game_id: str, targets: list[int], replicates: int | None = None) -> dict:
    """In-memory replicate draws: main bit masks [R, T]; Powerball [R, T] or supplementary masks [R, T]; and the
    drawn main labels [R, T, 7] for MR5."""
    root, pid = policy['output_value'], policy['policy_id']
    replicates = R if replicates is None else replicates
    T = len(targets)
    main = np.zeros((replicates, T), dtype=np.uint64)
    extra = np.zeros((replicates, T), dtype=np.uint64 if game_id == 'OZLOTTO' else np.int64)
    labels = np.zeros((replicates, T, 7), dtype=np.int64)
    for r in range(replicates):
        for j, t in enumerate(targets):
            m, x = G.fair_draw(root, pid, game_id, r + 1, t)
            main[r, j] = _mask(m)
            labels[r, j] = m
            extra[r, j] = _mask(x) if game_id == 'OZLOTTO' else x
    return {'targets': targets, 'index': {t: j for j, t in enumerate(targets)}, 'main': main, 'extra': extra,
            'labels': labels, 'R': replicates}


def _division_table(game_id: str) -> np.ndarray:
    if game_id == 'POWERBALL':
        tab = np.zeros((8, 2), dtype=np.int64)
        for m in range(8):
            for b in range(2):
                tab[m, b] = DV.division(game_id, m, powerball_match=b)
    else:
        tab = np.zeros((8, 4), dtype=np.int64)
        for m in range(8):
            for s in range(min(3, 7 - m) + 1):
                tab[m, s] = DV.division(game_id, m, supplementary_matches=s)
    return tab


def _replay(sim: dict, game_id: str, entries: dict) -> tuple[np.ndarray, np.ndarray]:
    """(main matches [R, n], division [R, n]) of one track's frozen tickets, over its own valid targets."""
    cols = [sim['index'][t] for t in sorted(entries)]
    tick = np.array([_mask(entries[t][0]) for t in sorted(entries)], dtype=np.uint64)
    mm = _popcount(sim['main'][:, cols] & tick[None, :])
    tab = _division_table(game_id)
    if game_id == 'POWERBALL':
        pb = np.array([entries[t][1] for t in sorted(entries)], dtype=np.int64)
        second = (sim['extra'][:, cols] == pb[None, :]).astype(np.int64)
    else:
        second = _popcount(sim['extra'][:, cols] & tick[None, :])
    return mm, tab[mm, second]


def _mc(k: int, reps: int) -> dict:
    p = Fraction(k + 1, reps + 1)
    return {'p_up': p, 'k': k, 'R': reps, 'ci': NU.clopper_pearson(k, reps)}


def _mr1_at_least(game_id: str, w_rep: np.ndarray, w_obs: list[int]) -> int:
    """How many replicates have MR1 >= the observed MR1 (same n), decided exactly (design 7.4): MR1_rep >= MR1_obs
    iff prod p_d^(W_rep_d) <= prod p_d^(W_obs_d). A float difference far from zero decides; ties near zero are
    settled with exact Fractions."""
    probs = DV.division_probabilities(game_id)
    D = DV.DIVISION_COUNT[game_id]
    pd = [probs[d] if isinstance(probs, dict) else probs[d - 1] for d in range(1, D + 1)]
    bits = np.array([-log2(float(p)) for p in pd])
    obs_bits = float(np.dot(bits, np.array(w_obs, dtype=float)))
    rep_bits = w_rep.astype(float) @ bits
    diff = rep_bits - obs_bits
    count = int((diff > 1e-6).sum())
    near = np.nonzero(np.abs(diff) <= 1e-6)[0]
    lhs_obs = Fraction(1)
    for p, w in zip(pd, w_obs):
        lhs_obs *= p ** int(w)
    for i in near:
        v = Fraction(1)
        for p, w in zip(pd, w_rep[i]):
            v *= p ** int(w)
        count += v <= lhs_obs
    return count


def runner(policy: dict):
    """The function report.run_report calls at step 8 (after the ledgers are written)."""
    def run(game_id: str, per_track: dict, per_variant: dict, families: list) -> dict:
        if any(not tr['track_id'].endswith(':WF') for tr in per_track.values()):
            raise ValueError('N1 refuses in-sample input: walk-forward tracks only (design 7.5; MRT-06)')
        targets = sorted({t for tr in per_track.values() for t in tr['entries']} |
                         {t for vr in per_variant.values() for t in vr['groups']})
        if not targets:
            return {'mr1': {}, 'mr5': {}, 'families': {}, 'R': R}
        sim = simulate(policy, game_id, targets)
        reps = sim['R']
        D = DV.DIVISION_COUNT[game_id]
        out = {'mr1': {}, 'mr5': {}, 'families': {}, 'R': reps, 'policy_id': policy['policy_id']}
        for key, tr in per_track.items():
            if not tr['entries']:
                continue
            mm, div = _replay(sim, game_id, tr['entries'])
            w_rep = np.stack([(div == d).sum(axis=1) for d in range(1, D + 1)], axis=1)
            w_obs = [sum(1 for x in tr['targets'] if x['division'] == d) for d in range(1, D + 1)]
            out['mr1'][key] = _mc(_mr1_at_least(game_id, w_rep, w_obs), reps)
        # MR5 reference: replicate sum of doubled mid-ranks of the drawn main numbers, lower = better.
        for key, vr in per_variant.items():
            if not vr['groups']:
                continue
            ts = sorted(vr['groups'])
            cols = [sim['index'][t] for t in ts]
            rank2 = np.zeros((len(ts), DV.MAIN_POOL[game_id] + 1), dtype=np.int64)
            for j, t in enumerate(ts):
                for lab, rk in MS.mid_ranks_from_groups(vr['groups'][t]['MAIN'], DV.MAIN_POOL[game_id]).items():
                    rank2[j, lab] = int(2 * rk)
            rep = rank2[np.arange(len(ts))[None, :, None], sim['labels'][:, cols, :]].sum(axis=(1, 2))
            obs = sum(int(2 * Fraction(x['mean_rank_main']) * 7) for x in vr['targets'])
            k = int((rep <= obs).sum())
            out['mr5'][key] = {'MR5.MAIN': dict(_mc(k, reps), label='N1_FIXED_FORECAST_REFERENCE')}
            if game_id == 'POWERBALL':
                q2 = np.zeros((len(ts), DV.PB_POOL + 1), dtype=np.int64)
                for j, t in enumerate(ts):
                    for lab, rk in MS.mid_ranks_from_groups(vr['groups'][t]['POWERBALL'], DV.PB_POOL).items():
                        q2[j, lab] = int(2 * rk)
                rep_pb = q2[np.arange(len(ts))[None, :], sim['extra'][:, cols]].sum(axis=1)
                obs_pb = sum(int(2 * Fraction(x['rank_powerball'])) for x in vr['targets'])
                out['mr5'][key]['MR5.PB'] = dict(_mc(int((rep_pb <= obs_pb).sum()), reps),
                                                 label='N1_FIXED_FORECAST_REFERENCE')
        # Family maximum statistic (MR7.MAIN, and MR7.PB for Powerball), exact tails per replicate.
        for fam in families:
            ch = fam['measure'].split('.')[1]
            per = []
            for tid in fam['roster']:
                hit = next(((k, tr) for k, tr in per_track.items() if tr['track_id'] == tid and tr['entries']), None)
                if hit is None:
                    continue
                key, tr = hit
                n = len(tr['entries'])
                if ch == 'MAIN':
                    mm, _d = _replay(sim, game_id, tr['entries'])
                    s_rep = mm.sum(axis=1)
                    s_obs = sum(x['main_matches'] for x in tr['targets'])
                    up = _tail_table(game_id, n)
                else:
                    cols = [sim['index'][t] for t in sorted(tr['entries'])]
                    pb = np.array([tr['entries'][t][1] for t in sorted(tr['entries'])], dtype=np.int64)
                    s_rep = (sim['extra'][:, cols] == pb[None, :]).sum(axis=1)
                    s_obs = sum(x['powerball_match'] for x in tr['targets'])
                    up = [NU.binom_upper(n, Fraction(1, 20), s) for s in range(n + 1)]
                per.append((up, s_rep, s_obs))
            if not per:
                continue
            obs_min = min(up[s_obs] for up, _s, s_obs in per)
            k = 0
            for r in range(reps):
                if min(up[int(s[r])] for up, s, _o in per) <= obs_min:
                    k += 1
            out['families'][fam['family_id']] = dict(_mc(k, reps), label='N1_FIXED_FORECAST_REFERENCE',
                                                     p=Fraction(k + 1, reps + 1))
        return out
    return run


_TAILS: dict = {}


def _tail_table(game_id: str, n: int) -> list[Fraction]:
    """P_up(S) for S = 0..7n, exact (MR7's null)."""
    if (game_id, n) not in _TAILS:
        c = NU.mr7_null(game_id, n)
        total = sum(c)
        tails, acc = [0] * len(c), 0
        for s in range(len(c) - 1, -1, -1):
            acc += c[s]
            tails[s] = Fraction(acc, total)
        _TAILS[(game_id, n)] = tails
    return _TAILS[(game_id, n)]
