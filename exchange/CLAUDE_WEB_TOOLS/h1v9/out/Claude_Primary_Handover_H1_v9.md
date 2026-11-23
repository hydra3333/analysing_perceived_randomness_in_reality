# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v9

**Document:** H-1 under the agreed roles position v0.1r1, section 9 item 4.
**Version:** v9 CANDIDATE, 23 November 2026 (Adelaide, UTC+10:30). **H-1 v8 brought up to date** after build step 1
and the light tidy-up were installed, as the owner agreed (decision log entry 166). Built from the installed H-1 v8's
Git bytes by `exchange/CLAUDE_WEB_TOOLS/h1v9/make_h1_v9.py`, with counted replacements; `H1_v8_TO_v9.diff` beside it is
the exact difference. **Sections 1, 2 and 2A are still H-1 v7r1's bytes, unchanged** (the builder asserts it). The
sections rewritten are listed in Appendix B; everything else is v8's text.
**Status:** CANDIDATE, NOT RATIFIED. The installed Claude handover is H-1 v8 (RAT-41) until the owner ratifies this
edition. It authorises nothing.
**Audience:** any later Claude chat that takes over as primary designer and coder; the ChatGPT reviewer chat; the
project owner.
**Repository:** `hydra3333/analysing_perceived_randomness_in_reality`, public GitHub, branch `main`.
**Baseline described:** `main` on 23 November 2026 after the tidy-up's install (`c7e6ed8`) and its record (`6c3a0fa`).
**The method files are now in the new layout** (build step 1, `0aea10a`) **and commented** (the tidy-up, `c7e6ed8`);
everything else under `src/` and `tests/`, the root `.bat` files and `requirements.txt` is still the old system, as at
`cc0ab73`. Nothing of the new system's engine, trees or commands is coded.
**Replaces, once ratified:** H-1 v8 and its blurb (RAT-41), which stay where they are as history.
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
   - `exchange/DECISIONS/DECISION_LOG.md`, entries 121 to the latest (the owner's own words; entry 147 is RAT-40, entry
     153 is RAT-41, entry 156 is RAT-42; entries 158 to 169 are build step 1 and the tidy-up);
   - the two installed code packages' notes, which show how a package is built, proved and installed here:
     `exchange/CLAUDE_WEB_TOOLS/step1/STEP1_PACKAGE_NOTE_v0_3.md` and `exchange/CLAUDE_WEB_TOOLS/tidy1/TIDY1_PACKAGE_NOTE_v0_1.md`,
     with the reviewer's findings on the first (`exchange/EX_276_ChatGPT.md`) and its passes (`EX_278`, `EX_280`);
   - `exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md` (the joint working principle);
   - the reviewer's findings on the design: `exchange/EX_267_ChatGPT.md`, `EX_269_ChatGPT.md`, `EX_271_ChatGPT.md` (they
     show what the reviewer watches, and EX_271 section 3 holds a test still owed);
   - the reviewer's handover in force (`exchange/CONTINUITY_NOW.md` names it; section 4.4);
   - `exchange/README.md` (the exchange protocol, v0.6) and `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (the local
     runner's rulebook, v0.6; section 8.6).
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
   EX numbers is the owner's choice: the takeovers of 21 and 22 November 2026 used none and were recorded in the
   decision log (entries 134, 157). The outgoing Claude chat stops committing once you start. The reviewer chat stays in role through a
   Claude takeover unless the owner says otherwise.
5. Before any code (once normal work is authorised): name the work item, its risk tier and its reviewer chat
   (section 1.2), and check that the owner has given the go for that build step (section 10).
6. Keep `exchange/CONTINUITY_NOW.md` current after every milestone. Record every owner decision in the decision log at
   once, in his words, reading the time from the clock in the command that writes it. When the chat grows long, write
   the next handover first.
7. **Models (MC-1, section 2):** take over on Opus; section 10 says where Fable (High) is suggested.

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

## 0A. Things that trip a new chat

1. **Two systems share this repository.** The code under `src/` is the OLD system (the proof-of-concept coordinator,
   the contract runner, Mode H, the walk-forward driver and report tool), **except that its method files are now in
   the new system's layout** (build step 1) and carry the coding practices' headers (the tidy-up). The old runner
   still computes them, through a table built from the folder tree. The ratified design's engine, trees and commands
   are **not coded at all**. The older design documents (the Mode H design v0.1r7, the MHUP-B supplements and code
   plan, parts of E2R-1 and R3, the direction document's section 9) are history, except the clauses the
   specification's section 1.2 keeps by reference (section 4.2 below). Do not build from the MHUP-B plan and do not
   install the MHUP-B slices (section 7.3).
2. **The words DRAFT and CANDIDATE inside a ratified file are frozen wording.** A file's status paragraph and the
   decision log say what is ratified. The two design documents in `doc/` still carry DRAFT in their titles.
3. **Read the log for a number before using one.** Register v0.32 (section 4.4) is the newest edition; it records
   RAT-34's install to RAT-40 and its own ratification. For anything later the decision log is the record. Read the
   log for the last RAT number, the last entry number and the last EX number before using a new one. At this
   edition: the last RAT is RAT-42 (the runner's rulebook v0.6); the newest EX is EX_280; the newest decision log
   entry is 169 (the tidy-up installed), and entry 170 records this candidate.
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

## 0B. The state at this edition (23 November 2026)

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
   **the equivalence check `RESULT: PASS - COMPLETE`**: every old development forecast (Powerball 17,280, Oz Lotto
   8,760) computed again with the moved code and equal by `canonical_content_digest`.
7. **The light tidy-up is INSTALLED and proved** (entries 165 to 169; `main` `c7e6ed8`). 37 method files got the coding
   practices' headers and comments; no code changed. The owner accepted leaving E_1's six byte-pinned modules as they
   are (entry 166). Reviewed in EX_279 and EX_280 (PASS). On his PC: a new comments-only check (`RESULT: PASS`), the
   suite unchanged, and the equivalence check again `RESULT: PASS - COMPLETE`.
8. **What is authorised now:** documents and records. Build step 2 needs the owner's own go (section 10); so does
   every install and every run on his PC.
9. **What is owed** is listed once, in section 12.8.
10. **The chats.** This Claude chat took over on 22 November 2026 from H-1 v8 (HO-2 accepted, entry 157) and did build
    step 1 and the tidy-up. The ChatGPT reviewer chat is the one that took over on 21 November 2026; it reviewed EX_266
    to EX_280. On 23 November 2026 the reviewer committed its own H-2 v5 candidate (section 4.4), and the owner agreed
    that Claude refresh H-1 before build step 2 (entry 166): this edition. The owner has not decided on a chat switch.

## 0C. Sections 1, 2 and 2A are carried unchanged: read them with these notes

They are H-1 v7r1's text, byte for byte, because they hold the roles, the reviewer's rights, the review procedure,
the Git rules and the owner's working preferences, none of which the redesign changed. Their section references
are to this edition's sections of the same number ("section 0B, item 4" is item 4 above). Where they are out of date:

1. **Section 1.1, the reviewer chats.** The "present reviewer chat" it describes reached its limit on 21 November
   2026 (entry 128). The chat that took over that day (0B item 8) has the same rights and independence.
2. **Section 1.1, the local runner.** The rulebook is now v0.6 (RAT-42, entry 156): a restrictive baseline that
   names the new system's commands as never run. A narrowly scoped, reviewed amendment is owed before any runner
   rehearsal of the new system (section 8.6).
3. **Section 1.6 describes how code reaches the owner's clone and GitHub,** which is DEV. It still applies to every
   code package. How software then reaches QA or PROD is new and different: the commands of specification
   section 12, from local files, never by Git. Where 1.6 says Claude records the reviewer's files and the owner
   uploads zips, its own first bullet is the current practice: the reviewer commits its own. The rounds of November
   2026 used plain `.md` EX files with no zip (section 12.1).
4. **Section 1.6, the register and the protocol.** Register v0.32 is still the newest (RAT-41; section 4.4); the next
   edition is owed (section 12.8). `exchange/README.md` is now v0.6 (entry 155), where 1.6 says v0.5.
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
ratified; of it, only the method files' layout is built (build step 1). It runs on Windows 11 with Python 3.15. The owner expects the most likely outcome
to be that no method works; a carefully measured null result is valid and useful (section 2A).

---

## 4. Governing documents

SHA-256 values are of the Git content (LF), computed by the builder from `HEAD`.

### 4.1 The authority for the active system (RAT-40)

| Document | SHA-256 |
|---|---|
| `doc/Predictive_Randomness_System_Specification_v0_6.md` | `ee7199d0c17e8bcf877d49e25c6db1a009105c3f8da75ff1ec28b15726216ad0` |
| `doc/Predictive_Randomness_Deployment_Design_v0_12.md` | `e9f778d86c0c1a8a73bfbebf21982aec897a3afdb1296c3029f2ba1da9b58b3d` |
| `doc/CODING_PRACTICES_v0_1.md` | `d64f0101a4fdb21998b2871765bd9b3f06ccb6c7409c7a2d0e9f230cebbd7ddd` |

Each design document is the candidate the reviewer passed in EX_271 with its status paragraph alone changed. The
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
- **The reviewer's handover (H-2).** **In force: H-2 v4, the reviewer's own full edition current to RAT-40, ratified by
  the owner on 22 November 2026 (RAT-41):**
  `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md`
  (`8fa44f67fe37679c3039ae2c9676f86d2bc1269204a9e342f423e157d0612ba8` as ratified; first committed at `30826be`, that
  content at `70719f5`; its blurb's at `adfd973`). Its file name still says CANDIDATE: frozen wording. It replaces H-2
  v3r4 (RAT-36). With RAT-41 the owner asked the reviewer to check that its handover names the installed editions, so
  a later commit may refresh its references. Its section 0 states the current position, the
  four notes of ratification, the build order and the closed OV-1 question as this file does. Before it came the
  v3r10 continuity candidate of 21 November 2026, which Claude wrote on the owner's instruction when the previous
  reviewer chat was lost. **RAT-41 also covers the reviewer's refreshed H-2 v4** (entry 154: main `79406e4`, SHA-256
  `b2837f08f8fd89134aebfbbed5815ca28b00f0ccebd1cb54c92f2f13c50cea2b`; its blurb at `35a2ebf`): those are the bytes in force.
  **H-2 v5** (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5_CANDIDATE_20261123.md` and its blurb, committed by the
  reviewer on 23 November 2026 at `23689ef` and `31db13b`) is a candidate, not ratified. `exchange/CONTINUITY_NOW.md`
  names the edition in force.
- **The register:** `doc/RATIFICATION_REGISTER_v0_32.md`, ratified with this handover (RAT-41; documentary PASS in EX_273).
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
- **The two-site checker** (`src/two_site_results_check_v0_7.py`) drives The Lott's website automatically in its default `--sites both` mode. It was used only to build the first masters (late October 2026, when it also read Lotterywest-GOV's results-search page month by month). **It must never be run that way again** (decision TSC-1: it stays unchanged and is never used again; probe finding A5).
- **One master per game:** `source_data/<GAME>_results_master.csv` with its append-only ledger. `.gitattributes` has
  `source_data/** -text`; never change it. In the new system only PROD runs the updater; QA and DEV receive a
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
- Line endings: Git stores `.md` and `.py` as LF; `.bat` is `text eol=crlf`; `source_data/**` is `-text`. `git archive` applies the `.bat` rule, so hash `.bat` files from `git show`.
- **Python 3.15 makes UTF-8 the default text encoding (PEP 686).** No effect on the project's tests so far.
- **Record files and line endings:** Git stores `results/` files as text, so on the owner's `core.autocrlf=true` checkout any Git operation that rewrites one (a rebase, a checkout) gives it CRLF bytes, and a create-only record whose bytes are checked then refuses. The first Powerball report refused this way: both committed Powerball batch records (`plan.json` and the segment record) were `w/crlf` (`git ls-files --eol`), the plan 12,029 bytes against 12,028 in Git. The owner restored them (delete the files, then `git -c core.autocrlf=false checkout -- <batch folder>`), and the report then ran. Reminder R-011 adds a `results/** -text` rule.
- **Exact arithmetic can be slow at full size:** WF-1B's exact Clopper-Pearson bisection over 10,000-trial binomial tails took over an hour per report until PERF-1. Profile at full size on invented data before trusting a run-time estimate.
- **Byte-code caches:** with `PYTHONPYCACHEPREFIX` set, Python reads and writes cached byte-code only under that prefix, never in the `__pycache__/` folders beside the sources; `-B` (or `PYTHONDONTWRITEBYTECODE=1`) stops the writes; `-I` ignores both environment variables, so an isolated run needs `-B -X pycache_prefix=...` given directly. A sourceless `.pyc` outside `__pycache__/` is still importable. (Reproduced on CPython by the cold-read helper, 3 November 2026; design 4.1.)
- **Reference figures** (fair-draw model, context only, never a veto): Powerball main matches mean 1.4, SD 0.9604; P(>=4) = 0.01826; P(>=5) = 0.00121; Powerball 0.05 per draw. Oz Lotto main-match mean 49/47.
- **Run times measured on the owner's PC (23 November 2026):** the whole suite, one module per process, about 25
  minutes; the equivalence check of every old development forecast about 40 minutes (Powerball about 31, Oz Lotto
  about 9; E_18 and the minimax fits take most of it). In the cloud workspace the suite took about 10 minutes and
  the scored-only equivalence check about 35.
- **New in H-1 v8: DEV's working files are the install source.** If Git rewrites line endings in the owner's
  clone, file hashes change, readiness markers stop matching and a helper may be refused. That fails safe; pinning
  line endings for `src/` in `.gitattributes` avoids it (specification section 20). The owner's checkout uses
  `core.autocrlf=true`.

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
- **Everything else** under `src/` and `tests/`, the root `.bat` files and `requirements.txt` is the old system, as at
  `cc0ab73`, apart from step 1's changes named above and the lines it changed in 14 test files for the moved paths.
- **The suite's known result** (owner's PC and cloud, 22 and 23 November 2026): 45 modules, 571 tests; **three tests
  fail, with eight failed assertions**, on `main` since before step 1: `test_mhupa_launchers` `test_gitignore_lines`
  (one; the owner un-ignored a results folder at `cc665ce`; it prints a set, in a different order each run) and in
  `test_multigame_reader_contracts` `test_master_source_and_ledger_file_hashes` (two sub-tests, pinned to the
  version-1 masters) and `test_only_legacy_e1_allowed_at_boundary` (five). On Windows four symlink tests skip
  (section 6). Compare before and after with `compare_suite_reports.py` (section 12.2), test by test.
- The three safety switches are False and the allowlist is empty in `src/`. A fourth, older switch,
  `ENABLE_CONTRACT_REAL_DEVELOPMENT`, is True in the old contract runner (owner, 31 October 2026).

### 7.2 Data and records

- **Masters, version 2:** Powerball draws 1144 to 1591 (448 rows),
  `e4f2feb8b18fc2dbe389583a189fa26127a648f4da940dd76219ee282170f3e0`; Oz Lotto draws 1474 to 1708 (235 rows),
  `63e3349333f8aa0485b7b067abe70249e39de81c6d02cda1a5710cf1041a4e9e`.
- **In Git:** the sealed Mode H records and reports (`c7622fa`); the development and Mode H score records (`cc665ce`);
  the earlier ranking reports; and the development batch records
  (`results/real/development/wf_batches/<GAME>/<batch>/plan.json` and `segment_*.json`), which list every published
  development forecast: 17,280 Powerball and 8,760 Oz Lotto.
- **Not in Git:** the old forecast run folders (26,040 development, three files each, and 800 Mode H) and attempts
  ledgers exist only on the owner's PC, in his backups and in his ZIP of entry 163. 5,838 Powerball and 2,802 Oz Lotto
  development forecasts were never scored, so they exist only there. The transition check of build step 3 reads them;
  **they stay until then** (entry 163; their cleanup is the owner's own act).

### 7.3 Staged work that is not installed and will not be installed as built

- **The three MHUP-B slices** under `exchange/CLAUDE_WEB_TOOLS/mhupb/` (slice 1, EX_231 PASS; slice 2, EX_237 PASS;
  slice 3, EX_242 PASS) implement the weekly-session design that the course correction replaced. They are a source
  of reviewed code and tests to draw on, never a package to install.
- **The OV-1 kernel** is `exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/slice2_new/src/evaluation/ov1_numeric.py`
  (`2858075e37d2fed447388c770aafe2de9c6d296cd84808078f4cff8cba8d8234`), with its tests beside
  it. The specification's 1.2 names it as the implementation of OV-1's mathematics; the reviewer accepted its proofs
  P1 to P8 at source level (EX_233). Build step 2 carries it into the new system: reuse it, do not rewrite it; any
  change to it is HIGH work.

### 7.4 The design's working record, and the build's

- `exchange/CLAUDE_WEB_TOOLS/simplify/`: every draft of the specification (v0.1 to v0.6) and of the deployment design
  (v0.7 to v0.12), the exact diff between each pair of editions, the builders, and
  `DRAFT_CONTRADICTIONS_FOR_REVIEWER_v0_1.md`. The specification's section 21 says where each finding and decision landed.
- `exchange/CLAUDE_WEB_TOOLS/step1/` and `tidy1/`: the two installed packages, their builders, tools, notes and
  evidence, including the owner's own outputs (`evidence/owner_pc_2026_11_23/` in each). Section 12.2.

### 7.5 Not tested by anyone

**Nothing of the new system's engine, trees or commands has run.** What has run is the moved and commented method
code, under the old runner, on the owner's PC (section 6 has the times). The specification's section 20 and the
deployment design's section 17 list the uncertainties; the costs still to measure in the first rehearsal are the
derived check at each job, a first full fill, a `Check_Forecasts --all`, a rerun, and a backup of a whole tree with
its environment.

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

- **What it is:** Claude Code on the owner's Windows PC carries out task files that Claude writes, in disposable task
  clones that cannot push, and reports what happened. Its rulebook is `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`
  (v0.6, RAT-42, entry 156). Its reports are owner-machine evidence, not reviewer evidence and not acceptance.
- **Rulebook v0.6 is a restrictive baseline.** It allows nothing new: it names the new system's seventeen commands
  as never run, keeps QA, PROD and their backups out of reach (rule 11), and forbids reading `results/`,
  `source_data/` and `transitory_data/` (rule 5). **Before any runner rehearsal of the new system,** write a narrowly
  scoped amendment for that rehearsal, for review and ratification (EX_274). Three deny lines for
  `.claude/settings.json` are proposed in `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_6/COVER_NOTE.md` section 5; the file is
  the owner's. The runner can still run the existing suite in a task clone, as task T024 did.
- **Build step 1 and the tidy-up did not use the runner.** Their checks read the old records under `results/`, which
  rule 5 forbids it, so they ran as reviewed owner-run sheets (section 12.3).
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
owed after build step 3 (section 12.8). The owner's OUTLANDISH_01 method family is in this project's backlog,
"probably first" (owner, 14 November 2026), and comes in only by this route; its own runs are not evidence here.

---

## 10. Next work, in order (planned; the owner decides each step)

1. **Done:** H-1 v8, H-2 v4 and register v0.32 ratified (RAT-41); rulebook v0.6 (RAT-42); the takeover of this chat
   (entry 157); **build step 1** (entry 164, `0aea10a`); **the light tidy-up** (entry 169, `c7e6ed8`).
2. **This edition** (H-1 v9), for the reviewer's check and the owner's ratification, as with v8. The reviewer's own
   H-2 v5 candidate is its business; ratifying the two together is the owner's choice.
3. **Build step 2: the research engine, in DEV** (specification sections 3 to 11), on the owner's own go: the lists,
   the job with its fill and catch-up, scoring, the reports, both OV-1 scores (with the kernel of section 7.3), the
   status file and withdrawal; the checks of 5.6A and 5.8 and both header identities from the first day; RAT-40's
   start-and-end warnings. **Settle in that package:** the exact clause list for E2R-1 section 7 (specification 20);
   specification 17.3's stale pointer to the simplification design v0.1 (entry 157 item 6); pinned line endings for
   `src/` wherever a byte-bound marker is first built (section 6). Build it as steps 1 and the tidy-up were built:
   a builder from a clean clone, the whole suite before and after, planted faults, a reviewed package and an owner-run
   sheet (section 12.3).
4. **Build step 3: trees, installs, backups and restore** (specification 12.1 to 12.6, 13, 14.1), then the transition
   check and PROD's first job. **The owner's question on the updater** (the watchpoint below) is put to him before
   that part is coded. Before a runner rehearsal: the narrow rulebook amendment (section 8.6). The old run folders
   stay until the transition check (section 7.2). **After this step PROD exists and forecasts every week, and new
   methods can be added: the main game.**
5. **Build step 4: the laboratory tools** (specification 12.7, 14.2, 7A, 12.8, `Check_Forecasts`), with the test of
   EX_271 section 3. Until it is built, a fault found in shared code is not improvised around: the affected work is
   held, or the owner restores a backup (specification 17.4).
6. **Then, in the owner's order:** new methods and waves; OUTLANDISH_01's family; the housekeeping of section 12.8.

**A watchpoint for build steps 2 and 3** (found on 22 November 2026; register v0.32; EX_273 section 2; entry 157 item
5). The installed code still has checks from the Mode H study that the ratified design does not make a gate:
`src/methods/_common/contract_dispatch.py` and `master_versions.py` consult the opening record
`source_data/HOLDOUT_OPENED_<GAME>.json` for targets at or after the former holdout, and the updater
`src/results_master_v0_2.py` refuses an update for a game that has none (`holdout_opened`, line 157, used at lines
243, 721 and 817),
although specification 7.1 says it runs "unchanged". The reviewer prefers a narrowly reviewed correction in step 3
that removes ONLY the obsolete Mode H precondition and keeps every Lotterywest-GOV source, overlap, chronology,
record, ledger and concurrency check. **The owner decides before it is implemented.** Fresh DEV, QA and PROD trees
must work under RAT-40 with no Mode H opening or seal as a prerequisite; the obsolete record is not silently copied
into a new tree merely to satisfy old code; no genuine source or ledger check is removed. No design change.

**Models (MC-1; suggestions, the owner decides):** Opus for packaging, sheets, task files, records and handovers.
**Fable (High) for the core of step 2** (the list writer and its invariants, the job's fill and catch-up, the derived
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

This section describes practice, not rules. Section 12.3 is now the practice of build step 1 and the tidy-up, both
installed; section 12.4 is carried from H-1 v7r1 in short form and was not exercised by this chat.

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

### 12.4 Claude Code task files

One task per rehearsal; commands written out in full with absolute Windows paths; each step with its expected PASS
line; a STOP sends the runner to clean-up and the report. Never put `.bat` or any other denied text in a task
command. Read the whole report: every step's command, exit code and output.

### 12.5 Traps in the cloud workspace

The first line is H-1 v7r1's, unchanged:

- **Stopping your own test jobs in the cloud workspace, and nothing else (EX_117 C02).** This applies only to expendable, non-scientific test processes that Claude itself started in its own cloud workspace for this chat (a test suite, a rehearsal, a mutation run, a profile). Never stop them by a name pattern: `pkill -f unittest` matched the chat's own shell twice and killed it. Find the job you started (`ps -eo pid,ppid,etime,cmd`), confirm from its parent and its full command line that it is that job, and stop only that one; if you are not certain, let it finish. **A PID is neither proof of ownership nor permission to stop anything else.** Claude never terminates a project process: no experiment, worker, coordinator, batch, report or uncertain process, on any machine. The protected no-status/no-kill interlock (Architecture section 5C; section 5.4 above) and the owner's separate process-control gates govern those, and nothing on the owner's computer is ever stopped by Claude.
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
- He saves a package ZIP to `E:\TEMP` and extracts it there; the evidence folders of a sheet are `E:\TEMP\<name>_evidence`.
  His ZIP of the whole project folder (entry 163) is on four external drives.

### 12.8 Open items at this edition (23 November 2026)

The live state is `exchange/CONTINUITY_NOW.md`; it overtakes this list.

- **Waiting on the reviewer:** its check of this candidate, when the owner asks.
- **Waiting on the owner:** ratification of this edition; his go for build step 2; his word on reminders R-007
  (proposed dropped) and R-017 (proposed done) (entry 155); the three deny lines for `.claude/settings.json` when he
  chooses (entry 156).
- **Owed by Claude, in order of need:**
  1. Build steps 2, 3 and 4, each on its go, with what section 10 says each must settle.
  2. The owner's question on the updater's Mode H precondition, before that part of step 3 is coded (section 10).
  3. A narrowly scoped rulebook amendment before any runner rehearsal of the new system (section 8.6).
  4. The test of EX_271 section 3, in build step 4.
  5. The next register edition, when a code package or a handover next travels (section 1.6): it records RAT-41's
     install, RAT-42, build step 1, the tidy-up and what follows.
  6. A new draft of `doc/METHOD_TEMPLATE/` for the new layout, after build step 3.
  7. The measurements of section 7.5, in the first rehearsal.
- **Done since H-1 v8:** the owner's ZIP (entry 163); the suite's result established (section 7.1); the pass over
  `exchange/OWNER_REMINDERS.md` and `exchange/OWNER_ROADMAP.md` (entry 155; two reminders await his word, above).
- **Later, and only when the owner asks:** the deferred performance study (R-006;
  `doc/Deferred_Performance_Engineering_Proposal_v0_1.md`: profile real run times before choosing any speed-up) and the
  simplicity review after full implementation (KISS-1).
- **Small leftovers the owner may choose to clear:** deleting `venv.bak` and Python 3.14; the duplicate exploration
  note in `doc/`; the old EX copies in `review/`; after step 3's transition check, the old run folders.

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

SHA-256 of the Git content at `HEAD` (LF unless noted), computed by the builder. A file cannot name its own hash:
this file's and its blurb's are in the decision log entry that records each edition.

| File | SHA-256 |
|---|---|
| `doc/Predictive_Randomness_System_Specification_v0_6.md` | `ee7199d0c17e8bcf877d49e25c6db1a009105c3f8da75ff1ec28b15726216ad0` |
| `doc/Predictive_Randomness_Deployment_Design_v0_12.md` | `e9f778d86c0c1a8a73bfbebf21982aec897a3afdb1296c3029f2ba1da9b58b3d` |
| `doc/CODING_PRACTICES_v0_1.md` | `d64f0101a4fdb21998b2871765bd9b3f06ccb6c7409c7a2d0e9f230cebbd7ddd` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v8.md` | `8230e3dfecca528d185153e46a2173ef8a7a4d8fbc41695cc3b2bbbfcb20c45e` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v8_introductory_blurb.md` | `586ececea64fca65b1ef3872a9fec60f1d7c659e0da408eb61e62d996d556d66` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md` | `b2837f08f8fd89134aebfbbed5815ca28b00f0ccebd1cb54c92f2f13c50cea2b` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122_introductory_blurb.md` | `5f113e4c4dca8648ccbf2a05e9a192bebf76d4473ad21e02c58de0b54a6bfcd5` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5_CANDIDATE_20261123.md` | `54ce9f3bd62ea0bac4e591d03904af34bf3ae444e5510af2aafc62057204a8af` |
| `doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md` | `7d572400b941ad423978a7542d6c32fb73c934f0057240dbc5138898112bd53b` |
| `doc/HANDOVER/AI_Roles_Transition_Record_H3_v1r1.md` | `8b01c57fd8804029906e1e9c87e8ecef18edb914a269e43a45dac90880703ce5` |
| `doc/RATIFICATION_REGISTER_v0_32.md` | `f59d1911279e7e95a952a14c3a0c68422ba0f4e67f91ffd5369eb73c606c9acb` |
| `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md` | `5067aa520990b8ccc8521a04f3581424100cdd94994f5b9e3cb9e37863685339` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` | `f92f17f60db63990fc10a663778ec8d6a2b0737c9232895f1ee0af76ffdfa632` |
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

Commits named in this file: `c7e6ed8` (the tidy-up installed) and `6c3a0fa` (its record); `0aea10a` (build
step 1 installed); `31db13b` and `23689ef` (the reviewer's H-2 v5 candidate); `79406e4` and `35a2ebf` (the
refreshed H-2 v4 and its blurb); `cc0ab73` (the old code baseline); `c7622fa` (the Mode H results and version-2
masters); `cc665ce` (the score records); `cf1c6d9` (the first commit after the history clean-up). H-1 v8
Appendix A names the commits of the design rounds.

---

## Appendix B. What changed from H-1 v8

### B.1 What changed from H-1 v8

| v8 section | In v9 |
|---|---|
| Header | rewritten for the state after the tidy-up; status CANDIDATE |
| 0 First actions | item 2: the newer entries and the two package notes added to the reading list, and the protocol's and rulebook's editions; item 4: the takeover of 22 November 2026 added |
| 0A Things that trip a new chat | item 1: the method files are in the new layout; item 3: the newest numbers; items 10 and 11 added (text-reading tests and pinned E_1 files; `.gitignore` and `*.log`) |
| 0B The state | rewritten: items 1 to 4 kept; item 5 notes (b) and (c) brought up to date; items 6 and 7 (step 1, the tidy-up) new; items 8 to 10 rewritten |
| 0C Notes on sections 1, 2, 2A | items 2 (rulebook v0.6), 4 (register, `exchange/README.md` v0.6) and 6 (the owner's lists) brought up to date |
| 1, 2, 2A | **carried byte for byte** (still H-1 v7r1's bytes) |
| 2B, 4.1 to 4.3, 5.1, 5.2, 5.4, 11 | unchanged |
| 5.3 The owner's decisions | one line: the owner's ZIP is done (entry 163) |
| 3 Project in one paragraph | one sentence: the layout is built |
| 4.4 History and working documents | the refreshed H-2 v4 (entry 154) and the H-2 v5 candidate added |
| 6 Verified technical facts | one line added (run times on the owner's PC and in the cloud) |
| 7 What exists today | rewritten (the installed layout and tidy-up; the suite's known result; the records and run folders; the build's record) |
| 8.6 The local runner | rulebook v0.6 and the narrow amendment; why the build did not use the runner |
| 8.8 Lessons | eight lessons from step 1 and the tidy-up added at the top; the rest unchanged |
| 9 Adding a new method | one clause: the existing families are the worked example |
| 10 Next work | rewritten from step 2 on; the watchpoint now names the owner's question and the reviewer's preference |
| 12 intro, 12.1, 12.2, 12.3, 12.6, 12.8, 12.9 | brought up to date; 12.3 rewritten as the practice of the two installed packages |
| Appendix A | rebuilt from HEAD with the files a new chat now needs |
| Appendix B | this one |

Nothing binding was dropped: every v8 passage that was replaced described a state that has since moved on, and the
decision log entries 154 to 169 hold the record.

### B.2 Known limits

- **Verified with tools for this edition:** every hash in section 4 and Appendix A (computed by the builder from
  `HEAD`); that sections 1, 2 and 2A equal v8's and v7r1's bytes; the layout's counts (40 `VARIANT.json`, 40 `method.py`);
  the suite's and the equivalence check's results (the owner's unedited outputs, filed as evidence).
- **Not re-checked for this edition:** the hashes in section 4.2 and 4.3 beyond the builder's comparison with v8
  (unchanged files); statements about the owner's PC other than those in his outputs.
- Of the reviewer's H-2 v5 candidate Claude read the status lines only; reviewing it is not part of this edition.

### B.3 Integrity

US-ASCII; LF; one final newline. The carried sections 1, 2 and 2A are identical to H-1 v8's and to H-1 v7r1's (the
builder asserts both). Every replacement's old text is found exactly once in H-1 v8. The builder refuses on any failure.

End of H-1 v9.
