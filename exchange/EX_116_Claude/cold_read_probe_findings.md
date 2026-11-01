# Snapshot probes (1 Nov 2026, two cold-read helpers; docs and code only; no data folders)

## Probe A: results updater / scraper (agent a4c180f95add79859)
Key findings to act on (snapshot docs and/or the Mode H + update + prospective design):
A1 CRITICAL for 9 Nov plan: game_draws_reader and outcome_reader accept ONLY a single version-1 INIT ledger line;
   any update (even NO_CHANGE) adds a ledger line -> every method run and report refuses. Version-2+ consumption,
   pinning (NO_CHANGE rows bump version with same SHA) and old-version retrieval are undocumented/unbuilt.
A2 HOLDOUT_OPENED_<GAME>.json (HOLDOUT_OPENED_V1) is defined only in results_master_v0_1.py code: no doc for schema,
   writer, study-manifest SHA, commit; it is permanent and also unlocks all later weekly updates.
A3 Updater can only add holdout + later draws together; Mode H store (combined vs sequential release) is OPEN (R3);
   roadmap says "update adds draws after the holdout" - order needs a precise design.
A4 Run_Results_Updater.bat with NO arguments runs `update` (refused today; would run once HOLDOUT_OPENED exists).
A5 two_site_results_check_v0_7.py default --sites both AUTOMATES www.thelott.com (contradicts "no automation of The
   Lott"). Used only for INIT. Needs a recorded rule/fix.
A6 Production is single-source (Lotterywest only; owner decided no manual Lott check in production) vs R2-C03 /
   proposal v0.6 "independent evidence"/"candidate version"/"promotion" - contradiction to record/resolve.
A7 No owner procedure for accepting/committing a new master version, stale lock, crash between replace and ledger
   append, orphan grabs.
A8 Default window (current month + 5 back) stops overlapping the master around Jan 2027 -> refused until widened.
A9 Data tools never run under Python 3.15 (venv now 3.15.2).
A10 Small: proposal v0.6 line 152 links oz.lotterywest.com; checker comments "pending ratification"; rulebook rule 1
   heading pairs The Lott with oz.lotterywest.com (a Lotterywest domain).
A11 R3 7.6 "independent outcome ledger" vs master ledger undefined.

## Probe B: performance / workers (agent a8af116eb1181881c)
B1 Register v0.22 line 1234 still says WF-1B carries WORKERS-1 (stale; WB-0 moved it to WF-1C) -> v0.23.
B2 "byte for byte" (register) vs design v0.1 5.4 identity definition (same outcome/reason/canonical digest).
B3 R-006 keeps "one CPU core (about 4%)" claim that EX_099 C01 marked unprofiled.
B4 Roadmap 10d omits 60-worker cap, 4 GiB floor, separate owner approvals for real-data re-runs and Windows tests
   (EX_105 C03), WB-3/WB-4 undecided.
B5 "six-worker limit stands" misdescribes the driver (it is sequential, no limit).
B6 WF-1C order vs Mode H unclear in roadmap/R-007 wording.
B7 Performance proposal assumes six workers and no default-concurrency change (pre WORKERS-1).
B8 Thread policy conflicts (H1 "one BLAS thread per worker" vs proposal "no blanket rule" vs Architecture "one
   initially"); walk-forward runs do not record thread settings (EX_105 C02).
B9 Architecture v0.8 10.1 "No default 12/24-worker runs", ~2 GB per worker -> amend in v0.9.
B10 Timing claims disagree (105 min design, "minutes", "hours"); no measured Windows durations recorded
   (now: Powerball batch ~80 min; Oz batch ~35 min; Oz report >1 h before PERF-1).
B11 "Very end" for the performance study undefined relative to the prospective mode.
B12 No scorer speed-up recorded anywhere (PERF-1 now; record in v0.23).
