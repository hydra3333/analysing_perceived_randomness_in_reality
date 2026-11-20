"""Worked INVENTED examples for the OV-1 simplification amendment, DRAFT v0.2 (EX_253 section 5, B and D; EX_255 E01,
E02, E04). Design evidence only. Version 2 of the examples: who counts at a draw is read from release records that
carry DRAW NUMBERS, and every line gets a standing, SUPPORTED or QUALIFIED.

Everything here is invented: the barrel is 35 numbers, the draws 101 to 116 come from a hash, and the "methods" are toy
functions. No real draw, forecast, ledger or project record is read. The ONLY project code used is the passed
numerical kernel (src/evaluation/ov1_numeric.py of the staged slice-3 tree), imported unchanged, so the factors shown
are the certified ones the real recorder would store.

Usage:  python -B ov1_prevailing_examples_v2.py PATH_TO_STAGED_src
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


def as_of(releases, t: int) -> list:
    """The cohort as of draw t, from the release records alone: every variant a record with first draw <= t adds, less
    every variant a record with first draw <= t retires. No date, no clock, no roster of today."""
    live = set()
    for r in sorted(releases, key=lambda r: r['first']):
        if r['first'] <= t:
            live |= set(r.get('adds', ()))
            live -= set(r.get('retires', ()))
    return sorted(live)


def stream(releases, upto: int, *, known=None, lines=None, before=None, failed=(), not_run=(), flavour=None):
    """The prevailing stream from START (or continued from `lines`).
    releases: the release records as they finally stand. known: the records present when each line was computed (if
    some were reinstated only later). before: target -> True if its set was forecast before its draw. failed: (variant,
    target) with only a failure record. not_run: (variant, target) a cohort member that could not be run at all."""
    lines = list(lines or [])
    logs = [int(v) for v in lines[-1]['logs']] if lines else [0] * 6
    for t in range(lines[-1]['target'] + 1 if lines else START, upto + 1):
        early = (before or {}).get(t, True)
        ran = [v for v in as_of(known or releases, t) if (v, t) not in not_run]          # those with a weekly record
        pairs = {v: forecast(v, t, (flavour or {}).get(v, '')) for v in ran if (v, t) not in failed}
        classes = {'forecast_before_the_draw': len(pairs) if early else 0, 'caught_up_after_the_draw': 0 if early else len(pairs)}
        ln, logs = line(t, pairs, classes, logs)
        want = as_of(releases, t)
        why = []
        if sorted(ran) != want:
            why.append('cohort by the release records is not the set that was run: missing ' + ','.join(sorted(set(want) - set(ran))))
        if not early and any((v, t) in failed for v in ran):
            why.append('a failure record made after the result was on file')
        ln['standing'] = 'SUPPORTED' if not why else 'QUALIFIED (' + '; '.join(why) + ')'
        lines.append(ln)
    return lines


def maths(ln: dict) -> str:
    return json.dumps({k: ln[k] for k in ('target', 'counted_variants', 'weights', 'x', 'logs')}, sort_keys=True)


def show(title: str, lines, pick=None) -> None:
    if title:
        print(title)
    for ln in lines:
        if pick is None or ln['target'] in pick:
            c = ln['classes']
            print(f"  draw {ln['target']}: {len(ln['counted_variants'])} variants "
                  f"({c['forecast_before_the_draw']} before, {c['caught_up_after_the_draw']} caught up), "
                  + (f"X={ln['x']:+d} Z={ln['z']}" if ln['factor_one'] is None else f"factor 1 ({ln['factor_one']})")
                  + f", score {ln['score']}, {ln['standing']}")


def bound(lines) -> str:
    q = [ln['target'] for ln in lines if ln['standing'] != 'SUPPORTED']
    return 'the 2.5% bound is supported for the whole stream' if not q else f'the 2.5% bound is NOT certified from draw {q[0]} ({len(q)} qualified lines)'


def hits(variant: str, targets) -> int:
    return sum(len(set(forecast(variant, t)[0]) & set(drawn(t))) for t in targets)


def same(a, b) -> bool:
    return len(a) == len(b) and all(maths(x) == maths(y) for x, y in zip(a, b))


R0 = {'name': 'BASE', 'first': START, 'adds': BASE}        # the release that starts the score: its first draw is 101
R1 = {'name': 'NEW', 'first': 109, 'adds': ('NEW',)}       # made when the last draw on file was 108: first draw 108 + 1
RECS = [R0, R1]

print('=== 1. Ordinary weeks: five variants, draws 101 to 108, each forecast before its draw')
s1 = stream([R0], 108)
show('', s1)

print('\n=== 2. NEW is released when the last draw on file is 108: its release record says first draw 109')
full = stream(RECS, LAST)
print('  (a) the ranking is recomputed with NEW in it. TOP ticket, hits and chance (7*7/35 = 1.4 a draw):')
for label, rng in (('draws 101-108 (NEW: back-history, development evidence)', range(101, 109)),
                   ('draws 109-116 (NEW: forward)', range(109, 117))):
    row = sorted(((hits(v, rng), v) for v in BASE + ('NEW',)), reverse=True)
    print(f'      {label}: ' + ', '.join(f'{v} {h} hits ({h / len(rng):.2f} a draw)' for h, v in row))
print(f'  (b) prevailing stream, draws 101-108, before and after NEW was released: identical = {same(s1, full[:8])}')
show('  (c) prevailing stream, NEW counted from draw 109:', full, pick=(108, 109, 116))
retro = stream([dict(R0, adds=BASE + ('NEW',))], LAST)
print(f'  (d) EXPLORATORY retrospective view with NEW back-filled from 101 (never the prevailing score): '
      f'score after 108 = {retro[7]["score"]}, after 116 = {retro[-1]["score"]}')
print(f'      the prevailing score after 108 = {full[7]["score"]}, after 116 = {full[-1]["score"]}; {bound(full)}')

print('\n=== 3. A missed week: draw 111 was not forecast beforehand; the next session catches it up')
missed = stream(RECS, LAST, before={111: False})
print(f'  factors and score the same as if forecast beforehand: {same(full, missed)}; {bound(missed)}')
show('', missed, pick=(111,))

print('\n=== 4. Forecasts that are really missing')
a = stream(RECS, LAST, failed={('A3', 113)} | {(v, 114) for v in BASE + ('NEW',)})
show('  4a. failure records made BEFORE the draws (A3 at 113; every variant at 114):', a, pick=(113, 114))
print(f'      {bound(a)}')
b = stream(RECS, LAST, before={115: False}, failed={('A3', 115)})
show('  4b. draw 115 is caught up after its result is on file, and A3 fails in that catch-up:', b, pick=(115, 116))
print(f'      {bound(b)}')

print('\n=== 5. Restores (the lost draws are replayed under N-1 by the ordinary session)')
aft = {t: False for t in range(108, 117)}
r5a = stream(RECS, LAST, lines=full[:10], before=aft)
print(f'  5a. backup taken after draw 110: replay of 111-116 equals the lost originals: {same(full, r5a)}; {bound(r5a)}')
r5b1 = stream(RECS, LAST, lines=full[:7], before=aft)
print(f'  5b-i. OLDER backup, after draw 107, before NEW\'s release. NEW\'s release is put back from its saved record FIRST')
print(f'        (its first draw stays 109), then the catch-up runs: equals the lost originals: {same(full, r5b1)}; {bound(r5b1)}')
r5b2 = stream(RECS, LAST, known=[R0], lines=full[:7], before=aft)
print(f'  5b-ii. the same backup, but the catch-up is run BEFORE the release is put back: final score {r5b2[-1]["score"]} '
      f'(lost original {full[-1]["score"]});')
show('', r5b2, pick=(108, 109))
print(f'        {bound(r5b2)}')
r5c = stream(RECS, LAST, lines=full[:10], before=aft, flavour={'A2': 'changed-environment'})
print(f'  5c. as 5a, but A2 computes differently after a changed Python package: final score {r5c[-1]["score"]} '
      f'(lost original {full[-1]["score"]}); {bound(r5c)}')

print('\n=== 6. A revision is superseded: the release with first draw 113 retires A2 and adds A2R')
R2 = {'name': 'A2R', 'first': 113, 'adds': ('A2R',), 'retires': ('A2',)}
sup = stream(RECS + [R2], LAST)
show('  6a. ordinary operation: A2 counts through draw 112, A2R from 113:', sup, pick=(112, 113))
print(f'      {bound(sup)}')
r6 = stream(RECS + [R2], LAST, lines=sup[:10], before=aft, not_run={('A2', 111), ('A2', 112)})
show('  6b. restore from a backup taken after draw 110; the superseding release is put back, so A2\'s old code cannot run:', r6, pick=(111, 112, 113))
print(f'      {bound(r6)}')
