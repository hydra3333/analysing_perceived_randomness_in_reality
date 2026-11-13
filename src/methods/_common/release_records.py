"""MHUP-A: the release records' one reader (design v0.1r5 section 4.3; EX_148 B03). Pure, read-only, standard library
only, so the records tool (src/package_tools/install_records.py, which writes the records) and the Mode H study manifest
(src/evaluation/mode_h.py, which must freeze only released variants) apply the same rule.

Records live in src/methods/_common/contract_data/install_records/ as canonical JSON:
  INSTALL_<PACKAGE>_V1.json (INSTALL_RECORD_V1) and RELEASE_<PACKAGE>_V1.json (RELEASE_RECORD_V1), plus the baseline
  RELEASE_BASELINE_20261031_V1.json.
`validate_records` refuses: a symlink, non-canonical bytes or an unknown schema; an entry without a registry chain entry
for exactly that (game, method, revision, variant); a date that is not the day of writing (the baseline excepted); a
release record whose install record is absent or later; two release records naming one entry.
`released_variants` is the released, unretired set: every release record's entries, less every entry a record retires
or marks superseded_by, and less every entry whose registry chain has moved on - its chain's active (newest) entry is
another revision, or is not SUPPORTED (EX_148 B03 (a)). A registry entry's own date field is never read here and is
never a release date (EX_142 C01, condition 3).
"""
from __future__ import annotations

from datetime import date, datetime
import hashlib
import json
from pathlib import Path

INSTALL_SCHEMA = 'INSTALL_RECORD_V1'
RELEASE_SCHEMA = 'RELEASE_RECORD_V1'
BASELINE_NAME = 'RELEASE_BASELINE_20261031_V1.json'
RECORDS_REL = Path('src') / 'methods' / '_common' / 'contract_data' / 'install_records'
REGISTRY_REL = Path('src') / 'methods' / '_common' / 'contract_data' / 'registry'
GAMES = ('POWERBALL', 'OZLOTTO')


class Refused(Exception):
    pass


def canonical(rec) -> bytes:
    return (json.dumps(rec, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n').encode('ascii')


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def records_dir(root: Path) -> Path:
    return Path(root) / RECORDS_REL


def _entry(e, where: str) -> tuple:
    if type(e) is not dict or set(e) - {'superseded_by'} != {'game_id', 'method_id', 'method_revision', 'variant_id'} or \
            e['game_id'] not in GAMES or not all(type(e[k]) is str and e[k] for k in ('method_id', 'method_revision', 'variant_id')):
        raise Refused(f'{where}: an entry is not (game_id, method_id, method_revision, variant_id)')
    return e['game_id'], e['method_id'], e['method_revision'], e['variant_id']


def registry_chains(root: Path) -> dict:
    """(game, method, variant) -> {'revisions': [every chain entry's revision], 'active': (revision, status) of the
    newest entry by entry_sequence}, from the installed registry files (read-only)."""
    out: dict = {}
    for path in sorted((Path(root) / REGISTRY_REL).glob('*/*/*/entry_*.json')):
        e = json.loads(path.read_bytes().decode('ascii'))
        c = out.setdefault((e['game_id'], e['method_id'], e['variant_id']), {'revisions': [], 'seq': -1, 'active': None})
        c['revisions'].append(e['method_revision'])
        if e['entry_sequence'] > c['seq']:
            c['seq'], c['active'] = e['entry_sequence'], (e['method_revision'], e['registry_status'])
    return out


def load_records(root: Path) -> dict:
    folder = records_dir(root)
    installs, releases = [], []
    if folder.is_dir():
        for path in sorted(folder.glob('*.json')):
            if path.is_symlink():
                raise Refused(f'{path.name} is a symlink')
            raw = path.read_bytes()
            rec = json.loads(raw.decode('ascii'))
            if canonical(rec) != raw:
                raise Refused(f'{path.name} is not its canonical bytes')
            if rec.get('schema') == INSTALL_SCHEMA:
                installs.append(rec)
            elif rec.get('schema') == RELEASE_SCHEMA:
                rec['_file'] = path.name
                releases.append(rec)
            else:
                raise Refused(f'{path.name}: unknown schema')
    return {'installs': installs, 'releases': releases}


def validate_release(rec: dict, root: Path, *, is_baseline: bool) -> None:
    chains = registry_chains(root)
    for e in rec['entries'] + rec.get('retires', []):
        g, m, rv, v = _entry(e, rec.get('package', 'release'))
        if rv not in chains.get((g, m, v), {}).get('revisions', []):
            raise Refused(f'release record {rec.get("package")}: {g} {m} revision {rv} {v} has no registry chain entry')
    try:
        d = date.fromisoformat(rec['local_date'])
        written = datetime.strptime(rec['released_utc'][:10], '%Y-%m-%d').date()
    except (KeyError, ValueError):
        raise Refused('release record: dates missing or malformed') from None
    if not is_baseline and abs((d - written).days) > 1:
        raise Refused('release record: local_date is not the day it was written (a release record never carries an '
                      'earlier date; the baseline is the one exception)')


def validate_records(root: Path) -> dict:
    recs = load_records(root)
    seen: dict = {}
    for r in recs['releases']:
        is_baseline = r['_file'] == BASELINE_NAME
        validate_release(r, root, is_baseline=is_baseline)
        if not is_baseline:
            installs = {sha256(canonical(i)): i for i in recs['installs']}
            if r.get('install_record_sha256') not in installs:
                raise Refused(f'{r["_file"]}: its install record is not present with that digest')
            if r['released_utc'] < installs[r['install_record_sha256']]['post_pass_utc']:
                raise Refused(f'{r["_file"]}: released before its install record was written')
        for e in r['entries']:
            key = _entry(e, r['_file'])
            if key in seen:
                raise Refused(f'{r["_file"]} and {seen[key]} both name {key}')
            seen[key] = r['_file']
    return recs


def released_variants(root: Path) -> dict:
    """(game, method, revision, variant) -> local release date, for the released, unretired entries: every release
    record's entries, less every entry a record retires or marks superseded_by, and less every entry whose registry
    chain has moved on (its active entry is another revision, or is not SUPPORTED). The Mode H cohort must equal this
    set (mode_h.manifest) and the weekly roster (MHUP-B) is computed from it."""
    recs = validate_records(root)
    chains = registry_chains(root)
    out: dict = {}
    retired: set = set()
    for r in recs['releases']:
        for e in r['entries']:
            key = _entry(e, r['_file'])
            if e.get('superseded_by'):
                retired.add(key)
            out[key] = r['local_date']
        for e in r.get('retires', []):
            retired.add(_entry(e, r['_file']))
    def current(k):
        active = chains.get((k[0], k[1], k[3]), {}).get('active')
        return active == (k[2], 'SUPPORTED')
    return {k: v for k, v in out.items() if k not in retired and current(k)}
