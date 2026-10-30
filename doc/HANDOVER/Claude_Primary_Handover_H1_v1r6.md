# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v1r6

**Document:** H-1 under the agreed roles position v0.1r1, section 9 item 4.
**Version:** v1r6 DRAFT, 30 October 2026 (Adelaide, UTC+10:30). v1r6 refreshes v1r5 after waves 1 and 2 (owner, 30 October 2026). It keeps v1r5's structure, describes the current state and the owner's order of work, and changes no rule. Appendix B lists what changed. Author: Claude. The project owner ratifies. **The reviewer chat that reviewed v1r5 reached its maximum length on 30 October 2026, after EX_075;** on the owner's instruction Claude also drafted the reviewer's handover, H-2 v1r7, and the new reviewer chat reads both when it starts.
**Status:** DRAFT for the owner. It becomes authoritative only when the owner ratifies it and installs it with register v0.20; until then H-1 v1r5 stands. Nothing here grants any run, test, data-access, holdout, termination or Git permission.
**Audience:** any later Claude chat that takes over as primary designer and coder; the ChatGPT reviewer chat; the project owner.
**Repository:** `hydra3333/analysing_perceived_randomness_in_reality`, public GitHub, branch `main`.
**Baseline described:** the wave 2 package installed at `b61b1a27999dcdfce2e2e59c6ced4f349ee652b4` (30 October 2026; verified by Claude from GitHub; section 7). Later commits are `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/` records only. The commit that installs this file cannot name itself; Claude records it in the post-push check.
**Replaces, for future roles:** H-1 v1r5, v1r4, v1r3, v1r2 and v1r1 (kept as history), and, as they did, the older handovers listed in v1r3's header. D-1 and ADD-2 are inputs, not authority.
**Authority:** the ratified documents and the current register prevail over this handover wherever they conflict. This file summarises and points to them.
**Holdout discipline for the reader:** no winning, Powerball or supplementary number of any draw appears here. The only number lists are the frozen E_1 *forecast* outputs (section 7.3). Never display, paste or compute with an outcome for Powerball >= 1577 or Oz Lotto >= 1694.

---

## 0. First actions in a new Claude chat

1. Clone `main`. Check that this file is the H-1 edition the current register names, and that the hashes in sections 4 and 7 match `git show HEAD:<path> | sha256sum`.
2. Read, in order: the introductory blurb that started your chat (`doc/HANDOVER/Claude_Primary_Handover_H1_v1r6_introductory_blurb.md`); this file; H-2 (what the reviewer checks and its rights); the **current register's newest sections** (they hold everything since this file); H-3; `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`; `exchange/README.md`; `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (the local runner's rulebook); `doc/METHOD_TEMPLATE/README.md` (how a method is added); the governing set in section 4; the newest `exchange/EX_NNN_*` files, which show the latest open exchange with the reviewer; and the owner's two working lists, `exchange/OWNER_ROADMAP.md` and `exchange/OWNER_REMINDERS.md` (section 2).
3. Ask the owner where things stand, using section 10 and `exchange/OWNER_ROADMAP.md` as the list. Do not assume anything has advanced since this file was written.
4. Before any code: name the work item, its risk tier and its reviewer chat (section 1.2), and check that the owner has scoped it.
5. Keep a running checkpoint of decisions and hashes at each package boundary, so no state lives only in the chat. The cloud workspace is not permanent: everything needed to rebuild a package travels in its EX record (section 8.7). When the chat nears its limit, write the next handover first.

---

## 1. Roles and workflow (agreed position v0.1r1, ratified)

### 1.1 Who does what

- **Claude (you):** normally leads scientific and technical design, specifications, governing-document integration, primary code and its first tests. You prepare complete, hash-recorded packages; you never open pull requests, and you never change project files in the main tree. **Your commit rights (owner-authorised):** inside `exchange/` (every exchange file from both chats, byte-for-byte; section 1.6), and in and under `CLAUDE_CODE_WORKING_FOLDER_TREE/` (owner, 28 and 29 October 2026; section 8.6). Nothing else.
- **ChatGPT reviewer chat:** normally leads independent scientific and technical review. It may propose competing designs, methods and hypotheses, and may do bounded coding, alternative implementations or tests when the owner assigns them. Its handover is H-2. The reviewer chat that served until EX_075 reached its maximum length (30 October 2026); the owner started a new one from H-2 v1r7 and its introductory blurb, both drafted by Claude on the owner's instruction, with H-2's protected rights text byte-identical. Treat the new chat exactly as the old: same rights, same independence.
- **Claude Code local runner** (owner-decided 28 and 29 October 2026): Claude Code on the owner's Windows machine carries out task files Claude writes, in disposable task clones that cannot push, and reports what happened. It makes no design or code decisions. Its reports are owner-machine evidence, not reviewer evidence and not acceptance (section 8.6).
- **Project owner** (GitHub `hydra3333`): sole ratifier and execution authoriser, and sole committer of project files. Runs every Windows install and every data tool. **Never name the owner in anything that may be committed**; write "the project owner" or "hydra3333".
- Both models may challenge each other with evidence. Neither may override an owner-ratified decision. The owner may revise the allocation at any time. The ChatGPT coding chat and the earlier Claude reviewer chat are retired (27 and 26 October 2026).

### 1.2 Author and reviewer rules

1. Every consequential deliverable names its **author chat** and its **reviewer chat**.
2. The required independent review is always by the **other model**. A second Claude chat never counts as the independent review, however careful.
3. **Mixed authorship:** if the reviewer rewrites consequential parts of your patch, those parts come back to you for review, or become a separate package. Nobody approves its own mixed result.
4. **Work-item card** at the top of every handback: item ID; author and reviewer chats; base commit; input hashes; scope; risk tier; owner gate; evidence state.

### 1.3 Risk tiers and evidence (agreed position section 3)

- **HIGH, whatever the size:** normative or authority text in a governing document or the register; a protected block; a test golden or expected hash; a safety switch, gate constant or allowlist; reader, view or digest code; evaluator, scorer or tie code; dispatch, publication and consumption code; anything under `source_data/`.
- **LOW:** comments, and formatting in non-normative text (still hash-recorded).
- The tier decides who must check; the scope decides how much checking is needed.
- **Every handback carries:** the base commit; changed files with hashes; exact test commands and their outputs; environment versions; an explicit not-tested list; a holdout statement.
- **Evidence states are distinct:** IMPLEMENTED, TESTED, REVIEWED, ACCEPTED, COMMITTED. Never use one for another. Label evidence VERIFIED / OWNER-REPORTED / UNVERIFIED (TO-TEST for Windows-only behaviour), and say whose it is (author, reviewer, runner).

### 1.4 Findings, rights and disagreement

- Finding classes: **BLOCKER, CORRECTION, OPTIONAL, RECONSIDER**. RECONSIDER asks the owner to revisit a ratified decision; it never blocks by itself. Each finding cites file and line, the failure scenario and replacement text. A style preference is never a BLOCKER.
- **The reviewer's rights R-1..R-11** (agreed position section 5 and H-2): full bytes, never excerpts; independent reproduction of authorised offline tests (R-2); design-stage review before code for HIGH work, including a competing design (R-3); independent reference oracles where justified (R-4); findings outside the diff (R-5); RECONSIDER (R-6); access to your not-tested list (R-7); and R-8..R-11 (problem framing, evidence sufficiency, declining unsafe tests, material findings outside a narrow scope). **Support these rights; never narrow them.** Supply everything the reviewer needs to reproduce your results.
- **Disagreement:** finding, author's reply, reviewer's response; if still open, it goes to the owner as claim, evidence, counterexample, consequence if wrong and recommended decision. Two rounds on unchanged evidence; a new counterexample opens a new finding. Never withhold evidence; never relitigate a settled point without new evidence.

### 1.5 Decision labels, oversight and the always-review list

- Report a choice as **DECIDED** only for an already ratified owner choice, or a purely mechanical implementation choice explicitly inside the approved scope; cite the authority. Label proposed consequential choices **RECOMMENDED**, and unresolved ones **OPEN**. Claude does not independently ratify a new scientific, safety, test or review policy.
- Claude may choose routine internal coding organisation, packaging details, version labels and presentation that neither alter the approved scope nor affect an acceptance or review gate. Deferring a ratified or required test, changing required evidence, waiving or reducing an independent review, changing a safety gate, accepting a consequential deviation, new rules or scope, anything that weakens safety, switch-on or destructive tests, ratifications, real-data gates and anything irreversible go to the owner, with independent reviewer input where required.
- **REVIEWER-DECIDED:** the reviewer settles routine review matters itself (owner, 27 October 2026; H-2 section 3.1). **Oversight (owner, 27 and 28 October 2026; indefinite):** Claude checks every REVIEWER-DECIDED item against the ratified compliance, safety and process rules and reports one to the owner **only by exception**: if Claude disagrees, or judges it of owner interest. This is reporting only; reviewer rights are unchanged. No departure has been found so far (through W2-075-RD-04).
- **Always independently reviewed before consequential execution or acceptance** (owner, 23 October 2026): process termination (kill logic, ownership, the switch); N-1 boundaries and leakage; fit seeds and canonical forecast identity; TOP/WORST readout, ties and selection; holdout access and unsealing; FINAL freezing, persistence and publication; the synthetic/real firewall; dependency upgrades (W-23). The HIGH tier adds to this list; it never removes from it.
- **Review dispositions** (`review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`, owner-accepted 27 October 2026): **FIX AND PROCEED** lets Claude make exactly the authorised correction and continue; **RECHECK** (the default) sends it back. Only the reviewer assigns one; Claude never assigns, broadens or changes it; the owner may override. FIX AND PROCEED never applies to code concerning an always-review subject. Keep the exact diff, hashes, the authorised wording, test outputs and a not-tested list for every FIX AND PROCEED item. If the fix needs more than was authorised, it becomes RECHECK.

### 1.6 Git and transport

- **Code packages** (anything touching `src/`, `tests/`, a wrapper or an always-review subject): whole-file overlay plus a read-only verifier. The package has `repo_overlay/`, `VERIFY_*.py` with `pre` / `post` / `committed` phases, a suite runner that compares each module's test count with its expected count, the exact diff of every changed file, and `INSTALL_INSTRUCTIONS.md`. Replaced files are listed and checked against their base bytes; deletions are explicit. The install order is fixed: `git status --short` (clean) and `git pull --ff-only`; PRE; copy; POST; **the suite, before the commit**; stage; commit; COMMITTED; **push only after `COMMITTED PASS`**. Never an unconditional `git reset --hard HEAD~1`; on a STOP the owner stops and sends the output. While the owner installs, Claude pushes nothing. After the push, Claude verifies from a fresh GitHub clone (file list, every blob against the manifest, the suite).
- **Document-only installs** (owner, 28 October 2026; files only under `doc/` and `review/`): one zip mirroring the repository, short commands (`git pull --ff-only`, copy, `git add doc review`, `git status --short` showing only the expected files, commit, push), and one Claude check from GitHub after the push. No verifier, no PRE/POST/COMMITTED, no reviewer check of the install zip. Content review is unchanged.
- **Review rounds** (owner, 29 October 2026): register text goes to the reviewer only together with a code package or the handovers, never in a round of its own.
- **Final packages after ratification** differ from the reviewed candidate only by the owner's finalisation (the register's status line, any filled placeholder, and the dependent manifest line and verifier hashes). They travel to `exchange/` in a for-the-record EX message that needs no reply (EX_046, EX_054, EX_057, EX_067, EX_076), with the narrow diff; the reviewer is not asked to re-review them.
- **Verifiers must tolerate CRLF working copies.** The owner's checkout uses `core.autocrlf=true` (Git warns "LF will be replaced by CRLF" when staging; harmless); Git stores LF. Compare working files after CRLF->LF normalisation and committed files with `git show HEAD:<path>`; use `git --no-optional-locks`. Test every verifier in an LF clone and a CRLF clone, with negative tests (a stray file, a modified guarded file, wrong bytes, an extra file, an extra committed file, a damaged package).
- **The exchange protocol** (`exchange/README.md` v0.4, `63c19e7`). Each message between the two AI chats is one upload: `EX_NNN_<Sender>.md`, or a flat `EX_NNN_<Sender>.zip` whose EX message has a `Contents:` line (no zip inside a zip, except an install package carried as a member). One shared increasing `NNN`; never reuse a number. First line `# EX_NNN - <Sender> to <Recipient>`; headers `Date`, `Project`, `Replies to`, optional `Supersedes`, `Contents`, `Subject`; EX messages US-ASCII with CRLF and a member table with two hashes (as stored, and after CRLF->LF). An enclosed document derived from a UTF-8 project file keeps its encoding; its identity is its LF hash. **Claude records every EX file from both sides in `exchange/`, unchanged** (a zip also extracted to `exchange/EX_NNN_<Sender>/`), commits and pushes only there, and checks the pushed bytes. **The owner uploads the reviewer's zips to Claude and does not save them into the repository** (owner, 29 October 2026). Besides EX files, Claude keeps two owner working lists in `exchange/` (section 2); they are not EX messages and not rules. When an exchange review later goes into `review/`, store an **LF copy** and cite its LF hash.
- **Already-committed files:** if a file a package would add is already committed byte-identical, the verifier treats it as guarded, not new, and the builder asserts the identity first.

---

## 2. How the owner wants work presented (follow strictly)

- **Lead the owner through next steps.** Say what happens next and who does it, in plain step-by-step English. Label every paste block with its **destination chat**.
- End every response that needs relaying to the reviewer with a short **paste-ready block**; the owner likes these. Hashes in any block are computed by a tool and copied, never retyped.
- **Decisions:** plain-English question / why / recommendation / options, one at a time with a recommendation each (the question tool is fine for several independent ones).
- **Verify, don't assert.** Check claims against the files, line numbers, library source or official documentation.
- **Plain English**, not acronym-dense text; concentrate on substance. Explain alarming-looking tool output in one line (for example "create mode 100644" or the CRLF warning).
- **Files Claude produces:** US-ASCII where possible; CRLF for EX messages; LF for repository files; UTF-8 kept where the file derives from a ratified UTF-8 text; the version in the file name; no owner name. Check the encoding mechanically.
- **Superseded versions are kept**, not overwritten.
- **Proportion** (owner, 29 October 2026): the owner asked how much plumbing is really needed. Keep the safety-critical machinery (holdout and orphan protections, the release gate, independent review of HIGH work, hash-checked code installs) and keep everything else lean: combine rounds, keep documents short, and do not add machinery a method does not need. The owner's priority is **getting the project running**.
- **Package sizing (owner, 27 October 2026):** small packages for complex or HIGH work; a lead item that proves the pattern before a batch of similar items; heavy methods one at a time; ensembles last.
- **The owner's working lists** (owner, 30 October 2026), both in `exchange/`, both outside the rules:
  - `OWNER_ROADMAP.md`: the steps in plain English and where the project is up to. Update it at each milestone and show it to the owner then, and whenever asked;
  - `OWNER_REMINDERS.md`: things the owner asked to be reminded of, each with the date asked and its status (OPEN, DONE or DROPPED, never deleted). Raise each OPEN item when its "when" arrives, or when the owner asks.
- **Introductory blurbs** (owner, 30 October 2026): each handover has a starter text saved next to it, named `<handover file name>_introductory_blurb.md`, which the owner pastes to start the new chat. Keep it in step with its handover, and write your own handover and blurb first.
- **When the owner is away** and has said to carry on: work in chunks, each ending in something the reviewer can review; hold code whose design has not yet passed; and leave a short summary of what was done, what to send and what to decide.

The owner restated the purpose on 30 October 2026, with the reviewer chat's six working principles (register v0.15). It restates these points and changes no rule.

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

Two games, never pooled, one game per run. **Powerball:** current format since Draw 1144, 19 April 2018; 7 distinct main numbers from 1-35 plus 1 Powerball from 1-20. **Oz Lotto:** current era since Draw 1474, 17 May 2022; 7 from 1-47 and no Powerball barrel; its 3 supplementaries never enter any method view, fit, seed, digest or prediction, and **the evaluator alone** may read a target's supplementaries, after the target is opened and its forecast frozen, solely to classify prize divisions (R2 v0.5 section 2.5). The project builds a Python research system on Windows 11 (the venv is Python 3.15.2) that tests whether past draws hold any predictive structure, using 62 permanently registered methods, E_1-E_62 (room up to E_106; E_63 and later are not registered). Each method produces full rankings and publishes TOP and WORST predictions side by side. Real weekly forecasting starts only after modelling is complete: train on all eligible draws before the target, predict, freeze and push before the draw, score afterwards, append the draw, repeat. Method rankings (league tables) are reports per R3 section 17; they never feed forecasts.

---

## 4. Governing documents

All in `doc/`. SHA-256 values are of Git blobs (UTF-8, LF).

| Document | SHA-256 | Governs |
|---|---|---|
| `Predictive_Randomness_Research_Project_Proposal_v0_6.md` | `6a281e05127e7db976a16557ba69006327a8d615c2b0ec90bb6b34ee1c648a73` | Charter and philosophy; A-01..A-37, D1-D5; 2.7 rankings charter; E_1-E_6 definitions |
| `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` | `19809ae8a1aca716c6c6a4de71a37b705129304894a2b382036d51b76575b99f` | The E_1-E_62 catalogue |
| `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_5.md` | `2c67db8fcba50e469b0490cd85caf2fe964b3b79fc17fe7da4ebf033b91d9a3e` | Data, views, N-1, method contracts; 2.5 supplementaries; 5.5 E_1 goldens; 5.6 stage-1 fields; 8.4 in-sample mode; T-01..T-39 |
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md` | `53e30a3e649b48b8a88923d08bf578caf04a4ce93d6ea6468891ca97e93a57b6` | Evaluation, TOP/WORST, rank position, holdout, freeze-to-score; section 17 method ranking measures |
| `Predictive_Randomness_Software_Architecture_Discussion_v0_8.md` | `32cf157d9ce8850e790274e962236f2be3b50a8bdee7ec94a28ba00d7fd452ec` | Wrappers, coordinator, **5C process safety (protected)**, W-01..W-25, A-01..A-26, 20A |
| `Predictive_Randomness_MultiGame_Infrastructure_P3_Task_Specification_v0_2.md` | `2f3ac0e82dfd159025c3933ba41e812a4af0254da13e56664ed36dd5c5dcb61c` | Package 2 invariants M-INV-01..07 |
| `Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md` | `0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954` | **E2R-1**: the method-generic contract (records, registry, release rule 12A.3, retirement 12A.2), owner decisions D-1..D-11 |
| `Predictive_Randomness_E2R_Code_Scope_v0_1.md` | `2d0b0c6acf2f77a518276e24c1c69f6ab3c065ddda26b1cf153cbce0f50c08a1` | The three-package scope S-1..S-3 (CODE-1, CODE-2, CODE-3) |
| `Predictive_Randomness_E2R_CODE2_Design_v0_1r1.md` | `f0c36fd3dabb83dcc5f21d8b92bd9b5c3eaf9647da069a4e5bff63514a26f2dd` | CODE-2's design (dispatch gate, standalone runner, publication, consumption, E_1 wrapper); D2-1..D2-4 |
| `Predictive_Randomness_E6_Specification_and_Method_Template_Design_v0_1.md` | `cef16b44fb7088ec018e0a8d6f233231c04e3fe6d5431cf0a2e604ad8f6fc82e` | E_6's specification and the new-method template's design; D6-1..D6-5 (for lambda < 1, read "discounted (power-likelihood) Beta update" for "posterior mean": register v0.15) |
| `Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md` | `b9d60b4c753bb90c6a7ca302fb4802c353b0ae23fbe82c2b417ae7b089fad072` | E_3's and E_4's specification and the shared polynomial-fit helper; D34-1..D34-5 |
| `Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md` | `06b491225812e14962aef99e299cbd6c003be68bb5a73425e566f1b1fe685060` | Wave 1: E_7, E_8, E_9 and E_10 and the shared counting helper; W1-1..W1-6 |
| `Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md` | `2ab342911701edf1e93ad590e4765a3efac54a76d732b7fd2c5875c7d363fe74` | Wave 2: E_2, E_17 (Method A), E_18 and E_19 and the shared gaps helper; W2-1..W2-8 |
| `GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md` | `4f5459b5bb3ae24ba0624e140e71729213928eafc090bb9fd9a78405a621c597` | The owner's Methods A and B (A is E_17's log-age variant; B becomes E_45's specification in wave 3); supersedes the pre-exploratory `GASI_thought_experiments_possibly_unexplored_areas.md` |
| `METHOD_TEMPLATE/README.md` (and the 9 other template files) | `daac8da1f404e21bd1869609e4621f47bc25a84b3524c1688703c69ca2064214` | The new-method template, draft 3 (W2-7): what to copy, what to fill in, the checklist, "things that bite" |
| `Predictive_Randomness_NAMES1_Rename_Specification_v0_2.md` | `07bda3e4a8a99bfc611a76cec672f8642532186567737e1a23de5e5701489e5a` | Stable file names; OPEN-N1..N3 decided |
| `Predictive_Randomness_E1_ALIGN_Specification_v0_2r1.md` | `d9ffd900c74d8a0cc5002bb78c83121f818514cd88ca9150bada8d6d1fa6653a` | E_1 in its own folder; the symbol-aware firewall; E1A-D1..D3 |
| `contracts/TIE_SHA256_V1_Ratified_Encoding_v0_2.md` | `045b784d16a4611ac4ba5e8af063733e957b0b9359882d52b7143b912a65a0b6` | Tie and seed encoding |
| `HOLDOUT_EXPOSURE_RECORD_v0_2.md` | `aec833fe031b6d1d73e6acbb81757b50b193425a6899c84d438431d9df4433e2` | Factual, value-free exposure record (6 items) |
| `NUMERICAL_INTEGRITY_AND_RETRAINING_REFERENCE_v0_1.md` | `51bcc84bc2ce4c2eda9c99008e75817f85e3f17ef12fc6639c1be6fd0ac3108d` | Non-normative precision guidance |
| `Predictive_Randomness_Windows_POC_Implementation_Task_Specification_v0_2.md` | `ca5e89dde7e9927974e759f1df115eefca03144de45e073c240aa9e13f24ebf1` | P0-P2 history, subject to Architecture 5C |

- **The register:** the current edition is the authority on every document's status, every install and every owner decision; register v0.20 is installed with this file (register v0.19 is `b3ae51fd162960b64a9d145a52646dceeb3aec5b91e4b359ad7166e5e4c8e6a0`). Each edition ends with a list of **out-of-date statements** in earlier files; the files are not edited, and the next edition of each folds the corrections in.
- **Historical, kept, not operative:** earlier editions of all of the above, and the method ranking measures proposal v0.2-v0.5 (v0.5 is integrated history).
- **Protected blocks (byte-identical through every consolidation; never edit casually):** Architecture 5C; R2 section 7 and 4.1; R3 0.4, 2.4 and 3; Proposal E_1-E_6.
- **Never edit a ratified file in place.** Old "candidate" headers stay; the register decides status.
- **R1 method families:** E_1-E_6 originals; E_7-E_16 frequency/Bayesian/regime; E_17-E_22 recurrence; E_23-E_32 within-draw/drawn order; E_33-E_40 spectral/curve; E_41-E_48 information/nonlinear; E_49-E_54 ML/external (E_54 uses date covariates); E_55-E_56 ensembles; E_57-E_62 pilot-wave-inspired mathematics. E_14 and E_54 use dates. E_1 is "historical appearance frequency", not a pilot-wave method.

---

## 5. Settled decisions - do not reopen without substantive cause

The governing documents hold the rules and the register holds the history. The essentials:

### 5.1 Data and holdout

- **Quarantine from 2026-08-01.** Powerball >= 1577 and Oz Lotto >= 1694 are quarantined. Development data: Powerball 1144-1576 (433 draws), Oz Lotto 1474-1693 (220). Development targets never exceed 1576 / 1693; walk-forward windows (Powerball 1145-1576, Oz 1475-1693) are maxima pending preregistration (OPEN).
- **FINAL_HOLDOUT_10:** Powerball 1577-1586, Oz Lotto 1694-1703.
- **E_1 exception:** the target-1577 regression is forecast-only, trained on 1144-1576; the 1577 outcome is never read, scored or counted as a holdout result.
- **Drawn order:** the published sequence is assumed operator order, label `OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`; never verified physical order; set and order views of the same rows are not independent samples.
- **Source:** Lotterywest's own results-search page on `www.lotterywest.wa.gov.au`, read by an honest, unmodified headless browser with >= 2 s pauses. **No API of any site; no browser impersonation; no bot-protection bypass; `oz.lotterywest.com` is never contacted; no new scraper by any AI.** The Lott is used only through pages the owner saves by hand outside the repository, as a private verifier; nothing derived from it is committed; **no automation of The Lott, ever**.
- **No lottery-results searches** by any project session, author, reviewer or runner. Accidental exposure is reported factually for the exposure record, never suppressed or asserted harmless.
- **One master per game:** `source_data/<GAME>_results_master.csv` with its append-only ledger, value-free INIT record and create-only `backups/` and `grabs/`. Every run pins the master version and SHA from the ledger. `.gitattributes` has `source_data/** -text`; never change it.
- **The owner will not run `results_master update`**, even to test; it is gated by `HOLDOUT_OPENED_<GAME>.json`, which is not authorised.
- **Dates only** in masters. No pre-April-2018 draws, including Powerball-only analyses.
- **Exposure record v0.2 (six items, value-free):** never repeat the values it refers to; disclose rather than re-seal; make no claim about influence. When diffing documents containing the R1 draw-1587 paragraph, filter it out first.

### 5.2 Scientific contract

- **Strict N-1:** target N sees only eligible draws with `draw_number < N`. **T-05:** change N and every later row; every method-visible field, array byte, schema, digest and capability must be identical, and the forecast byte-identical. Orchestration-side provenance may differ; provenance handed to a method must not.
- **The B1 rule:** the whole-master SHA-256 is derived from target-and-later rows. It is orchestration-only provenance and never reaches a method, directly or inside any method-facing object. The same holds for whole-file size and any other suffix-derived metadata.
- **Seeds and content identity** come from the permitted training-view digest, never the whole-file hash.
- **Views:** `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER`, `PAIRED_DIAGNOSTIC`; caller-declared; paired views never double-count. New schemas bind `game_id`, era and profile version (the legacy `E1_REAL_U_TRAINING_VIEW_V1` alone is exempt). Dates are opt-in with their own schema and digest.
- **Numerics:** `int64` integers and `float64` floats in the reader's table and every returned view; views are byte-backed, own their prefix-only copies, read-only, with no `.base` path to later rows. Python `int` for exact counts beyond int64.
- **Fresh fit for every target** on the eligible prefix; an incremental cache needs a reviewed byte-identical comparison with from-scratch fitting.
- **TOP and WORST from one frozen ranking;** joint-set TOP gets WORST only through `INVERSE_FROM_MARGINALS`, otherwise `INVERSE_UNAVAILABLE`, never fabricated.
- **Prediction-time ties:** `TIE_SHA256_V1` only. Post-draw rank position uses mid-ranks and never alters a frozen forecast.
- **Status vocabularies stay separate:** benchmark (R2-C20) `SUCCESS`, `TIMEOUT`, `ERROR`, `INSUFFICIENT_HISTORY`, `BLOCKED_DEPENDENCY`, `NUMERIC_INVALID`; evaluation (R3) `RUNTIME_FAILURE`, `INSUFFICIENT_HISTORY`, `DIAGNOSTIC_ONLY`, `NOT_IMPLEMENTED`, `INVERSE_UNAVAILABLE`, `PREDICTION_AVAILABLE`; registry `SUPPORTED` / `FORMULA_OPEN` / `UNSUPPORTED_FOR_GAME` with a reason. Oz has no Powerball barrel; never zero-pad one.
- **Synthetic firewall:** synthetic data, states and scores never enter real fits, predictions or scores, and never exclude a method.
- **Method rankings (R3 section 17):** reports only; walk-forward and in-sample never ranked together but shown side by side with a "hindsight advantage" column; in-sample labelled `IS_NOT_CALIBRATED` and never on the scientific allowlist; ranking-driven selection is a separately registered meta-method using past walk-forward scores only. One programme-wide search log, `results/audit/SEARCH_LOG.csv`. Bonferroni over predeclared families; no Sidak.

### 5.3 The method contract (E2R-1, implemented by CODE-1 and CODE-2)

- **Identity and records:** a method's scientific identity is `E_n`; its folder `src/methods/E_<nnn>/` is a locator only (E2R-R53). Each revision has an immutable `METHOD_DECLARATION_V1`; its status lives in append-only, hash-chained `REGISTRY_ENTRY_V1` records under `src/methods/_common/contract_data/`. The installed data, in both games: E_1 `SUPPORTED` (variant `FULL_HISTORY_RAW_COUNTS_V1`, revision 1); revision 1, all `FORMULA_OPEN` with their `IN_DEVELOPMENT.txt` flags present, of E_3 and E_4 (six variants each), E_6 (three), wave 1's E_7, E_8, E_9 and E_10 (three each) and wave 2's E_2, E_17, E_18 and E_19 (three each); and E_2..E_62 each keeping a `FORMULA_OPEN` placeholder with variant `NOT_YET_SPECIFIED`, which is never edited (also for the methods that now have real variants). That is 80 declarations and 202 registry chains (282 files).
- **The release rule (D-6, E2R-R57):** a normal dispatch needs an active `SUPPORTED` entry for the exact game, method and variant, pinned by the request, with matching revision and declaration, **and** no `src/methods/E_<nnn>/IN_DEVELOPMENT.txt`, **and** every other gate. Release (E2R-R58) is a separate small reviewed package: it deletes the flag and appends a `SUPPORTED` entry; new code always arrives non-runnable. A refusal reads no data and creates nothing. Neither action alone, nor both, authorises a scientific run.
- **Other owner decisions in E2R-1 section 14:** D-1 `track_id` excludes the method revision; D-2 synthetic and benchmark records carry `NOT_EVIDENCE`; D-3 plain-English method texts (written for E_1 and E_2 in CODE-1); D-4 current code only, stable names; D-5 superseded revisions move to `archive/methods/E_<nnn>/r<k>/` with a README, no stored hashes or commit IDs, no promise of exact replay (this is CODE-3); D-7 the package order; D-8 results shown "as published" and "current methods"; D-9..D-11 seed roots from a pre-announced NIST Randomness Beacon pulse, fetched once by hand and verified, runs never fetch, every root tried is logged and counted (carried forward to the seed-policy package: keep a dated copy of each pulse-selection rule; reject any response for a different pulse).
- **CODE-2's owner decisions (29 October 2026):** D2-1 standalone path only; the coordinator side has only a refusing entry point. D2-2 a fourth switch, `ENABLE_CONTRACT_REAL_DEVELOPMENT`, stays False: contract runs are synthetic only. D2-3 E_1's legacy runner gets the release check (E_1 stays revision 1; E2RC2-RD-07). D2-4 Package 2's roster is a roll-up of the installed registry only; admission is the dispatch gate's.
- **Owner decisions for the new methods (30 October 2026):** D6-1..D6-5 (E_6: no per-method entry file for a contract method, E_6's model and variants, the release plan, WF-1 planning only, the template draft 1) and D34-1..D34-5 (E_3/E_4: one shared helper, six frozen variants, raw least squares and smoothed interpolation and minimax, scores only, precise naming); W1-1..W1-6 (wave 1: one shared counting helper, twelve fixed variants, E_7's full-history calibration variant kept, E_9 and E_10 score-only and E_7 and E_8 publishing marginals, template draft 2, E_8 by moment estimates); W2-1..W2-8 (wave 2: one shared gaps helper; twelve fixed variants; W2-3, E_17's `HAZARD_LOGAGE_SIGN_V1` is Method A's own log-age rule, decided exactly, with Method A's diagnostics A1-A5 a later package after WF-1; all four score-only; E_18 a fixed four-law library by exact minimum chi-square; E_19 per number with cycles 2, 3 and 4; W2-7 template draft 3 with the byte-reproducibility rule; W2-8 the NIST seed settled at WF-1's design). Each method's variant settings are fixed in its specification before its code, because any later code change to a released method is a new revision (E2R-R14A).
- **Layout:** a **contract method** (D6-1) has no entry file of its own: the shared standalone runner, `Method_Contract_Runner.py`, is its entry, through one `ADAPTERS` line. Its code is in its own folder, `src/methods/E_<nnn>/`, with `contract.py` (compute and verify) and `IN_DEVELOPMENT.txt`. E_1 keeps its legacy entry file directly in `src/methods/` (`E_<nnn>_<Name>.py`), as the Option F wrapper requires. Shared reviewed modules are in `src/methods/_common/`; contract adapters are in `src/methods/contract_adapters/`. The static import firewall is symbol-aware with exact, counted allowances (E1-ALIGN).
- **Multi-game:** profiles are a frozen module with no free-form barrel parameters; identity is (`game_id`, `draw_number`); separate namespaces per game; no cross-game pooling without a preregistered owner-approved design. **No Oz Lotto method execution is authorised.**

### 5.4 Engineering and process safety

- **Option F, the single launch interface:** `Run_Coordinator.bat` -> Python coordinator -> `Run_Experiment.bat` per experiment -> method `.py`; manual: `Run_Experiment.bat` -> method (including `Method_Contract_Runner.py`). No second production launcher. ERR-R2-02 / Option F has provisional production acceptance until owner-run P1/P2 gates pass.
- **Wrappers:** venv checks; scoped activation; `SETLOCAL`/`ENDLOCAL`; explicit `.venv\Scripts\python.exe`; `%*` forwarding; AutoRun checked; `SAFE_ARG`. The coordinator refuses to start unless `VIRTUAL_ENV` and `sys.prefix` match the project `.venv`. `.bat` files are stored with CRLF.
- **Concurrency:** 1-6 workers, default 6; one BLAS thread per worker; no nested pools.
- **Dependencies:** `install_upgrade_dependencies_into_venv.bat` is the sole package list. **After every upgrade, stop** until the offline suites, numerical and N-1 tests, the W-suite including W-23 and all E_1 goldens pass; goldens are never recalibrated. No upgrade between freezing and scoring, or within Mode H. The venv is Python 3.15.2 (owner, 28 October 2026); the old 3.14.10 venv is kept as `venv.bak` as the fallback. The owner's data tools have not yet been run under 3.15.
- **Timing (owner, 24 Oct):** `POLL_SECONDS_DEFAULT/MIN/MAX` = 1.0/0.5/5.0; `PIPE_EOF_WAIT_SECONDS` 5.0; `RELEASE_POLL_SECONDS` 0.5; `RELEASE_WAIT_SECONDS` 15. The protected 3 s termination waits stay.
- **Process termination (Architecture 5C, protected):** psutil only; no Job Objects; no `taskkill`, no kill by name, no fresh PID lookup. Ownership is proved by ancestry captured while the wrapper root is alive (PID plus creation time). **Strict no-status/no-kill.** When uncertain, leave the process and report `UNVERIFIED` / `ORPHAN_SUSPECTED`.
- **Orphan marker rule (owner, binding):** if anything is unconfirmed, the coordinator publishes the no-overwrite, fsynced `transitory_data/poc_runs/UNRESOLVED_ORPHAN.json`. **Any entry at that path blocks all launches for both games. Only the owner's approved manual clearance procedure clears it. No chat ever clears, bypasses or suggests bypassing it.** The contract runner and `read_run` read it from a fixed location; no caller can point them elsewhere.
- **Failed-group firewall:** results of FAIL or orphan-suspected groups are never consumed. A method cannot issue its own coordinator receipt. Contract runs are consumed only through `read_run`, which establishes its own gates.
- **The switches stay False:** `ENABLE_PROCESS_TERMINATION`, `ENABLE_SCIENTIFIC_COORDINATION`, `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE`, and since CODE-2 `ENABLE_CONTRACT_REAL_DEVELOPMENT`. No CLI override. Only the owner flips one, after reviewed tests. The scientific result-consumer allowlist `_COORDINATED_SCIENCE_ALLOWLIST` is empty.
- **No-clobber publishing:** contract records are published create-only with `os.link` from an fsynced temporary file (fails on any existing name; fail closed where hard links are unavailable); legacy frozen results use `os.rename`; never `os.replace` for frozen output.
- **No caller-chosen authority** (the reviewer's E2RC2-CODE-B01/B02): no public function takes a parameter that locates safety evidence (orphan marker, registry, method folders) or chooses the execution path. Tests patch module constants in-process through one harness helper.
- **Testing order:** non-destructive tests first; destructive tests one at a time, each separately approved.

---

## 6. Verified technical facts (reuse rather than re-derive)

- The Windows venv `python.exe` is a redirector (CPython `PC/venvlauncher.c`): `Popen.pid` is not the interpreter's PID.
- Windows does not kill children when the parent dies; `TerminateProcess` is asynchronous.
- A `.bat` launched via `Popen` runs under `cmd.exe` with CMD argument parsing (gh-114539): hence `SAFE_ARG` and `%*`.
- The `Run_Experiment.bat` process tree is root `cmd.exe`, a pipe child `cmd.exe` plus `findstr.exe`, a pre-check redirector plus interpreter, then the experiment's redirector plus interpreter. The allow-list is `cmd.exe`, `findstr.exe`, `python.exe`.
- psutil 7.2.2: `children(recursive=True)` filters by creation time against the root only (hence the per-edge check); `kill()`/`terminate()` check PID reuse; `Process.wait()` on Windows has no reuse check.
- `O_NOFOLLOW` does not exist on Windows; symlink refusal there relies on `is_symlink()`. NTFS hard links: the reader's `st_nlink != 1` refusal passes on the owner's drive. The owner's account cannot create symlinks (WinError 1314), so **three** symlink tests skip on Windows (reader contracts, exit receipt, and CODE-2's dangling-symlink test); the suite runner allows exactly those.
- Line endings: Git stores `.md` and `.py` as LF; `.bat` is `text eol=crlf`; `source_data/**` is `-text`. `git archive` applies the `.bat` rule, so hash `.bat` files from `git show`.
- **Python 3.15 makes UTF-8 the default text encoding (PEP 686).** No effect on the project's tests so far.
- **Reference figures** (fair-draw model, context only, never a veto): Powerball main matches mean 1.4, SD 0.9604; P(>=4) = 0.01826; P(>=5) = 0.00121; Powerball 0.05 per draw. Oz Lotto main-match mean 49/47.

---

## 7. Implementation status at the baseline

### 7.1 Installed packages (the register has each one's full record)

| Commit | Package | In one line |
|---|---|---|
| `c542483` | Package 2 v0.11-r1 | Multi-game reader, profiles, launch, receipts, synthetic scorer (register v0.5) |
| `ae76c29`, `d36735d` | Integration; effective commit | Ranking measures integrated; the new roles (registers v0.5, v0.6) |
| `744afea` | TH-1 | T-05 hardening, AST anchor, split link tests (register v0.6) |
| `908db9e` | DOC-2 | E2R-1 v0.3r3 and register v0.7 (two-commit one-off exception; register v0.8) |
| `52ebeaa` | NAMES-1 | Stable file names (register v0.9) |
| `295118d` (+ `c1159c7`, `1b23fd9`) | E1-ALIGN | E_1 into `src/methods/E_001/`; shared encoding; symbol-aware firewall (registers v0.10, v0.11) |
| `205ae73` | E2R-CODE-1 v2 | The contract library: records, registry, task, forecast, receipts, installed contract data (registers v0.11, v0.12) |
| `ced9b6c` | E2R-CODE-2 v3 | Dispatch gate, standalone contract runner, create-only publication, `read_run`, E_1 wrapper, legacy-runner gate, refusing coordinator entry point; register v0.13 (register v0.14) |
| `7c93320` | E_6 package v2 | E_6 revision 1, per-number Beta-Bernoulli with three fixed forgetting variants, installed non-runnable; the new-method template draft 1; register v0.15 (register v0.16) |
| `5b9edb4` | E_3/E_4 package v1 | E_3 and E_4 revision 1, exact polynomial fits (value and slope at the target) with the shared helper `polynomial_fits.py`, installed non-runnable; register v0.16 (register v0.17) |
| `947c370` | Wave 1 package v1 | E_7, E_8, E_9 and E_10 revision 1 with the shared helper `occurrence_counts.py`, installed non-runnable; template draft 2; register v0.18 (register v0.19) |
| `b61b1a2` | Wave 2 package v1 | E_2, E_17 (Method A), E_18 and E_19 revision 1 with the shared helper `recurrence_gaps.py`, installed non-runnable; template draft 3; register v0.19 (register v0.20) |

Document-only installs: `be18548` (DOC-1), `ee62eb6` (DOC-3), `040f80e` (DOC-4), `b846519` (register v0.12), `337b5b2` (DOC-6: H-1 v1r4, H-2 v1r5, register v0.14; four duplicate zips removed at `f9de54a`), `8defe9d` (DOC-7: H-1 v1r5, H-2 v1r6, register v0.17).

### 7.2 Module map

| Path | Responsibility |
|---|---|
| `src/methods/_common/game_profiles.py` | Frozen era profiles and capabilities |
| `src/methods/_common/game_draws_reader.py` | Orchestration-owned master, ledger and INIT verification; prefix-only `DrawView`; schema and digest. **Highest isolation sensitivity** |
| `src/methods/_common/canonical_encoding.py` | Shared canonical bytes and length-prefixed tuple encoding |
| `src/methods/_common/contract_vocab.py`, `contract_records.py`, `contract_task.py`, `contract_forecast.py`, `contract_receipts.py`, `contract_registry.py` | CODE-1: the contract vocabulary, record validators, method task, forecast assembly, receipts and the installed registry (`InstalledRegistry`, canonical bytes, fresh copies) |
| `src/methods/_common/contract_data/` | Installed declarations and hash-chained registry entries (282 files) |
| `src/methods/_common/contract_dispatch.py` | CODE-2: `dispatch_gate`, `legacy_gate`, `variant_released`, `active_pins`; the one refusal text |
| `src/methods/_common/contract_publication.py` | CODE-2: `create_only`, `RunPublication` (always STANDALONE), `read_run`, `run_disposition` |
| `src/methods/_common/contract_runner.py` | CODE-2: `run_contract_method` and the switch `ENABLE_CONTRACT_REAL_DEVELOPMENT = False` |
| `src/methods/Method_Contract_Runner.py` | CODE-2: the command line (`pins`, `run`); `ADAPTERS` maps a method ID to its adapter: E_1, E_2, E_3, E_4, E_6, E_7, E_8, E_9, E_10, E_17, E_18, E_19 |
| `src/methods/contract_adapters/e_001.py` | E_1's contract wrapper: compute through E_1's own function; verify label-for-label equality |
| `src/methods/E_006/` | E_6: `beta_bernoulli.py` (exact Beta-Bernoulli with forgetting; the variant table) and `contract.py`; flag present |
| `src/methods/_common/polynomial_fits.py` | Shared helper for E_3 and E_4, revision 1: exact least squares, interpolation and minimax, each with a second algorithm or certificate for verify() |
| `src/methods/E_003/`, `src/methods/E_004/` | E_3 and E_4: `variants.py` (the same six-row table) and `contract.py` (scores p(0) and p'(0)); flags present |
| `src/methods/_common/occurrence_counts.py` | Shared helper for wave 1, revision 1: window counts, decayed counts and period counts, exact, each with a second route |
| `src/methods/E_007/` .. `src/methods/E_010/` | Wave 1: `variants.py` and `contract.py` each (E_7 Beta shrinkage, E_8 hierarchical periods, E_9 decayed counts, E_10 two-window contrast); flags present |
| `src/methods/_common/recurrence_gaps.py` | Shared helper for wave 2, revision 1: appearances, gaps, censored exposures by age, age bins, and the certified log-age sign by two routes (the second with its own exact-zero test; a 1,024-term refusal cap) |
| `src/methods/E_002/`, `E_017/`, `E_018/`, `E_019/` | Wave 2: `variants.py` and `contract.py` each (E_2 interval alignment, E_17 binned hazard and Method A's log-age sign, E_18 four-law mixture with a KKT certificate, E_19 per-number periodic factor); flags present |
| `src/coordinator_private/contract_coordinated_gate.py` | Runs the dispatch gate, then always refuses `COORDINATED_CONTRACT_DISPATCH_NOT_ENABLED` |
| `src/methods/E_001/` and `src/methods/E_001_Historical_Appearance_Frequency.py` | E_1's modules and its legacy entry file (now gated by `legacy_gate`) |
| `src/methods/_common/multigame_method_registry.py`, `multigame_standalone_contract.py`, `multigame_coordinated_manifest.py`, `multigame_result_registry.py` | Package 2 roster (now a roll-up of the installed registry), standalone and coordinated manifests, result firewall |
| `src/methods/_common/multigame_console_protocol.py`, `multigame_worker_launch_handshake.py`, `multigame_ancestry_release.py`, `src/coordinator_private/multigame_coordinator_exit_receipt.py`, `multigame_launch_spec.py` | Launch, console, ancestry release and the coordinator-only receipt |
| `src/Powerball_Experiment_Coordinator.py` | The coordinator; 11 protected functions AST-identical to v0.6 (`2e23d550...`) |
| `src/coordinator_private/multigame_windows_lifecycle.py` | Windows synthetic lifecycle; gate False; **never run; needs a full review before any gate** |

**The eleven protected coordinator functions:** `accept_ancestry_candidate`, `check_exited_worker_for_orphan`, `departed_members_check`, `read_status`, `record_unresolved_orphan`, `register_root`, `require_no_unresolved_orphan`, `save_new`, `status_and_result`, `status_orphan_evidence`, `terminate_owned_tree`.

### 7.3 Powerball E_1 (accepted; frozen; revision 1)

- Entry file `src/methods/E_001_Historical_Appearance_Frequency.py`; modules in `src/methods/E_001/`; tests `tests/test_e1_standalone.py`, `tests/test_e1_align.py` and the frozen fixture `tests/p3_e1_synthetic_v0_3.json`.
- **Ratified goldens (R2 5.5 / TIE v0.2):** synthetic training view `df21871f8067e5405b4fdb1eec50c65dddbaa35958872bad3230d3c10a791fd4`; synthetic MAIN label-3 tie `7ce5ab1bae014adf61f1f02dd152d4b500cb405b65cb3886cdcee8dd9e2c9932`; synthetic canonical forecast `7b43d659d611791deb14d106a72984f153d9f79cc63b3d25000365de4c811d1e` (fixture target 1152).
- **Real target 1577, forecast-only:** view `d47fbbd6e60e6abc429fb74f47d8bbeafc6560152c2ecddb3b75d79932df4339`; legacy canonical result `7f1130872b3afaa222ff4e8c2396cd2c2872583544dfa6b31cc5a07cd067164e`. The standalone-runner synthetic pair `3851fa46...` / `8a7f917a...` is a separate, distinctly labelled set.
- The legacy entry file has `ENABLE_REAL_HISTORICAL_DEVELOPMENT = True` since `fbb66ef` (24 Oct): the reviewed gate for E_1 standalone historical development under D3 (holdout sealed, no FINAL, no termination). It authorises nothing beyond D3, and no new real-data run without a separate owner gate. Since CODE-2 it also refuses unless E_1's release holds (D2-3).
- E_1's contract path (`contract_adapters/e_001.py`) is synthetic-only: E_1's multi-game function accepts only `SYNTHETIC_CONTRACT_TEST` data.
- Frozen **forecast** outputs (predictions from pre-1577 draws, not outcomes): TOP `[9,17,7,11,18,30,12]` with PB 2; WORST `[31,13,8,29,26,33,35]` with PB 12. Never read a 1577 outcome to check them. No golden is ever updated to make code pass.

### 7.4 Tests

- **299 offline tests in 21 modules** at `b61b1a2`: 84 earlier, 54 CODE-1 (`test_e2r_contract` 53 including the six-worker T12, `test_e2r_prefix` 1), 52 CODE-2 (`test_e2r_dispatch` 18, `test_e2r_runner` 34), 20 E_6 (`test_e6_beta_bernoulli`), 19 + 13 E_3/E_4 (`test_polynomial_fits`, `test_e3_e4_polynomial`), 8 + 18 wave 1 (`test_occurrence_counts`, `test_wave1_frequency`) and 12 + 19 wave 2 (`test_recurrence_gaps`, `test_wave2_recurrence`). The suite runner `RUN_W2_SUITE.py` (inside `exchange/EX_076_Claude/W2_Install_v1.zip`) runs each module and compares its count; Windows allows only the three symlink skips. Results: Linux (Claude, Python 3.13.17 and a 3.15.0b4 venv with the project's dependencies) 299 pass; Windows (owner-reported, Python 3.15.2, 30 October 2026) 299 pass with 3 symlink skips, before the commit, for both waves.
- Manual form: `PYTHONPATH=src:src/methods:tests python -m unittest -v <module>` (Windows: `set PYTHONPATH=src;src\methods;tests`).
- E2R-T12 starts up to six ordinary Python worker processes that finish normally; it needs the owner's approval for each run context (approved for the rehearsals and installs of CODE-1, CODE-2, E_6, E_3/E_4, wave 1 and wave 2). Read every test before running it; a name or an "offline" label is not proof that it is safe.

### 7.5 Owner-run tools and data (Claude wrote the tools; do not rewrite or invoke them)

- `src/two_site_results_check_v0_7.py` (`69cb1decb1a1fed4077ccb41b91607405805721795992f57f302ae6618759aed`) and `src/results_master_v0_1.py` (`3436da9f560172606f4b9e010cd85a806b58e55597685f2ab7f65c3e17523619`) with `Run_Results_Updater.bat`. `update` has never been run and is not authorised.
- Masters: Powerball `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8` (last row 1576); Oz Lotto `4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f` (last row 1693); each ledger holds only INIT version 1.
- Reviewed orphan utilities in `transitory_data/`: do not modify.
- `src/GAIS/GAIS_results_fetcher_comparer.py` was deleted (`a52ffd8`); never revive, run, import or adapt it.

### 7.6 Not tested by anyone

Windows wrappers, venv activation and exit flow; `Run_Experiment.bat Method_Contract_Runner.py` on Windows (only the tests have run there); NTFS symlink semantics; console Ctrl+C and timeouts; process lifetimes and decoys; the synthetic Windows lifecycle; P1/P2 destructive probes; the owner's Windows dependency suite; the owner's data tools under 3.15; real scientific scoring; any real-data contract run; Mode H; FINAL; online acquisition; any gate-enabled coordination. The `DrawView` split is reviewed discipline, not OS sandboxing.

**Deferred optionals:** resolved-path containment under `source_data`; a full review of `multigame_windows_lifecycle.py` before any lifecycle gate; the diagnostic-only command-line option (E2RC2-O01; comes with the first method that declares a diagnostic record).

---

## 8. How to work as primary designer and coder

### 8.1 Workspace

- Work in disposable scratch trees, never on the owner's checkout. Build a tree with `git archive <base>` or a fresh clone, apply your overlay, and run everything there.
- Unpack every received zip into its own fresh directory; keep your scripts elsewhere; run Python that reads untrusted files with `-I`.
- Never let a tool print a quarantined row or the R1 draw-1587 paragraph. When reading master data for a non-outcome fact, print only the fields needed.
- The cloud sandbox cannot reach lottery sites and must not try.

### 8.2 Design before code (HIGH work)

- Write the design (or the specification change) first and give the reviewer a design-stage review and the chance of a competing design (R-3) before writing code. The owner ratifies any schema or rule change before code depends on it. A speculative candidate built alongside the design is fine, but it is reviewed only after the design passes unchanged (agreed in EX_038 and applied in E2RC2-RD-03).
- Plan the oracles up front (R-4): invariants, exact-arithmetic checks or independently designed fixtures that give real extra assurance. Proportionate, never decorative.

### 8.3 Your own first tests

- **Mutation checks, within safe limits:** for each safety property, plant a defect in a disposable copy and show a test fails; ship the mutation tool and its output. Never mutate installed files, a live switch, real master or holdout inputs, or live process controls. A test that cannot fail is not evidence.
- For any statistical claim (calibration, exactness, independence), build the smallest exhaustive toy that could break it and enumerate it exactly with `fractions.Fraction`.
- Never "refresh" an expected hash. A mismatch is investigated, not accommodated.
- Run the suite on Linux on the project's Python line (3.13 and a 3.15 build), and the install run-through in LF and CRLF clones of the current `main`, before sending.

### 8.4 The handback package

Include: the work-item card; base commit; `repo_overlay/` with a SHA-256 manifest; the exact diff of every changed file; test commands and full outputs; environment versions; mutation evidence; the DECIDED / RECOMMENDED / OPEN record; the not-tested list; a holdout statement; owner-run Windows instructions written as instructions, never as claims of execution; and a paste block or EX message for the reviewer. Derive every count in the instructions (tests, files, allowed skips) from the tools themselves, not by hand.

### 8.5 Document work

- Prepare a **new candidate edition** from the exact ratified Git blob with narrowly scoped, counted replacements (each old string asserted to occur exactly once), in a builder script that travels with the candidate, and submit the candidate and its diff for review. Finalising after ratification changes only the status line. Never overwrite the installed edition.
- **Registers:** each edition adds one section for its events, ends with its out-of-date statements, and records install results only after installation, never predeclared.
- **Handovers** may be restructured and shortened (as this edition is); when they are, list what was dropped and where it now lives, so the reviewer can confirm nothing binding was lost.
- **Copy agreed wording verbatim.** Check mechanically: every ID present; protected blocks byte-identical; inserted characters ASCII; LF and a single final newline.

### 8.6 The Claude Code local runner

- **Where:** `CLAUDE_CODE_WORKING_FOLDER_TREE/` (rulebook `CLAUDE.md` v0.2; `inbox/` task files; `outbox/` reports; `tools/`; `scratch/` ignored by Git). The root `CLAUDE.md` pointer and `.claude/settings.json` (no web access, no bypass mode, Git writes and data-folder reads denied) were committed by the owner at `ee76fc0`.
- **Tools** (`tools/`): `cc_clone.py` (`make` a task clone from GitHub with its remote removed and a refusing pre-push hook; `guard`; `unzip` with a SHA-256 check; `overlay`, new files only plus named tracked files with `--replace`; `git` with the guard before and after; `remove`; `commit-report`, which commits one report file in the main repository); `check_module_origin.py` (imported modules and contract data come from the clone); `run_e2r_suite_without_t12.py`.
- **How a task runs:** Claude writes `inbox/TASK_Tnnn.md` with every command in full, the expected PASS line of each step, a clean-up step and a report step, and commits it with any tool change. The owner pulls, **starts a new Claude Code conversation** (a running one keeps the old rulebook), and types `Do inbox\TASK_Tnnn.md`. The runner commits `outbox/REPORT_Tnnn.md`; the owner pushes; Claude reads the report from GitHub. A STOP is a STOP.
- **Use it** to rehearse a code package on the owner's Windows machine before the real install (T003 for CODE-1, T004 for CODE-2, T005 for E_6, T006 for E_3/E_4, T007 for wave 1, T008 for wave 2), when the owner wants that. Check that the task's tools fit the package's shape (for example replaced files) before writing the task. Make each new task from the last one by counted edits.
- **Never ask the runner to count or filter output** (T005: it redirected status output to a file outside the repository to count it, and could not delete the file). Ask for the whole output in the report, and count it yourself from the report.

### 8.7 Rebuilding a package

The cloud workspace does not persist. Every EX package from Claude carries its builder (or a diff to the previous builder), the register builder, the verifier template where it changed, the end-to-end test script and the evidence; the base is a Git commit. For CODE-2: `exchange/EX_038_Claude/` (first builder, verifier template, e2e script), `EX_040_Claude/` (verifier template v2, base snapshot), `EX_042_Claude/` (v3 builder, code diff), `EX_044_Claude/` (builder with the register; `make_register_v13.py`) and `EX_046_Claude/` (final builder diff, final zip). The mutation tool is installed as `review/E2R_CODE2_Install_v3/tools/e2r_code2_mutations.py`. For E_6: `EX_050_Claude/` (first candidate, base snapshot), `EX_052_Claude/` (v2 candidate, builder, register v0.15 builder) and `EX_054_Claude/` (final zip). For E_3/E_4: `EX_055_Claude/` (candidate, builder, base snapshot `BASE_7c93320_src_tests.zip`, register v0.16 builder) and `EX_057_Claude/` (final zip). For wave 1: `EX_061_Claude/` and `EX_063_Claude/` (design, reference script, template draft 2 builder), `EX_065_Claude/` (candidate, builder, verifier template, base snapshot `BASE_7462ea9_src_tests_template.zip`, register v0.18 builder) and `EX_067_Claude/` (final zip). For wave 2: `EX_068_Claude/`, `EX_070_Claude/` and `EX_072_Claude/` (design v0.1, v0.1r1 and v0.1r2 with their builders, the reference script and probes), `EX_074_Claude/` (candidate, builder, verifier template, e2e script, base snapshot `BASE_8f44d50_src_tests_template.zip`, register v0.19 builder) and `EX_076_Claude/` (final zip). Their mutation tools, method and contract-data generators and template builders are installed under `review/E6_Install_v2/tools/`, `review/E34_Install_v1/tools/`, `review/W1_Install_v1/tools/` and `review/W2_Install_v1/tools/`. A new chat can rebuild a package from these and check it against the recorded hashes.

### 8.8 Lessons from Claude's own errors (keep them)

- Check IDs mechanically **and** search for rules without IDs (consolidation: dropped invariants; a miscount).
- State the exact conditions of every "exact" or "calibrated" claim (Sidak instead of Bonferroni; over-broad calibration claims; scored-set selection).
- When the reviewer leans towards suppressing a number, propose labelling instead.
- Scan every script you write for non-ASCII; the file tool can turn `\uXXXX` escapes into literal characters.
- Verifiers: normalise CRLF or use Git's view; give every revision a distinct zip and folder name; read the install log's paths before saying it is safe to commit; commit, check, then push (N1I-C01).
- Any fixture meant to be valid gets its own test proving the reader accepts it; split platform-dependent checks into subtests and skip only what cannot run (TH-1).
- **Static guards must be symbol-aware**, and "nothing else changed" is proved with a frozen exact allowlist of edits, not regex categories (E1-ALIGN).
- **Count before claiming**; compute every hash with a tool and copy it.
- **Shell pitfalls:** `open(p,'wb').write(open(p,'rb').read())` truncates first; an unquoted heredoc expands backticks; `git archive` converts `.bat` to CRLF; never `rm -rf` the shell's own directory.
- **Never let a caller choose safety evidence** (E2RC2-CODE-B01, B02): a parameter "for tests" that points the gate at another orphan marker or registry, or that chooses the execution path, is a bypass. Never accept a caller's boolean that "the gates passed" (E2RC2-B02). Every launch path is under the release rule, including legacy ones (E2RC2-B01).
- **Prove create-only publication**, not "rename won't overwrite" (E2RC2-C01); tell a legitimate empty result from invalid output (C02).
- **Runner tools must match the API they inspect:** T001 stopped because a helper still used CODE-1 v1 attributes. Test task tools against the installed code first.
- **Counts in instructions come from the tools:** a hand-written "the two symlink tests" disagreed with the runner's allowance of three; a hand-written test count was wrong in CODE-1 v1.
- **The suite step before the commit has been skipped twice** (CODE-1 and E_3/E_4 installs; both recorded as departures, both run straight after the push and passed). Say plainly not to skip it, and put the suite command in the same command block as POST, not in a block of its own.
- **Mutation checks find real gaps:** "every variant computed as full memory" passed every E_6 test until a test computed each variant's own setting; a certificate accepting D + 1 alternations passed until a hand case was added. Plan one mutation per variant setting and per verification rule.
- **Do not pin lists other packages will extend** (E_6's test pinned the whole `ADAPTERS` list; the template trial caught it). Assert only your own entry.
- **Compute every worked example in a design note with a tool** (the E_3/E_4 draft had two wrong hand-worked values, caught before sending).
- **An owner decision given before the reviewer's formal reply** is recorded as OWNER-DECIDED, subject to revisiting if the review changes anything (D6-1..D6-5).
- **The owner sometimes saves files into the repository**; a verifier's PRE then stops, or a rebase is blocked. Ask for downloads outside the repository (`E:\TEMP`) and for the reviewer's zips to be uploaded to Claude.
- **Assert the whole of a protected section,** not its heading and points (H1F5-C01: a note placed inside H-1's section 2A passed a builder that checked only part of it).
- **A score's ranking claims need their exact conditions** (W1-C01): the same strictly increasing function of each number's count over the same draws ranks like counting; count-only scores in general need not.
- **Changing a covariate is not ranking-preserving** (W2-B01, a BLOCKER): v0.1 of wave 2 claimed a least-squares slope on harmonic numbers ranks exactly as Method A's logistic slope on ln(age); the reviewer proved the reversal with an exact witness. Prove an equivalence, or search for a witness; never assume one.
- **Every loop that waits for a condition needs a proved exit for every input** (W2R1-C01): an interval narrowing until it excludes zero never does at exactly zero. Test exact zero separately, and add a cap that refuses as an error.
- **Hand-written test expectations go wrong too** (two in wave 2's first helper tests; the code was right). Compute them with a tool.
- **Run Python 3.15 checks in a venv with the project's dependencies;** a bare interpreter fails every module on `numpy` and `psutil` (wave 2, before the evidence run).

---

## 9. Adding a new method (the process from here)

CODE-1 and CODE-2 give every method the release gate, create-only publication, receipts and traceability. A new method needs only its own pieces, and starts from the template, `doc/METHOD_TEMPLATE/` (draft 3; README and checklist), as every method since E_6 has:

1. **The idea, in the owner's words:** what it looks at and what it predicts. Decide its identity: an existing catalogue method (E_2..E_62, now `FORMULA_OPEN`, variant `NOT_YET_SPECIFIED`), or a new identity E_63 or later, which is OPEN and needs an owner decision and a catalogue amendment first.
2. **A short specification** (Claude drafts; reviewer R-3; owner ratifies): the exact rule; its views and channels (UNORDERED_SET / OPERATOR_DRAWN_ORDER, dates or not); its variant ID; its outputs (ranking, TOP and WORST per channel, probability kind per channel, any diagnostic record); insufficient-history behaviour; whether it needs seeds (if so, the seed-policy package comes first); and its plain-English text (D-3). **Fix every variant's settings here, before code** (E2R-R14A). Check it against the owner's philosophy (section 2A): no number suppressed, no veto.
3. **One code package** (HIGH; R-2 reproduction; owner's Windows run): its folder `src/methods/E_<nnn>/` with `contract.py` and `IN_DEVELOPMENT.txt` (no entry file, D6-1), any shared helper in `_common/`, a `METHOD_DECLARATION_V1` and a `FORMULA_OPEN` registry entry for each variant in each game (generated by a script that travels with the package), the `ADAPTERS` line in `Method_Contract_Runner.py` (an edit to an existing file, listed and checked), synthetic tests including T-05 and each variant's own setting computed in the test, and mutation checks. The register text rides in the same round. It installs non-runnable, after a Claude Code rehearsal.
4. **Release** (a separate small reviewed package; the owner's two actions): delete the flag; append a `SUPPORTED` entry for the same declaration. Then the method can run through the contract runner, on synthetic data.
5. **Real data** stays a separate owner gate: `ENABLE_CONTRACT_REAL_DEVELOPMENT` is False (D2-2). Turning it on, the development walk-forward, preregistration and scoring are each their own reviewed, owner-approved steps.

**Keeping the template current** (owner, 30 October 2026): whenever a method's design, review, code or install shows something the template should say or do differently, in Claude's assessment or the reviewer's, Claude proposes the template update in the next package. It is reviewed like any other document, and its draft number goes up. Each method's handback says whether it found anything for the template.

E_6 proved the pattern; E_3/E_4 and waves 1 and 2 used it, each wave with a shared helper and a generator for its method folders and contract data, so several methods travel in one package. Template draft 3 folds in what they taught. The owner's Methods A and B (`doc/GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md`) are catalogue methods, not new E-numbers: Method A's predictor is E_17's `HAZARD_LOGAGE_SIGN_V1` (installed in wave 2), and its diagnostics A1-A5 are a later package after WF-1 (W2-3); Method B becomes E_45's specification in wave 3.

---

## 10. Next work, in order (planned; the owner decides each step)

1. **Done since v1r5:** DOC-7 (H-1 v1r5, H-2 v1r6, register v0.17); wave 1 with template draft 2; wave 2 with template draft 3; the rehearsals T007 and T008 (sections 7.1, 7.4, 8.6).
2. **Now:** this file, H-2 v1r7 (drafted by Claude on the owner's instruction, the previous reviewer chat having reached its maximum length) and register v0.20, in one document-only install; then the owner starts the new reviewer chat from H-2 v1r7 and its introductory blurb.
3. **Then, in the owner's order (30 October 2026; register v0.18; `exchange/OWNER_ROADMAP.md` lists every method):**
   - **releases and WF-1:** switch the installed methods on (small reviewed packages; D6-3), then the first real measured results over past draws, walk-forward, with the R3 scorer and its N1 fair-draw simulator. The seed policy and the NIST root are settled at WF-1's design (W2-8; R-004);
   - **wave 3,** look-alike past draws: E_27, E_45 (= Method B), E_26, E_28;
   - **the NL-means discussion** (`exchange/OWNER_REMINDERS.md` R-002);
   - **waves 4 to 11:** 4 E_5, E_11, E_15, E_14, then E_13, E_12 and E_16 each in its own package; 5 E_37, E_33, E_35, E_34, E_39, E_36, E_38, E_40; 6 E_23, E_25, E_20, E_21, E_22, E_24; 7 E_32, E_29, E_30, E_31; 8 E_41, E_42, E_43, E_44, E_46, E_47; 9 machine learning E_49-E_53 (a dependency change and the seed policy); 10 E_57, E_60, E_58, E_59, E_61, E_62; 11 E_54, E_48;
   - **the ensembles,** E_55 and E_56, last.
4. **Method A's diagnostics A1-A5,** with their simulated fair-draw envelopes, as a separate package after WF-1 (W2-3); they need the seed policy and a diagnostic report design.
5. **Releases** (D6-3), each a small reviewed package: E_6 full memory first, then the others when the owner wants. Even released, contract runs stay synthetic until WF-1's gate (D2-2).
6. **E2R-CODE-3, retirement tooling** (E2R-T15; D-5): kept by the owner. Needed before any method's second revision.
7. **Coordinated contract runs** (a later package; D2-1), when the owner wants many methods run together.
8. **Still permission-gated, each separately:** real-data contract runs (D2-2); new real-data scientific evaluation, including the E_1 development walk-forward and the R3 scorer on real draws; walk-forward preregistration; Windows lifecycle and destructive gates (P2 closure, ERR-R2-02 / Option F final acceptance); allowlist entries; ranking and in-sample engines (R3 17.13 stages 2-3); any Oz Lotto science; Mode H; FINAL and the production weekly loop.
9. **Housekeeping, owner's choice:** the data tools' first run under 3.15; later, delete `venv.bak` and Python 3.14; the owner tools' versioned names (OPEN-N2, deferred); the duplicate "(1)" copy of the Claude Code exploration note in `doc/`, which the owner may delete; the 10 older EX copies in `review/` (R-003).

**Genuinely OPEN questions** (do not disguise as decided): the first real Oz Lotto run; E_54 feed timing; each remaining `FORMULA_OPEN` method's formula; E_63 and later identities; walk-forward preregistration; Mode H storage; scientific allowlist activation; whether to scope the optional oracle prototypes (agreed position 10.3); which methods WF-1 runs first.

---

## 11. Gates that stay closed

This handover authorises nothing. In particular: no Windows lifecycle or destructive test; no real-data scientific evaluation; no real-data contract run; no holdout access; no Mode H or FINAL; no process termination; no switch change; no allowlist entry; no master update; no dependency upgrade; no lottery-results search; no network acquisition; no orphan-marker clearance by any chat; no commit by Claude outside `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`. The owner authorises each gate separately, after independent review.

---

## Appendix A. Identities (non-self-referential)

| Item | Identity |
|---|---|
| Agreed roles position v0.1r1 (ratified) | `doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md`, `7d572400b941ad423978a7542d6c32fb73c934f0057240dbc5138898112bd53b` |
| H-3 v1r1 | `doc/HANDOVER/AI_Roles_Transition_Record_H3_v1r1.md`, `8b01c57fd8804029906e1e9c87e8ecef18edb914a269e43a45dac90880703ce5` |
| H-2 v1r6 (current reviewer handover until v1r7 is installed) | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r6.md`, `db40f40ef22995fc65a949243001858f1d7d1285713c9954531ae6b601fc5616` |
| H-1 v1r5 (predecessor) | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r5.md`, `1214bd971058ddd6cc680526fd80375bdbbd6db17397e41ba4c14ae5467101e1` |
| H-1 v1r4 | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r4.md`, `2050e9363d841634ecf2a9c308d3efb1ed51b359fbdaf2aa3531a60eb1f1c16a` |
| H-1 v1r3 | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r3.md`, `ddf4de23b726b2abf55ffcab613f926b62775469076476f939288a278e6422fc` |
| Review-disposition procedure | `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`, `5067aa520990b8ccc8521a04f3581424100cdd94994f5b9e3cb9e37863685339` |
| Exchange protocol v0.4 | `exchange/README.md` at `63c19e7`, `b08d9e2b62daf1f435c5c02b8908e447c1bc790b28d1d92c2866f110846b2256` |
| Register v0.19 | `doc/RATIFICATION_REGISTER_v0_19.md`, `b3ae51fd162960b64a9d145a52646dceeb3aec5b91e4b359ad7166e5e4c8e6a0` |
| Claude Code rulebook v0.2 | `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`, `12b50a5cadda0d5cef73106b75ec31051fd1c6b4cbe80ddafa387bd49936f562` |
| CODE-2 install manifest | `review/E2R_CODE2_Install_v3/INSTALL_MANIFEST_SHA256.txt`, `75a0c1f4759a7b652e2c4dd35ff37ec8622bd939ca5dac883b6cf231e524b510` |
| CODE-2 final package | `exchange/EX_046_Claude/E2R_CODE2_Install_v3.zip`, `ec643ceab097ca69630594e42551a2c7c4fc5ef5b4d8e6e593a7489a694c6969` |
| CODE-1 final package | `exchange/EX_037_Claude/E2R_CODE1_Install_v2.zip`, `5a2b978c96d82e3159cc50e8c24a2f29a944a39d29b7452452f8b484b9a23a11` |
| E_6 install manifest | `review/E6_Install_v2/INSTALL_MANIFEST_SHA256.txt`, `a1426607bd4076d10fd53c44d1c55b0dc991e3259de5a6870df8b2cfb4f3ef1c` |
| E_6 final package | `exchange/EX_054_Claude/E6_Install_v2.zip`, `eea8e4442285a6569c9060f8076bbebef42a936acae63daf4d15eb1a5bcf3e29` |
| E_3/E_4 install manifest | `review/E34_Install_v1/INSTALL_MANIFEST_SHA256.txt`, `4855549182ab5e944d69ef1b7dd14f89f3c37da2a857e46c9ea1acf21d7785ce` |
| E_3/E_4 final package | `exchange/EX_057_Claude/E34_Install_v1.zip`, `9d9949d545dad0c32761e9d377f7e5c945a7b99a6909753b180eb56636ee15fc` |
| Wave 1 install manifest | `review/W1_Install_v1/INSTALL_MANIFEST_SHA256.txt`, `2126d8e069a705134799d1efdfac83878e0d87d4d1dab47416b528fb1027fd9f` |
| Wave 1 final package | `exchange/EX_067_Claude/W1_Install_v1.zip`, `51c81eb0757b92eff321ceb24227fa1ffcee976d5c5d72e1dd1df146d9da30c2` |
| Wave 2 install manifest | `review/W2_Install_v1/INSTALL_MANIFEST_SHA256.txt`, `9c2ad9fe2b40413ab689f0875e95044a3353aa0c7124dcbb5312b927935c8af7` |
| Wave 2 final package | `exchange/EX_076_Claude/W2_Install_v1.zip`, `57ef34b67b8aa6cc023c5ea3d78c2940ab1a9875c3141626c5016355da53c429` |
| Committed coordinator v0.6 (AST anchor) | `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b` (also `tests/fixtures/coordinator_v0_6_baseline/`) |

Older identities (D-1, ADD-2, reviewer handover v10, coder handover v1.1r1, the interim note, the Package 2 acceptance record, the review methods kit, the integration packages, NAMES-1 and DOC-2 manifests, earlier H-1 editions, checkpoint v4) are listed in H-1 v1r3 Appendix A, which stays in the repository.

## Appendix B. Changes in v1r6

v1r6 refreshes v1r5 in place. It changes no rule; where it states a rule, the ratified documents and the register prevail. Nothing in v1r5 was dropped except what is superseded below. v1r5's own change list stays in v1r5.

1. **Header and section 0:** baseline `b61b1a2`; the reviewer chat that reviewed v1r5 reached its maximum length, and Claude drafted H-2 v1r7 on the owner's instruction; the reading list starts with the introductory blurb.
2. **Section 1:** the new reviewer chat, with the same rights; the oversight status through W2-075-RD-04; EX_067 and EX_076 as for-the-record final packages.
3. **Section 2:** introductory blurbs saved next to each handover (owner, 30 October 2026). Section 2A is unchanged, byte for byte (the builder asserts the whole section).
4. **Section 4:** the wave 1 and wave 2 design notes and the Methods A and B proposal added; the template is draft 3; the register pointer moves to v0.20.
5. **Section 5.3:** the installed contract data (80 declarations, 202 chains, 282 files); W1-1..W1-6 and W2-1..W2-8.
6. **Section 7:** two installed packages and DOC-7; the module map adds both helpers and the eight method folders; tests are 299 in 21 modules, run on Windows before each commit.
7. **Section 8:** T007 and T008; rebuilding waves 1 and 2; six lessons added (H1F5-C01, W1-C01, W2-B01, W2R1-C01, hand-written test expectations, the 3.15 venv).
8. **Section 9:** the template's draft 3; several methods per package; Methods A and B placed.
9. **Section 10:** rewritten for the current position in the owner's order; the seed policy at WF-1 (W2-8); Method A's diagnostics after WF-1; "when E_2 and E_5 are taken up" is no longer OPEN.
10. **Appendix A:** current identities.

*End of H-1.*
