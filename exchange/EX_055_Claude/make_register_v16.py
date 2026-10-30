"""Draft register v0.16 from the installed register v0.15 by counted in-place edits (Claude, 30 Oct 2026).

Records: the E_6 package's rehearsal (TASK_T005) and installation, the reviewer's three-part review (EX_053),
the owner's decisions after it (v0.15 ratified, T12 for E_6, D34-1..D34-5), the owner-reminders file, and the
E_3/E_4 package, installed with this register. Every old string must occur exactly once; inserted text is
ASCII. The input is the Git blob of doc/RATIFICATION_REGISTER_v0_15.md (405cc2f9...ea2e).
Placeholders, finalised after review and the owner's ratification: "RATIFICATION CANDIDATE" (version line)
and [T12-E34] (the owner's T12 decision for this package's rehearsal and install).
Usage: python3 -I make_register_v16.py REGISTER_v0_15 OUT_v0_16
"""
import hashlib, sys

src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '405cc2f964db5a86cdf6a94bfc1382d01911ef9f41162b047c43c7f1af04ea2e'
t = raw.decode('utf-8')
assert '\r' not in t

NEW_SECTION = """## E_6 installed, and E_3 and E_4, the polynomial-fit pair (register v0.16)

Paths in this section are under `doc/`, except those beginning `review/`, `exchange/`, `src/`, `tests/` or `CLAUDE_CODE_WORKING_FOLDER_TREE/`, which are from the repository root. In this section, "this register" means register v0.16.

**The E_6 rehearsal (TASK_T005).** Before the install, Claude Code ran the final E_6 package (`exchange/EX_054_Claude/E6_Install_v2.zip`, `eea8e444...3e29`) in a disposable task clone on the owner's machine. The report (`CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T005.md`, commit `6e85b78`) gives:
- PASS in all 15 steps;
- all 210 tests, including E2R-T12, in 52 seconds, with the 3 allowed symlink skips;
- the main repository unchanged, and `scratch\\` empty again.

**Deviation, recorded.** At step 11, Claude Code redirected the status output to a temporary file outside the repository so that it could count the lines, and the file's deletion was declined. The file holds only that status output, and nothing in the repository was touched. Later task files will have the tool do any counting itself, so no redirection is needed.

**The E_6 package installed** at commit `7c93320c2cce853b94e23203bb47e3f66aaa7994` (30 October 2026; parent `6e85b78`, the T005 report).
- **The owner's log**, in order:
  - the ZIP's SHA-256 checked;
  - `git status --short` empty, and `Already up to date`;
  - `PRE PASS`;
  - 43 files copied;
  - `POST PASS`;
  - **before the commit**, `SUITE PASS`: all 210 tests, including E2R-T12, with only the 3 allowed symlink skips;
  - 40 `A` and 3 `M`;
  - `COMMITTED PASS`, then the push.
- **Claude's check, from a fresh GitHub clone:**
  - the parent and the 40 `A` + 3 `M` change set;
  - `COMMITTED PASS` repeated;
  - all 42 manifest entries match their Git blobs;
  - register v0.15 is the ratified `405cc2f9...ea2e`;
  - 210 tests pass on Linux.

E_6 is installed non-runnable, as D6-3 intends.

**The three-part review (EX_052 and EX_053).** The verdict is `review/Independent_ChatGPT_EX052_Three_Part_Review_v0_1.md`, LF copy, `8cb7519e72c01751d8a88e211517e65daf8ea63d88fef3fbafd35fc21a1b6491`, installed with this register. It found 0 BLOCKER, 0 CORRECTION and 0 RECONSIDER.
- **E_6 v2 against v1:** a narrow content and identity PASS. The candidate diff reproduced every changed file byte for byte, and no arithmetic changed.
- **Register v0.15:** CONTENT PASS. The exact predecessor was reconstructed, and the three counted edits reproduced the candidate byte for byte.
- **The E_3/E_4 design note v0.1:** R-3 design PASS unchanged, with 2 OPTIONAL items, both adopted as tests:
  - E34-O01: the exchange method in detail (ties for the largest error, a reference with zero levelled error, the sign pattern of the final reference, the cap);
  - E34-O02: for least squares and interpolation, the per-number polynomials of a barrel add up to the constant K, so their values at the target add up to K and their slopes to 0. This is not imposed on minimax, which is not linear.
- **REVIEWER-DECIDED, checked by Claude, no exception to report:**
  - E6-052-RD-01: accept the v2 terminology and identity change without reopening E_6's design;
  - REG15-052-RD-02: v0.15 content acceptable for ratification;
  - E34-052-RD-03: the E_3/E_4 code may be prepared to the frozen design; it still needs its own R-2 review.
- **EX_054** (Claude) recorded the owner's decisions below and the final E_6 package, for the record only.

**Owner decisions (30 October 2026).**
- **Register v0.15 OWNER-RATIFIED,** as reviewed.
- **E2R-T12 OWNER-APPROVED** for the E_6 package's rehearsal and install run.
- **D34-1..D34-5 OWNER-DECIDED** as designed:
  - D34-1: one shared helper, `_common/polynomial_fits.py`, versioned with both methods;
  - D34-2: six fixed variants per method, including the interpolation node positions 50, 40, 26, 11, 1;
  - D34-3: least squares on the raw 0/1 series; interpolation and minimax on the series smoothed by a centred mean of half-width 4, clipped to the window. The smoother is part of the hypothesis tested, not a claim about cause;
  - D34-4: scores only, with no probability vector;
  - D34-5: precise naming. The least-squares fit is ordinary polynomial least squares; "Chebyshev" names the interpolation nodes and the minimax criterion.

**The owner-reminders file.** `exchange/OWNER_REMINDERS.md` (added by Claude at `43c95c5`, 30 October 2026) lists things the owner asked to be reminded of, with the date asked and whether each is open or done. It is a working list, not reviewed and not part of the rules. Its items stay on file when completed or dropped.

**The E_3/E_4 package (installed with this register).**
- **What it adds:**
  - the shared helper `src/methods/_common/polynomial_fits.py`, revision 1: exact rational least squares, interpolation and minimax, each with a second, differently written algorithm or certificate for verify();
  - `src/methods/E_003/` and `src/methods/E_004/`, each with `variants.py`, `contract.py` and `IN_DEVELOPMENT.txt`;
  - 24 declarations and 24 `FORMULA_OPEN` registry entries;
  - `tests/test_polynomial_fits.py` (19 tests) and `tests/test_e3_e4_polynomial.py` (13 tests);
  - the design note;
  - review evidence.
- **What it replaces:** `src/methods/Method_Contract_Runner.py`, with two imports and two `ADAPTERS` entries.
- **What it does not change:** the contract libraries, the reader, the coordinator and its 11 protected functions, E_1, E_6, the template, the launchers and wrappers, the owner tools, and E_3's and E_4's `NOT_YET_SPECIFIED` placeholders. The four switches stay False, and the allowlist stays empty.
- **E_3 and E_4 cannot run** once this is installed: every request is refused with `NOT_SUPPORTED` before any data is read, and both flags are present.
- **Review and acceptance:**
  - the owner's Windows run of all 242 tests comes before the commit;
  - E2R-T12 for this package's rehearsal and install run: [T12-E34];
  - Claude verifies the commit from GitHub.

  The results are recorded after installation; this register does not predeclare them.

**Out-of-date statements (register v0.16).** This register prevails, and the files are not edited:
- Register v0.15, "installed with this register" for the E_6 package: done, at `7c93320`, as above.
- Register v0.15, the owner's plan, "one Chebyshev fitting helper": by D34-5, a polynomial-fit helper; "Chebyshev" applies to the interpolation nodes and the minimax criterion only.
- H-1 v1r4 section 7.4, "190 offline tests in 14 modules": 242 in 17 once the E_3/E_4 package is installed.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md` | Claude; reviewed by the ChatGPT reviewer chat | Design PASS unchanged (E34-052-RD-03); owner decisions D34-1..D34-5 as above; installed with this register; `b9d60b4c753bb90c6a7ca302fb4802c353b0ae23fbe82c2b417ae7b089fad072` |
| `RATIFICATION_REGISTER_v0_15.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 30 Oct 2026; installed at `7c93320`; superseded by this register; `405cc2f964db5a86cdf6a94bfc1382d01911ef9f41162b047c43c7f1af04ea2e` |

"""

EDITS = [
    ('**Register version:** v0.15 OWNER-RATIFIED 30 October 2026, recording',
     '**Register version:** v0.16 RATIFICATION CANDIDATE (drafted 30 October 2026), recording the E_6 installation, the three-part review and owner decisions, and the E_3/E_4 package; v0.15 OWNER-RATIFIED 30 October 2026, recording'),
    ("The E_6 package and this register are installed together, in one commit identified after installation; the owner's Windows results for it are recorded after installation.",
     "The E_6 package and this register are installed together, in one commit identified after installation; the owner's Windows results for it are recorded after installation. For v0.16, the E_6 installation commit `7c93320` was verified by Claude from GitHub. The E_3/E_4 package and this register are installed together, in one commit identified after installation; the owner's Windows results for it are recorded after installation."),
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
