"""Engineering-only Windows subprocess fixture. NOT a lottery prediction method."""
from __future__ import annotations
import argparse
import json
import os
import sys
import uuid
from pathlib import Path

from _common.project_paths_and_output_locations import project_root, poc_run_directory, project_relative
from _common.experiment_console_and_file_output import canonical_json, digest, publish_immutable
from _common.experiment_runtime_status_and_resources import ProbeStatus
from _common.runtime_environment_verification import check_project_environment, thread_settings


CASES = ("echo-argv", "canonical-fixture", "exit-code", "verbose")


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthetic Windows architecture probe; NOT E-method")
    parser.add_argument("--poc", action="store_true", required=True)
    parser.add_argument("--case", choices=CASES, required=True)
    parser.add_argument("--run-id", default="poc-" + uuid.uuid4().hex)
    parser.add_argument("--exit", type=int, default=0)
    parser.add_argument("--exit-style", choices=("normal", "exception", "hard"), default="normal")
    parser.add_argument("--lines", type=int, default=10)
    parser.add_argument("--path-probe", default="tests/fixtures/poc_canonical_fixture.json")
    parser.add_argument("--note", default="")
    parser.add_argument("--history", type=int, default=None)
    args = parser.parse_args()
    if not args.poc:
        parser.error("--poc required")
    if args.lines < 0 or args.lines > 100_000:
        parser.error("--lines must be in 0..100000")
    if args.exit_style != "normal" and args.case != "exit-code":
        parser.error("--exit-style requires --case=exit-code")
    details = check_project_environment()
    run_dir = poc_run_directory(args.run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    status_path = run_dir / "status.json"
    if status_path.exists():
        raise FileExistsError(f"Run ID already used: {args.run_id}")
    status = ProbeStatus(status_path, args.run_id, args.case)
    print(f"BEGIN POC_Architecture_Probe case={args.case} run={args.run_id}", flush=True)
    try:
        if args.case == "exit-code":
            if args.exit_style == "hard":
                os._exit(7)  # Must leave STARTED-only status.
            if args.exit_style == "exception":
                raise RuntimeError("Deliberate POC exception")
            if args.exit:
                status.finish("FAILED", error=f"Deliberate exit code {args.exit}")
                return args.exit
            payload = {"probe": "POC_Architecture_Probe", "case": "exit-code", "code": 0}
        elif args.case == "echo-argv":
            payload = {"probe": "POC_Architecture_Probe", "case": args.case,
                       "argv": sys.argv[1:], "root": str(project_root()),
                       "cwd": os.getcwd(), "project_path_probe": str(project_relative(args.path_probe)),
                       "environment": details, "threads": thread_settings()}
        elif args.case == "canonical-fixture":
            path = project_root() / "tests" / "fixtures" / "poc_canonical_fixture.json"
            raw = path.read_bytes()
            fixture = json.loads(raw)
            payload = {"probe": "POC_Architecture_Probe", "case": "canonical-fixture",
                       "fixture_sha256": digest(raw), "synthetic_values": fixture["values"],
                       "synthetic_total": sum(fixture["values"]),
                       "note": "Synthetic POC; never a lottery forecast"}
        else:
            for i in range(args.lines):
                print(f"PROGRESS POC_Architecture_Probe {i + 1}/{args.lines}", flush=True)
            payload = {"probe": "POC_Architecture_Probe", "case": "verbose", "lines": args.lines}
        canonical = canonical_json(payload)
        publish_immutable(run_dir / "canonical_result.json", canonical)
        print("RESULT " + canonical.decode("utf-8").strip(), flush=True)
        print("DIGEST " + digest(canonical), flush=True)
        status.finish("SUCCESS")
        print("FINISH POC_Architecture_Probe SUCCESS", flush=True)
        return 0
    except Exception as exc:
        status.finish("FAILED", error=f"{type(exc).__name__}: {exc}")
        print("FINISH POC_Architecture_Probe FAILED", file=sys.stderr, flush=True)
        raise


if __name__ == "__main__":
    sys.exit(main())
