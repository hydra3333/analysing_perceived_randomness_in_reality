# Claude fact check of H-2 (ChatGPT reviewer handover) v1, v1

**Work-item card**

| Field | Value |
|---|---|
| Item | Fact check of H-2 under agreed roles position v0.1r1, section 9 item 4 |
| Author of H-2 | ChatGPT reviewer chat |
| Fact checker | Claude (new Claude chat). Scope: facts only. **The rights sections (H-2 sections 2 and 3) are the project owner's alone to check; nothing here narrows or reinterprets them.** |
| Input | `ChatGPT_Reviewer_Handover_H2_v1.md`, SHA-256 `f083238376d9688639948ef1b8c227d08e15c3faaf6295fad05d94044ab1e420` (UTF-8, LF, 215 lines) |
| Repository checked | GitHub `main` at `ae76c29783856dbb9bf0076fabe0c3612340314e` (fresh fetch, 27 Oct 2026) |
| Risk tier | HIGH (authority text) |
| Evidence state | REVIEWED (facts) |

**Date:** 27 October 2026 (Adelaide). **Holdout statement:** no draw outcome was read or shown.

## 1. Verdict

**Facts: PASS with 3 CORRECTION and 3 OPTIONAL.** The corrections bring status lines up to date (the integration has since been installed) and fix two references; none touches a right. Recommend the ChatGPT reviewer apply them as H-2 v1r1; per the mixed-authorship rule, Claude does not edit H-2.

## 2. Checked and correct

- **Rights block (section 2):** the R-1..R-7 table, the oracle-subjects paragraph and the T-05 reference test (16 lines) are **byte-identical** to `doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md` (`7d572400...3b`), checked mechanically line by line.
- Roles, independence, mixed authorship, work-item card, risk tiers and the five evidence states (sections 1, 1.1) match the agreed position sections 1-3.
- The eight always-review triggers (4.2) match the owner's 23 October procedure.
- Package 2 facts: install commit `c5424839...`, 27/27 blobs, r1 `7bddda74...`, overlay `6e674f40...`, PASS 0/0/3, 58 OK with 1 skip, 11/11 ASTs, 96/96 probe, P2-R1-O1 and O3 deferred.
- MR facts: v1 `86f40744...355c` and B-01; C-01 and C-02 with their replacement text; v2 and C-v2-01 (the separately approved O-02 row-key clarification); v3 `af0e3b81...` and its PASS; install v1 `154924d8...` with the five edition hashes; C-INSTALL-01.
- B1 (`order_evidence.master_sha256`) and its closure in r1.
- Boundaries (section 6): consistent with the ratified rules and the owner's standing prohibitions (no lottery-results searches; holdout Powerball >= 1577, Oz Lotto >= 1694; no The Lott automation; never `oz.lotterywest.com`; no APIs, impersonation, bypass or new scraper; GAIS retired; the orphan-marker rule; owner-only Git). No owner name appears.
- The role-change file's authoring-time "candidate" header (line 15 claim): correct.
- Encoding: UTF-8, LF; non-ASCII only inside the verbatim rights block and three section signs (lines 157, 202, 209).

## 3. CORRECTION

**C-H2-01 - status has advanced: the integration is installed.** Lines 15, 171 and 183.
Failure scenario: a cold-start reviewer treats installed editions as unverified candidates, or believes C-INSTALL-01 is still open.
Facts: the owner installed package **v1r1** (`154f54d8afb8870c7e4cc613fc9f69d656f8d8bbfbe343cc924f1566c67cd162`), in which only the verifier changed (every Git call uses `--no-optional-locks` and `GIT_OPTIONAL_LOCKS=0`; overlay byte-identical to v1), at commit **`ae76c29783856dbb9bf0076fabe0c3612340314e`**. Claude verified from GitHub: exactly the 10 files added, every blob matching the manifest, predecessors unchanged.
Suggested replacements:
- Line 15, the sentence beginning "MR integration **v3 candidates...**": "MR integration **v3 candidates were separately owner-ratified** on 27 October after this reviewer's PASS. Installation package v1 was reviewed with one verifier-only correction (`C-INSTALL-01`), applied in v1r1 (`154f54d8...d162`), and the owner installed v1r1 at `ae76c29783856dbb9bf0076fabe0c3612340314e` (Claude-verified; not re-cloned by this reviewer)."
- Line 171, the final clause: replace "verify replacement install package/commit before treating these as operative" with "these were installed at `ae76c29...` (Claude-verified); confirm against current HEAD".
- Line 183, the "MR integration INSTALL v1 candidate" row: "`154924d8...ab36` (v1): five edition bytes PASS, C-INSTALL-01 raised; `154f54d8...d162` (v1r1): verifier corrected, installed at `ae76c29...`".

**C-H2-02 - the effective commit cannot be named inside H-3.** Lines 169 ("H-3 determines effective role date"), 192 (step 1: "Obtain ... `H-3` effective commit") and 212.
Failure scenario: a cold-start reviewer looks in H-3 for a commit ID that cannot be there, because H-3 is installed in that same commit.
Facts: H-3 section 2 defines the effective commit as the commit that installs H-1, H-2 and H-3 together; its ID is recorded in Claude's post-push verification and described in the register edition installed with it (v0.5).
Suggested replacements:
- Line 169: "**H-3 defines the effective commit** (the commit that installs H-1, H-2 and H-3 together)."
- Line 192, step 1 first sentence: "Obtain the actual clean HEAD and identify the effective commit as the commit that added H-1, H-2 and H-3 together (for example `git log --diff-filter=A --format=%H -- doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1.md`); establish that H-1/H-2/H-3 are owner-ratified, installed in that one commit and Git-blob verified."
- Line 212: "H-2's path, SHA-256 and review disposition are recorded in the register edition installed with it (v0.5); the installed commit ID is recorded in Claude's post-push verification, since no file can name the commit that contains it."

**C-H2-03 - path of the roles agreement.** Line 49 names `AI_Roles_Agreed_v0_1r1_RATIFIED.md`. The file is `doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md` (as line 169 correctly says). Replace accordingly.

## 4. OPTIONAL

**O-H2-01 - section numbers inside the verbatim block.** R-6 reads "RECONSIDER findings (section 4)". That is the agreed position's section 4 (finding classes); in H-2, section 4 is the review method and the finding classes are section 5. Keep the block verbatim, and add one line **after** it: "Section numbers inside this block refer to the agreed position; its section 4 (finding classes) corresponds to H-2 section 5." This changes no right.

**O-H2-02 - record the owner's scheduling decision.** Line 202: add "On 27 October the owner decided not to bring P2-R1-O1/O3 forward; they are planned as the first package under the new roles, subject to the owner's scoping of that package."

**O-H2-03 - identities for the inputs.** Line 173: add D-1 Git blob `ac6dda4f6f965637118dbf2811cb4006497006e10f7be72476e5acd64c37a50c` and ADD-2 `ebaff99f4fc34ce38099ac5581abada7a1d0ffd1d8a7b7bfe3a0ce5fbb41f35b`, and the ratification commit `4a45b70` (27 October 2026, 00:09 Adelaide) for the roles agreement at line 13.

## 5. For the project owner only: H-2 section 3 (proposed rights R-8..R-11)

Not assessed by Claude for scope; that is your decision alone. Facts only: each is labelled new wording for your ratification, each says it grants no authority to run, fetch data, change gates or commit, and none contradicts a ratified rule I know of. In plain terms they would let the reviewer: question the problem framing and propose different designs (R-8); ask for the evidence it needs and withhold an unqualified PASS when evidence is insufficient (R-9); decline an unsafe test and escalate an urgent BLOCKER, but never clear or bypass a safeguard (R-10); and report material findings outside a narrow scope, labelled as such (R-11).

## 6. Not checked

The rights' merits (owner only). Any statement about the ChatGPT reviewer chat's own environment or what it accessed (lines 17, 25-27 self-descriptions) beyond consistency.

*End of fact check.*
