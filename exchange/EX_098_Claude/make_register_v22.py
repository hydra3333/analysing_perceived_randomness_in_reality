"""Draft register v0.22 from the installed register v0.21 by counted in-place edits (Claude, 31 Oct 2026).

Records: EX_085 and the owner's acceptance of REL-1 and WF-1A; the REL-1, WF-1A and E_1 revision 2 (with CODE-3)
installations and their rehearsals T009 to T011; the CODE-3 and E_1 revision 2 design and code reviews (EX_086 to
EX_097) and the owner's decisions; the first two walk-forward batches; the owner's performance proposal; and the
owner's directions for WF-1B. Every old string must occur exactly once; inserted text is ASCII. Input: the Git blob
of doc/RATIFICATION_REGISTER_v0_21.md (65524f92...8405). Placeholder, finalised after the owner's ratification:
"RATIFICATION CANDIDATE" (version line). This register is installed by the document-only procedure.
Usage: python3 -I make_register_v22.py REGISTER_v0_21 OUT_v0_22
"""
import hashlib, sys

src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '65524f92b99db2f9556c300536700af43bb1e449c55a998c8c87f427e1b78405'
t = raw.decode('utf-8')
assert '\r' not in t

NEW_SECTION = """## The installs, E_1 revision 2 and the first walk-forward batches (register v0.22)

Paths in this section are under `doc/`, except those beginning `review/`, `exchange/`, `src/`, `tests/`, `archive/`, `results/` or `CLAUDE_CODE_WORKING_FOLDER_TREE/`, which are from the repository root. In this section, "this register" means register v0.22. Every commit named here was verified by Claude from GitHub; the owner's Windows results are owner-reported.

**WF-1A's RECHECK and the owner's acceptance (EX_085, EX_086).**
- **EX_085** (`ef51305`): focused RECHECK PASS of WF-1A v2 (WF1A-R2-B01 resolved); REL-1 v2 has no new code or test change; register v0.21 candidate 2 is consistent. 0 BLOCKER, 0 CORRECTION, 0 OPTIONAL, 0 RECONSIDER. The reviewer ran 7 of WF-1A's 22 test methods and a probe of its own; the full suites are author evidence.
- **The owner (31 October 2026)** ratified register v0.21 and accepted REL-1 v2 and WF-1A v2 for installation, REL-1 first.
- **EX_086** (`1a90281`) recorded the final REL-1 package, `exchange/EX_086_Claude/REL1_Install_v2.zip` (`3ca731fe22ffc10a2dd4f59fd5f5725f9f6c88553a426f12eea395795e1e4b36`). Of its 100 members only three differ from candidate 2: register v0.21's version line, the manifest's register line, and the verifier's two constants for them. EX_087's part A checked that record.

**REL-1 installed.**
- **TASK_T009** (Claude Code; report `bf61c97`) rehearsed it in a task clone: PASS on all 16 steps; 304 tests with 3 symlink skips; 108 status lines (92 A, 5 M, 11 D). The task needed `git rm` in a task clone, which `CLAUDE_CODE_WORKING_FOLDER_TREE/tools/cc_clone.py` v0.3 allows (`1a90281`).
- **The owner installed it** at `6a1bed9e9de4c733e76afeea8cecbdd39e89f97d` (31 October 2026; parent `41d2da3`).
- **Claude verified it from a fresh GitHub clone:** `COMMITTED PASS` (92 A, 5 M, 11 D); `src/` and `tests/` equal the reviewed tree; register v0.21 is `65524f92...8405`. The 39 variants of E_2, E_3, E_4, E_6, E_7, E_8, E_9, E_10, E_17, E_18 and E_19 are released in both games.

**WF-1A installed.**
- **The final package** is `CLAUDE_CODE_WORKING_FOLDER_TREE/packages/WF1A_Install_v2.zip` (`9fa6577ab95d5a16931a6df7c056764f06a61282e2f78a497b2292610a9e3c06`; `6fd4955`). Of its 18 members only `VERIFY_WF1A_INSTALL.py` differs from the reviewed candidate, in its base constant (`6a1bed9`). It is in that folder, not `exchange/`, because it needed no EX number (the folder's README says so).
- **TASK_T010** (report `d0a1036`): PASS on all 15 steps; 326 tests with 3 symlink skips; 15 status lines (10 A, 5 M).
- **The owner installed it** at `0d98706dfcc40a8f09d3c8c94a13665ac152f168` (31 October 2026; parent `d0a1036`), with `COMMITTED PASS` before the push.
- **Claude verified it from a fresh GitHub clone:** `COMMITTED PASS` (10 A, 5 M); `src/`, `tests/` and `.gitignore` equal the reviewed tree.
- **`ENABLE_CONTRACT_REAL_DEVELOPMENT` is now True** (WF1-3). The other three switches stay False, and the science allowlist stays empty.

**CODE-3 and E_1 revision 2: the design (EX_086 to EX_091).**
- **EX_086** (`1a90281`) sent the design note v0.1 for R-3. **EX_087** (`cf5b065`): RECHECK, with 1 BLOCKER (E1R2-R3-B01: the install's interim states were not fail-closed: r2's code could run under r1's approval), 2 CORRECTION (C01: a test-time archive load; C02: no independent Oz Lotto real-namespace oracle) and 1 OPTIONAL (O01: the README's retirement date).
- **EX_088** (`d06eb25`): v0.1r1, resolving all four. **EX_089** (`ae190c7`): B01, C01 and C02 resolved, O01 adopted; a new C03 (CORRECTION: the barrier test's expected refusal codes did not follow the gate's order) and O02 (OPTIONAL: a STOP after the barrier's removal).
- **EX_090** (`13af75d`): v0.1r2, with a table of the exact refusal code for each request after each install step. **EX_091** (`babb238`): focused RECHECK PASS; O03 (OPTIONAL: the barrier test's step-0 planning wording), applied in the code's test.
- **The design ratified:** `Predictive_Randomness_CODE3_and_E1_Revision2_Design_v0_1r2.md` (`fb3b26daba2a14c6e2b5ad82e102ed9920faba14115046a820fbd0ee63b7209a`), OWNER-RATIFIED 31 October 2026 as reviewed, and installed with the package below.
- **The owner's decisions on it (31 October 2026):**
  - **ER-1:** one package for CODE-3's tooling and E_1 revision 2.
  - **ER-2r1** (replacing ER-2 after EX_087 B01): one package, installed in five named steps behind a temporary barrier, E_1's own `IN_DEVELOPMENT.txt`, copied first and deleted last and never committed. An exception to E2R-R58's recommended two packages, for E_1 only.
  - **ER-3:** the archive holds revision 1 complete, including the files revision 2 keeps unchanged and the legacy entry file; an old path is removed only when the successor does not reuse it.
  - **ER-4:** the contract adapter's stale docstring sentence is corrected, with no code change.
  - **ER-5:** records WF1-13 itself.
  - **ER-6 declined:** no method-restricted batch plan. Every batch holds the full cohort.

**CODE-3 and E_1 revision 2: the code (EX_092 to EX_097).**
- **EX_092** (`41d2da3`) sent `E1R2_Install_v1` for R-2. **EX_093** (`18f0d70`): RECHECK, with 1 BLOCKER (E1R2-R2-B01: the archive-execution check missed paths built in pieces, such as `Path("archive") / "methods"`, and the claim that `archive/` could not be imported was overstated, because Python 3's namespace packages need no `__init__.py`) and 1 OPTIONAL (O01: check every input before writing).
- **EX_094** (`3873461`): `E1R2_Install_v2`, resolving both. **EX_095** (`a4b5dfe`): focused RECHECK PASS; O02 (OPTIONAL: the check folds constants within one expression, so a path root assigned on one line and joined on another escaped it).
- **The owner (31 October 2026)** accepted the package and chose to apply O02 before installing, with the reviewer's check of that change: any path construction with an `archive` component is now flagged.
- **EX_096** (`c805bf8`): `E1R2_Install_v3` (`exchange/EX_096_Claude/E1R2_Install_v3.zip`, `8547fd37fea6e5dc6a1f1941322cc5844031f2351bd50fb4c1ee1179086a2394`), built on WF-1A's install commit `0d98706`. **EX_097** (`4f1aae2`): focused RECHECK PASS, 0 BLOCKER, 0 CORRECTION, 0 OPTIONAL, 0 RECONSIDER.
- **REVIEWER-DECIDED, checked by Claude, no exception to report:** none in this round; every change went back to the owner or to a RECHECK.

**CODE-3 and E_1 revision 2 installed.**
- **TASK_T011** (report `ef439c6`) rehearsed the five steps in a task clone: PASS on all 21 steps; every verifier phase passed (pre, barrier, code, release, post, committed); 350 tests with 3 symlink skips; 40 status lines (33 A, 7 M) and no barrier file.
- **The owner installed it** at `86d12ea913d443c4ad944ee8db167df705841af1` (31 October 2026; parent `4f1aae2`), with `COMMITTED PASS` before the push.
- **Claude verified it from a fresh GitHub clone:** `COMMITTED PASS` (33 A, 7 M); no barrier file in the commit; `src/`, `tests/` and `archive/` equal the reviewed tree.
- **What it installed:**
  - **CODE-3:** `src/package_tools/method_retirement.py`, the retirement tooling (E2R-R54 to R56, T15), reusable for later successors.
  - **The archive:** `archive/methods/E_001/r1/`, E_1 revision 1's seven files unchanged, with its README (no commit ID and no hash).
  - **E_1 revision 2:** its multi-game function admits `REAL_DEVELOPMENT` as well, with revision 1's counting, ranking and tie order; its legacy runner's release gate (D2-3) names revision 2; new r2 declarations and `SUPPORTED` entries in both games; WF-1A's `NOT_REAL_CAPABLE` is empty.
- **E2R-R56, as installed:** nothing in `src/` or `tests/` may refer to a path or module inside `archive/`, enforced by a static check (constants folded within one expression, plus any path construction with an `archive` component) and a runtime check (no module from `archive/`, namespace packages included). The missing `__init__.py` files are a layout rule, not an import barrier. It is a normal-workflow control, not a security boundary.

**The first walk-forward batches (owner-authorised and run, 31 October 2026).** The owner decided to run no batch until E_1 revision 2 was installed, so that each game's first batch holds all 40 variants. Each batch was planned and run by the owner with `Run_Experiment.bat Method_Walk_Forward.py`, led step by step by Claude; Claude Code runs no batch.
- **Powerball:** batch `wf-3347ad1160df45faaaab1e2eedcedd0f`, targets 1145-1576, 40 variants, master version 1 (`ce0ae7e77e09...`, as recorded for draws 1144-1576). `COMPLETE`: 17,280 runs, and every pair proven done by this batch's own attempts. The owner's `status` checks during the run (to about a third of it) showed only `SUCCESS`, consumable under the plan's pins. Its plan, segment record and search-log row were committed by the owner at `86a1a01`.
- **Oz Lotto:** batch `wf-a75988650fb04cc399f8f7409ea27243`, targets 1475-1693, 40 variants, master version 1 (`4a6cecc27fb6...`, as recorded for draws 1474-1693). `COMPLETE`: 8,760 runs, and every pair proven done by this batch's own attempts. Committed at `8430a15`.
- **What was committed:** only `results/audit/SEARCH_LOG.csv` and each batch's `plan.json` and segment record under `results/real/development/wf_batches/`. The run folders and `attempts.jsonl` stay local and git-ignored. Claude checked those commits' paths and sizes from GitHub, not their contents.
- **Evidence tier:** retrospective development walk-forward (`DEVELOPMENT_WF_EXPLORATORY`). Nothing is scored yet; scoring is WF-1B. No holdout target was predicted.

**The owner's performance proposal (owner-committed, not reviewed).** `Deferred_Performance_Engineering_Proposal_v0_1.md` (`a5ed53c7d0cfb3278ef8342043ab1d39a99557f6f79684f3bd3276d61a5b22cb`), committed by the owner at `1050338` (31 October 2026). It is scheduled as the project's final stage (`exchange/OWNER_ROADMAP.md` item 22; `exchange/OWNER_REMINDERS.md` R-006), to start only when the owner activates it. Not reviewed, not ratified, and it authorises nothing. The owner added a note to R-006: a walk-forward batch runs one method run at a time on one CPU core, and running variants in parallel is to be studied there.

**The owner's directions for WF-1B (31 October 2026).**
- **The report leads with the descriptive league tables:** methods ranked by their scores against the real draws only. The significance tables, against fair random draws (R3 17.5; N1), follow separately and are titled as such. This is presentation within R3 section 17, which already has both kinds of table, and changes no ratified rule.
- **A progress line in the walk-forward driver** (runs done, the current variant and target, elapsed time and an estimate) comes with WF-1B. Meanwhile the read-only `status` command gives the same facts.

**Other process records.**
- **Review copies installed with this register** (LF), for the reviews not yet under `review/`:
  - `review/Independent_ChatGPT_WF1A_REL1_Code_R2_Review_EX083.md` (`262fe0da97d147a4c78375f84a70ab47516bbe986d80bc82e017a404b336b9fe`);
  - `review/Independent_ChatGPT_WF1A_Code_Focused_RECHECK_EX085.md` (`0764cadf4d6a0f5c9284aae54ba9d284977d0a9c4db611fa98142babfcf52c54`);
  - `review/Independent_ChatGPT_E1R2_Code_Focused_RECHECK_EX097.md` (`7cfc20233104aff876573f013d189be462c6e09ce87f8efd62ad4c89a61035f3`).

  The E_1 revision 2 package installed the copies of EX_087, EX_089, EX_091, EX_093 and EX_095.
- **The exchange numbering:** a final package that differs from its reviewed candidate only in its verifier's base can go in `CLAUDE_CODE_WORKING_FOLDER_TREE/packages/`, named in a task file and recorded in the next register, so that it needs no EX number.
- **The owner's nine commits in this period:** the performance proposal (`1050338`); the three Claude Code reports (`bf61c97`, `d0a1036`, `ef439c6`); the three installations (`6a1bed9`, `0d98706`, `86d12ea`); and the two batch commits (`86a1a01`, `8430a15`). Claude's own commits touched only `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`.

**Out-of-date statements (register v0.22).** This register prevails, and the files are not edited:
- **Register v0.21, "installed with this register" and "WF-1A follows in its own commit":** done, at `6a1bed9` and `0d98706`.
- **Register v0.21 and WF1-13's interim:** "E_1 revision 1 is not real-capable; families have M = 78": ended with E_1 revision 2 (`86d12ea`). Each game's batch holds 40 variants, so WF-1B's MR7 families have M = 80, as designed.
- **E2R-CODE-2's E2RC-C04 reading,** "E_1 keeps revision 1 ... real runs stay off": superseded by WF1-13 and E_1 revision 2; the adapter's docstring is corrected.
- **D2-3,** the legacy runner's release gate pinned to revision 1: the gate is kept and now names revision 2.
- **H-1 v1r6 and H-2 v1r7, "the four switches stay False":** `ENABLE_CONTRACT_REAL_DEVELOPMENT` is True since WF-1A; the other three stay False. Their other status lines are superseded by this register.
- **The CODE-3 and E_1 revision 2 design v0.1r2, sections 4.1 and 7A,** where they imply that `archive/` is outside every import path: read as above (EX_093); the protection is that nothing refers to the archive, with the static and runtime checks.

| Document (path under `doc/`) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `Predictive_Randomness_CODE3_and_E1_Revision2_Design_v0_1r2.md` | Claude; reviewed by the ChatGPT reviewer chat (EX_087, EX_089, EX_091) | OWNER-RATIFIED 31 Oct 2026; installed at `86d12ea`; `fb3b26daba2a14c6e2b5ad82e102ed9920faba14115046a820fbd0ee63b7209a` |
| `Deferred_Performance_Engineering_Proposal_v0_1.md` | The owner (committed at `1050338`); not reviewed | Scheduled as the final stage; not ratified; `a5ed53c7d0cfb3278ef8342043ab1d39a99557f6f79684f3bd3276d61a5b22cb` |
| `RATIFICATION_REGISTER_v0_21.md` | Claude; content checked by the ChatGPT reviewer chat (EX_083, EX_085) | OWNER-RATIFIED 31 Oct 2026; installed at `6a1bed9`; superseded by this register; `65524f92b99db2f9556c300536700af43bb1e449c55a998c8c87f427e1b78405` |

"""

EDITS = [
    ('**Register version:** v0.21 OWNER-RATIFIED 31 October 2026, recording',
     '**Register version:** v0.22 RATIFICATION CANDIDATE (drafted 31 October 2026), recording the REL-1, WF-1A and E_1 revision 2 installations, the CODE-3 and E_1 revision 2 design and code reviews with the owner\'s decisions, the first walk-forward batches and the owner\'s performance proposal; v0.21 OWNER-RATIFIED 31 October 2026, recording'),
    ("The REL-1 package and this register are installed together, in one commit identified after installation; WF-1A follows in its own commit. The owner's Windows results for both are recorded after installation.",
     "The REL-1 package and this register are installed together, in one commit identified after installation; WF-1A follows in its own commit. The owner's Windows results for both are recorded after installation. For v0.22, the installation commits `6a1bed9` (REL-1), `0d98706` (WF-1A) and `86d12ea` (CODE-3 and E_1 revision 2), the batch commits `86a1a01` and `8430a15`, and the exchange records from `ef51305` onward were verified by Claude from GitHub; the Windows results are owner-reported. This register is installed by the document-only procedure, in one commit identified after installation."),
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
