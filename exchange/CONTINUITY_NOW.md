# CONTINUITY NOW - the one page that lets a new chat take over

Living page (P0 and P3, adopted 14 November 2026). Updated in place by the Claude web chat after every milestone; Git
keeps the history. It is a recovery index, not a handover, and grants no permission; the installed handovers and the
durable EX messages are authoritative.

**Last updated:** 20 November 2026, 16:40 Australia/Adelaide (EX_250: a narrow RECHECK with the owner's new backup and recovery decisions, entries 112 and 113; the design note DRAFT v0.3 sent as EX_251, entry 114). **Next: the reviewer's focused recheck (EX_252); then the owner's ratification; then H-1 v8 and a new Claude chat for the code round, on its own go. No code.**

## For the owner: NOW

- **THE DEPLOYMENT DESIGN NOTE, DRAFT v0.3, IS WITH THE REVIEWER FOR ITS FOCUSED RECHECK (entries 112 to 114; 20 November
  2026).** EX_250 accepted v0.2's corrections in principle and carried the owner's new decisions: full snapshots with
  `.venv`; a plain same-path restore; PRE and POST deployment snapshots; a recovery kit zip on T: so that a restore
  needs neither E: nor a working production folder. The owner then decided A to G and H1 (production's environment
  built his way and verified by the suite) and "no Python at all" for a restore (entries 112, 113). v0.3:
  `exchange/CLAUDE_WEB_TOOLS/mhupb/deploy/MHUPB_DEPLOYMENT_DESIGN_NOTE_DRAFT_v0_3.md`; sent as
  `exchange/EX_251_Claude.md`; the reply will be EX_252. **Then the owner's ratification** (it covers the amendment to
  the orphan-marker rule, the note's section 8). **Then, as the owner agreed on 20 November: H-1 v8 first, and the
  code round in a NEW Claude chat on its own go.** The go for the early File Explorer check (E) is not given.
  No code, package, Windows step, install, snapshot, restore or run is authorised. v0.1, v0.2 are history.
- **THE DEPLOYMENT DESIGN NOTE, DRAFT v0.2, IS WITH THE REVIEWER FOR ITS RECHECK (entries 110, 111; 20 November 2026).**
  EX_248 was RECHECK with six findings (B01 to B06), all accepted. The owner confirmed nine choices (entry 110: no
  `.venv` in snapshots; the flag before a job's first write; all jobs go on with a standing warning when a snapshot
  cannot be made; a stale orphan marker neither blocks a restore nor is copied back; formal OV-1 reported truthfully;
  a path-checked guard; `restore` as a fifth mode; `G:\a_p_r_i_r`; `T:\a_p_r_i_r_backups`). v0.2:
  `exchange/CLAUDE_WEB_TOOLS/mhupb/deploy/MHUPB_DEPLOYMENT_DESIGN_NOTE_DRAFT_v0_2.md`; sent as
  `exchange/EX_249_Claude.md`; the reply will be EX_250. **Then the owner: five choices (note section 15, A to E) and
  ratification.** No code, package, Windows step, install, restore or run is authorised. v0.1 and EX_247 are history.
- **THE DEPLOYMENT DESIGN NOTE IS WITH THE REVIEWER (entries 107, 108; 20 November 2026).** The owner's go (19 November,
  23:50) covered the design note only. Draft v0.1: `exchange/CLAUDE_WEB_TOOLS/mhupb/deploy/MHUPB_DEPLOYMENT_DESIGN_NOTE_DRAFT_v0_1.md`;
  sent as `exchange/EX_247_Claude.md`; the reviewer's reply will be EX_248. **Waiting on the reviewer's design review;
  then on the owner: seven choices (note section 15), two folder names, and ratification.** No code, package, task
  file, Windows step, install, restore or run is authorised. The Fable task is finished (Opus until the review).
- **RAT-39 (entry 106, 19 November 2026, 23:25): H-1 v7r1 RATIFIED AND INSTALLED** after the reviewer's PASS:
  `doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md` (SHA-256 `6f968eef...771c97cd`; status line finalised) and its blurb
  (`76be41b0...d41992a6`). It is the installed Claude handover; H-1 v6 is history. **Nothing else is authorised: the
  deployment design note still needs the owner's go** (Claude will suggest Fable (High)). Section 12.3's leftover
  sentence is for the next edition.
- **(History) H-1 v7r1 CANDIDATE (23:12): the one to ratify.** The reviewer supported v7 and asked (relayed by the owner at 23:11)
  for two narrow corrections only: section 0 steps 1 and 3 (the obsolete prohibition on reading `source_data/` and
  records removed, RAT-34) and section 7.5 (the updater has run live once per game). Files:
  `exchange/CLAUDE_WEB_TOOLS/h1v7/out_r1/` (builder `make_h1_v7r1.py`; diff `H1_v7_TO_v7r1.diff`, 18 lines). The owner
  intends to ratify it.
- **H-1 v7 CANDIDATE (19 November 2026; entry 105)** in `exchange/CLAUDE_WEB_TOOLS/h1v7/out/` (builder `make_h1_v7.py`, the
  diffs from v6 beside it): a full edition from H-1 v6's ratified bytes folding in everything decided since v6 (its
  section 0B item 13 and Appendix B). Superseded by v7r1 before ratification; never ratified. Not a prerequisite to the deployment design note.
- **The owner's decisions of 19 November 2026, evening:** test on **Python 3.15 only**, the routine 3.13 runs dropped,
  risk accepted (entry 103); **no monthly restore test** (entry 104; the one restore T017 rehearses stays); **no
  comparison of a replay with the originals**, which a catch-up cannot do either (entry 105).
- **HO-2 TAKEOVER ACCEPTED; NORMAL WORK AUTHORISED (entry 102, 19 November 2026, 06:31).** The new Claude chat started at
  about 06:04 from H-1 v6's blurb (`de1aa3e`): first reply `exchange/EX_245_Claude.md`; the reviewer's five questions;
  blind answers `exchange/EX_246_Claude.md`; the reviewer's PASS on all five, relayed by the owner. Claude's commit
  rights are as before. **NOT a go for:** the deployment design note, deployment code, the integrated package, T017,
  any install, `declare-developed`, OV-1's registration or any real-data run. **Next: the owner's go for the deployment
  design note** (Claude will suggest Fable (High)). H-1 v7 at a convenient point; not a prerequisite.
- **RAT-38 (entry 101): H-1 v6 and its blurb RATIFIED AS THEY STAND**, now in `doc/HANDOVER/`
  (`Claude_Primary_Handover_H1_v6.md`, SHA-256 `6dc8185a...e280353`; blurb `d78249b9...7c47c`). Bytes unchanged: its
  header still says CANDIDATE, which is frozen history (as for H-2 v3r4). The owner wants the latest decisions folded
  in at the earliest convenient time (the next full edition, H-1 v7, and the package's document amendments).
- **EX_244 GOVERNS RESTORE AND REPLAY (entry 101; the owner with the reviewer, 18 November 2026, after H-1 v6 was
  written):** a full restore from a verified snapshot followed by N-1 walk-forward replay, with OV-1's numbers
  recomputed, is valid research; no automatic research STOP and no prospective-evidence reconstruction because an older
  backup was restored; the FORMAL registered OV-1 guarantee keeps its own assumptions, which never block ordinary
  research computations. It takes precedence over older restore guidance in the handovers (H-1 v6 section 12.11
  included). The reviewer's H-2 v3r5 candidate was superseded by its H-2 v3r6 candidate (`de1aa3e`); H-2 v3r4 (RAT-36)
  stays operative.
- **THE OWNER'S RESTORE DECISION (entry 100, 19 November 2026, 06:16):** "rename the old code/data folder tree and
  restore afresh into a fresh \"standard\" empty tree": the old production tree is renamed aside (kept, never
  deleted) and the snapshot unpacked into a new, empty tree at the standard production path. Details are for the
  deployment design note; a restore is a step on the owner's own go.
- **MODE H IS COMPLETE AND READ.** Oz Lotto SEALED 15 November 2026 (EX_196); Powerball SEALED 16 November 2026 (EX_199).
  Both AIs read both reports independently and agree (EX_200 to EX_205; "EX_203" in EX_204 and entry 40 means EX_203A).
  **No statistically significant predictive advantage was demonstrated under the predeclared Mode H tests** (Bonferroni
  family-adjusted P 1.000, 0.672, 0.920). The record of the study is in register v0.31 (from EX_205 section 5). The
  development walk-forward evaluation (26,040 forecasts) also showed nothing significant. D5 done: the owner committed the
  results at `c7622fa`.
- **THE APPROACH OF 16 NOVEMBER 2026 IS IN FORCE (RAT-34, 17 November, about 15:15; entry 63),** with the reviewer's EX_206
  conditions: all draws are treated the same and the AI chats may read draw values, the masters and the results; no lottery
  websites or results searches by any AI; results count only from the reviewed programs and logged runs (chat calculations
  are "suggestive"); N-1 isolation, forecast identities and append-only evidence kept; known draws give development
  evidence only; the sealed Mode H records are never altered or rescored; nothing runs without the owner's go. Claude
  commits reviewed and ratified documents directly; code still goes by reviewed package, Windows rehearsal and the owner's
  install; Claude never writes `source_data/`, `results/`, `transitory_data/`, `GAIS/` or settings; nothing is deleted.
  The reviewer commits its own replies to `exchange/`. The local runner keeps rulebook v0.5, rules 4 and 5 included, until
  MHUP-B's rulebook edition. Record: `exchange/DECISIONS/AGREED_APPROACH_2026_11_16.md`; register v0.31.
- **THE MHUP-B DESIGN IS RATIFIED (RAT-33, 17 November, 14:48; entry 61):** `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_7.md`
  (SHA-256 `04c4f68a...3d26`; reviews EX_207 to EX_213). Full MHUP-B in eight tested layers, the live path isolated; a league
  table of every method and variant with `current` and archive folders; re-forecasting of every draw up to the holdout's end
  by every variant as development evidence, the sealed Mode H records kept as separate history; OV-1, one exact evidence
  score per game (bar 40), registered before its first draw, the only confirmatory forward test. **Design only: no code,
  run or install.** O-4 (scoring Powerball 1145-1285) is an approved objective; its run needs its own go.
- **Installed documents (RAT-34, committed by Claude, verified from a fresh clone):** register v0.31, H-1 v4 and its blurb,
  and the supplement. H-2: v2 r1 stays installed; the reviewer updates its H-2 v3 candidate for a separate ratification.
- **THE CLAUDE HANDOVER IS DONE (HO-2; entry 64).** A fresh Claude chat took over on 17 November 2026 from H-1 v4: first
  reply EX_216, the reviewer's five blind questions EX_217, the answers EX_218, **EX_219: TAKEOVER PASS**. The owner
  authorised normal work at 16:01.
- **History (the plan stage, now complete):** the code plan went to the reviewer as EX_220 (entry 65). Draft v0.1:
  `exchange/CLAUDE_WEB_TOOLS/mhupb/codeplan/MHUPB_CODE_PLAN_DRAFT_v0_1.md`, with the OV-1 numerical probe and the evidence
  beside it. The condition of entry 67 (review, OD-1 to OD-6, ratification, then a specific go for code) was met by
  RAT-35 (entry 74) and the owner's code go (entry 75).
- **History:** EX_223 (supersedes EX_221 and EX_222): PASS WITH REQUIRED CORRECTIONS (B01-B04, C01-C04), answered by
  plan v0.2 and supplement v0.8 (EX_224 to EX_227), ratified as RAT-35.
- **OD-1 TO OD-6 ARE ALL AGREED BY THE OWNER (entries 69 and 70), as directions:** OD-1 two kinds of development run
  (routine fill; exploratory rerun); OD-2 a missed week counts as a neutral factor of 1 under a rule fixed in advance
  and blind to the outcome (else stop); OD-3 noon Adelaide time as the last moment for OV-1's pre-draw entry (the owner:
  both games close at 7.30pm AEST); OD-4 a stopped stream stays stopped; OD-5 the real score records checked before the
  install: the owner committed them (`cc665ce`) and Claude's census passed; OD-6 three review slices, one install.
- **RAT-35 (17 November, 20:06; entry 74): THE MHUP-B CODE PLAN v0.3 AND DESIGN SUPPLEMENT v0.8 ARE RATIFIED** (reviews
  EX_223, EX_225, EX_227 PASS). Installed in `doc/`: `Predictive_Randomness_MHUPB_Code_Plan_v0_3.md` (SHA-256
  `d5c2b318...546d0169`) and `Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md` (SHA-256 `e3d977e1...9be97c27e`),
  byte for byte the candidates; v0.8 governs, v0.7 is history. Includes O-5 (the 01:30 UTC cut-off, a conservative
  choice), O-6, O-7.
- **THE OWNER GAVE THE GO FOR CODE (17 November, 20:09; entry 75).** Order: slice 1 (baseline fixes, L1 to L3), slice 2
  (L5, L6), slice 3 (L4, L7, L8), the integrated package and document amendments, T017, the install. Slices 1 and 2 are
  Fable (High) work; slice 3 and packaging are Opus work.
- **SLICE 1 PASSED THE REVIEWER'S SOURCE REVIEW (EX_231; entry 79).** History: EX_228 (first edition), EX_229 (four
  corrections), EX_230 (corrected), EX_231 (PASS, with the small note N-231-1, since applied). Files:
  `exchange/CLAUDE_WEB_TOOLS/mhupb/slice1/` (MHUP-A layout). NOT INSTALLED. Rebuild with the commands in EX_228 section 1.
- **THE OWNER'S CLARIFIED MODEL (18 November; entry 84; EX_235 governs, with EX_234 and EX_233 where not superseded).**
  All draws equal (the former holdout draws are ordinary draws; the Mode H seal is an archive, never a gate in normal
  work); every method version its own identity, old versions kept; catch-up is the same N-1 walk-forward; two
  labelled OV-1 uses (formal prospective, bar 40; retrospective diagnostic, descriptive, in slice 3's report).
  This changes parts of supplement v0.8 (6.7; 7.2 rules 1 to 3) and plan v0.3 (L6 gates); the change note is
  `exchange/DECISIONS/OWNER_CLARIFICATION_2026_11_18_EQUAL_DRAWS_AND_OV1_USES.md`; the amendments travel with the package.
- **SLICE 2 PASSED: EX_237 (entry 86), the reviewer's focused source-review PASS of the corrected edition EX_236.**
  Files: `exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/`. NOT INSTALLED. 700 tests, 0 failing, on both Pythons (Claude's runs);
  101 planted defects caught; tree digest `000dc4ae...7a581241d`. Two installed archive checks were left on purpose and
  are to be re-evaluated when the integrated package is planned (EX_237 section 2).
- **The reviewer chat changed on 18 November 2026 (about 11:00);** the new one took over from H-2 v3r3 and refreshed its
  handover to H-2 v3r4 (`d5e810c`), **which the owner ratified (RAT-36; EX_238; entry 87).**
- **SLICE 3 PASSED: EX_242 (entry 91), the reviewer's focused recheck of the corrected edition EX_241. All three slices
  have now passed source review (EX_231, EX_237, EX_242).** L4 the league table, L7 the weekly report with
  the two labelled OV-1 views, L8 the two sequencers and launchers. History: EX_239 (first edition, entry 89); EX_240
  (review: structure accepted, the five questions answered and the choices kept, three narrow corrections F3-01 to
  F3-03); EX_241 (the three applied). Files: `exchange/CLAUDE_WEB_TOOLS/mhupb/slice3/` (README there). NOT INSTALLED.
  758 tests in 55 modules, 0 failing, on both Pythons (Claude's runs); 106 planted defects caught; tree digest
  `ef2b67e0...1f50e9d13`. **NEXT: the integrated package. THE OWNER HAS NOT GIVEN ITS GO: he wants to discuss it first (entry 92).**
- **DECIDED BY THE OWNER, 18 November 2026, evening (entries 93 to 98; `exchange/EX_243_Claude.md` is the record for the
  reviewer, table D1 to D12): where production runs.** Production gets its own folder on his G: drive with NO Git in it
  at all (OFF-1); development, Git and GitHub stay in the clone on E:. Code reaches production only through one small,
  re-runnable deploy tool (outline: `check`, `init`, `update`, `export`). A marker file makes real-data commands refuse
  anywhere else. A verified `.zip` snapshot (Python's `zipfile`; to T:, a setting) at the END of every production job;
  a missed one is made first by the next job; rollback = restore from backup. **Build it clean, once: nothing is
  installed or deployed now and changed later.** None of it is designed yet.
- **THE ORDER NOW (entry 98; steps 1 to 3 done by 19 November, 06:20):** (1) done: EX_243 to the reviewer (its
  replies: H-2 v3r5, EX_244, H-2 v3r6); (2) done: the reviewer's H-2 candidate (v3r6; not yet ratified);
  (3) done: H-1 v6 ratified (RAT-38) and a NEW CLAUDE CHAT started and accepted (EX_245, EX_246; entry 102); (4) the new chat's first real task, on the owner's go: the deployment design note (Fable (High)),
  to the reviewer before any code; (5) the deployment layer, reviewed like a slice; (6) the integrated package; (7)
  T017; (8) the first deployment. **No go has been given for the design note or the package.**
- **Done (entry 99, 18 November 2026, 23:31):** on the owner's word, the ratified bytes of
  `doc/HANDOVER/Claude_Primary_Handover_H1_v4_introductory_blurb.md` were restored by a forward commit (his commit
  `86f6c43` had changed it, apparently by accident); SHA-256 `2cfa6cf5...67be`, as recorded at RAT-34.
- **DECIDED BY THE OWNER (entry 92): the package removes the two installed Mode H archive checks** (the results reader's
  opening-record condition at or above the former holdout; the diagnostic route's opening and seal conditions).
- **SLICE 2, FIRST EDITION: EX_232 (entry 83)**, reviewed in EX_233 (kernel proofs accepted; S2-F01 withdrawn later;
  S2-F02 stood). Superseded by EX_236.
- **Slice 2, first edition, as recorded then: EX_232 (entry 83).** Files:
  `exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/` (README there). NOT INSTALLED. 694 tests, 0 failing, on both Pythons;
  94 planted defects caught; tree digest `887731e1...4bedabc4`. EX_232 section 6 lists what was built lean or moved
  to slice 3, and section 7 six questions for the reviewer. The Fable task (slice 2) is finished: Opus is enough
  until the reviewer replies.
- **NEXT: slice 3** (L4 league table, L7 report, L8 sequencers; Opus) on the
  owner's go; slices are serial. Slice 3 must: connect `ov1.publication_names` to the league manifests; write
  `LEAGUE_SOURCES_<GAME>.json` in the shape `score_identities.league_sources` reads; add OV-1's measure-registry
  entry; run `Method_OV1.py record` after every score and at once on FROZE_NEXT, reading its state line and not only
  its exit code; admit existing attempts before any routine fill, verifying complete report records; build the two
  labelled OV-1 views in the report (formal; retrospective, descriptive, same kernel, never the formal ledger). Owner's standing rule (entry 80): no over-engineering of side issues; add a guard, test
  or feature only if its absence could change a result, invalidate the evidence or break his weekly use. No change to
  his PC's date, time or zone (entry 78); no further daylight-saving work.
- **Joint working principle (entry 81), agreed by Claude and the reviewer on the owner's text:**
  `exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md`. READ IT BEFORE BUILDING OR REVIEWING.
  The science, the methods, the calculations and the reporting must be right; effort on side issues is kept
  proportionate. Whoever proposes extra work states the concrete failure and consequence. A ratified item is
  built in its simplest satisfying version and noted in the covering note. For slice 2 the missed-week rule is
  part of OV-1's validity (correct and sufficiently tested, no recovery machinery).
- **The test baseline on current `main` (EX_219 C2), cloud only:** 570 tests run in 45 modules on Python 3.13 and 3.15
  (E2R-T12 left out); exactly two fail, both in `tests/test_multigame_reader_contracts.py`, both the expected ones tied to
  the version-1 masters (F-2). T024's 571 is dated history. No Windows baseline at the current state exists yet (T017).
  From `cc665ce` a third test fails, known: `tests/test_mhupa_launchers.py` `test_gitignore_lines` (the owner commented
  out an ignore line that the test requires; fixed with the package, entry 70).
- **Blocks or STOPs:** none.

## Reviewer status

- **The reviewer may commit its own EX replies to `exchange/` and its H-2 files to `doc/HANDOVER/`** (owner, entries 50 and
  56). Fetch before reading or numbering anything; never edit its files.
- Open findings: none. Latest reviews: EX_213 (MHUP-B design pass), EX_215 (RAT-34 documentary pass), EX_219 (HO-2 takeover
  PASS; cautions C1 and C2 for the code plan). Since then: EX_223, EX_225 and EX_227 (code plan, PASS), EX_229 (slice 1 corrections), EX_231 (slice 1 PASS; N-231-1
  applied). EX_233 (slice 2 review), EX_234 and EX_235 (the owner's clarified model). EX_237 (slice 2 PASS). EX_240 to EX_242 (slice 3; PASS). EX_244 (restore and replay; governs, entry 101). The new Claude chat's takeover: EX_245, EX_246, PASS relayed by the owner (entry 102). EX_248 (the design note v0.1: RECHECK, B01 to B06). EX_250 (v0.2: narrow RECHECK, R3-C01 and R3-C02). **Awaited: the focused R-3 recheck of the design note v0.3 (EX_251; its reply EX_252).** The joint working principle (entry 81) was agreed by chat
  paste, with no EX number. (EX_177 B01 closed 14 November by the owner's scoped W-23 acceptance; never "W-23 PASS".)
- EX_196 (Oz Lotto) and EX_199 (Powerball): PASS WITH EVIDENCE LIMITATIONS; nothing blocking. EX_199 C01 closed (entry 37).
- Evidence limits: Windows results (T016, T023, T024) are runner reports, not reproduced by either AI; the live PC state
  (untracked files, running processes, the sealed local artifacts) is owner-reported.
- Latest reviewer messages: EX_191 (H-1 v3 and register v0.30: PASS WITH CORRECTIONS; no H-2 edition needed), EX_193 and EX_198 (the streamlined arrangement, each game), EX_195 (page check r2), EX_196 and EX_199 (the two audits), EX_200 (independent reading of both reports: primary family results null in both games). EX_203A (pasted assessment of EX_201: AGREE, three nonblocking qualifications; the development evidence to be recognised, kept separate), EX_203 (reply to EX_202: Q1 accept with wording precision, Q2 retain with further qualification, Q3 agree).

## If a chat ends

- **Claude chat ended:** start a new Claude chat by pasting the blurb of the installed handover, H-1 v7r1 (RAT-39):
  `doc/HANDOVER/Claude_Primary_Handover_H1_v7r1_introductory_blurb.md`. Fill in its last lines (the commit, the date and
  "see exchange/CONTINUITY_NOW.md"). The new chat reads H-1 v7r1's section 0B first (items 12 and 13 above all), then the
  decision log from entry 99 on.
- **ChatGPT reviewer chat ended:** the operative reviewer handover is **H-2 v3r4**, ratified by the owner (RAT-36; entry
  87): `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r4_RATIFICATION_CANDIDATE_20261118.md` (the word CANDIDATE in its name
  is frozen history). Point the new reviewer chat straight at that full file, then at `exchange/CONTINUITY_NOW.md` and
  the newest EX messages. The separate H-2 blurbs (v3, v3r3) were not ratified and are older; H-2 v2 r1 is history.

## Resuming the MHUP-B slice work (for a new Claude chat)

- **What governs:** `doc/Predictive_Randomness_MHUPB_Code_Plan_v0_3.md` (L5 section 5 and section 6 for OV-1; L6 section 5;
  sections 7, 9, 13, 14) and `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md` (6.5 and 6.8 for OV-1), with the
  design `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md`. Apply the working principle (entry 81).
- **Where the code is:** slice 1 in full at `exchange/CLAUDE_WEB_TOOLS/mhupb/slice1/` (README, `WORKING_NOTES.md`, the
  edit scripts, the new files by final path in `slice1_new/`, the suite runner, the mutation tool, the evidence). Nothing
  is installed; `src/` and `tests/` on `main` are as at `cc0ab73`. The cloud workspace of an ended chat is gone: rebuild
  from the repository. Slice 2 goes in `exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/` in the same layout, built on top of
  slice 1's tree (never in `src/` or `tests/` on `main`).
- **Rebuild and test (cloud, from the repository root):**
  `git clone <repo> base`, then
  `sh exchange/CLAUDE_WEB_TOOLS/mhupb/slice1/build_dev_slice1.sh base dev exchange/CLAUDE_WEB_TOOLS/mhupb/slice1`,
  `python3 -I exchange/CLAUDE_WEB_TOOLS/mhupb/slice1/run_suite.py dev OUT 2` (one module per process, without class
  `T12Determinism`), and `python3 -I exchange/CLAUDE_WEB_TOOLS/mhupb/slice1/mutations_slice1.py <a separate copy of dev>`.
  The interpreter (Python 3.15 only, entry 103; the earlier 3.13 runs are history): `uv python install 3.15` then `uv venv --python 3.15 venv315` and
  `uv pip install --python venv315 numpy scipy psutil requests beautifulsoup4 selenium`; run the suite with
  `venv315/bin/python -I`. Use absolute paths in the build script's arguments.
- **Last known results:** EX_230's tree 623 tests, 0 failing on 3.13.18 and 3.15.0b4, 57 mutants caught, digest
  `14d07246...596c8017a`. After N-231-1 only the two weekly modules (46 tests) were rerun, both Pythons pass, and the new
  mutant is caught; slice 2's submission carries the full-suite run.
- **Slice 2 is built and submitted (EX_232):** `exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/` with its README. Rebuild:
  `sh exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/build_dev_slice2.sh base dev exchange/CLAUDE_WEB_TOOLS/mhupb/slice1
  exchange/CLAUDE_WEB_TOOLS/mhupb/slice2`; the suite with slice 1's `run_suite.py`; the planted defects with
  `mutations_slice2.py` on a separate copy of the tree. Corrections after the review go into that folder's tools
  (`apply_slice2.py`, `slice2_new/`), never into `src/` or `tests/` on `main`. Slice 3 goes in `slice3/`, built on
  top of slice 2's tree. Next free EX number after `git fetch`: EX_244 at the time of writing.

## Installed handovers (authoritative)

**H-1 v7r1 (Claude; RAT-39, entry 106; `doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md`, SHA-256 `6f968eef...771c97cd`,
committed by Claude on 19 November 2026 after the reviewer's PASS; status line finalised)** and **H-2 v3r4 (reviewer; RAT-36,
entry 87; `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r4_RATIFICATION_CANDIDATE_20261118.md`, blob `6477493d`)**, with
register v0.31 (`doc/RATIFICATION_REGISTER_v0_31.md`; RAT-35 to RAT-39 are in the decision log, for register
v0.32). H-1 v6 (RAT-38, header CANDIDATE as frozen history), H-1 v5 (RAT-37), H-1 v4 (RAT-34), H-2 v2 r1 (RAT-31), H-1 v3 and register v0.30 stay as history. The `h1v5/out/` candidate files
are frozen. The `h1v6/out/` candidate files are frozen too. The reviewer's H-2 v3r6 is a CANDIDATE
(`de1aa3e`), not ratified; H-2 v3r5 was superseded by it.

## Working approach adopted 14 November 2026 (P0-P6)

EX_182 as modified by EX_183, agreed in EX_184; decision log entry 1. In short: decide by effect (level 1 owner decides
after review: science, safety, `src/`, packages, real data, Mode H; level 2 reviewed, still needs its own go; level 3
cosmetic or routine author choices only); one decisions log; this one NOW page; living drafts, but a procedure used for
a real step is fixed and re-reviewed if changed; an ideas backlog after Mode H; and at each substantial milestone a short
independent "how the process went" note from each AI, with reasoning and alternatives. Reviewer rights unchanged.

## Changes since the installed handovers (all committed)

- Owner dependency change cc0ab73; TASK_T024 PASS (ENV PASS, 571 tests); new environment digest 5bf4eb8a36dd...
  (H-1 v2 still quotes the older 966a2792...; readiness sheet r2c has the new one).
- EX_176-EX_177: PASS WITH CORRECTIONS. C01 applied (sheet r2c). C02 closed by the owner without a pip check. B01 closed (scoped W-23 acceptance).
- The old ChatGPT reviewer chat ended; the replacement took over (EX_178-EX_180: 12 of 12) and was accepted by the owner.
- D1-D7 decided as recommended (exchange/DECISIONS/OWNER_DECISIONS_2026_11_14b_C02_AND_REVIEWER.md); EX_181 agreed.
- Working approach P0-P6 adopted (EX_182-EX_184; exchange/DECISIONS/DECISION_LOG.md).
- OUTLANDISH_01's methods join the method backlog, probably first among the methods still to do, through this project's
  normal route (decision log entry 3).
- The owner works on OUTLANDISH_01 in GAIS/, committing with `git add GAIS/OUTLANDISH_01/`; no further package installs
  planned (he will ask Claude first).

## Mode H state

Both games SEALED (Oz Lotto 15 November 19:54; Powerball 16 November 20:53) and read (EX_200 to EX_205). The sealed studies
are never reopened, rescored or edited. The freeze has ended. D5 is done (entry 48, commit `c7622fa`). Q7 (no raw draw value in an AI chat) is replaced by the agreed approach of 16 November, which
the reviewer has still to be consulted on. The two Mode H report files' SHA-256 values are in entry 38; the reading tools
are in `exchange/CLAUDE_WEB_TOOLS/modeh_reading/`.

## Full order from here

1. Done: Mode H, the readings, D5, the approach of 16 November (in force), the MHUP-B design (RAT-33), register v0.31 and
   H-1 v4 (RAT-34), the holdout exposure record closed.
2. Done 17 November: the handover to a fresh Claude chat (EX_216 to EX_219; entry 64).
3. **MHUP-B code.** Plan done (RAT-35). Slice 1 done (EX_231 PASS). Slice 2 done (EX_237 PASS). **Slice 3 done (EX_242 PASS; entry 91).** Next, on the owner's
   go: After its acceptance, on the owner's go: the integrated package with the document amendments (plan section 11), the Windows
   rehearsal T017 (with a full-suite run after step 18; no change to the PC's clock), the owner's install, the
   registration of OV-1 before its first forward draw, and the runs, each on its own go.
4. Done 18 November: the reviewer's H-2 v3r4 ratified (RAT-36); H-1 v5 ratified (RAT-37).
5. Then WF-1C, then the methods still to do (OUTLANDISH_01 probably first).
