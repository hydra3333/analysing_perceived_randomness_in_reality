#!/usr/bin/env python3
"""Powerball Q4h: minimal production-shaped runner, SYNTHETIC TEST ONLY.

Deliberately NO REAL execution API/CLI, no published G: file reads and no Q5.
Receipts/historical profiles come from Q4b; streaming engine from Q3 v0.4.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4h_Events_v0_1 as E

SCHEMA = 'OUTLANDISH_Q4H_POWERBALL_TEST_RUN_V1'


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def put_new(path, data):
    G._no_links(Path(path).absolute())
    with Path(path).open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def _test(roots, profile):
    if not isinstance(roots, G.FixedRoots) or not roots.synthetic:
        raise ValueError('Q4h cannot use a production root; no REAL entry point')
    G.FixedRoots.test_sandbox(roots.base)
    if os.name == 'nt' and roots.base.is_relative_to(
            Path(r'G:\OUTLANDISH_01\large_artifacts').absolute()):
        raise ValueError('synthetic sandbox nested in production artifacts')
    if (not isinstance(profile, G.HistoryProfile) or not profile.synthetic
            or profile.game != 'powerball' or profile.header != G.PB_HEADER
            or Path(profile.source).absolute() !=
               (roots.base / 'histories' / 'powerball_synthetic.csv').absolute()):
        raise ValueError('Q4h requires isolated synthetic Powerball history')
    for label in ('digits', 'histories', 'results'):
        if not (roots.base / label).is_dir():
            raise ValueError('missing marked fixture folder')


def _receipt_only(roots, constant, meta):
    # Replay never opens packed BCD, even if original source is absent.
    receipt = G._inside(roots.base, roots.receipt(constant))
    raw = receipt.read_bytes()
    if hashlib.sha256(raw).hexdigest() != meta.get('receipt_sha256'):
        raise ValueError('converter receipt changed')
    obj = json.loads(raw.decode('utf-8'))
    if (obj.get('constant') != constant or obj.get('format') != G.FORMAT
            or obj.get('scope') != G.SCOPE
            or obj.get('binary_name') != roots.published_binary(constant).name
            or obj.get('binary_sha256_streamed') != meta.get('packed_sha256')
            or obj.get('digits_including_integer') != meta.get('digits')
            or obj.get('packed_bytes') != meta.get('bytes_hashed')):
        raise ValueError('converter receipt/run mismatch')


def load_test_run(roots, profile, constant, run_id):
    """Digest/identity replay of COMPLETE synthetic run, without BCD reread."""
    _test(roots, profile)
    folder = roots.run_location('TEST_REAL', run_id)
    raw_meta = (G._inside(roots.base, folder / 'run_manifest.json')).read_bytes()
    meta = json.loads(raw_meta.decode('utf-8'))
    required = {'schema': SCHEMA, 'status': 'COMPLETE', 'run_type': 'TEST_REAL',
                'game': 'powerball', 'constant': constant, 'run_id': run_id,
                'event_file': 'raw_events.csv',
                'packed_file': roots.published_binary(constant).name,
                'scanner': 'OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py'}
    if not isinstance(meta, dict) or any(meta.get(k) != v for k, v in required.items()):
        raise ValueError('invalid COMPLETE Powerball run identity')
    n = meta.get('digits')
    if type(n) is not int or n < 32 or meta.get('bytes_hashed') != (n+1)//2:
        raise ValueError('run source length/hash coverage invalid')
    if not G.SHA256.fullmatch(meta.get('packed_sha256', '')):
        raise ValueError('missing scan source digest')
    _receipt_only(roots, constant, meta)
    hist = G.validate_drawset(profile, expected_sha256=meta.get('history_sha256'))
    events, classified = E.read_and_classify(
        (G._inside(roots.base, folder / 'raw_events.csv')).read_bytes(),
        recorded_sha256=meta.get('event_sha256'), history=hist, digits=n)
    if len(events) != meta.get('event_count') or {
        fam: sum(e.family == fam for e in events) for fam in sorted(set(e.family for e in events))
    } != meta.get('family_counts'):
        raise ValueError('event totals differ from manifest')
    return meta, raw_meta, hist, events, classified


def run_test_powerball(roots, profile, constant, run_id, *, digits, chunk_bytes=None,
                       inject_failure=False):
    """Run a tiny isolated synthetic fixture; never accept REAL input paths."""
    _test(roots, profile)
    source = G.validate_published_source(roots, constant, fixture_digits=digits)
    history = G.validate_drawset(profile)
    location = roots.validate_run_location('TEST_REAL', run_id,
                                           roots.run_location('TEST_REAL', run_id))
    from OUTLANDISH_01_Q3_Packed_Matcher_v0_4 import PBRecord, scan_packed_stream
    draws = tuple(PBRecord(i, vals[:7], vals[7]) for i, vals in history.draw_rows)
    location.mkdir(exist_ok=False)
    base = {'schema': SCHEMA, 'run_type': 'TEST_REAL', 'status': 'INCOMPLETE',
            'game': 'powerball', 'constant': constant, 'run_id': run_id,
            'event_file': 'raw_events.csv', 'packed_file': source.path.name,
            'scanner': 'OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py',
            'digits': source.digits, 'history_sha256': history.sha256,
            'receipt_sha256': source.receipt_sha256,
            'packed_sha256': source.packed_sha256,
            'started_utc': datetime.now(timezone.utc).isoformat(timespec='seconds')}
    put_new(location / 'run_manifest.json', encode(base))
    scan = scan_packed_stream(source.path, physical_digits=source.digits,
                              effective_digits=source.digits, draws=draws,
                              output_csv=location / 'raw_events.csv',
                              expected_full_sha256=source.packed_sha256,
                              chunk_bytes=chunk_bytes)
    source.check_completed_stream(scan.sha256_full_packed, scan.bytes_hashed)
    raw = (location / 'raw_events.csv').read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != scan.event_sha256 or scan.event_count < 0:
        raise ValueError('scanner CSV digest/count invalid')
    events, _ = E.read_and_classify(raw, recorded_sha256=digest, history=history,
                                    digits=source.digits)
    counted = {f: sum(e.family == f for e in events)
               for f in sorted(set(e.family for e in events))}
    if (len(events) != scan.event_count or counted != scan.family_counts
            or scan.event_csv != location / 'raw_events.csv'):
        raise ValueError('scanner event identity/totals mismatch')
    # Final small-file provenance check immediately before COMPLETE. The 5 GB
    # input is NOT reopened: its read-once scan digest was already compared.
    if G._sha(source.receipt_path) != source.receipt_sha256:
        raise ValueError('converter receipt changed during scan')
    G.validate_drawset(profile, expected_sha256=history.sha256)
    if inject_failure:
        raise RuntimeError('injected failure after verified scan, before COMPLETE')
    finished = {**base, 'status': 'COMPLETE', 'event_sha256': digest,
                'event_count': scan.event_count, 'family_counts': scan.family_counts,
                'bytes_hashed': scan.bytes_hashed,
                'chunk_bytes': scan.chunk_bytes,
                'finished_utc': datetime.now(timezone.utc).isoformat(timespec='seconds')}
    put_new(location / 'run_manifest.next.json', encode(finished))
    os.replace(location / 'run_manifest.next.json', location / 'run_manifest.json')
    return location


if __name__ == '__main__':
    raise SystemExit('Q4h has no REAL production CLI; synthetic qualification only')
