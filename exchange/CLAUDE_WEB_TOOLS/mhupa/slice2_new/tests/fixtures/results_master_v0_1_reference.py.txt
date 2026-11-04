"""Results master files: initialise and update. v0.1.

One master file per game holds the latest APPROVED results, keyed by
(game, draw_number), in drawn order:

    source_data/POWERBALL_results_master.csv
        Draw_Number,Date,Drawn_1..Drawn_7,Powerball
    source_data/OZLOTTO_results_master.csv
        Draw_Number,Date,Drawn_1..Drawn_7,Supp_1,Supp_2,Supp_3

Alongside each master:
    source_data/<GAME>_results_master_ledger.csv    one appended line per version (append-only)
    source_data/backups/<GAME>_master_draws_<a>-<b>_as_at_<UTC>.csv   exact prior copies (create-only)
    source_data/grabs/<GAME>_grab_draws_<a>-<b>_as_at_<UTC>.csv       what each update fetched (create-only)
    source_data/<GAME>_results_master_init_verification.json          evidence for the first version

Commands
    python src\\results_master_v0_1.py --self-test
    python src\\results_master_v0_1.py init --build-run <history build run> --lott-check-run <Lott cross-check run>
    python src\\results_master_v0_1.py update [--games POWERBALL,OZLOTTO] [--months-back 5] [--browser chrome]

Quarantine (holdout): until source_data/HOLDOUT_OPENED_<GAME>.json exists (a
deliberate owner step at Mode H), no master may contain, and no update may
request, any draw dated on or after QUARANTINE_START_DATE. There is no
command-line override. The update command is NOT to be run until the owner
decides (after the holdout experiments).

Source for updates: Lotterywest's own results-search page on
www.lotterywest.wa.gov.au (owner decision: accepted as official). Honest
automation only: headless real browser, default settings, >= 2 s between page
loads, a block/challenge page means STOP.

Exit codes: 0 success (or nothing new); 1 verification failure or mismatch;
2 STOP (blocked page, quarantine reached, parse failure); 3 refused.
"""
from __future__ import annotations

import argparse
import calendar
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from types import MappingProxyType

TOOL_VERSION = "0.1"

# ---------------------------------------------------------------------------
# Fixed constants. No command-line override for any quarantine value.
# ---------------------------------------------------------------------------
QUARANTINE_START_DATE = date(2026, 8, 1)
FIRST_QUARANTINED_DRAW = MappingProxyType({"POWERBALL": 1577, "OZLOTTO": 1694})
DEFAULT_MONTHS_BACK = 5            # current month plus the previous 5
MAX_MONTHS_BACK = 60
MIN_PAUSE_SECONDS = 2.0
PAGE_WAIT_SECONDS = 15.0
WAIT_POLL_SECONDS = 0.5
OLD_POWERBALL_COMMIT = "06f6e0f"
OLD_HISTORY = "source_data/australian_powerball_history_20261021.csv"
OLD_ORDER = "source_data/australian_powerball_draw_order_20261021.csv"
LEDGER_COLUMNS = ("version", "utc", "action", "master_sha256", "first_draw", "last_draw", "draw_count",
                  "added_count", "added_first", "added_last", "grab_file", "grab_sha256",
                  "backup_file", "backup_sha256", "tool_version", "tool_sha256", "note")


@dataclass(frozen=True)
class Era:
    first_draw: int
    first_date: date
    weekday: int          # Monday = 0
    main_max: int
    secondary_count: int
    secondary_max: int
    slug: str
    lotterywest_code: int


ERAS = MappingProxyType({
    "POWERBALL": Era(1144, date(2018, 4, 19), 3, 35, 1, 20, "powerball", 5132),
    "OZLOTTO": Era(1474, date(2022, 5, 17), 1, 47, 3, 47, "oz-lotto", 5130),
})
MONTH_NAMES = tuple(calendar.month_name[1:])


class Refused(Exception):
    pass


class Stop(Exception):
    pass


class VerifyFail(Exception):
    pass


@dataclass(frozen=True)
class Draw:
    game: str
    number: int
    day: str                 # ISO date
    main: tuple[int, ...]    # drawn order
    secondary: tuple[int, ...]


# ---------------------------------------------------------------------------
# Pure rules
# ---------------------------------------------------------------------------
def derived_date(game: str, n: int) -> date:
    e = ERAS[game]
    return e.first_date + timedelta(days=7 * (n - e.first_draw))


def header(game: str) -> list[str]:
    cols = ["Draw_Number", "Date"] + [f"Drawn_{i}" for i in range(1, 8)]
    return cols + (["Powerball"] if game == "POWERBALL" else ["Supp_1", "Supp_2", "Supp_3"])


def check_constants() -> None:
    for g, fq in FIRST_QUARANTINED_DRAW.items():
        if not derived_date(g, fq) >= QUARANTINE_START_DATE > derived_date(g, fq - 1):
            raise Refused(f"{g}: quarantine constants disagree")
    if not 1 <= DEFAULT_MONTHS_BACK <= MAX_MONTHS_BACK or MIN_PAUSE_SECONDS < 2.0:
        raise Refused("window or pause constants invalid")


def holdout_opened(root: Path, game: str) -> bool:
    """True only if a well-formed owner record exists. Its creation is a Mode H step."""
    p = root / "source_data" / f"HOLDOUT_OPENED_{game}.json"
    if not p.exists():
        return False
    if p.is_symlink() or not p.is_file():
        raise Refused(f"{p.name} is not a regular file")
    try:
        rec = json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        raise Refused(f"{p.name} is not valid JSON") from None
    if (rec.get("schema") != "HOLDOUT_OPENED_V1" or rec.get("game") != game or
            not re.fullmatch(r"[0-9a-f]{64}", str(rec.get("study_manifest_sha256", ""))) or
            not rec.get("opened_utc") or not rec.get("owner_statement")):
        raise Refused(f"{p.name} is incomplete; the holdout is NOT treated as opened")
    return True


def validate_draw(d: Draw, *, quarantine_closed: bool) -> list[str]:
    """Raise VerifyFail on any hard error; return warnings (date off weekly rule)."""
    e = ERAS[d.game]
    day = date.fromisoformat(d.day)
    if quarantine_closed and (d.number >= FIRST_QUARANTINED_DRAW[d.game] or day >= QUARANTINE_START_DATE):
        raise Stop(f"{d.game}: a quarantined draw was encountered (numbers withheld)")
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


def validate_series(game: str, draws: list[Draw], *, quarantine_closed: bool) -> list[str]:
    """Consecutive from the era's first draw, every draw valid. Returns warnings."""
    if not draws:
        raise VerifyFail(f"{game}: no draws")
    warns = []
    for i, d in enumerate(draws):
        if d.game != game or d.number != ERAS[game].first_draw + i:
            raise VerifyFail(f"{game}: draws not consecutive from {ERAS[game].first_draw} (at position {i})")
        warns += validate_draw(d, quarantine_closed=quarantine_closed)
    return warns


def to_csv_bytes(game: str, draws: list[Draw]) -> bytes:
    out = [",".join(header(game))]
    for d in draws:
        out.append(",".join(str(x) for x in (d.number, d.day, *d.main, *d.secondary)))
    return ("\r\n".join(out) + "\r\n").encode("ascii")


def from_csv_bytes(game: str, data: bytes) -> list[Draw]:
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
    return hashlib.sha256(data).hexdigest()


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def write_new(path: Path, data: bytes) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as fh:      # create-only
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    return sha(data)


def replace_atomically(path: Path, data: bytes) -> str:
    tmp = path.with_name(path.name + f".part-{os.getpid()}")
    with tmp.open("xb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)
    return sha(data)


def month_window(today: date, months_back: int) -> tuple[date, date]:
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
    def __init__(self, root: Path, game: str):
        self.root, self.game = root, game
        self.dir = root / "source_data"
        self.master = self.dir / f"{game}_results_master.csv"
        self.ledger = self.dir / f"{game}_results_master_ledger.csv"
        self.backups = self.dir / "backups"
        self.grabs = self.dir / "grabs"
        self.init_record = self.dir / f"{game}_results_master_init_verification.json"

    def ledger_rows(self) -> list[dict]:
        if not self.ledger.is_file():
            return []
        rows = list(csv.DictReader(io.StringIO(self.ledger.read_bytes().decode("ascii"))))
        if rows and tuple(rows[0].keys()) != LEDGER_COLUMNS:
            raise VerifyFail(f"{self.ledger.name}: unexpected columns")
        return rows

    def append_ledger(self, row: dict) -> None:
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

    def load_verified_master(self, *, quarantine_closed: bool) -> tuple[list[Draw], bytes, dict]:
        if not self.master.is_file() or self.master.is_symlink():
            raise Refused(f"{self.master.name} not found (run init first)")
        data = self.master.read_bytes()
        rows = self.ledger_rows()
        if not rows:
            raise VerifyFail(f"{self.ledger.name} missing or empty")
        last = rows[-1]
        if sha(data) != last["master_sha256"]:
            raise VerifyFail(f"{self.master.name} does not match the last ledger entry (edited outside the tool, "
                             "or an update was interrupted: see source_data/backups and the ledger)")
        draws = from_csv_bytes(self.game, data)
        validate_series(self.game, draws, quarantine_closed=quarantine_closed)
        if len(draws) != int(last["draw_count"]) or draws[-1].number != int(last["last_draw"]):
            raise VerifyFail(f"{self.master.name} disagrees with its ledger counts")
        return draws, data, last


def tool_sha() -> str:
    return sha(Path(__file__).read_bytes())


# ---------------------------------------------------------------------------
# INIT (offline): first master from the verified history build
# ---------------------------------------------------------------------------
def old_powerball_dev_rows(root: Path) -> tuple[dict, dict, str]:
    """Old committed files, DEVELOPMENT ROWS ONLY (draw number checked before any other field)."""
    def raw(rel):
        p = root / rel
        if p.is_file():
            return p.read_bytes(), f"working tree {rel}"
        r = subprocess.run(["git", "-C", str(root), "show", f"{OLD_POWERBALL_COMMIT}:{rel}"],
                           capture_output=True, timeout=30, check=False)
        if r.returncode:
            raise Refused(f"old file not available: {rel}")
        return r.stdout, f"git {OLD_POWERBALL_COMMIT}:{rel}"

    def dev_only(data: bytes):
        lines = data.decode("utf-8-sig").splitlines()
        keep = [lines[0]]
        for ln in lines[1:]:
            first = ln.split(",", 1)[0].strip()
            if first.isdigit() and int(first) < FIRST_QUARANTINED_DRAW["POWERBALL"]:
                keep.append(ln)
        return {int(r["Draw_Number"]): r for r in csv.DictReader(keep)}
    hb, hs = raw(OLD_HISTORY)
    ob, os_ = raw(OLD_ORDER)
    return dev_only(hb), dev_only(ob), f"{hs}; {os_}"


def read_build_run(run: Path, game: str) -> tuple[list[Draw], dict]:
    prov_path = run / "provenance.json"
    prov = json.loads(prov_path.read_text(encoding="utf-8"))
    if prov.get("mode") != "BUILD_HISTORY_LOTTERYWEST_GOV":
        raise Refused(f"{run.name} is not a history-build run")
    name = f"lotterywest_dev_{game}.csv"
    data = (run / name).read_bytes()
    if sha(data) != prov.get("output_sha256", {}).get(name):
        raise VerifyFail(f"{name} does not match its recorded SHA-256")
    s = prov.get("summary", {}).get(game, {})
    if s.get("missing") != 0 or s.get("unexpected") != 0 or s.get("date_vs_weekly_rule_fail") != 0:
        raise VerifyFail(f"{run.name}: build reported missing/unexpected/off-date {game} draws")
    if game == "POWERBALL" and prov.get("summary", {}).get("POWERBALL_vs_old_files", {}).get("fail") != 0:
        raise VerifyFail(f"{run.name}: build reported old-file comparison failures")
    rows = list(csv.reader(io.StringIO(data.decode("ascii"))))
    k = ERAS[game].secondary_count
    if not rows or rows[0] != ["Game"] + header(game) + ["Source", "Order_Label"]:
        raise VerifyFail(f"{name}: header not recognised")
    draws = []
    for r in rows[1:]:
        if len(r) != 12 + k or r[0] != game or r[10 + k] != "LOTTERYWEST_GOV_RESULTS_SEARCH":
            raise VerifyFail(f"{name}: unexpected column count, game or source column")
        first = r[1].strip()
        if not first.isdigit() or int(first) >= FIRST_QUARANTINED_DRAW[game]:
            raise Stop(f"{name}: a quarantined draw is present (numbers withheld)")
        draws.append(Draw(game, int(r[1]), r[2], tuple(int(x) for x in r[3:10]), tuple(int(x) for x in r[10:10 + k])))
    return sorted(draws, key=lambda d: d.number), {"run": run.name, "provenance_sha256": sha(prov_path.read_bytes()),
                                                    "csv": name, "csv_sha256": sha(data),
                                                    "build_tool_version": prov.get("tool_version"),
                                                    "build_tool_sha256": prov.get("script_sha256")}


def read_lott_check_run(run: Path, build_run: Path) -> dict:
    prov_path = run / "provenance.json"
    prov = json.loads(prov_path.read_text(encoding="utf-8"))
    if prov.get("mode") != "OFFLINE_SAVED_PAGES":
        raise Refused(f"{run.name} is not an offline cross-check run")
    against = [i.get("against_run") for i in prov.get("inputs", []) if "against_run" in i]
    if not against or re.split(r"[\\/]", str(against[0]).rstrip("\\/"))[-1] != build_run.name:
        raise Refused(f"{run.name} was not run against {build_run.name}")
    out = {"run": run.name, "provenance_sha256": sha(prov_path.read_bytes()), "summary": prov.get("summary", {})}
    for g, c in out["summary"].items():
        if c.get("fail") != 0 or c.get("all_pass") != c.get("expected"):
            raise VerifyFail(f"{run.name}: The Lott cross-check reported failures for {g}")
    out["saved_pages"] = len([i for i in prov.get("inputs", []) if i.get("source") == "thelott"])
    # Per-field tallies from the value-free reconciliation report (hash-checked first).
    rep_path = run / "reconciliation.txt"
    if rep_path.is_file():
        data = rep_path.read_bytes()
        if sha(data) != prov.get("output_sha256", {}).get("reconciliation.txt"):
            raise VerifyFail(f"{run.name}: reconciliation.txt does not match its recorded SHA-256")
        fields: dict = {}
        for line in data.decode("ascii").splitlines():
            m = re.fullmatch(r"(POWERBALL|OZLOTTO) \d+: (.*)", line)
            if not m or "MISSING" in line or "UNEXPECTED" in line:
                continue
            for part in m.group(2).split(", "):
                k, _, v = part.rpartition(" ")
                fields.setdefault(m.group(1), {}).setdefault(k, {}).setdefault(v, 0)
                fields[m.group(1)][k][v] += 1
        out["fields"] = fields
        for g, f in fields.items():
            if any(v.get("FAIL") for v in f.values()):
                raise VerifyFail(f"{run.name}: a field FAIL is recorded for {g}")
    return out


def cmd_init(root: Path, build_run: Path, lott_run: Path, games: list[str]) -> int:
    check_constants()
    lott = read_lott_check_run(lott_run, build_run)
    for game in games:
        st = Store(root, game)
        for p in (st.master, st.ledger, st.init_record):
            if p.exists():
                raise Refused(f"{p.name} already exists; init is a one-off")
    results = {}
    for game in games:
        draws, build = read_build_run(build_run, game)
        warns = validate_series(game, draws, quarantine_closed=True)
        if warns:
            raise VerifyFail(f"{game}: {len(warns)} draw date(s) off the weekly rule")
        if draws[-1].number != FIRST_QUARANTINED_DRAW[game] - 1:
            raise VerifyFail(f"{game}: build does not reach the last development draw")
        ls = lott["summary"].get(game) or {}
        if not ls.get("all_pass"):
            raise VerifyFail(f"{game}: no The Lott cross-check results")
        check = {"source": "LOTTERYWEST_GOV_RESULTS_SEARCH", "build": build, "warnings": len(warns),
                 "lott_sample": lott["summary"].get(game), "lott_sample_fields": lott.get("fields", {}).get(game),
                 "lott_check_run": lott["run"],
                 "lott_check_provenance_sha256": lott["provenance_sha256"]}
        if game == "POWERBALL":
            hist, order, src = old_powerball_dev_rows(root)
            passed = 0
            for d in draws:
                h, o = hist.get(d.number), order.get(d.number)
                if (h and o and d.day == h["Date"] == o["Date"] and
                        d.main == tuple(int(o[f"Drawn_{i}"]) for i in range(1, 8)) and
                        tuple(sorted(d.main)) == tuple(int(h[f"Ball_{i}"]) for i in range(1, 8)) and
                        d.secondary[0] == int(h["Powerball"]) == int(o["Powerball"])):
                    passed += 1
            if passed != len(draws) or len(hist) != len(draws) or len(order) != len(draws):
                raise VerifyFail(f"POWERBALL: old-file comparison {passed}/{len(draws)}")
            check["old_files"] = {"source": src, "compared": len(draws), "passed": passed}
        results[game] = (draws, check)
    for game, (draws, check) in results.items():
        st = Store(root, game)
        data = to_csv_bytes(game, draws)
        h = write_new(st.master, data)
        record = {"schema": "RESULTS_MASTER_INIT_VERIFICATION_V1", "game": game, "tool_version": TOOL_VERSION,
                  "tool_sha256": tool_sha(), "utc": datetime.now(timezone.utc).isoformat(),
                  "master_file": st.master.name, "master_sha256": h, "first_draw": draws[0].number,
                  "last_draw": draws[-1].number, "draw_count": len(draws),
                  "quarantine": {"start_date": QUARANTINE_START_DATE.isoformat(),
                                 "first_quarantined_draw": FIRST_QUARANTINED_DRAW[game]}, **check}
        write_new(st.init_record, (json.dumps(record, indent=1, sort_keys=True) + "\n").encode("ascii"))
        st.append_ledger({"version": 1, "utc": record["utc"], "action": "INIT", "master_sha256": h,
                          "first_draw": draws[0].number, "last_draw": draws[-1].number, "draw_count": len(draws),
                          "added_count": len(draws), "added_first": draws[0].number, "added_last": draws[-1].number,
                          "tool_version": TOOL_VERSION, "tool_sha256": tool_sha(),
                          "note": f"from {check['build']['run']}; verified (see {st.init_record.name})"})
        print(f"[MASTER] {game}: INIT {len(draws)} draws {draws[0].number}..{draws[-1].number}, "
              f"sha256 {h[:16]}..., warnings {check['warnings']}")
        if "old_files" in check:
            print(f"[MASTER] {game}: old committed files {check['old_files']['passed']}/{check['old_files']['compared']} PASS")
        print(f"[MASTER] {game}: The Lott sample {check['lott_sample']}")
        for k, v in sorted((check.get("lott_sample_fields") or {}).items()):
            print(f"[MASTER] {game}:   The Lott sample field {k}: {v}")
    # Prove what was written: reload through the normal verified path and compare with the build.
    for game, (built, _) in results.items():
        draws, _, _ = Store(root, game).load_verified_master(quarantine_closed=True)
        if draws != built:
            raise VerifyFail(f"{game}: master re-read differs from the build")
        print(f"[MASTER] {game}: re-read, verified and identical to the build ({len(draws)} draws)")
    return 0


# ---------------------------------------------------------------------------
# UPDATE (network; not to be run until the owner decides)
# ---------------------------------------------------------------------------
_WEEKDAYS = "Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday"
_MONTHS = (r"Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|"
           r"Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?")
_HEAD = re.compile(rf"Draw\s+(?P<n>\d{{3,5}})\s+(?:{_WEEKDAYS})\s+(?P<d>\d{{1,2}})\s+(?P<m>{_MONTHS})\s+(?P<y>\d{{4}})")


def _month_no(tok: str) -> int:
    return [m[:3].lower() for m in MONTH_NAMES].index(tok[:3].lower()) + 1


def parse_gov(game: str, text: str, a: date, b: date, *, quarantine_closed: bool) -> list[Draw]:
    """Lotterywest results-search text. Each block is checked on number/date BEFORE its numbers are read."""
    heads = list(_HEAD.finditer(text))
    out = []
    for i, h in enumerate(heads):
        n = int(h.group("n"))
        day = date(int(h.group("y")), _month_no(h.group("m")), int(h.group("d")))
        if quarantine_closed and (n >= FIRST_QUARANTINED_DRAW[game] or day >= QUARANTINE_START_DATE):
            raise Stop(f"{game}: a quarantined draw appeared on the page (numbers withheld)")
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
            validate_draw(d, quarantine_closed=quarantine_closed)
        except VerifyFail as exc:
            raise Stop(str(exc)) from None
        out.append(d)
    return out


def gov_url(game: str, a: date, b: date) -> str:
    f = lambda d: d.strftime("%a+%b+%d+%Y")
    e = ERAS[game]
    return (f"https://www.lotterywest.wa.gov.au/results/{e.slug}?fromDate={f(a)}&toDate={f(b)}"
            f"&filterByGame={e.lotterywest_code}")


class BrowserFetcher:
    """Real fetcher: headless, unmodified browser; only the page's own requests."""

    def __init__(self, browser: str, pause: float):
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

    def fetch(self, game: str, a: date, b: date, *, quarantine_closed: bool) -> list[Draw]:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.common.exceptions import TimeoutException
        if quarantine_closed and b >= QUARANTINE_START_DATE:
            raise Refused(f"{game}: search window reaches the quarantine; nothing requested")
        url = gov_url(game, a, b)
        gap = time.monotonic() - self.last
        if self.last and gap < self.pause:
            time.sleep(self.pause - gap)
        self.last = time.monotonic()
        self.log.append({"utc": datetime.now(timezone.utc).isoformat(), "url": url})
        self.driver.get(url)
        if any(k in (self.driver.title or "").lower() for k in ("attention required", "cloudflare", "access denied", "just a moment")):
            raise Stop("www.lotterywest.wa.gov.au served a block/challenge page; nothing was bypassed")
        inner, n = [], ERAS[game].first_draw
        while derived_date(game, n) < b:
            if derived_date(game, n) > a:
                inner.append(n)
            n += 1
        seen = {"headings": 0}

        def ready(d):
            t = d.find_element(By.TAG_NAME, "body").text
            seen["headings"] = sum(1 for h in _HEAD.finditer(t)
                                   if a < date(int(h.group("y")), _month_no(h.group("m")), int(h.group("d"))) < b)
            return t if seen["headings"] >= len(inner) else False
        try:
            text = WebDriverWait(self.driver, PAGE_WAIT_SECONDS, poll_frequency=WAIT_POLL_SECONDS).until(ready)
        except TimeoutException:
            raise Stop(f"results for {a}..{b} did not appear (expected at least {len(inner)}, saw {seen['headings']})") from None
        return parse_gov(game, text, a, b, quarantine_closed=quarantine_closed)

    def close(self):
        self.driver.quit()


def update_game(root: Path, game: str, fetcher, months_back: int, today: date) -> dict:
    st = Store(root, game)
    closed = not holdout_opened(root, game)
    a, b = month_window(today, months_back)
    if closed and b >= QUARANTINE_START_DATE:
        raise Refused(f"{game}: the holdout is not opened; an update window ending {b} would reach the "
                      f"quarantine (from {QUARANTINE_START_DATE}). Nothing was requested.")
    master, master_bytes, last = st.load_verified_master(quarantine_closed=closed)
    got: dict[int, Draw] = {}
    for (wa, wb) in split_windows(a, b):
        for d in fetcher.fetch(game, wa, wb, quarantine_closed=closed):
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
    warns = [w for d in new for w in validate_draw(d, quarantine_closed=closed)]
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
    validate_series(game, merged, quarantine_closed=closed)
    h = replace_atomically(st.master, to_csv_bytes(game, merged))
    row.update({"action": "UPDATE", "master_sha256": h, "last_draw": merged[-1].number, "draw_count": len(merged),
                "added_count": len(new), "added_first": new[0].number, "added_last": new[-1].number,
                "backup_file": backup.name, "backup_sha256": backup_sha,
                "note": f"{len(overlap)} overlapping draws matched; {len(warns)} date warnings"})
    st.append_ledger(row)
    st.load_verified_master(quarantine_closed=closed)
    return {"game": game, "checked": len(overlap), "added": len(new), "added_range": f"{new[0].number}..{new[-1].number}",
            "warnings": warns, "grab": grab_path.name, "backup": backup.name}


class Lock:
    def __init__(self, root: Path):
        self.path = root / "source_data" / ".results_master.lock"

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise Refused(f"{self.path.name} exists: another run is active, or a previous run crashed "
                          "(check, then delete the lock by hand)") from None
        os.write(fd, datetime.now(timezone.utc).isoformat().encode("ascii"))
        os.close(fd)
        return self

    def __exit__(self, *exc):
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def cmd_update(root: Path, games: list[str], months_back: int, browser: str, pause: float,
               fetcher_factory=None, today: date | None = None) -> int:
    check_constants()
    if pause < MIN_PAUSE_SECONDS:
        raise Refused(f"--pause must be at least {MIN_PAUSE_SECONDS}")
    today = today or date.today()
    for g in games:   # refuse before any browser starts
        if not holdout_opened(root, g) and today >= QUARANTINE_START_DATE:
            a, b = month_window(today, months_back)
            raise Refused(f"{g}: the holdout is not opened; the update window {a}..{b} reaches the quarantine. "
                          "Nothing was requested.")
    with Lock(root):
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


# ---------------------------------------------------------------------------
# Self-test (offline, synthetic data only)
# ---------------------------------------------------------------------------
def self_test() -> int:
    import contextlib
    import tempfile
    results = []

    def check(name, fn):
        try:
            fn(); results.append((name, True))
        except AssertionError as exc:
            results.append((name, False)); print(f"[SELF-TEST] FAIL {name}: {exc}")

    def raises(fn, exc):
        try:
            fn()
        except exc:
            return True
        return False

    def synth(game, n):
        hi = ERAS[game].main_max
        main = []
        for k in range(7):
            x = ((n * 7 + k * 5) % hi) + 1
            while x in main:
                x = x % hi + 1
            main.append(x)
        if game == "POWERBALL":
            sec = [(n % 20) + 1]
        else:
            sec, x = [], (n * 3) % 47 + 1
            while len(sec) < 3:
                if x not in main and x not in sec:
                    sec.append(x)
                x = x % 47 + 1
        return Draw(game, n, derived_date(game, n).isoformat(), tuple(main), tuple(sec))

    class FakeFetcher:
        def __init__(self, mutate=None, quarantine_on_page=False):
            self.mutate, self.q = mutate, quarantine_on_page

        def fetch(self, game, a, b, *, quarantine_closed):
            lines = []
            n = ERAS[game].first_draw
            while derived_date(game, n) <= b:
                d = synth(game, n)
                if self.mutate:
                    d = self.mutate(d)
                if a <= derived_date(game, n) <= b and (not quarantine_closed or n < FIRST_QUARANTINED_DRAW[game] or self.q):
                    day = date.fromisoformat(d.day)
                    lines += [f"Draw {d.number}", f"{day.strftime('%A')} {day.day} {MONTH_NAMES[day.month-1]} {day.year}",
                              "Winning numbers:", *map(str, d.main),
                              "Powerball:" if game == "POWERBALL" else "Supplementary numbers:", *map(str, d.secondary),
                              "View prizes"]
                n += 1
            return parse_gov(game, "\n".join(lines), a, b, quarantine_closed=quarantine_closed)

    def make_root(td, upto=None):
        root = Path(td)
        for game in ERAS:
            last = (upto or {}).get(game, FIRST_QUARANTINED_DRAW[game] - 1)
            draws = [synth(game, n) for n in range(ERAS[game].first_draw, last + 1)]
            st = Store(root, game)
            st.dir.mkdir(parents=True, exist_ok=True)
            h = write_new(st.master, to_csv_bytes(game, draws))
            st.append_ledger({"version": 1, "utc": "t", "action": "INIT", "master_sha256": h,
                              "first_draw": draws[0].number, "last_draw": last, "draw_count": len(draws),
                              "added_count": len(draws), "tool_version": TOOL_VERSION})
        return root

    def t_constants():
        check_constants()
        assert derived_date("POWERBALL", 1576) == date(2026, 7, 30) and derived_date("OZLOTTO", 1693) == date(2026, 7, 28)
        assert header("POWERBALL")[-1] == "Powerball" and header("OZLOTTO")[-3:] == ["Supp_1", "Supp_2", "Supp_3"]

    def t_window():
        assert month_window(date(2027, 3, 15), 5) == (date(2026, 10, 1), date(2027, 3, 15))
        assert month_window(date(2027, 3, 15), 0) == (date(2027, 3, 1), date(2027, 3, 15))
        assert raises(lambda: month_window(date(2027, 3, 15), 61), Refused)
        w = split_windows(date(2022, 1, 1), date(2027, 1, 10))
        assert w[0][0] < date(2022, 1, 1) and w[-1][1] == date(2027, 1, 10)
        assert all(y[0] < x[1] for x, y in zip(w, w[1:]))                  # windows overlap
        for g in ERAS:
            for (a, b) in w:
                assert len([n for n in range(ERAS[g].first_draw, 3000) if a < derived_date(g, n) < b]) < 100

    def t_gate():
        with tempfile.TemporaryDirectory() as td:
            root = make_root(td)
            assert not holdout_opened(root, "POWERBALL")
            # Default window in October 2026 reaches the quarantine -> refused before any fetcher is created.
            made = []
            assert raises(lambda: cmd_update(root, ["POWERBALL"], 5, "chrome", 2.0,
                                             fetcher_factory=lambda: made.append(1) or FakeFetcher(),
                                             today=date(2026, 10, 25)), Refused) and not made
            bad = root / "source_data" / "HOLDOUT_OPENED_POWERBALL.json"
            bad.write_text('{"schema": "HOLDOUT_OPENED_V1", "game": "POWERBALL"}')
            assert raises(lambda: holdout_opened(root, "POWERBALL"), Refused)
            bad.write_text(json.dumps({"schema": "HOLDOUT_OPENED_V1", "game": "POWERBALL", "opened_utc": "x",
                                       "study_manifest_sha256": "a" * 64, "owner_statement": "opened"}))
            assert holdout_opened(root, "POWERBALL")

    def t_quarantine_in_data():
        d = synth("POWERBALL", 1577)
        assert raises(lambda: validate_draw(d, quarantine_closed=True), Stop)
        assert validate_draw(d, quarantine_closed=False) == []
        text = "Draw 1577\nThursday 6 August 2026\nWinning numbers:\nX\n"
        assert raises(lambda: parse_gov("POWERBALL", text, date(2026, 1, 1), date(2026, 12, 31), quarantine_closed=True), Stop)
        with tempfile.TemporaryDirectory() as td:
            root = make_root(td)
            st = Store(root, "POWERBALL")
            draws = from_csv_bytes("POWERBALL", st.master.read_bytes()) + [synth("POWERBALL", 1577)]
            assert raises(lambda: validate_series("POWERBALL", draws, quarantine_closed=True), Stop)

    def t_master_tamper():
        with tempfile.TemporaryDirectory() as td:
            root = make_root(td)
            st = Store(root, "OZLOTTO")
            st.load_verified_master(quarantine_closed=True)
            data = bytearray(st.master.read_bytes()); data[-5] = ord("9") if data[-5] != ord("9") else ord("8")
            st.master.write_bytes(bytes(data))
            assert raises(lambda: st.load_verified_master(quarantine_closed=True), VerifyFail)

    def opened_root(td, upto):
        root = make_root(td, upto)
        for g in ERAS:
            (root / "source_data" / f"HOLDOUT_OPENED_{g}.json").write_text(json.dumps(
                {"schema": "HOLDOUT_OPENED_V1", "game": g, "opened_utc": "x",
                 "study_manifest_sha256": "b" * 64, "owner_statement": "opened"}))
        return root

    def t_update_adds():
        with tempfile.TemporaryDirectory() as td:
            root = opened_root(td, {"POWERBALL": 1590, "OZLOTTO": 1700})
            with contextlib.redirect_stdout(io.StringIO()):
                rc = cmd_update(root, ["POWERBALL", "OZLOTTO"], 5, "chrome", 2.0,
                                fetcher_factory=lambda: FakeFetcher(), today=date(2027, 1, 20))
            assert rc == 0
            for g, start in (("POWERBALL", 1590), ("OZLOTTO", 1700)):
                st = Store(root, g)
                draws, _, last = st.load_verified_master(quarantine_closed=False)
                assert last["action"] == "UPDATE" and int(last["added_first"]) == start + 1
                assert derived_date(g, draws[-1].number) <= date(2027, 1, 20) < derived_date(g, draws[-1].number + 1)
                mine = lambda d: [f for f in d.iterdir() if f.name.startswith(g + "_")]
                assert len(mine(st.backups)) == 1 and len(mine(st.grabs)) == 1
                backup = mine(st.backups)[0]
                assert from_csv_bytes(g, backup.read_bytes())[-1].number == start
                assert sha(backup.read_bytes()) == st.ledger_rows()[-1]["backup_sha256"]
            # second run: NO_CHANGE, master untouched (sleep: file stamps have 1 s resolution)
            time.sleep(1.1)
            before = Store(root, "POWERBALL").master.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()):
                cmd_update(root, ["POWERBALL"], 5, "chrome", 2.0, fetcher_factory=lambda: FakeFetcher(), today=date(2027, 1, 20))
            assert Store(root, "POWERBALL").master.read_bytes() == before
            assert Store(root, "POWERBALL").ledger_rows()[-1]["action"] == "NO_CHANGE"

    def t_update_mismatch_and_gap():
        with tempfile.TemporaryDirectory() as td:
            root = opened_root(td, {"POWERBALL": 1590, "OZLOTTO": 1700})
            st = Store(root, "POWERBALL")
            before = st.master.read_bytes()
            swap = lambda d: Draw(d.game, d.number, d.day, d.main[1:] + d.main[:1], d.secondary) if d.number == 1585 else d
            assert raises(lambda: cmd_update(root, ["POWERBALL"], 5, "chrome", 2.0,
                                             fetcher_factory=lambda: FakeFetcher(swap), today=date(2027, 1, 20)), VerifyFail)
            assert st.master.read_bytes() == before and not st.backups.exists()
            assert len(list(st.grabs.iterdir())) == 1                 # grab kept for inspection
            assert not (root / "source_data" / ".results_master.lock").exists()
            # gap: master ends far earlier than the window
        with tempfile.TemporaryDirectory() as td:
            root = opened_root(td, {"POWERBALL": 1500, "OZLOTTO": 1650})
            assert raises(lambda: cmd_update(root, ["POWERBALL"], 5, "chrome", 2.0,
                                             fetcher_factory=lambda: FakeFetcher(), today=date(2027, 1, 20)), Refused)

    def t_lock_and_create_only():
        with tempfile.TemporaryDirectory() as td:
            root = opened_root(td, {"POWERBALL": 1590, "OZLOTTO": 1700})
            (root / "source_data" / ".results_master.lock").write_text("x")
            assert raises(lambda: cmd_update(root, ["POWERBALL"], 5, "chrome", 2.0,
                                             fetcher_factory=lambda: FakeFetcher(), today=date(2027, 1, 20)), Refused)
            p = Path(td) / "x.csv"
            write_new(p, b"a")
            assert raises(lambda: write_new(p, b"b"), FileExistsError)

    def t_init():
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            build = root / "private_results_checks" / "run_build"; lott = root / "private_results_checks" / "run_lott"
            build.mkdir(parents=True); lott.mkdir(parents=True); (root / "source_data").mkdir()
            out = {}
            for g in ERAS:
                k = ERAS[g].secondary_count
                cols = ["Game", "Draw_Number", "Date"] + [f"Drawn_{i}" for i in range(1, 8)] + \
                       (["Powerball"] if g == "POWERBALL" else ["Supp_1", "Supp_2", "Supp_3"]) + ["Source", "Order_Label"]
                lines = [",".join(cols)]
                for n in range(ERAS[g].first_draw, FIRST_QUARANTINED_DRAW[g]):
                    d = synth(g, n)
                    lines.append(",".join(map(str, [g, n, d.day, *d.main, *d.secondary,
                                                    "LOTTERYWEST_GOV_RESULTS_SEARCH", "SOURCE_SEQUENCE"])))
                data = ("\r\n".join(lines) + "\r\n").encode("ascii")
                (build / f"lotterywest_dev_{g}.csv").write_bytes(data); out[f"lotterywest_dev_{g}.csv"] = sha(data)
                assert k in (1, 3)
            (build / "provenance.json").write_text(json.dumps({"mode": "BUILD_HISTORY_LOTTERYWEST_GOV", "output_sha256": out,
                "summary": {**{g: {"missing": 0, "unexpected": 0, "date_vs_weekly_rule_fail": 0} for g in ERAS},
                            "POWERBALL_vs_old_files": {"fail": 0}}}))
            recon = ("TWO-SITE\r\nPOWERBALL 1500: date PASS, main_order PASS, powerball_order N/A\r\n"
                     "OZLOTTO 1600: date PASS, main_order PASS\r\n").encode("ascii")
            (lott / "reconciliation.txt").write_bytes(recon)
            (lott / "provenance.json").write_text(json.dumps({"mode": "OFFLINE_SAVED_PAGES",
                "output_sha256": {"reconciliation.txt": sha(recon)},
                "inputs": [{"source": "thelott"}, {"against_run": str(build)}],
                "summary": {"POWERBALL": {"all_pass": 52, "expected": 52, "fail": 0},
                            "OZLOTTO": {"all_pass": 31, "expected": 31, "fail": 0}}}))
            hist = ["Draw_Number,Date," + ",".join(f"Ball_{i}" for i in range(1, 8)) + ",Powerball"]
            order = ["Draw_Number,Date," + ",".join(f"Drawn_{i}" for i in range(1, 8)) + ",Powerball,Official_Source_URL"]
            for n in range(1144, 1577):
                d = synth("POWERBALL", n)
                hist.append(f"{n},{d.day}," + ",".join(map(str, sorted(d.main))) + f",{d.secondary[0]}")
                order.append(f"{n},{d.day}," + ",".join(map(str, d.main)) + f",{d.secondary[0]},u")
            hist += [f"{n},POISON" for n in range(1577, 1588)]; order += [f"{n},POISON" for n in range(1577, 1588)]
            (root / OLD_HISTORY).write_text("\n".join(hist) + "\n"); (root / OLD_ORDER).write_text("\n".join(order) + "\n")
            with contextlib.redirect_stdout(io.StringIO()):
                assert cmd_init(root, build, lott, list(ERAS)) == 0
            for g in ERAS:
                st = Store(root, g)
                draws, _, last = st.load_verified_master(quarantine_closed=True)
                assert len(draws) == FIRST_QUARANTINED_DRAW[g] - ERAS[g].first_draw and last["action"] == "INIT"
                assert all(d == synth(g, d.number) for d in draws)
            rec = json.loads(Store(root, "POWERBALL").init_record.read_text())
            assert rec["lott_sample_fields"]["main_order"] == {"PASS": 1} and rec["old_files"]["passed"] == 433
            assert raises(lambda: cmd_init(root, build, lott, list(ERAS)), Refused)       # one-off
            # tampered build csv refused
            (root / "source_data" / "POWERBALL_results_master.csv").unlink()
            (root / "source_data" / "POWERBALL_results_master_ledger.csv").unlink()
            (root / "source_data" / "POWERBALL_results_master_init_verification.json").unlink()
            (build / "lotterywest_dev_POWERBALL.csv").write_bytes(b"x")
            assert raises(lambda: cmd_init(root, build, lott, ["POWERBALL"]), VerifyFail)
            # a quarantined row in the build (hash re-recorded) stops before anything is written
            d = synth("POWERBALL", 1577)
            rows = [",".join(["Game", *header("POWERBALL"), "Source", "Order_Label"])] + [
                ",".join(map(str, ["POWERBALL", x.number, x.day, *x.main, *x.secondary, "LOTTERYWEST_GOV_RESULTS_SEARCH",
                                   "SOURCE_SEQUENCE"])) for x in [synth("POWERBALL", n) for n in range(1144, 1577)] + [d]]
            data = ("\r\n".join(rows) + "\r\n").encode("ascii")
            (build / "lotterywest_dev_POWERBALL.csv").write_bytes(data)
            prov = json.loads((build / "provenance.json").read_text()); prov["output_sha256"]["lotterywest_dev_POWERBALL.csv"] = sha(data)
            (build / "provenance.json").write_text(json.dumps(prov))
            assert raises(lambda: cmd_init(root, build, lott, ["POWERBALL"]), Stop)
            assert not (root / "source_data" / "POWERBALL_results_master.csv").exists()

    for name, fn in [("constants", t_constants), ("windows", t_window), ("holdout gate", t_gate),
                     ("quarantine in data", t_quarantine_in_data), ("master tamper", t_master_tamper),
                     ("update adds draws, backup, ledger, no-change", t_update_adds),
                     ("mismatch and gap", t_update_mismatch_and_gap), ("lock and create-only", t_lock_and_create_only),
                     ("init from verified build", t_init)]:
        check(name, fn)
    ok = sum(r for _, r in results)
    print(f"[SELF-TEST] {ok}/{len(results)} PASS")
    return 0 if ok == len(results) else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=f"Results master files: init and update (v{TOOL_VERSION})")
    p.add_argument("--self-test", action="store_true")
    sub = p.add_subparsers(dest="cmd")
    pi = sub.add_parser("init", help="one-off: create the first masters from the verified history build (offline)")
    pi.add_argument("--build-run", required=True)
    pi.add_argument("--lott-check-run", required=True)
    pi.add_argument("--games", default="POWERBALL,OZLOTTO")
    pu = sub.add_parser("update", help="fetch recent results and update the masters (NOT to be run yet)")
    pu.add_argument("--games", default="POWERBALL,OZLOTTO")
    pu.add_argument("--months-back", type=int, default=DEFAULT_MONTHS_BACK,
                    help=f"previous months to include besides the current one (0..{MAX_MONTHS_BACK})")
    pu.add_argument("--browser", choices=("chrome", "firefox"), default="chrome")
    pu.add_argument("--pause", type=float, default=MIN_PAUSE_SECONDS)
    a = p.parse_args(argv)
    if a.self_test:
        return self_test()
    root = Path(__file__).resolve().parents[1]
    try:
        games = [g.strip().upper() for g in getattr(a, "games", "").split(",") if g.strip()]
        if a.cmd in ("init", "update") and (not games or any(g not in ERAS for g in games)):
            raise Refused("games must be POWERBALL and/or OZLOTTO")
        if a.cmd == "init":
            return cmd_init(root, Path(a.build_run).resolve(), Path(a.lott_check_run).resolve(), games)
        if a.cmd == "update":
            return cmd_update(root, games, a.months_back, a.browser, a.pause)
        p.print_help()
        return 3
    except Refused as exc:
        print(f"[MASTER] REFUSED: {exc}", file=sys.stderr); return 3
    except Stop as exc:
        print(f"[MASTER] STOP: {exc}", file=sys.stderr); return 2
    except VerifyFail as exc:
        print(f"[MASTER] VERIFY FAIL: {exc}", file=sys.stderr); return 1
    except OSError as exc:
        print(f"[MASTER] FILE ERROR: {exc} (is a file open in another program?)", file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
