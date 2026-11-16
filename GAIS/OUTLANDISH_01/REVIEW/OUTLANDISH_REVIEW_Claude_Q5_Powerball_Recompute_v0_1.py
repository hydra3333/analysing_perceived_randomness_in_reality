#!/usr/bin/env python3
"""OUTLANDISH_01 reviewer's independent recomputation of Powerball Q5, v0.1 (Claude, memo 007).

Purpose
    Evidence behind OUTLANDISH_REVIEW_007_Claude_to_ChatGPT.md. It re-derives
    every figure in the six Powerball REAL reports and the six-constant
    aggregate from the raw event files, using the reviewer's own code and none
    of the project's matching, classification or statistics modules.

What it checks
    1. Identity: each run is COMPLETE and REAL, covers 10^10 digits and
       5,000,000,000 hashed bytes, and carries the source SHA-256 recorded on
       14 Nov 2026 and the pinned history SHA-256. Event, report and aggregate
       digests match. Seeds follow owner decision D1. 10,000 permutations.
    2. Soundness: every event satisfies its family rule against the genuine
       pre-holdout Powerball draw it is attributed to.
    3. Category counts, including the drawn-order views.
    4. Both statistics (D4 primary: mean of log10(gap + 1); secondary: median
       gap) with centre, two-sided p and tails, from the same 10,000 shuffles.
    5. Both six-constant Holm families in the aggregate.

What it does NOT do
    It cannot check completeness (that no match was missed): that needs the
    5 GB constants. Completeness evidence is the phi known-answer comparison
    (227 of 227) and the synthetic qualification. It does not open the packed
    constants, starts no scan, needs no switch and writes nothing.
    It READS the genuine results and POWERBALL_preholdout_only.csv, so run it
    only on results from an owner-authorised Q5.

Usage (Windows CMD, from the repository root)
    ".venv\\Scripts\\python.exe" "GAIS\\OUTLANDISH_01\\REVIEW\\OUTLANDISH_REVIEW_Claude_Q5_Powerball_Recompute_v0_1.py" --results-dir "G:\\OUTLANDISH_01\\large_artifacts\\results"

Expected final line
    REVIEWER Q5 POWERBALL RECOMPUTATION PASS: six reports and aggregate identical ...

Run by the reviewer on a copy of the owner's results of 16 Nov 2026 (code
commit f939652; Linux, Python 3.13.18): PASS. About one minute.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HISTORY_DEFAULT = Path(__file__).absolute().parent.parent / 'POWERBALL_preholdout_only.csv'
HISTORY_SHA256 = 'c71039c63f64479b2d83c10e8df3ad5e7525091b3a7f44c5a2680015f4fd2e54'
SOURCE_SHA256 = {
    'pi': '62ab5b9a511eb0fcf5d09717df9ee51f8bd29ea09acf379e6f1045c537ababe2',
    'phi': 'dd80be0c3fdb330fe4e1780c2d53bf03bde297a5dea83b5785cd3349838ad36d',
    'e': '522f088b013432f775098df863b851ad87a4f5d0f0296b54cb00d6f13f72720f',
    'log2': '6993b8b6c6f46ae13b5e213aae0d46e784c8acae510f10e6862aecde83a15694',
    'gamma': '68e4a47d27759632dd8c608af973fa5bd22fb2aa7290d5e92f59e485ceb85e6a',
    'lemniscate': '958210dcda823fd1951b8487fbfe3cb98aeda9748c2b0dea4db9684608d21369',
}
CONSTANTS = tuple(SOURCE_SHA256)
N = 10**10
LENGTH = {'K7S': 16, 'K7': 14, 'K6S': 14}
PRIMARY = 'P3_ANY_MEAN_LOG10_MIN_ABS_GAP_PLUS_ONE_V1'
SECONDARY = 'P3_ANY_MEDIAN_MIN_ABS_GAP_V1'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def need(condition, message: str) -> None:
    if not condition:
        raise SystemExit('REVIEWER Q5 RECOMPUTATION FAIL: ' + message)


def seed_for(constant: str):
    label = f'OUTLANDISH_01|powerball|{constant}|PRIMARY_W_TO_W1|V1'
    return label, int.from_bytes(hashlib.sha256(label.encode('ascii')).digest()[:8], 'big')


def geometric(gaps):
    return round(math.fsum(math.log10(g + 1) for g in sorted(gaps)) / len(gaps), 12)


def pair_gaps(sets):
    return [min(abs(y - x) for x in a for y in b) for a, b in zip(sets, sets[1:]) if a and b]


def is_subsequence(short, long):
    it = iter(long)
    return all(x in it for x in short)


def holm(pvalues):
    running, out = 0.0, {}
    for rank, (constant, value) in enumerate(sorted(pvalues.items(), key=lambda kv: (kv[1], kv[0]))):
        running = max(running, min(1.0, (6 - rank) * value))
        out[constant] = running
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--results-dir', required=True,
                        help='folder holding REAL_<constant>_<suffix> and the aggregate folder')
    parser.add_argument('--suffix', default='q5_v1', help='run suffix (default q5_v1)')
    parser.add_argument('--history', default=str(HISTORY_DEFAULT))
    args = parser.parse_args()
    results, history = Path(args.results_dir), Path(args.history)
    need(sha(history) == HISTORY_SHA256, 'history file is not the pinned pre-holdout file')
    rows = list(csv.reader(history.open(encoding='utf-8-sig')))[1:]
    draws = {int(r[0]): ([int(x) for x in r[2:9]], int(r[9])) for r in rows}
    ids = sorted(draws)
    need(ids == list(range(1144, 1577)), 'history is not exactly draws 1144 to 1576')

    aggregate_dir = results / f'REAL_AGGREGATE_powerball_{args.suffix}'
    aggregate = json.loads((aggregate_dir / 'aggregate.json').read_text(encoding='utf-8'))
    need((aggregate_dir / 'aggregate.sha256').read_text().strip() == sha(aggregate_dir / 'aggregate.json'),
         'aggregate digest')
    need(aggregate['run_type'] == 'REAL' and aggregate['null_comparison'] == 'NOT_RUN_OPTIONAL'
         and aggregate['primary_statistic'] == PRIMARY and aggregate['secondary_statistic'] == SECONDARY,
         'aggregate identity')

    primary_p, secondary_p, table = {}, {}, {}
    for constant in CONSTANTS:
        folder = results / f'REAL_{constant}_{args.suffix}'
        manifest = json.loads((folder / 'run_manifest.json').read_text(encoding='utf-8'))
        report = json.loads((folder / 'report.json').read_text(encoding='utf-8'))
        label, seed = seed_for(constant)
        need(manifest['status'] == 'COMPLETE' and manifest['run_type'] == 'REAL'
             and manifest['constant'] == constant and manifest['game'] == 'powerball', f'{constant}: manifest identity')
        need(manifest['digits'] == N and manifest['bytes_hashed'] == N // 2, f'{constant}: coverage')
        need(manifest['packed_sha256'] == SOURCE_SHA256[constant], f'{constant}: source SHA-256')
        need(manifest['history_sha256'] == HISTORY_SHA256, f'{constant}: history SHA-256')
        need(sha(folder / 'raw_events.csv') == manifest['event_sha256'], f'{constant}: event digest')
        need((folder / 'report.sha256').read_text().strip() == sha(folder / 'report.json'), f'{constant}: report digest')
        need(report['run_manifest_sha256'] == sha(folder / 'run_manifest.json')
             and report['event_sha256'] == manifest['event_sha256']
             and report['source_sha256'] == manifest['packed_sha256'], f'{constant}: report provenance')
        need(report['seed_label'] == label and report['seed'] == seed == report['permutation']['seed']
             and report['seed_status'] == 'OWNER_APPROVED_DETERMINISTIC_V1', f'{constant}: D1 seed')
        need(report['permutations_predeclared'] == 10_000
             and report['permutation']['iterations_requested'] == 10_000, f'{constant}: permutation count')
        need(report['primary_statistic'] == PRIMARY and report['secondary_statistic'] == SECONDARY,
             f'{constant}: statistic names')
        need(report['legacy_exposure_disclosure'] == aggregate['legacy_exposure_disclosure']
             and report['legacy_exposure_disclosure'].startswith('Before the Powerball primary statistic was fixed'),
             f'{constant}: D5 disclosure')
        need(aggregate['per_constant'][constant]['report_sha256'] == sha(folder / 'report.json'),
             f'{constant}: aggregate report digest')

        events = [(int(d), fam, int(o), s) for d, fam, o, s in
                  list(csv.reader((folder / 'raw_events.csv').open(encoding='utf-8')))[1:]]
        need(events == sorted(events, key=lambda t: (t[2], t[1], t[0]))
             and len({(d, fam, o) for d, fam, o, _ in events}) == len(events)
             and len(events) == manifest['event_count'], f'{constant}: event order, identity or count')
        counts = dict(P1_any=0, P1_drawn=0, P2_any=0, P2_drawn=0, P3_any=0, P3_subsequence=0)
        for d, fam, o, s in events:
            mains, pb = draws[d]
            v = [int(s[i:i + 2]) for i in range(0, len(s), 2)]
            need(len(s) == LENGTH[fam] and 0 <= o and o + LENGTH[fam] <= N, f'{constant}: event bounds')
            if fam == 'K7S':
                ok = len(set(v[:7])) == 7 and set(v[:7]) == set(mains) and v[7] == pb
                counts['P1_any'] += 1
                counts['P1_drawn'] += v[:7] == mains
            elif fam == 'K7':
                ok = len(set(v)) == 7 and set(v) == set(mains)
                counts['P2_any'] += 1
                counts['P2_drawn'] += v == mains
            else:
                ok = len(set(v[:6])) == 6 and set(v[:6]) <= set(mains) and v[6] == pb
                counts['P3_any'] += 1
                counts['P3_subsequence'] += is_subsequence(v[:6], mains)
            need(ok, f'{constant}: event at offset {o} violates its rule for draw {d}')
        views = {row['view']: row for row in report['category_summary']}
        need(all(views[k]['events'] == v for k, v in counts.items()), f'{constant}: category counts')

        per_draw = {i: set() for i in ids}
        for d, fam, o, _ in events:
            if fam == 'K6S':
                per_draw[d].add(o)
        sets = [tuple(sorted(per_draw[i])) for i in ids]          # zero-match draws kept
        gaps = pair_gaps(sets)
        obs_geo, obs_med = geometric(gaps), statistics.median(gaps)
        shuffler, geos, meds = random.Random(seed), [], []
        for _ in range(10_000):
            trial = list(sets)
            shuffler.shuffle(trial)
            g = pair_gaps(trial)
            if g:
                geos.append(geometric(g))
                meds.append(statistics.median(g))
        centre_geo, centre_med, n = round(statistics.median(geos), 12), statistics.median(meds), len(geos) + 1
        p_geo = (1 + sum(abs(x - centre_geo) >= abs(obs_geo - centre_geo) for x in geos)) / n
        p_med = (1 + sum(abs(x - centre_med) >= abs(obs_med - centre_med) for x in meds)) / n
        lower = (1 + sum(x <= obs_geo for x in geos)) / n
        upper = (1 + sum(x >= obs_geo for x in geos)) / n
        prim = report['permutation']['geometric_primary']
        sec = report['permutation']['median_secondary']
        need((prim['observed'], prim['permuted_median_center'], prim['centered_two_sided_p'],
              prim['tail_lower_inclusive'], prim['tail_upper_inclusive'])
             == (obs_geo, centre_geo, p_geo, lower, upper), f'{constant}: primary statistic')
        need((sec['observed'], sec['permuted_median_center'], sec['centered_two_sided_p'])
             == (obs_med, centre_med, p_med), f'{constant}: secondary statistic')
        need(report['permutation']['observed_evaluable_pairs'] == len(gaps)
             and report['permutation']['valid_permutations'] == len(geos), f'{constant}: pair or validity counts')
        primary_p[constant], secondary_p[constant] = p_geo, p_med
        table[constant] = (counts, len(gaps), 10 ** obs_geo, 10 ** centre_geo, p_geo, obs_med, p_med, min(gaps))

    holm_primary, holm_secondary = holm(primary_p), holm(secondary_p)
    for constant in CONSTANTS:
        entry = aggregate['per_constant'][constant]
        need(entry['raw_primary_p'] == primary_p[constant] and entry['raw_secondary_p'] == secondary_p[constant]
             and abs(entry['holm_adjusted_p'] - holm_primary[constant]) < 1e-15
             and abs(entry['holm_adjusted_secondary_p'] - holm_secondary[constant]) < 1e-15,
             f'{constant}: aggregate p-values or Holm')

    expected = 433 * 5040 * (N - 13) / 1e14
    print(f'expected per constant under random digits: P3_any {expected:.1f}, P2_any {expected:.1f}, '
          f'P1_any {433 * 5040 * (N - 15) / 1e16:.2f}')
    print(f'{"constant":<11}{"P1any":>6}{"P2any":>6}{"P3any":>6}{"drawn":>6}{"pairs":>6} | '
          f'{"geo-mean gap":>14}{"chance":>14}{"raw p":>8}{"Holm":>7} | {"median gap":>14}{"raw p":>8}{"Holm":>7} | {"min gap":>12}')
    for constant in CONSTANTS:
        c, pairs, gm, gmc, pg, med, pm, mn = table[constant]
        drawn = c['P1_drawn'] + c['P2_drawn'] + c['P3_subsequence']
        print(f'{constant:<11}{c["P1_any"]:>6}{c["P2_any"]:>6}{c["P3_any"]:>6}{drawn:>6}{pairs:>6} | '
              f'{gm:>14,.0f}{gmc:>14,.0f}{pg:>8.4f}{holm_primary[constant]:>7.4f} | '
              f'{med:>14,.0f}{pm:>8.4f}{holm_secondary[constant]:>7.4f} | {mn:>12,}')
    print('REVIEWER Q5 POWERBALL RECOMPUTATION PASS: six reports and aggregate identical to the '
          f'reviewer\'s independent calculation; smallest primary Holm p = {min(holm_primary.values()):.4f}')
    print('  Soundness and statistics verified from raw events. Completeness is not checkable here.')


if __name__ == '__main__':
    main()
