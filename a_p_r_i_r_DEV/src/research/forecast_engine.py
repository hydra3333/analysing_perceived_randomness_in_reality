"""The forecast of one variant for one target draw: the content of its TARGET line.

What this file is for
    For one variant and one target T it builds the permitted view (the draws before T), gives the method that
    view and a frozen task, reads the forecast out of the method's scores, lets the method check the result by
    its own second calculation, and returns the content of the list line: a FORECAST (scores, ranking, TOP and
    WORST for every barrel) or a NO_FORECAST with one typed reason. It writes nothing and reads nothing but the
    results bytes it is handed. Nothing in the content depends on any draw at or after T, or on the results
    file as a whole.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 5.3 (FORECAST, NO_FORECAST and what is never
    recorded), 5.4 (the content and its digest) and 6 (earlier draws only).

Which of the project's own modules it uses
    research.reader             permitted_view: the draws before the target
    research.readout            read_out, method_facing_record: ranking, ties, TOP, WORST
    research.method_api         MethodFailed: the method's own declared failure
    research.variant_folders    Variant: the variant's identity, declaration and fingerprint
    _common.contract_task       MethodTask: the frozen task a method is given; permitted_view_digest
    _common.contract_records    record_digest: SHA-256 of a record's canonical bytes
    _common.game_profiles       get_profile: the game's profile version and era

What uses it
    research/research_job.py (the fill and the catch-up), and the engine's tests.
"""
from __future__ import annotations

from _common.contract_records import record_digest
from _common.contract_task import MethodTask, permitted_view_digest
from _common.game_profiles import get_profile
from research.method_api import MethodFailed
from research.reader import ResultsOnFile, permitted_view
from research.readout import ReadoutRefused, method_facing_record, read_out
from research.variant_folders import Variant

# The two things a TARGET line can be, and the two typed reasons for NO_FORECAST (specification 5.3).
FORECAST = 'FORECAST'
NO_FORECAST = 'NO_FORECAST'
INSUFFICIENT_HISTORY = 'INSUFFICIENT_HISTORY'
METHOD_FAILED = 'METHOD_FAILED'
# The frozen task a method receives was defined by the old system with eleven fields. Three of them are retired
# in this system: every task carries the same fixed value for each, and none of them enters a record.
#   RETIRED_RUN_MODE must be a real-data mode, because E_1's own code turns it into the view's data kind
#   ("REAL_HISTORICAL_DEVELOPMENT"), which is part of the view digest and so of every tie order.
RETIRED_RUN_MODE = 'REAL_DEVELOPMENT'
RETIRED_FIELD_VALUE = 'NOT_USED'
# Every existing variant is deterministic: no seed exists. A stochastic variant would have its seed fixed by its
# identity and the target (specification 6) and recorded here.
NO_SEED = None


def make_task(variant: Variant, game_id: str, target: int) -> MethodTask:
    """Build the frozen task a method is given for one target.

    variant: the Variant.  game_id: the game.  target: the draw to forecast.
    Returns the MethodTask, for example MethodTask(game_id='POWERBALL', method_id='E_2',
    variant_id='RECUR_MEAN_ALL_V1', target_draw_number=1592, observation_view='UNORDERED_SET', ...).
    """
    profile = get_profile(game_id)
    return MethodTask(game_id=game_id, profile_version=profile.version, era_id=profile.era_id,
                      method_id=variant.method_id, variant_id=variant.variant,
                      method_revision=RETIRED_FIELD_VALUE, target_draw_number=target,
                      observation_view=variant.declaration['observation_view'], include_dates=False,
                      run_mode=RETIRED_RUN_MODE, product_kind=RETIRED_FIELD_VALUE)


def content_digest(content: dict) -> str:
    """The digest of a TARGET line's content: the SHA-256 of its canonical bytes, 64 hexadecimal characters."""
    return record_digest(content)


def view_digest_for(variant: Variant, results: ResultsOnFile, target: int) -> str:
    """The digest of the permitted view a variant is given for a target: the draws before it, and nothing else.

    The job compares it with the digest a stored TARGET line holds, to find results that changed other than by
    growing. Returns 64 hexadecimal characters.
    """
    task = make_task(variant, results.game_id, target)
    view = permitted_view(results, method_id=variant.method_id, variant_id=variant.variant, target=target,
                          observation_view=task.observation_view, include_dates=False)
    return permitted_view_digest(view, task.run_mode)


def compute_target(variant: Variant, method, results: ResultsOnFile, target: int) -> tuple:
    """Compute one variant's TARGET-line content for one target, from the draws before it only.

    variant: the Variant.  method: its imported method.py (variant_folders.load_method).
    results: the game's results on file; only the rows before `target` are read.  target: the draw to forecast.
    Returns (content, detail). content is the line's content, for example
        {'game': 'POWERBALL', 'family': 'E_002', 'variant': 'RECUR_MEAN_ALL_V1', 'target': 1592,
         'permitted_view_digest': '9c1f...', 'configuration': {'variant_fingerprint': 'ab12...'}, 'seed': None,
         'status': 'FORECAST',
         'barrels': {'MAIN': {'label_low': 1, 'label_high': 35, 'selected_count': 7, 'scores': [...],
                              'ranking': [...], 'top': [...], 'worst': [...]}, 'POWERBALL': {...}}}
    or the same identity with 'status': 'NO_FORECAST' and 'reason': 'INSUFFICIENT_HISTORY' or 'METHOD_FAILED'.
    detail is None, or for METHOD_FAILED the text of what failed (kept in the line's envelope, for the reader).
    What becomes METHOD_FAILED, and nothing else: compute() raising MethodFailed; the readout refusing the
    output; verify() raising ValueError. Every other exception is passed on unchanged: the caller writes no line
    and stops the game (an environmental fault is never recorded as a method failure).
    """
    game_id = results.game_id
    task = make_task(variant, game_id, target)
    view = permitted_view(results, method_id=variant.method_id, variant_id=variant.variant, target=target,
                          observation_view=task.observation_view, include_dates=False)
    view_digest = permitted_view_digest(view, task.run_mode)
    content = {'game': game_id, 'family': variant.family, 'variant': variant.variant, 'target': target,
               'permitted_view_digest': view_digest,
               'configuration': {'variant_fingerprint': variant.fingerprint}, 'seed': NO_SEED}

    def failed(detail: str) -> tuple:
        """The NO_FORECAST content for a method failure, with its detail."""
        return dict(content, status=NO_FORECAST, reason=METHOD_FAILED), detail

    try:
        output = method.compute(task, view)
    except MethodFailed as failure:
        return failed(f'compute() declared a failure: {failure}')
    try:
        records = read_out(game_id, output, view_digest=view_digest, target=target,
                           method_id=variant.method_id, variant_id=variant.variant)
    except ReadoutRefused as refusal:
        return failed(f'the readout refused the output: {refusal}')
    try:
        method.verify(task, view, method_facing_record(records), None)
    except ValueError as mismatch:
        return failed(f'verify() refused the result: {mismatch}')
    if records is None:
        return dict(content, status=NO_FORECAST, reason=INSUFFICIENT_HISTORY), None
    barrels = {barrel_id: {key: record[key] for key in ('label_low', 'label_high', 'selected_count', 'scores',
                                                        'ranking', 'top', 'worst')}
               for barrel_id, record in records.items()}
    return dict(content, status=FORECAST, barrels=barrels), None
