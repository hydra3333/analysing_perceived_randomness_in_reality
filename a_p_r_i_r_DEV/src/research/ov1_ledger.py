"""OV-1: one draw's line, and the two series of a game, both from the one passed kernel.

What this file is for
    OV-1 is the one overall evidence score of a game. For each counted draw, every counted method adds +1 to
    each number of its TOP seven and -1 to each number of its WORST seven of the main barrel; X is the sum of
    those weights over the seven numbers drawn; the kernel turns X into six exact log-factors (one for each
    lambda), each a proved lower bound, and the running sums give the score, whose reference bar is 40. This
    file works out one draw's line from the lists, and never chooses a number itself: the arithmetic is the
    kernel's (research/ov1_numeric.py, unchanged).

    Two series, one calculation, one of each per game. The exploratory series counts every method at every draw
    it has a scored pair. The second series (called "prevailing" in the files and reports) counts each method
    only from the draw after its establishment draw (IN_PLACE_SINCE) up to, and not including, its retirement
    draw. Both are made again by every job, both are exploratory indicators, and neither claims that any result
    was unseen when a method was written.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 5 step 6;
    doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md sections 6.1, 6.3 and 6.5 (the mathematics).

Which of the project's own modules it uses
    research.ov1_numeric    the kernel: factor_table, mixture_lower, crossing, z_text, fixed_text
    research.game_state     MAIN_BARREL; the VariantStates it is given hold each method's summarised lines
    research.variant_lists  the two series are written as plain lists
    _common.game_profiles   get_profile: the size of the main barrel

What uses it
    research/research_job.py (the line on the prevailing series in its ending), reporting/printouts.py (prints
    both series), and the tests.
"""
from __future__ import annotations

from pathlib import Path

from _common.game_profiles import get_profile
from research import ov1_numeric as kernel
from research import variant_lists as lists
from research.game_state import MAIN_BARREL

# The two series of a game, under the tree's research folder.
PREVAILING_LEDGER = 'ov1/prevailing.jsonl'
EXPLORATORY_LEDGER = 'ov1/exploratory.jsonl'
# The two states of a cohort member in a line.
COUNTED = 'counted'
NO_PAIR = 'no_pair'
# What the line on the prevailing series says before any method has an establishment draw.
NOT_STARTED_TEXT = 'prevailing OV-1: not started; no method has an establishment draw yet'


class Blocked(Exception):
    """A line of the second series cannot be made: a method that counts at the draw has no line for it, or a
    forecast for it that is not scored (its calculation failed in this job). The series stops at that draw."""


def ledger_path(tree_root: Path, game_id: str, which: str = PREVAILING_LEDGER) -> Path:
    """Where a series is kept, for example <tree>/results/research/POWERBALL/ov1/prevailing.jsonl."""
    return Path(tree_root) / lists.RESEARCH_FOLDER / game_id / which


def series_header(game_id: str, kind: str) -> dict:
    """The header line of a series file: the game, the kernel's version, the bar and the lambdas."""
    return {'line': lists.HEADER_LINE, 'format': lists.LIST_FORMAT, 'list': kind, 'game': game_id,
            'kernel_version': kernel.KERNEL_VERSION, 'bar': kernel.BAR,
            'lambdas': [f'{numerator}/{denominator}' for numerator, denominator in kernel.LAMBDAS]}


def write_series(tree_root: Path, game_id: str, prevailing: list, exploratory: list) -> int:
    """Write both series of a game as plain lists, each afresh. Returns how many of the two files changed."""
    written = 0
    for which, kind, line_name, series in (
            (PREVAILING_LEDGER, lists.PREVAILING_KIND, lists.PREVAILING_LINE, prevailing),
            (EXPLORATORY_LEDGER, lists.EXPLORATORY_KIND, lists.EXPLORATORY_LINE, exploratory)):
        lines = [{'line': line_name, 'content': made['content'], 'audit': made['audit']} for made in series]
        written += lists.write_whole(ledger_path(tree_root, game_id, which), series_header(game_id, kind), lines)
    return written


def prevailing_start(states) -> int | None:
    """The draw the second series starts at: the smallest first-counted draw among the methods (the draw after
    an establishment draw), or None while no method has one. For example 1607."""
    eligible = [state.status.eligible_from for state in states if state.status.eligible_from is not None]
    return min(eligible) if eligible else None


def prevailing_cohort(states, draw: int) -> list:
    """Who counts in the second series at a draw: every method in place before it and not retired from a draw
    at or below it; in identity order."""
    return sorted((state for state in states if state.status.in_prevailing_cohort_at(draw)),
                  key=lambda state: state.variant.identity)


def exploratory_cohort(states, draw: int) -> list:
    """The exploratory cohort of a draw: every variant that is not held and has a scored pair or a NO_FORECAST
    line at the draw, in identity order (specification 10.5: every variant wherever it has one)."""
    return sorted((state for state in states if not state.held and draw in state.targets
                   and (draw in state.score_contents or state.targets[draw].status == 'NO_FORECAST')),
                  key=lambda state: state.variant.identity)


def draw_line(game_id: str, draw: int, cohort, drawn_main, running_logs) -> dict:
    """Work out one draw's OV-1 line for a cohort.

    game_id: the game.  draw: the draw.  cohort: the VariantStates that count at it.
    drawn_main: the seven main numbers drawn.  running_logs: the six running sums before this draw, as whole
    numbers in the kernel's fixed point (all 0 before the first line).
    Returns {'content': ..., 'audit': ...}. The content is the scientific part that the full check compares:
        {'draw': 1607, 'cohort': [{'variant': 'E_002/RECUR_MEAN_ALL_V1', 'state': 'counted'},
                                  {'variant': 'E_901/X_V1', 'state': 'no_pair', 'reason': 'METHOD_FAILED'}],
         'weights': [1, 0, -2, ...] (one for each number of the main barrel), 'variance': [28, 5] (a fraction;
         [0, 1] when V is zero), 'x': -3, 'z': '-0.716114874039' (None when the factor is exactly 1),
         'factor_is_one': False, 'log_factors': ['...', ...] and 'running_logs': ['...', ...] (six whole numbers
         each, as text), 'score_lower_bound': '0.998765432109', 'crossed': False}
    The audit counts, from the forecasts' envelopes: how many counted forecasts were made with the result not yet
    on file and how many after, and where they were computed, for example
        {'counted_before_result': 40, 'counted_after_result': 0, 'computed_in': {'PROD': 40}}.
    Raises Blocked, naming the variant, if a cohort member is held, has no TARGET line for the draw, or holds a
    FORECAST for it that is not scored. Raises ValueError if X from the weights and X from the score lines
    disagree, and the kernel's Refuse if no bound can be established.
    """
    barrel = next(b for b in get_profile(game_id).barrels if b.barrel_id == MAIN_BARREL)
    weights = [0] * (barrel.high - barrel.low + 1)
    members, x_from_scores = [], 0
    audit = {'counted_before_result': 0, 'counted_after_result': 0, 'computed_in': {}}
    for state in cohort:
        identity = state.variant.identity
        if state.held:
            raise Blocked(f'draw {draw}: {identity} is held (a foreign list stands in its place)')
        facts = state.targets.get(draw)
        if facts is None:
            raise Blocked(f'draw {draw}: {identity} has no line for it yet')
        if facts.status != 'FORECAST':
            members.append({'variant': identity, 'state': NO_PAIR, 'reason': facts.reason})
            continue
        score = state.score_contents.get(draw)
        if score is None:
            raise Blocked(f'draw {draw}: the forecast of {identity} is not scored yet')
        members.append({'variant': identity, 'state': COUNTED})
        for number in facts.sets[MAIN_BARREL]['top']:
            weights[number - barrel.low] += 1
        for number in facts.sets[MAIN_BARREL]['worst']:
            weights[number - barrel.low] -= 1
        x_from_scores += score['matches'][MAIN_BARREL]['top'] - score['matches'][MAIN_BARREL]['worst']
        audit['counted_after_result' if facts.result_on_file else 'counted_before_result'] += 1
        audit['computed_in'][facts.role] = audit['computed_in'].get(facts.role, 0) + 1
    x = sum(weights[number - barrel.low] for number in drawn_main)
    if x != x_from_scores:
        raise ValueError(f'{game_id} draw {draw}: X is {x} from the weights and {x_from_scores} from the score '
                         f'lines. The lists disagree with themselves; nothing is written.')
    table = kernel.factor_table(weights)
    if table is None:
        variance, log_factors, z_text = [0, 1], [0] * len(kernel.LAMBDAS), None
    else:
        variance = list(table['variance'])
        log_factors = [row[x] for row in table['rows']]
        z_text = kernel.z_text(x, *table['variance'])
    running = [before + factor for before, factor in zip(running_logs, log_factors)]
    content = {'draw': draw, 'cohort': members, 'weights': weights, 'variance': variance, 'x': x, 'z': z_text,
               'factor_is_one': table is None, 'log_factors': [str(value) for value in log_factors],
               'running_logs': [str(value) for value in running],
               'score_lower_bound': kernel.fixed_text(kernel.mixture_lower(running)),
               'crossed': kernel.crossing(running)}
    return {'content': content, 'audit': audit}


def running_logs_of(content: dict | None) -> list:
    """The six running sums a line's content holds, as whole numbers; all 0 for None (before the first line)."""
    if content is None:
        return [0] * len(kernel.LAMBDAS)
    return [int(value) for value in content['running_logs']]


def exploratory_series(game_id: str, states, outcomes: dict, through: int) -> list:
    """The exploratory score, draw by draw: the same calculation over every draw that has any scored pair.

    states: the game's VariantStates.  outcomes: {draw: the seven main numbers drawn}.  through: the last draw
    to include.
    Returns the list of draw_line results, in draw order, for every draw up to `through` at which at least one
    variant that is not held has a scored forecast. It is a print-out: nothing is stored, and no error bound
    applies to it.
    """
    series, running = [], [0] * len(kernel.LAMBDAS)
    scored_draws = sorted({draw for state in states if not state.held for draw in state.score_contents
                           if draw <= through})
    for draw in scored_draws:
        line = draw_line(game_id, draw, exploratory_cohort(states, draw), outcomes[draw], running)
        running = running_logs_of(line['content'])
        series.append(line)
    return series


def prevailing_series(game_id: str, states, outcome_of, through: int) -> tuple:
    """The second series, draw by draw: each method counting from the draw after its establishment draw up to,
    and not including, its retirement draw.

    states: the game's VariantStates.  outcome_of: gives the seven main numbers drawn at a draw.
    through: the last draw to include.
    Returns (series, blocked): the list of draw_line results for each draw from the series' start, in order;
    and None, or the one line saying at which draw it had to stop and why (see Blocked).
    """
    start = prevailing_start(states)
    series, running = [], [0] * len(kernel.LAMBDAS)
    if start is None:
        return series, None
    for draw in range(start, through + 1):
        try:
            cohort = [state for state in prevailing_cohort(states, draw) if state.first_target <= draw]
            line = draw_line(game_id, draw, cohort, outcome_of(draw), running)
        except Blocked as blocked:
            return series, str(blocked)
        running = running_logs_of(line['content'])
        series.append(line)
    return series, None


def prevailing_status_line(records) -> str:
    """One line saying where the prevailing OV-1 stands, for example 'prevailing OV-1: lines for draws 1592 to
    1600; score (numerical lower bound) 0; reference line 40: not reached'. records: the game's GameRecords (its
    states, its second series' lines and why that series stopped, if it did). The research job ends with this
    line and the prevailing print-out shows it, so it lives here, beside the series it describes."""
    eligible = [s.status.eligible_from for s in records.states if s.status.eligible_from is not None]
    if not eligible:
        return NOT_STARTED_TEXT
    if not records.ledger_lines:
        text = f'prevailing OV-1: starts at draw {min(eligible)}; no line yet'
    else:
        last = records.ledger_lines[-1]['content']
        text = (f'prevailing OV-1: lines for draws {records.ledger_lines[0]["content"]["draw"]} to {last["draw"]}; '
                f'score (numerical lower bound) {last["score_lower_bound"]}; reference line {kernel.BAR}: '
                + ('reached' if any(line['content']['crossed'] for line in records.ledger_lines) else 'not reached'))
    return text + (f'; BLOCKED: {records.blocked}' if records.blocked else '')
