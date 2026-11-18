# MHUP-B slice 3 - working notes (Claude; cloud workspace; nothing installed)

Slice 3 = L4 (league table), L7 (consolidated report, two labelled OV-1 views, retired index), L8 (two sequencers,
launchers), built ON TOP of slice 2's tree (digest 000dc4ae...7a581241d). Owner's go: 18 November 2026, 14:33
(decision log entry 88). Governing: code plan v0.3 (L4, L7, L8, sections 7 to 9, 12A), supplement v0.8 (3, 4, 5, 8) as
changed by `exchange/DECISIONS/OWNER_CLARIFICATION_2026_11_18_EQUAL_DRAWS_AND_OV1_USES.md`, EX_235 section 2 (the two
OV-1 views), EX_237 section 5 (four obligations), the working principle (entry 81).

Workspace: /home/claude/work/slice3/{tools, dev}. Quick build: `sh /home/claude/work/slice3/build_dev.sh` (copies
slice 2's built tree, runs `apply_slice3.py`, copies `slice3_new/`). Suite: slice 1's `run_suite.py`.

## Design decisions made while building (each to be named in the covering note)
- One row per score record and readout; a record carries both barrels, so the one-score key is
  (method, revision, variant, target, readout) and the Powerball barrel rides with it.
- Weekly amendments: no tool writes one yet. The table uses the routine line of every key, counts amendment lines in
  its header, and refuses a branching chain (two amendments of one line). A named selection of a correction is not
  provided (it would be a reviewed change on the owner's decision, as for replacing a canonical source).
- Pins in a publication manifest: the forecast ledger by its chained extent (what OV-1's reconcile checks); the
  score and witness ledgers by line count and SHA-256 of those lines; each development source by its score-ledger
  SHA-256; the sealed Mode H ledger by its SHA-256; the roster. A rebuild reads exactly the pinned prefix.
- `history` and `reconstruction` write create-only derived files under `league/derived/`, with no search-log row
  (they compute no new statistic). ASK THE REVIEWER.
- Retrospective OV-1 (use B): the per-game ensemble, cohort = the currently released variants by default, or a
  named list; tickets from the forecasts the canonical sources scored; drawn numbers quoted from the accepted score
  records (no outcome reader); same kernel; a derived part of the report only.

## Progress log (times Australia/Adelaide, read from the clock)
- 14:41 18 Nov: started on the owner's go (14:33). Read plan L4/L7/L8, sections 7-9, 12A, supplement 3-5 and 8, design 6.1/6.6/Appendix F, EX_235 section 2. NEXT: L4 (league_sources.py, league_table.py, league_publish.py, Method_League_Table.py), then tests.
- 14:49 18 Nov: L4 first cut written: league_sources.py (three adapters, pins, manifests reader, attempt_entry, batch_state), league_table.py (pure), league_publish.py (the one writer: publish/repair/admit/history/reconstruction), Method_League_Table.py; apply_slice3.py (released_history; ov1.publication_names connected). A whole publication works on the synthetic weekly project (smoke run). NEXT: tests/test_mhupb_league.py, then L7.
- 14:59 18 Nov: tests/test_mhupb_league.py: 21 tests pass on 3.13 (figures against an oracle, sources, the five publication steps with a fault after every durable step, admission, history, reconstruction, the OV-1 seam, statics). The oracle caught a CSV column slip of mine (forward kind written twice). Admission now checks every score record against the frozen forecast it scores (complete per readout; matches recomputed from the ticket and the record's own drawn numbers): a truncated or altered ledger was otherwise pinned silently. edit_tests_slice3.py: slice 2's static import list for ov1.py gains league_sources. NEXT: real-records test, then L7.
- 15:03 18 Nov: tests/test_mhupb_league_real.py (2 tests): the adapters read the committed real ledgers as the census counted them (Oz Lotto 11,916 and Powerball 22,884 development score lines, 80 tracks each, revisions 1 and 2; 800 sealed Mode H lines each, shown and never summed). The admission's forecast check cannot run on real records in the cloud (the run folders are on the owner's PC only). L4 DONE apart from mutants. NEXT: L7 (consolidated_report.py, ov1_retrospective.py, Method_Weekly_Report.py).
- 15:18 18 Nov: L7 built: ov1_retrospective.py (use B: the ensemble over forecasts already scored; kernel unchanged; tickets from frozen forecasts, drawn numbers quoted from score records, X computed twice), consolidated_report.py (7 parts; WEEKLY_REPORT row; create-only files incl. the retired index), Method_Weekly_Report.py; registry gains CATCH_UP and OV-1's two labelled uses. tests/test_mhupb_weekly_report.py: 11 tests pass on 3.13. The retrospective series equals an oracle written in the test (own count of the fair-draw distribution, floating point) to 9 places and never exceeds it; over the formal stream's draws its X, Z and score ARE the formal FACTOR lines'. N1 for the forward/catch-up tables is wired through WF-1B's own measures_stage (runs when a seed policy is approved). NEXT: L8 (sequencer_children.py, two orchestrators, two .bat launchers, layer static test), then mutants, full suites.
