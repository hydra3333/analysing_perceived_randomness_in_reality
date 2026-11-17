"""MHUP-B test fixtures: a temporary project in weekly operation (design v0.1r7 section 6). Everything is INVENTED: the
masters, the owner records, the clock and the release dates. No real draw is read or written.

`Weekly` is a TestCase base that builds, for one game: an invented master grown past the holdout, the opening record,
the developed record, a small cohort (E_6's three variants by default) with release dates the test chooses, and a
clock the test moves. It patches, in-process and only for the test: the runner's and the dispatch gate's project root,
the orphan marker, the cohort and the released set, the session's closure and environment digests, the weekly clock
(now, local midnight) and the publication clock. The production APIs take no such arguments.

Two independently written oracles (R-4; design Appendix L) live here: `oracle_chain_ok` (a chain checker that shares no
code with jsonl_ledger) and `oracle_closed_targets` (which targets are closed, from lines, and score lines alone).
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

import mhupa_fixtures as X
import _common.contract_dispatch as CD
import _common.contract_publication as CP
import _common.contract_runner as CR
import _common.release_records as RR
import _common.walk_forward as WF
import _common.weekly_records as WR
import _common.weekly_session as WS
from _common import jsonl_ledger as JL
from _common import owner_records as OR
from _common.game_profiles import get_profile

ADELAIDE_DAYLIGHT = timezone(timedelta(hours=10, minutes=30))
_real_cohort = WF.cohort


def adapters():
    import Method_Contract_Runner as M
    return M.ADAPTERS


class Boom(Exception):
    """The injected fault of the interruption harness."""


class Weekly(unittest.TestCase):
    GAME = 'POWERBALL'
    EXTRA = 2                                    # invented accepted draws after the holdout
    METHODS = ('E_6',)
    RELEASED = '2026-01-01'                      # before every post-holdout draw date: CATCH_UP and FINAL_NEXT_DRAW

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.td = Path(self._td.name)
        self.proj = self.td / 'project'
        self.p = get_profile(self.GAME)
        self.first = self.p.holdout_last + 1                 # the first weekly target
        self.versions = [list(range(self.p.holdout_first, self.p.holdout_last + 1 + self.EXTRA))]
        self.rows = X.grow_master(self.proj, self.p, self.versions)
        X.write_opening_record(self.proj, self.GAME, freeze_version=1, freeze_sha=self.rows[0]['master_sha256'])
        # the game's Mode H study is sealed and the system declared developed (stage S5 of Appendix E)
        self.seal_and_declare()
        self.methods = set(self.METHODS)
        self.release_dates = {}                               # (method, variant) -> date, overriding RELEASED
        self.digests = ('c' * 64, 'e' * 64)
        self.now = self.at(self.first + self.EXTRA, hours_before=30)     # well before the next draw's deadline
        self.stack = contextlib.ExitStack()
        for obj, name, value in (
                (CR, 'PROJECT_ROOT', self.proj), (CD, 'PROJECT_ROOT', self.proj),
                (CR, 'ORPHAN_MARKER', self.proj / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'),
                (WF, 'cohort', self._cohort), (RR, 'released_variants', self._released),
                (WS, '_digests', lambda: self.digests), (WR, 'now_utc', self._now),
                (WR, 'local_midnight', lambda d: datetime(d.year, d.month, d.day, tzinfo=ADELAIDE_DAYLIGHT)),
                (CP, 'utc_now', lambda: WR.utc_text(self._now()))):
            self.stack.enter_context(mock.patch.object(obj, name, value))

    def tearDown(self):
        self.stack.close()
        self._td.cleanup()

    BATCH = 'wf-' + 'a' * 32
    SCORE_DIGEST = 'b' * 64

    def seal_and_declare(self):
        """The game's one Mode H plan with its four lifecycle markers, written through the installed marker writer (so
        each has its real shape and order), and the developed record as `declare-developed` writes it."""
        plan = X.write_mode_h_plan(self.proj, self.GAME, self.BATCH, [], [], pin=(2, self.rows[1]['master_sha256']),
                                   manifest_sha=X.write_study_manifest(self.proj, self.GAME))
        for name in OR.LIFECYCLE_MARKERS:
            OR.write_marker(self.proj, self.GAME, self.BATCH, name, {
                'schema': OR.MARKER_SCHEMAS[name], 'batch_id': self.BATCH, 'game_id': self.GAME,
                'utc': '2026-11-15T00:00:00.000000Z', 'plan_digest': X.record_digest(plan), 'pairs': 1,
                'attempt_id': 'mh-fixture', 'roster_digest': 'a' * 64, 'score_ledger_sha256': self.SCORE_DIGEST,
                'report_sha256': 'c' * 64})
        self.write_developed()

    def write_developed(self, **change):
        rec = {'schema': OR.DEVELOPED_SCHEMA, 'game': self.GAME, 'declared_utc': '2026-11-16T00:00:00.000000Z',
               'owner_statement': OR.DEVELOPED_STATEMENT, 'mode_h_score_digest': self.SCORE_DIGEST,
               'mode_h_batch_id': self.BATCH, 'mode_h_score_attempt_id': 'mh-fixture'}
        rec.update(change)
        path = OR.developed_record_path(self.proj, self.GAME)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(X.canonical(rec))
        return rec

    # ------------------------------------------------------------ the patched facts
    def _now(self):
        self.now += timedelta(milliseconds=1)                # every reading is later than the one before
        return self.now

    def at(self, target, *, hours_before=0.0, minutes_before=0.0):
        """The instant `hours_before` (or minutes) before the target's deadline (00:00 Adelaide daylight time)."""
        d = self.p.derived_date(target)
        dl = datetime(d.year, d.month, d.day, tzinfo=ADELAIDE_DAYLIGHT).astimezone(timezone.utc)
        return dl - timedelta(hours=hours_before, minutes=minutes_before)

    def _cohort(self, game_id, adapters_):
        members, excluded = _real_cohort(game_id, adapters_)
        return [m for m in members if m['method_id'] in self.methods], excluded

    def _released(self, root):
        members, _excluded = _real_cohort(self.GAME, adapters())
        return {(self.GAME, m['method_id'], m['method_revision'], m['variant_id']):
                self.release_dates.get((m['method_id'], m['variant_id']), self.RELEASED)
                for m in members if m['method_id'] in self.methods}

    # ------------------------------------------------------------ the master
    def grow(self, *more):
        """Append one ledger version per argument (a list of draws, or None for NO_CHANGE); earlier versions keep
        their bytes."""
        self.versions = [*self.versions, *more]
        self.rows = X.grow_master(self.proj, self.p, self.versions)
        return self.rows

    @property
    def last_draw(self):
        return self.rows[-1]['last_draw']

    # ------------------------------------------------------------ the two halves, and the sequencer's loop
    def open(self, **kw):
        return WS.open_session(self.GAME, adapters(), **kw)

    def next(self, sid, out=None):
        return WS.next_step(self.GAME, sid, adapters(), echo=(out.append if out is not None else lambda s: None))

    def score(self, sid, target, out=None):
        from evaluation import weekly_score
        return weekly_score.score(self.GAME, sid, target, echo=(out.append if out is not None else lambda s: None))

    def loop(self, sid):
        """What the weekly sequencer does: next and score in turn until a clean end. Returns the states."""
        states = []
        while True:
            state, target = self.next(sid)
            states.append((state, target))
            if state != 'FROZE':
                return states
            self.score(sid, target)

    def session(self):
        """One whole session: open, loop, close. Returns (session id, states)."""
        sid = self.open()['session_id']
        states = self.loop(sid)
        WS.close_session(self.GAME, sid)
        return sid, states

    def resume_token(self, sid, *, age=timedelta(seconds=10)):
        """What the process tool's CLEAN check writes (its record shape), dated `age` before now."""
        stamp = WR.utc_text(self.now - age)
        path = WR.sessions_folder(self.proj, self.GAME) / \
            f'RESUME_{sid}_{stamp.replace(":", "").replace("-", "").replace(".", "")}.json'
        rec = {'schema': OR.RESUME_TOKEN_SCHEMA, 'game_id': self.GAME, 'session_id': sid, 'utc': stamp,
               'process_table_sha256': '0' * 64, 'tool_version': 'fixture'}
        path.write_bytes((json.dumps(rec, sort_keys=True, separators=(',', ':')) + '\n').encode('ascii'))
        return path

    def clear_lock(self):
        """What the process tool's clear-session-lock does on CLEAN (the lock removed; every record stays)."""
        OR.session_lock_path(self.proj, self.GAME).unlink()

    # ------------------------------------------------------------ reading the records
    def lines(self):
        return WR.forecast_ledger(self.proj, self.GAME)

    def scores(self):
        return WR.score_ledger(self.proj, self.GAME)

    def tickets(self):
        return WR.session_tickets(self.proj, self.GAME)

    def run_folders(self):
        """Every run folder a session made: CATCH_UP and FINAL_NEXT_DRAW under the weekly root, a session's
        REAL_DEVELOPMENT runs under the development root (design 6.4). The fixture makes no other development run."""
        out = []
        for base in (OR.weekly_runs_root(self.proj), OR.development_runs_root(self.proj)):
            root = base / self.GAME
            out += [f for f in root.glob('*/*/*') if f.is_dir()] if root.is_dir() else []
        return sorted(out)

    def weekly_bytes(self):
        """Every file under the game's weekly folder and the weekly run root, by relative name."""
        out = {}
        for base in (OR.weekly_root(self.proj, self.GAME), OR.weekly_runs_root(self.proj),
                     OR.development_runs_root(self.proj)):
            if base.is_dir():
                for f in sorted(base.rglob('*')):
                    if f.is_file():
                        out[str(f.relative_to(self.proj))] = f.read_bytes()
        return out

    def science(self):
        """The run-id-free and time-free content of the final state: for every freeze line and score line, who was
        forecast for what, in which mode and class, with which content digest and which quantities."""
        lines = [(l['target_draw_number'], l['set_kind'], l['deadline_met'],
                  sorted((r['method_id'], r['method_revision'], r['variant_id'], r['run_mode'], r['record_kind'],
                          r['effective_class'], r['missing_batch'], r['scored_record_digest']) for r in l['records']))
                 for l in self.lines()]
        scores = sorted((s['target_draw_number'], s['method_id'], s['variant_id'], s['scored_record_digest'],
                         s['effective_class'], json.dumps(s['readouts'], sort_keys=True), json.dumps(s['rank'], sort_keys=True),
                         tuple(s['drawn_main']), s['drawn_powerball']) for s in self.scores())
        return lines, scores

    def done_counts(self):
        """(method, revision, variant, target) -> number of DONE tickets, over every session's ledger."""
        out = {}
        for rows in self.tickets().values():
            for t in rows:
                if t['kind'] == 'DONE':
                    out[OR.pair_of(t)] = out.get(OR.pair_of(t), 0) + 1
        return out


# ---------------------------------------------------------------- the interruption harness

@contextlib.contextmanager
def fault_after(k: int):
    """Raise Boom at the k-th durable step (counted from 1) of the weekly path: every ledger append and every contract
    run. `fault_after(0)` only counts. Yields a list whose length is the number of steps taken."""
    import evaluation.weekly_score as SC
    steps = []
    real_append, real_run = JL.append, CR.run_contract_method

    def step(kind):
        steps.append(kind)
        if k and len(steps) == k:
            raise Boom(f'injected fault at step {k} ({kind})')

    def append(path, record):
        raw = real_append(path, record)
        step(f'append {Path(path).name.split("_")[0]} {record.get("kind") or record.get("schema")}')
        return raw

    def run(request, **kw):
        res = real_run(request, **kw)
        step('run')
        return res
    with contextlib.ExitStack() as stack:
        for mod in (WS.JL, SC.JL):
            stack.enter_context(mock.patch.object(mod, 'append', append))
        stack.enter_context(mock.patch.object(WS.CR, 'run_contract_method', run))
        yield steps


# ---------------------------------------------------------------- oracles (R-4), written without the package's code

def oracle_chain_ok(path: Path) -> bool:
    """True if every line of the ledger file names its 1-based number and the SHA-256 of the exact bytes of the line
    before it (None first). It hashes the file's own bytes, line by line."""
    raw = Path(path).read_bytes()
    if raw and not raw.endswith(b'\n'):
        return False
    prev = None
    for i, line in enumerate(raw.split(b'\n')[:-1], start=1):
        try:
            rec = json.loads(line.decode('ascii'))
        except ValueError:
            return False
        if rec.get('line_number') != i or rec.get('previous_line_digest') != prev:
            return False
        prev = hashlib.sha256(line + b'\n').hexdigest()
    return True


def oracle_closed_targets(forecast_ledger: Path, score_ledger: Path) -> set:
    """Which targets are closed, from the two ledger files alone: a target is closed when, for every record its freeze
    line names, the score ledger holds a routine line for the same method, revision, variant, target and digest."""
    def rows(p):
        return [json.loads(x) for x in Path(p).read_text(encoding='ascii').splitlines()] if Path(p).exists() else []
    scored = {(s['method_id'], s['method_revision'], s['variant_id'], s['target_draw_number'], s['scored_record_digest'])
              for s in rows(score_ledger) if s['scoring_policy_id'] == 'WEEKLY_SCORE_POLICY_V1'}
    out = set()
    for line in rows(forecast_ledger):
        t = line['target_draw_number']
        if all((r['method_id'], r['method_revision'], r['variant_id'], t, r['scored_record_digest']) in scored
               for r in line['records']):
            out.add(t)
    return out
