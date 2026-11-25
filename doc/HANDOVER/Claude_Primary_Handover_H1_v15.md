# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v15

**Document:** H-1 under the agreed roles position v0.1r1, section 9 item 4.
**This edition: v15, 26 November 2026 (Adelaide, UTC+10:30). RATIFIED BY THE OWNER (RAT-60, decision log
entry 320).** The reviewer had not read it when it was installed; its cold read is owed when the owner asks.
**It is the next ordinary edition after the consolidated H-1 v14** (RAT-58). **Chapter 0 is written afresh and is the
only place that says what is true now:** slices A and B of build step 3 have passed review, slice C is written, the
reviewer has asked for corrections to it (EX_329, RECHECK) and they are with him for the focused recheck (EX_330),
nothing of build step 3 is installed. Sections 0A and 0C, sections 1 to 12 and the appendices are H-1 v14's, with the
corrections the reviewer's cold read of v14 asked for (H14-C01 to H14-C03 and its two observations) and the
closing of OUTLANDISH_01 made in place, each marked "(v15)"; Appendix D lists every one.
The HISTORY part at the end (sections 0B, 0D and 0E of H-1 v13) is carried as v14 carried it. **Sections 1, 2 and 2A
are byte for byte H-1 v14's and v13's** (the builder asserts it); **they are H-1 v7r1's text, the same as v7r1's
only after line endings are normalised** (v7r1 is LF; this file is CRLF; the reviewer's H14-C02). Built from the
installed H-1 v14's Git bytes (RAT-58; SHA-256 `24cc0579fec0f1b025216d969451457e378d1987eef96bf31f9a3bb924b5a6ac`) by `exchange/CLAUDE_WEB_TOOLS/h1v15/make_h1_v15.py`.
H-1 v14's own chapter 0 is not carried: H-1 v14 stays in `doc/HANDOVER/` as history.

**Audience:** any later Claude chat that takes over as primary designer and coder; the ChatGPT reviewer chat, which
checks it against the repository.
**Repository:** `hydra3333/analysing_perceived_randomness_in_reality`, public GitHub, branch `main`.
**Baseline described:** `main` at `23988644eade6d10dabfddd7f470fb5bbfb76205` (decision log entry 320; newest EX: EX_330).
**Authority:** the ratified documents and the decision log prevail over this handover wherever they differ.
`exchange/CONTINUITY_NOW.md` with the decision log carries whatever is newer. This file authorises nothing.
**Draw values:** none appear in this file.

---

## 0. THE LIVE POSITION (26 November 2026). Read this chapter first; it prevails over everything below it

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
     system on one page), the deployment design (the amendments of the two, RAT-56 and RAT-59, are in 0.3
     and 0.4 item 4), the coding practices, and the file-form standard `doc/FILE_FORM_STANDARD_v0_2.md`, which is short and
     governs every file you will write;
   - `exchange/DECISIONS/DECISION_LOG.md`, entries 121 to the latest (the owner's own words). A map: 147 is RAT-40
     (the new design); 158 to 169 build step 1 and the tidy-up; 176 to 212 build step 2; 217 to 243 build step 3's
     go and plan and the probe TASK_T028; 244 to 261 the file-form standard and the conversion of DEV; 262 to 269
     H-1 v12 and v13, H-2 v7 and v8, the register v0.33; **270 to the latest are the present Claude chat: its
     takeover; slice A and its review (271 to 281); the reviewer chat's end, H-2 v9 and H-1 v14 (282 to 286); the new
     reviewer chat (287); slice B and its review (288 to 300); slice C and its review (301 to 313, 317, 318); this
     edition (314 to 316). Read these in full;**
   - **build step 3's working record:** the build plan `exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md`;
     each slice's package note and corrections notes (`step3/slice_a/`, `step3/slice_b/`, `step3/slice_c/`) with the
     reviewer's replies (`EX_319`, `EX_321` for A; `EX_323`, `EX_325`, `EX_327` for B; `EX_329` for C); and the working notes kept
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
  `T:\a_p_r_i_r`, PROD `G:\a_p_r_i_r`, backups `T:\a_p_r_i_r_backups\QA` and `...\PROD`; the runner's scratch
  folder `D:\DELETE_ME\`. The owner keeps his own whole copies of the project folder on external drives.

### 0.3 The chats, the handovers and the ratifications

- **The present Claude chat** took over from H-1 v13 on 25 November 2026 (HO-2; entry 270) and wrote slices A to C
  of build step 3, H-2 v9 at the owner's request, H-1 v14 and this edition. It was compacted once in the evening of
  25 November and lost nothing (entry 303).
- **The reviewer chat that reviewed slice A ended at its maximum length** just after EX_321 (entry 282). **The
  present reviewer chat took over from H-2 v9** (entry 287) and reviewed slice B (EX_323, EX_325, EX_327: PASS) and
  made the cold read of H-1 v14 (`exchange/ChatGPT_to_Claude_H1_v14_Cold_Read_20261125.md`: PASS with the
  corrections H14-C01 to C03 and two observations, all made in this edition; Appendix D). **It reviewed slice C
  (EX_328) and replied with EX_329: RECHECK** (0.4 item 3).
- **The reviewer's handover in force: H-2 v9,** `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v9_20261125.md`
  (`8b7a61506a5275fcf2001f84fada77144560345e641bb8471096d45967983945`), with its blurb beside it (RAT-57; entries 282 and 283). **Claude wrote it,** at the owner's
  request, because the reviewer could not: its live chapter 0 only; the reviewer's rights and its chapters 1 to 19
  are H-2 v8's bytes. Expect the reviewer's own next edition to replace it.
- **Ratifications since the register v0.33** (RAT-53, `doc/RATIFICATION_REGISTER_v0_33.md`, the newest register):
  RAT-54 H-1 v13; RAT-55 the reviewer's H-2 v8; **RAT-56 (entry 280), the first amendment of the deployment
  design:** in its section 2, "(`deploy\`, standard library only)" is read as "(`deploy\`, standard library only,
  except the process rule of section 9, which uses psutil from the Python that runs the tool)"; the ratified v0.12
  file is not edited; restore stays standard library only. RAT-57 H-2 v9. RAT-58 H-1 v14 (entry 286). **RAT-59 (entry
  320), two more narrow amendments of the deployment design and the specification** (0.4 item 4; the ratified files
  are again not edited). **RAT-60 (entry 320), this edition.** The register's next ordinary edition carries RAT-54
  onward; it is owed, not urgent.
- **Numbers:** read the log's last line for the next EX, entry and RAT before using one; the reviewer takes EX
  numbers too. At this edition the newest EX is EX_330 (Claude's); the reviewer's reply is expected as EX_331.

### 0.4 What is authorised, what waits, and the order of work

**Authorised now:** build step 3's design and cloud coding only (the owner's go, entry 217; the plan
`exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md`, passed by the reviewer in EX_301; each slice also had
the owner's own go: A, entry 270; B, entry 288; C, entry 301). Records and working files under `exchange/`.
**Nothing on the owner's PC:** no install, no run, no tree, no runner task. Each of those is his separate go, and a
PASS or a ratification gives none.

**The order (the plan's slices; one install into DEV at the end, entry 219):**

1. **Slice A, foundations: PASS (EX_321).** Not installed.
2. **Slice B, backups, the recovery kit, restore: PASS (EX_327).** Not installed.
3. **Slice C, creating a tree, the installs, verifying a tree: WRITTEN; THE REVIEWER'S EX_329 IS A RECHECK; THE
   CORRECTIONS ARE WITH THE REVIEWER (EX_330).** Not installed. "The architecture and approach are sound"; no
   redesign. **Four blockers:** C-B01 (`Reinstall_Infra`:
   the owner's YES can rest on a stale statement if a job finishes during the question; the accepted plan and what
   the statement rested on are checked again under the second reservation, before anything is written; an ordinary
   install likewise must not act on a changed base); C-B02 (`Init_Tree`: the six results files are read as one
   set, and both copied pairs are checked with the results reader before the record; a continued creation with
   its record reads no source); C-B03 (the same command must finish a reinstall that removes a file); C-B04 (a
   replacement of an unfinished reinstall must not forget the regeneration of reports it owes). **Four
   corrections:** C-C01 (the read-only checks also make the job's results-only-grew check); C-C02 (an ordinary
   install's suite depends on byte equality with DEV, not on DEV's readiness marker); C-C03 (`Verify_Tree` repeats
   the unfinished-operation and orphan checks under its lock); C-C04 (the smoke case's kept table in CRLF; the
   suite line in both verdicts). **All eight are corrected in the overlay and proved in the cloud** (the owner's
   go, entry 318; done, entry 319): the suite of an install, 23 modules, 787 tests, passed; 29 planted faults for
   the corrections, none survived; the whole suite and the slice's 250 planted faults were not repeated, as the
   reviewer asked. The note for him is
   `exchange/CLAUDE_WEB_TOOLS/step3/slice_c/SLICE_C_CORRECTIONS_AFTER_EX_329_v0_1.md`, with the exact differences
   from `e404c22`, the hashes and the evidence beside it; section 4 of
   `exchange/CLAUDE_WEB_TOOLS/step3/SLICE_C_PLAN_AND_NOTES.md` says where the slice stands. **They went to
   the reviewer as EX_330 on the owner's word** (26 November 2026, entry 320), for the focused recheck; his reply
   is expected as EX_331.
4. **Two narrow amendments are ratified (RAT-59; the owner, 26 November 2026, entry 320),** in the wording of
   `exchange/DECISIONS/AMENDMENTS_PROPOSED_FOR_RAT59_v0_1.md`, with which the reviewer concurred (EX_329, section
   2): `Verify_Tree.bat` does not run the test suite (the owner's decision, entry 305; deployment design section
   7, specification sections 13 and 12.3 item 3); and at an
   infrastructure reinstall the job lock is let go for the kit, the backup and the question and taken again before
   anything is overwritten (reading C-R9; deployment design section 6, steps 2, 4, 6 and 11). **The ratified
   design and specification files are not edited, and neither is that document (its status line still reads
   "PROPOSED"): the amendments stand by the ratification, as RAT-56 does.**
5. **Slice D:** the clean-sheet updater `results_master_v0_3.py` (entries 180, 181): Lotterywest-GOV only; the old
   v0.2 stays unchanged in DEV; no Mode H preconditions carried over. **It needs the owner's go,** and it is a new
   subsystem: say "Suggest switching to Fable (High) for this" first.
6. **Slice E, the joined acceptance:** one rehearsal on Windows by the local runner in a scratch tree under
   `D:\DELETE_ME\` (the runner's rulebook v0.7, section 2A), where everything of slices A to D first meets Windows
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

**Waiting on the owner at this edition:** nothing. **Waiting on the reviewer:** EX_331, his focused recheck of the
corrections (EX_330). **Next for Claude:** whatever EX_331 asks; after slice C has passed, slice D on the owner's
go (item 5).

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
- **Reading C-R9, with which the reviewer concurs:** the design has `Reinstall_Infra` hold the job lock through
  its `PRE_INFRA` backup; slice B never backs up under a job lock; the lock is let go for the kit, the backup and
  the question and taken again before anything is overwritten (the second amendment of 0.4 item 4).
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
docstring in `src/research/environment_marker.py` holds `Lib\site-packages` with a single backslash (a SyntaxWarning
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

## 0A. Things that trip a new chat

1. **Two systems share this repository.** The code under `src/` is the OLD system (the proof-of-concept coordinator,
   the contract runner, Mode H, the walk-forward driver and report tool), **except that its method files are now in
   the new system's layout** (build step 1) and carry the coding practices' headers (the tidy-up). The old runner
   still computes them, through a table built from the folder tree. The ratified design's **research engine is installed
   beside it** (`src/research/`, build step 2); (v14) of its trees, installs and backups, slice A of build step 3 is written and reviewed but not installed (chapter 0, section 0.5); the rest of build step 3 and the laboratory tools are **not coded**. The older design documents (the Mode H design v0.1r7, the MHUP-B supplements and code
   plan, parts of E2R-1 and R3, the direction document's section 9) are history, except the clauses the
   specification's section 1.2 keeps by reference (section 4.2 below). Do not build from the MHUP-B plan and do not
   install the MHUP-B slices (section 7.3).
2. **The words DRAFT and CANDIDATE inside a ratified file are frozen wording.** A file's status paragraph and the
   decision log say what is ratified. The two design documents in `doc/` still carry DRAFT in their titles.
3. **Read the log for a number before using one.** (v14) Register v0.33 (RAT-53) is the newest edition; for anything later
   (RAT-54 onward) the decision log is the record. Read the log for the last RAT number, the last entry number and
   the last EX number before using a new one (chapter 0, section 0.3).
4. **Commit IDs changed on 6 November 2026.** A history clean-up renumbered the 27 commits of 5 and 6 November 2026.
   A record that cites one of them uses its OLD ID, and `git show <old id>` fails. Translate with
   `exchange/HISTORY_CLEANUP_2026_11_06/commit-map.txt`. Every file hash in every record is unchanged. Commits from
   `cf1c6d9` onward are unaffected.
5. **The cloud workspace is gone** when a chat ends, and a new clone may be shallow. Everything needed travels in the
   repository (sections 8.7 and 12).
6. **The reviewer commits its own files.** Fetch before reading or numbering anything, and never edit its files. Not
   every reviewer message is an EX file: three handbacks of 21 and 22 November 2026 are
   `exchange/ChatGPT_to_Claude_*.md`, and the decision log records each (entries 135, 136, 142).
7. **Use the project's words.** "Restore from backup", "catch-up", "walk-forward", "historical walk-forward rerun",
   "QA software replacement from PROD", "research-data reseeding from PROD". Never "reset" or "replay": the owner
   rejected them as foreign to the project (entry 136). A code such as "R5-F04" is always explained in plain words,
   with an example, when it is put to him.
8. **The OV-1 timing question is closed** (entry 142): the time a forecast was computed is not by itself a condition
   of the 2.5% bound; the claim stays conditional exactly as specification 10.6 words it; one engine in every tree;
   truthful counts of what was computed when. Do not reopen it and do not add a rule, mode or label for it.
9. **No more general design rounds.** The owner and the reviewer both want the effort to go to building and testing
   code (entries 142, 144, 146). A gap found while coding is settled in that step's package, in the leanest way that
   keeps the science right, or put to the owner as one plain question.
10. **Some tests read the method files as text.** They refuse words such as `open(`, `import math`, `float(`, `numpy`,
    `subprocess` or `contract_` in particular files, and two archive tests pin six E_1 modules byte for byte
    (`tests/test_code3_retirement.py`, `tests/test_e1r3_revision3.py`; the references are never refreshed). Even a
    comment can fail them: run the whole suite after any change to a method file (section 7.1).
11. **`.gitignore` holds `*.log`,** and `git add` skips an ignored file without a word. Name evidence files `.txt`, and
    build every hash table from the bytes Git holds (`git show :<path>`), never from the working copy (EX_276 C03).
12. **Some record files are CRLF and some are LF.** `exchange/OWNER_REMINDERS.md`, `exchange/OWNER_ROADMAP.md`,
    `exchange/CLAUDE_WEB_TOOLS/README.md` and the task files in `inbox/` are CRLF; the decision log, `CONTINUITY_NOW.md` and
    the runner's rulebook are LF. Edit a file's bytes and keep its endings, and **look at
    `git diff --cached --numstat` before every commit** (entry 193).
13. **Push nothing while the owner is in the middle of an install** (entry 210): his tree then holds uncommitted
    files and a commit of yours on GitHub costs him a pull he did not expect. Hold the records until his commit
    is pushed.
14. **The reviewer takes EX numbers too.** Fetch immediately before taking one, and never reuse one (entry 189).
15. **The old system kept a record for a target it could not forecast** (`INSUFFICIENT_HISTORY`); a new list simply
    begins later, at `first_target`. Anything that compares old records with new lists must count those apart
    (entries 205 to 208).

## 0C. Sections 1, 2 and 2A are carried unchanged: read them with these notes

They are H-1 v7r1's text ((v15) the reviewer's H14-C02: byte for byte H-1 v13's and v14's, and the same as
H-1 v7r1's only after line endings are normalised, v7r1 being LF and this file CRLF), because they hold the roles, the reviewer's rights, the review procedure,
the Git rules and the owner's working preferences, none of which the redesign changed. Their section references
are to this edition's sections of the same number ("section 0B, item 4" is item 4 above). Where they are out of date:

1. **Section 1.1, the reviewer chats.** The "present reviewer chat" it describes reached its limit on 21 November
   2026 (entry 128). The chat that took over that day ended on 23 November 2026 and is
   history. The chat that took over from H-2 v5r1 on 23 November 2026 (entry 175; 0B item 13) ended on 24 November after
   EX_303. **(v11) The present reviewer chat started on 24 November 2026 from Claude's refresh H-2 v6r2** (entries
   232 and 234; section 0D), with
   the same rights and independence. **(v14) That chat ended on 25 November 2026 at its maximum length, after EX_321
   (entry 282); the present one is started by the owner from H-2 v9 (chapter 0, section 0.3).**
2. **Section 1.1, the local runner.** The rulebook is now v0.7 (RAT-44, entry 192): it names the new system's
   commands as never run, except against a scratch tree under `D:\DELETE_ME\` when a task file says so (section
   8.6).
3. **Section 1.6 describes how code reaches the owner's clone and GitHub,** which is DEV. It still applies to every
   code package. How software then reaches QA or PROD is new and different: the commands of specification
   section 12, from local files, never by Git. Where 1.6 says Claude records the reviewer's files and the owner
   uploads zips, its own first bullet is the current practice: the reviewer commits its own. The rounds of November
   2026 used plain `.md` EX files with no zip (section 12.1).
4. **Section 1.6, the register and the protocol.** (v14) Register v0.33 is the newest (RAT-53); its next
   edition is owed for RAT-54 onward (chapter 0, section 0.3). `exchange/README.md` is now v0.6 (entry 155), where 1.6 says v0.5.
5. **Section 2, pushing.** The Mode H freeze it mentions ended on 16 November 2026. The rule not to push while the
   owner may have local commits waiting still applies.
6. **Section 2, the owner's two working lists** (`OWNER_ROADMAP.md`, `OWNER_REMINDERS.md`) were brought up to date on
   22 November 2026 (entry 155). Under P3 the roadmap's NOW block points to `CONTINUITY_NOW.md`. Two reminders await
   the owner's word (section 12.8).
7. **Sections 1.3 and 1.5 in the new system (Claude's reading, RECOMMENDED, not a new rule).** Judged by effect, HIGH
   and always-review work includes: the one reader and the permitted view (N-1); the writer of the forecast and score
   lists and its invariants (specification 5); scoring (8); the readout (ranking, ties, TOP and WORST); OV-1 and its
   kernel (10); the status file's writer and withdrawal (3.5, 11); the variant fingerprint and the forecasting-code
   identity (12.4); the derived check and the cutoff file (5.8); the install checks and smoke cases (12.3); the
   archive-then-shorten steps of a rerun (7A); anything that reads PROD (12.7, 14.2); the updater's launcher; the
   process rule and the orphan-marker check.

---

## 1. Roles and workflow (agreed position v0.1r1, ratified)

### 1.1 Who does what

- **Claude (you):** normally leads scientific and technical design, specifications, governing-document integration, primary code and its first tests. You prepare complete, hash-recorded packages; you never open pull requests, and you never change project files in the main tree. **Your commit rights (owner-authorised):** inside `exchange/` (every exchange file from both chats, byte-for-byte; section 1.6), and in and under `CLAUDE_CODE_WORKING_FOLDER_TREE/` (owner, 28 and 29 October 2026; section 8.6); and, since RAT-34, reviewed and ratified documents into `doc/` (section 1.6). Nothing else.
- **ChatGPT reviewer chat:** normally leads independent scientific and technical review. It may propose competing designs, methods and hypotheses, and may do bounded coding, alternative implementations or tests when the owner assigns them. Its handover is H-2. The reviewer chat that served until EX_075 reached its maximum length (30 October 2026); the owner started a new one from H-2 v1r7. That chat reviewed EX_077 to EX_152 (the snapshot, the direction document, the MHUP-1 design rounds and both MHUP-A slices) and **ended on 6 November 2026 without a handover** (R-022). The owner started the **next reviewer chat** on 6 November 2026 from H-2 v1r9 and its blurb (written by Claude from the records, with H-2's protected rights text byte-identical). It verified the rights region, found five documentation corrections and answered Claude's 19 blind questions (EX_153-EX_156; RAT-25), and has reviewed everything since: the handover deltas (EX_157-EX_162), the integrated MHUP-A package (EX_164 PASS), the post-install test fix (EX_165, EX_166), the Mode H readiness sheet (EX_167, EX_168 PASS), its own handover candidate H-2 v1r11 (EX_169, corrected as r1 in EX_170; never installed), and, at the owner's request for one full document, **H-2 v2** (EX_172), together with its documentary review of H-1 v2 (EX_172), and the owner's dependency change (EX_177: PASS WITH CORRECTIONS). **It reached its maximum length on 14 November 2026, about 18:00, after EX_177.** The owner started the **present reviewer chat** that evening from H-2 v2 r1's blurb with its placeholders filled (`exchange/HANDOVER_2026_11_14_REVIEWER/NEW_REVIEWER_START_PASTE.md`). It verified the rights region from Git's bytes, answered Claude's twelve blind questions 12 of 12 (EX_178 the questions, EX_179 its answers, EX_180 the key the owner had held sealed, with Claude's comparison) and was accepted by the owner; since then it has advised on D1-D7 (EX_181) and on the working approach (EX_183), and agreed or checked each run (EX_185, EX_187, EX_189). Some of its replies are pasted by the owner rather than uploaded; Claude records them as EX files (section 12.1). Treat it exactly as the old ones: same rights, same independence.
- **Claude Code local runner** (owner-decided 28 and 29 October 2026): Claude Code on the owner's Windows machine carries out task files Claude writes, in disposable task clones that cannot push, and reports what happened, under its rulebook `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (v0.5, RAT-30). It makes no design or code decisions. Its reports are owner-machine evidence, not reviewer evidence and not acceptance (section 8.6).
- **Project owner** (GitHub `hydra3333`): sole ratifier and execution authoriser, and sole committer of project files. Runs every Windows install and every data tool. **Never name the owner in anything that may be committed**; write "the project owner" or "hydra3333".
- Both models may challenge each other with evidence. Neither may override an owner-ratified decision. The owner may revise the allocation at any time. The ChatGPT coding chat and the earlier Claude reviewer chat are retired (27 and 26 October 2026).

### 1.2 Author and reviewer rules

1. Every consequential deliverable names its **author chat** and its **reviewer chat**.
2. The required independent review is always by the **other model**. A second Claude chat never counts as the independent review, however careful.
3. **Mixed authorship:** if the reviewer rewrites consequential parts of your patch, those parts come back to you for review, or become a separate package. Nobody approves its own mixed result.
4. **Work-item card** at the top of every handback: item ID; author and reviewer chats; base commit; input hashes; scope; risk tier; owner gate; evidence state.

### 1.3 Risk tiers and evidence (agreed position section 3)

- **HIGH, whatever the size:** normative or authority text in a governing document or the register; a protected block; a test golden or expected hash; a safety switch, gate constant or allowlist; reader, view or digest code; evaluator, scorer or tie code; dispatch, publication and consumption code; anything under `source_data/`.
- **LOW:** comments, and formatting in non-normative text (still hash-recorded).
- The tier decides who must check; the scope decides how much checking is needed.
- **Every handback carries:** the base commit; changed files with hashes; exact test commands and their outputs; environment versions; an explicit not-tested list; a holdout statement.
- **Evidence states are distinct:** IMPLEMENTED, TESTED, REVIEWED, ACCEPTED, COMMITTED. Never use one for another. Label evidence VERIFIED / OWNER-REPORTED / UNVERIFIED (TO-TEST for Windows-only behaviour), and say whose it is (author, reviewer, runner).

### 1.4 Findings, rights and disagreement

- Finding classes: **BLOCKER, CORRECTION, OPTIONAL, RECONSIDER**. RECONSIDER asks the owner to revisit a ratified decision; it never blocks by itself. Each finding cites file and line, the failure scenario and replacement text. A style preference is never a BLOCKER.
- **The reviewer's rights R-1..R-11** (agreed position section 5 and H-2): full bytes, never excerpts; independent reproduction of authorised offline tests (R-2); design-stage review before code for HIGH work, including a competing design (R-3); independent reference oracles where justified (R-4); findings outside the diff (R-5); RECONSIDER (R-6); access to your not-tested list (R-7); and R-8..R-11 (problem framing, evidence sufficiency, declining unsafe tests, material findings outside a narrow scope). R-8..R-11 are ratified (register; H2-TAKEOVER-O01): H-2's section 3 still calls them "proposed for owner ratification" only because its rights region is kept byte-identical; the register's ratification prevails. **Support these rights; never narrow them.** Supply everything the reviewer needs to reproduce your results.
- **Disagreement:** finding, author's reply, reviewer's response; if still open, it goes to the owner as claim, evidence, counterexample, consequence if wrong and recommended decision. Two rounds on unchanged evidence; a new counterexample opens a new finding. Never withhold evidence; never relitigate a settled point without new evidence.

### 1.5 Decision labels, oversight and the always-review list

- Report a choice as **DECIDED** only for an already ratified owner choice, or a purely mechanical implementation choice explicitly inside the approved scope; cite the authority. Label proposed consequential choices **RECOMMENDED**, and unresolved ones **OPEN**. Claude does not independently ratify a new scientific, safety, test or review policy.
- Claude may choose routine internal coding organisation, packaging details, version labels and presentation that neither alter the approved scope nor affect an acceptance or review gate. Deferring a ratified or required test, changing required evidence, waiving or reducing an independent review, changing a safety gate, accepting a consequential deviation, new rules or scope, anything that weakens safety, switch-on or destructive tests, ratifications, real-data gates and anything irreversible go to the owner, with independent reviewer input where required.
- **REVIEWER-DECIDED:** the reviewer settles routine review matters itself (owner, 27 October 2026; H-2 section 3.1). **Oversight (owner, 27 and 28 October 2026; indefinite):** Claude checks every REVIEWER-DECIDED item against the ratified compliance, safety and process rules and reports one to the owner **only by exception**: if Claude disagrees, or judges it of owner interest. This is reporting only; reviewer rights are unchanged. No departure has been found so far (through EX_172; up to EX_131 the latest REVIEWER-DECIDED items were the register v0.22 correction C01 (EX_099, FIX AND PROCEED), the optional WF1B-R2-O01 (EX_111) and WF1B-R2-O02 (EX_113), both deferred by the owner, and EX_131's FIX AND PROCEED for the MHUP-1 restore safeguard, inserted as worded in v0.1r5 and recorded in EX_132; the later reviews and their dispositions are in registers v0.25 to v0.28 and in `exchange/HO2_2026_11_10/`).
- **Always independently reviewed before consequential execution or acceptance** (owner, 23 October 2026): process termination (kill logic, ownership, the switch); N-1 boundaries and leakage; fit seeds and canonical forecast identity; TOP/WORST readout, ties and selection; holdout access and unsealing; FINAL freezing, persistence and publication; the synthetic/real firewall; dependency upgrades (W-23). The HIGH tier adds to this list; it never removes from it.
- **Review dispositions** (`review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`, owner-accepted 27 October 2026): **FIX AND PROCEED** lets Claude make exactly the authorised correction and continue; **RECHECK** (the default) sends it back. Only the reviewer assigns one; Claude never assigns, broadens or changes it; the owner may override. FIX AND PROCEED never applies to code concerning an always-review subject. Keep the exact diff, hashes, the authorised wording, test outputs and a not-tested list for every FIX AND PROCEED item. If the fix needs more than was authorised, it becomes RECHECK.

### 1.6 Git and transport

- **Since 16 and 17 November 2026 (section 0B, item 4; in force from RAT-34):** a document that has been reviewed and ratified is committed by Claude directly (named paths, after `git fetch` and a fast-forward, never over the owner's push) and checked from GitHub; the owner only pulls. The install instructions below remain for code packages. The reviewer commits its own EX replies to `exchange/` and its H-2 files to `doc/HANDOVER/`; fetch before reading or numbering anything, and never edit its files.
- **Code packages** (anything touching `src/`, `tests/`, a wrapper or an always-review subject): whole-file overlay plus a read-only verifier. The package has `repo_overlay/`, `VERIFY_*.py` with `pre` / `post` / `committed` phases, a suite runner that compares each module's test count with its expected count, the exact diff of every changed file, and `INSTALL_INSTRUCTIONS.md`. Replaced files are listed and checked against their base bytes; deletions are explicit. The install order is fixed: `git status --short` (clean) and `git pull --ff-only`; PRE; copy; POST; **the suite, before the commit**; stage; commit; COMMITTED; **push only after `COMMITTED PASS`**. Never an unconditional `git reset --hard HEAD~1`; on a STOP the owner stops and sends the output. While the owner installs, Claude pushes nothing. After the push, Claude verifies from a fresh GitHub clone (file list, every blob against the manifest, the suite).
- **Document-only installs** (owner, 28 October 2026; files only under `doc/` and `review/`): one zip mirroring the repository, short commands (`git pull --ff-only`, copy, `git add doc review`, `git status --short` showing only the expected files, commit, push), and one Claude check from GitHub after the push. Until the snapshot these had no verifier. **DOC-10 (the snapshot) and DOC-11 have one each** (`VERIFY_DOC10_INSTALL.py`, `VERIFY_DOC11_INSTALL.py`; pre/post/committed): DOC-10 because it changed files outside `doc/` and `review/` (`README.md`, `.gitattributes`, the Claude Code rulebook); DOC-11 because the owner wanted a checked handover installation (it adds only files under `doc/` and `review/`); a small document-only install may still use the short form. Content review is unchanged.
- **Review rounds** (owner, 29 October 2026): register text goes to the reviewer only together with a code package or the handovers, never in a round of its own.
- **Document installs since DOC-12** (6 to 13 November 2026): the owner copies the files from `exchange/` into `doc/` with the commands Claude gives (DOC-12 and DOC-13 with an install script, `exchange/DOC12/` and `exchange/DOC13/`; the H-1 deltas with `install_h1_*.py`; DOC-14 and register v0.28 with plain copy commands), commits and pushes, and Claude verifies the installed bytes from GitHub. The owner's checkout is CRLF, so give him `certutil -hashfile` values of the CRLF bytes when he checks a file before committing, and say which bytes each hash identifies.
- **Final packages after ratification** differ from the reviewed candidate only by the owner's finalisation (the register's status line, any filled placeholder, and the dependent manifest line and verifier hashes). They travel to `exchange/` in a for-the-record EX message that needs no reply (EX_046, EX_054, EX_057, EX_067, EX_076, EX_086, EX_102, EX_122, for a design EX_132, and for MHUP-A's frozen package EX_163, which the reviewer checked in EX_164), with the narrow diff, or, when the only difference is the verifier's base commit, in `CLAUDE_CODE_WORKING_FOLDER_TREE/packages/` named by a task file (WF-1A, register v0.22); the reviewer is not asked to re-review them.
- **Verifiers must tolerate CRLF working copies.** The owner's checkout uses `core.autocrlf=true` (Git warns "LF will be replaced by CRLF" when staging; harmless); Git stores LF. Compare working files after CRLF->LF normalisation and committed files with `git show HEAD:<path>`; use `git --no-optional-locks`. Test every verifier in an LF clone and a CRLF clone, with negative tests (a stray file, a modified guarded file, wrong bytes, an extra file, an extra committed file, a damaged package).
- **The exchange protocol** (`exchange/README.md` v0.5, 1 November 2026, which brought v0.4 (`63c19e7`) into line with this section). Each message between the two AI chats is one upload: `EX_NNN_<Sender>.md`, or a flat `EX_NNN_<Sender>.zip` whose EX message has a `Contents:` line (no zip inside a zip, except an install package carried as a member). One shared increasing `NNN`; never reuse a number. First line `# EX_NNN - <Sender> to <Recipient>`; headers `Date`, `Project`, `Replies to`, optional `Supersedes`, `Contents`, `Subject`; EX messages US-ASCII with CRLF and a member table with two hashes (as stored, and after CRLF->LF). An enclosed document derived from a UTF-8 project file keeps its encoding; its identity is its LF hash. **Claude records every EX file from both sides in `exchange/`, unchanged** (a zip also extracted to `exchange/EX_NNN_<Sender>/`), commits and pushes only there, and checks the pushed bytes. **The owner uploads the reviewer's zips to Claude and does not save them into the repository** (owner, 29 October 2026). Besides EX files, Claude keeps two owner working lists in `exchange/` (section 2); they are not EX messages and not rules. When an exchange review later goes into `review/`, store an **LF copy** and cite its LF hash.
- **Already-committed files:** if a file a package would add is already committed byte-identical, the verifier treats it as guarded, not new, and the builder asserts the identity first.

### 1.7 The working approach adopted on 14 November 2026 (P0-P6)

The owner's decision (`exchange/DECISIONS/DECISION_LOG.md`, entry 1), on the consensus of EX_182 (Claude's proposals), EX_183 (the reviewer's modifications) and EX_184 (Claude accepting every modification unchanged). It is working guidance: where it and the ratified documents differ, they govern; the reviewer's rights R-1 to R-11 and the eight mandatory RECHECK areas are unchanged; nothing about Mode H, its gates, D1-D7 or the freeze changes. The owner's aim: less administration and plain reporting, with ambitious science and the full independent review kept.

- **P0, continuity.** `exchange/CONTINUITY_NOW.md` is the one-page recovery index: the owner's NOW (what waits on him, the next possible go, blocks), the reviewer's status (open findings, evidence limits), how to restart either chat, the changes since the installed handovers, and Mode H's state. Claude updates it in place after every milestone (an owner decision, an EX message, a run report). It is not a handover and grants nothing; important reviewer findings and reasoning live in EX messages. At every stage judge whether to refresh the handovers (before the first Approval 1, after a big design round, or when either chat grows long or slow) and say so.
- **P1, who decides, judged by effect** (never by a file's location or a diff's size). **Level 1**, the owner decides after independent review: science and safety rules, anything under `src/`, dependencies, releases, real data, holdout, Mode H, installs, deleting data, ratifications. **Level 2**, reviewed for its actual side effects, still run only on the owner's own go (a reviewed tool or run sheet is never an advance approval): Claude Code task files (still checked by `check_task_commands.py`), owner run sheets, tools in `exchange/`. **Level 3**, Claude decides and records it, and the reviewer may look at any time: truly cosmetic wording and layout, routine author choices inside an already-reviewed design, the upkeep of the reminders, the roadmap and CONTINUITY_NOW. **Never level 3:** code semantics, scoring, tests and goldens, statistical conclusions, report labels, multiplicity and p-value wording, gate behaviour, required evidence, reviewed commands. A design review never replaces the code review before promotion.
- **P2, one decisions log.** `exchange/DECISIONS/DECISION_LOG.md`, living and append-only: date and time, the owner's exact words, where given, status and links; a correction is a new entry. The earlier decision files, the register and the installed documents keep their authority; the log is not a separate approval process.
- **P3, one NOW page.** The owner's NOW is the top of CONTINUITY_NOW.md (no second summary to drift); the roadmap's NOW block points there; the roadmap and reminders stay as archives.
- **P4, living drafts, fixed procedures.** Non-binding drafts (the roadmap, design drafts) are edited in place with dated change notes. A run sheet or tool used for a high-consequence action has an exact reviewed identity (a Git blob) fixed for that action; a substantive change means re-review and a new go; an executed procedure is never edited afterwards. Handovers, ratifications and registered contracts keep their editions and fingerprints.
- **P5, an ideas backlog, after Mode H.** Unusual or costly analyses, each with what it measures, its possible value, a rough cost and a priority; discussed before any run; negative findings kept (mark, never suppress); never displacing baseline work.
- **P6, a short process review at each substantial milestone.** Each AI's normal handback ends with a brief, independent "how the process went" note (what worked, what was friction, any suggested change, with the reasoning, the alternatives and the uncertainties), written before any joint recommendation; the owner adds his own; the outcome goes briefly into CONTINUITY_NOW.md; any change to a binding rule goes to the owner as a decision.

---

## 2. How the owner wants work presented (follow strictly)

- **Lead the owner through next steps.** Say what happens next and who does it, in plain step-by-step English. Label every paste block with its **destination chat**.
- End every response that needs relaying to the reviewer with a short **paste-ready block**; the owner likes these. Hashes in any block are computed by a tool and copied, never retyped.
- **Decisions:** plain-English question / why / recommendation / options, one at a time with a recommendation each (the question tool is fine for several independent ones).
- **Verify, don't assert.** Check claims against the files, line numbers, library source or official documentation.
- **Plain English**, not acronym-dense text; concentrate on substance. Explain alarming-looking tool output in one line (for example "create mode 100644" or the CRLF warning).
- **Files Claude produces:** US-ASCII where possible; CRLF for EX messages; LF for repository files; UTF-8 kept where the file derives from a ratified UTF-8 text; the version in the file name; no owner name. Check the encoding mechanically.
- **Superseded versions are kept**, not overwritten.
- **Proportion** (owner, 29 October 2026): the owner asked how much plumbing is really needed. Keep the safety-critical machinery (holdout and orphan protections, the release gate, independent review of HIGH work, hash-checked code installs) and keep everything else lean: combine rounds, keep documents short, and do not add machinery a method does not need. The owner's priority is **getting the project running**.
- **Package sizing (owner, 27 October 2026):** small packages for complex or HIGH work; a lead item that proves the pattern before a batch of similar items; heavy methods one at a time; ensembles last.
- **The owner's working lists** (owner, 30 October 2026), both in `exchange/`, both outside the rules:
  - `OWNER_ROADMAP.md`: the steps in plain English and where the project is up to. Update it at each milestone and show it to the owner then, and whenever asked;
  - `OWNER_REMINDERS.md`: things the owner asked to be reminded of, each with the date asked and its status (OPEN, DONE or DROPPED, never deleted). Raise each OPEN item when its "when" arrives, or when the owner asks.
- **Introductory blurbs** (owner, 30 October 2026): each handover has a starter text saved next to it, named `<handover file name>_introductory_blurb.md`, which the owner pastes to start the new chat. Keep it in step with its handover, and write your own handover and blurb first.
- **When the owner is away** and has said to carry on: work in chunks, each ending in something the reviewer can review; hold code whose design has not yet passed; and leave a short summary of what was done, what to send and what to decide. On 1 November 2026 the owner, going out, told Claude to make its best guess on anything needing his approval and report it afterwards; that applies to routine choices inside an approved scope, never to a gate, a rule or anything irreversible.
- **The owner is sometimes on a phone only,** with no command window and no VS Code. Then give only steps that need no PC (an upload to the reviewer, a decision), and queue the rest.
- **Pushing:** do not push while the owner may have local commits waiting (an install, a Claude Code report, report results), or his push is rejected and he must pull with a rebase, which on his `core.autocrlf=true` checkout can rewrite record files (section 12.6). It happened at MHUP-A's gate D (13 November 2026): Claude pushed between the owner's pull and his settings commit, his push was rejected, and `git pull --rebase` renumbered his commit (harmless that time; it touched no record file). During the Mode H freeze a rebase must not happen at all (section 5.4). The session's stop hook complains about unpushed commits; explain the hold in one line and push straight after the owner's push.
- **Helpers (other agents):** the owner approved them on 31 October 2026. They block the chat while they run and are killed if the owner posts, so the owner agreed to wait until Claude says it has finished. A helper's model can be chosen per call (for example Opus for a cold read while the chat runs on Fable).
- **Model choice (MC-1; owner, 2 November 2026, refined 3 November 2026; register v0.24):** before (a) designing a new subsystem or a major change to one, (b) a statistical design or validity question, (c) the root cause of an unexplained failure or STOP, or (d) a cold-read review of a design before it goes to the reviewer, say "Suggest switching to Fable (High) for this" and wait for the owner's "go". Everything else (packaging, task files, install steps, roadmap and reminder updates, explanations, paste blocks, records) goes ahead without asking. You cannot see which model is selected, and you cannot change it yourself (only the owner can, with `/model`), so flag and hold; split a mixed request at the boundary; when a Fable task is finished, say so, so the owner can switch back. **Refinement:** Fable is saved for the hard core (new HIGH design, the core of a HIGH code module, a BLOCKER-level finding, an unexplained STOP), because the owner's token allowance may otherwise run out before the end of a week; at each step say which model you recommend (Opus 5.5 or Fable 5.2, the models at this edition) with a one-line reason; cold-read helpers may run on Opus whatever the chat's model. Use the commit attribution line for the model the owner says is selected.
- **The owner's risk posture on chat length (3 November 2026):** this chat has already run out of room once (its context was summarised). Keep the handovers current at each milestone rather than at the end, and when the owner asks whether to continue or start a new chat, give a plain recommendation with the reason.
- **Full editions, not layers (owner, 14 November 2026):** the owner found the growing pile of handover deltas and overlays disconcerting and asked for fully updated documents. Prefer a full new edition of a handover (built by counted edits from the ratified bytes, with a list of what moved where) to another delta; a delta is for an emergency only, and is folded into the next full edition at once.
- **Proportion, restated (owner, 13 November 2026):** "keep the process proportionate and prioritise scientific correctness, functional reliability and the agreed safety protections"; add no administrative machinery that does not serve one of those.
- **Show the reasoning (owner, 14 November 2026):** explain not just the recommendation but why, with the reasonable alternatives and the uncertainties; the owner sometimes finds something important in them. At each substantial milestone, the short process note of P6 (section 1.7).
- **Chat length, restated (owner, 14 November 2026):** he once lost both AI chats at once in another project. At every stage judge whether to pause and refresh the handovers, and say so; `exchange/CONTINUITY_NOW.md` (P0) keeps the gap small. Today's reviewer takeover (EX_178-EX_180) showed that the installed handover plus that page is enough to restart a chat.

The owner restated the purpose on 30 October 2026, with the reviewer chat's six working principles (register v0.15). It restates these points and changes no rule.

### 2A. The owner's foundational points (26 Oct; binding)

1. The project is **deliberately and extremely speculative**. It looks for patterns that conventional statistics may have missed. No idea, method or measure is excluded because conventional statistics says it cannot work.
2. The owner **expects the most likely outcome to be that no method works**. A carefully measured null result is valid and useful.
3. **"Mark, never suppress":** every number the owner asks for is computed and shown; where it is not a calibrated probability, it carries a plain label saying so.
4. **Statistics tells kinds of pattern apart; it is never a gate.** The four origins: PO-1 a consequence of the method; PO-2 an effect of fitting; PO-3 chance, multiplicity or selection; PO-4 persistence on genuinely new draws. Strict N-1, the sealed holdout and the walk-forward / in-sample separation exist so that any surprise can be tested honestly.
5. **Openness with discipline:** any idea may be explored, but a claim needs a definable, testable form.
6. **Design test for any proposal:** does it make a number more honest without making any idea, method or measure ineligible? If it would act as a veto, flag it against this philosophy.
7. **Plain language in outputs:** terms such as "walk-forward" and "in-sample" are always printed with their exact project meaning.

### 2B. Added since v7r1 (owner, 21 and 22 November 2026)

- **Discuss first.** "Discuss my queries with me first; issue or revise an EX message only when I ask." He had EX_263
  revised twice in place under one number.
- **Plain words and examples.** The project's words only (section 0A item 7). An example with invented names helps
  him decide; the specification's examples (7.2, 7A.7) and the deployment design's section 14 were written for that.
- **The main game.** The science, N-1, scoring and recoverability come first. On 22 November 2026 he said the
  project had spent most of its time on matters outside the experiment (entry 142). Operational machinery is
  justified by a shown need or left out; a rare corner case gets the simplest safe behaviour: refuse and say why.
- **QA is his independent laboratory, never a gate** (entries 126, 135, 136). No install into PROD reads QA or asks
  about it. He may make QA a true mirror of PROD when he chooses; it must then give PROD's results.
- **Say what a thing costs.** "It costs nothing" about a backup attempt was wrong: it costs time and disk space.
- **Handovers at milestones, for both chats at once** (22 November 2026): he asks the reviewer to bring its own
  handover up to date when Claude writes this one.

---

## 3. Project in one paragraph

Two games, never pooled, one game at a time. **Powerball:** the current format since Draw 1144, 19 April 2018; 7
distinct main numbers from 1 to 35 plus 1 Powerball from 1 to 20. **Oz Lotto:** the current era since Draw 1474,
17 May 2022; 7 from 1 to 47 and no Powerball barrel; its supplementary numbers are used for prize divisions only,
never for forecasting (specification section 8). The project tests whether past draws hold any predictive
structure, with a catalogue of 62 method families (E_1 to E_62; R2 section 7). Twelve families have code today
(E_1 to E_4, E_6 to E_10, E_17 to E_19): 40 variants per game. Each variant ranks every number and gives a TOP seven
and a WORST seven for a draw, from earlier draws only. The first study, Mode H, is complete and sealed. **The system
ratified on 22 November 2026** has three separate folder trees (DEV, QA, PROD), each complete in itself; one research
job that fills every missing draw in order, scores it, saves a league report for every draw, keeps two OV-1 evidence
scores per game and forecasts the next draw; and every result as one appended line in a list. It is designed and
ratified; (v14) of it, the method files' layout (build step 1) and the research engine in DEV (build step 2) are installed, and build step 3 (the trees, the installs, the backups and the new updater) is being coded (chapter 0). It runs on Windows 11 with Python 3.15. The owner expects the most likely outcome
to be that no method works; a carefully measured null result is valid and useful (section 2A).

---

## 4. Governing documents

SHA-256 values are of the Git content, computed by the builder from `HEAD` when each was written. (v15, the reviewer's H14-C01: at this edition's baseline 11 of the 11 hashes in this section equal the file's bytes on `main` today. An older identity identifies the bytes it was taken of, at its commit; chapter 0, section 0.1 step 1.)

### 4.1 The authority for the active system (RAT-40)

| Document | SHA-256 |
|---|---|
| `doc/Predictive_Randomness_System_Specification_v0_6.md` | `ee7199d0c17e8bcf877d49e25c6db1a009105c3f8da75ff1ec28b15726216ad0` |
| `doc/Predictive_Randomness_Deployment_Design_v0_12.md` | `e9f778d86c0c1a8a73bfbebf21982aec897a3afdb1296c3029f2ba1da9b58b3d` |
| `doc/CODING_PRACTICES_v0_1.md` | `d64f0101a4fdb21998b2871765bd9b3f06ccb6c7409c7a2d0e9f230cebbd7ddd` |
| `doc/FILE_FORM_STANDARD_v0_2.md` (v12: RAT-49, 24 November 2026, entry 253: **the standard in force**) | `73d52529d52e743b16942ffada69df239d72cc019844f4c73476d6d38db1e680` |
| `doc/FILE_FORM_STANDARD_v0_1.md` (v11: RAT-47, 24 November 2026, entry 237; v12: history since RAT-49) | `97034474f1a7e9c54a14b9554b45666cb1fa031d566545433a0412d4312f8335` |

Each of the two design documents (the specification and the deployment design) is the candidate the reviewer
passed in EX_271 with its status paragraph alone changed. (v11) The file-form standard is the candidate v0.1r2
the reviewer passed in EX_305, ratified as RAT-47, with its status statements changed at installation (the
exact difference is in `exchange/CLAUDE_WEB_TOOLS/rat47/`). (v12) The standard v0.2 is the candidate v0.2r1 the
reviewer passed in EX_311, ratified as RAT-49 and installed the same way (`exchange/CLAUDE_WEB_TOOLS/standards/rat49/`);
RAT-50 (entry 258) changed its section 7 narrowly for the one conversion without re-issuing it. The
candidates and every earlier draft, with exact diffs between editions, are in `exchange/CLAUDE_WEB_TOOLS/simplify/`.

### 4.2 Still binding by reference (specification 1.2: science and safety)

| Document | SHA-256 | What stays binding |
|---|---|---|
| `doc/Predictive_Randomness_Experimental_Method_Specifications_R2_v0_5.md` | `2c67db8fcba50e469b0490cd85caf2fe964b3b79fc17fe7da4ebf033b91d9a3e` | sections 1 (invariants), 2 (data contract), 4 (observation policy), 7 (the 62 families) |
| each family's own ratified design (in `doc/`: E_6; E_3 and E_4; wave 1; wave 2; the E_1 documents) | see H-1 v7r1 section 4 | the family's rule and its variants' fixed settings |
| `doc/Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md` | `0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954` | section 7 only (the readout: ranking, ties, TOP and WORST), less its revision, run-mode and receipt fields |
| `doc/Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md` | `53e30a3e649b48b8a88923d08bf578caf04a4ce93d6ea6468891ca97e93a57b6` | sections 3 (measures), 4 (reference values) and 17 (league measures; the time axis is the draw number; games never pooled), less 17.3.6 |
| `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md` | `e3d977e16c910dfb0c3c37b440760f3d4c6ac4588c06af519aa0f9c9be97c27e` | sections 6.1, 6.3 and 6.5 only (OV-1's mathematics), as implemented by the kernel of section 7.3 |
| `doc/Predictive_Randomness_Software_Architecture_Discussion_v0_9.md` | `e0a03f41ddd561cf42b4d69367ab365d414c288f7943283fb47439f9c59df376` | section 5C (process safety; protected), amended by RAT-40 for the orphan-marker exception at a restore (deployment design 12) |

Also kept by the specification's 1.2: Lotterywest-GOV as the one results source through the one reviewed updater;
the process, orphan-marker and no-kill rules; the three safety switches (False) and the allowlist (empty); W-23.
**An exact clause list for E2R-1 section 7 is a first task of the code round** (specification section 20).

### 4.3 Neither named as binding nor as history by the specification

| Document | SHA-256 | Note |
|---|---|---|
| `doc/Predictive_Randomness_Research_Project_Proposal_v0_6.md` | `6a281e05127e7db976a16557ba69006327a8d615c2b0ec90bb6b34ee1c648a73` | the charter and philosophy; the source of section 2A |
| `doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` | `19809ae8a1aca716c6c6a4de71a37b705129304894a2b382036d51b76575b99f` | the catalogue E_1 to E_62 |
| `doc/contracts/TIE_SHA256_V1_Ratified_Encoding_v0_2.md` | `045b784d16a4611ac4ba5e8af063733e957b0b9359882d52b7143b912a65a0b6` | the tie and seed encoding that the readout of E2R-1 section 7 and the installed code use |

RAT-40 did not change them. Treat them as standing; if a clause of either seems to conflict with the specification,
say so and ask.

### 4.4 History, and the working documents

- **Historical for the active system (specification 1.3):** the Mode H design v0.1r7; the MHUP-B supplements v0.7 and
  v0.8 except the three sections above; the MHUP-B code plan v0.3; E2R-1 sections 5, 6, 8, 9, 12 and 12A; R3 sections
  6 and 10 and 17.3.6; the direction document v0.3r1 section 9; every draft of the MHUP-B deployment note. H-1 v7r1
  section 4 lists these files with their hashes.
- **Roles and review:** `doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md`
  (`7d572400b941ad423978a7542d6c32fb73c934f0057240dbc5138898112bd53b`);
  `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`
  (`5067aa520990b8ccc8521a04f3581424100cdd94994f5b9e3cb9e37863685339`).
- **(v14) In force now:** the reviewer's handover is H-2 v9, `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v9_20261125.md`
  (`8b7a61506a5275fcf2001f84fada77144560345e641bb8471096d45967983945`; RAT-57; chapter 0, section 0.3), and the newest
  register is v0.33 (RAT-53). What this section says below about which edition is in force is history.
- **The reviewer's handover (H-2).** **Previously in force (RAT-41), now history: H-2 v4, the reviewer's own full edition current to
  RAT-40, ratified by the owner on 22 November 2026:**
  `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md`
  (`8fa44f67fe37679c3039ae2c9676f86d2bc1269204a9e342f423e157d0612ba8` as ratified; first committed at `30826be`, that
  content at `70719f5`; its blurb's at `adfd973`). Its file name still says CANDIDATE: frozen wording. It replaces H-2
  v3r4 (RAT-36). With RAT-41 the owner asked the reviewer to check that its handover names the installed editions, so
  a later commit may refresh its references. Its section 0 states the current position, the
  four notes of ratification, the build order and the closed OV-1 question as this file does. Before it came the
  v3r10 continuity candidate of 21 November 2026, which Claude wrote on the owner's instruction when the previous
  reviewer chat was lost. **RAT-41 also covers the reviewer's refreshed H-2 v4** (entry 154: main `79406e4`, SHA-256
  `b2837f08f8fd89134aebfbbed5815ca28b00f0ccebd1cb54c92f2f13c50cea2b`; its blurb at `35a2ebf`): those were the bytes in force until RAT-43.
  **(v11: the installed reviewer handover is now H-2 v6, RAT-46, entry 216, `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124.md`; the present reviewer chat started from Claude's unratified refresh of it, H-2 v6r2: section 0D.) Before RAT-46 the one installed reviewer handover, in force since RAT-43 (entry 174), was H-2 v5r1,** `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5r1_20261123.md` and its blurb. It is the
  reviewer's own H-2 v5 (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5_CANDIDATE_20261123.md`, committed at `23689ef`
  and `31db13b`) with its status statements refreshed by Claude after the reviewer chat ended (entry 173); its rights
  text and historical chapters are the reviewer's bytes. H-2 v4 and v5 stay as history.
  `exchange/CONTINUITY_NOW.md` names the edition in force.
- **The register:** (v13) `doc/RATIFICATION_REGISTER_v0_33.md` (RAT-53, entry 265; documentary PASS in EX_316), which records RAT-41's install to RAT-52 and the five installs in DEV. Before it: `doc/RATIFICATION_REGISTER_v0_32.md`, ratified with H-1 v8 (RAT-41; documentary PASS in EX_273).
  It is register v0.31 (`c6369a72753ebda016f758e623df7a40bcb7a1300a49d503ccbb93be1b3cae6d`, RAT-34) with one added section
  that records RAT-34's install to RAT-40. A file cannot hold the hash of a file that holds its own, so register
  v0.32's hash is in decision log entry 153. For anything after RAT-41 the decision log is the record.
- **Protected blocks** (byte-identical through every consolidation): Architecture 5C; R2 section 7 and 4.1; R3 0.4,
  2.4 and 3; the proposal's E_1 to E_6. **Never edit a ratified file in place.**

---

## 5. Settled decisions - do not reopen without substantive cause

The three ratified documents hold the rules of the new system; the decision log holds the owner's words. This
section carries what a new chat most needs, and what is not in those three documents.

### 5.1 Data, the results source, and what the AI chats may do

The first five lines are H-1 v7r1's, unchanged.

- **Source: Lotterywest-GOV** (decision LW-1, owner, 4 November 2026): **Lotterywest-GOV means exclusively the official Western Australian Government Lotterywest website, using HTTPS and the exact hostname `www.lotterywest.wa.gov.au`. No other Lotterywest-branded website, hostname or third-party source is authorised for retrieving production draw results.** Where this project's earlier documents (the ratified design and the direction document among them) name "Lotterywest" as the results source, they mean Lotterywest-GOV; `oz.lotterywest.com` is a different Lotterywest-branded site and is never contacted. The updater reads Lotterywest-GOV's own results-search page with an honest, unmodified headless browser with >= 2 s pauses. **MHUP-C03 (owner, 3 November 2026):** Lotterywest-GOV's published results are official and trusted as they stand; no second-source check of a new draw in production. This single-source decision waives none of the updater's other checks: overlap with every draw already held, consecutive numbering, dates, the closed grammar, the ledger chain and provenance. **The updater v0.2 checks that the browser's final URL after page load uses HTTPS and has hostname exactly `www.lotterywest.wa.gov.au`; the path and query may identify the selected Lotterywest-GOV results-search page. No other origin, redirect destination, mirror, API or fallback is accepted. The browser can already have followed a redirect before this check, so the check is a refusal before parsing or writing, not proof that an untrusted host was never contacted** (design section 7, A6; EX_134 C01). **No API of any site; no browser impersonation; no bot-protection bypass; `oz.lotterywest.com` is never contacted; no new scraper by any AI.** The Lott is used only through pages the owner saves by hand outside the repository, as a private verifier; nothing derived from it is committed; **no automation of The Lott, ever**.
- **No lottery-results searches** by any project session, author, reviewer or runner. Accidental exposure is reported factually for the exposure record, never suppressed or asserted harmless.
- **Drawn order:** the published sequence is assumed operator order, label `OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`; never verified physical order; set and order views of the same rows are not independent samples.
- **Dates only** in masters. No pre-April-2018 draws, including Powerball-only analyses.
- **The two-site checker** (`src/two_site_results_check_v0_7.py`) drives The Lott's website automatically in its default `--sites both` mode. It was used only to build the first masters (late October 2026, when it also read Lotterywest-GOV's results-search page month by month). **It must never be run that way again** (decision TSC-1: it stays unchanged and is never used again; probe finding A5). (v14, EX_317 O01: the conversion of 25 November 2026 changed its form and two of its lines and gave no permission to run it; it is retired machinery and is not maintained.)
- **One master per game:** `source_data/<GAME>_results_master.csv` with its append-only ledger. `.gitattributes` has
  `source_data/** -text`; never change it. (v14: since the conversion `.gitattributes` holds the file-form standard's three lines instead, `* -text` first; that Git converts nothing now holds for every file.) In the new system only PROD runs the updater; QA and DEV receive a
  checked copy of PROD's accepted results (specification 7.1).
- **What the AI chats may read and write:** section 0B item 4.

### 5.2 The scientific contract

These lines are H-1 v7r1's, unchanged; they summarise R2 and E2R-1 section 7, which govern. The specification's
section 6 restates N-1 for the new system and adds its test.

- **Strict N-1:** target N sees only eligible draws with `draw_number < N`. **T-05:** change N and every later row; every method-visible field, array byte, schema, digest and capability must be identical, and the forecast byte-identical. Orchestration-side provenance may differ; provenance handed to a method must not.
- **The B1 rule:** the whole-master SHA-256 is derived from target-and-later rows. It is orchestration-only provenance and never reaches a method, directly or inside any method-facing object. The same holds for whole-file size and any other suffix-derived metadata.
- **Seeds and content identity** come from the permitted training-view digest, never the whole-file hash.
- **Views:** `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER`, `PAIRED_DIAGNOSTIC`; caller-declared; paired views never double-count. New schemas bind `game_id`, era and profile version (the legacy `E1_REAL_U_TRAINING_VIEW_V1` alone is exempt). Dates are opt-in with their own schema and digest.
- **Numerics:** `int64` integers and `float64` floats in the reader's table and every returned view; views are byte-backed, own their prefix-only copies, read-only, with no `.base` path to later rows. Python `int` for exact counts beyond int64.
- **Fresh fit for every target** on the eligible prefix; an incremental cache needs a reviewed byte-identical comparison with from-scratch fitting.
- **TOP and WORST from one frozen ranking;** joint-set TOP gets WORST only through `INVERSE_FROM_MARGINALS`, otherwise `INVERSE_UNAVAILABLE`, never fabricated.
- **Prediction-time ties:** `TIE_SHA256_V1` only. Post-draw rank position uses mid-ranks and never alters a frozen forecast.
- **Synthetic firewall:** synthetic data, states and scores never enter real fits, predictions or scores, and never exclude a method.
- **Games are never pooled. The time axis is the draw number, never a date** (R3 section 17).
- **One science in every tree** (owner, entry 136): no calculation, cohort rule, eligibility rule, check, warning or
  confirmation is written differently for QA or DEV (specification section 2).
- **League tables are descriptive reports. They select nothing and never feed a forecast** (specification section 9).
- **Not carried here:** v7r1's lines on status vocabularies and on the significance machinery of the first study
  (the N1 fair-draw replicates, the NIST seed policy, the programme-wide search log, the Bonferroni families). They
  describe the old report tool and Mode H. The new system's records and reports are the specification's sections 5,
  9 and 10; R3's fuller measures are "available as a further report ... on request" (specification section 9).
  Whether any of the old machinery is used again is not decided: ask, do not assume.

### 5.3 The owner's decisions of 19 to 22 November 2026 that shaped the new system

The specification's section 19 has the table with entry numbers. The ones a new chat is most likely to get wrong:

- **Families and variants only; no revisions.** A variant's scientific files never change once installed; a changed
  method is a new variant. Nothing is retired automatically (entry 122).
- **Withdrawal** is the owner's act alone, by one command and one confirmation, recorded in the variant's status file
  beside its software, and one-way (entries 130, 136, 137). No tool withdraws anything by itself.
- **QA is never a gate; one science in every tree; no sandbox mode** (entries 126, 136).
- **Installing is releasing** (specification 12.6): `Install.bat` adds every variant marked ready in DEV that the
  target lacks, checks it there and asks for one confirmation. No install or release records, and no Git, outside DEV. (v14, EX_317 H13-C03: read this as no release registry and no Git there; `records\INSTALLED_FILES.json` and `records\INSTALL_LOG.jsonl` are required in every installed tree, deployment design section 2.)
- **Shared code:** helpers are add-only (a changed helper is a new file with a new name) **except a genuine defect,**
  which the owner corrects in place by its own command; every variant the fault can affect is then held until its
  whole history is computed again (entries 127, 141, 143; specification 12.8). This is never a route for a changed
  idea.
- **Before a rerun replaces anything, the old lines are saved in one verified, clearly named ZIP;** if it cannot be
  made, nothing is changed (entry 142; specification 7A.4). The original forecasts keep their
  made-before-the-result character, in that archive.
- **The research job runs the reviewed updater itself in PROD** (entry 130; `--no-update` leaves it out). This
  replaced the decision of 4 November 2026 that kept the updater a separate operation.
- **The eligibility draw** (`prevailing_ov1_first_eligible_draw`) is the first draw not on file after a successful
  results step, for a variant whose history is complete (entries 130, 135; specification 10.2).
- **Backups** are complete copies of a whole tree. At an install a backup is attempted and reported truthfully; it
  is never a condition of the install; a failed backup is a warning and a confirmation that defaults to NO, never a
  stop (entries 135, 136; specification 14.1).
- **Restore** puts back exactly one backup and nothing else; the research then catches up (deployment design 12). No
  monthly restore test (entry 104). A recomputation after a restore is not compared with what was lost (entry 105).
- **The three laboratory operations** exist only on the owner's own command and none starts another: the QA software
  replacement from PROD; the research-data reseeding from PROD into QA or DEV; the historical walk-forward rerun, in
  any tree, PROD as a last resort (entries 128, 129, 135, 137). **Nothing run for QA or DEV ever writes a byte of
  PROD.**
- **The owner makes one full ZIP of the project folder on E: himself** before phase 1 moves any source file (entry
  131). No tool is built for it. **Done on 23 November 2026** (entry 163), before build step 1 was installed.
- **One design, built in four steps, each on its own go** (entry 143; specification 17.4; section 10).
- **Python 3.15 only** for tests (entry 103). **W-23 is unchanged** (section 5.4).
- **Closed:** the OV-1 timing question (section 0A item 8).

### 5.4 Engineering and process safety

The specification's section 13 cites "H-1 5.4" for the evidence a dependency upgrade needs. That is the first line
below. The five lines are H-1 v7r1's, unchanged; where the first mentions Mode H and "Approval 1" it is history, and
its rule stands: after every upgrade, stop until the evidence passes.

- **Dependencies:** `install_upgrade_dependencies_into_venv.bat` is the sole package list. **After every upgrade, stop** until the offline suites, numerical and N-1 tests, the W-suite including W-23 and all E_1 goldens pass; goldens are never recalibrated. No upgrade between freezing and scoring, or within Mode H. The venv is Python 3.15.2 (owner, 28 October 2026); the old 3.14.10 venv is kept as `venv.bak` as the fallback. `pyahocorasick` is an approved dependency (DEP-1, 6 November 2026). **The owner's dependency change of 14 November 2026** (`cc0ab73`; in its installation modes, its default included, the installer requests upgrades of pip and every listed package, and its `VERIFY` mode is read-only): TASK_T024 (ENV PASS, 90 distributions, 571 tests PASS) and the POC rerun of the same night were accepted by the owner as a **scoped W-23 acceptance for that change only** (decision log entry 5; never "W-23 PASS"; the timeout, Ctrl+C, memory-stress and other lifecycle cases not run, their risk accepted as not reliably quantifiable). Any further installer run before the first Approval 1 requires a renewed environment inventory and the applicable regression and compatibility evidence (T024 again), and an updated expected digest if the environment changed; the owner plans no more installs and will ask Claude first (OUTLANDISH_01 uses this venv too). The updater's offline self-test passed under 3.15 on 14 November 2026 (13/13).
- **Process termination (Architecture 5C, protected):** psutil only; no Job Objects; no `taskkill`, no kill by name, no fresh PID lookup. Ownership is proved by ancestry captured while the wrapper root is alive (PID plus creation time). **Strict no-status/no-kill.** When uncertain, leave the process and report `UNVERIFIED` / `ORPHAN_SUSPECTED`.
- **Orphan marker rule (owner, binding):** if anything is unconfirmed, the coordinator publishes the no-overwrite, fsynced `transitory_data/poc_runs/UNRESOLVED_ORPHAN.json`. **Any entry at that path blocks all launches for both games. Only the owner's approved manual clearance procedure clears it. No chat ever clears, bypasses or suggests bypassing it.** The contract runner and `read_run` read it from a fixed location; no caller can point them elsewhere.
- **Three switches stay False:** `ENABLE_PROCESS_TERMINATION`, `ENABLE_SCIENTIFIC_COORDINATION`, `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE`. The fourth, `ENABLE_CONTRACT_REAL_DEVELOPMENT`, is True since WF-1A (WF1-3, `0d98706`). No CLI override. Only the owner flips one, after reviewed tests. **MHUP-1 adds no switch:** the new real modes (`REAL_HOLDOUT`, `CATCH_UP`, `FINAL_NEXT_DRAW`) are governed by the owner's create-only records (the opening record, the developed record), the tickets and the binding gates (design 3.4, 5.1). The scientific result-consumer allowlist `_COORDINATED_SCIENCE_ALLOWLIST` is empty.
- **Testing order:** non-destructive tests first; destructive tests one at a time, each separately approved.
- **In the new system:** no program ends another process; the process rules are the table in the deployment design's
  section 9; the orphan-marker check stays in every tree although nothing installed outside DEV writes one; nothing
  ever changes the PC's date, time or zone (specification section 15).
- **History, true of the old code only:** v7r1 section 5.4's Option F launch interface, wrapper rules, coordinator
  concurrency, timing constants and the Mode H freeze. The old modules stay in DEV for the proof-of-concept suite
  and are not installed in QA or PROD (specification 17.3).

---

## 6. Verified technical facts (reuse rather than re-derive)

These lines are H-1 v7r1's, unchanged. Its section 6 also holds facts about the updater's internals and the Mode H
closure: true of the old code, not needed until that code is touched.

- The Windows venv `python.exe` is a redirector (CPython `PC/venvlauncher.c`): `Popen.pid` is not the interpreter's PID.
- Windows does not kill children when the parent dies; `TerminateProcess` is asynchronous.
- A `.bat` launched via `Popen` runs under `cmd.exe` with CMD argument parsing (gh-114539): hence `SAFE_ARG` and `%*`.
- `O_NOFOLLOW` does not exist on Windows; symlink refusal there relies on `is_symlink()`. NTFS hard links: the reader's `st_nlink != 1` refusal passes on the owner's drive. The owner's account cannot create symlinks (WinError 1314), so **four** symlink tests skip on Windows (reader contracts, exit receipt, CODE-2's dangling-symlink test, and WF-1B's symlinked-master test); the suite runner allows exactly those modules. A test that creates a symlink without catching `OSError` fails there (T013); hard links work and are the portable way to test the link guard.
- Line endings: (v12: superseded on 25 November 2026. Git now converts nothing in this project, `* -text`, and stores every file exactly as committed: the living project's text files CRLF, `.jsonl` LF, frozen history as it was. Section 0E items 2 and 7.) Before that: Git stores `.md` and `.py` as LF; `.bat` is `text eol=crlf`; `source_data/**` is `-text`. `git archive` applies the `.bat` rule, so hash `.bat` files from `git show`.
- **Python 3.15 makes UTF-8 the default text encoding (PEP 686).** No effect on the project's tests so far.
- **Record files and line endings:** Git stores `results/` files as text, so on the owner's `core.autocrlf=true` checkout any Git operation that rewrites one (a rebase, a checkout) gives it CRLF bytes, and a create-only record whose bytes are checked then refuses. The first Powerball report refused this way: both committed Powerball batch records (`plan.json` and the segment record) were `w/crlf` (`git ls-files --eol`), the plan 12,029 bytes against 12,028 in Git. The owner restored them (delete the files, then `git -c core.autocrlf=false checkout -- <batch folder>`), and the report then ran. Reminder R-011 adds a `results/** -text` rule.
- **Exact arithmetic can be slow at full size:** WF-1B's exact Clopper-Pearson bisection over 10,000-trial binomial tails took over an hour per report until PERF-1. Profile at full size on invented data before trusting a run-time estimate.
- **Byte-code caches:** with `PYTHONPYCACHEPREFIX` set, Python reads and writes cached byte-code only under that prefix, never in the `__pycache__/` folders beside the sources; `-B` (or `PYTHONDONTWRITEBYTECODE=1`) stops the writes; `-I` ignores both environment variables, so an isolated run needs `-B -X pycache_prefix=...` given directly. A sourceless `.pyc` outside `__pycache__/` is still importable. (Reproduced on CPython by the cold-read helper, 3 November 2026; design 4.1.)
- **Reference figures** (fair-draw model, context only, never a veto): Powerball main matches mean 1.4, SD 0.9604; P(>=4) = 0.01826; P(>=5) = 0.00121; Powerball 0.05 per draw. Oz Lotto main-match mean 49/47.
- **Run times measured on the owner's PC (23 November 2026):** the whole suite, one module per process, about 25
  minutes; the equivalence check of every old development target record about 40 minutes (Powerball about 31, Oz Lotto
  about 9; E_18 and the minimax fits take most of it). In the cloud workspace the suite took about 10 minutes and
  the scored-only equivalence check about 35.
- **New in H-1 v8: DEV's working files are the install source.** If Git rewrites line endings in the owner's
  clone, file hashes change, readiness markers stop matching and a helper may be refused. That fails safe; pinning
  line endings for `src/` in `.gitattributes` avoids it (specification section 20). The owner's checkout uses
  `core.autocrlf=true`. (v12: settled by the file-form standard: the root `.gitattributes` says `* -text`, so that
  setting no longer rewrites any file of the project; `GAIS/` keeps its own rules.)

---

## 7. What exists today

### 7.1 The installed code

- **The method files are in the new layout** (build step 1, `0aea10a`): `src/methods/E_0nn/` holds each family's
  `core_v1.py` (the shared calculation; E_6 also `beta_bernoulli.py`), `variants.py` (each variant's fixed settings)
  and one folder per variant with `method.py` (calls the core) and `VARIANT.json` (the scientific declaration of
  specification 3.4). Shared helpers are `src/methods/_shared/{recurrence_gaps_v1,occurrence_counts_v1,polynomial_fits_v1}.py`.
  The old contract runner's table of methods is built from the folder tree (`src/methods/_common/method_table.py`;
  `ADAPTERS = build_method_table()` in `Method_Contract_Runner.py`); `contract_adapters/` is gone, E_1's wrapper is
  `E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py`, and E_1's own modules stay where the proof-of-concept suite imports them.
- **The tidy-up** (`c7e6ed8`) gave 37 of those files the coding practices' headers and a comment on every function;
  no code changed. **Six E_1 modules are pinned byte for byte by two archive tests** (section 0A item 10) and were
  left as they are (entry 166).
- Twelve method families, 40 variants per game: E_1 (one variant), E_3 and E_4 (six each), and E_2, E_6, E_7, E_8,
  E_9, E_10, E_17, E_18, E_19 (three each).
- **The research engine of the new system** (build step 2, `5f16b35`): the package `src/research/`, 20 files when it was installed and (v14) 21 since the conversion added `windows_text.py`; the
  program `src/research_command.py` behind both launchers; `Run_Research.bat` and `Withdraw_Variant.bat` in the root;
  `deploy/INFRA_MANIFEST.ini` (the 32 infrastructure files in three classes: forecast 13, derived 16, other 3);
  `ENVIRONMENT.example.ini`; seven test modules `tests/test_research_*.py` with `tests/research_fixtures.py`. The
  install added 33 files and changed two (`.gitignore`, and one list in `tests/test_mhupa_master_versions.py`).
  **It imports the old system's shared files and does not change them.** What each module does, and the choices made
  in it, are in `exchange/CLAUDE_WEB_TOOLS/step2/STEP2_PACKAGE_NOTE_v0_3.md`; every file's own header says what it is
  for. In short: `variant_lists.py` (the two chained, append-only lists per variant per game), `code_identity.py` and
  `variant_folders.py` (the two header identities), `forecast_engine.py` and `reader.py` (one forecast from the N-1
  view), `scoring.py`, `game_state.py`, `research_job.py` (the job; fill and catch-up are one function,
  `complete_draw`), `derived_check.py` (the check of specification 5.8 and the marker `NOT_CURRENT_FROM.json`),
  `ov1_numeric.py` and `ov1_ledger.py`, `reports.py` (made again in memory at every job, written only when the bytes
  differ), `status_file.py`, `withdraw.py`, `settings.py`, `job_lock.py`, `results_step.py`.
- **A tree's settings are `ENVIRONMENT.ini`,** beside the launchers; Git ignores it. In DEV the owner made it by
  copying the example (entry 212). The launchers refuse without it, and refuse a Python that is not the tree's own
  `.venv`. **The example's comments mislead and its commented paths are out of date** (the owner's observation,
  entry 211): it is rewritten in build step 3.
- **Everything else** under `src/` and `tests/`, the root `.bat` files and `requirements.txt` is the old system, as at
  `cc0ab73`, apart from step 1's changes named above and the lines it changed in 14 test files for the moved paths.
- (v12) **The suite's known result since the conversion (owner's PC, 25 November 2026): 54 modules, 830 tests:**
  the 52 modules and 762 tests below, with the same three failing tests, and two new modules, `test_file_form`
  (52 tests) and `test_research_file_form` (16). On the night, one of the 68 new tests failed on Windows (the
  lock file's line); it passes since `fe1c310` (116 tests of the three affected modules run by the owner, `OK`).
  **The whole suite has not been run since that one-line commit:** the next package's run is the first.
- **The suite's known result** (owner's PC and cloud, 24 November 2026): **52 modules, 762 tests** (the old 45
  modules and 571 tests, and the engine's 7 modules and 191 tests); **three tests fail, with eight failed
  assertions**, on `main` since before step 1: `test_mhupa_launchers` `test_gitignore_lines` (one; it prints a set, in
  a different order each run) and in `test_multigame_reader_contracts` `test_master_source_and_ledger_file_hashes`
  (two sub-tests, pinned to the version-1 masters) and `test_only_legacy_e1_allowed_at_boundary` (five). On Windows
  the old symlink tests skip (section 6), and two of the engine's link tests skip where the account cannot make a
  symbolic link; its three folder-link tests then run with a junction. Compare before and after with
  `compare_suite_reports.py` (section 12.2), test by test. The two suite runs take about 25 and 29 minutes on the
  owner's PC.
- The three safety switches are False and the allowlist is empty in `src/`. A fourth, older switch,
  `ENABLE_CONTRACT_REAL_DEVELOPMENT`, is True in the old contract runner (owner, 31 October 2026).

### 7.2 Data and records

- **Masters, version 2:** Powerball draws 1144 to 1591 (448 rows),
  `e4f2feb8b18fc2dbe389583a189fa26127a648f4da940dd76219ee282170f3e0`; Oz Lotto draws 1474 to 1708 (235 rows),
  `63e3349333f8aa0485b7b067abe70249e39de81c6d02cda1a5710cf1041a4e9e`.
- **In Git:** the sealed Mode H records and reports (`c7622fa`); the development and Mode H score records (`cc665ce`);
  the earlier ranking reports; and the development batch records
  (`results/real/development/wf_batches/<GAME>/<batch>/plan.json` and `segment_*.json`), which list every published
  development target record: 17,280 Powerball and 8,760 Oz Lotto. Not all of them are forecasts (the last item of
  this section).
- **Not in Git:** the old run folders (26,040 development target records, three files each, and 800 Mode H) and
  attempts ledgers exist only on the owner's PC, in his backups and in his ZIP of entry 163. 5,838 Powerball and 2,802
  Oz Lotto development target records have no score, so they exist only there: 3,036 Powerball forecasts that were
  never scored, and 2,802 `INSUFFICIENT_HISTORY` records in each game (the last item of this section). The transition check of build step 3 reads them;
  **they stay until then** (entry 163; their cleanup is the owner's own act).
- **DEV's research results** (24 November 2026; ignored by Git, on the owner's PC only): `results\research\<GAME>\`
  with `variants\<family>\<variant>\forecasts.jsonl` and `scores.jsonl`, the reports under `reports\` (start with
  `README.txt`), and `records\`. Forty variants in each game. A list begins at its variant's `first_target` and holds
  no line before it (specification 5.2). **The prevailing OV-1 has not started in DEV** and cannot until a tree
  exists to copy accepted results from (build step 3); the job says so at its end. The cloud workspace's own fill
  gave the same counts; it is suggestive only and is gone with the workspace.
- **The old development records, counted exactly** (entries 205 to 208; EX_295). A "target record" is what the old
  system kept for one variant at one target; it is a forecast or an `INSUFFICIENT_HISTORY` record. **Powerball:** 17,280
  target records = 14,478 forecasts + 2,802 `INSUFFICIENT_HISTORY` records; the rank ledgers name 11,442 scored
  forecasts, so 3,036 forecasts were never scored, and 5,838 target records have no score. **Oz Lotto:** 8,760 =
  5,958 forecasts, all of them scored, + 2,802 `INSUFFICIENT_HISTORY` records. **In all:** 26,040 = 20,436 forecasts +
  5,604. Build step 2's comparison compared the content of the 20,436 forecasts with the new lists, and separately
  found each of the 5,604 below its variant's `first_target`, where a new list has no line: for those it compared no
  forecast content and no view digest, because the new system has none there.

### 7.3 Staged work that is not installed and will not be installed as built

- **The three MHUP-B slices** under `exchange/CLAUDE_WEB_TOOLS/mhupb/` (slice 1, EX_231 PASS; slice 2, EX_237 PASS;
  slice 3, EX_242 PASS) implement the weekly-session design that the course correction replaced. They are a source
  of reviewed code and tests to draw on, never a package to install.
- **The OV-1 kernel** is `exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/slice2_new/src/evaluation/ov1_numeric.py`
  (`2858075e37d2fed447388c770aafe2de9c6d296cd84808078f4cff8cba8d8234`), with its tests beside
  it. The specification's 1.2 names it as the implementation of OV-1's mathematics; the reviewer accepted its proofs
  P1 to P8 at source level (EX_233). Build step 2 carried it into the new system byte for byte at its installation, as `src/research/ov1_numeric.py` ((v14) since the conversion that file is the same kernel with CRLF line endings, equal to the reviewed one once CRLF is read as LF; the install manifest pinned its hash and no test of the suite compares the two, where earlier editions said that a test asserts the
  equality): do not rewrite it; any
  change to it is HIGH work.

### 7.4 The design's working record, and the build's

- `exchange/CLAUDE_WEB_TOOLS/simplify/`: every draft of the specification (v0.1 to v0.6) and of the deployment design
  (v0.7 to v0.12), the exact diff between each pair of editions, the builders, and
  `DRAFT_CONTRADICTIONS_FOR_REVIEWER_v0_1.md`. The specification's section 21 says where each finding and decision landed.
- `exchange/CLAUDE_WEB_TOOLS/step1/` and `tidy1/`: the two installed packages, their builders, tools, notes and
  evidence, including the owner's own outputs (`evidence/owner_pc_2026_11_23/` in each). Section 12.2.
- `exchange/CLAUDE_WEB_TOOLS/step2/`: build step 2. The engine's files as they went into the tree (`overlay/`), the
  builder and its tools, the four packages (`package/`, `package_v1r1/`, `package_v1r2/` are superseded; `package_v1r3/`
  is the one installed), the three notes, the build plans, and the evidence of each round (`evidence*/`). The
  owner's own install outputs of 24 November 2026 are in the decision log entries 209 to 212, in his words.
- `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_7/`: the three candidates of the runner's rulebook v0.7, their diffs and
  builders, and the two scripts that installed it. `t025/`, `t026/`, `t027/`: the three task files' builders.

### 7.5 What has run, and what has not been tested by anyone

**Has run on the owner's PC, from reviewed programs:** the research job in DEV, twice (a first fill and a job with
nothing new), and the engine's 191 tests; in a scratch tree, the same, and `Withdraw_Variant.bat --help`.

**Has not run anywhere but in the engine's own tests, on invented data:** a job with a new draw on file (a real
catch-up); the results step (DEV has no tree to copy from); the prevailing OV-1 ledger on real results; a
withdrawal; a crash and its resume on Windows (a planted interruption would mean ending a process, which the owner's
rules forbid; the tests cover it); a held variant; the marker `NOT_CURRENT_FROM.json`.

**Known limits of build step 2, recorded in its note (section 9):** until build step 4 no command clears a held
variant or a `MISMATCH` (in DEV the interim is to delete the untracked `results\research\` by hand, on the owner's
word, and fill again); a job that is killed leaves its lock file, which the owner deletes by hand after reading what
the launcher says; an interrupted withdrawal of several variants leaves the first withdrawn (run it again without
that one); the guard against linked working folders covers five named folders and one writer under the job lock,
no more (EX_290).

**Nothing of the trees, the installs, the backups, the restore or the laboratory tools has been coded or run.** The
specification's section 20 and the deployment design's section 17 list the uncertainties; the costs still to
measure are a `Check_Forecasts --all`, a historical walk-forward rerun, and a backup of a whole tree with its
environment. Measured so far, on the owner's PC: a first fill of both games 46 to 47 minutes (nearly all of it inside
the methods' exact-fraction fits, E_3, E_4 and E_18); a job with nothing new 3 minutes; the comparison with the old
records 2 minutes.

---

## 8. How to work as primary designer and coder

### 8.1 Workspace

- Work in disposable scratch trees in the cloud workspace, never on the owner's checkout. Build a tree with
  `git archive <base>` or a fresh clone, apply your changes, and run everything there.
- Unpack every received file into its own fresh directory; keep your scripts elsewhere; run Python that reads
  untrusted files with `-I`.
- The cloud workspace cannot reach lottery sites and must not try.

### 8.2 Design before code

The design is done and ratified. Each build step is a code package under it; none needs a new design round. Where
the specification leaves a choice to the code round (for example the exact clause list for E2R-1 section 7), make
the leanest choice that keeps the science right, record it in the package's note as RECOMMENDED, and let the
reviewer and the owner judge it with the code. A choice that would change a ratified rule goes to the owner first,
as one plain question. Plan the tests up front: the specification's section 18 lists what the code rounds must show.

### 8.3 Your own first tests

- **Mutation checks, within safe limits:** for each safety property, plant a defect in a disposable copy and show
  that a test fails. The coding practices require it: "each rule has a test with a planted fault". Never mutate
  installed files, a live switch, real masters or live process controls. A test that cannot fail is not evidence.
- For any statistical or exactness claim, build the smallest exhaustive toy that could break it and enumerate it
  exactly with `fractions.Fraction`.
- Never "refresh" an expected hash. A mismatch is investigated, not accommodated.
- Run the **whole** suite before sending, not only the new tests, on one Python 3.15 build (entry 103). The
  authoritative runs are on the owner's Python 3.15.2 under Windows.

### 8.4 The handback package

This paragraph is H-1 v7r1's, unchanged:

Include: the work-item card; base commit; `repo_overlay/` with a SHA-256 manifest; the exact diff of every changed file; test commands and full outputs; environment versions; mutation evidence; the DECIDED / RECOMMENDED / OPEN record; the not-tested list; a holdout statement; owner-run Windows instructions written as instructions, never as claims of execution; and a paste block or EX message for the reviewer. Derive every count in the instructions (tests, files, allowed skips) from the tools themselves, not by hand.

Add, from RAT-40: the line "coding practices met", or the exceptions with their reasons.

### 8.5 Document work

These lines are H-1 v7r1's, unchanged:

- Prepare a **new candidate edition** from the exact ratified Git blob with narrowly scoped, counted replacements (each old string asserted to occur exactly once), in a builder script that travels with the candidate, and submit the candidate and its diff for review. Finalising after ratification changes only the status line. Never overwrite the installed edition.
- **Handovers** may be restructured and shortened (as this edition is); when they are, list what was dropped and where it now lives, so the reviewer can confirm nothing binding was lost.
- **Copy agreed wording verbatim.** Check mechanically: every ID present; protected blocks byte-identical; inserted characters ASCII; LF and a single final newline.
- **In this chat's rounds** each new edition was built from the previous one by a small Python builder of counted
  replacements (whitespace-tolerant; every anchor asserted to occur exactly once), then proved by making a `diff -u`
  and applying it with `patch` to the old file and comparing the result with `cmp`. **Commit the builder beside the
  document** (section 8.8).

### 8.6 The Claude Code local runner

- **What it is:** Claude Code on the owner's Windows PC carries out task files that Claude writes and reports what
  happened. Its rulebook is `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`, **v0.7 (RAT-44, entry 192; its version line
  corrected in entry 195)**. Its reports are owner-machine evidence, not reviewer evidence and not acceptance.
- **Rulebook v0.7 adds section 2A, the scratch folder `D:\DELETE_ME\`** (reviewed in EX_286, EX_287 and EX_289), and
  changes nothing else of substance. Only when a task file says "section 2A": anything under `D:\DELETE_ME\` may be
  created, read, changed and deleted; real results may be copied in by reading and used there; the new system's
  commands may be run against a tree whose root lies there; a scratch tree's own `.venv` may be built with that
  tree's own two scripts. Nothing leaves the scratch folder but the report and the text a task file names to be
  copied into it. **Never, even there:** the results updater, any scraper, the old coordinator and its launchers, a
  push, the PC's clock, ending a process. The owner's real QA and PROD trees and their backups stay out of reach
  without exception (rule 11). Rule 10 has one exception, which a task file must state: the suite's known failing
  tests, named one by one. A scratch run is a rehearsal, never a result of the project.
- **The owner's `.claude/settings.json` is his file.** On 23 November 2026 he removed two deny lines from it, the ones
  that matched every `.bat` and the dependency script (entry 197), so that a scratch tree's launchers can be typed.
  Its other deny lines stand: every delete, every push, `pip`, the updater, the old launchers and more. So a task
  cannot delete: the owner deletes a scratch folder himself. Its `Read` lines for `results` and `source_data` bind
  the runner's own file tools under the repository; they did not stop a Python command that copies those folders.
- **How a task runs:** Claude writes `inbox/TASK_Tnnn.md` with every command in full, the expected line of each step,
  a clean-up step and a report step, and commits it. The owner pulls, starts a **new** Claude Code conversation
  (a running one keeps the rulebook it started with) and types `Do inbox\TASK_Tnnn.md`. The runner commits
  `outbox/REPORT_Tnnn.md`; the owner pushes; Claude reads the report from GitHub. A STOP is a STOP. To check that the
  runner has the right rulebook, the owner asks it which version and ratification number it works under and what
  its section 2A allows (entry 201).
- **The runner's shell is Git Bash inside VS Code, and it has the main `.venv` active** (`VIRTUAL_ENV` is set). The
  project's `create_venv.bat` and dependency script refuse then, as they are written to (TASK_T025's stop). **A
  tree's `.venv` is built by the owner from a plain CMD window.** A `.bat` started from Git Bash by its full path
  does run and returns its own exit code.
- **The three tasks of 23 and 24 November 2026** are the worked example (section 12.4): TASK_T025 (the install
  sheet's parts 1 to 4 in a task clone, then a scratch tree; stopped at the `.venv`), T026 (the launchers, the first
  fill and the comparison; stopped on the comparison tool's fault) and T027 (the corrected comparison; PASS). The
  reviewer cold-read T025 (EX_291 asked four corrections of its text; EX_292 PASS); the owner ran T026 and T027 on
  his own go without a further look. T001 to T024 are in H-1 v7r1 section 8.6.
- **The owner favours running heavy, repeatable things there** (test suites, rehearsals), because they cost few
  tokens. Let that guide what goes to the runner. Never ask the runner to judge: give the exact expected lines and
  numbers, and say that anything else is a STOP.

### 8.7 Rebuilding

The cloud workspace does not persist. Everything needed to rebuild a document or a package travels in `exchange/`:
its builder, its template or base, its diffs and its evidence. The base of a code package is a Git commit.

### 8.8 Lessons from Claude's own errors

**From build step 2 (23 and 24 November 2026):**

- **A path that cannot be run where you work is the path that fails.** Three faults of this step were in code written
  with care and never executed: a crash point between two writes (EX_283), a cleanup that deleted what it had not
  checked (EX_285), and a comparison against records that exist only on the owner's PC (TASK_T026). **Make the
  unrunnable runnable first:** build made-up records in the real form (`check_compare_tool.py` did, afterwards, and
  reproduced the owner's output number for number), and plant the interruption in a test.
- **A correction can carry a new fault.** Both EX_285's blocker and the stale folder in package v1r3's sheet came in
  with a correction. For every new `unlink`, `replace` or `truncate`, ask what it could reach if its assumptions were
  false; after renaming a package, search every text for the old name (the builder now refuses a sheet that names
  another package).
- **"This is not a STOP" is never written to save a round trip.** TASK_T025's first text did it twice and the
  reviewer caught both (EX_291). A refusal, an error or an unexpected number stops the task.
- **Require the exact numbers, not only PASS.** TASK_T027 required every count; a bare PASS would not have told a
  right explanation from a tool that now forgave too much. Take the numbers from a tool's output, never from memory.
- **Never type a hash; never type a time.** A hash is computed by the builder or the assembler. A decision log
  heading's time is read from the clock in the command that writes it (entries 192 to 194 carry estimated times,
  corrected in entry 195).
- **Look at the count of changed lines before every commit** (`git diff --cached --numstat`). A script once wrote
  three CRLF files back as LF and Git showed nearly every line changed (entry 193). Section 0A item 12.
- **Push nothing while the owner is in the middle of an install.** A record pushed then put GitHub one commit ahead
  of his uncommitted tree and cost him a pull and his trust in his local Git (entry 210). When he doubts his
  repository, give read-only checks with the exact expected output, not reassurance.
- **A sheet says what must exist before it starts, and its builder checks every path.** The install met a baseline
  folder that had been deleted and a command that named the old package (entries 209, 210).
- **Fetch immediately before taking an EX number.** The reviewer took EX_287 while a message of that number waited
  (entry 189).
- **State what a claim rests on.** The cause of TASK_T026's stop was called an inference, with its arithmetic, until
  the corrected tool had read the real records; the reviewer asked for exactly that (EX_294).

**From build step 1 and the tidy-up (22 and 23 November 2026):**

- **A check must say what it covered, not only that nothing differed.** The first equivalence checker could report a
  complete PASS without the never-scored forecasts or for one game (EX_276 C01). Take the list of what must be found
  from an independent record (here the tracked batch segments), require every item, and print `PARTIAL` with each
  reason otherwise. A cloud run that covers only part is called PARTIAL, never PASS.
- **A comparison tool must account for every item or fail closed.** The first suite comparison identified 563 of 571
  tests (EX_276 C02). Count against the tool's own summary and refuse when they differ.
- **`git add` skips ignored files silently** (EX_276 C03; section 0A item 11). Hash from Git's bytes; check every
  named file on `origin/main` after the push.
- **A sheet that says "any FAIL is a STOP" must also say which failures are expected** (EX_276 C04).
- **Make the change mechanical:** a builder from a clean clone, every new word in one file, counted replacements, and
  a direct proof (for the tidy-up, the code with comments and docstrings removed, compared by `ast.dump`). The reviewer
  then reads one file, and the owner's PC repeats the proof.
- **Check each citation against its document while writing.** Four wrong section references and a wrong error type
  were caught that way before any proof ran.
- **A sheet's extraction step must say "extract to `E:\TEMP`":** the ZIP holds its own top folder, and Windows'
  "Extract all" otherwise nests it one level deeper (entry 169).
- **Push nothing while the owner runs a sheet** that ends with his push: record the go first, then wait.

**From the redesign (20 to 22 November 2026):**

- **Ask what a thing is for before designing it.** Three times a mechanism went past the owner's intent and he
  corrected it: a restore that reinstalled later releases; QA as a gate between trees; a "sandbox" OV-1 for QA (QA
  must be able to be a true mirror of PROD). Put the operating question to him first, and offer the simplest version.
- **Where no decision exists and you choose a mechanism, put the leaner alternative beside it** (specification
  section 19). The reviewer's largest findings were in mechanisms Claude had chosen alone; twice the owner's own
  answer was simpler and better (correct in place, then recompute; status beside the software).
- **An ordinary YES must never be able to install code that changes forecasts** (EX_267 R6-F01). Anything that can
  change what a stored forecast would be has its own command, its own warning, and a persistent identity check.
- **A summary sentence must not contradict the detail under it.** Re-read the detail after writing the summary.
- **After every change of rule, search the whole document for the old wording.** Stale words survived more than one build.
- **Do not invent terms.** "Reset" and "replay" cost a round of confusion; so did unexplained finding codes.
- **Do not say a thing costs nothing, or that a property is lost, without checking.** A backup attempt costs time
  and space. Original forecasts keep their made-before-the-result character in the archive; only the replacements
  are retrospective.
- **Read the clock in the command that writes a record.** Typed times were wrong twice more in this chat.
- **Commit builders with their documents.** The builders of three editions sat only in the workspace until this
  edition; the exact diffs were committed, which saved the record.
- **A handover is a document; a chat switch is a separate decision.** Recommending a new chat a day after a
  takeover, without saying why, unsettled the owner. Give the reason and let him choose the moment.
- **Decisions run ahead of documents.** The owner was "slightly disconcerted" to find it at the takeover (entry 134).
  Record each decision at once and say plainly when a document is behind.

**General, carried from earlier editions (H-1 v7r1 section 8.8 has the full list of 76; read it once before a code
round):**

- Count before claiming; compute every hash, count and worked example with a tool and copy it.
- A claim the record repeats is still checked against the code. A rule you remember is still checked against it.
- A record's presence is not its validity: validate at the point of use. Test what binds one record to another.
- But do not harden a gate that should not exist: ask what a check protects today before strengthening it.
- State machines need every exit enumerated: a crash at each step, a resume, a second run of the same command.
- Every loop that waits for a condition needs a proved exit for every input.
- Never let a caller choose safety evidence: no parameter "for tests" that points a gate somewhere else.
- Prove create-only writing; do not assume a rename will not overwrite.
- Mutation survivors show weak tests. An equivalent mutant is listed with its reason, never silently dropped.
- An exact method can be correct and still unusably slow: profile at full size on invented data first.
- Precision bugs hide in conversions: test extreme values against an independent route.
- Never invent a label or status word that no ratified document defines.
- A probe is not the implementation.
- Tests must be Windows-safe; task commands must pass the runner's deny list; counts in instructions come from tools.
- Use absolute paths in scripts. Scan every script for non-ASCII. Never stop a job by a name pattern (section 12.5).
- The owner commits often outside the reviewed line: fetch and look at what changed before building on `main`.
- Do not push while the owner may have local commits waiting.
- A cold read by a fresh helper before a review round pays for itself.
- When the owner's wish and a rule conflict, say which rules have a safety reason and which do not, and let him decide.
- Do not read the owner's words in the way that is convenient; when a remark could mean two things, say both and ask.

---

## 9. Adding a new method (in the new system)

1. **The idea, in the owner's words.** Decide its identity: a family already in the catalogue (E_1 to E_62), or a new
   family (E_63 or later is OPEN and needs an owner decision and a catalogue amendment first).
2. **A short specification** (Claude drafts; the reviewer reviews; the owner ratifies): the exact rule, its views,
   its variants. **Fix every variant's settings before code.** Check it against section 2A: no number suppressed,
   no veto.
3. **Code in DEV:** a folder per variant with `method.py` and `VARIANT.json`; shared computation in the family folder
   or in `_shared/`, each helper versioned by its file name (specification 3.2 to 3.4; the twelve existing families
   are the worked example since build step 1, section 7.1); tests, among them the N-1
   test that changes and appends draws at and after the target; mutation checks; the coding practices. It reaches
   the owner's clone as a reviewed package (section 1.6).
4. **Ready, then installed:** `Make_Installable.bat` writes the readiness marker; `Install.bat PROD` (or `QA`) adds the
   variant, checks it in the target with a smoke case and asks for one confirmation (specification 4, 12.1 to 12.3).
5. **The next research job** fills its history draw by draw; after a successful results step with its history
   complete it gets its eligibility draw for the prevailing OV-1 (specification 7.1, 10.2).

A changed method is a new variant. `doc/METHOD_TEMPLATE/` (draft 5) describes the old process (`contract.py`,
`IN_DEVELOPMENT.txt`, registry entries, a release package): it is history until a new draft is written, which is
owed after build step 3 (section 12.8). (v15) OUTLANDISH_01 is closed (owner, 25 November 2026;
entry 295): completed, null under the matching criteria investigated, and not integrated into this project. It is
not a method family to be built here and is no longer in the backlog; its own runs are not evidence here.

---

## 10. Next work, in order (planned; the owner decides each step)

**(v14) Chapter 0, section 0.4, is the present order and prevails. What follows was written for H-1 v9 to v13 and is
kept for its detail of each step.**

1. **Done:** H-1 v8, H-2 v4 and register v0.32 ratified (RAT-41); rulebook v0.6 (RAT-42); the takeover of this chat
   (entry 157); **build step 1** (entry 164, `0aea10a`); **the light tidy-up** (entry 169, `c7e6ed8`); H-1 v9 and
   H-2 v5r1 (RAT-43, entry 174); the runner's rulebook v0.7 (RAT-44, entry 192); **build step 2** (entries 176 to
   212, `5f16b35`).
2. **Done: H-1 v10 ratified (RAT-45, entry 215)** after EX_295 and EX_296, and this edition, H-1 v11, ratified
   (RAT-48, entry 244) after EX_306 and EX_307; (v12) **the file-form standard v0.2 (RAT-49, entry 253), the
   conversion of DEV (RAT-50, entry 258; `691f58e`, entry 260), the lock line (`fe1c310`, entry 261) and H-1 v12
   (RAT-51, entry 262): section 0E.** The reviewer has written its own
   H-2 v6 as a CANDIDATE (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_CANDIDATE_20261124.md`; EX_296): (v11) the
   reviewer corrected it as the candidate H-2 v6r1
   (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6r1_CANDIDATE_20261124.md`; EX_297); the owner ratified that corrected
   candidate (RAT-46, entry 216) and the reviewer installed it as H-2 v6; section 0D has what followed.
3. **Build step 3: trees, installs, backups and restore** (specification 12.1 to 12.6, 13, 14.1), then the transition
   check and PROD's first job. **(v11) The owner gave his go for its design and cloud coding on 24 November 2026
   (entry 217). Its plan, the plan's review, his decisions and where the work stands are in section 0D; the
   conversion to the file-form standard comes before its first package** (v12: **the conversion is done; slice A,
   brought to the standard, is the next work: section 0E item 10**)**.** Every operation on his PC is still his
   own go. **Already decided by the owner** (section 0B item 10): the
   updater as a clean-sheet new edition, put to the reviewer before it is coded; (v11: not "LF pinned": the
   file-form standard, RAT-47); the places on G: and T:; no parallel runner. **To settle or carry in that package:** the rewrite
   of `ENVIRONMENT.example.ini` (entry 211); that `Init_Tree.bat` stops for the owner to build the tree's `.venv` from a
   plain CMD window; rehearsals by the runner in scratch trees under `D:\DELETE_ME\`, each tree with a rehearsal role;
   the measurements of section 7.5. The old run folders stay until the transition check (section 7.2). **After this
   step PROD exists and forecasts every week, and new methods can be added: the main game.**
4. **Build step 4: the laboratory tools** (specification 12.7, 14.2, 7A, 12.8, `Check_Forecasts`), with the test of
   EX_271 section 3. Until it is built, a fault found in shared code is not improvised around: the affected work is
   held, or the owner restores a backup (specification 17.4); build step 2's limits in section 7.5 apply.
5. **The operations manual, after build step 3** (the owner, entries 171 and 182): its skeleton is agreed with the
   reviewer first. It must say what is and is not overwritten (an install never overwrites; shared code is
   corrected in place only by `Correct_Shared_Code.bat`; a variant's own files never, a corrected method is a new
   variant name) and how the markers and flag files work (`I_AM_INSTALLABLE.json`, `ENVIRONMENT_VERIFIED.json`, the
   status file, the job lock, the install barrier, the not-current marker).
6. **Then, in the owner's order:** new methods and waves; the housekeeping of section 12.8. (v15: OUTLANDISH_01 is closed, entry 295.)

**The updater and Mode H (the watchpoint of H-1 v9, now decided).** The installed code still has checks from the
Mode H study that the ratified design does not make a gate: `src/methods/_common/contract_dispatch.py` and
`master_versions.py` consult the opening record `source_data/HOLDOUT_OPENED_<GAME>.json`, and the updater
`src/results_master_v0_2.py` refuses an update for a game that has none. The reviewer preferred a narrow correction
that removes only that precondition. **The owner chose a clean-sheet new edition** (entry 181; section 0B item 10).
Put it to the reviewer as the owner's decision, with the proof that every genuine check is kept. Fresh trees must
work with no Mode H opening or seal as a prerequisite; the obsolete record is not copied into a new tree to satisfy
old code; no genuine source or ledger check is removed.

**Models (MC-1; suggestions, the owner decides):** Opus for packaging, sheets, task files, records and handovers.
**Fable (High) for the state machines of step 3** (the install and its barrier, the backup, the restore), for the
rerun and correction steps of step 4, and for any unexplained STOP. Cold reads before a review round may be helpers
on Opus. The owner switches models himself; say when a Fable task is finished.

**Genuinely OPEN** (do not present as decided): (v15: OUTLANDISH_01 is closed, entry 295, and its methods are no longer open); each
remaining catalogue family's formula; E_63 and later identities; whether any of the first study's significance
machinery is used again (section 5.2); the old system's undecided items, which H-1 v7r1 section 10 lists and which
may never be needed.

---

## 11. Gates that stay closed

This handover authorises nothing. Neither does RAT-40, any ratified design, or any review PASS. **Closed until the
owner's own go, each separately:** each of the four build steps; every install into his clone; the creation of QA
and PROD; every run of any program on his PC, whether a test task, the equivalence check, the transition check, a
research job, a rerun, a backup or a restore; every results update; every dependency change; every Claude Code
task. **Never, by any chat:** contact with a lottery website or a search for lottery results; a write under
`source_data/`, `results/`, `transitory_data/` or `GAIS/`; code or tests committed into `src/` or `tests/`; a change to the
PC's date, time or time zone; ending a project process; clearing or bypassing the orphan marker in place ((v15) the reviewer's H14-C03: the one ratified exception is the restore's, deployment design section 12, with all four of its conditions; it sets the marker aside as evidence; chapter 0, section 0.1); flipping a safety
switch or adding an allowlist entry; altering, rerunning or rescoring the sealed Mode H records; editing the
reviewer's files; pooling the games; weakening method-facing N-1 isolation. No Windows lifecycle or destructive test
runs without its own separately approved gate. A STOP is a STOP: nothing is retried, reset or worked around.

---

## 12. Working knowledge

This section describes practice, not rules. Section 12.3 is the practice of build step 1, the tidy-up and build
step 2, all installed; section 12.4 is the practice of the three runner tasks of 23 and 24 November 2026.

### 12.1 The work cycle, and the exchange protocol in practice

1. **Scope.** The owner names the work and gives the go. Write the work-item card (section 1.2).
2. **Build** in the cloud workspace; run the whole suite, the mutation checks and any rehearsal.
3. **Send** an EX message to the reviewer, when the owner asks for it. The reviewer replies PASS or RECHECK with
   findings. Fix, resend for a focused recheck, repeat.
4. **Windows:** a Claude Code task file, or the owner's own run, on his go; read the whole report.
5. **Owner acceptance and install** into his clone (section 1.6); verify from GitHub afterwards.
6. **Record:** the decision log, `CONTINUITY_NOW.md`, and the next register edition.

- **EX files:** `exchange/EX_NNN_<Sender>.md`; one shared increasing number; check the highest committed number, and
  fetch first, since the reviewer commits its own. US-ASCII with CRLF. First line `# EX_NNN - <Sender> to <Recipient>`;
  then `Date`, `Project`, `Replies to`, `Contents`, `Subject`. Open with the disposition of every finding answered. Say
  which reply number the reviewer should use. End with a member table (file, SHA-256) and a short "how the process
  went" note (P6). The documents themselves stay at their repository paths and are named by path and hash; no zip
  is needed unless a code package travels. **With a code package** (EX_275, EX_277, EX_279): the message is
  `exchange/EX_NNN_Claude/EX_NNN_Claude.md` beside the package ZIP and its member list, the package also extracted
  there, and all three in `exchange/EX_NNN_Claude.zip`; an `assemble_exNNN.py` in the package's tool folder builds
  both hash tables from Git's staged bytes.
- **For the owner:** end the chat reply with a short paste-ready block for the reviewer chat.
- **The decision log** (`exchange/DECISIONS/DECISION_LOG.md`): append-only, US-ASCII, LF; each entry numbered, dated
  and timed from the clock (`TZ=Australia/Adelaide date`), with the owner's exact words and what follows from them.
- **Committing:** `git fetch origin main` and a fast-forward merge first; `git add` with named paths, never `-A`;
  commit; push to `main`; then check the pushed bytes by hash from `origin/main`. Use the commit attribution line for
  the model the session names.
- **Repository access:** a Claude Code cloud session with the repository attached through the GitHub app, with push
  access. If a session has no write access, do not work around it: give the owner the files with the exact
  commands, and verify from GitHub after his push.

### 12.2 The tools (`exchange/CLAUDE_WEB_TOOLS/`)

`README.md` there is authoritative on names and use. Still useful for the build: the package builders and the
verifier and suite templates (how a code package for the owner's clone is made and checked: `pre`, `post`,
`committed`); the mutation tools; `check_task_commands.py`; `exchange/EX_019_Claude/make_zip.py` (a deterministic zip).
New since v7r1: `simplify/` (section 7.4), `h1v8/` and `h1v9/` (the handover builders), `register/`, `rulebook_v0_6/`,
and the two installed packages' folders:
- **`step1/`** (build step 1): `make_step1_layout.py` (the layout change from a clean clone), `build_step1_pkg.py`,
  `templates/` (the folder-built method table and the variant `method.py`), and three reusable tools:
  `run_suite.py` (`python run_suite.py <tree> <report folder>`: one `python -B -m unittest -v <module>` per process,
  one report per module and `MODULES.txt`), `compare_suite_reports.py` (`<before> <after>`: identifies every test,
  compares each test's result and each module's counts, fails closed; its last line says whether anything changed),
  and `check_layout_equivalence.py` (`--tree <root> [--game] [--part K/N] [--sample N]`: computes every old development
  forecast again in memory through the runner's own functions and compares `canonical_content_digest`; coverage is
  required against the tracked batch segments; `RESULT: PASS - COMPLETE` only for both games with `MISSING: 0`).
- **`tidy1/`** (the tidy-up): `tidy_texts.py` (every new word), `make_tidy_up.py`, `build_tidy_pkg.py`, and
  `check_comments_only.py` (compares every Python file under `src` and `tests` with a commit, with comments and
  docstrings removed; reusable for any comments-only change).
- **`step2/`** (build step 2): `build_step2_pkg.py <repo> <base> <out> <engine tests>` (the package from a clean clone
  at the base commit and `overlay/`; it writes the verifier, the manifest and the sheet, and refuses a sheet that
  names another package), `apply_edits.py` (the two counted edits to existing files), `sync_and_test.sh`,
  `mutation_check.py` (36 planted faults), `scan_practices.py`, `rehearse_install.sh` (an LF and a CRLF clone, seven
  cases that must STOP), `compare_fill_with_old_records.py` (a first fill against the old score records and the old
  run folders; `PASS - COMPLETE` only for both games with the run folders present), `check_compare_tool.py` (that
  tool on made-up old records, with planted differences), and the assemblers `assemble_ex*.py` (an EX message with
  every hash computed).
- **`rulebook_v0_7/`**, **`t025/`, `t026/`, `t027/`** and **`h1v10/`**: the rulebook's builders, the task files' builders
  (section 12.4) and this edition's.
The workspace paths inside older scripts are a previous chat's; change them at the top before use.

### 12.3 Building, proving and installing a code package (as done for build step 1 and the tidy-up)

- **Base tree:** a fresh clone at the base commit. **Dev tree:** a second clone, changed by the package's builder.
  Never the owner's checkout.
- **The Python 3.15 environment** does not exist in a new workspace: `uv python install 3.15`, `uv venv --python 3.15
  <dir>`, then `uv pip install numpy scipy psutil pandas pyahocorasick selenium beautifulsoup4 requests html5lib`
  (the direct packages of `install_upgrade_dependencies_into_venv.bat`; a bare interpreter fails modules on `numpy` and
  `psutil`).
- **The suite:** `run_suite.py` on the base tree and on the dev tree (two background runs at once are fine), then
  `compare_suite_reports.py`; the result needed is "no module and no test changed". E2R-T12 starts ordinary worker
  processes; the owner allows it in Claude's cloud runs (entry 159).
- **Science-preserving changes:** the equivalence check on the dev tree. In the cloud it can only be `PARTIAL` (the
  never-scored forecasts are only on the owner's PC); `--part 1/2` and `--part 2/2` in parallel save time.
- **Planted faults:** for every check the package relies on, plant a fault in a disposable copy and show the check
  STOPs.
- **The package:** `repo_overlay/`, `DELETE_PATHS.txt` if anything is deleted, the read-only verifier made from
  `exchange/CLAUDE_WEB_TOOLS/wf1/verifier_template.py` (phases `pre`, `post`, `committed`; guarded files), the tools
  the sheet uses, the manifest, and `INSTALL_AND_RUN_SHEET.md` (CRLF) with every count derived from the files. Rehearse
  the install in an LF clone and a `core.autocrlf=true` clone, with planted cases that must STOP.
- **The owner's sheet:** part 1 the baseline suite; part 2 PRE, copy (and `git rm`), POST and any direct proof; part
  3 the suite again and the comparison; part 4 the equivalence check (`PASS - COMPLETE` only); part 5 `git add`,
  commit, COMMITTED, and push only after `COMMITTED PASS`. A paragraph says which baseline failures are expected.
  The owner sends each part's output as he goes; check each before he continues; file the outputs unedited as
  evidence; verify the pushed commit from GitHub against the manifest and the tested tree.
- **Coding practices:** every package says "coding practices met" or lists the exceptions with their reasons.
- **What build step 2 added to this practice:** a code-bearing package goes to the reviewer as an EX ZIP made by an
  assembler (the message, the package ZIP unchanged, its member list), with the package also extracted in the
  `exchange/EX_nnn_Claude/` folder; a corrected package is a new name (`v1r1`, `v1r2`, `v1r3`) with the exact diff
  from the one reviewed and a table of the files that differ; **a rehearsal on Windows by the runner comes before
  the owner's install** (section 8.6); the sheet's baseline is made in the same sitting or its folder is checked
  to exist; and **nothing is pushed while the owner installs** (section 0A item 13). The cloud workspace of this
  chat kept a filled copy of the tree, which let made-up records in the real form be built (section 8.8).

### 12.4 Claude Code task files

As practised for TASK_T025 to T027 (`inbox/`, with their builders in `exchange/CLAUDE_WEB_TOOLS/t025/`, `t026/`, `t027/`):

- **Build the task file from a template** in which each long path is defined once; write it with CRLF, as the
  other task files are. Check before committing: every Python one-liner compiles; the steps are numbered in order;
  no command holds a word the owner's settings deny (for example `results_master`, `pip`, `conda`, `rmtree`); every
  D: path lies under `D:\DELETE_ME\`. `exchange/CLAUDE_WEB_TOOLS/check_task_commands.py` is the older check.
- **Each step gives the exact command, the exact expected lines and numbers, and what is a STOP.** A long step
  writes its output and its own exit code into a file (`...; echo "EXIT CODE $?" >> file`) and runs in the background;
  the task then shows named parts of the file. Say what the runner may add to a task line (`cd`, an `echo` of the
  exit code, `date +%H:%M:%S` in Git Bash) and nothing else. `grep -c` exits 1 when its count is 0: say so.
- **A section 2A task** names its folder, checks first that `D:\DELETE_ME` is an ordinary folder, never deletes, and
  says which text may be copied into the report. Lines that may show numbers drawn are counted, never copied.
- **A task that follows another** takes its commands from the earlier, reviewed task by its builder, which asserts
  that they are the same, character for character (T026).
- Read the whole report: every step's command, exit code and output, and its Deviations and Observations.

### 12.5 Traps in the cloud workspace

The first line is H-1 v7r1's, unchanged:

- **Stopping your own test jobs in the cloud workspace, and nothing else (EX_117 C02).** This applies only to expendable, non-scientific test processes that Claude itself started in its own cloud workspace for this chat (a test suite, a rehearsal, a mutation run, a profile). Never stop them by a name pattern: `pkill -f unittest` matched the chat's own shell twice and killed it. Find the job you started (`ps -eo pid,ppid,etime,cmd`), confirm from its parent and its full command line that it is that job, and stop only that one; if you are not certain, let it finish. **A PID is neither proof of ownership nor permission to stop anything else.** Claude never terminates a project process: no experiment, worker, coordinator, batch, report or uncertain process, on any machine. The protected no-status/no-kill interlock (Architecture section 5C; section 5.4 above) and the owner's separate process-control gates govern those, and nothing on the owner's computer is ever stopped by Claude.
- The shell tool's default timeout is about two minutes: give a longer one, or run long jobs in the background
  writing to a file, and poll the file.
- The shell may reset its working directory: use absolute paths.
- Outbound network goes through an allowlist (package registries and GitHub). Lottery sites are never tried.
- Do not import a package's own scripts in place for a probe (a `__pycache__` folder once crept into a package).

### 12.6 The owner's machine

- Windows 11; 12 cores, 24 logical processors. Git with `core.autocrlf=true` (v12: without effect on this project
  since `* -text`; his working copy is byte for byte what Git holds). Downloads go to `E:\TEMP`, never into
  the repository.
- **DEV** is the clone at `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`, with its `.venv`
  (Python 3.15.2). **PROD** will be `G:\a_p_r_i_r` and **QA** `T:\a_p_r_i_r`, with backups under `T:\a_p_r_i_r_backups\PROD`
  and `\QA` (the owner, entry 181; the deployment design's own examples are older); each tree's `ENVIRONMENT.ini`
  decides. Neither exists yet. DEV has its `ENVIRONMENT.ini` (entry 212).
- **The scratch folder is `D:\DELETE_ME\`** (an SSD), for the runner's rehearsals (section 8.6). The owner deletes
  what is left there himself.
- **A plain CMD window** (from the Start menu) is where the owner runs a sheet and builds a `.venv`. A VS Code
  terminal has the main `.venv` active.
- **Measured there (24 November 2026):** the suite 25 minutes (571 tests) and 29 minutes (762); a first fill of
  both games 46 to 47 minutes; a job with nothing new 3 minutes; the comparison with the old records 2 minutes.
- The owner's OUTLANDISH_01 work (`GAIS/OUTLANDISH_01/`, with its own ChatGPT chat) is outside the reviewed line and
  uses the E: `.venv`. He commits it with `git add GAIS/OUTLANDISH_01/`, never `-A`.
- If a Windows console window is clicked it can freeze a program at its next print; Esc releases it.
- The owner is sometimes on a phone only: then give only steps that need no PC.
- He saves a package ZIP to `E:\TEMP` and extracts it there; the evidence folders of a sheet are `E:\TEMP\<name>_evidence`.
  His ZIP of the whole project folder (entry 163) is on four external drives.

### 12.8 Open items at this edition (v12: 25 November 2026; section 0E item 10 is the current list and prevails)

**(v14) No longer so: chapter 0, section 0.4, is the present list and prevails. What follows is of the morning of
25 November 2026 and earlier.**

The live state is `exchange/CONTINUITY_NOW.md`; it overtakes this list.

- **Waiting on the reviewer:** nothing.
- **Waiting on the owner:** (v11: H-2 v6 is ratified and build step 3 has his go; section 0D item 16 lists what waits
  now) his word on reminders R-007 (proposed
  dropped) and R-017 (proposed done) (entry 155).
- **Owed by Claude, in order of need:**
  1. Build steps 3 and 4, each on its go, with what section 10 says each must settle.
  2. The clean-sheet updater put to the reviewer as the owner's decision, before it is coded (section 10).
  3. The rewrite of `ENVIRONMENT.example.ini` (entry 211), in slice A. (v12: the conversion to the file-form
     standard, which v11 listed here, is done.)
  4. The test of EX_271 section 3, in build step 4.
  5. The next register edition (v13: **done as register v0.33, RAT-53;** the edition after it records RAT-53's
     install and RAT-54), when a code package or a handover next travels (section 1.6): it records RAT-41's
     install, RAT-42, RAT-43, RAT-44, build steps 1 and 2, the tidy-up and what follows.
  6. The operations manual's skeleton, agreed with the reviewer, after build step 3 (section 10 item 5).
  7. A new draft of `doc/METHOD_TEMPLATE/` for the new layout, after build step 3.
  8. The measurements still open in section 7.5.
  9. (v11) The reviewer's handover: H-2 v6 is installed (RAT-46); Claude's refresh H-2 v6r2 is unratified; the
     present reviewer chat writes its own next edition when it chooses.
- **Done since H-1 v9:** build step 2, reviewed, rehearsed, installed and run (section 0B items 8 and 9); the narrow
  rulebook amendment (v0.7, RAT-44); the owner's answer on the updater (entry 181).
- **Later, and only when the owner asks:** the deferred performance study (R-006;
  `doc/Deferred_Performance_Engineering_Proposal_v0_1.md`: profile real run times before choosing any speed-up; a
  first fill's time is inside three families' exact-fraction fits) and the simplicity review after full
  implementation (KISS-1).
- **Small leftovers the owner may choose to clear:** `E:\TEMP\STEP2_baseline_clone` (no longer needed, entry 212; v11: the
  scratch folder of TASK_T025 has been deleted by the owner, entry 222); deleting `venv.bak` and Python 3.14; the duplicate
  exploration note in `doc/`; the old EX copies in `review/`; after step 3's transition check, the old run folders.

### 12.9 The first hour in a new chat

1. Clone with full history; read section 0's list; check the hashes of section 4 and Appendix A.
2. Read the newest EX files and the decision log's last entries; list anything in flight (an unanswered message, a
   report not yet read, a decision given but not recorded).
3. **Confirm the takeover to the owner** in plain English (section 0, item 4). Do no work until he says so.
4. Only after his authorisation, and only when a build step is given its go: set up a workspace (section 12.3) and
   run the whole suite once with `run_suite.py` to prove the tools before any change; it should give section 7.1's
   known result.

---

## Appendix A. Identities

SHA-256 of the Git content at `HEAD` (LF unless noted), computed by the builder of the edition that wrote each row.
(v15, the reviewer's H14-C01 and its observation: at this edition's baseline 60 of the 69 hashes in
this appendix equal the file's bytes on `main` today. The others are older identities, each of the bytes it was
taken of at its commit, and are not expected to equal today's: `src/methods/_common/method_table.py`, `src/methods/Method_Contract_Runner.py`, `.claude/settings.json`, `src/research/ov1_numeric.py`, `src/research_command.py`, `Run_Research.bat`, `Withdraw_Variant.bat`, `deploy/INFRA_MANIFEST.ini`, `ENVIRONMENT.example.ini`.) A file cannot name its own hash:
this file's and its blurb's are in the decision log entry that records each edition.

| File | SHA-256 |
|---|---|
| `doc/Predictive_Randomness_System_Specification_v0_6.md` | `ee7199d0c17e8bcf877d49e25c6db1a009105c3f8da75ff1ec28b15726216ad0` |
| `doc/Predictive_Randomness_Deployment_Design_v0_12.md` | `e9f778d86c0c1a8a73bfbebf21982aec897a3afdb1296c3029f2ba1da9b58b3d` |
| `doc/CODING_PRACTICES_v0_1.md` | `d64f0101a4fdb21998b2871765bd9b3f06ccb6c7409c7a2d0e9f230cebbd7ddd` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v9.md` | `8c28f82c0662be75d683bd37b13d6b0596b3b6424584d5674f09f1d965b182b1` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v9_introductory_blurb.md` | `1cbe95bedb9741a610760b25de80e24eb3c798d9814287a4d28d8256c551dbe5` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md` | `b2837f08f8fd89134aebfbbed5815ca28b00f0ccebd1cb54c92f2f13c50cea2b` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122_introductory_blurb.md` | `5f113e4c4dca8648ccbf2a05e9a192bebf76d4473ad21e02c58de0b54a6bfcd5` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5_CANDIDATE_20261123.md` | `54ce9f3bd62ea0bac4e591d03904af34bf3ae444e5510af2aafc62057204a8af` |
| `doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md` | `7d572400b941ad423978a7542d6c32fb73c934f0057240dbc5138898112bd53b` |
| `doc/HANDOVER/AI_Roles_Transition_Record_H3_v1r1.md` | `8b01c57fd8804029906e1e9c87e8ecef18edb914a269e43a45dac90880703ce5` |
| `doc/RATIFICATION_REGISTER_v0_32.md` | `f59d1911279e7e95a952a14c3a0c68422ba0f4e67f91ffd5369eb73c606c9acb` |
| `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md` | `5067aa520990b8ccc8521a04f3581424100cdd94994f5b9e3cb9e37863685339` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` | `4416c4b574567f57f40d19ba9d58a765ce7dce551cf06937430aced730325456` |
| `exchange/README.md` | `e28255d525c04eca6a49254b7b9800b6a7600a4a40151c0e945f899928f892f0` |
| `exchange/DECISIONS/AGREED_APPROACH_2026_11_16.md` | `077cd5135415bfe3de10e9fe497ceb4cb6fc1e998e95625894db6c751b18e528` |
| `exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md` | `59e8d9c1ce8f5c1619e1c8c617e94535eee4dae179b8fafd67df9bec68d0ffd3` |
| `exchange/EX_271_ChatGPT.md` | `a80f1b61ed04938510a272ec9d6f0e5fcdb9ebbddb27113edab39dc947b8ca10` |
| `exchange/EX_274_ChatGPT.md` | `972cc2551ec5cd12f44dcc6f19ef27dfa4cd3ebe21c0402fc524d2ef8fc937f5` |
| `exchange/EX_276_ChatGPT.md` | `c45b3bda77ace3f9269870ea0ab96abb96d711731e5ccbef6147600edd5599c3` |
| `exchange/EX_277_Claude/EX_277_Claude.md` | `8b32b9e3e220c0a8279daf278e7f4acdfcad52a96ea148d0c163b68cc77b1a6e` |
| `exchange/EX_278_ChatGPT.md` | `53f6251128ab5ad1f7b089d4f0f09b68d70bf0fbba61599df451e63a6a3bddad` |
| `exchange/EX_279_Claude/EX_279_Claude.md` | `9a8f4327d54a5b7a131876c3c1f33f03d52103469636784729d93ba00c6ebaac` |
| `exchange/EX_280_ChatGPT.md` | `acd6e1d626dc3b29660b3dc28f92e8097c0ec619216cbca0d8b4d42f6b9440c0` |
| `exchange/CLAUDE_WEB_TOOLS/step1/STEP1_PACKAGE_NOTE_v0_3.md` | `dfe402f36bbe9e5f875b4da96b7b15dbf0a5cfd407bc5d9c38fdd92d90abf6db` |
| `exchange/CLAUDE_WEB_TOOLS/step1/check_layout_equivalence.py` | `1e7455ba9cbdeec09b6ff17378b26fec8c34c49d95285677516577ebde5dadd3` |
| `exchange/CLAUDE_WEB_TOOLS/step1/run_suite.py` | `89e8919917484ce73e7ead5d67ceeb15f89088ed5962dd3f78d348365332e24b` |
| `exchange/CLAUDE_WEB_TOOLS/step1/compare_suite_reports.py` | `37e0db59439b8e9de9c64b6725cd1116c653f8d685517800389c65fac35feb32` |
| `exchange/CLAUDE_WEB_TOOLS/tidy1/TIDY1_PACKAGE_NOTE_v0_1.md` | `ade815e023d3275088f6b282bbd86b63805fb68734ae13cf60c6c7494e9141f9` |
| `exchange/CLAUDE_WEB_TOOLS/tidy1/check_comments_only.py` | `71487c82d11964de12e63ef118ce541c6b6ed3c2e4dd1e09cad6a53e77ca43f1` |
| `exchange/CLAUDE_WEB_TOOLS/wf1/verifier_template.py` | `08aae763a2a3d782acdf9ed71c3768e97b7396ff2a7a6e7021146f020ef5c937` |
| `exchange/CLAUDE_WEB_TOOLS/check_task_commands.py` | `7e0c05b7f971edd4a1d55a697651cbe7a80fc78d158158c3a00574f9a801243a` |
| `exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/slice2_new/src/evaluation/ov1_numeric.py` | `2858075e37d2fed447388c770aafe2de9c6d296cd84808078f4cff8cba8d8234` |
| `exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/slice2_new/tests/test_mhupb_ov1_numeric.py` | `6d6830e32906fbdf748f1cad6675b6edb069c23d453552678a6d79e18dda3370` |
| `src/methods/_common/method_table.py` | `ca63c367b5e9ebfdd78eb8477410aafe9f7afa0ea66a8f5f423b9eb4ba79c0eb` |
| `src/methods/Method_Contract_Runner.py` | `89db65847b0743b7242a1f5ab2f26d5bae73ae0736d091a8f018e4d44361beb7` |
| `source_data/POWERBALL_results_master.csv` | `e4f2feb8b18fc2dbe389583a189fa26127a648f4da940dd76219ee282170f3e0` |
| `source_data/OZLOTTO_results_master.csv` | `63e3349333f8aa0485b7b067abe70249e39de81c6d02cda1a5710cf1041a4e9e` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5r1_20261123.md` | `234e5917c2b980cc50a1a0f08fc77af320febdd0ee05f595abff32564714edc8` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5r1_20261123_introductory_blurb.md` | `f195212e0de626608b2fb7f96c71d3244b3770394baa28eb372449707f6f20aa` |
| `exchange/EX_283_ChatGPT.md` | `13994645ab0cb9a9d1dd0008dd8690db28313e2c6ccbf4c3061bcde600f30be8` |
| `exchange/EX_285_ChatGPT.md` | `fb42367a43891fc6a405356629dd1a0d7c967fd6872cf9da506a239037d00581` |
| `exchange/EX_286_ChatGPT.md` | `3f5e07f6611927b12231aa28134f69e07738a0203d121278bf3049c2350e31ff` |
| `exchange/EX_287_ChatGPT.md` | `42b8e7daee36f1bff8bda2912b086f732c28c97c5f4ae4c1503598ee4c57daf5` |
| `exchange/EX_289_ChatGPT.md` | `a42ef8d8c71f150b376869596bafcb6cacf977b0796ca219065a2fe628f673fb` |
| `exchange/EX_290_ChatGPT.md` | `9903cafccc4d23ee1ce43c0c8024733db8ad82f776cec9d9b5802313a79b7378` |
| `exchange/EX_291_ChatGPT.md` | `9d39717eb7b2744577517c8056e57e7852525810225300fcdd917771be6723e5` |
| `exchange/EX_292_ChatGPT.md` | `13a2bfd95e7989f1b737bcfe36c094d7e09ec60be875847427e764ddb3d53845` |
| `exchange/EX_293_Claude/EX_293_Claude.md` | `1c693c612820b1bb9489900416c61b5e74f103d64a942bb17e127f5bd50030ba` |
| `exchange/EX_294_ChatGPT.md` | `9f59ae4fd1318e6c36bd639221df442ec9566222b40723975b99ed08ba5c8ce1` |
| `exchange/EX_295_ChatGPT.md` | `983f748344d41f07207f8fdc14b185264622b2817015bf6e9810947d58a6e641` |
| `exchange/CLAUDE_WEB_TOOLS/step2/STEP2_PACKAGE_NOTE_v0_3.md` | `3d14dbc9c68e406355af07e8e8d16a2b44687a74bb76851e1f5ea332eca28ccf` |
| `exchange/CLAUDE_WEB_TOOLS/step2/package_v1r3/STEP2_Research_Engine_v1r3.zip` | `e80e87ae4d0d9e9baaa15b8f2a405df717f66eb6be7de4126b734ad374bc6926` |
| `exchange/CLAUDE_WEB_TOOLS/step2/package_v1r3/INSTALL_AND_RUN_SHEET.md` | `9fa3ee880519d90ca497e4cabdb93c080e3cae11a664ff0ce68b7ee9dadd2310` |
| `exchange/CLAUDE_WEB_TOOLS/step2/build_step2_pkg.py` | `c17056636464856f824d71d1f6b29b8d1a404c4354c5e4160f8bdccfd2513bad` |
| `exchange/CLAUDE_WEB_TOOLS/step2/compare_fill_with_old_records.py` | `b4135af7ea925caba020bcbc77185999f51837bff0dcedddeb295ff0d241ada6` |
| `exchange/CLAUDE_WEB_TOOLS/step2/check_compare_tool.py` | `db4f255693bd7319581d31143f094e914b7a6bb13e7c24191b1bd11a2a2cb0a7` |
| `.claude/settings.json` | `bf4def6d8c9a9c7b44a39b030e3236197c2964db5b2cf82a9efd9145bd56ecfd` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T025.md` | `c9482a9a5c87edf57834d5d1118309dbab44aea553baae3ba3e1018dc5215fb5` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T026.md` | `473cd1ef8889247767603a6b107cd7891612fb62a7f82520a5a1a72413630cd8` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T027.md` | `a2252015fc88ee8cf9ee98d533425dd2644d9988927be567d207ccc1964bf1cd` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T025.md` | `37df8e8a6163ded0d21f15c21eea5c985d02f2578c9494ba3511e3ce69710992` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T026.md` | `3b009412faea0169399f36203aafe584131c195f1e2cf3f9875f349e39838799` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T027.md` | `66c0579d26beb3d2bfabec68e29dd0d9ad42df6a12aa7b162f23674d9aae38df` |
| `src/research/ov1_numeric.py` | `2858075e37d2fed447388c770aafe2de9c6d296cd84808078f4cff8cba8d8234` |
| `src/research_command.py` | `67e2edd38a27933768c3a034cc8612c27f8da64730f4d9f2915b10fbcea627a5` |
| `Run_Research.bat` | `e4786da8f15c3cbc9e52e94e648753b6f81ebb0d04e149b3330a1e6c1d4dbdf3` |
| `Withdraw_Variant.bat` | `7cd9afe9a0a978a301de8d8ad9db252707ff3ca635493ab579a07a882281f0ab` |
| `deploy/INFRA_MANIFEST.ini` | `eccdea0040a4fc96792d5192f495f5e8901ab51dc29bd911e0888ae0e3baaace` |
| `ENVIRONMENT.example.ini` | `565b7f9fdef8d236600569df5c47088bac81935e2aeef78ebfd5c8798c47fdd7` |

Commits named in this file: `5f16b35` (build step 2 installed); `c7e6ed8` (the tidy-up installed) and `6c3a0fa` (its record); `0aea10a` (build
step 1 installed); `31db13b` and `23689ef` (the reviewer's H-2 v5 candidate); `79406e4` and `35a2ebf` (the
refreshed H-2 v4 and its blurb); `cc0ab73` (the old code baseline); `c7622fa` (the Mode H results and version-2
masters); `cc665ce` (the score records); `cf1c6d9` (the first commit after the history clean-up). H-1 v8
Appendix A names the commits of the design rounds.

---

## Appendix B. What changed from H-1 v9

### B.1 What changed from H-1 v9

| v9 section | In v10 |
|---|---|
| Header | rewritten for the state after build step 2; status CANDIDATE |
| 0 First actions | item 2: the newer entries, build step 2's note and the reviewer's findings on it added to the reading list; the rulebook's edition |
| 0A Things that trip a new chat | item 1: the research engine is installed; item 3: the newest numbers; items 12 to 15 added (CRLF record files and the changed-line count; no push during an install; the reviewer takes EX numbers; the old system's insufficient-history records) |
| 0B The state | heading's date; items 1 to 7 kept (in item 6 "target record" for "forecast", EX_295); items 8 to 10 replaced by items 8 to 13 (build step 2; the rehearsal and rulebook v0.7; the owner's decisions for step 3; what is authorised; what is owed; the chats) |
| 0C Notes on sections 1, 2, 2A | item 1: the present reviewer chat and its takeover (EX_295); item 2: rulebook v0.7 |
| 1, 2, 2A | **carried byte for byte** (still H-1 v7r1's bytes) |
| 2B, 3, 4.1 to 4.3, 5, 8.1 to 8.5, 8.7, 9, 11, 12.1, 12.5, 12.9 | unchanged |
| 4.4 History and working documents | H-2 v4 labelled as history and H-2 v5r1 as the one installed reviewer handover (EX_295) |
| 6 Verified technical facts | one phrase: "target record" for "forecast" (EX_295) |
| 7.1 The installed code | the research engine, the settings file and the suite's new known result (52 modules, 762 tests) |
| 7.2 Data and records | "target record" where all the old records are meant, and the never-scored counts put right (EX_295); two items added: DEV's research results; the old records counted exactly |
| 7.3 Staged work | one sentence: the OV-1 kernel is carried into `src/research/` byte for byte |
| 7.4 The build's record | `step2/`, `rulebook_v0_7/` and the three task folders added |
| 7.5 Not tested | rewritten: what has run, what has run only in tests, build step 2's known limits, what is still to measure |
| 8.6 The local runner | rewritten: rulebook v0.7 and its section 2A, the owner's settings change, the runner's shell, the three tasks |
| 8.8 Lessons | ten lessons from build step 2 added at the top; the rest unchanged |
| 10 Next work | rewritten: step 2 done; step 3 with the owner's decisions; the operations manual; the updater decided |
| 12 intro, 12.2, 12.3, 12.6 | brought up to date (the step 2 tools; what step 2 added to building a package; the owner's places, his scratch folder and the measured times) |
| 12.4 Task files | rewritten as the practice of TASK_T025 to T027 |
| 12.8 Open items | rewritten |
| Appendix A | rebuilt from HEAD: v9's files with their hashes computed again, H-1 v9 in place of H-1 v8, H-2 v5r1 and its blurb (EX_295), and the files a new chat now needs |
| Appendix B | this one |

Nothing binding was dropped: every v9 passage that was replaced described a state that has since moved on, and the
decision log entries 175 to 213 hold the record.

### B.2 Known limits

- **Verified with tools for this edition:** every hash in Appendix A (computed by the builder from `HEAD`); that
  sections 1, 2 and 2A equal v9's bytes; that every replacement's old text is found exactly once in v9; the counts
  and times of section 0B item 8 and section 7 (the owner's unedited console outputs and the runner's three reports).
- **Not re-checked for this edition:** the hashes written in sections 4.2 and 4.3 (v9's text, unchanged files);
  statements about the owner's PC other than those in his outputs and the runner's reports; H-2 v5r1, which is the
  reviewer's.
- **Written by the chat that did the work,** late in a long conversation: the reviewer's cold read of this edition
  against the repository is the check on it.

### B.3 Integrity

(v12, and v13, which is built the same way from H-1 v12's bytes) US-ASCII; **CRLF** (the file-form standard: a new text file); one final line ending. The carried sections 1,
2 and 2A are identical to H-1 v11's, and so to H-1 v7r1's (the builder asserts it against v11). Every
replacement's old text is found exactly once in H-1 v11. The builder refuses on any failure. (This paragraph
still described H-1 v9 and v10 in H-1 v11, whose last line read "End of H-1 v10": a stale statement, put right
here.)

## Appendix C. What changed from H-1 v13 (the builder's own account)

**Carried byte for byte from H-1 v13** (the builder asserts each): sections 1, 2 and 2A (H-1 v7r1's text; (v15)
the same as v7r1's only after line endings are normalised, H14-C02); and
sections 0B, 0D and 0E, moved to the HISTORY part at the end with their headings, so that a reference such as
"section 0E item 14" still finds its text.

**Written afresh:** the header and chapter 0 (sections 0.1 to 0.7), which take the place of H-1 v13's header,
its section 0 and the live content of its sections 0B, 0D and 0E. This Appendix.

**Carried with corrections made in place, each marked "(v14)":**

- **Section 0A item 1:** what is coded of the new system (EX_317 H13-C04).
- **Section 0A item 3:** the newest register, and the numbers of v11 removed (entry 270 point f).
- **Section 0C item 1:** the reviewer chats brought up to date.
- **Section 0C item 4:** the newest register (entry 270 point f).
- **Section 3:** what is built (entry 270 point c).
- **Section 4.4:** the reviewer's handover and the register in force now.
- **Section 5.1, the two-site checker:** the checker is no longer byte for byte unchanged (EX_317 O01).
- **Section 5.1, `.gitattributes`:** the three lines of the standard (entry 270 point e).
- **Section 5.3:** the records an installed tree does hold (EX_317 H13-C03).
- **Section 7.1:** the engine is 21 files (EX_317 H13-C04).
- **Section 7.3:** the OV-1 kernel and the test that was said to assert it (entry 270 point h; EX_317 H13-C01).
- **Section 10:** a line that sends the reader to chapter 0.
- **Section 12.8:** a line that sends the reader to chapter 0.

**Nothing else is changed.** Everything of H-1 v13 that is not named above is in this edition byte for byte, in the
same order: sections 0A and 0C (but for their corrections), sections 3 to 12, Appendices A and B.

**The findings this edition answers:** decision log entry 270, points (a) to (h); EX_317, H13-C01 (the OV-1
kernel: section 7.3), H13-C02 (hashes and line endings: 0.6, 0.7), H13-C03 (records in an installed tree: section
5.3, 0.5 item 7), H13-C04 (the layers: this whole edition), O01 (the two-site checker: section 5.1) and O02 (H-1 v13's
header said no reviewer had read it before installation; the reviewer had checked its difference from H-1 v12, its
hashes and its carried sections before ratification, and made the full cold read afterwards, EX_317).

---

## Appendix D. What changed from H-1 v14 (the builder's own account)

**Written afresh:** the header and chapter 0. H-1 v14's chapter 0 is not carried (H-1 v14 stays in
`doc/HANDOVER/` as history).

**Carried byte for byte from H-1 v14** (the builder asserts each): sections 1, 2 and 2A; and the HISTORY part.

**Changed in place, each marked "(v15)":**

- **Section 0C, its opening:** what "byte for byte" means for sections 1, 2 and 2A (H14-C02).
- **Section 4, its opening:** which hashes of section 4 are today's bytes, computed (11 of 11; H14-C01).
- **Appendix A, its opening:** which hashes of Appendix A are today's bytes, computed (60 of 69; H14-C01 and the observation).
- **Section 9, OUTLANDISH_01:** OUTLANDISH_01 closed (entry 295; the reviewer's cold read, section 5).
- **Section 10, item 6:** OUTLANDISH_01 taken out of the order of work.
- **Section 10, what is genuinely open:** OUTLANDISH_01 taken out of what is open.
- **Section 11:** the restore's one ratified exception named beside the orphan rule (H14-C03).
- **Appendix C, its first paragraph:** the same precision (H14-C02).

**Nothing else is changed.** Everything of H-1 v14 from section 0A to its Appendix C that is not named above is in
this edition byte for byte.

# HISTORY (not live): sections 0B, 0D and 0E of H-1 v13, byte for byte

**Nothing below this line says what is true now.** These are the three layers that H-1 v9 to v13 added one upon
another: the state at 24 November 2026 (0B), what followed that afternoon and evening (0D), and the night of 24 and
the morning of 25 November 2026 (0E). They are kept whole because they hold the detailed record of build step 2's
rehearsal and first fill, the file-form standard and the conversion of DEV, the probe TASK_T028 and slice A's
beginnings, and because other sections refer to their items by number. Where they say what is in force, what is
next or what waits, chapter 0 prevails.

## 0B. The state at this edition (24 November 2026)

1. **The first study, Mode H, is complete and sealed in both games** (Oz Lotto 15 November 2026, Powerball
   16 November 2026). Its result, in the words agreed for the record (EX_205 section 5; register v0.31): "No
   statistically significant predictive advantage was demonstrated under the predeclared Mode H tests." The sealed
   records are never altered, rerun or rescored. They are an archive, never a gate in normal work, and they are not
   part of the new trees (specification 17.1).
2. **All draws are equal research targets** (owner, 16 and 18 November 2026). The former holdout draws are ordinary
   draws. No holdout is needed for future method development.
3. **The course correction** (owner, 20 and 21 November 2026; EX_258, EX_259; entries 121, 122): families and variants
   only, no revisions; a clean new baseline, nothing destroyed; three separate trees; minimum administrative software.
   The design rounds that followed are EX_260 to EX_271; the reviewer's PASS (DESIGN) is EX_271.
4. **The approach the owner agreed on 16 November 2026** (`exchange/DECISIONS/AGREED_APPROACH_2026_11_16.md`; reviewed
   with conditions in EX_206; in force since RAT-34), unchanged by the redesign:
   - The AI chats may read draw values, the masters and the results. They never write there.
   - Three protections stay: no lottery website and no results search by any AI (the owner's reviewed updater is the
     only source); results count only from the reviewed programs and their logged runs, and anything an AI works
     out in a chat is labelled "suggestive"; method-facing N-1 isolation, forecast identities and append-only records.
   - **Claude's writing:** documents and records are committed and pushed by Claude directly (named paths; fetch and
     fast-forward first; nothing deleted or overwritten): freely under `exchange/` and
     `CLAUDE_CODE_WORKING_FOLDER_TREE/`, and into `doc/` only once reviewed and ratified. **Code and tests never go into
     `src/` or `tests/` from Claude:** they travel as a reviewed package that the owner installs (section 1.6).
   - The reviewer commits its own EX replies to `exchange/` and its own handover files to `doc/HANDOVER/`.
5. **RAT-40 (22 November 2026, 13:33; entry 147).** The owner ratified the system specification v0.6 and the
   deployment design v0.12, with four notes binding on the code: (a) wherever variants are held or results are not
   current, the job says so plainly at its start and at its end, names the cause and gives the exact command; (b)
   `doc/CODING_PRACTICES_v0_1.md`, which **the owner applied to all coding, build step 1 included** (entry 158); (c) a
   light tidy-up of the existing method files after build step 1 is proved and before anything is installed into QA
   or PROD (**done**, item 7); (d) the one test of EX_271 section 3, owed in build step 4.
6. **Build step 1, the folder layout, is INSTALLED and proved** (entries 158 to 164; `main` `0aea10a`, 23 November
   2026). Reviewed in EX_275 to EX_278 (one RECHECK of four narrow corrections). Before it the owner made his own ZIP of
   the whole project folder on E:, with `.git` and the Git-ignored old run folders, on four external drives (entry
   163): it is the way back to the old system (specification 17.2). On his PC: the suite identical before and after;
   **the equivalence check `RESULT: PASS - COMPLETE`**: every old development target record (Powerball 17,280, Oz Lotto
   8,760; not all of them are forecasts, section 7.2) computed again with the moved code and equal by
   `canonical_content_digest`.
7. **The light tidy-up is INSTALLED and proved** (entries 165 to 169; `main` `c7e6ed8`). 37 method files got the coding
   practices' headers and comments; no code changed. The owner accepted leaving E_1's six byte-pinned modules as they
   are (entry 166). Reviewed in EX_279 and EX_280 (PASS). On his PC: a new comments-only check (`RESULT: PASS`), the
   suite unchanged, and the equivalence check again `RESULT: PASS - COMPLETE`.
8. **Build step 2, the research engine, is INSTALLED in DEV and has run** (the owner's go, entry 176; entries 176 to
   212; `main` `5f16b35`, 24 November 2026). A new package `src/research/` beside the old system, which is not edited: the lists, the job
   (`Run_Research.bat`: start, fill, results, catch-up, end), scoring, the reports, both OV-1 scores, each variant's
   status file and the withdrawal (`Withdraw_Variant.bat`). Reviewed in four rounds: EX_283 (two crash-recovery
   blockers), EX_285 (one, in the first correction), EX_290 PASS, and EX_294 PASS for package v1r3, which changed one
   tool. The package is `STEP2_Research_Engine_v1r3` (`exchange/CLAUDE_WEB_TOOLS/step2/package_v1r3/`); its note is
   `STEP2_PACKAGE_NOTE_v0_3.md`. **On the owner's PC:** the install sheet's parts 1 to 4 (`PRE`, `POST` and
   `COMMITTED PASS`; the suite 571 tests before and 762 after, every old test with the same result); DEV's first
   fill of both games in 47 minutes (Powerball 15,118 forecasts and 15,078 scores; Oz Lotto 6,598 and 6,558); a
   second job with nothing to do in 3 minutes; and the comparison with the old records **`RESULT: PASS - COMPLETE`**:
   all 34,800 old score records and all 20,436 forecasts the old development runs kept are in the new lists with
   the same view digest, scores, ranking, TOP and WORST. Section 7 has what exists; section 7.5 what has not run.
9. **Before the install, a rehearsal on Windows by the local runner** (TASK_T025, T026 and T027; entries 199 to 208),
   in a task clone and in a scratch tree under `D:\DELETE_ME\`, under **the runner's rulebook v0.7** (RAT-44, entry
   192; section 8.6). It found three things where nothing real could be harmed: the runner's shell has the main
   `.venv` active, so a tree's own `.venv` is built from a plain CMD window; a fault in Claude's comparison tool
   (corrected in package v1r3); and the time of a first fill.
10. **The owner's decisions for build step 3, already given** (entries 180 and 181; 23 November 2026): no parallel
    or multi-threaded runner now; the results updater as a **clean-sheet new edition** (`results_master_v0_3.py`: every
    Mode H state removed, every genuine source, parse, overlap, chronology, ledger and lock check kept and proved
    unchanged, `v0_2` left untouched in DEV), to be put to the reviewer, whose stated preference was narrower; (v11: H-1 v10 said here "line endings pinned to LF for the project's code in `.gitattributes`, in step 3, before
    the first tree is made"; the file-form standard, RAT-47, replaces that: section 0D); the
    places: PROD `G:\a_p_r_i_r`, QA `T:\a_p_r_i_r`, backups `T:\a_p_r_i_r_backups\PROD` and `\QA`; rehearsals as Claude
    chooses, the runner in the scratch folder on D:.
11. **What is authorised now (v11):** documents and records; and, since the owner's go of 24 November 2026 (entry
    217), build step 3's design within the ratified documents, its coding and testing in the cloud, and its
    reviewed packages. Every install, run, tree creation, conversion, backup, restore and runner task on his PC
    still needs his own go.
12. **What is owed** is listed once, in section 12.8.
13. **The chats.** This Claude chat took over on 22 November 2026 from H-1 v8 (HO-2 accepted, entry 157) and did build
    step 1, the tidy-up and build step 2. A new ChatGPT reviewer chat took over from H-2 v5r1 on 23 November 2026
    (entry 175) and reviewed EX_282 to EX_294. (v11: that reviewer chat wrote H-2 v6, RAT-46, and ended on 24
    November 2026 after EX_303; a new reviewer chat started that evening from Claude's refresh H-2 v6r2 and has
    written EX_304 and EX_305: section 0D.) The owner has not decided on a Claude chat switch; this edition is written so that one
    can happen at any time (the chat is long).

## 0D. After H-1 v10: 24 November 2026, afternoon and evening (v11; it prevails over older statements, and section 0E prevails over it)

Everything here is from the decision log (entries 216 to 243), the EX messages (EX_297 to EX_306) and the files named.
**Next numbers at this edition: EX_308, decision log entry 245, RAT-49** (v12: those were v11's; the present ones
are at the head of section 0E)**.** Fetch `main` and confirm before using any:
the reviewer took five numbers in a row this afternoon while Claude was working.

1. **Records.** RAT-46: the reviewer's H-2 v6, ratified as its corrected candidate v6r1 (entry 216). RAT-47: the file-form standard (entry 237). RAT-48: this handover (entry 244). The next
   register edition is still owed (section 12.8 item 5) and now also records RAT-45 to RAT-48.

2. **Build step 3 has the owner's GO (entry 217, 15:53): "Build step 3, go now please."** It covers design within
   the ratified documents, coding and testing in the cloud, and the reviewed packages. It covers no install, run,
   tree creation, backup, restore or runner task on his PC.

3. **The build plan:** `exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md`. Four code slices, each a package
   for the reviewer, then the transition: **A** foundations (the settings of the three trees, the readiness
   markers and `Make_Installable`, the static import check, the list of installed files, the environment's digest,
   `Check_Tree`, the launch guard); **B** backups, the recovery kit, the restore; **C** `Init_Tree`, `Install`,
   `Reinstall_Infra`, `Verify_Tree` and the half-finished states; **D** the clean-sheet updater
   `results_master_v0_3.py`; **E** the transition (`Init_Tree.bat QA`, which stops for the owner to build QA's own `.venv`; `Init_Tree.bat QA`
   again; `Run_Research.bat --game BOTH --no-update` in QA; the transition check there; then PROD). Its section 6A lists what the joined slices must show before the
   one install into DEV. **Reviewed:** EX_299 (four findings), narrowed by EX_300; all corrected in v0.1r1;
   **EX_301 FOCUSED PASS.** A working plan, not a ratified design.

4. **The owner's decisions on the plan (entry 219):** one install into DEV at the end; a probe task first; QA
   before PROD; the plan to the reviewer.

5. **How Windows' processes are read (entry 222; plan section 4A).** The reviewed `src\package_tools\process_check.py`
   uses psutil and holds the old system's lock clearances: its rule and its refusals are kept, the file is not
   reused. **The owner chose:** the restore stays standard library only (a few dozen lines read names, parents and
   start times from Windows; the probe has such a reader); every other process check uses psutil; psutil for the
   restore too only if that proves too hard, said beforehand. **The narrow amendment of the deployment design
   section 2 ("standard library only" for the install tools) is NOT ratified yet;** put its wording to the reviewer
   with slice A. (r1) TASK_T028 showed the standard library's reading agreeing exactly with psutil's on the owner's
   PC: option A stands, and option B is not needed (entry 240).

6. **TASK_T028, a probe of three Windows facts: RAN on the owner's PC on 24 November 2026, on his go; PASS, every
   measurement made (r1; entries 239 to 242).**
   `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028.md` r1 and `inbox/TASK_T028_probe.py` r1 (builder and template in
   `exchange/CLAUDE_WEB_TOOLS/t028/`). EX_301 found three faults in the first edition; EX_302 passed r1. It
   measures how Windows answers a rename, replacement or removal when something is open; the size and time of a
   ZIP of the main `.venv` alone (an environment-only proxy: the scratch tree of TASK_T025 is deleted); and what
   psutil and the standard library each read of the PC's Python processes. The
   install, backup and restore logic of slices B and C is designed around its answers. **What it found (entry
   240; `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T028.md`):** Windows refuses, wholly, a folder's rename and a
   file's replacement or removal while a file in it is open or another process stands in the folder, and lets
   them through at once afterwards; 1,000 write-then-replace cycles were never refused; the main `.venv` is
   19,059 files and 508.9 MB; the environment digest's inventory took 150.6 seconds on first reading and 5.2
   when lately read; its ZIP is 180.2 MB in 80.1 seconds at Deflate level 9 (184.5 MB in 20.7 seconds at level
   6); the standard library's reading of the process table agrees exactly with psutil's; and **every Python
   program started from an environment is two processes** (the environment's `python.exe` and the base Python
   under it), so every process rule counts a pair as one program. **The owner keeps Deflate level 9** (entry
   243), against the reviewer's informal preference for level 6. One evening, drives D: and E: only; T: and G:
   are measured in the joined rehearsal. After the steps the runner ran one line of its own that its report
   does not record (entries 240, 241): no measurement is affected, and the reviewer asked for no rerun. The
   scratch folder `D:\DELETE_ME\a_p_r_i_r\T028` may be deleted by the owner.

7. **Slice A's working files exist** (entries 222, 225): `exchange/CLAUDE_WEB_TOOLS/step3/overlay/`, copied into a
   work clone and tested by `step3/sync_and_test.sh <clone> <python> <test modules>`. **Not a package, not reviewed,
   nothing installed.** Done: `src/research/settings.py` (DEV's entries for QA and PROD and every cross-tree check
   of the deployment design's section 1), the rewritten `ENVIRONMENT.example.ini`, `deploy/install_import_check.py`,
   `deploy/install_readiness.py` (the two markers), `deploy/make_installable.py`, `deploy/deploy_command.py`,
   `Make_Installable.bat`, the manifest's `[install_tool]` section, and the tests `test_trees_settings.py` (32) and
   `test_trees_readiness.py` (38). **Two readings of the specification to put to the reviewer with the slice:** a
   variant may import its own listed files as well as its helpers; the tool itself refuses a variant that imports
   an infrastructure file not classed `forecast`. **Not yet written:** the list of installed files, the
   environment's digest over the fixed inventory, `Check_Tree`, the launch guard. **All of it was written before
   the file-form standard:** its files and the bytes its programs write must be brought to the standard.

8. **The owner's principle (entry 227, his words):** "git should never be used as an operational gatekeeper/checker
   nor for gating/checking deployments etc, github is a tool for managing commits and project statuses." No tool
   of the new system consults Git. The readiness markers are not tracked by Git.

9. **THE FILE-FORM STANDARD, RAT-47 (entries 226 to 237): `doc/FILE_FORM_STANDARD_v0_1.md`** (v12: now v0.2, RAT-49,
   which holds one fault of fact of v0.1 corrected: section 0E item 2)**. Read it; it replaces
   "LF pinned".** How it came about: three files under `src` are CRLF on the owner's disk where Git holds LF, and
   one of them, `src/methods/_common/game_profiles.py`, is `forecast`-class, so its bytes are part of the identity
   every list in DEV records. The owner would not leave that as it lay, asked what Windows' own conventions are,
   and directed a written standard to which everything conforms. **The standard:** every text file of the living
   project is CRLF, whoever wrote it; **every `.jsonl` file is LF** (a list line is the canonical encoding whose
   bytes, ending included, the hash chain and the content digests are computed from); every program names the
   line ending it writes (Python's default differs between his PC and the cloud); Git converts nothing (`* -text`
   at the root; `GAIS\` keeps its own rules, entry 234); the project's own checker enforces it, in the suite, in
   `Make_Installable` and in `Check_Tree`; frozen history is never converted; six files of the retired Mode H
   release machinery are left out by name (its section 3A). **Reviewed** in EX_303 (four clarifications), EX_304
   (one: no undo from the list; the way back is the owner's copy) and EX_305 (FOCUSED PASS).

10. (v12: **DONE on 24 and 25 November 2026, and not as this item describes it:** one attempt with no second
    run, the owner's whole-folder copy as the way back, no rehearsal by the runner (RAT-50). Section 0E items 3 to
    6 have what happened; what follows is v11's text, kept as the record of what was planned.)
    **The conversion is the next work, before slice A is packaged** (the standard's section 7): a conversion list
    made in the cloud (each tracked file's SHA-256 before and after); a conversion program the owner runs in DEV
    (it walks the folders itself and never calls Git; prints what it found by class and waits for his word; a
    listed file whose hash is the "after" is passed over, "before" is converted, any third value is a STOP; it
    holds the job lock and the updater's lock; it checks his pre-conversion copy first, and **on a second run
    checks that copy against the "before" hashes recorded at the first run, not against files already
    converted** (the reviewer's watchpoint, EX_305)); the engine's writers changed to the standard's forms; the
    checker; `.gitattributes` and `.gitignore`; the one refresh of his working copy under `* -text`; a sheet; a
    rehearsal by the runner. **The conversion of `forecast`-class files changes the forecasting-code identity, so DEV's existing research
    lists become foreign: DEV's research results and its status files are removed on his own go and filled
    again (about 47 minutes); a status file that holds anything but ACTIVE is a STOP for his decision, and his
    checked pre-conversion copy is the way back.** (r1, EX_306 H11-C01: `game_profiles.py` itself is CRLF on his
    disk already, entry 226, and need not change; it is the other `forecast`-class files that do.) **Begun
    (entry 242), as working files, not a package:** `exchange/CLAUDE_WEB_TOOLS/conversion/overlay/` holds
    `deploy/file_form.py`, the one piece of code with the standard's rule, and `tests/test_file_form.py` (44 tests;
    the two that check the real tree fail until it is converted). The search for writes that name no line
    ending found two in the project's programs outside the six files left out by name. Claude's own new files are CRLF from that day, not before.

11. **What Claude's trial in the cloud showed, and did not** (`exchange/CLAUDE_WEB_TOOLS/standards/`): 669 files
    under `src`, `deploy`, `tests` and the root made CRLF in a copy; 732 of 762 tests the same; 30 failing, all in
    five `test_mhupa_*` modules, tracing to the six files left out by name; with those six put back, all five pass.
    It did not cover `source_data\`, the changed writers, the refresh of his working copy, or Windows.

12. **Mode H.** The owner (entry 230): "I dop not currently care about obsoleted Mode H stuff." Read narrowly: the
    retired machinery is not maintained and is no veto. **The binding rule that the sealed Mode H records are never
    altered is unchanged.**

13. **The operations manual** (entries 220 and 230; EX_298), after build step 3 is proved: short, for a human, a
    practical how-to; finding and reading the reports is a necessary topic; a short command cheat sheet in an appendix is to be considered, not decided (r1); a
    "Standards" section that names the `.jsonl` exception; its structure proposed by Claude and the reviewer
    together for the owner's approval.

14. **The reviewer chats.** The chat that wrote H-2 v6 ended on 24 November without notice after EX_303. At the
    owner's request Claude refreshed H-2 v6 as the candidate H-2 v6r2 (`exchange/CLAUDE_WEB_TOOLS/h2v6r2/`; entry
    232): unratified, and written by Claude, not by a reviewer. The owner started a new reviewer chat from its
    blurb (entry 234); it wrote EX_304 and EX_305. It read this handover's v11 in EX_306 (PASS for continuity; two narrow corrections, made in r1) and passed r1
    in EX_307, and the
    owner confirmed its established commit rights (entry 243). **In force for the reviewer: H-2 v6 (RAT-46).**

15. **The owner's PC is as H-1 v10 describes it.** DEV at `5f16b35` with his first fill; no QA or PROD; nothing of
    build step 3 installed; nothing converted; `.gitattributes` unchanged; the prevailing OV-1 not started.
    (v12: no longer so: DEV is converted, filled again and at `fe1c310`; section 0E item 8.)

16. **What waits, at this edition.** On the reviewer: nothing. On the owner: nothing (this handover is
    ratified, RAT-48). On Claude, in order: the conversion (item 10; v12: done, so the list now begins with slice
    A: section 0E item 10); the rest of slice A, to the standard; slices
    B, C and D; the joined rehearsal; the one install into DEV; then QA, the transition check and PROD, each on
    his go. Each week before PROD's first job is one draw of each game that cannot count in the prevailing OV-1.

17. **Lessons of the day, for whoever continues** (in the manner of section 8.8). (a) A script that writes a
    record and a commit command must not be two unchained lines: when the script stopped, the commit ran and
    named an entry that did not yet exist (entry 223); begin such a block with `set -e`. (b) The decision log is
    not pure ASCII (the owner's quoted words): append to it as bytes. (c) Never install on the owner's relay of
    the reviewer's recommendation; wait for his own words (entries 215, 236). (d) A task file is read cold for:
    every existing folder above the place it first writes; whether each command line does what the prose around
    it says; and whether "finished" can be printed when a measurement was not made (EX_301). (e) Before promising
    that a change can be undone, ask whether the change is one-to-one: making line endings uniform is not
    (EX_304). (f) Say what a reader's summary is evidence of: a cloud trial is Claude's evidence, not the
    reviewer's and not Windows'. (g) The owner's first answer to "which option" may be a principle; put the
    options again in its light instead of choosing for him (entries 227, 228). (h, r1) A task file that leaves the runner a need unmet (how the time is to be written; a
    check of its own report) invites an invented command: give the command in the task file (entries 240, 241).

**Identities added at this edition** (SHA-256 of the Git content at `HEAD`, computed by the builder):

| File | SHA-256 |
|---|---|
| `doc/FILE_FORM_STANDARD_v0_1.md` | `97034474f1a7e9c54a14b9554b45666cb1fa031d566545433a0412d4312f8335` |
| `exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md` | `6eb18f0e38279a9b68e88dec304dbea205a64b62bc8e80bfc8dc9723c39b3195` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028.md` | `96e2a6cf86873a9f6a1df1f9e9d3ec2c884e3a8f19b767395498b7ab7f88b02c` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028_probe.py` | `57fde59dc4f56526c1a73e95e006fee63b80bbffa223206740ee64776c6128bf` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124.md` | `588c52b9c08781956330676a3c13bda99b0c8fd90211139f74c26503adf174a1` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124_introductory_blurb.md` | `58c8f5b2b13dabc63f3739c04a42dd6bb30784fcf9c40b504e65da72c8c8efe3` |
| `exchange/CLAUDE_WEB_TOOLS/h2v6r2/out/ChatGPT_Reviewer_Handover_H2_v6r2_CANDIDATE_20261124.md` | `b078323351f37d370980d9a75dfcae98834f7cec7d94d0e1e6fb894da3617621` |
| `exchange/CLAUDE_WEB_TOOLS/h2v6r2/out/ChatGPT_Reviewer_Handover_H2_v6r2_CANDIDATE_20261124_introductory_blurb.md` | `c227314861daa9994bf9e6ff9da455759ee76a89d564ed04c47816754221215b` |
| `exchange/CLAUDE_WEB_TOOLS/standards/TRIAL_CRLF_SUITE_COMPARISON.txt` | `8baac6b033e2b60fb9f5f1ed6bb2f666bae4e455d7779b9db906c4da9d2e26af` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T028.md` (r1) | `69315a498ac59f5cb558786a89d8b5bbd8c1ba98f87d3e3660c00bfc4a5be7a5` |
| `exchange/EX_306_ChatGPT.md` (r1) | `e8a2813a9dc1cf4754920b4d67b3eab4872da795586ec069324581136cb7704b` |

## 0E. After H-1 v11: the night of 24 November and 25 November 2026 (v12, with items 13 to 16 added in v13; this section prevails over every older statement, section 0D included)

Everything here is from the decision log (entries 244 to 268), the EX messages (EX_308 to EX_316) and the files named.
**Next numbers at this edition (v13): EX_317, decision log entry 269, RAT-56.** Fetch `main` and confirm before using
any: the reviewer commits its own files, and did so twice on 25 November while Claude was building.

1. **Records.** RAT-48: H-1 v11 (entry 244). **RAT-49: the file-form standard v0.2** (entry 253). **RAT-50** (entry
   258): for the one conversion of DEV, one attempt and no resumption; the package `FILE_FORM_Conversion_v2`
   accepted; the runner's rehearsal dropped. **RAT-51** (entry 262): this handover, **ratified by the owner in
   advance** ("i ratify your new handover docs in advance") and so installed without the reviewer's read; that
   read is owed. **RAT-52** (entry 262): the reviewer's own H-2 v7, which the owner ratified in advance the same
   morning and the reviewer installed (item 9). (v13) **RAT-53** (entry 265): the ratification register v0.33,
   installed, which records RAT-41's install to RAT-52. **RAT-54** (entry 268): this edition, H-1 v13. **RAT-55**
   (entry 268): the reviewer's own H-2 v8 (item 13).

2. **THE FILE-FORM STANDARD IN FORCE IS v0.2: `doc/FILE_FORM_STANDARD_v0_2.md` (RAT-49). Read it.** v0.1 (RAT-47) is
   history. The rule is unchanged: every text file of the living project is CRLF; **every `.jsonl` file is LF**;
   every program names the line ending it writes; Git converts nothing; frozen history is never converted; six
   files of the retired Mode H machinery are left out by name. **What v0.2 corrected:** v0.1 said that the one
   line `* -text` in the root `.gitattributes` "does not reach GAIS". A simulation showed it reached 173 of
   GAIS's 204 tracked files. The root file therefore holds **three lines**, approved by the owner (entry 251):
   `* -text`, `GAIS/** !text` and `GAIS/**/*.bat text eol=crlf`. v0.2 also says: of 18 writes that named no line
   ending, the 16 in the frozen `src/results_master_v0_2.py` stay and the 2 in `src/two_site_results_check_v0_7.py`
   are corrected; the search covers programs, not tests' temporary fixtures, and "Any test that writes an actual
   in-scope project file remains subject to the standard" (EX_310); the staging and the refresh of the owner's
   working copy are done by a program, by content. Reviewed in EX_310 and EX_311 (FOCUSED PASS).

3. **THE OWNER'S FINDING, WHICH IS NOW A STANDING LESSON (entry 255; 24 November 2026, 22:33): "we have absolutely
   overengineered and wasted time and money."** And: "i do not understand how simple conversion of EOF could be
   made into such a drawn out process. there are no binary files that i know of, we could more easily easily have
   just done the lot and rebuilt all draws and data". Claude had built, for a job of line endings in some 650
   files, one Git setting and a refill: a conversion program with resume logic, a second program, a verifier, a
   look-only kit, 130 tests and planted-fault scripts; the reviewer's recheck (EX_312, five corrections C01 to
   C05) asked for more of the same. **EX_313 (the reviewer, on the owner's direction) superseded it:** one
   attempt; a verified copy of the whole project folder first; on any STOP the whole folder put back on the
   owner's go; only the small direct safeguards kept; no resume, no recovery machinery, no further testing. The
   edits to the existing programs took under half an hour. **What needed care in that job was two things only:**
   the short list of files that must not be converted, and one content-based staging step in Git (item 7).

4. **THE CONVERSION IS DONE (entries 255 to 260).** Package `FILE_FORM_Conversion_v2`
   (`exchange/CLAUDE_WEB_TOOLS/conversion/package/`; reviewed in EX_314, FOCUSED PASS; v1 is kept beside it as
   evidence). The owner ran its sheet in DEV on the night of 24 November, each part on his own go: the whole
   project folder copied to `E:\TEMP` and proved (107,135 files, `COPY PASS`); the package's 12 files copied in
   (`PRE PASS`, `POST PASS`); **650 listed files and `ENVIRONMENT.ini` converted, line endings only; DEV's 1,578
   research results and status files removed** on his typed `CONVERT` and `REMOVE`; the four results masters and
   ledgers proved unchanged; **685 files staged by content and 1,873 working copies of frozen documents put back to
   Git's own bytes** on his typed `STAGE`; the suite compared with a baseline made from a clean clone (762 of 762
   earlier tests with the same result); **his commit `691f58e4e171761f47f407dce2a4b7b7a687c271`**, `COMMITTED PASS`;
   the fill (47 minutes): POWERBALL 15118 forecasts and 15078 scores through draw 1591, OZLOTTO 6598 and 6558
   through draw 1708, **the counts of build step 2**; the repeat run wrote nothing; the comparison with the old
   development records `RESULT: PASS - COMPLETE - both games` (34800 score records and 20436 forecasts equal,
   `DIFFERENT: 0`); **pushed by the owner on 25 November at 07:02.** Verified by Claude from GitHub: all 686 listed
   files at the list's "after" bytes and in their form; 685 paths changed, none off the list; no `GAIS/` path
   and no `.jsonl` file changed. His windows: `conversion/day_result/OWNERS_WINDOWS_20261124_25.txt`. The whole-folder
   copy was never needed.

5. **One fault found that night, and corrected (entries 260, 261).** One of the 68 new tests failed on Windows
   only: `test_research_file_form ... test_a_lock_file_is_one_line_ending_crlf`. **Cause:** `src/research/job_lock.py`
   opened the lock file with `os.open` without `O_BINARY`; Windows' C runtime then writes a carriage return of
   its own before a line feed, so the line ended CR CR LF. Linux does not, so the cloud passed; and the standard's
   search for writes that name no line ending passes over `os.open` by design, which is where it hid. The owner
   chose to go on that night and correct it afterwards, and the reviewer agreed. **`FILE_FORM_Lock_Fix_v1`**
   (`exchange/CLAUDE_WEB_TOOLS/lock_fix/`; EX_315, FOCUSED PASS): one line gains `| getattr(os, 'O_BINARY', 0)`;
   installed by the owner as **commit `fe1c3108c10b77035a824968c9760803eb1b523a`**, 116 tests of the three affected
   modules `OK`, pushed. No rebuild: `job_lock.py` is class `derived`, and the engine writes that digest into new
   lines and compares it nowhere.

6. **What changed in the living project, in sum.** New: `deploy/file_form.py` (the standard's one rule, the checker's
   core, and the search for writes that name no line ending), `src/research/windows_text.py` (`windows_lines`,
   `LINE_ENDING`), `tests/test_file_form.py`, `tests/test_research_file_form.py`. Changed: the engine's four writers
   of text (`reports.py`, `status_file.py`, `derived_check.py`, `job_lock.py`) write CRLF; a status file's own check
   is over its CRLF bytes and a file in the old form is refused; two lines of the old
   `src/two_site_results_check_v0_7.py`; `deploy/INFRA_MANIFEST.ini` (the helper, class `derived`); `.gitattributes`
   (three lines); `.gitignore` (the two readiness markers). **No `.jsonl` writer and no calculation was touched.**
   The conversion changed the bytes of `forecast`-class files, so the forecasting-code identity changed: that is
   why DEV's results were removed and filled again, and DEV's lists now carry the new identity. **`Make_Installable`
   and `Check_Tree` are not yet wired to the checker:** that is slice A's.

7. **Working rules that follow. Each replaces an older habit of this file.**
   - **Every text file Claude adds is CRLF** (`.sh` and `.jsonl` apart), checked before each commit with the
     project's own rule, for example `file_form.faults_of_files(Path('.'), paths)` from `deploy/file_form.py`. The
     cloud workspace has no automatic conversion: write bytes, or name the line ending. **Files that existed
     before 25 November 2026 stay as they are:** the decision log and `exchange/CONTINUITY_NOW.md` are LF and are
     appended to as bytes; older files under `exchange/`, `doc/` and `review/` are frozen history.
   - **A file's bytes are now the same in Git, in a clone and on the owner's disk.** Hashes are compared exactly;
     nothing is "normalised" first. This supersedes section 1.6's "Verifiers must tolerate CRLF working copies"
     (a carried section, so its text stands unedited) and section 6's notes on line endings.
   - **A package's own files are delivered in their form** (CRLF), and a sheet's `certutil` hash of a file in DEV
     equals the hash of the Git content.
   - **Any low-level write of text is binary** (`os.open` with `O_BINARY`, or `open(..., 'wb')`), with the line
     ending written by the program. Only a run on Windows shows Windows' own translation.
   - **Git does not notice a change of line endings by itself** once `* -text` is set (it trusts the size and time
     it remembers): staging after such a change is by content (`git hash-object -w --no-filters`, then
     `git update-index --index-info`), as `conversion/tools/stage_and_refresh.py` did. That program and the
     conversion program are one-off tools, used once and not project code; do not reuse them.
   - **Nothing is pushed by Claude between the owner's pull and his push on a day of install** (it happened twice,
     entries 210 and 260; EX_315 asks the same of both chats). Records are written after his push.

8. **The owner's PC now.** DEV at `fe1c310` plus the records' commits, converted, filled, Git clean; its
   `ENVIRONMENT.ini` is CRLF. No QA or PROD; nothing of build step 3 installed; the prevailing OV-1 not started.
   Leftovers he may delete: `E:\TEMP\FILE_FORM_copy_of_project`, `E:\TEMP\FILE_FORM_baseline_clone`,
   `E:\TEMP\FILE_FORM_Conversion_v2`, `E:\TEMP\FILE_FORM_Lock_Fix_v1`, `E:\TEMP\FILE_FORM_evidence_v2` and
   `D:\DELETE_ME\a_p_r_i_r\T028`. `E:\TEMP\STEP2_evidence` no longer exists: **a sheet must not name a baseline
   folder on his PC without saying how to make it again** (it is made from a clean clone: entries 210 and 260).

9. **The chats.** The reviewer chat is the one that started on the evening of 24 November (EX_304 to EX_315); it
   commits its own EX files and handover. (v13: **H-2 v8 is now ratified, RAT-55: item 13.**) **In force for the
   reviewer when H-1 v12 was written: H-2 v7 (RAT-52),**
   `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v7_20261125.md` with its blurb beside it: written and installed by the
   reviewer on 25 November 2026 at 07:17, ratified by the owner in advance, current to entry 261 and EX_315. It is
   the reviewer's: Claude has not reviewed it and does not edit it. H-2 v6 (RAT-46) is history, and Claude's
   refresh H-2 v6r2, never ratified, is superseded by it.
   **The owner's plan for this Claude chat ends on the night of 25 November 2026;** this edition is written so that
   a new chat can take over from it.

10. (v13: **item 15 is the present list;** in this item (a) is under way, item 14, and (c) is done, RAT-53.)
    **What waits, at this edition.** On the reviewer: its cold read of this handover (item 1). On the owner:
    nothing. **On Claude, in order:**
    (a) **slice A of build step 3** (section 0D items 2 to 7): its working files in
    `exchange/CLAUDE_WEB_TOOLS/step3/overlay/` were written before the standard and against `main` at `5f16b35`;
    bring them to the standard (CRLF; every write names its line ending), rebase them on `main` as it is now, wire
    `deploy/file_form.py` into `Make_Installable` and `Check_Tree`, write what section 0D item 7 lists as not yet
    written, and put the slice to the reviewer with the unratified amendment of the deployment design's section 2
    (how processes are read, section 0D item 5) and the two readings of the specification;
    (b) slices B, C and D, the joined rehearsal, the one install into DEV, then QA, the transition check and PROD,
    each on his go;
    (c) the register edition (overdue);
    (d) the operations manual's skeleton after build step 3; its "Standards" section names the `.jsonl` exception.
    **Apply item 3 to all of it: say the simplest safe route first.**

11. **Lessons of these two days, for whoever continues** (in the manner of section 8.8).
    (a) For a one-off migration, begin from "a verified copy of the whole folder, one attempt, put it back on a
    STOP". Do not build resumption. When the owner asks for a standard, tell him at once what the smallest job
    is that would meet it.
    (b) A reviewer's recheck can itself over-engineer. Say so to the owner, with the risk each demand guards
    against and whether that state can exist; the decision is his.
    (c) A comparison that lists a new test as NEW does not say whether it passes. A sheet says that each new
    module ends `OK`, and Claude reads the suite's own lines, not only the comparison's.
    (d) What a program prints is promised by its sheet: a finding about a file is fixed words, never the file's
    content (EX_308).
    (e) A statement of fact in a document for ratification is tried before it is ratified: "does not reach GAIS"
    was written, reviewed and ratified, and was false (entry 250).
    (f) The cloud's evidence is not Windows'. Three Windows facts cost time here: the C runtime's text mode, the
    refusal of a rename while a file is open (TASK_T028), and that every program started from an environment is
    two processes.
    (g) Do not push during the owner's install (item 7).
    (h) When the owner says stop, stop; put the options, recommend one, and do only what he chooses.

12. **What changed from H-1 v11.** The header; section 0 item 2 (the standard's edition; entries 244 to 261); section
    0D (its heading, its next numbers, items 9, 10, 15 and 16: each a note that v12 supersedes it; the text is
    kept); section 4.1 (the standard v0.2 and its hash); section 6 (two notes on line endings); section 7.1 (the
    suite's known result since the conversion); section 10 items 2 and 3; section 12.6; section 12.8 (its heading,
    items 3 and 5); Appendix B.3 and the last line; and this section. Sections 1, 2 and 2A are byte for byte H-1
    v11's. Nothing binding was dropped. **Not re-read for this edition:** sections 3, 5, 8, 9, 11, 12.1 to 12.5,
    12.9 and Appendix A, which are H-1 v11's text; Appendix A's hashes were computed at H-1 v10 and v11 from
    files that Git then held LF, and for files of the living project they are **no longer the hashes of the
    present files** (the conversion changed their bytes). Compute afresh from `HEAD`.

13. **(v13) Since H-1 v12: the morning of 25 November 2026 (entries 263 to 268; EX_316).**
    - **The ratification register v0.33 is ratified and installed: `doc/RATIFICATION_REGISTER_v0_33.md` (RAT-53, entry
      265).** It is v0.32 with its version line changed and one new section: RAT-41's install to RAT-52, each with
      its entry, review, installed file, commit and hash; the five installs of code in DEV; what is recorded and
      not ratified. Reviewed in EX_316 (DOCUMENTARY PASS); its two clarifications of wording were made at
      installation (`exchange/CLAUDE_WEB_TOOLS/register/v0_33/`, with the candidate, the builder and both differences).
    - **The owner's decision (entry 265, 07:33): `deploy/file_form.py` is infrastructure, installed into every tree**
      (the manifest's `[files]`, class `other`), not a DEV-side install tool. One checker serves DEV's suite,
      `Make_Installable` and `Check_Tree` in DEV, QA and PROD. The reviewer concurs (EX_316): no duplicate module, and
      it is not to be imported into `forecast`-class code.
    - **This edition (RAT-54, entry 268)** was asked for at 07:51 so that a new chat can take over; the reviewer's
      cold read, owed since H-1 v12, now falls on it.
    - **The reviewer's H-2 v8 (RAT-55, entry 268).** At the owner's word the reviewer brought its own handover up
      to date through entry 266 and committed it as a candidate
      (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v8_CANDIDATE_20261125.md`, with its blurb beside it); it differs from
      H-2 v7 in its header and its chapter 0 only. **The owner ratified it and this edition together, 07:58: "both
      chatgpt and claude are ratified now."** The reviewer installs its own final file; when this edition was
      installed only the candidate was on `main`. `exchange/CONTINUITY_NOW.md` names the reviewer handover in force.
      It names H-1 v12 as the Claude handover, which was true at its cutoff; this edition replaces H-1 v12.

14. **(v13) SLICE A OF BUILD STEP 3: EXACTLY WHERE IT STANDS (entries 264 to 266). Working files; not a package; not
    reviewed; nothing installed.** The files are `exchange/CLAUDE_WEB_TOOLS/step3/overlay/`, laid out as they go into
    the tree: eleven files, **all CRLF, and sitting on `main` as it is now** (the conversion changed
    `deploy/INFRA_MANIFEST.ini`; the slice's copy is merged with it).
    - **How to work on it:** clone `main` into a work folder, then
      `bash exchange/CLAUDE_WEB_TOOLS/step3/sync_and_test.sh <clone> <python> <test modules>` copies the overlay in and
      runs the modules. Never run the slice against the repository clone you commit from.
    - **Written and tested:** `src/research/settings.py` (DEV's entries for QA and PROD, and every cross-tree check
      of the deployment design's section 1) and the rewritten `ENVIRONMENT.example.ini`; `src/research/code_identity.py`
      (reads the manifest's `[install_tool]` list); `deploy/install_import_check.py` (the static import check);
      `deploy/install_readiness.py` (the two readiness markers, written CRLF, **and the file-form checker: nothing in
      the wrong form can be marked ready, and reading readiness makes the same check**); `deploy/make_installable.py`,
      `deploy/deploy_command.py` and `Make_Installable.bat`; the manifest, with the `[install_tool]` section and
      `deploy/file_form.py = other` under `[files]`; the tests `tests/test_trees_settings.py` (32) and
      `tests/test_trees_readiness.py` (40).
    - **The cloud's evidence at entry 266** (Claude's, not Windows'): those two modules with `test_file_form` (52),
      `test_research_manifest` (9) and `test_research_identity` (25), 158 tests, all OK in a clone of `main` with the
      overlay; and, read-only in that clone, **all 40 real variants and the real infrastructure (34 files, 5
      install-tool files, the manifest) pass every readiness check, the form check included.** The whole suite has
      not been run with the slice.
    - **STILL TO WRITE, in this order:** (1) `records\INSTALLED_FILES.json` (deployment design section 2: every
      installed software file with its SHA-256, each variant's fingerprint, each status file by name only); (2) the
      check of the environment's digest over the fixed inventory (specification section 13; the engine's
      `environment_digest` exists already; on the owner's PC the inventory is 11,997 files, 150.6 seconds on first
      reading and 5.2 when lately read, TASK_T028); (3) `Check_Tree.bat` (specification section 16; deployment design
      sections 1 and 10: read-only; what is installed, each variant's status, what is ready, any drift, the backup
      ZIPs, locks), **with the checker in it** (the standard's section 6: the files on the tree's list of installed
      files, its `ENVIRONMENT.ini`, every status file, and what the project's programs have written under
      `source_data\`, `results\research\` and `records\`, each by its kind); (4) the launch guard with the process rule
      (deployment design section 9; the build plan's section 4A: the rule and the refusals of the reviewed
      `src\package_tools\process_check.py` are kept, the file is not reused; psutil for every process check but the
      restore's; **every program started from an environment is two processes and counts as one**).
    - **To go to the reviewer with the slice:** the narrow, UNRATIFIED amendment of the deployment design's section
      2 ("standard library only" for the install tools; section 0D item 5); and two readings of the
      specification (a variant may import its own listed files as well as its helpers; the tool itself refuses a
      variant that imports an infrastructure file not classed `forecast`).
    - **What the slice changes in DEV when it is one day installed:** the forecasting-code identity stays as it is
      (no forecast is made again); the derived-code digest changes (`settings.py` and `code_identity.py` are of that
      class), which the engine writes into new lines and compares nowhere.
    - **Two things found on the way, to keep in mind.** `tests/research_fixtures.py`, the engine tests' shared
      helper, writes with Python's default line ending, which is CRLF on the owner's PC and LF in the cloud; it is
      not changed: a test that needs files in their form brings its invented tree to form itself (`bring_to_form`
      and `write_crlf` in `tests/test_trees_readiness.py`). And a test that edits a file "afterwards" must append a
      line in its form, or it tests the form check and not what it means to test.
    - **The plan is unchanged** (`step3/STEP3_BUILD_PLAN_v0_1r1.md`): slice A goes to the reviewer as its own package
      on the owner's word; nothing is installed in DEV until slices A to D have passed and been rehearsed. The
      reviewer has said it will assess the completed package, not each increment. The plan gives slice A's plainer
      parts to Opus and slices B and C to Fable; the owner switches.

15. **(v13) What waits now.** On the reviewer: the cold read of this handover, when the owner asks. On the owner:
    nothing. **On Claude, in order:** the four parts of item 14 still to write; slice A's package and its note;
    slices B, C and D; the joined rehearsal; the one install into DEV; QA, the transition check and PROD, each on
    his go; the operations manual's skeleton after build step 3. **Before any of it, the staged takeover of
    section 0 item 4 if this is a new chat.** Apply item 3 throughout: the simplest safe route is said first.

16. **(v13) Two more lessons, and what changed from H-1 v12.** (i) Fetch `main` immediately before installing a
    handover or a register: the reviewer installed its own H-2 v7 while H-1 v12 was being built, and H-1 v12 had
    to be rebuilt to name it. (j) When the owner asks for something "now" and has ratified a like thing in advance
    the same day, his advance word does not stretch to the next document: ask for it (the register, RAT-53, and
    this edition, RAT-54, each had his own word). **Changed from H-1 v12:** the header; section 0 item 2; this
    section's heading, its first lines, items 1 and 10, and these items 13 to 16 with their table; the line on the
    register in section 4.4; section 12.8 item 5; Appendix B.3 and the last line. Nothing else; sections 1, 2 and
    2A are byte for byte H-1 v12's.

**Identities added in v13** (SHA-256 of the Git content at `HEAD`, computed by the builder):

| File | SHA-256 |
|---|---|
| `doc/RATIFICATION_REGISTER_v0_33.md` | `94cb836c7f8776bb7916793e43591cb98f1575a1767f50a2830b7deb3ef0a2d2` |
| `exchange/EX_316_ChatGPT.md` | `6ba1a5cb8ba2229728c94e98d96d1e2bd6050b99f4e9070d652dcca7ab46f191` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v8_CANDIDATE_20261125.md` | `9b00a49398f8c9585d2eeaa63240d8dc92ca6ff36a7a55b42955bb455340de1c` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v8_CANDIDATE_introductory_blurb_20261125.md` | `9ee90a8af4871484dbea09d2a3ce66de332934316df81e7cfb8a3ceb3a8240b2` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v12.md` | `41a20b7ddac9fee4fcb4ed2e5592c8dafafa8b50b1cf2dae9e2c8a91deaa29cd` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v12_introductory_blurb.md` | `ed150c814e392203d380124023692a7d60af714ec08b76e758c87bb5371f38c0` |
| `exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md` | `6eb18f0e38279a9b68e88dec304dbea205a64b62bc8e80bfc8dc9723c39b3195` |
| `exchange/CLAUDE_WEB_TOOLS/step3/sync_and_test.sh` | `13b2d077eb2c360119c72815df79b4b96efdc5325787b80e9a822a7e8fcc5a15` |
| `exchange/CLAUDE_WEB_TOOLS/step3/overlay/ENVIRONMENT.example.ini` | `f272d82d4cd7d8635a226eca8e81210c34fa0f2190963a22063dfdfca80ea67e` |
| `exchange/CLAUDE_WEB_TOOLS/step3/overlay/Make_Installable.bat` | `0ad61482d82d7ff41d5656e2bf981ae39f487afd9a5f8289baf5ed4d2880d758` |
| `exchange/CLAUDE_WEB_TOOLS/step3/overlay/deploy/INFRA_MANIFEST.ini` | `6c80656fc99b1958ee6a6c1cf4825c27c5f515772d537b99d1aac992ed55664e` |
| `exchange/CLAUDE_WEB_TOOLS/step3/overlay/deploy/deploy_command.py` | `f5d1255eead9ab0c1322cabd623f11ea1ed55200fed33c8e2f62d3bcac8bc401` |
| `exchange/CLAUDE_WEB_TOOLS/step3/overlay/deploy/install_import_check.py` | `425121bcd439e7b5dce9b5eac7c11d35e62cf45c2ce3a679042e28401214741e` |
| `exchange/CLAUDE_WEB_TOOLS/step3/overlay/deploy/install_readiness.py` | `0bee38df8053910c4a2125d16292b3f04ef8c427f9c9cc5eecea9f689b6f5cd7` |
| `exchange/CLAUDE_WEB_TOOLS/step3/overlay/deploy/make_installable.py` | `90a50b43e0decf4a484849145d90fd78ed5b155ef3211dc7d01eecffda2b84b2` |
| `exchange/CLAUDE_WEB_TOOLS/step3/overlay/src/research/code_identity.py` | `01b97b4e9f309433af150ce367968561f2cda63c720f0296295d0ff1be9527be` |
| `exchange/CLAUDE_WEB_TOOLS/step3/overlay/src/research/settings.py` | `8fb85b95714cd4692939d5a678df5742ad96864dd5bf2bac192954f01955545b` |
| `exchange/CLAUDE_WEB_TOOLS/step3/overlay/tests/test_trees_readiness.py` | `00211eb4ad903969103172daea736a52fbfaca81325ec489022ab3414d525621` |
| `exchange/CLAUDE_WEB_TOOLS/step3/overlay/tests/test_trees_settings.py` | `48cf4b9d1384ace2dc92b9ace85f0d53a2da2bb27b8dd028ae83ba4386815cc6` |

**Identities added at this edition** (SHA-256 of the Git content at `HEAD`, computed by the builder):

| File | SHA-256 |
|---|---|
| `doc/FILE_FORM_STANDARD_v0_2.md` | `73d52529d52e743b16942ffada69df239d72cc019844f4c73476d6d38db1e680` |
| `.gitattributes` | `f0fe9c68753286cb2e20f03b80c6ca0be2cc165682e94951e7f2e3e513c8dc47` |
| `deploy/file_form.py` | `0d7738e542baae2be92982ff2a3981519b40cd8da554d5c50958dd1a55119cc5` |
| `src/research/windows_text.py` | `243d246c37ffd3ef61a8412cc98b39fde34f80fd19d96e7883d4d177597fc244` |
| `src/research/job_lock.py` | `efe8419e5927d87207fc39de0b97519c86b0b4a01f533b5751b6a6f54bc7853f` |
| `exchange/CLAUDE_WEB_TOOLS/conversion/package/FILE_FORM_Conversion_v2.zip` | `ca5816cb85813de1df88fbeaf37097c6bd2126fa59f0d3a36f7927783f1c091c` |
| `exchange/CLAUDE_WEB_TOOLS/conversion/package/FILE_FORM_Conversion_v2/CONVERSION_LIST.json` | `40abea55b09e13f341f056a43596c334e10ef462563715c42a850175a919f2f4` |
| `exchange/CLAUDE_WEB_TOOLS/conversion/package/FILE_FORM_Conversion_v2/INSTALL_AND_RUN_SHEET.md` | `25968638311354b0547e849f404c71bbd12b187475f7a4f6ba1bbc695f59702b` |
| `exchange/CLAUDE_WEB_TOOLS/conversion/package/FILE_FORM_Conversion_v2_REVIEW_NOTE.md` | `fee612117f3cf84526b0b5c61350116ae73c6ff32d13d98a93a1fcf85c791d2d` |
| `exchange/CLAUDE_WEB_TOOLS/conversion/day_result/OWNERS_WINDOWS_20261124_25.txt` | `5f28662e22ae61221df8a04b73df97937de15ebbf03d46eaf61662df21c8843a` |
| `exchange/CLAUDE_WEB_TOOLS/lock_fix/package/FILE_FORM_Lock_Fix_v1.zip` | `744efbd3ca1ea70162d6c1dcae060836e9326625299f9116b5ac2dbb19e20318` |
| `exchange/EX_312_ChatGPT.md` | `576973db292927b868e586c2bfed6d083aad4783d474a01be20a9dadfdf44145` |
| `exchange/EX_313_ChatGPT.md` | `0884eb2a475442838a7783dcbbbdfe22e9e317c08f8c7ef7a9bfb24224e5fda9` |
| `exchange/EX_314_ChatGPT.md` | `c7beffa62ffc18b9b841fbd254af8a2006e4112c019bcdee2929fa27581f82e1` |
| `exchange/EX_315_ChatGPT.md` | `d1710c07770a5df5dd3586db227e669fcf7be26bc0a7be8b55cd98ae713b9de3` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v7_20261125.md` | `a954efc6caf0109f6575869326ed548d86b747dda9ad7c20e343e8037cc7058b` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v7_introductory_blurb_20261125.md` | `20c4fd217a881ea98765db9d079eed632b98ad4a962ebf5f916b29c6e1ce70b7` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v11.md` | `91a9c1814587bcbe0ee9ce23de51a6ed5008932d4c721e9f52c0467930c09318` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v11_introductory_blurb.md` | `16d7feedc6102bc87e62d5e6d4a464a38013ffd6f8e2262d0a80320387d9b5ec` |

End of H-1 v15.
