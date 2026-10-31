"""WF-1B: one ranking report run, in the fixed order of design v0.1r1 section 6.1 (with the WF-1B supplement
v0.1r1, OWNER-RATIFIED 31 October 2026).

1. Refusals that read nothing: the orphan marker; the window (S >= E(G) + 1 is implied by the grid; L <= the last
   development draw; [S, L] inside the batch's own window); an unknown or altered batch; an unreadable family
   registry.
2. The fixed grid, from the plan alone (collect.grid).
3. The frozen forecasts (collect.collect), through the driver's attempt binding and read_run.
4. One RANKING_REPORT search-log row, BEFORE any outcome is read.
5. The scoring plan (create-only), BEFORE any outcome is read.
6. The outcomes of the grid's valid targets only (outcome_reader).
7. The score ledger and the rank-position ledger (create-only).
8. Measures, families, N1 (when an approved seed policy is installed) and the report files.

An invocation refused at step 1 appends nothing. Every invocation that passes step 3 has its row, whether or not it
reaches a report; a later failure never removes it.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import uuid
from collections import Counter
from fractions import Fraction
from pathlib import Path

import _common.contract_publication as CP
import _common.contract_runner as CR
import _common.contract_vocab as V
import _common.walk_forward as WF
from _common.contract_receipts import track_id, validate_score_record
from _common.contract_records import canonical, record_digest, sha256_hex
from _common.game_profiles import get_profile

from . import collect as COL
from . import divisions as DV
from . import measures as MS
from . import outcome_reader as OR

TOOL = 'Method_Rankings_Report.py'
EVALUATOR_VERSION = 'WF1B_EVALUATOR_V1'
SCORING_PLAN_SCHEMA = 'SCORING_PLAN_V1'
RANK_SCHEMA = 'RANK_POSITION_RECORD_V1'
ATTEMPT = 'rr-'
REGISTRY_DIR = Path(__file__).resolve().parent / 'registry'
READOUT_MEASURES = ('MR0', 'MR1', 'MR4', 'MR7', 'MR16')     # looked up in `measures` at call time
STAGE2 = 'MR0,MR1,MR1-T,MR4,MR5,MR7,MR16'


class ReportRefused(Exception):
    """Refused at step 1: nothing was read beyond the plan and registries, and nothing was written."""


def tool_sha256() -> str:
    """SHA-256 of the evaluation package's sources (LF), in name order: the report's tool provenance."""
    h = hashlib.sha256()
    for p in sorted(Path(__file__).resolve().parent.glob('*.py')):
        h.update(p.name.encode('ascii') + b'\0' + p.read_bytes().replace(b'\r\n', b'\n') + b'\0')
    return h.hexdigest()


def frac(x) -> str | None:
    """Exact rational as text ('a/b' or 'a'), for records; None stays None."""
    return None if x is None else str(Fraction(x))


def roots() -> dict:
    project = Path(CR.PROJECT_ROOT)
    return {'project': project, 'scores': project / 'results' / 'real' / 'development' / 'scores',
            'reports': project / 'results' / 'method_rankings', 'search_log': WF.roots()['search_log']}


def load_families(game_id: str, first: int, last: int) -> list[dict]:
    """The registered families that apply: same game and exactly the family's window (design 6.7)."""
    reg = json.loads((REGISTRY_DIR / 'FAMILY_REGISTRY_V1.json').read_bytes().decode('ascii'))
    if reg.get('schema') != 'FAMILY_REGISTRY_V1':
        raise ReportRefused('the family registry is not FAMILY_REGISTRY_V1')
    return [f for f in reg['families'] if f['game_id'] == game_id and (f['window_first'], f['window_last']) == (first, last)]


def search_rows(game_id: str | None = None) -> list[dict]:
    path = roots()['search_log']
    if not path.is_file():
        return []
    rows = list(csv.DictReader(io.StringIO(path.read_bytes().decode('ascii'))))
    return [r for r in rows if game_id is None or r.get('game_id') == game_id]


def declared_tests(game_id: str, n_tracks: int, n_variants: int) -> int:
    """The number of local tests the report shows (fixed before outcomes): per readout track, every sub-measure that
    carries a significance figure and counts in M (MR0 and MR1-T are descriptive only; MR16's repeated tests do not
    count again); per variant, MR5's channels."""
    per_track = 0
    for name in READOUT_MEASURES:
        for sid, sub in getattr(MS, name.lower())(game_id, [], 'GRID_EMPTY')['sub_measures'].items():
            if sid in ('MR0', 'MR1-T') or sub.get('counts_in_M') is False:
                continue
            per_track += 1
    per_variant = len(MS.mr5(game_id, [], 'GRID_EMPTY')['sub_measures'])
    return n_tracks * per_track + n_variants * per_variant


def run_report(game_id: str, batch_id: str, first: int, last: int, *, echo=print, n1_runner=None) -> dict:
    """Steps 1-7 of design 6.1 and the measures; returns everything the report writer needs. Raises ReportRefused
    at step 1 (nothing appended). Any later exception leaves the search-log row in place."""
    # ---------------------------------------------------------------- step 1: refusals that read nothing
    m = Path(CR.ORPHAN_MARKER)
    if m.exists() or m.is_symlink():
        raise ReportRefused('UNRESOLVED_ORPHAN_MARKER: no experiment or report is permitted')
    p = get_profile(game_id)
    if type(first) is not int or type(last) is not int or first > last:
        raise ReportRefused('the window must be two whole draw numbers, first <= last')
    if first < p.first_draw:
        raise ReportRefused(f'first must be at least {p.first_draw} (S >= E(G), R3 17.3.6)')
    if last > p.holdout_first - 1:
        raise ReportRefused(f'last must be at most {p.holdout_first - 1} in this phase (R3 17.3.6; MRT-14)')
    try:
        plan = WF.load_plan(game_id, batch_id)
    except WF.BatchRefused as exc:
        raise ReportRefused(f'unknown or altered batch: {exc}') from None
    if first < plan['window_first'] - (1 if plan['window_first'] == p.first_draw + 1 else 0) or last > plan['window_last']:
        raise ReportRefused(f"the window [{first}, {last}] is outside the batch's window "
                            f"[{plan['window_first']}, {plan['window_last']}]")
    families = load_families(game_id, first, last)

    # ---------------------------------------------------------------- steps 2-3: grid and frozen forecasts
    collected = COL.collect(plan, first, last)
    members = plan['cohort']
    tracks = [(mem, ro) for mem in members for ro in COL.READOUTS]
    grid_digest = sha256_hex(canonical({'grids': [[k[0], k[1], g] for k, g in sorted(collected['grids'].items())]}))
    selected = sorted([k[0], k[1], k[2], c['forecast_content_digest'], c['freeze_receipt_digest']]
                      for k, c in collected['cells'].items() if c['valid'])
    availability = Counter(c['reason'] if not c['valid'] else 'VALID' for c in collected['cells'].values())
    tests = declared_tests(game_id, len(tracks), len(members))
    attempt_id = ATTEMPT + uuid.uuid4().hex
    scoring_run_id = attempt_id
    scoring_plan = {'schema': SCORING_PLAN_SCHEMA, 'attempt_id': attempt_id, 'game_id': game_id, 'mode': 'WF',
                    'batch_id': batch_id, 'window_first': first, 'window_last': last,
                    'plan_digest': record_digest(plan), 'cohort_digest': plan['cohort_digest'],
                    'grid_digest': grid_digest, 'family_ids': [f['family_id'] for f in families],
                    'measures': STAGE2, 'declared_tests': tests, 'selected_forecasts': selected,
                    'availability': dict(sorted(availability.items())), 'evaluator_version': EVALUATOR_VERSION,
                    'receipt_selection_policy': 'EARLIEST_FROZEN_AT_UTC_EQUAL_CONTENT_DIGESTS'}
    sp_digest = record_digest(scoring_plan)

    # ---------------------------------------------------------------- step 4: the search-log row (before outcomes)
    row = WF._append_search_row({'row_type': 'RANKING_REPORT', 'utc': CP.utc_now(), 'game_id': game_id, 'mode': 'WF',
                                 'window_first': first, 'window_last': last, 'cohort_size': len(tracks),
                                 'cohort_digest': plan['cohort_digest'],
                                 'family_ids': ';'.join(f['family_id'] for f in families), 'test_count': tests,
                                 'measures': STAGE2, 'batch_id': batch_id, 'attempt_id': attempt_id,
                                 'plan_digest': sp_digest, 'tool': TOOL, 'tool_version': EVALUATOR_VERSION,
                                 'tool_sha256': tool_sha256()})
    scoring_plan_record = dict(scoring_plan, search_log_row=row)

    # ---------------------------------------------------------------- step 5: the scoring plan (before outcomes)
    folder = roots()['scores'] / game_id / batch_id / scoring_run_id
    folder.mkdir(parents=True, exist_ok=False)
    CP.create_only(folder / 'scoring_plan.json', canonical(scoring_plan_record))

    # ---------------------------------------------------------------- step 6: the outcomes of valid grid targets only
    targets = sorted({k[2] for k, c in collected['cells'].items() if c['valid']})
    outcomes = OR.read_outcomes(repo_root=roots()['project'], game_id=game_id,
                                master_sha256=plan['master_sha256'], targets=targets) if targets else {}

    # ---------------------------------------------------------------- step 7: the ledgers (create-only)
    scores, ranks = [], []
    per_track, per_variant = {}, {}
    for mem in members:
        key = (mem['method_id'], mem['variant_id'])
        for ro in COL.READOUTS:
            valid, invalid = COL.track_cells(collected, *key, ro)
            tid = track_id(game_id, *key, ro, 'WF')
            rows, entries = [], {}
            for t in valid:
                c = collected['cells'][(*key, t)]
                tmain, tpb = c['entries'][ro]
                dmain, extra = outcomes[t]
                mr = DV.match_record(game_id, tmain, tpb, dmain, extra)      # supplementaries end here (R2 2.5)
                rec = {'schema': V.SCORE, 'game_id': game_id, 'draw_number': t, 'track_id': tid, 'mode': 'WF',
                       'method_revision': c['method_revision'], 'forecast_content_digest': c['forecast_content_digest'],
                       'freeze_receipt_digest': c['freeze_receipt_digest'], 'drawn_main': list(dmain),
                       **({'drawn_powerball': extra} if game_id == 'POWERBALL' else {}),
                       **mr, 'evaluator_version': EVALUATOR_VERSION}
                validate_score_record(rec)
                scores.append(rec)
                rows.append({'draw_number': t, **mr})
                entries[t] = (tmain, tpb)
            per_track[(*key, ro)] = {'targets': rows, 'status': COL.track_status(valid, invalid),
                                     'invalid': dict(invalid), 'track_id': tid, 'entries': entries}
        # MR5: the method-variant ranking (one per variant; R3 17.3.4A)
        rrows, rinvalid, rgroups = [], Counter(), {}
        for t in collected['grids'][key]:
            c = collected['cells'][(*key, t)]
            groups = c.get('ranked_groups') or {}
            if not c['valid']:
                rinvalid[c['reason']] += 1
                continue
            if groups.get('MAIN') is None or (game_id == 'POWERBALL' and groups.get('POWERBALL') is None):
                rinvalid['RANKING_UNAVAILABLE'] += 1
                continue
            dmain, extra = outcomes[t]
            fields = MS.mr5_target_fields(
                game_id, MS.mid_ranks_from_groups(groups['MAIN'], DV.MAIN_POOL[game_id]), dmain,
                *((MS.mid_ranks_from_groups(groups['POWERBALL'], DV.PB_POOL), extra) if game_id == 'POWERBALL' else ()))
            ranks.append({'schema': RANK_SCHEMA, 'game_id': game_id, 'draw_number': t, 'method_id': key[0],
                          'variant_id': key[1], 'mode': 'WF', 'method_revision': c['method_revision'],
                          'forecast_content_digest': c['forecast_content_digest'],
                          'freeze_receipt_digest': c['freeze_receipt_digest'],
                          **{k: frac(v) for k, v in fields.items()}, 'evaluator_version': EVALUATOR_VERSION})
            rrows.append({'draw_number': t, **fields})
            rgroups[t] = groups
        per_variant[key] = {'targets': rrows, 'status': COL.track_status(rrows, rinvalid), 'invalid': dict(rinvalid),
                            'groups': rgroups}
    keys = [(s['track_id'], s['draw_number'], s['method_revision'], s['forecast_content_digest'],
             s['freeze_receipt_digest'], s['evaluator_version']) for s in scores]
    if len(set(keys)) != len(keys):                                  # E2R-R45A create-only key, within the ledger
        raise RuntimeError('duplicate score-record key inside one ledger')
    CP.create_only(folder / 'score_ledger.jsonl', b''.join(canonical(s) for s in scores))   # each ends with \n
    CP.create_only(folder / 'rank_ledger.jsonl', b''.join(canonical(r) for r in ranks))

    # ---------------------------------------------------------------- step 8: measures (N1 optional)
    n1 = n1_runner(game_id, per_track, per_variant, families) if n1_runner is not None else None
    results = {}
    for (mid, vid, ro), tr in per_track.items():
        res = {}
        for name in READOUT_MEASURES:
            fn = getattr(MS, name.lower())
            kw = {'invalid_cells': tr['invalid']}
            if name == 'MR1' and n1 is not None:
                kw['n1'] = n1['mr1'].get((mid, vid, ro))
            res[name] = fn(game_id, tr['targets'], tr['status'], **kw)
        results[(mid, vid, ro)] = res
    var_results = {}
    for key, vr in per_variant.items():
        kw = {'invalid_cells': vr['invalid']}
        if n1 is not None:
            kw['n1'] = n1['mr5'].get(key)
        var_results[key] = MS.mr5(game_id, vr['targets'], vr['status'], **kw)
    return {'plan': plan, 'families': families, 'collected': collected, 'per_track': per_track,
            'per_variant': per_variant, 'results': results, 'var_results': var_results, 'n1': n1,
            'attempt_id': attempt_id, 'search_log_row': row, 'scoring_plan': scoring_plan_record,
            'scoring_plan_digest': sp_digest, 'scores_folder': folder, 'declared_tests': tests,
            'grid_digest': grid_digest, 'first': first, 'last': last, 'game_id': game_id}
