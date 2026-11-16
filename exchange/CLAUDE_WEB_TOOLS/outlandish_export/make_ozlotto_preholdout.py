#!/usr/bin/env python3
"""Make OZLOTTO_preholdout_only.csv for the OUTLANDISH_01 side project (Claude web chat, 16 November 2026). Owner-run only.

What it reads: ONLY the Oz Lotto results master as COMMITTED in Git (`git show HEAD:source_data/OZLOTTO_results_master.csv`),
which is the version-1 master built from Lotterywest-GOV, ending before the holdout. It refuses unless those bytes have the
version-1 SHA-256 4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f (readiness sheet, prerequisite 5). It never
reads the working-tree master (which now holds the holdout), any ledger, grab, backup, results file or holdout record.
How it checks: with the installed updater's own CSV reader and validators (src/results_master_v0_2.py, imported read-only,
unchanged), quarantine closed: any draw at or after the holdout boundary stops it before anything is written.
What it writes: one NEW file, GAIS/OUTLANDISH_01/OZLOTTO_preholdout_only.csv (refuses if it exists), UTF-8 (ASCII), LF, no
BOM: Draw_Number,Date,Drawn_1..Drawn_7,Supplementary_1..Supplementary_3, ascending, the numbers in the order the master
stores them (as the official results page lists them; never sorted). The FILE holds every drawn number; the screen
shows a certificate of counts and hashes only (no drawn number), including how many rows have their mains, or their
supplementaries, already in ascending order: if (nearly) all do, the page shows them sorted, not in drawn order.
Run from the repository root:  "%CD%\\.venv\\Scripts\\python.exe" -I -B exchange\\CLAUDE_WEB_TOOLS\\outlandish_export\\make_ozlotto_preholdout.py
Exit codes: 0 written; 1 a check failed (nothing written); 3 refused (nothing written).
"""
from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
GAME = "OZLOTTO"
V1_SHA256 = "4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f"
OUT_REL = Path("GAIS") / "OUTLANDISH_01" / "OZLOTTO_preholdout_only.csv"
HEADER = ["Draw_Number", "Date"] + [f"Drawn_{i}" for i in range(1, 8)] + [f"Supplementary_{i}" for i in range(1, 4)]


def say(text: str) -> None:
    print(f"[OZ-PREHOLDOUT] {text}", flush=True)


def main(root: Path | None = None) -> int:
    root = Path(root) if root else Path(__file__).resolve().parents[3]
    out = root / OUT_REL
    if out.exists():
        say(f"REFUSED: {OUT_REL.as_posix()} already exists; nothing was read or written"); return 3
    if not out.parent.is_dir():
        say(f"REFUSED: {OUT_REL.parent.as_posix()} is not a folder; nothing was read or written"); return 3
    spec = importlib.util.spec_from_file_location("results_master_v0_2", root / "src" / "results_master_v0_2.py")
    RM = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = RM            # before exec: @dataclass looks its module up there (reviewer, 16 November 2026)
    spec.loader.exec_module(RM)
    era, cutoff = RM.ERAS[GAME], RM.FIRST_QUARANTINED_DRAW[GAME]
    r = subprocess.run(["git", "--no-optional-locks", "-C", str(root), "show", f"HEAD:source_data/{GAME}_results_master.csv"],
                       capture_output=True)
    if r.returncode:
        say("REFUSED: could not read the committed master from Git; nothing was written"); return 3
    data = r.stdout
    if hashlib.sha256(data).hexdigest() != V1_SHA256:
        say("REFUSED: the committed master is not the version-1 bytes (SHA-256 differs); nothing was written"); return 3
    try:
        draws = RM.from_csv_bytes(GAME, data)
        warns = RM.validate_series(GAME, draws, quarantine_closed=True)   # stops on any holdout-or-later draw
    except (RM.VerifyFail, RM.Stop) as exc:
        say(f"FAIL: {exc}; nothing was written"); return 1
    nums = [d.number for d in draws]
    problems = []
    if nums[0] != era.first_draw:
        problems.append(f"first draw {nums[0]}, not {era.first_draw}")
    if nums[-1] != cutoff - 1 or max(nums) >= cutoff:
        problems.append(f"last draw {nums[-1]}, not {cutoff - 1}")
    if len(draws) != cutoff - era.first_draw or len(set(nums)) != len(nums):
        problems.append(f"{len(draws)} rows, not {cutoff - era.first_draw} distinct")
    bad = [d.number for d in draws if len(set(d.main + d.secondary)) != 10
           or not all(1 <= x <= 47 for x in d.main + d.secondary)]
    if bad:
        problems.append(f"{len(bad)} row(s) without 10 distinct values in 1-47 (first: draw {bad[0]})")
    if problems:
        say("FAIL: " + "; ".join(problems) + "; nothing was written"); return 1
    lines = [",".join(HEADER)] + [",".join(str(x) for x in (d.number, d.day, *d.main, *d.secondary)) for d in draws]
    body = ("\n".join(lines) + "\n").encode("ascii")
    with out.open("xb") as fh:
        fh.write(body)
    say(f"source: the committed version-1 Oz Lotto master (Lotterywest-GOV), SHA-256 {V1_SHA256}")
    say(f"current format from draw {era.first_draw} ({era.first_date}); exclusive cutoff {cutoff} "
        f"(the parent project's Oz Lotto holdout is {cutoff}-{cutoff + 9}; FIRST_QUARANTINED_DRAW in src/results_master_v0_2.py)")
    say(f"first draw {nums[0]}, last draw {nums[-1]}, rows {len(draws)} (= {cutoff} - {era.first_draw}); max draw {max(nums)} < {cutoff}")
    say(f"every row: 10 distinct values, all in 1-47 ({len(draws)}/{len(draws)}); ascending, no gaps or duplicates; "
        f"dates off the weekly rule: {len(warns)}")
    asc_m = sum(1 for d in draws if list(d.main) == sorted(d.main))
    asc_s = sum(1 for d in draws if list(d.secondary) == sorted(d.secondary))
    say(f"order check: rows with the 7 mains already ascending {asc_m}/{len(draws)}; with the 3 supplementaries ascending "
        f"{asc_s}/{len(draws)} (if drawn order is stored, expect about {len(draws) / 5040:.2f} and {len(draws) / 6:.0f}; "
        f"if all {len(draws)}, the page lists them sorted, not in drawn order)")
    say("read: only the committed Git bytes above; no working-tree master, ledger, grab, backup, results or holdout file")
    say(f"wrote {OUT_REL.as_posix()}: {len(body)} bytes, UTF-8 (ASCII), LF, no BOM; SHA-256 {hashlib.sha256(body).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
