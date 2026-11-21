# Predictive Randomness - specification of the active research system - DRAFT v0.1

**Status:** DRAFT v0.1 for independent review. Not ratified. It authorises nothing. Until the project owner ratifies
it, every ratified document stands and nothing is coded, moved, installed, run, migrated or deleted.
**Written:** 21 November 2026, 13:04 Australia/Adelaide, by the Claude web chat (primary designer and coder), on the project owner's
directions of 20 and 21 November 2026 (decision log entries 121, 122 and 124; EX_258, EX_259, EX_261, EX_262) and his
go for design work only. Fable (High).
**Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner, after the review.
**Risk tier:** HIGH. **Companion:** the deployment design DRAFT v0.7 (how the installs, backups and restores are carried
out). **Replaces as drafts:** the research system simplification design v0.1 (EX_260) and the OV-1 amendment drafts.
**Marking:** "(owner)" marks a direction the owner has given. Everything else is a mechanism proposed for ratification.

## 0. The whole system in plain English

1. **Three separate folders, each complete in itself:** DEV (where methods are written; the Git clone on E:), QA (a
   test bed that behaves exactly like production; on D:), and PROD (the real research; on G:). Each has its own data,
   results, Python environment and backup folder. Their places are set in a small settings file, never in code.
2. **A method is a family; a family has one or more variants; a variant never changes once installed.** A changed
   method is a new variant. Nothing is retired automatically; the owner alone can withdraw a variant that is wrong.
3. **A variant becomes installable** when a small marker file in its DEV folder says so and matches its files exactly.
4. **Installing is two steps and nothing more:** install into QA, where the tests run by themselves; then install the
   very same files into PROD. **PROD refuses anything that has not passed in QA, byte for byte. There is no way
   round that.** Shared system code is updated by a separate command, under the same rule.
5. **One command does the research:** it works out what is missing, forecasts and scores it draw by draw from earlier
   draws only, fetches new official results (in PROD), saves a league report after every draw, keeps the two OV-1
   scores, and forecasts the next draw. It is safe to run at any time and after any interruption.
6. **Every result is one line in a list that is only ever added to.** That is what prevents double counting, and it
   is what lets an interrupted job carry on.
7. **Backups are complete copies of a whole tree,** checked when made. A restore puts back exactly one backup and
   nothing else; the research then catches up with what that backup held.

## 1. Authority, and what is binding

**1.1** When ratified, this document and its companion are the one authoritative description of the active system.
**1.2 Still binding, by reference (science and safety; not restated here):**
- The methods: R2 v0.5 sections 1 (invariants), 2 (data contract), 4 (observation policy) and 7 (the 62 families),
  and each family's own ratified design (for example the Wave 2 design v0.1r2).
- The readout: how scores become a ranking, ties, and the TOP and WORST seven: E2R-1 v0.3r3 section 7, less its
  revision, run-mode and receipt fields.
- The measures and the time axis: R3 v0.5 sections 3 (TOP, WORST and rank-position measures), 4 (reference values)
  and 17 (league measures; MRD-12: "The time axis is the draw number"; 17.3.1: games are never pooled).
- OV-1's mathematics: supplement v0.8 sections 6.1 (weights, X, V, Z), 6.3 (per game; bar 40) and 6.5 (the exact
  evidence score and its numerical contract), as implemented by the passed kernel `ov1_numeric.py`.
- The results source and its one reviewed updater (Lotterywest-GOV only, R-017); the process, orphan-marker and
  no-kill rules (Architecture 5C; design 6.1); the three safety switches (False) and the allowlist (empty); W-23.
**1.3 Historical once this is ratified** (the record of the first study; no longer rules for the active system): design
v0.1r7; supplements v0.7 and v0.8 except the three sections named above; the MHUP-B code plan v0.3; E2R-1 sections 5,
6, 8, 9, 12 and 12A (declarations with revisions, run requests, receipts and tracks, modes and tiers, versioning,
retirement and release); R3 sections 6 and 10 (holdout windows; the weekly FINAL protocol) and 17.3.6; the direction
document v0.3r1 section 9; every draft of the MHUP-B deployment note. The sealed Mode H records are not altered,
rerun or rescored: they are simply not part of the new trees (section 17).

## 2. Three roles, three trees (owner; EX_262 F09)

| | DEV | QA | PROD |
|---|---|---|---|
| Purpose | write and try methods; build installs | prove an install before PROD | the research |
| Example root | the Git clone on E: | `D:\TEST_BED` | `G:\a_p_r_i_r` |
| Holds | all source, tests, documents, unfinished variants, its own scratch results | installed software only; its own copy of the accepted results; its own results; its own `.venv` | the same, for real |
| Variants that run | every variant folder with a valid `VARIANT.json`, finished or not | installed variants only | installed variants only |
| Official results | a verified copy from PROD | a verified copy from PROD | the one reviewed updater |
| Backups | Git, and the cold copy of section 17 | its own backup root | its own backup root |

- **Each tree's root holds `ENVIRONMENT.ini`,** which states its role, its own root, its backup root and its
  environment folder. A tree is what its own file says it is: a copy of QA placed somewhere else does not become
  PROD. Every launcher checks the file against the folder it is in. The backup root must lie outside the tree.
- **DEV's file also names where QA and PROD are.** No drive letter or path appears in any program.
- **Nothing flows from QA to PROD, or from PROD to QA or DEV, except** the accepted official results, copied one way
  from PROD, checked to be the same file grown longer. QA's results and scores are never copied anywhere.
- **Git and GitHub are DEV conveniences only** (owner). No install, run, backup or restore needs them or a network.

## 3. Families, variants and their code (owner; EX_259; EX_262 items 3, 8)

**3.1 Identity** is (game, family, variant); a result adds the target draw number. There is no revision.

**3.2 Layout, the same for every family, including a family of one:**

    src/methods/
        E_002/
            core_v1.py                       optional: computation shared by this family's variants (immutable)
            RECUR_MEAN_ALL_V1/
                method.py                    compute(task, view), verify(...)
                VARIANT.json                 the declaration (3.4)
                I_AM_INSTALLABLE.json        DEV only: the readiness marker (section 4)
        _shared/
            recurrence_gaps_v1.py            helpers used by more than one family (immutable, versioned by name)
        _common/                             infrastructure (section 12.4)

**3.3 Add-only.** In QA and PROD, a variant's folder and every helper file under a family folder or `_shared/` is
never changed or removed once installed, by any command. A changed implementation is a new variant folder; a changed
helper is a new file with a new name (`core_v2.py`). Helpers are not scored and are not installed for their own
sake: a helper arrives with the first variant that names it. Prefer code inside the variant's folder.

**3.4 `VARIANT.json`:** the family and variant identifiers (equal to the folder names); a title and one line of
description; the games supported; for each, the minimum number of earlier draws needed; the observation view; and
**`helpers`: the exact list of helper files this variant uses.** A static check requires every import from a family
folder or `_shared/` made by the variant's files or its listed helpers to be on that list. That is the whole of
dependency handling: no resolver.

## 4. Readiness in DEV; the registry in QA and PROD (owner; EX_262 F08)

- **The marker `I_AM_INSTALLABLE.json`** lists every file of the variant's folder and every helper it names, each with
  its SHA-256, and one fingerprint over them all. `Make_Installable.bat <family> <variant>` validates the declaration,
  runs the import check and writes it. A marker made by hand counts only if it validates the same way.
- **It is bound to content.** If any listed file changes afterwards, the marker no longer matches and the variant is
  not ready until the marker is made again. A marker nominates a variant; it proves nothing about correctness.
- **Ready** means: a valid declaration, a matching marker, and the import check passing.
- **In QA and PROD there are no markers.** A variant exists and runs when its folder is installed with a valid
  declaration. As a check against accidents, each tree keeps one list of every installed software file and its hash;
  the job refuses to run if the tree does not match it.
- **In DEV** the research job may run any variant folder with a valid declaration, marked or not, against DEV's own
  scratch results. A list made by an earlier version of an unfinished variant is set aside automatically (5.6).

## 5. The canonical record (EX_259 D; EX_261 F01, F06)

**5.1 Two append-only files per variant per game:**

    results/research/<GAME>/variants/<FAMILY>/<VARIANT>/forecasts.jsonl
    results/research/<GAME>/variants/<FAMILY>/<VARIANT>/scores.jsonl

Every line carries the digest of the line before it. Lines are only ever appended.

**5.2 Lines of the forecast file.**

| Kind | When | Holds |
|---|---|---|
| `HEADER` | first line | game, family, variant, the variant's fingerprint, `first_target` (the first draw with enough earlier draws) |
| `TARGET` | one per draw, from `first_target`, ascending by one | a status and its content (5.3) |
| `FORWARD_FROM` | at most once | a draw number (section 10.2) |
| `WITHDRAWN_FROM` | at most once; nothing follows it | a draw number and the reason (section 11) |

Only `TARGET` lines are counted in the ascending-by-one rule; the other kinds sit between them where they were written.

**5.3 A `TARGET` line is one of exactly two things.**
- **`FORECAST`:** for every barrel of the game, the score of each number, the full ranking, and complete TOP and WORST
  sets. Anything less is not a forecast.
- **`NO_FORECAST`,** with one typed reason. `INSUFFICIENT_HISTORY`: the method returned its declared "not enough
  history" result. `METHOD_FAILED`: the method raised the one declared exception type for a failure of its own
  mathematics (for example a fit that cannot be made), or its output failed the readout's validation or its own
  `verify`. A `NO_FORECAST` line is final for that target and can never be scored.
- **Anything else that goes wrong** (any other exception, a missing module, memory, the disk, an interruption) writes
  no line. The job stops for that game and says why. Rerunning tries again. An environmental fault is never
  recorded as a method failure.

**5.4 Content and envelope** (F06). Each `TARGET` line has two parts.
- *Content,* with its digest: the identity; the target; the digest of the **permitted view** (the draws before the
  target, and nothing else); the variant's fixed configuration and seed; the status and the forecast itself.
  **Nothing in the content, and nothing given to the method, depends on any draw at or after the target, or on the
  results file as a whole.**
- *Envelope,* for audit only: the version and SHA-256 of the whole results file at the time; the digest of the
  installed software; the digest of the environment; whether the target's result was already on file; the time.
The same code, configuration, seed and earlier draws in the same environment give the same content digest whatever
is appended to the results later. Across a changed environment identical bytes are not promised.

**5.5 The score file** has one line for each `FORECAST` whose result is on file: the target, the forecast content's
digest, the numbers drawn (quoted with the results file's version and hash), the TOP and WORST matches for each
barrel, and the prize divisions. Its lines ascend. A `NO_FORECAST` target has no score line.

**5.6 The invariants,** checked whenever the files are read; a failure refuses that game and names the line.
1. The chain is unbroken, and the first line is the header, whose fingerprint is the installed variant's. (In DEV a
   different fingerprint means the variant was edited: both files are moved to a dated `_stale` folder and the lists
   start again. In QA and PROD it is a refusal.)
2. `TARGET` lines run from `first_target` upward by one with no gap and no repeat.
3. Every score line names a `FORECAST` line by target and content digest; no target is scored twice.
4. Every `FORECAST` line has a score line, except that **the final `TARGET` line may be an unscored forecast** (the
   pending next draw). An unscored forecast followed by any later `TARGET` line is a fault.
5. After `WITHDRAWN_FROM` there is no further line.
*Example (F01):* target 100 `FORECAST` and scored; 101 `NO_FORECAST: METHOD_FAILED`; 102 `FORECAST` and scored. All
five invariants hold: 101 is resolved by its own line and needs no score.

**5.7 What to do next is read from the files, never remembered** (crash resume). For a variant and the draws on file
through N: any target from `first_target` to N without a `TARGET` line is computed, in order; any `FORECAST` whose
result is on file and has no score line is scored; target N+1 is forecast if it has no line. **A torn last line** (a
crash while writing) is not a record: it is cut off before the next append, which is the only removal of bytes the
system ever makes. The write order for a draw is: forecast lines, score lines, the prevailing OV-1 line, the report.
Each step is skipped if already done, so a crash between any two is repaired by running the job again.

## 6. Earlier draws only (N-1)

For target T a method receives the permitted view: the draws before T. The one reader builds it and nothing else
reaches the method. Seeds are fixed by identity and target. No cache, feature or statistic computed from draws at or
after T may reach a forecast for T, in a first fill, a catch-up or a later recomputation. The reader's existing tests
stay, and a test changes and appends draws at and after T and requires T's content digest to be unchanged.

## 7. The research job (owner: the four stages; EX_259 C; EX_261 P03, F03)

**7.1 One command, `Run_Research.bat`,** for one game or both, in any tree. It is the routine after an install and the
weekly routine: the same job. For each game:

| Step | What happens |
|---|---|
| Start | The tree's own checks (section 15); one job lock; the "backup due" flag |
| Fill | With results on file through draw M: every missing target up to M, for every variant, is forecast from the draws before it and scored, in draw order (5.7). Then every variant without a line for M+1 is forecast for it. If the fill added anything, all of that game's reports are rebuilt (section 9) |
| Results | **PROD:** the one reviewed Lotterywest-GOV updater is run through its own launcher, unchanged (choice A, section 19). **QA and DEV:** the accepted results are copied from PROD and checked to be the same file grown longer; neither ever contacts the lottery site. `--no-update` leaves the step out. The results on file now reach N |
| Catch-up | For each T from M+1 to N, in order: forecast lines for any variant lacking one; score lines; **the prevailing OV-1 line for T, if the prevailing score has started and T is at or after its start** (section 10); the league report for T. Each draw is finished before the next begins |
| End | If the results step ran and succeeded in this job: every variant without a `FORWARD_FROM` line gets one, N+1; and the prevailing score's start is fixed if it has none (10.3). Every variant without a line for N+1 is forecast. The next-draw report is saved. The end-of-job backup |

- Fill and catch-up are one function. There is one forecasting engine and one scoring function.
- **No clock rule exists.** The next draw is always attempted. The absence of a result on file is never treated as
  proof that the draw has not been made.
- **A results step that fails or is left out** changes nothing: N is M, no `FORWARD_FROM` is written, the job says so
  and finishes. The next job catches up.
- **A results file that has changed other than by growing** refuses that game and names the draw. What to recompute
  is then a reviewed decision.
- A catch-up of no draws is normal. An interrupted job is continued by the same command.
- **In DEV** the job writes only DEV's scratch results, and `--only <family>/<variant>` limits it to named variants.

**7.2 Examples** (results on file through 1600 at the start).
- *An install, no backlog.* V41 is new. Fill: V41 from its first target to 1600; the forty others nothing. Reports
  rebuilt with V41 in them. V41 forecast for 1601; the others' forecasts for 1601 untouched. Results: nothing new.
  End: V41's `FORWARD_FROM` is 1601. The next week: 1601 arrives; 41 forecasts scored; the prevailing line for 1601
  counts 41 variants; `league_..._d01601` saved; 1602 forecast.
- *An install with six draws waiting.* Fill as above. Results: 1601 to 1606 arrive. Catch-up, six times over: forecast
  (the forty reuse their 1601; V41 reuses the one just made), score, prevailing line, league report. Six reports.
  V41's `FORWARD_FROM` is 1607: its results for 1601 to 1606 are in every report and in the exploratory OV-1, not in
  the prevailing one. The forty counted at all six.
- *The very first job of a new tree.* Every variant fills its whole history. Results bring 1601 to 1606: forecast,
  scored and reported, **with no prevailing line, because the prevailing score has not started.** End: every variant's
  `FORWARD_FROM` is 1607 and the prevailing score's start is 1607.
- *The first job with the updater failing.* History filled; 1601 forecast; no `FORWARD_FROM`; the report says
  "prevailing OV-1: not started; waiting for a successful results update". Nothing provisional is published.

## 8. Scoring

One function, for both games, from R3 section 3 and the game profiles: for each barrel, how many of the numbers drawn
are in the TOP set and how many in the WORST set (Powerball: the main barrel of 35 and the Powerball barrel; Oz Lotto:
the main barrel of 47, with the supplementary numbers used for the prize divisions only, never for forecasting); and
the prize division each ticket would have won. A forecast is scored once, when its target's result is on file.

## 9. Saved reports (owner; EX_259 F; EX_261 P04)

    results/research/<GAME>/reports/league/league_<GAME>_d<draw, 5 digits>.txt  and  .csv
    results/research/<GAME>/reports/next/next_draw_<GAME>_d<draw>.txt  and  .csv
    results/research/<GAME>/reports/ov1/ov1_prevailing_<GAME>.txt  and  .csv
    results/research/<GAME>/reports/ov1/ov1_exploratory_<GAME>.txt  and  .csv
    results/research/<GAME>/reports/README.txt

- **A league report exists for every draw that has any score.** The report for draw T is cumulative: each variant over
  every draw up to T it has a score for. One row per variant, TOP and WORST side by side: draws scored; hits; hits
  expected by chance (seven times seven over the barrel size, a draw); the difference a draw and in per cent; the
  last ten draws; TOP minus WORST a draw; the Powerball barrel for Powerball; prize divisions; first scored draw;
  how many of its forecasts were made with the result not yet on file; its `FORWARD_FROM`; its `NO_FORECAST` counts by
  reason; "WITHDRAWN from draw T" where that applies. Ordered by TOP hits above chance a draw, ties by identity, with
  the WORST order beside it. Header: "A descriptive order. It selects nothing."
- **Reports are derived and replaceable** (owner). They are a function of the canonical files alone. When a fill adds
  history, every league report of that game and the exploratory OV-1 are rebuilt with the whole current population;
  otherwise a job adds only the new draw's files. Earlier editions are not kept in the tree; each backup holds the
  editions of its day.
- **Every file says** what draw it runs to, how many variants it holds, when it was made, and, where it applies:
  "rebuilt with the current population: a variant's figures at draws before its installation were computed
  afterwards; this is not a table published at that draw's date".
- The same canonical files give the same report bytes (the time of making is in a side file).
- R3's fuller measures (section 17 of R3) are available as a further report over the same files, on request.

## 10. OV-1 (owner: two uses; EX_257 F01; EX_261 P05, F03)

**10.1 Unchanged:** the mathematics and the kernel named in 1.2; one score per game; the bar of 40; a factor of
exactly 1 when no variant has a counted pair or V is zero.

**10.2 `FORWARD_FROM`: when a variant begins to count in the prevailing score.** It is a draw number, written once in
the variant's own forecast file at the end of the first job in which its history is complete and the results step ran
and succeeded: the last draw then on file, plus one.
- **What it means, and no more:** the first draw **not present in the accepted results on file after a successful
  check of the official source.** It does not prove the draw had not been made, or that its result could not be known
  some other way.
- It differs from "the last draw on file at installation, plus one" only when the check then finds draws already
  made; those are exactly the draws that must not count for a variant installed after them.
- No date, clock or choice enters it. A restore keeps the numbers the backup holds.

**10.3 The start.** The prevailing score of a game starts at the `FORWARD_FROM` draw fixed by the first job of that tree
whose results step succeeded. Its ledger opens with one line stating that draw. Before it there is no prevailing
score, and draws caught up before it are scored and reported as research only.

**10.4 One line per draw from the start,** in order, appended once
(`results/research/<GAME>/ov1/prevailing.jsonl`).
- **The cohort as of T:** every installed variant whose `FORWARD_FROM` is at or below T and which is not withdrawn
  from a draw at or below T.
- The line is written when every cohort member has its `TARGET` line for T and, if that is a forecast, its score.
  Until then the line is **blocked** (an operational wait), never skipped.
- Each cohort member is recorded as *counted* (a complete TOP and WORST pair) or *no pair*, with the reason
  (`INSUFFICIENT_HISTORY`, `METHOD_FAILED`). The weights come from the counted pairs only.
- The line also holds: how many counted forecasts were made with the result not yet on file; the weights; V; X
  (derived from the weights and from the score lines, which must agree); Z; the six log-factors and running sums;
  the envelope digests. Rebuilding the ledger from the canonical files must give the same bytes.
- Blocked until fixed, never stopped; no reset; no second stream.

**10.5 The exploratory score** is the same kernel over every draw that has any scored pair, counting every variant
wherever it has one. It is rebuilt with the league reports. Every file is headed: "OV-1 EXPLORATORY RETROSPECTIVE - not
the prevailing score; no error bound applies; 40 is a reference line only".

**10.6 The claim, as the prevailing report prints it** (F01, F03):

> "If this game's draws are fair, and if nothing that decided a draw's forecasts or which variants counted at it was
> influenced by that draw's result (that includes what code was installed or withdrawn and when, and which backup
> was restored), the chance that this score ever reaches 40 is at most 2.5%. The software checks that each forecast
> was computed from earlier draws only, that the variants counted are those fixed by draw number, and that every
> draw is taken once. It cannot check the second 'if'."

Beside it, as plain counts: draws counted; counted forecasts made before and after the result was on file; lines
with a "no pair" member, and the first such draw. There is no SUPPORTED or QUALIFIED label.

**10.7 After a restore** the files and the ledger are the backup's and the job continues them. Nothing is marked for
the restore. The score may differ from the one that was lost; that is a truthful result.

## 11. Withdrawing a defective variant (owner; EX_261 F02)

- **What it is:** the owner's explicit decision that a variant is wrong and stops. It is never automatic and never a
  judgement of performance. The corrected method is a new variant, installed in the ordinary way.
- **How:** `Withdraw_Variant.bat <family> <variant> --game <game|BOTH> --reason "<text>"`, in the tree concerned. It
  shows the variant and the draw, and the owner types one confirmation. It appends one `WITHDRAWN_FROM` line to the
  variant's forecast file: **the last draw on file plus one,** and the reason. That is the whole mechanism: no
  registry, no status table. The owner tells the reviewer the reason in the ordinary exchange.
- **From that draw:** no forecast is computed; the variant is not in the prevailing cohort; a forecast it already
  holds for that draw is left unscored and shown as "not scored: withdrawn".
- **Nothing is removed or rewritten:** its code stays installed; its lines stay; the prevailing factors already
  written stay; every league report still shows it over the draws it was scored for, marked withdrawn; the
  exploratory score still uses its scored draws.
- **It is data of that tree.** A restore to a backup made before the withdrawal brings the variant back as it then
  was; it runs again in the catch-up, and nothing withdraws it again automatically. A newly created tree (section
  12.5) installs it and runs it until the owner withdraws it there.

## 12. Installing (owner; EX_262 F08, F10; the decision of 21 November 2026 on QA)

**12.1 Two kinds of install, never mixed.**
- **`Install.bat QA|PROD`: new variants only.** It finds every ready variant in DEV (section 4) that the target does
  not hold, shows the exact batch (variants, helper files, and what it left out and why), and adds those folders and
  any helper files that are new. `--only` narrows the batch. It never overwrites: a variant the target already holds
  is left alone even if DEV's copy has changed (changed science is a new variant), and a helper the target holds with
  different bytes is a refusal. Nothing to add ends at once, with the target untouched.
- **`Reinstall_Infra.bat QA|PROD`: infrastructure only** (12.4).

**12.2 QA first, always (owner).** "Successful QA verification is required before every ordinary PROD installation,
including both new variant batches and REINSTALL INFRA."
- **A QA pass** is written only by an operation on the QA tree that ends with QA tested as a whole (12.3). It records
  the complete list of QA's installed software, file by file with hashes, and the hashes of the tests and of the
  install tool that were used.
- **Every PROD installation checks, and refuses on any difference, naming the file:**
  1. QA's tree still equals its latest pass (nothing changed in QA since it passed).
  2. Every file about to be written to PROD: DEV's bytes are the bytes that passed.
  3. After the operation, PROD's infrastructure is exactly the infrastructure that passed: the same files, the same
     bytes.
  4. Every variant and helper in PROD after the operation is in the pass with the same bytes.
  5. The tests and the install tool in DEV are the ones that passed.
- **"Changes after QA verification require another QA pass":** a file edited in DEV after the pass fails check 2.
- **"Do not implement a QA-bypass mechanism":** no option, setting or prompt skips these checks. If QA is lost, it is
  created again (12.5) before anything is installed in PROD. A restore is not an installation and is not affected.
- A PROD installation shows the batch and the pass it rests on, and the owner types **one** confirmation for the
  whole batch. Nothing is confirmed per variant, and nothing is activated afterwards.

**12.3 What QA tests** (by itself, as part of the QA operation).
1. The whole test suite, run with QA's own Python on a temporary copy of the candidate; tests are never installed.
2. The structure: add-only kept; declarations valid; the import check.
3. **Regression of what was already installed.** Recompute forecasts and scores of installed variants from QA's own
   canonical files and require identical content. After a variant install: a fixed sample. After an infrastructure
   change: every forecast and every score of every variant.
4. The research job in QA, to the end: every new variant fills its whole history on QA's copy of the real results.
   The owner can read QA's league reports before deciding on PROD.
Only if all four succeed is the pass written.

**12.4 Infrastructure** (owner: REINSTALL INFRA).
- **What it is:** the files named, one per line, in `deploy/INFRA_MANIFEST.txt`: the reader, the readout, the list and
  job code, scoring, reports, OV-1, the guard, backup and restore, the launchers and the owner's four environment
  scripts. Nothing is infrastructure unless it is on the list; a test requires the list to hold every project module
  those files import. **Not on it, and never installed outside DEV:** documents, the exchange, tests, Git files,
  unmarked variants, DEV's results, and the proof-of-concept coordinator and probes with their plumbing.
- `Reinstall_Infra.bat` shows every file it would add, overwrite or remove, with both hashes and the differences, and
  touches nothing under a family folder or `_shared/`.
- **An infrastructure change that alters any earlier forecast or score is a scientific change, not maintenance.** In
  QA the full regression (12.3, 3) then fails, no pass is written, and so it cannot reach PROD. The way forward is a
  separately reviewed correction or new variants, never this command.
- One kind of change at a time: it refuses if QA's Python environment has changed since QA's last pass (section 13).

**12.5 Creating a tree: `Init_Tree.bat QA|PROD`.** For a root that does not exist or is empty. It writes the tree's
`ENVIRONMENT.ini`; installs the infrastructure and every ready variant; copies the accepted results (QA: from PROD, or
from DEV while no PROD exists; PROD: from DEV, the first time); stops for the owner to build the environment with his
scripts; verifies it. `Init_Tree.bat QA` ends with the tests of 12.3 and a pass. `Init_Tree.bat PROD` is a PROD
installation under 12.2. No result, score or report is ever copied into a new tree.

**12.6 Installation is release** (owner). The next research job finds the new variants and fills their history.

## 13. The Python environment

- Each tree's `.venv` is built by the owner with his own scripts, in that tree. It is not pinned to a draw (owner): a
  draw computed late runs in whatever environment the tree then holds, and its digest is in the line's envelope.
- **Verified before use.** `Verify_Tree.bat QA|PROD` runs the suite with that tree's Python and, on success, writes
  `.venv\ENVIRONMENT_VERIFIED.json` with the environment's full digest. Launchers refuse without it; each job compares
  the full digest at its start; the owner's install script removes the marker before changing anything.
- It also recomputes a fixed sample of the tree's forecasts and **reports** any difference. After an environment
  change such differences are information for the review below; they do not by themselves refuse.
- **W-23 is unchanged** (owner). Every dependency upgrade: the reviewer's assessment and the owner's go first; DEV
  rebuilt and the evidence of H-1 5.4 produced; then QA rebuilt and verified, which gives a new QA pass; the reviewer
  sees both; then PROD: a backup, the rebuild, `Verify_Tree.bat PROD`.

## 14. Backups and restore (owner; EX_259 section 7; EX_261 P06)

- **A backup is one ordinary ZIP of a whole tree:** installed software, accepted results, canonical files, reports,
  records, `ENVIRONMENT.ini` and the complete `.venv`. Only two temporary control files are left out. It is written to
  that tree's own backup root, checked twice (the archive read back; every source file read again), and called a
  backup only when both checks pass and the tree was quiet throughout.
- **When:** at the end of every research job; before and after every install, infrastructure reinstall and
  environment verification; at the end of a tree's creation; and whenever the owner runs `Run_Snapshot.bat`.
- **If a backup cannot be made, the job goes on** with a standing warning until one is made (owner). One exception: a
  PROD installation stops before changing anything if the recovery kit cannot be written to PROD's backup root.
- **The recovery kit:** a small checked ZIP in the backup root for each software state, holding the restore tool and
  plain instructions. It needs only an installed Python: not DEV, not QA, not a working tree.
- **Restore puts back exactly one chosen backup, at the path it came from** (owner). The old tree is renamed aside,
  never deleted. Nothing is installed, upgraded, rebuilt, withdrawn or brought back from anywhere else. No Python
  program may be running on the PC. Then the ordinary job catches up, with that backup's variants. Any change after
  that is a separate decision by the owner, through QA like any other.
- If the restored environment does not start, the restore says "RESTORED; ENVIRONMENT NOT READY" and the owner decides.
- QA has the same tools with its own roots. QA backups on QA's own drive are permitted, with a warning that they do
  not survive the loss of that drive.
- The accepted results and PROD's research exist only in PROD and its backups. Nothing is copied back to DEV or to
  Git by the system (choice E, section 19).

## 15. Safety rules kept, unchanged

No program ends another process. Before a job, an install, a backup or a restore the process rules of the deployment
design apply. An orphan marker blocks every launch until the owner's approved clearance. The three safety switches
stay False and the allowlist empty. Only the one reviewed updater contacts Lotterywest-GOV, only in PROD; no AI chat
and no other program contacts any lottery site. No program changes the PC's date, time or zone. No program deletes
research data; the only removal of bytes is a torn last line (5.7), and DEV's stale scratch lists are moved, not
deleted.

## 16. The owner's commands, and what refusals mean

| Where | Command | Purpose |
|---|---|---|
| DEV | `Make_Installable.bat` | mark a finished variant ready |
| DEV | `Install.bat QA`, then `Install.bat PROD` | add new variants |
| DEV | `Reinstall_Infra.bat QA`, then `PROD` | update infrastructure |
| DEV | `Init_Tree.bat QA`, `PROD` | create a tree |
| DEV | `Check_Tree.bat QA` or `PROD` | read-only: what is installed, what is ready, any drift, backups, locks |
| any tree | `Run_Research.bat` | the research job |
| QA, PROD | `Verify_Tree.bat`, `Run_Snapshot.bat`, `Withdraw_Variant.bat` | environment check; backup now; withdrawal |
| a kit | `Restore.bat --snapshot <zip>` | exact restore |

Every refusal prints one line saying what was found and one saying what to do. The main ones: "not the QA-tested
bytes: <file>" (run the QA step again); "already installed with different bytes" (give the changed work a new variant
name, or return QA to its backup from before that install and install again); "an install did not finish" (run the
same command again, or restore the backup taken before it); "environment not verified" (`Verify_Tree.bat`); "this tree
is not <role>" (the settings file and the folder disagree); "results changed other than by growing"; "a process of
this tree is running"; "orphan marker present". A STOP is a STOP: nothing retries by itself.

## 17. From the old system to this one (owner: a clean baseline, nothing destroyed; EX_259 B; EX_261 F04, P07)

**17.1 What "clean" means.** The new trees start with the accepted official results and no derived record. All history
is computed again by the first jobs. Nothing recomputed is ever described as forecast or published at the original
time. The sealed Mode H records, the old run folders and the old reports are not in QA or PROD.

**17.2 The old state is preserved before anything changes, and it is said plainly which copy holds what.**

| Copy | Holds | Does not hold |
|---|---|---|
| The owner's source ZIP from GitHub | tracked files at one commit | Git history; ignored files (old run folders with their forecast records); any environment |
| **A verified cold ZIP of the project clone folder** (the one folder named as DEV's root in its settings file; never the E: drive), written to a cold-backup folder the owner names | everything in that folder: tracked files, `.git`, the ignored run folders | by default the old `.venv` (it can be rebuilt; including it is the owner's choice) |
| GitHub | tracked files and history | ignored files |

- Before the cold ZIP is made, a dry run prints the file count and size of each top-level folder and what would be
  left out, and writes nothing. The owner then decides its scope (choice C, section 19). Making it needs its own go.
- **The cold ZIP is the only copy of the old forecast records that Git does not track.** That is its value. Its cost is
  disk space and time, once.
- **Rollback, stated truthfully.** Phase 1 moves source files inside the DEV clone, so after phase 1 the clone is no
  longer the old system. A Git tag brings back the old source, not the ignored records. **The old system can be run
  again only from an untouched copy:** unpack the cold ZIP into a new folder (never over the clone), build its
  environment with its own scripts, and run it there. Until PROD is declared in use, that is the rollback.
- QA and PROD are new folders; creating them changes nothing in DEV and deletes nothing anywhere.

**17.3 Two implementation phases, each verified by itself** (owner).
- **Phase 1: layout only, in DEV.** Method files move to the layout of section 3; import lines change; no computation,
  contract or record changes (the old revision field is still there at its end). Evidence: a listing showing each
  moved file's bytes unchanged apart from imports; the existing suite; and **the equivalence oracle:** every existing
  variant, both games, every target with an old development forecast, recomputed by the moved code and compared by
  the old content digest. It reads the old records, writes no research record, and needs the owner's go.
- **Phase 2: this specification.** New code is added in DEV beside the old; nothing is removed from DEV (the old
  system's modules stay there for the proof-of-concept suite, unlisted in the infrastructure manifest). Then, in
  order, each on its own go: `Init_Tree.bat QA`; **the transition check** in QA; `Init_Tree.bat PROD`; PROD's first job.
- **The transition check** compares, for every (variant, target) the old system forecast in development, the new
  forecast in QA with the old record: the score of every number, the ranking, TOP and WORST. It compares that
  scientific content, not whole-record digests, because the record format has changed (P07). It is a program of the
  transition package, outside the infrastructure; it reads the old records in DEV or in an unpacked cold copy,
  read-only; a difference stops the transition for review. After it, no part of the new system reads an old record.
- The file-by-file starting list for the code rounds is section 10 of the simplification design v0.1, with three
  changes: the coordinator and its plumbing are not installed outside DEV; install and release records and Git are
  gone from deployment; the install tool works from local files (deployment design).

## 18. Tests the code rounds must show (functional faults, not fraud)

On invented games and toy variants unless marked (real):
- **Records (F01):** 100 forecast and scored, 101 `METHOD_FAILED`, 102 forecast and scored: valid, and the job goes on;
  a first target fixed by minimum history, and a method-declared insufficient history; a gap, a repeat, a score
  without a forecast, a second score, an unscored forecast that is not last, a line after a withdrawal, a broken
  chain: each refused; a torn last line in each file, cut and redone; any other exception writes nothing and stops;
  a crash planted between every two writes of 5.7, then the job again, gives the bytes of an uninterrupted run.
- **N-1 (F06):** draws at and after T changed and appended: T's content digest unchanged, its envelope changed; the
  same variant recomputed in the same environment gives the same content.
- **The job:** the four examples of 7.2 line for line; the results step absent, failing and left out; results changed
  other than by growing; QA and DEV never start the updater.
- **OV-1 (F03):** no prevailing line before the start; the start fixed only after a successful results step; a later
  variant's `FORWARD_FROM`; a cohort member with `NO_FORECAST`; a missing member blocks; a withdrawn member leaves the
  cohort at its draw and earlier lines are byte-identical; the ledger equals its rebuild; the fixed text.
- **Withdrawal (F02):** the line and its draw; the pending forecast left unscored; reports and both scores afterwards;
  a restore to before it runs the variant again.
- **Readiness and installing (F08 to F10; the QA rule), with the examples of EX_262:** two ready variants and one
  unfinished in DEV, `Install.bat QA` adds the two only; one is edited afterwards: its marker no longer matches,
  `Install.bat PROD` refuses it by name, and the other is installed; a hand-made marker with a wrong hash is not ready;
  an import not on the helper list is not ready; a helper present with other bytes refuses; an existing variant is
  never overwritten; `Reinstall_Infra.bat` changes one listed file and no variant; an infrastructure change that
  alters one old forecast gets no QA pass; each of the five checks of 12.2 with one planted difference; QA changed
  after its pass; **no command line makes a PROD install succeed without a pass;** an install stopped at every step,
  then the command again; nothing half-installed is ever run.
- **Roles (F09):** QA's settings pointing at PROD's folder refuses; a QA tree copied to another place refuses; a
  backup root inside the tree refuses; QA and PROD backups land in their own roots.
- **Backup and restore:** as the deployment design lists, including that a restore installs nothing afterwards.
- **(real)** Phase 1's oracle; the transition check.
One planted defect for each rule. The whole suite before and after each install.

## 19. Still for the owner at ratification, and for the reviewer

**Owner's choices (my recommendation first; none blocks the review).**
- **A. The results step in PROD.** The job runs the reviewed updater itself, through the updater's own unchanged
  launcher, with `--no-update` to leave it out (recommended: one weekly command). Or the owner runs the updater
  himself first, as his decision of 4 November 2026 has it. Either way no other program can be reached: the job
  names that one launcher, and a test pins it.
- **B. `FORWARD_FROM`** as section 10.2 and 10.3 (recommended), or "the last draw on file at installation, plus one".
- **C. The cold ZIP of the old project clone:** the whole clone folder without the old `.venv`, after the dry run
  (recommended); or with it; or only the GitHub source ZIP plus the old `results` folders copied by hand.
- **D. Withdrawal** as section 11: one line in the variant's own file, by one command with one typed confirmation.
- **E. Nothing is copied back from PROD to DEV or Git** (recommended: the backups are the record, and it removes a
  whole mode of the old design). It changes the decisions of 16 and 17 November 2026 to commit results and score
  records. Or a small read-only export of the accepted results and the reports.

**For the reviewer.**
1. Do 5.2 to 5.7 close F01, including the metadata lines and the crash order?
2. Is 12.2 a faithful and sufficient form of the owner's QA rule? Is check 4 (every PROD variant is in the QA pass)
   right, or stricter than needed?
3. Is a sample regression enough after a variant-only install, with the full one kept for infrastructure?
4. Section 13 reports, and does not refuse on, numerical differences after an environment change, because the
   environment is not pinned and W-23 reviews them. Acceptable?
5. QA and DEV receive results only by copy from PROD, so the lottery site is contacted from one tree. Acceptable?
6. The coordinator and the proof-of-concept suite stay in DEV only. Any objection?
7. Is anything a routine owner needs missing from section 16?

## 20. Not tested, and uncertainties

- Nothing has been run. No timing is known: a first full fill, a full regression in QA, or a backup of a tree.
- The static import check assumes ordinary import statements; a method importing by a computed name would escape it.
- The readout may carry the old run mode deeper than its record fields; the transition check is what would show it.
- DEV's working files are the install source. If Git rewrites line endings in DEV, hashes change: markers stop
  matching and a helper may be refused. That fails safe; pinning line endings for `src/` in `.gitattributes` avoids it.
- Section 1.2 names the binding clauses by section. An exact clause list for E2R-1 section 7 is a first task of the
  code round.

## 21. Where each review finding landed

| Finding | Where |
|---|---|
| EX_261 F01 record states, metadata, crash order | 5.2 to 5.7; 18 |
| F02 owner-only withdrawal | 11; 10.4; 9 |
| F03 `FORWARD_FROM` wording, first job, failed updater | 7.1, 7.2; 10.2 to 10.4, 10.6 |
| F04 cold copy scope; rollback truth | 17.2 |
| F05 a coherent install and update sequence | 12; deployment design sections 4 to 6 |
| F06 content and envelope | 5.4; 6; 18 |
| F07 one complete specification | this document; 1.2 and 1.3 |
| EX_262 F08 marker, ready-and-absent, local files | 3.4; 4; 12.1 |
| F09 roles, settings, backup roots | 2; 14; deployment design section 1 |
| F10 REINSTALL INFRA | 12.4 |
| The owner, 21 November 2026: QA before every PROD installation, exact files, no bypass | 12.2, 12.3; deployment design section 3 |

End of the specification, DRAFT v0.1.
