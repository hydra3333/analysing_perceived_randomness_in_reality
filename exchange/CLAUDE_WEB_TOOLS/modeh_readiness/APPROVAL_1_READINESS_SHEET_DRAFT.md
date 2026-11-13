# Mode H: the Approval 1 readiness sheet (both games) - DRAFT for the reviewer's independent check

**DRAFT (Claude web chat on Fable 5.2, 13-14 November 2026). Nothing here is authorised and nothing was run or opened.**
Written at the project owner's request of 13 November 2026, 22:08, after his decisions that day (Mode H first, then
MHUP-B, in principle; Q7 decided). It goes to the ChatGPT reviewer first; the owner decides afterwards, one approval at a
time. Sources: design v0.1r7 sections 1, 4, 5 and 7; the installed code at `main` (commit `87c4219` for `tests/`, `effc179`
for everything Mode H runs), read line by line for this sheet; a dress rehearsal on invented data (section 10).
US-ASCII, CRLF. No outcome of any draw appears here; draw numbers and dates (from the weekly rule) are identifiers only.

## 1. What you would be committing to

For each game, once: freeze the study (the 40 released variants, the code, the environment), open the holdout, bring the
ten holdout draws into the master, make every variant's forecast for each of the ten draws from the draws before it,
then score them once and seal the result. Each step writes create-only records; no step can be done twice.

**Recorded at your instruction (13 November 2026):**
- **The cohort is fixed.** The 40 variants per game released today (12 methods; 39 released on 31 October 2026 and E_1
  revision 3 on 13 November 2026) are the whole Mode H study. A method, revision or variant released later can never
  claim a fresh evaluation on these ten draws: by then the draws are ordinary history, and the tools refuse a second
  plan or score.
- **CATCH_UP is retrospective.** A forecast made after its draw's result was public is catch-up evidence, reported in
  its own tier and never pooled with prospective evidence. It cannot replace a genuine prospective forecast that was
  not frozen before its draw. Every week before the weekly session exists (MHUP-B) is one more draw per game that can
  only ever be catch-up.
- **The freeze.** From the first Approval 1 until both games are sealed: no MHUP-B install and no change to the frozen
  code or environment (section 7).
- **Q7.** The restriction on raw draw values in the AI chats stays after Mode H. Approved project programs read and score
  them through their controlled interfaces. Aggregate reports are shareable.

## 2. What this evaluation can and cannot show

- **What it is:** a precommitted holdout evaluation with N-1 isolation, not pre-draw forecasting. The ten results per game
  have been public since August to October 2026; what keeps them from the methods is the reader, which never decodes the
  target row or any later row. The supported statement is design section 1's: plan, code and environment frozen before
  the holdout was opened; every forecast used only earlier draws; every forecast frozen before any scoring read an outcome.
- **The pre-registered readouts are three family results:** for Powerball, main numbers and the Powerball number (each
  the best of 80 tracks: 40 variants, TOP and WORST picks); for Oz Lotto, main numbers (best of 80). The study manifest
  fixes them before opening. Everything else in the report (league tables, per-track figures) is descriptive.
- **Ten draws give little power.** My own exact arithmetic, as a guide to scale only (the report computes its own
  figures; `modeh_scale_illustration.py`): for a track to stand out family-wise at 5%, it needs at least 25 main-number
  matches over the ten Powerball draws (fair expectation 14.0), or 21 over the ten Oz Lotto draws (fair 10.4), or 5 of 10
  Powerball numbers right (fair 0.5). That is about 1.8 to 2 times chance, or ten times for the Powerball number. An edge
  of 5% would need over a thousand draws to show for even one pre-chosen track. So Mode H can reveal only a dramatic
  effect; it cannot detect a small one.
- **A null result** means "no statistically compelling departure from the fair-draw reference under the reported
  measures". It is not proof of randomness, and it says nothing about methods outside these 12.
- **Expect chance "hits".** The Powerball report counts 2,080 local tests; of the order of a hundred will fall below 5% by
  chance alone. A single low local p-value is not a finding; the family lines are the test. Picking "the best variant"
  from ten draws is exploratory.
- **Exposure flags.** Powerball 1585 and 1586 were displayed in a reviewer chat on 25 October 2026 (HX-1). They are scored
  and counted like any other draw and flagged in the records and the report. Oz Lotto has none.
- **Not frozen, and stated:** the operating system, the hardware, the clock. A method that fails on a target is recorded
  and scored as missing, never rerun.
- **Two separate studies.** The games are never pooled. To avoid a choice made after seeing one result, I recommend you
  decide now that both games will be run, whatever the first shows (section 9, D2).

## 3. The four approvals, per game

| | Powerball | Oz Lotto |
|---|---|---|
| Holdout draws (targets) | 1577-1586 (6 August to 8 October 2026) | 1694-1703 (4 August to 6 October 2026) |
| Cohort | 40 variants, 80 tracks | 40 variants, 80 tracks |
| Families | main numbers; the Powerball number | main numbers (supplementaries are never stored) |
| Exposure flags | 1585, 1586 (HX-1) | none |
| The first update will add | 1577 to the latest published draw (1591 until the draw of 19 November) | 1694 to the latest published draw (1708 until the draw of 17 November) |
| Runs in the batch | 400 | 400 |

| Approval | What it does | Writes | After it |
|---|---|---|---|
| **1** | Freezes the study manifest, then writes the opening record with your typed sentence | the manifest; the opening record (permanent); two search-log rows | the code and environment are locked for this game; the updater's quarantine no longer protects it |
| **2** | The first results update, from Lotterywest-GOV, for this game only | the master (version 2), one ledger row, a backup of version 1, the grab | the holdout draws and every later draw are in the master; the updater refuses for this game until the seal |
| **3** | Freezes the one plan, then runs every variant on each of the ten draws | the plan and its id record; 400 frozen forecasts with their tickets; `BATCH_COMPLETE` | no forecast can be added or changed |
| **4** | The one score: reads the ten outcomes once, writes the score ledger, the report and the seal | `SCORING_STARTED`, the score ledger, `SCORE_COMPLETE`, three report files, `MODE_H_SEALED` | the study is closed; the updater is free again for this game |

Not part of these approvals, and not to be run now: `declare-developed` (GOAL-1; it belongs with the weekly session) and
`advance` (only after written agreement, for a ledger row that should not exist).

## 4. What cannot be undone or repeated

- **The manifest** (Approval 1, first command). Create-only; the design provides no re-planning. From this moment the
  game's study is tied to the exact code and environment on your PC. Nothing is exposed yet.
- **The opening record** (Approval 1, second command). Permanent. It removes the quarantine for this game.
- **The first update** (Approval 2). The holdout draws enter the master. They cannot be taken out again in any meaningful
  sense. This is the real point of no return.
- **The plan and each forecast** (Approval 3). One plan per game; one counted attempt per variant and draw.
- **The score** (Approval 4). One routine score per game. An interrupted score resumes the same attempt; a second is
  refused. A corrective scoring run exists in the design only after the seal, under its own identity, and only once
  MHUP-B provides it.
- **If the frozen code needs a fix after the manifest,** that game is blocked: every later step refuses a changed
  closure, and abandoning or re-planning needs its own reviewed design, which does not exist. Blocked is not broken:
  nothing expires, no outcome is read, and the other game is unaffected if its Approval 1 has not been given.

## 5. Before the first Approval 1 (prerequisites)

Each is yours to do or confirm; none is authorised by this sheet.

1. **Backups confirmed** of `source_data\` and `results\` (R-015 (c)). The frozen forecasts, the tickets and the score
   ledger are Git-ignored and exist only on your PC, so back up again after each game is sealed.
2. **The POC rerun** (R-015 (b)): `OWNER_POC_RERUN_R015b_DRAFT.md`, with its own go. It ends with no orphan marker and
   the byte-code folder absent.
3. **The updater's offline self-test** (design 4.4; register future action 4): `Run_Results_Updater.bat --self-test`.
   Expect only `[SELF-TEST] 13/13 PASS`. Any `FAIL` or traceback is a STOP.
4. **The tree is the reviewed one:**
   ```
   cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
   git pull --ff-only
   git status --short
   git status --short --ignored src
   git diff --stat effc179 HEAD -- src "*.bat" requirements.txt
   ```
   Expect: nothing from the first status; from the second, nothing or only lines ending `__pycache__/`; nothing from the
   diff (no code file has changed since the install).
5. **The browser starts** (proposed; section 8, F-1; it opens a blank page and contacts no lottery website):
   ```
   "%CD%\.venv\Scripts\python.exe" -B -c "import os; os.environ.setdefault('SE_AVOID_STATS','true'); os.environ.setdefault('SE_AVOID_BROWSER_DOWNLOAD','true'); from selenium import webdriver; o=webdriver.ChromeOptions(); o.add_argument('--headless=new'); d=webdriver.Chrome(options=o); d.get('about:blank'); print('BROWSER OK', d.capabilities.get('browserVersion')); d.quit()"
   ```
   Expect `BROWSER OK` and a Chrome version. Selenium may fetch Chrome's matching driver from Google the first time, as
   the updater itself would. A failure here is fixed outside the frozen code (Chrome or its driver).
6. **Quiet machine:** nothing of the project running; VS Code's Python terminals and Claude Code closed; no orphan marker
   (`dir transitory_data\poc_runs\UNRESOLVED_ORPHAN.json` gives `File Not Found`).

## 6. The commands (one CMD window at the repository root; one game at a time)

Each line is run only under its own approval. Check each output against "Expect" before the next line. There is no time
limit between approvals; a pause of hours or days changes nothing.

### Oz Lotto (recommended first: section 9, D1)

**Approval 1 - the manifest and the opening record** (the manifest hashes the code and the whole Python environment; allow
a few minutes):
```
Run_Evaluation.bat Method_Mode_H.py manifest --game OZLOTTO
```
Expect one line: `[MODE-H] MANIFEST written for OZLOTTO: 40 variants, targets 1694-1703, frozen master version 1, closure 497 files, digest <12 characters>..., environment digest 966a27926d23...`
**Check before going on:** 40 variants; version 1; 497 files; the environment digest starts `966a27926d23` (the value T016 found on
your venv on 13 November). If any of the four differs, stop here and send me the line: nothing is opened yet.
```
Run_Evaluation.bat Method_Mode_H.py open --game OZLOTTO --statement "I open the holdout of this game for the sealed Mode H study; the study manifest is frozen."
```
Expect: `[MODE-H] HOLDOUT OPENED for OZLOTTO: freeze version 1; the opening record is permanent. ...`
Recommended witness (section 9, D3), before Approval 2:
```
git status --short
git add results/real/holdout/OZLOTTO/MODE_H_STUDY_MANIFEST_V1.json source_data/HOLDOUT_OPENED_OZLOTTO.json results/audit/SEARCH_LOG.csv
git commit -m "Mode H OZLOTTO: study manifest and opening record (Approval 1)"
git push
```
Expect `git status --short` to show exactly those three paths (two new, the search log modified), plus any earlier game's files.

**Approval 2 - the first results update** (contacts Lotterywest-GOV; headless Chrome; about a minute):
```
Run_Results_Updater.bat update --games OZLOTTO
```
Expect: `[MASTER] OZLOTTO: checked 9 overlapping draws (all matched), added <n> (1694..<latest draw>), warnings <w>` and
`[MASTER]   grab kept: ...; backup: ...`. The count 9 holds while it is November; `<latest draw>` must be 1703 or later.
A `warning:` line about a date off the weekly rule is information: send it to me before Approval 3.

**Approval 3 - the plan and the batch** (about one to five minutes):
```
Run_Experiment.bat Method_Walk_Forward.py plan --mode H --game OZLOTTO
```
Expect: `[WALK-FORWARD] MODE H PLAN wf-<32 characters>: OZLOTTO targets 1694-1703, 40 variants, master version 2 <12 characters>...`
and a `next:` line giving the exact run command with the batch id. Paste that line's command:
```
Run_Experiment.bat Method_Walk_Forward.py run --game OZLOTTO --batch wf-<the id printed>
```
Expect, at the end: `[WALK-FORWARD] BATCH_COMPLETE written: every planned pair has its DONE ticket (design 5.2)` and
`[WALK-FORWARD] COMPLETE: 400 run(s) in this invocation; every pair of the plan is done`.

**Approval 4 - the one score and the report** (about one to five minutes):
```
Run_Evaluation.bat Method_Mode_H.py score --game OZLOTTO
```
Expect progress lines ending `MODE_H_SEALED written; the study is closed`, then
`[MODE-H] SEALED: attempt mh-<32 characters>, batch wf-..., search-log row <n>, 800 score lines, 400 rank lines` and three
`[MODE-H] wrote ...results\method_rankings\OZLOTTO\mode_h_OZLOTTO_1694-1703_mh-....txt` (and `.csv`, `.json`) lines.

### Powerball

**Approval 1 - the manifest and the opening record:**
```
Run_Evaluation.bat Method_Mode_H.py manifest --game POWERBALL
```
Expect one line: `[MODE-H] MANIFEST written for POWERBALL: 40 variants, targets 1577-1586, frozen master version 1, closure 497 files, digest <12 characters>..., environment digest 966a27926d23...`
**Check before going on:** 40 variants; version 1; 497 files; the environment digest starts `966a27926d23` (the value T016 found on
your venv on 13 November). If any of the four differs, stop here and send me the line: nothing is opened yet.
```
Run_Evaluation.bat Method_Mode_H.py open --game POWERBALL --statement "I open the holdout of this game for the sealed Mode H study; the study manifest is frozen."
```
Expect: `[MODE-H] HOLDOUT OPENED for POWERBALL: freeze version 1; the opening record is permanent. ...`
Recommended witness (section 9, D3), before Approval 2:
```
git status --short
git add results/real/holdout/POWERBALL/MODE_H_STUDY_MANIFEST_V1.json source_data/HOLDOUT_OPENED_POWERBALL.json results/audit/SEARCH_LOG.csv
git commit -m "Mode H POWERBALL: study manifest and opening record (Approval 1)"
git push
```
Expect `git status --short` to show exactly those three paths (two new, the search log modified), plus any earlier game's files.

**Approval 2 - the first results update** (contacts Lotterywest-GOV; headless Chrome; about a minute):
```
Run_Results_Updater.bat update --games POWERBALL
```
Expect: `[MASTER] POWERBALL: checked 9 overlapping draws (all matched), added <n> (1577..<latest draw>), warnings <w>` and
`[MASTER]   grab kept: ...; backup: ...`. The count 9 holds while it is November; `<latest draw>` must be 1586 or later.
A `warning:` line about a date off the weekly rule is information: send it to me before Approval 3.

**Approval 3 - the plan and the batch** (about one to five minutes):
```
Run_Experiment.bat Method_Walk_Forward.py plan --mode H --game POWERBALL
```
Expect: `[WALK-FORWARD] MODE H PLAN wf-<32 characters>: POWERBALL targets 1577-1586, 40 variants, master version 2 <12 characters>...`
and a `next:` line giving the exact run command with the batch id. Paste that line's command:
```
Run_Experiment.bat Method_Walk_Forward.py run --game POWERBALL --batch wf-<the id printed>
```
Expect, at the end: `[WALK-FORWARD] BATCH_COMPLETE written: every planned pair has its DONE ticket (design 5.2)` and
`[WALK-FORWARD] COMPLETE: 400 run(s) in this invocation; every pair of the plan is done`.

**Approval 4 - the one score and the report** (about one to five minutes):
```
Run_Evaluation.bat Method_Mode_H.py score --game POWERBALL
```
Expect progress lines ending `MODE_H_SEALED written; the study is closed`, then
`[MODE-H] SEALED: attempt mh-<32 characters>, batch wf-..., search-log row <n>, 800 score lines, 400 rank lines` and three
`[MODE-H] wrote ...results\method_rankings\POWERBALL\mode_h_POWERBALL_1577-1586_mh-....txt` (and `.csv`, `.json`) lines.

For Powerball the score also reports the Powerball-number family, and the report names the two exposure flags.

## 7. The freeze: from the first Approval 1 until both games are sealed

Every Mode H step re-checks every file under `src\`, every `.bat` in the repository root, `requirements.txt`, the venv and
the base Python installation, and refuses on any difference. So, in that window:

- **Do not** edit, save, add, rename or delete anything under `src\`, or any `.bat` in the root (a new one counts too).
- **Do not** run `install_upgrade_dependencies_into_venv.bat`, `create_venv.bat` or `pip`, or update or repair Python.
- **Do not** install any package (MHUP-B included). I will push nothing outside `exchange\`.
- **Git:** only `git pull --ff-only`, `git status`, `git log`, `git add <named paths>`, `git commit`, `git push`. No
  `checkout`, `restore`, `reset`, `stash`, `switch` or `clean`: your working copy holds the installed files with the line
  endings the install wrote, and those commands can rewrite them (the content would be the same; the frozen bytes not).
- **Do not** run the updater again for a game between its Approval 2 and its seal (it refuses), and I suggest not at all
  until MHUP-B's checklist exists.
- A refusal for a changed file is recoverable by restoring the exact bytes, as a reviewed step; it is still a STOP.

## 8. An unexpected STOP, and what my cold read found

**The rule.** Any output other than the expected one is a STOP: do not rerun, do not change arguments, do not edit, move
or delete any file, record, marker or lock (if the updater says "delete the lock by hand", do not); send me the whole
window. Before pasting, glance for draw results (these tools print none by design); never paste the master, grab or
backup files or `mode_h_score_ledger.jsonl`. I propose the next step for that exact state; the reviewer checks it; you
approve it.

**How the tools stop** (so you can tell the kind):
- `[MODE-H] REFUSED: ... Nothing was written by this command.` and `[WALK-FORWARD] REFUSED ...`: nothing changed.
- `[MODE-H] FAILED: ... Records written so far stay; a rerun resumes.` and `[WALK-FORWARD] STOP after <n> run(s): ...`:
  stopped part-way; what was done is kept; the designed next step is the same command again, after review.
- `[MASTER] REFUSED`, `STOP` or `VERIFY FAIL`: the master and ledger are unchanged (a grab file may be kept as evidence).
- A launcher line `... no_pycache_ever exists; refusing to run.` (exit 10): the forbidden folder exists.
- A traceback, or a closed window or power cut mid-step: send what you have; do not rerun.

**Findings for the reviewer (none changes the code):**
- **F-1. The updater's live fetch has never run.** The masters are at version 1, and the updater has refused every update
  since the quarantine began, so Approval 2 is the first time its browser fetch and page parser meet the real site, after
  the permanent opening record and with the code frozen. A failure that needs waiting, a retry, Chrome, its driver or
  `--browser firefox` is harmless (nothing is written; the same update is retried). A failure that needs a code change
  (the page's layout changed, say) blocks that game. Mitigations proposed: prerequisite 5; one game at a time (D1); and
  optionally your own look at the Lotterywest results-search page for a June-July 2026 date range in your normal browser,
  to see that each result still reads "Draw <number>", the date, "Winning numbers:". Not proposed: a new fetch dry-run
  mode, which would be a code package before Approval 1.
- **F-2. One test module is pinned to the pre-opening files.** `tests/test_multigame_reader_contracts.py` checks the real
  masters' version-1 SHA-256 and pre-opening refusals, so the suite on `main` will stop passing in full once a game is
  opened or updated. Mode H is unaffected (tests are outside the frozen closure and nothing in Mode H runs them). It
  matters for MHUP-B's step 10 and for any suite run on a clone holding the updated masters: a tests-only fix, designed
  with MHUP-B. The step 10 wording "six development data files" (J-1) will also need its MHUP-B edition.
- **F-3. Line endings.** The install copied the package's exact bytes (LF for the code files) into a working copy whose
  other files Git checked out with CRLF; Git has not rewritten them. That is harmless and stable under the Git commands
  of section 7. The identity check is prerequisite 4 plus the
  manifest's "497 files", not a digest prediction.
- **F-4. Two recovery procedures are MHUP-B's and do not exist yet:** the interrupted-update recovery (design 7, A7) and
  the corrective scoring run. Under "Mode H first", either would be written per case, reviewed and approved, as for J-3.
- **F-5. The orphan marker blocks Mode H too.** Hence the POC rerun before Approval 1, never inside the freeze.
- **F-6. The report is shareable; the score ledger is not.** The three report files hold counts, statistics, draw numbers
  and labels, never a drawn number (decision WF1-10; checked in the rehearsal). The score ledger records the drawn
  numbers; it is Git-ignored and stays on your PC.

## 9. Exposure, and the decisions I ask for after the reviewer's check

**Exposure.** After Approval 2 the master holds the holdout draws and every later draw. The master and its ledger are
tracked by Git: once pushed, every clone holds them (mine, the reviewer's read access, Claude Code's task clones). The
rules do not change: no chat and no runner opens `source_data`, `results` or `transitory_data`; the settings deny those
reads to Claude Code. The later draws that come in with the same update (Powerball 1587 on, with 1587 and 1588 flagged
HX-2; Oz Lotto 1704 on) are not part of Mode H; they are catch-up material for the weekly session.

- **D1. Order.** One game at a time, each through its seal, Oz Lotto first. If the first game met a blocking fault, the
  second would not yet be committed. Powerball, the project's first game, goes second, on a proven path.
- **D2. Both games, whatever the first shows** (barring a technical blocker), decided now.
- **D3. A witness push** of the manifest, the opening record and the search log after each Approval 1 and before
  Approval 2 (value-free files). GitHub's time then shows the study was frozen before the holdout entered the master.
- **D4. The browser pre-check** (prerequisite 5), and the optional look at the page (F-1).
- **D5. The updated masters:** leave them uncommitted until both games are sealed, then decide the push (my
  recommendation; your backups cover them meanwhile). Commit and push the value-free plan, markers and report files when
  you choose.
- **D6. How I see the result:** you attach the report's `.txt` file in the chat. I keep to not opening `results\`.
- **D7. Your own gos, in order:** the POC rerun; the self-test; the backups; then Approval 1 for the first game.

## 10. Evidence behind this sheet (PRELIMINARY; invented data only)

`modeh_dress_rehearsal.py`, run on Linux Python 3.15 against a copy of the installed `src\` with its real release
records: for each game, an invented master, the manifest, the opening record, an invented first update that goes five
draws past the holdout (as the real one will), the plan with the real runner adapters, the batch and the one score.
**DRESS REHEARSAL PASS:** 40 variants and 400 of 400 forecasts published per game; batch about one minute, score about
one minute; markers in the designed order; a second plan, a second score and a rerun after the seal each refused; no
drawn number in any report file (`evidence/PRELIMINARY_modeh_dress_rehearsal_full_cohort_py315.txt`). The automated
suite covers the same path with two methods; this run adds the full cohort. It is not Windows evidence and not real data.
The released set, the registry and the runner adapters agree at 40 per game (a read-only check of the installed code).
