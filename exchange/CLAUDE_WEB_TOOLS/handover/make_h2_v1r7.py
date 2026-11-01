"""H-2 v1r7 from the installed H-2 v1r6 by counted edits (Claude, 30 Oct 2026, on the owner's instruction).

The ChatGPT reviewer chat that wrote H-2 v1r6 reached its maximum length on 30 October 2026 (after EX_075). The
owner instructed Claude to bring the reviewer's handover up to date, as the only available author. v1r7 changes
only the status, checkpoint and cold-start facts and the change-control section. The protected reviewer-rights
region (from the line starting '## 2.' to just before the line starting '## 4.') must stay byte-identical:
7,676 bytes, SHA-256 70e50dc3...; the builder asserts it. Everything outside that region stays US-ASCII.
Usage: python3 -I make_h2_v1r7.py H2_v1r6 OUT
"""
import hashlib, sys

src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == 'db40f40ef22995fc65a949243001858f1d7d1285713c9954531ae6b601fc5616'
RIGHTS_SHA = '70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db'


def rights(b):
    i = b.index(b'\n## 2.') + 1
    j = b.index(b'\n## 4.') + 1
    return b[i:j]


assert len(rights(raw)) == 7676 and hashlib.sha256(rights(raw)).hexdigest() == RIGHTS_SHA
t = raw.decode('utf-8')
E = []


def rep(old, new):
    E.append((old, new))


rep("# Predictive Randomness - ChatGPT Independent Reviewer Handover H-2 v1r6 r1 (DRAFT)",
    "# Predictive Randomness - ChatGPT Independent Reviewer Handover H-2 v1r7 (DRAFT)")
rep("**Repository target:** `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r6.md`  ",
    "**Repository target:** `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r7.md`  ")
rep("**Status:** **DRAFT r1, revised after Claude factual review; for joint owner ratification with H-1 v1r5 and Register v0.17; NOT installed.**  ",
    "**Status:** **DRAFT, for owner ratification with H-1 v1r6 and Register v0.20; NOT installed.**  ")
rep("**Author:** the ChatGPT independent reviewer chat.  ",
    "**Author:** **Claude (the primary designer and coder), on the project owner's explicit instruction of 30 October 2026.** The ChatGPT reviewer chat that wrote H-2 v1r6 reached its maximum length after EX_075 and could not update or review its own handover; the owner directed that Claude bring it up to date from v1r6 as the only available route. Claude changed only status, checkpoint, cold-start and change-control facts, kept the reviewer-rights region byte-identical, and added no reviewer rule. **The new reviewer chat should read this handover critically on takeover and report to the owner any factual error, omission, or wording that would narrow its independence; such a report is a normal finding, and the owner decides.**  ")
rep("**Predecessor:** owner-ratified and installed H-2 v1r5 (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r5.md`), canonical LF SHA-256 `67a1b3eaa3e1f51415eceba513fd7e1a39de91619296f0efba97ba108570a094` (DOC-6, commit `337b5b2`, per Register v0.16). The predecessor bytes used here are the ratified EX_049 handover, not the earlier H-2 v1r5 draft.  ",
    "**Predecessor:** owner-ratified and installed H-2 v1r6 (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r6.md`), canonical LF SHA-256 `db40f40ef22995fc65a949243001858f1d7d1285713c9954531ae6b601fc5616` (DOC-7, commit `8defe9d`, per Register v0.17).  ")
rep("**Rights preservation:** the complete `## 2.` through immediately before `## 4.` region remains **7,676 bytes, byte-for-byte identical** to H-2 v1r5 and H-2 v1r4;",
    "**Rights preservation:** the complete `## 2.` through immediately before `## 4.` region remains **7,676 bytes, byte-for-byte identical** to H-2 v1r6, H-2 v1r5 and H-2 v1r4;")
# ---------------------------------------------------------------- section 0
rep("- **Current handovers and register:** H-1 v1r4 and H-2 v1r5 are operative; Register v0.16 is owner-ratified. Claude is drafting H-1 v1r5 and Register v0.17; this H-2 v1r6 joins them for **one combined other-model/factual review and subsequent owner ratification**. No successor is operative merely because it is drafted or placed in `exchange/`.",
    "- **Current handovers and register:** H-1 v1r5 and H-2 v1r6 are operative; Register v0.19 is owner-ratified and installed at `b61b1a2`. Claude drafted H-1 v1r6, this H-2 v1r7 and Register v0.20 for owner ratification and one document-only install. **This round had no other-model review**, because the previous reviewer chat had ended; the new reviewer chat's takeover reading (header) stands in for it, and the owner may ask for a v1r8. No successor is operative merely because it is drafted or placed in `exchange/`.")
rep("- **New methods installed, NOT RELEASED:** **E_6 revision 1** (exact rational Beta-Bernoulli; discounted/power-likelihood updates for decay variants, three variants) at `7c93320`, after **T005**; **E_3/E_4 revision 1** (exact polynomial endpoint/gradient, shared helper, six variants each) at **`5b9edb4`**, after **T006**. Each declared variant has its own revision-1 `FORMULA_OPEN` registry entry; each method folder has `IN_DEVELOPMENT.txt`; separately, each method's unchanged `NOT_YET_SPECIFIED` placeholder remains. All three methods are **non-runnable**. E_3/E_4 scores are not probability vectors. Consult Registers v0.15-v0.17 and the installed designs for scientific settings, evidence and provenance.",
    "- **New methods installed, NOT RELEASED:** **E_6 revision 1** (exact rational Beta-Bernoulli; discounted/power-likelihood updates for decay variants, three variants) at `7c93320`, after **T005**; **E_3/E_4 revision 1** (exact polynomial endpoint/gradient, shared helper, six variants each) at **`5b9edb4`**, after **T006**; **wave 1, E_7, E_8, E_9 and E_10 revision 1** (shared counting helper; three variants each; E_7 and E_8 publish marginal probabilities, E_9 and E_10 scores only) at **`947c370`**, after **T007**; **wave 2, E_2, E_17, E_18 and E_19 revision 1** (shared gaps helper; three variants each; all scores only; E_17's `HAZARD_LOGAGE_SIGN_V1` is the owner's Method A, using its own ln(age) covariate, with its sign decided exactly) at **`b61b1a2`**, after **T008**. Each declared variant has its own revision-1 `FORMULA_OPEN` registry entry; each method folder has `IN_DEVELOPMENT.txt`; separately, each method's unchanged `NOT_YET_SPECIFIED` placeholder remains. All eleven methods are **non-runnable**. Consult Registers v0.15-v0.20 and the installed designs for scientific settings, evidence and provenance.")
rep("- **Safety remains closed:** all four execution switches are `False`, the scientific-result consumer allowlist is empty, and unresolved-orphan/no-status/no-kill rules remain binding.",
    "- **Safety remains closed:** all four execution switches are `False`, the scientific-result consumer allowlist is empty, and unresolved-orphan/no-status/no-kill rules remain binding. No installed method uses random numbers; the seed policy and the NIST Beacon root are settled at WF-1's design (owner decision W2-8).")
rep("E_6/E_3/E_4 final-package differences were limited by REG15-052-RD-02 and REG16-056-RD-02, recorded in EX_054/EX_057 without another reviewer check; this is **not** a general code-review waiver.",
    "E_6/E_3/E_4 final-package differences were limited by REG15-052-RD-02 and REG16-056-RD-02, recorded in EX_054/EX_057 without another reviewer check; wave 1's and wave 2's likewise, per EX_066 and EX_075, recorded in EX_067/EX_076; this is **not** a general code-review waiver.")
rep("- **Exchange and working lists:** the shared EX sequence has reached **EX_057** (owner-reported). `exchange/OWNER_REMINDERS.md` and `exchange/OWNER_ROADMAP.md` are informal owner working lists, **not governing rules or release authority**; their exact current entries were not supplied for this draft. Follow the installed `exchange/README.md` and verify the next free EX number at handoff.",
    "- **Exchange and working lists:** the shared EX sequence has reached **EX_076** (Claude's for-the-record final wave 2 package; the last reviewer message was EX_075). `exchange/OWNER_REMINDERS.md` (R-001..R-004) and `exchange/OWNER_ROADMAP.md` are informal owner working lists, **not governing rules or release authority**. Follow the installed `exchange/README.md` and verify the next free EX number at handoff.")
rep("**Evidence boundary:** Claude verified the `7c93320` and `5b9edb4` commits and T005/T006 reports from GitHub (Registers v0.16/v0.17); the owner's Windows runs remain **owner-reported**. This reviewer verified predecessor/document bytes but **could not fetch the live tree or EX_057** when drafting. Check current Git and the installed register on takeover; do not misstate who verified what.",
    "**Evidence boundary:** Claude verified the `7c93320`, `5b9edb4`, `947c370` and `b61b1a2` commits and the T005-T008 reports from GitHub (Registers v0.16-v0.20); the owner's Windows runs remain **owner-reported**. The previous reviewer's own independent reproductions are in its review records (`review/` and `exchange/EX_*_ChatGPT/`); this edition was drafted by Claude, so **none of its checkpoint facts is reviewer-verified**. Check current Git and the installed register on takeover; do not misstate who verified what.")
# ---------------------------------------------------------------- section 6
rep("1. **Establish actual authority:** obtain the owner-verified HEAD (at least `5b9edb4`, verified by Claude), the latest installed register (v0.16 at this checkpoint, installed at `5b9edb4`), H-1 v1r4, H-2 v1r5, H-3, the ratified roles position, relevant package sources/hashes and the latest owner decisions. If the tree, report or register cannot be fetched, state the limitation rather than guessing. Do not treat H-1 v1r5, H-2 v1r6 or Register v0.17 as installed before joint ratification and commit verification.",
    "1. **Establish actual authority:** obtain the owner-verified HEAD (at least `b61b1a2`, verified by Claude, and the later document-only install of this edition), the latest installed register (v0.19 at this checkpoint, installed at `b61b1a2`; v0.20 once installed), H-1 v1r6 or its installed successor, this H-2, H-3, the ratified roles position, relevant package sources/hashes and the latest owner decisions. If the tree, report or register cannot be fetched, state the limitation rather than guessing. Do not treat H-1 v1r6, H-2 v1r7 or Register v0.20 as installed before ratification and commit verification.")
rep("E_6 and E_3/E_4 installed specifications and `doc/METHOD_TEMPLATE/` when reviewing new methods.",
    "E_6, E_3/E_4, wave 1 (`doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md`) and wave 2 (`doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md`) installed specifications, the owner's Methods A and B proposal (`doc/GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md`) and `doc/METHOD_TEMPLATE/` (draft 3) when reviewing new methods.")
rep("For the 17 reviewer lessons and source/review anchors, read **H-2 v1r4 sections 7 and 8.2**; they were not copied into this handover or moved into the register.",
    "For the 17 reviewer lessons and source/review anchors, read **H-2 v1r4 sections 7 and 8.2**; they were not copied into this handover or moved into the register. **Three later catches by the previous reviewer show the standard to keep:** W1-C01 (a ranking claim stated without its exact conditions), W2-B01 (a claimed equivalence under a changed covariate, refuted with an exact constructed witness) and W2R1-C01 (a verification loop with no terminating branch at exact zero, shown with an eight-draw witness). Construct small exact witnesses, and test every exit.")
rep("3. **Inspect the next owner gate:** after this handover round the owner's sequence is template draft 2, E_7-E_16, Method A as E_17, Method B as E_45, then non-local means (Register v0.17); each still needs its own gates.",
    "3. **Inspect the next owner gate:** after this handover round the owner's sequence (Register v0.18; `exchange/OWNER_ROADMAP.md`) is releases and WF-1 (the first real measured walk-forward results with the R3 scorer and its N1 simulator; the seed policy settled at its design), then wave 3 (E_27, E_45 as Method B, E_26, E_28), the non-local means discussion, waves 4-11 and the ensembles; Method A's diagnostics A1-A5 are a separate package after WF-1 (W2-3). Each still needs its own gates.")
rep("Check `exchange/README.md`, the maximum committed EX number (at least EX_057 when drafted), and sender-collision history before naming the next reply.",
    "Check `exchange/README.md`, the maximum committed EX number (at least EX_076 when drafted), and sender-collision history before naming the next reply.")
# ---------------------------------------------------------------- section 7
old7 = t[t.index('## 7. H-2 v1r6 change control'):]
new7 = """## 7. H-2 v1r7 change control

- **Baseline and scope:** based on the owner-ratified H-2 v1r6 LF bytes (SHA-256 above), by counted edits in a builder that asserts the rights region. The checkpoint advances from E_3/E_4 at `5b9edb4` to wave 1 at `947c370` and wave 2 at `b61b1a2` (both commits Claude-verified). Registers v0.18 and v0.19, rehearsals T007/T008, the wave 2 design reviews (EX_068-EX_073) and code review (EX_074-EX_075) are recorded in the register; this file points to them. There is **no substantive new reviewer rule or scientific authorisation**.
- **Authorship:** drafted by Claude on the owner's instruction, because the reviewer chat that wrote v1r6 could not continue. The reviewer's own words elsewhere in this file are unchanged.
- **Protected reviewer rights:** unchanged **byte-for-byte**, 7,676 bytes with the recorded SHA-256. No proposed rights modification; any future modification requires explicit owner ratification. This includes R-1 through R-11, the T-05 note and the reviewer-discretion text.
- **Review status:** no other-model review was possible before ratification; the new reviewer chat's takeover reading stands in for it. Await the owner's ratification and documentary installation; H-2 v1r6 remains operative until then. Verify the post-push Git blobs rather than treating an EX commit as installation.

**End of H-2 v1r7 DRAFT - NOT OWNER-RATIFIED.**
"""
rep(old7, new7)

for old, new in E:
    c = t.count(old)
    assert c == 1, (c, old[:80])
    assert new.isascii(), old[:60]
    t = t.replace(old, new)
b = t.encode('utf-8')
assert rights(b) == rights(raw), 'the protected reviewer-rights region changed'
assert '\r' not in t and t.endswith('NOT OWNER-RATIFIED.**\n')
i = b.index(b'\n## 2.') + 1
j = b.index(b'\n## 4.') + 1
assert (b[:i] + b[j:]).isascii()
open(out, 'wb').write(b)
print(len(E), 'edits;', out, hashlib.sha256(b).hexdigest(), len(t.splitlines()), 'lines; rights region',
      len(rights(b)), 'bytes', hashlib.sha256(rights(b)).hexdigest()[:16])
