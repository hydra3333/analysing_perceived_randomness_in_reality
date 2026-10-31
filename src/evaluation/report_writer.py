"""WF-1B: the report files (R3 17.10; design v0.1r1 section 6.8; WF-1B supplement v0.1r1 section 3, WB-1).

Text layout (WB-1): header; Part A "League tables: results against the real draws" (the RK-4 disclosure block, then
every descriptive table); glossary; fair-draw reference; Part B "League tables: adjusted against fair random
draws" (every significance table and the families' global figures); per-track detail; notes.
The CSV and JSON carry the same rows, each with `table_kind` DESCRIPTIVE, SIGNIFICANCE or RK4_DISCLOSURE.
No drawn number appears in any report file (decision WF1-10): only counts, statistics, draw numbers and labels.
"""
from __future__ import annotations

import csv
import io
import json
import math
import platform
from collections import Counter
from fractions import Fraction
from pathlib import Path

import _common.contract_publication as CP
from _common.contract_registry import InstalledRegistry
import _common.contract_registry as REG
from _common.contract_records import canonical, sha256_hex

from . import divisions as DV
from . import measures as MS
from . import numerics as NU
from . import report as RP

RK4_TITLE = ('RK-4 disclosure - global and significance context, not part of the descriptive rankings '
             '(full figures in Part B)')
PART_A = 'PART A - LEAGUE TABLES: RESULTS AGAINST THE REAL DRAWS'
PART_B = 'PART B - LEAGUE TABLES: ADJUSTED AGAINST FAIR RANDOM DRAWS'
TIER = 'DEVELOPMENT_WF_EXPLORATORY'
TIER_TEXT = 'retrospective development walk-forward'
MEASURE_ORDER = ('MR0', 'MR1', 'MR4', 'MR5', 'MR7', 'MR16')


def _num(x) -> str:
    """Display: ints as ints; Fractions and floats to 6 significant digits; None as '-'."""
    if x is None:
        return '-'
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, int):
        return str(x)
    if isinstance(x, Fraction):
        return x.numerator.__str__() if x.denominator == 1 else f'{float(x):.6g}'
    if isinstance(x, float):
        return '>= 1000' if math.isinf(x) else f'{x:.6g}'
    if isinstance(x, tuple):
        return '(' + ', '.join(_num(v) for v in x) + ')'
    return str(x)


def _jsonable(x):
    if isinstance(x, Fraction):
        return str(x)
    if isinstance(x, float):
        return None if math.isnan(x) else ('Infinity' if math.isinf(x) else x)
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, MS.MR1Key):
        return str(x)
    return x


_SHOW = (('W', 'wins by division'), ('MR1', 'bits per draw'), ('MR1-T', 'top-division score'), ('E0', 'fair'), ('difference', 'minus fair'),
         ('k_S', 'wins'), ('S', 'main matches'), ('B', 'Powerball hits'), ('S_per_draw', 'per draw'), ('excess', 'above fair'), ('k', 'hits'),
         ('rate', 'rate'), ('interval', '95% interval'), ('mean_rank_main', 'mean drawn rank'),
         ('MR5', 'mean rank of the drawn numbers (1 = most favoured)'), ('expectation', 'fair'),
         ('expected', 'fair expectation'))


def describe(sub: dict) -> str:
    """The sub-measure's main real-outcome results, for the descriptive tables (no p-value, sigma or label)."""
    parts = []
    for k, name in _SHOW:
        if k in sub and sub[k] is not None and not isinstance(sub[k], dict):
            v = sub[k]
            if isinstance(v, (list, tuple)) and k == 'W':
                v = ' '.join(str(x) for x in v)
            parts.append(f'{name} {_num(v)}')
    return '; '.join(parts) if parts else '-'


def _sig_text(sig: dict | None) -> tuple[str, str, str]:
    """(Z_plus, P_up, labels) for display. The calibration label is shown together with any range label of the
    p-value (P_BELOW_FLOAT64_RANGE) or the sigma (SIGMA_ABOVE_BOUND), never replaced by it (EX_109 C02)."""
    if not sig:
        return '-', '-', '-'
    zp = sig.get('Z_plus')
    z = '-' if not zp or zp.get('sigma') is None else ('>= 1000' if zp.get('label') == 'SIGMA_ABOVE_BOUND'
                                                          else NU.format_sigma(zp['sigma']))
    po = sig.get('P_up_output')
    p = '-' if not po else (NU.format_prob(po['p_float']) if po['label'] is None else f"10^{po['p_log10']}")
    labels = [sig.get('label')] + [x.get('label') if isinstance(x, dict) else None for x in (po, zp)]
    out = []
    for lab in labels:
        if lab and lab not in out:
            out.append(lab)
    return z, p, '+'.join(out) or '-'


def mc_fields(blk) -> dict | None:
    """N1's Monte Carlo facts for a block, if it carries them: k, R, P = (k+1)/(R+1) and the Clopper-Pearson 95%
    interval on k/R (R3 17.5A, 17.5.3; EX_109 C01)."""
    if not isinstance(blk, dict) or blk.get('R') is None or blk.get('k') is None:
        return None
    lo, hi = blk['ci']
    return {'k': blk['k'], 'R': blk['R'], 'p_mc': Fraction(blk['k'] + 1, blk['R'] + 1), 'ci_low': lo, 'ci_high': hi}


def mc_text(blk) -> str | None:
    m = mc_fields(blk)
    if m is None:
        return None
    return (f"N1 Monte Carlo: k = {m['k']} of R = {m['R']} replicates; P = (k+1)/(R+1) = {NU.format_prob(float(m['p_mc']))}; "
            f"Monte Carlo 95% interval on k/R (Clopper-Pearson) [{m['ci_low']:.6g}, {m['ci_high']:.6g}]")


def _mc_csv(blk) -> dict:
    m = mc_fields(blk)
    if m is None:
        return {}
    return {'n1_mc_k': m['k'], 'n1_mc_R': m['R'], 'n1_mc_p': repr(float(m['p_mc'])), 'n1_mc_ci95_low_k_over_R': repr(m['ci_low']),
            'n1_mc_ci95_high_k_over_R': repr(m['ci_high'])}


def _method_texts(game_id: str, members) -> dict:
    reg = InstalledRegistry(Path(REG.DATA_ROOT))
    out = {}
    for mem in members:
        e = reg.active_entry(game_id, mem['method_id'], mem['variant_id'])
        out[(mem['method_id'], mem['variant_id'])] = {'name': e.get('method_name'), 'one_liner': e.get('one_liner'),
                                                       'short_explanation': e.get('short_explanation')}
    return out


def rows_of(res: dict) -> list[dict]:
    """One row per (analysis unit, sub-measure), with its descriptive and significance parts."""
    out = []
    g = res['game_id']
    for (mid, vid, ro), measures in res['results'].items():
        tr = res['per_track'][(mid, vid, ro)]
        for name in ('MR0', 'MR1', 'MR4', 'MR7', 'MR16'):
            r = measures[name]
            for sid, sub in r['sub_measures'].items():
                out.append({'analysis_unit': 'READOUT_TRACK', 'unit_id': tr['track_id'], 'track_id': tr['track_id'],
                            'method_id': mid, 'variant_id': vid, 'readout': ro, 'measure': name, 'sub': sub,
                            'track_status': tr['status'], 'invalid_cells': tr['invalid']})
    for (mid, vid), r in res['var_results'].items():
        vr = res['per_variant'][(mid, vid)]
        uid = f'{g}:{mid}:{vid}:WF'
        for sid, sub in r['sub_measures'].items():
            out.append({'analysis_unit': 'METHOD_VARIANT_RANKING', 'unit_id': uid, 'track_id': uid, 'method_id': mid,
                        'variant_id': vid, 'readout': '-', 'measure': 'MR5', 'sub': sub,
                        'track_status': vr['status'], 'invalid_cells': vr['invalid']})
    return out


def families_global(res: dict) -> list[dict]:
    """Each registered family's global figures (design 6.2A, 6.7; R3 17.5.3)."""
    out = []
    by_tid = {}
    for (mid, vid, ro), measures in res['results'].items():
        by_tid[res['per_track'][(mid, vid, ro)]['track_id']] = (measures, res['per_track'][(mid, vid, ro)])
    for fam in res['families']:
        sub_id = fam['measure']                              # 'MR7.MAIN' or 'MR7.PB'
        broke, ps, members = [], [], []
        for tid in fam['roster']:
            if tid not in by_tid:
                broke.append((tid, 'NOT_IN_THIS_REPORT'))
                continue
            measures, tr = by_tid[tid]
            sub = measures['MR7']['sub_measures'][sub_id]
            sig = sub.get('significance') or {}
            if tr['status'] != 'GRID_COMPLETE':
                broke.append((tid, tr['status']))
            elif sig.get('label') != 'EXACT_LOCAL':
                broke.append((tid, sig.get('label') or 'NO_P_VALUE'))
            if sig.get('P_up') is not None:
                ps.append((sig['P_up'], tid))
            members.append(tid)
        roster_ok = set(fam['roster']) == set(by_tid)
        if not roster_ok:
            broke.append(('*', 'ROSTER_DIFFERS_FROM_REPORT_COHORT'))
        entry = {'family_id': fam['family_id'], 'M': fam['M'], 'measure': sub_id, 'roster_digest': fam['roster_digest'],
                 'broken': broke, 'n_broken': len([b for b in broke if b[0] != '*']), 'tracks_with_p': len(ps)}
        if ps:
            pmin, tid = min(ps)
            b = MS.bonferroni(pmin, fam['M'])
            entry.update({'min_P_up': pmin, 'min_track': tid, 'P_bonf': b['P_bonf'], 'P_bonf_output': b['P_bonf_output'],
                          'Z_plus': b['Z_plus'],
                          'guaranteed': not broke,
                          'label': None if not broke else 'BONFERRONI_REFERENCE_UNCALIBRATED'})
        else:
            entry.update({'min_P_up': None, 'P_bonf': None, 'guaranteed': False, 'label': 'MR_INSUFFICIENT_DATA'})
        n1 = (res.get('n1') or {}).get('families', {}).get(fam['family_id'])
        entry['n1_max'] = n1 if n1 is not None else {'label': 'N1_NOT_RUN'}
        if n1 is not None and broke:
            entry['n1_max'] = dict(n1, flag='SELECTION_UNVERIFIED')
        out.append(entry)
    return out


GUARANTEED_TEXT = 'guaranteed (design 6.2A conditions hold)'


def _bonf_label_text(f: dict) -> str:
    """No new label is invented: a guaranteed figure is shown as such; otherwise R3's own label (17.5.2)."""
    return GUARANTEED_TEXT if f.get('guaranteed') else f['label']


def build(res: dict, *, generated_utc: str, seed_line: str, n1_policies_on_file: int, environment: dict) -> dict:
    """Builds the three file contents (bytes) without writing anything."""
    g, S, L = res['game_id'], res['first'], res['last']
    plan = res['plan']
    texts = _method_texts(g, plan['cohort'])
    mreg = json.loads((RP.REGISTRY_DIR / 'MEASURE_REGISTRY_V1.json').read_bytes().decode('ascii'))
    rows = rows_of(res)
    fams = families_global(res)
    srows = RP.search_rows(g)
    by_type = Counter(r['row_type'] for r in srows)
    rr = [r for r in srows if r['row_type'] == 'RANKING_REPORT']
    unfinished = [r for r in rr if r['attempt_id'] != res['attempt_id'] and
                  not any((RP.roots()['reports'] / g).glob(f"*{r['attempt_id']}*.json"))]
    status_counts = Counter(tr['status'] for tr in res['per_track'].values())
    L_ = []
    w = L_.append

    # ---------------------------------------------------------------- 1. header
    w('PREDICTIVE RANDOMNESS - METHOD RANKINGS REPORT')
    w('')
    w(f'Game: {g}')
    w(f"Mode: {mreg['modes']['WF']['display']}")
    w(f"  {mreg['modes']['WF']['plain_meaning'].replace('**', '')}")
    w(f'Evidence tier: {TIER} ({TIER_TEXT}); randomness chosen for the experiment where N1 runs (D-11)')
    w(f'Window: {S}-{L} (each track scored on its own fixed grid inside it: OWN_SET, decision WF1-6)')
    w(f"Batch: {plan['batch_id']} (targets {plan['window_first']}-{plan['window_last']}); cohort digest "
      f"{plan['cohort_digest']}; {len(plan['cohort'])} variants, {len(res['per_track'])} tracks")
    w('Families: ' + (', '.join(f['family_id'] for f in res['families']) or 'none apply to this window: '
                      'every table is EXPLORATORY_COHORT'))
    w('Track counts by status: ' + ', '.join(f'{k} {v}' for k, v in sorted(status_counts.items())))
    w(f"Master: {plan['master_file']} version {plan['ledger_version']}, SHA-256 {plan['master_sha256']}")
    w(f"Tool: {RP.TOOL} {RP.EVALUATOR_VERSION}, sources SHA-256 {RP.tool_sha256()}")
    w(f'N1: {seed_line}; N1 seed policies on file for this game: {n1_policies_on_file}')
    w('Environment: ' + ', '.join(f'{k} {v}' for k, v in sorted(environment.items())))
    w(f"Report attempt: {res['attempt_id']}; search-log row {res['search_log_row']}; scoring plan digest "
      f"{res['scoring_plan_digest']}; generated {generated_utc}")
    w(f"Search log ({g}): {by_type.get('RANKING_REPORT', 0)} RANKING_REPORT rows, of which {len(unfinished)} have no "
      f"completed report besides this one; {by_type.get('WF_BATCH', 0)} WF_BATCH rows")
    w('')

    # ---------------------------------------------------------------- 2. Part A
    w('=' * 100)
    w(PART_A)
    w('=' * 100)
    w('')
    w('+' + '-' * 98)
    w('| ' + RK4_TITLE)
    w(f"| Tracks compared: {len(res['per_track'])}; variants: {len(res['per_variant'])}; local tests counted for "
      f"this report: {res['declared_tests']}")
    w(f"| Search log ({g}): RANKING_REPORT rows {by_type.get('RANKING_REPORT', 0)} (without a completed report, "
      f"other than this one: {len(unfinished)}); WF_BATCH rows {by_type.get('WF_BATCH', 0)}")
    for f in fams:
        z, p, _ = _sig_text({'Z_plus': f.get('Z_plus'), 'P_up_output': f.get('P_bonf_output')}) if f.get('P_bonf') is not None \
            else ('-', '-', '-')
        n1 = f['n1_max']
        w(f"| Family {f['family_id']}: M = {f['M']}; Bonferroni P = {p}, Z_plus = {z}, "
          f"{_bonf_label_text(f)}; tracks breaking the guarantee's conditions: {f['n_broken']}; "
          f"N1 maximum statistic: {n1.get('label')}" + (f"; {mc_text(n1)}" if mc_text(n1) else ''))
    w(f'| N1: {seed_line}; N1 seed policies on file: {n1_policies_on_file}')
    w('+' + '-' * 98)
    w('')
    csv_rows = [{'table_kind': 'RK4_DISCLOSURE', 'analysis_unit': '', 'unit_id': f['family_id'], 'sub_measure': f['measure'],
                 'rank': '', 'n': '', 'descriptive_key': '', 'z_plus': _num((f.get('Z_plus') or {}).get('sigma')),
                 'p_value': _num(f.get('P_bonf')), 'label': _bonf_label_text(f), 'track_status': f"broken={f['n_broken']}"}
                for f in fams]
    for row, f in zip(csv_rows, fams):
        row.update(_mc_csv(f['n1_max']))
    descriptive_tables, significance_tables = [], []
    subs = []
    for r in rows:
        if (r['measure'], r['sub']['sub_measure']) not in subs:
            subs.append((r['measure'], r['sub']['sub_measure']))
    subs.sort(key=lambda x: (MEASURE_ORDER.index(x[0]), 0))
    for measure, sid in subs:
        group = [r for r in rows if r['measure'] == measure and r['sub']['sub_measure'] == sid]
        if any(r['sub'].get('descriptive_order') for r in group):
            order = next(r['sub']['descriptive_order'] for r in group if r['sub'].get('descriptive_order'))
            ranked = MS.rank_table([{'track_id': r['track_id'], 'r': r} for r in group],
                                   key=lambda x: x['r']['sub']['descriptive_key'], descending=(order != 'ascending'))
            descriptive_tables.append((measure, sid, order, ranked))
        if any(r['sub'].get('significance') for r in group):
            ranked = MS.rank_table([{'track_id': r['track_id'], 'r': r} for r in group],
                                   key=lambda x: x['r']['sub']['significance_key'], descending=True)
            significance_tables.append((measure, sid, ranked))
    for measure, sid, order, ranked in descriptive_tables:
        w(f"{sid} - descriptive ranking (by the raw result against the real draws; "
          f"{'lower is better' if order == 'ascending' else 'higher is better'})")
        w(f"{'Rank':>5}  {'Unit':<58} {'n':>4}  Status; result")
        for e in ranked:
            r = e['r'] if 'r' in e else e['row']['r']
            sub = r['sub']
            key = '(undefined)' if e['undefined'] else describe(sub)
            name = texts[(r['method_id'], r['variant_id'])]['name'] or ''
            w(f"{e['display']:>5}  {r['unit_id']:<58} {sub['n']:>4}  {r['track_status']}"
              f"{' ' + ','.join(sub['flags']) if sub['flags'] else ''}")
            w(f"{'':7}{r['method_id']} {name}: {key}")
            csv_rows.append({'table_kind': 'DESCRIPTIVE', 'analysis_unit': r['analysis_unit'], 'unit_id': r['unit_id'],
                             'sub_measure': sid, 'rank': e['display'], 'n': sub['n'], 'descriptive_key': key,
                             'z_plus': '', 'p_value': '', 'label': 'NOT_A_P_VALUE', 'track_status': r['track_status']})
        w('')

    # ---------------------------------------------------------------- 3. glossary
    w('=' * 100)
    w('GLOSSARY')
    w('=' * 100)
    for code in ('WF', 'IS'):
        w(mreg['modes'][code]['display'])
        w('  ' + mreg['modes'][code]['plain_meaning'].replace('**', ''))
    w('')
    for m in mreg['measures']:
        w(f"{m['heading']}")
        w(f"  One line: {m['one_liner']}")
        w(f"  Short explanation: {m['short_explanation'].replace('**', '')}")
    w('')
    w('Calibration labels:')
    for lab in mreg['calibration_labels']:
        w(f"  {lab['label']}: {lab['meaning'].replace('**', '')}")
    w('  MR_EXACT_BOUND_EXCEEDED, P_BELOW_FLOAT64_RANGE, SIGMA_ABOVE_BOUND, N1_NOT_RUN: design v0.1r1 6.6 and 7.6.')
    w('Report statuses:')
    for st in mreg['report_statuses']:
        w(f"  {st['status']}: {st['meaning']}")
    w('  GRID_COMPLETE / GRID_INCOMPLETE / GRID_EMPTY: design v0.1r1 6.2A (track statuses).')
    w('Evidence tiers:')
    for t in mreg['evidence_tiers']:
        w(f"  {t['tier']}: {t['meaning']}")
    w('Pattern origins:')
    for o in mreg['pattern_origins']:
        w(f"  {o['id']} {o['origin']}: {o['distinguished_by']}")
    w('Methods:')
    for (mid, vid), tx in sorted(texts.items(), key=lambda kv: (int(kv[0][0][2:]), kv[0][1])):
        w(f"  {mid} {vid}: {tx['name']} - {tx['one_liner']}")
    w('')

    # ---------------------------------------------------------------- 4. fair-draw reference
    w('=' * 100)
    w('FAIR-DRAW REFERENCE')
    w('=' * 100)
    probs = DV.division_probabilities(g)
    w('Division probabilities per draw (exact) and expected wins over n = 100 draws:')
    for d in range(1, DV.DIVISION_COUNT[g] + 1):
        p = probs[d] if isinstance(probs, dict) else probs[d - 1]
        w(f"  Division {d}: {p} ({float(p):.6g}); expected per 100 draws {float(p) * 100:.4g}")
    fm = DV.fair_moments(g)
    w(f"Main matches per draw: mean0 {fm['mean0']} ({float(fm['mean0']):.6g}), Var0 {fm['var0']} ({float(fm['var0']):.6g})")
    w('Sigma table (one-sided): 1 sigma 0.158655; 2 sigma 0.0227501; 3 sigma 0.00134990; 4 sigma 3.16712e-5; '
      '5 sigma 2.86652e-7; 6 sigma 9.86588e-10. A local sigma treats one track alone; see the family figures.')
    w('')

    # ---------------------------------------------------------------- 5. Part B
    w('=' * 100)
    w(PART_B)
    w('=' * 100)
    w('')
    for measure, sid, ranked in significance_tables:
        w(f'{sid} - significance ranking (local Z_plus, adjusted against fair random draws)')
        w(f"{'Rank':>5}  {'Unit':<58} {'n':>4}  {'Z_plus':>8}  {'P_up':>13}  Label")
        for e in ranked:
            r = e['row']['r']
            sig = r['sub'].get('significance')
            z, p, lab = _sig_text(sig)
            w(f"{e['display']:>5}  {r['unit_id']:<58} {r['sub']['n']:>4}  {z:>8}  {p:>13}  {lab}"
              f"{' ' + ','.join(r['sub']['flags']) if r['sub']['flags'] else ''}")
            if mc_text(sig):
                w(f"{'':7}{mc_text(sig)}")
            csv_rows.append(dict({'table_kind': 'SIGNIFICANCE', 'analysis_unit': r['analysis_unit'],
                                  'unit_id': r['unit_id'], 'sub_measure': sid, 'rank': e['display'],
                                  'n': r['sub']['n'], 'descriptive_key': '', 'z_plus': z, 'p_value': p, 'label': lab,
                                  'track_status': r['track_status']}, **_mc_csv(sig)))
            for extra_key in ('approx', 'n1_reference'):           # shown beside it, never instead (design 7.1)
                blk = r['sub'].get(extra_key)
                if isinstance(blk, dict) and blk is not sig and blk.get('label'):
                    z2, p2, lab2 = _sig_text(blk)
                    w(f"{'':7}also: {lab2}, Z_plus {z2}, P_up {p2}")
                    if mc_text(blk):
                        w(f"{'':13}{mc_text(blk)}")
                    csv_rows.append(dict({'table_kind': 'SIGNIFICANCE', 'analysis_unit': r['analysis_unit'],
                                          'unit_id': r['unit_id'], 'sub_measure': f'{sid}:{extra_key}', 'rank': '',
                                          'n': r['sub']['n'], 'descriptive_key': '', 'z_plus': z2, 'p_value': p2,
                                          'label': lab2, 'track_status': r['track_status']}, **_mc_csv(blk)))
        w('')
    w('Families (global figures):')
    for f in fams:
        z, p, _ = _sig_text({'Z_plus': f.get('Z_plus'), 'P_up_output': f.get('P_bonf_output')}) if f.get('P_bonf') is not None \
            else ('-', '-', '-')
        w(f"  {f['family_id']}: M = {f['M']}; smallest P_up {_num(f.get('min_P_up'))} ({f.get('min_track', '-')}); "
          f"Bonferroni P = {p}, Z_plus = {z}, {_bonf_label_text(f)}")
        for tid, why in f['broken']:
            w(f'    breaks the guarantee: {tid} ({why})')
        n1m = f['n1_max']
        w(f"    N1 maximum statistic: {n1m.get('label')}" + (f", flag {n1m['flag']}" if n1m.get('flag') else '') +
          (f"; {mc_text(n1m)}" if mc_text(n1m) else ''))
    w('')

    # ---------------------------------------------------------------- 6. per-track detail and notes
    w('=' * 100)
    w('PER-TRACK DETAIL')
    w('=' * 100)
    for (mid, vid, ro), tr in res['per_track'].items():
        w(f"{tr['track_id']}: status {tr['status']}; scored {len(tr['targets'])}; invalid cells "
          f"{dict(sorted(tr['invalid'].items())) or 'none'}")
    for (mid, vid), vr in res['per_variant'].items():
        w(f"{g}:{mid}:{vid}:WF (ranking): status {vr['status']}; scored {len(vr['targets'])}; invalid "
          f"{dict(sorted(vr['invalid'].items())) or 'none'}")
    w('')
    w('NOTES')
    w('- Every number above is computed from frozen forecasts and the actual development draws; no holdout draw is '
      'read or scored. Rankings are reports and change no forecast (R3 17.9 RK-1).')
    w('- Ties: standard competition ranking, listed by track ID (R3 17.10.4). Undefined values are listed last, '
      'never sorted as zero.')
    w('- LOW_N marks n < 30. GRID_INCOMPLETE tracks carry SELECTION_UNVERIFIED on their exact figures (design 6.2A).')
    w('- Not produced in this stage: MR2, MR3, MR6, MR8-MR15, the in-sample mode and the side-by-side tables (R3 '
      'stage 3).')
    text = ('\n'.join(L_) + '\n').encode('ascii', errors='replace')

    buf = io.StringIO()
    cols = ['table_kind', 'analysis_unit', 'unit_id', 'sub_measure', 'rank', 'n', 'descriptive_key', 'z_plus',
            'p_value', 'label', 'track_status', 'n1_mc_k', 'n1_mc_R', 'n1_mc_p', 'n1_mc_ci95_low_k_over_R',
            'n1_mc_ci95_high_k_over_R']
    wr = csv.DictWriter(buf, fieldnames=cols, lineterminator='\n')
    wr.writeheader()
    for r in csv_rows:
        wr.writerow({k: r.get(k, '') for k in cols})
    csv_bytes = buf.getvalue().encode('ascii', errors='replace')
    n1_figures = []
    for r in rows:
        for kind in ('significance', 'n1_reference'):
            m = mc_fields(r['sub'].get(kind))
            if m is not None:
                n1_figures.append({'unit_id': r['unit_id'], 'sub_measure': r['sub']['sub_measure'], 'block': kind,
                                   'label': r['sub'][kind].get('label'), 'k': m['k'], 'R': m['R'],
                                   'p_mc': str(m['p_mc']), 'ci95_k_over_R': [m['ci_low'], m['ci_high']]})
    manifest = {'schema': 'RANKING_REPORT_MANIFEST_V1', 'n1_figures': n1_figures, 'game_id': g, 'mode': 'WF', 'mode_display': mreg['modes']['WF']['display'],
                'evidence_tier': TIER, 'window_first': S, 'window_last': L, 'batch_id': plan['batch_id'],
                'attempt_id': res['attempt_id'], 'search_log_row': res['search_log_row'],
                'scoring_plan_digest': res['scoring_plan_digest'], 'grid_digest': res['grid_digest'],
                'cohort_digest': plan['cohort_digest'], 'master_sha256': plan['master_sha256'],
                'declared_tests': res['declared_tests'], 'families': _jsonable(fams), 'n1': seed_line,
                'n1_policies_on_file': n1_policies_on_file, 'tool': RP.TOOL, 'tool_version': RP.EVALUATOR_VERSION,
                'tool_sha256': RP.tool_sha256(), 'environment': environment, 'generated_utc': generated_utc,
                'track_status_counts': dict(status_counts), 'text_sha256': sha256_hex(text),
                'csv_sha256': sha256_hex(csv_bytes)}
    return {'txt': text, 'csv': csv_bytes, 'json': canonical(manifest)}


def write(res: dict, contents: dict, stamp: str) -> list[Path]:
    """Create-only files in results/method_rankings/<GAME>/ (R3 17.10.1); the attempt ID is part of each name."""
    g = res['game_id']
    folder = RP.roots()['reports'] / g
    folder.mkdir(parents=True, exist_ok=True)
    base = f"ranking_{g}_WF_{res['first']}-{res['last']}_{stamp}_{res['attempt_id']}"
    paths = []
    for ext in ('txt', 'csv', 'json'):
        p = folder / f'{base}.{ext}'
        CP.create_only(p, contents[ext])
        paths.append(p)
    return paths
