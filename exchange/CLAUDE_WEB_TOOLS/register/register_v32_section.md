## RAT-34 installed, the MHUP-B plan and slices, the owner's course correction, and the new system ratified as RAT-40 (register v0.32)

Paths in this section are from the repository root. In this section, "this register" means register v0.32. Every commit named
here was checked by Claude from GitHub, and every hash was computed from Git's stored bytes. This section records decisions
already taken and events that happened; it makes no new decision, and nothing in it authorises code, a check, a run, a
package or an install. It is kept short on purpose: the owner's exact words and the detail of each event are in
`exchange/DECISIONS/DECISION_LOG.md`, entries 62 to 150, which this section indexes.

**The position at this edition (read this first).**
- **A new system is ratified and not yet coded.** On 22 November 2026 the owner ratified the system specification v0.6 and
  the deployment design v0.12 (RAT-40). With `doc/CODING_PRACTICES_v0_1.md` they are the authority for the active system.
  They replace the weekly-session design (MHUP-B) as the thing to be built.
- **The installed code is the old system, unchanged.** No file under `src/` or `tests/`, no root `.bat` and no
  `requirements.txt` has changed since `cc0ab73` (14 November 2026). No code package was installed in the period of this
  section, and the decision log records no real-data run, results update or report run in it. Both masters are at
  version 2, as register v0.31 records.
- **Mode H stays complete and sealed in both games.** Its records are never altered, rerun or rescored. They are an archive,
  never a gate in normal work (owner, 18 November 2026; entry 84), and they are not part of the new trees.
- **Nothing is authorised but documents and records.** The new system is built in four steps, each on the owner's own go
  (specification 17.4). No go has been given.

**The ratifications, from RAT-34's install to RAT-40.** Each was committed into `doc/` by Claude directly (the approach of
16 November 2026), except RAT-36's file, which the reviewer had committed itself.

| | The owner's ratification (Adelaide time) | What | Entry | In `doc/` at |
|---|---|---|---|---|
| RAT-34 | 17 Nov 2026, about 15:15 | register v0.31; H-1 v4 and its blurb; the approach of 16 November 2026 in force | 63 | `0044de8`, with the RAT-33 supplement v0.7 |
| RAT-35 | 17 Nov 2026, about 20:06 | the MHUP-B code plan v0.3 and design supplement v0.8, together (after EX_227) | 74 | `7d78e2b` |
| RAT-36 | 18 Nov 2026, about 14:28 | the reviewer's handover H-2 v3r4 (relayed in EX_238) | 87 | `d5e810c` (the reviewer's commit) |
| RAT-37 | 18 Nov 2026, 20:11 | H-1 v5 and its blurb; ratified by the owner directly, with no reviewer ruling | 92 | `6d4f4fa` |
| RAT-38 | 19 Nov 2026, 06:20 | H-1 v6 and its blurb, byte for byte as the candidates | 101 | `a356fb4` |
| RAT-39 | 19 Nov 2026, 23:25 | H-1 v7r1 and its blurb, after the reviewer's PASS | 106 | `7f9edc0` |
| RAT-40 | 22 Nov 2026, 13:33 | the system specification v0.6 and the deployment design v0.12, after EX_271; with four notes | 147 | `4de0fe4`, with the coding practices v0.1 |

Several of these files carry frozen wording that their ratification overrides: H-2 v3r4's name and heading say CANDIDATE; the
code plan v0.3 and the supplement v0.8 say RATIFICATION CANDIDATE; H-1 v6's header says CANDIDATE; the two RAT-40 design
documents say DRAFT in their titles. The bytes were kept so that the ratified hashes hold.

**What happened, in order (each item names its decision log entries).**
1. **17 November 2026: a new Claude chat took over** from H-1 v4 (HO-2; EX_216 to EX_219; entry 64): PASS, and the owner
   authorised normal work. Its notes D2, D4 and D5 on H-1 v4's own text are recorded here, as entry 74 asked: the readiness
   sheet's r2c hash was quoted at a path that by then held r2d; "87 Bash deny patterns" were 84 deny and 3 allow; E_2 has
   three variants, not six (the total of 40 was right).
2. **The MHUP-B code plan** (EX_220 to EX_227; entries 65 to 74). The owner's directions OD-1 to OD-6 (entries 69, 70). For
   OD-5 he committed the development and Mode H score records, unchanged, at `cc665ce` (ten files, and `.gitignore`).
   **RAT-35.**
3. **The code round** (the owner's go, entry 75). Three slices were built in the cloud and passed by the reviewer at source
   level: slice 1 (EX_228 to EX_231), slice 2 (EX_232, EX_233, EX_236, EX_237) and slice 3 (EX_239 to EX_242); entries 76 to
   91. They are kept under `exchange/CLAUDE_WEB_TOOLS/mhupb/`. **Nothing of them was installed.**
4. **18 November 2026.** The joint working principle (entry 81). The owner's clarified research model (entry 84; EX_234,
   EX_235): all draws are equal research targets; the sealed study is a read-only archive and never a gate; two labelled
   uses of OV-1. The reviewer chat reached its limit and a new one took over (entry 86). **RAT-36. RAT-37,** with the owner's
   decision that the two Mode H archive checks left in the installed code be removed (entry 92).
5. **Where production runs** (owner, evening of 18 November 2026; entries 93 to 98; `exchange/EX_243_Claude.md`): a separate
   production folder; no Git in it; complete ZIP backups; rollback by restoring a backup; built clean, once.
6. **19 November 2026.** EX_244 (the reviewer with the owner): a restore from backup followed by the ordinary walk-forward
   is valid research. A new Claude chat took over from H-1 v6 (HO-2; EX_245, EX_246; entries 100 to 102). **RAT-38.** The
   owner's decisions: how a restore is done (entry 100); Python 3.15 only for tests (entry 103); no monthly restore test
   (entry 104); a recomputation after a restore is not compared with what was lost (entry 105). **RAT-39.** Entry 99
   records a ratified file changed by accident and put back (the table below).
7. **The deployment design note and the OV-1 simplification amendment** (19 and 20 November 2026; EX_247 to EX_257; entries
   107 to 121): drafts v0.1 to v0.5 of the note and v0.1 and v0.2 of the amendment, each reviewed. **None was ratified.**
   Item 8 overtook them.
8. **The owner's course correction** (20 and 21 November 2026; EX_258, EX_259; entries 121, 122): families and variants only,
   no revisions; a clean new baseline with nothing destroyed; installing is releasing; minimum administrative software.
9. **The redesign** (21 and 22 November 2026): EX_260 to EX_265 (entries 123 to 131), then EX_266 to EX_271 with the
   reviewer's three handbacks `exchange/ChatGPT_to_Claude_*.md` (entries 135 to 146). The specification's section 19 indexes
   the owner's decisions by entry. EX_267 and EX_269 were RECHECK; **EX_271 is PASS (DESIGN).**
10. **Both chats changed on 21 November 2026.** The reviewer chat reached its limit (entry 128). On the owner's instruction
    Claude wrote a continuity candidate of the reviewer's handover, H-2 v3r10 (entry 129; `c8ff276`), and a new reviewer chat
    took over from it (entries 132, 134). A new Claude chat took over from a takeover note (entries 133, 134; no EX numbers,
    at the owner's choice).
11. **RAT-40** (entry 147; below).
12. **The handovers at this milestone** (22 November 2026; entries 148 to 150): Claude's H-1 v8 candidate, passed by the
    reviewer with one pointer correction, which was applied (EX_272); the reviewer's own H-2 v4 candidate; this register.
    The owner has decided that a new Claude chat takes over once H-1 v8 is ratified (entry 149).

**RAT-40 (owner, 22 November 2026, 13:33; entry 147).** After the reviewer's PASS (DESIGN) in EX_271, the owner ratified
`doc/Predictive_Randomness_System_Specification_v0_6.md` and `doc/Predictive_Randomness_Deployment_Design_v0_12.md`, each the
reviewed candidate with its status paragraph alone changed. The ratification covers: the two documents as the one authority
for the active system; the earlier design documents as history, with their science kept by reference (specification 1.2
and 1.3); the orphan-marker exception at a restore, which amends Architecture section 5C by ratification (deployment
design section 12); the mechanisms of specification section 19; and the four-step build order (17.4). **Four notes of
ratification bind the code:** (1) wherever variants are held or results are not current, the job says so plainly at its
start and at its end, names the cause and gives the exact command; (2) `doc/CODING_PRACTICES_v0_1.md`; (3) a light tidy-up of
the existing method files after build step 1 is proved and before anything is installed into QA or PROD, with no
calculation changed and the equivalence check run again; (4) the one test of EX_271 section 3, owed in build step 4.
RAT-40 authorises no code, source move, install, tree, run, copy, backup or restore.

**Carried into the build from earlier decisions, so that they are not lost.**
- **Nothing ever changes the PC's date, time or time zone** (owner, 17 November 2026; entry 78).
- **The Mode H archive checks (entry 92, decision 2).** Decided for the MHUP-B integrated package, which was not built. Its
  substance stands under the owner's rule that the sealed study is never a gate (entry 84). A fact for the build, checked
  in the installed code for this edition: the opening record `source_data/HOLDOUT_OPENED_<GAME>.json` is still consulted
  by `src/methods/_common/master_versions.py` and `src/methods/_common/contract_dispatch.py`, and the updater
  `src/results_master_v0_2.py` refuses an update for a game that has none. The ratified design does not name that
  record. Build steps 2 and 3 therefore settle, in their own packages, how the code the new system reuses treats it
  and whether a new tree's `source_data\` holds it. This is recorded as a practical point for those packages, not as a
  decision.
- **Python 3.15 only for tests; no monthly restore test; no comparison after a restore** (entries 103 to 105).
- **W-23 is unchanged:** every dependency upgrade is independently reviewed first (specification section 13).

**Out-of-date statements (register v0.32).** This register prevails, and the files are not edited:
- **Register v0.31, future actions.** Item 1: done (EX_215; RAT-34; `0044de8`). Item 2: the code plan was written, reviewed
  and ratified (RAT-35) and its three slices passed review, but the package was not built and nothing of it is installed;
  the build order of specification 17.4 replaces it, and the document amendments item 2 lists are not owed in that form.
  Item 3: the Powerball 1145-1285 report run was not run; in the new system the first jobs compute all history
  (specification 17.1). Item 4: see the future actions below.
- **Every "Current" status in this register for the documents that specification 1.3 names:** the Mode H design v0.1r7;
  the MHUP-B supplements v0.7 and v0.8, except sections 6.1, 6.3 and 6.5 of v0.8; the MHUP-B code plan v0.3; E2R-1 sections
  5, 6, 8, 9, 12 and 12A; R3 sections 6, 10 and 17.3.6; the direction document v0.3r1 section 9. From RAT-40 they are the
  record of the first study and no longer rules for the active system. Their ratifications and hashes stand as history.
  What specification 1.2 keeps by reference stays binding: R2 v0.5 sections 1, 2, 4 and 7 and each family's own design;
  E2R-1 section 7 (the readout), less its revision, run-mode and receipt fields; R3 sections 3, 4 and 17; the supplement
  v0.8 sections 6.1, 6.3 and 6.5; the one results source and its reviewed updater; Architecture 5C; the three safety
  switches and the empty allowlist; W-23.
- **Architecture v0.9 section 5C:** amended by RAT-40 for the orphan-marker exception at a restore. The file is not edited.
- **E4 of 4 November 2026 (register v0.25's section): "The results updater stays a separate operation".** For the new
  system the research job runs the reviewed updater itself in PROD (owner, entry 130).
- **The direction document v0.3r1, "monthly restore test":** dropped (entry 104).
- **Register v0.31's record of the approach of 16 November 2026, item 5** ("until MHUP-B's reviewed rulebook edition"): the
  local runner's rulebook v0.5 stays as it is until the new edition that is owed before any rehearsal of the new system.
- **H-1 v4** (RAT-34): superseded by H-1 v5 (RAT-37), v6 (RAT-38) and v7r1 (RAT-39). **H-2 v2 r1:** superseded by H-2 v3r4
  (RAT-36). Their rights regions are unaffected.
- **H-1 v5, v6 and v7r1, "register v0.32 ... travels with the MHUP-B package":** it travels with the handovers of
  22 November 2026.
- **Wherever earlier sections say MHUP-B, the weekly session or OV-1's registration comes next:** history. The next work is
  the list below.

| Document (path) | Author / check | Status and Git-content SHA-256 (as stored) |
|---|---|---|
| `doc/RATIFICATION_REGISTER_v0_31.md` | Claude, from the records | OWNER-RATIFIED 17 Nov 2026 (RAT-34); installed at `0044de8`; superseded by this register; `@@SHA:doc/RATIFICATION_REGISTER_v0_31.md@@` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v4.md` and its blurb | Claude | RAT-34; installed at `0044de8`; superseded at RAT-37; `@@SHA:doc/HANDOVER/Claude_Primary_Handover_H1_v4.md@@`; blurb `@@SHA:doc/HANDOVER/Claude_Primary_Handover_H1_v4_introductory_blurb.md@@` (changed by accident in the owner's commit `86f6c43`, put back to these ratified bytes at `7df2b5a`; entry 99) |
| `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_7.md` | Claude; the reviewer (EX_207 to EX_213) | RAT-33; committed at `0044de8`; superseded by v0.8; `@@SHA:doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_7.md@@` |
| `doc/Predictive_Randomness_MHUPB_Code_Plan_v0_3.md` | Claude; the reviewer (EX_223 to EX_227) | RAT-35; `7d78e2b`; history for the active system since RAT-40; `@@SHA:doc/Predictive_Randomness_MHUPB_Code_Plan_v0_3.md@@` |
| `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md` | Claude; the reviewer (EX_223 to EX_227) | RAT-35; `7d78e2b`; history since RAT-40 except sections 6.1, 6.3 and 6.5; `@@SHA:doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md@@` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r4_RATIFICATION_CANDIDATE_20261118.md` | the reviewer | RAT-36; `d5e810c`; the operative reviewer handover until the owner ratifies a successor; `@@SHA:doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r4_RATIFICATION_CANDIDATE_20261118.md@@` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v5.md` and its blurb | Claude | RAT-37; `6d4f4fa`; superseded at RAT-38; `@@SHA:doc/HANDOVER/Claude_Primary_Handover_H1_v5.md@@`; blurb `@@SHA:doc/HANDOVER/Claude_Primary_Handover_H1_v5_introductory_blurb.md@@` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v6.md` and its blurb | Claude | RAT-38; `a356fb4`; superseded at RAT-39; `@@SHA:doc/HANDOVER/Claude_Primary_Handover_H1_v6.md@@`; blurb `@@SHA:doc/HANDOVER/Claude_Primary_Handover_H1_v6_introductory_blurb.md@@` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md` and its blurb | Claude; the reviewer (PASS at `39f3ef7`) | RAT-39; `7f9edc0`; the installed Claude handover until the owner ratifies H-1 v8; `@@SHA:doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md@@`; blurb `@@SHA:doc/HANDOVER/Claude_Primary_Handover_H1_v7r1_introductory_blurb.md@@` |
| `doc/Predictive_Randomness_System_Specification_v0_6.md` | Claude; the reviewer (EX_267, EX_269, EX_271) | OWNER-RATIFIED 22 Nov 2026 (RAT-40); `4de0fe4`; `@@SHA:doc/Predictive_Randomness_System_Specification_v0_6.md@@`; the reviewed candidate `exchange/CLAUDE_WEB_TOOLS/simplify/SYSTEM_SPECIFICATION_DRAFT_v0_6.md` `@@SHA:exchange/CLAUDE_WEB_TOOLS/simplify/SYSTEM_SPECIFICATION_DRAFT_v0_6.md@@` |
| `doc/Predictive_Randomness_Deployment_Design_v0_12.md` | Claude; the reviewer (EX_267, EX_269, EX_271) | OWNER-RATIFIED 22 Nov 2026 (RAT-40); `4de0fe4`; `@@SHA:doc/Predictive_Randomness_Deployment_Design_v0_12.md@@`; the reviewed candidate `exchange/CLAUDE_WEB_TOOLS/simplify/DEPLOYMENT_DESIGN_DRAFT_v0_12.md` `@@SHA:exchange/CLAUDE_WEB_TOOLS/simplify/DEPLOYMENT_DESIGN_DRAFT_v0_12.md@@` |
| `doc/CODING_PRACTICES_v0_1.md` | the owner's points, set out by Claude | a note of ratification to RAT-40; `4de0fe4`; `@@SHA:doc/CODING_PRACTICES_v0_1.md@@` |
| `exchange/EX_271_ChatGPT.md` | the reviewer | PASS (DESIGN) of the two candidates; `@@SHA:exchange/EX_271_ChatGPT.md@@` |
| `exchange/EX_244_ChatGPT.md` | the reviewer, with the owner | governs restore and the walk-forward after it (entry 101); `@@SHA:exchange/EX_244_ChatGPT.md@@` |
| `exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md` | Claude and the reviewer, on the owner's text | agreed 18 Nov 2026 (entry 81); `@@SHA:exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md@@` |
| `exchange/DECISIONS/OWNER_CLARIFICATION_2026_11_18_EQUAL_DRAWS_AND_OV1_USES.md` | the owner's clarification, recorded by Claude | 18 Nov 2026 (entry 84); `@@SHA:exchange/DECISIONS/OWNER_CLARIFICATION_2026_11_18_EQUAL_DRAWS_AND_OV1_USES.md@@` |
| `exchange/CLAUDE_WEB_TOOLS/h1v8/out/Claude_Primary_Handover_H1_v8.md` and its blurb | Claude; the reviewer (EX_272) | CANDIDATE, not ratified; `@@SHA:exchange/CLAUDE_WEB_TOOLS/h1v8/out/Claude_Primary_Handover_H1_v8.md@@`; blurb `@@SHA:exchange/CLAUDE_WEB_TOOLS/h1v8/out/Claude_Primary_Handover_H1_v8_introductory_blurb.md@@` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md` and its blurb | the reviewer | CANDIDATE, not ratified; `@@SHA:doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md@@`; blurb `@@SHA:doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122_introductory_blurb.md@@` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r10_CONTINUITY_CANDIDATE_20261121.md` | Claude, on the owner's instruction (entry 129) | a continuity candidate, never ratified; the present reviewer chat started from it; `@@SHA:doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r10_CONTINUITY_CANDIDATE_20261121.md@@` |
| `exchange/DECISIONS/DECISION_LOG.md` and `exchange/CONTINUITY_NOW.md` | Claude, from the owner's words and the records | living files (P2, P0); no fixed hash; Git keeps their history |

**Future actions (replacing register v0.31's list; not authorisations).**
1. The reviewer's review of this register. The owner's ratification of it and of the two handovers (the next free number is
   RAT-41), and their installation in `doc/`.
2. A new Claude chat takes over once H-1 v8 is ratified (owner, entry 149).
3. The owner's own ZIP of the whole project folder on E:, when Claude says, before build step 1 moves any source file in
   his clone.
4. The four build steps of specification 17.4, each on the owner's own go: the folder layout; the research engine in DEV;
   trees, installs, backups and restore, after which PROD exists and forecasts every week; the laboratory tools. Between
   step 1 and any install into QA or PROD: the light tidy-up of the existing method files.
5. With the build: a new local runner rulebook edition and the owner's deny entries before the first rehearsal of the new
   system; the test of EX_271 section 3 in step 4; a new draft of `doc/METHOD_TEMPLATE/` after step 3; the practical point
   about the opening record above.
6. No new edition of R2, R3, E2R-1 or the Architecture is planned in the ratified build order: specification 1.2 and 1.3 say
   which of their clauses bind.
7. One pass over `exchange/OWNER_ROADMAP.md` and `exchange/OWNER_REMINDERS.md`, marking each item carried, done or dropped
   under the new design, for the owner to confirm.
8. Later, and only when the owner asks: new methods and waves (OUTLANDISH_01's family probably first); the deferred
   performance study (R-006); KISS-1; the ideas backlog (P5).

**The ratification of this register.** Not yet given. If the owner ratifies it, the finalisation changes only this
register's version line, this paragraph and the status cells of the table above for the files ratified with it.

