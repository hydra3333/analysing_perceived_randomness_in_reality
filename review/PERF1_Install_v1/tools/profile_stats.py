"""Profile WF-1B's statistics stage (report step 8: N1 runner + measures) at full size on INVENTED data only.
Usage: PYTHONPATH=src:src/methods python3 profile_stats.py GAME [R]   (run from a WF-1B dev tree)"""
import cProfile, pstats, random, sys, time
from collections import Counter
from evaluation import n1 as N1, measures as MS, divisions as DV, collect as COL, report as RP
from evaluation.report import track_id

GAME = sys.argv[1]
R = int(sys.argv[2]) if len(sys.argv) > 2 else 10_000
N1.R = R
FIRST, LAST = (1286, 1576) if GAME == 'POWERBALL' else (1474, 1693)
POOL = DV.MAIN_POOL[GAME]
rng = random.Random(12345)
targets = list(range(FIRST, LAST + 1))
outcomes = {}
for t in targets:                                    # invented draws
    if GAME == 'POWERBALL':
        outcomes[t] = (tuple(sorted(rng.sample(range(1, 36), 7))), rng.randint(1, 20))
    else:
        s = rng.sample(range(1, 48), 10)
        outcomes[t] = (tuple(sorted(s[:7])), tuple(sorted(s[7:])))
per_track, per_variant = {}, {}
for v in range(40):                                  # 40 invented variants
    key = (f'E_{v + 1}', 'V01')
    rgroups, rrows = {}, []
    for t in targets:
        order = rng.sample(range(1, POOL + 1), POOL)
        g = {'MAIN': [[x] for x in order]}
        if GAME == 'POWERBALL':
            g['POWERBALL'] = [[x] for x in rng.sample(range(1, 21), 20)]
        rgroups[t] = g
        dmain, extra = outcomes[t]
        rrows.append({'draw_number': t, **MS.mr5_target_fields(
            GAME, MS.mid_ranks_from_groups(g['MAIN'], POOL), dmain,
            *((MS.mid_ranks_from_groups(g['POWERBALL'], DV.PB_POOL), extra) if GAME == 'POWERBALL' else ()))})
    per_variant[key] = {'targets': rrows, 'status': 'GRID_COMPLETE', 'invalid': {}, 'groups': rgroups}
    for ro in COL.READOUTS:
        rows, entries = [], {}
        for t in targets:
            order = [x[0] for x in rgroups[t]['MAIN']]
            tmain = tuple(sorted(order[:7] if ro == 'TOP' else order[-7:]))
            tpb = rgroups[t]['POWERBALL'][0][0] if GAME == 'POWERBALL' else None
            dmain, extra = outcomes[t]
            rows.append({'draw_number': t, **DV.match_record(GAME, tmain, tpb, dmain, extra)})
            entries[t] = (tmain, tpb)
        per_track[(*key, ro)] = {'targets': rows, 'status': 'GRID_COMPLETE', 'invalid': {},
                                 'track_id': track_id(GAME, *key, ro, 'WF'), 'entries': entries}
fams = RP.load_families(GAME, FIRST, LAST)
roster = sorted(tr['track_id'] for tr in per_track.values())
families = [dict(f, roster=roster) for f in fams]
policy = {'policy_id': 'N1_ROOT_TEST_ONLY_V1', 'output_value': 'AB' * 64}
print(f'{GAME}: {len(per_track)} tracks, {len(per_variant)} variants, {len(targets)} targets, R={R}, '
      f'{len(families)} families', flush=True)

def stage():
    t0 = time.time()
    n1 = N1.runner(policy)(GAME, per_track, per_variant, families)
    t1 = time.time()
    for (mid, vid, ro), tr in per_track.items():
        for name in RP.READOUT_MEASURES:
            kw = {'invalid_cells': tr['invalid']}
            if name == 'MR1':
                kw['n1'] = n1['mr1'].get((mid, vid, ro))
            getattr(MS, name.lower())(GAME, tr['targets'], tr['status'], **kw)
    for key, vr in per_variant.items():
        MS.mr5(GAME, vr['targets'], vr['status'], invalid_cells=vr['invalid'], n1=n1['mr5'].get(key))
    t2 = time.time()
    print(f'N1 runner {t1 - t0:.1f} s; measures {t2 - t1:.1f} s', flush=True)

pr = cProfile.Profile()
pr.enable(); stage(); pr.disable()
st = pstats.Stats(pr); st.sort_stats('cumulative').print_stats(25); st.sort_stats('tottime').print_stats(15)
