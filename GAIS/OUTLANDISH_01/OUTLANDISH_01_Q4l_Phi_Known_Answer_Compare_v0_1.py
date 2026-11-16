#!/usr/bin/env python3
"""Q4l: after a separately authorised COMPLETE REAL phi scan, compare P3 event sets only.

NO scan, no history input, no gaps or statistical summaries, no production writes.
D5 permits only exact (draw, start offset, matched digits) identity checks.
Use --self-test before Q5; do NOT use --run-id until a qualified phi REAL scan exists.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile

import OUTLANDISH_01_Q1_Reconcile_Saved_Phi_Events as Q1
import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G

LEGACY_RELATIVE = Path('results') / 'packed_run_20261108T012705Z_43564c3c' / 'matches.csv'
LEGACY_SHA256 = '7a4315d66b028a2664413f0b3017714c10653110a1d79af7102d8ea09bbb5c83'
PHI_PACKED_SHA256 = 'dd80be0c3fdb330fe4e1780c2d53bf03bde297a5dea83b5785cd3349838ad36d'
HISTORY_SHA256 = 'c71039c63f64479b2d83c10e8df3ad5e7525091b3a7f44c5a2680015f4fd2e54'
LEGACY_P3_COUNT = 227


def _p3_triples(evidence: Q1.Evidence) -> set[tuple[int, int, str]]:
    if 'P3' not in evidence.available:
        raise ValueError('P3 evidence missing')
    return {(e.draw, e.offset, e.digits) for e in evidence.events if e.category == 'P3'}


def _compare(legacy: Q1.Evidence, current: Q1.Evidence) -> dict:
    old, new = _p3_triples(legacy), _p3_triples(current)
    missing, extra = sorted(old - new), sorted(new - old)
    fields = lambda rows: [dict(draw=d, start_offset=o, matched_digits=s)
                           for d, o, s in rows]
    return {'matched': len(old & new), 'missing': len(missing), 'extra': len(extra),
            'missing_rows': fields(missing), 'extra_rows': fields(extra)}


def _require_complete_phi_manifest(meta: object, run_id: str):
    expected = {
        'schema': 'OUTLANDISH_Q4H_POWERBALL_RUN_V2',
        'status': 'COMPLETE', 'run_type': 'REAL', 'game': 'powerball',
        'constant': 'phi', 'run_id': run_id, 'event_file': 'raw_events.csv',
        'digits': G.DIGITS_PRODUCTION, 'bytes_hashed': G.BYTES_PRODUCTION,
        'packed_sha256': PHI_PACKED_SHA256, 'history_sha256': HISTORY_SHA256,
    }
    if not isinstance(meta, dict) or any(meta.get(k) != v for k, v in expected.items()):
        raise ValueError('not the qualified COMPLETE Powerball phi run')
    digest = meta.get('event_sha256')
    if not isinstance(digest, str) or not G.SHA256.fullmatch(digest):
        raise ValueError('missing or malformed event SHA-256')


def _compare_real(run_id: str) -> dict:
    # Fixed G: production paths; no caller-specified source or root substitutions.
    roots = G.FixedRoots.production()
    folder = roots.run_location('REAL', run_id)
    manifest = G._inside(roots.base, folder / 'run_manifest.json')
    meta = json.loads(manifest.read_bytes().decode('utf-8'))
    _require_complete_phi_manifest(meta, run_id)

    old_csv = G._inside(roots.base, roots.base / LEGACY_RELATIVE)
    if G._sha(old_csv) != LEGACY_SHA256:
        raise ValueError('saved 227-row phi evidence digest differs from pinned record')
    old = Q1.parse_evidence(old_csv)
    if len(_p3_triples(old)) != LEGACY_P3_COUNT:
        raise ValueError('saved phi P3 row count is not 227')

    new_csv = G._inside(roots.base, folder / 'raw_events.csv')
    if G._sha(new_csv) != meta['event_sha256']:
        raise ValueError('qualified phi event CSV digest differs from COMPLETE manifest')
    new = Q1.parse_evidence(new_csv)
    if new.rows != meta.get('event_count'):
        raise ValueError('raw event CSV count differs from COMPLETE manifest')
    return _compare(old, new)


def _self_test():
    # Only synthetic, temporary CSVs. No G:, no historical draws, no production paths.
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q4L_SYNTHETIC_') as temp:
        a, b = Path(temp) / 'legacy.csv', Path(temp) / 'new.csv'
        a.write_text(
            'draw_number,category,start_digit_offset_0_based,matched_decimal_digits\n'
            '100,3,10,01234567890123\n'
            '101,3,20,12345678901234\n', encoding='utf-8')
        b.write_text(
            'draw_number,family,start_digit_offset,matched_digits\n'
            '100,K6S,10,01234567890123\n'
            '102,K6S,30,23456789012345\n'
            '100,K7,15,01234567890123\n', encoding='utf-8')
        output = _compare(Q1.parse_evidence(a), Q1.parse_evidence(b))
        assert output['matched'] == 1 and output['missing'] == 1 and output['extra'] == 1
        assert output['missing_rows'] == [{'draw': 101, 'start_offset': 20,
                                           'matched_digits': '12345678901234'}]
        assert output['extra_rows'] == [{'draw': 102, 'start_offset': 30,
                                         'matched_digits': '23456789012345'}]
        b.write_text('draw_number,family,start_digit_offset,matched_digits\n'
                     '100,K6S,10,01234567890123\n'
                     '101,K6S,20,12345678901234\n', encoding='utf-8')
        exact = _compare(Q1.parse_evidence(a), Q1.parse_evidence(b))
        assert exact == {'matched': 2, 'missing': 0, 'extra': 0,
                         'missing_rows': [], 'extra_rows': []}
        try:
            _require_complete_phi_manifest({'status': 'INCOMPLETE'}, 'REAL_phi_example')
        except ValueError:
            pass
        else:
            raise AssertionError('incomplete run accepted')
    print('Q4L SYNTHETIC PHI SET-COMPARISON PASS: exact/missing/extra/guard; production-reads=0')


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    group = cli.add_mutually_exclusive_group(required=True)
    group.add_argument('--self-test', action='store_true')
    group.add_argument('--run-id', help='a previously completed qualified REAL phi run identifier')
    args = cli.parse_args()
    if args.self_test:
        _self_test()
        return 0
    try:
        result = _compare_real(args.run_id)
    except (OSError, ValueError, Q1.BadEvidence, UnicodeError, json.JSONDecodeError) as exc:
        print('Q4L PHI KNOWN-ANSWER REFUSAL:', str(exc))
        return 2
    print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))
    print('Q4L PHI KNOWN-ANSWER:', 'PASS' if not result['missing'] and not result['extra'] else 'FAIL')
    return 0 if not result['missing'] and not result['extra'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
