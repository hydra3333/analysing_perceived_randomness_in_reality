# MHUP-A integrated package: reviewer comments on Items 1-2, N1, F1-F4

Date: 2026-11-10 (Adelaide)
Project: hydra3333/analysing_perceived_randomness_in_reality
Checkpoint reviewed: b9ef1bbc70f8f0795a808570f68dad985890f912
Base reported: c48ac3c393d2eab30014e6200d427b76d90f47ac
From: ChatGPT, independent reviewer
Status: PRELIMINARY / FOCUSED COMMENTS. Not an EX message; no EX number consumed.
Authority: REVIEW ONLY. No install, T016, real-data, holdout or owner-operation authority follows from this file.

## 1. Disposition

- Items 1 and 2: checkpoint ACCEPTABLE as preliminary development progress, not an integrated-package PASS. I independently fetched the checkpoint report, builder/templates, logs, and reproduced-finding text from GitHub. The recorded preliminary suites each show 570/570, zero skips; the negative log has 11 expected STOP cases. These statements describe recorded evidence, not my own execution of those suites.
- N1: ACCEPT. Recommend the narrowly scoped .gitattributes fix, with verification and rechecks below. It is a change to the reviewed package and requires the owner's approval. I have NOT approved its application on the owner's behalf.
- F1: AGREE IN PRINCIPLE, subject to the exact reviewed controls and clean-tree/pinned-base checks below.
- F2: RECHECK before v0.5/T016. The mapping is promising, but two design-required Windows checks are not yet equivalently covered; see section 4.
- F3: AGREE Route A, with a focused prior review, owner ratification and commit of v0.5, then a separately authorised T016. The exact final task and package identity need a final recheck.
- F4: AGREE in principle; verify the actual task commands against cc_clone.py and the real settings deny rules, and explicitly test PRE after unrelated commits.
- Item 3: RECOMMEND separate owner GO, using Fable (High), strictly limited to its specified verifier/release proof/negative tests and cold read. The owner, not the reviewer, gives the GO.

## 2. N1: Git conversion of canonical install/release records

Evidence: evidence_2026_11_10/FINDING_records_crlf_reproduction.txt shows a records-validation PASS, three files reported i/lf w/crlf without attributes after Git rewrites, then VALIDATE STOP for INSTALL_MHUP_A_V1.json. Current .gitattributes protects source_data/** and results/** using -text but not the new install_records/ subtree. This is a real correctness problem for a Windows core.autocrlf=true checkout.

Recommended solution, in principle:
  src/methods/_common/contract_data/install_records/** -text

Requirements:
1. Add only the reviewed attribute for the canonical record subtree. Ensure the records are actually created as LF canonical bytes and stay byte-identical after Git add/commit, fresh clone, forced checkout and subsequent Git update with core.autocrlf=true. Compare working-tree SHA-256 to the committed blobs; git check-attr and git ls-files --eol should show no conversion for all three records. Independently validate baseline + install + release records after the rewrite.
2. Include .gitattributes as an added modified path in the manifest, stage list and PRE/POST/COMMITTED/RELEASED checks. Recompute overlay counts (previously 37 new, 33 modified, 1 deleted; normally becomes 37 new, 34 modified, 1 deleted) and related hashes. Update the build's asserted inventory, counts and all documentation accordingly.
3. Test the absence of the attribute as an expected failure, and the fixed fresh Windows-style checkout as a PASS. Recheck that adding the attribute has no unintended effect on other tracked files.
4. Any modifications after the final date/base freeze create a new candidate and require the full frozen-candidate evidence again. No release record is final until its Windows worktree validation is demonstrated.
5. Check whether any other newly added byte-canonical files outside source_data/** and results/** are vulnerable; do not broaden the fix without evidence and review.

## 3. F1: settings deny lines and their timing

- The register says the owner edits settings with MHUP-A's install; adding patterns that prohibit process_check.py or install_records.py before T016 would conflict with the chosen narrow exception. Prefer a separate OWNER commit AFTER accepted T016 and BEFORE Appendix J step 0. Do not edit settings during steps 0-19.
- Non-conflicting denials may be added earlier, subject to review. Exact pattern set is for the owner to approve; note register v0.26 expressly names process_check.py but does not expressly mandate an install_records.py denial. Proposed additions therefore need accurate provenance and scope.
- PRE must demonstrate that its base/ancestor check permits a reviewed settings-only descendant commit, but refuses altered package-path base bytes. Keep a clean tree and record both commit identities. The same reasoning applies to the earlier v0.5 rulebook commit outside package paths.
- The proposed patterns must be tested against the actual T016 commands and negative examples. check_task_commands.py checks command-text denies only; PASS does not independently establish compliance with the runner rulebook.
- The v0.5 allowance lapses once relevant deny entries are installed. A further T016 would need a new transparent owner decision; never evade denials by renaming paths or reshaping command text.

## 4. F2: T016 mapping - two outstanding design obligations

The proposed division between synthetic clone steps and owner-run lifecycle evidence is directionally sound. Empty placeholder source_data/ and results/ folders may make a data-free root structurally valid; the task must not access real data or bypass rules 2.5 and 9. The following require explicit corrections BEFORE accepting the T016 procedure:

F2-C01 (HIGH): R-020(b) requires the Windows inventory branch to run on the owner's machine AT T016, including the actual Windows interpreter executable, DLLs, DLLs/ and Lib/ and the RECORD/orphan-file checks. The proposal's 'existing synthetic tests on Windows; first real inventory at Approval 1' is NOT equivalent. Specify a real Windows inventory in a synthetic, data-safe context, with its paths, expected output, ownership and STOP handling. If the command needed would violate v0.5/permissions, propose a separately owner-run check or obtain an explicitly reviewed and ratified alternative. An unrecognised/orphan file must STOP; no hand removal and no deferral to Approval 1.

F2-C02 (HIGH): design 6.1 and Appendix L require both (a) CLEAN on the ordinary Windows desktop with Claude Code and a console at the real project root, and (b) correct refusal/listing for an actual live Run_Experiment.bat child. A synthetic-clone --root check does not, by itself, prove (a) for the real root. A bare 'python -c sleep' is weaker than (b), so may be an extra diagnostic but cannot be represented as equivalent. Split each exact oracle into runner-safe clone checks and separately owner-authorised, controlled, synthetic-process checks. Never launch a real experiment or read protected outcomes to satisfy an oracle. If exact (a)/(b) cannot be exercised safely, seek owner-reviewed alternative or mark evidence unmet; do not issue T016 PASS.

F2-C03 (documentation): provide a table for ALL T016 oracles naming operator (Claude Code or owner), exact read/write root, data-safety conditions, script/command, expected PASS and STOP, and evidence file. Distinguish the ordinary project root, the non-pushing task clone, its empty synthetic root, the actual Windows venv and the staging folder. An unpushed synthetic-data deletion commit still leaves historical Git objects in the clone; do not claim a data-free Git history, only an empty working-tree data fixture and no data read.

## 5. F3: Route A, and the smoke-test STOP that must not be mistaken for a PASS

Route A is preferred: review v0.5 and the T016 protocol in a focused round; the owner commits v0.5; freeze the final candidate; then recheck the actual T016 task against its final package identities, current deny settings and rulebook; owner gives T016 GO; integrated review receives the final Windows evidence. A code-path change after freeze triggers evidence repetition. This is not standing permission for T016.

Additional finding S1 (CORRECTION, preliminary scaffold): smoke_steps.sh at lines 43-47 deliberately calls the refusing released stub at step 17c, ignores its failure, then releases U at step 18 and prints 'SMOKE PASS'. The log confirms this behaviour. Since Appendix J requires STOP at a failed RELEASED check (with P re-created and U held, subject to the reviewed recovery), these logs must NOT be described as a successful end-to-end install or as safe STOP recovery. The script can be described as a scaffold smoke through the built phases ONLY, with the expected step 17 STOP separately observed. To demonstrate correct STOP behaviour, stop with U held and the appropriate P restoration on a simulated failed release; to demonstrate a successful step 18, finish the released verifier first and run the actual positive path. Do not treat the intentional failure as a benign continuation in any final rehearsal.

The separate 570-test suite log is useful but does not fill omitted smoke step 10 in the synthetic root. The final end-to-end LF/CRLF and T016 evidence must exercise the required suite step in an authorised compatible environment, or formally distinguish and review any partitioned equivalent.

## 6. F4 and other scope notes

- Using git add --pathspec-from-file in the owner instructions and in cc_clone.py git for the clone is reasonable, but test the exact Windows command lines and make sure the pathspec files and staged indices match the manifest. Clone step 0 cannot pull (no remote), so a clean-tree, pinned-HEAD/descendant identity check is a clearly labelled rehearsal adaptation; production step 0 remains the real pull.
- Check the 70 overlay files vs 71 changed paths wording: the 70 are 37 added plus 33 modified, with one deletion separately; N1 will increase the overlay to 71 files and total changed paths to 72. Use explicit terminology.
- R-007: the reminder describes an OPTIONAL, not-a-gate seed-record reader-name cross-check in src/evaluation/seed_policies.py, outside the reviewed 70-file overlay. Correctly disclose it; do not silently insert it into this HIGH package or mark it done. If proposed for MHUP-A, it is a separate change requiring review and renewed counts; otherwise retain it for a later relevant package.
- F5: correct Appendix J order is package COMMITTED; fresh install check; E then P removed; release record; release commit and RELEASED verification; finally U released; then push. The replacement Claude had that order right.
- F6/F7: any game's Approval-1-to-seal freeze rules out changing shared closure/environment; per-game studies can nevertheless have separate frozen closure identities if ordered as design permits. Changing an overlay path after candidate freeze invalidates the candidate's earlier evidence.
- F8/F9: E2R-T12 was approved only for the specified cloud test context; R-020(g) is only for T016 and does not authorise MHUP-B's T017.

## 7. Decision and relay

My recommended owner actions:
A. APPROVE IN PRINCIPLE N1's narrowly scoped .gitattributes fix, with the concrete checks in section 2.
B. APPROVE IN PRINCIPLE F1 timing and Route A as procedure, not permission to edit settings, commit v0.5 or run T016 today.
C. REQUIRE RECHECK of F2's Windows inventory and exact live-process evidence mapping; reject any proposal to defer the first real Windows inventory to Approval 1 without a new owner-ratified change.
D. AUTHORISE item 3 separately, if the owner wishes, using Fable (High) for the RELEASED phase, two-commit/barrier proofs, verifier negatives and independent cold read only. A focused review remains necessary before T016.

No additional code work, installation, running of T016, creation of records on real data, holdout access or reviewer-execution privilege is authorised by this review. The new Claude should report a narrow resolution of F2-C01 and F2-C02 before asking for rulebook v0.5/T016 approval. If no new numbered EX file has been committed, preserve EX_163 as merely the next possible number.
