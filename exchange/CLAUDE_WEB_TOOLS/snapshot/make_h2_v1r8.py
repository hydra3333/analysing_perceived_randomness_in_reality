"""H-2 v1r8 from the installed H-2 v1r7 by counted edits (Claude, 1 Nov 2026, for the snapshot).

The reviewer chat that started on 30 October 2026 continues; v1r8 brings its handover's status, checkpoint, safety-
status, cold-start and change-control facts up to the snapshot, and adds (outside the protected region) the
clarification asked for in the reviewer's takeover finding H2-TAKEOVER-O01 (register v0.21). The protected
reviewer-rights region (from the line starting '## 2.' to just before the line starting '## 4.') must stay
byte-identical: 7,676 bytes, SHA-256 70e50dc3...; the builder asserts it. Everything outside it stays US-ASCII.
Placeholders `[[FILL: ...]]` are filled at finalisation.
Usage: python3 -I make_h2_v1r8.py H2_v1r7 OUT
"""
import hashlib, re, sys

src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == 'a59ab8504d0d63d852d66efcc9491a05d3329656eb5164eef682df57da60ec38'
RIGHTS_SHA = '70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db'


def rights(b):
    i = b.index(b'\n## 2.') + 1
    j = b.index(b'\n## 4.') + 1
    return b[i:j]


assert len(rights(raw)) == 7676 and hashlib.sha256(rights(raw)).hexdigest() == RIGHTS_SHA
t = raw.decode('utf-8')
assert '\r' not in t
E = []


def rep(old, new):
    E.append((old, new))


def between(head, nxt):
    i = t.index(head)
    return t[i:t.index(nxt, i)]


# ---------------------------------------------------------------- header
rep("# Predictive Randomness - ChatGPT Independent Reviewer Handover H-2 v1r7 (DRAFT)",
    "# Predictive Randomness - ChatGPT Independent Reviewer Handover H-2 v1r8 (DRAFT)")
rep("**Repository target:** `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r7.md`",
    "**Repository target:** `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8.md`")
rep("**Status:** **DRAFT, for owner ratification with H-1 v1r6 and Register v0.20; NOT installed.**",
    "**Status:** **DRAFT, for the reviewer's check and owner ratification with H-1 v1r7 and Register v0.23 (the snapshot); NOT installed.**")
rep("**Prepared:** 30 October 2026 (Australia/Adelaide).",
    "**Prepared:** 1 November 2026 (Australia/Adelaide).")
rep(t[t.index('**Author:** **Claude (the primary designer and coder), on the project owner'):t.index('\n', t.index('**Author:** **Claude (the primary designer and coder), on the project owner'))],
    "**Author:** **Claude (the primary designer and coder), for the snapshot the owner requested on 1 November 2026, before a planned Claude chat switch.** The reviewer chat that started on 30 October 2026 from H-2 v1r7 continues in role; this edition only brings its status, checkpoint, safety-status, cold-start and change-control facts up to date, keeps the reviewer-rights region byte-identical, and adds no reviewer rule. **Unlike v1r7, this edition goes to the current reviewer chat for a factual check before the owner ratifies it; report any factual error, omission, or wording that would narrow your independence as a normal finding, and the owner decides.**")
rep("**Predecessor:** owner-ratified and installed H-2 v1r6 (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r6.md`), canonical LF SHA-256 `db40f40ef22995fc65a949243001858f1d7d1285713c9954531ae6b601fc5616` (DOC-7, commit `8defe9d`, per Register v0.17).",
    "**Predecessor:** owner-ratified and installed H-2 v1r7 (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r7.md`), canonical LF SHA-256 `a59ab8504d0d63d852d66efcc9491a05d3329656eb5164eef682df57da60ec38` (DOC-8, commit `03f7da4`, per Register v0.21).")
rep("**Rights preservation:** the complete `## 2.` through immediately before `## 4.` region remains **7,676 bytes, byte-for-byte identical** to H-2 v1r6, H-2 v1r5 and H-2 v1r4; SHA-256 `70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db`. **No reviewer-rights change is proposed.** Historical \"proposed\" wording embedded in that protected block is deliberately untouched; the owner's subsequent ratifications govern its status.",
    "**Rights preservation:** the complete `## 2.` through immediately before `## 4.` region remains **7,676 bytes, byte-for-byte identical** to H-2 v1r7, v1r6, v1r5 and v1r4; SHA-256 `70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db`. **No reviewer-rights change is proposed.** Historical \"proposed\" wording embedded in that protected block is deliberately untouched; the owner's subsequent ratifications govern its status. **Clarification (H2-TAKEOVER-O01, outside the protected region):** R-8 to R-11, and the safeguards in section 3 that the protected text still calls \"proposed\", have been OWNER-RATIFIED since 27 October 2026 (H-2 v1r2; the register records it). They bind as fully as R-1 to R-7.")

# ---------------------------------------------------------------- section 0
rep(between('## 0. Authority and checkpoint (30 October 2026)', '## 1. Reviewer'), """## 0. Authority and checkpoint (1 November 2026)

- **Roles:** Claude is the primary designer/coder; ChatGPT is the independent other-model reviewer; the owner alone ratifies and controls repository installation, scientific release and gated tests. The role transition was effective at `d36735da`. Claude Code is an owner-authorised local task runner, **not** a designer, coder or independent reviewer. Its scope and write permissions remain those actually ratified, not inferred from its availability. **A new Claude chat takes over from the current one after the snapshot**, from H-1 v1r7; it has the same role and the same obligations to you. You continue unchanged.
- **Current handovers and register:** H-1 v1r6 and H-2 v1r7 are operative; Register v0.22 is owner-ratified and installed at `2b1e7e3` (DOC-9). Claude drafted H-1 v1r7, this H-2 v1r8, Register v0.23 and Architecture v0.9 for the snapshot, with the other documents listed in Register v0.23, for your review and the owner's ratification. No successor is operative merely because it is drafted or placed in `exchange/`.
- **Code milestone since v1r7** (each reviewed by you, rehearsed by Claude Code, installed by the owner and verified by Claude from GitHub):
  - **REL-1 v2** (`6a1bed9`): the 39 revision-1 variants of E_2, E_3, E_4, E_6, E_7, E_8, E_9, E_10, E_17, E_18 and E_19 released in both games (T009);
  - **WF-1A v2** (`0d98706`): the walk-forward driver; **`ENABLE_CONTRACT_REAL_DEVELOPMENT` turned on** by the owner's decision WF1-3, so contract runs may read the development masters (never the holdout) (T010);
  - **E1R2 v3** (`86d12ea`): CODE-3's retirement tooling, E_1 revision 1 archived under `archive/methods/E_001/r1/`, and E_1 revision 2 real-capable and released (T011);
  - **WF-1B v3** (`24d192f`): the R3 stage-2 scorer and ranking report (`src/evaluation/`, `Run_Method_Rankings.bat`), N1 (R = 10,000) and its seed-policy records (EX_104-EX_107 design; EX_108-EX_113 code; T012 and T013 stopped safely, T014 PASS);
  - **PERF-1** (EX_114; EX_115 PASS with no finding): the exact Clopper-Pearson interval found fast with bit-identical results, and the report tool's count-only progress lines; T015 PASS (report `9eeb843`); installed by the owner at `3fce327` (1 November 2026), verified by Claude from GitHub.
  All 40 variants are `SUPPORTED`; no `IN_DEVELOPMENT.txt` flag remains. The suite is 471 tests (36 modules).
- **Real-data runs so far** (each a separate owner authorisation): the first walk-forward batches, Powerball `wf-3347ad1160df45faaaab1e2eedcedd0f` (targets 1145-1576, 17,280 runs) and Oz Lotto `wf-a75988650fb04cc399f8f7409ea27243` (1475-1693, 8,760 runs), all `SUCCESS` (31 October 2026); the first ranking reports (1 November 2026): Oz Lotto 1474-1693 COMPLETE (`441daf2`; before PERF-1, about 4.5 hours); Powerball 1286-1576 first refused at its plan check (its two committed batch records had been rewritten with CRLF on the owner's computer; restored by the owner; R-011's `.gitattributes` rule is in the snapshot), then COMPLETE with PERF-1 in about 26 minutes (`608025c`). In both games no family figure departs from fair draws (descriptive development evidence only; register v0.23 quotes the family figures). Their record contents are not reviewer evidence unless the owner supplies them; the reports exclude every holdout draw.
- **The N1 seed:** the owner brought the announced pulse forward to `2026-10-31T10:30:00.000Z` (EX_103) and approved policy `N1_ROOT_NIST_C2_20261031T1030Z_V1` (pulse 2007128; signature `NOT_PERFORMED` under WF1-12). You compared the owner's saved file with the record in EX_111. The 6 November policy is `REPLACED_BEFORE_PULSE`, never fetched.
- **Safety status:** three execution switches stay `False` (`ENABLE_PROCESS_TERMINATION`, `ENABLE_SCIENTIFIC_COORDINATION`, `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE`); the fourth, `ENABLE_CONTRACT_REAL_DEVELOPMENT`, is True since WF-1A. The scientific-result consumer allowlist is empty, and the unresolved-orphan/no-status/no-kill rules remain binding. No master update, Mode H, FINAL or holdout access is authorised.
- **The owner's decisions since v1r7 that bear on review** (the register records each): WF1-1..WF1-13; ER-1..ER-6; WORKERS-1 (worker limits to the logical processor count, default half) moved by **WB-0** into a separate package **WF-1C**, which must carry EX_101's and EX_105's obligations in full (EX_107); WB-1 (descriptive real-results tables first); WB-2 (the seed in WF-1B); the deferrals of EX_111 O01 and EX_113 O02; **PERF-1** approved as a small item brought forward from the deferred performance study and reviewed once after coding (owner's choice of process); **HX-1** (Mode H scores all ten holdout draws per game, Powerball 1585 and 1586 flagged for the recorded exposure; until Mode H all ten are treated as unseen); and the order: snapshot, then Mode H with the results update and the prospective mode (goal: next-draw forecasts for the week of 9 November 2026), then WF-1C, then the waves.
- **Review process:** record each REVIEWER-DECIDED disposition; Claude checks and reports exceptions (none so far, through EX_115). Document-only installation stays simplified; code still requires HIGH-tier review, Windows acceptance and post-push Git verification. A final package differing from its reviewed candidate only in its verifier's base may sit in `CLAUDE_CODE_WORKING_FOLDER_TREE/packages/` (WF-1A; Register v0.22); this is **not** a general code-review waiver.
- **Exchange and working lists:** the shared EX sequence has reached **EX_115** (your PERF-1 PASS); the snapshot's review request is EX_116, and your reply is EX_117. `exchange/OWNER_REMINDERS.md` (R-001..R-012) and `exchange/OWNER_ROADMAP.md` are informal owner working lists, **not governing rules or release authority**. Follow the installed `exchange/README.md` and verify the next free EX number at handoff.

**Evidence boundary:** Claude verified the `6a1bed9`, `0d98706`, `86d12ea` and `24d192f` commits and the T009-T014 reports from GitHub (Registers v0.22-v0.23); the owner's Windows runs remain **owner-reported**. Your own independent reproductions are in your review records (`exchange/EX_*_ChatGPT*` and `review/`), with the limits each one states. This edition was drafted by Claude, so **none of its checkpoint facts is reviewer-verified** until you check them. Check current Git and the installed register; do not misstate who verified what.

**Matters for review raised by Claude's cold-read probes (1 November 2026; Register v0.23, R-012):** two fresh helpers, reading only the repository, found that the two readers accept only the single version-1 master ledger line (so any results update stops every run and report until a version-2 reader is designed), that `HOLDOUT_OPENED_<GAME>.json` is defined only in code, that the updater's launcher runs `update` when given no arguments, and that the two-site checker's default mode drives The Lott's website automatically. Expect the first three in the Mode H, update and prospective design; the snapshot records the fourth as never to be run that way.

""")

# ---------------------------------------------------------------- section 5 (safety status facts only)
rep("Synthetic and real result trees remain segregated; consumer allowlist empty; all four switches closed unless separately approved.",
    "Synthetic and real result trees remain segregated; consumer allowlist empty; three switches closed and the fourth (`ENABLE_CONTRACT_REAL_DEVELOPMENT`) open only for owner-authorised development runs since WF-1A, none changed unless separately approved.")

# ---------------------------------------------------------------- section 6
rep(between('1. **Establish actual authority:**', '2. **Read the binding contracts'),
    "1. **Establish actual authority:** obtain the owner-verified HEAD (at least `24d192f`, verified by Claude, and the later snapshot install of this edition), the latest installed register (v0.22 at this checkpoint, installed at `2b1e7e3`; v0.23 once installed), H-1 v1r7 or its installed successor, this H-2, H-3, the ratified roles position, relevant package sources/hashes and the latest owner decisions. If the tree, report or register cannot be fetched, state the limitation rather than guessing. Do not treat H-1 v1r7, H-2 v1r8 or Register v0.23 as installed before ratification and commit verification.\n")
rep("E_6, E_3/E_4, wave 1 (`doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md`) and wave 2 (`doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md`) installed specifications, the owner's Methods A and B proposal (`doc/GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md`) and `doc/METHOD_TEMPLATE/` (draft 3) when reviewing new methods.",
    "E_6, E_3/E_4, wave 1 (`doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md`) and wave 2 (`doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md`) installed specifications, the owner's Methods A and B proposal (`doc/GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md`) and `doc/METHOD_TEMPLATE/` (draft 4 from the snapshot) when reviewing new methods; and for releases, walk-forward, scoring and the seed: `doc/Predictive_Randomness_Releases_and_WF1_Design_v0_1r1.md`, `doc/Predictive_Randomness_CODE3_and_E1_Revision2_Design_v0_1r2.md` and `doc/Predictive_Randomness_WF1B_Supplement_Design_v0_1r1.md`. The owner's `doc/Deferred_Performance_Engineering_Proposal_v0_1.md` is owner-committed, unreviewed and authorises nothing.")
rep("Construct small exact witnesses, and test every exit.",
    "Construct small exact witnesses, and test every exit. **Your own later catches show the same standard:** WF1-R3-B01 (a driver continuing after a data-admission failure), WF1A-R2-B01 (resume binding neither master pin nor batch), E1R2-R3-B01 and E1R2-R2-B01 (an interim state not fail-closed; an archive check missing paths built in pieces), EX_105 B01 (parallel STOP admission and parent loss) and WF1B-R2-B01 (seed-policy binding).")
rep(between('3. **Inspect the next owner gate:**', '4. **Hand back review evidence compactly:**'),
    "3. **Inspect the next owner gate:** after the snapshot the owner's sequence (`exchange/OWNER_ROADMAP.md` items 10c, 10d and 11 on) is the Mode H, results update and prospective (next-draw) design, designed together (R3 sections 3, 6.2 and 10, V1; the Mode H store, the version-2 reader, the `HOLDOUT_OPENED` record and R3-D20's timing proof are OPEN); then WF-1C (workers, with EX_101's and EX_105's obligations); then wave 3 (E_27, E_45 as Method B, E_26, E_28), the non-local means discussion, waves 4-11 and the ensembles; Method A's diagnostics A1-A5 are a separate package (W2-3). Each still needs its own gates. New experiments merit open-minded R-3 scrutiny and independent numerical oracles where justified, then separate R-2 and owner acceptance. Do not confuse mathematical coherence, exploratory structure and prospectively calibrated prediction. Do not infer permission for T12, process control, a further real-history run or report, FINAL, holdout access or publication merely from the latest installation.\n")
rep("Check `exchange/README.md`, the maximum committed EX number (at least EX_076 when drafted), and sender-collision history before naming the next reply.",
    "Check `exchange/README.md`, the maximum committed EX number (at least EX_115 when drafted), and sender-collision history before naming the next reply.")

# ---------------------------------------------------------------- section 7
old7 = t[t.index('## 7. H-2 v1r7 change control'):]
new7 = """## 7. H-2 v1r8 change control

- **Baseline and scope:** based on the owner-ratified H-2 v1r7 LF bytes (SHA-256 above), by counted edits in a builder that asserts the rights region. The checkpoint advances from wave 2 at `b61b1a2` to REL-1 (`6a1bed9`), WF-1A (`0d98706`), E1R2 (`86d12ea`), WF-1B (`24d192f`) and PERF-1, all reviewed by you; the register records each round (EX_077-EX_115) and rehearsal (T009-T015). Section 5 changes only the switch-status fact. There is **no substantive new reviewer rule or scientific authorisation**.
- **Authorship:** drafted by Claude for the snapshot, with you in role; you check it before ratification. The reviewer's own words elsewhere in this file are unchanged.
- **Protected reviewer rights:** unchanged **byte-for-byte**, 7,676 bytes with the recorded SHA-256. The H2-TAKEOVER-O01 clarification is in the header, outside the region. Any future modification requires explicit owner ratification. This includes R-1 through R-11, the T-05 note and the reviewer-discretion text.
- **Review status:** awaiting your factual check and the owner's ratification and documentary installation; H-2 v1r7 remains operative until then. Verify the post-push Git blobs rather than treating an EX commit as installation.

**End of H-2 v1r8 DRAFT - NOT OWNER-RATIFIED.**
"""
rep(old7, new7)

for old, new in E:
    c = t.count(old)
    assert c == 1, (c, old[:80])
    assert new.isascii(), old[:60]
    t = t.replace(old, new)
b = t.encode('utf-8')
assert rights(b) == rights(raw), 'the protected reviewer-rights region changed'
assert hashlib.sha256(rights(b)).hexdigest() == RIGHTS_SHA
assert '\r' not in t and t.endswith('NOT OWNER-RATIFIED.**\n')
i = b.index(b'\n## 2.') + 1
j = b.index(b'\n## 4.') + 1
assert (b[:i] + b[j:]).isascii()
fills = re.findall(r'\[\[FILL: [^\]]*\]\]', t)
open(out, 'wb').write(b)
print(len(E), 'edits;', out, hashlib.sha256(b).hexdigest(), len(t.splitlines()), 'lines; rights region',
      len(rights(b)), 'bytes', hashlib.sha256(rights(b)).hexdigest()[:16], ';', len(fills), 'placeholders')
for f in fills:
    print('  ', f)
