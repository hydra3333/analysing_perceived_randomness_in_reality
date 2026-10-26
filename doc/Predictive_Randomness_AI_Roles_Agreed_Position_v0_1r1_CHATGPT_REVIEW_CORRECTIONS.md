# Predictive Randomness - AI roles and transition: agreed position v0.1r1

**Status:** CANDIDATE FOR OWNER RATIFICATION. Until the project owner ratifies the arrangement **and the expressly designated effective commit or milestone in section 9 is reached**, the current roles stand: ChatGPT is primary coder and Claude is independent reviewer. Neither ratification nor this document grants any run, test, data-access, holdout, termination or Git permission.
**Date:** 26 October 2026 (Adelaide).
**Drafted by:** Claude, the earlier reviewer chat. ChatGPT review correction v0.1r1 pending owner ratification.
**Consolidates:**
- the discussion paper v0.1 (ChatGPT), `75af18cfac1250c4fe0afd18ef63024c05669596d432da189f654f8dfd0f0ca5`;
- Claude's response v2, `90f2461be10d4f42565c54ec46fb7052d228d47805a82729d6d4557d723cd02d`;
- ChatGPT's response to v2, `3e077fa51de1d66c2c7d9d82b96cf83b35bfd893ef47851158333e992b08363d`.

Every substantive position below reflects agreement by both models, including the section 8 **[Claude amendment]**, confirmed by ChatGPT in this review. The document remains unratified pending the project owner's decision.

## 1. Roles (the default, not a monopoly)

- **Claude** normally leads scientific and technical design, specifications, governing-document integration, primary code and its own first tests.
- **ChatGPT** normally leads independent scientific and technical review. It is free to propose competing designs, methods and hypotheses, and to do bounded coding, alternative implementations or tests when the owner assigns them.
- **The project owner** is the sole ratifier, execution authoriser and committer.
- Both models may challenge each other with evidence. Neither may override an owner-ratified decision.
- The owner can revise or reverse this allocation at any time. At practical package boundaries, the owner may consider whether independent review found material issues, whether original alternatives proved useful, and whether the division reduced or increased coordination overhead. No formal scorecard or trial gate is required.

## 2. Author and reviewer

1. Every consequential deliverable names its **author chat** and its **reviewer chat**, not just the model.
2. The required independent review is always by the **other model**. A second chat of the same model may add continuity or an extra check, but never counts as the independent review.
3. **Mixed authorship:** if one model's patch is reviewed and the reviewer then rewrites consequential parts, those parts go back to the other model for review, or are split into a separate package. Nobody approves its own mixed result.
4. **Work-item card** at the top of each handback, not a separate document. Its fields: item ID; lead and reviewer chats; base commit; input hashes; scope; risk tier; owner gate; evidence state.

## 3. Risk tiers and evidence

**HIGH, whatever the size of the change.** Any change that touches:
- normative or authority text in a governing document, or the ratification register;
- a protected block;
- a test golden or expected hash;
- a safety switch, gate constant or allowlist;
- reader, view or digest code;
- evaluator, scorer or tie code;
- anything under `source_data/`.

**LOW.** Comments, and formatting in non-normative text. These are still hash-recorded.

**The tier decides who must check. The scope decides how much checking is needed.** For example, a one-sentence register fix is HIGH, but a focused check of the text, its history and the hashes is enough.

**Every handback carries:**
- the base commit;
- the changed files with their hashes;
- the exact test commands and their outputs;
- the environment versions;
- an explicit list of what was not tested;
- a holdout statement.

Checkpoint files are kept at each package boundary. No vital state lives only in a chat.

**Evidence states are distinct and never synonyms:** IMPLEMENTED, TESTED, REVIEWED, ACCEPTED, COMMITTED.

## 4. Finding classes

**BLOCKER, CORRECTION, OPTIONAL and RECONSIDER.** A RECONSIDER finding asks the owner to revisit a ratified decision. It never blocks current work by itself, and the decision stays binding until the owner changes it.

Each finding cites the file and line, the failure scenario and replacement text. A style preference is never a BLOCKER.

## 5. Reviewer rights

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

## 6. Disagreement

- The usual sequence is: finding, author's reply, reviewer's response. If the point is still open, it goes to the owner as claim, evidence, counterexample or alternative, consequence if wrong, and recommended decision.
- The two-round limit applies to repeated argument over the same finding on substantially unchanged evidence.
- A materially new counterexample, or a newly located rule, opens a new scoped finding.
- Nobody withholds evidence to fit the limit, and settled questions are not re-litigated without new evidence.

## 7. Git and patches

AI sessions may prepare exact, hash-recorded candidate trees and reviewable patches in disposable workspaces, but do not push, create remote PRs, alter the canonical branch or publish releases. The owner controls final application and Git commit. The default transport may be a `git diff --binary` patch against the stated base, verified with `git apply --check` and applied by the owner before the owner's own commit. If `git format-patch`/`git am` is preferred, the owner explicitly accepts its author/committer metadata semantics and the required local temporary commits. Neither patch format constitutes acceptance or bypasses review.

No immediate choice of Git delivery format is required to ratify the roles; this can be a separately ratified tooling decision before the first new implementation package.

## 8. Data, holdout and test boundaries

1. **No lottery-results searches.** No project AI session, author or reviewer, searches for or fetches lottery results, results pages or draw news. The only exception is source acquisition that the owner separately approves for a specific purpose, outside method development. Accidental exposures are reported factually for the exposure record, never suppressed or asserted harmless.
2. **Offline tests and data:**
   - Existing owner-authorised nondestructive offline tests and frozen E_1 development-prefix forecast-only goldens may be reproduced within their current contract. Neither a method nor a test decodes, exposes or uses real target-or-later outcome fields forbidden by that contract; no holdout outcome is introduced. Whole-file integrity hashing without decoding remains permitted where already ratified. **[Claude amendment, confirmed by ChatGPT]** That hash is derived from target-and-later rows. It is provenance for orchestration only and never reaches a method, directly or inside any method-facing object (the Package 2 v0.11 B1 rule). Synthetic suffix-poisoning and N−1 invariance fixtures remain valid. Any new real-data computation, scientific scoring, network use, dependency upgrade, process-destructive test or holdout access needs its applicable separate owner approval.
   - The reviewer must **inspect how the test works before treating it as safe**; a test's title or `offline` label is not sufficient.
3. All earlier ratified rules stand unchanged. These include:
   - MR v0.5, "mark, never suppress";
   - PO-1..4;
   - strict N-1 isolation;
   - supplementaries for the evaluator's scoring only;
   - the synthetic-versus-real firewall;
   - the sealed holdout;
   - the no-status/no-kill and process-safety gates.

## 9. Transition sequence (atomic)

1. **Package 2 v0.11-r1, Option A, under the current roles:**
   - The exact ZIP (`7bddda746f56668fbc60af9826cee83c7fd95031dfd3c9b4b474641cc2734635`) and the coding chat's original blurb go verbatim to the **new Claude chat**.
   - It checks the hash and reviews as independent reviewer, including the B1/C1 closure checklist in Claude's response v2, section 6.
   - Any r2 is written by the current ChatGPT coding chat, unless the owner chooses otherwise.
   - The earlier Claude chat does **not** cross-check.
2. **MR integration, in parallel and not dependent on the role change:**
   - The new Claude chat applies C-v2-01 verbatim to produce v3.
   - The ChatGPT reviewer does a narrow check.
   - The owner ratifies and installs the five editions.
3. **Before the old chats retire:**
   - **ADD-2:** a knowledge-transfer note from the ChatGPT coding chat, covering the module map, non-obvious choices, current defects and uncertainties, Windows-only checks, untested paths and possible improvements. It supplements source review.
   - **D-1:** a short delta note from the earlier Claude chat, covering what has happened since reviewer handover v10.

   Neither becomes authoritative merely by being written. After D-1, the earlier Claude chat retires, except in exceptional circumstances.
4. **Prepare the handovers** against the accepted repository baseline:

   | Handover | Author | Reviewer |
   |---|---|---|
   | H-1 Claude primary | New Claude chat | ChatGPT |
   | H-2 ChatGPT reviewer | ChatGPT | Claude checks the facts; the owner alone checks the rights section, so the reviewee cannot narrow the reviewer's rights |
   | H-3 Transition record | Either | Owner-ratified |

5. **The owner names the effective commit or milestone.** The default is the commit that accepts Package 2 v0.11, or a later one the owner names. The owner ratifies H-1, H-2 and H-3, and installs them together. Earlier handovers are marked superseded for future roles and remain as evidence. There is no interval in which the old roles are disclaimed and the new handovers are absent.

## 10. Near-term work after the transition

Streams 0A and 0B (section 9, items 2 and 1) are not delayed by the role work.

1. **E_2-readiness specification** (MR v0.5 section 13 stage 1):
   - the contract-field schema, fields 1-7, and the acceptance list;
   - Claude drafts it, and ChatGPT does a design review and may propose an alternative;
   - the owner ratifies the schema before code.
2. **E_2-readiness offline code**, after that ratification:
   - schema types and validators;
   - registry status;
   - probability-kind validators;
   - IS capability as a declaration only;
   - separate product, mode and score status;
   - per-track provenance kept on the orchestration side;
   - the scorer-only post-outcome record type with no data path;
   - a migration rule.

   Tests use synthetic fixtures and the development prefix only. Review includes reproduction under R-2 and an R-4 oracle for T-05.
3. **Optional, owner-scoped reference-oracle prototypes** for exact-fraction division tables and sigma/tails. They may be built while the E_2 design settles. Promoting them into library code is a separate phasing decision, since MR section 13 places it at stage 2.
4. **Still permission-gated:**
   - new real-data scientific evaluation, including the E_1 development walk-forward and the R3 scorer on real draws;
   - Windows lifecycle and destructive gates;
   - method registration and science allowlist entries;
   - ranking and in-sample engines;
   - E_2-E_6 implementations;
   - Mode H and FINAL.

## 11. Owner decisions to ratify

- [ ] The roles in sections 1-8.
- [ ] The transition sequence in section 9, including Option A, and the effective commit (default: the Package 2 acceptance commit).
- [ ] Requests to the ChatGPT coding chat for ADD-2, and to the earlier Claude chat for D-1.
- [ ] Whether to scope the optional oracle prototypes in section 10, item 3.
- [ ] The Git transport (section 7), now or before the first new implementation package.

*End of document.*
