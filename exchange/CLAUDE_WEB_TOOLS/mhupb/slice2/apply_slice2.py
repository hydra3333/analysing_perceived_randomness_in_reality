"""MHUP-B slice 2, layer L6: counted edits on top of slice 1's tree (code plan v0.3 section 5 L6; design supplement
v0.8 sections 7.1A, 7.2).

A second plan schema, WF_BATCH_PLAN_V2 (kind ROUTINE_FILL or EXPLORATORY_RERUN, explicit pairs), beside the first,
which keeps its bytes and its rules. Its runs are REAL_DEVELOPMENT, ticketed, bound to the plan (binding kind
DEV_BATCH), published under the development roots only, and admitted by a new branch of the dispatch gate.
Every old string must occur exactly once; the script stops otherwise. Usage: python3 -I apply_slice2.py TREE
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


C = 'src/methods/_common/'
E = 'src/evaluation/'

# ---------------------------------------------------------------- the vocabulary and the request (design 3.4)
edit(C + 'contract_vocab.py', [
    ("BINDING_KINDS = frozenset(('MODE_H_BATCH', 'WEEKLY_SESSION', 'OWNER_DIAGNOSTIC'))",
     "BINDING_KINDS = frozenset(('MODE_H_BATCH', 'WEEKLY_SESSION', 'OWNER_DIAGNOSTIC', 'DEV_BATCH'))   # DEV_BATCH: MHUP-B"),
])
edit(C + 'contract_records.py', [
    ("                   'OWNER_DIAGNOSTIC': ('kind',)}\n",
     "                   'OWNER_DIAGNOSTIC': ('kind',),\n"
     "                   'DEV_BATCH': ('kind', 'batch_id', 'plan_digest', 'run_id')}   # MHUP-B: a plan of the second kind\n"),
    ("    if kind == 'MODE_H_BATCH':\n        _match(BATCH_ID, b['batch_id'], f'{where}.batch_id')\n",
     "    if kind in ('MODE_H_BATCH', 'DEV_BATCH'):\n        _match(BATCH_ID, b['batch_id'], f'{where}.batch_id')\n"),
    ("    elif mode == 'REAL_DEVELOPMENT':\n        if in_prefix:\n",
     "    elif mode == 'REAL_DEVELOPMENT':\n"
     "        if kind == 'DEV_BATCH':\n"
     "            pass      # MHUP-B (supplement v0.8 7.2): a development plan of the second kind may name any target with\n"
     "                      # history; which targets, and under which records, is the dispatch gate's (the DEV_BATCH branch)\n"
     "        elif in_prefix:\n"),
])

# ---------------------------------------------------------------- the version ledger alone (for OV-1's recorder)
edit(C + 'master_versions.py', [
    ("def current_pin(repo_root: Path, game_id: str) -> tuple[int, str]:\n",
     '''def ledger_rows(repo_root: Path, game_id: str) -> list[LedgerRow]:
    """The rows of the game's version ledger alone, its chain parsed and checked. The master itself is not opened
    (MHUP-B: OV-1's recorder needs the current last draw number and pin, and never a draw). Orchestration only."""
    try:
        raw = _trusted_file_bytes(source_paths(repo_root, game_id)[0])
    except ValueError as exc:
        raise LedgerRefused(f'source file: {exc}') from None
    return parse_ledger(raw, game_id)


def current_pin(repo_root: Path, game_id: str) -> tuple[int, str]:
'''),
])

# ---------------------------------------------------------------- the plan's value-free reader
edit(C + 'owner_records.py', [
    ("def plan_lists_pair(plan: Mapping, method_id: str, method_revision: str, variant_id: str, target: int) -> bool:\n",
     '''DEV_PLAN_SCHEMA = 'WF_BATCH_PLAN_V2'
DEV_PLAN_KINDS = ('ROUTINE_FILL', 'EXPLORATORY_RERUN')


def dev_batch_folder(root: Path, game_id: str, batch_id: str) -> Path:
    return Path(root) / 'results' / 'real' / 'development' / 'wf_batches' / game_id / batch_id


def dev_plan(root: Path, game_id: str, batch_id: str) -> dict:
    """A development plan of the second kind (MHUP-B, supplement v0.8 section 7.1A): its kind, its cohort and its
    explicit pairs [method, revision, variant, target], each a pair of a cohort member, none twice."""
    if type(batch_id) is not str or not BATCH_ID.fullmatch(batch_id):
        raise RecordRefused('invalid batch id')
    what = 'development plan'
    plan = _read_canonical_json(dev_batch_folder(root, game_id, batch_id) / 'plan.json', what)
    if plan.get('schema') != DEV_PLAN_SCHEMA or plan.get('batch_id') != batch_id or plan.get('game_id') != game_id:
        raise RecordRefused(f'{what}: wrong schema, batch or game')
    if plan.get('plan_kind') not in DEV_PLAN_KINDS or plan.get('run_mode') != 'REAL_DEVELOPMENT':
        raise RecordRefused(f'{what}: unknown kind, or not a development plan')
    pin_of(plan, what)
    cohort, pairs = plan.get('cohort'), plan.get('pairs')
    if type(cohort) is not list or type(pairs) is not list or not pairs:
        raise RecordRefused(f'{what}: cohort or pairs missing')
    members = {(m.get('method_id'), m.get('method_revision'), m.get('variant_id')) for m in cohort if type(m) is dict}
    seen = set()
    for pair in pairs:
        if (type(pair) is not list or len(pair) != 4 or tuple(pair[:3]) not in members or type(pair[3]) is not int or
                tuple(pair) in seen):
            raise RecordRefused(f'{what}: a pair that is not [method, revision, variant, target] of a member, once')
        seen.add(tuple(pair))
    return plan


def dev_plan_lists_pair(plan: Mapping, method_id: str, method_revision: str, variant_id: str, target: int) -> bool:
    return [method_id, method_revision, variant_id, target] in plan.get('pairs', [])


def search_log_names(root: Path, row_type: str, batch_id: str, plan_digest: str) -> bool:
    """Whether the search log holds a row of this type for this batch and plan digest (value-free; a log that exists
    but is not a plain file refuses)."""
    import csv
    import io
    path = Path(root) / 'results' / 'audit' / 'SEARCH_LOG.csv'
    if absent(path):
        return False
    if not _plain_file(path):
        raise RecordRefused('the search log exists but is not a plain file')
    try:
        rows = list(csv.DictReader(io.StringIO(path.read_bytes().decode('ascii'))))
    except (UnicodeDecodeError, csv.Error):
        raise RecordRefused('the search log does not decode') from None
    return any(r.get('row_type') == row_type and r.get('batch_id') == batch_id and r.get('plan_digest') == plan_digest
               for r in rows)


def session_ticket_for_pair(root: Path, game_id: str, pair: tuple) -> bool:
    """Whether any session's attempts ledger of the game holds a ticket of any kind for this pair."""
    for path in all_session_attempt_paths(root, game_id):
        rows = tickets(path, scope_kind='WEEKLY_SESSION', scope_id=session_id_of_attempts_path(path), game_id=game_id)
        if any(pair_of(t) == pair for t in rows):
            return True
    return False


def plan_lists_pair(plan: Mapping, method_id: str, method_revision: str, variant_id: str, target: int) -> bool:
'''),
])

edit(C + 'release_records.py', [
    ("def released_variants(root: Path) -> dict:\n",
     '''def release_instants(root: Path) -> dict:
    """(game, method, revision, variant) -> the `released_utc` of the release record that names it, for the released,
    unretired entries (MHUP-B, supplement v0.8 section 7.2 rule 2A: back-history is judged by the release instant)."""
    live = released_variants(root)
    out: dict = {}
    for r in validate_records(root)['releases']:
        for e in r['entries']:
            key = _entry(e, r['_file'])
            if key in live:
                out[key] = r['released_utc']
    return out


def released_variants(root: Path) -> dict:
'''),
])

# ---------------------------------------------------------------- the dispatch gate's DEV_BATCH branch (plan L6)
edit(C + 'contract_dispatch.py', [
    ("        elif kind == 'OWNER_DIAGNOSTIC':\n            if mode != 'REAL_DEVELOPMENT':\n",
     '''        elif kind == 'DEV_BATCH':
            # MHUP-B (code plan v0.3 L6; supplement v0.8 7.1A, 7.2). A development plan of the second kind: the plan
            # exists with the digest the binding names and its search-log row, and lists this exact pair; the request
            # pins the plan's pin; an open ticket, and no DONE ticket for the pair in the batch. At or above the
            # holdout: the opening record and the game's seal. Above the holdout: a weekly freeze line for the target
            # (a target still open in the weekly session is never a batch's); and, for a routine fill, rule 2A: that
            # line was frozen before the variant's release instant, does not name the variant, and no session ledger
            # holds a ticket for the pair. Value-free records at fixed roots only.
            plan = OR.dev_plan(root, game, b['batch_id'])
            if record_digest(plan) != b['plan_digest']:
                refuse('BINDING_NOT_RESOLVED', 'the binding does not name the plan\\'s digest')
            if not OR.search_log_names(root, 'DEV_BATCH', b['batch_id'], b['plan_digest']):
                refuse('PLAN_NOT_LOGGED', 'the plan has no search-log row')
            if pin != OR.pin_of(plan, 'development plan'):
                refuse('PIN_DISAGREES_WITH_PLAN', 'the request does not pin the master version the plan froze')
            if not OR.dev_plan_lists_pair(plan, method, revision, variant, target):
                refuse('PAIR_NOT_IN_PLAN', 'the plan does not list this method, revision, variant and target')
            rows = OR.tickets(OR.dev_batch_folder(root, game, b['batch_id']) / 'attempts.jsonl',
                              scope_kind='DEV_BATCH', scope_id=b['batch_id'], game_id=game)
            if OR.pair_has_done_ticket(rows, pair):
                refuse('PAIR_ALREADY_DONE', 'the pair has a DONE ticket in this batch; no second record')
            if not OR.open_ticket_for(rows, run_id=run_id, pair=pair, request_digest=record_digest(request)):
                refuse('NO_OPEN_TICKET', 'no open ticket names this run id, pair and request')
            p = get_profile(game)
            if target >= p.holdout_first:
                if OR.opening_record(root, game) is None:
                    refuse('HOLDOUT_NOT_OPENED', 'a holdout or later development target needs the opening record')
                if not OR.mode_h_sealed(root, game):
                    refuse('MODE_H_NOT_SEALED', 'a holdout or later development target needs the game\\'s Mode H seal')
            if target > p.holdout_last:
                lines = [r for r in OR.forecast_ledger_lines(root, game) if r['target_draw_number'] == target]
                if len(lines) != 1:
                    refuse('TARGET_NOT_FROZEN', 'a target after the holdout is a batch\\'s only once its weekly freeze '
                                                'line exists; an open target is the weekly session\\'s')
                if plan['plan_kind'] == 'ROUTINE_FILL':
                    import _common.release_records as RR
                    try:
                        released = RR.release_instants(root).get((game, method, revision, variant))
                    except (RR.Refused, ValueError, KeyError) as exc:
                        refuse('BINDING_NOT_RESOLVED', f'the release records refuse: {exc}')
                    frozen = lines[0].get('frozen_utc')
                    if type(released) is not str or type(frozen) is not str or \\
                            _instant(frozen) is None or _instant(released) is None:
                        refuse('BINDING_NOT_RESOLVED', 'no release instant for this variant, or no freeze time')
                    if not _instant(frozen) < _instant(released):
                        refuse('FROZEN_AFTER_RELEASE', 'the target was frozen at or after the variant\\'s release instant: '
                                                       'it was the weekly session\\'s (rule 2A)')
                    if any(type(r) is dict and (r.get('method_id'), r.get('method_revision'), r.get('variant_id')) ==
                           (method, revision, variant) for r in lines[0].get('records') or []):
                        refuse('PAIR_HAS_WEEKLY_RECORD', 'the target\\'s freeze line names this variant')
                    if OR.session_ticket_for_pair(root, game, pair):
                        refuse('PAIR_HAS_WEEKLY_TICKET', 'a session ledger holds a ticket for this pair')
        elif kind == 'OWNER_DIAGNOSTIC':
            if mode != 'REAL_DEVELOPMENT':
'''),
    ("def legacy_gate(game_id: str, method_id: str, variant_id: str, revision: str) -> tuple[dict, dict]:\n",
     '''def _instant(text: str):
    """A UTC instant written as the records write it, or None."""
    from datetime import datetime, timezone
    for fmt in ('%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ'):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def legacy_gate(game_id: str, method_id: str, variant_id: str, revision: str) -> tuple[dict, dict]:
'''),
])

# ---------------------------------------------------------------- the runner: the root and the mode-to-pin rule
edit(C + 'contract_runner.py', [
    ("    if kind == 'WEEKLY_SESSION':\n        return OR.session_runs_root(PROJECT_ROOT, request.get('run_mode'))\n",
     "    if kind == 'WEEKLY_SESSION':\n        return OR.session_runs_root(PROJECT_ROOT, request.get('run_mode'))\n"
     "    if kind == 'DEV_BATCH':                              # MHUP-B: a plan of the second kind writes under the\n"
     "        return OR.development_runs_root(PROJECT_ROOT)     # development run root only (supplement v0.8 7.2 rule 5)\n"),
    ("    if mode not in V.WEEKLY_MODES and kind not in ('WEEKLY_SESSION', 'OWNER_DIAGNOSTIC'):\n",
     "    if mode not in V.WEEKLY_MODES and kind not in ('WEEKLY_SESSION', 'OWNER_DIAGNOSTIC', 'DEV_BATCH'):\n"),
])

# ---------------------------------------------------------------- the driver: WF_BATCH_PLAN_V2
edit(C + 'walk_forward.py', [
    ("  <project>/results/real/holdout/<GAME>/MODE_H_BATCH_ID.json          the game's one plan (create-only)\n\"\"\"\n",
     "  <project>/results/real/holdout/<GAME>/MODE_H_BATCH_ID.json          the game's one plan (create-only)\n"
     "\n"
     "MHUP-B adds plans of the second kind, WF_BATCH_PLAN_V2 (design supplement v0.8 sections 7.1A, 7.2; code plan v0.3\n"
     "L6): `make_dev_plan` freezes a ROUTINE_FILL (the driver works out the missing pairs from the league's source list)\n"
     "or an EXPLORATORY_RERUN (the owner names variants and window), each with its explicit pairs. Its runs are\n"
     "REAL_DEVELOPMENT, bound to the plan (binding kind DEV_BATCH), ticketed like the Mode H batch's, and published under\n"
     "the development roots above, beside the first kind's. Plans of the first kind keep their schema, bytes and rules.\n"
     "\"\"\"\n"),
    ("DRIVER_VERSION = 'WF1A_DRIVER_V2'            # MHUP-A: the Mode H batch kind\n",
     "DRIVER_VERSION = 'WF1A_DRIVER_V3'            # MHUP-A: the Mode H batch kind; MHUP-B: plans of the second kind\n"),
    ("MODE_H_PLAN_SCHEMA = OR.MODE_H_PLAN_SCHEMA\nKINDS = ('WF_BATCH', 'MODE_H_BATCH')\n",
     "MODE_H_PLAN_SCHEMA = OR.MODE_H_PLAN_SCHEMA\n"
     "DEV_PLAN_SCHEMA = OR.DEV_PLAN_SCHEMA         # MHUP-B: WF_BATCH_PLAN_V2 (supplement v0.8 7.1A); V1 plans are untouched\n"
     "KINDS = ('WF_BATCH', 'MODE_H_BATCH', 'DEV_BATCH')\n"
     "TICKETED = ('MODE_H_BATCH', 'DEV_BATCH')     # kinds whose runs are bound to the plan and ticketed (design 3.4)\n"),
    ("    if kind != 'WF_BATCH':\n        raise ValueError(f'unknown batch kind {kind!r}')\n",
     "    if kind not in ('WF_BATCH', 'DEV_BATCH'):               # both development kinds share the development roots\n"
     "        raise ValueError(f'unknown batch kind {kind!r}')\n"),
    ("def kind_of(plan: Mapping) -> str:\n    return 'MODE_H_BATCH' if plan.get('schema') == MODE_H_PLAN_SCHEMA else 'WF_BATCH'\n",
     '''def kind_of(plan: Mapping) -> str:
    schema = plan.get('schema')
    return 'MODE_H_BATCH' if schema == MODE_H_PLAN_SCHEMA else 'DEV_BATCH' if schema == DEV_PLAN_SCHEMA else 'WF_BATCH'


def plan_pairs(plan: Mapping) -> list[tuple[dict, int]]:
    """Every (member, target) pair of a plan, in run order: a plan of the first kind and the Mode H plan run their
    whole cohort over their window; a plan of the second kind runs exactly the pairs it lists."""
    if kind_of(plan) == 'DEV_BATCH':
        members = {(m['method_id'], m['method_revision'], m['variant_id']): m for m in plan['cohort']}
        return [(members[(m, rev, v)], t) for m, rev, v, t in plan['pairs']]
    return [(mem, t) for mem in plan['cohort'] for t in range(plan['window_first'], plan['window_last'] + 1)]
'''),
    ("# ---------------------------------------------------------------- the Mode H batch kind (MHUP-A, design 4.1, 5.1, 5.2)\n",
     '''# ---------------------------------------------------------------- plans of the second kind (MHUP-B, supplement 7.1A)

def development_cap(game_id: str) -> int:
    """The last draw a development batch may target under the window contract (supplement v0.8 7.2 rules 1 and 2):
    the Phase 1 cap until the game's Mode H study is sealed, the holdout's last draw after it."""
    p = get_profile(game_id)
    root = roots()['project']
    try:
        sealed = OR.opening_record(root, game_id) is not None and OR.mode_h_sealed(root, game_id)
    except OR.RecordRefused as exc:
        raise BatchRefused(f'owner record refused: {exc}') from None
    return p.holdout_last if sealed else p.holdout_first - 1


def _weekly_facts(game_id: str) -> tuple[dict, dict]:
    """(target -> verified weekly freeze line, (game, method, revision, variant) -> release instant). Value-free."""
    import _common.release_records as RR
    from _common import weekly_records as WR
    root = roots()['project']
    try:
        lines = {line['target_draw_number']: line for line in WR.forecast_ledger(root, game_id)}
        instants = RR.release_instants(root)
    except (OR.RecordRefused, RR.Refused, ValueError, KeyError) as exc:
        raise BatchRefused(f'the weekly or release records refuse: {exc}') from None
    return lines, instants


def _fill_pairs(game_id: str, members, cap: int, last_draw: int) -> list[list]:
    """A routine fill's pairs, worked out by the driver (plan L6): for every released variant, its eligible targets
    that no canonical source covers. Eligible: the game's first target to the cap; and, above the holdout, rule 2A:
    an accepted target whose weekly freeze line was frozen before the variant's release instant, does not name the
    variant, and for which no session ledger holds a ticket."""
    from _common import score_identities as SI
    from _common import weekly_records as WR
    p = get_profile(game_id)
    root = roots()['project']
    try:
        covered = SI.canonical_coverage(root, game_id)
    except OR.RecordRefused as exc:
        raise BatchRefused(f'the league\\'s source list refuses: {exc}') from None
    lines, instants = _weekly_facts(game_id) if cap == p.holdout_last and last_draw > p.holdout_last else ({}, {})
    pairs = []
    for mem in members:
        key = (mem['method_id'], mem['method_revision'], mem['variant_id'])
        for t in range(p.first_draw + 1, cap + 1):
            if (*key, t) not in covered:
                pairs.append([*key, t])
        released = instants.get((game_id, *key))
        for t in sorted(lines):
            if t > last_draw or (*key, t) in covered or released is None:
                continue
            line = lines[t]
            try:
                weekly = (WR.parse_utc(line['frozen_utc']) >= WR.parse_utc(released) or
                          any(WR.named_key(r) == key for r in line['records']) or
                          OR.session_ticket_for_pair(root, game_id, (*key, t)))
            except OR.RecordRefused as exc:
                raise BatchRefused(f'the weekly records refuse: {exc}') from None
            if not weekly:
                pairs.append([*key, t])
    return pairs


def make_dev_plan(game_id: str, plan_kind: str, adapters: Mapping, *, variants=None, first=None, last=None) -> dict:
    """Freeze a plan of the second kind (create-only) and append one DEV_BATCH search-log row.

    ROUTINE_FILL: the owner names only the game; the driver works out the missing pairs (see _fill_pairs).
    EXPLORATORY_RERUN: the owner names the window and, optionally, the variants as (method_id, variant_id) pairs (the
    whole released cohort otherwise). Any target up to the cap, and any later accepted target that has a weekly freeze
    line, whether or not it was scored before. A window that reaches a target outside those refuses.
    Either kind runs only released, runnable variants (a retired revision is not runnable), gives development evidence
    only, and writes only under the development roots."""
    from _common import master_versions as MV
    p = get_profile(game_id)
    if _marker_present():
        raise BatchRefused('UNRESOLVED_ORPHAN_MARKER: no experiment is permitted')
    if plan_kind not in OR.DEV_PLAN_KINDS:
        raise BatchRefused(f'the plan kind is one of {", ".join(OR.DEV_PLAN_KINDS)}')
    members, excluded = cohort(game_id, adapters)
    if not members:
        raise BatchRefused('the cohort is empty: no released variant with a runner adapter')
    version, pin = ledger_pin(game_id)
    try:
        last_draw = MV.load_verified_source(roots()['project'], game_id)[1][-1].last_draw
    except MV.LedgerRefused as exc:
        raise BatchRefused(f'{game_id}: the master ledger does not pass the version-2 rules: {exc}') from None
    cap = development_cap(game_id)
    if plan_kind == 'ROUTINE_FILL':
        if variants is not None or first is not None or last is not None:
            raise BatchRefused('a routine fill works out its own pairs: it takes no variants and no window')
        pairs = _fill_pairs(game_id, members, cap, last_draw)
        if not pairs:
            raise BatchRefused('nothing to fill: every eligible pair of every released variant is covered')
    else:
        if type(first) is not int or type(last) is not int or first > last:
            raise BatchRefused('an exploratory rerun needs a window: two whole draw numbers, first <= last')
        if first < p.first_draw + 1:
            raise BatchRefused(f'first must be at least {p.first_draw + 1}: the era\\'s first draw has no history')
        if last > last_draw:
            raise BatchRefused(f'last must be an accepted draw (the master ends at {last_draw})')
        chosen = members
        if variants is not None:
            wanted = [tuple(v) for v in variants]
            by_name = {(m['method_id'], m['variant_id']): m for m in members}
            unknown = [f'{m} {v}' for m, v in wanted if (m, v) not in by_name]
            if unknown or not wanted or len(set(wanted)) != len(wanted):
                raise BatchRefused('not released, runnable variants of this game (or named twice): ' + ', '.join(unknown))
            chosen = [by_name[w] for w in sorted(set(wanted), key=lambda k: (int(k[0][2:]), k[1]))]
        lines = _weekly_facts(game_id)[0] if last > p.holdout_last else {}
        for t in range(first, last + 1):
            if cap < t <= p.holdout_last:
                raise BatchRefused(f'target {t} is a holdout draw and the game\\'s Mode H study is not sealed')
            if t > p.holdout_last and (cap != p.holdout_last or t not in lines):
                raise BatchRefused(f'target {t} is after the holdout and has no weekly freeze line: it is the weekly '
                                   f'session\\'s, not a batch\\'s')
        pairs = [[m['method_id'], m['method_revision'], m['variant_id'], t] for m in chosen for t in range(first, last + 1)]
        members = chosen
    used = {tuple(pair[:3]) for pair in pairs}
    members = [m for m in members if (m['method_id'], m['method_revision'], m['variant_id']) in used]
    batch_id = 'wf-' + uuid.uuid4().hex
    targets = [pair[3] for pair in pairs]
    plan = {'schema': DEV_PLAN_SCHEMA, 'plan_kind': plan_kind, 'batch_id': batch_id, 'game_id': game_id,
            'profile_version': p.version, 'window_first': min(targets), 'window_last': max(targets),
            'created_utc': utc_now(), 'driver_version': DRIVER_VERSION, 'run_mode': 'REAL_DEVELOPMENT',
            'product_kind': V.producible('REAL_DEVELOPMENT', V.FORECAST)[0], 'observation_view': VIEW,
            'include_dates': False, 'master_file': f'{game_id}_results_master.csv', 'ledger_version': version,
            'master_sha256': pin, 'development_cap': cap, 'cohort': members, 'not_in_cohort': excluded,
            'cohort_digest': sha256_hex(canonical({'cohort': members})), 'pairs': pairs,
            'pairs_digest': sha256_hex(canonical({'pairs': pairs}))}
    folder = roots('DEV_BATCH')['batches'] / game_id / batch_id
    folder.mkdir(parents=True, exist_ok=False)
    CP.create_only(folder / 'plan.json', canonical(plan))
    _append_search_row({'row_type': 'DEV_BATCH', 'utc': plan['created_utc'], 'game_id': game_id, 'mode': 'WF',
                        'window_first': plan['window_first'], 'window_last': plan['window_last'],
                        'cohort_size': len(members), 'cohort_digest': plan['cohort_digest'], 'batch_id': batch_id,
                        'plan_digest': record_digest(plan), 'tool': 'Method_Walk_Forward.py',
                        'tool_version': DRIVER_VERSION, 'tool_sha256': tool_sha256()})
    return plan


# ---------------------------------------------------------------- the Mode H batch kind (MHUP-A, design 4.1, 5.1, 5.2)
'''),
    ("    plan = json.loads(path.read_bytes().decode('ascii'))\n    if (plan.get('schema') != schema or",
     "    plan = json.loads(path.read_bytes().decode('ascii'))\n"
     "    if kind == 'WF_BATCH' and type(plan) is dict and plan.get('schema') == DEV_PLAN_SCHEMA:      # the second kind\n"
     "        kind, schema, row_type = 'DEV_BATCH', DEV_PLAN_SCHEMA, 'DEV_BATCH'\n"
     "    if (plan.get('schema') != schema or"),
    ("        if plan.get('targets') != list(range(plan['window_first'], plan['window_last'] + 1)):\n"
     "            raise BatchRefused('the Mode H plan\\'s targets are not its window')\n",
     "        if plan.get('targets') != list(range(plan['window_first'], plan['window_last'] + 1)):\n"
     "            raise BatchRefused('the Mode H plan\\'s targets are not its window')\n"
     "    if kind == 'DEV_BATCH':\n"
     "        try:\n"
     "            OR.dev_plan(roots(kind)['project'], game_id, batch_id)        # its kind, its pin, its explicit pairs\n"
     "        except OR.RecordRefused as exc:\n"
     "            raise BatchRefused(f'not a valid plan of the second kind: {exc}') from None\n"
     "        if plan.get('pairs_digest') != sha256_hex(canonical({'pairs': plan['pairs']})):\n"
     "            raise BatchRefused('the plan\\'s pairs do not match their digest')\n"),
    ("    if kind_of(plan) == 'MODE_H_BATCH':\n        version, sha = _admitted_pin(plan)\n",
     "    if kind_of(plan) == 'DEV_BATCH':\n"
     "        req['binding'] = {'kind': 'DEV_BATCH', 'batch_id': plan['batch_id'], 'plan_digest': record_digest(plan),\n"
     "                          'run_id': run_id}\n"
     "    if kind_of(plan) == 'MODE_H_BATCH':\n        version, sha = _admitted_pin(plan)\n"),
    ("    if kind_of(plan) == 'MODE_H_BATCH':\n        t = OR.ticket('OPEN', scope_kind='MODE_H_BATCH', scope_id=plan['batch_id'], game_id=plan['game_id'],\n",
     "    if kind_of(plan) in TICKETED:\n        t = OR.ticket('OPEN', scope_kind=kind_of(plan), scope_id=plan['batch_id'], game_id=plan['game_id'],\n"),
    ("    t = OR.ticket(kind, scope_kind='MODE_H_BATCH', scope_id=plan['batch_id'], game_id=plan['game_id'],\n",
     "    t = OR.ticket(kind, scope_kind=kind_of(plan), scope_id=plan['batch_id'], game_id=plan['game_id'],\n"),
    ("        return OR.tickets(_attempts_path(plan), scope_kind='MODE_H_BATCH', scope_id=plan['batch_id'],\n",
     "        return OR.tickets(_attempts_path(plan), scope_kind=kind_of(plan), scope_id=plan['batch_id'],\n"),
    ("    members = {(m['method_id'], m['variant_id']): m for m in plan['cohort']}\n    out, bad = {}, 0\n    for t in _mode_h_tickets(plan):\n",
     "    members = {(m['method_id'], m['variant_id']): m for m in plan['cohort']}\n"
     "    planned = {(mem['method_id'], mem['variant_id'], target) for mem, target in plan_pairs(plan)}\n"
     "    out, bad = {}, 0\n    for t in _mode_h_tickets(plan):\n"),
    ("        if (mem is None or mem['method_revision'] != t['method_revision'] or target not in plan['targets'] or\n",
     "        if (mem is None or mem['method_revision'] != t['method_revision'] or\n"
     "                (t['method_id'], t['variant_id'], target) not in planned or\n"),
    ("    if kind_of(plan) != 'MODE_H_BATCH':\n        return {}\n",
     "    if kind_of(plan) not in TICKETED:\n        return {}\n"),
    ("    counts = {'DONE': 0, 'FAILED_TO_START': 0}\n    for mem in plan['cohort']:\n        decl = reg.declaration(mem['declaration_digest'])\n        for target in plan['targets']:\n            for rid in attempts.get((mem['method_id'], mem['variant_id'], target), ()):\n                if rid in closed:\n                    continue\n                state, why = attempt_state(plan, mem, target, rid, decl)\n                req = request_for(plan, mem, target, rid)\n                if state == 'DONE':\n                    _append_closing_ticket(plan, req, 'DONE', why.split(' (', 1)[0])\n                    counts['DONE'] += 1\n                else:\n                    _append_closing_ticket(plan, req, 'FAILED_TO_START', None)\n                    counts['FAILED_TO_START'] += 1\n                closed.add(rid)\n",
     "    counts = {'DONE': 0, 'FAILED_TO_START': 0}\n    for mem, target in plan_pairs(plan):\n        decl = reg.declaration(mem['declaration_digest'])\n        for rid in attempts.get((mem['method_id'], mem['variant_id'], target), ()):\n            if rid in closed:\n                continue\n            state, why = attempt_state(plan, mem, target, rid, decl)\n            req = request_for(plan, mem, target, rid)\n            if state == 'DONE':\n                _append_closing_ticket(plan, req, 'DONE', why.split(' (', 1)[0])\n                counts['DONE'] += 1\n            else:\n                _append_closing_ticket(plan, req, 'FAILED_TO_START', None)\n                counts['FAILED_TO_START'] += 1\n            closed.add(rid)\n"),
    ("    if kind_of(plan) == 'MODE_H_BATCH':\n        return _mode_h_attempts(plan)\n",
     "    if kind_of(plan) in TICKETED:\n        return _mode_h_attempts(plan)\n"),
    ("    out = {}\n    for mem in plan['cohort']:\n        decl = reg.declaration(mem['declaration_digest'])\n        for target in range(plan['window_first'], plan['window_last'] + 1):\n            key = (mem['method_id'], mem['variant_id'], target)\n            done = any(attempt_state(plan, mem, target, rid, decl)[0] == 'DONE' for rid in attempts.get(key, ()))\n            out[key] = 'DONE' if done else 'NOT_DONE'\n    return out, bad\n",
     "    out = {}\n    for mem, target in plan_pairs(plan):\n        decl = reg.declaration(mem['declaration_digest'])\n        key = (mem['method_id'], mem['variant_id'], target)\n        done = any(attempt_state(plan, mem, target, rid, decl)[0] == 'DONE' for rid in attempts.get(key, ()))\n        out[key] = 'DONE' if done else 'NOT_DONE'\n    return out, bad\n"),
    ("    return [(mem, t) for mem in plan['cohort'] for t in range(plan['window_first'], plan['window_last'] + 1)\n            if states[(mem['method_id'], mem['variant_id'], t)] != 'DONE']\n",
     "    return [(mem, t) for mem, t in plan_pairs(plan) if states[(mem['method_id'], mem['variant_id'], t)] != 'DONE']\n"),
    ("        if cls == 'CONTINUE' and kind_of(plan) == 'MODE_H_BATCH':\n",
     "        if cls == 'CONTINUE' and kind_of(plan) in TICKETED:\n"),
    ("        done, made, why = 0, 0, {}\n        for target in range(plan['window_first'], plan['window_last'] + 1):\n",
     "        done, made, why = 0, 0, {}\n        mine = [t for m, t in plan_pairs(plan) if m is mem]\n        for target in mine:\n"),
    ("        n = plan['window_last'] - plan['window_first'] + 1\n", "        n = len(mine)\n"),
])

# ---------------------------------------------------------------- the canonical-coverage reader (identities only)
edit(C + 'score_identities.py', [
    ("def routine_identity(game_id: str, target: int, named: Mapping) -> tuple:\n",
     '''# ---------------------------------------------------------------- which keys the league's canonical sources cover

LEAGUE_SOURCES_SCHEMA = 'LEAGUE_SOURCES_V1'
LEAGUE_SOURCE_FIELDS = ('attempt_id', 'batch_id', 'batch_kind', 'plan_digest', 'window_first', 'window_last',
                        'score_ledger_sha256', 'evaluator_version')
LEAGUE_SOURCE_KINDS = ('WF_BATCH_PLAN_V1', 'ROUTINE_FILL')          # an exploratory rerun is never a canonical source


def league_sources_path(root: Path, game_id: str) -> Path:
    return Path(root) / 'results' / 'method_rankings' / game_id / 'league' / f'LEAGUE_SOURCES_{game_id}.json'


def league_sources(root: Path, game_id: str) -> list[dict]:
    """The canonical development attempts listed in LEAGUE_SOURCES_<GAME>.json (supplement v0.8 section 4; the file
    is written only by the league's admission step, layer L4). A file never written lists nothing; a file that is
    not exactly a source list refuses."""
    import json
    from _common.contract_records import canonical
    path = league_sources_path(root, game_id)
    if OR.absent(path):
        return []
    if path.is_symlink() or not path.is_file():
        raise OR.RecordRefused('league sources: exists but is not a plain file')
    raw = path.read_bytes()
    try:
        rec = json.loads(raw.decode('ascii'))
    except (ValueError, UnicodeDecodeError):
        raise OR.RecordRefused('league sources: not JSON') from None
    if (type(rec) is not dict or canonical(rec) != raw or set(rec) != {'schema', 'game_id', 'sources'} or
            rec['schema'] != LEAGUE_SOURCES_SCHEMA or rec['game_id'] != game_id or type(rec['sources']) is not list):
        raise OR.RecordRefused('league sources: not a canonical LEAGUE_SOURCES_V1 record of this game')
    seen = set()
    for s in rec['sources']:
        if (type(s) is not dict or set(s) != set(LEAGUE_SOURCE_FIELDS) or s['batch_kind'] not in LEAGUE_SOURCE_KINDS or
                type(s['batch_id']) is not str or not OR.BATCH_ID.fullmatch(s['batch_id']) or
                not all(type(s[f]) is str and V.SHA256.fullmatch(s[f]) for f in ('plan_digest', 'score_ledger_sha256')) or
                not all(type(s[f]) is int for f in ('window_first', 'window_last')) or
                s['window_first'] > s['window_last'] or type(s['attempt_id']) is not str or s['attempt_id'] in seen):
            raise OR.RecordRefused('league sources: an entry of an unknown shape, or an attempt listed twice')
        seen.add(s['attempt_id'])
    return rec['sources']


def canonical_coverage(root: Path, game_id: str) -> frozenset:
    """Every (method, revision, variant, target) key that a canonical development source covers: for each listed
    attempt, the pairs of its batch's plan inside the attempt's window. Identities only: it reads the source list and
    the plans, never a score record, an outcome or a forecast. A listed batch whose plan is gone or changed refuses."""
    import _common.walk_forward as WF
    from _common.contract_records import record_digest
    out = set()
    for s in league_sources(root, game_id):
        try:
            plan = WF.load_plan(game_id, s['batch_id'])
        except WF.BatchRefused as exc:
            raise OR.RecordRefused(f'league sources: the plan of {s["batch_id"]} does not load: {exc}') from None
        kind = plan['plan_kind'] if WF.kind_of(plan) == 'DEV_BATCH' else 'WF_BATCH_PLAN_V1'
        if WF.kind_of(plan) == 'MODE_H_BATCH' or kind != s['batch_kind'] or record_digest(plan) != s['plan_digest']:
            raise OR.RecordRefused(f'league sources: {s["batch_id"]} is not the plan the list names')
        for mem, t in WF.plan_pairs(plan):
            if s['window_first'] <= t <= s['window_last']:
                out.add((mem['method_id'], mem['method_revision'], mem['variant_id'], t))
    return frozenset(out)


def routine_identity(game_id: str, target: int, named: Mapping) -> tuple:
'''),
])

# ---------------------------------------------------------------- the report tool: V2 batches on their own pairs
edit(E + 'collect.py', [
    ("    e = get_profile(plan['game_id']).first_draw\n    need = max(1, member['minimum_history_draws'])\n"
     "    return [n for n in range(first, last + 1) if n - e >= need]\n",
     "    e = get_profile(plan['game_id']).first_draw\n    need = max(1, member['minimum_history_draws'])\n"
     "    if WF.kind_of(plan) == 'DEV_BATCH':                    # MHUP-B: a plan of the second kind is reported on its own pairs\n"
     "        mine = sorted(t for mem, t in WF.plan_pairs(plan)\n"
     "                      if (mem['method_id'], mem['variant_id']) == (member['method_id'], member['variant_id']))\n"
     "        return [n for n in mine if first <= n <= last and n - e >= need]\n"
     "    return [n for n in range(first, last + 1) if n - e >= need]\n"),
])
edit(E + 'outcome_reader.py', [
    ("def _weekly_release_allowed(repo_root: Path, game_id: str, target: int) -> bool:\n",
     '''def development_release_allowed(repo_root: Path, game_id: str, target: int) -> bool:
    """The post-seal development rule (MHUP-B; supplement v0.8 section 7.2 rules 1, 2 and 2A; code plan CF-4; an
    always-review subject). Decides whether the outcome of a holdout or later draw may be served to a DEVELOPMENT
    report: only when the game's opening record exists and its Mode H study is SEALED (the sealed study is never
    reopened: this reads the master, not the study); and, for a draw after the holdout, only when the weekly
    freeze-line rule also releases it (the developed record, a verified freeze line for the draw, the draw accepted).
    Fixed evidence paths under the root; anything invalid or absent refuses (False)."""
    import _common.owner_records as OR
    p = get_profile(game_id)
    if type(target) is not int or target < p.holdout_first:
        return False
    try:
        if OR.opening_record(repo_root, game_id) is None or not OR.mode_h_sealed(repo_root, game_id):
            return False
    except OR.RecordRefused:
        return False
    return target <= p.holdout_last or _weekly_release_allowed(repo_root, game_id, target)


def _weekly_release_allowed(repo_root: Path, game_id: str, target: int) -> bool:
'''),
    ("def _check_targets(game_id: str, targets, repo_root: Path | None = None) -> list[int]:\n",
     "def _check_targets(game_id: str, targets, repo_root: Path | None = None, released=None) -> list[int]:\n"
     "    released = released or outcome_release_allowed\n"),
    ("        if t >= p.holdout_first and (repo_root is None or not outcome_release_allowed(repo_root, game_id, t)):\n",
     "        if t >= p.holdout_first and (repo_root is None or not released(repo_root, game_id, t)):\n"),
    ("def read_outcomes(*, repo_root: Path, game_id: str, master_sha256: str, targets, ledger_version: int = 1) -> dict:\n",
     "def read_outcomes(*, repo_root: Path, game_id: str, master_sha256: str, targets, ledger_version: int = 1,\n"
     "                  development: bool = False) -> dict:\n"),
    ("    rows = read_outcome_rows(repo_root=repo_root, game_id=game_id, master_sha256=master_sha256, targets=targets,\n"
     "                             ledger_version=ledger_version)\n",
     "    rows = read_outcome_rows(repo_root=repo_root, game_id=game_id, master_sha256=master_sha256, targets=targets,\n"
     "                             ledger_version=ledger_version, development=development)\n"),
    ("def read_outcome_rows(*, repo_root: Path, game_id: str, master_sha256: str, targets, ledger_version: int = 1) -> dict:\n",
     "def read_outcome_rows(*, repo_root: Path, game_id: str, master_sha256: str, targets, ledger_version: int = 1,\n"
     "                      development: bool = False) -> dict:\n"),
    ("    wanted = _check_targets(game_id, targets, repo_root)\n",
     "    # `development=True` is the development report's call (MHUP-B): holdout and later draws are then released by the\n"
     "    # post-seal development rule, not by the Mode H scorer's or the weekly scorer's rule.\n"
     "    released = development_release_allowed if development else outcome_release_allowed\n"
     "    wanted = _check_targets(game_id, targets, repo_root, released)\n"),
    ("        if number >= p.holdout_first and not outcome_release_allowed(repo_root, game_id, number):\n",
     "        if number >= p.holdout_first and not released(repo_root, game_id, number):\n"),
])
edit(E + 'report.py', [
    ("def load_families(game_id: str, first: int, last: int) -> list[dict]:\n"
     "    \"\"\"The registered families that apply: same game and exactly the family's window (design 6.7).\"\"\"\n",
     "def load_families(game_id: str, first: int, last: int, tier: str | None = None) -> list[dict]:\n"
     "    \"\"\"The registered families that apply: same game and exactly the family's window (design 6.7). With `tier`\n"
     "    (MHUP-B, code plan CF-5): only the families registered for that evidence tier, so a development report never\n"
     "    takes a Mode H family (a family without a tier field is a development family). The Mode H scorer calls this\n"
     "    without a tier, as before.\"\"\"\n"),
    ("    return [f for f in reg['families'] if f['game_id'] == game_id and (f['window_first'], f['window_last']) == (first, last)]\n",
     "    return [f for f in reg['families'] if f['game_id'] == game_id and (f['window_first'], f['window_last']) == (first, last)\n"
     "            and (tier is None or (f.get('evidence_tier') or 'DEVELOPMENT_WF_EXPLORATORY') == tier)]\n"),
    ("    if last > p.holdout_first - 1:\n        raise ReportRefused(f'last must be at most {p.holdout_first - 1} for a development report (R3 17.3.6; MRT-14); '\n                            f'the Mode H batch is scored once by Method_Mode_H.py score (design 5.4)')\n    try:\n        plan = WF.load_plan(game_id, batch_id)\n    except WF.BatchRefused as exc:\n        raise ReportRefused(f'unknown or altered batch: {exc}') from None\n    if WF.kind_of(plan) != 'WF_BATCH':\n        raise ReportRefused('this tool reports development batches only; the Mode H batch is scored by Method_Mode_H.py')\n    if first < plan['window_first'] - (1 if plan['window_first'] == p.first_draw + 1 else 0) or last > plan['window_last']:\n        raise ReportRefused(f\"the window [{first}, {last}] is outside the batch's window \"\n                            f\"[{plan['window_first']}, {plan['window_last']}]\")\n    families = load_families(game_id, first, last)\n",
     "    try:\n        plan = WF.load_plan(game_id, batch_id)\n    except WF.BatchRefused as exc:\n        raise ReportRefused(f'unknown or altered batch: {exc}') from None\n    if WF.kind_of(plan) == 'MODE_H_BATCH':\n        raise ReportRefused('this tool reports development batches only; the Mode H batch is scored by Method_Mode_H.py')\n    second_kind = WF.kind_of(plan) == 'DEV_BATCH'\n    if not second_kind and last > p.holdout_first - 1:\n        raise ReportRefused(f'last must be at most {p.holdout_first - 1} for a development report (R3 17.3.6; MRT-14); '\n                            f'the Mode H batch is scored once by Method_Mode_H.py score (design 5.4)')\n    if first < plan['window_first'] - (1 if plan['window_first'] == p.first_draw + 1 else 0) or last > plan['window_last']:\n        raise ReportRefused(f\"the window [{first}, {last}] is outside the batch's window \"\n                            f\"[{plan['window_first']}, {plan['window_last']}]\")\n    if second_kind:\n        # MHUP-B (supplement v0.8 7.2; code plan L6): a plan of the second kind is reported on its own pairs. A holdout\n        # or later target is read only under the post-seal development rule; that is checked here, before the\n        # search-log row, from value-free records, so a refused window appends nothing. No registered family applies:\n        # every table of such a report is EXPLORATORY_COHORT.\n        for t in sorted({t for _mem, t in WF.plan_pairs(plan) if first <= t <= last and t >= p.holdout_first}):\n            if not OR.development_release_allowed(roots()['project'], game_id, t):\n                raise ReportRefused(f'target {t} is not released to a development report (the game\\'s Mode H seal; and, '\n                                    f'after the holdout, the weekly freeze line: supplement 7.2)')\n        families = []\n    else:\n        families = load_families(game_id, first, last, tier='DEVELOPMENT_WF_EXPLORATORY')\n"),
    ("                    'receipt_selection_policy': 'EARLIEST_FROZEN_AT_UTC_EQUAL_CONTENT_DIGESTS'}\n    sp_digest = record_digest(scoring_plan)\n",
     "                    'receipt_selection_policy': 'EARLIEST_FROZEN_AT_UTC_EQUAL_CONTENT_DIGESTS'}\n"
     "    if second_kind:\n"
     "        scoring_plan['plan_kind'] = plan['plan_kind']\n"
     "    sp_digest = record_digest(scoring_plan)\n"),
    ("                                targets=targets, ledger_version=plan['ledger_version']) if targets else {}\n",
     "                                targets=targets, ledger_version=plan['ledger_version'],\n"
     "                                development=True) if targets else {}\n"),
    ("    progress('measures done; writing the report')\n    return {'plan': plan,",
     "    progress('measures done; writing the report')\n"
     "    from . import reforecast_compare as RC\n"
     "    sealed = RC.sealed_comparison(game_id, plan, collected, first, last) if second_kind else None   # reads only (rule 7)\n"
     "    return {'sealed_comparison': sealed, 'plan': plan,"),
])
edit(E + 'report_writer.py', [
    ("    w('Track counts by status: ' + ', '.join(f'{k} {v}' for k, v in sorted(status_counts.items())))\n",
     "    if plan.get('schema') == 'WF_BATCH_PLAN_V2':\n"
     "        w(f\"Plan kind: {plan['plan_kind']} ({len(plan['pairs'])} planned pairs, each named in the plan). Development \"\n"
     "          'evidence only: no figure here is catch-up, prospective or Mode H evidence, and repeated runs of a draw are '\n"
     "          'never added together or treated as independent observations.')\n"
     "    w('Track counts by status: ' + ', '.join(f'{k} {v}' for k, v in sorted(status_counts.items())))\n"),
    ("    text = ('\\n'.join(L_) + '\\n').encode('ascii', errors='replace')\n",
     "    if res.get('sealed_comparison') is not None:\n"
     "        from . import reforecast_compare as RC\n"
     "        for line in RC.section_lines(res['sealed_comparison']):\n"
     "            w(line)\n"
     "    text = ('\\n'.join(L_) + '\\n').encode('ascii', errors='replace')\n"),
    ("    if mode_h:\n        adv = res.get('advance')\n        manifest.update(generated_utc=None,",
     "    if plan.get('schema') == 'WF_BATCH_PLAN_V2':\n"
     "        manifest.update(plan_kind=plan['plan_kind'], planned_pairs=len(plan['pairs']),\n"
     "                        sealed_comparison=res.get('sealed_comparison'))\n"
     "    if mode_h:\n        adv = res.get('advance')\n        manifest.update(generated_utc=None,"),
])

# ---------------------------------------------------------------- the driver's command
edit('src/methods/Method_Walk_Forward.py', [
    ("  run    --game G --batch ID            Run the plan:",
     "  plan   --fill --game G                MHUP-B (supplement 7.1A): a routine fill. The driver works out the missing\n"
     "                                        pairs of every released variant itself; one DEV_BATCH search-log row.\n"
     "  plan   --rerun --game G --first S --last L [--variants M:V,M:V,...]\n"
     "                                        MHUP-B: an exploratory rerun of the named variants (or the whole released\n"
     "                                        cohort) over S..L, whether or not scored before. Never a canonical source.\n"
     "  run    --game G --batch ID            Run the plan:"),
    ("    plan.add_argument('--last', type=int)\n",
     "    plan.add_argument('--last', type=int)\n"
     "    plan.add_argument('--fill', action='store_true')\n"
     "    plan.add_argument('--rerun', action='store_true')\n"
     "    plan.add_argument('--variants')\n"),
    ("            if args.first is None or args.last is None:\n                parser.error('a development plan needs --first and --last')\n",
     "            if args.fill or args.rerun:\n"
     "                if args.fill and args.rerun:\n"
     "                    parser.error('one of --fill and --rerun')\n"
     "                names = None\n"
     "                if args.variants is not None:\n"
     "                    names = [tuple(x.split(':', 1)) for x in args.variants.split(',')]\n"
     "                    if any(len(n) != 2 for n in names):\n"
     "                        parser.error('--variants is a list of METHOD:VARIANT separated by commas')\n"
     "                made = WF.make_dev_plan(args.game, 'ROUTINE_FILL' if args.fill else 'EXPLORATORY_RERUN', ADAPTERS,\n"
     "                                        variants=names, first=args.first, last=args.last)\n"
     "                print(f\"[WALK-FORWARD] PLAN {made['batch_id']}: {args.game} {made['plan_kind']}, {len(made['pairs'])} \"\n"
     "                      f\"pairs of {len(made['cohort'])} variants, targets {made['window_first']}-{made['window_last']}, \"\n"
     "                      f\"master version {made['ledger_version']} {made['master_sha256'][:12]}...\", flush=True)\n"
     "                print(f\"[WALK-FORWARD] next: Run_Experiment.bat Method_Walk_Forward.py run --game {args.game} \"\n"
     "                      f\"--batch {made['batch_id']}\", flush=True)\n"
     "                return 0\n"
     "            if args.variants is not None:\n"
     "                parser.error('--variants belongs to --rerun')\n"
     "            if args.first is None or args.last is None:\n                parser.error('a development plan needs --first and --last')\n"),
])
