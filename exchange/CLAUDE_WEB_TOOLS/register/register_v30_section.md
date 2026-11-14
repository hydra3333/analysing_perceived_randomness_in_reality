## The handover round installed, the dependency change, the replacement reviewer, the owner's decisions and the first two Mode H prerequisites of 14 November 2026 (register v0.30)

Paths in this section are from the repository root. In this section, "this register" means register v0.30. Every commit named
here was checked by Claude from GitHub. This section records decisions already taken and events that happened; it makes no
new decision, and nothing in it authorises a check, an approval or a run.

**The documentation round installed.** The five files ratified by RAT-31 (H-1 v2 and its blurb, H-2 v2 r1 and its blurb,
register v0.29) were installed by the owner at **`5a8527b`** (14 November 2026); Claude's verifier
(`exchange/CLAUDE_WEB_TOOLS/doc_round_rat31/verify_doc_round.py`) reported COMMITTED PASS, every file equal to its ratified
bytes. The old handovers stay in `doc/HANDOVER/` as history, as the owner chose.

**The owner's dependency change.** On 14 November 2026 the owner edited and ran `install_upgrade_dependencies_into_venv.bat`
(39 direct packages; in its installation modes, its default included, it requests upgrades of pip and every listed package;
its `VERIFY` mode is read-only) and committed it at **`cc0ab73`** (with two duplicate GAIS
notes, outside the closure). At the owner's request Claude wrote TASK_T024; the Claude Code local runner reported **PASS**
(report `811d0cc`): the read-only `env_freeze_check.py` printed ENV PASS (90 distributions, every RECORD file present and
matching, no orphan; Python 3.15.2; environment digest `5bf4eb8a36ddb9063fbcb27ff1b692d38de3847321518e563f70c7219999a3f9`),
and the whole suite passed (571, with the 4 permitted symlink skips). The owner, asked whether dependency upgrades should stay
an always-review topic, chose to keep the review (W-23). EX_176 sent the change to the reviewer; **EX_177**: PASS WITH
CORRECTIONS. B01: T024 does not run the Windows W-suite, so W-23 needs the owner's decision (below). C01: the readiness sheet's
attribution wording, applied as sheet **r2c** (r2b had carried the new digest and the baseline `cc0ab73`). C02: the installer's
own evidence. C03: nothing to change. The environment digest at T016 (`966a2792...`, 27 distributions) is history; Approval 1
expects T024's value.

**The reviewer chat changed.** The ChatGPT reviewer chat that started on 6 November 2026 reached its maximum length on
14 November 2026, about 18:00, after EX_177. H-2 v2 r1 needed no new edition; Claude filled its blurb's placeholders
(`exchange/HANDOVER_2026_11_14_REVIEWER/NEW_REVIEWER_START_PASTE.md`) and wrote twelve blind takeover questions (**EX_178**),
whose answer key the owner held sealed (SHA-256 `8d3ca6db09ac419d75b22baa471b4a5f78848a7fc35d38d10277f7089c56697a`, published
in EX_178 before the answers). The new chat's first reply (recorded in
`exchange/HANDOVER_2026_11_14_REVIEWER/NEW_REVIEWER_FIRST_REPLY.md`) verified the rights region from Git's bytes (7,676 LF
bytes, SHA-256 `70e50dc3...72db`) and read RAT-31 as installed. Its answers (**EX_179**) were compared with the published key
(**EX_180**): 12 of 12. The owner accepted it as the standing independent reviewer under H-2 v2 r1. Its rights are unchanged.

**The owner's decisions of 14 November 2026 (evening).** Records: `exchange/DECISIONS/OWNER_DECISIONS_2026_11_14b_C02_AND_REVIEWER.md`
(as stored `7ba931c6d2cc1e216e851afb73bd3feba6243ab70371edffaa08e6becc62d6ac`) and the new living decision log
`exchange/DECISIONS/DECISION_LOG.md` (entries 1 to 5), each with the owner's exact words.
1. **The replacement reviewer accepted** (about 19:35).
2. **EX_177 C02 closed** (19:37): the installer's own output is gone; the owner reports that a separate ChatGPT conversation,
   not the project's reviewer and not in this repository, went through the run with him and judged it successful; with T024 he
   finds that sufficient and asks for no `pip check`.
3. **D1 to D7 decided as recommended** (about 19:50), after the reviewer's advice (**EX_181**, agreeing with each; D4
   strongly): D1 Oz Lotto from manifest to seal, then Powerball; D2 both games whatever the first shows, barring a technical
   or safety STOP; D3 a value-free witness push after each Approval 1 and before Approval 2, each on its own go; D4 the
   official-page check is done; D5 the updated masters and ledgers uncommitted until both seals, backups checked after each
   seal, any later push of raw files its own decision; D6 the value-free report files shared together after both seals where
   practicable; D7 each prerequisite and approval on its own go, in the sheet's order. They authorise nothing to run.
4. **The working approach P0-P6** (about 20:17; decision log entry 1): Claude's proposals (**EX_182**, with the owner's
   query recorded beside it), the reviewer's modifications (**EX_183**) and Claude's acceptance of every modification
   (**EX_184**) reached consensus, which the owner had said he would adopt. Working guidance only: one living recovery index
   (`exchange/CONTINUITY_NOW.md`), decisions classified by effect into three levels, one living decisions log, one NOW page, fixed
   identities for procedures used in high-consequence actions, an ideas backlog after Mode H, and a short independent process
   note from each AI at each substantial milestone. Where it differs from the installed handovers, they govern until their next
   editions; the reviewer's rights R-1 to R-11 and the eight RECHECK areas are unchanged; Mode H is unchanged.
5. **OUTLANDISH_01's method family** (about 20:32; decision log entry 3): it joins this project's method backlog, probably
   first among the methods still to do; it enters only through this project's normal route (an identity decision and a
   catalogue amendment for E_63 onward, design review, N-1 isolation, rework to the method contract, release, Q7); its runs in
   `GAIS/OUTLANDISH_01/` are not evidence for this project. The reviewer acknowledged it (EX_185).
6. **EX_177 B01 closed** (about 22:45; decision log entry 5), after the POC rerun (below), Claude's proposed wording (EX_186)
   and the reviewer's agreement with one qualification (EX_187): a **scoped W-23 acceptance for the dependency change of
   14 November 2026 (`cc0ab73`) only**. T024 and the POC rerun are accepted as sufficient. Not run: the timeout and process-tree
   cleanup case (`--with-timeout`), Ctrl+C, memory stress and the other W-suite lifecycle cases; the residual risk that those
   paths are unverified on the new environment is accepted, and it cannot be reliably quantified. This is not "W-23 PASS" and
   authorises nothing further.
The owner also said he plans no further package installs and will ask Claude first; his OUTLANDISH_01 work uses this venv and
is committed by naming `GAIS/OUTLANDISH_01/`.

**The first two Mode H prerequisites (14 November 2026; each on its own go).**
- **The Windows POC rerun (R-015 (b)):** run by the owner after the reviewer's agreement (EX_185), exactly as the reviewed
  instructions r3 (Git blob `1105ff1c6c37f8be9bbb99e8b833dfd8dfa0a097`), without `--with-timeout`. Every block matched its
  expected output: the five synthetic suite cases PASS, the launchers' success and exit-3 cases, both launchers refusing with
  exit 10 while the byte-code folder existed, the folder removed, no orphan marker, no byte-code, a clean tree before and after;
  the launcher's output digest equals the suite's built-in reference. **PASS** (EX_186; the reviewer's check EX_187). The window
  is recorded unchanged: `exchange/RUNS/POC_R015b_2026_11_14_owner_window.txt`
  (`8179ca7d56d0378e57ba4902f63bef10ea94042e0f21ed393f9c6ccb16fbb6d1`).
- **The updater's offline self-test:** `Run_Results_Updater.bat --self-test` printed only `[SELF-TEST] 13/13 PASS`, exit 0.
  Two untracked OUTLANDISH files were present before and after (expected: an empty status); both AIs judged the deviation
  benign. **PASS** (EX_188; the reviewer EX_189). The window: `exchange/RUNS/SELFTEST_2026_11_14_owner_window.txt`
  (`62b37f5c14d16715ac5d788b5129cf3cf8ff1d26ea237464d57b44f030a596da`). The owner then committed the OUTLANDISH files
  (`657a2c1`, merged at `a6c2894`); no file under `src/`, no root `.bat` and no `requirements.txt` has changed since `cc0ab73`.
No AI chat contacted any lottery website; no holdout was opened; the updater has never run live.

**The Claude handover H-1 v3 (15 November 2026).** A full edition built from H-1 v2's ratified bytes by counted edits and
whole-part replacements (`exchange/CLAUDE_WEB_TOOLS/h1v3/make_h1_v3.py`; the diffs from v2 in `exchange/CLAUDE_WEB_TOOLS/h1v3/out/`),
with its blurb, bringing H-1 to this checkpoint and recording the working approach as section 1.7. It changes no rule; section
2A is byte-identical. Sent with this register as **EX_190** for the reviewer's documentary review; **EX_191**: PASS WITH CORRECTIONS (C01 the
installer's modes; C02 the recovery index; O01 which steps share a day), applied as FIX AND PROCEED in EX_192. The reviewer
judged that H-2 v2 r1 needs no new edition before the freeze.

**RAT-32 (owner, 15 November 2026, about 09:10).** Record: `exchange/DECISIONS/DECISION_LOG.md`, entry 6. Asked whether he
ratifies "the three reviewed files for installation: H-1 v3, its blurb, and register v0.30 (RAT-32)", with H-1 v2 staying in
`doc/HANDOVER/` as history, the owner answered "Yes, ratify all three". H-1 v3 replaces H-1 v2 as the operative Claude
handover; H-2 v2 r1 stays the reviewer's. Only H-1 v3's status line, and this register's version line, this paragraph and
its table's status cells, changed after the review. The ratification authorises the documentation install only, nothing for
Mode H. The install commit cannot be named here; the next register edition records it.

**Future actions (updating register v0.29's list; not authorisations).**
1. The reviewer's review of H-1 v3 and this register (EX_190); the owner's ratification; one owner-run documentation install,
   before the day of the first Approval 1, so that no `doc/` change is pending during the freeze. The reviewer judges whether
   H-2 needs a new edition.
2. Each on its own go: the official-page check, which the readiness sheet requires on the same day as the first Approval 1;
   the backup confirmation (R-015 (c)), the tree and identity checks and a quiet machine; then Oz Lotto's Approval 1. The later
   approvals (Oz Lotto's 2 to 4, then Powerball's 1 to 4) keep their own gos and their own safe schedule, with the freeze from
   the first Approval 1 until both games are sealed; the sheet also allows a separately approved Powerball-only page recheck
   after Oz Lotto is sealed and before Powerball's Approval 1.
3. Unchanged from register v0.29, items 3 to 5: after both seals the study recorded, the holdout exposure record and the
   handovers refreshed, then MHUP-B with everything it must carry; Q7 into the next editions; WF-1C; the methods still to do,
   now with OUTLANDISH_01's family probably first; KISS-1 when the owner asks; the next editions of R3, E2R-1, Architecture
   and the proposal. The ideas backlog (P5) after Mode H.

**Out-of-date statements (register v0.30).** This register prevails, and the files are not edited:
- **Register v0.29, future actions 1 and 2:** D1-D7 are decided; the POC rerun and the self-test have run; the documentation
  install is done (`5a8527b`).
- **H-1 v2, sections 6, 10 and 11 and Appendix A:** the environment digest `966a27926d23...` (now `5bf4eb8a36dd...`); "D1 to D7"
  as open; the POC rerun and self-test as not run; the readiness sheet as r2a (now r2c). Replaced by H-1 v3 once it is installed.
- **H-2 v2 r1, its statements of the afternoon of 14 November 2026** (the reviewer chat in office then; D1-D7 pending; the
  prerequisites not run; EX_177 not yet written): overtaken by this register and by `exchange/CONTINUITY_NOW.md`; the
  reviewer decides whether its next edition is needed now. Its rights region is unaffected.
- **The readiness sheet r2a and r2b:** superseded by r2c.
- **The owner's roadmap's NOW block** (`exchange/OWNER_ROADMAP.md`): kept as history; the live NOW is `exchange/CONTINUITY_NOW.md`.

| Document (path) | Author / check | Status and Git-content SHA-256 |
|---|---|---|
| `doc/RATIFICATION_REGISTER_v0_29.md` | Claude, from the records | OWNER-RATIFIED 14 Nov 2026 (RAT-31); installed at `5a8527b`; superseded by this register; `03efd2bac52272494a177a2654f6bcc852a3337eb5f506a73a2784064042f752` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v3.md` | Claude, from H-1 v2 and the records | OWNER-RATIFIED 15 Nov 2026 (RAT-32); `@H1V3@` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v3_introductory_blurb.md` | Claude | OWNER-RATIFIED 15 Nov 2026 (RAT-32); `@H1V3B@` |
| `exchange/DECISIONS/OWNER_DECISIONS_2026_11_14b_C02_AND_REVIEWER.md` | the owner's words, recorded by Claude | OWNER DECISIONS 14 Nov 2026; as stored `7ba931c6d2cc1e216e851afb73bd3feba6243ab70371edffaa08e6becc62d6ac` |
| `exchange/DECISIONS/DECISION_LOG.md` and `exchange/CONTINUITY_NOW.md` | Claude, from the owner's words and the records | living files (P2, P0); no fixed hash; Git keeps their history |
| `exchange/CLAUDE_WEB_TOOLS/modeh_readiness/APPROVAL_1_READINESS_SHEET_DRAFT.md` (r2c) | Claude; the reviewer (EX_167, EX_168 PASS; EX_177) | REVIEWED DRAFT; authorises nothing; as stored `8f31c5ba1fd12984ce266f52e1e27a77d7208164e1974895bf9f774a4af357a1` |
| `install_upgrade_dependencies_into_venv.bat` (at `cc0ab73`) | the owner | the owner's change; scoped W-23 acceptance; `c45cc336b758c39d6ccf33269fc2d1e96dd508192719c638bcc2416096f388b3` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T024.md` (at `811d0cc`) | the Claude Code local runner | TASK_T024 PASS; `a68a05771e4dfb06cda610bec881e80dba5facfaa48ee5441e33c10780b900ee` |
| `exchange/EX_180_Claude_EX_178_ANSWER_KEY.md` | Claude (held sealed by the owner until EX_179) | as stored `8d3ca6db09ac419d75b22baa471b4a5f78848a7fc35d38d10277f7089c56697a` |

