"""E_2-readiness contract (E2R-1 v0.3r3): run-level publication of records, receipts and the terminal record.

E2R-CODE-2. Orchestration side only: no method code is imported, and nothing here reads draw data.
Publication order (E2R-R38A): the output record (C1 or C2) is created, validated, and only then its
freeze receipt (D1 or the diagnostic receipt); a SUCCESS terminal record (D2) naming those receipts
comes last. Every file is create-only (E2R-R36): written in full to this write's own temporary file,
then published by an atomic hard link that fails if the name exists, so nothing is ever replaced. Nothing
here deletes, moves, quarantines or terminates anything (apart from each write's own temporary file), and
nothing retries: an interrupted run leaves its files as they are and is not consumable (E2R-T16).

Run folder (E2R-R52): <run_root>/<game_id>/<method_id>/<variant_id>/<run_id>/, created exclusively.
"""
from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import uuid

import _common.contract_vocab as V
from _common.contract_forecast import validate_diagnostic, validate_forecast
from _common.contract_receipts import (
    consumable, status_at_freeze, validate_diagnostic_receipt, validate_freeze_receipt, validate_terminal,
)
from _common.contract_records import canonical, record_digest, sha256_hex, validate_run_request

FILES = {'forecast': 'forecast.json', 'forecast_receipt': 'forecast_receipt.json',
         'diagnostic': 'diagnostic.json', 'diagnostic_receipt': 'diagnostic_receipt.json',
         'terminal': 'terminal.json'}


def new_run_id() -> str:
    """A fresh Package 2 format run ID, mg-<32 hex> (E2R-R52)."""
    rid = 'mg-' + uuid.uuid4().hex
    assert V.RUN_ID.fullmatch(rid)
    return rid


def _fsync_dir(folder: Path) -> None:
    """Make a directory entry durable where the platform allows it (POSIX). Windows has no directory
    fsync; NTFS journals the link itself."""
    if os.name == 'nt':
        return
    fd = os.open(folder, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def create_only(path: Path, raw: bytes) -> None:
    """Publish a new file without ever replacing one (E2R-R36; reviewer's E2RC2-C01).

    The bytes go to a new temporary file owned by this call (exclusive create), are flushed and
    fsynced, and are then published with os.link(temporary, path). Creating a hard link is atomic and
    fails with FileExistsError if anything already has that name, on POSIX and on NTFS; so a published
    file is never overwritten, a reader never sees a partial file, and of several concurrent writers
    exactly one wins. Only this call's own temporary file is removed afterwards. A filesystem that
    cannot make hard links refuses publication (fail closed); nothing falls back to a rename."""
    tmp = path.with_name(f'.{path.name}.part-{uuid.uuid4().hex}')
    try:
        with tmp.open('xb') as fh:
            fh.write(raw)
            fh.flush()
            os.fsync(fh.fileno())
        try:
            os.link(tmp, path)
        except FileExistsError:
            raise FileExistsError(f'{path.name} already exists; publication never overwrites') from None
        except (NotImplementedError, OSError) as exc:
            raise RuntimeError(f'no-clobber publication is not available here ({type(exc).__name__}); '
                               f'{path.name} was not published') from None
    finally:
        tmp.unlink(missing_ok=True)
    _fsync_dir(path.parent)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def environment_identity() -> dict:
    """Informational provenance for receipts (section 8.1): never part of any record's content."""
    def version(name):
        try:
            return importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            return 'NOT_INSTALLED'
    packages = sorted({f'{(d.metadata["Name"] or "").lower()}=={d.version}'
                       for d in importlib.metadata.distributions() if d.metadata['Name']})
    return {'python_version': platform.python_version(), 'numpy_version': version('numpy'),
            'psutil_version': version('psutil'), 'os_name': platform.system() or 'UNKNOWN',
            'os_build': platform.version() or 'UNKNOWN',
            'installed_packages_digest': hashlib.sha256('\n'.join(packages).encode('utf-8')).hexdigest()}


def run_folder(run_root: Path, request: Mapping) -> Path:
    return (Path(run_root) / request['game_id'] / request['method_id'] / request['variant_id'] /
            request['run_id'])


class RunPublication:
    """The files of one admitted run, published in E2R-R38A order. One instance per run."""

    def __init__(self, run_root: Path, request: Mapping, *, entry_digest: str, provenance: Mapping):
        validate_run_request(request)
        if request['registry_entry_digest'] != entry_digest:
            raise ValueError('the admitted entry is not the one the request pins')
        self.request = dict(request)
        self.execution_path = 'STANDALONE'         # CODE-2 publishes standalone runs only (E2RC2-CODE-B02)
        self.provenance = dict(provenance)          # master_file .. init_record_sha256, from the runner
        self.folder = run_folder(run_root, request)
        self.folder.parent.mkdir(parents=True, exist_ok=True)
        self.folder.mkdir(exist_ok=False)           # a run folder belongs to one run only
        _fsync_dir(self.folder.parent)
        self.receipts: list[str] = []
        self.terminal_written = False

    def _write(self, key: str, record: Mapping) -> bytes:
        raw = canonical(record)
        create_only(self.folder / FILES[key], raw)
        if (self.folder / FILES[key]).read_bytes() != raw:
            raise ValueError(f'{FILES[key]} does not read back as written')
        return raw

    def _receipt(self, schema: str, record: Mapping, raw: bytes, product_digest_names) -> dict:
        r = {'schema': schema, 'game_id': record['game_id'], 'target_draw_number': record['target_draw_number'],
             'method_id': record['method_id'], 'variant_id': record['variant_id'],
             'method_revision': record['method_revision'],
             'master_file': self.provenance['master_file'], 'ledger_version': self.provenance['ledger_version'],
             'master_sha256': self.provenance['master_sha256'], 'ledger_sha256': self.provenance['ledger_sha256'],
             'init_record_sha256': self.provenance['init_record_sha256'],
             'environment_identity': environment_identity(), 'run_id': self.request['run_id'],
             'execution_path': self.execution_path, 'registry_entry_digest': self.request['registry_entry_digest'],
             'run_mode': record['run_mode'], 'product_kind': record['product_kind'],
             'evidence_tier': V.producible(record['run_mode'], record['schema'])[1],
             'window': None, 'outcome_opened_at_freeze': False, 'frozen_at_utc': utc_now()}
        content_name, file_name = product_digest_names
        r[content_name] = record['canonical_content_digest']
        r[file_name] = sha256_hex(raw)
        return r

    def freeze_forecast(self, record: Mapping, declaration: Mapping) -> dict:
        """C1 then D1. The record must already be valid; it is validated again from the file bytes."""
        self._before_terminal()
        validate_forecast(record, declaration)
        raw = self._write('forecast', record)
        frozen = json.loads(raw)
        validate_forecast(frozen, declaration)
        receipt = self._receipt(V.FREEZE_RECEIPT, frozen, raw, ('forecast_content_digest', 'forecast_file_sha256'))
        receipt.update(cohort_id=None, status_at_freeze=status_at_freeze(frozen))
        validate_freeze_receipt(receipt, frozen)
        self._write('forecast_receipt', receipt)
        self.receipts.append(record_digest(receipt))
        return receipt

    def freeze_diagnostic(self, record: Mapping, declaration: Mapping) -> dict:
        """C2 then its diagnostic receipt."""
        self._before_terminal()
        validate_diagnostic(record, declaration)
        raw = self._write('diagnostic', record)
        frozen = json.loads(raw)
        validate_diagnostic(frozen, declaration)
        receipt = self._receipt(V.DIAGNOSTIC_RECEIPT, frozen, raw,
                                ('diagnostic_content_digest', 'diagnostic_file_sha256'))
        validate_diagnostic_receipt(receipt, frozen)
        self._write('diagnostic_receipt', receipt)
        self.receipts.append(record_digest(receipt))
        return receipt

    def terminal(self, outcome: str, reason: str) -> dict:
        """D2, written once. SUCCESS names every receipt issued; any other outcome names none, so
        receipts issued before a failure stay on disk, unnamed and never consumable (E2R-R38A)."""
        self._before_terminal()
        if outcome == 'SUCCESS' and not self.receipts:
            raise ValueError('SUCCESS needs at least one receipt')
        t = {'schema': V.TERMINAL, 'run_id': self.request['run_id'], 'game_id': self.request['game_id'],
             'method_id': self.request['method_id'], 'variant_id': self.request['variant_id'],
             'method_revision': self.request['method_revision'],
             'target_draw_number': self.request['target_draw_number'], 'execution_path': self.execution_path,
             'outcome': outcome, 'outcome_reason': reason,
             'registry_entry_digest': self.request['registry_entry_digest'],
             'receipt_digests': sorted(self.receipts) if outcome == 'SUCCESS' else []}
        validate_terminal(t)
        self.terminal_written = True
        self._write('terminal', t)
        return t

    def _before_terminal(self):
        if self.terminal_written:
            raise ValueError('the terminal record is already written; nothing follows it')


# Terminal outcome reasons with a fixed meaning (E2RC2-C02). A legitimate empty target, where the method
# validly reports no available TOP or WORST and declares no diagnostic record, has no output to publish;
# the frozen D2 vocabulary has no outcome for it, so D2 says VALIDATION_FAILURE with this reason prefix,
# and run_disposition() counts it as DIAGNOSTIC_ONLY (unscored, valid), never as a failure.
NO_TICKET_NO_DIAGNOSTIC = 'NO_TICKET_NO_DIAGNOSTIC'


def run_disposition(terminal: Mapping) -> str:
    """How reports count a run (section 7.4): SUCCESS, DIAGNOSTIC_ONLY (a valid empty target) or FAILED.
    A SUCCESS run's own records say whether it is scorable (record_status); this says only what the run
    produced. An invalid terminal record is FAILED."""
    try:
        validate_terminal(terminal)
    except ValueError:
        return 'FAILED'
    if terminal['outcome'] == 'SUCCESS':
        return 'SUCCESS'
    if terminal['outcome'] == 'VALIDATION_FAILURE' and terminal['outcome_reason'].startswith(NO_TICKET_NO_DIAGNOSTIC + ':'):
        return 'DIAGNOSTIC_ONLY'
    return 'FAILED'


def _installed_entry_for(receipt: Mapping, registry) -> dict | None:
    """The installed registry entry the receipt says admitted the run, if it is in that variant's chain."""
    try:
        chain = registry.chain(receipt['game_id'], receipt['method_id'], receipt['variant_id'])
    except ValueError:
        return None
    for e in chain:
        if record_digest(e) == receipt['registry_entry_digest']:
            return e
    return None


def read_run(folder: Path) -> dict:
    """The consumption check for a standalone contract run folder (E2R-R38A; reviewer's E2RC2-B02).

    Read-only. It establishes every gate itself, from current evidence, and fails closed; no caller can
    vouch for a gate. For each output (forecast, diagnostic) found, it returns (consumable, reason):
      - the global unresolved-orphan marker must be absent now (checked on every call);
      - the terminal record must exist, be valid, be SUCCESS and name the output's receipt;
      - the run must be STANDALONE: a COORDINATED run's group and exit-receipt gates have no evidence
        path in CODE-2, so it is never consumable here;
      - the folder must be <game>/<method>/<variant>/<run_id> of the records it holds;
      - the declaration is the installed one with the record's declaration digest, fetched afresh,
        never one the caller supplies;
      - the receipt's registry entry must be in that variant's installed chain, SUPPORTED, and name the
        same revision and declaration.
    The orphan marker and the installed registry are the fixed module constants; no caller can point
    this check at other evidence (reviewer's E2RC2-CODE-B01). Nothing is repaired, moved or deleted.
    """
    from _common.contract_registry import InstalledRegistry
    import _common.contract_registry as R
    import _common.contract_runner as CRun
    folder = Path(folder)
    marker = Path(CRun.ORPHAN_MARKER)

    def load(key):
        p = folder / FILES[key]
        if not p.is_file() or p.is_symlink():
            return None
        try:
            return json.loads(p.read_bytes().decode('ascii'))
        except (ValueError, UnicodeDecodeError):
            return 'UNREADABLE'
    terminal = load('terminal')
    result = {}
    for out_key, rec_key in (('forecast', 'forecast_receipt'), ('diagnostic', 'diagnostic_receipt')):
        output, receipt = load(out_key), load(rec_key)
        if output is None and receipt is None:
            continue
        result[out_key] = _consumable_here(folder, output, receipt, terminal, marker,
                                           Path(R.DATA_ROOT), InstalledRegistry)
    return result


def _consumable_here(folder, output, receipt, terminal, marker, data_root, InstalledRegistry) -> tuple[bool, str]:
    if marker.exists() or marker.is_symlink():
        return False, 'UNRESOLVED_ORPHAN_MARKER'
    if not isinstance(output, dict) or not isinstance(receipt, dict):
        return False, 'OUTPUT_OR_RECEIPT_MISSING_OR_UNREADABLE'
    if terminal is None:
        return False, 'NO_TERMINAL_RECORD'
    if not isinstance(terminal, dict):
        return False, 'INVALID_TERMINAL_RECORD: unreadable'
    if terminal.get('execution_path') != 'STANDALONE' or receipt.get('execution_path') != 'STANDALONE':
        return False, 'COORDINATED_EVIDENCE_NOT_AVAILABLE: only standalone runs are consumable in CODE-2'
    try:
        where = tuple(folder.parts[-4:])
        if where != (receipt['game_id'], receipt['method_id'], receipt['variant_id'], receipt['run_id']):
            return False, 'RUN_FOLDER_DOES_NOT_MATCH_RECORDS'
        registry = InstalledRegistry(data_root)
        declaration = registry.declaration(output['declaration_digest'])
    except (KeyError, TypeError, ValueError, OSError):
        return False, 'DECLARATION_NOT_INSTALLED'
    entry = _installed_entry_for(receipt, registry)
    if (entry is None or entry['registry_status'] != 'SUPPORTED' or
            entry['method_revision'] != output.get('method_revision') or
            entry['declaration_digest'] != output.get('declaration_digest')):
        return False, 'ADMITTING_ENTRY_NOT_INSTALLED_OR_NOT_SUPPORTED'
    # Every gate above is established here; consumable() then checks the records themselves.
    return consumable(output, receipt, terminal, gates_pass=True, declaration=declaration)
