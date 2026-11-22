# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v8

**Document:** H-1 under the agreed roles position v0.1r1, section 9 item 4.
**Version:** v8, 22 November 2026 (Adelaide, UTC+10:30). A **full edition, restructured and shortened**, as H-1 v7r1
section 8.5 allows. It is written for the system the owner ratified on 22 November 2026 (RAT-40). **Sections 1, 2 and
2A are H-1 v7r1's bytes, unchanged** (the builder asserts it; section 0C says how to read them today). Everything else
is rewritten. Appendix B lists what was dropped from v7r1 and where it now lives. Built by
`exchange/CLAUDE_WEB_TOOLS/h1v8/make_h1_v8.py` from `H1_v8_template.md` beside it.
**Status:** CANDIDATE for independent review and the owner's ratification. It authorises nothing. Until it is
ratified, H-1 v7r1 (RAT-39) is the installed Claude handover, read with decision log entries 121 to the latest.
**Audience:** any later Claude chat that takes over as primary designer and coder; the ChatGPT reviewer chat; the
project owner.
**Repository:** `hydra3333/analysing_perceived_randomness_in_reality`, public GitHub, branch `main`.
**Baseline described:** `main` on 22 November 2026, after RAT-40 (commit `4de0fe4`). **The code on `main` is the old
system, and none of the new system is coded:** no file under `src/` or `tests/`, no root `.bat` and no
`requirements.txt` has changed since `cc0ab73` (14 November 2026; checked with `git diff` for this edition).
**Replaces, once ratified:** H-1 v7r1 and its blurb (RAT-39), and the takeover note of 21 November 2026 with its blurb
(a working note, never a handover). All stay where they are as history.
**Authority:** the ratified documents and the decision log prevail over this handover wherever they differ. This file
summarises and points to them.
**Draw values:** none appear in this file.

---

## 0. First actions in a new Claude chat

1. Attach the repository with push access and clone `main` **with its full history** (if
   `git rev-parse --is-shallow-repository` says `true`, run `git fetch --unshallow`). Check the hashes in section 4 and
   Appendix A with `git show HEAD:<path> | sha256sum`.
2. Read, in this order:
   - the introductory blurb that started your chat (the owner's hard rules, in his words; copied below);
   - `exchange/CONTINUITY_NOW.md`, its top block (the live state; it overtakes this file as soon as anything moves);
   - this file, all of it (it is short);
   - **the three ratified documents of section 4.1:** the system specification (its section 0 first: the whole
     system on one page), the deployment design, and the coding practices;
   - `exchange/DECISIONS/DECISION_LOG.md`, entries 121 to the latest (the owner's own words; entry 147 is RAT-40);
   - `exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md` (the joint working principle);
   - the reviewer's findings on the design: `exchange/EX_267_ChatGPT.md`, `EX_269_ChatGPT.md`, `EX_271_ChatGPT.md` (they
     show what the reviewer watches, and EX_271 section 3 holds a test still owed);
   - the reviewer's handover in force (`exchange/CONTINUITY_NOW.md` names it; section 4.4);
   - `exchange/README.md` (the exchange protocol) and `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (the local runner's
     rulebook; section 8.6 says why it is out of date).
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
   write in the chat; build, run and commit nothing, not even under `exchange/`. Whether the takeover exchanges get
   EX numbers is the owner's choice: the takeover of 21 November 2026 used none and was recorded in the decision log
   (entry 134). The outgoing Claude chat stops committing once you start. The reviewer chat stays in role through a
   Claude takeover unless the owner says otherwise.
5. Before any code (once normal work is authorised): name the work item, its risk tier and its reviewer chat
   (section 1.2), and check that the owner has given the go for that build step (section 10).
6. Keep `exchange/CONTINUITY_NOW.md` current after every milestone. Record every owner decision in the decision log at
   once, in his words, reading the time from the clock in the command that writes it. When the chat grows long, write
   the next handover first.
7. **Models (MC-1, section 2):** take over on Opus; section 10 says where Fable (High) is suggested.

**The owner's hard rules, in his words** (from the blurb of 21 November 2026; binding):

{{HARD_RULES}}

To these add, from the same standing rules: never write under `source_data/`, `results/`, `transitory_data/` or `GAIS/`;
never write the owner's personal name in anything committed (write "the project owner" or `hydra3333`).

## 0A. Things that trip a new chat

1. **Two systems share this repository.** The code under `src/` is the OLD system (the proof-of-concept coordinator,
   the contract runner, Mode H, the walk-forward driver and report tool). The ratified design describes a NEW system
   that is **not coded at all**. The older design documents (the Mode H design v0.1r7, the MHUP-B supplements and code
   plan, parts of E2R-1 and R3, the direction document's section 9) are history, except the clauses the
   specification's section 1.2 keeps by reference (section 4.2 below). Do not build from the MHUP-B plan and do not
   install the MHUP-B slices (section 7.3).
2. **The words DRAFT and CANDIDATE inside a ratified file are frozen wording.** A file's status paragraph and the
   decision log say what is ratified. The two design documents in `doc/` still carry DRAFT in their titles.
3. **The register is behind.** `doc/RATIFICATION_REGISTER_v0_31.md` is the newest edition; RAT-35 to RAT-40 are recorded
   only in the decision log. Read the log for the last RAT number, the last entry number and the last EX number
   before using a new one. At this edition: the last RAT is RAT-40; the newest EX is EX_271; the newest decision log
   entry is 148 (this candidate).
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

## 0B. The state at this edition (22 November 2026)

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
   `doc/CODING_PRACTICES_v0_1.md`; (c) a light tidy-up of the existing method files after build step 1 is proved and
   before anything is installed into QA or PROD; (d) the one test of EX_271 section 3, owed in build step 4.
6. **What is authorised now: documents and records only.** No code, source move, install, tree, run, copy, backup or
   restore. Each of the four build steps (section 10) needs the owner's own go.
7. **What is owed** is listed once, in section 12.8.
8. **The chats.** This Claude chat took over on 21 November 2026 from the takeover note (HO-2 accepted, entry 134).
   The present ChatGPT reviewer chat took over the same day, after the previous one reached its limit (entries 128,
   132, 134); it has reviewed EX_266 to EX_271. On 22 November 2026 the owner asked both chats to bring their
   handovers fully up to date at this milestone; the reviewer committed its H-2 v4 candidate that afternoon
   (section 4.4).

## 0C. Sections 1, 2 and 2A are carried unchanged: read them with these notes

They are H-1 v7r1's text, byte for byte, because they hold the roles, the reviewer's rights, the review procedure,
the Git rules and the owner's working preferences, none of which the redesign changed. Their section references
are to this edition's sections of the same number ("section 0B, item 4" is item 4 above). Where they are out of date:

1. **Section 1.1, the reviewer chats.** The "present reviewer chat" it describes reached its limit on 21 November
   2026 (entry 128). The chat that took over that day (0B item 8) has the same rights and independence.
2. **Section 1.1, the local runner.** Rulebook v0.5 names the old system's programs. A new edition is owed
   before any rehearsal of the new system (section 8.6).
3. **Section 1.6 describes how code reaches the owner's clone and GitHub,** which is DEV. It still applies to every
   code package. How software then reaches QA or PROD is new and different: the commands of specification
   section 12, from local files, never by Git. Where 1.6 says Claude records the reviewer's files and the owner
   uploads zips, its own first bullet is the current practice: the reviewer commits its own. The rounds of November
   2026 used plain `.md` EX files with no zip (section 12.1).
4. **Section 1.6, the register.** v0.31 is the newest; v0.32 is owed (section 12.8).
5. **Section 2, pushing.** The Mode H freeze it mentions ended on 16 November 2026. The rule not to push while the
   owner may have local commits waiting still applies.
6. **Section 2, the owner's two working lists** (`OWNER_ROADMAP.md`, `OWNER_REMINDERS.md`) were last updated on 18 and
   14 November 2026. Under P3 the roadmap's NOW block points to `CONTINUITY_NOW.md`. A pass over both is owed
   (section 12.8).
7. **Sections 1.3 and 1.5 in the new system (Claude's reading, RECOMMENDED, not a new rule).** Judged by effect, HIGH
   and always-review work includes: the one reader and the permitted view (N-1); the writer of the forecast and score
   lists and its invariants (specification 5); scoring (8); the readout (ranking, ties, TOP and WORST); OV-1 and its
   kernel (10); the status file's writer and withdrawal (3.5, 11); the variant fingerprint and the forecasting-code
   identity (12.4); the derived check and the cutoff file (5.8); the install checks and smoke cases (12.3); the
   archive-then-shorten steps of a rerun (7A); anything that reads PROD (12.7, 14.2); the updater's launcher; the
   process rule and the orphan-marker check.

---

{{CARRIED_1_2}}

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
ratified, and none of it is coded. It runs on Windows 11 with Python 3.15. The owner expects the most likely outcome
to be that no method works; a carefully measured null result is valid and useful (section 2A).

---

## 4. Governing documents

SHA-256 values are of the Git content (LF), computed by the builder from `HEAD`.

### 4.1 The authority for the active system (RAT-40)

| Document | SHA-256 |
|---|---|
| `doc/Predictive_Randomness_System_Specification_v0_6.md` | `{{SHA:doc/Predictive_Randomness_System_Specification_v0_6.md}}` |
| `doc/Predictive_Randomness_Deployment_Design_v0_12.md` | `{{SHA:doc/Predictive_Randomness_Deployment_Design_v0_12.md}}` |
| `doc/CODING_PRACTICES_v0_1.md` | `{{SHA:doc/CODING_PRACTICES_v0_1.md}}` |

Each design document is the candidate the reviewer passed in EX_271 with its status paragraph alone changed. The
candidates and every earlier draft, with exact diffs between editions, are in `exchange/CLAUDE_WEB_TOOLS/simplify/`.

### 4.2 Still binding by reference (specification 1.2: science and safety)

| Document | SHA-256 | What stays binding |
|---|---|---|
| `doc/Predictive_Randomness_Experimental_Method_Specifications_R2_v0_5.md` | `{{SHA:doc/Predictive_Randomness_Experimental_Method_Specifications_R2_v0_5.md}}` | sections 1 (invariants), 2 (data contract), 4 (observation policy), 7 (the 62 families) |
| each family's own ratified design (in `doc/`: E_6; E_3 and E_4; wave 1; wave 2; the E_1 documents) | see H-1 v7r1 section 4 | the family's rule and its variants' fixed settings |
| `doc/Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md` | `{{SHA:doc/Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md}}` | section 7 only (the readout: ranking, ties, TOP and WORST), less its revision, run-mode and receipt fields |
| `doc/Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md` | `{{SHA:doc/Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md}}` | sections 3 (measures), 4 (reference values) and 17 (league measures; the time axis is the draw number; games never pooled), less 17.3.6 |
| `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md` | `{{SHA:doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md}}` | sections 6.1, 6.3 and 6.5 only (OV-1's mathematics), as implemented by the kernel of section 7.3 |
| `doc/Predictive_Randomness_Software_Architecture_Discussion_v0_9.md` | `{{SHA:doc/Predictive_Randomness_Software_Architecture_Discussion_v0_9.md}}` | section 5C (process safety; protected), amended by RAT-40 for the orphan-marker exception at a restore (deployment design 12) |

Also kept by the specification's 1.2: Lotterywest-GOV as the one results source through the one reviewed updater;
the process, orphan-marker and no-kill rules; the three safety switches (False) and the allowlist (empty); W-23.
**An exact clause list for E2R-1 section 7 is a first task of the code round** (specification section 20).

### 4.3 Neither named as binding nor as history by the specification

| Document | SHA-256 | Note |
|---|---|---|
| `doc/Predictive_Randomness_Research_Project_Proposal_v0_6.md` | `{{SHA:doc/Predictive_Randomness_Research_Project_Proposal_v0_6.md}}` | the charter and philosophy; the source of section 2A |
| `doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` | `{{SHA:doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md}}` | the catalogue E_1 to E_62 |
| `doc/contracts/TIE_SHA256_V1_Ratified_Encoding_v0_2.md` | `{{SHA:doc/contracts/TIE_SHA256_V1_Ratified_Encoding_v0_2.md}}` | the tie and seed encoding that the readout of E2R-1 section 7 and the installed code use |

RAT-40 did not change them. Treat them as standing; if a clause of either seems to conflict with the specification,
say so and ask.

### 4.4 History, and the working documents

- **Historical for the active system (specification 1.3):** the Mode H design v0.1r7; the MHUP-B supplements v0.7 and
  v0.8 except the three sections above; the MHUP-B code plan v0.3; E2R-1 sections 5, 6, 8, 9, 12 and 12A; R3 sections
  6 and 10 and 17.3.6; the direction document v0.3r1 section 9; every draft of the MHUP-B deployment note. H-1 v7r1
  section 4 lists these files with their hashes.
- **Roles and review:** `doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md`
  (`{{SHA:doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md}}`);
  `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`
  (`{{SHA:review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md}}`).
- **The reviewer's handover (H-2).** Ratified: H-2 v3r4 (RAT-36; its file name still says CANDIDATE). **The newest is
  the reviewer's own full edition current to RAT-40,**
  `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md`
  (`{{SHA:doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md}}`; commits `30826be` (full candidate) and
  `6316767` (current introductory blurb)): a candidate until the owner ratifies it. Its section 0 states the current position, the
  four notes of ratification, the build order and the closed OV-1 question as this file does. Before it came the
  v3r10 continuity candidate of 21 November 2026, which Claude wrote on the owner's instruction when the previous
  reviewer chat was lost. `exchange/CONTINUITY_NOW.md` names the edition in force.
- **The register:** `doc/RATIFICATION_REGISTER_v0_31.md` (`{{SHA:doc/RATIFICATION_REGISTER_v0_31.md}}`), RAT-34. For
  RAT-35 to RAT-40 the decision log is the record.
- **Protected blocks** (byte-identical through every consolidation): Architecture 5C; R2 section 7 and 4.1; R3 0.4,
  2.4 and 3; the proposal's E_1 to E_6. **Never edit a ratified file in place.**

---

## 5. Settled decisions - do not reopen without substantive cause

The three ratified documents hold the rules of the new system; the decision log holds the owner's words. This
section carries what a new chat most needs, and what is not in those three documents.

### 5.1 Data, the results source, and what the AI chats may do

The first five lines are H-1 v7r1's, unchanged.

{{B:- **Source: Lotterywest-GOV** (decision LW-1}}
{{B:- **No lottery-results searches**}}
{{B:- **Drawn order:**}}
{{B:- **Dates only** in masters.}}
{{B:- **The two-site checker**}}
- **One master per game:** `source_data/<GAME>_results_master.csv` with its append-only ledger. `.gitattributes` has
  `source_data/** -text`; never change it. In the new system only PROD runs the updater; QA and DEV receive a
  checked copy of PROD's accepted results (specification 7.1).
- **What the AI chats may read and write:** section 0B item 4.

### 5.2 The scientific contract

These lines are H-1 v7r1's, unchanged; they summarise R2 and E2R-1 section 7, which govern. The specification's
section 6 restates N-1 for the new system and adds its test.

{{B:- **Strict N-1:**}}
{{B:- **The B1 rule:**}}
{{B:- **Seeds and content identity**}}
{{B:- **Views:**}}
{{B:- **Numerics:**}}
{{B:- **Fresh fit for every target**}}
{{B:- **TOP and WORST from one frozen ranking;**}}
{{B:- **Prediction-time ties:**}}
{{B:- **Synthetic firewall:**}}
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
  target lacks, checks it there and asks for one confirmation. No install or release records, and no Git, outside DEV.
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
  131). No tool is built for it. Claude tells him when it is time (section 10).
- **One design, built in four steps, each on its own go** (entry 143; specification 17.4; section 10).
- **Python 3.15 only** for tests (entry 103). **W-23 is unchanged** (section 5.4).
- **Closed:** the OV-1 timing question (section 0A item 8).

### 5.4 Engineering and process safety

The specification's section 13 cites "H-1 5.4" for the evidence a dependency upgrade needs. That is the first line
below. The five lines are H-1 v7r1's, unchanged; where the first mentions Mode H and "Approval 1" it is history, and
its rule stands: after every upgrade, stop until the evidence passes.

{{B:- **Dependencies:** `install_upgrade_dependencies_into_venv.bat`}}
{{B:- **Process termination (Architecture 5C, protected):**}}
{{B:- **Orphan marker rule (owner, binding):**}}
{{B:- **Three switches stay False:**}}
{{B:- **Testing order:**}}
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

{{B:- The Windows venv `python.exe` is a redirector}}
{{B:- Windows does not kill children when the parent dies;}}
{{B:- A `.bat` launched via `Popen` runs under `cmd.exe`}}
{{B:- `O_NOFOLLOW` does not exist on Windows;}}
{{B:- Line endings: Git stores `.md` and `.py` as LF;}}
{{B:- **Python 3.15 makes UTF-8 the default text encoding (PEP 686).**}}
{{B:- **Record files and line endings:**}}
{{B:- **Exact arithmetic can be slow at full size:**}}
{{B:- **Byte-code caches:**}}
{{B:- **Reference figures**}}
- **New in this edition: DEV's working files are the install source.** If Git rewrites line endings in the owner's
  clone, file hashes change, readiness markers stop matching and a helper may be refused. That fails safe; pinning
  line endings for `src/` in `.gitattributes` avoids it (specification section 20). The owner's checkout uses
  `core.autocrlf=true`.

---

## 7. What exists today

### 7.1 The installed code (the old system)

- `src/`, `tests/`, the root `.bat` files and `requirements.txt` are as at `cc0ab73`. Twelve method families, 40 variants
  per game: E_1 (one variant), E_3 and E_4 (six each), and E_2, E_6, E_7, E_8, E_9, E_10, E_17, E_18, E_19 (three each).
- **Tests:** 571 offline tests in 45 modules at the last recorded runs (H-1 v7r1 section 7.4). **This chat has not run
  the suite.** v7r1 records two known causes of failures on `main` today: the tests pinned to the version-1 masters
  (the masters are at version 2), and `test_gitignore_lines` (the owner un-ignored a results folder at `cc665ce`).
  **Establish the suite's present result before build step 1 changes anything,** so that "the existing suite" in
  specification 17.3 has a known expected outcome.
- The module map and the installed packages' record are H-1 v7r1 sections 7.1 to 7.3: history, and accurate for this
  code.
- The three safety switches are False and the allowlist is empty in `src/` (checked for this edition). A fourth,
  older switch, `ENABLE_CONTRACT_REAL_DEVELOPMENT`, is True in the old contract runner (owner, 31 October 2026).

### 7.2 Data and records

- **Masters, version 2** (checked for this edition): Powerball draws 1144 to 1591 (448 rows),
  `{{SHA:source_data/POWERBALL_results_master.csv}}`; Oz Lotto draws 1474 to 1708 (235 rows),
  `{{SHA:source_data/OZLOTTO_results_master.csv}}`.
- **In Git:** the sealed Mode H records and reports (`c7622fa`); the development and Mode H score records (`cc665ce`);
  the earlier ranking reports and batch plans.
- **Not in Git:** the old forecast run folders and attempts ledgers are Git-ignored and exist only on the owner's PC
  and in his backups. The equivalence check of build step 1 and the transition check read them (specification
  17.2, 17.3). **That is why the owner's own ZIP comes first.**

### 7.3 Staged work that is not installed and will not be installed as built

- **The three MHUP-B slices** under `exchange/CLAUDE_WEB_TOOLS/mhupb/` (slice 1, EX_231 PASS; slice 2, EX_237 PASS;
  slice 3, EX_242 PASS) implement the weekly-session design that the course correction replaced. They are a source
  of reviewed code and tests to draw on, never a package to install.
- **The OV-1 kernel** is `exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/slice2_new/src/evaluation/ov1_numeric.py`
  (`{{SHA:exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/slice2_new/src/evaluation/ov1_numeric.py}}`), with its tests beside
  it. The specification's 1.2 names it as the implementation of OV-1's mathematics; the reviewer accepted its proofs
  P1 to P8 at source level (EX_233). Build step 2 carries it into the new system: reuse it, do not rewrite it; any
  change to it is HIGH work.

### 7.4 The design's working record

`exchange/CLAUDE_WEB_TOOLS/simplify/`: every draft of the specification (v0.1 to v0.6) and of the deployment design
(v0.7 to v0.12), the exact diff between each pair of editions, the builders (those of the last three editions,
`build_v0_4_v0_10.py` to `build_v0_6_v0_12.py` with their two templates, were committed with this candidate), and
`DRAFT_CONTRADICTIONS_FOR_REVIEWER_v0_1.md` (where the early drafts disagreed
with later decisions, with provenance). The specification's section 21 says where each finding and decision landed.

### 7.5 Not tested by anyone

**Nothing of the new system has run.** No timing is known. The specification's section 20 and the deployment
design's section 17 list the uncertainties; the costs to measure in the first rehearsal are the derived check at
each job, a first full fill, a `Check_Forecasts --all`, a rerun, and a backup of a whole tree with its environment.
For the old code, H-1 v7r1 section 7.6 stands.

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

{{B:Include: the work-item card;}}

Add, from RAT-40: the line "coding practices met", or the exceptions with their reasons.

### 8.5 Document work

These lines are H-1 v7r1's, unchanged:

{{B:- Prepare a **new candidate edition** from the exact ratified Git blob}}
{{B:- **Handovers** may be restructured and shortened}}
{{B:- **Copy agreed wording verbatim.**}}
- **In this chat's rounds** each new edition was built from the previous one by a small Python builder of counted
  replacements (whitespace-tolerant; every anchor asserted to occur exactly once), then proved by making a `diff -u`
  and applying it with `patch` to the old file and comparing the result with `cmp`. **Commit the builder beside the
  document** (section 8.8).

### 8.6 The Claude Code local runner

- **What it is:** Claude Code on the owner's Windows PC carries out task files that Claude writes, in disposable task
  clones that cannot push, and reports what happened. Its rulebook is `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`
  (v0.5, RAT-30). Its reports are owner-machine evidence, not reviewer evidence and not acceptance.
- **Rulebook v0.5 is written for the old system.** It names the old programs it must never run and holds a
  finished one-task allowance (its section 2A). **Before any rehearsal of the new system a new edition is owed,**
  reviewed and ratified, naming the new commands, with matching deny entries in `.claude/settings.json` that the owner
  edits. Until then the runner can still run the existing suite in a task clone, as task T024 did.
- **How a task runs:** Claude writes `inbox/TASK_Tnnn.md` with every command in full, the expected PASS line of each
  step, a clean-up step and a report step, and commits it. The owner pulls, starts a **new** Claude Code conversation
  and types `Do inbox\TASK_Tnnn.md`. The runner commits `outbox/REPORT_Tnnn.md`; the owner pushes; Claude reads the
  report from GitHub. A STOP is a STOP.
- **The deny list matches command text** (`*.bat*` among many). Check every task file with
  `python3 -I exchange/CLAUDE_WEB_TOOLS/check_task_commands.py <repo> <task>` before committing it. Never ask the runner
  to count or filter output; ask for the whole output and count it yourself.
- **The owner favours running heavy, repeatable things there** (test suites, rehearsals), because they cost few
  tokens. Let that guide what goes to the runner. The last task run was T024; H-1 v7r1 section 8.6 has the record of
  T001 to T024 and the practical detail.

### 8.7 Rebuilding

The cloud workspace does not persist. Everything needed to rebuild a document or a package travels in `exchange/`:
its builder, its template or base, its diffs and its evidence. The base of a code package is a Git commit.

### 8.8 Lessons from Claude's own errors

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
   or in `_shared/`, each helper versioned by its file name (specification 3.2 to 3.4); tests, among them the N-1
   test that changes and appends draws at and after the target; mutation checks; the coding practices. It reaches
   the owner's clone as a reviewed package (section 1.6).
4. **Ready, then installed:** `Make_Installable.bat` writes the readiness marker; `Install.bat PROD` (or `QA`) adds the
   variant, checks it in the target with a smoke case and asks for one confirmation (specification 4, 12.1 to 12.3).
5. **The next research job** fills its history draw by draw; after a successful results step with its history
   complete it gets its eligibility draw for the prevailing OV-1 (specification 7.1, 10.2).

A changed method is a new variant. `doc/METHOD_TEMPLATE/` (draft 5) describes the old process (`contract.py`,
`IN_DEVELOPMENT.txt`, registry entries, a release package): it is history until a new draft is written, which is
owed after build step 3 (section 12.8). The owner's OUTLANDISH_01 method family is in this project's backlog,
"probably first" (owner, 14 November 2026), and comes in only by this route; its own runs are not evidence here.

---

## 10. Next work, in order (planned; the owner decides each step)

1. **This handover:** the reviewer's review; the owner's ratification; installation in `doc/HANDOVER/` with its blurb.
   The reviewer's own handover current to RAT-40 (H-2 v4, section 4.4) awaits the owner's ratification too.
2. **The owner decides whether build step 1 starts in the present Claude chat or a new one.**
3. **Build step 1: the folder layout** (specification 17.3, phase 1), on the owner's go.
   - First, establish the suite's present result on `main` (section 7.1).
   - The package moves method files to the layout of specification 3.2 and changes import lines; no computation,
     contract or record changes. Its evidence: a listing that shows each moved file's bytes unchanged apart from
     imports; the existing suite; and the equivalence check of every existing variant, both games, every target with
     an old development forecast.
   - **The equivalence check reads the old forecast records, which exist only on the owner's PC** (section 7.2). So
     it runs there, on his go, read-only. Where exactly it runs (his clone after the install, or an unpacked copy of
     his ZIP) is the first practical point to settle with him in that package: one plain question, not a design round.
   - **The owner's ZIP of the whole project folder on E: comes before he installs that package** (before any source
     file moves in his clone). Tell him when. The advice given to him: include `.git` and the results and run
     folders; `.venv` optional; nothing of the project running; open the ZIP once to check it; keep it off E:.
4. **The light tidy-up of the existing method files** (RAT-40 note): after step 1 is proved and before anything is
   installed into QA or PROD. Headers, dependency lists, comments where plainly missing; no calculation changes; the
   equivalence check run again. It is done then because a variant's files can never change once installed.
5. **Build step 2: the research engine, in DEV** (specification sections 3 to 11): the lists, the job with its fill
   and catch-up, scoring, the reports, both OV-1 scores (with the kernel of section 7.3), the status file and
   withdrawal; the checks of 5.6A and 5.8 and both header identities from the first day.
6. **Build step 3: trees, installs, backups and restore** (specification 12.1 to 12.6, 13, 14.1), then the transition
   check and PROD's first job. Before its first rehearsal on the owner's PC: the new rulebook edition (section 8.6).
   **After this step PROD exists and forecasts every week, and new methods can be added: the main game.**
7. **Build step 4: the laboratory tools** (specification 12.7, 14.2, 7A, 12.8, `Check_Forecasts`), with the test of
   EX_271 section 3. Until it is built, a fault found in shared code is not improvised around: the affected work is
   held, or the owner restores a backup (specification 17.4).
8. **Then, in the owner's order:** new methods and waves; OUTLANDISH_01's family; the housekeeping of section 12.8.

**Models (MC-1; suggestions, the owner decides):** Opus for step 1, the tidy-up, packaging, task files and records.
Fable (High) for the core of step 2 (the list writer and its invariants, the job's fill and catch-up, the derived
check, OV-1's integration), for the install, backup and restore state machines of step 3, for the rerun and
correction steps of step 4, and for any unexplained STOP. Cold reads before a review round may be helpers on Opus.

**Genuinely OPEN** (do not present as decided): the identities, form and order of OUTLANDISH_01's methods; each
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
PC's date, time or time zone; ending a project process; clearing or bypassing the orphan marker; flipping a safety
switch or adding an allowlist entry; altering, rerunning or rescoring the sealed Mode H records; editing the
reviewer's files; pooling the games; weakening method-facing N-1 isolation. No Windows lifecycle or destructive test
runs without its own separately approved gate. A STOP is a STOP: nothing is retried, reset or worked around.

---

## 12. Working knowledge

This section describes practice, not rules. **This chat did document work only:** it built no code workspace and
ran no suite. Sections 12.3 and 12.4 are carried from H-1 v7r1 in short form and were not exercised here.

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
  is needed unless a code package travels.
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
New since v7r1: `simplify/` (section 7.4) and `h1v8/` (this edition's template and builder). The workspace paths
inside older scripts are a previous chat's; change them at the top before use.

### 12.3 Building and rehearsing a code package (carried; not exercised by this chat)

- **Base tree:** `git archive <base commit> | tar -x -C BASE`. **Dev tree:** a copy plus your changes. Never the
  owner's checkout.
- **The Python 3.15 environment** does not exist in a new workspace: `uv python install 3.15`, `uv venv --python 3.15
  <dir>`, then the project's direct packages as listed in `DIRECT_PACKAGES` in
  `install_upgrade_dependencies_into_venv.bat` (a bare interpreter fails every module on `numpy` and `psutil`).
- **Suite on Linux:** `PYTHONPATH=src:src/methods:tests python3 -B -m unittest <module>`, one module per process, in a
  full disposable clone (some accepted tests read the masters through the project's reader). About 25 minutes was
  recorded for 571 tests. E2R-T12 starts ordinary worker processes and needs the owner's approval for each run
  context; ask, or run the suite without it and say so.
- **Before sending:** the suite passes on the 3.15 build, the mutants are all caught or explained, every count in
  the instructions came from a tool, and any task file passes the deny check.
- H-1 v7r1 sections 12.2 to 12.4 have the fuller detail (frozen mirrors, LF and CRLF rehearsals, negative tests).

### 12.4 Claude Code task files

One task per rehearsal; commands written out in full with absolute Windows paths; each step with its expected PASS
line; a STOP sends the runner to clean-up and the report. Never put `.bat` or any other denied text in a task
command. Read the whole report: every step's command, exit code and output.

### 12.5 Traps in the cloud workspace

The first line is H-1 v7r1's, unchanged:

{{B:- **Stopping your own test jobs in the cloud workspace, and nothing else (EX_117 C02).**}}
- The shell tool's default timeout is about two minutes: give a longer one, or run long jobs in the background
  writing to a file, and poll the file.
- The shell may reset its working directory: use absolute paths.
- Outbound network goes through an allowlist (package registries and GitHub). Lottery sites are never tried.
- Do not import a package's own scripts in place for a probe (a `__pycache__` folder once crept into a package).

### 12.6 The owner's machine

- Windows 11; 12 cores, 24 logical processors. Git with `core.autocrlf=true`. Downloads go to `E:\TEMP`, never into
  the repository.
- **DEV** is the clone at `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`, with its `.venv`
  (Python 3.15.2). **QA** will be `D:\TEST_BED` (backups `D:\TEST_BED_backups`) and **PROD** `G:\a_p_r_i_r` (backups
  `T:\a_p_r_i_r_backups`): the deployment design's examples; each tree's `ENVIRONMENT.ini` decides. Neither exists yet.
- The owner's OUTLANDISH_01 work (`GAIS/OUTLANDISH_01/`, with its own ChatGPT chat) is outside the reviewed line and
  uses the E: `.venv`. He commits it with `git add GAIS/OUTLANDISH_01/`, never `-A`.
- If a Windows console window is clicked it can freeze a program at its next print; Esc releases it.
- The owner is sometimes on a phone only: then give only steps that need no PC.

### 12.8 Open items at this edition (22 November 2026)

The live state is `exchange/CONTINUITY_NOW.md`; it overtakes this list.

- **Waiting on the reviewer:** its review of this candidate.
- **Waiting on the owner:** the ratification of this edition and of the reviewer's H-2 v4 candidate; the choice of
  chat for build step 1; then each go of section 10.
- **Owed by Claude, in order of need:**
  1. Telling the owner when to make his ZIP (section 10, item 3).
  2. The suite's present result on `main`, before build step 1.
  3. The four build steps and the tidy-up, each on its go.
  4. A new local runner rulebook edition, with the owner's deny entries, before the first rehearsal of the new
     system.
  5. The test of EX_271 section 3, in build step 4.
  6. Register v0.32, recording RAT-35 to RAT-40 and the decisions since v0.31. Register text goes to the reviewer
     only with a code package or the handovers (section 1.6); it was not written for this candidate, so it travels
     with the first code package unless the owner wants it sooner.
  7. A new draft of `doc/METHOD_TEMPLATE/` for the new layout, after build step 3.
  8. One pass over `exchange/OWNER_REMINDERS.md` and `exchange/OWNER_ROADMAP.md`, marking each item carried, done or
     dropped under the new design, for the owner to confirm. Most reminders concern the old system.
  9. The measurements of section 7.5, in the first rehearsal.
- **Later, and only when the owner asks:** the deferred performance study (R-006;
  `doc/Deferred_Performance_Engineering_Proposal_v0_1.md`: profile real run times before choosing any speed-up) and the
  simplicity review after full implementation (KISS-1).
- **Small leftovers the owner may choose to clear:** deleting `venv.bak` and Python 3.14; the duplicate exploration
  note in `doc/`; the old EX copies in `review/`.

### 12.9 The first hour in a new chat

1. Clone with full history; read section 0's list; check the hashes of section 4 and Appendix A.
2. Read the newest EX files and the decision log's last entries; list anything in flight (an unanswered message, a
   report not yet read, a decision given but not recorded).
3. **Confirm the takeover to the owner** in plain English (section 0, item 4). Do no work until he says so.
4. Only after his authorisation, and only when a build step is given its go: set up a workspace (section 12.3) and
   run the whole suite once to prove the tools before any change.

---

## Appendix A. Identities

SHA-256 of the Git content at `HEAD` (LF unless noted), computed by the builder. A file cannot name its own hash:
this file's and its blurb's are in the decision log entry that records each edition.

{{IDTABLE}}

Commits named in this file: `4de0fe4` (RAT-40 installed); `cc0ab73` (the code baseline); `c7622fa` (the Mode H results
and version-2 masters); `cc665ce` (the score records); `2e44bc2`, `1c7bd79`, `8eed779` (EX_266, EX_268, EX_270); `2fae39e`,
`5d22683`, `7492846` (EX_267, EX_269, EX_271); `9f5c132`, `a8bcfaa`, `dd39845` (the reviewer's three handbacks); `30826be`,
`18ce192` (the reviewer's H-2 v4 candidate and its blurb); `cf1c6d9` (the first commit after the history clean-up).

---

## Appendix B. What changed from H-1 v7r1, and where what was dropped now lives

### B.1 By section

| v7r1 | In v8 | Where the dropped text lives |
|---|---|---|
| Header | rewritten | - |
| 0 First actions | rewritten for the new reading list; the HO-2 takeover rule kept in full | v7r1 section 0 (the old reading list) |
| 0A Four things that trip a new chat | items 1 to 3 kept in short form (0A items 4, 5); item 4 (register v0.27's "RAT-28") dropped | v7r1 section 0A; register v0.28 |
| 0B The state at 19 November 2026 | replaced by a new 0B; its item 4 is kept as item 4 | v7r1 section 0B: the full record of Mode H, MHUP-B, OD-1 to OD-6, the deployment decisions D1 to D12, EX_244 |
| 1 Roles and workflow (1.1 to 1.7) | **carried byte for byte** | - |
| 2 How the owner wants work presented, and 2A | **carried byte for byte**; 2B added after it | - |
| 3 Project in one paragraph | rewritten | v7r1 section 3 (the weekly-session description) |
| 4 Governing documents | rewritten around RAT-40 and specification 1.2 and 1.3 | v7r1 section 4: the full table of older documents with hashes |
| 5.1 Data and holdout | the source, searches, drawn order, dates and two-site lines carried unchanged; the quarantine, holdout, HX-1, HX-2, updater first-run and exposure-record lines dropped as history | v7r1 section 5.1; `doc/HOLDOUT_EXPOSURE_RECORD_v0_3.md` |
| 5.2 Scientific contract | nine lines carried unchanged; the status-vocabulary and method-rankings lines dropped, with a note | v7r1 section 5.2; R2, R3 |
| 5.3 The method contract (E2R-1) and the owner's decisions to 14 November | dropped as a whole; replaced by the decisions that shaped the new system | v7r1 section 5.3; registers v0.23 to v0.31 |
| 5.4 Engineering and process safety | five lines carried unchanged (dependencies, termination, orphan marker, switches, testing order); the rest dropped as true of the old code only | v7r1 section 5.4; Architecture v0.9 |
| 6 Verified technical facts | ten lines carried unchanged; one added | v7r1 section 6 (the updater's internals, the Mode H closure, the MHUP-A line-ending rules, the version-1 test pins) |
| 7 Implementation status | rewritten in short form | v7r1 sections 7.1 to 7.6 (packages, module map, E_1, tests, owner-run tools, not tested) |
| 8 How to work | 8.4 and three lines of 8.5 carried unchanged; 8.1 to 8.3, 8.6 and 8.7 shortened; 8.8 replaced by this cycle's lessons and a selection | v7r1 section 8, above all 8.6 (the tasks T001 to T024) and 8.8 (the full list of lessons) |
| 9 Adding a new method | rewritten for the new system | v7r1 section 9; `doc/METHOD_TEMPLATE/` draft 5 |
| 10 Next work | rewritten | v7r1 section 10 (the MHUP-B road; WF-1C; Method A's diagnostics; coordinated runs) |
| 11 Gates that stay closed | rewritten | v7r1 section 11 |
| 12 Working knowledge | 12.1 to 12.6, 12.8 and 12.9 rewritten in short form; one line of 12.5 carried unchanged; 12.7 (a checklist repeating section 2), 12.10 (resuming the MHUP-B slices) and 12.11 (the deployment work) dropped | v7r1 section 12 |
| Appendix A Identities | replaced by a new, shorter table | v7r1 Appendix A |
| Appendix B Changes | replaced by this one | v7r1 Appendix B |

### B.2 Known limits

- **What Claude re-read of v7r1 for this edition.** In full: sections 0, 0A, 1 to 6 and 11. In part (the opening
  of each paragraph): sections 0B, 7.4 to 7.6, 8, 9, 10 and 12. Not re-read: sections 7.1 to 7.3 and the two
  appendices. Everything dropped from the parts read in part or not at all is old-system record that stays in v7r1.
- **Not verified by running anything:** the suite's present result; the workspace steps of section 12.3; every
  statement about the owner's PC.
- **Verified with tools for this edition:** every hash in section 4 and Appendix A; that `src/`, `tests/`, the root
  `.bat` files and `requirements.txt` are unchanged since `cc0ab73`; the three switches and the allowlist; the masters'
  draw ranges and row counts; that the carried sections and lines equal v7r1's bytes.
- The reviewer's rights region of H-2 is not reproduced here; section 1.4 summarises it and H-2 holds it.
- Of the reviewer's H-2 v4 candidate Claude read section 0 only (its statement of the current position), not the
  inherited chapters. Reviewing that file is not part of this edition.

### B.3 Integrity

US-ASCII; LF; one final newline. The carried sections 1, 2 and 2A are {{CARRIED_LINES}} lines, {{CARRIED_BYTES}} bytes, SHA-256
`{{CARRIED_SHA}}`, identical in H-1 v7r1 (`{{SHA:doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md}}`). Each single
line marked as carried is found exactly once in v7r1 and copied whole. The builder refuses on any failure.

End of H-1 v8.
