"""MHUP-A: the Mode H study's owner commands (design v0.1r5 sections 4.1, 4.2, 5.2-5.4, 6.7).
Launched as: Run_Evaluation.bat Method_Mode_H.py <command> --game G [--statement "..."]

  manifest          --game G             Write the study manifest (4.1): cohort, targets, exposure flags, measures,
                                         families, N1 policy, v_f, the closure and environment inventories. Create-only.
  open              --game G --statement Write the opening record (4.2) after the manifest; the owner types the fixed
                                         sentence. Create-only, permanent. The display rule of the holdout stays.
  advance           --game G --statement Write the study version advance (4.1) when the ledger holds rows beyond the
                                         admitted version, after Claude's and the reviewer's written agreement.
  declare-developed --game G --statement Write the GOAL-1 record (6.7) after the Mode H seal.
  score             --game G             The one Mode H score attempt (5.2-5.4), resumable; never a second one.
  statements                             Print the three fixed owner sentences.

Each record is written once; a second write refuses. Nothing here runs a method or reads a draw except the score,
which reads the ten holdout outcomes once, under the freeze-before-outcome rule, after SCORING_STARTED.
Exit codes: 0 done; 1 failed after a record was written (the record stays; the next run resumes); 2 refused before
anything was written, or invalid arguments.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (str(HERE.parent / 'methods'), str(HERE.parent)):
    if p not in sys.path:
        sys.path.insert(0, p)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='MHUP-A Mode H study commands')
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('manifest', 'open', 'advance', 'declare-developed', 'score'):
        sp = sub.add_parser(name)
        sp.add_argument('--game', required=True, choices=('POWERBALL', 'OZLOTTO'))
        if name in ('open', 'advance', 'declare-developed'):
            sp.add_argument('--statement', required=True, help='the fixed owner sentence, typed exactly')
    sub.add_parser('statements')
    args = parser.parse_args(argv)

    import _common.contract_publication as CP
    import _common.owner_records as OR
    from evaluation import mode_h as MH

    def echo(text: str) -> None:
        print(f'[MODE-H] {text}', flush=True)

    if args.command == 'statements':
        for name, text in (('open', OR.OPENING_STATEMENT), ('advance', OR.ADVANCE_STATEMENT),
                           ('declare-developed', OR.DEVELOPED_STATEMENT)):
            print(f'{name}: {text}')
        return 0
    try:
        if args.command == 'manifest':
            rec = MH.manifest(args.game)
            echo(f"MANIFEST written for {args.game}: {len(rec['cohort'])} variants, targets {rec['targets'][0]}-"
                 f"{rec['targets'][-1]}, frozen master version {rec['freeze_version']}, closure {rec['closure']['count']} "
                 f"files, digest {rec['closure']['digest'][:12]}..., environment digest {rec['environment']['digest'][:12]}...")
            return 0
        if args.command == 'open':
            rec = MH.open_holdout(args.game, args.statement)
            echo(f"HOLDOUT OPENED for {args.game}: freeze version {rec['freeze_version']}; the opening record is permanent. "
                 f"The display rule is unchanged: no outcome of a holdout draw is shown or computed with outside the "
                 f"sealed Mode H score.")
            return 0
        if args.command == 'advance':
            rec = MH.advance(args.game, args.statement)
            echo(f"STUDY VERSION ADVANCED for {args.game}: admitted version {rec['admitted_version_before']} -> "
                 f"{rec['admitted_version_after']} ({len(rec['rows_beyond_admitted'])} row(s) named); the Mode H report "
                 f"discloses it")
            return 0
        if args.command == 'declare-developed':
            rec = MH.declare_developed(args.game, args.statement)
            echo(f"DEVELOPED declared for {args.game} (GOAL-1): Mode H score digest {rec['mode_h_score_digest'][:12]}...")
            return 0
        # score
        from evaluation import n1 as N1
        from evaluation import seed_policies as SP
        try:
            policy, on_file = SP.approved_policy(), SP.count_policies()
        except ValueError as exc:
            print(f'[MODE-H] REFUSED: seed policy records are invalid: {exc}. Nothing was written.', file=sys.stderr)
            return 2
        seed_line = (f"policy {policy['policy_id']}, R = {N1.R}" if policy else 'N1_NOT_RUN: seed policy not approved')
        env = {k: v for k, v in CP.environment_identity().items() if k in ('python_version', 'numpy_version', 'os_name')}
        res = MH.score(args.game, echo=echo, n1_runner=(N1.runner(policy) if policy else None), seed_line=seed_line,
                       n1_policies_on_file=on_file, environment=env)
        echo(f"SEALED: attempt {res['attempt_id']}, batch {res['batch_id']}, search-log row {res['search_log_row']}, "
             f"{res['scores']} score lines, {res['ranks']} rank lines")
        for p in res['paths']:
            echo(f'wrote {p}')
        return 0
    except MH.ModeHRefused as exc:
        print(f'[MODE-H] REFUSED: {exc}. Nothing was written by this command.', file=sys.stderr, flush=True)
        return 2
    except Exception as exc:
        print(f'[MODE-H] FAILED: {type(exc).__name__}: {exc}. Records written so far stay; a rerun resumes.',
              file=sys.stderr, flush=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
