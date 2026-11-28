# H-1 v19 - the Claude web chat's handover (short form)

Version v19, 28 November 2026, afternoon. Written by the Claude web chat (primary designer and coder) at the owner's
word ("yes to updating your handover now", decision log entry 408), for the next Claude chat. It replaces H-1 v18
(RAT-68), written this morning before QA and PROD were made and before the operations manual existed.
**Status: RATIFIED by the owner, RAT-72 (decision log entry 409).**

## 0. What this is, and what to read

This is the short handover of the simple scheme. **The decision log is the full record; this document is an index
to it, not a substitute.** H-1 v18 and every earlier handover stay in Git as history; read them only to answer a
question about the past.

Read, in this order, and check what you read against the repository:

1. This document.
2. **The operations manual,** `a_p_r_i_r_DEV/OPERATIONS_MANUAL.md` (edition 2, RAT-71): how the system is run, what
   every command and message means, and (Appendices C and D) every method and research lead. It is the quickest
   way to understand the system as it now stands.
3. **The design in force:** `exchange/Claude_The_Simple_Scheme_v0_2_20261126.md`
   (SHA-256 `15f52cabb54068860f439cb69a8480067a8e688b3c85107988743ecba38a1a77`; agreed by the owner, entry 344).
   Its work order was replaced by the owner's of entry 365, now done to its end (section 6).
4. **The owner's reframing**, which is why the scheme exists:
   `exchange/Claude_Comment_On_The_Owners_Reframing_Back_To_The_Research_v0_1_20261126.md` (it carries his words).
5. **The decision log from entry 330** (`exchange/DECISIONS/DECISION_LOG.md`, the pause) to the last entry.
   Entries 392 to 408 are the work since H-1 v18 (section 6 lists them).
6. The top block of `exchange/CONTINUITY_NOW.md` ("For the owner: NOW"), and its sections "If a chat ends" and
   "Installed handovers". The rest of the page is mostly history.
7. **The coding standards, binding on every line of code you write:** `doc/CODING_PRACTICES_v0_1.md` (RAT-40) and
   `doc/FILE_FORM_STANDARD_v0_2.md` (RAT-49) as the scheme changed it. Section 9 says how they apply now.
8. `a_p_r_i_r_DEV/README.md`, then the code in `a_p_r_i_r_DEV/src/research/` and `a_p_r_i_r_DEV/deploy/`.
9. **The tidy in hand:** `exchange/Claude_Tree_Tidy_Inventory_And_Procedure_v0_1_20261128.md` and the reviewer's
   `exchange/ChatGPT_Tree_Tidy_Consolidated_Agreement_v0_1_20261128.md`, with entries 394 to 398 (section 8).
10. `exchange/OWNER_REMINDERS.md`: the four deferred discussions, R-001 and R-002, and what you have promised.

## 1. The project and the roles

The question: do Australian Powerball and Oz Lotto results hold patterns that conventional statistics missed? The
expected outcome is a carefully measured null. It is speculative research, and the owner wants it run as research:
**the science must be right; the administration small** (his reframing of 26 November 2026, entry 330).

- **The project owner** (GitHub `hydra3333`): sole decider and authoriser. **Never write his personal name in
  anything committed.** He relays between the two AI chats.
- **The Claude web chat (you):** the primary designer and coder.
- **The ChatGPT chat:** the independent reviewer. Its handover in force is **H-2 v13**
  (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v13_20261128.md` and its blurb beside it; RAT-69, entry 397). The
  reviewer chat that wrote it ended; at the owner's request Claude corrected its position to entry 396 before he
  ratified it; a new reviewer chat took over from it at 10:47 without the opening questions (entry 398) and has
  worked since. It commits its own files; never edit them unless the owner asks for that one change (as he did for
  H-2 v13). Open reviewer findings: none.
- **Claude Code on the owner's PC:** a local runner only, under its rulebook v0.8 (RAT-66) and the permission
  settings r2. It never works in a real tree, never touches the `T:` or `G:` drives, and never runs the results
  updater, anywhere. It has not been used since TASK_T031; the tidy will need a short rulebook v0.9 (section 8).

## 2. The hard rules (binding)

- The one production results source is Lotterywest-GOV (`www.lotterywest.wa.gov.au`, HTTPS), reached only by the
  owner's approved tools. You never contact any lottery website, and you never search for lottery results.
- **Only the owner runs the results updater,** in any tree. Neither AI nor the runner ever runs it or lets it reach
  the site. Every test and tool uses invented pages, and replaces the real-browser class with one that refuses.
  It has fetched from the real site in all three trees (entries 386, 387, 399, 400, 402).
- You may read draw values, `source_data/` and `results/`. You never write there. Anything you work out in the chat
  from draw values is labelled "suggestive"; results count only from the reviewed programs. Keep draw values out of
  the decision log and the other records.
- Method-facing N-1 isolation is never weakened (a method sees only the draws before its target). Games are never
  pooled. TOP and WORST come from one ranking. The sealed Mode H records of the first system are never altered.
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
  asks for that one change. You never write under `transitory_data/` or `GAIS/`.
- A PASS or an agreed design authorises no install or run.

## 3. How the owner works

- Plain step-by-step English. Decisions as: the question, why it matters, your recommendation, the options.
- Verify, don't assert: compute hashes, counts and comparisons with a tool. Show your reasoning, alternatives and
  uncertainties; he sometimes spots something important from them.
- **At every point, say what you think he should do next** (entry 335; he asks the reviewer the same).
- End anything to be relayed with a short paste-ready block for the reviewer chat.
- Discuss his queries with him first; issue an EX message only when he asks. When he relays the reviewer's
  recommendations without words of his own, they are not yet his decision: ask him. When he relays decisions he
  made in the reviewer's chat, record them as relayed.
- **Do not over-engineer.** Tell him the simplest safe route first. Admin that does not serve the science or
  recoverability is not wanted. This is not a request for shorter reporting.
- A short "how the process went" note at milestones.
- **Tell him before any run or wait longer than a few minutes** what is running and about how long; when he runs
  something long himself, tell him when to expect its end.
- **He reads output himself and spots what is odd** (the progress line of entry 387). Read the code before you
  answer such a finding. When he stops a step of yours, stop and wait for his word.
- **Model rule:** before designing a new subsystem or a major change, a statistical validity question, the root
  cause of an unexplained STOP, or a cold read of a design, say "Suggest switching to Fable (High) for this" and wait
  for his go. Tell him when a Fable task is finished. Save Fable for the hard parts; everything else runs on Opus.
- Watch the chat's length: say when a handover update is due, before the chat runs out.

## 4. How we got here (one paragraph)

The first system (the coordinator, method contracts, Mode H's sealed holdout) was replaced by a redesign ratified on
22 November 2026 (RAT-40). On 26 November 2026 the owner found that design had outgrown the research and paused
everything (entry 330); owner, reviewer and Claude agreed **the simple scheme v0.2** the same day (entry 344). On 26
and 27 November its steps 1 to 4 were built in `a_p_r_i_r_DEV/`, each read once by the reviewer and corrected; on
the evening of 27 November the runner rehearsed it on the owner's PC. **On 28 November the owner filled DEV, the
comparison with the frozen engine was repeated on his PC (SAME), he made the first real fetch, a misleading
progress line was corrected, and QA and PROD were made: all three trees give the same results. The system is in
production.** The operations manual was written and ratified the same day, and now travels with the software.

## 5. The design in force, in brief

The operations manual says how it is used; the scheme and the README say how it works. Its spine, as built:

- **Kept from specification v0.6, unchanged:** N-1; TOP and WORST from the same model for a target; games never
  pooled; the methods, readout and tie order; scoring and divisions; the league measures; the OV-1 arithmetic.
- **Principles:** what a tree does follows from the software in it, not its name; everything a tree computes can be
  made again, so nothing is sealed or chained. **A difference in what was computed never refuses**: a changed
  method or engine fingerprint, or a corrected result, means "make that again". What still refuses is what cannot
  be made again or would be wrong to use: a settings file that is invalid or not this tree's, a working folder that
  is not the tree's own, accepted results the reader cannot use, a lock already held.
- **Three trees, one shape, the role as the end of the folder name:** DEV =
  `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV`; QA = `T:\a_p_r_i_r_QA`;
  PROD = `G:\a_p_r_i_r_PROD`; backups in `T:\a_p_r_i_r_backups\DEV`, `\QA` and `\PROD`. **All three exist and hold
  the same software and results.**
- **The settings file** (`ENVIRONMENT.ini`, the same form in every tree) and **the four identity rules**
  (`src/research/settings.py`). A tree's `.venv` is `<tree>\.venv`, built from a plain window with no environment
  active. DEV's settings, `.venv`, `source_data`, `results` and `records` are not in Git.
- **One lock per tree,** `records\TREE.lock` (`src/research/tree_lock.py`); `Who_Uses` and the environment scripts
  take none. A command of DEV that runs another tree's job starts it with `--under-lock <key>`.
- **Three small files beside each method,** all in Git in DEV: `I_AM_INSTALLABLE` (all 41 flags committed,
  `5498e5a`; the infrastructure's last refreshed in `16d2071`), `I_AM_RETIRED` (none yet), `IN_PLACE_SINCE` (DEV's
  40 say Powerball 1591 and Oz Lotto 1708; QA's and PROD's say 1593 and 1710, written by their first fills). None
  is copied by `Create_Tree` or `Install`.
- **Fingerprints.** The engine's covers every file under `src\` outside the method families and `src\updater`;
  **any change to such a file, a message included, makes every tree that holds results rebuild everything** at its
  next job (about 49 minutes a tree), and deletes both games' stored results even in a one-game job. A method's
  covers its own files and the helpers its `VARIANT.json` names. The updater's and the root files' (the launchers,
  the environment scripts and, since `5812b70`, `OPERATIONS_MANUAL.md`) decide only what may be installed.
- **The research job** (`Run_Research.bat`): lock; check the tree; the updater per game unless `--no-update`; delete
  what is out of date; catch up, the next draw included; league, reports, both OV-1 series; one job-log line; a
  backup. Its progress line reads "processed target draw N (results on file through M)" (`8fce853`).
- **The two OV-1 series** are both exploratory; neither claims an error bound; 40 is a reference line. The second
  counts each method from the draw after its establishment draw in that tree: DEV from 1592 and 1709, QA and PROD
  from 1594 and 1711. The manual's section 2 has the agreed plain-English account (the reviewer's wording).
- **The updater** (`src/updater/results_updater.py`): the first system's reviewed updater with every Mode H state
  removed. Defaults: both games, this month and the five before (up to 60 with `--months-back`), Chrome.
- **Backups:** one plain ZIP at maximum compression per tree, without `.venv`, the lock and caches; after every job,
  before every replacement, and on demand. Never written over or deleted by the system.
- **DEV's commands:** `Make_Installable`, `Who_Uses`, `Create_Tree`, `Install [--show]`, `Retire`,
  `Copy_From_PROD`, `Restore`. Appendix B of the manual is the full reference.
- **The proof (scheme section 9):** `deploy/compare_with_frozen.py`; shown on the owner's PC by TASK_T031 (SAME),
  accepted by him (entry 385). The tidy will retire it with the frozen top level (section 8).

## 6. Where things stand (28 November 2026, 13:40)

- **In production.** DEV, QA and PROD each hold 40 methods a game and results through Powerball 1593 and Oz Lotto
  1710: Powerball 15,198 forecasts and 15,158 scores, Oz Lotto 6,678 and 6,638, in every tree. Every variant has
  the history it needs (the smallest margin: three variants needing 208 earlier draws have 29 scored Oz Lotto
  draws). **The routine: `Run_Research.bat` in PROD after each draw**; the first is after Tuesday's Oz Lotto draw.
- **One transient fetch failure,** in QA's first job (Oz Lotto, "results ... did not appear"): nothing written; one
  standalone retry normal; recorded as a transient fetch failure of unknown cause (entries 399 and 400). PROD's
  fetches were normal. If it recurs, investigate before further fetching.
- **The owner dropped the separate standalone first fetch** for QA (entry 396) and PROD (402): the updater had
  fetched three times in DEV with every overlap matching.
- **The operations manual** is ratified: edition 1 RAT-70 (entry 404), edition 2 RAT-71 (406). Its master is
  `a_p_r_i_r_DEV/OPERATIONS_MANUAL.md`; `ROOT_FILES` carries it (`5812b70`, two tests, the reviewer's PASS); it is
  installed in QA and PROD (entry 407). Edition 2 adds Appendix D and the provisional identities E_63 to E_71.
- **The tests:** 282 in `a_p_r_i_r_DEV` (280 and the manual's two), all passing in the cloud. On Windows (T029,
  before the manual's two) 277 passed and 3 skipped where no frozen system lay beside the tree.
- **Authorised on the owner's PC:** nothing beyond what he runs himself.

| Entry | What |
|---|---|
| 392-393 | RAT-68 (H-1 v18); DEV's rebuild on the corrected engine: the same totals and OV-1 values |
| 394-395 | no Git history reset (about 5 MB to gain); one tidy after QA and PROD; the tidy proposal v0.1 |
| 396 | QA created; its first fill a fetching job (the owner); the reviewer's tidy agreement v0.1 committed |
| 397 | RAT-69: H-2 v13, written by the reviewer that ended, corrected by Claude |
| 398 | the new reviewer's takeover; the method template as the fourth deferred discussion, with a dummy method |
| 399-400 | QA's first fill the same as DEV's; the transient Oz Lotto fetch failure; the retry |
| 401-404 | the operations manual: outline, v0.1, the reviewer's review, v0.2, R01 to R05; RAT-70; `ROOT_FILES` |
| 402 | PROD established: item 7 done; the system in production |
| 405-407 | NL-means last; provisional E_63 to E_71; edition 2 (RAT-71); installed in QA and PROD |
| 408 | this handover written as a candidate |

## 7. Where everything is

| What | Where |
|---|---|
| The living system (DEV tree) | `a_p_r_i_r_DEV/` (`src/research/` engine; `src/updater/`; `src/methods/` 40 methods in 12 families; `deploy/`; `tests/`; the launchers and `OPERATIONS_MANUAL.md` at its root) |
| The operations manual | `a_p_r_i_r_DEV/OPERATIONS_MANUAL.md` (the master, edition 2); a pointer in `doc/OPERATIONS_MANUAL.md`; its candidates and reviews in `exchange/` |
| The comparison tools | `a_p_r_i_r_DEV/deploy/compare_with_frozen.py`, `compare_updater_with_frozen.py` (to be retired at the tidy) |
| The file-form checker | `a_p_r_i_r_DEV/deploy/file_form.py`: `faults_of_files(root, relative_paths)` |
| The frozen reference | the top level: `src/`, `tests/`, `Run_Research.bat`, the updater `src/results_master_v0_2.py` |
| The runner | `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (v0.8), `.claude/settings.json` (r2), `inbox/` (last T031), `outbox/` |
| Decisions | `exchange/DECISIONS/DECISION_LOG.md` (LF; appended as bytes) |
| The continuity page | `exchange/CONTINUITY_NOW.md` (LF; its top block and its two handover sections are current) |
| Standing reminders | `exchange/OWNER_REMINDERS.md` (CRLF) |
| Handovers | in force in `doc/HANDOVER/`; Claude's candidates in `exchange/HANDOVER_2026_11_28/` |
| The tidy | `exchange/Claude_Tree_Tidy_Inventory_And_Procedure_v0_1_20261128.md`; `exchange/ChatGPT_Tree_Tidy_Consolidated_Agreement_v0_1_20261128.md` |
| Science kept | `doc/Predictive_Randomness_System_Specification_v0_6.md` (its science sections); R1, R2, R3 and the method designs in `doc/` |
| Coding standards (binding) | `doc/CODING_PRACTICES_v0_1.md`; `doc/FILE_FORM_STANDARD_v0_2.md` as the scheme changed it |

**Running the tests** (in `a_p_r_i_r_DEV`): `PYTHONPATH=src:src/methods:tests python -B -m unittest discover -s
tests -p "test_research_*.py"` (on Windows `set PYTHONPATH=src;src\methods;tests`). About 90 seconds in the
cloud; all on invented draws; no test lets the real updater run.

**The cloud workspace does not carry over between chats.** Clone `main`; use Python 3.15 with the packages of
`requirements.txt`. The top-level `source_data` holds the results the first system accepted (through 1591 and
1708); the trees' newer results are on the owner's PC only. To repeat the frozen comparison, H-1 v18 section 7
gives the recipe; after the tidy it will no longer exist.

**The updater file** was made by scripted exact removals from the frozen updater; edit
`src/updater/results_updater.py` directly, and keep `compare_updater_with_frozen.py`'s declared lists up to date
while that tool exists.

**What the rehearsal taught, for the next task file** (if the runner is used again): a backslash before `*` breaks a
permission rule, and `:*` at a rule's end means "a space, then anything", so use forms like `*T:*a_p_r_i_r*`; the
guard refuses any shell command whose text holds the updater's file name; the runner's shell may have a virtual
environment active (start environment scripts inside `( unset VIRTUAL_ENV; ... )`); a test fixture that appends in
text mode writes CRLF on Windows, so write bytes.

## 8. What comes next

**1. The one tree tidy (the scheme's step 7), now due: QA and PROD exist.** Agreed in principle by the reviewer and
the owner (entries 394 to 398; the reviewer's consolidated agreement v0.1 with its corrections C01 to C04):

- **No Git history is rewritten.** Retain every commit.
- **Claude writes the revised candidate and the exact list (P1)** against the tree as it is, then the reviewer reads
  both and the owner ratifies (RAT-72 or later). What the revision must take in:
  - C01 to C04 of the agreement (local OV-1 cohorts; the two VS Code paths in `.vscode/settings.json` changed to
    DEV's `.venv`; full-path untracked deletion only, with rollback; the owner's no-update check after his pull).
  - **The `exchange/` rule** (Claude's of entry 396, the reviewer's concurrence of 398): keep every EX message and
    every written file (`.md`, `.txt`, `.json`); remove only the code and data copies (`.py`, `.diff`, `.zip`,
    `.bat`, `.ini`, `.cmd`) in the EX folders and `CLAUDE_WEB_TOOLS/`, **except where a code file or attachment
    embodies a unique scientific idea**: look for these by name (method sketches, prototypes); keep when in doubt.
  - **Keep** `doc/METHOD_TEMPLATE/` (entry 398),
    `exchange/ChatGPT_to_Claude_Operations_Manual_Discussion_v0_1_20261125.md`, the manual's candidates and reviews,
    every source of the manual's Appendix D (R1, the Methods A and B proposal, `doc/GASI_thought_experiments/`), the
    first system's `results/`, the runner's whole folder, the records.
  - **Retire** the first system's software, tests, launchers, `source_data`, `transitory_data` and `.venv`; the two
    comparison tools and their 8 tests (282 to 274), the helpers the other updater tests use moved unchanged into a
    fixtures file; no `src/` file changes (so no fingerprint and no rebuild); one comment line in the updater that
    names the retired tool is left as it is.
  - **The runner's rulebook v0.9:** the runner's Python becomes real DEV's, as an interpreter only (`-I -B`, no
    `pip`); the first system's text removed. Ratified separately before the top-level `.venv` goes.
  - An annotated tag `before_tidy_<date>` pushed first; `ARCHIVE_INDEX.md` saying how to read what was removed; a
    fresh verified full-project backup first; the owner deletes untracked leftovers only from a list of full paths.
- Also then: widen the install message "only the updater or the launchers differ" to name the root files
  (`deploy/`, outside every fingerprint).

**2. The rest of step 7:** the decision log and the continuity page converted to CRLF, and the continuity page cut
down to what is current; both handovers refreshed after the tidy.

**3. Step 8, the research.** First, together, **the four deferred discussions** (`exchange/OWNER_REMINDERS.md`):
future method priorities (entry 289; the draft is not read until then); the roles of the two AIs and a possible
reversal trial (292); minimal coding-practice improvements (299); **the method template, proven boilerplate, a
dummy method and the template's relation to the manual (398).** The agreed sequence: (a) the four discussions; (b)
the simplified template, boilerplate and dummy method, outside the living `src/`; (c) the dummy method proved with
the real engine in an isolated temporary tree on invented draws (a trivial history-dependent calculation, equal
scores for the tie rule, both games, compute/verify agreement, short history, legal outputs, TOP and WORST from one
ranking, never entering real results), kept as a permanent regression test; (d) the first new scientific method from
that boilerplate. No generator script. **The research catalogue:** R2's E_1 to E_62; provisional E_63 to E_71
(entry 405; temporary labels, R2 not amended, no order decided) with **NL-means (E_71) last** by the owner's
direction.

## 9. Working practices

- **The coding practices** (`doc/CODING_PRACTICES_v0_1.md`, RAT-40) apply to all code: a plain-English header on every
  `.py` file; constants at the top with a comment; a comment on every function saying what it does, each
  parameter, what it returns with an example, and what makes it refuse; names that say what a thing is; messages
  that say what happened, where, why and what to do; nothing swallowed; one shared piece of code per shared task;
  each test named for the rule it proves, with a planted fault. **Every code commit says "coding practices met" or
  lists the exceptions with reasons.** Under the scheme, read three items this way until the owner ratifies a
  revision: a header names the scheme's section where the part is administrative; "held or not current" becomes
  "rebuilt"; and "a variant's files can never change once installed" no longer holds. Lines of code at most 120
  characters (tests 140; a file that came from the frozen top level keeps its own long lines).
- **Proving a change:** plant each fault the change guards against and show the tests catch it. Run pyflakes, the
  file-form checker over every tracked file of `a_p_r_i_r_DEV`, and the whole suite before each code commit. Before
  a change to an engine file, say what its fingerprint change costs. A behaviour-preserving change is checked by
  equal totals and OV-1 values, and detailed results where it matters; a scientific change by its own mathematics
  and tests.
- **The file form:** every text file of the living system is CRLF and ASCII, the `.jsonl` records and the manual
  included. The frozen top level is not changed.
- **An edit of the manual** makes the INFRA flag out of date: the owner then runs `Make_Installable.bat INFRA`,
  commits the flag, and installs; each install runs the tree's ordinary job, which finds nothing to make again.
  Batch editorial edits with the next ordinary install.
- **The decision log:** record every owner decision at once, in his words. **Write each record in a command of its
  own, with its checks (the time read from `TZ=Australia/Adelaide date`, line widths, the expected last line), and
  commit only after it has succeeded.** Four times on 28 November a record's line-length check stopped it after the
  commit beside it had already gone out; a shell's stop-on-error does not cover a command inside an `&&` chain
  followed by more lines, so give the writing command `|| exit 1` and commit in a separate step. Each entry ends
  "Next numbers: ...".
- **The continuity page:** a new bullet at the top of "For the owner: NOW" and the "Last updated" line, at each
  milestone; its "If a chat ends" and "Installed handovers" sections at each ratification of a handover.
- **Git:** fetch, then look at `git status -sb` and `git log HEAD..origin/main` before each commit (the reviewer and
  the owner commit too; take their commits in first). Look at `git diff --cached --stat` before committing. Never
  type a hash: compute it.
- **Documents:** every new text file CRLF and ASCII; the decision log and the continuity page are LF until the
  tidying. Lines of documents at most 120 characters.
- **Commit trailer:** the attribution lines the session gives you.
- **Numbers at this writing:** next EX is EX_334 (Claude's); next decision log entry 409; next ratification RAT-72
  (this document's). The decision log's last line is the authority.

## 10. Taking over

1. Add the repository (push access) and read section 0's list. Check this document's statements against the
   repository; do not take summaries on trust.
2. Give the owner your first reply: what you understand the state to be, what is and is not authorised, the next
   deliverable, and anything unclear or inconsistent. Build and commit nothing yet.
3. The owner decides whether to accept the takeover. He may ask the reviewer to put a few questions to you first.

END.
