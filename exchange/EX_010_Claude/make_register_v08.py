"""Draft register v0.8 from the installed register v0.7 by counted in-place edits (Claude, 28 Oct 2026).

Records: the DOC-2 installation; the NAMES-1 v0.2 ratification and the owner's OPEN-N1..N3 decisions;
the NAMES-1 installation (in the same commit as this register); the owner decisions made after
register v0.7 (oversight extended indefinitely; the exchange protocol; the E1-ALIGN v0.2r1 ratification
and decisions E1A-D1..D3);
a known gap in the committed static firewall test; and the out-of-date statements.
Every old string must occur exactly once; inserted text is ASCII. The input is the final register v0.7
(f9be980c...c015, UTF-8, LF). The DOC-2 commit ID
(908db9ea9d4a37b17833f5d43919804c78ef7e14) is filled in; the one remaining placeholder, "RATIFICATION
CANDIDATE", is finalised after review and the owner's ratification.
Usage: python3 -I make_register_v08.py REGISTER_v0_7 OUT_v0_8
"""
import hashlib, sys

src, out = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == 'f9be980c2482c22cb2da6f7af34020f8cfd8e32302694c975c955ec407fcc015'
t = raw.decode('utf-8')
assert '\r' not in t

SPEC = 'Predictive_Randomness_NAMES1_Rename_Specification_v0_2.md'

NEW_SECTION = f"""## NAMES-1 and owner decisions after register v0.7 (register v0.8)

Paths in this section are under `doc/`, except those beginning `review/` or `exchange/`, which are from the repository root. In this section, "this register" means register v0.8.

**DOC-2 installation.** The E2R-1 specification v0.3r3 and register v0.7 were installed at commit `908db9ea9d4a37b17833f5d43919804c78ef7e14` (28 October 2026).
- **It arrived in two commits.** The owner had already committed four of the package's eight files, byte-identical to the package, in commit `2c766644215a315edd8b92130e691224b60cd3de` (merged as `f300f2dfcd5c6a5efccb4c8b1040368728e2ad69`). They were the two DOC-2 review packages and the two DOC-2 reviews. `908db9ea9d4a37b17833f5d43919804c78ef7e14` added the other four.
- **The installer stopped on its one-commit rule only.** Its final check requires a single commit to add all eight files, and that is the rule that failed. Its blob check, which runs first, had passed for all eight files. The owner pushed after Claude confirmed that.
- **Claude verified the result from GitHub.** At `908db9ea9d4a37b17833f5d43919804c78ef7e14` all eight files match the package: the seven listed in `review/DOC2_Install_v1/INSTALL_MANIFEST_SHA256.txt`, and the manifest itself (`c3b373a3222d716963a1894ccc9d84f5737fa4af673d74b1fca18fdf1c39f8a0`). No file under `src/` or `tests/`, and no `.bat` file, has changed since `38fc60e`.
- **Commit `2c76664` also carried six NAMES-1 and E1-ALIGN history files**, byte-identical to those that NAMES-1 cites: the two NAMES-1 review packages and reviews, the owner-decisions record, and the E1-ALIGN early comments. Register v0.7's final bytes are `f9be980c2482c22cb2da6f7af34020f8cfd8e32302694c975c955ec407fcc015`. Its reviewed candidate r2 was `8b751a878e0626165b6c01bbc49d7d3014b3bd83a171200b4247eb5ec761796d`, and the mechanical finalisation diff is `review/DOC2_Register_v0_7_candidate_to_final.diff`.
- The DOC-2 reviews were:
  - `review/Independent_ChatGPT_Review_DOC2_Register_v0_7_v1.md` (2 CORRECTION, 1 OPTIONAL);
  - the PASS recheck `review/Independent_ChatGPT_Focused_Recheck_DOC2_Register_v0_7_r2.md` (`fc35b3ff7ad6892a066c7aca081f00c90cbc0847901ccebe3a2c202b376af13a`).

**NAMES-1, the one-off rename to stable file names.** `{SPEC}` (`07bda3e4a8a99bfc611a76cec672f8642532186567737e1a23de5e5701489e5a`) is OWNER-RATIFIED 28 October 2026. Its `OPEN` labels show its drafting state; the owner's decisions are below.
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
| `{SPEC}` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; `07bda3e4a8a99bfc611a76cec672f8642532186567737e1a23de5e5701489e5a` |
| `Predictive_Randomness_E1_ALIGN_Specification_v0_2r1.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026 (design only); `d9ffd900c74d8a0cc5002bb78c83121f818514cd88ca9150bada8d6d1fa6653a` |
| `RATIFICATION_REGISTER_v0_7.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; superseded by this register; `f9be980c2482c22cb2da6f7af34020f8cfd8e32302694c975c955ec407fcc015` |

"""

EDITS = [
    ('**Register version:** v0.7 OWNER-RATIFIED 28 October 2026, recording',
     '**Register version:** v0.8 RATIFICATION CANDIDATE (drafted 28 October 2026), recording the DOC-2 and NAMES-1 installations, the NAMES-1 ratification and the owner decisions made after register v0.7; v0.7 OWNER-RATIFIED 28 October 2026, recording'),
    ('its installation is a separate owner decision.',
     'its installation is a separate owner decision. The v0.8 entries were cross-checked by Claude against GitHub commit `908db9ea9d4a37b17833f5d43919804c78ef7e14` (28 October 2026); the NAMES-1 specification and code, and the E1-ALIGN specification, are installed with register v0.8, in one commit, and are identified by content hash.'),
    ('| OWNER-RATIFIED 28 Oct 2026; superseded by this register; `5e677dce',
     '| OWNER-RATIFIED 28 Oct 2026; superseded by register v0.7; `5e677dce'),
    ('\n## Interpretation and verification\n',
     '\n' + NEW_SECTION + '## Interpretation and verification\n'),
]
for old, new in EDITS:
    n = t.count(old)
    assert n == 1, (n, old[:80])
    assert all(ord(c) < 128 for c in new), old[:60]
    t = t.replace(old, new)
assert t.endswith('\n')
open(out, 'wb').write(t.encode('utf-8'))
print(out, hashlib.sha256(t.encode()).hexdigest(), len(t.splitlines()), 'lines')
