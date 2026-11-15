#!/usr/bin/env python3
"""OUTLANDISH_01 reviewer's Q4h end-to-end check, v0.1 (Claude, review point B).

Purpose
    Re-runnable evidence behind OUTLANDISH_REVIEW_003_Claude_to_ChatGPT.md.
    Drives the Q4h runner, report and aggregate modules at a realistic
    Powerball SHAPE (433 synthetic draws, about 200 planted events per
    constant, 10,000 permutations) and compares every result with the
    reviewer's own independent calculation.

What it checks
    1. Events from the Q4h runner equal the reviewer's own index oracle.
    2. Report: category counts, analytical expectation, evaluable pairs,
       observed median gap and the centred two-sided permutation p.
    3. Aggregate: six-constant Holm from REAL-like reports alone (no NULL).
    4. Positive control: one constant has planted hits for adjacent draws
       placed close together; its primary p must be small.
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

Run time was about 20 seconds for the reviewer; allow a minute or two (six
reports, each permutation test computed by Q4h and again independently).
Last run by the reviewer at commit b7ce6fd052d65186b7e4d338260aebf054188e45
(Linux, Python 3.13.18, NumPy 2.5.3).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
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


def median_gap(sets):
    gaps = [min(abs(y - x) for x in a for y in b) for a, b in zip(sets, sets[1:]) if a and b]
    return (statistics.median(gaps) if gaps else None), len(gaps)


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

        roster, my_p = {}, {}
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
            observed, pairs = median_gap(sets)
            shuffler, valid = random.Random(R.TEST_PRIMARY_SEED), []
            for _ in range(R.PERMUTATIONS):
                trial = list(sets)
                shuffler.shuffle(trial)
                value, _ = median_gap(trial)
                if value is not None:
                    valid.append(value)
            centre = statistics.median(valid)
            p = (1 + sum(abs(v - centre) >= abs(observed - centre) for v in valid)) / (len(valid) + 1)

            perm = report['permutation']
            views = {row['view']: row for row in report['category_summary']}
            checks = [
                perm['iterations_requested'] == 10_000,
                perm['observed_median'] == observed,
                perm['observed_evaluable_pairs'] == pairs,
                perm['valid_permutations'] == len(valid),
                perm['centered_two_sided_p'] == p,
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
            roster[constant], my_p[constant] = run_id, p
            print(f'PASS {constant}: events={len(expected)} P3_any={views["P3_any"]["events"]} '
                  f'evaluable_pairs={pairs} median_gap={observed} p={p:.4f} '
                  f'report_seconds={report_seconds:.1f}')

        A.create_test_aggregate(roots, profile, 'TEST_AGGREGATE_reviewB', roster)
        started = time.perf_counter()
        aggregate = A.load_test_aggregate(roots, profile, 'TEST_AGGREGATE_reviewB')
        load_seconds = time.perf_counter() - started
        running, holm = 0.0, {}
        for rank, (constant, value) in enumerate(sorted(my_p.items(), key=lambda kv: (kv[1], kv[0]))):
            running = max(running, min(1.0, (6 - rank) * value))
            holm[constant] = running
        for constant in S.CONSTANTS:
            entry = aggregate['per_constant'][constant]
            if entry['raw_primary_p'] != my_p[constant] or abs(entry['holm_adjusted_p'] - holm[constant]) > 1e-15:
                raise AssertionError(f'{constant}: Holm differs from reviewer calculation')
        if aggregate['null_comparison'] != 'NOT_RUN_OPTIONAL':
            raise AssertionError('aggregate must not depend on NULL')
        print('PASS aggregate: REAL-only Holm = '
              + ', '.join(f'{c} {holm[c]:.4f}' for c in S.CONSTANTS)
              + f'; ordinary load {load_seconds:.2f}s')

        if not (my_p[CLUSTERED] < 0.01 and holm[CLUSTERED] < 0.05):
            raise AssertionError('positive control: planted adjacency was not detected')
        print(f'PASS positive control: planted adjacency in "{CLUSTERED}" gives '
              f'p={my_p[CLUSTERED]:.4f}, Holm={holm[CLUSTERED]:.4f}')

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

    print(f'REVIEWER Q4H END-TO-END PASS: constants=6 draws={DRAWS} permutations=10000 '
          'aggregate=REAL-only positive-control=detected corruption=refused')
    print('  SYNTHETIC ONLY; no REAL constants, receipts, histories or results read.')
    print('  Not Q4 production qualification; not Q5 authorisation.')


if __name__ == '__main__':
    main()
