"""MHUP-A: the executable and scientific closure, and the installed-file environment freeze (design v0.1r5
section 4.1, Appendix H; owner decision of 3 November 2026).

Orchestration-only. Nothing here reads a master, a ledger, a run record or any draw. It enumerates and digests:

- the closure: every file under src/ except __pycache__/ folders (a *.pyc or *.pyo outside __pycache__/ is a
  sourceless module and a refusal), every .bat at the repository root, requirements.txt and
  install_upgrade_dependencies_into_venv.bat; a full listing with SHA-256s, so an added, removed or changed file
  is a difference;
- the environment: the Python version and platform; the venv's pyvenv.cfg; the base installation's interpreter
  files (python.exe, pythonw.exe, python3*.dll, vcruntime*.dll on Windows; the python* executables otherwise)
  and every file under its DLLs/ and Lib/ trees except __pycache__/; the venv's Scripts/ (bin/) redirectors; and
  every distribution under the venv's site-packages: its METADATA name and version, its RECORD as pip wrote it,
  every listed file checked against its recorded SHA-256 (an entry without a hash is hashed here unless it is
  under __pycache__/), and every other file under site-packages (an orphan, a *.pyc outside __pycache__/
  included) a refusal.

The study manifest stores both inventories with their digests (Appendix H); every later Mode H step
re-enumerates and compares (`check`). What is not frozen is stated, not claimed: the operating system, its
libraries outside the interpreter's tree, the hardware, the clock.

The roots come from one `Environment` value. Production callers use `Environment.current(project_root)`, which
reads sys.prefix, sys.base_prefix and sysconfig; tests build synthetic trees and pass them explicitly, which is
a test harness only (no production caller chooses a root for another process).
"""
from __future__ import annotations

import base64
import csv
from dataclasses import dataclass
import hashlib
import io
import os
from pathlib import Path
import platform
import sys
import sysconfig

from _common.contract_records import canonical

ROOT_FILES = ('requirements.txt', 'install_upgrade_dependencies_into_venv.bat')
EXCLUDED = ('tests/', 'doc/', 'review/', 'exchange/', 'CLAUDE_CODE_WORKING_FOLDER_TREE/', '.claude/', '.git*',
            'source_data/', 'results/', 'transitory_data/')
NOT_FROZEN = ('the operating system', 'its libraries outside the interpreter\'s tree', 'the hardware', 'the clock')
WINDOWS_INTERPRETER = ('python.exe', 'pythonw.exe')
WINDOWS_INTERPRETER_GLOBS = ('python3*.dll', 'vcruntime*.dll')
BASE_TREES_WINDOWS = ('DLLs', 'Lib')
BASE_TREES_POSIX = ('lib',)


class ClosureRefused(ValueError):
    """The closure or the environment differs from the manifest, or contains something it must not."""


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def _files(folder: Path, *, skip_pycache: bool = True):
    """Every regular file under `folder` (sorted, symlinks included by name), excluding __pycache__/ folders."""
    out = []
    for dirpath, dirnames, filenames in os.walk(folder):
        if skip_pycache:
            dirnames[:] = [d for d in dirnames if d != '__pycache__']
        dirnames.sort()
        for name in sorted(filenames):
            out.append(Path(dirpath) / name)
    return out


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


# ---------------------------------------------------------------- the closure (Appendix H rows 1-4)

def closure_inventory(project_root: Path) -> dict:
    """{'files': {relative path: sha256}, 'digest': sha256 of the canonical listing}. Refuses a sourceless *.pyc or
    *.pyo under src/ outside a __pycache__/ folder."""
    root = Path(project_root)
    files = {}
    src = root / 'src'
    if not src.is_dir():
        raise ClosureRefused('no src/ folder under the project root')
    for p in _files(src):
        if p.suffix.lower() in ('.pyc', '.pyo'):
            raise ClosureRefused(f'sourceless byte-code under src/: {_rel(p, root)}')
        files[_rel(p, root)] = _sha(p)
    for p in sorted(root.glob('*.bat')):
        if p.is_file():
            files[p.name] = _sha(p)
    for name in ROOT_FILES:
        p = root / name
        if p.is_file():
            files[name] = _sha(p)
    return {'files': files, 'count': len(files), 'digest': _digest(files)}


def _digest(obj) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


# ---------------------------------------------------------------- the environment (Appendix H rows 5-6)

@dataclass(frozen=True)
class Environment:
    venv_prefix: Path          # sys.prefix: the venv
    base_prefix: Path          # sys.base_prefix: the base installation named by pyvenv.cfg
    site_packages: Path        # the venv's purelib
    scripts: Path              # the venv's Scripts/ (Windows) or bin/ redirectors
    windows: bool

    @staticmethod
    def current() -> 'Environment':
        paths = sysconfig.get_paths()
        return Environment(venv_prefix=Path(sys.prefix), base_prefix=Path(sys.base_prefix),
                           site_packages=Path(paths['purelib']), scripts=Path(paths['scripts']),
                           windows=os.name == 'nt')


def _interpreter_files(env: Environment) -> list[Path]:
    base = env.base_prefix
    out = []
    if env.windows:
        for name in WINDOWS_INTERPRETER:
            if (base / name).is_file():
                out.append(base / name)
        for pattern in WINDOWS_INTERPRETER_GLOBS:
            out.extend(sorted(p for p in base.glob(pattern) if p.is_file()))
    else:
        for folder in (base / 'bin',):
            if folder.is_dir():
                out.extend(sorted(p for p in folder.glob('python*') if p.is_file() and not p.is_symlink()))
    return out


def _parse_record(text: str) -> list[tuple[str, str | None]]:
    """RECORD rows as (path, sha256 hex or None). pip writes `path,sha256=<base64url without padding>,size`."""
    out = []
    for row in csv.reader(io.StringIO(text)):
        if not row or not row[0]:
            continue
        path = row[0]
        digest = None
        if len(row) > 1 and row[1].startswith('sha256='):
            raw = row[1][len('sha256='):]
            digest = base64.urlsafe_b64decode(raw + '=' * (-len(raw) % 4)).hex()
        out.append((path, digest))
    return out


def _metadata(dist_info: Path) -> tuple[str, str]:
    name = version = ''
    meta = dist_info / 'METADATA'
    if meta.is_file():
        for line in meta.read_text(encoding='utf-8', errors='replace').splitlines():
            if line.startswith('Name: ') and not name:
                name = line[6:].strip()
            elif line.startswith('Version: ') and not version:
                version = line[9:].strip()
            if name and version:
                break
    return name, version


def environment_inventory(env: Environment) -> dict:
    """The frozen environment (Appendix H). Refuses an orphan under site-packages, a RECORD entry whose file is
    missing or differs from its recorded hash, and a *.pyc outside __pycache__/ anywhere it looks."""
    inv: dict = {'python_version': platform.python_version(), 'platform': platform.platform(),
                 'implementation': platform.python_implementation()}
    cfg = env.venv_prefix / 'pyvenv.cfg'
    if not cfg.is_file():
        raise ClosureRefused(f'no pyvenv.cfg at {env.venv_prefix}')
    inv['pyvenv_cfg'] = cfg.read_text(encoding='utf-8', errors='replace').replace('\r\n', '\n')
    inv['interpreter'] = {_rel(p, env.base_prefix): _sha(p) for p in _interpreter_files(env)}
    if not inv['interpreter']:
        raise ClosureRefused(f'no interpreter files found under {env.base_prefix}')
    trees = {}
    for name in (BASE_TREES_WINDOWS if env.windows else BASE_TREES_POSIX):
        folder = env.base_prefix / name
        if folder.is_dir():
            for p in _files(folder):
                if p.suffix.lower() in ('.pyc', '.pyo'):
                    raise ClosureRefused(f'sourceless byte-code in the base installation: {_rel(p, env.base_prefix)}')
                trees[_rel(p, env.base_prefix)] = _sha(p)
    inv['base_trees'] = trees
    inv['scripts'] = {p.name: _sha(p) for p in _files(env.scripts)} if env.scripts.is_dir() else {}
    # installed distributions and the orphan check
    sp = env.site_packages
    if not sp.is_dir():
        raise ClosureRefused(f'no site-packages at {sp}')
    listed: set[Path] = set()
    dists = []
    for info in sorted(p for p in sp.iterdir() if p.is_dir() and p.name.endswith('.dist-info')):
        record = info / 'RECORD'
        if not record.is_file():
            raise ClosureRefused(f'{info.name} has no RECORD')
        text = record.read_text(encoding='utf-8', errors='replace')
        name, version = _metadata(info)
        files = {}
        for rel, digest in _parse_record(text):
            target = (sp / rel).resolve()
            listed.add(target)
            if '__pycache__' in Path(rel).parts:
                continue                                        # caches: made irrelevant, never trusted (4.1)
            if not target.is_file():
                raise ClosureRefused(f'{info.name}: RECORD lists {rel}, which is missing')
            actual = _sha(target)
            if digest is not None and actual != digest:
                raise ClosureRefused(f'{info.name}: {rel} differs from its RECORD hash')
            files[rel] = actual
        dists.append({'dist_info': info.name, 'name': name, 'version': version,
                      'record_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(), 'files': files})
    inv['distributions'] = dists
    orphans = [p for p in _files(sp) if p.resolve() not in listed]
    if orphans:
        raise ClosureRefused(f'{len(orphans)} file(s) under site-packages that no RECORD lists, the first: '
                             f'{_rel(orphans[0], sp)}')
    inv['digest'] = _digest({k: v for k, v in inv.items() if k != 'digest'})
    return inv


# ---------------------------------------------------------------- writing to and checking against the manifest

def freeze(project_root: Path, env: Environment | None = None) -> dict:
    """Both inventories, for the study manifest."""
    return {'closure': closure_inventory(project_root), 'environment': environment_inventory(env or Environment.current()),
            'excluded': list(EXCLUDED), 'not_frozen': list(NOT_FROZEN)}


def _first_difference(frozen: dict, now: dict, what: str) -> str:
    added = sorted(set(now) - set(frozen))
    removed = sorted(set(frozen) - set(now))
    changed = sorted(k for k in frozen if k in now and frozen[k] != now[k])
    parts = []
    if added:
        parts.append(f'added {added[0]}' + (f' (+{len(added) - 1})' if len(added) > 1 else ''))
    if removed:
        parts.append(f'removed {removed[0]}' + (f' (+{len(removed) - 1})' if len(removed) > 1 else ''))
    if changed:
        parts.append(f'changed {changed[0]}' + (f' (+{len(changed) - 1})' if len(changed) > 1 else ''))
    return f'{what}: ' + '; '.join(parts) if parts else f'{what}: differs'


def check(project_root: Path, manifest: dict, env: Environment | None = None) -> None:
    """Re-enumerate and compare with the manifest's inventories; refuse on any difference, naming the first."""
    now_c = closure_inventory(project_root)
    if now_c['digest'] != manifest['closure']['digest']:
        raise ClosureRefused(_first_difference(manifest['closure'].get('files', {}), now_c['files'], 'closure'))
    now_e = environment_inventory(env or Environment.current())
    frozen_e = manifest['environment']
    if now_e['digest'] != frozen_e['digest']:
        for key in ('python_version', 'platform', 'implementation', 'pyvenv_cfg'):
            if now_e.get(key) != frozen_e.get(key):
                raise ClosureRefused(f'environment: {key} differs')
        for key in ('interpreter', 'base_trees', 'scripts'):
            if now_e.get(key) != frozen_e.get(key):
                raise ClosureRefused(_first_difference(frozen_e.get(key, {}), now_e.get(key, {}), f'environment {key}'))
        frozen_d = {d['dist_info']: d for d in frozen_e.get('distributions', [])}
        now_d = {d['dist_info']: d for d in now_e['distributions']}
        if set(frozen_d) != set(now_d):
            raise ClosureRefused(_first_difference(frozen_d, now_d, 'environment distributions'))
        for k in sorted(frozen_d):
            if frozen_d[k] != now_d[k]:
                raise ClosureRefused(_first_difference(frozen_d[k].get('files', {}), now_d[k].get('files', {}),
                                                       f'environment distribution {k}'))
        raise ClosureRefused('environment: differs')
