"""E_2-readiness contract (E2R-1 v0.3r3): installed declarations, registry entries and release policy checks.

Stage-1 contract library (E2R-CODE-1). The only file access is a read-only load of this package's
own data under contract_data/ (canonical JSON, one file per declaration and per registry entry).
Nothing is dispatched here: the dispatch gate (E2R-R57, T14) is wired into the launchers by CODE-2.
The revision-rollover check (E2R-R14A, T13) is a package-time governance check over identities;
it is not a run-time hashing or code-recording mechanism.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import MappingProxyType
from collections.abc import Mapping

import _common.contract_vocab as V
from _common.contract_records import (
    canonical, record_digest, validate_declaration, validate_entry_declaration_pair,
    validate_registry_chain,
)

DATA_ROOT = Path(__file__).resolve().parent / 'contract_data'
REGISTERED_METHODS = tuple(f'E_{i}' for i in range(1, 63))   # E_1..E_62 stay registered (E2R-R19)
STRUCTURAL_EXCEPTIONS = MappingProxyType({                       # E2R-R14A; E1A-D1 (register v0.8)
    'NAMES-1': 'one-off rename to stable file names',
    'E1-ALIGN': 'E_1 modules into src/methods/E_001 and the shared canonical encoding',
})


def _load_canonical(path: Path) -> dict:
    # A Windows checkout with core.autocrlf may give the data files CRLF line endings; the
    # canonical form is the LF bytes, so they are compared after CRLF -> LF (README v0.4 rule).
    raw = path.read_bytes().replace(b'\r\n', b'\n')
    rec = json.loads(raw.decode('ascii'))
    if canonical(rec) != raw:
        raise ValueError(f'{path.name}: not stored as canonical bytes')
    return rec


class InstalledRegistry:
    """Every installed declaration and registry chain, validated on load and immutable afterwards.

    Storage (E2RC1-B01): each record is kept only as its canonical bytes, keyed by the SHA-256 digest
    of those bytes, inside read-only mappings and tuples. Bytes cannot be changed, so no installed
    value can drift from its digest, at any depth. The instance itself refuses attribute changes.
    Access: every accessor builds a NEW dict from the stored bytes and checks it against the stored
    digest before returning it. The caller owns that copy and may keep or change it; a changed copy
    affects neither the registry nor any other caller, and it is not the installed record: its own
    record_digest differs, so it can never be passed off under the installed identity.
    """

    __slots__ = ('_declarations', '_chains')

    def __init__(self, root: Path = DATA_ROOT):
        decls, chains = {}, {}
        for path in sorted((root / 'declarations').glob('*/*/*/r*.json')):
            d = validate_declaration(_load_canonical(path))
            game, method, variant = path.parts[-4:-1]
            if (d['game_id'], d['method_id'], d['variant_id'], f'r{d["method_revision"]}.json') != (
                    game, method, variant, path.name):
                raise ValueError(f'{path}: file location does not match the declaration')
            dig = record_digest(d)
            if dig in decls:
                raise ValueError('duplicate declaration')
            decls[dig] = d
        for folder in sorted({p.parent for p in (root / 'registry').glob('*/*/*/entry_*.json')}):
            files = sorted(folder.glob('entry_*.json'))
            entries = [_load_canonical(p) for p in files]
            for i, (p, e) in enumerate(zip(files, entries), start=1):
                if p.name != f'entry_{i:04d}.json':
                    raise ValueError(f'{p}: registry entry files must be entry_0001.json, entry_0002.json, ...')
                if (e['game_id'], e['method_id'], e['variant_id']) != tuple(folder.parts[-3:]):
                    raise ValueError(f'{p}: file location does not match the entry')
            validate_registry_chain(entries)
            for e in entries:
                validate_entry_declaration_pair(e, decls.get(e['declaration_digest']) if e['declaration_digest'] else None)
            chains[tuple(folder.parts[-3:])] = tuple(_frozen(e) for e in entries)
        for game in ('POWERBALL', 'OZLOTTO'):
            listed = {m for (g, m, _v) in chains if g == game}
            if listed != set(REGISTERED_METHODS):
                raise ValueError(f'{game}: every method E_1..E_62 must stay registered (E2R-R19)')
        object.__setattr__(self, '_declarations', MappingProxyType({k: _frozen(v)[1] for k, v in decls.items()}))
        object.__setattr__(self, '_chains', MappingProxyType(chains))

    def __setattr__(self, name, value):
        raise AttributeError('InstalledRegistry is read-only')

    def __delattr__(self, name):
        raise AttributeError('InstalledRegistry is read-only')

    def declaration_digests(self) -> tuple[str, ...]:
        return tuple(sorted(self._declarations))

    def chain_keys(self) -> tuple[tuple[str, str, str], ...]:
        """(game_id, method_id, variant_id) of every registry chain, sorted."""
        return tuple(sorted(self._chains))

    def declaration(self, digest: str) -> dict:
        """A new, caller-owned copy of the installed declaration with this digest."""
        if digest not in self._declarations:
            raise ValueError('no installed declaration with this digest')
        return _thaw(digest, self._declarations[digest])

    def chain(self, game_id: str, method_id: str, variant_id: str) -> list[dict]:
        """New, caller-owned copies of every entry in one chain, oldest first."""
        return [_thaw(dig, raw) for dig, raw in self._chain(game_id, method_id, variant_id)]

    def active_entry(self, game_id: str, method_id: str, variant_id: str) -> dict:
        """A new, caller-owned copy of the newest entry in one chain."""
        return _thaw(*self._chain(game_id, method_id, variant_id)[-1])

    def _chain(self, game_id, method_id, variant_id):
        key = (game_id, method_id, variant_id)
        if key not in self._chains:
            raise ValueError('no registry chain for this method variant')
        return self._chains[key]


def _frozen(rec: Mapping) -> tuple[str, bytes]:
    raw = canonical(rec)
    return hashlib.sha256(raw).hexdigest(), raw


def _thaw(digest: str, raw: bytes) -> dict:
    rec = json.loads(raw.decode('ascii'))
    if record_digest(rec) != digest or canonical(rec) != raw:
        raise ValueError('installed record does not match its digest')
    return rec


# ---------------------------------------------------------------- revision rollover (E2R-R14A, E2R-T13)

def revision_rollover_findings(baseline: Mapping, successor: Mapping, *, package_id: str) -> list[str]:
    """Check a package's identities against the rule that a behaviourally relevant change needs a successor revision.

    `baseline` and `successor` are synthetic identity manifests:
      {'helpers': {name: revision}, 'methods': {method_id: {'revision', 'helpers': {name: revision},
                                                             'implementation_changed': bool, 'runnable': bool}}}
    A runnable method whose own implementation, or any shared helper it uses, changed must have a new
    revision, unless the package is the one structural exception that names itself. Unaffected
    methods keep their revisions, with a recorded finding. Raises ValueError on a violation.
    """
    findings = []
    old_helpers, new_helpers = baseline['helpers'], successor['helpers']
    for mid, new in sorted(successor['methods'].items()):
        old = baseline['methods'].get(mid)
        if old is None:
            findings.append(f'{mid}: new method at revision {new["revision"]}')
            continue
        changed = sorted(h for h, rev in old['helpers'].items() if new_helpers.get(h) != old_helpers.get(h))
        touched = bool(changed) or new['implementation_changed']
        if not touched:
            if new['revision'] != old['revision']:
                findings.append(f'{mid}: revision {old["revision"]} -> {new["revision"]} with no recorded change')
            else:
                findings.append(f'{mid}: unaffected by this package; keeps revision {old["revision"]}')
            continue
        if new['revision'] == old['revision']:
            if not new['runnable']:
                findings.append(f'{mid}: not runnable; no revision needed yet')
            elif package_id in STRUCTURAL_EXCEPTIONS and successor.get('structural_only') is True:
                findings.append(f'{mid}: keeps revision under the {package_id} structural exception')
            else:
                raise ValueError(f'{mid}: behaviourally relevant change ({changed or "own implementation"}) '
                                 f'without a successor revision (E2R-R14A)')
        else:
            if int(new['revision']) <= int(old['revision']):
                raise ValueError(f'{mid}: a successor revision must be a higher number')
            stale = sorted(h for h, rev in new['helpers'].items() if new_helpers.get(h) != rev)
            if stale:
                raise ValueError(f'{mid}: successor revision still names superseded helpers {stale}')
            findings.append(f'{mid}: successor revision {new["revision"]} for {changed or "own implementation"}')
    return findings
