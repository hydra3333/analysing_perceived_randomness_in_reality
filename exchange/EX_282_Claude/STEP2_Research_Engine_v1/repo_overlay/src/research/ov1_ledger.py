"""OV-1: the prevailing ledger's lines and the exploratory score, both from the one passed kernel.

What this file is for
    OV-1 is the one overall evidence score of a game. For each counted draw, every counted variant adds +1 to
    each number of its TOP seven and -1 to each number of its WORST seven of the main barrel; X is the sum of
    those weights over the seven numbers drawn; the kernel turns X into six exact log-factors (one for each
    lambda), each a proved lower bound, and the running sums give the score, whose bar is 40. This file works
    out one draw's line from the lists and the status files, and never chooses a number itself: the arithmetic
    is the kernel's (research/ov1_numeric.py, copied unchanged from the passed MHUP-B slice 2).

    Two uses, one calculation. The prevailing score counts, at each draw, the cohort fixed by draw number in the
    status files (eligible at or below the draw, not withdrawn at or below it), and its lines are stored in a
    ledger. The exploratory score counts every variant wherever it has a scored pair; it is only a print-out.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 10.1 to 10.5;
    doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md sections 6.1, 6.3 and 6.5 (the mathematics).

Which of the project's own modules it uses
    research.ov1_numeric    the kernel: factor_table, mixture_lower, crossing, z_text, fixed_text
    research.game_state     MAIN_BARREL; the VariantStates it is given hold each variant's summarised lines
    research.variant_lists  the ledger file is a list of the same chained form
    _common.game_profiles   get_profile: the size of the main barrel

What uses it
    research/research_job.py (writes prevailing lines), research/derived_check.py (rebuilds and compares),
    research/reports.py (prints both scores), and the engine's tests.
"""
from __future__ import annotations

from pathlib import Path

from _common.game_profiles import get_profile
from research import ov1_numeric as kernel
from research import variant_lists as lists
from research.game_state import MAIN_BARREL

# The prevailing ledger of a game, under the tree's research folder (specification 10.4).
PREVAILING_LEDGER = 'ov1/prevailing.jsonl'
# The two states of a cohort member in a line.
COUNTED = 'counted'
NO_PAIR = 'no_pair'


class Blocked(Exception):
    """A prevailing line cannot be written yet: a cohort member is not complete for the draw, or is held. An
    operational wait, named with the variant that causes it; never a skip (specification 10.4)."""


def ledger_path(tree_root: Path, game_id: str) -> Path:
    """The prevailing ledger of a game, for example <tree>/results/research/POWERBALL/ov1/prevailing.jsonl."""
    return Path(tree_root) / lists.RESEARCH_FOLDER / game_id / PREVAILING_LEDGER


def ledger_header(game_id: str) -> dict:
    """The header line of a new prevailing ledger: the game, the kernel's version, the bar and the lambdas."""
    return {'line': lists.HEADER_LINE, 'format': lists.LIST_FORMAT, 'list': lists.PREVAILING_KIND, 'game': game_id,
            'kernel_version': kernel.KERNEL_VERSION, 'bar': kernel.BAR,
            'lambdas': [f'{numerator}/{denominator}' for numerator, denominator in kernel.LAMBDAS], 'prev': None}


def read_ledger(tree_root: Path, game_id: str) -> tuple:
    """Read a game's prevailing ledger and check it.

    Returns (None, []) if it is not begun; otherwise (the ListOnFile, its lines after the header).
    Refuses (ListFault): a broken chain (see variant_lists.read_list); a header for another game or another
    kernel version; lines whose draws do not run upward by one.
    """
    path = ledger_path(tree_root, game_id)
    listed = lists.read_list(path, lists.PREVAILING_KIND)
    if listed is None:
        return None, []
    if listed.header.get('game') != game_id or listed.header.get('kernel_version') != kernel.KERNEL_VERSION:
        raise lists.ListFault(f'{path} line 1: the header is not that of the {game_id} prevailing ledger under '
                              f'kernel {kernel.KERNEL_VERSION}.')
    lines = list(listed.lines)
    for number, line in enumerate(lines, start=2):
        draw = (line.get('content') or {}).get('draw')
        if type(draw) is not int or (number > 2 and draw != lines[number - 3]['content']['draw'] + 1):
            raise lists.ListFault(f'{path} line {number}: the draws of the prevailing ledger run upward by one; '
                                  f'this line does not follow the one before it.')
    listed.lines = []
    return listed, lines


def prevailing_start(states) -> int | None:
    """The draw the prevailing score starts at: the smallest eligibility draw among the installed variants, or
    None while no variant has one (specification 10.3). For example 1607."""
    eligible = [state.status.eligible_from for state in states if state.status.eligible_from is not None]
    return min(eligible) if eligible else None


def prevailing_cohort(states, draw: int) -> list:
    """The prevailing cohort as of a draw, read from the status files: every installed variant whose eligibility
    draw is at or below it and which is not withdrawn from a draw at or below it; in identity order."""
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
