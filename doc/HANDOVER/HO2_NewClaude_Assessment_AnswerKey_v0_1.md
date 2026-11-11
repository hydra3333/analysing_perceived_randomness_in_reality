# HO-2 - reviewer takeover assessment and suggested answer key (10 November 2026)

Project: hydra3333/analysing_perceived_randomness_in_reality
Claude's reported read-only checkpoint: c48ac3c393d2eab30014e6200d427b76d90f47ac
Disposition: FIRST-REPLY PROVISIONAL PASS; BLIND QUESTIONS Q1-Q9 PENDING.
Status: assessment for owner only. DO NOT forward to Claude until it has answered the separate blind question file. NOT an EX message; no run/install authorisation.

## 1. Initial assessment

The replacement Claude's first reply is a credible, well-structured handover. It respects the mandated read-only/no-build/no-test/no-commit/no-push interval and identifies the owner's authority, the reviewer role, the code-review and installation boundaries, the method/science state, safe holdout isolation, the E2R-T12 process exception, and the incomplete MHUP-A integration. It acknowledges uncertainty in the dated blurb placeholders and reports concrete hash checks instead of inventing outcomes. This is a satisfactory first-reply checkpoint, not yet HO-2 completion: independently answered questions and the owner's explicit GO are still required.

Source checks performed by this reviewer against GitHub at the specified ref:
- The repository's `exchange/OWNER_REMINDERS.md`, R-020(g), expressly records the owner's option (i) decision at about 18:30 Adelaide on 10 November 2026, narrowly authorising the *design choice* for rulebook v0.5 while retaining separate review and T016 GO. The new Claude was correct to say the decision was DONE.
- `exchange/CLAUDE_WEB_TOOLS/mhupa/integrated/PLAN.md` records the 8 November preliminary 569/570 runs on Python 3.13 and 3.15, the corrected focused 8-test rerun, the pending frozen 570-test suite and both mutation chains, the ten-file gate closure, and a checkpoint naming `build_mhupa_pkg.py` as the next unfinished task.
- H-1 v1r10r3 delta section 7 and the installed introductory blurb establish HO-2's no-work-before-authorisation rule, C01-EFF, rulebook/T016 bounds, model split, and final evidence order.
- Ratified amendment A1 defines one create-only *whole ledger*, followed by validation, `SCORE_COMPLETE`, reports and `MODE_H_SEALED`, with explicit crash oracles; its text is now incorporated into design v0.1r6.
- Register v0.26's future-actions section explicitly assigns the MHUP-A installation/review record to **register v0.27**. Claude correctly noticed the stale v0.26 pointer in the supplementary handover and declined to treat it as authoritative.
- The source's H-2 role description preserves independent reviewer rights and states that Claude Code is an owner-authorised local runner only.

Some of Claude's SHA-256 and current-tree checks were reported by Claude/the predecessor rather than recomputed independently here; the owner supplies that the previous Claude checked them. This assessment does not pretend to reproduce every one of its 84-hash verification checks, run reports or directory diff.

## 2. Focus points and nonblocking observations

A. **Immediate checkpoint, not an additional mandatory preliminary test round.** The plan's checkpoint already reached the builder (`integrated/build_mhupa_pkg.py`). A quick fresh-base rebuild/diff at c48ac3c makes sense because owner commits moved `main`, but a full preliminary suite is optional, and is not final evidence. Claude should understand the distinction and avoid expensive redundant work without a reason. Section 7 item 1 remains available; the immediate *unfinished* item is 2.

B. **A1 order and crash recovery.** The first reply did not restate the ratified ordering, and prior handover reviews found it easy to reverse. Verify without giving the answer away first.

C. **Freeze identities.** It read C01-EFF but did not explain the consequences for E_1 r3's date and fixed test, or for `pyahocorasick` and the relocated `GAIS/`. Probe before authorising package work.

D. **Owner R-020(g) decision versus T016 permission.** No contradiction: option (i) is decided; rulebook v0.5 and the owner's denial-line edits still need preparation/review, and T016 requires an explicit, separate GO. The existing v0.4 prohibition still governs until the relevant approved change is operative. No settings bypass may be introduced to obtain a superficial PASS.

E. **Provenance/record pointers.** The candidate correctly distinguishes the installed register v0.26 from planned v0.27 and notes a handful of stale editorial pointers. These are not a takeover blocker and need not cause another document-review round unless they would change operational instructions.

F. **Model guidance and push capability.** Claude transparently reported the session's Fable 5.2 indication despite the requested Opus start. The owner determines the selected model and access. A switch before normal Opus work is sensible; push permission is not a reason to grant broad repository write authority. Claude's scope must remain limited to owner-authorised paths and workflows.

G. **T022 chronology.** Windows T022 was run before relocation of `src/GAIS` to top-level `GAIS`; it is valid evidence for the reviewed slice 2 v1r2 candidate but not a substitute for T016 and final tests on the newer integrated, date-frozen tree.

## 3. Suggested answer key - PRIVATE until Claude has answered

**Q1 - Current state.** Installed: PERF-1 baseline, 40 released method variants in both games, walk-forward execution/scoring/rank reports on development data. Development reports do not establish any predictive departure from fair draws; exploratory and calibrated claims remain separate. MHUP-1 design v0.1r6 ratified with A1. MHUP-A two code slices reviewed and accepted (EX_146, EX_152), but no integrated package accepted or installed; MHUP-B future. T022 570 tests with up to 4 permitted symlink skips on Windows (reviewed slice 2), while the 8 Nov integrated rebuild was preliminary 569/570 on two Linux Pythons; a focused fix/recheck 8/8 was not a full final suite. Final date-frozen suite, mutation chains, rehearsals and reviewer PASS remain outstanding.

**Q2 - A1 publication order.** `SCORING_STARTED` fixes attempt/roster. Scorer obtains one freeze-authorised outcome read for all target draws, computes all score and MR5 rank-position records, publishes the complete `mode_h_score_ledger.jsonl` once via create-only temp/sync/link. Before `SCORE_COMPLETE`, validate the published ledger byte-for-byte and all identity/roster/number consistency (including Oz Lotto checks). Then `SCORE_COMPLETE` with ledger digest, report's three create-only files/recovery, and finally `MODE_H_SEALED`. No outcome re-read after the ledger is published; once `SCORE_COMPLETE`, outcome reader refuses holdout target access. Invalid ledger = STOP, never relax validation or rewrite accepted lines.

**Q3 - A1 recovery.** Before link, no ledger accepted; repeat same attempt and frozen-roster check, outcome re-read allowed, ignore leftover temp file. After link but before `SCORE_COMPLETE`, do NOT reread outcomes: revalidate existing complete ledger using numbers recorded in it and write the marker or STOP. After `SCORE_COMPLETE`, no reread; resume report creation and sealing only. One fixed scoring attempt per game and one create-only ledger; no partial per-pair ledger/skip logic. Post-seal corrective scoring deferred to separately reviewed MHUP-B route with policy ID and `amendment_of`, never rewriting original seal or ledger.

**Q4 - C01-EFF.** `effective_date` for E_1 r3 means *integrated package preparation date*, frozen prior to the review and not later substituted with installation or release date. It appears in two E_1 registry entry files and the archived r2 README; the targeted test's expected date is a counted edit. Freeze new date/bytes, recompute SHA identities and entire final evidence, not just a focused test, if it changes or if the package changes. New HEAD requires proof the reviewed baseline and owner files are preserved.

**Q5 - DEP/GAIS.** DEP-1: `pyahocorasick` approved, installed in the owner's venv, so environment freeze must capture it at Approval 1, including installed package files and RECORD list; unrecorded/orphan site-packages content refuses, investigated under reviewed remediation, never hand-delete. GAIS-1: moved `src/GAIS/` to top-level `GAIS/`, outside covered `src/` closure, while the ignore rules keep large binaries and y-cruncher artifacts out of Git; do not exclude other protected code. Rebuild against current main, preserve owner's `.gitignore`, `.bat`/README/root changes, perform precise overlay-diff and closure checks, no source folder access.

**Q6 - R-020(g).** Owner chose restricted option (i) 10 Nov; that is not blanket permission to run T016. Rulebook v0.5 may allow only `process_check.py` and `install_records.py` in prescribed T016 synthetic disposable task clone, from package staging, under explicit task file. `check_task_commands.py` must pass, `.claude/settings.json` denials cannot be bypassed, no push, no main modifications, no real data. Approval for rulebook/setting changes, their review and separate T016 GO remain. If impossible without violating denials, STOP and take alternative back to owner, rather than override.

**Q7 - Install/release.** Builder computes changed import closure for `contract_dispatch.py` and asserts exactly ten step-6 gate files (eight modified and two new under `src/methods/_common/`); do not trust a copied literal alone. Install then release separate commits, exact-only file list and parent check, `INSTALL_MHUP_A_V1.json` and `RELEASE_MHUP_A_V1.json`, proof no extra files/paths and correct manifest/record digests, lock/barrier E/P state. Release record must name E_1 revision 3 for POWERBALL and OZLOTTO. Before valid release, E_1 r3 remains installed/unreleased and refuses official CATCH_UP; revision 2 is superseded appropriately. No real-run authority implied.

**Q8 - Meaning of Mode H/other decisions.** Owner chose option A: freeze study plan/code before opening holdout, admit first results update, then forecast each holdout target from prior draws only and score after every forecast is frozen; this is honest retrospective precommitted evaluation, *not* advance prediction before already-public draw outcomes. Q7 display rule remains open until before Approval 2. MHUP-B timing must be decided: install before Approval 1 or after the affected game's Mode H seal, never during the unsealed interval. Backups, Windows POC rerun versus documented waiver, Approvals 1-4, actual updater/Mode H/real-data operations all owner-gated separately. Any corrective scoring MHUP-B only.

**Q9 - Next work and STOP.** Now builder is the checkpoint's unfinished work; refresh/rebuild current HEAD as needed with exact overlay comparison, possibly a preliminary suite but do not count it as final evidence. Opus for builder; Fable recommended for HIGH released-phase/two-commit/barrier proofs. Owner R-020(g) choice already made, then review and stage rulebook v0.5/settings lines, choose/freeze C01-EFF date, make final candidate, full suite both Pythons, both mutation chains, LF and CRLF rehearsals, then T016 under distinct owner authorisation (or reviewer provisional until T016), finally EX review at next free number, PASS + owner install and release, verification and v0.27. Before normal work obtain owner go after HO-2; E2R-T12 has process-spawning impact and needs owner approval for **this** run context even if allowed elsewhere. No unauthorized model switching, dependencies, holdout, processes, data reads, real outcomes or termination. At STOP, stop and report with scoped recovery request; no self-authorised retry, unsafe kill, deletion or bypass.

## 4. Decision procedure on returned answers

- Assess Q1-Q9 independently before disclosing this key. Mark each PASS, CORRECTION or UNRESOLVED and quote any critical misconception.
- Key hard blockers: incorrect A1 publication/crash order, release admitted on install alone, treating R-020(g) as T016 GO, wrong `effective_date` semantics, mis-scoping GAIS/environment freeze, self-authorising holdout access or STOP recovery.
- Minor wording gaps and stale pointers can be corrected directly without re-running takeover if all safety/functional gates are understood.
- Owner decides whether HO-2 is complete and whether to authorise the next normal work. The reviewer should not issue an EX for this handover probe unless owner requests one or findings justify a formal exchange.

## 5. Source basis and limitations

Primary repository checkpoint at c48ac3c393d2eab30014e6200d427b76d90f47ac: `doc/HANDOVER/Claude_Primary_Handover_H1_v1r8.md`, `doc/HANDOVER/Claude_Primary_Handover_H1_v1r10r3_delta.md`, its introductory blurb; `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r9.md` plus v1r10 delta; `doc/RATIFICATION_REGISTER_v0_26.md`; `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r6.md`; `exchange/MHUP1_design_amendment_A1_RATIFIED.md`; `exchange/OWNER_REMINDERS.md`; `exchange/CLAUDE_WEB_TOOLS/mhupa/integrated/PLAN.md`. Read from GitHub connector. Facts about exact tests/hashes rely on the tool-verified records and predecessor's verification reports, not a fresh scientific run by this reviewer.
