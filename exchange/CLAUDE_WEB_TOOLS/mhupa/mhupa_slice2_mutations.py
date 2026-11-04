"""MHUP-A slice 2 mutation checks (Claude, 5 Nov 2026): one planted defect per rule of the slice; each must make a test
fail, except the few marked EQUIVALENT (a redundant defence-in-depth check whose removal another rule masks; the reason is
printed). The tree given is a full clone with the slice's src/, tests/, root .bat files and .gitignore overlaid (some
existing tests read the development masters through the project's reader; this tool never opens them). Each mutant is
applied to a copy of the tree (without .git) and the named test modules or classes run in a fresh process with -f.
The updater's mutants are caught by its own offline self-test, run by tests.test_mhupa_updater_v0_2.
Usage: python3 -I mhupa_slice2_mutations.py TREE [--only N]"""
import os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
ONLY = int(sys.argv[sys.argv.index('--only') + 1]) if '--only' in sys.argv else None
UP = 'src/results_master_v0_2.py'
CL = 'src/methods/_common/closure.py'
OR = 'src/methods/_common/owner_records.py'
WF = 'src/methods/_common/walk_forward.py'
CD = 'src/methods/_common/contract_dispatch.py'
MH = 'src/evaluation/mode_h.py'
OC = 'src/evaluation/outcome_reader.py'
RW = 'src/evaluation/report_writer.py'
PC = 'src/package_tools/process_check.py'
IR = 'src/package_tools/install_records.py'
RE = 'Run_Experiment.bat'
RV = 'Run_Evaluation.bat'
T_UP = ['test_mhupa_updater_v0_2']
T_LA = ['test_mhupa_launchers']
T_MO = ['test_mhupa_mode_h.ManifestAndOpening']
T_PL = ['test_mhupa_mode_h.PlanRefusals']
T_PI = ['test_mhupa_mode_h.Pipeline']
T_RD = ['test_mhupa_mode_h.OutcomeReaderRule']
T_CLI = ['test_mhupa_method_mode_h_cli']
T_PC = ['test_mhupa_process_check']
T_IR = ['test_mhupa_install_records']
T_G = ['test_mhupa_gates']

MUTANTS = [
    # ---- the updater v0.2 (design 4.1 refusals (1), (2), admission (3); A6; 4.2 freeze fields), via its self-test
    ('updater: refusal (1) never raised (an opened, unsealed game past v_f may update)', UP,
     "    raise Refused(f\"{game}: the holdout is opened and the Mode H study is not sealed; the ledger's last row is \"",
     "    return 'SEALED'\n    raise Refused(f\"{game}: the holdout is opened and the Mode H study is not sealed; the ledger's last row is \"", T_UP),
    ('updater: refusal (1) compares the version only, not the master SHA-256', UP,
     '    if int(last["version"]) == v_f and last["master_sha256"] == h_f:', '    if int(last["version"]) == v_f:', T_UP,
     'EQUIVALENT in the self-test: a ledger at v_f with another SHA-256 fails load_verified_master (chain) before freeze_state; '
     'the field is read for the message and for an opening record that names a foreign master; defence in depth'),
    ('updater: refusal (2) dropped before the lock', UP,
     '        if session_lock_present(root, g):                      # refusal (2), before any lock or fetch\n'
     '            raise Refused(f"{g}: ACTIVE_SESSION.lock exists (a weekly session is active); nothing was requested")\n',
     '', T_UP),
    ('updater: refusal (2) dropped under the lock', UP,
     "    if session_lock_present(root, game):                       # refusal (2) re-checked under the updater's lock\n"
     '        raise Refused(f"{game}: ACTIVE_SESSION.lock exists (a weekly session is active); nothing was requested")\n',
     '', T_UP),
    ('updater: refusal (1) not re-checked under the lock', UP,
     "    state = freeze_state(root, game, st.ledger_rows())        # refusal (1) re-checked under the updater's lock\n",
     "    state = 'SEALED'\n", T_UP),
    ('updater: admission (3) accepts an UPDATE that stops short of holdout_last', UP,
     '    if state == "FIRST_UPDATE" and (not new or new[-1].number < holdout_last(game)):',
     '    if state == "FIRST_UPDATE" and not new:', T_UP),
    ('updater: admission (3) lets a NO_CHANGE append a row in the window', UP,
     '    if state == "FIRST_UPDATE" and (not new or new[-1].number < holdout_last(game)):',
     '    if state == "FIRST_UPDATE" and new and new[-1].number < holdout_last(game):', T_UP),
    ('updater: holdout_last off by one', UP,
     '    return FIRST_QUARANTINED_DRAW[game] + HOLDOUT_DRAWS - 1', '    return FIRST_QUARANTINED_DRAW[game] + HOLDOUT_DRAWS - 2', T_UP),
    ('updater: a sealed study needs no batch-id record', UP,
     '    rec_path = root / "results" / "real" / "holdout" / game / "MODE_H_BATCH_ID.json"\n    if not rec_path.exists():\n        return False\n',
     '    rec_path = root / "results" / "real" / "holdout" / game / "MODE_H_BATCH_ID.json"\n    if not rec_path.exists():\n        return True\n', T_UP),
    ('updater: a malformed MODE_H_SEALED marker counts as the seal', UP,
     '    if mk.get("schema") != SEAL_SCHEMA or mk.get("batch_id") != bid:\n        raise Refused(f"{seal.name} for {game} is not a valid MODE_H_SEALED marker")\n',
     '', T_UP),
    ('updater: an inconsistent study version advance is accepted', UP,
     '        if named != beyond:\n            raise Refused(f"{game}: the study version advance does not name exactly the ledger rows beyond "\n'
     '                          f"version {admitted}; nothing was requested")\n',
     '', T_UP, 'EQUIVALENT: the refusal (1) stands whether or not the advance is consistent; the check only sharpens the message '
                'and refuses a forged record; the self-test asserts Refused either way'),
    ('updater: the final host may be any Lotterywest host', UP,
     '    if parts.scheme != "https" or host != RESULTS_HOST:', '    if parts.scheme != "https" or not host.endswith("lotterywest.wa.gov.au"):', T_UP),
    ('updater: the scheme is not checked', UP,
     '    if parts.scheme != "https" or host != RESULTS_HOST:', '    if host != RESULTS_HOST:', T_UP),
    ('updater: the final-host check is not called in fetch', UP,
     '        check_final_url(self.driver.current_url)\n', '', T_UP),
    ('updater: an opening record without the freeze fields is accepted', UP,
     '    if (type(rec.get("freeze_version")) is not int or rec["freeze_version"] < 1 or\n'
     '            not re.fullmatch(r"[0-9a-f]{64}", str(rec.get("freeze_master_sha256", "")))):\n'
     '        raise Refused(f"{p.name} lacks the freeze fields (freeze_version, freeze_master_sha256); "\n'
     '                      "the holdout is NOT treated as opened")\n', '', T_UP),
    ('updater: TOOL_VERSION left at 0.1', UP, 'TOOL_VERSION = "0.2"\n', 'TOOL_VERSION = "0.1"\n', T_UP),
    # ---- the launchers (design 4.1 (a)-(d); 6.1)
    ('launcher: -B dropped from the run line', RE, b'"%PY%" -B -u %*', b'"%PY%" -u %*', T_LA),
    ('launcher: PYTHONDONTWRITEBYTECODE not set before the probe', RE, b'set "PYTHONDONTWRITEBYTECODE=1"\r\n', b'', T_LA),
    ('launcher: the pycache folder present does not refuse', RE, b'if exist "%PYTHONPYCACHEPREFIX%" goto :pycache_present\r\n', b'', T_LA),
    ('launcher: the refusal exits with a code already in use', RE, b'set "RC=10"', b'set "RC=9"', T_LA),
    ('launcher: Run_Evaluation.bat launches from src\\methods', RV, b'pushd "%ROOT%src\\evaluation"', b'pushd "%ROOT%src\\methods"', T_LA),
    # ---- the closure and the environment (design 4.1, Appendix H)
    ('closure: a sourceless .pyc under src/ is accepted', CL,
     "        if p.suffix.lower() in ('.pyc', '.pyo'):\n            raise ClosureRefused(f'sourceless byte-code under src/: {_rel(p, root)}')\n", '', T_MO),
    ('closure: __pycache__ folders enter the closure', CL,
     "            dirnames[:] = [d for d in dirnames if d != '__pycache__']\n", '', T_MO),
    ('closure: the root .bat files are not frozen', CL,
     "    for p in sorted(root.glob('*.bat')):\n        if p.is_file():\n            files[p.name] = _sha(p)\n", '', T_PL),
    ('environment: a RECORD hash mismatch is accepted', CL,
     "            if digest is not None and actual != digest:\n                raise ClosureRefused(f'{info.name}: {rel} differs from its RECORD hash')\n", '', T_PL),
    ('environment: orphans under site-packages are accepted', CL,
     "    if orphans:\n        raise ClosureRefused(f'{len(orphans)} file(s) under site-packages that no RECORD lists, the first: '\n"
     "                             f'{_rel(orphans[0], sp)}')\n", '', T_MO),
    ('environment: the interpreter files are not frozen', CL,
     "    inv['interpreter'] = {_rel(p, env.base_prefix): _sha(p) for p in _interpreter_files(env)}\n    if not inv['interpreter']:\n        raise ClosureRefused(f'no interpreter files found under {env.base_prefix}')\n",
     "    inv['interpreter'] = {'fixed': '0' * 64}\n", T_PL),
    ('environment: check compares nothing (digest ignored)', CL,
     "    if now_e['digest'] != frozen_e['digest']:", "    if False:", T_PL),
    ('closure: check compares nothing (digest ignored)', CL,
     "    if now_c['digest'] != manifest['closure']['digest']:", "    if False:", T_PL),
    # ---- the owner records of slice 2 (design 4.1, 5.2)
    ('markers: write_marker ignores the order (SCORING_STARTED without BATCH_COMPLETE)', OR,
     "    if order > 0 and LIFECYCLE_MARKERS[order - 1] not in present:\n        raise RecordRefused(f'{name}: the marker before it ({LIFECYCLE_MARKERS[order - 1]}) does not exist')\n",
     '', T_PI, 'EQUIVALENT in the suite: every writer checks the marker before it itself (the scorer refuses without BATCH_COMPLETE; '
              'the driver writes BATCH_COMPLETE first); the order rule is defence in depth against a hand-written marker'),
    ('markers: a second marker of the same name may be written', OR,
     "    if any(LIFECYCLE_MARKERS.index(m) >= order for m in present):\n        raise RecordRefused(f'{name}: a marker at or after it already exists ({\", \".join(present)})')\n",
     '', T_PI, 'EQUIVALENT: write_record is create-only (contract_publication.create_only refuses an existing file), so a second '
              'marker of the same name fails there; the rule also refuses a LATER marker already present (defence in depth)'),
    ('roster digest: a pair with two DONE tickets is accepted (the first wins)', OR,
     "            if len(ids) != 1:\n                raise RecordRefused(f'pair {pair} has {len(ids)} DONE tickets; exactly one is the roster\\'s')\n",
     "            if len(ids) < 1:\n                raise RecordRefused(f'pair {pair} has {len(ids)} DONE tickets; exactly one is the roster\\'s')\n", T_PI),
    ('roster digest: run ids left out of the roster', OR,
     "            roster.append([*pair, ids[0]])", "            roster.append([*pair])", T_RD),
    ('exposure flags: 1585 and 1586 not flagged', OR,
     "    decision = EXPOSED_DRAWS.get(game_id, {}).get(target)", "    decision = None", T_MO),
    ('admitted version: an advance need not name exactly the rows beyond v_a', OR,
     "    if named != beyond:\n        raise RecordRefused('the study version advance does not name exactly the ledger rows beyond the admitted version')\n",
     '', T_PI),
    ('SCORING_STARTED marker accepted without its roster digest', OR,
     "    if marker == 'SCORING_STARTED':\n        _sha(rec, 'roster_digest', what)\n", '', T_RD),
    # ---- the Mode H batch kind (design 5.1, 5.2, 4.1)
    ('plan: the complete first update not required (admitted version unchecked)', WF,
     "    if last.version != study['admitted']:\n        raise BatchRefused(f'the ledger\\'s last row is version {last.version}; the admitted version is '\n"
     "                           f'{study[\"admitted\"]} (rows beyond it need a study version advance, design 4.1)')\n", '', T_PL),
    ('plan: an update that stops short of holdout_last is accepted', WF,
     "    if last.last_draw < p.holdout_last:", "    if last.last_draw < p.holdout_first:", T_PL),
    ('plan: the closure and environment are not re-checked', WF,
     "        CL.check(study['root'], study['manifest'])\n", "        pass\n", T_PL),
    ('plan: the cohort need not equal the manifest\'s', WF,
     "    if ids(members) != ids(manifest['cohort']):\n        raise BatchRefused('the released cohort differs from the study manifest\\'s cohort')\n", '', T_PL),
    ('plan: a second Mode H plan is allowed', WF,
     "        if OR.batch_id_record(root, game_id) is not None:\n            raise BatchRefused('this game already has its one Mode H plan (the batch-id record exists); a second plan is '\n"
     "                               'not provided')\n", '', T_PL),
    ('plan: an advance before the plan is accepted', WF,
     "    if study['advance'] is not None:\n        raise BatchRefused('a study version advance exists before the plan; the plan must be frozen at v_a')\n", '', T_PL),
    ('run: no DONE ticket written after a CONTINUE-class Mode H run', WF,
     "        if cls == 'CONTINUE' and kind_of(plan) == 'MODE_H_BATCH':\n            _append_closing_ticket(plan, req, 'DONE', f'{res.outcome} {reason_prefix(res.reason)}')\n", '', T_PI),
    ('run: BATCH_COMPLETE written whether or not every pair is done', WF,
     "    if left:\n        echo(f'[WALK-FORWARD] STOP: {left} pair(s) still pending after a complete pass')\n        return 1\n", '', T_PI),
    ('run: lifecycle markers do not stop a run invocation', WF,
     "    if markers:\n        raise BatchRefused(f'the batch is closed: lifecycle marker(s) present: {\", \".join(markers)}')\n", '', T_PI),
    ('resume: an open ticket without a proving run folder is closed DONE', WF,
     "                else:\n                    _append_closing_ticket(plan, req, 'FAILED_TO_START', None)\n                    counts['FAILED_TO_START'] += 1\n",
     "                else:\n                    _append_closing_ticket(plan, req, 'DONE', 'SUCCESS PUBLISHED')\n                    counts['DONE'] += 1\n", T_PI),
    ('Mode H requests carry no binding', WF,
     "        req.update(ledger_version=version, master_sha256=sha,\n                   binding={'kind': 'MODE_H_BATCH', 'batch_id': plan['batch_id'], 'plan_digest': record_digest(plan),\n"
     "                            'run_id': run_id})\n",
     "        req.update(ledger_version=version, master_sha256=sha)\n", T_PI),
    # ---- the dispatch gate's study version advance (slice 2 part; the rest is slice 1's)
    ('gate: an advance tied to another manifest is accepted', CD,
     "                if advance['study_manifest_sha256'] != opening['study_manifest_sha256']:\n"
     "                    refuse('PLAN_NOT_TIED_TO_STUDY', 'the study version advance does not name the opening record\\'s manifest')\n", '', T_PI),
    # ---- the scorer (design 5.2-5.4)
    ('scorer: BATCH_COMPLETE not required', MH,
     "    if 'BATCH_COMPLETE' not in present:\n        raise ModeHRefused('the batch is not complete: no BATCH_COMPLETE marker (design 5.2)')\n", '', T_CLI),
    ('scorer: a sealed study may be scored again', MH,
     "    if 'MODE_H_SEALED' in present:\n        raise ModeHRefused('the Mode H study is sealed; a corrective scoring run is a separately identified run under its '\n"
     "                           'own policy id (design 5.4), not provided by this command')\n", '', T_CLI),
    ('scorer: a resumed attempt with a changed roster is accepted', MH,
     "        if started['roster_digest'] != roster:\n            raise ModeHRefused('the roster differs from the one this attempt started scoring (design 5.2); nothing re-scored')\n", '', T_PI),
    ('scorer: SCORING_STARTED written after the outcome read (the marker and the read swapped)', MH,
     "        OR.write_marker(root, game_id, batch_id, 'SCORING_STARTED',\n",
     "        _late_marker = lambda: OR.write_marker(root, game_id, batch_id, 'SCORING_STARTED',\n", T_PI,
     'applied as: the marker call becomes a deferred lambda that is never called, so the outcome read is attempted without '
     'SCORING_STARTED; the outcome reader must then refuse the holdout targets (freeze-before-outcome, 5.3)'),
    ('scorer: the outcome is re-read when SCORE_COMPLETE exists but the ledger is missing', MH,
     "        if 'SCORE_COMPLETE' in present:\n            raise ModeHRefused('SCORE_COMPLETE exists but the score ledger does not; nothing is re-read')\n", '', T_PI,
     'EQUIVALENT in the suite: with SCORE_COMPLETE present the outcome reader refuses every holdout target (5.3), so the read '
     'fails before any line is written; this check gives the owner the right message first (defence in depth)'),
    ('scorer: an existing report with other bytes is overwritten', MH,
     "            if (report_folder / f'{base}.{ext}').read_bytes() != contents[ext]:\n"
     "                raise ModeHRefused(f'the existing report {base}.{ext} differs from the bytes rebuilt from the accepted '\n"
     "                                   f'lines; nothing is written')\n", '', T_PI),
    ('scorer: the exposure flag not carried into the score lines', MH,
     "                                                 exposure=lambda t: OR.exposure_flag(game_id, t))",
     "                                                 exposure=None)", T_PI),
    ('scorer: the score ledger accepts lines of another schema', MH,
     "    if len(scores) + len(ranks) != len(rows):\n        raise ModeHRefused('the Mode H score ledger holds a line of another schema')\n", '', T_PI,
     'EQUIVALENT in the suite: no test plants a foreign line in the ledger (the ledger is written once by the scorer from '
     'validated records; a hand edit is outside the pipeline test); defence in depth'),
    ('manifest: the holdout already opened does not refuse', MH,
     "        if OR.opening_record(root, game_id) is not None:\n            raise ModeHRefused('the holdout is already opened; the manifest is written before the opening record')\n", '', T_MO),
    ('manifest: the ledger need not end at holdout_first - 1', MH,
     "    if v_f.last_draw != p.holdout_first - 1:", "    if False:", T_MO),
    ('opening record: the ledger need not be at the frozen version', MH,
     "    if (rows[-1].version, rows[-1].master_sha256) != (man['freeze_version'], man['freeze_master_sha256']):",
     "    if False:", T_MO),
    ('owner statements: any text accepted', MH,
     "    if type(given) is not str or given.strip() != expected:\n        raise ModeHRefused('the owner statement must be typed exactly as the design fixes it:\\n  ' + expected)\n", '', T_MO),
    ('developed record: written before the seal', MH,
     "        if rec_id is None or not OR.mode_h_sealed(root, game_id):\n            raise ModeHRefused('the Mode H study is not sealed: GOAL-1 follows the sealed score (design 6.7)')\n",
     "        if rec_id is None:\n            raise ModeHRefused('the Mode H study is not sealed: GOAL-1 follows the sealed score (design 6.7)')\n", T_PI),
    # ---- the freeze-before-outcome rule (design 5.3)
    ('outcome reader: holdout outcomes released without SCORING_STARTED', OC,
     "        if 'BATCH_COMPLETE' not in present or 'SCORING_STARTED' not in present or 'SCORE_COMPLETE' in present:",
     "        if 'BATCH_COMPLETE' not in present or 'SCORE_COMPLETE' in present:", T_RD),
    ('outcome reader: holdout outcomes still released after SCORE_COMPLETE', OC,
     "        if 'BATCH_COMPLETE' not in present or 'SCORING_STARTED' not in present or 'SCORE_COMPLETE' in present:",
     "        if 'BATCH_COMPLETE' not in present or 'SCORING_STARTED' not in present:", T_PI),
    ('outcome reader: the roster digest not compared', OC,
     "        return started['roster_digest'] == OR.roster_digest(repo_root, game_id, plan)", "        return True", T_RD),
    ('outcome reader: a draw after the holdout released by the Mode H rule', OC,
     "    if type(target) is not int or target > p.holdout_last or target < p.holdout_first:\n        return False\n",
     "    if type(target) is not int or target < p.holdout_first:\n        return False\n", T_RD,
     'EQUIVALENT: _check_targets refuses every target above holdout_last before this rule is consulted, and the plan\'s targets '
     'end at holdout_last; defence in depth'),
    ('outcome reader: holdout targets served without the release rule (the request check dropped)', OC,
     "        if t >= p.holdout_first and (repo_root is None or not outcome_release_allowed(repo_root, game_id, t)):",
     "        if False:", T_RD, 'EQUIVALENT: the read loop re-checks outcome_release_allowed on every holdout row it reaches (the second '
                              'guard, line 142) and refuses the same way; the request-level check refuses before any file is opened'),
    ('outcome reader: holdout rows served without the release rule (the read-loop guard dropped)', OC,
     "        if number >= p.holdout_first and not outcome_release_allowed(repo_root, game_id, number):\n"
     "            raise OutcomeRefused('holdout row reached without release')     # a second guard; unreachable by construction\n",
     '', T_RD, 'EQUIVALENT: the request-level check of _check_targets refuses every unreleased holdout target before the read; the '
               'read-loop guard is unreachable by construction (defence in depth)'),
    # ---- the report (design 5.4)
    ('report: a wall-clock field in the Mode H manifest', RW,
     "        manifest.update(generated_utc=None, mode_h={'score_attempt_id': res['attempt_id'],",
     "        manifest.update(generated_utc=CP.utc_now(), mode_h={'score_attempt_id': res['attempt_id'],", T_PI),
    ('report: the study version advance not disclosed', RW,
     "        adv = res.get('advance')\n        if adv is None:\n            w(f\"Admitted master version:",
     "        adv = None\n        if adv is None:\n            w(f\"Admitted master version:", T_PI),
    ('report: the Mode H file name carries no attempt id', RW,
     "    return f\"mode_h_{res['game_id']}_{res['first']}-{res['last']}_{res['attempt_id']}\"",
     "    return f\"mode_h_{res['game_id']}_{res['first']}-{res['last']}\"", T_PI),
    # ---- the process tool (design 6.1, Appendix J)
    ('process tool: an unreadable Python process is CLEAN', PC,
     "        if p.error:\n            p.reasons.append(f'unreadable: {p.error}')\n            listed.append(p)\n            continue\n", "        if p.error:\n            continue\n", T_PC),
    ('process tool: ancestors\' command lines not examined', PC,
     "            q = by_pid.get(q.ppid) if q.ppid is not None else None\n        if p.reasons:", "            q = None\n        if p.reasons:", T_PC),
    ('process tool: the current directory rule dropped', PC,
     "        if p.cwd and _under(p.cwd, str(root)):\n            p.reasons.append('current directory under the project root')\n", '', T_PC),
    ('process tool: clear-updater-lock clears an install\'s lock', PC,
     "    if INSTALL_LOCK.fullmatch(content):\n        out('REFUSED: the updater lock names an install; only the install\\'s own release step or its restore steps '\n"
     "            'remove it (Appendix J)')\n        return 1\n", '', T_PC),
    ('process tool: the install check ignores session locks', PC,
     "            if lock.exists() or lock.is_symlink():\n                raise Refused(f'{g}: a session lock exists ({lock.name}); resume or close that session first')\n", '', T_PC),
    ('process tool: a roster-changing install does not wait for an unfinished set', PC,
     "        if install.get('changes_roster'):", "        if False:", T_PC),
    ('process tool: a resume token is written without a CLEAN check', PC,
     "    if listed:\n        out(f'REFUSED: {len(listed)} project Python process(es) listed above (a human lets each end or closes it through '\n"
     "            f'its own console; this tool never terminates anything)')\n        return 1\n", '', T_PC),
    # ---- the install and release records (design 4.3, Appendix J)
    ('records: the install record needs no barrier', IR,
     "    if not (root / BARRIER_REL).exists():\n        raise Refused('the install barrier P is absent: the install record is written during the install (step 12)')\n", '', T_IR),
    ('records: a release record while P exists', IR,
     "    if (root / BARRIER_REL).exists() or (root / BARRIER_REL).is_symlink():\n        raise Refused('the install barrier P still exists; the release record follows COMMITTED PASS and the removal of E '\n"
     "                      'and P (Appendix J step 16)')\n", '', T_IR),
    ('records: the install record need not be committed', IR,
     "    if not _committed(root, install_rel):\n        raise Refused('the install record is not committed at HEAD with these bytes: the release record follows the '\n"
     "                      'package commit and COMMITTED PASS')\n", '', T_IR),
    ('records: tracked changes tolerated', IR,
     "    if changes:\n        raise Refused('tracked files differ from HEAD; COMMITTED PASS cannot have been reached:\\n  ' + '\\n  '.join(changes))\n", '', T_IR),
    ('records: two release records may name one entry', IR,
     "            if key in seen:\n                raise Refused(f'{r[\"_file\"]} and {seen[key]} both name {key}')\n", '', T_IR),
    ('records: an entry without a registry chain entry is accepted', IR,
     "        if rv not in chains.get((g, m, v), []):\n            raise Refused(f'release record {rec.get(\"package\")}: {g} {m} revision {rv} {v} has no registry chain entry')\n", '', T_IR),
    ('records: a release record may carry an earlier date', IR,
     "    if not is_baseline and abs((d - written).days) > 1:", "    if False:", T_IR),
    ('records: superseded entries stay released', IR,
     "            if e.get('superseded_by'):\n                retired.add(key)\n", '', T_IR),
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
    print('baseline (unmutated) passes:', ok, f'({time.perf_counter() - t0:.0f}s)', flush=True)
    caught = equivalent = 0
    for i, (name, rel, old, new, mods, *note) in enumerate(muts):
        with tempfile.TemporaryDirectory() as td:
            tree = Path(td) / 't'
            copy_tree(tree)
            f = tree / rel
            if isinstance(old, bytes):
                data = f.read_bytes()
                if data.count(old) != 1:
                    print(f'MUTANT NOT APPLIED ({data.count(old)} matches): {name}')
                    continue
                f.write_bytes(data.replace(old, new))
            else:
                text = f.read_text(encoding='utf-8')
                if text.count(old) != 1:
                    print(f'MUTANT NOT APPLIED ({text.count(old)} matches): {name}')
                    continue
                f.write_text(text.replace(old, new), encoding='utf-8')
            passed = run(tree, mods)
            if note and note[0].startswith('EQUIVALENT') and passed:
                equivalent += 1
                print(f'EQUIVALENT [{i}] {name}  ({", ".join(mods)})  -- {note[0]}', flush=True)
                continue
            caught += not passed
            print(('CAUGHT   ' if not passed else 'SURVIVED ') + f'[{i}] ' + name + f'  ({", ".join(mods)})'
                  + (f'  -- {note[0]}' if note else ''), flush=True)
    print(f'{caught} of {len(muts)} mutants caught; {equivalent} equivalent (survive by design, reason given); '
          f'{len(muts) - caught - equivalent} survived')
