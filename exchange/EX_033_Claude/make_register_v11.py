"""Draft register v0.11 from the installed register v0.10 by counted in-place edits (Claude, 28 Oct 2026; E2R-CODE-1).

Records: the E1-ALIGN installation and the owner's Windows acceptance; the candidate-ZIP departure and its
fix; the owner's waiver of E1A-CODE-RD-02; the owner-approved E_2-readiness code scope (S-1..S-3); and the
E2R-CODE-1 contract library, installed in the same commit as this register.
Every old string must occur exactly once; inserted text is ASCII. The input is the Git blob of
doc/RATIFICATION_REGISTER_v0_10.md (8ee8307e...75a4, UTF-8, LF). One placeholder, finalised after review and
the owner's ratification: "RATIFICATION CANDIDATE" (version line).
Usage: python3 -I make_register_v11.py REGISTER_v0_10 SCOPE_SHA256 NOTES_SHA256 OUT_v0_11
"""
import hashlib, sys

src, scope_sha, notes_sha, out = sys.argv[1:5]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '8ee8307e3c98eabbf24743391c7ebb821e6700f8efa8a093996f97d3d43475a4'
t = raw.decode('utf-8')
assert '\r' not in t

NEW_SECTION = f"""## E1-ALIGN accepted and the E_2-readiness contract library (register v0.11)

Paths in this section are under `doc/`, except those beginning `review/`, `exchange/`, `src/` or `tests/`, which are from the repository root. In this section, "this register" means register v0.11.

**E1-ALIGN installation verified and accepted.** The E1-ALIGN code and register v0.10 were installed at commit `295118d3aedb40d1113d234fced6bac77bf55f3a` (28 October 2026; parent `72ef196`).
- **The owner's Windows run** (Windows 11, Python 3.15.2; owner-reported):
  - PRE PASS; the 5 moves; 21 files copied; POST PASS (the 10 edited files equal predecessor plus the reviewed allowlist);
  - all 84 tests passed, with only the 2 allowed symlink skips;
  - all 37 location, origin and mutation checks passed;
  - COMMITTED PASS before the push. A first commit command was mistyped, so the committed check ran before any commit and stopped; nothing had been committed or pushed, and the owner then committed and re-ran it.
- **Claude verified the commit from GitHub:** exactly 5 deletions, 5 moved-path additions, 11 other additions and 6 modifications, every blob equal to the committed manifest, and the 84 tests pass on Linux. **E1A-T13:** in a disposable clone, since deleted, `git revert` gave `src/` and `tests/` identical to `72ef196`, and the 79 pre-E1-ALIGN tests passed. This is not a later rollback guarantee.
- **E1A-D1 holds:** with that evidence the E1A-R02 conditions are met, and **E_1 remains revision 1** under its scoped structural exception.
- **The reviewer's reviews** are installed with this register as LF copies: `review/Independent_ChatGPT_E1ALIGN_Code_RECHECK_v0_1.md` and `review/Independent_ChatGPT_Register_v0_10_Review_v0_1.md` (EX_028).

**Departure, recorded and fixed.** The owner installed the reviewed candidate ZIP (`c613cc1a...b00c`), not the final ZIP (`87a8fdcb...2283`). Their code, tests, allowlist and evidence are byte-identical; they differ only in register v0.10's version line, its manifest line and the verifier constants. So `295118d` carried the candidate register ("RATIFICATION CANDIDATE") and its manifest. The owner fixed both by the document-only procedure: `c1159c7` (the register, `8ee8307e...75a4`) and `1b23fd9` (the manifest, `66109201...dddd`). The second commit was needed because the packaging used fixed ZIP member times: the two manifests have the same size, so Git did not see the replacement until it was re-added. Claude's packaging now uses real times. The tree at `1b23fd9` holds all 21 files byte-identical to the final package.

**E1A-CODE-RD-02 waived (OWNER-DECIDED 28 October 2026).** The reviewer required a mechanical check of the final ZIP before installation. The owner waived it on Claude's advice: the install's POST phase rebuilds every edited code file from its base blob using only the reviewed allowlist, whose hash the verifier pins, so a wrong code byte would have stopped the install. The reviewer received the narrow diff afterwards (EX_029).

**E_2-readiness code scope (OWNER-APPROVED 28 October 2026).** `Predictive_Randomness_E2R_Code_Scope_v0_1.md` (`{scope_sha}`) is the owner scoping that E2R-1 section 13A requires, installed with this register. The owner approved:
- **S-1:** three packages. CODE-1 is the contract library, new files only and wired into nothing. CODE-2 wires it into the launchers and coordinator, with its own design note first, and any change to a protected coordinator function is an owner decision first. CODE-3 is retirement tooling (E2R-T15).
- **S-2:** E_1's synthetic `METHOD_FORECAST_V1` adapter for E2R-T09 lives in the tests, not in `src/methods/E_001/`.
- **S-3:** the reviewer was asked to start an independent R-4 T-05 oracle in parallel (EX_031).
- **The reviewer's design-stage view** (EX_032; `review/Independent_ChatGPT_E2R_Code_Scope_Review_v0_1.md`, LF copy): it supports S-1..S-3, with 0 BLOCKER, 4 CORRECTION and 1 OPTIONAL. E2RC-C01..C03 and O01 are implemented in CODE-1; C04 (E_1 revision discipline when it is wired in) binds CODE-2's design note.
- **The R-4 oracle** (`review/Independent_E2R_T05_Oracle_v0_1.py` and its plan, LF copies) agreed with CODE-1 on all 192 synthetic cases when Claude ran it on Linux. That is evidence, not authorisation.

**E2R-CODE-1, the contract library (installed with this register).**
- **What it adds** (new files only):
  - six shared modules under `src/methods/_common/`: `contract_vocab.py`, `contract_records.py`, `contract_task.py`, `contract_forecast.py`, `contract_receipts.py` and `contract_registry.py`;
  - the installed contract data under `src/methods/_common/contract_data/`: E_1's `METHOD_DECLARATION_V1` for both games, its `SUPPORTED` registry entries, and `FORMULA_OPEN` entries (variant `NOT_YET_SPECIFIED`) for E_2..E_62 in both games, with the texts for E_1 and E_2 written in plain English (owner decision D-3);
  - the tests `tests/test_e2r_contract.py`, `tests/test_e2r_prefix.py` and their fixtures `tests/e2r_fixtures.py`: E2R-T01 to T13, T16 at record level, T17 and T18.
- **What it does not change:** every existing file, including the reader, the coordinator and its 11 protected functions, `coordinator_private`, both launchers, the wrappers, E_1's code, Package 2's modules and `multigame_method_registry.py`. The three switches stay False and the allowlist stays empty. No gate is activated. E_1 keeps revision 1 with no exception needed, because no E_1 code changes.
- **Nothing is wired in:** no launcher dispatches through the contract yet. The dispatch gate (E2R-T14), run-level receipts and terminal records, `mg-` run IDs and E_1 producing `METHOD_FORECAST_V1` at run time are CODE-2's.
- **Implementation choices made within E2R-1** are listed in `review/E2R_CODE1_Implementation_Notes_v0_1.md` (`{notes_sha}`), for the reviewer's RECHECK.
- **Review:** CODE-1 gets the reviewer's independent HIGH-tier RECHECK, with R-2 reproduction and the R-4 T-05 oracle, and the owner's Windows run before the commit. Its results are recorded after installation; this register does not predeclare them.

**Out-of-date statements (register v0.11).** This register prevails, and the files are not edited:
- Register v0.10, its forward wording "installed with this register" for E1-ALIGN: done, at `295118d`, as above.
- E2R-1 section 13's test list: T14 joins with CODE-2 and T15 with CODE-3, as its own note says; T16 is tested at record level now and at run level in CODE-2.
- Package 2's `multigame_method_registry.py` stays the live dispatch roster until CODE-2 replaces its use; the installed registry entries are the contract's record of status from now on.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `Predictive_Randomness_E2R_Code_Scope_v0_1.md` | Claude; design-stage view by the ChatGPT reviewer chat | OWNER-APPROVED 28 Oct 2026; `{scope_sha}` |
| `RATIFICATION_REGISTER_v0_10.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; installed at `295118d`, finalised at `c1159c7`; superseded by this register; `8ee8307e3c98eabbf24743391c7ebb821e6700f8efa8a093996f97d3d43475a4` |

"""

EDITS = [
    ('**Register version:** v0.10 OWNER-RATIFIED 28 October 2026, recording',
     '**Register version:** v0.11 RATIFICATION CANDIDATE (drafted 28 October 2026), recording the E1-ALIGN acceptance, the owner-approved E_2-readiness code scope and the E2R-CODE-1 contract library; v0.10 OWNER-RATIFIED 28 October 2026, recording'),
    ("the owner's Windows results for it are recorded after installation.",
     "the owner's Windows results for it are recorded after installation. For v0.11, the E1-ALIGN commit `295118d` and the follow-up commits `c1159c7` and `1b23fd9` were verified by Claude from GitHub; the Windows results are owner-reported. The CODE-1 contract library and this register are installed together, in one commit identified after installation."),
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
