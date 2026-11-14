# Mode H: the Approval 1 readiness sheet (both games) - DRAFT r2 for the reviewer's focused recheck

**DRAFT r2 (Claude web chat on Fable 5.2, 14 November 2026). Nothing here is authorised and nothing was run or opened.**
r2 applies the reviewer's EX_167 (PASS WITH CORRECTIONS: blocking B01 and B02, nonblocking C01 to C05); section 11 says
where. Written at the project owner's request of 13 November 2026, 22:08. The owner decides after the recheck, one step
at a time. Sources: design v0.1r7 sections 1, 4, 5 and 7; the installed code at `main` (`effc179` for everything Mode H
runs), read line by line; a dress rehearsal on invented data (section 10).
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
- **CATCH_UP is retrospective.** A forecast made after its draw's result was accepted is never prospective evidence. For
  a draw dated after the variant's release date it is catch-up evidence, in its own tier; for a draw on or before that
  date it is development evidence (design 6.4). Neither is ever pooled with prospective evidence, and neither can replace a genuine
  prospective forecast that was not frozen before its draw. So for the variants already released, each draw that passes
  before the weekly session exists (MHUP-B) can later count only as catch-up.
- **The freeze.** From the first Approval 1 until both games are sealed: no MHUP-B install and no change to the frozen
  code or environment (section 7).
- **Q7.** The restriction on raw draw values in the AI chats stays after Mode H. Approved project programs read and score
  them through their controlled interfaces. Aggregate reports are shareable. No rule or enforcement change is needed
  now; the decision goes into the next register edition, and the stale "open" labels (design section 9, H-1, H-2, the
  holdout exposure record) are closed when those documents are next edited.

## 2. What this evaluation can and cannot show

- **What it is:** a precommitted holdout evaluation with N-1 isolation, not pre-draw forecasting. The ten results per game
  have been public since August to October 2026; what keeps them from the methods is the reader, which never decodes the
  target row or any later row. The supported statement is design section 1's: plan, code and environment frozen before
  the holdout was opened; every forecast used only earlier draws; every forecast frozen before any scoring read an outcome.
- **Three separate pre-registered readouts:** Powerball main numbers, the Powerball number, and Oz Lotto main numbers.
  Each is the best of its own family of 80 tracks (40 variants, TOP and WORST picks), fixed in the study manifest before
  opening. Multiplicity is controlled within each family, not across the three: with three families each tested at 5%,
  the chance that at least one flags by chance alone is up to about 15%. Everything else in the report (league tables,
  per-track figures) is descriptive.
- **Ten draws give little power.** My own exact arithmetic, as a guide to scale only; it is not the report's test, which
  computes its own figures (`modeh_scale_illustration.py`; the reviewer recomputed the thresholds). For a track to stand
  out within its family at 5%, it needs at least 25 main-number matches over the ten Powerball draws (fair expectation
  14.0), or 21 over the ten Oz Lotto draws (fair 10.4), or 5 of 10 Powerball numbers right (fair 0.5). That is about 1.8
  to 2 times chance, or ten times for the Powerball number. An edge of 5% would need over a thousand draws to show for
  even one pre-chosen track. So Mode H can reveal only a dramatic effect; it cannot detect a small one.
- **A null result** means "no statistically compelling departure from the fair-draw reference under the reported
  measures". It is not proof of randomness, and it says nothing about methods outside these 12.
- **Expect chance "hits".** The Powerball report counts 2,080 local tests; of the order of a hundred will fall below 5% by
  chance alone. A single low local p-value is not a finding; the family lines are the test. Picking "the best variant"
  from ten draws is exploratory.
- **Exposure flags.** Powerball 1585 and 1586 were displayed in a reviewer chat on 25 October 2026 (HX-1). They are scored
  and counted like any other draw and flagged in the records and the report. Oz Lotto has none.
- **Not frozen, and stated:** the operating system, the hardware, the clock. A method that fails on a target is recorded
  and scored as missing, never rerun.
- **Two separate studies.** The games are never pooled. To avoid a choice made after seeing one result, decide now that
  both games will be run whatever the first shows, barring a technical or safety STOP (section 9, D2).

## 3. The four approvals, per game

| | Powerball | Oz Lotto |
|---|---|---|
| Holdout draws (targets) | 1577-1586 (6 August to 8 October 2026) | 1694-1703 (4 August to 6 October 2026) |
| Cohort | 40 variants, 80 tracks | 40 variants, 80 tracks |
| Families | main numbers; the Powerball number | main numbers (supplementaries are never stored) |
| Exposure flags | 1585, 1586 (HX-1) | none |
| The first update will add | 1577 to the latest published draw (1591 until the draw of 19 November) | 1694 to the latest published draw (1708 until the draw of 17 November) |
| Planned pairs in the batch | 400 | 400 |

| Approval | What it does | Writes | After it |
|---|---|---|---|
| **1** | Freezes the study manifest, then writes the opening record with your typed sentence | the manifest; the opening record (permanent); two search-log rows | the code and environment are locked for this game; the updater's quarantine no longer protects it |
| **2** | The first results update, from Lotterywest-GOV, for this game only | the grab; a backup of version 1; the master (version 2); one ledger row | the holdout draws and every later draw are in the master; the updater refuses for this game until the seal |
| **3** | Freezes the one plan, then runs every variant on each of the ten draws | the plan and its id record; for each of the 400 pairs a frozen forecast or a recorded method failure, with its tickets; `BATCH_COMPLETE` | no forecast can be added or changed |
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

## 5. Before the first Approval 1 (prerequisites, in this order)

Each needs your own separate go; none is authorised by this sheet. Check each "Expect" before the next line; anything
else is a STOP. Begin with `git pull --ff-only` (before the freeze a pull is fine).

1. **The POC rerun** (R-015 (b)): `OWNER_POC_RERUN_R015b_DRAFT.md` (r3). It ends with no orphan marker and the byte-code
   folder absent. It says nothing about the results page (that is prerequisite 3).
2. **The updater's offline self-test** (design 4.4; register future action 4): `Run_Results_Updater.bat --self-test`.
   Expect only `[SELF-TEST] 13/13 PASS`. Any `FAIL` or traceback is a STOP.
3. **The official-page fetch-and-parse check** (EX_167 B01; new in r2; contacts Lotterywest-GOV twice; about a minute).
   `gov_fetch_parse_smoke.py` is a one-off, read-only script outside `src\`. It uses the installed updater's own browser
   fetcher and parser, unchanged, on the nine June and July 2026 draws per game that the real first update will check
   as its overlap, always with the quarantine closed, and compares each parsed draw with your master. It requests no
   date from 1 August 2026 on, writes nothing, takes no lock and prints draw numbers and counts only.
   ```
   cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
   git status --short
   git rev-parse HEAD:exchange/CLAUDE_WEB_TOOLS/modeh_readiness/gov_fetch_parse_smoke.py
   "%CD%\.venv\Scripts\python.exe" -I -B exchange\CLAUDE_WEB_TOOLS\modeh_readiness\gov_fetch_parse_smoke.py
   echo EXIT %ERRORLEVEL%
   git status --short
   ```
   Expect: nothing from the first status; `1cbd32941234661d422c32f53bbf3b5343af2ff7` (the reviewed file; anything else: stop,
   do not run it); then
   ```
   [GOV-SMOKE] POWERBALL: master verified against its ledger (version 1, last draw 1576); read-only
   [GOV-SMOKE] OZLOTTO: master verified against its ledger (version 1, last draw 1693); read-only
   [GOV-SMOKE] POWERBALL: window 2026-05-31..2026-07-31; final address https://www.lotterywest.wa.gov.au; parsed 9 draw(s) 1568-1576; on the weekly date rule 9/9; equal to the master 9/9
   [GOV-SMOKE] POWERBALL: PASS
   [GOV-SMOKE] OZLOTTO: window 2026-05-31..2026-07-31; final address https://www.lotterywest.wa.gov.au; parsed 9 draw(s) 1685-1693; on the weekly date rule 9/9; equal to the master 9/9
   [GOV-SMOKE] OZLOTTO: PASS
   [GOV-SMOKE] PASS: POWERBALL, OZLOTTO: the installed fetcher and parser read the official page as expected. This check wrote nothing.
   ```
   `EXIT 0`; nothing from the second status.
   **STOP criteria:** any exit code but 0; any `REFUSED`, `STOP`, `FAIL`, `VERIFY FAIL` or `ERROR` line; a traceback; a
   line that differs from the above (a weekly-rule count below 9/9 with `PASS` is the one tolerated difference: send it).
   On a STOP: do not rerun (the site is not to be retried casually), change nothing, send me the window. No Approval 1
   follows a STOP. What each means:
   - `ERROR` (exit 4): the browser, its driver or Selenium did not start. Fixed outside the frozen code, before any manifest.
   - `REFUSED: the browser's final URL is ...` (exit 3): the site sent the browser elsewhere. There is no other source.
   - `STOP: ... served a block/challenge page` (exit 2): automation was refused. Nothing is bypassed, now or later.
   - `STOP: results ... did not appear`, `... not found` or `... not where expected` (exit 2): the page's timing or wording
     has changed. This is the fault the check exists to find while the code can still be fixed by a reviewed package.
   - `STOP: ... a quarantined draw appeared on the page` (exit 2): the page showed a result outside the dates asked for;
     the check stopped before reading its numbers. Inconclusive; send it.
   - `FAIL` (exit 1): the page parsed, but not to the expected nine draws, or not equal to the master.
   **What a PASS shows:** on that day the installed browser and parser read 18 known draws from the official page exactly
   as the master holds them. It cannot promise the page is the same at Approval 2, so run it on the day of the first
   Approval 1. It may be run again for Powerball alone (`--games POWERBALL`) before Powerball's Approval 1; it changes
   nothing the freeze protects.
4. **Backups confirmed** of `source_data\` and `results\` (R-015 (c)). The frozen forecasts, the tickets and the score
   ledger are Git-ignored and exist only on your PC, so back up again after each game is sealed, and check the copy.
5. **The tree is the reviewed one** (the last thing before Approval 1):
   ```
   git status --short
   git status --short --ignored src
   git diff --stat effc179 HEAD -- src "*.bat" requirements.txt
   certutil -hashfile source_data\OZLOTTO_results_master.csv SHA256
   certutil -hashfile source_data\POWERBALL_results_master.csv SHA256
   ```
   Expect: nothing from the first status; from the second, nothing or only lines ending `__pycache__/`; nothing from the
   diff (no code file has changed since the install); the version-1 hashes
   `4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f` (Oz Lotto) and
   `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8` (Powerball).
6. **Quiet machine:** nothing of the project running; VS Code's Python terminals and Claude Code closed; no orphan marker
   (`dir transitory_data\poc_runs\UNRESOLVED_ORPHAN.json` gives `File Not Found`).

## 6. The commands (one CMD window at the repository root; one game at a time)

Each line is run only under its own go. Check each output against "Expect" before the next line. There is no time
limit between approvals; a pause of hours or days changes nothing. A review PASS is not a go.

### Oz Lotto (first: section 9, D1)

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

The witness push (section 9, D3; its own go), before Approval 2:
```
git status --short
git add results/real/holdout/OZLOTTO/MODE_H_STUDY_MANIFEST_V1.json source_data/HOLDOUT_OPENED_OZLOTTO.json results/audit/SEARCH_LOG.csv
git diff --cached --name-only
git commit -m "Mode H OZLOTTO: study manifest and opening record (Approval 1)"
git push
git rev-parse HEAD
```
Expect `git diff --cached --name-only` to list exactly those three paths and nothing else (no master, no ledger); if it
lists anything else, stop before the commit. Never `git add -A` or `git add .`. Keep the commit id the last line prints.
If the push is refused, stop and tell me (section 7); do not pull.

**Approval 2 - the first results update** (contacts Lotterywest-GOV; headless Chrome; about a minute):
```
Run_Results_Updater.bat update --games OZLOTTO
```
Expect: `[MASTER] OZLOTTO: checked 9 overlapping draws (all matched), added <n> (1694..<latest draw>), warnings <w>` and
`[MASTER]   grab kept: ...; backup: ...`. The count 9 holds while it is November; `<latest draw>` must be 1703 or later.
A `warning:` line about a date off the weekly rule is information: send it to me before Approval 3.
**Any other result: section 8.2. No rerun of any kind, whatever the tool's own message suggests.**

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
"Done" means each of the 400 planned pairs ended in a recorded way: a frozen forecast, or a method failure that is
recorded, scored as missing and never rerun. To see which, read-only (long output; optional but recommended):
```
Run_Experiment.bat Method_Walk_Forward.py status --game OZLOTTO --batch wf-<the id printed>
```
Expect, for every variant, `"done": 10`, `"pending": 0` and the one attempt state
`DONE: SUCCESS, consumable, under this plan's pins`. A `DONE:` state that names a failure instead (for example
`RUNTIME_FAILURE METHOD_FAILED`) is a recorded method failure: not a STOP, but send me the output before Approval 4.

**Approval 4 - the one score and the report** (about one to five minutes):
```
Run_Evaluation.bat Method_Mode_H.py score --game OZLOTTO
```
Expect progress lines ending `MODE_H_SEALED written; the study is closed`, then
`[MODE-H] SEALED: attempt mh-<32 characters>, batch wf-..., search-log row <n>, <s> score lines, <r> rank lines` and three
`[MODE-H] wrote ...results\method_rankings\OZLOTTO\mode_h_OZLOTTO_1694-1703_mh-....txt` (and `.csv`, `.json`) lines.
If every pair has a forecast, `<s>` is 800 and `<r>` is 400 (the rehearsal's figures); each failed pair lowers them, and the
report names it as missing.

### Powerball (only after Oz Lotto is sealed, and only on its own gos)

**Approval 1 - the manifest and the opening record** (the manifest hashes the code and the whole Python environment; allow
a few minutes):
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

The witness push (section 9, D3; its own go), before Approval 2:
```
git status --short
git add results/real/holdout/POWERBALL/MODE_H_STUDY_MANIFEST_V1.json source_data/HOLDOUT_OPENED_POWERBALL.json results/audit/SEARCH_LOG.csv
git diff --cached --name-only
git commit -m "Mode H POWERBALL: study manifest and opening record (Approval 1)"
git push
git rev-parse HEAD
```
Expect `git diff --cached --name-only` to list exactly those three paths and nothing else (no master, no ledger); if it
lists anything else, stop before the commit. Never `git add -A` or `git add .`. Keep the commit id the last line prints.
If the push is refused, stop and tell me (section 7); do not pull.

**Approval 2 - the first results update** (contacts Lotterywest-GOV; headless Chrome; about a minute):
```
Run_Results_Updater.bat update --games POWERBALL
```
Expect: `[MASTER] POWERBALL: checked 9 overlapping draws (all matched), added <n> (1577..<latest draw>), warnings <w>` and
`[MASTER]   grab kept: ...; backup: ...`. The count 9 holds while it is November; `<latest draw>` must be 1586 or later.
A `warning:` line about a date off the weekly rule is information: send it to me before Approval 3.
**Any other result: section 8.2. No rerun of any kind, whatever the tool's own message suggests.**

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
"Done" means each of the 400 planned pairs ended in a recorded way: a frozen forecast, or a method failure that is
recorded, scored as missing and never rerun. To see which, read-only (long output; optional but recommended):
```
Run_Experiment.bat Method_Walk_Forward.py status --game POWERBALL --batch wf-<the id printed>
```
Expect, for every variant, `"done": 10`, `"pending": 0` and the one attempt state
`DONE: SUCCESS, consumable, under this plan's pins`. A `DONE:` state that names a failure instead (for example
`RUNTIME_FAILURE METHOD_FAILED`) is a recorded method failure: not a STOP, but send me the output before Approval 4.

**Approval 4 - the one score and the report** (about one to five minutes):
```
Run_Evaluation.bat Method_Mode_H.py score --game POWERBALL
```
Expect progress lines ending `MODE_H_SEALED written; the study is closed`, then
`[MODE-H] SEALED: attempt mh-<32 characters>, batch wf-..., search-log row <n>, <s> score lines, <r> rank lines` and three
`[MODE-H] wrote ...results\method_rankings\POWERBALL\mode_h_POWERBALL_1577-1586_mh-....txt` (and `.csv`, `.json`) lines.
If every pair has a forecast, `<s>` is 800 and `<r>` is 400 (the rehearsal's figures); each failed pair lowers them, and the
report names it as missing.

For Powerball the score also reports the Powerball-number family, and the report names the two exposure flags.

## 7. The freeze: from the first Approval 1 until both games are sealed

Every Mode H step re-checks every file under `src\`, every `.bat` in the repository root, `requirements.txt`, the venv and
the base Python installation, and refuses on any difference. So, in that window:

- **Do not** edit, save, add, rename or delete anything under `src\`, or any `.bat` in the root (a new one counts too).
- **Do not** run `install_upgrade_dependencies_into_venv.bat`, `create_venv.bat` or `pip`, or update or repair Python.
- **Do not** install any package (MHUP-B included).
- **Git, allowed:** `git status`, `git log`, `git diff`, `git add <named paths>`, `git commit`, `git push`, `git rev-parse`.
- **Git, not allowed:** `checkout`, `restore`, `reset`, `stash`, `switch`, `clean`, `git add -A`, `git add .`, a re-clone.
  Your working copy holds the installed files with the line endings the install wrote; those commands can rewrite them
  (the content would be the same; the frozen bytes not), and after Approval 2 they could discard the updated master.
- **No pull unless one is needed.** I will push nothing while an approval is in progress, and nothing outside `exchange\`
  at any time. If a pull is needed (your push was refused, or I have sent a reviewed step), first look at what would
  come in:
  ```
  git fetch
  git diff --name-only HEAD origin/main
  ```
  Every path listed must begin with `exchange/`. Only then `git pull --ff-only`. Any other path: stop and tell me.
- **A dirty tree is expected after Approval 2.** `git status --short` will show the game's master and ledger as modified
  (` M`) until you decide their push (D5). That is correct. It is never a reason to reset, restore or clean.
- **Do not** run the updater again for a game between its Approval 2 and its seal (it refuses), and I suggest not at all
  until MHUP-B's checklist exists.
- A refusal for a changed file is recoverable by restoring the exact bytes, as a reviewed step; it is still a STOP.

## 8. An unexpected result

### 8.1 The rule, for every step

Any output other than the expected one is a STOP: do not rerun, do not change arguments, do not edit, move or delete any
file, record, marker or lock (if a tool says "delete the lock by hand" or "rerun with ...", do not); send me the whole
window. Before pasting, glance for draw results (these tools print none by design); never paste the master, grab or
backup files or `mode_h_score_ledger.jsonl`. I propose the next step for that exact state; the reviewer checks it; you
approve it. A STOP in one game is not permission to start the other.

How the Mode H tools stop:
- `[MODE-H] REFUSED: ... Nothing was written by this command.` and `[WALK-FORWARD] REFUSED before any run: ...`: by
  design nothing changed.
- `[MODE-H] FAILED: ... Records written so far stay; a rerun resumes.` and `[WALK-FORWARD] STOP after <n> run(s): ...`:
  stopped part-way; what was done is kept; the designed next step is the same command again, but only after review.
- A launcher line `... no_pycache_ever exists; refusing to run.` (exit 10): the forbidden folder exists.
- A traceback, or a closed window or power cut mid-step: send what you have; do not rerun.

### 8.2 Approval 2, the first update (EX_167 B02)

The update is not one indivisible step. In order, it: checks its refusals; takes its lock; starts the browser; fetches and
parses; **writes the grab file**; compares the overlap with the master; **writes a backup of the master**; **replaces the
master**; **appends the ledger row**; re-verifies; removes its lock. Where it stopped decides what is on disk, and the
message alone does not prove that. Three kinds:

- **(i) Refused before any request** (`[MASTER] REFUSED: ...` naming a precondition: the window, the freeze state, a
  session lock, the updater's own lock; exit 3): by design nothing was written.
- **(ii) Stopped at or after the fetch, before the backup** (`[MASTER] STOP: ...`, `[MASTER] VERIFY FAIL: ...`, or a
  `REFUSED` about the final URL or the overlap): by design the master and ledger are unchanged; a grab file may have been
  added. The first-update admission STOP ("must bring the master to draw ...") is of this kind.
- **(iii) Anything else:** `[MASTER] FILE ERROR`, a traceback, a closed window, a power cut, a lock left behind, or
  success lines that do not match "Expect". The master may have been replaced without its ledger row. The designed
  recovery for that (design 7, A7) is MHUP-B's and does not exist yet.

**For all three the same rule:** no rerun, no wider `--months-back`, no `--browser firefox`, no deletion (the lock
included), no restore from a backup, until the state on disk is known and a step for that exact state has been proposed,
reviewed and approved by you. The tool's own advice to "rerun the same update with a wider --months-back" applies only
to a confirmed admission STOP of kind (ii) with the master and ledger unchanged, and even then only as an approved step.

**The state snapshot** (read-only; its output holds file names and hashes, no draw result; run it straight after any
unexpected Approval 2 result and send it with the window; `<GAME>` is `OZLOTTO` or `POWERBALL`):
```
git status --short source_data
dir /b source_data\.results_master.lock
dir /b source_data\*.part-*
dir /b /o:d source_data\grabs
dir /b /o:d source_data\backups
certutil -hashfile source_data\<GAME>_results_master.csv SHA256
```
Unchanged looks like this: no ` M` line for the game's master or ledger; `File Not Found` for the lock and the `.part-`
file; no backup newer than the run; the master's hash still the version-1 hash of prerequisite 5.

### 8.3 What my cold read found (none changes the code)

- **F-1. The updater's own fetch has never run against the real site.** The masters are at version 1, and `update` has
  refused since the quarantine began. The page itself is not new to the project: the retired two-site checker (v0.7;
  never to be used again, decision TSC-1) read this same results-search page, a month at a time, in late October 2026
  (the several successful fetches you recalled on 14 November; its code shows the same address form and page wording
  that the updater's parser expects). What is untested is the updater's own fetcher
  (one long window, its wait rule, the final-address rule) and the page as it is now. Without a check, the first real
  parse would come after the permanent opening record, with the code frozen: a fault needing a code change would block
  that game. Prerequisite 3 tests the installed fetcher and parser on the real page before any manifest. A blank-page
  browser start (r1's proposal) proved only that Chrome starts and is dropped. One game at a time (D1) limits the harm
  to one game; it does not protect the first. Residual risk, stated: the page could change between the check and
  Approval 2, or behave differently for the longer window to today; the check makes that unlikely, not impossible.
- **F-2. One test module is pinned to the pre-opening files.** `tests/test_multigame_reader_contracts.py` checks the real
  masters' version-1 SHA-256 and pre-opening refusals, so the suite on `main` will stop passing in full once a game is
  opened or updated. Mode H is unaffected (tests are outside the frozen closure and nothing in Mode H runs them). It
  matters for MHUP-B's step 10 and for any suite run on a clone holding the updated masters: a tests-only fix, designed
  with MHUP-B. The step 10 wording "six development data files" (J-1) will also need its MHUP-B edition.
- **F-3. Line endings.** The install copied the package's exact bytes (LF for the code files) into a working copy whose
  other files Git checked out with CRLF; Git has not rewritten them. That is harmless and stable under the Git commands
  section 7 allows. The identity check is prerequisite 5 plus the manifest's "497 files", not a digest prediction.
- **F-4. Two recovery procedures are MHUP-B's and do not exist yet:** the interrupted-update recovery (design 7, A7) and
  the corrective scoring run. Under "Mode H first", either would be written per case, reviewed and approved (8.2).
- **F-5. The orphan marker blocks Mode H too.** Hence the POC rerun before Approval 1, never inside the freeze.
- **F-6. The report is shareable; the score ledger is not.** The three report files hold counts, statistics, draw numbers
  and labels; the writer has no field for a drawn number (decision WF1-10; checked on the rehearsal's invented draws).
  The score ledger records the drawn numbers; it is Git-ignored and stays on your PC.

## 9. Exposure, and the decisions for you after the recheck

**Exposure.** After Approval 2 the master holds the holdout draws and every later draw. The master and its ledger are
tracked by Git: once pushed, every clone holds them (mine, the reviewer's read access, Claude Code's task clones). The
rules do not change: no chat and no runner opens `source_data`, `results` or `transitory_data`; the settings deny those
reads to Claude Code. The later draws that come in with the same update (Powerball 1587 on, with 1587 and 1588 flagged
HX-2; Oz Lotto 1704 on) are not part of Mode H; they are material for the weekly session.

The reviewer's position (EX_167 section 5) is given with each.

- **D1. Order.** Oz Lotto from manifest to seal, then Powerball. Both use the same frozen code and venv, kept unchanged
  until both are sealed. A STOP in Oz Lotto is not permission to go on to Powerball. *Reviewer: agrees.*
- **D2. Both games, whatever the first shows,** barring a technical or safety STOP; still four separate gos per game.
  *Reviewer: agrees.*
- **D3. A witness push** of the manifest, the opening record and the search log (value-free) after each Approval 1 and
  before Approval 2, on its own go, with the commit id recorded. What it is: remote evidence that the study record
  existed before the project first ingested the holdout results. What it is not: proof of time (a commit's own
  timestamps are set by the PC; GitHub's record of when the push arrived is the stronger item, if you note it), and never
  evidence of forecasting before the draws, which were already public. *Reviewer: agrees, with that precision.*
- **D4. The official-page check** (prerequisite 3). Either authorise it, or record in writing that you accept the risk
  that a page change discovered at Approval 2 permanently blocks the first game. I recommend the check: two page loads,
  about a minute, nothing written. *Reviewer: requires one or the other (B01).*
- **D5. The updated masters:** left uncommitted until both games are sealed; backups checked after each seal; the tree
  knowingly dirty meanwhile; any later push of the raw files is its own decision. Value-free records (plan, markers,
  report files) may be committed by name when you choose. *Reviewer: agrees, on those conditions.*
- **D6. How I see the result:** you upload the report's `.txt` file (it is large; upload, do not paste), and preferably
  both games' reports together after both are sealed, so that reading the first cannot colour the second. Never the
  score ledger, masters, grabs or backups. *Reviewer: agrees, with that preference; I adopt it.*
- **D7. Your gos, in order:** the POC rerun; the self-test; the official-page check; the backups and the tree check;
  then Approvals 1, 2, 3, 4 for Oz Lotto, looking at the evidence after each; then the same for Powerball. *Reviewer:
  agrees, with the page check added.*

## 10. Evidence behind this sheet (PRELIMINARY; invented data only)

- `modeh_dress_rehearsal.py`, run on Linux Python 3.15 against a copy of the installed `src\` with its real release
  records: for each game, an invented master, the manifest, the opening record, an invented first update that goes five
  draws past the holdout (as the real one will), the plan with the real runner adapters, the batch and the one score.
  **DRESS REHEARSAL PASS:** 40 variants and 400 of 400 forecasts published per game; batch about one minute, score about
  one minute; markers in the designed order; a second plan, a second score and a rerun after the seal each refused; no
  drawn number in any report file (`evidence/PRELIMINARY_modeh_dress_rehearsal_full_cohort_py315.txt`). It is not
  Windows evidence, not real data, and not a live fetch.
- `gov_fetch_parse_smoke_devtest.py`: the page check run against a stand-in browser object and an invented master (no
  website contacted): 13 of 13 cases, covering the pass, every STOP and refusal listed in prerequisite 3, "no file
  changed" after every case, and "no browser started" on every precondition refusal
  (`evidence/PRELIMINARY_gov_fetch_parse_smoke_devtest_py315.txt`). It proves the script's logic, nothing about the
  real page.
- The released set, the registry and the runner adapters agree at 40 per game (a read-only check of the installed code).

## 11. Where EX_167 was applied

| Item | Where |
|---|---|
| B01 the page check before Approval 1; the blank-page start not called adequate | prerequisite 3; `gov_fetch_parse_smoke.py`; F-1; D4 |
| B02 Approval 2 outcomes; no generic retry | section 8.2; section 6 (Approval 2); F-4 |
| C01 success-only counts | section 3; section 6 (Approvals 3 and 4) |
| C02 the Git boundary in the freeze | section 6 (witness push); section 7 |
| C03 the witness claim | D3 |
| C04 three readouts; catch-up against development evidence | sections 1 and 2 |
| C05 Q7 records; sharing the reports | section 1; D6; F-6 |
| Section 4 (POC) | `OWNER_POC_RERUN_R015b_DRAFT.md` r3 |
| One addition of mine for the recheck | the page check also compares each parsed draw with the master (read through the updater's own verified loader; counts only are printed). It is the comparison the real update makes next. Say if you want it out. |
