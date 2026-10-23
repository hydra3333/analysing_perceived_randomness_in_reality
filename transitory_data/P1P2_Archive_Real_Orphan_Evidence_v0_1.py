"""Archive one identified P1/P2 v0.6 non-destructive Windows timeout rehearsal.

Does not terminate processes, modify experiment output, delete/rename the original
safety marker, or remove the interlock. Run manually from the repository root.
Fixed identity and SHA-256 guards deliberately make this a one-incident utility.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

import psutil

GROUP = "coord-2a42fac2c24549b5b216ffa691f225a7"
RUN = GROUP + "_w001"
ORIGINAL_MARKER_SHA256 = "2d8269eb3845cf17ce7124254f1f9397ae52a1dd5603a0aeb67bdda05453a2aa"
EXPECTED_COORDINATOR_SHA256 = "2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b"
ROOT = Path.cwd()
POC = ROOT / "transitory_data" / "poc_runs"
MARKER = POC / "UNRESOLVED_ORPHAN.json"
DESTINATION = ROOT / "results" / "architecture_poc" / "20261023_timeout_no_kill_coord-2a42fac2"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError("SAFETY HOLD: " + message)


def checked_bytes(p: Path) -> bytes:
    require(p.is_file() and not p.is_symlink(), "missing or unexpected file: " + str(p))
    return p.read_bytes()


def original_gone(label: str, pid: object, born: object) -> None:
    require(type(pid) is int and pid > 0 and type(born) in (int, float),
            label + ": invalid PID/creation time")
    try:
        process = psutil.Process(pid)
        observed_born = process.create_time()
        if abs(observed_born - float(born)) >= 0.5:
            print(f"  {label}: original GONE (PID {pid} reused)", flush=True)
            return
        require(not (process.is_running() and process.status() != psutil.STATUS_ZOMBIE),
                f"{label}: original process {pid} is STILL ALIVE")
        print(f"  {label}: original EXITED", flush=True)
    except psutil.NoSuchProcess:
        print(f"  {label}: original GONE (PID {pid} not present)", flush=True)
    except (psutil.AccessDenied, OSError, ValueError, OverflowError) as exc:
        raise RuntimeError(f"SAFETY HOLD: {label}: identity uncertain: {exc}") from exc


def verify_processes(worker: dict, status: dict) -> None:
    original_gone("wrapper cmd.exe", worker.get("root_pid"), worker.get("root_create_time"))
    members = worker.get("members")
    require(isinstance(members, list) and len(members) == 2,
            "unexpected member count; do not clear marker")
    for i, member in enumerate(members, 1):
        require(isinstance(member, dict), "invalid captured member")
        original_gone(f"captured member #{i} ({member.get('name')})",
                      member.get("pid"), member.get("create_time"))
    original_gone("status experiment (evidence only)",
                  status.get("pid"), status.get("process_create_time_epoch"))


def main() -> int:
    print("=== ARCHIVE ONLY: P1/P2 REAL-MARKER REHEARSAL ===", flush=True)
    raw = checked_bytes(MARKER)
    require(sha(raw) == ORIGINAL_MARKER_SHA256, "marker SHA-256 changed")
    marker = json.loads(raw)
    require(isinstance(marker, dict) and marker.get("group_id") == GROUP,
            "marker identifies a different group")
    require(marker.get("enable_process_termination") is False,
            "unexpected termination switch in marker")
    require(marker.get("coordinator_sha256") == EXPECTED_COORDINATOR_SHA256,
            "unexpected coordinator source identity in marker")
    worker = marker.get("worker")
    require(isinstance(worker, dict) and worker.get("run_id") == RUN,
            "unexpected worker identity")

    locations = {
        "UNRESOLVED_ORPHAN.original.json": MARKER,
        "manifest.json": POC / GROUP / "manifest.json",
        "worker_001.stdout.log": POC / GROUP / "worker_001.stdout.log",
        "runtime_environment.json": POC / GROUP / "runtime_environment.json",
        "pip_freeze.txt": POC / GROUP / "pip_freeze.txt",
        "status.json": POC / RUN / "status.json",
        "canonical_result.json": POC / RUN / "canonical_result.json",
    }
    originals = {name: checked_bytes(path) for name, path in locations.items()}
    require(originals["UNRESOLVED_ORPHAN.original.json"] == raw, "marker changed during read")
    status = json.loads(originals["status.json"])
    require(isinstance(status, dict) and status.get("run_id") == RUN,
            "unexpected status identity")
    require(status.get("state") == "FAILED" and status.get("finished_utc"),
            "unexpected status state; investigate before clearance")
    require(status.get("error") == "OSError: [Errno 22] Invalid argument",
            "unexpected experiment failure reason")
    require(status.get("pid") == 25212 and
            abs(status.get("process_create_time_epoch", 0) - 1792749107.0771797) < 0.001,
            "unexpected status-reported process identity")
    manifest = json.loads(originals["manifest.json"])
    require(isinstance(manifest, dict) and manifest.get("group_id") == GROUP and
            manifest.get("orphan_suspected") is True and
            manifest.get("enable_process_termination") is False and
            manifest.get("status") == "FAIL", "unexpected manifest; investigate")

    print("Original marker verified; validating process identities:", flush=True)
    verify_processes(worker, status)
    require(sha(checked_bytes(MARKER)) == ORIGINAL_MARKER_SHA256,
            "marker changed during preflight")
    require(not DESTINATION.exists(), "archive location already exists: " + str(DESTINATION))

    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.mkdir(exist_ok=False)
    hashes = {}
    for name, data in originals.items():
        target = DESTINATION / name
        with target.open("xb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        require(target.read_bytes() == data, "archive verification failed for " + name)
        hashes[name] = {"sha256": sha(data), "bytes": len(data)}

    record = {
        "archive_record_schema": "POC_MANUAL_ORPHAN_CLEARANCE_EVIDENCE_V1",
        "description": "Non-destructive timeout rehearsal; experiment status is FAILED, not SUCCESS",
        "group": GROUP, "run": RUN,
        "archived_at_utc": datetime.now(timezone.utc).isoformat(),
        "original_marker_sha256": ORIGINAL_MARKER_SHA256,
        "files": hashes,
        "notes": [
            "All original wrapper/descendant/status PID identities were checked as exited or reused before archive.",
            "The original marker has NOT been deleted, renamed or changed by this script.",
            "Source worker stdout log may be empty because coordinator exited before pipe drain.",
            "Archive the original operator console transcript separately if available.",
            "Manual marker clearance is a separate, deliberate operator decision.",
        ],
    }
    with (DESTINATION / "archive_record.json").open("xb") as f:
        f.write((json.dumps(record, sort_keys=True, indent=2) + "\n").encode("utf-8"))
        f.flush()
        os.fsync(f.fileno())

    require(sha(checked_bytes(MARKER)) == ORIGINAL_MARKER_SHA256,
            "original marker changed during archiving; do not clear")
    print("Rechecking original identities after archive:", flush=True)
    verify_processes(worker, status)
    print(f"ARCHIVE PASS: {DESTINATION}", flush=True)
    print(f"ORIGINAL_MARKER_SHA256={ORIGINAL_MARKER_SHA256}", flush=True)
    print("ORIGINAL SAFETY MARKER REMAINS ACTIVE - this script has NOT cleared it", flush=True)
    print("The FAILED status and empty stdout log have been preserved as evidence.", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        print(f"ARCHIVE NOT ACCEPTED: {error}", file=sys.stderr, flush=True)
        print("SAFETY INTERLOCK MUST REMAIN ACTIVE", file=sys.stderr, flush=True)
        sys.exit(2)
