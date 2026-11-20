"""Worked INVENTED examples for the OV-1 simplification amendment (EX_253 section 5, B and D). Design evidence only.

Everything here is invented: the barrel is 35 numbers, the draws 101 to 116 come from a hash, and the "methods" are toy
functions. No real draw, forecast, ledger or project record is read. The ONLY project code used is the passed
numerical kernel (src/evaluation/ov1_numeric.py of the staged slice-3 tree), imported unchanged, so the factors shown
are the certified ones the real recorder would store.

Usage:  python -B ov1_prevailing_examples.py PATH_TO_STAGED_src
"""
import hashlib, json, sys
sys.path.insert(0, sys.argv[1])
from evaluation import ov1_numeric as NUM

N, K, FIRST, LAST, START = 35, 7, 101, 116, 101
BASE = ('A1', 'A2', 'A3', 'A4', 'A5')


def _h(*parts) -> int:
    return int(hashlib.sha256('|'.join(str(p) for p in parts).encode()).hexdigest(), 16)


def drawn(t: int) -> tuple:
    """The invented result of draw t: seven of 1..35."""
    return tuple(sorted(sorted(range(1, N + 1), key=lambda j: _h('INVENTED-DRAW', t, j))[:K]))


def history(t: int) -> tuple:
    """What a method may see for target t: the draws BEFORE t only (N-1)."""
    return tuple(drawn(u) for u in range(FIRST - 20, t))


def toy(variant: str, t: int, hist: tuple, flavour: str = '') -> tuple:
    """A deterministic toy method: a ranking of the 35 numbers from the variant's name, the target and the history it
    was given. TOP is the first seven, WORST the last seven."""
    seed = hashlib.sha256(repr(hist).encode()).hexdigest()
    order = sorted(range(1, N + 1), key=lambda j: _h(variant, flavour, t, seed, j))
    return tuple(sorted(order[:K])), tuple(sorted(order[-K:]))


KNOWN_TO_DESIGNER = {t: drawn(t) for t in range(FIRST, 109)}       # NEW was written after draw 108 was known


def new_method(t: int, hist: tuple) -> tuple:
    """NEW: 'inspired' by the results up to 108. For a target its designer had seen, it favours what was drawn. For a
    later target it has nothing but the toy rule. It never reads a result through its inputs: hist stops at t - 1."""
    if t in KNOWN_TO_DESIGNER:
        top = KNOWN_TO_DESIGNER[t]
        rest = [j for j in sorted(range(1, N + 1), key=lambda j: _h('NEW', t, j)) if j not in top]
        return top, tuple(sorted(rest[-K:]))
    return toy('NEW', t, hist)


def forecast(variant: str, t: int, flavour: str = ''):
    return new_method(t, history(t)) if variant == 'NEW' else toy(variant, t, history(t), flavour)


def line(t: int, pairs: dict, classes: dict, logs: list) -> tuple:
    """One target's line of the prevailing stream from the counted pairs {variant: (TOP, WORST)}."""
    w = [0] * N
    for top, worst in pairs.values():
        for j in top:
            w[j - 1] += 1
        for j in worst:
            w[j - 1] -= 1
    table = NUM.factor_table(w) if pairs else None
    out = {'target': t, 'counted_variants': sorted(pairs), 'weights': w, 'classes': classes}
    if table is None:
        out.update(factor_one=('NO_COUNTED_PAIR' if not pairs else 'V_IS_ZERO'), x=None, z=None)
    else:
        x = sum(w[j - 1] for j in drawn(t))
        logs = [L + row[x] for L, row in zip(logs, table['rows'])]
        out.update(factor_one=None, x=x, z=NUM.z_text(x, *table['variance'], places=3))
    out['logs'] = [str(L) for L in logs]
    out['score'] = NUM.fixed_text(NUM.mixture_lower(logs), 6)
    return out, logs


def stream(first_eligible: dict, upto: int, *, before: dict | None = None, lines=None, absent=(), flavour=None):
    """The prevailing stream from START (or continued from `lines`). first_eligible: variant -> its first eligible draw.
    before: target -> True if that target's set was forecast before its draw (else it was caught up afterwards).
    absent: (variant, target) pairs with no complete pair (a failure record). flavour: variant -> a changed toy rule."""
    lines = list(lines or [])
    logs = [int(v) for v in lines[-1]['logs']] if lines else [0] * 6
    t0 = lines[-1]['target'] + 1 if lines else START
    for t in range(t0, upto + 1):
        cohort = [v for v, f in sorted(first_eligible.items()) if f <= t and (v, t) not in absent]
        pairs = {v: forecast(v, t, (flavour or {}).get(v, '')) for v in cohort}
        early = (before or {}).get(t, True)
        classes = {'forecast_before_the_draw': len(pairs) if early else 0, 'caught_up_after_the_draw': 0 if early else len(pairs)}
        ln, logs = line(t, pairs, classes, logs)
        lines.append(ln)
    return lines


def maths(ln: dict) -> str:
    return json.dumps({k: ln[k] for k in ('target', 'counted_variants', 'weights', 'x', 'logs')}, sort_keys=True)


def show(title: str, lines, pick=None) -> None:
    print(title)
    for ln in lines:
        if pick is None or ln['target'] in pick:
            c = ln['classes']
            print(f"  draw {ln['target']}: {len(ln['counted_variants'])} variants "
                  f"({c['forecast_before_the_draw']} before, {c['caught_up_after_the_draw']} caught up), "
                  + (f"X={ln['x']:+d} Z={ln['z']}" if ln['factor_one'] is None else f"factor 1 ({ln['factor_one']})")
                  + f", score {ln['score']}")


def hits(variant: str, targets) -> int:
    return sum(len(set(forecast(variant, t)[0]) & set(drawn(t))) for t in targets)


REL = {v: START for v in BASE}                   # the five base variants were released before draw 101
REL_NEW = dict(REL, NEW=109)                     # NEW is released after draw 108: its first eligible draw is 109

print('=== 1. Ordinary weeks: five variants, draws 101 to 108, each forecast before its draw')
s1 = stream(REL, 108)
show('', s1)

print('\n=== 2. NEW is released after draw 108. Spectacular on the draws its designer had seen, ordinary afterwards')
full = stream(REL_NEW, LAST)
print('  (a) the ranking is recomputed with NEW in it. TOP ticket, hits and chance (7*7/35 = 1.4 a draw):')
for label, rng in (('draws 101-108 (NEW: back-history, development evidence)', range(101, 109)),
                   ('draws 109-116 (NEW: forward)', range(109, 117))):
    row = sorted(((hits(v, rng), v) for v in REL_NEW), reverse=True)
    print(f'      {label}: ' + ', '.join(f'{v} {h} hits ({h / len(rng):.2f} a draw)' for h, v in row))
unchanged = all(maths(a) == maths(b) for a, b in zip(s1, full[:8]))
print(f'  (b) prevailing stream, draws 101-108, before and after NEW was released: identical = {unchanged}')
show('  (c) prevailing stream, NEW counted from draw 109:', full, pick=(108, 109, 110, 116))
retro = stream(dict(REL, NEW=START), LAST)
print(f'  (d) EXPLORATORY retrospective view with NEW back-filled from 101 (never the prevailing score): '
      f'score after 108 = {retro[7]["score"]}, after 116 = {retro[-1]["score"]}; '
      f'bar of 40 reached at some draw = {any(NUM.crossing([int(v) for v in ln["logs"]]) for ln in retro)}')
print(f'      the prevailing score after 108 = {full[7]["score"]}, after 116 = {full[-1]["score"]}')

print('\n=== 3. A missed week: draw 111 was not forecast beforehand; the next session catches it up')
missed = stream(REL_NEW, LAST, before={111: False})
print(f'  the factors and the score are the same as if it had been forecast beforehand: '
      f'{all(maths(a) == maths(b) for a, b in zip(full, missed))}')
show('', missed, pick=(110, 111, 112))
print('  (supplement v0.8 would have given draw 111 the factor 1: MISSED_NO_FREEZE)')

print('\n=== 4. A forecast that is really missing: A3 has only a failure record for draw 113; no variant has a pair for 114')
gone = {('A3', 113)} | {(v, 114) for v in REL_NEW}
show('', stream(REL_NEW, LAST, absent=gone), pick=(112, 113, 114, 115))

print('\n=== 5. A restore. The backup was taken after draw 110 was scored; draws 111 to 116 are replayed (N-1)')
replay = stream(REL_NEW, LAST, lines=full[:10], before={t: False for t in range(111, 117)})
print(f'  replayed factors and score, draws 111-116, equal the lost originals: '
      f'{all(maths(a) == maths(b) for a, b in zip(full, replay))}; final score {replay[-1]["score"]} (lost original {full[-1]["score"]})')
print('  5b. An OLDER backup, taken after draw 107, before NEW was released. NEW is installed again after the restore,')
print('      so its first eligible draw is now 117:')
older = stream(dict(REL, NEW=117), LAST, lines=full[:7], before={t: False for t in range(108, 117)})
print(f'      draws 108-116 replayed without NEW: final score {older[-1]["score"]} (lost original {full[-1]["score"]}); '
      f'draws 101-107 untouched: {all(maths(a) == maths(b) for a, b in zip(full[:7], older[:7]))}')
print('  5c. The same replay as 5, but variant A2 now computes differently (as after a changed Python package):')
drift = stream(REL_NEW, LAST, lines=full[:10], before={t: False for t in range(111, 117)}, flavour={'A2': 'changed-environment'})
print(f'      final score {drift[-1]["score"]} (lost original {full[-1]["score"]}); every weight still came from history before its draw')

print('\n=== 6. The kernel\'s own check on every table used above: the stored factors have a fair-draw mean of at most 1')
print('  (factor_table refuses otherwise; none refused)')
