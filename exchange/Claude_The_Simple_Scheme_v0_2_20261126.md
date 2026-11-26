# The simple scheme: how the research system works from here (v0.2)

**Date:** 26 November 2026. **Author:** the Claude web chat, on the owner's go (decision log entry 339).
**For:** the owner's agreement. The ChatGPT reviewer chat read v0.1 once (entry 341) and asked for no further
review; section 13 lists every change since v0.1.
**Status:** for the owner's agreement. Nothing in it is built, moved or installed, and it authorises nothing on
the owner's PC. Everything stays paused (entry 330) until he has agreed it. Draw values: none appear here.

**How to read it.** Everything here is decided by the owner (entries 326 to 328, 330, 335 to 337, 342, 343) or
agreed by all three (entries 333, 334, 338, 341). Nothing is left marked PROPOSED.

## 1. What this is for

This is speculative, exploratory research: do Australian Powerball and Oz Lotto results hold patterns that
ordinary statistics missed? The system exists to try methods, walk them forward over the draws, and show honestly
how they did. If something ever looks unusual enough, a formal investigation would be a separate, later project
on then-future draws. Nothing is built now on its account.

Three principles govern everything below:

1. **What a tree does follows from the software in it, not from the tree's name.**
2. **Everything a tree computes can be made again** from the official results and the software. So nothing is
   sealed, chained or locked, and **a difference never refuses: it means "rebuild that part".**
3. **The science must be right; the administration must be small.**

## 2. What stays exactly as it is

- **The science, by reference:** N-1 (a forecast for a draw is computed only from earlier draws); TOP and WORST
  from the same model for a target; games never pooled; the methods, the readout and ties, the scoring, the league
  measures and OV-1's arithmetic, as the specification v0.6 section 1.2 lists them and its sections 3.4, 6, 8, 9
  and 10 describe them. The permitted-view digest stays, because it is part of every tie order.
- **The source:** Lotterywest-GOV over HTTPS only, through the owner's reviewed updater with its own checks.
- **The standing rules:** no AI chat and no local runner ever contacts a lottery website or runs the updater; no
  program ends another process; nothing changes the PC's date, time or zone; nothing runs on the owner's PC
  without his go. The sealed Mode H records and the old system's files are left untouched.

## 3. The three trees

**Names and places.** Each tree's folder name ends with its role.

| Tree | Folder | Backups go to |
|---|---|---|
| DEV | `...\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV` (a subfolder of the repository) | `T:\a_p_r_i_r_backups\DEV` |
| QA | `T:\a_p_r_i_r_QA` | `T:\a_p_r_i_r_backups\QA` |
| PROD | `G:\a_p_r_i_r_PROD` | `T:\a_p_r_i_r_backups\PROD` |

**Every tree has the same shape:**

    <tree>\
      ENVIRONMENT.ini        the settings (section 3.1)
      Run_Research.bat ...   the launchers
      .venv\                 this tree's own Python, built by the owner's two scripts
      src\research\ ...      the engine (the "infrastructure": everything under src\ outside the method families)
      src\methods\<family>\<variant>\    the methods
      source_data\           the accepted official results (the updater's files)
      results\research\      everything the job computes; all of it can be made again
      records\               the lock file and the job log

DEV also has `deploy\` (the install tools) and `tests\`. Nothing else differs. In DEV the software is tracked by
Git; the settings, `.venv`, `results\research` and `records` are not.

**What each tree is for.** DEV: methods and the engine are written, changed and tried, and installed from.
QA: the same software as PROD when the owner makes it so, or ahead of it; where an install is proved. PROD:
the ongoing research. No tree is a gate for another.

### 3.1 The settings file and how a tree knows which tree it is

One file of the same form in every tree; only the `role` line differs:

    [environment]
    role = QA
    [DEV]
    tree_root = E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV
    backup_root = T:\a_p_r_i_r_backups\DEV
    [QA]
    tree_root = T:\a_p_r_i_r_QA
    backup_root = T:\a_p_r_i_r_backups\QA
    [PROD]
    tree_root = G:\a_p_r_i_r_PROD
    backup_root = T:\a_p_r_i_r_backups\PROD

1. **A command works on the folder its own launcher lies in.** Never on the current folder of the window it was
   typed in, and never on a path read from the settings.
2. **Before anything, it checks that folder:** the `role` must be the ending of the folder's name, and that role's
   `tree_root` must be that folder. If not, it stops and names both.
3. **Before it reads from or writes into another tree,** it reads that tree's own settings file and requires the
   role intended, by the same check. No settings file there means "not a tree": it stops. A new tree is made only
   by the create command, into a folder that is absent or empty.
4. **When the file is read:** no two roles share a `tree_root`; no tree lies inside another; no backup folder
   equals or lies inside any of the three trees.

The settings file is never copied between trees. Paths are compared as real absolute Windows paths.

## 4. The three small files beside a method

They lie in the method's own folder, `src\methods\<family>\<variant>\`, where its software is. All are plain text.

| File | Who writes it | What it holds | What it means |
|---|---|---|---|
| `I_AM_INSTALLABLE` | "make installable", in DEV | the method's fingerprint | this version may be installed. No file: not offered. A file older than the method's files: reported, and not installed until it is made again |
| `I_AM_RETIRED` | "retire", from DEV, into every tree that has the method | for each game, the draw from which it stops; one line of reason | the method makes no forecast for that draw or any later one. Its earlier results stay, marked retired. Deleting the file brings it back |
| `IN_PLACE_SINCE` | the research job, in each tree | for each game, the last draw the tree held when this version of the method's code was first used there (its "establishment draw") | bookkeeping only: lets a report show how a method did on the draws since its code was in place. Written afresh whenever the job rebuilds the method because its code changed. A missing file stops nothing |

**A method's fingerprint** is what the engine computes today: one SHA-256 over its declaration, its own files and
the family and shared helper files it uses. So a changed helper changes every method that uses it. **The three
small files above, and generated files such as `__pycache__`, are never part of any fingerprint.**
**The infrastructure's fingerprint** is one SHA-256 over every file under `src\` outside the method families,
with the same exclusions.
"Make installable" for the infrastructure writes the same kind of flag, once, in `src\`.

## 5. The research job: `Run_Research.bat`

The same in every tree. In order:

1. Take the tree's lock (one file in `records\`), unless the command that started the job already holds it. If
   another holds it, stop and say so; if a crash left it behind, the owner deletes it by hand.
2. Check the tree is the tree its settings say (3.1).
3. Fetch new official results with the updater, unless `--no-update`.
4. **Find what is out of date, and rebuild exactly that:**
   - the infrastructure's fingerprint is not the one the tree's results were made with (kept in one small file
     beside them): **everything is rebuilt** (about 47 minutes today for 40 methods and both games, unattended);
   - a method's fingerprint is not the one written in its own stored data (the first line of its files names the
     software that made them): that method's results are deleted and filled again from its starting draw, and its
     `IN_PLACE_SINCE` is written afresh. Because the comparison is with the data itself, it stays right when
     software and data are copied into a tree separately;
   - a stored forecast's permitted-view digest no longer matches the results (draw T was corrected at the
     source): T's score is made again, and every forecast from T + 1 on, with everything that follows from them;
   - `--rebuild <method>` rebuilds one chosen method; `--rebuild-all` rebuilds everything (for example after Python
     or a package is upgraded).
5. Catch up: every method that is not retired forecasts every draw it has not yet forecast, **the next draw
   included,** and is scored against every draw whose result is known. A retired method is filled only up to, and
   not including, its retirement draw.
6. Make the league, the reports and both OV-1 series again, one of each per game: one over all draws; the other
   over the same games with each method counting only from its establishment draw up to (not including) its
   retirement draw, if any. Both are exploratory indicators.
7. Write one line in the job log: the time, the Python and package versions, what was rebuilt and why, and any
   method that failed, with the reason. A failed calculation is never recorded as a result.
8. Make a backup (section 7). Release the lock.

A method folder whose declaration is broken is reported and passed over; the job goes on. The starting draws
are as today: each game's known compatible starting draw and each method's declared minimum history.

**The records** keep their present fields and lose three things: the link from each line to the one before, the
digests that were checked on reading, and the environment digest. They become plain line records, CRLF.

## 6. The commands

| Command | Where | What it does |
|---|---|---|
| `Run_Research.bat` | every tree | section 5. `--no-update` walks forward over the results on file without fetching; `--rebuild <method>` and `--rebuild-all` as section 5 says |
| `Run_Results_Updater.bat` | every tree | fetches new official results into this tree only |
| `Backup.bat` | every tree | a backup now |
| `Make_Installable.bat <method> / ALL / INFRA` | DEV | writes the flag (section 4) |
| `Who_Uses.bat <helper>` | DEV | lists every method that uses a helper file; changes nothing |
| `Create_Tree.bat QA / PROD` | DEV | into an absent or empty folder: writes the settings, copies the flagged software and DEV's accepted results. The owner then builds its `.venv` and runs the job |
| `Install.bat QA / PROD` | DEV | backs the destination up; replaces the infrastructure if it is flagged and differs; replaces or adds every flagged, non-retired method that differs or is missing; then runs the destination's own job with `--no-update`, under the lock it already holds, which rebuilds what changed. A method the destination has and DEV does not is left alone. `--show` prints what it would add, replace and rebuild, and does nothing |
| `Retire.bat <method> <reason>` | DEV | backs up each tree that has the method; writes `I_AM_RETIRED` there, from that tree's own next draw |
| `Copy_From_PROD.bat software / data` | DEV | into QA: PROD's software, or PROD's data (`source_data` and `results\research`), after a backup of QA. Into DEV: data only. Then the destination's job |
| `Restore.bat QA / PROD <zip>` | DEV | section 7 |

Every command that touches another tree takes that tree's lock (once) and checks its identity, and that of any
tree it reads from (3.1 rule 3). When it then runs the destination's job, the job works under that same lock.

## 7. Backups and restore

- **A backup is one plain ZIP** of the tree at maximum compression, named with the role, the date and time, and
  why it was made, in that tree's backup folder. The same mechanism in every tree. No second reading, no digest,
  no recovery kit.
- **When:** after every research job; before every replacement (install, retire, copy from PROD, restore); and
  on demand.
- **The ZIP leaves out `.venv` and the lock file.** The environment is rebuilt by the owner's two scripts, and the
  job log records the versions. Without it a backup is small and quick.
- **If a backup fails,** a job says so loudly and its results stand; a replacement stops before it replaces
  anything.
- **Restore:** first the settings file inside the ZIP must name the tree being restored (its role, and that
  role's `tree_root`); if not, it stops. Then the tree's folder is renamed aside (its new name no longer ends with
  the role, so nothing can run in it), the ZIP is unpacked into a fresh folder of the right name, and the `.venv`
  is built again. Restored
  files are never mixed with newer ones. For DEV the owner does the same by hand; its software is in Git.

## 8. The updater

One updater, the same in every tree, writing only its own tree's `source_data`. It is the present reviewed
updater with every Mode H state taken out and nothing else changed: the same source, parsing, game, draw-number,
chronology, range and overlap checks, and the one comparison of the results file with its own ledger. Shown
unchanged by running old and new on the same invented pages and comparing the results files.

## 9. The proof that the simplification broke nothing

The present engine is left untouched at the top level of the repository. From the same accepted results, the
simplified engine in `a_p_r_i_r_DEV` must give **the same forecasts, the same scores and the same OV-1 numbers**
for every method, game and draw (the second OV-1 series compared with the same starting draws given to both).
Compared in the cloud while it is written, and once on the owner's PC before any tree is created.

## 10. Moving the living system into `a_p_r_i_r_DEV`: what it costs

I looked at how the present engine finds its files. **It already takes its root from where its own program lies**
and names every folder relative to that. So the living system can be **copied** into the subfolder with the same
inner layout and no change to how it finds anything.

- **What is copied:** the 31 infrastructure files, the 12 method families with their 40 methods and 3 shared
  helpers, the launchers, the owner's environment scripts, the 8 test modules of the engine with their fixtures,
  and the two games' accepted results.
- **Copy, do not move** (the owner, entry 342). The top level stays exactly as it is: the old system, and the present
  engine as the reference of section 9. It is frozen from then on. The method files then exist twice in Git, one
  frozen and one living. That is the price; it can be tidied away later.
- **On the owner's PC:** one new `.venv` built in the subfolder with his two scripts, and a first fill there
  (about 47 minutes). Both on his go.
- **Small things:** a few lines in `.gitignore`; a note at the top level saying where the living system is.
- **The local runner's rulebook** names the top level's paths, which do not change, so it stays true. It needs
  one short new edition before the runner rehearses anything of the simple scheme.

My judgement: the cost is small, and smaller than either other way of giving DEV a `_DEV` name.

## 11. What is set aside, and what this replaces

**Set aside** (kept in Git's history, not installed, not maintained): slices A and C of build step 3 (the launch
guard, the environment marker and `Verify_Tree`, the list of installed files, `Check_Tree`, the readiness
machinery, `Init_Tree`, `Install` and `Reinstall_Infra` as built) and slice B's verified backup, recovery kit and
restore; in the engine, the chains and checked digests, the "not current" handling, the status file, the copy
from PROD as a step of the job, and the historical walk-forward rerun as a separate command.

**Replaced when this is agreed:** the administrative parts of the specification v0.6 (its sections 2, 3.3, 3.5,
4, 7A and 11 to 18, and in its sections 5 and 7 what sections 5 and 8 above change) and the whole deployment
design v0.12; RAT-59's two amendments, which become moot; the
build plan of step 3. The specification's scientific sections stay as section 2 above says. The present
handover's account of build step 3 is replaced by a short one.

## 12. How we work from here

- **Review where the science is:** N-1, scoring, OV-1, the mathematics of each new method, and the comparison of
  section 9. The scripts of section 6 get one reading for one question: can this destroy something that cannot
  be made again?
- A Git commit names what is being discussed. Short papers, a decision log that holds decisions, a handover of
  a few pages. **Each AI says, at each point, what it thinks the owner should do next.**
- **The living system's code is committed by Claude directly into `a_p_r_i_r_DEV\` on `main`** (the owner,
  entry 342), named paths only, nothing at the top level touched; the reviewer reads the commit; the owner pulls.
  This replaces the install packages and sheets, and changes, for that subfolder only, the owner's standing rule
  that code never comes from Claude by commit. Nothing runs on his PC without his go, as before.

**The work, in order, each step on the owner's go:**

1. Copy the living system into `a_p_r_i_r_DEV` (section 10).
2. Simplify the engine there; prove it by section 9 in the cloud.
3. The updater without Mode H (section 8).
4. The settings reader, the lock and the commands of section 6.
5. One rehearsal on the owner's PC by the local runner in the scratch folder, with the comparison of section 9
   (after the short new edition of the runner's rulebook).
6. On the owner's PC: DEV's `.venv` and first fill; then QA created; then PROD created.
7. A few pages of how-to, a short handover, the last two LF records converted to CRLF.
8. **Then the research:** new methods.

## 13. What changed since v0.1

**The owner's answers** (entries 342 and 343): DEV's backups in `T:\a_p_r_i_r_backups\DEV`; the ZIP without
`.venv`; a failed backup stops a replacement and only warns after a job; the living system copied, not moved;
Claude commits its code into `a_p_r_i_r_DEV\`. **His three additions:** `--rebuild <method>`, `Install --show`
and `Who_Uses.bat`.

**The reviewer's six clarifications** (entry 341), all taken in:

1. The next-draw forecast is said explicitly; a corrected draw T remakes T's score and every later forecast.
2. Out-of-date research is found from the fingerprint written in the stored data, not from `IN_PLACE_SINCE`.
3. The second OV-1 series is one combined series per game, each method counting from its establishment draw to
   its retirement draw; exploratory only.
4. The three small files and generated caches are left out of every fingerprint.
5. The lock file is left out of backups; a command that runs the destination's job does not take its lock twice.
6. A restore first checks that the ZIP's own settings name the tree being restored.

**Also decided (entry 343):** what the operations manual needs is revisited by the three after implementation.

END.
