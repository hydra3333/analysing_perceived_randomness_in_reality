#!/usr/bin/env python3
"""Q4e verified reporting/replay integration, SYNTHETIC-ONLY.

Uses previously qualified Q4c TEST runs; computes only from run manifests,
receipt, saved isolated TEST history/decoy bytes and verified raw event CSV.
NO published packed file read, production reporting, Q5 or parent integration.
Every output uses fixed type-isolated synthetic-only roots and create-only paths.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1 as P
import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S

SCHEMA = 'OUTLANDISH_Q4E_SYNTHETIC_REPORT_V1'
REPORT_ID = re.compile(r'TEST_(?:REAL|NULL)_[A-Za-z0-9_-]{1,48}\Z')
CODE_FILES = (
    'OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py',
    'OUTLANDISH_01_Q3_Event_Interface_Smoke_v0_1.py',
    'OUTLANDISH_01_Q3_Event_Classifier_v0_1.py',
    'OUTLANDISH_01_Q4_Published_Source_Guards_v0_1.py',
    'OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1.py',
    'OUTLANDISH_01_Q4d_Statistical_Core_v0_1.py',
    'OUTLANDISH_01_Q4e_Synthetic_Report_Bundle_v0_1.py',
)


def _hash(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _read(path: Path) -> bytes:
    G._no_links(path.absolute())
    if not path.is_file():
        raise ValueError('ordinary existing provenance file required')
    return path.read_bytes()


def _json(raw: bytes) -> dict:
    try:
        obj = json.loads(raw.decode('utf-8'))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError('invalid strict JSON report/manifest') from exc
    if not isinstance(obj, dict):
        raise ValueError('JSON report/manifest must be an object')
    return obj


def _encoded(obj: dict) -> bytes:
    return (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def _create(path: Path, raw: bytes) -> None:
    G._no_links(path.absolute())
    with path.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def _codes() -> dict[str, str]:
    root = Path(__file__).absolute().parent
    # These are snapshots of the actual on-disk implementation modules, not
    # an owner-maintained allowlist or a substitute for tests/source receipts.
    return {filename: _hash(_read(root / filename)) for filename in CODE_FILES}


def _check(roots: G.FixedRoots, game: str, constant: str, kind: str, run_id: str):
    P._check_test_root(roots)
    if game not in ('powerball', 'oz') or constant not in G.CONSTANT_STEMS:
        raise ValueError('unknown test game/constant')
    if kind not in ('TEST_REAL', 'TEST_NULL') or not isinstance(run_id, str) \
            or REPORT_ID.fullmatch(run_id) is None or not run_id.startswith(kind + '_'):
        raise ValueError('wrong synthetic run identity/type')
    run = G._inside(roots.base, roots.run_location(kind, run_id))
    if not run.is_dir():
        raise ValueError('existing Q4c TEST source run required')
    return run


def _report_folder(roots: G.FixedRoots, kind: str, run_id: str, *, new: bool) -> Path:
    parent = G._inside(roots.base, roots.base / (
        'reports_test_real' if kind == 'TEST_REAL' else 'reports_test_null'))
    if new:
        parent.mkdir(exist_ok=True)
    if not parent.is_dir():
        raise ValueError('missing report root')
    folder = G._inside(roots.base, parent / ('REPORT_' + run_id))
    if new and (folder.exists() or folder.is_symlink()):
        raise FileExistsError('reports are create-only; old results never overwritten')
    return folder


def _classified(game: str, numbered, events, n: int):
    from OUTLANDISH_01_Q3_Event_Classifier_v0_1 import (
        classify_events, PBRecord, OzRecord, RawEvent)
    if game == 'powerball':
        draws = tuple(PBRecord(i, values[:7], values[7]) for i, values in numbered)
    else:
        draws = tuple(OzRecord(i, values[:7], values[7:]) for i, values in numbered)
    cast = tuple(RawEvent(e.draw_number, e.family, e.start_digit_offset, e.matched_digits)
                 for e in events)
    return cast, classify_events(game, cast, draws, effective_digits=n)


def analyse_verified_synthetic_run(roots: G.FixedRoots, game: str, constant: str,
                                   kind: str, run_id: str, *, seed: int = 271828,
                                   iterations: int = 64) -> dict:
    """Recalculate pure science summaries; no direct packed-file access.

    Caller specifies only a marked sandbox and an existing Q4c TEST run.
    TEST_NULL produces K summary counts without joining raw NULL rows to REAL.
    """
    source = _check(roots, game, constant, kind, run_id)
    if type(seed) is not int or not 0 <= seed < 2**64 or \
            type(iterations) is not int or not 1 <= iterations <= 10_000:
        raise ValueError('bounded TEST permutation seed/iteration required')
    # This enforces COMPLETE, receipt/drawset/decoy hashes, event identity/order,
    # counts, EOF, classification and run type. It NEVER opens the BCD input.
    events = P.load_verified_synthetic_run(roots, game, constant, kind, run_id)
    original = _read(G._inside(roots.base, source / 'run_manifest.json'))
    meta = _json(original)
    if (meta.get('status') != 'COMPLETE' or meta.get('game') != game
            or meta.get('constant') != constant or meta.get('run_type') != kind):
        raise ValueError('invalid upstream COMPLETE manifest identity')
    n = meta.get('effective_digits')
    if type(n) is not int or n < 32:
        raise ValueError('invalid event prefix')
    # Recheck the exact bytes after Q4c verification, guarding against source
    # changes between replay and report construction (still no BCD re-open).
    event_sha = _hash(_read(G._inside(roots.base, source / 'raw_events.csv')))
    receipt_sha = _hash(_read(G._inside(roots.base, roots.receipt(constant))))
    if event_sha != meta.get('event_sha256') or receipt_sha != meta.get('receipt_sha256'):
        raise ValueError('source event/receipt changed during report validation')
    provenance = {'source_manifest_sha256': _hash(original),
                  'raw_events_sha256': event_sha,
                  'source_receipt_sha256': receipt_sha,
                  'verified_input_sha256': meta['input_sha256_actual']}
    answer = {'schema': SCHEMA, 'execution_scope': 'SYNTHETIC_TEST_REPORT_ONLY',
              'game': game, 'constant': constant, 'run_type': kind,
              'source_run_id': run_id, 'effective_digits': n,
              'provenance': provenance, 'counts_are_draw_attributed': True}
    if kind == 'TEST_REAL':
        profile = P._historical_profile(roots, game)
        history = G.validate_drawset(profile, expected_sha256=meta['drawset_sha256'])
        numbered = history.draw_rows
        draws = tuple(i for i, _ in numbered)
        cast, classified = _classified(game, numbered, events, n)
        categories = S.category_summary(game, classified, draws, n)
        rows, transition_meta, whole_sets = S.transitions(game, cast, draws, n)
        answer.update(
            history_sha256=history.sha256,
            category_summary=categories,
            physical_same_draw_overlaps=S.physical_overlaps(game, cast, draws, n),
            transitions=rows,
            transitions_summary=transition_meta,
            primary_is_proposed_owner_vetoable=True,
            permutation=S.permutation_test(whole_sets, seed=seed, iterations=iterations),
        )
    else:
        # No raw NULL rows are emitted to this report. Each decoy history has
        # its own 3 positions; reported counts are grouped by independent decoy.
        raw = _read(G._inside(roots.base, source / 'decoy_histories.csv'))
        if _hash(raw) != meta['decoy_sha256']:
            raise ValueError('decoy source changed')
        decoys = P._read_decoys(raw, game=game, k=meta['k'])
        views = tuple(rule[0] for rule in S.VIEW_RULES[game])
        groups = []
        for k in range(meta['k']):
            numbered = tuple((ordinal, vals) for ordinal, _, vals in decoys[k*3:(k+1)*3])
            allowed = {ordinal for ordinal, _ in numbered}
            part = tuple(e for e in events if e.draw_number in allowed)
            _, classified = _classified(game, numbered, part, n)
            rows = S.category_summary(game, classified,
                                      (ordinal for ordinal, _ in numbered), n)
            counts = {row['view']: row['events'] for row in rows}
            if set(counts) != set(views):
                raise ValueError('decoy category roster mismatch')
            groups.append(dict(decoy=f'DECOY-{k+1:04d}', counts=counts))
        answer.update(k=meta['k'], decoy_histories_sha256=_hash(raw),
                      decoy_generator=meta['generator'],
                      decoy_seed=meta['seed'], per_decoy_summary_counts=groups)
    return answer


def compare_verified_summary_counts(real: dict, null: dict) -> dict:
    """Compare aggregate class counts ONLY; do not read or join raw NULL rows."""
    if not isinstance(real, dict) or not isinstance(null, dict) or \
            real.get('schema') != SCHEMA or null.get('schema') != SCHEMA or \
            real.get('run_type') != 'TEST_REAL' or null.get('run_type') != 'TEST_NULL' or \
            real.get('game') != null.get('game') or \
            real.get('constant') != null.get('constant'):
        raise ValueError('wrong REAL/NULL summary identities')
    actual = {row['view']: row['events'] for row in real['category_summary']}
    groups = null['per_decoy_summary_counts']
    if type(null.get('k')) is not int or len(groups) != null['k']:
        raise ValueError('invalid NULL summary roster')
    return {name: S.decoy_count_tails(count, [part['counts'][name] for part in groups])
            for name, count in actual.items()}


def create_synthetic_report(roots: G.FixedRoots, game: str, constant: str,
                            kind: str, run_id: str, *, seed: int = 271828,
                            iterations: int = 64,
                            inject_failure_before_complete: bool = False) -> Path:
    """Create-once report folder; incomplete records are never accepted."""
    _check(roots, game, constant, kind, run_id)
    dest = _report_folder(roots, kind, run_id, new=True)
    report = analyse_verified_synthetic_run(roots, game, constant, kind, run_id,
                                            seed=seed, iterations=iterations)
    hashes = _codes()
    dest.mkdir(exist_ok=False)
    manifest = dest / 'report_manifest.json'
    basic = {'schema': SCHEMA, 'scope': 'SYNTHETIC_Q4E_NOT_Q5',
             'status': 'INCOMPLETE', 'game': game, 'constant': constant,
             'run_type': kind, 'source_run_id': run_id,
             'report_name': 'report.json', 'source_provenance': report['provenance'],
             'implementation_sha256': hashes,
             'permutation_seed': seed, 'permutation_iterations': iterations}
    _create(manifest, _encoded(basic))
    raw = _encoded(report)
    _create(dest / 'report.json', raw)
    if inject_failure_before_complete:
        raise RuntimeError('injected Q4e failure; leaves INCOMPLETE report')
    # Independently revalidate source and stored bytes while status is incomplete.
    if _read(dest / 'report.json') != _encoded(analyse_verified_synthetic_run(
            roots, game, constant, kind, run_id, seed=seed, iterations=iterations)):
        raise ValueError('report changed during publication')
    done = {**basic, 'status': 'COMPLETE', 'report_sha256': _hash(raw)}
    pending = dest / 'report_manifest.next.json'
    _create(pending, _encoded(done))
    os.replace(pending, manifest)  # only inside the new synthetic-only folder
    return dest


def load_verified_synthetic_report(roots: G.FixedRoots, game: str, constant: str,
                                   kind: str, run_id: str) -> dict:
    """Read-only, recompute-on-replay report verification; never open BCD."""
    _check(roots, game, constant, kind, run_id)
    dest = _report_folder(roots, kind, run_id, new=False)
    if not dest.is_dir():
        raise ValueError('report folder missing')
    manifest = _json(_read(G._inside(roots.base, dest / 'report_manifest.json')))
    expected = {'schema': SCHEMA, 'scope': 'SYNTHETIC_Q4E_NOT_Q5',
                'status': 'COMPLETE', 'game': game, 'constant': constant,
                'run_type': kind, 'source_run_id': run_id,
                'report_name': 'report.json'}
    if any(manifest.get(field) != value for field, value in expected.items()):
        raise ValueError('unqualified report status/type/identity')
    if manifest.get('implementation_sha256') != _codes():
        raise ValueError('executing implementation differs from report provenance')
    seed, iterations = manifest.get('permutation_seed'), manifest.get('permutation_iterations')
    report = analyse_verified_synthetic_run(roots, game, constant, kind, run_id,
                                            seed=seed, iterations=iterations)
    if report['provenance'] != manifest.get('source_provenance'):
        raise ValueError('source run changed after report completion')
    raw = _read(G._inside(roots.base, dest / 'report.json'))
    if _hash(raw) != manifest.get('report_sha256') or raw != _encoded(report):
        raise ValueError('report SHA/content disagrees with verified replay')
    return report


def compare_verified_test_run_summaries(roots: G.FixedRoots, game: str,
                                        constant: str, real_run_id: str,
                                        null_run_id: str) -> dict:
    """Only compare report summaries AFTER both typed inputs pass verified replay.

    This is deliberately synthetic-only; no PUBLIC/REAL report comparison API.
    """
    real = load_verified_synthetic_report(roots, game, constant,
                                          'TEST_REAL', real_run_id)
    null = load_verified_synthetic_report(roots, game, constant,
                                          'TEST_NULL', null_run_id)
    return compare_verified_summary_counts(real, null)


if __name__ == '__main__':
    raise SystemExit('NO production report CLI. Use synthetic-only qualification harness.')
