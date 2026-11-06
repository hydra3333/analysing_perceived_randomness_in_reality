#!/usr/bin/env python3
"""Single TOML configuration: user settings + atomically replaced generated state.

No third-party TOML writer: tomllib reads; a bounded marked generated section is
rewritten, preserving the user section (including all its comments) byte-for-byte.
This module never silently falls back to another drive or creates binary files.
"""
from __future__ import annotations

import contextlib
from dataclasses import dataclass
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import shutil
import tempfile
import time
import threading
import tomllib

WORKSPACE = Path(__file__).resolve().parent
CONFIG_FILE = WORKSPACE / 'outlandish.local.toml'
START = '# --- BEGIN OUTLANDISH GENERATED STATE ---'
END = '# --- END OUTLANDISH GENERATED STATE ---'
CONSTANTS = ('pi', 'phi', 'e', 'log2', 'gamma', 'lemniscate')
SUBDIRS = ('digits', 'scratch', 'staging', 'results', 'logs')
SHA_RE = re.compile(r'^[0-9a-f]{64}$')
NAME_RE = re.compile(r'^[a-zA-Z0-9_ .-]+\.bin$')


class ConfigError(ValueError):
    pass


def _unsafe_link(path: Path) -> bool:
    checker = getattr(path, 'is_junction', None)
    return path.is_symlink() or bool(checker and checker())


def _validate_ancestors(p: Path) -> None:
    # A junction inside the tree would make lexical containment misleading.
    cursor = p
    while True:
        if _unsafe_link(cursor):
            raise ConfigError(f'links/junctions are prohibited: {cursor}')
        if cursor.parent == cursor:
            break
        cursor = cursor.parent


def _component(value: object, key: str) -> str:
    if (not isinstance(value, str) or not value or value in ('.', '..')
            or any(x in value for x in ('/', '\\', ':', '\x00'))
            or value.rstrip(' .') != value):
        raise ConfigError(f'{key} must be a single relative directory name, not a path: {value!r}')
    return value


def _basename(value: object) -> str:
    if not isinstance(value, str) or not NAME_RE.fullmatch(value) or value in ('.', '..'):
        raise ConfigError(f'active file must be a simple .bin basename: {value!r}')
    return value


def _record(item: dict, constant: str) -> dict:
    if constant not in CONSTANTS or not isinstance(item, dict):
        raise ConfigError(f'invalid state record: {constant!r}')
    expected = {'file', 'digits', 'sha256', 'verified_utc'}
    if set(item) != expected:
        raise ConfigError(f'state.{constant} keys must be {sorted(expected)}')
    _basename(item['file'])
    if type(item['digits']) is not int or item['digits'] < 32:
        raise ConfigError(f'invalid digit count for {constant}')
    if not isinstance(item['sha256'], str) or not SHA_RE.fullmatch(item['sha256']):
        raise ConfigError(f'invalid SHA-256 for {constant}')
    if not isinstance(item['verified_utc'], str) or not item['verified_utc'].endswith('Z'):
        raise ConfigError(f'invalid verification time for {constant}')
    return dict(item)


@dataclass(frozen=True)
class Config:
    root: Path
    names: dict[str, str]
    generator: dict
    scanner: dict
    retention: dict
    active: dict[str, dict]
    pending: dict[str, dict]

    def path(self, kind: str, *, create: bool = False) -> Path:
        if kind == 'main':
            p = self.root
        elif kind == 'artifacts':
            p = self.root / self.names['artifact']
        elif kind in SUBDIRS:
            p = self.root / self.names['artifact'] / self.names[kind]
        else:
            raise ConfigError(f'unknown configured directory: {kind}')
        _validate_ancestors(p)
        if create:
            try:
                p.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                raise ConfigError(f'cannot create configured directory {p}: {exc}') from exc
            if not p.is_dir():
                raise ConfigError(f'configured directory is not a directory: {p}')
            _validate_ancestors(p)
        return p

    def digit_file(self, basename: str, *, require_existing: bool = False) -> Path:
        name = _basename(basename)
        p = self.path('digits') / name
        _validate_ancestors(p)
        if require_existing and (not p.is_file() or _unsafe_link(p)):
            raise ConfigError(f'active binary missing/not ordinary: {p}')
        return p


def load_config() -> Config:
    if not CONFIG_FILE.is_file() or _unsafe_link(CONFIG_FILE):
        raise ConfigError(f'missing/unsafe local TOML: {CONFIG_FILE}; install the supplied template')
    original = CONFIG_FILE.read_bytes()
    try:
        raw = tomllib.loads(original.decode('utf-8-sig'))
    except (UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise ConfigError(f'invalid TOML: {exc}') from exc
    if original.count(START.encode()) != 1 or original.count(END.encode()) != 1:
        raise ConfigError('generated state boundary markers missing/duplicated')
    if not isinstance(raw.get('settings'), dict) or set(raw) != {'settings', 'state'}:
        raise ConfigError('expected only [settings] and [state] sections')
    settings = raw['settings']
    if set(settings) != {'storage', 'generator', 'scanner', 'retention'}:
        raise ConfigError('settings section names changed or missing')
    storage = settings['storage']
    if set(storage) != {'main_root', 'artifact_dir', *(name + '_dir' for name in SUBDIRS)}:
        raise ConfigError('settings.storage missing/unknown directory settings')
    if not isinstance(storage['main_root'], str) or not Path(storage['main_root']).is_absolute():
        raise ConfigError('main_root must be one absolute path for this operating system')
    root = Path(storage['main_root'])
    _validate_ancestors(root)
    names = {'artifact': _component(storage['artifact_dir'], 'artifact_dir')}
    names.update({k: _component(storage[k + '_dir'], k + '_dir') for k in SUBDIRS})
    if len(set(x.casefold() for x in names.values())) != len(names):
        raise ConfigError('configured folder names must be distinct')
    generator = settings['generator']
    # Backward compatible: an existing v0.2 TOML without this key defaults OFF.
    # The new setting controls y-cruncher's -verify switch, NOT the Python
    # pipeline's independent output reread, SHA-256 and prefix checks.
    required_generator = {'threads', 'mode', 'memory_gib'}
    if (not required_generator.issubset(generator)
            or set(generator) - required_generator - {'ycruncher_verify_output'}
            or type(generator['threads']) is not int or generator['threads'] < 1
            or generator['mode'] not in ('auto', 'ram', 'swap')
            or type(generator['memory_gib']) is not int or generator['memory_gib'] < 1
            or type(generator.get('ycruncher_verify_output', False)) is not bool):
        raise ConfigError('invalid [settings.generator]')
    generator = dict(generator)
    generator.setdefault('ycruncher_verify_output', False)
    scanner = settings['scanner']
    if (set(scanner) != {'chunk_bytes', 'progress_seconds'}
            or type(scanner['chunk_bytes']) is not int or not 32 <= scanner['chunk_bytes'] <= 64_000_000
            or type(scanner['progress_seconds']) not in (float, int) or scanner['progress_seconds'] <= 0):
        raise ConfigError('invalid [settings.scanner]')
    retention = settings['retention']
    if set(retention) != {'delete_superseded'} or type(retention['delete_superseded']) is not bool:
        raise ConfigError('invalid [settings.retention]')
    state = raw['state']
    if set(state) != {'active', 'pending_retirement'}:
        raise ConfigError('unexpected/missing generated state sections')
    active = {k: _record(v, k) for k, v in state['active'].items()}
    pending = {k: _record(v, k) for k, v in state['pending_retirement'].items()}
    for c, v in pending.items():
        if c not in active or active[c]['file'] == v['file']:
            raise ConfigError(f'inconsistent retirement record for {c}')
    return Config(root, names, dict(generator), dict(scanner), dict(retention), active, pending)


def _render_records(section: str, entries: dict[str, dict]) -> str:
    s = f'[state.{section}]\n'
    for const in CONSTANTS:
        if const not in entries:
            continue
        v = _record(entries[const], const)
        s += f'\n[state.{section}.{const}]\n'
        s += '# Parent: settings.storage.digits_dir (under artifact_dir, under main_root)\n'
        s += f"file = '{v['file']}'\n"
        s += f"digits = {v['digits']}\n"
        s += f"sha256 = '{v['sha256']}'\n"
        s += f"verified_utc = '{v['verified_utc']}'\n"
    return s


_locking_thread = threading.local()

@contextlib.contextmanager
def exclusive_lock(timeout_s: float = 30.0):
    """Cross-process advisory lock for registry writes and cooperative scans."""
    depth = getattr(_locking_thread, 'depth', 0)
    if depth:
        _locking_thread.depth = depth + 1
        try:
            yield
        finally:
            _locking_thread.depth -= 1
        return
    lock = WORKSPACE / 'outlandish.local.toml.lock'
    if _unsafe_link(lock):
        raise ConfigError(f'unsafe lock file: {lock}')
    with lock.open('a+b') as f:
        f.seek(0, os.SEEK_END)
        if f.tell() < 1:
            f.write(b'\x00')
            f.flush()
        end = time.monotonic() + timeout_s
        while True:
            try:
                if os.name == 'nt':
                    import msvcrt
                    f.seek(0)
                    msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError as exc:
                if time.monotonic() >= end:
                    raise ConfigError(f'OUTLANDISH program/registry lock busy: {lock}') from exc
                time.sleep(0.1)
        _locking_thread.depth = 1
        try:
            yield
        finally:
            _locking_thread.depth = 0
            if os.name == 'nt':
                import msvcrt
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def save_generated_state(active: dict[str, dict], pending: dict[str, dict]) -> None:
    """Call only with exclusive_lock held; atomically replace generated section.

    Preserve comments/settings above START; never edit or silently fix user settings.
    A same-folder .bak records the previous entire config, but is not auto-restored.
    """
    current = load_config()  # fail closed on manually invalid state/config
    for entries in (active, pending):
        if not isinstance(entries, dict) or set(entries) - set(CONSTANTS):
            raise ConfigError('unknown generated record')
        for k, v in entries.items():
            _record(v, k)
    for k, v in pending.items():
        if k not in active or v['file'] == active[k]['file']:
            raise ConfigError('pending retirement missing successor or duplicates active')
    original = CONFIG_FILE.read_bytes()
    beginning = original.index(START.encode())
    ending = original.index(END.encode()) + len(END.encode())
    if original[ending:].strip():
        raise ConfigError('unexpected text after generated end marker; refusing state rewrite')
    # Preserve the exact user-managed prefix up to the generated-state marker.
    prefix = original[:beginning]
    newline = b'\r\n' if b'\r\n' in prefix else b'\n'
    generated = (START + '\n' + _render_records('active', active) + '\n'
                 + _render_records('pending_retirement', pending) + END + '\n').encode()
    new = prefix + generated.replace(b'\n', newline)
    tmp = None
    bak_tmp = None
    try:
        with tempfile.NamedTemporaryFile(dir=WORKSPACE, prefix='.outlandish_config_new_', delete=False) as f:
            tmp = Path(f.name)
            f.write(new)
            f.flush()
            os.fsync(f.fileno())
        with tempfile.NamedTemporaryFile(dir=WORKSPACE, prefix='.outlandish_config_bak_', delete=False) as f:
            bak_tmp = Path(f.name)
            f.write(original)
            f.flush()
            os.fsync(f.fileno())
        # Validate the new TOML before publication (manual parser + exact records).
        check = tomllib.loads(new.decode('utf-8-sig'))
        if check['state']['active'] != active or check['state']['pending_retirement'] != pending:
            raise ConfigError('TOML state serialization validation failed')
        os.replace(bak_tmp, CONFIG_FILE.with_suffix('.toml.bak'))
        bak_tmp = None
        os.replace(tmp, CONFIG_FILE)
        tmp = None
    finally:
        for p in (tmp, bak_tmp):
            if p is not None and p.exists():
                p.unlink()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
