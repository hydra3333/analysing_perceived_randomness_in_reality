"""One-incident manual clearance of a *previously archived* P1/P2 safety marker.

The default --check is read-only.  --clear-confirmed removes ONLY the exact,
SHA-256-pinned active marker after reverifying archived evidence and original
Windows process identities (PID + creation time). No process termination.

This is an incident-specific operator utility, not coordinator production code.
Run from the project repository root with the project's Python .venv.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys

import psutil

GROUP = "coord-2a42fac2c24549b5b216ffa691f225a7"
RUN = GROUP + "_w001"
MARKER_SHA = "2d8269eb3845cf17ce7124254f1f9397ae52a1dd5603a0aeb67bdda05453a2aa"
COORDINATOR_SHA = "2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b"
EXPECTED_IDENTITIES = (
    ("wrapper cmd.exe", 31720, 1792749106.972062),
    ("first python.exe", 17432, 1792749107.0698512),
    ("experiment python.exe", 25212, 1792749107.0771797),
)
FILES = {
    "UNRESOLVED_ORPHAN.original.json",
    "manifest.json",
    "worker_001.stdout.log",
    "runtime_environment.json",
    "pip_freeze.txt",
    "status.json",
    "canonical_result.json",
}
ROOT = Path.cwd()
ACTIVE = ROOT / "transitory_data" / "poc_runs" / "UNRESOLVED_ORPHAN.json"
ARCHIVE = ROOT / "results" / "architecture_poc" / "20261023_timeout_no_kill_coord-2a42fac2"


def require(ok: bool, why: str) -> None:
    if not ok:
        raise RuntimeError("SAFETY HOLD: " + why)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def bytes_from_regular_file(path: Path) -> bytes:
    require(path.is_file() and not path.is_symlink(), "file missing or unexpected type: " + str(path))
    return path.read_bytes()


def original_is_gone(name: str, pid: int, created: float) -> str:
    try:
        proc = psutil.Process(pid)
        current_created = proc.create_time()
        require(math.isfinite(current_created), f"{name} identity time uncertain")
        if abs(current_created - created) >= 0.5:
            return f"{name}: original GONE; PID {pid} reused"
        require(not (proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE),
                f"{name}: original PID {pid} still ALIVE")
        return f"{name}: original EXITED (PID {pid})"
    except psutil.NoSuchProcess:
        return f"{name}: original GONE (PID {pid} absent)"
    except (psutil.AccessDenied, OSError, ValueError, OverflowError) as exc:
        raise RuntimeError(f"SAFETY HOLD: {name}: identity inspection uncertain: {exc}") from exc


def preflight() -> list[str]:
    require(ROOT.joinpath("Run_Coordinator.bat").is_file(), "run from repository root")
    require(sha(bytes_from_regular_file(ROOT / "src" / "Powerball_Experiment_Coordinator.py")) == COORDINATOR_SHA,
            "coordinator source is not the reviewed v0.6")
    original = bytes_from_regular_file(ACTIVE)
    require(sha(original) == MARKER_SHA, "active safety marker changed; do NOT clear")
    marker = json.loads(original)
    require(isinstance(marker, dict) and marker.get("group_id") == GROUP,
            "active marker identifies an unexpected group")
    require(marker.get("coordinator_sha256") == COORDINATOR_SHA and
            marker.get("enable_process_termination") is False,
            "active marker has unexpected coordinator identity or switch")
    worker = marker.get("worker")
    require(isinstance(worker, dict) and worker.get("run_id") == RUN,
            "marker has unexpected worker identity")
    require(worker.get("root_pid") == 31720 and
            abs(worker.get("root_create_time", 0) - 1792749106.972062) < 0.001,
            "marker wrapper identity mismatch")
    members = worker.get("members")
    require(isinstance(members, list) and len(members) == 2, "unexpected marker member count")
    marker_members = {(m.get("pid"), m.get("create_time")) for m in members if isinstance(m, dict)}
    require(len(marker_members) == 2 and
            all(any(pid == mpid and abs(t - mt) < 0.001 for mpid, mt in marker_members)
                for _, pid, t in EXPECTED_IDENTITIES[1:]), "marker process identities mismatch")

    require(ARCHIVE.is_dir() and not ARCHIVE.is_symlink(), "expected archive missing")
    record = json.loads(bytes_from_regular_file(ARCHIVE / "archive_record.json"))
    require(isinstance(record, dict) and record.get("group") == GROUP and
            record.get("run") == RUN and record.get("original_marker_sha256") == MARKER_SHA,
            "archive record identity mismatch")
    table = record.get("files")
    require(isinstance(table, dict) and set(table) == FILES,
            "archive record missing required files")
    for name in sorted(FILES):
        raw = bytes_from_regular_file(ARCHIVE / name)
        entry = table[name]
        require(isinstance(entry, dict) and entry.get("sha256") == sha(raw) and
                entry.get("bytes") == len(raw), "archived file checksum mismatch: " + name)
    require(bytes_from_regular_file(ARCHIVE / "UNRESOLVED_ORPHAN.original.json") == original,
            "archived original marker is not byte-for-byte identical to active marker")
    status = json.loads(bytes_from_regular_file(ARCHIVE / "status.json"))
    require(isinstance(status, dict) and status.get("run_id") == RUN and
            status.get("state") == "FAILED" and
            status.get("error") == "OSError: [Errno 22] Invalid argument" and
            status.get("pid") == 25212 and
            abs(status.get("process_create_time_epoch", 0) - 1792749107.0771797) < 0.001,
            "unexpected archived probe identity/status")
    manifest = json.loads(bytes_from_regular_file(ARCHIVE / "manifest.json"))
    require(isinstance(manifest, dict) and manifest.get("group_id") == GROUP and
            manifest.get("orphan_suspected") is True and
            manifest.get("enable_process_termination") is False and
            manifest.get("status") == "FAIL", "unexpected archived coordinator manifest")

    states = [original_is_gone(*identity) for identity in EXPECTED_IDENTITIES]
    # Status must agree with the captured experiment identity; it is evidence ONLY.
    states.append(original_is_gone("status-reported experiment", 25212, 1792749107.0771797))
    require(sha(bytes_from_regular_file(ACTIVE)) == MARKER_SHA, "marker changed during checks")
    return states


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--check", action="store_true", help="Read-only clearance eligibility check")
    actions.add_argument("--clear-confirmed", action="store_true", help="Remove ONLY exact pinned safety marker after all checks")
    args = parser.parse_args()

    print("=== P1/P2 INCIDENT-SPECIFIC MANUAL ORPHAN CLEARANCE ===", flush=True)
    print(f"Original marker SHA256: {MARKER_SHA}", flush=True)
    states = preflight()
    for state in states:
        print("  " + state, flush=True)
    print("PASS: seven archived files verified; archived and active marker bytes identical", flush=True)
    print("The archived FAILED experiment status is intentionally preserved.", flush=True)
    if args.check:
        print("CHECK PASS: eligible for deliberate manual clearance; active marker NOT MODIFIED", flush=True)
        return 0

    # Re-run immediately before clearance, reducing time between inspection and removal.
    states = preflight()
    for state in states:
        print("  FINAL CHECK: " + state, flush=True)
    # Do not overwrite any existing record, ever. If a previous attempt failed
    # after creating this record, it requires human inspection, not a retry.
    clearance_record = ARCHIVE / "manual_clearance_record.json"
    require(not clearance_record.exists() and not clearance_record.is_symlink(),
            "clearance record already exists; investigate before proceeding")
    evidence = {
        "schema": "P1P2_ONE_INCIDENT_MANUAL_CLEARANCE_V1",
        "group_id": GROUP, "run_id": RUN,
        "action": "operator_verified_clearance_of_exact_marker",
        "marker_original_sha256": MARKER_SHA,
        "marker_path": str(ACTIVE),
        "archived_original": str(ARCHIVE / "UNRESOLVED_ORPHAN.original.json"),
        "checked_original_identities": states,
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "note": "This check does not claim experiment SUCCESS; archived status is FAILED.",
    }
    with clearance_record.open("xb") as f:
        f.write((json.dumps(evidence, sort_keys=True, indent=2) + "\n").encode("utf-8"))
        f.flush()
        os.fsync(f.fileno())
    require(sha(bytes_from_regular_file(ACTIVE)) == MARKER_SHA,
            "marker changed after clearance record; leave active")
    ACTIVE.unlink()  # Only deletion in this entire script: exact SHA-pinned incident marker.
    require(not ACTIVE.exists() and not ACTIVE.is_symlink(),
            "marker still exists following removal")
    print("MANUAL CLEARANCE PASS: exact original active marker removed; archive preserved", flush=True)
    print("ARCHIVE: " + str(ARCHIVE), flush=True)
    print("CLEARANCE RECORD: " + str(clearance_record), flush=True)
    print("NO PROCESS TERMINATION OR EXPERIMENT MODIFICATION PERFORMED", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print("SAFETY HOLD: " + str(exc), file=sys.stderr, flush=True)
        print("DO NOT DELETE THE SAFETY MARKER MANUALLY ON THIS FAILURE", file=sys.stderr, flush=True)
        sys.exit(2)
