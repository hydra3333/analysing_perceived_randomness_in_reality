# Operations manual - the research system

**Edition 1, 28 November 2026.** Written by the Claude web chat from the commands as built and from what they
printed on the owner's PC on 27 and 28 November 2026. Outline agreed by the owner and the reviewer (decision log
entry 401); the reviewer's corrections taken in (entries 403 and 404).
**Status: RATIFIED by the owner, RAT-70 (decision log entry 404).**

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
- The rest: 10. Standards; A. The system at a glance; B. Command reference; C. Methods list

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

**Research leads without a number.** Kept in `exchange\OWNER_REMINDERS.md` and `doc\GASI_thought_experiments\`:
the owner's Methods A and B (to become the specifications of E_17 and E_45; R-001), and pattern-spotting by
non-local means (the NL-means idea; R-002). The R1 research document
(`doc\Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md`, section 4.7.1b) keeps the remaining
pilot-wave (de Broglie-Bohm) inspired leads, among them a full configuration-space (entangled) wave. A
catalogue entry is not a priority.

END.
