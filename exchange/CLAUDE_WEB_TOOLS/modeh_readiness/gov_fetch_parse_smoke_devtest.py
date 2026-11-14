#!/usr/bin/env python3
"""Development test of gov_fetch_parse_smoke.py on INVENTED data with a FAKE browser (Claude web chat, 14 November 2026).
No website is contacted: the installed BrowserFetcher.fetch runs unchanged against a stand-in driver object whose page
text is built from an invented master. It reads nothing under the repository's source_data/, results/ or
transitory_data/. Not Windows evidence, and no evidence about the real page: that is what the owner-run check is for.
Usage (from a clone; selenium importable): PYTHONPATH=src:src/methods:tests python -B gov_fetch_parse_smoke_devtest.py
"""
import contextlib, hashlib, io, json, shutil, sys, tempfile
from datetime import date
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
from test_e6_beta_bernoulli import write_varied_master
from _common.game_profiles import POWERBALL, OZLOTTO
import gov_fetch_parse_smoke as SMOKE

PROFILES = {"POWERBALL": POWERBALL, "OZLOTTO": OZLOTTO}


def build(td: Path) -> Path:
    root = td / "project"
    for prof in PROFILES.values():
        write_varied_master(root, prof, prof.holdout_first, 0)
    (root / "src").mkdir()
    shutil.copy2(REPO / "src" / "results_master_v0_2.py", root / "src" / "results_master_v0_2.py")
    return root


def tree(root: Path) -> dict:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file()}


class FakeDriver:
    """Stands in for the Selenium driver: one page text per game, taken from the game's slug in the URL."""

    def __init__(self, pages, title="Results", final=None):
        self.pages, self.title, self.final, self.current_url, self.text, self.gets = pages, title, final, "", "", []

    def get(self, url):
        self.gets.append(url)
        self.current_url = self.final or url
        self.text = self.pages["OZLOTTO" if "/oz-lotto?" in url else "POWERBALL"]

    def find_element(self, by, name):
        return self

    def quit(self):
        pass


def page(RM, root, game, *, change=None, extra=()):
    """The page text for the smoke's window, in the wording the parser expects, from the INVENTED master."""
    a, b = SMOKE.WINDOW
    master = RM.Store(root, game).load_verified_master(quarantine_closed=True)[0]
    lines = []
    for d in list(master) + list(extra):
        day = date.fromisoformat(d.day)
        if not a <= day <= b and d not in extra:
            continue
        if change:
            d = change(d)
            if d is None:
                continue
        lines += [f"Draw {d.number}", f"{day.strftime('%A')} {day.day} {RM.MONTH_NAMES[day.month - 1]} {day.year}",
                  "Winning numbers:", *map(str, d.main),
                  "Powerball:" if game == "POWERBALL" else "Supplementary numbers:", *map(str, d.secondary), "View prizes"]
    return "\n".join(lines)


def run(root, driver=None, argv=(), factory=None):
    import results_master_v0_2 as RM
    def make():
        f = object.__new__(RM.BrowserFetcher)                # the real class and its real fetch(); only the driver is fake
        f.driver, f.pause, f.last, f.log = driver, 0.0, 0.0, []
        return f
    out = io.StringIO()
    before = tree(root)
    with contextlib.redirect_stdout(out):
        rc = SMOKE.main(list(argv), root=root, fetcher_factory=factory or make)
    assert tree(root) == before, "the check changed a file"
    return rc, out.getvalue()


def main() -> int:
    results = []
    with tempfile.TemporaryDirectory() as td:
        root = build(Path(td))
        sys.path.insert(0, str(root / "src"))
        import results_master_v0_2 as RM
        RM.PAGE_WAIT_SECONDS, RM.WAIT_POLL_SECONDS = 1.0, 0.2          # the test only: do not wait 15 s for a fake page
        good = {g: page(RM, root, g) for g in PROFILES}
        import dataclasses

        def case(name, want_rc, want_text, **kw):
            rc, text = run(root, **kw)
            ok = rc == want_rc and want_text in text and "Traceback" not in text
            results.append(ok)
            print(f"{'PASS' if ok else 'FAIL'} {name}: exit {rc}" + ("" if ok else f"\n{text}"))
            return text

        t = case("both games read as expected", 0, "PASS: POWERBALL, OZLOTTO", driver=FakeDriver(good))
        assert "parsed 9 draw(s) 1568-1576" in t and "parsed 9 draw(s) 1685-1693" in t and "equal to the master 9/9" in t
        drawn = [" ".join(map(str, d.main)) for g in PROFILES for d in RM.Store(root, g).load_verified_master(quarantine_closed=True)[0][-9:]]
        assert not any(x in t for x in drawn), "a drawn number sequence was printed"
        d1 = FakeDriver(good)
        case("one game only", 0, "PASS: OZLOTTO", driver=d1, argv=["--games", "OZLOTTO"])
        assert len(d1.gets) == 1 and "toDate=Fri+Jul+31+2026" in d1.gets[0] and "fromDate=Sun+May+31+2026" in d1.gets[0]
        case("a redirect to another host is refused", 3, "REFUSED: the browser's final URL is https://oz.lotterywest.com",
             driver=FakeDriver(good, final="https://oz.lotterywest.com/results"))
        case("a challenge page stops", 2, "STOP: www.lotterywest.wa.gov.au served a block/challenge page",
             driver=FakeDriver(good, title="Just a moment..."))
        q = RM.Draw("POWERBALL", 1577, "2026-08-06", (1, 2, 3, 4, 5, 6, 7), (1,))
        case("a quarantined heading on the page stops before its numbers are read", 2, "a quarantined draw appeared on the page",
             driver=FakeDriver({**good, "POWERBALL": page(RM, root, "POWERBALL", extra=[q])}))
        case("a changed page wording stops", 2, "'Winning numbers:' not found",
             driver=FakeDriver({**good, "POWERBALL": good["POWERBALL"].replace("Winning numbers:", "Results:")}))
        case("too few results stop after the wait", 2, "did not appear (expected at least 9, saw 8)",
             driver=FakeDriver({**good, "POWERBALL": page(RM, root, "POWERBALL", change=lambda d: None if d.number == 1570 else d)}))
        def swap(d):
            return dataclasses.replace(d, main=d.main[1:] + d.main[:1]) if d.number == 1690 else d
        t = case("a draw that differs from the master fails, values withheld", 1, "OZLOTTO: FAIL: parsed draw(s) 1690 differ",
                 driver=FakeDriver({**good, "OZLOTTO": page(RM, root, "OZLOTTO", change=swap)}))
        assert "equal to the master 8/9" in t
        def boom():
            raise RuntimeError("the browser did not start\nsecond line never shown")
        t = case("a browser that does not start is an error, without a traceback", 4, "ERROR: RuntimeError: the browser did not start", factory=boom)
        assert "second line" not in t
        called = []
        lock = root / "source_data" / ".results_master.lock"
        lock.write_text("x")
        case("the updater's lock refuses before any browser", 3, ".results_master.lock exists", factory=lambda: called.append(1))
        lock.unlink()
        rec = root / "source_data" / "HOLDOUT_OPENED_OZLOTTO.json"
        rec.write_text(json.dumps({"schema": "HOLDOUT_OPENED_V1", "game": "OZLOTTO", "study_manifest_sha256": "0" * 64,
                                   "opened_utc": "x", "owner_statement": "x", "freeze_version": 1, "freeze_master_sha256": "0" * 64}))
        case("an opened game refuses before any browser", 3, "OZLOTTO: the holdout is opened", factory=lambda: called.append(1))
        case("the other game still runs when asked alone", 0, "PASS: POWERBALL", driver=FakeDriver(good), argv=["--games", "POWERBALL"])
        rec.unlink()
        case("an unknown game is refused", 3, "games must be POWERBALL and/or OZLOTTO", argv=["--games", "LOTTO"], factory=lambda: called.append(1))
        assert not called, "a refusal started the browser"
        assert not list(root.rglob("__pycache__")), "byte-code was written"
    print(f"DEVTEST {sum(results)}/{len(results)} PASS" if all(results) else "DEVTEST FAILED")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
