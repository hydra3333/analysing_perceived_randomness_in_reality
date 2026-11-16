#!/usr/bin/env python3
"""OUTLANDISH Q4f: six-constant/two-game/two-type *synthetic* integration.

No production CLI, production-root discovery, historical REAL files, or Q5.
Every generated file is in a marked TemporaryDirectory under an independent
synthetic TEST root. Reuses the already installed Q4b/Q4c/Q4d/Q4e components.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import tempfile

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1 as P
import OUTLANDISH_01_Q4c_Synthetic_Processing_Qualification_v0_1 as F
import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S
import OUTLANDISH_01_Q4e_Synthetic_Report_Bundle_v0_1 as R

CONSTANTS = S.CONSTANTS
GAMES = ('powerball', 'oz')
KINDS = ('TEST_REAL', 'TEST_NULL')
N = 10_001


def refuses(label, action):
    try:
        action()
    except (ValueError, RuntimeError, FileExistsError, KeyError, TypeError):
        return 1
    raise AssertionError('UNEXPECTED ACCEPTANCE: ' + label)


def seed_six_sources(roots, n):
    """Synthetic-only distinct BCD sources with *correctly recalculated* receipts."""
    if not roots.synthetic or n != N:
        raise ValueError('six-source fixture has fixed synthetic identity')
    template = roots.published_binary('phi').read_bytes()
    assert len(template) == (n + 1) // 2
    digests = {}
    for i, constant in enumerate(CONSTANTS):
        path = roots.published_binary(constant)
        if constant != 'phi':
            block = bytearray(template)
            block[3500 + i] = 0x81  # after planted event positions, valid decimal BCD
            path.write_bytes(block)
        binary = path.read_bytes()
        digest = hashlib.sha256(binary).hexdigest()
        plan = G.sample_plan(len(binary))
        receipt = dict(format=G.FORMAT, format_version=1, scope=G.SCOPE,
                       constant=constant, binary_name=path.name,
                       digits_including_integer=n, packed_bytes=len(binary),
                       binary_sha256_streamed=digest,
                       sample_block_length=plan[0][1],
                       samples=[dict(offset_bytes=offset, size=length,
                                     sha256=hashlib.sha256(binary[offset:offset+length]).hexdigest())
                                for offset, length in plan])
        if constant != 'phi':
            roots.receipt(constant).write_text(json.dumps(receipt, sort_keys=True)+'\n',
                                               encoding='utf-8')
        checked = G.validate_published_source(roots, constant, fixture_digits=n)
        assert checked.packed_sha256 == digest
        digests[constant] = digest
    assert len(set(digests.values())) == 6, 'six fixture sources must be distinct'
    return digests


def test_boundaries(roots):
    n = 0
    # A fixed, owner-approved Oz REAL profile now exists; forged bounds still refuse.
    n += refuses('forged Oz REAL era', lambda: G.HistoryProfile(
        'oz', Path(G.__file__).absolute().parent/'OZLOTTO_preholdout_only.csv',
        1473,1694,G.OZ_HEADER))
    n += refuses('TEST runner cannot take REAL type', lambda: P.run_synthetic(
        roots, 'powerball', 'phi', 'REAL', 'REAL_forbidden', fixture_digits=N))
    n += refuses('TEST runner cannot take NULL type', lambda: P.run_synthetic(
        roots, 'oz', 'phi', 'NULL', 'NULL_forbidden', fixture_digits=N, seed=1))
    n += refuses('bad constant injection', lambda: G.validate_published_source(
        roots, 'fictional', fixture_digits=N))
    n += refuses('test cannot use unrestricted history path', lambda: G.HistoryProfile(
        'powerball', roots.base/'histories'/'powerball_synthetic.csv', 1144, 1577,
        G.PB_HEADER, False))
    n += refuses('REAL history not accepted as NULL', lambda: roots.output_parent('REAL'))
    n += refuses('NULL history not accepted as REAL', lambda: roots.output_parent('NULL'))
    assert n == 7
    return n


def run_matrix(roots, n):
    all_records = {}
    raw_p = defaultdict(dict)
    refusals = 0
    source_digests = seed_six_sources(roots, n)
    for game in GAMES:
        for i, constant in enumerate(CONSTANTS):
            for kind in KINDS:
                run_id = f'{kind}_q4f_{game}_{constant}'
                kwargs = dict(fixture_digits=n, chunk_bytes=9)
                if kind == 'TEST_NULL':
                    kwargs.update(seed=10_000 + i + (0 if game == 'powerball' else 100), k=2)
                run = P.run_synthetic(roots, game, constant, kind, run_id, **kwargs)
                before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in run.iterdir() if p.is_file()}
                manifest = json.loads((run/'run_manifest.json').read_text('utf-8'))
                assert manifest['status'] == 'COMPLETE'
                assert manifest['input_sha256_actual'] == source_digests[constant]
                assert manifest['bytes_hashed'] == (n+1)//2
                assert manifest['run_type'] == kind and manifest['game'] == game
                assert type(manifest['event_count']) is int and manifest['event_count'] >= 0
                assert run.parent == roots.output_parent(kind)
                if kind == 'TEST_NULL':
                    assert (run/'decoy_histories.csv').exists()
                    assert 'drawset_sha256' not in manifest
                else:
                    assert 'decoy_sha256' not in manifest
                    assert 'drawset_sha256' in manifest

                report_dir = R.create_synthetic_report(roots, game, constant,
                                                       kind, run_id, seed=31_415,
                                                       iterations=48)
                after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in run.iterdir() if p.is_file()}
                assert before == after, 'reporter unexpectedly modified source run'
                report = R.load_verified_synthetic_report(roots, game, constant,
                                                          kind, run_id)
                assert report['game'] == game and report['constant'] == constant
                assert report['run_type'] == kind
                assert json.loads((report_dir/'report_manifest.json').read_text())['status'] == 'COMPLETE'
                assert report_dir.parent not in (roots.output_parent('TEST_REAL'),
                                                 roots.output_parent('TEST_NULL'))
                all_records[game, constant, kind] = (run_id, run, report_dir, report)
                if kind == 'TEST_REAL':
                    value = report['permutation']['centered_two_sided_p']
                    raw_p[game][constant] = value
                    assert len(report['transitions']) == 2
                else:
                    assert len(report['per_decoy_summary_counts']) == 2
                    assert 'category_summary' not in report
                refusals += refuses('never overwrite an existing source run',
                                    lambda: P.run_synthetic(roots, game, constant,
                                        kind, run_id, **kwargs))
                refusals += refuses('never overwrite an existing report',
                                    lambda: R.create_synthetic_report(
                                        roots, game, constant, kind, run_id, iterations=48))

    assert len(all_records) == 24
    assert {g: set(raw_p[g]) for g in GAMES} == {g: set(CONSTANTS) for g in GAMES}
    holm = {g: S.holm_six_constants(raw_p[g]) for g in GAMES}
    for game in GAMES:
        assert set(holm[game]) == set(CONSTANTS)
        for constant in CONSTANTS:
            raw = raw_p[game][constant]
            adjusted = holm[game][constant]
            assert (raw is None and adjusted is None) or (
                raw is not None and adjusted is not None and raw <= adjusted <= 1.0)
            real_id, _, _, real = all_records[game, constant, 'TEST_REAL']
            null_id, _, _, null = all_records[game, constant, 'TEST_NULL']
            assert R.compare_verified_test_run_summaries(roots, game, constant,
                                                          real_id, null_id) == \
                R.compare_verified_summary_counts(real, null)
    # Run IDs are bound to one constant, one game and one type (not just a folder).
    for game in GAMES:
        for constant in CONSTANTS:
            real_id, _, _, _ = all_records[game, constant, 'TEST_REAL']
            other_game = 'oz' if game == 'powerball' else 'powerball'
            other_constant = 'phi' if constant != 'phi' else 'pi'
            refusals += refuses('cross-game verified report read',
                lambda: R.load_verified_synthetic_report(
                    roots, other_game, constant, 'TEST_REAL', real_id))
            refusals += refuses('cross-constant verified report read',
                lambda: R.load_verified_synthetic_report(
                    roots, game, other_constant, 'TEST_REAL', real_id))
            refusals += refuses('cross-type verified report read',
                lambda: R.load_verified_synthetic_report(
                    roots, game, constant, 'TEST_NULL', real_id))

    # Read-only replay genuinely must not touch any packed source.
    renamed = []
    try:
        for constant in CONSTANTS:
            path = roots.published_binary(constant)
            other = path.with_name(path.name + '.temporarily_absent')
            path.rename(other)
            renamed.append((path, other))
        for (game, constant, kind), (run_id, _run, _reportdir, _report) in all_records.items():
            assert R.load_verified_synthetic_report(roots, game, constant,
                                                     kind, run_id)['run_type'] == kind
    finally:
        for original, temporary in reversed(renamed):
            temporary.rename(original)

    # A reporting-source manifest mutation must not be made valid merely by
    # updating the report JSON hash; verified replay must reject it.
    game, constant, kind = 'powerball', 'pi', 'TEST_REAL'
    run_id, source_dir, reportdir, _ = all_records[game, constant, kind]
    upstream = source_dir/'run_manifest.json'
    baseline = upstream.read_bytes()
    try:
        changed = json.loads(baseline)
        changed['input_sha256_actual'] = '0'*64
        upstream.write_text(json.dumps(changed, sort_keys=True)+'\n', encoding='utf-8')
        refusals += refuses('forged source digest rejected by downstream report',
            lambda: R.load_verified_synthetic_report(roots, game, constant, kind, run_id))
    finally:
        upstream.write_bytes(baseline)

    assert refusals == 48 + 36 + 1, f'unexpected final integration refusal count {refusals}'
    return 24, 24, refusals, holm


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--self-test', action='store_true')
    modes.add_argument('--run', action='store_true')
    option = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q4F_ISOLATED_ONLY_') as temp:
        roots, n = F.make_temp(Path(temp))
        basic = test_boundaries(roots)
        if option.run:
            runs, reports, extra, holm = run_matrix(roots, n)
            assert len(holm) == 2
        else:
            runs = reports = extra = 0
    print(f'Q4F SYNTHETIC {"INTEGRATION" if option.run else "BOUNDARIES"} PASS: '
          f'guard-refusals={basic+extra} source-runs={runs} reports={reports} '
          'games=2 constants=6 production-scans=0 REAL-history-reads=0')


if __name__ == '__main__':
    main()
