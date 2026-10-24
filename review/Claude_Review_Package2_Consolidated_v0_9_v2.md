# Claude review and change direction - Multi-Game Package 2 (v0.9 review plus owner decisions), v2

**Reviewer:** Claude (independent reviewer)
**Dates:** review 24 October 2026; owner decisions 24-25 October 2026 (Adelaide)
**Reviewed candidate:** `Predictive_Randomness_MultiGame_Package2_Consolidated_v0_9_CODE_REVIEW_CANDIDATE.zip`, SHA-256 `a14af81be9f99e623d453930ce59c2e396fc8f775f037c0cb7b633ee68ead46a`
**Baseline:** GitHub HEAD `06f6e0f`; committed coordinator v0.6 SHA-256 `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b`
**Supersedes:** `Claude_Review_Package2_Consolidated_v0_9_v1.md` entirely, and any draft paste block from the follow-up discussion.
**Status:** review and direction only. Nothing in this document authorises running anything, changing a safety switch, any network request, holdout access, Mode H, FINAL or process termination.

**Labels used:**
- `[OWNER-DECIDED]` - decided by the project owner in discussion.
- `[REVIEWER-DECIDED]` - routine decision made by Claude under the owner's standing direction.
- `[RATIFY]` - changes a ratified document; ChatGPT drafts the amendment, the owner ratifies.
- `[PENDING]` - not yet decided; do not implement.
- `[SUPERSEDED]` - replaced by a later decision; do not implement.

No winning, Powerball or supplementary numbers appear in this document.

---

## 1. Summary

1. **v0.9 code: no BLOCKERS.** The verification in section 2 stands. Corrections C1 and C3-C8 stand, adjusted in section 3. C2 is replaced by Part A.
2. **Timing (Part A):** human-speed throughout. One configurable poll interval, default 1 s. No fast polling anywhere.
3. **Data source (Part B):** the public Lotterywest JSON results API, for both games. The Lott is not used for any committed data.
4. **Data layout (Part C):** one file per game, in drawn order. One common reader builds a read-only in-memory table and hands out sorted or drawn-order views, according to each method's entitlement.
5. **Scraper (Part D):** one tool with explicit modes. A once-off development build for both games, up to but not including the holdouts. Later modes for holdout fetch and production updates are disabled until their phase. A saved-page fallback is included.
6. **Holdouts (Part E):** a calendar-aligned boundary, the same week for both games: Powerball >= 1578, Oz Lotto >= 1695. The old Powerball data files are deleted and the base is rebuilt without holdout rows.
7. **Process (Part F):** development, then holdout testing (Mode H), then production.

---

## 2. v0.9 verification (independent; unchanged from v1)

| Check | Result |
|---|---|
| Manifest | 43/43 files match; nothing unlisted or missing |
| Overlay footprint | Only `src/Powerball_Experiment_Coordinator.py` replaces an existing file; everything else is new |
| Coordinator diff | Rebuilt from committed v0.6; identical to `evidence/COORDINATOR_V06_TO_V09_EXACT.diff` |
| Coordinator AST | Only `Worker` (fields), `coordinator_main`, `drain` changed; no v0.6 safety function changed |
| Switches | `ENABLE_PROCESS_TERMINATION`, `ENABLE_SCIENTIFIC_COORDINATION`, `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE` all False, no CLI override |
| Synthetic gate | SAFETY STOP, exit 3, no group directory, no process |
| Tests (scratch copy of HEAD + overlay, Linux) | 91/91 multi-game, 13/13 legacy E_1 PASS |
| 1577 regression | Reproduces view `d47fbbd6...4339`, result `7f113087...164e` from training draws 1144-1576 only |
| New modules | No network client, no kill, no source_data/holdout access, no Lott host |
| Classification | Synthetic mode in all four artefacts; scientific allowlist empty |

---

## 3. v0.9 code findings - disposition

| ID | Finding (v1) | Disposition |
|---|---|---|
| C1 | Ancestry release file not published atomically; the worker fails on a partial read | **Keep.** Temp file in the run dir, fsync, then create-only publish (`os.link` + unlink, or `os.rename`, which fails if the target exists). The worker treats absent or shorter-than-expected as "not yet" and fails only on a complete file that differs. Build the release from the status file's own `process_create_time_epoch`. |
| C2 | 25 ms polling with forced tree scans | **[SUPERSEDED] by Part A.** |
| C3 | Gate document command and procedure | **Keep, updated.** Use `Run_Coordinator.bat --synthetic-contract-test --game POWERBALL --target 1577 --timeout-seconds 25 --poll-seconds 1.0`. No local drive path. One `findstr /N /C:"..."` per literal. Exact enable procedure: a one-line change of `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE` in an uncommitted working copy; record that file's SHA-256; a single run; restore to False; show the restored SHA equals the reviewed one. State the intervals and the reasons for them. |
| C4 | Tests for C1/C2 | **Keep,** plus the Part A tests. |
| C5 | Snapshot publisher re-reads after audit; truncated warning count | **Keep;** applies to the new snapshot writer (Part D). Hash what was audited (one in-memory copy), and use the full warning count. |
| C6 | Cross-publisher date disagreement is an error | **Keep wherever a cross-check remains.** Date disagreement is a warning; dates never block. |
| C7 | Sealed Oz profile keeps the unsealed version | **Replaced** by the fixed Oz boundary (Part E): new profile version with `holdout_first=1695`, `holdout_last=1704`; retire `with_sealed_holdout` and `proposed_oz_holdout_metadata`. |
| C8 | Provenance gaps (robots digest per origin, PolicyDecision required, crawl-delay, lottodraw) | **Retarget to the API source (Parts B/D):** add host `www.lotterywest.wa.gov.au` to the policy allowlist; the request is allowed only with `request_allowed=True` for that exact origin; policy returns `crawl_delay`/`request_rate`; robots digest recorded per origin. lottodraw deferred (section 12). |
| O1 | `exists()` vs `lexists` at coordinator 1065 | **Do** [REVIEWER-DECIDED] |
| O2 | Marker on any exception after a clean exit | **Defer** to after the first Windows run [REVIEWER-DECIDED] |
| O3 | `MappingProxyType` for `PROFILES` and the method `_REGISTRY` | **Do** [REVIEWER-DECIDED] |
| O4 | Dead code in `multigame_u_view_v1.py` 62-67 | **Do** (remove) [REVIEWER-DECIDED]; that module is superseded by Part C anyway |
| O5 | Receipt binds SHA-256 of the result-registry and console-protocol modules | **Do** [REVIEWER-DECIDED] |

---

## 4. Part A - Timing and polling [OWNER-DECIDED]

Principle: human-speed. Nothing waits on a fast fixed cycle. Waits block on events where possible, and periodic checks run once per configured interval.

| # | Where | v0.9 behaviour | Decision |
|---|---|---|---|
| 1 | v0.6 coordinator main loop (`coordinator_main`) | `time.sleep(0.04)` + non-blocking drain | One shared helper: block on `messages.get(timeout=poll_seconds)`, process that item, drain the rest non-blocking, then periodic checks (exit via `proc.poll()`, timeout, tree scan). Wakes immediately on output. **No per-worker exit-waiter threads.** |
| 2 | `capture_owned_tree` throttle | fixed 0.5 s | Throttle = `poll_seconds`, supplied as a parameter or a Worker field set at launch (no mutable module global). Exactly one forced scan immediately after each Popen. Scan logic otherwise unchanged. |
| 3 | End-of-run pipe-EOF wait (v0.6 `finally`) | 0.04 s loop, 3.0 s cap | Same helper until all readers are at EOF and the queue is empty; cap `PIPE_EOF_WAIT_SECONDS = 5.0`. Stuck reader -> orphan suspected + global marker, exactly as now. |
| 4 | Reader threads (`read_lines`) | blocking reads; default-buffered log | Unchanged, except the per-worker log is **line-buffered** (`buffering=1`), so it is complete on disk up to the last line read, including in stuck-pipe and coordinator-crash cases. No fsync. |
| 5 | Synthetic lifecycle loop | 0.025 s; `force=True` every pass | Uses the row 1 helper and the row 2 throttle. Refuse `--timeout-seconds` < `RELEASE_WAIT_SECONDS + 2 x poll_seconds` or > 60. |
| 6 | Synthetic post-exit pipe wait | 0.025 s, 3.0 s cap | As row 3. |
| 7 | Worker `await_release` | 0.025 s, 15 s | Poll every `RELEASE_POLL_SECONDS = 0.5`; keep the 15 s deadline and every per-check test (orphan marker, symlink, size, exact bytes); include C1. The file stays the signalling channel (it leaves an evidence record). |
| 8 | Old Powerball scraper | 0.4 s between draw pages, none between year pages | Old scraper retired (Part B). The new tool pauses before **every** request to a host: default 2.0 s, minimum 1.0 s; effective pause = the largest of the configured value, robots `Crawl-delay`, and the interval implied by `Request-rate`. |
| 9 | `POC_Coordinator_Probe.py` sleeps / cpu-load loop | simulated work | No change. |

**Constants (no bare timing numbers):**
- Coordinator: `POLL_SECONDS_DEFAULT = 1.0`, `POLL_SECONDS_MIN = 0.5`, `POLL_SECONDS_MAX = 5.0`, `PIPE_EOF_WAIT_SECONDS = 5.0`.
- `_common/multigame_ancestry_release_v1.py`: `RELEASE_POLL_SECONDS = 0.5`, `RELEASE_WAIT_SECONDS = 15.0`.
- The worker cannot import coordinator code, so an offline test asserts `RELEASE_POLL_SECONDS == POLL_SECONDS_MIN` and the timeout floor rule.

**CLI:** `--poll-seconds` (float, default 1.0, refused outside 0.5..5.0) for both `--poc` and `--synthetic-contract-test`. It is the only timing value settable from the CLI.

**Status-read rule:** before release, a status read that fails or returns None means "not yet" (retry until the deadline); never fatal, never a marker. Only a present but mismatching status is fatal.

**Diff constraint:** the coordinator diff vs v0.6 may change ONLY:
- `coordinator_main` (loop and `finally` wait);
- its nested `drain` if needed;
- `capture_owned_tree` (throttle source only);
- `read_lines` (buffering only);
- `arguments()` (new option);
- plus the new helper and the constants.

These must be AST-identical to v0.6: `terminate_owned_tree`, `register_root`, `accept_ancestry_candidate`, `departed_members_check`, `check_exited_worker_for_orphan`, `status_orphan_evidence`, `record_unresolved_orphan`, `require_no_unresolved_orphan`, `status_and_result`, `save_new`, `read_status`. Update any static test that pins 0.04 / 0.5 / 3.0 and list which ones. Provide the exact owner-run Windows commands to re-run the P1/P2 non-destructive suites with `--poll-seconds 1.0` (not run by ChatGPT).

**Tests:** the helper wakes on output and on the interval (simulated clock/queue, no processes); poll bounds and the timeout floor are refused; status None before release is not fatal; partial/empty release then complete -> proceeds; complete wrong release -> fails; release uses the status ctime.

---

## 5. Part B - Data sources [OWNER-DECIDED unless marked]

### 5.1 Lotterywest public JSON results API (the source for both games)

- **Endpoint:** `https://www.lotterywest.wa.gov.au/api/games/draws/search?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD&game_id=<code>&page=<n>&draw_num=<n or empty>`. This is the request the Lotterywest results page makes in the browser.
- **Lotterywest game codes:** POWERBALL `5132`, OZLOTTO `5130`. In our code, call this value **`lotterywest_game_code`**. Never call it `game_id`: that name means `POWERBALL`/`OZLOTTO` in the project. It is used only to build the request, and is recorded in provenance.
- **Verified 25 Oct 2026, structure only, one request, development range 2018:**
  - plain JSON, top-level `data`;
  - pagination fields `total_records`, `page`, `total_pages`, `page_start`, `page_end`, `records_this_page`;
  - 37 records, draws 1144-1180, dated 2018-04-19 to 2018-12-27;
  - no authentication, cookies, special headers, error or rate-limit message.
- **Record fields:** `draw_num`, `draw_date`, `game`, `winning_numbers`, `winning_numbers_display`, `supplementary_numbers`, `supplementary_numbers_display`, plus prize data (`division_matrix`, `divisions`), which is ignored.
- **To establish in implementation (value-free, by code):**
  - the key of the record array inside `data`;
  - the page numbering base;
  - the date format of `draw_date`;
  - **which field carries drawn order.** Proven against the old Powerball drawn-order data (Part D, DEV_BUILD); one of the pair is expected to be drawn order and the other sorted for display;
  - that Powerball's Powerball is in `supplementary_numbers`;
  - that current-era Oz Lotto has 3 supplementaries. Pre-1474 draws have 2, and are refused.
- **Permission:** `https://www.lotterywest.wa.gov.au/robots.txt` is `User-agent: *` / `Allow: /` (verified 24 Oct 2026). The legal page only asserts copyright. Note: this host differs from `www.oz.lotterywest.com`, which the old scraper used.
- **Politeness:**
  - robots.txt fetched once per host per run and evaluated with `multigame_source_policy_v1`; unavailable/empty/no rules/invalid/disallowed -> STOP; its SHA-256 recorded;
  - pause before every request as in Part A row 8;
  - request windows of at most one calendar year, following `total_pages`;
  - User-Agent: a plain project string, e.g. `analysing_perceived_randomness_in_reality/<version> (+https://github.com/hydra3333/analysing_perceived_randomness_in_reality)`, never `Mozilla/5.0` and nothing disguised;
  - no browser automation and no special headers.
- **Load:** the development build is about 9 requests for Powerball and 5 for Oz Lotto. A production update is 1 request per game.

### 5.2 Lotterywest results search page (fallback only)

- Page: `https://www.lotterywest.wa.gov.au/results/powerball?filterByGame=<code>&fromDate=...&toDate=...`. The owner saves it by hand as .mhtml.
- **It returns at most 100 draws per search** (observed), so saved ranges must be at most one year.
- Verified value-free against the committed data:
  - 86/86 (draws 1463-1548) and 37/37 (1144-1180) agree on date, set, Powerball and drawn order;
  - no sequence was already ascending, so the page shows drawn order;
  - the owner selects "Drawn" (the Drawn/Numerical toggle changes the order).
- An Oz Lotto 2018 save showed 36 Tuesday draws (1262-1297), each with 7 main numbers and 2 supplementaries (old era).

### 5.3 Other sources

- **The Lott / The Lottery Corporation:** not used for any committed data.
  - Its Terms of Use (effective 9 Nov 2023) allow content to be viewed and downloaded only with a browser for personal, non-commercial use, and prohibit reproduction, redistribution, or copying to another server for publication.
  - Its API is undocumented and bot-protected.
  - A private, hand-saved local verifier was discussed and **not adopted** [PENDING]. Asking The Lottery Corporation for written permission or a data file remains an optional route.
- **powerball.net and the old per-draw scraping:** not needed. The old Powerball scraper `scrape_australian_powerball_history_from_2018_04_19_v0_3.py` is retired and kept unchanged as the historical record of how the 20261021 snapshot was made [REVIEWER-DECIDED].
- **[SUPERSEDED]:** per-draw page scraping for Oz Lotto, and the incremental changes to the old Powerball scraper.
- **lottodraw.com.au:** optional future verifier [PENDING / deferred].

---

## 6. Part C - Data layout: one file per game, one common reader [OWNER-DECIDED] [RATIFY]

### 6.1 Files

- One snapshot file per game, in **drawn order**:
  - `australian_powerball_drawn_YYYYMMDD.csv`: `Draw_Number,Date,Drawn_1,...,Drawn_7,Powerball`;
  - `australian_ozlotto_drawn_YYYYMMDD.csv`: `Draw_Number,Date,Drawn_1,...,Drawn_7,Supp_1,Supp_2,Supp_3` (supplementaries in drawn order).
  - File names are proposals; ChatGPT may refine them, but they must be fixed patterns enforced in code.
- Canonical format: the exact header, canonical decimals, ISO dates, one row per draw, consecutive from the era's first draw.
- **Create-only and immutable.** Each update writes a new dated file; if that date already exists -> STOP. Existing files are never modified.
- A **metadata-only provenance JSON** beside each snapshot (no ball values):
  - mode;
  - source (API, or saved pages);
  - `lotterywest_game_code`;
  - request windows and pages;
  - SHA-256 of each raw response or saved page;
  - robots SHA-256 per host;
  - User-Agent;
  - effective pauses;
  - base snapshot SHA-256 (for updates);
  - new file SHA-256;
  - draw range;
  - counts;
  - date-warning count;
  - UTC start/finish.
- Raw API responses and saved pages stay local in a **git-ignored folder** (`.gitignore` rule by folder and extension). Only their hashes are committed.
- The **sorted / drawn-order two-file layout and Oz's separate winning-only / raw files are replaced** by this one-file layout.

### 6.2 Common reader (one reviewed module, e.g. `_common/game_draws_reader_v1.py`)

- **Validate on load:**
  - header;
  - consecutive draws from the era start (Oz: refuse anything before 1474);
  - ranges and distinct numbers;
  - supplementaries distinct from mains;
  - Powerball range;
  - ISO dates;
  - derived weekly dates checked for every row, reported as **warnings only** (dates never block);
  - no draw at or above the game's `holdout_first` in a development base.
- **Build one read-only in-memory table per game with numpy** (no pandas). All arrays `flags.writeable = False`.

  | Column | Type |
  |---|---|
  | `draw_number` | `int32[N]` |
  | `draw_date` | `datetime64[D][N]` (date only; draw time unresolved) |
  | `drawn` | `int8[N,7]` |
  | `sorted` | `int8[N,7]` (derived once) |
  | Powerball | `int8[N]` |
  | Oz supplementaries | `int8[N,3]` |
- **One access call,** e.g. `view(game, method_id, variant_id, target, kind="SORTED"|"DRAWN")`:
  - returns read-only rows from the era start to **target - 1** (a slice, so look-ahead is impossible);
  - `kind="DRAWN"` is refused unless the method registry entitles that (game, method, variant) to drawn order;
  - SORTED is the default;
  - supplementaries are never part of any scientific view; only the structural audit sees them;
  - a plain-Python-list accessor is provided for simple methods, numpy arrays for others.
- **Digests:** a view digest is computed from exactly the rows handed over, in the same canonical serialisation as now. numpy is only the in-memory form, never what is hashed. The E_1 SORTED view for target 1577 must still give `d47fbbd6...4339`, and E_1's result `7f113087...164e`.
- **Entitlement registry:** add the permitted view kinds per (game, method, variant). E_1 is SORTED only. E_23-E_32 drawn-order entitlement stays FORMULA_OPEN until those methods are approved.
- **E_1 migrates to the common reader.** The 1577 regression must pass byte-for-byte on the rebuilt base.
- **Dependency:** numpy goes in `requirements.txt` and in `install_upgrade_dependencies_into_venv.bat`, the single authoritative dependency list.

---

## 7. Part D - The results tool (one tool, explicit modes)

One tool (e.g. `src/multigame_results_tool_v1.py`, run via `Run_Scraper.bat <GAME> <MODE>`), with the same parser and validation for API responses and saved pages.

**Common rules for every mode:**
- value-free console and provenance (counts, draw numbers, dates, pass/fail, field names; never ball values);
- create-only outputs;
- the politeness rules from section 5.1;
- no live run by ChatGPT. Live runs are by the owner, after Claude reviews the code.

| Mode | Phase | Gate | What it does |
|---|---|---|---|
| `DEV_BUILD` | 1 (now) | owner-run after review | Builds the development base. Windows from the era start minus one day to **`DEV_TO_DATE = 2026-08-07`** (a hard cap in code; a later date is refused). Any record at or above `holdout_first` -> **STOP** with no output and no display. Requires exactly first draw .. `holdout_first - 1`, consecutive. Writes the snapshot plus provenance. |
| `OFFLINE_SAVED_PAGES` | any | none (no network) | The same validations from owner-saved Lotterywest results-search .mhtml pages (one year or less each). Fallback for any mode. Records `input_mode=OFFLINE_SAVED_PAGES`. |
| `HOLDOUT_FETCH` | 2 (Mode H) | source constant False; enabled only with a Mode H opening record | Fetches quarantined draws into a separate quarantine area; never displayed. Not part of this delta beyond the disabled stub. |
| `UPDATE` | 3 (production) | source constant False until production is approved | The owner chooses a date range. The tool **refuses** a range that does not overlap the base by at least one draw. Every overlapping draw must match the base exactly, else STOP, reporting draw number and field only. Only missing draws are added; the result must be consecutive; a new dated base is written; existing files are never changed. |

**DEV_BUILD, Powerball:** the rebuilt base must match the old data for 1144-1577 on date, set, Powerball and drawn order, **434/434**, else STOP. The old files are deleted from the working tree (Part E), so the tool reads the old copy **from git history** in memory (e.g. `git show 06f6e0f:source_data/australian_powerball_history_20261021.csv` and the draw-order file; the commit used is recorded in provenance), compares draws 1144-1577 only, and outputs counts. This comparison also proves which API field is drawn order [REVIEWER-DECIDED].

**DEV_BUILD, Oz Lotto:** draws 1474-1694. Structural audit as in 6.2. Derived dates are warnings only.

**Tests (offline, synthetic fixtures only; no real pages or responses that contain quarantined draws):**
- API JSON parsing, including pagination;
- .mhtml parsing;
- DEV_TO_DATE cap refused;
- holdout-range record -> STOP;
- pre-1474 Oz refused;
- incomplete or non-consecutive -> STOP;
- Powerball git-history comparison (fixture repo);
- UPDATE: no overlap -> refuse; overlap mismatch -> STOP; append only; same-date output exists -> STOP;
- robots deny -> STOP;
- minimum pause and Crawl-delay honoured (mock clock);
- User-Agent string;
- provenance JSON contains no ball values.

**Retire or replace:** the Package 2 modules built for the old source plan:
- `multigame_source_plan_v1` -> API date windows;
- `multigame_offline_source_adapters_v1` -> JSON and .mhtml adapters;
- `multigame_offline_response_archive_v1` -> local raw-response archive;
- `multigame_u_view_v1` and `multigame_structural_audit_v1` -> the common reader and its audit;
- `multigame_snapshot_publish_v1` -> the snapshot writer (with C5).

Keep `multigame_source_policy_v1` (with C8) and `multigame_bounded_crosscheck_v1` only if still used (with C6).

---

## 8. Part E - Holdout boundary, quarantine and the old data [OWNER-DECIDED] [RATIFY]

**Calendar-aligned boundary (same week for both games):**

| Game | Last development draw | First quarantined draw | FINAL_HOLDOUT_10 | Later quarantined draws |
|---|---|---|---|---|
| POWERBALL | 1577 (Thu 6 Aug 2026) | 1578 (Thu 13 Aug 2026) | 1578-1587 (ratified, unchanged) | 1588 onward |
| OZLOTTO | 1694 (Tue 4 Aug 2026) | 1695 (Tue 11 Aug 2026) | 1695-1704 (new) | 1705 onward |

- Development fetches stop at 2026-08-07 for both games. Everything from 2026-08-08 onward is quarantined until Mode H.
- **The Oz rule changes** from "ten highest draw numbers in the first structurally accepted snapshot" to the fixed boundary above. Create a new Oz profile version with `holdout_first=1695`, `holdout_last=1704`. Retire `with_sealed_holdout` and `proposed_oz_holdout_metadata`. Oz development targets are then 1475-1694 (`historical_development_target_allowed`).
- **Old Powerball data:** delete `source_data/australian_powerball_history_20261021.csv` and `source_data/australian_powerball_draw_order_20261021.csv` from the working tree **first**, then rebuild the base with DEV_BUILD. Git history keeps them; they are used only for the DEV_BUILD comparison and, at Mode H, a value-free cross-check of 1578-1587. Update every code and document reference to them: the E_1 real-source path, the 1577 regression test, the ratification register, Proposal/Architecture text that names them, and their recorded hashes. **[SUPERSEDED]:** the separate `source_data_sealed/` folder idea.
- **Exposure record** [RECOMMENDED; owner to confirm]: add `doc/HOLDOUT_EXPOSURE_RECORD_v0_1.md` with one entry: "Powerball holdout draws 1585-1587 (and 1588) were shown in the reviewer chat on 25 Oct 2026; no method code, design or selection used them." No values.
- **Chat rule:** never paste results, API responses or saved pages for quarantined ranges into either chat. URLs are fine.

---

## 9. Part F - The three phases

### Phase 1 - Development (pre-holdout; now)

1. ChatGPT delivers the v0.10 delta (section 10) and the document amendments marked [RATIFY].
2. Claude reviews; the owner ratifies the amendments; the owner installs.
3. The install deletes the old Powerball files (Part E).
4. The owner runs `DEV_BUILD POWERBALL`, then `DEV_BUILD OZLOTTO`, and shares the value-free console output and provenance. Claude checks the counts, the 434/434 comparison and the 1577 regression.
5. Development resumes on the development bases only, with each step separately gated as before:
   - 1577 scoring;
   - walk-forward windows ending at 1577 (Powerball) and 1694 (Oz);
   - further methods;
   - the Windows synthetic lifecycle run (Part A / C3), once authorised.

### Phase 2 - Holdout testing (Mode H; when the owner decides)

Ratified basis: Proposal v0.4 section 5.4 Mode H; R3 v0.3 sections 1.2 and 6.2.

1. Per game, freeze a study manifest: method/variant versions, scoring rules, hypotheses, planned reports; its hash recorded.
2. The owner creates a create-only opening record referencing the manifest hash, plus an environment snapshot (R3-T50).
3. `HOLDOUT_FETCH` is enabled for that run only. The code fetches the quarantined draws into the quarantine area. Output is counts only; the values go only to the scorer. Powerball 1578-1587 is cross-checked against the git-history copy, value-free.
4. A runner steps N = `holdout_first` .. `holdout_last` in order. For each N:
   - forecast from the development base plus the holdout draws before N;
   - freeze and receipt the forecast;
   - **only then** release outcome N to the scorer;
   - append the score to an append-only ledger.
5. Produce an immutable report and an audit record. The holdout is no longer pristine for any later method change.
6. **Later quarantined draws** (Powerball 1588+, Oz 1705+): how to handle them (a second untouched set stepped the same way, or merged) is agreed at that time [PENDING].
7. The runner and the holdout mode are a later package with their own review, **not part of v0.10.**

### Phase 3 - Production (after testing)

1. The first `UPDATE` per game fills in the holdout and later draws (they are missing from the base) after the overlap check. It must agree with the quarantine copy.
2. Weekly:
   - the owner chooses an overlapping date range;
   - `UPDATE` writes a new dated base;
   - the FINAL forecast batch, using all known draws (R3 1.3), is frozen and pushed to GitHub **before** the next draw, and scored afterwards in separate append-only records (Mode P).
3. The saved-page fallback (`OFFLINE_SAVED_PAGES`) applies if the API changes or blocks access.
4. FINAL operation remains a separate owner decision.

---

## 10. Requested deliverable: Package 2 v0.10

- **One delta against v0.9,** containing:
  - Part A;
  - C1, C3-C8 as amended in section 3;
  - O1, O3, O4, O5;
  - Part C (reader, layout, E_1 migration);
  - Part D (tool; HOLDOUT_FETCH and UPDATE as disabled stubs with tests of their refusals);
  - the Part E profile change;
  - removal or retargeting of the superseded modules.
- **Evidence:**
  - the exact coordinator diff vs `2e23d550`, with the AST statement from Part A;
  - a single SHA-256 manifest;
  - the full offline test transcript (multi-game, legacy, 1577 regression on a synthetic stand-in where the real base is not yet rebuilt; state clearly which);
  - owner-run Windows commands (P1/P2 re-run; synthetic gate pre-check).
- **Document amendments (separate files, marked for ratification):**
  - Proposal v0.4 section 0A: Oz holdout rule, data layout, source;
  - R2 Erratum Record / ERR-R2-05: Oz holdout rule, views via the common reader, entitlement;
  - R3 v0.3 section 0A.3: Oz boundary and Oz FINAL_HOLDOUT_10;
  - Architecture v0.6 section 0A: one-file layout, common reader and numpy table, timing constants, tool modes, Lotterywest API;
  - P3 multi-game task spec: Package 3 becomes DEV_BUILD; no seal step;
  - ratification register; removal of the old snapshot hashes as active sources.
- **Labelling:** mark everything DECIDED / RECOMMENDED / OPEN honestly. Do not claim any Windows or live result.

---

## 11. Not authorised by this document

- Any run by ChatGPT, any live network request by ChatGPT, or any Windows process run.
- Changing any safety switch; the Windows synthetic lifecycle run; process termination.
- `HOLDOUT_FETCH`, `UPDATE`, Mode H, FINAL.
- Any automated access to The Lott or `data.api.thelott.com`; browser automation; disguised requests.
- Pasting quarantined results into either chat.
- Running `DEV_BUILD`, until Claude has reviewed the v0.10 code and the owner chooses to run it.

---

## 12. Open items

1. [PENDING] Handling of later quarantined draws (Powerball 1588+, Oz 1705+) at Mode H.
2. [PENDING] The Lott as a private, hand-saved local verifier (not adopted). Optional permission request to The Lottery Corporation.
3. [RECOMMENDED] The holdout exposure record (section 8).
4. [OPEN] Nominal draw time and timezone (Lotterywest shows 8:00 pm without a timezone; The Lott says about 8:30 pm AEST). Use closing time for deadlines meanwhile.
5. [DEFERRED] lottodraw.com.au as a second-publisher verifier.

*End of document.*
