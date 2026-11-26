"""A game's records in memory while the research job works it: the methods' lists, summarised.

What this file is for
    For one game the job holds, for every method in the tree, what its two lists say: which draws it has a
    line for, the TOP and WORST sets of each forecast, and each score. This file reads a method's lists into
    that form and says when they must be made again instead: when they cannot be read, do not follow on, or
    were made by other software than the method's files in the tree now.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 5 (steps 4 and 5).

Which of the project's own modules it uses
    research.variant_lists    the list files
    research.reader           first_target: a method's first draw in a game
    research.scoring          read_outcome: a draw's result
    research.method_flags     MethodStatus
    research.variant_folders  Variant

What uses it
    research/research_job.py, research/ov1_ledger.py, research/reports.py, and the tests.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from research import variant_lists as lists
from research.method_flags import MethodStatus
from research.reader import first_target
from research.scoring import read_outcome
from research.variant_folders import Variant

# The barrel OV-1 and the league's main figures are taken on, in both games.
MAIN_BARREL = 'MAIN'


@dataclass
class TargetFacts:
    """What the job keeps of one TARGET line.

    status: 'FORECAST' or 'NO_FORECAST'.  reason: the NO_FORECAST reason, or None.
    content_digest: the line's content digest.
    sets: for a FORECAST, {barrel: {'top': (...), 'worst': (...)}}; None otherwise.
    view_digest: the digest of the permitted view the line was computed from.
    result_on_file: whether the target's result was already on file when the line was computed (the envelope).
    rerun: the rerun's name if a historical walk-forward rerun wrote the line, else None.  role: the tree role
    that computed it, for example 'PROD'.
    """
    status: str
    reason: str | None
    content_digest: str
    sets: dict | None
    view_digest: str
    result_on_file: bool
    rerun: str | None
    role: str


@dataclass
class VariantState:
    """One installed variant's records for one game.

    variant: the Variant.  status: its MethodStatus, from the small files in its folder.
    first_target: the first draw it can forecast in this game.
    forecasts, scores: its two lists as read (their lines are dropped once summarised), or None if not begun.
    targets: {target: TargetFacts}.  score_contents: {target: the score line's content}.
    held, foreign_reason: always False and None (the reports still ask; nothing is held in this scheme).
    failed: None, or why the method stopped in this job (a fault in its calculation); it is then passed over.
    """
    variant: Variant
    status: MethodStatus
    first_target: int
    forecasts: lists.ListOnFile | None = None
    scores: lists.ListOnFile | None = None
    targets: dict = field(default_factory=dict)
    score_contents: dict = field(default_factory=dict)
    held: bool = False
    foreign_reason: str | None = None
    failed: str | None = None

    @property
    def next_target(self) -> int:
        """The first draw with no TARGET line, for example 1593 when lines run to 1592."""
        return self.first_target + len(self.targets)

    def forecast_content(self, game_id: str, target: int) -> dict:
        """The part of a FORECAST's content that scoring needs, rebuilt from the summary, for example
        {'game': 'POWERBALL', 'target': 1592, 'status': 'FORECAST', 'barrels': {'MAIN': {'top': [...], ...}}}."""
        facts = self.targets[target]
        return {'game': game_id, 'target': target, 'status': facts.status,
                'barrels': {barrel: {which: list(numbers) for which, numbers in sets.items()}
                            for barrel, sets in (facts.sets or {}).items()}}


@dataclass
class GameRecords:
    """Everything the job holds for one game while it runs.

    game_id: the game.  tree_root, role: the tree and its role.  results: the results on file.
    states: the VariantStates of the methods in the tree, in identity order.
    foreign: the identities of methods that have results here but no software in this tree; they are left
    alone and count nowhere.
    ledger_lines: the second OV-1 series (each method counting from its establishment draw to its retirement
    draw), one {'content', 'audit'} a draw, made again by every job.
    blocked: None, or the one line saying at which draw that series had to stop, and why.
    cutoff: always None (the reports still ask; nothing is "not current" in this scheme).
    outcomes: {draw: read_outcome's result}, filled as draws are needed.
    """
    game_id: str
    tree_root: Path
    role: str
    results: object
    states: list
    foreign: list
    ledger_lines: list = field(default_factory=list)
    cutoff: tuple | None = None
    outcomes: dict = field(default_factory=dict)
    blocked: str | None = None

    @property
    def ledger_contents(self) -> list:
        """The scientific content of each line of the second OV-1 series, in draw order."""
        return [line['content'] for line in self.ledger_lines]

    @property
    def workable(self) -> list:
        """The methods the job computes for and the reports show: all of them."""
        return list(self.states)

    def outcome_of(self, draw: int) -> dict:
        """The result of a draw on file, read once and kept (see scoring.read_outcome)."""
        if draw not in self.outcomes:
            self.outcomes[draw] = read_outcome(self.results, draw)
        return self.outcomes[draw]


def summarise_target_line(line: dict) -> TargetFacts:
    """The summary of one TARGET line (see TargetFacts)."""
    content, envelope = line['content'], line.get('envelope', {})
    sets = None
    if content['status'] == 'FORECAST':
        sets = {barrel: {'top': tuple(record['top']), 'worst': tuple(record['worst'])}
                for barrel, record in content['barrels'].items()}
    return TargetFacts(status=content['status'], reason=content.get('reason'), content_digest=line['content_digest'],
                       sets=sets, view_digest=content.get('permitted_view_digest', ''),
                       result_on_file=bool(envelope.get('target_result_on_file')),
                       rerun=envelope.get('rerun'), role=(envelope.get('computed_in') or {}).get('role', '?'))


def _forget_lines(state: VariantState) -> None:
    """Drop the lists' lines from memory once they are summarised (the files are untouched): a forecast line
    holds every number's score, and nothing after the summary needs them."""
    for listed in (state.forecasts, state.scores):
        if listed is not None:
            listed.lines = []


def load_variant_state(tree_root: Path, game_id: str, variant: Variant, status: MethodStatus) -> tuple:
    """Read one method's two lists for a game, and say whether they must be made again.

    tree_root: the tree.  game_id: the game.  variant: the Variant.  status: its status in the game.
    Returns (state, stale): the VariantState, and None or the reason its stored results must be made again. With
    a reason the state is empty (nothing was summarised) and the caller deletes the method's results. The
    reasons: a list was made by other software than the method's files in the tree now (its header names another
    fingerprint); a list cannot be read or does not follow on; a score list without its forecast list; a header
    that names another game or method than its folder, or another first target than the declaration gives.
    """
    state = VariantState(variant=variant, status=status,
                         first_target=first_target(game_id, variant.minimum_earlier_draws(game_id)))
    forecasts_path, scores_path = lists.variant_list_paths(tree_root, game_id, variant.family, variant.variant)
    try:
        forecasts = lists.read_list(forecasts_path, lists.FORECASTS_KIND)
        scores = lists.read_list(scores_path, lists.SCORES_KIND)
        if forecasts is None:
            return state, ('a score list without its forecast list' if scores is not None else None)
        for listed in (forecasts, scores):
            if listed is None:
                continue
            if (listed.header.get('game'), listed.header.get('family'),
                    listed.header.get('variant')) != (game_id, variant.family, variant.variant):
                return state, f'{listed.path.name} names another game or method than the folder it lies in'
            if listed.header.get('variant_fingerprint') != variant.fingerprint:
                return state, 'its stored results were made by other files than the method has now'
        summary = lists.check_lists(forecasts, scores)
    except lists.ListFault as fault:
        return state, f'a list cannot be used ({fault})'
    if summary['first_target'] != state.first_target:
        return state, (f'its list begins at draw {summary["first_target"]} but its declaration now gives '
                       f'{state.first_target}')
    state.forecasts, state.scores = forecasts, scores
    for line in forecasts.lines:
        state.targets[line['content']['target']] = summarise_target_line(line)
    for line in (scores.lines if scores is not None else []):
        state.score_contents[line['content']['target']] = line['content']
    _forget_lines(state)
    return state, None


def lists_of_variants_not_installed(tree_root: Path, game_id: str, installed) -> list:
    """The methods that have results on disk for a game but no software in this tree. They are left alone.

    installed: the identities of the methods in the tree, for example {'E_002/RECUR_MEAN_ALL_V1', ...}.
    Returns their identities in order, for example ['E_002/RECUR_OLD_V1'].
    """
    folder = Path(tree_root) / lists.RESEARCH_FOLDER / game_id / 'variants'
    found = []
    if folder.is_dir():
        for family in sorted(p for p in folder.iterdir() if p.is_dir()):
            for variant in sorted(p for p in family.iterdir() if p.is_dir()):
                identity = f'{family.name}/{variant.name}'
                if identity not in installed and any(variant.iterdir()):
                    found.append(identity)
    return found
