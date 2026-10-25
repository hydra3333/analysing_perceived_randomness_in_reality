"""Two-site lottery results check: The Lott versus Lotterywest. v0.5 TEST BUILD.

PRIVATE, OWNER-RUN, DEVELOPMENT DATA ONLY. Place this file in the project's src/
folder and run it with the project's .venv Python (3.14).

What it does
- Drives a real, unmodified browser (Chrome or Firefox) with Selenium, headless.
- For each requested month and game it:
    * opens The Lott results page, picks the month and year, clicks Find, makes
      sure the "Drawn" order is selected, and reads that month's draws;
    * opens Lotterywest's own results-search page (www.lotterywest.wa.gov.au)
      for that month and reads the same draws. (oz.lotterywest.com blocked
      automation with Cloudflare on 25 Oct 2026, so it is never contacted.)
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
    python src\\two_site_results_check_v0_5.py --self-test
    python src\\two_site_results_check_v0_5.py --offline-dir <folder of saved .mhtml pages>
    python src\\two_site_results_check_v0_5.py --diagnose-lotterywest --game POWERBALL --month 2026-01
    python src\\two_site_results_check_v0_5.py --browser chrome
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

TOOL_VERSION = "0.5"

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
    weekday: int  # Monday=0


ERAS = MappingProxyType({
    "POWERBALL": Era(1144, date(2018, 4, 19), (2018, 4), 35, 1, 20, "Powerball",
                     "powerball", "powerball", "Search Powerball Results", 3),
    "OZLOTTO": Era(1474, date(2022, 5, 17), (2022, 5), 47, 3, 47, "Supplementary",
                   "oz-lotto", "oz-lotto", "Search Oz Lotto Results", 1),
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
    """Return 'PRE_ERA' or 'DEV'. Raise QuarantineStop BEFORE numbers are read.

    A development draw on the wrong weekday means the page is for the other game
    (or is corrupt): ParseFailure, still before any numbers are read.
    """
    if draw_number >= FIRST_QUARANTINED_DRAW[game] or draw_date >= QUARANTINE_START_DATE:
        raise QuarantineStop(game)
    if draw_number < ERAS[game].first_draw:
        return "PRE_ERA"
    if draw_date.weekday() != ERAS[game].weekday:
        raise ParseFailure(f"{game} draw {draw_number}: wrong weekday for this game (wrong game page?)")
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


_MONTHS_RE = (r"Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|"
              r"Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?")


def month_number(token: str) -> int:
    return [m[:3].lower() for m in MONTH_NAMES].index(token[:3].lower()) + 1
_LW_HEADER = re.compile(
    rf"(?P<day>\d{{1,2}})(?:st|nd|rd|th)?\s+(?P<mon>{_MONTHS_RE})\.?,?\s+(?P<year>\d{{4}}),?\s*"
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
        mon = month_number(h.group("mon"))
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


_WEEKDAYS = "Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday"
_GOV_HEADER = re.compile(
    rf"Draw\s+(?P<draw>\d{{3,5}})\s+(?:{_WEEKDAYS})\s+(?P<day>\d{{1,2}})\s+(?P<mon>{_MONTHS_RE})\s+(?P<year>\d{{4}})")


def parse_gov_text(game: str, year: int, month: int, text: str) -> tuple[list[Record], dict]:
    """Strict parser for Lotterywest's www.lotterywest.wa.gov.au results-search text.

    Layout: 'Draw N' / 'Weekday D Month YYYY' / 'Winning numbers:' 7 numbers /
    'Powerball:' 1 number or 'Supplementary [numbers]:' 3 numbers / 'View prizes'.
    Each block is classified on draw number and date BEFORE its numbers are read.
    """
    headers = list(_GOV_HEADER.finditer(text))
    records, info = [], {"headers": len(headers), "other_month_ignored": 0, "pre_era_ignored": 0}
    for idx, h in enumerate(headers):
        n = int(h.group("draw"))
        d = date(int(h.group("year")), month_number(h.group("mon")), int(h.group("day")))
        if classify(game, n, d) == "PRE_ERA":
            info["pre_era_ignored"] += 1
            continue
        if (d.year, d.month) != (year, month):
            info["other_month_ignored"] += 1
            continue
        body = text[h.end(): headers[idx + 1].start() if idx + 1 < len(headers) else len(text)]
        tokens = body.split()
        try:
            i = next(k for k in range(len(tokens) - 1)
                     if tokens[k].lower() == "winning" and tokens[k + 1].lower() == "numbers:")
        except StopIteration:
            raise ParseFailure(f"{game} draw {n}: 'Winning numbers:' label not found") from None
        main, i = _take_numbers(tokens, i + 2)
        if game == "POWERBALL":
            if i >= len(tokens) or tokens[i].lower() != "powerball:":
                raise ParseFailure(f"{game} draw {n}: 'Powerball:' label not where expected")
            i += 1
        else:
            if i < len(tokens) and tokens[i].lower() == "supplementary:":
                i += 1
            elif i + 1 < len(tokens) and tokens[i].lower() == "supplementary" and tokens[i + 1].lower() == "numbers:":
                i += 2
            else:
                raise ParseFailure(f"{game} draw {n}: 'Supplementary' label not where expected")
        secondary, _ = _take_numbers(tokens, i)
        validate_numbers(game, n, main, secondary)
        records.append(Record(game, n, d.isoformat(), tuple(main), tuple(secondary),
                              "LOTTERYWEST_GOV_RESULTS_SEARCH", "SOURCE_SEQUENCE"))
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
    _check_not_blocked(driver, "www.thelott.com")
    # Only the search controls are touched; the page's default result block is never read.
    _wait(driver, lambda d: d.find_elements(By.CSS_SELECTOR, "section.results-search select.select-month"),
          "The Lott month selector")
    month_el = driver.find_element(By.CSS_SELECTOR, "section.results-search select.select-month")
    year_el = driver.find_element(By.CSS_SELECTOR, "section.results-search select.select-year")
    Select(year_el).select_by_visible_text(str(year))      # year first: it may reset the month list
    Select(month_el).select_by_visible_text(MONTH_NAMES[month - 1])
    month_el = driver.find_element(By.CSS_SELECTOR, "section.results-search select.select-month")
    year_el = driver.find_element(By.CSS_SELECTOR, "section.results-search select.select-year")
    if (Select(month_el).first_selected_option.text.strip() != MONTH_NAMES[month - 1] or
            Select(year_el).first_selected_option.text.strip() != str(year)):
        raise BlockedStop("The Lott month/year selection did not take")
    want = len(expected_draws(game, year, month))
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
        if not m or int(m.group(1)) != want:   # never accept '0 draws found' or a partial list
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


def _check_not_blocked(driver, site: str) -> None:
    title = (driver.title or "").lower()
    if any(k in title for k in ("attention required", "cloudflare", "access denied", "just a moment", "blocked")):
        raise BlockedStop(f"{site} served a block/challenge page")


def fetch_lotterywest_month(driver, pacer: Pacer, game: str, year: int, month: int) -> tuple[list[Record], dict]:
    from selenium.webdriver.common.by import By
    url = gov_search_url(game, year, month)
    pacer.wait("load", url)
    driver.get(url)
    _wait(driver, lambda d: d.execute_script("return document.readyState") == "complete", "Lotterywest page load")
    _check_not_blocked(driver, "www.lotterywest.wa.gov.au")

    def month_blocks_present(d):
        text = d.find_element(By.TAG_NAME, "body").text
        hits = [h for h in _GOV_HEADER.finditer(text)
                if month_number(h.group("mon")) == month and int(h.group("year")) == year]
        return text if hits else False

    text = _wait(driver, month_blocks_present, f"Lotterywest results for {MONTH_NAMES[month-1]} {year}")
    _check_not_blocked(driver, "www.lotterywest.wa.gov.au")
    records, info = parse_gov_text(game, year, month, text)
    info["url"] = url
    return records, info


LOTTERYWEST_GAME_CODE = MappingProxyType({"POWERBALL": 5132, "OZLOTTO": 5130})


def gov_search_url(game: str, year: int, month: int) -> str:
    """www.lotterywest.wa.gov.au results-search page for ONE allowed month.

    From = last day of the previous month, To = last day of the month itself,
    so the range can never reach the quarantine start date.
    """
    if (year, month) > LAST_ALLOWED_MONTH:
        raise UsageRefused("month is in or after the quarantine boundary month")
    first = date(year, month, 1)
    frm = first - timedelta(days=1)
    to = date(year, month, calendar.monthrange(year, month)[1])
    if to >= QUARANTINE_START_DATE:
        raise UsageRefused("search range would reach the quarantine start date")
    fmt = lambda d: d.strftime("%a+%b+%d+%Y")
    # The PATH selects the game on a direct load (filterByGame alone is ignored).
    return (f"https://www.lotterywest.wa.gov.au/results/{ERAS[game].lotterywest_slug}"
            f"?fromDate={fmt(frm)}&toDate={fmt(to)}&filterByGame={LOTTERYWEST_GAME_CODE[game]}")


def diagnose_lotterywest(args) -> int:
    """Load ONE allowed Lotterywest month page; print structure with every digit masked."""
    game = args.game.strip().upper()
    y, m = (int(x) for x in args.month.split("-"))
    validate_request([game], (y, m), (y, m))
    pacer = Pacer(MIN_PAUSE_SECONDS)
    driver = make_driver(args.browser)
    try:
        url = gov_search_url(game, y, m)
        pacer.wait("load", url)
        driver.get(url)
        time.sleep(8)  # let client-side rendering finish
        from selenium.webdriver.common.by import By
        text = driver.find_element(By.TAG_NAME, "body").text
        mask = lambda s: re.sub(r"\d", "#", s)
        print(f"[DIAG] requested: {url}")
        print(f"[DIAG] final URL: {mask(driver.current_url)}")
        print(f"[DIAG] title: {mask(driver.title)}")
        print(f"[DIAG] body characters: {len(text)}; draw headings recognised: {len(list(_GOV_HEADER.finditer(text)))}")
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        print(f"[DIAG] first {min(len(lines), 120)} of {len(lines)} non-empty lines (ALL DIGITS MASKED):")
        for ln in lines[:120]:
            print("   | " + mask(ln)[:160])
    finally:
        driver.quit()
    return 0


# ---------------------------------------------------------------------------
# Offline mode: owner-saved .mhtml pages (no network, no browser)
# ---------------------------------------------------------------------------
def _mhtml(path: Path) -> tuple[str, str]:
    import email
    from email import policy
    msg = email.message_from_bytes(path.read_bytes(), policy=policy.default)
    parts = [x for x in msg.walk() if not x.is_multipart() and x.get_content_type() == "text/html"]
    if not parts:
        raise ParseFailure(f"{path.name}: no HTML part")
    html = max((x.get_content() for x in parts), key=len)
    return (msg.get("Snapshot-Content-Location") or ""), html


def _soup(html: str):
    from bs4 import BeautifulSoup
    s = BeautifulSoup(html, "html.parser")
    for x in s(["script", "style", "noscript"]):
        x.decompose()
    return s


def offline_file_records(path: Path) -> tuple[str, str, list[Record], dict]:
    """Return (game, source, records, info) for one saved page.

    The Lott: ONLY the search-results block is read (the page's latest-draw
    panel, which shows quarantined draws, is never touched). Every block is
    classified on draw number and date before any ball text is read.
    """
    from urllib.parse import urlsplit, parse_qs
    loc, html = _mhtml(path)
    u = urlsplit(loc)
    if u.hostname == "www.thelott.com":
        game = {"/powerball/results": "POWERBALL", "/oz-lotto/results": "OZLOTTO"}.get(u.path.rstrip("/"))
        if game is None:
            raise ParseFailure(f"{path.name}: unrecognised The Lott page")
        sec = _soup(html).select_one("section.results-search default-results")
        if sec is None:
            raise ParseFailure(f"{path.name}: The Lott search-results block not found")
        m = re.search(r"(\d+)\s+draws?\s+found", (sec.select_one(".draws-found") or sec).get_text(" ", strip=True))
        drawn = [b for b in sec.select(".ball-order button") if b.get_text(strip=True).lower() == "drawn"]
        order_label = "DRAWN_SELECTED" if drawn and drawn[0].has_attr("disabled") else "ORDER_UNCONFIRMED"
        rows = []
        for ln in sec.select("lotto-numbers"):
            row = ln.parent
            while row is not None and not row.select("[class*='draw-num']"):
                row = row.parent
            if row is None:
                raise ParseFailure(f"{path.name}: draw row structure not recognised")
            draw_text = row.select_one("[class*='draw-num']").get_text(" ", strip=True)
            spans = row.select("[class*='text-right'] span")
            date_text = spans[0].get_text(" ", strip=True) if spans else ""
            dm = _LOTT_DRAW.search(draw_text)
            if not dm:
                raise ParseFailure(f"{path.name}: draw label not recognised")
            rows.append((int(dm.group(1)), parse_lott_date(date_text), draw_text, date_text, ln))
        for n, d, *_ in rows:                       # classify ALL blocks before reading any balls
            classify(game, n, d)
        months = {(d.year, d.month) for n, d, *_ in rows if n >= ERAS[game].first_draw}
        if len(months) > 1:
            raise ParseFailure(f"{path.name}: The Lott search block spans more than one month")
        if not m or int(m.group(1)) != len(rows):
            raise ParseFailure(f"{path.name}: 'draws found' count does not match the blocks")
        records = []
        for n, d, draw_text, date_text, ln in rows:
            pr = [e.get_text(strip=True) for e in ln.select(".primary-numbers .number")]
            se = [e.get_text(strip=True) for e in ln.select(".secondary-numbers > div")]
            rec = lott_block_record(game, d.year, d.month, draw_text, date_text, pr, se, order_label)
            if rec is not None:
                records.append(rec)
        return game, "thelott", records, {"file": path.name, "url": loc, "order_label": order_label,
                                          "months": sorted(f"{y}-{mm:02d}" for y, mm in months)}
    if u.hostname == "www.lotterywest.wa.gov.au" and u.path.startswith("/results/"):
        q = parse_qs(u.query)
        code = (q.get("filterByGame") or [""])[0]
        by_code = {str(v): k for k, v in LOTTERYWEST_GAME_CODE.items()}
        by_path = {"/results/powerball": "POWERBALL", "/results/oz-lotto": "OZLOTTO"}
        # A saved page keeps the game picked on screen in filterByGame; the path can be stale.
        game = by_code.get(code) or by_path.get(u.path.rstrip("/"))
        if game is None:
            raise ParseFailure(f"{path.name}: game not identifiable")
        for key in ("fromDate", "toDate"):
            if key in q:
                try:
                    dd = datetime.strptime(q[key][0], "%a %b %d %Y").date()
                except ValueError:
                    raise ParseFailure(f"{path.name}: {key} not recognised") from None
                if dd >= QUARANTINE_START_DATE:
                    raise QuarantineStop(game)   # file's search range reaches the boundary: not read
        text = _soup(html).get_text("\n", strip=True)
        heads = list(_GOV_HEADER.finditer(text))
        found = []
        for h in heads:                               # classify ALL headers before reading any numbers
            n = int(h.group("draw"))
            d = date(int(h.group("year")), month_number(h.group("mon")), int(h.group("day")))
            if classify(game, n, d) == "DEV":
                found.append((d.year, d.month))
        records = []
        for (y, mm) in sorted(set(found)):
            records += parse_gov_text(game, y, mm, text)[0]
        return game, "lotterywest", records, {"file": path.name, "url": loc,
                                              "months": sorted(f"{y}-{mm:02d}" for y, mm in set(found))}
    raise ParseFailure(f"{path.name}: not a recognised The Lott or Lotterywest results page")


def run_offline(args) -> int:
    check_boundary_constants()
    folder = Path(args.offline_dir)
    files = sorted(folder.glob("*.mhtml"))
    if not files:
        raise UsageRefused("no .mhtml files in the offline folder")
    root = Path(__file__).resolve().parents[1]
    base = root / OUTPUT_FOLDER_NAME
    ignored = git_ignored(root, base / "probe.csv")
    if ignored is False:
        raise UsageRefused(f"{OUTPUT_FOLDER_NAME}/ is not git-ignored; add it to .gitignore first")
    data: dict = {}
    inputs = []
    for f in files:
        game, src, recs, info = offline_file_records(f)
        bucket = data.setdefault(game, {"thelott": {}, "lotterywest": {}, "months": set()})
        for r in recs:
            old = bucket[src].get(r.draw_number)
            if old is not None and old != r:
                raise ParseFailure(f"{game} draw {r.draw_number}: two saved {src} pages disagree")
            bucket[src][r.draw_number] = r
            bucket["months"].add(tuple(int(x) for x in r.draw_date[:7].split("-")))
        inputs.append({**info, "game": game, "source": src, "draws": len(recs),
                       "sha256": hashlib.sha256(f.read_bytes()).hexdigest()})
        print(f"[OFFLINE] {f.name}: {game} {src} {len(recs)} draws, months {info['months']}", flush=True)
    run_dir = make_run_dir(base)
    hashes, report, summary = {}, [], {}
    for game, b in sorted(data.items()):
        months = sorted(b["months"])
        lott, lw = list(b["thelott"].values()), list(b["lotterywest"].values())
        hashes[f"thelott_{game}.csv"] = write_new(run_dir / f"thelott_{game}.csv", csv_bytes(csv_rows(game, lott)))
        hashes[f"lotterywest_{game}.csv"] = write_new(run_dir / f"lotterywest_{game}.csv", csv_bytes(csv_rows(game, lw)))
        lines, counts = reconcile(game, months, lott, lw)
        report += lines
        summary[game] = counts
    report_text = "\r\n".join(["TWO-SITE RESULTS CHECK, OFFLINE (value-free)", *report, "",
                               json.dumps(summary, sort_keys=True)]) + "\r\n"
    hashes["reconciliation.txt"] = write_new(run_dir / "reconciliation.txt", report_text.encode("ascii"))
    prov = {"tool_version": TOOL_VERSION, "mode": "OFFLINE_SAVED_PAGES",
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "python": sys.version,
            "quarantine": {"start_date": QUARANTINE_START_DATE.isoformat(),
                           "first_quarantined_draw": dict(FIRST_QUARANTINED_DRAW)},
            "inputs": inputs, "summary": summary, "output_sha256": hashes, "git_ignored_output": ignored,
            "finished_utc": datetime.now(timezone.utc).isoformat()}
    write_new(run_dir / "provenance.json", json.dumps(prov, indent=1, sort_keys=True).encode("utf-8"))
    for line in report:
        print("[OFFLINE] " + line)
    print(f"[OFFLINE] summary {json.dumps(summary, sort_keys=True)}")
    print(f"[OFFLINE] files in {run_dir}")
    return 0 if all(c["fail"] == 0 and c["all_pass"] == c["expected"] for c in summary.values()) else 1


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
        abbr = pb_ok.replace("29 January 2026", "Thu 29 Jan 2026").replace("22 January 2026", "22nd Jan, 2026")
        recs, _ = parse_lotterywest_text("POWERBALL", 2026, 1, abbr)
        assert [r.draw_number for r in recs] == [1550, 1549]
        assert month_number("Sept") == 9 and month_number("jun") == 6
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

    gov_pb = ("Search by game, draw number, and date:\nPowerball\nDec 31, 2025\nJan 31, 2026\n"
              "Draw 1550\nThursday 29 January 2026\nWinning numbers:\n1\n2\n3\n4\n5\n6\n7\nPowerball:\n9\nView prizes\n"
              "Draw 1549\nThursday 22 January 2026\nWinning numbers:\n11\n12\n13\n14\n15\n16\n17\nPowerball:\n20\nView prizes\n"
              "What does my money support in WA?\nIn 2024-25, we gave back over $1.5 billion\n")
    gov_oz = ("Draw 1671\nTuesday 24 February 2026\nWinning numbers:\n40\n41\n42\n43\n44\n45\n46\n"
              "Supplementary numbers:\n1\n2\n3\nView prizes\n")

    def t_gov_parser():
        recs, info = parse_gov_text("POWERBALL", 2026, 1, gov_pb)
        assert [r.draw_number for r in recs] == [1550, 1549] and recs[0].main == (1, 2, 3, 4, 5, 6, 7)
        assert recs[1].secondary == (20,) and recs[0].source == "LOTTERYWEST_GOV_RESULTS_SEARCH"
        recs, _ = parse_gov_text("OZLOTTO", 2026, 2, gov_oz)
        assert recs[0].secondary == (1, 2, 3)
        recs, _ = parse_gov_text("OZLOTTO", 2026, 2, gov_oz.replace("Supplementary numbers:", "Supplementary:"))
        assert recs[0].secondary == (1, 2, 3)
        for bad in (gov_pb.replace("1\n2\n3\n4\n5\n6\n7", "1\n2\n3\n4\n5\n6\n1\n8"),
                    gov_pb.replace("Powerball:\n9", "Powerball:\n21"),
                    gov_pb.replace("1\n2\n3\n4\n5\n6\n7", "1\n2\n3\n4\n5\n6\n6")):
            assert refused(lambda: parse_gov_text("POWERBALL", 2026, 1, bad), ParseFailure)
        q = gov_pb + "Draw 1577\nThursday 6 August 2026\nWinning numbers:\nX\n"
        assert refused(lambda: parse_gov_text("POWERBALL", 2026, 1, q), QuarantineStop)
        q2 = gov_oz + "Draw 1694\nTuesday 4 August 2026\nWinning numbers:\n1\n"
        assert refused(lambda: parse_gov_text("OZLOTTO", 2026, 2, q2), QuarantineStop)
        other = gov_pb + "Draw 1551\nThursday 5 February 2026\nWinning numbers:\n1\n2\n3\n4\n5\n6\n7\nPowerball:\n1\n"
        recs, info = parse_gov_text("POWERBALL", 2026, 1, other)
        assert len(recs) == 2 and info["other_month_ignored"] == 1

    def t_offline():
        import tempfile
        from email.message import EmailMessage

        def mht(folder, name, loc, html):
            m = EmailMessage()
            m["Snapshot-Content-Location"] = loc
            m.set_content(html, subtype="html")
            pth = Path(folder) / name
            pth.write_bytes(m.as_bytes())
            return pth
        gov = ("https://www.lotterywest.wa.gov.au/results/powerball?fromDate=Wed+Dec+31+2025"
               "&toDate=Sat+Jan+31+2026&filterByGame=5132")
        body = "<html><body>" + "".join(f"<div>{x}</div>" for x in gov_pb.split("\n")) + "</body></html>"
        with tempfile.TemporaryDirectory() as td:
            g, s, recs, _ = offline_file_records(mht(td, "a.mhtml", gov, body))
            assert (g, s, [r.draw_number for r in recs]) == ("POWERBALL", "lotterywest", [1550, 1549])
            late = gov.replace("toDate=Sat+Jan+31+2026", "toDate=Sat+Aug+01+2026")
            assert refused(lambda: offline_file_records(mht(td, "b.mhtml", late, body)), QuarantineStop)
            wrong = gov.replace("filterByGame=5132", "filterByGame=5130")   # Oz page showing Thursday draws
            assert refused(lambda: offline_file_records(mht(td, "c.mhtml", wrong, body)), ParseFailure)
            row = ('<div class="row"><div class="columns draw-num"><span>Draw {n}</span></div>'
                   '<div class="columns text-right"><span>{d}</span></div><lotto-numbers><div class="primary-numbers">'
                   + "".join(f'<div class="number"><span>{x}</span></div>' for x in range(1, 8)) +
                   '</div><div class="secondary-numbers"><div class="suppsnumber"><span>9</span></div></div></lotto-numbers></div>')
            lott = ('<html><body><div class="latest">Draw No. 1588 Thu, 22 Oct 2026 '
                    '<span class="number">99</span></div><section class="results-search"><default-results>'
                    '<div class="draws-found">1 draws found <div class="ball-order"><button disabled="">Drawn</button>'
                    '<button>Numerical</button></div></div>' + row.format(n=1550, d="Thu, 29 Jan 2026") +
                    '</default-results></section></body></html>')
            g, s, recs, info = offline_file_records(mht(td, "d.mhtml", "https://www.thelott.com/powerball/results", lott))
            assert (g, s, len(recs), info["order_label"]) == ("POWERBALL", "thelott", 1, "DRAWN_SELECTED")
            bad = lott.replace(row.format(n=1550, d="Thu, 29 Jan 2026"), row.format(n=1577, d="Thu, 6 Aug 2026"))
            assert refused(lambda: offline_file_records(mht(td, "e.mhtml", "https://www.thelott.com/powerball/results", bad)),
                           QuarantineStop)

    def t_gov_url():
        u = gov_search_url("POWERBALL", 2026, 1)
        assert u == ("https://www.lotterywest.wa.gov.au/results/powerball?fromDate=Wed+Dec+31+2025"
                     "&toDate=Sat+Jan+31+2026&filterByGame=5132"), u
        u = gov_search_url("OZLOTTO", 2026, 7)
        assert "/results/oz-lotto?" in u and "filterByGame=5130" in u and "toDate=Fri+Jul+31+2026" in u, u
        assert refused(lambda: gov_search_url("POWERBALL", 2026, 8))
        assert refused(lambda: gov_search_url("OZLOTTO", 2027, 1))

    def t_output_create_only():
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "a.txt"
            write_new(p, b"x")
            assert refused(lambda: write_new(p, b"y"), FileExistsError)

    for name, fn in [("constants", t_constants), ("month limits", t_months), ("classify", t_classify),
                     ("expected draws", t_expected), ("Lotterywest parser", t_lw_parser),
                     ("Lotterywest quarantine stop", t_lw_quarantine), ("The Lott block", t_lott_block),
                     ("reconcile value-free", t_reconcile), ("create-only output", t_output_create_only),
                     ("gov search URL limits", t_gov_url), ("gov results parser", t_gov_parser),
                     ("offline saved pages", t_offline)]:
        check(name, fn)
    passed = sum(ok for _, ok in results)
    print(f"[SELF-TEST] {passed}/{len(results)} PASS")
    return 0 if passed == len(results) else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Private two-site results check (The Lott vs Lotterywest), v0.5")
    p.add_argument("--self-test", action="store_true", help="test blockouts and parsers offline, then exit")
    p.add_argument("--offline-dir", default=None,
                   help="process a folder of owner-saved .mhtml pages instead of using a browser")
    p.add_argument("--diagnose-lotterywest", action="store_true",
                   help="load one allowed Lotterywest month page and print its structure with all digits masked")
    p.add_argument("--game", default="POWERBALL", help="for --diagnose-lotterywest")
    p.add_argument("--month", default="2026-01", help="for --diagnose-lotterywest (YYYY-MM, July 2026 or earlier)")
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
        if args.offline_dir:
            return run_offline(args)
        if args.diagnose_lotterywest:
            return diagnose_lotterywest(args)
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
