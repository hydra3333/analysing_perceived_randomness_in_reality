"""The readout: from a method's scores to the ranking, the tie order, and the TOP and WORST sets.

What this file is for
    A method returns one score for every number of every barrel. This file checks that output and reads the
    forecast out of it: numbers with equal scores form a group; groups are ordered best first; inside a group the
    order is fixed by the ratified tie rule TIE_SHA256_V1; TOP is the first k of the ranking and WORST the last
    k, where k is how many numbers the barrel draws. Both sets come from the one frozen ranking.

    It calls the same functions the old system's assembly calls (score_groups, tie_identity_for and order_groups
    in _common/contract_records.py), so the ranking, the ties, TOP and WORST are the old system's by
    construction. The old record's revision, run-mode, product and receipt fields are not used.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 1.2 (the readout: E2R-1 v0.3r3 section 7,
    less its revision, run-mode and receipt fields) and 5.3 (what a FORECAST holds).
    doc/contracts/TIE_SHA256_V1_Ratified_Encoding_v0_2.md (the tie rule).

Which of the project's own modules it uses
    _common.contract_forecast   the types a method returns (MethodOutput, BarrelOutput, ScoredRanking,
                                ProbabilityVector)
    _common.contract_records    score_groups, tie_identity_for, order_groups: groups and the tie order;
                                check_json_value: every stored value is a plain, finite number
    _common.game_profiles       get_profile: each game's barrels

What uses it
    research/forecast_engine.py, and the engine's tests.
"""
from __future__ import annotations

from collections.abc import Mapping

from _common.contract_forecast import BarrelOutput, MethodOutput, ProbabilityVector, ScoredRanking
from _common.contract_records import check_json_value, order_groups, score_groups, tie_identity_for
from _common.game_profiles import get_profile

# The one tie rule (E2R-1 section 7; the ratified encoding v0.2). Every existing declaration names it.
TIE_READOUT_VERSION = 'TIE_SHA256_V1'
# What a method-facing record says about a barrel with no probability vector (the methods' verify() compares it).
NO_PROBABILITY = {'kind': 'NONE'}
# The two statuses of the record a method's verify() is given.
STATUS_AVAILABLE = 'PREDICTION_AVAILABLE'
STATUS_INSUFFICIENT = 'INSUFFICIENT_HISTORY'


class ReadoutRefused(ValueError):
    """A method's output is not a forecast. The message names the barrel and says what is wrong. The engine
    records NO_FORECAST with the reason METHOD_FAILED."""


def read_out(game_id: str, output: object, *, view_digest: str, target: int, method_id: str,
             variant_id: str) -> dict | None:
    """Check a method's output and read out the ranking, TOP and WORST for every barrel.

    game_id: the game.  output: what compute() returned.  view_digest: the digest of the permitted view.
    target: the draw being forecast.  method_id, variant_id: the identity the tie rule uses, for example 'E_2'
    and 'RECUR_MEAN_ALL_V1'.
    Returns None if the method returned its "not enough history" result (a MethodOutput with no barrel).
    Otherwise returns {barrel: record} for every barrel of the game, each record holding 'barrel_id',
    'label_low', 'label_high', 'selected_count', 'scores' (one for each number, lowest number first),
    'ranking' (every number, best first), 'top' and 'worst' (k numbers each) and 'probability', for example
        {'MAIN': {'barrel_id': 'MAIN', 'label_low': 1, 'label_high': 35, 'selected_count': 7,
                  'scores': [0.21, 0.18, ...], 'ranking': [1, 17, ...], 'top': [1, 17, ...],
                  'worst': [9, 30, ...], 'probability': {'kind': 'NONE'}}}.
    Refuses (ReadoutRefused): an output that is not a MethodOutput; a barrel missing or one the game does not
    have; a barrel without a score for every number; scores that are not all whole numbers or all floats, or not
    finite; a joint selection (not used in this system); a probability vector that is not one finite float for
    each number.
    """
    if not isinstance(output, MethodOutput) or not isinstance(output.barrels, Mapping):
        raise ReadoutRefused(f'{variant_id}: compute() must return a MethodOutput.')
    if len(output.barrels) == 0:
        return None
    profile = get_profile(game_id)
    barrels = {b.barrel_id: b for b in profile.barrels}
    if set(output.barrels) != set(barrels):
        raise ReadoutRefused(f'{variant_id}: the output has barrels {sorted(output.barrels)} but {game_id} has '
                             f'{sorted(barrels)}. A forecast covers every barrel of the game.')
    header = {'permitted_view_digest': view_digest, 'target_draw_number': target, 'method_id': method_id,
              'variant_id': variant_id}
    records = {}
    for barrel_id in sorted(barrels):
        barrel, out = barrels[barrel_id], output.barrels[barrel_id]
        labels = list(range(barrel.low, barrel.high + 1))
        if not isinstance(out, BarrelOutput) or not isinstance(out.ranking, ScoredRanking) \
                or not isinstance(out.ranking.scores, Mapping) or set(out.ranking.scores) != set(labels):
            raise ReadoutRefused(f'{variant_id} barrel {barrel_id}: a score is needed for every number '
                                 f'{barrel.low} to {barrel.high}, in a ScoredRanking.')
        if out.map_set is not None:
            raise ReadoutRefused(f'{variant_id} barrel {barrel_id}: a joint selection was returned; this system '
                                 f'reads TOP and WORST from the ranking only.')
        scores = [out.ranking.scores[label] for label in labels]
        if not (all(type(s) is int for s in scores) or all(type(s) is float for s in scores)):
            raise ReadoutRefused(f'{variant_id} barrel {barrel_id}: the scores must be all whole numbers or all '
                                 f'floats.')
        try:
            check_json_value(scores, f'{variant_id} barrel {barrel_id} scores')
        except ValueError as error:
            raise ReadoutRefused(str(error)) from None
        probability = dict(NO_PROBABILITY)
        if out.probability is not None:
            vector = list(out.probability.vector) if isinstance(out.probability, ProbabilityVector) else None
            try:
                if vector is None or len(vector) != len(labels) or any(type(x) is not float for x in vector):
                    raise ValueError('it must be one float for each number')
                check_json_value(vector, f'{variant_id} barrel {barrel_id} probability')
            except ValueError as error:
                raise ReadoutRefused(f'{variant_id} barrel {barrel_id}: the probability vector is not valid: '
                                     f'{error}.') from None
            probability = {'kind': 'RETURNED', 'vector': vector, 'provenance': str(out.probability.provenance)}
        groups = score_groups(scores, barrel.low)
        ranking = order_groups(groups, tie_identity_for(header, barrel_id, TIE_READOUT_VERSION))
        records[barrel_id] = {'barrel_id': barrel_id, 'label_low': barrel.low, 'label_high': barrel.high,
                              'selected_count': barrel.selected, 'scores': scores, 'ranking': ranking,
                              'top': ranking[:barrel.selected],
                              'worst': list(reversed(ranking))[:barrel.selected], 'probability': probability}
    return records


def method_facing_record(records: dict | None) -> dict:
    """The record a method's verify() is given: the keys the existing methods read, in the old record's shape.

    records: read_out's result (None for "not enough history").
    Returns {'record_status': ..., 'barrels': {...}}; each barrel has 'label_low', 'label_high', 'scores',
    'ranking', 'probability', and 'top' and 'worst' as {'labels': [...]}, for example
        {'record_status': 'PREDICTION_AVAILABLE', 'barrels': {'MAIN': {'scores': [...], 'top': {'labels': [...]}, ...}}}.
    """
    if records is None:
        return {'record_status': STATUS_INSUFFICIENT, 'barrels': {}}
    barrels = {}
    for barrel_id, record in records.items():
        barrels[barrel_id] = dict(record, top={'labels': list(record['top'])}, worst={'labels': list(record['worst'])})
    return {'record_status': STATUS_AVAILABLE, 'barrels': barrels}
