#!/usr/bin/env python3
"""SINGLE owner-controlled Q5 Powerball production entry point.

DEFAULT DISABLED. The ONLY toggle for genuine scans is the named constant below.
An owner Git commit changing it to True is required before any Q5 scan.
The Q4h runner separately checks this same constant at the scan boundary,
so bypassing this CLI does not bypass the authorisation switch.

Existing COMPLETE REAL run/report inspection does not require the switch.
No Oz/NULL/forecast/parent project work is authorised by this switch.
"""
from __future__ import annotations

import argparse

ENABLE_Q5_PRODUCTION_SCANS = False  # OWNER Q5 GATE: keep False until separate approval!


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('status', help='show the scan switch, without accessing production inputs')
    scan = sub.add_parser('scan', help='new REAL Powerball scan; requires owner switch True')
    scan.add_argument('--constant', required=True,
                      choices=('pi','phi','e','log2','gamma','lemniscate'))
    scan.add_argument('--run-id', required=True, help='new REAL_... run identifier')
    report = sub.add_parser('report', help='create report from existing COMPLETE REAL run')
    report.add_argument('--constant', required=True,
                        choices=('pi','phi','e','log2','gamma','lemniscate'))
    report.add_argument('--run-id', required=True)
    ag = sub.add_parser('aggregate', help='create REAL-only Holm from six COMPLETE reports')
    ag.add_argument('--aggregate-id', required=True, help='REAL_AGGREGATE_powerball_...')
    ag.add_argument('--runs', required=True, nargs=6,
                    metavar='REAL_ID',help='six run IDs in order: pi phi e log2 gamma lemniscate')
    args = parser.parse_args()
    if args.action == 'status':
        print('Q5 PRODUCTION POWERBALL SCANS:', 'ENABLED' if ENABLE_Q5_PRODUCTION_SCANS else 'DISABLED')
        return
    # Always check switch BEFORE constructing production mode / opening sources.
    if args.action == 'scan' and ENABLE_Q5_PRODUCTION_SCANS is not True:
        raise SystemExit('SAFETY STOP: Q5 production scans DISABLED; owner git authorisation required')

    from OUTLANDISH_01_Q4i_Mode_v0_1 import PowerballMode
    mode = PowerballMode.production_powerball()
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
