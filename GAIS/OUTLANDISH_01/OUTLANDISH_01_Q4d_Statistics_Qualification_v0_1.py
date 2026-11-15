#!/usr/bin/env python3
"""Q4d statistics qualification: hand-computed synthetic or full Q4c/Q3 fixtures.

--self-test: stdlib only, no imports of scanner or project histories.
--run: requires previously qualified Q3/Q4b/Q4c sources; creates four tiny
marked temporary TEST runs, replays and classifies without opening packed BCD.
Both modes operate only in TemporaryDirectory. NO production scans or Q5.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import hashlib
import itertools
import statistics
from unittest import mock
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace as Obj

import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S

@dataclass(frozen=True)
class E:
    draw_number: int
    family: str
    start_digit_offset: int
    matched_digits: str


def event(d, fam, offset):
    return E(d, fam, offset, '0' * S.FAMILY_LENGTHS[fam])


def clas(e, category, *, drawn=None, subseq=None, reordered=None, last=None):
    return Obj(event=e, category=category, drawn_order=drawn,
               drawn_subsequence_order=subseq, reordered_only=reordered,
               supplementary_last=last)


def refusal(name, fn):
    try:
        fn()
    except (ValueError, TypeError):
        return 1
    raise AssertionError(f'expected refusal missing: {name}')


def hand_computed():
    checks=0
    refusals=0
    ids=(1,2,3,4,5)
    # Same-start+shifted physical overlaps, all within draw 1.
    ev=[event(1,'K7S',5),event(1,'K7',5),event(1,'K6S',7)]
    ev=tuple(sorted(ev,key=lambda e:(e.start_digit_offset,e.family,e.draw_number)))
    classes=[]
    for e in ev:
        if e.family=='K7S':
            classes.append(clas(e,'P1',drawn=True,reordered=False))
        elif e.family=='K7':
            classes.append(clas(e,'P2',drawn=False,reordered=True))
        else:
            classes.append(clas(e,'P3',subseq=True,reordered=False))
    rows=S.category_summary('powerball',classes,ids,100)
    by={r['view']:r for r in rows}
    assert by['P1_any']['events']==1 and by['P1_drawn']['events']==1
    assert by['P1_reordered']['events']==0
    assert by['P2_any']['events']==1 and by['P2_drawn']['events']==0
    assert by['P3_any']['events']==1 and by['P3_subsequence']['events']==1
    assert by['P3_reordered']['events']==0
    assert by['P1_any']['distinct_offsets']==by['P1_any']['distinct_draws']==1
    assert by['P1_any']['eligible_starts_per_draw']==85
    assert by['P1_any']['sequences_per_draw']==5040
    assert abs(by['P1_any']['analytical_expected_events']-5*5040*85/(10**16))<1e-22
    assert by['P3_subsequence']['conditional_parent']=='P3_any'
    assert by['P3_subsequence']['conditional_q']==1/720
    assert by['P3_subsequence']['conditional_expected']==1/720
    checks+=13
    overlap=S.physical_overlaps('powerball',ev,ids,100)
    assert overlap['events']==3 and overlap['direct_same_draw_pairs']==3
    assert overlap['same_start_pairs']==1 and overlap['shifted_start_pairs']==2
    assert overlap['family_pair_counts']=={'K6S+K7':1,'K6S+K7S':1,'K7+K7S':1}
    checks+=4
    # Two equally close signed-gap candidates: -5 wins over +5.
    assert S.closest_gap((10,20),(15,))==(5,-5,20,15)
    assert S.closest_gap((20,10),(15,15))==(5,-5,20,15)
    assert S.closest_gap((30,),(30,))==(0,0,30,30)
    assert S.closest_gap((),(10,)) is None
    # Exhaustively compare the bisect implementation to an independent
    # O(A*B) tiny oracle for every pair of nonempty subsets of five offsets.
    universes=range(5)
    choices=[tuple(i for i in universes if mask & (1<<i)) for mask in range(1,32)]
    for a in choices:
        for b in choices:
            brute=min((abs(y-x),y-x,x,y) for x in a for y in b)
            assert S.closest_gap(a,b)==brute
    checks+=4+31*31
    # Five positions including the empty middle draw; two evaluable of four.
    offsets=[(10,20),(15,),(),(30,45),(30,)]
    events=[]
    for draw,ss in zip(ids,offsets):
        events.extend(event(draw,'K6S',start) for start in ss)
    events.sort(key=lambda e:(e.start_digit_offset,e.family,e.draw_number))
    trs,summary,sets=S.transitions('powerball',events,ids,100)
    assert summary['total_adjacent_pairs']==4
    assert summary['evaluable_pairs']==2 and summary['non_evaluable_pairs']==2
    assert summary['observed_median_absolute_gap']==2.5
    assert trs[0]['minimum_abs_gap']==5 and trs[0]['signed_gap']==-5
    assert (trs[0]['start_W'],trs[0]['start_next'])==(20,15)
    assert trs[1]['evaluable'] is False and trs[2]['evaluable'] is False
    assert trs[3]['zero_physical_gap'] and trs[3]['signed_gap']==0
    assert sets==tuple(offsets)
    checks+=8
    perm=S.permutation_test(sets,seed=1977,iterations=99)
    repeat=S.permutation_test(sets,seed=1977,iterations=99)
    assert perm==repeat
    assert perm['iterations_requested']==99
    assert perm['observed_median']==2.5
    assert perm['valid_permutations']+perm['undefined_permutations']==99
    assert 0<perm['centered_two_sided_p']<=1
    assert 0<perm['tail_upper_inclusive']<=1
    assert 0<perm['tail_lower_inclusive']<=1
    assert perm['permutation_evaluable_min']<=perm['permutation_evaluable_max']<=4
    checks+=8
    # Explicitly enumerate all 24 whole-draw permutations, including empty.
    # Independent brute-force gap arithmetic and median are the oracle here.
    small=((0,),(3,),(10,),())
    arrangements=list(itertools.permutations(small))
    all_medians=[]
    for arrangement in arrangements:
        gaps=[]
        for a,b in zip(arrangement,arrangement[1:]):
            if a and b:
                gaps.append(min(abs(y-x) for x in a for y in b))
        if gaps:
            all_medians.append(statistics.median(gaps))
    center=statistics.median(all_medians)
    observed=statistics.median((3,7))
    expected=(1+sum(abs(m-center)>=abs(observed-center) for m in all_medians))/(len(all_medians)+1)
    class EnumerateAll:
        def __init__(self,seed):
            self.ordered=iter(arrangements)
        def shuffle(self,items):
            items[:]=next(self.ordered)
    with mock.patch.object(S.random,'Random',EnumerateAll):
        census=S.permutation_test(small,seed=9,iterations=24)
    assert census['valid_permutations']==len(all_medians)
    assert census['undefined_permutations']==24-len(all_medians)
    assert census['permuted_median_center']==center
    assert census['centered_two_sided_p']==expected
    checks+=4
    empty=S.permutation_test(((),(),(),()),seed=1,iterations=17)
    assert empty['observed_median'] is None and empty['valid_permutations']==0
    assert empty['undefined_permutations']==17
    assert empty['centered_two_sided_p'] is None
    assert empty['tail_upper_inclusive'] is None and empty['tail_lower_inclusive'] is None
    assert empty['undefined_reason']=='OBSERVED_NO_EVALUABLE_ADJACENT_PAIRS'
    checks+=5
    rare=S.permutation_test(((10,),(),(),()),seed=2,iterations=9)
    assert rare['centered_two_sided_p'] is None and rare['undefined_permutations']==9
    checks+=1
    assert S.binomial_two_sided(0,0,.5)==1
    assert abs(S.binomial_two_sided(2,2,.5)-.5)<1e-12
    assert abs(S.binomial_two_sided(2,0,.5)-.5)<1e-12
    checks+=3
    # Independent six-constant Holm example with missing one held at p=1.
    pv=dict(pi=.01,phi=.04,e=.03,log2=.002,gamma=.5,lemniscate=None)
    holm=S.holm_six_constants(pv)
    assert holm['lemniscate'] is None
    assert abs(holm['log2']-.012)<1e-12
    assert abs(holm['pi']-.05)<1e-12
    assert abs(holm['e']-.12)<1e-12 and abs(holm['phi']-.12)<1e-12
    assert holm['gamma']==1
    checks+=5
    tail=S.decoy_count_tails(2,(0,1,2))
    assert tail['K']==3 and tail['upper_inclusive_p']==.5
    assert tail['lower_inclusive_p']==1
    assert tail['comparison']=='SUMMARY_COUNTS_ONLY_NOT_RAW_EVENT_JOIN'
    checks+=3
    oz_event=event(1,'K7mix',0)
    oz_classes=(clas(oz_event,'O2',last=True,subseq=True,reordered=False),)
    oz={r['view']:r for r in S.category_summary('oz',oz_classes,ids,100)}
    assert oz['O2_any_slot']['events']==oz['O2_supplementary_last']['events']==1
    assert oz['O2_subsequence']['events']==1
    assert oz['O2_last_reordered']['events']==0
    assert oz['O2_any_slot']['sequences_per_draw']==105840
    assert oz['O2_supplementary_last']['sequences_per_draw']==15120
    assert oz['O2_subsequence']['sequences_per_draw']==21
    assert oz['O2_subsequence']['conditional_q']==21/15120
    checks+=6
    # Must fail without any production sources. These are scientific canaries.
    refusals+=refusal('missing draw position',lambda:S.transitions('powerball',(),(1,3),100))
    refusals+=refusal('out-of-era event',lambda:S.transitions('powerball',(event(99,'K6S',3),),ids,100))
    refusals+=refusal('wrong family',lambda:S.transitions('oz',(event(1,'K6S',0),),ids,100))
    refusals+=refusal('EOF mismatch',lambda:S.transitions('powerball',(event(1,'K6S',90),),ids,100))
    refusals+=refusal('duplicate identity',lambda:S.physical_overlaps('powerball',(event(1,'K6S',0),event(1,'K6S',0)),ids,100))
    refusals+=refusal('out of order',lambda:S.physical_overlaps('powerball',(event(1,'K6S',10),event(1,'K6S',0)),ids,100))
    refusals+=refusal('bad classification',lambda:S.category_summary('powerball',(clas(event(1,'K6S',2),'P1'),),ids,100))
    refusals+=refusal('wrong six Holm',lambda:S.holm_six_constants(dict(pi=.5)))
    refusals+=refusal('bad p',lambda:S.holm_six_constants(dict.fromkeys(S.CONSTANTS,1.2)))
    refusals+=refusal('invalid decoy count',lambda:S.decoy_count_tails(1,(-1,)))
    refusals+=refusal('invalid iteration count',lambda:S.permutation_test(((),()),seed=0,iterations=0))
    refusals+=refusal('invalid offset',lambda:S.permutation_test(((0,),(-1,)),seed=0,iterations=9))
    refusals+=refusal('boolean counts',lambda:S.decoy_count_tails(True,(1,)))
    return checks,refusals


def _classify_q4c(roots, game, kind, run_id):
    """Q4c's existing verified loader is the ONLY source of event inputs here."""
    import OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1 as P
    import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
    from OUTLANDISH_01_Q3_Event_Classifier_v0_1 import (
        classify_events, RawEvent, PBRecord, OzRecord)
    loaded=P.load_verified_synthetic_run(roots,game,'phi',kind,run_id)
    if kind=='TEST_REAL':
        numbered=G.validate_drawset(P._historical_profile(roots,game)).draw_rows
        labels=None
    else:
        source=roots.run_location(kind,run_id)/'decoy_histories.csv'
        manifest=json.loads((roots.run_location(kind,run_id)/'run_manifest.json').read_text())
        decoded=P._read_decoys(source.read_bytes(),game=game,k=manifest['k'])
        numbered=tuple((n,v) for n,_,v in decoded)
        labels=tuple(label for _,label,_ in decoded)
    ev=tuple(RawEvent(e.draw_number,e.family,e.start_digit_offset,e.matched_digits) for e in loaded)
    if game=='powerball':
        draws=tuple(PBRecord(n,v[:7],v[7]) for n,v in numbered)
    else:
        draws=tuple(OzRecord(n,v[:7],v[7:]) for n,v in numbered)
    classes=classify_events(game,ev,draws,effective_digits=10001)
    return ev,classes,tuple(n for n,_ in numbered),labels


def _fixture_reports(roots, game, report, category, rows, overlapped, permutation):
    """Create ONLY scratch reports under a marked temporary root; no saved REAL run modifications."""
    import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
    if not roots.synthetic or report != f'TEST_REPORT_{game}' or game not in ('powerball','oz'):
        raise ValueError('fixture reporting cannot touch production root or unrelated paths')
    G.FixedRoots.test_sandbox(roots.base)
    folder=G._inside(roots.base,roots.base/'q4d_synthetic_reports'/report)
    folder.parent.mkdir(exist_ok=True)
    folder.mkdir(exist_ok=False)
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=tuple(category[0]),lineterminator='\n')
    writer.writeheader(); writer.writerows(category)
    sources={'category_summary.csv':stream.getvalue().encode('utf-8')}
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=tuple(rows[0]) if rows else ('W','W_plus_1'),lineterminator='\n')
    writer.writeheader();writer.writerows(rows)
    sources['transitions.csv']=stream.getvalue().encode('utf-8')
    summary=dict(schema='Q4D_SYNTHETIC_REPORT_ONLY_V1',game=game,
                 report=report,physical_overlaps=overlapped,permutation=permutation)
    sources['summary.json']=(json.dumps(summary,indent=2,sort_keys=True)+'\n').encode('utf-8')
    for name,payload in sources.items():
        with (folder/name).open('xb') as f:
            f.write(payload)
    assert all((folder/name).read_bytes()==blob for name,blob in sources.items())
    return folder


def integration():
    """Four genuine Q3 v0.4 scans using Q4c's prevalidated tiny fixture data."""
    import OUTLANDISH_01_Q4c_Synthetic_Processing_Qualification_v0_1 as Q
    import OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1 as P
    from OUTLANDISH_01_Q3_Event_Classifier_v0_1 import summarize_same_draw_overlaps
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q4D_STATS_') as temp:
        roots,n=Q.make_temp(Path(temp))
        records={}
        for game in ('powerball','oz'):
            for kind,k,seed in (('TEST_REAL',1,None),('TEST_NULL',2,7777 if game=='powerball' else 8888)):
                runid=f'{kind}_q4d_{game}'
                P.run_synthetic(roots,game,'phi',kind,runid,
                                fixture_digits=n,k=k,seed=seed,chunk_bytes=9)
                records[(game,kind)]=(runid,*_classify_q4c(roots,game,kind,runid))
        report_count=0
        for game in ('powerball','oz'):
            realid,realev,realclass,realids,_=records[(game,'TEST_REAL')]
            nullid,nullev,nullclass,nullids,labels=records[(game,'TEST_NULL')]
            assert labels is not None and all(x.startswith('DECOY-') for x in labels)
            categories=S.category_summary(game,realclass,realids,n)
            by={entry['view']:entry for entry in categories}
            overlaps=S.physical_overlaps(game,realev,realids,n)
            previous=summarize_same_draw_overlaps(realev,game=game)
            assert overlaps['events']==previous.events
            assert overlaps['direct_same_draw_pairs']==previous.direct_same_draw_pairs
            assert overlaps['same_start_pairs']==previous.same_start_pairs
            assert overlaps['shifted_start_pairs']==previous.shifted_start_pairs
            assert overlaps['family_pair_counts']=={'+'.join(key):value for key,value in previous.family_pair_counts.items()}
            transitions,summary,offsets=S.transitions(game,realev,realids,n)
            perm=S.permutation_test(offsets,seed=1024,iterations=101)
            assert len(transitions)==len(realids)-1==2
            assert summary['evaluable_pairs']+summary['non_evaluable_pairs']==2
            primary='P3_any' if game=='powerball' else 'O3_any'
            null_primary='P3' if game=='powerball' else 'O3'
            null_counts=[0,0]
            for c in nullclass:
                if c.category==null_primary:
                    null_counts[(c.event.draw_number-1)//3]+=1
            comparison=S.decoy_count_tails(by[primary]['events'],null_counts)
            assert comparison['K']==2 and 0<comparison['upper_inclusive_p']<=1
            destination=_fixture_reports(roots,game,f'TEST_REPORT_{game}',categories,
                                         transitions,overlaps,perm)
            assert b'Q4D_SYNTHETIC_REPORT_ONLY_V1' in (destination/'summary.json').read_bytes()
            assert len((destination/'category_summary.csv').read_bytes())>100
            report_count+=1
        # Holm is one six-constant family for EACH game, never combines games.
        S.holm_six_constants(dict.fromkeys(S.CONSTANTS,None))
        return report_count,4


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--self-test',action='store_true')
    group.add_argument('--run',action='store_true')
    args=parser.parse_args()
    checks,refusals=hand_computed()
    reports=runs=0
    if args.run:
        reports,runs=integration()
    print(f'Q4D SYNTHETIC {"INTEGRATION" if args.run else "ARITHMETIC"} PASS: '
          f'hand-checks={checks} guard-refusals={refusals} '
          f'synthetic-scans={runs} fixture-reports={reports} '
          'production-scans=0 REAL-history-reads=0')


if __name__=='__main__':
    main()
