"""REVIEW-GATED one-worker Windows synthetic coordinator lifecycle, NEVER science.

This module contains a real Popen implementation but CANNOT be entered unless
Powerball_Experiment_Coordinator.ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE is changed
from False after independent review and explicit owner authorisation.
It reuses the unchanged v0.6 POC's root/ancestry capture and orphan functions.
No signal or kill call is made in this module, including on exceptions.
No source data or outcomes are loaded. No scientific schema is registered.
"""
from __future__ import annotations

PIPE_READER_JOIN_TIMEOUT_SECONDS = 0.05

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import queue
import re
import subprocess
import sys
import threading
import time
import uuid

from .multigame_launch_spec import build_synthetic_launch_spec
from .multigame_coordinator_exit_receipt import issue_coordinator_receipt


def parse_synthetic_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description='REVIEW-GATED synthetic Windows lifecycle ONLY')
    p.add_argument('--synthetic-contract-test', action='store_true', required=True)
    p.add_argument('--game', choices=('POWERBALL', 'OZLOTTO'), required=True)
    p.add_argument('--target', type=int, required=True)
    p.add_argument('--timeout-seconds', type=float, default=25.0)
    p.add_argument('--poll-seconds', type=float, default=1.0)
    a = p.parse_args(argv)
    if not 0.5 <= a.poll_seconds <= 5.0:
        p.error('poll interval must be 0.5..5.0 seconds')
    if not 15.0 + 2*a.poll_seconds <= a.timeout_seconds <= 60.0:
        p.error('timeout requires RELEASE_WAIT_SECONDS + 2 x poll_seconds, up to 60')
    return a


def strict_release_eligibility(*, launch, worker, status: dict | None) -> None:
    """Worker identity must have been observed by real ancestry while alive."""
    if (status is None or worker.root_process is None or worker.root_create_time is None or
            worker.proc.poll() is not None or worker.experiment_member is None or
            worker.ownership_errors or worker.unmatched_status or
            any(status.get(k) != v for k, v in launch.identity().items()) or
            status.get('mode') != 'SYNTHETIC_CONTRACT_TEST' or
            status.get('state') != 'STARTED' or
            type(status.get('pid')) is not int or
            type(status.get('process_create_time_epoch')) not in (float, int) or
            status['pid'] != worker.experiment_member.pid or
            abs(status['process_create_time_epoch'] - worker.experiment_member.create_time) >= 0.001):
        raise ValueError('synthetic launch identity or live ancestry unverified')


def run_windows_synthetic(coordinator, argv: list[str]) -> int:
    """Intentionally unreachable under default source switches, no CLI override."""
    if (not coordinator.ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE or
            coordinator.ENABLE_SCIENTIFIC_COORDINATION or
            coordinator.ENABLE_PROCESS_TERMINATION or sys.platform != 'win32'):
        raise ValueError('Windows synthetic lifecycle is NOT AUTHORISED')
    args = parse_synthetic_args(argv)
    # Perform every static check before launching anything.
    group_id = 'syn-' + uuid.uuid4().hex
    run_id = 'mg-' + uuid.uuid4().hex
    synth_root = coordinator.ROOT / 'transitory_data' / 'multigame_synthetic_runs'
    methods_dir = coordinator.ROOT / 'src' / 'methods'
    if str(methods_dir) not in sys.path:
        sys.path.append(str(methods_dir))  # NEVER shadow coordinator_private.
    launch = build_synthetic_launch_spec(
        group_id=group_id, worker_sequence=1, run_id=run_id,
        game_id=args.game, draw_number=args.target, method_id='E_1',
        variant_id='SYNTHETIC_PLUMBING_V1', synthetic_root=synth_root)
    if launch.mode != 'SYNTHETIC_CONTRACT_TEST':
        raise ValueError('scientific launch in synthetic-only harness')
    coordinator.validate_environment()
    coordinator.POC_DIR.mkdir(parents=True, exist_ok=True)
    coordinator.require_no_unresolved_orphan()
    group = coordinator.POC_DIR / group_id
    if group.exists() or group.is_symlink() or launch.run_dir.exists() or launch.run_dir.is_symlink():
        raise ValueError('pre-existing group/run directory; fail closed')
    group.mkdir(exist_ok=False)
    coordinator.capture_environment(group)
    # Validate only approved arguments; no user-supplied paths/command strings.
    command = [str(coordinator.WRAPPER), *launch.command_arguments, '--await-coordinator-release']
    for arg in command[1:]:
        coordinator.safe_child_arg(arg)
    messages = queue.Queue(maxsize=coordinator.LINE_QUEUE_MAX)
    reader_done = threading.Event()
    logfile = group / 'worker_001.stdout.log'
    worker = None
    proc = None
    problem = ''
    orphan = False
    marker_write_failed = False
    released = False
    exit_verified = False
    receipt_path = None
    started_utc = coordinator.ISO()
    t0 = time.monotonic()

    def mark(reason: str) -> None:
        nonlocal orphan, marker_write_failed, problem
        problem = reason
        orphan = True
        if not coordinator.record_unresolved_orphan(group_id=group_id, reason=reason, worker=worker):
            marker_write_failed = True

    def drain(*, block: bool = False) -> None:
        if worker is None:
            return
        for n, line in coordinator.receive_messages(messages, poll_seconds=args.poll_seconds,
                                                     block=block):
            if n != 1:
                worker.reader_error = True
                continue
            worker.output_lines += 1
            worker.lines_tail.append(line)
            if line.startswith(('BEGIN ', 'RESULT ', 'DIGEST ', 'FINISH ')):
                if len(worker.console_publication_records) < 8:
                    worker.console_publication_records.append(line)
                else:
                    worker.reader_error = True
            if line.startswith('BEGIN '): worker.begin_seen = True
            if line.startswith('FINISH ') and line.endswith(' SUCCESS'): worker.finish_success_seen = True
            if line.startswith('RESULT '): worker.console_result = line[7:]
            if line.startswith('DIGEST '): worker.console_digest = line[7:]
            if line.startswith('READER_ERROR:'): worker.reader_error = True
            # Synthetic worker logs contain no lottery data; keep full evidence.
            print('[SYNTHETIC WORKER] ' + line, flush=True)

    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, text=True, encoding='utf-8',
                                errors='replace', bufsize=1, cwd=coordinator.ROOT, shell=False)
        reader = threading.Thread(target=coordinator.read_lines,
                                  args=(proc, 1, logfile, messages, reader_done),
                                  daemon=True, name='synthetic-output-1')
        worker = coordinator.Worker(1, run_id, proc, time.monotonic(),
                                    launch.run_dir, logfile, reader, reader_done)
        coordinator.register_root(worker)
        coordinator.capture_owned_tree(worker, force=True)
        reader.start()
        deadline = time.monotonic() + args.timeout_seconds
        while True:
            drain(block=True)
            coordinator.capture_owned_tree(worker, poll_seconds=args.poll_seconds)
            if not released and worker.proc.poll() is None and worker.experiment_member is not None:
                status = coordinator.read_status(launch.run_dir)
                if status is not None:
                    strict_release_eligibility(launch=launch, worker=worker, status=status)
                    if os.path.lexists(coordinator.UNRESOLVED_ORPHAN_MARKER):
                        raise ValueError('global orphan marker before release')
                    from _common.multigame_ancestry_release import release_document, RELEASE_NAME
                    path = launch.run_dir / RELEASE_NAME
                    if os.path.lexists(path):
                        raise ValueError('ancestry release collision')
                    # Bound to the status-reported creation time independently matched
                    # against captured ancestry, never a separately read process PID.
                    release = release_document(launch.identity(), pid=status['pid'],
                                 create_time_epoch=status['process_create_time_epoch'])
                    temporary = path.with_name(path.name + '.part-' + uuid.uuid4().hex)
                    try:
                        with temporary.open('xb') as fh:
                            fh.write(coordinator.canonical_bytes(release))
                            fh.flush()
                            os.fsync(fh.fileno())
                        os.link(temporary, path)  # atomic CREATE-ONLY across platforms
                    finally:
                        temporary.unlink(missing_ok=True)
                    released = True
            if proc.poll() is not None:
                worker.exit_observed_utc = coordinator.ISO()
                worker.exit_code = proc.returncode
                found, saved = coordinator.check_exited_worker_for_orphan(worker, group_id=group_id)
                if found:
                    orphan = True
                    marker_write_failed |= not saved
                    problem = 'orphan/uncertain descendants after wrapper exit'
                else:
                    worker.final_state = 'EXITED'
                break
            if time.monotonic() >= deadline:
                mark('synthetic wrapper still alive or exit uncertain after timeout; NO SIGNAL SENT')
                worker.final_state = 'TERMINATION_DISABLED'
                break
        # No waiting on an unexited worker's pipe; that would hang the coordinator.
        if proc.poll() is not None:
            pipe_end = time.monotonic() + coordinator.PIPE_EOF_WAIT_SECONDS
            while time.monotonic() < pipe_end and (not reader_done.is_set() or not messages.empty()):
                drain(block=True)
            drain()
            if not reader_done.is_set():
                mark('reader pipe did not reach EOF after wrapper exited')
            else:
                worker.reader.join(timeout=PIPE_READER_JOIN_TIMEOUT_SECONDS)
                if proc.stdout is not None:
                    proc.stdout.close()
            # The second v0.6 orphan check is obligatory even after terminal logs.
            found, saved = coordinator.check_exited_worker_for_orphan(worker, group_id=group_id)
            if found:
                orphan = True
                marker_write_failed |= not saved
                problem = 'late status or member evidence of orphan after exit'
        if not orphan and not released:
            # A vanished child may have escaped capture. In that case ownership
            # cannot be proven, even if the wrapper is known gone.
            mark('wrapper exited before positively verified synthetic-worker ancestry')
        if not orphan:
            ok, why, status = coordinator.status_and_result(worker, require_success=True)
            if not ok:
                problem = 'status/result validation refused: ' + why
            elif (worker.exit_code != 0 or worker.root_create_time is None or
                  worker.experiment_member is None or worker.ownership_errors or
                  worker.unmatched_status or worker.reader_error or
                  not reader_done.is_set() or not worker.exit_observed_utc):
                problem = 'process identity / exit / reader evidence incomplete'
            elif any(status.get(k) != v for k, v in launch.identity().items()):
                problem = 'terminal status identity mismatch'
            else:
                # Final secondary status-orphan check, before issuing receipt.
                found, saved = coordinator.check_exited_worker_for_orphan(worker, group_id=group_id)
                if found:
                    orphan = True
                    marker_write_failed |= not saved
                    problem = 'last exit-time orphan check refused'
                else:
                    receipts = group / 'receipts'
                    if receipts.exists() or receipts.is_symlink():
                        raise ValueError('receipts directory collision')
                    receipts.mkdir(exist_ok=False)
                    receipt_path = issue_coordinator_receipt(
                        group_dir=group, run_dir=launch.run_dir,
                        identity=launch.identity(),
                        coordinator_sha256=coordinator.sha256(Path(coordinator.__file__).read_bytes()),
                        root_pid=proc.pid, root_create_time_epoch=worker.root_create_time,
                        wrapper_exit_code=worker.exit_code,
                        exit_observed_utc=worker.exit_observed_utc,
                        console_publication_records=worker.console_publication_records)
                    exit_verified = True
    except Exception as exc:
        # Popen may have already started something; NEVER forget it on error.
        problem = f'synthetic coordinator exception: {type(exc).__name__}: {exc}'
        if proc is not None and not orphan:
            mark(problem)
    finally:
        if proc is not None and worker is not None and proc.poll() is not None:
            if worker.exit_observed_utc is None:
                worker.exit_observed_utc = coordinator.ISO()
            if not orphan:
                found, saved = coordinator.check_exited_worker_for_orphan(worker, group_id=group_id)
                if found:
                    orphan = True
                    marker_write_failed |= not saved
                    problem = 'late orphan before final group publication'
        success = bool(exit_verified and not orphan and not problem and not marker_write_failed
                       and not os.path.lexists(coordinator.UNRESOLVED_ORPHAN_MARKER))
        report = {'sequence': 1, 'run_id': run_id,
                  'state': 'SUCCESS' if success else 'FAILED',
                  'mode': 'SYNTHETIC_CONTRACT_TEST',
                  'receipt_path': str(receipt_path) if receipt_path else None,
                  'wrapper_pid': proc.pid if proc else None,
                  'exit_code': worker.exit_code if worker else None,
                  'exit_observed_utc': worker.exit_observed_utc if worker else None,
                  'verified_ancestry': bool(worker is not None and worker.experiment_member is not None)}
        group_record = {'schema': 'MULTIGAME_SYNTHETIC_GROUP_V1_REVIEW',
                        'engineering_only': True, 'mode': 'SYNTHETIC_CONTRACT_TEST',
                        'group_id': group_id, 'game_id': launch.game_id,
                        'draw_number': launch.draw_number, 'success': success,
                        'status': 'PASS' if success else 'FAIL',
                        'orphan_suspected': orphan, 'marker_write_failed': marker_write_failed,
                        'started_utc': started_utc, 'finished_utc': coordinator.ISO(),
                        'enable_process_termination': False,
                        'enable_scientific_coordination': False,
                        'issue': problem, 'workers': [report]}
        coordinator.save_new(group / 'manifest.json', coordinator.canonical_bytes(group_record))
        print(f'[SYNTHETIC COORDINATOR] {group_record["status"]} group={group_id} '
              f'run={run_id} manifest={group / "manifest.json"}', flush=True)
    # Even a genuine PASS is NON-SCIENTIFIC and is refused by the scientific consumer.
    return 0 if success else 1
