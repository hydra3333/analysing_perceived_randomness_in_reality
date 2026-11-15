#!/usr/bin/env python3
"""Synthetic Q4c processing qualification (stdlib preflight or full Q3 integration).

Only creates marked TemporaryDirectory contents. No G: reads, no REAL science,
no Q5 entry point. Full --run requires the existing Q3 v0.4 and classifier.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import tempfile

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1 as P


def refuses(label, fn):
    try:
        fn()
    except (ValueError, FileExistsError, RuntimeError, TypeError):
        return 1
    raise AssertionError(f'FAIL: expected refusal: {label}')


def altered(path, new: bytes, fn, label):
    old=path.read_bytes()
    if old==new:
        raise AssertionError(f'{label}: bad mutation setup')
    try:
        path.write_bytes(new)
        return refuses(label, fn)
    finally:
        path.write_bytes(old)


def csv_bytes(header, rows):
    stream=io.StringIO(newline='')
    writer=csv.writer(stream,lineterminator='\n')
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue().encode('utf-8')


def make_temp(root: Path):
    base=root/'OUTLANDISH_Q4_SOURCE_SYNTHETIC_ONLY_c01'
    base.mkdir()
    (base/'SYNTHETIC_MARKER').write_bytes(G.MAGIC)
    for name in ('digits','histories','results','results_null'):
        (base/name).mkdir()
    roots=G.FixedRoots.test_sandbox(base)
    n=10_001
    digits=bytearray(b'9'*n)
    def plant(offset, vals):
        encoded=''.join(f'{v:02d}' for v in vals).encode('ascii')
        digits[offset:offset+len(encoded)]=encoded

    pb=[(11,'2026-01-01',1,2,3,4,5,6,7,1),
        (12,'2026-01-08',8,9,10,11,12,13,14,20),
        (13,'2026-01-15',15,16,17,18,19,20,21,3)]
    oz=[(21,'2026-01-01',1,2,3,4,5,6,7,8,9,10),
        (22,'2026-01-08',11,12,13,14,15,16,17,18,19,20),
        (23,'2026-01-15',21,22,23,24,25,26,27,28,29,30)]
    (roots.base/'histories/powerball_synthetic.csv').write_bytes(csv_bytes(G.PB_HEADER,pb))
    (roots.base/'histories/oz_synthetic.csv').write_bytes(csv_bytes(G.SYNTHETIC_OZ_HEADER,oz))
    # Separate, non-overlapping physical substrings for game and type checks.
    plant(13, (1,2,3,4,5,6,7,1))  # PB K7S
    plant(101,(1,2,3,4,5,6,7))   # PB K7 & Oz K7
    plant(201,(1,2,3,4,5,6,8))   # Oz K7mix
    pb_decoy, pb_index=P.generate_decoy_draws('powerball',seed=7777,k=2)
    oz_decoy, oz_index=P.generate_decoy_draws('oz',seed=8888,k=2)
    plant(401,pb_index[0][2][:7])  # independently generated PB NULL K7
    plant(501,oz_index[0][2][:7])  # independently generated Oz NULL K7
    binary=bytes.fromhex((bytes(digits)+b'0').decode('ascii'))
    path=roots.published_binary('phi')
    path.write_bytes(binary)
    plan=G.sample_plan(len(binary))
    receipt={'format':G.FORMAT,'format_version':1,'scope':G.SCOPE,
             'constant':'phi','binary_name':path.name,
             'digits_including_integer':n,'packed_bytes':len(binary),
             'binary_sha256_streamed':hashlib.sha256(binary).hexdigest(),
             'sample_block_length':plan[0][1],
             'samples':[{'offset_bytes':start,'size':length,
                         'sha256':hashlib.sha256(binary[start:start+length]).hexdigest()}
                        for start,length in plan]}
    roots.receipt('phi').write_text(json.dumps(receipt,sort_keys=True)+'\n',encoding='utf-8')
    return roots, n


def guard_only(roots):
    n=0
    a, b=P.generate_decoy_draws('powerball',seed=7777,k=2)
    assert b==P._read_decoys(a,game='powerball',k=2)
    assert P.generate_decoy_draws('powerball',seed=7777,k=2)[0]==a
    c, d=P.generate_decoy_draws('oz',seed=8888,k=2)
    assert d==P._read_decoys(c,game='oz',k=2)
    assert a!=c and len(b)==len(d)==6
    assert all(label.startswith('DECOY-') for _,label,_ in b)
    assert len({label for _,label,_ in b})==6
    n+=refuses('bad nullable seed',lambda:P.generate_decoy_draws('oz',seed=True,k=2))
    n+=refuses('missing K',lambda:P.generate_decoy_draws('powerball',seed=1,k=0))
    n+=refuses('excess K',lambda:P.generate_decoy_draws('powerball',seed=1,k=9))
    n+=refuses('wrong version schema',lambda:P._read_decoys(a,game='oz',k=2))
    n+=refuses('truncated history',lambda:P._read_decoys(a[:-10],game='powerball',k=2))
    n+=refuses('wrong K when decoding',lambda:P._read_decoys(a,game='powerball',k=1))
    n+=refuses('bad decoy text label',lambda:P._read_decoys(a.replace(b'DECOY-0001-0001',b'001'),game='powerball',k=2))
    n+=refuses('nonnumeric decoy outcome',lambda:P._read_decoys(a.replace(b',',b',X',1),game='powerball',k=2))
    n+=refuses('production root into Q4c',lambda:P._check_test_root(G.FixedRoots(roots.base,False)))
    n+=refuses('invalid run name',lambda:roots.run_location('TEST_REAL','TEST_NULL_cross'))
    assert G.validate_published_source(roots,'phi',fixture_digits=10_001).digits==10_001
    assert G.validate_drawset(P._historical_profile(roots,'powerball')).draw_count==3
    assert G.validate_drawset(P._historical_profile(roots,'oz')).draw_count==3
    return n


def full_run(roots,n):
    count=0
    pairs=[('powerball','TEST_REAL',None,1),
           ('powerball','TEST_NULL',7777,2),
           ('oz','TEST_REAL',None,1),
           ('oz','TEST_NULL',8888,2)]
    run_paths=[]
    for i,(game,kind,seed,k) in enumerate(pairs,1):
        ident=f'{kind}_q4c_{game}_{i}'
        folder=P.run_synthetic(roots,game,'phi',kind,ident,
                              fixture_digits=n,seed=seed,k=k,chunk_bytes=9)
        events=P.load_verified_synthetic_run(roots,game,'phi',kind,ident)
        manifest=json.loads((folder/'run_manifest.json').read_bytes())
        assert manifest['status']=='COMPLETE' and len(events)==manifest['event_count']
        assert manifest['bytes_hashed']==5001
        assert manifest['event_count']>0, f'{game}/{kind}: fixture expected positive match'
        if kind=='TEST_NULL':
            assert (folder/'decoy_histories.csv').is_file()
            assert b'DECOY-' in (folder/'raw_events.csv').read_bytes()
        else:
            assert not (folder/'decoy_histories.csv').exists()
            assert b'DECOY-' not in (folder/'raw_events.csv').read_bytes()
        run_paths.append((game,kind,ident,folder))
        count+=refuses('create-only run refusal',lambda:P.run_synthetic(
            roots,game,'phi',kind,ident,fixture_digits=n,seed=seed,k=k))
    # Replay must NOT require packed binary to exist or be opened.
    source=roots.published_binary('phi')
    absent=source.with_name(source.name+'.temporarily_absent')
    source.rename(absent)
    try:
        for game,kind,ident,_ in run_paths:
            P.load_verified_synthetic_run(roots,game,'phi',kind,ident)
    finally:
        absent.rename(source)
    game,kind,ident,folder=run_paths[0]
    good=lambda:P.load_verified_synthetic_run(roots,game,'phi',kind,ident)
    record=folder/'raw_events.csv'
    count+=altered(record,record.read_bytes()+b'bad\n',good,'tampered REAL events')
    history=roots.base/'histories/powerball_synthetic.csv'
    count+=altered(history,history.read_bytes()+b'\n',good,'changed REAL history')
    receipt=roots.receipt('phi')
    count+=altered(receipt,receipt.read_bytes()+b' ',good,'changed receipt')
    manifest=folder/'run_manifest.json'
    md=json.loads(manifest.read_bytes())
    md['run_type']='TEST_NULL'
    count+=altered(manifest,(json.dumps(md)+'\n').encode(),good,'cross-type manifest spoof')
    game,kind,ident,folder=run_paths[1]
    good=lambda:P.load_verified_synthetic_run(roots,game,'phi',kind,ident)
    source=folder/'decoy_histories.csv'
    count+=altered(source,source.read_bytes()+b'\n',good,'modified decoy bytes')
    source=folder/'raw_events.csv'
    count+=altered(source,source.read_bytes().replace(b'DECOY-',b'REAL--'),good,'typed decoy tamper')
    count+=refuses('wrong NULL/REAL replay',lambda:P.load_verified_synthetic_run(
        roots,game,'phi','TEST_REAL',ident))
    count+=refuses('no REAL parameters on TEST_REAL',lambda:P.run_synthetic(
        roots,'oz','phi','TEST_REAL','TEST_REAL_badparams',fixture_digits=n,seed=99))
    count+=refuses('no missing seed on TEST_NULL',lambda:P.run_synthetic(
        roots,'oz','phi','TEST_NULL','TEST_NULL_missingseed',fixture_digits=n))
    count+=refuses('unknown run type',lambda:P.run_synthetic(
        roots,'powerball','phi','REAL','REAL_illegal',fixture_digits=n))
    # Injected post-scan error: manifest remains INCOMPLETE and not replayable.
    ident='TEST_REAL_forced_failure'
    count+=refuses('injected post-scan failure',lambda:P.run_synthetic(
        roots,'powerball','phi','TEST_REAL',ident,
        fixture_digits=n,fail_after_scan=True,chunk_bytes=13))
    failed=roots.run_location('TEST_REAL',ident)
    assert json.loads((failed/'run_manifest.json').read_text())['status']=='INCOMPLETE'
    count+=refuses('INCOMPLETE replay not reportable',lambda:P.load_verified_synthetic_run(
        roots,'powerball','phi','TEST_REAL',ident))
    return count,len(run_paths)


def main():
    p=argparse.ArgumentParser(description='Q4c temporary synthetic run qualification')
    p.add_argument('--self-test',action='store_true',help='stdlib guards only')
    p.add_argument('--run',action='store_true',help='full Q3 v0.4 synthetic integration')
    opt=p.parse_args()
    if opt.self_test==opt.run:
        p.error('choose exactly one test mode')
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q4C_ISOLATED_') as tmp:
        roots,n=make_temp(Path(tmp))
        basic=guard_only(roots)
        if opt.run:
            more,runs=full_run(roots,n)
        else:
            more,runs=0,0
    print(f'Q4C SYNTHETIC {"INTEGRATION" if opt.run else "GUARDS"} PASS: '
          f'isolated-runs={runs} guard-refusals={basic+more} '
          'production-scans=0 REAL-history-reads=0')


if __name__=='__main__':
    main()
