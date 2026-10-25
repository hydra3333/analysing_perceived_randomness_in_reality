# Claude review of Package 2 v0.10-r1, plus current direction and what is now in place, v2

**Reviewer:** Claude (independent reviewer)
**Date:** 25 October 2026 (Adelaide)
**Reviewed candidate:** Package 2 v0.10-r1 review ZIP, SHA-256 `f1db9629f4735f25de357a991a98748abffe0f53ed58efb03e11991b972cf45b`
**Baseline:** GitHub HEAD `995920d`. The committed coordinator is still v0.6, SHA-256 `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b`.
**Supersedes:** v1 of this document (v2 records the owner's decisions P1-P4 of 25 Oct and the completed master initialisation). Also supersedes Parts B, D and E, and the file names in Part C 6.1, of `Claude_Review_Package2_Consolidated_v0_9_v2.md` (SHA-256 prefix `bd5665e0`). Every other part of that document stands unless this one says otherwise.
**Status:** review and direction only. Nothing here authorises a run by ChatGPT, a network request by ChatGPT, a Windows run, a safety-switch change, holdout access, Mode H, FINAL or process termination. `ENABLE_PROCESS_TERMINATION` stays False.

**Labels:**
- `[OWNER-DECIDED]`: decided by the project owner.
- `[REVIEWER-DECIDED]`: a routine decision by Claude under the owner's standing direction.
- `[PENDING]`: not yet decided; do not implement.
- `[RATIFY]`: changes a ratified document. ChatGPT drafts the amendment; the owner ratifies it.
- `[SUPERSEDED]`: replaced; do not implement.

No winning, Powerball or supplementary numbers appear in this document.

---

## 1. Summary

1. **v0.10-r1 code: no BLOCKERS. Six CORRECTIONS (C1-C6)** in section 2. C1 is a real N-1 leak and must be fixed before any scientific use of the new reader.
2. **Results acquisition is no longer ChatGPT's work.** Two owner-run tools, reviewed and written on the Claude side, now cover it (sections 4 and 5).
   - ChatGPT's Lotterywest API client, saved-page parser and results tool are superseded.
   - **[OWNER-DECIDED]** No API is used.
3. **The source is Lotterywest's own results-search web page** on `www.lotterywest.wa.gov.au` **[OWNER-DECIDED]**.
   - It is read by an honest, unmodified headless browser, and the owner accepts it as official.
   - The Lott is used only as a private, hand-saved verifier. Nothing derived from The Lott is committed.
4. **The development history is built and verified** (section 4.3):
   - Powerball 433/433 draws (1144-1576) and Oz Lotto 220/220 (1474-1693): none missing, none extra, no date failures.
   - Powerball matches the old committed files 433/433, on date, drawn order, sorted set and Powerball.
   - An independent sample from The Lott matches: 52/52 Powerball draws over 12 months, and 31/31 Oz Lotto draws over 7 months.
5. **One master results file per game** replaces the dated snapshot files **[OWNER-DECIDED]**.
   - Each master has an append-only ledger and create-only backups and grabs. All of these are committed.
   - The reader must consume the master, bound by its hash (section 3.2).
6. **The holdout boundary moves to a month boundary** **[OWNER-DECIDED 25 Oct; RATIFY the document changes]**:
   - all draws dated 1 August 2026 or later are quarantined;
   - Powerball from 1577, Oz Lotto from 1694.
7. **Requested next deliverable:** Package 2 v0.11, a delta against v0.10-r1 (section 7).

---

## 2. v0.10-r1 findings

### 2.1 What was verified

- The candidate's SHA-256 is as above. The delta overlay was rebuilt into a scratch copy of the baseline.
- **The legacy E_1 golden values reproduce through the new reader:** view `d47fbbd6...4339` and result `7f113087...164e`.
  - Method: development rows were rebuilt from the git-history copy of the old drawn-order file (`06f6e0f`), filtered on the first field before any other field was parsed.
  - Derived sorted set, Powerball and date matched 434/434 on the v0.10 week-aligned base.
  - Only rows below the target were consumed. No row at or above 1578 was parsed.
- `ENABLE_PROCESS_TERMINATION`, `ENABLE_SCIENTIFIC_COORDINATION` and `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE` are all False, with no CLI override. The scientific result allowlist is still empty.
- Part A constants are present:
  - `POLL_SECONDS_DEFAULT/MIN/MAX` = 1.0/0.5/5.0;
  - `PIPE_EOF_WAIT_SECONDS` = 5.0;
  - `RELEASE_POLL_SECONDS` = 0.5;
  - `RELEASE_WAIT_SECONDS` = 15.0.

### 2.2 Corrections

| ID | Finding | Required change |
|---|---|---|
| C1 | **N-1 leak through numpy views.** `DevelopmentDrawTable.view()` returns slices such as `self.drawn[:count]`. A numpy slice keeps `.base` pointing at the whole table array, so `view.main.base` (and the same on `draw_number`, `draw_date`, `powerball`, `drawn_main`) reaches every development row, including rows at and after the target. Read-only does not prevent reading. | Each view must own copies. Build every array in a `DrawView` with `_readonly(source[:count])`, a fresh byte-backed array whose base is a `bytes` object holding only the prefix. **Test:** for every view array, `arr.base` is `bytes` and `len(arr.base) == count * row_itemsize`, and no attribute chain reaches more than `count` rows. Add a poisoned-table test: the rows after the target hold values the test would detect. |
| C2 | **The method boundary is not enforced.** This answers the owner's N-1 question (request 6). | (a) Methods receive only `DrawView` objects (or the plain-list form), never `DevelopmentDrawTable`, a path or a file handle. Orchestration code holds the table. (b) Full validation of a results file happens once: when the master version is created (by `results_master` init/update, section 5), bound by SHA-256 in the ledger. (c) A per-run loader checks the file's SHA-256 against the ledger version pinned in the run manifest, then **parses only rows below the target** and stops reading. A suffix is never parsed in a scientific run. This restores the earlier rule "the loader never parses row N". (d) Tests: a poisoned-suffix file (garbage after the target) still yields the correct view and is never parsed; the source path is refused if it is a symlink or has `st_nlink > 1`; a static check shows that no method implementation (outside the `_common` reader and orchestration code) imports the loader or names a `source_data` path. A separate process is not needed at this stage [REVIEWER-DECIDED]. |
| C3 | **Dates are exposed but not digested.** `DrawView.draw_date` is handed to callers, but `simple_rows()` and `e1_view_digest()` exclude it. A method could consume dates without the digest recording it. | Dates are opt-in: `view(..., include_dates=False)` by default. When dates are included they are part of the digest, under a new schema name. The legacy E_1 schema and digest stay unchanged, because E_1 does not take dates. |
| C4 | **The "exact" coordinator diff does not match.** `evidence/COORDINATOR_V06_TO_V010_EXACT.diff` does not reproduce the shipped `src/Powerball_Experiment_Coordinator.py` from committed v0.6 (`2e23d550`). | Regenerate the diff mechanically from `2e23d550` to the shipped file. State the shipped file's SHA-256, and re-run the AST statement for the protected functions. |
| C5 | **Keep a pre-build 1577 regression.** v0.10-r1 makes the real golden check a gate after DEV_BUILD only. | Keep an offline regression that does not depend on any build. It derives the 1144-1576 rows at test time from git history (`06f6e0f`, first-field filter, rows < 1577 only), runs E_1 for target 1577, and asserts `d47fbbd6...4339` / `7f113087...164e`. This is a forecast for 1577 from earlier draws only; the 1577 outcome is never read. Under the month-aligned boundary, 1577 is the first quarantined draw, so this test uses the narrow exception in section 6, item P3 [OWNER-DECIDED]. Once the master exists, add the same assertion against the master (which ends at 1576). |
| C6 | **Timing literals remain; one test is missing.** v0.6-era literals remain: `messages.put(..., timeout=0.12)`, `reader.join(timeout=0.05)`, and the same 0.05 s join in `multigame_windows_lifecycle_v1.py`. The offline test asserting `RELEASE_POLL_SECONDS == POLL_SECONDS_MIN` is missing. | Name the literals as constants where the diff constraint already allows changes: `read_lines`, the `coordinator_main` `finally`, and the lifecycle module. Leave the 3.0 s / 3 s waits in the termination path untouched, because those functions must stay AST-identical to v0.6. Add the missing test, and list any literal deliberately kept. |

### 2.3 Optional

- **O1:** the old-file comparison code parses holdout rows with `DictReader` before skipping them. Filter on the first field, as raw text, before any parsing. The two Claude-side tools already do this.
- **O2:** add real (pre-boundary) Lotterywest results-search page excerpts to `tests/fixtures`. A 2018 page is enough. Only the owner may supply them; never use pages that show quarantined draws.
- **O3:** `requirements.txt` is stale (it lists neither numpy nor selenium). The installer `.bat` is the single authoritative dependency list. Either regenerate `requirements.txt` from it or mark it as historical.

---

## 3. Owner decisions on the v0.10-r1 questions

### 3.1 Reader views

- **[OWNER-DECIDED]** There is no per-method view-entitlement registry. The reader offers `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER` and `PAIRED_DIAGNOSTIC` on request.
- The separate scientific result allowlist is kept, and stays empty until methods are approved.
- The R2 no-double-likelihood principle remains binding.

### 3.2 The reader consumes the master

- The reader loads `source_data/<GAME>_results_master.csv`. Its header is the same as v0.10's:
  - Powerball: `Draw_Number,Date,Drawn_1..Drawn_7,Powerball`;
  - Oz Lotto: `Draw_Number,Date,Drawn_1..Drawn_7,Supp_1,Supp_2,Supp_3`.
- The `australian_<game>_drawn_YYYYMMDD.csv` name pattern is [SUPERSEDED].
- Before parsing, the loader checks that the file's SHA-256 equals the `master_sha256` of the ledger version pinned in the run manifest.
  - During development that is version 1, `INIT`.
  - The manifest records the game, master file name, ledger version and SHA-256.
- During development, the master ends exactly at `holdout_first - 1`. The loader refuses a master that does not (C2 rules apply).
- Loading after the holdout is opened belongs to the Mode H package, not v0.11.

### 3.3 Drawn order [OWNER-DECIDED 25 Oct] (answers the order-promotion question)

- **Decision:** the published sequence is treated as the operator's drawn order, for both games. This is the owner's stated assumption: publishers show results in drawn order, and the owner recalls seeing the order on the televised draw. It is not a proof; no website can prove physical order.
- **Supporting record:** `source_data/<GAME>_results_master_init_verification.json`, bound to the master's SHA-256 and written by `results_master init`. It records:
  - the full-era source (Lotterywest results search);
  - Powerball only: full-era agreement with the old Lotterywest per-draw pages, 433/433. This is the same publisher, so it shows consistency, not independent verification;
  - the independent sample from The Lott: Powerball 52/52 and Oz Lotto 31/31, every field PASS, including `main_order` and the Powerball / supplementary order.
- **Reader:** set `order_verification_status = "OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION"` for the master versions covered by that record, citing the record's file name and the master SHA-256. The reader does not decide this itself, and the value and citation travel with every view and its digest.
- `OPERATOR_DRAWN_ORDER` and `PAIRED_DIAGNOSTIC` need no further gate beyond normal method approval.
- Reports and manifests that use order must state it as "published drawn order (assumed operator order)", never "verified".

### 3.4 Draw date and time

- **[OWNER-DECIDED]** Dates only.
- No authoritative draw time or timezone was found:
  - the SA Powerball rules (March 2026) are silent;
  - Lotterywest pages show a time with no timezone;
  - third-party claims are internally inconsistent.
- Keep `Date` (ISO, date only) in the masters, and label time as not recorded.
- An optional timing sidecar can be designed later, with its own source, provenance and view schema. It needs no amendment now.

### 3.5 Holdout exposure record

- **[OWNER-DECIDED in principle]** A short, value-free record, for example `doc/HOLDOUT_EXPOSURE_RECORD_v0_1.md`.
- Shorten v0.10-r1's draft to facts only:
  1. On 25 October 2026 the reviewer chat displayed the published results of Powerball draws 1585-1588.
  2. The old committed Powerball files `*_20261021.csv` contain draws in the quarantined range. They remain in git history; the Claude-side tools read them only through a raw first-field filter (draw < 1577).
  3. Commit `9b78b8f` contained a saved results page that showed recent quarantined draws. It was removed in a later commit and remains in git history.
- No values, no "no effect" claim, and no analysis.

---

## 4. Sources and verification [OWNER-DECIDED unless marked]

### 4.1 Lotterywest results search (the official source)

- **URL:** `https://www.lotterywest.wa.gov.au/results/<powerball|oz-lotto>?fromDate=<Ddd+Mmm+DD+YYYY>&toDate=<...>&filterByGame=<5132|5130>`.
  - The path selects the game. The code is `lotterywest_game_code`, never `game_id`.
- At most 100 draws per search, so windows are at most about one year.
- The page text per draw is: `Draw N`, the date, `Winning numbers:` and 7 numbers, then `Powerball:` and 1 number or `Supplementary numbers:` and 3 numbers, then `View prizes`.
- `robots.txt` allows all.
- **Honest automation only:**
  - a real browser (Selenium 4.51, headless), unmodified, with default settings and no stealth;
  - only the page's own requests;
  - at least 2 s between page loads;
  - a block or challenge page means STOP, never a bypass.
- `oz.lotterywest.com` serves a Cloudflare challenge to automation. It is never contacted.
- **[SUPERSEDED]** The Lotterywest JSON API (v0.9-v2 section 5.1), and the plain-requests User-Agent approach.

### 4.2 The Lott

- Honest automation gets "0 draws found", which is treated as bot protection and not pursued.
- No API (`data.api.thelott.com`), no impersonation, no bypass.
- The owner saves pages by hand, outside the repo; `*.mhtml` is git-ignored.
- Parsing reads only the results-search block. The page's latest-draw panel shows quarantined draws and is never read.
- The Lott is a private verifier only. No values derived from it are committed.

### 4.3 Results (owner-run, value-free outputs; run folders are git-ignored under `private_results_checks/`)

| Run | What | Result |
|---|---|---|
| `run_20261025T020840Z_5a7fbb` | History build from Lotterywest results search (`--build-history`) | Powerball 433/433 (1144-1576), Oz Lotto 220/220 (1474-1693); 0 missing, 0 extra, 0 off the weekly date rule. Powerball vs the old committed files: 433/433 PASS (date, drawn order, sorted set, Powerball) |
| `run_20261025T021022Z_714ecd` | The Lott hand-saved sample vs that build (offline, seed 20261025) | Powerball 52/52 over 12 months; Oz Lotto 31/31 over 7 months; 0 failures |
| January 2026 checks | Both sites, both games | All matched |

---

## 5. What is now in place

| Item | Status |
|---|---|
| `install_upgrade_dependencies_into_venv.bat` | Committed. Adds `selenium`. Default mode installs and upgrades; also `INSTALL`, `UPGRADE`, `VERIFY`. Writes before/after `pip freeze` snapshots and prints changed versions. **[RATIFY]** This departs from Architecture section 5A.2 (no automatic upgrades); a one-line amendment is needed. |
| `src/two_site_results_check_v0_7.py` | Committed (`995920d`). SHA-256 `69cb1dec...9aed`. Self-test 14/14. Modes: `--build-history`, `--offline-dir` (with `--against-run`), `--pick-lott-sample`, `--diagnose-lotterywest`. Hard quarantine (any draw >= the first quarantined draw, or dated >= 2026-08-01, is a STOP before its numbers are read). Value-free reports; create-only, git-ignored run folders. |
| `src/results_master_v0_1.py` | New. Its SHA-256 is printed in every ledger line. Self-test 9/9; fake-browser tests 9/9; init tested on the real old Powerball rows. Details below. |
| `Run_Results_Updater.bat` | New. Same venv checks as `Run_Coordinator.bat`. With no arguments it runs `update`; otherwise it passes arguments through. |
| `.gitattributes` | Adds `source_data/** -text`, so masters, ledgers, grabs and backups are stored byte-for-byte and their hashes hold on any checkout. |
| Masters, ledgers and init verification | **Done 25 Oct.** Created by the owner's offline `init` run and committed. Powerball 433 draws (1144-1576), master SHA-256 `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8` (equal to Claude's independent computation from the old committed rows). Oz Lotto 220 draws (1474-1693), master SHA-256 prefix `4a6cecc27fb6a5b8` (full value in its ledger). Warnings 0; re-read identical to the build. Git shows both stored byte-for-byte (`-text`). The old `*_20261021.csv` files were removed from the working tree with `git rm`. |

### 5.1 `results_master_v0_1.py`

**Files, all in `source_data/` [OWNER-DECIDED]:**
- `<GAME>_results_master.csv`: the latest approved results, keyed by draw number, in drawn order, CRLF, ASCII.
- `<GAME>_results_master_ledger.csv`: append-only, one line per version. Columns: version, UTC, action (`INIT`, `UPDATE`, `NO_CHANGE`), master SHA-256, first/last draw, count, added range, grab and backup file names and SHA-256, tool version and tool SHA-256.
- `backups/<GAME>_master_draws_<a>-<b>_as_at_<UTC stamp>.csv`: an exact create-only copy of the master before each replacement.
- `grabs/<GAME>_grab_draws_<a>-<b>_as_at_<UTC stamp>.csv`: what each update fetched, create-only, kept even when the update fails.
- `<GAME>_results_master_init_verification.json`: value-free evidence for version 1.

**`init` (offline, once):**
1. Refuses if any master, ledger or record already exists.
2. Checks the build run's provenance mode and every CSV SHA-256, and its zero missing/extra/off-date counts.
3. Checks The Lott run's mode, that it was run against that build, zero failures, its report hash, and the per-field tallies.
4. Re-validates every row: consecutive from the era start to exactly the last development draw, ranges, distinct numbers, supplementaries not overlapping the mains, the weekday, and exact weekly dates. Any quarantined row is a STOP.
5. Re-runs the Powerball comparison with the old files, 433/433 required. The old files are read through the raw first-field filter, from the working tree or `git show 06f6e0f:`.
6. Writes create-only, then re-reads through the normal verified path, and requires it to be identical to the build.
7. The expected Powerball master SHA-256 is `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8`. Claude computed it independently from the old committed rows, and the owner's init must reproduce it.

**`update` (production; not run, by owner decision):**
- Lotterywest results search only. Default window: the current month plus the previous 5; `--months-back` from 0 to 60. Windows are split into overlapping searches of about a year or less.
- Before anything is requested:
  - if no well-formed `source_data/HOLDOUT_OPENED_<GAME>.json` exists, any window reaching 2026-08-01 is refused, with no browser started. There is no override;
  - a lock file is taken;
  - the master's SHA-256 must equal the last ledger line, and its rows are re-validated.
- After fetching:
  - every overlapping draw must match the master exactly, else the update fails with the master unchanged and the grab kept;
  - no overlap means refused (gap risk);
  - new draws must be consecutive.
- Then, in order: backup, atomic temp-file replace, ledger append, re-verify.
- Exit codes: 0 OK, 1 verification failure, 2 STOP, 3 refused.

**[RATIFY]** The masters replace "immutable, never overwritten" snapshots. The amendment should state:
- every version is preserved byte-for-byte in `backups/`;
- the ledger and hashes identify each version;
- every scientific run pins the master SHA-256 and ledger version it used.

---

## 6. Holdout boundary [OWNER-DECIDED 25 Oct; RATIFY the document changes]

| Game | Last development draw | First quarantined draw | FINAL_HOLDOUT_10 |
|---|---|---|---|
| POWERBALL | 1576 (Thu 30 Jul 2026) | 1577 (Thu 6 Aug 2026) | 1577-1586 |
| OZLOTTO | 1693 (Tue 28 Jul 2026) | 1694 (Tue 4 Aug 2026) | 1694-1703 |

- **P1 [OWNER-DECIDED]:** the boundary is the first draw dated in August 2026, for both games.
  - Constants: `QUARANTINE_START_DATE = 2026-08-01` and `FIRST_QUARANTINED_DRAW = {POWERBALL: 1577, OZLOTTO: 1694}`.
  - These replace v0.10's 1578/1695 and `DEV_TO_DATE = 2026-08-07`.
- **P2 [OWNER-DECIDED]:** FINAL_HOLDOUT_10 = the first ten quarantined draws per game.
  - For Powerball this changes the ratified 1578-1587 to 1577-1586 **[RATIFY]**.
  - For Oz Lotto it is the fixed rule replacing "ten highest in the first accepted snapshot" **[RATIFY]**.
- **P3 [OWNER-DECIDED]:** the narrow E_1 regression exception (C5). Target 1577 may be forecast from draws 1144-1576 for the regression test only. The 1577 outcome is never read, no score is computed, and the output never counts as a holdout result.
- **Development targets:**
  - Powerball 1145-1576;
  - Oz Lotto 1475-1693.
  - Walk-forward windows end at 1576 and 1693.
- **Physical separation:** done; the old `*_20261021.csv` files are removed from the working tree. Git history keeps them. Update every code and document reference: the E_1 real-source path, the regression test, the ratification register and the recorded hashes.

---

## 7. Requested deliverable: Package 2 v0.11 (a delta against v0.10-r1)

1. C1-C6 and O1-O3.
2. Reader changes from section 3.2: it consumes the master, bound to the ledger, and parses the prefix only. Section 3.3 order status read from the verification record. Section 3.4 dates opt-in and digested.
3. Profiles: implement section 6 as named constants (owner-decided; the document amendments still need ratification). Section 3.3 drawn-order status.
4. **Retire (move to a `retired/` folder or remove from the overlay, with a list):**
   - `lotterywest_api_client_v1.py`;
   - `lotterywest_results_v1.py`;
   - `lotterywest_saved_pages_v1.py`;
   - `multigame_results_build_v1.py`;
   - `multigame_results_tool_v1.py`;
   - `Run_Scraper.bat`;
   - any test that exercises only these.
   - Keep the old Powerball scraper unchanged as the historical record [REVIEWER-DECIDED].
   - Do **not** copy or rewrite the Claude-side tools. Reference them by path and SHA-256.
5. **Document amendments, as separate files marked [RATIFY]:**
   - Architecture section 5A.2: the installer;
   - masters and ledger versus immutability;
   - the source: the Lotterywest results-search page through the owner-run tools;
   - timing constants;
   - Proposal section 0A, R2 ERR-R2-05 and R3 section 0A.3 for the boundary and FINAL_HOLDOUT_10;
   - the P3 task spec: no DEV_BUILD by ChatGPT, since the masters exist;
   - the ratification register;
   - the shortened exposure record (section 3.5).
6. **Evidence:**
   - the mechanically regenerated coordinator diff and AST statement;
   - one SHA-256 manifest;
   - the full offline test transcript;
   - owner-run Windows commands, listed but not run.
7. **Labelling:** DECIDED / RECOMMENDED / OPEN, honestly. Make no claim of any Windows, live or real-data run.

---

## 8. Not authorised by this document

- Any run, network request or Windows process by ChatGPT.
- Any safety-switch change, process termination or the Windows synthetic lifecycle run.
- Mode H, FINAL, holdout access, or creating any `HOLDOUT_OPENED_*` record.
- Running `results_master update` (the owner has decided not to run it, even to test).
- Any automated access to The Lott, any API use, browser impersonation or bot-protection bypass.
- Pasting results, pages or responses for quarantined ranges into either chat.

## 9. Open items

1. [PENDING] Handling of later quarantined draws at Mode H, after the first ten.
2. [PENDING] The Mode H runner, and loading the master after the holdout is opened (a later package).
3. [DEFERRED] Optional timing sidecar (section 3.4).

*End of document.*
