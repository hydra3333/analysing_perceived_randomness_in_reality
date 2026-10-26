"""Package 2 OFFLINE review candidate for coordinated-method console records.

This module neither launches nor controls processes, and does NOT update the
existing P2 coordinator. In particular, it does not authorise coordinated
method execution. Its parser is intentionally stricter than the current POC
coordinator's token flags; production integration requires separate review.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Sequence

from _common.multigame_standalone_contract_v1 import json_bytes

_ID = re.compile(r'[A-Z][A-Z0-9]*\Z', re.ASCII)
_METHOD = re.compile(r'E_[1-9][0-9]*\Z', re.ASCII)
_RUN = re.compile(r'mg-[a-z0-9][a-z0-9_-]{7,95}\Z', re.ASCII)
_HEX = re.compile(r'[a-f0-9]{64}\Z', re.ASCII)


def _check_ids(game_id: str, method_id: str, run_id: str, target: int) -> None:
    if (not isinstance(game_id, str) or _ID.fullmatch(game_id) is None or
            not isinstance(method_id, str) or _METHOD.fullmatch(method_id) is None or
            not isinstance(run_id, str) or _RUN.fullmatch(run_id) is None or
            type(target) is not int or target < 1):
        raise ValueError('invalid console identity')


def prepare_success_records(*, game_id: str, method_id: str,
                            run_id: str, target: int, result: dict) -> tuple[str, ...]:
    """Construct the exact four protocol lines; DOES NOT publish a result."""
    _check_ids(game_id, method_id, run_id, target)
    if (type(result) is not dict or result.get('game_id') != game_id or
            result.get('method_id') != method_id or result.get('draw_number') != target or
            result.get('draw_key') != f'{game_id}_{target}'):
        raise ValueError('console/result identity mismatch')
    raw = json_bytes(result)
    return (
        f'BEGIN {method_id} game={game_id} draw={target} run={run_id}',
        'RESULT ' + raw.decode('ascii').removesuffix('\n'),
        'DIGEST ' + hashlib.sha256(raw).hexdigest(),
        f'FINISH {method_id} game={game_id} draw={target} run={run_id} SUCCESS',
    )


def verify_success_records(lines: Sequence[str], *, game_id: str, method_id: str,
                           run_id: str, target: int, canonical_result: bytes) -> None:
    """Validate console/JSON binding, exact order, uniqueness and identities.

    Intended as a new REQUIRED gate *in addition to* coordinator lifecycle,
    ancestry, process exit, status, orphan and failure-firewall gates.
    """
    _check_ids(game_id, method_id, run_id, target)
    if (not isinstance(canonical_result, bytes) or not canonical_result or
            len(canonical_result) > 2_000_000):
        raise ValueError('invalid canonical record')
    try:
        parsed = json.loads(canonical_result)
        if type(parsed) is not dict or json_bytes(parsed) != canonical_result:
            raise ValueError('noncanonical result')
    except (UnicodeError, json.JSONDecodeError) as ex:
        raise ValueError('invalid result JSON') from ex
    expected = prepare_success_records(game_id=game_id, method_id=method_id,
        run_id=run_id, target=target, result=parsed)
    if not isinstance(lines, (list, tuple)) or any(type(s) is not str for s in lines):
        raise ValueError('invalid console transcript')
    # Unlike the POC coordinator, reject duplicate publication markers.
    markers = tuple(s for s in lines if s.startswith(('BEGIN ', 'FINISH ', 'RESULT ', 'DIGEST ')))
    if markers != expected:
        raise ValueError('missing, duplicated, reordered or mismatched console records')
    for line in lines:
        if line.startswith('READER_ERROR:'):
            raise ValueError('console reader failed')


def verify_failed_records(lines: Sequence[str], *, game_id: str, method_id: str,
                          run_id: str, target: int) -> None:
    """Failure may not announce result, digest or successful finish."""
    _check_ids(game_id, method_id, run_id, target)
    if not isinstance(lines, (list,tuple)) or any(type(s) is not str for s in lines):
        raise ValueError('invalid console transcript')
    if any(s.startswith(('RESULT ', 'DIGEST ', 'FINISH ')) and s.endswith(' SUCCESS')
           or s.startswith(('RESULT ', 'DIGEST ', 'READER_ERROR:')) for s in lines):
        raise ValueError('failed run contains prohibited success/reader record')
    if sum(s.startswith('BEGIN ') for s in lines) > 1:
        raise ValueError('duplicate BEGIN')
    for s in lines:
        if s.startswith('BEGIN ') and s != f'BEGIN {method_id} game={game_id} draw={target} run={run_id}':
            raise ValueError('failed run BEGIN mismatch')
        if s.startswith('FINISH ') and s != f'FINISH {method_id} game={game_id} draw={target} run={run_id} FAILED':
            raise ValueError('invalid failure finish')
