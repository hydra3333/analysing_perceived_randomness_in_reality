# HO-2 closure and limited owner GO for the replacement Claude - 10 November 2026

Project: hydra3333/analysing_perceived_randomness_in_reality
For: replacement Claude chat, primary designer and coder
From: project owner, following independent ChatGPT review and predecessor Claude's third cross-check
Status: OWNER DECISION / DEVELOPMENT SCOPE. Not an EX message; no EX number consumed.
Reference checkpoint for the takeover checks: main c48ac3c393d2eab30014e6200d427b76d90f47ac.

## 1. Owner decisions now made

1. HO-2 replacement-Claude takeover: ACCEPTED and CLOSED. All nine blind takeover answers passed the ChatGPT reviewer; the predecessor Claude's independent v0.2 cross-check found no takeover BLOCKER. There is no need for more blind questions. You may now see the review findings.
2. H-1 v1r10r3 section 7 ITEM 1: AUTHORISED. Rebuild the temporary BASE and DEV trees from the *then-current* GitHub main. Compare with the reviewed MHUP-A slice 2 overlay, check intervening changes outside exchange/ (especially root files and .gitignore), and document any deviations. An optional preliminary offline/synthetic full-suite run in the cloud workspace is authorised; label it PRELIMINARY, not final acceptance evidence.
3. H-1 v1r10r3 section 7 ITEM 2: AUTHORISED. Develop the integrated MHUP-A package builder, manifest, repo_overlay, manifest-controlled copy helper, verifier scaffolding/appropriate existing phases, suite runner and draft Appendix J installation instructions. The builder must recompute the exact gate-file import closure and assert that its manifest's ten gate files equal the computed closure: eight changed and two new. Keep an explicit boundary between item 2 and the separate item 3 work on the `released` verifier phase, two-commit/barrier-order proofs and cold read; item 3 is NOT yet authorised. Do not falsely label a partial verifier as final or installation-ready.
4. E2R-T12: the owner expressly approves the self-terminating worker-process test when invoked by the replacement Claude's offline suite in this cloud-workspace development context, after this GO. The approval is not transferable to Windows T016, reviewer-run reproduction, another environment, a real run, or any other new run context.
5. The owner accepts the reviewer-recommended next sequence in principle, favouring ROUTE A for the rulebook/T016 dependency: a separate focused review and owner installation of rulebook v0.5 and T016 task/instructions BEFORE T016 runs, followed by T016 under its own specific go and an integrated package review with the Windows evidence. This is not permission to run T016, commit/install rulebook v0.5 now, edit settings, or begin item 3.

Proceed with items 1 and 2 and report their completion, evidence and any STOP. If an activity crosses the item 2 boundary, ask for its separate approval. The owner controls the live repository, installs, real runs and releases; the normal named-path restrictions remain in force.

## 2. Results of the predecessor-Claude third cross-check

The predecessor's `HO2_Predecessor_Claude_Third_Crosscheck_v0_2.md` (10 November) and the independent ChatGPT review `HO2_Predecessor_Third_Crosscheck_ChatGPT_Review_v0_1.md` concluded that the takeover passes, but identified F1-F9 for future package work. These are a REQUIRED DESIGN/REVIEW INPUT to items 2, 5 and 6, not already-resolved implementation facts. Preserve the findings and record each proposed resolution explicitly.

F1 - Settings-deny timing. Register v0.26 says the owner's `.claude/settings.json` additions are made with the MHUP-A install; the two T016 tools (`process_check.py`, and if separately approved `install_records.py`) must not be denied during authorised T016. Proposed sequence: complete T016 first; the owner then makes a separate, reviewed settings edit/commit before Appendix J step 0, rather than inside steps 0-19. Test the actual task commands with `check_task_commands.py` and negative examples. Timing, not a disguised command or filename, protects the exception. IMPORTANT additional reviewer qualification: a settings commit advances main; the final package's base identity, ancestry, PRE clean-tree and exact-byte checks must still pass. If the freeze or candidate evidence is invalidated, STOP and resolve it openly, possibly by re-freezing and repeating final evidence. Do not silently change the frozen base.

F2 - T016 rulebook/data/lifecycle conflict (HIGH PRIORITY). R-020(g) option (i) permits only the two named tools under tightly constrained T016 synthetic-clone conditions; it does not override rulebook v0.4 rule 2.5 (no reading anything under source_data/, results/, transitory_data/, in any clone) or rule 9 (no Windows lifecycle tests). However Appendix J's tools touch U at `source_data/.results_master.lock` and inspect `results/real/weekly/` session/attempt/forecast records. The ratified design section 6.1 and Appendix L additionally call for Windows evidence that the process check gives CLEAN on the ordinary desktop with Claude Code and a console open at the root, and detects a live `Run_Experiment.bat` child. Rule 7/command denials prohibit launching that child via Claude Code. Before T016, define and review exactly which checks run on an isolated synthetic root that contains NO real outcome data, which owner-operated checks occur outside Claude Code under separate approval, and whether any alternative is genuinely equivalent. Do not treat the option (i) decision as an override of rules 2.5 or 9, and do not silently omit any design-required oracle. The owner has not authorised live lifecycle experiments or data access.

F3 - Rulebook review/install sequencing (HIGH PRIORITY). Claude Code reads the actual installed rulebook on main, not the proposed file inside an uninstalled package. Therefore T016 cannot use the new exception until v0.5 is independently reviewed, owner-ratified and committed in the live repository. The owner favours Route A: prepare a focused v0.5/T016 task review, get separate owner approval to install v0.5, then separately authorise T016, then put T016 evidence in the integrated-package review. Route B (provisional integrated review, then T016 and evidence RECHECK) is the documented alternative only if Route A proves unsuitable and the owner agrees. Committing v0.5 is a distinct preparatory change, not T016 itself; re-check package/base consequences.

F4 - Real instruction versus task-clone Git commands. Appendix J step 12 must stage added/deleted `*results_master*` paths, which a task command naming those paths would hit settings `Bash(*results_master*)` denial. Design a manifest/pathspec-file staging route through `cc_clone.py git`, so the T016 task can reproduce the owner's actual staging semantics without a denied filename on the command line. Appendix J step 0 requires `git pull --ff-only`, but a T016 clone deliberately has no remote; specify an explicit read-only checkpoint/identity substitution for the clone, while the owner's live install retains the real step 0. Never bypass a denial or insert an undeclared Git remote.

F5 - Barrier/release order (wording correction only). Appendix J exact order: step 13 COMMITTED for the package commit; step 14 install check; step 15 delete E THEN P; step 16 write release record (refuses while P exists); step 17 release commit and `released` phase; step 18 release U; step 19 push. On a STOP in 16 or 17, P is restored as prescribed. Replacement Claude's Q7 stated this correctly. The ChatGPT comparison used a potentially misleading abbreviated ordering, and the predecessor's H-1 section 6 called the two-commit proof `COMMITTED` too broadly. Correct explanatory wording; follow Appendix J, not the shorthand.

F6 - Frozen period is per game and begins at Approval 1, not at Approval 2. MHUP-B installation is either before that game's Approval 1 or after that game's MODE_H_SEALED; during that interval, any change to frozen code-closure or environment bytes (including new root BAT, untracked src files, dependencies, venv and base-Python updates) can make Mode H refuse. If one game's seal occurs before the other game's Approval 1, an install in that gap is only possible under all governing rules; the studies then freeze different closures and should disclose that. Treat as owner operational reminder.

F7 - Once the candidate's base/date/overlay bytes are frozen, changing a touched path (especially .gitignore) may require re-freeze and complete repeat evidence. OUTLANDISH changes outside the closure/overlay still require the relevant PRE/base checks. Tell the owner at freeze time.

F8 - E2R-T12 approval is scoped to the new chat's cloud-workspace suites only, expressly confirmed above. Windows, independent reviewer reproduction and other run contexts are outside it.

F9 - R-020(g) is only a T016 allowance. MHUP-B's T017 will have different requirements and needs a new owner decision; no standing permission carries forward.

## 3. Hard boundaries / what is NOT authorised by this GO

- No MHUP-A installation, no owner-machine T016, no real-data/holdout/master updates, no production or weekly runs, no approval 1-4, no code-changing live installation, no dependency change, no termination of project processes, no orphan-marker clearance.
- No unilateral rulebook v0.5 installation and no edit to the owner's `.claude/settings.json`. Those require their own later review and owner decision.
- Item 3 (`released` verifier phase and two-commit/barrier-order proof, fresh-helper cold read) and later evidence/rehearsal work remain separate. You may design the interfaces in item 2 without performing item 3 prematurely.
- A STOP is a STOP. Do not work around deny patterns, unsafe-data boundaries, unknown process identity, or inconsistent hashes. Preserve logs and report the cause; an owner-authorised recovery follows the governing rules.
- No real results values in chats or public exchange files. Work from synthetic fixtures only. Keep outcome-free provenance and scientific N-1 protections intact.
- Do not assume an EX number: check the current highest exchange/ number when an actual reviewer exchange is ready. At this point EX_162 was highest; no EX number used for the HO-2 review.

## 4. Required next report from the replacement Claude

When items 1 and 2 have been completed or a STOP occurs, report to the owner:

- the verified current-main base commit and what changed since c48ac3c;
- rebuilt tree/overlay identity, ten-gate derivation, .gitignore and root-file treatment;
- which builder artifacts exist and their precise hashes or diff identities; which elements are scaffolding versus complete;
- all preliminary suite runs and their full PASS/FAIL/SKIP counts and exact environments (not final evidence);
- a concrete approach to F1-F4, with F2's synthetic/owner test mapping and F3's Route A prerequisites; any issue requiring a fresh owner decision;
- the next proposed, separately reviewed package and the exact authorisation needed before item 3 or rulebook v0.5 work.

Continue as primary designer/coder under the ratified H-1/H-2 roles. The independent reviewer reviews substantial proposed code and its evidence; the owner decides all authorisations.
