"""Non-destructive, automated P1/P2 Windows smoke suite.

Execute manually under project .venv AFTER standalone P0 testing. It does not
claim W-01..W-25 closure, run memory stress, or edit the lottery dataset.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parent.parent
POC_DIR = ROOT / "transitory_data" / "poc_runs"
COORD = ROOT / "Run_Coordinator.bat"
EXPERIMENT = ROOT / "Run_Experiment.bat"
CANON_DIGEST = "a853ac3545213c8f9be9355e312bf220a74fa89f240e4123aed308d983350937"


def run(command: list[str], *, expected: int, cwd: Path = ROOT, timeout: int = 120) -> str:
    completed = subprocess.run(command, cwd=cwd, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, encoding="utf-8", errors="replace",
                               timeout=timeout, shell=False)
    if completed.returncode != expected:
        raise AssertionError(f"Exit {completed.returncode}, expected {expected}; "
                             f"cmd={command!r}\n{completed.stdout[-7000:]}")
    return completed.stdout


def output_and_status(run_id: str) -> tuple[bytes, dict]:
    folder = POC_DIR / run_id
    return ((folder / "canonical_result.json").read_bytes(),
            json.loads((folder / "status.json").read_text("utf-8")))


def coordinator(case: str, count: int, workers: int, *extras: str,
                expect: int = 0, timeout: int = 120) -> tuple[str, dict]:
    group_id = "smoke_" + uuid.uuid4().hex
    cmd = [str(COORD), "--poc", "--case=" + case,
           "--count=" + str(count), "--workers=" + str(workers),
           "--group-id=" + group_id, "--console-mode=summary", *extras]
    text = run(cmd, expected=expect, timeout=timeout)
    path = POC_DIR / group_id / "manifest.json"
    manifest = json.loads(path.read_text("utf-8"))
    assert manifest["group_id"] == group_id
    return text, manifest


def main() -> int:
    p = argparse.ArgumentParser(description="Windows-only safe architecture POC smoke tests")
    p.add_argument("--with-timeout", action="store_true",
                   help="Also test safe timed-out sleeping worker and process-tree cleanup")
    args = p.parse_args()
    if os.name != "nt":
        p.error("Actual CMD/batch acceptance requires Windows")
    if str(Path(sys.prefix).resolve()).casefold() != str((ROOT / '.venv').resolve()).casefold():
        p.error("First activate project .venv")
    print("[SMOKE] P1/P2 Windows engineering tests (no lottery dataset)", flush=True)
    run_id = "smoke_manual_" + uuid.uuid4().hex
    text = run([str(EXPERIMENT), "POC_Architecture_Probe.py", "--poc",
                "--case=canonical-fixture", "--run-id=" + run_id], expected=0,
               cwd=ROOT / "tests")
    assert "FINISH POC_Architecture_Probe SUCCESS" in text
    base_bytes, base_status = output_and_status(run_id)
    assert base_status["state"] == "SUCCESS"
    assert hashlib.sha256(base_bytes).hexdigest() == CANON_DIGEST
    print("PASS: independent wrapper canonical fixture", flush=True)

    _text, one = coordinator("canonical-fixture", 1, 1)
    assert one["status"] == "PASS" and one["successes"] == 1
    out, status = output_and_status(one["workers"][0]["run_id"])
    assert out == base_bytes and status["state"] == "SUCCESS"
    print("PASS: one-worker coordinator / canonical bytes match direct", flush=True)

    _text, six = coordinator("canonical-fixture", 6, 6)
    assert six["status"] == "PASS" and six["successes"] == 6
    assert len(six["workers"]) == 6
    for record in six["workers"]:
        out, status = output_and_status(record["run_id"])
        assert out == base_bytes and status["state"] == "SUCCESS"
        assert record["console_integrity"] is True
        assert record["experiment_pid"] != 0
    print("PASS: 1-vs-6 and manual/coordinator byte-identical; separate status", flush=True)

    _text, nonzero = coordinator("exit-code", 1, 1, "--exit=3", expect=1)
    r = nonzero["workers"][0]
    assert r["exit_code"] == 3 and nonzero["status"] == "FAIL"
    assert r["status_state"] == "FAILED"
    assert not (POC_DIR / r["run_id"] / "canonical_result.json").exists()
    print("PASS: nonzero exit=3 passed through two wrappers into coordinator", flush=True)

    _text, hard = coordinator("exit-code", 1, 1, "--exit-style=hard", expect=1)
    r = hard["workers"][0]
    assert r["exit_code"] == 7 and hard["status"] == "FAIL"
    assert r["status_state"] == "STARTED"
    assert not (POC_DIR / r["run_id"] / "canonical_result.json").exists()
    print("PASS: hard exit 7, incomplete STARTED status flagged", flush=True)

    if args.with_timeout:
        _text, timed = coordinator("sleep-timeout", 1, 1,
                                  "--sleep-seconds=15", "--timeout-seconds=2", expect=1)
        r = timed["workers"][0]
        assert r["state"] == "TIMEOUT" and timed["orphan_suspected"] is False
        assert not (POC_DIR / r["run_id"] / "canonical_result.json").exists()
        print("PASS: sleeping worker timeout, process tree stopped", flush=True)
    else:
        print("NOT TESTED: timeout cleanup (use --with-timeout explicitly)", flush=True)
    print("NOT TESTED: Ctrl+C, memory stress, W-23 upgrade gating and other W-suite cases")
    print("[SMOKE] PASS", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"[SMOKE] FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
