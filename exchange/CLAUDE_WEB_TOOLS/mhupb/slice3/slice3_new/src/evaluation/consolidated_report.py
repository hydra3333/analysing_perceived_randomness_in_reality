"""MHUP-B layer L7: the consolidated (weekly) report and the retired-revision index (design v0.1r7 section 6.6; design
supplement v0.8 section 8; code plan v0.3 L7, as changed by the owner's clarification of 18 November 2026).

Parts, each from named sources by identity. NOTHING IS POOLED INTO A P VALUE, and the games are never combined:

 1. the league table: the latest published one, quoted byte for byte from the archive (this tool publishes nothing);
 2. OV-1 FORMAL PROSPECTIVE (REGISTERED): the registered test's state, read from its own ledger;
 3. OV-1 RETROSPECTIVE WALK-FORWARD - DESCRIPTIVE, NOT FORMAL PROSPECTIVE: derived here (ov1_retrospective);
 4. the forward and the catch-up tables, under the heading "secondary", labelled EXPLORATORY_COHORT (their window and
    roster grow from report to report, so they are not a family fixed in advance; EX_223 CP-Q4): WF-1B's measure
    functions, unchanged, over the weekly score lines of class PROSPECTIVE and of class CATCH_UP, kept apart. Local
    figures keep their own labels and LOW_N. No family, no Bonferroni figure, no confirmatory claim;
 5. the matched-target view (R3 17.3.7): variants compared only over the draws all of them have;
 6. the development and the Mode H reports, QUOTED from their own files by identity, never recomputed;
 7. the retired-revision index: each retired revision once, its last scored draw and where its records are.

One WEEKLY_REPORT search-log row per report, written before the parts are computed; the report's files are create-only
and carry the attempt id. A part that cannot be computed is printed as NOT AVAILABLE with its reason; it never stops
the other parts and never changes any other record.
"""
from __future__ import annotations

import csv
import io
import json
import uuid
from collections import Counter
from pathlib import Path

import _common.contract_publication as CP
import _common.contract_runner as CR
import _common.owner_records as OR
import _common.walk_forward as WF
import _common.weekly_records as WR
from _common.contract_receipts import track_id
from _common.contract_records import canonical, record_digest, sha256_hex

from . import collect as COL
from . import league_publish as LP
from . import league_sources as LS
from . import league_table as LT
from . import ov1 as OV
from . import ov1_retrospective as RET
from . import report as RP
from . import report_writer as RW

TOOL = 'Method_Weekly_Report.py'
REPORT_VERSION = 'MHUPB_WEEKLY_REPORT_V1'
PLAN_SCHEMA = 'WEEKLY_REPORT_PLAN_V1'
MANIFEST_SCHEMA = 'WEEKLY_REPORT_MANIFEST_V1'
ATTEMPT = 'wr-'
ROW_TYPE = 'WEEKLY_REPORT'
FORMAL_LABEL = 'OV-1 FORMAL PROSPECTIVE (REGISTERED)'
SECONDARY_LABEL = 'EXPLORATORY_COHORT'
CLASSES = (('FORWARD', 'PROSPECTIVE'), ('CATCH_UP', 'CATCH_UP'))          # kept apart, never merged
NO_POOLING = ('No figure in this report pools games, kinds of evidence or tests into one P value. Each part names its '
              'sources; a part marked NOT AVAILABLE was not computed.')
HEADLINE = ('MR7.MAIN', 'MR7.PB', 'MR5.MAIN')                               # the sub-measures shown in the text
CSV_FIELDS = ('part', 'label', 'game_id', 'unit', 'item', 'n', 'value', 'z', 'p', 'labels', 'source', 'monte_carlo')


class ReportRefused(Exception):
    """Refused before the search-log row: nothing was written."""


# ---------------------------------------------------------------- the parts

def league_part(root: Path, game_id: str) -> dict:
    latest = LS.latest_logged(root, game_id)
    if latest is None:
        return {'state': 'NOT_AVAILABLE', 'reason': 'no league table has been published yet'}
    m = latest['manifest']
    raw = LP._archived(root, game_id, m)[f'{m["name"]}.txt']
    return {'state': 'QUOTED', 'name': m['name'], 'manifest_digest': latest['digest'], 'txt_sha256': m['txt_sha256'],
            'text': raw.decode('ascii')}


def formal_part(root: Path, game_id: str) -> dict:
    """The registered formal test, from its own registration and ledger. This reads; it never writes a line."""
    try:
        st = OV.stream(root, game_id)
        s = OV.status(game_id)
    except OV.OV1Refused:
        return {'label': FORMAL_LABEL, 'state': 'NOT_REGISTERED',
                'reason': 'not registered yet (the owner registers it once, before its first eligible draw)'}
    except OV.OV1Blocked as exc:
        return {'label': FORMAL_LABEL, 'state': 'NOT_AVAILABLE', 'reason': str(exc)}
    rows = st['rows']
    return {'label': FORMAL_LABEL, 'state': 'STOPPED' if s['stopped'] is not None else 'RUNNING', 'status': s,
            'registration_digest': st['registration_digest'], 'ledger_lines': len(rows),
            'ledger_last_line_digest': record_digest(rows[-1]) if rows else None,
            'assumptions': list(st['reg']['rules']['operating_assumptions']), 'text': OV.status_lines(game_id)}


def retrospective_part(root: Path, game_id: str, data: dict, evidence, cohort, first, last) -> dict:
    try:
        if evidence is None:
            raise RET.RetroRefused('the weekly forecasts could not be read')
        return {'state': 'COMPUTED', **RET.view(root, game_id, data, cohort=cohort, first=first, last=last, evidence=evidence)}
    except RET.RetroRefused as exc:
        return {'label': RET.LABEL, 'statement': RET.STATEMENT, 'state': 'NOT_AVAILABLE', 'reason': str(exc)}


def secondary_part(root: Path, game_id: str, evidence, n1_runner, progress) -> dict:
    """The forward and the catch-up tables: WF-1B's measures over the weekly score lines of one class at a time."""
    scores = [s for s in WR.score_ledger(root, game_id) if s['scoring_policy_id'] == WR.ROUTINE_POLICY]
    out = {'label': SECONDARY_LABEL, 'classes': {}}
    for name, cls in CLASSES:
        tracks: dict = {}
        variants: dict = {}
        for s in scores:
            if s['effective_class'] != cls:
                continue
            m, rev, v, t = s['method_id'], s['method_revision'], s['variant_id'], s['target_draw_number']
            forecast = (evidence or {}).get((m, rev, v, t))
            failed = s['record_kind'] == 'PREDICTION_FAILED'
            vr = variants.setdefault((m, (rev, v)), {'targets': [], 'invalid': Counter(), 'groups': {}, 'whole': True})
            for ro in LS.READOUTS:
                tr = tracks.setdefault((m, (rev, v), ro), {'targets': [], 'invalid': Counter(), 'entries': {}, 'whole': True,
                                                           'track_id': track_id(game_id, m, v, ro, 'WF')})
                r = None if failed else s['readouts'][ro]
                if r is None or 'unavailable' in r:
                    tr['invalid']['PREDICTION_FAILED' if failed else r['unavailable']] += 1
                    continue
                tr['targets'].append({'draw_number': t, **r})
                entry = None if forecast is None else COL._entry(forecast, ro, game_id)[0]
                if entry is None:
                    tr['whole'] = False
                else:
                    tr['entries'][t] = entry
            if failed or s['rank'] is None:
                vr['invalid']['PREDICTION_FAILED' if failed else 'RANKING_UNAVAILABLE'] += 1
                continue
            vr['targets'].append({'draw_number': t, **{k: RP._unfrac(x) for k, x in s['rank'].items()}})
            if forecast is None:
                vr['whole'] = False
            else:
                barrels = forecast.get('barrels', {})
                vr['groups'][t] = {b: barrels[b].get('ranked_groups') for b in barrels}
        for unit in list(tracks.values()) + list(variants.values()):
            unit['status'] = COL.track_status(unit['targets'], unit['invalid'])
            if not unit.pop('whole'):                         # the Monte Carlo reference needs every frozen ticket
                unit['entries' if 'entries' in unit else 'groups'] = {}
        results, var_results, n1 = RP.measures_stage(game_id, tracks, variants, [], n1_runner, progress)
        rows = []
        for (m, (rev, v), ro), measures in sorted(results.items()):
            for mname in RP.READOUT_MEASURES:
                for sid, sub in measures[mname]['sub_measures'].items():
                    rows.append(_measure_row(f'{game_id}:{m}:r{rev}:{v}:{ro}', sid, sub, tracks[(m, (rev, v), ro)]))
        for (m, (rev, v)), r in sorted(var_results.items()):
            for sid, sub in r['sub_measures'].items():
                rows.append(_measure_row(f'{game_id}:{m}:r{rev}:{v}:RANKING', sid, sub, variants[(m, (rev, v))]))
        out['classes'][name] = {'effective_class': cls, 'tracks': len(tracks), 'variants': len(variants),
                                'score_lines': sum(1 for s in scores if s['effective_class'] == cls),
                                'local_figures_shown': RP.declared_tests(game_id, len(tracks), len(variants)),
                                'n1': 'N1_NOT_RUN' if n1 is None else f'policy {n1.get("policy_id")}, R = {n1.get("R")}',
                                'rows': rows}
    return out


def _measure_row(unit: str, sid: str, sub: dict, track: dict) -> dict:
    sig = sub.get('significance')
    z, p, labels = RW._sig_text(sig)
    return {'unit': unit, 'sub_measure': sid, 'n': sub['n'], 'descriptive': RW.describe(sub), 'z_plus': z, 'p_up': p,
            'labels': '+'.join(x for x in (labels if labels != '-' else '', *sub['flags']) if x) or '-',
            'mc': RW.mc_text(sig) or RW.mc_text(sub.get('n1_reference')) or '', 'track_status': track['status']}


def matched_part(data: dict) -> dict:
    """R3 17.3.7: the variants that have any summed TOP score, compared only over the draws all of them have."""
    per = LT.chance_per_draw(data['game_id'])
    entries = [e for e in LT.summarise(data) if e['not_available'] is None and e['all_draws']]
    by: dict = {}
    for r in data['rows']:
        if r['readout'] == 'TOP':
            by.setdefault((r['method'], r['revision'], r['variant']), {})[r['target']] = r['main']
    keys = [(e['method'], e['revision'], e['variant']) for e in entries]
    common = sorted(set.intersection(*[set(by[k]) for k in keys])) if keys else []
    rows = [{'method': k[0], 'revision': k[1], 'variant': k[2], 'draws': len(common),
             'hits': sum(by[k][t] for t in common), 'chance': str(len(common) * per)} for k in keys]
    return {'variants': len(keys), 'matched_draws': len(common), 'first': common[0] if common else None,
            'last': common[-1] if common else None, 'rows': rows,
            'left_out': sorted({n['source'] for n in data['not_available']})}


def quoted_part(root: Path, game_id: str, data: dict) -> list[dict]:
    """The development and Mode H reports, by identity: file names and digests, and the family lines as recorded."""
    wanted = [(e['attempt_id'], f'ranking_{game_id}_WF_{e["window_first"]}-{e["window_last"]}_*_{e["attempt_id"]}.json',
               'development report') for e in data['sources']]
    if data['mode_h']['identity'] is not None:
        a = data['mode_h']['identity']['attempt_id']
        wanted.append((a, f'mode_h_{game_id}_*_{a}.json', 'Mode H report (sealed study; history)'))
    out = []
    for attempt, pattern, what in wanted:
        found = sorted(LS.reports_dir(root, game_id).glob(pattern))
        if len(found) != 1:
            out.append({'attempt_id': attempt, 'what': what, 'state': 'NOT_AVAILABLE', 'reason': 'its report files are not there'})
            continue
        base = found[0].name[:-len('.json')]
        files = {ext: found[0].with_name(f'{base}.{ext}') for ext in ('txt', 'csv', 'json')}
        try:
            man = json.loads(found[0].read_bytes().decode('ascii'))
        except (ValueError, UnicodeDecodeError):
            out.append({'attempt_id': attempt, 'what': what, 'state': 'NOT_AVAILABLE', 'reason': 'its manifest is not JSON'})
            continue
        out.append({'attempt_id': attempt, 'what': what, 'state': 'QUOTED', 'base': base,
                    'sha256': {ext: (sha256_hex(p.read_bytes()) if p.is_file() else None) for ext, p in files.items()},
                    'window': [man.get('window_first'), man.get('window_last')], 'evidence_tier': man.get('evidence_tier'),
                    'families_as_recorded': man.get('families') or [],
                    'wording_as_recorded': (man.get('mode_h') or {}).get('null_result_wording')})
    return out


def retired_index(data: dict) -> list[dict]:
    """Each retired revision once: its last scored draw and which sources hold its records (Sup 8)."""
    out = []
    for e in LT.summarise(data):
        if e['status'] != 'RETIRED':
            continue
        key = (e['method'], e['revision'], e['variant'])
        mine = [r for r in data['rows'] + data['mode_h']['rows'] if (r['method'], r['revision'], r['variant']) == key]
        out.append({'method': key[0], 'revision': key[1], 'variant': key[2], 'release_date': e['release_date'],
                    'last_scored_target': max((r['target'] for r in mine), default=None),
                    'score_records': len(mine), 'records_in': sorted({r['source'] for r in mine})})
    return sorted(out, key=lambda r: (r['method'], r['revision'], r['variant']))


# ---------------------------------------------------------------- one report

def run_report(game_id: str, *, cohort='CURRENT', ov1_first: int | None = None, ov1_last: int | None = None,
               n1_runner=None, echo=None) -> dict:
    """Read the sources, append the WEEKLY_REPORT row, compute the parts. ReportRefused before the row."""
    def progress(text: str) -> None:
        if echo is not None:
            echo(f'{CP.utc_now()[11:19]} UTC  {text}')
    m = Path(CR.ORPHAN_MARKER)
    if m.exists() or m.is_symlink():
        raise ReportRefused('UNRESOLVED_ORPHAN_MARKER: no experiment or report is permitted')
    root = LS.project_root()
    try:
        data, pins = LS.collect(root, game_id)
    except LS.LeagueRefused as exc:
        raise ReportRefused(f'the sources do not read: {exc}') from None
    named = cohort if isinstance(cohort, str) else sorted(list(c) for c in cohort)
    plan = {'schema': PLAN_SCHEMA, 'game_id': game_id, 'report_version': REPORT_VERSION, 'inputs': pins,
            'ov1_retrospective': {'cohort': named, 'window': [ov1_first, ov1_last]}, 'n1': n1_runner is not None,
            'secondary_label': SECONDARY_LABEL}
    attempt_id = ATTEMPT + uuid.uuid4().hex
    try:
        row = WF._append_search_row({'row_type': ROW_TYPE, 'utc': CP.utc_now(), 'game_id': game_id, 'mode': 'WF',
                                     'window_last': LT.latest_draw(data), 'cohort_size': len(pins['roster']),
                                     'cohort_digest': record_digest({'roster': pins['roster']}),
                                     'measures': RP.STAGE2 + ',OV-1', 'attempt_id': attempt_id,
                                     'plan_digest': record_digest(plan), 'tool': TOOL, 'tool_version': REPORT_VERSION,
                                     'tool_sha256': LP.tool_sha256()})
    except WF.BatchRefused as exc:
        raise ReportRefused(str(exc)) from None
    progress(f'search-log row {row} written; reading the frozen forecasts')
    try:
        evidence = RET.weekly_evidence(root, game_id)
    except RET.RetroRefused:
        evidence = None
    res = {'game_id': game_id, 'attempt_id': attempt_id, 'search_log_row': row, 'plan': plan,
           'plan_digest': record_digest(plan), 'data': data}
    try:
        res['league'] = league_part(root, game_id)
    except LS.LeagueRefused as exc:
        res['league'] = {'state': 'NOT_AVAILABLE', 'reason': str(exc)}
    res['formal'] = formal_part(root, game_id)
    progress('the retrospective OV-1 view')
    res['retrospective'] = retrospective_part(root, game_id, data, evidence, cohort, ov1_first, ov1_last)
    progress('the forward and catch-up tables')
    res['secondary'] = secondary_part(root, game_id, evidence, n1_runner, progress)
    res['matched'] = matched_part(data)
    res['quoted'] = quoted_part(root, game_id, data)
    res['retired'] = retired_index(data)
    return res


def build(res: dict, generated_utc: str) -> dict:
    """The report's four members as bytes: text, CSV, the manifest and the retired-revision index."""
    g = res['game_id']
    out: list[str] = []
    w = out.append
    rows: list[dict] = []

    def add(part, label, unit, item, n='', value='', z='', p='', labels='', source='', mc=''):
        rows.append(dict(zip(CSV_FIELDS, (part, label, g, unit, item, n, value, z, p, labels, source, mc))))

    def head(title):
        out.extend(['', '=' * 100, title, '=' * 100])

    w(f'WEEKLY REPORT - {g} - {generated_utc}')
    w(f'Attempt {res["attempt_id"]}; search-log row {res["search_log_row"]}; report plan {res["plan_digest"]}')
    w(NO_POOLING)

    head('1. THE LEAGUE TABLE (quoted from the archive; not recomputed)')
    lg = res['league']
    if lg['state'] == 'QUOTED':
        w(f'Publication {lg["name"]}; manifest {lg["manifest_digest"]}; text sha256 {lg["txt_sha256"]}')
        w('-' * 100)
        out.extend(lg['text'].splitlines())
    else:
        w(f'NOT AVAILABLE: {lg["reason"]}')

    head(f'2. {FORMAL_LABEL}')
    f = res['formal']
    if f['state'] in ('RUNNING', 'STOPPED'):
        s = f['status']
        w(f'Source: registration {f["registration_digest"]}; OV-1 ledger {f["ledger_lines"]} lines, last line '
          f'{f["ledger_last_line_digest"]}. One stream for this game alone.')
        out.extend(f['text'])
        w(f'The guarantee, and what it rests on: if this game\'s draws are fair, the chance that the score ever reaches '
          f'{s["bar"]} is at most 1 in {s["bar"]} (2.5%), provided that: ' + '; '.join(f['assumptions']) + '.')
        w(f'Reaching {s["bar"]} would be a challenge to the fair-draw assumption for this game, not proof of a cause.')
        for item in ('counted', 'skipped', 'missed'):
            add('OV1_FORMAL', FORMAL_LABEL, g, item, value=s[item], source=f['registration_digest'])
        add('OV1_FORMAL', FORMAL_LABEL, g, 'score_lower_bound', value=s['score_text'], labels=f['state'],
            source=f['registration_digest'])
    else:
        w(f'{f["state"]}: {f["reason"]}')
        add('OV1_FORMAL', FORMAL_LABEL, g, 'state', labels=f['state'])

    head(f'3. {RET.LABEL}')
    r = res['retrospective']
    if r['state'] == 'COMPUTED':
        out.extend(RET.lines(r)[1:])
        for s in r['series']:
            add('OV1_RETROSPECTIVE', RET.LABEL, s['target'], 'score_after_this_draw', n=s['pairs'], value=s['score_text'],
                z=s['z'] or '', labels=s['state'], source=r['identity_digest'])
        add('OV1_RETROSPECTIVE', RET.LABEL, g, 'final_score_lower_bound', n=r['counted'], value=r['final_score_text'],
            labels='DESCRIPTIVE_NOT_A_P_VALUE', source=r['identity_digest'])
    else:
        w(f'{r["statement"]}')
        w(f'NOT AVAILABLE: {r["reason"]}')
        add('OV1_RETROSPECTIVE', RET.LABEL, g, 'state', labels='NOT_AVAILABLE')

    head(f'4. SECONDARY: THE FORWARD AND THE CATCH-UP TABLES ({SECONDARY_LABEL})')
    w(f'{SECONDARY_LABEL}: the draws and the variants in these tables grow from report to report, so they are not a family '
      f'fixed in advance. Every figure is a local figure with its own label; LOW_N marks fewer than 30 draws. No family '
      f'is registered for them, no family-wise or Bonferroni figure is computed, and nothing here is a confirmatory '
      f'claim. Forward (class PROSPECTIVE) and catch-up (class CATCH_UP) are kept apart. The text shows the headline '
      f'local measures ({", ".join(HEADLINE)}); every sub-measure is in the CSV.')
    for name, _cls in CLASSES:
        c = res['secondary']['classes'][name]
        w('')
        w(f'{name} ({c["effective_class"]}): {c["score_lines"]} score lines, {c["tracks"]} readout tracks, {c["variants"]} '
          f'rankings; {c["local_figures_shown"]} local figures shown; Monte Carlo reference: {c["n1"]}')
        shown = [x for x in c['rows'] if x['sub_measure'] in HEADLINE]
        out.extend(LT._table(['Unit', 'Measure', 'n', 'Result', 'Z_plus', 'P_up (local)', 'Labels'],
                             [[x['unit'], x['sub_measure'], x['n'], x['descriptive'], x['z_plus'], x['p_up'], x['labels']]
                              for x in shown]) if shown else ['  no score line of this class yet'])
        for x in c['rows']:
            if x['mc']:                                      # the fixed-forecast Monte Carlo reference, beside its figure
                w(f'  {x["unit"]} {x["sub_measure"]}: {x["mc"]}')
        for x in c['rows']:
            add(f'SECONDARY_{name}', SECONDARY_LABEL, x['unit'], x['sub_measure'], n=x['n'], value=x['descriptive'],
                z=x['z_plus'], p=x['p_up'], labels=x['labels'], source='weekly score ledger', mc=x['mc'])

    head('5. THE MATCHED-TARGET VIEW (TOP ticket, main barrel; only the draws every listed variant has)')
    mt = res['matched']
    if mt['matched_draws']:
        w(f'{mt["variants"]} variants, {mt["matched_draws"]} matched draws (draws {mt["first"]} to {mt["last"]}).')
        out.extend(LT._table(['Method', 'Rev', 'Variant', 'Draws', 'Hits', 'Chance'],
                             [[x['method'], x['revision'], x['variant'], x['draws'], x['hits'], LT.dec(_frac(x['chance']))]
                              for x in mt['rows']]))
    else:
        w(f'No draw is scored for every one of the {mt["variants"]} variants that have a score.')
    if mt['left_out']:
        w('Left out (source not available): ' + ', '.join(mt['left_out']))
    for x in mt['rows']:
        add('MATCHED_TARGETS', 'DESCRIPTIVE', f'{g}:{x["method"]}:r{x["revision"]}:{x["variant"]}', 'hits_on_matched_draws',
            n=x['draws'], value=x['hits'])

    head('6. THE DEVELOPMENT AND MODE H REPORTS (quoted from their own files; not recomputed)')
    if not res['quoted']:
        w('No development attempt is listed and no Mode H score is recorded.')
    for q in res['quoted']:
        if q['state'] != 'QUOTED':
            w(f'{q["what"]} {q["attempt_id"]}: NOT AVAILABLE: {q["reason"]}')
            continue
        w(f'{q["what"]} {q["attempt_id"]}: {q["base"]} (draws {q["window"][0]}-{q["window"][1]}; {q["evidence_tier"]})')
        for ext in ('txt', 'csv', 'json'):
            w(f'  .{ext} sha256 {q["sha256"][ext]}')
        for fam in q['families_as_recorded']:
            w('  family as recorded: ' + canonical(fam).decode('ascii').rstrip('\n'))
        if q['wording_as_recorded']:
            w(f'  as recorded: {q["wording_as_recorded"]}')
        add('QUOTED_REPORT', q['evidence_tier'] or '', q['attempt_id'], 'report_text_sha256', value=q['sha256']['txt'], source=q['base'])

    head('7. THE RETIRED-REVISION INDEX')
    if not res['retired']:
        w('No retired revision.')
    for x in res['retired']:
        w(f'{x["method"]} revision {x["revision"]} {x["variant"]} (released {x["release_date"]}): last scored draw '
          f'{x["last_scored_target"] or "-"}; {x["score_records"]} score records in: {", ".join(x["records_in"]) or "-"}')
        add('RETIRED_INDEX', 'RETIRED_AS_PUBLISHED', f'{g}:{x["method"]}:r{x["revision"]}:{x["variant"]}',
            'last_scored_target', n=x['score_records'], value=x['last_scored_target'] or '', source=';'.join(x['records_in']))

    text = ('\n'.join(out) + '\n').encode('ascii')
    buf = io.StringIO()
    wr = csv.DictWriter(buf, CSV_FIELDS, lineterminator='\n')
    wr.writeheader()
    wr.writerows(rows)
    csv_bytes = buf.getvalue().encode('ascii')
    retired = canonical({'schema': 'RETIRED_REVISION_INDEX_V1', 'game_id': g, 'attempt_id': res['attempt_id'],
                         'generated_utc': generated_utc, 'retired': res['retired']})
    sec = {n: {k: v for k, v in c.items() if k != 'rows'} for n, c in res['secondary']['classes'].items()}
    manifest = {'schema': MANIFEST_SCHEMA, 'game_id': g, 'attempt_id': res['attempt_id'],
                'search_log_row': res['search_log_row'], 'generated_utc': generated_utc, 'plan': res['plan'],
                'plan_digest': res['plan_digest'], 'tool': TOOL, 'tool_version': REPORT_VERSION,
                'statement': NO_POOLING,
                'parts': {'league_table': {k: v for k, v in res['league'].items() if k != 'text'},
                          'ov1_formal': {k: v for k, v in res['formal'].items() if k != 'text'},
                          'ov1_retrospective': res['retrospective'],
                          'secondary': {'label': SECONDARY_LABEL, 'classes': sec},
                          'matched_targets': res['matched'], 'quoted_reports': res['quoted'],
                          'retired_index_sha256': sha256_hex(retired)},
                'text_sha256': sha256_hex(text), 'csv_sha256': sha256_hex(csv_bytes)}
    return {'txt': text, 'csv': csv_bytes, 'json': canonical(manifest), 'retired_index.json': retired}


def _frac(text: str):
    from fractions import Fraction
    return Fraction(text)


def write(res: dict, contents: dict, stamp: str) -> list[Path]:
    """Create-only files in results/method_rankings/<GAME>/; the attempt id is part of each name."""
    folder = LS.reports_dir(LS.project_root(), res['game_id'])
    folder.mkdir(parents=True, exist_ok=True)
    base = f'weekly_report_{res["game_id"]}_{stamp}_{res["attempt_id"]}'
    paths = []
    for ext in ('txt', 'csv', 'json', 'retired_index.json'):
        p = folder / (f'{base}.{ext}' if ext != 'retired_index.json' else f'{base}_retired_index.json')
        CP.create_only(p, contents[ext])
        paths.append(p)
    return paths
