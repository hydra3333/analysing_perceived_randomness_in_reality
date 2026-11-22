# Predictive Randomness - specification of the active research system - DRAFT v0.6

**Status:** DRAFT v0.6 for independent review (EX_270). It is DRAFT v0.5 with the four focused corrections and the notes of
EX_269 (R7-F01 to R7-F04, R7-N01 to R7-N03): counted changes only, in sections 5.8, 7A.2, 7A.4, 7A.5, 9, 12.4, 12.7,
14.2, 18 and 21. `SPEC_v0_5_TO_v0_6.diff` is exact. Nothing else is changed and no new mechanism is added. Not
ratified. It authorises nothing. Until the project owner ratifies it, every ratified document stands and nothing is
coded, moved, installed, run, migrated or deleted.
**Written:** 22 November 2026, by the Claude web chat (primary designer and coder), on the project owner's request of
12:56 (decision log entry 145).
**Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner, after the review.
**Risk tier:** HIGH. **Companion:** the deployment design DRAFT v0.12 (how the installs, copies, backups and restores are
carried out). **Marking:** "(owner)" marks a direction the owner has given, with its decision log entry. Everything else
is a mechanism proposed for ratification.
**Words used throughout (owner, entry 136):** *restore from backup* (put back exactly one chosen backup); *walk-forward*
(forecast each draw from the draws before it, then score it); *catch-up* (the walk-forward over draws not yet done);
*historical walk-forward rerun* (an owner-requested recomputation of draws already done); *QA software replacement from
PROD*; *research-data reseeding from PROD*.

## 0. The whole system in plain English

1. **Three separate folders, each complete in itself:** DEV (where methods are written; the Git clone on E:), QA (the
   owner's laboratory; on D:), and PROD (the real research; on G:). Each has its own data, results, Python environment
   and backup folder. Their places are set in a small settings file, never in code.
2. **One science in every tree** (owner). DEV and QA compute exactly as PROD does, from their installed software and
   their own settings file. No formula, rule or check is different because a tree is QA or DEV.
3. **A method is a family; a family has one or more variants; a variant's scientific files never change once
   installed.** A changed method is a new variant. Nothing is retired automatically; the owner alone can withdraw a
   variant that is wrong, and a withdrawal is one-way.
4. **A variant's status is in a small readable file beside its software** (owner): whether it is withdrawn, from which
   draw and why, and the first draw at which it counts in the prevailing OV-1.
5. **A variant becomes installable** when a small marker file in its DEV folder says so and matches its files exactly.
   `Install.bat PROD` adds every marked variant PROD lacks, checks it in place and asks for one confirmation. QA is
   never required. Shared system code is updated by a separate command, with a marker of its own. **A
   fault in shared code is corrected in place by a third command, after which every variant it can affect is
   computed again** (owner; 12.8).
6. **One command does the research:** it works out what is missing, forecasts and scores it draw by draw from earlier
   draws only, fetches new official results (in PROD), saves a league report after every draw, keeps the two OV-1
   scores, and forecasts the next draw. It is safe to run at any time and after any interruption.
7. **Every result is one line in a list.** Ordinary work only ever adds lines. That is what prevents double counting
   and lets an interrupted job carry on.
8. **Three further operations exist, each only on the owner's own command, and none starts another** (owner): the
   **QA software replacement from PROD** (QA's installed software becomes PROD's); the **research-data reseeding from
   PROD** (QA's or DEV's research data becomes PROD's); and the **historical walk-forward rerun** (past draws computed
   again in the tree he names). PROD is only ever read by the first two.
9. **Backups are complete copies of a whole tree,** checked when made. A restore puts back exactly one backup and
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

## 2. Three roles, three trees (owner; EX_262 F09; entries 135, 136)

| | DEV | QA | PROD |
|---|---|---|---|
| Purpose | write and try methods; build installs | the owner's laboratory: a mirror of PROD when he makes it one; or PROD plus the things under test; or something else he is trying | the research |
| Example root | the Git clone on E: | `D:\TEST_BED` | `G:\a_p_r_i_r` |
| Holds | all source, tests, documents, unfinished variants, its own research results | installed software only; its own accepted results; its own results; its own `.venv` | the same, for real |
| Variants that run | every variant folder with a valid `VARIANT.json`, finished or not | installed variants only | installed variants only |
| Official results | a checked copy from PROD | a checked copy from PROD | the one reviewed updater |
| Backups | Git, and the owner's own ZIP of section 17 | its own backup root | its own backup root |

- **Each tree's root holds `ENVIRONMENT.ini`,** which states its role, its own root, its backup root and its
  environment folder. A tree is what its own file says it is: a copy of QA placed somewhere else does not become
  PROD. Every launcher checks the file against the folder it is in. The backup root must lie outside the tree.
- **DEV's file also names where QA and PROD are.** No drive letter or path appears in any program.
- **One science in every tree (owner, entry 136).** The trees differ only in what their settings files state: the
  role, the paths, and where the accepted results come from. No calculation, cohort rule, eligibility rule, check,
  warning or confirmation is written differently for QA or DEV. There is no "sandbox" mode and no QA version of OV-1.
  When QA holds PROD's software, status files and research data it must give PROD's results, and a difference is
  something to explain (the Python environment is the usual cause), never something to wave away. Two limits are
  about safety, not science: only PROD may run the updater, and PROD is never the destination of a copy.
- **QA is never a gate** (owner, entry 126). No install into PROD reads QA or asks about it.
- **What may pass between trees, and nothing else:**

| From, to | What | By |
|---|---|---|
| DEV to QA; DEV to PROD | ready variants; infrastructure | `Install`, `Reinstall_Infra`, `Init_Tree` (section 12) |
| PROD to QA | PROD's installed software, with each variant's status file | the QA software replacement (12.7) |
| PROD to QA; PROD to DEV | the accepted official results | the results step of the research job (7.1) |
| PROD to QA; PROD to DEV | the complete research data | the research-data reseeding (14.2) |

  PROD is opened for reading only by these. Nothing ever passes from QA or DEV into PROD, and QA's and DEV's results
  go nowhere.
- **Git and GitHub are DEV conveniences only** (owner). No install, run, copy, backup or restore needs them or a
  network.

## 3. Families, variants and their code (owner; EX_259; EX_262 items 3, 8; entries 127, 136)

**3.1 Identity** is (game, family, variant); a result adds the target draw number. There is no revision.

**3.2 Layout, the same for every family, including a family of one:**

    src/methods/
        E_002/
            core_v1.py                       optional: computation shared by this family's variants (immutable)
            RECUR_MEAN_ALL_V1/
                method.py                    compute(task, view), verify(...)          scientific, immutable
                VARIANT.json                 the declaration (3.4)                      scientific, immutable
                VARIANT_STATUS.ini           this tree's operating status (3.5)         changes only as 3.5 says
                I_AM_INSTALLABLE.json        DEV only: the readiness marker (section 4)
        _shared/
            recurrence_gaps_v1.py            helpers used by more than one family (immutable, versioned by name)
        _common/                             infrastructure (section 12.4)

**3.3 Add-only.** In QA and PROD, a variant's scientific files and every helper file under a family folder or `_shared/`
are never changed or removed by an install. A changed implementation is a new variant folder; a changed helper is a
new file with a new name (`core_v2.py`). Helpers are not scored and are not installed for their own sake: a helper
arrives with the first variant that names it. Prefer code inside the variant's folder. **Three things, and only
these, change what an installed variant folder holds:** the status file, as 3.5 says; the QA software replacement
from PROD, in QA only (12.7); and a restore from backup (section 14). **One command only may overwrite a helper: the
correction of a defect (12.8).**

**3.3A A helper changes in exactly two ways, and the owner says which (owner, entries 127, 143).**
- **A changed idea** (a different calculation is wanted): a new file (`..._v2.py`) and a **successor variant** for each
  variant that is to use it. The old variants stay installed and running, beside the new, until the owner himself
  withdraws any of them (section 11); nothing withdraws them for him. `Who_Uses.bat` and `Make_Successors.bat` do the
  typing (section 4).
- **A defect** (the helper does not compute what was always intended): the helper is corrected in place by the
  correction command, and every variant that uses it is computed again over its whole history (12.8). The names
  stay; their fingerprints change, because the fingerprint covers the helper (3.4).
No ordinary install ever overwrites a helper.

**3.4 `VARIANT.json`, the scientific declaration:** the family and variant identifiers (equal to the folder names); a
title and one line of description; the games supported; for each, the minimum number of earlier draws needed; the
observation view; **`files`: the exact list of the folder's own scientific files** (`method.py` and any other); and
**`helpers`: the exact list of helper files this variant uses.**
- **The variant's fingerprint** is computed from exactly these: `VARIANT.json`, the files it lists and the helpers it
  lists. Each is hashed as its bytes on disk (SHA-256). The fingerprint is the SHA-256 of the lines
  `<path from src/methods, forward slashes><TAB><sha256><LF>`, sorted by path. Nothing else enters it: not the status
  file, not the marker, not a cache.
- **Any other file in the variant's folder is a fault,** except `VARIANT_STATUS.ini`, `I_AM_INSTALLABLE.json` and
  Python's own `__pycache__` folders and `.pyc` files, which are ignored. An editor's backup or a scratch file is
  therefore named and refused ("not on the declaration's list: remove it or list it"), never silently hashed or
  silently skipped. Launchers run Python so that it writes no cache in QA or PROD.
- **Imports are checked statically.** Every import of project code made by a listed file or helper must be a plain
  `import` or `from ... import` statement naming a file on the `helpers` list or the infrastructure. **Importing by a
  computed name is forbidden in a variant's files and in helpers:** any use of `importlib`, `__import__`, `exec`,
  `eval` or a change to `sys.path` there fails the check. That is the whole of dependency handling: no resolver.

**3.5 `VARIANT_STATUS.ini`: the variant's operating status, beside its software (owner, entries 136, 137).** One small
file in every variant folder, in every tree, readable in Notepad:

    ; E_002 / RECUR_MEAN_ALL_V1 - operating status in THIS tree.
    ; Written only by the project's commands. Do not edit by hand: a hand edit is detected and the game refuses.
    [POWERBALL]
    status = WITHDRAWN
    withdrawn_from_draw = 1601
    withdrawn_reason = the gap table was built from the wrong column
    withdrawn_recorded = 2027-01-05 19:42; results on file through 1600
    prevailing_ov1_first_eligible_draw = 1596
    prevailing_ov1_eligibility_recorded = 2026-12-01 20:10; results on file through 1595 after a successful results step
    [OZLOTTO]
    status = ACTIVE
    prevailing_ov1_first_eligible_draw = 1712
    prevailing_ov1_eligibility_recorded = 2026-12-01 20:31; results on file through 1711 after a successful results step
    [check]
    sha256 = 5f0c...e91a

- **It holds, for each game the variant supports, exactly two facts, each set at most once:** whether the variant is
  withdrawn, from which draw and why (section 11); and the first draw at which it counts in the prevailing OV-1
  (10.2). The two "recorded" lines are for the reader; no rule reads a date.
- **It is the authority.** The research engine reads it, in every tree and in every kind of run, to decide whether the
  variant is forecast and scored at a draw and whether it is in the prevailing cohort at a draw. No copy of these
  facts in any other file outranks it.
- **Who writes it, and no one else:** the installer creates it (`ACTIVE`, nothing more) when the variant is installed;
  `Withdraw_Variant.bat` writes the withdrawal, on the owner's command; the research job writes the eligibility draw,
  once (10.2); the QA software replacement brings PROD's file with PROD's software; a restore brings the backup's. In
  DEV, where nothing is installed, the job creates a missing file as `ACTIVE`; in QA and PROD a missing file is a
  refusal. Git ignores the file: it is the state of one tree.
- **How it is written:** the whole file to a temporary name, then one rename. The `[check]` line holds the SHA-256 of
  every byte above it. A file whose check fails, or which the standard INI reader rejects, refuses that game and
  names the file. The way out is to take the file from the newest backup ZIP (it is an ordinary file in an ordinary
  ZIP), or a restore, or in QA the software replacement. The check is against accidents, not a signature.
- **It never changes the science.** It is not in the variant's fingerprint, not on the readiness marker, and not
  copied by an install from DEV. Withdrawing a variant creates no new variant and alters no scientific byte.

## 4. Readiness in DEV; the registry in QA and PROD (owner; EX_262 F08; EX_264 R5-F02)

- **The marker `I_AM_INSTALLABLE.json`** holds the variant's fingerprint and the list it was computed from (3.4):
  `VARIANT.json`, the declared files and the declared helpers, each with its SHA-256. **It does not list itself,** nor
  the status file, nor any cache. `Make_Installable.bat <family> <variant>` validates the declaration, runs the
  import check, refuses any undeclared file in the folder, and writes the marker. A marker made by hand counts only
  if it validates the same way. One small utility and an ordinary hash list: no receipts, no resolver.
- **It is bound to content.** If any listed file changes afterwards, the marker no longer matches and the variant is
  not ready until the marker is made again. Running it again on unchanged files gives the same marker bytes. A marker
  nominates a variant; it proves nothing about correctness, and it is not the owner's approval.
- **Ready** means: a valid declaration, a matching marker, and the import check passing.
- **In QA and PROD there are no markers.** A variant exists and runs when its folder is installed with a valid
  declaration. As a check against accidents, each tree keeps one list of every installed software file and its hash
  (status files are on it by name only, since their content changes); the job refuses to run if the tree does not
  match it.
- **In DEV** the research job may run any variant folder with a valid declaration, marked or not, against DEV's own
  research results.
- **Three DEV conveniences** (owner; they touch nothing outside DEV). `Who_Uses.bat <helper>` lists every variant whose
  declaration names that helper. `Make_Successors.bat <old helper> <new helper>` copies each such variant to a new
  folder with the next version number in its name and rewrites its helper reference and declaration. **It refuses if
  any new folder name already exists; it changes no existing folder; it copies no marker and no status file; it marks
  nothing and withdraws nothing** (EX_264 Q8); the owner reviews the result. `Make_Installable.bat` accepts several
  variants at once, and `--unmark` removes markers.

## 5. The canonical record (EX_259 D; EX_261 F01, F06; EX_264 R5-F01)

**5.1 Two list files per variant per game:**

    results/research/<GAME>/variants/<FAMILY>/<VARIANT>/forecasts.jsonl
    results/research/<GAME>/variants/<FAMILY>/<VARIANT>/scores.jsonl

Every line carries the digest of the line before it. **The research job only ever appends to them.** Lines leave a
list in exactly two ways, each only on the owner's own command with a confirmation: a historical walk-forward rerun,
which first saves the old lines in a verified archive (section 7A), and a research-data reseeding, which replaces a
QA or DEV tree's research data with PROD's (14.2).

**5.2 Lines.** Each file begins with a `HEADER`: game, family, variant, the variant's fingerprint, and the identity
of the shared forecasting code the list was begun under (12.4); the forecast file's
header also holds `first_target` (the first draw with enough earlier draws). After it come only result lines: `TARGET`
lines in the forecast file, one per draw from `first_target`, ascending by one; score lines in the score file. **A
variant's status is not kept in its lists:** it is in its status file (3.5), and only there.

**5.3 A `TARGET` line is one of exactly two things.**
- **`FORECAST`:** for every barrel of the game, the score of each number, the full ranking, and complete TOP and WORST
  sets. Anything less is not a forecast.
- **`NO_FORECAST`,** with one typed reason. `INSUFFICIENT_HISTORY`: the method returned its declared "not enough
  history" result. `METHOD_FAILED`: the method raised the one declared exception type for a failure of its own
  mathematics (for example a fit that cannot be made), or its output failed the readout's validation or its own
  `verify`. A `NO_FORECAST` line is final for that target and can never be scored.
- **Anything else that goes wrong** (any other exception, a missing module, memory, the disk, an interruption) writes
  no line. The job stops for that game and says why. Running it again tries again. An environmental fault is never
  recorded as a method failure.

**5.4 Content and envelope** (F06). Each `TARGET` line has two parts.
- *Content,* with its digest: the identity; the target; the digest of the **permitted view** (the draws before the
  target, and nothing else); the variant's fixed configuration and seed; the status and the forecast itself.
  **Nothing in the content, and nothing given to the method, depends on any draw at or after the target, or on the
  results file as a whole.**
- *Envelope,* for audit only: the version and SHA-256 of the whole results file at the time; the digest of the
  forecasting code (12.4) and of the environment; **where it was computed** (the tree's role and root); **whether the
  target's result was already on file when it was computed;** the rerun's name if a historical walk-forward rerun
  made it (7A); the time.
The same code, configuration, seed and earlier draws in the same environment give the same content digest whatever
is appended to the results later. Across a changed environment identical bytes are not promised.
**The envelope is how the truth about evidence is kept, in every tree alike** (owner, entry 136): a line computed after
its draw was known says so and is never shown as a forecast made before it; a line copied from PROD still says PROD.
No tree computes differently because of it.

**5.5 The score file** has one line for each scored `FORECAST`: the target, the forecast content's digest, the numbers
drawn (quoted with the results file's version and hash), the TOP and WORST matches for each barrel, the prize
divisions, and the digest of the scoring code. Its lines ascend. A `NO_FORECAST` target has no score line.

**5.6 The invariants,** checked whenever the files are read.
1. The chain is unbroken and the first line is the header.
2. `TARGET` lines run from `first_target` upward by one with no gap and no repeat.
3. Every score line names a `FORECAST` line by target and content digest; no target is scored twice.
4. **Scoring is in order and complete:** if a `FORECAST` has no score line, no later target has one. An unscored
   `FORECAST` is one of three things, and each has a name: **pending** (its result is not on file); **withdrawn**
   (the variant is withdrawn from that draw: it is never scored; R5-F01); or **withheld** (5.8).
5. **The list agrees with the status file.** For a variant withdrawn from draw T: no `TARGET` line beyond T, and no
   score line at T or beyond. A `FORECAST` at T itself, made before the withdrawal, stays as history, unscored for
   ever.
A break of 1 to 3 in a list that belongs to the tree is a fault: that game refuses and names the line. A list that
does not belong is handled by 5.6A.
*Example (F01):* target 100 `FORECAST` and scored; 101 `NO_FORECAST: METHOD_FAILED`; 102 `FORECAST` and scored. Valid:
101 is resolved by its own line and needs no score.
*Example (R5-F01):* results on file through 1600; the variant holds a pending `FORECAST` for 1601; the owner
withdraws it, effective 1601; next week 1601's result arrives. The forecast is still there and is never scored; no
line for 1602 is ever written; the variant is absent from 1601's league scoring and from both OV-1 scores at 1601.

**5.6A A list that does not belong to this tree's software or status (owner, entry 129: "warn about them, ignore them
and continue").** A list is **foreign** when its variant is not installed here; or its header's fingerprint is not the
installed variant's; or its header's forecasting-code identity is not that of the forecasting code installed here;
or it breaks invariant 5 against this tree's status file. This arises after a research-data reseeding, a QA software
replacement, or a correction of shared code (12.8). A foreign list is named in a warning at every job, is never
appended to, and counts in no report and in neither OV-1. If the variant is installed here it is **held**: the job
computes nothing for it in that game until the owner clears the foreign list by one of three things: a rerun for
that variant (7A; the foreign list is archived and the variant is computed with this tree's own software), a
research-data reseeding, or in QA the software replacement. Nothing is moved, merged or repaired by itself, and
there is no import folder or second registry: the header is the whole of the mechanism.
**"Ignore and continue" never means a score computed without a member it should have (EX_267 N02).** A held variant
that belongs to the prevailing cohort blocks the prevailing line (10.4); and because the stored reports and OV-1
records were built with the list that is now foreign, the game's derived results are marked not current from that
variant's first draw (5.8) until the owner settles it.

**5.7 What to do next is read from the files and the status files, never remembered** (crash resume). For a variant
that is not held, with the draws on file through N, and W its withdrawal draw if it has one:
- every target from `first_target` to N with no `TARGET` line, **and below W,** is computed, in order;
- every `FORECAST` whose result is on file, with no score line, **at a target below W,** is scored, in order, unless
  the game's derived results are being withheld (5.8);
- target N+1 is forecast if it has no line **and N+1 is below W.**
**A torn last line** (a crash while writing) is not a record: it is cut off before the next append. The write order
for a draw is: forecast lines, score lines, the prevailing OV-1 line, the report. Each step is skipped if already
done, so a crash between any two is repaired by running the job again.

**5.8 The derived results are checked in full, and what is not current is made to look not current** (EX_267 R6-F02).
- **What is stored evidence and what is only a print-out.** The score lists and the prevailing ledger are stored
  results. The league reports, the next-draw report and the exploratory OV-1 are print-outs: they are never checked,
  because they are made again from the lists whenever anything changes.
- **What the check compares.** At its start the job recomputes, in memory, every score of the game and the whole
  prevailing ledger, with the installed code, from the stored forecasts, the results on file and the status files,
  and compares **the scientific content only**. For a score line: the target, the forecast content's digest, the
  numbers drawn, the TOP and WORST matches for each barrel, and the prize divisions. For a prevailing line: the
  draw, the cohort with each member counted or "no pair", the weights, V, X, Z, and the six log-factors and running
  sums. **Not compared, because they rightly differ over time:** the version and hash of the results file quoted when
  the line was written, any code digest, the rerun's name, where and when it was computed. Those are checked only
  for being well formed. So a results file that has since grown, or scoring code rewritten without changing an
  answer, raises nothing.
- **If the content differs from some draw X on** (the scoring or OV-1 code was changed; the data came from a tree with
  other software or status; variants were added, removed or held), the game's derived results are **not current from
  X**. The job then: writes one small file, `results/research/<GAME>/NOT_CURRENT_FROM.json`, holding X and one of two reasons
  (`MISMATCH`, here; or `AWAITING_CATCH_UP`, below);
  **moves every report file for a draw at or after X, and both OV-1 print-outs, out of the active reports folder into
  `reports/not_current/`,** so that nothing left in the active folder is stale; makes the exploratory OV-1 and the
  league reports again only up to the draw before X; writes no score, prevailing line or report at X or beyond; and
  alters no stored line. Forecasts go on, so the next draw is never lost. Every program that writes or reads a
  report honours that one file. The job says which draw, and names the command that settles it: the derived-only
  rerun (7A), which removes the file when it has finished.
- **The two reasons are treated differently** (EX_269 R7-F01). `MISMATCH` means stored results disagree with the installed
  code, or a list is foreign: nothing is written at X or beyond until the owner's rerun. `AWAITING_CATCH_UP` is
  written only by a rerun that the owner stopped at draw N (7A.2): the results before X = N+1 are right and those
  from X on are simply not computed yet. Then the ordinary job compares only the draws before X, and **goes on to
  catch up from X in draw order exactly as for newly arrived draws:** forecasts, scores, prevailing lines, reports.
  When every draw to the last on file is done it runs the full comparison once more and removes the file only if
  that finds nothing. If something does stand in the way (a held variant in the cohort, say), the file stays, its
  reason becomes `MISMATCH` at the draw concerned, and the job says so: a catch-up never clears a real mismatch.
- Nothing recomputes stored results by itself. The check is exhaustive, not a sample. Its cost is unmeasured
  (section 20); if it proves too slow to run at every job, it runs at every install and copy instead, which sets the
  same file.

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
| Start | The tree's own checks (section 15); one job lock; the "backup due" flag; the status files' own checks (3.5); the lists read and any foreign list named (5.6A); the derived check (5.8) |
| Fill | With results on file through draw M: every missing target up to M, for every variant not held and not withdrawn at that target, is forecast from the draws before it and scored, in draw order (5.7). Then every such variant without a line for M+1 is forecast for it. If the fill added anything, all of that game's reports are rebuilt (section 9), and every prevailing line still missing for a draw up to M is written, in draw order (10.4) |
| Results | **PROD:** the one reviewed Lotterywest-GOV updater is run through its own launcher, unchanged (owner, entry 130). **QA and DEV:** the accepted results are copied from PROD and checked to be the same file grown longer; neither ever contacts the lottery site. `--no-update` leaves the step out. The results on file now reach N |
| Catch-up | For each T from M+1 to N, in order: forecast lines for any variant lacking one; score lines; **the prevailing OV-1 line for T, if T is at or after the prevailing score's start** (section 10); the league report for T. Each draw is finished before the next begins |
| End | If the results step ran and succeeded in this job: every variant that has no eligibility draw in its status file, is not withdrawn, and has its history complete, gets one: N+1 (10.2). Every variant without a line for N+1 is forecast. The next-draw report is saved. The end-of-job backup |

- Fill and catch-up are one function. There is one forecasting engine and one scoring function, in every tree.
- **No clock rule exists.** The next draw is always attempted. The absence of a result on file is never treated as
  proof that the draw has not been made.
- **A results step that fails or is left out** changes nothing: N is M, no eligibility draw is written, the job says
  so and finishes. The next job catches up.
- **"The results step succeeded" is one rule in every tree.** What the step does is set by the tree's settings: the
  updater in PROD; the checked copy from the place the settings name in QA and DEV.
- **A results file that has changed other than by growing** refuses that game and names the draw. What to recompute
  is then a reviewed decision.
- A catch-up of no draws is normal. An interrupted job is continued by the same command.
- `--only <family>/<variant>` limits a job to named variants. In DEV the job writes DEV's own research results.

**7.2 Examples** (results on file through 1600 at the start).
- *An install, no backlog.* V41 is new. Fill: V41 from its first target to 1600; the forty others nothing. Reports
  rebuilt with V41 in them. V41 forecast for 1601; the others' forecasts for 1601 untouched. Results: nothing new.
  End: V41's status file gets `prevailing_ov1_first_eligible_draw = 1601`. The next week: 1601 arrives; 41 forecasts
  scored; the prevailing line for 1601 counts 41 variants; `league_..._d01601` saved; 1602 forecast.
- *An install with six draws waiting.* Fill as above. Results: 1601 to 1606 arrive. Catch-up, six times over: forecast
  (the forty reuse their 1601; V41 reuses the one just made), score, prevailing line, league report. Six reports.
  V41's eligibility draw is 1607: its results for 1601 to 1606 are in every report and in the exploratory OV-1, not in
  the prevailing one. The forty counted at all six.
- *The very first job of a new tree.* Every variant fills its whole history. Results bring 1601 to 1606: forecast,
  scored and reported, **with no prevailing line, because no variant has an eligibility draw yet.** End: every
  variant's eligibility draw is 1607, which is therefore the prevailing score's start.
- *The first job with the updater failing.* History filled; 1601 forecast; no eligibility draw; the report says
  "prevailing OV-1: not started; waiting for a successful results step". Nothing provisional is published.
- *QA as PROD's mirror.* QA's software was replaced from PROD and its research data reseeded from PROD. V1's status
  file in QA says eligible from 1601, as in PROD. QA's later jobs copy results through 1700 from PROD. V1's eligibility
  draw stays 1601: the job writes one only where none exists (10.2). QA's prevailing ledger equals PROD's, line for
  line, unless the environments differ.

## 7A. The historical walk-forward rerun (owner, entries 128, 135, 136, 137, 143; EX_267 R6-F03)

**7A.1 What it is.** The owner's command to compute again draws that are already computed, in the one tree he runs it
in: to try a corrected or changed method or infrastructure in QA or DEV, to rebuild derived results after a
correction, to recompute the variants a corrected shared file affects (12.8), or, in PROD, as a last resort. It is
the same walk-forward as every other run: same engine, same N-1 rule, same status files. It is never started by an
install, a correction, a copy, a job or a schedule.

**7A.2 The command and its two modes.**

    Rerun_Walk_Forward.bat --game <POWERBALL|OZLOTTO|BOTH> [--from J] [--to N] [--only <family>/<variant> ...]
    Rerun_Walk_Forward.bat --game <POWERBALL|OZLOTTO|BOTH> [--from J] --derived-only

Without `--from`, the whole history. **What each mode may change, and nothing else:**

| | Forecast rerun | Derived-only rerun |
|---|---|---|
| Purpose | forecasts are computed again | scores and OV-1 are computed again from the forecasts as they stand |
| A method runs | yes | **never** |
| Forecast lists | of the selected variants only (all, without `--only`): lines from J on are replaced | **not one byte of any forecast list changes;** every forecast keeps its first-written line and envelope |
| Score lists | of the selected variants: lines from J on are replaced | of every variant: lines from J on are replaced |
| The prevailing ledger | lines from J on are replaced | lines from J on are replaced |
| Reports and the exploratory OV-1 | made again from J on | made again from J on |
| Status files | **never touched** | **never touched** |
| Foreign lists | one within the selection is archived, removed, and its variant computed afresh; others stay foreign | untouched; they stay foreign and their variants held |
| `--only`, `--to` | allowed | **refused:** it is cheap, so it always covers the whole game to the last draw on file |

- **`--only` still rebuilds everything that depends on those variants:** the league reports of the game, the
  exploratory OV-1 and the prevailing ledger from the earliest affected draw, for all variants.
- **`--to N`** stops the recomputation after draw N. **Said plainly before the confirmation:** "everything from J on is
  archived; draws J to N are computed now; draws after N are left for the next `Run_Research.bat`, which will compute
  them as an ordinary catch-up. Until then this game's results are not current from draw N+1." The cutoff file of
  5.8 is left saying N+1 with the reason `AWAITING_CATCH_UP`, so nothing after N looks current; the next ordinary job
  catches up from N+1 and removes the file when everything to the last draw is complete and agrees (5.8).

**7A.3 Everything that depends on the recomputed draws is rebuilt, always** (owner, entry 135). No report or OV-1 line
computed from the old lines is left standing as if complete. The status files are never touched: withdrawals and
eligibility draws are the same after a rerun as before it, so the cohort at every draw is the same, and a rerun is
never a way to bring a withdrawn variant back or to give a variant a new eligibility draw.

**7A.4 Before anything is replaced, it is saved in one verified, clearly named ZIP (owner, entry 142).** The rerun
first writes, into `results/research_set_aside/`, one ordinary ZIP **for each game it covers** (a rerun of both games
writes two, so neither game can look absent), of every file of that game it is about to change, whole:

    <ROLE>_<GAME>_<RERUN|CORRECTION>_ARCHIVE_<YYYYMMDD>_<HHMMSS>_<what>_BEFORE_RECOMPUTE.zip
    for example  PROD_POWERBALL_CORRECTION_ARCHIVE_20270105_194200_recurrence_gaps_v1_BEFORE_RECOMPUTE.zip

It holds the forecast and score lists the mode will change (a derived-only rerun archives the score lists, not the
forecast lists it leaves alone), the prevailing ledger, the reports and OV-1 print-outs of the game, and a readable
`ARCHIVE_CONTENTS.txt`: the tree, the game, the variants, each file's path and SHA-256, the command and scope the owner
confirmed, his stated reason, and the identities of the software before and after. It is read back and every member
checked against that list. **If it cannot be written or does not verify, the rerun stops and no active file has been
touched.** It says in its own first line that it is not a backup of the tree and cannot restore one. Nothing in the
system reads it again; it travels in every backup; nothing prunes it. In QA and DEV the owner may delete such ZIPs by
hand. **A forecast first made before its result was known keeps that property, in the archive;** it is the line
computed in its place that is retrospective.

**7A.5 The steps.** (1) The process checks; the job lock, held to the end. (2) The scope is shown: the mode; exactly
which lists will be replaced and which will not; what will be rebuilt; 7A.2's sentence where `--to` is used; and, in
a forecast rerun, how many forecasts first made before their results were known will be replaced. (3) **One
confirmation: the owner types the tree's role** (`QA`, `DEV` or `PROD`); anything else is no. In PROD the text first
says: "This is PROD. Lines written when their results were unknown will be replaced by lines computed now, with the
results known. The first-written lines are kept in the archive ZIP named below and in your existing backups. This
cannot be undone except by a restore from backup." (4) A barrier file holding the scope; while it exists every
launcher of the tree refuses, except this command with the same scope. (5) The archive of 7A.4, written and
verified; its name and SHA-256 are then written into the barrier file,
with the stage `ARCHIVED`. **A rerun that is continued never makes the
archive again:** it finds the name in the barrier, checks that ZIP still verifies, and goes on, so records already
shortened are never archived in place of the first-written ones. (6) The cutoff file of 5.8 is set to J. Then the lists the mode may change are each rewritten to end
before J, the prevailing ledger likewise, and the reports from J on are removed; when all of that is done the barrier's stage becomes
`SHORTENED`. **Step 6 is carried out only while the stage is `ARCHIVED`** (EX_269 R7-F03): shortening a list that already
ends before J changes nothing, and nothing is computed until the stage is `SHORTENED`, so a crash inside step 6 is
repaired by doing it again; once the stage is `SHORTENED` no list is ever shortened again. (7) The ordinary fill computes what
is now missing (no method, in a derived-only rerun), to N or to the last draw on file; then the prevailing lines
and the reports, draw by draw. (8) The cutoff file is removed, or moved to N+1 where `--to` was used; the barrier is
removed; the end-of-job backup is attempted. **Interrupted at any point:** the barrier keeps every job out and the
cutoff file says nothing from J on is current; the same command again continues: the archive is verified and
recorded before step 6 and is reused; step 6 is never repeated once its stage is recorded, so lines already
computed again are never cut a second time; and step 7 computes only what is missing. The barrier is removed only
when every dependent result agrees and the cutoff file is in its final state.

**7A.6 The truth about what a rerun produces** (owner, entry 136; the reviewer, entries 137, 142). Every line a rerun
writes carries, in its envelope, that its result was on file when it was computed, and the rerun's name. So, in
every tree, a rerun's results are retrospective and are shown as that: the league report's column of forecasts made
before the result was known falls accordingly, and the prevailing report says how many of its draws were computed
again, when, and in which archive the first-written lines are (10.6). Nothing else about OV-1 changes: the same
mathematics, the same conditional claim, the same words in every tree.

**7A.7 Examples.**
- *A corrected OV-1 in QA (derived-only).* QA mirrors PROD. The owner installs corrected OV-1 code into QA with
  `Reinstall_Infra.bat QA`, having been told it changes OV-1 lines from draw 1612. QA's results are not current from
  1612. `Rerun_Walk_Forward.bat --game POWERBALL --from 1612 --derived-only`: the score lists, the ledger and the
  reports go into the archive; scores and ledger are rebuilt from the stored forecasts; **every forecast line,
  including those first made before their results, is byte for byte as it was.** He compares QA's new figures with
  the archived ones and with PROD's. Nothing in PROD has changed.
- *A draw range across a withdrawal.* V1 is withdrawn from 1601. `--from 1550 --to 1650`: V1 is recomputed for 1550 to
  1600 and for nothing after; every other variant for 1550 to 1650; reports and both OV-1 records for 1550 to 1650
  are rebuilt with V1 absent from 1601 on; the game is not current from 1651 until the next ordinary job.
- *One variant after a reseeding.* QA holds its own experimental `E_002/RECUR_MEAN_ALL_V1` (other bytes than PROD's
  variant of that name). After a reseeding, PROD's list for that name is foreign and the variant is held.
  `--only E_002/RECUR_MEAN_ALL_V1`: PROD's list is archived; QA's variant is computed over its whole history; every
  report and both OV-1 records of the game are rebuilt with it; no other variant's forecast list changes.
- *PROD, the last resort.* A scoring fault is corrected, proved in QA as in the first example, and installed into
  PROD. The owner runs the derived-only rerun in PROD, types `PROD`, and the prevailing report thereafter says which
  draws were computed again and in which archive the first lines are.

## 8. Scoring

One function, for both games, from R3 section 3 and the game profiles: for each barrel, how many of the numbers drawn
are in the TOP set and how many in the WORST set (Powerball: the main barrel of 35 and the Powerball barrel; Oz Lotto:
the main barrel of 47, with the supplementary numbers used for the prize divisions only, never for forecasting); and
the prize division each ticket would have won. A forecast is scored at most once, when its target's result is on file, and
never if its variant is withdrawn from that draw (section 11).

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
  how many of its forecasts were made with the result not yet on file; its first draw in the prevailing OV-1; its
  `NO_FORECAST` counts by reason; "WITHDRAWN from draw T: <reason>" where its status file says so, with any forecast it
  held for T shown as "not scored: withdrawn". Ordered by TOP hits above chance a draw, ties by identity, with the
  WORST order beside it. Header: "A descriptive order. It selects nothing."
- **Reports are derived and replaceable** (owner). They are a function of the lists, the results and the status files
  alone. When a fill or a rerun adds or changes history, every league report of that game from the earliest affected
  draw and the exploratory OV-1 are rebuilt with the whole current population; otherwise a job adds only the new
  draw's files. **They are also all made again whenever the code that makes them is changed** (12.4), so that no file
  made by old report code is left in the active folder (EX_269 R7-F02). Earlier editions are not kept in the tree; each backup holds the editions of its day.
- **Every file says** which tree made it (role and root), what draw it runs to, how many variants it holds, when it
  was made, which foreign lists were ignored (5.6A), and, where it applies: "rebuilt with the current population: a
  variant's figures at draws before its installation were computed afterwards; this is not a table published at that
  draw's date".
- The same lists, results and status files give the same report bytes (the time of making is in a side file).
- R3's fuller measures (section 17 of R3) are available as a further report over the same files, on request.

## 10. OV-1 (owner: two uses; EX_257 F01; EX_261 P05, F03; entries 130, 135, 136, 137)

**10.1 Unchanged:** the mathematics and the kernel named in 1.2; one score per game; the bar of 40; a factor of
exactly 1 when no variant has a counted pair or V is zero. The same code and rules run in every tree.

**10.2 `prevailing_ov1_first_eligible_draw`: when a variant begins to count in the prevailing score** (the owner's
choice B, entry 130; named so that it says what it controls, entry 135). It is a draw number in the variant's status
file (3.5). It stops nothing else: the variant's whole history is still forecast and scored, and counts in every
league report and in the exploratory score.
- **How it is set:** by the research job, at the end of the first job in that tree in which the variant's history is
  complete and the results step ran and succeeded: the last draw then on file, plus one.
- **It is set once and never changed** (the reviewer's qualification, entry 137). The job writes it only where the
  status file has none. A value that arrived with PROD's software in a QA software replacement is PROD's value and
  stays: PROD's 1601 does not become 1701 because QA received results later.
- **What it means, and no more:** the first draw **not present in the accepted results on file after a successful
  results step.** It does not prove the draw had not been made, or that its result could not be known some other way.
- It differs from "the last draw on file at installation, plus one" only when the results step then finds draws
  already made; those are exactly the draws that must not count for a variant installed after them.
- No date, clock or choice enters it. A restore keeps the values the backup holds.

**10.3 The start.** The prevailing score of a game starts at the smallest eligibility draw among the variants
installed in the tree. Before any variant has one there is no prevailing score, and draws caught up before the start
are scored and reported as research only.

**10.4 One line per draw from the start,** in order (`results/research/<GAME>/ov1/prevailing.jsonl`). The research job
only appends to it.
- **The cohort as of T,** read from the status files: every installed variant whose eligibility draw is at or below T
  and which is not withdrawn from a draw at or below T.
- The line is written when every cohort member has its `TARGET` line for T and, if that is a forecast, its score.
  Until then the line is **blocked** (an operational wait, named with the variant that causes it), never skipped. A
  cohort member that is held (5.6A) blocks in the same way.
- Each cohort member is recorded as *counted* (a complete TOP and WORST pair) or *no pair*, with the reason
  (`INSUFFICIENT_HISTORY`, `METHOD_FAILED`). The weights come from the counted pairs only.
- The line also holds: how many counted forecasts were made with the result not yet on file; the weights; V; X
  (derived from the weights and from the score lines, which must agree); Z; the six log-factors and running sums;
  the digest of the OV-1 code; the rerun's name if a rerun wrote it.
- **The stored ledger must equal its rebuild** from the lists, the results and the status files (5.8). Blocked or
  withheld until settled, never stopped; never started afresh by a job; no second stream.

**10.5 The exploratory score** is the same kernel over every draw that has any scored pair, counting every variant
wherever it has one. It is rebuilt with the league reports. Every file is headed: "OV-1 EXPLORATORY RETROSPECTIVE - not
the prevailing score; no error bound applies; 40 is a reference line only".

**10.6 The claim, as the prevailing report prints it in every tree** (F01, F03):

> "If this game's draws are fair, and if nothing that decided a draw's forecasts or which variants counted at it was
> influenced by that draw's result (that includes what code was installed, corrected or withdrawn and when, which
> backup was restored, and any rerun), the chance that this score ever reaches 40 is at most 2.5%. The software
> checks that each forecast was computed from earlier draws only, that the variants counted are those fixed by draw
> number, and that every draw is taken once. It cannot check the second 'if'."

Beside it, as plain counts taken from the envelopes: the tree that made the report; draws counted; counted forecasts
made before and after the result was on file; draws whose lines were written by a historical walk-forward rerun,
with each rerun's date and its archive ZIP; where the counted forecasts were computed (for example "PROD 812;
QA 0"); lines with a "no pair" member, and the first such draw. There is no SUPPORTED, QUALIFIED or sandbox label:
the counts say what kind of evidence the score is, in the same words whichever tree prints them.

**10.7 After a restore** the lists, the ledger and the status files are the backup's and the job continues them.
Nothing is marked for the restore. The score may differ from the one that was lost; that is a truthful result.

**10.8 After a QA software replacement or a reseeding,** nothing special is computed. The ordinary rules decide: lists
that are foreign are ignored (5.6A); a stored ledger that no longer equals its rebuild is withheld (5.8); the owner
settles either by the operation he chooses. When QA has PROD's software, status files and research data, none of
these arises and QA's score is PROD's.

## 11. Withdrawing a defective variant (owner; EX_261 F02; EX_264 R5-F01, N01; entries 130, 136, 137)

- **What it is:** the owner's explicit decision that a variant is wrong and stops. It is never automatic and never a
  judgement of performance. The corrected method is a new variant, installed in the ordinary way.
- **How:** `Withdraw_Variant.bat <family> <variant> --game <game|BOTH> --reason "<text>"`, in the tree concerned. It
  shows the variant, the last draw on file and when the results were last checked, and the draw the withdrawal will
  take effect from: **the last draw on file plus one.** The owner types one confirmation. **From before the draw is shown until the status file is written, the
  command holds the tree's job lock and the updater's own lock,** so that no job and no results step can run in
  between; under those locks it reads the last draw on file again and refuses if it is no longer the one it showed
  (EX_267 R6-F07). It then rewrites that
  variant's status file with `status = WITHDRAWN`, the draw and the reason (3.5), and adds one line to the tree's
  log. That is the whole mechanism: no registry, no status table, nothing written into any list. Several variants
  can be named in one command, under one confirmation.
- **What the effective draw does and does not assure (N01).** It is fixed from the results on file, not from the
  calendar. If a draw has been made but not yet fetched, the withdrawal takes effect at that draw. The command says
  so and suggests running the research job first; it makes no fresh check itself and applies no clock rule. The
  claim of 10.6 already names withdrawals among the things that must not depend on a result.
- **From that draw:** no forecast is computed; no score is ever written, **including for a forecast the variant already
  holds for that draw, which stays in its list as history, unscored** (5.6, 5.7); the variant is not in the prevailing
  cohort.
- **Nothing is removed or rewritten:** its code stays installed; its lines stay; the prevailing lines already written
  stay; every league report still shows it over the draws it was scored for, marked withdrawn; the exploratory score
  still uses its scored draws.
- **It is one-way (owner, entry 137).** No command reinstates a withdrawn variant. The method comes back only as a new
  variant, or by a restore from a backup made before the withdrawal: that backup's status file says `ACTIVE`, the
  variant runs again in the catch-up, and nothing withdraws it again by itself.
- **It is the state of one tree, and it travels with the software.** The QA software replacement brings PROD's
  withdrawals into QA with PROD's variants; a research-data reseeding changes no status file. **In DEV the owner
  removes the withdrawn variant's marker** (`Make_Installable.bat --unmark`), so that no tree created later receives
  it.
- **Every tree applies it identically** (owner, entry 136): a catch-up or a rerun in QA or DEV treats a variant
  withdrawn from 1601 exactly as PROD does.

## 12. Installing (owner; EX_262 F08, F10; EX_264 R5-F02 to R5-F05; entries 126, 127, 135, 136)

**12.1 Two kinds of install from DEV, never mixed.**
- **`Install.bat PROD` (or `QA`): new variants only.** It finds every ready variant in DEV (section 4) that the target
  does not hold, shows the exact batch (variants, helper files, and what it left out and why), and adds those folders
  and any helper files that are new, creating each new variant's status file as `ACTIVE`. `--only` narrows the
  batch. It never overwrites: a variant the target already holds is left alone even if DEV's copy has changed
  (changed science is a new variant), and a helper the target holds with different bytes is a refusal. Nothing to
  add ends at once, with the target untouched. The owner types **one** confirmation for the whole batch; nothing is
  confirmed per variant or activated afterwards.
- **`Reinstall_Infra.bat PROD` (or `QA`): infrastructure only** (12.4).

**12.2 What an install requires: the readiness marker, and nothing from QA (owner, entry 126).** A variant is installed
into PROD on the strength of its marker in DEV. There is no QA pass record, no comparison of PROD with QA, and no
required order between them. QA and PROD are each installed from DEV. What still protects PROD, with no ceremony: the
marker is bound to the files' content; installed scientific files are never overwritten by an install; the install
checks itself in the tree it installs into (12.3); one confirmation. **Infrastructure has a marker of the same
kind:** `deploy\INFRA_IS_INSTALLABLE.json`, made by `Make_Installable.bat INFRA` (owner, entry 127).

**12.3 What every install checks by itself, in the tree it installs into** (QA and PROD alike; the same code).
1. **The structure:** markers match; declarations valid; no undeclared file; the import check; add-only kept; every
   status file passes its own check.
2. **Each NEW variant is made to forecast once, for each game it supports, before the install is finished**
   (R5-F03). The smoke case builds an invented results table for the game from a fixed seed, long enough for the
   variant's declared minimum history, and runs the variant through the ordinary engine (the N-1 view, the method,
   the readout and its validation) with the target's own Python. **It passes only on a complete `FORECAST`:** a full
   ranking and valid TOP and WORST sets for every barrel. `INSUFFICIENT_HISTORY` or `METHOD_FAILED` is a failure of
   the smoke case. It reads no real draw, and writes only under `<tree>\scratch\`, never a list, a report or an OV-1
   line; the scratch files are removed on success and left, named, on failure. **What it shows and does not:** that
   this variant computes a legal forecast here. It says nothing about whether the mathematics is right.
3. **The test suite, when it is the suite of the software being checked.** The tests live in DEV and belong to DEV's
   infrastructure. They are run, with the target's Python on a temporary copy, only when the target's installed
   infrastructure is file for file DEV's (always true at a tree's creation and after an infrastructure reinstall).
   When DEV's infrastructure has moved on, the tool says "the tests in DEV are for newer code than this tree holds;
   not run" and relies on the checks that travel with the installed software: 2, 4 and 5.
4. **A fixed sample of stored forecasts** of variants already installed is recomputed and must be identical in
   content. It is a sample: it can show a fault, it cannot show there is none.
5. **The derived results, in full** (5.8): every score and the whole prevailing ledger, recomputed and compared by
   their scientific content. **An unexpected difference is a fault and stops the install.** There is one expected
   case, and it is not this check failing: an infrastructure reinstall that the owner accepted after being told,
   before anything was overwritten, that it changes derived results from draw X (12.4). There the tool reports the
   difference as what was accepted, and checks instead that the tree now shows those results as not current from X
   (5.8). It never reports "all stored values agree" when they do not (EX_267 R6-F06).
A failure stops the install with its barrier in place, so no job runs. The ways out are the same command after the
cause is corrected, or a restore from a verified backup of the owner's choosing. **The tool names the backup it took
just before only if that backup was in fact made and verified** (R5-F04).

**12.4 Infrastructure** (owner: REINSTALL INFRA; EX_264 R5-F04, R5-F05, N03).
- **What it is:** the files named in `deploy/INFRA_MANIFEST.ini` (the owner's name for it; first written with the phase
  2 package and reviewed there; afterwards edited by hand to add or remove a line). Nothing is infrastructure unless
  it is on the list. **Not on it, and never installed outside DEV:** documents, the exchange, tests, Git files,
  unmarked variants, DEV's results, the settings files, and the proof-of-concept coordinator and probes.
- **Its syntax, read by Python's standard INI reader and nothing else** (N03): under `[files]`, one line a file,
  `<path from the tree root, forward slashes, no spaces> = <class>`. Under `[install_tool]`, the DEV-side tool's own
  files in the same form. The reader is used with `=` as the only separator, names taken exactly as written, no
  value substitution and duplicates refused. A line that is not of that form, a path given twice, a path that does
  not exist, or a class that is not one of the three, refuses.
- **The class says what a file can change:** `forecast` (it can change a forecast: the reader and views, the seeds,
  the engine that calls a method, the readout, ranking and ties); `derived` (it can change a score, a league report
  or an OV-1 line, but not a forecast: scoring, the lists' code, reports, the OV-1 kernel and ledger); `other`
  (neither: launchers, the guard, backup and restore, the owner's environment scripts). A test in the suite follows
  the imports: every project file the forecasting entry point imports must be `forecast`, and every file the scoring,
  report and OV-1 entry points import must be `forecast` or `derived`. So a wrong class is caught by a test, not
  trusted. **A class is a careful label, not a proof** (EX_267 N01): a file whose effect on forecasts cannot be ruled out
  is classed `forecast`, and a planted dependency from an `other` file into the forecasting path must fail the test.
- **The identity of the forecasting code** is one SHA-256 over the `forecast`-class files, computed as a variant's
  fingerprint is (3.4). Every list's header records it (5.2). So a list always says which shared forecasting code
  it was made under, and a list made under other code than is installed is foreign (5.6A). **It identifies this project's source
  code and nothing more** (EX_269 R7-N03): it proves no numerical equivalence across a changed Python or library,
  which the environment digest in each line and W-23 cover (section 13).
- `Reinstall_Infra.bat` shows every file it would add, overwrite or remove, with both hashes, its class and the
  differences, and touches nothing under a family folder or `_shared/`.
- **It never changes forecasting code** (EX_267 R6-F01). A plan that would add, overwrite or remove any `forecast`-class
  file is refused by this command, which says: "this changes code that makes forecasts; that is a correction of
  shared code: `Correct_Shared_Code.bat`" (12.8).
- **What it checks before it overwrites anything** (R5-F05; there is no recomputation of the whole history). On a
  temporary copy of the software as it would be, with the target's Python and the target's own data, read only:
  the suite; the derived results **in full** (12.3, 5); and the fixed sample of forecasts (12.3, 4). The result is
  shown as one of two plain statements:
  - "No stored result changes." (Nothing differed.)
  - "**This changes stored scores or OV-1 lines,** for <game> from draw X. It is a scientific correction to derived
    results. Stored forecasts are not affected. If you install it, <game>'s scores, reports and prevailing line will
    be not current from draw X until you run the derived-only rerun." (Exhaustive: every such change is found.)
  **A difference in the forecast sample here is a fault,** since no forecasting code is in the plan: a file is
  wrongly classed. The reinstall stops and names the forecasts that differ.
- **A correction to scoring, reports or OV-1 is installable, plainly stated, and is never hidden as maintenance**
  (EX_267 R6-F01 case A, R6-F06). The owner sees the second statement before the question and may say yes. Stored
  forecasts are untouched; the derived results are not current from X (5.8) until he runs the derived-only rerun
  (7A). Nothing is recomputed by the install. Trying it in QA first costs PROD nothing, and is what QA is for; it
  is never required.
- **The print-outs are made again when their code changes** (EX_269 R7-F02). If the plan holds any `derived`-class
  file and the stored results agree, the reinstall ends by making every league report, next-draw report and OV-1
  print-out of both games again with the new code, before it removes its barrier. If the results do not agree, the
  cutoff file and the move of stale reports (5.8) do the same duty until the derived-only rerun.
- **`Check_Forecasts.bat`** recomputes stored forecasts with the installed software and environment and compares
  their content. `--sample` is what the installs run; `--all`, or a game, a draw range or named variants, is the
  owner's to run in any tree. It can be stopped and continued. It writes a report under `scratch\` and nothing else.
- **The backup and the confirmation** (owner, entries 135, 136; this replaces the refusal of entry 128). An
  infrastructure reinstall overwrites files. In this order: the plan and the statement above are shown; the recovery
  kit is written; **the usual whole-tree backup is attempted and its result reported truthfully** (made and verified,
  with its name; or NOT made, with the reason); then one warning and one confirmation. **The tool does not look for,
  count or verify earlier backups, and a missing backup or kit is not a refusal.** The warning, in substance:

  > "This overwrites installed system files in <role> <root>. Make sure you hold a valid backup. If the overwrite
  > fails, the way back is a manual restore of the whole tree from a backup you choose: there is no automatic
  > rollback. A restore puts back exactly that backup: its software, variants, status files, results and Python
  > environment. Anything installed, withdrawn or upgraded after it is not put back; you then run the research job to
  > catch up. If Python, the environment or its packages have changed since that backup, the restored tree may not
  > run, or may not give identical results. With no valid backup, recovery may not be possible. [The backup just
  > attempted: <result>.] [The recovery kit: <result>.] Proceed? Type YES to proceed. Anything else, Enter included,
  > is NO."

  NO overwrites nothing; the backup and the kit just attempted may by then exist, and are logged (EX_267 N03). YES
  proceeds, whatever the backup's result: the risk is the owner's informed choice. The same
  text and rule apply in QA: it is the same software.
- A variant install (12.1) adds files and overwrites none. It attempts the same backup and writes the same kit, and
  reports each truthfully; a failed kit is put in its confirmation ("the recovery kit could not be written: <reason>";
  default NO) and no longer stops the install (owner, entry 136).

**12.5 Creating a tree: `Init_Tree.bat QA|PROD`.** For a root that does not exist or is empty. It writes the tree's
`ENVIRONMENT.ini`; installs the infrastructure and every ready variant, each with a new status file; copies the
accepted results (QA: from PROD, or from DEV while no PROD exists; PROD: from DEV, the first time); stops for the
owner to build the environment with his scripts; verifies it; takes the first backup. Creating a tree copies no
forecast, score, report or OV-1 record; a reseeding (14.2) is a separate, later act of the owner's.

**12.6 Installation is release** (owner). The next research job finds the new variants and fills their history.

**12.7 The QA software replacement from PROD (owner, entries 135, 136).** `Replace_QA_Software_From_PROD.bat`, run from
DEV, on the owner's own command. It makes QA's installed software exactly PROD's: PROD's infrastructure, PROD's
variants and helpers, and **each variant's status file as PROD holds it** (so PROD's withdrawals and eligibility draws
arrive with PROD's variants). Whatever software QA held that PROD does not is removed: this is a wipe and a
replacement, not a merge, and it exists only for QA.
- **PROD is read, never written:** no program of this project writes a log, lock, marker or any byte there, and nothing
  of PROD's is started. **Every file read from PROD, each variant's status file included, is hashed at a first
  reading and again at a second;** any difference, a status file changed by a withdrawal among them, refuses the
  replacement (EX_267 R6-F04). Those hashes are kept in the tool's memory and in QA, never in PROD. (Windows may
  itself record a file's last-access time when it is read; that is the operating system's, and is outside this
  promise: section 20.)
- **QA is reserved first:** the tool takes QA's job lock before it reads PROD and holds it to the end, so that no QA
  job can start in between (EX_267 R6-F05).
- **QA keeps what makes it QA:** its `ENVIRONMENT.ini`, its `.venv`, its backup root, its own records and logs. Nothing
  of PROD's settings, environment, records, locks or backups is copied.
- **No list or ledger is copied or changed.** QA's lists and ledgers stay as they were. **Before the tool finishes, and
  before its barrier is removed, it applies the ordinary rules itself with the software now installed** (EX_269
  R7-F02): it names the lists that are now foreign (5.6A); it runs the derived check (5.8); and where QA's results
  are no longer current it writes the cutoff file and moves the stale report files out of the active folder. So QA
  never comes back from this command with a report in view that the installed software and status would not have
  produced. The tool says this before the confirmation, and names the two things that settle it: a reseeding, or a
  rerun.
- **QA's own environment must run PROD's software.** After the replacement every variant's smoke case (12.3, 2) is run
  with QA's Python. If any fails, QA's environment marker is removed, so that every QA launcher refuses until the
  owner rebuilds the environment and runs `Verify_Tree.bat QA`. PROD's `.venv` is never copied, and identical results
  are not promised across different environments.
- **A half-done replacement never looks finished:** the install barrier is in place from before the first change
  until after the last check; the same command again does the whole replacement afresh.
The steps are in the deployment design (section 6A). It is never run for DEV or PROD, and it is no part of any
install into PROD.

**12.8 Correcting defective shared code in place (owner, entries 141 to 143; EX_267 R6-F01).**
`Correct_Shared_Code.bat PROD` (or `QA`) `--reason "<the defect>"`, run from DEV, on the owner's own command.
- **What it is for:** shared code that does not compute what was always intended. **Shared code** is: the
  `forecast`-class infrastructure files (12.4); a helper under `_shared/`; a helper in a family folder. It is never
  for a variant's own files (a corrected method is a new variant) and never for a changed idea (3.3A). Which of the
  two a change is, is the owner's judgement, given in one line of reason; nothing else is asked of him.
- **What it changes in the target:** exactly the shared files that differ between DEV and the target: `forecast`-class
  files as the infrastructure marker lists them, and helpers the target holds with other bytes than DEV's. DEV's
  markers must match (the variants that use a corrected helper are marked again in DEV, since their fingerprints
  have changed). Nothing under a variant folder is written, and no status file.
- **Which variants it affects, taken widely** (the reviewer, entry 142): for a helper, every installed variant whose
  declaration lists it (3.4: a variant's list is its whole dependency, so this is a look-up, not an analysis); for a
  `forecast`-class file, every installed variant, in both games. The plan shows them by name. The fixed sample of
  forecasts is shown as information only: a sample that happens to match excuses no variant.
- **Its own question, never the install question:** after the plan, the kit and the backup attempt (reported as
  always), the text says: "This is a CORRECTION OF SHARED CODE in <role> <root>: <reason>. These <n> variants will be
  HELD: nothing of them will be forecast, scored or counted until you run the historical walk-forward rerun for
  them, over their whole history. <game>'s results will be not current from draw <first> until then. Forecasts
  already made stay exactly as they are until that rerun archives them. Type CORRECT <role> to proceed." Anything
  else is no.
- **How the hold comes about, with nothing new:** the corrected helper changes the fingerprint of each variant that
  lists it, and corrected forecasting code changes the forecasting-code identity; either way the affected variants'
  lists no longer match their headers, so they are foreign and their variants held (5.6A), in every later job,
  until the rerun. The tool writes the cutoff file of 5.8 at the affected variants' earliest first draw. **No list
  made under the old code is ever appended to under the new:** one name is one forecaster in the active record.
- **The code being replaced is kept** (the reviewer, entry 144). Before any file is overwritten, the old bytes of every
  file in the plan are saved in one small verified ZIP beside the reruns' archives
  (`<ROLE>_CORRECTED_CODE_<date>_<time>_BEFORE_CORRECTION.zip`, with the reason and each file's SHA-256). If it cannot
  be written or does not verify, nothing is overwritten. The rerun's own archive, made later, holds the old results;
  this one holds the old code that made them.
- **Then the owner runs the rerun** (7A), for those variants or for all, when he chooses: it archives what it replaces
  (7A.4) and computes the affected variants' whole history; unaffected variants' forecasts are kept as they are;
  every report and both OV-1 records of the game are rebuilt. The correction never starts the rerun itself.
- **What it never does:** change a status file (withdrawals and eligibility draws stand; a correction is not a way to
  bring back a withdrawn variant or to give anything a new eligibility draw); touch a list; run in PROD without
  `PROD` typed in its question; or run half-way: it uses the install barrier, so that a tree with some files
  corrected and others not is never runnable. The same command again finishes it.
- **In DEV** nothing is installed: editing a helper or a forecasting file there has the same effect by the same rule
  (the lists made under the old bytes become foreign), and the rerun clears it.
The steps are in the deployment design (section 6C).

## 13. The Python environment

- Each tree's `.venv` is built by the owner with his own scripts, in that tree. It is not pinned to a draw (owner): a
  draw computed late runs in whatever environment the tree then holds, and its digest is in the line's envelope.
- **Verified before use.** `Verify_Tree.bat QA|PROD` runs the checks of 12.3 (items 1, 3, 4 and 5, and every installed
  variant's smoke case) with that tree's Python and, on success, writes `.venv\ENVIRONMENT_VERIFIED.json` with the
  environment's digest. Launchers refuse without it; each job compares the digest at its start; the owner's install
  script removes the marker before changing anything.
- **The digest does not include its own marker** (R5-F02). It is taken over a fixed inventory: `pyvenv.cfg`; every file
  under `Scripts\`; every file under `Lib\site-packages\` except `__pycache__` folders and `.pyc` files; and the base
  Python's version and executable. The marker lies beside `pyvenv.cfg`, outside all of these, so writing it changes
  nothing that is hashed, and a second unchanged launch finds the same digest.
- The fixed sample of forecasts is recomputed and any difference **reported**. After an environment change such
  differences are information for the review below; they do not by themselves refuse. A variant that can no longer
  produce a legal forecast (a failed smoke case) does refuse.
- **W-23 is unchanged** (owner). Every dependency upgrade: the reviewer's assessment and the owner's go first; DEV
  rebuilt and the evidence of H-1 5.4 produced; the reviewer sees it; then PROD: a backup,
  the rebuild, `Verify_Tree.bat PROD`. Rebuilding and verifying QA first is the owner's option.

## 14. Backups, restore, and the research-data reseeding (owner; EX_259 section 7; EX_261 P06; EX_265; entry 135)

**14.1 Backups and restore.**
- **A backup is one ordinary ZIP of a whole tree:** installed software with every status file, accepted results, lists,
  ledgers, reports, the archives that reruns have set aside, records, `ENVIRONMENT.ini` and the complete `.venv`. Only two temporary control
  files are left out. It is written to that tree's own backup root, checked twice (the archive read back; every
  source file read again), and called a backup only when both checks pass and the tree was quiet throughout.
- **When:** at the end of every research job and every rerun; before and after every install, infrastructure
  reinstall, QA software replacement and environment verification; at the end of a tree's creation; and whenever the
  owner runs `Run_Snapshot.bat`. Each is an attempt: its result is always stated truthfully.
- **If a backup cannot be made, the work goes on** with a standing warning until one is made (owner). A missing
  recovery kit is a warning and a default-NO confirmation, never a stop (owner, entry 136).
- **The recovery kit:** a small checked ZIP in the backup root for each software state, holding the restore tool and
  plain instructions. It needs only an installed Python: not DEV, not QA, not a working tree. It is not a backup.
- **Restore puts back exactly one chosen backup, at the path it came from** (owner). The old tree is renamed aside,
  never deleted. Nothing is installed, upgraded, rebuilt, withdrawn or brought back from anywhere else. No Python
  program may be running on the PC. Then the ordinary job catches up, with that backup's variants and status files.
  Any change after that is a separate decision by the owner. **Every rollback is this, done by hand by the owner from
  a backup he chooses** (owner, entry 128); nothing rolls back by itself.
- If the restored environment does not start, the restore says "RESTORED; ENVIRONMENT NOT READY" and the owner decides.
- QA has the same tools with its own roots. QA backups on QA's own drive are permitted, with a warning that they do
  not survive the loss of that drive.
- `Check_Tree.bat` lists, read-only, the full path, size and date of every backup ZIP in a tree's backup root. It
  verifies none of them, and nothing requires it (owner, entry 136).

**14.2 The research-data reseeding from PROD (owner; EX_265 section 1; entries 128, 129, 135).**
`Reseed_Research_Data_From_PROD.bat QA` (or `DEV`), run from DEV, on the owner's own command. It makes the
destination's research data exactly PROD's.
- **What is copied, complete:** the accepted results with their version ledgers, verification and provenance records;
  every forecast and score list; the league and next-draw reports; both OV-1 records. **What is not:** any software or
  status file, `.venv`, `ENVIRONMENT.ini`, records, logs, locks, set-aside archives or backups.
- **PROD is read, never written, whatever happens:** no lock, marker, log, flag or any byte, on success, failure or
  interruption. No PROD program is started. (The promise is that no program of this project writes to PROD;
  Windows may itself record a last-access time when a file is read: section 20.) With no lock allowed, PROD's stillness is established by reading: the
  tool refuses if PROD shows a job, an install or a backup in progress; it hashes every file as it copies; then it
  reads and hashes all of them again; any difference means PROD changed meanwhile, and the copy is refused and
  discarded.
- **The destination's research data is wiped and replaced** (owner: no reference folder, no archive of what was
  there, no backup first). The printed summary shows what will go and what will arrive; the owner types one
  confirmation. A destination that is busy, or that is PROD, PROD's backup root or any other name for either, is
  refused.
- **The destination is reserved first:** the tool takes the destination's job lock before it reads PROD and holds it
  until it has finished, so that no job can start there and have its data removed under it (EX_267 R6-F05).
- **Never a half-copied mixture:** PROD's data is first copied into a temporary folder inside the destination and
  checked there; only then, behind a barrier file, is the old data removed and the new put in its place by renames.
  Stopped before the barrier: the destination is unchanged. Stopped after: every launcher refuses until the same
  command is run again.
- **It changes no software and no status file,** and it is not a way round either. Afterwards the ordinary rules
  decide what the destination's job may use: a list whose variant is not installed there, or is installed with other
  bytes, or disagrees with the local status file, is foreign: warned about, ignored, never counted (5.6A; owner: "warn
  about them, ignore them and continue"); derived results the local code would not have computed are
  not current (5.8). **The tool applies both before it finishes:** the cutoff file is written and stale report files
  are moved out before its barrier is removed.
  Every copied line still says it was computed in PROD (5.4).
- **To make QA a full mirror of PROD** the owner runs the software replacement (12.7) and this, separately. Neither
  starts the other.
- There is no separate export of PROD's data to any other folder (owner, entry 135), and nothing is copied to Git.

## 15. Safety rules kept

No program ends another process. Before a job, a rerun, an install, a copy, a backup or a restore the process rules
of the deployment design apply. An orphan marker blocks every launch until the owner's approved clearance. The three
safety switches stay False and the allowlist empty. Only the one reviewed updater contacts Lotterywest-GOV, only in
PROD; no AI chat and no other program contacts any lottery site. No program changes the PC's date, time or zone.
**Nothing run for QA or DEV, and no copy of any kind, ever writes a byte of PROD.** **Research data is never deleted in PROD by any program:** a rerun first saves the old lines in a verified archive ZIP in the tree, in every tree alike, and does nothing if
that archive cannot be made. Research data is deleted in exactly one case, a reseeding, and only in
its destination, which is never PROD. Installed software is removed in exactly one case, the QA software
replacement, and only in QA. A helper is overwritten in exactly one case, the correction of a defect (12.8). The only other removal of bytes is a torn last line (5.7).

## 16. The owner's commands, and what refusals mean

| Where | Command | Purpose |
|---|---|---|
| DEV | `Make_Installable.bat` | mark finished variants, or the infrastructure, ready; `--unmark` |
| DEV | `Who_Uses.bat`, `Make_Successors.bat` | find the variants that use a helper; prepare their successors |
| DEV | `Install.bat PROD` (or `QA`) | add new variants |
| DEV | `Reinstall_Infra.bat PROD` (or `QA`) | update infrastructure that makes no forecast |
| DEV | `Correct_Shared_Code.bat PROD` (or `QA`) | correct a fault in shared code in place; the affected variants are then held until the rerun |
| DEV | `Init_Tree.bat QA`, `PROD` | create a tree |
| DEV | `Check_Tree.bat QA` or `PROD` | read-only: what is installed, each variant's status, what is ready, any drift, the backup ZIPs, locks |
| DEV | `Replace_QA_Software_From_PROD.bat` | QA's installed software becomes PROD's |
| DEV | `Reseed_Research_Data_From_PROD.bat QA` (or `DEV`) | the destination's research data becomes PROD's |
| any tree | `Run_Research.bat` | the research job |
| any tree | `Rerun_Walk_Forward.bat` | the historical walk-forward rerun |
| any tree | `Check_Forecasts.bat` | read-only: stored forecasts recomputed and compared |
| any tree | `Withdraw_Variant.bat` | withdrawal |
| QA, PROD | `Verify_Tree.bat`, `Run_Snapshot.bat` | environment check; backup now |
| a kit | `Restore.bat --snapshot <zip>` | exact restore |

Every refusal prints one line saying what was found and one saying what to do. The main ones: "marker does not match
its files" (finish the work and run `Make_Installable.bat` again); "a file is not on the declaration's list"; "already
installed with different bytes" (changed work needs a new variant name); "an install did not finish" (run the same
command again, or restore a backup you choose); "environment not verified" (`Verify_Tree.bat`); "this tree is not
<role>" (the settings file and the folder disagree); "results changed other than by growing"; "a status file fails
its check" (take it from your newest backup); "a process of this tree is running"; "orphan marker present". The main
warnings that are not refusals: "a list is foreign and is ignored: <variant>" (reseed, replace QA's software, or rerun
that variant); "results not current from draw X" (the derived-only rerun; or, after a correction of shared code, the rerun for the
variants it names); "the updater failed: nothing new was
read" (run the job again later; `--no-update` to work without it). A STOP is a STOP: nothing retries by itself.

## 17. From the old system to this one (owner: a clean baseline, nothing destroyed; EX_259 B; EX_261 F04, P07; entry 131)

**17.1 What "clean" means.** The new trees start with the accepted official results and no derived record. All history
is computed again by the first jobs. Nothing recomputed is ever described as forecast or published at the original
time. The sealed Mode H records, the old run folders and the old reports are not in QA or PROD.

**17.2 The old state is preserved before anything changes: the owner's own ZIP (owner, entries 130, 131).** Before
phase 1 moves any source file in DEV, **the owner himself makes one full ZIP of the whole project folder on E:,** by
hand, with the old run folders that Git ignores and `.git` included, and keeps it off E:. Claude tells him when it is
time. No tool is designed or built for it, and no second ZIP from GitHub is needed.

| Copy | Holds | Does not hold |
|---|---|---|
| **The owner's ZIP of the project folder** | everything in that folder: tracked files, `.git`, the ignored run folders with the old forecast records; the old `.venv` if he includes it | anything outside that folder |
| GitHub | tracked files and history | ignored files |

- **That ZIP is the only copy of the old forecast records that Git does not track.** Phase 1's oracle and the
  transition check read those records.
- **Rollback, stated truthfully.** Phase 1 moves source files inside the DEV clone, so after phase 1 the clone is no
  longer the old system. A Git tag brings back the old source, not the ignored records. **The old system can be run
  again only from an untouched copy:** unpack the owner's ZIP into a new folder (never over the clone), build its
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
  (QA is recommended here so that the check is made before PROD exists; it is not required, and the check can
  equally be made in PROD before PROD is declared in use.)
- **The transition check** compares, for every (variant, target) the old system forecast in development, the new
  forecast in QA with the old record: the score of every number, the ranking, TOP and WORST. It compares that
  scientific content, not whole-record digests, because the record format has changed (P07). It is a program of the
  transition package, outside the infrastructure; it reads the old records in DEV or in an unpacked copy of the
  owner's ZIP, read-only; a difference stops the transition for review. After it, no part of the new system reads an
  old record.
- **What phase 1 moves** (owner, entry 139; taken from the installed tree, where `src/` is as at commit `cc0ab73`):

| Today | After phase 1 |
|---|---|
| `src/methods/E_002` to `E_019`: each family's `contract.py` and its own modules (for example E_6's `beta_bernoulli.py`), with `variants.py` | the family's shared core file (`core_v1.py`, and its other modules beside it) and one folder per variant holding `method.py` and `VARIANT.json` |
| `src/methods/E_001/*` and `contract_adapters/e_001.py` | the adapter becomes `E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py`; E_1's own modules stay where the proof-of-concept suite imports them |
| `_common/recurrence_gaps.py`, `occurrence_counts.py`, `polynomial_fits.py` | `_shared/recurrence_gaps_v1.py`, `occurrence_counts_v1.py`, `polynomial_fits_v1.py` |
| Every `import` of a moved file, in `src/` and in the tests | follows the move; no other line changes |
| `Method_Contract_Runner.py` (its hand-kept table of methods) and `closure.py` (its list of code folders) | the table is built from the folder tree; the folder list follows |

  Phase 1 changes DEV's working files only. Nothing is installed anywhere by it: QA and PROD do not yet exist.
- **Phase 2's starting list** is the table of kept, changed and left-out modules in section 10 of the simplification
  design v0.1, read with this specification: the coordinator and its plumbing are not installed outside DEV; install
  and release records and Git are gone from deployment; the install tools work from local files; and the lists, the
  status file, the job and the tools are as specified here. Its first task is the exact list of what the coordinator
  plumbing imports.

**17.4 The build order: one ratified design, built in four steps, each on its own go (owner, entry 143).**
1. **The folder layout:** phase 1, above.
2. **The research engine, in DEV:** the lists, the job with its fill and catch-up, scoring, the reports, both OV-1
   scores, the status file and withdrawal (sections 3 to 11). This is the experiment itself, running on DEV's data.
3. **Trees, installs, backups and restore:** `Init_Tree`, `Install`, `Reinstall_Infra`, the checks, backups, the recovery
   kit and the restore (12.1 to 12.6, 13, 14.1), then the transition check and PROD's first job. **After this step PROD
   exists and forecasts every week,** and new methods can be added.
4. **The laboratory tools:** the QA software replacement (12.7), the research-data reseeding (14.2), the historical
   walk-forward rerun (7A), the correction of shared code (12.8) and `Check_Forecasts`.
Steps 2 and 3 are built so that step 4 adds to them and does not change them: every list header carries the
fingerprint and the forecasting-code identity from the first day, and the job's checks of 5.6A and 5.8 are in step
2, because step 4's tools rely on them. **Until step 4 is built, a fault found in shared code is not improvised around:** the affected work is stopped
or held (a withdrawal, or no job for that game) until the tools exist, or the owner restores a backup (the reviewer,
entry 144).

## 18. Tests the code rounds must show (functional faults, not fraud)

On invented games and toy variants unless marked (real):
- **Records (F01):** 100 forecast and scored, 101 `METHOD_FAILED`, 102 forecast and scored: valid, and the job goes on;
  a first target fixed by minimum history, and a method-declared insufficient history; a gap, a repeat, a score
  without a forecast, a second score, a score beyond an unscored forecast, a broken chain: each refused; a torn last
  line in each file, cut and redone; any other exception writes nothing and stops; a crash planted between every
  two writes of 5.7, then the job again, gives the bytes of an uninterrupted run.
- **N-1 (F06):** draws at and after T changed and appended: T's content digest unchanged, its envelope changed; the
  same variant recomputed in the same environment gives the same content.
- **The job:** the examples of 7.2 line for line; the results step absent, failing and left out; results changed
  other than by growing; QA and DEV never start the updater.
- **The status file (entries 136, 137):** created `ACTIVE` at install; shows status, draw, reason and eligibility draw
  per game; a withdrawal changes that file and no scientific byte, and the variant's fingerprint and marker are
  unchanged; a hand edit, a deleted `[check]` line and a missing file in QA each refuse and name the file; a crash
  planted before and after the rename leaves the old or the new file, never a mixture; an eligibility draw already
  present is never rewritten by any job; a file taken from a backup ZIP is accepted.
- **Withdrawal (F02, R5-F01):** the planted late result: a pending forecast for 1601, a withdrawal effective 1601, the
  result of 1601 then accepted: no score line, no league scoring and no contribution to either OV-1 at 1601, no line
  for 1602, earlier lines byte-identical; the same in a catch-up of six draws; no command reinstates; a restore to
  before it runs the variant again; the same behaviour in QA and DEV as in PROD.
- **OV-1 (F03):** no prevailing line before the start; an eligibility draw written only after a successful results
  step; a later variant's eligibility draw; a cohort member with `NO_FORECAST`; a missing or held member blocks; a
  withdrawn member leaves the cohort at its draw and earlier lines are byte-identical; the ledger equals its
  rebuild; the fixed text and the counts. **QA and PROD agree:** with the same software, status files and research
  data the two ledgers are byte-identical; QA receiving a hundred more draws leaves a copied eligibility draw of 1601
  at 1601.
- **The derived check (5.8):** one stored score altered, one ledger line altered, a planted change to the scoring
  code: each is found at the right draw; forecasts go on and the next draw is forecast; no score, line or report is
  written from that draw; nothing stored is altered; the derived-only rerun settles it.
- **Readiness and installing (F08 to F10, R5-F02), with the examples of EX_262:** two ready variants and one unfinished
  in DEV: `Install.bat` adds the two only; one is edited afterwards and is left out by name until marked again; a
  hand-made marker with a wrong hash is not ready; marking twice gives the same bytes; Python making `__pycache__` in
  DEV changes nothing; an editor's backup file in the folder is named and refused; an edited helper un-readies every
  variant that lists it; an import not on the helper list, and each forbidden way of importing, is not ready; a
  helper present with other bytes refuses; an existing variant is never overwritten; QA and PROD installed
  independently, in either order; nothing half-installed is ever run; no tool or launcher writes a settings file
  after its creation.
- **The smoke case (R5-F03):** a variant with a valid marker and clean imports whose `compute()` fails: the install
  refuses and the target stays behind its barrier, though the suite and the sample pass; a variant that returns
  insufficient history on the smoke table fails; the smoke case writes under `scratch\` only (every other file of the
  tree is hashed before and after) and reads no real draw.
- **Infrastructure (R5-F04, R5-F05, N03):** `Reinstall_Infra.bat` changes one listed file and no variant; the marker
  stale after an edit; the manifest with a malformed line, a duplicate path, a missing file and an unknown class;
  the class test catching a `derived` label on a file the forecasting entry point imports; the two statements, each produced by a planted change of the right kind; a plan holding a `forecast`-class file
  refused and sent to the correction command; a change to scoring found in full, at the right draw; **the
  backup attempt failing, reported as not made, never named as a way back;** NO and Enter change nothing; YES
  proceeds with the backup failed; the kit failing warns and does not stop; an install stopped at every step, then
  the command again; no rerun is ever started by an install.
- **`Check_Forecasts`:** a planted change to the readout found by `--all` and missed by a sample chosen to miss it (the
  reason a sample is never called a proof); stopped and continued; writes only its report.
- **The rerun (7A):** the examples of 7A.7; a range with `--to`: nothing after N is left looking complete, and the next
  job catches up to the same bytes as a rerun without `--to`; every dependent report and both OV-1 records rebuilt;
  status files byte-identical before and after; the archive ZIP holds the first-written lines exactly and verifies; every
  new line says its result was on file and names the rerun; stopped at every step, then the command again; a wrong
  role typed changes nothing; the PROD warning shown only where the settings say PROD, by the same code.
- **The QA software replacement (12.7):** PROD holds V1, V2 and infrastructure I1; QA holds V1, an experimental V3 and
  I2: afterwards QA's software is V1, V2 and I1 with PROD's status files; QA's settings, `.venv`, backup root and
  records are its own; QA's research data is byte-identical; its lists for V3 are foreign and ignored; **every file of
  PROD is hashed before and after: identical;** a failing smoke case leaves QA refusing to launch; stopped at every
  step, QA never looks ready; a destination that is, or is another name for, PROD or DEV refuses.
- **The reseeding (14.2), EX_265's tests:** PROD byte for byte unchanged through a successful, a failed and an
  interrupted copy; PROD changed during the copy: refused, destination unchanged; a busy destination refuses;
  stopped before and after the barrier; QA keeps its software, status files, settings and `.venv`; one QA variant
  with other bytes than PROD's of the same name: its copied list is warned about and ignored, everything else is
  used, and a rerun for it computes QA's variant; the same reseeding into DEV; then the software replacement as
  well: QA's figures equal PROD's.
- **Helpers and the DEV conveniences:** no command but `Correct_Shared_Code` overwrites an installed helper, and that one only on its own question; `Who_Uses` against planted
  declarations; `Make_Successors` refuses a name that exists, leaves the originals untouched, copies no marker and
  no status file, and withdraws nothing; batch marking, unmarking and withdrawal; an unmarked variant is not
  installed into a new tree.
- **Roles (F09):** QA's settings pointing at PROD's folder refuses; a QA tree copied to another place refuses; a
  backup root inside the tree refuses; QA and PROD backups land in their own roots.
- **Backup and restore:** as the deployment design lists, including that a restore installs nothing afterwards and
  brings back the status files of its day.
- **EX_267's oracles.** *R6-F01:* a ranking change that alters a sampled forecast of V1: `Reinstall_Infra` refuses the
  plan; `Correct_Shared_Code` holds every variant; no list made under the old code is appended to; after the rerun
  every active forecast of V1 carries the new identity and the first-written ones are in the archive, hashed. A
  helper used by V1 and V2 corrected: both held, V3's forecast list byte-identical throughout. A family's core
  corrected: only that family's variants held. A corrected forecasting file whose sample happens to match: every
  variant still held. A correction leaves every status file byte-identical, a withdrawn variant withdrawn and every
  eligibility draw as it was. *R6-F02:* a draw appended to the results file leaves every earlier score "agreeing";
  scoring code rewritten with the same answers agrees; one changed answer is found at its draw; a league CSV naming
  a variant now foreign is moved out of the active folder and the cutoff file names the draw. *R6-F03:* a
  derived-only rerun changes zero bytes of every forecast list and keeps every made-before-the-result envelope;
  `--only V1` rebuilds every game-level report and both OV-1 records; `--to N` leaves nothing after N current;
  `--derived-only` with `--only` or `--to` refuses; a rerun stopped after each step, then run again, gives the same
  bytes; the archive ZIP failing to verify leaves every active file untouched. *R6-F06:* a corrected scorer that
  changes draw X is foretold with X, installs on YES, leaves the tree not current from X, and nothing reports
  agreement. *R6-F07:* a job, and a results step, started between the withdrawal's display and its write: each finds
  the lock held; no score at T after a withdrawal from T; the status file is the old or the new, never between.
- **EX_269's oracles.** *R7-F01:* results on file through 1700; a rerun `--from 1550 --to 1650`: nothing after 1650 is
  current; one ordinary job then gives the scientific content of a rerun without `--to`, and the cutoff file goes
  only then; the same with `--only V1` while V2 is held: the hold is not cleared and the file stays, as `MISMATCH`.
  *R7-F02:* a changed report formatter that alters no score: no old-format file remains in the active folder when
  the reinstall returns; PROD's V1 withdrawn from 1601 and QA holding reports beyond 1600: when the QA software
  replacement returns, before any job, no invalid report is in QA's active folder and the cutoff file is there.
  *R7-F03:* a rerun crashed after the archive, after some lists were shortened, after all were, and after J+3 was
  computed again, then crashed once more during recovery: the first ZIP is unchanged and verifies, no recomputed
  line is cut again, and the final content equals an uninterrupted run's. *R7-F04:* in the deployment design.
- **(real)** Phase 1's oracle; the transition check.
One planted defect for each rule. The whole suite before and after each install.

## 19. Decided, and what is left for ratification

**The owner's choices on the earlier drafts are all made** (none is open):

| | Decided | Entry |
|---|---|---|
| A | The research job runs the reviewed updater itself in PROD, through its own launcher; `--no-update` leaves it out | 130 |
| B | The eligibility draw is the first draw not on file after a successful results step (10.2) | 130; named, 135 |
| C | The owner himself makes one full ZIP of the project folder on E: before phase 1; no tool, no second ZIP | 131 |
| D | Withdrawal by one command and one confirmation; now recorded in the variant's status file; one-way | 130, 136, 137 |
| E | The research-data reseeding from PROD into QA or DEV, required; no other export | 128, 129, 135 |
| F | A readiness marker for the infrastructure; `deploy/INFRA_MANIFEST.ini` | 127 |
| - | Helpers add-only; successors; the three DEV conveniences | 127 |
| - | QA never a gate; one science in every tree; no sandbox mode | 126, 136 |
| - | The QA software replacement from PROD; the rerun in every tree, PROD as a last resort | 135, 137 |
| - | Backups at installs: attempted, reported, never a condition; a confirmation defaulting to NO | 135, 136 |
| - | Defective shared code corrected in place, the affected variants then recomputed; replaces 127's no-overwrite rule for defects only | 141, 143 |
| - | What a rerun replaces is first saved in one verified, clearly named ZIP | 142 |
| - | The phase 1 file list in this document; one design built in four steps | 139, 143 |

**Mechanisms I chose where no decision exists, each with the leaner alternative** (for the reviewer to judge and the
owner to ratify with the rest; none needs an answer before the review):
1. **The job checks the derived results in full at every start** (5.8). Leaner: only at an install or a copy. If it
   proves slow when measured, the alternative stands ready and sets the same cutoff file.
2. **Any change to a `forecast`-class file is a correction of shared code, and holds every variant until a rerun**
   (12.4, 12.8), even a change believed to alter nothing. That is the price of a persistent rule that needs no
   judgement of harmlessness. Leaner in running cost, fuller in machinery: let `Check_Forecasts --all` finding every
   stored forecast unchanged stand in for the rerun. Not designed; it can be added if such changes prove common.
3. **In DEV an edited variant's or helper's old lists are foreign and wait for a rerun** (5.6A), where v0.3 moved them
   aside by itself. One rule in every tree; the cost is one command in DEV after an edit.
4. **The suite is run only where it belongs to the installed infrastructure** (12.3, 3).

**For the reviewer.**
1. Does 12.8, with the header identity of 12.4 and the hold of 5.6A, close R6-F01 with no mixed history and no
   way round it?
2. Is the list of compared fields in 5.8 the right projection, and does moving stale reports out of the active
   folder, with one cutoff file, close R6-F02?
3. Does the table of 7A.2 leave any mode able to change a file it should not, or to leave a dependent result
   standing (R6-F03)?
4. Do 12.7 and 14.2, with the deployment design's 6A and 6B, now close R6-F04 and R6-F05?
5. Is item 2 of the list above acceptable as the persistent rule, at its running cost?

## 20. Not tested, and uncertainties

- Nothing has been run. No timing is known: a first full fill, the derived check at each job, a `Check_Forecasts
  --all`, a rerun, or a backup of a tree.
- **The derived check is called cheap on reasoning, not measurement:** it runs no method, but the OV-1 kernel uses
  exact whole-number arithmetic and its cost over a long history is unmeasured.
- The smoke case uses invented fair draws. A method whose fit cannot be made on such a table would fail it and would
  need a table of its own; none is known to.
- The static import check reads ordinary import statements and forbids the named dynamic ones; a determined
  workaround in a method file would escape it. It is a check against accidents.
- The readout may carry the old run mode deeper than its record fields; the transition check is what would show it.
- DEV's working files are the install source. If Git rewrites line endings in DEV, hashes change: markers stop
  matching and a helper may be refused. That fails safe; pinning line endings for `src/` in `.gitattributes` avoids it.
- Windows may update a file's last-access time when PROD is read. "PROD unchanged" means every file's content, name,
  size and modification time.
- QA will be backed up at the end of each job like any tree. If that proves a nuisance in a laboratory used many
  times a day, a setting in QA's own settings file to leave it out is the lean answer; not designed until measured.
- **A correction of forecasting code holds every variant until a full rerun,** however small the change. With many or
  slow methods that is a long computation, unmeasured. It is the owner's choice each time.
- Step 4 of the build order comes last. A design fault found then in a step-4 tool could reach back into steps 2
  and 3; the header identities and the two checks are put in step 2 to make that unlikely, not impossible.
- Section 1.2 names the binding clauses by section. An exact clause list for E2R-1 section 7 is a first task of the
  code round.

## 21. Where each finding and decision landed

The full index (every decision, finding and draft contradiction, with its section) opens EX_266. In short:

| Item | Where |
|---|---|
| EX_261 F01 record states, crash order | 5.2 to 5.7; 18 |
| F02 owner-only withdrawal | 11; 3.5; 10.4; 9 |
| F03 eligibility wording, first job, failed updater | 7.1, 7.2; 10.2 to 10.4, 10.6 |
| F04 the old system's preservation; rollback truth | 17.2 |
| F05 a coherent install and update sequence | 12; deployment design sections 4 to 6B |
| F06 content and envelope | 5.4; 6; 18 |
| F07 one complete specification | this document; 1.2 and 1.3 |
| EX_262 F08 marker, ready-and-absent, local files | 3.4; 4; 12.1 |
| F09 roles, settings, backup roots | 2; 14; deployment design section 1 |
| F10 REINSTALL INFRA | 12.4 |
| EX_264 R5-F01 a withdrawn pending forecast is never scored | 5.6 (4, 5), 5.7, 7.1, 9, 10.4, 11; 18 |
| R5-F02 exact hash closure; no self-reference | 3.4; 4; 13; deployment design 3.1 |
| R5-F03 each new variant made to forecast | 12.3 (2); deployment design 3.3, 5 |
| R5-F04 never a promised rollback that does not exist | 12.3; 12.4; 14.1; deployment design 5, 6, 8 |
| R5-F05 no recomputation of everything | 5.8; 12.4; 7A |
| N01 withdrawal boundary | 11 |
| N02 QA and DEV OV-1 | superseded by the owner (entry 136): 2; 5.4; 10.6 |
| N03 manifest syntax | 12.4 |
| N04, N05 | 4; 16 (`Check_Tree`) |
| Entry 126 the marker alone; QA never a gate | 2; 12.2 |
| Entry 127 infrastructure marker; helpers; successors | 3.3A; 4; 12.2; 12.4 |
| Entries 128, 129, 135 the research-data reseeding | 14.2; 5.6A |
| Entries 130, 131 choices A, B, C, D | 7.1; 10.2; 17.2; 11 |
| Entry 135 the QA software replacement; rerun rebuilds everything; the eligibility draw's name | 12.7; 7A.3; 10.2 |
| Entries 135, 136 backups at an install | 12.4; 14.1 |
| Entry 136 one science in every tree; the status file; the words | 2; 3.5; 5.4; 10.6; header |
| Entry 137 the rerun in every tree; one-way withdrawal; one status file; eligibility preserved | 7A; 11; 3.5; 10.2 |

| EX_267 R6-F01 forecast-changing shared code | 12.8; 12.4; 3.3A; 5.2; 5.6A; 18 |
| R6-F02 what the derived check compares; stale reports | 5.8; 18 |
| R6-F03 the rerun's modes | 7A.2 (table), 7A.4, 7A.5; 18 |
| R6-F04 status bytes hashed when PROD is read | 12.7; deployment design 6A |
| R6-F05 the destination reserved before the copy | 12.7; 14.2; deployment design 6A, 6B |
| R6-F06 an expected derived difference is not a failed check | 12.3 (5); 12.4 |
| R6-F07 the withdrawal serialised | 11 |
| N01 classes are labels; N02 a held member blocks; N03 what NO leaves | 12.4; 5.6A; 12.4 |
| Entry 139 the phase 1 file list | 17.3 |
| Entry 142 the archive ZIP | 7A.4 |
| Entry 143 correction in place; the four-step build order | 12.8; 17.4 |

| EX_269 R7-F01 a rerun stopped at N and the ordinary catch-up | 5.8; 7A.2 |
| R7-F02 print-outs after a report-code change; QA after a software replacement | 9; 12.4; 12.7; 14.2 |
| R7-F03 a continued rerun never shortens twice | 7A.5 |
| R7-F04 an ordinary install and a job started meanwhile | deployment design 5 |
| R7-N01, N02, N03 | deployment design 3.4 and section 18 here; 7A.4; 12.4 |

End of the specification, DRAFT v0.6.
