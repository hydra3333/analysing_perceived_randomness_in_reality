# HO-2 replacement-Claude takeover: ChatGPT review of predecessor cross-check v0.2

Date: 10 November 2026 (Adelaide)
Project: hydra3333/analysing_perceived_randomness_in_reality
Repository reference: main c48ac3c393d2eab30014e6200d427b76d90f47ac
For: the project owner, then the replacement Claude as a controlled handback
Exchange number: NONE. This is not EX_163.
Scope: documentary and operational review, not an MHUP-A code/package PASS.

## 1. Basis and verdict

I read the predecessor's entire v0.2 third cross-check (17,909 bytes, US-ASCII,
CRLF; SHA-256 e4c5e0d699ea84396fc5f5bd0f5c760c8619bc79f9011d366c202acd50b3a1b3)
and the replacement's original Q1-Q9 blind answers. The predecessor reports that it
independently verified the answers' bytes and checked their text word for word.
I cross-checked the critical claims against GitHub files at the pinned commit:
CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md v0.4; .claude/settings.json;
exchange/CLAUDE_WEB_TOOLS/check_task_commands.py; register v0.26;
design v0.1r6 (especially 4.4, 6.1, Appendix J, L-I4);
exchange/OWNER_REMINDERS.md; H-1 v1r10r3 delta; integrated/PLAN.md.
I did not execute a test, build, inspect outcomes, or amend the repository.

Disposition: TAKEOVER PASS. No further blind questions needed. The replacement's
answers Q1-Q9 demonstrate the requisite understanding of current status, A1,
C01-EFF, freezes, the two-commit release, and safeguards. Its own Q7 states the
correct Appendix J sequence, and its Q6 identified the future settings-deny risk.

F1-F4 are valid package-development corrections; F5 is a documentary correction
to review/handover wording, NOT a defect in the replacement's answers; F6-F9
are valuable clarifications. None is a takeover BLOCKER. F2 and F3 ARE
pre-T016 blockers until a reviewed, owner-authorised execution/evidence route exists.

## 2. Finding-by-finding dispositions

### F1 - ACCEPT, with an identity/freeze qualification

The register v0.26 already says that the owner edits .claude/settings.json
"with MHUP-A's install" (section near the v0.25 MHUP-A narrative; also its
future action 1). At the pinned main, the settings file does NOT yet contain
Bash deny lines naming process_check.py or install_records.py. Its current
Bash(*results_master*) and Bash(*.bat*) patterns do block several other commands.

It is sensible to stage the conflicting process_check/install_records denies
AFTER T016's accepted run, so the runner does not evade or circumvent the
deny layer. A separate owner commit BEFORE Appendix J step 0 would keep the
install worktree clean and the overlay-path staging exact. The published
register expressly requires a process_check.py deny; treating a new
install_records.py deny as desirable additional protection is a proposed
owner-reviewed choice, not a pre-existing explicit register mandate.

IMPORTANT: that settings-only commit advances live main. The final package's
manifest records a base_commit, and PRE allows base or a descendant subject
to byte checks. Explicitly prove that the later settings commit is an
allowed, non-overlay, non-code-closure descendant and does not change the
package's pinned base, content or scientific/functional test identity.
Reconcile this with the handover's "new base/date/byte => new candidate"
rule. If this cannot be demonstrated, stop and re-freeze/rehearse instead.
Do not edit .claude/settings.json during Appendix J's steps 0-19 or hide
patterns using path spellings designed to evade a denial.

### F2 - ACCEPT; must be resolved before T016 (highest priority)

Verified: rulebook v0.4 section 2 rule 5 (often called rule 2.5) prohibits
Claude Code reading any source_data/, results/ or transitory_data/ directory
in the real repository OR a clone, with a narrow exception for accepted
test programs run by a task. Running the process/install tools as part of
T016 is not automatically exempt from this prohibition. Rule 9 separately
forbids Windows lifecycle tests. Rule 7 prohibits launchers.

The ratified design (6.1, L-I4 and Appendix J) requires process/lock tests
including checking a real ordinary Windows desktop with Claude Code and a
console open and demonstrating that a live Run_Experiment.bat child is
listed. It also requires install checks of weekly locks/ledgers and use of
U at source_data/.results_master.lock. Merely granting option (i)'s two
staged tools inside a clone does not authorise all of these operations.

REQUIRED BEFORE T016:
- Define "synthetic T016 clone/root" precisely: creation, allowed files,
  no access to production outcome values, and how PRE, POST, COMMITTED and
  RELEASED can still be evidenced on the correct source bytes.
- Map EVERY ratified Windows/T016 oracle to (a) authorised synthetic test
  program in the clone, (b) separately approved OWNER-MANUAL demonstration,
  or (c) a separately reviewed and owner-ratified equivalent, if any. Keep
  real-main desktop-CLEAN and live child detection explicit on the map.
- Do not interpret the owner's option (i) as authority for Claude Code to
  run Run_Experiment.bat, to perform a Windows lifecycle test, or to
  read protected production data. No process termination.
- Amend/clarify rulebook v0.5 rules 2.5 and 9 as needed, with an exact,
  audited synthetic-only exception for those operations the runner is
  actually to perform. An owner-manual operation is not a Claude Code
  permission and requires its own bounded approval. If any design
  acceptance criterion must change, refer it for formal review and owner
  decision rather than quietly weakening the evidence.
- Test the actual task command text against the settings deny list AND
  review the rulebook manually: check_task_commands.py only checks the
  Bash denials; PASS from it is not proof of rulebook compliance.

No real data must be exposed to either AI. No real owner-root process test
should be substituted silently with a scratch-clone test, or vice versa.

### F3 - ACCEPT; choose Route A as the clean default

Rulebook v0.4 is binding and is read from the runner's main repository.
A task file cannot override it. Under option (i), rulebook v0.5 must be
reviewed, owner-ratified and installed on main BEFORE T016 can execute its
narrow exception. If the first review of v0.5 occurs only in the integrated
package submission (nominally EX_163), then EX_163 cannot already include
complete authorised T016 evidence.

Preferred Route A:
1. After the approved preparatory work (items 1-2 and necessary design of
   the T016 route), draft v0.5 and its exact synthetic evidence policy.
2. Send v0.5 plus the T016 procedure/oracle mapping for focused independent
   review; owner ratifies and installs v0.5 before the final freeze or,
   at minimum, before T016. Keep the review narrowly scoped.
3. Assemble and freeze the exact final integrated candidate, ensuring the
   committed v0.5 baseline is reflected appropriately; generate final
   suites, mutations and LF/CRLF evidence on those frozen bytes.
4. Check the actual T016 task file and staging hashes against the final
   candidate, obtain the owner's separate T016 go, run the permitted
   synthetic part, and collect any required owner-manual evidence.
5. Submit the integrated package for its normal high-tier review with
   the full Windows evidence.

Route B (allowed but less efficient): an explicitly provisional integrated
review first, then the v0.5 review and T016, followed by an evidence
RECHECK before installation. Any baseline/candidate identity change
requires fresh analysis and, where applicable, rerunning final evidence.
The R-020(g) owner choice (i) is NOT reopened by this sequencing advice.

### F4 - ACCEPT; builder must test exact command route

Appendix J step 12 stages a deleted and an added results_master module.
The current Bash(*results_master*) denial matches command TEXT naming
those paths, regardless of whether they are used for copying or Git
staging. The builder needs a stage-by-manifest pathspec-file strategy,
run through cc_clone.py git in task clones, without placing forbidden
paths directly on task command lines. Git staging must include additions,
modifications AND deletions, and its output must be exactly the expected
manifest inventory. The real owner's CMD instructions and T016 must
exercise equivalent audited steps; avoid replacing real steps with
unverified task-only shortcuts.

Appendix J step 0's git pull --ff-only is an OWNER-main operation; it
cannot run in a clone with no remote and cannot be run by Claude Code.
Document a distinct clone-specific checkpoint that validates the pinned
revision and clean tree. This is a disclosed rehearsal adaptation, not a
pretence that pull was executed. Step 19 push is likewise omitted in T016.

### F5 - ACCEPT as a wording correction; NOT a new-Claude fault

My suggested-answer comparison compressed Appendix J's order ambiguously.
Correct order: COMMITTED (step 13), install check (14), remove E THEN P
(15), write release record (16), commit/RELEASED verifier (17), release
U (18), push (19). The predecessor's H-1 section 6 statement that
"COMMITTED PASS proves both commits" is also imprecise; the RELEASED
phase can check the second commit only after it exists. The replacement
Claude stated the sequence accurately. Correct both summaries at their
next appropriate edits; no second blind test.

### F6 - ACCEPT as an operational clarification

Each game's Approval 1 freezes its closure and interpreter environment;
until that game's MODE_H_SEALED, no action may change those frozen
bytes. This includes a root *.bat, any src/ file including untracked
files, venv/site-packages, or an interpreter/base-Python patch.
An install altering closure during that period refuses. Both games use
the same installation, so if EITHER game is in its freeze-to-seal
window, a shared-code/environment change is disallowed. The design 4.4
sequence is specified per game: installing MHUP-B after one game's seal
but before the other game's Approval 1 is conceptually possible; the
two different study closures must be disclosed. Do not imply that a
completed seal authorises changing code for another still-open game.
Non-closure-only documentation changes are not automatically prohibited
without considering what the study manifest actually freezes.

### F7 - ACCEPT; notify owner at final freeze

The frozen integrated candidate includes .gitignore and a base commit,
not just its src/ code. Changing any overlay path after freeze invalidates
the pertinent byte checks and requires a new candidate/evidence. Other
commits may be harmless only if they are verified non-overlay descendants,
with PRE and the package's base policy still valid. Warn the owner before
the freeze, especially about .gitignore and root files.

### F8 - ACCEPT; approval context must be explicit

E2R-T12 starts worker processes. The replacement says the owner approved
it for that chat's CLOUD-WORKSPACE suite runs on 10 November 2026, subject
to the separate normal-work go. I cannot independently verify that
owner-chat approval here. Ask the owner to confirm its context in one
sentence; do not extend it to Windows T016, reviewer reproduction or
other machines. Each needs distinct authorisation where required.

### F9 - ACCEPT; keep for MHUP-B

The R-020(g) option-(i) exception addresses T016 only. It confers no
standing authority for T017 or the first production contract child under
MHUP-B. When T017 is designed, separately reconcile the live tool denials,
rulebook limits and required rehearsal; get a separate owner decision.

## 3. Recommendations to the project owner

1. CLOSE this replacement-Claude HO-2 takeover: it passed the original
   assessment and the predecessor's genuinely independent third check.
2. If desired, authorise ONLY section 7 items 1-2: rebuild on current main,
   optional preliminary suite, and package-builder development. Other
   work remains under later, specific owner decisions. Confirm the
   E2R-T12 CLOUD-WORKSPACE scope explicitly.
3. Forward F1-F9 to the new Claude as inputs, particularly F2's exact
   oracle/permission mapping and F3's separate rulebook review route A.
4. Require a focused v0.5/T016-procedure review, then an independently
   reviewed, date-frozen integrated MHUP-A package with final evidence.
5. Keep all scientific/data gates unchanged; DO NOT install MHUP-A, execute
   T016, access holdout, update masters, or authorise real runs based on
   the HO-2 PASS.

## 4. Read-only source anchors

- Pinned GitHub commit: c48ac3c393d2eab30014e6200d427b76d90f47ac
- CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md, section 2 rules 5, 7, 9,
  sections 3-6.
- .claude/settings.json, permissions.deny; note Bash(*results_master*)
  and Bash(*.bat*).
- exchange/CLAUDE_WEB_TOOLS/check_task_commands.py, lines 1-28.
- doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r6.md,
  especially 4.1, 4.4, 6.1, Appendix J steps 0-19, and L-I4.
- doc/RATIFICATION_REGISTER_v0_26.md, future action 1 and the statement
  that settings denials are the owner's edit made with MHUP-A installation.
- exchange/CLAUDE_WEB_TOOLS/mhupa/integrated/PLAN.md.
- exchange/OWNER_REMINDERS.md R-020(g); H-1 v1r10r3 delta section 7.

This is a review and recommendation, not a ratification or execution
permission. The owner makes the final decisions. No EX number consumed.
