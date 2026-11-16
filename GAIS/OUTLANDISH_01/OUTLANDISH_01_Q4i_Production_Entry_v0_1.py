#!/usr/bin/env python3
"""Single owner-controlled entry for shared Powerball/Oz Q4h science.

Independent game scan switches default OFF. Each requires a separate owner
authorisation commit. The Q4h runner checks the correct gate again at the
actual scan boundary; constructing modes and reading old COMPLETE results
do not require scan authorisation. Oz D6 does not reopen Powerball.
"""
from __future__ import annotations

import argparse

ENABLE_Q5_PRODUCTION_SCANS = False  # OWNER Q5 GATE: keep False until separate approval!
#ENABLE_Q5_PRODUCTION_SCANS = True  # prior 16 Nov owner Q5 authority is CLOSED
ENABLE_OZ_PRODUCTION_SCANS = False  # OWNER OZ GATE: NO Oz REAL scans authorised


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--game', choices=('powerball','oz'), default='powerball',
                        help='select pinned game; default retains old Powerball CLI')
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('status', help='show the scan switch, without accessing production inputs')
    preflight = sub.add_parser('preflight',
                               help='OWNER-PERMITTED read-only receipt/sample check; no scan')
    preflight.add_argument('--constant', required=True,
                           choices=('pi','phi','e','log2','gamma','lemniscate'))
    scan = sub.add_parser('scan', help='new REAL game scan; requires that game switch True')
    scan.add_argument('--constant', required=True,
                      choices=('pi','phi','e','log2','gamma','lemniscate'))
    scan.add_argument('--run-id', required=True, help='new REAL_... run identifier')
    report = sub.add_parser('report', help='create report from existing COMPLETE REAL run')
    report.add_argument('--constant', required=True,
                        choices=('pi','phi','e','log2','gamma','lemniscate'))
    report.add_argument('--run-id', required=True)
    ag = sub.add_parser('aggregate', help='create game-specific REAL-only Holm from six COMPLETE reports')
    ag.add_argument('--aggregate-id', required=True, help='REAL_AGGREGATE_<game>_...')
    ag.add_argument('--runs', required=True, nargs=6,
                    metavar='REAL_ID',help='six run IDs in order: pi phi e log2 gamma lemniscate')
    args = parser.parse_args()
    if args.action == 'status':
        if args.game == 'powerball':
            print('Q5 PRODUCTION POWERBALL SCANS:', 'ENABLED' if ENABLE_Q5_PRODUCTION_SCANS else 'DISABLED')
        else:
            print('OZ LOTTO PRODUCTION SCANS:', 'ENABLED' if ENABLE_OZ_PRODUCTION_SCANS else 'DISABLED')
        return
    # Check only the corresponding named owner gate, before opening any inputs.
    enabled = ENABLE_Q5_PRODUCTION_SCANS if args.game == 'powerball' else ENABLE_OZ_PRODUCTION_SCANS
    if args.action == 'scan' and enabled is not True:
        raise SystemExit('SAFETY STOP: ' + args.game + ' production scans DISABLED; '
                         'separate owner git authorisation required')

    from OUTLANDISH_01_Q4i_Mode_v0_1 import PowerballMode
    mode = PowerballMode.production(args.game)
    if args.action == 'preflight':
        # This is an explicit operator action only: never called automatically.
        # Verifies receipt fields, size and 12 sampled blocks without full-file scan,
        # without reading historical outcomes, and without creating any output.
        # Owner must separately authorise actually invoking this action.
        from OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 import validate_published_source
        checked = validate_published_source(mode.roots, args.constant)
        print('READ-ONLY PREFLIGHT PASS:', checked.constant, 'bytes=', checked.packed_bytes,
              'receipt_sha256=', checked.receipt_sha256,
              'expected_full_scan_sha256=', checked.packed_sha256)
        return
    if args.action == 'scan':
        from OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1 import run_powerball
        print(run_powerball(mode,args.constant,args.run_id))
    elif args.action == 'report':
        from OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1 import create_report
        print(create_report(mode,args.constant,args.run_id))
    else:
        from OUTLANDISH_01_Q4h_Powerball_Test_Aggregate_v0_1 import create_aggregate
        from OUTLANDISH_01_Q4d_Statistical_Core_v0_1 import CONSTANTS
        print(create_aggregate(mode,args.aggregate_id,dict(zip(CONSTANTS,args.runs))))


if __name__ == '__main__':
    main()
