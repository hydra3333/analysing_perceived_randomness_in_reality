#!/usr/bin/env python3
"""Q4h Powerball REPORT: synthetic-only, 10,000 permutations, digest-load.

The provisional per-game seed below is for qualification only; no owner
ratification or REAL reporter is implied. An explicit audit recomputes science.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S
import OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1 as P

PERMUTATIONS = 10_000
TEST_PRIMARY_SEED = 271828  # PROVISIONAL; owner must approve REAL seed convention.
SCHEMA = 'OUTLANDISH_Q4H_TEST_REAL_REPORT_V1'
CODE_NAMES = ('OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py',
              'OUTLANDISH_01_Q3_Event_Classifier_v0_1.py',
              'OUTLANDISH_01_Q4d_Statistical_Core_v0_1.py',
              'OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1.py')


def _code_hashes():
    base = Path(__file__).absolute().parent
    return {name: hashlib.sha256((base / name).read_bytes()).hexdigest()
            for name in CODE_NAMES}


def compute_test_report(roots, profile, constant, run_id):
    meta, raw_manifest, hist, events, classified = P.load_test_run(
        roots, profile, constant, run_id)
    N = meta['digits']
    draws = tuple(i for i, _ in hist.draw_rows)
    rows, transition, sets = S.transitions('powerball', events, draws, N)
    return {
        'schema': SCHEMA, 'game': 'powerball', 'run_type': 'TEST_REAL',
        'constant': constant, 'run_id': run_id, 'digits': N,
        'source_sha256': meta['packed_sha256'],
        'history_sha256': hist.sha256,
        'event_sha256': meta['event_sha256'],
        'run_manifest_sha256': hashlib.sha256(raw_manifest).hexdigest(),
        'code_sha256_recorded_not_a_gate': _code_hashes(),
        'primary_family': 'K6S', 'primary_owner_vetoable': True,
        'permutations_predeclared': PERMUTATIONS,
        'seed': TEST_PRIMARY_SEED,
        'seed_status': 'PROVISIONAL_TEST_ONLY_OWNER_DECISION_PENDING',
        'category_summary': S.category_summary('powerball', classified, draws, N),
        'physical_same_draw_overlaps': S.physical_overlaps('powerball', events, draws, N),
        'transitions': rows, 'transitions_summary': transition,
        'permutation': S.permutation_test(sets, seed=TEST_PRIMARY_SEED,
                                           iterations=PERMUTATIONS),
    }


def create_test_report(roots, profile, constant, run_id):
    """Create once; digest file is the last, create-only publication step."""
    body = compute_test_report(roots, profile, constant, run_id)
    folder = roots.run_location('TEST_REAL', run_id)
    path = G._inside(roots.base, folder / 'report.json')
    digest_path = G._inside(roots.base, folder / 'report.sha256')
    if path.exists() or digest_path.exists():
        raise FileExistsError('report already exists or incomplete')
    raw = P.encode(body)
    P.put_new(path, raw)
    P.put_new(digest_path, (hashlib.sha256(raw).hexdigest() + '\n').encode('ascii'))
    return path


def load_test_report(roots, profile, constant, run_id):
    """Ordinary load checks digests and source identities, NO permutations."""
    meta, raw_manifest, _hist, _events, _classified = P.load_test_run(
        roots, profile, constant, run_id)
    folder = roots.run_location('TEST_REAL', run_id)
    raw = (G._inside(roots.base, folder / 'report.json')).read_bytes()
    recorded = (G._inside(roots.base, folder / 'report.sha256')).read_bytes()
    if recorded != (hashlib.sha256(raw).hexdigest() + '\n').encode('ascii'):
        raise ValueError('report SHA differs from create-only receipt')
    report = json.loads(raw.decode('utf-8'))
    required = {'schema': SCHEMA, 'game': 'powerball', 'run_type': 'TEST_REAL',
                'constant': constant, 'run_id': run_id, 'digits': meta['digits'],
                'source_sha256': meta['packed_sha256'],
                'history_sha256': meta['history_sha256'],
                'event_sha256': meta['event_sha256'],
                'run_manifest_sha256': hashlib.sha256(raw_manifest).hexdigest(),
                'primary_family': 'K6S', 'primary_owner_vetoable': True,
                'permutations_predeclared': PERMUTATIONS, 'seed': TEST_PRIMARY_SEED,
                'seed_status': 'PROVISIONAL_TEST_ONLY_OWNER_DECISION_PENDING'}
    if not isinstance(report, dict) or any(report.get(k) != v for k, v in required.items()):
        raise ValueError('report provenance/primary configuration mismatch')
    perm = report.get('permutation')
    if not isinstance(perm, dict) or perm.get('iterations_requested') != PERMUTATIONS \
            or perm.get('seed') != TEST_PRIMARY_SEED:
        raise ValueError('report permutation convention mismatch')
    return {'report': report,
            'code_matches_current': report.get('code_sha256_recorded_not_a_gate') ==
                                    _code_hashes()}


def _close(a, b):
    if isinstance(a, (int, float)) and not isinstance(a, bool) and isinstance(b, (int, float)) and not isinstance(b, bool):
        return math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-12)
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_close(a[k], b[k]) for k in a)
    if isinstance(a, (tuple, list)) and isinstance(b, (tuple, list)):
        return len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))
    return a == b


def audit_test_report(roots, profile, constant, run_id):
    """Opt-in recomputation; never silently invoked on ordinary report loads."""
    saved = load_test_report(roots, profile, constant, run_id)['report']
    fresh = compute_test_report(roots, profile, constant, run_id)
    # Code hashes may differ after an ordinary future code edit; not science.
    fresh['code_sha256_recorded_not_a_gate'] = saved.get('code_sha256_recorded_not_a_gate')
    return {'science_matches': _close(saved, fresh),
            'code_matches_current': saved.get('code_sha256_recorded_not_a_gate') == _code_hashes()}


if __name__ == '__main__':
    raise SystemExit('Synthetic-only Q4h report library: no production CLI')
