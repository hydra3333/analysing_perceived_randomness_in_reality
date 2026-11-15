#!/usr/bin/env python3
"""Does the INSTALLED updater depend on the order in which the results page lists its draws? (Claude web chat,
15 November 2026, after the official-page check's STOP: the real page lists draws newest first.)

INVENTED data only; no website is contacted. For each game and each scenario, the installed src/results_master_v0_2.py
runs its real cmd_update -> update_game -> BrowserFetcher.fetch -> parse_gov path, unchanged, against a stand-in driver
object whose page text holds the same invented draws in three orders: oldest first, newest first, shuffled. The roots,
the INIT and the opening record are built by the project's own accepted test fixtures
(tests/test_mhupa_updater_v0_2.py, EmittedBytesReconciliation). It then compares, across the three orders: the exit
code, the printed [MASTER] line, the master's bytes, the grab's bytes, the backup's bytes and every ledger field except
the run's own time stamps and time-stamped file names.

Scenario A, the Mode H first update: the game opened, "today" 15 November 2026, the default --months-back 5 (one page
of 24 draws: the 9 overlapping draws, the 10 holdout draws and 5 later ones).
Scenario B, a closed game before the quarantine: "today" 31 July 2026 (one page of pre-quarantine draws; NO_CHANGE).

It reads nothing under the repository's source_data/, results/ or transitory_data/. Not Windows evidence and no evidence
about the real page's wording: that is what the owner-run check is for.
Usage (from a data-free copy of the repository; selenium importable):
  PYTHONPATH=src:src/methods:tests python -B exchange/CLAUDE_WEB_TOOLS/modeh_readiness/updater_page_order_evidence.py
"""
import contextlib, hashlib, io, json, random, re, sys, tempfile
from datetime import date
from pathlib import Path

sys.dont_write_bytecode = True
import test_mhupa_updater_v0_2 as T
import _common.owner_records as OR

ORDERS = ("oldest first", "newest first", "shuffled")
STAMPED = ("utc", "grab_file", "backup_file")          # the only fields allowed to differ between runs


class FakeDriver:
    def __init__(self, text):
        self.title, self.text, self.current_url, self.gets = "Results", text, "", []

    def get(self, url):
        self.gets.append(url); self.current_url = url

    def find_element(self, by, name):
        return self

    def quit(self):
        pass


def page(up, fx, game, a, b, order, *, closed):
    """The page text for one search window: the invented draws dated a..b, in the wording the parser expects."""
    blocks, n = [], up.ERAS[game].first_draw
    while up.derived_date(game, n) <= b:
        day = up.derived_date(game, n)
        if a <= day and (not closed or n < up.FIRST_QUARANTINED_DRAW[game]):
            d = fx.synth(game, n)
            blocks.append("\n".join([f"Draw {d.number}", f"{day.strftime('%A')} {day.day} {up.MONTH_NAMES[day.month - 1]} {day.year}",
                                     "Winning numbers:", *map(str, d.main),
                                     "Powerball:" if game == "POWERBALL" else "Supplementary numbers:",
                                     *map(str, d.secondary), "View prizes"]))
        n += 1
    if order == "newest first":
        blocks.reverse()
    elif order == "shuffled":
        random.Random(20261115).shuffle(blocks)
    return blocks


def one_run(up, fx, game, today, order, *, opened):
    with tempfile.TemporaryDirectory() as td:
        root = fx.init_root(Path(td), game)
        st = up.Store(root, game)
        if opened:
            OR.write_record(OR.opening_record_path(root, game),
                            {"schema": OR.OPENING_SCHEMA, "game": game, "study_manifest_sha256": "a" * 64,
                             "opened_utc": "2026-11-15T08:00:00Z", "owner_statement": OR.OPENING_STATEMENT,
                             "freeze_version": 1, "freeze_master_sha256": st.ledger_rows()[0]["master_sha256"]})
        windows = up.split_windows(*up.month_window(today, up.DEFAULT_MONTHS_BACK))
        assert len(windows) == 1, windows
        blocks = page(up, fx, game, *windows[0], order, closed=not opened)
        driver = FakeDriver("\n".join(blocks))

        def make():
            f = object.__new__(up.BrowserFetcher)        # the real class and its real fetch(); only the driver is fake
            f.driver, f.pause, f.last, f.log = driver, 0.0, 0.0, []
            return f
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = up.cmd_update(root, [game], up.DEFAULT_MONTHS_BACK, "chrome", up.MIN_PAUSE_SECONDS, fetcher_factory=make, today=today)
        sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        grabs = sorted(st.grabs.glob("*.csv")); backups = sorted(st.backups.glob("*.csv")) if st.backups.is_dir() else []
        rows = [{k: v for k, v in r.items() if k not in STAMPED} for r in st.ledger_rows()]
        first = re.match(r"Draw (\d+)", blocks[0]).group(1)
        return {"rc": rc, "line": out.getvalue().splitlines()[0], "master": sha(st.master), "grabs": [sha(g) for g in grabs],
                "backups": [sha(x) for x in backups], "ledger": json.dumps(rows, sort_keys=True),
                "page": (len(blocks), first), "gets": len(driver.gets)}


def main() -> int:
    T.EmittedBytesReconciliation.setUpClass()
    fx = T.EmittedBytesReconciliation("test_emitted_ledger_and_master_pass_the_version_2_rules")
    up = fx.up
    up.PAGE_WAIT_SECONDS, up.WAIT_POLL_SECONDS = 1.0, 0.2            # this script only: do not wait 15 s for a fake page
    ok = True
    for name, today, opened in (("A: the Mode H first update (opened game, 15 November 2026)", date(2026, 11, 15), True),
                                ("B: a closed game before the quarantine (31 July 2026)", date(2026, 7, 31), False)):
        print(name)
        for game in ("POWERBALL", "OZLOTTO"):
            runs = {o: one_run(up, fx, game, today, o, opened=opened) for o in ORDERS}
            for o, r in runs.items():
                print(f"  {game}, page {o} ({r['page'][0]} draws, first listed {r['page'][1]}, {r['gets']} page load): exit {r['rc']}; "
                      f"{r['line']}; master {r['master'][:12]}, grab {r['grabs'][0][:12]}"
                      + (f", backup {r['backups'][0][:12]}" if r["backups"] else ""))
            base = {k: v for k, v in runs[ORDERS[0]].items() if k != "page"}
            same = all({k: v for k, v in r.items() if k != "page"} == base for r in runs.values())
            firsts = {r["page"][1] for r in runs.values()}
            ok = ok and same and base["rc"] == 0 and len(firsts) == 3
            print(f"  {game}: {'IDENTICAL' if same else 'DIFFERENT'} across the three page orders "
                  "(exit code, [MASTER] line, master, grab, backup and ledger fields)")
    print("PAGE-ORDER EVIDENCE PASS: the installed updater's result does not depend on the page's order" if ok
          else "PAGE-ORDER EVIDENCE FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
