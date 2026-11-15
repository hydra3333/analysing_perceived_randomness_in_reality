#!/usr/bin/env python3
"""Q4h six-constant Powerball REAL-like Holm, independent of NULL data.

Synthetic-only. Optional future NULL comparisons are a separate add-on, never
required for primary REAL Holm. Loads stored digest-verified reports, not MC.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S
import OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1 as P
import OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1 as R

SCHEMA = 'OUTLANDISH_Q4H_TEST_REAL_AGGREGATE_V1'


def _folder(roots, aggregate_id):
    if (not isinstance(aggregate_id, str) or not aggregate_id.startswith('TEST_AGGREGATE_')
            or len(aggregate_id) > 64 or not all(x.isalnum() or x in '_-' for x in aggregate_id)):
        raise ValueError('invalid synthetic aggregate identifier')
    return G._inside(roots.base, roots.base / 'reports_test_aggregate' / 'powerball' / aggregate_id)


def compute_test_aggregate(roots, profile, real_runs):
    P._test(roots, profile)
    if not isinstance(real_runs, dict) or set(real_runs) != set(S.CONSTANTS):
        raise ValueError('one REAL-like run per each of six constants is required')
    if len(set(real_runs.values())) != 6:
        raise ValueError('duplicate REAL-like run identity')
    entries, pvals, histories, digests, lengths = {}, {}, set(), set(), set()
    for const in S.CONSTANTS:
        view = R.load_test_report(roots, profile, const, real_runs[const])
        body = view['report']
        if body['primary_family'] != 'K6S':
            raise ValueError('primary family mismatch')
        primary = body['permutation']['centered_two_sided_p']
        if primary is not None and (type(primary) not in (int, float) or not 0 <= primary <= 1):
            raise ValueError('invalid primary p-value')
        pvals[const] = primary
        histories.add(body['history_sha256'])
        lengths.add(body['digits'])
        digests.add(body['source_sha256'])
        entries[const] = {'source_run': real_runs[const],
                          'report_sha256': hashlib.sha256(G._inside(roots.base, roots.run_location('TEST_REAL', real_runs[const]) / 'report.json').read_bytes()).hexdigest(),
                          'raw_primary_p': primary,
                          'observed_median_gap': body['permutation']['observed_median'],
                          'valid_permutations': body['permutation']['valid_permutations']}
    if len(histories) != 1 or len(lengths) != 1 or len(digests) != 6:
        raise ValueError('six reports must share history and N, and have distinct sources')
    corrected = S.holm_six_constants(pvals)
    for const in S.CONSTANTS:
        entries[const]['holm_adjusted_p'] = corrected[const]
    return {'schema': SCHEMA, 'game': 'powerball', 'run_type': 'TEST_REAL',
            'primary_family': 'K6S', 'permutations': R.PERMUTATIONS,
            'seed': R.TEST_PRIMARY_SEED, 'seed_status': 'PROVISIONAL_TEST_ONLY',
            'history_sha256': next(iter(histories)), 'digits': next(iter(lengths)),
            'holm_family': list(S.CONSTANTS), 'per_constant': entries,
            'null_comparison': 'NOT_RUN_OPTIONAL',
            'exploratory_no_Q5': True}


def create_test_aggregate(roots, profile, aggregate_id, real_runs):
    body = compute_test_aggregate(roots, profile, real_runs)
    dest = _folder(roots, aggregate_id)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.mkdir(exist_ok=False)
    body['aggregate_id'] = aggregate_id
    raw = P.encode(body)
    P.put_new(dest / 'aggregate.json', raw)
    P.put_new(dest / 'aggregate.sha256', (hashlib.sha256(raw).hexdigest() + '\n').encode('ascii'))
    return dest


def load_test_aggregate(roots, profile, aggregate_id):
    P._test(roots, profile)
    dest = _folder(roots, aggregate_id)
    raw = (G._inside(roots.base, dest / 'aggregate.json')).read_bytes()
    digest = (G._inside(roots.base, dest / 'aggregate.sha256')).read_bytes()
    if digest != (hashlib.sha256(raw).hexdigest() + '\n').encode('ascii'):
        raise ValueError('aggregate digest mismatch')
    body = json.loads(raw.decode('utf-8'))
    if (not isinstance(body, dict) or body.get('schema') != SCHEMA
            or body.get('game') != 'powerball' or body.get('run_type') != 'TEST_REAL'
            or body.get('aggregate_id') != aggregate_id or body.get('null_comparison') != 'NOT_RUN_OPTIONAL'
            or body.get('holm_family') != list(S.CONSTANTS)):
        raise ValueError('bad aggregate identity')
    roster = {c: body['per_constant'][c]['source_run'] for c in S.CONSTANTS}
    # Cheap verified-report digest loads; never redo permutations.
    verified = compute_test_aggregate(roots, profile, roster)
    verified['aggregate_id'] = aggregate_id
    if P.encode(verified) != raw:
        raise ValueError('aggregate differs from current verified source summaries')
    return body


if __name__ == '__main__':
    raise SystemExit('Q4h synthetic-only aggregate; no REAL/NULL production CLI')
