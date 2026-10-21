"""Australian Powerball current-format historical results downloader, v0.3.

Only draws with rules 7 distinct main balls from 1..35 and 1 Powerball
from 1..20, starting with draw 1144 on 2018-04-19.  Never merge earlier eras.

Primary input: https://www.powerball.net/australia/archive/YYYY
Optional independent official verification and reported draw-order output:
    https://www.oz.lotterywest.com/powerball/results/draw/NNNN

Install in your chosen Python environment:
    python -m pip install requests beautifulsoup4

Commands:
    python scrape_australian_powerball_history_from_2018_04_19_v0_3.py
    python scrape_australian_powerball_history_from_2018_04_19_v0_3.py --official-order

The ten-column normal CSV remains compatible with the previous scraper.
The optional separate draw-order CSV is written ONLY when every draw has been
cross-checked against Lotterywest. No prediction or simulation is performed.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import tempfile
import time
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.powerball.net/australia/archive/"
OFFICIAL_URL = "https://www.oz.lotterywest.com/powerball/results/draw/"
START_DATE = date(2018, 4, 19)
START_DRAW = 1144
MAIN_COUNT = 7
MAIN_MAX = 35
POWERBALL_MAX = 20
PUBLICATION_GRACE_DAYS = 2
RESULT_PATH = re.compile(r"/australia/results/(\d{4}-\d{2}-\d{2})/?")
DRAW_NUMBER = re.compile(r"\bDraw\s+(\d+)\b", re.IGNORECASE)
NUMBER = re.compile(r"(?<!\w)\d{1,2}(?!\w)")
FIELDS = ["Draw_Number", "Date"] + [f"Ball_{n}" for n in range(1, 8)] + ["Powerball"]
ORDER_FIELDS = ["Draw_Number", "Date"] + [f"Drawn_{n}" for n in range(1, 8)] + ["Powerball", "Official_Source_URL"]


class ScrapeError(Exception):
    """Data quality, format or archive-coverage failure."""


def check_balls(balls: tuple[int, ...] | list[int], context: str) -> None:
    if (len(balls) != 8 or len(set(balls[:7])) != 7
            or not all(1 <= n <= MAIN_MAX for n in balls[:7])
            or not 1 <= balls[7] <= POWERBALL_MAX):
        raise ScrapeError(f"Invalid 7/35 + 1/20 result for {context}: {balls!r}")


def extract_draw(anchor, day: date) -> tuple:
    """Extract a dated archive entry, inspecting only its immediate containers."""
    candidates = [anchor]
    if anchor.parent is not None:
        candidates.append(anchor.parent)
        if anchor.parent.parent is not None:
            candidates.append(anchor.parent.parent)
    for element in candidates:
        text = element.get_text(" ", strip=True)
        markers = list(DRAW_NUMBER.finditer(text))
        if len(markers) != 1:
            continue
        draw_num = int(markers[0].group(1))
        balls = tuple(int(x) for x in NUMBER.findall(text[markers[0].end():]))
        if len(balls) != 8:
            continue
        check_balls(balls, f"draw {draw_num}")
        return (draw_num, day, *sorted(balls[:7]), balls[7])
    raise ScrapeError(f"Cannot identify exactly eight balls for {day}: "
                      f"{anchor.get_text(' ', strip=True)!r}")


def parse_archive(html: str, year: int) -> list[tuple]:
    soup = BeautifulSoup(html, "html.parser")
    results: dict[date, tuple] = {}
    for anchor in soup.find_all("a", href=True):
        url = urljoin(BASE_URL, anchor["href"])
        parsed = urlparse(url)
        match = RESULT_PATH.fullmatch(parsed.path)
        if not match or parsed.hostname != "www.powerball.net":
            continue
        day = date.fromisoformat(match.group(1))
        # Explicitly avoid the old six-from-40 draws in January-April 2018.
        if day.year != year or day < START_DATE:
            continue
        row = extract_draw(anchor, day)
        if day in results and results[day] != row:
            raise ScrapeError(f"Contradictory results for {day} on archive {year}")
        results[day] = row
    if not results:
        title = soup.title.get_text(" ", strip=True) if soup.title else "(untitled)"
        raise ScrapeError(f"No current-format draw entries found for {year}; page: {title!r}")
    return list(results.values())


def expected_thursdays(year: int, cutoff: date) -> set[date]:
    beginning = max(date(year, 1, 1), START_DATE)
    ending = min(date(year, 12, 31), cutoff)
    if beginning > ending:
        return set()
    current = beginning + timedelta(days=(3 - beginning.weekday()) % 7)
    found = set()
    while current <= ending:
        found.add(current)
        current += timedelta(days=7)
    return found


def check_completeness(draws: list[tuple], today: date) -> list[tuple]:
    if not draws:
        raise ScrapeError("No draws extracted")
    seen_dates, seen_numbers = set(), set()
    for draw_num, day, *balls in draws:
        if day < START_DATE or day > today:
            raise ScrapeError(f"Draw outside supported date interval: {draw_num}, {day}")
        if day.weekday() != 3:
            raise ScrapeError(f"Unexpected non-Thursday draw: {draw_num}, {day}")
        if day in seen_dates or draw_num in seen_numbers:
            raise ScrapeError(f"Duplicate date/number: {draw_num}, {day}")
        if tuple(balls[:7]) != tuple(sorted(balls[:7])):
            raise ScrapeError(f"Main numbers not in ascending CSV order for {draw_num}")
        check_balls(balls, f"draw {draw_num}")
        seen_dates.add(day)
        seen_numbers.add(draw_num)

    chronological = sorted(draws, key=lambda r: r[1])
    if chronological[0][:2] != (START_DRAW, START_DATE):
        raise ScrapeError(f"First draw must be {START_DRAW} on {START_DATE}, "
                          f"found {chronological[0][:2]!r}")
    for previous, current in zip(chronological, chronological[1:]):
        if current[0] != previous[0] + 1 or (current[1] - previous[1]).days != 7:
            raise ScrapeError(f"Gap/mismatch between {previous[:2]!r} and {current[:2]!r}")

    # A recently completed draw may require up to two days to be published.
    publication_cutoff = today - timedelta(days=PUBLICATION_GRACE_DAYS)
    for year in range(START_DATE.year, today.year + 1):
        expected = expected_thursdays(year, publication_cutoff)
        actual = {row[1] for row in chronological if row[1].year == year}
        missing = sorted(expected - actual)
        if missing:
            raise ScrapeError(f"Missing {len(missing)} expected draw(s) in {year}: {missing[:8]}")
    return chronological


def parse_lotterywest_order(html: str, draw_number: int, day: date) -> tuple[int, ...]:
    """Extract independently published main-ball ORDER from an official page.

    The official result page presents a 'Main numbers' label followed by seven
    displayed integers, and a 'Powerball' label followed by one integer.
    Never silently interpret ascending archive order as physical draw order.
    A future page-template change must trigger failure rather than fabrication.
    """
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    tokens = list(soup.stripped_strings)
    head = " ".join(tokens[:60])
    if not re.search(rf"\bDraw\s+{draw_number}\b", head, re.I):
        raise ScrapeError(f"Lotterywest page does not identify Draw {draw_number} ({day})")

    matches = [i for i, s in enumerate(tokens) if s.strip().casefold() == "main numbers"]
    if len(matches) != 1:
        raise ScrapeError(f"Cannot uniquely locate Lotterywest main-number section: Draw {draw_number}")
    start = matches[0] + 1
    power_labels = [i for i in range(start, min(start + 30, len(tokens)))
                    if tokens[i].strip().casefold() == "powerball"]
    if len(power_labels) != 1:
        raise ScrapeError(f"Cannot locate Lotterywest Powerball section: Draw {draw_number}")
    pb_index = power_labels[0]

    def numeric_tokens(values: list[str]) -> list[int]:
        nums = []
        for token in values:
            normalized = " ".join(token.split())
            if re.fullmatch(r"\d{1,2}(?: \d{1,2})*", normalized):
                nums.extend(int(x) for x in normalized.split())
            elif normalized:
                # The main-number area should contain nothing but numbers.
                raise ScrapeError(f"Unexpected Lotterywest token in Draw {draw_number}: {normalized!r}")
        return nums

    mains = numeric_tokens(tokens[start:pb_index])
    if len(mains) != 7:
        raise ScrapeError(f"Lotterywest displays {len(mains)} rather than seven main balls in Draw {draw_number}")
    following = [x.strip() for x in tokens[pb_index + 1:pb_index + 8]]
    if not following or not re.fullmatch(r"\d{1,2}", following[0]):
        raise ScrapeError(f"Cannot extract official Powerball for Draw {draw_number}")
    result = tuple(mains + [int(following[0])])
    check_balls(result, f"Lotterywest Draw {draw_number}")
    # Date belongs to the expected record; the page's draw-number identity is
    # checked above. Additional mismatch is caught by main/PB comparison.
    return result


def fetch_archive(session: requests.Session, today: date) -> list[tuple]:
    all_draws = []
    for year in range(START_DATE.year, today.year + 1):
        url = f"{BASE_URL}{year}"
        print(f"Fetching {year}: {url}", flush=True)
        response = session.get(url, timeout=25)
        response.raise_for_status()
        year_draws = parse_archive(response.text, year)
        print(f"  Found {len(year_draws)} current-format draw(s)", flush=True)
        all_draws.extend(year_draws)
    return check_completeness(all_draws, today)


def fetch_official_order(session: requests.Session, draws: list[tuple], delay: float) -> list[tuple]:
    """Optional, complete official check; rejects inconsistent or missing pages."""
    ordered = []
    total = len(draws)
    print(f"Independently checking {total} Lotterywest result pages (optional mode).", flush=True)
    for index, row in enumerate(draws, 1):
        draw_number, day, *nums = row
        url = f"{OFFICIAL_URL}{draw_number}"
        response = session.get(url, timeout=25)
        response.raise_for_status()
        actual = parse_lotterywest_order(response.text, draw_number, day)
        if tuple(sorted(actual[:7])) != tuple(nums[:7]) or actual[7] != nums[7]:
            raise ScrapeError(
                f"OFFICIAL CROSS-CHECK FAILED: Draw {draw_number} on {day}: "
                f"archive {nums!r}, Lotterywest {actual!r}. No CSV has been modified."
            )
        ordered.append((draw_number, day, *actual, url))
        if index % 25 == 0 or index == total:
            print(f"  Lotterywest verified {index}/{total}", flush=True)
        if index < total and delay:
            time.sleep(delay)
    return ordered


def atomic_csv(rows: list[tuple], filename: Path, columns: list[str]) -> None:
    """Replace one file only after all parsing and validation succeeded."""
    pending = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", newline="", encoding="utf-8", suffix=".tmp",
            dir=filename.parent, delete=False
        ) as stream:
            pending = Path(stream.name)
            writer = csv.writer(stream)
            writer.writerow(columns)
            for row in rows:
                writer.writerow([cell.isoformat() if isinstance(cell, date) else cell for cell in row])
        os.replace(pending, filename)
    finally:
        if pending is not None:
            pending.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--official-order", action="store_true",
                        help="Also fetch EVERY matching Lotterywest result, verify winning balls, "
                             "and write a separate reported draw-order CSV. This makes hundreds of "
                             "extra requests; optional because websites can change.")
    parser.add_argument("--official-delay", type=float, default=0.4,
                        help="Pause seconds between Lotterywest page requests (default 0.4).")
    args = parser.parse_args()
    if args.official_delay < 0.2:
        parser.error("--official-delay must be at least 0.2 seconds")

    today = date.today()
    if today < START_DATE:
        raise ScrapeError(f"Local system date precedes supported start {START_DATE}")
    suffix = today.strftime("%Y%m%d")
    destination = Path(__file__).with_name(f"australian_powerball_history_{suffix}.csv")
    order_destination = Path(__file__).with_name(f"australian_powerball_draw_order_{suffix}.csv")

    with requests.Session() as session:
        session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; PowerballHistoricalDataResearch/0.3)"})
        draws = fetch_archive(session, today)
        ordered = (fetch_official_order(session, draws, args.official_delay)
                   if args.official_order else None)

    # IMPORTANT: no output is replaced until ALL requested sources pass checks.
    atomic_csv(draws, destination, FIELDS)
    if ordered is not None:
        atomic_csv(ordered, order_destination, ORDER_FIELDS)
        print(f"OFFICIAL ORDER SUCCESS: {len(ordered)} independently checked draws in {order_destination}")
    print(f"SUCCESS: {len(draws)} validated current-format draws written to {destination}")
    print(f"Draw/date range: {draws[0][0]} ({draws[0][1]}) through "
          f"{draws[-1][0]} ({draws[-1][1]})")
    if (today - draws[-1][1]).days <= PUBLICATION_GRACE_DAYS:
        print("NOTE: Most recent Thursday may still be within publication grace period.")


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, ScrapeError, OSError, ValueError) as exc:
        raise SystemExit(f"FAILED: {exc}\nSource/validation failures preserve all existing CSVs; "
                         "if the failure was a local disk error during final saving, "
                         "inspect output files before rerunning.") from exc
