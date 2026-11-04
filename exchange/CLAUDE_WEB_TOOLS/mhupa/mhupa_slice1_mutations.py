"""MHUP-A slice 1 mutation checks (Claude, 4 Nov 2026): one planted defect per rule of the slice; each must make a test
fail, except the few marked EQUIVALENT (a redundant defence-in-depth check whose removal another rule masks; the reason is
printed). The tree given is a full clone with the slice's src/, tests/ and archive/ overlaid (some existing tests read the
development masters through the project's reader; this tool never opens them). Each mutant is applied to a copy of the
tree (without .git) and the named test modules run in a fresh process with -f (stop at the first failure).
Usage: python3 -I mhupa_slice1_mutations.py TREE [--only N]"""
import os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
ONLY = int(sys.argv[sys.argv.index('--only') + 1]) if '--only' in sys.argv else None
MV = 'src/methods/_common/master_versions.py'
RD = 'src/methods/_common/game_draws_reader.py'
RC = 'src/methods/_common/contract_records.py'
CD = 'src/methods/_common/contract_dispatch.py'
CR = 'src/methods/_common/contract_runner.py'
CT = 'src/methods/_common/contract_task.py'
OR = 'src/methods/_common/owner_records.py'
WF = 'src/methods/_common/walk_forward.py'
OC = 'src/evaluation/outcome_reader.py'
E1 = 'src/methods/E_001/multigame_e1.py'
AD = 'src/methods/contract_adapters/e_001.py'
MCR = 'src/methods/Method_Contract_Runner.py'
VOC = 'src/methods/_common/contract_vocab.py'
T_MV = ['test_mhupa_master_versions']
T_G = ['test_mhupa_gates']
T_E1 = ['test_e1r3_revision3']
T_WF = ['test_wf1a_walk_forward']

MUTANTS = [
    # ---- design 3.2 rule 1: the ledger chain grammar (master_versions.parse_ledger)
    ('grammar: versions need not be consecutive', MV,
     "        if version != i:\n            raise LedgerRefused(f'{where}: version {version} out of order (expected {i})')",
     "        if False:\n            raise LedgerRefused(f'{where}: version {version} out of order (expected {i})')", T_MV),
    ('grammar: the first row need not be INIT', MV,
     "            if action != 'INIT':\n                raise LedgerRefused(f'{where}: the first row is not INIT')",
     "            if action not in ('INIT', 'UPDATE', 'NO_CHANGE'):\n                raise LedgerRefused(f'{where}: the first row is not INIT')", T_MV),
    ('grammar: INIT may cover less than the development prefix', MV,
     "            if last != p.holdout_first - 1 or count != p.holdout_first - p.first_draw:",
     "            if last > p.holdout_first - 1 or count > p.holdout_first - p.first_draw:", T_MV),
    ('grammar: draw_count unchecked against first and last', MV,
     "        if count != last - first + 1 or count < 1:", "        if count < 1:", T_MV,
     'EQUIVALENT: implied by the INIT rule and the UPDATE/NO_CHANGE cross-row rules by induction; kept as defence in depth'),
    ('grammar: utc may decrease', MV,
     "            if t < previous_utc:\n                raise LedgerRefused(f'{where}: utc decreases')",
     "            if False:\n                raise LedgerRefused(f'{where}: utc decreases')", T_MV),
    ('grammar: a NO_CHANGE row may carry a new master_sha256', MV,
     "                if sha != prev.master_sha256 or last != prev.last_draw or count != prev.draw_count or added != 0:",
     "                if last != prev.last_draw or count != prev.draw_count or added != 0:", T_MV),
    ('grammar: an UPDATE row\'s added range unchecked against the row before', MV,
     "                if added < 1 or a_first != prev.last_draw + 1 or a_last != last or a_last != a_first + added - 1 \\\n"
     "                        or count != prev.draw_count + added:",
     "                if added < 1 or a_last != last or a_last != a_first + added - 1:", T_MV),
    ('grammar: backup_sha256 need not be the previous master', MV,
     "                if _sha_field(row, 'backup_sha256', where, required=True) != prev.master_sha256:",
     "                if _sha_field(row, 'backup_sha256', where, required=True) is None:", T_MV),
    ('grammar: an UPDATE may repeat the previous master_sha256', MV,
     "                if sha == prev.master_sha256:\n                    raise LedgerRefused(f'{where}: UPDATE row repeats the previous master_sha256')",
     "                if False:\n                    raise LedgerRefused(f'{where}: UPDATE row repeats the previous master_sha256')", T_MV),
    ('grammar: an unknown action accepted', MV,
     "            else:\n                raise LedgerRefused(f'{where}: action {action!r} is not INIT, UPDATE or NO_CHANGE')",
     "            else:\n                pass", T_MV),
    ('grammar: a ledger with the wrong header accepted', MV,
     "    if tuple(parsed[0]) != LEDGER_COLUMNS:", "    if False:", T_MV),
    # ---- design 3.2 rule 2: prefix-verified pins (verify_master_against_ledger, resolve_pin)
    ('pins: the whole file need not equal the last row', MV,
     "    if hashlib.sha256(raw_master).hexdigest() != rows[-1].master_sha256:",
     "    if False:", T_MV,
     'EQUIVALENT: the last row\'s prefix hash with the exact line count binds the whole file; kept as the stated rule and as defence in depth'),
    ('pins: earlier rows not prefix-verified', MV,
     "        if hashlib.sha256(prefix).hexdigest() != row.master_sha256:",
     "        if row is rows[-1] and hashlib.sha256(prefix).hexdigest() != row.master_sha256:", T_MV),
    ('pins: the last line of a version need not start with last_draw', MV,
     "        if not _DIGIT.fullmatch(first_field) or int(first_field) != row.last_draw:",
     "        if not _DIGIT.fullmatch(first_field):", T_MV,
     ),
    ('pins: extra master lines beyond the last row tolerated', MV,
     "    if len(lines) != 1 + rows[-1].draw_count:", "    if len(lines) < 1 + rows[-1].draw_count:", T_MV,
     'EQUIVALENT: with extra lines the last row\'s prefix hash and the whole-file hash cannot both hold, so one of them refuses first; kept as the stated rule and as defence in depth'),
    ('pins: a pin resolves by version alone (sha ignored)', MV,
     "    if type(master_sha256) is not str or master_sha256 != row.master_sha256:",
     "    if type(master_sha256) is not str:", T_MV),
    ('pins: a pin to a version beyond the ledger resolves to the last row', MV,
     "    if type(ledger_version) is not int or not 1 <= ledger_version <= len(rows):",
     "    if type(ledger_version) is not int or ledger_version < 1:\n"
     "        raise LedgerRefused('x')\n    ledger_version = min(ledger_version, len(rows))\n    if False:", T_MV),
    ('INIT evidence: the verification record unchecked', MV,
     "    check_init_evidence(evidence, game_id, rows)\n    return rows", "    return rows", T_MV),
    # ---- design 3.2 rule 3: the target gate and the opening record (master_versions, game_draws_reader)
    ('target gate: last_draw(v) + 2 admitted', MV,
     "    return type(target) is int and p.first_draw + 1 <= target <= row.last_draw + 1",
     "    return type(target) is int and p.first_draw + 1 <= target <= row.last_draw + 2", T_MV),
    ('reader: the target gate not applied', RD,
     "        if not MV.target_admissible(game_id, target, row):\n            raise ValueError('target is outside the pinned version (at most its last draw plus one)')",
     "        if False:\n            raise ValueError('target is outside the pinned version (at most its last draw plus one)')", T_MV),
    ('reader: a holdout target without the opening record', RD,
     "                if OR.opening_record(repo_root, game_id) is None:\n                    raise ValueError('a holdout or later target needs the game\\'s opening record')",
     "                if False:\n                    raise ValueError('a holdout or later target needs the game\\'s opening record')", T_MV),
    ('reader: ledger_version 0 accepted', RD,
     "            run_manifest['ledger_version'] < 1):", "            run_manifest['ledger_version'] < 0):", T_MV,
     'EQUIVALENT: resolve_pin refuses version 0 with the same ValueError; the manifest check only names the cause earlier'),
    ('opening record: the study manifest\'s SHA-256 unchecked', OR,
     "    if file_sha256(manifest) != rec['study_manifest_sha256']:",
     "    if False:", T_MV + T_G),
    # ---- design 3.2 rule 5: the outcome reader's version pin (outcome_reader._verify_source)
    ('outcome reader: serves the whole master, not the pinned prefix', OC,
     "    return MV.prefix_bytes(raw, row)", "    return raw", T_MV),
    ('outcome reader: the pin\'s version ignored', OC,
     "        row = MV.resolve_pin(rows, ledger_version, master_sha256)",
     "        row = MV.resolve_pin(rows, len(rows), rows[-1].master_sha256)", T_MV),
    # ---- design 3.3: one data kind for every real mode (contract_task, E_1 revision 3, the adapter)
    ('data kind: REAL_HOLDOUT keeps its own view kind', CT,
     "    return REAL_VIEW_DATA_KIND if run_mode in V.REAL_MODES or run_mode == 'CATCH_UP' else run_mode",
     "    return REAL_VIEW_DATA_KIND if run_mode in ('REAL_DEVELOPMENT', 'CATCH_UP') else run_mode", T_E1),
    ('E_1 r3: accepts a run mode as a data kind', E1,
     "    if data_kind not in ('SYNTHETIC_CONTRACT_TEST', 'REAL_HISTORICAL_DEVELOPMENT'):",
     "    if data_kind not in ('SYNTHETIC_CONTRACT_TEST', 'REAL_HISTORICAL_DEVELOPMENT', 'REAL_HOLDOUT'):", T_E1),
    ('E_1 r3: a short training view accepted', E1,
     "    if len(records) != target - profile.first_draw:", "    if len(records) > target - profile.first_draw:", T_E1),
    ('E_1 r3: the ranking order inverted', E1,
     "        ranking = sorted(counts, key=lambda n:(-counts[n], _digest(digest,target,desc.barrel_id,n),n))",
     "        ranking = sorted(counts, key=lambda n:(counts[n], _digest(digest,target,desc.barrel_id,n),n))", T_E1),
    # ---- design 3.4(a): mode, target and binding rules (contract_records)
    ('3.4(a): a synthetic request may carry a binding', RC,
     "        if kind is not None:\n            raise ValueError(f'{where}: a {mode} request carries no binding')",
     "        if False:\n            raise ValueError(f'{where}: a {mode} request carries no binding')", T_G),
    ('3.4(a): a development run in the prefix may carry a session binding', RC,
     "            if kind not in (None, 'OWNER_DIAGNOSTIC'):", "            if kind not in (None, 'OWNER_DIAGNOSTIC', 'WEEKLY_SESSION'):", T_G),
    ('3.4(a): a session-bound development run may target a holdout draw', RC,
     "            if target <= p.holdout_last:\n                raise ValueError(f'{where}: a session-bound development run must target a draw after the holdout')",
     "            if target < p.holdout_first:\n                raise ValueError(f'{where}: a session-bound development run must target a draw after the holdout')", T_G),
    ('3.4(a): REAL_HOLDOUT may target a draw after the holdout', RC,
     "        if not in_holdout:\n            raise ValueError(f'{where}: REAL_HOLDOUT targets only the holdout draws {p.holdout_first}-{p.holdout_last}')",
     "        if target < p.holdout_first:\n            raise ValueError(f'{where}: REAL_HOLDOUT targets only the holdout draws {p.holdout_first}-{p.holdout_last}')", T_G),
    ('3.4(a): REAL_HOLDOUT admitted with a diagnostic binding', RC,
     "        if kind != 'MODE_H_BATCH':\n            raise ValueError(f'{where}: a REAL_HOLDOUT request must be bound to the Mode H plan')",
     "        if kind not in ('MODE_H_BATCH', 'OWNER_DIAGNOSTIC'):\n            raise ValueError(f'{where}: a REAL_HOLDOUT request must be bound to the Mode H plan')", T_G),
    ('3.4(a): FINAL_NEXT_DRAW admitted unbound', RC,
     "        if kind != 'WEEKLY_SESSION':\n            raise ValueError(f'{where}: a {mode} request must be bound to a weekly session')",
     "        if kind not in (None, 'WEEKLY_SESSION'):\n            raise ValueError(f'{where}: a {mode} request must be bound to a weekly session')", T_G,
     'EQUIVALENT in slice 1: FINAL_NEXT_DRAW is reserved (no producible product) and CATCH_UP is not yet a run mode, so the branch is unreachable until slice 2 unreserves them; slice 2 tests it'),
    ('3.4(a): a binding may name another run id', RC,
     "    if kind != 'OWNER_DIAGNOSTIC' and b['run_id'] != run_id:", "    if False:", T_G),
    ('3.4(a): a binding of an unknown kind accepted', RC,
     "    if type(b) is not dict or b.get('kind') not in V.BINDING_KINDS:",
     "    if type(b) is not dict:", T_G),
    # ---- design 3.4(b): publication admission (contract_dispatch._resolve_binding), barrier P (Appendix J)
    ('barrier P: not checked', CD,
     "    if barrier.exists() or barrier.is_symlink():", "    if False:", T_G),
    ('Mode H: the plan digest unchecked', CD,
     "            if record_digest(plan) != b['plan_digest']:", "            if False:", T_G),
    ('Mode H: a pair the plan does not list admitted', CD,
     "            if not OR.plan_lists_pair(plan, method, revision, variant, target):", "            if False:", T_G),
    ('Mode H: a closed batch still admits runs', CD,
     "            if markers:\n                refuse('BATCH_CLOSED'", "            if False:\n                refuse('BATCH_CLOSED'", T_G),
    ('Mode H: a pair with a DONE ticket admitted again', CD,
     "            if OR.pair_has_done_ticket(rows, pair):\n                refuse('PAIR_ALREADY_DONE', 'the pair has a DONE ticket; no second record')",
     "            if False:\n                refuse('PAIR_ALREADY_DONE', 'the pair has a DONE ticket; no second record')", T_G),
    ('Mode H: no open ticket needed', CD,
     "            if not OR.open_ticket_for(rows, run_id=run_id, pair=pair, request_digest=record_digest(request)):\n"
     "                refuse('NO_OPEN_TICKET', 'no open ticket names this run id, pair and request')\n"
     "        elif kind == 'WEEKLY_SESSION':",
     "            if False:\n"
     "                refuse('NO_OPEN_TICKET', 'no open ticket names this run id, pair and request')\n"
     "        elif kind == 'WEEKLY_SESSION':", T_G),
    ('tickets: an OPEN ticket for another request digest counts', OR,
     "        if t['kind'] == 'OPEN' and t['run_id'] == run_id and pair_of(t) == pair and t['request_digest'] == request_digest:",
     "        if t['kind'] == 'OPEN' and t['run_id'] == run_id and pair_of(t) == pair:", T_G),
    ('tickets: a FAILED_TO_START ticket does not close the OPEN one', OR,
     "        elif t['kind'] in ('DONE', 'FAILED_TO_START') and t['run_id'] == run_id:",
     "        elif t['kind'] in ('DONE',) and t['run_id'] == run_id:", T_G),
    ('tickets: a torn last line is parsed', OR,
     "    torn = not raw.endswith(b'\\n')", "    torn = False", T_G),
    ('session: the session digest unchecked', CD,
     "            if record_digest(session) != b['session_digest']:", "            if False:", T_G),
    ('session: a variant outside the roster admitted', CD,
     "            if member is None:\n                refuse('NOT_IN_SESSION_ROSTER'", "            if member is None:\n                member = {'release_date': '2026-01-01'}\n            if False:\n                refuse('NOT_IN_SESSION_ROSTER'", T_G),
    ('session: no developed record needed', CD,
     "            if OR.developed_record(root, game) is None:\n                refuse('NOT_DEVELOPED'", "            if False:\n                refuse('NOT_DEVELOPED'", T_G),
    ('session: a frozen target still admitted', CD,
     "            if OR.freeze_line_exists(root, game, target):", "            if False:", T_G),
    ('session: a pair DONE in another session admitted', CD,
     "            if OR.pair_done_in_any_session(root, game, pair):", "            if False:", T_G),
    ('session: no open ticket needed', CD,
     "            if not OR.open_ticket_for(rows, run_id=run_id, pair=pair, request_digest=record_digest(request)):\n"
     "                refuse('NO_OPEN_TICKET', 'no open ticket names this run id, pair and request')\n"
     "            try:",
     "            if False:\n"
     "                refuse('NO_OPEN_TICKET', 'no open ticket names this run id, pair and request')\n"
     "            try:", T_G),
    ('session: a variant released before the draw may publish a development record', CD,
     "            if mode == 'REAL_DEVELOPMENT' and released_before:", "            if False:", T_G),
    ('session: the release comparison off by a day', CD,
     "                released_before = OR.release_date_of(member) < get_profile(game).derived_date(target)",
     "                released_before = OR.release_date_of(member) <= get_profile(game).derived_date(target)", T_G),
    ('diagnostic: admits other run modes', CD,
     "            if mode != 'REAL_DEVELOPMENT':\n                refuse('DIAGNOSTIC_MODE'", "            if False:\n                refuse('DIAGNOSTIC_MODE'", T_G,
     'EQUIVALENT: the request validator admits OWNER_DIAGNOSTIC with REAL_DEVELOPMENT only, before dispatch; kept as defence in depth'),
    ('diagnostic: a holdout target without the opening record', CD,
     "                if OR.opening_record(root, game) is None:\n                    refuse('HOLDOUT_NOT_OPENED', 'a holdout or later diagnostic target needs the opening record')",
     "                if False:\n                    refuse('HOLDOUT_NOT_OPENED', 'a holdout or later diagnostic target needs the opening record')", T_G),
    ('diagnostic: a holdout target before the seal', CD,
     "                if not OR.mode_h_sealed(root, game):", "                if False:", T_G),
    ('seal: any lifecycle marker counts as the seal', OR,
     "    return SEAL in lifecycle_markers_present(root, game_id, rec['batch_id'])",
     "    return bool(lifecycle_markers_present(root, game_id, rec['batch_id']))", T_G),
    # ---- the runner (design 3.4, 5.1): roots, the project-only rule, the stale pin
    ('runner: a real run may read a workspace other than the project', CR,
     "            if Path(repo_root).resolve() != PROJECT_ROOT.resolve():\n                raise ValueError('a real run reads only the project itself')",
     "            if False:\n                raise ValueError('a real run reads only the project itself')", T_G),
    ('runner: a bound run may publish under any root', CR,
     "            if expected_root is not None and Path(run_root).resolve() != expected_root.resolve():", "            if False:", T_G),
    ('runner: the Mode H root is the development root', CR,
     "    if kind == 'MODE_H_BATCH':\n        return OR.mode_h_runs_root(PROJECT_ROOT)",
     "    if kind == 'MODE_H_BATCH':\n        return PROJECT_ROOT / 'results' / 'real' / 'development' / 'contract_runs'", T_G),
    ('runner: a stale pin accepted for an official run', CR,
     "    if (request['ledger_version'], request['master_sha256']) != (version, sha):", "    if False:", T_G),
    # ---- EX_142 B01: the frozen pin in the plan and the session
    ('B01: the request pin not compared with the plan\'s frozen pin', CD,
     "            if pin != plan_pin:", "            if False:", T_G),
    ('B01: the plan not tied to the opening record\'s study manifest', CD,
     "            if plan['study_manifest_sha256'] != opening['study_manifest_sha256']:", "            if False:", T_G),
    ('B01: the plan\'s version need not be the admitted version', CD,
     "            if plan_pin[0] != opening['freeze_version'] + 1:", "            if False:", T_G),
    ('B01: a Mode H binding without the opening record', CD,
     "            if opening is None:\n                refuse('HOLDOUT_NOT_OPENED', 'a Mode H plan binding needs the game\\'s opening record')",
     "            if opening is None:\n                opening = {'study_manifest_sha256': plan['study_manifest_sha256'], 'freeze_version': plan['ledger_version'] - 1}", T_G),
    ('B01: the request pin not compared with the session\'s frozen pin', CD,
     "            if pin != OR.pin_of(session, 'session record'):", "            if False:", T_G),
    ('B01: a plan without a pin accepted', OR,
     "    pin_of(plan, 'Mode H plan')\n    _sha(plan, 'study_manifest_sha256', 'Mode H plan')\n    return plan",
     "    return plan", T_G),
    ('B01: a session record without a pin accepted', OR,
     "    pin_of(rec, 'session record')\n    return rec", "    return rec", T_G,
     'EQUIVALENT: the dispatch gate calls pin_of on the session record itself and refuses the same way; kept as defence in depth'),
    ('B01: a malformed pin accepted', OR,
     "    if type(v) is not int or v < 1:\n        raise RecordRefused(f'{what}: ledger_version is not a positive whole number')\n    return v, _sha(rec, 'master_sha256', what)",
     "    return v, rec.get('master_sha256')", T_G),
    # ---- EX_142 B02: present-but-invalid evidence fails closed
    ('B02: a ledger that is not a plain file reads as empty', OR,
     "    if not _plain_file(path):\n        raise RecordRefused(f'{path.name}: exists but is not a plain file')\n    raw = path.read_bytes()",
     "    if not _plain_file(path):\n        return [], False\n    raw = path.read_bytes()", T_G),
    ('B02: session ledgers that are not plain files filtered away', OR,
     "    return sorted(folder.glob('SESSION_*_attempts.jsonl'))", "    return sorted(p for p in folder.glob('SESSION_*_attempts.jsonl') if _plain_file(p))", T_G),
    ('B02: an unknown forecast-ledger schema ignored', OR,
     "        if r.get('schema') not in FORECAST_LEDGER_SCHEMAS:\n            raise RecordRefused('forecast ledger: a line of an unknown schema')",
     "        if False:\n            raise RecordRefused('forecast ledger: a line of an unknown schema')", T_G),
    ('B02: a freeze line with a malformed target ignored', OR,
     "        if type(r.get('target_draw_number')) is not int:\n            raise RecordRefused('forecast ledger: a line without a whole-number target')",
     "        if False:\n            raise RecordRefused('forecast ledger: a line without a whole-number target')", T_G),
    ('B02: a marker that is not a plain file counts as present', OR,
     "        if not _plain_file(path):\n            raise RecordRefused(f'lifecycle marker {m} exists but is not a plain file')\n        out.append(m)",
     "        out.append(m)", T_G),
    ('B02: a marker that is not a plain file counts as absent', OR,
     "        if not _plain_file(path):\n            raise RecordRefused(f'lifecycle marker {m} exists but is not a plain file')\n        out.append(m)",
     "        if not _plain_file(path):\n            continue\n        out.append(m)", T_G),
    # ---- EX_142 B03: the grammar applies to every ledger
    ('B03: a blank physical line tolerated', MV,
     "    if any(line.strip() == '' for line in physical):\n        raise LedgerRefused('ledger has a blank line')",
     "    physical = [line for line in physical if line.strip() != '']", T_MV),
    ('B03: a record spanning two physical lines tolerated', MV,
     "    if len(parsed) != len(physical):\n        raise LedgerRefused('ledger has a record spanning more than one physical line')",
     "    if False:\n        raise LedgerRefused('ledger has a record spanning more than one physical line')", T_MV,
     'EQUIVALENT since B03r1: the canonical round trip of every physical line refuses a split record first; kept as defence in depth'),
    ('B03: the INIT row\'s utc not parsed', MV,
     "        t = _utc_instant(row.get('utc'), where)\n        if not row.get('tool_version', '').strip():",
     "        t = _utc_instant(row.get('utc'), where) if i > 1 else None\n        if not row.get('tool_version', '').strip():", T_MV),
    ('B03: the INIT row\'s tool_version may be empty', MV,
     "        if not row.get('tool_version', '').strip():\n            raise LedgerRefused(f'{where}: tool_version is empty')",
     "        if i > 1 and not row.get('tool_version', '').strip():\n            raise LedgerRefused(f'{where}: tool_version is empty')", T_MV),
    ('B03: the INIT row\'s added fields unchecked', MV,
     "            if added != count or _int_field(row, 'added_first', where) != first or \\\n                    _int_field(row, 'added_last', where) != last:",
     "            if False:", T_MV),
    ('B03: the INIT row may carry grab or backup fields', MV,
     "            for f in ('grab_file', 'grab_sha256', 'backup_file', 'backup_sha256'):\n                if row.get(f) != '':\n                    raise LedgerRefused(f'{where}: the INIT row has {f}')",
     "            pass", T_MV),
    ('B03: a one-row ledger exempt from the prefix and line-count rules', MV,
     "    for row in rows:\n        n = 1 + row.draw_count",
     "    for row in (rows if len(rows) > 1 else []):\n        n = 1 + row.draw_count", T_MV),
    # ---- EX_144 B02r1 and B03r1
    ('B02r1: a blank complete JSONL line skipped as before', OR,
     "        if not line:\n            raise RecordRefused(f'{path.name}: a blank complete line (never written by a ledger writer)')   # EX_144 B02r1",
     "        if not line:\n            continue", T_G),
    ('B03r1: the CSV parser not strict', MV,
     "        parsed = list(csv.reader(physical, strict=True))", "        parsed = list(csv.reader(physical))", T_MV,
     'EQUIVALENT: the canonical round trip refuses every malformed quoting the strict parser would; strict=True is kept as the stated boundary and as defence in depth'),
    ('B03r1: no canonical round trip of each record', MV,
     "        if _render(fields) != line:", "        if False:", T_MV),
    # ---- the plan's pin (walk_forward.ledger_pin) and the legacy launcher
    ('walk-forward: the plan pins version 1 whatever the ledger says', WF,
     "        return MV.current_pin(roots()['project'], game_id)", "        return 1, MV.current_pin(roots()['project'], game_id)[1]", T_G),
    ('standalone launcher: REAL_HOLDOUT not refused at the CLI', MCR,
     "    elif args.mode in ('REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'CATCH_UP'):",
     "    elif args.mode in ('FINAL_NEXT_DRAW', 'CATCH_UP'):", T_G),
    ('standalone launcher: the diagnostic route publishes under the development root', MCR,
     "            run_root = OR.diagnostic_runs_root(CR.PROJECT_ROOT)                             # MHUP-A (design 3.4)",
     "            run_root = CR.PROJECT_ROOT / 'results' / 'real' / 'development' / 'contract_runs'", T_G),
    ('standalone launcher: --binding accepted for a synthetic run', MCR,
     "        if args.binding is not None:\n            parser.error('--binding is for real runs only')",
     "        if False:\n            parser.error('--binding is for real runs only')", T_G),
]


def run(tree: Path, mods) -> bool:
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(tree / p) for p in ('src', 'src/methods', 'tests'))
    r = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-f'] + [f'tests.{m}' for m in mods], cwd=tree, env=env,
                       capture_output=True, text=True, timeout=1800)
    return r.returncode == 0


def copy_tree(dst: Path):
    shutil.copytree(TREE, dst, ignore=shutil.ignore_patterns('__pycache__', '.git'))


if __name__ == '__main__':
    muts = list(MUTANTS)
    if ONLY is not None:
        muts = muts[ONLY:ONLY + 1]
    t0 = time.perf_counter()
    ok = run(TREE, sorted({m for x in muts for m in x[4]}))
    print('baseline (unmutated) passes:', ok, f'({time.perf_counter() - t0:.0f}s)')
    caught = equivalent = 0
    for i, (name, rel, old, new, mods, *note) in enumerate(muts):
        with tempfile.TemporaryDirectory() as td:
            tree = Path(td) / 't'
            copy_tree(tree)
            f = tree / rel
            text = f.read_text(encoding='utf-8')
            if text.count(old) != 1:
                print(f'MUTANT NOT APPLIED ({text.count(old)} matches): {name}')
                continue
            f.write_text(text.replace(old, new), encoding='utf-8')
            passed = run(tree, mods)
            if note and passed:
                equivalent += 1
                print(f'EQUIVALENT [{i}] {name}  ({", ".join(mods)})  -- {note[0]}', flush=True)
                continue
            caught += not passed
            print(('CAUGHT   ' if not passed else 'SURVIVED ') + f'[{i}] ' + name + f'  ({", ".join(mods)})'
                  + ('  -- expected EQUIVALENT but caught' if note else ''), flush=True)
    print(f'{caught} of {len(muts)} mutants caught; {equivalent} equivalent (survive by design, reason given); '
          f'{len(muts) - caught - equivalent} survived')
