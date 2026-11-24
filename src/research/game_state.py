"""One game's research records as the job holds them in memory: variants, lists, statuses, what is foreign.

What this file is for
    Before anything is computed, the job reads what the tree already holds for a game: each installed variant's
    status file and two lists, checked against their rules. It keeps a small summary of every line (the TOP and
    WORST sets, the score, where and when the forecast was made) and decides which lists belong to this tree's
    software and status and which are foreign. A foreign list is never appended to and counts nowhere; if its
    variant is installed here, the variant is held. Scoring, OV-1, the full check and the reports all read this
    one picture, so they cannot disagree about what the lists say.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 5.6 (invariant 5: the list agrees with the
    status file), 5.6A (foreign lists and held variants) and 5.7 (what to do next is read from the files).

Which of the project's own modules it uses
    research.variant_lists     read_list, check_lists, the list paths and kinds
    research.status_file       GameStatus
    research.variant_folders   Variant
    research.reader            first_target

What uses it
    research/research_job.py, research/ov1_ledger.py, research/derived_check.py, research/reports.py,
    research/withdraw.py, and the engine's tests.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from research import variant_lists as lists
from research.reader import first_target
from research.status_file import GameStatus
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

    variant: the Variant.  status: its GameStatus from the status file.
    first_target: the first draw it can forecast in this game.
    forecasts, scores: its two lists as read (their lines are dropped once summarised), or None if not begun.
    targets: {target: TargetFacts}.  score_contents: {target: the score line's content}.
    held: True if a foreign list stands in its place; foreign_reason says why.
    """
    variant: Variant
    status: GameStatus
    first_target: int
    forecasts: lists.ListOnFile | None = None
    scores: lists.ListOnFile | None = None
    targets: dict = field(default_factory=dict)
    score_contents: dict = field(default_factory=dict)
    held: bool = False
    foreign_reason: str | None = None

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

    game_id: the game.  tree_root, role: the tree and its role.  results: the results on file (replaced when the
    results step brings more).  states: the installed variants' VariantStates, in identity order.
    foreign: the identities of variants that have lists here but are not installed.
    ledger: the prevailing ledger as read, or None if not begun.  ledger_lines: its lines after the header, in
    draw order (each {'line', 'content', 'audit', 'envelope', 'prev'}).
    blocked: None, or the one line saying which variant makes the next prevailing line wait.
    cutoff: None, or (draw, reason, detail) from NOT_CURRENT_FROM.json.
    outcomes: {draw: read_outcome's result}, filled as draws are needed.
    forecasting_code_identity, derived_code_digest, environment_digest: the identities quoted in lines.
    """
    game_id: str
    tree_root: Path
    role: str
    results: object
    states: list
    foreign: list
    forecasting_code_identity: str
    derived_code_digest: str
    environment_digest: str
    ledger: lists.ListOnFile | None = None
    ledger_lines: list = field(default_factory=list)
    cutoff: tuple | None = None
    outcomes: dict = field(default_factory=dict)
    blocked: str | None = None

    @property
    def ledger_contents(self) -> list:
        """The scientific content of each prevailing line, in draw order."""
        return [line['content'] for line in self.ledger_lines]

    @property
    def workable(self) -> list:
        """The variants that are not held: those the job computes for and the reports show."""
        return [state for state in self.states if not state.held]

    def withheld(self, draw: int) -> bool:
        """True if no score, prevailing line or report may be written at this draw: the game's derived results
        are not current from a draw at or below it because of a mismatch (specification 5.8)."""
        return self.cutoff is not None and self.cutoff[1] == 'MISMATCH' and draw >= self.cutoff[0]


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


def load_variant_state(tree_root: Path, game_id: str, variant: Variant, status: GameStatus,
                       forecasting_code_identity: str) -> VariantState:
    """Read one installed variant's two lists for a game, check them, and decide whether they belong.

    tree_root: the tree.  game_id: the game.  variant: the installed Variant.  status: its status in the game.
    forecasting_code_identity: the identity of the forecasting code installed in this tree.
    Returns the VariantState. Its lists are foreign, and the variant held, when (5.6A): the forecast list's
    header names another fingerprint than the installed variant's, or another forecasting-code identity than the
    installed code's, or the lists break invariant 5 against the status file (a TARGET line beyond the withdrawal
    draw, or a score at or beyond it). A foreign list is not read further.
    Refuses (ListFault): a list that belongs but breaks invariants 1 to 4; a header that names another game or
    variant than its folder; a score list without its forecast list.
    """
    state = VariantState(variant=variant, status=status,
                         first_target=first_target(game_id, variant.minimum_earlier_draws(game_id)))
    forecasts_path, scores_path = lists.variant_list_paths(tree_root, game_id, variant.family, variant.variant)
    forecasts = lists.read_list(forecasts_path, lists.FORECASTS_KIND)
    scores = lists.read_list(scores_path, lists.SCORES_KIND)
    if forecasts is None:
        if scores is not None:
            raise lists.ListFault(f'{scores_path}: a score list without its forecast list. Restore both from a '
                                  f'backup, or rerun the variant.')
        return state
    for listed in (forecasts, scores):
        if listed is not None and (listed.header.get('game'), listed.header.get('family'),
                                   listed.header.get('variant')) != (game_id, variant.family, variant.variant):
            raise lists.ListFault(f'{listed.path} line 1: the header names another game or variant than the folder '
                                  f'it lies in.')
    for listed in (forecasts, scores):
        if listed is None:
            continue
        if listed.header.get('variant_fingerprint') != variant.fingerprint:
            state.held, state.foreign_reason = True, 'it was made by other files than the variant installed here'
        elif listed.header.get('forecasting_code_identity') != forecasting_code_identity:
            state.held = True
            state.foreign_reason = 'it was made under other shared forecasting code than is installed here'
    state.forecasts, state.scores = forecasts, scores
    if state.held:
        # The foreign list's own first draw is where the stored reports first held this variant (5.6A, 5.8).
        if type(forecasts.header.get('first_target')) is int:
            state.first_target = forecasts.header['first_target']
        _forget_lines(state)
        return state
    summary = lists.check_lists(forecasts, scores)
    if summary['first_target'] != state.first_target:
        raise lists.ListFault(f'{forecasts_path} line 1: the first target is {summary["first_target"]} but the '
                              f'variant\'s declaration gives {state.first_target}.')
    withdrawn_from = status.withdrawn_from
    if withdrawn_from is not None and (summary['next_target'] > withdrawn_from + 1
                                       or any(target >= withdrawn_from for target in summary['scored'])):
        state.held = True
        state.foreign_reason = (f'it does not agree with the status file: the variant is withdrawn from draw '
                                f'{withdrawn_from}, but the list has a line beyond it or a score at or beyond it')
        _forget_lines(state)
        return state
    for line in forecasts.lines:
        state.targets[line['content']['target']] = summarise_target_line(line)
    for line in (scores.lines if scores is not None else []):
        state.score_contents[line['content']['target']] = line['content']
    _forget_lines(state)
    return state


def lists_of_variants_not_installed(tree_root: Path, game_id: str, installed) -> list:
    """The variants that have lists on disk for a game but are not installed in this tree (5.6A: foreign).

    installed: the identities of the installed variants, for example {'E_002/RECUR_MEAN_ALL_V1', ...}.
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
