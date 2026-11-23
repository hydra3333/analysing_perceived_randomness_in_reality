"""Scoring: the one function that scores a forecast against its draw, and the reading of a draw's result.

What this file is for
    When a target's result is on file, each FORECAST for it is scored once: for each barrel, how many of the
    numbers drawn are in the TOP set and how many in the WORST set; and the prize division the TOP ticket and
    the WORST ticket would each have won. This file reads one draw's result from the results on file and makes
    the content of the score line. It is the only place in the engine that reads the numbers of a target draw,
    and nothing here is imported by the forecasting code.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 8 (scoring) and 5.5 (the score line);
    R3 v0.5 section 3 (TOP and WORST matches) and 17.4 (prize divisions), through evaluation/divisions.py.
    Oz Lotto's supplementary numbers are used for the prize division only and are not stored (R2 2.5).

Which of the project's own modules it uses
    research.reader          ResultsOnFile, header_for: the results on file and the file's columns
    evaluation.divisions     match_record: main matches, Powerball or supplementary match, prize division
    _common.game_profiles    get_profile: the game's barrels

What uses it
    research/research_job.py (the fill and the catch-up), research/derived_check.py (the full check), and the
    engine's tests.
"""
from __future__ import annotations

import csv

from _common.game_profiles import get_profile
from evaluation.divisions import match_record
from research.reader import ResultsOnFile, ResultsRefused, header_for

# The two sets of a forecast that are scored, as the score line names them.
SCORED_SETS = ('top', 'worst')


def read_outcome(results: ResultsOnFile, draw: int) -> dict:
    """Read one draw's result from the results on file.

    results: the game's results on file.  draw: a draw on file.
    Returns {'MAIN': the seven main numbers in rising order, and 'POWERBALL': [the Powerball] for Powerball, or
    'SUPPLEMENTARY': the three supplementary numbers for Oz Lotto}, for example (invented)
        {'MAIN': [3, 9, 14, 20, 27, 31, 35], 'POWERBALL': [7]}.
    Refuses (ResultsRefused) a draw that is not on file or a row that is not that draw's well-formed result.
    """
    if type(draw) is not int or not results.first_draw <= draw <= results.last_draw:
        raise ResultsRefused(f'{results.game_id} draw {draw}: its result is not on file (draws '
                             f'{results.first_draw} to {results.last_draw} are).')
    line = results.raw.split(b'\n')[draw - results.first_draw + 1].rstrip(b'\r')
    columns = header_for(results.game_id)
    try:
        row = next(csv.reader([line.decode('ascii')], strict=True))
        if len(row) != len(columns) or int(row[0]) != draw:
            raise ValueError('wrong number of fields or wrong draw number')
        if any(not field.isdecimal() or field.startswith('0') for field in row[2:]):
            raise ValueError('a number is not a plain whole number')
        numbers = [int(field) for field in row[2:]]
    except (ValueError, UnicodeDecodeError, StopIteration, csv.Error) as error:
        raise ResultsRefused(f'{results.game_id} draw {draw}: its row in the results file is malformed ({error}). '
                             f'Restore the results file from a backup.') from None
    outcome = {'MAIN': sorted(numbers[:7])}
    outcome['POWERBALL' if results.game_id == 'POWERBALL' else 'SUPPLEMENTARY'] = \
        numbers[7:] if results.game_id == 'POWERBALL' else sorted(numbers[7:])
    return outcome


def score_content(forecast_content: dict, forecast_content_digest: str, outcome: dict) -> dict:
    """The scientific content of one score line.

    forecast_content: the content of a FORECAST line.  forecast_content_digest: its digest.
    outcome: read_outcome's result for the forecast's target.
    Returns {'target', 'forecast_content_digest', 'drawn' (the numbers drawn in each scored barrel), 'matches'
    ({barrel: {'top': n, 'worst': n}}), 'divisions' ({'top': d, 'worst': d}; 0 is no prize) and, for Oz Lotto,
    'supplementary_matches' ({'top': s, 'worst': s})}, for example (invented)
        {'target': 1592, 'forecast_content_digest': 'ab12...', 'drawn': {'MAIN': [3, 9, ...], 'POWERBALL': [7]},
         'matches': {'MAIN': {'top': 2, 'worst': 1}, 'POWERBALL': {'top': 0, 'worst': 0}},
         'divisions': {'top': 0, 'worst': 0}}.
    Refuses (ValueError) content that is not a FORECAST: a NO_FORECAST line is never scored. A malformed outcome
    or set raises the divisions module's own ValueError.
    """
    if forecast_content.get('status') != 'FORECAST':
        raise ValueError(f'draw {forecast_content.get("target")}: only a FORECAST is scored; this line is '
                         f'{forecast_content.get("status")}.')
    game_id = forecast_content['game']
    barrels = {b.barrel_id for b in get_profile(game_id).barrels}
    drawn = {barrel_id: list(outcome[barrel_id]) for barrel_id in sorted(barrels)}
    matches = {barrel_id: {which: len(set(forecast_content['barrels'][barrel_id][which]) & set(drawn[barrel_id]))
                           for which in SCORED_SETS} for barrel_id in sorted(barrels)}
    content = {'target': forecast_content['target'], 'forecast_content_digest': forecast_content_digest,
               'drawn': drawn, 'matches': matches, 'divisions': {}}
    for which in SCORED_SETS:
        ticket_main = forecast_content['barrels']['MAIN'][which]
        if game_id == 'POWERBALL':
            record = match_record(game_id, ticket_main, forecast_content['barrels']['POWERBALL'][which][0],
                                  outcome['MAIN'], outcome['POWERBALL'][0])
        else:
            record = match_record(game_id, ticket_main, None, outcome['MAIN'], outcome['SUPPLEMENTARY'])
            content.setdefault('supplementary_matches', {})[which] = record['supplementary_matches']
        if record['main_matches'] != matches['MAIN'][which]:
            raise ValueError(f'draw {content["target"]}: the two counts of {which} main matches disagree.')
        content['divisions'][which] = record['division']
    return content
