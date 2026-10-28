"""E_2-readiness contract (E2R-1 v0.3r3): typed method output, assembly and validation of C1 and C2.

Stage-1 contract library (E2R-CODE-1). The method computes; the contract assembles (E2R-R07): a
method returns only a MethodOutput with no identity fields. The contract adds every identity field
from the declaration, the task and the view, derives equal-score groups, applies TIE_SHA256_V1,
reads TOP and WORST from the one frozen ranking, then validates the whole record by recomputation.
Nothing is written to disk here; freezing a record to a file is orchestration (CODE-2).
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
from collections.abc import Mapping, Sequence

import _common.contract_vocab as V
from _common.contract_records import (
    canonical, check_json_value, check_probability_vector, check_selection, content_digest,
    order_groups, profile_and_barrels, ranking_digest, record_digest, score_groups, tie_identity_for,
    validate_declaration, _keys, _text, _match, _in, _int, _bool, _schema,
)
from _common.contract_task import MethodTask, permitted_view_digest, record_task


# ---------------------------------------------------------------- typed method output (section 7.0)

@dataclass(frozen=True)
class ScoredRanking:
    scores: Mapping[int, object]          # one genuine score per label


@dataclass(frozen=True)
class OrderOnlyRanking:
    ranked_groups: Sequence[Sequence[int]]  # best first; STRICT means groups of one


@dataclass(frozen=True)
class NoRanking:
    reason: str                           # a ranking is declared but unavailable for this target


@dataclass(frozen=True)
class ProbabilityVector:
    vector: Sequence[float]               # label order
    provenance: str


@dataclass(frozen=True)
class BarrelOutput:
    ranking: object = None                # ScoredRanking | OrderOnlyRanking | NoRanking | None
    map_set: Sequence[int] | None = None  # native joint selection (MAP_SET), optional
    probability: ProbabilityVector | None = None


@dataclass(frozen=True)
class DiagnosticValue:
    name: str
    unit: str
    value: object                         # finite int64 or float64, or a list of them


@dataclass(frozen=True)
class MethodOutput:
    barrels: Mapping[str, BarrelOutput] = field(default_factory=dict)
    diagnostic: Sequence[DiagnosticValue] | None = None
    warnings: Sequence[str] = ()


# ---------------------------------------------------------------- header

_HEADER = ('schema', 'game_id', 'profile_version', 'era_id', 'method_id', 'variant_id', 'method_revision',
           'declaration_digest', 'target_draw_number', 'draw_key', 'training_last_draw_number',
           'observation_view', 'include_dates', 'permitted_view_digest', 'fit_sampling_model_version',
           'fit_seed_policy_id', 'fit_seed_identity', 'run_mode', 'product_kind', 'record_status',
           'barrels', 'warnings', 'canonical_content_digest')
_DIAG_HEADER = ('schema', 'game_id', 'profile_version', 'era_id', 'method_id', 'variant_id',
                'method_revision', 'declaration_digest', 'target_draw_number', 'draw_key',
                'training_last_draw_number', 'observation_view', 'include_dates', 'permitted_view_digest',
                'run_mode', 'product_kind', 'diagnostic_schema_id', 'values', 'canonical_content_digest')


def _identity(task: MethodTask, declaration: Mapping, view_digest: str) -> dict:
    p, _ = profile_and_barrels(task.game_id)
    return {'game_id': task.game_id, 'profile_version': task.profile_version, 'era_id': task.era_id,
            'method_id': task.method_id, 'variant_id': task.variant_id,
            'method_revision': task.method_revision, 'declaration_digest': record_digest(declaration),
            'target_draw_number': task.target_draw_number, 'draw_key': p.draw_key(task.target_draw_number),
            'training_last_draw_number': task.target_draw_number - 1,
            'observation_view': task.observation_view, 'include_dates': task.include_dates,
            'permitted_view_digest': view_digest, 'run_mode': task.run_mode}


def _check_task(task: MethodTask, declaration: Mapping) -> None:
    if not isinstance(task, MethodTask):
        raise ValueError('a MethodTask is required')
    for f in ('game_id', 'profile_version', 'era_id', 'method_id', 'variant_id', 'method_revision'):
        if getattr(task, f) != declaration[f]:
            raise ValueError(f'task and declaration disagree on {f}')
    if declaration['stochastic_fit']:
        raise ValueError('no seed policy exists in stage 1: a stochastic fit cannot produce a record (E2R-R61)')


# ---------------------------------------------------------------- per-barrel assembly

def _unavailable(rule_id: str, version: str, status: str) -> dict:
    return {'status': status, 'rule_id': rule_id, 'rule_version': version}


def _assemble_barrel(header: Mapping, channel: Mapping, barrel, out: BarrelOutput | None,
                     insufficient: bool) -> dict:
    bid = barrel.barrel_id
    rk = channel['ranking_kind']
    rv = channel['readout_selection_rule_version']
    top_unavail = V.TOP_UNAVAILABLE_STATUS[bid]
    worst_unavail = V.WORST_UNAVAILABLE_STATUS[bid]
    if out is not None and not isinstance(out, BarrelOutput):
        raise ValueError(f'{bid}: BarrelOutput required')
    rec = {'barrel_id': bid, 'label_low': barrel.low, 'label_high': barrel.high,
           'selected_count': barrel.selected, 'ranking_kind': rk}
    labels = list(range(barrel.low, barrel.high + 1))
    ranking = None
    ranking_obj = None if out is None else out.ranking
    if rk == 'NONE':
        if ranking_obj is not None:
            raise ValueError(f'{bid}: a ranking was returned but none is declared')
        rec['ranking_status'] = 'NOT_DECLARED'
    elif insufficient or ranking_obj is None or isinstance(ranking_obj, NoRanking):
        reason = 'INSUFFICIENT_HISTORY' if insufficient else (
            ranking_obj.reason if isinstance(ranking_obj, NoRanking) else None)
        rec['ranking_status'] = 'UNAVAILABLE'
        rec['ranking_unavailable_reason'] = _text(reason, f'{bid}: ranking unavailable reason')
    else:
        tie = tie_identity_for(header, bid, channel['ranking_tie_readout_version'])
        if rk == 'RANKING_WITH_SCORES':
            if not isinstance(ranking_obj, ScoredRanking):
                raise ValueError(f'{bid}: RANKING_WITH_SCORES needs a ScoredRanking')
            sc = ranking_obj.scores
            if not isinstance(sc, Mapping) or set(sc) != set(labels):
                raise ValueError(f'{bid}: a score is needed for every label')
            scores = [sc[lab] for lab in labels]
            want = int if channel['score_type'] == 'INTEGER' else float
            if any(type(s) is not want for s in scores):
                raise ValueError(f'{bid}: scores must be {channel["score_type"]}')
            check_json_value(scores, f'{bid}.scores')
            groups = score_groups(scores, barrel.low)
            rec['scores'] = scores
            rec['score_direction'] = 'HIGHER_IS_BETTER'
        else:
            if not isinstance(ranking_obj, OrderOnlyRanking):
                raise ValueError(f'{bid}: RANKING_ORDER_ONLY needs an OrderOnlyRanking')
            groups = [sorted(g) for g in ranking_obj.ranked_groups]
            scores = None
        rec['ranking_status'] = 'AVAILABLE'
        rec['ranked_groups'] = groups
        ranking = order_groups(groups, tie)
        rec['ranking'] = ranking
        rec['tie_identity'] = tie
        rec['ranking_digest'] = ranking_digest(rk, scores, groups, ranking,
                                               channel['ranking_tie_readout_version'])
    k = barrel.selected
    top_rule, worst_rule = channel['top_rule_id'], channel['worst_rule_id']
    native = None if out is None else out.map_set
    if top_rule == 'MAP_SET' and not insufficient and native is not None:
        rec['top'] = {'status': V.SELECTION_STATUS_AVAILABLE, 'rule_id': top_rule, 'rule_version': rv,
                      'labels': check_selection(list(native), barrel, f'{bid}.top')}
    elif top_rule == 'TOP_MARGINAL' and ranking is not None:
        if native is not None:
            raise ValueError(f'{bid}: a MAP_SET selection was returned but TOP_MARGINAL is declared')
        rec['top'] = {'status': V.SELECTION_STATUS_AVAILABLE, 'rule_id': top_rule, 'rule_version': rv,
                      'labels': ranking[:k]}
    else:
        if native is not None and not insufficient:
            raise ValueError(f'{bid}: a MAP_SET selection was returned but not declared')
        rec['top'] = _unavailable(top_rule, rv, top_unavail)
    if worst_rule in ('INVERSE', 'INVERSE_FROM_MARGINALS') and ranking is not None:
        rec['worst'] = {'status': V.SELECTION_STATUS_AVAILABLE, 'rule_id': worst_rule, 'rule_version': rv,
                        'labels': list(reversed(ranking))[:k]}
    else:
        rec['worst'] = _unavailable(worst_rule, rv, worst_unavail)
    pk = channel['probability_kind']
    prob = None if out is None else out.probability
    if pk == 'NONE':
        if prob is not None:
            raise ValueError(f'{bid}: a probability vector was returned but none is declared')
        rec['probability'] = {'kind': 'NONE'}
    elif insufficient:
        rec['probability'] = {'kind': pk, 'status': 'UNAVAILABLE', 'unavailable_reason': 'INSUFFICIENT_HISTORY'}
    else:
        if not isinstance(prob, ProbabilityVector):
            raise ValueError(f'{bid}: declared {pk} but no lawful vector (E2R-R16)')
        vec = list(prob.vector)
        check_probability_vector(vec, pk, barrel, channel['probability_sum_tolerance'], f'{bid}.probability')
        rec['probability'] = {'kind': pk, 'status': 'AVAILABLE', 'vector': vec,
                              'tolerance': channel['probability_sum_tolerance'],
                              'smoothing_note': channel['smoothing_note'],
                              'calibration_note': channel['calibration_note'],
                              'provenance': _text(prob.provenance, f'{bid}.probability.provenance'),
                              'digest': record_digest(vec)}
    return rec


def assemble_forecast(declaration: Mapping, task: MethodTask, view, output: MethodOutput) -> dict | None:
    """Build and validate a METHOD_FORECAST_V1 record, or return None when there is no ticket.

    None means no barrel has an available TOP or WORST: the caller writes a C2 record if one is
    declared, or nothing (section 7.4). Insufficient history is decided here, from the view.
    """
    validate_declaration(declaration)
    _check_task(task, declaration)
    product = record_task(task, V.FORECAST).product_kind
    if task.product_kind != product:
        raise ValueError(f'the request product {task.product_kind} is not a forecast product for {task.run_mode}')
    if not isinstance(output, MethodOutput):
        raise ValueError('a MethodOutput is required')
    p, barrels = profile_and_barrels(task.game_id)
    if set(output.barrels) - set(barrels):
        raise ValueError('output names a barrel the profile does not have')
    eligible = len(view.draw_number)
    insufficient = eligible < declaration['minimum_history_draws']
    header = {'schema': V.FORECAST, **_identity(task, declaration, permitted_view_digest(view, task.run_mode)),
              'fit_sampling_model_version': declaration['fit_sampling_model_version'],
              'fit_seed_policy_id': None, 'fit_seed_identity': None, 'product_kind': product}
    recs = {bid: _assemble_barrel(header, declaration['channels'][bid], barrels[bid],
                                  output.barrels.get(bid), insufficient) for bid in sorted(barrels)}
    available = any(r[s]['status'] == V.SELECTION_STATUS_AVAILABLE for r in recs.values() for s in ('top', 'worst'))
    if insufficient:
        status = 'INSUFFICIENT_HISTORY'
    elif available:
        status = 'PREDICTION_AVAILABLE'
    else:
        return None
    warnings = list(output.warnings)
    if any(type(w) is not str for w in warnings):
        raise ValueError('warnings must be text')
    record = {**header, 'record_status': status, 'barrels': recs, 'warnings': warnings}
    record['canonical_content_digest'] = content_digest(record)
    validate_forecast(record, declaration)
    return record


def assemble_diagnostic(declaration: Mapping, task: MethodTask, view, output: MethodOutput) -> dict | None:
    """Build and validate a METHOD_DIAGNOSTIC_V1 record from output.diagnostic, or None if absent."""
    validate_declaration(declaration)
    _check_task(task, declaration)
    task = record_task(task, V.DIAGNOSTIC)   # C2's own product kind (E2RC-C03)
    product = task.product_kind
    if output.diagnostic is None:
        return None
    if declaration['diagnostic_schema_id'] is None:
        raise ValueError('no diagnostic schema is declared: no C2 record may be written')
    values = []
    for dv in output.diagnostic:
        if not isinstance(dv, DiagnosticValue):
            raise ValueError('diagnostic values must be DiagnosticValue')
        item = {'name': dv.name, 'unit': dv.unit, 'value': list(dv.value) if isinstance(dv.value, (list, tuple)) else dv.value}
        if type(item['value']) is list:
            item['length'] = len(item['value'])
        values.append(item)
    record = {'schema': V.DIAGNOSTIC, **_identity(task, declaration, permitted_view_digest(view, task.run_mode)),
              'product_kind': product, 'diagnostic_schema_id': declaration['diagnostic_schema_id'],
              'values': values}
    record['canonical_content_digest'] = content_digest(record)
    validate_diagnostic(record, declaration)
    return record


# ---------------------------------------------------------------- validation by recomputation (7.2, 7.3)

def _validate_header(rec: Mapping, declaration: Mapping, schema: str, where: str) -> None:
    p, _ = profile_and_barrels(rec['game_id'])
    for f in ('game_id', 'profile_version', 'era_id', 'method_id', 'variant_id', 'method_revision'):
        if rec[f] != declaration[f]:
            raise ValueError(f'{where}: {f} does not match the declaration')
    if rec['declaration_digest'] != record_digest(declaration):
        raise ValueError(f'{where}: declaration_digest does not match')
    target = _int(rec['target_draw_number'], f'{where}.target_draw_number')
    if not p.historical_development_target_allowed(target):
        raise ValueError(f'{where}: target outside the development prefix')
    if rec['draw_key'] != p.draw_key(target) or rec['training_last_draw_number'] != target - 1:
        raise ValueError(f'{where}: draw_key or training_last_draw_number inconsistent')
    if rec['observation_view'] not in declaration['observation_views']:
        raise ValueError(f'{where}: observation view not declared')
    if _bool(rec['include_dates'], f'{where}.include_dates') and not declaration['uses_dates']:
        raise ValueError(f'{where}: dates included for a method that does not declare uses_dates')
    _match(V.SHA256, rec['permitted_view_digest'], f'{where}.permitted_view_digest')
    product, _ = V.producible(_in(rec['run_mode'], V.RUN_MODES, f'{where}.run_mode'), schema)
    if rec['product_kind'] != product:
        raise ValueError(f'{where}: product_kind {rec["product_kind"]!r} is not legal here (E2R-R41)')
    if rec['canonical_content_digest'] != content_digest(rec):
        raise ValueError(f'{where}: canonical_content_digest does not match the content')


def _validate_barrel(rec: Mapping, header: Mapping, channel: Mapping, barrel, record_status: str,
                     where: str) -> bool:
    bid, rk = barrel.barrel_id, channel['ranking_kind']
    base = ('barrel_id', 'label_low', 'label_high', 'selected_count', 'ranking_kind', 'ranking_status',
            'top', 'worst', 'probability')
    status = rec.get('ranking_status')
    if status == 'AVAILABLE':
        extra = ('ranked_groups', 'ranking', 'tie_identity', 'ranking_digest') + (
            ('scores', 'score_direction') if rk == 'RANKING_WITH_SCORES' else ())
    elif status == 'UNAVAILABLE':
        extra = ('ranking_unavailable_reason',)
    else:
        extra = ()
    _keys(rec, base + extra, where)
    if (rec['barrel_id'], rec['label_low'], rec['label_high'], rec['selected_count'], rec['ranking_kind']) != (
            bid, barrel.low, barrel.high, barrel.selected, rk):
        raise ValueError(f'{where}: barrel identity does not match the profile and declaration')
    labels = list(range(barrel.low, barrel.high + 1))
    ranking = None
    if rk == 'NONE':
        if status != 'NOT_DECLARED':
            raise ValueError(f'{where}: ranking_status must be NOT_DECLARED')
    elif status == 'UNAVAILABLE':
        _text(rec['ranking_unavailable_reason'], f'{where}.ranking_unavailable_reason')
        if record_status == 'INSUFFICIENT_HISTORY' and rec['ranking_unavailable_reason'] != 'INSUFFICIENT_HISTORY':
            raise ValueError(f'{where}: insufficient history must be the reason')
    elif status == 'AVAILABLE':
        if record_status == 'INSUFFICIENT_HISTORY':
            raise ValueError(f'{where}: no ranking may be recorded with insufficient history')
        tie = tie_identity_for(header, bid, channel['ranking_tie_readout_version'])
        if rec['tie_identity'] != tie:
            raise ValueError(f'{where}: tie_identity does not match the record identity')
        groups = rec['ranked_groups']
        if (type(groups) is not list or any(type(g) is not list or not g or g != sorted(g) for g in groups) or
                sorted(x for g in groups for x in g) != labels or any(type(x) is not int for g in groups for x in g)):
            raise ValueError(f'{where}: ranked_groups must partition the labels exactly, each group ascending')
        if rk == 'RANKING_WITH_SCORES':
            scores = rec['scores']
            want = int if channel['score_type'] == 'INTEGER' else float
            if type(scores) is not list or len(scores) != len(labels) or any(type(s) is not want for s in scores):
                raise ValueError(f'{where}: scores must be one {channel["score_type"]} per label, label order')
            check_json_value(scores, f'{where}.scores')
            if rec['score_direction'] not in V.SCORE_DIRECTIONS:
                raise ValueError(f'{where}: unknown score_direction')
            if groups != score_groups(scores, barrel.low):
                raise ValueError(f'{where}: ranked_groups disagree with the scores (recomputed, not trusted)')
        else:
            scores = None
            if channel['order_ties'] == 'STRICT' and any(len(g) != 1 for g in groups):
                raise ValueError(f'{where}: STRICT order requires groups of one')
        ranking = order_groups(groups, tie)
        if rec['ranking'] != ranking:
            raise ValueError(f'{where}: ranking is not the TIE_SHA256_V1 order of ranked_groups')
        if rec['ranking_digest'] != ranking_digest(rk, scores, groups, ranking, channel['ranking_tie_readout_version']):
            raise ValueError(f'{where}: ranking_digest does not match')
    else:
        raise ValueError(f'{where}: unknown ranking_status')
    k, rv = barrel.selected, channel['readout_selection_rule_version']
    available = False
    for side, rule, unavailable, from_ranking in (
            ('top', channel['top_rule_id'], V.TOP_UNAVAILABLE_STATUS[bid], lambda r: r[:k]),
            ('worst', channel['worst_rule_id'], V.WORST_UNAVAILABLE_STATUS[bid], lambda r: list(reversed(r))[:k])):
        sel = rec[side]
        if type(sel) is not dict or sel.get('rule_id') != rule or sel.get('rule_version') != rv:
            raise ValueError(f'{where}.{side}: rule_id/rule_version must be as declared')
        if sel.get('status') == V.SELECTION_STATUS_AVAILABLE:
            _keys(sel, ('status', 'rule_id', 'rule_version', 'labels'), f'{where}.{side}')
            check_selection(sel['labels'], barrel, f'{where}.{side}')
            if record_status == 'INSUFFICIENT_HISTORY':
                raise ValueError(f'{where}.{side}: no numbers may be recorded with insufficient history')
            if rule == 'MAP_SET':
                pass  # native joint choice, recorded as given (E2R-R30)
            elif rule in ('TOP_MARGINAL', 'INVERSE', 'INVERSE_FROM_MARGINALS'):
                if ranking is None or sel['labels'] != from_ranking(ranking):
                    raise ValueError(f'{where}.{side}: must be read from the one frozen ranking (E2R-R29)')
            else:
                raise ValueError(f'{where}.{side}: an unavailable rule cannot be available')
            available = True
        elif sel.get('status') == unavailable:
            _keys(sel, ('status', 'rule_id', 'rule_version'), f'{where}.{side}')
            if side == 'worst' and ranking is not None and rule != 'INVERSE_UNAVAILABLE':
                raise ValueError(f'{where}.worst: an inverse exists and must be recorded')
            if side == 'top' and ranking is not None and rule == 'TOP_MARGINAL':
                raise ValueError(f'{where}.top: TOP_MARGINAL exists and must be recorded')
        else:
            raise ValueError(f'{where}.{side}: unknown status {sel.get("status")!r}')
    pk = channel['probability_kind']
    pr = rec['probability']
    if pk == 'NONE':
        if pr != {'kind': 'NONE'}:
            raise ValueError(f'{where}.probability: must be {{"kind": "NONE"}}')
    elif record_status == 'INSUFFICIENT_HISTORY':
        if pr != {'kind': pk, 'status': 'UNAVAILABLE', 'unavailable_reason': 'INSUFFICIENT_HISTORY'}:
            raise ValueError(f'{where}.probability: unavailable only for insufficient history')
    else:
        _keys(pr, ('kind', 'status', 'vector', 'tolerance', 'smoothing_note', 'calibration_note',
                   'provenance', 'digest'), f'{where}.probability')
        if (pr['kind'], pr['status'], pr['tolerance'], pr['smoothing_note'], pr['calibration_note']) != (
                pk, 'AVAILABLE', channel['probability_sum_tolerance'], channel['smoothing_note'],
                channel['calibration_note']):
            raise ValueError(f'{where}.probability: kind, tolerance and notes must be as declared')
        check_probability_vector(pr['vector'], pk, barrel, pr['tolerance'], f'{where}.probability.vector')
        _text(pr['provenance'], f'{where}.probability.provenance')
        if pr['digest'] != record_digest(pr['vector']):
            raise ValueError(f'{where}.probability.digest does not match')
    return available


def validate_forecast(rec: object, declaration: Mapping) -> dict:
    """Full recomputation of a METHOD_FORECAST_V1 record against its declaration (E2R-R27..R35)."""
    where = 'forecast'
    _schema(rec, V.FORECAST, where)
    _keys(rec, _HEADER, where)
    check_json_value(rec, where)
    validate_declaration(declaration)
    _validate_header(rec, declaration, V.FORECAST, where)
    if rec['fit_sampling_model_version'] != declaration['fit_sampling_model_version']:
        raise ValueError(f'{where}: fit_sampling_model_version does not match')
    if declaration['stochastic_fit'] or rec['fit_seed_policy_id'] is not None or rec['fit_seed_identity'] is not None:
        raise ValueError(f'{where}: seed fields are null for a deterministic fit; no stochastic record in stage 1')
    status = _in(rec['record_status'], V.RECORD_STATUSES, f'{where}.record_status')
    _, barrels = profile_and_barrels(rec['game_id'])
    if type(rec['barrels']) is not dict or set(rec['barrels']) != set(barrels):
        raise ValueError(f'{where}: barrels must be exactly the profile barrels (absent barrels are not written)')
    available = [_validate_barrel(rec['barrels'][b], rec, declaration['channels'][b], barrels[b], status,
                                  f'{where}.barrels.{b}') for b in sorted(barrels)]
    if status == 'PREDICTION_AVAILABLE' and not any(available):
        raise ValueError(f'{where}: PREDICTION_AVAILABLE needs an available TOP or WORST (7.4)')
    if type(rec['warnings']) is not list or any(type(w) is not str for w in rec['warnings']):
        raise ValueError(f'{where}: warnings must be a list of text')
    return rec


def validate_diagnostic(rec: object, declaration: Mapping) -> dict:
    where = 'diagnostic'
    _schema(rec, V.DIAGNOSTIC, where)
    _keys(rec, _DIAG_HEADER, where)
    check_json_value(rec, where)
    validate_declaration(declaration)
    if declaration['diagnostic_schema_id'] is None or rec['diagnostic_schema_id'] != declaration['diagnostic_schema_id']:
        raise ValueError(f'{where}: diagnostic_schema_id must be the declared one')
    _validate_header(rec, declaration, V.DIAGNOSTIC, where)
    values = rec['values']
    if type(values) is not list:
        raise ValueError(f'{where}: values must be a list')
    names = set()
    for i, item in enumerate(values):
        w = f'{where}.values[{i}]'
        v = item.get('value') if type(item) is dict else None
        _keys(item, ('name', 'unit', 'value') + (('length',) if type(v) is list else ()), w)
        if _text(item['name'], f'{w}.name') in names:
            raise ValueError(f'{w}: duplicate name')
        names.add(item['name'])
        _text(item['unit'], f'{w}.unit')
        items = v if type(v) is list else [v]
        if type(v) is list and item['length'] != len(v):
            raise ValueError(f'{w}: stated length does not match')
        if any(type(x) not in (int, float) for x in items):
            raise ValueError(f'{w}: value must be int64 or float64, or a list of them')
    return rec
