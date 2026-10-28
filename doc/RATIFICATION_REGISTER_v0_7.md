# Predictive Randomness — Ratification Register

**Register version:** v0.7 OWNER-RATIFIED 28 October 2026, recording the E2R-1 specification ratification and the owner decisions of 28 October 2026; v0.6 OWNER-RATIFIED 28 October 2026, recording the records after the effective commit (its identity, the delivery method, the review-disposition procedure and TH-1); v0.5 OWNER-RATIFIED 27 October 2026, recording the AI roles transition, the Package 2 v0.11-r1 acceptance and the integration installation; v0.4 OWNER-RATIFIED 27 October 2026 (drafted 26 October 2026), adding the method-ranking integration; v0.3 OWNER-RATIFIED 26 October 2026; v0.2 OWNER-RATIFIED 24 October 2026. Historical ratifications are preserved and remain valid.
**Basis:** the historical owner decisions and approved handovers, with current committed files cross-checked by Claude at GitHub HEAD `1c7cfced` (24 October 2026). Ten other content hashes matched that HEAD; the Architecture hash below is explicitly corrected to the **actually committed** v0.5 content (unfixed §5C heading). The separately proposed one-line heading change and register v0.1 were **not committed**. The pre-integration consolidated editions below were owner-ratified 26 October 2026; only explicit OPEN/PROVISIONAL/RECOMMENDED subitems remain undecided. The v0.4 entries were cross-checked by Claude against GitHub HEAD `618fe48` (26 October 2026), the v0.5 entries against GitHub HEAD `ae76c29` (27 October 2026), the v0.6 entries against GitHub HEAD `b14116b` (27 October 2026), and the already-committed v0.7 references against GitHub commit `38fc60e` (28 October 2026). The E2R-1 v0.3r3 specification is not present at that commit; it is verified by its content hash below, and its installation is a separate owner decision.  
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
| `RATIFICATION_REGISTER_v0_6.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; superseded by this register; `5e677dce3f2ae01cd7a3f6cc1ff408c8e32e268150fe0c956e42bf703a9b074c` |

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
