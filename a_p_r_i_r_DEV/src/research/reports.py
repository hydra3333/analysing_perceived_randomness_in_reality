"""The saved reports: the league tables, the next-draw reports and the two OV-1 print-outs.

What this file is for
    Reports are print-outs for the owner. They are made from the lists, the results and the status files alone,
    and are made again whenever those change: a file is written only when its bytes would differ from what is
    on disk, so the reports folder always shows exactly what the installed code makes of the current records and
    an unchanged report is left untouched. Nothing here is evidence and nothing here is ever read back by the
    job. The time each file was made is kept in a side file, so that the same records give the same report
    bytes.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 9 (saved reports) and 10.5 and 10.6 (the
    two OV-1 print-outs), with the words of the simple scheme v0.2: "retired" and "method", and both OV-1 series
    exploratory (section 5 step 6), so that the second series' print-out claims no error bound. Since the scheme
    nothing is set aside as "not current": what no longer fits is made again.

Which of the project's own modules it uses
    research.game_state     GameRecords, MAIN_BARREL: the game's records in memory
    research.ov1_numeric    BAR, the kernel's bar, for the print-outs
    research.variant_lists  RESEARCH_FOLDER
    research.windows_text   windows_lines, LINE_ENDING: every report file is written with each line ending CRLF
    _common.game_profiles   get_profile: the barrels' sizes

What uses it
    research/research_job.py, and the engine's tests.
"""
from __future__ import annotations

import csv
import io
import os
import textwrap
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

from _common.game_profiles import get_profile
from research import ov1_numeric as kernel
from research.game_state import MAIN_BARREL, GameRecords
from research.variant_lists import RESEARCH_FOLDER
from research.windows_text import LINE_ENDING, windows_lines

# The folders and files of specification section 9, under results/research/<GAME>/.
REPORTS_FOLDER = 'reports'
MADE_TIMES_NAME = 'made_times.csv'
README_NAME = 'README.txt'
LEAGUE_HEADLINE = 'A descriptive order. It selects nothing.'
REBUILT_NOTE = ('rebuilt with the current population: a method\'s figures at draws before its installation were '
                'computed afterwards; this is not a table published at that draw\'s date')
EXPLORATORY_HEADLINE = ('OV-1 EXPLORATORY RETROSPECTIVE - over all draws; no error bound applies; 40 is a '
                        'reference line only')
# What the second OV-1 series is, as its print-out says it in every tree. Both series are exploratory indicators
# (the simple scheme v0.2 section 5 step 6, and the reviewer's clarification 3 of entry 341): no error bound is
# claimed for either.
PREVAILING_CLAIM = (
    'An exploratory indicator, like the series over all draws: the same OV-1 calculation, with each method counted '
    'only from the draw after its establishment draw (the last draw this tree held when that version of the '
    'method was first used here) up to, and not including, the draw it is retired from. No error bound is claimed '
    'for it: methods are added, corrected and retired as the research goes on, and this score is not kept free of '
    'those choices. 40 is a reference line only. The software checks that each forecast was computed from earlier '
    'draws only and that every draw is taken once.')
NOT_STARTED_TEXT = 'prevailing OV-1: not started; no method has an establishment draw yet'
# The claim is one long sentence group; the text report breaks it into lines of at most this many characters.
CLAIM_LINE_WIDTH = 110
# How many of a method's latest scored draws the league table shows one by one.
LAST_DRAWS_SHOWN = 10


def reports_root(tree_root: Path, game_id: str) -> Path:
    """The active reports folder of a game, for example <tree>/results/research/POWERBALL/reports."""
    return Path(tree_root) / RESEARCH_FOLDER / game_id / REPORTS_FOLDER


def league_names(game_id: str, draw: int) -> tuple:
    """The two league files of a draw, from the reports folder, for example
    ('league/league_POWERBALL_d01601.txt', 'league/league_POWERBALL_d01601.csv')."""
    stem = f'league/league_{game_id}_d{draw:05d}'
    return stem + '.txt', stem + '.csv'


def next_draw_names(game_id: str, draw: int) -> tuple:
    """The two next-draw files of a draw, for example ('next/next_draw_POWERBALL_d01602.txt', '... .csv')."""
    stem = f'next/next_draw_{game_id}_d{draw:05d}'
    return stem + '.txt', stem + '.csv'


def ov1_names(game_id: str, which: str) -> tuple:
    """The two files of an OV-1 print-out; which is 'prevailing' or 'exploratory'."""
    stem = f'ov1/ov1_{which}_{game_id}'
    return stem + '.txt', stem + '.csv'


def fixed(value: Fraction, places: int = 3) -> str:
    """An exact fraction as text with a fixed number of decimal places, rounded half away from zero, for example
    fixed(Fraction(49, 35)) is '1.400' and fixed(Fraction(-1, 3)) is '-0.333'. No floating point is used, so the
    same records give the same text on every machine."""
    scaled = abs(value) * 10 ** places
    whole = (2 * scaled.numerator + scaled.denominator) // (2 * scaled.denominator)
    text = f'{whole // 10 ** places}.{whole % 10 ** places:0{places}d}' if places else str(whole)
    return ('-' if value < 0 and whole else '') + text


class ReportWriter:
    """Writes report files of one game, each only if its bytes would change, and remembers what it wrote.

    root: the game's active reports folder.  made: the time of making, as text, for the side file.
    written: the names (from the reports folder) of the files this job wrote.
    """

    def __init__(self, tree_root: Path, game_id: str, made: str):
        """tree_root, game_id: whose reports.  made: the time of making, for example '2026-12-01 20:10'."""
        self.root = reports_root(tree_root, game_id)
        self.made = made
        self.written = []

    def write(self, name: str, text: str) -> bool:
        """Write one report file unless the file on disk already holds exactly these bytes.

        name: the file, from the reports folder, forward slashes.  text: its content as the code built it (ASCII;
        lines end in LF). It is written in the standard's form, each line ending CRLF.
        Returns True if the file was written. The bytes go to a temporary name first and are then renamed, so a
        crash leaves the old file or the new one.
        """
        data = windows_lines(text).encode('ascii')
        path = self.root / name
        if path.is_file() and path.read_bytes() == data:
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + '.writing')
        with open(temporary, 'wb') as stream:
            stream.write(data)
        os.replace(temporary, path)
        self.written.append(name)
        # The time is noted at once, at the end of the side file, so that a job that is interrupted has still
        # recorded when it made each file; tidy_times puts the side file in order at the end of the job.
        with open(self.root / MADE_TIMES_NAME, 'a', encoding='ascii', newline=LINE_ENDING) as stream:
            stream.write(f'{name},{self.made}\n')
        return True

    def tidy_times(self) -> None:
        """Put the side file of making times in order: one row for each report file in the active folder, with
        the latest time noted for it, sorted by name."""
        path = self.root / MADE_TIMES_NAME
        if not path.is_file():
            return
        times = {}
        for row in csv.reader(io.StringIO(path.read_text(encoding='ascii'))):
            if len(row) == 2 and row[0] != 'file':
                times[row[0]] = row[1]
        text = 'file,made\n' + ''.join(f'{name},{when}\n' for name, when in sorted(times.items())
                                       if (self.root / name).is_file())
        data = windows_lines(text).encode('ascii')
        # Compared as bytes, so that a side file in another form is put right as well as one in another order.
        if path.read_bytes() != data:
            temporary = path.with_name(path.name + '.writing')
            temporary.write_bytes(data)
            os.replace(temporary, path)


def preamble(records: GameRecords, title: str, runs_to, variants: int) -> list:
    """The lines every report begins with: its title, the game, the draw it runs to, how many methods it holds,
    the tree that made it, the foreign lists that were ignored, and any marker that derived results are not
    current.

    runs_to: a draw number, or None for "no draw yet".  variants: how many methods the report holds.
    """
    held = [f'{state.variant.identity} (installed, held: {state.foreign_reason})' for state in records.states
            if state.held]
    foreign = held + [f'{identity} (not installed here)' for identity in records.foreign]
    lines = [title,
             f'Game: {records.game_id}    Runs to draw: {runs_to if runs_to is not None else "none yet"}    '
             f'Methods: {variants}',
             f'Made by: the {records.role} tree at {records.tree_root}    (time of making: see {MADE_TIMES_NAME})',
             'Foreign lists ignored: ' + ('; '.join(foreign) if foreign else 'none')]
    if records.cutoff is not None:
        lines.append(f'RESULTS NOT CURRENT FROM DRAW {records.cutoff[0]} ({records.cutoff[1]}): no report is made '
                     f'for that draw or a later one until the owner settles it.')
    return lines


def as_csv(preamble_lines: list, header: list, rows: list) -> str:
    """A report's CSV text: the preamble as lines beginning '# ', then the column names, then the rows."""
    out = io.StringIO()
    out.write(''.join(f'# {line}\n' for line in preamble_lines))
    writer = csv.writer(out, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(rows)
    return out.getvalue()


def as_table(header: list, rows: list) -> list:
    """A list of rows as text lines with columns padded to their widest cell (text left, the rest as given)."""
    cells = [[str(cell) for cell in row] for row in [header] + rows]
    widths = [max(len(row[column]) for row in cells) for column in range(len(header))]
    return ['  '.join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip() for row in cells]


class LeagueTable:
    """The cumulative league figures of one game, built draw by draw.

    add_draw(T) takes in every variant's line for draw T; render(T) then gives the report for T: each variant
    over every draw up to T it has a score for. Variants that are held are left out (their lists are foreign).
    """

    def __init__(self, records: GameRecords):
        """records: the game's records in memory. The table reads them as they stand when each draw is added."""
        self.records = records
        self.profile = get_profile(records.game_id)
        self.barrel_sizes = {b.barrel_id: b.high - b.low + 1 for b in self.profile.barrels}
        self.side_barrel = 'POWERBALL' if 'POWERBALL' in self.barrel_sizes else None
        self.rows = {}

    def _row(self, identity: str) -> dict:
        """The running figures of one variant (made on first use)."""
        return self.rows.setdefault(identity, {
            'draws': 0, 'hits': Counter(), 'side_hits': Counter(), 'side_selected': 0,
            'divisions': {'top': Counter(), 'worst': Counter()}, 'last': deque(maxlen=LAST_DRAWS_SHOWN),
            'first': None, 'before': 0, 'after': 0, 'no_forecast': Counter()})

    def add_draw(self, draw: int) -> bool:
        """Take in every variant's line for one draw. Returns True if any variant has a score for it."""
        any_score = False
        for state in self.records.workable:
            facts = state.targets.get(draw)
            if facts is None:
                continue
            row = self._row(state.variant.identity)
            if facts.status != 'FORECAST':
                row['no_forecast'][facts.reason] += 1
                continue
            score = state.score_contents.get(draw)
            if score is None:
                continue
            any_score = True
            row['draws'] += 1
            row['first'] = draw if row['first'] is None else row['first']
            row['after' if facts.result_on_file else 'before'] += 1
            main = score['matches'][MAIN_BARREL]
            row['last'].append((main['top'], main['worst']))
            for which in ('top', 'worst'):
                row['hits'][which] += main[which]
                row['divisions'][which][score['divisions'][which]] += 1
                if self.side_barrel:
                    row['side_hits'][which] += score['matches'][self.side_barrel][which]
            if self.side_barrel:
                row['side_selected'] = len(facts.sets[self.side_barrel]['top'])
        return any_score

    def render(self, draw: int) -> tuple:
        """The league report for a draw, from the figures taken in so far.

        Returns (the .txt text, the .csv text).
        """
        chance = Fraction(7 * 7, self.barrel_sizes[MAIN_BARREL])
        figures = []
        for state in self.records.workable:
            identity = state.variant.identity
            row = self.rows.get(identity) or self._row(identity)
            draws = row['draws']
            per = {which: (Fraction(row['hits'][which], draws) if draws else None) for which in ('top', 'worst')}
            figures.append((state, row, per))
        scored = [entry for entry in figures if entry[1]['draws']]
        top_order = sorted(scored, key=lambda e: (-e[2]['top'], e[0].variant.identity))
        worst_rank = {e[0].variant.identity: rank for rank, e in enumerate(
            sorted(scored, key=lambda e: (e[2]['worst'], e[0].variant.identity)), start=1)}
        ordered = top_order + sorted((e for e in figures if not e[1]['draws']), key=lambda e: e[0].variant.identity)
        header = ['order_top', 'method', 'draws_scored', 'top_hits', 'top_hits_a_draw', 'chance_hits_a_draw',
                  'top_difference_a_draw', 'top_difference_percent', f'top_last_{LAST_DRAWS_SHOWN}', 'worst_hits',
                  'worst_hits_a_draw', 'worst_difference_a_draw', 'worst_difference_percent',
                  f'worst_last_{LAST_DRAWS_SHOWN}', 'order_worst', 'top_minus_worst_a_draw']
        if self.side_barrel:
            header += ['powerball_top_hits', 'powerball_worst_hits', 'powerball_chance_hits']
        header += ['top_divisions', 'worst_divisions', 'first_scored_draw', 'scored_forecasts_made_before_result',
                   'scored_forecasts_made_after_result', 'prevailing_ov1_first_draw',
                   'no_forecast_insufficient_history', 'no_forecast_method_failed', 'note']
        short = ['#', 'method', 'draws', 'TOP hits', 'TOP/draw', 'chance', 'TOP diff', 'TOP %', 'TOP last',
                 'WORST hits', 'WORST/draw', 'WORST diff', 'WORST %', 'WORST last', 'W#', 'T-W/draw']
        if self.side_barrel:
            short += ['PB TOP', 'PB WORST', 'PB chance']
        short += ['TOP divs', 'WORST divs', 'first', 'before', 'after', 'OV-1 from', 'NF hist', 'NF fail', 'note']
        rows, rebuilt = [], False
        for position, (state, row, per) in enumerate(ordered, start=1):
            draws, identity = row['draws'], state.variant.identity
            rebuilt = rebuilt or row['after'] > 0

            def figure(which: str) -> list:
                """Hits, hits a draw, difference a draw and in per cent, and the last draws, for TOP or WORST."""
                if not draws:
                    return [0, '-', '-', '-', '-']
                difference = per[which] - chance
                return [row['hits'][which], fixed(per[which]), fixed(difference), fixed(difference / chance * 100, 1),
                        ''.join(str(pair[0 if which == 'top' else 1]) for pair in row['last'])]

            top, worst = figure('top'), figure('worst')
            cells = [position if draws else '-', identity, draws, top[0], top[1], fixed(chance), top[2], top[3],
                     top[4] or '-', worst[0], worst[1], worst[2], worst[3], worst[4] or '-',
                     worst_rank.get(identity, '-'), fixed(per['top'] - per['worst']) if draws else '-']
            if self.side_barrel:
                cells += [row['side_hits']['top'], row['side_hits']['worst'],
                          fixed(Fraction(draws * row['side_selected'], self.barrel_sizes[self.side_barrel]))
                          if draws else '-']
            cells += [self._divisions(row['divisions'][which]) for which in ('top', 'worst')]
            cells += [row['first'] if row['first'] is not None else '-', row['before'], row['after'],
                      state.status.eligible_from if state.status.eligible_from is not None else '-',
                      row['no_forecast']['INSUFFICIENT_HISTORY'], row['no_forecast']['METHOD_FAILED'],
                      self._note(state, draw)]
            rows.append(cells)
        lines = preamble(self.records, f'LEAGUE TABLE - {self.records.game_id} - through draw {draw}', draw, len(rows))
        lines.append(LEAGUE_HEADLINE)
        lines += ['Ordered by TOP hits above chance a draw (ties by name). "W#": the order by WORST hits a draw, 1 = '
                  'fewest.',
                  'Chance: seven times seven over the barrel size, a draw. "diff" and "%": hits a draw above chance.',
                  f'"last": the main-barrel hits at each of the latest {LAST_DRAWS_SHOWN} scored draws, oldest first. '
                  f'Divisions: <division>x<times won>.',
                  '"first": first scored draw. "before" and "after": scored forecasts made before and after the result '
                  'was on file.',
                  '"OV-1 from": first draw in the prevailing OV-1. "NF": NO_FORECAST lines, by reason. "PB": the '
                  'Powerball barrel.',
                  'The .csv beside this file holds the same columns under their full names.']
        if rebuilt:
            lines.append(REBUILT_NOTE)
        text = '\n'.join(lines + [''] + as_table(short, rows)) + '\n'
        return text, as_csv(lines, header, rows)

    @staticmethod
    def _divisions(counts: Counter) -> str:
        """Prize divisions won as text, for example '8x3 9x12'; '-' if none."""
        won = sorted((division, times) for division, times in counts.items() if division)
        return ' '.join(f'{division}x{times}' for division, times in won) or '-'

    @staticmethod
    def _note(state, draw: int) -> str:
        """The status note of a method in a league report: its retirement, and a forecast left unscored by it."""
        withdrawn_from = state.status.withdrawn_from
        if withdrawn_from is None:
            return ''
        note = f'RETIRED from draw {withdrawn_from}: {state.status.withdrawn_reason}'
        facts = state.targets.get(withdrawn_from)
        if facts is not None and facts.status == 'FORECAST' and draw >= withdrawn_from:
            note += f' (its forecast for draw {withdrawn_from}: not scored: retired)'
        return note


def next_draw_report(records: GameRecords, draw: int) -> tuple:
    """The next-draw report for a draw: what each method forecast for it.

    Returns (the .txt text, the .csv text). One row for each method that is not held and has a line for the
    draw, or is retired from a draw at or below it.
    """
    barrels = [b.barrel_id for b in get_profile(records.game_id).barrels]
    header = ['method', 'line']
    for barrel in barrels:
        header += [f'{barrel.lower()}_top', f'{barrel.lower()}_worst']
    header += ['made_before_the_result_was_on_file', 'note']
    rows = []
    for state in sorted(records.workable, key=lambda s: s.variant.identity):
        facts = state.targets.get(draw)
        withdrawn = state.status.is_withdrawn_at(draw)
        if facts is None and not withdrawn:
            continue
        note = ''
        if withdrawn:
            note = f'RETIRED from draw {state.status.withdrawn_from}: {state.status.withdrawn_reason}'
        if facts is None:
            rows.append([state.variant.identity, 'none'] + ['-'] * (2 * len(barrels)) + ['-', note])
            continue
        cells = [state.variant.identity, facts.status if facts.status == 'FORECAST' else f'NO_FORECAST: {facts.reason}']
        for barrel in barrels:
            for which in ('top', 'worst'):
                cells.append(' '.join(str(n) for n in sorted(facts.sets[barrel][which])) if facts.sets else '-')
        cells += ['no' if facts.result_on_file else 'yes', note]
        rows.append(cells)
    lines = preamble(records, f'NEXT-DRAW FORECASTS - {records.game_id} - draw {draw}', draw, len(rows))
    lines.append('What each method forecast for this draw: its TOP and WORST numbers in each barrel. A descriptive '
                 'list. It selects nothing.')
    lines.append(prevailing_status_line(records))
    return '\n'.join(lines + [''] + as_table(header, rows)) + '\n', as_csv(lines, header, rows)


def prevailing_status_line(records: GameRecords) -> str:
    """One line saying where the prevailing OV-1 stands, for example 'prevailing OV-1: lines for draws 1592 to
    1600; score (proved lower bound) 0; reference line 40: not reached'."""
    eligible = [s.status.eligible_from for s in records.states if s.status.eligible_from is not None]
    if not eligible:
        return NOT_STARTED_TEXT
    if not records.ledger_lines:
        text = f'prevailing OV-1: starts at draw {min(eligible)}; no line yet'
    else:
        last = records.ledger_lines[-1]['content']
        text = (f'prevailing OV-1: lines for draws {records.ledger_lines[0]["content"]["draw"]} to {last["draw"]}; '
                f'score (proved lower bound) {last["score_lower_bound"]}; reference line {kernel.BAR}: '
                + ('reached' if any(line['content']['crossed'] for line in records.ledger_lines) else 'not reached'))
    return text + (f'; BLOCKED: {records.blocked}' if records.blocked else '')


def _ov1_rows(lines: list) -> tuple:
    """The table rows of an OV-1 print-out, one a draw, from draw_line results or ledger lines."""
    header = ['draw', 'counted', 'no_pair', 'x', 'z', 'variance', 'score_lower_bound', 'reached_40',
              'counted_made_before_result', 'counted_made_after_result', 'rerun']
    rows = []
    for line in lines:
        content, audit = line['content'], line.get('audit', {})
        counted = sum(1 for member in content['cohort'] if member['state'] == 'counted')
        rows.append([content['draw'], counted, len(content['cohort']) - counted, content['x'],
                     content['z'] if content['z'] is not None else 'factor exactly 1',
                     f'{content["variance"][0]}/{content["variance"][1]}', content['score_lower_bound'],
                     'yes' if content['crossed'] else 'no', audit.get('counted_before_result', '-'),
                     audit.get('counted_after_result', '-'), (line.get('envelope') or {}).get('rerun') or '-'])
    return header, rows


def _ov1_counts(records: GameRecords, lines: list) -> list:
    """The plain counts printed beside an OV-1 score, taken from the lines' audit parts and envelopes."""
    before = sum(line.get('audit', {}).get('counted_before_result', 0) for line in lines)
    after = sum(line.get('audit', {}).get('counted_after_result', 0) for line in lines)
    where = Counter()
    for line in lines:
        where.update(line.get('audit', {}).get('computed_in', {}))
    reruns = Counter((line.get('envelope') or {}).get('rerun') for line in lines)
    reruns.pop(None, None)
    no_pair = [line['content']['draw'] for line in lines
               if any(member['state'] != 'counted' for member in line['content']['cohort'])]
    return [f'The tree that made this report: {records.role} at {records.tree_root}',
            f'Draws counted: {len(lines)}',
            f'Counted forecasts made before the result was on file: {before}; after: {after}',
            'Draws whose lines were written by a historical walk-forward rerun: '
            + ('; '.join(f'{name}: {times}' for name, times in sorted(reruns.items())) if reruns else '0'),
            'Where the counted forecasts were computed: '
            + ('; '.join(f'{role} {times}' for role, times in sorted(where.items())) if where else 'none yet'),
            'Lines with a "no pair" member: ' + (f'{len(no_pair)}, the first at draw {no_pair[0]}' if no_pair else '0')]


def prevailing_report(records: GameRecords) -> tuple:
    """The prevailing OV-1 print-out, from the stored ledger. Returns (the .txt text, the .csv text)."""
    lines_on_file = records.ledger_lines
    runs_to = lines_on_file[-1]['content']['draw'] if lines_on_file else None
    cohort_now = len(lines_on_file[-1]['content']['cohort']) if lines_on_file else 0
    lines = preamble(records, f'OV-1 PREVAILING SCORE - {records.game_id}', runs_to, cohort_now)
    lines += [''] + textwrap.wrap(PREVAILING_CLAIM, CLAIM_LINE_WIDTH) + ['', prevailing_status_line(records)]
    lines += _ov1_counts(records, lines_on_file)
    header, rows = _ov1_rows(lines_on_file)
    return '\n'.join(lines + [''] + as_table(header, rows)) + '\n', as_csv(lines, header, rows)


def exploratory_report(records: GameRecords, series: list) -> tuple:
    """The exploratory OV-1 print-out, from ov1_ledger.exploratory_series. Returns (the .txt, the .csv text)."""
    runs_to = series[-1]['content']['draw'] if series else None
    lines = preamble(records, EXPLORATORY_HEADLINE, runs_to, len(records.workable))
    lines += [f'OV-1 exploratory - {records.game_id}: the same calculation over every draw that has any scored '
              f'pair, counting every method wherever it has one.']
    if series:
        last = series[-1]['content']
        lines.append(f'Value now (not a bound on any error): {last["score_lower_bound"]}; reference line '
                     f'{kernel.BAR}: ' + ('reached' if any(l['content']['crossed'] for l in series) else 'not reached'))
    lines += _ov1_counts(records, series)[1:]
    header, rows = _ov1_rows(series)
    return '\n'.join(lines + [''] + as_table(header, rows)) + '\n', as_csv(lines, header, rows)


def readme_text(game_id: str) -> str:
    """The README of a game's reports folder: what each file is, in plain words."""
    return '\n'.join([
        f'Reports of the research system - {game_id}',
        '',
        'These files are print-outs. They are made from the forecast and score lists, the accepted results and the',
        'status files, and are made again whenever those change. They are not evidence and nothing reads them back.',
        'Do not edit them: the next job would replace an edited file.',
        '',
        f'league/league_{game_id}_d<draw>.txt and .csv',
        '    One for every draw that has any score: each method over every draw up to that one. A descriptive',
        '    order. It selects nothing.',
        f'next/next_draw_{game_id}_d<draw>.txt and .csv',
        '    What each method forecast for a draw. One for every draw that some forecast was made for before its',
        '    result was on file.',
        f'ov1/ov1_prevailing_{game_id}.txt and .csv',
        '    The second OV-1 series: one line a draw, each method counted from its establishment draw until it',
        '    is retired. Exploratory, like the one below; with the counts that say what kind of evidence it is.',
        f'ov1/ov1_exploratory_{game_id}.txt and .csv',
        '    The same calculation over all scored history. A retrospective: no error bound applies.',
        f'{MADE_TIMES_NAME}',
        '    When each file was last made (kept here so that the same records give the same report bytes).',
        '']) + '\n'
