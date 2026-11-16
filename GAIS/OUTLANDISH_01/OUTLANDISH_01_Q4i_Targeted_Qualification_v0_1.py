#!/usr/bin/env python3
"""Q4i targeted synthetic checks ONLY; no published G: inputs or real history.

This deliberately does NOT duplicate Claude's 433-draw independent test:
REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_1.py --run
Rerun that existing script separately after installing this overlay.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4c_Synthetic_Processing_Qualification_v0_1 as F
import OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1 as Old
import OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1 as P
import OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1 as R
import OUTLANDISH_01_Q4h_Events_v0_1 as E
import OUTLANDISH_01_Q4i_Mode_v0_1 as M
import OUTLANDISH_01_Q4i_Production_Entry_v0_1 as Entry


def refuses(label, func, errors=(ValueError, RuntimeError, PermissionError,
                                   FileNotFoundError, FileExistsError, TypeError)):
    try:
        func()
    except errors:
        return 1
    raise AssertionError('missing required refusal: ' + label)


def test_modes(roots, profile, digits):
    m = M.PowerballMode.synthetic(roots,profile,digits)
    assert m.checked() is m and m.run_type == 'TEST_REAL'
    assert Entry.ENABLE_Q5_PRODUCTION_SCANS is False, 'OWNER SAFETY STOP: test needs switch OFF'
    checks = 0
    forged=replace(m,run_type='REAL')
    checks += refuses('synthetic cannot claim REAL', forged.checked)
    original_mode_check=M.PowerballMode.checked
    try:
        M.PowerballMode.checked=lambda self:self  # negative canary: one guard temporarily disabled
        assert forged.checked() is forged
    finally:
        M.PowerballMode.checked=original_mode_check
    checks += refuses('synthetic cannot substitute output root',
                     lambda: roots.run_location('REAL','REAL_forged'))
    checks += refuses('synthetic cannot relabel Oz as Powerball',
                     lambda: replace(m,profile=Old._historical_profile(roots,'oz')).checked())
    checks += refuses('production switch checked even on direct runner call',
                     lambda: P._require_scan_permission(SimpleNamespace(
                         checked=lambda: None, roots=SimpleNamespace(synthetic=False))))
    # No construction of a REAL mode is needed for the above test. A production
    # mode can be created for read-only inspection with switch OFF on Windows;
    # starting a genuine scan must remain blocked by P._require_scan_permission.
    label,seed=R.primary_seed('powerball','pi')
    assert label=='OUTLANDISH_01|powerball|pi|PRIMARY_W_TO_W1|V1'
    assert seed == int.from_bytes(hashlib.sha256(label.encode('ascii')).digest()[:8], 'big')
    assert 0 <= seed < 2**64 and R.primary_seed('powerball','phi')[1]!=seed
    assert R.PERMUTATIONS == 10_000
    assert R._close(1,1) and not R._close(1,2)
    assert R._close(0.5,0.5+1e-12)
    return checks


def test_history_sha_canary(roots,profile):
    saved=profile.source.read_bytes()
    original=G.validate_drawset
    original_sha=hashlib.sha256(saved).hexdigest()
    changed=saved.replace(b'2026-01-01',b'2026-01-02',1)
    assert changed != saved
    try:
        profile.source.write_bytes(changed)
        refuses('history mutation must fail digest',lambda:original(profile,expected_sha256=original_sha))
        try:
            G.validate_drawset=lambda p,expected_sha256=None:original(p)
            assert G.validate_drawset(profile,expected_sha256=original_sha).sha256 != original_sha
        finally:
            G.validate_drawset=original
    finally:
        profile.source.write_bytes(saved)
    return 1


def test_unsampled_corruption(roots, profile):
    # 150,000 bytes > 12*4096; some physical bytes are NOT preflight-sampled.
    source = roots.published_binary('phi')
    tiny = source.read_bytes()
    total_bytes=150_000
    binary=tiny + bytes([0x99])*(total_bytes-len(tiny))
    source.write_bytes(binary)
    n=total_bytes*2
    plan=G.sample_plan(total_bytes)
    covered=bytearray(total_bytes)
    for start,length in plan:
        covered[start:start+length]=b'\x01'*length
    missed=next((i for i in range(len(tiny),total_bytes) if covered[i]==0),None)
    if missed is None:
        raise AssertionError('large fixture has no unsampled byte')
    record={'format':G.FORMAT,'format_version':1,'scope':G.SCOPE,
            'constant':'phi','binary_name':source.name,
            'digits_including_integer':n,'packed_bytes':total_bytes,
            'binary_sha256_streamed':hashlib.sha256(binary).hexdigest(),
            'sample_block_length':plan[0][1],
            'samples':[{'offset_bytes':s,'size':length,
                        'sha256':hashlib.sha256(binary[s:s+length]).hexdigest()}
                       for s,length in plan]}
    roots.receipt('phi').write_text(json.dumps(record,sort_keys=True)+'\n',encoding='utf-8')
    m=M.PowerballMode.synthetic(roots,profile,n)
    assert G.validate_published_source(roots,'phi',fixture_digits=n).packed_sha256==record['binary_sha256_streamed']
    altered=bytearray(binary)
    altered[missed]=0x98 if altered[missed]!=0x98 else 0x97  # decimal BCD, avoids parse rejection
    source.write_bytes(altered)
    # All sampled blocks remain identical, deliberately ruling out sample preflight.
    assert G.validate_published_source(roots,'phi',fixture_digits=n).packed_sha256==record['binary_sha256_streamed']
    rid='TEST_REAL_q4i_unsampled_digest'
    count=refuses('unsampled corruption caught by full scanner digest',
                  lambda:P.run_powerball(m,'phi',rid,chunk_bytes=4096))
    run=roots.run_location('TEST_REAL',rid)
    assert json.loads((run/'run_manifest.json').read_text('utf-8'))['status']=='INCOMPLETE'
    assert not (run/'raw_events.csv').exists(), 'failed scan left a falsely usable event CSV'
    # Negative canary: disable BOTH logical full-stream comparisons (the scanner
    # expected digest and the postscan CheckedSource check) in this synthetic
    # environment. The corrupted input would then be wrongly marked COMPLETE.
    # Restore both functions immediately; no production root or input involved.
    import OUTLANDISH_01_Q3_Packed_Matcher_v0_4 as Engine
    original_scan=Engine.scan_packed_stream
    original_final=G.CheckedSource.check_completed_stream
    def unverified_scan(*args,**kwargs):
        kwargs['expected_full_sha256']=None
        return original_scan(*args,**kwargs)
    try:
        Engine.scan_packed_stream=unverified_scan
        G.CheckedSource.check_completed_stream=lambda self,*args:None
        canary_id='TEST_REAL_q4i_digest_disabled_canary'
        P.run_powerball(m,'phi',canary_id,chunk_bytes=4096)
        assert json.loads((roots.run_location('TEST_REAL',canary_id)/'run_manifest.json').read_text())['status']=='COMPLETE'
    finally:
        Engine.scan_packed_stream=original_scan
        G.CheckedSource.check_completed_stream=original_final
    return count, total_bytes, missed


def test_duplicate_replay(roots, profile, digits):
    # One run, then change the saved CSV and its manifest checksums and counts.
    m=M.PowerballMode.synthetic(roots,profile,digits)
    rid='TEST_REAL_q4i_duplicate'
    folder=P.run_powerball(m,'phi',rid,chunk_bytes=9)
    raw=(folder/'raw_events.csv').read_bytes()
    rows=raw.splitlines(keepends=True)
    assert len(rows)>1, 'fixture needs at least one event'
    duplicated=b''.join([rows[0],rows[1],rows[1],*rows[2:]])
    (folder/'raw_events.csv').write_bytes(duplicated)
    meta=json.loads((folder/'run_manifest.json').read_text('utf-8'))
    meta['event_sha256']=hashlib.sha256(duplicated).hexdigest()
    meta['event_count']+=1
    fam=rows[1].decode('utf-8').split(',')[1]
    meta['family_counts'][fam]+=1
    (folder/'run_manifest.json').write_bytes(P.encode(meta))
    count=refuses('classifier rejects duplicate despite updated digests/totals',
                  lambda:P.load_run(m,'phi',rid))
    # Targeted local canary: replacement of the semantic verifier would make
    # the duplicate input unreadably *accepted*. Restore immediately.
    original=E.read_and_classify
    def unverified(raw,*,recorded_sha256,history,digits):
        from OUTLANDISH_01_Q3_Event_Classifier_v0_1 import RawEvent
        import csv,io
        lines=list(csv.reader(io.StringIO(raw.decode('utf-8')),strict=True))[1:]
        return tuple(RawEvent(int(d),fam,int(off),md) for d,fam,off,md in lines),()
    try:
        E.read_and_classify=unverified
        # This intentional negative control is never shipped as a production path.
        loaded=P.load_run(m,'phi',rid)
        assert len(loaded[3]) == meta['event_count']
    finally:
        E.read_and_classify=original
    return count,1


def main():
    parser=argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--self-test',action='store_true')
    g.add_argument('--run',action='store_true')
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q4I_SYNTHETIC_') as td:
        roots,n=F.make_temp(Path(td))
        profile=Old._historical_profile(roots,'powerball')
        refusals=test_modes(roots,profile,n)
        if args.run:
            # Duplicate replay on the ORIGINAL small fixture, then large fixture
            # replaces only the isolated phi source for the unsampled hash test.
            duplicates, canaries=test_duplicate_replay(roots,profile,n)
            canaries+=test_history_sha_canary(roots,profile)
            refuse_large,size,missed=test_unsampled_corruption(roots,profile)
            canaries+=1  # verified negative control: full digest disabled accepts corruption
            canaries+=1  # verified negative control: mode identity disabled accepts forged mode
            refusals+=duplicates+refuse_large
        else:
            canaries=0
            size=missed=0
    print(f'Q4I SYNTHETIC {"TARGETED" if args.run else "GUARDS"} PASS: '
          f'refusals={refusals} canaries={canaries} '
          f'unsampled-fixture-bytes={size} unsampled-offset={missed} '
          'Q5-switch=OFF production-scans=0 REAL-history-reads=0')


if __name__=='__main__':
    main()
