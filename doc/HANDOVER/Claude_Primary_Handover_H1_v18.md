# H-1 v18 - the Claude web chat's handover (short form)

Version v18, 28 November 2026. Written by the Claude web chat (primary designer and coder) at the owner's word
("time for you to update you handover fully too", decision log entry 391), for the next Claude chat. It replaces
H-1 v17r1 (RAT-64), written before the rehearsal on the owner's PC, DEV's first fill and the first real fetch.
**Status: RATIFIED by the owner, RAT-68 (decision log entry 392).**

## 0. What this is, and what to read

This is the short handover of the simple scheme. **The decision log is the full record; this document is an index
to it, not a substitute.** H-1 v17r1 and every earlier handover stay in Git as history; read them only to answer a
question about the past.

Read, in this order, and check what you read against the repository:

1. This document.
2. **The design in force:** `exchange/Claude_The_Simple_Scheme_v0_2_20261126.md`
   (SHA-256 `15f52cabb54068860f439cb69a8480067a8e688b3c85107988743ecba38a1a77`; agreed by the owner, entry 344).
   About 12 pages. **Its work order (section 12) for steps 5 and 6 was replaced** by the owner's of entry 365
   (section 8 below), of which items 1 to 6 are done.
3. **Step 2 as done:** `exchange/Claude_Step_2_Engine_Simplified_And_Compared_v0_1_20261126.md` (its section 4 was
   ratified as RAT-61).
4. **The owner's reframing**, which is why the scheme exists:
   `exchange/Claude_Comment_On_The_Owners_Reframing_Back_To_The_Research_v0_1_20261126.md` (it carries his words).
5. **The decision log from entry 330** (`exchange/DECISIONS/DECISION_LOG.md`, the pause) to the last entry. Entries
   367 to 391 are the work since H-1 v17r1 (section 6 lists them).
6. The top block of `exchange/CONTINUITY_NOW.md` ("For the owner: NOW"), and its sections "If a chat ends" and
   "Installed handovers". The rest of the page is mostly history.
7. **The coding standards, binding on every line of code you write:** `doc/CODING_PRACTICES_v0_1.md` (RAT-40) and
   `doc/FILE_FORM_STANDARD_v0_2.md` (RAT-49) as the scheme changed it. Section 9 says how they apply now.
8. `a_p_r_i_r_DEV/README.md` (it describes every command), then the code in `a_p_r_i_r_DEV/src/research/` and
   `a_p_r_i_r_DEV/deploy/`.
9. **The runner's rulebook v0.8** (`CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`) and the three rehearsal reports
   (`CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T029.md`, `REPORT_T030.md`, `REPORT_T031.md`).
10. `exchange/OWNER_REMINDERS.md`, item R-030 (what you have promised to remind the owner of, and when).

## 1. The project and the roles

The question: do Australian Powerball and Oz Lotto results hold patterns that conventional statistics missed? The
expected outcome is a carefully measured null. It is speculative research, and the owner wants it run as research:
**the science must be right; the administration small** (his reframing of 26 November 2026, entry 330).

- **The project owner** (GitHub `hydra3333`): sole decider and authoriser. **Never write his personal name in
  anything committed.** He relays between the two AI chats.
- **The Claude web chat (you):** the primary designer and coder.
- **The ChatGPT chat:** the independent reviewer. Its handover in force is **H-2 v12**
  (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v12_20261128.md` and its introductory blurb beside it; written and
  installed by the reviewer at `436f05e` and `e3b14c7`; ratified by the owner, RAT-67, entry 390; current to entry
  389). H-2 v11 (RAT-65) is history. It commits its own files; never edit them. Open reviewer findings: none.
- **Claude Code on the owner's PC:** a local runner only. It carries out task files the web chat writes, under its
  rulebook, **v0.8, in force (RAT-66, entry 370)**, and behind the permission settings of `.claude\settings.json`
  (edition r2, entry 375). It never works in a real tree, never touches the `T:` or `G:` drives, and never runs the
  results updater, anywhere. Its scratch folder is `D:\DELETE_ME\`.

## 2. The hard rules (binding)

- The one production results source is Lotterywest-GOV (`www.lotterywest.wa.gov.au`, HTTPS), reached only by the
  owner's approved tools. You never contact any lottery website, and you never search for lottery results.
- **Only the owner runs the results updater.** Neither AI nor the runner ever runs it or lets it reach the site.
  Every test and tool uses invented pages, and replaces the real-browser class with one that refuses. The owner
  made its first real fetch himself, by itself in DEV, on 28 November 2026 (entry 386). **The same care is owed
  before the first fetching job in QA and in PROD** (entry 358): the updater by itself first, a look at what it
  wrote, only then a job without `--no-update`.
- You may read draw values, `source_data/` and `results/`. You never write there. Anything you work out in the chat
  from draw values is labelled "suggestive"; results count only from the reviewed programs. Keep draw values out of
  the decision log and the other records.
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
  asks for that one change (as he did for the permission guards in `.claude\settings.json`, entries 366, 373 and
  375). You never write under `transitory_data/` or `GAIS/`.
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
  ninety minutes without word; entry 362). When he runs something long himself, tell him when to expect its end.
- **He reads the output himself and spots what is odd** (the progress line of entry 387). Read the code before you
  answer such a finding, and say plainly whether it is a fault of wording or of what was computed.
- **Model rule:** before designing a new subsystem or a major change, a statistical validity question, the root
  cause of an unexplained STOP, or a cold read of a design, say "Suggest switching to Fable (High) for this" and wait
  for his go. Tell him when a Fable task is finished. Save Fable for the hard parts; everything else runs on Opus.
- Watch the chat's length: say when a handover update is due, before the chat runs out.

## 4. How we got here (one paragraph)

The first system (the coordinator, method contracts, Mode H's sealed holdout) was replaced by a redesign ratified on
22 November 2026 (RAT-40). On 26 November 2026 the owner found that design had outgrown the research and paused
everything (entry 330); owner, reviewer and Claude agreed **the simple scheme v0.2** the same day (entry 344). On 26
and 27 November its steps 1 to 4 were built in `a_p_r_i_r_DEV/`, each read once by the reviewer and corrected. On
the evening of 27 November the runner rehearsed it on the owner's PC (T029, T030). On 28 November the owner filled
DEV, the runner repeated the comparison with the frozen engine there (T031: RESULT: SAME), the owner accepted it and
made the updater's first real fetch. What remains before the research resumes is the making of QA and PROD, and a
little tidying.

## 5. The design in force, in brief

Read the scheme and `a_p_r_i_r_DEV/README.md` for the whole; this is its spine, as built.

- **Kept from specification v0.6, unchanged:** N-1; TOP and WORST from the same model for a target; games never
  pooled; the methods, readout and tie order; scoring and divisions; the league measures; the OV-1 arithmetic.
- **Principles:** what a tree does follows from the software in it, not its name; everything a tree computes can be
  made again, so nothing is sealed or chained. **A difference in what was computed never refuses**: a changed
  method or engine fingerprint, or a corrected result, means "make that again". What still refuses is what cannot
  be made again or would be wrong to use: a settings file that is invalid or not this tree's, a working folder that
  is not the tree's own, accepted results the reader cannot use, a lock already held.
- **Three trees, one shape, the role as the end of the folder name:** DEV =
  `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV`; QA = `T:\a_p_r_i_r_QA`;
  PROD = `G:\a_p_r_i_r_PROD`; backups in `T:\a_p_r_i_r_backups\DEV`, `\QA` and `\PROD`. **DEV is filled and
  working; neither QA nor PROD exists yet.**
- **The settings file** (`ENVIRONMENT.ini`, the same form in every tree: `[environment] role`, then `[DEV]`, `[QA]`,
  `[PROD]` with `tree_root` and `backup_root`) and **the four identity rules** (`src/research/settings.py`). A tree's
  `.venv` is `<tree>\.venv`. DEV's `ENVIRONMENT.ini`, `.venv`, `source_data`, `results` and `records` are not in Git.
- **One lock per tree,** `records\TREE.lock`, taken by every command (`src/research/tree_lock.py`); `Who_Uses` alone,
  which only reads, takes none. Each lock file holds a key; a command of DEV that runs another tree's job starts
  it with `--under-lock <key>`, and the job works only under that lock and leaves it in place. A lock left by a
  killed command is deleted by the owner by hand.
- **Three small files beside each method,** all kept in Git in DEV (entry 352): `I_AM_INSTALLABLE` (made by
  `Make_Installable`; none exists yet), `I_AM_RETIRED` (a retired method keeps neither forecasts nor scores from its
  retirement draw on; entry 353), `IN_PLACE_SINCE` (the establishment draw; bookkeeping only; DEV's 40 are
  committed, `62872f8`, and say Powerball 1591 and Oz Lotto 1708). The infrastructure's flag
  (`src\I_AM_INSTALLABLE`) holds three fingerprints: the engine's, the updater's and the root launchers'. None of
  the three small files is copied between trees by `Create_Tree` or `Install`.
- **The engine's fingerprint** covers every file under `src\` outside the method families and outside `src\updater`
  (entry 356); `reports.py` and `research_job.py` are inside it. **Any change to such a file, a message included,
  makes every tree that holds results rebuild everything at its next job** (about 49 minutes a tree on the owner's
  PC). So a small change to the engine is best made before more trees exist, or kept for the next change that is
  needed anyway (entry 388). A method's own fingerprint does not change with the engine's, so its `IN_PLACE_SINCE`
  stays.
- **The research job** (`Run_Research.bat`; `src/research/research_job.py`): the tree's first step and lock; the
  updater per game unless `--no-update` (a failure warns loudly, the job goes on with the accepted results and ends
  with exit code 1; after a website "Stop" nothing more is fetched in that job); delete what is out of date; catch
  up, the next draw included; league, reports, both OV-1 series (both exploratory); one job-log line; a backup. It
  works every draw on file and then one more step, the forecasts for the next draw; its progress line, at every
  25th step, reads "processed target draw N (results on file through M)".
- **The second OV-1 series** counts each method from the draw after its establishment draw in that tree. In DEV it
  therefore starts at Powerball 1592 and Oz Lotto 1709. The series of 1551 and 1668 onward belongs to the frozen
  top level; T031's scratch trees were given those starting draws on purpose.
- **The updater** (`src/updater/results_updater.py`; `Run_Results_Updater.bat`): the first system's reviewed
  updater with every Mode H state removed by exact removals, its own lock removed (the caller holds the tree's), and
  a second final-URL check before parsing. `deploy/compare_updater_with_frozen.py` proves it on invented pages:
  RESULT: SAME. Defaults: both games, this month and the five before, Chrome. It prints, for each game, "checked N
  overlapping draws (all matched), added M", the grab kept and the master's backup. Exit codes: 0 done, 1 a check
  failed, 2 STOP, 3 refused.
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
  never end it: Ctrl+C in the installing window only says it is still working. On Windows a console Ctrl+C may also
  reach the child job itself, which then stops by itself; the parent never forcibly ends it, and keeps the lock until
  the child has ended.
- **The reports' wording** (entry 366): "retired" and "method"; the second OV-1 series' text, the reviewer's own,
  says it is exploratory and claims no error bound; "numerical lower bound"; nothing is set aside.
- **The proof (scheme section 9):** `deploy/compare_with_frozen.py` (`invented`, `run`, `align`, `trees`, `code`):
  from the same accepted results the simplified engine gives the same forecasts, scores, both OV-1 series and,
  through a declared list of wording changes (`WORDING_CHANGES`, 21 kinds), the same report files as the frozen
  engine at the top level. **Shown on the owner's PC by TASK_T031 and accepted by him (entries 384 and 385).**

## 6. Where things stand (28 November 2026, 09:10)

- **Steps 1 to 4 are built, read by the reviewer, corrected, rehearsed on Windows and proved there.** 280 tests in
  `a_p_r_i_r_DEV`: all pass in the cloud (Linux, Python 3.15.0b4); on the owner's PC 277 pass and 3 are skipped as
  expected (T029).
- **The rehearsal passed** (the runner, in `D:\DELETE_ME\`): T029, the test suite in a scratch DEV tree with its own
  `.venv` (report `a0662da`); T030, every command on three scratch trees with invented results, the child-process
  install and the restore's rename aside included (31 steps, report `607834e`); T031, the comparison of the two
  engines from DEV's own fill with DEV's own Python 3.15.2 and numpy 2.5.5: twelve lines SAME, RESULT: SAME
  (report `22ea440`). The stops on the way were all in the harness: the permission rules' syntax, a virtual
  environment active in the runner's shell, and one test's own line-ending assumption (section 7 has the lessons).
- **DEV is filled** (the owner, entry 383; 49 minutes): 40 methods a game; Powerball 15,118 forecasts and 15,078
  scores, Oz Lotto 6,598 and 6,558, from results through draws 1591 and 1708.
- **The first real fetch is done** (the owner, entry 386): every overlapping draw matched, two draws added a game.
  DEV now holds Powerball through draw 1593 and Oz Lotto through 1710. The job that followed (entry 387) wrote 80
  forecasts and 80 scores a game and gave the second OV-1 series its first lines in DEV (Powerball 1592 to 1593,
  score 0.983267352796; Oz Lotto 1709 to 1710, score 0.997794221022; reference line 40 not reached in either).
- **The owner's finding, corrected** (entries 387 to 389): the progress line "worked through draw 1594 of 1593" was
  misleading wording, nothing more. Corrected in `8fce853` (two lines of one message; the reviewer's PASS). The
  engine's fingerprint changed, so **DEV is rebuilding everything once: started by the owner at 08:28, about 49
  minutes.** When he sends its output, check: one REBUILD line; Powerball 15,198 forecasts and 15,158 scores, Oz
  Lotto 6,678 and 6,638; the second OV-1 series exactly as above; the 40 `IN_PLACE_SINCE` files unchanged (`git
  status` clean); a backup line. Record it in the decision log.
- **Authorised on the owner's PC:** nothing beyond what he runs himself. QA and PROD do not exist. He may delete
  everything under `D:\DELETE_ME\a_p_r_i_r\`.

| Entry | What |
|---|---|
| 367 | RAT-64 (H-1 v17r1) and RAT-65 (H-2 v11) |
| 368-370 | the runner's rulebook v0.8, its permission settings and the task files T029 to T031 written, read by the reviewer, corrected; RAT-66 |
| 371-380 | T029: three stops in the harness (the drive guard's syntax, settings r1 then r2; an active virtual environment; one test's line endings, `165d19f`); then PASS |
| 381-382 | T030: PASS; item 2 of the work order done |
| 383 | DEV's first fill by the owner; the 40 `IN_PLACE_SINCE` files committed; the reviewer accepts T029 and T030 |
| 384-385 | T031: RESULT: SAME on the owner's PC; the owner accepts it (items 4 and 5) |
| 386-387 | the owner's first real fetch; DEV's first job with the updater in it (item 6); his finding, the progress line |
| 388-389 | the progress line corrected (`8fce853`); the reviewer's PASS; DEV rebuilds once |
| 390 | RAT-67: H-2 v12; the continuity page brought up to date |
| 391 | this handover written as a candidate, at the owner's word |

## 7. Where everything is

| What | Where |
|---|---|
| The living system (DEV tree) | `a_p_r_i_r_DEV/` (`src/research/` engine; `src/updater/`; `src/methods/` 40 methods in 12 families; `deploy/`; `tests/`; the launchers at its root) |
| The comparison tools | `a_p_r_i_r_DEV/deploy/compare_with_frozen.py`, `compare_updater_with_frozen.py` |
| The file-form checker | `a_p_r_i_r_DEV/deploy/file_form.py` (everything CRLF and ASCII, `.jsonl` included) |
| The frozen reference | the top level: `src/`, `tests/`, `Run_Research.bat`, the updater `src/results_master_v0_2.py` |
| The runner's rulebook | `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (v0.8; SHA-256 `a51ca9bdb7f39c475a74ce87a77fd61c42b9318b1894938e708b065a80aea381`); its candidates in `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_8/` |
| The runner's permissions | `.claude/settings.json` (edition r2; SHA-256 `026408594841046a46c0bc934e58c9779513f85f3c99a3e5f3deba73f5dbc9fa`) |
| The runner's tasks | `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_Tnnn.md` (last T031) and `inbox/REHEARSAL_HELPER.py`; reports in `outbox/`; `tools/cc_clone.py` |
| Decisions | `exchange/DECISIONS/DECISION_LOG.md` (LF; appended as bytes) |
| The continuity page | `exchange/CONTINUITY_NOW.md` (LF; its top block and its two handover sections are current) |
| Standing reminders | `exchange/OWNER_REMINDERS.md` (CRLF) |
| Handovers | in force in `doc/HANDOVER/`; Claude's candidates in `exchange/HANDOVER_2026_11_28/` |
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
`requirements.txt`. Read `source_data` only; never write there. The top-level `source_data` holds the results as
accepted by the first system (through draws 1591 and 1708); DEV's own, with the newer draws, is on the owner's PC
only. **A quick recheck after a change to `reports.py` alone:** copy the new `src` into the second tree, set its
stored engine fingerprint (`results/research/INFRASTRUCTURE`, by `code_identity.store_fingerprint`) to the new
engine's, run its job (about 3 minutes: only the reports are made again) and `trees`. Say so when you use it; the
owner's PC makes everything from nothing.

**The updater file** was made by a workspace script of scripted exact removals from the frozen updater; the script
did not carry over. Edit `src/updater/results_updater.py` directly, and keep `compare_updater_with_frozen.py`'s
declared lists of changed and removed definitions up to date.

**What the rehearsal taught, for the next task file:**

- **Permission rules** (`.claude\settings.json`, deny rules for the runner's shell): a backslash before `*` breaks a
  rule, single or doubled; `:*` at the end of a rule means "a space, then anything", so a bare `*T:*` is rejected.
  The forms that work are of the kind `*T:*a_p_r_i_r*` (and `t:`, `G:`, `g:`), `T:/`, `/t/`, `/g/`, and
  `Read`/`Edit` rules for `//t/**` and `//g/**`. Probe each rule with a harmless `echo` before relying on it.
- **The guard refuses any shell command whose text holds the updater's file name,** a listing included. Keep that
  name out of the commands a task gives; where a report must hold it, the runner writes the report with its file
  tool (T031 did).
- **The runner's shell may have a virtual environment active.** A tree's `create_venv.bat` refuses then. In a task,
  start the two environment scripts inside `( unset VIRTUAL_ENV; ... )`. **The owner, for QA and PROD:** build each
  `.venv` from a plain command window with no environment active.
- **Windows line endings in tests:** a fixture that appends to a file in text mode writes CRLF on Windows and LF in
  the cloud. Write bytes (`165d19f`). The cloud cannot show this by itself.
- **The helper** `inbox/REHEARSAL_HELPER.py` (`check-scratch`, `copy-dev`, `settings`, `invented`, `run-tests`,
  `plant-edit`, `one-backup`, `comparison-trees`) writes only under `D:\DELETE_ME` and can serve a later rehearsal.

## 8. What comes next

**The owner's work order of entry 365: items 1 to 6 are done** (1 rulebook, wording and task files; 2 the
rehearsal; 3 DEV's first fill; 4 T031; 5 his acceptance; 6 his first real fetch and a job that fetches).

**First: DEV's rebuild** (section 6). Check its output and record it.

**Then item 7: QA, then PROD. The owner runs every step himself;** the runner never touches a real tree or the `T:`
and `G:` drives. Write him plain step-by-step instructions, one tree at a time, and read
`a_p_r_i_r_DEV/README.md` and `deploy/install_tools.py` (`create_tree`) again before you write them. In outline:

1. In DEV: `Make_Installable.bat ALL INFRA`. It writes `src\I_AM_INSTALLABLE` and one `I_AM_INSTALLABLE` beside each
   of the 40 methods. These files are kept in Git: the owner commits and pushes them (as he did the 40
   `IN_PLACE_SINCE` files; `git add a_p_r_i_r_DEV`).
2. In DEV: `Create_Tree.bat QA`. It makes `T:\a_p_r_i_r_QA` (absent or empty before): DEV's flagged infrastructure
   and methods, DEV's accepted results, the settings file last.
3. In QA, from a plain command window with no environment active: `create_venv.bat`, then
   `install_upgrade_dependencies_into_venv.bat`, then `Run_Research.bat --no-update` (QA's first fill, about 49
   minutes; tell him so). QA's `IN_PLACE_SINCE` files are written by that job, with the last draws QA then holds, so
   QA's second OV-1 series starts after them.
4. **Before QA's first fetching job, the same care as in DEV** (entry 358): `Run_Results_Updater.bat` by itself in
   QA, a look at what it wrote, only then `Run_Research.bat` without `--no-update`.
5. The same for PROD (`Create_Tree.bat PROD`, `G:\a_p_r_i_r_PROD`).
6. After both: the top-level `.venv` can go (the owner's decision).

Compare QA's first-fill totals with DEV's for the same draws: the same software on the same accepted results must
give the same counts and the same first OV-1 series (the second series differs by its starting draw).

**Then, step 7 of the scheme, tidying:** a few pages of how-to; this handover brought up to date; the decision log
and the continuity page converted to CRLF (and the continuity page cut down to what is current); **the three
revisit the operations manual** (entry 343); **a decision on the frozen top level** (keep as history, or move aside).

**Then step 8, the research.** New methods. First, together, **the three deferred discussions**: the future-method-
priorities draft (`doc/Predictive_Randomness_Future_Method_Priorities_v0_1_DRAFT.md`, entry 289); the roles of the
two AIs (entry 292); and each AI's minimal additions to `doc/CODING_PRACTICES_v0_1.md` (entry 299). **Only if it
matters then:** a job with nothing to do takes a few minutes, because every league report is made again.

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
  `a_p_r_i_r_DEV`, and the whole suite before each code commit. Before a change to an engine file, say what its
  fingerprint change costs (section 5).
- **The file form:** every text file of the living system is CRLF and ASCII, the `.jsonl` records included. The
  frozen top level is not changed.
- **The decision log:** record every owner decision at once, in his words. **Read the time from the clock
  (`TZ=Australia/Adelaide date`) in the command that writes the entry; never type it** (the headings of entries
  387, 388 and 390 carry typed times a few minutes late; entry 391 says so). Each entry ends "Next numbers: ...".
  Check the file ends with the expected line before appending.
- **The continuity page:** a new bullet at the top of "For the owner: NOW" and the "Last updated" line, at each
  milestone; its "If a chat ends" and "Installed handovers" sections at each ratification of a handover.
- **Git:** fetch, then look at `git status -sb` and `git log HEAD..origin/main` before each commit (the reviewer and
  the owner commit too; take their commits in first, then commit and push your own). Look at
  `git diff --cached --stat` before committing. Never type a hash: compute it.
- **Documents:** every new text file CRLF and ASCII; the decision log and the continuity page are LF until the
  tidying. Lines of documents at most 120 characters.
- **Commit trailer:** the attribution lines the session gives you.
- **Numbers at this writing:** next EX is EX_334 (Claude's); next decision log entry 392; next ratification RAT-68
  (this document's). The decision log's last line is the authority.

## 10. Taking over

1. Add the repository (push access) and read section 0's list. Check this document's statements against the
   repository; do not take summaries on trust.
2. Give the owner your first reply: what you understand the state to be, what is and is not authorised, the next
   deliverable, and anything unclear or inconsistent. Build and commit nothing yet.
3. The owner decides whether to accept the takeover. He may ask the reviewer to put a few questions to you first.

END.
