# Predictive Randomness - ChatGPT Independent Reviewer Handover H-2 v1r9 (CANDIDATE, written by Claude)

**Repository target:** `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r9.md` (staged in `exchange/HANDOVER_2026_11_06/` until the
owner installs it).

**Status:** **CANDIDATE - NOT OWNER-RATIFIED, NOT REVIEWER-WRITTEN.** H-2 v1r8 remains the operative reviewer handover until the
owner ratifies this edition. The new reviewer's takeover check comes first, and is a normal review of this text.

**Prepared:** 6 November 2026 (Australia/Adelaide).

**Author:** **Claude (the primary designer and coder), on the project owner's instruction of 6 November 2026.** The ChatGPT
reviewer chat that held this role from 30 October 2026 reviewed:
- the MHUP-1 design rounds;
- DOC-11;
- the HO-2 takeover;
- both MHUP-A code slices (EX_142 to EX_152).

It reached its conversation limit on 6 November 2026 **without writing its own handover**. This edition is Claude's best
reconstruction of what that reviewer knew, taken only from the committed records: its own messages EX_142, EX_144, EX_146,
EX_148 (with its evidence supplement), EX_150 and EX_152, together with the register, the roadmap and the reminders. Claude is the
author of the work under review, so **treat every checkpoint fact here as author-reported until you verify it against the
repository**. Report any factual error, omission or wording that would narrow your independence as a normal finding; the owner
decides.

**Predecessor:** H-2 v1r8 (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8.md`, installed with DOC-10). Its Git (LF) blob SHA-256
at main 43dd069 is `4e2737c28a69ab73577fa6c39c87c04518e42ed1be47f240295e80802774b956`.

**Rights preservation:**
- The complete `## 2.` through immediately before `## 4.` region is still **7,676 bytes, byte-for-byte identical** to H-2
  v1r8, v1r7, v1r6, v1r5 and v1r4, with SHA-256 `70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db`. Claude
  recomputed both figures from the v1r8 blob on 6 November 2026, and the builder asserts them.
- Sections 1, 4 and 5 are also carried byte-for-byte from v1r8.
- **No reviewer-rights change is proposed.**
- **Clarification (H2-TAKEOVER-O01, outside the protected region, unchanged in substance):** R-8 to R-11, and the safeguards in
  section 3 that the protected text still calls "proposed", have been OWNER-RATIFIED since 27 October 2026. They bind as fully
  as R-1 to R-7.

**Encoding:** UTF-8, because the protected region uses UTF-8 typography; everything outside it is ASCII. LF line endings, so the
recorded hashes can be checked directly.

**Reading rule:** this is an operational handover, not a second ratification register. For history, installation identities,
decisions, evidence and SHA-256s, read the **latest owner-installed** `doc/RATIFICATION_REGISTER_v*.md` (v0.24), installed
source, `review/` records and the EX messages. An EX message or an owner working list is not a ratification.

## 0. Authority and checkpoint (6 November 2026)

### 0.1 Roles

- **Roles:** Claude is the primary designer and coder; ChatGPT (you) is the independent other-model reviewer; the owner alone
  ratifies and controls installation, scientific release and gated tests. Claude Code is an owner-authorised local task runner,
  not a designer, coder or reviewer.
- **The Claude chat:** the Claude chat in role since the staged handover HO-2 (completed 4 November 2026) continues. If it is
  replaced, its successor starts from H-1 v1r8 plus the delta `exchange/HANDOVER_2026_11_06/Claude_Primary_Handover_H1_v1r9_delta.md`,
  and you check its first reply, as your predecessor did in HO-2.

### 0.2 Installed state (unchanged in code since PERF-1)

- **Code:** the last installed code package is still PERF-1 at `3fce327`.
  - All 40 variants are `SUPPORTED` and released in both games.
  - The suite installed on main is 471 tests.
  - Three execution switches stay `False`; `ENABLE_CONTRACT_REAL_DEVELOPMENT` is `True` (WF-1A) for owner-authorised
    development runs only.
  - The allowlist is empty.
  - No master update, Mode H, FINAL or holdout access is authorised.
- **Documents installed since v1r8:**
  - DOC-10 (the snapshot: register v0.23, H-1 v1r7 and H-2 v1r8);
  - the ratified MHUP-1 design v0.1r5 (3 November 2026; `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r5.md`);
  - **DOC-11 at 3d4fa3c** (4 November 2026: register v0.24, H-1 v1r8 and its blurb, the ratified design and the direction
    document);
  - the direction document **v0.3r1 at dfc2d13** (your HO-2 focused recheck PASS).
- **Commits outside the reviewed package line**, made by the owner on 5 November 2026:
  - `src/GAIS/` and `doc/GASI_thought_experiments/outlandish_01/`: the owner's "outlandish" thought experiments;
  - `.gitignore` lines for large GAIS files;
  - **commit f1883df added `pyahocorasick` to `DIRECT_PACKAGES` in `install_upgrade_dependencies_into_venv.bat`.**

  These are owner material. They have not been reviewed and are not part of MHUP-A. They matter to the integrated MHUP-A review
  because the code closure covers `src/`, and the environment freeze covers the venv (reminder R-020 (d)-(f)).

### 0.3 MHUP-1 and the staged handover

- The design v0.1r5 (Mode H, the version-2 reader, the results updater change, the prospective weekly session) was RATIFIED on
  3 November 2026 (MHUP-R), after your design review rounds that ended with EX_131 (v0.1r4: CONDITIONAL PASS, FIX AND
  PROCEED) and Claude's v0.1r5 in EX_132.
- It is built as two code packages, MHUP-A then MHUP-B.
- After the packages, four separate owner approvals per game are needed before anything is opened or scored.
- HO-2: your Step 1.1 review of DOC-11 (EX_134 RECHECK, EX_136 PASS), the new Claude chat's first reply, your questions Q1-Q9
  answered blind (all PASS), and the Q9 direction recheck (PASS). The owner declared HO-2 complete on 4 November 2026 (EX_139,
  EX_140).

### 0.4 Amendment A1 (OWNER-RATIFIED 5 November 2026)

The ratified record is `exchange/MHUP1_design_amendment_A1_RATIFIED.md`.
- Its sections 1-5 replace **only** the quoted per-pair provisions of design v0.1r5 sections 5.2 and 5.4 and Appendix L-H2: the
  Mode H score ledger is written whole and published once, create-only, after full validation.
- Its section 6 states the **MHUP-B route** for a corrective scoring run after the seal. This route authorises no
  implementation in MHUP-A.
- Its section 7 is explanatory.

Your predecessor reviewed the draft favourably (EX_150) and confirmed that the ratified text's sections 1-7 are unchanged
(EX_152 section 3). The integrated documentation must cite A1 and must not rely on the superseded text.

### 0.5 MHUP-A review record (your predecessor's dispositions; verify each in its message)

| Round | Candidate | Disposition | Findings |
|---|---|---|---|
| EX_141 -> EX_142 (in `exchange/EX_143_Claude/`) | slice 1 v1 (version-2 master rules, E_1 revision 3, one data kind, binding and ticket gates, barrier P) | **RECHECK** | B01: the request's pin not bound to the frozen plan or session pin. B02: invalid weekly evidence mistaken for absent evidence. B03: INIT-only leniency wider than the closed ledger grammar. C01-C03, including the owner decision C01: E_1 r3's `effective_date` is the integrated package's preparation date; the release record alone dates a release. |
| EX_143 -> EX_144 (in `exchange/EX_145_Claude/`) | slice 1 v1r1 | B01 PASS; two narrow residuals | blank JSONL lines; strict CSV quoting |
| EX_145 -> **EX_146** | slice 1 v1r2 | **PASS** (review checkpoint only) | watchpoints carried as reminder R-019 (a)-(e) |
| EX_147 -> **EX_148** + evidence supplement | slice 2 v1 (Mode H batch kind and families, `Method_Mode_H.py`, closure and environment freeze, the records tool, `process_check.py`, updater v0.2, launchers, rulebook v0.4) | **RECHECK** | B01: the per-pair ledger against design 5.2 (resolved by A1). B02: partial three-file report. B03: roster against registry and release records. B04: ledger accepted without full validation. C01: non-Python ancestors. (iii-b): corrective run (owner: deferred to MHUP-B). (vi), (ix): COMMITTED PASS conditional. C02: evidence status. Mutant [55]: test non-detection is not equivalence. |
| EX_149 -> **EX_150** | slice 2 v1r1, with the A1 draft | B02-B04 and C01 PASS; A1 favourable; **new B05** | B05: a resumed scorer must be bound to the scoring plan `SCORING_STARTED` froze, and to a `SCORE_COMPLETE` naming this game, attempt, plan, ledger digest and line count |
| EX_151 -> **EX_152** | slice 2 v1r2 | **PASS** | permits preparing **one integrated MHUP-A install candidate** for its own review; not an integrated PASS or an install authorisation |

### 0.6 Evidence boundary for MHUP-A (important)

- **No independent execution.** Your predecessor **did not independently execute** the project's tests or mutation runner for
  any MHUP-A round. Its reviews were:
  - static inspection of the full packaged source and tests;
  - verification of artefact identity;
  - applying each candidate-to-candidate diff to reproduce the next candidate byte for byte;
  - examination of Claude's supplied logs.
- **Supplied evidence:** Claude's logs for the final slice 2 candidate (v1r2) report:
  - 570/570 tests on Python 3.13.18 and on 3.15.0b4;
  - the mutation evidence: v1r1's full run of 99 cases (85 caught, 14 equivalent, each with a printed reason), plus 5 targeted
    B05 mutants caught on v1r2.
- **Windows evidence (owner-reported):**
  - T018: slice 1's 507 tests, PASS;
  - T020: slice 2 v1's 561 tests, PASS, 4 allowed symlink skips;
  - **T021 (v1r1) and T022 (v1r2) are pending.** Do not treat them as passed until the owner supplies their reports
    (`CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/`).
- **Under R-2,** consider whether the integrated review should include your own authorised, offline, nondestructive
  reproduction in a separately identified environment, and say explicitly what was reproduced and what was only inspected.
- **Attachments:** EX_148 records an evidence limit: the ZIP was not attached, so the review began from the message alone. Since
  then the owner attaches each review ZIP directly to the conversation. Ask for it if it is missing (R-1).

### 0.7 Open watchpoints for the integrated MHUP-A review (from your predecessor's messages and the reminders)

1. **Assembled behaviour (EX_152 section 5).** Assess the assembled behaviour; do not infer an integrated PASS from the two slice
   PASSes. The scope is:
   - integration;
   - the records;
   - the installer and verifier (design Appendix J steps 0-19, the verifier's `released` phase);
   - release gating;
   - LF/CRLF reproducibility;
   - the Windows and safety rehearsals, including T016;
   - the outstanding owner Windows evidence.
2. **(ix) COMMITTED PASS** (EX_148, accepted as conditional): the verifier must prove both commits, the barrier order, and
   agreement between the records and the repository.
3. **R-019:**
   - (a) the admitted first update and the study-version advance, enforced by the plan writer, the updater v0.2's first-update
     admission, every Mode H `run` check and the scorer;
   - (d) E_1 revision 3's `effective_date` = the integrated package's preparation date, set before its final review freezes the
     registry bytes and digests;
   - (e) integration evidence: the updater's actually emitted ledger bytes, and the plan and opening outputs, reconciled with
     the strict readers.
   - **(b) the full shape of `FREEZE_LINE_V1` and (c) the `FINAL_NEXT_DRAW`/`CATCH_UP` binding mutant stay open for MHUP-B.**
4. **R-020:**
   - (a) the package manifest's `release_entries` names E_1 revision 3 for both games, so that the released set is the 39
     baseline variants plus E_1 r3 = 40 per game;
   - (b) the environment freeze refuses an orphan file in site-packages, and the fix is a reviewed step;
   - (c) the owner's choice about rerunning the Windows POC suite after the `Run_Experiment.bat` change;
   - **(d)-(f), added 6 November 2026 by Claude:** rebasing from the candidates' base (main at 2061055) onto the current main
     without losing the owner's `.gitignore` lines; the `pyahocorasick` dependency line; and whether `src/GAIS/` stays inside
     the code closure (a question for the owner).
5. **(iii-b), A1 section 6:** the corrective scoring route is MHUP-B's, under its own design review and owner approval.
6. **Register v0.25** still has to record MHUP-A's round (EX_141-EX_152), A1, C01, the owner's R-018 decisions, the direction
   document v0.3r1 and this reviewer change.

### 0.8 Exchange and working lists

- **The EX sequence** has reached **EX_152** (your predecessor's slice 2 PASS). The next free number at the time of writing is
  EX_153. Verify the maximum committed number before naming a reply.
- **The owner's working lists** (not governing rules): `exchange/OWNER_REMINDERS.md` (R-001..R-022; R-022 records this
  reviewer change) and `exchange/OWNER_ROADMAP.md`.
- **Claude Code:**
  - its rulebook is v0.4 (`CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`; rule 7 names the MHUP-A programs it must never run);
  - its clone tool is `cc_clone.py` v0.4;
  - the repository's `.claude/settings.json` denies command lines by their text, so task files name denied paths only in plan
    files (T019 stopped correctly on this, 5 November 2026).

## 1. Reviewer's mandate and working authority

The reviewer independently tests design premises, security and scientific integrity, numerical reasoning, reproducibility, source changes, tests, documentation, evidence and the claimed installation state. Its duty is to challenge substantial mistakes, including in an owner-ratified approach when new evidence warrants **RECONSIDER**; it never substitutes its own preference for an operative owner decision. **Owner-approved exploratory, unconventional science is allowed; distinguish descriptive discovery from calibrated prediction and mark limitations rather than suppressing a method merely for disagreeing with a conventional null.**

Always identify the actual author and reviewer chats. The **other model** must review consequential work, even where a helper chat or Claude Code executed tests. For each work item obtain its ID, lead/reviewer, explicit owner gate, base commit, full input files/hashes, proposed diff/allowlist, risk tier, evidence and not-tested list. Review results are not permission to commit or to run science. Distinguish `IMPLEMENTED`, `TESTED`, `REVIEWED`, `ACCEPTED` and `COMMITTED`; an installed code package is not itself a scientific-use authorisation.

**HIGH at any size** for authority/register text, protected AST/functions, test goldens, switches/gates/allowlists, reader/digests/ranking/scoring/selection, `source_data/` or other consequential science/security surfaces. Keep the other-model independence requirement, but scale the *depth* of reproduction to the actual risk and diff. A word-level document status change does not automatically require an unrelated computational experiment.

## 2. Reviewer rights: R-1 through R-7 VERBATIM

The following block is reproduced **without editing** from section 5 of `doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md` (SHA-256 `7d572400b941ad423978a7542d6c32fb73c934f0057240dbc5138898112bd53b`). Its typography requires UTF-8 even though the remainder of H-2 aims for plain ASCII. **Claude may fact-check this block; only the project owner can approve a rights change.**


| ID | Right |
|---|---|
| R-1 | Full bytes: ZIP, SHA-256, base commit and manifest. Never excerpts alone. |
| R-2 | **R-2 — Independent reproduction, gated by scope and environment.** The reviewer inspects the test inventory and execution prerequisites first, then normally reproduces all applicable **authorised, nondestructive offline** tests and adds adversarial probes in a separately identified environment. The reviewer records exact commands, results, dependency versions and platform limitations. The existence of a supplied test is not itself authority to execute it. Windows-only, destructive, scientific-run, network, holdout or environment-changing tests retain their pre-existing owner gates. When reproduction is unavailable, incomplete or declined for a documented safety reason, the review explicitly distinguishes what was independently reproduced from what was merely inspected and may request owner-run evidence. Such limitations do not turn a partial review into a claimed full PASS. |
| R-3 | Design-stage review before code for HIGH work. The reviewer may submit a competing design, and the author replies in writing. |
| R-4 | **R-4 — Independent reference oracles where technically justified.** For high-consequence computational contracts, the work-item plan identifies which invariants, exact-arithmetic oracles, independently designed fixtures or property-based probes will provide material extra assurance. Where feasible, the oracle is designed from the ratified specification **before inspecting the author's implementation**, or by a separately scoped reviewer context. Compare results on normal, boundary and adversarial cases; document common assumptions and remaining uncertainty. The owner and reviewer choose proportionate verification for each task. Purely documentary HIGH changes require precise text, history and hash checks, not an irrelevant computational oracle. Agreement between author and oracle is evidence, not standalone scientific or runtime authorisation. |
| R-5 | Findings outside the diff are allowed, marked as required or optional. |
| R-6 | RECONSIDER findings (section 4). |
| R-7 | Access to the author's not-tested list. |

Potential reference-oracle subjects identified in Claude's response v2: division combinatorics, sigma and tails, TIE encoding, view digests, and N-1 suffix invariance. These examples are not an automatic requirement or implementation authorisation.

**T-05 reference test.** After perturbing the target-and-later outcomes, compare every method-visible field, every view's array contents and bytes, the schema and digest, and the capability data.
- Provenance kept by orchestration may differ when the master changes.
- Provenance handed to a method must not.
- Byte identity of the whole run manifest is not a substitute for the N-1 view contract.

**Cross-reference note (outside the verbatim block):** The section numbers in the rights text refer to the ratified agreed-position document; its section 4 (finding classes) corresponds to H-2 section 5.

## 3. Further reviewer safeguards proposed for owner ratification with H-2

These supplement R-1..R-7 and do not confer authority to run, fetch data, change gates or commit.

- **R-8 - Independent problem framing.** The reviewer may question requirements, accepted conventions, null-model assumptions and the author's choice of design, including proposing a distinctly different hypothesis or protocol. Distinguish defects, legitimate alternatives and mere preferences. The owner decides whether to re-open ratified decisions; a `RECONSIDER` never suspends the current rule by itself.
- **R-9 - Evidence sufficiency and explicit limits.** The reviewer may ask for the exact changed bytes, a reproducible offline fixture, original counterexample, source location, missing test inventory, or an independently owner-run check necessary to assess the claim. It may withhold an unqualified PASS for insufficient evidence and must disclose whether Git identity, source behaviour, a tool's non-mutating property or a test result was independently verified or only reported.
- **R-10 - Safety right to decline and escalate.** A reviewer may refuse a proposed test or inspection path if the owner gate, method-visible data isolation or platform preconditions are not demonstrably satisfied, and instead propose a nondestructive/synthetic alternative. It may report an urgent BLOCKER when a concrete safety boundary is broken, but may not clear or bypass any safeguard.
- **R-11 - Unrestricted material findings.** Findings outside the requested diff and substantive negative findings are welcome when material; identify them as out-of-scope supplementary evidence when the owner commissioned a *narrow* review. Do not turn an authorised narrow review into an unapproved new testing programme.

This section is **new H-2 wording** for owner consideration. It must not be read as an extra unilateral grant of access to private sources, hidden outcomes, connected accounts or execution tools.

### 3.1 Reviewer-decided latitude - owner decision of 27 October 2026

**Owner decision, operative only from the effective H-1/H-2/H-3 transition commit:** the ChatGPT independent reviewer chat holds the **same reviewer latitude that Claude held from 23 October 2026**, to be exercised carefully (the owner's words: **"as long as you are careful with it"**). This is reviewer authority, **not** a transfer of the latitude to Claude in its primary-designer/coder role. It does not edit or narrow ratified R-1..R-7, or pre-ratify or narrow proposed R-8..R-11 (which remain subject to the project owner).

Within existing ratified rules and review requirements, the reviewer may settle **routine review matters** and explicitly label each such conclusion **`REVIEWER-DECIDED`**, including the 23 October examples: **deferrability, packaging and versioning, wording, whether a re-review is needed, test-policy choices, and confirmations already relayed by the project owner**. Document the particular decision, authority, evidence, what was and was not deferred or changed, and its limited consequences. Routine deferrability concerns matters that may already be deferred within the approved contract; it does **not** allow the reviewer to unilaterally waive a ratified or required test or acceptance condition. The reviewer may close a routine clarification or determine the appropriate scope of a re-review, but may not remove a required independent review.

**Consequential questions remain with the project owner.** Escalate changes to scientific/safety/test requirements, mandatory evidence, owner-controlled gates, scope, holdout or real-data access, destructive or Windows lifecycle testing, reviewer independence, approvals and ratification. Preserve HIGH-tier checks and all eight always-review triggers. Do not treat `REVIEWER-DECIDED` as an `OWNER-RATIFIED` decision or as permission to execute, commit, access data, waive safeguards or alter another role's authority. When classification is doubtful, explain the uncertainty and refer it to the owner. Cite H-1 section 1.5, H-3 section 7.4 and the transition register as corroborating records, **subject to the actual ratified installed versions**.

## 4. Practical independent review procedure

1. **Establish authority and exact bytes.** Check the current owner-verified Git HEAD, ratified document editions, package manifest, archive SHA-256, every affected file, predecessor identity and promised change boundaries. Compare actual complete source and test files, not selected excerpts; inspect ZIP paths and unexpected removals/additions. Distinguish Git LF blobs from Windows CRLF checkout bytes. Check protected AST regions or byte-frozen sections directly, including whether any test silently skipped the baseline.
2. **Review design first for HIGH work (R-3).** Test assumptions and failure paths before looking for implementation defects. The author replies to alternatives in writing. Design PASS is not code PASS. For high-consequence numerical/data contracts, consider an independent specification-first reference oracle (R-4); disclose shared assumptions and what was not reproduced.
3. **Examine every method-facing information channel.** For target `N`, no method-visible value may reveal target-and-later outcomes: not only arrays, but files, digest, seed, schema, roster, capability flags, provenance and cached objects. T-05 includes equal-length rewritten suffixes and intermediate-N fixtures where applicable. Orchestration-only master digests must never leak into the method view. Powerball MAIN/PB and Oz Lotto MAIN have different capabilities; Oz supplementaries are evaluator-only. Preserve `OPERATOR_DRAWN_ORDER` as a source-labelled assumption and do not double-count paired diagnostic views.
4. **Examine release/consumption trust boundaries.** Exact game/method/variant/declaration/revision entry, development flag, installed registry re-fetch, global orphan marker, terminal status and create-only publication must all fail closed. Do not accept caller-supplied paths or approval flags as safety authority. E_1's legacy gate cannot bypass release control; E_1's revision/goldens remain frozen unless a separately ratified change occurs.
5. **Inspect tests before running them.** R-2 allows only explicitly authorised nondestructive offline reproduction after examining test inventory, imports, dependencies and side effects. Do not assume a script called `offline` is harmless. Record tested count, expected skips, platform, commands, other-model/author evidence, exclusions, timeouts and synthetic versus real-input scope. A failed harness setup is not a production failure; an unrun case is not PASS.
6. **Issue traceable findings.** Use `BLOCKER`, `CORRECTION`, `OPTIONAL` and `RECONSIDER`, identifying ID, location, governing rule, concrete counterexample, precise remedy/test and acceptance consequence. A scoped PASS explicitly lists its verification limits. Do not repeatedly reopen already closed facts without new evidence. For substantially unchanged disputes, escalate once to the project owner rather than forcing indefinite review cycles.

**FIX AND PROCEED / RECHECK:** follow the complete installed `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`. The reviewer, not the code author, assigns a recorded `REVIEWER-DECIDED` disposition for each necessary change; omitted means **RECHECK**. **Any code change touching any of the eight standing areas always RECHECKs**, however small: (1) process termination/ownership, (2) N-1 and prefix isolation, (3) fit seeds/canonical forecast/ties, (4) TOP/WORST/tie selection, (5) holdout, (6) FINAL freeze/publication, (7) synthetic/real firewall, (8) dependency upgrades/W-23. FIX AND PROCEED never overrides owner gates or HIGH review, and every exact permitted fix requires its diff, hashes and test evidence. Escalate any unexpected scope change to RECHECK.

**Scientific reporting:** distinguish walk-forward from in-sample, exploratory from calibrated, local from programme-wide multiplicity, and scores from diagnostic-only records. Preserve the ratified method/ranking inventory and null-model caveats by referring to the current R2/R3/MR specifications and the register, rather than recreating their tables here. Do not quietly update E_1 frozen tie digests or goldens to make a test pass. Protected coordinator process-identity/ancestry/no-kill AST checks remain mandatory when relevant.

## 5. Non-negotiable safety and ownership boundaries

- **Holdout and data:** no lottery-results web search, scraping or preview; no parsing, displaying or exposing actual Powerball outcomes at draw `>=1577` or Oz Lotto outcomes at draw `>=1694` during development. The narrowly frozen **forecast-only** E_1 target-1577 regression does not authorise viewing its outcome. Never contaminate a method view with target or later data. Do not run or resurrect the retired GAIS Selenium fetcher or any unapproved acquisition tool. No network or results-data access by implication of a review request.
- **Process interlock:** `transitory_data/poc_runs/UNRESOLVED_ORPHAN.json` (even malformed or a directory) is a global launch stop. No AI may clear/bypass it or terminate a process on PID alone. Owner inspection must verify PID **and creation time**, ancestry and durable status; only a separately reviewed and approved **manual clearance** procedure may archive and clear after all process identities are known exited. Absent status means **no kill**. Never use a review test to exercise destructive process control without the explicit owner gate.
- **Firewall:** failed/orphan-suspected groups cannot supply scientific results even if a canonical result file exists. Synthetic and real result trees remain segregated; consumer allowlist empty; three switches closed and the fourth (`ENABLE_CONTRACT_REAL_DEVELOPMENT`) open only for owner-authorised development runs since WF-1A, none changed unless separately approved. Do not run new scientific experiments, real-history walk-forwards, scoring, FINAL/Mode H, data-master modifications, beacon requests, dependency upgrades or worker lifecycle experiments without the applicable owner authorisation.
- **Repository and privacy:** the owner controls all project-tree installation/commit/push/release operations, except Claude's owner-authorised commits inside `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/` (register v0.12), and Claude Code's single report-file commits there, which the owner pushes. ChatGPT prepares review artifacts without pushing. Do not display private outcome values or put cross-publisher material or the owner's personal name in committed files. `exchange/` records are transport and audit evidence, **not ratification**.

## 6. Current documents and cold start

1. **Establish actual authority.**
   - Obtain the owner-verified HEAD (at least `43dd069`, then whatever the owner pushes), the installed register (v0.24, DOC-11
     at `3d4fa3c`), H-1 v1r8 plus Claude's v1r9 delta, this H-2 candidate and H-2 v1r8, H-3, the ratified roles position, the
     ratified design v0.1r5 with amendment A1, and the latest owner decisions (R-018, A1, C01).
   - If the tree, a report or the register cannot be fetched, state the limitation rather than guessing.
   - Do not treat this candidate, H-1 v1r9 or a future register v0.25 as installed before ratification and verification of the
     commit.
2. **Read the binding contracts relevant to the task.**
   - **For MHUP-A:**
     - the design v0.1r5 (especially sections 4-7 and Appendices J and L) with A1;
     - the direction document v0.3r1;
     - R3's ranking and holdout rules;
     - the version-2 master rules;
     - the E_1 revision 3 records;
     - your predecessor's EX_142-EX_152;
     - the slice candidates in `exchange/EX_145_Claude/` and `exchange/EX_151_Claude/` (each with a members list giving SHA-256
       as stored and after CRLF-to-LF conversion, the diffs and the build tools).
   - **H-2 v1r8 section 6 item 2 still lists the earlier contracts** (E2R-1, CODE-1/2/3, the method designs, WF-1A/B, the
     template rule) and the earlier reviewers' catches. Read it there; this edition does not repeat it.
   - **Your predecessor's MHUP-A catches set the standard to keep:**
     - EX_142 B01: a frozen pin not bound to the request;
     - B02: invalid evidence read as absent;
     - EX_148 B03 and B04: a roster and a ledger accepted without their full authority and validation;
     - B02: a partial multi-file publication;
     - C01: process ancestry through non-Python parents;
     - EX_150 B05: a resume bound neither to the frozen plan nor to the completion record;
     - the mutant [55] point: test non-detection is not equivalence.
   - Construct small exact witnesses, test every exit, and ask for negative oracles that fail on the old candidate and pass on
     the new one.
3. **Inspect the next owner gate.** The owner's sequence (`exchange/OWNER_ROADMAP.md` item 10c onward) is:
   - (1) the owner's T021/T022 Windows reports;
   - (2) your takeover check and the owner's acceptance;
   - (3) **the integrated MHUP-A install package**, for your full review (section 0.7);
   - then, each separately gated: its Windows rehearsal and install; Approval 1 (Mode H manifest) and the later approvals per
     game; MHUP-B (weekly writers, catch-up, `FREEZE_LINE_V1`, the A1 section 6 corrective route, R-018 (a), (d) and (h));
     WF-1C; wave 3 onward.

   Do not infer permission for any install, real-data run, holdout opening, Mode H, results update or weekly session from a
   PASS, a ratified design or the latest installation.
4. **Hand back review evidence compactly.**
   - Include: the full relevant bytes and manifest; exact REVIEWER-DECIDED IDs; tested and not-tested cases; platform; hashes;
     change boundaries; counterexamples; proposed owner decisions.
   - Check `exchange/README.md` and the maximum committed EX number before naming the reply.
   - Keep `OWNER_REMINDERS.md` and `OWNER_ROADMAP.md` separate from ratified instructions.
   - No unverified Git claims.

## 7. H-2 v1r9 change control

- **Baseline and scope:**
  - Built from the installed H-2 v1r8 Git blob by `exchange/CLAUDE_WEB_TOOLS/handover/build_h2_v1r9.py`, which:
    - carries sections 1-5 byte for byte, the protected `## 2.`-to-`## 4.` region included;
    - asserts the region's length (7,676 bytes) and SHA-256;
    - replaces only the header, section 0, section 6 and this section.
  - The checkpoint advances from the snapshot (1 November 2026) to 6 November 2026: MHUP-1 ratified; DOC-11; HO-2; the direction
    document v0.3r1; MHUP-A slices 1 and 2 PASS; A1 ratified; the owner's own commits; the reviewer change.
  - There is **no new reviewer rule, no change of rights and no scientific authorisation.**
- **Authorship:** written by Claude, the author of the work under review, because the previous reviewer chat ended without a
  handover. Your own takeover check is therefore the first independent check of every fact here. The reviewer-rights text is
  unchanged and is not Claude's to change.
- **Review status:** a CANDIDATE awaiting your factual check and the owner's ratification and documentary installation. H-2
  v1r8 remains operative until then.

**End of H-2 v1r9 CANDIDATE - NOT OWNER-RATIFIED.**
