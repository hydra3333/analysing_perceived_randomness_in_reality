"""Engineering-only six-worker coordinator POC (Option F, NOT lottery prediction).

Launches only whitelisted POC probes through the existing Run_Experiment.bat.
No persistent services, Windows Job Objects, scientific E-method loading, or holdout data.
Windows proof-of-concept results, not Linux execution, determine acceptance.
"""
from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import signal
import subprocess
import sys
import threading
import time
import uuid
from typing import Any

try:
    import psutil
except ImportError as exc:
    raise SystemExit("[COORDINATOR] ERROR: psutil missing; run dependency .bat INSTALL") from exc

ROOT = Path(__file__).resolve().parent.parent
POC_DIR = ROOT / "transitory_data" / "poc_runs"
WRAPPER = ROOT / "Run_Experiment.bat"
SIMPLE_CASES = {"canonical-fixture", "echo-argv", "verbose", "exit-code"}
EXTRA_CASES = {"sleep-timeout", "cpu-load", "memory-load"}
CASE_NAMES = SIMPLE_CASES | EXTRA_CASES
SAFE_ID = re.compile(r"[A-Za-z0-9_-]{1,90}\Z")
SAFE_ARG = re.compile(r'[A-Za-z0-9_.,=:/\\ -]+\Z')
LINE_QUEUE_MAX = 8192
# OWNER SAFETY SWITCH. Default is NEVER terminate a process.
# Change to True ONLY after the documented N-series plan-only tests and owner review.
# A command-line argument CANNOT override this setting.
ENABLE_PROCESS_TERMINATION = False
ALLOWED_WRAPPER_DESCENDANTS = frozenset({"cmd.exe", "findstr.exe", "python.exe"})
ISO = lambda: datetime.now(timezone.utc).isoformat()


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save_new(destination: Path, content: bytes) -> None:
    """No overwrite: destinations must be unique; atomic rename on Windows."""
    tmp = destination.with_name(destination.name + ".part-" + uuid.uuid4().hex)
    try:
        with tmp.open("xb") as fh:
            fh.write(content)
            fh.flush()
            os.fsync(fh.fileno())
        # Windows must reject an existing destination. This is a W-test gate.
        os.rename(tmp, destination)
    finally:
        tmp.unlink(missing_ok=True)


def expected_venv() -> Path:
    return (ROOT / ".venv").resolve()


def verify_cmd_autorun() -> None:
    """Fail visibly rather than execute registry AutoRun during batch launches."""
    import winreg  # Windows-only module; imported only after the OS gate.
    key_name = r"Software\Microsoft\Command Processor"
    for root, label in ((winreg.HKEY_CURRENT_USER, "HKCU"),
                        (winreg.HKEY_LOCAL_MACHINE, "HKLM")):
        try:
            with winreg.OpenKey(root, key_name) as handle:
                try:
                    value, _kind = winreg.QueryValueEx(handle, "AutoRun")
                except FileNotFoundError:
                    continue
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise RuntimeError(f"Could not inspect {label} CMD AutoRun: {exc}") from exc
        if value:
            raise RuntimeError(f"CMD AutoRun configured in {label}\\{key_name}: "
                               "review system configuration before POC. No registry changes made.")


def validate_environment() -> None:
    if os.name != "nt":
        raise RuntimeError("Windows-only POC; Windows tests cannot be run on this host")
    expected = str(expected_venv()).casefold()
    actual = str(Path(sys.prefix).resolve()).casefold()
    if actual != expected:
        raise RuntimeError(f"Wrong venv: sys.prefix={sys.prefix}; expected={expected_venv()}")
    active_env = os.environ.get("VIRTUAL_ENV")
    if not active_env or str(Path(active_env).resolve()).casefold() != expected:
        raise RuntimeError("Coordinator requires VIRTUAL_ENV set to this project's .venv; "
                           "start via Run_Coordinator.bat instead of direct Python")
    if not WRAPPER.is_file():
        raise RuntimeError(f"Missing project experiment wrapper: {WRAPPER}")
    verify_cmd_autorun()


def safe_child_arg(value: str) -> str:
    if not SAFE_ARG.fullmatch(value):
        raise ValueError(f"Unsafe or unsupported CMD argument: {value!r}")
    return value


def capture_environment(folder: Path) -> None:
    """Record actual software versions; no mutation to installed dependencies."""
    completed = subprocess.run([sys.executable, "-m", "pip", "freeze"], cwd=ROOT,
                               capture_output=True, text=True, timeout=40, check=True)
    save_new(folder / "pip_freeze.txt", completed.stdout.encode("utf-8"))
    info = {"python": sys.version, "python_executable": sys.executable,
            "sys_prefix": sys.prefix, "psutil": psutil.__version__,
            "wrapper_sha256": sha256(WRAPPER.read_bytes()),
            "coordinator_sha256": sha256(Path(__file__).read_bytes()),
            "captured_utc": ISO()}
    save_new(folder / "runtime_environment.json", canonical_bytes(info))


def same_process(pid: int | None, creation_time: float | None) -> bool | None:
    """True=original PID is live; False=gone/reused; None=cannot determine."""
    if pid is None or creation_time is None:
        return None
    try:
        obj = psutil.Process(pid)
        if abs(obj.create_time() - creation_time) >= 0.5:
            return False  # PID reused: NEVER signal this new process.
        return obj.is_running() and obj.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False
    except (psutil.AccessDenied, OSError):
        return None


def read_status(directory: Path) -> dict[str, Any] | None:
    try:
        obj = json.loads((directory / "status.json").read_text(encoding="utf-8"))
        return obj if isinstance(obj, dict) else None
    except (OSError, json.JSONDecodeError, ValueError):
        return None


@dataclass
class OwnedMember:
    """Stored psutil object with ancestry checked while root wrapper was alive."""
    process: psutil.Process
    pid: int
    create_time: float
    name: str
    parent_pid: int
    depth: int


def _member_alive(member: OwnedMember) -> bool | None:
    """Keep the original Process object, so psutil rejects reused PIDs."""
    try:
        return member.process.is_running() and member.process.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False
    except (psutil.AccessDenied, OSError):
        return None


def _process_brief(member: OwnedMember) -> str:
    return (f"pid={member.pid} name={member.name} born={member.create_time:.6f} "
            f"parent_pid={member.parent_pid} depth={member.depth} alive={_member_alive(member)}")


def _root_brief(worker: "Worker") -> str:
    return (f"pid={worker.proc.pid} name=cmd.exe born={worker.root_create_time} "
            f"alive={worker.proc.poll() is None} (Popen handle)")


def register_root(worker: "Worker") -> None:
    """Immediately after Popen, record root identity; never trust a PID from disk."""
    try:
        root = psutil.Process(worker.proc.pid)
        born = root.create_time()
        name = root.name().lower()
        if name != "cmd.exe":
            worker.ownership_errors.append(f"WRONG_ROOT_NAME pid={root.pid} name={name}")
            return
        worker.root_process = root
        worker.root_create_time = born
    except (psutil.NoSuchProcess, psutil.AccessDenied, OSError) as exc:
        worker.ownership_errors.append(f"ROOT_IDENTITY_UNVERIFIED pid={worker.proc.pid}: {exc}")


def accept_ancestry_candidate(
        *, pid: int, parent_pid: int, born: float, name: str,
        known: dict[int, tuple[float, int]], allowed: frozenset[str]
) -> tuple[bool, str]:
    """Pure acceptance rule; usable in synthetic N4/N5 unit tests."""
    parent = known.get(parent_pid)
    if parent is None:
        return False, "PARENT_NOT_VERIFIED"
    if born < parent[0] - 0.001:
        return False, "CHILD_OLDER_THAN_PARENT"
    if name.lower() not in allowed:
        return False, "UNEXPECTED_EXECUTABLE"
    if pid in known:
        return False, "PID_ALREADY_REGISTERED"
    return True, "VERIFIED"


def capture_owned_tree(worker: "Worker", *, force: bool = False) -> None:
    """Capture descendants ONLY while Popen root is alive and has verified identity."""
    now = time.monotonic()
    if not force and now - getattr(worker, "last_capture_monotonic", 0.0) < 0.5:
        return
    worker.last_capture_monotonic = now
    if worker.root_process is None or worker.root_create_time is None:
        return
    if worker.proc.poll() is not None:
        return
    root = worker.root_process
    try:
        if not root.is_running() or abs(root.create_time() - worker.root_create_time) >= 0.001:
            worker.ownership_errors.append("ROOT_IDENTITY_CHANGED; no further capture")
            return
        snapshots = root.children(recursive=True)
    except (psutil.NoSuchProcess, psutil.AccessDenied, OSError) as exc:
        worker.ownership_errors.append(f"TREE_CAPTURE_ERROR: {exc}")
        return
    # Parent must be identified, not merely included in psutil's recursive snapshot.
    known = {root.pid: (worker.root_create_time, 0)}
    known.update({m.pid: (m.create_time, m.depth) for m in worker.owned_members.values()
                  if _member_alive(m) is not False})
    unprocessed = list(snapshots)
    for _ in range(len(unprocessed) + 1):
        if not unprocessed:
            break
        progress = False
        remaining = []
        for child in unprocessed:
            try:
                pid = child.pid
                parent_pid = child.ppid()
                born = child.create_time()
                name = child.name().lower()
            except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
                continue  # a transient exited before inspection; no kill authority
            previous = worker.owned_members.get(pid)
            if previous is not None:
                if abs(previous.create_time - born) < 0.001:
                    continue  # The very same already-verified member.
                old_alive = _member_alive(previous)
                if old_alive is False:
                    # Windows may reuse the PID of a short-lived wrapper/pre-check
                    # child.  The *stored* process object confirms that the old
                    # identity is gone; retire it without granting the new process
                    # any ownership.  The new candidate must still pass the full
                    # ancestry, creation-time and executable-name checks below.
                    worker.departed_members.append(previous)
                    del worker.owned_members[pid]
                    known.pop(pid, None)  # Never use a departed parent as proof.
                else:
                    # Both a live conflict and an unverifiable old identity fail
                    # closed.  Neither object is a new termination target.
                    worker.ownership_errors.append(
                        f"MEMBER_PID_IDENTITY_CONFLICT pid={pid} old_alive={old_alive}")
                    continue
            if parent_pid not in known:
                remaining.append(child)
                continue
            valid, why = accept_ancestry_candidate(
                pid=pid, parent_pid=parent_pid, born=born, name=name,
                known=known, allowed=ALLOWED_WRAPPER_DESCENDANTS)
            if not valid:
                worker.ownership_errors.append(f"{why}: pid={pid} name={name} parent={parent_pid}")
                continue
            member = OwnedMember(child, pid, born, name, parent_pid, known[parent_pid][1] + 1)
            worker.owned_members[pid] = member
            known[pid] = (born, member.depth)
            progress = True
        unprocessed = remaining
        if not progress:
            break
    for child in unprocessed:
        worker.ownership_errors.append(f"UNVERIFIED_PARENT descendant_pid={child.pid}")

    status = read_status(worker.run_dir)
    if status is None or status.get("run_id") != worker.run_id:
        return
    pid = status.get("pid")
    born = status.get("process_create_time_epoch")
    if type(pid) is not int or not isinstance(born, (float, int)):
        return
    found = worker.owned_members.get(pid)
    if found is not None and abs(found.create_time - float(born)) < 0.001:
        worker.experiment_member = found
        worker.unmatched_status = ""
    else:
        # STATUS PID IS NEVER ADDED TO THE TARGETS, including if a file changes later.
        worker.unmatched_status = f"STATUS_PID_NOT_OWNED pid={pid} born={born}"


def print_termination_plan(worker: "Worker", reason: str, *, preview: bool) -> None:
    """Safety BEFORE/AFTER reports for plan-only inspection; performs NO termination."""
    print(f"[SAFETY BEFORE] worker={worker.sequence:02d} reason={reason} "
          f"ENABLE_PROCESS_TERMINATION={ENABLE_PROCESS_TERMINATION} "
          f"mode={'PREVIEW_ONLY' if preview else 'STOP_REQUEST'}", flush=True)
    print(f"[SAFETY TARGET] root {_root_brief(worker)}", flush=True)
    for member in sorted(worker.owned_members.values(), key=lambda m: (-m.depth, m.pid)):
        print(f"[SAFETY TARGET] descendant {_process_brief(member)}", flush=True)
    print(f"[SAFETY PROOF] experiment_matched={worker.experiment_member is not None} "
          f"unmatched_status={worker.unmatched_status or 'none'} "
          f"ownership_anomalies={worker.ownership_errors or 'none'}", flush=True)
    if preview:
        print(f"[SAFETY AFTER] worker={worker.sequence:02d} PREVIEW ONLY; "
              "no termination attempted; workers continue normally", flush=True)


def terminate_owned_tree(worker: "Worker", reason: str) -> tuple[bool, str]:
    """Only stored, verified ancestry may be killed; protected by owner switch."""
    capture_owned_tree(worker, force=True)
    print_termination_plan(worker, reason, preview=False)
    if not ENABLE_PROCESS_TERMINATION or worker.plan_only:
        details = (f"TERMINATION_DISABLED: switch={ENABLE_PROCESS_TERMINATION} "
                   f"plan_only={worker.plan_only}, no signals issued; "
                   f"root_alive={worker.proc.poll() is None}; "
                   f"experiment_matched={worker.experiment_member is not None}")
        print(f"[SAFETY AFTER] worker={worker.sequence:02d} {details}", flush=True)
        return False, details
    # No destructive action if the wrapper or reported experiment wasn't verified.
    final_status = read_status(worker.run_dir)
    experiment = worker.experiment_member
    verified_status = (final_status is not None and
                       final_status.get("run_id") == worker.run_id and
                       experiment is not None and
                       final_status.get("pid") == experiment.pid and
                       isinstance(final_status.get("process_create_time_epoch"), (int, float)) and
                       abs(float(final_status["process_create_time_epoch"]) - experiment.create_time) < 0.001)
    if (worker.root_process is None or worker.root_create_time is None or
            not verified_status or worker.ownership_errors or worker.unmatched_status):
        details = "TERMINATION_REFUSED: root, experiment, or ancestry unverified; no signals issued"
        print(f"[SAFETY AFTER] worker={worker.sequence:02d} {details}", flush=True)
        return False, details
    actions: list[str] = []
    kill_requested: list[OwnedMember] = []
    live_members = sorted(worker.owned_members.values(), key=lambda m: (-m.depth, m.pid))
    for member in live_members:
        live = _member_alive(member)
        if live is not True:
            actions.append(f"pid={member.pid} not-signalled live={live}")
            continue
        print(f"[SAFETY ACTION] worker={worker.sequence:02d} KILL descendant "
              f"pid={member.pid} name={member.name} born={member.create_time:.6f}", flush=True)
        try:
            member.process.kill()  # psutil guards PID reuse via stored creation time
            kill_requested.append(member)
            actions.append(f"pid={member.pid} kill requested")
        except (psutil.NoSuchProcess, psutil.AccessDenied, OSError) as exc:
            actions.append(f"pid={member.pid} kill refused: {type(exc).__name__}: {exc}")
    if worker.proc.poll() is None:
        print(f"[SAFETY ACTION] worker={worker.sequence:02d} KILL root (Popen handle) "
              f"pid={worker.proc.pid} name=cmd.exe born={worker.root_create_time:.6f}", flush=True)
        try:
            worker.proc.kill()  # handle-based; never construct new kill PID
            actions.append(f"root_pid={worker.proc.pid} handle kill requested")
        except (OSError, subprocess.SubprocessError) as exc:
            actions.append(f"root_pid={worker.proc.pid} handle kill failed: {exc}")
    # TerminateProcess is asynchronous on Windows: a successful kill request
    # does NOT prove exit.  Wait on the *stored, verified* descendant objects,
    # with a firm bound, before checking survivors.  This never sends signals.
    wait_error: str | None = None
    if kill_requested:
        try:
            gone, still_alive = psutil.wait_procs(
                [m.process for m in kill_requested], timeout=3.0)
            actions.append(f"descendant_wait gone={len(gone)} alive={len(still_alive)}")
        except (psutil.Error, OSError, ValueError) as exc:
            wait_error = f"{type(exc).__name__}: {exc}"
            actions.append(f"descendant_wait failed={wait_error}")
    try:
        worker.proc.wait(timeout=3)
    except (subprocess.TimeoutExpired, OSError):
        pass
    # No kill escalation beyond verified members.  Only confirmed departures
    # count as stopped; ambiguous identities or wait failures fail closed.
    survivors = [m.pid for m in live_members if _member_alive(m) is not False]
    root_alive = worker.proc.poll() is None
    confirmed = (wait_error is None and not survivors and not root_alive
                 and _member_alive(worker.experiment_member) is False)
    state = "STOPPED_CONFIRMED" if confirmed else "ORPHAN_SUSPECTED"
    details = (f"{state}: actions={actions}; survivors={survivors}; "
               f"root_alive={root_alive}; wait_error={wait_error or 'none'}")
    print(f"[SAFETY AFTER] worker={worker.sequence:02d} {details}", flush=True)
    return confirmed, details


@dataclass
class Worker:
    sequence: int
    run_id: str
    proc: subprocess.Popen[str]
    started: float
    run_dir: Path
    stdout_log: Path
    reader: threading.Thread
    reader_done: threading.Event
    exit_code: int | None = None
    final_state: str | None = None
    issue: str = ""
    timed_out: bool = False
    stopped_cleanly: bool = False
    begin_seen: bool = False
    finish_success_seen: bool = False
    reader_error: bool = False
    console_result: str | None = None
    console_digest: str | None = None
    output_lines: int = 0
    latest_progress: str = ""
    lines_tail: deque[str] = field(default_factory=lambda: deque(maxlen=12))
    root_process: psutil.Process | None = None
    root_create_time: float | None = None
    owned_members: dict[int, OwnedMember] = field(default_factory=dict)
    # Historical identity evidence only; departed objects grant no kill authority.
    departed_members: list[OwnedMember] = field(default_factory=list)
    experiment_member: OwnedMember | None = None
    ownership_errors: list[str] = field(default_factory=list)
    unmatched_status: str = ""
    plan_printed: bool = False
    plan_only: bool = False
    last_capture_monotonic: float = 0.0


def read_lines(proc: subprocess.Popen[str], number: int, logfile: Path,
               messages: queue.Queue[tuple[int, str]], done: threading.Event) -> None:
    """Daemon reader prevents pipe EOF deadlock from hanging coordinator exit."""
    try:
        with logfile.open("x", encoding="utf-8", newline="\n") as fh:
            assert proc.stdout is not None
            for line in proc.stdout:
                fh.write(line)
                while not done.is_set():
                    try:
                        messages.put((number, line.rstrip("\r\n")), timeout=0.12)
                        break
                    except queue.Full:
                        continue
    except Exception as ex:
        try:
            messages.put_nowait((number, f"READER_ERROR: {ex}"))
        except queue.Full:
            pass
    finally:
        done.set()


def status_and_result(worker: Worker, *, require_success: bool) -> tuple[bool, str, dict | None]:
    status = read_status(worker.run_dir)
    if status is None:
        return False, "Missing or invalid status.json", None
    if status.get("run_id") != worker.run_id:
        return False, "Status run identity mismatch", status
    if str(status.get("sys_prefix", "")).casefold() != str(expected_venv()).casefold():
        return False, "Child sys.prefix does not match project venv", status
    if not isinstance(status.get("pid"), int):
        return False, "Child did not report its own PID", status
    if status.get("state") == "SUCCESS" and worker.exit_code != 0:
        return False, "Status says SUCCESS but subprocess nonzero", status
    if not require_success:
        if status.get("state") == "SUCCESS":
            return False, "Unexpected successful result on a failed/timeout run", status
        if (worker.run_dir / "canonical_result.json").exists():
            return False, "Unexpected canonical result exists on failed/timeout run", status
        return True, "Non-success correctly not published", status
    if worker.exit_code != 0 or status.get("state") != "SUCCESS":
        return False, f"exit={worker.exit_code}, status={status.get('state')}", status
    path = worker.run_dir / "canonical_result.json"
    try:
        raw = path.read_bytes()
        obj = json.loads(raw)
    except (OSError, json.JSONDecodeError) as ex:
        return False, f"Missing/bad canonical JSON: {ex}", status
    if raw != canonical_bytes(obj):
        return False, "Result JSON not in canonical byte format", status
    if not worker.begin_seen or not worker.finish_success_seen or worker.reader_error:
        return False, "Missing BEGIN/FINISH or pipe reader reported an error", status
    if worker.console_result is None or worker.console_digest is None:
        return False, "Missing RESULT/DIGEST console record", status
    if worker.console_result != raw.decode("utf-8").strip():
        return False, "Console RESULT differs from published JSON", status
    if worker.console_digest != sha256(raw):
        return False, "Console DIGEST differs from result bytes", status
    process_state = same_process(status.get("pid"), status.get("process_create_time_epoch"))
    if process_state is not False:
        return False, f"Probe PID not confirmed gone at completed run: {process_state}", status
    return True, "canonical result validated", status


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Windows Option F coordinator POC; no scientific methods")
    parser.add_argument("--poc", action="store_true", required=True)
    parser.add_argument("--case", choices=sorted(CASE_NAMES), default="canonical-fixture")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    parser.add_argument("--group-id", default=None)
    parser.add_argument("--lines", type=int, default=10)
    parser.add_argument("--exit", type=int, default=0)
    parser.add_argument("--exit-style", choices=("normal", "exception", "hard"), default="normal")
    parser.add_argument("--sleep-seconds", type=float, default=2.0)
    parser.add_argument("--cpu-seconds", type=float, default=1.0)
    parser.add_argument("--memory-mb", type=int, default=32)
    parser.add_argument("--allow-memory-stress", action="store_true")
    parser.add_argument("--min-available-gb", type=float, default=4.0)
    parser.add_argument("--critical-available-gb", type=float, default=2.0)
    parser.add_argument("--console-mode", choices=("all", "summary"), default="all")
    parser.add_argument("--plan-termination", action="store_true",
                        help="Print verified process inventory; do not signal any process")
    args = parser.parse_args()
    if not args.poc:
        parser.error("Only explicit --poc engineering runs are permitted")
    if not (1 <= args.workers <= 6):
        parser.error("--workers must be in 1..6")
    if not (1 <= args.count <= 100):
        parser.error("--count must be in 1..100")
    if not (1 <= args.timeout_seconds <= 7200):
        parser.error("--timeout-seconds must be in 1..7200")
    if not (0 <= args.lines <= 100_000):
        parser.error("--lines must be in 0..100000")
    if not (1 <= args.memory_mb <= 2048):
        parser.error("--memory-mb must be in 1..2048")
    if args.case == "memory-load" and args.memory_mb > 128 and not args.allow_memory_stress:
        parser.error("Memory allocations over 128 MB require --allow-memory-stress")
    if args.allow_memory_stress and not ENABLE_PROCESS_TERMINATION:
        parser.error("High memory stress disallowed while process termination is disabled")
    if args.plan_termination and args.case != "sleep-timeout":
        parser.error("--plan-termination first-release diagnostic requires --case=sleep-timeout")
    if args.plan_termination and args.timeout_seconds <= args.sleep_seconds + 2:
        parser.error("--plan-termination requires timeout > sleep duration + 2s; "
                     "no cleanup should be requested during a plan-only run")
    if args.min_available_gb <= args.critical_available_gb or args.critical_available_gb < 0:
        parser.error("Available-memory guard floors must be positive and ordered")
    if args.group_id is not None and (not SAFE_ID.fullmatch(args.group_id) or len(args.group_id) > 85):
        parser.error("--group-id must be 1..85 ASCII letters/digits/_/-")
    if args.case != "exit-code" and (args.exit != 0 or args.exit_style != "normal"):
        parser.error("--exit/--exit-style require case=exit-code")
    return args


def child_command(args: argparse.Namespace, run_id: str) -> list[str]:
    name = "POC_Architecture_Probe.py" if args.case in SIMPLE_CASES else "POC_Coordinator_Probe.py"
    output = [str(WRAPPER), name, "--poc", "--case=" + args.case, "--run-id=" + run_id]
    if args.case == "verbose":
        output.append(f"--lines={args.lines}")
    elif args.case == "exit-code":
        output.extend([f"--exit={args.exit}", f"--exit-style={args.exit_style}"])
    elif args.case == "sleep-timeout":
        output.append(f"--sleep-seconds={args.sleep_seconds}")
    elif args.case == "cpu-load":
        output.append(f"--cpu-seconds={args.cpu_seconds}")
    elif args.case == "memory-load":
        output.extend([f"--memory-mb={args.memory_mb}", f"--sleep-seconds={args.sleep_seconds}"])
    # Prevent CMD metacharacter injection, and never expand arbitrary filenames.
    for x in output[1:]:
        safe_child_arg(x)
    return output


def coordinator_main() -> int:
    args = arguments()
    validate_environment()
    POC_DIR.mkdir(parents=True, exist_ok=True)
    group_id = args.group_id or "coord-" + uuid.uuid4().hex
    group = POC_DIR / group_id
    group.mkdir(exist_ok=False)
    capture_environment(group)
    messages: queue.Queue[tuple[int, str]] = queue.Queue(maxsize=LINE_QUEUE_MAX)
    all_workers: list[Worker] = []
    active: dict[int, Worker] = {}
    next_number = 1
    started_utc = ISO()
    started = time.monotonic()
    peak_available_pressure = psutil.virtual_memory().available
    min_available = args.min_available_gb * 2**30
    critical = args.critical_available_gb * 2**30
    stop_launches = False
    interrupted = False
    orphan_suspected = False
    coordinator_issue = ""
    printed_lines = 0
    interrupt_requested = False

    def on_sigint(_signum: int, _frame: object) -> None:
        nonlocal interrupt_requested
        interrupt_requested = True  # flag only: no asynchronous KeyboardInterrupt

    old_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, on_sigint)

    def drain(limit: int = 6000) -> None:
        nonlocal printed_lines
        for _ in range(limit):
            try:
                number, line = messages.get_nowait()
            except queue.Empty:
                break
            w = all_workers[number - 1]
            w.output_lines += 1
            w.lines_tail.append(line)
            if line.startswith("BEGIN "):
                w.begin_seen = True
            elif line.startswith("FINISH ") and line.endswith(" SUCCESS"):
                w.finish_success_seen = True
            elif line.startswith("READER_ERROR:"):
                w.reader_error = True
            elif line.startswith("RESULT "):
                w.console_result = line[7:]
            elif line.startswith("DIGEST "):
                w.console_digest = line[7:]
            elif line.startswith("PROGRESS "):
                w.latest_progress = line
            if args.console_mode == "all" or not line.startswith("PROGRESS "):
                print(f"[WORKER {number:02d}] {line}", flush=True)
                printed_lines += 1

    def stop(worker: Worker, reason: str) -> None:
        nonlocal orphan_suspected, stop_launches
        good, info = terminate_owned_tree(worker, reason)
        worker.stopped_cleanly = good
        worker.issue = f"{reason}: {info}"
        worker.timed_out = reason == "TIMEOUT"
        worker.final_state = reason if good else (
            "TERMINATION_DISABLED" if not ENABLE_PROCESS_TERMINATION else "ORPHAN_SUSPECTED")
        if not good:
            orphan_suspected = True
            stop_launches = True
            print(f"[COORDINATOR] ERROR {worker.issue}", file=sys.stderr, flush=True)
        worker.exit_code = worker.proc.poll()

    try:
        print(f"[COORDINATOR] ENGINEERING POC group={group_id} "
              f"case={args.case} count={args.count} workers={args.workers}", flush=True)
        while active or (next_number <= args.count and not stop_launches):
            if interrupt_requested:
                interrupted = True
                stop_launches = True
                signal.signal(signal.SIGINT, signal.SIG_IGN)
                print("[COORDINATOR] INTERRUPTED; supervising active workers; "
                      f"termination_switch={ENABLE_PROCESS_TERMINATION}", flush=True)
                for w in list(active.values()):
                    stop(w, "INTERRUPTED")
                active.clear()
                break
            free_ram = psutil.virtual_memory().available
            peak_available_pressure = min(peak_available_pressure, free_ram)
            if free_ram < critical:
                stop_launches = True
                coordinator_issue = f"Critical available memory floor reached: {free_ram / 2**30:.2f} GiB"
                for w in list(active.values()):
                    if w.final_state is None:
                        stop(w, "MEMORY_GUARD")
            while not stop_launches and len(active) < args.workers and next_number <= args.count:
                if psutil.virtual_memory().available < min_available:
                    stop_launches = True
                    coordinator_issue = "Available memory below admission floor; no further workers launched"
                    print("[COORDINATOR] " + coordinator_issue, file=sys.stderr, flush=True)
                    break
                n = next_number
                run_id = f"{group_id}_w{n:03d}"
                if not SAFE_ID.fullmatch(run_id):
                    raise ValueError("Group ID leaves no room for worker suffix")
                run_dir = POC_DIR / run_id
                if run_dir.exists():
                    raise FileExistsError(f"Worker run directory already exists: {run_dir}")
                command = child_command(args, run_id)
                proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        stdin=subprocess.DEVNULL, text=True, encoding="utf-8",
                                        errors="replace", bufsize=1, cwd=ROOT, shell=False)
                reader_done = threading.Event()
                logfile = group / f"worker_{n:03d}.stdout.log"
                reader = threading.Thread(target=read_lines,
                                          args=(proc, n, logfile, messages, reader_done),
                                          daemon=True, name=f"worker-output-{n}")
                w = Worker(n, run_id, proc, time.monotonic(), run_dir, logfile, reader, reader_done)
                w.plan_only = args.plan_termination
                all_workers.append(w)
                active[n] = w  # immediate registration before any blocking operation
                register_root(w)
                capture_owned_tree(w)
                reader.start()
                next_number += 1
                print(f"[COORDINATOR] launched worker={n:02d} root_pid={proc.pid}", flush=True)
            drain()
            for n, w in list(active.items()):
                if w.final_state is None:
                    capture_owned_tree(w)
                    if (args.plan_termination and not w.plan_printed and
                            (w.experiment_member is not None or
                             time.monotonic() - w.started > 2)):
                        print_termination_plan(w, "PLAN_ONLY", preview=True)
                        w.plan_printed = True
                if w.final_state is not None:
                    active.pop(n)
                    continue
                if w.proc.poll() is None and time.monotonic() - w.started > args.timeout_seconds:
                    stop(w, "TIMEOUT")
                    active.pop(n)
                    continue
                if w.proc.poll() is not None:
                    w.exit_code = w.proc.returncode
                    w.final_state = "EXITED"
                    active.pop(n)
            time.sleep(0.04)
    except Exception as exc:
        stop_launches = True
        coordinator_issue = f"Coordinator error: {type(exc).__name__}: {exc}"
        print("[COORDINATOR] ERROR " + coordinator_issue, file=sys.stderr, flush=True)
        for w in list(active.values()):
            stop(w, "COORDINATOR_ERROR")
        active.clear()
    finally:
        # Keep SIGINT ignored through final manifest publication after interruption.
        if not interrupted:
            signal.signal(signal.SIGINT, old_handler)
        # Always drain pending logs, and never wait indefinitely for a pipe EOF.
        cutoff = time.monotonic() + 3.0
        while time.monotonic() < cutoff:
            drain()
            if all(w.reader_done.is_set() for w in all_workers) and messages.empty():
                break
            time.sleep(0.04)
        drain(100000)
        stuck_readers = [w.sequence for w in all_workers if not w.reader_done.is_set()]
        if stuck_readers:
            orphan_suspected = True
            coordinator_issue += f" Reader pipe(s) still open: {stuck_readers}"
            print(f"[COORDINATOR] ORPHAN_SUSPECTED reader threads {stuck_readers}",
                  file=sys.stderr, flush=True)
        for w in all_workers:
            w.reader.join(timeout=0.05)  # Never wait indefinitely for a pipe EOF.
            if w.proc.stdout is not None and w.reader_done.is_set():
                w.proc.stdout.close()

    reports = []
    total_successes = 0
    for w in all_workers:
        ok, explanation, status = status_and_result(w, require_success=w.final_state == "EXITED" and w.exit_code == 0)
        if w.final_state == "EXITED" and w.exit_code == 0 and ok:
            state = "SUCCESS"
            total_successes += 1
        else:
            state = w.final_state or "UNKNOWN"
            if state == "EXITED":
                state = "FAILED" if w.exit_code else "INVALID_RESULT"
            if not ok:
                explanation = explanation or "Run rejected"
        reports.append({"sequence": w.sequence, "run_id": w.run_id, "state": state,
                        "wrapper_pid": w.proc.pid, "experiment_pid": status.get("pid") if status else None,
                        "experiment_create_time_epoch": status.get("process_create_time_epoch") if status else None,
                        "exit_code": w.exit_code, "elapsed_seconds": time.monotonic() - w.started,
                        "status_state": status.get("state") if status else None,
                        "cpu_seconds": status.get("cpu_time_seconds") if status else None,
                        "peak_working_set_bytes": status.get("peak_working_set_bytes") if status else None,
                        "peak_memory_field": status.get("peak_field") if status else None,
                        "output_lines": w.output_lines,
                        "console_integrity": bool(ok and state == "SUCCESS"),
                        "failure_handling_valid": bool(ok) if state != "SUCCESS" else None,
                        "validation": explanation, "issue": w.issue,
                        "owned_processes": [{"pid": m.pid, "name": m.name,
                                              "create_time": m.create_time,
                                              "parent_pid": m.parent_pid, "depth": m.depth}
                                             for m in w.owned_members.values()],
                        "ownership_errors": w.ownership_errors,
                        "unmatched_status": w.unmatched_status,
                        "stdout_log": str(w.stdout_log.relative_to(ROOT)),
                        "result_path": str((w.run_dir / "canonical_result.json").relative_to(ROOT))})
    successful = (total_successes == args.count and len(all_workers) == args.count
                  and not interrupted and not orphan_suspected and not coordinator_issue)
    final = {"schema": "ENGINEERING_COORDINATOR_POC_V1", "engineering_only": True,
             "group_id": group_id, "case": args.case, "workers_maximum": args.workers,
             "count_requested": args.count, "count_started": len(all_workers),
             "successes": total_successes, "success": successful,
             "status": "PASS" if successful else "FAIL",
             "started_utc": started_utc, "finished_utc": ISO(),
             "elapsed_seconds": time.monotonic() - started,
             "minimum_observed_available_memory_bytes": peak_available_pressure,
             "interrupted": interrupted, "orphan_suspected": orphan_suspected,
             "enable_process_termination": ENABLE_PROCESS_TERMINATION,
             "issue": coordinator_issue, "workers": reports}
    save_new(group / "manifest.json", canonical_bytes(final))
    print(f"[COORDINATOR] {'PASS' if successful else 'FAIL'} successes={total_successes}/{args.count}; "
          f"manifest={group / 'manifest.json'}", flush=True)
    return 130 if interrupted else (0 if successful else 1)


if __name__ == "__main__":
    try:
        raise SystemExit(coordinator_main())
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"[COORDINATOR] ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
