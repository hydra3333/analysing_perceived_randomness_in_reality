"""MHUP-A slice 2: results_master_v0_1.py -> results_master_v0_2.py (design 4.1, 4.2, 7).

Usage: python3 -I make_updater_v0_2.py <path of results_master_v0_1.py> <output path of results_master_v0_2.py>

The new file is the old one with exactly the design's permitted differences, made as counted text edits so the
diff is reproducible: (1) the two refusals of 4.1 (opened and unsealed game whose ledger is past v_f; session
lock), checked before any fetch, lock or ledger write and re-checked under the updater's lock; (2) the final-host
rule of A6; (3) the first-update admission of 4.1 (D1); (4) a self-test case for each; TOOL_VERSION "0.1" -> "0.2";
the module docstring; and the self-test fixture edits the additions need (opened_root and t_gate gain the two
freeze fields; t_update_adds runs its second update with a MODE_H_SEALED marker present). The fetch, parse,
overlap, numbering, date, chain and transaction logic is untouched.
"""
import sys
from pathlib import Path

EDITS = []


def edit(old, new, count=1):
    EDITS.append((old, new, count))


# ---------------------------------------------------------------- docstring and version
edit('"""Results master files: initialise and update. v0.1.\n',
     '"""Results master files: initialise and update. v0.2.\n')
edit('    python src\\\\results_master_v0_1.py --self-test\n'
     '    python src\\\\results_master_v0_1.py init --build-run <history build run> --lott-check-run <Lott cross-check run>\n'
     '    python src\\\\results_master_v0_1.py update [--games POWERBALL,OZLOTTO] [--months-back 5] [--browser chrome]\n',
     '    python src\\\\results_master_v0_2.py --self-test\n'
     '    python src\\\\results_master_v0_2.py init --build-run <history build run> --lott-check-run <Lott cross-check run>\n'
     '    python src\\\\results_master_v0_2.py update [--games POWERBALL,OZLOTTO] [--months-back 5] [--browser chrome]\n')
edit('automation only: headless real browser, default settings, >= 2 s between page\n'
     'loads, a block/challenge page means STOP.\n',
     'automation only: headless real browser, default settings, >= 2 s between page\n'
     'loads, a block/challenge page means STOP. The browser\'s final URL must be on\n'
     'scheme https and host exactly www.lotterywest.wa.gov.au (MHUP-A design A6):\n'
     'a redirect anywhere else is refused after the browser followed it, and there\n'
     'is no fallback source of any kind.\n'
     '\n'
     'v0.2 (MHUP-A, design 4.1 and 7): four additions and nothing else of substance.\n'
     '(1) Two refusals before any fetch, lock or ledger write, re-checked under the\n'
     'updater\'s own lock: a game whose opening record exists and whose MODE_H_SEALED\n'
     'marker does not is refused unless the ledger\'s last row is the freeze version\n'
     'v_f exactly (version and master SHA-256 as the opening record states them),\n'
     'and a game whose weekly session lock (ACTIVE_SESSION.lock) exists is refused.\n'
     'Both read value-free owner records and markers only; a NO_CHANGE run is refused\n'
     'in that window like any other. (2) The final-host rule above. (3) The first\n'
     'update of an opened, unsealed game writes only if it is an UPDATE after which\n'
     'the master\'s last draw is at least the game\'s last holdout draw\n'
     '(FIRST_QUARANTINED_DRAW + 9); otherwise it STOPs with the grab kept and the\n'
     'master and ledger byte-identical, and the same first update may be retried\n'
     '(usually with a wider --months-back). (4) A self-test case for each.\n')
edit('TOOL_VERSION = "0.1"\n', 'TOOL_VERSION = "0.2"\n')

# ---------------------------------------------------------------- constants for the additions
edit('FIRST_QUARANTINED_DRAW = MappingProxyType({"POWERBALL": 1577, "OZLOTTO": 1694})\n',
     'FIRST_QUARANTINED_DRAW = MappingProxyType({"POWERBALL": 1577, "OZLOTTO": 1694})\n'
     'HOLDOUT_DRAWS = 10                 # the ten holdout draws; holdout_last = FIRST_QUARANTINED_DRAW + 9\n'
     'RESULTS_HOST = "www.lotterywest.wa.gov.au"   # the one origin (A6); scheme https; no fallback\n'
     'SEAL_SCHEMA = "MODE_H_SEALED_V1"\n'
     'BATCH_ID_SCHEMA = "MODE_H_BATCH_ID_V1"\n'
     'ADVANCE_SCHEMA = "STUDY_VERSION_ADVANCE_V1"\n')

# ---------------------------------------------------------------- the opening record gains the freeze fields
edit('    if (rec.get("schema") != "HOLDOUT_OPENED_V1" or rec.get("game") != game or\n'
     '            not re.fullmatch(r"[0-9a-f]{64}", str(rec.get("study_manifest_sha256", ""))) or\n'
     '            not rec.get("opened_utc") or not rec.get("owner_statement")):\n'
     '        raise Refused(f"{p.name} is incomplete; the holdout is NOT treated as opened")\n'
     '    return True\n',
     '    if (rec.get("schema") != "HOLDOUT_OPENED_V1" or rec.get("game") != game or\n'
     '            not re.fullmatch(r"[0-9a-f]{64}", str(rec.get("study_manifest_sha256", ""))) or\n'
     '            not rec.get("opened_utc") or not rec.get("owner_statement")):\n'
     '        raise Refused(f"{p.name} is incomplete; the holdout is NOT treated as opened")\n'
     '    if (type(rec.get("freeze_version")) is not int or rec["freeze_version"] < 1 or\n'
     '            not re.fullmatch(r"[0-9a-f]{64}", str(rec.get("freeze_master_sha256", "")))):\n'
     '        raise Refused(f"{p.name} lacks the freeze fields (freeze_version, freeze_master_sha256); "\n'
     '                      "the holdout is NOT treated as opened")\n'
     '    return True\n'
     '\n'
     '\n'
     'def holdout_last(game: str) -> int:\n'
     '    return FIRST_QUARANTINED_DRAW[game] + HOLDOUT_DRAWS - 1\n'
     '\n'
     '\n'
     'def _owner_json(p: Path, what: str) -> dict:\n'
     '    """A value-free owner record or marker: a regular file holding one JSON object, or a refusal."""\n'
     '    if p.is_symlink() or not p.is_file():\n'
     '        raise Refused(f"{what} ({p.name}) is not a regular file")\n'
     '    try:\n'
     '        rec = json.loads(p.read_text(encoding="utf-8"))\n'
     '    except (ValueError, OSError):\n'
     '        raise Refused(f"{what} ({p.name}) is not valid JSON") from None\n'
     '    if not isinstance(rec, dict):\n'
     '        raise Refused(f"{what} ({p.name}) is not a JSON object")\n'
     '    return rec\n'
     '\n'
     '\n'
     'def mode_h_sealed(root: Path, game: str) -> bool:\n'
     '    """True only if the game\'s batch-id record names a batch whose MODE_H_SEALED marker exists and is well formed.\n'
     '    Neither file holds a draw outcome. No batch-id record means not sealed."""\n'
     '    rec_path = root / "results" / "real" / "holdout" / game / "MODE_H_BATCH_ID.json"\n'
     '    if not rec_path.exists():\n'
     '        return False\n'
     '    rec = _owner_json(rec_path, "batch-id record")\n'
     '    bid = rec.get("batch_id")\n'
     '    if (rec.get("schema") != BATCH_ID_SCHEMA or rec.get("game_id") != game or\n'
     '            not isinstance(bid, str) or not re.fullmatch(r"wf-[0-9a-f]{32}", bid)):\n'
     '        raise Refused(f"{rec_path.name} is not a valid batch-id record for {game}")\n'
     '    seal = root / "results" / "real" / "holdout" / "wf_batches" / game / bid / "MODE_H_SEALED.json"\n'
     '    if not seal.exists():\n'
     '        return False\n'
     '    mk = _owner_json(seal, "MODE_H_SEALED marker")\n'
     '    if mk.get("schema") != SEAL_SCHEMA or mk.get("batch_id") != bid:\n'
     '        raise Refused(f"{seal.name} for {game} is not a valid MODE_H_SEALED marker")\n'
     '    return True\n'
     '\n'
     '\n'
     'def study_version_advance(root: Path, game: str) -> dict | None:\n'
     '    """The study version advance record (design 4.1), if any: the rows it names beyond v_a, and v_a\'."""\n'
     '    p = root / "results" / "real" / "holdout" / game / f"STUDY_VERSION_ADVANCE_{game}_V1.json"\n'
     '    if not p.exists():\n'
     '        return None\n'
     '    rec = _owner_json(p, "study version advance")\n'
     '    rows = rec.get("rows_beyond_admitted")\n'
     '    if (rec.get("schema") != ADVANCE_SCHEMA or rec.get("game_id") != game or not isinstance(rows, list) or not rows or\n'
     '            any(not isinstance(r, dict) or type(r.get("version")) is not int or r.get("action") not in ("UPDATE", "NO_CHANGE")\n'
     '                or not re.fullmatch(r"[0-9a-f]{64}", str(r.get("master_sha256", ""))) for r in rows) or\n'
     '            rec.get("admitted_version_after") != rows[-1]["version"]):\n'
     '        raise Refused(f"{p.name} is not a valid study version advance for {game}")\n'
     '    return rec\n'
     '\n'
     '\n'
     'def session_lock_present(root: Path, game: str) -> bool:\n'
     '    """Refusal (2) of design 4.1: the weekly session lock of 6.1, whatever its content."""\n'
     '    return (root / "results" / "real" / "weekly" / game / "ACTIVE_SESSION.lock").exists()\n'
     '\n'
     '\n'
     'def freeze_state(root: Path, game: str, rows: list[dict]) -> str:\n'
     '    """Refusal (1) of design 4.1 and the window of the first-update admission (3).\n'
     '    Returns CLOSED (holdout not opened: the quarantine rules apply), SEALED (opened and MODE_H_SEALED exists:\n'
     '    ordinary updates) or FIRST_UPDATE (opened, unsealed, and the ledger\'s last row is v_f exactly, by version\n'
     '    and master SHA-256 as the opening record states them). Opened, unsealed and anything else refuses; a\n'
     '    study version advance is read so an inconsistent one refuses and the message names v_a\', but it never\n'
     '    reopens the window: no row may be appended until the seal."""\n'
     '    if not holdout_opened(root, game):\n'
     '        return "CLOSED"\n'
     '    if mode_h_sealed(root, game):\n'
     '        return "SEALED"\n'
     '    rec = json.loads((root / "source_data" / f"HOLDOUT_OPENED_{game}.json").read_text(encoding="utf-8"))\n'
     '    v_f, h_f = rec["freeze_version"], rec["freeze_master_sha256"]\n'
     '    if not rows:\n'
     '        raise Refused(f"{game}: the holdout is opened but the ledger is missing or empty")\n'
     '    last = rows[-1]\n'
     '    if int(last["version"]) == v_f and last["master_sha256"] == h_f:\n'
     '        return "FIRST_UPDATE"\n'
     '    admitted = v_f + 1\n'
     '    adv = study_version_advance(root, game)\n'
     '    if adv is not None:\n'
     '        beyond = [(int(r["version"]), r["action"], r["master_sha256"]) for r in rows if int(r["version"]) > admitted]\n'
     '        named = [(r["version"], r["action"], r["master_sha256"]) for r in adv["rows_beyond_admitted"]]\n'
     '        if named != beyond:\n'
     '            raise Refused(f"{game}: the study version advance does not name exactly the ledger rows beyond "\n'
     '                          f"version {admitted}; nothing was requested")\n'
     '        admitted = adv["admitted_version_after"]\n'
     '    raise Refused(f"{game}: the holdout is opened and the Mode H study is not sealed; the ledger\'s last row is "\n'
     '                  f"version {last[\'version\']} (freeze version {v_f}, admitted version {admitted}); no update, "\n'
     '                  f"NO_CHANGE included, is permitted until MODE_H_SEALED exists. Nothing was requested.")\n')

# ---------------------------------------------------------------- the final-host rule (A6)
edit('class BrowserFetcher:\n',
     'def check_final_url(url: str) -> None:\n'
     '    """A6: after the browser followed every redirect, the final URL must be https on exactly RESULTS_HOST.\n'
     '    A browser exposes no status code, so this is the check a browser allows. There is no fallback."""\n'
     '    from urllib.parse import urlsplit\n'
     '    parts = urlsplit(url or "")\n'
     '    host = (parts.hostname or "")\n'
     '    if parts.scheme != "https" or host != RESULTS_HOST:\n'
     '        raise Refused(f"the browser\'s final URL is {parts.scheme or \'(no scheme)\'}://{host or \'(no host)\'}; only "\n'
     '                      f"https://{RESULTS_HOST} is accepted and there is no fallback source. Nothing was parsed or written.")\n'
     '\n'
     '\n'
     'class BrowserFetcher:\n')
edit('            raise Stop("www.lotterywest.wa.gov.au served a block/challenge page; nothing was bypassed")\n'
     '        inner, n = [], ERAS[game].first_draw\n',
     '            raise Stop("www.lotterywest.wa.gov.au served a block/challenge page; nothing was bypassed")\n'
     '        check_final_url(self.driver.current_url)\n'
     '        inner, n = [], ERAS[game].first_draw\n')

# ---------------------------------------------------------------- update_game: re-checks under the lock, admission (3)
edit('    master, master_bytes, last = st.load_verified_master(quarantine_closed=closed)\n'
     '    got: dict[int, Draw] = {}\n',
     '    master, master_bytes, last = st.load_verified_master(quarantine_closed=closed)\n'
     '    state = freeze_state(root, game, st.ledger_rows())        # refusal (1) re-checked under the updater\'s lock\n'
     '    if session_lock_present(root, game):                       # refusal (2) re-checked under the updater\'s lock\n'
     '        raise Refused(f"{game}: ACTIVE_SESSION.lock exists (a weekly session is active); nothing was requested")\n'
     '    got: dict[int, Draw] = {}\n')
edit('    warns = [w for d in new for w in validate_draw(d, quarantine_closed=closed)]\n'
     '    version = int(last["version"]) + 1\n',
     '    warns = [w for d in new for w in validate_draw(d, quarantine_closed=closed)]\n'
     '    if state == "FIRST_UPDATE" and (not new or new[-1].number < holdout_last(game)):\n'
     '        raise Stop(f"{game}: the first update after opening the holdout must bring the master to draw "\n'
     '                   f"{holdout_last(game)} at least (it would end at {(new or master)[-1].number}); nothing written "\n'
     '                   f"but the grab, kept as {grab_path.name}; the master and ledger stay at version {last[\'version\']}. "\n'
     '                   f"Rerun the same update with a wider --months-back.")\n'
     '    version = int(last["version"]) + 1\n')

# ---------------------------------------------------------------- cmd_update: the refusals before any lock or fetch
edit('    for g in games:   # refuse before any browser starts\n'
     '        if not holdout_opened(root, g) and today >= QUARANTINE_START_DATE:\n'
     '            a, b = month_window(today, months_back)\n'
     '            raise Refused(f"{g}: the holdout is not opened; the update window {a}..{b} reaches the quarantine. "\n'
     '                          "Nothing was requested.")\n'
     '    with Lock(root):\n',
     '    for g in games:   # refuse before any browser starts\n'
     '        if not holdout_opened(root, g) and today >= QUARANTINE_START_DATE:\n'
     '            a, b = month_window(today, months_back)\n'
     '            raise Refused(f"{g}: the holdout is not opened; the update window {a}..{b} reaches the quarantine. "\n'
     '                          "Nothing was requested.")\n'
     '        if session_lock_present(root, g):                      # refusal (2), before any lock or fetch\n'
     '            raise Refused(f"{g}: ACTIVE_SESSION.lock exists (a weekly session is active); nothing was requested")\n'
     '        freeze_state(root, g, Store(root, g).ledger_rows())    # refusal (1), before any lock or fetch\n'
     '    with Lock(root):\n')

# ---------------------------------------------------------------- self-test fixtures
edit('            bad.write_text(json.dumps({"schema": "HOLDOUT_OPENED_V1", "game": "POWERBALL", "opened_utc": "x",\n'
     '                                       "study_manifest_sha256": "a" * 64, "owner_statement": "opened"}))\n'
     '            assert holdout_opened(root, "POWERBALL")\n',
     '            bad.write_text(json.dumps({"schema": "HOLDOUT_OPENED_V1", "game": "POWERBALL", "opened_utc": "x",\n'
     '                                       "study_manifest_sha256": "a" * 64, "owner_statement": "opened"}))\n'
     '            assert raises(lambda: holdout_opened(root, "POWERBALL"), Refused)      # v0.2: freeze fields required\n'
     '            bad.write_text(json.dumps({"schema": "HOLDOUT_OPENED_V1", "game": "POWERBALL", "opened_utc": "x",\n'
     '                                       "study_manifest_sha256": "a" * 64, "owner_statement": "opened",\n'
     '                                       "freeze_version": 1, "freeze_master_sha256": "c" * 64}))\n'
     '            assert holdout_opened(root, "POWERBALL")\n')
edit('    def opened_root(td, upto):\n'
     '        root = make_root(td, upto)\n'
     '        for g in ERAS:\n'
     '            (root / "source_data" / f"HOLDOUT_OPENED_{g}.json").write_text(json.dumps(\n'
     '                {"schema": "HOLDOUT_OPENED_V1", "game": g, "opened_utc": "x",\n'
     '                 "study_manifest_sha256": "b" * 64, "owner_statement": "opened"}))\n'
     '        return root\n',
     '    def opened_root(td, upto):\n'
     '        root = make_root(td, upto)\n'
     '        for g in ERAS:\n'
     '            last = Store(root, g).ledger_rows()[-1]\n'
     '            (root / "source_data" / f"HOLDOUT_OPENED_{g}.json").write_text(json.dumps(\n'
     '                {"schema": "HOLDOUT_OPENED_V1", "game": g, "opened_utc": "x",\n'
     '                 "study_manifest_sha256": "b" * 64, "owner_statement": "opened",\n'
     '                 "freeze_version": int(last["version"]), "freeze_master_sha256": last["master_sha256"]}))\n'
     '        return root\n'
     '\n'
     '    def seal(root, g, bid="wf-" + "0" * 32):\n'
     '        """Plant a value-free batch-id record and MODE_H_SEALED marker, as Method_Mode_H leaves them."""\n'
     '        hold = root / "results" / "real" / "holdout"\n'
     '        (hold / g).mkdir(parents=True, exist_ok=True)\n'
     '        (hold / g / "MODE_H_BATCH_ID.json").write_text(json.dumps({"schema": BATCH_ID_SCHEMA, "game_id": g, "batch_id": bid}))\n'
     '        (hold / "wf_batches" / g / bid).mkdir(parents=True, exist_ok=True)\n'
     '        (hold / "wf_batches" / g / bid / "MODE_H_SEALED.json").write_text(json.dumps({"schema": SEAL_SCHEMA, "batch_id": bid}))\n')
edit('            # second run: NO_CHANGE, master untouched (sleep: file stamps have 1 s resolution)\n'
     '            time.sleep(1.1)\n',
     '            # second run: NO_CHANGE, master untouched (sleep: file stamps have 1 s resolution); v0.2: a second\n'
     '            # update of an opened game needs the MODE_H_SEALED marker (refusal (1)), so it is planted first\n'
     '            seal(root, "POWERBALL")\n'
     '            time.sleep(1.1)\n')

# ---------------------------------------------------------------- the four new self-test cases
edit('    def t_init():\n',
     '    def t_refusal_unsealed_window():\n'
     '        # refusal (1): opened, unsealed, ledger past v_f -> refused before any fetcher is made; NO_CHANGE included\n'
     '        with tempfile.TemporaryDirectory() as td:\n'
     '            root = opened_root(td, {"POWERBALL": 1590, "OZLOTTO": 1700})\n'
     '            with contextlib.redirect_stdout(io.StringIO()):\n'
     '                assert cmd_update(root, ["POWERBALL"], 5, "chrome", 2.0, fetcher_factory=lambda: FakeFetcher(),\n'
     '                                  today=date(2027, 1, 20)) == 0                      # the one permitted first update\n'
     '            st = Store(root, "POWERBALL")\n'
     '            rows = st.ledger_rows(); before = st.master.read_bytes()\n'
     '            assert int(rows[-1]["version"]) == 2\n'
     '            made = []\n'
     '            assert raises(lambda: cmd_update(root, ["POWERBALL"], 5, "chrome", 2.0,\n'
     '                                             fetcher_factory=lambda: made.append(1) or FakeFetcher(),\n'
     '                                             today=date(2027, 1, 20)), Refused) and not made\n'
     '            assert st.ledger_rows() == rows and st.master.read_bytes() == before\n'
     '            assert not (root / "source_data" / ".results_master.lock").exists()\n'
     '            assert raises(lambda: freeze_state(root, "POWERBALL", rows), Refused)\n'
     '            # a study version advance naming exactly the rows beyond v_a keeps the refusal (window unsealed)\n'
     '            seal(root, "POWERBALL")\n'
     '            time.sleep(1.1)                                   # grab file names carry a 1 s stamp\n'
     '            with contextlib.redirect_stdout(io.StringIO()):\n'
     '                assert cmd_update(root, ["POWERBALL"], 5, "chrome", 2.0, fetcher_factory=lambda: FakeFetcher(),\n'
     '                                  today=date(2027, 1, 20)) == 0                      # sealed: ordinary update\n'
     '            assert freeze_state(root, "POWERBALL", st.ledger_rows()) == "SEALED"\n'
     '            (root / "results" / "real" / "holdout" / "wf_batches" / "POWERBALL" / ("wf-" + "0" * 32) / "MODE_H_SEALED.json").unlink()\n'
     '            rows = st.ledger_rows()\n'
     '            assert int(rows[-1]["version"]) == 3\n'
     '            adv = root / "results" / "real" / "holdout" / "POWERBALL" / "STUDY_VERSION_ADVANCE_POWERBALL_V1.json"\n'
     '            adv.write_text(json.dumps({"schema": ADVANCE_SCHEMA, "game_id": "POWERBALL", "admitted_version_after": 3,\n'
     '                                       "rows_beyond_admitted": [{"version": 3, "action": rows[-1]["action"],\n'
     '                                                                 "master_sha256": rows[-1]["master_sha256"]}]}))\n'
     '            assert raises(lambda: freeze_state(root, "POWERBALL", rows), Refused)\n'
     '            adv.write_text(json.dumps({"schema": ADVANCE_SCHEMA, "game_id": "POWERBALL", "admitted_version_after": 3,\n'
     '                                       "rows_beyond_admitted": [{"version": 3, "action": "UPDATE", "master_sha256": "d" * 64}]}))\n'
     '            assert raises(lambda: freeze_state(root, "POWERBALL", rows), Refused)   # inconsistent advance refuses too\n'
     '            # the other game is untouched by all of this: still in its first-update window\n'
     '            assert freeze_state(root, "OZLOTTO", Store(root, "OZLOTTO").ledger_rows()) == "FIRST_UPDATE"\n'
     '            # a malformed seal marker or batch-id record refuses rather than counting as sealed\n'
     '            seal(root, "OZLOTTO")\n'
     '            (root / "results" / "real" / "holdout" / "wf_batches" / "OZLOTTO" / ("wf-" + "0" * 32) / "MODE_H_SEALED.json").write_text("{}")\n'
     '            assert raises(lambda: mode_h_sealed(root, "OZLOTTO"), Refused)\n'
     '            # a closed game (no opening record) is CLOSED, as v0.1 treated it\n'
     '            (root / "source_data" / "HOLDOUT_OPENED_OZLOTTO.json").unlink()\n'
     '            assert freeze_state(root, "OZLOTTO", Store(root, "OZLOTTO").ledger_rows()) == "CLOSED"\n'
     '\n'
     '    def t_refusal_session_lock():\n'
     '        # refusal (2): the weekly session lock refuses before any fetcher is made, and again under the lock\n'
     '        with tempfile.TemporaryDirectory() as td:\n'
     '            root = opened_root(td, {"POWERBALL": 1590, "OZLOTTO": 1700})\n'
     '            lock = root / "results" / "real" / "weekly" / "POWERBALL" / "ACTIVE_SESSION.lock"\n'
     '            lock.parent.mkdir(parents=True); lock.write_text("anything")\n'
     '            made = []\n'
     '            assert raises(lambda: cmd_update(root, ["POWERBALL"], 5, "chrome", 2.0,\n'
     '                                             fetcher_factory=lambda: made.append(1) or FakeFetcher(),\n'
     '                                             today=date(2027, 1, 20)), Refused) and not made\n'
     '            assert not (root / "source_data" / ".results_master.lock").exists()\n'
     '            assert Store(root, "POWERBALL").ledger_rows()[-1]["version"] == "1"\n'
     '            assert raises(lambda: update_game(root, "POWERBALL", FakeFetcher(), 5, date(2027, 1, 20)), Refused)\n'
     '            lock.unlink()\n'
     '            with contextlib.redirect_stdout(io.StringIO()):\n'
     '                assert cmd_update(root, ["POWERBALL"], 5, "chrome", 2.0, fetcher_factory=lambda: FakeFetcher(),\n'
     '                                  today=date(2027, 1, 20)) == 0\n'
     '\n'
     '    def t_first_update_admission():\n'
     '        # admission (3): the first update writes only as an UPDATE reaching holdout_last; otherwise STOP, grab kept\n'
     '        assert holdout_last("POWERBALL") == 1586 and holdout_last("OZLOTTO") == 1703\n'
     '        with tempfile.TemporaryDirectory() as td:\n'
     '            root = opened_root(td, {"POWERBALL": 1580, "OZLOTTO": 1700})\n'
     '            st = Store(root, "POWERBALL")\n'
     '            before, rows = st.master.read_bytes(), st.ledger_rows()\n'
     '            # a window ending at draw 1584 (this month and one back: 1577..1584 fetched, 1581..1584 new):\n'
     '            # an UPDATE that stops short of 1586 -> STOP\n'
     '            short = derived_date("POWERBALL", 1584)\n'
     '            assert raises(lambda: cmd_update(root, ["POWERBALL"], 1, "chrome", 2.0, fetcher_factory=lambda: FakeFetcher(),\n'
     '                                             today=short), Stop)\n'
     '            assert st.master.read_bytes() == before and st.ledger_rows() == rows and not st.backups.exists()\n'
     '            assert len(list(st.grabs.iterdir())) == 1\n'
     '            assert not (root / "source_data" / ".results_master.lock").exists()\n'
     '            time.sleep(1.1)\n'
     '            # a NO_CHANGE result in the window -> STOP, no row appended\n'
     '            assert raises(lambda: cmd_update(root, ["POWERBALL"], 1, "chrome", 2.0, fetcher_factory=lambda: FakeFetcher(),\n'
     '                                             today=derived_date("POWERBALL", 1580)), Stop)\n'
     '            assert st.master.read_bytes() == before and st.ledger_rows() == rows and len(list(st.grabs.iterdir())) == 2\n'
     '            time.sleep(1.1)\n'
     '            # the retry with a wider window succeeds and reaches 1586 or beyond\n'
     '            with contextlib.redirect_stdout(io.StringIO()):\n'
     '                assert cmd_update(root, ["POWERBALL"], 5, "chrome", 2.0, fetcher_factory=lambda: FakeFetcher(),\n'
     '                                  today=derived_date("POWERBALL", 1586)) == 0\n'
     '            draws, _, last = st.load_verified_master(quarantine_closed=False)\n'
     '            assert last["action"] == "UPDATE" and draws[-1].number >= 1586 and int(last["version"]) == 2\n'
     '            # Oz Lotto, untouched, is still in its window; its first update to 2027 reaches 1703\n'
     '            with contextlib.redirect_stdout(io.StringIO()):\n'
     '                assert cmd_update(root, ["OZLOTTO"], 5, "chrome", 2.0, fetcher_factory=lambda: FakeFetcher(),\n'
     '                                  today=date(2027, 1, 20)) == 0\n'
     '            assert Store(root, "OZLOTTO").load_verified_master(quarantine_closed=False)[0][-1].number >= 1703\n'
     '\n'
     '    def t_final_host():\n'
     '        # A6: only https on exactly www.lotterywest.wa.gov.au passes; anything else is refused, naming the host\n'
     '        check_final_url("https://www.lotterywest.wa.gov.au/results/powerball?fromDate=x")\n'
     '        check_final_url("HTTPS://WWW.LOTTERYWEST.WA.GOV.AU/results")                  # scheme and host are case-insensitive\n'
     '        for bad in ("http://www.lotterywest.wa.gov.au/results", "https://oz.lotterywest.com/results",\n'
     '                    "https://lotterywest.wa.gov.au/results", "https://www.lotterywest.wa.gov.au.example.net/x",\n'
     '                    "https://www.thelott.com/powerball/results", "https://user@evil.example/www.lotterywest.wa.gov.au",\n'
     '                    "", "about:blank", "data:text/html,x"):\n'
     '            assert raises(lambda: check_final_url(bad), Refused), bad\n'
     '        try:\n'
     '            check_final_url("https://oz.lotterywest.com/results")\n'
     '        except Refused as exc:\n'
     '            assert "oz.lotterywest.com" in str(exc) and "no fallback" in str(exc)\n'
     '        for g in ERAS:\n'
     '            check_final_url(gov_url(g, date(2026, 1, 1), date(2026, 1, 31)))\n'
     '\n'
     '    def t_init():\n')
edit('                     ("mismatch and gap", t_update_mismatch_and_gap), ("lock and create-only", t_lock_and_create_only),\n'
     '                     ("init from verified build", t_init)]:\n',
     '                     ("mismatch and gap", t_update_mismatch_and_gap), ("lock and create-only", t_lock_and_create_only),\n'
     '                     ("refusal: opened and unsealed window", t_refusal_unsealed_window),\n'
     '                     ("refusal: weekly session lock", t_refusal_session_lock),\n'
     '                     ("first-update admission", t_first_update_admission), ("final host", t_final_host),\n'
     '                     ("init from verified build", t_init)]:\n')


def main(src: Path, dst: Path) -> None:
    text = src.read_text(encoding='ascii')
    assert '\r' not in text
    for old, new, count in EDITS:
        n = text.count(old)
        if n != count:
            raise SystemExit(f'edit anchor found {n} time(s), expected {count}:\n{old[:200]}')
        text = text.replace(old, new)
    dst.write_text(text, encoding='ascii', newline='\n')
    print(f'{dst}: {len(EDITS)} edits applied')


if __name__ == '__main__':
    main(Path(sys.argv[1]), Path(sys.argv[2]))
