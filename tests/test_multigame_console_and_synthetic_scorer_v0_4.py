"""Package 2: offline-only protocol and scorer tests; no real draws used."""
from __future__ import annotations
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'/'methods'))
from _common.game_profiles_v1 import POWERBALL, OZLOTTO
from _common.multigame_e1_v1 import forecast
from _common.multigame_standalone_contract_v1 import (
    begin_synthetic, publish_synthetic_success, json_bytes,
)
from _common.multigame_console_protocol_v1 import (
    prepare_success_records,verify_success_records,verify_failed_records,
)
from _common.multigame_synthetic_scorer_v1 import score_verified_synthetic


def make_run(root: Path,p,draw,tag):
    rows=[]
    for i in range(p.first_draw,draw):
        row={'draw':i}
        for b in p.barrels:
            row[b.barrel_id]=list(range(b.low,b.low+b.selected))
        rows.append(row)
    result=forecast(p,rows,'0'*64,draw,data_kind='SYNTHETIC_CONTRACT_TEST')
    run_id='mg-'+tag
    directory,status=begin_synthetic(root,run_id=run_id,profile=p,target=draw,
        method_id='E_1',variant_id='FULL_HISTORY_RAW_COUNTS_V1')
    publish_synthetic_success(directory,status,result)
    return p,run_id,directory,result


def synthetic_outcome(p,draw,*,value=1):
    return {
        'kind':'SYNTHETIC_CONTRACT_TEST','game_id':p.game_id,
        'draw_number':draw,'draw_key':p.draw_key(draw),
        'profile_version':p.version,
        'barrels':{b.barrel_id:list(range(value,value+b.selected)) for b in p.barrels},
    }


class ConsoleProtocolTests(unittest.TestCase):
    def test_matching_protocol_and_strict_order(self):
        d={'game_id':'OZLOTTO','method_id':'E_1','draw_number':1480,
           'draw_key':'OZLOTTO_1480','barrels':{'MAIN':{}}}
        args=dict(game_id='OZLOTTO',method_id='E_1',run_id='mg-testconsole004',target=1480)
        lines=list(prepare_success_records(result=d,**args))
        verify_success_records(lines,canonical_result=json_bytes(d),**args)
        for mutant in (lines[:-1],lines+[lines[2]],list(reversed(lines)),
                       [lines[0],lines[2],lines[1],lines[3]],
                       [*lines,'READER_ERROR: synthetic'],
                       [*lines[:2],'DIGEST '+'0'*64,lines[-1]],
                       [lines[0].replace('OZLOTTO','POWERBALL'),*lines[1:]],
                       [*lines,'FINISH E_1 SUCCESS']):
            with self.subTest(mutant=mutant):
                with self.assertRaises(ValueError):
                    verify_success_records(mutant,canonical_result=json_bytes(d),**args)
        with self.assertRaises(ValueError):
            verify_success_records(lines,canonical_result=json_bytes({**d,'draw_number':1481}),**args)

    def test_console_binding_to_exact_published_json(self):
        args=dict(game_id='POWERBALL',method_id='E_2',run_id='mg-testconsole005',target=1200)
        d={'game_id':'POWERBALL','draw_number':1200,'draw_key':'POWERBALL_1200','method_id':'E_2','message':'x'}
        lines=list(prepare_success_records(result=d,**args))
        verify_success_records(lines,canonical_result=json_bytes(d),**args)
        with self.assertRaises(ValueError):
            verify_success_records(lines,canonical_result=json_bytes({**d,'message':'changed'}),**args)
        with self.assertRaises(ValueError):
            verify_success_records(lines,canonical_result=b'{"a":1}\n',**args)

    def test_failed_record_never_publishes_success(self):
        args=dict(game_id='OZLOTTO',method_id='E_1',run_id='mg-testconsole006',target=1478)
        prefix='BEGIN E_1 game=OZLOTTO draw=1478 run=mg-testconsole006'
        finish='FINISH E_1 game=OZLOTTO draw=1478 run=mg-testconsole006 FAILED'
        verify_failed_records([prefix,finish],**args)
        verify_failed_records([prefix],**args)  # abrupt failure need not finish
        for bad in (['RESULT {}'],['DIGEST '+'0'*64],[prefix,finish.replace('FAILED','SUCCESS')],
                    [prefix,prefix],['READER_ERROR: test'],['BEGIN E_2 wrong']):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    verify_failed_records(bad,**args)

class SyntheticScorerTests(unittest.TestCase):
    def test_oz_one_barrel_and_native_mid_rank(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); p,run_id,directory,result=make_run(root,OZLOTTO,1478,'testscoresoz004')
            calls=[]
            def loader():
                calls.append(1)
                return synthetic_outcome(p,1478)
            s=score_verified_synthetic(run_dir=directory,run_id=run_id,profile=p,
                method_id='E_1',variant_id='FULL_HISTORY_RAW_COUNTS_V1',
                target=1478,global_orphan_marker=root/'UNRESOLVED_ORPHAN.json',
                outcome_loader=loader)
            self.assertEqual(calls,[1]); self.assertEqual(set(s['barrels']),{'MAIN'})
            self.assertEqual(s['barrels']['MAIN']['top_matches'],7)
            self.assertEqual(s['barrels']['MAIN']['worst_matches'],0)
            # 7 labels tie at score 4 occupying positions 1..7 => mid-rank 4.
            self.assertEqual(s['barrels']['MAIN']['mean_native_mid_rank'],4.0)
            self.assertAlmostEqual(s['barrels']['MAIN']['reference_top_matches'],49/47)
            self.assertEqual(s['barrels']['MAIN']['reference_mean_rank'],24)

    def test_powerball_two_barrels(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); p,run_id,directory,result=make_run(root,POWERBALL,1148,'testscorespb004')
            s=score_verified_synthetic(run_dir=directory,run_id=run_id,profile=p,
                method_id='E_1',variant_id='FULL_HISTORY_RAW_COUNTS_V1',
                target=1148,global_orphan_marker=root/'UNRESOLVED_ORPHAN.json',
                outcome_loader=lambda:synthetic_outcome(p,1148))
            self.assertEqual(set(s['barrels']),{'MAIN','POWERBALL'})
            self.assertEqual(s['barrels']['MAIN']['reference_mean_rank'],18)
            self.assertEqual(s['barrels']['POWERBALL']['reference_mean_rank'],10.5)
            self.assertEqual(s['barrels']['POWERBALL']['top_matches'],1)
            self.assertEqual(s['barrels']['POWERBALL']['worst_matches'],0)
            self.assertAlmostEqual(s['barrels']['POWERBALL']['reference_top_matches'],.05)

    def test_firewall_before_outcome_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p,run_id,directory,_=make_run(root,OZLOTTO,1478,'testscoresfw004')
            call_count=[]
            def load():
                call_count.append(1);return synthetic_outcome(p,1478)
            args=dict(run_dir=directory,run_id=run_id,profile=p,
                method_id='E_1',variant_id='FULL_HISTORY_RAW_COUNTS_V1',
                target=1478,global_orphan_marker=root/'UNRESOLVED_ORPHAN.json',
                outcome_loader=load)
            # A global orphan marker blocks the OUTCOME CALLBACK as well.
            marker=root/'UNRESOLVED_ORPHAN.json';marker.write_text('{}')
            with self.assertRaises(ValueError):score_verified_synthetic(**args)
            self.assertEqual(call_count,[])
            marker.unlink()
            (directory/'standalone_manifest.json').write_bytes(b'{}\n')
            with self.assertRaises(ValueError):score_verified_synthetic(**args)
            self.assertEqual(call_count,[])

    def test_outcome_identity_and_rank_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p,run_id,directory,_=make_run(root,OZLOTTO,1478,'testscoresid004')
            args=dict(run_dir=directory,run_id=run_id,profile=p,
                method_id='E_1',variant_id='FULL_HISTORY_RAW_COUNTS_V1',
                target=1478,global_orphan_marker=root/'UNRESOLVED_ORPHAN.json')
            for wrong in (
                {**synthetic_outcome(p,1478),'game_id':'POWERBALL'},
                {**synthetic_outcome(p,1478),'draw_number':1479},
                {**synthetic_outcome(p,1478),'draw_key':'POWERBALL_1478'},
                {**synthetic_outcome(p,1478),'barrels':{'MAIN':[1,1,1,1,1,1,1]}},
                {**synthetic_outcome(p,1478),'barrels':{'MAIN':list(range(41,48)),'POWERBALL':[1]}},
            ):
                with self.subTest(wrong=wrong.get('draw_key')):
                    with self.assertRaises(ValueError):
                        score_verified_synthetic(**args,outcome_loader=lambda w=wrong:w)

if __name__=='__main__':unittest.main()
