"""Draft register v0.5 from the installed register v0.4 by counted in-place edits (Claude, 27 Oct 2026).

Records the AI roles transition, Package 2 v0.11-r1 acceptance and the integration installation.
Every old string must occur exactly the expected number of times; inserted text is ASCII.
Usage: python3 -I make_register_v05.py REGISTER_v0_4 OUT_v0_5
"""
import sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
t = src.read_bytes().decode('utf-8')
assert '\r' not in t and t.endswith('\n')

H1 = 'HANDOVER/Claude_Primary_Handover_H1_v1r1.md'
H2 = 'HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r1.md'
H3 = 'HANDOVER/AI_Roles_Transition_Record_H3_v1r1.md'

NEW_SECTION = f"""## AI roles transition, Package 2 acceptance and integration installation (27 October 2026)

Paths in this section are under `doc/`, except those beginning `review/`, which are from the repository root.

**Roles.** `HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md` (`7d572400b941ad423978a7542d6c32fb73c934f0057240dbc5138898112bd53b`) is OWNER-RATIFIED (committed at `4a45b70`). **Effective commit (owner decision, 27 October 2026):** the commit that installs this register edition together with H-1, H-2 and H-3; it is not the Package 2 acceptance commit. From the effective commit, Claude is primary designer and coder, the ChatGPT reviewer chat is the independent reviewer, and the project owner remains sole ratifier, run authoriser and committer; the agreed position's sections 1-8 apply. **Owner decision, 27 October 2026:** from the effective commit, the ChatGPT reviewer chat holds the latitude Claude held as reviewer from 23 October, to be used carefully: it settles routine review matters itself, labelled REVIEWER-DECIDED; consequential items still go to the owner. Claude as author keeps only routine choices that affect no scope, acceptance or review gate. The ChatGPT coding chat retired on 27 October 2026 and the earlier Claude reviewer chat on 26 October 2026. As of drafting, the owner reports no intervening code package since the ChatGPT coding chat retired; any work before the effective commit is reconciled at installation against the existing roles and gates.

| Transition document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `{H1}` | Claude; reviewed by the ChatGPT reviewer chat | RATIFICATION CANDIDATE; `[H1-SHA]` |
| `{H2}` | ChatGPT reviewer chat; facts checked by Claude; rights section checked by the owner alone | RATIFICATION CANDIDATE; `[H2-SHA]` |
| `{H3}` | Claude; facts checked by the ChatGPT reviewer chat | RATIFICATION CANDIDATE; `[H3-SHA]` |

**Superseded for future roles** (kept in place as evidence, not normative): `HANDOVER/Claude_Reviewer_Handover_Predictive_Randomness_v10.md` (`61a5127816d30e2ffc342a011e3d029d7a3a6a80bc55c368751cc9d09ed9b191`); `HANDOVER/Predictive_Randomness_ChatGPT_Coder_Handover_v1_1r1.md` (`ab0afb64cec845cbbde29265e53309225991cd4a469306c609b905aff9048a01`); `HANDOVER/Interim_Handover_Note_for_both_claude_and_chatgpt_v1.md` (`a46866cad2c8d16869685f3a37b898dc453bf651572e60d27579024a2015a1e5`); `HANDOVER/Claude_Checkpoint_v2.md` (`33ddaf9c1d0d35726088d832893f72c7c97e532967c24b63cc36e6822f2693cf`). **Inputs, never authority:** D-1 `HANDOVER/Claude_Delta_Handover_D1_since_v10_v1.md` (`ac6dda4f6f965637118dbf2811cb4006497006e10f7be72476e5acd64c37a50c`) and ADD-2 `review/ChatGPT_Coder_ADD_2_Package2_v0_11r1_v0_1.md` (`ebaff99f4fc34ce38099ac5581abada7a1d0ffd1d8a7b7bfe3a0ce5fbb41f35b`).

**Package 2 v0.11-r1: ACCEPTED by the owner on 27 October 2026 and installed at commit `c5424839d8fc9d620bae132873e8594b5651d2ce`** (27 files: 2 modified, 25 added; Claude verified every blob against the reviewed bytes). Claude's review: `review/Claude_Review_Package2_v0_11r1_v1.zip` (`5c2e84655dcfd1d3a24129c0d38a5996e2f14195e807def382ba2bdb7d545a29`; PASS, 0 BLOCKER, 0 CORRECTION, 3 OPTIONAL). Factual record: `HANDOVER/Package2_v0_11r1_Acceptance_Deferred_Work_v0_1.md` (`42a75e0d75d33b4d8538070ba557b7e1a8ecc7117205baf131041473227a3ad3`). **Erratum:** that record names the installation hash file `EXPECTED_SOURCE_SHA256.json`; the actual file is `evidence/CLAUDE_EXPECTED_26_FILE_SHA256.txt` inside `review/Predictive_Randomness_MultiGame_Package2_v0_11r1_OWNER_INSTALL_OVERLAY_v0_1.zip`. Deferred test items P2-R1-O1 and P2-R1-O3 are scheduled as the first package under the new roles (owner decision, 27 October 2026); the other open optionals stay open. Acceptance grants no Windows, lifecycle, destructive, scientific, holdout, Mode H, FINAL, switch or allowlist authority.

**Integration installation:** installed at commit `ae76c29783856dbb9bf0076fabe0c3612340314e` (10 files added; Claude verified every blob). Package `MR_Integration_Install_v1r1.zip` (`154f54d8afb8870c7e4cc613fc9f69d656f8d8bbfbe343cc924f1566c67cd162`); its manifest `review/MR_Integration_Install_v1/INSTALL_MANIFEST_SHA256.txt` gives register v0.4's own SHA-256, `cdb8c24eeb1a855a042cfebed30a801e9e36a654ccc655b5a2b8cc4eba4585d7`. ChatGPT reviews: `review/Independent_ChatGPT_Focused_Review_MR_Integration_Candidates_v3.md` (PASS) and `review/Independent_ChatGPT_Focused_Review_MR_Integration_Install_v1.md` (editions PASS; C-INSTALL-01, verifier only, applied in v1r1).

| Document (path under `doc/`) | Authority and status | Git-content SHA-256 (UTF-8/LF) |
|---|---|---|
| `RATIFICATION_REGISTER_v0_4.md` | OWNER-RATIFIED 27 Oct 2026; superseded by this register when it is ratified | `cdb8c24eeb1a855a042cfebed30a801e9e36a654ccc655b5a2b8cc4eba4585d7` |

**Out-of-date statements in ratified editions.** These describe events that have since happened; this register prevails, and the files are not edited. Fold them into the next editions when those are revised for another reason.
- R3 v0.5 section 0.1, the Package 2 v0.11 row ("PENDING code/review"): Package 2 v0.11-r1 is accepted and installed (above).
- Architecture v0.8 section 0, "Current runtime task" (Package 2 v0.11 to correct C1-C6 under Claude's review): done; the reader and coordinator are installed at `c542483`.
- Proposal v0.6 section 0, "Current execution boundary" (ChatGPT implements and Claude reviews), and A-29: from the effective commit, the agreed roles position governs who drafts and who reviews. The rest of that paragraph (no scientific use approved; switches False; orphan interlock; empty allowlist) still holds.
- Proposal v0.6 section 0, "Document classification" (Package 2 outstanding), and A-18 (Package 2 v0.11 and its reviews outstanding): done.

"""

EDITS = [
    ('**Register version:** v0.4 OWNER-RATIFIED 27 October 2026 (drafted 26 October 2026), adding the method-ranking integration;',
     '**Register version:** v0.5 RATIFICATION CANDIDATE (27 October 2026), recording the AI roles transition, the Package 2 v0.11-r1 acceptance and the integration installation; v0.4 OWNER-RATIFIED 27 October 2026 (drafted 26 October 2026), adding the method-ranking integration;', 1),
    ('The v0.4 entries were cross-checked by Claude against GitHub HEAD `618fe48` (26 October 2026).',
     'The v0.4 entries were cross-checked by Claude against GitHub HEAD `618fe48` (26 October 2026), and the v0.5 entries against GitHub HEAD `ae76c29` (27 October 2026).', 1),
    ('Two documents were owner-ratified on 26 October 2026 at commit `ac01678`.',
     'In this section, "this register" means register v0.4, the edition that recorded the integration. Two documents were owner-ratified on 26 October 2026 at commit `ac01678`.', 1),
    ('OWNER-RATIFIED 26 Oct 2026; superseded by this register (v0.4, OWNER-RATIFIED 27 Oct 2026) |',
     'OWNER-RATIFIED 26 Oct 2026; superseded by register v0.4 (OWNER-RATIFIED 27 Oct 2026) |', 1),
    ('**Continuity documents (commit `618fe48`, verified by Claude):** the current handovers are',
     '**Continuity documents:** from the effective commit, the current continuity documents are H-1, H-2 and H-3 (next section). Before it (commit `618fe48`, verified by Claude), the current handovers were', 1),
    ('the interim note is in `HANDOVER/`. They are continuity records, not normative.',
     'the interim note is in `HANDOVER/`. They are continuity records, not normative, and are superseded for future roles by H-1, H-2 and H-3.', 1),
    ('\n## Interpretation and verification\n',
     '\n' + NEW_SECTION + '## Interpretation and verification\n', 1),
    ('Future substantive changes still follow ChatGPT draft \u2192 Claude review at the required gates \u2192 owner ratification.',
     'Until the effective commit, substantive changes followed ChatGPT draft, then Claude review at the required gates, then owner ratification. From the effective commit they follow the agreed roles position v0.1r1: normally Claude drafts, the ChatGPT reviewer chat independently reviews (always the other model), and the owner ratifies.', 1),
]

for old, new, n in EDITS:
    c = t.count(old)
    assert c == n, f'expected {n} of {old[:60]!r}, found {c}'
    bad = sorted({ch for ch in new if ord(ch) > 127} - {ch for ch in old if ord(ch) > 127})
    assert not bad, f'non-ASCII inserted: {bad!r}'
    t = t.replace(old, new)
out.write_bytes(t.encode('utf-8'))
print('register v0.5 draft written:', out)
