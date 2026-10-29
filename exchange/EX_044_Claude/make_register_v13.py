"""Draft register v0.13 from the installed register v0.12 by counted in-place edits (Claude, 29 Oct 2026).

Records: the E2R-CODE-2 design and code reviews (EX_038..EX_043), the owner decisions D2-1..D2-4 and the
install-procedure decisions of 29 October 2026, and E2R-CODE-2 itself, installed with this register.
Every old string must occur exactly once; inserted text is ASCII. The input is the Git blob of
doc/RATIFICATION_REGISTER_v0_12.md (6f6f4556...4eb, UTF-8, LF). One placeholder, finalised after review and
the owner's ratification: "RATIFICATION CANDIDATE" (version line).
Usage: python3 -I make_register_v13.py REGISTER_v0_12 OUT_v0_13
"""
import hashlib, sys

src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '6f6f4556522b54ae4416da07357b50bed82ec799e7761f758cac99b6324ac4eb'
t = raw.decode('utf-8')
assert '\r' not in t

NEW_SECTION = """## E2R-CODE-2: the dispatch gate and the standalone contract runner (register v0.13)

Paths in this section are under `doc/`, except those beginning `review/`, `exchange/`, `src/` or `tests/`, which are from the repository root. In this section, "this register" means register v0.13.

**Register v0.12 installed.** The owner installed it by the document-only procedure at commit `b846519bce7463cc7a7a57095d438b9223dd8bb9` (29 October 2026), with the EX_036 review copy. Claude verified from GitHub that the commit adds exactly those 2 files: the register is `6f6f4556...4eb` and the review copy is `a99c8539...e2a3`. Only the register's version line changed from the reviewed candidate (`e1ac8b55...567c`).

**The design note.** `Predictive_Randomness_E2R_CODE2_Design_v0_1r1.md` (`f0c36fd3dabb83dcc5f21d8b92bd9b5c3eaf9647da069a4e5bff63514a26f2dd`) is installed with this register. It meets E2R-CODE-1 scope S-1's requirement of a design note before CODE-2.
- **v0.1** (EX_038, `d15a42af...b161`) was REVISIONS REQUIRED. The reviewer's review (EX_039; `review/Independent_ChatGPT_E2R_CODE2_R3_Design_and_Register_v12_Review_v0_1.md`, LF copy, `eedd59e4eb0dcde7e0876fa2ae47b01ec0b45d75927a602b7d967e1a1f02f18a`) found 2 BLOCKER, 3 CORRECTION and 1 OPTIONAL:
  - E2RC2-B01: E_1's legacy runner was outside the release rule;
  - E2RC2-B02: consumption trusted a caller-supplied "gates passed" flag;
  - C01: publication relied on a rename, not a proven create-only step;
  - C02: a legitimate no-ticket, no-diagnostic result had to be told apart from invalid output;
  - C03: the per-method roster is not a variant admission authority;
  - O01: the command line cannot request a diagnostic-only run, which is to be labelled a launcher limit.
- **v0.1r1** (EX_040) resolved all six. The reviewer passed it unchanged (EX_041, E2RC2-RD-06).

**The code.**
- **v1** (EX_038, `a5e8ac89...4a49`) was never run by the reviewer, because the design did not pass unchanged (RD-03).
- **v2** (EX_040, `cea050a0...7e00`) was REVISIONS REQUIRED. The reviewer's HIGH-tier review (EX_041; `review/Independent_ChatGPT_E2R_CODE2_v2_HIGH_RECHECK_v0_1.md`, LF copy, `110564fbeed2b01807649be96c55bcb95a8a36c3b4d3232f9c1068b4b3126d26`) found 2 BLOCKER, both RECHECK:
  - E2RC2-CODE-B01: the public run, dispatch, consumption and coordinator-gate functions accepted a caller-chosen orphan marker, registry folder and method folder;
  - E2RC2-CODE-B02: the standalone runner could publish a SUCCESS record labelled COORDINATED.
- **v3** (EX_042, `0f4b6600d3a239a0de124ce8365c382450eb6df24a07750457a58505f3ebd69f`) removed every such parameter and fixed the run's data source. `review/E2R_CODE2_EX041_Corrections_v0_1.md` (`55eb9a4e1b4ec108f4b203e60bf93c53fcc909423b598457a2d141426f8441ef`) records the changes. The reviewer's focused RECHECK (EX_043; `review/Independent_ChatGPT_E2R_CODE2_v3_Focused_RECHECK_v0_1.md`, LF copy, `da67250611475fdf3e1941a5a2f8d26546a6cd169690a84636243e352328ee01`) passed with 0 findings.
- **Independent reproduction:** the reviewer's R-2 run passed 179 of 179 selected offline tests, with no skips. The 10 tests that need the real masters and E2R-T12 were not run there; they are reserved for the owner's run (RD-14).
- **Claude's evidence** (author evidence): 190 tests on Linux, Python 3.13.17 and 3.15.0b4; 22 of 22 planted defects caught; install run-throughs in disposable clones.

**REVIEWER-DECIDED, checked by Claude, no exception to report:**
- E2RC2-RD-01: register v0.12's content passed;
- RD-02: the HIGH tier is kept, with a RECHECK of the five required design corrections;
- RD-03: no code review until the design passes unchanged;
- RD-04: D2-1, D2-2 and D2-4 supported, D2-4 with the variant-exact safeguard; D2-3 for the owner;
- RD-05: the E_1 wrapper plan is kept, with no undocumented registry or legacy-gate exception;
- RD-06: design v0.1r1 passed unchanged;
- RD-07: E_1 stays revision 1 for the new legacy gate, because the only change to E_1's files is the gate insertion, and E_1's calculation and goldens are unchanged;
- RD-08: the condition for the code review was met;
- RD-09 and RD-10: CODE-B01 and CODE-B02 assigned, BLOCKER and RECHECK;
- RD-11: v2 not recommended for installation;
- RD-12 and RD-13: CODE-B01 and CODE-B02 closed, PASS;
- RD-14: the bounded 179-test reproduction is accepted, and is not a 190-test acceptance;
- RD-15: v3 recommended for the owner's acceptance, with every owner gate kept.

**Owner decisions (29 October 2026).**
- **D2-3, OWNER-DECIDED** (before v0.1r1): E_1's legacy standalone runner gets the release check, not an exception.
- **D2-1, OWNER-RATIFIED:** CODE-2 covers the standalone path. The coordinator side gets only an entry point that runs the release check and then refuses every contract request. Coordinated contract runs need a later package.
- **D2-2, OWNER-RATIFIED:** a fourth switch, `ENABLE_CONTRACT_REAL_DEVELOPMENT`, stays `False`. Turning it on needs a separate owner approval.
- **D2-4, OWNER-RATIFIED:** Package 2's roster is read from the installed registry, as a roll-up only. Admission is the dispatch gate's alone.
- **OWNER-APPROVED:** E2R-T12 (up to six ordinary Python worker processes that finish normally) for CODE-2's rehearsal and install run.
- **OWNER-DECIDED:**
  - Claude Code rehearses the final package in a disposable task clone before the install;
  - no reviewer check of the final ZIP before installation, as for CODE-1. Claude sends the reviewer the narrow diff afterwards.
- **OWNER-DECIDED (process):** the reviewer's ZIPs are given to Claude, which records them in `exchange/`. The owner does not save them into the repository working tree.

**E2R-CODE-2 (installed with this register).**
- **What it adds** (new files):
  - `src/methods/_common/contract_dispatch.py`: the one dispatch gate (E2R-R57, T14). It admits a request only if:
    - the installed registry's active entry for the exact game, method and variant is SUPPORTED;
    - the request pins exactly that entry and its declaration;
    - the revision matches;
    - there is no `IN_DEVELOPMENT.txt`.

    It loads the installed registry afresh on every call. A refusal reads no data and creates nothing;
  - `contract_publication.py`: create-only publication (no file is ever overwritten), the run-level receipts and terminal record, and `read_run`. `read_run` decides whether a run may be consumed from the fixed orphan marker and the installed registry only, and for standalone runs only;
  - `contract_runner.py`: the standalone contract runner, with `mg-` run IDs and the switch `ENABLE_CONTRACT_REAL_DEVELOPMENT = False`;
  - `src/methods/Method_Contract_Runner.py`: its command line, launched by the existing `Run_Experiment.bat`;
  - `src/methods/contract_adapters/`: E_1's wrapper (E2RC-C04 option (a)), outside E_1's folder, which must match E_1's own result exactly;
  - `src/coordinator_private/contract_coordinated_gate.py`: the refusing coordinator-side entry point (D2-1);
  - the tests `tests/test_e2r_dispatch.py`, `tests/test_e2r_runner.py` and their fixtures `tests/e2r_code2_fixtures.py`: E2R-T14, and T16 at run level.
- **What it replaces** (3 files):
  - `multigame_method_registry.py`: the roster as a roll-up (D2-4);
  - `multigame_standalone_contract.py`: a synthetic run needs a released variant;
  - `E_001_Historical_Appearance_Frequency.py`: the legacy gate (D2-3), eight lines after its orphan-marker check.
- **What it does not change:**
  - the coordinator file, its 11 protected functions and `coordinator_main`;
  - the reader;
  - the launchers;
  - E_1's code under `src/methods/E_001/`;
  - CODE-1's modules and contract data.

  The three existing switches stay False, and the allowlist stays empty. E_1 keeps revision 1 (RD-07). There are no coordinated contract runs, no real-data contract runs and no FINAL, IS, scoring or retirement.
- **Review and acceptance:** the owner's Windows run, with all 190 tests including T12, comes before the commit. Claude verifies the commit from GitHub. The results are recorded after installation; this register does not predeclare them.

**Out-of-date statements (register v0.13).** This register prevails, and the files are not edited:
- Register v0.11, S-1, "CODE-2 wires it into the launchers and coordinator": by D2-1, CODE-2 wires the standalone path and E_1's legacy runner. The coordinator side gets only the refusing entry point.
- Register v0.11, "Package 2's `multigame_method_registry.py` stays the live dispatch roster until CODE-2 replaces its use": with CODE-2 the roster is a roll-up of the installed registry (D2-4).
- Register v0.11, T14 "joins with CODE-2" and T16 "at run level in CODE-2": both are in CODE-2's tests.
- Register v0.12, "Nothing calls the library yet": the standalone contract runner, E_1's legacy runner and the coordinator-side entry point call it once CODE-2 is installed. The EX_036 watchpoint is met: the gate loads the installed registry afresh.
- Design note v0.1r1, section 8: it gives 185 tests (47 for CODE-2, 29 in `test_e2r_runner.py`) and 18 planted defects. v3 has 190 tests (52 for CODE-2, 34 in `test_e2r_runner.py`) and 22 defects. The corrections note lists the additions.
- Design note v0.1r1, section 10, "awaiting the owner" for D2-1, D2-2 and D2-4: decided, as above.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `Predictive_Randomness_E2R_CODE2_Design_v0_1r1.md` | Claude; reviewed by the ChatGPT reviewer chat | Design PASS (E2RC2-RD-06); owner decisions D2-1 to D2-4 as above; installed with this register; `f0c36fd3dabb83dcc5f21d8b92bd9b5c3eaf9647da069a4e5bff63514a26f2dd` |
| `RATIFICATION_REGISTER_v0_12.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 29 Oct 2026; installed at `b846519`; superseded by this register; `6f6f4556522b54ae4416da07357b50bed82ec799e7761f758cac99b6324ac4eb` |

"""

EDITS = [
    ('**Register version:** v0.12 OWNER-RATIFIED 29 October 2026, recording',
     '**Register version:** v0.13 RATIFICATION CANDIDATE (drafted 29 October 2026), recording the E2R-CODE-2 reviews, the owner decisions D2-1 to D2-4 and the E2R-CODE-2 installation; v0.12 OWNER-RATIFIED 29 October 2026, recording'),
    ('This register is installed by the document-only procedure.',
     'This register is installed by the document-only procedure. For v0.13, the register v0.12 commit `b846519` and the exchange records `5957569` to `8d1f080` were verified by Claude from GitHub. The E2R-CODE-2 code and this register are installed together, in one commit identified after installation; the owner\'s Windows results for it are recorded after installation.'),
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
