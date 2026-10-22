"""Platform-neutral source checks only, NOT an actual Windows W-suite run."""
from pathlib import Path
import ast
import hashlib
import zipfile

ROOT = Path(__file__).resolve().parent.parent
FILES = [
    "src/Powerball_Experiment_Coordinator.py",
    "src/methods/POC_Coordinator_Probe.py",
    "tests/windows_architecture_poc_suite.py",
    "tests/p1p2_static_checks.py",
]
for name in FILES:
    path = ROOT / name
    ast.parse(path.read_text("utf-8"), filename=name)

bat = (ROOT / "Run_Coordinator.bat").read_bytes()
assert b"\r\n" in bat and bat.replace(b"\r\n", b"").find(b"\n") == -1
assert b"setlocal DisableDelayedExpansion" in bat
assert b"endlocal & exit /b %RC%" in bat

coordinator = (ROOT / FILES[0]).read_text("utf-8")
assert "Run_Experiment.bat" in coordinator
assert "CASE_NAMES = SIMPLE_CASES | EXTRA_CASES" in coordinator
assert "workers <= 6" in coordinator
assert "W-23" not in coordinator  # No false upgrade-gate claim.
assert "source_data" not in coordinator  # POC does not read Powerball files.
print("PASS: source syntax, six-worker cap, CRLF, POC boundary, no scientific source_data")
print("NOT TESTED: Windows CMD, live subprocess pipes, process-tree cleanup, memory/interrupt")
