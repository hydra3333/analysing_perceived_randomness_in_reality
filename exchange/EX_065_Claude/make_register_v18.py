"""Draft register v0.18 from the installed register v0.17 by counted in-place edits (Claude, 30 Oct 2026).

Records: the handover round's installation (DOC-7) and the reviewer's EX_060 review with H1F5-C01; the owner's
revised order of work; the wave 1 design review (EX_061 to EX_064) and the owner's decisions W1-1..W1-6; and
the wave 1 package (E_7, E_8, E_9, E_10, their shared helper and the template's draft 2), installed with this
register. Every old string must occur exactly once; inserted text is ASCII. The input is the Git blob of
doc/RATIFICATION_REGISTER_v0_17.md (268e72b2...9d17).
Placeholders, finalised after review and the owner's ratification: "RATIFICATION CANDIDATE" (version line)
and [T12-W1] (the owner's T12 decision for this package's rehearsal and install).
Usage: python3 -I make_register_v18.py REGISTER_v0_17 OUT_v0_18
"""
import hashlib, sys

src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '268e72b2a435628550079682040ae2eab69b5a08baa3241e4ee9e47e54499d17'
t = raw.decode('utf-8')
assert '\r' not in t

NEW_SECTION = """## The handovers installed, the owner's revised order, and wave 1 (register v0.18)

Paths in this section are under `doc/`, except those beginning `review/`, `exchange/`, `src/`, `tests/` or `CLAUDE_CODE_WORKING_FOLDER_TREE/`, which are from the repository root. In this section, "this register" means register v0.18.

**The handover round's review (EX_058 to EX_060).** The verdict on H-1 v1r5 and register v0.17 is `review/Independent_ChatGPT_H1_v1r5_Register_v17_Review_v0_1.md` (LF copy, `1a20c96264c54957152c0d3cf27562f0abe5fc0470af82a1bf263cdaa2fb2fa6`), installed at `8defe9d`.
- **H1F5-C01 (CORRECTION, FIX AND PROCEED) was Claude's error.** A note pointing to the owner's purpose restatement had been placed inside H-1's section 2A, and Claude's builder had checked only the section's heading and seven points, so the claim "section 2A is unchanged" was not true of the whole section.
  - Claude moved the note unchanged to just before the section, as the reviewer specified.
  - The result is `1214bd97...01e1`, the reviewer's own reconstruction.
  - The whole section is byte-identical (1,359 bytes), and the builder now asserts the whole section.
  - Register v0.17 changed only in its two H-1 references.
- **The other two dispositions:** register v0.17 CONTENT PASS, and H-2 v1r6 r1 adopting all six of Claude's H2F6 items with the rights region unchanged.
- **REVIEWER-DECIDED, checked by Claude, no exception to report:** HROUND-060-RD-01..03.

**The handovers installed (DOC-7)** at commit `8defe9d7fbc0a1f46ddda14cac4355970e348761` (30 October 2026; parent `eed7485`), by the document-only procedure.
- The owner's log is clean.
- Claude checked all 6 files from GitHub against the ratified bytes: H-1 v1r5, H-2 v1r6 (r1, `db40f40e...5616`), register v0.17 (`268e72b2...9d17`), and the review copies of EX_056 and EX_060 with Claude's fact check.
- H-1 v1r5 and H-2 v1r6 are now the operative handovers.

**The owner's revised order of work (OWNER-DECIDED, 30 October 2026; it replaces register v0.17's order of the same day).** The owner asked whether other catalogue methods should come first. Claude proposed the order below, with a plain description of every method, and the owner agreed:
1. **Wave 1,** light counting methods, with the template's draft 2: E_7, E_9, E_10, E_8.
2. **Wave 2,** gaps between appearances, sharing one helper: E_2 (one of the owner's original six), E_17 as Method A, E_19, E_18.
3. **Releases and WF-1:** switch the methods on, then the first real measured results over past draws, walk-forward, with the scorer.
4. **Wave 3,** look-alike past draws: E_27, E_45 as Method B, E_26, E_28.
5. **The non-local means discussion** (the owner chose to keep it here, rather than after wave 11).
6. **Waves 4 to 11** (`exchange/OWNER_ROADMAP.md` lists every method):
   - 4: E_5 and the rest of E_11 to E_16, with E_12, E_13 and E_16 each in its own package;
   - 5: curves and cycles;
   - 6: numbers acting together;
   - 7: drawn order;
   - 8: information and nonlinear methods;
   - 9: machine learning, which needs a dependency change and the seed policy;
   - 10: the pilot-wave-inspired family;
   - 11: outside data.
7. **The ensembles,** E_55 and E_56, last.

**Reasons given to the owner for the change:**
- E_2 and E_5 are owner originals still unbuilt.
- The heavy members of E_7 to E_16 deserve their own packages.
- Methods A and B pair with their simplest relatives.
- After about ten methods, measuring them on real past draws is worth more than adding more.

**The wave 1 design review (EX_061 to EX_064).** The design note is `Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md`, installed with this register.
- **EX_062** found it scientifically sound, with one shared CORRECTION, W1-C01, which was Claude's overstatement.
  - The note and the template README said that a score depending only on a number's count ranks exactly like counting. That holds only for the same strictly increasing function of each count over the same draws. Count-only scores need not be monotonic, and deliberately non-monotonic methods are not excluded.
  - The reviewer also checked E_8's moment estimator algebraically, and independently on 10,000 exhaustive synthetic histories.
- **EX_064** passed the corrected design v0.1r1 and README unchanged. Both of the reviewer's optional items were adopted: the reference script asserts E_8's cap example, and the template builder pins both draft-1 files.
- **The review copies,** installed with this register:
  - `review/Independent_ChatGPT_Wave1_R3_and_Template_Draft2_Review_v0_1.md` (LF, `76818fab4d16988ea89a0e52b55c42ada46163e5d10da288a4b558285aad1a21`);
  - `review/Independent_ChatGPT_Wave1_v0_1r1_Focused_RECHECK_v0_1.md` (LF, `780513e0b1f36ac1981f5b2e6476b985bec266a8ee01fa0fd2fb49b70d81763a`).
- **REVIEWER-DECIDED, checked by Claude, no exception to report:** W1-RD-01..07.

**Owner decisions W1-1..W1-6 (OWNER-DECIDED 30 October 2026, as recommended, with the reviewer's support):**
- W1-1: one shared counting helper, `_common/occurrence_counts.py`, versioned with the four methods;
- W1-2: the 12 fixed variants of the design note's section 6;
- W1-3: E_7's full-history variant is kept as the pure calibration variant, although it ranks like E_1;
- W1-4: E_9 and E_10 are score-only; E_7 and E_8 publish marginal probabilities, with their limits stated;
- W1-5: the template's draft 2;
- W1-6: E_8 uses moment estimates, not a sampled Bayesian fit.

**The wave 1 package (installed with this register).**
- **What it adds:**
  - the helper `src/methods/_common/occurrence_counts.py`, revision 1;
  - `src/methods/E_007/`, `E_008/`, `E_009/` and `E_010/`, each with `variants.py`, `contract.py` and `IN_DEVELOPMENT.txt`;
  - 24 declarations and 24 `FORMULA_OPEN` entries;
  - `tests/test_occurrence_counts.py` (8 tests) and `tests/test_wave1_frequency.py` (18 tests);
  - the design note v0.1r1 and its reference script;
  - review evidence.
- **What it replaces:**
  - `src/methods/Method_Contract_Runner.py`: four imports and four `ADAPTERS` entries;
  - the template's `README.md`, `METHOD_SPECIFICATION_TEMPLATE.md` and `method_folder/contract.py.txt`, which become draft 2. The README has one bullet more than the reviewed draft 2 r1, from a finding in the code (below).
- **What it does not change:** the contract libraries, the reader, the coordinator, E_1, E_3, E_4, E_6 and their helpers, the launchers and owner tools, and the four methods' `NOT_YET_SPECIFIED` placeholders. The four switches stay False, and the allowlist stays empty.
- **The four methods cannot run** once this is installed: every request is refused with `NOT_SUPPORTED` before any data is read, and the flags are present.
- **A finding from the code, for the template** (the owner's keep-current rule):
  - E_8's three period lengths give identical scores whenever its weight is 0 and their whole periods cover the same draws. For example, Oz Lotto's 218 draws hold 16 quarters, 8 half-years or 4 years: the same 208 draws.
  - This follows from the design, and the tests check that variants differ exactly where their correct values differ.
  - The README gains one "things that bite" bullet saying so.
- **Review and acceptance:**
  - the owner's Windows run of all 268 tests comes before the commit;
  - E2R-T12 for this package's rehearsal and install run: [T12-W1];
  - Claude verifies the commit from GitHub.

  The results are recorded after installation; this register does not predeclare them.

**Out-of-date statements (register v0.18).** This register prevails, and the files are not edited:
- Register v0.17, "installed with this register" for H-1 v1r5 and H-2 v1r6: done, at `8defe9d`, as above.
- Register v0.17 and H-1 v1r5 section 10, the owner's order of work: replaced by the revised order above.
- H-1 v1r5 section 7.4, "242 offline tests in 17 modules": 268 in 19 once the wave 1 package is installed.
- The template's draft 1 (`METHOD_TEMPLATE/`), where draft 2 replaces it.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md` | Claude; reviewed by the ChatGPT reviewer chat | Design PASS unchanged (W1-RD-05); owner decisions W1-1..W1-6 as above; installed with this register; `06b491225812e14962aef99e299cbd6c003be68bb5a73425e566f1b1fe685060` |
| `RATIFICATION_REGISTER_v0_17.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 30 Oct 2026; installed at `8defe9d`; superseded by this register; `268e72b2a435628550079682040ae2eab69b5a08baa3241e4ee9e47e54499d17` |

"""

EDITS = [
    ('**Register version:** v0.17 OWNER-RATIFIED 30 October 2026, recording',
     '**Register version:** v0.18 RATIFICATION CANDIDATE (drafted 30 October 2026), recording the handover installation, the owner\'s revised order of work, the wave 1 review and owner decisions, and the wave 1 package; v0.17 OWNER-RATIFIED 30 October 2026, recording'),
    ("This register, H-1 v1r5 and H-2 v1r6 are installed together by the document-only procedure.",
     "This register, H-1 v1r5 and H-2 v1r6 are installed together by the document-only procedure. For v0.18, the handover installation commit `8defe9d` was verified by Claude from GitHub. The wave 1 package and this register are installed together, in one commit identified after installation; the owner's Windows results for it are recorded after installation."),
    ('\n## Interpretation and verification\n',
     '\n' + NEW_SECTION + '## Interpretation and verification\n'),
]
for old, new in EDITS:
    n = t.count(old)
    assert n == 1, (n, old[:80])
    assert all(ord(c) < 128 for c in new), old[:60]
    t = t.replace(old, new)
open(out, 'wb').write(t.encode('utf-8'))
print(out, hashlib.sha256(t.encode()).hexdigest(), len(t.splitlines()), 'lines')
