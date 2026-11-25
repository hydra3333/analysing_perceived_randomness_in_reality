"""The new texts of H-1 v14 (the consolidated edition): the header, chapter 0, and Appendix C. Plain text with LF;
the builder writes them CRLF. Names in braces are filled in by the builder from Git."""

HEADER = '''# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v14

**Document:** H-1 under the agreed roles position v0.1r1, section 9 item 4.
**This edition: v14, 25 November 2026 (Adelaide, UTC+10:30). {STATUS}**
**It is the consolidated edition the owner and the reviewer asked for** (decision log entries 271, 272 and 284;
EX_317 finding H13-C04): H-1 v9 to v13 each added a layer that prevailed over the older ones (sections 0B, 0D, 0E),
and a new chat had to read them all to learn what was true. **In this edition chapter 0 is the whole live position,
written afresh, and it is the only place that says what is true now.** Sections 0A and 0C and sections 1 to 12 with
the appendices are the standing knowledge: carried from H-1 v13, with the stale statements the takeover and the
reviewer's cold read found corrected in place, each marked "(v14)". The three layered sections of H-1 v13 (0B, 0D,
0E) are kept byte for byte at the end under the heading HISTORY: they are the detailed record of 23 to 25 November
2026 and are not live. Sections 1, 2 and 2A are byte for byte H-1 v7r1's, as in every edition (the builder
asserts it). Built from the installed H-1 v13's Git bytes (RAT-54; SHA-256
`37aa0196e828ddf012c83d61c66c49f814892341ffe88d1dc976609da289bbae`) by
`exchange/CLAUDE_WEB_TOOLS/h1v14/make_h1_v14.py`; Appendix C says exactly what was carried, changed and moved.
H-1 v13 and its predecessors stay in `doc/HANDOVER/` as history; their long headers of "the edition it is built
from" are not repeated here.

**Audience:** any later Claude chat that takes over as primary designer and coder; the ChatGPT reviewer chat, which
checks it against the repository.
**Repository:** `hydra3333/analysing_perceived_randomness_in_reality`, public GitHub, branch `main`.
**Baseline described:** `main` at `{HEAD}` (decision log entry {ENTRY}; newest EX: EX_321).
**Authority:** the ratified documents and the decision log prevail over this handover wherever they differ.
`exchange/CONTINUITY_NOW.md` with the decision log carries whatever is newer. This file authorises nothing.
**Draw values:** none appear in this file.

---

'''

CHAPTER_0 = '''## 0. THE LIVE POSITION (25 November 2026). Read this chapter first; it prevails over everything below it

### 0.1 First actions in a new Claude chat

1. Attach the repository with push access and clone `main` **with its full history** (if
   `git rev-parse --is-shallow-repository` says `true`, run `git fetch --unshallow`). Check the hashes in section 4 and
   Appendix A with `git show HEAD:<path> | sha256sum` (0.7 says which of Appendix A's differ, and why).
2. Read, in this order:
   - the introductory blurb that started your chat (the owner's hard rules, in his words; copied below);
   - `exchange/CONTINUITY_NOW.md`, its top block (the live state; it overtakes this file as soon as anything moves);
   - this chapter 0, then sections 0A and 0C and sections 1 to 12. The HISTORY part at the end is read when a
     question needs the detail of 23 to 25 November 2026, not as part of taking over;
   - **the four ratified documents of section 4.1:** the system specification (its section 0 first: the whole
     system on one page), the deployment design (with its one amendment, RAT-56, in 0.3), the coding practices, and
     the file-form standard `doc/FILE_FORM_STANDARD_v0_2.md`, which is short and governs every file you will write;
   - `exchange/DECISIONS/DECISION_LOG.md`, entries 121 to the latest (the owner's own words). A map: 147 is RAT-40
     (the new design); 158 to 169 build step 1 and the tidy-up; 176 to 212 build step 2; 217 to 243 build step 3's
     go and plan, the reviewer chat of 24 November and the probe TASK_T028; 244 to 261 the file-form standard and
     the conversion of DEV; 262 to 269 H-1 v12 and v13, H-2 v7 and v8, the register v0.33; **270 to the latest are
     the present Claude chat: its takeover, slice A of build step 3 and its review, RAT-56, the end of the reviewer
     chat, H-2 v9 and this edition. Read these in full;**
   - slice A's two notes, which show how a slice is written, proved and reviewed here:
     `exchange/CLAUDE_WEB_TOOLS/step3/slice_a/SLICE_A_PACKAGE_NOTE_v0_1.md` and
     `SLICE_A_CORRECTIONS_AFTER_EX_319_v0_1.md` beside it, with the reviewer's `exchange/EX_319_ChatGPT.md` and
     `EX_321_ChatGPT.md`; and the build plan `exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md`;
   - the installed packages' notes when you come to build a package: `exchange/CLAUDE_WEB_TOOLS/step1/STEP1_PACKAGE_NOTE_v0_3.md`,
     `tidy1/TIDY1_PACKAGE_NOTE_v0_1.md` and `step2/STEP2_PACKAGE_NOTE_v0_3.md`, with the reviewer's findings on them
     (`EX_276`, `EX_283`, `EX_285`) and its passes (`EX_278`, `EX_280`, `EX_290`, `EX_294`);
   - `exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md` (the joint working principle; binding);
   - the reviewer's findings on the design: `exchange/EX_267_ChatGPT.md`, `EX_269_ChatGPT.md`, `EX_271_ChatGPT.md`
     (EX_271 section 3 holds a test still owed, in build step 4);
   - the reviewer's handover in force (0.3 names it);
   - `exchange/README.md` (the exchange protocol, v0.6) and `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (the local
     runner's rulebook, v0.7; section 8.6).
3. Ask the owner where things stand. Do not assume anything has advanced since this file was written, and do not
   assume it has not.
4. **The staged takeover (HO-2), before any work at all.** Your first substantive reply to the owner explains, in
   your own words: what is implemented, what is designed, what is ratified and what is unresolved; the current
   position and the immediate priorities; the next tasks, their dependencies and the approvals outstanding; the
   safety, scientific and operational restrictions; exactly what you believe you are authorised to do next, and what
   you must not do without the owner's further approval; and any discrepancy, uncertainty or question. **Do not
   design, implement, build, install or run anything because this file names it as the next task.** The owner passes
   your reply to the reviewer chat, which sends targeted questions; answer them yourself, from the repository, before
   you see the reviewer's assessment (the owner relays the questions alone). Material discrepancies are resolved
   before the takeover counts as successful. **Until the owner authorises normal work:** read, check hashes and
   write in the chat; build, run and commit nothing, not even under `exchange/`. The takeover is recorded in the
   decision log once the owner accepts it (the last one is entry 270). The outgoing Claude chat stops committing
   once you start. The reviewer chat stays in role through a Claude takeover unless the owner says otherwise.
5. Before any code (once normal work is authorised): name the work item, its risk tier and its reviewer chat
   (section 1.2), and check that the owner has given the go for that step (0.4).
6. Keep `exchange/CONTINUITY_NOW.md` current after every milestone. Record every owner decision in the decision log at
   once, in his words, reading the time from the clock in the command that writes it. **At every milestone ask
   yourself whether the handover should be brought up to date, and tell the owner when it should:** on 25 November
   2026 the reviewer chat ended without warning at its maximum length (entry 282).
7. **Models (MC-1, section 2):** take over on Opus. Before designing a new subsystem, a question of statistical
   validity, the root cause of an unexplained STOP, or a cold read of a design, say "Suggest switching to Fable
   (High) for this" and wait for the owner's go; tell him when a Fable task is finished.

**The owner's hard rules, in his words** (from the blurb of 21 November 2026; binding):

- The one production results source is Lotterywest-GOV (www.lotterywest.wa.gov.au, HTTPS), reached only by my approved
  tools. You never contact any lottery website, and you never search for lottery results.
- You may read draw values, source_data/ and results/. You never write there. Anything you work out in the chat from
  draw values is labelled "suggestive"; results count only from the reviewed programs.
- Method-facing N-1 isolation is never weakened. Games are never pooled. The sealed Mode H records are never altered.
- No program ends another process. The orphan marker blocks all launches. Three safety switches stay False and the
  allowlist stays empty.
- Nothing runs on my PC without my go. No install, run, backup, restore, migration or deletion without my separate
  approval. Nothing ever changes my PC's date, time or time zone. A STOP is a STOP.
- You commit and push documents and records yourself (named paths only; fetch and fast-forward first; nothing deleted
  or overwritten): under exchange/ and CLAUDE_CODE_WORKING_FOLDER_TREE/ freely, into doc/ only once reviewed and
  ratified. Code and tests never go into src/ or tests/ from you. Never edit the reviewer's files.
- A PASS or a ratified design authorises no install or run.

To these add, from the same standing rules: never write under `source_data/`, `results/`, `transitory_data/` or `GAIS/`;
never write the owner's personal name in anything committed (write "the project owner" or `hydra3333`).

**And his standing direction on overheads** (entries 255 and 273; the working principle above): do not over-engineer;
no "software admin" checks and overheads that the science, N-1, scoring and recoverability do not need. Tell him the
simplest safe route first. This is not a request for shorter reporting.

### 0.2 What is installed and proved (all in DEV, the owner's clone on E:; there is no QA and no PROD tree yet)

| Step | Commit | What it is | Proved by |
|---|---|---|---|
| Build step 1 | `0aea10a` | the method files in the new layout (12 families, 40 variants) | the whole suite and the old records, equal |
| The light tidy-up | `c7e6ed8` | the coding practices' headers in 37 method files | the same |
| Build step 2 | `5f16b35` | the research engine `src/research/` with its launchers | the first fill in DEV; 34,800 old score records and 20,436 old forecasts equal |
| The conversion to the file-form standard | `691f58e` | every living text file CRLF, every `.jsonl` LF, Git converts nothing | the suite, a whole fill again, the same comparison |
| The lock line | `fe1c310` | one line of `job_lock.py` (Windows wrote CR CR LF) | the owner's 116 targeted tests |

- **The suite on `main`:** 54 modules, 830 tests, with three known failing tests and no other
  (`test_mhupa_launchers` `test_gitignore_lines`; `test_multigame_reader_contracts`
  `test_master_source_and_ledger_file_hashes` and `test_only_legacy_e1_allowed_at_boundary`). They fail on `main`
  for old reasons and are named in every comparison.
- **The results on file** (the masters, read-only to you): Powerball draws 1144 to 1591, 448 rows; Oz Lotto draws
  1474 to 1708, 235 rows. The updater has not run in the new system; the research results under
  `results/research/` exist only on the owner's PC.
- **The prevailing OV-1 has not started:** it starts at the first successful results step in a tree, which needs
  build step 3. Nothing so far is evidence of predictive success; Mode H's result is a measured null.
- **The old system's code is still in `src/`** beside the engine (section 0A item 1). The three science switches
  are False and the allowlist is empty.
- **The owner's PC:** DEV on E:, converted, filled, Git clean at the last report. The trees to come: QA
  `T:\\a_p_r_i_r`, PROD `G:\\a_p_r_i_r`, backups `T:\\a_p_r_i_r_backups\\QA` and `...\\PROD`; the runner's scratch
  folder `D:\\DELETE_ME\\`. The owner keeps his own whole copies of the project folder on external drives.

### 0.3 The chats, the handovers and the ratifications

- **The present Claude chat** took over from H-1 v13 on 25 November 2026 (HO-2; the reviewer's PASS; the owner's
  acceptance, entry 270). The reviewer's recommendations on six uncertainties it raised are recorded there and were
  followed in slice A (0.5).
- **The reviewer chat that reviewed slice A ended on 25 November 2026 at its maximum length,** just after EX_321
  (entry 282). No finding was open. **The owner starts a new reviewer chat from H-2 v9;** the decision log says
  whether its takeover is done. Until it is, nothing can be reviewed.
- **The reviewer's handover in force: H-2 v9,** `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v9_20261125.md`
  (`{H2V9}`), with its blurb beside it (RAT-57, ratified in advance, entries 282 and 283). **Claude wrote it,** at
  the owner's request, because the reviewer could not: its live chapter 0 only; the reviewer's rights and its
  chapters 1 to 19 are H-2 v8's bytes. It says so itself and asks the new reviewer to verify and correct it. Expect
  the reviewer's own next edition to replace it.
- **Ratifications since the register v0.33** (RAT-53, `doc/RATIFICATION_REGISTER_v0_33.md`, the newest register):
  RAT-54 H-1 v13; RAT-55 the reviewer's H-2 v8; **RAT-56 (entry 280), the one amendment of the deployment design:**
  in its section 2, "(`deploy\\`, standard library only)" is read as "(`deploy\\`, standard library only, except the
  process rule of section 9, which uses psutil from the Python that runs the tool)"; the ratified v0.12 file is not
  edited; restore stays standard library only. RAT-57 H-2 v9. The register's next ordinary edition carries RAT-54
  onward; it still calls the amendment "not ratified", which is stale. A register edition is owed, not urgent.
- **Numbers:** read the log for the last EX, entry and RAT before using one; the reviewer takes EX numbers too.
  At this edition the newest EX is EX_321 and the next free ratification number is in the log's last line.

### 0.4 What is authorised, what waits, and the order of work

**Authorised now:** build step 3's design and cloud coding only (the owner's go, entry 217; the plan
`exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md`, passed by the reviewer in EX_301). Records and working
files under `exchange/`. **Nothing on the owner's PC:** no install, no run, no tree, no runner task. Each of those is
his separate go, and a PASS or a ratification gives none.

**The order (the plan's slices; one install into DEV at the end, entry 219):**

1. **Slice A, foundations: WRITTEN AND REVIEWED, PASS (EX_321). Not installed.** See 0.5.
2. **Slice B: backups (`Run_Snapshot`), the recovery kit, restore (`Restore`).** Not started. It is a new subsystem:
   say "Suggest switching to Fable (High) for this" and wait for the owner's go. What is already decided for it:
   the restore tool is standard library only with its own reader of Windows' processes (entry 222), which must
   agree with psutil's (TASK_T028 showed it does on his PC); a whole verified ZIP of the tree at level 9 (entry
   243); a backup before an overwrite is attempted and reported truthfully, and its failure does not veto the
   owner's typed YES (the confirmation defaults to NO); a restore is of one snapshot the owner chooses, the old
   tree set aside, the restored environment possibly NOT READY; the orphan-marker exception at a restore
   (deployment design; architecture 5C as amended by RAT-40); no program ever ends a process; no monthly restore
   test and no replay comparison (the owner's earlier decisions). `launch_guard.UNFINISHED_OPERATIONS` already
   names `RESTORE_IN_PROGRESS.json` and `SNAPSHOT_IN_PROGRESS.lock`, and takes a `finishing` argument for the
   command that completes an operation.
3. **Slice C:** `Init_Tree`, `Install`, `Reinstall_Infra`, `Verify_Tree`, the half-finished states. `Verify_Tree`
   and `Init_Tree` write the environment's marker with `environment_marker.write_marker`; an install writes the
   list with `installed_files.write_list`.
4. **Slice D:** the clean-sheet updater `results_master_v0_3.py` (entries 180, 181): Lotterywest-GOV only; the old
   v0.2 stays unchanged in DEV; no Mode H preconditions carried over.
5. **Slice E, the joined acceptance:** one rehearsal on Windows by the local runner in a scratch tree under
   `D:\\DELETE_ME\\` (the runner's rulebook v0.7, section 2A), where everything of slices A to D first meets Windows:
   the native environment digest, psutil on real command lines, the real launch paths, timing. Then **one install
   into DEV,** then QA with the transition check against the old records, then PROD. Each on the owner's go.
6. **After build step 3:** the operations manual's skeleton (the reviewer's own first thoughts are on `main`:
   `exchange/ChatGPT_to_Claude_Operations_Manual_Discussion_v0_1_20261125.md`; unread by Claude and not acted on);
   build step 4 (the laboratory tools, the report-staleness test of EX_271 section 3, corrections and reruns); a
   register edition. Section 10 has more detail on each step, written for earlier editions.

**Waiting on the owner at this edition:** his go for slice B; the ratification of this edition. **Waiting on the
reviewer:** nothing, until its new chat has taken over.

### 0.5 Slice A of build step 3: what it is, where it lies, what is settled

**The files:** `exchange/CLAUDE_WEB_TOOLS/step3/overlay/`, {OVERLAY} files laid out as they go into the tree, all CRLF:
16 new and 10 that exist on `main`. New code: `deploy/install_readiness.py`, `install_import_check.py`,
`make_installable.py`, `check_tree.py`, `deploy_command.py`; `src/research/installed_files.py`,
`environment_marker.py`, `process_rule.py`, `launch_guard.py`; two launchers; five test modules
(`tests/test_trees_*.py`). Changed: `ENVIRONMENT.example.ini`, `deploy/INFRA_MANIFEST.ini`,
`src/research/code_identity.py`, `research_job.py`, `settings.py`, `withdraw.py`, `src/research_command.py`,
`tests/research_fixtures.py`, `tests/test_research_identity.py`, `tests/test_research_ov1_and_checks.py`. The
manifest with the slice: {MANIFEST}. **These are working files: nothing of build step 3 is installed until slices
A to D have passed and the joined rehearsal is done.** When later slices change one of these files, the overlay is
changed and the reviewer is told which reviewed bytes moved.

**What it does:** the settings of the three trees (`settings.py`); the readiness markers and `Make_Installable`; the
static import check; the list of installed files `records/INSTALLED_FILES.json`; one digest of a tree's own
Python environment and its marker `.venv/ENVIRONMENT_VERIFIED.json`; `Check_Tree.bat DEV|QA|PROD`, run from DEV,
read-only; the process rule (psutil); and the launch guard: `check_at_launch` at every launch,
`check_at_job_start` under the job lock, `check_software_is_as_installed` and `check_no_unfinished_operation` for
every command that writes.

**Settled, with the reviewer's concurrence or the owner's decision. Do not reopen:**

1. **One environment digest, the full one of specification 13, of each tree's own `.venv`, in every tree** (the
   owner's option A, entry 275). It covers `pyvenv.cfg`, every file under `Scripts` and under `Lib\\site-packages`
   (caches and compiled files apart), and the base Python's version, path and program-file bytes. A missing part or
   an unreadable file or folder refuses. It goes into the envelope of every forecast a job makes. Cost on his PC:
   each job reads its environment first, 5 to 150 seconds (TASK_T028).
2. **The trees are independent** (the owner, entry 275): in routine work no tree reads another's environment or
   records. `Check_Tree`'s comparison with DEV is information, never a gate.
3. The manifest's `[files]` must exist in every tree; its `[install_tool]` files only where DEV asks for that list.
4. The guard's four modules are classed `derived` (the job calls them); forecast-class identity is unchanged.
5. The process rule applies at the start of a job in every tree, DEV too: a DEV job refuses while another Python of
   the DEV tree runs. A status file's presence stays the job's own check, game by game.
6. A withdrawal checks, under its two locks and before it writes: no unfinished operation (every tree); the
   software matches its list (QA and PROD). `Make_Installable` refuses beside an unfinished operation's file or the
   orphan marker. `Check_Tree` only reports.
7. No repair command; no cache-removal machinery; no DEV registry of installs; `records\\INSTALLED_FILES.json` and
   `records\\INSTALL_LOG.jsonl` are required in every installed tree; no release registry and no Git outside DEV.

**Its review:** EX_318 (the slice), EX_319 (RECHECK: two blockers, three corrections, all true), EX_320 (the
corrections), EX_321 (PASS). **Its evidence is the cloud's only** (Linux, Python 3.15.0b4): 59 modules, 1000 tests,
the three known failing tests and no other; planted faults 22, 31 and 22, all caught. The digests in the tests are of
invented Windows-layout files. Nothing of it has run on Windows.

### 0.6 Working rules that hold now (each learned the hard way; the HISTORY part and section 8.8 tell the stories)

- **Every text file you add is CRLF** (`.sh` and `.jsonl` are LF), written as bytes or with the line ending named;
  the cloud converts nothing. **Files that existed before 25 November 2026 keep their form:** the decision log and
  `exchange/CONTINUITY_NOW.md` are LF and are appended to as bytes; older files under `exchange/`, `doc/` and
  `review/` are frozen. A file's bytes are the same in Git, in a clone and on the owner's disk: hashes are compared
  exactly and nothing is "normalised" first. **This overrides every older instruction in this file about LF,
  `core.autocrlf` or tolerating CRLF working copies** (sections 1.6, 2, 5.1, 6, 8.5, 12.3, 12.6 hold such text;
  EX_317 H13-C02). No rehearsal in an LF clone and a CRLF clone is owed for those old assumptions.
- Any low-level write of text is binary (`os.open` with `O_BINARY`, or `open(..., 'wb')`). Only a run on Windows
  shows Windows' own translation.
- **Never type a hash or a time:** compute the one from Git's bytes (`git show :<path>`) and read the other from
  the clock in the command that writes it. Look at `git diff --cached --numstat` before every commit.
- **Fetch immediately before taking an EX number, before committing and before installing a document;** the
  reviewer commits too. **Push nothing between the owner's pull and his push on a day of install.**
- When the owner relays a reviewer's result, fetch and read the EX file itself before acting; he may paste an
  older message by mistake (it happened on 25 November).
- **Issue or revise an EX message only when the owner asks.** Discuss his queries with him first. A decision is put
  as question, why, recommendation, options; name things exactly (a question about "the environment" was read as
  one tree checking another's; say "a tree's own `.venv`").
- **The cloud's evidence is not Windows'.** Say which it is every time. Three Windows facts already cost time: the
  C runtime's text mode, the refusal of a rename while a file is open, and that every program started from an
  environment is two processes.
- A comparison that lists a test as NEW does not say that it passes: read the suite's own lines.
- **Before a slice goes to review, walk every command that writes through each new guard.** In slice A the job was
  guarded and the withdrawal and `Make_Installable` were not (EX_319 A-B02).
- Give the reviewer the exact differences as well as the hashes: it rebuilds each changed file from the hunks and
  need not reread the rest.
- A workspace helper that edits files must be safe to run twice (an edit is made exactly when its new text is
  present); two helpers that undid each other's edits cost a suite run.
- For a one-off job, begin from the smallest thing that would do. A reviewer's recheck can over-engineer too: say
  so to the owner with the risk each demand guards against; the decision is his. When he says stop, stop.
- When he ratifies one document in advance, his word does not stretch to the next: ask.
- **If the reviewer chat ends without a handover of its own,** its next edition is built from its own last
  edition's bytes: live chapter only, its rights and inherited chapters untouched, the authorship stated in the
  document and in its blurb (entries 282, 283).

### 0.7 The cloud workspace, and what in this file is known to be out of date

**The workspace** is gone when a chat ends. To make it again: a clone of `main` to commit from; a second, disposable
clone to run tests in; Python 3.15 (the cloud had 3.15.0b4, installed with `uv`) with numpy, scipy and psutil.
`exchange/CLAUDE_WEB_TOOLS/step1/run_suite.py <tree> <report folder>` runs the whole suite (about ten minutes) and
`compare_suite_reports.py <before> <after>` compares two runs test by test.
`exchange/CLAUDE_WEB_TOOLS/step3/sync_and_test.sh <clone> <python> [modules]` copies the overlay into a disposable
clone and runs modules with `PYTHONPATH=src:src/methods:tests`. The three `mutation_check_*.py` beside it plant one
fault at a time and expect the tests to fail; their paths at the top are the workspace's and are set again.

**Known to be out of date below, and left as written** (the corrections made in place are in Appendix C):

- **Appendix A:** nine of its hashes are of the files before the conversion. Eight differ from today's by line
  endings only; `deploy/INFRA_MANIFEST.ini` also by the one line `src/research/windows_text.py = derived`. Old
  identities stay with their commit; today's hash is of today's exact bytes.
- **Section 7.1** gives the manifest on `main` as it was at build step 2; it is now {MANIFEST_MAIN}.
- **Sections 7.5, 10 and 12.8** were written for H-1 v9 to v12. Where they say what has run, what is next or what
  is open, this chapter is the present truth.
- **Section 0C item 1 and section 1.1** on the reviewer chats: 0.3 above is the present truth.

---

'''

APPENDIX_C = '''## Appendix C. What changed from H-1 v13 (the builder's own account)

**Carried byte for byte from H-1 v13** (the builder asserts each): sections 1, 2 and 2A (H-1 v7r1's text); and
sections 0B, 0D and 0E, moved to the HISTORY part at the end with their headings, so that a reference such as
"section 0E item 14" still finds its text.

**Written afresh:** the header and chapter 0 (sections 0.1 to 0.7), which take the place of H-1 v13's header,
its section 0 and the live content of its sections 0B, 0D and 0E. This Appendix.

**Carried with corrections made in place, each marked "(v14)":**

{CORRECTIONS}

**Nothing else is changed.** Everything of H-1 v13 that is not named above is in this edition byte for byte, in the
same order: sections 0A and 0C (but for their corrections), sections 3 to 12, Appendices A and B.

**The findings this edition answers:** decision log entry 270, points (a) to (h); EX_317, H13-C01 (the OV-1
kernel: section 7.3), H13-C02 (hashes and line endings: 0.6, 0.7), H13-C03 (records in an installed tree: section
5.3, 0.5 item 7), H13-C04 (the layers: this whole edition), O01 (the two-site checker: section 5.1) and O02 (H-1 v13's
header said no reviewer had read it before installation; the reviewer had checked its difference from H-1 v12, its
hashes and its carried sections before ratification, and made the full cold read afterwards, EX_317).

---

'''
