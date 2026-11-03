# Takeover test - H-1 v1r8 (DOC-11 rehearsal copy at 4357308)

Test limits observed: read-only; nothing opened under `source_data`, `results` or `transitory_data`; no web access;
no lottery outcome printed or computed. H-1 section 12.9's workspace set-up (step 2) and full Linux suite (step 3)
were SKIPPED, as instructed.

---

## PART 1 - First substantive reply to the owner

Hello. I am the new Claude chat taking over as primary designer and coder. I have read H-1 v1r8 in full, its
section 0 reading list (H-2, register v0.24's newest section, the MHUP-1 design v0.1r5 sections 0 to 10 with
Appendices J and K, the direction document, the rulebook, your roadmap and reminders) and EX_129 to EX_132. This
reply is what section 0 item 4 asks for. I will not start any work until you say so.

**What is implemented (installed and running).** The code has not changed since PERF-1 (`3fce327`, 1 November);
I checked that nothing under `src/`, `tests/` or the launchers has changed since. All 40 method variants are
released in both games: E_1 revision 2 plus 39 variants of E_2, E_3, E_4, E_6 to E_10 and E_17 to E_19. The
walk-forward driver ran the first batches on past draws (Powerball 17,280 runs, Oz Lotto 8,760, all SUCCESS). The
scorer and ranking report (WF-1B) and its speed-up (PERF-1) are installed. The first reports found nothing that
departs from fair draws. That is development evidence only. The suite is 471 tests in 36 modules. Three safety
switches are False. The fourth, `ENABLE_CONTRACT_REAL_DEVELOPMENT`, is on, for runs you authorise. The scientific
allowlist is empty.

**What is designed and ratified, but not built.** MHUP-1 ("Mode H, the results update and the prospective mode"),
design v0.1r5. It went through four review rounds (EX_125 to EX_131). You ratified it as a whole on 3 November
(MHUP-R), with Q1 = option A and the decisions Q10, Q11, B02, B04, C03 and D1 to D3. It will be built as two code
packages:
- **MHUP-A:** E_1 revision 3; a version-2 reader so the results file can grow; the binding and ticket gates; the
  study manifest and the opening record; the Mode H batch; the install and release records; the updater v0.2
  with its four additions; `Run_Evaluation.bat`; the byte-code lines in `Run_Experiment.bat`; `process_check.py`.
- **MHUP-B:** your weekly session (forecast N, reveal N, score N, then N+1, then freeze the next draw before its
  deadline), with its ledgers and your one-page checklist.

Mode H is a precommitted holdout evaluation, not pre-draw forecasting: ten sealed draws per game, scored once,
with Powerball 1585 and 1586 flagged.

**What is still unresolved.**
- Q7: whether the rule against displaying holdout draws is relaxed after Mode H. It must be decided before
  Approval 2.
- At MHUP-A's approval: whether to rerun the Windows POC suite, and confirming the backup of `results/` and
  `source_data/` (asked 2 November).
- Walk-forward preregistration, E_54's feed timing, the formulas for the remaining methods, and WF-1C's open
  choices.

**Where we are now.** We are at step 2 of your staged handover (HO-2). DOC-11 (H-1 v1r8, its blurb, register v0.24,
the design and the direction document in `doc/`) is meant to be reviewed by the reviewer chat (Step 1.1, EX_133 and
EX_134), then ratified and installed by you, before I start. **This is the first thing I need you to confirm.** In
the copy I was given:
- H-1 v1r8 and register v0.24 both still say **CANDIDATE**, and H-1's own status line says "until it is ratified
  and installed, H-1 v1r7 stands";
- the install commit is labelled "DOC-11 (rehearsal copy)";
- there is no EX_133 or EX_134 in `exchange/`.

So I cannot tell from the repository whether Step 1.1 happened, or whether v1r8 is the handover in force.

**The next tasks, in order, with what each needs.**
1. Finish the takeover. You pass this reply to the reviewer. I answer its questions myself, before seeing its
   suggested answers. Any material discrepancy is resolved. Then you explicitly authorise normal work.
2. MHUP-A (HIGH). Code and tests, mutation checks, LF and CRLF rehearsals, the reviewer's code review (R-2) with
   the demonstrations EX_131 section 4 requires, and Claude Code rehearsal T016. Then your install by Appendix J
   (two commits; the install holds the updater lock). At its approval you make the POC-suite choice and confirm
   the backups.
3. MHUP-B (HIGH), the same way, with rehearsal T017. It must be installed before Approval 1, or else only after
   the Mode H score is sealed.
4. Per game, each separately: your Q7 decision; Approval 1 (freeze the study manifest and write the opening
   record); the updater's offline self-test under Python 3.15; Approval 2 (the first update, which must bring in
   all ten holdout draws or write nothing); Approval 3 (the Mode H batch); Approval 4 (score, report, seal). Then
   your GOAL-1 "developed" decision and the first weekly session.
5. Register v0.25. Then WF-1C, wave 3, the NL-means discussion, waves 4 to 11 and the ensembles last.

Your planning target (ST-5, about 13 to 15 November; first frozen forecasts Oz Lotto 1709 and Powerball 1592) was
set before HO-2 added a review round and this takeover. FB-1 says slip rather than rush.

**The restrictions I will keep.**
- *Safety and data:*
  - No lottery-results searches.
  - No contact with `oz.lotterywest.com`, The Lott or any lottery site, and no new scraper.
  - Never display or compute with Powerball 1577 or later, or Oz Lotto 1694 or later.
  - I never open `source_data`, `results` or `transitory_data` myself.
  - Never clear, bypass or suggest bypassing the orphan marker. Never terminate any project process.
  - No switch or allowlist change.
  - No results updater run of any kind before MHUP-A is installed and you separately approve the first update.
    The bare `Run_Results_Updater.bat` runs an update.
  - The two-site checker is never run again in its default mode.
- *Scientific:*
  - Strict N-1, and T-05.
  - Mark, never suppress. Statistics never acts as a gate.
  - Goldens are never recalibrated, and an expected hash is never "refreshed".
  - Mode H is described honestly, as a precommitted holdout evaluation.
- *Operational:*
  - Every HIGH item gets design review before code, and review by the other model.
  - The release rule applies.
  - Each run, batch, report, approval and weekly session is your separate decision.
  - I commit only inside `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`. I never use `git add -A`, and I
    never push while you may have local commits waiting.
  - I never write your name in anything committed.

**What I believe I am authorised to do now.**
- Read and check: I have checked the hashes, as listed below.
- Write this reply.
- Answer the reviewer's questions.
- Ask you questions.

**What I must not do without your further approval.**
- Start MHUP-A in any form (code, packages, task files), even though H-1 calls it the next task. The ratified
  design authorises no code, run, install or update.
- Run anything that touches your machine.
- Commit or push anything during the takeover, unless you tell me to. That would include recording EX_133 and
  EX_134 and updating your roadmap.

I have **not** run the full Linux suite (section 12.9 step 3). Section 7.4 says E2R-T12, which starts up to six
worker processes, needs your approval for each run context. HO-2 also says to execute nothing. I would like your
"yes" first.

**What I checked, and the discrepancies.**
- **Hashes.** I checked 75 file hashes in sections 4 and 7 and Appendix A against `git show HEAD:<path> | sha256sum`.
  All 75 match. One needs explaining: `2e23d550...` is the hash of the v0.6 fixture
  `tests/fixtures/coordinator_v0_6_baseline/...`, not of today's coordinator. I also checked five historical
  hashes at their own commits (all match), and all 17 lines of DOC-11's manifest (all match; H-1's own hash
  agrees). Every commit ID H-1 cites exists.
- **Hashes I did not check:**
  - the two master hashes in 7.5, because I may not open `source_data`;
  - the five computed digests in 7.3, which are run outputs, not file hashes.
- **Discrepancies.**
  - The status question above (CANDIDATE; no EX_133 or EX_134).
  - Your roadmap stops at 2 November. Its item 10c says "Next: your ratification of design v0.1r5 as a whole,
    then MHUP-A code". It does not mention MHUP-R, DOC-11 or HO-2.
  - H-1 12.8 cites reminder R-015 "added with DOC-11", but there is no R-015 in `OWNER_REMINDERS.md`. R-013 is
    still OPEN there.
  - H-1 10.2 and 12.8 say the code is paused "until DOC-11 is installed". HO-2 says work resumes only after this
    verification and your authorisation. I am following HO-2.
  - EX_132 asked the reviewer to number any reply EX_133. H-1 gives EX_133 to the Step 1.1 review request.
  - In a few places the direction document is older than the design (for example "CATCH-UP starts at its
    install", where the design says release record). I will follow the design.

**My questions for you.**
1. Is DOC-11 installed in its ratified form? What did Step 1.1 (EX_133 and EX_134) conclude?
2. Is the previous Claude chat retired, or still committing to `exchange/`?
3. May I run the full suite, including E2R-T12, in my cloud workspace now?
4. Do you still hold to the 13 to 15 November target?
5. Should the reviewer's questions reach me without its suggested answers? I suggest you paste only the
   questions.

Model: Opus 5.5 is fine for this reply and the follow-up questions. I would suggest Fable (High) only when MHUP-A's
core code starts.

**Paste for the ChatGPT reviewer chat** (no zip; this text only):

```
To the ChatGPT reviewer chat: the new Claude chat's first takeover reply (HO-2 step 3) is above. Please assess its
understanding and send the owner targeted questions only; the owner will hold your suggested answers and
assessment until Claude has answered.
```

---

## PART 2 - Gaps for the handover's author

Hash check summary:
- H-1 holds 84 distinct 64-hex values. I checked 75 file hashes (sections 4, 5.3, 7 and 8.7, and Appendix A)
  against `git show HEAD:<path> | sha256sum`. All 75 match. The coordinator AST anchor matches the v0.6 fixture
  file, not `src/Powerball_Experiment_Coordinator.py`, which is `6d202f5e...`; see item 6.
- Two more full historical hashes (rulebook v0.2 at `7bb0bfd^`, exchange README v0.4 at `63c19e7`) and three
  abbreviated ones (Architecture v0.8, exposure record v0.2, template draft 3) match at their commits.
- Not checked: 2 master hashes (they are in `source_data`, so off limits) and 5 computed E_1 digests in 7.3.
- DOC-11 manifest: 17 of 17 match. H-1 v1r8 is `b54c3545...`, the same as its manifest line. The commit adds
  exactly the manifest's files plus the manifest itself.
- Register v0.24 section: the 14 hashes I tried all match.
- All 46 commit IDs cited in H-1 exist.

1. **MAJOR - The installed copy does not say it is in force.**
   - Where: H-1 header, "**Status:** CANDIDATE for the reviewer's check and the owner's ratification with
     register v0.24 (DOC-11). Until it is ratified and installed, H-1 v1r7 stands."
   - Where: register v0.24 line 3, "v0.24 CANDIDATE ... (not yet ratified)".
   - Also: no EX_133 or EX_134 is committed, and the commit is "DOC-11 (rehearsal copy)".
   - Problem: the blurb says to use it only after Step 1.1 is resolved and DOC-11 is installed. Read literally,
     a new chat is therefore governed by v1r7, whose next step (the Mode H design) is already done. Nothing tells
     the new chat what to do when the status lines still say CANDIDATE.
   - Fix: make sure only the RATIFIED build (item 2) is installed. Add to H-1 0.3: "If this file's or the
     register's status line reads CANDIDATE, or EX_133/EX_134 are missing, stop and ask the owner which
     handover is in force."

2. **MINOR (fails closed) - The RATIFIED build cannot run as written.**
   - Where: `review/DOC11_Claude_Handover_v1/make_register_v24.py`, whose RATIFIED version line is
     `'... OWNER-RATIFIED @@DATE@@ (content reviewed in @@EX@@)'`.
   - Problem 1: `build_doc11.py` replaces only `@@DATE@@`, then asserts `b'@@' not in`, so the RATIFIED build
     aborts.
   - Problem 2: `build_doc11.py` passes `sys.argv[6:8]` (the H-1 SHA and the blurb SHA) to the register builder,
     but its usage line documents only `[@@DATE@@ text]`. The H-1 SHA is also needed before H-1 is built, because
     the register is built first.
   - Risk: a hurried finaliser might install the CANDIDATE build instead.
   - Fix: build H-1 first and compute its SHA in-process; replace `@@EX@@` (with "EX_133 and EX_134"); fix the
     usage line; run the RATIFIED path once in the e2e.

3. **MAJOR - The pause is tied to the wrong event.**
   - Where: H-1 10 item 2, "**The owner has paused the code until the documents are updated** (3 November
     2026)".
   - Where: H-1 12.8, "The design is ratified; the code is paused until DOC-11 is installed."
   - Problem: both lift the pause at DOC-11's install. HO-2 step (4), blurb step 5 and H-1 0.4 say work resumes
     only after the verified takeover and the owner's explicit authorisation. A new chat told "DOC-11 is
     installed" could reasonably start MHUP-A.
   - Fix: in both places, "paused until the staged takeover (HO-2) is verified and the owner explicitly
     authorises normal work (section 0 item 4)".

4. **MAJOR - The roadmap is stale and points straight at MHUP-A code.**
   - Where: `exchange/OWNER_ROADMAP.md`. It was last updated "2 November 2026 (night)" (committed `79f6ea6`,
     before MHUP-R).
   - Its 10c ends: "Next: your ratification of design v0.1r5 as a whole, then MHUP-A code (Fable for the core)."
   - Missing: MHUP-R, DOC-11, HO-2 and the pause. The header cites `doc/Direction_for_operational_procedures_v0_1.md`
     (removed at `6de0d99`) and stock-take v0_7.
   - Problem: H-1 0.3 tells the new chat to use "exchange/OWNER_ROADMAP.md (item 10c) as the list". This is the
     single most likely route to the wrong action.
   - Fix: commit a roadmap update before the switch: 10c "design ratified (MHUP-R); now DOC-11 and the staged
     takeover (HO-2); MHUP-A only after the owner's authorisation"; fix the two stale paths.

5. **MINOR - The reminders do not match H-1.**
   - H-1 12.8 says "R-015 the owner's two choices at MHUP-A's approval and Q7 (added with DOC-11)", but there is
     no R-015 in `exchange/OWNER_REMINDERS.md`. DOC-11 touches only `doc/` and `review/`, so it cannot add one.
   - R-013 is still "Status: OPEN" (H-1 says it is closed by DOC-11).
   - R-007, R-008 and R-010 still say "next package", not "folded into MHUP-A".
   - The standing reminders cite stock-take v0_7 and `doc/Direction_..._v0_1.md`, and call model choice
     "provisional ... To be carried into the next H-1" (it is now MC-1).
   - The register's future-actions list covers Q7 and the two choices, so this is not MAJOR.
   - Fix: commit the reminders update (add R-015; close R-013 on install; retarget R-007, R-008 and R-010) with
     the roadmap, before the switch. Or reword H-1 12.8 to "to be added".

6. **MAJOR - The hash-check instruction collides with a hard rule.**
   - Where: H-1 0.1 and 12.9 step 1, "check the hashes in sections 4 and 7 and Appendix A".
   - Problem 1: section 7.5 includes the two master hashes ("Masters: Powerball `ce0ae7e7...`; Oz Lotto
     `4a6cecc2...`"). Checking them means reading `source_data/`, which the blurb forbids ("Never open anything
     under `source_data` ... yourself").
   - Problem 2: section 7.3's five digests are computed outputs, not file hashes. One is the real target-1577
     view.
   - Problem 3: 7.2 line 302 puts `(`2e23d550...`)` beside `src/Powerball_Experiment_Coordinator.py`, which hashes
     to `6d202f5e...`; it is the v0.6 fixture's file hash.
   - Fix: "check the file hashes of sections 4 and 7 and Appendix A, except the master hashes in 7.5 (never open
     `source_data`) and the computed digests in 7.3". In 7.2 and Appendix A, add "(SHA-256 of the v0.6 fixture
     file, not of the current coordinator)".

7. **MAJOR - May the new chat run the suite during the takeover?**
   - Where: H-1 12.9 step 3, "Run the whole suite on Linux ... This proves the tools and the workspace before any
     change". The blurb says "work through H-1 section 12.9 in your own cloud workspace".
   - Conflict 1: H-1 7.4 says "E2R-T12 ... needs the owner's approval for each run context".
   - Conflict 2: HO-2 and blurb step 3 say "executes nothing".
   - Conflict 3: 0.7 says 12.9 "builds and runs nothing on the owner's machine", which implies cloud runs are fine.
   - Result: a new chat either breaks 7.4 or skips 12.9. Some accepted tests also read the development masters
     in the clone.
   - Fix: one sentence in 12.9: "During the staged takeover the owner [authorises / does not authorise] the full
     suite including E2R-T12 in Claude's cloud workspace; otherwise use `run_e2r_suite_without_t12.py` and ask."

8. **MAJOR - The blind-answer step conflicts with the record-keeping rule.**
   - Where: HO-2 step (3) and blurb step 4: "Answer those questions yourself, before you see the reviewer's
     suggested answers or assessment".
   - Conflict: H-1 1.6, "Claude records every EX file from both sides in `exchange/`, unchanged", and 12.1, "The
     owner uploads the reviewer's files to the Claude chat; Claude commits them".
   - Problem: if the reviewer's assessment and suggested answers come as one EX file, the new chat has to read
     it to commit it, which defeats the verification gate.
   - Also unclear: whether the takeover reply, the questions and the answers are EX messages, and their numbers
     (EX_135 and on?).
   - Fix: a short paragraph: the owner relays only the questions (an EX file holding the questions alone, or a
     paste); the reviewer's assessment and suggested answers are held by the owner and given to Claude, and
     committed, only after Claude's answers are sent; give the numbering.

9. **MINOR - EX number collision.**
   - EX_132 says "if you do reply, please number it EX_133".
   - H-1 10 item 2 and 12.1 say "the Step 1.1 review of the Claude handover package is EX_133 and the reviewer's
     reply EX_134". That also leaves unclear who sends EX_133.
   - Fix: "If the reviewer replied to EX_132 as EX_133, the Step 1.1 request takes the next free number; always
     check the highest committed number."

10. **MINOR - Commit and push rights during the takeover, and the outgoing chat.**
    - The blurb says the owner "is the only one who commits project files and pushes" and that Claude "commit[s]
      only inside `exchange/` ...".
    - H-1 12.1 says Claude pushes `exchange/` commits. HO-2 says "before any work at all".
    - Unclear: whether the new chat may commit or push (EX_133/134 records, the roadmap) before authorisation,
      and whether the authoring chat is retired. Two Claude chats with push rights to `exchange/` risk rejected
      pushes and rebases (the CRLF trap of 12.6).
    - Fix: "During the takeover the new chat commits and pushes nothing until the owner says so; the outgoing
      chat stops committing once the new chat starts (or is retired on <date>)." Reword the blurb as "the only
      one who commits project files (Claude pushes its own `exchange/` commits)".

11. **MINOR - Speculative code while waiting.**
    - Where: H-1 8.2, "A speculative candidate built alongside the design is fine".
    - Pressure from: the design's section 8 table ("Thu 5 - Mon 9 Nov | MHUP-A code") and ST-5's dates.
    - Problem: a new chat might draft MHUP-A in its workspace "while waiting", which is arguably "implementing"
      under HO-2.
    - Fix: add to 0.4, "including no draft or speculative code, task files or packages in your workspace".

12. **MINOR - The schedule has not been re-baselined for HO-2.**
    - Where: H-1 10 item 3 still quotes "installed by about 13 to 15 November ... Oz Lotto 1709 ... Powerball
      1592".
    - The design's 8 table has ratification on "Wed 4 - Thu 5 Nov" and MHUP-A on 5 to 9 Nov.
    - Problem: HO-2 adds a review round and a takeover verification, and nothing says whether the owner moved
      ST-5.
    - Fix: one line in 10 item 3, "HO-2 adds about N days; the owner [has / has not] moved ST-5; FB-1 applies".

13. **MINOR - The direction document contradicts the design, not just "looser".**
    - The four contradictions, by section:

      | Direction v0.2r1 | Says | The design |
      |---|---|---|
      | Section 5 step 4 | "a newly released revision has none until its walk-forward is done" | 6.3: it joins at its next session; back-history is optional and separate |
      | Section 7 | "its CATCH-UP record starts at its install" | 4.3: the release record's date, not install |
      | Section 4 | Mode H statement without "the environment" and "all planned attempts" | The ratified wording includes both |
      | Section 11 | Lists Q1, Q4, Q5, Q6, Q8 and Q9 as open | All decided by MHUP-R |

    - H-1 section 4 says only "the design prevails where it is looser", and DIR-1 calls the document "to be
      referred to and checked against".
    - Fix: add these to register v0.24's out-of-date statements (or to H-1 section 4's row): "superseded by the
      design: 5(4), 7 (install -> release record), 4 (wording), 11 (decided)".

14. **MINOR - The MHUP-A rulebook and deny additions differ between documents.**
    - Register future action 1 names four: "`Run_Evaluation.bat`, `Method_Mode_H.py`, `process_check.py` and
      `results_master_v0_2.py`".
    - Design section 8's MHUP-A bullet names two: "(`Run_Evaluation.bat`, `Method_Mode_H.py`)".
    - `Bash(*results_master*)` already exists in `.claude/settings.json`.
    - Fix: list it in register v0.24's out-of-date statements ("design 8: the register's four prevail") or in H-1
      10 item 3.

15. **MINOR - The blurb drops items H-1 keeps.**
    - "Still open" names only Q7 and the POC-suite choice. It omits the backup confirmation (register future
      action 2(b); H-1 12.8 "asked 2 November 2026") and that Q7 must be decided before Approval 2.
    - The reading list omits H-3 and `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`, which H-1 0.2
      lists.
    - Fix: add both to "Still open"; add "and the rest of H-1 section 0's list" to step 1.

16. **MINOR - The rebuild tools are not where H-1 says.**
    - H-1 12.2: "`doc11/` ... holds DOC-11's builders: `make_register_v24.py` with `reg24_section.md`,
      `make_h1_v1r8.py`, the H-1 v1r8 blurb, `build_doc11.py` and `e2e_doc11.sh`". `exchange/CLAUDE_WEB_TOOLS/doc11/`
      holds neither of the last two: `build_doc11.py` is only in `review/DOC11_Claude_Handover_v1/`, and
      `e2e_doc11.sh` is nowhere in the repository.
    - `exchange/CLAUDE_WEB_TOOLS/README.md` has no `doc11/` section.
    - `build_doc11.py` hard-codes `REPO = '/home/claude/analysing_perceived_randomness_in_reality'` and its
      verifier template path.
    - The README's 3.15 venv package list (`numpy scipy psutil`) differs from H-1 12.3's seven packages.
    - Fix: commit `build_doc11.py` and `e2e_doc11.sh` to `doc11/`, add a README section, and align the package
      list.

17. **NIT - The design's own status text is stale, and H-1 does not warn of it.**
    - The design header still reads "FOR THE OWNER'S RATIFICATION", and section 1 says "the design as a whole is
      ratified after this recheck".
    - Its work-item card says the direction copy "goes into `doc/` with the next document package (R-013)".
    - The section 8 table has the owner ratifying on "Wed 4 - Thu 5 Nov".
    - This is correct by design (byte-identical to EX_132), but a new chat sees conflicting status.
    - Fix: in H-1 section 4's design row, "its header and footer predate MHUP-R; byte-identical to EX_132; the
      register records the ratification".

18. **NIT - H-2 v1r8 calls itself a draft.**
    - Its title has "(DRAFT)" and its footer says "End of H-2 v1r8 DRAFT - NOT OWNER-RATIFIED", while its status
      line says OWNER-RATIFIED.
    - H-1 notes that H-2's checkpoint facts are stale, but not this.
    - Fix: add a half-sentence to H-1 Appendix A's H-2 row: "its DRAFT title and footer are historical; the
      register's status prevails".

19. **NIT - Small count and status slips.**
    - H-1 10 item 3 says "Appendix J's 19 steps", but the table has 20 rows (steps 0 to 19).
    - H-1 1.6 names a verifier only for DOC-10, although DOC-11 has `VERIFY_DOC11_INSTALL.py`.
    - `doc/METHOD_TEMPLATE/README.md` is titled "draft 4" but its Status line says "DRAFT 3" (pre-existing).
    - DOC-11 carries no blurb diff (DOC-10 carried `H1_blurb_v1r6_to_v1r7.diff`).
    - Fix: "steps 0 to 19"; mention DOC-11's verifier; fold the template Status into draft 5; add the blurb diff.

20. **MINOR - Cross-check: could a reader think the ratified design authorises building MHUP-A now?**
    - These texts are clear that it does not:
      - blurb steps 3 and 6;
      - H-1 0.4 and section 11 ("neither does the ratified MHUP-1 design");
      - register MHUP-R ("The design authorises nothing");
      - EX_131 section 4.
    - The routes to a wrong reading are items 3 (the pause tied to DOC-11's install), 4 (the roadmap's "then
      MHUP-A code"), 11 (speculative candidates) and 12 (a schedule that implies coding from 5 November).
    - Fixing 3 and 4 removes the material risk.
