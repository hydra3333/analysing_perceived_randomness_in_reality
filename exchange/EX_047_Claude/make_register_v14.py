"""Draft register v0.14 from the installed register v0.13 by counted in-place edits (Claude, 29 Oct 2026).

Records: the E2R-CODE-2 installation and acceptance (with the TASK_T004 rehearsal), the reviewer's EX_045
review, the owner decisions of 29 October 2026 after register v0.13, and H-1 v1r4 and H-2 v1r5, which are
installed with this register by the document-only procedure. Every old string must occur exactly once;
inserted text is ASCII. The input is the Git blob of doc/RATIFICATION_REGISTER_v0_13.md (6ff86e72...391e,
UTF-8, LF). Placeholders, finalised after review and the owner's ratification: "RATIFICATION CANDIDATE"
(version line); [H2-V1R5-SHA] (H-2 v1r5's LF hash, twice), filled when that file is final; and [H-STATUS]
(the two handovers' status cells), filled with their ratification status.
Usage: python3 -I make_register_v14.py REGISTER_v0_13 H1_V1R4_SHA256 OUT_v0_14
"""
import hashlib, sys

src, h1_sha, out = sys.argv[1:4]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '6ff86e728142ce47adb76cb975e9f1ad75f01de48b6ab71c005fdb6c2331391e'
t = raw.decode('utf-8')
assert '\r' not in t and len(h1_sha) == 64

NEW_SECTION = f"""## E2R-CODE-2 accepted, and the handovers refreshed (register v0.14)

Paths in this section are under `doc/`, except those beginning `review/`, `exchange/`, `src/`, `tests/` or `CLAUDE_CODE_WORKING_FOLDER_TREE/`, which are from the repository root. In this section, "this register" means register v0.14.

**E2R-CODE-2 installation verified and accepted.** CODE-2 and register v0.13 were installed at commit `ced9b6cbd43b98e9584b8020724388109eb28d68` (29 October 2026; parent `bce33b1`). The package was `E2R_CODE2_Install_v3.zip` (final, `ec643ceab097ca69630594e42551a2c7c4fc5ef5b4d8e6e593a7489a694c6969`), taken from `exchange/EX_046_Claude/`.
- **The owner's Windows run** (Windows 11, Python 3.15.2; owner-reported), in the reviewed order:
  - a clean tree and `git pull --ff-only`;
  - the ZIP hash checked with `certutil`;
  - PRE PASS; 25 files copied; POST PASS;
  - **before the commit**, `SUITE PASS`: all 190 tests including E2R-T12, with only the 3 allowed symlink skips;
  - 22 added and 3 modified files staged; COMMITTED PASS before the push.
- **Claude verified the commit from a fresh GitHub clone:**
  - exactly 22 added and 3 modified files;
  - COMMITTED PASS;
  - all 24 manifest entries match their blobs (manifest `75a0c1f4759a7b652e2c4dd35ff37ec8622bd939ca5dac883b6cf231e524b510`);
  - register v0.13 is `6ff86e72...391e`;
  - the 190 tests pass on Linux.
- **What it does not change:** as register v0.13 states. The four switches stay False, the allowlist stays empty, and E_1 keeps revision 1. Contract runs are standalone and synthetic only.
- **The final ZIP and the reviewed candidate.** After the owner ratified v0.13, the final ZIP differed from the candidate the reviewer checked (EX_045) in:
  - the register's version line, its manifest line and two verifier constants;
  - one sentence of the install instructions, corrected before use. It had said the only allowed skips were "the two symlink tests"; the unchanged suite runner also allows CODE-2's dangling-symlink skip, so it now says "up to 3".

  No code or test changed. Under the owner's decision (register v0.13), the reviewer did not check the final ZIP before the install. Claude sent the narrow diff for information (EX_046).

**The rehearsal (TASK_T004; OWNER-DECIDED in register v0.13).** Before the install, Claude Code ran the final package in a disposable task clone on the owner's machine: PASS in all 15 steps, including all 190 tests with T12, in 39 seconds, with the 3 symlink skips. The main repository was unchanged.
- The task and two tool updates are at `5b1481a`, and the report is at `bce33b1`. The tool updates:
  - `cc_clone.py overlay --replace`, which may replace only named, tracked files;
  - the module-origin check also covers CODE-2's modules.
- The report is owner-machine evidence produced by the runner; it is not reviewer evidence.

**The reviewer's review of register v0.13 (EX_045).** `review/Independent_ChatGPT_Register_v0_13_Content_Review_v0_1.md` (LF copy, `5ee5bba48ce5f9a43b330e7bfbdde6e6f33bd3f793dabc8d3e5a070b3343d56c`, installed with this register) passed v0.13's content and the package's identity, with 0 findings.
- **REVIEWER-DECIDED, checked by Claude, no exception to report:**
  - E2RC2-RD-16: register v0.13's content PASS; finalisation changes only the status line and its dependent identities;
  - RD-17: the package candidate's identity PASS: the reviewed v3 code and tests are unchanged.

**Owner decisions (29 October 2026, after register v0.13).**
- **OWNER-RATIFIED:** register v0.13. Only its version line changed from the reviewed candidate (`b1c21a2c...f22c` to `6ff86e72...391e`).
- **OWNER-DECIDED:**
  - E2R-CODE-3 (retirement tooling, E2R-T15) is kept in the plan; the owner expects the need soon;
  - **review rounds are combined:** register text goes to the reviewer only together with a code package or the handovers, never in a round of its own;
  - **the handovers are refreshed at milestones:** after CODE-2, now, and later when a method is released, a process changes, or a register's out-of-date list grows long. H-1 is shortened and points to the register for history.
- **Proportion (owner's remark, recorded):** the owner asked how much plumbing the project really needs. The answer adopted: keep the safety-critical machinery, and keep everything else lean. This changes no rule.

**H-1 v1r4 and H-2 v1r5 (installed with this register).**
- `HANDOVER/Claude_Primary_Handover_H1_v1r4.md` (`{h1_sha}`): Claude's handover, refreshed to `ced9b6c` and shortened. Its Appendix B lists what changed and where any material it no longer repeats now lives. It adds the process for adding a new method (its section 9). It changes no rule. It is reviewed by the ChatGPT reviewer chat.
- `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r5.md` (`[H2-V1R5-SHA]`): the reviewer's handover, refreshed by the reviewer chat. It gets one factual review by Claude.
- Each replaces its predecessor for future roles; the predecessors are kept as history. Neither authorises anything.

**Out-of-date statements (register v0.14).** This register prevails, and the files are not edited:
- Register v0.13, "installed with this register" for CODE-2: done, at `ced9b6c`, as above. Its review and Windows results, "recorded after installation", are recorded here.
- Register v0.13, "Claude sends the reviewer the narrow diff afterwards": done (EX_046).
- H-1 v1r3 and H-2 v1r4, generally: superseded by H-1 v1r4 and H-2 v1r5. The out-of-date statements of registers v0.10 to v0.13 that concern H-1 v1r3 are folded into H-1 v1r4.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `HANDOVER/Claude_Primary_Handover_H1_v1r4.md` | Claude; reviewed by the ChatGPT reviewer chat | [H-STATUS]; installed with this register; `{h1_sha}` |
| `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r5.md` | the ChatGPT reviewer chat; factual review by Claude | [H-STATUS]; installed with this register; `[H2-V1R5-SHA]` |
| `HANDOVER/Claude_Primary_Handover_H1_v1r3.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 28 Oct 2026; superseded by H-1 v1r4; `ddf4de23b726b2abf55ffcab613f926b62775469076476f939288a278e6422fc` |
| `HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r4.md` | the ChatGPT reviewer chat; factual review by Claude | OWNER-RATIFIED 28 Oct 2026; superseded by H-2 v1r5; `73b90ea348aea5fc337097a14ec4a8669258bc6cba55ce5a2485de26575f3f3a` |
| `RATIFICATION_REGISTER_v0_13.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 29 Oct 2026; installed at `ced9b6c`; superseded by this register; `6ff86e728142ce47adb76cb975e9f1ad75f01de48b6ab71c005fdb6c2331391e` |

"""

EDITS = [
    ('**Register version:** v0.13 OWNER-RATIFIED 29 October 2026, recording',
     '**Register version:** v0.14 RATIFICATION CANDIDATE (drafted 29 October 2026), recording the E2R-CODE-2 installation and acceptance, the owner decisions after register v0.13, and H-1 v1r4 and H-2 v1r5; v0.13 OWNER-RATIFIED 29 October 2026, recording'),
    ('The E2R-CODE-2 code and this register are installed together, in one commit identified after installation; the owner\'s Windows results for it are recorded after installation.',
     'The E2R-CODE-2 code and this register are installed together, in one commit identified after installation; the owner\'s Windows results for it are recorded after installation. For v0.14, the CODE-2 commit `ced9b6c` and the Claude Code commits named in its section were verified by Claude from GitHub; the Windows results are owner-reported. This register, H-1 v1r4 and H-2 v1r5 are installed together by the document-only procedure.'),
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
