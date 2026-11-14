#!/usr/bin/env python3
"""Q3 shared-engine synthetic qualification: preserve PB, add Oz K7/K7mix/K6.

Fixture-only on Windows/Linux. Uses temp files only. NO REAL drawset/packed
constant, receipts, results, or registry access. The unchanged Q2 plain-string
oracle independently defines expected exact raw event tuples.

    python OUTLANDISH_01_Q3_Shared_Qualification_v0_2.py --self-test
    python OUTLANDISH_01_Q3_Shared_Qualification_v0_2.py --run

Not a production REAL/NULL entry point. No Q5 permission.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import random
import tempfile

from OUTLANDISH_01_Q2_Independent_Oracle_v0_1 import (
    OzDraw, oracle, encoded, plant, pack_independent,
)
from OUTLANDISH_01_Q3_Packed_Matcher_v0_2 import (
    OzRecord, PBRecord, scan_packed_oz, scan_packed, write_fixture_events_create_only,
)
from OUTLANDISH_01_Q3_Event_Interface_Smoke_v0_1 import read_events
import OUTLANDISH_01_Q3_Powerball_Qualification_v0_1 as pb_qualification

ORACLE_GIT_BLOB = '6ea5562ed681c854f8c552e9600af5d8f9d3be00'
HERE = Path(__file__).resolve().parent

# Deliberately invented draws; cannot coincide with REAL Oz draw number range.
O1 = OzDraw(7, (1,5,9,13,17,21,47), (2,4,6))
O2 = OzDraw(8, (3,7,11,15,19,23,35), (8,10,12))
O3 = OzDraw(9, (4,6,8,10,12,14,16), (1,3,5))
O4 = OzDraw(10, O1.mains, O1.supp)  # same legitimate keys, *different* draw attribution
O5 = OzDraw(11, (1,5,9,13,17,21,33), (47,2,4))
DRAWS = (O1, O2, O3, O4, O5)


def as_records(draws):
    return [OzRecord(x.number, x.mains, x.supp) for x in draws]


def as_tuples(events):
    actual = {(e.draw_number, e.family, e.start_digit_offset, e.matched_digits) for e in events}
    if len(actual) != len(events):
        raise AssertionError('duplicate raw events in engine output')
    return actual


def check_case(label: str, text: str, draws, effective: int, tmp: Path,
               chunks=(1,2,3,7,16,31,64), mandatory: set | None = None) -> int:
    if not 1 <= len(text) <= 6000 or not 1 <= effective <= len(text):
        raise AssertionError('fixture bounds incorrect')
    expected_hits = oracle('oz', text[:effective], list(draws))
    expected = {(h.draw,h.family,h.start,h.digits) for h in expected_hits}
    if len(expected) != len(expected_hits):
        raise AssertionError('reference duplicate output')
    if mandatory is not None and not mandatory.issubset(expected):
        raise AssertionError(f'{label}: planted oracle hits missing {sorted(mandatory-expected)[:10]}')
    path = tmp / f'{label}.SYNTHETIC_TEST_ONLY.packed.bin'
    blob = pack_independent(text)
    path.write_bytes(blob)
    digest = hashlib.sha256(blob).hexdigest()
    count = 0
    for chunk in chunks:
        result = scan_packed_oz(path, physical_digits=len(text), effective_digits=effective,
                                draws=as_records(draws), chunk_bytes=chunk,
                                expected_full_sha256=digest)
        actual = as_tuples(result.events)
        if actual != expected:
            raise AssertionError(f'{label} chunk={chunk}: missing={sorted(expected-actual)[:6]} '
                                 f'extra={sorted(actual-expected)[:6]}')
        if result.bytes_hashed != len(blob) or result.sha256_full_packed != digest:
            raise AssertionError(f'{label} chunk={chunk}: full-file byte hashing incorrect')
        csv_path = tmp / f'{label}.{chunk}.events.csv'
        event_sha = write_fixture_events_create_only(csv_path, result.events)
        loaded = read_events(csv_path.read_bytes(), game='oz', logical_N=effective,
                             allowed_draws={d.number for d in draws},
                             recorded_sha256=event_sha)
        if {(e.draw_number,e.family,e.start_digit_offset,e.matched_digits)
            for e in loaded} != expected:
            raise AssertionError(f'{label} chunk={chunk}: CSV mismatch')
        try:
            write_fixture_events_create_only(csv_path, result.events)
        except FileExistsError:
            pass
        else:
            raise AssertionError('create-only writer allowed overwriting evidence')
        count += 1
    families = {f: sum(h.family == f for h in expected_hits)
                for f in ('K7','K7mix','K6')}
    print(f'PASS: Oz {label}: {len(expected)} exact oracle events; chunks={count}; '
          f'K7/K7mix/K6={families["K7"]}/{families["K7mix"]}/{families["K6"]}')
    return count


def scenarios():
    # Two O1, seven O2 including every supplementary slot, and several O3.
    # O1 is also O2 for draw 11, verifying *different* families and draw roles
    # can share the exact same 14-digit starting window legitimately.
    pat_o1 = encoded(*O1.mains)
    pat_o2 = encoded(*O2.mains)
    pat_o3 = encoded(*O3.mains)
    basesix = list(O1.mains[:6])
    patches = [(13,pat_o1),(37,pat_o2),(61,pat_o3)]
    for slot in range(7):
        values = basesix.copy()
        values.insert(slot, O1.supp[0])
        patches.append((89+24*slot,encoded(*values)))
    patches += [(270,encoded(*O2.mains[:6])),
                (293,encoded(*O3.mains[:6])),
                (320,pat_o1)]
    primary = plant(389,patches)
    mandatory = {
        (7,'K7',13,pat_o1), (10,'K7',13,pat_o1),
        (11,'K7mix',13,pat_o1), (8,'K7',37,pat_o2),
        (9,'K7',61,pat_o3), (7,'K7',320,pat_o1),
        (7,'K6',13,encoded(*O1.mains[:6])),
        (7,'K6',15,encoded(*O1.mains[1:])),
    }
    for slot in range(7):
        values = basesix.copy()
        values.insert(slot, O1.supp[0])
        mandatory.add((7,'K7mix',89+24*slot,encoded(*values)))
    yield ('O1_O2_all_supp_slots_and_O3_multi_attribution',primary,DRAWS,len(primary),mandatory)
    # Family specific physical EOF where 12 digits still fit but 14 do not.
    last_k6 = encoded(*O1.mains[:6])
    yield ('K6_last_valid_odd_N',plant(57,[(45,last_k6)]),[O1],57,
           {(7,'K6',45,last_k6)})
    last_k7 = encoded(*O1.mains)
    yield ('K7_last_valid_even_N',plant(58,[(44,last_k7)]),[O1],58,
           {(7,'K7',44,last_k7)})
    last_mix = encoded(*O1.mains[:6], O1.supp[0])
    yield ('K7mix_last_valid_odd_N',plant(59,[(45,last_mix)]),[O1],59,
           {(7,'K7mix',45,last_mix)})
    yield ('K7_start_zero',plant(53,[(0,last_k7)]),[O1],53,
           {(7,'K7',0,last_k7)})
    yield ('K7_start_odd',plant(53,[(1,last_k7)]),[O1],53,
           {(7,'K7',1,last_k7)})
    # 59 physical digits, effective prefix 56: K7 at start45 needs end59
    # while K6 at 45 ends57. Both ineligible for effective N=56.
    yield ('K7mix_outside_effective_prefix',plant(59,[(45,last_mix)]),[O1],56,set())
    # K6 final valid start in prefix 56 is 44; 14-digit K7mix may be out.
    yield ('K6_eligible_K7mix_ineligible_prefix',plant(59,[(44,last_k6)]),[O1],56,
           {(7,'K6',44,last_k6)})
    # Two O3 hits at fixed locations, with no complete seventh valid field.
    text = plant(88, [(9, encoded(*O2.mains[:6])), (47,encoded(*O3.mains[:6]))])
    yield ('two_separate_O3',text,[O2,O3],88,
           {(8,'K6',9,encoded(*O2.mains[:6])),(9,'K6',47,encoded(*O3.mains[:6]))})
    # An invalid repeated seventh must not be accepted as O1/O2.
    text = plant(74,[(17,encoded(1,5,9,13,17,21,21))])
    yield ('repeated_seventh_not_eligible',text,[O1,O5],74,set())
    # Draws O1/O4 have duplicate match *keys*, not duplicate identities.
    text = plant(97,[(33,last_k7)])
    yield ('duplicate_keys_different_draws',text,[O1,O4],97,
           {(7,'K7',33,last_k7),(10,'K7',33,last_k7)})


def expect_error(label, thunk, contains):
    try:
        thunk()
    except (ValueError, FileExistsError) as ex:
        if contains not in str(ex):
            raise AssertionError(f'{label}: unexpected exception {ex}') from ex
        print(f'PASS: Oz refusal_{label}')
    else:
        raise AssertionError(f'{label}: expected refusal absent')


def negative_cases(tmp: Path) -> int:
    digits = plant(73,[(23,encoded(*O1.mains))])
    blob = pack_independent(digits)
    good = tmp/'good.SYNTHETIC_TEST_ONLY.packed.bin'
    good.write_bytes(blob)
    args = dict(physical_digits=len(digits),effective_digits=len(digits),
                draws=as_records([O1]),chunk_bytes=3)
    corrupt = tmp/'corrupt.SYNTHETIC_TEST_ONLY.packed.bin'
    b=bytearray(blob);b[9]=0xEA;corrupt.write_bytes(b)
    expect_error('invalid_BCD',lambda:scan_packed_oz(corrupt,**args),'nondecimal packed BCD')
    pad = tmp/'pad.SYNTHETIC_TEST_ONLY.packed.bin'
    b=bytearray(blob);b[-1]|=0x05;pad.write_bytes(b)
    expect_error('odd_pad',lambda:scan_packed_oz(pad,**args),'padding')
    truncated=tmp/'truncated.SYNTHETIC_TEST_ONLY.packed.bin'
    truncated.write_bytes(blob[:-1])
    expect_error('truncated',lambda:scan_packed_oz(truncated,**args),'size disagree')
    expect_error('bad_sha',lambda:scan_packed_oz(good,**args,
                      expected_full_sha256='0'*64),'SHA-256 mismatch')
    expect_error('bad_effective_N',lambda:scan_packed_oz(good,**(args|{
                       'effective_digits':len(digits)+1})),'effective digit count')
    expect_error('duplicate_draw_id',lambda:scan_packed_oz(good,**(args|{
                       'draws':as_records([O1,O4]) + as_records([O1])})),'duplicate draw')
    expect_error('same_barrel_overlap',lambda:scan_packed_oz(good,**(args|{
                       'draws':[OzRecord(7,O1.mains,(1,4,6))]})),'wrong Oz draw')
    expect_error('wrong_range',lambda:scan_packed_oz(good,**(args|{
                       'draws':[OzRecord(7,O1.mains,(48,4,6))]})),'wrong Oz draw')
    expect_error('bad_chunk',lambda:scan_packed_oz(good,**(args|{
                       'chunk_bytes':0})),'byte chunk size')
    expect_error('empty_draws',lambda:scan_packed_oz(good,**(args|{
                       'draws':[]})),'empty fixture drawset')
    return 10


def self_test():
    if not __debug__:
        raise RuntimeError('run without Python -O')
    oracle_src = (HERE/'OUTLANDISH_01_Q2_Independent_Oracle_v0_1.py').read_bytes().replace(b'\r\n',b'\n')
    oid = hashlib.sha1(f'blob {len(oracle_src)}\0'.encode()+oracle_src).hexdigest()
    if oid != ORACLE_GIT_BLOB:
        raise ValueError('Q2 oracle differs from pinned independent version')
    suite = list(scenarios())
    if len(suite) != 11:
        raise AssertionError('Oz fixture count unexpectedly changed')
    # Verify the independent reference really contains the advertised planted
    # any-slot O2 and multi-draw families before invoking engine under test.
    _,digit_string,draws,n,required=suite[0]
    event_ref = {(h.draw,h.family,h.start,h.digits)
                 for h in oracle('oz',digit_string[:n],list(draws))}
    if not required.issubset(event_ref):
        raise AssertionError('Oz fixture mandatory oracle tuples missing')
    for slot in range(7):
        if not any(h[1]=='K7mix' and h[2]==89+24*slot for h in event_ref):
            raise AssertionError(f'missing supplementary-slot {slot} oracle fixture')
    print('Q3 OZ SELF-TEST PASS: independent oracle pinned; 11 planted scenario definitions,')
    print('  both O1/O2/O3, all seven supplementary slots and PB regression dependencies.')


def run_all():
    self_test()
    print('RUNNING UNCHANGED POWERBALL QUALIFICATION against SHARED v0.2 engine:')
    old_scan_packed = pb_qualification.scan_packed
    old_pb_record = pb_qualification.PBRecord
    try:
        pb_qualification.scan_packed = scan_packed
        pb_qualification.PBRecord = PBRecord  # dataclass identity from shared module
        pb_qualification.run_all()
    finally:
        pb_qualification.scan_packed = old_scan_packed
        pb_qualification.PBRecord = old_pb_record
    num_cases=num_chunks=0
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q3_OZ_TEST_ONLY_') as td:
        root=Path(td)
        for name,digits,draws,effective,mandatory in scenarios():
            num_chunks+=check_case(name,digits,draws,effective,root,mandatory=mandatory)
            num_cases+=1
        rng=random.Random(20261114)
        pats=[encoded(*O1.mains),encoded(*O2.mains[:6],O2.supp[0]),
              encoded(*O3.mains[:6])]
        for i in range(10):
            n=190+31*i
            digits=[str(rng.randrange(10)) for _ in range(n)]
            off=17+(i*13)%45
            pat=pats[i%3]
            digits[off:off+len(pat)]=pat
            num_chunks+=check_case(f'seeded_{i:02d}',''.join(digits),DRAWS,
                                   n-(i%7),root,chunks=(3,17,64))
            num_cases+=1
        refused=negative_cases(root)
    print('Q3 SHARED ENGINE PASS: Powerball preserved (22 fixtures/114 configs/7 refusals); '
          f'Oz fixtures={num_cases} chunk-configurations={num_chunks} negative-refusals={refused}; '
          'exact independent-oracle tuples, full-byte SHA, create-only CSV, effective EOF; '
          'TEMP FIXTURES ONLY / NO REAL SCANS / Q5 NOT AUTHORISED')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--self-test',action='store_true')
    group.add_argument('--run',action='store_true')
    args=parser.parse_args()
    if args.self_test:
        self_test()
    else:
        run_all()

if __name__=='__main__':
    main()
