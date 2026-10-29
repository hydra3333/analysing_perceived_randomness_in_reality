#!/usr/bin/env python3
"""Synthetic only: show CODE-2 v2 authority-path overrides and coordinated publication.

Requires reviewed BASE_b846519 src/tests snapshot with CODE-2 v2 repo_overlay applied.
Run from any directory with PYTHONPATH set to <repo>/src:<repo>/src/methods:<repo>/tests.
Uses TemporaryDirectory and mock; no real master reads, process termination, or repository writes.
This is reviewer evidence, not a project installation script.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock
import json
import e2r_code2_fixtures as C
from _common import contract_publication as CP
from _common import contract_runner as CR
from _common import contract_registry as R
from _common.contract_dispatch import dispatch_gate, DispatchRefused
from contract_adapters import e_001

with TemporaryDirectory() as tmp:
    base = Path(tmp)
    live_marker = base / 'UNRESOLVED_ORPHAN.json'
    live_marker.write_text('synthetic marker only', encoding='ascii')
    fake_absent = base / 'no_marker_here'

    ws, master_sha = C.workspace(base / 'ws', 'POWERBALL', 1300)
    registry = R.InstalledRegistry()
    active = registry.active_entry('POWERBALL', *C.E1)
    decl = registry.declaration(active['declaration_digest'])
    req = C.request(decl, active, 1300, master_sha, run_id='mg-synthetic-review-0001')

    # Case A: Run-level unresolved-orphan safety bypass via a caller-supplied locator.
    with mock.patch.object(CR, 'ORPHAN_MARKER', live_marker):
        try:
            CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify,
                                   repo_root=ws, run_root=base / 'runs')
        except CR.RunRefused as exc:
            assert exc.reason == 'UNRESOLVED_ORPHAN_MARKER'
            print('A1: default marker blocks run:', exc.reason)
        else:
            raise AssertionError('expected default-marker refusal')
        success = CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify,
                                         repo_root=ws, run_root=base / 'runs',
                                         orphan_marker=fake_absent)
        assert success.outcome == 'SUCCESS' and live_marker.exists()
        print('A2: caller marker override admits run:', success.outcome)
        blocked = CP.read_run(success.folder)
        bypassed = CP.read_run(success.folder, orphan_marker=fake_absent)
        assert blocked['forecast'][0] is False and bypassed['forecast'][0] is True
        print('A3: default consumption blocked:', blocked['forecast'])
        print('A4: caller marker override marks consumed:', bypassed['forecast'])

    # Case B: A method's active installed registry is not supported, yet a caller may supply
    # a different data_root containing a fabricated supported entry; no scientific run follows.
    test_decl = C.release_declaration()
    closed = C.copy_data_root(base / 'closed_registry')
    C.install_declaration(closed, test_decl)
    C.append_entry(closed, C.entry(test_decl, 'FORMULA_OPEN'))
    alternate = C.copy_data_root(base / 'alternate_registry')
    C.install_declaration(alternate, test_decl)
    supported = C.entry(test_decl, 'SUPPORTED')
    C.append_entry(alternate, supported)
    req2 = C.request(test_decl, supported, 1300, master_sha)
    with mock.patch.object(R, 'DATA_ROOT', closed):
        try:
            dispatch_gate(req2, methods_root=base / 'methods')
        except DispatchRefused as exc:
            assert exc.reason == 'NOT_SUPPORTED'
            print('B1: default installed registry refuses:', exc.reason)
        else:
            raise AssertionError('expected not-supported refusal')
        admitted = dispatch_gate(req2, data_root=alternate, methods_root=base / 'methods')
        assert admitted[0]['registry_status'] == 'SUPPORTED'
        print('B2: caller alternate registry admits:', admitted[0]['registry_status'])

    # Case C: The standalone runner accepts coordinated execution without the rejecting
    # coordinated entry point. read_run correctly refuses consumption but D2 is already SUCCESS.
    other = C.request(decl, active, 1300, master_sha, run_id='mg-coord-review-0001')
    made = CR.run_contract_method(other, compute=e_001.compute, verify=e_001.verify,
                                  repo_root=ws, run_root=base / 'runs',
                                  execution_path='COORDINATED')
    terminal = json.loads((made.folder / 'terminal.json').read_text(encoding='ascii'))
    assert terminal['execution_path'] == 'COORDINATED' and terminal['outcome'] == 'SUCCESS'
    assert CP.read_run(made.folder)['forecast'][0] is False
    print('C1: standalone API published coordinated D2:', terminal['outcome'])
    print('C2: downstream read_run refuses it:', CP.read_run(made.folder)['forecast'])
print('All three synthetic bypass demonstrations reproduced; no installed files were touched.')
