"""The results updater: fetches new official results into this tree's own source_data, and nothing else.

What this file is for
    One results file per game holds the tree's accepted results, keyed by draw number, in drawn order:
        source_data/POWERBALL_results_master.csv    Draw_Number,Date,Drawn_1..Drawn_7,Powerball
        source_data/OZLOTTO_results_master.csv      Draw_Number,Date,Drawn_1..Drawn_7,Supp_1,Supp_2,Supp_3
    Beside each:
        source_data/<GAME>_results_master_ledger.csv   one appended line per version (append-only)
        source_data/backups/<GAME>_master_draws_<a>-<b>_as_at_<UTC>.csv   the file as it was before each update
        source_data/grabs/<GAME>_grab_draws_<a>-<b>_as_at_<UTC>.csv       what each update fetched
    An update fetches the results of the last few months, requires that every draw it fetched and the tree
    already holds agrees with the tree's file, and appends the draws that are new. A mismatch, a gap, a page it
    cannot read or a page that is not the official one changes nothing and says why.

    The one source: Lotterywest's own results-search page on www.lotterywest.wa.gov.au (the project owner's
    decision: accepted as official). Honest automation only: a headless real browser with default settings, at
    least 2 seconds between page loads, and a block or challenge page means STOP. After every redirect the
    browser's final URL must be https on exactly that host; there is no fallback source of any kind.

    It is the first system's reviewed updater (src/results_master_v0_2.py at the top level of the repository)
    with every Mode H state taken out: the quarantine of the former holdout, the opening, freeze and seal
    records, the weekly session lock, the first-update admission and the one-off "init" command are gone; the
    source, the parsing and every check of game, draw number, date, range and overlap are that program's own
    statements. One statement is added: the check of the browser's final URL is made a second time, after the
    page has finished loading and immediately before it is parsed. And the updater's own lock file is gone:
    the tree's one lock, held by whoever starts an update, stands in its place.
    deploy/compare_updater_with_frozen.py shows all of this, definition by definition and by running both on
    the same invented pages. For that reason the names and the layout of the statements are the reviewed
    program's, not this project's later style (the one exception to the coding practices in this file).

    Exit codes: 0 done (or nothing new); 1 a check failed or the files disagree; 2 STOP (a blocked page, a page
    that cannot be read); 3 refused.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 8, and section 5 step 3 (the research job
    fetches new results with it unless --no-update).

Which of the project's own modules it uses
    none: the standard library, and selenium for the browser (loaded only when a real fetch starts).

What uses it
    src/research_command.py (the program behind Run_Results_Updater.bat), research/research_job.py (at the
    start of a job, under the job's lock), and the tests (always with invented pages; no test, and neither AI,
    ever lets it reach the real site).
"""
from __future__ import annotations

import argparse
import calendar
import csv
import hashlib
import io
import os
from pathlib import Path
import re
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from types import MappingProxyType

# The version this program writes into each ledger line it adds (0.2 was the first system's updater).
TOOL_VERSION = "0.3"

# ---------------------------------------------------------------------------
# Fixed constants.
# ---------------------------------------------------------------------------
RESULTS_HOST = "www.lotterywest.wa.gov.au"   # the one origin (A6); scheme https; no fallback
DEFAULT_MONTHS_BACK = 5            # current month plus the previous 5
MAX_MONTHS_BACK = 60               # the widest window --months-back may ask for
MIN_PAUSE_SECONDS = 2.0            # the least time between two page loads; --pause may only lengthen it
PAGE_WAIT_SECONDS = 15.0           # how long a page may take to show the results asked for
WAIT_POLL_SECONDS = 0.5            # how often the page is looked at while waiting
# The columns of a ledger line, in order. The first six are what the research engine's reader uses.
LEDGER_COLUMNS = ("version", "utc", "action", "master_sha256", "first_draw", "last_draw", "draw_count",
                  "added_count", "added_first", "added_last", "grab_file", "grab_sha256",
                  "backup_file", "backup_sha256", "tool_version", "tool_sha256", "note")


@dataclass(frozen=True)
class Era:
    """One game as it has been since its present rules began: its first draw and that draw's date, its weekday
    (Monday is 0), the highest main number, how many secondary numbers (the Powerball, or the supplementaries)
    and their highest, and the game's name and code on the results page."""
    first_draw: int
    first_date: date
    weekday: int          # Monday = 0
    main_max: int
    secondary_count: int
    secondary_max: int
    slug: str
    lotterywest_code: int


# The two games. A draw's date follows from its number: one draw a week from the first.
ERAS = MappingProxyType({
    "POWERBALL": Era(1144, date(2018, 4, 19), 3, 35, 1, 20, "powerball", 5132),
    "OZLOTTO": Era(1474, date(2022, 5, 17), 1, 47, 3, 47, "oz-lotto", 5130),
})
MONTH_NAMES = tuple(calendar.month_name[1:])


class Refused(Exception):
    """The update may not start or go on as asked (exit code 3). Nothing was changed; the message says why."""


class Stop(Exception):
    """A page could not be trusted or read: a block page, a wrong weekday, numbers not where expected, a gap
    (exit code 2). Nothing but the grab, if one was made, was written."""


class VerifyFail(Exception):
    """A check of data failed: the results file and its ledger disagree, or a fetched draw disagrees with the
    one the tree holds (exit code 1). The results file is unchanged."""


@dataclass(frozen=True)
class Draw:
    """One draw: its game, number, date, the seven main numbers in drawn order, and the secondary numbers."""
    game: str
    number: int
    day: str                 # ISO date
    main: tuple[int, ...]    # drawn order
    secondary: tuple[int, ...]


# ---------------------------------------------------------------------------
# Pure rules
# ---------------------------------------------------------------------------
def derived_date(game: str, n: int) -> date:
    """The date of draw n of a game by the weekly rule, for example derived_date("POWERBALL", 1144) is
    date(2018, 4, 19)."""
    e = ERAS[game]
    return e.first_date + timedelta(days=7 * (n - e.first_draw))


def header(game: str) -> list[str]:
    """The column names of a game's results file, for example ["Draw_Number", "Date", "Drawn_1", ...,
    "Drawn_7", "Powerball"]."""
    cols = ["Draw_Number", "Date"] + [f"Drawn_{i}" for i in range(1, 8)]
    return cols + (["Powerball"] if game == "POWERBALL" else ["Supp_1", "Supp_2", "Supp_3"])


def check_constants() -> None:
    """Refuse (Refused) if the window or pause constants above are not sensible."""
    if not 1 <= DEFAULT_MONTHS_BACK <= MAX_MONTHS_BACK or MIN_PAUSE_SECONDS < 2.0:
        raise Refused("window or pause constants invalid")


def validate_draw(d: Draw) -> list[str]:
    """Raise VerifyFail on any hard error; return warnings (date off weekly rule)."""
    e = ERAS[d.game]
    day = date.fromisoformat(d.day)
    if d.number < e.first_draw:
        raise VerifyFail(f"{d.game} draw {d.number}: before the current era")
    if day.weekday() != e.weekday:
        raise VerifyFail(f"{d.game} draw {d.number}: wrong weekday")
    if len(d.main) != 7 or len(set(d.main)) != 7 or not all(1 <= x <= e.main_max for x in d.main):
        raise VerifyFail(f"{d.game} draw {d.number}: main numbers invalid")
    if (len(d.secondary) != e.secondary_count or len(set(d.secondary)) != e.secondary_count or
            not all(1 <= x <= e.secondary_max for x in d.secondary)):
        raise VerifyFail(f"{d.game} draw {d.number}: Powerball/supplementary invalid")
    if d.game == "OZLOTTO" and set(d.main) & set(d.secondary):
        raise VerifyFail(f"{d.game} draw {d.number}: supplementary overlaps a main number")
    return [] if day == derived_date(d.game, d.number) else [f"{d.game} draw {d.number}: date off the weekly rule"]


def validate_series(game: str, draws: list[Draw]) -> list[str]:
    """Consecutive from the era's first draw, every draw valid. Returns warnings."""
    if not draws:
        raise VerifyFail(f"{game}: no draws")
    warns = []
    for i, d in enumerate(draws):
        if d.game != game or d.number != ERAS[game].first_draw + i:
            raise VerifyFail(f"{game}: draws not consecutive from {ERAS[game].first_draw} (at position {i})")
        warns += validate_draw(d)
    return warns


def to_csv_bytes(game: str, draws: list[Draw]) -> bytes:
    """The bytes of a results file (or a grab) holding these draws: the header line, then one line a draw, each
    line ending CRLF."""
    out = [",".join(header(game))]
    for d in draws:
        out.append(",".join(str(x) for x in (d.number, d.day, *d.main, *d.secondary)))
    return ("\r\n".join(out) + "\r\n").encode("ascii")


def from_csv_bytes(game: str, data: bytes) -> list[Draw]:
    """The draws a results file's bytes hold, in the file's order. Raises VerifyFail on a header that is not
    the game's, a wrong number of columns, or a value that is not a number or a date."""
    rows = list(csv.reader(io.StringIO(data.decode("ascii"))))
    if not rows or rows[0] != header(game):
        raise VerifyFail(f"{game}: master/grab header not recognised")
    k = ERAS[game].secondary_count
    out = []
    for r in rows[1:]:
        if len(r) != 9 + k:
            raise VerifyFail(f"{game}: wrong column count")
        try:
            out.append(Draw(game, int(r[0]), date.fromisoformat(r[1]).isoformat(),
                            tuple(int(x) for x in r[2:9]), tuple(int(x) for x in r[9:9 + k])))
        except ValueError:
            raise VerifyFail(f"{game}: non-numeric or bad date in a row") from None
    return out


def sha(data: bytes) -> str:
    """The SHA-256 of some bytes, as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def utc_stamp() -> str:
    """The present time (UTC) as it goes into a grab's or a backup's file name, for example
    "20270120_093015Z"."""
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def write_new(path: Path, data: bytes) -> str:
    """Write a file that must not exist yet (its folder is made if needed); return the SHA-256 of its bytes.
    Raises FileExistsError if the file exists: a grab and a backup are never written over."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as fh:      # create-only
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    return sha(data)


def replace_atomically(path: Path, data: bytes) -> str:
    """Put new bytes in place of a file by writing them beside it and renaming, so that a reader finds the old
    file or the new one and never half of one; return the SHA-256 of the new bytes."""
    tmp = path.with_name(path.name + f".part-{os.getpid()}")
    with tmp.open("xb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)
    return sha(data)


def month_window(today: date, months_back: int) -> tuple[date, date]:
    """The dates an update asks for: from the first day of the month months_back months before this one, to
    today; for example month_window(date(2027, 3, 15), 5) is (date(2026, 10, 1), date(2027, 3, 15)).
    Refuses (Refused) a months_back outside 0..MAX_MONTHS_BACK."""
    if not 0 <= months_back <= MAX_MONTHS_BACK:
        raise Refused(f"--months-back must be 0..{MAX_MONTHS_BACK}")
    y, m = today.year, today.month
    for _ in range(months_back):
        y, m = (y - 1, 12) if m == 1 else (y, m - 1)
    return date(y, m, 1), today


def split_windows(a: date, b: date) -> list[tuple[date, date]]:
    """Overlapping inclusive search windows of at most ~12 months (each under the 100-draw cap).
    The first starts the day before a; the last ends exactly on b (never later)."""
    out, s = [], a - timedelta(days=1)
    while True:
        e = min(date(s.year + 1, s.month, 1), b)
        out.append((s, e))
        if e >= b:
            return out
        s = e - timedelta(days=2)


# ---------------------------------------------------------------------------
# Ledger and master
# ---------------------------------------------------------------------------
class Store:
    """One game's results file, its ledger, and the folders of its backups and grabs, in one tree."""

    def __init__(self, root: Path, game: str):
        """root: the tree.  game: "POWERBALL" or "OZLOTTO"."""
        self.root, self.game = root, game
        self.dir = root / "source_data"
        self.master = self.dir / f"{game}_results_master.csv"
        self.ledger = self.dir / f"{game}_results_master_ledger.csv"
        self.backups = self.dir / "backups"
        self.grabs = self.dir / "grabs"

    def ledger_rows(self) -> list[dict]:
        """The ledger's lines as records, oldest first ([] if there is no ledger). Raises VerifyFail if its
        columns are not LEDGER_COLUMNS."""
        if not self.ledger.is_file():
            return []
        rows = list(csv.DictReader(io.StringIO(self.ledger.read_bytes().decode("ascii"))))
        if rows and tuple(rows[0].keys()) != LEDGER_COLUMNS:
            raise VerifyFail(f"{self.ledger.name}: unexpected columns")
        return rows

    def append_ledger(self, row: dict) -> None:
        """Add one line to the end of the ledger (with the header line first if the ledger is new), and make it
        durable. row: {column: value}; columns not given are left empty."""
        exists = self.ledger.is_file()
        line = io.StringIO()
        w = csv.DictWriter(line, fieldnames=LEDGER_COLUMNS, lineterminator="\r\n")
        if not exists:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in LEDGER_COLUMNS})
        with self.ledger.open("ab") as fh:
            fh.write(line.getvalue().encode("ascii"))
            fh.flush()
            os.fsync(fh.fileno())

    def load_verified_master(self) -> tuple[list[Draw], bytes, dict]:
        """Read the results file and check it: it must be the file its ledger's last line names (by SHA-256),
        hold consecutive valid draws from the game's first, and agree with that line's counts.
        Returns (the draws, the file's bytes, the ledger's last line). Refuses (Refused) if there is no results
        file; raises VerifyFail on any disagreement."""
        if not self.master.is_file() or self.master.is_symlink():
            raise Refused(f"{self.master.name} not found (this tree holds no accepted results for {self.game}: "
                          "they are copied in when the tree is created)")
        data = self.master.read_bytes()
        rows = self.ledger_rows()
        if not rows:
            raise VerifyFail(f"{self.ledger.name} missing or empty")
        last = rows[-1]
        if sha(data) != last["master_sha256"]:
            raise VerifyFail(f"{self.master.name} does not match the last ledger entry (edited outside the tool, "
                             "or an update was interrupted: see source_data/backups and the ledger)")
        draws = from_csv_bytes(self.game, data)
        validate_series(self.game, draws)
        if len(draws) != int(last["draw_count"]) or draws[-1].number != int(last["last_draw"]):
            raise VerifyFail(f"{self.master.name} disagrees with its ledger counts")
        return draws, data, last


def tool_sha() -> str:
    """The SHA-256 of this program's own file, written into each ledger line it adds."""
    return sha(Path(__file__).read_bytes())


# ---------------------------------------------------------------------------
# UPDATE (network: run only by the project owner, on his PC)
# ---------------------------------------------------------------------------
# How a draw's heading reads on the results page: "Draw 1601 Thursday 21 January 2027".
_WEEKDAYS = "Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday"
_MONTHS = (r"Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|"
           r"Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?")
_HEAD = re.compile(rf"Draw\s+(?P<n>\d{{3,5}})\s+(?:{_WEEKDAYS})\s+(?P<d>\d{{1,2}})\s+(?P<m>{_MONTHS})\s+(?P<y>\d{{4}})")


def _month_no(tok: str) -> int:
    """The number of a month from its name or the name's first letters, for example 1 for "Jan" or "January"."""
    return [m[:3].lower() for m in MONTH_NAMES].index(tok[:3].lower()) + 1


def parse_gov(game: str, text: str, a: date, b: date) -> list[Draw]:
    """Lotterywest results-search text. Each block is checked on number/date BEFORE its numbers are read.
    game: the game asked for.  text: the page's visible text.  a, b: the dates asked for (inclusive).
    Returns the draws of the page dated a..b, in page order. Raises Stop on a wrong weekday, on numbers or
    their labels not where expected, and on a draw that is not valid."""
    heads = list(_HEAD.finditer(text))
    out = []
    for i, h in enumerate(heads):
        n = int(h.group("n"))
        day = date(int(h.group("y")), _month_no(h.group("m")), int(h.group("d")))
        if not (a <= day <= b) or n < ERAS[game].first_draw:
            continue
        if day.weekday() != ERAS[game].weekday:
            raise Stop(f"{game} draw {n}: wrong weekday (wrong game page?)")
        tok = text[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)].split()
        try:
            j = next(k for k in range(len(tok) - 1) if tok[k].lower() == "winning" and tok[k + 1].lower() == "numbers:")
        except StopIteration:
            raise Stop(f"{game} draw {n}: 'Winning numbers:' not found") from None
        j += 2
        main = []
        while j < len(tok) and re.fullmatch(r"\d{1,2}", tok[j]):
            main.append(int(tok[j])); j += 1
        if game == "POWERBALL":
            if j >= len(tok) or tok[j].lower() != "powerball:":
                raise Stop(f"{game} draw {n}: 'Powerball:' not where expected")
            j += 1
        elif j < len(tok) and tok[j].lower() == "supplementary:":
            j += 1
        elif j + 1 < len(tok) and tok[j].lower() == "supplementary" and tok[j + 1].lower() == "numbers:":
            j += 2
        else:
            raise Stop(f"{game} draw {n}: 'Supplementary' not where expected")
        sec = []
        while j < len(tok) and re.fullmatch(r"\d{1,2}", tok[j]):
            sec.append(int(tok[j])); j += 1
        d = Draw(game, n, day.isoformat(), tuple(main), tuple(sec))
        try:
            validate_draw(d)
        except VerifyFail as exc:
            raise Stop(str(exc)) from None
        out.append(d)
    return out


def gov_url(game: str, a: date, b: date) -> str:
    """The address of the official results search for a game and the dates a..b."""
    f = lambda d: d.strftime("%a+%b+%d+%Y")
    e = ERAS[game]
    return (f"https://www.lotterywest.wa.gov.au/results/{e.slug}?fromDate={f(a)}&toDate={f(b)}"
            f"&filterByGame={e.lotterywest_code}")


def check_final_url(url: str) -> None:
    """A6: after the browser followed every redirect, the final URL must be https on exactly RESULTS_HOST.
    A browser exposes no status code, so this is the check a browser allows. There is no fallback."""
    from urllib.parse import urlsplit
    parts = urlsplit(url or "")
    host = (parts.hostname or "")
    if parts.scheme != "https" or host != RESULTS_HOST:
        raise Refused(f"the browser's final URL is {parts.scheme or '(no scheme)'}://{host or '(no host)'}; only "
                      f"https://{RESULTS_HOST} is accepted and there is no fallback source. Nothing was parsed or written.")


class BrowserFetcher:
    """Real fetcher: headless, unmodified browser; only the page's own requests."""

    def __init__(self, browser: str, pause: float):
        """Start the browser. browser: "chrome" or "firefox".  pause: seconds between two page loads."""
        os.environ.setdefault("SE_AVOID_STATS", "true")
        os.environ.setdefault("SE_AVOID_BROWSER_DOWNLOAD", "true")
        from selenium import webdriver
        if browser == "chrome":
            o = webdriver.ChromeOptions(); o.add_argument("--headless=new"); o.add_argument("--window-size=1400,1000")
            self.driver = webdriver.Chrome(options=o)
        else:
            o = webdriver.FirefoxOptions(); o.add_argument("-headless")
            self.driver = webdriver.Firefox(options=o)
        self.pause, self.last, self.log = pause, 0.0, []

    def fetch(self, game: str, a: date, b: date) -> list[Draw]:
        """Load the results search for a game and the dates a..b, wait until the page shows the draws expected
        between them, and return the draws it shows. Raises Stop on a block or challenge page and when the
        results do not appear; Refused if the browser is anywhere but the official host, when the page is first
        loaded or when it has finished loading."""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.common.exceptions import TimeoutException
        url = gov_url(game, a, b)
        gap = time.monotonic() - self.last
        if self.last and gap < self.pause:
            time.sleep(self.pause - gap)
        self.last = time.monotonic()
        self.log.append({"utc": datetime.now(timezone.utc).isoformat(), "url": url})
        self.driver.get(url)
        if any(k in (self.driver.title or "").lower() for k in ("attention required", "cloudflare", "access denied", "just a moment")):
            raise Stop("www.lotterywest.wa.gov.au served a block/challenge page; nothing was bypassed")
        check_final_url(self.driver.current_url)
        inner, n = [], ERAS[game].first_draw
        while derived_date(game, n) < b:
            if derived_date(game, n) > a:
                inner.append(n)
            n += 1
        seen = {"headings": 0}

        def ready(d):
            """The page's text once it shows at least the headings expected, else False (keep waiting)."""
            t = d.find_element(By.TAG_NAME, "body").text
            seen["headings"] = sum(1 for h in _HEAD.finditer(t)
                                   if a < date(int(h.group("y")), _month_no(h.group("m")), int(h.group("d"))) < b)
            return t if seen["headings"] >= len(inner) else False
        try:
            text = WebDriverWait(self.driver, PAGE_WAIT_SECONDS, poll_frequency=WAIT_POLL_SECONDS).until(ready)
        except TimeoutException:
            raise Stop(f"results for {a}..{b} did not appear (expected at least {len(inner)}, saw {seen['headings']})") from None
        # The one statement that is not the first system's: the final-URL check again, now that the page has
        # finished loading and immediately before it is parsed (the reviewer's reading of step 3).
        check_final_url(self.driver.current_url)
        return parse_gov(game, text, a, b)

    def close(self):
        """End the browser this fetcher started."""
        self.driver.quit()


def update_game(root: Path, game: str, fetcher, months_back: int, today: date) -> dict:
    """Update one game's results file in a tree.

    root: the tree.  fetcher: gives the draws the source shows for a game and two dates (fetch(game, a, b)).
    months_back, today: the window asked for (month_window).
    What was fetched is kept as a grab. Every fetched draw the tree already holds must equal the tree's; the
    draws beyond the tree's last must follow it with no gap. Then either one NO_CHANGE line is added to the
    ledger, or the old file is kept as a backup, the new file is put in place, one UPDATE line is added and the
    file is read back and checked.
    Returns, for example, {"game": "POWERBALL", "checked": 20, "added": 2, "added_range": "1601..1602",
    "warnings": [], "grab": "<file name>", "backup": "<file name>"}.
    Raises Refused (no overlap with what the tree holds), Stop (the searches disagree; a gap in what was
    fetched) or VerifyFail (a fetched draw disagrees with the tree's; new draws not consecutive)."""
    st = Store(root, game)
    a, b = month_window(today, months_back)
    master, master_bytes, last = st.load_verified_master()
    got: dict[int, Draw] = {}
    for (wa, wb) in split_windows(a, b):
        for d in fetcher.fetch(game, wa, wb):
            if d.number in got and got[d.number] != d:
                raise Stop(f"{game} draw {d.number}: overlapping searches disagree")
            got[d.number] = d
    got = {k: d for k, d in got.items() if a <= date.fromisoformat(d.day) <= b}
    grab = sorted(got.values(), key=lambda d: d.number)
    if any(y.number != x.number + 1 for x, y in zip(grab, grab[1:])):
        raise Stop(f"{game}: the grab has a gap in draw numbers; nothing written")
    stamp = utc_stamp()
    span = f"{grab[0].number}-{grab[-1].number}" if grab else "none"
    grab_path = st.grabs / f"{game}_grab_draws_{span}_as_at_{stamp}.csv"
    grab_sha = write_new(grab_path, to_csv_bytes(game, grab))
    by_no = {d.number: d for d in master}
    overlap = [d for d in grab if d.number in by_no]
    if not overlap:
        raise Refused(f"{game}: the grab does not overlap the master (gap risk); widen --months-back")
    bad = [d.number for d in overlap if by_no[d.number] != d]
    if bad:
        raise VerifyFail(f"{game}: {len(bad)} overlapping draw(s) disagree with the master "
                         f"(draws {', '.join(map(str, bad[:10]))}); master unchanged; grab kept as {grab_path.name}")
    new = [d for d in grab if d.number > master[-1].number]
    expect = master[-1].number + 1
    for d in new:
        if d.number != expect:
            raise VerifyFail(f"{game}: new draws not consecutive (expected {expect}, got {d.number}); master unchanged")
        expect += 1
    warns = [w for d in new for w in validate_draw(d)]
    version = int(last["version"]) + 1
    row = {"version": version, "utc": datetime.now(timezone.utc).isoformat(), "grab_file": grab_path.name,
           "grab_sha256": grab_sha, "tool_version": TOOL_VERSION, "tool_sha256": tool_sha(),
           "first_draw": master[0].number}
    if not new:
        row.update({"action": "NO_CHANGE", "master_sha256": last["master_sha256"], "last_draw": master[-1].number,
                    "draw_count": len(master), "added_count": 0, "note": f"{len(overlap)} overlapping draws matched"})
        st.append_ledger(row)
        return {"game": game, "checked": len(overlap), "added": 0, "warnings": warns, "grab": grab_path.name}
    backup = st.backups / f"{game}_master_draws_{master[0].number}-{master[-1].number}_as_at_{stamp}.csv"
    backup_sha = write_new(backup, master_bytes)
    merged = master + new
    validate_series(game, merged)
    h = replace_atomically(st.master, to_csv_bytes(game, merged))
    row.update({"action": "UPDATE", "master_sha256": h, "last_draw": merged[-1].number, "draw_count": len(merged),
                "added_count": len(new), "added_first": new[0].number, "added_last": new[-1].number,
                "backup_file": backup.name, "backup_sha256": backup_sha,
                "note": f"{len(overlap)} overlapping draws matched; {len(warns)} date warnings"})
    st.append_ledger(row)
    st.load_verified_master()
    return {"game": game, "checked": len(overlap), "added": len(new), "added_range": f"{new[0].number}..{new[-1].number}",
            "warnings": warns, "grab": grab_path.name, "backup": backup.name}


def cmd_update(root: Path, games: list[str], months_back: int, browser: str, pause: float,
               fetcher_factory=None, today: date | None = None) -> int:
    """Update the results files of the named games in a tree, and say what was done.

    root: the tree.  games: for example ["POWERBALL", "OZLOTTO"].  months_back: previous months to ask for
    besides the current one.  browser, pause: for the real fetcher.  fetcher_factory: makes the fetcher (a test
    gives one that reads invented pages; left out, the real browser is started).  today: the last date asked for
    (left out, the PC's date).
    The caller holds the tree's lock (research/tree_lock.py): the research job, or the command program when
    the updater is started by itself. The first system's updater had a lock of its own; the tree's one lock
    stands in its place.
    Returns 0. Raises Refused, Stop or VerifyFail as update_game does; a game after the one that failed is not
    worked."""
    check_constants()
    if pause < MIN_PAUSE_SECONDS:
        raise Refused(f"--pause must be at least {MIN_PAUSE_SECONDS}")
    today = today or date.today()
    fetcher = (fetcher_factory or (lambda: BrowserFetcher(browser, pause)))()
    try:
        results = [update_game(root, g, fetcher, months_back, today) for g in games]
    finally:
        getattr(fetcher, "close", lambda: None)()
    for r in results:
        print(f"[MASTER] {r['game']}: checked {r['checked']} overlapping draws (all matched), added {r['added']}"
              + (f" ({r['added_range']})" if r.get("added_range") else "") + f", warnings {len(r['warnings'])}")
        for w in r["warnings"]:
            print(f"[MASTER]   warning: {w}")
        print(f"[MASTER]   grab kept: {r['grab']}" + (f"; backup: {r['backup']}" if r.get("backup") else ""))
    return 0


def main(argv, root: Path) -> int:
    """The command line of Run_Results_Updater.bat.

    argv: what the owner typed after the command, for example ["--months-back", "11"].
    root: the tree the launcher lies in; only its source_data is written.
    Returns the exit code: 0 done (or nothing new); 1 a check failed; 2 STOP; 3 refused."""
    p = argparse.ArgumentParser(prog="Run_Results_Updater.bat",
                                description=f"Fetch new official results into this tree (updater v{TOOL_VERSION})")
    p.add_argument("--games", default="POWERBALL,OZLOTTO")
    p.add_argument("--months-back", type=int, default=DEFAULT_MONTHS_BACK,
                   help=f"previous months to include besides the current one (0..{MAX_MONTHS_BACK})")
    p.add_argument("--browser", choices=("chrome", "firefox"), default="chrome")
    p.add_argument("--pause", type=float, default=MIN_PAUSE_SECONDS)
    a = p.parse_args(argv)
    try:
        games = [g.strip().upper() for g in a.games.split(",") if g.strip()]
        if not games or any(g not in ERAS for g in games):
            raise Refused("games must be POWERBALL and/or OZLOTTO")
        return cmd_update(Path(root), games, a.months_back, a.browser, a.pause)
    except Refused as exc:
        print(f"[MASTER] REFUSED: {exc}", file=sys.stderr); return 3
    except Stop as exc:
        print(f"[MASTER] STOP: {exc}", file=sys.stderr); return 2
    except VerifyFail as exc:
        print(f"[MASTER] VERIFY FAIL: {exc}", file=sys.stderr); return 1
    except OSError as exc:
        print(f"[MASTER] FILE ERROR: {exc} (is a file open in another program?)", file=sys.stderr); return 1
