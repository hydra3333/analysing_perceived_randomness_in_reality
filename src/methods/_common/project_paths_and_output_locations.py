"""Path discovery for independent POC probes. Never use the shell's CWD as root."""
from pathlib import Path


def project_root() -> Path:
    root = Path(__file__).resolve().parents[3]
    if not (root / "src" / "methods").is_dir():
        raise RuntimeError(f"Not a project root: {root}")
    return root


def poc_run_directory(run_id: str) -> Path:
    """Unique scratch path; no user-supplied arbitrary output destinations in P0."""
    if not run_id or len(run_id) > 90 or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in run_id):
        raise ValueError("run-id must contain only ASCII letters, digits, underscore or hyphen")
    return project_root() / "transitory_data" / "poc_runs" / run_id


def project_relative(value: str) -> Path:
    """Resolve a (potentially quoted at CMD) path relative to project root."""
    p = Path(value)
    return p.resolve() if p.is_absolute() else (project_root() / p).resolve()
