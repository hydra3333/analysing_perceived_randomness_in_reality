#!/usr/bin/env python3
"""Shared Powerball six-constant aggregate, no NULL prerequisite.

Aggregate is create-only under existing REAL/TEST_REAL results root. Ordinary
load checks stored aggregate digest and six report digests, not recalculation.
"""
from __future__ import annotations

import hashlib
import json

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S
import OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1 as P
import OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1 as R
import OUTLANDISH_01_Q4i_Mode_v0_1 as M

SCHEMA = 'OUTLANDISH_Q4H_POWERBALL_AGGREGATE_V3'
OZ_SCHEMA = 'OUTLANDISH_Q4H_OZ_AGGREGATE_V1'


def _folder(mode, aggregate_id):
    mode = mode.checked()
    if not isinstance(aggregate_id, str) or not aggregate_id.startswith(
            mode.run_type + '_AGGREGATE_' + mode.game + '_'):
        raise ValueError('aggregate must carry matching type and game')
    return mode.roots.run_location(mode.run_type, aggregate_id)


def compute_aggregate(mode: M.PowerballMode, real_runs: dict):
    mode = mode.checked()
    if mode.game == 'oz':
        return _compute_oz_aggregate(mode, real_runs)
    if not isinstance(real_runs, dict) or set(real_runs) != set(S.CONSTANTS):
        raise ValueError('exact six REAL-like constant run roster required')
    if len(set(real_runs.values())) != len(S.CONSTANTS):
        raise ValueError('duplicate constant run identity')
    entries, pvals, secondary_pvals, histories, digests, lengths = {}, {}, {}, set(), set(), set()
    for const in S.CONSTANTS:
        run_id = real_runs[const]
        body = R.load_report(mode,const,run_id)['report']
        if (body['primary_family'] != 'K6S' or body['primary_statistic'] != R.PRIMARY_STATISTIC
                or body['secondary_statistic'] != R.SECONDARY_STATISTIC):
            raise ValueError('wrong predeclared primary/secondary statistic')
        primary = body['permutation']['geometric_primary']
        secondary = body['permutation']['median_secondary']
        p, sp = primary['centered_two_sided_p'], secondary['centered_two_sided_p']
        if any(v is not None and (type(v) not in (int, float) or not 0 <= v <= 1)
               for v in (p, sp)):
            raise ValueError('invalid primary/secondary p-value')
        pvals[const], secondary_pvals[const] = p, sp
        histories.add(body['history_sha256'])
        lengths.add(body['digits'])
        digests.add(body['source_sha256'])
        report = G._inside(mode.roots.base, mode.roots.run_location(mode.run_type,run_id)/'report.json')
        entries[const] = {'source_run': run_id,
                          'report_sha256': hashlib.sha256(report.read_bytes()).hexdigest(),
                          'raw_primary_p': p,
                          'raw_secondary_p': sp,
                          'observed_primary_mean_log10_gap_plus_one': primary['observed'],
                          'observed_median_gap': secondary['observed'],
                          'valid_permutations': body['permutation']['valid_permutations'],
                          'seed': body['seed'], 'seed_label': body['seed_label']}
    if len(histories) != 1 or len(lengths) != 1 or len(digests) != len(S.CONSTANTS):
        raise ValueError('six reports must share history and N, with six different inputs')
    corrected = S.holm_six_constants(pvals)
    corrected_secondary = S.holm_six_constants(secondary_pvals)
    for c in S.CONSTANTS:
        entries[c]['holm_adjusted_p'] = corrected[c]
        entries[c]['holm_adjusted_secondary_p'] = corrected_secondary[c]
    return {'schema':SCHEMA,'game':'powerball','run_type':mode.run_type,
            'primary_family':'K6S',
            'primary_statistic':R.PRIMARY_STATISTIC,
            'secondary_statistic':R.SECONDARY_STATISTIC,
            'secondary_exploratory':True,
            'legacy_exposure_disclosure':R.D5_LEGACY_EXPOSURE_DISCLOSURE,
            'permutations':R.PERMUTATIONS,
            'seed_rule':'DERIVED_PER_GAME_AND_CONSTANT_V1' if not mode.roots.synthetic
                        else 'PROVISIONAL_SYNTHETIC_271828',
            'history_sha256':next(iter(histories)),'digits':next(iter(lengths)),
            'holm_family':list(S.CONSTANTS),
            'secondary_holm_family':list(S.CONSTANTS),
            'per_constant':entries,
            'null_comparison':'NOT_RUN_OPTIONAL',
            'primary_owner_vetoable':False}


def _compute_oz_aggregate(mode, real_runs: dict):
    """Owner D6: one fixed 18-hypothesis family, NO Oz secondary."""
    if (not isinstance(real_runs, dict) or set(real_runs) != set(S.CONSTANTS)
            or len(set(real_runs.values())) != len(S.CONSTANTS)):
        raise ValueError('exact six distinct Oz REAL report IDs required')
    keys = [f'{const}:{view}' for const in S.CONSTANTS for view in S.OZ_D6_VIEWS]
    pvalues, entries, histories, digests, lengths = {}, {}, set(), set(), set()
    for const in S.CONSTANTS:
        run_id = real_runs[const]
        body = R.load_report(mode, const, run_id)['report']
        if (body['game'] != 'oz' or body['primary_statistic'] != S.OZ_D6_PRIMARY
                or body['primary_views'] != list(S.OZ_D6_VIEWS)):
            raise ValueError('incorrect Oz D6 report identity')
        views = body['permutation']['views']
        histories.add(body['history_sha256'])
        lengths.add(body['digits'])
        digests.add(body['source_sha256'])
        report_path = G._inside(mode.roots.base,
                               mode.roots.run_location(mode.run_type, run_id) / 'report.json')
        entry = {'source_run': run_id,
                 'report_sha256': hashlib.sha256(report_path.read_bytes()).hexdigest(),
                 'seed': body['seed'], 'seed_label': body['seed_label'],
                 'views': {}}
        for view in S.OZ_D6_VIEWS:
            data = views[view]
            pv = data['centered_two_sided_p']
            if pv is not None and (type(pv) not in (int, float) or not 0 <= pv <= 1):
                raise ValueError('invalid Oz primary p-value')
            pvalues[f'{const}:{view}'] = pv
            entry['views'][view] = {
                'family': S.OZ_D6_FAMILIES[view],
                'raw_primary_p': pv,
                'observed_primary_mean_log10_gap_plus_one': data['observed'],
                'valid_permutations': data['valid_permutations']}
        entries[const] = entry
    if len(histories) != 1 or len(lengths) != 1 or len(digests) != len(S.CONSTANTS):
        raise ValueError('Oz reports must share history/digits and have six distinct sources')
    adjusted = S.holm_adjusted(pvalues, keys)
    for const in S.CONSTANTS:
        for view in S.OZ_D6_VIEWS:
            entries[const]['views'][view]['holm_adjusted_p'] = adjusted[f'{const}:{view}']
    return {
        'schema': OZ_SCHEMA, 'game': 'oz', 'run_type': mode.run_type,
        'primary_statistic': S.OZ_D6_PRIMARY,
        'primary_views': list(S.OZ_D6_VIEWS),
        'primary_families': dict(S.OZ_D6_FAMILIES),
        'secondary_statistic': None, 'secondary_exploratory': False,
        'permutations': R.PERMUTATIONS,
        'seed_rule': ('PROVISIONAL_SYNTHETIC_271828' if mode.roots.synthetic
                      else 'DERIVED_PER_GAME_AND_CONSTANT_V1'),
        'history_sha256': next(iter(histories)), 'digits': next(iter(lengths)),
        'holm_family': keys, 'per_constant': entries,
        'null_comparison': 'NOT_RUN_OPTIONAL', 'primary_owner_vetoable': False}


def create_aggregate(mode: M.PowerballMode, aggregate_id: str, real_runs: dict):
    body = compute_aggregate(mode,real_runs)
    folder = _folder(mode,aggregate_id)
    roots = mode.roots
    roots.validate_run_location(mode.run_type,aggregate_id,folder)
    folder.mkdir(exist_ok=False)
    body['aggregate_id'] = aggregate_id
    raw = P.encode(body)
    P.put_new(folder/'aggregate.json',raw)
    P.put_new(folder/'aggregate.sha256',(hashlib.sha256(raw).hexdigest()+'\n').encode('ascii'))
    return folder


def load_aggregate(mode: M.PowerballMode, aggregate_id: str):
    mode = mode.checked()
    folder = _folder(mode, aggregate_id)
    raw = G._inside(mode.roots.base, folder/'aggregate.json').read_bytes()
    recorded = G._inside(mode.roots.base, folder/'aggregate.sha256').read_bytes()
    if recorded != (hashlib.sha256(raw).hexdigest() + '\n').encode('ascii'):
        raise ValueError('aggregate digest mismatch')
    body = json.loads(raw.decode('utf-8'))
    required = {
        'schema': SCHEMA if mode.game == 'powerball' else OZ_SCHEMA,
        'game': mode.game, 'run_type': mode.run_type,
        'aggregate_id': aggregate_id, 'null_comparison': 'NOT_RUN_OPTIONAL',
        'permutations': R.PERMUTATIONS}
    if mode.game == 'powerball':
        required.update(primary_statistic=R.PRIMARY_STATISTIC,
                        secondary_statistic=R.SECONDARY_STATISTIC,
                        secondary_exploratory=True,
                        legacy_exposure_disclosure=R.D5_LEGACY_EXPOSURE_DISCLOSURE,
                        holm_family=list(S.CONSTANTS),
                        secondary_holm_family=list(S.CONSTANTS))
    else:
        required.update(primary_statistic=S.OZ_D6_PRIMARY,
                        primary_views=list(S.OZ_D6_VIEWS),
                        primary_families=dict(S.OZ_D6_FAMILIES),
                        secondary_statistic=None, secondary_exploratory=False,
                        holm_family=[f'{c}:{v}' for c in S.CONSTANTS for v in S.OZ_D6_VIEWS])
    if (not isinstance(body, dict) or any(body.get(k) != v for k,v in required.items())
            or not isinstance(body.get('per_constant'), dict)
            or set(body['per_constant']) != set(S.CONSTANTS)):
        raise ValueError('bad aggregate identity or family scope')
    # Digest-and-identity replay, WITHOUT recalculating Holm or Monte Carlo.
    for const in S.CONSTANTS:
        item = body['per_constant'][const]
        if not isinstance(item, dict) or not isinstance(item.get('source_run'), str):
            raise ValueError('bad aggregate source report reference')
        run_id = item['source_run']
        report = R.load_report(mode, const, run_id)['report']
        filename = G._inside(mode.roots.base, mode.roots.run_location(
            mode.run_type, run_id)/'report.json')
        if hashlib.sha256(filename.read_bytes()).hexdigest() != item.get('report_sha256'):
            raise ValueError('stored source report digest changed')
        if (report['history_sha256'] != body['history_sha256']
                or report['digits'] != body['digits']):
            raise ValueError('aggregate report history/length mismatch')
        if mode.game == 'oz':
            if (not isinstance(item.get('views'), dict)
                    or set(item['views']) != set(S.OZ_D6_VIEWS)
                    or any(item['views'][v].get('raw_primary_p') !=
                           report['permutation']['views'][v]['centered_two_sided_p']
                           for v in S.OZ_D6_VIEWS)):
                raise ValueError('Oz aggregate view identity mismatch')
    return body


# Thin compatibility functions keep older synthetic qualification harness.
def _legacy_test_aggregate_id(value):
    # Retained reviewer scripts use TEST_AGGREGATE_...; transparently map to
    # the ONE checked TEST_REAL result root without adding another directory.
    if isinstance(value,str) and value.startswith('TEST_AGGREGATE_'):
        suffix = value[len('TEST_AGGREGATE_'):]
        return 'TEST_REAL_AGGREGATE_' + (suffix if suffix.startswith('powerball_')
                                          else 'powerball_' + suffix)
    return value

def compute_test_aggregate(roots,profile,real_runs):
    if not isinstance(real_runs,dict) or set(real_runs) != set(S.CONSTANTS):
        raise ValueError('exact six TEST constant roster required')
    m=P._mode_from_run(roots,profile,real_runs['pi'])
    return compute_aggregate(m,real_runs)

def create_test_aggregate(roots,profile,aggregate_id,real_runs):
    m=P._mode_from_run(roots,profile,real_runs['pi'])
    return create_aggregate(m,_legacy_test_aggregate_id(aggregate_id),real_runs)

def load_test_aggregate(roots,profile,aggregate_id):
    # Verified digits are obtained from a persisted aggregate's first run.
    aggregate_id=_legacy_test_aggregate_id(aggregate_id)
    folder=roots.run_location('TEST_REAL',aggregate_id)
    raw=(G._inside(roots.base,folder/'aggregate.json')).read_bytes()
    obj=json.loads(raw.decode('utf-8'))
    rid=obj['per_constant']['pi']['source_run']
    return load_aggregate(P._mode_from_run(roots,profile,rid),aggregate_id)


if __name__ == '__main__':
    raise SystemExit('No aggregate CLI; production entry is the single Q4i module')
