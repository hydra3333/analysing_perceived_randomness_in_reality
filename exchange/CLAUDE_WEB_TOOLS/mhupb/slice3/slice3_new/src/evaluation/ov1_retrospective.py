"""MHUP-B layer L7: the RETROSPECTIVE OV-1 view (the owner's decision of 18 November 2026; EX_235 section 2 B; the change
note OWNER_CLARIFICATION_2026_11_18_EQUAL_DRAWS_AND_OV1_USES). A DERIVED part of the consolidated report.

    OV-1 RETROSPECTIVE WALK-FORWARD - DESCRIPTIVE, NOT FORMAL PROSPECTIVE

It applies the same exact arithmetic as the registered formal test (the kernel ov1_numeric: the exact fair-draw
distribution of X, certified factors that are never inflated, the six lambdas with equal weights, exact running sums)
to forecasts ALREADY SCORED by the league's summed sources: the canonical development attempts (which include every
re-forecast former holdout draw) and the weekly score ledger. It is the per-game ENSEMBLE of OV-1 (w_j = TOP minus
WORST over the cohort's variants with a complete pair for that draw), not a test per method.

What it is not. It is not the registered test and is never written to the formal OV-1 ledger, which this module does
not open. Its cohort, window and methods were chosen with the results known, so the registered false-alarm guarantee
does not carry over: it gives NO P value, and 40 is drawn as a reference line only. The games are never combined.

Inputs, all by identity: the tickets come from the frozen forecasts the summed sources scored (read again here, read-
only); the numbers drawn are quoted from the accepted score records themselves, so no result file and no outcome reader
is opened. X is computed twice (from the tickets' weights and from the scored matches) and the two must agree.
A cohort member with no scored pair for a draw contributes nothing to that draw and is counted as such, never guessed.
"""
from __future__ import annotations

from pathlib import Path

import _common.walk_forward as WF
import _common.weekly_records as WR
from _common.contract_records import record_digest

from . import collect as COL
from . import league_sources as LS
from . import ov1_numeric as NUM

LABEL = 'OV-1 RETROSPECTIVE WALK-FORWARD - DESCRIPTIVE, NOT FORMAL PROSPECTIVE'
VIEW_VERSION = 'MHUPB_OV1_RETROSPECTIVE_V1'
SCOPES = {'CURRENT': 'CURRENT_RELEASED_VARIANTS', 'ALL': 'EVERY_SCORED_IDENTITY'}
REFERENCE = NUM.BAR
STATEMENT = ('Descriptive only. This is not the registered formal test: the cohort, the window and the methods were '
             'chosen with the results known, so the registered false-alarm guarantee does not apply. No P value is '
             f'given. The line at {REFERENCE} is a reference only. Nothing here is written to the formal OV-1 ledger. '
             'The games are never combined.')


class RetroRefused(Exception):
    """The view cannot be computed from the records as they stand; the message names what disagrees or is missing."""


def weekly_evidence(root: Path, game_id: str) -> dict:
    """(method, revision, variant, target) -> the frozen forecast of every FORECAST record a freeze line names, each
    verified against its session, ticket and run folder (weekly_records.verify_named_records)."""
    out = {}
    try:
        for line in WR.forecast_ledger(root, game_id):
            for ev in WR.verify_named_records(root, game_id, line):
                r = ev['named']
                if r['record_kind'] == 'FORECAST':
                    out[(r['method_id'], r['method_revision'], r['variant_id'], line['target_draw_number'])] = ev['forecast']
    except WR.RecordRefused as exc:
        raise RetroRefused(f'the weekly records do not verify: {exc}') from None
    return out


def tickets(root: Path, game_id: str, data: dict, evidence: dict | None = None) -> dict:
    """(method, revision, variant, target) -> (TOP numbers, WORST numbers), for the forecasts the summed sources scored
    that give both tickets: from each available listed attempt (the forecast its scoring plan selected) and from the
    weekly freeze lines."""
    out = {}
    gone = {n['source'] for n in data['not_available']}
    for e in data['sources']:
        if e['attempt_id'] in gone:
            continue
        try:
            plan = WF.load_plan(game_id, e['batch_id'])
            sp = LS.canonical_file(LS.scores_folder(game_id, e['batch_id'], e['attempt_id']) / 'scoring_plan.json',
                                   f'scoring plan of {e["attempt_id"]}')
        except (WF.BatchRefused, LS.LeagueRefused) as exc:
            raise RetroRefused(f'{e["attempt_id"]}: {exc}') from None
        selected = {(s[0], s[1], s[2]): s[3] for s in sp['selected_forecasts']}
        for (method, variant, t), cell in COL.collect(plan, e['window_first'], e['window_last'])['cells'].items():
            if cell['valid'] and selected.get((method, variant, t)) == cell['forecast_content_digest'] and \
                    set(cell['entries']) == {'TOP', 'WORST'}:
                out[(method, cell['method_revision'], variant, t)] = (cell['entries']['TOP'][0], cell['entries']['WORST'][0])
    for key, forecast in (weekly_evidence(root, game_id) if evidence is None else evidence).items():
        pair = [COL._entry(forecast, readout, game_id)[0] for readout in ('TOP', 'WORST')]
        if pair[0] is not None and pair[1] is not None:
            out[key] = (pair[0][0], pair[1][0])
    return out


def view(root: Path, game_id: str, data: dict, *, cohort='CURRENT', first: int | None = None, last: int | None = None,
         evidence: dict | None = None) -> dict:
    """The retrospective series over the summed sources in `data` (league_sources.collect). `cohort` is 'CURRENT' (the
    released, unretired variants), 'ALL' (every scored identity, each revision its own member) or a list of
    [method, revision, variant]. Pure given the records: the same inputs give the same result."""
    n = WR.MAIN_POOL[game_id]
    pairs: dict[tuple, dict] = {}
    for r in data['rows']:
        pairs.setdefault((r['method'], r['revision'], r['variant'], r['target']), {})[r['readout']] = r
    complete = {k: p for k, p in pairs.items() if len(p) == 2}
    scored = sorted({k[:3] for k in complete})
    if cohort == 'CURRENT':
        members = sorted(tuple(r[:3]) for r in data['roster'] if r[4] == 'CURRENT')
    elif cohort == 'ALL':
        members = scored
    else:
        members = sorted({tuple(c) for c in cohort})
        known = {tuple(r[:3]) for r in data['roster']} | set(scored)
        if not members or any(len(m) != 3 or m not in known for m in members):
            raise RetroRefused('the named cohort holds an identity that is neither released nor scored')
    scope = SCOPES.get(cohort, 'NAMED_LIST') if isinstance(cohort, str) else 'NAMED_LIST'
    inside = lambda t: (first is None or t >= first) and (last is None or t <= last)
    by_target: dict[int, list] = {}
    for k in complete:
        if k[:3] in set(members) and inside(k[3]):
            by_target.setdefault(k[3], []).append(k)
    have = tickets(root, game_id, data, evidence)
    sums = [0] * len(NUM.LAMBDAS)
    series, counted, skipped, first_at, peak = [], 0, 0, None, NUM.mixture_lower(sums)
    per_member = {m: 0 for m in members}
    for t in sorted(by_target):
        here = sorted(by_target[t])
        w, x_matches, drawn = [0] * n, 0, None
        for k in here:
            if k not in have:
                raise RetroRefused(f'the scored pair {k} has no frozen forecast giving both tickets')
            for labels, sign in zip(have[k], (1, -1)):
                if len(labels) != NUM.K or len(set(labels)) != NUM.K or not all(type(j) is int and 1 <= j <= n for j in labels):
                    raise RetroRefused(f'a frozen ticket of {k} is not seven different numbers of the main barrel')
                for j in labels:
                    w[j - 1] += sign
            top, worst = complete[k]['TOP'], complete[k]['WORST']
            x_matches += top['main'] - worst['main']
            for row in (top, worst):
                if drawn is None:
                    drawn = list(row['drawn_main'])
                elif drawn != list(row['drawn_main']):
                    raise RetroRefused(f'draw {t}: the score records disagree about the numbers drawn')
            per_member[k[:3]] += 1
        x = sum(w[d - 1] for d in drawn)
        if x != x_matches:
            raise RetroRefused(f'draw {t}: X by the tickets\' weights is {x}, by the scored matches {x_matches}; they must agree')
        try:
            table = NUM.factor_table(w)
            if table is None:
                skipped += 1
                state, z = 'V0_SKIPPED', None
            else:
                if x not in table['counts']:
                    raise RetroRefused(f'draw {t}: X = {x} is not a value these weights can give')
                sums = [a + row[x] for a, row in zip(sums, table['rows'])]
                counted += 1
                state, z = 'COUNTED', NUM.z_text(x, *table['variance'])
            value, at = NUM.mixture_lower(sums), NUM.crossing(sums)
        except NUM.Refuse as exc:
            raise RetroRefused(f'draw {t}: the kernel refuses: {exc}') from None
        peak = max(peak, value)
        if at and first_at is None:
            first_at = t
        series.append({'target': t, 'pairs': len(here), 'cohort_without_pair': len(members) - len(here), 'state': state,
                       'x': x, 'z': z, 'score_text': NUM.fixed_text(value), 'at_or_above_reference': at})
    identity = {'view_version': VIEW_VERSION, 'kernel_version': NUM.KERNEL_VERSION, 'game_id': game_id,
                'cohort_scope': scope, 'cohort': [list(m) for m in members], 'window': [first, last],
                'lambdas': [list(x) for x in NUM.LAMBDAS], 'inputs': data['pins']}
    return {'label': LABEL, 'statement': STATEMENT, 'game_id': game_id, 'identity': identity,
            'identity_digest': record_digest(identity), 'cohort_scope': scope,
            'cohort': [{'method': m[0], 'revision': m[1], 'variant': m[2], 'pairs': per_member[m]} for m in members],
            'window': [first, last], 'targets': len(series), 'counted': counted, 'skipped_v0': skipped,
            'first_target': series[0]['target'] if series else None, 'last_target': series[-1]['target'] if series else None,
            'final_score_text': NUM.fixed_text(NUM.mixture_lower(sums)), 'highest_score_text': NUM.fixed_text(peak),
            'reference_line': REFERENCE, 'first_target_at_or_above_reference': first_at, 'series': series}


def lines(v: dict) -> list[str]:
    """The view as text: the label first, the statement, the identity, the totals, then the whole series."""
    out = [v['label'], f'{v["game_id"]}. {v["statement"]}', '',
           f'Cohort ({v["cohort_scope"]}): {len(v["cohort"])} variants, each revision its own member; window: '
           f'{"all scored draws" if v["window"] == [None, None] else v["window"]}; identity of this view '
           f'(cohort, window, inputs, kernel): {v["identity_digest"]}',
           f'Draws in the series: {v["targets"]} ({v["counted"]} counted, {v["skipped_v0"]} with all weights equal and '
           f'factor 1)' + (f', draws {v["first_target"]} to {v["last_target"]}' if v['targets'] else ''),
           f'Evidence score after the last draw (proved lower bound): {v["final_score_text"]}; highest in the series: '
           f'{v["highest_score_text"]}; reference line {v["reference_line"]}: ' +
           ('never reached' if v['first_target_at_or_above_reference'] is None else
            f'first reached at draw {v["first_target_at_or_above_reference"]} (an observation about history; not the '
            f'registered finding and not a P value)'), '',
           'Cohort members (scored pairs used):']
    out += [f'  {c["method"]} revision {c["revision"]} {c["variant"]}: {c["pairs"]}' +
            (' - NO SCORED PAIR IN THE WINDOW' if not c['pairs'] else '') for c in v['cohort']]
    out += ['', f'{"Draw":>6}  {"Pairs":>5}  {"Without":>7}  {"State":<10}  {"X":>5}  {"Z":>16}  Score after this draw']
    out += [f'{s["target"]:>6}  {s["pairs"]:>5}  {s["cohort_without_pair"]:>7}  {s["state"]:<10}  {s["x"]:>5}  '
            f'{s["z"] or "-":>16}  {s["score_text"]}{"  (at or above the reference line)" if s["at_or_above_reference"] else ""}'
            for s in v['series']]
    return out
