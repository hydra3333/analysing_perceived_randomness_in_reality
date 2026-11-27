# H-1 v17 - the Claude web chat's handover (short form)

Version v17, 27 November 2026. Written by the Claude web chat (primary designer and coder) on Opus, at the owner's
go (decision log entry 366), for the next Claude chat. It replaces H-1 v16r1 (RAT-62), written before steps 3 and 4
were built. **Status: CANDIDATE for owner ratification.**

## 0. What this is, and what to read

This is the short handover of the simple scheme. **The decision log is the full record; this document is an index
to it, not a substitute.** H-1 v16r1 and every earlier handover stay in Git as history; read them only to answer a
question about the past.

Read, in this order, and check what you read against the repository:

1. This document.
2. **The design in force:** `exchange/Claude_The_Simple_Scheme_v0_2_20261126.md`
   (SHA-256 `15f52cabb54068860f439cb69a8480067a8e688b3c85107988743ecba38a1a77`; agreed by the owner, entry 344).
   About 12 pages. **Its work order (section 12) for steps 5 and 6 is replaced** by the owner's of entry 365
   (section 8 below).
3. **Step 2 as done:** `exchange/Claude_Step_2_Engine_Simplified_And_Compared_v0_1_20261126.md` (its section 4 was
   ratified as RAT-61).
4. **The owner's reframing**, which is why the scheme exists:
   `exchange/Claude_Comment_On_The_Owners_Reframing_Back_To_The_Research_v0_1_20261126.md` (it carries his words).
5. **The decision log from entry 330** (`exchange/DECISIONS/DECISION_LOG.md`, the pause) to the last entry. Entries
   351 to 366 are the work since H-1 v16r1 (section 6 lists them).
6. The top block of `exchange/CONTINUITY_NOW.md` ("For the owner: NOW"). Below it the page is mostly history.
7. **The coding standards, binding on every line of code you write:** `doc/CODING_PRACTICES_v0_1.md` (RAT-40) and
   `doc/FILE_FORM_STANDARD_v0_2.md` (RAT-49) as the scheme changed it. Section 9 says how they apply now.
8. `a_p_r_i_r_DEV/README.md` (it describes every command), then the code in `a_p_r_i_r_DEV/src/research/` and
   `a_p_r_i_r_DEV/deploy/`.
9. `exchange/OWNER_REMINDERS.md` (what you have promised to remind the owner of, and when).

## 1. The project and the roles

The question: do Australian Powerball and Oz Lotto results hold patterns that conventional statistics missed? The
expected outcome is a carefully measured null. It is speculative research, and the owner wants it run as research:
**the science must be right; the administration small** (his reframing of 26 November 2026, entry 330).

- **The project owner** (GitHub `hydra3333`): sole decider and authoriser. **Never write his personal name in
  anything committed.** He relays between the two AI chats.
- **The Claude web chat (you):** the primary designer and coder.
- **The ChatGPT chat:** the independent reviewer. Its handover in force is H-2 v10
  (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v10_20261127.md`, RAT-63). It has written an H-2 v11 candidate and
  blurb (`exchange/HANDOVER_2026_11_27/ChatGPT_Reviewer_Handover_H2_v11_20261127*.md`, not yet ratified) and will
  refresh it before the Windows rehearsal. It commits its own files; never edit them.
- **Claude Code on the owner's PC:** a local runner only. It carries out task files the web chat writes, under its
  rulebook (`CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`). **v0.7 is in force and names the 22 November design;** a
  v0.8 candidate for the simple scheme is being written (section 8, item 1). The runner never runs the results
  updater, anywhere.

## 2. The hard rules (binding)

- The one production results source is Lotterywest-GOV (`www.lotterywest.wa.gov.au`, HTTPS), reached only by the
  owner's approved tools. You never contact any lottery website, and you never search for lottery results.
- **The new updater has never fetched from the real site.** Neither AI nor the runner ever runs it or lets it reach
  the site. Every test and tool uses invented pages, and replaces the real-browser class with one that refuses.
  The first real fetch is the owner's own, by itself in DEV (entry 358).
- You may read draw values, `source_data/` and `results/`. You never write there. Anything you work out in the chat
  from draw values is labelled "suggestive"; results count only from the reviewed programs.
- Method-facing N-1 isolation is never weakened (a method sees only the draws before its target). Games are never
  pooled. The sealed Mode H records of the first system are never altered.
- No program ends another process. In the frozen top level, three safety switches of the first system stay False,
  its allowlist stays empty, and its orphan marker blocks launches; nothing clears or bypasses it. **In the new
  trees the orphan-marker check is dropped** (entry 353).
- Nothing runs on the owner's PC without his go. No install, run, backup, restore, migration or deletion without his
  separate approval. Nothing ever changes his PC's date, time or time zone. A STOP is a STOP.
- **Commits.** You commit and push documents and records yourself (named paths only; fetch and look at
  `git status -sb` and `git log HEAD..origin/main` first; nothing deleted or overwritten): under `exchange/` and
  `CLAUDE_CODE_WORKING_FOLDER_TREE/` freely, into `doc/` only once ratified. **Code: you commit the living system's
  code directly into `a_p_r_i_r_DEV/` on `main`** (entry 342), named paths only; the reviewer reads the commit; the
  owner pulls. The top level (`src/`, `tests/`, `.claude/` and the rest) is frozen: never change it unless the owner
  asks for that one change (as he has for two lines of `.claude\settings.json`, entry 366). You never write under
  `transitory_data/` or `GAIS/`.
- A PASS or an agreed design authorises no install or run.

## 3. How the owner works

- Plain step-by-step English. Decisions as: the question, why it matters, your recommendation, the options.
- Verify, don't assert: compute hashes, counts and comparisons with a tool. Show your reasoning, alternatives and
  uncertainties; he sometimes spots something important from them.
- **At every point, say what you think he should do next** (entry 335; he asks the reviewer the same).
- End anything to be relayed with a short paste-ready block for the reviewer chat.
- Discuss his queries with him first; issue an EX message only when he asks. When he relays the reviewer's
  recommendations without words of his own, they are not yet his decision: ask him.
- **Do not over-engineer.** Tell him the simplest safe route first. Admin that does not serve the science or
  recoverability is not wanted. This is not a request for shorter reporting.
- A short "how the process went" note at milestones.
- **Tell him before any run or wait longer than a few minutes** what is running and about how long (he once waited
  ninety minutes without word; entry 362).
- **Model rule:** before designing a new subsystem or a major change, a statistical validity question, the root
  cause of an unexplained STOP, or a cold read of a design, say "Suggest switching to Fable (High) for this" and wait
  for his go. Tell him when a Fable task is finished. Save Fable for the hard parts; everything else runs on Opus.
- Watch the chat's length: say when a handover update is due, before the chat runs out.

## 4. How we got here (one paragraph)

The first system (the coordinator, method contracts, Mode H's sealed holdout) was replaced by a redesign ratified on
22 November 2026 (RAT-40). On 26 November 2026 the owner found that design had outgrown the research and paused
everything (entry 330); owner, reviewer and Claude agreed **the simple scheme v0.2** the same day (entry 344). On 26
and 27 November its steps 1 to 4 were built in `a_p_r_i_r_DEV/`, each read once by the reviewer and corrected, and
the reports' wording was changed. What remains before the research resumes is the rehearsal on the owner's PC and
the making of the real trees.

## 5. The design in force, in brief

Read the scheme and `a_p_r_i_r_DEV/README.md` for the whole; this is its spine, as built.

- **Kept from specification v0.6, unchanged:** N-1; TOP and WORST from the same model for a target; games never
  pooled; the methods, readout and tie order; scoring and divisions; the league measures; the OV-1 arithmetic.
- **Principles:** what a tree does follows from the software in it, not its name; everything a tree computes can be
  made again, so nothing is sealed or chained, and a difference never refuses: it means "make that again".
- **Three trees, one shape, the role as the end of the folder name:** DEV =
  `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV`; QA = `T:\a_p_r_i_r_QA`;
  PROD = `G:\a_p_r_i_r_PROD`; backups in `T:\a_p_r_i_r_backups\DEV`, `\QA` and `\PROD`. Neither QA nor PROD exists.
- **The settings file** (`ENVIRONMENT.ini`, the same form in every tree: `[environment] role`, then `[DEV]`, `[QA]`,
  `[PROD]` with `tree_root` and `backup_root`) and **the four identity rules** (`src/research/settings.py`). A tree's
  `.venv` is `<tree>\.venv`.
- **One lock per tree,** `records\TREE.lock`, taken by every command (`src/research/tree_lock.py`); `Who_Uses` alone,
  which only reads, takes none. Each lock file holds a key; a command of DEV that runs another tree's job starts
  it with `--under-lock <key>`, and the job works only under that lock and leaves it in place. A lock left by a
  killed command is deleted by the owner by hand.
- **Three small files beside each method,** all kept in Git in DEV (entry 352): `I_AM_INSTALLABLE` (made by
  `Make_Installable`), `I_AM_RETIRED` (a retired method keeps neither forecasts nor scores from its retirement draw
  on; entry 353), `IN_PLACE_SINCE` (the establishment draw; bookkeeping only). The infrastructure's flag
  (`src\I_AM_INSTALLABLE`) holds three fingerprints: the engine's, the updater's and the root launchers'.
- **The engine's fingerprint** covers every file under `src\` outside the method families and outside `src\updater`
  (entry 356); `reports.py` is inside it. A change to it makes everything again in a tree's next job.
- **The research job** (`Run_Research.bat`; `src/research/research_job.py`): the tree's first step and lock; the
  updater per game unless `--no-update` (a failure warns loudly, the job goes on with the accepted results and ends
  with exit code 1; after a website "Stop" nothing more is fetched in that job); delete what is out of date; catch
  up, the next draw included; league, reports, both OV-1 series (both exploratory); one job-log line; a backup.
- **The updater** (`src/updater/results_updater.py`): the first system's reviewed updater with every Mode H state
  removed by exact removals, its own lock removed (the caller holds the tree's), and a second final-URL check before
  parsing. `deploy/compare_updater_with_frozen.py` proves it on invented pages: RESULT: SAME.
- **Backups** (`src/research/backup.py`): one plain ZIP at maximum compression, without `.venv`, the lock and caches,
  never written over or deleted; after every job (a failure: loud warning, exit code 1, results stand), before
  every replacement (a failure stops it), on demand (`Backup.bat`). An unreadable folder fails a backup.
- **DEV's commands** (`deploy/dev_command.py`, `dev_tools.py`, `install_tools.py`, `tree_tools.py`, `tree_parts.py`):
  `Make_Installable`, `Who_Uses`, `Create_Tree QA|PROD`, `Install QA|PROD [--show]`, `Retire`, `Copy_From_PROD
  software|data|both QA` and `data DEV`, `Restore QA|PROD <zip>`. Each reads the other tree's own settings first,
  locks every tree it touches, and backs a tree up before replacing anything in it. The owner accepted Claude's
  choices (entries 362 and 365): a helper shared by several methods goes in only with every method of the
  destination that uses it; a retired method is replaced if flagged and differing, never added; `both` copies with
  one backup and one job, PROD's `I_AM_RETIRED` and `IN_PLACE_SINCE` going with the software; no typed
  confirmations; Restore unpacks into a fresh folder and renames the old tree aside, never deleting it; Retire runs
  no job; the one write in PROD during Copy_From_PROD is its lock file. A tree's job is waited for in steps that
  never end it: Ctrl+C only says it is still working.
- **The reports' wording** (entry 366): "retired" and "method"; the second OV-1 series' text, the reviewer's own,
  says it is exploratory and claims no error bound; "numerical lower bound"; nothing is set aside.
- **The proof (scheme section 9):** `deploy/compare_with_frozen.py` (`invented`, `run`, `align`, `trees`, `code`):
  from the same accepted results the simplified engine gives the same forecasts, scores, both OV-1 series and,
  through a declared list of wording changes (`WORDING_CHANGES`, 21 kinds), the same report files as the frozen
  engine at the top level.

## 6. Where things stand (27 November 2026, evening)

- **Steps 1 to 4 are built, read by the reviewer and corrected,** and the reports' wording is changed. 280 tests
  pass in `a_p_r_i_r_DEV`. Evidence class: cloud only (Linux, Python 3.15.0b4). **Nothing has run on Windows.**
- **The engine comparison on the accepted results says RESULT: SAME** on the engine of `42bb082` (Powerball 15,118
  forecasts and 15,078 scores, Oz Lotto 6,598 and 6,558, 40 methods a game, 901 and 475 report files byte for
  byte), and on the wording commits with the reports remade from the stored results.
- **Nothing is authorised on the owner's PC.** No tree exists but DEV, and DEV has no results yet.

| Entry | What |
|---|---|
| 351-352 | H-1 v16r1 (RAT-62); all three small files in Git; the reviewer's reading of step 2 |
| 353 | a retired method drops its forecasts too; the orphan-marker check dropped in the new trees |
| 354-355 | step 2 corrections; H-2 v10 (RAT-63) |
| 356-359 | step 3, the updater: four points confirmed, built (`d4f01e0`), read, corrected (`2ebbb11`); entry 358: the owner's first real fetch is his own, by itself in DEV |
| 360-363 | step 4a: settings, lock, backups, DEV's own commands (`3effdbe`); choices accepted (exit 1 after a failed backup); read and corrected (`e452f32`) |
| 364-365 | step 4b: the five cross-tree commands (`42bb082`); read; F01 to F04 corrected (`068c93f`); choices accepted; the lock in PROD; the reversed seeding; **the work order from here** |
| 366 | the reports' wording (`168b896`, `56cc3ec`); the three rehearsal decisions; GO for this handover, the rulebook v0.8 candidate and the task files |

## 7. Where everything is

| What | Where |
|---|---|
| The living system (DEV tree) | `a_p_r_i_r_DEV/` (`src/research/` engine; `src/updater/`; `src/methods/` 40 methods in 12 families; `deploy/`; `tests/`; the launchers at its root) |
| The comparison tools | `a_p_r_i_r_DEV/deploy/compare_with_frozen.py`, `compare_updater_with_frozen.py` |
| The file-form checker | `a_p_r_i_r_DEV/deploy/file_form.py` (everything CRLF and ASCII, `.jsonl` included) |
| The frozen reference | the top level: `src/`, `tests/`, `Run_Research.bat`, the updater `src/results_master_v0_2.py` |
| The runner's rulebook and tasks | `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (v0.7); `inbox/TASK_Tnnn.md` (last T028); `outbox/` reports; `tools/cc_clone.py`; `.claude/settings.json` (its permissions) |
| Decisions | `exchange/DECISIONS/DECISION_LOG.md` (LF; appended as bytes) |
| The continuity page | `exchange/CONTINUITY_NOW.md` (LF; its top block is current) |
| Standing reminders | `exchange/OWNER_REMINDERS.md` |
| Handovers | in force in `doc/HANDOVER/`; candidates in `exchange/HANDOVER_2026_11_27/` |
| EX messages | `exchange/EX_nnn_<author>.md` (latest EX_333, now history; the lighter process uses few) |
| Science kept | `doc/Predictive_Randomness_System_Specification_v0_6.md` (its science sections only) |
| Coding standards (binding) | `doc/CODING_PRACTICES_v0_1.md`; `doc/FILE_FORM_STANDARD_v0_2.md` as the scheme changed it |

**Running the tests** (in `a_p_r_i_r_DEV`): `PYTHONPATH=src:src/methods:tests python -B -m unittest discover -s
tests -p "test_research_*.py"` (on Windows `set PYTHONPATH=src;src\methods;tests`). About two minutes; all on
invented draws; no test lets the real updater run.

**The cloud workspace does not carry over between chats.** To repeat the comparison on the accepted results: clone
`main` twice (or once and copy). In one copy (the frozen tree) give the top level an `ENVIRONMENT.ini` in the
first system's form (`[environment]` with `role = DEV`, `tree_root` that folder, `venv_dir` its `.venv`). Make a
second tree whose folder name ends `_DEV`, holding a copy of `a_p_r_i_r_DEV/src`, the four files of
`source_data/` and an `ENVIRONMENT.ini` in the new form (QA and PROD pointing at folders that need not exist; backup
folders outside all three). Then `compare_with_frozen.py run <tree> --game BOTH --no-update` on each (about 30
minutes each in the cloud), `align`, `run` on each again, `trees`. Use Python 3.15 with the packages of
`requirements.txt`. Read `source_data` only; never write there. **A quick recheck after a change to `reports.py`
alone:** copy the new `src` into the second tree, set its stored engine fingerprint (`results/research/
INFRASTRUCTURE`, by `code_identity.store_fingerprint`) to the new engine's, run its job (about 3 minutes: only the
reports are made again) and `trees`. Say so when you use it; the owner's PC makes everything from nothing.

**The updater file** was made by a workspace script of scripted exact removals from the frozen updater; the script
did not carry over. Edit `src/updater/results_updater.py` directly, and keep `compare_updater_with_frozen.py`'s
declared lists of changed and removed definitions up to date.

## 8. What comes next: the work order (the owner, entry 365)

1. **Before the rehearsal (Claude, Opus; the owner's go of entry 366):**
   - **the runner's rulebook v0.8 candidate,** for the reviewer's one reading and the owner's ratification. It names
     the simple scheme's trees, real paths and ten commands; it says plainly which commands are never run against
     a real tree, which a task file names for a scratch tree, and that the real updater is never run anywhere (its
     only use is inside the test suite, on invented pages). In the scratch folder: scratch trees named
     `<x>_<ROLE>` with scratch-only settings and backups; `TMP`/`TEMP` inside the scratch folder for the test suite;
     the runner may copy real DEV's `source_data` and `results\research` into the scratch folder by reading; and,
     for TASK_T031 only, real DEV's own Python as the interpreter for calculations on scratch trees (`-I -B`; no
     install, no change to DEV). Rule 10's known-failure exception goes;
   - **two lines in `.claude\settings.json`** (the owner asked, entry 366): deny a command naming `results_updater`,
     or the `T:\` or `G:\` drives; check the patterns refuse those and do not stop the tests on invented pages;
   - **the task files:** TASK_T029 (the test suite on Windows, in a scratch DEV tree that builds its own `.venv`
     with its own two scripts); TASK_T030 (the ten commands on three scratch trees with **invented results**, the
     Windows restore and the child-process job included, a few planted refusals); TASK_T031 (after item 3: the
     comparison in the scratch folder).
2. **The rehearsal:** T029, then T030, run by the runner on the owner's go.
3. **The owner runs DEV's first fill himself:** the accepted results into `a_p_r_i_r_DEV\source_data`, his
   `ENVIRONMENT.ini` from the example, then `Run_Research.bat --no-update` (about 47 minutes). After it, the 40
   `IN_PLACE_SINCE` files are committed.
4. **T031, the comparison:** the runner copies DEV's `source_data` and `results\research` into the scratch folder by
   reading, makes a frozen tree there, runs the frozen engine with real DEV's own Python, aligns (the alignment's
   artificial `IN_PLACE_SINCE` stay in the scratch folder), runs both again and compares.
5. **The owner accepts the Windows comparison.**
6. **The owner runs `Run_Results_Updater.bat` by itself in DEV, the first real fetch** (entry 358; remind him then),
   and looks at what it prints, the new ledger line, the grab and backup under `source_data`; only then a job that
   fetches.
7. **QA, then PROD:** `Make_Installable.bat ALL INFRA`, `Create_Tree.bat QA` (then its `.venv` and first job, the
   same care before its first fetching job), then PROD. After this the top-level `.venv` can go.

**Then, step 7 of the scheme, tidying:** a few pages of how-to; this handover brought up to date; the decision log
and the continuity page converted to CRLF (and the continuity page cut down to what is current); **the three
revisit the operations manual** (entry 343); **a decision on the frozen top level** (keep as history, or move aside).

**Then step 8, the research.** New methods. First, together, **the three deferred discussions**: the future-method-
priorities draft (`doc/Predictive_Randomness_Future_Method_Priorities_v0_1_DRAFT.md`, entry 289); the roles of the
two AIs (entry 292); and each AI's minimal additions to `doc/CODING_PRACTICES_v0_1.md` (entry 299). **Only if it
matters then:** a job with nothing to do takes about two minutes, because every league report is made again.

## 9. Working practices

- **The coding practices** (`doc/CODING_PRACTICES_v0_1.md`, RAT-40) apply to all code: a plain-English header on every
  `.py` file (what it is for, which part of the design it carries out, which project modules it uses and for what,
  what uses it); constants at the top with a comment; a comment on every function saying what it does, each
  parameter, what it returns with an example, and what makes it refuse; names that say what a thing is; messages
  that say what happened, where, why and what to do; nothing swallowed; one shared piece of code per shared task;
  each test named for the rule it proves, with a planted fault. **Every code commit says "coding practices met" or
  lists the exceptions with reasons;** the reviewer checks code against them. Under the scheme, read three items
  this way until the owner ratifies a revision: a header names the scheme's section where the part is
  administrative; "held or not current" becomes "rebuilt"; and "a variant's files can never change once installed"
  no longer holds (a changed method is rebuilt). Lines of code at most 120 characters (tests 140; a file that came
  from the frozen top level keeps its own long lines).
- **Proving a change:** plant each fault the change guards against, one at a time, and show the tests catch it
  (done for every finding of steps 4a and 4b). Run pyflakes, the file-form checker over every tracked file of
  `a_p_r_i_r_DEV`, and the whole suite before each code commit.
- **The file form:** every text file of the living system is CRLF and ASCII, the `.jsonl` records included. The
  frozen top level is not changed.
- **The decision log:** record every owner decision at once, in his words, with the time read from the clock
  (`TZ=Australia/Adelaide`) in the command that writes it. Each entry ends "Next numbers: ...". Check the file ends
  with the expected line before appending.
- **The continuity page:** a new bullet at the top of "For the owner: NOW" and the "Last updated" line, at each
  milestone.
- **Git:** fetch, then look at `git status -sb` and `git log HEAD..origin/main` before each commit (the reviewer
  commits too: a push was refused twice because of its commits; rebase your own commit on top and push). Look at
  `git diff --cached --stat` before committing. Never type a hash or a time: compute them.
- **Documents:** every new text file CRLF and ASCII; the decision log and the continuity page are LF until the
  tidying. Lines of documents at most 120 characters.
- **Commit trailer:** the attribution lines the session gives you.
- **Numbers now:** next EX is EX_334 (Claude's); next decision log entry 367; next ratification RAT-64.

## 10. Taking over

1. Add the repository (push access) and read section 0's list. Check this document's statements against the
   repository; do not take summaries on trust.
2. Give the owner your first reply: what you understand the state to be, what is and is not authorised, the next
   deliverable, and anything unclear or inconsistent. Build and commit nothing yet.
3. The owner decides whether to accept the takeover. He may ask the reviewer to put a few questions to you first.

END.
