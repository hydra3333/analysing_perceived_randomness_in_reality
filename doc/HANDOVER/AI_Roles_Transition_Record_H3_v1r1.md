# H-3 - AI roles transition record - Predictive Randomness project, v1r1

**Document:** H-3 under the agreed roles position v0.1r1, section 9 item 4.
**Version:** v1r1 DRAFT, 27 October 2026 (Adelaide); applies the ChatGPT reviewer's C-TRANS-01, C-TRANS-02, C-TRANS-03 and O-TRANS-01. Drafted by Claude. The project owner ratifies; the ChatGPT reviewer chat checks the facts.
**Status:** DRAFT. It takes effect only when the owner ratifies it and installs it together with H-1 and H-2 at the transition commit. It records events and decisions; it adds no rule and grants no run, test, data-access, holdout, termination or Git permission.

## 1. What this records

The change of AI roles agreed in `doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md` (`7d572400b941ad423978a7542d6c32fb73c934f0057240dbc5138898112bd53b`; owner-ratified, committed at `4a45b70`):

| | Before the effective commit | From the effective commit |
|---|---|---|
| Primary designer and coder | ChatGPT coding chat | Claude (H-1) |
| Independent reviewer | Claude | ChatGPT reviewer chat (H-2) |
| Ratifier, run authoriser, committer | Project owner | Project owner (unchanged) |

All other provisions of the agreed position (sections 1-8) apply from the effective commit: author/reviewer naming, other-model independent review, risk tiers, evidence states, finding classes, reviewer rights R-1..R-7, disagreement handling, the Git rules and the data, holdout and test boundaries.

## 2. The effective commit

**Owner decision, 27 October 2026:** the effective commit is a **separate, later transition commit** that installs H-1, H-2 and H-3 together. It is **not** the Package 2 acceptance commit (the agreed position's default). The commit cannot name itself. Its actual ID is identified and recorded in post-push verification evidence, and may be entered in a later register edition. Register v0.5 defines the effective commit by the set of installed documents, not by a self-referential commit hash.

## 3. The transition sequence (agreed position section 9), as carried out

| Item | What happened | Evidence |
|---|---|---|
| 9.1 Package 2 v0.11-r1, Option A | The new Claude chat reviewed r1 (`7bddda74...4635`) on its parent v0.11 (`0e00e231...d74c`) as independent reviewer: PASS, 0 BLOCKER, 0 CORRECTION, 3 OPTIONAL. The earlier Claude chat did not cross-check. No r2 was needed. The owner accepted the code and installed it. | `review/Claude_Review_Package2_v0_11r1_v1.zip` (`5c2e84655dcfd1d3a24129c0d38a5996e2f14195e807def382ba2bdb7d545a29`); install commit `c5424839d8fc9d620bae132873e8594b5651d2ce`, 27/27 blobs verified by Claude |
| 9.2 Method-ranking integration | The new Claude chat applied C-v2-01 verbatim and the owner-approved line-4 wording (v3, `af0e3b81...5d324`). The ChatGPT reviewer's narrow check: PASS, no findings. The owner ratified v3 on 27 October 2026. The ChatGPT reviewer checked the installation status edits: the five editions PASS, with 1 CORRECTION (C-INSTALL-01: the verifier's `git status` could refresh `.git/index`), applied as package v1r1 (`154f54d8...d162`; only the verifier changed). The owner installed it. | `review/Independent_ChatGPT_Focused_Review_MR_Integration_Candidates_v3.md` (`1d01adea...a95d`); `review/MR_Integration_Install_v1/INSTALL_MANIFEST_SHA256.txt`; `review/Independent_ChatGPT_Focused_Review_MR_Integration_Install_v1.md`; install commit `ae76c29783856dbb9bf0076fabe0c3612340314e`, verified by Claude (10 files added, all blobs match) |
| 9.3 Knowledge transfer | **D-1** from the earlier Claude chat; **ADD-2** from the ChatGPT coding chat. Neither is authoritative; both are inputs to H-1. | D-1 `doc/HANDOVER/Claude_Delta_Handover_D1_since_v10_v1.md` (Git blob `ac6dda4f...a50c`); ADD-2 `review/ChatGPT_Coder_ADD_2_Package2_v0_11r1_v0_1.md` (`ebaff99f...f35b`) |
| 9.3 Retirements | The earlier Claude reviewer chat retired after D-1 (26 October). The ChatGPT coding chat retired on 27 October 2026, after ADD-2 and the Package 2 installation overlay (owner-reported). | Owner statements, 26 and 27 October |
| 9.4 Handovers | H-1 (Claude primary; author Claude, reviewer the ChatGPT reviewer chat: `review/Independent_ChatGPT_Review_Claude_Transition_Docs_v1.md`, 1 BLOCKER, 5 CORRECTION, 2 OPTIONAL, applied in v1r1; focused recheck PASS, `review/Independent_ChatGPT_Focused_Recheck_Claude_Transition_Docs_v1r2.md`); H-2 (ChatGPT reviewer; author the ChatGPT reviewer chat; Claude checked the facts (`review/Claude_Fact_Check_H2_v1_v1.md`: 3 CORRECTION, 3 OPTIONAL; rights block verbatim); H-2 v1r1 (`0f9a8a98a8a56231e2730891ed71f1d2ed0b4afb890458de94b03f61c45668b5`) applied all six; H-2 v1r2 (`53f3af3f0845ea8534e25e896ffc8790fe685a7df9ecad8f7d7e48cd53f234a2`) added section 3.1, recording the owner's reviewer-latitude decision (Claude's fact check: `review/Claude_Fact_Check_H2_v1r2_v1.md`, PASS with one footer erratum); the owner alone checked and ratified its rights section, including R-8..R-11, on 27 October 2026); H-3 (this record). | Paths in section 5 |
| 9.5 Installation | The owner ratifies H-1, H-2 and H-3 and installs them together at the transition commit. | The transition commit, verified by Claude after the push |

**Interval control:** the project owner reports that no code package was started, produced or accepted after the ChatGPT coding chat's retirement, through the date of this draft (owner-confirmed, 27 October 2026); only documents were worked on (the integration install and these handovers). Until the effective transition commit, the existing roles and gates remain in force. At installation, the project owner verifies and records whether any further intervening work occurred; if so, its author, reviewer and acceptance state are reconciled before the transition.

## 4. Supersession

- **Superseded for future roles** (kept in place as evidence; not moved or edited): `doc/HANDOVER/Claude_Reviewer_Handover_Predictive_Randomness_v10.md`; `doc/HANDOVER/Predictive_Randomness_ChatGPT_Coder_Handover_v1_1r1.md`; `doc/HANDOVER/Interim_Handover_Note_for_both_claude_and_chatgpt_v1.md`; `doc/HANDOVER/Claude_Checkpoint_v2.md`. Earlier versions in `doc/HANDOVER/superseded/` stay historical.
- **Inputs, never authority:** D-1 and ADD-2.
- **Unchanged and still in force:** the agreed roles position itself; `doc/HANDOVER/Package2_v0_11r1_Acceptance_Deferred_Work_v0_1.md` as a factual record (subject to the erratum in section 6); every ratified governing document and rule.
- Files are left at their paths so that existing references stay valid; the register records their status.

## 5. Installed together at the transition commit (proposed)

| Path | What |
|---|---|
| `doc/HANDOVER/Claude_Primary_Handover_H1_v1r1.md` | H-1 |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r2.md` | H-2 |
| `doc/HANDOVER/AI_Roles_Transition_Record_H3_v1r1.md` | H-3 |
| `doc/RATIFICATION_REGISTER_v0_5.md` | Records: the roles ratification; the effective commit (as "the commit that installs this edition with H-1, H-2 and H-3"); Package 2 v0.11-r1 acceptance at `c542483`; the integration installation; the out-of-date statements listed in H-1 section 4; the supersessions above. Drafted by Claude, reviewed by the ChatGPT reviewer (HIGH tier). |
| `review/` | The reviews of H-1, H-2 and register v0.5; the ChatGPT reviewer's check of the integration install package (`Independent_ChatGPT_Focused_Review_MR_Integration_Install_v1.md`) and its confirmation of C-INSTALL-01; `MR_Integration_Install_v1r1.zip`, the package actually used, as history |

## 6. Erratum

`doc/HANDOVER/Package2_v0_11r1_Acceptance_Deferred_Work_v0_1.md`, section "Accepted Package 2 code", names the installation hash file `EXPECTED_SOURCE_SHA256.json`. The actual file is `evidence/CLAUDE_EXPECTED_26_FILE_SHA256.txt` inside `review/Predictive_Randomness_MultiGame_Package2_v0_11r1_OWNER_INSTALL_OVERLAY_v0_1.zip`. The recorded hashes themselves are correct (Claude verified all 27 installed blobs). The file is not edited; this record corrects the reference.

## 7. Owner decisions still open after the transition

1. The Git transport for new implementation packages (agreed position section 7): the overlay-plus-verifier route used so far, or a `git diff --binary` patch. Decide before the first new implementation package.
2. Whether to scope the optional reference-oracle prototypes (agreed position section 10 item 3).
3. Owner decision already made (27 October): deferred test items P2-R1-O1 and P2-R1-O3 are **not** brought forward; they form the first package under the new roles.
4. **Owner decision, 27 October 2026:** from the effective commit, the ChatGPT reviewer chat holds the same latitude Claude held as reviewer from 23 October, to be used carefully: it settles routine review matters itself and labels them REVIEWER-DECIDED (the 23 October examples: deferrability, packaging and versioning, wording, whether a re-review is needed, test-policy choices, and confirmations the owner has already relayed); consequential items still go to the owner. Claude as author keeps only routine choices that affect no scope, acceptance or review gate (H-1 section 1.5).
5. **Owner instruction, 27 October 2026:** for the first three reviews under the new roles (the owner may change the number), Claude's response to each review lists every item the reviewer marked REVIEWER-DECIDED, checks each against the ratified compliance, safety and process rules (holdout and data boundaries, risk tiers and required reviews, test and evidence requirements, gates), and flags to the owner in plain English any that departs from them, naming the rule. This is reporting only: Claude does not overrule the reviewer or narrow its rights; the owner decides.
6. Owner ratification, 27 October 2026: H-1 v1r1, H-2 v1r2 (including R-8..R-11 and section 3.1), H-3 v1r1 and register v0.5, with the final mechanical edits recorded in `review/AI_Transition_Install_v1/`.

## 8. Owner ratification checklist

- [ ] H-1 ratified (after the ChatGPT reviewer's review and any revision).
- [ ] H-2 ratified (after Claude's fact check and the owner's own check of its rights section).
- [ ] H-3 ratified.
- [ ] Register v0.5 ratified.
- [ ] All installed together in one commit; Claude verifies every blob after the push.

*End of H-3.*
