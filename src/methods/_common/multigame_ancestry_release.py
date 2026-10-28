"""Synthetic-only cooperative ancestry handshake; NOT proof of exit.

The worker publishes STARTED first, then waits for a coordinator-authored
create-only release matching its actual process identity. The coordinator
independently validates live ancestry; a forged release cannot grant any
receipt or ownership. This module never executes a command or reads datasets.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import time

from .multigame_standalone_contract import json_bytes

RELEASE_NAME = 'coordinator_ancestry_release.json'
RELEASE_POLL_SECONDS = 0.5
RELEASE_WAIT_SECONDS = 15.0


def release_document(identity: dict, *, pid: int, create_time_epoch: float) -> dict:
    if (type(identity) is not dict or type(pid) is not int or pid <= 0 or
            type(create_time_epoch) not in (int, float) or create_time_epoch <= 0):
        raise ValueError('invalid ancestry release identity')
    return {'schema': 'SYNTHETIC_ANCESTRY_RELEASE_V1_REVIEW',
            **identity, 'pid': pid, 'process_create_time_epoch': create_time_epoch,
            'not_exit_evidence': True}


def await_release(*, run_dir: Path, identity: dict, pid: int,
                  create_time_epoch: float, orphan_marker: Path,
                  timeout_seconds: float = RELEASE_WAIT_SECONDS) -> None:
    if not 0.1 <= timeout_seconds <= 30:
        raise ValueError('invalid ancestry release timeout')
    expected = json_bytes(release_document(identity, pid=pid,
                                           create_time_epoch=create_time_epoch))
    candidate = run_dir / RELEASE_NAME
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if os.path.lexists(orphan_marker):
            raise ValueError('global orphan interlock while awaiting ancestry release')
        if candidate.is_symlink():
            raise ValueError('unsafe ancestry release symlink')
        if candidate.exists():
            # Byte comparison, not a worker claim of ancestry or process exit.
            if not candidate.is_file() or candidate.stat().st_size > 2048:
                raise ValueError('invalid ancestry release file')
            # A present but incomplete file is still an unpublished signal;
            # a complete wrong identity is terminal evidence of tampering.
            if candidate.stat().st_size < len(expected):
                time.sleep(RELEASE_POLL_SECONDS)
                continue
            if candidate.read_bytes() != expected:
                raise ValueError('ancestry release identity mismatch')
            return
        time.sleep(RELEASE_POLL_SECONDS)
    raise TimeoutError('coordinator ancestry release was not observed')
