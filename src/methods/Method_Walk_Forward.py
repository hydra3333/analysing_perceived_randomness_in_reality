"""WF-1A walk-forward driver (releases and WF-1 design v0.1r1 section 5). Launched as: Run_Experiment.bat Method_Walk_Forward.py ...

  plan   --game G --first S --last L    Freeze a batch plan for every released variant of game G over targets
                                        S..L (S >= the era's first draw + 1; L below the holdout), append one
                                        WF_BATCH search-log row, and print the batch ID.
  run    --game G --batch ID            Run the plan: one standalone contract run per (variant, target), in order;
                                        re-running the same command resumes. Stops at once on any refusal, data-
                                        admission failure, interruption or unrecognised outcome (the STOP rule).
  status --game G --batch ID            Print the counts by variant. Read-only.

Every run goes through the unchanged contract runner and its dispatch gate; the driver adds no other path. No
subprocess, timer, termination or coordinator is involved. It reads no results and scores nothing.
Exit codes: 0 done (or plan made, or status printed); 1 stopped; 2 refused, or invalid arguments.
"""
from __future__ import annotations

import argparse
import json
import sys

from Method_Contract_Runner import ADAPTERS


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='WF-1A walk-forward driver')
    sub = parser.add_subparsers(dest='command', required=True)
    plan = sub.add_parser('plan')
    plan.add_argument('--game', required=True)
    plan.add_argument('--first', type=int, required=True)
    plan.add_argument('--last', type=int, required=True)
    for name in ('run', 'status'):
        p = sub.add_parser(name)
        p.add_argument('--game', required=True)
        p.add_argument('--batch', required=True)
    args = parser.parse_args(argv)

    import _common.walk_forward as WF
    try:
        if args.command == 'plan':
            made = WF.make_plan(args.game, args.first, args.last, ADAPTERS)
            print(f"[WALK-FORWARD] PLAN {made['batch_id']}: {args.game} targets {args.first}-{args.last}, "
                  f"{len(made['cohort'])} variants, master {made['master_sha256'][:12]}...", flush=True)
            print(f"[WALK-FORWARD] next: Run_Experiment.bat Method_Walk_Forward.py run --game {args.game} "
                  f"--batch {made['batch_id']}", flush=True)
            return 0
        if args.command == 'run':
            return WF.run_batch(args.game, args.batch, ADAPTERS, echo=lambda s: print(s, flush=True))
        print(json.dumps(WF.status(args.game, args.batch), indent=1, sort_keys=True), flush=True)
        return 0
    except (WF.BatchRefused, ValueError) as exc:
        print(f'[WALK-FORWARD] REFUSED: {exc}. Nothing was run.', file=sys.stderr, flush=True)
        return 2


if __name__ == '__main__':
    sys.exit(main())
