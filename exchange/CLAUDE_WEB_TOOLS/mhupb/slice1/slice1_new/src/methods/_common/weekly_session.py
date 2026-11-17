"""MHUP-B: the forecasting half of the weekly session (design v0.1r7 sections 6.1 to 6.5, Appendices F and I; code plan
v0.3 section 5, L2). Launched only through Method_Weekly_Forecast.py under Run_Experiment.bat.

It forecasts and freezes; it never scores and never reads an outcome. It imports nothing from the evaluator. What it
knows of scores is the scientific identities `score_identities` returns, so that it can tell which target is closed.

Commands (each re-derives everything from the create-only records; nothing is held in memory between commands):
  status         the status block (6.2); read-only.
  open-session   a new session: the session record (pin = the ledger's last row, the roster, the closure and
                 environment digests), then the session lock. With resume=True: reopen the session the lock names,
                 only with a fresh, unused resume token and unchanged digests; recorded as a RESUMED ticket.
  next           exactly Appendix F. STALE if the master grew. Otherwise the lowest accepted target after the holdout
                 that is not closed: if it has a freeze line, FROZE N at once; if not, complete its set (close the
                 open tickets, run the roster's variants that have no DONE ticket in any session, write the freeze
                 line), FROZE N. With none: M = last draw + 1: OPEN M if it has a freeze line; complete a set that a
                 SET_STARTED ticket began; start one if at least an hour remains to M's deadline; else NONE.
  close-session  remove the lock at a clean end (STALE, or nothing accepted left unclosed and no set left unfinished).

The order is enforced here, so a faulty sequencer cannot skip a step: `next` never looks at a later target while an
accepted one is unclosed, and never makes a second set for a target.
"""
from __future__ import annotations

from collections.abc import Mapping
import json
from pathlib import Path
import uuid

import _common.contract_publication as CP
import _common.contract_runner as CR
import _common.walk_forward as WF
from _common import closure as CL
from _common import jsonl_ledger as JL
from _common import master_versions as MV
from _common import owner_records as OR
from _common import release_records as RR
from _common import score_identities as SI
from _common import weekly_records as WR
from _common.contract_dispatch import DispatchRefused
from _common.contract_records import record_digest
from _common.game_profiles import get_profile

STATES = ('STALE', 'FROZE', 'FROZE_NEXT', 'OPEN', 'NONE')
CLEAN_END = ('STALE', 'FROZE_NEXT', 'OPEN', 'NONE')


class SessionRefused(Exception):
    """Refused before this command wrote anything."""


class SessionStopped(Exception):
    """Stopped part-way: every record already written stands; rerunning the command resumes from the records."""


def _root() -> Path:
    return Path(CR.PROJECT_ROOT)


def _guard(fn, *args, **kw):
    try:
        return fn(*args, **kw)
    except (OR.RecordRefused, RR.Refused) as exc:
        raise SessionRefused(str(exc)) from None


def _marker_check() -> None:
    m = Path(CR.ORPHAN_MARKER)
    if m.exists() or m.is_symlink():
        raise SessionRefused('UNRESOLVED_ORPHAN_MARKER: no experiment or session is permitted')


def _last_row(game_id: str):
    try:
        _raw, rows, _evidence = MV.load_verified_source(_root(), game_id)
    except MV.LedgerRefused as exc:
        raise SessionRefused(f'the master ledger does not pass the version-2 rules: {exc}') from None
    return rows[-1]


def _digests() -> tuple[str, str]:
    try:
        frozen = CL.freeze(_root())
    except CL.ClosureRefused as exc:
        raise SessionRefused(f'the closure or the environment refuses: {exc}') from None
    return frozen['closure']['digest'], frozen['environment']['digest']


def _exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def _lock_session(game_id: str) -> str | None:
    """The session id the game's lock names, or None if there is no lock."""
    lock = OR.session_lock_path(_root(), game_id)
    if not _exists(lock):
        return None
    if lock.is_symlink() or not lock.is_file():
        raise SessionRefused('the session lock exists but is not a plain file')
    sid = lock.read_bytes().decode('ascii', errors='replace').split(' ', 1)[0].strip()
    if not OR.SESSION_ID.fullmatch(sid):
        raise SessionRefused('the session lock does not name a session id')
    return sid


def _order(key) -> tuple:
    return (int(key[0][2:]), key[2], int(key[1]))            # method number, variant, revision


def roster_now(game_id: str, adapters: Mapping) -> tuple[list[dict], list[dict]]:
    """(the session roster, the registered but non-runnable methods). The roster is every released, unretired variant
    of the game (release_records) with its release date, and must equal the installed registry's runnable set
    (active SUPPORTED entry, no development flag, an adapter): an installed but unreleased revision qualifies for
    nothing (design 4.3), and a released variant that cannot run refuses the session rather than being dropped."""
    try:
        members, excluded = WF.cohort(game_id, adapters)
    except WF.BatchRefused as exc:
        raise SessionRefused(f'cohort: {exc}') from None
    try:
        released = {k: v for k, v in RR.released_variants(_root()).items() if k[0] == game_id}
    except (RR.Refused, ValueError, KeyError) as exc:
        raise SessionRefused(f'the release records refuse: {exc}') from None
    runnable = {(game_id, m['method_id'], m['method_revision'], m['variant_id']): m for m in members}
    if set(runnable) != set(released) or excluded:
        only_reg, only_rel = sorted(set(runnable) - set(released)), sorted(set(released) - set(runnable))
        raise SessionRefused('the runnable set is not the released set: '
                             f'{len(only_reg)} runnable but not released, {len(only_rel)} released but not runnable, '
                             f'{len(excluded)} excluded' + (f' (first: {(only_reg + only_rel)[0]})' if only_reg + only_rel else ''))
    roster = [{'method_id': m['method_id'], 'method_revision': m['method_revision'], 'variant_id': m['variant_id'],
               'release_date': released[k], 'declaration_digest': m['declaration_digest'],
               'registry_entry_digest': m['registry_entry_digest'], 'minimum_history_draws': m['minimum_history_draws']}
              for k, m in runnable.items()]
    roster.sort(key=lambda m: _order((m['method_id'], m['method_revision'], m['variant_id'])))
    reg = WF._registry()
    not_runnable = []
    for (g, m, v) in reg.chain_keys():
        if g == game_id and reg.active_entry(g, m, v)['registry_status'] != 'SUPPORTED':
            not_runnable.append({'method_id': m, 'variant_id': v,
                                 'registry_status': reg.active_entry(g, m, v)['registry_status']})
    return roster, not_runnable


# ---------------------------------------------------------------- open-session, resume

def open_session(game_id: str, adapters: Mapping, *, resume: bool = False) -> dict:
    _marker_check()
    root, p = _root(), get_profile(game_id)
    if _guard(OR.developed_record, root, game_id) is None:
        raise SessionRefused(f'NOT_DEVELOPED: no developed record for {game_id} (GOAL-1); the weekly session has not begun')
    if _exists(OR.updater_lock_path(root)):
        raise SessionRefused('the updater\'s lock exists (an update may be in progress); no session is opened')
    locked = _lock_session(game_id)
    if resume:
        return _resume(game_id, locked)
    if locked is not None:
        raise SessionRefused(f'a session lock exists for session {locked}; resume it (open-session --resume, after the '
                             f'process check) or clear it with the process tool')
    row = _last_row(game_id)
    if row.last_draw < p.holdout_last:
        raise SessionRefused('the master does not yet hold the whole holdout')
    closure, environment = _digests()
    roster, not_runnable = roster_now(game_id, adapters)
    rec = {'schema': OR.SESSION_SCHEMA, 'session_id': uuid.uuid4().hex, 'game_id': game_id,
           'started_utc': WR.utc_text(WR.now_utc()), 'ledger_version': row.version, 'master_sha256': row.master_sha256,
           'last_draw': row.last_draw,
           'developed_record_sha256': OR.file_sha256(OR.developed_record_path(root, game_id)),
           'closure_digest': closure, 'environment_digest': environment, 'roster': roster,
           'not_runnable': not_runnable, 'tool': WR.SESSION_TOOL, 'tool_version': WR.FORECAST_VERSION}
    WR.validate_session(rec, game_id)
    OR.write_record(OR.session_record_path(root, game_id, rec['session_id']), rec)
    lock = OR.session_lock_path(root, game_id)
    lock.parent.mkdir(parents=True, exist_ok=True)
    CP.create_only(lock, f"{rec['session_id']} {rec['started_utc']}\n".encode('ascii'))
    return rec


def _resume(game_id: str, locked: str | None) -> dict:
    root = _root()
    if locked is None:
        raise SessionRefused('no session lock: there is no session to resume (open a new one)')
    session = _guard(WR.session, root, game_id, locked)
    if _digests() != (session['closure_digest'], session['environment_digest']):
        raise SessionRefused('CODE_CHANGED: the closure or environment digest differs from the session record\'s; '
                             'this session cannot continue (clear its lock with the process tool and open a new one)')
    tokens = sorted(WR.sessions_folder(root, game_id).glob(f'RESUME_{locked}_*.json'))
    if not tokens:
        raise SessionRefused('no resume token for this session (run the process check first)')
    newest = tokens[-1]
    try:
        tok = json.loads(newest.read_bytes().decode('ascii')) if newest.is_file() and not newest.is_symlink() else None
    except (ValueError, UnicodeDecodeError):
        tok = None
    if (type(tok) is not dict or tok.get('schema') != OR.RESUME_TOKEN_SCHEMA or tok.get('game_id') != game_id or
            tok.get('session_id') != locked):
        raise SessionRefused('the newest resume token is not a token of this session')
    now = WR.now_utc()
    age = now - _guard(WR.parse_utc, tok.get('utc'), 'resume token time')
    if age > WR.RESUME_TOKEN_MAX_AGE or age.total_seconds() < -60:
        raise SessionRefused('the resume token is older than five minutes (or from the future); run the process check again')
    path = OR.session_attempts_path(root, game_id, locked)
    rows = _guard(OR.tickets, path, scope_kind='WEEKLY_SESSION', scope_id=locked, game_id=game_id)
    if any(t['kind'] == 'RESUMED' and t.get('resume_token') == newest.name for t in rows):
        raise SessionRefused('the resume token was already used; run the process check again')
    JL.append(path, OR.ticket('RESUMED', scope_kind='WEEKLY_SESSION', scope_id=locked, game_id=game_id, method_id=None,
                              variant_id=None, method_revision=None, target_draw_number=None, run_id=None,
                              utc=WR.utc_text(now),
                              extra={'resume_token': newest.name, 'resume_token_sha256': OR.file_sha256(newest)}))
    return session


# ---------------------------------------------------------------- the state every command derives from the records

def _state(game_id: str, row) -> dict:
    """The freeze lines, which targets are closed, and the lowest accepted target that is not (or None)."""
    root, p = _root(), get_profile(game_id)
    lines = _guard(WR.forecast_ledger, root, game_id)
    identities = _guard(SI.scored_identities, root, game_id)
    closed = _guard(SI.closed_targets, game_id, lines, identities)
    by_target = {line['target_draw_number']: line for line in lines}
    lowest = next((t for t in range(p.holdout_last + 1, row.last_draw + 1) if t not in closed), None)
    return {'lines': lines, 'by_target': by_target, 'closed': closed, 'lowest_unclosed': lowest,
            'identities': identities}


def _set_started(tickets_by_session: Mapping, target: int) -> bool:
    return any(t['kind'] == 'SET_STARTED' and t['target_draw_number'] == target
               for rows in tickets_by_session.values() for t in rows)


def _own_session(game_id: str, session_id: str) -> dict:
    locked = _lock_session(game_id)
    if locked != session_id:
        raise SessionRefused(f'session {session_id} is not the game\'s active session (the lock names {locked})')
    return _guard(WR.session, _root(), game_id, session_id)


# ---------------------------------------------------------------- next

def next_step(game_id: str, session_id: str, adapters: Mapping, *, echo=print) -> tuple[str, int | None]:
    """One step of Appendix F. Returns (state, target)."""
    _marker_check()
    session = _own_session(game_id, session_id)
    if _digests() != (session['closure_digest'], session['environment_digest']):
        raise SessionRefused('CODE_CHANGED: the closure or environment digest differs from the session record\'s')
    row = _last_row(game_id)
    if (row.version, row.master_sha256) != OR.pin_of(session, 'session record'):
        return 'STALE', None
    st = _state(game_id, row)
    n = st['lowest_unclosed']
    if n is not None:
        if n not in st['by_target']:
            _complete_set(session, n, 'CATCH_UP_SET', st['lines'], adapters, echo)
        return 'FROZE', n
    m = row.last_draw + 1
    if m in st['by_target']:
        return 'OPEN', m
    root = _root()
    if not _set_started(_guard(WR.session_tickets, root, game_id), m):
        deadline_utc, _offset = WR.deadline(game_id, m)
        now = WR.now_utc()
        if now + WR.HOUR_RULE > deadline_utc:
            return 'NONE', m
        JL.append(OR.session_attempts_path(root, game_id, session_id),
                  OR.ticket('SET_STARTED', scope_kind='WEEKLY_SESSION', scope_id=session_id, game_id=game_id,
                            method_id=None, variant_id=None, method_revision=None, target_draw_number=m, run_id=None,
                            utc=WR.utc_text(now),
                            extra={'run_mode': 'FINAL_NEXT_DRAW', 'deadline_utc': WR.utc_text(deadline_utc)}))
    _complete_set(session, m, 'NEXT_DRAW_SET', st['lines'], adapters, echo)
    return 'FROZE_NEXT', m


def _declaration(digest: str) -> dict:
    try:
        return WF._registry().declaration(digest)
    except ValueError:
        raise SessionRefused('a roster entry\'s declaration is not installed') from None


def _close_open_tickets(game_id: str, target: int) -> dict:
    """Before any new ticket (design 6.3): every OPEN ticket for the target, in any session's ledger, that no DONE or
    FAILED_TO_START has closed gets one: DONE if its run folder proves a completed run, FAILED_TO_START otherwise."""
    root = _root()
    counts = {'DONE': 0, 'FAILED_TO_START': 0}
    for sid, rows in _guard(WR.session_tickets, root, game_id).items():
        closed = {t['run_id'] for t in rows if t['kind'] in ('DONE', 'FAILED_TO_START')}
        for t in rows:
            if t['kind'] != 'OPEN' or t['target_draw_number'] != target or t['run_id'] in closed:
                continue
            kind, tclass = 'FAILED_TO_START', None
            try:
                owner = WR.session(root, game_id, sid)
                mem = OR.roster_entry(owner, t['method_id'], t['method_revision'], t['variant_id'])
                mode = t.get('run_mode')
                if mem is not None and mode in WR.SESSION_RUN_MODES:
                    req = WR.request_for(owner, mem, target, t['run_id'], mode)
                    if record_digest(req) == t['request_digest']:
                        ev = WR.run_evidence(root, req, _declaration(mem['declaration_digest']))
                        kind, tclass = 'DONE', ev['terminal_class']
            except OR.RecordRefused:
                pass                                            # nothing proves a completed run: FAILED_TO_START
            JL.append(OR.session_attempts_path(root, game_id, sid),
                      OR.ticket(kind, scope_kind='WEEKLY_SESSION', scope_id=sid, game_id=game_id,
                                method_id=t['method_id'], variant_id=t['variant_id'],
                                method_revision=t['method_revision'], target_draw_number=target, run_id=t['run_id'],
                                utc=WR.utc_text(WR.now_utc()), terminal_class=tclass,
                                extra={'run_mode': t.get('run_mode')}))
            counts[kind] += 1
            closed.add(t['run_id'])
    return counts


def _complete_set(session: Mapping, target: int, set_kind: str, lines, adapters: Mapping, echo) -> None:
    """Run the session roster's variants that have no DONE ticket for the target in any session's ledger, then append
    the target's freeze line, naming every variant's one ticketed DONE record with that record's own session."""
    root, game_id, sid = _root(), session['game_id'], session['session_id']
    p = get_profile(game_id)
    resumed = _close_open_tickets(game_id, target)
    if any(resumed.values()):
        echo(f'[WEEKLY-FORECAST] target {target}: open tickets closed: {resumed["DONE"]} DONE, '
             f'{resumed["FAILED_TO_START"]} FAILED_TO_START (run ids never reused)')
    done = _guard(WR.done_records, _guard(WR.session_tickets, root, game_id), target)
    accepted = target <= session['last_draw']
    draw_date = p.derived_date(target)
    attempts = OR.session_attempts_path(root, game_id, sid)
    for mem in session['roster']:
        key = (mem['method_id'], mem['method_revision'], mem['variant_id'])
        if key in done:
            continue
        if accepted:
            mode = 'CATCH_UP' if OR.release_date_of(mem) < draw_date else 'REAL_DEVELOPMENT'
        else:
            mode = 'FINAL_NEXT_DRAW'
        req = WR.request_for(session, mem, target, CP.new_run_id(), mode)
        ident = f"{mem['method_id']} {mem['variant_id']} target {target} {mode}"
        common = dict(scope_kind='WEEKLY_SESSION', scope_id=sid, game_id=game_id, method_id=mem['method_id'],
                      variant_id=mem['variant_id'], method_revision=mem['method_revision'], target_draw_number=target,
                      run_id=req['run_id'], extra={'run_mode': mode})
        JL.append(attempts, OR.ticket('OPEN', utc=WR.utc_text(WR.now_utc()), request_digest=record_digest(req), **common))
        try:
            res = CR.run_contract_method(req, compute=adapters[mem['method_id']].compute,
                                         verify=adapters[mem['method_id']].verify, repo_root=root,
                                         run_root=OR.weekly_runs_root(root))
        except (CR.RunRefused, DispatchRefused) as exc:
            raise SessionStopped(f'{ident}: REFUSED: {exc.text}') from None
        if WF.classify(res.outcome, res.reason) != 'CONTINUE':
            raise SessionStopped(f'{ident}: {res.outcome}: {res.reason}')
        tclass = f'{res.outcome} {WF.reason_prefix(res.reason)}'
        try:
            ev = WR.run_evidence(root, req, _declaration(mem['declaration_digest']))
        except OR.RecordRefused as exc:
            raise SessionStopped(f'{ident}: the run folder does not prove the run ({exc})') from None
        if ev['terminal_class'] != tclass or (res.outcome == 'SUCCESS' and ev['forecast'] is None):
            raise SessionStopped(f'{ident}: the run folder does not hold what the run reported')
        JL.append(attempts, OR.ticket('DONE', utc=WR.utc_text(WR.now_utc()), terminal_class=tclass, **common))
        echo(f'[WEEKLY-FORECAST] {ident}: {tclass}')
    done = _guard(WR.done_records, _guard(WR.session_tickets, root, game_id), target)
    deadline_utc, deadline_offset = WR.deadline(game_id, target)
    records = [_named_record(game_id, target, key, done[key], deadline_utc) for key in sorted(done, key=_order)]
    finals = [r['effective_class'] == 'PROSPECTIVE' for r in records
              if r['run_mode'] == 'FINAL_NEXT_DRAW' and r['record_kind'] == 'FORECAST']
    now = WR.now_utc()
    if lines and now < WR.parse_utc(lines[-1]['frozen_utc']):
        raise SessionStopped(f'target {target}: the clock is behind the last freeze line; no freeze line is written '
                             f'until the clock is right')
    line = JL.chained({'schema': OR.FREEZE_LINE_SCHEMA, 'game_id': game_id, 'target_draw_number': target,
                       'target_draw_date': draw_date.isoformat(), 'set_kind': set_kind, 'writing_session_id': sid,
                       'frozen_utc': WR.utc_text(now), 'local_offset_minutes': WR.offset_minutes(now.astimezone()),
                       'deadline_utc': WR.utc_text(deadline_utc), 'deadline_offset_minutes': deadline_offset,
                       'deadline_met': all(finals) if finals else None, 'records': records,
                       'not_runnable': session['not_runnable'], 'closure_digest': session['closure_digest'],
                       'environment_digest': session['environment_digest'], 'tool': WR.SESSION_TOOL,
                       'tool_version': WR.FORECAST_VERSION}, lines)
    try:
        WR.validate_freeze_line(line, game_id)
    except OR.RecordRefused as exc:
        raise SessionStopped(f'target {target}: the freeze line would be invalid ({exc}); nothing was appended') from None
    JL.append(OR.forecast_ledger_path(root, game_id), line)
    echo(f'[WEEKLY-FORECAST] target {target}: freeze line {line["line_number"]} written, {len(records)} record(s), '
         f'{set_kind}')


def _named_record(game_id: str, target: int, key: tuple, found: tuple, deadline_utc) -> dict:
    """One entry of a freeze line: the pair's one ticketed DONE record, with its own session binding, re-read from its
    run folder (so the line names only what the records prove)."""
    root = _root()
    sid, done_ticket, open_ticket = found
    try:
        owner = WR.session(root, game_id, sid)
        mem = OR.roster_entry(owner, *key)
        mode = open_ticket.get('run_mode')
        if mem is None or mode not in WR.SESSION_RUN_MODES:
            raise OR.RecordRefused('its ticket does not name a roster variant and a session run mode')
        req = WR.request_for(owner, mem, target, done_ticket['run_id'], mode)
        if record_digest(req) != open_ticket['request_digest']:
            raise OR.RecordRefused('its ticket does not name the session\'s request')
        ev = WR.run_evidence(root, req, _declaration(mem['declaration_digest']))
    except OR.RecordRefused as exc:
        raise SessionStopped(f'target {target}: the DONE record of {key} does not verify ({exc})') from None
    failed = ev['forecast'] is None
    frozen = None if failed else WR.parse_utc(ev['receipt']['frozen_at_utc'])
    before = OR.release_date_of(mem) < get_profile(game_id).derived_date(target)
    return {'method_id': key[0], 'method_revision': key[1], 'variant_id': key[2], 'session_id': sid,
            'session_digest': record_digest(owner), 'run_id': done_ticket['run_id'], 'run_mode': mode,
            'tier': WR.tier_of(mode), 'record_kind': 'PREDICTION_FAILED' if failed else 'FORECAST',
            'terminal_class': ev['terminal_class'], 'done_ticket_digest': record_digest(done_ticket),
            'scored_record_digest': record_digest(ev['terminal']) if failed else ev['forecast']['canonical_content_digest'],
            'freeze_receipt_digest': None if failed else record_digest(ev['receipt']),
            'terminal_digest': record_digest(ev['terminal']), 'ledger_version': owner['ledger_version'],
            'master_sha256': owner['master_sha256'],
            'frozen_at_utc': None if failed else ev['receipt']['frozen_at_utc'], 'release_date': mem['release_date'],
            'effective_class': WR.effective_class(mode, frozen, deadline_utc, failed=failed),
            'missing_batch': before and mode != 'FINAL_NEXT_DRAW'}


# ---------------------------------------------------------------- close-session

def close_session(game_id: str, session_id: str) -> str:
    """Remove the session lock, only at a clean end. Returns the end state it found."""
    _own_session(game_id, session_id)
    session = _guard(WR.session, _root(), game_id, session_id)
    row = _last_row(game_id)
    if (row.version, row.master_sha256) != OR.pin_of(session, 'session record'):
        end = 'STALE'
    else:
        st = _state(game_id, row)
        if st['lowest_unclosed'] is not None:
            raise SessionRefused(f'target {st["lowest_unclosed"]} has an accepted result and is not closed; the session is '
                                 f'not at a clean end and its lock stays')
        m = row.last_draw + 1
        if m in st['by_target']:
            end = 'OPEN'
        elif _set_started(_guard(WR.session_tickets, _root(), game_id), m):
            raise SessionRefused(f'the set for target {m} was started and has no freeze line; the lock stays')
        else:
            end = 'NONE'
    OR.session_lock_path(_root(), game_id).unlink()
    return end


# ---------------------------------------------------------------- status (6.2)

def status(game_id: str) -> dict:
    """The status block's facts, from the records alone. Read-only; no run, no ticket, no outcome."""
    root, p = _root(), get_profile(game_id)
    row = _last_row(game_id)
    out = {'game_id': game_id, 'ledger_version': row.version, 'last_draw': row.last_draw,
           'developed': _guard(OR.developed_record, root, game_id) is not None,
           'session_lock': _lock_session(game_id), 'updater_lock': _exists(OR.updater_lock_path(root))}
    st = _state(game_id, row)
    tickets = _guard(WR.session_tickets, root, game_id)
    backlog = []
    for t in range(p.holdout_last + 1, row.last_draw + 1):
        if t not in st['closed']:
            line = st['by_target'].get(t)
            backlog.append({'target': t, 'status': 'OUTCOME_AVAILABLE',
                            'state': 'frozen, not yet scored' if line else 'not yet forecast',
                            'unscored': len(SI.unscored_records(game_id, line, st['identities'])) if line else None})
    m = row.last_draw + 1
    deadline_utc, offset = WR.deadline(game_id, m)
    now = WR.now_utc()
    if m in st['by_target']:
        nxt = 'OPEN (frozen; its result is not yet accepted)'
    elif _set_started(tickets, m):
        nxt = 'a set was started and has no freeze line: the next session completes it'
    elif now + WR.HOUR_RULE <= deadline_utc:
        nxt = 'a next-draw set can start (at least an hour remains): its records will be PROSPECTIVE if frozen before the deadline'
    else:
        nxt = 'OUTCOME_PENDING: too late for a next-draw set; it will be caught up (CATCH_UP) once its result is accepted'
    out.update(backlog=backlog, next_target=m, next_target_date=p.derived_date(m).isoformat(),
               next_deadline_utc=WR.utc_text(deadline_utc), next_deadline_offset_minutes=offset, next_state=nxt,
               frozen_targets=len(st['lines']), closed_targets=len(st['closed']))
    try:
        released = sorted((k[1], k[2], k[3]) for k in RR.released_variants(root) if k[0] == game_id)
    except (RR.Refused, ValueError, KeyError) as exc:
        raise SessionRefused(f'the release records refuse: {exc}') from None
    out['active_variants'] = len(released)
    last = None
    for path in sorted(WR.sessions_folder(root, game_id).glob('SESSION_*.json')) if WR.sessions_folder(root, game_id).is_dir() else []:
        s = _guard(WR.session, root, game_id, path.name[len('SESSION_'):-len('.json')])
        if last is None or s['started_utc'] > last['started_utc']:
            last = s
    if last is not None:
        before = {(m_['method_id'], m_['method_revision'], m_['variant_id']) for m_ in last['roster']}
        out['joined_since_last_session'] = sorted(set(released) - before)
        out['left_since_last_session'] = sorted(before - set(released))
        out['last_session'] = last['session_id']
    done_by_variant, scored_by_variant = {}, {}
    for rows in tickets.values():
        for t in rows:
            if t['kind'] == 'DONE':
                k = (t['method_id'], t['method_revision'], t['variant_id'])
                done_by_variant[k] = max(done_by_variant.get(k, 0), t['target_draw_number'])
    for ident in st['identities']:
        k = (ident[1], ident[2], ident[3])
        scored_by_variant[k] = max(scored_by_variant.get(k, 0), ident[4])
    out['variants_with_records'] = len(done_by_variant)
    out['last_done_target'] = max(done_by_variant.values(), default=None)
    out['last_scored_target'] = max(scored_by_variant.values(), default=None)
    diag = OR.diagnostic_runs_root(root) / game_id
    out['diagnostic_records'] = sum(1 for _f in diag.rglob(CP.FILES['terminal'])) if diag.is_dir() else 0
    return out


def status_lines(s: Mapping) -> list[str]:
    g = s['game_id']
    lines = [f'[WEEKLY-FORECAST] STATUS {g}: last accepted result version {s["ledger_version"]}, last draw {s["last_draw"]}',
             f'[WEEKLY-FORECAST]   developed record: {"present" if s["developed"] else "ABSENT (the weekly session has not begun)"}; '
             f'session lock: {s["session_lock"] or "none"}; updater lock: {"PRESENT" if s["updater_lock"] else "none"}',
             f'[WEEKLY-FORECAST]   active variants: {s["active_variants"]}; frozen targets: {s["frozen_targets"]}; '
             f'closed targets: {s["closed_targets"]}; last target with a record: {s["last_done_target"]}; last scored: '
             f'{s["last_scored_target"]}']
    if s.get('joined_since_last_session') or s.get('left_since_last_session'):
        lines.append(f'[WEEKLY-FORECAST]   roster since the last session: {len(s["joined_since_last_session"])} joined, '
                     f'{len(s["left_since_last_session"])} left')
    if s['backlog']:
        for b in s['backlog']:
            lines.append(f'[WEEKLY-FORECAST]   backlog: draw {b["target"]} {b["status"]}: {b["state"]}'
                         + (f' ({b["unscored"]} record(s) unscored)' if b['unscored'] else ''))
    else:
        lines.append('[WEEKLY-FORECAST]   backlog: none (every accepted draw after the holdout is closed)')
    lines.append(f'[WEEKLY-FORECAST]   next target: draw {s["next_target"]} on {s["next_target_date"]}; deadline '
                 f'{s["next_deadline_utc"]} (local offset {s["next_deadline_offset_minutes"]} minutes); {s["next_state"]}')
    if s['diagnostic_records']:
        lines.append(f'[WEEKLY-FORECAST]   diagnostic records (unofficial, never scored into a ledger): {s["diagnostic_records"]}')
    return lines
