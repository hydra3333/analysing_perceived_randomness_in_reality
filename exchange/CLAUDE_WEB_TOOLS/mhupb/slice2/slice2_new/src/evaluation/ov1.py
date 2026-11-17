"""MHUP-B: OV-1, the one confirmatory test of the forward phase, one stream per game (design supplement v0.8 sections
6.1 to 6.8; code plan v0.3 section 5 L5 and section 6). Launched only through Method_OV1.py under Run_Evaluation.bat.

  register   the owner's registration of the test for a game, create-only, before its first eligible draw.
  record     the one writer of the game's OV-1 ledger; idempotent. Takes the targets from the first eligible one in
             draw order, each exactly once, and appends whatever is due: an eligibility line (before the cut-off), a
             factor line (once the eligible variants' score lines exist), a missed line (after the cut-off) or a stop.
  stop       the owner's recorded stop. A stopped stream stays stopped: no command registers again or recovers.
  status     what the ledger says. Reads only.
  verify     rebuilds every line from the eligibility lines, the forecast ledger, the run folders and the score ledger
             and compares bytes.

What each target becomes is fixed by what existed before its cut-off C(T), 01:30 UTC on its derived draw date:
  counted   a next-draw freeze line frozen before C(T), and an eligibility line durable before C(T). The whole factor
            table of the draw and its certificate are computed from the frozen tickets and sealed in that line before
            any outcome exists; the factor line only looks up the observed X. V = 0 is the registered skip (factor 1).
  missed    no such freeze line. Factor 1; recorded after C(T) from the forecast ledger, once it verifies and
            reconciles with every earlier record that names part of it. Labelled as recorded after the cut-off.
  stop      a pre-cut-off freeze line with no eligibility line at C(T); an owner stop; or a contradiction about a
            counted target. No factor line for that target or any later one, ever.
  blocked   an input is not there yet or does not verify. Nothing is written for the target or any later one; nothing
            is passed over; `record` resumes by itself when the input verifies. A failure is never a skip.

This module reads the frozen tickets, the forecast ledger, the score ledger, the witness ledger and the master's
version ledger (never a master's draws: X comes from the score lines, two ways). It runs no method and no forecast.
Every figure is a proved lower bound from ov1_numeric; nothing here uses a float.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import _common.contract_publication as CP
import _common.contract_runner as CR
import _common.jsonl_ledger as JL
import _common.master_versions as MV
import _common.owner_records as OR
import _common.score_identities as SI
import _common.walk_forward as WF
import _common.weekly_records as WR
from _common.contract_records import canonical, record_digest, sha256_hex
from _common.game_profiles import get_profile

from . import collect as COL
from . import ov1_numeric as NUM

TOOL = 'Method_OV1.py'
OV1_VERSION = 'MHUPB_OV1_V1'
REGISTRATION_SCHEMA = 'OV1_REGISTRATION_V1'
LINE_SCHEMA = 'OV1_LINE_V1'
KINDS = ('ELIGIBILITY', 'FACTOR', 'MISSED', 'STOP')
STOP_CAUSES = ('ELIGIBILITY_NOT_VERIFIED', 'OWNER_STOP', 'FACTOR_TABLE_MISMATCH', 'X_CONTRADICTION',
               'SCORE_LINE_CONTRADICTION', 'DRAW_DATE_NOT_DERIVED')
F01_TEXT = 'OV-1 eligibility NOT VERIFIED - PRIMARY STREAM STOP'
MISSED_REASON = 'MISSED_NO_FREEZE'
MISSED_LABEL = 'RECORDED_AFTER_THE_CUTOFF_FROM_LOCAL_RECORDS'
REGISTRATION_STATEMENT = ('I register OV-1 for this game before its first eligible draw. Both games close at 7.30pm '
                          'AEST. A stopped stream stays stopped.')
STOP_STATEMENT = 'I stop the OV-1 stream of this game. It stays stopped.'
RULES = {
    'formula': 'w_j = (variants with j in TOP) - (variants with j in WORST), over the variants with a complete '
               'PROSPECTIVE pair; X = sum of w_j over the seven drawn; Z = X / sqrt(V); '
               'f(lambda) = exp(lambda Z) / E0[exp(lambda Z)]; E(n) = mean over lambda of the products of f; E(0) = 1',
    'lambdas': [f'{n}/{d}' for n, d in NUM.LAMBDAS],
    'lambda_weights': 'EQUAL',
    'bar': NUM.BAR,
    'pair_rule': 'COMPLETE_PROSPECTIVE_TOP_AND_WORST_PAIR; anything else contributes nothing; nothing imputed',
    'zero_variance_rule': 'SKIP_WITH_FACTOR_1, decided on the eligibility line',
    'opportunity_rule': 'every target from first_target, in draw order, exactly once: COUNTED (or SKIPPED), '
                        'MISSED_NO_FREEZE (factor 1), or STOP; fixed by what existed before the cut-off',
    'cutoff_rule': '01:30 UTC on the target\'s derived draw date; the eligibility line durable before it',
    'operating_assumptions': [
        'the writers append as specified and nothing is later truncated, replaced or suppressed',
        'the PC\'s clock and the order of its events are trustworthy relative to the real cut-off',
        'no eligible freeze line is removed or hidden after the fact'],
    'after_a_stop': 'the stream stays stopped; no second registration; no recovery (RC-1)',
    'scoring_policy_id': WR.ROUTINE_POLICY,
    'kernel_version': NUM.KERNEL_VERSION,
    'kernel_digits': NUM.DIGITS,
    'kernel_margin': str(NUM.MARGIN),
    'error_budget': {'this_game': '1/40', 'programme': '1/20',
                     'rule': 'union bound over the two games; no reuse, no reset'},
}
REGISTRATION_FIELDS = ('schema', 'game_id', 'registered_utc', 'owner_statement', 'first_target',
                       'first_target_cutoff_utc', 'developed_record_digest', 'master_pin', 'rules', 'tool',
                       'tool_version')


class OV1Refused(Exception):
    """Refused before this command wrote anything."""


class OV1Blocked(Exception):
    """An input is not there yet or does not verify. Nothing was written for the target or any later one."""


def _root() -> Path:
    return Path(CR.PROJECT_ROOT)


def _marker_check() -> None:
    m = Path(CR.ORPHAN_MARKER)
    if m.exists() or m.is_symlink():
        raise OV1Refused('UNRESOLVED_ORPHAN_MARKER: no experiment, record or score is permitted')


def registration_path(root: Path, game_id: str) -> Path:
    return OR.weekly_root(root, game_id) / f'OV1_REGISTRATION_{game_id}_V1.json'


def ledger_path(root: Path, game_id: str) -> Path:
    return OR.weekly_root(root, game_id) / f'OV1_LEDGER_{game_id}_V1.jsonl'


def cutoff(game_id: str, target: int) -> datetime:
    """C(T): 01:30 UTC on the target's derived draw date. A fixed instant; no time-zone rule is involved. It is noon
    in Adelaide in daylight time and 11:00 in standard time, eight hours before 7.30pm AEST."""
    d = get_profile(game_id).derived_date(target)
    return datetime(d.year, d.month, d.day, 1, 30, tzinfo=timezone.utc)


def tool_sha256() -> str:
    """SHA-256 of this module and the kernel (LF): the registration's tool provenance."""
    here = Path(__file__).resolve().parent
    return sha256_hex(b''.join(p.read_bytes().replace(b'\r\n', b'\n') for p in (here / 'ov1.py', here / 'ov1_numeric.py')))


# ---------------------------------------------------------------- the registration (Sup 6.5; plan L5)

def validate_registration(rec, game_id: str) -> dict:
    what = 'OV-1 registration'
    if type(rec) is not dict or set(rec) != set(REGISTRATION_FIELDS):
        raise OR.RecordRefused(f'{what}: not the registration\'s fields')
    if rec['schema'] != REGISTRATION_SCHEMA or rec['game_id'] != game_id:
        raise OR.RecordRefused(f'{what}: wrong schema or game')
    if rec['owner_statement'] != REGISTRATION_STATEMENT:
        raise OR.RecordRefused(f'{what}: not the owner\'s fixed sentence')
    if rec['rules'] != RULES or rec['tool'] != TOOL or rec['tool_version'] != OV1_VERSION:
        raise OR.RecordRefused(f'{what}: registered under other rules or another version than this program\'s')
    t0 = rec['first_target']
    if type(t0) is not int or t0 <= get_profile(game_id).holdout_last:
        raise OR.RecordRefused(f'{what}: the first target is not a draw after the holdout')
    registered = WR.parse_utc(rec['registered_utc'], f'{what}.registered_utc')
    if rec['first_target_cutoff_utc'] != WR.utc_text(cutoff(game_id, t0)) or registered >= cutoff(game_id, t0):
        raise OR.RecordRefused(f'{what}: not registered before its first target\'s cut-off')
    pin = rec['master_pin']
    if (type(pin) is not dict or set(pin) != {'ledger_version', 'master_sha256', 'last_draw'} or
            pin['last_draw'] != t0 - 1 or type(pin['ledger_version']) is not int or
            type(pin['master_sha256']) is not str or not CP.V.SHA256.fullmatch(pin['master_sha256']) or
            type(rec['developed_record_digest']) is not str or not CP.V.SHA256.fullmatch(rec['developed_record_digest'])):
        raise OR.RecordRefused(f'{what}: the pin, the first target or the developed record\'s digest')
    return dict(rec)


def registration(root: Path, game_id: str) -> dict | None:
    """The game's registration, or None if the game was never registered. Anything in its place that is not exactly a
    registration refuses."""
    path = registration_path(root, game_id)
    if OR.absent(path):
        return None
    rec = WR._canonical_file(path)
    if rec is None:
        raise OR.RecordRefused('OV-1 registration: not a plain file of canonical bytes')
    return validate_registration(rec, game_id)


def _master_last(root: Path, game_id: str):
    """The last row of the master's version ledger (version, digest, last draw). The master itself is not opened."""
    try:
        return MV.ledger_rows(root, game_id)[-1]
    except (ValueError, IndexError) as exc:
        raise OV1Blocked(f'the master\'s version ledger does not read: {exc}') from None


def _forecast_ledger(root: Path, game_id: str) -> tuple[list[dict], bool]:
    """(verified freeze lines, whether the file ends in an unfinished line)."""
    try:
        lines = WR.forecast_ledger(root, game_id)
        _rows, torn = JL.read_lines(OR.forecast_ledger_path(root, game_id))
    except OR.RecordRefused as exc:
        raise OV1Blocked(f'the forecast ledger does not verify: {exc}') from None
    return lines, torn


def register(game_id: str, statement: str) -> dict:
    _marker_check()
    root = _root()
    if type(statement) is not str or statement.strip() != REGISTRATION_STATEMENT:
        raise OV1Refused('the owner statement must be typed exactly:\n  ' + REGISTRATION_STATEMENT)
    path = registration_path(root, game_id)
    if not OR.absent(path) or not OR.absent(ledger_path(root, game_id)):
        raise OV1Refused('OV-1 is already registered for this game (one registration per game; no second, ever)')
    try:
        developed = WR.developed(root, game_id)
    except OR.RecordRefused as exc:
        raise OV1Refused(str(exc)) from None
    try:
        last = _master_last(root, game_id)
        lines, _torn = _forecast_ledger(root, game_id)
    except OV1Blocked as exc:
        raise OV1Refused(str(exc)) from None
    t0 = last.last_draw + 1
    if WR.freeze_line_for(lines, t0) is not None:
        raise OV1Refused(f'draw {t0} already has a freeze line: OV-1 is registered before its first target is frozen')
    now = WR.now_utc()
    if now >= WR.deadline(game_id, t0)[0]:
        raise OV1Refused(f'the deadline of draw {t0} has passed: register after its result is accepted, for the next draw')
    rec = {'schema': REGISTRATION_SCHEMA, 'game_id': game_id, 'registered_utc': WR.utc_text(now),
           'owner_statement': REGISTRATION_STATEMENT, 'first_target': t0,
           'first_target_cutoff_utc': WR.utc_text(cutoff(game_id, t0)),
           'developed_record_digest': record_digest(developed),
           'master_pin': {'ledger_version': last.version, 'master_sha256': last.master_sha256, 'last_draw': last.last_draw},
           'rules': RULES, 'tool': TOOL, 'tool_version': OV1_VERSION}
    validate_registration(rec, game_id)
    OR.write_record(path, rec)
    WF._append_search_row({'row_type': 'OV1_REGISTRATION', 'utc': rec['registered_utc'], 'game_id': game_id,
                           'mode': 'OV1', 'window_first': t0, 'test_count': 1, 'measures': 'OV-1',
                           'plan_digest': record_digest(rec), 'tool': TOOL, 'tool_version': OV1_VERSION,
                           'tool_sha256': tool_sha256()})
    return rec


# ---------------------------------------------------------------- the ledger's lines and their order

_COMMON = ('schema', 'kind', 'game_id', 'target_draw_number', 'registration_digest', 'line_number',
           'previous_line_digest')
_FIELDS = {
    'ELIGIBILITY': _COMMON + ('cutoff_utc', 'written_utc', 'freeze_line_digest', 'freeze_line_number',
                              'freeze_frozen_utc', 'forecast_ledger_extent', 'eligible', 'eligible_count',
                              'eligible_digest', 'weights', 'variance', 'skip', 'factor_table_digest', 'certificate',
                              'kernel_version', 'master_pin'),
    'FACTOR': _COMMON + ('eligibility_line_digest', 'skipped', 'outcome_pins', 'x', 'z', 'log_factors',
                         'running_logs', 'counted_draws', 'score_lower_bound', 'score_text', 'crossed'),
    'MISSED': _COMMON + ('cutoff_utc', 'written_utc', 'reason', 'label', 'forecast_ledger_extent'),
    'STOP': _COMMON + ('written_utc', 'cause', 'detail', 'owner_statement'),
}


def _int_text(v) -> int:
    if type(v) is not str or not (v.lstrip('-').isdigit() and v.isascii()) or v != str(int(v)):
        raise OR.RecordRefused('OV-1 ledger: not a whole number as text')
    return int(v)


def _score_fields(sums, counted: int) -> dict:
    return {'running_logs': [str(v) for v in sums], 'counted_draws': counted,
            'score_lower_bound': str(NUM.mixture_lower(sums)), 'score_text': NUM.fixed_text(NUM.mixture_lower(sums)),
            'crossed': NUM.crossing(sums)}


def replay(reg: dict, rows) -> dict:
    """The stream's state from its registration and the ledger's lines, every line checked for its shape, its place in
    the order and its arithmetic. Anything else refuses (RecordRefused): the ledger is then not this program's."""
    game, reg_digest = reg['game_id'], record_digest(reg)
    n = WR.MAIN_POOL[game]
    st = {'reg': reg, 'registration_digest': reg_digest, 'rows': list(rows), 'next_target': reg['first_target'],
          'pending': None, 'sums': [0] * len(NUM.LAMBDAS), 'counted': 0, 'skipped': 0, 'missed': 0, 'stopped': None,
          'first_crossing': None, 'last_utc': WR.parse_utc(reg['registered_utc'])}
    for row in rows:
        what = f'OV-1 ledger line {row.get("line_number")}'
        kind = row.get('kind')
        if kind not in KINDS or set(row) != set(_FIELDS[kind]):
            raise OR.RecordRefused(f'{what}: not the fields of a known kind')
        t = st['next_target']
        if (row['schema'] != LINE_SCHEMA or row['game_id'] != game or row['registration_digest'] != reg_digest or
                row['target_draw_number'] != t):
            raise OR.RecordRefused(f'{what}: wrong schema, game, registration or target (expected draw {t})')
        if st['stopped'] is not None:
            raise OR.RecordRefused(f'{what}: a line after a stop')
        if kind != 'FACTOR':
            when = WR.parse_utc(row['written_utc'], f'{what}.written_utc')
            if when < st['last_utc']:
                raise OR.RecordRefused(f'{what}: a time earlier than the line before it')
            st['last_utc'] = when
        cut = cutoff(game, t)
        if kind == 'ELIGIBILITY':
            w = row['weights']
            if st['pending'] is not None or row['cutoff_utc'] != WR.utc_text(cut) or not when < cut or \
                    not WR.parse_utc(row['freeze_frozen_utc'], what) < cut:
                raise OR.RecordRefused(f'{what}: an eligibility line out of order or not before its cut-off')
            if type(w) is not list or len(w) != n or not all(type(x) is int for x in w) or sum(w) != 0:
                raise OR.RecordRefused(f'{what}: weights')
            num, den = NUM.variance(w)
            elig = row['eligible']
            if (row['variance'] != f'{num}/{den}' or row['skip'] is not (num == 0) or
                    (row['factor_table_digest'] is None) is not row['skip'] or
                    row['certificate'] != (None if row['skip'] else 'PASS') or
                    row['kernel_version'] != NUM.KERNEL_VERSION or type(elig) is not list or
                    row['eligible_count'] != len(elig) or row['eligible_digest'] != record_digest({'eligible': elig}) or
                    elig != sorted(elig) or type(row['freeze_line_number']) is not int):
                raise OR.RecordRefused(f'{what}: variance, skip, table, kernel or eligible variants do not agree')
            st['pending'] = row
        elif kind == 'FACTOR':
            p = st['pending']
            if p is None or row['eligibility_line_digest'] != record_digest(p) or row['skipped'] is not p['skip']:
                raise OR.RecordRefused(f'{what}: a factor line without its eligibility line')
            logs = [_int_text(v) for v in row['log_factors']] if type(row['log_factors']) is list else []
            if len(logs) != len(NUM.LAMBDAS) or (p['skip'] and (any(logs) or row['x'] is not None)) or \
                    (not p['skip'] and type(row['x']) is not int):
                raise OR.RecordRefused(f'{what}: log-factors or X')
            st['sums'] = [a + b for a, b in zip(st['sums'], logs)]
            st['counted'] += 0 if p['skip'] else 1
            st['skipped'] += 1 if p['skip'] else 0
            want = _score_fields(st['sums'], st['counted'])
            if any(row[k] != v for k, v in want.items()):
                raise OR.RecordRefused(f'{what}: running sums, score or crossing do not follow from the lines before')
            if row['crossed'] and st['first_crossing'] is None:
                st['first_crossing'] = t
            st['pending'], st['next_target'] = None, t + 1
        elif kind == 'MISSED':
            if st['pending'] is not None or row['cutoff_utc'] != WR.utc_text(cut) or when < cut or \
                    row['reason'] != MISSED_REASON or row['label'] != MISSED_LABEL:
                raise OR.RecordRefused(f'{what}: a missed line out of order, before its cut-off or mislabelled')
            st['missed'] += 1
            st['next_target'] = t + 1
        else:
            if row['cause'] not in STOP_CAUSES or type(row['detail']) is not str or \
                    row['owner_statement'] != (STOP_STATEMENT if row['cause'] == 'OWNER_STOP' else None):
                raise OR.RecordRefused(f'{what}: stop cause, detail or statement')
            st['stopped'] = row
    return st


def stream(root: Path, game_id: str) -> dict:
    """The game's stream: its registration and its ledger, verified. OV1Refused if the game is not registered;
    OV1Blocked if the registration or the ledger does not verify."""
    try:
        reg = registration(root, game_id)
        if reg is None:
            raise OV1Refused(f'OV-1 is not registered for {game_id} (the owner registers it once, before its first draw)')
        rows, torn = JL.read_lines(ledger_path(root, game_id))
        JL.verify_chain(rows, 'OV-1 ledger')
        st = replay(reg, rows)
    except OR.RecordRefused as exc:
        raise OV1Blocked(f'the OV-1 records do not verify: {exc}') from None
    st['torn'] = torn
    return st


# ---------------------------------------------------------------- building the lines (pure, given their inputs)

def _base(st: dict, kind: str) -> dict:
    return {'schema': LINE_SCHEMA, 'kind': kind, 'game_id': st['reg']['game_id'],
            'target_draw_number': st['next_target'], 'registration_digest': st['registration_digest']}


def tickets_to_weights(game_id: str, evidence) -> tuple[list, list[int]]:
    """(eligible variants, the weight of every number) from the verified records of a next-draw freeze line: a variant
    counts only with a FINAL_NEXT_DRAW forecast of class PROSPECTIVE that gives both a TOP and a WORST ticket (Sup 6.1).
    A failure record, a late record or a forecast lacking either ticket contributes nothing. A ticket that is not
    seven different numbers of the main barrel refuses."""
    n = WR.MAIN_POOL[game_id]
    weights, eligible = [0] * n, []
    for ev in evidence:
        r = ev['named']
        if r['record_kind'] != 'FORECAST' or r['run_mode'] != 'FINAL_NEXT_DRAW' or r['effective_class'] != 'PROSPECTIVE':
            continue
        pair = [COL._entry(ev['forecast'], readout, game_id)[0] for readout in ('TOP', 'WORST')]
        if pair[0] is None or pair[1] is None:
            continue
        for labels in (pair[0][0], pair[1][0]):
            if len(labels) != NUM.K or len(set(labels)) != NUM.K or \
                    not all(type(j) is int and 1 <= j <= n for j in labels):
                raise OR.RecordRefused('a frozen ticket is not seven different numbers of the main barrel')
        for j in pair[0][0]:
            weights[j - 1] += 1
        for j in pair[1][0]:
            weights[j - 1] -= 1
        eligible.append([r['method_id'], r['method_revision'], r['variant_id'], r['scored_record_digest']])
    return sorted(eligible), weights


def eligibility_content(game_id: str, line: dict, evidence) -> dict:
    """What an eligibility line says about the frozen tickets of one freeze line, with the draw's factor table built
    and certified (ov1_numeric.Refuse if no bound can be established). No time and no pin: the caller adds those."""
    eligible, weights = tickets_to_weights(game_id, evidence)
    num, den = NUM.variance(weights)
    table = NUM.factor_table(weights)
    return {'freeze_line_digest': record_digest(line), 'freeze_line_number': line['line_number'],
            'freeze_frozen_utc': line['frozen_utc'], 'eligible': eligible, 'eligible_count': len(eligible),
            'eligible_digest': record_digest({'eligible': eligible}), 'weights': weights, 'variance': f'{num}/{den}',
            'skip': table is None, 'factor_table_digest': None if table is None else NUM.table_digest(table),
            'certificate': None if table is None else 'PASS', 'kernel_version': NUM.KERNEL_VERSION}


def factor_step(game_id: str, policy: str, elig: dict, sums, counted: int, line: dict | None, score_rows) -> tuple:
    """What the pending eligibility line `elig` leads to, from the target's freeze line and the validated score ledger:
    ('FACTOR', fields), ('STOP', cause, detail), ('WAITING', why) while an eligible variant's score line is not yet
    written (the ordinary state between the freeze and the scoring), or ('BLOCKED', why). Pure: the same inputs give
    the same bytes."""
    t = elig['target_draw_number']
    if line is None or record_digest(line) != elig['freeze_line_digest'] or line['line_number'] != elig['freeze_line_number']:
        return ('BLOCKED', f'the forecast ledger no longer holds the freeze line that draw {t}\'s eligibility line sealed')
    if elig['skip']:
        return ('FACTOR', {'eligibility_line_digest': record_digest(elig), 'skipped': True, 'outcome_pins': [],
                           'x': None, 'z': None, 'log_factors': ['0'] * len(NUM.LAMBDAS),
                           **_score_fields(sums, counted)})
    try:
        table = NUM.factor_table(elig['weights'])
    except NUM.Refuse as exc:
        return ('STOP', 'FACTOR_TABLE_MISMATCH', f'the sealed table could not be rebuilt: {exc}')
    if table is None or NUM.table_digest(table) != elig['factor_table_digest']:
        return ('STOP', 'FACTOR_TABLE_MISMATCH', 'the factor table rebuilt at scoring is not the sealed one')
    by_key: dict[tuple, list] = {}
    for s in score_rows:
        if s['target_draw_number'] == t and s['scoring_policy_id'] == policy and s['amendment_of'] is None:
            by_key.setdefault((s['method_id'], s['method_revision'], s['variant_id']), []).append(s)
    mine, missing = [], None
    for m, rev, v, digest in elig['eligible']:
        found = by_key.get((m, rev, v), [])
        if not found:
            missing = missing or f'{m} revision {rev} {v}'
            continue
        s = found[0]
        try:
            if len(found) != 1:
                raise OR.RecordRefused('more than one routine score line')
            WR.check_score_linkage(s, line)
            if s['scored_record_digest'] != digest or s['record_kind'] != 'FORECAST' or s['effective_class'] != 'PROSPECTIVE':
                raise OR.RecordRefused('it is not the score of the frozen PROSPECTIVE forecast')
            for readout in ('TOP', 'WORST'):
                if 'main_matches' not in s['readouts'][readout]:
                    raise OR.RecordRefused(f'its {readout} readout is unavailable')
        except OR.RecordRefused as exc:
            return ('STOP', 'SCORE_LINE_CONTRADICTION', f'draw {t}, {m} revision {rev} {v}: {exc}')
        if not s['draw_date_is_derived']:
            return ('STOP', 'DRAW_DATE_NOT_DERIVED', f'draw {t}: its date in the master is not its derived date')
        mine.append(s)
    if missing:
        return ('WAITING', f'draw {t}: the score line of {missing} is not written yet')
    if len({tuple(s['drawn_main']) for s in mine}) != 1:
        return ('STOP', 'X_CONTRADICTION', f'draw {t}: the eligible variants\' score lines disagree about the drawn numbers')
    x_matches = sum(s['readouts']['TOP']['main_matches'] - s['readouts']['WORST']['main_matches'] for s in mine)
    x_weights = sum(elig['weights'][d - 1] for d in mine[0]['drawn_main'])
    if x_matches != x_weights or x_weights not in table['counts']:
        return ('STOP', 'X_CONTRADICTION', f'draw {t}: X by matches is {x_matches}, by weights {x_weights}; '
                                           f'they must agree and be a value the frozen weights can give')
    logs = [row[x_weights] for row in table['rows']]
    new = [a + b for a, b in zip(sums, logs)]
    pins = sorted({(s['outcome_ledger_version'], s['outcome_master_sha256']) for s in mine})
    return ('FACTOR', {'eligibility_line_digest': record_digest(elig), 'skipped': False,
                       'outcome_pins': [list(p) for p in pins], 'x': x_weights,
                       'z': NUM.z_text(x_weights, *table['variance']), 'log_factors': [str(v) for v in logs],
                       **_score_fields(new, counted + 1)})


def publication_names(root: Path, game_id: str) -> list[dict]:
    """The forecast-ledger extents and freeze-line digests that the league table's publication manifests name
    (Sup 6.8, EX_225 RC-225-1), each as {'what', 'lines', 'last_line_digest'} or {'what', 'target', 'freeze_line_digest'}.
    The league table is layer L4 (slice 3): until its manifests exist there is nothing to name, and its reader is
    connected here in that slice."""
    return []


def reconcile(root: Path, game_id: str, st: dict, lines, torn: bool, now: datetime) -> None:
    """Before a missed line: the forecast ledger must be whole and agree with every earlier record that names part of
    it. Any failure blocks (OV1Blocked); an absence of evidence is never taken as evidence of absence."""
    if torn:
        raise OV1Blocked('the forecast ledger ends in an unfinished line')
    if lines and WR.parse_utc(lines[-1]['frozen_utc']) > now:
        raise OV1Blocked('the forecast ledger holds a freeze time later than this program\'s clock')
    by_target = {line['target_draw_number']: line for line in lines}

    def extent(ext, what):
        if type(ext) is not dict or not JL.extent_still_there(lines, ext):
            raise OV1Blocked(f'the forecast ledger no longer holds the extent that {what} names')

    def freeze(target, digest, what):
        line = by_target.get(target)
        if line is None or record_digest(line) != digest:
            raise OV1Blocked(f'{what} names a freeze line for draw {target} that the forecast ledger does not hold')

    for row in st['rows']:
        if row['kind'] in ('ELIGIBILITY', 'MISSED'):
            extent(row['forecast_ledger_extent'], f'OV-1 ledger line {row["line_number"]}')
        if row['kind'] == 'ELIGIBILITY':
            freeze(row['target_draw_number'], row['freeze_line_digest'], f'OV-1 ledger line {row["line_number"]}')
    try:
        for w in WR.witness_ledger(root, game_id):
            freeze(w['target_draw_number'], w['freeze_line_digest'], 'a witness line')
        SI.scored_identities(root, game_id, lines)             # every score line names its target's freeze line
    except OR.RecordRefused as exc:
        raise OV1Blocked(f'the weekly records do not verify: {exc}') from None
    for name in publication_names(root, game_id):
        if 'lines' in name:
            extent(name, name['what'])
        else:
            freeze(name['target'], name['freeze_line_digest'], name['what'])


# ---------------------------------------------------------------- record: the one writer (plan L5)

def _stop_line(st: dict, cause: str, detail: str) -> dict:
    return {**_base(st, 'STOP'), 'written_utc': WR.utc_text(WR.now_utc()), 'cause': cause,
            'detail': detail.encode('ascii', 'replace').decode('ascii')[:400], 'owner_statement': None}


def _due(root: Path, game_id: str, st: dict) -> dict | None:
    """The one line due next for the stream's open target, or None when nothing is due yet. OV1Blocked when an input
    is not there or does not verify."""
    t = st['next_target']
    cut = cutoff(game_id, t)
    lines, torn = _forecast_ledger(root, game_id)
    line = WR.freeze_line_for(lines, t)
    if st['pending'] is not None:
        try:
            scores = WR.score_ledger(root, game_id)
        except OR.RecordRefused as exc:
            raise OV1Blocked(f'the score ledger does not verify: {exc}') from None
        step = factor_step(game_id, st['reg']['rules']['scoring_policy_id'], st['pending'], st['sums'], st['counted'],
                           line, scores)
        if step[0] == 'BLOCKED':
            raise OV1Blocked(step[1])
        if step[0] == 'WAITING':
            return None                                         # sealed before the cut-off; its scores are to come
        return _stop_line(st, step[1], step[2]) if step[0] == 'STOP' else {**_base(st, 'FACTOR'), **step[1]}
    pre_cutoff = (line is not None and line['set_kind'] == 'NEXT_DRAW_SET' and WR.parse_utc(line['frozen_utc']) < cut)
    if pre_cutoff:
        if WR.now_utc() >= cut:
            return _stop_line(st, 'ELIGIBILITY_NOT_VERIFIED',
                              f'{F01_TEXT}: draw {t} was frozen before its cut-off and no eligibility line was durable by then')
        last = _master_last(root, game_id)
        if last.last_draw >= t:
            raise OV1Blocked(f'draw {t}\'s result is already in the master before its cut-off: no eligibility line '
                             f'may be written; the stream stops at the cut-off')
        try:
            content = eligibility_content(game_id, line, WR.verify_named_records(root, game_id, line))
        except (OR.RecordRefused, NUM.Refuse) as exc:
            raise OV1Blocked(f'draw {t}: its eligibility cannot be established yet ({exc}); if this still holds at '
                             f'the cut-off the stream stops') from None
        written = WR.now_utc()                                  # read last: the line must be durable before C(T)
        if written >= cut:
            return _stop_line(st, 'ELIGIBILITY_NOT_VERIFIED', f'{F01_TEXT}: draw {t}\'s cut-off passed while its '
                                                               f'eligibility line was being prepared')
        return {**_base(st, 'ELIGIBILITY'), 'cutoff_utc': WR.utc_text(cut), 'written_utc': WR.utc_text(written),
                **content, 'forecast_ledger_extent': JL.extent(lines),
                'master_pin': {'ledger_version': last.version, 'master_sha256': last.master_sha256,
                               'last_draw': last.last_draw}}
    now = WR.now_utc()
    if now < cut:
        return None                                             # the open target: nothing is due before its cut-off
    reconcile(root, game_id, st, lines, torn, now)
    return {**_base(st, 'MISSED'), 'cutoff_utc': WR.utc_text(cut), 'written_utc': WR.utc_text(WR.now_utc()),
            'reason': MISSED_REASON, 'label': MISSED_LABEL, 'forecast_ledger_extent': JL.extent(lines)}


def record(game_id: str, *, echo=print) -> dict:
    """Append every line that is due, in order, nothing twice. Returns {'written': [(kind, target)...], 'state'}.
    OV1Blocked leaves what was appended before it in place; rerunning continues from the records alone."""
    _marker_check()
    root = _root()
    written = []
    while True:
        st = stream(root, game_id)
        if st['stopped'] is not None:
            break
        line = _due(root, game_id, st)
        if line is None:
            break
        JL.append(ledger_path(root, game_id), JL.chained(line, st['rows']))
        written.append((line['kind'], line['target_draw_number']))
        echo(f'[OV1] draw {line["target_draw_number"]}: {line["kind"]} line appended'
             + (f' ({line["cause"]}: {line["detail"]})' if line['kind'] == 'STOP' else ''))
    return {'written': written, 'state': status(game_id)}


def stop(game_id: str, statement: str) -> dict:
    """The owner's recorded stop, at the stream's open target. Nothing recovers it."""
    _marker_check()
    root = _root()
    if type(statement) is not str or statement.strip() != STOP_STATEMENT:
        raise OV1Refused('the owner statement must be typed exactly:\n  ' + STOP_STATEMENT)
    st = stream(root, game_id)
    if st['stopped'] is not None:
        raise OV1Refused('the stream is already stopped')
    line = {**_stop_line(st, 'OWNER_STOP', 'stopped by the owner'), 'owner_statement': STOP_STATEMENT}
    JL.append(ledger_path(root, game_id), JL.chained(line, st['rows']))
    return line


# ---------------------------------------------------------------- status and verify (read only)

def status(game_id: str) -> dict:
    st = stream(_root(), game_id)
    return {'game_id': game_id, 'first_target': st['reg']['first_target'], 'next_target': st['next_target'],
            'awaiting_score': None if st['pending'] is None else st['pending']['target_draw_number'],
            'counted': st['counted'], 'skipped': st['skipped'], 'missed': st['missed'],
            'score_text': NUM.fixed_text(NUM.mixture_lower(st['sums'])), 'bar': NUM.BAR,
            'first_crossing': st['first_crossing'],
            'stopped': None if st['stopped'] is None else
            {'target': st['stopped']['target_draw_number'], 'cause': st['stopped']['cause'],
             'detail': st['stopped']['detail']},
            'lines': len(st['rows'])}


def status_lines(game_id: str) -> list[str]:
    s = status(game_id)
    out = [f'OV-1 {game_id}: registered from draw {s["first_target"]}; {s["counted"]} counted, {s["skipped"]} skipped '
           f'(V = 0), {s["missed"]} missed; proved lower bound of the evidence score {s["score_text"]} (bar {s["bar"]})']
    if s['first_crossing'] is not None:
        out.append(f'  the score reached {s["bar"]} at draw {s["first_crossing"]}: a challenge to the fair-draw '
                   f'assumption for this game, not proof of a cause')
    if s['stopped'] is not None:
        out.append(f'  STREAM STOPPED at draw {s["stopped"]["target"]} ({s["stopped"]["cause"]}): {s["stopped"]["detail"]}')
        out.append('  a stopped stream stays stopped; forecasting and scoring continue as normal')
    elif s['awaiting_score'] is not None:
        out.append(f'  draw {s["awaiting_score"]}: eligibility sealed before its cut-off; awaiting its scores')
    else:
        out.append(f'  next target: draw {s["next_target"]}')
    out.append('  class PROSPECTIVE rests on local timing and tamper-evident records; it is not external proof of '
               'pre-draw publication')
    return out


def verify(game_id: str) -> dict:
    """Rebuild every line and compare bytes: an eligibility line from its freeze line and the run folders it names; a
    factor line from its eligibility line and the score ledger; a missed line from the forecast ledger. OV1Blocked
    names the first line that is not reproduced."""
    root = _root()
    st = stream(root, game_id)
    lines, _torn = _forecast_ledger(root, game_id)
    try:
        scores = WR.score_ledger(root, game_id)
    except OR.RecordRefused as exc:
        raise OV1Blocked(f'the score ledger does not verify: {exc}') from None
    policy = st['reg']['rules']['scoring_policy_id']
    by_number = {line['line_number']: line for line in lines}
    counts = dict.fromkeys(KINDS, 0)
    pending, sums, counted = None, [0] * len(NUM.LAMBDAS), 0
    for row in st['rows']:
        what, t = f'OV-1 ledger line {row["line_number"]} (draw {row["target_draw_number"]})', row['target_draw_number']
        counts[row['kind']] += 1
        if row['kind'] == 'ELIGIBILITY':
            line = by_number.get(row['freeze_line_number'])
            try:
                if line is None or line['target_draw_number'] != t or line['set_kind'] != 'NEXT_DRAW_SET':
                    raise OR.RecordRefused('its freeze line is not in the forecast ledger')
                content = eligibility_content(game_id, line, WR.verify_named_records(root, game_id, line))
            except (OR.RecordRefused, NUM.Refuse) as exc:
                raise OV1Blocked(f'{what}: not reproduced ({exc})') from None
            if canonical({**row, **content}) != canonical(row) or not JL.extent_still_there(lines, row['forecast_ledger_extent']):
                raise OV1Blocked(f'{what}: the frozen tickets do not give this eligibility line')
            pending = row
        elif row['kind'] == 'FACTOR':
            step = factor_step(game_id, policy, pending, sums, counted, WR.freeze_line_for(lines, t), scores)
            if step[0] != 'FACTOR' or canonical({**row, **step[1]}) != canonical(row):
                raise OV1Blocked(f'{what}: the score ledger does not give this factor line ({step[0]}: {step[1]})')
            sums = [int(v) for v in row['running_logs']]
            counted, pending = row['counted_draws'], None
        elif row['kind'] == 'MISSED':
            line = WR.freeze_line_for(lines, t)
            if not JL.extent_still_there(lines, row['forecast_ledger_extent']) or (
                    line is not None and line['set_kind'] == 'NEXT_DRAW_SET' and
                    WR.parse_utc(line['frozen_utc']) < cutoff(game_id, t)):
                raise OV1Blocked(f'{what}: the forecast ledger holds a pre-cut-off freeze line, or lost the named extent')
    return {'lines': len(st['rows']), **{k.lower(): v for k, v in counts.items()}}
