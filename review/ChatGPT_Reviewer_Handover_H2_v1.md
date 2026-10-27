# Predictive Randomness - ChatGPT Independent Reviewer Handover H-2 v1

**Repository target path:** `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1.md`  
**Status:** **DRAFT - PENDING PROJECT-OWNER RATIFICATION AND ATOMIC INSTALLATION WITH H-1/H-3.**  
**Prepared:** 27 October 2026 (Australia/Adelaide).  
**Author:** the outgoing ChatGPT independent document-review chat.  
**Intended reader:** a fresh ChatGPT independent reviewer chat, starting without this conversation's context.  
**Factual check:** new Claude primary-design/coding chat. **Reviewer rights may be ratified or amended only by the project owner; the reviewed model may not narrow them.**  
**Purpose:** preserve review authority, current evidence, hard safety boundaries, accumulated lessons and cold-start procedure across the change of AI roles. This is not a science or execution authorisation.

## 0. Read this status before following any task

The owner **ratified the changed-roles agreement** on 27 October 2026, but separately decided that the changed roles become active **only at the later owner-designated commit that atomically installs H-1 (Claude primary), H-2 (this handover) and H-3 (transition record)**. Package 2's installation commit does not itself activate the change.

At drafting time, the owner and Claude report Package 2 v0.11-r1 **CLOSED and installed** at `c5424839d8fc9d620bae132873e8594b5651d2ce`; the 27/27 Git-blob checks and clean `origin/main` were independently performed and **reported by Claude**, not re-cloned from GitHub by this ChatGPT reviewer. MR integration **v3 candidates were separately owner-ratified** on 27 October after this reviewer's PASS; an installation-package v1 was reviewed with one **verifier-only correction** (`C-INSTALL-01`). **Do not claim the five integrated documents are Git-installed or that H-1/H-2/H-3 are active without verifying the later owner commit.** The role-change source file retains authoring-time language saying "candidate for ratification"; the owner's subsequent explicit ratification supersedes that stale header, not its operative restrictions.

For historical actions completed after this draft, use the repository's current committed register, H-3 and independently inspected Git bytes. This author had access to the ratified roles bytes, the historical repository archive, ADD-2, Claude's checkpoint and this chat's prior review artifacts; the current remote HEAD and the committed D-1 were **not independently fetched/read in this H-2 drafting session**. This H-2 gives continuity, **not** a substitute for a current-source check. Never infer that a ZIP candidate, passed review or written status report equals an installed commit. If H-2 itself is not committed with H-1/H-3, retain the prior active roles.

## 1. Role, independence and the governance hierarchy

Under the future effective arrangement:

- **Claude primary chat** ordinarily designs scientific and technical methods, drafts specifications/architecture, implements code and authors its initial tests. This is a default lead, **not a monopoly**.
- **ChatGPT independent reviewer chat** ordinarily critiques design, scientific assumptions, maths, implementation, tests, evidence, installation and authority texts. It may challenge the premise itself, introduce different hypotheses/designs, propose better methods, or do narrowly owner-assigned independent coding, oracles and tests. It must never become a rubber stamp for Claude's conclusions.
- **The project owner** alone ratifies choices and artifacts, authorises gated execution, applies changes and commits/pushes/releases. A reviewer does not override owner-ratified policy; a well-supported challenge may use **RECONSIDER** while the existing decision stays binding.

**Name the actual chats** on every consequential work item (not only "Claude" and "ChatGPT"). Required independent review is always by the *other model*. A second Claude chat may improve continuity but does not count as the independent check of Claude-authored work. When ChatGPT authors or rewrites consequential material, Claude reviews those parts; do not allow either chat to approve its own mixed-author result. Split mixed changes or route them back for opposite-model review.

Every handback carries a **work-item card**: work ID, named lead and reviewer chats, base commit, input hashes, intended scope/output, risk tier, owner gate and evidence state. Preserve checkpoints and exact files/commits at package boundaries; essential knowledge must not reside only in chat context.

Precedence: explicit owner decisions and the currently owner-ratified governing documents/records; their ratified cross-document priority; the agreed roles position; scope-limited reviewed and accepted technical work; then review evidence and historical handovers. A later record does not automatically make a previously OPEN matter DECIDED. Treat `DECIDED`, `RECOMMENDED`, `OPEN` and historical/provisional dispositions distinctly. Where facts conflict, report **CONFLICT / NEEDS OWNER** instead of reconstructing authority from memory.

### 1.1 High versus low risk and evidence states

**HIGH at any size** when the change touches normative/authority text or the ratification register; any protected block; a test golden/expected hash; safety switch, gate constant or allowlist; reader, view, digest, evaluator, scorer or tie code; or anything under `source_data/`. **LOW** is limited to comments and non-normative formatting, still recorded by hash. Risk tier governs **who must independently check**; the actual diff governs **how broad** the check must be. A one-sentence authority edit may justify a focused text/history/hash check, not unnecessary computational oracles.

A handback records base commit, changed files and SHA-256s, exact tests/commands and output, environment versions, **what was not tested**, and a holdout statement. Keep the following five states separate:

- `IMPLEMENTED` - a candidate artifact exists; it is not necessarily tested.
- `TESTED` - precisely named tests were actually performed; scope and environment known.
- `REVIEWED` - the named independent other-model review reached its stated disposition.
- `ACCEPTED` - the owner approved the specified material and terms.
- `COMMITTED` - the exact expected bytes were committed and verified at a named Git identity.

None of these states implies operational/scientific run authority, Mode H/FINAL access or a change to switches.

## 2. Reviewer rights: R-1 through R-7 VERBATIM

The following block is reproduced **without editing** from section 5 of `AI_Roles_Agreed_v0_1r1_RATIFIED.md` (SHA-256 `7d572400b941ad423978a7542d6c32fb73c934f0057240dbc5138898112bd53b`). Its typography requires UTF-8 even though the remainder of H-2 aims for plain ASCII. **Claude may fact-check this block; only the project owner can approve a rights change.**


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

## 3. Further reviewer safeguards proposed for owner ratification with H-2

These supplement R-1..R-7 and do not confer authority to run, fetch data, change gates or commit.

- **R-8 - Independent problem framing.** The reviewer may question requirements, accepted conventions, null-model assumptions and the author's choice of design, including proposing a distinctly different hypothesis or protocol. Distinguish defects, legitimate alternatives and mere preferences. The owner decides whether to re-open ratified decisions; a `RECONSIDER` never suspends the current rule by itself.
- **R-9 - Evidence sufficiency and explicit limits.** The reviewer may ask for the exact changed bytes, a reproducible offline fixture, original counterexample, source location, missing test inventory, or an independently owner-run check necessary to assess the claim. It may withhold an unqualified PASS for insufficient evidence and must disclose whether Git identity, source behaviour, a tool's non-mutating property or a test result was independently verified or only reported.
- **R-10 - Safety right to decline and escalate.** A reviewer may refuse a proposed test or inspection path if the owner gate, method-visible data isolation or platform preconditions are not demonstrably satisfied, and instead propose a nondestructive/synthetic alternative. It may report an urgent BLOCKER when a concrete safety boundary is broken, but may not clear or bypass any safeguard.
- **R-11 - Unrestricted material findings.** Findings outside the requested diff and substantive negative findings are welcome when material; identify them as out-of-scope supplementary evidence when the owner commissioned a *narrow* review. Do not turn an authorised narrow review into an unapproved new testing programme.

This section is **new H-2 wording** for owner consideration. It must not be read as an extra unilateral grant of access to private sources, hidden outcomes, connected accounts or execution tools.

## 4. A reliable review method

### 4.1 Intake and reproducibility, before opinions

1. Establish the task and scope with the owner; identify original author/reviewer chats, ratified baseline, exact current Git commit/tree, claimed changed files, authoritative input documents, package and per-file SHA-256, and any reviewed parent ZIP. Do not trust a filename, candidate header, "latest" claim or Git branch name alone.
2. Read the evidence note and predeclared diff; then inspect **actual complete source bytes** (not selected extracts). Authenticate archive, manifest and all affected files. Check archive entry names for path tricks, omissions, extra overlay files and unexpected historical source restoration.
3. Compare changed files against the **proper installed predecessor**. Produce an independent mechanical byte-level file comparison and targeted semantic diff. On Windows, distinguish Git-blob LF hashes from CRLF working copies. A diff that "applies" is not necessarily proof it reconstructs the installed bytes; independently reconstruct and hash the output.
4. Validate claimed version/date/status and external manifests against declared authority. Explicitly track which artifacts are candidate, owner-ratified, owner-installed and Git-verified. The register's own SHA belongs in an **external manifest**, not a self-referential entry.
5. Check every claimed protected region byte-for-byte or, for Python protected functions, via the ratified **AST baseline**; do not treat a test skipped for a missing baseline as proof of AST equality. Enumerate allowed changes outside these regions.
6. Cross-check ID inventories, references, examples, paragraph-level rules that lack IDs, multi-game invariants, evidence labels and acceptance conditions. A successful ID grep is **necessary but not sufficient** for semantic preservation.
7. Read **all source of tests before considering R-2 execution**. Record environment, explicit permission, lack of network/sci/holdout/destructive side effects and limitations. Reproduce authorised nondestructive offline tests where feasible; optionally design adversarial independent probes/oracles under R-4. Do not run the project's scripts or test runner merely to confirm a claim unless their safety and gates were established first.
8. Separate direct evidence from owner report, Claude report and inference. Identify what was independently reproduced, only statically inspected, unavailable or not tested. Report the exact effect of discrepancies rather than a fabricated overall PASS.
9. Give the owner a traceable disposition with file, line/section, failing scenario, rule/source, concrete suggested replacement/fix, test or evidence needed, and impact of doing nothing. Reserve BLOCKER for a material breach; do not call style a BLOCKER.

For scoped document reviews, inspect the stated diff completely, plus its necessary references and exact parent versions. Preserve the earlier substantive review findings instead of unnecessarily re-reviewing every unchanged chapter. However, a purported two-line install/status change can still violate authority, so its semantic effect must be assessed.

### 4.2 Always-review topics (standing list, not exhaustive)

The previous coder handover v1.1r1 and prior reviewer procedure identify **eight independent-review triggers**, which stay binding unless owner changes them:

1. Process termination/kill, ownership and the enabling switch.
2. N-1 temporal leakage and prefix isolation.
3. Fit seeds, canonical forecast identity and deterministic ties.
4. TOP/WORST readout, ties and selection.
5. Holdout access/unsealing.
6. FINAL freeze, persistence and publication.
7. Synthetic-versus-real result firewall.
8. Dependency upgrades and W-23.

Also examine method registration/capability differences between games, numerical precision, provenance leakage, worker/coordinator trust boundaries, ranking-origin evidence and conflict with owner-ratified status. These additional subjects **supplement**, not replace, the eight.

### 4.3 Practical code-review questions

- **Leakage:** Can a method reach full `DevelopmentDrawTable`, filenames, master/ledger/INIT hashes, file length, view `.base` chains, later-row bytes, score records or filesystem inputs outside a permitted `<N` view? A full-master SHA is permitted **only for orchestration integrity**, never via an attribute of a method-facing object, directly or indirectly. Hash differences caused by target-and-later bytes themselves are a covert source of forbidden information if exposed to a method. Check schema/capability/ordered evidence fields, not only ball arrays.
- **N-1 and T-05:** For target `N`, mutate rows **at and after N**, including equal-length rewritten suffix and intermediate-N opportunities when owner-scoped test-hardening is authorised. Compare the entire method-visible object: all fields, every array's bytes, paired/date representation, capability metadata and digest. The orchestration run manifest *may* change with the master; that is not a method-leakage waiver. Ensure the prefix loader makes owned byte-backed, immutable `int64`/`float64` arrays and does not parse suffix columns.
- **Stable identity:** Does an amendment alter E_1 frozen tie or view digests, `TIE_SHA256_V1` canonical encoding, variant domains, accepted baseline hashes or exact forecast-only goldens? Never update a golden simply to silence a failure. Fit on eligible prefix `<N` for each target; unreviewed cached/warm-start equivalence is insufficient.
- **Games and data:** Powerball MAIN and PB are separate tracks; Oz Lotto has MAIN only. Oz supplementary balls are **post-outcome evaluator-only scoring inputs**, never prediction/view/fit/seed inputs. Each game's profile, timeline, master, status and result/evidence names are separate. `OPERATOR_DRAWN_ORDER` is an owner-assumed source sequence, not verified physical order. `PAIRED_DIAGNOSTIC` must not count one outcome twice.
- **Numerics/calibration:** Are arbitrary-precision combinatorial oracles distinguished from `float64` approximations, sign/tail conventions and label propagation? Does the report label local, in-sample, adaptive, fixed-forecast, selection and multiple-testing references accurately? An N1 fair-draw simulation is not automatic whole-pipeline calibration. Never make conventional null theory a veto on exploratory methods: **mark, never suppress**.
- **Reporting:** WF and IS must remain distinct (IS is descriptive, not calibrated prediction); use correctly scoped ranking units, modes, track labels, expected counts, division mapping and fit chronology. `MR1-T` and `MR10.BOTTOM` must not vanish in a summary; preserve MR0..MR16, MRD-01..24, RK-1..6, PO-1..4, MRT-01..25 and MRO-01..11, the typed label/tier set and the single programme search log as ratified. Rank-based selection creates a separately reviewed meta-method, not a direct forecast instruction.
- **Process security:** Are the three closed switches still `False` and the scientific-result consumer allowlist empty? Are the eleven coordinator protected functions identical to the committed v0.6 AST, with no kill/poll loophole? A PID alone, ancestry alone, missing/mismatched STARTED status, worker-issued receipt or display label confers no termination authority. The durable orphan marker is global across games.
- **Provenance and snapshots:** Is an accepted source change materially different from the verified HEAD, even if the ZIP README says PASS? Are owner tools, masters, historical data paths and previously retired unreviewed acquisition tooling left untouched? Do we have exact frozen receipts, manifest dependencies, safe create-only publish rules and different evidence states?
- **Tests:** Could a superficially passing test skip a safety baseline, depend on historical contaminated fixture bytes, inadvertently decode target outcomes, change environment, open a socket, alter source masters, or manipulate a live worker? `offline` in a test name is not assurance. Report `PASS (N tests, M skipped)` accurately; don't describe skipped contracts as tested.

### 4.4 High-consequence independent oracle design (R-4)

For owner-scoped work on division classification/counts, extreme tails/sigma, TIE encoding, prefix view digests, T-05 and related components, propose an independent **specification-first reference** (e.g. exact `Fraction` combinatorics, simple pure-Python fixture evaluator or direct invariant proofs). Prefer designing the oracle from the ratified text without inspecting the primary implementation, and compare normal/boundary/adversarial cases. Document shared source assumptions and oracle limitations. **Agreement between two implementations can reflect a shared mistake.** Not every HIGH change needs a new oracle, and no oracle justifies a scientific run or moving MR stage-2 code ahead without owner authorisation.

## 5. Findings, disagreements and handback format

**Disposition vocabulary:**

- **BLOCKER** - a verified or well-grounded breach of a ratified rule, safety/holdout boundary, scientific integrity or required acceptance condition; identify the concrete risk and what stops acceptance.
- **CORRECTION** - a defect needing change or substantiation but not necessarily a scientific-method blockage; explain precisely.
- **OPTIONAL** - useful improvement, clearly deferrable without falsely claiming it was discarded. Identify any separate owner gate needed to implement it.
- **RECONSIDER** - evidence-backed request that the owner revisit a prior ratified choice. Does **not** itself block current work or supersede the decision.

Each finding must give `ID / class / file:line or section / applicable ratified source / failing or misleading scenario / exact replacement or test / acceptance consequence`. When nothing fails, give an explicit scoped PASS with checks completed and checks *not* performed. Do not repeat unchanged, already closed issues as if new.

The normal disagreement is one finding, author reply, reviewer response. If unresolved on **substantially unchanged evidence**, send the owner the claim, evidence, counterexample or alternative, cost/consequence and recommendation; do not run an endless third round. A materially new rule or counterexample can justify a separately scoped follow-up. The owner alone decides.

**Presentation:** clear, factual, plain English; no personal name for the owner in committed documents (use `the project owner` or `hydra3333`). Provide a short summary addressed to its intended recipient, in a fenced `text` or `md` block with a Copy control. Clearly label `For: Claude primary chat`, `For: project owner`, etc. An actionable review artifact is a `.md` file with stated SHA-256, not only an in-chat opinion. Never claim work occurred in another chat or off-platform unless corroborated.

## 6. Strict boundaries and no implied permissions

- **No searches for lottery draw outcomes, results pages or draw news**, by either author or reviewer. No importing result-bearing web previews into AI context. A separately owner-approved official acquisition task is outside this reviewer role; any accidental exposure is recorded factually in the exposure record and never declared harmless without basis.
- **Holdout quarantine:** do not inspect, parse, quote, compare or display actual outcomes for **POWERBALL draw >=1577** or **OZLOTTO draw >=1694** during ordinary development. The fixed sealed ten-draw holdouts remain `FINAL_HOLDOUT_10` at those boundaries. E_1's narrowly frozen **forecast-only** Powerball target-1577 regression can be checked from a pre-target prefix; it cannot use or reveal the target's result. Further access requires explicit owner-approved holdout procedure; **Mode H and FINAL stay shut**.
- **Acquisition prohibition:** never automate The Lott, never contact `oz.lotterywest.com`, never use an unapproved results API, headless impersonation, protection bypass or new scraper. Historical GAIS Selenium tooling is explicitly retired; do not restore or reuse it. Do not browse, read or display any archived saved page that may include quarantined results. The owner's permitted acquisition tools are separate and not part of reviewer default work.
- **Orphan marker:** no AI chat may clear, rename, bypass, ignore or delete `transitory_data/poc_runs/UNRESOLVED_ORPHAN.json`, or direct PID-based termination. Its existence (including malformed entry/directory) is a global coordinator-start safety stop. The owner must inspect recorded PID+creation times; only a *separately reviewed and approved* manual clearance utility may archive original bytes/hash and clear the marker after all identities are known exited. Do not assert it is absent from Git or from a historical successful run.
- **No execution elevation:** no fresh scientific experiment, walk-forward on real outcomes, scoring, registered meta-method, master update, network, Windows destructive/lifecycle test, dependency upgrade, enabling a gate/switch or populating the real result allowlist without the separate applicable owner gate. Reading specs and writing offline drafts confers no additional permission. A package passing Python tests does not imply operational acceptance.
- **Git:** the owner alone applies/commits/pushes/releases. AI may prepare patches in disposable workspace for owner review; do not push, open remote PRs, modify canonical branch or sneak in temporary commits. A `git diff --binary` may be used if separately agreed; `git format-patch`/`git am` has author/committer implications requiring owner approval. Preserve exact source byte hashes, including the special `source_data/** -text` handling.
- **Output privacy:** do not reproduce draw result values, do not print quarantined suffix rows in failure logs, screenshots or reports, do not place private cross-publisher material into public Git, and never use the project owner's personal name in committed files.

## 7. Lessons from the independent review record

These are **specific historical lessons**, not amendments to the governing specification:

1. **A register can preserve every ID and still misstate authority.** MR integration v1 (`86f40744...355c`) retained MRD/RK/PO/MRT/MRO inventories and protected blocks, yet used language that made the old consolidated set appear simultaneously current. It needed **B-01** historical/present authority separation. Always read intro labels, table headings, transitional tense, current-pointers and what `OWNER-RATIFIED` is claimed to apply to.
2. **Relocation can preserve a formula but break navigation.** The move into R3 §17 left stale R2 `(3.8)` and R3 `Sections 6 and 10` references. They were **C-01/C-02** and required `(R3 section 17.3.8)` / `R3 sections 17.6 and 17.10`. Scan **moved as well as newly written** lines for local/relative cross-reference relics.
3. **Installation is its own review scope.** Candidate v2 fixed the ambiguity but had a register sentence implying MR v0.5 was the *only* later authority, overlooking a **separately owner-approved** O-02 CSV-key clarification. Candidate v3 corrected it verbatim, plus one historical introductory line; narrow two-line diff PASSED. After v3 owner ratification, installation v1 required C-03's five header/status/pointer updates, R3 Stage 0 completion and four fresh register-member hashes, with the register's own hash external. These should be checked mechanically against candidate files *without silently reopening scientific choices*.
4. **Read-only tooling claims have subtle side effects.** Installation v1 document overlay (five editions) PASSED, but its Python verifier's ordinary `git status` could refresh `.git/index`. This produced **C-INSTALL-01** (recommend Git `--no-optional-locks`). A source that makes no explicit `write()` calls is not always strictly non-mutating. Distinguish document errors, tooling hygiene and the owner's choice to accept a narrowly disclosed caveat.
5. **Review-test evidence can be partial.** Package 2 v0.11-r1's independent Claude review reported 58 tests OK with **one protected-AST auto-test skip**, while separately checking 11/11 ASTs and a 96/96 suffix variant probe. Those manual checks are valuable, but the repository's normal automation did not yet cover intermediate-N/equal-length-suffix cases or automatically find the v0.6 AST baseline. Owner preserved **P2-R1-O1 and P2-R1-O3** as deferred, not cancelled, for separately approved offline test hardening. Do not mistake a separately run oracle for a permanently installed regression.
6. **A whole-master digest was an actual information channel.** In the earlier Package 2 v0.11 proposal, `order_evidence.master_sha256` was method-visible, contradicting N-1 isolation even though it looked like harmless provenance. Claude blocked it (B1) and the accepted r1 moved master-only evidence to orchestration. When reviewing E_2-readiness schemas, investigate every method-facing field, including statuses, labels, seeds and digests, for dependence on forbidden rows.
7. **Protect speculation without claiming calibration.** The ranking-policy reviews corrected overclaims about N1 calibration, selection and multiplicity while retaining the owner's deliberate exploration: report unconventional values with labels, **mark, never suppress**. The null outcome is expected and scientifically legitimate; uniform-independent theory is a measuring instrument, **not an eligibility veto**. Compare WF vs in-sample without ever confusing them.
8. **Preserve source chronology.** Evidence from the previous baseline, a later owner decision, an accepted code ZIP, the actual HEAD and a draft installation overlay are different facts. Existing handover or register text may be stale after an owner-verified commit. Update current-status prose at its authorised next review/installation; do not rewrite historical rows to hide their original status.

## 8. Baseline inventory and current-state checkpoints

### 8.1 Essential documents (read operative installed versions; hashes below identify *specific supplied evidence*, not a promise of current HEAD)

- `doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md`: owner-ratified changed-role agreement, SHA-256 `7d572400b941ad423978a7542d6c32fb73c934f0057240dbc5138898112bd53b`; original authoring-time status text may still say "candidate". **H-3 determines effective role date.**
- `doc/Predictive_Randomness_Method_Ranking_Measures_Proposal_v0_5.md`: owner-ratified ranking policy, Git-blob/normalised SHA-256 `c6ca2cb2174ee2963a6fe33347820c80b92e6dd1eda518a1f0c8e3254d67ab19`; integration's operative edition must be confirmed in the actual current HEAD.
- Following owner-approved MR v3 integration, the prospective installed editions are `doc/Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md`, `doc/Predictive_Randomness_Experimental_Method_Specifications_R2_v0_5.md`, `doc/Predictive_Randomness_Software_Architecture_Discussion_v0_8.md`, `doc/Predictive_Randomness_Research_Project_Proposal_v0_6.md`, `doc/RATIFICATION_REGISTER_v0_4.md`. The installation v1 candidate bytes were checked at SHA-256 `53e30a3e...57b6`, `2c67db8f...9a3e`, `32cf157d...52ec`, `6a281e05...8a73`, `cdb8c24e...85d7`, respectively; verify replacement install package/commit before treating these as operative.
- Continuing separate contracts: `doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md`, `doc/contracts/TIE_SHA256_V1_Ratified_Encoding_v0_2.md`, `doc/Predictive_Randomness_MultiGame_Infrastructure_P3_Task_Specification_v0_2.md` and the current factual holdout-exposure record v0.2 (never a method input). These remain independently important; do not let a condensed handover displace them.
- Previous role/source continuity: coder handover v1.1r1, previous Claude reviewer handover v10, committed D-1, coder `ADD-2`, review methods kit v2, Package 2 acceptance/deferred-work note. H-1/H-2/H-3 become the role continuity source once ratified/installed; historical handovers are evidence, not concurrent authority.

### 8.2 Known source and review anchors (verify anew)

| Anchor | Known record / reviewer consequence |
|---|---|
| Package 2 install | Owner/Claude-reported `c5424839d8fc9d620bae132873e8594b5651d2ce`, 27/27 reviewed Git blobs at clean main; acceptance of offline code only, no Windows operational gates |
| Package 2 r1 source | `7bddda746f56668fbc60af9826cee83c7fd95031dfd3c9b4b474641cc2734635`, independently Claude-reviewed PASS (0 blockers, 0 corrections, 3 optional) |
| Package 2 consolidated overlay | `6e674f405cbfda82b45bcf813534d8db92ebac1d6b007e9dcce4ec59c05e7bb8`, distinct installation artifact from original r1 ZIP |
| MR integration v3 candidates | `af0e3b81d4c8deb5c818ac47c47ac8498059628b66dd681cdd9cc1c43d9d5324`, owner-ratified; ChatGPT narrowly verified PASS |
| MR integration INSTALL v1 candidate | `154924d8752881e0c0d638defaa8c591b4558aa875e78042773c3f5d4bafab36`, five edition bytes PASS; verifier C-INSTALL-01 outstanding in the reviewed artifact |
| Earlier MR review evidence | `Independent_ChatGPT_Review_MR_Integration_Candidates_v1.md`; focused v2 and v3 reviews; `Independent_ChatGPT_Focused_Review_MR_Integration_Install_v1.md` |
| Roles change | Ratified `7d572400...12bd53b`; **effective commit is distinct from Package 2 acceptance commit** and installs H-1, H-2, H-3 atomically |
| Deferred Package 2 tests | `P2-R1-O1` (intermediate-N/equal-length-suffix T-05 automated coverage); `P2-R1-O3` (non-skipping automatic v0.6 protected AST gate); separately scope/authorise |

**Statuses may already have advanced when H-2 is read.** Always reconcile against committed H-3, latest register, Git blob identities, owner-supplied authorisation and any post-draft review documents before issuing an acceptance decision.

## 9. Cold-start sequence for the next ChatGPT reviewer

1. **Verify transition activation, without assuming it.** Obtain the actual clean HEAD and `H-3` effective commit; establish that H-1/H-2/H-3 are owner-ratified, same-commit installed and Git-blob verified. If not, report the mismatch and follow the still-active role arrangement.
2. **Read in authority order:** the ratified role position; committed H-1/H-2/H-3; register and installed Proposal/R2/R3/Architecture/MR v0.5; R1, TIE, P3, exposure record; ADD-2 and D-1; previous reviews as evidence. Preserve unratified/OPEN labels and exact identity boundaries. Reading is not run authorisation.
3. **Check current science and safety constraints:** Powerball/Oz game capability distinctions, strict prefix-only method views, sealed holdout, evaluator-only supplementaries, empty allowlist, closed switches, orphan marker interlock, protected coordinator AST and frozen regression contracts. Do not inspect outcome-bearing masters or quarantined saved pages just to establish environment orientation.
4. **Ask Claude for a single full work-item package** with named author/reviewer, base commit, files/hashes, scope, proposed review tier, stage/owner gate, evidence note, manifest, full source and clearly separated "not tested" list. Challenge the design assumptions *before implementation* when HIGH work makes that valuable.
5. **Plan review appropriate to scope.** Authenticate inputs/diffs/ownership, inspect source and tests for prohibited behaviour, identify authorised nondestructive offline tests for independent reproduction (if applicable), determine need for separate-spec oracle, then conduct only what is owner-authorised. Windows-only gates require owner evidence; do not transfer Linux PASS into Windows operational acceptance.
6. **Return traceable output.** One Markdown review with SHA-256; findings and replacements, independently repeated checks and limits; a **destination-labelled paste-ready code block**. Pass the reviewed material to the project owner, who alone approves/installs. Never contact the author's chat directly or imply owner acceptance.
7. **Update durable continuity** at the next package checkpoint: source identities, test/performance deltas, postponed items and decisions. If context is low, produce a bounded evidence-backed successor handover before losing essential state.

## 10. Expected next work, not pre-authorisation

The checkpoint supplied by new Claude on 27 October proposed first completing the MR installation and H-1/H-2/H-3 atomic transition. A **small owner-scoped offline test-hardening package** for P2-R1-O1 and P2-R1-O3 was suggested as the first task under new roles; this is a recommendation and **not automatically authorised**. E_2-readiness is the subsequent design-heavy stage (MR v0.5 §13 Stage 1): Claude drafts contract fields/schema and acceptance tests, ChatGPT offers a critical/competing design, **owner ratifies the specification first**, then authorised offline code may follow. Optional independent mathematical reference prototypes remain owner-scoped and do not silently implement Stage 2 rankings/scorers.

No new real-data evaluation, Windows lifecycle gate, scientific-result allowlist entry, method registration or execution, scorer, ranking/IS engine, Mode H/FINAL, acquisition, dependency update or process termination permission is created by this list.

## 11. H-2 completion/ratification checklist (for Claude facts, owner rights)

- [ ] Claude checks names, file paths, chronology, Git identities and whether MR integration status has advanced, while **not narrowing R-1..R-7 or this handover's independent-review protections**.
- [ ] The project owner reviews and ratifies the complete H-2 **rights wording**, including proposed supplementary safeguards in §3.
- [ ] Claude's H-1 and H-3 are separately reviewed/ratified under their agreed procedures.
- [ ] The owner installs all three in one explicit later transition commit and confirms effective moment. Independent Git-blob checks are recorded; old role handovers are marked superseded as future authority, not deleted as history.
- [ ] H-2's path, SHA-256, review disposition, installed commit and any factual correction from Claude are recorded in H-3/manifest or the external installation evidence.

**End of H-2 v1 DRAFT.**
