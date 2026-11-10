# MHUP-A - owner decisions after Items 1-2 focused review (10 November 2026)

Project: hydra3333/analysing_perceived_randomness_in_reality
From: Project owner, relayed by ChatGPT independent reviewer
For: Replacement Claude primary designer/coder
Applies to: b9ef1bbc70f8f0795a808570f68dad985890f912 (draft checkpoint); main development base c48ac3c393d2eab30014e6200d427b76d90f47ac
Related review: MHUPA_Items1_2_ChatGPT_Focused_Review_2026_11_10.md
Status: OWNER DECISIONS AND BOUNDED GO; not an EX message. No EX number used.

## 1. Owner decisions (explicit)

D01 - Item 3: AUTHORISED. The owner accepts the reviewer's recommendation to proceed with H-1 v1r10r3 section 7 item 3 using Fable (High). Scope: build the verifier's released phase, two-commit and barrier-order proofs, associated negative tests, and an independent cold read of installation instructions against ratified Appendix J. Report any STOP. Do not proceed automatically into items 5-8.

D02 - N1: APPROVED IN PRINCIPLE for development and focused review. Add the narrowly scoped Git attribute line to the next MHUP-A package candidate:

    src/methods/_common/contract_data/install_records/** -text

This is authority to implement and test the change in the draft package, NOT authority to install or release it. The reviewer requires an updated file inventory, hashes, verifiers, staged paths and negative/positive oracles. Prove that all three canonical records retain byte identity after Git add/commit, fresh checkout and a Git rewrite with core.autocrlf=true; include git check-attr, git ls-files --eol and actual validator results. Evaluate other unprotected byte-canonical files, but propose any wider change separately. The current expected changed set becomes 37 added, 34 modified and 1 deleted, subject to independent recount; 71 overlay payload files plus one deletion (72 changed paths), with the install record itself a separately created/staged record.

D03 - F1: APPROVED IN PRINCIPLE, not for execution now. The conflicting Claude Code Bash deny rules may be added as a separate owner-made, reviewed .claude/settings.json commit AFTER the final accepted T016 rehearsal and BEFORE live-install Appendix J step 0. Do not install them early, evade them, or edit the settings yourself. Review the exact rules, including whether install_records.py needs its own additional deny line. Prove PRE still passes on a clean descendant with only non-package changes (rulebook/settings commits), and STOPs on changes to package-path base bytes. The owner makes and authorises any settings edit separately.

D04 - F3 / Route A: ACCEPTED as the planned review sequence. First produce a focused reviewed and owner-ratified rulebook v0.5 and complete T016 protocol/task; only after rulebook v0.5 is separately installed may T016 be run with its own owner GO. Obtain final task/package-identity review against the frozen candidate and current deny settings. The final integrated MHUP-A review will include the accepted Windows evidence. This is not advance permission for the rulebook install or T016.

D05 - F2: NOT APPROVED AS PREVIOUSLY SUBMITTED. The owner accepts the reviewer's requirement for F2-C01 through F2-C03 corrections and a focused RECHECK before the v0.5/T016 decision:
  * At T016, exercise the actual Windows interpreter/DLL/Lib and venv RECORD inventory branch (R-020(b)), including orphan-file refusal; synthetic unit tests alone or postponement until Approval 1 do not satisfy it.
  * Preserve both design 6.1 / Appendix L process oracles: CLEAN on the ordinary Windows desktop with Claude Code and a console at the real project root; correct detection/refusal for a live Run_Experiment.bat child. A bare sleeping Python process is not a substitute, and no live real-data experiment is authorised merely for this oracle. Propose explicitly owner-run, synthetic-safe checks if required, or report an unmet oracle and seek reviewed alternatives.
  * Provide a complete T016 oracle matrix: operator, command, real/synthetic root, data safety, expected PASS/STOP, evidence and separate authorisation. Respect current rulebook rules 2.5 and 9; the narrow R-020(g) option (i) exemption alone does not relax them.

D06 - F4: ACCEPTED IN PRINCIPLE. Continue with manifest-controlled pathspec staging, tested against actual Windows cc_clone.py and Bash-deny matching. In task clones, replace the impossible step-0 git pull with an expressly identified, read-only clean-tree/HEAD identity check. The owner's live install retains the real step 0. No permission to bypass deny rules.

D07 - S1 (new smoke-test finding): REQUIRE CORRECTION. The draft smoke script currently observes the deliberately refusing released stub, continues to release U, and prints SMOKE PASS. This is only a preliminary scaffold experiment, not evidence of an end-to-end safe install. After item 3, verify a true positive path and test a refused RELEASED phase that STOPs with appropriate barriers retained/re-established and U held, under the ratified Appendix J recovery procedure. Do not present continuation after STOP as an acceptable rehearsal.

D08 - F5-F9: Carry forward the review's clarifications without expanding authority. Correct barrier order (COMMITTED; install check; remove E then P; publish release record; release commit and RELEASED; release U; push). Respect per-game Approval-1-to-seal frozen closure/environment, overlay freeze, the narrow E2R-T12 cloud-suite authorisation, and the separate future decision for T017. Do not silently add R-007's optional source change to this package.

## 2. Immediate work and stopping boundary

Claude may now perform Item 3 (D01), including the N1 draft fix and its focused tests (D02), and prepare written refinements for F1-F4, S1 and T016 (D03-D08). This does NOT give authority to run T016, install rulebook v0.5, edit live .claude/settings.json, install MHUP-A, run any real-data operation, open the holdout, change dependencies, or proceed automatically to final freeze or final integrated review. These later activities retain their separate reviews and owner approvals.

Deliver a concise item-3 checkpoint: identities of the draft files, tests and negatives actually run; N1 before/after Windows-style Git conversion evidence; a repaired STOP-aware smoke flow; and an F2 oracle matrix for focused review. Label preliminary evidence as preliminary. If an instruction or test conflicts with the current ratified design or runner rulebook, STOP and ask rather than improvise.

## 3. Exchange protocol

This handback is not a numbered EX message. Check exchange/ for the highest actual EX identifier before the next numbered exchange. Nothing in this note reserves EX_163.
