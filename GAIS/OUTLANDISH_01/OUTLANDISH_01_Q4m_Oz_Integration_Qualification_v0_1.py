#!/usr/bin/env python3
"""Q4m: ONE shared-stack synthetic Oz D6 end-to-end qualification.

Six fabricated packed sources, three fabricated Oz draws, same Q3 scanner,
Q4h runner/reporter/aggregate, 10,000 common shuffles, Holm 18.
No genuine Oz history, G: source, production scan or NULL computation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4c_Synthetic_Processing_Qualification_v0_1 as F
import OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1 as Old
import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S
import OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1 as P
import OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1 as R
import OUTLANDISH_01_Q4h_Powerball_Test_Aggregate_v0_1 as A
import OUTLANDISH_01_Q4i_Mode_v0_1 as M
import OUTLANDISH_01_Q4i_Production_Entry_v0_1 as Entry


def refuses(label, fn):
    try:
        fn()
    except (ValueError, FileNotFoundError, FileExistsError, PermissionError, RuntimeError):
        return 1
    raise AssertionError('missing guard refusal: ' + label)


def make_sources(roots, n):
    """Three views in three consecutive fabricated draws; distinct source receipts."""
    rows = G.validate_drawset(Old._historical_profile(roots, 'oz')).draw_rows
    logical = bytearray(b'9' * n)
    for j, (_draw, vals) in enumerate(rows):
        mains, supplements = vals[:7], vals[7:]
        placements = (
            (1000 + j*113, mains),             # O1 K7
            (2200 + j*137, (*mains[:6], supplements[0])),  # O2 K7mix
            (3500 + j*149, mains[:6]),         # O3 K6
        )
        for start, chosen in placements:
            token = ''.join(f'{v:02d}' for v in chosen).encode('ascii')
            logical[start:start+len(token)] = token
    seen = set()
    for i, const in enumerate(S.CONSTANTS):
        own = bytearray(logical)
        own[9000 + i] = ord(str(i))  # six distinct byte-accurate fixture sources
        binary = bytes.fromhex((bytes(own) + b'0').decode('ascii'))
        path = roots.published_binary(const)
        path.write_bytes(binary)
        plan = G.sample_plan(len(binary))
        receipt = {
            'format': G.FORMAT, 'format_version': 1, 'scope': G.SCOPE,
            'constant': const, 'binary_name': path.name,
            'digits_including_integer': n, 'packed_bytes': len(binary),
            'binary_sha256_streamed': hashlib.sha256(binary).hexdigest(),
            'sample_block_length': plan[0][1],
            'samples': [{'offset_bytes': x, 'size': length,
                         'sha256': hashlib.sha256(binary[x:x+length]).hexdigest()}
                        for x,length in plan],
        }
        roots.receipt(const).write_bytes(
            (json.dumps(receipt,sort_keys=True)+'\n').encode('ascii'))
        result = G.validate_published_source(roots, const, fixture_digits=n)
        assert result.packed_sha256 == receipt['binary_sha256_streamed']
        seen.add(result.packed_sha256)
    assert len(seen) == len(S.CONSTANTS)


def run():
    assert Entry.ENABLE_OZ_PRODUCTION_SCANS is False
    assert Entry.ENABLE_Q5_PRODUCTION_SCANS is False
    refusals = 0
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q4M_OZ_SYNTHETIC_') as tmp:
        roots, n = F.make_temp(Path(tmp))
        profile = Old._historical_profile(roots, 'oz')
        mode = M.PowerballMode.synthetic(roots, profile, n, game='oz')
        assert mode.game == 'oz'
        refusals += refuses('cannot label Oz fixture as Powerball', lambda:
            M.PowerballMode.synthetic(roots, profile, n, game='powerball'))
        refusals += refuses('cannot create cross-game Oz run ID', lambda:
            P.run_powerball(mode, 'pi', 'TEST_REAL_powerball_wrong', chunk_bytes=9))
        make_sources(roots, n)
        roster = {}
        raw = {}
        for const in S.CONSTANTS:
            rid = f'TEST_REAL_oz_{const}_q4m'
            P.run_powerball(mode, const, rid, chunk_bytes=9)
            saved, _, _, events, classes = P.load_run(mode, const, rid)
            assert saved['game']=='oz' and saved['status']=='COMPLETE'
            assert len(events)>0 and len(classes)==len(events)
            R.create_report(mode, const, rid)
            rep = R.load_report(mode, const, rid)['report']
            assert rep['game']=='oz' and rep['primary_statistic']==S.OZ_D6_PRIMARY
            assert rep['primary_views']==list(S.OZ_D6_VIEWS)
            assert rep['secondary_statistic'] is None
            assert rep['permutation']['iterations_requested']==10_000
            for view in S.OZ_D6_VIEWS:
                d = rep['permutation']['views'][view]
                assert d['event_view']==view and d['statistic']==S.OZ_D6_PRIMARY
                assert d['observed_evaluable_pairs']==2
                assert d['valid_permutations']==10_000
                raw[f'{const}:{view}'] = d['centered_two_sided_p']
                assert d['observed']==rep['transitions_summary'][view][
                    'observed_primary_mean_log10_gap_plus_one']
            assert R.audit_report(mode, const, rid)['science_matches']
            roster[const] = rid
            refusals += refuses('create-only Oz report',lambda const=const,rid=rid:
                               R.create_report(mode,const,rid))
        agg_id = 'TEST_REAL_AGGREGATE_oz_q4m_v1'
        A.create_aggregate(mode, agg_id, roster)
        agg = A.load_aggregate(mode, agg_id)
        assert agg['game']=='oz' and len(agg['holm_family'])==18
        assert agg['secondary_statistic'] is None
        expected = S.holm_adjusted(raw, agg['holm_family'])
        for const in S.CONSTANTS:
            for view in S.OZ_D6_VIEWS:
                observed=agg['per_constant'][const]['views'][view]
                assert observed['raw_primary_p']==raw[f'{const}:{view}']
                assert observed['holm_adjusted_p']==expected[f'{const}:{view}']
        refusals += refuses('cannot aggregate fewer than six',lambda:
                            A.compute_aggregate(mode,{'pi':roster['pi']}))
        refusals += refuses('cannot load Oz aggregate in PB mode',lambda:
                            A.load_aggregate(M.PowerballMode.synthetic(
                                roots,Old._historical_profile(roots,'powerball'),n),
                                agg_id))
        # Explicit N/A entry remains in 18-way Holm and is not silently dropped.
        raw_na = dict(raw)
        raw_na['pi:O1_any'] = None
        adj = S.holm_adjusted(raw_na, agg['holm_family'])
        assert adj['pi:O1_any'] is None and len(adj)==18
        all_empty = {v:((),(),()) for v in S.OZ_D6_VIEWS}
        empty = S.oz_three_family_permutation(all_empty, seed=1, iterations=8)
        assert all(empty['views'][v]['centered_two_sided_p'] is None
                   and empty['views'][v]['undefined_reason']==
                       'OBSERVED_NO_EVALUABLE_ADJACENT_PAIRS'
                   for v in S.OZ_D6_VIEWS)
        print(f'Q4M OZ SYNTHETIC INTEGRATION PASS: runs=6 reports=6 aggregates=1 '
              f'views=3 holm=18 shuffles-per-report=10000 guards={refusals} '
              'production-scans=0 REAL-history-reads=0')


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',action='store_true',required=True)
    opts=p.parse_args()
    run()
