"""Per-experiment metrics: no assumptions about Windows redirector PID."""
from __future__ import annotations
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from .experiment_console_and_file_output import publish_mutable_status

try:
    import psutil
except ImportError:
    psutil = None  # Installer is required before full Windows POC acceptance.


def _iso_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def resource_sample() -> dict:
    out = {"cpu_time_seconds": time.process_time(), "peak_working_set_bytes": None,
           "peak_field": "UNAVAILABLE", "process_create_time_epoch": None}
    if psutil is None:
        return out
    process = psutil.Process(os.getpid())
    out["process_create_time_epoch"] = process.create_time()
    info = process.memory_info()
    for field in ("peak_wset", "peak_rss"):
        value = getattr(info, field, None)
        if value is not None:
            out["peak_working_set_bytes"] = int(value)
            out["peak_field"] = field
            break
    return out


class ProbeStatus:
    def __init__(self, path: Path, run_id: str, case: str):
        self.path = path
        self.started = time.perf_counter()
        self.start_info = resource_sample()
        self.value: dict = {
            "schema": "ENGINEERING_POC_STATUS_V1", "run_id": run_id, "case": case,
            "state": "STARTED", "pid": os.getpid(), "sys_prefix": sys.prefix,
            "started_utc": _iso_utc(), "process_create_time_epoch": self.start_info["process_create_time_epoch"],
        }
        publish_mutable_status(path, self.value)

    def finish(self, state: str, *, error: str | None = None) -> None:
        if state not in ("SUCCESS", "FAILED"):
            raise ValueError("Illegal terminal status")
        self.value.update({"state": state, "finished_utc": _iso_utc(),
                           "elapsed_seconds": time.perf_counter() - self.started,
                           **resource_sample()})
        if error:
            self.value["error"] = error
        publish_mutable_status(self.path, self.value)
