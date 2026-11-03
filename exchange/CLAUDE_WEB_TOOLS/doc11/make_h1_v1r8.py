"""H-1 v1r8 from the installed H-1 v1r7 by counted edits (Claude, 3 Nov 2026).

v1r8 is the full working handover after the MHUP-1 design's ratification (owner, 3 November 2026: "functional, not
kept short", pointing to register v0.24 and the design rather than repeating them). It brings every section up to
DOC-11: the chat switch done, the stock-take, the direction document, the MHUP-1 decisions and ratification, the
model-choice instruction, the next work (MHUP-A, MHUP-B, the approvals) and the future actions, and adds the lessons
of the new chat. It changes no rule; where it states one, the ratified documents and the register prevail.
Section 2A (the owner's foundational points) must stay byte-identical; the builder asserts the whole section.
Usage: python3 -I make_h1_v1r8.py H1_v1r7 OUT STATUS(CANDIDATE|RATIFIED)
"""
import hashlib, sys

src, out, status = sys.argv[1:4]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == 'b51f63792dde7f7d6c0c9e01ea6cecc5b5a12038ba748b91647738273ebc29fb'
t = raw.decode('ascii')
assert '\r' not in t


def section(text, head, nxt):
    i = text.index(head)
    return text[i:text.index(nxt, i)]


S2A = section(t, '### 2A. The owner\'s foundational points', '---\n\n## 3.')
E = []


def rep(old, new):
    E.append((old, new))


def rep_between(head, nxt, new):
    assert t.count(head) == 1 and t.count(nxt) == 1, (head[:50], nxt[:50])
    E.append((section(t, head, nxt), new))


DESIGN = '`doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r5.md`'
STATUS = {
    'CANDIDATE': '**Status:** CANDIDATE for the reviewer\'s check and the owner\'s ratification with register v0.24 (DOC-11). Until it is ratified and installed, H-1 v1r7 stands. Nothing here grants any run, test, data-access, holdout, termination or Git permission.',
    'RATIFIED': '**Status:** OWNER-RATIFIED @@DATE@@ with register v0.24 (DOC-11); authoritative once installed. Nothing here grants any run, test, data-access, holdout, termination or Git permission.',
}[status]

# ================================================================ header
rep('# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v1r7',
    '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v1r8')
rep(t[t.index('**Version:** v1r7, 1 November 2026'):t.index('\n', t.index('**Version:** v1r7, 1 November 2026'))],
    '**Version:** v1r8, 3 November 2026 (Adelaide, UTC+10:30). v1r8 brings the handover up to the ratification of the MHUP-1 design (Mode H, the results update and the prospective mode) on 3 November 2026, so that if this Claude chat runs out of room, a new one can carry on from the repository alone (the owner\'s risk posture, 3 November 2026). On the owner\'s instruction it is a full working edition, not a short one, but it **points to register v0.24 and the design rather than repeating them**. The Claude chat that wrote it took over from the previous chat on 1 November 2026 (H-1 v1r7); the previous chat was retired on 2 November 2026. It changes no rule. Appendix B lists what changed. Author: Claude. The project owner ratifies. The ChatGPT reviewer chat that started on 30 October 2026 continues.')
rep('**Status:** OWNER-RATIFIED 1 November 2026 (content reviewed in EX_117, EX_119 and EX_121). It is authoritative once installed with register v0.23 (the snapshot, DOC-10); until that install H-1 v1r6 stands. Nothing here grants any run, test, data-access, holdout, termination or Git permission.',
    STATUS)
rep('**Baseline described:** WF-1B v3 installed at `24d192fe596dc381fe2945e3b88503e68ff60d44` (1 November 2026; verified by Claude from GitHub; section 7), PERF-1 installed at `3fce3270b4797198504c85893e77e1d8f3aa35a1` (1 November 2026; verified), and the owner\'s report commits `441daf2` (Oz Lotto) and `608025c` (Powerball). Other later commits are `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/` records. The commit that installs this file cannot name itself; Claude records it in the post-push check.',
    '**Baseline described:** the code is unchanged since PERF-1 at `3fce3270b4797198504c85893e77e1d8f3aa35a1` (1 November 2026; verified by Claude from GitHub; section 7); documents: DOC-10 at `7bb0bfd` (register v0.23, the snapshot), the owner\'s settings deny line `905ecee`, his stock-take and direction commits (`f47ce14` to `6de0d99`), and the exchange records through EX_132 (`79f6ea6`). The commit that installs this file cannot name itself; Claude records it in the post-push check and register v0.25.')
rep('**Replaces, for future roles:** H-1 v1r6, v1r5, v1r4, v1r3, v1r2 and v1r1 (kept as history)',
    '**Replaces, for future roles:** H-1 v1r7, v1r6, v1r5, v1r4, v1r3, v1r2 and v1r1 (kept as history)')

# ================================================================ section 0
rep('1. Clone `main`. Check that this file\'s Git-content SHA-256 equals its line in the snapshot\'s manifest, `review/DOC10_Snapshot_v1/INSTALL_MANIFEST_SHA256.txt` (a file cannot name its own hash; later register editions record it), and that the hashes in sections 4 and 7 and Appendix A match `git show HEAD:<path> | sha256sum`.',
    '1. Clone `main`. Check that this file\'s Git-content SHA-256 equals its line in DOC-11\'s manifest, `review/DOC11_Claude_Handover_v1/INSTALL_MANIFEST_SHA256.txt` (a file cannot name its own hash; register v0.24\'s table and later editions record it), and that the hashes in sections 4 and 7 and Appendix A match `git show HEAD:<path> | sha256sum`.')
rep('2. Read, in order: the introductory blurb that started your chat (`doc/HANDOVER/Claude_Primary_Handover_H1_v1r7_introductory_blurb.md`); this file, **including section 12 (Working knowledge)**; H-2 (what the reviewer checks and its rights); the **current register\'s newest sections** (register v0.23 and later; they hold everything since this file);',
    '2. Read, in order: the introductory blurb that started your chat (`doc/HANDOVER/Claude_Primary_Handover_H1_v1r8_introductory_blurb.md`); this file, **including section 12 (Working knowledge)**; H-2 (what the reviewer checks and its rights); the **current register\'s newest sections** (register v0.24 and later; v0.24\'s section records the stock-take, every MHUP-1 decision, the ratification, the rules it amends and the future actions with when each falls due); **the ratified MHUP-1 design**, ' + DESIGN + ' (the specification for the next two code packages; read its section 0 first, then sections 1 to 10, then the appendices as each package needs them); `doc/Direction_for_operational_procedures_v0_2r1.md` (the owner-ratified direction in plain English; the design prevails where it is looser);')
rep('3. Ask the owner where things stand, using section 10 and `exchange/OWNER_ROADMAP.md` as the list. Do not assume anything has advanced since this file was written; in particular, check the placeholders this file had at drafting (the two first reports, PERF-1) against the register.',
    '3. Ask the owner where things stand, using section 10 and `exchange/OWNER_ROADMAP.md` (item 10c) as the list. Do not assume anything has advanced since this file was written; in particular, check that DOC-11 is installed, what the reviewer\'s Step 1.1 review of the handover package (EX_133) concluded and how it was resolved, and that no MHUP-A work has started.')

rep('4. Before any code: name the work item, its risk tier and its reviewer chat (section 1.2), and check that the owner has scoped it.',
    '4. **The staged takeover (owner, 3 November 2026; register v0.24, HO-2), before any work at all:** your first substantive reply to the owner explains, in your own words: what is implemented, what is designed, what is ratified and what is still unresolved; the current project position and the immediate priorities; the next tasks, their dependencies and the approvals still outstanding; the important safety, scientific and operational restrictions; exactly what you believe you are authorised to do next, and what you must not do without the owner\'s further approval; and any discrepancies, uncertainties or questions. **Do not implement, install, build or execute anything because this file names it as the next task.** The owner passes your reply to the existing ChatGPT reviewer chat, which assesses it and suggests targeted questions; answer those questions yourself, before you see the reviewer\'s suggested answers or assessment. Material discrepancies are resolved before the takeover counts as successful, and normal work resumes only after the owner authorises it. The ChatGPT reviewer chat is **not** being replaced: it stays in role throughout, and a reviewer handover is considered separately, later.\n5. Before any code (once the owner has authorised normal work): name the work item, its risk tier and its reviewer chat (section 1.2), and check that the owner has scoped it.')
rep('5. Keep a running checkpoint', '6. Keep a running checkpoint')
rep('6. Work through section 12.9\'s first-hour checklist before the owner\'s first task.', '7. Work through section 12.9\'s first-hour checklist before your first reply (it reads and checks; it builds and runs nothing on the owner\'s machine).')

# ================================================================ section 1
rep('That reviewer chat has reviewed everything from EX_077 to EX_115 and continues across this Claude chat switch.',
    'That reviewer chat has reviewed everything from EX_077 to EX_131 (including the snapshot, the direction document\'s content check and the four MHUP-1 design rounds), checked the new Claude chat\'s takeover reply (PASS, 1 to 2 November 2026; owner-reported) and continues.')
rep('No departure has been found so far (through EX_115; the latest REVIEWER-DECIDED items were WF1-R3-C05 (EX_080), the register v0.22 correction C01 (EX_099, FIX AND PROCEED), and the optional WF1B-R2-O01 (EX_111) and WF1B-R2-O02 (EX_113), both deferred by the owner).',
    'No departure has been found so far (through EX_131; the latest REVIEWER-DECIDED items were the register v0.22 correction C01 (EX_099, FIX AND PROCEED), the optional WF1B-R2-O01 (EX_111) and WF1B-R2-O02 (EX_113), both deferred by the owner, and EX_131\'s FIX AND PROCEED for the MHUP-1 restore safeguard, inserted as worded in v0.1r5 and recorded in EX_132).')
rep('They travel to `exchange/` in a for-the-record EX message that needs no reply (EX_046, EX_054, EX_057, EX_067, EX_076, EX_086, EX_102), with the narrow diff,',
    'They travel to `exchange/` in a for-the-record EX message that needs no reply (EX_046, EX_054, EX_057, EX_067, EX_076, EX_086, EX_102, EX_122, and for a design EX_132), with the narrow diff,')

# ================================================================ section 2
rep('- **Helpers (other agents):** the owner approved them on 31 October 2026. They block the chat while they run and are killed if the owner posts, so the owner agreed to wait until Claude says it has finished.',
    '- **Helpers (other agents):** the owner approved them on 31 October 2026. They block the chat while they run and are killed if the owner posts, so the owner agreed to wait until Claude says it has finished. A helper\'s model can be chosen per call (for example Opus for a cold read while the chat runs on Fable).\n'
    '- **Model choice (MC-1; owner, 2 November 2026, refined 3 November 2026; register v0.24):** before (a) designing a new subsystem or a major change to one, (b) a statistical design or validity question, (c) the root cause of an unexplained failure or STOP, or (d) a cold-read review of a design before it goes to the reviewer, say "Suggest switching to Fable (High) for this" and wait for the owner\'s "go". Everything else (packaging, task files, install steps, roadmap and reminder updates, explanations, paste blocks, records) goes ahead without asking. You cannot see which model is selected, and you cannot change it yourself (only the owner can, with `/model`), so flag and hold; split a mixed request at the boundary; when a Fable task is finished, say so, so the owner can switch back. **Refinement:** Fable is saved for the hard core (new HIGH design, the core of a HIGH code module, a BLOCKER-level finding, an unexplained STOP), because the owner\'s token allowance may otherwise run out before the end of a week; at each step say which model you recommend (Opus 5.5 or Fable) with a one-line reason; cold-read helpers may run on Opus whatever the chat\'s model.\n'
    '- **The owner\'s risk posture on chat length (3 November 2026):** this chat has already run out of room once (its context was summarised). Keep the handovers current at each milestone rather than at the end, and when the owner asks whether to continue or start a new chat, give a plain recommendation with the reason.')

# ================================================================ section 3
rep('Real weekly forecasting (**the prospective mode**, the owner\'s weekly session MH-1, section 10) starts once the owner declares the pipeline **developed** for the released cohort (GOAL-1); later waves keep adding methods afterwards. Each week: update the results, catch up missed draws in order, score the open forecast, then train on all eligible draws before the next target, predict, freeze and record it before the draw. How R3\'s FINAL mode maps onto this loop is OPEN for the Mode H design (section 10). Method rankings (league tables) are reports per R3 section 17; they never feed forecasts.',
    'Real weekly forecasting (**the prospective mode**, the owner\'s weekly session MH-1) starts once the owner declares the pipeline **developed** for the released cohort (GOAL-1); later waves keep adding methods afterwards. Its design is ratified (MHUP-R, 3 November 2026; ' + DESIGN + '): one command per game runs a small sequencer that alternates a forecasting program and a scoring program one target at a time (forecast N from the draws before it, reveal N, score N, then N+1), then freezes the next draw\'s forecast before its deadline. The weekly session **is** R3\'s FINAL_NEXT_DRAW protocol as amended by the design, and the owner\'s GOAL-1 declaration is R3\'s "explicit FINAL opening" (design 6.7). Before that comes **Mode H**, a precommitted holdout evaluation of every released variant on the ten sealed draws per game, scored once (design section 5). Method rankings (league tables) are reports per R3 section 17; they never feed forecasts.')

# ================================================================ section 4
rep('| `Deferred_Performance_Engineering_Proposal_v0_1.md` |',
    '| `Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r5.md` | `e5fb491ca601fa71793d143871d99c40929d20cdd8398fe92e0c6858c44a5455` | **MHUP-1, ratified 3 November 2026 (MHUP-R):** Mode H (option A), the version-2 master rules, one data kind, the binding and ticket gates, the study manifest and opening record, install and release records, the weekly session, the forecast, witness and score ledgers, the deadline and labels, the updater v0.2, the two packages MHUP-A and MHUP-B, and Appendices A to L (the review tables, citation anchors, gate matrix, event order, witness lifecycle, manifest inventory, classification rule, installation safety, rules amended, oracles). Installed with DOC-11 |\n'
    '| `Direction_for_operational_procedures_v0_2r1.md` | `0aa5967febb817707953b4634937a9a76e2a56e364360cfd1004d10d85c56855` | The owner-ratified operational direction in plain English (DIR-1, 2 November 2026); content-checked by the reviewer; the design and the register prevail where it is looser. Installed with DOC-11 |\n'
    '| `Deferred_Performance_Engineering_Proposal_v0_1.md` |')
rep('- **The register:** the current edition is the authority on every document\'s status, every install and every owner decision; register v0.23 is installed with this file (register v0.22 is `ca955cf23b5681a534e784b4a4852acd2e8d0ccd0484e34150a05c824c0fe56b`).',
    '- **The register:** the current edition is the authority on every document\'s status, every install and every owner decision; register v0.24 is installed with this file (register v0.23 is `7502b75556c56f4c9b91e9022829ee18f05d02591260e87bfe053ec1c79bb6c2`). **Amended by ratification, not edited:** R3 (the push-based timing proof and related clauses), R2-C03, E2R-1 (E2R-R41, R44, 9.1), Architecture section 5C.1 and this file\'s section 5.4 are amended as register v0.24 lists (from the design\'s Appendix K); their next editions fold the changes in, and the register prevails meanwhile.')

# ================================================================ section 5.1
rep('- **The owner will not run `results_master update`**, even to test, **until he separately approves the first update run at the Mode H stage** (an always-review subject); it is gated by `HOLDOUT_OPENED_<GAME>.json`, which is not authorised. Opening the holdout (writing that record) is also a separate owner approval; who or what writes it is designed in Mode H. Running `Run_Results_Updater.bat` with no arguments starts `update` (refused today); never suggest running it bare. The results update after Mode H is still to be designed (section 10; probe finding A1 in section 12.8).',
    '- **The owner will not run `results_master update`**, even to test, **until MHUP-A (with the version-2 reader and the updater v0.2) is installed and he separately approves the first update run** (Approval 2; an always-review subject). Today it is also gated by `HOLDOUT_OPENED_<GAME>.json`, which does not exist. Under the ratified design: Approval 1 freezes the study manifest and writes the opening record (`Method_Mode_H.py open`, design 4.1-4.2); Approval 2 is the first update, which **writes only an `UPDATE` that brings in every holdout draw** (MHUP-D1), after which the updater refuses for that game until its Mode H is sealed (MHUP-B04); every install holds the updater\'s own lock (MHUP-D2). Running `Run_Results_Updater.bat` with no arguments starts `update`; never suggest running it bare (the checklist says so).')
rep('- **Source:** Lotterywest\'s own results-search page on `www.lotterywest.wa.gov.au`, read by an honest, unmodified headless browser with >= 2 s pauses.',
    '- **Source:** Lotterywest\'s own results-search page on `www.lotterywest.wa.gov.au`, read by an honest, unmodified headless browser with >= 2 s pauses. **MHUP-C03 (owner, 3 November 2026):** its published results are official and trusted as they stand; no second-source check of a new draw in production; the updater v0.2 checks the browser\'s final URL is exactly `https://www.lotterywest.wa.gov.au` and has no fallback of any kind (design section 7).')

# ================================================================ section 5.3
rep('- **The owner\'s other decisions in register v0.23 (31 October and 1 November 2026):**',
    '- **The owner\'s decisions in register v0.24 (2 and 3 November 2026; the register has each in full, the design has the detail):** the stock-take positions ST-1 to ST-5 (frozen records: forecasts never changed, scores kept with new scoring runs beside them, league tables as dated views; retired revisions archived and indexed; three labels PROSPECTIVE, CATCH-UP and development evidence; nothing scored twice; an unaccepted draw left open; the status block; the previous chat retired; the planning target of about 13 to 15 November 2026); DIR-1 (the direction document); MC-1 (model choice, section 2) and KISS-1 (the simplicity review after full implementation, only when asked); and for MHUP-1: **MHUP-Q1** option A (Mode H a precommitted holdout evaluation with N-1 isolation, not pre-draw forecasting), **MHUP-Q10** (ER-2r1 extended to E_1 revision 3), **MHUP-B02** (MH-1\'s per-target order exactly, with a sequencer), **MHUP-C03** (Lotterywest trusted; exact origin), **MHUP-B04** (the updater refuses while a game\'s holdout is open and unsealed, and while a session lock exists; the environment frozen to the installed files), **MHUP-Q11** (official runs only through tickets; hand-typed runs an unofficial diagnostic route), **MHUP-D1** (the first-update admission), **MHUP-D2** (an install holds the updater\'s lock), **MHUP-D3** (the POC path, the report tool and the walk-forward driver are not launched during an install; the stated residual risks accepted), and **MHUP-R**, the design ratified as a whole with the recommendations for Q2-Q6, Q8 and Q9. **Q7 is OPEN** (whether the display restriction on holdout draws is relaxed after Mode H; until decided, nothing changes).\n'
    '- **The owner\'s other decisions in register v0.23 (31 October and 1 November 2026):**')

# ================================================================ section 5.4
rep('- **Option F, the single launch interface:** `Run_Coordinator.bat` -> Python coordinator -> `Run_Experiment.bat` per experiment -> method `.py`; manual: `Run_Experiment.bat` -> method (including `Method_Contract_Runner.py`). No second production launcher. ERR-R2-02 / Option F has provisional production acceptance until owner-run P1/P2 gates pass.',
    '- **Option F, the single launch interface:** `Run_Coordinator.bat` -> Python coordinator -> `Run_Experiment.bat` per experiment -> method `.py`; manual: `Run_Experiment.bat` -> method (including `Method_Contract_Runner.py`). Method code runs only through `Run_Experiment.bat`. **Amended by MHUP-R (register v0.24):** the evaluator and session launchers are `Run_Method_Rankings.bat` (WF-1B), `Run_Evaluation.bat` (MHUP-A) and `Run_Weekly_Session.bat` (MHUP-B); the weekly orchestrator is a sequencer, not a coordinator (no supervision, no termination, no PID use, no orphan writes); `src/package_tools/process_check.py` lists processes but acts on none. ERR-R2-02 / Option F has provisional production acceptance until owner-run P1/P2 gates pass.')
rep('- **Three switches stay False:** `ENABLE_PROCESS_TERMINATION`, `ENABLE_SCIENTIFIC_COORDINATION`, `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE`. The fourth, `ENABLE_CONTRACT_REAL_DEVELOPMENT`, is True since WF-1A (WF1-3, `0d98706`). No CLI override. Only the owner flips one, after reviewed tests.',
    '- **Three switches stay False:** `ENABLE_PROCESS_TERMINATION`, `ENABLE_SCIENTIFIC_COORDINATION`, `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE`. The fourth, `ENABLE_CONTRACT_REAL_DEVELOPMENT`, is True since WF-1A (WF1-3, `0d98706`). No CLI override. Only the owner flips one, after reviewed tests. **MHUP-1 adds no switch:** the new real modes (`REAL_HOLDOUT`, `CATCH_UP`, `FINAL_NEXT_DRAW`) are governed by the owner\'s create-only records (the opening record, the developed record), the tickets and the binding gates (design 3.4, 5.1).')

rep("a full freeze list of his venv is not recorded (an open item for R3-T50's no-upgrade rule in Mode H).",
    "a full freeze list of his venv is not recorded; for Mode H the design freezes the installed files themselves (interpreter files and pip's RECORD hashes; design 4.1, MHUP-B04).")
rep('rulebook v0.3 (in the snapshot) adds them to rule 7', 'rulebook v0.3 (installed at `7bb0bfd`) adds them to rule 7')
rep('- **Reference figures** (fair-draw model, context only, never a veto):',
    '- **The results updater** (`src/results_master_v0_1.py`, checked for the MHUP-1 design): it fetches through a browser driver (`BrowserFetcher`, line 540; `self.driver.get(url)`, line 567), so it sees only the final URL after redirects, never a status code; it takes its own lock `source_data/.results_master.lock` with a create-exclusive open (lines 657-663) at line 686, before the fetch, so any existing lock file stops it (the install barrier of MHUP-D2 uses this); its `holdout_opened` check accepts extra JSON fields; `FIRST_QUARANTINED_DRAW` (line 60) gives the first holdout draw of each game. Its `--self-test` works in temporary folders.\n'
    '- **Byte-code caches:** with `PYTHONPYCACHEPREFIX` set, Python reads and writes cached byte-code only under that prefix, never in the `__pycache__/` folders beside the sources; `-B` (or `PYTHONDONTWRITEBYTECODE=1`) stops the writes; `-I` ignores both environment variables, so an isolated run needs `-B -X pycache_prefix=...` given directly. A sourceless `.pyc` outside `__pycache__/` is still importable. (Reproduced on CPython by the cold-read helper, 3 November 2026; design 4.1.)\n'
    '- **Reference figures** (fair-draw model, context only, never a veto):')

# ================================================================ section 7
rep('Document-only installs: `be18548` (DOC-1), `ee62eb6` (DOC-3), `040f80e` (DOC-4), `b846519` (register v0.12), `337b5b2` (DOC-6: H-1 v1r4, H-2 v1r5, register v0.14; four duplicate zips removed at `f9de54a`), `8defe9d` (DOC-7: H-1 v1r5, H-2 v1r6, register v0.17), `03f7da4` (DOC-8: H-1 v1r6, H-2 v1r7, register v0.20), `2b1e7e3` (DOC-9: register v0.22). The snapshot installs this file with register v0.23; that commit cannot name itself, so Claude records it in the post-push check and the next register.',
    'Document-only installs: `be18548` (DOC-1), `ee62eb6` (DOC-3), `040f80e` (DOC-4), `b846519` (register v0.12), `337b5b2` (DOC-6: H-1 v1r4, H-2 v1r5, register v0.14; four duplicate zips removed at `f9de54a`), `8defe9d` (DOC-7: H-1 v1r5, H-2 v1r6, register v0.17), `03f7da4` (DOC-8: H-1 v1r6, H-2 v1r7, register v0.20), `2b1e7e3` (DOC-9: register v0.22), `7bb0bfd` (DOC-10, the snapshot: register v0.23, Architecture v0.9, H-1 v1r7, H-2 v1r8 and the rest; verified, 30 of 30 rows). DOC-11 installs this file with register v0.24, the MHUP-1 design and the direction document; that commit cannot name itself, so Claude records it in the post-push check and register v0.25. The owner\'s own commits since: the settings deny line `905ecee`, and the stock-take and direction documents `f47ce14` to `6de0d99`.')

# ================================================================ section 8.6
rep('- **Where:** `CLAUDE_CODE_WORKING_FOLDER_TREE/` (rulebook `CLAUDE.md` v0.3 from the snapshot (v0.2 before it);',
    '- **Where:** `CLAUDE_CODE_WORKING_FOLDER_TREE/` (rulebook `CLAUDE.md` v0.3, installed with the snapshot at `7bb0bfd`; MHUP-A and MHUP-B each add their new tools to rule 7, with matching deny entries in `.claude/settings.json` that the owner edits;')
rep('- **Before writing any task file:** check that `.claude/settings.json` holds the owner\'s deny entry for the report tool (`Bash(*Method_Rankings_Report*--game*)`, added by the owner after the snapshot install; if absent, ask him), then run `check_task_vs_deny.py` on the task file.',
    '- **Before writing any task file:** check that `.claude/settings.json` holds the owner\'s deny entry for the report tool (`Bash(*Method_Rankings_Report*--game*)`, committed by the owner at `905ecee`; if absent, ask him), and, once MHUP-A or MHUP-B is installed, the deny entries for their tools; then run `check_task_vs_deny.py` on the task file. The next rehearsals are T016 (MHUP-A) and T017 (MHUP-B).')

# ================================================================ section 8.7
rep('**From the snapshot on, the whole working tool set is also in `exchange/CLAUDE_WEB_TOOLS/`** (section 12.2). A new chat can rebuild a package from these and check it against the recorded hashes.',
    '**From the snapshot on, the whole working tool set is also in `exchange/CLAUDE_WEB_TOOLS/`** (section 12.2). For the MHUP-1 design: every edition is in its EX folder (`EX_124_Claude/` v0.1r1, `EX_126_Claude/` v0.1r2, `EX_128_Claude/` v0.1r3, `EX_130_Claude/` v0.1r4, `EX_132_Claude/` v0.1r5), each with the cold-read reports, the draft the helper read and the diffs; the design was built as section files spliced into a copy of the previous edition, so untouched sections stayed byte-identical. For DOC-11: `exchange/CLAUDE_WEB_TOOLS/doc11/` (the register and handover builders, the package builder and the rehearsal script). A new chat can rebuild a package from these and check it against the recorded hashes.')

# ================================================================ section 8.8 (lessons added at the end)
rep('- **An exact method can be correct and still unusably slow:** WF-1B\'s exact Clopper-Pearson took over an hour per real report; full-size profiling on invented data found it in minutes (PERF-1). Profile at full size before the owner\'s first real run.',
    '- **An exact method can be correct and still unusably slow:** WF-1B\'s exact Clopper-Pearson took over an hour per real report; full-size profiling on invented data found it in minutes (PERF-1). Profile at full size before the owner\'s first real run.\n'
    '- **A claim the record repeats is still checked against the code** (MHUP-1): "no released method uses its target\'s draw number" was repeated through the stock-take until a cold read found the target in every tie-break key and view digest; the record was corrected (register v0.24).\n'
    '- **A cold read by a fresh helper before every review round pays for itself** (MHUP-1, five rounds): it found that E_1 revision 2 refuses every new mode; a later-released method could never pass the holdout draws; partial forecast sets would be orphaned after a clean session end; the install preflight ran a tool not yet installed; a nested launch would create the "never-existing" byte-code folder (reproduced on CPython); the updater lock was released before the release record. Give the helper the reviewer\'s findings, the old and new editions and the diff, ask for scenario traces, and send it a recheck after the fixes; run it on Opus to save Fable.\n'
    '- **State machines need every exit enumerated** (EX_127 B01-B03, EX_129 C01): crash at each step, resume under the same identity versus a successor, roster changes between start and finish, a clock-based rule judged twice. Persist each judgement as a record (tickets, `SET_STARTED`) instead of recomputing it, and write the event-order table before the prose.\n'
    '- **Check what an existing tool really does before relying on it** (EX_129 B02): the updater\'s own create-exclusive lock (`results_master_v0_1.py` lines 657-663, taken at line 686 before the fetch) became the install\'s barrier with no code change, and its browser-driven fetch (line 567) meant a redirect could only be refused after the fact.\n'
    '- **An extension of an owner decision found during the work goes back to the owner before it is recorded as decided** (MHUP-D3 was extended the same day only after the owner said yes). Mark it proposed until then.\n'
    '- **A FIX AND PROCEED is inserted exactly as the reviewer worded it**, with the diff, in a for-the-record EX message (EX_132).\n'
    '- **The owner sometimes edits `doc/` himself** (`6de0d99` removed the direction v0.2 copy): report what you see, never touch `doc/`, and fold the change into the next document package.')

# ================================================================ section 9
rep('4. **Release** (a separate small reviewed package; the owner\'s two actions, as REL-1 did for 39 variants): delete the flag; append a `SUPPORTED` entry for the same declaration. Then the method can run through the contract runner.',
    '4. **Release** (a separate small reviewed package; the owner\'s two actions, as REL-1 did for 39 variants): delete the flag; append a `SUPPORTED` entry for the same declaration. Then the method can run through the contract runner. **From MHUP-A on** every install also writes an install record (code arrival) and every release a release record, after COMMITTED PASS, as a second commit (design 4.3, Appendix J); a variant\'s release date is its release record\'s local date, which decides whether its catch-up forecasts count as CATCH-UP or as development evidence.')
rep('5. **Real data:** with `ENABLE_CONTRACT_REAL_DEVELOPMENT` on (WF1-3), a released method joins the next walk-forward batch the owner authorises; a batch holds the full cohort (ER-6), so a new method means a new batch per game, then a report. Preregistration, Mode H and FINAL stay separate gates.',
    '5. **Real data:** with `ENABLE_CONTRACT_REAL_DEVELOPMENT` on (WF1-3), a released method joins the next walk-forward batch the owner authorises; a batch holds the full cohort (ER-6), so a new method means a new batch per game, then a report. **Once the weekly session runs** (MHUP-B), a newly released variant joins the session roster at its next session and is first forecast at the first target frozen after its release; it never forecasts a holdout draw or an earlier closed target; its back-history over post-holdout draws, if wanted, is a separately identified development batch (design 6.3; roadmap 21b). A roster-changing install is refused while a weekly forecast set is unfinished (design Appendix J). Preregistration stays a separate gate.')

# ================================================================ section 10 (rewritten)
rep_between('## 10. Next work, in order (planned; the owner decides each step)', '---\n\n## 11. Gates that stay closed',
"""## 10. Next work, in order (planned; the owner decides each step)

1. **Done since v1r7:** DOC-10 installed (`7bb0bfd`) and the owner's deny line (`905ecee`); the chat switch (HO-1), the new chat's takeover PASS, and the previous chat retired (ST-4); the stock-take and its ratification (ST-1 to ST-5); the direction document (RECHECK, then PASS; DIR-1); the MHUP-1 design in five editions with five cold reads and four review rounds (EX_123 to EX_132), the owner's decisions during them, and the ratification of v0.1r5 (MHUP-R). No code was installed and nothing ran on real data.
2. **Now: DOC-11 and the staged Claude handover (HO-2, owner, 3 November 2026).** DOC-11 is Claude's handover package: this file and its introductory blurb, register v0.24, the design and the direction document in `doc/`, and six review copies. The steps: (1) the package is completed; (1.1) the existing ChatGPT reviewer examines the complete package for completeness, accuracy, consistency with the register and the design, missing obligations and risks of misunderstanding (EX_133; reply EX_134), and every problem it finds is resolved; the owner then ratifies and installs DOC-11; (2) the owner starts the replacement Claude chat, which reads and verifies before anything else (section 0, item 4); (3) the reviewer assesses the new chat's first replies and suggests targeted questions, which the new chat answers before seeing the reviewer's answers; material discrepancies are resolved; (4) normal work resumes only after that verification and the owner's authorisation; (5) a ChatGPT reviewer handover is considered only later, after the new Claude chat has shown reliable continuity. H-2 v1r8 stays in force meanwhile; no ChatGPT takeover is prepared. **The owner has paused the code until the documents are updated** (3 November 2026).
3. **Next, towards next-draw forecasts** (ST-5: Mode H and the weekly session installed by about 13 to 15 November 2026, the first forecasts frozen before a draw being Oz Lotto 1709 on Tuesday 17 November and Powerball 1592 on Thursday 19 November; FB-1: slip rather than rush):
   - **MHUP-A** (HIGH; design sections 2 to 5 and 7; model: Fable for the core, Opus for packaging): E_1 revision 3 (under the extended ER-2r1); the version-2 master rules and `master_versions.py`; one data kind; the binding, ticket and diagnostic gates; the barrier; the study manifest with its closure and installed-file environment freeze; `Method_Mode_H.py` (`manifest`, `open`, `advance`, `declare-developed`); the install- and release-record tool and the baseline release record; the Mode H batch kind with tickets and lifecycle markers; the freeze-before-outcome rule; the Mode H families, report ceiling and texts; `Run_Evaluation.bat`; `Run_Experiment.bat`'s byte-code lines; `process_check.py`; the updater v0.2 (four additions only); the `REAL_HOLDOUT` row unreserved; the rulebook's rule 7 additions (and the owner's deny entries); R-007, R-008 and R-010 folded in. Code review R-2 with EX_131 section 4's demonstrations; Claude Code rehearsal T016; the owner's install by Appendix J's 19 steps (two commits). At its approval, the owner chooses whether to rerun the Windows POC suite or accept it unrun.
   - **MHUP-B** (HIGH; design section 6 and section 7's checklist): `CATCH_UP`, `FINAL_NEXT_DRAW` unreserved, `Method_Weekly_Forecast.py`, `Method_Weekly_Score.py`, the orchestrator, `Run_Weekly_Session.bat`, the session records, attempts ledgers and locks, the three ledgers, the deadline, `LATE_PRE_DRAW`, the league table, the owner's one-page checklist; rehearsal T017. Installed before Approval 1, or else only after the Mode H score is sealed (design 4.4).
   - **Then the owner's approvals, per game, each separately** (design 4.4): Q7's decision before Approval 2; Approval 1 (freeze the study manifest, write the opening record); Approval 2 (the first update, after the updater's offline self-test under Python 3.15); Approval 3 (the Mode H batch); Approval 4 (the Mode H score and report, then the seal). Then the owner's GOAL-1 decision (the developed record) and the first weekly session.
   - **Register v0.25** records all of it.
4. **WF-1C** (WORKERS-1; roadmap item 10d), after MHUP-1 (ORD-1), carrying EX_101's four obligations and EX_105's B01 and C02-C05 in full (EX_107).
5. **Then, in the owner's order:** the efficiency items after WF-1C (roadmap 21b: the cross-batch report reusing frozen records, the retired index, a later method's back-history batch); wave 3 (E_27, E_45 = Method B, E_26, E_28); the NL-means discussion (R-002); waves 4 to 11 (4 E_5, E_11, E_15, E_14, then E_13, E_12 and E_16 each in its own package; 5 E_37, E_33, E_35, E_34, E_39, E_36, E_38, E_40; 6 E_23, E_25, E_20, E_21, E_22, E_24; 7 E_32, E_29, E_30, E_31; 8 E_41, E_42, E_43, E_44, E_46, E_47; 9 machine learning E_49-E_53, with a dependency change; 10 E_57, E_60, E_58, E_59, E_61, E_62; 11 E_54, E_48); the ensembles last; KISS-1 when the owner asks (R-014); the final performance study only when the owner activates it (R-006; roadmap item 22).
6. **Method A's diagnostics A1-A5** (W2-3): a separate package after WF-1; they need the seed policy (approved) and a diagnostic report design.
7. **Coordinated contract runs** (D2-1), when the owner wants many methods run together.
8. **Still permission-gated, each separately:** each walk-forward batch and report run; walk-forward preregistration; Windows lifecycle and destructive gates (P2 closure, ERR-R2-02 / Option F final acceptance); allowlist entries; the in-sample engine (R3 17.13 stage 3); Approvals 1 to 4 and the developed record; every weekly session; any master update.
9. **Future actions with their timing** are listed in register v0.24 ("Future actions recorded"): keep that list and `exchange/OWNER_REMINDERS.md` in step, and raise each when it falls due (the next editions of R3, E2R-1 and Architecture; the documents to amend after Q7; the rulebook and deny additions inside each package).
10. **Housekeeping, owner's choice:** later, delete `venv.bak` and Python 3.14; OPEN-N2; the duplicate exploration note in `doc/`; the old EX copies in `review/` (R-003).

**Genuinely OPEN questions** (do not disguise as decided): Q7 (the display rule after Mode H); walk-forward preregistration; E_54 feed timing; each remaining `FORMULA_OPEN` method's formula; E_63 and later identities; scientific allowlist activation; whether to scope the optional oracle prototypes (agreed position 10.3); WF-1C's open choices (the 60-worker cap, memory floor, WB-3/WB-4).

""")

# ================================================================ section 11
rep('This handover authorises nothing. In particular: no Windows lifecycle or destructive test; no real-data batch or report run without the owner\'s authorisation of that run; no holdout access; no Mode H or FINAL; no process termination; no switch change; no allowlist entry; no master update;',
    'This handover authorises nothing, and neither does the ratified MHUP-1 design. In particular: no Windows lifecycle or destructive test; no real-data batch or report run without the owner\'s authorisation of that run; no holdout access, opening record or study manifest; no Mode H, weekly session or FINAL; no process termination; no switch change; no allowlist entry; no master update, and no updater run of any kind before MHUP-A is installed and the first update is separately approved;')

# ================================================================ section 12.1
rep('- Numbers are shared and increasing; check the highest committed number first. The snapshot\'s review request is EX_116 and the reviewer\'s reply EX_117; after that, check the highest committed number before choosing the next.',
    '- Numbers are shared and increasing; check the highest committed number first. At this edition the last committed number is EX_132; the Step 1.1 review of the Claude handover package is EX_133 and the reviewer\'s reply EX_134. Always check the highest committed number before choosing the next.')

# ================================================================ section 12.2
rep('The workspace paths inside these scripts are the previous chat\'s (for example `/home/claude/work/...`; the snapshot tools in `snapshot/` hard-code `/home/claude/work/snap/`); change them at the top of each script before use.',
    'The workspace paths inside these scripts are the previous chat\'s (for example `/home/claude/work/...`; the snapshot tools in `snapshot/` hard-code `/home/claude/work/snap/`); change them at the top of each script before use. **`doc11/`** (this chat, 3 November 2026) holds DOC-11\'s builders: `make_register_v24.py` with `reg24_section.md`, `make_h1_v1r8.py`, the H-1 v1r8 blurb, `build_doc11.py` and `e2e_doc11.sh`; they take their paths as arguments or from the top of the script. The MHUP-1 design tools (the section files and the zip script) are in the EX folders named in section 8.7; the zip tool is `exchange/EX_019_Claude/make_zip.py` (a copy is in `doc11/`).')

# ================================================================ section 12.8 (rewritten)
rep_between('### 12.8 Open items at the snapshot', '### 12.9 The first hour in a new chat',
"""### 12.8 Open items at DOC-11 (3 November 2026)

- **The owner's goal and plan:** next-draw forecasts through MHUP-1 (section 10, item 3; ST-5 and FB-1). The design is ratified; the code is paused until DOC-11 is installed.
- **Waiting on the reviewer:** the Step 1.1 review of the complete Claude handover package (EX_133; reply EX_134), then, after the switch, its assessment of the new chat's first replies (HO-2).
- **The ChatGPT reviewer handover:** not now (HO-2). H-2 v1r8 stays in force; its checkpoint facts (sections 0 and 6) are out of date, and register v0.24 prevails. A new H-2 edition is prepared only when the owner decides on a reviewer handover, after this Claude handover has proved itself.
- **Waiting on the owner:** ratifying and installing DOC-11; confirming the backup of `results/` and `source_data/` (asked 2 November 2026); later, Q7 before Approval 2, and the Windows POC-suite choice at MHUP-A's approval (register v0.24, "Future actions recorded").
- **The reminders** (`exchange/OWNER_REMINDERS.md`): R-001 the owner's Methods A and B (A installed as E_17's log-age variant; B is E_45 in wave 3); R-002 the NL-means discussion after wave 3; R-003 optional tidy-up of old EX copies in `review/`; R-004, R-005, R-009, R-011 DONE; R-006 the deferred performance study (FINAL, inactive); R-007 and R-010 (optional; folded into MHUP-A); R-008 (the verifier's wording; folded into MHUP-A); R-012 the cold-read probe findings (the document ones settled by DOC-10, A5 by TSC-1, and A1-A3, A6-A8 and A11 settled by the MHUP-1 design; the WF-1C ones still carried); R-013 the direction document in `doc/` (closed by DOC-11); R-014 the KISS review (KISS-1; only when the owner asks); R-015 the owner's choices still to come (Q7 before Approval 2; the Windows POC suite and the backup at MHUP-A's approval); R-016 the staged handover and the later ChatGPT reviewer handover (both added 3 November 2026, in `exchange/`).
- **The probe findings, where they landed:** A1 (version-1-only readers) -> design section 3; A2 (the opening record) -> 4.2; A3 (holdout added with later draws; the store) -> 4.4, 4.5 (combined master, Q2); A6 (single source) -> MHUP-C03, section 7; A7 (procedures: accepting a version, a stale lock, an interrupted update, grabs) -> section 7 and the checklist; A8 (the update window) -> section 7; A9 (Python 3.15) -> the self-test before Approval 2; A11 (R3 7.6's independent outcome ledger) -> the score ledger's outcome pins (6.6). B4, B7, B8, B10 and B11 stay with WF-1C or the performance study.
- **WF-1C's obligations:** EX_101's four (memory headroom, which bytes must match across worker counts, failure semantics, the default on odd or unknown processor counts) and EX_105's B01 (atomic admission, no prefetch, fail closed on parent loss, no kill) and C02-C05 in full (EX_107).
- **The R-2 obligations already set for MHUP-A and MHUP-B** (EX_131 section 4): synthetic demonstrations of the first-update admission, the old and new updater lock, failure-state restoration, the unfinished-set refusal, direct and nested byte-code discipline, the two-commit release order, and the stated Windows rehearsals and owner choices. The design's Appendix L lists every oracle and the only existing tests that change.

""")

# ================================================================ section 12.9
rep('4. Read the newest EX messages and the roadmap; list anything in flight (an unanswered EX message, a task report not yet read, an install not yet verified).',
    '4. Read the newest EX messages and the roadmap; list anything in flight (an unanswered EX message, a task report not yet read, an install not yet verified). At this edition: the staged takeover itself (section 0, item 4); then, after the owner\'s authorisation, MHUP-A.')

# ================================================================ Appendix A
rep('| H-2 v1r7 (current reviewer handover until v1r8 is installed) | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r7.md`, `a59ab8504d0d63d852d66efcc9491a05d3329656eb5164eef682df57da60ec38` |\n| H-1 v1r6 (predecessor) |',
    '| H-1 v1r7 (predecessor) | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r7.md`, `b51f63792dde7f7d6c0c9e01ea6cecc5b5a12038ba748b91647738273ebc29fb`; its blurb `bc46c07a1705aa49738ba6b8d8797f46df40cbc7996e4ba22a25eaefdab73240` |\n'
    '| H-2 v1r8 (the reviewer handover in force; a new edition only with a later reviewer handover, HO-2) | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8.md`, `4e2737c28a69ab73577fa6c39c87c04518e42ed1be47f240295e80802774b956`; its blurb `17633e4ec5413d12ed3c2909819b9f899a156af22631a31ee3e1b6f145ea0d2a` |\n'
    '| H-2 v1r7 | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r7.md`, `a59ab8504d0d63d852d66efcc9491a05d3329656eb5164eef682df57da60ec38` |\n| H-1 v1r6 |')
rep('| Register v0.23 (installed with this file) | `doc/RATIFICATION_REGISTER_v0_23.md`, `7502b75556c56f4c9b91e9022829ee18f05d02591260e87bfe053ec1c79bb6c2` |',
    '| Register v0.24 and this file with its blurb (installed together with DOC-11) | identified by DOC-11\'s manifest, `review/DOC11_Claude_Handover_v1/INSTALL_MANIFEST_SHA256.txt` |\n'
    '| The MHUP-1 design v0.1r5 (ratified 3 November 2026; installed with DOC-11) | `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r5.md`, `e5fb491ca601fa71793d143871d99c40929d20cdd8398fe92e0c6858c44a5455`; EX_132 zip `cec02f6b60ade13ae4fcec4610083fe233f817eceba776bf8e5fabb07972a9de` |\n'
    '| The direction document v0.2r1 (installed with DOC-11) | `doc/Direction_for_operational_procedures_v0_2r1.md`, LF `0aa5967febb817707953b4634937a9a76e2a56e364360cfd1004d10d85c56855` (its CRLF working copy `exchange/Direction_for_operational_procedures_v0_2r1.md`, `be409f50d957483ae310b1ba17b33ff68fade5a155d1ab2f1c5651b26740a96b`) |\n'
    '| The stock-take record | `exchange/STOCKTAKE_2026_11_02_v0_8.md`, as stored `f97c33dd911124383c74962e469a1d55b36cd2640848cac92f7bb2cacce6ae33` |\n'
    '| Register v0.23 | `doc/RATIFICATION_REGISTER_v0_23.md`, `7502b75556c56f4c9b91e9022829ee18f05d02591260e87bfe053ec1c79bb6c2` |')
rep('| H-2 v1r8 (installed with this file) | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8.md`, `4e2737c28a69ab73577fa6c39c87c04518e42ed1be47f240295e80802774b956`; its blurb `17633e4ec5413d12ed3c2909819b9f899a156af22631a31ee3e1b6f145ea0d2a` |\n', '')
rep('| Holdout exposure record v0.3 (installed with this file) |', '| Holdout exposure record v0.3 (installed at `7bb0bfd`) |')
rep('| Architecture v0.9 (installed with this file) |', '| Architecture v0.9 (installed at `7bb0bfd`; section 5C.1 amended by MHUP-R) |')
rep('| This file (H-1 v1r7) | identified by the DOC-10 manifest, `review/DOC10_Snapshot_v1/INSTALL_MANIFEST_SHA256.txt` |\n', '')
rep('| Claude Code rulebook v0.3 (installed with this file) |', '| Claude Code rulebook v0.3 (installed at `7bb0bfd`) |')

# ================================================================ Appendix B (rewritten)
rep_between('## Appendix B. Changes in v1r7', '*End of H-1.*',
"""## Appendix B. Changes in v1r8

v1r8 refreshes v1r7 in place after the MHUP-1 design's ratification (owner, 3 November 2026: a full working edition that points to register v0.24 and the design). It changes no rule; where it states a rule, the ratified documents and the register prevail. Nothing in v1r7 was dropped except what is superseded below. v1r7's own change list stays in v1r7.

1. **Header and section 0:** v1r8, the baseline (code unchanged since PERF-1; DOC-10 and the records through EX_132); the reading list adds register v0.24's newest section, the design and the direction document; DOC-11's manifest.
2. **Section 0:** the staged takeover (HO-2) as item 4. **Section 1:** the reviewer chat through EX_131 and the takeover PASS; oversight through EX_131 (EX_131's FIX AND PROCEED); for-the-record EX_122 and EX_132.
3. **Section 2:** helpers' model per call; MC-1 (model choice with the 3 November refinement); the owner's risk posture on chat length. Section 2A is unchanged, byte for byte (the builder asserts the whole section).
4. **Section 3:** the prospective mode as designed; FINAL decided (Q8). **Section 6:** two verified facts (the updater; byte-code caches).
5. **Section 4:** the design and the direction document added; the register pointer moves to v0.24; the documents amended by ratification.
6. **Section 5:** the updater rules under the design (MHUP-A first; Approvals 1 and 2; D1, B04, D2); the trusted source (C03); the register v0.24 decisions summarised; Option F's launchers and the no-new-switch rule as amended.
7. **Section 7:** DOC-10 and DOC-11 in the install list; the owner's commits.
8. **Section 8:** the rulebook v0.3 installed and the new tools' rule 7 additions; T016 and T017; the MHUP-1 and DOC-11 rebuild records; seven lessons added.
9. **Section 9:** install and release records; a new variant's place in the weekly roster; the roster-change refusal.
10. **Section 10:** rewritten: done since v1r7, DOC-11, MHUP-A, MHUP-B, the approvals, then WF-1C and the waves; the future-actions pointer.
11. **Section 11:** the design authorises nothing; no updater before MHUP-A.
12. **Section 12:** the EX numbers at this edition; `doc11/`; section 12.8 rewritten as the open items at DOC-11 (including where each probe finding landed); section 12.9's in-flight items.
13. **Appendix A:** current identities (H-1 v1r7 the predecessor; H-2 v1r8 still in force; the design; the direction document; the stock-take record; register v0.23).

""")

# ---- cold-read takeover test fixes (3 Nov 2026), applied after the main edits; each old string must occur once
FIX = [
 ("in particular, check that DOC-11 is installed,",
  "if this file's or register v0.24's status line still reads CANDIDATE, stop and ask the owner which handover is in force; in particular, check that DOC-11 is installed,"),
 ("Material discrepancies are resolved before the takeover counts as successful, and normal work resumes only after the owner authorises it.",
  "Material discrepancies are resolved before the takeover counts as successful, and normal work resumes only after the owner authorises it. **Until then:** read, check hashes and write; build, run and commit nothing: no draft or speculative code, task file or package in your workspace, no test suite run (section 12.9's suite and workspace steps wait for the owner's authorisation), and no commit or push, even in `exchange/`. **Keeping your answers blind:** the owner relays the reviewer's questions on their own (a paste, or an EX file holding only the questions); the reviewer's assessment and suggested answers stay with the owner until you have sent your answers, and only then come to you. Once the owner authorises normal work, you record every takeover exchange in `exchange/` under the next free EX numbers, as section 1.6 requires. The outgoing Claude chat stops committing once you start."),
 ("**The owner has paused the code until the documents are updated** (3 November 2026).",
  "**The code is paused** (owner, 3 November 2026) until the staged takeover is verified and the owner explicitly authorises normal work (section 0, item 4); DOC-11's install alone does not lift the pause. The planning dates of ST-5 have not been moved by the owner; HO-2 adds a review round and a takeover check, and FB-1 applies (slip rather than rush)."),
 ("The design is ratified; the code is paused until DOC-11 is installed.",
  "The design is ratified; the code is paused until the staged takeover is verified and the owner authorises normal work (section 0, item 4)."),
 ("the owner's install by Appendix J's 19 steps (two commits).", "the owner's install by Appendix J's steps 0 to 19 (two commits)."),
 ("| `src/Powerball_Experiment_Coordinator.py` | The coordinator; 11 protected functions AST-identical to v0.6 (`2e23d550...`) |",
  "| `src/Powerball_Experiment_Coordinator.py` | The coordinator; 11 protected functions AST-identical to v0.6 (`2e23d550...` is the SHA-256 of the v0.6 fixture file, not of the current coordinator) |"),
 ("At this edition the last committed number is EX_132; the Step 1.1 review of the Claude handover package is EX_133 and the reviewer's reply EX_134.",
  "At this edition the last committed number is EX_132; the Step 1.1 review of the Claude handover package is planned as EX_133 with the reviewer's reply EX_134 (EX_132 offered EX_133 for an optional reply; if that number was used, the request took the next free one)."),
 ("A speculative candidate built alongside the design is fine,",
  "A speculative candidate built alongside the design is fine (but never during a takeover: section 0, item 4),"),
 ("**DOC-10 (the snapshot) has one** (`VERIFY_DOC10_INSTALL.py`, pre/post/committed),",
  "**DOC-10 (the snapshot) and DOC-11 have one each** (`VERIFY_DOC10_INSTALL.py`, `VERIFY_DOC11_INSTALL.py`; pre/post/committed),"),
]
FIX += [
 ("and that the hashes in sections 4 and 7 and Appendix A match `git show HEAD:<path> | sha256sum`.\n2. Read,",
  "and that the file hashes in sections 4 and 7 and Appendix A match `git show HEAD:<path> | sha256sum`, except the two master hashes in section 7.5 (never open `source_data/`) and the computed E_1 digests in section 7.3 (run outputs, not files).\n2. Read,"),
 ("1. Clone, read section 0's list, and check the hashes in sections 4 and 7 and Appendix A.",
  "1. Clone, read section 0's list, and check the file hashes in sections 4 and 7 and Appendix A (not the master hashes of 7.5 or the computed digests of 7.3; section 0, item 1)."),
 ("2. Read `exchange/CLAUDE_WEB_TOOLS/README.md`; set up a workspace:",
  "2. **After the owner has authorised normal work (section 0, item 4), not before:** read `exchange/CLAUDE_WEB_TOOLS/README.md`; set up a workspace:"),
 ("Installed with DOC-11 |\n| `Direction_for_operational_procedures_v0_2r1.md`",
  "Installed with DOC-11, byte-identical to EX_132's member, so its own header, section 1 and section 8 table still read as before ratification; register v0.24 records the ratification |\n| `Direction_for_operational_procedures_v0_2r1.md`"),
 ("the design and the register prevail where it is looser. Installed with DOC-11 |",
  "the design and the register prevail where it is looser or differs (register v0.24 lists four places: its sections 4, 5 step 4, 7 and 11). Installed with DOC-11 |"),
 ("| H-2 v1r8 (the reviewer handover in force; a new edition only with a later reviewer handover, HO-2) |",
  "| H-2 v1r8 (the reviewer handover in force; a new edition only with a later reviewer handover, HO-2; its \"DRAFT\" title and footer are historical, the register's status prevails) |"),
 ("| Committed coordinator v0.6 (AST anchor) | `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b` (also",
  "| Committed coordinator v0.6 (AST anchor; the SHA-256 of the v0.6 fixture file, not of today's coordinator) | `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b` (also"),
]
for _o, _n in FIX:
    rep(_o, _n)

for old, new in E:
    n = t.count(old)
    assert n == 1, (n, old[:90])
    assert all(ord(c) < 128 for c in new), old[:60]
    t = t.replace(old, new)
assert section(t, '### 2A. The owner\'s foundational points', '---\n\n## 3.') == S2A
assert '\r' not in t and t.endswith('\n') and not t.endswith('\n\n')
open(out, 'wb').write(t.encode('ascii'))
print(out, hashlib.sha256(t.encode()).hexdigest(), len(E), 'edits', len(t.encode()), 'bytes')
