#!/usr/bin/env python3
"""Q3 v0.3 streaming/automatic-RAM-chunk fixture-only qualification.

Run --self-test or --run from repository root using project Python. --run
reuses all prior Q3 Powerball+Oz qualification, then independently compares
new streamed output to the Q2 oracle and the earlier v0.2 in-memory CSV.
Creates temporary synthetic packed files ONLY; no G:, REAL, receipts, registry.
NOT a REAL/NULL entry point or Q5 authorisation.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
from pathlib import Path
import random
import tempfile

from OUTLANDISH_01_Q2_Independent_Oracle_v0_1 import (
    oracle, encoded, plant, pack_independent,
)
from OUTLANDISH_01_Q2_LegacyScanner_Comparison_v0_1 import DRAWS as PB_DRAWS, D1, D2, D3, scenario_set
import OUTLANDISH_01_Q3_Powerball_Qualification_v0_1 as pb_qual
import OUTLANDISH_01_Q3_Shared_Qualification_v0_2 as oz_qual
import OUTLANDISH_01_Q3_Packed_Matcher_v0_2 as predecessor
import OUTLANDISH_01_Q3_Packed_Matcher_v0_3 as current
from OUTLANDISH_01_Q3_Event_Interface_Smoke_v0_1 import read_events

HERE = Path(__file__).resolve().parent
ORACLE_SHA = '6ea5562ed681c854f8c552e9600af5d8f9d3be00'


def _tuple_set(hits):
    return {(x.draw_number,x.family,x.start_digit_offset,x.matched_digits) for x in hits}


def _reference_hits(game, text, draws):
    ref = oracle(game,text, list(draws))
    expected = {(x.draw,x.family,x.start,x.digits) for x in ref}
    if len(ref) != len(expected):
        raise AssertionError('independent oracle duplicate identity')
    return expected


def _records(game, draws):
    if game == 'powerball':
        return [current.PBRecord(x.number,x.mains,x.pb) for x in draws]
    return [current.OzRecord(x.number,x.mains,x.supp) for x in draws]


def _check_case(label, game, text, draws, effective, root, chunks=(1,3,7,16,64)):
    if not 1 <= effective <= len(text) <= 4000:
        raise AssertionError('bad fixture boundaries')
    packed = pack_independent(text)
    path = root / (label + '.SYNTHETIC_TEST_ONLY.packed.bin')
    path.write_bytes(packed)
    actual_digest = hashlib.sha256(packed).hexdigest()
    oracle_expected = _reference_hits(game,text[:effective], draws)
    records = _records(game, draws)
    oldrecords = ([predecessor.PBRecord(x.number,x.mains,x.pb) for x in draws]
                  if game == 'powerball' else
                  [predecessor.OzRecord(x.number,x.mains,x.supp) for x in draws])
    scan_mem = current.scan_packed if game == 'powerball' else current.scan_packed_oz
    scan_stream = current.scan_packed_stream if game == 'powerball' else current.scan_packed_oz_stream
    oldscan = predecessor.scan_packed if game == 'powerball' else predecessor.scan_packed_oz
    for chunk in chunks:
        args = dict(physical_digits=len(text), effective_digits=effective,
                    chunk_bytes=chunk, expected_full_sha256=actual_digest)
        old = oldscan(path, draws=oldrecords, **args)
        mem = scan_mem(path, draws=records, **args)
        if (_tuple_set(mem.events) != oracle_expected or
                _tuple_set(old.events) != oracle_expected or
                mem.events != tuple(current.RawEvent(*vars(x).values()) for x in old.events)):
            raise AssertionError(f'{game}/{label} chunk={chunk}: in-memory or v0.2 mismatch')
        baseline = root / f'{game}.{label}.{chunk}.baseline.csv'
        old_sha = predecessor.write_fixture_events_create_only(baseline, old.events)
        output = root / f'{game}.{label}.{chunk}.streamed.csv'
        result = scan_stream(path, draws=records, output_csv=output, **args)
        if (result.event_count != len(old.events) or result.event_sha256 != old_sha
                or baseline.read_bytes() != output.read_bytes()
                or result.bytes_hashed != len(packed)
                or result.sha256_full_packed != actual_digest
                or sum(result.family_counts.values()) != len(old.events)):
            raise AssertionError(f'{game}/{label} chunk={chunk}: streamed bytes/hash/count mismatch')
        loaded = read_events(output.read_bytes(), game=game, logical_N=effective,
                             allowed_draws={x.number for x in draws},
                             recorded_sha256=result.event_sha256)
        if {(e.draw_number,e.family,e.start_digit_offset,e.matched_digits)
                for e in loaded} != oracle_expected:
            raise AssertionError(f'{game}/{label} chunk={chunk}: streamed CSV oracle mismatch')
        # Create-only guarantee and no overwrite of accepted result.
        try:
            scan_stream(path, draws=records, output_csv=output, **args)
        except FileExistsError:
            pass
        else:
            raise AssertionError('existing streamed output incorrectly overwritten')
    print(f'PASS: {game}/{label}: {len(oracle_expected)} oracle events, '
          f'{len(chunks)} chunk choices, exact streamed bytes and SHA')
    return len(chunks)


def policy_self_test():
    small,large = current.AUTO_SMALL_CHUNK_BYTES,current.AUTO_LARGE_CHUNK_BYTES
    g = current.GIB
    table = [
        ((16*g, 8*g), small),
        ((17*g, 8*g), small),
        ((17*g+1, 8*g), large),
        ((32*g, 3*g), small),
        ((32*g, 4*g), large),
        ((32*g, 8*g), large),
    ]
    for mem, expected in table:
        assert current.resolve_chunk_bytes(None, memory=mem) == expected
    assert current.resolve_chunk_bytes(3, memory=(16*g,8*g)) == 3
    assert current.resolve_chunk_bytes(large, memory=(16*g,8*g)) == large
    for wrong in (0,-1,True,current.MAX_CHUNK_BYTES+1,1.5):
        try:
            current.resolve_chunk_bytes(wrong)
        except ValueError:
            pass
        else:
            raise AssertionError(f'chunk override wrongly accepted: {wrong!r}')
    assert current.resolve_chunk_bytes(None,memory=None) in (small,large)
    print('RAM CHUNK POLICY PASS: 4MB <=17GiB/low-free, 8MB >17GiB with >=4GiB free; explicit override')


def self_test():
    if not __debug__:
        raise RuntimeError('Do not run with Python -O; assertion tests are required')
    source = (HERE / 'OUTLANDISH_01_Q2_Independent_Oracle_v0_1.py').read_bytes().replace(b'\r\n',b'\n')
    actual_sha = hashlib.sha1(f'blob {len(source)}\0'.encode() + source).hexdigest()
    if actual_sha != ORACLE_SHA:
        raise ValueError('independent Q2 oracle unexpectedly changed')
    policy_self_test()
    memory = current._memory_snapshot()
    if memory is None:
        print('HOST RAM PROBE: unavailable; conservative 4 MB packed chunk selected')
    else:
        total,free=memory
        print(f'HOST RAM: installed={total / current.GIB:.2f} GiB, '
              f'currently-available={free / current.GIB:.2f} GiB, '
              f'auto-chunk={current.resolve_chunk_bytes() // 1_000_000} MB packed')
    print('Q3 STREAM SELF-TEST PASS: independent oracle pinned; original v0.2 retained; '
          'no synthetic scan or REAL input accessed')


def check_failure_cleanup(root):
    text = plant(57,[(41,encoded(*D1.mains,D1.pb))])
    packed = pack_independent(text)
    path = root/'intentional_failure.SYNTHETIC_TEST_ONLY.packed.bin'
    path.write_bytes(packed)
    output = root/'intentional_failure.csv'
    try:
        current.scan_packed_stream(path, physical_digits=len(text),effective_digits=len(text),
                     draws=_records('powerball',[D1]), output_csv=output,
                     chunk_bytes=3, expected_full_sha256='0'*64)
    except ValueError as e:
        if 'SHA-256 mismatch' not in str(e):
            raise AssertionError(f'wrong error from SHA canary: {e}')
    else:
        raise AssertionError('corrupt SHA did not refuse stream')
    if output.exists():
        raise AssertionError('incomplete streaming file left behind after SHA refusal')
    print('PASS: bad full-input SHA refused and incomplete CSV removed')


def run():
    self_test()
    # Replay all PB+Oz qualification cases against the v0.3 module, not v0.2.
    saved = (oz_qual.scan_packed,oz_qual.PBRecord,oz_qual.scan_packed_oz,oz_qual.OzRecord)
    try:
        oz_qual.scan_packed = current.scan_packed
        oz_qual.PBRecord = current.PBRecord
        oz_qual.scan_packed_oz = current.scan_packed_oz
        oz_qual.OzRecord = current.OzRecord
        oz_qual.run_all()
    finally:
        oz_qual.scan_packed,oz_qual.PBRecord,oz_qual.scan_packed_oz,oz_qual.OzRecord = saved
    cases=chunks=0
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q3_STREAM_TEST_ONLY_') as td:
        root=Path(td)
        for s in scenario_set():
            n=s.prefix_digits if s.prefix_digits is not None else len(s.digits)
            chunks += _check_case('pb_'+s.name,'powerball',s.digits,PB_DRAWS,n,root)
            cases+=1
        pb_cases=[
            ('zero_P1',plant(57,[(0,encoded(*D1.mains,D1.pb))]),[D1],57),
            ('odd_P1',plant(57,[(1,encoded(*D1.mains,D1.pb))]),[D1],57),
            ('EOF_P1',plant(57,[(41,encoded(*D1.mains,D1.pb))]),[D1],57),
            ('EOF_P2',plant(57,[(43,encoded(*D2.mains))]),[D2],57),
            ('EOF_P3',plant(57,[(43,encoded(2,4,6,8,12,14,18))]),[D3],57),
            ('short_P1',plant(57,[(41,encoded(*D1.mains,D1.pb))]),[D1],55),
        ]
        for label, digits, draws, n in pb_cases:
            chunks+=_check_case('pb_'+label,'powerball',digits,draws,n,root)
            cases+=1
        rng=random.Random(20261114)
        pats=[encoded(*D1.mains,D1.pb),encoded(*D2.mains),encoded(2,4,6,8,12,14,18)]
        for j in range(10):
            n=189+j*37; digits=[str(rng.randrange(10)) for _ in range(n)]
            start=30+(j*17)%65; pat=pats[j%3];digits[start:start+len(pat)]=pat
            chunks+=_check_case(f'pb_seeded{j:02d}','powerball',''.join(digits),PB_DRAWS,
                                n-(j%5),root,chunks=(3,17,64))
            cases+=1
        for label, digits, draws, effective, mandatory in oz_qual.scenarios():
            chunks+=_check_case('oz_'+label,'oz',digits,draws,effective,root)
            cases+=1
        rng=random.Random(20261114)
        patterns=[encoded(*oz_qual.O1.mains),encoded(*oz_qual.O2.mains[:6],oz_qual.O2.supp[0]),
                  encoded(*oz_qual.O3.mains[:6])]
        for j in range(10):
            n=190+31*j;digits=[str(rng.randrange(10)) for _ in range(n)]
            start=17+(j*13)%45;pat=patterns[j%3];digits[start:start+len(pat)]=pat
            chunks+=_check_case(f'oz_seeded{j:02d}','oz',''.join(digits),oz_qual.DRAWS,
                                n-(j%7),root,chunks=(3,17,64))
            cases+=1
        check_failure_cleanup(root)
    print(f'Q3 STREAMING PASS: fixtures={cases} streamed-comparisons={chunks}; '
          'PB/Oz v0.3 exact independent-oracle tuples and v0.2 byte-identical CSV, '
          'whole-source SHA, incremental CSV digest, create-only and failure cleanup; '
          'RAM 4/8MB automatic + override. SYNTHETIC ONLY; Q5 NOT AUTHORISED')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--self-test',action='store_true')
    g.add_argument('--run',action='store_true')
    args=p.parse_args()
    if args.self_test:
        self_test()
    else:
        run()

if __name__ == '__main__':
    main()
