"""Shared synthetic fixtures for the E2R-CODE-2 tests (dispatch gate and run-level publication). OFFLINE.

Every registry, method folder, master and run folder here is a temporary copy or an invented file in a
temporary folder. The installed contract data and the repository are only read, never written. No real
draw value is read and no process is started.
"""
from __future__ import annotations

import contextlib
import shutil
from pathlib import Path
from unittest import mock

import e2r_fixtures as F
from test_t05_hardening import write_master
from _common.contract_records import canonical, record_digest
from _common.contract_registry import DATA_ROOT
from _common.game_profiles import get_profile

E1 = ('E_1', 'FULL_HISTORY_RAW_COUNTS_V1')
RELEASE_VARIANT = 'EXAMPLE_RELEASE_V1'


def copy_data_root(td: Path) -> Path:
    """A private copy of the installed contract data, which a test may extend."""
    root = Path(td) / 'contract_data'
    shutil.copytree(DATA_ROOT, root)
    return root


def install_declaration(root: Path, decl: dict) -> Path:
    p = root / 'declarations' / decl['game_id'] / decl['method_id'] / decl['variant_id'] / f'r{decl["method_revision"]}.json'
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as fh:
        fh.write(canonical(decl))
    return p


def append_entry(root: Path, entry: dict) -> Path:
    p = (root / 'registry' / entry['game_id'] / entry['method_id'] / entry['variant_id'] /
         f'entry_{entry["entry_sequence"]:04d}.json')
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as fh:
        fh.write(canonical(entry))
    return p


def entry(decl: dict, status: str, seq: int = 1, prev: dict | None = None) -> dict:
    return {'schema': 'REGISTRY_ENTRY_V1', 'game_id': decl['game_id'], 'method_id': decl['method_id'],
            'variant_id': decl['variant_id'], 'entry_sequence': seq, 'method_revision': decl['method_revision'],
            'declaration_digest': record_digest(decl), 'registry_status': status,
            'registry_status_reason': 'synthetic release-transition test', 'method_name': 'Synthetic probe',
            'one_liner': 'A synthetic contract test double.', 'short_explanation': 'Invented for a test.',
            'text_provenance': {'author': 'test', 'date': '2026-10-29', 'text_version': 'v1',
                                'source_reference': 'tests/e2r_code2_fixtures.py'},
            'effective_date': '2026-10-29', 'previous_entry_digest': record_digest(prev) if prev else None}


def release_declaration(game: str = 'POWERBALL', revision: str = '1') -> dict:
    d = F.declaration(game, method='E_2', variant=RELEASE_VARIANT)
    d['method_revision'] = revision
    return d


def workspace(td: Path, game: str, target: int, suffix_variant: int = 0) -> tuple[Path, str]:
    """An invented master, ledger and INIT record for one game under td/source_data."""
    sha, _length, _hashes = write_master(Path(td), get_profile(game), target, suffix_variant)
    return Path(td), sha


def request(decl: dict, entry_record: dict, target: int, sha: str, *, run_id: str = F.RUN_ID,
            view: str = 'UNORDERED_SET', revision: str | None = None) -> dict:
    r = F.request(decl, target, view, sha=sha, run_id=run_id, entry_digest=record_digest(entry_record))
    if revision is not None:
        r['method_revision'] = revision
    return r


def probe_compute(task, view):
    """The CODE-1 synthetic contract test double, in the runner's (task, view) order."""
    return F.probe_method(view, task)


def no_verify(task, view, forecast, diagnostic):
    return None


@contextlib.contextmanager
def installed(data=None, methods=None, marker=None):
    """Test harness only: temporarily patch the fixed module constants (the installed registry, the
    method folders, the global orphan marker) to temporary copies. The production APIs take no such
    arguments (reviewer's E2RC2-CODE-B01)."""
    import _common.contract_dispatch as D
    import _common.contract_registry as R
    import _common.contract_runner as CR
    with contextlib.ExitStack() as stack:
        if data is not None:
            stack.enter_context(mock.patch.object(R, 'DATA_ROOT', Path(data)))
        if methods is not None:
            stack.enter_context(mock.patch.object(D, 'METHODS_ROOT', Path(methods)))
        if marker is not None:
            stack.enter_context(mock.patch.object(CR, 'ORPHAN_MARKER', Path(marker)))
        yield
