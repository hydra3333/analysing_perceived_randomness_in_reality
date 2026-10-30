"""Standalone E_2-readiness contract runner (E2R-CODE-2). Launched as: Run_Experiment.bat Method_Contract_Runner.py ...

  pins  --game G --method M --variant V
        Print what a request must pin for that method variant now (installed registry only).
  run   --game G --method M --variant V --revision R --target N --view VIEW [--dates]
        --mode SYNTHETIC_CONTRACT_TEST --declaration-digest D --registry-entry-digest E
        --master-sha256 S --workspace DIR
        One run through the dispatch gate. Synthetic runs read only the invented masters of the given
        workspace and publish under DIR/contract_runs/<game>/<method>/<variant>/<run_id>/.

Every run is refused before any data is read unless the dispatch gate admits it (E2R-R57). Contract
runs on the real development masters are switched off in the shared runner (a code-level switch).
No subprocess, timer, termination or coordinator is involved. Exit codes: 0 SUCCESS; 1 a run that
ended in a non-SUCCESS terminal record; 2 refused, or invalid arguments.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from contract_adapters import e_001
from E_006 import contract as e_006

# The methods this runner can dispatch. Being listed here is not permission: the dispatch gate decides.
# A new contract method adds one line here and nothing else in this file (E_6 design note, D6-1).
ADAPTERS = {'E_1': e_001, 'E_6': e_006}


def build_request(args, run_id: str) -> dict:
    from _common.contract_vocab import FORECAST, RUN_REQUEST, producible
    return {'schema': RUN_REQUEST, 'game_id': args.game, 'method_id': args.method, 'variant_id': args.variant,
            'method_revision': args.revision, 'target_draw_number': args.target,
            'observation_view': args.view, 'include_dates': args.dates, 'run_mode': args.mode,
            'product_kind': producible(args.mode, FORECAST)[0],
            'declaration_digest': args.declaration_digest, 'registry_entry_digest': args.registry_entry_digest,
            'run_id': run_id, 'master_file': f'{args.game}_results_master.csv', 'ledger_version': 1,
            'master_sha256': args.master_sha256}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='E_2-readiness contract runner')
    sub = parser.add_subparsers(dest='command', required=True)
    pins = sub.add_parser('pins')
    run = sub.add_parser('run')
    for p in (pins, run):
        p.add_argument('--game', required=True)
        p.add_argument('--method', required=True)
        p.add_argument('--variant', required=True)
    run.add_argument('--revision', required=True)
    run.add_argument('--target', type=int, required=True)
    run.add_argument('--view', required=True)
    run.add_argument('--dates', action='store_true')
    run.add_argument('--mode', required=True)
    run.add_argument('--declaration-digest', required=True)
    run.add_argument('--registry-entry-digest', required=True)
    run.add_argument('--master-sha256', required=True)
    run.add_argument('--workspace', type=Path, default=None, help='synthetic runs only')
    args = parser.parse_args(argv)

    from _common.contract_dispatch import DispatchRefused, active_pins
    if args.command == 'pins':
        try:
            for k, v in active_pins(args.game, args.method, args.variant).items():
                print(f'{k}: {v}')
        except ValueError as exc:
            print(f'[CONTRACT] no registry chain: {exc}', file=sys.stderr)
            return 2
        return 0

    from _common import contract_runner as CR
    from _common.contract_publication import new_run_id
    if args.mode == 'REAL_DEVELOPMENT':
        if args.workspace is not None:
            parser.error('--workspace is for synthetic runs only')
        repo_root = CR.PROJECT_ROOT
        run_root = CR.PROJECT_ROOT / 'transitory_data' / 'contract_runs'
    else:
        if args.workspace is None:
            parser.error('a synthetic run needs --workspace')
        try:
            repo_root = CR.check_synthetic_workspace(args.workspace)
        except ValueError as exc:
            parser.error(str(exc))
        run_root = repo_root / 'contract_runs'
    adapter = ADAPTERS.get(args.method)
    try:
        request = build_request(args, new_run_id())
    except ValueError as exc:
        print(f'[CONTRACT] DISPATCH REFUSED: invalid run mode: {exc}. No data was read.', file=sys.stderr)
        return 2
    try:
        if adapter is None:
            # The same gate first, so an unregistered or unsupported method gets the standard refusal.
            from _common.contract_dispatch import dispatch_gate, refusal_text
            dispatch_gate(request)
            raise DispatchRefused(refusal_text(args.game, args.method, args.variant, args.revision,
                                               'NO_CONTRACT_WRAPPER: this runner has no wrapper for the method'),
                                  'NO_CONTRACT_WRAPPER')
        result = CR.run_contract_method(request, compute=adapter.compute, verify=adapter.verify,
                                        repo_root=repo_root, run_root=run_root)
    except (DispatchRefused, CR.RunRefused) as exc:
        print(f'[CONTRACT] {exc.text}', file=sys.stderr, flush=True)
        return 2
    print(f'[CONTRACT] {result.outcome} run={request["run_id"]} reason={result.reason}', flush=True)
    print(f'[CONTRACT] folder={result.folder}', flush=True)
    return 0 if result.outcome == 'SUCCESS' else 1


if __name__ == '__main__':
    sys.exit(main())
