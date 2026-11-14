#!/usr/bin/env python3
"""Lotterywest-GOV fetch-and-parse smoke check (EX_167 B01). DRAFT until reviewed; run only by the project owner,
only on his own separate go, before a game's Approval 1. One-off: not production code, not part of any package.

What it does: with the INSTALLED updater's own browser fetcher and parser (src/results_master_v0_2.py, unchanged, imported
read-only), it loads the official results-search page once per game for a window that ends BEFORE the quarantine
(31 May to 31 July 2026: the nine draws per game that the first real update will check as its overlap), always with
quarantine_closed=True, and checks without showing any drawn number that:
  - the browser's final address is https on exactly www.lotterywest.wa.gov.au (the updater's own rule; no fallback);
  - the page is not a block or challenge page (the updater's own rule; nothing is bypassed);
  - the parser returns exactly the nine expected draw numbers, each structurally valid (the updater's own checks; a date
    off the weekly rule is counted and shown, as the updater's warning would be, and is not a failure by itself);
  - each parsed draw equals the master's draw of the same number (the comparison the real update makes next).
What it never does: it writes no file, takes no lock, changes no master, ledger, record, code or environment file, makes
no Git change, requests no date on or after 1 August 2026, and prints draw numbers and counts only, never a drawn number.
(Selenium may keep Chrome's driver in its own cache in the user profile, as it would for the updater.)

Run from the repository root:  "%CD%\\.venv\\Scripts\\python.exe" -I -B <this file> [--games POWERBALL,OZLOTTO] [--browser chrome]
Exit codes: 0 PASS; 1 FAIL (parsed, but not what was expected); 2 STOP (block page, results missing, parse failure);
3 REFUSED (a precondition, or the final address); 4 ERROR (anything else, for example the browser did not start).
Any exit code but 0 is a STOP for the owner: do not rerun; send the output.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True          # as -B: no byte-code file is ever written by this check

import argparse
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

WINDOW = (date(2026, 5, 31), date(2026, 7, 31))                        # ends before the quarantine (1 August 2026)
EXPECTED = {"POWERBALL": (1568, 1576), "OZLOTTO": (1685, 1693)}        # the draws strictly inside the window


def say(text: str) -> None:
    print(f"[GOV-SMOKE] {text}", flush=True)


def check_game(RM, game: str, master: list, fetcher) -> bool:
    a, b = WINDOW
    lo, hi = EXPECTED[game]
    draws = fetcher.fetch(game, a, b, quarantine_closed=True)           # the installed fetch and parse, unchanged
    driver = getattr(fetcher, "driver", None)
    final = urlsplit(getattr(driver, "current_url", "") or "")
    numbers = [d.number for d in draws]
    by_no = {d.number: d for d in master}
    on_rule = sum(1 for d in draws if d.day == RM.derived_date(game, d.number).isoformat())
    differ = [d.number for d in draws if by_no.get(d.number) != d]
    say(f"{game}: window {a}..{b}; final address {final.scheme}://{final.hostname}; parsed {len(draws)} draw(s)"
        + (f" {numbers[0]}-{numbers[-1]}" if numbers else "") + f"; on the weekly date rule {on_rule}/{len(draws)}; "
        f"equal to the master {len(draws) - len(differ)}/{len(draws)}")
    ok = True
    if numbers != list(range(lo, hi + 1)):
        say(f"{game}: FAIL: expected exactly draws {lo}-{hi} ({hi - lo + 1}); the parser returned {len(numbers)}")
        ok = False
    if differ:
        say(f"{game}: FAIL: parsed draw(s) {', '.join(map(str, differ[:10]))} differ from the master (values withheld)")
        ok = False
    if ok:
        say(f"{game}: PASS")
    return ok


def main(argv=None, *, root: Path | None = None, fetcher_factory=None) -> int:
    p = argparse.ArgumentParser(description="Lotterywest-GOV fetch-and-parse smoke check (read-only)")
    p.add_argument("--games", default="POWERBALL,OZLOTTO")
    p.add_argument("--browser", choices=("chrome", "firefox"), default="chrome")
    args = p.parse_args(argv)
    root = Path(root) if root else Path(__file__).resolve().parents[3]
    tool = root / "src" / "results_master_v0_2.py"
    if not tool.is_file():
        say(f"REFUSED: {tool} not found (run this from its place in the repository). Nothing was requested.")
        return 3
    sys.path.insert(0, str(root / "src"))
    import results_master_v0_2 as RM
    try:
        games = [g.strip().upper() for g in args.games.split(",") if g.strip()]
        if not games or len(set(games)) != len(games) or any(g not in EXPECTED for g in games):
            raise RM.Refused("games must be POWERBALL and/or OZLOTTO")
        RM.check_constants()
        a, b = WINDOW
        if b >= RM.QUARANTINE_START_DATE or RM.RESULTS_HOST != "www.lotterywest.wa.gov.au":
            raise RM.Refused("this check's window or the updater's host constant is not as reviewed")
        if (root / "source_data" / ".results_master.lock").exists():
            raise RM.Refused("source_data/.results_master.lock exists (an updater run is active or was interrupted)")
        masters = {}
        for g in games:                                                 # every refusal comes before any browser starts
            lo, hi = EXPECTED[g]
            inside = [n for n in range(lo - 2, hi + 3) if a < RM.derived_date(g, n) < b]
            if inside != list(range(lo, hi + 1)) or hi != RM.FIRST_QUARANTINED_DRAW[g] - 1:
                raise RM.Refused(f"{g}: this check's expected draws disagree with the updater's calendar")
            if RM.holdout_opened(root, g):
                raise RM.Refused(f"{g}: the holdout is opened; this check is only for a game before its Approval 1")
            master, _, last = RM.Store(root, g).load_verified_master(quarantine_closed=True)
            if master[-1].number != hi:
                raise RM.Refused(f"{g}: the master ends at draw {master[-1].number}, not {hi} (not the pre-opening state)")
            masters[g] = master
            say(f"{g}: master verified against its ledger (version {last['version']}, last draw {hi}); read-only")
        fetcher = (fetcher_factory or (lambda: RM.BrowserFetcher(args.browser, RM.MIN_PAUSE_SECONDS)))()
        try:
            results = [check_game(RM, g, masters[g], fetcher) for g in games]
        finally:
            getattr(fetcher, "close", lambda: None)()
    except RM.Refused as exc:
        say(f"REFUSED: {exc}"); return 3
    except RM.Stop as exc:
        say(f"STOP: {exc}"); return 2
    except RM.VerifyFail as exc:
        say(f"VERIFY FAIL: {exc}"); return 1
    except Exception as exc:            # for example the browser or its driver did not start; no traceback is printed
        say(f"ERROR: {type(exc).__name__}: {(str(exc).splitlines() or [''])[0][:300]}"); return 4
    if not all(results):
        say("FAIL: see the line(s) above. This check wrote nothing."); return 1
    say(f"PASS: {', '.join(games)}: the installed fetcher and parser read the official page as expected. "
        "This check wrote nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
