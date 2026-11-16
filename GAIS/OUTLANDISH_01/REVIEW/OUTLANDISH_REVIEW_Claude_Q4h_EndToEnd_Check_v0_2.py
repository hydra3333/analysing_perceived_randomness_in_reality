#!/usr/bin/env python3
"""OUTLANDISH_01 reviewer's Q4h end-to-end check, v0.2 (Claude, D4/D5 focused check).

Supersedes v0.1 for commits from b5f2ada (Q4k) onward. v0.1 checked the median
as the primary; since owner decision D4 the primary is the geometric-mean gap,
so v0.1 stops at the aggregate comparison on current code. v0.1 remains valid
evidence for commits b7ce6fd to 103d274.

Purpose
    Re-runnable evidence behind OUTLANDISH_REVIEW_003 and _006 memos.
    Drives the Q4h runner, report and aggregate modules at a realistic
    Powerball SHAPE (433 synthetic draws, about 200 planted events per
    constant, 10,000 permutations) and compares every result with the
    reviewer's own independent calculation.

What it checks
    1. Events from the Q4h runner equal the reviewer's own index oracle.
    2. Report: category counts, analytical expectation, evaluable pairs, and
       BOTH statistics from the same shuffles: the D4 primary (mean of
       log10(gap + 1)) and the secondary (median gap), each with observed
       value, permutation centre, centred two-sided p and both tails.
    3. Aggregate: two separate six-constant Holm families (primary and
       secondary) from REAL-like reports alone (no NULL).
    4. Positive control: one constant has planted hits for adjacent draws
       placed close together; its primary p must be small.
    4a. The D5 disclosure text in every report and in the aggregate equals
       the wording agreed on 16 Nov 2026, held independently in this script.
    4b. Cross-platform check: the primary values and p-values are compared
       with the reviewer's Linux values recorded below.
    5. Ordinary aggregate load is fast; explicit audit reproduces the report.
    6. Source corruption OUTSIDE the receipt's sampled blocks passes the
       preflight but is refused by the in-scan full digest, leaving the run
       INCOMPLETE with no event file.

What it does NOT do
    No REAL data: it never opens the published packed constants, receipts,
    POWERBALL_preholdout_only.csv, any results folder or any parent-project
    path. Draws, digits and receipts are fabricated in a TemporaryDirectory
    that is deleted on exit. Writes nothing into the repository.
    A PASS is reviewer evidence about synthetic behaviour only. It is not
    Q4 production qualification and not Q5 authorisation.

Usage (Windows CMD, from the repository root)
    ".venv\\Scripts\\python.exe" "GAIS\\OUTLANDISH_01\\REVIEW\\OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_1.py" --run

Expected final line
    REVIEWER Q4H END-TO-END PASS: constants=6 draws=433 permutations=10000 ...
and, just above it, "identical to the reviewer's Linux values: yes".

Run time was about 20 seconds for the reviewer; allow a minute or two (six
reports, each permutation test computed by Q4h and again independently).
Last run by the reviewer at commit b5f2ada45a1b897576eab625d79dc8d668e3d2d5
(Linux, Python 3.13.18, NumPy 2.5.3).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
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

FIRST_DRAW = 11          # fixture identifiers, far below the real era
DRAWS = 433              # same count as the real Powerball era; values are fabricated
DIGITS = 300_000         # 150,000 packed bytes: larger than the 12 x 4,096 sampled bytes
CLUSTERED = 'e'          # the positive-control constant

# Owner decision D5, wording agreed 16 Nov 2026 (independent copy for comparison).
D5_TEXT = (
    'Before the Powerball primary statistic was fixed, legacy match rows had been examined '
    'for phi (full 10^10 digits, 227 P3 rows) and for pi and phi (first 10^9 digits). '
    'On 5 November 2026 the signed P3->P3 gaps for the five adjacent draw pairs having P3 '
    'matches in those 10^9 prefixes (pi 3, phi 2) were computed and recorded in '
    'OUTLANDISH_01_2026-11-05_Historical_Status_and_Draft_Spec_v0_1.md section 5.2. '
    'No median, geometric-mean or permutation test of P3->P3 gaps appears in the reviewed '
    'project record. The D4 primary statistic was chosen on simulation evidence '
    '(REVIEW/OUTLANDISH_REVIEW_005_Claude_to_ChatGPT.md) without reference to these values. '
    'These exposures are disclosed; results are not represented as wholly blind.')
PRIMARY_NAME = 'P3_ANY_MEAN_LOG10_MIN_ABS_GAP_PLUS_ONE_V1'
SECONDARY_NAME = 'P3_ANY_MEDIAN_MIN_ABS_GAP_V1'

# Reviewer's Linux values at b5f2ada: (primary observed, primary p, secondary p).
REVIEWER_LINUX = {
    'pi': (4.595767612697, 0.145985401459854, 0.3414658534146585),
    'phi': (4.659329973255, 0.25537446255374463, 0.1867813218678132),
    'e': (3.928165878835, 9.999000099990002e-05, 9.999000099990002e-05),
    'log2': (4.729516887825, 0.6223377662233777, 0.0927907209279072),
    'gamma': (4.637034028106, 0.15258474152584742, 0.1411858814118588),
    'lemniscate': (4.737309268951, 0.46765323467653236, 0.9826017398260174),
}


def fixed2(values) -> str:
    return ''.join(f'{v:02d}' for v in values)


def write_source(G, roots, constant: str, digits: str) -> None:
    """Fabricated packed file plus a receipt in the converter's layout."""
    packed = bytes.fromhex(digits if len(digits) % 2 == 0 else digits + '0')
    path = roots.published_binary(constant)
    path.write_bytes(packed)
    plan = G.sample_plan(len(packed))
    record = {
        'format': G.FORMAT, 'format_version': 1, 'scope': G.SCOPE, 'constant': constant,
        'binary_name': path.name, 'digits_including_integer': len(digits),
        'packed_bytes': len(packed),
        'binary_sha256_streamed': hashlib.sha256(packed).hexdigest(),
        'sample_block_length': plan[0][1],
        'samples': [{'offset_bytes': o, 'size': n,
                     'sha256': hashlib.sha256(packed[o:o + n]).hexdigest()} for o, n in plan],
    }
    roots.receipt(constant).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')


def build_oracle(draws):
    """Reviewer's own lookup, built differently from the project's matcher."""
    k6s, k7 = {}, {}
    for number, mains, pb in draws:
        k7.setdefault(frozenset(mains), []).append((number, pb))
        for omitted in mains:
            key = (frozenset(m for m in mains if m != omitted), pb)
            k6s.setdefault(key, []).append(number)

    def oracle(ds: str):
        out = []
        for k in range(len(ds) - 13):
            v = [int(ds[k + 2*j:k + 2*j + 2]) for j in range(7)]
            six = frozenset(v[:6])
            if len(six) != 6:
                continue
            for number in k6s.get((six, v[6]), ()):
                out.append((number, 'K6S', k, ds[k:k + 14]))
            seven = frozenset(v)
            if len(seven) == 7:
                for number, pb in k7.get(seven, ()):
                    out.append((number, 'K7', k, ds[k:k + 14]))
                    if k + 16 <= len(ds) and int(ds[k + 14:k + 16]) == pb:
                        out.append((number, 'K7S', k, ds[k:k + 16]))
        return sorted(out, key=lambda t: (t[2], t[1], t[0]))
    return oracle


def pair_gaps(sets):
    return [min(abs(y - x) for x in a for y in b) for a, b in zip(sets, sets[1:]) if a and b]


def geometric(gaps):
    """D4 primary: mean of log10(gap + 1), exact sum, 12 decimal places."""
    return round(math.fsum(math.log10(g + 1) for g in sorted(gaps)) / len(gaps), 12)


def centred(observed, values, centre):
    n = len(values) + 1
    return {'centre': centre,
            'p': (1 + sum(abs(v - centre) >= abs(observed - centre) for v in values)) / n,
            'upper': (1 + sum(v >= observed for v in values)) / n,
            'lower': (1 + sum(v <= observed for v in values)) / n}


def holm(pvalues):
    running, out = 0.0, {}
    for rank, (constant, value) in enumerate(sorted(pvalues.items(), key=lambda kv: (kv[1], kv[0]))):
        running = max(running, min(1.0, (6 - rank) * value))
        out[constant] = running
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--run', action='store_true', required=True)
    parser.parse_args()

    import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
    import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S
    import OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1 as P
    import OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1 as R
    import OUTLANDISH_01_Q4h_Powerball_Test_Aggregate_v0_1 as A

    rng = random.Random(99)
    print(f'PROJECT: {PROJECT}')
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_REVIEW_Q4H_') as tmp:
        base = Path(tmp) / 'OUTLANDISH_Q4_SOURCE_SYNTHETIC_ONLY_reviewB'
        base.mkdir()
        (base / 'SYNTHETIC_MARKER').write_bytes(G.MAGIC)
        for name in ('digits', 'histories', 'results'):
            (base / name).mkdir()
        roots = G.FixedRoots.test_sandbox(base)

        draws = [(FIRST_DRAW + i, rng.sample(range(1, 36), 7), rng.randint(1, 20))
                 for i in range(DRAWS)]
        text = io.StringIO(newline='')
        writer = csv.writer(text, lineterminator='\n')
        writer.writerow(G.PB_HEADER)
        for number, mains, pb in draws:
            writer.writerow((number, '2000-01-01', *mains, pb))
        history = base / 'histories' / 'powerball_synthetic.csv'
        history.write_bytes(text.getvalue().encode('utf-8'))
        profile = G.HistoryProfile('powerball', history, FIRST_DRAW, FIRST_DRAW + DRAWS,
                                   G.PB_HEADER, True)
        oracle = build_oracle(draws)

        roster, my_p, my_secondary, seen = {}, {}, {}, {}
        for index, constant in enumerate(S.CONSTANTS):
            digits = [str(rng.randrange(10)) for _ in range(DIGITS)]
            for _ in range(215 + index):            # about the P3_any density of a 10^10 scan
                position_in_history = rng.randrange(DRAWS)
                number, mains, pb = draws[position_in_history]
                six = rng.sample(mains, 7)[:6]
                if constant == CLUSTERED and rng.random() < 0.5:
                    pos = (position_in_history * 600) % (DIGITS - 20)   # neighbours land close
                else:
                    pos = rng.randrange(DIGITS - 20)
                digits[pos:pos + 14] = list(fixed2(six) + fixed2([pb]))
            ds = ''.join(digits)
            write_source(G, roots, constant, ds)

            run_id = f'TEST_REAL_reviewB_{constant}'
            P.run_test_powerball(roots, profile, constant, run_id, digits=DIGITS,
                                 chunk_bytes=[None, 4096, 9999][index % 3])
            _meta, _raw, _hist, events, _cls = P.load_test_run(roots, profile, constant, run_id)
            expected = oracle(ds)
            got = [(e.draw_number, e.family, e.start_digit_offset, e.matched_digits) for e in events]
            if got != expected:
                raise AssertionError(f'{constant}: events differ from reviewer oracle')

            started = time.perf_counter()
            R.create_test_report(roots, profile, constant, run_id)
            report_seconds = time.perf_counter() - started
            report = R.load_test_report(roots, profile, constant, run_id)['report']

            per_draw = {n: set() for n, _, _ in draws}
            for number, family, start, _ in expected:
                if family == 'K6S':
                    per_draw[number].add(start)
            sets = [tuple(sorted(per_draw[n])) for n, _, _ in draws]   # empties kept
            observed_gaps = pair_gaps(sets)
            pairs = len(observed_gaps)
            obs_med, obs_geo = statistics.median(observed_gaps), geometric(observed_gaps)
            shuffler, meds, geos = random.Random(R.TEST_PRIMARY_SEED), [], []
            for _ in range(R.PERMUTATIONS):
                trial = list(sets)
                shuffler.shuffle(trial)             # one shuffle serves both statistics
                g = pair_gaps(trial)
                if g:
                    meds.append(statistics.median(g))
                    geos.append(geometric(g))
            med = centred(obs_med, meds, statistics.median(meds))
            geo = centred(obs_geo, geos, round(statistics.median(geos), 12))

            perm = report['permutation']
            prim, sec = perm['geometric_primary'], perm['median_secondary']
            views = {row['view']: row for row in report['category_summary']}
            checks = [
                perm['iterations_requested'] == 10_000,
                perm['observed_evaluable_pairs'] == pairs,
                perm['valid_permutations'] == len(meds) == len(geos),
                # secondary (median), including the retained legacy fields
                perm['observed_median'] == obs_med == sec['observed'],
                perm['centered_two_sided_p'] == med['p'] == sec['centered_two_sided_p'],
                sec['permuted_median_center'] == med['centre'],
                sec['tail_upper_inclusive'] == med['upper'], sec['tail_lower_inclusive'] == med['lower'],
                sec['statistic'] == SECONDARY_NAME,
                # primary (geometric mean), D4
                prim['statistic'] == PRIMARY_NAME,
                prim['observed'] == obs_geo,
                prim['permuted_median_center'] == geo['centre'],
                prim['centered_two_sided_p'] == geo['p'],
                prim['tail_upper_inclusive'] == geo['upper'], prim['tail_lower_inclusive'] == geo['lower'],
                report['transitions_summary']['observed_primary_mean_log10_gap_plus_one'] == obs_geo,
                report['primary_statistic'] == PRIMARY_NAME,
                report['secondary_statistic'] == SECONDARY_NAME,
                report['secondary_exploratory'] is True,
                report['legacy_exposure_disclosure'] == D5_TEXT,
                views['P3_any']['events'] == sum(t[1] == 'K6S' for t in expected),
                views['P2_any']['events'] == sum(t[1] == 'K7' for t in expected),
                views['P1_any']['events'] == sum(t[1] == 'K7S' for t in expected),
                views['P3_any']['draw_count'] == DRAWS,
                len(report['transitions']) == DRAWS - 1,
                abs(views['P3_any']['analytical_expected_events']
                    - DRAWS * 5040 * (DIGITS - 13) / 1e14) < 1e-12,
            ]
            if not all(checks):
                raise AssertionError(f'{constant}: report differs from reviewer calculation {checks}')
            p = geo['p']
            my_secondary[constant] = med['p']
            seen[constant] = (obs_geo, geo['p'], med['p'])
            roster[constant], my_p[constant] = run_id, p
            print(f'PASS {constant}: events={len(expected)} P3_any={views["P3_any"]["events"]} '
                  f'evaluable_pairs={pairs} primary={obs_geo:.12f} primary_p={p:.4f} '
                  f'median_gap={obs_med} secondary_p={med["p"]:.4f} '
                  f'report_seconds={report_seconds:.1f}')

        A.create_test_aggregate(roots, profile, 'TEST_AGGREGATE_reviewB', roster)
        started = time.perf_counter()
        aggregate = A.load_test_aggregate(roots, profile, 'TEST_AGGREGATE_reviewB')
        load_seconds = time.perf_counter() - started
        holm_primary, holm_secondary = holm(my_p), holm(my_secondary)
        for constant in S.CONSTANTS:
            entry = aggregate['per_constant'][constant]
            if (entry['raw_primary_p'] != my_p[constant]
                    or entry['raw_secondary_p'] != my_secondary[constant]
                    or abs(entry['holm_adjusted_p'] - holm_primary[constant]) > 1e-15
                    or abs(entry['holm_adjusted_secondary_p'] - holm_secondary[constant]) > 1e-15
                    or entry['observed_primary_mean_log10_gap_plus_one'] != seen[constant][0]):
                raise AssertionError(f'{constant}: aggregate differs from reviewer calculation')
        if (aggregate['null_comparison'] != 'NOT_RUN_OPTIONAL'
                or aggregate['primary_statistic'] != PRIMARY_NAME
                or aggregate['secondary_statistic'] != SECONDARY_NAME
                or aggregate['legacy_exposure_disclosure'] != D5_TEXT):
            raise AssertionError('aggregate identity, NULL independence or D5 text wrong')
        holm_p = holm_primary
        print('PASS aggregate: REAL-only; primary Holm = '
              + ', '.join(f'{c} {holm_primary[c]:.4f}' for c in S.CONSTANTS))
        print('                 secondary Holm = '
              + ', '.join(f'{c} {holm_secondary[c]:.4f}' for c in S.CONSTANTS)
              + f'; ordinary load {load_seconds:.2f}s')
        print('PASS D5 disclosure text identical in six reports and the aggregate')

        if not (my_p[CLUSTERED] < 0.01 and holm_p[CLUSTERED] < 0.05):
            raise AssertionError('positive control: planted adjacency was not detected')
        print(f'PASS positive control: planted adjacency in "{CLUSTERED}" gives '
              f'primary p={my_p[CLUSTERED]:.4f}, Holm={holm_p[CLUSTERED]:.4f}')

        if not R.audit_test_report(roots, profile, 'pi', roster['pi'])['science_matches']:
            raise AssertionError('explicit audit did not reproduce the stored report')
        print('PASS explicit audit reproduces the stored report')

        # Corruption outside the sampled blocks: only the in-scan digest can see it.
        path = roots.published_binary('pi')
        raw = bytearray(path.read_bytes())
        covered = set()
        for offset, length in G.sample_plan(len(raw)):
            covered.update(range(offset, offset + length))
        free = [i for i in range(len(raw)) if i not in covered]
        if not free:
            raise AssertionError('fixture too small: every byte is sampled')
        victim = free[len(free) // 2]
        raw[victim] = 0x11 if raw[victim] != 0x11 else 0x22       # still valid BCD
        path.write_bytes(bytes(raw))
        G.validate_published_source(roots, 'pi', fixture_digits=DIGITS)   # preflight passes
        try:
            P.run_test_powerball(roots, profile, 'pi', 'TEST_REAL_reviewB_corrupt', digits=DIGITS)
        except ValueError as exc:
            message = str(exc)
        else:
            raise AssertionError('corrupted source was accepted')
        folder = roots.run_location('TEST_REAL', 'TEST_REAL_reviewB_corrupt')
        status = json.loads((folder / 'run_manifest.json').read_text(encoding='utf-8'))['status']
        if status != 'INCOMPLETE' or (folder / 'raw_events.csv').exists():
            raise AssertionError('corrupt run must stay INCOMPLETE with no event file')
        print(f'PASS unsampled-byte corruption: sampled={len(covered)} of {len(raw)} bytes; '
              f'preflight passed, scan refused ("{message}"), run INCOMPLETE')

    if REVIEWER_LINUX:
        same = all(seen[c] == REVIEWER_LINUX[c] for c in REVIEWER_LINUX)
        print("identical to the reviewer's Linux values: " + ('yes' if same else
              'NO - please send this whole output to the reviewer'))
    else:
        print('VALUES', json.dumps(seen))
    print(f'REVIEWER Q4H END-TO-END PASS: constants=6 draws={DRAWS} permutations=10000 '
          'primary=geometric-mean secondary=median aggregate=REAL-only two-Holm-families '
          'D5-text=exact positive-control=detected corruption=refused')
    print('  SYNTHETIC ONLY; no REAL constants, receipts, histories or results read.')
    print('  Not Q4 production qualification; not Q5 authorisation.')


if __name__ == '__main__':
    main()
