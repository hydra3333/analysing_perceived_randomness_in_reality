"""MHUP-B layer L4: the ONE league writer (design supplement v0.8 sections 4 and 5; code plan v0.3 L4; EX_223 B02, C01,
C03; EX_225 RC-225-2). Only this module creates the table files, the publication manifest, the WEEKLY_TABLE search-log
row, the `current` copies and LEAGUE_SOURCES_<GAME>.json. It writes nothing else: no score, no freeze line, no Mode H
path. It rescores nothing.

One publication has one identity (game, version, latest scored draw, UTC time), which is its file name. In order:

  1. both members' bytes are built in memory and checked;
  2. the manifest is created in the archive, create-only: the identity, both members' digests and every input pinned;
  3. the two archive members are created, create-only;
  4. the WEEKLY_TABLE row is appended, naming the manifest - LAST, so a row always points at a complete set;
  5. the `current` folder is refreshed: new copies under temporary names, verified; a CURRENT_COPY_INCOMPLETE
     notice; the old copies replaced; the notice removed last.

Every publish and repair first finishes any manifest that has no row: the table is rebuilt from the manifest's pinned
inputs; if the bytes are the manifest's, the missing members are created and the row appended (same bytes, same
identity); if not, a create-only PUBLICATION_INCOMPLETE note is put beside the manifest and that publication is never
logged. Nothing in the archive is overwritten or deleted, and a version number is never reused (it comes from the
manifests). A publish whose pinned inputs equal the latest logged publication's writes nothing.

Admission (supplement 4 rule 2A): a complete routine-fill attempt, or a complete report attempt over a batch of the
first kind, is added to the source list only if none of its keys is already supplied. A repeat of exactly the listed
attempt succeeds and changes no byte; anything else refuses and changes nothing. An exploratory rerun is never admitted.
"""
from __future__ import annotations

import hashlib
import uuid
from pathlib import Path

import _common.contract_publication as CP
import _common.contract_runner as CR
import _common.owner_records as OR
import _common.score_identities as SI
import _common.walk_forward as WF
from _common.contract_records import canonical, record_digest, sha256_hex

from . import league_sources as LS
from . import league_table as LT

TOOL = 'Method_League_Table.py'
NOTICE = 'CURRENT_COPY_INCOMPLETE.txt'
INCOMPLETE_SCHEMA = 'PUBLICATION_INCOMPLETE_V1'
LeagueRefused = LS.LeagueRefused


# ---------------------------------------------------------------- the durable steps (one small function each, so the
# interruption harness counts every one of them)

def _create(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    CP.create_only(path, raw)


def _row(row: dict) -> int:
    try:
        return WF._append_search_row(row)
    except WF.BatchRefused as exc:
        raise LeagueRefused(str(exc)) from None


def _move(tmp: Path, final: Path) -> None:
    tmp.replace(final)


def _remove(path: Path) -> None:
    path.unlink()


def _replace_file(path: Path, raw: bytes) -> None:
    """An atomic replace of one whole file: a reader sees the old bytes or the new bytes, never a mixture."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f'.{path.name}.new-{uuid.uuid4().hex}')
    CP.create_only(tmp, raw)
    tmp.replace(path)
    CP._fsync_dir(path.parent)


def _marker_check() -> None:
    m = Path(CR.ORPHAN_MARKER)
    if m.exists() or m.is_symlink():
        raise LeagueRefused('UNRESOLVED_ORPHAN_MARKER: no experiment or report is permitted')


def tool_sha256() -> str:
    """SHA-256 of the evaluation package's sources (LF), in name order: the tool provenance of a row."""
    h = hashlib.sha256()
    for p in sorted(Path(__file__).resolve().parent.glob('*.py')):
        h.update(p.name.encode('ascii') + b'\0' + p.read_bytes().replace(b'\r\n', b'\n') + b'\0')
    return h.hexdigest()


# ---------------------------------------------------------------- one publication

def _identity(m: dict) -> dict:
    return {'name': m['name'], 'version': m['version'], 'latest_draw': m['latest_draw'], 'published_utc': m['published_utc']}


def _log(root: Path, game_id: str, name: str, m: dict) -> None:
    """Step 4: the WEEKLY_TABLE row, unless a row already names this publication (EX_225 RC-225-2)."""
    if any(r.get('row_type') == LS.ROW_TYPE and r.get('attempt_id') == name for r in LS.search_rows(game_id)):
        return
    _row({'row_type': LS.ROW_TYPE, 'utc': m['published_utc'], 'game_id': game_id, 'mode': 'WF',
          'window_last': m['latest_draw'], 'cohort_size': len(m['inputs']['roster']),
          'cohort_digest': record_digest({'roster': m['inputs']['roster']}), 'attempt_id': name,
          'plan_digest': record_digest(m), 'tool': TOOL, 'tool_version': LS.TABLE_VERSION, 'tool_sha256': tool_sha256()})


def _archived(root: Path, game_id: str, m: dict) -> dict:
    """The two archive members of a publication, verified against its manifest."""
    out = {}
    for ext in ('txt', 'csv'):
        path = LS.archive_dir(root, game_id) / f'{m["name"]}.{ext}'
        if OR.absent(path) or sha256_hex(path.read_bytes()) != m[f'{ext}_sha256']:
            raise LeagueRefused(f'archive member {path.name} is absent or is not the bytes its manifest names')
        out[path.name] = path.read_bytes()
    return out


def _refresh_current(root: Path, game_id: str, m: dict) -> str:
    """Step 5: the `current` folder holds copies of exactly this publication's two members, or the notice."""
    want = _archived(root, game_id, m)
    folder = LS.current_dir(root, game_id)
    have = {f.name: f for f in folder.iterdir()} if folder.is_dir() else {}
    if set(have) == set(want) and all(have[n].read_bytes() == want[n] for n in want):
        return 'CURRENT_OK'
    for f in have.values():
        if f.name.startswith('.new-'):
            _remove(f)                                       # this writer's own unfinished copies of an earlier try
    for n, raw in want.items():
        tmp = folder / f'.new-{n}'
        _create(tmp, raw)
        if tmp.read_bytes() != raw:
            raise LeagueRefused(f'the new copy of {n} did not verify against the archive')
    if OR.absent(folder / NOTICE):
        _create(folder / NOTICE, (f'The copies in this folder are being replaced by {m["name"]}. Until this notice is '
                                  f'gone the folder is not current; the archive is the record.\n').encode('ascii'))
    for f in sorted(folder.iterdir()):
        if f.name != NOTICE and not f.name.startswith('.new-'):
            _remove(f)                                       # the old copies (a convenience, never a source)
    for n in want:
        _move(folder / f'.new-{n}', folder / n)
    _remove(folder / NOTICE)
    return 'CURRENT_REFRESHED'


def _finish(root: Path, game_id: str, p: dict) -> str:
    """Finish one manifest that has no row, with the same bytes and identity; or mark it incomplete, for good."""
    m, folder = p['manifest'], LS.archive_dir(root, game_id)
    why = None
    try:
        data, _pins = LS.collect(root, game_id, m['inputs'])
        built = LT.build(data, _identity(m))
        if any(sha256_hex(built[ext]) != m[f'{ext}_sha256'] for ext in ('txt', 'csv')):
            why = 'the table rebuilt from the pinned inputs is not the bytes the manifest names'
        else:
            for ext in ('txt', 'csv'):
                path = folder / f'{m["name"]}.{ext}'
                if not OR.absent(path) and path.read_bytes() != built[ext]:
                    why = f'the archive member {path.name} holds other bytes'
    except LeagueRefused as exc:
        why = str(exc)
    if why is not None:
        _create(folder / f'{m["name"]}.PUBLICATION_INCOMPLETE.json',
                canonical({'schema': INCOMPLETE_SCHEMA, 'game_id': game_id, 'name': m['name'],
                           'manifest_digest': p['digest'], 'reason': why.encode('ascii', 'replace').decode('ascii')[:400],
                           'noted_utc': CP.utc_now()}))
        return 'INCOMPLETE'
    for ext in ('txt', 'csv'):
        path = folder / f'{m["name"]}.{ext}'
        if OR.absent(path):
            _create(path, built[ext])
    _log(root, game_id, m['name'], m)
    return 'FINISHED'


def repair(game_id: str, echo=None) -> dict:
    """Finish or mark every publication that has a manifest and no row; then make `current` the latest logged one."""
    _marker_check()
    root = LS.project_root()
    say = echo or (lambda s: None)
    out = {'finished': [], 'incomplete': [], 'current': None}
    for p in LS.manifests(root, game_id):
        if p['logged'] or p['incomplete']:
            continue
        state = _finish(root, game_id, p)
        out['finished' if state == 'FINISHED' else 'incomplete'].append(p['name'])
        say(f'[LEAGUE] unfinished publication {p["name"]}: ' +
            ('finished with the same bytes and identity' if state == 'FINISHED' else
             'could not be rebuilt identically; marked PUBLICATION_INCOMPLETE and never logged'))
    latest = LS.latest_logged(root, game_id)
    if latest is not None:
        out['current'] = _refresh_current(root, game_id, latest['manifest'])
        if out['current'] == 'CURRENT_REFRESHED':
            say(f'[LEAGUE] the current folder now holds {latest["name"]}')
    return out


def publish(game_id: str, echo=None) -> dict:
    """The league table of the game, published once per change of its inputs. Returns {'state': 'PUBLISHED' or
    'UP_TO_DATE', 'name', 'repair'}. LeagueRefused before anything of a new publication is written."""
    _marker_check()
    root = LS.project_root()
    say = echo or (lambda s: None)
    repaired = repair(game_id, echo=echo)
    data, pins = LS.collect(root, game_id)
    pubs = LS.manifests(root, game_id)
    logged = [p for p in pubs if p['logged']]
    if logged and logged[-1]['manifest']['inputs'] == pins:
        return {'state': 'UP_TO_DATE', 'name': logged[-1]['name'], 'repair': repaired}
    version = (pubs[-1]['manifest']['version'] if pubs else 0) + 1          # from the manifests: never reused
    utc = CP.utc_now()
    name = LS.publication_name(game_id, LT.latest_draw(data), version, utc)
    identity = {'name': name, 'version': version, 'latest_draw': LT.latest_draw(data), 'published_utc': utc}
    built = LT.build(data, identity)                                        # step 1: in memory
    manifest = {'schema': LS.MANIFEST_SCHEMA, 'game_id': game_id, **identity, 'txt_sha256': sha256_hex(built['txt']),
                'csv_sha256': sha256_hex(built['csv']), 'inputs': pins, 'tool': TOOL, 'table_version': LS.TABLE_VERSION}
    LS.validate_manifest(manifest, game_id, name)
    folder = LS.archive_dir(root, game_id)
    _create(folder / f'{name}.manifest.json', canonical(manifest))          # step 2
    for ext in ('txt', 'csv'):
        _create(folder / f'{name}.{ext}', built[ext])                       # step 3
    _log(root, game_id, name, manifest)                                     # step 4: the row, last
    say(f'[LEAGUE] published {name} (version {version}); search-log row written')
    _refresh_current(root, game_id, manifest)                               # step 5
    return {'state': 'PUBLISHED', 'name': name, 'repair': repaired}


# ---------------------------------------------------------------- admission (supplement 4 rules 2A and 5)

def admit(game_id: str, *, attempt_id: str | None = None, batch_id: str | None = None, first: int | None = None,
          last: int | None = None) -> dict:
    """Add one complete report attempt to LEAGUE_SOURCES_<GAME>.json, or change nothing. Returns {'state': 'ADMITTED' or
    'ALREADY_ADMITTED', 'attempt_id'}."""
    _marker_check()
    root = LS.project_root()
    if attempt_id is None:
        st = LS.batch_state(root, game_id, batch_id, first, last)
        if st['batch_kind'] not in SI.LEAGUE_SOURCE_KINDS:
            raise LeagueRefused('an exploratory rerun is never admitted (supplement 4 rule 2A)')
        if st['admitted'] is not None:
            attempt_id = st['admitted']
        elif len(st['complete']) == 1:
            attempt_id = st['complete'][0]
        elif not st['complete']:
            raise LeagueRefused(f'batch {batch_id} has no complete report over draws {st["first"]}-{st["last"]}' +
                                (f' ({st["incomplete_reasons"][0]})' if st['incomplete_reasons'] else ''))
        else:
            raise LeagueRefused(f'batch {batch_id} has {len(st["complete"])} complete reports over draws {st["first"]}-'
                                f'{st["last"]}; name one with --attempt (the first admitted is the canonical one)')
    entry, rows = LS.attempt_entry(root, game_id, attempt_id)
    try:
        listed = SI.league_sources(root, game_id)
    except OR.RecordRefused as exc:
        raise LeagueRefused(str(exc)) from None
    for s in listed:
        if s['attempt_id'] == attempt_id:
            if s == entry:
                return {'state': 'ALREADY_ADMITTED', 'attempt_id': attempt_id}        # the file is not rewritten
            raise LeagueRefused(f'{attempt_id} is already listed with a different score ledger, scope or evaluator '
                                f'version; nothing was changed')
    have = LS.canonical_keys(root, game_id)
    clash = sorted(k for k in ((r['method'], r['revision'], r['variant'], r['target'], r['readout']) for r in rows)
                   if k in have)
    if clash:
        raise LeagueRefused(f'{attempt_id} is not admitted: the key {clash[0]} is already supplied by '
                            f'{have[clash[0]]}; nothing was changed')
    _replace_file(SI.league_sources_path(root, game_id),
                  canonical({'schema': SI.LEAGUE_SOURCES_SCHEMA, 'game_id': game_id, 'sources': [*listed, entry]}))
    return {'state': 'ADMITTED', 'attempt_id': attempt_id}


# ---------------------------------------------------------------- checks and the two derived views

def sources_check(game_id: str) -> dict:
    """Read everything a publication would read, and every logged publication's members. Writes nothing."""
    root = LS.project_root()
    data, _pins = LS.collect(root, game_id)
    pubs = LS.manifests(root, game_id)
    for p in pubs:
        if p['logged']:
            _archived(root, game_id, p['manifest'])
    return {'sources': len(data['sources']), 'rows': len(data['rows']), 'not_available': data['not_available'],
            'mode_h': data['mode_h']['not_available'] or 'available',
            'logged': sum(1 for p in pubs if p['logged']),
            'pending': [p['name'] for p in pubs if not p['logged'] and not p['incomplete']],
            'incomplete': [p['name'] for p in pubs if p['incomplete']],
            'current_notice': not OR.absent(LS.current_dir(root, game_id) / NOTICE)}


def history(game_id: str) -> dict:
    """Sup 5.2: the published tables joined, newest first, byte for byte from the archive. It recomputes nothing."""
    _marker_check()
    root = LS.project_root()
    logged = [p for p in LS.manifests(root, game_id) if p['logged']]
    if not logged:
        raise LeagueRefused('no league table has been published yet')
    parts = [f'LEAGUE TABLE HISTORY - {game_id} - {len(logged)} published tables, newest first. This joins the published '
             f'files as they are; nothing is recomputed.\n'.encode('ascii')]
    for p in reversed(logged):
        txt = _archived(root, game_id, p['manifest'])[f'{p["name"]}.txt']
        parts += [('\n' + '=' * 100 + '\n').encode('ascii'), txt]
    raw = b''.join(parts)
    path = LS.derived_dir(root, game_id) / f'league_history_{game_id}_through_v{logged[-1]["manifest"]["version"]:05d}.txt'
    if not OR.absent(path):
        if path.read_bytes() != raw:
            raise LeagueRefused(f'{path.name} exists with other bytes; nothing was written')
        return {'state': 'UNCHANGED', 'path': path}
    _create(path, raw)
    return {'state': 'WRITTEN', 'path': path}


def reconstruction(game_id: str) -> dict:
    """Sup 5.3: the current-cohort historical reconstruction, one labelled CSV, on request."""
    _marker_check()
    root = LS.project_root()
    data, _pins = LS.collect(root, game_id)
    if data['not_available']:
        raise LeagueRefused(f'a listed source is not available ({data["not_available"][0]["source"]}); no reconstruction')
    utc = CP.utc_now()
    raw = LT.reconstruction(data, utc[:10])
    stamp = utc[:19].replace('-', '').replace(':', '') + 'Z'
    path = LS.derived_dir(root, game_id) / f'league_reconstruction_{game_id}_{stamp}.csv'
    _create(path, raw)
    return {'state': 'WRITTEN', 'path': path}
