"""Windows P1/P2 engineering-only N1 decoy exclusion test.

No terminate()/kill()/taskkill: Python decoys exit upon a stop-file or TTL;
CMD decoy receives its own 'exit' command through stdin. No live process
is terminated forcibly, including on watchdog expiry.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parent.parent
POC_ROOT = ROOT / "transitory_data" / "poc_runs"
COORDINATOR = ROOT / "src" / "Powerball_Experiment_Coordinator.py"
BATCH = ROOT / "Run_Coordinator.bat"
# The reviewed v0.3 source; do not silently run changed termination code.
EXPECTED_COORDINATOR_SHA256 = "a2402175eaf22bf9d0293b49a6d1c91b48fe20d26866cf5d096dcfae6a95a58b"
DECOY_MAX_LIFETIME = 240.0
COORDINATOR_WATCH_SECONDS = 100.0  # Wait only; never kills the child on expiry.
STOP_WAIT_SECONDS = 8.0
TARGET_RE = re.compile(r"^\[SAFETY TARGET\] (?:root|descendant) pid=(\d+)\b", re.M)


def exact_process(proc, pid: int, born: float) -> bool:
    """Only consider original PID + creation time, not any subsequent PID user."""
    import psutil  # Imported only by parent; global decoy needs no third-party packages.
    try:
        return proc.pid == pid and proc.is_running() and abs(proc.create_time() - born) < 0.001
    except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
        return False


def child_decoy(args: argparse.Namespace) -> int:
    """Simple cooperative decoy: nothing is launched or terminated by it."""
    if args.ttl <= 0 or args.ttl > 600:
        raise ValueError("Invalid decoy TTL")
    ready, stop = Path(args.ready), Path(args.stop)
    # Atomically publish startup identity: parent must never parse partial JSON.
    temporary = ready.with_name(ready.name + ".part")
    temporary.write_text(json.dumps({"pid": os.getpid(), "executable": sys.executable,
                                    "prefix": sys.prefix, "base_prefix": sys.base_prefix,
                                    "flavour": args.flavour}), encoding="utf-8")
    temporary.rename(ready)
    until = time.monotonic() + args.ttl
    while time.monotonic() < until and not stop.exists():
        time.sleep(0.15)
    return 0


def verify_switch_and_source() -> str:
    raw = COORDINATOR.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_COORDINATOR_SHA256:
        raise RuntimeError(f"Coordinator SHA-256 is {digest}; expected reviewed v0.3 "
                           f"{EXPECTED_COORDINATOR_SHA256}. Refuse unreviewed source.")
    tree = ast.parse(raw, filename=str(COORDINATOR))
    switches = [n.value.value for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "ENABLE_PROCESS_TERMINATION"
                        for t in n.targets)
                and isinstance(n.value, ast.Constant)]
    if switches != [False]:
        raise RuntimeError("OWNER SAFETY STOP: termination switch is not exactly False")
    if not BATCH.is_file():
        raise RuntimeError("Missing Run_Coordinator.bat")
    return digest


def check_parent_environment() -> str:
    if os.name != "nt":
        raise RuntimeError("Actual decoy/coordinator acceptance requires Windows")
    expected = (ROOT / ".venv").resolve()
    actual = Path(sys.prefix).resolve()
    active = os.environ.get("VIRTUAL_ENV", "")
    if actual != expected or not active or Path(active).resolve() != expected:
        raise RuntimeError("Start from project .venv with 'call activate_venv.bat'")
    return str(expected)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def start_python(flavour: str, interpreter: Path, folder: Path, records: list) -> None:
    import psutil
    ready = folder / f"{flavour}.ready.json"
    stop = folder / f"{flavour}.stop"
    stderr_path = folder / f"{flavour}.stderr.txt"
    env = os.environ.copy()
    if flavour == "global_python":
        env.pop("VIRTUAL_ENV", None)
    cmd = [str(interpreter), "-u", str(Path(__file__).resolve()), "--decoy",
           "--ready", str(ready), "--stop", str(stop), "--flavour", flavour,
           "--ttl", str(DECOY_MAX_LIFETIME)]
    with stderr_path.open("xb") as err:
        pop = subprocess.Popen(cmd, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.DEVNULL, stderr=err,
                               creationflags=subprocess.CREATE_NO_WINDOW)
    record = {"flavour": flavour, "popen": pop, "stop": stop,
              "stderr": stderr_path, "ready": ready}
    records.append(record)  # Register immediately, including on later startup error.
    deadline = time.monotonic() + 12
    while not ready.exists() and time.monotonic() < deadline:
        if pop.poll() is not None:
            break
        time.sleep(0.08)
    if not ready.exists():
        raise RuntimeError(f"{flavour} failed to start; see {stderr_path}")
    hello = read_json(ready)
    pid = hello["pid"]
    process = psutil.Process(pid)
    born = process.create_time()
    parent_ids = {p.pid for p in process.parents()}
    if pid != pop.pid and pop.pid not in parent_ids:
        raise RuntimeError(f"{flavour}: child not linked to its launched Python process")
    if flavour == "global_python" and hello["prefix"] != hello["base_prefix"]:
        raise RuntimeError("Global Python decoy accidentally uses a venv")
    if flavour == "project_python" and Path(hello["prefix"]).resolve() != (ROOT / ".venv").resolve():
        raise RuntimeError("Project Python decoy has wrong sys.prefix")
    launcher = psutil.Process(pop.pid)
    record.update({"pid": pid, "ctime": born, "process": process,
                   "launcher_pid": pop.pid, "launcher_ctime": launcher.create_time(),
                   "launcher_process": launcher, "interpreter": hello["executable"],
                   "name": process.name()})
    print(f"[DECOY BEFORE] {flavour} pid={pid} name={process.name()} "
          f"born={born:.6f} launcher_pid={pop.pid} alive=True", flush=True)


def start_cmd(folder: Path, records: list) -> None:
    import psutil
    comspec = Path(os.environ.get("ComSpec", r"C:\Windows\System32\cmd.exe"))
    pop = subprocess.Popen([str(comspec), "/D", "/Q", "/K"], cwd=ROOT,
                           stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW)
    record = {"flavour": "independent_cmd", "popen": pop}
    records.append(record)
    process = psutil.Process(pop.pid)
    born = process.create_time()
    time.sleep(0.30)
    if process.name().lower() != "cmd.exe" or not exact_process(process, pop.pid, born):
        raise RuntimeError("Independent CMD decoy did not remain alive")
    record.update({"pid": pop.pid, "ctime": born, "process": process, "name": process.name()})
    print(f"[DECOY BEFORE] independent_cmd pid={pop.pid} name=cmd.exe "
          f"born={born:.6f} alive=True", flush=True)


def inspect_coordinator(log_text: str, manifest: dict, decoys: list) -> dict:
    target_pids = [int(v) for v in TARGET_RE.findall(log_text)]
    forbidden = {record["pid"] for record in decoys}
    # A venv redirector is also independent of the worker tree.
    forbidden.update(record["launcher_pid"] for record in decoys
                     if (record.get("launcher_process") is not None and
                         exact_process(record["launcher_process"],
                                       record["launcher_pid"], record["launcher_ctime"])))
    overlap = forbidden.intersection(target_pids)
    if overlap:
        raise RuntimeError(f"DECOY SELECTED BY TERMINATION PLAN: {sorted(overlap)}")
    if len(target_pids) < 18:
        raise RuntimeError(f"Unexpectedly short target list: {len(target_pids)}; expected >=18")
    if log_text.count("[SAFETY BEFORE]") != 6 or log_text.count("PREVIEW ONLY; no termination attempted") != 6:
        raise RuntimeError("Missing BEFORE/AFTER preview from one or more workers")
    proof = re.findall(r"^\[SAFETY PROOF\] ([^\r\n]+)", log_text, flags=re.M)
    if len(proof) != 6 or any("experiment_matched=True" not in p or
                              "unmatched_status=none" not in p or
                              "ownership_anomalies=none" not in p for p in proof):
        raise RuntimeError(f"Ownership proofs incomplete or anomalous: {proof}")
    if "[SAFETY ACTION]" in log_text or "[SAFETY TARGET] root" not in log_text:
        raise RuntimeError("Termination action or missing root targets in preview")
    if (manifest.get("status") != "PASS" or manifest.get("successes") != 6 or
            manifest.get("count_started") != 6 or manifest.get("enable_process_termination") is not False):
        raise RuntimeError("Unexpected coordinator manifest status or safety switch")
    if "[COORDINATOR] PASS successes=6/6" not in log_text:
        raise RuntimeError("Missing coordinator six-worker success line")
    return {"safety_targets": len(target_pids), "ownership_proofs": 6,
            "decoy_pids_excluded": sorted(forbidden), "termination_actions": 0}


def cooperative_stop(records: list) -> list[str]:
    warnings = []
    for r in records:
        print(f"[DECOY STOP BEFORE] {r['flavour']} pid={r.get('pid', r['popen'].pid)} "
              f"name={r.get('name', 'unverified')} method=COOPERATIVE_ONLY no_force_kill", flush=True)
        if r["flavour"] == "independent_cmd":
            try:
                if r["popen"].poll() is None and r["popen"].stdin:
                    r["popen"].stdin.write(b"exit\r\n")
                    r["popen"].stdin.flush()
                    r["popen"].stdin.close()
            except (BrokenPipeError, OSError) as exc:
                warnings.append(f"CMD cooperative exit issue: {exc}")
        else:
            try:
                r["stop"].touch(exist_ok=False)
            except FileExistsError:
                pass
            except OSError as exc:
                warnings.append(f"{r['flavour']} stop-file issue: {exc}")
    for r in records:
        try:
            rc = r["popen"].wait(timeout=STOP_WAIT_SECONDS)
            original_alive = (exact_process(r["process"], r["pid"], r["ctime"])
                              if all(k in r for k in ("process", "pid", "ctime")) else None)
            print(f"[DECOY STOP AFTER] {r['flavour']} pid={r.get('pid', r['popen'].pid)} "
                  f"name={r.get('name', 'unverified')} cooperative_exit_code={rc} "
                  f"original_identity_alive={original_alive} force_kill=False", flush=True)
            if original_alive is True:
                warnings.append(f"{r['flavour']} original process remains after cooperative exit")
        except subprocess.TimeoutExpired:
            warnings.append(f"{r['flavour']} pid={r['popen'].pid} did not exit cooperatively; "
                            "NO SIGNAL SENT. Inspect process manually; Python TTL auto-expires.")
        except (OSError, ValueError) as exc:
            warnings.append(f"{r['flavour']} wait issue: {exc}")
    return warnings


def test_run() -> int:
    import psutil
    source_digest = verify_switch_and_source()
    venv = check_parent_environment()
    group_id = "decoy_" + uuid.uuid4().hex
    POC_ROOT.mkdir(parents=True, exist_ok=True)
    folder = POC_ROOT / group_id
    folder.mkdir(exist_ok=False)
    coordinator_log = folder / "coordinator_console.txt"
    report_path = folder / "decoy_test_report.json"
    records: list[dict] = []
    errors: list[str] = []
    result: dict = {"test_id": group_id, "coordinator_sha256": source_digest,
                    "project_venv": venv, "test_status": "INCOMPLETE", "no_forced_termination": True}
    try:
        base = Path(getattr(sys, "_base_executable", sys.executable)).resolve()
        print(f"[DECOY TEST] source reviewed-v0.3; switch=False; group={group_id}", flush=True)
        start_python("global_python", base, folder, records)
        start_python("project_python", Path(sys.executable).resolve(), folder, records)
        start_cmd(folder, records)
        result["decoys"] = [{k: r[k] for k in ("flavour", "pid", "ctime")} for r in records]
        for r in records:
            if not exact_process(r["process"], r["pid"], r["ctime"]):
                raise RuntimeError(f"Decoy not alive immediately before run: {r['flavour']}")
        cmd = [str(BATCH), "--poc", "--case=sleep-timeout", "--count=6",
               "--workers=6", "--sleep-seconds=12", "--timeout-seconds=45",
               "--plan-termination", "--group-id=" + group_id + "_coord"]
        with coordinator_log.open("xb") as log:
            runner = subprocess.Popen(cmd, cwd=ROOT, stdin=subprocess.DEVNULL,
                                      stdout=log, stderr=subprocess.STDOUT)
            print(f"[COORDINATOR] launched wrapper_pid={runner.pid}; no forced termination ", flush=True)
            try:
                rc = runner.wait(timeout=COORDINATOR_WATCH_SECONDS)
            except subprocess.TimeoutExpired:
                raise RuntimeError(f"Coordinator wait exceeded {COORDINATOR_WATCH_SECONDS}s; "
                                   f"pid={runner.pid} LEFT RUNNING, no kill sent. "
                                   f"Inspect {coordinator_log}")
        result["coordinator_exit_code"] = rc
        log_text = coordinator_log.read_text(encoding="utf-8", errors="replace")
        if rc != 0:
            raise RuntimeError(f"Coordinator exit={rc}; inspect {coordinator_log}")
        manifest_path = POC_ROOT / (group_id + "_coord") / "manifest.json"
        manifest = read_json(manifest_path)
        result["ownership"] = inspect_coordinator(log_text, manifest, records)
        for r in records:
            alive = exact_process(r["process"], r["pid"], r["ctime"])
            print(f"[DECOY VERIFY] {r['flavour']} pid={r['pid']} "
                  f"same_identity_alive_after={alive}", flush=True)
            if not alive:
                raise RuntimeError(f"Decoy not intact after preview: {r['flavour']}")
        result["test_status"] = "PASS"
        print("[DECOY TEST] PASS: 3 decoys intact; 6/6 workers; 0 decoys in plans; no kills", flush=True)
    except (RuntimeError, OSError, ValueError, KeyError, json.JSONDecodeError, psutil.Error) as exc:
        result["test_status"] = "FAIL_OR_INCOMPLETE"
        result["error"] = f"{type(exc).__name__}: {exc}"
        print(f"[DECOY TEST] FAIL/INCOMPLETE: {result['error']}", flush=True)
    finally:
        if records:
            warnings = cooperative_stop(records)
            result["cooperative_cleanup_warnings"] = warnings
            for w in warnings:
                print(f"[DECOY WARNING] {w}", flush=True)
            if warnings:
                result["test_status"] = "FAIL_OR_INCOMPLETE"
        with report_path.open("xb") as f:
            f.write((json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8"))
        print(f"[DECOY TEST] report={report_path}", flush=True)
        print(f"[DECOY TEST] coordinator_console={coordinator_log}", flush=True)
    return 0 if result["test_status"] == "PASS" else 1


def self_test() -> int:
    # Safe, cross-platform parser sanity check: does not launch processes.
    sample = """[SAFETY BEFORE] worker=01 reason=PLAN_ONLY
[SAFETY TARGET] root pid=111 name=cmd.exe alive=True
[SAFETY TARGET] descendant pid=112 name=python.exe
[SAFETY TARGET] descendant pid=113 name=python.exe
[SAFETY PROOF] experiment_matched=True unmatched_status=none ownership_anomalies=none
[SAFETY AFTER] worker=01 PREVIEW ONLY; no termination attempted; workers continue normally
""" * 6 + "[COORDINATOR] PASS successes=6/6\n"
    fake_manifest = {"status": "PASS", "successes": 6,
                     "count_started": 6, "enable_process_termination": False}
    outcome = inspect_coordinator(sample, fake_manifest, [{"pid": 999, "launcher_pid": 999}])
    if outcome["termination_actions"] != 0:
        raise RuntimeError("Parser unexpectedly indicated a kill")
    try:
        inspect_coordinator(sample, fake_manifest, [{"pid": 111}])
    except RuntimeError:
        pass
    else:
        raise RuntimeError("Parser failed to identify selected decoy PID")
    print("PASS: non-destructive plan parser and decoy exclusion (synthetic only)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="P1/P2 automated decoys; strictly non-destructive")
    p.add_argument("--decoy", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--ready", default="", help=argparse.SUPPRESS)
    p.add_argument("--stop", default="", help=argparse.SUPPRESS)
    p.add_argument("--flavour", default="", help=argparse.SUPPRESS)
    p.add_argument("--ttl", type=float, default=DECOY_MAX_LIFETIME, help=argparse.SUPPRESS)
    p.add_argument("--self-test", action="store_true", help="Run parser test; no processes")
    args = p.parse_args()
    if args.decoy:
        if not args.ready or not args.stop or not args.flavour:
            p.error("Internal decoy arguments missing")
        return child_decoy(args)
    if args.self_test:
        return self_test()
    return test_run()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError, ImportError) as exc:
        print(f"[DECOY TEST] ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
