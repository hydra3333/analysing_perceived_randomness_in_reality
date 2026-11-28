# The reporting part: code plan for phase 1 (v0.1)

Date: 28 November 2026. From the Claude web chat, on the owner's "go" (decision log entry 424), for the reviewer's
independent reading before any code.
Under: `doc/Predictive_Randomness_Reporting_Design_And_Specification_Amendment_A1_v0_5.md` (RAT-74; "the design").
**Status: PLAN. No code is written. It authorises no install or run.** Where this plan and the design differ, the
design governs and the plan is corrected.

## 0. In short

- **Five slices, each one commit for the reviewer to read.** Only the first touches the engine. It is a pure move:
  every report comes out with the same bytes as before. The rankings, the settings, the inventory and the workbook
  then arrive as changes to the reporting part alone.
- **One rebuild a tree, once.** The owner pulls and runs in DEV only after all five slices are read and passed.
- **The MR1 benchmark is done** (section 4): on the real division profiles of PROD's 80 Powerball tracks, a grid of
  one ten-thousandth of a bit gives a bracket that agrees to two decimals for all 80, in about 10 seconds for the
  whole history of a game. One small tightening of the bracket was needed; it is set out for the reviewer.
- **Two things the design left to this plan are proposed:** a small permanent proof tool (section 8) and the simplest
  staleness check allowed by A10 (section 6).

## 1. The slices

| Slice | What | Engine fingerprint | Proof |
|---|---|---|---|
| S1 | **The move.** All printing leaves the engine, unchanged in what it prints (the league table included, for now). The engine's fingerprint leaves `src/reporting/` out. The job ends by starting the reporting part. The reason the second OV-1 series stopped is stored. The engine stops deleting the reports folder. Install, copy and their checks learn the reporting part. | changes (the only time) | every report file, the league included, has the same bytes for the same inputs; the scientific content of every list is equal (section 8) |
| S2 | **The laws and the measures,** as a library with its tests: exact tails, signed Z, the MR1 bracket, the MR17.EQ tail; the registry of measures and sorts; the track table through a draw. Nothing printed changes yet. | same | hand-worked cases; brute-force enumeration on a small invented game |
| S3 | **The ranking reports** in text and CSV replace the league: introductions, legends, yardsticks, core columns; `REPORT_SETTINGS.ini`; LAST, DRAW n, ALL; the inventory, staleness, failures; `Run_Reports.bat`; the timings printed. | same | tests of every rule of A8 to A10 |
| S4 | **The workbook** (Rankings, Legends, Fair reference), and the file Excel holds open. | same | sheets and values read back by plain ZIP and XML |
| S5 | **The manual's section 2** rewritten for the new reports (the Oz Lotto chance figure corrected with it); the tree's `README.md`; the reports' own `README.txt`. | same | the file-form check |

After S5: the owner's proof and installs (section 9), the MEASURE timings, his ALL. Then phase 2, promptly.

## 2. The files

`src/reporting/` (new; not in the engine's fingerprint; its own fingerprint in `research/code_identity.py`):

| File | What it holds | Slice |
|---|---|---|
| `__init__.py` | nothing but its header | S1 |
| `report_command.py` | what `Run_Reports.bat` starts: the same checks of the tree, its settings and its Python as `research_command.py` makes, the lock, the arguments, the exit code | S1 (LAST only), S3 |
| `report_job.py` | one run for one game: check the inputs, decide the draws, make, remove what is stale, keep the inventory, name what failed, print the timings | S1, S3 |
| `report_inputs.py` | the read-only loading and checking of section 3 | S1 |
| `printouts.py` | the engine's present `reports.py`, moved: the next-draw reports, the two OV-1 print-outs, the writer that writes a file only when its bytes differ, `made_times.csv`; the league table until S3 removes it | S1 |
| `fair_laws.py` | the exact laws and tails of section 4 | S2 |
| `measures.py` | the registry: one entry a measure and one a sort (identity, short title, games, unit, what it computes, its keys, its legend text, its worked example) | S2 |
| `track_table.py` | every track's figures through a draw, built in one pass over the draws, read relative to that draw | S2 |
| `ranking_reports.py` | the text reading view, the CSV, the introduction, the legend, the yardsticks | S3 |
| `report_settings.py` | `REPORT_SETTINGS.ini`: read, checked, defaults | S3 |
| `inventory.py` | the inventory file and the staleness check of section 6 | S3 |
| `workbook.py` | the workbook | S4 |

Root files added (`deploy/tree_parts.py` `ROOT_FILES`): `Run_Reports.bat` (S1), `REPORT_SETTINGS.example.ini` (S3).

## 3. S1 in detail: the engine's one change

**Engine files changed, and nothing else in `src/research/`:**

| File | Change |
|---|---|
| `reports.py` | removed (moved to `src/reporting/printouts.py`, its imports alone changed) |
| `research_job.py` | `make_series_and_reports` keeps the making and writing of both OV-1 series and hands the rest to the reporting part, which it starts in the same process under the lock the job holds; `remove_reports_no_longer_made` moves with the reports; `settle_infrastructure` no longer removes the reports folder; a fault in the reporting part is caught, said loudly, counted in the job's "not clean" ending, and leaves the forecasts and scores as they are; the count "report files" in the ending line comes from the reporting part |
| `ov1_ledger.py` | the header line of each series file gains `made_from` (a digest of what the series was made from: the last draw on file, and each method's identity, fingerprint, first counted draw and retirement draw); the second series' header also gains `blocked`: the reason it stopped early, or an explicit null. `prevailing_status_line` (three lines, used in the job's ending) moves here |
| `code_identity.py` | `REPORTING_FOLDER = 'reporting'` left out of `infrastructure_files`; `reporting_files` and `reporting_fingerprint`, made as the updater's are |

`research_command.py`, `game_state.py`, `scoring.py`, the forecasting code, the readout, `ov1_numeric.py` and every
method are not touched. `GameRecords.cutoff` stays as the dead field it is; nothing new reads it.

**The reporting part's reading (`report_inputs.py`), all through existing functions that only read:**

1. `results_on_file`; `find_variants`; `method_flags.status_of` (never `settle_...`).
2. `code_identity.stored_fingerprint` equals `infrastructure_fingerprint` of the tree, or the game is refused.
3. For each method, `game_state.load_variant_state`: a reason to make its results again is a refusal of the game
   (the engine would delete them; the reporting part never does).
4. Each method's newest forecast was made from the results now on file (`view_digest_for`, one digest a method);
   no line lies beyond the results on file; a retired method holds nothing at or after its retirement draw.
5. Each score line's drawn numbers equal the result on file for its draw (a comparison; nothing is scored again).
6. Both series files exist, and their `made_from` equals the digest worked from what was just read; a series with
   no lines is legitimate, a missing file or a header without `blocked` is a refusal.

A refusal says which check failed and "run Run_Research.bat first", makes nothing for that game, and marks that
game's existing reports NOT CURRENT in `made_times.csv`. Inside a job these checks pass by construction.

**Deploy (DEV only; in no fingerprint a result depends on):** `tree_parts.infrastructure_paths` adds the reporting
files; `dev_tools.infrastructure_fingerprints` adds `reporting_fingerprint`, so the INFRA flag vouches for it;
`install_tools` and `tree_tools` compare it where they compare the updater's; the plan's line is widened to "(only
the updater, the reporting part or the root files differ)". `compare_with_frozen.py` has its import of the moved
file changed in S1 and its league comparison dropped in S3, said in its output; it goes at the tidy.

## 4. S2 in detail: laws, tails and the MR1 benchmark

- **Tails** are inclusive, kept as P_up and P_lo and their logarithms; sigma from the small tail directly
  (`scipy.special.ndtri` of the tail, never of one minus it); signed Z = Z_plus - Z_minus (A5.1).
- **MR7.MAIN:** the n-th power of the one-draw hypergeometric law by repeated convolution (an array of 7n + 1
  numbers). **MR7.PB and every MR4 event:** binomial tails summed from the far end. **MR17.SUM:** the same
  convolution with the Powerball factor. **MR17.EQ:** A5.4's sum, the least M found by whole-number arithmetic on
  323 M'^2 against 6272 (b_obs - b)^2, so that no rounding decides a boundary.
- **Every law depends only on the game and n.** A run first gathers every (n, observed) it needs, for all its
  draws and tracks, then walks n upward once, answering as it goes. No law is stored for later.

**MR1, benchmarked** (Python 3.15, NumPy 2.5.5, the cloud workspace; the division profiles and n of PROD's 80
Powerball tracks through draw 1593, taken from the league table the owner attached; suggestive use only):

| Grid | Time, both roundings, n to 449 | Tracks whose two bounds agree to 2 decimals | Widest bracket of Z |
|---|---|---|---|
| 0.001 bit | 0.5 s | 65 of 80 | 0.045 |
| 0.0001 bit | 10.3 s | 80 of 80 | below 0.0001 |

- **Proposed: 0.0001 bit.** About 10 seconds a game covers every n of the game's history, so the same cost serves
  LAST and ALL. The array is as long as the greatest observed total needs; all chance beyond it is carried as one
  lump, which lies wholly in every upper tail asked for, so nothing is cut off.
- **One tightening of A5.3's bracket, for the reviewer to confirm.** With weights rounded down (L) and up (U), a
  track's own outcome has L below its own upper bound u_obs whenever it won a prize, so A5.3's lower bound
  P(L >= u_obs) leaves out the chance of the very outcome observed. For a track with one or two prizes that chance
  is large (a quarter, for one Division 9 win in 29 draws) and the bracket would be useless. The plan adds the exact
  multinomial chance of the observed division counts to that lower bound, and likewise to the lower bound of P_lo.
  Both stay valid bounds (the observed outcome is in both true tails and was not already counted), and A5.3's
  display and ordering rules are unchanged. The benchmark above is with this tightening.
- **Tests of it:** on an invented game with three divisions and n to 6, every count vector is enumerated with exact
  fractions; the true tails must lie inside the bracket for every possible observed outcome, and the bracket must
  close to the true value as the grid is refined.

## 5. S3 in detail: the ranking reports

- **The track table** is built once for a run: one pass over the draws adds each track's counts; at each draw the
  run needs, the figures are taken as they stand. Expected targets, "missing" and the grid tag follow A3; a
  retirement shows only from its own draw on.
- **Text:** the core columns of A8.2 in that order; then the sorted criterion's own columns (observed, luck's
  figure, P_up, P_lo, Z, or its bracket); then one rank column for each sort switched on, headed by the sort's
  identity. Introduction and legend from the registry's texts; the worked example computed from the first ranked
  line of that report.
- **CSV:** one row a track; columns named `<sort or measure identity>.<what>`; every value, tail, logarithm, sigma,
  bound, rank and tag; no prose rows. The tree, game, draw and counts that the text states in words are columns.
- **Yardsticks:** counted from the registry for the game (every distinct test, switched on or off) and from the
  tracks actually ranked.
- **Settings:** `REPORT_SETTINGS.ini`, read as `ENVIRONMENT.ini` is (the standard reader, `=` only, names exact,
  duplicates refused): `[formats]` with `text`, `csv`, `workbook`; `[text_sorts]` with one line a sort; each `on`
  or `off`. A missing file or a missing line means the default. An unknown name or value refuses the run with the
  names it knows.
- **Exit codes** as A2. A run for both games ends 0 only if both are complete; 1 if any output of either is
  missing or not current; 2 only if nothing at all was written because every game asked for was refused.
  `DRAW n` needs one game named (`--game`); with BOTH it is refused, since the two games' draw numbers are
  unrelated.
- **Timings:** each run prints, for each game, the seconds spent reading, on the laws, on the tables, and writing
  each format, and how many files it wrote. That is the MEASURE item's instrument.

## 6. The inventory and the staleness check (the implementation choice A10 leaves open)

One small file a game, `reports/REPORT_INVENTORY.json`, written whole and put in place:

- what the reports were made by and in: the tree, the reporting fingerprint, the engine fingerprint, a digest of
  the settings in force;
- what they were made from: for each method its fingerprint, its retirement draw, and for each of its two list
  files the length in bytes when last read and the SHA-256 of those bytes;
- what is held: the draws with reports; the draw the reports were last brought up to; whether ALL has established
  complete coverage; the draws whose workbook was asked for; outputs pending after a failure.

**The check, at the start of every run:** if the tree, either fingerprint or the settings differ, or the set of
methods, a fingerprint or a retirement differs, or the first bytes of any list file no longer hash to what was
noted (anything but lines added at the end), then **every draw held is treated as stale** and is removed and made
again. Otherwise only new draws are made.

- This regenerates more than A10's definition requires in some cases (a retirement from a late draw, say). A10
  allows that as an implementation choice where it is simplest; it never regenerates less. Whether a finer check
  is worth writing is decided after the MEASURE timings, not before.
- First migration: no inventory and a `league` folder present: that folder is removed and the run makes LAST.
- A reports folder deleted by the owner: no inventory, so LAST.
- Reports copied from PROD: the tree differs, so every draw held is made again under this tree's own settings.

## 7. S4 in detail: the workbook

XlsxWriter, with a fixed creation time and no volatile properties, so that the same inputs give the same cell
contents. Written beside its place and then put there. If Windows refuses because Excel holds the old one: the old
file stays, `made_times.csv` lists it NOT CURRENT with the reason, the run ends 1. If the package is not in the
tree's Python the workbook is skipped with one plain line and the run ends 1 while `workbook = on`.

## 8. A small permanent proof tool (proposed)

The design's proof (A12) needs a program: "the scientific content of every list is equal". Proposed:
`deploy/compare_science_with_backup.py` (DEV only; in no fingerprint): given a tree and a backup ZIP of it, it
compares, for both games, every forecast's content and digest, every score's content, both OV-1 series' lines, and
each method's identity, first target, establishment draw and retirement; it sets aside only the envelope of each
line and says how many it set aside; it prints SAME or the first differences. It changes nothing.

- It is what the reviewer's tidy agreement asked of every later engine change ("a rebuild gives the same as
  before"), so it outlives `compare_with_frozen.py`, which the tidy retires.
- The design said "no new deploy utility" of installing, copying and restoring. This is a read-only check, not
  such a utility; if the reviewer reads it otherwise, the alternative is the same comparison as a test the owner
  runs, which is clumsier with a real tree.

## 9. After the five slices: the owner's steps (each on his separate go)

1. In DEV: `Backup.bat`; pull; `Make_Installable.bat INFRA`; `Run_Research.bat --no-update` (about 49 minutes:
   everything is made again once; the reports migrate to LAST).
2. The proof: the tool of section 8 against that backup; and, for S1 alone if he wishes, the report files compared
   with the backup's. Any difference is a STOP (A12).
3. Route A or B to QA and PROD.
4. The MEASURE timings in DEV (A14), Claude's recommendation, then his ALL in each tree.

The local runner could rehearse step 1 and 2 in the scratch folder beforehand, on a copy of DEV's results by
reading; proposed only if the reviewer or the owner wants that extra assurance, since it costs two 49-minute runs.

## 10. Tests

New files, all on invented draws, none letting the real updater run: `test_research_reporting_laws.py` (S2),
`test_research_reporting_measures.py` (S2), `test_research_reporting_reports.py` (S3),
`test_research_reporting_job.py` (S3: inputs refused, LAST, DRAW, ALL, inventory, staleness, failures, migration,
copies), `test_research_reporting_workbook.py` (S4). Each of A15's cases is one named test with a planted fault.
The present tests that read reports through the engine are pointed at the reporting part in S1 without change of
what they assert; the eight tests of the comparison tools are adjusted as section 3 says.

## 11. Costs and what is not known

- **Size:** roughly 2,000 lines of code and as many of tests, over five commits.
- **Run time added to a routine job:** about 10 seconds a game for MR1's law (Powerball measured; Oz Lotto has
  fewer draws and divisions), plus reading and writing; to be measured, not promised.
- **Not known until measured:** the time of ALL; whether the conservative staleness check is acceptable in PROD
  once ALL has been run there.
- **Not known until tried:** whether XlsxWriter's files are identical byte for byte across runs; the tests ask for
  identical cell contents and treat container bytes as outside the science, as the design says.

## 12. What is asked

- **The reviewer:** its reading; in particular the slicing (section 1), the engine's exact change (section 3),
  the tightening of the MR1 bracket (section 4), the staleness check (section 6) and the proof tool (section 8).
- **The owner:** nothing to decide yet, unless the reviewer's reading raises a choice. His go is needed before
  S1 is written.

END.
