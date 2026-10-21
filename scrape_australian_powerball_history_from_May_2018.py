"""Download and validate Australian Powerball draw histories from powerball.net.

Requires: python -m pip install requests beautifulsoup4

The seven main numbers are stored in the order displayed by the archive
(typically ascending), NOT necessarily their physical drawing order.

"""

# AUS POWERBALL from 3 May 2018 onward (7/35 + 1/20 format):
# Each Thursday after 7:30pm AEST, the Powerball game is drawn from 2 barrels:
# - 7 numbers are drawn from the main barrel (numbered from 1 to 35)
# - 1 Powerball number is drawn from the Powerball barrel (numbered from 1 to 20).
# To win Division 1, you need to have done both of these things in a single game entry:
# a) select all 7 winning numbers drawn from the main barrel 
# b) select the winning Powerball number drawn from the Powerball barrel

import csv
import os
import re
import tempfile
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.powerball.net/australia/archive/"
START_DATE = date(2018, 5, 3)  # First May draw; Draw 1146
START_YEAR = START_DATE.year
OUTPUT_FILE = Path(__file__).with_name(
    f"australian_powerball_history_{date.today():%Y%m%d}.csv"
)
RESULT_PATH = re.compile(r"/australia/results/(\d{4}-\d{2}-\d{2})/?")
DRAW_NUMBER = re.compile(r"\bDraw\s+(\d+)\b", re.IGNORECASE)
NUMBER = re.compile(r"(?<!\w)\d{1,2}(?!\w)")
FIELDS = ["Draw_Number", "Date"] + [f"Ball_{n}" for n in range(1, 8)] + ["Powerball"]


class ScrapeError(Exception):
    """Archive format or data-integrity problem."""


def extract_draw(anchor, day):
    """Find draw number and exactly eight balls in one archive entry.

    Usually the anchor contains the whole result. The nearest enclosing
    element is an alternative if the site's markup splits a result across
    an anchor and nearby text.
    """
    candidates = [anchor]
    if anchor.parent is not None:
        candidates.append(anchor.parent)
    if anchor.parent is not None and anchor.parent.parent is not None:
        candidates.append(anchor.parent.parent)

    for element in candidates:
        value = element.get_text(" ", strip=True)
        matches = list(DRAW_NUMBER.finditer(value))
        if len(matches) != 1:
            continue
        draw_num = int(matches[0].group(1))
        tail = value[matches[0].end():]
        balls = [int(s) for s in NUMBER.findall(tail)]
        if len(balls) == 8:
            if (len(set(balls[:7])) == 7
                    and all(1 <= n <= 35 for n in balls[:7])
                    and 1 <= balls[7] <= 20):
                return (draw_num, day, *balls)

    raise ScrapeError(
        f"Cannot extract exactly 7 main balls and 1 Powerball for {day}. "
        f"Result link text: {anchor.get_text(' ', strip=True)!r}"
    )


def parse_archive(html, year):
    soup = BeautifulSoup(html, "html.parser")
    results = {}
    matched_links = 0

    for anchor in soup.find_all("a", href=True):
        url = urljoin(BASE_URL, anchor["href"])
        parsed = urlparse(url)
        match = RESULT_PATH.fullmatch(parsed.path)
        if not match or parsed.hostname != "www.powerball.net":
            continue
        day = date.fromisoformat(match.group(1))
        # 2018 includes earlier 6/40 draws that MUST be excluded
        # before extract_draw(), which expects seven main balls.
        if day.year != year or day < START_DATE:
            continue
        matched_links += 1
        draw = extract_draw(anchor, day)
        previous = results.get(day)
        if previous is not None and previous != draw:
            raise ScrapeError(f"Contradictory results for {day} on {year} page")
        results[day] = draw

    if not results:
        title = soup.title.get_text(" ", strip=True) if soup.title else "(no title)"
        raise ScrapeError(
            f"No valid draw entries found on {year} archive page "
            f"(matching result links: {matched_links}; page title: {title!r}). "
            "The site's layout or the downloaded page may have changed."
        )

    return list(results.values())


def expected_thursdays(year, cutoff):
    beginning = max(date(year, 1, 1), START_DATE)
    ending = min(date(year, 12, 31), cutoff)
    if beginning > ending:
        return set()
    first = beginning + timedelta(days=(3 - beginning.weekday()) % 7)
    dates = set()
    d = first
    while d <= ending:
        dates.add(d)
        d += timedelta(days=7)
    return dates


def check_completeness(draws, start_year, end_year, today):
    seen_dates = set()
    seen_numbers = set()
    for draw in draws:
        draw_num, day, *balls = draw
        if day < START_DATE:
            raise ScrapeError(f"Draw before supported start date: {draw_num}, {day}")
        if day in seen_dates or draw_num in seen_numbers:
            raise ScrapeError(f"Duplicate draw number or date: {draw_num}, {day}")
        seen_dates.add(day)
        seen_numbers.add(draw_num)

    # Allow up to two days for publication of the most recent Thursday draw.
    cutoff = today - timedelta(days=2)
    for year in range(start_year, end_year + 1):
        expected = expected_thursdays(year, cutoff)
        actual = {draw[1] for draw in draws if draw[1].year == year}
        missing = sorted(expected - actual)
        unexpected = sorted(day for day in actual if day.weekday() != 3 or day > today)
        if missing or unexpected:
            raise ScrapeError(
                f"Year {year} incomplete/inconsistent: "
                f"missing expected draws {missing[:8]}; "
                f"unexpected draw dates {unexpected[:8]}"
            )

    chronological = sorted(draws, key=lambda row: row[1])
    for previous, current in zip(chronological, chronological[1:]):
        if current[0] != previous[0] + 1:
            raise ScrapeError(
                f"Nonconsecutive draw numbers: {previous[0]} ({previous[1]}) "
                f"then {current[0]} ({current[1]})"
            )
        if (current[1] - previous[1]).days != 7:
            raise ScrapeError(
                f"Nonweekly draw dates: {previous[1]} then {current[1]}"
            )
    if chronological and (chronological[0][0], chronological[0][1]) != (1146, START_DATE):
        raise ScrapeError(f"Unexpected first draw: {chronological[0][0:2]!r}; "
                          f"expected Draw 1146 on {START_DATE}")
    return chronological


def save_csv_atomically(draws, destination):
    # Never overwrite a good existing CSV with an empty or failed scrape.
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", newline="", encoding="utf-8", suffix=".tmp",
            dir=destination.parent, delete=False
        ) as out:
            temporary_path = Path(out.name)
            writer = csv.writer(out)
            writer.writerow(FIELDS)
            for draw_num, day, *balls in draws:
                writer.writerow([draw_num, day.isoformat(), *balls])
        os.replace(temporary_path, destination)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def main():
    today = date.today()
    end_year = today.year
    if end_year < START_YEAR:
        raise ScrapeError("Local system date is before START_YEAR")
    all_draws = []

    with requests.Session() as session:
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; AustralianPowerballArchiveResearch/1.0)"
        })
        for year in range(START_YEAR, end_year + 1):
            url = f"{BASE_URL}{year}"
            print(f"Fetching {year}: {url}", flush=True)
            response = session.get(url, timeout=25)
            response.raise_for_status()
            year_draws = parse_archive(response.text, year)
            print(f"  Found {len(year_draws)} draw(s)", flush=True)
            all_draws.extend(year_draws)

    if not all_draws:
        raise ScrapeError("No draws extracted; not creating CSV")
    validated = check_completeness(all_draws, START_YEAR, end_year, today)
    save_csv_atomically(validated, OUTPUT_FILE)
    print(f"SUCCESS: {len(validated)} validated draws written to {OUTPUT_FILE}")
    print(f"Date range: {validated[0][1]} through {validated[-1][1]}")


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, ScrapeError, OSError) as error:
        raise SystemExit(f"FAILED: {error}\nExisting CSV has not been replaced.") from error
