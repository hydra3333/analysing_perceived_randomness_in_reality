"""Workspace helper (not project code): the texts of H-1 v15 written afresh (its header, chapter 0, Appendix D and its
blurb). make_h1_v15.py beside this file puts them together with H-1 v14's bytes. Placeholders in braces are filled
in by the builder from Git."""

HEADER = '''# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v15

**Document:** H-1 under the agreed roles position v0.1r1, section 9 item 4.
**This edition: v15, 25 November 2026 (Adelaide, UTC+10:30). A CANDIDATE for the owner's ratification** (decision
log entry 315). It goes into `doc/HANDOVER/` only once he has ratified it; the reviewer has not read it.
**It is the next ordinary edition after the consolidated H-1 v14** (RAT-58). **Chapter 0 is written afresh and is the
only place that says what is true now:** slices A and B of build step 3 have passed review, slice C is written and
is with the reviewer (EX_328), nothing of build step 3 is installed. Sections 0A and 0C, sections 1 to 12 and the
appendices are H-1 v14's, with the corrections the reviewer's cold read of v14 asked for (H14-C01 to H14-C03 and its
two observations) and the closing of OUTLANDISH_01 made in place, each marked "(v15)"; Appendix D lists every one.
The HISTORY part at the end (sections 0B, 0D and 0E of H-1 v13) is carried as v14 carried it. **Sections 1, 2 and 2A
are byte for byte H-1 v14's and v13's** (the builder asserts it); **they are H-1 v7r1's text, the same as v7r1's
only after line endings are normalised** (v7r1 is LF; this file is CRLF; the reviewer's H14-C02). Built from the
installed H-1 v14's Git bytes (RAT-58; SHA-256 `{v14_sha}`) by `exchange/CLAUDE_WEB_TOOLS/h1v15/make_h1_v15.py`.
H-1 v14's own chapter 0 is not carried: H-1 v14 stays in `doc/HANDOVER/` as history.

**Audience:** any later Claude chat that takes over as primary designer and coder; the ChatGPT reviewer chat, which
checks it against the repository.
**Repository:** `hydra3333/analysing_perceived_randomness_in_reality`, public GitHub, branch `main`.
**Baseline described:** `main` at `{head}` (decision log entry 315; newest EX: EX_328).
**Authority:** the ratified documents and the decision log prevail over this handover wherever they differ.
`exchange/CONTINUITY_NOW.md` with the decision log carries whatever is newer. This file authorises nothing.
**Draw values:** none appear in this file.

---

'''

CHAPTER0 = '''## 0. THE LIVE POSITION (25 November 2026, late). Read this chapter first; it prevails over everything below it

### 0.1 First actions in a new Claude chat

1. Attach the repository with push access and clone `main` **with its full history** (if
   `git rev-parse --is-shallow-repository` says `true`, run `git fetch --unshallow`). **Check identities in two
   kinds** (the reviewer's observation on v14): a hash this file gives for a *living* file (the handovers in force,
   the ratified documents, the overlay's files) is checked against today's bytes with `git show HEAD:<path> |
   sha256sum`, and must agree exactly; a hash of an *older* identity (nine rows of Appendix A, written before the
   conversion of 25 November 2026) identifies those older bytes at their commit and is not expected to equal
   today's. Section 4 and Appendix A now say, as the builder computed them, which of their hashes equal today's
   bytes (v15): all of section 4's, and all but those nine of Appendix A's.
2. Read, in this order:
   - the introductory blurb that started your chat (the owner's hard rules, in his words; copied below);
   - `exchange/CONTINUITY_NOW.md`, its top block (the live state; it overtakes this file as soon as anything moves);
   - this chapter 0, then sections 0A and 0C and sections 1 to 12. The HISTORY part at the end is read when a
     question needs the detail of 23 to 25 November 2026, not as part of taking over;
   - **the four ratified documents of section 4.1:** the system specification (its section 0 first: the whole
     system on one page), the deployment design (with its one amendment, RAT-56, in 0.3, and one more proposed,
     0.4), the coding practices, and the file-form standard `doc/FILE_FORM_STANDARD_v0_2.md`, which is short and
     governs every file you will write;
   - `exchange/DECISIONS/DECISION_LOG.md`, entries 121 to the latest (the owner's own words). A map: 147 is RAT-40
     (the new design); 158 to 169 build step 1 and the tidy-up; 176 to 212 build step 2; 217 to 243 build step 3's
     go and plan and the probe TASK_T028; 244 to 261 the file-form standard and the conversion of DEV; 262 to 269
     H-1 v12 and v13, H-2 v7 and v8, the register v0.33; **270 to the latest are the present Claude chat: its
     takeover; slice A and its review (271 to 281); the reviewer chat's end, H-2 v9 and H-1 v14 (282 to 286); the new
     reviewer chat (287); slice B and its review (288 to 300); slice C (301 to 313); this edition (314, 315). Read
     these in full;**
   - **build step 3's working record:** the build plan `exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md`;
     each slice's package note and corrections notes (`step3/slice_a/`, `step3/slice_b/`, `step3/slice_c/`) with the
     reviewer's replies (`EX_319`, `EX_321` for A; `EX_323`, `EX_325`, `EX_327` for B); and the working notes kept
     while each slice was written (`step3/SLICE_B_PLAN_AND_NOTES.md`, `step3/SLICE_C_PLAN_AND_NOTES.md`; the second's
     section 0 is the list of checks to make after a stop);
   - the installed packages' notes when you come to build a package: `exchange/CLAUDE_WEB_TOOLS/step1/STEP1_PACKAGE_NOTE_v0_3.md`,
     `tidy1/TIDY1_PACKAGE_NOTE_v0_1.md` and `step2/STEP2_PACKAGE_NOTE_v0_3.md`, with the reviewer's findings on them
     (`EX_276`, `EX_283`, `EX_285`) and its passes (`EX_278`, `EX_280`, `EX_290`, `EX_294`);
   - `exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md` (the joint working principle; binding);
   - the reviewer's findings on the design: `exchange/EX_267_ChatGPT.md`, `EX_269_ChatGPT.md`, `EX_271_ChatGPT.md`
     (EX_271 section 3 holds a test still owed, in build step 4);
   - the reviewer's handover in force (0.3 names it), and its cold read of H-1 v14,
     `exchange/ChatGPT_to_Claude_H1_v14_Cold_Read_20261125.md`;
   - `exchange/README.md` (the exchange protocol, v0.6) and `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (the local
     runner's rulebook, v0.7; section 8.6);
   - `exchange/OWNER_REMINDERS.md`, its standing reminders at the end (the discussions deferred to just before new
     methods are begun; the operations manual's sections the owner has asked for).
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
   (High) for this" and wait for the owner's go; tell him when a Fable task is finished. The owner switches models
   himself, sometimes in the middle of a task; a chat that resumes after a model reset makes the checks of section 0
   of the slice's working notes before anything else (entry 302).

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

**The orphan marker, read exactly** (the reviewer's H14-C03): the rule above stands, and nothing clears or bypasses
the marker in place; the owner's approved manual procedure is the only way to clear it. **The one exception already
ratified (RAT-40) is the restore's,** deployment design section 12: at a restore, a stale marker is set aside as
evidence, not cleared, and only when all four of its conditions hold (the tool showed it with a warning that
recommends restarting the PC; the PC was started after the marker was written; a fresh process check made after that
is CLEAN; the owner types the sentence it asks for). Slice B carries it out; nothing else does.

To these add, from the same standing rules: never write under `source_data/`, `results/`, `transitory_data/` or `GAIS/`;
never write the owner's personal name in anything committed (write "the project owner" or `hydra3333`).

**And his standing direction on overheads** (entries 255 and 273; the working principle above): do not over-engineer;
no "software admin" checks and overheads that the science, N-1, scoring and recoverability do not need. Tell him the
simplest safe route first. This is not a request for shorter reporting.

### 0.2 What is installed and proved (all in DEV, the owner's clone on E:; there is no QA and no PROD tree yet)

**Nothing has been installed since H-1 v14.** Build step 3 is written in the cloud and is not installed (0.5).

| Step | Commit | What it is | Proved by |
|---|---|---|---|
| Build step 1 | `0aea10a` | the method files in the new layout (12 families, 40 variants) | the whole suite and the old records, equal |
| The light tidy-up | `c7e6ed8` | the coding practices' headers in 37 method files | the same |
| Build step 2 | `5f16b35` | the research engine `src/research/` with its launchers | the first fill in DEV; 34,800 old score records and 20,436 old forecasts equal |
| The conversion to the file-form standard | `691f58e` | the living text files converted under RAT-50 (0.6 says exactly which) | the suite, a whole fill again, the same comparison |
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

- **The present Claude chat** took over from H-1 v13 on 25 November 2026 (HO-2; entry 270) and wrote slices A to C
  of build step 3, H-2 v9 at the owner's request, H-1 v14 and this edition. It was compacted once in the evening of
  25 November and lost nothing (entry 303).
- **The reviewer chat that reviewed slice A ended at its maximum length** just after EX_321 (entry 282). **The
  present reviewer chat took over from H-2 v9** (entry 287) and reviewed slice B (EX_323, EX_325, EX_327: PASS) and
  made the cold read of H-1 v14 (`exchange/ChatGPT_to_Claude_H1_v14_Cold_Read_20261125.md`: PASS with the
  corrections H14-C01 to C03 and two observations, all made in this edition; Appendix D). **It now holds slice C
  (EX_328); its reply will be EX_329.**
- **The reviewer's handover in force: H-2 v9,** `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v9_20261125.md`
  (`{h2v9_sha}`), with its blurb beside it (RAT-57; entries 282 and 283). **Claude wrote it,** at the owner's
  request, because the reviewer could not: its live chapter 0 only; the reviewer's rights and its chapters 1 to 19
  are H-2 v8's bytes. Expect the reviewer's own next edition to replace it.
- **Ratifications since the register v0.33** (RAT-53, `doc/RATIFICATION_REGISTER_v0_33.md`, the newest register):
  RAT-54 H-1 v13; RAT-55 the reviewer's H-2 v8; **RAT-56 (entry 280), the one amendment of the deployment design so
  far:** in its section 2, "(`deploy\\`, standard library only)" is read as "(`deploy\\`, standard library only,
  except the process rule of section 9, which uses psutil from the Python that runs the tool)"; the ratified v0.12
  file is not edited; restore stays standard library only. RAT-57 H-2 v9. RAT-58 H-1 v14 (entry 286). **This
  edition takes the next free number when the owner ratifies it.** A second amendment is proposed and waits for the
  reviewer's view before the owner ratifies it (0.4). The register's next ordinary edition carries RAT-54 onward; it
  is owed, not urgent.
- **Numbers:** read the log's last line for the next EX, entry and RAT before using one; the reviewer takes EX
  numbers too. At this edition the newest EX is EX_328 (Claude's); the reviewer's next is EX_329 and Claude's next
  EX_330.

### 0.4 What is authorised, what waits, and the order of work

**Authorised now:** build step 3's design and cloud coding only (the owner's go, entry 217; the plan
`exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md`, passed by the reviewer in EX_301; each slice also had
the owner's own go: A, entry 270; B, entry 288; C, entry 301). Records and working files under `exchange/`.
**Nothing on the owner's PC:** no install, no run, no tree, no runner task. Each of those is his separate go, and a
PASS or a ratification gives none.

**The order (the plan's slices; one install into DEV at the end, entry 219):**

1. **Slice A, foundations: PASS (EX_321).** Not installed.
2. **Slice B, backups, the recovery kit, restore: PASS (EX_327).** Not installed.
3. **Slice C, creating a tree, the installs, verifying a tree: WRITTEN, WITH THE REVIEWER (EX_328).** Not
   installed. **Waiting on the reviewer: EX_329.** Answer each finding narrowly, as for A and B: a corrections note,
   the exact differences, hashes, the affected tests and the planted faults for what changed; no redesign.
4. **The amendment the owner's decision needs (entry 305): `Verify_Tree.bat` does not run the test suite.** Its
   proposed wording of deployment design section 7 and specification section 13 is in slice C's package note,
   section 3. **The owner ratifies it only after the reviewer's view** (the next free RAT number then).
5. **Slice D:** the clean-sheet updater `results_master_v0_3.py` (entries 180, 181): Lotterywest-GOV only; the old
   v0.2 stays unchanged in DEV; no Mode H preconditions carried over. **It needs the owner's go,** and it is a new
   subsystem: say "Suggest switching to Fable (High) for this" first.
6. **Slice E, the joined acceptance:** one rehearsal on Windows by the local runner in a scratch tree under
   `D:\\DELETE_ME\\` (the runner's rulebook v0.7, section 2A), where everything of slices A to D first meets Windows
   (0.5 lists what each slice left for it). Then **one install into DEV,** then QA with the transition check against
   the old records, then PROD. Each on the owner's go.
7. **After build step 3:** the operations manual (the reviewer's first thoughts are on `main`,
   `exchange/ChatGPT_to_Claude_Operations_Manual_Discussion_v0_1_20261125.md`, unread by Claude; the owner has asked
   for an appendix of every method family and method with a short description, entry 289, and a section on
   changing Python versions, entry 305); build step 4 (the laboratory tools, the report-staleness test of EX_271
   section 3, corrections and reruns); a register edition.
8. **Deferred by the owner to just before new methods are begun** (all in `exchange/OWNER_REMINDERS.md`): the
   reviewer's draft `doc/Predictive_Randomness_Future_Method_Priorities_v0_1_DRAFT.md`, not to be read until then
   (entry 289); the roles of the two AIs, where the owner favours a trial (entry 292); both AIs' review of
   `doc/CODING_PRACTICES_v0_1.md`, kept minimal (entry 299).

**Waiting on the owner at this edition:** his ratification of this edition; later, of the amendment. **Waiting on the
reviewer:** EX_329.

### 0.5 Build step 3 in the overlay: what lies where, and what is settled

**The files:** `exchange/CLAUDE_WEB_TOOLS/step3/overlay/`, 54 files laid out as they go into a tree, all CRLF:
slice A's 26 (16 new, 10 that exist on `main`), slice B's 8 new, slice C's 20 new; slices B and C changed some of
the earlier ones, and each told the reviewer exactly which reviewed bytes moved. The manifest in the overlay:
48 files in `[files]` (forecast 13, derived 22, other 13) and 20 install-tool files. **These are working files:
nothing of build step 3 is installed until slices A to D have passed and the joined rehearsal is done.**
`exchange/CLAUDE_WEB_TOOLS/step3/sync_and_test.sh` lays the overlay over a disposable clone to test it.

**Slice A (foundations):** the settings of the three trees; the readiness markers and `Make_Installable`; the static
import check; `records/INSTALLED_FILES.json`; one digest of a tree's own Python environment and its marker
`.venv/ENVIRONMENT_VERIFIED.json`; `Check_Tree.bat`, read-only; the process rule (psutil); the launch guard. Settled
with the reviewer or by the owner, not to be reopened: one full environment digest per tree (option A, entry 275);
the trees are independent in routine work (entry 275); the guard's modules are `derived`; the process rule holds at
every job start, DEV too; no repair command, no release registry and no Git outside DEV; `INSTALLED_FILES.json` and
`INSTALL_LOG.jsonl` in every installed tree.

**Slice B (backups, the recovery kit, restore):** `src/research/snapshot.py` (a verified whole-tree ZIP at level 9,
written only of a quiet tree, read back member by member; the research job's backups at its start when one is owed
and at its end; `Run_Snapshot.bat`); `deploy/recovery_kit.py`; `deploy/restore_tool.py` with `Restore.bat` and
`HOW_TO_RESTORE.txt` (one file, standard library only, its own reader of Windows' processes; the orphan exception of
0.1). Settled at its review: a backup is never made while a job lock or the updater's lock lies in the tree (the job
backs up after releasing its lock); a failed backup never stops a job and is told exactly; a restore checks its
destination against the backup's own settings and refuses a role that is not QA or PROD.

**Slice C (creating a tree, the installs, verifying a tree):** the checks that travel with the installed software
(`src/research/tree_checks.py`: the smoke case, the fixed forecast sample, the derived results in full); `Verify_Tree`
(`tree_verify.py`); the program an install tool starts with the target's own Python (`src/tree_checks_command.py`:
`verify`, `checks`, `reports`); what the installs share (`deploy/install_common.py`, `suite_on_copy.py`,
`SUITE_MANIFEST.ini`); `Init_Tree`, `Install`, `Reinstall_Infra`. Its package note
`exchange/CLAUDE_WEB_TOOLS/step3/slice_c/SLICE_C_PACKAGE_NOTE_v0_1.md` lists the readings (C-R1 to C-R15). The ones
a new chat must know:
- **`Verify_Tree` does not run the suite** (owner, entry 305; the amendment of 0.4 item 4). Only a failed smoke case
  withholds the environment's marker; a difference in the forecast sample or the derived results is said in
  capitals and does not, because the tree's own remedy cannot start without a verified environment.
- **The suite of an install** is `deploy/SUITE_MANIFEST.ini` (23 modules, the tests of the new system), run with the
  target's Python on a temporary copy of DEV's `src`, `deploy`, `tests` and root files, at `Init_Tree` and every
  `Reinstall_Infra`, and at an ordinary install when the target's infrastructure is file for file DEV's.
- **The conflict of reading C-R9, put to the reviewer:** the design has `Reinstall_Infra` hold the job lock through
  its `PRE_INFRA` backup; slice B never backs up under a job lock; the reading lets the lock go for the kit, the
  backup and the question and takes it again before anything is overwritten.
- **`Reinstall_Infra` refuses** any plan that touches a forecast-class file, and also a file moved into or out of the
  forecast class with its bytes unchanged (the identity of the forecasting code is taken over that class).
- **The owner's four environment scripts are now infrastructure** (`create_venv.bat` and the other three, class
  `other`), so that a new tree holds them and a change reaches a tree by `Reinstall_Infra`.

**The evidence of build step 3 is the cloud's only** (Linux, Python 3.15.0b4, numpy, scipy, psutil): at slice C's
final files, 68 modules and 1334 tests, the three known failing tests and no other; planted faults in every slice,
all caught (slice C alone: 250). The real chain was run once in the cloud: a creation on the project's real software,
then the checks program started for real under a tree's own Python, where all 40 real variants passed their smoke
cases. **Kept for the joined Windows rehearsal:** the native environment digest; psutil on real command lines; the
restore's process reader and launcher chain; a real rename; a restored Python that imports; the size and time of a
real whole-tree backup; the second half of a creation and `Install` and `Reinstall_Infra` end to end with a real
Windows target; every launcher; the whole suite on the final bytes on Windows.

**Carried to the joined package, not done in any slice:** tests that make a link must skip where Windows refuses
(WinError 1314 on the owner's account; in `test_trees_restore`, `test_trees_snapshot`, `test_trees_settings` and
`research_fixtures`); the early refusal's line of the research job should read "no research was written"; one
docstring in `src/research/environment_marker.py` holds `Lib\\site-packages` with a single backslash (a SyntaxWarning
on Python 3.15).

### 0.6 Working rules that hold now (each learned the hard way; the HISTORY part and section 8.8 tell the stories)

- **The file-form standard, exactly** (`doc/FILE_FORM_STANDARD_v0_2.md`; the reviewer's H14-C01). Frozen history keeps
  its recorded bytes: older files under `exchange/`, `doc/` and `review/` are not converted. The living files that
  existed before 25 November 2026 were converted under RAT-50 and follow the standard now. The standard's named
  exceptions keep their own rules (the six files of the retired Mode H release machinery, listed in
  `deploy/file_form.py`), and so does `GAIS/`; `.venv` and other third-party or generated material is outside its
  scope. **Every text file you add is CRLF; `.jsonl` and the cloud's `.sh` files are LF;** write them as bytes or
  with the line ending named; the cloud converts nothing. The decision log and `exchange/CONTINUITY_NOW.md` are LF
  and are appended to as bytes. **Compare today's identities exactly** (for files Git tracks with `-text`, at the
  same revision, Git's bytes, a clone's and the owner's disk are the same bytes); an older hash taken of LF bytes
  identifies those older bytes. This overrides every older instruction in this file about LF, `core.autocrlf` or
  tolerating CRLF working copies.
- Any low-level write of text is binary (`os.open` with `O_BINARY`, or `open(..., 'wb')`). Only a run on Windows
  shows Windows' own translation.
- **Never type a hash or a time:** compute the one from Git's bytes and read the other from the clock in the command
  that writes it. Look at `git diff --cached --numstat` before every commit.
- **Fetch immediately before taking an EX number, before committing and before installing a document;** the
  reviewer commits too. **Push nothing between the owner's pull and his push on a day of install.**
- When the owner relays a reviewer's result, fetch and read the EX file itself before acting.
- **Issue or revise an EX message only when the owner asks.** Discuss his queries with him first. A decision is put
  as question, why, recommendation, options; name things exactly. He may change his mind about timing: record each
  word as it comes (entries 314 and 315).
- **The cloud's evidence is not Windows'.** Say which it is every time.
- **Run the whole suite early, not only at the end:** it caught slice C breaking the project's own rule that the
  installed engine starts no program (entry 304); the code was corrected, not the rule.
- **A test's stand-in must do what the real thing does:** a stand-in for the start of a tree's Python imported the
  variants from the wrong folder and hid nothing only because the end-to-end run came after it.
- A comparison that lists a test as NEW does not say that it passes: read the suite's own lines.
- **Before a slice goes to review, walk every command that writes through each new guard** (EX_319 A-B02).
- Give the reviewer the exact differences of every reviewed file that moved, as well as the hashes.
- A workspace helper that edits files must be safe to run twice: each edit is made only when its old text is present
  (or its new text absent), and if neither is found it stops. **Compile every file a helper writes,** with warnings
  as errors: one helper lost its escape characters (entry 307's part).
- **Commit each part of a slice as soon as its tests pass,** with the working notes' "where it stands" brought up to
  date in the same commit, so that a stop loses at most the part in hand.
- For a one-off job, begin from the smallest thing that would do. A reviewer's recheck can over-engineer too: say so
  to the owner with the risk each demand guards against; the decision is his. When he says stop, stop.
- When he ratifies one document in advance, his word does not stretch to the next: ask.
- **If the reviewer chat ends without a handover of its own,** its next edition is built from its own last
  edition's bytes: live chapter only, its rights and inherited chapters untouched, the authorship stated (entries 282,
  283).

### 0.7 The cloud workspace, and what in this file is known to be out of date

**The workspace** is gone when a chat ends. To make it again: a clone of `main` to commit from; a second, disposable
clone to run tests in; Python 3.15 (the cloud had 3.15.0b4, installed with `uv`) with numpy, scipy and psutil.
`exchange/CLAUDE_WEB_TOOLS/step1/run_suite.py <tree> <report folder>` runs the whole suite (about fifteen minutes
now) and `compare_suite_reports.py <before> <after>` compares two runs test by test.
`exchange/CLAUDE_WEB_TOOLS/step3/sync_and_test.sh <clone> <python> [modules]` lays the overlay over a disposable clone
and runs modules with `PYTHONPATH=src:src/methods:tests`. The `mutation_check_*.py` scripts beside it plant one
fault at a time; their paths at the top are the workspace's and are set again. The helpers that copied LF working
copies into the overlay as CRLF lived only in the workspace: take the overlay's files as the truth.

**Known to be out of date below, and left as written:**

- **Appendix A:** nine of its hashes are older identities (0.1 step 1); its opening names them.
- **Section 7.1** gives the manifest on `main` as it was at build step 2; on `main` it is now 33 files in `[files]`
  (forecast 13, derived 17, other 3); the overlay's is in 0.5.
- **Sections 7.5, 10 and 12.8** were written for H-1 v9 to v12. Where they say what has run, what is next or what
  is open, this chapter is the present truth.
- **Section 0C item 1 and section 1.1** on the reviewer chats: 0.3 above is the present truth.

---

'''

APPENDIX_D = '''## Appendix D. What changed from H-1 v14 (the builder's own account)

**Written afresh:** the header and chapter 0. H-1 v14's chapter 0 is not carried (H-1 v14 stays in
`doc/HANDOVER/` as history).

**Carried byte for byte from H-1 v14** (the builder asserts each): sections 1, 2 and 2A; and the HISTORY part.

**Changed in place, each marked "(v15)":**

{made}

**Nothing else is changed.** Everything of H-1 v14 from section 0A to its Appendix C that is not named above is in
this edition byte for byte.

'''

BLURB = '''# Introductory blurb for H-1 v15: for a new Claude chat (paste everything below the line)

---

You are taking over as the Claude web chat, the PRIMARY DESIGNER AND CODER of the research project
hydra3333/analysing_perceived_randomness_in_reality (do Australian Powerball and Oz Lotto results hold patterns that
conventional statistics missed; the expected outcome is a carefully measured null). I am the project owner (GitHub
hydra3333; never write my personal name in anything committed). A separate ChatGPT chat is the independent reviewer.
I relay between you, and I alone ratify and authorise.

The previous Claude chat left you a handover, H-1 v15 (ratified by me as {rat}; SHA-256 {sha}). Its chapter 0 is the
whole live position. The project was redesigned from the root in November 2026; the new design was ratified on 22
November 2026 (RAT-40). Build step 1 (the method files' new layout), the light tidy-up and build step 2 (the research
engine, in DEV) are installed and proved. A standard for the form of every file is in force
(doc/FILE_FORM_STANDARD_v0_2.md). Build step 3 (the trees, installs, backups, restore and the new updater) has my go
for design and cloud coding only. Its slices A and B have passed independent review; slice C (creating a tree, the
installs, verifying a tree) is written and is with the reviewer; slice D (the updater) waits for my go. All of it
lies as working files under exchange/CLAUDE_WEB_TOOLS/step3/overlay/ and none of it is installed. There is no QA
and no PROD tree yet, and the old system's code is still in src/ beside the new engine.

DO THIS FIRST, and nothing else: add the repository (you will need push access for documents and records), then read
doc/HANDOVER/Claude_Primary_Handover_H1_v15.md and follow its chapter 0, section 0.1 (its reading order and the staged
takeover). Verify what you read against the repository; do not take summaries on trust.
THEN give me your first substantive reply: what you understand the project's state to be, what is and is not
authorised, what the next deliverable is, and anything you found unclear or inconsistent. Implement, design,
build and commit nothing yet. The ChatGPT reviewer will then ask you some blind questions, which I will relay,
and I will decide whether to accept your takeover (procedure HO-2).

HARD RULES, binding now (the handover has them in full):
- The one production results source is Lotterywest-GOV (www.lotterywest.wa.gov.au, HTTPS), reached only by my approved
  tools. You never contact any lottery website, and you never search for lottery results.
- You may read draw values, source_data/ and results/. You never write there. Anything you work out in the chat from
  draw values is labelled "suggestive"; results count only from the reviewed programs.
- Method-facing N-1 isolation is never weakened. Games are never pooled. The sealed Mode H records are never altered.
- No program ends another process. The orphan marker blocks all launches; nothing clears or bypasses it in place, and
  the one ratified exception is the restore's (deployment design section 12: a stale marker set aside as evidence
  when all four of its conditions hold). Three safety switches stay False and the allowlist stays empty.
- Nothing runs on my PC without my go. No install, run, backup, restore, migration or deletion without my separate
  approval. Nothing ever changes my PC's date, time or time zone. A STOP is a STOP.
- You commit and push documents and records yourself (named paths only; fetch and fast-forward first; nothing deleted
  or overwritten): under exchange/ and CLAUDE_CODE_WORKING_FOLDER_TREE/ freely, into doc/ only once reviewed and
  ratified. Code and tests never go into src/ or tests/ from you. You never write under transitory_data/ or GAIS/.
  Never edit the reviewer's files.
- A PASS or a ratified design authorises no install or run.

HOW I LIKE TO WORK: plain step-by-step English; decisions as question, why, recommendation, options; verify, don't
assert (compute hashes and counts with a tool); show your reasoning, alternatives and uncertainties; a short "how
the process went" note at milestones; end anything to be relayed with a short paste-ready block for the reviewer
chat. Do not over-engineer: the science, N-1, scoring and recoverability are the main game. On 24 November 2026 I had
to stop a simple job that had been over-built ("we have absolutely overengineered and wasted time and money"): tell
me the simplest safe route first. Discuss my queries with me first; issue or revise an EX message only when I ask.
Use the project's own words (restore from backup, catch-up, walk-forward, historical walk-forward rerun), and
explain any finding code in plain words with an example.

MODEL CHOICE: before designing a new subsystem, a statistical validity question, the root cause of an unexplained
STOP, or a cold read of a design, say "Suggest switching to Fable (High) for this" and wait for my go. Tell me when
a Fable task is finished. Everything else proceeds without asking.
'''
