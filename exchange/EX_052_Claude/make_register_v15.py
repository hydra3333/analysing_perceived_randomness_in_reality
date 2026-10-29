"""Draft register v0.15 from the installed register v0.14 by counted in-place edits (Claude, 30 Oct 2026).

Records: the document-round installation (DOC-6) and its clean-up, the owner's restatement of the project's
purpose, the owner's plan and decisions of 29-30 October 2026 (including D6-1..D6-5), the reviewer's E_6
review (EX_051), and the E_6 package, installed with this register. Every old string must occur exactly once;
inserted text is ASCII. The input is the Git blob of doc/RATIFICATION_REGISTER_v0_14.md (74d2ae89...bfa4).
Placeholders, finalised after review and the owner's ratification: "RATIFICATION CANDIDATE" (version line)
and [T12-E6] (the owner's T12 decision for this package's rehearsal and install).
Usage: python3 -I make_register_v15.py REGISTER_v0_14 OUT_v0_15
"""
import hashlib, sys

src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '74d2ae89a16d2c7a971db1b62e89c3e9aa7f6a2803a9102516507fa705e2bfa4'
t = raw.decode('utf-8')
assert '\r' not in t

NEW_SECTION = """## E_6, the first new method, and the new-method template (register v0.15)

Paths in this section are under `doc/`, except those beginning `review/`, `exchange/`, `src/`, `tests/` or `CLAUDE_CODE_WORKING_FOLDER_TREE/`, which are from the repository root. In this section, "this register" means register v0.15.

**The document round installed (DOC-6).** H-1 v1r4, H-2 v1r5 and register v0.14 were installed by the document-only procedure at commit `337b5b20f7eb8c642f42e24227fe4884a7a880fc` (29 October 2026; parent `dceab36`). Claude verified from GitHub that the six intended files are exactly the ratified bytes:
- H-1 v1r4 `2050e936...c16a`;
- H-2 v1r5 `67a1b3ea...a094`;
- register v0.14 `74d2ae89...bfa4`;
- the three review copies.

**Departure, recorded and fixed.** The owner's first `git status --short` was not empty: four EX zips downloaded into `review/` (`EX_047_ChatGPT`, `EX_047_Claude`, `EX_048_Claude`, `EX_049_ChatGPT`) were staged and committed too.
- Claude checked that each is byte-identical to its copy in `exchange/`.
- The owner removed them at `f9de54ad4b877bf45a5e4d8bcca2e4b4b5e3f752`, which makes 4 deletions and nothing else; Claude verified this from GitHub.

The rule stands: if the first status line shows anything, stop and ask.

**Older duplicates, left in place.** `review/` also holds 10 earlier copies of EX messages from the owner's snapshot commits: `EX_026_Claude.md` twice, one with a "(1)" suffix, and `EX_027` to `EX_034`. Each matches its `exchange/` copy, apart from line endings in the `.md` files. The owner may remove them later.

**The project's purpose, restated (owner-reported, 30 October 2026).** The owner put the purpose to the reviewer chat: to detect, predict and measure unusual fluctuations or patterns in apparent randomness by mathematically valid means. That includes deliberately unusual ones, for example from quantum physics, or relaxed assumptions. The reviewer chat agreed, with six working principles:
1. be exploratory;
2. do not reject an idea because conventional theory predicts it should fail;
3. distinguish mathematical validity from statistical orthodoxy;
4. measure what actually happens: a method can fail as a predictor yet succeed as an exploratory instrument;
5. protect the integrity of evaluation (N-1, frozen forecasts, TOP/WORST, null-world diagnostics, the sealed holdout);
6. investigate surprises rather than explain them away, without reading an analogy as a mechanism.

This restates the owner's foundational points (H-1 v1r4 section 2A) and changes no rule. The exchange took place in the owner's chats, not in an EX file.

**The owner's plan (OWNER-DECIDED, 29-30 October 2026).**
1. E_6 first, as the lead method and the first real use of the new plumbing, with a draft template for later methods.
2. Then E_3 and E_4 together, sharing one Chebyshev fitting helper with three fit types (least squares, interpolation and minimax), in one review round.
3. Then the E_7-E_16 frequency family as a batch made from the template.

Each step keeps its own design review, code review and owner go-ahead.
- **The template** keeps only what changes from method to method; safety logic stays in the shared library.
- **Variant settings are fixed in a method's specification before its code.** By E2R-R14A, any later change to a released method's code is a new revision.
- **Claude Code** rehearses each install. Whether it may try building a method from the template is asked when the batch is reached; that needs a rulebook change.

**The E_6 review (EX_050 and EX_051).**
- **What was reviewed:** the design note `Predictive_Randomness_E6_Specification_and_Method_Template_Design_v0_1.md` (`cef16b44fb7088ec018e0a8d6f233231c04e3fe6d5431cf0a2e604ad8f6fc82e`), installed with this register, and Claude's speculative candidate (`E6_Install_v1_candidate.zip`, `098214c1...6b66`).
- **The verdict** (`review/Independent_ChatGPT_E6_R3_R2_Review_v0_1.md`, LF copy, `ee0613f618738b219cd2ba33b03fd16148abfc471bef66140e1c583822e6b4cb`, installed with this register):
  - R-3 design PASS unchanged;
  - R-2 HIGH-tier candidate PASS, with 0 BLOCKER, CORRECTION or RECONSIDER;
  - 199 of 199 selected offline tests independently reproduced, run module by module. This is not a whole-suite run: the 10 real-master tests and T12 are reserved for the owner's run.
- **REVIEWER-DECIDED, checked by Claude, no exception to report:**
  - E6-RD-01: design PASS unchanged;
  - RD-02: D6-1..D6-5 supported, for the owner's decision;
  - RD-03: the candidate PASS;
  - RD-04: the owner's Windows acceptance and the install checks are not replaced by the review.
- **The reviewer's non-blocking terminology note, adopted:** for lambda < 1, E_6's estimate is a discounted (power-likelihood) Beta update, not the plain Bayesian posterior; only lambda = 1 is the posterior mean. The package now labels the two decay variants accordingly:
  - fit version `BETA_BERNOULLI_DISCOUNTED_UPDATE_V1`;
  - their own calibration note;
  - a sentence in their registry texts and the code comments.

  `BETA_BERNOULLI_FULL_MEMORY_V1`'s declarations and entries are byte-identical to the reviewed candidate. Nothing else changed in the code or the tests, apart from one test that checks the fit version per variant. The reviewer receives the narrow diff with this register.

**Owner decisions D6-1..D6-5 (OWNER-DECIDED 30 October 2026).** The owner decided all five after seeing the reviewer's interim view, before its formal reply. EX_051 then supported all five unchanged.
- **D6-1:** a contract method needs no per-method entry file. The shared standalone runner is its entry, and its code lives in its own folder, `src/methods/E_<nnn>/`. This narrows NAMES-1 OPEN-N1 "A" for contract methods only; E_1's legacy entry file is unchanged.
- **D6-2:** E_6 revision 1 is approved at method level (R2 7.1):
  - an independent Beta-Bernoulli model for each number;
  - a prior centred on the fair-draw rate and worth one draw;
  - forgetting weight lambda^age;
  - exact rational arithmetic;
  - three fixed variants: lambda 1, 74/75 and 149/150, in both games.
- **D6-3:** the release plan: installed non-runnable; release 1 makes `BETA_BERNOULLI_FULL_MEMORY_V1` `SUPPORTED` and removes the flag; release 2 adds the two decay variants, registry only. Real-data contract runs stay off.
- **D6-4 (planning only):** real-data contract runs, a walk-forward driver and the R3 scorer, as a later reviewed package, WF-1. Nothing is authorised.
- **D6-5:** the new-method template, `doc/METHOD_TEMPLATE/`, as draft 1.

**The E_6 package (installed with this register).**
- **What it adds:**
  - `src/methods/E_006/`: the mathematics, the runner connection and `IN_DEVELOPMENT.txt`;
  - 6 declarations and 6 `FORMULA_OPEN` registry entries;
  - `tests/test_e6_beta_bernoulli.py` (20 tests);
  - the design note;
  - the template, 10 files under `doc/METHOD_TEMPLATE/`;
  - review evidence.
- **What it replaces:**
  - `src/methods/Method_Contract_Runner.py`: one import and one `ADAPTERS` entry;
  - `tests/test_e2r_contract.py`: the literal count of 124 registry chains becomes the count of installed chain folders;
  - `tests/test_e2r_dispatch.py`: "no `IN_DEVELOPMENT.txt` anywhere" becomes "flags only in unreleased method folders, never E_001".
- **What it does not change:** the contract libraries (CODE-1 and CODE-2), the reader, the coordinator and its 11 protected functions, E_1, the launchers and wrappers, the owner tools, and E_6's `NOT_YET_SPECIFIED` placeholder. The four switches stay False, and the allowlist stays empty.
- **E_6 cannot run** once this is installed: every request is refused with `NOT_SUPPORTED` before any data is read, and the flag is present.
- **Review and acceptance:**
  - the owner's Windows run of all 210 tests comes before the commit;
  - E2R-T12 for this package's rehearsal and install run: [T12-E6];
  - Claude verifies the commit from GitHub.

  The results are recorded after installation; this register does not predeclare them.

**Out-of-date statements (register v0.15).** This register prevails, and the files are not edited:
- Register v0.14, "installed with this register" for H-1 v1r4 and H-2 v1r5: done, at `337b5b2`, as above.
- H-1 v1r4 section 9, step 3, "the entry file ... its contract adapter": by D6-1, a contract method has no entry file of its own. Its connection to the runner is `contract.py` in its own folder, as `doc/METHOD_TEMPLATE/README.md` describes.
- H-1 v1r4 section 7.4, "190 offline tests in 14 modules": 210 in 15 once the E_6 package is installed.
- The E_6 design note v0.1, sections 1 and 2.2, "the posterior mean" for every variant: exactly so only for lambda = 1. For lambda < 1 it is a discounted (power-likelihood) Beta update, as above.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `Predictive_Randomness_E6_Specification_and_Method_Template_Design_v0_1.md` | Claude; reviewed by the ChatGPT reviewer chat | Design PASS unchanged (E6-RD-01); owner decisions D6-1..D6-5 as above; installed with this register; `cef16b44fb7088ec018e0a8d6f233231c04e3fe6d5431cf0a2e604ad8f6fc82e` |
| `RATIFICATION_REGISTER_v0_14.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 29 Oct 2026; installed at `337b5b2`; superseded by this register; `74d2ae89a16d2c7a971db1b62e89c3e9aa7f6a2803a9102516507fa705e2bfa4` |

"""

EDITS = [
    ('**Register version:** v0.14 OWNER-RATIFIED 29 October 2026, recording',
     '**Register version:** v0.15 RATIFICATION CANDIDATE (drafted 30 October 2026), recording the document-round installation, the E_6 review and owner decisions, and the E_6 package; v0.14 OWNER-RATIFIED 29 October 2026, recording'),
    ('This register, H-1 v1r4 and H-2 v1r5 are installed together by the document-only procedure.',
     'This register, H-1 v1r4 and H-2 v1r5 are installed together by the document-only procedure. For v0.15, the DOC-6 commit `337b5b2` and the clean-up commit `f9de54a` were verified by Claude from GitHub. The E_6 package and this register are installed together, in one commit identified after installation; the owner\'s Windows results for it are recorded after installation.'),
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
