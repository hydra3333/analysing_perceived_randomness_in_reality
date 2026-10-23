"""Platform-neutral *non-destructive* coordinator ownership tests. No subprocess starts or kills."""
from __future__ import annotations
import contextlib
from io import StringIO
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace

root = Path(__file__).resolve().parent.parent
path = root / "src" / "Powerball_Experiment_Coordinator.py"
spec = importlib.util.spec_from_file_location("poc_safe_coordinator_module", path)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

assert mod.ENABLE_PROCESS_TERMINATION is False, "Owner safety switch must default to False"
assert not any("taskkill" in x for x in path.read_text("utf-8").lower().splitlines()
               if not x.lstrip().startswith("#")), "No taskkill fallback"
known = {1000: (100.0, 0), 2000: (101.0, 1)}
for pid, parent, birth, name, expected, reason in [
    (3000, 2000, 102, "python.exe", True, "VERIFIED"),
    (3000, 2000, 102, "findstr.exe", True, "VERIFIED"),
    (3000, 2000, 102, "cmd.exe", True, "VERIFIED"),
    (3000, 2000, 102, "chcp.com", False, "UNEXPECTED_EXECUTABLE"),
    (3000, 2000, 102, "notepad.exe", False, "UNEXPECTED_EXECUTABLE"),
    (3000, 9000, 102, "python.exe", False, "PARENT_NOT_VERIFIED"),
    (3000, 2000, 99, "python.exe", False, "CHILD_OLDER_THAN_PARENT"),
    (2000, 1000, 102, "python.exe", False, "PID_ALREADY_REGISTERED"),
]:
    yes, why = mod.accept_ancestry_candidate(pid=pid, parent_pid=parent,
        born=birth, name=name, known=known,
        allowed=mod.ALLOWED_WRAPPER_DESCENDANTS)
    assert (yes, why) == (expected, reason), (pid, name, yes, why)

class FakeProcess:
    def __init__(self, pid, parent, birth, name):
        self.pid, self.parent, self.birth, self.executable = pid, parent, birth, name
        self.kills = 0
    def is_running(self): return True
    def status(self): return "running"
    def create_time(self): return self.birth
    def ppid(self): return self.parent
    def name(self): return self.executable
    def children(self, recursive=True): return [child]
    def kill(self):
        self.kills += 1
        raise AssertionError("KILL CALLED WITH FALSE OWNER SWITCH")

parent = FakeProcess(1000, 888, 100, "cmd.exe")
child = FakeProcess(2000, 1000, 101, "python.exe")
root_proc = SimpleNamespace(pid=1000, poll=lambda: None)
worker = SimpleNamespace(sequence=1, run_id="safety_test", proc=root_proc,
    root_process=parent, root_create_time=100.0, owned_members={},
    ownership_errors=[], experiment_member=None, unmatched_status="",
    run_dir=root / "does_not_exist", plan_only=False)

original_read_status = mod.read_status
try:
    # N2: valid ancestry but malicious status naming an unrelated decoy PID.
    mod.read_status = lambda folder: {"run_id": "safety_test", "pid": 9000,
                                     "process_create_time_epoch": 200.0}
    mod.capture_owned_tree(worker, force=True)
    assert sorted(worker.owned_members) == [2000]
    assert worker.experiment_member is None
    assert worker.unmatched_status.startswith("STATUS_PID_NOT_OWNED")
    assert 9000 not in worker.owned_members
    # Matching status later verifies actual captured member, clearing stale mismatch.
    mod.read_status = lambda folder: {"run_id": "safety_test", "pid": 2000,
                                     "process_create_time_epoch": 101.0}
    mod.capture_owned_tree(worker, force=True)
    assert worker.experiment_member is not None
    assert worker.unmatched_status == ""
    out = StringIO()
    with contextlib.redirect_stdout(out):
        success, explanation = mod.terminate_owned_tree(worker, "SYNTHETIC_TEST")
    report = out.getvalue()
    assert not success and "TERMINATION_DISABLED" in explanation
    assert "[SAFETY BEFORE]" in report and "[SAFETY AFTER]" in report
    assert "pid=1000 name=cmd.exe" in report and "pid=2000 name=python.exe" in report
    assert "switch=False plan_only=False, no signals issued" in report
    assert parent.kills == 0 and child.kills == 0
    # Even with switch toggled inside this SYNTHETIC test, plan-only cannot kill.
    mod.ENABLE_PROCESS_TERMINATION = True
    worker.plan_only = True
    more = StringIO()
    with contextlib.redirect_stdout(more):
        safe, message = mod.terminate_owned_tree(worker, "SYNTHETIC_PLAN_ONLY")
    assert not safe and "plan_only=True" in message
    assert parent.kills == 0 and child.kills == 0
    # With switch True and plan False, unverified status refuses even root killing.
    worker.plan_only = False
    mod.read_status = lambda folder: {"run_id":"wrong", "pid":2000,
                                     "process_create_time_epoch":101.0}
    more = StringIO()
    with contextlib.redirect_stdout(more):
        safe, message = mod.terminate_owned_tree(worker, "SYNTHETIC_UNVERIFIED")
    assert not safe and "TERMINATION_REFUSED" in message
    assert parent.kills == 0 and child.kills == 0
    mod.ENABLE_PROCESS_TERMINATION = False
    # N3: status with wrong run_id must not identify an experiment.
    worker.experiment_member = None
    mod.read_status = lambda folder: {"run_id":"wrong", "pid":2000,
                                     "process_create_time_epoch":101.0}
    mod.capture_owned_tree(worker, force=True)
    assert worker.experiment_member is None
finally:
    mod.read_status = original_read_status
    mod.ENABLE_PROCESS_TERMINATION = False

print("PASS: N2/N3 synthetic status, N4/N5 per-edge/name, owner switch False, BEFORE/AFTER, no kill")
print("NOT TESTED: actual Windows process ancestry, console handling, or destructive cleanup")
