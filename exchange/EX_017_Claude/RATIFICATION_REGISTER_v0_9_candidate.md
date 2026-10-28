# Predictive Randomness — Ratification Register

**Register version:** v0.9 RATIFICATION CANDIDATE (drafted 28 October 2026), recording the NAMES-1 installation, the move to Python 3.15 and H-1 v1r3; v0.8 OWNER-RATIFIED 28 October 2026, recording the DOC-2 and NAMES-1 installations, the NAMES-1 ratification and the owner decisions made after register v0.7; v0.7 OWNER-RATIFIED 28 October 2026, recording the E2R-1 specification ratification and the owner decisions of 28 October 2026; v0.6 OWNER-RATIFIED 28 October 2026, recording the records after the effective commit (its identity, the delivery method, the review-disposition procedure and TH-1); v0.5 OWNER-RATIFIED 27 October 2026, recording the AI roles transition, the Package 2 v0.11-r1 acceptance and the integration installation; v0.4 OWNER-RATIFIED 27 October 2026 (drafted 26 October 2026), adding the method-ranking integration; v0.3 OWNER-RATIFIED 26 October 2026; v0.2 OWNER-RATIFIED 24 October 2026. Historical ratifications are preserved and remain valid.
**Basis:** the historical owner decisions and approved handovers, with current committed files cross-checked by Claude at GitHub HEAD `1c7cfced` (24 October 2026). Ten other content hashes matched that HEAD; the Architecture hash below is explicitly corrected to the **actually committed** v0.5 content (unfixed §5C heading). The separately proposed one-line heading change and register v0.1 were **not committed**. The pre-integration consolidated editions below were owner-ratified 26 October 2026; only explicit OPEN/PROVISIONAL/RECOMMENDED subitems remain undecided. The v0.4 entries were cross-checked by Claude against GitHub HEAD `618fe48` (26 October 2026), the v0.5 entries against GitHub HEAD `ae76c29` (27 October 2026), the v0.6 entries against GitHub HEAD `b14116b` (27 October 2026), and the already-committed v0.7 references against GitHub commit `38fc60e` (28 October 2026). The E2R-1 v0.3r3 specification is not present at that commit; it is verified by its content hash below, and its installation is a separate owner decision. The v0.8 entries were cross-checked by Claude against GitHub commit `908db9ea9d4a37b17833f5d43919804c78ef7e14` (28 October 2026); the NAMES-1 specification and code, and the E1-ALIGN specification, are installed with register v0.8, in one commit, and are identified by content hash. For v0.9, historical predecessor references through commit `83d1515` (28 October 2026) were checked by Claude. The new Python 3.15.2 environment and the Windows results are owner-reported. H-1 v1r3 and register v0.9 are candidates pending owner ratification and DOC-3 installation, and are identified by content hash; the actual install commit and final blobs are verified separately after installation.  
**Authority:** This register records approvals; it does **not** independently ratify any document, authorise an experiment, or supersede an operative specification. If a historic document still says “draft”, “review candidate” or “not ratified”, its status at the time of drafting is historical. The later owner approval recorded here determines its current status.

## Current and historical ratification identities

SHA-256 below is computed from **UTF-8 Git-stored file content with LF line endings** (the canonical content represented by the source GitHub ZIP and ratified install artifacts), *not* from a Windows working copy whose checkout may have CRLF endings. The Architecture v0.5 hash below represents **actual Git-committed v0.5 content**, including the historical §5C heading. The corrected-heading version (`2d57f59afbd152ae80720e117dab5b9749ab3a611bf32ab1b14d3ed1be478acd`) was only proposed, never committed; Architecture v0.6 would replace it after ratification, without changing the v0.5 historical bytes. Hashes are immutable document-content identities, not Git commit IDs.

| Document (under `doc/`) | Authority and status | Owner approval date | Superseded by / qualifier | Git-content SHA-256 |
|---|---|---|---|---|
| `Predictive_Randomness_Research_Project_Proposal_v0_3.md` | Historical — OWNER-RATIFIED | 21 Oct 2026 | Proposal v0.4 | `04e061d13b69e49c0dc227b7093570e96598d4c416952ac6092af4d3d14d4b64` |
| `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` | Current — OWNER-RATIFIED | 21 Oct 2026 | — | `19809ae8a1aca716c6c6a4de71a37b705129304894a2b382036d51b76575b99f` |
| `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` | Historical — OWNER-RATIFIED | 22 Oct 2026 | — (R2 approved erratum v0.2 also applies) | `7ec4bad9ab00a619a42cedc4abbe4bec393589563d3bc3061ab4737525259d71` |
| `Predictive_Randomness_R2_v0_3_Approved_Erratum_v0_2.md` | Historical — OWNER-APPROVED narrow erratum | 22 Oct 2026 | — (ERR-R2-02 remains provisional pending P2) | `a08b4e7620be8cb32142b23146c5f82c415a50e56cba0b2ea3bed6e1a4b80d5e` |
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_2.md` | Historical — OWNER-RATIFIED | 22 Oct 2026 (ratified handback v0.2) | R3 v0.3 | `dd0b5243ad8f93a0de7c502e2e6ce54a99c5e427063ce7b3e49313fb18975800` |
| `Predictive_Randomness_Software_Architecture_Discussion_v0_4.md` | Historical — previously OWNER-RATIFIED | 23 Oct 2026 | Architecture v0.5 | `7526e381be93caa68ce8f8a6b90f135748925f1c0b080e171e1ef18cd771f257` |
| `Predictive_Randomness_Software_Architecture_Discussion_v0_5.md` | Historical — OWNER-RATIFIED | 23 Oct 2026 | Architecture v0.6 | `9889617f39be766a167856fdd171896c1ffb712aae8db4e78d6f3d861a345502` |
| `Predictive_Randomness_Windows_POC_Implementation_Task_Specification_v0_1.md` | Historical — OWNER-RATIFIED for P0–P2 | By 23 Oct 2026; precise date not independently established | Windows POC Task Spec v0.2 | `deeae27f846061d51555c3d89a77c8199941b74456520a98aa6501c504b85e5e` |
| `Predictive_Randomness_Windows_POC_Implementation_Task_Specification_v0_2.md` | Current — OWNER-RATIFIED | 23 Oct 2026 | — | `ca5e89dde7e9927974e759f1df115eefca03144de45e073c240aa9e13f24ebf1` |
| `HANDOVER/Predictive_Randomness_ChatGPT_Continuation_Handback_v0_2.md` | Historical — OWNER-RATIFIED | By 23 Oct 2026; precise date not independently established | Handback v0.4 | `53b33b6ddec5b874725b195d4c45e3295351915a6e8331e2d2eb56d4b8a28140` |
| `HANDOVER/Predictive_Randomness_ChatGPT_Continuation_Handback_v0_4.md` | Historical continuity — OWNER-RATIFIED | 23 Oct 2026 | — | `5093e446fb14bc281fecea1e722ee2bea366614dac9fb5192e36b96b63e603db` |

## Multi-game documents ratified 24 October 2026

| Ratified document | Authority and supersession | Git-content SHA-256 (UTF-8/LF) |
|---|---|---|
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_3.md` | OWNER-RATIFIED; supersedes R3 v0.2 for multi-game evaluation extensions | `69d61d162d8d46094c02c1aca36ba53b47e6aec56fe5552f3ef39687f07d0826` |
| `Predictive_Randomness_R2_v0_3_Erratum_Record_v0_3.md` | OWNER-APPROVED ERR-R2-05; preserves earlier errata, ERR-R2-02 still provisional | `f3be1b28bb156ec68207ad6cd614972bedcd2409519c9e8dd6a8751c41a5768e` |
| `Predictive_Randomness_Software_Architecture_Discussion_v0_6.md` | OWNER-RATIFIED; supersedes Architecture v0.5; existing safety conditions preserved | `99b8222b0d905fc45eda7723997aa9cfcbe7ba09a5b0b8d322b9eea3e766cea7` |
| `Predictive_Randomness_Research_Project_Proposal_v0_4.md` | OWNER-RATIFIED; supersedes Proposal v0.3 for multi-game scope | `1749889d4f02825b15a8f317e9620b2ab8b26908c41eda8611157c1675f089b5` |
| `Predictive_Randomness_MultiGame_Infrastructure_P3_Task_Specification_v0_1.md` | OWNER-RATIFIED new task specification; POC task v0.2 retained separately | `86c4d062cafab07595953e5447ec5ae5b287e0d98e2fa4ec35c1015e0fa052f4` |
| `contracts/TIE_SHA256_V1_Ratified_Encoding_v0_2.md` | OWNER-RATIFIED multi-game applicability; encoding unchanged | `045b784d16a4611ac4ba5e8af063733e957b0b9359882d52b7143b912a65a0b6` |

**Register identity:** this register cannot include its own SHA-256 without a self-reference. Its final file hash is provided in the enclosing installation manifest; update the register only in a later version after a corresponding owner decision.


## Method ranking measures and integration editions (26 October 2026)

In this section, "this register" means register v0.4, the edition that recorded the integration. Two documents were owner-ratified on 26 October 2026 at commit `ac01678`. Their authoring-time headers ("RATIFICATION CANDIDATE" / "CANDIDATE ... awaits owner ratification") are historical; the ratification recorded here determines their status, and the files are never edited to change those headers.

| Document (path under `doc/`) | Authority and status | Git-content SHA-256 (UTF-8/LF) |
|---|---|---|
| `Predictive_Randomness_Method_Ranking_Measures_Proposal_v0_5.md` | OWNER-RATIFIED 26 Oct 2026. Its content is integrated into the four editions below, owner-ratified 27 Oct 2026; the file is integrated history, kept unchanged. Versions v0.2-v0.4 are historical drafts. | `c6ca2cb2174ee2963a6fe33347820c80b92e6dd1eda518a1f0c8e3254d67ab19` |
| `HOLDOUT_EXPOSURE_RECORD_v0_2.md` | OWNER-RATIFIED 26 Oct 2026; factual, value-free record (6 items); supersedes v0.1 | `aec833fe031b6d1d73e6acbb81757b50b193425a6899c84d438431d9df4433e2` |
| `RATIFICATION_REGISTER_v0_3.md` | OWNER-RATIFIED 26 Oct 2026; superseded by register v0.4 (OWNER-RATIFIED 27 Oct 2026) | `99e75fbe1bc5cea34a7d2b1c456633815b88e340c4a05aab5fb671d624c7ec37` |

**Integration editions (OWNER-RATIFIED 27 October 2026).** Each is its ratified predecessor edited in place; every ratified ID and rule is kept, and the protected blocks are byte-identical.

| Integration edition (path under `doc/`) | Ratified predecessor | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md` | R3 v0.4 | OWNER-RATIFIED 27 Oct 2026; adds R3 section 17 (method ranking measures); `53e30a3e649b48b8a88923d08bf578caf04a4ce93d6ea6468891ca97e93a57b6` |
| `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_5.md` | R2 v0.4 | OWNER-RATIFIED 27 Oct 2026; adds R2 sections 2.5 (supplementary rule), 3.6 (numbering), 5.6 (stage-1 contract fields) and 8.4 (in-sample mode); `2c67db8fcba50e469b0490cd85caf2fe964b3b79fc17fe7da4ebf033b91d9a3e` |
| `Predictive_Randomness_Software_Architecture_Discussion_v0_8.md` | Architecture v0.7 | OWNER-RATIFIED 27 Oct 2026; adds Architecture sections 5A.4 (ranking tool launcher) and 12.5 (report tool, in-sample runs, N1); protected 5C unchanged; `32cf157d9ce8850e790274e962236f2be3b50a8bdee7ec94a28ba00d7fd452ec` |
| `Predictive_Randomness_Research_Project_Proposal_v0_6.md` | Proposal v0.5 | OWNER-RATIFIED 27 Oct 2026; adds Proposal section 2.7 (charter); supplementary sentence in Proposal sections 0 and 3.1; `6a281e05127e7db976a16557ba69006327a8d615c2b0ec90bb6b34ee1c648a73` |

**On owner ratification (given 27 October 2026):** the installation step changes the **five edition/status headers, including this register**, and all affected candidate-status and present-authority rows to OWNER-RATIFIED; it marks the pre-integration inventory explicitly historical, updates the R3 section 17.13 stage-0 integration status, recomputes the **four governed-document Git-content hashes** in this register and places this register's own SHA-256 in the external installation manifest. Claude verifies the resulting installed files against the committed Git HEAD. Historical hashes and decisions remain preserved. Neither ratification nor documentation authorises runs, Mode H/FINAL, holdout access, process termination or Package 2 scientific use. Unchanged by this integration: R1 v0.4, TIE_SHA256_V1 v0.2, P3 v0.2, the Windows POC Task Specification v0.2, the numerical reference v0.1, the E_1 legacy schema and goldens, the masters, the owner tools, the coordinator and Package 2 v0.11.

**Continuity documents:** from the effective commit, the current continuity documents are H-1, H-2 and H-3 (next section). Before it (commit `618fe48`, verified by Claude), the current handovers were `HANDOVER/Claude_Reviewer_Handover_Predictive_Randomness_v10.md` and `HANDOVER/Predictive_Randomness_ChatGPT_Coder_Handover_v1_1r1.md`. Reviewer handovers v2-v9, coder handovers v1.0r1 and v1.1, and the ChatGPT handbacks are in `HANDOVER/superseded/`; the interim note is in `HANDOVER/`. They are continuity records, not normative, and are superseded for future roles by H-1, H-2 and H-3.

## AI roles transition, Package 2 acceptance and integration installation (27 October 2026)

Paths in this section are under `doc/`, except those beginning `review/`, which are from the repository root.

**Roles.** `HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md` (`7d572400b941ad423978a7542d6c32fb73c934f0057240dbc5138898112bd53b`) is OWNER-RATIFIED (committed at `4a45b70`). **Effective commit (owner decision, 27 October 2026):** the commit that installed register v0.5 together with H-1, H-2 and H-3, which is `d36735da777b7d8403718af9e1d9d65c1cad47cc` (identified in register v0.6); it is not the Package 2 acceptance commit. From the effective commit, Claude is primary designer and coder, the ChatGPT reviewer chat is the independent reviewer, and the project owner remains sole ratifier, run authoriser and committer; the agreed position's sections 1-8 apply. **Owner decision, 27 October 2026:** from the effective commit, the ChatGPT reviewer chat holds the latitude Claude held as reviewer from 23 October, to be used carefully: it settles routine review matters itself, labelled REVIEWER-DECIDED; consequential items still go to the owner. Claude as author keeps only routine choices that affect no scope, acceptance or review gate. **Owner instruction, 27 October 2026:** for the first three reviews under the new roles, Claude checks every REVIEWER-DECIDED item against the ratified compliance, safety and process rules and flags any departure to the owner; reporting only (H-1 section 1.5). The transition documents below carry their authoring-time "DRAFT" headers; this register records their ratification. The ChatGPT coding chat retired on 27 October 2026 and the earlier Claude reviewer chat on 26 October 2026. As of drafting, the owner reports no intervening code package since the ChatGPT coding chat retired; any work before the effective commit is reconciled at installation against the existing roles and gates.

| Transition document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `HANDOVER/Claude_Primary_Handover_H1_v1r1.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 27 Oct 2026; superseded by H-1 v1r2 (register v0.6); `3223c41732888ea56c5458b365488660d157c93902b3745ed71d7d300fc2751e` |
| `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r2.md` | ChatGPT reviewer chat; facts checked by Claude; rights section checked by the owner alone | OWNER-RATIFIED 27 Oct 2026, including R-8..R-11 and section 3.1; superseded by H-2 v1r3 (register v0.6); `53f3af3f0845ea8534e25e896ffc8790fe685a7df9ecad8f7d7e48cd53f234a2`. Erratum: its closing line reads "End of H-2 v1r1 DRAFT"; the file is v1r2 and is installed unchanged. |
| `HANDOVER/AI_Roles_Transition_Record_H3_v1r1.md` | Claude; facts checked by the ChatGPT reviewer chat | OWNER-RATIFIED 27 Oct 2026; `8b01c57fd8804029906e1e9c87e8ecef18edb914a269e43a45dac90880703ce5` |

**Superseded for future roles** (kept in place as evidence, not normative): `HANDOVER/Claude_Reviewer_Handover_Predictive_Randomness_v10.md` (`61a5127816d30e2ffc342a011e3d029d7a3a6a80bc55c368751cc9d09ed9b191`); `HANDOVER/Predictive_Randomness_ChatGPT_Coder_Handover_v1_1r1.md` (`ab0afb64cec845cbbde29265e53309225991cd4a469306c609b905aff9048a01`); `HANDOVER/Interim_Handover_Note_for_both_claude_and_chatgpt_v1.md` (`a46866cad2c8d16869685f3a37b898dc453bf651572e60d27579024a2015a1e5`); `HANDOVER/Claude_Checkpoint_v2.md` (`33ddaf9c1d0d35726088d832893f72c7c97e532967c24b63cc36e6822f2693cf`). **Inputs, never authority:** D-1 `HANDOVER/Claude_Delta_Handover_D1_since_v10_v1.md` (`ac6dda4f6f965637118dbf2811cb4006497006e10f7be72476e5acd64c37a50c`) and ADD-2 `review/ChatGPT_Coder_ADD_2_Package2_v0_11r1_v0_1.md` (`ebaff99f4fc34ce38099ac5581abada7a1d0ffd1d8a7b7bfe3a0ce5fbb41f35b`).

**Package 2 v0.11-r1: ACCEPTED by the owner on 27 October 2026 and installed at commit `c5424839d8fc9d620bae132873e8594b5651d2ce`** (27 files: 2 modified, 25 added; Claude verified every blob against the reviewed bytes). Claude's review: `review/Claude_Review_Package2_v0_11r1_v1.zip` (`5c2e84655dcfd1d3a24129c0d38a5996e2f14195e807def382ba2bdb7d545a29`; PASS, 0 BLOCKER, 0 CORRECTION, 3 OPTIONAL). Factual record: `HANDOVER/Package2_v0_11r1_Acceptance_Deferred_Work_v0_1.md` (`42a75e0d75d33b4d8538070ba557b7e1a8ecc7117205baf131041473227a3ad3`). **Erratum:** that record names the installation hash file `EXPECTED_SOURCE_SHA256.json`; the actual file is `evidence/CLAUDE_EXPECTED_26_FILE_SHA256.txt` inside `review/Predictive_Randomness_MultiGame_Package2_v0_11r1_OWNER_INSTALL_OVERLAY_v0_1.zip`. Deferred test items P2-R1-O1 and P2-R1-O3 were scheduled as the first package under the new roles (owner decision, 27 October 2026) and are now done (TH-1, register v0.6); the other open optionals stay open. Acceptance grants no Windows, lifecycle, destructive, scientific, holdout, Mode H, FINAL, switch or allowlist authority.

**Integration installation:** installed at commit `ae76c29783856dbb9bf0076fabe0c3612340314e` (10 files added; Claude verified every blob). Package `MR_Integration_Install_v1r1.zip` (`154f54d8afb8870c7e4cc613fc9f69d656f8d8bbfbe343cc924f1566c67cd162`); its manifest `review/MR_Integration_Install_v1/INSTALL_MANIFEST_SHA256.txt` gives register v0.4's own SHA-256, `cdb8c24eeb1a855a042cfebed30a801e9e36a654ccc655b5a2b8cc4eba4585d7`. ChatGPT reviews: `review/Independent_ChatGPT_Focused_Review_MR_Integration_Candidates_v3.md` (PASS) and `review/Independent_ChatGPT_Focused_Review_MR_Integration_Install_v1.md` (editions PASS; C-INSTALL-01, verifier only, applied in v1r1).

| Document (path under `doc/`) | Authority and status | Git-content SHA-256 (UTF-8/LF) |
|---|---|---|
| `RATIFICATION_REGISTER_v0_4.md` | OWNER-RATIFIED 27 Oct 2026; superseded by register v0.5 (OWNER-RATIFIED 27 Oct 2026) | `cdb8c24eeb1a855a042cfebed30a801e9e36a654ccc655b5a2b8cc4eba4585d7` |

**Out-of-date statements in ratified editions.** These describe events that have since happened; this register prevails, and the files are not edited. Fold them into the next editions when those are revised for another reason.
- R3 v0.5 section 0.1, the Package 2 v0.11 row ("PENDING code/review"): Package 2 v0.11-r1 is accepted and installed (above).
- Architecture v0.8 section 0, "Current runtime task" (Package 2 v0.11 to correct C1-C6 under Claude's review): done; the reader and coordinator are installed at `c542483`.
- Proposal v0.6 section 0, "Current execution boundary" (ChatGPT implements and Claude reviews), and A-29: from the effective commit, the agreed roles position governs who drafts and who reviews. The rest of that paragraph (no scientific use approved; switches False; orphan interlock; empty allowlist) still holds.
- Proposal v0.6 section 0, "Document classification" (Package 2 outstanding), and A-18 (Package 2 v0.11 and its reviews outstanding): done.

## Records after the effective commit (register v0.6; 27 October 2026)

Paths in this section are under `doc/`, except those beginning `review/`, which are from the repository root. In this section, "this register" means register v0.6.

**Effective commit identity.** The effective commit is `d36735da777b7d8403718af9e1d9d65c1cad47cc` (parent `6460ae3`), verified by Claude in `review/Claude_Verification_Transition_Commit_d36735d_v1.md` (`c76b3bb305fca61bec0b791e6d792bc5b33f46529df0222498cbc5669a9343a0`, committed at `744afea`). The owner's commit `6460ae3` had already added four history files listed in the installation manifest, byte-identical to it; installation package v1r1's verifier accepted them. History commit `997ed46` added the final mechanical review and the installation ZIPs.

**Delivery method (owner decision, 27 October 2026; settles the Git transport question in the agreed roles position, section 11).** Changes are delivered as whole-file replacements: a `repo_overlay/` folder the owner copies onto the repository root, a read-only verifier with `pre`, `post` and `committed` phases (tolerant of CRLF working copies; every Git call uses `--no-optional-locks`), and a staging script naming the exact files. The exact unified diff of every changed file always travels with the package as evidence. No hand edits to project files; any deletion is explicit, listed and verified.

**Review dispositions (owner-accepted 27 October 2026).** `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md` (`5067aa520990b8ccc8521a04f3581424100cdd94994f5b9e3cb9e37863685339`, committed at `b14116b`) adds two reviewer-controlled dispositions to the four finding classes, which are unchanged. FIX AND PROCEED: Claude makes exactly the correction the reviewer authorised and continues without a separate recheck of it, keeping the evidence the procedure lists. RECHECK: the corrected material returns to the reviewer before acceptance. RECHECK is the default. Only the reviewer assigns a disposition, under its REVIEWER-DECIDED latitude; the owner may override. **Owner decision, 27 October 2026: FIX AND PROCEED never applies to code concerning any of the eight standing always-review subjects, however small the change.** The procedure changes no risk tier, always-review subject, reviewer right (R-1 to R-11), firewall, holdout safeguard or owner gate.

**Package sizing (owner-confirmed 27 October 2026).** Small packages for complex or HIGH work; a lead item that proves the pattern before a batch of similar items (for example, one lead method per family); heavy methods one at a time; ensembles last.

**TH-1 offline test hardening: ACCEPTED by the owner and installed at commit `744afea085c9fabc62c18ee5c18ee400d0853a9d`** (5 paths: 3 added, 2 modified; Claude verified every blob; the coordinator and the reader are unchanged; every file mode 100644). It closes the deferred Package 2 items P2-R1-O1 and P2-R1-O3. Installed package `review/TH1_Test_Hardening_v1r2.zip` (`47d6e5a67eb60b045c9b3c1b0930f0ced2ad082cee47dbdd93caaa74196c3015`); ChatGPT reviews `review/Independent_ChatGPT_Review_TH1_Test_Hardening_v1r1.md` and `review/Independent_ChatGPT_Focused_Recheck_TH1_Test_Hardening_v1r2.md` (PASS). The standard offline suite adds `tests.test_p2_r1_t05_hardening_v1` (60 tests). Owner-reported Windows evidence (Windows 11, Python 3.14.8): 60 OK with 2 skips, both because the owner's account cannot create symlinks; the reader's refusal of a hard-linked master passed on NTFS. Acceptance grants no Windows lifecycle, destructive, scientific, holdout, Mode H, FINAL, switch or allowlist authority.

**Oversight instruction status (as at register v0.6; superseded by register v0.7).** Two of the first three reviews under the new roles are done (the TH-1 review and its recheck). Claude listed the REVIEWER-DECIDED items (TH1-RD-01 to TH1-RD-04) and found no departure from the ratified rules. The third is the review of the package that carries this register edition.

**Continuity documents (register v0.6).** H-1 v1r2 replaces H-1 v1r1 for future roles; H-2 v1r3 replaces H-2 v1r2; H-3 v1r1 is unchanged. Earlier editions stay in place as history.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `HANDOVER/Claude_Primary_Handover_H1_v1r2.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; `55543ba522a4085fc4f2476d421a4940171bcd4c183a1fab5a691d291605eac0` |
| `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r3.md` | ChatGPT reviewer chat; facts checked by Claude; rights section checked by the owner alone | OWNER-RATIFIED 28 Oct 2026; `a2fb5c641a6fa8010aa59ff811aeba23145703bd5c0d4e2dbd70ac2fb419edb1` |
| `RATIFICATION_REGISTER_v0_5.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 27 Oct 2026; superseded by register v0.6; `551c1b42e99b58ad313dabe7d533e5650db83edce58e04f954b2f616c77afb3f` |

## E2R-1 specification and owner decisions of 28 October 2026 (register v0.7)

Paths in this section are under `doc/`, except those beginning `review/`, which are from the repository root. In this section, "this register" means register v0.7.

**DOC-1 installation.** Register v0.6, H-1 v1r2 and H-2 v1r3 were installed at commit `be185485693f29cf9ab28292dc6eebad00bbc32c` (parent `b14116b`; 9 files added; Claude verified every blob against `review/DOC1_Install_v1/INSTALL_MANIFEST_SHA256.txt`, whose SHA-256 is `6d992efa1fc78e286702f351c4180ef13720d93eca5c1cfbafade8fafc3c9476`, and which gives register v0.6's own hash, `5e677dce3f2ae01cd7a3f6cc1ff408c8e32e268150fe0c956e42bf703a9b074c`). The DOC-1 review is `review/Independent_ChatGPT_Review_DOC1_Records_Refresh_v1.md` (PASS). That review was the third of the first three reviews under the owner's oversight instruction; no departure was found.

**E2R-1, the E_2-readiness method-generic contract specification.** `Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md` (`0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954`) is OWNER-RATIFIED 28 October 2026. It is the stage-1 contract-field schema and acceptance list required by R2 v0.5 section 5.6, R3 v0.5 section 17.13 (stage 1) and Architecture v0.8 section 20A. Its authoring-time "DRAFT" header is historical; this register records its ratification.
- **Review history**, all by the ChatGPT reviewer chat:
  - the R-3 review of v0.2, `review/E2R_R3_Review_Commit_Independent.md` (`17087f5715bc3cfe49a2120fd25d1cdb626c6d9c480d53b5f3bb73559e93b2b2`; 3 BLOCKER, 10 CORRECTION, 2 OPTIONAL, 1 RECONSIDER);
  - its unforwarded predecessor, `review/Independent_ChatGPT_R3_Design_Review_E2R_v0_2_FINAL_OWNER_Addendum_v0_2.md` (history only; superseded);
  - focused rechecks of v0.3r1 (`review/Independent_ChatGPT_E2R_v0_3r1_Focused_Recheck_v0_1.md`, `866974a7ca38a156c76d46034fd0f31c2970b814dc627685f33c9c585f8ae392`) and v0.3r2 (`review/Independent_ChatGPT_E2R_v0_3r2_Focused_Recheck_v0_1.md`, `865edd97b97b06a5975b3ddc037dc5d3053e1f563cd1f295857a7a9d7623def2`);
  - the **PASS** recheck of v0.3r3, `review/Independent_ChatGPT_E2R_v0_3r3_Focused_Recheck_v0_1.md` (`3b69f540c637f400c503092daef9072c0069a857b9450cc91355e48e7c7d6646`; 0 findings).

  The review packages are `review/E2R_Spec_Review_v0_2.zip` and `review/E2R_Spec_Recheck_v0_3r1.zip` .. `_v0_3r3.zip` (commit `319fd11`).
- **What ratification does:** it fixes the design that the E_2-readiness code package implements. It authorises no code, no NAMES-1 work, no source move, no run, no registry change and no release. Each of those needs its own owner decision. It changes no ratified text of R2, R3 or Architecture; where it extends them, the next editions fold it in (out-of-date statements below).

**Owner decisions of 28 October 2026 recorded in the specification (its section 14).** Each is OWNER-DECIDED:
- **D-1:** `track_id` excludes the method revision. Each report uses one declared revision per track, and nothing is silently mixed or replaced (E2R-R40, R40A).
- **D-2:** synthetic and benchmark records carry the evidence tier `NOT_EVIDENCE`.
- **D-3:** method texts for E_1 and E_2 are written in the E_2-readiness code package; later methods' texts are written with their own specifications.
- **D-4:** `src/` holds current code only, with stable names and a folder per method (`src/methods/E_<nnn>/`, a locator only).
- **D-5:** superseded revisions move to revision-labelled archives (`archive/methods/E_<nnn>/r<k>/`, `archive/common/<name>/r<k>/`) with a README. There are no commit IDs, no stored file hashes and no run-time code-identity recording. Exact historical replay is not promised.
- **D-6:** a method runs only if its active registry entry is `SUPPORTED` for its current revision **and** no `IN_DEVELOPMENT.txt` flag is present. Release is the owner's two deliberate actions.
- **D-7:** NAMES-1, a one-off rename of existing versioned file names, comes before the E_2-readiness code.
- **D-8:** prospective results are shown both "as published" and "current methods".
- **D-9:** a seed policy's root is a pre-announced NIST Randomness Beacon pulse, fetched once by hand and independently verified. Runs never fetch.
- **D-10:** roots may be switched as a new revision or variant. Every root tried is logged and counted.
- **D-11:** a root published after historical targets may be used for retrospective development runs, labelled as experiment randomisation. A real forecast needs an already-approved root.

**Process decisions of 28 October 2026 (OWNER-DECIDED).**
- **Oversight instruction:** extended from three to six reviews under the new roles. The reviewer counts the E2R-1 rechecks as continuations of review 4 (its E2R-RD-13, -17 and -21). This newer owner instruction of 28 October 2026 supersedes the earlier requirement to send the owner every REVIEWER-DECIDED item: the reviewer still lists every item, and Claude still checks every one, but reports one to the owner only if Claude disagrees with it, or judges that it would interest the owner. It changes reporting only; reviewer rights are unchanged, and the authority is not delegated.
- **Handover documents get one review** each.
- **Git history:** the owner may clean or rewrite it once the code base is stable and in production, and does not plan to before then. Before any clean-up, Claude records which commit IDs this register and the handovers rely on. The E2R-1 design does not depend on Git history.

**Snapshot commits.** `319fd11` added `HANDOVER/Claude_Checkpoint_v4.md` (`d7634683d3d40edaa27c91576531cb198f1358613ca84c2e67e42096a1a6456e`; a non-authoritative running checkpoint) and the E2R-1 review history above. `38fc60e` added the superseded interim review and a duplicate copy of the checkpoint at `review/Claude_Checkpoint_v4.md`, byte-identical; history only.

**Out-of-date statements (register v0.7).** This register prevails, and the files are not edited:
- Architecture v0.8's standalone `.py` wording is extended by owner decision D-4. NAMES-1 proposes stable filename renaming only, without implementing per-method folders; its exact entry-file/folder layout is subject to the owner's separate OPEN-N1 decision. The next Architecture edition will incorporate the settled layout.
- R2 v0.5 section 5.6 and R3 v0.5 section 17.13 say the owner ratifies the stage-1 field schema first: done (above).
- H-1 v1r2:
  - section 1.5 describes the oversight instruction as three reviews with full reporting (now six, by exception);
  - section 9 lists the E_2-readiness specification as next (done; NAMES-1 is next, then the E_2-readiness code);
  - it does not mention the E2R-1 specification or decisions D-1..D-11.

  The next H-1 revision folds these in.
- Register v0.6, "Oversight instruction status" (two of three reviews done): superseded by the paragraph above.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; `0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954` |
| `RATIFICATION_REGISTER_v0_6.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; superseded by register v0.7; `5e677dce3f2ae01cd7a3f6cc1ff408c8e32e268150fe0c956e42bf703a9b074c` |

## NAMES-1 and owner decisions after register v0.7 (register v0.8)

Paths in this section are under `doc/`, except those beginning `review/` or `exchange/`, which are from the repository root. In this section, "this register" means register v0.8.

**DOC-2 installation.** The E2R-1 specification v0.3r3 and register v0.7 were installed at commit `908db9ea9d4a37b17833f5d43919804c78ef7e14` (28 October 2026).
- **It arrived in two commits.** The owner had already committed four of the package's eight files, byte-identical to the package, in commit `2c766644215a315edd8b92130e691224b60cd3de` (merged as `f300f2dfcd5c6a5efccb4c8b1040368728e2ad69`). They were the two DOC-2 review packages and the two DOC-2 reviews. `908db9ea9d4a37b17833f5d43919804c78ef7e14` added the other four.
- **The installer stopped on its one-commit rule only.** Its final check requires a single commit to add all eight files, and that is the rule that failed. Its blob check, which runs first, had passed for all eight files. The owner pushed after Claude confirmed that.
- **The owner accepted the two-commit delivery as a one-off exception (28 October 2026; OWNER-DECIDED).** It is not a precedent: a STOP remains a STOP. The installer STOP results are not recast as PASS. The reviewer accepted the installed DOC-2 content on this evidence (DOC2-RD-04, in `review/Independent_ChatGPT_EX_011_DOC2_Register_v0_8_NAMES1_Final_Recheck.md`, LF copy, `8c632dbc29916cded75efedecf6e3eea8918f07157e198e9fed2a72e34af6d0e`).
- **Claude verified the result from GitHub.** At `908db9ea9d4a37b17833f5d43919804c78ef7e14` all eight files match the package: the seven listed in `review/DOC2_Install_v1/INSTALL_MANIFEST_SHA256.txt`, and the manifest itself (`c3b373a3222d716963a1894ccc9d84f5737fa4af673d74b1fca18fdf1c39f8a0`). No file under `src/` or `tests/`, and no `.bat` file, has changed since `38fc60e`.
- **Commit `2c76664` also carried six NAMES-1 and E1-ALIGN history files**, byte-identical to those that NAMES-1 cites: the two NAMES-1 review packages and reviews, the owner-decisions record, and the E1-ALIGN early comments. Register v0.7's final bytes are `f9be980c2482c22cb2da6f7af34020f8cfd8e32302694c975c955ec407fcc015`. Its reviewed candidate r2 was `8b751a878e0626165b6c01bbc49d7d3014b3bd83a171200b4247eb5ec761796d`, and the mechanical finalisation diff is `review/DOC2_Register_v0_7_candidate_to_final.diff`.
- The DOC-2 reviews were:
  - `review/Independent_ChatGPT_Review_DOC2_Register_v0_7_v1.md` (2 CORRECTION, 1 OPTIONAL);
  - the PASS recheck `review/Independent_ChatGPT_Focused_Recheck_DOC2_Register_v0_7_r2.md` (`fc35b3ff7ad6892a066c7aca081f00c90cbc0847901ccebe3a2c202b376af13a`).

**NAMES-1, the one-off rename to stable file names.** `Predictive_Randomness_NAMES1_Rename_Specification_v0_2.md` (`07bda3e4a8a99bfc611a76cec672f8642532186567737e1a23de5e5701489e5a`) is OWNER-RATIFIED 28 October 2026. Its `OPEN` labels show its drafting state; the owner's decisions are below.
- **Review history**, all by the ChatGPT reviewer chat:
  - the R-3 review of v0.1, `review/Independent_ChatGPT_R3_Design_Review_NAMES1_v0_1.md` (`30d24ed02ff4ba3b0c84c760f306c8bfd02ddd2717db61013e60f855e3ace85a`; 0 BLOCKER, 4 CORRECTION, 1 OPTIONAL, 1 RECONSIDER);
  - the **PASS** recheck of v0.2, `review/Independent_ChatGPT_Focused_Recheck_NAMES1_Spec_v0_2.md` (`020fe9f73ba15f5260812d06701713d7b439880afb4197ace3488c4d63849f45`).

  The review packages are `review/NAMES1_Spec_Review_v0_1.zip` (`6aab40a1407c4b438ce05b7132ee2d3e183a6feb711d6f5877d9becc3246325f`) and `review/NAMES1_Spec_Recheck_v0_2.zip` (`fddf24f147406038653673e49350a7737b97c518849e46fc8c7b178d06b442a6`).
- **Owner decisions on NAMES-1, 28 October 2026** (OWNER-DECIDED; recorded in `review/Owner_Decisions_and_E1_ALIGN_Proposal_28Oct2026.md`):
  - **OPEN-N1 = A.** Each method's entry file stays directly in `src/methods/` (`E_<nnn>_<Name>.py`), as the Option F wrapper requires. Its folder `src/methods/E_<nnn>/` holds its method-specific modules and its `IN_DEVELOPMENT.txt` flag, and is created when that method's code first arrives. This settles the layout that E2R-1 section 12A.1 and decision D-4 left to NAMES-1.
  - **OPEN-N2 = deferred.** The owner's data tools and the legacy one-off test scripts stay out of NAMES-1. Any later tidy-up is a separate, owner-scoped package.
  - **OPEN-N3 = accepted.** The stable test names are those of the specification's section 3.
- **Installation.** The NAMES-1 code is installed in the same commit as this register. It makes 27 renames, with the 94 allowlisted substitutions in 27 files. Its manifest is `review/NAMES1_Code_Install_v1/INSTALL_MANIFEST_SHA256.txt`, and its exact allowlist and proof evidence are filed under `review/NAMES1_Code_Install_v1/`. The reviewer's code RECHECK is filed in `review/` in the same commit. The owner's Windows run of all 79 current tests, made before committing, is the acceptance.
- **E_1 stays revision 1**, under the structural exception scoped to NAMES-1 (N1-R03; E2R-R14A).
- **A visible record effect (N1-R01B).** A coordinator exit receipt issued before NAMES-1 no longer verifies afterwards, and is refused. No scientific receipt can exist yet, and none is converted or bypassed.
- **Test commands after NAMES-1.** The 60-test standard offline suite is `tests.test_multigame_reader_contracts tests.test_multigame_static_and_timing tests.test_multigame_launch_and_manifest tests.test_multigame_exit_receipt tests.test_multigame_science_allowlist tests.test_multigame_console_and_synthetic_scorer tests.test_t05_hardening`. The other 19 current tests are `tests.test_e1_standalone tests.test_multigame_windows_lifecycle_review`. Both use `PYTHONPATH` = `src`, `src/methods`, `tests`.

**Owner decisions made after register v0.7 (28 October 2026; OWNER-DECIDED).**
- **Oversight instruction: extended indefinitely**, superseding register v0.7's "six reviews". The reporting rule is unchanged: the reviewer lists every REVIEWER-DECIDED item, and Claude checks every one but reports one to the owner only if Claude disagrees or judges it of owner interest. Reviewer rights are unchanged, and the authority is not delegated.
- **Python 3.14.10 and the dependency update** (approved by the owner). The project venv was upgraded from Python 3.14.8 to 3.14.10 with `venv --upgrade`. The owner's dependency updater then changed no package versions: numpy 2.5.4, scipy 1.18.1, psutil 7.2.2, threadpoolctl 3.7.0, requests 2.34.2, beautifulsoup4 4.15.0 and selenium 4.51.0. Before NAMES-1, the owner re-ran the current suite on Windows: 60 tests OK with 2 skips, and the other 19 OK. Moving to Python 3.15 is a separate, later owner decision.
- **Phone exchange protocol:** `exchange/README.md` v0.3 (commit `262a2c4`).
  - When the owner relays from a phone, each message between the two AI chats is one upload: `EX_NNN_<Sender>.md`, or a flat `.zip` whose EX message lists its contents.
  - Claude records every EX file from both sides in `exchange/`, unchanged, and commits **only** inside `exchange/`.
  - Nothing in `exchange/` is ratified. Only the owner moves material into the main tree.
- **E1-ALIGN design ratified.** `Predictive_Randomness_E1_ALIGN_Specification_v0_2r1.md` (`d9ffd900c74d8a0cc5002bb78c83121f818514cd88ca9150bada8d6d1fa6653a`) is OWNER-RATIFIED 28 October 2026, as a design only, and is installed with this register. E1-ALIGN brings E_1 into the per-method layout and removes the shared reader's dependence on E_1's module.
  - **Review history**, all by the ChatGPT reviewer chat. Reviews that arrived through `exchange/` are stored under `review/` with LF line endings; the hashes below are of those LF copies, and the CRLF originals stay in `exchange/` (EX_004, EX_007 and EX_009):
    - early comments `review/Independent_ChatGPT_E1_ALIGN_Early_Design_Comments_28Oct2026.md` (`0cf83504ecd35440cc35723d74dcafab5c58b4dbd33c7feb3daaca3b475021af`);
    - the R-3 review of v0.1, `review/Independent_ChatGPT_R3_Review_E1_ALIGN_v0_1.md` (`ba64d1ef5a05718ac87f80802a74f08bde88b224c75a6cf58e6e9b7fb946df13`; 1 BLOCKER, 1 CORRECTION, 1 OPTIONAL);
    - the recheck of v0.2, `review/Independent_ChatGPT_E1_ALIGN_v0_2_Focused_Recheck_v0_1.md` (`7a887a780875da5b0f3f315b84d695c363017f8078aa6f6530939a9e5e9683c9`; 1 CORRECTION);
    - the **PASS** recheck of v0.2r1, `review/Independent_ChatGPT_EX_009_E1_ALIGN_v0_2r1_and_NAMES1_Order_Recheck.md` (`fbe0584ab69d7c59403bfc1f2e65aa3d868573d4fa17c38e6770d0ede7810248`; the reviewer's message EX_009, unchanged).
  - **Owner decisions, 28 October 2026** (OWNER-DECIDED):
    - **E1A-D1:** E_1 stays revision 1 under a structural-migration exception scoped to E1-ALIGN (its E1A-R02 conditions). This is a second scoped exception under E2R-R14A, not a precedent.
    - **E1A-D2:** the order is NAMES-1, then E1-ALIGN, then the E_2-readiness code. This amends E2R-R59.
    - **E1A-D3:** E_001's entry file keeps its whole-file firewall exemption for this migration, and the folder `E_001/` gets only the exact, counted allowances of the specification's section 5.
  - **Nothing about E1-ALIGN's code is authorised.** Its implementation is a separate HIGH-tier package after NAMES-1 is installed. It needs the owner's authorisation, an independent code RECHECK, and the owner's Windows run of all 84 tests.

**A known gap, found in review (28 October 2026).**
- The committed static import-firewall test (`test_method_loader_import_firewall_except_accepted_legacy_e1`) reads only the module part of `from X import Y`. So a method file using `from _common import game_draws_reader` would pass it.
- No current method uses that form, and NAMES-1 changes only the test's literal, not its logic.
- E1-ALIGN closes the gap with a symbol-aware check. Until then, Claude's review of every code package checks for that import form by hand.

**Out-of-date statements (register v0.8).** This register prevails, and the files are not edited:
- Register v0.7:
  - its oversight paragraph ("extended from three to six reviews"): now indefinite (above);
  - its line on Architecture's standalone `.py` wording ("subject to the owner's separate OPEN-N1 decision"): decided, A (above);
  - its basis line ("not present at that commit ... a separate owner decision"): the E2R-1 specification was installed at `908db9ea9d4a37b17833f5d43919804c78ef7e14`.
- E2R-1 section 12A.1 ("the exact entry-file and module layout inside each folder is fixed by NAMES-1"): fixed by OPEN-N1 = A.
- E2R-1 E2R-R59 (the order: specification, NAMES-1, E_2-readiness code): E1-ALIGN is inserted after NAMES-1 (E1A-D2).
- E2R-1 E2R-R14A ("the one scoped exception is NAMES-1's"): E1-ALIGN has its own scoped exception (E1A-D1).
- File names that NAMES-1 changed, in H-1 v1r2 (its section 7.1 module map and its suite command), in R2, R3 and Architecture, and in the TH-1 records: the old names are historical. The NAMES-1 specification's section 3 maps old to new. The next editions fold them in.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `Predictive_Randomness_NAMES1_Rename_Specification_v0_2.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; `07bda3e4a8a99bfc611a76cec672f8642532186567737e1a23de5e5701489e5a` |
| `Predictive_Randomness_E1_ALIGN_Specification_v0_2r1.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026 (design only); `d9ffd900c74d8a0cc5002bb78c83121f818514cd88ca9150bada8d6d1fa6653a` |
| `RATIFICATION_REGISTER_v0_7.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; superseded by register v0.8; `f9be980c2482c22cb2da6f7af34020f8cfd8e32302694c975c955ec407fcc015` |

## NAMES-1 installed, Python 3.15 and H-1 v1r3 (register v0.9)

Paths in this section are under `doc/`, except those beginning `review/` or `exchange/`, which are from the repository root. In this section, "this register" means register v0.9.

**NAMES-1 installation verified.** NAMES-1 was installed at commit `52ebeaa385fd05b18c4f3805c3cd2000948e343d` (28 October 2026; parent `7f6b4e8`), in one commit with register v0.8, the NAMES-1 v0.2 and E1-ALIGN v0.2r1 specifications and the review history, as register v0.8 records.
- **The owner's Windows run** (Python 3.14.10; owner-reported) followed the reviewed instructions:
  - PRE PASS; 27 renames; 42 files copied; POST PASS;
  - all 79 current tests passed, with 2 skips, the reader-contracts symlink subtest and the exit-receipt symlink test;
  - 63 import-origin and firewall checks passed;
  - COMMITTED PASS before the push.
- **One earlier attempt stopped at PRE** on three downloaded files saved under `review/`. It was undone with `git reset --hard` and `git clean -fd -- doc review`, and restarted from PRE. Nothing from it was committed.
- **Claude verified the commit from GitHub:**
  - the committed-phase verifier passes;
  - without rename detection, the commit has 42 additions, 27 deletions and 3 modifications;
  - `review/NAMES1_Code_Install_v1/INSTALL_MANIFEST_SHA256.txt` is `9d8664f38c33ee374ace06d29d98a4d84477af9199359e22bfcef84e1897f6a7`;
  - no `.bat` file and no test fixture changed;
  - the 79 tests pass on Linux.
- **The immediate recovery check (N1-T10) passed.** In a disposable clone, `git revert` restored a tree identical to `7f6b4e8`, and the pre-NAMES-1 suite passed under the old names. The clone was deleted. This is not a later rollback guarantee.
- **The reviewer's checks of the package:** the NAMES-1 code review (`review/Independent_ChatGPT_NAMES1_Code_Review_v0_1.md`), its rechecks (EX_009, EX_011) and the mechanical check of the final ZIP (`exchange/EX_013_ChatGPT.md`, PASS). Claude's report is `exchange/EX_014_Claude.md`.

**Python 3.15.2 (OWNER-DECIDED, 28 October 2026).**
- **The new venv:** the project venv is now Python 3.15.2, built afresh with `py -3.15 -m venv .venv`. The owner's dependency updater installed every package from a ready-built wheel: numpy 2.5.4, scipy 1.18.1, psutil 7.2.2, threadpoolctl 3.7.0, requests 2.34.2, beautifulsoup4 4.15.0 and selenium 4.51.0. Against the 3.14.10 venv, only certifi (2026.10.19 to 2026.10.23) and soupsieve (3.0.3 to 3.0.4) changed.
- **Tests (owner-reported):** on Python 3.15.2 at `52ebeaa`, all 79 current tests passed on Windows, with the same 2 symlink skips, and the 63 import checks passed.
- **The fallback:** the previous 3.14.10 venv is kept as `venv.bak` (ignored by Git), with Python 3.14 installed. The free-threaded 3.14t build was removed.
- **Not yet run under 3.15:** the owner's data tools. Their first run is a first run.
- **What changed in the language:** Python 3.15 makes UTF-8 the default text encoding (PEP 686). The tests show no effect on the project.
- **Ratified text this decision supersedes, on the interpreter version only:**
  - Proposal v0.6 A-17 ("Python 3.14 is the intended implementation platform") and its platform line;
  - R2 v0.5 section 9.1 ("Standard CPython 3.14 on Windows 11, not a free-threaded or experimental interpreter"). The rest of that line stands: the interpreter is standard CPython, not free-threaded;
  - R2 v0.5 section 12.3 ("Preserve the user's working standard Python 3.14.8 project `.venv`" and "its Python 3.14/Windows support checked"). Read these as the current project interpreter, now 3.15.2; any new package's support for that interpreter is still checked and announced first;
  - R3 v0.5's environment line, and Architecture v0.8 section 20.1, which cites the 3.14 documentation (an informational reference).

  The files are not edited; the next editions fold this in.
- **What this is not:** no scientific run, mode or gate changes with it. Moving to a new Python is not a W-23 waiver; the always-review rule on dependency upgrades stands.
- **Limits of the evidence:** the 79-test Windows run and 63 import checks are the evidence reported for this interpreter change; they do not by themselves establish the full W-23 and related dependency-upgrade acceptance gates. This record claims no completed gate not evidenced here. The owner's interpreter choice does not authorise a scientific or data run, or relax future upgrade preflight, numerical, N-1, golden or independent-review duties.

**H-1 v1r3.** `HANDOVER/Claude_Primary_Handover_H1_v1r3.md` (`ddf4de23b726b2abf55ffcab613f926b62775469076476f939288a278e6422fc`) is a candidate pending owner ratification, to be installed with this register; its ratification is recorded as OWNER-RATIFIED [H1-DATE] when given, and its installation is verified after the install.
- It is a records refresh of H-1 v1r2. Its Appendix C lists every change.
- It replaces H-1 v1r2 for future roles; v1r2 is kept as history.
- It authorises nothing.

**The phone exchange records.** `exchange/EX_001` to `EX_014` record the messages between the two AI chats from 28 October 2026. They are committed by Claude inside `exchange/` only, up to commit `83d1515`. They are evidence, not authority. Where they matter, the review files are stored under `review/` as LF copies, as register v0.8 records.

**Out-of-date statements (register v0.9).** This register prevails, and the files are not edited:
- Register v0.8, its future-tense description of NAMES-1 being installed with it: now historical fact (above).
- H-1 v1r2, generally: superseded by H-1 v1r3.
- Python 3.14 as the project interpreter, in the ratified documents listed above and in H-1 v1r2 and H-2 v1r3: the venv is now 3.15.2 (above).
- H-2 v1r3: it does not cover the events of 28 October 2026. The reviewer chat may refresh it as its own handover; it gets one review.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `HANDOVER/Claude_Primary_Handover_H1_v1r3.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED [H1-DATE]; `ddf4de23b726b2abf55ffcab613f926b62775469076476f939288a278e6422fc` |
| `HANDOVER/Claude_Primary_Handover_H1_v1r2.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; superseded by H-1 v1r3; `55543ba522a4085fc4f2476d421a4940171bcd4c183a1fab5a691d291605eac0` |
| `RATIFICATION_REGISTER_v0_8.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; superseded by this register; `3f217c6875d443a0cc1bba2f6c329b1fda455fb4a97bf7fe06090394736fffcf` |

## Interpretation and verification

- **Until the integration editions listed in the preceding table are owner-ratified**, the predecessor set identified below remains operative on its unaffected subjects, and the independently owner-ratified Method Ranking Measures Proposal v0.5 already governs its adopted subjects. **Upon owner ratification** (given 27 October 2026), the operative editions are Proposal v0.6, R1 v0.4, R2 v0.5, R3 v0.5, Architecture v0.8, the Windows POC Task Specification v0.2, P3 v0.2, TIE_SHA256_V1 v0.2, and exposure record v0.2.
- **Pre-integration predecessor set (ratified before this integration):** Proposal v0.5, R1 v0.4, R2 v0.4, R3 v0.4, Architecture v0.7, the Windows POC Task Specification v0.2, P3 v0.2 and TIE_SHA256_V1 v0.2. Their historical approvals and hashes remain valid; their operative status is superseded only on adoption of the corresponding later edition. Earlier editions and ChatGPT handovers remain historical sources, not replacement current specifications.
- ERR-R2-02 / Option F is **provisional for production** pending the P2 test evidence and owner disposition, even though the Architecture and POC Task Specification are ratified.
- The **failed/orphan-group result firewall** is OWNER-RATIFIED on 23 October 2026. Never consume downstream results from failed or orphan-suspected groups, even when a canonical result file exists.
- **Later owner report (23 October 2026):** the reviewed, incident-specific orphan-clearance utility completed `CHECK PASS` and `MANUAL CLEARANCE PASS`, preserving the archived FAILED evidence and writing a clearance record; a subsequent one-worker P2 canonical fixture passed and left no marker. The repository is not itself live-state proof; always recheck the current global marker before any future launch. These observations do not close P2 or authorise destructive tests.
- This register does not authorise process termination, destructive testing, holdout unsealing, Oz Lotto scraping or Oz science. Previously authorised Powerball E_1 historical development and the verified draw-1577 run are historical facts, not permission for new Oz runs. The current multi-game development pause remains binding. The historic-development draw ceiling is not a permanent constraint on later authorised prospective FINAL prediction, normal retraining, operation or maintenance; the holdout remains governed by its separate protections.
- To verify a Git-stored file hash on Windows CMD after committing, substitute the path and run: `git show HEAD:doc/EXAMPLE.md | python -c "import sys,hashlib;print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())"`. Git may normalise checkout line endings; `certutil -hashfile` on a CRLF working file can legitimately differ.
- Where an exact historic ratification day is not independently substantiated, the register says so rather than assigning a date without evidence. Improve those entries only when a documentary decision record supports the update.

## Change discipline

The owner-ratified v0.2 was the first committed register; the earlier v0.1 and single-line Architecture heading fix were uncommitted administrative housekeeping. They do not alter technical policy, scientific method contracts, executable code, or experiment evidence. Preserve earlier document versions. Until the effective commit, substantive changes followed ChatGPT draft, then Claude review at the required gates, then owner ratification. From the effective commit they follow the agreed roles position v0.1r1: normally Claude drafts, the ChatGPT reviewer chat independently reviews (always the other model), and the owner ratifies.


## Pre-integration consolidation - historical ratification inventory (26 October 2026)

This section preserves the prior consolidation's ratified identities, rules, decisions and Git-content hashes without deletion. The entries document the governing set **at the time of the v0.3 register's ratification**; they do not designate a second current set after the method-ranking integration is ratified. Present authority and supersession are stated in "Method ranking measures and integration editions" and "Interpretation and verification" above.

This register preserves the **17 previous ratified-file SHA-256 entries unchanged** in the tables above. Those are historical authority evidence, not hashes of the new ratified editions. Following the owner's decision to consolidate, the documents below became the **self-contained governing versions** on 26 October 2026, rather than layered amendments 0A/0B or a separate operative R2 erratum:

| Pre-integration ratified edition (path under `doc/`) | Historical governing predecessor | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `Predictive_Randomness_Research_Project_Proposal_v0_5.md` | Ratified Proposal v0.4 | OWNER-RATIFIED 26 Oct 2026; `834c0a8e738979ae5bed3527fd946d4f9b0f6a4d77dcbf6d087f1437db731d58` |
| `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_4.md` | R2 v0.3 + previously approved ERR-R2-01..05 + owner-decided ERR-R2-06 | OWNER-RATIFIED 26 Oct 2026; ERR-R2-02 Option F remains PROVISIONAL pending Windows gates; `1a1853570197a4a62a7d5695417848aac2de65b5fc83c25a931d936c84e05ef4` |
| `Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_4.md` | Ratified R3 v0.3 | OWNER-RATIFIED 26 Oct 2026; `78e2818ab71f6fce68cf1b39b24f5d0f2ad5563f7143b4358a3bcf5b6d49c752` |
| `Predictive_Randomness_Software_Architecture_Discussion_v0_7.md` | Ratified Architecture v0.6 | OWNER-RATIFIED 26 Oct 2026; `6c7ba2bc1da0d7b1f81e6e2e62e7c1e69448122bdf149399ae560f0c361b7218` |
| `Predictive_Randomness_MultiGame_Infrastructure_P3_Task_Specification_v0_2.md` | Ratified multi-game P3 v0.1 | OWNER-RATIFIED 26 Oct 2026; no execution authority; `2f3ac0e82dfd159025c3933ba41e812a4af0254da13e56664ed36dd5c5dcb61c` |
| `HOLDOUT_EXPOSURE_RECORD_v0_1.md` | new, factual and value-free | OWNER-RATIFIED, factual record 26 Oct 2026; superseded by v0.2 (26 Oct 2026); `a98064494444831b703587c48523dfb5e4b3c8aa66a3d00729ffcaa9d563c33b` |
| `NUMERICAL_INTEGRITY_AND_RETRAINING_REFERENCE_v0_1.md` | new, NON-NORMATIVE; operative requirements in R2/R3/Architecture | OWNER-RATIFIED, NON-NORMATIVE 26 Oct 2026; `51bcc84bc2ce4c2eda9c99008e75817f85e3f17ef12fc6639c1be6fd0ac3108d` |
| `RATIFICATION_REGISTER_v0_3.md` | owner-ratified v0.2 | OWNER-RATIFIED 26 Oct 2026; own SHA in external manifest (no self-reference) |

**Owner-ratified on 26 October 2026:** fixed 1 August 2026 quarantine and first-ten holdouts, versioned development masters with ledgers, source and provenance, assumed published order, free choice of safe reader representations, byte-owning prefix views, full-width `int64`/`float64` numeric types, opt-in date digests, default install-and-upgrade with mandatory regression tests, fresh per-target fitting and fixed safety gates. These requirements were ratified in consolidated R2 v0.4, R3 v0.4 and Architecture v0.7; upon owner ratification of the integration, their continuing operative editions are R2 v0.5, R3 v0.5 and Architecture v0.8. The newer editions integrate the owner-ratified Method Ranking Measures Proposal v0.5 and the separately owner-approved R3 section 17.10.1 CSV row-key clarification; no unrelated earlier rule is amended. Ratification of either set grants no run authority.

**Historical handovers (as at the v0.3 consolidation):** ChatGPT handbacks v0.6 and v0.6r1 were reported committed and were historical, not the accepted replacement new-coder handover. Exact HEAD bytes were to be checked independently at final installation. A definitive handover was to be prepared and independently reviewed only after those consolidated governing documents were ratified, installed and pushed; that was done (coder handover v1.0r1 at commit `6726963`, succeeded by v1.1r1 at `618fe48`).

**Post-ratification / commit verification (as at the v0.3 consolidation):** The seven installed document SHA-256 values above were computed from that ratified installation package; the committed files were confirmed byte-identical at Git HEAD `2db2554`. Register v0.3 omitted its own SHA-256 to avoid self-reference (it is now recorded in the method-ranking section above). Historical editions, R1 v0.4 and TIE note v0.2 were preserved unchanged.

## Consolidated v0.4 reviewed source dispositions (informational; OWNER-RATIFIED)

| Source / status | Treatment |
|---|---|
| R1 v0.4 | Unchanged operative method-catalogue source; may contain historical Powerball 1587 results; exposure recorded; no edits |
| TIE_SHA256_V1 v0.2 | Unchanged operative tie contract |
| R2 v0.3 + ERR-R2-01..06 | Historical sources; operative contents incorporated into owner-ratified consolidated R2 v0.4 |
| Architecture v0.6, R3 v0.3, Proposal v0.4, P3 v0.1 | Historical ratified predecessors, superseded by owner-ratified consolidated editions 26 Oct 2026 |
| `doc/experiments/P3_E1_..._REVIEW_CANDIDATE` | Historical review candidate, not a replacement governing spec |
| Windows POC Task Specifications v0.1 / v0.2 | Historical engineering planning, superseded by approved §5C and current architecture |
| ChatGPT handovers v0.6 and v0.6r1 | Historical/previous continuity snapshots, not normative; since superseded (see Continuity documents above) |
| Claude reviewer handovers v2–v8 | Historical prior-state snapshots; succeeded by v9 and then v10 (see Continuity documents above) |
| Repository root `README.md` | **TO UPDATE LATER**, not adopted as scientific authority in this consolidation |
| Exposure record and numerical technical reference | OWNER-RATIFIED 26 Oct 2026; factual record and non-normative guidance respectively |

Installation was then pending Claude's final mechanical comparison and the owner's commit/push; both were completed (installed at `2db2554`). The seven file hashes above identify the ratified-install package bytes. Ratification grants no run, update, holdout, Mode H, FINAL, process termination or Package 2 code acceptance.

**v0.3 full minimal-edit consolidation evidence:** original ratified predecessor source files remain preserved historically after the 26 October 2026 owner ratification. R1 and TIE unchanged. R2 erratum v0.3 is historical after consolidated R2 v0.4 ratification. Prior ChatGPT handovers v0.6/v0.6r1 are historical; the definitive coder handover was then pending Git HEAD verification and Claude's independent handover review, both since completed (v1.0r1 at `6726963`; v1.1r1 at `618fe48`).
