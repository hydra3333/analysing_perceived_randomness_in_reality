"""MHUP-B layer L4: the league table's rows, columns, order and labels (design supplement v0.8 section 3; code plan
v0.3 L4). PURE functions from the adapters' output (league_sources.collect) to the bytes of the `.txt` and `.csv`
members: the same input gives the same bytes. It reads no file, opens nothing for writing and rescores nothing.

 Rows     every released (method, revision, variant), current or retired, and any other identity a source scores.
 Columns  all scored draws (every summed score once, whatever its kind; NO P VALUE); forward only (class
          PROSPECTIVE) with the witness-verified count beside it; the last ten scored draws; then, in the second
          table, the split by kind, "Mode H as sealed" (shown, never added to a total), the WORST ticket, the Powerball
          barrel, prizes, and each variant's revision, release date, first and last scored draw, missing and failed.
 Order    by main-barrel hits above chance per draw over all scored draws, as an exact fraction; ties by identity
          (method, revision, variant). A variant with one scored draw is never ordered by its rate. NO_SCORES is
          unranked; LOW_N (under 30 draws) makes a rank provisional.
 Degraded a variant whose listed source is not available shows "not available: <source>" in place of a total.
"""
from __future__ import annotations

import csv
import io
from fractions import Fraction

import _common.owner_records as OR
import _common.weekly_records as WR
from _common.game_profiles import get_profile

LOW_N = 30
KINDS = ('DEVELOPMENT', 'CATCH_UP', 'LATE_PRE_DRAW', 'FORWARD')
ORDER_SENTENCE = 'A descriptive order. It does not select a winner and is not used to choose methods.'
RECONSTRUCTION_LABEL = 'current-cohort historical reconstruction as of {date}'
CSV_FIELDS = ('publication', 'game_id', 'rank', 'rank_provisional', 'method', 'revision', 'variant', 'status',
              'release_date', 'labels', 'not_available', 'all_draws', 'all_hits', 'all_chance', 'all_pct_vs_chance',
              'forward_draws', 'forward_hits', 'forward_chance', 'forward_witness_verified', 'last10_hits',
              'development_draws', 'development_hits', 'catch_up_draws', 'catch_up_hits', 'late_pre_draw_draws',
              'late_pre_draw_hits', 'mode_h_as_sealed_draws', 'mode_h_as_sealed_hits', 'worst_draws', 'worst_hits',
              'powerball_draws', 'powerball_hits', 'prize_draws', 'best_division', 'first_target', 'last_target',
              'missing_targets', 'failed_targets', 'exposure_flagged_draws')


def chance_per_draw(game_id: str) -> Fraction:
    """Expected main-barrel matches of a seven-number ticket in one fair draw: 7 x 7 / N."""
    return Fraction(49, WR.MAIN_POOL[game_id])


def dec(x: Fraction, places: int = 2, sign: bool = False) -> str:
    """An exact fraction as a decimal text, rounded half to even with whole-number arithmetic."""
    scaled = round(Fraction(x) * 10 ** places)
    s = f'{abs(scaled) // 10 ** places}.{abs(scaled) % 10 ** places:0{places}d}'
    return ('-' if scaled < 0 else '+' if sign else '') + s


def _blocked_by(data: dict, method: str, variant: str) -> str | None:
    for n in data['not_available']:
        if n['variants'] is None or [method, variant] in [list(v) for v in n['variants']]:
            return n['source']
    return None


def summarise(data: dict) -> list[dict]:
    """One entry per row of the table, in the table's order, every figure a whole number or an exact fraction."""
    game = data['game_id']
    per = chance_per_draw(game)
    people = {tuple(r[:3]): (r[3], r[4]) for r in data['roster']}
    for r in list(data['rows']) + data['mode_h']['rows']:
        people.setdefault((r['method'], r['revision'], r['variant']), ('-', 'RETIRED'))
    for ident in data['failed']:
        people.setdefault(tuple(ident[:3]), ('-', 'RETIRED'))
    by: dict[tuple, list] = {k: [] for k in people}
    for r in data['rows']:
        by[(r['method'], r['revision'], r['variant'])].append(r)
    sealed: dict[tuple, list] = {k: [] for k in people}
    for r in data['mode_h']['rows']:
        sealed[(r['method'], r['revision'], r['variant'])].append(r)
    out = []
    for key in sorted(people):
        top = sorted((r for r in by[key] if r['readout'] == 'TOP'), key=lambda r: r['target'])
        worst = [r for r in by[key] if r['readout'] == 'WORST']
        n, hits = len(top), sum(r['main'] for r in top)
        fwd = [r for r in top if r['kind'] == 'FORWARD']
        targets = [r['target'] for r in top]
        pb = [r for r in top if r['pb'] is not None]
        prizes = [r['division'] for r in top if r['division']]
        mh = [r for r in sealed[key] if r['readout'] == 'TOP']
        failed = sum(1 for f in data['failed'] if tuple(f[:3]) == key)
        e = {'method': key[0], 'revision': key[1], 'variant': key[2], 'release_date': people[key][0],
             'status': people[key][1], 'not_available': _blocked_by(data, key[0], key[2]),
             'all_draws': n, 'all_hits': hits, 'all_chance': n * per,
             'forward_draws': len(fwd), 'forward_hits': sum(r['main'] for r in fwd), 'forward_chance': len(fwd) * per,
             'forward_witness_verified': sum(1 for r in fwd if r['witnessed']),
             'last10_hits': sum(r['main'] for r in top[-10:]),
             'kinds': {k: (sum(1 for r in top if r['kind'] == k), sum(r['main'] for r in top if r['kind'] == k))
                       for k in KINDS},
             'mode_h': (len(mh), sum(r['main'] for r in mh)),
             'worst_draws': len(worst), 'worst_hits': sum(r['main'] for r in worst),
             'powerball_draws': len(pb), 'powerball_hits': sum(r['pb'] for r in pb),
             'prize_draws': len(prizes), 'best_division': min(prizes) if prizes else None,
             'first_target': targets[0] if targets else None, 'last_target': targets[-1] if targets else None,
             'missing_targets': (targets[-1] - targets[0] + 1 - len(set(targets))) if targets else 0,
             'failed_targets': failed,
             'exposure_flagged_draws': sum(1 for t in targets if OR.exposure_flag(game, t) is not None)}
        labels = []
        if e['not_available'] is None:
            labels += ['NO_SCORES'] if n == 0 else ['LOW_N'] if n < LOW_N else []
        if e['status'] == 'RETIRED':
            labels.append('RETIRED_AS_PUBLISHED')
        e['labels'] = labels
        out.append(e)

    def place(e):                                            # ranked first, by rate then identity; the rest by identity
        ranked = e['not_available'] is None and e['all_draws'] >= 2
        rate = Fraction(e['all_hits'], e['all_draws']) if ranked else Fraction(0)
        group = 0 if ranked else 1 if e['not_available'] is None and e['all_draws'] == 1 else 2
        return (group, -rate, e['method'], e['revision'], e['variant'])
    out.sort(key=place)
    rank = 0
    for e in out:
        if e['not_available'] is None and e['all_draws'] >= 2:
            rank += 1
            e['rank'] = rank
        else:
            e['rank'] = None
    return out


def rollup(entries: list[dict]) -> list[dict]:
    """By method and revision: variants, draws and hits summed over the method's variants, or 'not available'."""
    out: dict[tuple, dict] = {}
    for e in entries:
        r = out.setdefault((e['method'], e['revision']), {'method': e['method'], 'revision': e['revision'], 'variants': 0,
                                                         'draws': 0, 'hits': 0, 'chance': Fraction(0), 'not_available': None})
        r['variants'] += 1
        r['draws'] += e['all_draws']
        r['hits'] += e['all_hits']
        r['chance'] += e['all_chance']
        r['not_available'] = r['not_available'] or e['not_available']
    return [out[k] for k in sorted(out)]


def _pct(hits: int, chance: Fraction) -> str:
    return '-' if not chance else dec((hits - chance) / chance * 100, 2, sign=True)


def _table(head: list[str], rows: list[list[str]]) -> list[str]:
    widths = [max(len(str(c)) for c in col) for col in zip(head, *rows)] if rows else [len(h) for h in head]
    fmt = lambda cells: '  '.join(str(c).ljust(w) for c, w in zip(cells, widths)).rstrip()
    return [fmt(head), fmt(['-' * w for w in widths]), *[fmt(r) for r in rows]]


def header_lines(data: dict, identity: dict) -> list[str]:
    game = data['game_id']
    p = get_profile(game)
    n_pool = WR.MAIN_POOL[game]
    pins = data['pins']
    out = [f'LEAGUE TABLE - {game} - latest scored draw {identity["latest_draw"]} - version {identity["version"]} - '
           f'{identity["published_utc"]}',
           f'Publication: {identity["name"]}',
           '',
           ORDER_SENTENCE,
           'No P value is given in this table. Every figure counts each scored draw once, whatever its kind.',
           f'Game: seven numbers from {n_pool}; a seven-number ticket is expected to match {chance_per_draw(game)} '
           f'main numbers a draw by chance' + ('; Powerball barrel: one number from 20, chance 1/20 a draw.'
                                               if game == 'POWERBALL' else '.'),
           '',
           'Sources summed into "all scored draws" (each named by identity):',
           f'  weekly score ledger: {pins["weekly_score_ledger"]["lines"]} lines, sha256 '
           f'{pins["weekly_score_ledger"]["sha256"]}; forecast ledger: {pins["forecast_ledger"]["lines"]} lines; '
           f'witness ledger: {pins["witness_ledger"]["lines"]} lines']
    for s in data['sources']:
        gone = next((n['reason'] for n in data['not_available'] if n['source'] == s['attempt_id']), None)
        out.append(f'  development attempt {s["attempt_id"]} (batch {s["batch_id"]}, {s["batch_kind"]}, draws '
                   f'{s["window_first"]}-{s["window_last"]}, score ledger sha256 {s["score_ledger_sha256"]})' +
                   (f' - NOT AVAILABLE: {gone}' if gone else ''))
    if not data['sources']:
        out.append('  no development attempt is listed yet')
    out.append('Source list: ' + (f'LEAGUE_SOURCES_{game}.json sha256 {data["sources_file_sha256"]}'
                                  if data['sources_file_sha256'] else 'not written yet'))
    mh = data['mode_h']
    out.append('Shown, never summed - Mode H as sealed: ' + (
        f'batch {mh["identity"]["batch_id"]}, attempt {mh["identity"]["attempt_id"]}, ledger sha256 '
        f'{mh["identity"]["score_ledger_sha256"]}' if mh['identity'] else f'not available: {mh["not_available"]}'))
    scored = sorted({r['target'] for r in data['rows']})
    if scored:
        out.append(f'The all-draws column starts at draw {scored[0]} and ends at draw {scored[-1]} (the earliest and latest '
                   f'draw any summed source scores; the era starts at draw {p.first_draw}).')
    else:
        out.append('No summed source holds a score yet.')
    if data['amendments']:
        out.append(f'Corrections on file: {data["amendments"]}. The table uses the routine score of every key; a '
                   f'correction stands beside it in the score ledger.')
    if data['unavailable_readouts']:
        out.append(f'Readouts a forecast did not give (not scored): {data["unavailable_readouts"]}.')
    flagged = sorted({t for t in scored if OR.exposure_flag(game, t) is not None})
    if flagged:
        out.append('Exposure flags (information only; the draws are scored and counted like any other): ' +
                   ', '.join(f'draw {t} {OR.exposure_flag(game, t)["decision"]}' for t in flagged) +
                   f' ({OR.EXPOSURE_RECORD}).')
    out += ['',
            'Labels: LOW_N = fewer than 30 scored draws (a rank marked * is provisional). NO_SCORES = no eligible score, '
            'unranked.',
            'RETIRED_AS_PUBLISHED = a retired or superseded revision, shown as it was scored; never merged with a '
            'current revision.',
            'Forward = class PROSPECTIVE only (frozen before its draw by local timing); "witnessed" counts those whose '
            'freeze line has a verified witness received before the draw. LATE_PRE_DRAW is counted once in all scored '
            'draws and never in the forward column.',
            'Missing = draws between a variant\'s first and last scored draw with no score; failed = recorded '
            'prediction failures.']
    return out


def build(data: dict, identity: dict) -> dict:
    """The two members of one publication: {'txt': bytes, 'csv': bytes}."""
    game = data['game_id']
    entries = summarise(data)
    na = lambda e, text: f'not available: {e["not_available"]}' if e['not_available'] else text
    lines = header_lines(data, identity)
    lines += ['', 'ROLL-UP BY METHOD (all scored draws, TOP ticket, main barrel; summed over the method\'s variants)']
    lines += _table(['Method', 'Rev', 'Variants', 'Draws', 'Hits', 'Chance', '+/- %'],
                    [[r['method'], r['revision'], r['variants'],
                      *([f'not available: {r["not_available"]}', '', '', ''] if r['not_available'] else
                        [r['draws'], r['hits'], dec(r['chance']), _pct(r['hits'], r['chance'])])]
                     for r in rollup(entries)])
    lines += ['', 'MAIN TABLE (TOP ticket: the seven most favoured numbers; main barrel)']
    rows = []
    for e in entries:
        rank = '-' if e['rank'] is None else f'{e["rank"]}{"*" if "LOW_N" in e["labels"] else ""}'
        rows.append([rank, e['method'], e['revision'], e['variant'],
                     *([na(e, ''), '', '', ''] if e['not_available'] else
                       [e['all_draws'], e['all_hits'], dec(e['all_chance']), _pct(e['all_hits'], e['all_chance'])]),
                     e['forward_draws'], e['forward_hits'], dec(e['forward_chance']), e['forward_witness_verified'],
                     '-' if e['not_available'] else e['last10_hits'], ' '.join(e['labels'])])
    lines += _table(['Rank', 'Method', 'Rev', 'Variant', 'All:Draws', 'Hits', 'Chance', '+/- %', 'Fwd:Draws', 'Hits',
                     'Chance', 'Witnessed', 'Last10', 'Labels'], rows)
    lines += ['', 'BY KIND (TOP ticket, main barrel; draws/hits). "Mode H as sealed" is history: shown, never added to a total.']
    kd = lambda pair: f'{pair[0]}/{pair[1]}'
    lines += _table(['Method', 'Rev', 'Variant', 'Development', 'Catch-up', 'LATE_PRE_DRAW', 'Forward', 'Mode H as sealed'],
                    [[e['method'], e['revision'], e['variant'],
                      *([na(e, ''), '', '', ''] if e['not_available'] else [kd(e['kinds'][k]) for k in KINDS]),
                      kd(e['mode_h']) if data['mode_h']['identity'] else 'not available'] for e in entries])
    lines += ['', 'OTHER READOUTS AND DETAILS (draws/hits; prizes = scored draws that won any division, with the best)']
    lines += _table(['Method', 'Rev', 'Variant', 'Status', 'Released', 'WORST', *(['Powerball'] if game == 'POWERBALL' else []),
                     'Prizes', 'First', 'Last', 'Missing', 'Failed', 'Flagged'],
                    [[e['method'], e['revision'], e['variant'], e['status'], e['release_date'],
                      na(e, f'{e["worst_draws"]}/{e["worst_hits"]}'),
                      *([na(e, f'{e["powerball_draws"]}/{e["powerball_hits"]}')] if game == 'POWERBALL' else []),
                      na(e, f'{e["prize_draws"]}' + (f' (best division {e["best_division"]})' if e['best_division'] else '')),
                      e['first_target'] or '-', e['last_target'] or '-', e['missing_targets'], e['failed_targets'],
                      e['exposure_flagged_draws']] for e in entries])
    text = ('\n'.join(lines) + '\n').encode('ascii')

    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(CSV_FIELDS)
    for e in entries:
        gone = e['not_available'] is not None
        cell = lambda v: '' if gone else v
        w.writerow([identity['name'], game, '' if e['rank'] is None else e['rank'],
                    'yes' if e['rank'] is not None and 'LOW_N' in e['labels'] else 'no', e['method'], e['revision'],
                    e['variant'], e['status'], e['release_date'], ';'.join(e['labels']), e['not_available'] or '',
                    cell(e['all_draws']), cell(e['all_hits']), cell(str(e['all_chance'])),
                    cell(_pct(e['all_hits'], e['all_chance'])),
                    e['forward_draws'], e['forward_hits'], str(e['forward_chance']), e['forward_witness_verified'],
                    cell(e['last10_hits']),
                    *[cell(x) for k in KINDS[:3] for x in e['kinds'][k]],          # forward has its own columns
                    *(e['mode_h'] if data['mode_h']['identity'] else ('', '')),
                    cell(e['worst_draws']), cell(e['worst_hits']),
                    cell(e['powerball_draws']) if game == 'POWERBALL' else '',
                    cell(e['powerball_hits']) if game == 'POWERBALL' else '',
                    cell(e['prize_draws']), cell(e['best_division'] or ''),
                    e['first_target'] or '', e['last_target'] or '', e['missing_targets'], e['failed_targets'],
                    e['exposure_flagged_draws']])
    return {'txt': text, 'csv': buf.getvalue().encode('ascii')}


def latest_draw(data: dict) -> int:
    """The latest draw any summed source scores (0 when there is none): part of a publication's identity."""
    return max((r['target'] for r in data['rows']), default=0)


def reconstruction(data: dict, as_of: str) -> bytes:
    """Sup 5.3: one row per draw and CURRENT variant: that draw's matches, running totals and the rank after that draw,
    every row labelled. It is not what was published at those dates: a variant released later appears from the first
    draw with its back-history, and a column says whether the variant was released at that draw's date."""
    game = data['game_id']
    p = get_profile(game)
    label = RECONSTRUCTION_LABEL.format(date=as_of)
    current = {tuple(r[:3]): r[3] for r in data['roster'] if r[4] == 'CURRENT'}
    top = [r for r in data['rows'] if r['readout'] == 'TOP' and (r['method'], r['revision'], r['variant']) in current]
    by_target: dict[int, list] = {}
    for r in top:
        by_target.setdefault(r['target'], []).append(r)
    running = {k: [0, 0] for k in current}
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow([label])
    w.writerow(['label', 'game_id', 'target', 'method', 'revision', 'variant', 'kind', 'matches', 'running_draws',
                'running_hits', 'rank_after_this_draw', 'released_at_this_draw_date'])
    for t in sorted(by_target):
        day = str(p.derived_date(t))
        for r in by_target[t]:
            k = (r['method'], r['revision'], r['variant'])
            running[k][0] += 1
            running[k][1] += r['main']
        order = sorted((k for k in current if running[k][0] >= 2),
                       key=lambda k: (-Fraction(running[k][1], running[k][0]), k))
        rank = {k: i for i, k in enumerate(order, start=1)}
        for r in sorted(by_target[t], key=lambda r: (r['method'], r['revision'], r['variant'])):
            k = (r['method'], r['revision'], r['variant'])
            w.writerow([label, game, t, *k, r['kind'], r['main'], running[k][0], running[k][1], rank.get(k, ''),
                        'yes' if current[k] != '-' and current[k] <= day else 'no'])
    return buf.getvalue().encode('ascii')
