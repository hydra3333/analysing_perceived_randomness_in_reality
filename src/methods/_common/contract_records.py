"""E_2-readiness contract (E2R-1 v0.3r3): canonical encoding checks and fail-closed record validators.

Stage-1 contract library (E2R-CODE-1). Shared code: no method import, no file or network access,
no process action. Validators recompute everything they can and accept nothing they cannot check:
unknown schemas, unknown or missing fields and values outside a closed vocabulary all fail
(E2R-R06). A validation failure raises ValueError; nothing is corrected silently (E2R-R03).
"""
from __future__ import annotations

from datetime import date
import hashlib
import math
from collections.abc import Mapping, Sequence

from _common.canonical_encoding import canonical_bytes, length32_tuple
from _common.game_profiles import get_profile
import _common.contract_vocab as V

REVIEWED_SEED_POLICIES: frozenset[str] = frozenset()  # stage 1: none exists (E2R-R61, E2R-T08, T18)


# ---------------------------------------------------------------- encoding (section 4)

def check_json_value(value: object, where: str = 'record') -> None:
    """Every value is canonical-JSON-safe: int64 ints, finite float64 floats, no negative zero."""
    if value is None or type(value) is bool or type(value) is str:
        return
    if type(value) is int:
        if not V.INT64_MIN <= value <= V.INT64_MAX:
            raise ValueError(f'{where}: integer outside int64')
        return
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError(f'{where}: non-finite float')
        if value == 0.0 and math.copysign(1.0, value) < 0:
            raise ValueError(f'{where}: negative zero (E2R-R12)')
        return
    if type(value) is list:
        for i, item in enumerate(value):
            check_json_value(item, f'{where}[{i}]')
        return
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise ValueError(f'{where}: non-text key')
            check_json_value(item, f'{where}.{key}')
        return
    raise ValueError(f'{where}: type {type(value).__name__} is not allowed in a record')


def canonical(record) -> bytes:
    check_json_value(record)
    return canonical_bytes(record)


def sha256_hex(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def record_digest(record) -> str:
    """Digest of a whole record: SHA-256 of its canonical bytes (E2R-R10)."""
    return sha256_hex(canonical(record))


def content_digest(record: Mapping) -> str:
    """SHA-256 of the canonical bytes of the record without its canonical_content_digest field."""
    body = {k: v for k, v in record.items() if k != 'canonical_content_digest'}
    return record_digest(body)


# ---------------------------------------------------------------- small checks

def _keys(rec: object, required: Sequence[str], where: str, optional: Sequence[str] = ()) -> None:
    if type(rec) is not dict:
        raise ValueError(f'{where}: must be an object')
    missing = set(required) - set(rec)
    extra = set(rec) - set(required) - set(optional)
    if missing or extra:
        raise ValueError(f'{where}: missing {sorted(missing)} unknown {sorted(extra)}')


def _text(v: object, where: str) -> str:
    if type(v) is not str or not v.strip():
        raise ValueError(f'{where}: non-empty text required')
    return v


def _match(pattern, v: object, where: str) -> str:
    if type(v) is not str or not pattern.fullmatch(v):
        raise ValueError(f'{where}: invalid format')
    return v


def _int(v: object, where: str, low: int | None = None, high: int | None = None) -> int:
    if type(v) is not int:
        raise ValueError(f'{where}: integer required')
    if (low is not None and v < low) or (high is not None and v > high):
        raise ValueError(f'{where}: out of range')
    return v


def _bool(v: object, where: str) -> bool:
    if type(v) is not bool:
        raise ValueError(f'{where}: boolean required')
    return v


def _in(v: object, vocab, where: str) -> str:
    if type(v) is not str or v not in vocab:
        raise ValueError(f'{where}: {v!r} is not in the closed vocabulary')
    return v


def _iso_date(v: object, where: str) -> str:
    if type(v) is not str:
        raise ValueError(f'{where}: ISO date required')
    try:
        if date.fromisoformat(v).isoformat() != v:
            raise ValueError
    except ValueError:
        raise ValueError(f'{where}: ISO date required') from None
    return v


def _schema(rec: Mapping, schema: str, where: str) -> None:
    s = rec.get('schema') if type(rec) is dict else None
    if s in V.LEGACY_READ_ONLY_SCHEMAS:
        raise ValueError(f'{where}: legacy schema {s} is read-only and cannot be written (E2R-R49)')
    if s != schema:
        raise ValueError(f'{where}: unknown or wrong schema {s!r}')


def profile_and_barrels(game_id: object):
    if type(game_id) is not str:
        raise ValueError('game_id must be text')
    p = get_profile(game_id)
    return p, {b.barrel_id: b for b in p.barrels}


# ---------------------------------------------------------------- (A1) declaration, section 5

_DECL_FIELDS = ('schema', 'game_id', 'profile_version', 'era_id', 'method_id', 'variant_id',
                'method_revision', 'observation_views', 'uses_dates', 'minimum_history_draws',
                'stochastic_fit', 'fit_seed_policy_id', 'fit_sampling_model_version', 'channels',
                'diagnostic_schema_id', 'is_capability', 'is_interface_version',
                'source_method_dependencies')
_CHANNEL_FIELDS = ('ranking_kind', 'score_type', 'order_ties', 'top_rule_id', 'worst_rule_id',
                   'readout_selection_rule_version', 'ranking_tie_readout_version', 'probability_kind',
                   'probability_sum_tolerance', 'smoothing_note', 'calibration_note')


def validate_channel(ch: object, barrel_id: str, where: str) -> None:
    _keys(ch, _CHANNEL_FIELDS, where)
    rk = _in(ch['ranking_kind'], V.RANKING_KINDS, f'{where}.ranking_kind')
    st = _in(ch['score_type'], V.SCORE_TYPES, f'{where}.score_type')
    ot = _in(ch['order_ties'], V.ORDER_TIES, f'{where}.order_ties')
    top = _in(ch['top_rule_id'], V.TOP_RULES, f'{where}.top_rule_id')
    worst = _in(ch['worst_rule_id'], V.WORST_RULES, f'{where}.worst_rule_id')
    if (rk == 'RANKING_WITH_SCORES') != (st in ('INTEGER', 'FLOAT64')):
        raise ValueError(f'{where}: score_type must be INTEGER or FLOAT64 exactly when RANKING_WITH_SCORES')
    if (rk == 'RANKING_ORDER_ONLY') != (ot in ('STRICT', 'GROUPED')):
        raise ValueError(f'{where}: order_ties is STRICT/GROUPED exactly for RANKING_ORDER_ONLY')
    if (rk != 'NONE', top, worst) not in V.LEGAL_CHANNELS:
        raise ValueError(f'{where}: illegal channel combination {rk}/{top}/{worst} (E2R-R15A)')
    _match(V.VERSION_TAG, ch['readout_selection_rule_version'], f'{where}.readout_selection_rule_version')
    tie = _in(ch['ranking_tie_readout_version'], V.TIE_VERSIONS, f'{where}.ranking_tie_readout_version')
    if (tie == 'TIE_SHA256_V1') != (rk != 'NONE'):
        raise ValueError(f'{where}: TIE_SHA256_V1 exactly when a ranking is declared')
    pk = _in(ch['probability_kind'], V.PROBABILITY_KINDS[barrel_id], f'{where}.probability_kind')
    tol, sn, cn = ch['probability_sum_tolerance'], ch['smoothing_note'], ch['calibration_note']
    if pk == 'NONE':
        if tol is not None or sn is not None or cn is not None:
            raise ValueError(f'{where}: tolerance and notes must be null when probability_kind is NONE')
    else:
        if type(tol) is not float or not math.isfinite(tol) or not 0.0 < tol <= V.REVIEWER_TOLERANCE_LIMIT:
            raise ValueError(f'{where}: probability_sum_tolerance must be a float in (0, 1e-9] (E2R-R17)')
        _text(sn, f'{where}.smoothing_note')
        _text(cn, f'{where}.calibration_note')


def validate_declaration(d: object) -> dict:
    """Validate a METHOD_DECLARATION_V1 (sections 5.1-5.4). Returns it unchanged."""
    where = 'declaration'
    _schema(d, V.DECLARATION, where)
    _keys(d, _DECL_FIELDS, where)
    check_json_value(d, where)
    p, barrels = profile_and_barrels(d['game_id'])
    if d['profile_version'] != p.version or d['era_id'] != p.era_id:
        raise ValueError(f'{where}: profile_version/era_id must equal the frozen game profile')
    _match(V.METHOD_ID, d['method_id'], f'{where}.method_id')
    variant = _match(V.VARIANT_ID, d['variant_id'], f'{where}.variant_id')
    if variant == V.NOT_YET_SPECIFIED:
        raise ValueError(f'{where}: {V.NOT_YET_SPECIFIED} is reserved for registry entries with no declaration')
    _match(V.REVISION, d['method_revision'], f'{where}.method_revision')
    views = d['observation_views']
    if (type(views) is not list or not views or views != sorted(set(views)) or
            any(v not in V.OBSERVATION_VIEWS for v in views)):
        raise ValueError(f'{where}: observation_views must be a non-empty, sorted, duplicate-free subset')
    _bool(d['uses_dates'], f'{where}.uses_dates')
    _int(d['minimum_history_draws'], f'{where}.minimum_history_draws', low=1)
    stochastic = _bool(d['stochastic_fit'], f'{where}.stochastic_fit')
    policy = d['fit_seed_policy_id']
    if not stochastic and policy is not None:
        raise ValueError(f'{where}: fit_seed_policy_id must be null for a deterministic fit')
    if policy is not None:
        _match(V.VERSION_TAG, policy, f'{where}.fit_seed_policy_id')
    _match(V.VERSION_TAG, d['fit_sampling_model_version'], f'{where}.fit_sampling_model_version')
    ch = d['channels']
    if type(ch) is not dict or set(ch) != set(barrels):
        raise ValueError(f'{where}: channels must name exactly the profile barrels '
                         f'{sorted(barrels)}; an absent barrel is not written (no zero-padding)')
    for bid in sorted(ch):
        validate_channel(ch[bid], bid, f'{where}.channels.{bid}')
    diag = d['diagnostic_schema_id']
    if diag is not None:
        _match(V.VERSION_TAG, diag, f'{where}.diagnostic_schema_id')
    _in(d['is_capability'], V.IS_CAPABILITIES, f'{where}.is_capability')
    if d['is_interface_version'] is not None:
        raise ValueError(f'{where}: is_interface_version must be null in stage 1 (E2R-R48, E2R-T08)')
    if d['source_method_dependencies'] != []:
        raise ValueError(f'{where}: source_method_dependencies are reserved for ensembles (E2R-R48)')
    produces = any(c['ranking_kind'] != 'NONE' or c['top_rule_id'] != 'TOP_UNAVAILABLE' or
                   c['probability_kind'] != 'NONE' for c in ch.values())
    if not produces and diag is None:
        raise ValueError(f'{where}: declares no output of any kind')
    return d


# ---------------------------------------------------------------- (A2) registry entries, section 5.5

_ENTRY_FIELDS = ('schema', 'game_id', 'method_id', 'variant_id', 'entry_sequence', 'method_revision',
                 'declaration_digest', 'registry_status', 'registry_status_reason', 'method_name',
                 'one_liner', 'short_explanation', 'text_provenance', 'effective_date',
                 'previous_entry_digest')


def validate_registry_entry(e: object) -> dict:
    where = 'registry entry'
    _schema(e, V.REGISTRY_ENTRY, where)
    _keys(e, _ENTRY_FIELDS, where)
    check_json_value(e, where)
    profile_and_barrels(e['game_id'])
    _match(V.METHOD_ID, e['method_id'], f'{where}.method_id')
    variant = _match(V.VARIANT_ID, e['variant_id'], f'{where}.variant_id')
    seq = _int(e['entry_sequence'], f'{where}.entry_sequence', low=1)
    rev, dig = e['method_revision'], e['declaration_digest']
    status = _in(e['registry_status'], V.REGISTRY_STATUSES, f'{where}.registry_status')
    if (rev is None) != (dig is None):
        raise ValueError(f'{where}: method_revision and declaration_digest are both null or both set')
    if rev is None:
        if status != 'FORMULA_OPEN':
            raise ValueError(f'{where}: only a FORMULA_OPEN entry may have no declaration')
    else:
        _match(V.REVISION, rev, f'{where}.method_revision')
        _match(V.SHA256, dig, f'{where}.declaration_digest')
    if variant == V.NOT_YET_SPECIFIED and (rev is not None or status != 'FORMULA_OPEN'):
        raise ValueError(f'{where}: a {V.NOT_YET_SPECIFIED} entry is FORMULA_OPEN with no declaration')
    for f in ('registry_status_reason', 'method_name', 'one_liner', 'short_explanation'):
        _text(e[f], f'{where}.{f}')
    tp = e['text_provenance']
    _keys(tp, ('author', 'date', 'text_version', 'source_reference'), f'{where}.text_provenance')
    _text(tp['author'], f'{where}.text_provenance.author')
    _iso_date(tp['date'], f'{where}.text_provenance.date')
    _text(tp['text_version'], f'{where}.text_provenance.text_version')
    _text(tp['source_reference'], f'{where}.text_provenance.source_reference')
    _iso_date(e['effective_date'], f'{where}.effective_date')
    prev = e['previous_entry_digest']
    if seq == 1:
        if prev is not None:
            raise ValueError(f'{where}: the first entry has no previous_entry_digest')
    else:
        _match(V.SHA256, prev, f'{where}.previous_entry_digest')
    return e


def validate_registry_chain(entries: Sequence[Mapping]) -> dict:
    """Append-only chain for one (game, method, variant): 1, 2, 3 ... linked by digests.

    Returns the active (newest) entry."""
    if not entries:
        raise ValueError('registry chain is empty')
    key = None
    for i, e in enumerate(entries, start=1):
        validate_registry_entry(e)
        k = (e['game_id'], e['method_id'], e['variant_id'])
        if key is None:
            key = k
        elif k != key:
            raise ValueError('registry chain mixes method variants')
        if e['entry_sequence'] != i:
            raise ValueError('registry chain has a gap or is out of order')
        if i > 1 and e['previous_entry_digest'] != record_digest(entries[i - 2]):
            raise ValueError('registry chain link does not match the previous entry (edited history?)')
    return dict(entries[-1])


def validate_entry_declaration_pair(entry: Mapping, declaration: Mapping | None) -> None:
    """An entry governs exactly the declaration whose digest it names (E2R-R21C)."""
    if entry['declaration_digest'] is None:
        if declaration is not None:
            raise ValueError('entry names no declaration')
        return
    if declaration is None:
        raise ValueError('entry names a declaration that is not installed')
    validate_declaration(declaration)
    if record_digest(declaration) != entry['declaration_digest']:
        raise ValueError('declaration digest does not match the registry entry')
    for f in ('game_id', 'method_id', 'variant_id', 'method_revision'):
        if declaration[f] != entry[f]:
            raise ValueError(f'registry entry and declaration disagree on {f}')
    if entry['registry_status'] == 'SUPPORTED' and declaration['stochastic_fit']:
        if declaration['fit_seed_policy_id'] not in REVIEWED_SEED_POLICIES:
            raise ValueError('a SUPPORTED entry needs a reviewed seed policy for a stochastic fit '
                             '(E2R-R21C, E2R-R61); none exists in stage 1')


# ---------------------------------------------------------------- (B) run request, section 6.1

_REQUEST_FIELDS = ('schema', 'game_id', 'method_id', 'variant_id', 'method_revision', 'target_draw_number',
                   'observation_view', 'include_dates', 'run_mode', 'product_kind', 'declaration_digest',
                   'registry_entry_digest', 'run_id', 'master_file', 'ledger_version', 'master_sha256')


def validate_run_request(r: object) -> dict:
    where = 'run request'
    _schema(r, V.RUN_REQUEST, where)
    _keys(r, _REQUEST_FIELDS, where)
    check_json_value(r, where)
    p, _ = profile_and_barrels(r['game_id'])
    _match(V.METHOD_ID, r['method_id'], f'{where}.method_id')
    if _match(V.VARIANT_ID, r['variant_id'], f'{where}.variant_id') == V.NOT_YET_SPECIFIED:
        raise ValueError(f'{where}: a method with no specification cannot be requested')
    _match(V.REVISION, r['method_revision'], f'{where}.method_revision')
    target = _int(r['target_draw_number'], f'{where}.target_draw_number')
    if not p.historical_development_target_allowed(target):
        raise ValueError(f'{where}: target is outside the authorised development prefix (E2R-R52)')
    _in(r['observation_view'], V.OBSERVATION_VIEWS, f'{where}.observation_view')
    _bool(r['include_dates'], f'{where}.include_dates')
    mode = _in(r['run_mode'], V.RUN_MODES, f'{where}.run_mode')
    product = _in(r['product_kind'], V.PRODUCT_KINDS, f'{where}.product_kind')
    allowed = set()
    for schema in (V.FORECAST, V.DIAGNOSTIC):
        try:
            allowed.add(V.producible(mode, schema)[0])
        except ValueError:
            pass
    if product not in allowed:
        raise ValueError(f'{where}: {mode}/{product} is not a producible stage-1 combination (E2R-R41)')
    _match(V.SHA256, r['declaration_digest'], f'{where}.declaration_digest')
    _match(V.SHA256, r['registry_entry_digest'], f'{where}.registry_entry_digest')
    _match(V.RUN_ID, r['run_id'], f'{where}.run_id')
    if r['master_file'] != f'{p.game_id}_results_master.csv':
        raise ValueError(f'{where}: unapproved master file')
    _int(r['ledger_version'], f'{where}.ledger_version', low=1, high=1)
    _match(V.SHA256, r['master_sha256'], f'{where}.master_sha256')
    return r


def reader_pin(request: Mapping) -> dict:
    """The reader's existing development pin, derived from a valid run request (orchestration only)."""
    validate_run_request(request)
    return {'schema': 'DEVELOPMENT_MASTER_PIN_V1_REVIEW', 'game_id': request['game_id'],
            'method_id': request['method_id'], 'variant_id': request['variant_id'],
            'draw_number': request['target_draw_number'], 'view_kind': request['observation_view'],
            'include_dates': request['include_dates'], 'master_file': request['master_file'],
            'ledger_version': request['ledger_version'], 'master_sha256': request['master_sha256']}


# ---------------------------------------------------------------- ranking and tie rules (E2R-R27..R29)

def tie_digest(tie_identity: Mapping, label: int) -> str:
    """TIE_SHA256_V1: SHA-256 over the eight length-prefixed fields (E2R-R28, TIE v0.2)."""
    fields = (tie_identity['domain'], tie_identity['training_view_sha256'],
              str(tie_identity['target_draw_number']), tie_identity['method_id'],
              tie_identity['variant_id'], tie_identity['barrel_id'],
              tie_identity['ranking_tie_readout_version'], str(label))
    return hashlib.sha256(length32_tuple(fields)).hexdigest()


def order_groups(groups: Sequence[Sequence[int]], tie_identity: Mapping) -> list[int]:
    """The frozen ranking: groups in order, each ordered by ascending tie digest, label as fallback."""
    ranking = []
    for g in groups:
        if len(g) == 1:
            ranking.extend(g)
        else:
            ranking.extend(sorted(g, key=lambda lab: (tie_digest(tie_identity, lab), lab)))
    return ranking


def score_groups(scores: Sequence, low: int) -> list[list[int]]:
    """Equal-score groups, best (highest) first, labels ascending within a group (E2R-R27)."""
    by_score: dict = {}
    for i, s in enumerate(scores):
        by_score.setdefault(s, []).append(low + i)
    return [sorted(by_score[s]) for s in sorted(by_score, reverse=True)]


def ranking_digest(ranking_kind: str, scores, groups, ranking, tie_version: str) -> str:
    return record_digest({'digest_version': 'RANKING_DIGEST_V1', 'ranking_kind': ranking_kind,
                          'scores': scores, 'ranked_groups': groups, 'ranking': ranking,
                          'ranking_tie_readout_version': tie_version})


def tie_identity_for(record: Mapping, barrel_id: str, tie_version: str) -> dict:
    return {'domain': V.TIE_DOMAIN, 'training_view_sha256': record['permitted_view_digest'],
            'target_draw_number': record['target_draw_number'], 'method_id': record['method_id'],
            'variant_id': record['variant_id'], 'barrel_id': barrel_id,
            'ranking_tie_readout_version': tie_version}


def check_selection(labels: object, barrel, where: str) -> list[int]:
    """Distinct integers in range, exactly selected_count of them (E2R-R32)."""
    if (type(labels) is not list or len(labels) != barrel.selected or
            any(type(x) is not int for x in labels) or len(set(labels)) != len(labels) or
            any(not barrel.low <= x <= barrel.high for x in labels)):
        raise ValueError(f'{where}: a selection needs {barrel.selected} distinct labels in '
                         f'{barrel.low}..{barrel.high}')
    return labels


def check_probability_vector(vec: object, kind: str, barrel, tolerance: float, where: str) -> None:
    n = barrel.high - barrel.low + 1
    if type(vec) is not list or len(vec) != n:
        raise ValueError(f'{where}: probability vector must have {n} elements')
    for i, x in enumerate(vec):
        if type(x) is not float:
            raise ValueError(f'{where}[{i}]: probability must be a float64')
        check_json_value(x, f'{where}[{i}]')
        if not 0.0 <= x <= 1.0:
            raise ValueError(f'{where}[{i}]: probability outside [0, 1]')
    if abs(math.fsum(vec) - V.PROBABILITY_SUM[kind]) > tolerance:
        raise ValueError(f'{where}: probabilities do not sum to {V.PROBABILITY_SUM[kind]} within tolerance')
