#!/usr/bin/env python3
"""Q4e end-to-end SYNTHETIC-only report provenance qualification.

--self-test: no scanner, stdlib checks. --run: 4 small Q4c TEST runs,
then four create-only derived reports, replay/tamper/refusal checks. Does not
access genuine Powerball/Oz histories, the 5 GB published inputs or Q5.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1 as P
import OUTLANDISH_01_Q4c_Synthetic_Processing_Qualification_v0_1 as FIX
import OUTLANDISH_01_Q4e_Synthetic_Report_Bundle_v0_1 as R


def refuses(label, action):
    try:
        action()
    except (ValueError, RuntimeError, TypeError, FileExistsError, KeyError):
        return 1
    raise AssertionError(f'guard must refuse: {label}')


def altered(path, changed, work, label):
    before = path.read_bytes()
    if before == changed:
        raise AssertionError('mutation is an accidental no-op: ' + label)
    try:
        path.write_bytes(changed)
        return refuses(label, work)
    finally:
        path.write_bytes(before)


def mutate_json(path, action, work, label):
    record = json.loads(path.read_bytes())
    action(record)
    return altered(path, R._encoded(record), work, label)


def cheap_checks(roots):
    total = 0
    assert R.SCHEMA.endswith('_V1')
    assert set(R._codes()) == set(R.CODE_FILES)
    assert R._hash(b'a') == hashlib.sha256(b'a').hexdigest()
    assert R._json(R._encoded({'test': 1})) == {'test': 1}
    total += refuses('REAL entry disallowed', lambda: R._check(
        roots, 'powerball', 'phi', 'REAL', 'REAL_bad'))
    total += refuses('NULL entry disallowed', lambda: R._check(
        roots, 'powerball', 'phi', 'NULL', 'NULL_bad'))
    total += refuses('wrong game', lambda: R._check(
        roots, 'unknown', 'phi', 'TEST_REAL', 'TEST_REAL_valid'))
    total += refuses('wrong constant', lambda: R._check(
        roots, 'oz', 'unknown', 'TEST_REAL', 'TEST_REAL_valid'))
    total += refuses('wrong run/type', lambda: R._check(
        roots, 'oz', 'phi', 'TEST_REAL', 'TEST_NULL_wrong'))
    total += refuses('missing test run', lambda: R._check(
        roots, 'oz', 'phi', 'TEST_REAL', 'TEST_REAL_missing'))
    total += refuses('reject scalar JSON', lambda: R._json(b'[]'))
    total += refuses('reject malformed JSON', lambda: R._json(b'{bad'))
    total += refuses('wrong compare types', lambda: R.compare_verified_summary_counts(
        {'schema': R.SCHEMA, 'run_type': 'TEST_NULL'}, {'schema': R.SCHEMA, 'run_type': 'TEST_REAL'}))
    total += refuses('path outside marked sandbox', lambda:
                     G._inside(roots.base, roots.base.parent/'outside'))
    assert total == 10
    return total


def full_checks(roots, n):
    counts = 0
    specs = [('powerball', 'TEST_REAL', None, 1),
             ('powerball', 'TEST_NULL', 7777, 2),
             ('oz', 'TEST_REAL', None, 1),
             ('oz', 'TEST_NULL', 8888, 2)]
    runs = []
    report_pairs = {}
    for j, (game, kind, seed, k) in enumerate(specs, 1):
        run_id = f'{kind}_q4e_{game}_{j}'
        folder = P.run_synthetic(roots, game, 'phi', kind, run_id,
                                 fixture_digits=n, seed=seed, k=k, chunk_bytes=11)
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in folder.iterdir() if p.is_file()}
        out = R.create_synthetic_report(roots, game, 'phi', kind, run_id,
                                        seed=8675309, iterations=48)
        assert out.name == 'REPORT_' + run_id
        assert out.parent == roots.base / (
            'reports_test_real' if kind == 'TEST_REAL' else 'reports_test_null')
        after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in folder.iterdir() if p.is_file()}
        assert before == after, 'derived reporting must not alter Q4c evidence'
        loaded = R.load_verified_synthetic_report(roots, game, 'phi', kind, run_id)
        assert loaded['schema'] == R.SCHEMA and loaded['run_type'] == kind
        assert loaded['provenance']['source_manifest_sha256'] == hashlib.sha256(
            (folder/'run_manifest.json').read_bytes()).hexdigest()
        assert loaded['provenance']['raw_events_sha256'] == hashlib.sha256(
            (folder/'raw_events.csv').read_bytes()).hexdigest()
        if kind == 'TEST_REAL':
            assert len(loaded['transitions']) == 2
            assert loaded['transitions_summary']['total_adjacent_pairs'] == 2
            assert loaded['permutation']['iterations_requested'] == 48
            assert loaded['primary_is_proposed_owner_vetoable']
            assert 'per_decoy_summary_counts' not in loaded
        else:
            assert loaded['k'] == 2
            assert len(loaded['per_decoy_summary_counts']) == 2
            assert 'transitions' not in loaded and 'category_summary' not in loaded
        report_pairs[game, kind] = loaded
        runs.append((game, kind, run_id, folder, out))
        counts += refuses('create-only report collision', lambda: R.create_synthetic_report(
            roots, game, 'phi', kind, run_id, seed=8675309, iterations=48))
        counts += refuses('type crossover to report loader', lambda: R.load_verified_synthetic_report(
            roots, game, 'phi', 'TEST_NULL' if kind == 'TEST_REAL' else 'TEST_REAL', run_id))

    for game in ('powerball', 'oz'):
        real = report_pairs[game, 'TEST_REAL']
        null = report_pairs[game, 'TEST_NULL']
        comparison = R.compare_verified_summary_counts(real, null)
        from_loaded_reports = R.compare_verified_test_run_summaries(
            roots, game, 'phi',
            next(run_id for g,k,run_id,_,_ in runs if g==game and k=='TEST_REAL'),
            next(run_id for g,k,run_id,_,_ in runs if g==game and k=='TEST_NULL'))
        assert comparison == from_loaded_reports
        assert comparison and all(t['K'] == 2 for t in comparison.values())
        counts += refuses('no REAL to REAL decoy comparison', lambda:
                          R.compare_verified_summary_counts(real, real))
        counts += refuses('cross-game comparator refuses', lambda:
                          R.compare_verified_summary_counts(real,
                              report_pairs['oz' if game == 'powerball' else 'powerball', 'TEST_NULL']))

    # Verified replay never needs to open the packed source.
    original = roots.published_binary('phi')
    moved = original.with_name(original.name+'.test_absent')
    original.rename(moved)
    try:
        for game, kind, run_id, _, _ in runs:
            R.load_verified_synthetic_report(roots, game, 'phi', kind, run_id)
    finally:
        moved.rename(original)

    game, kind, run_id, source, report = runs[0]
    good = lambda: R.load_verified_synthetic_report(roots, game, 'phi', kind, run_id)
    raw = report/'report.json'
    counts += altered(raw, raw.read_bytes()+b'\n', good, 'changed report bytes')
    manifest = report/'report_manifest.json'
    counts += mutate_json(manifest, lambda m: m.update(status='INCOMPLETE'), good,
                          'INCOMPLETE report refusal')
    counts += mutate_json(manifest, lambda m: m.update(source_provenance={'fake':'yes'}), good,
                          'bad source manifest provenance')
    counts += mutate_json(manifest, lambda m: m['implementation_sha256'].update({
        R.CODE_FILES[-1]: '0'*64}), good, 'code digest substitution')
    counts += mutate_json(manifest, lambda m: m.update(permutation_iterations=True), good,
                          'invalid permutation count')
    counts += mutate_json(manifest, lambda m: m.update(report_sha256='0'*64), good,
                          'report digest mismatch')
    # Attempt to repair a modified report digest, to test semantic recomputation.
    original_bytes=raw.read_bytes()
    orig_manifest=manifest.read_bytes()
    changed=R._json(original_bytes)
    changed['counts_are_draw_attributed']=False
    tampered=R._encoded(changed)
    try:
        raw.write_bytes(tampered)
        mm=R._json(orig_manifest)
        mm['report_sha256']=R._hash(tampered)
        manifest.write_bytes(R._encoded(mm))
        counts += refuses('re-hashed incorrect report fails replay',good)
    finally:
        raw.write_bytes(original_bytes)
        manifest.write_bytes(orig_manifest)

    counts += altered(source/'run_manifest.json', (source/'run_manifest.json').read_bytes()+b'\n',
                      good, 'upstream manifest changed')
    counts += altered(source/'raw_events.csv', (source/'raw_events.csv').read_bytes()+b'bad\n',
                      good, 'upstream events changed')
    history=roots.base/'histories/powerball_synthetic.csv'
    counts += altered(history, history.read_bytes()+b'\n', good, 'upstream REAL history changed')
    receipt=roots.receipt('phi')
    counts += altered(receipt, receipt.read_bytes()+b' ', good, 'source receipt changed')
    null_game, null_kind, null_run, null_source, _ = runs[1]
    null_good = lambda: R.load_verified_synthetic_report(
        roots, null_game, 'phi', null_kind, null_run)
    decoy=null_source/'decoy_histories.csv'
    counts += altered(decoy,decoy.read_bytes()+b'\n',null_good,'NULL decoy changed')
    counts += refuses('invalid zero iterations', lambda: R.analyse_verified_synthetic_run(
        roots, game, 'phi', kind, run_id, iterations=0))
    counts += refuses('invalid excessive iterations', lambda: R.analyse_verified_synthetic_run(
        roots, game, 'phi', kind, run_id, iterations=10001))
    counts += refuses('invalid boolean seed', lambda: R.analyse_verified_synthetic_run(
        roots, game, 'phi', kind, run_id, seed=True))
    # A deliberate incomplete derived report must not appear publishable.
    fail_id='TEST_REAL_q4e_failure'
    P.run_synthetic(roots,'powerball','phi','TEST_REAL',fail_id,
                    fixture_digits=n,chunk_bytes=11)
    counts += refuses('fail-before-complete injection', lambda: R.create_synthetic_report(
        roots, 'powerball', 'phi', 'TEST_REAL',fail_id,
        inject_failure_before_complete=True, iterations=10))
    failed = R._report_folder(roots,'TEST_REAL',fail_id,new=False)
    assert R._json((failed/'report_manifest.json').read_bytes())['status']=='INCOMPLETE'
    counts += refuses('incomplete derived report replay', lambda: R.load_verified_synthetic_report(
        roots,'powerball','phi','TEST_REAL',fail_id))
    # Exact permanent source results roots must contain only Q4c original runs.
    for game, kind, rid, original_folder, report_folder in runs:
        assert original_folder.parent in (roots.base/'results',roots.base/'results_null')
        assert report_folder.parent not in (roots.base/'results',roots.base/'results_null')
    assert counts == 29, f'unexpected Q4e refusal count {counts}'
    return counts, len(runs), len(runs)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--run', action='store_true')
    arg=parser.parse_args()
    if arg.self_test == arg.run:
        parser.error('select exactly one qualification mode')
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q4E_TEMP_ONLY_') as temp:
        roots,n=FIX.make_temp(Path(temp))
        base=cheap_checks(roots)
        if arg.run:
            more, runs, reports=full_checks(roots,n)
        else:
            more=runs=reports=0
    label='INTEGRATION' if arg.run else 'GUARDS'
    print(f'Q4E SYNTHETIC {label} PASS: source-runs={runs} reports={reports} '
          f'guard-refusals={base+more} production-scans=0 REAL-history-reads=0')


if __name__ == '__main__':
    main()
