"""MHUP-B: named forecast content compared (design supplement v0.8 section 7.2 rule 7; code plan v0.3 section 5, L6).

A re-forecast of a holdout draw and the sealed Mode H forecast of the same variant and draw cannot be byte-identical:
their run modes differ, and the method contract's identity guarantee (E2R-1 7.1) holds within one run mode. So this
module compares NAMED FORECAST CONTENT ONLY: for each barrel, the ranking of the numbers with its scores and ties, and
the TOP and WORST sets; mode-specific fields are left out. For each pair it states which preconditions hold, lists
every difference and names the inputs by identity. The same comparison serves one development attempt against another.

Evaluator side. It reads frozen forecasts and their receipts through the batch kinds' own roots and writes nothing: no
sealed Mode H path, freeze line or ledger is opened for writing. A difference is information for the owner and the
reviewer, not automatically a fault, and it changes nothing in the sealed study.
"""
from __future__ import annotations

import _common.contract_publication as CP
import _common.owner_records as OR
import _common.walk_forward as WF
from _common.contract_records import record_digest
from _common.game_profiles import get_profile

from . import collect as COL

NOT_CHECKED = ('a method whose forecast does not depend on the run mode: NOT CHECKED by this tool (the method '
               'contract promises identical content only within one run mode)')


def _tie_versions(fc: dict):
    return sorted((b, (body.get('tie_identity') or {}).get('ranking_tie_readout_version'))
                  for b, body in fc.get('barrels', {}).items())


PRECONDITIONS = (
    ('the same method declaration', lambda fc, rc: fc.get('declaration_digest')),
    ('the same method revision and registry entry (the installed code\'s approval)',
     lambda fc, rc: (fc.get('method_revision'), rc.get('registry_entry_digest'))),
    ('the same observation view', lambda fc, rc: (fc.get('observation_view'), fc.get('include_dates'))),
    ('the same N-1 history (permitted view and training end)',
     lambda fc, rc: (fc.get('permitted_view_digest'), fc.get('training_last_draw_number'))),
    ('the same seed policy, seed identity and sampling model',
     lambda fc, rc: (fc.get('fit_seed_policy_id'), fc.get('fit_seed_identity'), fc.get('fit_sampling_model_version'))),
    ('the same tie-break version', lambda fc, rc: _tie_versions(fc)),
    ('the same environment', lambda fc, rc: rc.get('environment_identity')),
)


def named_content(fc: dict) -> dict:
    """The mode-free content of one forecast: its status and, per barrel, the ranking with scores and ties and the TOP
    and WORST selections."""
    out = {'record_status': fc.get('record_status'), 'barrels': {}}
    for b, body in sorted(fc.get('barrels', {}).items()):
        out['barrels'][b] = {
            'ranking_kind': body.get('ranking_kind'), 'ranking_status': body.get('ranking_status'),
            'ranking': body.get('ranking'), 'ranked_groups': body.get('ranked_groups'), 'scores': body.get('scores'),
            'score_direction': body.get('score_direction'),
            'top': {k: (body.get('top') or {}).get(k) for k in ('status', 'labels')},
            'worst': {k: (body.get('worst') or {}).get(k) for k in ('status', 'labels')}}
    return out


def differences(a: dict, b: dict) -> list[str]:
    """Every difference between two named contents, in words. Empty when they are equal."""
    out = []
    if a['record_status'] != b['record_status']:
        out.append(f"record status: {a['record_status']} against {b['record_status']}")
    for barrel in sorted(set(a['barrels']) | set(b['barrels'])):
        x, y = a['barrels'].get(barrel), b['barrels'].get(barrel)
        if x is None or y is None:
            out.append(f'{barrel}: present in one forecast only')
            continue
        for side in ('top', 'worst'):
            if x[side] != y[side]:
                out.append(f"{barrel} {side.upper()}: {x[side]['labels']} ({x[side]['status']}) against "
                           f"{y[side]['labels']} ({y[side]['status']})")
        if x['ranking'] != y['ranking']:
            if type(x['ranking']) is list and type(y['ranking']) is list and len(x['ranking']) == len(y['ranking']):
                at = next(i for i, (p, q) in enumerate(zip(x['ranking'], y['ranking'])) if p != q)
                moved = sum(1 for p, q in zip(x['ranking'], y['ranking']) if p != q)
                out.append(f'{barrel} ranking: {moved} position(s) differ, the first at position {at + 1} '
                           f"({x['ranking'][at]} against {y['ranking'][at]})")
            else:
                out.append(f'{barrel} ranking: not comparable position by position')
        if x['ranked_groups'] != y['ranked_groups']:
            out.append(f'{barrel} ties: the tie groups differ')
        if x['scores'] != y['scores']:
            if type(x['scores']) is list and type(y['scores']) is list and len(x['scores']) == len(y['scores']):
                out.append(f"{barrel} scores: {sum(1 for p, q in zip(x['scores'], y['scores']) if p != q)} label(s) differ")
            else:
                out.append(f'{barrel} scores: present or shaped differently')
        for k in ('ranking_kind', 'ranking_status', 'score_direction'):
            if x[k] != y[k]:
                out.append(f'{barrel} {k}: {x[k]} against {y[k]}')
    return out


def compare(a: dict, b: dict) -> dict:
    """a, b: {'forecast', 'receipt'} of the two records of one (variant, target)."""
    pre = [[name, pick(a['forecast'], a['receipt']) == pick(b['forecast'], b['receipt'])] for name, pick in PRECONDITIONS]
    diff = differences(named_content(a['forecast']), named_content(b['forecast']))
    return {'preconditions': pre, 'preconditions_hold': all(ok for _name, ok in pre), 'equal': not diff,
            'differences': diff}


def _record(plan: dict, cell: dict, method_id: str, variant_id: str):
    folder = WF.roots(WF.kind_of(plan))['runs'] / plan['game_id'] / method_id / variant_id / cell['run_id']
    fc, rc = COL._load(folder / CP.FILES['forecast']), COL._load(folder / CP.FILES['forecast_receipt'])
    if fc is None or rc is None:
        return None
    return {'forecast': fc, 'receipt': rc}


def compare_plans(plan_a: dict, collected_a: dict, plan_b: dict, collected_b: dict, keys) -> list[dict]:
    """One row per (method, variant, target) key: the two selected records compared, or why they were not."""
    rows = []
    for method_id, variant_id, target in keys:
        row = {'method_id': method_id, 'variant_id': variant_id, 'target_draw_number': target}
        ca, cb = collected_a['cells'].get((method_id, variant_id, target)), collected_b['cells'].get((method_id, variant_id, target))
        missing = [name for name, c in (('first', ca), ('second', cb)) if c is None or not c.get('valid')]
        if missing:
            why = '; '.join(f"{name}: {'no record in that batch' if c is None else c.get('reason')}"
                            for name, c in (('first', ca), ('second', cb)) if name in missing)
            rows.append({**row, 'status': 'NOT_COMPARED', 'why': why})
            continue
        a, b = _record(plan_a, ca, method_id, variant_id), _record(plan_b, cb, method_id, variant_id)
        if a is None or b is None:
            rows.append({**row, 'status': 'NOT_COMPARED', 'why': 'a selected record no longer reads as canonical bytes'})
            continue
        res = compare(a, b)
        rows.append({**row, 'status': 'IDENTICAL_CONTENT' if res['equal'] else 'DIFFERENT_CONTENT',
                     'first': {'run_id': ca['run_id'], 'content_digest': ca['forecast_content_digest'],
                               'run_mode': a['forecast'].get('run_mode'), 'master_sha256': a['receipt'].get('master_sha256')},
                     'second': {'run_id': cb['run_id'], 'content_digest': cb['forecast_content_digest'],
                                'run_mode': b['forecast'].get('run_mode'), 'master_sha256': b['receipt'].get('master_sha256')},
                     **res})
    return rows


def sealed_comparison(game_id: str, plan: dict, collected: dict, first: int, last: int) -> dict:
    """The comparison of a development batch's holdout re-forecasts (first) with the game's sealed Mode H forecasts
    (second), for the batch's pairs inside the report's window (rule 7). Reads only."""
    p = get_profile(game_id)
    keys = [(mem['method_id'], mem['variant_id'], t) for mem, t in WF.plan_pairs(plan)
            if first <= t <= last and p.holdout_first <= t <= p.holdout_last]
    out = {'against': 'the sealed Mode H forecasts', 'mode_h_batch_id': None, 'pairs': [], 'not_checked': NOT_CHECKED}
    if keys:
        try:
            rec = OR.batch_id_record(WF.roots('MODE_H_BATCH')['project'], game_id)
            sealed_plan = None if rec is None else WF.load_plan(game_id, rec['batch_id'])
        except (OR.RecordRefused, WF.BatchRefused) as exc:
            return {**out, 'unavailable': f'the Mode H plan does not load: {exc}', 'counts': {}}
        if sealed_plan is None:
            return {**out, 'unavailable': 'the game has no Mode H plan', 'counts': {}}
        out['mode_h_batch_id'] = sealed_plan['batch_id']
        out['mode_h_plan_digest'] = record_digest(sealed_plan)
        sealed = COL.collect(sealed_plan, p.holdout_first, p.holdout_last)
        out['pairs'] = compare_plans(plan, collected, sealed_plan, sealed, keys)
    counts = {}
    for row in out['pairs']:
        counts[row['status']] = counts.get(row['status'], 0) + 1
    out['counts'] = counts
    return out


def section_lines(result: dict) -> list[str]:
    """The report's section for one comparison."""
    out = ['', f"COMPARISON WITH {result['against'].upper()} (design supplement 7.2 rule 7)", '']
    out.append('Named forecast content only: the ranking with its scores and ties, and the TOP and WORST sets. The two '
               'records are never byte-identical (their run modes differ). A difference is information, not '
               'automatically a fault; nothing in the sealed study is changed, and nothing here is scored.')
    if result.get('unavailable'):
        out.append(f"Not available: {result['unavailable']}.")
        return out
    if not result['pairs']:
        out.append('No holdout target of this batch lies in the report\'s window: nothing to compare.')
        return out
    c = result['counts']
    out.append(f"Mode H batch {result['mode_h_batch_id']}. Pairs: {len(result['pairs'])}; identical content "
               f"{c.get('IDENTICAL_CONTENT', 0)}; different content {c.get('DIFFERENT_CONTENT', 0)}; not compared "
               f"{c.get('NOT_COMPARED', 0)}.")
    out.append(f"Precondition not covered: {result['not_checked']}.")
    for row in result['pairs']:
        who = f"{row['method_id']} {row['variant_id']} draw {row['target_draw_number']}"
        if row['status'] == 'NOT_COMPARED':
            out.append(f"- {who}: NOT COMPARED ({row['why']})")
            continue
        failed = [name for name, ok in row['preconditions'] if not ok]
        out.append(f"- {who}: {row['status']}; re-forecast {row['first']['run_id']} ({row['first']['content_digest'][:12]}...) "
                   f"against sealed {row['second']['run_id']} ({row['second']['content_digest'][:12]}...); preconditions "
                   + ('all hold' if not failed else 'NOT holding: ' + '; '.join(failed)))
        for d in row['differences']:
            out.append(f'    {d}')
    return out
