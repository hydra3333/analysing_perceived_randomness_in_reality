"""Draft register v0.9 from the installed register v0.8 by counted in-place edits (Claude, 28 Oct 2026; DOC-3).

Records: the NAMES-1 installation at 52ebeaa and Claude's verification; the owner's move to Python 3.15.2;
H-1 v1r3 (installed with this register); the exchange records so far; out-of-date statements.
Every old string must occur exactly once; inserted text is ASCII. The input is the Git blob of
doc/RATIFICATION_REGISTER_v0_8.md (3f217c68...ffcf, UTF-8, LF). Placeholders finalised after review and
the owner's ratification: "RATIFICATION CANDIDATE" (version line) and [H1-DATE] (H-1 v1r3's ratification).
Usage: python3 -I make_register_v09.py REGISTER_v0_8 H1_v1r3 OUT_v0_9
"""
import hashlib, sys

src, h1, out = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '3f217c6875d443a0cc1bba2f6c329b1fda455fb4a97bf7fe06090394736fffcf'
H1_SHA = hashlib.sha256(open(h1, 'rb').read()).hexdigest()
t = raw.decode('utf-8')
assert '\r' not in t
H1 = 'HANDOVER/Claude_Primary_Handover_H1_v1r3.md'

NEW_SECTION = f"""## NAMES-1 installed, Python 3.15 and H-1 v1r3 (register v0.9)

Paths in this section are under `doc/`, except those beginning `review/` or `exchange/`, which are from the repository root. In this section, "this register" means register v0.9.

**NAMES-1 installation verified.** NAMES-1 was installed at commit `52ebeaa385fd05b18c4f3805c3cd2000948e343d` (28 October 2026; parent `7f6b4e8`), in one commit with register v0.8, the NAMES-1 v0.2 and E1-ALIGN v0.2r1 specifications and the review history, as register v0.8 records.
- **The owner's Windows run** (Python 3.14.10; owner-reported) followed the reviewed instructions:
  - PRE PASS; 27 renames; 42 files copied; POST PASS;
  - all 79 current tests passed, with 2 skips, the reader-contracts symlink subtest and the exit-receipt symlink test;
  - 63 import-origin and firewall checks passed;
  - COMMITTED PASS before the push.
- **One earlier attempt stopped at PRE** on three downloaded files saved under `review/`. It was undone with `git reset --hard` and `git clean -fd -- doc review`, and restarted from PRE. Nothing from it was committed.
- **Claude verified the commit from GitHub:**
  - the committed-phase verifier passes;
  - without rename detection, the commit has 42 additions, 27 deletions and 3 modifications;
  - `review/NAMES1_Code_Install_v1/INSTALL_MANIFEST_SHA256.txt` is `9d8664f38c33ee374ace06d29d98a4d84477af9199359e22bfcef84e1897f6a7`;
  - no `.bat` file and no test fixture changed;
  - the 79 tests pass on Linux.
- **The immediate recovery check (N1-T10) passed.** In a disposable clone, `git revert` restored a tree identical to `7f6b4e8`, and the pre-NAMES-1 suite passed under the old names. The clone was deleted. This is not a later rollback guarantee.
- **The reviewer's checks of the package:** the NAMES-1 code review (`review/Independent_ChatGPT_NAMES1_Code_Review_v0_1.md`), its rechecks (EX_009, EX_011) and the mechanical check of the final ZIP (`exchange/EX_013_ChatGPT.md`, PASS). Claude's report is `exchange/EX_014_Claude.md`.

**Python 3.15.2 (OWNER-DECIDED, 28 October 2026).**
- **The new venv:** the project venv is now Python 3.15.2, built afresh with `py -3.15 -m venv .venv`. The owner's dependency updater installed every package from a ready-built wheel: numpy 2.5.4, scipy 1.18.1, psutil 7.2.2, threadpoolctl 3.7.0, requests 2.34.2, beautifulsoup4 4.15.0 and selenium 4.51.0. Against the 3.14.10 venv, only certifi (2026.10.19 to 2026.10.23) and soupsieve (3.0.3 to 3.0.4) changed.
- **Tests (owner-reported):** on Python 3.15.2 at `52ebeaa`, all 79 current tests passed on Windows, with the same 2 symlink skips, and the 63 import checks passed.
- **The fallback:** the previous 3.14.10 venv is kept as `venv.bak` (ignored by Git), with Python 3.14 installed. The free-threaded 3.14t build was removed.
- **Not yet run under 3.15:** the owner's data tools. Their first run is a first run.
- **What changed in the language:** Python 3.15 makes UTF-8 the default text encoding (PEP 686). The tests show no effect on the project.
- **Ratified text this decision supersedes, on the interpreter version only:**
  - Proposal v0.6 A-17 ("Python 3.14 is the intended implementation platform") and its platform line;
  - R2 v0.5 section 9.1 ("Standard CPython 3.14 on Windows 11, not a free-threaded or experimental interpreter"). The rest of that line stands: the interpreter is standard CPython, not free-threaded;
  - R2 v0.5 section 12.3 ("Preserve the user's working standard Python 3.14.8 project `.venv`" and "its Python 3.14/Windows support checked"). Read these as the current project interpreter, now 3.15.2; any new package's support for that interpreter is still checked and announced first;
  - R3 v0.5's environment line, and Architecture v0.8 section 20.1, which cites the 3.14 documentation (an informational reference).

  The files are not edited; the next editions fold this in.
- **What this is not:** no scientific run, mode or gate changes with it. Moving to a new Python is not a W-23 waiver; the always-review rule on dependency upgrades stands.
- **Limits of the evidence:** the 79-test Windows run and 63 import checks are the evidence reported for this interpreter change; they do not by themselves establish the full W-23 and related dependency-upgrade acceptance gates. This record claims no completed gate not evidenced here. The owner's interpreter choice does not authorise a scientific or data run, or relax future upgrade preflight, numerical, N-1, golden or independent-review duties.

**H-1 v1r3.** `{H1}` (`{H1_SHA}`) is a candidate pending owner ratification, to be installed with this register; its ratification is recorded as OWNER-RATIFIED [H1-DATE] when given, and its installation is verified after the install.
- It is a records refresh of H-1 v1r2. Its Appendix C lists every change.
- It replaces H-1 v1r2 for future roles; v1r2 is kept as history.
- It authorises nothing.

**The phone exchange records.** `exchange/EX_001` to `EX_014` record the messages between the two AI chats from 28 October 2026. They are committed by Claude inside `exchange/` only, up to commit `83d1515`. They are evidence, not authority. Where they matter, the review files are stored under `review/` as LF copies, as register v0.8 records.

**Out-of-date statements (register v0.9).** This register prevails, and the files are not edited:
- Register v0.8, its future-tense description of NAMES-1 being installed with it: now historical fact (above).
- H-1 v1r2, generally: superseded by H-1 v1r3.
- Python 3.14 as the project interpreter, in the ratified documents listed above and in H-1 v1r2 and H-2 v1r3: the venv is now 3.15.2 (above).
- H-2 v1r3: it does not cover the events of 28 October 2026. The reviewer chat may refresh it as its own handover; it gets one review.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `{H1}` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED [H1-DATE]; `{H1_SHA}` |
| `HANDOVER/Claude_Primary_Handover_H1_v1r2.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; superseded by H-1 v1r3; `55543ba522a4085fc4f2476d421a4940171bcd4c183a1fab5a691d291605eac0` |
| `RATIFICATION_REGISTER_v0_8.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; superseded by this register; `3f217c6875d443a0cc1bba2f6c329b1fda455fb4a97bf7fe06090394736fffcf` |

"""

EDITS = [
    ('**Register version:** v0.8 OWNER-RATIFIED 28 October 2026, recording',
     '**Register version:** v0.9 RATIFICATION CANDIDATE (drafted 28 October 2026), recording the NAMES-1 installation, the move to Python 3.15 and H-1 v1r3; v0.8 OWNER-RATIFIED 28 October 2026, recording'),
    ('the NAMES-1 specification and code, and the E1-ALIGN specification, are installed with register v0.8, in one commit, and are identified by content hash.',
     'the NAMES-1 specification and code, and the E1-ALIGN specification, are installed with register v0.8, in one commit, and are identified by content hash. For v0.9, historical predecessor references through commit `83d1515` (28 October 2026) were checked by Claude. The new Python 3.15.2 environment and the Windows results are owner-reported. H-1 v1r3 and register v0.9 are candidates pending owner ratification and DOC-3 installation, and are identified by content hash; the actual install commit and final blobs are verified separately after installation.'),
    ('| OWNER-RATIFIED 28 Oct 2026; superseded by this register; `f9be980c',
     '| OWNER-RATIFIED 28 Oct 2026; superseded by register v0.8; `f9be980c'),
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
