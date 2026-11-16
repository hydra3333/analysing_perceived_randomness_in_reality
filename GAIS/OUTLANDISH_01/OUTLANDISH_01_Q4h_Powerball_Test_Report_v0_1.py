#!/usr/bin/env python3
"""Shared Q4h Powerball report for TEST_REAL or (later authorised) REAL.

Qualified primary is 10,000 whole-draw permutations. Only REAL mode uses the
owner-approved deterministic per-(game,constant) seed. Ordinary loads do not
recompute; explicit audit does. Historical code hashes are advisory.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S
import OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1 as P
import OUTLANDISH_01_Q4i_Mode_v0_1 as M

PERMUTATIONS = 10_000
TEST_PRIMARY_SEED = 271828  # retained only for historical synthetic regressions
SCHEMA = 'OUTLANDISH_Q4H_POWERBALL_REPORT_V3'
PRIMARY_STATISTIC = S.GEOMETRIC_PRIMARY
SECONDARY_STATISTIC = S.MEDIAN_SECONDARY
D5_LEGACY_EXPOSURE_DISCLOSURE = (
    'Before the Powerball primary statistic was fixed, legacy match rows had been examined for phi (full '
    '10^10 digits, 227 P3 rows) and for pi and phi (first 10^9 digits). On 5 November 2026 the signed P3-'
    '>P3 gaps for the five adjacent draw pairs having P3 matches in those 10^9 prefixes (pi 3, phi 2) wer'
    'e computed and recorded in OUTLANDISH_01_2026-11-05_Historical_Status_and_Draft_Spec_v0_1.md section'
    ' 5.2. No median, geometric-mean or permutation test of P3->P3 gaps appears in the reviewed project r'
    'ecord. The D4 primary statistic was chosen on simulation evidence (REVIEW/OUTLANDISH_REVIEW_005_Clau'
    'de_to_ChatGPT.md) without reference to these values. These exposures are disclosed; results are not '
    'represented as wholly blind.'
)
CODE_NAMES = ('OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py',
              'OUTLANDISH_01_Q3_Event_Classifier_v0_1.py',
              'OUTLANDISH_01_Q4d_Statistical_Core_v0_1.py',
              'OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1.py')


def _code_hashes():
    base = Path(__file__).absolute().parent
    return {name: hashlib.sha256((base / name).read_bytes()).hexdigest()
            for name in CODE_NAMES}


def primary_seed(game: str, constant: str) -> tuple[str, int]:
    if game not in ('powerball', 'oz') or constant not in S.CONSTANTS:
        raise ValueError('unknown game/constant for primary seed')
    label = f'OUTLANDISH_01|{game}|{constant}|PRIMARY_W_TO_W1|V1'
    digest = hashlib.sha256(label.encode('ascii')).digest()
    return label, int.from_bytes(digest[:8], byteorder='big')


def _seed(mode, constant):
    if mode.roots.synthetic:
        return 'PROVISIONAL_SYNTHETIC_271828', TEST_PRIMARY_SEED, 'SYNTHETIC_TEST_ONLY'
    label, number = primary_seed('powerball', constant)
    return label, number, 'OWNER_APPROVED_DETERMINISTIC_V1'


def compute_report(mode: M.PowerballMode, constant: str, run_id: str):
    mode = mode.checked()
    meta, raw_manifest, hist, events, classified = P.load_run(mode, constant, run_id)
    N = mode.digits
    draws = tuple(i for i, _ in hist.draw_rows)
    rows, transition, sets = S.transitions('powerball', events, draws, N)
    label, seed, status = _seed(mode, constant)
    return {
        'schema': SCHEMA, 'game': 'powerball', 'run_type': mode.run_type,
        'constant': constant, 'run_id': run_id, 'digits': N,
        'source_sha256': meta['packed_sha256'],
        'history_sha256': hist.sha256,
        'event_sha256': meta['event_sha256'],
        'run_manifest_sha256': hashlib.sha256(raw_manifest).hexdigest(),
        'code_sha256_recorded_not_a_gate': _code_hashes(),
        'primary_family': 'K6S', 'primary_owner_vetoable': False,
        'primary_statistic': PRIMARY_STATISTIC,
        'secondary_statistic': SECONDARY_STATISTIC,
        'secondary_exploratory': True,
        'legacy_exposure_disclosure': D5_LEGACY_EXPOSURE_DISCLOSURE,
        'permutations_predeclared': PERMUTATIONS,
        'seed_label': label, 'seed': seed, 'seed_status': status,
        'category_summary': S.category_summary('powerball', classified, draws, N),
        'physical_same_draw_overlaps': S.physical_overlaps('powerball', events, draws, N),
        'transitions': rows, 'transitions_summary': transition,
        'permutation': S.permutation_test(sets, seed=seed, iterations=PERMUTATIONS,
                                          geometric_primary=True),
    }


def create_report(mode: M.PowerballMode, constant: str, run_id: str):
    body = compute_report(mode, constant, run_id)
    roots = mode.roots
    folder = roots.run_location(mode.run_type, run_id)
    path = G._inside(roots.base, folder / 'report.json')
    digest_path = G._inside(roots.base, folder / 'report.sha256')
    if path.exists() or digest_path.exists():
        raise FileExistsError('report already exists or incomplete')
    raw = P.encode(body)
    P.put_new(path, raw)
    P.put_new(digest_path, (hashlib.sha256(raw).hexdigest() + '\n').encode('ascii'))
    return path


def load_report(mode: M.PowerballMode, constant: str, run_id: str):
    """Digest/identity only, with NO automatic Monte Carlo recomputation."""
    mode = mode.checked()
    meta, raw_manifest, _hist, _events, _classified = P.load_run(mode, constant, run_id)
    roots = mode.roots
    folder = roots.run_location(mode.run_type, run_id)
    raw = G._inside(roots.base, folder / 'report.json').read_bytes()
    receipt = G._inside(roots.base, folder / 'report.sha256').read_bytes()
    if receipt != (hashlib.sha256(raw).hexdigest() + '\n').encode('ascii'):
        raise ValueError('stored report digest mismatch')
    body = json.loads(raw.decode('utf-8'))
    label, seed, status = _seed(mode, constant)
    required = {'schema': SCHEMA, 'game': 'powerball', 'run_type': mode.run_type,
                'constant': constant, 'run_id': run_id, 'digits': mode.digits,
                'source_sha256': meta['packed_sha256'],
                'history_sha256': meta['history_sha256'],
                'event_sha256': meta['event_sha256'],
                'run_manifest_sha256': hashlib.sha256(raw_manifest).hexdigest(),
                'primary_family': 'K6S', 'primary_owner_vetoable': False,
                'primary_statistic': PRIMARY_STATISTIC,
                'secondary_statistic': SECONDARY_STATISTIC,
                'secondary_exploratory': True,
                'legacy_exposure_disclosure': D5_LEGACY_EXPOSURE_DISCLOSURE,
                'permutations_predeclared': PERMUTATIONS,
                'seed_label': label, 'seed': seed, 'seed_status': status}
    if not isinstance(body, dict) or any(body.get(k) != v for k, v in required.items()):
        raise ValueError('report source/mode/primary provenance mismatch')
    perm = body.get('permutation')
    if (not isinstance(perm, dict) or perm.get('iterations_requested') != PERMUTATIONS
            or perm.get('seed') != seed
            or not isinstance(perm.get('geometric_primary'), dict)
            or perm['geometric_primary'].get('statistic') != PRIMARY_STATISTIC
            or not isinstance(perm.get('median_secondary'), dict)
            or perm['median_secondary'].get('statistic') != SECONDARY_STATISTIC
            or perm['median_secondary'].get('centered_two_sided_p') != perm.get('centered_two_sided_p')
            or perm['median_secondary'].get('observed') != perm.get('observed_median')):
        raise ValueError('report permutation/primary/secondary provenance mismatch')
    return {'report': body,
            'code_matches_current': body.get('code_sha256_recorded_not_a_gate') == _code_hashes()}


def _close(a,b):
    # Exact integer comparisons; tolerance ONLY for floating-point results.
    if type(a) is int or type(b) is int:
        return type(a) is type(b) and a == b
    if isinstance(a,float) and isinstance(b,float):
        return math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-12)
    if isinstance(a,dict) and isinstance(b,dict):
        return set(a)==set(b) and all(_close(a[k],b[k]) for k in a)
    if isinstance(a,(list,tuple)) and isinstance(b,(list,tuple)):
        return len(a)==len(b) and all(_close(x,y) for x,y in zip(a,b))
    return a==b


def audit_report(mode: M.PowerballMode, constant: str, run_id: str):
    saved = load_report(mode,constant,run_id)['report']
    fresh = compute_report(mode,constant,run_id)
    fresh['code_sha256_recorded_not_a_gate'] = saved.get('code_sha256_recorded_not_a_gate')
    return {'science_matches': _close(saved,fresh),
            'code_matches_current': saved.get('code_sha256_recorded_not_a_gate') == _code_hashes()}


# Thin synthetic compatibility functions, NO separate scientific stack.
def compute_test_report(roots,profile,constant,run_id):
    return compute_report(P._mode_from_run(roots,profile,run_id),constant,run_id)

def create_test_report(roots,profile,constant,run_id):
    return create_report(P._mode_from_run(roots,profile,run_id),constant,run_id)

def load_test_report(roots,profile,constant,run_id):
    return load_report(P._mode_from_run(roots,profile,run_id),constant,run_id)

def audit_test_report(roots,profile,constant,run_id):
    return audit_report(P._mode_from_run(roots,profile,run_id),constant,run_id)


if __name__ == '__main__':
    raise SystemExit('No reporter CLI; only the single Q4i production entry point')
