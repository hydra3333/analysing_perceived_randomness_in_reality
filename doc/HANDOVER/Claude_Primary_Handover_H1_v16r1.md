# H-1 v16r1 - the Claude web chat's handover (short form)

Version v16r1, 27 November 2026 (v16 with the coding standards made plain, at the owner's
query; entry 351). Written by the Claude web chat (primary designer and coder) on Opus, at the owner's
request (decision log entry 350), for the next Claude chat. **Status: RATIFIED by the owner, RAT-62 (decision log entry 352).**

## 0. What this is, and what to read

This is the short handover the simple scheme asked for (its section 11). It replaces the account in H-1 v15
(`doc/HANDOVER/Claude_Primary_Handover_H1_v15.md`, RAT-60), whose chapter 0 describes a design that has since been
set aside. H-1 v15 and every earlier handover stay in Git as history; read them only to answer a question about
the past. **The decision log is the full record; this document is an index to it, not a substitute.**

Read, in this order, and check what you read against the repository:

1. This document.
2. **The design in force:** `exchange/Claude_The_Simple_Scheme_v0_2_20261126.md`
   (SHA-256 `15f52cabb54068860f439cb69a8480067a8e688b3c85107988743ecba38a1a77`;
   agreed by the owner, entry 344). About 12 pages.
3. **Step 2 as done:** `exchange/Claude_Step_2_Engine_Simplified_And_Compared_v0_1_20261126.md`
   (6 pages; its section 4 was ratified as RAT-61).
4. **The owner's reframing**, which is why the scheme exists:
   `exchange/Claude_Comment_On_The_Owners_Reframing_Back_To_The_Research_v0_1_20261126.md` (it carries his words).
5. **The decision log from entry 330** (`exchange/DECISIONS/DECISION_LOG.md`, the pause) to the last entry.
6. The top block of `exchange/CONTINUITY_NOW.md` ("For the owner: NOW"). Below it the page is mostly history.
7. **The coding standards, binding on every line of code you write:** `doc/CODING_PRACTICES_v0_1.md` (one page;
   RAT-40) and `doc/FILE_FORM_STANDARD_v0_2.md` (RAT-49) as the scheme changed it. Section 9 says how they apply now.
8. `a_p_r_i_r_DEV/README.md`, then the code in `a_p_r_i_r_DEV/src/research/`.

## 1. The project and the roles

The question: do Australian Powerball and Oz Lotto results hold patterns that conventional statistics missed? The
expected outcome is a carefully measured null. It is speculative research, and the owner wants it run as research:
**the science must be right; the administration small** (his reframing of 26 November 2026, entry 330).

- **The project owner** (GitHub `hydra3333`): sole decider and authoriser. **Never write his personal name in
  anything committed.** He relays between the two AI chats.
- **The Claude web chat (you):** the primary designer and coder.
- **The ChatGPT chat:** the independent reviewer. Its handover in force is H-2 v9
  (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v9_20261125.md`, RAT-57); the reviewer chat in role took over from it on
  25 November 2026. It commits its own EX replies under `exchange/`; never edit its files.
- **Claude Code on the owner's PC:** a local runner only. It carries out task files the web chat writes, under its
  rulebook (`CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`, v0.7), which names the first system and must be given a
  short new edition before it rehearses anything of the scheme (step 5).

## 2. The hard rules (binding)

- The one production results source is Lotterywest-GOV (`www.lotterywest.wa.gov.au`, HTTPS), reached only by the
  owner's approved tools. You never contact any lottery website, and you never search for lottery results.
- You may read draw values, `source_data/` and `results/`. You never write there. Anything you work out in the chat
  from draw values is labelled "suggestive"; results count only from the reviewed programs.
- Method-facing N-1 isolation is never weakened (a method sees only the draws before its target). Games are never
  pooled. The sealed Mode H records of the first system are never altered.
- No program ends another process. Three safety switches of the first system stay False and its allowlist stays
  empty. Its orphan marker blocks launches; nothing clears or bypasses it.
- Nothing runs on the owner's PC without his go. No install, run, backup, restore, migration or deletion without his
  separate approval. Nothing ever changes his PC's date, time or time zone. A STOP is a STOP.
- **Commits.** You commit and push documents and records yourself (named paths only; fetch and look at
  `git status -sb` and `git log HEAD..origin/main` first; nothing deleted or overwritten): under `exchange/` and
  `CLAUDE_CODE_WORKING_FOLDER_TREE/` freely, into `doc/` only once reviewed and ratified. **Code: since 26 November
  2026 (entry 342) you commit the living system's code directly into `a_p_r_i_r_DEV/` on `main`**, named paths only;
  the reviewer reads the commit; the owner pulls. Code and tests never go into the top-level `src/` or `tests/`
  (frozen). You never write under `transitory_data/` or `GAIS/`.
- A PASS or a ratified design authorises no install or run.

## 3. How the owner works

- Plain step-by-step English. Decisions as: the question, why it matters, your recommendation, the options.
- Verify, don't assert: compute hashes, counts and comparisons with a tool. Show your reasoning, alternatives and
  uncertainties; he sometimes spots something important from them.
- **At every point, say what you think he should do next** (entry 335; he asks the reviewer the same).
- End anything to be relayed with a short paste-ready block for the reviewer chat.
- Discuss his queries with him first; issue an EX message only when he asks.
- **Do not over-engineer.** Tell him the simplest safe route first. Admin that does not serve the science or
  recoverability is not wanted. This is not a request for shorter reporting.
- A short "how the process went" note at milestones.
- **Model rule:** before designing a new subsystem or a major change, a statistical validity question, the root
  cause of an unexplained STOP, or a cold read of a design, say "Suggest switching to Fable (High) for this" and wait
  for his go. Tell him when a Fable task is finished. Save Fable for the hard parts; everything else runs on Opus.
- Watch the chat's length: say when a handover update is due, before the chat runs out.

## 4. How we got here (one paragraph)

The first system (the coordinator, method contracts, Mode H's sealed holdout) was replaced by a redesign ratified on
22 November 2026 (RAT-40: specification v0.6 and deployment design v0.12). Build steps 1 and 2 of that design were
installed (the method files' layout; a new research engine). Build step 3 (trees, installs, backups, a new updater)
was written in slices A, B and C, each passing review (slice C at EX_333). On 26 November 2026 the owner found the
design had again outgrown the research and **paused everything** (entry 330): he removed most controls and asked for
a simple scheme. Owner, reviewer and Claude agreed it the same day: **the simple scheme v0.2** (entry 344). Slices A
to C are set aside (kept in Git history, never installed). Step 1 and step 2 of the scheme's work order are done.

## 5. The design in force, in brief

Read the scheme for the whole; this is its spine.

- **Kept from specification v0.6, unchanged:** N-1; TOP and WORST from the same model for a target; games never
  pooled; the methods, readout and tie order (the permitted-view digest is part of every tie order); scoring and
  divisions; the league measures; the OV-1 arithmetic (its sections 1.2, 3.4, 6, 8, 9 and 10).
- **Principles:** what a tree does follows from the software in it, not its name; everything a tree computes can be
  made again, so nothing is sealed, chained or locked, and a difference never refuses: it means "make that again".
- **Three trees, one shape, the role as the end of the folder name:** DEV =
  `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV`; QA = `T:\a_p_r_i_r_QA`;
  PROD = `G:\a_p_r_i_r_PROD`; backups in `T:\a_p_r_i_r_backups\DEV`, `\QA` and `\PROD`. One settings file form
  in every tree (`[environment] role = ...`, then `[DEV]`, `[QA]`, `[PROD]` with `tree_root` and `backup_root`), and
  four identity rules (scheme section 3.1). Neither QA nor PROD exists yet.
- **Three small files beside each method:** `I_AM_INSTALLABLE`, `I_AM_RETIRED`, `IN_PLACE_SINCE` (scheme section 4;
  `a_p_r_i_r_DEV/src/research/method_flags.py`).
- **One research job, the same in every tree** (`Run_Research.bat`; scheme section 5): updater unless `--no-update`;
  make again what is out of date; catch up, the next draw included; league, reports and both OV-1 series per game;
  one job-log line; backup.
- **Commands** (scheme section 6): in every tree `Run_Research.bat`, `Run_Results_Updater.bat`, `Backup.bat`; in DEV
  `Make_Installable.bat`, `Who_Uses.bat`, `Create_Tree.bat`, `Install.bat` (with `--show`), `Retire.bat`,
  `Copy_From_PROD.bat`, `Restore.bat`.
- **Backups:** one plain ZIP at maximum compression, without `.venv` and the lock file; after every job, before every
  replacement and on demand. A failed backup stops a replacement but only warns after a job.
- **The proof (scheme section 9):** from the same accepted results the simplified engine must give the same
  forecasts, scores and OV-1 numbers as the frozen engine at the top level. Made in the cloud while writing; made
  once on the owner's PC before any tree is created.

## 6. Where things stand (27 November 2026)

- **Step 1 done** (entry 345): the living system copied into `a_p_r_i_r_DEV/`. The owner built its own `.venv` there
  (entry 346). The top-level `.venv` stays until after step 6: the frozen engine, the present updater and the
  runner's rulebook use it.
- **Step 2 done** (entries 348 and 349; commit `aedda2e`): the engine simplified inside `a_p_r_i_r_DEV/`. In the cloud
  (Python 3.15.0b4), on the accepted results and on invented results, `compare_with_frozen.py` ends `RESULT: SAME`:
  every forecast, score, line of the second OV-1 series and report file. 161 tests pass in the tree. The nine
  choices made while writing it are ratified (RAT-61, entry 350). Its code meets the coding practices; its commit
  did not say so, as the practices ask (an omission, recorded in entry 351).
- **The reviewer is reading step 2** (its one reading; findings, if any, are corrected before or with step 3).
- **The top level of the repository is frozen:** the first system and the engine as reviewed, the reference of the
  comparison. Do not change it.
- **Nothing is authorised on the owner's PC.**

## 7. Where everything is

| What | Where |
|---|---|
| The living system (DEV tree) | `a_p_r_i_r_DEV/` (`src/research/` engine; `src/methods/` 40 methods in 12 families; `tests/`; `deploy/`) |
| The comparison tool | `a_p_r_i_r_DEV/deploy/compare_with_frozen.py` (`invented`, `run`, `align`, `trees`, `code`) |
| The file-form checker | `a_p_r_i_r_DEV/deploy/file_form.py` (everything CRLF, `.jsonl` included) |
| The frozen reference | the top level: `src/`, `tests/`, `Run_Research.bat`, the updater `src/results_master_v0_2.py` |
| Decisions | `exchange/DECISIONS/DECISION_LOG.md` (LF; appended as bytes) |
| The continuity page | `exchange/CONTINUITY_NOW.md` (LF; its top block is current) |
| Standing reminders | `exchange/OWNER_REMINDERS.md` |
| EX messages | `exchange/EX_nnn_<author>.md` (latest: EX_333, the reviewer's PASS of slice C, now history) |
| Science kept | `doc/Predictive_Randomness_System_Specification_v0_6.md` (its science sections only) |
| Coding standards (binding) | `doc/CODING_PRACTICES_v0_1.md`; `doc/FILE_FORM_STANDARD_v0_2.md` as the scheme changed it (section 9) |

**Running the tests** (in `a_p_r_i_r_DEV`): `PYTHONPATH=src:src/methods:tests python -B -m unittest discover -s
tests -p "test_research_*.py"` (on Windows `set PYTHONPATH=src;src\methods;tests`). All run on invented draws.

**The cloud workspace does not carry over between chats.** To repeat the comparison on the accepted results: clone
`main` twice (or once and copy); in one copy give the top level an `ENVIRONMENT.ini` (role DEV, `tree_root` that
folder, `venv_dir` its `.venv`); make a second tree holding a copy of `a_p_r_i_r_DEV/src`, the four files of
`source_data/` (both games' `*_results_master.csv` and `*_results_master_ledger.csv`) and its own `ENVIRONMENT.ini`;
then `compare_with_frozen.py run` on each (about 30 minutes each in the cloud), `align`, `run` on each again,
`trees`. Use a Python 3.15 environment with the packages of `requirements.txt`. Read `source_data` only; never
write there.

## 8. What comes next: the work order, and where "left for later" fits

Each step on the owner's go. Steps 3 and 4 are Fable work (they hold what could destroy what cannot be made
again).

**Now, in parallel:** the reviewer's one reading of step 2. Any finding is corrected first.

**Step 3, the updater** (scheme section 8). The present reviewed updater (`src/results_master_v0_2.py`, headless
Chrome to Lotterywest-GOV) with every Mode H state removed, the same in every tree, writing only its own tree's
`source_data`; `Run_Results_Updater.bat` in the tree; the research job calls it at its start unless `--no-update`
(today the job says the updater is not part of it yet). The owner kept the reader's check that the results file
matches the last line of the updater's own ledger. Neither AI ever runs the updater.

**Step 4, the settings reader, the lock and the commands** (scheme sections 3, 6 and 7). Here also:
- the settings file in its new form and the four identity rules replace today's first form (`settings.py`);
- the lock (one file in `records/`) replaces `job_lock.py`'s present lock; **the first system's orphan-marker check
  is still in the job: whether the new trees keep it is a question for the owner** (it is one of his hard rules);
- the backup at the end of the job;
- **a question for the owner:** whether `I_AM_INSTALLABLE` and `I_AM_RETIRED` in DEV are kept in Git
  (`IN_PLACE_SINCE` is already ignored).

**Between step 4 and step 5: the reports' wording.** "Withdrawn" becomes "retired", "variant" becomes "method",
the second series' "at most 2.5%" claim is softened to "exploratory", the README stops mentioning reports set
aside. One small commit to `reports.py` only. Recommendation: give `compare_with_frozen.py` a declared list of these
replacements, applied to the frozen engine's reports before the byte comparison, so that the comparison of step 5
stays exact.

**Step 5, the rehearsal.** A short new edition of the runner's rulebook, then one rehearsal on the owner's PC by
the local runner in the scratch folder (`D:\DELETE_ME\`), with the comparison of section 9 on his PC.

**Step 6, the real trees.** DEV's first fill (about 47 minutes on his PC); `Create_Tree.bat QA`; `Create_Tree.bat
PROD`. After this the top-level `.venv` can go.

**Step 7, tidying.** A few pages of how-to; this handover brought up to date; the decision log and the continuity
page converted to CRLF (and the continuity page cut down to what is current); **the three revisit the operations
manual** (entry 343); **a decision on the frozen top level** (keep as history, or move aside).

**Step 8, the research.** New methods. First, together, **the three deferred discussions**: the future-method-
priorities draft (`doc/Predictive_Randomness_Future_Method_Priorities_v0_1_DRAFT.md`, entry 289); the roles of the
two AIs (entry 292: the reviewer's view is that no AI is the final independent reviewer of its own code); and each
AI's minimal additions to `doc/CODING_PRACTICES_v0_1.md` (entry 299). **Also here, only if it matters then:** a job
with nothing to do takes about two minutes, because every league report is made again.

## 9. Working practices

- **The coding practices** (`doc/CODING_PRACTICES_v0_1.md`, RAT-40) apply to all code: a plain-English header on every
  `.py` file (what it is for, which part of the design it carries out, which project modules it uses and for what,
  what uses it); constants at the top with a comment; a comment on every function saying what it does, each
  parameter, what it returns with an example, and what makes it refuse; names that say what a thing is; messages
  that say what happened, where, why and what to do; nothing swallowed; one shared piece of code per shared task;
  each test named for the rule it proves, with a planted fault. **Every code commit, and the paper that goes with
  it, says "coding practices met" or lists the exceptions with reasons;** the reviewer checks code against them.
  Under the scheme, read three items this way until the owner ratifies a revision (the review of the practices is
  one of step 8's deferred discussions): a header names the scheme's section where the part is administrative;
  "held or not current" becomes "rebuilt" (the job says what it makes again and why, at its start and again at its
  end); and "a variant's files can never change once installed" no longer holds (a changed method is rebuilt).
- **The file form:** every text file of the living system is CRLF and ASCII, the `.jsonl` records included (the
  scheme removed the standard's LF exception, which existed only for the hash chains). The checker is
  `a_p_r_i_r_DEV/deploy/file_form.py`; run it on every file you commit there. The frozen top level is not changed.
- **The decision log:** record every owner decision at once, in his words, with the time read from the clock
  (`TZ=Australia/Adelaide`) in the command that writes it. Each entry ends "Next numbers: ...". Check the file ends
  with the expected line before appending.
- **The continuity page:** a new bullet at the top of "For the owner: NOW" and the "Last updated" line, at each
  milestone.
- **Git:** fetch, then look at `git status -sb` and `git log HEAD..origin/main` before each commit (the reviewer
  commits too; once a push was refused because of a commit not looked for). Look at `git diff --cached --numstat`
  before committing. Never type a hash or a time: compute them.
- **Documents:** every new text file CRLF and ASCII; the decision log and the continuity page are LF until step 7.
  Lines of documents at most 120 characters.
- **Commit trailer:** the attribution lines the session gives you.
- **Numbers now:** next EX is EX_334 (Claude's); next decision log entry 352; next ratification RAT-62.

## 10. Taking over

1. Add the repository (push access) and read section 0's list. Check this document's statements against the
   repository; do not take summaries on trust.
2. Give the owner your first reply: what you understand the state to be, what is and is not authorised, the next
   deliverable, and anything unclear or inconsistent. Build and commit nothing yet.
3. The owner decides whether to accept the takeover. He may ask the reviewer to put a few questions to you first.

END.
