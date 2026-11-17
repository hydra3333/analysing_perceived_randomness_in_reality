"""MHUP-B: the scoring half of the weekly session (design v0.1r7 sections 6.3, 6.5, 6.6, Appendices E to G; code plan
v0.3 section 5, L3). Launched only through Method_Weekly_Score.py under Run_Evaluation.bat.

  score             one target: the cross-session check of every record its freeze line names; then the release rule;
                    then the outcome, read once; then one score line per named record that has none.
  witness, verify   the witness ledger's two kinds of line (6.5, Appendix G). No network is used.
  diagnostic_score  the owner's re-test route (3.4, Q11): prints one diagnostic record's per-target quantities and
                    writes nothing to any ledger.

A score binds to the freeze line and its records, which keep their own session binding and training pin; the scoring
session and the outcome pin are recorded as the score's provenance. The scientific identity (game, method, revision,
variant, target, the scored record's digest, the scoring policy id) is the duplicate guard: a second routine score for
it refuses, whatever the score run id. The per-target quantities are WF-1B's, through its own functions, unchanged.
This program runs no method and makes no forecast.
"""
from __future__ import annotations

from pathlib import Path
import uuid

import _common.contract_publication as CP
import _common.contract_runner as CR
import _common.master_versions as MV
import _common.owner_records as OR
import _common.jsonl_ledger as JL
import _common.score_identities as SI
import _common.weekly_records as WR
from _common.contract_records import record_digest
from _common.game_profiles import get_profile

from . import collect as COL
from . import divisions as DV
from . import measures as MS
from . import outcome_reader as RD
from .report import frac

SCORER_VERSION = 'MHUPB_WEEKLY_SCORE_V1'


class ScoreRefused(Exception):
    """Refused before this command wrote anything."""


class ScoreStopped(Exception):
    """Stopped part-way: the lines already appended stand; rerunning scores the unscored records only."""


def _root() -> Path:
    return Path(CR.PROJECT_ROOT)


def _guard(fn, *args, **kw):
    try:
        return fn(*args, **kw)
    except OR.RecordRefused as exc:
        raise ScoreRefused(str(exc)) from None


def _marker_check() -> None:
    m = Path(CR.ORPHAN_MARKER)
    if m.exists() or m.is_symlink():
        raise ScoreRefused('UNRESOLVED_ORPHAN_MARKER: no experiment, record or score is permitted')


def _ledger_rows(game_id: str):
    try:
        _raw, rows, _evidence = MV.load_verified_source(_root(), game_id)
    except MV.LedgerRefused as exc:
        raise ScoreRefused(f'the master ledger does not pass the version-2 rules: {exc}') from None
    return rows


def _active_session(game_id: str, session_id: str) -> dict:
    lock = OR.session_lock_path(_root(), game_id)
    if lock.is_symlink() or not lock.is_file():
        raise ScoreRefused('no session lock: scoring runs inside the game\'s active session')
    named = lock.read_bytes().decode('ascii', errors='replace').split(' ', 1)[0].strip()
    if named != session_id:
        raise ScoreRefused(f'session {session_id} is not the game\'s active session')
    return _guard(WR.session, _root(), game_id, session_id)


def quantities(game_id: str, forecast: dict, drawn_main, extra) -> tuple[dict, dict | None]:
    """(readouts, rank) of one forecast against one opened draw: WF-1B's per-target quantities (report.score_cells),
    through the same functions. A readout the forecast does not give is recorded as unavailable with its reason."""
    readouts = {}
    for ro in COL.READOUTS:
        entry, why = COL._entry(forecast, ro, game_id)
        if entry is None:
            readouts[ro] = {'unavailable': why}
        else:
            readouts[ro] = DV.match_record(game_id, entry[0], entry[1], drawn_main, extra)   # supplementaries end here
    barrels = forecast.get('barrels', {})
    groups = {b: barrels[b].get('ranked_groups') for b in barrels}
    rank = None
    if groups.get('MAIN') is not None and (game_id != 'POWERBALL' or groups.get('POWERBALL') is not None):
        fields = MS.mr5_target_fields(
            game_id, MS.mid_ranks_from_groups(groups['MAIN'], DV.MAIN_POOL[game_id]), drawn_main,
            *((MS.mid_ranks_from_groups(groups['POWERBALL'], DV.PB_POOL), extra) if game_id == 'POWERBALL' else ()))
        rank = {k: frac(v) for k, v in fields.items()}
    return readouts, rank


def score(game_id: str, session_id: str, target: int, *, echo=print) -> dict:
    """Score every record the target's freeze line names that has no routine score line. Returns the counts."""
    _marker_check()
    root, p = _root(), get_profile(game_id)
    scoring = _active_session(game_id, session_id)
    lines = _guard(WR.forecast_ledger, root, game_id)
    line = WR.freeze_line_for(lines, target) if type(target) is int else None
    if line is None:
        raise ScoreRefused(f'target {target!r} has no freeze line: no freeze line, no score')
    rows = _ledger_rows(game_id)
    try:
        outcome_row = MV.resolve_pin(rows, scoring['ledger_version'], scoring['master_sha256'])
    except MV.LedgerRefused as exc:
        raise ScoreRefused(f'the scoring session\'s pin is not a row of the ledger: {exc}') from None
    if target > outcome_row.last_draw:
        raise ScoreRefused(f'target {target} has no accepted result in the scoring session\'s master version '
                           f'(its last draw is {outcome_row.last_draw})')
    evidence = _guard(WR.verify_named_records, root, game_id, line)        # the cross-session check, every record
    for ev in evidence:
        r = ev['named']
        try:
            trained = MV.resolve_pin(rows, r['ledger_version'], r['master_sha256'])
        except MV.LedgerRefused as exc:
            raise ScoreRefused(f'a named record\'s training pin is not a row of the ledger: {exc}') from None
        if trained.version > outcome_row.version or trained.last_draw >= target:
            raise ScoreRefused('a named record\'s training pin is not a prefix of the scoring version that ends before '
                               'the target')
    identities = _guard(SI.scored_identities, root, game_id)
    _guard(SI.closed_targets, game_id, lines, identities)                  # a foreign routine identity refuses here
    todo = {SI.routine_identity(game_id, target, ev['named']): ev for ev in evidence
            if SI.routine_identity(game_id, target, ev['named']) not in identities}
    if not todo:
        echo(f'[WEEKLY-SCORE] target {target}: every named record is already scored; nothing written')
        return {'target': target, 'scored': 0, 'already': len(evidence)}
    if not RD.outcome_release_allowed(root, game_id, target):
        raise ScoreRefused(f'target {target} is not released by the freeze-before-outcome rule (design 5.3, 6.3)')
    try:
        drawn_main, extra, date_text = RD.read_outcome_rows(
            repo_root=root, game_id=game_id, master_sha256=scoring['master_sha256'], targets=[target],
            ledger_version=scoring['ledger_version'])[target]              # the outcome, read once
    except RD.OutcomeRefused as exc:
        raise ScoreRefused(f'the outcome was not released: {exc}') from None
    score_run_id = 'ws-' + uuid.uuid4().hex
    path = WR.score_ledger_path(root, game_id)
    written = 0
    for ident, ev in todo.items():
        r, forecast = ev['named'], ev['forecast']
        readouts, rank = (None, None) if forecast is None else quantities(game_id, forecast, drawn_main, extra)
        s = {'schema': WR.SCORE_LINE_SCHEMA, 'game_id': game_id, 'method_id': r['method_id'],
             'method_revision': r['method_revision'], 'variant_id': r['variant_id'], 'target_draw_number': target,
             'scored_record_digest': r['scored_record_digest'], 'scoring_policy_id': WR.ROUTINE_POLICY,
             'amendment_of': None, 'score_run_id': score_run_id, 'scorer_version': SCORER_VERSION,
             'scoring_session_id': session_id, 'outcome_ledger_version': scoring['ledger_version'],
             'outcome_master_sha256': scoring['master_sha256'], 'scored_utc': CP.utc_now(),
             'freeze_line_digest': record_digest(line), 'freeze_line_number': line['line_number'],
             'record_kind': r['record_kind'], 'run_id': r['run_id'], 'run_mode': r['run_mode'], 'tier': r['tier'],
             'frozen_at_utc': r['frozen_at_utc'], 'effective_class': r['effective_class'],
             'missing_batch': r['missing_batch'], 'training_ledger_version': r['ledger_version'],
             'training_master_sha256': r['master_sha256'], 'freeze_receipt_digest': r['freeze_receipt_digest'],
             'readouts': readouts, 'rank': rank, 'drawn_main': list(drawn_main),
             'drawn_powerball': extra if game_id == 'POWERBALL' else None,
             'exposure_flag': OR.exposure_flag(game_id, target),
             'draw_date_is_derived': date_text == p.derived_date(target).isoformat()}
        try:
            WR.validate_score_line(s)
            if SI.identity_of(s) != ident:
                raise OR.RecordRefused('the line\'s scientific identity is not the record\'s')
        except OR.RecordRefused as exc:
            raise ScoreStopped(f'target {target}: a score line would be invalid ({exc}); {written} line(s) were '
                               f'appended before it') from None
        JL.append(path, s)
        written += 1
    echo(f'[WEEKLY-SCORE] target {target}: {written} record(s) scored (score run {score_run_id}; scoring session '
         f'{session_id}; outcome version {scoring["ledger_version"]})')
    return {'target': target, 'scored': written, 'already': len(evidence) - written}


# ---------------------------------------------------------------- the witness ledger (design 6.5, Appendix G)

def witness(game_id: str, target: int, kind: str, ref: str) -> dict:
    """WITNESS_RECORDED: the owner's claim that the freeze line's digest was pushed or emailed. Not proof."""
    root = _root()
    line = WR.freeze_line_for(_guard(WR.forecast_ledger, root, game_id), target) if type(target) is int else None
    if line is None:
        raise ScoreRefused(f'target {target!r} has no freeze line: there is no digest to witness')
    if kind not in WR.WITNESS_KINDS:
        raise ScoreRefused(f'the witness kind is one of {", ".join(WR.WITNESS_KINDS)}')
    if type(ref) is not str or not ref.strip() or not ref.isascii() or not ref.isprintable():
        raise ScoreRefused('the reference (a commit id or a message id) is empty or not printable ASCII')
    _guard(WR.witness_ledger, root, game_id)
    w = {'schema': WR.WITNESS_SCHEMA, 'kind': 'WITNESS_RECORDED', 'game_id': game_id, 'target_draw_number': target,
         'freeze_line_digest': record_digest(line), 'witness_kind': kind, 'ref': ref.strip(),
         'recorded_utc': CP.utc_now()}
    JL.append(WR.witness_ledger_path(root, game_id), w)
    return w


def verify(game_id: str, target: int, verified_by: str, received_utc: str, evidence: str) -> dict:
    """WITNESS_VERIFIED: the person who checked the reference records the service's own receipt. The tool checks what a
    tool can: a role (never a name), a UTC instant, an evidence text that contains the recorded reference. That the
    referenced commit or message carries the freeze line's digest is the verifier's human check."""
    root = _root()
    line = WR.freeze_line_for(_guard(WR.forecast_ledger, root, game_id), target) if type(target) is int else None
    if line is None:
        raise ScoreRefused(f'target {target!r} has no freeze line')
    digest = record_digest(line)
    recorded = [w for w in _guard(WR.witness_ledger, root, game_id)
                if w['kind'] == 'WITNESS_RECORDED' and w['target_draw_number'] == target and
                w['freeze_line_digest'] == digest]
    if not recorded:
        raise ScoreRefused('no WITNESS_RECORDED line for this target\'s freeze line: record the witness first')
    if verified_by not in WR.VERIFIER_ROLES:
        raise ScoreRefused(f'verified-by is a role, one of {", ".join(WR.VERIFIER_ROLES)} (never a name)')
    _guard(WR.parse_utc, received_utc, 'received-utc')
    if type(evidence) is not str or not evidence.strip() or not evidence.isascii():
        raise ScoreRefused('the evidence text (the service\'s own receipt, quoted) is empty or not ASCII')
    ref = recorded[-1]['ref']
    if ref not in evidence:
        raise ScoreRefused('the evidence text does not contain the recorded reference')
    w = {'schema': WR.WITNESS_SCHEMA, 'kind': 'WITNESS_VERIFIED', 'game_id': game_id, 'target_draw_number': target,
         'freeze_line_digest': digest, 'witness_kind': recorded[-1]['witness_kind'], 'ref': ref,
         'verified_by': verified_by, 'received_utc': received_utc, 'evidence': evidence,
         'digest_binding': 'human-checked', 'recorded_utc': CP.utc_now()}
    JL.append(WR.witness_ledger_path(root, game_id), w)
    return w


# ---------------------------------------------------------------- diagnostic-score (design 3.4, Q11)

def diagnostic_score(game_id: str, run_id: str) -> dict:
    """The per-target quantities of one diagnostic record against an accepted outcome, for the console only. It writes
    nothing. The outcome is served only under the reader's own rules: a draw of the development prefix, or a draw the
    freeze-before-outcome rule has released."""
    root, p = _root(), get_profile(game_id)
    if type(run_id) is not str or not CP.V.RUN_ID.fullmatch(run_id):
        raise ScoreRefused('invalid run id')
    base = OR.diagnostic_runs_root(root) / game_id
    folders = sorted(f for f in base.glob(f'*/*/{run_id}') if f.is_dir() and not f.is_symlink()) if base.is_dir() else []
    if len(folders) != 1:
        raise ScoreRefused('no diagnostic record with this run id (only records under the diagnostic root are served)')
    ok, why = CP.read_run(folders[0]).get('forecast', (False, 'NO_FORECAST'))
    if not ok:
        raise ScoreRefused(f'the diagnostic record is not consumable: {why}')
    forecast = COL._load(folders[0] / CP.FILES['forecast'])
    receipt = COL._load(folders[0] / CP.FILES['forecast_receipt'])
    if forecast is None or receipt is None or forecast.get('run_mode') != 'REAL_DEVELOPMENT':
        raise ScoreRefused('the diagnostic record is not a canonical REAL_DEVELOPMENT forecast')
    target = forecast['target_draw_number']
    rows = _ledger_rows(game_id)
    if target > rows[-1].last_draw:
        raise ScoreRefused(f'draw {target} has no accepted result')
    if target >= p.holdout_first and not RD.outcome_release_allowed(root, game_id, target):
        raise ScoreRefused(f'draw {target} is not released by the freeze-before-outcome rule; nothing is shown')
    try:
        drawn_main, extra = RD.read_outcomes(repo_root=root, game_id=game_id, master_sha256=rows[-1].master_sha256,
                                             targets=[target], ledger_version=rows[-1].version)[target]
    except RD.OutcomeRefused as exc:
        raise ScoreRefused(f'the outcome was not released: {exc}') from None
    readouts, rank = quantities(game_id, forecast, drawn_main, extra)
    return {'game_id': game_id, 'run_id': run_id, 'method_id': forecast['method_id'],
            'variant_id': forecast['variant_id'], 'method_revision': forecast['method_revision'],
            'target_draw_number': target, 'readouts': readouts, 'rank': rank, 'unofficial': True}
