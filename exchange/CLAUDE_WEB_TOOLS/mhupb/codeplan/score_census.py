"""One-time census of the committed score records (OD-5): identities, counts and field names. Read-only."""
import csv, hashlib, io, json, sys
from pathlib import Path
from collections import Counter
root = Path(sys.argv[1])
def canon(rec): return (json.dumps(rec, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n').encode('ascii')
rows = list(csv.DictReader(io.StringIO((root / 'results/audit/SEARCH_LOG.csv').read_bytes().decode('ascii'))))
for kind, base in (('DEV', 'results/real/development/scores'), ('MODE_H', 'results/real/holdout/scores')):
    for folder in sorted((root / base).glob('*/*/*')):
        game, batch, attempt = folder.parts[-3:]
        print(f'--- {kind} {game} {batch[:11]}.. {attempt[:11]}..')
        sp_raw = (folder / 'scoring_plan.json').read_bytes(); sp = json.loads(sp_raw)
        body = {k: v for k, v in sp.items() if k != 'search_log_row'}
        dig = hashlib.sha256(canon(body)).hexdigest()
        row = rows[sp['search_log_row'] - 1]
        print('  scoring plan: canonical bytes', canon(sp) == sp_raw, '| search-log row', sp['search_log_row'], row['row_type'],
              '| row names this attempt', row['attempt_id'] == attempt, '| plan digest matches the row', row['plan_digest'] == dig)
        print('  plan fields:', sorted(sp))
        files = ['mode_h_score_ledger.jsonl'] if kind == 'MODE_H' else ['score_ledger.jsonl', 'rank_ledger.jsonl']
        for name in files:
            raw = (folder / name).read_bytes()
            lines = raw.split(b'\n'); assert lines[-1] == b''
            recs = [json.loads(l) for l in lines[:-1]]
            ok = all(canon(r) == l + b'\n' for r, l in zip(recs, lines))
            by = Counter(r['schema'] for r in recs)
            print(f'  {name}: {len(raw)} bytes, {len(recs)} lines, canonical {ok}, CR bytes {raw.count(bytes([13]))}, sha256 {hashlib.sha256(raw).hexdigest()}')
            for schema, n in by.items():
                keys = Counter(tuple(sorted(r)) for r in recs if r['schema'] == schema)
                print(f'    {schema}: {n} lines; field sets: {len(keys)}')
                for ks, c in keys.items(): print(f'      {c} x {list(ks)}')
            sc = [r for r in recs if r['schema'] == 'POST_OUTCOME_SCORE_RECORD_V1']
            if sc:
                keyset = {(r['track_id'], r['draw_number']) for r in sc}
                print(f'    score keys (track, draw): {len(keyset)} distinct of {len(sc)}; draws {min(r["draw_number"] for r in sc)}-{max(r["draw_number"] for r in sc)}; '
                      f'tracks {len({r["track_id"] for r in sc})}; revisions {sorted({r["method_revision"] for r in sc})}; evaluator {sorted({r["evaluator_version"] for r in sc})}; '
                      f'exposure flags {sum(1 for r in sc if "exposure_flag" in r)}; a track id: {sc[0]["track_id"]}')
        if kind == 'MODE_H':
            m = root / 'results/real/holdout/wf_batches' / game / batch
            done = json.loads((m / 'SCORE_COMPLETE.json').read_bytes()); seal = json.loads((m / 'MODE_H_SEALED.json').read_bytes())
            h = hashlib.sha256((folder / 'mode_h_score_ledger.jsonl').read_bytes()).hexdigest()
            print('  SCORE_COMPLETE names this ledger:', done['score_ledger_sha256'] == h, '| lines', done['lines'], '| seal names it:', seal['score_ledger_sha256'] == h,
                  '| attempt', done['attempt_id'] == attempt)
