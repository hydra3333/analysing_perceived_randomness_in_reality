"""Two-site lottery results check: The Lott versus Lotterywest. v0.1 TEST BUILD.

PRIVATE, OWNER-RUN, DEVELOPMENT DATA ONLY. Place this file in the project's src/
folder and run it with the project's .venv Python (3.14).

What it does
- Drives a real, unmodified browser (Chrome or Firefox) with Selenium, headless.
- For each requested month and game it:
    * opens The Lott results page, picks the month and year, clicks Find, makes
      sure the "Drawn" order is selected, and reads that month's draws;
    * opens the matching Lotterywest month page and reads the same month's draws.
- Writes both sets to CSV in a private, git-ignored run folder, and writes a
  value-free reconciliation report (PASS/FAIL per draw and field, no numbers).

Honest automation (project safeguard: no impersonation, no bot-protection bypass)
- Default browser settings only: no stealth flags, no User-Agent change, the
  browser's normal "automated" signal is left visible, no calls to any site API,
  no CAPTCHA or challenge handling. A missing expected page element means STOP.
- At least MIN_PAUSE_SECONDS between every page load or click.
- Selenium Manager usage statistics and browser downloads are switched off.

Quarantine (holdout) enforcement - fixed constants, no command-line override
- Months after LAST_ALLOWED_MONTH (July 2026) are never requested.
- Any draw at or above FIRST_QUARANTINED_DRAW, or dated on/after
  QUARANTINE_START_DATE, stops the run immediately: nothing is saved or printed
  and its numbers are never read.
- v0.1 limit: at most RUN_MONTH_LIMIT months per run (default January-February 2026).

Run
    python src\\two_site_results_check_v0_1.py --self-test
    python src\\two_site_results_check_v0_1.py --browser chrome
Exit codes: 0 all PASS; 1 mismatches or incomplete; 2 STOP (quarantine, blocked,
page not recognised); 3 usage/configuration refused.
"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from types import MappingProxyType

TOOL_VERSION = "0.1"

# ---------------------------------------------------------------------------
# FIXED QUARANTINE BOUNDARY (owner decision pending ratification: month-aligned,
# August 2026). Edit only after review. There is deliberately no CLI override.
# ---------------------------------------------------------------------------
QUARANTINE_START_DATE = date(2026, 8, 1)
LAST_ALLOWED_MONTH = (2026, 7)
FIRST_QUARANTINED_DRAW = MappingProxyType({"POWERBALL": 1577, "OZLOTTO": 1694})
RUN_MONTH_LIMIT = 2
DEFAULT_FROM = (2026, 1)
DEFAULT_TO = (2026, 2)
MIN_PAUSE_SECONDS = 2.0
PAGE_WAIT_SECONDS = 30.0
WAIT_POLL_SECONDS = 0.5
OUTPUT_FOLDER_NAME = "private_results_checks"


@dataclass(frozen=True)
class Era:
    first_draw: int
    first_date: date
    first_month: tuple[int, int]
    main_max: int
    secondary_count: int
    secondary_max: int
    secondary_label: str
    lott_slug: str
    lotterywest_slug: str
    lott_heading: str


ERAS = MappingProxyType({
    "POWERBALL": Era(1144, date(2018, 4, 19), (2018, 4), 35, 1, 20, "Powerball",
                     "powerball", "powerball", "Search Powerball Results"),
    "OZLOTTO": Era(1474, date(2022, 5, 17), (2022, 5), 47, 3, 47, "Supplementary",
                   "oz-lotto", "oz-lotto", "Search Oz Lotto Results"),
})
MAIN_COUNT = 7
MONTH_NAMES = tuple(calendar.month_name[1:])  # January..December (English)


class UsageRefused(Exception):
    """Configuration refused before any browser starts."""


class QuarantineStop(Exception):
    """A quarantined draw was encountered. Its numbers are never read or kept."""


class BlockedStop(Exception):
    """Site did not show the expected page (blocked, challenged or changed)."""


class ParseFailure(Exception):
    """A development draw could not be parsed strictly (draw number only)."""


# ---------------------------------------------------------------------------
# Pure functions (covered by --self-test; no browser, no network)
# ---------------------------------------------------------------------------
def derived_date(game: str, draw_number: int) -> date:
    era = ERAS[game]
    return era.first_date + timedelta(days=7 * (draw_number - era.first_draw))


def check_boundary_constants() -> None:
    """Fail closed unless the fixed constants agree with each other."""
    last = date(LAST_ALLOWED_MONTH[0], LAST_ALLOWED_MONTH[1],
                calendar.monthrange(*LAST_ALLOWED_MONTH)[1])
    if last + timedelta(days=1) != QUARANTINE_START_DATE:
        raise UsageRefused("boundary constants disagree (last allowed month vs start date)")
    for game, first_q in FIRST_QUARANTINED_DRAW.items():
        if not (derived_date(game, first_q) >= QUARANTINE_START_DATE >
                derived_date(game, first_q - 1)):
            raise UsageRefused(f"{game}: first quarantined draw is not the first draw of the boundary month")
    if RUN_MONTH_LIMIT < 1 or MIN_PAUSE_SECONDS < 2.0:
        raise UsageRefused("run limit or pause constant invalid")


def month_list(frm: tuple[int, int], to: tuple[int, int]) -> list[tuple[int, int]]:
    for y, m in (frm, to):
        if not (1 <= m <= 12 and 2000 <= y <= 2100):
            raise UsageRefused("invalid month")
    if frm > to:
        raise UsageRefused("start month is after end month")
    months, (y, m) = [], frm
    while (y, m) <= to:
        months.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return months


def validate_request(games: list[str], frm: tuple[int, int], to: tuple[int, int]) -> list[tuple[int, int]]:
    """Refuse anything that could request a quarantined month."""
    check_boundary_constants()
    if not games or any(g not in ERAS for g in games) or len(set(games)) != len(games):
        raise UsageRefused("games must be POWERBALL and/or OZLOTTO")
    months = month_list(frm, to)
    if any(mon > LAST_ALLOWED_MONTH for mon in months):
        raise UsageRefused("requested month is in or after the quarantine boundary month (August 2026)")
    if len(months) > RUN_MONTH_LIMIT:
        raise UsageRefused(f"v0.1 test build allows at most {RUN_MONTH_LIMIT} months per run")
    for g in games:
        if to < ERAS[g].first_month:
            raise UsageRefused(f"{g}: whole range is before the current era")
    return months


def expected_draws(game: str, year: int, month: int) -> list[int]:
    """Development draw numbers whose derived weekly date falls in the month."""
    era = ERAS[game]
    out, n = [], era.first_draw
    while derived_date(game, n) < date(year, month, 1):
        n += 1
    while derived_date(game, n).month == month and derived_date(game, n).year == year:
        if n < FIRST_QUARANTINED_DRAW[game]:
            out.append(n)
        n += 1
    return out


def classify(game: str, draw_number: int, draw_date: date) -> str:
    """Return 'PRE_ERA' or 'DEV'. Raise QuarantineStop BEFORE numbers are read."""
    if draw_number >= FIRST_QUARANTINED_DRAW[game] or draw_date >= QUARANTINE_START_DATE:
        raise QuarantineStop(game)
    if draw_number < ERAS[game].first_draw:
        return "PRE_ERA"
    return "DEV"


@dataclass(frozen=True)
class Record:
    game: str
    draw_number: int
    draw_date: str
    main: tuple[int, ...]
    secondary: tuple[int, ...]
    source: str
    order_label: str


def validate_numbers(game: str, draw_number: int, main: list[int], secondary: list[int]) -> None:
    era = ERAS[game]
    if len(main) != MAIN_COUNT or len(set(main)) != MAIN_COUNT:
        raise ParseFailure(f"{game} draw {draw_number}: main numbers count/distinct check failed")
    if not all(1 <= x <= era.main_max for x in main):
        raise ParseFailure(f"{game} draw {draw_number}: main number out of range")
    if len(secondary) != era.secondary_count or len(set(secondary)) != era.secondary_count:
        raise ParseFailure(f"{game} draw {draw_number}: {era.secondary_label} count/distinct check failed")
    if not all(1 <= x <= era.secondary_max for x in secondary):
        raise ParseFailure(f"{game} draw {draw_number}: {era.secondary_label} out of range")
    if game == "OZLOTTO" and set(main) & set(secondary):
        raise ParseFailure(f"{game} draw {draw_number}: supplementary overlaps a main number")


_MONTHS_RE = "|".join(MONTH_NAMES)
_LW_HEADER = re.compile(
    rf"(?P<day>\d{{1,2}})\s+(?P<mon>{_MONTHS_RE})\s+(?P<year>\d{{4}})\s*"
    rf"(?:(?P<time>\d{{1,2}}:\d{{2}}\s*[ap]m))?\s*Draw\s*(?P<draw>\d{{3,5}})", re.IGNORECASE)
_DIGITS = re.compile(r"\d{1,2}\Z")


def _take_numbers(tokens: list[str], start: int) -> tuple[list[int], int]:
    nums, i = [], start
    while i < len(tokens) and _DIGITS.fullmatch(tokens[i]):
        nums.append(int(tokens[i]))
        i += 1
    return nums, i


def parse_lotterywest_text(game: str, year: int, month: int, text: str) -> tuple[list[Record], dict]:
    """Strict parser for a Lotterywest month page's visible text.

    Each draw header is classified on draw number and date FIRST; a quarantined
    header stops everything before its numbers are tokenised. Draws from other
    months are ignored without reading their numbers.
    """
    era = ERAS[game]
    headers = list(_LW_HEADER.finditer(text))
    records, info = [], {"headers": len(headers), "other_month_ignored": 0, "pre_era_ignored": 0,
                         "times_seen": set()}
    for idx, h in enumerate(headers):
        mon = MONTH_NAMES.index(h.group("mon").capitalize()) + 1
        d = date(int(h.group("year")), mon, int(h.group("day")))
        n = int(h.group("draw"))
        if classify(game, n, d) == "PRE_ERA":
            info["pre_era_ignored"] += 1
            continue
        if (d.year, d.month) != (year, month):
            info["other_month_ignored"] += 1
            continue
        if h.group("time"):
            info["times_seen"].add(re.sub(r"\s+", " ", h.group("time").lower()))
        body = text[h.end(): headers[idx + 1].start() if idx + 1 < len(headers) else len(text)]
        tokens = body.split()
        try:
            i = next(k for k in range(len(tokens) - 1)
                     if tokens[k].lower() == "main" and tokens[k + 1].lower().startswith("number"))
        except StopIteration:
            raise ParseFailure(f"{game} draw {n}: 'Main numbers' label not found") from None
        main, i = _take_numbers(tokens, i + 2)
        if i >= len(tokens) or tokens[i].lower() != era.secondary_label.lower():
            raise ParseFailure(f"{game} draw {n}: '{era.secondary_label}' label not where expected")
        secondary, _ = _take_numbers(tokens, i + 1)
        validate_numbers(game, n, main, secondary)
        records.append(Record(game, n, d.isoformat(), tuple(main), tuple(secondary),
                              "LOTTERYWEST_MONTH_PAGE", "SOURCE_SEQUENCE"))
    info["times_seen"] = sorted(info["times_seen"])
    return records, info


_LOTT_DATE = re.compile(r"(?:[A-Z][a-z]{2},?\s+)?(\d{1,2})\s+([A-Z][a-z]{2,8})\s+(\d{4})")
_LOTT_DRAW = re.compile(r"Draw\s+(\d{3,5})")


def parse_lott_date(text: str) -> date:
    m = _LOTT_DATE.search(text or "")
    if not m:
        raise ValueError("date not recognised")
    day, mon, yr = m.groups()
    for fmt in ("%d %b %Y", "%d %B %Y"):
        try:
            return datetime.strptime(f"{day} {mon} {yr}", fmt).date()
        except ValueError:
            continue
    raise ValueError("date not recognised")


def lott_block_record(game: str, year: int, month: int, draw_text: str, date_text: str,
                      primary_texts: list[str], secondary_texts: list[str], order_label: str) -> Record | None:
    """Validate one The Lott draw block. Numbers are only converted after classify()."""
    m = _LOTT_DRAW.search(draw_text or "")
    if not m:
        raise ParseFailure(f"{game}: draw label not recognised")
    n = int(m.group(1))
    d = parse_lott_date(date_text)
    if classify(game, n, d) == "PRE_ERA":
        return None
    if (d.year, d.month) != (year, month):
        raise ParseFailure(f"{game} draw {n}: block is not in the requested month")
    try:
        main = [int(t.strip()) for t in primary_texts]
        secondary = [int(t.strip()) for t in secondary_texts]
    except ValueError:
        raise ParseFailure(f"{game} draw {n}: non-numeric ball text") from None
    validate_numbers(game, n, main, secondary)
    return Record(game, n, d.isoformat(), tuple(main), tuple(secondary), "THELOTT_MONTH_SEARCH", order_label)


def reconcile(game: str, months: list[tuple[int, int]], lott: list[Record], lw: list[Record]) -> tuple[list[str], dict]:
    """Value-free comparison: PASS/FAIL per draw and field, never numbers."""
    expected = sorted(n for (y, m) in months for n in expected_draws(game, y, m))
    a = {r.draw_number: r for r in lott}
    b = {r.draw_number: r for r in lw}
    lines, counts = [], {"expected": len(expected), "lott": len(a), "lotterywest": len(b),
                         "all_pass": 0, "fail": 0}
    sec = ERAS[game].secondary_label.lower()
    for n in sorted(set(expected) | set(a) | set(b)):
        x, y = a.get(n), b.get(n)
        if n not in expected:
            lines.append(f"{game} {n}: UNEXPECTED draw number for these months")
            counts["fail"] += 1
            continue
        if x is None or y is None:
            lines.append(f"{game} {n}: MISSING from " + ("The Lott" if x is None else "Lotterywest")
                         + ("" if (x or y) else " and Lotterywest"))
            counts["fail"] += 1
            continue
        checks = {
            "date": x.draw_date == y.draw_date,
            "date_vs_weekly_rule": x.draw_date == derived_date(game, n).isoformat(),
            "main_set": set(x.main) == set(y.main),
            "main_order": (x.main == y.main) if x.order_label == "DRAWN_SELECTED" else None,
            f"{sec}_set": set(x.secondary) == set(y.secondary),
            f"{sec}_order": (x.secondary == y.secondary) if x.order_label == "DRAWN_SELECTED" else None,
        }
        ok = all(v is not False for v in checks.values())
        counts["all_pass" if ok else "fail"] += 1
        lines.append(f"{game} {n}: " + ", ".join(
            f"{k} {'PASS' if v else ('N/A' if v is None else 'FAIL')}" for k, v in checks.items()))
    return lines, counts


def csv_rows(game: str, records: list[Record]) -> list[list]:
    sec = (["Powerball"] if game == "POWERBALL" else ["Supp_1", "Supp_2", "Supp_3"])
    rows = [["Game", "Draw_Number", "Date"] + [f"Drawn_{i}" for i in range(1, 8)] + sec + ["Source", "Order_Label"]]
    for r in sorted(records, key=lambda r: r.draw_number):
        rows.append([game, r.draw_number, r.draw_date, *r.main, *r.secondary, r.source, r.order_label])
    return rows


def make_run_dir(base: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run = base / f"run_{stamp}_{secrets.token_hex(3)}"
    base.mkdir(parents=True, exist_ok=True)
    run.mkdir(exist_ok=False)  # create-only
    return run


def write_new(path: Path, data: bytes) -> str:
    with path.open("xb") as fh:  # never overwrite
        fh.write(data)
    return hashlib.sha256(data).hexdigest()


def csv_bytes(rows: list[list]) -> bytes:
    lines = [",".join(str(c) for c in row) for row in rows]
    return ("\r\n".join(lines) + "\r\n").encode("ascii")


# ---------------------------------------------------------------------------
# Browser part (Selenium imported lazily so --self-test needs no browser)
# ---------------------------------------------------------------------------
class Pacer:
    def __init__(self, seconds: float):
        self.seconds, self.last = seconds, 0.0
        self.log: list[dict] = []

    def wait(self, action: str, target: str) -> None:
        gap = time.monotonic() - self.last
        if self.last and gap < self.seconds:
            time.sleep(self.seconds - gap)
        self.last = time.monotonic()
        self.log.append({"utc": datetime.now(timezone.utc).isoformat(), "action": action, "target": target})


def make_driver(browser: str):
    os.environ.setdefault("SE_AVOID_STATS", "true")              # no usage statistics
    os.environ.setdefault("SE_AVOID_BROWSER_DOWNLOAD", "true")   # use the installed browser
    from selenium import webdriver
    if browser == "chrome":
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless=new")       # nothing displayed on screen
        opts.add_argument("--window-size=1400,1000")
        return webdriver.Chrome(options=opts)
    opts = webdriver.FirefoxOptions()
    opts.add_argument("-headless")
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1400, 1000)
    return driver


def _wait(driver, condition, what: str):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException
    try:
        return WebDriverWait(driver, PAGE_WAIT_SECONDS, poll_frequency=WAIT_POLL_SECONDS).until(condition)
    except TimeoutException:
        raise BlockedStop(f"expected page content did not appear: {what}") from None


def fetch_lott_month(driver, pacer: Pacer, game: str, year: int, month: int) -> tuple[list[Record], dict]:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    era = ERAS[game]
    url = f"https://www.thelott.com/{era.lott_slug}/results"
    pacer.wait("load", url)
    driver.get(url)
    # Only the search controls are touched; the page's default result block is never read.
    _wait(driver, lambda d: d.find_elements(By.CSS_SELECTOR, "section.results-search select.select-month"),
          "The Lott month selector")
    month_el = driver.find_element(By.CSS_SELECTOR, "section.results-search select.select-month")
    year_el = driver.find_element(By.CSS_SELECTOR, "section.results-search select.select-year")
    Select(month_el).select_by_visible_text(MONTH_NAMES[month - 1])
    Select(year_el).select_by_visible_text(str(year))
    find_btn = driver.find_element(By.CSS_SELECTOR, "section.results-search button.button-find")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", find_btn)
    pacer.wait("click Find", f"{url} {MONTH_NAMES[month - 1]} {year}")
    find_btn.click()

    def requested_month_shown(d):
        # Reads ONLY draw labels and dates, never ball numbers, until the
        # result block shows exactly the requested month.
        res = d.find_elements(By.CSS_SELECTOR, "section.results-search default-results")
        if not res:
            return False
        found = res[0].find_elements(By.CSS_SELECTOR, ".draws-found")
        m = re.search(r"(\d+)\s+draws?\s+found", found[0].text if found else "")
        if not m:
            return False
        rows = res[0].find_elements(By.XPATH, ".//lotto-numbers/ancestor::*[.//*[contains(@class,'draw-num')]][1]")
        if len(rows) != int(m.group(1)):
            return False
        for row in rows:
            dates = row.find_elements(By.CSS_SELECTOR, "[class*='text-right'] span")
            try:
                dd = parse_lott_date(dates[0].text if dates else "")
            except ValueError:
                return False
            if (dd.year, dd.month) != (year, month):
                return False
        return (res[0], rows)

    res, rows = _wait(driver, requested_month_shown, f"The Lott results for {MONTH_NAMES[month-1]} {year}")

    def drawn_button(container):
        found = [b for b in container.find_elements(By.CSS_SELECTOR, ".ball-order button")
                 if b.text.strip().lower() == "drawn"]
        return found[0] if found else None

    order_label = "ORDER_UNCONFIRMED"
    button = drawn_button(res)
    if button is not None and button.get_attribute("disabled") is None:   # Drawn not active yet
        pacer.wait("click Drawn", url)
        button.click()
        time.sleep(WAIT_POLL_SECONDS)
        res, rows = _wait(driver, requested_month_shown, "The Lott results after Drawn order")
        button = drawn_button(res)
    if button is not None and button.get_attribute("disabled") is not None:  # active = disabled
        order_label = "DRAWN_SELECTED"

    records, pre_era = [], 0
    for row in rows:
        draw_text = row.find_element(By.CSS_SELECTOR, "[class*='draw-num']").text
        dates = row.find_elements(By.CSS_SELECTOR, "[class*='text-right'] span")
        m = _LOTT_DRAW.search(draw_text)
        if m:  # classify on number and date BEFORE any ball text is read
            classify(game, int(m.group(1)), parse_lott_date(dates[0].text if dates else ""))
        primary = [e.text for e in row.find_elements(By.CSS_SELECTOR, ".primary-numbers .number")]
        secondary = [e.text for e in row.find_elements(By.CSS_SELECTOR, ".secondary-numbers > div")]
        rec = lott_block_record(game, year, month, draw_text, dates[0].text if dates else "",
                                primary, secondary, order_label)
        if rec is None:
            pre_era += 1
        else:
            records.append(rec)
    return records, {"url": url, "order_label": order_label, "blocks": len(rows), "pre_era_ignored": pre_era}


def fetch_lotterywest_month(driver, pacer: Pacer, game: str, year: int, month: int) -> tuple[list[Record], dict]:
    from selenium.webdriver.common.by import By
    era = ERAS[game]
    url = f"https://www.oz.lotterywest.com/{era.lotterywest_slug}/results/{MONTH_NAMES[month-1].lower()}-{year}"
    pacer.wait("load", url)
    driver.get(url)
    _wait(driver, lambda d: d.execute_script("return document.readyState") == "complete", "Lotterywest page load")

    def month_blocks_present(d):
        text = d.find_element(By.TAG_NAME, "body").text
        hits = [h for h in _LW_HEADER.finditer(text)
                if h.group("mon").capitalize() == MONTH_NAMES[month - 1] and int(h.group("year")) == year]
        return text if hits else False

    text = _wait(driver, month_blocks_present, f"Lotterywest results for {MONTH_NAMES[month-1]} {year}")
    records, info = parse_lotterywest_text(game, year, month, text)
    info["url"] = url
    return records, info


def git_ignored(root: Path, path: Path) -> bool | None:
    try:
        r = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", str(path)],
                           capture_output=True, timeout=20, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.returncode == 0 if r.returncode in (0, 1) else None


def run(args) -> int:
    games = [g.strip().upper() for g in args.games.split(",")]
    frm = tuple(int(x) for x in args.from_month.split("-"))
    to = tuple(int(x) for x in args.to_month.split("-"))
    months = validate_request(games, frm, to)
    if args.pause < MIN_PAUSE_SECONDS:
        raise UsageRefused(f"pause must be at least {MIN_PAUSE_SECONDS} s")
    root = Path(__file__).resolve().parents[1]
    base = root / OUTPUT_FOLDER_NAME
    ignored = git_ignored(root, base / "probe.csv")
    if ignored is False:
        raise UsageRefused(f"{OUTPUT_FOLDER_NAME}/ is not git-ignored; add it to .gitignore first")
    if ignored is None:
        print(f"[CHECK] WARNING: could not confirm {OUTPUT_FOLDER_NAME}/ is git-ignored (git unavailable)", flush=True)

    pacer = Pacer(args.pause)
    started = datetime.now(timezone.utc).isoformat()
    results: dict = {}
    driver = make_driver(args.browser)
    meta = {}
    try:
        meta = {"browser": driver.capabilities.get("browserName"),
                "browser_version": driver.capabilities.get("browserVersion"),
                "user_agent_unmodified": driver.execute_script("return navigator.userAgent"),
                "navigator_webdriver_visible": driver.execute_script("return navigator.webdriver")}
        for game in games:
            results[game] = {"lott": [], "lw": [], "info": []}
            for (y, m) in months:
                if (y, m) < ERAS[game].first_month:
                    continue
                try:
                    lott, li = fetch_lott_month(driver, pacer, game, y, m)
                    lw, wi = fetch_lotterywest_month(driver, pacer, game, y, m)
                except (QuarantineStop, ParseFailure, BlockedStop, UsageRefused):
                    raise
                except Exception as exc:  # browser/page errors: type name only, never page text
                    raise BlockedStop(f"browser or page error ({type(exc).__name__}) in {game} {y}-{m:02d}") from None
                results[game]["lott"] += lott
                results[game]["lw"] += lw
                results[game]["info"].append({"month": f"{y}-{m:02d}", "thelott": li, "lotterywest": wi})
                print(f"[CHECK] {game} {y}-{m:02d}: The Lott {len(lott)} draws, Lotterywest {len(lw)} draws, "
                      f"expected {len(expected_draws(game, y, m))}", flush=True)
    finally:
        driver.quit()

    run_dir = make_run_dir(base)
    hashes, report, summary = {}, [], {}
    for game, data in results.items():
        hashes[f"thelott_{game}.csv"] = write_new(run_dir / f"thelott_{game}.csv", csv_bytes(csv_rows(game, data["lott"])))
        hashes[f"lotterywest_{game}.csv"] = write_new(run_dir / f"lotterywest_{game}.csv", csv_bytes(csv_rows(game, data["lw"])))
        lines, counts = reconcile(game, months, data["lott"], data["lw"])
        report += lines
        summary[game] = counts
    report_text = "\r\n".join(["TWO-SITE RESULTS CHECK (value-free)", *report, "",
                               json.dumps(summary, sort_keys=True)]) + "\r\n"
    hashes["reconciliation.txt"] = write_new(run_dir / "reconciliation.txt", report_text.encode("ascii"))
    prov = {"tool_version": TOOL_VERSION, "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "python": sys.version, "selenium": _selenium_version(), **meta, "headless": True,
            "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
            "games": games, "months": [f"{y}-{m:02d}" for y, m in months], "pause_seconds": args.pause,
            "quarantine": {"start_date": QUARANTINE_START_DATE.isoformat(),
                           "first_quarantined_draw": dict(FIRST_QUARANTINED_DRAW)},
            "actions": pacer.log, "per_month": {g: d["info"] for g, d in results.items()},
            "summary": summary, "output_sha256": hashes, "git_ignored_output": ignored}
    write_new(run_dir / "provenance.json", json.dumps(prov, indent=1, sort_keys=True, default=str).encode("utf-8"))
    for line in report:
        print("[CHECK] " + line)
    print(f"[CHECK] summary {json.dumps(summary, sort_keys=True)}")
    print(f"[CHECK] files in {run_dir}")
    complete = all(c["fail"] == 0 and c["all_pass"] == c["expected"] for c in summary.values())
    return 0 if complete else 1


def _selenium_version() -> str | None:
    try:
        import importlib.metadata as md
        return md.version("selenium")
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Self-test: blockout logic and parsers, synthetic data only (invented numbers)
# ---------------------------------------------------------------------------
def self_test() -> int:
    results = []

    def check(name, fn):
        try:
            fn()
            results.append((name, True))
        except AssertionError as exc:
            results.append((name, False))
            print(f"[SELF-TEST] FAIL {name}: {exc}")

    def refused(fn, exc=UsageRefused):
        try:
            fn()
        except exc:
            return True
        return False

    def t_constants():
        check_boundary_constants()
        assert derived_date("POWERBALL", 1576) == date(2026, 7, 30)
        assert derived_date("POWERBALL", 1577) == date(2026, 8, 6)
        assert derived_date("OZLOTTO", 1693) == date(2026, 7, 28)
        assert derived_date("OZLOTTO", 1694) == date(2026, 8, 4)

    def t_months():
        assert validate_request(["POWERBALL", "OZLOTTO"], (2026, 1), (2026, 2)) == [(2026, 1), (2026, 2)]
        assert validate_request(["POWERBALL"], (2026, 7), (2026, 7)) == [(2026, 7)]
        for frm, to in [((2026, 7), (2026, 8)), ((2026, 8), (2026, 8)), ((2026, 12), (2026, 12)),
                        ((2027, 1), (2027, 1)), ((2026, 1), (2026, 3)), ((2026, 2), (2026, 1)),
                        ((2026, 13), (2026, 13)), ((2026, 0), (2026, 1))]:
            assert refused(lambda: validate_request(["POWERBALL"], frm, to)), (frm, to)
        assert refused(lambda: validate_request(["KENO"], (2026, 1), (2026, 1)))
        assert refused(lambda: validate_request(["OZLOTTO"], (2022, 3), (2022, 4)))

    def t_classify():
        assert classify("POWERBALL", 1576, date(2026, 7, 30)) == "DEV"
        assert classify("POWERBALL", 1143, date(2018, 4, 12)) == "PRE_ERA"
        assert classify("OZLOTTO", 1693, date(2026, 7, 28)) == "DEV"
        assert classify("OZLOTTO", 1473, date(2022, 5, 10)) == "PRE_ERA"
        for g, n, d in [("POWERBALL", 1577, date(2026, 8, 6)), ("POWERBALL", 1600, date(2027, 1, 14)),
                        ("POWERBALL", 1500, date(2026, 8, 1)), ("OZLOTTO", 1694, date(2026, 8, 4)),
                        ("OZLOTTO", 1600, date(2026, 9, 1))]:
            assert refused(lambda: classify(g, n, d), QuarantineStop), (g, n, d)

    def t_expected():
        assert expected_draws("POWERBALL", 2026, 1) == [1546, 1547, 1548, 1549, 1550]
        assert expected_draws("POWERBALL", 2026, 2) == [1551, 1552, 1553, 1554]
        assert expected_draws("OZLOTTO", 2026, 1) == [1664, 1665, 1666, 1667]
        assert expected_draws("OZLOTTO", 2026, 2) == [1668, 1669, 1670, 1671]
        assert expected_draws("POWERBALL", 2026, 7)[-1] == 1576
        assert expected_draws("POWERBALL", 2026, 8) == []
        assert expected_draws("OZLOTTO", 2026, 8) == []
        assert expected_draws("POWERBALL", 2018, 4) == [1144, 1145]
        assert expected_draws("OZLOTTO", 2022, 5) == [1474, 1475, 1476]

    pb_ok = ("Powerball Results January 2026\n29 January 2026 8:30 pmDraw 1550\nMain numbers\n"
             "1 2 3 4 5 6 7\nPowerball\n9\nView dividends\n22 January 2026 8:30 pmDraw 1549\n"
             "Main numbers\n11 12 13 14 15 16 17\nPowerball\n20\n")
    oz_ok = ("OZ Lotto Results February 2026\nMar 2026\n24 February 2026 8:30 pm Draw 1671\nMain Numbers\n"
             "40 41 42 43 44 45 46\nSupplementary\n1 2 3\n")

    def t_lw_parser():
        recs, info = parse_lotterywest_text("POWERBALL", 2026, 1, pb_ok)
        assert [r.draw_number for r in recs] == [1550, 1549] and recs[0].main == (1, 2, 3, 4, 5, 6, 7)
        assert recs[0].secondary == (9,) and info["times_seen"] == ["8:30 pm"]
        recs, _ = parse_lotterywest_text("OZLOTTO", 2026, 2, oz_ok)
        assert recs[0].secondary == (1, 2, 3)
        split = pb_ok.replace("1 2 3 4 5 6 7", "1 2 3 4 5 6 1 8")
        assert refused(lambda: parse_lotterywest_text("POWERBALL", 2026, 1, split), ParseFailure)
        dup = pb_ok.replace("1 2 3 4 5 6 7", "1 2 3 4 5 6 6")
        assert refused(lambda: parse_lotterywest_text("POWERBALL", 2026, 1, dup), ParseFailure)
        rng = pb_ok.replace("Powerball\n9", "Powerball\n21")
        assert refused(lambda: parse_lotterywest_text("POWERBALL", 2026, 1, rng), ParseFailure)
        overlap = oz_ok.replace("Supplementary\n1 2 3", "Supplementary\n1 2 40")
        assert refused(lambda: parse_lotterywest_text("OZLOTTO", 2026, 2, overlap), ParseFailure)
        other = pb_ok + "5 February 2026 8:30 pmDraw 1551\nMain numbers\n1 2 3 4 5 6 7\nPowerball\n1\n"
        recs, info = parse_lotterywest_text("POWERBALL", 2026, 1, other)
        assert len(recs) == 2 and info["other_month_ignored"] == 1

    def t_lw_quarantine():
        q = pb_ok + "6 August 2026 8:30 pmDraw 1577\nMain numbers\n1 2 3 4 5 6 7\nPowerball\n1\n"
        assert refused(lambda: parse_lotterywest_text("POWERBALL", 2026, 1, q), QuarantineStop)
        q2 = oz_ok + "4 August 2026 8:30 pm Draw 1694\nMain Numbers\n1 2 3 4 5 6 7\nSupplementary\n8 9 10\n"
        assert refused(lambda: parse_lotterywest_text("OZLOTTO", 2026, 2, q2), QuarantineStop)
        q3 = "15 October 2026 8:30 pmDraw 1587\nMain numbers\nX\n" + pb_ok  # malformed AND quarantined
        assert refused(lambda: parse_lotterywest_text("POWERBALL", 2026, 1, q3), QuarantineStop)

    def t_lott_block():
        r = lott_block_record("POWERBALL", 2026, 1, "Draw 1550", "Thu, 29 Jan 2026",
                              list("1234567"), ["9"], "DRAWN_SELECTED")
        assert r.main == (1, 2, 3, 4, 5, 6, 7) and r.draw_date == "2026-01-29"
        assert refused(lambda: lott_block_record("POWERBALL", 2026, 8, "Draw 1577", "Thu, 6 Aug 2026",
                                                 list("1234567"), ["9"], "DRAWN_SELECTED"), QuarantineStop)
        assert refused(lambda: lott_block_record("POWERBALL", 2026, 1, "Draw 1550", "Thu, 29 Jan 2026",
                                                 list("123456"), ["9"], "DRAWN_SELECTED"), ParseFailure)
        assert refused(lambda: lott_block_record("POWERBALL", 2026, 2, "Draw 1550", "Thu, 29 Jan 2026",
                                                 list("1234567"), ["9"], "DRAWN_SELECTED"), ParseFailure)
        assert lott_block_record("POWERBALL", 2018, 4, "Draw 1143", "Thu, 12 Apr 2018",
                                 list("123456"), ["9"], "DRAWN_SELECTED") is None

    def t_reconcile():
        lw, _ = parse_lotterywest_text("POWERBALL", 2026, 1, pb_ok)
        lott = [Record(r.game, r.draw_number, r.draw_date, r.main, r.secondary, "THELOTT", "DRAWN_SELECTED") for r in lw]
        lines, c = reconcile("POWERBALL", [(2026, 1)], lott, lw)
        assert c["all_pass"] == 2 and c["fail"] == 3 and c["expected"] == 5  # 1546-1548 missing
        swapped = [Record(lott[0].game, lott[0].draw_number, lott[0].draw_date,
                          (2, 1, 3, 4, 5, 6, 7), lott[0].secondary, "THELOTT", "DRAWN_SELECTED")] + lott[1:]
        lines, c = reconcile("POWERBALL", [(2026, 1)], swapped, lw)
        assert any("1550" in l and "main_order FAIL" in l and "main_set PASS" in l for l in lines)
        assert not any(re.search(r"\b(1|2|3|4|5|6|7|9)\b(?!\d)", l.split(":", 1)[1]) for l in lines
                       if ":" in l and "MISSING" not in l), "report must not contain ball values"

    def t_output_create_only():
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "a.txt"
            write_new(p, b"x")
            assert refused(lambda: write_new(p, b"y"), FileExistsError)

    for name, fn in [("constants", t_constants), ("month limits", t_months), ("classify", t_classify),
                     ("expected draws", t_expected), ("Lotterywest parser", t_lw_parser),
                     ("Lotterywest quarantine stop", t_lw_quarantine), ("The Lott block", t_lott_block),
                     ("reconcile value-free", t_reconcile), ("create-only output", t_output_create_only)]:
        check(name, fn)
    passed = sum(ok for _, ok in results)
    print(f"[SELF-TEST] {passed}/{len(results)} PASS")
    return 0 if passed == len(results) else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Private two-site results check (The Lott vs Lotterywest), v0.1")
    p.add_argument("--self-test", action="store_true", help="test blockouts and parsers offline, then exit")
    p.add_argument("--browser", choices=("chrome", "firefox"), default="chrome")
    p.add_argument("--games", default="POWERBALL,OZLOTTO")
    p.add_argument("--from-month", default=f"{DEFAULT_FROM[0]}-{DEFAULT_FROM[1]:02d}")
    p.add_argument("--to-month", default=f"{DEFAULT_TO[0]}-{DEFAULT_TO[1]:02d}")
    p.add_argument("--pause", type=float, default=MIN_PAUSE_SECONDS, help=f"seconds between actions (>= {MIN_PAUSE_SECONDS})")
    args = p.parse_args(argv)
    if sys.version_info < (3, 10):
        print("[CHECK] ERROR: use the project's Python 3.14 venv", file=sys.stderr)
        return 3
    if args.self_test:
        return self_test()
    try:
        return run(args)
    except UsageRefused as exc:
        print(f"[CHECK] REFUSED: {exc}", file=sys.stderr)
        return 3
    except QuarantineStop as exc:
        print(f"[CHECK] STOP: a quarantined {exc} draw was encountered; nothing was saved and no values "
              "were read or shown.", file=sys.stderr)
        return 2
    except BlockedStop as exc:
        print(f"[CHECK] STOP: {exc}. The site may have blocked or changed the page; nothing was bypassed. "
              "Fall back to manual saves.", file=sys.stderr)
        return 2
    except ParseFailure as exc:
        print(f"[CHECK] STOP: strict parse failed - {exc}. Nothing was saved.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
