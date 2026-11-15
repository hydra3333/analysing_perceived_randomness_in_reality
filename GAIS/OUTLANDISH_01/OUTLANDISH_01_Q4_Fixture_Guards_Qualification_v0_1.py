#!/usr/bin/env python3
"""OUTLANDISH_01 Q4 fixture-only guard qualification. --self-test / --run only.

No REAL/NULL data or production paths accessed, no production run API exposed.
All binary/drawset/receipt/manifest files live in TemporaryDirectory.
Also regression-checks the 4 MB default against old v0.3 on planted fixtures.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import tempfile

from OUTLANDISH_01_Q2_Independent_Oracle_v0_1 import encoded, pack_independent, plant, oracle
from OUTLANDISH_01_Q2_LegacyScanner_Comparison_v0_1 import scenario_set, DRAWS as PB_DRAWS
import OUTLANDISH_01_Q3_Shared_Qualification_v0_2 as OZ_SUITE
import OUTLANDISH_01_Q3_Packed_Matcher_v0_3 as PREVIOUS
import OUTLANDISH_01_Q3_Packed_Matcher_v0_4 as MATCHER
import OUTLANDISH_01_Q4_Fixture_Run_Guards_v0_1 as GUARD


def fail_expected(name, work, fragment=None):
    try:
        work()
    except (ValueError, FileExistsError, RuntimeError) as e:
        if fragment and fragment not in str(e):
            raise AssertionError(f'{name}: wrong refusal: {e}') from e
        return 1
    raise AssertionError(f'{name}: unsafe action unexpectedly accepted')


def create_sandbox(root):
    root.mkdir(exist_ok=False)
    (root/'SYNTHETIC_FIXTURE_MARKER').write_bytes(GUARD.MAGIC)
    for relative in ('fixture_digits','fixture_histories','fixture_results_real','fixture_results_null'):
        (root/relative).mkdir()


def make_profile(root, game, kind):
    profile=GUARD.FixtureProfile(root,game,kind,'phi',1,4)
    if game=='powerball':
        draws=PB_DRAWS[:3]
        # Mixed 16/14 fields, including PB matching a main.
        text=plant(181,[(11,encoded(*draws[0].mains,draws[0].pb)),
                        (54,encoded(*draws[1].mains)),
                        (99,encoded(2,4,6,8,12,14,draws[2].pb))])
        header=GUARD.TEST_HEADER_PB
        rows=[(d.number,*d.mains,d.pb) for d in draws]
    else:
        draws=OZ_SUITE.DRAWS[:3]
        o1=draws[0]
        text=plant(181,[(11,encoded(*o1.mains)),
                        (54,encoded(o1.supp[0],*o1.mains[:6])),
                        (99,encoded(*draws[1].mains[:6]))])
        header=GUARD.TEST_HEADER_OZ
        rows=[(i+1,*d.mains,*d.supp) for i,d in enumerate(draws)]
    binary=pack_independent(text)
    profile.packed.write_bytes(binary)
    h=hashlib.sha256(binary).hexdigest()
    receipt={'format':GUARD.FORMAT,'format_version':1,'scope':GUARD.SCOPE,
             'constant':'phi','binary_name':profile.packed.name,
             'digits_including_integer':len(text),'packed_bytes':len(binary),
             'binary_sha256_streamed':h,
             'samples':[{'offset_bytes':0,'size':len(binary),'sha256':h}],
             'fixture_warning':'SYNTHETIC_ONLY_DO_NOT_USE_AS_REAL'}
    profile.receipt.write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    with profile.draws_file.open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(header)
        for index,row in enumerate(rows):
            if kind=='TEST_NULL':
                row=(f'DECOY-{index+1:04d}',*row[1:])
            writer.writerow(row)
    return profile


def _alter(path, transform, run, reason):
    original=path.read_bytes()
    changed=transform(original)
    if changed == original:
        raise AssertionError(f'{reason} fixture mutation was a no-op')
    try:
        path.write_bytes(changed)
        return fail_expected(reason,run)
    finally:
        path.write_bytes(original)


def _modify_json(path, update, run, label):
    def mut(b):
        obj=json.loads(b)
        update(obj)
        return (json.dumps(obj,sort_keys=True,indent=2)+'\n').encode('utf-8')
    return _alter(path,mut,run,label)


def _malformed_events_and_resealed_manifest(profile, run_id, *, kind):
    run=profile.result_root/run_id
    ev=run/'raw_events.csv'
    manifest=run/'run_manifest.json'
    original_raw=ev.read_bytes()
    original_manifest=manifest.read_bytes()
    cells=list(csv.reader(original_raw.decode('utf-8').splitlines()))
    assert len(cells)>1, 'need at least one event for duplicate mutation'
    if kind=='duplicate':
        cells.insert(2,cells[1][:])
    elif kind=='order':
        cells[1],cells[-1]=cells[-1],cells[1]
        if cells[1]==cells[-1]:
            raise AssertionError('order fixture did not change')
    elif kind=='EOF':
        cells[1][2]='180'
    elif kind=='NULL_as_REAL':
        cells[1][0]='DECOY-0001'
    elif kind=='REAL_as_NULL':
        cells[1][0]='1'
    else:
        raise AssertionError(kind)
    # Modify the event file and reseal its digest: structural validation MUST
    # still reject the row even if the same actor modifies the manifest hash.
    with ev.open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerows(cells)
    meta=json.loads(original_manifest)
    meta['event_sha256']=hashlib.sha256(ev.read_bytes()).hexdigest()
    meta['event_count']=len(cells)-1
    manifest.write_text(json.dumps(meta,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    try:
        return fail_expected(f'event structure {kind} despite matching digest',
                             lambda:GUARD.load_verified_fixture(profile,run_id,
                                            require_type=profile.run_type))
    finally:
        ev.write_bytes(original_raw)
        manifest.write_bytes(original_manifest)


def check_first_class_guards(root):
    cases=[]
    for game in ('powerball','oz'):
        for run_type in ('TEST_REAL','TEST_NULL'):
            profile=make_profile(root,game,run_type)
            run_id='TEST_'+game.upper()+'_'+run_type.replace('TEST_','')
            cases.append((profile,run_id))
            run=GUARD.run_fixture(profile,run_id,chunk_bytes=3)
            meta=json.loads((run/'run_manifest.json').read_text(encoding='utf-8'))
            assert meta['status']=='COMPLETE' and meta['chunk_bytes']==3
            result=GUARD.load_verified_fixture(profile,run_id,require_type=run_type)
            assert run.parent == profile.result_root and not (
                (profile.root / ('fixture_results_null' if run_type=='TEST_REAL' else 'fixture_results_real'))
                / run_id).exists(), 'cross-root fixture publication'
            assert result, f'{game} {run_type}: fixture unexpectedly has no matches'
            with (run/'raw_events.csv').open('r',encoding='utf-8') as f:
                second=list(csv.reader(f))[1][0]
            if run_type=='TEST_NULL':
                assert second.startswith('DECOY-') and not second.isdecimal()
            else:
                assert second.isdecimal()
            fail_expected('create-only run folder',lambda:GUARD.run_fixture(profile,run_id))
            other='TEST_NULL' if run_type=='TEST_REAL' else 'TEST_REAL'
            fail_expected('cross-type loader',lambda:GUARD.load_verified_fixture(profile,run_id,
                                                                      require_type=other))
            print(f'PASS: fixture {game}/{run_type} events={len(result)}, sealed manifest and strictly typed loader')
    return cases


def self_test():
    if not __debug__:
        raise RuntimeError('run without -O, assertions are required')
    assert MATCHER.resolve_chunk_bytes() == 4_000_000
    assert MATCHER.resolve_chunk_bytes(None) == 4_000_000
    assert MATCHER.resolve_chunk_bytes(8_000_000) == 8_000_000
    assert MATCHER.resolve_chunk_bytes(1) == 1
    for bad in (0,-2,True,64_000_001,1.5):
        fail_expected('invalid chunk override',lambda b=bad:MATCHER.resolve_chunk_bytes(b))
    assert GUARD.TEST_HEADER_PB[0]=='draw_number'
    assert GUARD.TEST_SCOPE!='REAL' and GUARD.TEST_SCOPE!='NULL'
    print('Q4 FIXTURE SELF-TEST PASS: stable 4MB default, 8MB override, TEST-only scope')


def q3_v04_regression(root):
    checks=0
    # Ensure v0.4 changes no match semantics relative to already qualified v0.3.
    for game in ('powerball','oz'):
        cases=( ((x.name,x.digits,PB_DRAWS,x.prefix_digits or len(x.digits))
                  for x in scenario_set()) if game=='powerball' else
                ((name,txt,draws,n) for name,txt,draws,n,_ in OZ_SUITE.scenarios()))
        for name,text,draws,n in cases:
            blob=pack_independent(text)
            src=root/f'TEST_{game}_{name}.packed.bin'
            src.write_bytes(blob)
            expected=hashlib.sha256(blob).hexdigest()
            if game=='powerball':
                oldrows=[PREVIOUS.PBRecord(d.number,d.mains,d.pb) for d in draws]
                newrows=[MATCHER.PBRecord(d.number,d.mains,d.pb) for d in draws]
                old=PREVIOUS.scan_packed_stream
                new=MATCHER.scan_packed_stream
            else:
                oldrows=[PREVIOUS.OzRecord(d.number,d.mains,d.supp) for d in draws]
                newrows=[MATCHER.OzRecord(d.number,d.mains,d.supp) for d in draws]
                old=PREVIOUS.scan_packed_oz_stream
                new=MATCHER.scan_packed_oz_stream
            for cb in (1,3,17):
                args=dict(physical_digits=len(text),effective_digits=n,
                          expected_full_sha256=expected,chunk_bytes=cb)
                a=root/f'{game}.{name}.{cb}.v03.csv'
                b=root/f'{game}.{name}.{cb}.v04.csv'
                old_result=old(src,draws=oldrows,output_csv=a,**args)
                new_result=new(src,draws=newrows,output_csv=b,**args)
                reference={(h.draw,h.family,h.start,h.digits) for h in oracle(game,text[:n],list(draws))}
                actual={(int(r[0]),r[1],int(r[2]),r[3]) for r in list(csv.reader(b.open('r',encoding='utf-8')))[1:]}
                if not (old_result.event_sha256==new_result.event_sha256 and
                        a.read_bytes()==b.read_bytes() and actual==reference):
                    raise AssertionError(f'v0.4 mismatch {game}/{name} chunk={cb}')
                checks+=1
    print(f'Q3 v0.4 REGRESSION PASS: streaming oracle/v0.3 byte-identical comparisons={checks}')
    return checks


def run_all():
    self_test()
    count=0
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q4_SYNTHETIC_ONLY_') as td:
        root=Path(td)
        # The temporary directory is already made by TemporaryDirectory.
        (root/'SYNTHETIC_FIXTURE_MARKER').write_bytes(GUARD.MAGIC)
        for rel in ('fixture_digits','fixture_histories','fixture_results_real','fixture_results_null'):
            (root/rel).mkdir()
        profiles=check_first_class_guards(root)
        count+=8 # duplicate run + type refusal for each of four case pairs
        for p,run_id in profiles:
            check=lambda p=p,run_id=run_id:GUARD.load_verified_fixture(
                p,run_id,require_type=p.run_type)
            # Source and outcome provenance must reject modification.
            count+=_alter(p.draws_file,lambda b:b+b'\n',check,'changed drawset SHA')
            count+=_modify_json(p.receipt,lambda obj:obj.__setitem__('format','INVALID'),
                                check,'modified receipt')
            event=p.result_root/run_id/'raw_events.csv'
            count+=_alter(event,lambda b:b+b'X',check,'event SHA')
            manifest=p.result_root/run_id/'run_manifest.json'
            count+=_modify_json(manifest,lambda obj:obj.__setitem__('run_type','TEST_UNTRUSTED'),
                                check,'manifest type tampering')
            count+=_modify_json(manifest,lambda obj:obj.__setitem__('event_sha256','0'*64),
                                check,'manifest event digest tampering')
            count+=_malformed_events_and_resealed_manifest(p,run_id,kind='duplicate')
            count+=_malformed_events_and_resealed_manifest(p,run_id,kind='order')
            count+=_malformed_events_and_resealed_manifest(p,run_id,kind='EOF')
            count+=_malformed_events_and_resealed_manifest(p,run_id,
                          kind='NULL_as_REAL' if p.run_type=='TEST_REAL' else 'REAL_as_NULL')
            # A separate filename cannot redirect a fixed profile to another game.
            count+=fail_expected('invalid fixed game',lambda p=p:GUARD.FixtureProfile(
                       p.root,'invalid',p.run_type,'phi',1,4).checked())
        # Deliberately interrupted after scan: cannot be replayed as completed.
        p=profiles[0][0]
        count+=fail_expected('deliberate incomplete run',lambda:GUARD.run_fixture(
            p,'TEST_INTERRUPTED',inject_failure_after_scan=True))
        count+=fail_expected('reject incomplete',lambda:GUARD.load_verified_fixture(
            p,'TEST_INTERRUPTED',require_type='TEST_REAL'),'incomplete')
        # Missing receipt (no result directory created) and invalid declaration.
        receipt_bytes=p.receipt.read_bytes()
        p.receipt.unlink()
        try:
            count+=fail_expected('missing receipt preflight',lambda:GUARD.run_fixture(p,'TEST_NO_RECEIPT'))
            assert not (p.result_root/'TEST_NO_RECEIPT').exists()
        finally:
            p.receipt.write_bytes(receipt_bytes)
        count+=fail_expected('production type prohibited',lambda:GUARD.FixtureProfile(
            p.root,p.game,'REAL','phi',1,4).checked())
        count+=fail_expected('path escape prohibited',lambda:GUARD.run_fixture(p,'TEST_../escape'))
        # Prove replay does NOT reread the packed binary after sealing, even if
        # physically unavailable: it is a pure event+history provenance phase.
        p.packed.unlink()
        assert GUARD.load_verified_fixture(p,profiles[0][1],require_type='TEST_REAL')
        print('PASS: event/drawset/receipt/manifest tampering, cross-type, interrupted run, path guards')
        # Version-compatibility regression against v0.3 and independent oracle.
        comparisons=q3_v04_regression(root)
    print(f'Q4 FIXTURE GUARDS PASS: isolated-scope-runs=4 guard-refusals={count} '
          f'v0.4-oracle-regressions={comparisons}; stable 4MB default, 8MB override; '
          'sealed synthetic receipts/manifest, REAL-vs-NULL analogue isolation; '
          'NO PRODUCTION ENTRY POINT / NO REAL DATA / Q5 NOT AUTHORISED')


def main():
    a=argparse.ArgumentParser(description=__doc__)
    g=a.add_mutually_exclusive_group(required=True)
    g.add_argument('--self-test',action='store_true')
    g.add_argument('--run',action='store_true')
    args=a.parse_args()
    if args.self_test:self_test()
    else:run_all()

if __name__=='__main__':main()
