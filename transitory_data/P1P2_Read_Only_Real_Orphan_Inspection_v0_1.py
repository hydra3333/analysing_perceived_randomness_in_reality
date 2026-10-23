"""READ ONLY. Inspect one known P1/P2 v0.6 timeout marker on Windows.

Never signals processes, writes files, archives evidence, or clears the interlock.
Run from the repository root using .venv\\Scripts\\python.exe.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import psutil

EXPECTED_GROUP = "coord-2a42fac2c24549b5b216ffa691f225a7"
EXPECTED_MARKER_SHA256 = "2d8269eb3845cf17ce7124254f1f9397ae52a1dd5603a0aeb67bdda05453a2aa"
ROOT = Path.cwd()
POC = ROOT / "transitory_data" / "poc_runs"
MARKER = POC / "UNRESOLVED_ORPHAN.json"


def inspect_identity(label: str, pid: object, creation_time: object) -> bool:
    """Return True ONLY if the original identity is confirmed gone/reused."""
    print(f"  {label}: original pid={pid}, creation_time={creation_time}")
    if type(pid) is not int or pid <= 0 or type(creation_time) not in (int, float):
        print("    UNCERTAIN: incomplete/invalid identity")
        return False
    try:
        process = psutil.Process(pid)
        observed_time = process.create_time()
        if abs(observed_time - float(creation_time)) >= 0.001:
            print(f"    ORIGINAL GONE: PID reused (observed creation_time={observed_time})")
            return True
        if process.is_running() and process.status() != psutil.STATUS_ZOMBIE:
            print("    STILL ALIVE: original PID and creation time match. KEEP INTERLOCK.")
            return False
        print("    ORIGINAL EXITED: matching process no longer running")
        return True
    except psutil.NoSuchProcess:
        print("    ORIGINAL GONE: PID not present")
        return True
    except (psutil.AccessDenied, OSError, ValueError, OverflowError) as exc:
        print(f"    UNCERTAIN: {type(exc).__name__}: {exc}. KEEP INTERLOCK.")
        return False


def main() -> int:
    print("=== READ-ONLY P1/P2 REAL-ORPHAN IDENTITY INSPECTION ===")
    if MARKER.is_symlink() or not MARKER.is_file():
        print("HOLD: expected regular marker missing/invalid; investigate manually")
        return 2
    original_bytes = MARKER.read_bytes()
    actual_hash = hashlib.sha256(original_bytes).hexdigest()
    print(f"Marker: {MARKER}")
    print(f"Marker SHA256: {actual_hash}")
    if actual_hash != EXPECTED_MARKER_SHA256:
        print("HOLD: original marker hash differs; do not clear")
        return 2
    try:
        marker = json.loads(original_bytes)
        worker = marker["worker"]
        group_id = marker["group_id"]
        run_id = worker["run_id"]
        members = worker["members"]
    except (ValueError, KeyError, TypeError) as exc:
        print(f"HOLD: marker cannot be interpreted: {exc}")
        return 2
    if group_id != EXPECTED_GROUP or run_id != EXPECTED_GROUP + "_w001":
        print("HOLD: unexpected group/run identity")
        return 2
    print(f"Group: {group_id}")
    print(f"Run:   {run_id}")
    safe = inspect_identity("Wrapper cmd.exe", worker.get("root_pid"),
                            worker.get("root_create_time"))
    if not isinstance(members, list) or len(members) != 2:
        print("HOLD: unexpected captured-member inventory")
        safe = False
    else:
        for index, member in enumerate(members, start=1):
            if not isinstance(member, dict):
                print(f"  Member #{index} malformed. HOLD.")
                safe = False
                continue
            safe = inspect_identity(f"Captured member #{index} ({member.get('name')})",
                                    member.get("pid"), member.get("create_time")) and safe
    status_path = POC / run_id / "status.json"
    print(f"Status: {status_path}")
    try:
        status = json.loads(status_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"  HOLD: missing or invalid status: {type(exc).__name__}: {exc}")
        return 2
    if not isinstance(status, dict) or status.get("run_id") != run_id:
        print("  HOLD: status is not for the expected run")
        return 2
    print(f"  State: {status.get('state')}; finished_utc: {status.get('finished_utc')}")
    safe = inspect_identity("Status-reported experiment (EVIDENCE ONLY)",
                            status.get("pid"), status.get("process_create_time_epoch")) and safe
    if status.get("state") != "SUCCESS" or not status.get("finished_utc"):
        print("  HOLD: probe has not reported a normal finished state")
        safe = False
    for item in (POC / group_id / "manifest.json",
                 POC / group_id / "worker_001.stdout.log",
                 POC / run_id / "canonical_result.json"):
        present = item.is_file()
        print(f"Evidence {'PRESENT' if present else 'MISSING'}: {item}")
        if not present:
            safe = False
    if safe:
        print("PASS: original wrapper and both captured descendants and status PID are confirmed gone/reused;")
        print("      probe reports SUCCESS, and relevant evidence files exist.")
        print("      Eligible for SEPARATE manual evidence archival and clearance after review.")
        print("      THIS INSPECTION DID NOT MODIFY ANYTHING.")
        return 0
    print("SAFETY HOLD: identity or completion remains uncertain. LEAVE MARKER IN PLACE.")
    print("THIS INSPECTION DID NOT MODIFY ANYTHING.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
