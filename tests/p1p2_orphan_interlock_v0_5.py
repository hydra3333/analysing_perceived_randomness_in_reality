"""Synthetic, non-destructive interlock B1 regression for coordinator v0.5.

Uses fake processes only; never executes a real process kill or timeout.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import sys

SOURCE = Path(__file__).resolve().parents[1] / 'src' / 'Powerball_Experiment_Coordinator.py'
spec = importlib.util.spec_from_file_location('coordinator_v05_synthetic_target', SOURCE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def fake_member(pid: int, live: bool | None):
    def status():
        if live is None:
            raise mod.psutil.AccessDenied(pid=pid)
        return mod.psutil.STATUS_RUNNING
    proc = SimpleNamespace(is_running=lambda: live if live is not None else True,
                           status=status)
    return mod.OwnedMember(proc, pid, 111.25, 'python.exe', 987, 2)


def worker(member, *, exited=True):
    root = SimpleNamespace(pid=987, poll=lambda: 1 if exited else None)
    return SimpleNamespace(sequence=1, run_id='fake_group_w001',
                           run_dir=Path(tempfile.gettempdir()) / 'v05_synthetic_no_status_dir',
                           proc=root, root_create_time=100.0,
                           experiment_member=None, unmatched_status='',
                           ownership_errors=[], owned_members={member.pid:member},
                           final_state=None, issue='')


def check():
    assert mod.ENABLE_PROCESS_TERMINATION is False
    with tempfile.TemporaryDirectory(prefix='p1p2_orphan_v05_') as td:
        marker = Path(td) / 'UNRESOLVED_ORPHAN.json'
        old_marker = mod.UNRESOLVED_ORPHAN_MARKER
        old_save = mod.save_new
        try:
            mod.UNRESOLVED_ORPHAN_MARKER = marker
            # B1: exited wrapper with live OR unknown descendant publishes interlock.
            for live in (True, None):
                w = worker(fake_member(12345, live))
                with contextlib.redirect_stderr(io.StringIO()) as log:
                    found, saved = mod.check_exited_worker_for_orphan(w, group_id='fake_group')
                assert found and saved and w.final_state == 'ORPHAN_SUSPECTED'
                assert marker.exists()
                recorded = json.loads(marker.read_bytes())
                assert recorded['worker']['members'][0]['pid'] == 12345
                assert recorded['worker']['members'][0]['alive_at_record'] == live
                assert 'UNRESOLVED PROCESS' in log.getvalue()
                assert 'NEVER manually kill' in log.getvalue()
                assert 'archive' in log.getvalue().lower()
                preserved = marker.read_bytes()
                with contextlib.redirect_stderr(io.StringIO()):
                    try:
                        mod.require_no_unresolved_orphan()
                    except RuntimeError as exc:
                        assert 'UNRESOLVED_ORPHAN' in str(exc)
                    else:
                        raise AssertionError('Marker did not block')
                # A second incident must not overwrite the original marker.
                with contextlib.redirect_stderr(io.StringIO()):
                    found2, saved2 = mod.check_exited_worker_for_orphan(
                        worker(fake_member(12349, True)), group_id='another_group')
                assert found2 and saved2 and marker.read_bytes() == preserved
                marker.unlink()
            # A confirmed-departed child does not cause B1 marker.
            w = worker(fake_member(12346, False))
            found, saved = mod.check_exited_worker_for_orphan(w, group_id='fake_group')
            assert not found and saved and not marker.exists() and w.final_state is None
            # Still-active root must not trigger false exited-root B1.
            w = worker(fake_member(12347, True), exited=False)
            found, saved = mod.check_exited_worker_for_orphan(w, group_id='fake_group')
            assert not found and saved and not marker.exists()

            # Marker write failure is returned, operator sees CRITICAL, not swallowed.
            def raise_permission(_path, _raw):
                raise PermissionError('synthetic disk write refusal')
            mod.save_new = raise_permission
            with contextlib.redirect_stderr(io.StringIO()) as log:
                found, saved = mod.check_exited_worker_for_orphan(
                    worker(fake_member(12348, True)), group_id='fake_group')
            assert found and saved is False
            assert 'CRITICAL' in log.getvalue() and 'DO NOT RUN' in log.getvalue()
            assert not marker.exists()
            assert '"marker_write_failed": marker_write_failed' in SOURCE.read_text()
            assert 'if explanation.startswith("Probe PID not confirmed gone"):' not in SOURCE.read_text()
            assert 'stop_launches = True' in SOURCE.read_text()
            assert 'ENABLE_PROCESS_TERMINATION = False' in SOURCE.read_text()
        finally:
            mod.save_new = old_save
            mod.UNRESOLVED_ORPHAN_MARKER = old_marker
    print('PASS: exited-root live/unknown member -> marker; departed member not marked; '
          'marker failure CRITICAL; owner switch False (all fakes; zero signals)')
    print('NOT TESTED: Windows real-process exit and marker persistence, or destructive termination')


if __name__ == '__main__':
    check()
