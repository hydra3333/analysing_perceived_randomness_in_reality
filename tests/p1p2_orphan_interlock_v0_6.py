"""B2 uncaptured-status orphan interlock regressions: fakes only, NO real kills.

Loads the coordinator without running main(). All process observations are
stubbed; safety marker files are restricted to a TemporaryDirectory.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace

SOURCE = Path(__file__).resolve().parents[1] / 'src' / 'Powerball_Experiment_Coordinator.py'
spec = importlib.util.spec_from_file_location('coordinator_v06_fake_only', SOURCE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def fake_worker(run_dir: Path, exit_code: int | None = 7):
    # No captured descendants. The wrapper has exited without an experiment
    # ever entering the coordinator's ancestry inventory.
    return SimpleNamespace(
        sequence=1, run_id='fake_group_w001', run_dir=run_dir,
        proc=SimpleNamespace(pid=8521, poll=lambda: exit_code),
        root_create_time=100.0, experiment_member=None,
        unmatched_status='', ownership_errors=[], owned_members={},
        status_orphan_evidence=None, issue='', final_state=None)


def check():
    assert mod.ENABLE_PROCESS_TERMINATION is False
    original_marker = mod.UNRESOLVED_ORPHAN_MARKER
    original_same = mod.same_process
    with tempfile.TemporaryDirectory(prefix='p1p2_orphan_b2_fake_') as td:
        root = Path(td)
        marker = root / 'UNRESOLVED_ORPHAN.json'
        run_dir = root / 'run'
        run_dir.mkdir()
        mod.UNRESOLVED_ORPHAN_MARKER = marker
        calls = []
        try:
            def observed(pid, ctime):
                calls.append((pid, ctime))
                return True
            mod.same_process = observed  # Never queries real PIDs.

            def publish_status(*, pid=55601, ctime=500.25, run='fake_group_w001'):
                obj = {'run_id': run, 'pid': pid, 'state': 'STARTED'}
                if ctime != 'OMITTED':
                    obj['process_create_time_epoch'] = ctime
                (run_dir / 'status.json').write_text(json.dumps(obj), encoding='utf-8')

            # B2 blocker: wrapper exited nonzero; nothing captured; reported
            # experiment PID still alive. Now MUST mark, block and report.
            publish_status()
            w = fake_worker(run_dir, 7)
            with contextlib.redirect_stderr(io.StringIO()) as output:
                found, saved = mod.check_exited_worker_for_orphan(w, group_id='fake_group')
            assert found and saved and marker.is_file()
            assert w.final_state == 'ORPHAN_SUSPECTED'
            evidence = json.loads(marker.read_bytes())
            assert evidence['worker']['status_orphan_evidence']['pid'] == 55601
            assert evidence['worker']['status_orphan_evidence']['alive'] is True
            assert evidence['worker']['members'] == []
            assert 'SAFETY STOP' in output.getvalue()
            assert 'status is evidence only; NOT a kill target' in w.issue
            assert calls == [(55601, 500.25)]
            with contextlib.redirect_stderr(io.StringIO()) as blocked_output:
                try:
                    mod.require_no_unresolved_orphan()
                except RuntimeError:
                    pass
                else:
                    raise AssertionError('Marker did not block next start')
            blocked = blocked_output.getvalue()
            for essential in ('SAFETY STOP', 'PREVIOUS WORKER', 'fake_group_w001',
                              'pid=55601', 'ORIGINAL DETECTION', 'OPERATOR ACTION REQUIRED',
                              'NEVER kill', 'MARKER:', 'NO automatic acknowledgement/bypass'):
                assert essential in blocked, (essential, blocked)
            marker.unlink()

            # An identity that cannot be checked must also fail closed.
            mod.same_process = lambda pid, ctime: None if ctime is None else True
            publish_status(pid=55602, ctime='OMITTED')
            w = fake_worker(run_dir, 9)
            with contextlib.redirect_stderr(io.StringIO()):
                found, saved = mod.check_exited_worker_for_orphan(w, group_id='fake_group')
            assert found and saved and marker.exists()
            record = json.loads(marker.read_bytes())
            assert record['worker']['status_orphan_evidence']['create_time'] is None
            assert record['worker']['status_orphan_evidence']['alive'] is None
            marker.unlink()

            # Unknown liveness with a valid timestamp also blocks.
            mod.same_process = lambda pid, ctime: None
            publish_status(pid=55603, ctime=500.75)
            with contextlib.redirect_stderr(io.StringIO()):
                found, saved = mod.check_exited_worker_for_orphan(
                    fake_worker(run_dir, 3), group_id='fake_group')
            assert found and saved and marker.exists()
            marker.unlink()

            # Original PID positively gone or reused (ctime mismatch) is safe
            # to ignore when *no captured member* indicates a survivor.
            mod.same_process = lambda pid, ctime: False
            publish_status(pid=55604, ctime=501.25)
            w = fake_worker(run_dir, 5)
            found, saved = mod.check_exited_worker_for_orphan(w, group_id='fake_group')
            assert not found and saved and not marker.exists()

            # Stale/forged run ID, absent file, bool PID, and missing PID do
            # not establish matching status PID evidence.
            mod.same_process = lambda *_args: (_ for _ in ()).throw(
                AssertionError('Invalid status must not ask to inspect a PID'))
            for kwargs in ({'run': 'other_run'}, {'pid': True}, {'pid': 'abc'}):
                publish_status(**kwargs)
                found, saved = mod.check_exited_worker_for_orphan(
                    fake_worker(run_dir, 2), group_id='fake_group')
                assert not found and saved and not marker.exists(), kwargs
            (run_dir / 'status.json').unlink()
            found, saved = mod.check_exited_worker_for_orphan(
                fake_worker(run_dir, 2), group_id='fake_group')
            assert not found and saved and not marker.exists()

            # Still-active wrapper does not trigger exited-worker path.
            publish_status()
            w = fake_worker(run_dir, None)
            found, saved = mod.check_exited_worker_for_orphan(w, group_id='fake_group')
            assert not found and saved and not marker.exists()

            source = SOURCE.read_text(encoding='utf-8')
            assert 'if found_orphan:\n                        orphan_suspected = True\n                        stop_launches = True' in source
            assert 'if explanation.startswith("Probe PID not confirmed gone"):' not in source
            assert 'ENABLE_PROCESS_TERMINATION = False' in source
        finally:
            mod.same_process = original_same
            mod.UNRESOLVED_ORPHAN_MARKER = original_marker
    print('PASS: B2 exited-wrapper uncaptured status PID live/unknown -> marker; '
          'gone/mismatch/no-evidence -> no false marker; status never a kill target')
    print('NOT TESTED: Windows actual orphan discovery, real process termination, Ctrl+C')


if __name__ == '__main__':
    check()
