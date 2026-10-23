"""Nondestructive regression of ownership PID recycling and bounded stop wait.

Runs entirely on synthetic objects; NEVER starts a child or signals an OS PID.
The true kill path is exercised only on fake processes with mocked wait_procs.
"""
from __future__ import annotations

import contextlib
from io import StringIO
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace

root = Path(__file__).resolve().parent.parent
path = root / "src" / "Powerball_Experiment_Coordinator.py"
spec = importlib.util.spec_from_file_location("poc_coordinator_v03_safety", path)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

assert mod.ENABLE_PROCESS_TERMINATION is False, "Owner kill switch must default to False"


class FakeProcess:
    def __init__(self, pid: int, parent: int, birth: float, name: str) -> None:
        self.pid = pid
        self.parent = parent
        self.birth = birth
        self.executable = name
        self.alive = True
        self.kills = 0
        self.children_list = []

    def is_running(self): return self.alive
    def status(self): return "running" if self.alive else "zombie"
    def create_time(self): return self.birth
    def ppid(self): return self.parent
    def name(self): return self.executable
    def children(self, recursive=True): return list(self.children_list)

    def kill(self):
        # This function is ONLY defined on synthetic FakeProcess objects.
        self.kills += 1
        assert self.kills == 1
        # Deliberately leave alive=True; mocked wait_procs confirms it later.


class FakePopen:
    def __init__(self, pid: int):
        self.pid = pid
        self.alive = True
        self.kills = 0
        self.waits = 0

    def poll(self): return None if self.alive else 1
    def kill(self):
        self.kills += 1
        self.alive = False

    def wait(self, timeout):
        assert timeout == 3
        self.waits += 1
        return 1


def worker_for(root_process, popen):
    return SimpleNamespace(
        sequence=1, run_id="synthetic_v03", proc=popen,
        root_process=root_process, root_create_time=root_process.birth,
        owned_members={}, departed_members=[], ownership_errors=[],
        experiment_member=None, unmatched_status="", run_dir=root / "does_not_exist",
        plan_only=False, last_capture_monotonic=0.0,
    )

old_read_status = mod.read_status
old_wait_procs = mod.psutil.wait_procs
try:
    # A. Old transient member vanished and a *different* member has its PID.
    root_process = FakeProcess(1000, 0, 100.0, "cmd.exe")
    popen = FakePopen(1000)
    w = worker_for(root_process, popen)
    old = FakeProcess(2000, 1000, 101.0, "python.exe")
    root_process.children_list = [old]
    mod.read_status = lambda _dir: None
    mod.capture_owned_tree(w, force=True)
    assert w.owned_members[2000].process is old
    old.alive = False
    replacement = FakeProcess(2000, 1000, 105.0, "python.exe")
    root_process.children_list = [replacement]
    mod.read_status = lambda _dir: {
        "run_id": w.run_id, "pid": 2000, "process_create_time_epoch": 105.0}
    mod.capture_owned_tree(w, force=True)
    assert w.owned_members[2000].process is replacement
    assert len(w.departed_members) == 1 and w.departed_members[0].process is old
    assert w.experiment_member is w.owned_members[2000]
    assert not w.ownership_errors and not w.unmatched_status, w.ownership_errors
    assert old.kills == replacement.kills == popen.kills == 0

    # B. Reused PID while the old identity is still believed alive: refuse.
    root2 = FakeProcess(1001, 0, 200.0, "cmd.exe")
    p2 = FakePopen(1001)
    w2 = worker_for(root2, p2)
    still_alive = FakeProcess(3000, 1001, 201.0, "python.exe")
    root2.children_list = [still_alive]
    mod.read_status = lambda _dir: None
    mod.capture_owned_tree(w2, force=True)
    conflicting = FakeProcess(3000, 1001, 202.0, "python.exe")
    root2.children_list = [conflicting]
    mod.capture_owned_tree(w2, force=True)
    assert w2.owned_members[3000].process is still_alive
    assert not w2.departed_members
    assert any("MEMBER_PID_IDENTITY_CONFLICT" in e for e in w2.ownership_errors)
    assert not still_alive.kills and not conflicting.kills and not p2.kills

    # C. Global switch False blocks kill calls (regardless of verified ancestry).
    mod.read_status = lambda _dir: {
        "run_id": w.run_id, "pid": 2000, "process_create_time_epoch": 105.0}
    text = StringIO()
    with contextlib.redirect_stdout(text):
        confirmed, explanation = mod.terminate_owned_tree(w, "SYNTHETIC_DISABLED")
    assert not confirmed and "TERMINATION_DISABLED" in explanation
    assert "[SAFETY BEFORE]" in text.getvalue() and "[SAFETY AFTER]" in text.getvalue()
    assert replacement.kills == popen.kills == 0

    # D. For coverage ONLY: synthetic, in-memory switch True, fake PIDs/objects.
    # This does NOT modify the source flag, create or kill any Windows process.
    observed = []
    def fake_wait_procs(processes, timeout):
        assert timeout == 3.0
        observed.append((processes[:], timeout))
        assert processes == [replacement]
        assert replacement.kills == 1, "wait must follow a kill request"
        replacement.alive = False
        return [replacement], []

    mod.psutil.wait_procs = fake_wait_procs
    mod.ENABLE_PROCESS_TERMINATION = True
    text = StringIO()
    with contextlib.redirect_stdout(text):
        confirmed, explanation = mod.terminate_owned_tree(w, "SYNTHETIC_WAIT")
    assert confirmed, explanation
    assert "STOPPED_CONFIRMED" in explanation
    assert "descendant_wait gone=1 alive=0" in explanation
    assert observed and popen.kills == 1 and popen.waits == 1
    assert replacement.kills == 1 and old.kills == 0
    assert "[SAFETY BEFORE]" in text.getvalue() and "[SAFETY AFTER]" in text.getvalue()
finally:
    mod.ENABLE_PROCESS_TERMINATION = False
    mod.read_status = old_read_status
    mod.psutil.wait_procs = old_wait_procs

assert mod.ENABLE_PROCESS_TERMINATION is False
print("PASS: v0.3 PID reuse retirement, alive-collision refusal, disabled kill, bounded wait (fakes only)")
print("NOT TESTED: actual Windows force termination, CTRL+C, or process-tree cleanup")
