import calendar
import csv
import datetime
import re
import time
from typing import Dict, List, Optional, Tuple

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import Select

# ==============================================================================
# CONFIGURATION PARAMETERS
# ==============================================================================
START_YEAR = 2026
START_MONTH = 1  # 1 = January, 2 = February, etc.
END_YEAR = 2026
END_MONTH = 3  # Inclusive end month

# Choose games: "Powerball", "OzLotto", or both
GAMES_TO_PROCESS = ["Powerball", "OzLotto"]

# ------------------------------------------------------------------------------
# BLACKOUT SETTINGS:
# On and from this specific draw number (draw_number >= threshold),
# numbers will be blacked out. Set to None if no blackout is needed for that game.
# ------------------------------------------------------------------------------
BLACKOUT_DRAWS = {
    "Powerball": 1550,  # All Powerball draws >= 1550 are blacked out
    "OzLotto": 1670,  # All Oz Lotto draws >= 1670 are blacked out
}

# Choose action for blacked out draws:
# "EXCLUDE" -> completely discard the draw (not stored in CSV, not compared)
# "REDACT"  -> keep Draw Number & Date, but clear the numbers (e.g. "[BLACKOUT]")
BLACKOUT_ACTION = "EXCLUDE"

# Browser: "chrome" or "firefox"
BROWSER = "chrome"

# Headless mode: False displays the browser window
HEADLESS = False

# Delay between page requests / button clicks (in seconds)
DELAY_SECONDS = 2.0

# Output file paths
THELOTT_CSV_FILE = "thelott_results.csv"
LOTTERYWEST_CSV_FILE = "lotterywest_results.csv"
RECONCILIATION_REPORT_FILE = "reconciliation_report.txt"
# ==============================================================================


def is_draw_blacked_out(game: str, draw_no: int) -> bool:
  """Checks if a draw meets or exceeds the blackout threshold."""
  threshold = BLACKOUT_DRAWS.get(game)
  if threshold is not None and draw_no >= threshold:
    return True
  return False


def create_driver(browser_name: str, headless: bool):
  """Initializes Chrome or Firefox WebDriver."""
  if browser_name.lower() == "chrome":
    opts = ChromeOptions()
    if headless:
      opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=opts)
  elif browser_name.lower() == "firefox":
    opts = FirefoxOptions()
    if headless:
      opts.add_argument("--headless")
    return webdriver.Firefox(options=opts)
  else:
    raise ValueError(
        f"Unsupported browser: {browser_name}. Use 'chrome' or 'firefox'."
    )


def generate_year_month_range(
    start_y: int, start_m: int, end_y: int, end_m: int
):
  """Yields (year, month_int, month_name) from start to end inclusive."""
  cur_y, cur_m = start_y, start_m
  while (cur_y < end_y) or (cur_y == end_y and cur_m <= end_m):
    yield cur_y, cur_m, calendar.month_name[cur_m]
    cur_m += 1
    if cur_m > 12:
      cur_m = 1
      cur_y += 1


def standardize_date(date_str: str) -> str:
  """Normalizes various Australian lottery date formats to YYYY-MM-DD."""
  clean_str = re.sub(r"^[A-Za-z]{3},?\s*", "", date_str.strip())
  match = re.search(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", clean_str)
  if match:
    day, mon, yr = match.groups()
    for fmt in ("%d %B %Y", "%d %b %Y"):
      try:
        dt = datetime.datetime.strptime(f"{day} {mon} {yr}", fmt)
        return dt.strftime("%Y-%m-%d")
      except ValueError:
        continue
  return date_str.strip()


# ==============================================================================
# SCRAPER 1: THE LOTT
# ==============================================================================
def scrape_thelott(
    driver, game: str, year: int, month_name: str
) -> List[Dict]:
  url = (
      "https://www.thelott.com/powerball/results"
      if game == "Powerball"
      else "https://www.thelott.com/oz-lotto/results"
  )

  print(f"[The Lott] Querying {game} for {month_name} {year}...")
  if driver.current_url != url:
    driver.get(url)
    time.sleep(3)

  expected_ball_count = 8 if game == "Powerball" else 10

  # Locate Month and Year dropdowns
  select_elements = driver.find_elements(By.TAG_NAME, "select")
  month_select, year_select = None, None

  for s in select_elements:
    txt = s.text.lower()
    if "january" in txt or "february" in txt:
      month_select = Select(s)
    elif str(year) in txt or "2025" in txt or "2024" in txt:
      year_select = Select(s)

  if not month_select or not year_select:
    print(f"[The Lott] Could not find dropdown selects on {url}")
    return []

  month_select.select_by_visible_text(month_name)
  year_select.select_by_visible_text(str(year))

  find_btn = driver.find_element(
      By.XPATH,
      "//button[contains(translate(text(), 'find', 'FIND'), 'FIND')] |"
      " //a[contains(translate(text(), 'find', 'FIND'), 'FIND')]",
  )
  driver.execute_script("arguments[0].click();", find_btn)

  # Anti-detection delay
  time.sleep(DELAY_SECONDS)

  page_text = driver.find_element(By.TAG_NAME, "body").text
  split_heading = (
      "Search Powerball Results"
      if game == "Powerball"
      else "Search Oz Lotto Results"
  )
  results_block = (
      page_text.split(split_heading)[-1]
      if split_heading in page_text
      else page_text
  )

  pattern = re.compile(
      r"Draw\s+(\d+)\s+([A-Za-z]{3},?\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4})\s+([\d\s]+?)(?:Watch|Show|$)",
      re.MULTILINE,
  )

  results = []
  for match in pattern.finditer(results_block):
    draw_no = int(match.group(1))

    # Blackout enforcement
    if is_draw_blacked_out(game, draw_no):
      if BLACKOUT_ACTION == "EXCLUDE":
        continue
      else:
        results.append({
            "game": game,
            "draw_number": draw_no,
            "draw_date": standardize_date(match.group(2)),
            "drawn_numbers": "[BLACKOUT]",
            "blacked_out": True,
        })
        continue

    raw_date = match.group(2).strip()
    raw_nums = match.group(3).strip().split()

    if len(raw_nums) >= expected_ball_count:
      drawn_balls = raw_nums[:expected_ball_count]
      results.append({
          "game": game,
          "draw_number": draw_no,
          "draw_date": standardize_date(raw_date),
          "drawn_numbers": " ".join(drawn_balls),
          "blacked_out": False,
      })

  return results


# ==============================================================================
# SCRAPER 2: LOTTERYWEST
# ==============================================================================
def scrape_lotterywest(
    driver, game: str, year: int, month_name: str
) -> List[Dict]:
  game_slug = "powerball" if game == "Powerball" else "oz-lotto"
  url = f"https://www.oz.lotterywest.com/{game_slug}/results/{month_name.lower()}-{year}"

  print(f"[Lotterywest] Querying {game} from {url}...")
  driver.get(url)

  # Anti-detection delay
  time.sleep(DELAY_SECONDS)

  body_text = driver.find_element(By.TAG_NAME, "body").text
  expected_ball_count = 8 if game == "Powerball" else 10

  draw_pattern = re.compile(
      r"(\d{1,2}\s+[A-Za-z]+\s+\d{4}).*?Draw\s*(\d+)\s+Main"
      r" [nN]umbers([\s\S]*?)(?=Dividends|\d{1,2}\s+[A-Za-z]+\s+\d{4}|$)",
      re.IGNORECASE,
  )

  results = []
  for match in draw_pattern.finditer(body_text):
    raw_date = match.group(1).strip()
    draw_no = int(match.group(2))
    numbers_block = match.group(3)

    # Blackout enforcement
    if is_draw_blacked_out(game, draw_no):
      if BLACKOUT_ACTION == "EXCLUDE":
        continue
      else:
        results.append({
            "game": game,
            "draw_number": draw_no,
            "draw_date": standardize_date(raw_date),
            "drawn_numbers": "[BLACKOUT]",
            "blacked_out": True,
        })
        continue

    found_nums = re.findall(r"\b\d+\b", numbers_block)
    if len(found_nums) >= expected_ball_count:
      drawn_balls = found_nums[:expected_ball_count]
      results.append({
          "game": game,
          "draw_number": draw_no,
          "draw_date": standardize_date(raw_date),
          "drawn_numbers": " ".join(drawn_balls),
          "blacked_out": False,
      })

  return results


# ==============================================================================
# CSV EXPORT & RECONCILIATION
# ==============================================================================
def save_to_csv(filepath: str, data: List[Dict]):
  """Saves rows to CSV."""
  with open(filepath, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Game", "Draw Number", "Draw Date", "Drawn Numbers"])
    for row in sorted(data, key=lambda x: (x["game"], x["draw_number"])):
      writer.writerow(
          [row["game"], row["draw_number"], row["draw_date"], row["drawn_numbers"]]
      )
  print(f"Saved {len(data)} rows to {filepath}")


def reconcile_data(thelott_list: List[Dict], lw_list: List[Dict]):
  """Performs reconciliation respecting blacked out draws."""
  thelott_map = {(r["game"], r["draw_number"]): r for r in thelott_list}
  lw_map = {(r["game"], r["draw_number"]): r for r in lw_list}

  all_keys = sorted(
      set(thelott_map.keys()) | set(lw_map.keys()), key=lambda k: (k[0], k[1])
  )

  report_lines = []
  report_lines.append("=" * 80)
  report_lines.append("                    RESULTS RECONCILIATION REPORT")
  report_lines.append("=" * 80)

  mismatches = 0
  matches = 0
  blacked_out_count = 0

  for game, draw_no in all_keys:
    t_item = thelott_map.get((game, draw_no))
    lw_item = lw_map.get((game, draw_no))

    if not t_item:
      report_lines.append(
          f"[-] MISMATCH: Draw {draw_no} ({game}) found in Lotterywest but"
          " MISSING from The Lott"
      )
      mismatches += 1
      continue

    if not lw_item:
      report_lines.append(
          f"[-] MISMATCH: Draw {draw_no} ({game}) found in The Lott but MISSING"
          " from Lotterywest"
      )
      mismatches += 1
      continue

    if t_item.get("blacked_out") or lw_item.get("blacked_out"):
      blacked_out_count += 1
      report_lines.append(
          f"[*] BLACKOUT: {game} Draw {draw_no:4d} | Date: {t_item['draw_date']} |"
          " Numbers Redacted"
      )
      continue

    date_match = t_item["draw_date"] == lw_item["draw_date"]
    nums_match = t_item["drawn_numbers"] == lw_item["drawn_numbers"]

    if date_match and nums_match:
      matches += 1
      report_lines.append(
          f"[+] MATCH:    {game:9s} Draw {draw_no:4d} | Date: {t_item['draw_date']}"
          f" | Numbers: {t_item['drawn_numbers']}"
      )
    else:
      mismatches += 1
      report_lines.append(f"[-] DISCREPANCY DETECTED: {game} Draw {draw_no}")
      if not date_match:
        report_lines.append(
            f"    Date mismatch: The Lott={t_item['draw_date']} vs"
            f" LW={lw_item['draw_date']}"
        )
      if not nums_match:
        report_lines.append(
            f"    Numbers mismatch: The Lott=[{t_item['drawn_numbers']}] vs"
            f" LW=[{lw_item['drawn_numbers']}]"
        )

  report_lines.append("=" * 80)
  report_lines.append(
      f"SUMMARY: {matches} matched | {blacked_out_count} blacked out |"
      f" {mismatches} discrepancies"
  )
  report_lines.append("=" * 80)

  report_text = "\n".join(report_lines)
  print("\n" + report_text)

  with open(RECONCILIATION_REPORT_FILE, "w", encoding="utf-8") as rf:
    rf.write(report_text)
  print(f"\nReconciliation report written to {RECONCILIATION_REPORT_FILE}")


def main():
  print("Starting Lottery Data Harvester with Blackout Control...")
  print(
      f"Date Range : {START_YEAR}-{START_MONTH:02d} to"
      f" {END_YEAR}-{END_MONTH:02d}"
  )
  print(f"Blackouts  : {BLACKOUT_DRAWS} (Action: {BLACKOUT_ACTION})")
  print(f"Rate Delay : {DELAY_SECONDS} seconds\n")

  driver = create_driver(BROWSER, HEADLESS)
  thelott_all = []
  lotterywest_all = []

  try:
    for game in GAMES_TO_PROCESS:
      for year, month, m_name in generate_year_month_range(
          START_YEAR, START_MONTH, END_YEAR, END_MONTH
      ):
        # 1. Scrape The Lott
        tl_draws = scrape_thelott(driver, game, year, m_name)
        thelott_all.extend(tl_draws)

        # 2. Scrape Lotterywest
        lw_draws = scrape_lotterywest(driver, game, year, m_name)
        lotterywest_all.extend(lw_draws)

  finally:
    driver.quit()

  # Save CSV files
  save_to_csv(THELOTT_CSV_FILE, thelott_all)
  save_to_csv(LOTTERYWEST_CSV_FILE, lotterywest_all)

  # Run reconciliation
  reconcile_data(thelott_all, lotterywest_all)


if __name__ == "__main__":
  main()

#How the Blackout Works:
#  - If you set BLACKOUT_DRAWS = {"Powerball": 1550, "OzLotto": 1670} and keep
#    BLACKOUT_ACTION = "EXCLUDE", any draw where draw_number >= 1550 for
#    Powerball or draw_number >= 1670 for Oz Lotto is filtered immediately at the
#    extraction level.
#  - It will not appear in either CSV, will not be printed in console output, and
#    will not be checked during reconciliation.
#  - If you want to disable the blackout for any game, set its value to None
#    (e.g. "OzLotto": None).

