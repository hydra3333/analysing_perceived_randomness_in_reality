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
