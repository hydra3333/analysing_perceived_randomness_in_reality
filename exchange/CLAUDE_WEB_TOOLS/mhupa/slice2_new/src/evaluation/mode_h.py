"""MHUP-A: the Mode H study's owner commands and its one score (design v0.1r5 sections 4.1, 4.2, 5.2-5.4, 6.7).

Evaluator side (it may import the outcome reader; no method code). Everything here reads value-free records,
the frozen forecasts and, in exactly one place and only under the freeze-before-outcome rule, the outcomes of the
ten holdout draws. Every record it writes is create-only.

- `manifest(game)`: the study manifest (4.1, Appendix H): cohort (exactly the validated released set, 4.3), targets, exposure flags, measures, families,
  the N1 policy, the evaluator's version, v_f, the closure and environment inventories; one MODE_H_STUDY_MANIFEST
  search-log row.
- `open_holdout(game, statement)`: the opening record (4.2), after the manifest exists with the digest it names;
  freeze_version and freeze_master_sha256 are the ledger's current last row, which must be the manifest's v_f.
- `advance(game, statement)`: the study version advance (4.1), naming exactly the ledger rows beyond v_a.
- `declare_developed(game, statement)`: the GOAL-1 record (6.7), after the seal.
- `score(game, ...)`: the one score attempt (5.2-5.4): BATCH_COMPLETE required; the exact roster verified
  (every planned pair with its DONE ticket); SCORING_STARTED (the attempt id and the roster digest) BEFORE the
  first outcome read; the search-log row and the scoring plan before it too; the outcomes of the ten draws read
  once through the outcome reader under `outcome_release_allowed`; the Mode H score ledger (create-only, one
  line per scored pair and readout, plus the MR5 rank lines); SCORE_COMPLETE; the report from the accepted lines
  (no outcome re-read); MODE_H_SEALED. Rerunning resumes the same attempt: SCORING_STARTED fixes the attempt id;
  an existing ledger is accepted only if it is exactly the lines this scorer writes for the frozen forecasts
  and the drawn numbers it records (EX_148 B04); after SCORE_COMPLETE no outcome is read; each of the three
  report files, where it exists, must equal the bytes rebuilt from the lines, and a missing one is created
  (EX_148 B02). A second routine attempt after SCORE_COMPLETE is refused.
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path

import _common.contract_publication as CP
import _common.contract_vocab as V
import _common.contract_runner as CR
import _common.walk_forward as WF
import _common.closure as CL
import _common.master_versions as MV
import _common.owner_records as OR
import _common.release_records as RR
from _common.contract_records import canonical, record_digest, sha256_hex
from _common.contract_receipts import validate_score_record
from _common.game_profiles import get_profile

from . import collect as COL
from . import divisions as DV
from . import report as RP
from . import report_writer as RW
from . import seed_policies as SP

TOOL = 'Method_Mode_H.py'
MODE_H_VERSION = 'MHUPA_MODE_H_V1'
ATTEMPT = 'mh-'
SCORE_LEDGER = 'mode_h_score_ledger.jsonl'


class ModeHRefused(Exception):
    """Refused before anything was written (or, during a score, before any further write)."""


def _root() -> Path:
    return Path(CR.PROJECT_ROOT)


def _refuse_if_marker() -> None:
    m = Path(CR.ORPHAN_MARKER)
    if m.exists() or m.is_symlink():
        raise ModeHRefused('UNRESOLVED_ORPHAN_MARKER: no experiment, record or score is permitted')


def _verified_rows(game_id: str):
    try:
        _raw, rows, _ev = MV.load_verified_source(_root(), game_id)
    except MV.LedgerRefused as exc:
        raise ModeHRefused(f'the master ledger does not pass the version-2 rules: {exc}') from None
    return rows


def _statement(given: str, expected: str) -> str:
    if type(given) is not str or given.strip() != expected:
        raise ModeHRefused('the owner statement must be typed exactly as the design fixes it:\n  ' + expected)
    return expected


# ---------------------------------------------------------------- the study manifest (4.1)

def manifest(game_id: str, *, env: CL.Environment | None = None) -> dict:
    """Write the study manifest, create-only, and its search-log row. Refuses if one exists, if the holdout is already
    opened, if the ledger does not pass, or if the closure or environment refuses (a sourceless .pyc, an orphan)."""
    _refuse_if_marker()
    p = get_profile(game_id)
    root = _root()
    path = OR.study_manifest_path(root, game_id)
    if not OR.absent(path):
        raise ModeHRefused('the study manifest already exists (create-only; re-planning is not provided)')
    try:
        if OR.opening_record(root, game_id) is not None:
            raise ModeHRefused('the holdout is already opened; the manifest is written before the opening record')
    except OR.RecordRefused as exc:
        raise ModeHRefused(f'opening record refused: {exc}') from None
    rows = _verified_rows(game_id)
    v_f = rows[-1]
    if v_f.last_draw != p.holdout_first - 1:
        raise ModeHRefused(f'the ledger\'s last row ends at draw {v_f.last_draw}; before the holdout is opened it must end '
                           f'at {p.holdout_first - 1}')
    try:
        members, excluded = WF.cohort(game_id, None)       # every released variant; the runner's adapters are checked
    except WF.BatchRefused as exc:                        # by the plan (methods side; the import firewall holds here)
        raise ModeHRefused(f'cohort: {exc}') from None
    if not members:
        raise ModeHRefused('the cohort is empty')
    _check_release_authority(root, game_id, members, excluded)        # EX_148 B03: only released variants are frozen
    not_runnable = list(excluded) + _not_runnable(game_id)
    families = RP.load_families(game_id, p.holdout_first, p.holdout_last)
    if not families:
        raise ModeHRefused('no Mode H family is registered for this game\'s holdout window (design 5.4)')
    policy = SP.approved_policy()
    if policy is None:
        raise ModeHRefused('no approved N1 seed policy is installed (design 5.4 reuses the approved root)')
    try:
        frozen = CL.freeze(root, env)
    except CL.ClosureRefused as exc:
        raise ModeHRefused(f'the closure or the environment refuses: {exc}') from None
    rec = {'schema': OR.STUDY_MANIFEST_SCHEMA, 'game_id': game_id, 'frozen_utc': CP.utc_now(), 'cohort': members,
           'not_runnable': not_runnable, 'targets': list(range(p.holdout_first, p.holdout_last + 1)),
           'exposure': {str(t): f for t in range(p.holdout_first, p.holdout_last + 1)
                        if (f := OR.exposure_flag(game_id, t)) is not None},
           'measures': RP.STAGE2, 'families': [f['family_id'] for f in families], 'n1_policy_id': policy['policy_id'],
           'evaluator_version': RP.EVALUATOR_VERSION, 'freeze_version': v_f.version,
           'freeze_master_sha256': v_f.master_sha256,
           'admission_rule': ('exactly one UPDATE row follows the frozen version before the batch, the admitted version '
                              'v_a = v_f + 1, and it brings in every holdout draw (design 4.1 admission (3)); any '
                              'row beyond v_a before the seal needs a study version advance'),
           'closure': frozen['closure'], 'environment': frozen['environment'], 'excluded': frozen['excluded'],
           'not_frozen': frozen['not_frozen'], 'tool': TOOL, 'tool_version': MODE_H_VERSION}
    OR.validate_study_manifest(rec, game_id)
    raw = OR.write_record(path, rec)
    WF._append_search_row({'row_type': 'MODE_H_STUDY_MANIFEST', 'utc': rec['frozen_utc'], 'game_id': game_id,
                           'mode': 'WF', 'window_first': p.holdout_first, 'window_last': p.holdout_last,
                           'cohort_size': len(members), 'cohort_digest': OR.manifest_cohort_digest(rec),
                           'family_ids': ';'.join(rec['families']), 'measures': RP.STAGE2,
                           'plan_digest': sha256_hex(raw), 'tool': TOOL, 'tool_version': MODE_H_VERSION,
                           'tool_sha256': RP.tool_sha256()})
    return rec


def _check_release_authority(root: Path, game_id: str, members, excluded) -> None:
    """The cohort the manifest freezes must be exactly the game's released, unretired set (design 4.3: an installed but
    unreleased revision qualifies for nothing; EX_148 B03). Both sides are computed independently: the members from
    the installed registry (active SUPPORTED, no development flag), the released set from the validated release records
    and the registry chains (release_records.released_variants). Any difference, or any refusal of the records, refuses."""
    try:
        released = {k for k in RR.released_variants(root) if k[0] == game_id}
    except (RR.Refused, ValueError, KeyError) as exc:
        raise ModeHRefused(f'the release records refuse: {exc}') from None
    cohort = {(game_id, m['method_id'], m['method_revision'], m['variant_id']) for m in members}
    excluded_mv = {(e['method_id'], e['variant_id']) for e in excluded}
    unreleased = sorted(cohort - released)
    missing = sorted(k for k in released - cohort if (k[1], k[3]) not in excluded_mv)
    if unreleased or missing:
        fmt = lambda ks: ', '.join(f'{m} revision {r} {v}' for _g, m, r, v in ks[:4]) + (f' (+{len(ks) - 4})' if len(ks) > 4 else '')
        raise ModeHRefused('the cohort is not the released set: ' + '; '.join(
            ([f'SUPPORTED in the registry but not released: {fmt(unreleased)}'] if unreleased else []) +
            ([f'released but not in the registry\'s runnable set: {fmt(missing)}'] if missing else [])))


def _not_runnable(game_id: str) -> list[dict]:
    """Every registered method of the game that is not released, by name and status (mark, never suppress)."""
    reg = WF._registry()
    out = []
    for (g, m, v) in sorted(reg.chain_keys(), key=lambda k: (int(k[1][2:]), k[2])):
        if g != game_id:
            continue
        e = reg.active_entry(g, m, v)
        if e['registry_status'] != 'SUPPORTED':
            out.append({'method_id': m, 'variant_id': v, 'reason': e['registry_status']})
    return out


# ---------------------------------------------------------------- the opening record (4.2)

def open_holdout(game_id: str, statement: str) -> dict:
    _refuse_if_marker()
    root = _root()
    path = OR.opening_record_path(root, game_id)
    if not OR.absent(path):
        raise ModeHRefused('the opening record already exists (create-only; it is permanent)')
    man = OR.study_manifest(root, game_id)
    if man is None:
        raise ModeHRefused('no study manifest: write it first (Method_Mode_H.py manifest)')
    rows = _verified_rows(game_id)
    if (rows[-1].version, rows[-1].master_sha256) != (man['freeze_version'], man['freeze_master_sha256']):
        raise ModeHRefused('the ledger\'s last row is not the version the study manifest froze; the opening record is '
                           'written before any update')
    rec = {'schema': OR.OPENING_SCHEMA, 'game': game_id,
           'study_manifest_sha256': OR.file_sha256(OR.study_manifest_path(root, game_id)),
           'opened_utc': CP.utc_now(), 'owner_statement': _statement(statement, OR.OPENING_STATEMENT),
           'freeze_version': rows[-1].version, 'freeze_master_sha256': rows[-1].master_sha256}
    OR.validate_opening_record(rec, game_id)
    OR.write_record(path, rec)
    WF._append_search_row({'row_type': 'HOLDOUT_OPENED', 'utc': rec['opened_utc'], 'game_id': game_id, 'mode': 'WF',
                           'plan_digest': rec['study_manifest_sha256'], 'tool': TOOL, 'tool_version': MODE_H_VERSION,
                           'tool_sha256': RP.tool_sha256()})
    return rec


# ---------------------------------------------------------------- the study version advance (4.1)

def advance(game_id: str, statement: str) -> dict:
    _refuse_if_marker()
    root = _root()
    path = OR.advance_record_path(root, game_id)
    if not OR.absent(path):
        raise ModeHRefused('a study version advance already exists for this game (create-only)')
    try:
        opening = OR.opening_record(root, game_id)
        if opening is None:
            raise ModeHRefused('the holdout is not opened')
        if OR.mode_h_sealed(root, game_id):
            raise ModeHRefused('the Mode H study is sealed; the updater is free and no advance applies')
    except OR.RecordRefused as exc:
        raise ModeHRefused(f'owner record refused: {exc}') from None
    rows = _verified_rows(game_id)
    v_a = opening['freeze_version'] + 1
    beyond = [r for r in rows if r.version > v_a]
    if not beyond:
        raise ModeHRefused(f'the ledger holds no row beyond the admitted version {v_a}; nothing to advance')
    rec = {'schema': OR.ADVANCE_SCHEMA, 'game_id': game_id, 'study_manifest_sha256': opening['study_manifest_sha256'],
           'admitted_version_before': v_a, 'admitted_version_after': beyond[-1].version,
           'rows_beyond_admitted': [{'version': r.version, 'action': r.action, 'master_sha256': r.master_sha256,
                                     'last_draw': r.last_draw} for r in beyond],
           'owner_statement': _statement(statement, OR.ADVANCE_STATEMENT), 'advanced_utc': CP.utc_now(),
           'tool': TOOL, 'tool_version': MODE_H_VERSION}
    OR.validate_advance_record(rec, game_id)
    OR.write_record(path, rec)
    WF._append_search_row({'row_type': 'STUDY_VERSION_ADVANCE', 'utc': rec['advanced_utc'], 'game_id': game_id,
                           'mode': 'WF', 'plan_digest': sha256_hex(canonical(rec)), 'tool': TOOL,
                           'tool_version': MODE_H_VERSION, 'tool_sha256': RP.tool_sha256()})
    return rec


# ---------------------------------------------------------------- the developed record (6.7)

def declare_developed(game_id: str, statement: str) -> dict:
    _refuse_if_marker()
    root = _root()
    path = OR.developed_record_path(root, game_id)
    if not OR.absent(path):
        raise ModeHRefused('the developed record already exists (create-only)')
    try:
        rec_id = OR.batch_id_record(root, game_id)
        if rec_id is None or not OR.mode_h_sealed(root, game_id):
            raise ModeHRefused('the Mode H study is not sealed: GOAL-1 follows the sealed score (design 6.7)')
        seal = OR.marker(root, game_id, rec_id['batch_id'], 'MODE_H_SEALED')
    except OR.RecordRefused as exc:
        raise ModeHRefused(f'owner record refused: {exc}') from None
    rec = {'schema': OR.DEVELOPED_SCHEMA, 'game': game_id, 'declared_utc': CP.utc_now(),
           'owner_statement': _statement(statement, OR.DEVELOPED_STATEMENT),
           'mode_h_score_digest': seal['score_ledger_sha256'], 'mode_h_batch_id': rec_id['batch_id'],
           'mode_h_score_attempt_id': seal['attempt_id']}
    OR.validate_developed_record(rec, game_id)
    OR.write_record(path, rec)
    WF._append_search_row({'row_type': 'DEVELOPED', 'utc': rec['declared_utc'], 'game_id': game_id, 'mode': 'WF',
                           'batch_id': rec_id['batch_id'], 'attempt_id': seal['attempt_id'],
                           'plan_digest': seal['score_ledger_sha256'], 'tool': TOOL, 'tool_version': MODE_H_VERSION,
                           'tool_sha256': RP.tool_sha256()})
    return rec


# ---------------------------------------------------------------- the one score (5.2-5.4)

def _ledger_lines(path: Path) -> tuple[list, list]:
    rows, torn = OR.read_jsonl(path)
    if torn:
        raise ModeHRefused('the Mode H score ledger has an unterminated last line; the ledger is written in one '
                           'create-only step, so this file is not the scorer\'s')
    scores = [r for r in rows if r.get('schema') == V.SCORE]
    ranks = [r for r in rows if r.get('schema') == RP.RANK_SCHEMA]
    if len(scores) + len(ranks) != len(rows):
        raise ModeHRefused('the Mode H score ledger holds a line of another schema')
    for r in scores:
        try:
            validate_score_record(r)
        except ValueError as exc:
            raise ModeHRefused(f'the Mode H score ledger holds an invalid score record: {exc}') from None
    return scores, ranks


def _verify_ledger(game_id: str, members, collected: dict, raw: bytes, scores: list, ranks: list) -> None:
    """EX_148 B04: before SCORE_COMPLETE (and again before the report), the ledger must be exactly the lines this
    scorer writes for the frozen forecasts, given the drawn numbers the ledger itself records; it never reads an
    outcome. Every drawn number of a draw must agree across its lines; the expected score and rank identities
    (track or variant, draw, revision, forecast and receipt digests, evaluator version: every valid cell of the
    frozen roster, from the collected forecasts) must appear exactly once each, nothing missing, duplicated or
    foreign; and every line is rebuilt with report.score_cells from those drawn numbers and must be byte-identical,
    in the same order. For Oz Lotto the supplementaries are never stored (R2 2.5), so each score line's
    supplementary_matches is taken from the line and checked for range and against its division; every other field
    is rebuilt."""
    drawn = {}
    for r in scores:
        t = r.get('draw_number')
        d = (tuple(r.get('drawn_main') or ()), r.get('drawn_powerball'))
        if drawn.setdefault(t, d) != d:
            raise ModeHRefused(f'the score ledger records two different drawn results for draw {t}')
    key_s = lambda r: (r['track_id'], r['draw_number'], r['method_revision'], r['forecast_content_digest'],
                       r['freeze_receipt_digest'], r['evaluator_version'])
    key_r = lambda r: (r['method_id'], r['variant_id'], r['draw_number'], r['method_revision'],
                       r['forecast_content_digest'], r['freeze_receipt_digest'], r['evaluator_version'])
    expected_targets = sorted({k[2] for k, c in collected['cells'].items() if c['valid']})
    if sorted(drawn) != expected_targets:
        raise ModeHRefused('the score ledger does not cover exactly the targets of the frozen valid forecasts')
    if game_id == 'POWERBALL':
        outcomes = {t: (list(d[0]), d[1]) for t, d in drawn.items()}
    else:                                          # placeholder supplementaries; their match counts are checked below
        outcomes = {t: (list(d[0]), [x for x in range(1, 48) if x not in d[0]][:3]) for t, d in drawn.items()}
    try:
        exp_scores, exp_ranks, _pt, _pv = RP.score_cells(game_id, members, collected, outcomes,
                                                         exposure=lambda t: OR.exposure_flag(game_id, t))
    except (ValueError, KeyError, TypeError) as exc:
        raise ModeHRefused(f'the score ledger\'s drawn numbers are not a valid draw: {exc}') from None
    if sorted(map(key_s, scores)) != sorted(map(key_s, exp_scores)) or len(scores) != len(exp_scores):
        raise ModeHRefused('the score ledger\'s score lines are not exactly the frozen roster\'s valid cells (a line '
                           'missing, duplicated or foreign)')
    if sorted(map(key_r, ranks)) != sorted(map(key_r, exp_ranks)) or len(ranks) != len(exp_ranks):
        raise ModeHRefused('the score ledger\'s rank lines are not exactly the frozen roster\'s ranked cells')
    if game_id != 'POWERBALL':
        for got, exp in zip(scores, exp_scores):
            s = got.get('supplementary_matches')
            m = exp['main_matches']
            if type(s) is not int or not 0 <= s <= min(3, 7 - m) or got.get('division') != DV.division(
                    game_id, m, supplementary_matches=s):
                raise ModeHRefused(f'draw {got.get("draw_number")}: supplementary_matches and division disagree')
            exp['supplementary_matches'], exp['division'] = s, got['division']
    if b''.join(canonical(r) for r in exp_scores + exp_ranks) != raw:
        raise ModeHRefused('the score ledger differs from the lines the scorer writes for the frozen forecasts and '
                           'the drawn numbers it records (a tampered or foreign line); nothing is completed')


def score(game_id: str, *, echo=None, n1_runner=None, seed_line: str, n1_policies_on_file: int, environment: dict) -> dict:
    """The one Mode H score attempt of a game, resumable (5.2). Returns what was written and the report paths."""

    def progress(text: str) -> None:
        if echo is not None:
            echo(f'{CP.utc_now()[11:19]} UTC  {text}')

    _refuse_if_marker()
    p = get_profile(game_id)
    root = _root()
    try:
        study = WF._study(game_id)
        WF._check_frozen(game_id, study)
        rec_id = OR.batch_id_record(root, game_id)
        if rec_id is None:
            raise ModeHRefused('no Mode H plan for this game')
        plan = WF.load_plan(game_id, rec_id['batch_id'])
    except (WF.BatchRefused, OR.RecordRefused) as exc:
        raise ModeHRefused(str(exc)) from None
    if WF.kind_of(plan) != 'MODE_H_BATCH':
        raise ModeHRefused('the game\'s batch is not a Mode H batch')
    batch_id = plan['batch_id']
    first, last = plan['window_first'], plan['window_last']
    present = OR.lifecycle_markers_present(root, game_id, batch_id)
    if 'MODE_H_SEALED' in present:
        raise ModeHRefused('the Mode H study is sealed; a corrective scoring run is a separately identified run under its '
                           'own policy id (design 5.4), not provided by this command')
    if 'BATCH_COMPLETE' not in present:
        raise ModeHRefused('the batch is not complete: no BATCH_COMPLETE marker (design 5.2)')
    families = RP.load_families(game_id, first, last)
    if [f['family_id'] for f in families] != study['manifest']['families']:
        raise ModeHRefused('the registered Mode H families differ from the study manifest\'s')
    # the exact roster: every planned pair DONE, by its ticket and by its run folder
    try:
        roster = OR.roster_digest(root, game_id, plan)
    except OR.RecordRefused as exc:
        raise ModeHRefused(f'the roster is not complete: {exc}') from None
    states, _bad = WF.pair_states(plan)
    not_done = [k for k, v in states.items() if v != 'DONE']
    if not_done:
        raise ModeHRefused(f'{len(not_done)} planned pair(s) have a DONE ticket but no run folder proving the run; the '
                           f'first: {not_done[0]}')
    progress(f'study and batch verified; roster of {len(states)} pairs, digest {roster[:12]}...')
    collected = COL.collect(plan, first, last)
    members = plan['cohort']
    tracks = [(mem, ro) for mem in members for ro in COL.READOUTS]
    grid_digest = sha256_hex(canonical({'grids': [[k[0], k[1], g] for k, g in sorted(collected['grids'].items())]}))
    selected = sorted([k[0], k[1], k[2], c['forecast_content_digest'], c['freeze_receipt_digest']]
                      for k, c in collected['cells'].items() if c['valid'])
    tests = RP.declared_tests(game_id, len(tracks), len(members))
    started = OR.marker(root, game_id, batch_id, 'SCORING_STARTED')
    if started is not None:
        if started['roster_digest'] != roster:
            raise ModeHRefused('the roster differs from the one this attempt started scoring (design 5.2); nothing re-scored')
        if started['plan_digest'] != record_digest(plan):
            raise ModeHRefused('SCORING_STARTED names another plan')
        attempt_id = started['attempt_id']
        folder = RP.roots('MODE_H_BATCH')['scores'] / game_id / batch_id / attempt_id
        sp_rec = json.loads((folder / 'scoring_plan.json').read_bytes().decode('ascii'))
        if canonical(sp_rec) != (folder / 'scoring_plan.json').read_bytes():
            raise ModeHRefused('the scoring plan record is not its canonical bytes')
        progress(f'resuming attempt {attempt_id}')
    else:
        attempt_id = ATTEMPT + uuid.uuid4().hex
        scoring_plan = {'schema': RP.SCORING_PLAN_SCHEMA, 'attempt_id': attempt_id, 'game_id': game_id, 'mode': 'WF',
                        'evidence_tier': RW.MODE_H_TIER, 'batch_id': batch_id, 'window_first': first, 'window_last': last,
                        'plan_digest': record_digest(plan), 'cohort_digest': plan['cohort_digest'],
                        'study_manifest_sha256': plan['study_manifest_sha256'], 'roster_digest': roster,
                        'grid_digest': grid_digest, 'family_ids': [f['family_id'] for f in families],
                        'measures': RP.STAGE2, 'declared_tests': tests, 'selected_forecasts': selected,
                        'evaluator_version': RP.EVALUATOR_VERSION,
                        'receipt_selection_policy': 'EARLIEST_FROZEN_AT_UTC_EQUAL_CONTENT_DIGESTS'}
        row = WF._append_search_row({'row_type': 'MODE_H_REPORT', 'utc': CP.utc_now(), 'game_id': game_id, 'mode': 'WF',
                                     'window_first': first, 'window_last': last, 'cohort_size': len(tracks),
                                     'cohort_digest': plan['cohort_digest'],
                                     'family_ids': ';'.join(f['family_id'] for f in families), 'test_count': tests,
                                     'measures': RP.STAGE2, 'batch_id': batch_id, 'attempt_id': attempt_id,
                                     'plan_digest': record_digest(scoring_plan), 'tool': TOOL,
                                     'tool_version': MODE_H_VERSION, 'tool_sha256': RP.tool_sha256()})
        sp_rec = dict(scoring_plan, search_log_row=row)
        folder = RP.roots('MODE_H_BATCH')['scores'] / game_id / batch_id / attempt_id
        folder.mkdir(parents=True, exist_ok=False)
        CP.create_only(folder / 'scoring_plan.json', canonical(sp_rec))
        OR.write_marker(root, game_id, batch_id, 'SCORING_STARTED',
                        {'schema': OR.MARKER_SCHEMAS['SCORING_STARTED'], 'batch_id': batch_id, 'game_id': game_id,
                         'attempt_id': attempt_id, 'roster_digest': roster, 'plan_digest': record_digest(plan),
                         'scoring_plan_digest': record_digest(sp_rec), 'utc': CP.utc_now()})
        progress(f'attempt {attempt_id}: search-log row {row}, scoring plan and SCORING_STARTED written')
    # the outcomes, read once, under the freeze-before-outcome rule
    ledger_path = folder / SCORE_LEDGER
    if OR.absent(ledger_path):
        if 'SCORE_COMPLETE' in present:
            raise ModeHRefused('SCORE_COMPLETE exists but the score ledger does not; nothing is re-read')
        version, sha = WF._admitted_pin(plan)
        targets = sorted({k[2] for k, c in collected['cells'].items() if c['valid']})
        from . import outcome_reader as OREAD
        outcomes = OREAD.read_outcomes(repo_root=root, game_id=game_id, master_sha256=sha, targets=targets,
                                       ledger_version=version) if targets else {}
        scores, ranks, _pt, _pv = RP.score_cells(game_id, members, collected, outcomes,
                                                 exposure=lambda t: OR.exposure_flag(game_id, t))
        CP.create_only(ledger_path, b''.join(canonical(r) for r in scores + ranks))
        progress(f'outcomes read once; score ledger written: {len(scores)} score lines, {len(ranks)} rank lines')
    scores, ranks = _ledger_lines(ledger_path)
    raw_ledger = ledger_path.read_bytes()
    _verify_ledger(game_id, members, collected, raw_ledger, scores, ranks)      # B04: before SCORE_COMPLETE
    ledger_sha = sha256_hex(raw_ledger)
    complete = OR.marker(root, game_id, batch_id, 'SCORE_COMPLETE')
    if complete is None:
        OR.write_marker(root, game_id, batch_id, 'SCORE_COMPLETE',
                        {'schema': OR.MARKER_SCHEMAS['SCORE_COMPLETE'], 'batch_id': batch_id, 'game_id': game_id,
                         'attempt_id': attempt_id, 'plan_digest': record_digest(plan), 'score_ledger_sha256': ledger_sha,
                         'lines': len(scores) + len(ranks), 'utc': CP.utc_now()})
    elif complete['score_ledger_sha256'] != ledger_sha or complete.get('attempt_id') != attempt_id:
        raise ModeHRefused('SCORE_COMPLETE does not name this ledger and attempt')
    # the report, from the accepted lines; no outcome read
    per_track, per_variant = RP.rebuild_from_ledgers(game_id, members, collected, scores, ranks)
    results, var_results, n1 = RP.measures_stage(game_id, per_track, per_variant, families, n1_runner, progress)
    res = {'plan': plan, 'families': families, 'collected': collected, 'per_track': per_track,
           'per_variant': per_variant, 'results': results, 'var_results': var_results, 'n1': n1,
           'attempt_id': attempt_id, 'search_log_row': sp_rec['search_log_row'], 'scoring_plan': sp_rec,
           'scoring_plan_digest': record_digest(sp_rec), 'scores_folder': folder, 'declared_tests': tests,
           'grid_digest': grid_digest, 'first': first, 'last': last, 'game_id': game_id, 'tier': RW.MODE_H_TIER,
           'exposure': {t: f for t in plan['targets'] if (f := OR.exposure_flag(game_id, t)) is not None},
           'advance': study['advance']}                       # the study version advance, disclosed by the report (4.1)
    contents = RW.build(res, generated_utc='', seed_line=seed_line, n1_policies_on_file=n1_policies_on_file,
                        environment=environment)
    base = RW.mode_h_base_name(res)
    report_folder = RP.roots()['reports'] / game_id
    paths = [report_folder / f'{base}.{ext}' for ext in ('txt', 'csv', 'json')]
    for p, ext in zip(paths, ('txt', 'csv', 'json')):          # EX_148 B02: every existing file verified first
        if not OR.absent(p) and (not p.is_file() or p.is_symlink() or p.read_bytes() != contents[ext]):
            raise ModeHRefused(f'the existing report {p.name} differs from the bytes rebuilt from the accepted lines; '
                               f'nothing is written')
    report_folder.mkdir(parents=True, exist_ok=True)
    made = []
    for p, ext in zip(paths, ('txt', 'csv', 'json')):          # then each missing file created, none overwritten
        if OR.absent(p):
            CP.create_only(p, contents[ext])
            made.append(ext)
    progress(f'report files: {", ".join(made) or "none"} written, {3 - len(made)} already present with these exact bytes')
    OR.write_marker(root, game_id, batch_id, 'MODE_H_SEALED',
                    {'schema': OR.MARKER_SCHEMAS['MODE_H_SEALED'], 'batch_id': batch_id, 'game_id': game_id,
                     'attempt_id': attempt_id, 'plan_digest': record_digest(plan), 'score_ledger_sha256': ledger_sha,
                     'report_sha256': sha256_hex(contents['txt']), 'report_manifest_sha256': sha256_hex(contents['json']),
                     'utc': CP.utc_now()})
    progress('MODE_H_SEALED written; the study is closed')
    return {'attempt_id': attempt_id, 'batch_id': batch_id, 'paths': paths, 'score_ledger_sha256': ledger_sha,
            'search_log_row': sp_rec['search_log_row'], 'scores': len(scores), 'ranks': len(ranks)}
