"""E_2-readiness contract (E2R-1 v0.3r3): one standalone contract run, from request to terminal record.

E2R-CODE-2. Orchestration side; imports no method code (the caller passes the method's compute and
verify functions). The order is fixed:
  1. refusals that read no data: the unresolved-orphan marker, the real-development switch, then the
     dispatch gate (E2R-R57). A refused request creates no folder and reads no data;
  2. the run folder is created exclusively, so every later failure ends in a terminal record;
  3. the reader loads the pinned prefix-only DrawView (it verifies the pin, the ledger and INIT);
  4. the frozen MethodTask is built; the method computes once from (task, view);
  5. the contract assembles C1 and/or C2, the method's own verify() checks them, and they are
     published in E2R-R38A order, ending with the D2 terminal record.
Nothing here deletes, moves, retries, kills or recovers anything.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import stat

import _common.contract_vocab as V
from _common.contract_dispatch import DispatchRefused, dispatch_gate, refusal_text
from _common.contract_forecast import assemble_diagnostic, assemble_forecast
from _common.contract_publication import NO_TICKET_NO_DIAGNOSTIC, RunPublication
from _common.contract_records import reader_pin, record_digest
from _common.contract_task import build_method_task
from _common.game_draws_reader import load_pinned_draw_view

# Code-level gate: contract runs on the real development masters. Turned ON by package WF-1A (releases and
# WF-1 design v0.1r1 section 5.5; owner decision WF1-3, ratified 31 October 2026): it admits standalone runs of
# released variants on the development prefix only; the reader still refuses every holdout target. It cannot
# be set by a command-line flag or an environment variable.
ENABLE_CONTRACT_REAL_DEVELOPMENT = True

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ORPHAN_MARKER = PROJECT_ROOT / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'
_FORBIDDEN_WORKSPACE_PARTS = ('source_data', 'results', 'transitory_data', 'src', 'tests', 'doc', 'review',
                              'exchange')


class RunRefused(Exception):
    """Refused before any data was read and before any folder was created."""

    def __init__(self, text: str, reason: str):
        super().__init__(text)
        self.text = text
        self.reason = reason


@dataclass(frozen=True)
class RunResult:
    folder: Path
    outcome: str
    reason: str
    terminal: dict


def check_synthetic_workspace(workspace: Path, project_root: Path = PROJECT_ROOT) -> Path:
    """A synthetic workspace holds its own invented masters. It may never be the project itself or
    sit inside any of the project's data, results, code or record folders."""
    ws = Path(workspace).resolve()
    proj = Path(project_root).resolve()
    if ws == proj:
        raise ValueError('a synthetic workspace cannot be the project root')
    if ws.is_relative_to(proj):
        first = ws.relative_to(proj).parts[0]
        if first.casefold() in _FORBIDDEN_WORKSPACE_PARTS:
            raise ValueError(f'a synthetic workspace cannot be inside the project folder {first}/')
    return ws


def _file_sha256(path: Path) -> str:
    """SHA-256 of a regular, single-link, non-symlink file (the reader's own source-file rule)."""
    st = os.lstat(path)
    if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
        raise ValueError(f'{path.name}: not a plain single-link file')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_provenance(repo_root: Path, request: Mapping) -> dict:
    """Receipt provenance (section 8.1; orchestration only, never in any record's content). Called only
    after the reader has verified the pin, the ledger and the INIT record for this request."""
    folder = Path(repo_root) / 'source_data'
    game = request['game_id']
    return {'master_file': request['master_file'], 'ledger_version': request['ledger_version'],
            'master_sha256': request['master_sha256'],
            'ledger_sha256': _file_sha256(folder / f'{game}_results_master_ledger.csv'),
            'init_record_sha256': _file_sha256(folder / f'{game}_results_master_init_verification.json')}


def _numeric(exc: BaseException) -> bool:
    text = str(exc).lower()
    return any(w in text for w in ('non-finite', 'nan', 'infinity', 'negative zero', 'outside int64'))


def run_contract_method(request: Mapping, *, compute: Callable, verify: Callable, repo_root: Path,
                        run_root: Path) -> RunResult:
    """Run one admitted request, as a STANDALONE run. Raises RunRefused or DispatchRefused before
    anything is read or created; otherwise always returns a RunResult whose terminal record is on disk.

    Reviewer's E2RC2-CODE-B01 and B02: the orphan marker, the installed registry and the method folders
    are the fixed module constants, and no caller can choose them; there is no execution-path
    parameter, so this runner can never publish a COORDINATED run. The data source is fixed too: a
    REAL_DEVELOPMENT run (switched off) may only read the project itself, and a synthetic run only a
    workspace outside the project's data, results, code and record folders."""
    r = request if isinstance(request, Mapping) else {}
    ident = (r.get('game_id'), r.get('method_id'), r.get('variant_id'), r.get('method_revision'))
    marker = Path(ORPHAN_MARKER)
    if marker.exists() or marker.is_symlink():
        raise RunRefused(refusal_text(*ident, 'UNRESOLVED_ORPHAN_MARKER: no experiment is permitted'),
                         'UNRESOLVED_ORPHAN_MARKER')
    if r.get('run_mode') == 'REAL_DEVELOPMENT' and ENABLE_CONTRACT_REAL_DEVELOPMENT is not True:
        raise RunRefused(refusal_text(*ident, 'REAL_DEVELOPMENT_DISABLED: contract runs on the real '
                                      'development masters are switched off'), 'REAL_DEVELOPMENT_DISABLED')
    try:
        if r.get('run_mode') == 'REAL_DEVELOPMENT':
            if Path(repo_root).resolve() != PROJECT_ROOT.resolve():
                raise ValueError('a real development run reads only the project itself')
        else:
            check_synthetic_workspace(repo_root)
    except ValueError as exc:
        raise RunRefused(refusal_text(*ident, f'DATA_SOURCE_REFUSED: {exc}'), 'DATA_SOURCE_REFUSED') from None
    entry, declaration = dispatch_gate(request)                   # reads no data
    pub = RunPublication(run_root, request, entry_digest=record_digest(entry), provenance={})

    def end(outcome, reason):
        return RunResult(pub.folder, outcome, reason, pub.terminal(outcome, reason))

    try:
        try:
            view = load_pinned_draw_view(repo_root=Path(repo_root), run_manifest=reader_pin(request))
            pub.provenance = source_provenance(repo_root, request)
            task = build_method_task(request, declaration, view)
        except Exception as exc:
            return end('VALIDATION_FAILURE', f'DATA_ADMISSION_REFUSED: {type(exc).__name__}: {exc}')
        try:
            output = compute(task, view)
        except Exception as exc:
            return end('NUMERIC_INVALID' if _numeric(exc) else 'RUNTIME_FAILURE',
                       f'METHOD_FAILED: {type(exc).__name__}: {exc}')
        try:
            try:
                forecast_product = V.producible(task.run_mode, V.FORECAST)[0]
            except ValueError:
                forecast_product = None
            c1 = (assemble_forecast(declaration, task, view, output)
                  if task.product_kind == forecast_product else None)
            c2 = (assemble_diagnostic(declaration, task, view, output)
                  if declaration['diagnostic_schema_id'] is not None else None)
            if c1 is None and c2 is None:
                # assemble_forecast returns None only for a valid output with no available TOP or WORST
                # (any invalid output raises). Section 7.4: with no diagnostic declared, that target is a
                # legitimate empty target, counted DIAGNOSTIC_ONLY; with a diagnostic declared, the method
                # owed its C2 record and the output is invalid (E2RC2-C02).
                if task.product_kind == forecast_product and declaration['diagnostic_schema_id'] is None:
                    verify(task, view, None, None)
                    return end('VALIDATION_FAILURE', f'{NO_TICKET_NO_DIAGNOSTIC}: valid output with no available '
                                                     'TOP or WORST and no declared diagnostic; DIAGNOSTIC_ONLY, unscored')
                raise ValueError('no record: the declared diagnostic record is missing, or the request asks for '
                                 'a product this output cannot give')
            verify(task, view, c1, c2)
        except Exception as exc:
            return end('NUMERIC_INVALID' if _numeric(exc) else 'VALIDATION_FAILURE',
                       f'CONTRACT_REFUSED_OUTPUT: {type(exc).__name__}: {exc}')
        if c1 is not None:
            pub.freeze_forecast(c1, declaration)
        if c2 is not None:
            pub.freeze_diagnostic(c2, declaration)
        status = c1['record_status'] if c1 is not None else 'DIAGNOSTIC_ONLY'
        return end('SUCCESS', f'PUBLISHED: {status}')
    except (Exception, KeyboardInterrupt) as exc:
        # Publication itself failed, or the run was interrupted: record that, if the terminal record
        # can still be written. Receipts already issued stay on disk, unnamed and never consumable.
        if pub.terminal_written:
            raise
        reason = 'INTERRUPTED' if isinstance(exc, KeyboardInterrupt) else f'PUBLICATION_FAILED: {type(exc).__name__}: {exc}'
        return end('RUNTIME_FAILURE', reason)


__all__ = ['ENABLE_CONTRACT_REAL_DEVELOPMENT', 'RunRefused', 'DispatchRefused', 'RunResult',
           'run_contract_method', 'check_synthetic_workspace', 'source_provenance']
