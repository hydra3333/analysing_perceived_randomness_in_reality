"""H-1 v1r6 from the installed H-1 v1r5 by counted edits (Claude, 30 Oct 2026).

v1r6 refreshes v1r5 after waves 1 and 2 (owner, 30 October 2026): the baseline, the installed methods and data,
the tests, the rebuild records, the lessons, the next work and the identities. It changes no rule. Section 2A
(the owner's foundational points) must stay byte-identical; the builder asserts the whole section.
Usage: python3 -I make_h1_v1r6.py H1_v1r5 OUT
"""
import hashlib, sys

src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '1214bd971058ddd6cc680526fd80375bdbbd6db17397e41ba4c14ae5467101e1'
t = raw.decode('ascii')


def section(text, head, nxt):
    i = text.index(head)
    return text[i:text.index(nxt, i)]


S2A = section(t, '### 2A. The owner\'s foundational points', '---\n\n## 3.')
E = []


def rep(old, new):
    E.append((old, new))


# ---------------------------------------------------------------- header
rep("# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v1r5",
    "# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v1r6")
rep("**Version:** v1r5 DRAFT, 30 October 2026 (Adelaide, UTC+10:30). v1r5 refreshes v1r4 at the milestone of the first three new methods (owner, 30 October 2026). It keeps v1r4's structure, describes the current state and the owner's order of work, and changes no rule. Appendix B lists what changed. Author: Claude. Independent reviewer: the ChatGPT reviewer chat. The project owner ratifies.",
    "**Version:** v1r6 DRAFT, 30 October 2026 (Adelaide, UTC+10:30). v1r6 refreshes v1r5 after waves 1 and 2 (owner, 30 October 2026). It keeps v1r5's structure, describes the current state and the owner's order of work, and changes no rule. Appendix B lists what changed. Author: Claude. The project owner ratifies. **The reviewer chat that reviewed v1r5 reached its maximum length on 30 October 2026, after EX_075;** on the owner's instruction Claude also drafted the reviewer's handover, H-2 v1r7, and the new reviewer chat reads both when it starts.")
rep("**Status:** DRAFT for review. It becomes authoritative only when the owner ratifies it and installs it with register v0.17; until then H-1 v1r4 stands.",
    "**Status:** DRAFT for the owner. It becomes authoritative only when the owner ratifies it and installs it with register v0.20; until then H-1 v1r5 stands.")
rep("**Baseline described:** the E_3/E_4 package installed at `5b9edb44d4f4bf01e2d4e8cd7ec9561b32b3110e` (30 October 2026; verified by Claude from GitHub; section 7).",
    "**Baseline described:** the wave 2 package installed at `b61b1a27999dcdfce2e2e59c6ced4f349ee652b4` (30 October 2026; verified by Claude from GitHub; section 7).")
rep("**Replaces, for future roles:** H-1 v1r4, v1r3, v1r2 and v1r1 (kept as history)",
    "**Replaces, for future roles:** H-1 v1r5, v1r4, v1r3, v1r2 and v1r1 (kept as history)")
# ---------------------------------------------------------------- section 0
rep("2. Read, in order: this file; H-2 (what the reviewer checks and its rights);",
    "2. Read, in order: the introductory blurb that started your chat (`doc/HANDOVER/Claude_Primary_Handover_H1_v1r6_introductory_blurb.md`); this file; H-2 (what the reviewer checks and its rights);")
# ---------------------------------------------------------------- section 1
rep("- **ChatGPT reviewer chat:** normally leads independent scientific and technical review. It may propose competing designs, methods and hypotheses, and may do bounded coding, alternative implementations or tests when the owner assigns them. Its handover is H-2.",
    "- **ChatGPT reviewer chat:** normally leads independent scientific and technical review. It may propose competing designs, methods and hypotheses, and may do bounded coding, alternative implementations or tests when the owner assigns them. Its handover is H-2. The reviewer chat that served until EX_075 reached its maximum length (30 October 2026); the owner started a new one from H-2 v1r7 and its introductory blurb, both drafted by Claude on the owner's instruction, with H-2's protected rights text byte-identical. Treat the new chat exactly as the old: same rights, same independence.")
rep("No departure has been found so far (through E34-056-RD-03).",
    "No departure has been found so far (through W2-075-RD-04).")
rep("They travel to `exchange/` in a for-the-record EX message that needs no reply (EX_046, EX_054, EX_057), with the narrow diff;",
    "They travel to `exchange/` in a for-the-record EX message that needs no reply (EX_046, EX_054, EX_057, EX_067, EX_076), with the narrow diff;")
# ---------------------------------------------------------------- section 2
rep("- **When the owner is away** and has said to carry on:",
    "- **Introductory blurbs** (owner, 30 October 2026): each handover has a starter text saved next to it, named `<handover file name>_introductory_blurb.md`, which the owner pastes to start the new chat. Keep it in step with its handover, and write your own handover and blurb first.\n- **When the owner is away** and has said to carry on:")
# ---------------------------------------------------------------- section 4
rep("| `Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md` | `b9d60b4c753bb90c6a7ca302fb4802c353b0ae23fbe82c2b417ae7b089fad072` | E_3's and E_4's specification and the shared polynomial-fit helper; D34-1..D34-5 |\n| `METHOD_TEMPLATE/README.md` (and the 9 other template files) | `f17e2d6eb489797415252689038078047011b7aa7ba2e24f987c265078df3e26` | The new-method template, draft 1 (D6-5): what to copy, what to fill in, the checklist |",
    "| `Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md` | `b9d60b4c753bb90c6a7ca302fb4802c353b0ae23fbe82c2b417ae7b089fad072` | E_3's and E_4's specification and the shared polynomial-fit helper; D34-1..D34-5 |\n| `Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md` | `06b491225812e14962aef99e299cbd6c003be68bb5a73425e566f1b1fe685060` | Wave 1: E_7, E_8, E_9 and E_10 and the shared counting helper; W1-1..W1-6 |\n| `Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md` | `2ab342911701edf1e93ad590e4765a3efac54a76d732b7fd2c5875c7d363fe74` | Wave 2: E_2, E_17 (Method A), E_18 and E_19 and the shared gaps helper; W2-1..W2-8 |\n| `GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md` | `4f5459b5bb3ae24ba0624e140e71729213928eafc090bb9fd9a78405a621c597` | The owner's Methods A and B (A is E_17's log-age variant; B becomes E_45's specification in wave 3); supersedes the pre-exploratory `GASI_thought_experiments_possibly_unexplored_areas.md` |\n| `METHOD_TEMPLATE/README.md` (and the 9 other template files) | `daac8da1f404e21bd1869609e4621f47bc25a84b3524c1688703c69ca2064214` | The new-method template, draft 3 (W2-7): what to copy, what to fill in, the checklist, \"things that bite\" |")
rep("register v0.17 is installed with this file (register v0.16 is `d84fc3ddd5978f0a5529bad20f9db9d1f95142c7e06e3dd78599cc0d4fa1c220`).",
    "register v0.20 is installed with this file (register v0.19 is `b3ae51fd162960b64a9d145a52646dceeb3aec5b91e4b359ad7166e5e4c8e6a0`).")
# ---------------------------------------------------------------- section 5.3
rep("The installed data, in both games: E_1 `SUPPORTED` (variant `FULL_HISTORY_RAW_COUNTS_V1`, revision 1); E_3 and E_4 revision 1 (six variants each) and E_6 revision 1 (three variants), all `FORMULA_OPEN` with their `IN_DEVELOPMENT.txt` flags present; and E_2..E_62 each keeping a `FORMULA_OPEN` placeholder with variant `NOT_YET_SPECIFIED`, which is never edited. That is 32 declarations and 154 registry chains (186 files).",
    "The installed data, in both games: E_1 `SUPPORTED` (variant `FULL_HISTORY_RAW_COUNTS_V1`, revision 1); revision 1, all `FORMULA_OPEN` with their `IN_DEVELOPMENT.txt` flags present, of E_3 and E_4 (six variants each), E_6 (three), wave 1's E_7, E_8, E_9 and E_10 (three each) and wave 2's E_2, E_17, E_18 and E_19 (three each); and E_2..E_62 each keeping a `FORMULA_OPEN` placeholder with variant `NOT_YET_SPECIFIED`, which is never edited (also for the methods that now have real variants). That is 80 declarations and 202 registry chains (282 files).")
rep("and D34-1..D34-5 (E_3/E_4: one shared helper, six frozen variants, raw least squares and smoothed interpolation and minimax, scores only, precise naming).",
    "and D34-1..D34-5 (E_3/E_4: one shared helper, six frozen variants, raw least squares and smoothed interpolation and minimax, scores only, precise naming); W1-1..W1-6 (wave 1: one shared counting helper, twelve fixed variants, E_7's full-history calibration variant kept, E_9 and E_10 score-only and E_7 and E_8 publishing marginals, template draft 2, E_8 by moment estimates); W2-1..W2-8 (wave 2: one shared gaps helper; twelve fixed variants; W2-3, E_17's `HAZARD_LOGAGE_SIGN_V1` is Method A's own log-age rule, decided exactly, with Method A's diagnostics A1-A5 a later package after WF-1; all four score-only; E_18 a fixed four-law library by exact minimum chi-square; E_19 per number with cycles 2, 3 and 4; W2-7 template draft 3 with the byte-reproducibility rule; W2-8 the NIST seed settled at WF-1's design).")
# ---------------------------------------------------------------- section 7.1
rep("| `5b9edb4` | E_3/E_4 package v1 | E_3 and E_4 revision 1, exact polynomial fits (value and slope at the target) with the shared helper `polynomial_fits.py`, installed non-runnable; register v0.16 (register v0.17) |",
    "| `5b9edb4` | E_3/E_4 package v1 | E_3 and E_4 revision 1, exact polynomial fits (value and slope at the target) with the shared helper `polynomial_fits.py`, installed non-runnable; register v0.16 (register v0.17) |\n| `947c370` | Wave 1 package v1 | E_7, E_8, E_9 and E_10 revision 1 with the shared helper `occurrence_counts.py`, installed non-runnable; template draft 2; register v0.18 (register v0.19) |\n| `b61b1a2` | Wave 2 package v1 | E_2, E_17 (Method A), E_18 and E_19 revision 1 with the shared helper `recurrence_gaps.py`, installed non-runnable; template draft 3; register v0.19 (register v0.20) |")
rep("`337b5b2` (DOC-6: H-1 v1r4, H-2 v1r5, register v0.14; four duplicate zips removed at `f9de54a`).",
    "`337b5b2` (DOC-6: H-1 v1r4, H-2 v1r5, register v0.14; four duplicate zips removed at `f9de54a`), `8defe9d` (DOC-7: H-1 v1r5, H-2 v1r6, register v0.17).")
# ---------------------------------------------------------------- section 7.2
rep("| `src/methods/_common/contract_data/` | Installed declarations and hash-chained registry entries (186 files) |",
    "| `src/methods/_common/contract_data/` | Installed declarations and hash-chained registry entries (282 files) |")
rep("`ADAPTERS` maps a method ID to its adapter: E_1, E_3, E_4, E_6 |",
    "`ADAPTERS` maps a method ID to its adapter: E_1, E_2, E_3, E_4, E_6, E_7, E_8, E_9, E_10, E_17, E_18, E_19 |")
rep("| `src/methods/E_003/`, `src/methods/E_004/` | E_3 and E_4: `variants.py` (the same six-row table) and `contract.py` (scores p(0) and p'(0)); flags present |",
    "| `src/methods/E_003/`, `src/methods/E_004/` | E_3 and E_4: `variants.py` (the same six-row table) and `contract.py` (scores p(0) and p'(0)); flags present |\n| `src/methods/_common/occurrence_counts.py` | Shared helper for wave 1, revision 1: window counts, decayed counts and period counts, exact, each with a second route |\n| `src/methods/E_007/` .. `src/methods/E_010/` | Wave 1: `variants.py` and `contract.py` each (E_7 Beta shrinkage, E_8 hierarchical periods, E_9 decayed counts, E_10 two-window contrast); flags present |\n| `src/methods/_common/recurrence_gaps.py` | Shared helper for wave 2, revision 1: appearances, gaps, censored exposures by age, age bins, and the certified log-age sign by two routes (the second with its own exact-zero test; a 1,024-term refusal cap) |\n| `src/methods/E_002/`, `E_017/`, `E_018/`, `E_019/` | Wave 2: `variants.py` and `contract.py` each (E_2 interval alignment, E_17 binned hazard and Method A's log-age sign, E_18 four-law mixture with a KKT certificate, E_19 per-number periodic factor); flags present |")
# ---------------------------------------------------------------- section 7.4
rep("- **242 offline tests in 17 modules** at `5b9edb4`: 84 earlier, 54 CODE-1 (`test_e2r_contract` 53 including the six-worker T12, `test_e2r_prefix` 1), 52 CODE-2 (`test_e2r_dispatch` 18, `test_e2r_runner` 34), 20 E_6 (`test_e6_beta_bernoulli`), 19 for the shared helper (`test_polynomial_fits`) and 13 E_3/E_4 (`test_e3_e4_polynomial`). The suite runner `RUN_E34_SUITE.py` (inside `exchange/EX_057_Claude/E34_Install_v1.zip`) runs each module and compares its count; Windows allows only the three symlink skips. Results: Linux (Claude, Python 3.13.17 and 3.15.0b4) 242 pass; Windows (owner-reported, Python 3.15.2, 30 October 2026) 242 pass with 3 symlink skips, run straight after the push (a recorded departure; the rehearsal T006 had passed the same bytes before).",
    "- **299 offline tests in 21 modules** at `b61b1a2`: 84 earlier, 54 CODE-1 (`test_e2r_contract` 53 including the six-worker T12, `test_e2r_prefix` 1), 52 CODE-2 (`test_e2r_dispatch` 18, `test_e2r_runner` 34), 20 E_6 (`test_e6_beta_bernoulli`), 19 + 13 E_3/E_4 (`test_polynomial_fits`, `test_e3_e4_polynomial`), 8 + 18 wave 1 (`test_occurrence_counts`, `test_wave1_frequency`) and 12 + 19 wave 2 (`test_recurrence_gaps`, `test_wave2_recurrence`). The suite runner `RUN_W2_SUITE.py` (inside `exchange/EX_076_Claude/W2_Install_v1.zip`) runs each module and compares its count; Windows allows only the three symlink skips. Results: Linux (Claude, Python 3.13.17 and a 3.15.0b4 venv with the project's dependencies) 299 pass; Windows (owner-reported, Python 3.15.2, 30 October 2026) 299 pass with 3 symlink skips, before the commit, for both waves.")
rep("(approved for the rehearsals and installs of CODE-1, CODE-2, E_6 and E_3/E_4)",
    "(approved for the rehearsals and installs of CODE-1, CODE-2, E_6, E_3/E_4, wave 1 and wave 2)")
# ---------------------------------------------------------------- section 8
rep("- **Use it** to rehearse a code package on the owner's Windows machine before the real install (T003 for CODE-1, T004 for CODE-2, T005 for E_6, T006 for E_3/E_4), when the owner wants that.",
    "- **Use it** to rehearse a code package on the owner's Windows machine before the real install (T003 for CODE-1, T004 for CODE-2, T005 for E_6, T006 for E_3/E_4, T007 for wave 1, T008 for wave 2), when the owner wants that.")
rep("Their mutation tools and contract-data generators are installed under `review/E6_Install_v2/tools/` and `review/E34_Install_v1/tools/`.",
    "For wave 1: `EX_061_Claude/` and `EX_063_Claude/` (design, reference script, template draft 2 builder), `EX_065_Claude/` (candidate, builder, verifier template, base snapshot `BASE_7462ea9_src_tests_template.zip`, register v0.18 builder) and `EX_067_Claude/` (final zip). For wave 2: `EX_068_Claude/`, `EX_070_Claude/` and `EX_072_Claude/` (design v0.1, v0.1r1 and v0.1r2 with their builders, the reference script and probes), `EX_074_Claude/` (candidate, builder, verifier template, e2e script, base snapshot `BASE_8f44d50_src_tests_template.zip`, register v0.19 builder) and `EX_076_Claude/` (final zip). Their mutation tools, method and contract-data generators and template builders are installed under `review/E6_Install_v2/tools/`, `review/E34_Install_v1/tools/`, `review/W1_Install_v1/tools/` and `review/W2_Install_v1/tools/`.")
rep("- **The owner sometimes saves files into the repository**; a verifier's PRE then stops, or a rebase is blocked. Ask for downloads outside the repository (`E:\\TEMP`) and for the reviewer's zips to be uploaded to Claude.",
    "- **The owner sometimes saves files into the repository**; a verifier's PRE then stops, or a rebase is blocked. Ask for downloads outside the repository (`E:\\TEMP`) and for the reviewer's zips to be uploaded to Claude.\n- **Assert the whole of a protected section,** not its heading and points (H1F5-C01: a note placed inside H-1's section 2A passed a builder that checked only part of it).\n- **A score's ranking claims need their exact conditions** (W1-C01): the same strictly increasing function of each number's count over the same draws ranks like counting; count-only scores in general need not.\n- **Changing a covariate is not ranking-preserving** (W2-B01, a BLOCKER): v0.1 of wave 2 claimed a least-squares slope on harmonic numbers ranks exactly as Method A's logistic slope on ln(age); the reviewer proved the reversal with an exact witness. Prove an equivalence, or search for a witness; never assume one.\n- **Every loop that waits for a condition needs a proved exit for every input** (W2R1-C01): an interval narrowing until it excludes zero never does at exactly zero. Test exact zero separately, and add a cap that refuses as an error.\n- **Hand-written test expectations go wrong too** (two in wave 2's first helper tests; the code was right). Compute them with a tool.\n- **Run Python 3.15 checks in a venv with the project's dependencies;** a bare interpreter fails every module on `numpy` and `psutil` (wave 2, before the evidence run).")
# ---------------------------------------------------------------- section 9
rep("and starts from the template, `doc/METHOD_TEMPLATE/` (draft 1; README and checklist), as E_6 and E_3/E_4 did:",
    "and starts from the template, `doc/METHOD_TEMPLATE/` (draft 3; README and checklist), as every method since E_6 has:")
rep("E_6 proved the pattern and E_3/E_4 used it for a pair sharing a helper; template draft 2 (section 10) folds in what they taught. The owner's two further methods are Methods A and B of `doc/GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md` (which supersedes the pre-exploratory `GASI_thought_experiments_possibly_unexplored_areas.md`). R2 already lists close relatives: A is near E_17 (and E_19), B near E_45 (and E_27, E_32). They become those methods' specifications, not new E-numbers.",
    "E_6 proved the pattern; E_3/E_4 and waves 1 and 2 used it, each wave with a shared helper and a generator for its method folders and contract data, so several methods travel in one package. Template draft 3 folds in what they taught. The owner's Methods A and B (`doc/GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md`) are catalogue methods, not new E-numbers: Method A's predictor is E_17's `HAZARD_LOGAGE_SIGN_V1` (installed in wave 2), and its diagnostics A1-A5 are a later package after WF-1 (W2-3); Method B becomes E_45's specification in wave 3.")
# ---------------------------------------------------------------- section 10 (rewritten)
old10 = section(t, '## 10. Next work, in order (planned; the owner decides each step)', '---\n\n## 11.')
new10 = """## 10. Next work, in order (planned; the owner decides each step)

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

"""
rep(old10, new10)
# ---------------------------------------------------------------- appendix A
rep("| H-2 v1r5 (current reviewer handover until v1r6 is installed) | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r5.md`, `67a1b3eaa3e1f51415eceba513fd7e1a39de91619296f0efba97ba108570a094` |\n| H-1 v1r4 (predecessor) | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r4.md`, `2050e9363d841634ecf2a9c308d3efb1ed51b359fbdaf2aa3531a60eb1f1c16a` |",
    "| H-2 v1r6 (current reviewer handover until v1r7 is installed) | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r6.md`, `db40f40ef22995fc65a949243001858f1d7d1285713c9954531ae6b601fc5616` |\n| H-1 v1r5 (predecessor) | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r5.md`, `1214bd971058ddd6cc680526fd80375bdbbd6db17397e41ba4c14ae5467101e1` |\n| H-1 v1r4 | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r4.md`, `2050e9363d841634ecf2a9c308d3efb1ed51b359fbdaf2aa3531a60eb1f1c16a` |")
rep("| Register v0.16 | `doc/RATIFICATION_REGISTER_v0_16.md`, `d84fc3ddd5978f0a5529bad20f9db9d1f95142c7e06e3dd78599cc0d4fa1c220` |",
    "| Register v0.19 | `doc/RATIFICATION_REGISTER_v0_19.md`, `b3ae51fd162960b64a9d145a52646dceeb3aec5b91e4b359ad7166e5e4c8e6a0` |")
rep("| E_3/E_4 final package | `exchange/EX_057_Claude/E34_Install_v1.zip`, `9d9949d545dad0c32761e9d377f7e5c945a7b99a6909753b180eb56636ee15fc` |",
    "| E_3/E_4 final package | `exchange/EX_057_Claude/E34_Install_v1.zip`, `9d9949d545dad0c32761e9d377f7e5c945a7b99a6909753b180eb56636ee15fc` |\n| Wave 1 install manifest | `review/W1_Install_v1/INSTALL_MANIFEST_SHA256.txt`, `2126d8e069a705134799d1efdfac83878e0d87d4d1dab47416b528fb1027fd9f` |\n| Wave 1 final package | `exchange/EX_067_Claude/W1_Install_v1.zip`, `51c81eb0757b92eff321ceb24227fa1ffcee976d5c5d72e1dd1df146d9da30c2` |\n| Wave 2 install manifest | `review/W2_Install_v1/INSTALL_MANIFEST_SHA256.txt`, `9c2ad9fe2b40413ab689f0875e95044a3353aa0c7124dcbb5312b927935c8af7` |\n| Wave 2 final package | `exchange/EX_076_Claude/W2_Install_v1.zip`, `57ef34b67b8aa6cc023c5ea3d78c2940ab1a9875c3141626c5016355da53c429` |")
# ---------------------------------------------------------------- appendix B (rewritten)
oldB = section(t, '## Appendix B. Changes in v1r5', '*End of H-1.*')
newB = """## Appendix B. Changes in v1r6

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

"""
rep(oldB, newB)

for old, new in E:
    c = t.count(old)
    assert c == 1, (c, old[:80])
    assert new.isascii(), old[:60]
    t = t.replace(old, new)
assert section(t, '### 2A. The owner\'s foundational points', '---\n\n## 3.') == S2A
assert t.endswith('*End of H-1.*\n') and '\r' not in t
open(out, 'wb').write(t.encode('ascii'))
print(len(E), 'edits;', out, hashlib.sha256(t.encode()).hexdigest(), len(t.splitlines()), 'lines; section 2A',
      len(S2A.encode()), 'bytes unchanged')
