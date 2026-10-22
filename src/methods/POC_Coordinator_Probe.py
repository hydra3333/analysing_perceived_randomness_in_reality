"""Additional engineering-only scheduler probes. Never a lottery E-method."""
from __future__ import annotations

import argparse
import os
import sys
import time
import uuid

from _common.experiment_console_and_file_output import canonical_json, digest, publish_immutable
from _common.experiment_runtime_status_and_resources import ProbeStatus
from _common.project_paths_and_output_locations import poc_run_directory
from _common.runtime_environment_verification import check_project_environment, thread_settings


def main() -> int:
    p = argparse.ArgumentParser(description="Scheduler engineering probe, no real lottery data")
    p.add_argument("--poc", action="store_true", required=True)
    p.add_argument("--case", choices=("sleep-timeout", "cpu-load", "memory-load"), required=True)
    p.add_argument("--run-id", default="poc-" + uuid.uuid4().hex)
    p.add_argument("--sleep-seconds", type=float, default=1.0)
    p.add_argument("--cpu-seconds", type=float, default=1.0)
    p.add_argument("--memory-mb", type=int, default=32)
    args = p.parse_args()
    if not (0 <= args.sleep_seconds <= 7200):
        p.error("--sleep-seconds must be 0..7200")
    if not (0 <= args.cpu_seconds <= 30):
        p.error("--cpu-seconds must be 0..30")
    if not (1 <= args.memory_mb <= 2048):
        p.error("--memory-mb must be 1..2048")
    environment = check_project_environment()
    run_dir = poc_run_directory(args.run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    if (run_dir / "status.json").exists():
        raise FileExistsError(f"Probe run already used: {args.run_id}")
    status = ProbeStatus(run_dir / "status.json", args.run_id, args.case)
    print(f"BEGIN POC_Coordinator_Probe case={args.case} run={args.run_id}", flush=True)
    try:
        if args.case == "sleep-timeout":
            time.sleep(args.sleep_seconds)
            calculation = {"duration_requested_seconds": args.sleep_seconds}
        elif args.case == "cpu-load":
            deadline = time.process_time() + args.cpu_seconds
            n = 0
            while time.process_time() < deadline:
                n = (n * 1664525 + 1013904223) % (2**32)
            calculation = {"cpu_work_completed": True}
        else:
            # Allocate physical pages deliberately. This requires an explicit
            # --allow-memory-stress gate in the coordinator for large tests.
            mem = bytearray(args.memory_mb * 1024 * 1024)
            for offset in range(0, len(mem), 4096):
                mem[offset] = 1
            print(f"PROGRESS memory-allocated-megabytes={args.memory_mb}", flush=True)
            time.sleep(args.sleep_seconds)
            calculation = {"memory_megabytes": args.memory_mb, "sample": mem[0]}
            del mem
        payload = {"probe": "POC_Coordinator_Probe", "case": args.case,
                   "engineering_only": True, "completed": True,
                   "environment": {"sys_prefix": environment["sys_prefix"]},
                   "threads": thread_settings(), **calculation}
        raw = canonical_json(payload)
        publish_immutable(run_dir / "canonical_result.json", raw)
        print("RESULT " + raw.decode("utf-8").strip(), flush=True)
        print("DIGEST " + digest(raw), flush=True)
        status.finish("SUCCESS")
        print("FINISH POC_Coordinator_Probe SUCCESS", flush=True)
        return 0
    except Exception as ex:
        status.finish("FAILED", error=f"{type(ex).__name__}: {ex}")
        print("FINISH POC_Coordinator_Probe FAILED", file=sys.stderr, flush=True)
        raise


if __name__ == "__main__":
    sys.exit(main())
