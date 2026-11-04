"""MHUP-A: the install record and the release record (design v0.1r5 section 4.3; Appendix J steps 12 and 16).

Two create-only records per code package, under src/methods/_common/contract_data/install_records/, committed
with the package:
  INSTALL_<PACKAGE>_V1.json   code arrival (written after POST PASS and the suite, before staging): the package,
                              its manifest's SHA-256, the UTC time and local date, the registry entries it adds.
                              It qualifies nothing by itself.
  RELEASE_<PACKAGE>_V1.json   the variants that became released (written after COMMITTED PASS, with E and P
                              removed, while the install still holds the updater lock): the released (game,
                              method, revision, variant) entries, the retirements, the UTC time and local date of
                              that step, the install record's digest. The release date of MH-1's rule is this
                              record's local date, read from the PC clock when it is written.
The baseline record RELEASE_BASELINE_20261031_V1.json travels in MHUP-A as a reviewed member (the one record whose
dates precede its writing, the owner's confirmed 31 October 2026 dates; the owner's installation confirms it).

Validation (`validate_records`): every entry a release record names has a registry chain entry, active or
superseded, for exactly that (game, method, revision, variant); two release records naming the same entry refuse;
a record's local date is the day it was written (the baseline excepted); the install record a release record names
exists with that digest and precedes it. `released_variants` gives the released, unretired set the weekly roster is computed from.

Run directly with the venv's Python (the pattern of process_check.py):
  python -I -B src/package_tools/install_records.py install-record --root R --package P --manifest M
  python -I -B src/package_tools/install_records.py release-record --root R --package P --manifest M
  python -I -B src/package_tools/install_records.py validate --root R
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

INSTALL_SCHEMA = 'INSTALL_RECORD_V1'
RELEASE_SCHEMA = 'RELEASE_RECORD_V1'
BASELINE_NAME = 'RELEASE_BASELINE_20261031_V1.json'
RECORDS_REL = Path('src') / 'methods' / '_common' / 'contract_data' / 'install_records'
BARRIER_REL = Path('src') / 'methods' / '_common' / 'contract_data' / 'INSTALL_IN_PROGRESS.txt'
PACKAGE = re.compile(r'[A-Za-z0-9_.-]+\Z')
GAMES = ('POWERBALL', 'OZLOTTO')


class Refused(Exception):
    pass


def canonical(rec) -> bytes:
    return (json.dumps(rec, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n').encode('ascii')


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def now() -> tuple[str, str]:
    """(UTC instant, local calendar date from the PC clock)."""
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ'), date.today().isoformat()


def records_dir(root: Path) -> Path:
    return root / RECORDS_REL


def write_new(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'xb') as fh:
        fh.write(raw)
        fh.flush()
        os.fsync(fh.fileno())


def load_manifest(path: Path) -> dict:
    """The package manifest: `package`, `release_entries` [{game_id, method_id, method_revision, variant_id}],
    `retires` [the same shape], `registry_entries_added` [paths]."""
    if not path.is_file():
        raise Refused(f'no package manifest at {path}')
    rec = json.loads(path.read_text(encoding='ascii'))
    if type(rec.get('package')) is not str or not PACKAGE.fullmatch(rec['package']):
        raise Refused('the package manifest names no package')
    for key in ('release_entries', 'retires'):
        rec.setdefault(key, [])
        for e in rec[key]:
            _entry(e, f'manifest {key}')
    rec.setdefault('registry_entries_added', [])
    return rec


def _entry(e, where: str) -> tuple:
    if type(e) is not dict or set(e) - {'superseded_by'} != {'game_id', 'method_id', 'method_revision', 'variant_id'} or \
            e['game_id'] not in GAMES or not all(type(e[k]) is str and e[k] for k in ('method_id', 'method_revision', 'variant_id')):
        raise Refused(f'{where}: an entry is not (game_id, method_id, method_revision, variant_id)')
    return e['game_id'], e['method_id'], e['method_revision'], e['variant_id']


# ---------------------------------------------------------------- the records

def install_record(root: Path, package: str, manifest_path: Path) -> Path:
    man = load_manifest(manifest_path)
    if man['package'] != package:
        raise Refused('--package does not match the manifest')
    if not (root / BARRIER_REL).exists():
        raise Refused('the install barrier P is absent: the install record is written during the install (step 12)')
    utc, local = now()
    rec = {'schema': INSTALL_SCHEMA, 'package': package, 'manifest_sha256': sha256(manifest_path.read_bytes()),
           'post_pass_utc': utc, 'local_date': local, 'registry_entries_added': list(man['registry_entries_added']),
           'release_entries_planned': list(man['release_entries']), 'retires_planned': list(man['retires']),
           'statement': 'code arrival (POST PASS); this record qualifies no variant for anything (design 4.3)'}
    path = records_dir(root) / f'INSTALL_{package}_V1.json'
    if path.exists() or path.is_symlink():
        raise Refused(f'{path.name} already exists (create-only)')
    write_new(path, canonical(rec))
    return path


def _committed(root: Path, rel: Path) -> bool:
    """The file at `rel` is committed at HEAD with exactly the working tree's bytes (read-only Git)."""
    try:
        blob = subprocess.run(['git', '-C', str(root), 'show', f'HEAD:{rel.as_posix()}'], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, check=True).stdout
    except (subprocess.CalledProcessError, OSError):
        return False
    return blob == (root / rel).read_bytes()


def _tracked_changes(root: Path) -> list[str]:
    r = subprocess.run(['git', '-C', str(root), 'status', '--porcelain', '--untracked-files=no'], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=True)
    return [ln for ln in r.stdout.decode('utf-8', errors='replace').splitlines() if ln.strip()]


def release_record(root: Path, package: str, manifest_path: Path) -> Path:
    man = load_manifest(manifest_path)
    if man['package'] != package:
        raise Refused('--package does not match the manifest')
    if (root / BARRIER_REL).exists() or (root / BARRIER_REL).is_symlink():
        raise Refused('the install barrier P still exists; the release record follows COMMITTED PASS and the removal of E '
                      'and P (Appendix J step 16)')
    install_rel = RECORDS_REL / f'INSTALL_{package}_V1.json'
    if not (root / install_rel).is_file():
        raise Refused('no install record for this package')
    if not _committed(root, install_rel):
        raise Refused('the install record is not committed at HEAD with these bytes: the release record follows the '
                      'package commit and COMMITTED PASS')
    changes = _tracked_changes(root)
    if changes:
        raise Refused('tracked files differ from HEAD; COMMITTED PASS cannot have been reached:\n  ' + '\n  '.join(changes))
    for g in GAMES:
        lock = root / 'results' / 'real' / 'weekly' / g / 'ACTIVE_SESSION.lock'
        if lock.exists() or lock.is_symlink():
            raise Refused(f'{g}: a session lock exists; no release record while a session is open')
    if man['release_entries'] or man['retires']:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import process_check as PC
        for g in GAMES:
            open_set = PC.unfinished_weekly_set(root, g)
            if open_set:
                raise Refused(f'{g}: an unfinished weekly set (targets {sorted(open_set)}); a roster-changing release waits '
                              f'(EX_129 C01)')
    path = records_dir(root) / f'RELEASE_{package}_V1.json'
    if path.exists() or path.is_symlink():
        raise Refused(f'{path.name} already exists (create-only)')
    existing = load_records(root)
    named = {_entry(e, 'release') for r in existing['releases'] for e in r['entries']}
    for e in man['release_entries']:
        if _entry(e, 'manifest release_entries') in named:
            raise Refused(f'entry {e} is already named by an earlier release record')
    utc, local = now()
    rec = {'schema': RELEASE_SCHEMA, 'package': package, 'entries': list(man['release_entries']),
           'retires': list(man['retires']), 'released_utc': utc, 'local_date': local,
           'install_record_sha256': sha256((root / install_rel).read_bytes()),
           'statement': ('the named variants became released on local_date (MH-1\'s release date); written after '
                         'COMMITTED PASS with E and P removed (design 4.3)')}
    validate_release(rec, root, is_baseline=False)
    write_new(path, canonical(rec))
    return path


# ---------------------------------------------------------------- validation and the released set

def _registry_chains(root: Path) -> dict:
    """(game, method, variant) -> [revisions of every chain entry], from the installed registry files (read-only)."""
    reg = root / 'src' / 'methods' / '_common' / 'contract_data' / 'registry'
    out: dict = {}
    for path in sorted(reg.glob('*/*/*/entry_*.json')):
        e = json.loads(path.read_bytes().decode('ascii'))
        out.setdefault((e['game_id'], e['method_id'], e['variant_id']), []).append(e['method_revision'])
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
    chains = _registry_chains(root)
    for e in rec['entries'] + rec.get('retires', []):
        g, m, rv, v = _entry(e, rec.get('package', 'release'))
        if rv not in chains.get((g, m, v), []):
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
    record's entries, less every entry a record retires or marks superseded_by, and less entries whose registry chain
    has moved on (a later revision active). The weekly roster (MHUP-B) is computed from this."""
    recs = validate_records(root)
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
    return {k: v for k, v in out.items() if k not in retired}


# ---------------------------------------------------------------- command line

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='command', required=True)
    for name in ('install-record', 'release-record', 'validate'):
        sp = sub.add_parser(name)
        sp.add_argument('--root', required=True)
        if name != 'validate':
            sp.add_argument('--package', required=True)
            sp.add_argument('--manifest', required=True)
    args = ap.parse_args(argv)
    root = Path(args.root)
    try:
        if not root.is_absolute() or not (root / '.git').exists():
            raise Refused('--root must be the absolute path of the repository')
        if args.command == 'install-record':
            path = install_record(root, args.package, Path(args.manifest))
            print(f'INSTALL RECORD PASS: {path}')
        elif args.command == 'release-record':
            path = release_record(root, args.package, Path(args.manifest))
            print(f'RELEASE RECORD PASS: {path}')
        else:
            recs = validate_records(root)
            print(f'RECORDS PASS: {len(recs["installs"])} install record(s), {len(recs["releases"])} release record(s), '
                  f'{len(released_variants(root))} released unretired entries')
        return 0
    except Refused as exc:
        print(f'{args.command.upper().replace("-", " ")} STOP: {exc}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
