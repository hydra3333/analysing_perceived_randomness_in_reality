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


def terminate_tree(proc: subprocess.Popen[str], status_file: Path,
                   *, wait_seconds: float = 8.0) -> tuple[bool, str]:
    """Snapshot descendants while root lives. Stop descendants then root.

    Returns (confirmed_stopped, explanation). Never kill a reused probe PID.
    Do not rely on Windows virtual-environment redirector internals.
    """
    prior = read_status(status_file.parent) or {}
    probe_pid = prior.get("pid") if isinstance(prior.get("pid"), int) else None
    born = prior.get("process_create_time_epoch")
    born = float(born) if isinstance(born, (float, int)) else None
    seen: dict[int, psutil.Process] = {}
    try:
        root = psutil.Process(proc.pid)
        if root.is_running():
            for child in root.children(recursive=True):
                seen[child.pid] = child
            seen[root.pid] = root
    except psutil.NoSuchProcess:
        pass
    except (psutil.AccessDenied, OSError) as exc:
        return False, f"Cannot enumerate child process tree: {exc}"

    # Include the child's directly self-reported PID even if the wrapper
    # died before enumeration. Only signal when PID+creation time match.
    probe_state = same_process(probe_pid, born)
    if probe_state is True and probe_pid not in seen:
        try:
            seen[probe_pid] = psutil.Process(probe_pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    targets = list(seen.values())
    # Children before CMD wrapper; psutil handles races and stale processes.
    targets.sort(key=lambda p: p.pid == proc.pid)
    for obj in targets:
        try:
            # Avoid killing a stale object whose PID has been reused.
            if obj.is_running():
                obj.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    _gone, alive = psutil.wait_procs(targets, timeout=wait_seconds / 2)
    for obj in alive:
        try:
            obj.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    _gone2, survivors = psutil.wait_procs(alive, timeout=wait_seconds / 2)
    try:
        proc.wait(timeout=1)
    except (subprocess.TimeoutExpired, OSError):
        pass
    still = same_process(probe_pid, born)
    if survivors or still is True or still is None and probe_pid is not None:
        return False, (f"ORPHAN_SUSPECTED: survivors={[x.pid for x in survivors]}; "
                       f"probe_pid={probe_pid} probe_state={still}")
    if proc.poll() is None:
        return False, "ORPHAN_SUSPECTED: wrapper process did not exit"
    return True, f"Terminated process tree (enumerated {len(targets)} processes)"


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
        good, info = terminate_tree(worker.proc, worker.run_dir / "status.json")
        worker.stopped_cleanly = good
        worker.issue = f"{reason}: {info}"
        worker.timed_out = reason == "TIMEOUT"
        worker.final_state = reason if good else "ORPHAN_SUSPECTED"
        if not good:
            orphan_suspected = True
            stop_launches = True
            print(f"[COORDINATOR] ERROR {worker.issue}", file=sys.stderr, flush=True)
        worker.exit_code = worker.proc.poll()

    try:
        print(f"[COORDINATOR] ENGINEERING POC group={group_id} "
              f"case={args.case} count={args.count} workers={args.workers}", flush=True)
        while active or (next_number <= args.count and not stop_launches):
            free_ram = psutil.virtual_memory().available
            peak_available_pressure = min(peak_available_pressure, free_ram)
            if free_ram < critical:
                stop_launches = True
                coordinator_issue = f"Critical available memory floor reached: {free_ram / 2**30:.2f} GiB"
                for w in list(active.values()):
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
                all_workers.append(w)
                active[n] = w
                reader.start()
                next_number += 1
                print(f"[COORDINATOR] launched worker={n:02d} root_pid={proc.pid}", flush=True)
            drain()
            for n, w in list(active.items()):
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
    except KeyboardInterrupt:
        interrupted = True
        stop_launches = True
        print("[COORDINATOR] INTERRUPTED: stopping all active wrappers", file=sys.stderr, flush=True)
        for w in list(active.values()):
            stop(w, "INTERRUPTED")
        active.clear()
    except Exception as exc:
        stop_launches = True
        coordinator_issue = f"Coordinator error: {type(exc).__name__}: {exc}"
        print("[COORDINATOR] ERROR " + coordinator_issue, file=sys.stderr, flush=True)
        for w in list(active.values()):
            stop(w, "COORDINATOR_ERROR")
        active.clear()
    finally:
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
             "issue": coordinator_issue, "workers": reports}
    save_new(group / "manifest.json", canonical_bytes(final))
    print(f"[COORDINATOR] {'PASS' if successful else 'FAIL'} successes={total_successes}/{args.count}; "
          f"manifest={group / 'manifest.json'}", flush=True)
    return 0 if successful else 1


if __name__ == "__main__":
    try:
        raise SystemExit(coordinator_main())
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"[COORDINATOR] ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
