"""Synthetic, process-free regression: v0.4 unresolved-orphan fail-closed gate.

NO destructive process calls. Imported source is never run as coordinator_main().
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace

SOURCE = Path(__file__).resolve().parents[1] / 'src' / 'Powerball_Experiment_Coordinator.py'
spec = importlib.util.spec_from_file_location('p1p2_orphan_interlock_test_target', SOURCE)
assert spec and spec.loader
import sys
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def check():
    assert module.ENABLE_PROCESS_TERMINATION is False
    with tempfile.TemporaryDirectory(prefix='orphan_interlock_test_') as d:
        marker = Path(d) / 'UNRESOLVED_ORPHAN.json'
        prior = module.UNRESOLVED_ORPHAN_MARKER
        try:
            module.UNRESOLVED_ORPHAN_MARKER = marker
            module.require_no_unresolved_orphan()
            proc = SimpleNamespace(pid=1234, poll=lambda: None)
            worker = SimpleNamespace(sequence=1, run_id='synthetic_only_w001',
                                     proc=proc, root_create_time=123.456,
                                     experiment_member=None, unmatched_status='status missing',
                                     ownership_errors=['SYNTHETIC_UNVERIFIED'], owned_members={})
            module.record_unresolved_orphan(group_id='synthetic_only',
                                            reason='Non-destructive unit test', worker=worker)
            assert marker.exists()
            raw = marker.read_bytes()
            record = json.loads(raw)
            assert record['schema'] == 'ENGINEERING_UNRESOLVED_ORPHAN_V1'
            assert record['group_id'] == 'synthetic_only'
            assert record['worker']['root_pid'] == 1234
            assert record['worker']['experiment_matched'] is False
            assert 'BLOCK_FUTURE_RUNS' in record['action']
            try:
                module.require_no_unresolved_orphan()
            except RuntimeError as e:
                assert 'UNRESOLVED_ORPHAN' in str(e)
            else:
                raise AssertionError('Gate did not reject an unresolved marker')
            module.record_unresolved_orphan(group_id='different_group', reason='must not overwrite')
            assert marker.read_bytes() == raw, 'Existing marker was overwritten'
            # An invalid JSON marker also blocks; startup does not blindly trust data.
            marker.write_text('not json', encoding='utf-8')
            try:
                module.require_no_unresolved_orphan()
            except RuntimeError:
                pass
            else:
                raise AssertionError('Malformed marker was ignored')
            marker.unlink()
            module.require_no_unresolved_orphan()
        finally:
            module.UNRESOLVED_ORPHAN_MARKER = prior
    print('PASS: orphan gate absent/present/invalid; durable no-clobber marker; strict switch False (synthetic only)')
    print('NOT TESTED: Windows interruption/crashes, actual processes, or destructive termination')


if __name__ == '__main__':
    check()
