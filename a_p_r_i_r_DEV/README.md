# a_p_r_i_r_DEV - the living research system (DEV tree)

This folder is the DEV tree of the research system as the simple scheme describes it
(`exchange/Claude_The_Simple_Scheme_v0_2_20261126.md`, agreed by the project owner on 26 November 2026). It has the
same shape as the QA tree (`T:\a_p_r_i_r_QA`) and the PROD tree (`G:\a_p_r_i_r_PROD`), plus `deploy\` and
`tests\`. Everything outside this folder, at the top of the repository, is the first system and the engine as it
was reviewed, frozen: it is the reference for the comparison of the scheme's section 9.

## Where the work stands

- **Step 1 (done):** the engine, its 40 methods in 12 families and its tests copied here byte for byte.
- **Step 2 (this state): the engine simplified.** Nothing is sealed, chained or refused because it differs: the
  research job makes again whatever is out of date. The science is the frozen engine's: the reader and the
  permitted view, the readout and its tie order, one target's forecast, scoring, the divisions and the OV-1
  arithmetic are the same programs (`deploy\compare_with_frozen.py code` lists every file by how it differs).
- **Step 3 (done): the results updater in this tree** (`src\updater\results_updater.py`,
  `Run_Results_Updater.bat`): the first system's reviewed updater with every Mode H state taken out and nothing
  else changed. The research job runs it at its start unless `--no-update`.
- **Step 4a (done): what touches only its own tree.** The settings file in its new form and the four rules by
  which a folder is, or is not, the tree its file says; one lock for every command; a backup at the end of every
  job; `Backup.bat`; and in DEV `Make_Installable.bat` and `Who_Uses.bat`.
- **Step 4b (done): the commands that touch another tree,** all run from DEV: `Create_Tree.bat`, `Install.bat`,
  `Retire.bat`, `Copy_From_PROD.bat` and `Restore.bat`.
- **Still to come:** the rehearsal on the owner's PC (step 5), the real trees (step 6), the how-to (step 7).

## The settings file, and how a tree knows which tree it is

`ENVIRONMENT.ini`, at the tree's root, has the same form in every tree: this tree's `role`, then for each of DEV,
QA and PROD its `tree_root` and `backup_root`. In DEV it is made by copying `ENVIRONMENT.example.ini`; Git ignores
it. Every command works on the folder its own launcher lies in, and first checks that folder: the role must be
the ending of the folder's name, and that role's `tree_root` must be that folder. No two trees share a folder,
none lies inside another, and no backup folder lies inside a tree. A folder that fails any of this runs nothing.

Then the command takes the tree's one lock, `records\TREE.lock`. While it exists every other command in that tree
refuses. A lock left by a command that was killed is deleted by hand, once nothing of the tree is running. The one
exception is `Who_Uses.bat`, which only reads and prints: it makes the same check of the folder but takes no lock.

## What the research job does (`Run_Research.bat`)

`Run_Research.bat [--game POWERBALL|OZLOTTO|BOTH] [--no-update] [--rebuild family/variant ...] [--rebuild-all]`

For each game: fetch new official results with the tree's updater (unless `--no-update`); read the results on
file; delete what is out of date and only that; forecast every draw a method has no line for, the next draw
included; score every forecast whose result is on file; make the league, the
reports and both OV-1 series again; add one line to `records\JOB_LOG.jsonl`; make a backup. What is out of date:

| What changed | What is made again |
|---|---|
| the engine (any file under `src\` outside the method families), or `--rebuild-all` | everything, both games (stored results of methods the tree has no software for included) |
| a method's files (its fingerprint is not the one in the first line of its stored lists), or `--rebuild` names it | that method |
| a list that cannot be read or does not follow on | that method |
| a draw's result corrected at the source | that draw's scores, and every forecast computed from it |
| a method retired | what it held for its retirement draw or a later one is dropped |
| a report the records no longer give (a draw no longer on file, say) | it is removed |

If the updater does not finish (the site is down, a page cannot be read, a draw disagrees), the job says so
loudly, goes on with the results the tree holds, and ends with exit code 1. A method whose calculation fails
writes no line; it is reported, and the job goes on with the others (exit code 1 again). An ordinary
job leaves alone the stored results of a method the tree has no software for, and counts them nowhere.

## The three small files beside a method (`src\methods\<family>\<variant>\`)

Plain text, one `key = value` a line; none is part of any fingerprint. All three are kept in Git (the owner,
decision log entry 352).

- `I_AM_INSTALLABLE`: written by "make installable" (step 4).
- `I_AM_RETIRED`: `retired_from_POWERBALL = 1601`, `retired_from_OZLOTTO = 1712`, `reason = ...`. The method makes
  no forecast for those draws or later ones; its results for earlier draws stay, and anything it held for those
  draws or later is dropped (so a retired method and the same method rebuilt hold the same history). An empty file
  made by hand retires it from the next draw (the job writes the draw in). Deleting the file brings the method
  back.
- `IN_PLACE_SINCE`: written by the job: the method's fingerprint, and for each game the last draw the tree held
  when this version of the method was first used here. Bookkeeping only: the second OV-1 series counts a method
  from the draw after it. A file that cannot be read never stops its method: the job writes it afresh and says so.

## Backups (`Backup.bat`, and the end of every job)

A backup is one plain ZIP of the whole tree at maximum compression, in the tree's backup folder, named with the
role, the date and time and why it was made (`PROD_20261201_201012_after_job.zip`). It leaves out `.venv` (rebuilt
by the two environment scripts; the job log records the versions) and the lock file. Any ZIP program opens it.
None is ever written over or deleted by this project. If the backup at the end of a job cannot be made, the job
says so loudly and ends with exit code 1; what it computed stands. A folder or file of the tree that cannot be
read fails the backup: none is ever made that silently lacks part of the tree.

## DEV's own commands

- `Make_Installable.bat family/variant ... | ALL | INFRA` writes the flag `I_AM_INSTALLABLE` beside each method
  named (ALL: every method) with the method's fingerprint, and for INFRA once in `src\` with the engine's
  fingerprint, the updater's and the root launchers'. A flag is out of date as soon as a file it vouches for
  changes. (Only the engine's fingerprint makes results again; the other two only decide what may be installed.)
- `Who_Uses.bat helper_file` lists every method that uses a helper file. It changes nothing and takes no lock.

## DEV's commands that touch another tree

Each first reads the other tree's own settings file and requires the role meant and the same places as DEV's
file; takes the lock of every tree it touches; and makes a backup of a tree before it replaces anything there.
If that backup cannot be made, nothing is replaced. None of them asks a question: what protects a tree is the
backup, and `Install.bat --show`.

- `Create_Tree.bat QA|PROD` makes a new tree in a folder that is absent or empty: DEV's flagged infrastructure,
  every method that is flagged and not retired, and DEV's accepted results. The settings file is written last, so
  a half-made folder is not a tree. Then, in the new tree: `create_venv.bat`,
  `install_upgrade_dependencies_into_venv.bat`, `Run_Research.bat --no-update`.
- `Install.bat QA|PROD [--show]` replaces the infrastructure if it is flagged and differs, and replaces or adds
  every flagged method that differs or is missing; then it runs the destination's own job (`--no-update`) under
  the lock it holds, which makes again whatever the new software changes. It waits for that job however long it
  takes and never ends it: Ctrl+C in the installing window only prints that the job is still working. A part
  whose flag is missing or older than its files is named and left alone (the launchers at the tree's root are
  part of what the INFRA flag vouches for). A helper file several methods share goes in only together with every
  method of the destination that uses it (so flag them all: `Make_Installable.bat ALL`). A retired method is
  never added. A method only the destination has is left alone. None of the three small files is copied.
  `--show` prints what would be done and changes nothing.
- `Retire.bat family/variant reason` writes `I_AM_RETIRED` beside the method in every tree that has it, from that
  tree's own next draw, after a backup of each. The tree's next job drops what the method had from that draw on.
- `Copy_From_PROD.bat software|data|both QA` makes QA's software, its data (`source_data` and
  `results\research`) or both the same as PROD's; `Copy_From_PROD.bat data DEV` copies the data into DEV. Then
  the destination's own job runs. With the software go PROD's `I_AM_RETIRED` and `IN_PLACE_SINCE` files, so that
  after `both` QA is PROD's twin and its job finds nothing to make again. Before anything is touched, PROD's
  accepted results of both games must pass the engine's own reader and PROD must hold what is to be copied. The
  one thing this command writes in PROD is its lock file, removed when the command ends.
- `Restore.bat QA|PROD backup.zip` puts a tree back from one of its own backups (a file name in that tree's
  backup folder, or a full path). The ZIP must read back whole and its own settings file must name that tree. It
  is unpacked into a fresh folder; the tree as it was is renamed aside (`..._set_aside_<date>_<time>`, where
  nothing can run) and never deleted; the fresh folder takes the tree's name. Then the tree's `.venv` is built
  again. DEV is not restored this way: its software is in Git. **A tree so damaged that its settings file cannot
  be read** is not touched by this command: rename its folder aside by hand (to a name that does not end with
  its role), then run `Restore.bat`, which restores into the place that is now empty.

Exit codes: 0 done; 1 done, but the destination's job did not finish cleanly; 2 refused before anything was
changed, or failed part way (the message, in capitals, says what state the tree is in and what to do).

## The results updater (`Run_Results_Updater.bat`)

`Run_Results_Updater.bat [--games POWERBALL,OZLOTTO] [--months-back 5] [--browser chrome|firefox] [--pause 2]`

It fetches the results of the last few months from the one official source (Lotterywest's own results search on
`www.lotterywest.wa.gov.au`, https, a headless real browser, at least 2 seconds between pages, a block page means
STOP), requires every fetched draw the tree already holds to agree with the tree's file, and appends the new
draws to this tree's `source_data` only. It keeps what it fetched (`source_data\grabs`) and the file as it was
(`source_data\backups`), and adds one line to the game's ledger. Started by itself it holds the tree's lock, so
it never runs while a research job does. **Only the project owner ever runs it against the real site;** every
test reads invented pages.

It is not part of the engine's fingerprint: a change to the updater makes no research again.
`deploy\compare_updater_with_frozen.py` shows that it is the reviewed updater with its Mode H states out:
definition by definition, and by running both on the same invented pages.

## Tests

In this folder, with this tree's Python:

    set PYTHONPATH=src;src\methods;tests
    .venv\Scripts\python.exe -B -m unittest discover -s tests -p "test_research_*.py"

Everything runs on invented draws and toy methods.

## The comparison with the frozen engine (`deploy\compare_with_frozen.py`)

It runs each engine in its own Python process and compares what the two trees then hold: every forecast, every
score, both OV-1 series line by line, and every report file byte for byte. (The frozen engine stores no file of
its series over all draws; the tool has the frozen engine's own code make it from the frozen tree's stored lists.)

- `invented <new folder>`: the whole comparison on invented results with the real methods (two trees are made in
  the folder; about as long as two first fills).
- `run <tree> --game BOTH --no-update`, `trees <frozen tree> <new tree>`, `align <frozen tree> <new tree>` and
  `code <frozen tree> <new tree>`: the same steps one at a time, for a comparison on the accepted results.

## Not kept in Git

This tree's `ENVIRONMENT.ini`, `.venv`, `source_data`, `results`, `records`, `scratch` and `transitory_data`
(see `.gitignore` here).

## Its Python environment

Built in this folder by the two scripts that lie in it, run in a plain CMD window with no environment active:
`create_venv.bat`, then `install_upgrade_dependencies_into_venv.bat`. Each works on the folder it lies in.
