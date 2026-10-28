"""Draft register v0.10 from the installed register v0.9 by counted in-place edits (Claude, 28 Oct 2026; E1-ALIGN).

Records: the DOC-3 and DOC-4 installations; H-2 v1r4; exchange/README.md v0.4; the owner's rule for
document-only installs; the E1-ALIGN code installation (in the same commit as this register).
Every old string must occur exactly once; inserted text is ASCII. The input is the Git blob of
doc/RATIFICATION_REGISTER_v0_9.md (e84a7a20...c6c8, UTF-8, LF). Placeholder finalised after review and
the owner's ratification: "RATIFICATION CANDIDATE" (version line) only.
Usage: python3 -I make_register_v10.py REGISTER_v0_9 OUT_v0_10
"""
import hashlib, sys

src, out = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == 'e84a7a208d99775bbbbf15af8a177d956c5a8e4819cf5b35537f6b70f5dfc6c8'
t = raw.decode('utf-8')
assert '\r' not in t

NEW_SECTION = """## E1-ALIGN installed, H-2 v1r4 and document installs (register v0.10)

Paths in this section are under `doc/`, except those beginning `review/`, `exchange/`, `src/` or `tests/`, which are from the repository root. In this section, "this register" means register v0.10.

**DOC-3 installation verified.** H-1 v1r3 and register v0.9 were installed at commit `ee62eb6d1c9c968f04ee1c6b26d7c9536dac0f3f` (28 October 2026; parent `ac9d120`), in one commit with the DOC-3 review records.
- **The owner's Windows run (owner-reported):** PRE PASS, 6 files copied, POST PASS, COMMITTED PASS before the push. An earlier attempt stopped before PRE on seven downloads saved under `review/`; they were moved out, and nothing was committed from that attempt.
- **Claude verified the commit from a fresh GitHub clone:** the committed-phase verifier passes, the commit adds exactly 6 files, and every blob equals `review/DOC3_Install_v1/INSTALL_MANIFEST_SHA256.txt`.

**H-2 v1r4 (OWNER-RATIFIED 28 October 2026; installed).** `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r4.md` (`73b90ea348aea5fc337097a14ec4a8669258bc6cba55ce5a2485de26575f3f3a`, UTF-8) was installed at commit `040f80e6e5ab90637da83ef971796ea59783e921` (DOC-4), with its review history.
- **Its one factual review** was Claude's (`review/Claude_Fact_Check_H2_v1r4_v1.md`): three documentary corrections, H2F-01..03, which the reviewer adopted (H2-RD-01..03).
- **Its reviewer-rights region** (R-1..R-11, T-05 and section 3.1; 7,676 bytes) is byte-identical to H-2 v1r3. Both chats checked this mechanically.
- **Its status lines are historical** ("PENDING PROJECT-OWNER RATIFICATION/INSTALLATION"); this register determines its status.
- **Supersession:** it replaces H-2 v1r3 for future reviewer roles; v1r3 is kept as history.
- **Verification:** Claude checked DOC-4 from GitHub: 8 added files, every blob equal to `review/DOC4_Install_v1/INSTALL_MANIFEST_SHA256.txt`. The owner's decisions record installed with it, `review/Owner_Decisions_H2_v1r4_and_Exchange_v0_4_28Oct2026.md`, is superseded by this register as the formal record.

**exchange/README.md v0.4 (OWNER-DECIDED 28 October 2026).** EX message files stay US-ASCII with CRLF. An enclosed document that is, or derives from, a UTF-8 project file keeps its characters, in LF or CRLF, and its identity is the SHA-256 of its canonical LF bytes. Committed by Claude inside `exchange/` only, at `63c19e7515e02acc10af1a9c7a290acc73371b7e`.

**Document-only installs (OWNER-DECIDED 28 October 2026).** The owner judged the install machinery for documents to be excessive overhead for little value, and directs effort to design safety, coding and testing.
- **Scope:** files only under `doc/` and `review/`: handovers, registers, specifications and review records. Not `src/`, `tests/`, a launch or owner `.bat` wrapper, data or `transitory_data/`.
- **Delivery:** one zip whose folders mirror the repository, and one short command block: extract; `git pull --ff-only`; copy; `git add doc review`; `git status --short`, which must list only the expected new files; commit; push.
- **The check:** after the push, Claude checks once from GitHub that the files and blobs are as expected. A mistake is fixed with a follow-up commit. There is no verifier script, no PRE/POST/COMMITTED, and no reviewer check of the install zip.
- **What is unchanged:** content review (one factual review of each handover; review of each register edition and specification) and the reviewer's rights.
- **Code packages keep the full discipline:** anything touching `src/`, `tests/`, wrappers or an always-review topic gets an exact allowlist, a read-only verifier, PRE, POST and COMMITTED before the push, an independent RECHECK and the owner's Windows tests. DOC-4 was the first install made this way.

**E1-ALIGN code (owner-authorised 28 October 2026; installed with this register).** The owner authorised the E1-ALIGN code package on 28 October 2026. The code is installed in the same commit as this register, under the ratified design `Predictive_Randomness_E1_ALIGN_Specification_v0_2r1.md` (`d9ffd900c74d8a0cc5002bb78c83121f818514cd88ca9150bada8d6d1fa6653a`) and its decisions E1A-D1..D3 (register v0.8).
- **What it changes:**
  - five E_1-only modules move from `src/methods/_common/` to `src/methods/E_001/`;
  - `canonical_bytes` and the tuple helper (now `length32_tuple`) move, bodies byte-for-byte unchanged, into `src/methods/_common/canonical_encoding.py`;
  - the shared reader imports its encoder from there, so it no longer depends on E_1;
  - the static import firewall is widened to method folders and made symbol-aware, with E_1's three exact, counted allowances (this closes the gap recorded in register v0.8);
  - `tests/test_e1_align.py` adds five guards.
- **The exact change set:** 5 moves, 10 edited files with 22 edit blocks, 1 file moved unchanged and 3 added files. Every edited file equals its predecessor plus the reviewed frozen allowlist, `review/E1ALIGN_Code_Install_v1/e1align_allowlist.json` (`aaf7f46e529ff42036cf7f943c4efc6232edbd2c3ff463e9e1be02f10a975164`), which the install verifier checks.
- **What it does not change:** no schema, record identity, golden, scientific constant or output byte; no E_1 behaviour. The protected coordinator, `coordinator_private`, the launch wrappers and the owner tools are not edited. The three switches stay False and the allowlist stays empty. E_1's real-mode gate and the orphan-marker checks are unchanged, and no gate is activated.
- **E1A-D1, E_1 revision 1:** E_1 stays revision 1 under its scoped structural exception only if the E1A-R02 conditions hold at installation. Those conditions are: the exact change set above; the moved definitions byte-identical; every E_1-facing symbol resolving to the same object; and the full proof, including the owner's Windows run. That run is the 84 tests by module (`RUN_E1ALIGN_SUITE.py`) and the location, origin and mutation checks (`CHECK_E1ALIGN_IMPORTS.py`), on the project interpreter, now Python 3.15.2 (register v0.9; this supersedes E1A-T12's "Python 3.14" on the version only). Its results are recorded after the install; this register does not predeclare them.
- **Evidence before installation (Claude, Linux; not Windows acceptance):** on Python 3.13.17, and on a 3.15.0b4 interpreter with numpy 2.5.4, scipy 1.18.1 and psutil 7.2.2, all 84 tests pass (79 before E1-ALIGN), with no skips. The exact allowlist check, the moved bodies, and the controls and mutations of the design pass. The allowlist regenerated from the installed NAMES-1 tree is byte-identical to the reviewed one.
- **Review:** the code package gets the reviewer's independent RECHECK (HIGH tier) before installation.

**The phone exchange records.** `exchange/EX_015` onward record the DOC-3, H-2 v1r4, DOC-4 and E1-ALIGN exchanges, from 28 October 2026. They are committed by Claude inside `exchange/` only, and are evidence, not authority.

**Out-of-date statements (register v0.10).** This register prevails, and the files are not edited:
- H-1 v1r3 section 1 and H-2 v1r4 section 8.2 ("Delivery practice"): document-only installs are now as above.
- H-1 v1r3's module map (section 7.1), Architecture v0.8's "one standalone `.py` per method", and the file paths of E_1's modules in R2, R3 and the TH-1 records: E_1's modules are now in `src/methods/E_001/`, its entry file is unchanged, and the encodings are in `_common/canonical_encoding.py`.
- H-1 v1r3, H-2 v1r4 and register v0.8, on the firewall's known `from _common import game_draws_reader` gap: closed by E1-ALIGN.
- Register v0.9, its exchange-records range ("`EX_001` to `EX_014`"): extended above.
- H-2 v1r3, generally: superseded by H-2 v1r4.

The next editions fold these in.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r4.md` | the ChatGPT reviewer chat; factual review by Claude | OWNER-RATIFIED 28 Oct 2026; installed at `040f80e`; `73b90ea348aea5fc337097a14ec4a8669258bc6cba55ce5a2485de26575f3f3a` |
| `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r3.md` | the ChatGPT reviewer chat; factual review by Claude | OWNER-RATIFIED; superseded by H-2 v1r4; `a2fb5c641a6fa8010aa59ff811aeba23145703bd5c0d4e2dbd70ac2fb419edb1` |
| `Predictive_Randomness_E1_ALIGN_Specification_v0_2r1.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; code installed with this register; `d9ffd900c74d8a0cc5002bb78c83121f818514cd88ca9150bada8d6d1fa6653a` |
| `RATIFICATION_REGISTER_v0_9.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; installed at `ee62eb6`; superseded by this register; `e84a7a208d99775bbbbf15af8a177d956c5a8e4819cf5b35537f6b70f5dfc6c8` |

"""

EDITS = [
    ('**Register version:** v0.9 OWNER-RATIFIED 28 October 2026, recording',
     '**Register version:** v0.10 RATIFICATION CANDIDATE (drafted 28 October 2026), recording the E1-ALIGN code installation, H-2 v1r4, exchange README v0.4 and the owner\'s rule for document-only installs; v0.9 OWNER-RATIFIED 28 October 2026, recording'),
    ('the actual install commit and final blobs are verified separately after installation.',
     'the actual install commit and final blobs are verified separately after installation. For v0.10, the DOC-3 commit `ee62eb6` and the DOC-4 commit `040f80e` were verified by Claude from GitHub; the Windows results are owner-reported. The E1-ALIGN code and this register are installed together, in one commit identified after installation; the owner\'s Windows results for it are recorded after installation.'),
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
