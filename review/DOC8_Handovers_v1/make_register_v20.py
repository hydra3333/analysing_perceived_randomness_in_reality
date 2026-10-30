"""Draft register v0.20 from the installed register v0.19 by counted in-place edits (Claude, 30 Oct 2026).

Records: wave 2's code review (EX_074, EX_075), final package (EX_076), rehearsal (TASK_T008) and installation
(b61b1a2) with Claude's GitHub verification; the end of the previous reviewer chat; the owner's instructions for
the handover round; and the handover round itself (H-1 v1r6, H-2 v1r7 and their introductory blurbs), installed
with this register by the document-only procedure. Every old string must occur exactly once; inserted text is
ASCII. The input is the Git blob of doc/RATIFICATION_REGISTER_v0_19.md (b3ae51fd...e6a0). The four handover-round
files are read and hashed here, so the register always names their exact bytes.
Placeholder, finalised after the owner's ratification: "RATIFICATION CANDIDATE" (version line).
Usage: python3 -I make_register_v20.py REGISTER_v0_19 H1_v1r6 H1_BLURB H2_v1r7 H2_BLURB OUT_v0_20
"""
import hashlib, sys

src, h1, h1b, h2, h2b, out = sys.argv[1:7]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == 'b3ae51fd162960b64a9d145a52646dceeb3aec5b91e4b359ad7166e5e4c8e6a0'
t = raw.decode('utf-8')
assert '\r' not in t
H = {k: hashlib.sha256(open(p, 'rb').read()).hexdigest() for k, p in (('h1', h1), ('h1b', h1b), ('h2', h2), ('h2b', h2b))}

NEW_SECTION = f"""## Wave 2 installed, the reviewer chat's end, and the handovers (register v0.20)

Paths in this section are under `doc/`, except those beginning `review/`, `exchange/`, `src/`, `tests/` or `CLAUDE_CODE_WORKING_FOLDER_TREE/`, which are from the repository root. In this section, "this register" means register v0.20.

**Wave 2's code review (EX_074 to EX_076).**
- **EX_074** sent the wave 2 code candidate (`W2_Install_v1_candidate.zip`, `30219330cd73687b12d2442fb176712c59966f92f8da6977ae7ca50d020e0515`) with template draft 3 and register v0.19's candidate.
- **EX_075** gave R-2 PASS (0 BLOCKER, 0 CORRECTION, 0 OPTIONAL, 0 RECONSIDER), and CONTENT PASS for template draft 3 and register v0.19. The reviewer reproduced 288 selected tests independently, including all 31 new ones; the ten real-master reader tests and E2R-T12 were not run by the reviewer.
- **The review copy,** `review/Independent_ChatGPT_Wave2_R2_Template3_Register19_Review_v0_1.md` (LF, `1d4cf3551b2311d8968f4f4ddc182ef11f8651ff2a49d246c57af946b86dff47`), is installed with this register.
- **REVIEWER-DECIDED, checked by Claude, no exception to report:** W2-075-RD-01..04.
- **The owner** ratified register v0.19 and approved E2R-T12 for wave 2's rehearsal and install run (30 October 2026).
- **EX_076** recorded the final package, `W2_Install_v1.zip` (`57ef34b67b8aa6cc023c5ea3d78c2940ab1a9875c3141626c5016355da53c429`), and register v0.19 final; it needed no reply.

**Wave 2's rehearsal and installation.**
- **TASK_T008** (Claude Code) rehearsed the final package in a task clone: PASS on all 15 steps. Its report is `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T008.md` at `94a5e95`. Claude read it in full: 90 status lines (87 A and 3 M), 80 declarations and 202 registry chains, 299 tests with 3 symlink skips, and no deviations.
- **The owner installed it** at `b61b1a27999dcdfce2e2e59c6ced4f349ee652b4` (30 October 2026; parent `94a5e95`). The log is clean: `PRE PASS`; 90 files copied; `POST PASS`; `SUITE PASS` (299 tests, 3 symlink skips) before the commit; 87 A + 3 M; `COMMITTED PASS`; then the push.
- **Claude verified the commit from a fresh GitHub clone:**
  - `COMMITTED PASS`;
  - all 89 manifest blobs;
  - register v0.19 `b3ae51fd...e6a0`, design v0.1r2 `2ab34291...fe74`, and template draft 3 (`README.md` `daac8da1...2214`, `METHOD_SPECIFICATION_TEMPLATE.md` `1ef9df2d...8cfa`);
  - nothing outside `doc`, `review`, `src` and `tests`;
  - all 299 tests on Linux.
- **The four wave 2 methods** are installed and not runnable.

**The reviewer chat's end (30 October 2026).** The ChatGPT reviewer chat that wrote every review from the role transition to EX_075 reached its maximum length without warning, before it could update its handover.
- **The owner's instruction (OWNER-DECIDED 30 October 2026):** Claude brings both handovers up to date (H-1 and the reviewer's H-2), and writes an introductory blurb for each new chat. There is no other route, because the old reviewer chat cannot continue.
- **The owner's order:** Claude's own handover first, then the reviewer's.
- **The owner's naming:** each blurb is saved next to its handover, as `<handover file name>_introductory_blurb.md`.
- **The departure, recorded:** H-2 v1r6 says that handovers receive one other-model factual review. This round has none before ratification, by the owner's decision. The safeguards are:
  1. H-2's protected reviewer-rights region is byte-identical: 7,676 bytes, SHA-256 `70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db`, asserted by the builder;
  2. Claude changed only status, checkpoint, cold-start and change-control facts in H-2, and added no reviewer rule;
  3. H-2's header asks the new reviewer chat to read it critically on takeover, and its blurb makes that check part of the first reply;
  4. the owner may ask for a v1r8 after that check.

**The handovers (installed with this register):**
- `HANDOVER/Claude_Primary_Handover_H1_v1r6.md` (`{H['h1']}`): built from H-1 v1r5 by `make_h1_v1r6.py` (31 counted edits). Section 2A is byte-identical, which the builder asserts. Its Appendix B lists every change.
- `HANDOVER/Claude_Primary_Handover_H1_v1r6_introductory_blurb.md` (`{H['h1b']}`): the starter text for a new Claude chat.
- `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r7.md` (`{H['h2']}`): built from H-2 v1r6 by `make_h2_v1r7.py` (18 counted edits, the rights region asserted).
- `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r7_introductory_blurb.md` (`{H['h2b']}`): the starter text for the new reviewer chat. It lists exactly what to attach: the repository as a ZIP without `source_data`, `results` and `transitory_data`, and the five files to read first. Its first task is a takeover check.

The builders, the four diffs and the register builder are installed with this register under `review/DOC8_Handovers_v1/`; this round has no EX message, because there was no reviewer chat to send it to.

**Out-of-date statements (register v0.20).** This register prevails, and the files are not edited:
- Register v0.19, "installed with this register" for the wave 2 package: done, at `b61b1a2`, as above.
- H-1 v1r5 and H-2 v1r6 throughout: superseded by H-1 v1r6 and H-2 v1r7 once installed.
- H-2 v1r6 section 0, "Handovers receive one other-model factual review": not applied to this round, by the owner's decision above.
- `exchange/OWNER_ROADMAP.md` item 9b: done once this round is installed.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `HANDOVER/Claude_Primary_Handover_H1_v1r6.md` | Claude; no other-model review (above) | Installed with this register on the owner's ratification; `{H['h1']}` |
| `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r7.md` | Claude, on the owner's instruction; rights region byte-identical | Installed with this register on the owner's ratification; `{H['h2']}` |
| `RATIFICATION_REGISTER_v0_19.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 30 Oct 2026; installed at `b61b1a2`; superseded by this register; `b3ae51fd162960b64a9d145a52646dceeb3aec5b91e4b359ad7166e5e4c8e6a0` |

"""

EDITS = [
    ('**Register version:** v0.19 OWNER-RATIFIED 30 October 2026, recording',
     '**Register version:** v0.20 RATIFICATION CANDIDATE (drafted 30 October 2026), recording the wave 2 installation, the end of the previous reviewer chat, and the handovers H-1 v1r6 and H-2 v1r7 with their introductory blurbs; v0.19 OWNER-RATIFIED 30 October 2026, recording'),
    ("For v0.19, the wave 1 installation commit `947c370` was verified by Claude from GitHub. The wave 2 package and this register are installed together, in one commit identified after installation; the owner's Windows results for it are recorded after installation.",
     "For v0.19, the wave 1 installation commit `947c370` was verified by Claude from GitHub. The wave 2 package and this register are installed together, in one commit identified after installation; the owner's Windows results for it are recorded after installation. For v0.20, the wave 2 installation commit `b61b1a2` was verified by Claude from GitHub. This register, H-1 v1r6, H-2 v1r7 and their introductory blurbs are installed together by the document-only procedure, in one commit identified after installation."),
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
