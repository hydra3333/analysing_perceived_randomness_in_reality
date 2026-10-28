"""Draft register v0.12 from the installed register v0.11 by counted in-place edits (Claude, 29 Oct 2026).

Records: the E2R-CODE-1 v2 installation and its review history (EX_033..EX_037), the owner decisions
of 29 October 2026, and the Claude Code local runner. Every old string must occur exactly once;
inserted text is ASCII. The input is the Git blob of doc/RATIFICATION_REGISTER_v0_11.md
(704dbd63...96ea, UTF-8, LF). One placeholder, finalised after review and the owner's ratification:
"RATIFICATION CANDIDATE" (version line).
Usage: python3 -I make_register_v12.py REGISTER_v0_11 RECHECK_V2_SHA256 OUT_v0_12
"""
import hashlib, sys

src, recheck_sha, out = sys.argv[1:4]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '704dbd6383fcef5a4501b8dbc867eedcdabd8df82d1945e80dcddb5a2e0996ea'
t = raw.decode('utf-8')
assert '\r' not in t

NEW_SECTION = f"""## E2R-CODE-1 accepted and the Claude Code local runner (register v0.12)

Paths in this section are under `doc/`, except those beginning `review/`, `exchange/`, `src/`, `tests/` or `CLAUDE_CODE_WORKING_FOLDER_TREE/`, which are from the repository root. In this section, "this register" means register v0.12.

**E2R-CODE-1 v2 installation verified and accepted.** The contract library and register v0.11 were installed at commit `205ae73dba203d8a8bcaf9be66578b7fde9687aa` (29 October 2026; parent `8b359c6`, an owner document commit). The package was `E2R_CODE1_Install_v2.zip` (final, `5a2b978c96d82e3159cc50e8c24a2f29a944a39d29b7452452f8b484b9a23a11`), taken from `exchange/EX_037_Claude/`.
- **The owner's Windows run** (Windows 11, Python 3.15.2; owner-reported):
  - the ZIP hash checked with `certutil`; PRE PASS; 156 files copied; POST PASS; COMMITTED PASS before the push.
- **Departure, recorded.** The owner's log has no test run between POST and the commit. The owner ran the suite straight after the push, unchanged in the repository: `SUITE PASS`, all 138 tests including E2R-T12, with only the 2 allowed symlink skips. The same package bytes had already passed all 138 tests on the owner's machine in the Claude Code rehearsal TASK_T003 (below). No further action is needed.
- **Claude verified the commit from a fresh GitHub clone:** exactly 156 added files and nothing else; COMMITTED PASS; all 155 manifest entries match their blobs (manifest `cb60b3c8e272d76d7dd1221a2f49de518b6d8977895942b332e10b1aa915452b`); register v0.11 is `704dbd63...96ea`; the 138 tests pass on Linux.
- **What it does not change:** every existing file, as register v0.11 states. The three switches stay False and the allowlist stays empty. Nothing calls the library yet; E_1 keeps revision 1.

**Review history (EX_033 to EX_037).**
- **v1** (EX_033, `acb9f0ea...76fb`) was never installed. The reviewer's HIGH-tier RECHECK (EX_034; `review/Independent_ChatGPT_E2R_CODE1_HIGH_RECHECK_v0_1.md`, LF copy, installed with CODE-1) found 1 BLOCKER and 2 CORRECTION:
  - E2RC1-B01: the registry's immutability was shallow;
  - E2RC1-C01: `frozen_at_utc` accepted offsets and date-only values;
  - E2RC1-C02: the instructions' test count.
- **v2** (EX_035) fixed all three in exactly three code files, with 5 new tests. The reviewer's focused RECHECK (EX_036; `review/Independent_ChatGPT_E2R_CODE1_v2_Focused_RECHECK_v0_1.md`, LF copy, `{recheck_sha}`, installed with this register) passed with 0 findings. Its independent R-2 run passed 127 of 127 selected offline tests; the 10 tests that need the real masters and T12 were not run there.
- **REVIEWER-DECIDED, checked by Claude, no exception to report:**
  - E2RC1-RD-01: keep the HIGH tier and require a focused RECHECK of B01 and C01;
  - RD-02: C02 is FIX AND PROCEED;
  - RD-03: register v0.11's content accepted conditionally (no ratification inferred);
  - RD-04: R-2 recorded as PARTIAL;
  - RD-05 and RD-06: B01 and C01 closed, PASS;
  - RD-07: C02 closed, with v2's 138-test count;
  - RD-08: CODE-1 v2 passed and recommended to the owner, with the Windows and installation gates kept.
- **CODE-2 watchpoint** (EX_036, not a finding): the dispatch gate must fetch the installed registry entry again, never trust a copy a caller holds.

**Owner decisions (29 October 2026).**
- **OWNER-RATIFIED:** register v0.11. Only its version line changed from the reviewed candidate (`16a29efc...19ae` to `704dbd63...96ea`).
- **OWNER-APPROVED:** E2R-T12, which starts up to six ordinary Python worker processes that finish normally, for the rehearsal and the install run.
- **OWNER-DECIDED:** no reviewer check of the final ZIP before installation, as for E1-ALIGN. Claude sent the reviewer the narrow diff afterwards (EX_037: the register line, its manifest line and two verifier constants).

**The Claude Code local runner (OWNER-DECIDED 28 and 29 October 2026).**
- **What it is:** Claude Code, in VS Code on the owner's Windows machine, carries out task files written by Claude and reports what happened. It makes no design or code decisions. It works in disposable task clones taken from GitHub, whose link to GitHub is removed and which refuse every push, and it commits only its own report file. The owner pushes.
- **Authorisation:** the owner authorised Claude and Claude Code to read, write and commit in and under `CLAUDE_CODE_WORKING_FOLDER_TREE/`. Claude's exchange/ rule is unchanged.
- **The files:**
  - the rulebook `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (v0.2 at `423bd19`), which repeats every hard prohibition;
  - the helper tools under `CLAUDE_CODE_WORKING_FOLDER_TREE/tools/` and the task and report formats;
  - the root `CLAUDE.md` pointer and `.claude/settings.json` (which turns off web access and bypass mode and denies Git writes, data-folder reads and edits outside that folder), committed by the owner at `ee76fc0`.
- **The first tasks:**
  - T001 (report `e33ccbf`): STOP at its module-origin step, because Claude's helper still used the v1 registry attributes. Nothing was changed. The tool was fixed at `ae7102b`.
  - T002 (report `a6a92d7`): PASS. The v2 candidate rehearsed in a task clone; 137 tests (T12 left out).
  - T003 (report `9351e1a`): PASS. The final package rehearsed in a task clone; all 138 tests, including T12.
- **What its reports are:** owner-machine evidence produced by a runner, read by Claude from GitHub. They are not reviewer evidence and not acceptance by themselves. One known fidelity slip: the T002 report retyped one output line with a wrong character. Claude will add a helper that records each step's output itself.

**Out-of-date statements (register v0.12).** This register prevails, and the files are not edited:
- Register v0.11, "installed with this register" for CODE-1: done, at `205ae73`, as above. Its review results, "recorded after installation", are recorded here.
- E2R-CODE-1's install instructions (v1) gave 132 tests; v2 gives the correct 138.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `RATIFICATION_REGISTER_v0_11.md` | Claude; reviewed by the ChatGPT reviewer chat | OWNER-RATIFIED 29 Oct 2026; installed at `205ae73`; superseded by this register; `704dbd6383fcef5a4501b8dbc867eedcdabd8df82d1945e80dcddb5a2e0996ea` |

"""

EDITS = [
    ('**Register version:** v0.11 OWNER-RATIFIED 29 October 2026, recording',
     '**Register version:** v0.12 RATIFICATION CANDIDATE (drafted 29 October 2026), recording the E2R-CODE-1 installation and acceptance and the Claude Code local runner; v0.11 OWNER-RATIFIED 29 October 2026, recording'),
    ('The CODE-1 contract library and this register are installed together, in one commit identified after installation.',
     'The CODE-1 contract library and this register are installed together, in one commit identified after installation. For v0.12, the CODE-1 commit `205ae73` and the Claude Code commits named in its section were verified by Claude from GitHub; the Windows results are owner-reported. This register is installed by the document-only procedure.'),
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
