# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v1r3

**Document:** H-1 under the agreed roles position v0.1r1, section 9 item 4.
**Version:** v1r3 DRAFT, 28 October 2026 (Adelaide, UTC+10:30). v1r3 is a records refresh (work item DOC-3): it brings v1r2 (owner-ratified 28 October 2026 and installed at `be18548`) up to date with the events and owner decisions of 28 October 2026: the E2R-1 specification, DOC-2, NAMES-1, the E1-ALIGN design, the phone exchange protocol, Python 3.15 and the indefinite oversight instruction. Appendix C lists every change; Appendix B (v1r2's changes) is kept. Author: Claude. Independent reviewer: the ChatGPT reviewer chat. The project owner ratifies.
**Status:** DRAFT for review. It becomes authoritative only when the owner ratifies it and installs it together with register v0.9; until then H-1 v1r2 stands. Nothing here grants any run, test, data-access, holdout, termination or Git permission.
**Audience:** any later Claude chat that takes over as primary designer and coder; the ChatGPT reviewer chat; the project owner.
**Repository:** `hydra3333/analysing_perceived_randomness_in_reality`, public GitHub, branch `main`.
**Baseline described:** NAMES-1 installed at `52ebeaa385fd05b18c4f3805c3cd2000948e343d` (verified by Claude from GitHub: 27 renames, 27 edited and 15 added files, every blob matching its manifest; the immediate recovery check passed; section 7.1B), on top of DOC-2 at `908db9ea9d4a37b17833f5d43919804c78ef7e14` (section 7.1C), DOC-1 at `be185485693f29cf9ab28292dc6eebad00bbc32c`, TH-1 at `744afea`, the integration at `ae76c29` and Package 2 at `c542483`. Later commits up to `83d1515` are `exchange/` records only (section 1.6). The commit that installs this file cannot name itself; Claude records its ID in the post-push verification.
**Replaces, for future roles:** H-1 v1r2 and v1r1 (kept as history); and, as before, Claude reviewer handover v10, ChatGPT coder handover v1.1r1, the interim note and Claude checkpoints v2 and v4. They stay in the repository as evidence. D-1 and ADD-2 are inputs to this file, not authority.
**Authority:** the repository's ratified documents prevail over this handover wherever they conflict. This file summarises and points to them.
**Holdout discipline for the reader:** no winning, Powerball or supplementary number of any draw appears here. The only number lists are the frozen E_1 *forecast* outputs (section 7.2). Never display, paste or compute with an outcome for Powerball >= 1577 or Oz Lotto >= 1694.

---

## 0. First actions in a new Claude chat

1. Clone `main`. Verify that this file is the H-1 edition the current register names, and that the hashes in sections 4 and 7 match `git show HEAD:<path> | sha256sum`.
2. Read, in order: this file; H-2 (so you know what the reviewer will check); H-3; the review-disposition procedure (`review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`); `exchange/README.md` (the phone exchange protocol, section 1.6); the register (current edition); the governing set in section 4, including the E2R-1, NAMES-1 and E1-ALIGN specifications; the latest checkpoint file in `doc/HANDOVER/`, if newer than this file; the newest `exchange/EX_NNN_*` files, which show the latest open exchange with the reviewer.
3. Ask the owner where things stand, using section 9 as the list. Do not assume any item has advanced since this file was written.
4. Before any code: name the work item, its risk tier and its reviewer chat (section 1.2), and check that the owner has scoped it.
5. Keep a running checkpoint file (`doc/HANDOVER/Claude_Checkpoint_vN.md`) at each package boundary, so no state lives only in the chat. When the chat nears its limit, write the next handover first.

---

## 1. Roles and workflow (agreed position v0.1r1, ratified)

### 1.1 Who does what

- **Claude (you):** normally leads scientific and technical design, specifications, governing-document integration, primary code and its first tests. You prepare complete, hash-recorded packages; you never open pull requests, and you never change anything in the main tree. **The one exception (owner-authorised, 28 October 2026; `exchange/README.md` v0.3):** you commit and push inside `exchange/` only, recording every exchange file from both AI chats byte-for-byte (section 1.6).
- **ChatGPT reviewer chat:** normally leads independent scientific and technical review. It may propose competing designs, methods and hypotheses, and may do bounded coding, alternative implementations or tests when the owner assigns them. Its handover is H-2.
- **Project owner** (GitHub `hydra3333`): sole ratifier, execution authoriser and committer. Runs every Windows test and every data tool on their own PC. **Never name the owner in anything that may be committed**; write "the project owner" or "hydra3333".
- Both models may challenge each other with evidence. Neither may override an owner-ratified decision. The owner may revise the allocation at any time.
- **The ChatGPT coding chat retired on 27 October 2026**, after ADD-2 and the Package 2 installation overlay. The earlier Claude reviewer chat retired after D-1 (26 October). Neither is consulted again except in exceptional circumstances.

### 1.2 Author and reviewer rules

1. Every consequential deliverable names its **author chat** and its **reviewer chat**.
2. The required independent review is always by the **other model**. A second Claude chat never counts as the independent review, however careful.
3. **Mixed authorship:** if the reviewer rewrites consequential parts of your patch, those parts come back to you for review, or become a separate package. Nobody approves its own mixed result.
4. **Work-item card** at the top of every handback: item ID; author and reviewer chats; base commit; input hashes; scope; risk tier; owner gate; evidence state.

### 1.3 Risk tiers and evidence (agreed position section 3)

- **HIGH, whatever the size:** normative or authority text in a governing document or the register; a protected block; a test golden or expected hash; a safety switch, gate constant or allowlist; reader, view or digest code; evaluator, scorer or tie code; anything under `source_data/`.
- **LOW:** comments, and formatting in non-normative text (still hash-recorded).
- The tier decides who must check; the scope decides how much checking is needed.
- **Every handback carries:** the base commit; changed files with hashes; exact test commands and their outputs; environment versions; an explicit not-tested list; a holdout statement.
- **Evidence states are distinct:** IMPLEMENTED, TESTED, REVIEWED, ACCEPTED, COMMITTED. Never use one for another.

### 1.4 Findings, rights and disagreement

- Finding classes: **BLOCKER, CORRECTION, OPTIONAL, RECONSIDER**. RECONSIDER asks the owner to revisit a ratified decision; it never blocks by itself. Each finding cites file and line, the failure scenario and replacement text. A style preference is never a BLOCKER.
- **The reviewer's rights R-1..R-7** (agreed position section 5; H-2 restates them): full bytes, never excerpts; independent reproduction of authorised offline tests (R-2); design-stage review before code for HIGH work, including a competing design (R-3); independent reference oracles where justified (R-4); findings outside the diff (R-5); RECONSIDER (R-6); access to your not-tested list (R-7). H-2 also sets out R-8..R-11 (problem framing, evidence sufficiency, declining unsafe tests, material findings outside a narrow scope); the owner ratified them with H-2 on 27 October 2026, and they bind equally. **Support these rights; never narrow them.** Supply everything the reviewer needs to reproduce your results.
- **Disagreement:** finding, author's reply, reviewer's response; if still open, it goes to the owner as claim, evidence, counterexample, consequence if wrong and recommended decision. Two rounds on unchanged evidence; a new counterexample opens a new finding. Never withhold evidence; never relitigate a settled point without new evidence.

### 1.5 Decision labels and the always-review list

- Report decision status as **DECIDED** only for already ratified owner choices, or for purely mechanical implementation choices explicitly inside the approved scope; cite the authority. Label proposed consequential choices **RECOMMENDED**, and unresolved ones **OPEN**. Claude does not independently ratify a new scientific, safety, test or review policy. The reviewer checks your DECIDED list for anything that should have been RECOMMENDED.
- Claude may choose routine internal coding organisation, packaging details, version labels and presentation that neither alter the approved scope nor affect an applicable acceptance or review gate. Decisions to defer a ratified or required test, change required evidence, waive or reduce an independent review, change a safety gate, or accept a consequential deviation go to the project owner for decision, with independent reviewer input where required. Other consequential items also go to the owner: new rules or scope, anything that weakens safety, switch-on or destructive tests, ratifications, real-data gates, anything irreversible. The HIGH-tier and always-review requirements stay binding however small the edit appears.
- **Note:** the 23 October latitude to settle routine review matters as REVIEWER-DECIDED was granted to Claude *as reviewer*. It does not pass to Claude as author. **Owner decision, 27 October 2026:** from the effective commit, the ChatGPT reviewer chat holds the same latitude Claude held as reviewer from 23 October, to be used carefully: it settles routine review matters itself and labels them REVIEWER-DECIDED (the 23 October examples: deferrability, packaging and versioning, wording, whether a re-review is needed, test-policy choices, and confirmations the owner has already relayed); consequential items still go to the owner. Expect REVIEWER-DECIDED labels in its reviews (H-2 section 3.1).
- **Owner instruction, 27 October 2026:** for the first three reviews under the new roles (the owner may change the number), Claude's response to each review lists every item the reviewer marked REVIEWER-DECIDED, checks each against the ratified compliance, safety and process rules (holdout and data boundaries, risk tiers and required reviews, test and evidence requirements, gates), and flags to the owner in plain English any that departs from them, naming the rule. This is reporting only: Claude does not overrule the reviewer or narrow its rights; the owner decides. **Since 28 October 2026 (owner decisions):** the instruction was first extended to six reviews and is now **extended indefinitely**, with **reporting by exception**. The reviewer still lists every REVIEWER-DECIDED item and Claude still checks every one, but Claude reports one to the owner only if Claude disagrees with it, or judges it of owner interest (for example a process deviation, a newly found gap, or a decision the owner must take). Reviewer rights are unchanged and the authority is not delegated. No departure has been found in any review so far.
- **Always independently reviewed before consequential execution or acceptance** (owner, 23 Oct; unchanged): process termination (kill logic, ownership, the switch); N-1 boundaries and leakage; fit seeds and canonical forecast identity; TOP/WORST readout, ties and selection; holdout access and unsealing; FINAL freezing, persistence and publication; the synthetic/real firewall; dependency upgrades (W-23). The agreed-position HIGH tier adds to this list; it never removes from it.
- **Review dispositions (owner-accepted 27 October 2026; `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`, committed at `b14116b`):** a finding that needs a change may also carry a disposition. **FIX AND PROCEED:** Claude makes exactly the correction the reviewer authorised, meets the reviewer's stated verification conditions and continues without a separate recheck of that correction. **RECHECK:** the corrected material goes back to the reviewer before acceptance. **RECHECK is the default** when the reviewer gives no disposition. Only the reviewer assigns a disposition, under its REVIEWER-DECIDED latitude; Claude may recommend one but never assigns, broadens or changes it; the owner may override. **Owner decision, 27 October 2026: FIX AND PROCEED never applies to code concerning any of the eight always-review subjects listed above, however small the change; such code always gets RECHECK.** Authority text and the register qualify for FIX AND PROCEED only for wording that changes no rule, status or authority; if in doubt, RECHECK. For every FIX AND PROCEED item, Claude keeps the exact before-and-after diff, the changed-file hashes, the reviewer's authorised wording and scope, the test commands and outputs, and a not-tested list, and shows the diff when the reviewer next looks at the package (procedure section 6). If the fix needs more than was authorised, differs from it, fails a test or reveals another issue, it becomes RECHECK. The procedure changes no risk tier, always-review subject, reviewer right (R-1..R-11) or owner gate.

### 1.6 Git and transport (agreed position section 7)

- You prepare exact candidate trees and patches in disposable workspaces; the owner applies, commits and pushes everything in the main tree. You never create remote pull requests or publish releases, and you push only `exchange/` records (next bullet).
- **Delivery method (owner decision, 27 October 2026; settles the transport question in agreed position section 11):** whole-file replacement through an overlay plus a read-only verifier: a `repo_overlay/` folder the owner copies onto the repository root, a `VERIFY_*.py` with `pre` / `post` / `committed` phases, and a `STAGE_EXACT_FILES.cmd`. The exact unified diff of every changed file always travels with the package as evidence. No hand edits to project files; any deletion is explicit, listed and checked by the verifier. Used for Package 2 (`c542483`), the integration (`ae76c29`), the transition (`d36735d`) and TH-1 (`744afea`). A `git diff --binary` patch is not used unless the owner decides otherwise.
- **Verifiers must tolerate CRLF working copies.** The owner's checkout uses `core.autocrlf`; Git stores LF. Compare working files after CRLF->LF normalisation (or with `git hash-object --path`), and compare committed files with `git show HEAD:<path>`. The first Package 2 verifier (inside `review/Predictive_Randomness_MultiGame_Package2_v0_11r1_OWNER_INSTALL_OVERLAY_v0_1.zip`) failed on CRLF working copies; the corrected `VERIFY_PACKAGE2_INSTALL_EOL_FIXED.py` (`1000017891e90f8dcbe7700afd68d5985b713d4a241c0e24df128e5276b98ac7`) was used for `c542483` but is not in the repository. The integration verifier `VERIFY_MR_INTEGRATION_INSTALL.py`, inside `review/MR_Integration_Install_v1r1.zip` (committed as history at the transition), is the current pattern; it uses `git --no-optional-locks` so that `git status` cannot rewrite `.git/index` (the reviewer's C-INSTALL-01). The latest example is `VERIFY_TH1_INSTALL.py` inside `review/TH1_Test_Hardening_v1r2.zip`, which also checks that guarded files are unchanged in Git.
- **Phone exchange protocol (`exchange/README.md` v0.3, commit `262a2c4`; owner, 28 October 2026).** When the owner relays from a phone, each message between the two AI chats is **one upload**: `EX_NNN_<Sender>.md`, or a flat `EX_NNN_<Sender>.zip` whose EX message has a `Contents:` line (no ZIP inside a ZIP). One shared, increasing `NNN` sequence; the next number is the highest in `exchange/` plus one; never reuse a number (a correction takes the next number and says `Supersedes:`). First line `# EX_NNN - <Sender> to <Recipient>`; header lines `Date`, `Project`, `Replies to`, optional `Supersedes`, `Contents` (ZIPs) and `Subject`; US-ASCII, CRLF; no personal names. **Claude records every EX file from both sides in `exchange/`, unchanged** (a ZIP also extracted to `exchange/EX_NNN_<Sender>/`), commits only there, gives the commit hash, and checks the pushed copy. Nothing in `exchange/` is ratified; only the owner moves material into the main tree. At the PC the owner may upload two files when a deliverable is itself a ZIP (EX_012 and its companion install ZIP).
- **Files shipped with CRLF** (the exchange rule) carry two hashes: as shipped, and after CRLF-to-LF conversion (the canonical identity of LF repository and package files). When an exchange file later goes into `review/`, store an **LF copy** and cite the LF hash: the owner's Git uses `core.autocrlf=true` and converts CRLF at commit, which would make a committed-phase check fail. The CRLF originals stay in `exchange/`.
- **Install order (the reviewer's N1I-C01, 28 October 2026):** commit, run `--phase committed`, and push **only after `COMMITTED PASS`**; on a STOP the commit is still local and `git reset --hard HEAD~1` removes it. Begin every install with `git pull --ff-only` (exchange records may have moved `main` on) and a clean `git status --short`. While the owner installs, Claude pushes nothing. After the push, Claude verifies from GitHub and, where specified, runs an immediate recovery check (`git revert` in a disposable clone).
- **Already-committed files:** if a file a package would add is already committed (byte-identical), the verifier treats it as guarded, not new, and the builder asserts the byte identity first (NAMES-1, section 7.1B).
- Test every verifier in two scratch clones before delivery: one plain LF, one with `core.autocrlf=true` and CRLF working files. Include negative tests (a tampered file, an extra file, a changed predecessor).
- After the owner pushes, verify independently: clone fresh, check the commit's file list (`git diff --name-status HEAD~1 HEAD`), every blob's SHA-256, modes, and that nothing else changed.

---

## 2. How the owner wants work presented (follow strictly)

- **Lead the owner through next steps.** Say what happens next, who does it, and label every paste block with its **destination chat** ("for the ChatGPT reviewer chat"). The owner relays by copy-paste and file upload, and once was confused about which chat a block was for.
- End every handback that goes to the reviewer with a short **paste-ready block** (a fenced `text` block). The owner likes these small pastes. **When the owner is on a phone, the EX file replaces the paste block** (section 1.6); hashes in any block are computed by a tool and copied, never retyped (section 8.6).
- **Decisions:** plain-English question / why / recommendation / options. Several decisions: one at a time, a recommendation each. Document references on a trailing line.
- **Verify, don't assert.** Check claims against the files, line numbers, library source or official documentation. Label evidence VERIFIED / OWNER-REPORTED / UNVERIFIED (or TO-TEST for Windows-only behaviour).
- **Plain English**, not acronym-dense text. Separate BLOCKER / CORRECTION / OPTIONAL; concentrate on substance.
- **Files Claude produces:** strict US-ASCII; CRLF for documents the owner reads, LF where the file joins a ratified LF text (the integration editions kept the ratified texts' UTF-8 with LF so protected blocks stayed byte-identical); the version in the file name; no owner name. Check the encoding mechanically after writing. Send files as files, with a one-line summary and the paste block in chat.
- **Superseded versions are kept**, not overwritten. Do not make revisions only to update version mentions. A mention of a versioned document means that version or later, except in records of past events.
- **Process discipline:** propose before transforming; the owner ratifies. The owner's priority is **getting the project running**, not measuring the role change.
- **Package sizing (owner-confirmed 27 October 2026):** small packages for complex or HIGH work; a lead item that proves the pattern before a batch of similar items (for example, one lead method per family); heavy methods one at a time; ensembles last.
- Owner's philosophy, binding (section 2A): the reference model is a measuring ruler, never a veto.

### 2A. The owner's foundational points (26 Oct; binding)

1. The project is **deliberately and extremely speculative**. It looks for patterns that conventional statistics may have missed. No idea, method or measure is excluded because conventional statistics says it cannot work.
2. The owner **expects the most likely outcome to be that no method works**. A carefully measured null result is valid and useful.
3. **"Mark, never suppress":** every number the owner asks for is computed and shown; where it is not a calibrated probability, it carries a plain label saying so.
4. **Statistics tells kinds of pattern apart; it is never a gate.** The four origins: PO-1 a consequence of the method; PO-2 an effect of fitting; PO-3 chance, multiplicity or selection; PO-4 persistence on genuinely new draws. Strict N-1, the sealed holdout and the walk-forward / in-sample separation exist so that any surprise can be tested honestly.
5. **Openness with discipline:** any idea may be explored, but a claim needs a definable, testable form.
6. **Design test for any proposal:** does it make a number more honest without making any idea, method or measure ineligible? If it would act as a veto, flag it against this philosophy.
7. **Plain language in outputs:** terms such as "walk-forward" and "in-sample" are always printed with their exact project meaning.

---

## 3. Project in one paragraph

Two games, never pooled, one game per run. **Powerball:** current format since Draw 1144, 19 April 2018; 7 distinct main numbers from 1-35 plus 1 Powerball from 1-20. **Oz Lotto:** current era since Draw 1474, 17 May 2022; 7 from 1-47 and no Powerball barrel; its 3 supplementaries never enter any method view, fit, seed, digest or prediction, and **the evaluator alone** may read a target's supplementaries, after the target is opened and its forecast frozen, solely to classify prize divisions (R2 v0.5 section 2.5). The project builds a Python research system on Windows 11 (the project venv is Python 3.15.2 since 28 October 2026; previously 3.14) that tests whether past draws hold any predictive structure, using 62 permanently registered methods, E_1-E_62 (room up to E_106, no quota; E_63 is not registered). Each method produces full rankings and publishes TOP and WORST predictions side by side. Real weekly forecasting starts only after modelling is complete: train on all eligible draws before the target, predict, freeze and push before the draw, score afterwards, append the draw, repeat. Method rankings (league tables) are reports per R3 section 17; they never feed forecasts.

---

## 4. Governing documents (after the integration install)

All in `doc/`. SHA-256 values are of Git blobs (UTF-8, LF), checked with `git show HEAD:<path> | sha256sum`.

| Document | SHA-256 | Governs |
|---|---|---|
| `Predictive_Randomness_Research_Project_Proposal_v0_6.md` | `6a281e05127e7db976a16557ba69006327a8d615c2b0ec90bb6b34ee1c648a73` | Charter and philosophy; A-01..A-37, D1-D5; section 2.7 rankings charter; E_1-E_6 definitions |
| `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` | `19809ae8a1aca716c6c6a4de71a37b705129304894a2b382036d51b76575b99f` | The E_1-E_62 catalogue (unchanged) |
| `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_5.md` | `2c67db8fcba50e469b0490cd85caf2fe964b3b79fc17fe7da4ebf033b91d9a3e` | Data, views, N-1, method contracts; 2.5 supplementary rule; 3.6 numbering; 5.5 E_1 goldens; **5.6 stage-1 contract fields (E_2 readiness)**; 8.4 in-sample mode; T-01..T-39 |
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md` | `53e30a3e649b48b8a88923d08bf578caf04a4ce93d6ea6468891ca97e93a57b6` | Evaluation, TOP/WORST, rank position, holdout, freeze-to-score; **section 17 method ranking measures** (MRD-01..24, RK-1..6, PO-1..4, MR0-MR16, MRT-01..25, MRO-01..11; 17.13 phasing) |
| `Predictive_Randomness_Software_Architecture_Discussion_v0_8.md` | `32cf157d9ce8850e790274e962236f2be3b50a8bdee7ec94a28ba00d7fd452ec` | Wrappers, coordinator, 5A.2 installer, 5A.4 ranking tool launcher, **5C process safety (protected)**, 12.5 report tool, W-01..W-25, A-01..A-26, O-register, 20A |
| `Predictive_Randomness_MultiGame_Infrastructure_P3_Task_Specification_v0_2.md` | `2f3ac0e82dfd159025c3933ba41e812a4af0254da13e56664ed36dd5c5dcb61c` | Package 2 work W1-W6; invariants M-INV-01..07 (Package 2 is now installed) |
| `contracts/TIE_SHA256_V1_Ratified_Encoding_v0_2.md` | `045b784d16a4611ac4ba5e8af063733e957b0b9359882d52b7143b912a65a0b6` | Tie and seed encoding |
| `HOLDOUT_EXPOSURE_RECORD_v0_2.md` | `aec833fe031b6d1d73e6acbb81757b50b193425a6899c84d438431d9df4433e2` | Factual, value-free exposure record (6 items) |
| `NUMERICAL_INTEGRITY_AND_RETRAINING_REFERENCE_v0_1.md` | `51bcc84bc2ce4c2eda9c99008e75817f85e3f17ef12fc6639c1be6fd0ac3108d` | Non-normative precision guidance |
| `Predictive_Randomness_Windows_POC_Implementation_Task_Specification_v0_2.md` | `ca5e89dde7e9927974e759f1df115eefca03144de45e073c240aa9e13f24ebf1` | P0-P2 history, subject to Architecture 5C |
| `RATIFICATION_REGISTER_v0_8.md` | `3f217c6875d443a0cc1bba2f6c329b1fda455fb4a97bf7fe06090394736fffcf` | Lineage and status after NAMES-1 (installed at `52ebeaa`); superseded by v0.9 when that is ratified and installed |
| `Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md` | `0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954` | **E2R-1** (ratified 28 Oct 2026): the stage-1 method-generic contract schema and acceptance list; owner decisions D-1..D-11 (its section 14); source-tree, retirement and release policy (its section 12A) |
| `Predictive_Randomness_NAMES1_Rename_Specification_v0_2.md` | `07bda3e4a8a99bfc611a76cec672f8642532186567737e1a23de5e5701489e5a` | **NAMES-1** (ratified 28 Oct 2026; installed at `52ebeaa`): the one-off rename to stable file names; OPEN-N1..N3 decided (register v0.8) |
| `Predictive_Randomness_E1_ALIGN_Specification_v0_2r1.md` | `d9ffd900c74d8a0cc5002bb78c83121f818514cd88ca9150bada8d6d1fa6653a` | **E1-ALIGN** (design ratified 28 Oct 2026, with E1A-D1..D3; code not yet authorised): E_1 into the per-method layout; the symbol-aware firewall |
| `Predictive_Randomness_Method_Ranking_Measures_Proposal_v0_5.md` | `c6ca2cb2174ee2963a6fe33347820c80b92e6dd1eda518a1f0c8e3254d67ab19` | Ratified 26 Oct; now integrated history, kept unchanged |

**Register v0.9, installed with this file, supersedes v0.8.** A register cannot contain its own hash; v0.9's is in that installation's manifest. Registers v0.4-v0.8 are history. Use whichever edition is current.

**Historical, kept, not operative:** Proposal v0.3-v0.5; R2 v0.3 and its errata files, R2 v0.4; R3 v0.1-v0.4; Architecture v0.2-v0.7; P3 v0.1; register v0.2-v0.8; TIE v0.1; exposure v0.1; MR proposal v0.2-v0.4; `doc/experiments/P3_E1_..._REVIEW_CANDIDATE.md`.

**Old headers:** a ratified file whose authoring-time header still says "candidate" keeps that header; the register's later record decides its status. Never edit a ratified file in place (the one agreed exception was the integration install's status edits, defined in register v0.4 and reviewed).

**Protected blocks (byte-identical through every consolidation; never edit casually):** Architecture 5C; R2 section 7 (method inventory) and 4.1; R3 0.4, 2.4 and 3; Proposal E_1-E_6.

**Known out-of-date statements left unedited at the integration install** (they describe other events; register v0.5 records the corrections, and the ratified files are not edited): the Package 2 "pending" or "outstanding" lines (R3 0.1 Package 2 row; Architecture section 0 "Current runtime task"; Proposal section 0 "Current execution boundary" and "Document classification"; Proposal A-18); the "ChatGPT implements, Claude reviews" role lines (Proposal section 0 and A-29). (Register v0.5 itself updated its own "Change discipline" and "Continuity documents" lines.) The register is authoritative on these; fold them into the next editions when those are next revised for another reason.

**R1 method families:** E_1-E_6 originals; E_7-E_16 frequency/Bayesian/regime; E_17-E_22 recurrence; E_23-E_32 within-draw/drawn order; E_33-E_40 spectral/curve; E_41-E_48 information/nonlinear; E_49-E_54 ML/external (E_54 uses date covariates); E_55-E_56 ensembles; E_57-E_62 pilot-wave-inspired mathematics. E_14 and E_54 use dates. E_1 is "historical appearance frequency", not a pilot-wave method.

---

## 5. Settled decisions - do not reopen without substantive cause

Reviewer handover v10 section 5 holds the full list with its history; the governing documents hold the rules. The essentials:

### 5.1 Data and holdout

- **Quarantine from 2026-08-01.** Powerball >= 1577 and Oz Lotto >= 1694 are quarantined. Development data: Powerball 1144-1576 (433 draws), Oz Lotto 1474-1693 (220). Development targets never exceed 1576 / 1693; walk-forward windows (Powerball 1145-1576, Oz 1475-1693) are maxima pending preregistration (OPEN).
- **FINAL_HOLDOUT_10:** Powerball 1577-1586, Oz Lotto 1694-1703.
- **E_1 exception:** the target-1577 regression is forecast-only, trained on 1144-1576; the 1577 outcome is never read, scored or counted as a holdout result.
- **Drawn order:** the published sequence is assumed operator order, label `OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`; never verified physical order; set and order views of the same rows are not independent samples.
- **Source:** Lotterywest's own results-search page on `www.lotterywest.wa.gov.au`, read by an honest, unmodified headless browser with >= 2 s pauses. **No API of any site; no browser impersonation; no bot-protection bypass; `oz.lotterywest.com` is never contacted; no new scraper by any AI.** The Lott is used only through pages the owner saves by hand outside the repository, as a private verifier; nothing derived from it is committed; **no automation of The Lott, ever**.
- **No lottery-results searches** by any project session, author or reviewer (agreed position 8.1). Accidental exposure is reported factually for the exposure record, never suppressed or asserted harmless.
- **One master per game:** `source_data/<GAME>_results_master.csv` with its append-only ledger, value-free INIT record and create-only `backups/` and `grabs/`. Every run pins the master version and SHA from the ledger. `.gitattributes` has `source_data/** -text`; never change it.
- **The owner will not run `results_master update`**, even to test; it is gated by `HOLDOUT_OPENED_<GAME>.json`, which is not authorised.
- **Dates only** in masters (ISO dates; no invented times or zones). No pre-April-2018 draws, including Powerball-only analyses.
- **Exposure record v0.2 (six items, value-free):** never repeat the values it refers to; disclose rather than re-seal; make no claim about influence. When diffing documents containing the R1 draw-1587 paragraph, filter it out first.

### 5.2 Scientific contract

- **Strict N-1:** target N sees only eligible draws with `draw_number < N`. **T-05:** change N and every later row; every method-visible field, array byte, schema, digest and capability must be identical, and the forecast byte-identical. Orchestration-side provenance may differ; provenance handed to a method must not.
- **The B1 rule (agreed position 8.2):** the whole-master SHA-256 is derived from target-and-later rows. It is orchestration-only provenance and never reaches a method, directly or inside any method-facing object. The same holds for whole-file size or any other suffix-derived metadata (ADD-2 section 2 item 1).
- **Seeds and content identity** come from the permitted training-view digest, never the whole-file hash.
- **Views:** `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER`, `PAIRED_DIAGNOSTIC`; caller-declared; paired views never double-count. New schemas bind `game_id`, era and profile version (the legacy `E1_REAL_U_TRAINING_VIEW_V1` alone is exempt). Dates are opt-in (`include_dates=False`) with their own schema and digest.
- **Numerics:** `int64` for every integer field and `float64` for floats, in the reader's table and every returned view; views are byte-backed, own their prefix-only copies, read-only, with no `.base` path to later rows (test `47*47 == 2209`). Python `int` for exact counts beyond int64. A wide dtype is not proof of correctness.
- **Fresh fit for every target** on the eligible prefix; an incremental cache needs a reviewed byte-identical comparison with from-scratch fitting.
- **TOP and WORST from one frozen ranking;** joint-set TOP gets WORST only through `INVERSE_FROM_MARGINALS`, otherwise `INVERSE_UNAVAILABLE`, never fabricated.
- **Prediction-time ties:** `TIE_SHA256_V1` only. Post-draw rank position uses mid-ranks and never alters a frozen forecast.
- **Status vocabularies stay separate:** benchmark (R2-C20) `SUCCESS`, `TIMEOUT`, `ERROR`, `INSUFFICIENT_HISTORY`, `BLOCKED_DEPENDENCY`, `NUMERIC_INVALID`; evaluation (R3) `RUNTIME_FAILURE`, `INSUFFICIENT_HISTORY`, `DIAGNOSTIC_ONLY`, `NOT_IMPLEMENTED`, `INVERSE_UNAVAILABLE`, `PREDICTION_AVAILABLE`; per-game registry `SUPPORTED` / `FORMULA_OPEN` / `UNSUPPORTED_FOR_GAME` with a structural reason. Oz has no Powerball barrel; never zero-pad one.
- **Synthetic firewall:** synthetic data, states and scores never enter real fits, predictions or scores, and never exclude a method.
- **Method rankings (R3 section 17):** reports only; walk-forward (WF) and in-sample (IS) never ranked together but shown side by side with separate ranks and a "hindsight advantage" column; IS labelled `IS_NOT_CALIBRATED` and never on the scientific allowlist; any ranking-driven selection is a separately registered meta-method using past WF scores only. One programme-wide search log, `results/audit/SEARCH_LOG.csv`, with `row_type`; each ranking report run appends exactly one `RANKING_REPORT` row. Bonferroni over predeclared families; no Sidak. Calibration labels as in R3 section 17.

### 5.3 Multi-game

- Profiles are a frozen Python module with no free-form barrel parameters (M-INV-06). Identity is (`game_id`, `draw_number`); `draw_key` is display-only. Derived weekly date = era start + 7 x (N - first draw); a source/derived date mismatch halts date-using methods for that game only.
- Separate namespaces per game; no cross-game pooling or covariates without a preregistered, owner-approved design. **No Oz Lotto method execution is authorised.**
- **A method-generic runtime contract replaces the E_1-specific conventions before E_2** (Architecture 20A; R2 5.6 stage-1 fields). Its design is **E2R-1 v0.3r3, owner-ratified 28 October 2026**; its code is the E_2-readiness package (section 9). The owner decisions recorded in its section 14:
  - D-1: `track_id` excludes the method revision; each report uses one declared revision per track.
  - D-2: synthetic and benchmark records carry the evidence tier `NOT_EVIDENCE`.
  - D-3: plain-English method texts for E_1 and E_2 are written in the E_2-readiness package.
  - D-4: `src/` holds current code only, with stable names (no version in file names), and a folder per method, `src/methods/E_<nnn>/`, which is a locator only; the scientific identity stays `E_n`.
  - D-5: a superseded revision moves to `archive/methods/E_<nnn>/r<k>/` (helpers to `archive/common/<name>/r<k>/`) with a README; no commit IDs, no stored hashes, no run-time code-identity recording; exact historical replay is not promised.
  - D-6: a method runs only if its active registry entry is `SUPPORTED` for its current revision **and** no `IN_DEVELOPMENT.txt` is present; release is the owner's two deliberate actions. Not yet implemented: it arrives with the E_2-readiness code.
  - D-7: NAMES-1 before the E_2-readiness code (now with E1-ALIGN between them; E1A-D2).
  - D-8: prospective results are shown both "as published" and "current methods".
  - D-9 to D-11: a seed policy's root is a pre-announced NIST Randomness Beacon pulse, fetched once by hand and verified; runs never fetch; roots may be switched as a new revision or variant, and every root tried is logged and counted; a root published after historical targets may be used for retrospective development runs, labelled as experiment randomisation, but a real forecast needs an already-approved root. **Carried forward to the seed-policy package:** keep a dated copy of each pulse-selection rule; reject any beacon response for a different pulse.
- **Layout (OPEN-N1 = A, owner 28 October 2026):** each method's entry file stays directly in `src/methods/` (`E_<nnn>_<Name>.py`), as the Option F wrapper requires; its folder `src/methods/E_<nnn>/` holds its method-specific modules and its `IN_DEVELOPMENT.txt` flag, created when its code first arrives. OPEN-N2: the owner's data tools and legacy test scripts keep their names for now. OPEN-N3: the stable test names of NAMES-1 section 3.
- **E1-ALIGN (design ratified 28 October 2026):** moves `canonical_bytes` and the length-prefixed tuple encoding into `_common/canonical_encoding.py` (so the shared reader no longer imports E_1 code) and E_1's five modules into `src/methods/E_001/`; keeps E_1's tie code with E_1; widens the import firewall to method folders with exact, counted, symbol-aware allowances; adds a six-encoder byte-equality guard. E1A-D1: E_1 stays revision 1 under its own structural exception; E1A-D2: NAMES-1, then E1-ALIGN, then the E_2-readiness code; E1A-D3: E_001's entry-file exemption is kept.

### 5.4 Engineering and process safety

- **Architecture 2:** one standalone `.py` entry file per method (`src/methods/E_###_name.py`), with its method-specific modules in its folder (layout above), shared reviewed `_common/` modules (no shared process or mutable state), a small coordinator.
- **Option F, the single launch interface:** `Run_Coordinator.bat` -> Python coordinator -> `Run_Experiment.bat` per experiment -> method `.py`; manual: `Run_Experiment.bat` -> method. No second production launcher. ERR-R2-02 / Option F has provisional production acceptance until owner-run P1/P2 gates pass.
- **Wrappers:** venv checks; scoped activation; `SETLOCAL`/`ENDLOCAL`; explicit `.venv\Scripts\python.exe`; `%*` forwarding, never rebuilt from `%1..%9`; AutoRun checked in the registry (no `/D /C`); `SAFE_ARG`. The coordinator refuses to start unless `VIRTUAL_ENV` and `sys.prefix` match the project `.venv`. `.bat` files are stored with CRLF (`.gitattributes`).
- **Concurrency:** 1-6 workers, default 6; one BLAS thread per worker; no nested pools.
- **Dependencies:** `install_upgrade_dependencies_into_venv.bat` is the sole package list; default INSTALL+UPGRADE (owner's choice). **After every upgrade, stop** until the offline suites, numerical and N-1 tests, the W-suite including W-23 and all E_1 goldens pass; goldens are never recalibrated. No upgrade between freezing and scoring, or within Mode H. Never invoke the installer as part of an offline test. **Python (owner, 28 October 2026):** the venv went from 3.14.8 to 3.14.10 (`venv --upgrade`; no package changed), then to a new **3.15.2** venv (`py -3.15 -m venv .venv`; every package a ready-built wheel; versions as in section 7.1). The 3.14.10 venv is kept as `venv.bak` (Git ignores `venv.bak/`, but not names such as `.venv314`), with Python 3.14 installed, as the fallback; the free-threaded 3.14t was removed. The owner's data tools have not yet been run under 3.15; treat their first run as a first run.
- **Timing (owner-decided 24 Oct):** `POLL_SECONDS_DEFAULT/MIN/MAX` = 1.0/0.5/5.0; `PIPE_EOF_WAIT_SECONDS` 5.0; `RELEASE_POLL_SECONDS` 0.5 (= `POLL_SECONDS_MIN`, tested); `RELEASE_WAIT_SECONDS` 15; one blocking `messages.get(timeout=...)` helper; capture throttle = poll interval; line-buffered logs. The protected 3 s termination waits stay.
- **Process termination (Architecture 5C, protected):** psutil only; no Job Objects; no `taskkill`, no kill by name, no fresh PID lookup. Ownership is proved by ancestry captured while the wrapper root is alive (PID plus creation time); kill only retained `psutil.Process` members and the root via its `Popen` handle. **Strict no-status/no-kill:** the status file can only block. When uncertain, leave the process and report `UNVERIFIED` / `ORPHAN_SUSPECTED`.
- **Orphan marker rule (owner, binding):** if anything is unconfirmed, the coordinator publishes the no-overwrite, fsynced `transitory_data/poc_runs/UNRESOLVED_ORPHAN.json`. **Any entry at that path blocks all launches for both games. Only the owner's approved manual clearance procedure clears it. No chat ever clears, bypasses or suggests bypassing it.** A past clearance is not proof that no marker exists now.
- **Failed-group firewall:** results of FAIL or orphan-suspected groups are never consumed, even if `canonical_result.json` exists. A method cannot issue its own coordinator receipt.
- **The three switches stay False:** `ENABLE_PROCESS_TERMINATION`, `ENABLE_SCIENTIFIC_COORDINATION`, `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE`. No CLI override. Only the owner flips them, after reviewed tests. The scientific result-consumer allowlist `_COORDINATED_SCIENCE_ALLOWLIST` is empty.
- **No-clobber publishing:** `os.rename` for frozen results (raises on Windows if the target exists); never `os.replace` for frozen output.
- **Testing order:** non-destructive tests first; destructive tests one at a time, each separately approved.

---

## 6. Verified technical facts (reuse rather than re-derive)

Reviewer handover v10 section 6 lists them with sources. The ones that bind code design:

- The Windows venv `python.exe` is a redirector (CPython `PC/venvlauncher.c`): `Popen.pid` is not the interpreter's PID.
- Windows does not kill children when the parent dies; `TerminateProcess` is asynchronous.
- A `.bat` launched via `Popen` runs under `cmd.exe` with CMD argument parsing (gh-114539): hence `SAFE_ARG` and `%*`.
- The `Run_Experiment.bat` process tree is root `cmd.exe`, a pipe child `cmd.exe` plus `findstr.exe`, a pre-check redirector plus interpreter, then the experiment's redirector plus interpreter. The allow-list is `cmd.exe`, `findstr.exe`, `python.exe`.
- psutil 7.2.2: `children(recursive=True)` filters by creation time against the root only (hence the per-edge check); `kill()`/`terminate()` check PID reuse; `Process.wait()` on Windows has no reuse check.
- `O_NOFOLLOW` does not exist on Windows; the reader's symlink refusal there relies on `is_symlink()`. **NTFS hard links (OWNER-REPORTED, 27 October 2026, Windows 11, Python 3.14.8):** the reader's refusal of a hard-linked master (`st_nlink != 1`) ran and passed in the offline suite on the owner's NTFS drive. Symlink refusal on Windows is still TO-TEST: the owner's account cannot create symlinks (WinError 1314), so those subtests skip there.
- Line endings: Git stores `.md` and `.py` as LF; `.bat` is `text eol=crlf`; `source_data/**` is `-text`. `git archive` applies the `.bat` rule, so a `.bat` file's archived bytes are CRLF while its Git blob is LF: hash `.bat` files from `git show`. The owner's checkout uses `core.autocrlf=true` (Git warns "LF will be replaced by CRLF" when staging); it converts CRLF text to LF at commit.
- **Python 3.15 makes UTF-8 the default text encoding (PEP 686).** The project's text reads without an explicit encoding only touch ASCII JSON and CSV test data; all 79 tests pass on 3.15.2 (OWNER-REPORTED, 28 October 2026). The committed static firewall test reads method files with an explicit `utf-8`.
- **Reference figures** (fair-draw model, context only, never a veto): Powerball main matches mean 1.4, SD 0.9604; P(>=4) = 0.01826; P(>=5) = 0.00121; Powerball 0.05 per draw. Oz Lotto main-match mean 49/47.

---

## 7. Implementation status at the baseline

### 7.1 Package 2 v0.11-r1 - ACCEPTED and COMMITTED at `c542483`

- Reviewed inputs: parent v0.11 `0e00e231c46dafd01df52fb6f50db6ceaf399ea27be40efb318529101611d74c`, r1 `7bddda746f56668fbc60af9826cee83c7fd95031dfd3c9b4b474641cc2734635`. Claude's review `review/Claude_Review_Package2_v0_11r1_v1.zip` (`5c2e84655dcfd1d3a24129c0d38a5996e2f14195e807def382ba2bdb7d545a29`): PASS, 0 BLOCKER, 0 CORRECTION, 3 OPTIONAL. Evidence: 58 tests OK, 1 skip; 11/11 protected ASTs; ratified goldens; independent T-05 probe 96/96 on the real development masters (the probe is in that ZIP; reuse it as a pattern).
- Install commit `c542483`: 27 files (2 modified, 25 added), all 27 blobs matching the reviewed bytes, all files mode 100644, switches False, allowlist empty. Coordinator SHA `bc8380b5f20a704c0f47d5f76eeb86156237142b5639e5b9770b8314db3bb822`; reader `game_draws_reader_v1.py` SHA `e06e0cca7edc298aadf5298ae860d6093467f6460fcbf9839928b1e4fdb342b5`.
- Factual record: `doc/HANDOVER/Package2_v0_11r1_Acceptance_Deferred_Work_v0_1.md`. **Erratum (recorded in H-3):** its "Accepted Package 2 code" section names `EXPECTED_SOURCE_SHA256.json`; the actual file is `evidence/CLAUDE_EXPECTED_26_FILE_SHA256.txt` in the install overlay.

**Module map** (from ADD-2 section 1, with the stable names NAMES-1 gave at `52ebeaa`; NAMES-1 section 3 maps old to new; read the code itself before changing it):

| Path | Responsibility |
|---|---|
| `src/methods/_common/game_profiles.py` | Frozen Powerball and Oz Lotto era profiles and capabilities |
| `src/methods/_common/game_draws_reader.py` | Orchestration-owned version/ledger/INIT verification, raw first-field cutoff, prefix-only conversion, byte-backed immutable `DrawView`, opt-in dates, schema and digest. **Highest isolation sensitivity.** `order_evidence` holds only the INIT record name and the status label |
| `src/methods/_common/e1_common_reader_bridge.py`, `multigame_e1.py` | Legacy E_1 bridge and generic E_1 launcher path; preserve the E_1 digest, tie encoding and goldens |
| `src/methods/_common/multigame_method_registry.py`, `multigame_standalone_contract.py`, `multigame_coordinated_manifest.py` | Method/game capability identity, run manifests, standalone contracts |
| `src/methods/_common/multigame_console_protocol.py`, `multigame_worker_launch_handshake.py` | Console and launch handshake, identity checks |
| `src/methods/_common/multigame_ancestry_release.py`, `src/coordinator_private/multigame_coordinator_exit_receipt.py` | Ancestry release and the coordinator-only, fail-closed receipt |
| `src/Powerball_Experiment_Coordinator.py`, `src/coordinator_private/multigame_launch_spec.py` | The coordinator; 11 protected functions AST-identical to v0.6 (`2e23d550...`) |
| `src/coordinator_private/multigame_windows_lifecycle.py` | Windows synthetic lifecycle; gate False; **never run; needs a full review before any gate** |
| `src/methods/_common/multigame_synthetic_scorer.py`, `multigame_result_registry.py`, `src/methods/POC_MultiGame_Synthetic_Worker.py` | Synthetic-only scoring, the result registry/firewall and the probe worker |

**The eleven protected coordinator functions:** `accept_ancestry_candidate`, `check_exited_worker_for_orphan`, `departed_members_check`, `read_status`, `record_unresolved_orphan`, `register_root`, `require_no_unresolved_orphan`, `save_new`, `status_and_result`, `status_orphan_evidence`, `terminate_owned_tree`. Kit script 05 checks them against committed v0.6.

**Offline suite commands** (from the repository root, Linux shell form; Windows uses `;` in `PYTHONPATH`). The 60-test standard suite:
`PYTHONPATH=src:src/methods:tests python -m unittest -v tests.test_multigame_reader_contracts tests.test_multigame_static_and_timing tests.test_multigame_launch_and_manifest tests.test_multigame_exit_receipt tests.test_multigame_science_allowlist tests.test_multigame_console_and_synthetic_scorer tests.test_t05_hardening`
The other 19 current tests: `PYTHONPATH=src:src/methods:tests python -m unittest -v tests.test_e1_standalone tests.test_multigame_windows_lifecycle_review`. Both are offline; the lifecycle-review module never starts a Windows process, and the E_1 standalone module uses invented CSVs in temporary folders. The NAMES-1 package's `RUN_NAMES1_SUITE.py` (in `exchange/EX_012_Claude/NAMES1_Code_Install_v1.zip`) runs all nine modules one by one and compares each with its expected count.
Windows CMD form: `set PYTHONPATH=src;src\methods;tests`, then the same `python -m unittest ...` line, then `set PYTHONPATH=`.
Result at `c542483` (six modules): 58 OK, 1 skip. At `52ebeaa` (all 79 current tests): Linux (Claude; Python 3.13.17, NumPy 2.5.3) 79 OK, 0 skipped; Windows (owner-reported, 28 October 2026) 79 OK on Python 3.14.10 and again on Python 3.15.2 (NumPy 2.5.4, SciPy 1.18.1, psutil 7.2.2), each with 2 skips: the reader-contracts symlink subtest and the exit-receipt symlink test, because the account cannot create symlinks (the hard-link subtest runs). Read every test before running it; its name or an "offline" label is not proof that it is safe (agreed position 8.2).

**Deferred, not discarded:**
- **P2-R1-O1 and P2-R1-O3: done** in TH-1 at `744afea` (section 7.1A).
- Older optionals still open: resolved-path containment under `source_data`; a full review of `multigame_windows_lifecycle.py` before any lifecycle gate.
- **A known gap (found in review, 28 October 2026; register v0.8):** the committed static import-firewall test (`test_method_loader_import_firewall_except_accepted_legacy_e1`) reads only the module part of `from X import Y`, so a method file using `from _common import game_draws_reader` would pass it. No current method uses that form. E1-ALIGN closes it; until then, Claude's review of every code package checks for that form by hand. NTFS `st_nlink` handling is now owner-evidenced (section 6).

**Not tested by anyone:** Windows wrappers, venv activation and exit flow, NTFS symlink semantics, console Ctrl+C and timeouts, process lifetimes and decoys, the synthetic Windows lifecycle, P1/P2 destructive probes, the owner's Windows dependency suite, Python 3.15 beyond the offline suite (the owner ran all 79 tests on 3.15.2 at `52ebeaa`; Claude runs 3.13), the owner's data tools under 3.15, real scientific scoring, Mode H, FINAL, online acquisition, any gate-enabled coordination. The `DrawView` split is reviewed discipline, not OS sandboxing.

### 7.1A TH-1 offline test hardening - ACCEPTED and COMMITTED at `744afea`

- **Scope:** tests only; it closes the deferred Package 2 items P2-R1-O1 and P2-R1-O3. Installed at `744afea085c9fabc62c18ee5c18ee400d0853a9d` (verified by Claude: exactly 5 paths, 3 added and 2 modified, every blob matching the reviewed bytes; all 290 files mode 100644; switches False; allowlist empty). The coordinator (`bc8380b5...b822`) and the reader (`e06e0cca...42b5`) are unchanged.

| Path | Change | Git-content SHA-256 |
|---|---|---|
| `tests/test_p2_r1_t05_hardening_v1.py` | added | `c3341ce2fa7409335f6232c0f65b2d9b5a1b2d03fde6ee863e4fe4e30c8b9e58` |
| `tests/fixtures/coordinator_v0_6_baseline/Powerball_Experiment_Coordinator_v0_6.py.txt` | added (the committed v0.6 coordinator from `d09d669`; the AST anchor) | `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b` |
| `tests/test_multigame_v011_static_and_timing.py` | modified | `8e606e965f748cb7b48f3ba8f76b29dfecf71552f59c4b3292cc76f42ab43696` |
| `tests/test_multigame_v011_reader_contracts.py` | modified | `a0460c49ac5d193871dd35f02ba532271e9c943185b8a9b759f0ee5b4a0da2dc` |
| `review/Claude_Verification_Transition_Commit_d36735d_v1.md` | added (history record) | `c76b3bb305fca61bec0b791e6d792bc5b33f46529df0222498cbc5669a9343a0` |

- **What the tests add:** T-05 at four development targets per game (first + 2, midway, last - 1, last), for each view kind, with and without dates, using invented masters in which the rows at and after N are rewritten twice at the same file length and once longer. A second test proves every rewritten row is itself a valid row. The 11-function AST check now reads a hash-pinned copy of the committed v0.6 coordinator and never skips. The reader's symlink and hard-link checks are separate subtests, so a missing symlink privilege skips only the symlink part.
- **Reviews:** `review/Independent_ChatGPT_Review_TH1_Test_Hardening_v1r1.md` (the link-test change passed; CORRECTION TH1-C01: the v1 "longer" rows were padded in a way that made them invalid; OPTIONAL TH1-O01, a count) and `review/Independent_ChatGPT_Focused_Recheck_TH1_Test_Hardening_v1r2.md` (PASS). Installed package `review/TH1_Test_Hardening_v1r2.zip` (`47d6e5a67eb60b045c9b3c1b0930f0ced2ad082cee47dbdd93caaa74196c3015`); v1 and v1r1 are kept beside it as history (commit `151f393`).
- **Author mutation checks** (disposable copies only): 11 mutants, all caught - the whole-file length, a truncated whole-file hash, the whole-master SHA and the last 60 file bytes each put into `order_evidence`; the prefix cut off by one; a change inside protected `terminate_owned_tree`; a tampered fixture; a missing fixture; the reader accepting hard links; the reader following symlinks; an invalid suffix row.

### 7.1B NAMES-1 - ACCEPTED and COMMITTED at `52ebeaa`

- **Scope:** the one-off rename of 27 versioned files (18 runtime modules, 9 current test modules) to stable names, with exactly the 94 allowlisted substitutions in 27 files (82 imports, 2 `mock.patch` targets, 7 file-name literals, 2 negative firewall literals, 1 docstring; `review/NAMES1_Code_Install_v1/names1_allowlist.tsv`). No behaviour, schema, identity or golden changed; E_1 stays revision 1 (N1-R03). The eleven protected coordinator functions are AST-identical to v0.6.
- **One visible record effect (N1-R01B):** a coordinator exit receipt keys `contract_modules_sha256` by the two contract files' names, so a receipt issued before NAMES-1 no longer verifies and is refused; none is converted or bypassed.
- **Installed** in one commit with the NAMES-1 v0.2 specification, the E1-ALIGN v0.2r1 specification, register v0.8 and the review history. The verifier pinned base `908db9e`; it treated six history files the owner had committed early (`2c76664`) as guarded. Owner's Windows run (Python 3.14.10): PRE, 27 renames, 42 files copied, POST, 79 tests (2 symlink skips), 63 import-origin and firewall checks, staging (27 R, 3 M, 15 A), COMMITTED PASS before push. A first attempt stopped at PRE (three downloads saved under `review/`) and was undone and restarted cleanly. Claude verified from GitHub: COMMITTED PASS; 42 A, 27 D, 3 M without rename detection; manifest `9d8664f38c33ee374ace06d29d98a4d84477af9199359e22bfcef84e1897f6a7`; and in a disposable clone `git revert` restored the pre-NAMES-1 tree exactly and the old suite passed.
- **Reviews:** design R-3 of v0.1 and the PASS recheck of v0.2; code review `review/Independent_ChatGPT_NAMES1_Code_Review_v0_1.md` (N1I-C01, install order), its recheck (EX_009), the final-candidate recheck (EX_011) and the final ZIP's mechanical check (EX_013, PASS). The final install ZIP is `exchange/EX_012_Claude/NAMES1_Code_Install_v1.zip` (`8548415c05688b788c0b9c9711bf670fd4afed64018f5c0617fc3a40811bfd9c`).

### 7.1C DOC-2 - installed at `908db9e` (two commits; owner-accepted exception)

- The E2R-1 specification v0.3r3 and register v0.7. Four of the package's eight files were already committed by the owner (`2c76664`, merged `f300f2d`), byte-identical; `908db9e` added the other four. The installer's PRE, POST and COMMITTED phases STOPPED (the last only on its one-commit rule; its blob check had passed for all eight). Claude confirmed byte identity before the owner pushed, and verified all eight files from GitHub. The owner accepted the two-commit delivery as a one-off exception (register v0.8); a STOP remains a STOP.

### 7.2 Powerball E_1 (accepted; frozen)

- `src/methods/E_001_Historical_Appearance_Frequency.py` with `_common/e1_historical_appearance_frequency.py`, `e1_training_view.py`, `e1_standalone_contract.py` (stable names since NAMES-1; E1-ALIGN will move them to `src/methods/E_001/`); tests `tests/test_e1_standalone.py` and `tests/p3_e1_synthetic_v0_3.json` (a frozen fixture; its name is kept).
- **Ratified goldens (R2 5.5 / TIE v0.2):** synthetic training view `df21871f8067e5405b4fdb1eec50c65dddbaa35958872bad3230d3c10a791fd4`; synthetic MAIN label-3 tie `7ce5ab1bae014adf61f1f02dd152d4b500cb405b65cb3886cdcee8dd9e2c9932`; synthetic canonical forecast `7b43d659d611791deb14d106a72984f153d9f79cc63b3d25000365de4c811d1e` (fixture target 1152).
- **Real target 1577, forecast-only:** view `d47fbbd6e60e6abc429fb74f47d8bbeafc6560152c2ecddb3b75d79932df4339`; legacy canonical result `7f1130872b3afaa222ff4e8c2396cd2c2872583544dfa6b31cc5a07cd067164e`.
- The standalone-runner synthetic pair `3851fa46...` / `8a7f917a...` is a separate, distinctly labelled set.
- `E_001_Historical_Appearance_Frequency.py` has `ENABLE_REAL_HISTORICAL_DEVELOPMENT = True` since commit `fbb66ef` (24 Oct): the reviewed gate for E_1 standalone historical development under D3 (holdout sealed, no FINAL, no termination). It is the long-standing accepted state, unchanged since; it authorises nothing beyond D3, and no new real-data run without a separate owner gate.
- Frozen **forecast** outputs (predictions from pre-1577 draws, not outcomes): TOP `[9,17,7,11,18,30,12]` with PB 2; WORST `[31,13,8,29,26,33,35]` with PB 12. Never read a 1577 outcome to check them. No golden is ever updated to make code pass.

### 7.3 Owner-run tools and data (Claude wrote the tools; do not rewrite or invoke them)

- `src/two_site_results_check_v0_7.py` (`69cb1decb1a1fed4077ccb41b91607405805721795992f57f302ae6618759aed`) and `src/results_master_v0_1.py` (`3436da9f560172606f4b9e010cd85a806b58e55597685f2ab7f65c3e17523619`) with `Run_Results_Updater.bat`. `update` has never been run and is not authorised.
- Masters: Powerball `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8` (last row 1576); Oz Lotto `4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f` (last row 1693); each ledger holds only INIT version 1.
- Reviewed orphan utilities in `transitory_data/` (inspection `606f5e22...`, archive `ca42d264...`, clearance `08000be1...`): do not modify.
- `src/GAIS/GAIS_results_fetcher_comparer.py` was deleted (commit `a52ffd8`); it stays in history and must never be revived, run, imported or adapted.

---

## 8. How to work as primary designer and coder

### 8.1 Workspace

- Work in disposable scratch trees, never on the owner's checkout. Build a tree with `git archive <base>` (or a fresh clone), apply your overlay, and run everything there.
- Unpack every received ZIP into its own fresh directory; keep your scripts elsewhere; run Python that reads untrusted files with `-I` (if tests then cannot import, add the tree to `sys.path` explicitly rather than dropping `-I`).
- Never let a tool print a quarantined row or the R1 draw-1587 paragraph. When reading master data for a non-outcome fact, print only the fields needed (`cut -d, -f1-2`).
- The cloud sandbox cannot reach lottery sites and must not try. Lottery-results searches are prohibited anyway.

### 8.2 Design before code (HIGH work)

- For HIGH work, write the design (or the specification change) first and give the reviewer the chance of a design-stage review and a competing design (R-3) before writing code. The owner ratifies any schema or rule change before code depends on it.
- Plan the oracles up front (R-4): which invariants, exact-arithmetic checks or independently designed fixtures give real extra assurance. Candidates already named: division combinatorics, sigma and tails, TIE encoding, view digests, N-1 suffix invariance. Proportionate, never decorative.

### 8.3 Your own first tests

- **Mutation checks, within safe limits:** where a test is owner-scoped and safe to execute offline, check that it detects an intentionally introduced defect, using an isolated synthetic fixture or a disposable candidate copy. Never mutate installed project files, an active safety switch, real master or holdout inputs, or live process controls for this purpose. Destructive, Windows lifecycle, scientific-run or environment-changing mutation probes keep their separate owner gates. Record any mutation check not performed as not tested. For Package 2 (in a scratch copy), putting `master_sha256` back into `order_evidence` failed 5 assertions, and a hash-free `len(raw)` leak failed all 8 ordered-kind T-05 subtests. A test that cannot fail is not evidence.
- For any statistical claim (calibration, exactness, independence), build the smallest exhaustive toy that could break it and enumerate it exactly with `fractions.Fraction`, both ways (section 8.6).
- Never "refresh" an expected hash. A mismatch is investigated, not accommodated.

### 8.4 The handback package

Include, at minimum: the work-item card; base commit; `repo_overlay/` (or a binary patch) with a SHA-256 manifest; the exact v-old to v-new diff for every changed file; test commands and full outputs; environment versions; mutation-test evidence; the DECIDED / RECOMMENDED / OPEN record; the not-tested list; a holdout statement; owner-run Windows instructions written as instructions, never as claims of execution; and a paste block for the reviewer. Keep the package reproducible from fresh Git blobs (the integration package was rebuilt from them by `run_all.sh`).

### 8.5 Document work

- Prepare a **new candidate edition** from the exact ratified Git blob, applying narrowly scoped, counted replacements (each old string asserted to occur exactly the expected number of times) to that candidate in a disposable tree, and preserving the full predecessor text except for the agreed changes. Never overwrite or amend the installed authoritative edition as a shortcut. Submit the candidate and its diff for independent review and owner ratification before installation. This edit-the-copy method is how consolidation v0.3/v0.4 and the integration succeeded; condensing or rewriting lost ratified substance (consolidation v0.1/v0.2).
- Check mechanically: every ID present; protected blocks byte-identical; every inserted character ASCII; LF and a single final newline; every line of a source accounted for; a reference scan of every inserted or moved line (proposal-relative section numbers left in moved text were the two v1 relics the reviewer caught).
- **Copy agreed wording verbatim.** Restyle only your own new text (D-1 section 6).
- Reusable patterns: the integration build and check tools (`review/MR_Integration_Tools_v3/` inside `review/Predictive_Randomness_MR_Integration_Candidates_v3.zip`; `run_all.sh` rebuilds everything from the ratified bases and runs every check) and `review/MR_Integration_Install_v1/install_status_edits.py`.

### 8.6 Lessons from Claude's own errors (keep them)

- Consolidation: Claude passed P3 v0.1 while missing that its M-INV-01..07 invariants had been dropped; counted 108 R2 IDs where there were 107. Check IDs mechanically **and** search for rules without IDs.
- Ranking proposal: Sidak instead of Bonferroni (anti-conservative for dependent events); an over-broad claim that fair-draw replay calibrates everything (it is exact only for single-track hit-code statistics on an outcome-independent opportunity grid); scored-set selection (a stopping rule at nominal 5% over at most 20 draws is crossed with probability 6467/65536 = 0.0987). State the exact conditions of every "exact" or "calibrated" claim.
- When the reviewer leans towards suppressing a number, propose labelling instead.
- Tooling: the file-writing tool can turn `\uXXXX` escapes in Python source into literal characters; scan every script you write for non-ASCII and re-escape mechanically. A diff of files containing non-ASCII may display escapes; say so when you ship it.
- The first install verifier compared raw working-file bytes and failed on the owner's CRLF checkout; normalise or use Git's own view (section 1.6).
- Git output such as "create mode 100644" can worry the owner; explain it in one line (it just records ordinary new files).
- TH-1 v1 (the reviewer's TH1-C01): a synthetic "longer" row, made by padding the last field, was not a valid row, so a test could have passed for the wrong reason. Any fixture that is meant to be valid gets its own test proving the reader accepts it.
- TH-1 v1 on Windows: a test that created a symlink before its hard-link check crashed on the owner's account (WinError 1314) and hid the hard-link result. Split platform-dependent checks into subtests and skip only the part that cannot run.
- TH-1 install: the owner extracted an earlier revision's ZIP; Claude caught it from the install log before the commit, and the owner restored the tree. A revision's verifier checks that revision's own bytes, so it cannot detect the wrong revision. Give every revision a distinct ZIP and folder name, name the exact folder in the commands, ask the owner to clear superseded extracted folders, and read the install log's paths before saying it is safe to commit.
- **Push before the committed check** (the reviewer's N1I-C01): earlier install instructions pushed first, so a wrong commit could have been published before the check stopped it. Commit, check, then push (section 1.6). The fix caught the DOC-2 deviation before anything was pushed.
- **The owner sometimes saves files into the repository** (EX files and ZIPs under `review/`, or history files committed early). A verifier's PRE then STOPs. Tell the owner to save downloads outside the repository (for example `E:\TEMP`) and to say before committing anything outside a package. When a phase STOPs and later steps were run anyway, undo and restart from PRE rather than continuing.
- **Static import guards must be symbol-aware.** E1-ALIGN v0.1 and v0.2 each missed a form the reviewer found: `from _common import game_draws_reader` (E1A-B01) and `from methods import E_001` (E1A2-C01). Check the module **and** every imported name, count textual mentions too, and add a mutation test for each counterexample. The same gap exists in the committed firewall test (section 7.1).
- **Prove "nothing else changed" with a frozen, exact allowlist** of (old block, new block) edits applied to the predecessor and compared byte for byte, not with regex categories such as "looks like an import" (E1A-C01).
- **Count before claiming.** The E1-ALIGN proposal claimed three encoder copies; there are six.
- **Hashes:** a ZIP hash retyped into a paste block was wrong twice in one message. Compute every hash with a tool and copy it.
- **Shell pitfalls:** `open(p,'wb').write(open(p,'rb').read())` truncates the file before reading it; an unquoted heredoc expands backticks (`` `name` `` became empty); `git archive` converts `.bat` files to CRLF; `rm -rf` of the shell's own working directory breaks later commands.
- **A new folder the ratified tests did not foresee** (`exchange/`, whose files deliberately contain old names) needs an exemption; flag such exemptions to the reviewer rather than deciding them silently.

---

## 9. Next work, in order (planned; the owner decides each step)

1. **Done:** TH-1 (`744afea`); DOC-1 (`be18548`); the E2R-1 specification v0.3r3 (ratified 28 October 2026) and DOC-2 (`908db9e`); NAMES-1 (`52ebeaa`); the E1-ALIGN design v0.2r1 (ratified 28 October 2026); Python 3.15.2 (28 October 2026).
2. **Next: DOC-3**, this file (H-1 v1r3) and register v0.9, which records the NAMES-1 commit and the move to Python 3.15. The reviewer may also refresh H-2. Then **the E1-ALIGN code package** (HIGH; it needs the owner's authorisation): rebase the ratified v0.2r1 trial (`exchange/EX_008_Claude/`: `apply_e1align.py`, `test_e1_align.py`, `e1align_checks.py`, `e1align_allowlist.json`) on the installed NAMES-1 tree (its `src/` and `tests/` are byte-identical to the trial's base); add the verifier and the install package in the NAMES-1 pattern; independent code RECHECK; the owner's Windows run of all 84 tests.
3. **E_2-readiness stage-1 offline code**, after E1-ALIGN (E2R-1 v0.3r3 is ratified): schema types and validators; registry status and the D-6 admission rule; per-channel probability-kind validators; IS capability as a declaration only; separate product, mode and score status; per-track provenance on the orchestration side; the scorer-only post-outcome record type with no data path; a migration rule; the D-3 method texts for E_1 and E_2. Synthetic fixtures and the development prefix only; review with R-2 reproduction and an R-4 T-05 oracle. The seed-policy package follows when a method needs seeds.
4. **Optional, owner-scoped oracle prototypes** for exact-fraction division tables and sigma/tails (agreed position 10.3), only if the owner scopes them.
5. **Still permission-gated, each separately:** new real-data scientific evaluation (including the E_1 development walk-forward and the R3 scorer on real draws); walk-forward window preregistration; Windows lifecycle and destructive gates (P2 closure, ERR-R2-02 / Option F final acceptance); method registration and allowlist entries; ranking and in-sample engines (R3 17.13 stages 2-3); E_2-E_6 implementations; any Oz Lotto science; Mode H (frozen study manifest R3-T50, `HOLDOUT_OPENED`, sequential release); FINAL and the production weekly loop.
6. **Owner decision still open from the agreed position (section 11):** whether to scope the oracle prototypes. (The transport choice was decided on 27 October 2026; section 1.6.)
7. **Housekeeping, owner's choice:** the first run of the data tools under Python 3.15; later, delete `venv.bak` and uninstall Python 3.14; a later owner-scoped tidy-up of the owner tools' and legacy tests' versioned names (OPEN-N2, deferred).

**Genuinely OPEN questions** (do not disguise as decided): the first real Oz Lotto run; E_54 feed timing; each FORMULA_OPEN method's formula; E_63 and later identities; walk-forward preregistration; Mode H storage (a separate outcome store released one by one, or a versioned master isolated by the parser; Claude's earlier suggestion is only a proposal); E_2-E_6 batching (one at a time or one reviewed batch); scientific allowlist activation.

---

## 10. Gates that stay closed

This handover authorises nothing. In particular: no Windows lifecycle or destructive test; no real-data scientific evaluation; no holdout access; no Mode H or FINAL; no process termination; no switch change; no allowlist entry; no master update; no dependency upgrade; no lottery-results search; no network acquisition; no orphan-marker clearance by any chat; no commit by Claude outside `exchange/`. The owner authorises each gate separately, after independent review.

---

## Appendix A. Identities (non-self-referential)

| Item | Identity |
|---|---|
| Agreed roles position v0.1r1 (ratified) | `doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md`, `7d572400b941ad423978a7542d6c32fb73c934f0057240dbc5138898112bd53b` |
| D-1 (earlier Claude delta) | `doc/HANDOVER/Claude_Delta_Handover_D1_since_v10_v1.md`, Git blob `ac6dda4f6f965637118dbf2811cb4006497006e10f7be72476e5acd64c37a50c` |
| ADD-2 (ChatGPT coder transfer) | `review/ChatGPT_Coder_ADD_2_Package2_v0_11r1_v0_1.md`, `ebaff99f4fc34ce38099ac5581abada7a1d0ffd1d8a7b7bfe3a0ce5fbb41f35b` |
| Claude reviewer handover v10 | `doc/HANDOVER/Claude_Reviewer_Handover_Predictive_Randomness_v10.md`, Git blob `61a5127816d30e2ffc342a011e3d029d7a3a6a80bc55c368751cc9d09ed9b191` |
| ChatGPT coder handover v1.1r1 | `doc/HANDOVER/Predictive_Randomness_ChatGPT_Coder_Handover_v1_1r1.md`, `ab0afb64cec845cbbde29265e53309225991cd4a469306c609b905aff9048a01` |
| Interim note | `doc/HANDOVER/Interim_Handover_Note_for_both_claude_and_chatgpt_v1.md`, `a46866cad2c8d16869685f3a37b898dc453bf651572e60d27579024a2015a1e5` |
| Package 2 acceptance record | `doc/HANDOVER/Package2_v0_11r1_Acceptance_Deferred_Work_v0_1.md`, `42a75e0d75d33b4d8538070ba557b7e1a8ecc7117205baf131041473227a3ad3` |
| Review methods kit v2 | `review/Claude_Review_Methods_Kit_v2/` (scripts 01-07; 05 = protected ASTs, 06 = E_1 synthetic goldens, 07 = statistical toys) |
| Integration candidates v3 | `review/Predictive_Randomness_MR_Integration_Candidates_v3.zip`, `af0e3b81d4c8deb5c818ac47c47ac8498059628b66dd681cdd9cc1c43d9d5324` |
| Integration install manifest | `review/MR_Integration_Install_v1/INSTALL_MANIFEST_SHA256.txt` |
| Review-disposition procedure (owner-accepted 27 Oct 2026) | `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`, `5067aa520990b8ccc8521a04f3581424100cdd94994f5b9e3cb9e37863685339` |
| Effective-commit verification | `review/Claude_Verification_Transition_Commit_d36735d_v1.md`, `c76b3bb305fca61bec0b791e6d792bc5b33f46529df0222498cbc5669a9343a0` |
| H-1 v1r1 (predecessor) | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r1.md`, `3223c41732888ea56c5458b365488660d157c93902b3745ed71d7d300fc2751e` |
| H-1 v1r2 (predecessor) | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r2.md`, `55543ba522a4085fc4f2476d421a4940171bcd4c183a1fab5a691d291605eac0` |
| H-2 v1r3 (current reviewer handover) | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r3.md`, `a2fb5c641a6fa8010aa59ff811aeba23145703bd5c0d4e2dbd70ac2fb419edb1` |
| Claude checkpoint v4 | `doc/HANDOVER/Claude_Checkpoint_v4.md`, `d7634683d3d40edaa27c91576531cb198f1358613ca84c2e67e42096a1a6456e` |
| Exchange protocol v0.3 | `exchange/README.md` at `262a2c4`, `a20589e5c5bdeed043e78815f86b1a71679426f17528aedfb14aef7d72ed10ef` |
| NAMES-1 install manifest | `review/NAMES1_Code_Install_v1/INSTALL_MANIFEST_SHA256.txt`, `9d8664f38c33ee374ace06d29d98a4d84477af9199359e22bfcef84e1897f6a7` |
| DOC-2 install manifest | `review/DOC2_Install_v1/INSTALL_MANIFEST_SHA256.txt`, `c3b373a3222d716963a1894ccc9d84f5737fa4af673d74b1fca18fdf1c39f8a0` |
| Committed coordinator v0.6 (AST anchor) | `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b` (in history before `c542483`; since `744afea` also the test fixture of section 7.1A) |

**Commits (verified by Claude unless marked):** `2db2554` governing documents installed; `a52ffd8` GAIS removed; `6726963` handover snapshot v9 + coder v1.0r1; `ac01678` MR v0.5 and exposure v0.2; `618fe48` handover v10 + coder v1.1r1; `4a45b70` roles agreed position; `0f07174` Claude's Package 2 review and integration v3 in `review/`; `089a97e` Package 2 install overlay and ADD-2 (history); `c542483` Package 2 v0.11-r1 installed; `ae76c29` integration installed; `6460ae3` four history files from the transition manifest (owner, before the install); `d36735d` the effective commit (H-1 v1r1, H-2 v1r2, H-3 v1r1, register v0.5); `997ed46` transition install history; `151f393` TH-1 packages and reviews (history); `744afea` TH-1 installed; `b14116b` review-disposition procedure; `be18548` DOC-1 (H-1 v1r2, H-2 v1r3, register v0.6); `319fd11` and `38fc60e` snapshots (E2R-1 review history, checkpoint v4); `6891196`, `06a672f` and `262a2c4` the exchange README v0.1-v0.3; `2c76664` (merged `f300f2d`) ten history files committed by the owner; `908db9e` DOC-2; `52ebeaa` NAMES-1; exchange records EX_001..EX_014 in `exchange/` (up to `83d1515`); the commit installing this file (recorded externally).

## Appendix B. Changes in v1r2 (records refresh DOC-1)

v1r2 is v1r1 with the following changes and nothing else; the exact diff travels with the DOC-1 package.

1. Header, section 0 and Appendix A: the effective commit named (`d36735d`); later commits listed; the review-disposition procedure added to the reading list and identities.
2. Section 1.5: the FIX AND PROCEED / RECHECK procedure with the owner's exclusion for always-review code; the status of the first-three-reviews oversight.
3. Section 1.6: the delivery method the owner decided on 27 October 2026 replaces the "two routes, transport not yet ratified" text.
4. Section 2: package sizing, as the owner confirmed on 27 October 2026.
5. Section 4: register v0.5 and v0.6 replace the register v0.4 row; the out-of-date list no longer names lines register v0.5 already corrected.
6. Section 6: the owner's NTFS hard-link evidence replaces "TO-TEST" for hard links.
7. Section 7: the new suite command and results; the new section 7.1A (TH-1); the deferred list and not-tested list updated.
8. Section 8.6: three lessons from TH-1.
9. Section 9: item 1 done; the transport decision removed from the open owner decisions.

## Appendix C. Changes in v1r3 (records refresh DOC-3)

v1r3 is v1r2 with the following changes and nothing else; the exact diff travels with the DOC-3 package.

1. Header, section 0 and Appendix A: the baseline is NAMES-1 at `52ebeaa`; the reading list adds the exchange protocol, the three new specifications and the newest EX files; new identities and commits.
2. Section 1.1 and section 10: Claude commits and pushes inside `exchange/` only.
3. Section 1.5: the oversight instruction, extended indefinitely with reporting by exception.
4. Section 1.6: the phone exchange protocol; CRLF and LF identities; LF copies under `review/`; commit, check, then push; `git pull --ff-only` first; already-committed files.
5. Section 2: the EX file replaces the paste block on a phone; hashes are never retyped.
6. Section 3 and section 5.4: Python 3.15.2, the fallback, the data tools not yet run under 3.15.
7. Section 4: register v0.8 and the E2R-1, NAMES-1 and E1-ALIGN specifications; register v0.9 installed with this file.
8. Section 5.3: E2R-1 decisions D-1..D-11, the layout (OPEN-N1..N3), E1-ALIGN and E1A-D1..D3.
9. Section 6: archived `.bat` bytes, the owner's `core.autocrlf=true`, Python 3.15's UTF-8 default.
10. Section 7: the stable module names; the 60 + 19 suite commands and results on 3.14.10 and 3.15.2; the known firewall gap; new sections 7.1B (NAMES-1) and 7.1C (DOC-2); E_1's file names.
11. Section 8.6: eight lessons from 28 October 2026.
12. Section 9: the done list; DOC-3, E1-ALIGN code, E_2-readiness code; housekeeping.

*End of H-1.*
