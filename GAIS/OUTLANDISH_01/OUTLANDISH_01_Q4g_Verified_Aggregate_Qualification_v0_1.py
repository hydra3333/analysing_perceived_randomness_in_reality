#!/usr/bin/env python3
"""Q4g verified cross-constant TEST reporting, temporary artificial files only.

--self-test: fail-closed roster/type/root checks without scanner invocation.
--run: actual installed Q3/Q4c/e via Q4f synthetic fixture matrix, two game
aggregates, adversarial tampering and replay with all packed files absent.
No production scan API, REAL history read or Q5 authorization.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile

import OUTLANDISH_01_Q4c_Synthetic_Processing_Qualification_v0_1 as F
import OUTLANDISH_01_Q4f_Final_Synthetic_Integration_v0_1 as Q4F
import OUTLANDISH_01_Q4g_Verified_Synthetic_Aggregate_v0_1 as A
import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S


def refused(label, f) -> int:
    try:
        f()
    except (ValueError, FileExistsError, RuntimeError, TypeError, KeyError):
        return 1
    raise AssertionError(f'UNEXPECTED ACCEPTANCE: {label}')


def rosters(game):
    return ({c:f'TEST_REAL_q4f_{game}_{c}' for c in S.CONSTANTS},
            {c:f'TEST_NULL_q4f_{game}_{c}' for c in S.CONSTANTS})


def self_tests(roots):
    real,null=rosters('powerball')
    checks=0
    checks+=refused('unknown game',lambda: A.compute_verified_test_game_aggregate(
        roots,'not_a_game',real,null))
    checks+=refused('missing constant',lambda: A.compute_verified_test_game_aggregate(
        roots,'powerball',{k:v for k,v in real.items() if k!='pi'},null))
    checks+=refused('extra constant',lambda: A.compute_verified_test_game_aggregate(
        roots,'powerball',real | {'tau':'TEST_REAL_q4f_powerball_tau'},null))
    checks+=refused('swapped REAL/NULL',lambda: A.compute_verified_test_game_aggregate(
        roots,'powerball',null,real))
    checks+=refused('duplicate REAL run ID',lambda: A.compute_verified_test_game_aggregate(
        roots,'powerball',real | {'pi':real['phi']},null))
    checks+=refused('cross-game label',lambda: A.compute_verified_test_game_aggregate(
        roots,'oz',real,null))
    checks+=refused('unknown group game',lambda: A._aggregate_folder(
        roots,'powerball','TEST_AGGREGATE_oz_bad',create=False))
    checks+=refused('unsafe group path syntax',lambda: A._aggregate_folder(
        roots,'powerball','TEST_AGGREGATE_powerball_../bad',create=False))
    checks+=refused('missing verified reports',lambda: A.compute_verified_test_game_aggregate(
        roots,'powerball',real,null))
    checks+=refused('no synthetic aggregate yet',lambda: A.load_verified_test_game_aggregate(
        roots,'powerball','TEST_AGGREGATE_powerball_missing'))
    assert checks==10
    # Strict fixed-six Holm with N/A, independently checked at Q4d.
    raw={c:None for c in S.CONSTANTS}
    result=S.holm_six_constants(raw)
    assert len(result)==6 and all(p is None for p in result.values())
    raw['pi']=0.01
    result=S.holm_six_constants(raw)
    assert abs(result['pi']-0.06)<1e-12 and all(result[c] is None for c in S.CONSTANTS if c!='pi')
    return checks


def mutate_bytes(path, change, action, label):
    previous=path.read_bytes()
    updated=change(previous)
    assert updated!=previous, 'mutation must change bytes: '+label
    try:
        path.write_bytes(updated)
        return refused(label,action)
    finally:
        path.write_bytes(previous)


def mutate_json(path, update, action, label):
    def change(raw):
        obj=json.loads(raw)
        update(obj)
        return (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode('utf-8')
    return mutate_bytes(path,change,action,label)


def integration(roots,n):
    source_runs,source_reports,legacy_refusals,existing_holm=Q4F.run_matrix(roots,n)
    assert (source_runs,source_reports,legacy_refusals)==(24,24,85)
    counts=0
    aggregates={}
    before={}
    for game in A.GAMES:
        real,null=rosters(game)
        for constant in S.CONSTANTS:
            for kind,rid in (('TEST_REAL',real[constant]),('TEST_NULL',null[constant])):
                f=A.R._report_folder(roots,kind,rid,new=False)
                before[f]=tuple(sorted((p.name,hashlib.sha256(p.read_bytes()).hexdigest())
                                       for p in f.iterdir() if p.is_file()))
        group=f'TEST_AGGREGATE_{game}_q4g'
        created=A.create_verified_test_game_aggregate(roots,game,group,real,null)
        result=A.load_verified_test_game_aggregate(roots,game,group)
        assert result['scope']==A.SCOPE and result['game']==game
        assert set(result['per_constant'])==set(S.CONSTANTS)
        assert {c:result['per_constant'][c]['holm_adjusted_primary_p']
                for c in S.CONSTANTS}==existing_holm[game]
        assert result['historical_fixture_sha256'] and result['common_logical_digits']==n
        assert result['fixed_holm_family_size']==6
        assert result['decoy_K_per_constant']==2 and result['permutation_iterations']==48
        assert created.parent.name==game and created.parent.parent.name=='reports_test_aggregate'
        aggregates[game]=(group,created)
        counts+=1
    assert counts==2
    for folder,baseline in before.items():
        after=tuple(sorted((p.name,hashlib.sha256(p.read_bytes()).hexdigest())
                           for p in folder.iterdir() if p.is_file()))
        assert baseline==after, 'Q4g mutated a qualified Q4e report'
    # All six synthetic BCD files may be completely unavailable on replay.
    moved=[]
    try:
        for constant in S.CONSTANTS:
            binary=roots.published_binary(constant)
            absent=binary.with_name(binary.name+'.absent_for_replay')
            binary.rename(absent)
            moved.append((binary,absent))
        for game,(group,_) in aggregates.items():
            assert A.load_verified_test_game_aggregate(roots,game,group)['game']==game
    finally:
        for binary,absent in reversed(moved):
            absent.rename(binary)
    checks=0
    for game,(group,_) in aggregates.items():
        real,null=rosters(game)
        other='oz' if game=='powerball' else 'powerball'
        checks+=refused('create-only repeated aggregate',lambda: A.create_verified_test_game_aggregate(
            roots,game,group,real,null))
        checks+=refused('cross-game verified aggregation',lambda: A.load_verified_test_game_aggregate(
            roots,other,group))
    game='powerball'
    group,folder=aggregates[game]
    action=lambda: A.load_verified_test_game_aggregate(roots,game,group)
    checks+=mutate_json(folder/'aggregate_manifest.json',lambda d: d.update(status='INCOMPLETE'),
                        action,'incomplete aggregate')
    checks+=mutate_json(folder/'aggregate_manifest.json',lambda d: d.update(
                        implementation_sha256={'malicious':'0'*64}),action,'changed code identity')
    checks+=mutate_json(folder/'aggregate_manifest.json',lambda d: d.update(
                        aggregate_sha256='0'*64),action,'tampered aggregate hash')
    checks+=mutate_json(folder/'aggregate.json',lambda d: d.update(fixed_holm_family_size=5),
                        action,'tampered Holm family')
    checks+=mutate_json(folder/'aggregate_manifest.json',lambda d: d.update(
                        real_runs={**d['real_runs'],'pi':d['real_runs']['phi']}),
                        action,'cross-constant source injection')
    upstream=A.R._report_folder(roots,'TEST_REAL','TEST_REAL_q4f_powerball_pi',new=False)
    checks+=mutate_json(upstream/'report.json',lambda d: d.update(game='oz'),
                        action,'tampered verified report')
    checks+=mutate_json(upstream/'report_manifest.json',lambda d: d.update(status='INCOMPLETE'),
                        action,'upstream report incomplete')
    upstream_run=roots.run_location('TEST_REAL','TEST_REAL_q4f_powerball_pi')
    checks+=mutate_json(upstream_run/'run_manifest.json',lambda d: d.update(status='INCOMPLETE'),
                        action,'upstream source incomplete')
    real,null=rosters('powerball')
    try:
        A.create_verified_test_game_aggregate(roots,game,'TEST_AGGREGATE_powerball_failed',
                                              real,null,inject_failure_before_complete=True)
    except RuntimeError:
        pass
    else:
        raise AssertionError('injected failure should refuse completion')
    checks+=refused('incomplete aggregate refused',lambda: A.load_verified_test_game_aggregate(
        roots,game,'TEST_AGGREGATE_powerball_failed'))
    # Refusal tests must restore full prior correctness.
    assert A.load_verified_test_game_aggregate(roots,game,group)['game']==game
    assert checks==13,checks
    return source_runs,source_reports,counts,checks


def main():
    p=argparse.ArgumentParser(description=__doc__)
    s=p.add_mutually_exclusive_group(required=True)
    s.add_argument('--self-test',action='store_true')
    s.add_argument('--run',action='store_true')
    args=p.parse_args()
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q4G_TEST_ONLY_') as directory:
        roots,n=F.make_temp(Path(directory))
        guards=self_tests(roots)
        if args.run:
            runs,reports,groups,extras=integration(roots,n)
        else:
            runs=reports=groups=extras=0
    print(f'Q4G SYNTHETIC {"INTEGRATION" if args.run else "GUARDS"} PASS: '
          f'guard-refusals={guards+extras} source-runs={runs} '
          f'upstream-reports={reports} verified-game-aggregates={groups} '
          'games=2 constants=6 production-scans=0 REAL-history-reads=0')


if __name__=='__main__':
    main()
