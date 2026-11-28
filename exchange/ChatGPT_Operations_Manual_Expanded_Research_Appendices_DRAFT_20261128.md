# Operations manual - the research system

**Proposed edition 2, 28 November 2026.** Written by the Claude web chat from the commands as built and from what they
printed on the owner's PC on 27 and 28 November 2026. Outline agreed by the owner and the reviewer (decision log
entry 401); the reviewer's corrections taken in (entries 403 and 404).
**Status: DRAFT for Claude and owner review. Based on ratified edition 1 (RAT-70, entry 404); only the research appendices and edition/contents lines are amended. Not installed.**

Where it lives: the master is `a_p_r_i_r_DEV\OPERATIONS_MANUAL.md`, kept in Git. Each tree holds the copy last
installed there (by `Create_Tree`, `Install` or `Copy_From_PROD software`), so a tree's copy is the edition it was
given, not proof that every method in it matches DEV.

This is a how-to for the person who runs the system. It says what to type, what you should see, and what to do
when something else appears. It is not a specification: the owner's agreed scientific and operational
requirements are the authority. If this manual and the system disagree, the manual may be wrong or the software
may have a fault: report it and have it resolved, rather than assuming either is right. Every command's full syntax
and options are in **Appendix B**, and only there; the sections give examples.

Contents

- Understanding the system: 0. Start here
- Operating it: 1. After each draw; 2. Reading the results
- Managing it: 3. Changing the software; 4. Methods; 5. New trees; 6. Copying between trees; 7. Backups and
  restoring; 8. Python
- When things go wrong: 9. Messages
- The rest: 10. Standards; A. The system at a glance; B. Command reference; C. Methods list; D. Research ideas and their scientific origins

---

## 0. Start here

**What the system does.** For each game (Powerball and Oz Lotto) it fetches the official results, has every
method forecast every draw from the draws before it only, scores those forecasts, and prints a league table, the
forecasts for the next draw, and two OV-1 series that sum up the evidence. The expected finding is a carefully
measured null: no method predicts better than chance.

**The three trees.** Each is a complete, independent copy of the system with its own software, results, Python
environment and settings.

| Tree | Where | What it is for |
|---|---|---|
| DEV | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV` (inside the Git repository) | where software is written and tested; the only tree with `deploy\` and `tests\`, and the one that runs the commands that touch the other two |
| QA | `T:\a_p_r_i_r_QA` | where new software is tried on real results before PROD gets it |
| PROD | `G:\a_p_r_i_r_PROD` | the production tree: the one run after every draw |

Backups go to `T:\a_p_r_i_r_backups\DEV`, `\QA` and `\PROD`.

**What may move between the trees, and which way.**

| What | Direction | How |
|---|---|---|
| software (engine, updater, methods, launchers, this manual) | DEV to QA, DEV to PROD | `Install.bat`, `Create_Tree.bat` (section 3, 5) |
| results and research data | PROD to QA, PROD to DEV | `Copy_From_PROD.bat` (section 6) |
| software | PROD to QA | `Copy_From_PROD.bat software QA` |
| official results | the website to each tree | each tree's own updater, inside its own job |

Nothing is ever copied into PROD except software, by `Install.bat` (and, once, DEV's accepted results when
`Create_Tree.bat PROD` made it). Settings files are never copied.

**The rules that matter.**

- **Only you run the trees.** Neither AI and not the local runner ever runs anything in DEV, QA or PROD, and none
  of them ever contacts a lottery website.
- **A STOP is a STOP.** Read its message (section 9) before doing anything else. Nothing retries by itself. Most
  stops happen before anything is changed; but an install, copy or restore can fail part way and leave a mix of
  old and new files. Its message, in capitals, then says what state the tree is in, and names the backup it made
  first.
- **Every replacement is backed up first.** If that backup cannot be made, nothing is replaced.
- **One command at a time per tree.** Every command takes the tree's lock, `records\TREE.lock`; a second command
  refuses while it exists (section 9). The exceptions take no lock: `Who_Uses.bat`, which only reads, and the
  environment scripts (`create_venv.bat` and the others), which you run by hand.
- **No command ever ends another process.** Ctrl+C in a window running an install only prints that the job is
  still working.
- **Run commands from a plain command window.** `cd /d` to the tree first. Build a `.venv` only from a window with
  no Python environment active.

---

## 1. After each draw

Powerball is drawn on Thursdays and Oz Lotto on Tuesdays. After either, in PROD:

    cd /d G:\a_p_r_i_r_PROD
    Run_Research.bat

It takes about four minutes when only a draw or two is new.

**Catching up.** Once results are on file, catching up is automatic: the job forecasts and scores every draw that
has no forecast or score, however many. Fetching is not unlimited: by default the updater asks the website for this
month and the five before. After a longer absence its fetch may not overlap what the tree holds, and it then
refuses rather than leave a gap (`the grab does not overlap the master (gap risk); widen --months-back`). Run it by
itself with a wider window, for example `Run_Results_Updater.bat --months-back 11` (up to 60), then
`Run_Research.bat --no-update`.

**What good output looks like.** PROD's first job, 28 November 2026 (a first fill, so it wrote everything; the
progress lines are left out):

    RESEARCH JOB - START - 2026-11-28 11:31 - the PROD tree at G:\a_p_r_i_r_PROD
    About to work: POWERBALL, OZLOTTO
    POWERBALL: fetching new official results with the results updater
    [MASTER] POWERBALL: checked 26 overlapping draws (all matched), added 0, warnings 0
    [MASTER]   grab kept: POWERBALL_grab_draws_1568-1593_as_at_20261128_010202Z.csv
    POWERBALL: results on file through draw 1593; 40 methods in the tree
    POWERBALL: finished. Results on file through draw 1593; written: 15198 forecasts, 15158 scores, 2 series files,
      904 report files. prevailing OV-1: starts at draw 1594; no line yet
    OZLOTTO: fetching new official results with the results updater
    [MASTER] OZLOTTO: checked 26 overlapping draws (all matched), added 0, warnings 0
    [MASTER]   grab kept: OZLOTTO_grab_draws_1685-1710_as_at_20261128_013721Z.csv
    OZLOTTO: results on file through draw 1710; 40 methods in the tree
    OZLOTTO: finished. Results on file through draw 1710; written: 6678 forecasts, 6638 scores, 2 series files,
      478 report files. prevailing OV-1: starts at draw 1711; no line yet
    Backup made: T:\a_p_r_i_r_backups\PROD\PROD_20261128_121921_after_job.zip
    RESEARCH JOB - END - 2026-11-28 12:19 - the PROD tree at G:\a_p_r_i_r_PROD
    The job finished.

After an ordinary draw the counts are small instead: with one new draw, 40 scores and 40 forecasts for that game.

Check three things:

1. Each game's `[MASTER]` line says **all matched**, and `added` is the number of new draws you expected.
2. Each game says `finished`, with `results on file through draw` the newest draw.
3. The last line is **`The job finished.`**

If the last line is anything else, read the warnings above it. **They are repeated at the end** ("said again"),
so you do not have to scroll. The common ones:

| You see | What it means | What to do |
|---|---|---|
| `WARNING: <GAME>: THE RESULTS UPDATER DID NOT FINISH NORMALLY (Stop: results ... did not appear ...)` | a transient failure: the results page did not show the expected draws in time. Nothing was written for that game; nothing more was fetched in that job. The job carried on with the results the tree already had. | **Retry once, by itself, a while later:** `Run_Results_Updater.bat`. If it then adds new draws, run `Run_Research.bat --no-update` (no need to fetch again). If it adds none and the job already finished, nothing more is needed. **If it stops the same way again, stop fetching and report it.** |
| `... (VERIFY FAIL: ...)` | a check failed. When it is that a fetched draw disagrees with the tree's file, or that new draws are not consecutive, the master is unchanged and the fetched grab may have been kept; a check after the new master is in place may fail with the master already replaced. | **Do not retry.** Report it. |
| `... served a block/challenge page; nothing was bypassed` | the website refused the automated browser: a STOP, not a transient failure | Do not retry for a while. Report it. |
| `<GAME>: <method>: its forecast for draw N failed and no line was written` | one method's calculation failed; the others went on | Report it. That method tries again in the next job. |
| `THE BACKUP AFTER THIS JOB WAS NOT MADE (...)` | the results stand, but there is no backup of them | Put the cause right (a full disk, the `T:` drive missing), then `Backup.bat`. |

The job's exit code is 0 when it finished cleanly and 1 when it finished "not cleanly" or a game stopped. Section 9
has every message.

**A real example (28 November 2026).** QA's first job printed the "did not appear" warning for Oz Lotto. QA's
results were not affected: they were the same as DEV's. One retry of `Run_Results_Updater.bat` by itself, at
11:22, said `checked 26 overlapping draws (all matched), added 0` for both games, so nothing more was needed. It was
recorded as a transient fetch failure of unknown cause. PROD's first job, an hour later, fetched both games
normally.

---

## 2. Reading the results

**Where they are.** In each tree, one folder per game:

    <tree>\results\research\POWERBALL\reports\
    <tree>\results\research\OZLOTTO\reports\

Each holds a `README.txt` that names every file. Every report comes as a `.txt` to read and a `.csv` to open in a
spreadsheet. **They are print-outs:** made again by every job, never read back, and an edited file is replaced by
the next job.

| Folder | File | What it is |
|---|---|---|
| `league\` | `league_<GAME>_d<draw>.txt` | every method's record over every draw up to that one; one file per draw |
| `next\` | `next_draw_<GAME>_d<draw>.txt` | what each method forecast for that draw |
| `ov1\` | `ov1_prevailing_<GAME>.txt` | the second OV-1 series |
| `ov1\` | `ov1_exploratory_<GAME>.txt` | the OV-1 series over all scored draws |

The newest league file is the current standing; the newest next-draw file is the forecast for the coming draw.

**The league table.** One row per method, in order of how many of its TOP numbers were drawn **per scored draw**
(the same order as hits above chance per draw; ties in method order). It is a descriptive order: **it selects
nothing**. The columns:

| Column | Meaning |
|---|---|
| `draws` | how many draws the method has been scored on |
| `TOP hits`, `TOP/draw` | how many of its seven TOP numbers were drawn, in total and on average per draw |
| `chance` | what a method choosing at random would average per draw: 49/35 = 1.400 for Powerball's main barrel, 49/45 = 1.089 for Oz Lotto |
| `TOP diff`, `TOP %` | the difference from chance, per draw and as a percentage of chance |
| `WORST ...` | the same for its seven WORST numbers (the ones it thinks least likely) |
| `W#` | its place in the WORST order: the method whose WORST numbers were drawn least often per scored draw is 1 |
| `T-W/draw` | TOP minus WORST per draw: a method that knew something would score above zero here |
| `TOP last`, `WORST last` | the hits of its last ten scored draws, one digit each |
| `PB TOP`, `PB WORST`, `PB chance` | Powerball only: how often its TOP and its WORST Powerball (the separate barrel) was drawn, and how often chance would give |
| `TOP divs`, `WORST divs` | the prize divisions its TOP and WORST sets would have won, as division x times |
| `first`, `before`, `after` | its first scored draw; how many of its scored forecasts were made before the result was on file, and how many after (rebuilt ones) |
| `OV-1 from` | the first draw at which it counts in the second OV-1 series |
| `NF hist`, `NF fail` | draws with no forecast: too little history, or the calculation failed |

"Made before the result was on file" is bookkeeping about this tree's files. It is not evidence that nobody could
know the result.

**TOP and WORST.** For every draw each method ranks all the numbers. Its TOP seven are the ones it ranks most
likely, its WORST seven the least likely, both from the same ranking. If a method were useful, its TOP seven would
be drawn more often than chance and its WORST seven less often.

**The next-draw report.** For the coming draw, each method's TOP and WORST numbers in each barrel. It is a record
of what each method said before the result was on file, not a recommendation.

**The two OV-1 series.** OV-1 combines the methods' TOP and WORST forecasts for the main barrel of each game (not
the Powerball barrel). It measures whether their combined rankings show unusual agreement or disagreement with the
drawn numbers. Six running evidence calculations are averaged to give one score, reported as a certified numerical
lower bound; it is worked out in whole numbers, so every machine gives the same digits. A score near or below 1
means that this combined statistic shows no elevated evidence. It does not rule out an interesting individual
method, or something else.

- **The exploratory series** (`ov1_exploratory_...`) counts every method on every draw it has been scored on.
- **The second series** (`ov1_prevailing_...`) counts each method only from the draw after it was first used in
  that tree, up to the draw it is retired from. So it differs between trees: a tree's second series starts after
  its own first fill. In DEV it starts at Powerball 1592 and Oz Lotto 1709; in QA and PROD at 1594 and 1711. Until
  then it says "starts at draw ...; no line yet". If a method that counts lacks a forecast or a score it needs, the
  series stops at that draw: the job warns `<GAME>: the second OV-1 series stops early: ...` and the status line
  ends `BLOCKED: ...`. Its lines resume once the missing work is done (usually by the next job).

**What "reference line 40" does and doesn't mean.** If successive draws were conditionally fair (every possible
set of seven main-barrel numbers equally likely, whatever came before), and the forecasts and the decisions about
which methods count at each draw were made without knowledge of that draw's outcome or later outcomes, the chance of
this score ever reaching 40 would be at most 1 in 40. Our research does not establish those conditions: methods can
be devised, selected and corrected with knowledge of historical results. **Both series are therefore exploratory
indicators, and 40 is a reference line only. Reaching it is not proof that anything predicts the draws.** Neither
series claims a statistical error bound; each print-out says so.

**If a result looks interesting** (a method well above chance, or a score climbing):

1. Look at how many draws it rests on. A strong showing over a few dozen draws is common by chance alone among 40
   methods.
2. Check it in the second series and on the later draws: does it keep up on draws that came after the method was
   in place?
3. Note it; do not act on it. Anything worked out from it in a chat is "suggestive" only.
4. A real claim would need a separate, pre-registered study on future draws. That is a follow-on project, not
   something this system declares.

---

## 3. Changing the software

All software is written in DEV, in the Git repository, and committed there. It reaches QA and PROD only through
`Install.bat`. The path:

1. **Develop and test in DEV.** In DEV, with DEV's own Python:

       set PYTHONPATH=src;src\methods;tests
       .venv\Scripts\python.exe -B -m unittest discover -s tests -p "test_research_*.py"

   About two minutes, all on invented draws. All 280 pass in the cloud. Three of them need the frozen first
   system beside the tree and are skipped where it is absent (T029, 27 November 2026: 277 passed, 3 skipped).
2. **Run DEV's own job** (`Run_Research.bat --no-update` is enough) and look at its totals.
3. **Flag what is ready:** `Make_Installable.bat ALL INFRA`. A flag records the fingerprint of the files as they
   stand; change a file afterwards and its flag is out of date, so it will not be installed. Commit the flag files.
4. **See what an install would do:** `Install.bat QA --show`. It changes nothing.
5. **Install to QA:** `Install.bat QA`. It backs QA up, replaces what is flagged and differs, then runs QA's own job
   (`--no-update`) and waits for it, however long.
6. **When satisfied, the same for PROD:** `Install.bat PROD --show`, then `Install.bat PROD`.

**How an install can end:**

| It prints | What happened | What to do |
|---|---|---|
| `Nothing to install: ...` (exit 0) | the destination already has everything flagged | nothing: no backup was made and no job run |
| the install lines, then the job's `The job finished.` (exit 0) | done | nothing |
| the install lines, then the job ends not cleanly (exit 1) | the software arrived; the destination's job did not finish cleanly | put right what its warnings say, then in the destination `Run_Research.bat --no-update`. Running `Install` again would find nothing to install |
| a message in capitals (exit 2) | the install itself failed, perhaps part way | follow the message: put the cause right and run `Install` again, or `Restore.bat` the backup it names |

`Copy_From_PROD.bat` ends in similar ways, except that it has no "nothing to install" case: it always copies. If
its copy fails, follow its message; if the copy is done but the destination's job is not clean, run
`Run_Research.bat --no-update` there.

**QA is where you try things, not a compulsory gate.** You may install to PROD without QA; the backup before the
install is the protection.

**What each kind of change makes again,** in each tree, at its next job:

| What changed | What is made again | Time on this PC |
|---|---|---|
| a method's own files | that method's whole history, both games | a small part of a full fill |
| a helper shared by several methods (`_shared\`, a family's core) | every method that uses it (`Who_Uses.bat` lists them) | depends on how many |
| the engine: anything under `src\` outside the methods and the updater | everything, both games | about 49 minutes |
| the updater (`src\updater\`), a launcher (`*.bat`) or this manual | nothing | none |

A rebuild prints one `REBUILD:` line saying why. An engine change deletes the stored results of **both games**,
even in a job run with `--game` for one: the other game is filled by the next job that works it (Appendix B,
`--rebuild-all`). **A changed method starts afresh** in each tree: its
`IN_PLACE_SINCE` is written again, so the second OV-1 series counts it from that tree's next draw. If an old
version's record should stay visible, add the new version as a new variant and retire the old one (section 4).

**Checking a change.** For a change meant to leave results alone (a message, a tidy-up), a job that makes again
what it made before should give the same totals and the same OV-1 values to the last digit: that is how the
progress-line correction of 28 November 2026 was checked. Equal totals are a useful summary, not proof that every
single forecast and score is identical; where it matters, compare the detailed results too. A change meant to
change results (a correction, a new method) needs its own mathematics checked and its own tests; equality with the
old results proves nothing there.

---

## 4. Methods

**Family and variant.** A family (for example `E_009`, exponentially decayed occurrence rates) is one idea. A
variant (for example `E_009/EXP_DECAY_5_6_V1`) is that idea with its settings fixed. Every forecast, score and
report line belongs to a variant, so "method" in the reports means a variant. Appendix C lists all 40.

A variant's folder, `src\methods\<family>\<variant>\`, holds:

| File | What it is | Who writes it |
|---|---|---|
| `method.py` | the variant's entry point | the developer |
| `VARIANT.json` | its title, games, minimum history and the helper files it uses | the developer |
| `I_AM_INSTALLABLE` | its flag: the fingerprint it may be installed at | `Make_Installable.bat` |
| `IN_PLACE_SINCE` | the last draw this tree held when this version was first used here | the job |
| `I_AM_RETIRED` | only if retired: from which draw, and why | `Retire.bat` |

All three small files are kept in Git in DEV. None is copied by `Install.bat` or `Create_Tree.bat`: each tree
keeps its own.

**Adding a method.** Write its specification, then its code and tests in DEV (section 3). The method template in
`doc\METHOD_TEMPLATE\` is being reconsidered: a simplified template, proven boilerplate and a dummy method will be
agreed before the first new method (decision log entry 398). Until then, copy the shape of an existing family.

**Retiring a method.** In DEV:

    Retire.bat E_009/EXP_DECAY_5_6_V1 the reason in a few words

It backs up every tree that has the method, then writes `I_AM_RETIRED` in each, from that tree's own next draw. It
runs no job. Each tree's next job then drops whatever the method held from that draw on; its earlier results stay.
To bring a method back, delete its `I_AM_RETIRED` file.

**What establishment and retirement mean for OV-1.** The exploratory series counts a method wherever it has
scores, up to its retirement. The second series counts it only from the draw after its establishment draw (its
`IN_PLACE_SINCE`) up to, and not including, its retirement draw.

**Which methods use a helper file:** `Who_Uses.bat _shared\occurrence_counts_v1.py`. It only reads.

---

## 5. New trees

As done for QA and PROD on 28 November 2026.

1. **In DEV,** with everything flagged (section 3, step 3):

       Create_Tree.bat QA

   The tree's folder (`T:\a_p_r_i_r_QA`) must be absent or empty. It copies DEV's flagged engine and methods and
   DEV's accepted results, checks the copy against DEV, and writes the settings file last. You should see
   `copied: the infrastructure and 40 methods (157 files), and DEV's accepted results (12 files)` and
   `The QA tree is created.`
2. **Open a new, plain command window,** with no `(.venv)` showing, and in the new tree:

       cd /d T:\a_p_r_i_r_QA
       create_venv.bat
       install_upgrade_dependencies_into_venv.bat

   The second downloads and installs 39 packages and takes a few minutes. Look for
   `No broken requirements found.` and `SUCCESS. All 39 direct requirements installed`.
3. **The first job:** `Run_Research.bat`. It computes everything (about 49 minutes). Its totals should equal DEV's
   for the same results. Its second OV-1 series says `starts at draw ...; no line yet`: that is right for a new
   tree.

If `Create_Tree` prints `THE TREE WAS NOT CREATED`, read the whole message. The settings file is written last, so
normally the folder holds none and is not a tree. Delete that folder by hand only when you have checked that it is
the new folder this command was making, that nothing is running, and that it holds nothing you had before; if in
doubt, keep it and report. Then put the cause right and run `Create_Tree` again.

---

## 6. Copying between trees

`Copy_From_PROD.bat` makes another tree like PROD. It is run in DEV.

| Command | What is replaced | Where |
|---|---|---|
| `Copy_From_PROD.bat software QA` | QA's engine, updater, launchers, this manual and methods, with PROD's `I_AM_RETIRED` and `IN_PLACE_SINCE` files | QA |
| `Copy_From_PROD.bat data QA` | QA's `source_data` and `results\research` | QA |
| `Copy_From_PROD.bat both QA` | both of the above, with one backup and one job | QA |
| `Copy_From_PROD.bat data DEV` | DEV's `source_data` and `results\research` | DEV |

Software never goes to DEV this way: DEV's software is in Git. Nothing goes to PROD.

For `data` and `both`, before touching anything it checks that PROD's results of both games pass the engine's own
reader and that PROD holds what is to be copied; for `software` it needs only PROD's software. It backs the
destination up first. **The one thing it writes in PROD is its lock file,** removed when it ends. Then it runs the
destination's own job (`--no-update`); if that job does not finish cleanly, the copy stands: put the cause right
and run `Run_Research.bat --no-update` in the destination.

**When you would use it:**
- QA has drifted from PROD (trials, a restore) and you want it to be PROD's twin again: `both QA`. QA's job then
  finds nothing to make again.
- You want to develop in DEV against PROD's latest results: `data DEV`.

---

## 7. Backups and restoring

**Three kinds of backup.**

| | Tree backups | Your full-project backup | Your copying script |
|---|---|---|---|
| What | one tree, as a plain ZIP | the whole repository folder as one ZIP, including `.git` (all history), both `.venv` folders and DEV's results | a fresh copy of the repository folder, and a cumulative copy of `T:\a_p_r_i_r_backups` |
| Made by | every job at its end; before every install, copy, retire and restore; `Backup.bat` on demand | your own `backup_a_p_r_i_r.bat` | your own `0-Backup-DO_COPY.bat`, given a destination drive |
| Where | `T:\a_p_r_i_r_backups\<ROLE>\` | `U:`, with checked copies on your USB drives | your other backup drives |
| Checked | written completely before it is given its name; read back whole when restored | read back, and each copy's SHA-256 checked | not checked by checksum |
| Restored by | `Restore.bat` (QA and PROD) | by hand | by hand |

The copying script replaces its copy of the repository folder each time, but it never removes anything from its
copy of `T:\a_p_r_i_r_backups`: tree backups you delete from `T:` stay on those drives. Run it when no job or
backup is running.

A tree backup's name says the tree, the time and why: `PROD_20261201_201012_after_job.zip` (others end
`before_install`, `before_retire`, `before_restore`, `before_copy_from_PROD`, `on_demand`). Any ZIP program opens
one. None is ever written over or deleted by the system; delete old ones yourself when you want the space.

**Restoring QA or PROD.** In DEV:

    Restore.bat PROD PROD_20261201_201012_after_job.zip

It checks that the ZIP reads back whole and that its own settings file names that tree, backs the tree up,
unpacks the ZIP into a fresh folder, renames the tree as it was to `..._set_aside_<date>_<time>` (where nothing can
run) and gives the fresh folder the tree's name. It never deletes the old tree. Then, in a plain window in the
restored tree: `create_venv.bat`, `install_upgrade_dependencies_into_venv.bat`, `Run_Research.bat --no-update`.
Delete the set-aside folder by hand when you no longer want it.

**A tree so damaged that its settings file cannot be read.** `Restore.bat` will not touch it. Rename its folder
by hand to a name that does not end with its role (for example `G:\a_p_r_i_r_PROD_damaged`), then run
`Restore.bat`, which restores into the place that is now empty.

**DEV is not restored this way.** Its software is in Git. Its results come back by `Copy_From_PROD.bat data DEV`,
by running its job (which rebuilds everything from the accepted results), or from your full-project backup.

**Your full-project backup** covers what nothing else does: the Git history on your PC, the `.venv` folders and
DEV's settings and results. Run it with the trees idle (its busy-tree check refuses while DEV's lock exists).

---

## 8. Python

**Rebuilding one tree's `.venv`** (after a damaged environment, or after a restore): from a plain window with no
environment active, in that tree, delete its `.venv` folder, then `create_venv.bat`, then
`install_upgrade_dependencies_into_venv.bat`. A rebuilt `.venv` changes no fingerprint, so no results are made
again. Each tree's environment is independent: the same names do not guarantee the same versions, so compare the
`[DEPS] Installed direct package versions` lists if it matters.

**Changing Python versions.** Get the reviewer's view and your own go first. Then, one tree at a time, DEV first:

1. Make a full-project backup, and in QA and PROD a `Backup.bat`.
2. Note the tree's current totals and OV-1 values (the last lines of its last job).
3. Delete the tree's `.venv`; build it again with the two scripts and the new Python.
4. **In DEV only:** run the test suite (section 3). All must pass, the same three skipped.
5. Run `Run_Research.bat --rebuild-all --no-update`. It makes everything again (about 49 minutes).
6. **Compare with step 2:** the same forecast and score totals, and the same values of both OV-1 series to the
   last digit. If anything differs, stop: do not change the next tree; report it. Where it matters, compare the
   detailed results too (totals alone cannot show that every forecast is identical).
7. Then QA, then PROD, each the same way.

A backup holds no `.venv`, so a tree restored after the change gets its `.venv` rebuilt with the Python then
installed, as every restore does (section 7).

---

## 9. Messages

Messages come in three kinds. A **warning** means the command finished its work but something needs your
attention. A **recoverable failure** means part of the work was not done; the message says what state things are
in, and a retry or a fix will finish it once that state is right. A **STOP or REFUSED** means the command stopped:
a refusal before anything was changed, or a failure part way that may leave old and new files mixed (section 0).
Read the message before anything else; it names any backup made first. Nothing retries by itself.

| Message (start of it) | Kind | Meaning | What to do |
|---|---|---|---|
| `The job finished.` | done | everything finished | nothing |
| `REBUILD: ...` | information | the job is making something again, and says why | nothing; expect a longer job |
| `The job finished, but not cleanly ...` (exit 1) | warning | the updater, a method or the backup did not finish | read the warnings repeated just above it |
| `WARNING: <GAME>: THE RESULTS UPDATER DID NOT FINISH NORMALLY (Stop: results ... did not appear ...)` | recoverable, transient | the website did not show the results in time; nothing written for that game; no more fetching in that job | retry once, by itself, a while later; then `Run_Research.bat --no-update` if it added draws; if it recurs, stop fetching and report |
| `[MASTER] STOP: ... block/challenge page ...` (updater exit 2) | STOP | the website refused the browser; nothing bypassed or written | do not retry for a while; report |
| `[MASTER] VERIFY FAIL: ...` (updater exit 1) | STOP | a check failed: usually a fetched draw disagrees with the tree's file, or new draws are not consecutive | do not retry; report. For those two checks the master is unchanged and the grab may have been kept; a check after the new master was put in place may leave it replaced |
| `[MASTER] REFUSED: ... the grab does not overlap the master (gap risk); widen --months-back` | REFUSED | the tree is further behind than the fetch window | run the updater by itself with a wider `--months-back` (section 1) |
| `[MASTER] FILE ERROR: ... (is a file open in another program?)` | recoverable, but check first | a results file could not be written. It may have happened after the master was replaced and before its ledger line was added | do not simply retry: read the message, look at the master, its ledger and the saved copy in `source_data\backups`, and if they do not agree, report it before anything else runs. The other game's update, if done, stands |
| `[MASTER] REFUSED: ...` (any other; updater exit 3) | REFUSED | a wrong option, or the tree is not right | read it; correct the command |
| `<GAME>: <method>: its forecast for draw N failed and no line was written` | warning | one method failed; the rest went on | report; it tries again next job |
| `THE BACKUP AFTER THIS JOB WAS NOT MADE (...)` | recoverable | results stand; no backup | fix the cause; `Backup.bat` |
| `REFUSED: a process of this tree is running: ...TREE.lock exists` | REFUSED | another command holds the lock, or one was killed and left it | wait. Only if you are sure nothing of that tree is running, delete `records\TREE.lock` by hand |
| `REFUSED: ...` (any other, exit 2) | REFUSED | the folder is not the tree its settings say, a settings file is wrong, the tree's Python is missing, a link instead of a folder, or a command was typed wrongly | read it; it says what to put right; nothing was changed |
| `... is still working and its lock is kept. Waiting for it to end by itself...` | information | you pressed Ctrl+C during an install or copy; the destination's job carries on | wait for it; on Windows Ctrl+C may also reach that job, which then stops by itself, and the command keeps the lock until it has ended |
| `A STOP is a STOP: at least one game did not finish; nothing retries by itself.` | STOP | a game could not be worked | read the warnings above |
| `THE TREE WAS NOT CREATED (...)` | STOP | `Create_Tree` failed part way; normally the folder holds no settings file and is not a tree | follow section 5: delete the folder only after the checks it lists; if in doubt keep it and report |
| a message in capitals from `Install`, `Retire`, `Copy_From_PROD` or `Restore` (exit 2) | STOP | the command failed, perhaps part way, leaving old and new files mixed | it says what state the tree is in and what to do; the backup it made first is named (section 3, "How an install can end") |
| `<GAME>: the second OV-1 series stops early: ...` | warning | a method that counts lacks a forecast or score; the series stops there | usually the next job resolves it; report it if it stays |

**Exit codes** (shown by `echo %ERRORLEVEL%` straight after a command):

| Command | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| `Run_Research.bat` | finished | finished not cleanly, or a game stopped | refused | - |
| `Run_Results_Updater.bat` | done (or nothing new) | a check failed | STOP | refused |
| DEV's commands | done | done, but the destination's job did not finish cleanly (`Make_Installable`: not everything flagged; `Who_Uses`: no method uses that helper, not a failure) | refused, or failed part way | - |

---

## 10. Standards

- **File form:** every text file of the living system is CRLF and ASCII, the `.jsonl` lists included; Git
  converts nothing (`.gitattributes`: `* -text`). See `doc\FILE_FORM_STANDARD_v0_2.md`, as the simple scheme
  changed it. DEV's checker: `deploy\file_form.py`.
- **Coding practices:** `doc\CODING_PRACTICES_v0_1.md`, binding on all code. Every code commit says "coding
  practices met" or lists the exceptions.
- **The science that never changes:** method-facing N-1 (a method sees only the draws before its target), games
  never pooled, TOP and WORST from one ranking. See the scientific sections of
  `doc\Predictive_Randomness_System_Specification_v0_6.md`.
- **The records:** `exchange\DECISIONS\DECISION_LOG.md` holds every decision.

---

## Appendix A. The system at a glance

**A tree's folders.**

| Folder or file | What it holds | In Git (DEV) |
|---|---|---|
| `ENVIRONMENT.ini` | the settings: this tree's role, and each tree's folder and backup folder | no |
| `*.bat` at the root | the launchers (Appendix B) | yes |
| `OPERATIONS_MANUAL.md` | this manual: the edition last installed in this tree | yes (the master) |
| `src\research\` | the engine: reading results, the permitted view, forecasting, scoring, reports, OV-1, the job | yes |
| `src\updater\` | the results updater | yes |
| `src\methods\` | the 40 methods in 12 families, `_shared\` helpers, `_common\` (the methods' shared code) | yes |
| `src\I_AM_INSTALLABLE` | the infrastructure's flag | yes |
| `source_data\` | the accepted results: `<GAME>_results_master.csv`, its ledger, `grabs\`, `backups\` | no |
| `results\research\<GAME>\` | each method's `forecasts.jsonl` and `scores.jsonl` (under `variants\`), the OV-1 series, `reports\` | no |
| `results\research\INFRASTRUCTURE` | the engine fingerprint the results were made with | no |
| `records\` | `TREE.lock` while a command runs; `JOB_LOG.jsonl`, one line per job | no |
| `.venv\` | the tree's Python environment | no |
| `deploy\`, `tests\` | DEV only: DEV's commands and the test suite | yes |

**The fingerprints.** A fingerprint is a SHA-256 over a set of files.
- **The engine's** covers every file under `src\` outside the methods and the updater. A difference from
  `results\research\INFRASTRUCTURE` makes everything again.
- **A method's** covers its own files and the helpers its `VARIANT.json` names. A difference from the first line
  of its stored lists makes that method again.
- **The updater's** and **the root files'** (the launchers, the environment scripts and this manual) decide only
  what may be installed. They make nothing again. So an edit of this manual needs `Make_Installable.bat INFRA`
  and an install to reach QA and PROD; the install still runs the destination's ordinary job, which finds
  nothing to make again. A purely editorial edit can wait for the next ordinary install.

**The job, in order:** take the lock; check the tree is the tree its settings say; fetch with the updater (unless
`--no-update`); find what is out of date and make that again; forecast every draw that has no forecast, the next
draw included; score every forecast whose result is on file; make the league, the reports and both OV-1 series;
add a line to `JOB_LOG.jsonl`; make a backup; release the lock.

---

## Appendix B. Command reference

Syntax: `[ ]` optional, `{ a | b }` choose one, `...` may repeat. Every command works on the tree its file lies in,
and first checks that the tree is the one its settings say. Run each from that tree's folder.

### Run_Research.bat (every tree)

    Run_Research.bat [--game {POWERBALL | OZLOTTO | BOTH}] [--no-update] [--rebuild family/variant ...] [--rebuild-all]

Fetches new results, makes again what is out of date, forecasts and scores, makes the reports and both OV-1
series, logs the job and makes a backup (Appendix A).

| Option | What it does | Where it applies |
|---|---|---|
| `--game` | works one game only; default `BOTH` | every tree |
| `--no-update` | leaves the updater out: works on the results the tree already holds | every tree; used by `Install`, `Copy_From_PROD` and `Restore` for the destination's job |
| `--rebuild family/variant ...` | deletes those methods' results and makes them again | every tree |
| `--rebuild-all` | deletes every stored result **of both games**, and makes again those of the games this job works (about 49 minutes for both) | every tree |

**`--game` with `--rebuild-all`:** `Run_Research.bat --game POWERBALL --rebuild-all --no-update` deletes the stored
results of both games but fills only Powerball; Oz Lotto is filled by the next job that works it. The same happens
after an engine change. Accepted results (`source_data`) are never deleted. For a whole rebuild, normally work both
games.

`--under-lock <key>` also exists: DEV's commands use it to run another tree's job under the lock they hold. Never
type it.

### Run_Results_Updater.bat (every tree; only the owner runs it)

    Run_Results_Updater.bat [--games {POWERBALL | OZLOTTO | POWERBALL,OZLOTTO}] [--months-back n]
                            [--browser {chrome | firefox}] [--pause seconds]

Fetches the last few months of official results from `www.lotterywest.wa.gov.au`, requires every draw the tree
already holds to agree, and appends the new draws to this tree's `source_data`. Keeps what it fetched in
`source_data\grabs` and the file as it was in `source_data\backups`, and adds a line to the game's ledger.

| Option | What it does | Default |
|---|---|---|
| `--games` | which games | both |
| `--months-back n` | how many months before this one to fetch, 0 to 60; widen it after a long absence (section 1) | 5 |
| `--browser` | which installed browser it drives, headless | `chrome` |
| `--pause seconds` | the least time between two pages; may only lengthen it | 2 |

### Backup.bat (every tree)

    Backup.bat

Makes a backup of this tree now, named `<ROLE>_<date>_<time>_on_demand.zip`, in its backup folder. No options.

### Make_Installable.bat (DEV only)

    Make_Installable.bat {family/variant ... | ALL} [INFRA]
    Make_Installable.bat INFRA

Writes the flag `I_AM_INSTALLABLE` with the current fingerprint.

| Argument | What it flags |
|---|---|
| `family/variant ...` | those methods |
| `ALL` | every method |
| `INFRA` | the infrastructure (engine, updater and launchers' fingerprints) in `src\` |

Prints `flagged:` or `already flagged, unchanged:` for each, or `NOT FLAGGED:` with the reason. Exit 1 if
anything named was not flagged.

### Who_Uses.bat (DEV only)

    Who_Uses.bat helper_file

Lists every method that uses a helper file, for example `Who_Uses.bat _shared\recurrence_gaps_v1.py`. Changes
nothing and takes no lock. Exit 0 if some method uses it; exit 1 if none does (not a failure).

### Create_Tree.bat (DEV only)

    Create_Tree.bat {QA | PROD}

Makes a new QA or PROD tree in its folder, which must be absent or empty: DEV's flagged infrastructure, every
flagged method that is not retired, and DEV's accepted results; the settings file last. Then build its `.venv` and
run its first job (section 5).

### Install.bat (DEV only)

    Install.bat {QA | PROD} [--show]

Replaces the destination's infrastructure if it is flagged and differs, and replaces or adds every flagged method
that differs or is missing; backs the destination up first; then runs the destination's own job (`--no-update`)
and waits for it.

| Option | What it does |
|---|---|
| `--show` | prints what would be done; changes nothing; takes the locks |

If nothing is flagged and different it prints `Nothing to install` and makes no backup and runs no job. How else it
can end, and what to do: section 3.

Left alone, and named: a part whose flag is missing or out of date; a helper shared by several methods unless
every method of the destination that uses it is flagged too; a method only the destination has. A retired method
is never added. None of the three small files is copied.

### Retire.bat (DEV only)

    Retire.bat family/variant reason in a few words

Backs up every tree that has the method, then writes `I_AM_RETIRED` beside it in each, from that tree's own next
draw. Runs no job. To undo: delete the file.

### Copy_From_PROD.bat (DEV only)

    Copy_From_PROD.bat {software | data | both} QA
    Copy_From_PROD.bat data DEV

| Argument | What is replaced |
|---|---|
| `software` | QA's engine, updater, launchers, this manual and methods, with PROD's `I_AM_RETIRED` and `IN_PLACE_SINCE` |
| `data` | the destination's `source_data` and `results\research` |
| `both` | both, with one backup and one job |
| `QA` / `DEV` | the destination; `software` and `both` only to QA |

For `data` and `both` it checks PROD's results first. It backs the destination up, copies, then runs the
destination's job (`--no-update`). Writes only its lock file in PROD. How it can end: section 3, after the install
table.

### Restore.bat (DEV only)

    Restore.bat {QA | PROD} backup_file.zip

Puts QA or PROD back from one of its own backups (a name in its backup folder, or a full path). The tree as it was
is renamed aside, never deleted. Then rebuild its `.venv` and run its job (section 7).

### The environment scripts (every tree)

    create_venv.bat
    install_upgrade_dependencies_into_venv.bat [{INSTALL_UPGRADE | INSTALL | UPGRADE | VERIFY}]

| Script or mode | What it does |
|---|---|
| `create_venv.bat` | makes this tree's `.venv`; never overwrites one; refuses while another environment is active |
| `INSTALL_UPGRADE` (default), `INSTALL`, `UPGRADE` | the same operation: upgrades pip, then installs or upgrades all 39 packages |
| `VERIFY` | installs and upgrades nothing; reports what is installed (it may write the package-version snapshot) |

`activate_venv.bat` and `deactivate_venv.bat` exist for working by hand; no command needs them.

### The test suite (DEV only)

    set PYTHONPATH=src;src\methods;tests
    .venv\Scripts\python.exe -B -m unittest discover -s tests -p "test_research_*.py"

All on invented draws; no test lets the real updater run.

---

## Appendix C. Methods list

**Implemented: 40 variants in 12 families,** the same in DEV, QA and PROD. "Needs" is the number of earlier
draws a variant needs before it forecasts (the same for both games). All use the draws as unordered sets. The
lines are short reminders; each family's design note in `doc\` defines it exactly.

| Variant | What it does | Needs |
|---|---|---|
| **E_1 Historical Appearance Frequency** | | |
| `E_001/FULL_HISTORY_RAW_COUNTS_V1` | ranks numbers by how often each has been drawn in all earlier draws | 1 |
| **E_2 Expected Recurrence-Interval Alignment** | ranks numbers by how close the gap since each was last drawn is to its usual gap | |
| `E_002/RECUR_MEAN_ALL_V1` | usual gap = the mean of all its earlier gaps | 104 |
| `E_002/RECUR_MEDIAN_ALL_V1` | usual gap = the median of all its earlier gaps | 104 |
| `E_002/RECUR_MEAN_LAST8_V1` | usual gap = the mean of its last 8 gaps | 104 |
| **E_3 Occurrence-Curve Endpoint Forecast** | fits a curve to each number's recent occurrences and scores its value at the target draw | |
| `E_003/POLY_LS_W52_D2_V1` | least-squares fit, last 52 draws, degree 2 | 52 |
| `E_003/POLY_LS_W52_D3_V1` | least-squares fit, last 52 draws, degree 3 | 52 |
| `E_003/POLY_LS_W104_D3_V1` | least-squares fit, last 104 draws, degree 3 | 104 |
| `E_003/POLY_INTERP_W52_D4_H4_V1` | interpolation through five smoothed points of the last 52 draws, degree 4 | 52 |
| `E_003/POLY_MINIMAX_W52_D2_H4_V1` | minimax fit to the smoothed last 52 draws, degree 2 | 52 |
| `E_003/POLY_MINIMAX_W52_D3_H4_V1` | minimax fit to the smoothed last 52 draws, degree 3 | 52 |
| **E_4 Occurrence-Curve Gradient Forecast** | the same six fits as E_3, scored by the curve's slope at the target draw | |
| `E_004/POLY_LS_W52_D2_V1` | as E_3's, slope | 52 |
| `E_004/POLY_LS_W52_D3_V1` | as E_3's, slope | 52 |
| `E_004/POLY_LS_W104_D3_V1` | as E_3's, slope | 104 |
| `E_004/POLY_INTERP_W52_D4_H4_V1` | as E_3's, slope | 52 |
| `E_004/POLY_MINIMAX_W52_D2_H4_V1` | as E_3's, slope | 52 |
| `E_004/POLY_MINIMAX_W52_D3_H4_V1` | as E_3's, slope | 52 |
| **E_6 Per-Number Fitted Distribution Models** | a Beta-Bernoulli model of each number's chance of being drawn | |
| `E_006/BETA_BERNOULLI_FULL_MEMORY_V1` | every earlier draw counts equally | 1 |
| `E_006/BETA_BERNOULLI_DECAY_74_75_V1` | older draws count less, by 74/75 per draw | 1 |
| `E_006/BETA_BERNOULLI_DECAY_149_150_V1` | older draws count less, by 149/150 per draw | 1 |
| **E_7 Bayesian Frequency Shrinkage** | each number's frequency shrunk toward the overall rate (prior strength 52) | |
| `E_007/BETA_SHRINK_W52_C52_V1` | over the last 52 draws | 52 |
| `E_007/BETA_SHRINK_W104_C52_V1` | over the last 104 draws | 104 |
| `E_007/BETA_SHRINK_FULL_C52_V1` | over all earlier draws | 1 |
| **E_8 Hierarchical Dirichlet-Multinomial Propensity** | propensities pooled across periods of fixed length | |
| `E_008/HIER_PERIODS_P13_V1` | periods of 13 draws | 26 |
| `E_008/HIER_PERIODS_P26_V1` | periods of 26 draws | 52 |
| `E_008/HIER_PERIODS_P52_V1` | periods of 52 draws | 104 |
| **E_9 Exponentially Decayed Occurrence Rates** | occurrence counts with older draws weighted down | |
| `E_009/EXP_DECAY_5_6_V1` | decay 5/6 per draw (short memory) | 1 |
| `E_009/EXP_DECAY_18_19_V1` | decay 18/19 per draw | 1 |
| `E_009/EXP_DECAY_37_38_V1` | decay 37/38 per draw (long memory) | 1 |
| **E_10 Multi-Horizon Frequency Contrasts** | a short-window frequency against a long-window one | |
| `E_010/CONTRAST_S13_L104_V1` | 13 draws against 104 | 104 |
| `E_010/CONTRAST_S26_L208_V1` | 26 draws against 208 | 208 |
| `E_010/CONTRAST_S52_FULL_V1` | 52 draws against all earlier draws | 104 |
| **E_17 Discrete Recurrence Hazard Curves** | the chance of reappearing, by how long a number has been absent | |
| `E_017/HAZARD_BINS_C100_V1` | binned hazard over all earlier gaps (prior strength 100) | 52 |
| `E_017/HAZARD_BINS_W208_C100_V1` | binned hazard over the last 208 draws (prior strength 100) | 208 |
| `E_017/HAZARD_LOGAGE_SIGN_V1` | the sign of the hazard's trend in log absence | 52 |
| **E_18 Mixtures of Recurrence Modes** | gaps modelled as a mixture of four recurrence modes (prior 10) | |
| `E_018/MIX4_ALL_C10_V1` | all earlier completed gaps | 104 |
| `E_018/MIX4_W104_C10_V1` | gaps within the last 104 draws | 104 |
| `E_018/MIX4_W208_C10_V1` | gaps within the last 208 draws | 208 |
| **E_19 Periodic Recurrence-Hazard Peaks** | looks for a hazard that peaks on a fixed cycle | |
| `E_019/PERIODIC_T2_V1` | a cycle of 2 draws | 104 |
| `E_019/PERIODIC_T3_V1` | a cycle of 3 draws | 104 |
| `E_019/PERIODIC_T4_V1` | a cycle of 4 draws | 104 |

The family designs: E_1 and E_6 in their own design notes, E_2 and E_17 to E_19 in the wave 2 design, E_3 and E_4
in the polynomial-fit design, E_7 to E_10 in the wave 1 design (all in `doc\`).

**Catalogued, not built.** The R2 method catalogue
(`doc\Predictive_Randomness_Experimental_Method_Specifications_R2_v0_5.md`, section 7) keeps 62 identities.
These 50 are not built; the catalogue holds each one's profile. Which come next is for the discussion on method
priorities (decision log entries 289 and 398), not for this manual.

| Group | Families |
|---|---|
| The original six | E_5 Shared Population/Draw Distribution Model |
| Frequency, Bayesian and regime | E_11 Change-Point Segmented Propensities; E_12 Hidden Markov Propensity Regimes; E_13 Latent State-Space Drift; E_14 Calendar-Phase Conditional Patterns; E_15 Historical Epoch Hierarchies; E_16 Biased Without-Replacement Urn Model |
| Recurrence and event process | E_20 Self-Exciting or Self-Inhibiting Occurrence; E_21 Cross-Number Recurrence Synchrony; E_22 Lagged Event-Trigger Matrices |
| Within-draw, set structure and drawn order | E_23 Pair Co-Occurrence Propensities; E_24 Higher-Order Triplet Interactions; E_25 Graph-Based Number Association; E_26 Draw-Level Geometry and Summary States; E_27 Nearest Neighbour of Historical Draw Sets; E_28 Markov Transitions of Draw Summaries; E_29 Physical Draw Position Preferences; E_30 Draw-Order Transition Signatures; E_31 Plackett-Luce Sequential Selection; E_32 Permutation/Ordinal Structure of Draw Order |
| Spectral, curve fitting and long memory | E_33 Fourier and Harmonic Occurrence Forecasts; E_34 Wavelet-Localized Cycles; E_35 Singular Spectrum Analysis; E_36 Gaussian-Process Next-Step Curves; E_37 Spline and Local-Polynomial Extrapolation; E_38 Empirical Mode Decomposition; E_39 Detrended Fluctuation and Long-Memory Features; E_40 Nonlinear Phase and Periodicity Maps |
| Information theory and nonlinear dynamics | E_41 Context-Tree and Compression Prediction; E_42 Conditional Mutual Information Features; E_43 Transfer-Entropy Directional Signals; E_44 Recurrence-Plot Analogue Prediction; E_45 Delay-Embedded Nearest-Analogue Forecast; E_46 Local S-Map Nonlinear State Forecast; E_47 Lyapunov-Style Instability Conditioning; E_48 Cross-Mapping of Potentially Connected Processes |
| Machine learning, external signals and ensembles | E_49 Regularized Logistic Event Forecasts; E_50 Random-Forest Conditional Patterns; E_51 Boosted-Tree Interaction Discovery; E_52 Reservoir Computing for Latent Dynamics; E_53 Evolutionary Symbolic Regression; E_54 External-Date Covariate Synchrony; E_55 Complementarity-Aware Multi-Method Combination; E_56 Adaptive Temporal Method Mixtures |
| Pilot-wave (de Broglie-Bohm) inspired | E_57 Fixed-Size Determinantal Seven-Set Model; E_58 Unconditioned Coupled Latent-Wave Field; E_59 Draw-Conditioned Coupled Latent-Wave Field; E_60 Post-Change Non-Equilibrium Relaxation Analogue; E_61 Guided-Particle Circulation Model; E_62 Guided-Particle Circulation with Reinjection |

**Additional research leads, provisionally numbered.** The owner requested identifiers even for leads not
yet specified, and placed NL-means last. E_1-E_62 are the existing R2 catalogue; the following E-identities
are temporary labels for discussion, not ratified additions to R2, implementation permission, or an agreed
order among the other investigations. Appendix D preserves their origins and detail.

| Provisional ID | Research lead | Status |
|---|---|---|
| E_63 | Constrained free-beta field | Pilot-wave (de Broglie-Bohm) inspired; unbuilt, to specify |
| E_64 | Regularised wave-node motion | Pilot-wave (de Broglie-Bohm) inspired; unbuilt, to specify |
| E_65 | Independently noisy positions | Pilot-wave (de Broglie-Bohm) inspired; unbuilt, to specify |
| E_66 | Two-dimensional torus | Pilot-wave (de Broglie-Bohm) inspired; unbuilt, to specify |
| E_67 | Cross-barrel field coupling | Pilot-wave (de Broglie-Bohm) inspired; unbuilt, to specify |
| E_68 | Full configuration-space / entangled wave | Pilot-wave (de Broglie-Bohm) inspired; unbuilt, to specify |
| E_69 | Topological data analysis / persistent homology | Historical GAIS lead, deferred; not yet a planned experiment |
| E_70 | Algorithmic information / normality in multiple bases | Historical GAIS lead, previously set aside; related to E_41, not yet a distinct specified experiment |
| E_71 | Pattern-spotting by non-local means (NL-means) | Deferred, R-002; last, by the owner's direction |

The owner's Method A is already represented by E_17 (log-age variant installed); retain its wider recurrence-gap
research. Method B belongs to E_45, including its proposed forbidden ordinal patterns investigation (R-001).
Neither needs a duplicate number. Other variants within an existing family retain that family's identity until a
distinct hypothesis is specified. A catalogue entry is not a priority, except that the owner explicitly places
NL-means last among the research ideas. Temporary labels must be reconciled with R2 before implementation.

---

## Appendix D. Research ideas and their scientific origins

This appendix preserves the substantive research record, with the source mathematics, distinctions and open
questions, including ideas not yet given permanent method numbers. It is a research reference, not an
operational procedure, ratification of a new method, or authority to develop one. The source papers remain
retained and authoritative in their proper scope; the current ratified scientific and operational requirements
take precedence over historical proposals. The two games remain separate, with legal outputs appropriate to
each game and barrel, strict N-1 method-facing history, and TOP/WORST from the same ranking. Both OV-1 series are
exploratory. Historical Powerball-only sample sizes, estimates, proposed diagnostics, holdout language, and
operational arrangements in source extracts below are historical, not newly adopted obligations; adapt any
future implementation to the current system and both games. No predictive advantage or physical mechanism is
established by the analogies. Synthetic research, where useful, is separate from real data and never a gate.

### D.1 Pilot-wave (de Broglie-Bohm) inspired research: E_57-E_62

The six numbered families and the six additional leads below originate in R1 v0.4 section 4.7:
`doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md`. The following is the complete substantive
section, retained in ASCII form (typographic substitutions only, heading levels adapted). R1 is a historical
research catalogue; its provisional designs are not implementation specifications. E_57-E_62 remain unbuilt.
The source's original Powerball examples do not restrict eventual separate Oz Lotto designs.

#### 4.7 Pilot-wave / de Broglie-Bohm-inspired mathematical family - accepted/provisional for R1 (E_57-E_62)

**User decision:** all four proposed C-PW1-C-PW4 candidates were added without exclusions; the subsequent guided-trajectory family E_61 and E_62 is also provisionally accepted with mathematical corrections. All preceding numbered experiments remain untouched. They are **analogy-inspired modelling experiments**, not assertions that the lottery machine exhibits quantum wave functions or Bohmian trajectories. The shared provenance of these ideas is scientifically interesting but cannot by itself confer predictive validity. This distinction is about the strength of the *claim*, not a rule for excluding a heterodox experiment.

**Physics background and interpretation.** de Broglie-Bohm theory describes particles with definite trajectories guided by a wave function. Quantum equilibrium can yield Born-rule statistics and an associated notion of absolute uncertainty [S27]. Valentini investigated non-equilibrium distributions and relaxation toward Born-rule statistics [S28]. The existence of these physical theories does **not** supply a measured pilot wave for the draw apparatus. These papers inspire precise mathematical *structures* worth testing on lottery histories. Determinantal point processes (DPPs) and tensor-network Born machines have independent mathematical/machine-learning literatures [S29, S30]. Neither is a validated physical explanation for lottery balls.

**Scope:** the primary sample is unchanged (Draw 1144 onward, seven distinct main numbers from 35 plus one Powerball from 20). The sequence preserved in the Lotterywest-derived CSV is **operator-labelled drawn order**, supported by The Lott's documentation (section 1.1a). Ordered likelihoods may be used where a model truly specifies sequential sampling, with the choice of ordered versus unordered observation governed by a common R2 policy. The evidence does not provide independent filmed verification for every historical draw, and no old-rule draws are used.

##### E_57 - Fixed-Size Determinantal Seven-Set Model (C-PW1; Fermion-Style Diversity)

- **Family / inputs:** Quantum-inspired set probability and subset repulsion; `U` main-barrel sets. **Development effort:** H; in-memory 35x35 linear algebra is feasible, but valid learning and probability computation require care.
- **Hypothesis:** the propensity of a *whole* seven-number set may contain structured pairwise exclusion/diversity beyond the combinatorial fact of seven unique numbers. This allows a legal set-level forecast, unlike independent Bernoulli picks.
- **Mathematical construction:** let `L` be a real positive-semidefinite 35x35 matrix. For any seven-element set `S`, define the **fixed-size L-ensemble DPP**:

  `P(S | |S|=7, L) = det(L[S,S]) / Z_7(L)` where `Z_7(L) = sum_{|T|=7} det(L[T,T])` (equivalently the seventh elementary symmetric polynomial of the eigenvalues of `L`).

  Taking `L = I` yields **exactly uniform probability for every legal seven-set**: `1 / C(35,7)`. A diagonal unequal `L` controls item propensities; off-diagonal entries describe similarity and lead to diversity/repulsion **subject to the positive-semidefinite requirement** [S29]. The sample-size constraint itself also introduces negative association, so reported repulsion must not be conflated with mere sampling without replacement.
- **Proposed next-draw output:** full seven-set score/probability; optionally per-number inclusion marginals for compatibility with ranking-based experiments. For a joint draw, select the Powerball via an independently defined one-of-20 model or a separately registered combination method. The Powerball barrel has no interesting seven-set DPP analogue when only one number is drawn.
- **Experiment families / controls to discuss at R2:** identity `L`, diagonal `L`, low-rank-plus-diagonal `L`, constrained similarity features, rolling parameter fits, and comparisons against E_16, E_23-E_24 and E_31. Preserve each variant's identity, regardless of correlation.
- **Critical technical limits:** a standard DPP is *repulsive*; it cannot represent all forms of positive co-selection attraction, and the fixed-size constraint complicates interpretation. An unrestricted 35x35 matrix has far more flexibility than a 444-draw history can identify reliably. Use explicit parameterisation and regularisation as *implementation choices*, not as exclusion gates. Ordinary NumPy/SciPy are potential dependencies; no new package needs installation at the R1 stage.
- **Evidence status:** DPP mathematics is established [S29]; its claimed advantage on Powerball is **unverified**. The quantum/fermion analogy establishes no physical mechanism.

##### E_58 - Unconditioned Coupled Latent-Wave Field (C-PW2)

- **Family / inputs:** Latent field, complex amplitudes, coupled oscillations; `U`, with optional covariates only as a separately declared variant. **Development effort:** H.
- **Hypothesis:** a hidden shared dynamical state may contain coupled, phase-dependent temporal structure that can be inferred from past draws and extrapolated, even where each individual number's history is weak.
- **Provisional construction:** define a 35-component complex state `psi_t` and a norm-preserving evolution `psi_(t+1) = U psi_t`, with `U` a constrained unitary matrix (a separate 20-component state for Powerball, if used). Number-specific *weights* are `w_i(t) = |psi_i(t)|^2`. The coupling and phases can create interference-like patterns and common spectral components. A fixed evolution matrix makes norm conservation precise; a time-varying rule would need its own declaration.
- **Crucial sample-space requirement:** `sum_i |psi_i|^2 = 1` describes **one categorical choice**, not a seven-without-replacement selection. To generate seven main numbers, **an explicitly specified legal fixed-size selection rule is mandatory**: e.g., sequential probability-proportional-to-weight sampling without replacement, or a set-level kernel derived from the weights. These options are mathematically distinct variants with distinct probabilities. Multiplying `|psi_i|^2` by seven is **not generally a valid inclusion-probability formula**, since an entry can exceed one and the dependence among seven choices is not defined. A Powerball-only amplitude state directly supports a one-of-20 categorical distribution.
- **What 'unconditioned' means:** given previously fitted initial state and evolution parameters, the latent field evolves without an additional draw-by-draw *state correction*. Past draws are used for **historical model fitting**, so this is not a claim that observed results are ignored entirely. It is also **not** a physical reproduction of Bohmian guidance.
- **Proposed testable output:** next-draw seven-set score/marginals and Powerball score, with explicit comparison against E_33 and other harmonic models whose oscillations are per-number rather than coupled. Record whether measured apparent improvements are due to coupling or merely the added flexibility of a larger parameter family.
- **Model capacity:** a free dense complex coupling model is strongly underconstrained by ~444 historical draws. Consider a sparse/neighbor-coupled, low-rank, banded or few-mode version for an initial *implementation*, but retain unconstrained versions as research leads rather than deleting them. NumPy/SciPy are candidate dependencies.
- **Evidence status:** Schrodinger-style amplitude mathematics and Born-type generative modelling exist [S30]; their **proposed time-evolving use here is a project-specific construction**, not a direct published recipe for forecasting lottery draws.

##### E_59 - Draw-Conditioned Coupled Latent-Wave Field (C-PW3)

- **Family / inputs:** Latent dynamics with observation-conditioned state update; `U`. **Development effort:** H.
- **Hypothesis:** observed draw outcomes might provide information that updates an underlying hidden-field state, and that update could improve next-draw prediction over the unconditioned propagation in E_58.
- **Provisional construction:** start with the constrained field and legal fixed-size observation likelihood in E_58. At each completed draw `t`, update a filtered estimate of the hidden state using **only the observed draw available by t**; propagate that posterior/filtered state to make the forecast for `t+1`. An observation-conditioned Bayesian update, measurement-like map or learned state-space filter are possible **distinct, versioned variants**. This is an *analogy* to conditioning and does not claim that a lottery observation physically collapses a Bohmian wave function.
- **Proposed outputs:** one-step-ahead seven-set and Powerball rankings or probabilities; a direct paired comparison with E_58 that isolates the contribution of observation conditioning.
- **Critical constraints:** the next target draw must **never** enter its own latent-state filter or initialisation. A freely learned update rule may memorize the history; specify parameter counting, regularisation and temporal fitting windows at R2. If an update breaks state normalisation or the seven-set sampling rule, re-normalisation and legal-set probabilities must be explicitly defined.
- **Evidence status:** observation-conditioned hidden-state methods are legitimate; the wave-labelled adaptation and claimed predictive potential remain speculative and untested.

##### E_60 - Post-Change Non-Equilibrium Relaxation Analogue (C-PW4)

- **Family / inputs:** Transient non-stationarity, change-point and decay models; `U`, optional `X` for **documented, time-available** equipment, ball-set or maintenance events. **Development effort:** M/H.
- **Hypothesis:** a process may exhibit a transient deviation in selection propensities after a change and subsequently relax toward a reference pattern. Motivated by non-equilibrium relaxation analogies in pilot-wave theory [S28], but **not** asserted to be a quantum process in a lottery machine.
- **Provisional mathematical structure:** for ball `i` after an epoch-start or independently documented event `t0`, define a time-dependent deviation such as `delta_i(t) = A_i exp(-(t-t0)/tau_i)`; combine this with a valid probability model for seven-number sets and a separate model for Powerball. Other decay laws (stretched-exponential, oscillatory decay, regime mixtures) may become named variants. The reference tendency need **not** be assumed uniform in all variants.
- **No equipment-data barrier:** first examine **observable** dates within the same-rule period (including the 19 April 2018 rule/equipment transition) as explicitly declared epochs; independently documented apparatus events can improve interpretation if available, but are optional. The primary same-rule dataset has no preceding observations under the *same* conditions before Draw 1144, which limits what an initial-transient model can claim. A variant may infer latent change points using only historical data available at each forecasting origin. Never use a post-event future draw to select a past change point for that forecast.
- **Proposed outputs:** next-draw propensities conditioned on time since a declared/inferred event, plus diagnostic estimates of whether and how a transient changes. Compare with E_11 and E_15, retaining all even if very correlated.
- **Evidence status:** Valentini studies relaxation toward equilibrium in a pilot-wave context [S28]; exponential decay of *lottery draw-number bias* is an **independent speculative hypothesis**, not a result established by that paper. Without documented event metadata, causal claims about equipment are not warranted.

##### 4.7.1 E_61 - Guided-Particle Circulation Model (C-PW5A; provisional)

**Research character:** deliberately speculative but mathematically operational hidden-trajectory model, inspired by the form of Bohmian guidance rather than by observed quantum physics in a lottery machine. **Applicability:** real observed same-rule Powerball draws, separately for 35 main-number particles and 20 Powerball particles. Artificial datasets are only additional, separately reported diagnostics.

**Hypothesis.** Each number labels a particle at an unknown position on an abstract one-dimensional circular ring. All particles move under a common time-dependent complex guiding field. A fixed capture region favours particles near it at the next draw. Historical draws provide indirect evidence about latent positions; in the reference variant, they do not physically alter the guiding field or particles. This may yield shared oscillations, persistent neighbours, attraction/co-occurrence, linked recurrence, and a **fixed latent cyclic ordering** despite apparently irregular observed numbers. Nothing asserts that lottery balls literally follow a quantum pilot wave.

**Proposed state and dynamics (reference):** at a draw time `t` each number `j` has hidden position `theta_j(t)  in  [0, 2pi)`. For a small truncation `K` (initial candidate `K  in  {1,2,3}`):

```text
psi(theta,t)     = sum[k=-K..K] c_k * exp(i*(k*theta - alpha*k*k*t))
normalisation    = sum[k=-K..K] |c_k|^2 = 1
reference        = |c_0| > sum[k!=0] |c_k|  ; psi is nowhere zero
reference beta   = 2*alpha ; epsilon = 0
v(theta,t)       = beta * Im(conj(psi)*dpsi/dtheta) / |psi|^2
dtheta_j / dt    = v(theta_j,t)
```

The dominant-constant-mode condition is **sufficient, not necessary** for avoiding zeros. It makes the exact reference mathematically well-defined. The `beta = 2*alpha` condition matches the continuity equation for this free-wave dispersion and yields **Bohmian-form equivariant transport** without the previous `epsilon` regulariser. With `epsilon > 0`, or freely chosen `beta`, this is a valid alternative **regularised or generic guided-flow** model but should not be called exactly Bohmian. Coefficients with wave nodes are not forbidden research ideas; they require an explicit different treatment. A single nonzero Fourier mode gives constant-velocity rotation; `K = 1` **does not** imply rigid rotation because modes `-1,0,+1` can interfere. Equal-magnitude counter-propagating modes may yield a zero-current standing wave; report frozen dynamics as a possible fitted outcome, never automatically as a discovery. The above one-dimensional smooth, periodic deterministic system should **not** be advertised as a chaos detector; two-dimensional variants are a distinct research question.

**Selection and legal draw rule.** Let `theta_c = 0` fix the rotational reference. Give each particle positive weight `w_j(t) = exp(kappa*cos(theta_j(t) - theta_c))`, then draw **seven different main labels without replacement**, sequentially according to the remaining weights. For Powerball, draw **one of 20** by its normalised weight, in an entirely separate model. With `kappa = 0`, the seven-set model is exactly uniform regardless of the hidden dynamics. A separate Born-style variant is `w_j = |psi(theta_j,t)|^(2*kappa)` where well-defined. These are operational *weight functions*, not proof of quantum mechanics. The sequential weighted model and E_57's fixed-size determinantal model are **not equivalent**, including when E_57's matrix is diagonal.

**Observational likelihoods.** For a genuine observed ordered sequence `a_1,...,a_7`, the sequential model assigns:

```text
P(a_1,...,a_7) = product[r=1..7] w_(a_r) / sum[j not in {a_1,...,a_(r-1)}] w_j
```

For the unordered seven-set `S`, sum this expression over the `7!` possible orders; a validated Wallenius noncentral-hypergeometric integral is a possible computational alternative. The Lotterywest sequence is supported as **operator-labelled drawn order** by The Lott documentation (section 1.1a). The unordered and ordered observational likelihoods are both legitimate model options wherever mathematically compatible. R2 shall define one common data-use and provenance rule covering both, and models must record which likelihood was used. This does not assert independent video confirmation of all historical sequences. The single Powerball likelihood is a normalised 20-class weight. All seven-number outputs remain legal and all probabilities normalised.

**Inference and forecasting.** Fit field coefficients, dispersion, capture sharpness and latent positions **only on historical observations available before each forecast target N**. Integration may use validated substepped ordinary differential equation solvers. Avoid naive 35-dimensional particle filters as a presumed solution: sample degeneracy and static-parameter estimation are material risks. Examine sliding/windowed fitting of latent initial positions and parameters by multistart optimisation, Markov chain Monte Carlo, resample-move or advanced sequential Monte Carlo; warm-start updates are allowed only from preceding forecasts. N-1 temporal boundaries, optimiser randomness and model version are recorded. Produce full 35-number inclusion ranks, top seven, one-of-20 Powerball ranks, and optional legal joint-set probability or score. Fitting and predicting are separate timed operations.

**Falsifiable signatures:** (i) a single latent cyclic order persists under smooth deterministic shared flow, (ii) nearby hidden neighbours can co-occur, allowing **attraction-like** patterns that E_57's repulsion model does not directly express, (iii) coupled recurrence intervals and short-lag persistence, (iv) any fitted circulation/phase pattern may transfer to a future forecast. A fitted latent ordering is defined only up to ring rotation and other justified symmetries; that must be accounted for before judging recovery.

**Noise and dimensionality:** the initial reference is **zero independent particle noise** to preserve ordering. A shared stochastic disturbance or capture-port jitter could preserve ordering in a specified model. Independent particle noise may permit crossings and therefore becomes a versioned, separately reported variant. Two-dimensional torus and cross-barrel field coupling are retained *leads* without being assumed as part of this reference method.

**Synthetic identifiability diagnostic, not eligibility gate:** on artificial histories produced by the model, assess (a) hidden ordering and parameter recovery subject to symmetries, (b) actual forecast quality, (c) repeatability, (d) sample-size sensitivity, and (e) resource requirements. Synthetic fitting states and records must remain outside real-data fitting. **Failure to recover synthetic truth or forecast the model's own artificial data cannot bar a real-data run or delete the method**; it informs interpretation and suggests additional model variants. If a real-data model forecasts well while synthetic self-recovery fails, explicitly report that its stated hidden-particle explanation is unsubstantiated by the recovery diagnostic.

**Challenges:** initial hidden-order configuration has vast combinatorial freedom; optimisation may be expensive, many parameterisations may be observationally equivalent, and apparent arcs may emerge by chance. Maintain a fixed and versioned inference budget rather than opportunistic retrospective changes. Exact runtime and feasibility are **unknown until benchmarked**, with the same agreed method-retention rights as all other E-methods. NumPy and SciPy are probable baseline packages; further numerical acceleration only if benchmarked.

##### 4.7.1a E_62 - Guided-Particle Circulation with Reinjection (C-PW5B; provisional)

**Purpose:** a distinct real-data forecasting hypothesis based on E_61's mathematical framework, but permitting draw outcomes to **alter the subsequent hidden state**. Selected particles undergo a prespecified repositioning or reinjection rule after the draw (for example to a re-entry arc or phase distribution); unsampled particles continue under the field. This explicitly tests historical feedback, rather than E_61's observation-only conditioning.

- **State transition:** define the reinjection rule *before* observing a target draw, including whether it preserves or changes the latent cyclic order. No fixed-order assertion survives automatically when reinjection crosses other particle positions.
- **Selection:** maintain legal main seven-without-replacement weighted draws and single-ball Powerball selection, with separate barrel systems, null nesting at `kappa = 0`, and both unordered and explicitly labelled operator-drawn-order likelihood options governed by the common R2 policy.
- **Inference:** adapt E_61's sliding/warm-start inference to the fact that the latent transition now depends on past observed outcomes. Every target N must use only draws through N-1; data assimilation is not hindsight access to target N.
- **Predictions:** ranks, valid main seven-set and Powerball choices, probability/score metadata and an explicit comparison with E_61 while preserving both permanent method identities.
- **Distinct predicted effects:** reinforcement, depletion, reinjection delays, recurrence shifts and potentially changing latent adjacency. Which occur depends on the frozen reinjection rule, not the quantum-inspired label.
- **Versions retained:** reinjection location/distribution, timing, shared versus independent noise, dimensionality and coupling can produce separately tracked variants, with model-definition changes disclosed.
- **Synthetic diagnostics:** self-recovery and planted-effect studies may refine engineering and interpretation but **never** substitute observations or synthetic fitted states into a real historical forecast or act as a hard eligibility gate.
- **Resource and dependencies:** potentially as expensive as or more expensive than E_61; benchmark before committing to computational schedules. Full-window estimation and complex state filtering may require later acceleration, not mandatory at R1.

##### 4.7.1b Remaining pilot-wave-inspired research leads, not deleted

The constrained free-`beta` field, regularised wave-node motion, independently noisy positions, two-dimensional torus, cross-barrel coupling, and full configuration-space/entangled wave remain separate *research leads*. Their unnumbered state is not a rejection or a reason to give them less evidentiary consideration; assign new stable E-identities when sufficiently specified. The original unrestricted guided-trajectory concept has been realised provisionally by E_61/E_62, rather than falsely retained as if still undefined.

##### 4.7.2 Distinctions to preserve in R2/R3

1. **Do not infer a mechanism from a fit.** A fitted DPP, coupled oscillation or post-event relaxation is a statistical claim about recorded observations, not evidence that de Broglie-Bohm theory governs the draw mechanism.
2. **Avoid a false equivalence with Pauli exclusion.** Drawing seven distinct lottery balls is sampling without replacement; fermionic antisymmetry motivates a *mathematical* analogy only.
3. **Keep outcome constraints exact.** Seven unique main balls, one Powerball, legal ranges and valid probability normalisation hold for every candidate claiming full probabilities. Candidates may still output non-probability scores if that is explicit.
4. **Keep the original experiments and correlated methods.** E_57 may be related to E_16/E_23; E_58/E_59 to E_33/E_52; E_60 to E_11/E_15. Similarity is a reporting variable, never a veto or reason to discard a model.
5. **Preserve separate synthetic and real observations/outputs.** Synthetic research may inform feasibility, model construction, method priority, debugging and interpretation, provided it is declared. Synthetic generated draws, synthetic fitted states and synthetic-only result scores must never be substituted into real predictive fitting or represented as real-data performance. Method retention and real-data eligibility never depend on passing synthetic diagnostics.
6. **Keep the implementation order flexible.** Inclusion of E_57-E_60 is accepted and E_61/E_62 are accepted provisionally for R1. We may discuss order based on software dependencies, testability or user preference, but **not** exclude an idea because accepted physics would predict no advantage.

---

**R1 bibliography for this family** (source reference labels retained):

- **[S27]** Durr, Goldstein & Zanghi (1992), *Quantum Equilibrium and the Origin of Absolute Uncertainty*, *Journal of Statistical Physics* 67, 843-907 - https://doi.org/10.1007/BF01049004 ; accessible manuscript https://arxiv.org/abs/quant-ph/0308039 . Relevant for physical interpretation and its constraints, not lottery forecasting.
- **[S28]** Valentini (1991), *Signal-locality, uncertainty, and the subquantum H-theorem. I*, *Physics Letters A* 156, 5-11 - https://doi.org/10.1016/0375-9601(91)90116-P . Establishes a theoretical non-equilibrium / relaxation proposal in pilot-wave foundations; it does **not** study mechanical lottery equipment.
- **[S29]** Kulesza & Taskar (2012), *Determinantal Point Processes for Machine Learning*, *Foundations and Trends in Machine Learning* 5, 123-286 - https://doi.org/10.1561/2200000044 ; https://mlanthology.org/ftml/2012/kulesza2012ftml-determinantal/ . Establishes DPP subset-diversity mathematics and tractable operations.
- **[S30]** Han, Wang, Fan, Wang & Zhang (2018), *Unsupervised Generative Modeling Using Matrix Product States*, *Physical Review X* 8, 031012 - https://doi.org/10.1103/PhysRevX.8.031012 . Demonstrates Born-rule-inspired generative modelling; **not** the time-varying coupled field proposed for E_58/E_59.

### D.2 Provisional identities for the remaining pilot-wave leads

R1 section 4.7.1b names all six separately but supplies no finished specifications. The following explanations
expand the original short titles using the neighbouring E_61/E_62 discussion; they are interpretations and
questions for design, not claims that the mathematical or inference choices have already been settled.

**E_63 (temporary) - Constrained free-beta field.** R1's exact node-free ring reference has dispersion alpha
and beta = 2*alpha. Investigate beta chosen independently within a declared constrained model. The reference
velocity is beta*Im(conj(psi)*dpsi/dtheta)/|psi|^2; changing beta alters the relation to the continuity equation.
Specify permissible coefficients, beta range, identifiability and comparison with the reference. Do not claim
exact Bohmian equivariance when its conditions fail. Keep a uniform-selection control.

**E_64 (temporary) - Regularised wave-node motion.** Relax the reference sufficient condition
|c_0| > sum[k!=0]|c_k| and investigate nodes, near-zero amplitudes and possible regularised guidance, e.g.
denominator |psi|^2 + epsilon with a declared epsilon > 0. The treatment of singular velocities, integration
accuracy, boundary conditions, and the effect of regularisation on equivariance remain open. This is a
distinct mathematical analogue, not the exact reference dynamics.

**E_65 (temporary) - Independently noisy positions.** Extend the shared smooth deterministic flow with
independent particle disturbances. Specify the stochastic process, correlations, integration and seed
handling. Independent noise may allow crossings and destroys the automatic cyclic-order invariant. Compare
with zero-noise and shared disturbances; do not presume identifiability or interpret fitted noise physically.

**E_66 (temporary) - Two-dimensional torus.** Extend the abstract periodic ring to two periodic coordinates.
Consider a field on a torus and a corresponding vector-valued guidance rule, with a declared capture/selection
geometry. One-dimensional cyclic ordering does not carry over; investigate dynamics, recurrence, possible
mixing and computational cost without presuming chaos. Field basis, integrator and fitting are unresolved.

**E_67 (temporary) - Cross-barrel field coupling.** Investigate coupling between the latent main and
supplementary Powerball systems (or past cross-barrel observations used in prediction), preserving their
different label spaces, legal selection and separate scoring. The games themselves must never be pooled.
Specify whether coupling is through shared parameters, state evolution or past observations; distinguish it
from the independent models in E_58/E_61. No such coupling is assumed by the reference method. Applicability
where only one barrel exists must be addressed explicitly.

**E_68 (temporary) - Full configuration-space / entangled wave.** A shared field on one coordinate is not
the same as a wave over the entire configuration Q = (q_1,...,q_n). The Bohmian guidance form
v_j(Q,t) = (hbar/m_j)*Im(grad_j psi(Q,t)/psi(Q,t)) motivates a separate, potentially non-factorisable
configuration-space construction. Investigate how a tractable representation of that wave could guide
labelled particles jointly, how to normalise it, treat nodes, impose legal observation/selection rules, and
infer parameters using only earlier draws. A product-separable reference versus genuinely coupled state is a
possible comparison, not a decided design. The dimensionality and identifiability problem is substantial;
resource feasibility, state representation and likelihood remain unresolved. No physical entanglement of
lottery balls is asserted. Retain the lead irrespective of anticipated feasibility.

These descriptions do not impose a development order. No extra permanent E-identity is assigned to each
possible subvariant. The earlier unrestricted guided-trajectory concept is represented provisionally by E_61
and E_62, as R1 explicitly says. The future-priorities draft of 25 November is a discussion input only, not an
amendment to the roadmap.

### D.3 Methods A and B: recurrence-gap spectrum and delay-embedding analogues

Source: `doc/GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md`, sections 1-4 and 8;
also OWNER_REMINDERS R-001. The following preserves the original research detail, including corrections to the
GAIS proposal, diagnostic statistics, prediction construction, numerical settings and limitations.
It is a historical proposal extract, not a fresh mandate for sample counts, simulation campaigns, old
holdouts, runtime estimates or reporting protocols. The owner has since mapped Method A to E_17 (the log-age
variant is installed) and Method B to E_45 (not built). The wider original ideas remain available for discussion.
The original order-data caveat is superseded by the accepted operator-labelled drawn-order policy.
In particular, the original suggested within-draw spacing construction was rejected, not all spacing research.
The original rejection of a physical pilot-wave interpretation is not a veto on the subsequently catalogued
mathematical analogues. The original optional predictive use of forbidden patterns remains an idea, not an
automatic synthetic-performance gate. The original proposal and its references retain the full historical record.

#### 1. Summary of the two methods

##### Method A - "Recurrence-gap spectrum: do ball numbers repel or cluster across weeks?"

**How it works**

- Each ball number (1-35 main, 1-20 Powerball) has its own history of the weeks in which it was drawn.
- Treat each history like the "energy levels" or "zeta zeros" studied in random-matrix theory.
- Ask whether a number that has just appeared is less likely to reappear soon ("repulsion", the Riemann/random-matrix signature) or more likely ("clustering"), compared with fair draws.
- Also ask whether appearances are more regular or more bunched over longer windows than fair draws allow.

**Prediction:** a fitted "chance of appearing next week, given weeks since last appearance" curve ranks the numbers. The top 7, plus the top Powerball, are the prediction.

**Under fair draws:** the curve is flat and the method has no edge.

##### Method B - "Delay-embedding analogues and forbidden patterns: is there week-to-week dynamical memory?"

**How it works**

- Build a "recent situation" from the last few weeks of draws.
- Find the past weeks whose recent situation most resembled it, and use what followed them as the prediction. This is the method of analogues, the practical predictive form of Takens' theorem.
- Separately, check whether certain up/down orderings of consecutive weekly values never occur ("forbidden ordinal patterns"). Such patterns are a fingerprint of deterministic dynamics that random sequences do not leave.

**Prediction:** the weighted votes of the analogue weeks' successors rank the numbers. The top 7, plus the top Powerball, are the prediction.

**Under fair draws:** past situations carry no information about the future and the method has no edge.

---

#### 2. Shared provenance and what was changed from the source

##### 2.1 Origin

Both methods come from the GAIS response in `GASI_thought_experiments_possibly_unexplored_areas.md`, specifically:

- Framework 1 (Riemann Hypothesis, random-matrix theory and quantum chaos) and its Phase 1 (spacing test, Brody distribution).
- Framework 3 (Takens' embedding and attractor reconstruction) and its Phase 3 (Bandt-Pompe permutation entropy, forbidden patterns).
- Phase 4 (surrogate-data testing), which is adopted for both.

##### 2.2 Corrections to the source (recorded so they are not carried into any spec)

1. **Within-draw spacing test (GAIS Phase 1) is rejected as constructed.**
   - Balls are drawn without replacement from whole numbers, so two balls in the same draw can never be closer than 1 apart.
   - Normalised spacings therefore can never be near zero. Any fitted curve will show "repulsion" whatever the physics.
   - With only 6 integer gaps per draw, the "unfolding" step GAIS describes has no meaning.
   - Method A replaces this with an across-time construction (section 3.4) that has an exact, artefact-free null.
2. **Brody parameter mislabelled.**
   - GAIS says a Brody parameter near 1 indicates "Riemann zeros / GUE".
   - Brody parameter 1 reproduces the Wigner surmise for the orthogonal ensemble (GOE, linear repulsion). It does not reproduce the unitary ensemble (GUE, quadratic repulsion), which is the one matching the zeta zeros.
   - The GUE formula GAIS quotes, P(s) = (32/pi^2) s^2 exp(-4 s^2 / pi), is itself correct, but it is not the Brody-1 case.
3. **No mechanism links the Riemann Hypothesis to lottery predictability.**
   - The Montgomery-Odlyzko result is a statistical resemblance between zeta zeros and random-matrix eigenvalues.
   - Nothing about it can be "applied" to predict draws.
   - What can be borrowed is the toolkit: spacing statistics, number variance, rigidity and form factor. Method A uses only that toolkit.
4. **Correlation-dimension estimation (GAIS Framework 3) is excluded.**
   - With N data points, the largest correlation dimension that can be credibly estimated is roughly 2 x log10(N) (Eckmann and Ruelle, 1992). That is about 5 for the ~446 draws in the current format.
   - A "finite fractal dimension" found at this sample size would be untrustworthy.
   - Method B uses analogue forecasting and ordinal patterns instead. Both are designed for short series.
5. **Smaller slips.**
   - "Solovay-Strassen" (GAIS Framework 4) is a primality test, not a normality test.
   - GAIS's draw count of ~1,040 over 20 years ignores the format change. Only the post-April-2018 draws are comparable (section 5.1).

##### 2.3 What was deliberately left out

- **Framework 2 (de Broglie-Bohm pilot waves, quantum non-equilibrium):** no observable in weekly lottery results could distinguish it from classical chaos.
- **Framework 4 (algorithmic information, normality in all bases):** needs far more data than exists. With ~446 draws it reduces to ordinary frequency tests.
- **Phase 2 (topological data analysis, persistent homology):**
  - Heavier dependencies (ripser or giotto-tda) and more compute.
  - Persistence diagrams of ~446 points in 7 dimensions are dominated by sampling noise.
  - It could be revisited later if the owner wants it, but it is not proposed here.

---

#### 3. Method A - Recurrence-gap spectrum

##### 3.1 One-line title

Recurrence-gap spectrum: do ball numbers repel or cluster across weeks?

##### 3.2 Provenance

- **H. Montgomery (1973):** derived the pair-correlation function of the Riemann zeta zeros. F. Dyson recognised it as the pair correlation of eigenvalues of random unitary (GUE) matrices.
- **A. Odlyzko (1987 onward):** confirmed this numerically to extraordinary precision for very high zeros.
- **E. Wigner and F. Dyson (1950s-60s):** random-matrix theory as a model for energy levels of heavy nuclei. Eigenvalues "repel": small spacings are suppressed.
- **O. Bohigas, M.-J. Giannoni and C. Schmit (1984):** the conjecture that quantum systems with chaotic classical counterparts show random-matrix level statistics, while integrable systems show Poisson (independent) statistics.
- **T. Brody (1973):** a one-parameter spacing distribution interpolating between Poisson and the Wigner (GOE) surmise.
- **Standard spectral statistics:** nearest-neighbour spacing distribution, number variance Sigma^2(L), Dyson-Mehta spectral rigidity Delta_3(L), and the spectral form factor (Fourier-domain correlation).

The idea borrowed is diagnostic. Random-matrix statistics give a well-developed vocabulary for whether events along a line are:

- independent (Poisson-like),
- mutually avoiding (repulsion, rigidity), or
- bunched (clustering).

Applied to "when does ball number n come up", that vocabulary becomes a sharp randomness test with an exact null.

##### 3.3 Why the within-draw version is not used

See section 2.2 item 1. Constraints of the game rules, not physics, would produce the effect GAIS proposed to look for.

##### 3.4 Construction (adopted)

1. **Data:** post-format draws only (Draw 1144, 19 April 2018, onward; section 5.1).
2. **Indicator histories.** For each main number n in 1..35, build a 0/1 series I_n(t) over draws t = 1..N, where I_n(t) = 1 if n was drawn in draw t. Do the same for each Powerball number m in 1..20 using the Powerball barrel only.
3. **Event "spectrum":** the draw indices where I_n(t) = 1. The gaps are the differences between consecutive indices (gap >= 1; gap = 1 means consecutive weeks).
4. **Exact null for a single number.**
   - Under fair draws, I_n(t) is independent Bernoulli(p) across draws, with p = 7/35 = 0.2 for main numbers and p = 1/20 = 0.05 for Powerball numbers.
   - Gaps are therefore exactly geometric: P(gap = k) = p (1 - p)^(k - 1).
   - "Unfolding" is trivial: the mean gap is 1/p (5 draws main, 20 draws Powerball) and the rate is constant.
5. **Pooled statistics.** Across numbers, the series are not independent, because each draw contains exactly 7 main numbers. Pooled statistics therefore take their null from Monte Carlo simulation of the real game (section 5.2), not from a formula.
6. **Expected volume (to ~Oct 2026, ~446 draws):**
   - Main: about 89 appearances per number, about 88 internal gaps each, about 3,080 pooled gaps.
   - Powerball: about 22 appearances per number, about 420 pooled gaps.
7. **Censoring.** The stretch before a number's first appearance and the stretch since its last appearance are incomplete gaps.
   - Pre-declare: exclude them from gap-distribution statistics.
   - Include the current open gap only as the predictor input (section 3.6).

##### 3.5 Diagnostic statistics (pre-declared)

All are computed separately for the main barrel (pooled over 35 numbers) and the Powerball barrel (pooled over 20 numbers). Each is compared with the same statistic on at least 10,000 simulated fair histories of identical length.

- **A1. Short-gap ratio (primary).**
  - The observed fraction of gaps equal to 1, compared with the null (p: 0.2 main, 0.05 Powerball).
  - A deficit means repulsion (the random-matrix-like direction). An excess means clustering.
  - Also report gaps of 2 and 3 as secondary.
- **A2. Gap-distribution distance.**
  - A single goodness-of-fit distance between the pooled gap histogram and the geometric law, for example chi-square over bins 1, 2, 3, 4-5, 6-8, 9-13, 14+ for main.
  - Its p-value comes from the simulated envelope, not chi-square tables.
- **A3. Hazard profile.**
  - h(k) = P(number appears at gap k | it has not appeared for k - 1 draws). This is flat at p under the null.
  - Fit one slope, a logistic regression of appearance on log(gap) pooled across numbers.
  - Slope < 0: the longer since last seen, the less likely (clustering/"hot").
  - Slope > 0: the longer since last seen, the more likely (repulsion/"due").
- **A4. Number variance Sigma^2(L) (primary).**
  - For window lengths L = 5, 10, 20, 50 draws (pre-declared, overlapping windows), compute the variance of a number's appearance count across windows, averaged over numbers.
  - The null per number is exactly binomial: L x p x (1 - p).
  - Below null means more regular than chance (rigidity, the random-matrix signature, which grows only logarithmically with L). Above null means bunching.
  - Report the ratio observed/null for each L against the simulated envelope.
- **A5. Form factor / periodicity (secondary, optional).**
  - Compute the periodogram of each centred indicator series, normalise and average across numbers, then test the largest peak against the simulated envelope.
  - This is the closest cheap analogue of the spectral form factor.
  - Physical hook: if ball sets or draw machines rotate on a fixed cycle and one set or machine is slightly biased, a peak at that period is the expected signature (section 3.9).

##### 3.6 Predictor

For each target draw t + 1, using only draws 1..t (strict walk-forward):

1. **Fit the hazard model** of A3 on draws 1..t, pooled across numbers, separately for each barrel.
   - Two parameters (intercept and slope on log gap), with mild shrinkage toward the null (slope 0) so early fits on little data do not swing wildly.
   - Pre-declare the shrinkage, for example a ridge penalty fixed in advance.
2. **Compute each number's current open gap** g_n (draws since last appearance).
3. **Score each number** by predicted probability h(g_n + 1).
4. **Pick** the top 7 main numbers and the top Powerball number.
   - Ties are broken by a seeded random draw, with the seed recorded.
   - Do not break ties by lowest number: that silently biases toward low numbers.
5. **Burn-in.** No predictions before a pre-declared minimum history, for example 52 draws (one year). Before that the hazard fit is mostly noise.

The sign of any effect is learned from the data, not chosen by hand. If the fitted slope is about 0, the picks are effectively random, which is the correct null behaviour.

This predictor is the formal, testable version of the folk "hot numbers" and "due numbers" beliefs. A clean null result is itself informative: it tests the gambler's-fallacy claims directly.

##### 3.7 Measurement within the project

- **Predictions:**
  - One prediction record per target draw, produced walk-forward.
  - Scored by the project's existing scoring (matches, prize-division equivalents) exactly as other methods are.
- **Baselines:**
  - Under fair draws, 7 picks from 35 match on average 7 x 7/35 = 1.4 main numbers (hypergeometric). The Powerball matches with probability 0.05.
  - Compare the method's score with these expectations and with the score distribution obtained by running the identical predictor on simulated fair histories. This null includes any selection or fitting artefacts.
- **Diagnostics:** A1-A5 are reported as randomness-test outputs, separate from prediction scores, each with its simulated-envelope p-value or z-score.
- **Real-world forward predictions:** once the method is frozen, its next-draw predictions join the project's forward predictions. They are the test that counts.

##### 3.8 Effort and runtime

- **Code:**
  - About 200-300 lines: indicator building, gap extraction, A1-A5, hazard fit, predictor.
  - It reuses the shared fair-draw simulator (section 5.2).
- **Dependencies:** numpy, scipy.
- **Runtime:**
  - The diagnostics on 10,000 simulated histories take seconds; the indicator arithmetic is about 10^8 operations, vectorised.
  - The walk-forward predictor null (about 1,000 simulated histories x about 400 refits each) takes a few minutes if the hazard fit is kept cheap (closed-form or a few Newton steps on a two-parameter model).
  - Well under the half-hour budget.

##### 3.9 Expectations and things to watch

- **Expected outcome:** null. Mechanically mixed balls drawn weekly have no known way to "remember" last week's numbers.
- **What the data could detect (rough):**
  - With ~3,080 main gaps, the standard error of the short-gap ratio is about sqrt(0.2 x 0.8 / 3080), about 0.007.
  - A shift of about 0.02 (a 10% relative change) would reach about 3 sigma.
  - Such an effect would raise expected main matches only from 1.40 to about 1.5 per draw, which is detectable over ~400 walk-forward draws at best marginally.
  - Any real effect is expected to be small.
- **Things to watch:**
  - *Era mixing:* never pool the pre-2018 formats into these statistics (section 5.1).
  - *Censoring handling* (section 3.4 item 7). Getting it wrong biases A1 and A2.
  - *Powerball sparsity:* ~420 gaps give much weaker tests than the main barrel. Expect wide envelopes.
  - *Cross-number dependence:* never use per-number binomial formulas for pooled p-values. Use the simulator.
  - *Cherry-picking:* do not report "number 17 is clustered" findings from 35 per-number tests without correction. The pre-declared statistics are pooled.
  - *Physical covariates:*
    - The current format was introduced with two Smartplay Halogen II draw machines (per public sources).
    - If per-draw machine or ball-set identity is available from any official source, record it as a covariate.
    - A real bias tied to one machine or one ball set would appear as periodicity (A5) or as a split between machine-specific subsets.
    - This is the single most plausible route to a genuine non-random finding, and it is a mechanical one, not an exotic one.

---

#### 4. Method B - Delay-embedding analogues and forbidden ordinal patterns

##### 4.1 One-line title

Delay-embedding analogues and forbidden patterns: is there week-to-week dynamical memory?

##### 4.2 Provenance

- **N. Packard, J. Crutchfield, J. D. Farmer and R. Shaw (1980); F. Takens (1981):** the state of a deterministic dynamical system can be reconstructed, up to a smooth change of coordinates, from delayed copies of a single observed quantity (delay embedding).
- **P. Grassberger and I. Procaccia (1983):** the correlation dimension. **J.-P. Eckmann and D. Ruelle (1992):** its data-size limits (section 2.2 item 4).
- **E. Lorenz (1969):** the method of analogues. Forecast by finding past states similar to the present one and seeing what followed.
- **G. Sugihara and R. May (1990):** simplex projection. Analogue forecasting in a delay embedding, used specifically to distinguish deterministic chaos from noise in short series. Later, S-maps test for state-dependent non-linearity.
- **C. Bandt and B. Pompe (2002):** permutation entropy, from the ordinal patterns of consecutive values.
- **J. Amigo, S. Zambrano and M. Sanjuan (2007):** "true and false forbidden patterns".
  - Deterministic systems have ordinal patterns that can never occur.
  - In random series a missing pattern is only a finite-sample accident.
- **L. Zunino and colleagues (2017):** tied values (equal consecutive values) can create spurious forbidden patterns and false conclusions.
- **J. Theiler and colleagues (1992):** surrogate-data testing for non-linearity.

The idea borrowed is this. If the weekly draw carried any deterministic memory, Takens says it is in principle recoverable from the observed series. The tools that work at small N are analogue forecasting and ordinal patterns, not dimension estimates.

##### 4.3 Why correlation dimension is not used

See section 2.2 item 4.

##### 4.4 Series (pre-declared; keep to this list)

- **S1 - Powerball value**, 1..20. Scalar. Many ties (section 4.6).
- **S2 - Sum of the 7 main numbers**, 28..224; null mean 126, null standard deviation about 24.2. Scalar, few ties. Diagnostic only; it does not map to picks.
- **S3 - Whole main draw as a 35-bit set.** Used for analogue forecasting of main picks.
- **S4 - Drawn-order series** (conditional on data availability; section 5.6), for example the first-drawn main ball. Physically the most meaningful series for dynamics. Include only if drawn order can be scraped reliably for the whole post-2018 era.

No other series without a recorded decision. Each added series is another chance for a false positive (section 5.3).

##### 4.5 B1 - Analogue forecasting (simplex projection) - predictor

**For S3 (main picks)**

1. **State at draw t:** the last E draws as E 35-bit sets.
   - Pack each draw into one 64-bit integer.
   - Hamming distance is then popcount(xor), summed over the E draws.
2. **Library for target t + 1:** all past (state at s, draw at s + 1) pairs with s + 1 <= t. This is strict walk-forward with no look-ahead.
3. **Neighbours:** the k = E + 1 nearest library states. Ties at the boundary distance are included with equal fractional weight, or by seeded random selection; pre-declare which.
4. **Votes:** each neighbour's successor draw votes for its 7 numbers, weighted exp(-d / d_min), the Sugihara-May weighting (guard against d_min = 0).
5. **Pick** the top 7 by weighted vote. Ties are broken by seeded random draw.

**For S1 (Powerball pick):** the same method on the scalar S1 delay vector (S1(t), S1(t-1), ..., S1(t-E+1)), with Euclidean distance. Neighbours' successor Powerball values vote; pick the top value.

**Settings**

- Primary setting pre-declared as E = 2, tau = 1 (consecutive weeks).
- Also report E = 1, 3 and 4 in full as secondary, never selecting the best after the fact.
- Burn-in: no predictions before 52 draws.

**Skill measures**

- For prediction: the project's standard scoring, as for Method A.
- For the dynamics diagnosis on S1 and S2 (the Sugihara-May test):
  - the correlation rho between predicted and actual values;
  - mean absolute error relative to the naive "training mean" forecast.
- Report skill against E (and against forecast horizon 1-3 draws). A genuinely deterministic system shows skill that declines with horizon; noise shows none at any horizon.

**Optional (secondary): S-map on S2**

- Test whether skill improves as the locality parameter theta rises above 0.
- Improvement indicates state-dependent (non-linear) dynamics.
- Include only if cheap to add once B1 exists.

**An expected weakness, recorded in advance**

- Two fair 7-from-35 draws share on average 1.4 numbers, so Hamming distances cluster tightly around 11.
- "Nearest" past states are therefore barely nearer than random ones. This is the curse of dimensionality, and it is why E is kept small.
- If B1 shows no skill, this weakness is part of the honest interpretation. If it does show skill, leakage is the first suspect (section 4.9).

##### 4.6 B2 - Forbidden ordinal patterns - diagnostic

1. **Series:** S1 and S2 (and S4 if adopted).
2. **Orders:** d = 3, 4, 5, with tau = 1.
   - d = 6 is excluded: 720 patterns over ~440 vectors gives under one expected count per pattern, so about half would be "missing" by chance.
   - At d = 5 (120 patterns, about 3.7 expected each) about 3 patterns are expected to be missing by chance alone.
   - At d = 4 (24 patterns, about 18 expected each) a missing pattern would be remarkable.
3. **Tie rule (pre-declared).**
   - Equal values are ranked by order of occurrence; this is the common convention.
   - Under the null, ties are frequent for S1: about 27% of 4-value windows and about 42% of 5-value windows contain at least one tie.
   - Run a sensitivity version that drops tied windows, and report both.
4. **Statistics:**
   - (i) the number of missing patterns;
   - (ii) normalised permutation entropy H in [0, 1];
   - (iii) the chi-square of pattern counts.
   - All are compared with at least 10,000 simulated fair histories run through the identical pipeline, including the identical tie rule. This makes tie-induced bias appear equally in the null and cancel.
5. **Nesting check (key discriminator).**
   - A genuinely forbidden pattern at order d forces every order-(d + 1) pattern containing it to be forbidden too, so true forbidden patterns propagate and grow in number with d.
   - Chance misses do not nest consistently.
   - Report whether any pattern missing at d = 4 has all its d = 5 extensions missing.
6. **Optional predictive use (secondary):** given the last d - 1 values, rank next-value regions by how under-represented each continuation pattern is. This is only worth building if B2 shows a significant missing-pattern result.

##### 4.7 Measurement within the project

- **Predictions:** B1 produces one prediction record per target draw (7 main + 1 Powerball), walk-forward, scored by the project's standard scoring.
- **Baselines:** the same as Method A (1.4 expected main matches, 0.05 Powerball), plus the score distribution from running B1 unchanged on at least 1,000 simulated fair histories.
- **Diagnostics:** B1 skill curves (S1, S2) and B2 statistics, each with simulated-envelope p-values or z-scores, reported separately from prediction scores.
- **Forward predictions:** as for Method A.

##### 4.8 Effort and runtime

- **Code:**
  - B1: about 150-250 lines.
  - B2: about 100-200 lines; no ordpy needed, as the ordinal encoding is a few lines of numpy.
  - Reuses the shared fair-draw simulator.
- **Runtime:**
  - B1 per history: about 400 targets x up to about 446 library states x E popcounts, about 10^6 operations; trivial.
  - B1 over 1,000 null histories x 4 values of E: a few minutes in vectorised numpy.
  - Spread across the 3900X's 12 cores via multiprocessing if wanted; each history is independent.
  - B2 over 10,000 null histories: seconds to a minute.
  - Total well under the half-hour budget.

##### 4.9 Expectations and things to watch

- **Expected outcome:** null.
  - Each draw is a separately run physical event.
  - Two machines and possibly several ball sets are in use.
  - Nothing physical obviously carries a "state" from one Thursday to the next.
- **What the data could detect (rough):**
  - The standard error of a forecast-skill correlation over ~400 walk-forward targets is about 1 / sqrt(400) = 0.05.
  - Skill around rho = 0.15 would be about 3 sigma.
  - That is a fairly strong effect; weak memory would go undetected.
- **Things to watch:**
  - *Look-ahead leakage (most important):*
    - Any library pair whose successor is the target draw or later invalidates the result.
    - A positive B1 result should be presumed to be a leakage bug until proven otherwise.
    - Recommended test: run B1 on simulated fair histories and confirm the skill is at chance.
  - *Post-hoc choice of E or k:* report the full pre-declared grid. Never promote the best-looking setting to "primary" afterwards.
  - *Ties:* see section 4.6. Never interpret missing patterns in S1 without the matched simulated null.
  - *Sorted versus drawn order:*
    - Published sorted results destroy the within-draw time order.
    - S3 is unaffected, because it uses sets.
    - S4 depends on drawn order being available.
  - *Machine switching:* if per-draw machine identity is ever available, it is a natural split. Dynamics, if any, would live within one machine's sequence.

---

#### 8. References (for provenance; not required reading)

- Amigo, J. M., Zambrano, S., Sanjuan, M. A. F. (2007). True and false forbidden patterns in deterministic and random dynamics. Europhysics Letters 79, 50001.
- Bandt, C., Pompe, B. (2002). Permutation entropy: a natural complexity measure for time series. Physical Review Letters 88, 174102.
- Bohigas, O., Giannoni, M.-J., Schmit, C. (1984). Characterization of chaotic quantum spectra and universality of level fluctuation laws. Physical Review Letters 52, 1.
- Brody, T. A. (1973). A statistical measure for the repulsion of energy levels. Lettere al Nuovo Cimento 7, 482.
- Eckmann, J.-P., Ruelle, D. (1992). Fundamental limitations for estimating dimensions and Lyapunov exponents in dynamical systems. Physica D 56, 185.
- Grassberger, P., Procaccia, I. (1983). Characterization of strange attractors. Physical Review Letters 50, 346.
- Lorenz, E. N. (1969). Atmospheric predictability as revealed by naturally occurring analogues. Journal of the Atmospheric Sciences 26, 636.
- Montgomery, H. L. (1973). The pair correlation of zeros of the zeta function. Proceedings of Symposia in Pure Mathematics 24, 181.
- Odlyzko, A. M. (1987). On the distribution of spacings between zeros of the zeta function. Mathematics of Computation 48, 273.
- Packard, N. H., Crutchfield, J. P., Farmer, J. D., Shaw, R. S. (1980). Geometry from a time series. Physical Review Letters 45, 712.
- Sugihara, G., May, R. M. (1990). Nonlinear forecasting as a way of distinguishing chaos from measurement error in time series. Nature 344, 734.
- Takens, F. (1981). Detecting strange attractors in turbulence. Lecture Notes in Mathematics 898, 366.
- Theiler, J., Eubank, S., Longtin, A., Galdrikian, B., Farmer, J. D. (1992). Testing for nonlinearity in time series: the method of surrogate data. Physica D 58, 77.
- Zunino, L., Olivares, F., Scholkmann, F., Rosso, O. A. (2017). Permutation entropy based time series analysis: equalities in the input signal can lead to false conclusions. Physics Letters A 381, 1883.
- Lotterywest media releases, 12-13 April 2018: Powerball format change to 7 from 35 plus 1 from 20, first draw Draw 1144 on Thursday 19 April 2018.



### D.4 Other historical research avenues (provisional identities)

Source: `doc/GASI_thought_experiments/GASI_thought_experiments_possibly_unexplored_areas.md`, Framework 4
and Phase 2, and the corrections and historical disposition in the Methods A/B proposal section 2.3.
These remain visible, without silently reinstating the source's rejected claims or assigning a development order.

**E_69 (temporary) - Topological data analysis / persistent homology.** Represent draw observations as points
in a declared feature space, examine the persistent connected components, loops or other topology across a
range of scales, and compare any proposed structure with suitably matched fair histories. The original
proposal envisaged a seven-coordinate point cloud and possible ripser or giotto-tda tools. The follow-up
A/B proposal deferred it because small samples in high dimensions may be dominated by sampling noise and
the dependencies are heavier. A defensible metric, representation, control and mapping (if any) from
diagnostic to next-draw ranks remain open. This is not an established low-sample-size advantage.

**E_70 (temporary) - Algorithmic information / normality in multiple bases.** The GAIS proposal contemplated
unusual information/compressibility and normality-based diagnostics. The A/B follow-up set it aside as
requiring more observations; the original claim about Solovay-Strassen is erroneous (it is a primality
test, not a normality test). Investigate only if a distinct and well-defined representation and experiment
can be justified; distinguish it from E_41's context-tree/compression prediction and other existing
information-theory methods. This temporary identity is for retention and discussion, not a new accepted
predictive method.

### D.5 E_71 (temporary) - Pattern-spotting by non-local means (NL-means) - LAST

Source: `exchange/OWNER_REMINDERS.md`, R-002. The owner places this idea last, superseding the old reminder
about its timing after wave 3. It is deferred, not rejected. NL-means is an image-denoising technique that
averages pixels using similarities between surrounding patches, including patches far away in the image.
Ideas originally retained for discussion:

- What: discuss, even if only to record why it is set aside, whether non-local means (NL-means, an
  image denoising method that averages each pixel with others anywhere in the image whose
  surrounding patches look alike) or a similar "non-local" technique could say anything about the
  draws. Ideas to discuss:
  - viewing the draw history in different ways: as a series of images over time, as one large image
    (draws by numbers, for example), or other imaginative arrangements;
  - applying NL-means or similar to those views, and seeing whether any structure (edges, repeated
    patches, anything) emerges that fair draws would not produce;
  - whether any such structure could be turned into a testable way of ranking numbers for the next
    draw;
  - whether it suggests some other oddball method that is easy to code.
  The owner's own view: probably not feasible, but worth discussing and recording either way.

A future design would need a causal representation of historical observations, a patch-similarity rule and
a means of turning any discovered structure into testable next-target rankings; these are not yet specified.
No later target may enter a denoised feature or a similarity search for an earlier forecast. No feasibility
or predictive advantage is claimed. This is the last research lead in the inventory by owner direction.

END.
