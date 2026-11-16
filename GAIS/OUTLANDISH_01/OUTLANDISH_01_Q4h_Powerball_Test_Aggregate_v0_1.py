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

SCHEMA = 'OUTLANDISH_Q4H_POWERBALL_AGGREGATE_V2'


def _folder(mode, aggregate_id):
    mode = mode.checked()
    if not isinstance(aggregate_id, str) or not aggregate_id.startswith(
            mode.run_type + '_AGGREGATE_powerball_'):
        raise ValueError('aggregate must carry matching type and game')
    return mode.roots.run_location(mode.run_type, aggregate_id)


def compute_aggregate(mode: M.PowerballMode, real_runs: dict):
    mode = mode.checked()
    if not isinstance(real_runs, dict) or set(real_runs) != set(S.CONSTANTS):
        raise ValueError('exact six REAL-like constant run roster required')
    if len(set(real_runs.values())) != len(S.CONSTANTS):
        raise ValueError('duplicate constant run identity')
    entries, pvals, histories, digests, lengths = {}, {}, set(), set(), set()
    for const in S.CONSTANTS:
        run_id = real_runs[const]
        body = R.load_report(mode,const,run_id)['report']
        if body['primary_family'] != 'K6S':
            raise ValueError('wrong predeclared primary family')
        p = body['permutation']['centered_two_sided_p']
        if p is not None and (type(p) not in (int,float) or not 0 <= p <= 1):
            raise ValueError('invalid primary p-value')
        pvals[const] = p
        histories.add(body['history_sha256'])
        lengths.add(body['digits'])
        digests.add(body['source_sha256'])
        report = G._inside(mode.roots.base, mode.roots.run_location(mode.run_type,run_id)/'report.json')
        entries[const] = {'source_run': run_id,
                          'report_sha256': hashlib.sha256(report.read_bytes()).hexdigest(),
                          'raw_primary_p': p,
                          'observed_median_gap': body['permutation']['observed_median'],
                          'valid_permutations': body['permutation']['valid_permutations'],
                          'seed': body['seed'], 'seed_label': body['seed_label']}
    if len(histories) != 1 or len(lengths) != 1 or len(digests) != len(S.CONSTANTS):
        raise ValueError('six reports must share history and N, with six different inputs')
    corrected = S.holm_six_constants(pvals)
    for c in S.CONSTANTS:
        entries[c]['holm_adjusted_p'] = corrected[c]
    return {'schema':SCHEMA,'game':'powerball','run_type':mode.run_type,
            'primary_family':'K6S','permutations':R.PERMUTATIONS,
            'seed_rule':'DERIVED_PER_GAME_AND_CONSTANT_V1' if not mode.roots.synthetic
                        else 'PROVISIONAL_SYNTHETIC_271828',
            'history_sha256':next(iter(histories)),'digits':next(iter(lengths)),
            'holm_family':list(S.CONSTANTS),'per_constant':entries,
            'null_comparison':'NOT_RUN_OPTIONAL',
            'primary_owner_vetoable':True}


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
    folder = _folder(mode,aggregate_id)
    raw = G._inside(mode.roots.base,folder/'aggregate.json').read_bytes()
    recorded = G._inside(mode.roots.base,folder/'aggregate.sha256').read_bytes()
    if recorded != (hashlib.sha256(raw).hexdigest()+'\n').encode('ascii'):
        raise ValueError('aggregate digest mismatch')
    body = json.loads(raw.decode('utf-8'))
    if (not isinstance(body,dict) or body.get('schema') != SCHEMA
            or body.get('game') != 'powerball' or body.get('run_type') != mode.run_type
            or body.get('aggregate_id') != aggregate_id
            or body.get('null_comparison') != 'NOT_RUN_OPTIONAL'
            or body.get('permutations') != R.PERMUTATIONS
            or body.get('holm_family') != list(S.CONSTANTS)
            or not isinstance(body.get('per_constant'),dict)
            or set(body['per_constant']) != set(S.CONSTANTS)):
        raise ValueError('bad aggregate identity or six-constant scope')
    # Replay each report's digest/source identity WITHOUT recomputing Holm or MC.
    for constant in S.CONSTANTS:
        item = body['per_constant'][constant]
        if not isinstance(item,dict) or not isinstance(item.get('source_run'),str):
            raise ValueError('bad aggregate report reference')
        run_id = item['source_run']
        view = R.load_report(mode,constant,run_id)['report']
        report = G._inside(mode.roots.base,mode.roots.run_location(mode.run_type,run_id)/'report.json')
        if hashlib.sha256(report.read_bytes()).hexdigest() != item.get('report_sha256'):
            raise ValueError('one stored source report digest changed')
        if (view['history_sha256'] != body['history_sha256']
                or view['digits'] != body['digits']):
            raise ValueError('one source report history/length differs')
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
