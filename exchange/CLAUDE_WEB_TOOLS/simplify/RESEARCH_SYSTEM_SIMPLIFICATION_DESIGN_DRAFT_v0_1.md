# Research system simplification design - DRAFT v0.1

**Status:** DRAFT v0.1 for independent review. Not ratified. It authorises nothing. Until it is reviewed and the project
owner ratifies it, every ratified document stands as it is and the three MHUP-B slices stay uninstalled.
**Written:** 21 November 2026, 11:39 Australia/Adelaide, by the Claude web chat (primary designer and coder), on the project owner's
course correction of 21 November 2026 (EX_259; decision log entry 122) and his go for design work only. Fable (High).
**Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner, after the review.
**Risk tier:** HIGH. It replaces the identity, registry, dispatch, record, workflow and reporting contracts, and the rule
of the one confirmatory forward test.
**Supersedes as drafts:** the OV-1 simplification amendment v0.1 and v0.2 (it carries their accepted content). **Read
with:** the deployment design note DRAFT v0.6, sent with it. **Answers:** EX_259 section 8, A to H; EX_257 F01 and F02.
**Owner-ratified directions and proposed mechanisms are kept apart:** section 1 lists the directions; everything from
section 2 on is a proposed mechanism unless it says "(owner)".

## 0. The whole thing in plain English

1. **Identity is three things: game, family, variant.** Every E-method is a family, even with one member. There are
   no revisions. A changed method is a new variant with its own name and its own code.
2. **Code that computes a forecast is add-only.** Once a variant is installed, its files and the helper files it uses
   are never changed or removed by any later install. The install tool checks this. That is the whole of "old variants
   keep working".
3. **One record per variant per game:** a forecast list and a score list, each one line per draw, in draw order, only
   ever added to. They are the canonical results. Because each list is its own progress marker, "find what is missing
   and do only that" needs nothing else: no plans, tickets, sessions, freeze lines, receipts or witness lines.
4. **One job does everything, and is safe to run at any time:** fill whatever is missing through the last draw on
   file; forecast the next draw; fetch new results with the one reviewed updater; catch up draw by draw, saving a
   league report and an OV-1 line after each; forecast the next draw. After an install it fills the new variants'
   whole history first. Weekly, the same command finds nothing to fill and goes straight on.
5. **Reports are files you can open, print and share:** one cumulative league report per game per draw, TOP and WORST
   together; the next draw's forecasts; the prevailing OV-1; the exploratory OV-1. They are rebuilt from the canonical
   lists whenever the population changes.
6. **Two OV-1 scores.** The prevailing one runs forward from the first draw after the new system starts and is never
   rewritten; a new variant joins it from the first draw whose result was not yet published when the job last read
   the official source. The exploratory one is rebuilt over all history with everything in it, and says so.
7. **A clean start, with nothing destroyed.** The new system writes under a new results folder in a new production
   tree. The old study, its records and its code stay exactly where they are, in the E: clone, in Git and in a cold
   copy. The only use made of the old records is one check: that the moved and simplified code gives the same
   forecasts as before.
8. **Two phases, each checked by itself:** first the folders are rearranged and shown to forecast identically; then
   the contracts are replaced and shown to forecast identically again.
9. **What I have questioned** is in section 12: five places where I propose something simpler than was suggested, and
   six real concerns with the smallest fix for each.

## 1. The owner's directions this design implements (decision log entries 121 and 122; EX_259)

Families and variants only; no revisions; no retirement, supersession or culling; a changed helper never changes an
earlier variant; two separately testable phases; a clean new baseline with the old evidence kept cold and nothing
deleted now; installation is release, then four stages; a saved cumulative league report for every draw with TOP and
WORST; the prevailing and the exploratory OV-1; minimum freeze and administrative software, protecting against bugs,
not fraud; draw numbers, never dates, in any scientific gate; no environment pinned per draw; W-23 unchanged; complete
verified backups and an exact-snapshot restore with no later release put back. The process, orphan and no-kill
safeguards, method-facing N-1 isolation, the one results source and its one reviewed updater, and the three safety
switches with the empty allowlist are not touched.

## 2. What I read and verified first

- EX_259, EX_258 and the permanent record in full; the checkpoint document's current section, as background only.
- **The staged slice-3 tree (the installed code plus the three passed slices), by reading:**
  - A family today is a folder (`src/methods/E_002/`) holding one `contract.py` for all its variants and a table
    `variants.py` whose own first line says "Changing or adding one is a new revision". Cross-family computation sits
    in `_common` (`recurrence_gaps.py`, used by E_2, E_17, E_18, E_19; `occurrence_counts.py`;
    `polynomial_fits.py`). E_1 is laid out differently, with its adapter outside its folder
    (`contract_adapters/e_001.py`). The runner holds a hard-coded `ADAPTERS` table.
  - The registry is 371 files: a chain of numbered entries per (game, method, variant), each with a
    `method_revision`, and one "active entry" per chain, read by the dispatch gate, the walk-forward driver, the
    weekly session, the report writer and Mode H. `release_records.released_variants` keeps only the newest active
    revision of each chain. Score tracks carry `method_revision` (`report.py`, `track_id`).
  - A forecast today is reached through a run request, a run folder, a forecast record, a freeze receipt and a
    terminal record; around them sit batch plans (two schemas), segments, attempts, tickets and resume tokens; the
    weekly tier adds sessions, a target-wide freeze line, witness lines and five effective classes decided by clock
    deadlines; then score lines, league sources, publications and the search log. Thirty-odd record schemas in all.
  - The walk-forward driver runs every method in-process: no child process, timer or termination is involved.
  - The league table, the exploratory OV-1 view and the exact OV-1 kernel exist in slices 2 and 3, passed.
- **Not done:** no project code changed; nothing ran on the owner's PC; no real draw was read. The inventory in
  section 10 is from reading and searching, not from a trial migration, and says where it is less certain.

## 3. Families and variants: the source tree (EX_259 A; phase 1)

**3.1 The layout, the same for every family.**

    src/methods/
        E_002/                          one folder per family
            __init__.py
            core_v1.py                  optional: computation shared by this family's variants
            RECUR_MEAN_ALL_V1/          one folder per variant, named exactly by its variant identifier
                __init__.py
                method.py               compute(task, view) and verify(...): this variant's entry point
                VARIANT.json            (phase 2) its declaration: names, games, minimum history, view
            RECUR_MEDIAN_ALL_V1/
                ...
        E_001/
            ...                         E_1's existing computation modules stay here, as its core
            FULL_HISTORY_RAW_COUNTS_V1/
                method.py               today's contract_adapters/e_001.py, moved
        _shared/                        computation helpers used by more than one family, versioned by file name
            recurrence_gaps_v1.py
            occurrence_counts_v1.py
            polynomial_fits_v1.py
        _common/                        infrastructure: the reader, ranking and ties, records, paths

A variant is found by convention: family folder, variant folder, `method.py`. The hard-coded `ADAPTERS` table and the
`contract_adapters` folder go. A singleton family has exactly one variant folder; nothing else differs.

**3.2 The one rule that keeps old variants unchanged: add-only.** Every file under `src/methods/E_*/` and
`src/methods/_shared/` is immutable once installed. A later release may add files there and may not change or remove
one. The deploy tool already compares the old and new hash lists; it refuses a release that breaks this rule. No
per-variant digest, chain or status is needed.
- **A changed implementation** is a new variant folder. If it needs a changed helper it brings its own copy or a new
  versioned file (`core_v2.py`, `recurrence_gaps_v2.py`). **Example:** `RECUR_MEAN_ALL_V2` wants gaps counted
  differently. Its release adds `E_002/RECUR_MEAN_ALL_V2/method.py` and `_shared/recurrence_gaps_v2.py`.
  `RECUR_MEAN_ALL_V1` still imports `recurrence_gaps_v1`, byte for byte as installed, and both run every draw.
- **Infrastructure in `_common`** (the N-1 reader, ranking, ties, TOP and WORST selection) stays shared and may be
  changed by a reviewed release. What protects earlier variants there is the test of 3.4, rerun at every release.
- **A defect in an installed variant** cannot be patched in place. The fix is a new variant; the defective one keeps
  running and keeps its record, unless the owner explicitly withdraws it by a reviewed release. Nothing withdraws a
  variant automatically, and no such route is built now.

**3.3 Phase 1 is moves only.** Files move and import lines change. No computation line, record schema, registry entry
or contract changes; the revision field is still there at the end of phase 1. Each family's `contract.py` becomes its
`core_v1.py`; each row of `variants.py` becomes a variant folder whose `method.py` fixes that row's parameters and
calls the core. E_1's modules that the proof-of-concept suite and the coordinator plumbing import stay at their
present paths inside `E_001/`.

**3.4 Phase 1's evidence that behaviour is unchanged.**
1. *By inspection:* a generated listing shows every moved file's bytes equal to the original apart from import lines.
2. *The existing suite,* unchanged apart from import paths, passes; the E_1 goldens are not recalibrated.
3. *The full equivalence oracle:* for every existing variant, both games, and every target that has a canonical
   development forecast today, the moved code recomputes the forecast and its content digest must equal the stored
   one. It reads existing records, writes nothing under `results/`, and prints counts and any difference. It is a
   real-data run in the E: clone and needs the owner's own go.
4. The rule of 3.2 has its own tests (a change, a removal and an addition under the two folders).

## 4. Identity, registry and the canonical record (EX_259 A, D; phase 2)

**4.1 Identity.** (game, family, variant), and for a result, the target draw number. `method_revision` leaves every
active contract: the request, the forecast, the score, the track identifier, the league row and OV-1.

**4.2 The registry is the folder tree.** A variant exists, is runnable and is released when its folder is installed
with a valid `VARIANT.json` (family and variant identifiers equal to the folder names; the games it supports; its
minimum history for each; its observation view; a title and a one-line description). No chains, entries, statuses,
development flags, release records or retirement index. The 371 registry and declaration files are replaced by one
small file per variant. Families not yet written are simply absent; a plain list of the R1 and R2 family names can
sit in `doc/` for the reader.

**4.3 The canonical record: two append-only lists per variant per game.**

    results/research/<GAME>/variants/<FAMILY>/<VARIANT>/forecasts.jsonl
    results/research/<GAME>/variants/<FAMILY>/<VARIANT>/scores.jsonl

- **A forecast line:** the target; what the method was given (data through target minus one, with the results file's
  version and SHA-256); the status (`FORECAST`, `INSUFFICIENT_HISTORY` or `FAILED` with its reason); for each barrel
  the scores, the full ranking, TOP and WORST; the content digest; **whether the target's result was already on file
  when it was computed**; the release identifier, the environment digest and the seed; the time, as information.
- **A score line:** the target; the forecast line's digest; the numbers drawn, quoted with the results file's version
  and SHA-256; the TOP and WORST matches for each barrel; the prize divisions.
- **Three invariants,** checked on every read: targets ascend by one with no gap from the variant's first compatible
  target; a score line exists only for a target with a forecast line; at most the last forecast is unscored.
- **What these give, with nothing else:** *idempotence* (the next thing to do for a variant is read from the ends of
  its two lists; a target that has a line is never computed or scored again); *no double score* (a second line for a
  target cannot be appended); *crash resume* (a torn final line is not a record and is redone; the existing chained
  ledger code already detects it); *missing-only fill* (a new variant has empty lists; an old one is up to date).
- **`FAILED` is written only for a failure the method itself raised** in its computation or its own verification, and
  is then final for that target. Any other error (a missing module, memory, a disk fault, an interruption) writes no
  line and stops the job; rerunning resumes. This keeps a broken environment from filling the lists with failures.
- A forecast belongs to its variant and target. There is no target-wide set, so a new variant's line for a draw other
  variants already forecast is simply its own line.

**4.4 The first line of each list fixes two numbers,** written by the job when it first meets the variant:
`first_target` (the first draw it can forecast, from the game's first draw and its minimum history) and, later, one
`FORWARD_FROM` line (section 7.2). Nothing is recorded anywhere else about a variant.

## 5. One job: fill, update, catch up, forecast (EX_259 C; EX_257 F02; phase 2)

**5.1 The command.** `Run_Research.bat` (one launcher; a game or both). It is the weekly routine and the step after an
install; they are the same job. Per game, in this order:

| Stage (EX_259) | What the job does |
|---|---|
| start | The production guard; the process check; the orphan marker blocks as always; one job lock; `SNAPSHOT_DUE` |
| 2 | **Fill.** With the results on file through draw M: for every installed variant, every target up to M that has no line is forecast from the draws before it and scored, in draw order. For a variant just installed that is its whole history; for the rest, usually nothing. Then every variant without a forecast for M+1 gets one, from the draws through M |
| 2, reports | If the fill added anything: every per-draw league report of the game and the exploratory OV-1 are rebuilt (section 6) |
| 3 | **Results.** The one reviewed Lotterywest-GOV updater is run through its own launcher, unchanged. The results on file now reach N |
| 4 | **Catch-up,** for each T from M+1 to N in order: every installed variant that has no forecast for T gets one, from the draws before T (the same function as stage 2); every forecast for T is scored; the league report for T is saved; the prevailing OV-1 line for T is written (section 7). Nothing waits for the end of the backlog |
| 4, end | Every variant without a `FORWARD_FROM` line gets one if the updater ran and succeeded in this job (7.2). Every variant without a forecast for N+1 gets one. The next-draw report is saved |
| end | The end-of-job snapshot (deployment note section 7); the lock removed |

- Stages 2 and 4 call one function, "make sure every installed variant has a forecast and a score for every draw on
  file, in order". There is one forecasting engine and one scoring function.
- **Installation is release** (owner). The deploy tool's `update` installs the code (stage 1); the owner then runs this
  job. No second approval, no activation step, nothing per variant. Several variants and families may arrive in one
  install.
- **No clock rule anywhere.** The next draw is always attempted. A forecast is never refused because of the time.
- **If the updater cannot run** (the site is down; `--no-update` was given), the job says so, treats N as M, and goes
  on. Nothing is lost; the next job catches up.
- **If the results file ever changes other than by growing** (a corrected earlier draw), the job refuses to continue
  for that game and names the draw. What to recompute is then a reviewed decision; it is not automated.
- **Interrupted at any point,** the same command continues: every step reads the ends of the lists.

**5.2 Example: an install with no backlog.** Results on file through 1600. Forty variants are up to date, each
holding a forecast for 1601. V41 is installed.
1. Fill: V41 is forecast and scored for every draw from its first target to 1600. The others: nothing.
   Reports: every league report of the game is rebuilt with V41 in it; the exploratory OV-1 is rebuilt.
   V41 gets its forecast for 1601. The others' forecasts for 1601 are not touched.
2. Results: nothing new. 3. Catch-up: no draws. V41's `FORWARD_FROM` is 1601. The next-draw report lists 41 variants.
A week later the same command: fill, nothing; results bring 1601; catch-up scores 41 forecasts, saves
`league_..._d01601`, writes the prevailing line for 1601 with 41 variants counted; forecasts 1602.

**5.3 Example: a six-draw backlog at an install.** Results on file through 1600; draws 1601 to 1606 have been made
and are not yet on file. V41 is installed.
1. Fill: as above, and V41's forecast for 1601 is computed from the draws through 1600.
2. Results: 1601 to 1606 arrive.
3. Catch-up, six times: for 1601 the forty reuse the forecasts they made before, V41 reuses the one just made, all are
   scored, `league_..._d01601` is saved, the prevailing line for 1601 is written. For 1602 to 1606 every variant is
   forecast from the draws before each, scored, reported, and the line written. Six league reports exist at the end.
4. V41's `FORWARD_FROM` is 1607: its results for 1601 to 1606 are in every league report and in the exploratory OV-1,
   and not in the prevailing OV-1, because those draws had been made before its code was installed. The forty counted
   at all six, as caught-up draws. Everyone is forecast for 1607.

## 6. Saved reports (EX_259 F; phase 2)

    results/research/<GAME>/reports/
        league/league_<GAME>_d<draw, 5 digits>.txt  and  .csv     one pair for every draw that has scores
        next/next_draw_<GAME>_d<draw>.txt  and  .csv              every variant's TOP and WORST for the pending draw
        ov1/ov1_prevailing_<GAME>.txt  and  .csv
        ov1/ov1_exploratory_<GAME>.txt  and  .csv
        README.txt                                                the definitions below, in plain words

- **The league report for draw T is cumulative:** for each variant, over every draw up to and including T that it has a
  score for. One row per variant (family and variant), for TOP and for WORST side by side: draws scored; hits; hits
  expected by chance (seven times seven over the barrel size, per draw); the difference per draw and in per cent; the
  last ten draws; TOP minus WORST per draw; the Powerball barrel for Powerball; the prize divisions; the variant's
  first scored draw; how many of its draws were forecast with the result not yet on file; its `FORWARD_FROM` draw; its
  failed and insufficient-history counts. Order: by TOP hits above chance per draw, ties by identity; the WORST order
  is given as a second column. The header repeats: "A descriptive order. It selects nothing."
- **Reports are derived and replaceable** (owner). They are a pure function of the canonical lists. After any fill
  that adds history, every league report of that game and the exploratory OV-1 are rebuilt with the whole current
  population. In a weekly job only the new draw's files are added. Earlier editions are not kept in production (every
  snapshot holds the editions of its day).
- **Honest labels in every file:** the draw on file the report runs to; the number of variants; when it was made; and,
  where it applies, "rebuilt with the current population: figures for a variant at draws before its installation were
  computed afterwards; this is not a table published at that draw's date".
- Same inputs give the same bytes (the time of generation is kept in one small side file, not in the reports), so a
  rebuild can be checked.
- The fuller statistics of R3 (the measures module) stay available as a report over the same lists, on request.

## 7. OV-1 (EX_259 E; EX_257 F01; replaces the amendment v0.2)

**7.1 Unchanged.** The weights from every counted variant's TOP and WORST tickets, X, V, Z; the exact fair-draw
distribution; the six fixed lambdas, equally weighted; certified lower bounds; the bar of 40; one score per game,
never pooled; a factor of exactly 1 when no variant has a counted pair or V is zero; one line per draw, in order,
appended once; `verify` rebuilds the ledger from the lists and must get the same bytes; blocked until fixed, never
stopped. The kernel (`ov1_numeric.py`) is not edited.

**7.2 Who counts at a draw: `FORWARD_FROM`, a draw number** (the mechanism is proposed; the direction is the owner's).
- A variant counts in the prevailing score at every draw at or above its `FORWARD_FROM` draw. With no retirement, it
  then counts for ever.
- **How the number is fixed, with no date, clock or choice:** it is written once, in the variant's own list, at the
  end of the first job in which (a) the variant's history is complete and (b) the official results updater ran and
  succeeded; it is the last draw then on file plus one. In words: **the first draw whose result had not been
  published when the job last read the official source.**
- **Why this and not "the last draw on file at installation, plus one":** the two agree whenever the results were up
  to date at the install (example 5.2). They differ only when the updater then finds draws already made (example
  5.3), which is exactly when a count from "plus one" would rest on a draw that had happened before the code arrived.
  The smallest counterexample to the simpler rule: a variant written on Wednesday by someone who knows Tuesday's
  result, installed before the results are fetched, would count at Tuesday's draw. The proposed rule costs one line
  kind and removes that case; it needs no pre-condition on the owner's order of work.
- **The start of the prevailing score** is the `FORWARD_FROM` draw of the first job of the new system: the draw after
  implementation (owner). Every variant present then shares it.
- **The cohort as of T** is every installed variant whose `FORWARD_FROM` is at or below T. The line for T is written
  when each of them has its line for T. It records the variants counted, those with no pair and why, how many
  forecasts were made with the result not yet on file, the weights, V, X, Z, the six log-factors and running sums,
  and the release and environment digests of the job.
- **After a restore** the lists and the ledger are the snapshot's; the same job catches up with the snapshot's
  variants; nothing is qualified for that and nothing is put back (owner). A variant installed again later is new:
  its lists start again and its `FORWARD_FROM` is set as for any install.

**7.3 The exploratory OV-1.** The same kernel over every draw that has any scored pair, with every installed variant
counted wherever it has a pair, back-history included. Rebuilt whenever the league reports are. Every file headed
"OV-1 EXPLORATORY RETROSPECTIVE - not the prevailing score; no error bound applies; 40 is a reference line only".

**7.4 What the prevailing report says about the 2.5%** (EX_257 F01). Not "the bound is supported". The fixed text:

> "If this game's draws are fair, and if nothing that decided a draw's forecasts or which variants counted at it was
> influenced by that draw's result, the chance that this score ever reaches 40 is at most 2.5%. The software checks
> that each forecast was computed from earlier draws only, that the variants counted are those fixed by draw number,
> and that every draw is taken once. It cannot check the second 'if'."

Beside it, as software evidence and nothing more: the draws counted; how many counted forecasts were made with the
result not yet on file and how many after; the lines where a counted variant had no pair, with the first such draw.
The vocabulary SUPPORTED and QUALIFIED of v0.2 is dropped: with no retirement and an exact restore, the cohort that
was run can no longer differ from the cohort the records define, so only the plain counts remain. The environment is
not pinned and is not a qualifier (owner); its digest is on each line for anyone investigating a difference.

## 8. The freeze, receipt and ledger machinery: what goes and what stays (EX_259 D)

| Today | What it was for | Proposed | Why |
|---|---|---|---|
| Run request, run folder, run identifier | one folder of files per run | **removed** | the line in the variant's list is the record |
| Forecast record | the ranking, TOP and WORST | **kept as the content of a forecast line,** without the revision and run-mode fields | the scientific result |
| Forecast and diagnostic freeze receipts | proof a record was fixed at a time | **removed** | an appended line is already fixed; timing proof is not a requirement now |
| Terminal record | how a run ended | **folded into the line's status** | one place |
| Batch plans (two schemas), segments, attempts, the search-log row per plan | which pairs a batch may run; resumption | **removed** | the lists say what is missing; resumption reads their ends |
| Tickets, resume tokens | one run at a time for a pair; crash recovery | **removed** | append-only order makes a second line impossible; a torn line is redone |
| Weekly session record, session lock | the roster and inputs of a session | **replaced by one job lock**; the job's digests go on the lines it writes | provenance without a second record |
| Target-wide freeze line | the one set of forecasts for a draw | **removed** | a forecast belongs to its variant; no set (owner) |
| Witness lines, the midnight deadline, the hour rule, the five effective classes | evidence a forecast preceded its draw | **removed;** one fact kept on each line: was the result on file when it was computed | the split is still reported honestly, by draw number |
| Run modes (development, catch-up, final, holdout) | which records count as what | **removed** | one calculation (owner); `FORWARD_FROM` decides the prevailing score |
| Score lines; the corrected-score chain | scores; corrections beside originals | **one score list per variant;** no chain | one scoring function; a defect in it is fixed by a reviewed release |
| League sources file, admissions, publication manifests, the archive of numbered tables | which attempts a total may sum; what was published when | **removed** | one source: the lists; reports are derived and replaceable (owner) |
| OV-1 registration, eligibility lines, cut-off, MISSED, STOP | the formal stream's label | **removed** (agreed in EX_255, EX_257) | section 7 |
| Mode H manifests, markers, opening and developed records, holdout caps | the sealed study and its gates | **not in the new system;** kept cold, untouched | section 9 |
| Release records, install records, the retired-revision index, registry chains | who is released, since when, superseded by what | **removed;** the deploy tool's one deployment log stays | installation is release; the tree is the registry |
| The N-1 prefix view of the reader | a method sees only earlier draws | **kept, unchanged** | the core scientific guarantee |
| Ranking, tie-break, TOP and WORST selection, validation | the readout | **kept, unchanged** | always-review science |
| The results file's version ledger and pins | exactly which results a line used | **kept** | reproducing a surprise |
| Process check, orphan marker, no-kill rule, the updater's lock | process safety | **kept, unchanged** | not weakened (owner) |
| The append-only chained list with torn-line detection (`jsonl_ledger.py`) | safe appends | **kept, and now the only record mechanism** | bugs and crashes |

## 9. The clean baseline: a transition that destroys nothing (EX_259 B)

- **The new system writes only under `results/research/`, in the new production tree `G:\a_p_r_i_r`.** The deploy
  tool's `init` copies `source_data/` (the accepted results files, their version ledgers and verification records) and
  the new code. It copies nothing from the old `results/` or `transitory_data/`. The new history is computed there by
  the first job. So the "reset" is the creation of a new tree; no old file is moved, rewritten or deleted.
- **The old state stays whole in three places:** the E: clone as it is (records, run folders, environment); Git, at a
  tag the owner puts on the last commit before phase 1; and, before anything else, two cold copies: the source ZIP
  the owner downloads from GitHub (source only: no ignored data, no environment, no history), and **one verified ZIP
  of the whole E: clone folder,** ignored run folders, `.git` and `.venv` included, on T:. I propose the second is
  made with the snapshot module's own core, delivered first as a small stand-alone reviewed script: it is the same
  code the backups will use, and it tests a full-size archive early. By hand with another tool is the alternative.
- **Rollback at any point before the owner declares the new system the one in use:** do nothing on E:; it still runs
  the old system at the tagged commit. After that: the cold ZIP.
- **Retained in the new system:** the accepted official results and their provenance, and nothing derived.
- **No legacy reader and no crosswalk in the new code.** The old records are used once, by a checker that is part of
  the transition package and not of `src/`: after the first history fill, every new forecast for a (variant, target)
  the old system also forecast in development must have the same scores, ranking, TOP and WORST. It reads the old
  records in the E: clone, read-only, and prints counts and differences. A difference stops the transition for review.
- **Mode H.** The sealed records are not altered, rerun or rescored: they are simply not in the new tree. The holdout
  caps, the developed declaration, the opening record and the Mode H programs are not part of the new system; every
  draw is an ordinary draw. Nothing recomputed is ever labelled as forecast or published at the original time.
- **Housekeeping left for later, on the owner's word:** whether the old tracked results in the E: clone are moved under
  an `archive/` folder once the new system has run for a while. Not needed for anything here.

## 10. Code affected, by phase (EX_259 A, H). From reading and searching the staged tree; lines are today's sizes

**Phase 1 (layout only; installed in the E: clone by the existing procedure; the old contracts untouched).**

| Files | Change |
|---|---|
| `src/methods/E_002` to `E_019` (each `contract.py`, with `variants.py` or its own modules, such as E_6's `beta_bernoulli.py`) | `contract.py` and the family's own modules become its core (`core_v1.py`); one folder per variant with `method.py` |
| `src/methods/E_001/*`, `contract_adapters/e_001.py` | the adapter becomes `E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py`; E_1's own modules stay where the proof-of-concept suite imports them |
| `_common/recurrence_gaps.py`, `occurrence_counts.py`, `polynomial_fits.py` | moved to `_shared/` with `_v1` names; imports follow |
| `Method_Contract_Runner.py` (its `ADAPTERS` table), `closure.py` (the list of code folders) | the table is built from the folder tree; the folder list follows |
| Tests | import paths; the new tests of 3.4 |

**Phase 2 (contracts; first installed by `init` into the new production tree).** Kept, changed, or left out of the new
release set. Nothing is deleted from Git.

| Area | Files (lines) | Phase 2 |
|---|---|---|
| The N-1 reader and results versions | `game_draws_reader.py` (278), `master_versions.py` (335), `game_profiles.py` (107) | kept; the profile's holdout fields go |
| The readout | `contract_forecast.py` (465), `contract_task.py` (97), `canonical_encoding.py` (27), `seed_policies.py` (130) | kept; the forecast content loses the revision and run-mode fields. **Always-review** |
| Safe appends | `jsonl_ledger.py` (128) | kept |
| The kernel; prize divisions; numerics | `ov1_numeric.py` (307), `divisions.py` (256), `numerics.py` (533), `n1.py`, `n1_generator.py` | kept, not edited |
| The results updater and its checks | `results_master_v0_2.py`, `two_site_results_check_*` | not touched |
| Process safety | `process_check.py` (468) | kept; "session lock" becomes "job lock"; the deployment note's edits |
| The environment inventory | `closure.py` (271) | kept |
| **New** | `research_job.py` (the job of section 5), `variant_lists.py` (section 4.3), `variants.py` (the folder-tree registry), `score.py` (the one scoring function, from today's two), `reports.py` (section 6), `Run_Research.bat` | my estimate: 2,000 to 3,000 lines in all |
| OV-1 | `ov1.py` (713), `ov1_retrospective.py` (192), `Method_OV1.py` | `ov1.py` shrinks to record, status, verify over the lists; the exploratory view reads the lists |
| League | `league_table.py` (310), `measures.py` (682) | the formatter and the measures kept, reading the lists; `league_sources.py` (563), `league_publish.py` (325) left out |
| Registry, dispatch, release | `contract_registry.py` (174), `contract_dispatch.py` (312), `release_records.py` (167), `multigame_method_registry.py`, `install_records.py` (230), `method_retirement.py` (277) | left out, **except what the coordinator plumbing imports** (below). The gate's surviving checks (a valid variant folder; an N-1 view; the job lock) move into the job. **Always-review** |
| Runs, receipts, plans, tickets | `contract_runner.py` (245), `contract_publication.py` (300), `contract_receipts.py` (253), `contract_records.py` (505), `contract_vocab.py` (130), `walk_forward.py` (940), `owner_records.py` (763), `score_identities.py` (150) | left out; the pieces of record validation still needed move into `variant_lists.py` |
| Weekly tier | `weekly_records.py` (778), `weekly_session.py` (525), `weekly_score.py` (266), the two orchestrators, `sequencer_children.py` | left out |
| Old reports and Mode H | `report.py`, `report_writer.py`, `collect.py`, `consolidated_report.py`, `reforecast_compare.py`, `outcome_reader.py`, `mode_h.py`, the `Method_*` command files | left out; the outcome quoting needed by scoring moves into `score.py` |
| Launchers | `Run_Weekly_Session.bat`, `Run_Development_Batch.bat`, `Run_Evaluation.bat`, `Run_Method_Rankings.bat` | left out; `Run_Results_Updater.bat` and the proof-of-concept launchers stay |
| The proof-of-concept suite and the coordinator | `Powerball_Experiment_Coordinator.py`, the `multigame_*` plumbing, the three probes | **not changed.** The three switches stay False and the allowlist empty |

**The least certain row is the coordinator plumbing.** It imports from the dispatch and registry modules (for example
the synthetic probe's "released" check). The code round's first task is the exact list of those imports; each is
either kept as it is or re-pointed in an always-review change. I have not traced them all.

The three passed MHUP-B slices are not installed as built. About half of slice 3 (the league formatter, the
exploratory view) and the slice 2 kernel carry over; the weekly tier, the recorder's formal machinery, the two
orchestrators and the admission code do not.

## 11. Tests the two code rounds must show (EX_259 H)

**Phase 1:** the three kinds of evidence of 3.4, and the add-only rule's tests.

**Phase 2, on invented games and toy variants unless stated:**
- *The same science:* the transition checker of section 9 (real data, the owner's go): equal scores, ranking, TOP and
  WORST for every pair the old system forecast. The reader's N-1 tests and the readout's tests pass unchanged.
- *The lists:* each invariant with a planted defect (a gap, a repeat, a score without a forecast, two unscored
  forecasts, a torn line, a broken chain); a method-raised failure writes `FAILED` and the walk goes on; any other
  error writes nothing and stops; a second run of the job changes no byte of any list.
- *The job:* the two examples of section 5 line for line; an interruption planted at every write, then the command
  again, giving the same final bytes as an uninterrupted run; the updater absent, failing and skipped; a results
  file changed other than by growing refuses; two installs in a row; a variant with too little history.
- *Reports:* a report for every scored draw, none missing in a backlog; TOP and WORST both; the same inputs give the
  same bytes; a rebuild after an install changes every draw's file and no list; the labels of section 6.
- *OV-1:* the kernel's tests untouched; `FORWARD_FROM` in each case (results up to date; a backlog found; the updater
  failed, then succeeded a job later); earlier prevailing lines byte-identical after an install; `verify` after every
  scenario; the exploratory score equals the kernel applied to the whole population; the fixed text of 7.4.
- *A restore:* the tree copied back to an earlier state, then the job: it continues with that state's variants, and a
  variant installed again starts new lists.
- *The add-only rule* in the deploy tool; the registry-by-folder (a folder without a valid `VARIANT.json`, a name
  mismatch, two variants with one name).
- One planted defect for each rule above, as for the slices. The suite before and after each install, as now.

## 12. Critical assessment (the owner asked for one)

**Where I propose something simpler than was suggested.**
1. **One list per variant, not one file per target.** Fewer files by a factor of several hundred, and the list is its
   own progress marker, which is what makes "missing-only" free.
2. **`FORWARD_FROM` in the variant's own list, not an `effective_first_draw` field in release records** (my v0.2). With
   installation as release and no retirement, release records have nothing left to say.
3. **Add-only folders checked by the deploy tool, not a registry of pinned digests** per variant.
4. **No SUPPORTED or QUALIFIED labels** (7.4): the case they existed for cannot arise any more.
5. **No legacy reader; one transition check** (section 9). I would not drop that check: it is the only direct evidence
   that two large rearrangements left the forecasts alone, and the old records are the oracle for it.

**Real concerns, each with the smallest fix I can see.**
1. *Mathematical: when a new variant starts to count.* "The last draw on file plus one, at installation" can count a
   draw already made. Counterexample and fix in 7.2 (`FORWARD_FROM` after the job has read the official source).
2. *Operational: add-only means an installed defect is permanent.* That is the price of "old variants never change".
   Fix: none needed in software; a corrected method is a new variant, and an explicit withdrawal is the owner's to
   order if a variant is ever simply wrong.
3. *Functional: a broken environment must not fill the lists with failures* (lines are final). Fix: only a failure the
   method itself raises is recorded (4.3); and "if it breaks we restore".
4. *Functional: a corrected earlier draw* would silently make stored forecasts stale. Fix: the job refuses and names
   it (5.1). Rare; the decision is then a reviewed one.
5. *Honesty of rebuilt reports.* A league report for an old draw, rebuilt today, is not what was known then. Fix: the
   label of section 6, and the per-variant columns that say how many of its draws were forecast before the result was
   on file. No archive of old editions is needed for that.
6. *Scope.* This is close to a rewrite of the orchestration around a kept scientific core. The risk is not the new
   code, which is small; it is what the old code did implicitly that nobody listed. Fix: the two equivalence checks,
   and the code round starting from an import-by-import inventory, not from this table alone.

**One thing I would not simplify further:** the N-1 reader, the readout (ranking, ties, TOP, WORST) and the kernel are
kept byte for byte wherever possible. Everything removed is administration around them.

## 13. Documents (each reviewed and ratified in the ordinary way)

- **I propose one new, short system specification for the active system,** written with the phase 2 package, in place
  of amending each of: design v0.1r7 (sections 4, 6, Appendices I and J), supplement v0.8, the code plan v0.3, E2R-1's
  rules on revisions, receipts and registry chains, and R3's sections on tracks and classes. Those stay in `doc/` as
  the record of the first study. Amending five documents that describe a system no longer run is the kind of work the
  owner asks to avoid. The reviewer may prefer amendments.
- R2 and R3's scientific content (the methods; the measures) is not changed by this design.
- The deployment design note: DRAFT v0.6, sent with this document.
- The runner's rulebook and the owner's deny lines: the program names change with phase 2.
- **H-1 v8:** written after ratification, as the handover for a new Claude chat (section 15).

## 14. For the owner at ratification, and for the reviewer

**Four choices, each with my recommendation; none blocks the review.**
1. **The job runs the results updater itself** (stage 3), with `--no-update` to leave it out. Recommended: yes; one
   command a week. It changes your decision of 4 November 2026 that the updater stays separately controlled; say if
   you would rather keep running it yourself between two commands.
2. **`FORWARD_FROM` as in 7.2** (recommended), or the simpler "last draw on file plus one, at installation".
3. **The cold copy of the whole E: clone** by a small reviewed script that is the snapshot module's core
   (recommended), or by hand.
4. **One new system specification** (section 13; recommended), or amendments to the five existing documents.

**For the reviewer.**
1. Are the three invariants of 4.3 enough for "no double score, no partial write taken as complete, bounded resume"?
2. Is add-only by path (3.2) an acceptable replacement for the registry's pinned digests and chains?
3. `FORWARD_FROM` (7.2) and the fixed text (7.4): do they meet F01 and E?
4. Is the transition check of section 9 the right single use of the old records, and is anything else of the old
   evidence needed by the new system?
5. Is anything in section 8's "removed" column still needed for correctness rather than for timing proof?
6. Phase 1 before phase 2, each with its own equivalence check: is that the separation you and the owner intended?

## 15. Not tested, and uncertainties

- Nothing here has run. The line estimates and the "kept unchanged" entries of section 10 come from reading.
- The coordinator plumbing's imports (section 10) are not fully traced.
- How long a full-history fill takes for a new variant, and for the whole population at the first job, is unmeasured.
- The readout modules may carry the revision or the run mode deeper than their record fields (for example E_1 takes a
  view digest that depends on the run mode). The transition check is what would show a consequence.
- Whether R3's fuller measures can read the lists with only an input adapter is assumed, not checked.
- This design was written in a chat that has run long. I recommend that the code rounds start in a new Claude chat
  from H-1 v8, after ratification.

End of the design, DRAFT v0.1.
