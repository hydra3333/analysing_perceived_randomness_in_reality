"""MHUP-A slice 1: counted edits to the existing modules (design v0.1r5 sections 2, 3; register v0.24).

Applies to a dev TREE (a copy of the base at main 2061055, code unchanged since PERF-1 3fce327). Every old
string must occur exactly once; the script stops otherwise. The new modules (master_versions.py,
owner_records.py) are written separately. Usage: python3 -I apply_slice1.py TREE
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
M = tree / 'src' / 'methods'


def edit(rel, pairs):
    p = tree / rel
    s = p.read_bytes().decode('ascii')
    for a, b in pairs:
        assert s.count(a) == 1, (rel, s.count(a), a[:80])
        s = s.replace(a, b)
    s.encode('ascii')
    p.write_bytes(s.encode('ascii'))
    print('edited', rel, len(pairs))


# ---------------------------------------------------------------- contract_vocab.py
edit('src/methods/_common/contract_vocab.py', [
    ("RESERVED_MODES = frozenset(('REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'IN_SAMPLE_DIAGNOSTIC'))  # E2R-R44, R44A\n",
     "# E2R-R44, R44A. REAL_HOLDOUT was unreserved by MHUP-R (design v0.1r5 section 5.1): it opens only for a ticketed\n"
     "# request bound to the game's one Mode H plan, with the opening record present (the dispatch gate decides).\n"
     "RESERVED_MODES = frozenset(('FINAL_NEXT_DRAW', 'IN_SAMPLE_DIAGNOSTIC'))\n"
     "REAL_MODES = frozenset(('REAL_DEVELOPMENT', 'REAL_HOLDOUT', 'FINAL_NEXT_DRAW'))   # every mode that reads a real master\n"
     "# The binding a real-mode request above the development prefix must carry (design 3.4): the Mode H plan, a weekly\n"
     "# session, or the owner's unofficial diagnostic route.\n"
     "BINDING_KINDS = frozenset(('MODE_H_BATCH', 'WEEKLY_SESSION', 'OWNER_DIAGNOSTIC'))\n"),
    ("    if schema == FORECAST:\n        if run_mode == 'REAL_DEVELOPMENT':\n            return 'WF_FORECAST', 'DEVELOPMENT_WF_EXPLORATORY'\n",
     "    if schema == FORECAST:\n        if run_mode == 'REAL_DEVELOPMENT':\n            return 'WF_FORECAST', 'DEVELOPMENT_WF_EXPLORATORY'\n"
     "        if run_mode == 'REAL_HOLDOUT':\n            return 'WF_FORECAST', 'HOLDOUT_MODE_H'           # E2R-R41's row, unreserved as written (MHUP-R)\n"),
])

# ---------------------------------------------------------------- contract_records.py
edit('src/methods/_common/contract_records.py', [
    ("import hashlib\nimport math\n", "import hashlib\nimport math\nimport re\n"),
    ("                   'registry_entry_digest', 'run_id', 'master_file', 'ledger_version', 'master_sha256')\n\n\n"
     "def validate_run_request(r: object) -> dict:\n    where = 'run request'\n    _schema(r, V.RUN_REQUEST, where)\n"
     "    _keys(r, _REQUEST_FIELDS, where)\n",
     "                   'registry_entry_digest', 'run_id', 'master_file', 'ledger_version', 'master_sha256')\n"
     "_REQUEST_OPTIONAL = ('binding',)      # MHUP-A: present exactly when the mode and target need one (design 3.4)\n"
     "_BINDING_FIELDS = {'MODE_H_BATCH': ('kind', 'batch_id', 'plan_digest', 'run_id'),\n"
     "                   'WEEKLY_SESSION': ('kind', 'session_id', 'session_digest', 'run_id'),\n"
     "                   'OWNER_DIAGNOSTIC': ('kind',)}\n"
     "BATCH_ID = re.compile(r'wf-[0-9a-f]{32}\\Z', re.ASCII)\n"
     "SESSION_ID = re.compile(r'[0-9a-f]{32}\\Z', re.ASCII)\n\n\n"
     "def validate_binding(b: object, run_id: str, where: str = 'run request.binding') -> dict:\n"
     "    \"\"\"One of the three binding shapes of design 3.4(a). A binding names the run id of its own request.\"\"\"\n"
     "    if type(b) is not dict or b.get('kind') not in V.BINDING_KINDS:\n"
     "        raise ValueError(f'{where}: kind must be one of {sorted(V.BINDING_KINDS)}')\n"
     "    kind = b['kind']\n"
     "    _keys(b, _BINDING_FIELDS[kind], where)\n"
     "    if kind == 'MODE_H_BATCH':\n"
     "        _match(BATCH_ID, b['batch_id'], f'{where}.batch_id')\n"
     "        _match(V.SHA256, b['plan_digest'], f'{where}.plan_digest')\n"
     "    elif kind == 'WEEKLY_SESSION':\n"
     "        _match(SESSION_ID, b['session_id'], f'{where}.session_id')\n"
     "        _match(V.SHA256, b['session_digest'], f'{where}.session_digest')\n"
     "    if kind != 'OWNER_DIAGNOSTIC' and b['run_id'] != run_id:\n"
     "        raise ValueError(f'{where}: the binding names another run id')\n"
     "    return b\n\n\n"
     "def binding_kind(request: Mapping) -> str | None:\n"
     "    b = request.get('binding')\n"
     "    return b['kind'] if type(b) is dict else None\n\n\n"
     "def _check_mode_target_binding(r: Mapping, p, where: str) -> None:\n"
     "    \"\"\"Design 3.4(a): which modes may name which targets, and which binding each needs. The pin-dependent half\n"
     "    (target <= last_draw(v) + 1; FINAL_NEXT_DRAW only for last_draw(v) + 1) is checked where the pin is read.\"\"\"\n"
     "    mode, target = r['run_mode'], r['target_draw_number']\n"
     "    kind = binding_kind(r)\n"
     "    if 'binding' in r:\n"
     "        validate_binding(r['binding'], r['run_id'], f'{where}.binding')\n"
     "    if target <= p.first_draw:\n"
     "        raise ValueError(f'{where}: the era\\'s first draw has no history to forecast from')\n"
     "    in_prefix = p.historical_development_target_allowed(target)\n"
     "    in_holdout = p.holdout_first <= target <= p.holdout_last\n"
     "    if mode in V.SYNTHETIC_MODES or mode in V.BENCHMARK_MODES or mode == 'IN_SAMPLE_DIAGNOSTIC':\n"
     "        if not in_prefix:\n"
     "            raise ValueError(f'{where}: target is outside the authorised development prefix (E2R-R52)')\n"
     "        if kind is not None:\n"
     "            raise ValueError(f'{where}: a {mode} request carries no binding')\n"
     "    elif mode == 'REAL_DEVELOPMENT':\n"
     "        if in_prefix:\n"
     "            if kind not in (None, 'OWNER_DIAGNOSTIC'):\n"
     "                raise ValueError(f'{where}: a development run within the prefix carries no session or Mode H binding')\n"
     "        elif kind == 'WEEKLY_SESSION':\n"
     "            if target <= p.holdout_last:\n"
     "                raise ValueError(f'{where}: a session-bound development run must target a draw after the holdout')\n"
     "        elif kind != 'OWNER_DIAGNOSTIC':\n"
     "            raise ValueError(f'{where}: a REAL_DEVELOPMENT target above the development prefix needs a session or '\n"
     "                             f'diagnostic binding (design 3.4)')\n"
     "    elif mode == 'REAL_HOLDOUT':\n"
     "        if not in_holdout:\n"
     "            raise ValueError(f'{where}: REAL_HOLDOUT targets only the holdout draws {p.holdout_first}-{p.holdout_last}')\n"
     "        if kind != 'MODE_H_BATCH':\n"
     "            raise ValueError(f'{where}: a REAL_HOLDOUT request must be bound to the Mode H plan')\n"
     "    elif mode in ('FINAL_NEXT_DRAW', 'CATCH_UP'):\n"
     "        if target <= p.holdout_last:\n"
     "            raise ValueError(f'{where}: {mode} targets only draws after the holdout')\n"
     "        if kind != 'WEEKLY_SESSION':\n"
     "            raise ValueError(f'{where}: a {mode} request must be bound to a weekly session')\n"
     "    else:\n"
     "        raise ValueError(f'{where}: no target rule for run mode {mode}')\n\n\n"
     "def validate_run_request(r: object) -> dict:\n    where = 'run request'\n    _schema(r, V.RUN_REQUEST, where)\n"
     "    _keys(r, _REQUEST_FIELDS, where, _REQUEST_OPTIONAL)\n"),
    ("    target = _int(r['target_draw_number'], f'{where}.target_draw_number')\n"
     "    if not p.historical_development_target_allowed(target):\n"
     "        raise ValueError(f'{where}: target is outside the authorised development prefix (E2R-R52)')\n"
     "    _in(r['observation_view'], V.OBSERVATION_VIEWS, f'{where}.observation_view')\n",
     "    _int(r['target_draw_number'], f'{where}.target_draw_number')\n"
     "    _in(r['observation_view'], V.OBSERVATION_VIEWS, f'{where}.observation_view')\n"),
    ("    _match(V.RUN_ID, r['run_id'], f'{where}.run_id')\n    if r['master_file'] != f'{p.game_id}_results_master.csv':\n"
     "        raise ValueError(f'{where}: unapproved master file')\n"
     "    _int(r['ledger_version'], f'{where}.ledger_version', low=1, high=1)\n",
     "    _match(V.RUN_ID, r['run_id'], f'{where}.run_id')\n    _check_mode_target_binding(r, p, where)\n"
     "    if r['master_file'] != f'{p.game_id}_results_master.csv':\n"
     "        raise ValueError(f'{where}: unapproved master file')\n"
     "    _int(r['ledger_version'], f'{where}.ledger_version', low=1)       # any version the ledger chain accepts (MHUP-A)\n"),
])

# ---------------------------------------------------------------- contract_forecast.py (the header's target gate)
edit('src/methods/_common/contract_forecast.py', [
    ("    target = _int(rec['target_draw_number'], f'{where}.target_draw_number')\n"
     "    if not p.historical_development_target_allowed(target):\n"
     "        raise ValueError(f'{where}: target outside the development prefix')\n",
     "    target = _int(rec['target_draw_number'], f'{where}.target_draw_number')\n"
     "    # MHUP-A (design 3.2 rule 3): a record's target must be one its run mode may name. Synthetic and in-sample\n"
     "    # records stay within the development prefix; a REAL_HOLDOUT record names a holdout draw; a REAL_DEVELOPMENT\n"
     "    # record names any draw after the era's first (above the prefix it is session-bound or diagnostic, which the\n"
     "    # dispatch gate and the scorer establish from the records, not from the forecast itself).\n"
     "    mode = rec['run_mode']\n"
     "    if mode == 'REAL_HOLDOUT':\n"
     "        if not (p.holdout_first <= target <= p.holdout_last):\n"
     "            raise ValueError(f'{where}: a REAL_HOLDOUT record must name a holdout draw')\n"
     "    elif mode in V.REAL_MODES:\n"
     "        if target <= p.first_draw:\n"
     "            raise ValueError(f'{where}: target has no history')\n"
     "    elif not p.historical_development_target_allowed(target):\n"
     "        raise ValueError(f'{where}: target outside the development prefix')\n"),
])

# ---------------------------------------------------------------- contract_receipts.py
edit('src/methods/_common/contract_receipts.py', [
    ("    _int(r['ledger_version'], f'{where}.ledger_version', low=1, high=1)\n",
     "    _int(r['ledger_version'], f'{where}.ledger_version', low=1)       # any version the ledger chain accepts (MHUP-A)\n"),
])

# ---------------------------------------------------------------- contract_task.py (one data kind, design 3.3)
edit('src/methods/_common/contract_task.py', [
    ("def view_data_kind(run_mode: str) -> str:\n    return REAL_VIEW_DATA_KIND if run_mode == 'REAL_DEVELOPMENT' else run_mode\n",
     "def view_data_kind(run_mode: str) -> str:\n"
     "    \"\"\"One data kind for every real mode (design 3.3): the view a method sees, and so its permitted-view digest and\n"
     "    every tie-break, depend on the prefix, the configuration and the software only, never on the run mode. A\n"
     "    synthetic mode keeps its own name, as before.\"\"\"\n"
     "    return REAL_VIEW_DATA_KIND if run_mode in V.REAL_MODES or run_mode == 'CATCH_UP' else run_mode\n"),
])

# ---------------------------------------------------------------- E_1 revision 3 (design section 2)
edit('src/methods/E_001/multigame_e1.py', [
    ("def forecast(profile: GameProfile, records: Sequence[Mapping], digest: str, target: int,\n"
     "             *, data_kind: str) -> dict:\n"
     "    if data_kind not in ('SYNTHETIC_CONTRACT_TEST', 'REAL_DEVELOPMENT'):\n"
     "        # Revision 2 (owner decision WF1-13): synthetic contract tests and real development runs only.\n"
     "        raise ValueError('multi-game E_1 real execution not authorised')\n"
     "    if not profile.historical_development_target_allowed(target):\n"
     "        raise ValueError('historical target outside development boundary')\n"
     "    if len(records) != target - profile.first_draw:\n",
     "def forecast(profile: GameProfile, records: Sequence[Mapping], digest: str, target: int,\n"
     "             *, data_kind: str) -> dict:\n"
     "    if data_kind not in ('SYNTHETIC_CONTRACT_TEST', 'REAL_HISTORICAL_DEVELOPMENT'):\n"
     "        # Revision 3 (MHUP-R, design v0.1r5 section 2; owner decision MHUP-Q10): the method takes the VIEW data kind,\n"
     "        # never a run mode. Every real run mode maps to the one real view kind (design 3.3); the target ceiling is\n"
     "        # the shared target gate and mode gates of design section 3, not the method's own check.\n"
     "        raise ValueError('multi-game E_1: unknown view data kind')\n"
     "    if type(target) is not int or target <= profile.first_draw:\n"
     "        raise ValueError('target has no history')\n"
     "    if len(records) != target - profile.first_draw:\n"),
])
edit('src/methods/E_001_Historical_Appearance_Frequency.py', [
    ("        legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '2')\n",
     "        legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '3')\n"),
])
edit('src/methods/contract_adapters/e_001.py', [
    ("published record can never differ from what E_1 itself computes. Since E_1 revision 2 (owner decision\n"
     "WF1-13), E_1's function accepts SYNTHETIC_CONTRACT_TEST and REAL_DEVELOPMENT data, with revision 1's counting.\n",
     "published record can never differ from what E_1 itself computes. Since E_1 revision 3 (MHUP-R, design v0.1r5\n"
     "section 2), E_1's function takes the view data kind (SYNTHETIC_CONTRACT_TEST or REAL_HISTORICAL_DEVELOPMENT) and\n"
     "never a run mode, with revision 1's counting, ranking and tie order.\n"),
    ("from _common.contract_task import permitted_view_digest\n",
     "from _common.contract_task import permitted_view_digest, view_data_kind\n"),
    ("                       task.target_draw_number, data_kind=task.run_mode)\n",
     "                       task.target_draw_number, data_kind=view_data_kind(task.run_mode))\n"),
])

print('slice 1 edits applied to', tree)
