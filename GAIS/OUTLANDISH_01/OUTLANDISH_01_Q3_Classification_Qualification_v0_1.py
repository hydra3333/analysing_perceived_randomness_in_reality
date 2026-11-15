#!/usr/bin/env python3
"""Q3 PB/Oz independent classification and same-draw overlap qualification.

Only invented fixture histories and tiny synthetic packed files under OS TEMP.
No REAL drawset, published constant, receipt, result root, or registry accessed.
No production entry point or Q5 permission.
"""
from __future__ import annotations

import argparse
from collections import Counter,defaultdict
import hashlib
from pathlib import Path
import tempfile

from OUTLANDISH_01_Q2_Independent_Oracle_v0_1 import (
    PowerballDraw, OzDraw, oracle, encoded, plant, pack_independent,
)
from OUTLANDISH_01_Q2_LegacyScanner_Comparison_v0_1 import (
    scenario_set as pb_scenarios, DRAWS as PB_DRAWS,
)
from OUTLANDISH_01_Q3_Shared_Qualification_v0_2 import (
    scenarios as oz_scenarios,
)
from OUTLANDISH_01_Q3_Packed_Matcher_v0_2 import (
    PBRecord, OzRecord, RawEvent, scan_packed, scan_packed_oz,
    write_fixture_events_create_only,
)
from OUTLANDISH_01_Q3_Event_Interface_Smoke_v0_1 import read_events
from OUTLANDISH_01_Q3_Event_Classifier_v0_1 import (
    classify_events, summarize_same_draw_overlaps,
)

HERE = Path(__file__).resolve().parent
PINNED_Q2_ORACLE = '6ea5562ed681c854f8c552e9600af5d8f9d3be00'
PINNED_SHARED_ENGINE = '38f74d923f444e871f9319a52f2698c0c21e6288'


def blob_sha1(path: Path) -> str:
    data = path.read_bytes().replace(b'\r\n',b'\n')
    return hashlib.sha1(f'blob {len(data)}\0'.encode('ascii')+data).hexdigest()


def pb_records(draws):
    return [PBRecord(d.number,d.mains,d.pb) for d in draws]


def oz_records(draws):
    return [OzRecord(d.number,d.mains,d.supp) for d in draws]


def raw_from_oracle(game, digit_string, draws):
    hits = oracle(game,digit_string,list(draws))
    expected = {(h.draw,h.family,h.start,h.digits): h for h in hits}
    if len(expected) != len(hits):
        raise AssertionError('independent oracle emitted duplicate raw identities')
    events = tuple(sorted((RawEvent(h.draw,h.family,h.start,h.digits) for h in hits),
                 key=lambda e:(e.start_digit_offset,e.family,e.draw_number)))
    return expected, events


def validate_oracle_flags(game, classified, reference):
    counts = Counter()
    for c in classified:
        e=c.event
        key=(e.draw_number,e.family,e.start_digit_offset,e.matched_digits)
        flags=set(reference[key].flags)
        if game=='powerball':
            label={'K7S':'P1','K7':'P2','K6S':'P3'}[e.family]
            assert c.category==label
            assert (label+'_any_order') in flags
            if e.family in ('K7S','K7'):
                assert c.drawn_order == (label+'_drawn_order' in flags), (key,flags,c)
                assert c.reordered_only == (label+'_reordered_only' in flags), (key,flags,c)
                assert c.historical_pb_baseline == c.drawn_order
                assert c.drawn_subsequence_order is None
            else:
                assert c.drawn_subsequence_order == ('P3_drawn_subsequence_order' in flags), (key,flags,c)
                assert c.reordered_only == ('P3_reordered_only' in flags)
                assert c.historical_pb_baseline is True
                assert c.omitted_main is not None
        else:
            label={'K7':'O1','K7mix':'O2','K6':'O3'}[e.family]
            assert c.category == label
            assert c.historical_pb_baseline is None
            if e.family=='K7':
                assert c.drawn_order == ('O1_drawn_order' in flags), (key,flags,c)
                assert c.reordered_only == ('O1_reordered_only' in flags)
            elif e.family=='K6':
                assert c.drawn_subsequence_order == ('O3_drawn_subsequence_order' in flags)
                assert c.reordered_only == ('O3_reordered_only' in flags)
            else:
                assert 'O2_any_slot' in flags
                assert f'O2_supp_slot_{c.supplementary_slot}' in flags
                assert c.supplementary_slot in range(7)
                assert c.supplementary_drawn_index in range(3)
                assert c.supplementary_last == ('O2_supplementary_last' in flags)
                assert c.drawn_subsequence_order == ('O2_drawn_subsequence_order' in flags)
                assert c.supplementary_last_reordered_only == ('O2_supplementary_last_reordered_only' in flags)
                assert c.any_slot_non_drawn == ('O2_any_slot_non_drawn' in flags)
                assert c.reordered_only is None  # no ambiguous generic O2 reorder label
                counts[f'O2_SLOT_{c.supplementary_slot}']+=1
        counts[label]+=1
        if c.drawn_order is True: counts[label+'_DRAWN']+=1
        if c.drawn_subsequence_order is True: counts[label+'_SUBSEQ']+=1
        if c.reordered_only is True: counts[label+'_REORDERED']+=1
    return counts


def naive_overlap(events,game):
    lengths=({'K7S':16,'K7':14,'K6S':14} if game=='powerball' else
             {'K7':14,'K7mix':14,'K6':12})
    same=total=0
    families=Counter()
    for i,a in enumerate(events):
        for b in events[i+1:]:
            if a.draw_number != b.draw_number:continue
            if a.start_digit_offset < b.start_digit_offset + lengths[b.family] and b.start_digit_offset < a.start_digit_offset + lengths[a.family]:
                total+=1
                same+=(a.start_digit_offset==b.start_digit_offset)
                families[tuple(sorted((a.family,b.family)))]+=1
    return total,same,dict(families)


def check_case(game,label, digits, draws, effective, root, *, chunk_size):
    by_draw = pb_records(draws) if game=='powerball' else oz_records(draws)
    expected, reference_events = raw_from_oracle(game,digits[:effective],draws)
    expected_classes=classify_events(game,reference_events,by_draw,effective_digits=effective)
    counts=validate_oracle_flags(game,expected_classes,expected)
    packed=pack_independent(digits)
    path=root / (game+'_'+label+'.SYNTHETIC_TEST_ONLY.packed.bin')
    path.write_bytes(packed)
    scanned=(scan_packed if game=='powerball' else scan_packed_oz)(
        path,physical_digits=len(digits),effective_digits=effective,
        draws=by_draw,chunk_bytes=chunk_size,
        expected_full_sha256=hashlib.sha256(packed).hexdigest())
    if scanned.events!=reference_events:
        raise AssertionError(f'{game}/{label}: raw scanner vs independent oracle differs')
    classes=classify_events(game,scanned.events,by_draw,effective_digits=effective)
    if classes!=expected_classes:
        raise AssertionError(f'{game}/{label}: classifier vs Q2-oracle flags differs')
    csv=root/(game+'_'+label+'.events.csv')
    csv_digest=write_fixture_events_create_only(csv,scanned.events)
    parsed=read_events(csv.read_bytes(),game=game,logical_N=effective,
          allowed_draws={d.number for d in draws},recorded_sha256=csv_digest)
    reparsed=[RawEvent(e.draw_number,e.family,e.start_digit_offset,e.matched_digits) for e in parsed]
    if classify_events(game,reparsed,by_draw,effective_digits=effective) != classes:
        raise AssertionError(f'{game}/{label}: classification replay after CSV failed')
    overlaps=summarize_same_draw_overlaps(scanned.events,game=game)
    brute=naive_overlap(scanned.events,game)
    if (overlaps.direct_same_draw_pairs,overlaps.same_start_pairs,overlaps.family_pair_counts) != brute:
        raise AssertionError(f'{game}/{label}: overlap sweep differs from independent pair enumeration: {overlaps} != {brute}')
    print(f'PASS: {game} {label}: classified {len(classes)} oracle-equal rows; direct-overlap-pairs={overlaps.direct_same_draw_pairs}')
    offsets=defaultdict(set)
    for c in classes:
        offsets[c.category].add(c.event.start_digit_offset)
    return counts,len(classes),offsets


def expect_refusal(name,call):
    try:call()
    except ValueError:
        print('PASS: refusal_'+name)
    else:raise AssertionError('malformed fixture accepted: '+name)


def refusal_tests():
    p=PBRecord(1,(3,7,11,15,19,23,35),7)
    o=OzRecord(2,(1,5,9,13,17,21,47),(2,4,6))
    ptext=encoded(*p.mains_drawn,p.powerball)
    gold=RawEvent(1,'K7S',2,ptext)
    tests={
        'duplicate_event':lambda:classify_events('powerball',[gold,gold],[p],effective_digits=50),
        'out_of_order':lambda:classify_events('powerball',[RawEvent(1,'K7',21,ptext[:14]),gold],[p],effective_digits=50),
        'invalid_special':lambda:classify_events('powerball',[RawEvent(1,'K7S',2,ptext[:-2]+'12')],[p],effective_digits=50),
        'unknown_draw':lambda:classify_events('powerball',[RawEvent(2,'K7S',2,ptext)],[p],effective_digits=50),
        'family_wrong_game':lambda:classify_events('oz',[gold],[o],effective_digits=50),
        'invalid_digit_text':lambda:classify_events('powerball',[RawEvent(1,'K7S',2,'A'+ptext[1:])],[p],effective_digits=50),
        'invalid_prefix_EOF':lambda:classify_events('powerball',[gold],[p],effective_digits=17),
        'wrong_P3_subset':lambda:classify_events('powerball',[RawEvent(1,'K6S',2,'01020304050607')],[p],effective_digits=50),
        'duplicate_draw':lambda:classify_events('powerball',[gold],[p,p],effective_digits=50),
        'invalid_Oz_roles':lambda:classify_events('oz',[],[OzRecord(2,o.mains_drawn,(1,4,6))],effective_digits=50),
        'invalid_Oz_supp_slot':lambda:classify_events('oz',[RawEvent(2,'K7mix',3,'01050913172147')],[o],effective_digits=50),
        'invalid_negative_start':lambda:classify_events('powerball',[RawEvent(1,'K7S',-1,ptext)],[p],effective_digits=50),
        'invalid_order_raw':lambda:classify_events('powerball',[RawEvent(1,'K7S',2,ptext),RawEvent(1,'K7',0,ptext[:14])],[p],effective_digits=50),
    }
    for name,f in tests.items(): expect_refusal(name,f)
    return len(tests)


def self_test():
    if not __debug__:
        raise RuntimeError('run without -O')
    if blob_sha1(HERE/'OUTLANDISH_01_Q2_Independent_Oracle_v0_1.py')!=PINNED_Q2_ORACLE:
        raise ValueError('independent oracle changed since Q2 qualification')
    if blob_sha1(HERE/'OUTLANDISH_01_Q3_Packed_Matcher_v0_2.py')!=PINNED_SHARED_ENGINE:
        raise ValueError('Q3 shared scanner changed; re-review classifier test inputs')
    # Zero-start and negative/near-end overlap semantics; distinct draws excluded.
    toy=(RawEvent(1,'K7',0,'01020304050607'),RawEvent(2,'K7',0,'01020304050607'),
         RawEvent(1,'K6S',2,'02030405060708'),RawEvent(1,'K7',16,'01020304050607'))
    summary=summarize_same_draw_overlaps(toy,game='powerball')
    if summary.direct_same_draw_pairs != 1 or summary.shifted_start_pairs!=1:
        raise AssertionError('overlap half-open / same-draw contract regression')
    if len(list(pb_scenarios()))<6 or len(list(oz_scenarios()))!=11:
        raise AssertionError('historical Q3 fixture definitions changed')
    print('Q3 CLASSIFIER SELF-TEST PASS: Q2 oracle and shared engine pinned; half-open same-draw overlap rule; no files created')


def run_all():
    self_test()
    all_count=Counter();all_offsets=defaultdict(set);cases=rows=0
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q3_CLASSIFICATION_FIXTURE_ONLY_') as t:
        root=Path(t)
        for p in pb_scenarios():
            n=p.prefix_digits if p.prefix_digits is not None else len(p.digits)
            counts,k,offsets=check_case('powerball',p.name,p.digits,PB_DRAWS,n,root,chunk_size=3)
            all_count.update(counts);cases+=1;rows+=k
            for cat,locations in offsets.items():all_offsets[cat].update(locations)
        # Extra designed controls to ensure both drawn/reordered P1/P2 and P3.
        d=PowerballDraw(101,(3,7,11,15,19,23,35),7)
        for name,pat in [('pb_drawn',encoded(*d.mains,d.pb)),
                         ('pb_reordered',encoded(*reversed(d.mains),d.pb)),
                         ('pb_P3_reordered',encoded(7,3,11,15,19,23,7))]:
            data=plant(71,[(17,pat)])
            counts,k,offsets=check_case('powerball',name,data,[d],71,root,chunk_size=5)
            all_count.update(counts);cases+=1;rows+=k
            for cat,locations in offsets.items():all_offsets[cat].update(locations)
        for name,text,draws,n,_ in oz_scenarios():
            counts,k,offsets=check_case('oz',name,text,draws,n,root,chunk_size=3)
            all_count.update(counts);cases+=1;rows+=k
            for cat,locations in offsets.items():all_offsets[cat].update(locations)
        # Explicit Oz O1 reordered and O3 reordered classification with valid roles.
        d=OzDraw(77,(1,5,9,13,17,21,47),(2,4,6))
        for name,pat in [('oz_O1_reordered',encoded(*reversed(d.mains))),
                         ('oz_O3_reordered',encoded(5,1,9,13,17,21)),
                         ('oz_O2_supp_last_reordered',encoded(5,1,9,13,17,21,2))]:
            counts,k,offsets=check_case('oz',name,plant(73,[(23,pat)]),[d],73,root,chunk_size=7)
            all_count.update(counts);cases+=1;rows+=k
            for cat,locations in offsets.items():all_offsets[cat].update(locations)
    needed=('P1','P2','P3','O1','O2','O3')
    if any(all_count[x]<2 or len(all_offsets[x])<2 for x in needed):
        raise AssertionError(f'missing two distinct physical starts/category: {dict(all_count)}, {dict(all_offsets)}')
    if any(all_count[f'O2_SLOT_{i}']<1 for i in range(7)):
        raise AssertionError('some Oz supplementary slots not covered')
    if all_count['P1_DRAWN']<2 or all_count['P2_DRAWN']<2 or all_count['O1_DRAWN']<2:
        raise AssertionError('narrow drawn-order controls insufficient')
    if all_count['P3_SUBSEQ']<1 or all_count['O3_SUBSEQ']<1 or all_count['O2_SUBSEQ']<1:
        raise AssertionError('drawn-subsequence controls insufficient')
    if all_count['P3_REORDERED']<1 or all_count['O3_REORDERED']<1 or all_count['O1_REORDERED']<1:
        raise AssertionError('reordered controls insufficient')
    refusals=refusal_tests()
    print(f'Q3 CLASSIFIER PASS: scenarios={cases}, raw-events={rows}, at least two distinct starts/family, seven Oz supplementary slots, baseline/drawn/subsequence/reordered flags oracle-equal; same-draw overlap sweep agrees with brute force; refusals={refusals}. SYNTHETIC ONLY / Q5 NOT AUTHORISED')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    x=p.add_mutually_exclusive_group(required=True)
    x.add_argument('--self-test',action='store_true')
    x.add_argument('--run',action='store_true')
    a=p.parse_args()
    if a.self_test:self_test()
    else:run_all()

if __name__=='__main__':main()
