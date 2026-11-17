"""MHUP-B slice 1: counted edits to the installed modules (code plan v0.3 sections 3, 5 L1 to L3; design v0.1r7 3.4, 6).

Applies to a dev TREE (a copy of main; src/ and tests/ unchanged since cc0ab73). Every old string must occur exactly
once; the script stops otherwise. The new modules are copied separately (build_dev_slice1.sh).
Usage: python3 -I apply_slice1.py TREE
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()


def edit(rel, pairs):
    p = tree / rel
    raw = p.read_bytes()
    crlf = b'\r\n' in raw
    s = raw.decode('ascii').replace('\r\n', '\n')
    for a, b in pairs:
        assert s.count(a) == 1, (rel, s.count(a), a[:80])
        s = s.replace(a, b)
    s.encode('ascii')
    p.write_bytes(s.replace('\n', '\r\n').encode('ascii') if crlf else s.encode('ascii'))
    print('edited', rel, len(pairs))


# ---------------------------------------------------------------- L1: contract_vocab.py (E2R-R41, R44 amended; design 6.4)
edit('src/methods/_common/contract_vocab.py', [
    ("RUN_MODES = frozenset(('REAL_DEVELOPMENT', 'REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'IN_SAMPLE_DIAGNOSTIC',\n",
     "RUN_MODES = frozenset(('REAL_DEVELOPMENT', 'REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'CATCH_UP', 'IN_SAMPLE_DIAGNOSTIC',\n"),
    ("RESERVED_MODES = frozenset(('FINAL_NEXT_DRAW', 'IN_SAMPLE_DIAGNOSTIC'))\n"
     "REAL_MODES = frozenset(('REAL_DEVELOPMENT', 'REAL_HOLDOUT', 'FINAL_NEXT_DRAW'))   # every mode that reads a real master\n",
     "# FINAL_NEXT_DRAW was unreserved by MHUP-B (design v0.1r7 section 6.4), and CATCH_UP added as a run mode with its own\n"
     "# evidence tier: both open only for a ticketed request bound to a weekly session, above the holdout, with the game's\n"
     "# developed record (the dispatch gate decides), and under the mode-to-pin rule (the runner, after the reader).\n"
     "RESERVED_MODES = frozenset(('IN_SAMPLE_DIAGNOSTIC',))\n"
     "REAL_MODES = frozenset(('REAL_DEVELOPMENT', 'REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'CATCH_UP'))   # every mode that reads a real master\n"
     "WEEKLY_MODES = frozenset(('FINAL_NEXT_DRAW', 'CATCH_UP'))                 # session-bound, above the holdout only\n"),
    ("EVIDENCE_TIERS = frozenset(('DEVELOPMENT_WF_EXPLORATORY', 'HOLDOUT_MODE_H', 'PROSPECTIVE',\n",
     "EVIDENCE_TIERS = frozenset(('DEVELOPMENT_WF_EXPLORATORY', 'HOLDOUT_MODE_H', 'PROSPECTIVE', 'CATCH_UP',\n"),
    ("        if run_mode == 'REAL_HOLDOUT':\n            return 'WF_FORECAST', 'HOLDOUT_MODE_H'           # E2R-R41's row, unreserved as written (MHUP-R)\n",
     "        if run_mode == 'REAL_HOLDOUT':\n            return 'WF_FORECAST', 'HOLDOUT_MODE_H'           # E2R-R41's row, unreserved as written (MHUP-R)\n"
     "        if run_mode == 'FINAL_NEXT_DRAW':\n            return 'WF_FORECAST', 'PROSPECTIVE'              # E2R-R41's row, unreserved as written (MHUP-B)\n"
     "        if run_mode == 'CATCH_UP':\n            return 'WF_FORECAST', 'CATCH_UP'                 # the new row (design 6.4; E2R-R41 amended)\n"),
])

# ---------------------------------------------------------------- L1: the forecast header's target rule for the weekly modes
edit('src/methods/_common/contract_forecast.py', [
    ("    elif mode in V.REAL_MODES:\n        if target <= p.first_draw:\n",
     "    elif mode in V.WEEKLY_MODES:\n        if target <= p.holdout_last:\n"
     "            raise ValueError(f'{where}: a {mode} record must name a draw after the holdout')\n"
     "    elif mode in V.REAL_MODES:\n        if target <= p.first_draw:\n"),
])

# ---------------------------------------------------------------- L1: the task's data kind (the special case folded in)
edit('src/methods/_common/contract_task.py', [
    ("    return REAL_VIEW_DATA_KIND if run_mode in V.REAL_MODES or run_mode == 'CATCH_UP' else run_mode\n",
     "    return REAL_VIEW_DATA_KIND if run_mode in V.REAL_MODES else run_mode\n"),
])

# ---------------------------------------------------------------- L1: the runner: the mode-to-pin rule (design 3.4(a); CF-2)
edit('src/methods/_common/contract_runner.py', [
    ("        if r.get('run_mode') in V.REAL_MODES or r.get('run_mode') == 'CATCH_UP':\n",
     "        if r.get('run_mode') in V.REAL_MODES:\n"),
    ("def _numeric(exc: BaseException) -> bool:\n",
     "def _check_mode_pin(repo_root: Path, request: Mapping) -> None:\n"
     "    \"\"\"Design 3.4(a), the pin-dependent half of the mode rules, checked where the pin is read (MHUP-B; code plan CF-2):\n"
     "    FINAL_NEXT_DRAW only for target = last_draw(v) + 1 of the pinned version v, so a FINAL_NEXT_DRAW record can never\n"
     "    exist for a draw whose result the pinned master already holds; CATCH_UP, a session-bound REAL_DEVELOPMENT run and\n"
     "    the owner's diagnostic route only for targets at or below last_draw(v). Read after the reader has verified the\n"
     "    chain and the pin; no draw is decoded here.\"\"\"\n"
     "    mode, kind = request['run_mode'], binding_kind(request)\n"
     "    if mode not in V.WEEKLY_MODES and kind not in ('WEEKLY_SESSION', 'OWNER_DIAGNOSTIC'):\n"
     "        return\n"
     "    from _common import master_versions as MV\n"
     "    _raw, rows, _evidence = MV.load_verified_source(Path(repo_root), request['game_id'])\n"
     "    last = MV.resolve_pin(rows, request['ledger_version'], request['master_sha256']).last_draw\n"
     "    target = request['target_draw_number']\n"
     "    if mode == 'FINAL_NEXT_DRAW':\n"
     "        if target != last + 1:\n"
     "            raise ValueError(f'MODE_PIN: FINAL_NEXT_DRAW names only the draw after the pinned master\\'s last draw '\n"
     "                             f'({last + 1}), not {target}')\n"
     "    elif target > last:\n"
     "        raise ValueError(f'MODE_PIN: a {mode} run with this binding names only draws the pinned master holds '\n"
     "                         f'(up to {last}), not {target}')\n"
     "\n\n"
     "def _numeric(exc: BaseException) -> bool:\n"),
    ("            _check_pin_current(repo_root, request)\n",
     "            _check_pin_current(repo_root, request)\n"
     "            _check_mode_pin(repo_root, request)\n"),
])

# ---------------------------------------------------------------- the ignore list (plan section 3; design 6.4)
edit('.gitignore', [
    ("# WF-1B: the score and rank-position ledgers hold drawn numbers, so they stay local (design 6.4, 6.8; WF1-10);\n"
     "# the report files in results/method_rankings/ and the search log are committed\n"
     "#results/real/development/scores/\n",
     "# WF-1B: the report files in results/method_rankings/ and the search log are committed; so, since 17 November 2026\n"
     "# (owner decision OD-5, decision log entry 70), are the score and rank-position ledgers under the scores folder\n"),
    ("# MHUP-A (design 4.2, Appendix J, 5.1-5.4, 6.1): the updater's local working files (covered by the owner's\n"
     "# backups), the two install barriers, the Mode H holdout contract runs, each batch's attempts log and the\n"
     "# score ledgers (they hold drawn numbers; the plan, the batch-id record, the lifecycle markers, the study\n"
     "# manifest and the owner records are committed), the lock clearance records and the byte-code sentinel\n",
     "# MHUP-A (design 4.2, Appendix J, 5.1-5.4, 6.1): the updater's local working files (covered by the owner's\n"
     "# backups), the two install barriers, the Mode H holdout contract runs and each batch's attempts log (the plan,\n"
     "# the batch-id record, the lifecycle markers, the study manifest, the owner records and, since 17 November 2026,\n"
     "# the Mode H score ledgers are committed), the lock clearance records and the byte-code sentinel\n"),
    ("results/real/holdout/wf_batches/**/attempts.jsonl\n#results/real/holdout/scores/\n",
     "results/real/holdout/wf_batches/**/attempts.jsonl\n"),
    ("transitory_data/lock_clearances/\ntransitory_data/no_pycache_ever\n",
     "transitory_data/lock_clearances/\ntransitory_data/no_pycache_ever\n"
     "\n"
     "# MHUP-B (design 6.4): the weekly and diagnostic contract runs (bulk), each session's attempts ledger and the\n"
     "# session lock. The session records, the forecast, witness and score ledgers, the OV-1 ledgers and the league\n"
     "# tables are committed, so a push of them is a witness.\n"
     "results/real/weekly/contract_runs/\n"
     "results/real/weekly/**/SESSION_*_attempts.jsonl\n"
     "results/real/weekly/**/ACTIVE_SESSION.lock\n"
     "results/real/diagnostic/contract_runs/\n"),
])

# ---------------------------------------------------------------- L3: the outcome reader (design 5.3, 6.3; an always-review subject)
edit('src/evaluation/outcome_reader.py', [
    ("""this package (the weekly freeze-line rule arrives with MHUP-B).
""",
     """the weekly freeze-line rule releases it (MHUP-B, design 6.3: the game's developed record, a freeze line for the
draw whose every named record verifies, and the draw accepted in the master).
"""),
    ("""    exist (after it, no outcome is re-read, 5.2). For a draw after the holdout: never in this package (the weekly
    freeze-line rule is MHUP-B's). Anything invalid or absent refuses (False).\"\"\"
    import _common.owner_records as OR
    p = get_profile(game_id)
    if type(target) is not int or target > p.holdout_last or target < p.holdout_first:
        return False
""",
     """    exist (after it, no outcome is re-read, 5.2). For a draw after the holdout (MHUP-B, design 6.3 and Appendix E): only
    when the game's developed record exists, the forecast ledger (verified in full: canonical lines, the chain, every
    line's shape) holds a freeze line for the target, every record that line names verifies (its own session record
    and digest, its DONE ticket and digest, its run folder and digest), and the target is at most the last draw of
    the ledger's current last row. Anything invalid or absent refuses (False).\"\"\"
    import _common.owner_records as OR
    p = get_profile(game_id)
    if type(target) is not int or target < p.holdout_first:
        return False
    if target > p.holdout_last:
        return _weekly_release_allowed(repo_root, game_id, target)
"""),
    ("""def _check_targets(game_id: str, targets, repo_root: Path | None = None) -> list[int]:
""",
     """def _weekly_release_allowed(repo_root: Path, game_id: str, target: int) -> bool:
    \"\"\"The weekly freeze-line rule (design 6.3). Fixed evidence paths under the root; no caller-chosen input.\"\"\"
    import _common.owner_records as OR
    import _common.weekly_records as WR
    try:
        if OR.developed_record(repo_root, game_id) is None:
            return False
        line = WR.freeze_line_for(WR.forecast_ledger(repo_root, game_id), target)
        if line is None:
            return False
        WR.verify_named_records(repo_root, game_id, line)
        _raw, rows, _evidence = MV.load_verified_source(repo_root, game_id)
        return target <= rows[-1].last_draw
    except (OR.RecordRefused, MV.LedgerRefused, ValueError, OSError):
        return False


def _check_targets(game_id: str, targets, repo_root: Path | None = None) -> list[int]:
"""),
    ("""        if type(t) is not int or t < p.first_draw + 1 or t > p.holdout_last:
            raise OutcomeRefused(f'target {t!r} is outside [{p.first_draw + 1}, {p.holdout_last}]')
        if t >= p.holdout_first and (repo_root is None or not outcome_release_allowed(repo_root, game_id, t)):
            raise OutcomeRefused(f'target {t} is a holdout draw not released by the freeze-before-outcome rule '
                                 f'(design 5.3)')
""",
     """        if type(t) is not int or t < p.first_draw + 1:
            raise OutcomeRefused(f'target {t!r} is not a draw after the first of the era ({p.first_draw})')
        if t >= p.holdout_first and (repo_root is None or not outcome_release_allowed(repo_root, game_id, t)):
            raise OutcomeRefused(f'target {t} is a holdout or later draw not released by the freeze-before-outcome '
                                 f'rule (design 5.3, 6.3)')
"""),
    ("""def read_outcomes(*, repo_root: Path, game_id: str, master_sha256: str, targets, ledger_version: int = 1) -> dict:
    \"\"\"{target: (drawn_main, drawn_powerball)} for Powerball, or {target: (drawn_main, drawn_supplementaries)} for
    Oz Lotto, both as ascending tuples, for exactly the requested targets. Refuses (OutcomeRefused) before
    decoding any row if a target or a source check fails. `ledger_version` is the pinned version (MHUP-A).\"\"\"
""",
     """def read_outcomes(*, repo_root: Path, game_id: str, master_sha256: str, targets, ledger_version: int = 1) -> dict:
    \"\"\"{target: (drawn_main, drawn_powerball)} for Powerball, or {target: (drawn_main, drawn_supplementaries)} for
    Oz Lotto, both as ascending tuples, for exactly the requested targets. Refuses (OutcomeRefused) before
    decoding any row if a target or a source check fails. `ledger_version` is the pinned version (MHUP-A).\"\"\"
    rows = read_outcome_rows(repo_root=repo_root, game_id=game_id, master_sha256=master_sha256, targets=targets,
                             ledger_version=ledger_version)
    return {t: (main, extra) for t, (main, extra, _date) in rows.items()}


def read_outcome_rows(*, repo_root: Path, game_id: str, master_sha256: str, targets, ledger_version: int = 1) -> dict:
    \"\"\"As read_outcomes, with each draw's date as the master records it: {target: (drawn_main, drawn_powerball or
    drawn_supplementaries, draw_date_text)} (MHUP-B: the weekly score line records whether the master's date is the
    draw's derived date, supplement v0.8 section 6.8). The same checks, in the same order.\"\"\"
"""),
    ("""    last = wanted[-1]                               # <= holdout_last; in the holdout only if released (5.3)
""",
     """    last = wanted[-1]                               # in or after the holdout only if released (5.3, 6.3)
"""),
    ("""            raise OutcomeRefused('holdout row reached without release')     # a second guard; unreachable by construction
""",
     """            raise OutcomeRefused('holdout or later row reached without release')     # a second guard; unreachable by construction
"""),
    ("""            out[number] = (main, _number(row[9], 20, 'Powerball'))
""",
     """            out[number] = (main, _number(row[9], 20, 'Powerball'), row[1])
"""),
    ("""            out[number] = (main, supps)
""",
     """            out[number] = (main, supps, row[1])
"""),
])
