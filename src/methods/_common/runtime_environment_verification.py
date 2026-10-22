"""A running child is the authority for its own venv identity."""
import os
import sys
from pathlib import Path
from .project_paths_and_output_locations import project_root


def check_project_environment() -> dict[str, str | int]:
    expected = (project_root() / ".venv").resolve()
    actual = Path(sys.prefix).resolve()
    if os.name == "nt" and str(actual).casefold() != str(expected).casefold():
        raise RuntimeError(f"Wrong Python environment: sys.prefix={actual}; expected {expected}")
    if os.name != "nt":
        # Direct Linux syntax checks cannot validate Windows venv invocation.
        # This helper is Windows-specific; do not claim a Linux test passed W-04.
        raise RuntimeError("Windows-only POC: wrapper tests must run on Windows")
    return {
        "sys_prefix": str(actual),
        "interpreter": sys.executable,
        "pid": os.getpid(),
    }


def thread_settings() -> dict[str, str | None]:
    names = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
    return {name: os.environ.get(name) for name in names}
