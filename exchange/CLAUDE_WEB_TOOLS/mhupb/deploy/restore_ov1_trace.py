"""A design-stage TRACE for the deployment design note (EX_248 R3-B03). NOT project code, not a test, not installed.
It runs the STAGED, PASSED slice 3 tree (built from the repository copy) on the invented weekly project of
tests/mhupb_fixtures.py and tests/test_mhupb_ov1.py, and shows what the staged OV-1 recorder appends, in five cases,
when the invented project folder is put back to an earlier copy of itself ("restore") and the weekly work is done
again. Every draw, clock reading and release date is invented. Nothing here is a result.
Usage (from the built tree's root):  PYTHONPATH=src:src/methods:tests python3.15 -B <this file>
"""
import shutil, sys, unittest
import test_mhupb_ov1 as T
import _common.weekly_session as WS
from evaluation import ov1 as OV

OUT = []
def say(s=''): OUT.append(s)


class Trace(T.Stream):
    EXTRA = 0

    def snap(self, name):
        dst = self.td / f'snapshot_{name}'
        shutil.copytree(self.proj, dst)
        return dst, list(self.versions), self.now

    def restore(self, snap, *, now):
        """The owner's method: the old tree renamed aside, the snapshot unpacked at the same path. The clock is NOT put
        back: `now` is the real time of the restore."""
        dst, versions, _taken = snap
        aside = self.td / f'set_aside_{len(list(self.td.glob("set_aside_*")))}'
        self.proj.rename(aside)
        shutil.copytree(dst, self.proj)
        self.versions = list(versions)
        self.now = now
        return aside

    def show(self, title):
        say(f'  {title}')
        try:
            st = OV.status(self.GAME)
        except OV.OV1Refused as exc:
            say(f'    status: {exc}')
            return
        say(f'    OV-1 ledger: {[(k, t - self.m) for k, t in self.kinds()]}   (targets shown as M+n)')
        say(f'    status: counted {st.get("counted")}, missed {st.get("missed")}, score {st.get("score_text")}, '
            f'stopped {st.get("stopped")}')

    def factor(self, target):
        return next((r for r in self.ov1_rows() if r['kind'] == 'FACTOR' and r['target_draw_number'] == target), None)

    def science(self, row):
        return {k: v for k, v in row.items() if k not in ('written_utc', 'line_number', 'previous_line_sha256', 'line_sha256',
                                                             'previous_digest', 'digest', 'chain')}

    def three_weeks(self):
        self.register(); self.week()                    # freezes M before its cut-off
        self.result(self.m); self.week()                # FACTOR M, freezes M+1
        s2 = self.snap('after_week_2')
        self.result(self.m + 1); self.week()            # FACTOR M+1, freezes M+2
        s3 = self.snap('after_week_3')
        return s2, s3

    def test_a_nothing_lost(self):
        say('(a) No formal line lost: restore to the snapshot taken at the end of the last job.')
        _s2, s3 = self.three_weeks()
        before = self.ledger_bytes()
        self.restore(s3, now=self.now)
        say(f'    the OV-1 ledger after the restore equals the one before, byte for byte: {self.ledger_bytes() == before}')
        self.result(self.m + 2); self.week()
        self.show('after the next ordinary week')

    def test_b_only_a_factor_line_lost(self):
        say('(b) Only a FACTOR line lost; its pre-cut-off freeze and eligibility lines are in the snapshot.')
        self.register(); self.week(); self.result(self.m); self.week()
        s = self.snap('after_week_2')                   # holds ELIGIBILITY M+1 (and its CONFIRMED)
        self.result(self.m + 1)
        sid = self.open()['session_id']                 # the job that breaks: scores M+1, records its factor, then dies
        self.next(sid); self.score(sid, self.m + 1); self.record()
        lost = self.science(self.factor(self.m + 1))
        self.show('the old tree when it broke')
        self.restore(s, now=self.now)                   # before the cut-off of M+2
        self.grow([self.m + 1]); self.week()
        again = self.science(self.factor(self.m + 1))
        self.show('the restored tree after the results update and one weekly session')
        same = {k for k in lost if lost[k] == again.get(k)}
        say(f'    the re-derived FACTOR line for M+1: {len(same)} of {len(lost)} fields equal the lost line\'s; '
            f'different: {sorted(set(lost) - same)}')

    def test_c_a_counted_draw_lost_after_its_cutoff(self):
        say('(c) A pre-cut-off freeze and eligibility line lost, and the restore comes after that draw\'s cut-off.')
        s2, _s3 = self.three_weeks()
        self.result(self.m + 2); self.week()            # FACTOR M+2 (counted, genuinely frozen before its cut-off)
        self.show('the old tree before the restore')
        old_scores = {(s['method_id'], s['variant_id']): s['readouts'] for s in self.scores()
                      if s['target_draw_number'] == self.m + 2}
        self.restore(s2, now=self.now)                  # the snapshot predates the freeze of M+2; its cut-off has passed
        self.grow([self.m + 1], [self.m + 2]); states, wrote = self.week()
        say(f'    the replayed session: {[(s, t - self.m) for s, t in states]}')
        self.show('the restored tree after the results update and one weekly session')
        row = next(r for r in self.ov1_rows() if r['target_draw_number'] == self.m + 2)
        say(f'    M+2 is now a {row["kind"]} line: reason {row.get("reason")}, label {row.get("label")}')
        new = {(s['method_id'], s['variant_id']): (s['readouts'], s['effective_class']) for s in self.scores()
               if s['target_draw_number'] == self.m + 2}
        say(f'    ordinary scores of M+2 in the replay: {len(new)} variants; readouts equal to the old tree\'s for '
            f'{sum(1 for k in new if new[k][0] == old_scores.get(k))} of them; classes {sorted({v[1] for v in new.values()})}')
        say(f'    verify() on the restored tree: {OV.verify(self.GAME).get("state", "passes")}')

    def test_d_the_registration_is_not_in_the_snapshot(self):
        say('(d) The snapshot is older than the registration.')
        s0 = self.snap('before_registration')
        self.register(); self.week(); self.result(self.m); self.week()
        self.show('the old tree before the restore')
        self.restore(s0, now=self.now)
        say(f'    registration file present after the restore: {OV.registration_path(self.proj, self.GAME).exists()}')
        try:
            OV.record(self.GAME, echo=lambda s: None)
        except OV.OV1Refused as exc:
            say(f'    record (library call): refused, "{exc}"; the command answers NOT_REGISTERED, exit 0 (EX_239)')
        self.grow([self.m])
        try:                                            # typed straight after the restore and the results update
            r = self.register()
            say(f'    a second `register` typed before any session is ACCEPTED by the staged code '
                f'(first target M+{r["first_target"] - self.m}): the code cannot know of the first one')
        except Exception as exc:                        # noqa: BLE001
            say(f'    a second `register` typed before any session is refused: {exc}')
        self.restore(s0, now=self.now)
        self.grow([self.m]); states, _w = self.week(record=False)
        say(f'    one weekly session without the recorder: {[(s, t - self.m) for s, t in states]} (ordinary work goes on)')
        try:
            self.register()
            say('    a second `register` typed after that session is ACCEPTED')
        except Exception as exc:                        # noqa: BLE001
            say(f'    a second `register` typed after that session is refused by an existing rule: {exc}')

    def test_e_the_old_tree_cannot_be_read(self):
        say('(e) The set-aside tree cannot be read. The recorder never looks at it: what it appends in the restored tree is')
        say('    case (c)\'s, line for line. Any rule that needs the old tree\'s ledgers cannot be applied here.')


if __name__ == '__main__':
    suite = unittest.TestSuite(Trace(n) for n in sorted(x for x in dir(Trace) if x.startswith('test_')))
    res = unittest.TextTestRunner(stream=sys.stderr, verbosity=0).run(suite)
    print('\n'.join(OUT))
    print(f'\ntrace finished: {res.testsRun} cases, {len(res.failures)} failures, {len(res.errors)} errors; '
          f'python {sys.version.split()[0]}')
    for _t, tb in res.failures + res.errors:
        print(tb)
