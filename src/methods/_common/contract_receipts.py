"""E_2-readiness contract (E2R-1 v0.3r3): receipts, terminal records, the score-record type and consumption.

Stage-1 contract library (E2R-CODE-1). Types and validators only: no function here opens, writes,
renames or deletes a file, starts or stops a process, or reads an outcome. Publishing these records
(create-only, in the order of E2R-R38A) is orchestration work for CODE-2. The consumption rule is a
pure function over records; the caller supplies the result of every existing gate (exit receipt,
orphan-marker interlock) as an explicit boolean.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
import re

import _common.contract_vocab as V
from _common.contract_forecast import validate_diagnostic, validate_forecast
from _common.contract_records import (
    canonical, check_json_value, profile_and_barrels, record_digest, sha256_hex,
    _keys, _text, _match, _in, _int, _bool, _schema,
)

_RECEIPT_FIELDS = ('schema', 'forecast_content_digest', 'forecast_file_sha256', 'game_id',
                   'target_draw_number', 'method_id', 'variant_id', 'method_revision', 'master_file',
                   'ledger_version', 'master_sha256', 'ledger_sha256', 'init_record_sha256',
                   'environment_identity', 'run_id', 'execution_path', 'registry_entry_digest', 'run_mode',
                   'product_kind', 'evidence_tier', 'window', 'cohort_id', 'status_at_freeze',
                   'outcome_opened_at_freeze', 'frozen_at_utc')
_DIAG_RECEIPT_FIELDS = tuple('diagnostic_content_digest' if f == 'forecast_content_digest' else
                             'diagnostic_file_sha256' if f == 'forecast_file_sha256' else f
                             for f in _RECEIPT_FIELDS if f not in ('cohort_id', 'status_at_freeze'))
_ENV_FIELDS = ('python_version', 'numpy_version', 'psutil_version', 'os_name', 'os_build',
               'installed_packages_digest')
_TERMINAL_FIELDS = ('schema', 'run_id', 'game_id', 'method_id', 'variant_id', 'method_revision',
                    'target_draw_number', 'execution_path', 'outcome', 'outcome_reason',
                    'registry_entry_digest', 'receipt_digests')


# A UTC date-time with an explicit clock time and one final Z (E2RC1-C01): YYYY-MM-DDTHH:MM:SS, then
# optionally 1 to 6 fraction digits, then Z. No offset, no date-only form, ASCII digits only. The
# value is informational: it is not proof that publication preceded an outcome (E2R-R40C, R2 8.2A).
_UTC_TIMESTAMP = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z')


def _utc(v: object, where: str) -> str:
    if type(v) is not str or _UTC_TIMESTAMP.fullmatch(v) is None:
        raise ValueError(f'{where}: UTC date-time YYYY-MM-DDTHH:MM:SS[.ffffff]Z required')
    try:
        datetime.strptime(v[:19], '%Y-%m-%dT%H:%M:%S')   # rejects impossible dates and times
    except ValueError:
        raise ValueError(f'{where}: not a real UTC date-time') from None
    return v


def status_at_freeze(record: Mapping) -> dict:
    return {'record_status': record['record_status'],
            'barrels': {b: {'top': r['top']['status'], 'worst': r['worst']['status']}
                        for b, r in sorted(record['barrels'].items())}}


def _common_receipt(r: Mapping, record: Mapping, where: str) -> None:
    for f in ('game_id', 'target_draw_number', 'method_id', 'variant_id', 'method_revision', 'run_mode',
              'product_kind'):
        if r[f] != record[f]:
            raise ValueError(f'{where}: {f} differs from the frozen record')
    p, _ = profile_and_barrels(r['game_id'])
    if r['master_file'] != f'{p.game_id}_results_master.csv':
        raise ValueError(f'{where}: unapproved master file')
    _int(r['ledger_version'], f'{where}.ledger_version', low=1, high=1)
    for f in ('master_sha256', 'ledger_sha256', 'init_record_sha256', 'registry_entry_digest'):
        _match(V.SHA256, r[f], f'{where}.{f}')
    env = r['environment_identity']
    _keys(env, _ENV_FIELDS, f'{where}.environment_identity')
    for f in _ENV_FIELDS[:-1]:
        _text(env[f], f'{where}.environment_identity.{f}')
    _match(V.SHA256, env['installed_packages_digest'], f'{where}.environment_identity.installed_packages_digest')
    _match(V.RUN_ID, r['run_id'], f'{where}.run_id')
    _in(r['execution_path'], V.EXECUTION_PATHS, f'{where}.execution_path')
    w = r['window']
    if w is not None and (type(w) is not list or len(w) != 2 or any(type(x) is not int for x in w) or w[0] > w[1]):
        raise ValueError(f'{where}: window must be null or [S, L] with S <= L')
    if r['outcome_opened_at_freeze'] is not False:
        raise ValueError(f'{where}: outcome_opened_at_freeze must be false')
    _utc(r['frozen_at_utc'], f'{where}.frozen_at_utc')


def validate_freeze_receipt(r: object, forecast: Mapping) -> dict:
    """FORECAST_FREEZE_RECEIPT_V1 against the frozen C1 record it names (section 8.1). No scoring field."""
    where = 'freeze receipt'
    _schema(r, V.FREEZE_RECEIPT, where)
    _keys(r, _RECEIPT_FIELDS, where)
    check_json_value(r, where)
    if forecast.get('schema') != V.FORECAST:
        raise ValueError(f'{where}: names a record that is not METHOD_FORECAST_V1')
    if r['forecast_content_digest'] != forecast['canonical_content_digest']:
        raise ValueError(f'{where}: forecast_content_digest does not match')
    if r['forecast_file_sha256'] != sha256_hex(canonical(forecast)):
        raise ValueError(f'{where}: forecast_file_sha256 is not the frozen file bytes')
    _common_receipt(r, forecast, where)
    product, tier = V.producible(r['run_mode'], V.FORECAST)
    if (r['product_kind'], r['evidence_tier']) != (product, tier):
        raise ValueError(f'{where}: evidence_tier does not match the run mode (E2R-R41)')
    c = r['cohort_id']
    if c is not None and c != 'EXPLORATORY_COHORT':
        _match(V.VERSION_TAG, c, f'{where}.cohort_id')
    if r['status_at_freeze'] != status_at_freeze(forecast):
        raise ValueError(f'{where}: status_at_freeze does not match the record')
    return r


def validate_diagnostic_receipt(r: object, diagnostic: Mapping) -> dict:
    where = 'diagnostic receipt'
    _schema(r, V.DIAGNOSTIC_RECEIPT, where)
    _keys(r, _DIAG_RECEIPT_FIELDS, where)
    check_json_value(r, where)
    if diagnostic.get('schema') != V.DIAGNOSTIC:
        raise ValueError(f'{where}: names a record that is not METHOD_DIAGNOSTIC_V1')
    if r['diagnostic_content_digest'] != diagnostic['canonical_content_digest']:
        raise ValueError(f'{where}: diagnostic_content_digest does not match')
    if r['diagnostic_file_sha256'] != sha256_hex(canonical(diagnostic)):
        raise ValueError(f'{where}: diagnostic_file_sha256 is not the frozen file bytes')
    _common_receipt(r, diagnostic, where)
    if (r['product_kind'], r['evidence_tier']) != V.producible(r['run_mode'], V.DIAGNOSTIC):
        raise ValueError(f'{where}: evidence_tier does not match')
    return r


def validate_terminal(t: object) -> dict:
    """RUN_TERMINAL_RECORD_V1 (section 8.3): every run that completes the protocol ends with one."""
    where = 'terminal record'
    _schema(t, V.TERMINAL, where)
    _keys(t, _TERMINAL_FIELDS, where)
    check_json_value(t, where)
    _match(V.RUN_ID, t['run_id'], f'{where}.run_id')
    profile_and_barrels(t['game_id'])
    _match(V.METHOD_ID, t['method_id'], f'{where}.method_id')
    _match(V.VARIANT_ID, t['variant_id'], f'{where}.variant_id')
    _match(V.REVISION, t['method_revision'], f'{where}.method_revision')
    _int(t['target_draw_number'], f'{where}.target_draw_number', low=1)
    _in(t['execution_path'], V.EXECUTION_PATHS, f'{where}.execution_path')
    outcome = _in(t['outcome'], V.TERMINAL_OUTCOMES, f'{where}.outcome')
    _text(t['outcome_reason'], f'{where}.outcome_reason')
    _match(V.SHA256, t['registry_entry_digest'], f'{where}.registry_entry_digest')
    rd = t['receipt_digests']
    if type(rd) is not list or rd != sorted(set(rd)) or any(type(x) is not str or not V.SHA256.fullmatch(x) for x in rd):
        raise ValueError(f'{where}: receipt_digests must be a sorted, duplicate-free list of SHA-256')
    if (outcome == 'SUCCESS') != bool(rd):
        raise ValueError(f'{where}: a SUCCESS names its receipts; any other outcome names none')
    return t


def consumable(output: Mapping, receipt: Mapping, terminal: Mapping | None, *, gates_pass: bool,
               declaration: Mapping) -> tuple[bool, str]:
    """E2R-R38A: an output is consumable only with a valid SUCCESS terminal record naming a receipt that
    matches it, and only if every existing group and firewall gate passes. Anything else is not
    successful. This function never deletes, moves, quarantines or terminates anything."""
    if terminal is None:
        return False, 'NO_TERMINAL_RECORD'
    try:
        validate_terminal(terminal)
    except ValueError as exc:
        return False, f'INVALID_TERMINAL_RECORD: {exc}'
    if terminal['outcome'] != 'SUCCESS':
        return False, f'TERMINAL_{terminal["outcome"]}'
    try:
        if output.get('schema') == V.FORECAST:
            validate_forecast(output, declaration)
            validate_freeze_receipt(receipt, output)
        else:
            validate_diagnostic(output, declaration)
            validate_diagnostic_receipt(receipt, output)
    except ValueError as exc:
        return False, f'INVALID_OUTPUT_OR_RECEIPT: {exc}'
    if record_digest(receipt) not in terminal['receipt_digests']:
        return False, 'RECEIPT_NOT_NAMED_BY_TERMINAL_RECORD'
    for f in ('run_id', 'game_id', 'method_id', 'variant_id', 'method_revision', 'execution_path',
              'registry_entry_digest'):
        if receipt[f] != terminal[f]:
            return False, f'TERMINAL_AND_RECEIPT_DISAGREE_ON_{f.upper()}'
    if receipt['target_draw_number'] != terminal['target_draw_number']:
        return False, 'TERMINAL_AND_RECEIPT_DISAGREE_ON_TARGET'
    if gates_pass is not True:
        return False, 'GROUP_OR_FIREWALL_GATE_FAILED'
    return True, 'CONSUMABLE'


# ---------------------------------------------------------------- (E) post-outcome score record, type only (section 10)

_SCORE_FIELDS_PB = ('schema', 'game_id', 'draw_number', 'track_id', 'mode', 'method_revision',
                    'forecast_content_digest', 'freeze_receipt_digest', 'drawn_main', 'drawn_powerball',
                    'main_matches', 'powerball_match', 'division', 'evaluator_version')
_SCORE_FIELDS_OZ = ('schema', 'game_id', 'draw_number', 'track_id', 'mode', 'method_revision',
                    'forecast_content_digest', 'freeze_receipt_digest', 'drawn_main',
                    'main_matches', 'supplementary_matches', 'division', 'evaluator_version')


def track_id(game_id: str, method_id: str, variant_id: str, readout: str, mode: str) -> str:
    """E2R-R40: GAME:METHOD:VARIANT:READOUT:MODE; the revision is not part of it (owner decision D-1)."""
    profile_and_barrels(game_id)
    _match(V.METHOD_ID, method_id, 'track method_id')
    _match(V.VARIANT_ID, variant_id, 'track variant_id')
    _in(readout, V.TRACK_READOUTS, 'track readout')
    _in(mode, V.TRACK_MODES, 'track mode')
    return f'{game_id}:{method_id}:{variant_id}:{readout}:{mode}'


def validate_score_record(s: object) -> dict:
    """Validate synthetic values only. There is no data path: nothing here reads an outcome."""
    where = 'score record'
    _schema(s, V.SCORE, where)
    game = s.get('game_id') if type(s) is dict else None
    p, barrels = profile_and_barrels(game)
    _keys(s, _SCORE_FIELDS_PB if game == 'POWERBALL' else _SCORE_FIELDS_OZ, where)
    check_json_value(s, where)
    _int(s['draw_number'], f'{where}.draw_number', low=p.first_draw)
    parts = s['track_id'].split(':') if type(s['track_id']) is str else []
    if len(parts) != 5 or track_id(*parts) != s['track_id'] or parts[0] != game:
        raise ValueError(f'{where}: invalid track_id')
    if s['mode'] != parts[4]:
        raise ValueError(f'{where}: mode must match the track')
    _match(V.REVISION, s['method_revision'], f'{where}.method_revision')
    _match(V.SHA256, s['forecast_content_digest'], f'{where}.forecast_content_digest')
    _match(V.SHA256, s['freeze_receipt_digest'], f'{where}.freeze_receipt_digest')
    main = barrels['MAIN']
    dm = s['drawn_main']
    if (type(dm) is not list or len(dm) != 7 or dm != sorted(set(dm)) or
            any(type(x) is not int or not main.low <= x <= main.high for x in dm)):
        raise ValueError(f'{where}: drawn_main must be 7 distinct labels, ascending')
    mm = _int(s['main_matches'], f'{where}.main_matches', 0, 7)
    if game == 'POWERBALL':
        pb = barrels['POWERBALL']
        _int(s['drawn_powerball'], f'{where}.drawn_powerball', pb.low, pb.high)
        _int(s['powerball_match'], f'{where}.powerball_match', 0, 1)
        _int(s['division'], f'{where}.division', 0, 9)
    else:
        _int(s['supplementary_matches'], f'{where}.supplementary_matches', 0, min(3, 7 - mm))
        _int(s['division'], f'{where}.division', 0, 7)
    _text(s['evaluator_version'], f'{where}.evaluator_version')
    return s


def score_record_key(s: Mapping) -> tuple:
    """E2R-R45A create-only key: one record scores one specific frozen forecast."""
    validate_score_record(s)
    return (s['track_id'], s['draw_number'], s['method_revision'], s['forecast_content_digest'],
            s['freeze_receipt_digest'], s['evaluator_version'])
