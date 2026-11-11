# MHUP-A Rulebook v0.5 / TASK_T016 r2 - ChatGPT focused RECHECK

Date: 2026-11-11 (Australia/Adelaide)
Repository: hydra3333/analysing_perceived_randomness_in_reality
Reviewed commit: 19e45ff12db2234ecfe4da105c531f1904739f0f
Prior candidate: 5e1a70460d75af98322d21aaf978937ec710ca6f
Scope: exchange/CLAUDE_WEB_TOOLS/mhupa/t016/ (rulebook, T016 task, owner rows 8-9, Appendix J amendments, r2 dry-run evidence); compared with active rulebook v0.4 and prior focused review.
Status: R-2 FOCUSED PASS - no blocking correction. Two minor wording adjustments may be incorporated during finalisation without another design review. This is not an EX message or an authorisation to install or run.

## 1. Findings disposition

- T016-C01 PASS. OWNER_ROWS_8_9_DRAFT.md now accurately distinguishes reading weekly ticket/forecast-ledger metadata if present from fetching or printing drawn outcome values, and advises the owner to inspect full process command lines for private strings before forwarding outputs.
- T016-C02 PASS. New rulebook section 2A A6 and the T016 task require recording each command, exit code and full output as it finishes, ahead of the existing guarded cleanup-before-report sequence. Unexpected failures do not licence clone inspection, repair or recovery.
- T016-C03 PASS. A4 identifies the real repository as prohibited as a tool target while explicitly allowing its venv python.exe as the interpreter. The staged package copies, not the real installed process_check.py/install_records.py, are invoked against the task clone.
- T016-C04 PASS. A5 now requires nonzero exit, an output line beginning with the specified refusal text, and no Traceback. Task steps 10, 19, 27 name later positive checks of the relevant barriers/record state. The new r2 Linux dry run shows each expected refusal with exit 1 and the anchored message, plus continuing positive checks. This validates the Linux rehearsal, not Windows execution.
- T016-C05 PASS. The task header requires pinned ZIP path/SHA-256, final counts, task commit named in the owner's GO, and rerunning check_task_commands.py against the then-current settings. F1 deny patterns remain deferred until after T016. The current draft checker is reported PASS on 47 command lines.
- J-REVIEW PASS. J-1/J-2 clearly replace the step-10 normal-path premise with the N5 shadow-suite mechanism; J-3/J-4 are exceptional STOP recovery only, separately reviewed and owner-approved per actual state. They preserve a fresh CLEAN before any Git/code change, barrier retention, no reset/history rewrite, and reviewed revert/abandon-and-rebuild. Section 4.3's 40-per-game and post_pass_utc wording corrections preserve the schema.

The narrow permission, isolation of the task clone, the development-only six-file shadow data copy, no-launcher/no-push restrictions, read-only real-vENV inventory and planted orphan in scratch remain intact. Prior full Linux rehearsal with step 10 included demonstrated 571/571 on draft code; the new r2 evidence omits step 10 because the suite and package were unchanged and concentrates on the three stricter expected-refusal oracles. This evidence is sufficient for the present design RECHECK, not for a Windows PASS or real installation.

## 2. Two nonblocking wording cleanups

W01: Rulebook v0.5 section 2A A4 ends with 'T016 launches nothing.' That is literally false: RUN_MHUP_A_SUITE.py starts unittest subprocesses, including the accepted E2R-T12 ordinary Python workers. Replace with something like: 'T016 launches no project launcher, coordinator, real-data run or lifecycle test; the accepted suite may start its pre-authorised ordinary Python test workers.' Keep the same restrictions and approved test scope. This is a clarity correction, not a permission expansion.

W02: TASK_T016_DRAFT.md Purpose says 'five byte-checked items' while step 37 correctly lists SIX files with i/lf w/lf attr/-text (three install/release records plus process_check.py, results_master_v0_2.py and the v0.1 reference fixture). Replace 'five' with 'six'. No test or manifest change is needed.

Optional precision: task step 10 says later steps prove the updater lock is 'unchanged'. They establish that a correct U remains held, not necessarily byte-for-byte identity of its timestamp. Prefer 'U remains valid and held by this package'. Do not add a new test just to support that stronger but unnecessary claim.

These minor edits can be made in final candidate preparation with a normal consistency check. They do not warrant an extra independent RECHECK unless code, permissions or safety behaviour changes.

## 3. Reviewer recommendation and boundaries

Recommend owner ratification of the narrow v0.5 rulebook and Appendix J J-1/J-2, J-3/J-4 and section 4.3 clarifications after the two wording cleanups, followed by freezing the package and preparing the final pinned TASK_T016, with the usual final manifest, byte hash and command-check evidence. This recommendation does not itself ratify, install or authorise anything. Rulebook v0.4 remains live; there is no GO for T016, owner-run F2 rows 8-9, .claude/settings.json edits or live MHUP-A installation. F1 deny patterns are installed only after T016 (and before live installation), as already planned. Preserve the owner's priority: scientific correctness and functional safety without adding unnecessary permanent production administration.

Evidence limitation: read-only inspection of the GitHub-committed draft and reported test logs, not independent Windows execution and not a verification of the owner's local venv.
