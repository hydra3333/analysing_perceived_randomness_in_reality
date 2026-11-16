#!/usr/bin/env python3
"""Q4h shared Powerball/Oz runner, taking the Q4i immutable game mode.

Both per-game scan switches default OFF. Direct production calls are guarded
separately by game. Existing Powerball TEST wrappers remain compatible.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4h_Events_v0_1 as E
import OUTLANDISH_01_Q4i_Mode_v0_1 as M

SCHEMA = 'OUTLANDISH_Q4H_POWERBALL_RUN_V2'
OZ_SCHEMA = 'OUTLANDISH_Q4H_OZ_RUN_V1'


def _schema(game):
    return SCHEMA if game == 'powerball' else OZ_SCHEMA if game == 'oz' else None


def _guard_run_game(mode, run_id):
    # Oz runs must be game-labelled; Powerball's historical IDs remain valid.
    prefix = mode.run_type + '_oz_'
    if (mode.game == 'oz' and not run_id.startswith(prefix)) or (
            mode.game == 'powerball' and run_id.startswith(prefix)):
        raise ValueError('run ID/game identity mismatch')



def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def put_new(path, data):
    G._no_links(Path(path).absolute())
    with Path(path).open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def _test(roots, profile):
    # Backward-compatible validation for the pre-Review-B qualification harness.
    M.PowerballMode.synthetic(roots, profile, 32)


def _mode_from_run(roots, profile, run_id):
    """TEST wrapper only: read untrusted N, then let strict loader validate it."""
    folder = roots.run_location('TEST_REAL', run_id)
    raw = G._inside(roots.base, folder / 'run_manifest.json').read_bytes()
    obj = json.loads(raw.decode('utf-8'))
    if not isinstance(obj, dict):
        raise ValueError('bad TEST manifest')
    return M.PowerballMode.synthetic(roots, profile, obj.get('digits'),
                                     game=profile.game)


def _receipt_only(mode, constant, meta):
    roots = mode.roots
    receipt = G._inside(roots.base, roots.receipt(constant))
    raw = receipt.read_bytes()
    if hashlib.sha256(raw).hexdigest() != meta.get('receipt_sha256'):
        raise ValueError('converter receipt changed')
    obj = json.loads(raw.decode('utf-8'))
    if (not isinstance(obj, dict) or obj.get('constant') != constant
            or obj.get('format') != G.FORMAT or obj.get('scope') != G.SCOPE
            or obj.get('binary_name') != roots.published_binary(constant).name
            or obj.get('binary_sha256_streamed') != meta.get('packed_sha256')
            or obj.get('digits_including_integer') != mode.digits
            or obj.get('packed_bytes') != meta.get('bytes_hashed')):
        raise ValueError('converter receipt/run mismatch')


def load_run(mode: M.PowerballMode, constant: str, run_id: str):
    """Read COMPLETE manifest and event CSV; never reopen packed BCD."""
    mode = mode.checked()
    roots = mode.roots
    _guard_run_game(mode, run_id)
    folder = roots.run_location(mode.run_type, run_id)
    raw_meta = G._inside(roots.base, folder / 'run_manifest.json').read_bytes()
    meta = json.loads(raw_meta.decode('utf-8'))
    required = {'schema': _schema(mode.game), 'status': 'COMPLETE', 'run_type': mode.run_type,
                'game': mode.game, 'constant': constant, 'run_id': run_id,
                'event_file': 'raw_events.csv',
                'packed_file': roots.published_binary(constant).name,
                'scanner': 'OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py',
                'digits': mode.digits}
    if not isinstance(meta, dict) or any(meta.get(k) != v for k,v in required.items()):
        raise ValueError('invalid COMPLETE Powerball run identity')
    if (type(meta.get('bytes_hashed')) is not int
            or meta['bytes_hashed'] != (mode.digits + 1)//2
            or not isinstance(meta.get('packed_sha256'), str)
            or G.SHA256.fullmatch(meta['packed_sha256']) is None):
        raise ValueError('invalid scan source digest and coverage')
    _receipt_only(mode, constant, meta)
    history = G.validate_drawset(mode.profile, expected_sha256=meta.get('history_sha256'))
    events, classified = E.read_and_classify(
        G._inside(roots.base, folder / 'raw_events.csv').read_bytes(),
        recorded_sha256=meta.get('event_sha256'), history=history, digits=mode.digits,
        game=mode.game)
    counts = {f: sum(e.family == f for e in events)
              for f in sorted(set(e.family for e in events))}
    if len(events) != meta.get('event_count') or counts != meta.get('family_counts'):
        raise ValueError('event totals disagree with run manifest')
    return meta, raw_meta, history, events, classified


def _require_scan_permission(mode):
    mode.checked()
    if not mode.roots.synthetic:
        # Independent per-game gates at the actual scan boundary, not just CLI.
        from OUTLANDISH_01_Q4i_Production_Entry_v0_1 import (
            ENABLE_Q5_PRODUCTION_SCANS, ENABLE_OZ_PRODUCTION_SCANS)
        enabled = (ENABLE_Q5_PRODUCTION_SCANS if mode.game == 'powerball'
                   else ENABLE_OZ_PRODUCTION_SCANS if mode.game == 'oz' else False)
        if enabled is not True:
            raise PermissionError(f'{mode.game} production scanning disabled; '
                                  'separate owner git authorisation required')


def run_powerball(mode: M.PowerballMode, constant: str, run_id: str, *,
                  chunk_bytes=None, inject_failure=False):
    """One shared game runner; independent gates before ANY production I/O."""
    _require_scan_permission(mode)  # Before production source/history/output access.
    _guard_run_game(mode, run_id)
    roots = mode.roots
    source = G.validate_published_source(roots, constant,
                                          fixture_digits=mode.digits if roots.synthetic else None)
    history = G.validate_drawset(mode.profile)
    location = roots.validate_run_location(mode.run_type, run_id,
                                            roots.run_location(mode.run_type, run_id))
    from OUTLANDISH_01_Q3_Packed_Matcher_v0_4 import (
        PBRecord, OzRecord, scan_packed_stream, scan_packed_oz_stream)
    # Scanner v0.4 owns record classes; classification has its own v0.2 types.
    if mode.game == 'powerball':
        draws = tuple(PBRecord(i, vals[:7], vals[7]) for i, vals in history.draw_rows)
    else:
        draws = tuple(OzRecord(i, vals[:7], vals[7:]) for i, vals in history.draw_rows)
    scanner = scan_packed_stream if mode.game == 'powerball' else scan_packed_oz_stream
    location.mkdir(exist_ok=False)
    base = {'schema': _schema(mode.game), 'run_type': mode.run_type, 'status': 'INCOMPLETE',
            'game': mode.game, 'constant': constant, 'run_id': run_id,
            'event_file': 'raw_events.csv', 'packed_file': source.path.name,
            'scanner': 'OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py',
            'digits': mode.digits, 'history_sha256': history.sha256,
            'receipt_sha256': source.receipt_sha256,
            'packed_sha256': source.packed_sha256,
            'started_utc': datetime.now(timezone.utc).isoformat(timespec='seconds')}
    put_new(location / 'run_manifest.json', encode(base))
    scan = scanner(source.path, physical_digits=mode.digits,
                              effective_digits=mode.digits, draws=draws,
                              output_csv=location / 'raw_events.csv',
                              expected_full_sha256=source.packed_sha256,
                              chunk_bytes=chunk_bytes)
    source.check_completed_stream(scan.sha256_full_packed, scan.bytes_hashed)
    raw = G._inside(roots.base, location / 'raw_events.csv').read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != scan.event_sha256 or scan.event_count < 0:
        raise ValueError('scanner CSV digest/count invalid')
    events, _ = E.read_and_classify(raw, recorded_sha256=digest, history=history,
                                    digits=mode.digits, game=mode.game)
    counted = {f: sum(e.family == f for e in events)
               for f in sorted(set(e.family for e in events))}
    if (len(events) != scan.event_count or counted != scan.family_counts
            or scan.event_csv != location / 'raw_events.csv'):
        raise ValueError('scanner event identity/totals mismatch')
    if G._sha(source.receipt_path) != source.receipt_sha256:
        raise ValueError('converter receipt changed during scan')
    G.validate_drawset(mode.profile, expected_sha256=history.sha256)
    if inject_failure:
        raise RuntimeError('injected post-scan pre-COMPLETE failure')
    complete = {**base, 'status': 'COMPLETE', 'event_sha256': digest,
                'event_count': scan.event_count, 'family_counts': scan.family_counts,
                'bytes_hashed': scan.bytes_hashed, 'chunk_bytes': scan.chunk_bytes,
                'finished_utc': datetime.now(timezone.utc).isoformat(timespec='seconds')}
    put_new(location / 'run_manifest.next.json', encode(complete))
    os.replace(location / 'run_manifest.next.json', location / 'run_manifest.json')
    return location


# Thin compatibility wrappers keep Q4h historical tests, not a separate REAL stack.
def load_test_run(roots, profile, constant, run_id):
    return load_run(_mode_from_run(roots, profile, run_id), constant, run_id)


def run_test_powerball(roots, profile, constant, run_id, *, digits, chunk_bytes=None,
                       inject_failure=False):
    return run_powerball(M.PowerballMode.synthetic(roots, profile, digits), constant,
                         run_id, chunk_bytes=chunk_bytes, inject_failure=inject_failure)


if __name__ == '__main__':
    raise SystemExit('No direct runner CLI: Q5 switch is controlled in single entry point')
