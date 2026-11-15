#!/usr/bin/env python3
"""Q4h production-shaped Powerball TEST harness, all files TemporaryDirectory.

--self-test: policy/refusal checks only. --run: real installed Q3 v0.4 matcher
against six tiny synthetic distinct sources, 10,000 permutations each, Holm
with NO NULL runs. No REAL input access or production CLI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4c_Synthetic_Processing_Qualification_v0_1 as F
import OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1 as OldP
import OUTLANDISH_01_Q4f_Final_Synthetic_Integration_v0_1 as Six
import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S
import OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1 as P
import OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1 as R
import OUTLANDISH_01_Q4h_Powerball_Test_Aggregate_v0_1 as A


def refuses(label, fn):
    try:
        fn()
    except (ValueError, RuntimeError, FileExistsError, TypeError, KeyError, FileNotFoundError):
        return 1
    raise AssertionError('expected refusal not raised: ' + label)


def altered(path, value, fn, label):
    original = path.read_bytes()
    try:
        path.write_bytes(value)
        return refuses(label, fn)
    finally:
        path.write_bytes(original)


def guards(roots, profile):
    n = 0
    n += refuses('cannot use REAL FixedRoots',
                 lambda: P._test(G.FixedRoots(roots.base, synthetic=False), profile))
    n += refuses('cannot switch to Oz history',
                 lambda: P._test(roots, OldP._historical_profile(roots, 'oz')))
    n += refuses('cannot choose external synthetic historical file',
                 lambda: P._test(roots, G.HistoryProfile('powerball',
                     roots.base/'histories'/'alternative.csv', 11, 14, G.PB_HEADER, True)))
    n += refuses('cannot accept genuine REAL type identifier',
                 lambda: roots.run_location('TEST_REAL', 'REAL_not_allowed'))
    n += refuses('cannot aggregate fewer than six constants',
                 lambda: A.compute_test_aggregate(roots, profile, {'pi': 'TEST_REAL_pi'}))
    assert R.PERMUTATIONS == 10_000 and R.TEST_PRIMARY_SEED == 271828
    return n


def integration(roots, profile, digits):
    source_sha = Six.seed_six_sources(roots, digits)
    roster = {}
    refusal_count = 0
    for i, const in enumerate(S.CONSTANTS):
        rid = f'TEST_REAL_q4h_{const}'
        folder = P.run_test_powerball(roots, profile, const, rid,
                                      digits=digits, chunk_bytes=9)
        run, _, _, events, _ = P.load_test_run(roots, profile, const, rid)
        assert run['status'] == 'COMPLETE' and run['packed_sha256'] == source_sha[const]
        assert run['bytes_hashed'] == (digits+1)//2 and len(events) == run['event_count']
        R.create_test_report(roots, profile, const, rid)
        view = R.load_test_report(roots, profile, const, rid)
        assert view['code_matches_current']
        report = view['report']
        assert report['permutation']['iterations_requested'] == 10_000
        assert report['primary_family'] == 'K6S' and report['game'] == 'powerball'
        assert R.audit_test_report(roots, profile, const, rid)['science_matches']
        roster[const] = rid
        refusal_count += refuses('create-only run', lambda const=const, rid=rid:
            P.run_test_powerball(roots, profile, const, rid, digits=digits))
        refusal_count += refuses('create-only report', lambda const=const, rid=rid:
            R.create_test_report(roots, profile, const, rid))

    aggregate_id = 'TEST_AGGREGATE_powerball_q4h_01'
    aggregate_path = A.create_test_aggregate(roots, profile, aggregate_id, roster)
    aggregate = A.load_test_aggregate(roots, profile, aggregate_id)
    assert aggregate['null_comparison'] == 'NOT_RUN_OPTIONAL'
    assert aggregate['holm_family'] == list(S.CONSTANTS)
    refusal_count += refuses('create-only aggregate', lambda:
                            A.create_test_aggregate(roots, profile, aggregate_id, roster))
    refusal_count += refuses('cross-constant report', lambda:
                R.load_test_report(roots, profile, 'pi', roster['e']))

    # Code changes should be reported as advisory, NOT reject historical reports.
    old_codes = R._code_hashes
    R._code_hashes = lambda: {'changed': 'changed'}
    try:
        assert R.load_test_report(roots, profile, 'phi', roster['phi'])['code_matches_current'] is False
        assert A.load_test_aggregate(roots, profile, aggregate_id)['permutations'] == 10000
    finally:
        R._code_hashes = old_codes

    # Ordinary loads must NOT re-run 10,000 permutations; audit is explicit.
    original_perm = S.permutation_test
    S.permutation_test = lambda *a, **k: (_ for _ in ()).throw(
        AssertionError('ordinary load unexpectedly recomputed permutations'))
    try:
        R.load_test_report(roots, profile, 'phi', roster['phi'])
        A.load_test_aggregate(roots, profile, aggregate_id)
    finally:
        S.permutation_test = original_perm

    # Replay after all six packed sources disappear: no binary opens/rehashing.
    renamed = []
    try:
        for const in S.CONSTANTS:
            src = roots.published_binary(const)
            absent = src.with_name(src.name+'.absent_for_replay')
            src.rename(absent)
            renamed.append((src, absent))
        for const in S.CONSTANTS:
            R.load_test_report(roots, profile, const, roster[const])
        A.load_test_aggregate(roots, profile, aggregate_id)
    finally:
        for src, absent in reversed(renamed):
            absent.rename(src)

    good = lambda: R.load_test_report(roots, profile, 'pi', roster['pi'])
    folder = roots.run_location('TEST_REAL', roster['pi'])
    path = folder/'report.json'
    refusal_count += altered(path, path.read_bytes()+b' ', good, 'report digest tamper')
    path = folder/'raw_events.csv'
    refusal_count += altered(path, path.read_bytes()+b'FAKE\n', good, 'event digest tamper')
    path = folder/'run_manifest.json'
    refusal_count += altered(path, path.read_bytes()+b' ', good, 'manifest provenance tamper')
    path = roots.receipt('pi')
    refusal_count += altered(path, path.read_bytes()+b' ', good, 'receipt tamper')
    path = profile.source
    refusal_count += altered(path, path.read_bytes()+b'\n', good, 'historical drawset tamper')
    path = aggregate_path/'aggregate.json'
    refusal_count += altered(path, path.read_bytes()+b' ', lambda:
                            A.load_test_aggregate(roots, profile, aggregate_id),
                            'aggregate digest tamper')

    failed_id = 'TEST_REAL_q4h_injected_failure'
    refusal_count += refuses('injected precompletion failure', lambda:
                            P.run_test_powerball(roots, profile, 'pi', failed_id,
                                                 digits=digits, inject_failure=True, chunk_bytes=9))
    failed = roots.run_location('TEST_REAL', failed_id)
    assert json.loads((failed/'run_manifest.json').read_text())['status'] == 'INCOMPLETE'
    refusal_count += refuses('cannot load INCOMPLETE run', lambda:
                            P.load_test_run(roots, profile, 'pi', failed_id))
    return len(roster), 6, 1, refusal_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--self-test', action='store_true')
    mode.add_argument('--run', action='store_true')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q4H_ISOLATED_') as tmp:
        roots, n = F.make_temp(Path(tmp))
        profile = OldP._historical_profile(roots, 'powerball')
        refusal_count = guards(roots, profile)
        runs = reports = aggregates = 0
        if args.run:
            runs, reports, aggregates, refused = integration(roots, profile, n)
            refusal_count += refused
    print(f'Q4H POWERBALL SYNTHETIC {"INTEGRATION" if args.run else "GUARDS"} PASS: '
          f'runs={runs} reports={reports} aggregates={aggregates} '
          f'guard-refusals={refusal_count} permutations-per-report=10000 '
          'production-scans=0 REAL-history-reads=0')


if __name__ == '__main__':
    main()
