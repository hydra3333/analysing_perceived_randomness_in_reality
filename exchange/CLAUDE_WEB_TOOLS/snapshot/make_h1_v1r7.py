"""H-1 v1r7 from the installed H-1 v1r6 by counted edits (Claude, 1 Nov 2026).

v1r7 is the handover for the planned chat switch (owner, 1 November 2026): a new Claude chat takes over primary
design and coding after the snapshot, without this chat's workspace. It brings every section up to the snapshot
and adds section 12, "Working knowledge" (the work cycle's mechanics, the tools, the workspace's traps, the owner's
preferences, the lessons, the open items and a first-hour checklist). It changes no rule. Section 2A (the owner's
foundational points) must stay byte-identical; the builder asserts the whole section.
Placeholders `[[FILL: ...]]` are filled at finalisation (see NOTES.md); the builder lists them.
Usage: python3 -I make_h1_v1r7.py H1_v1r6 OUT
"""
import hashlib, re, sys

src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == 'a5f74126dfead7f5ea40a5999b3944e44fe7f0764d9bdef463df1075953f9509'
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
    """Replace the text from `head` (inclusive) to `nxt` (exclusive); both must occur exactly once."""
    assert t.count(head) == 1 and t.count(nxt) == 1, (head[:50], nxt[:50])
    E.append((section(t, head, nxt), new))


# ================================================================ header
rep("# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v1r6",
    "# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v1r7")
rep(t[t.index('**Version:** v1r6 DRAFT'):t.index('\n', t.index('**Version:** v1r6 DRAFT'))],
    "**Version:** v1r7 DRAFT, 1 November 2026 (Adelaide, UTC+10:30). v1r7 is the handover for the owner's planned chat switch (owner, 1 November 2026): after the snapshot, a **new Claude chat** takes over primary design and coding from the chat that wrote this file, and it will not have that chat's cloud workspace. On the owner's request v1r7 is more complete than usual: every section is brought up to the snapshot, and a new section 12, **Working knowledge**, writes down what used to live only in the chat (the exact mechanics of the work cycle, the tools, the workspace's traps, the owner's preferences, the lessons and the open items). It changes no rule. Appendix B lists what changed. Author: Claude. The project owner ratifies. The ChatGPT reviewer chat that started on 30 October 2026 continues; only the Claude chat changes.")
rep("**Status:** DRAFT for the owner. It becomes authoritative only when the owner ratifies it and installs it with register v0.20; until then H-1 v1r5 stands.",
    "**Status:** DRAFT for review by the ChatGPT reviewer chat and ratification by the owner. It becomes authoritative only when the owner ratifies it and installs it with register v0.23 (the snapshot); until then H-1 v1r6 stands.")
rep("**Baseline described:** the wave 2 package installed at `b61b1a27999dcdfce2e2e59c6ced4f349ee652b4` (30 October 2026; verified by Claude from GitHub; section 7). Later commits are `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/` records only.",
    "**Baseline described:** WF-1B v3 installed at `24d192fe596dc381fe2945e3b88503e68ff60d44` (1 November 2026; verified by Claude from GitHub; section 7), PERF-1 installed at `3fce3270b4797198504c85893e77e1d8f3aa35a1` (1 November 2026; verified), and the owner's report commits `441daf2` (Oz Lotto) and `608025c` (Powerball). Other later commits are `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/` records.")
rep("**Replaces, for future roles:** H-1 v1r5, v1r4, v1r3, v1r2 and v1r1 (kept as history)",
    "**Replaces, for future roles:** H-1 v1r6, v1r5, v1r4, v1r3, v1r2 and v1r1 (kept as history)")

# ================================================================ section 0
rep_between('## 0. First actions in a new Claude chat', '---\n\n## 1. Roles and workflow', """## 0. First actions in a new Claude chat

1. Clone `main`. Check that this file is the H-1 edition the current register names, and that the hashes in sections 4 and 7 and Appendix A match `git show HEAD:<path> | sha256sum`.
2. Read, in order: the introductory blurb that started your chat (`doc/HANDOVER/Claude_Primary_Handover_H1_v1r7_introductory_blurb.md`); this file, **including section 12 (Working knowledge)**; H-2 (what the reviewer checks and its rights); the **current register's newest sections** (register v0.23 and later; they hold everything since this file); H-3; `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`; `exchange/README.md`; `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (the local runner's rulebook); `doc/METHOD_TEMPLATE/README.md` (how a method is added); the governing set in section 4; `exchange/CLAUDE_WEB_TOOLS/README.md` (the tools the previous chat built with; section 12.2); the newest `exchange/EX_NNN_*` files, which show the latest open exchange with the reviewer; and the owner's two working lists, `exchange/OWNER_ROADMAP.md` and `exchange/OWNER_REMINDERS.md` (section 2).
3. Ask the owner where things stand, using section 10 and `exchange/OWNER_ROADMAP.md` as the list. Do not assume anything has advanced since this file was written; in particular, check the placeholders this file had at drafting (the two first reports, PERF-1) against the register.
4. Before any code: name the work item, its risk tier and its reviewer chat (section 1.2), and check that the owner has scoped it.
5. Keep a running checkpoint of decisions and hashes at each package boundary, so no state lives only in the chat. The cloud workspace is not permanent and is not shared between chats: everything needed to rebuild a package travels in its EX record and in `exchange/CLAUDE_WEB_TOOLS/` (sections 8.7 and 12.2). When the chat nears its limit, write the next handover first.
6. Work through section 12.9's first-hour checklist before the owner's first task.

""")

# ================================================================ section 1
rep("Its handover is H-2. The reviewer chat that served until EX_075 reached its maximum length (30 October 2026); the owner started a new one from H-2 v1r7 and its introductory blurb, both drafted by Claude on the owner's instruction, with H-2's protected rights text byte-identical. Treat the new chat exactly as the old: same rights, same independence.",
    "Its handover is H-2. The reviewer chat that served until EX_075 reached its maximum length (30 October 2026); the owner started a new one from H-2 v1r7 and its introductory blurb, both drafted by Claude on the owner's instruction, with H-2's protected rights text byte-identical. That reviewer chat has reviewed everything from EX_077 to EX_115 and continues across this Claude chat switch. Treat it exactly as the old one: same rights, same independence.")
rep("No departure has been found so far (through W2-075-RD-04).",
    "No departure has been found so far (through EX_115; the latest REVIEWER-DECIDED items were WF1-R3-C05 (EX_080), the register v0.22 correction C01 (EX_099, FIX AND PROCEED), and the optional WF1B-R2-O01 (EX_111) and WF1B-R2-O02 (EX_113), both deferred by the owner).")
rep("They travel to `exchange/` in a for-the-record EX message that needs no reply (EX_046, EX_054, EX_057, EX_067, EX_076), with the narrow diff;",
    "They travel to `exchange/` in a for-the-record EX message that needs no reply (EX_046, EX_054, EX_057, EX_067, EX_076, EX_086, EX_102), with the narrow diff, or, when the only difference is the verifier's base commit, in `CLAUDE_CODE_WORKING_FOLDER_TREE/packages/` named by a task file (WF-1A, register v0.22);")

# ================================================================ section 2
rep("- **When the owner is away** and has said to carry on: work in chunks, each ending in something the reviewer can review; hold code whose design has not yet passed; and leave a short summary of what was done, what to send and what to decide.",
    """- **When the owner is away** and has said to carry on: work in chunks, each ending in something the reviewer can review; hold code whose design has not yet passed; and leave a short summary of what was done, what to send and what to decide. On 1 November 2026 the owner, going out, told Claude to make its best guess on anything needing his approval and report it afterwards; that applies to routine choices inside an approved scope, never to a gate, a rule or anything irreversible.
- **The owner is sometimes on a phone only,** with no command window and no VS Code. Then give only steps that need no PC (an upload to the reviewer, a decision), and queue the rest.
- **Pushing:** do not push while the owner may have local commits waiting (an install, a Claude Code report, report results), or his push is rejected and he must pull with a rebase, which on his `core.autocrlf=true` checkout can rewrite record files (section 12.6). The session's stop hook complains about unpushed commits; explain the hold in one line and push straight after the owner's push.
- **Helpers (other agents):** the owner approved them on 31 October 2026. They block the chat while they run and are killed if the owner posts, so the owner agreed to wait until Claude says it has finished.""")

# ================================================================ section 4
rep("| `Predictive_Randomness_Software_Architecture_Discussion_v0_8.md` | `32cf157d9ce8850e790274e962236f2be3b50a8bdee7ec94a28ba00d7fd452ec` | Wrappers, coordinator, **5C process safety (protected)**, W-01..W-25, A-01..A-26, 20A |",
    "| `Predictive_Randomness_Software_Architecture_Discussion_v0_9.md` | `3a88e6d166bf09385760a4c191006d2072e01b0f323cd242abf88604012de104` | Wrappers, coordinator, **5C process safety (protected)**, W-01..W-25, A-01..A-26, 20A; v0.9 adds the walk-forward driver, `src/evaluation/`, the report wrapper and where records live (v0.8 `32cf157d...52ec` is history) |")
rep("| `Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md` | `2ab342911701edf1e93ad590e4765a3efac54a76d732b7fd2c5875c7d363fe74` | Wave 2: E_2, E_17 (Method A), E_18 and E_19 and the shared gaps helper; W2-1..W2-8 |",
    """| `Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md` | `2ab342911701edf1e93ad590e4765a3efac54a76d732b7fd2c5875c7d363fe74` | Wave 2: E_2, E_17 (Method A), E_18 and E_19 and the shared gaps helper; W2-1..W2-8 |
| `Predictive_Randomness_Releases_and_WF1_Design_v0_1r1.md` | `03f95fbe5c3f0e3771a07550b8b57d3c87fe5f7e06a8cc5d02974982ff7a12ee` | REL-1, WF-1A (the walk-forward driver), SEED-1 and WF-1B; WF1-1..WF1-13; the N1 fair-draw simulator and its generator (sections 7, 9.3) |
| `Predictive_Randomness_CODE3_and_E1_Revision2_Design_v0_1r2.md` | `fb3b26daba2a14c6e2b5ad82e102ed9920faba14115046a820fbd0ee63b7209a` | CODE-3 (retirement tooling) and E_1 revision 2; ER-1..ER-6 |
| `Predictive_Randomness_WF1B_Supplement_Design_v0_1r1.md` | `a2f470797f31e387f44b5492ed406f1376b3eb92f2181dc76f6ac4c80168185a` | The scorer and report's run order, families, N1, the seed and the report layout; WB-0..WB-2; WF-1C's obligations carried |
| `Deferred_Performance_Engineering_Proposal_v0_1.md` | `a5ed53c7d0cfb3278ef8342043ab1d39a99557f6f79684f3bd3276d61a5b22cb` | The owner's proposal for the final performance study (R-006). **Owner-committed, not reviewed, not ratified, authorises nothing** |""")
rep("| `METHOD_TEMPLATE/README.md` (and the 9 other template files) | `daac8da1f404e21bd1869609e4621f47bc25a84b3524c1688703c69ca2064214` | The new-method template, draft 3 (W2-7): what to copy, what to fill in, the checklist, \"things that bite\" |",
    "| `METHOD_TEMPLATE/README.md` (and the other template files) | `9e993efafe1528e9a26470d6f557f4ba32d6042b5595b802727c462a7df4d41a` | The new-method template, draft 4 (snapshot; draft 3 `daac8da1...4214` is history): what to copy, what to fill in, the checklist, \"things that bite\" |")
rep("| `HOLDOUT_EXPOSURE_RECORD_v0_2.md` | `aec833fe031b6d1d73e6acbb81757b50b193425a6899c84d438431d9df4433e2` | Factual, value-free exposure record (6 items) |",
    "| `HOLDOUT_EXPOSURE_RECORD_v0_3.md` | `53a27b02535a3a7b8d66d4c8915f451b32e01fa95daafe932c671f4e0e45ad38` | Factual, value-free exposure record, with the owner's decision HX-1 (1 November 2026; section 5.1). v0.2 (`aec833fe...33e2`, owner-ratified 26 October 2026 although its header reads CANDIDATE) is history |")
rep("register v0.20 is installed with this file (register v0.19 is `b3ae51fd162960b64a9d145a52646dceeb3aec5b91e4b359ad7166e5e4c8e6a0`).",
    "register v0.23 is installed with this file (register v0.22 is `ca955cf23b5681a534e784b4a4852acd2e8d0ccd0484e34150a05c824c0fe56b`).")

# ================================================================ section 5.1
rep("- **Quarantine from 2026-08-01.** Powerball >= 1577 and Oz Lotto >= 1694 are quarantined. Development data: Powerball 1144-1576 (433 draws), Oz Lotto 1474-1693 (220). Development targets never exceed 1576 / 1693; walk-forward windows (Powerball 1145-1576, Oz 1475-1693) are maxima pending preregistration (OPEN).",
    "- **Quarantine from 2026-08-01.** Powerball >= 1577 and Oz Lotto >= 1694 are quarantined. Development data: Powerball 1144-1576 (433 draws), Oz Lotto 1474-1693 (220). Development targets never exceed 1576 / 1693; walk-forward windows (Powerball 1145-1576, Oz 1475-1693) are maxima pending preregistration (OPEN). The first batches used those maxima; the first reports use Powerball 1286-1576 and Oz Lotto 1474-1693 (the families' windows in `src/evaluation/registry/FAMILY_REGISTRY_V1.json`).")
rep("- **The owner will not run `results_master update`**, even to test; it is gated by `HOLDOUT_OPENED_<GAME>.json`, which is not authorised.",
    """- **The owner will not run `results_master update`**, even to test; it is gated by `HOLDOUT_OPENED_<GAME>.json`, which is not authorised. Running `Run_Results_Updater.bat` with no arguments starts `update` (refused today); never suggest running it bare. The results update after Mode H is still to be designed (section 10; probe finding A1 in section 12.8).
- **Holdout exposure decision HX-1 (owner, 1 November 2026):** the record keeps the exposure it lists (a reviewer chat once displayed Powerball 1585-1588; 1585 and 1586 are inside the Powerball holdout). Mode H scores **all ten** holdout draws in each game, with Powerball 1585 and 1586 flagged in Mode H's records and report. **Until Mode H, all ten are treated as unseen**, and every rule above stays in force. The record is settled in the snapshot (section 4).
- **The two-site checker** (`src/two_site_results_check_v0_7.py`) drives The Lott's website automatically in its default `--sites both` mode. It was used only to build the first masters. **It must never be run that way again**; if it is ever needed, only its offline modes, under a reviewed change (probe finding A5).""")
rep("- **Exposure record v0.2 (six items, value-free):** never repeat the values it refers to; disclose rather than re-seal; make no claim about influence.",
    "- **The exposure record (value-free):** never repeat the values it refers to; disclose rather than re-seal; make no claim about influence.")

# ================================================================ section 5.3
rep("The installed data, in both games: E_1 `SUPPORTED` (variant `FULL_HISTORY_RAW_COUNTS_V1`, revision 1); revision 1, all `FORMULA_OPEN` with their `IN_DEVELOPMENT.txt` flags present, of E_3 and E_4 (six variants each), E_6 (three), wave 1's E_7, E_8, E_9 and E_10 (three each) and wave 2's E_2, E_17, E_18 and E_19 (three each); and E_2..E_62 each keeping a `FORMULA_OPEN` placeholder with variant `NOT_YET_SPECIFIED`, which is never edited (also for the methods that now have real variants). That is 80 declarations and 202 registry chains (282 files).",
    "The installed data, in both games: **all 40 variants are released (`SUPPORTED`)**: E_1 revision 2 (variant `FULL_HISTORY_RAW_COUNTS_V1`; revision 1 is archived under `archive/methods/E_001/r1/` by CODE-3) and the 39 revision-1 variants of E_2, E_3, E_4 (six each), E_6, E_7, E_8, E_9, E_10, E_17, E_18 and E_19 (three each), released by REL-1 (78 `entry_0002.json` records; no `IN_DEVELOPMENT.txt` flag remains); and E_2..E_62 each keeping a `FORMULA_OPEN` placeholder with variant `NOT_YET_SPECIFIED`, which is never edited. That is 82 declarations and 282 registry-entry files (364 files under `contract_data/`).")
rep("- **Other owner decisions in E2R-1 section 14:** D-1",
    """- **The releases and walk-forward (31 October 2026):** WF1-1..WF1-13 (design v0.1r1 and register v0.21); WF1-2 replaced D6-3's release order; **WF1-3 turned `ENABLE_CONTRACT_REAL_DEVELOPMENT` on** (installed with WF-1A, `0d98706`), so contract runs may read real development data (never the holdout); WF1-6 each track scored on its own grid; WF1-12 the NIST seed trusted through NIST's HTTPS service, signature `NOT_PERFORMED`; WF1-13 and ER-1..ER-6, E_1 revision 2 after CODE-3. Every real batch and every report run is a separate owner authorisation.
- **WF-1B (31 October and 1 November 2026):** WB-0 the workers change (WORKERS-1) moved to its own package WF-1C; WB-1 the report leads with the descriptive real-results tables (Part A), significance tables against fair draws after (Part B); WB-2 the approved seed travels in WF-1B. **SEED-1 (decisions SD-1 and SD-2):** the owner brought N1's pulse forward to `2026-10-31T10:30:00.000Z` (EX_103, `92a6cef`), fetched it by hand, Claude read it independently, and the owner **approved** policy `N1_ROOT_NIST_C2_20261031T1030Z_V1` (pulse 2007128; record `src/evaluation/seed_policies/N1_ROOT_NIST_C2_20261031T1030Z_V1.json`, `4c429266b6471c0939e2d0b2d3d4bd12f62300af7085e3e9283f0e14705a154a`); the 6 November policy stays as `REPLACED_BEFORE_PULSE`, never fetched. R stays 10,000.
- **PERF-1 (decisions PF-1 and PF-2, 1 November 2026):** a small item brought forward from the deferred performance study: the exact Clopper-Pearson interval found fast with bit-identical results, and the report tool's progress lines; coded and tested first and reviewed once (EX_114, EX_115 PASS), by the owner's choice of process. The rest of R-006 stays deferred.
- **The owner's other decisions in register v0.23 (31 October and 1 November 2026):** GOAL-1 (forecasts for the week of 9 November 2026, and the road to them); WF1B-A1 and WF1B-A2 (WF-1B v2 and v3 accepted; EX_111 O01 and EX_113 O02 deferred as R-007 and R-010); HX-1 (below); ORD-1 (the order: the snapshot, then Mode H with the results update and the prospective mode, then WF-1C); HO-1 (the chat switch after the snapshot); TSC-1 (the two-site checker is never used again); MH-1, OFF-1 and EFF-1 (binding inputs for the Mode H, results update and prospective design; section 12.8).
- **Other owner decisions in E2R-1 section 14:** D-1""")
rep("D2-2 a fourth switch, `ENABLE_CONTRACT_REAL_DEVELOPMENT`, stays False: contract runs are synthetic only.",
    "D2-2 a fourth switch, `ENABLE_CONTRACT_REAL_DEVELOPMENT`, stayed False until WF1-3 turned it on (above).")
rep("**No Oz Lotto method execution is authorised.**",
    "Oz Lotto runs only as the owner authorises each batch or report (the first Oz Lotto batch ran on 31 October 2026).")

# ================================================================ section 5.4
rep("- **Concurrency:** 1-6 workers, default 6; one BLAS thread per worker; no nested pools.",
    "- **Concurrency:** the coordinator allows 1-6 workers, default 6; one BLAS thread per worker initially (the wrappers pin `OMP`/`OPENBLAS`/`MKL`/`NUMEXPR` threads to 1); no nested pools. The walk-forward driver runs one method run at a time. The owner's WORKERS-1 (31 October 2026) changes both at WF-1C (section 10); until WF-1C is reviewed and installed, these limits stand.")
rep("- **The switches stay False:** `ENABLE_PROCESS_TERMINATION`, `ENABLE_SCIENTIFIC_COORDINATION`, `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE`, and since CODE-2 `ENABLE_CONTRACT_REAL_DEVELOPMENT`. No CLI override. Only the owner flips one, after reviewed tests.",
    "- **Three switches stay False:** `ENABLE_PROCESS_TERMINATION`, `ENABLE_SCIENTIFIC_COORDINATION`, `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE`. The fourth, `ENABLE_CONTRACT_REAL_DEVELOPMENT`, is True since WF-1A (WF1-3, `0d98706`). No CLI override. Only the owner flips one, after reviewed tests.")

# ================================================================ section 6
rep("The owner's account cannot create symlinks (WinError 1314), so **three** symlink tests skip on Windows (reader contracts, exit receipt, and CODE-2's dangling-symlink test); the suite runner allows exactly those.",
    "The owner's account cannot create symlinks (WinError 1314), so **four** symlink tests skip on Windows (reader contracts, exit receipt, CODE-2's dangling-symlink test, and WF-1B's symlinked-master test); the suite runner allows exactly those modules. A test that creates a symlink without catching `OSError` fails there (T013); hard links work and are the portable way to test the link guard.")
rep("- **Python 3.15 makes UTF-8 the default text encoding (PEP 686).** No effect on the project's tests so far.",
    """- **Python 3.15 makes UTF-8 the default text encoding (PEP 686).** No effect on the project's tests so far.
- **The scorer's figures are byte-identical on Windows and Linux:** `tests/test_wf1b_crossplatform.py` pins a report digest and passed on the owner's Windows (T013, T014, the WF-1B install).
- **Record files and line endings:** Git stores `results/` files as text, so on the owner's `core.autocrlf=true` checkout any Git operation that rewrites one (a rebase, a checkout) gives it CRLF bytes, and a create-only record whose bytes are checked then refuses. The first Powerball report refused this way: both committed Powerball batch records (`plan.json` and the segment record) were `w/crlf` (`git ls-files --eol`), the plan 12,029 bytes against 12,028 in Git. The owner restored them (delete the files, then `git -c core.autocrlf=false checkout -- <batch folder>`), and the report then ran. Reminder R-011 adds a `results/** -text` rule.
- **Exact arithmetic can be slow at full size:** WF-1B's exact Clopper-Pearson bisection over 10,000-trial binomial tails took over an hour per report until PERF-1. Profile at full size on invented data before trusting a run-time estimate.""")

# ================================================================ section 7.1
rep("| `b61b1a2` | Wave 2 package v1 | E_2, E_17 (Method A), E_18 and E_19 revision 1 with the shared helper `recurrence_gaps.py`, installed non-runnable; template draft 3; register v0.19 (register v0.20) |",
    """| `b61b1a2` | Wave 2 package v1 | E_2, E_17 (Method A), E_18 and E_19 revision 1 with the shared helper `recurrence_gaps.py`, installed non-runnable; template draft 3; register v0.19 (register v0.20) |
| `6a1bed9` | REL-1 v2 | Releases the 39 variants of E_2-E_4, E_6-E_10, E_17-E_19 in both games; WF-1 design v0.1r1; register v0.21 (register v0.22) |
| `0d98706` | WF-1A v2 | The walk-forward driver (`Method_Walk_Forward.py`, `_common/walk_forward.py`); `ENABLE_CONTRACT_REAL_DEVELOPMENT` on; real runs under `results/real/development/` (register v0.22) |
| `86d12ea` | E1R2 v3 | CODE-3 (`src/package_tools/method_retirement.py`), E_1 revision 1 archived, E_1 revision 2 real-capable and released (register v0.22) |
| `24d192f` | WF-1B v3 | The R3 stage-2 scorer and ranking report (`src/evaluation/`, `Run_Method_Rankings.bat`), N1 and its seed-policy records; the supplement design v0.1r1 (register v0.23) |
| `3fce327` | PERF-1 v1 | Faster exact binomial sums and Clopper-Pearson intervals (bit-identical) and the report tool's progress lines (register v0.23) |""")
rep("Document-only installs: `be18548` (DOC-1), `ee62eb6` (DOC-3), `040f80e` (DOC-4), `b846519` (register v0.12), `337b5b2` (DOC-6: H-1 v1r4, H-2 v1r5, register v0.14; four duplicate zips removed at `f9de54a`), `8defe9d` (DOC-7: H-1 v1r5, H-2 v1r6, register v0.17).",
    "Document-only installs: `be18548` (DOC-1), `ee62eb6` (DOC-3), `040f80e` (DOC-4), `b846519` (register v0.12), `337b5b2` (DOC-6: H-1 v1r4, H-2 v1r5, register v0.14; four duplicate zips removed at `f9de54a`), `8defe9d` (DOC-7: H-1 v1r5, H-2 v1r6, register v0.17), `03f7da4` (DOC-8: H-1 v1r6, H-2 v1r7, register v0.20), `2b1e7e3` (DOC-9: register v0.22). The snapshot installs this file with register v0.23; that commit cannot name itself, so Claude records it in the post-push check and the next register.\n\n**Owner data commits:** the first walk-forward batches (`86a1a01` Powerball, `8430a15` Oz Lotto: each batch's `plan.json`, segment record and the search-log row) and the first ranking reports (`441daf2` Oz Lotto, `608025c` Powerball: each report's .txt, .csv and .json and its search-log row).")

# ================================================================ section 7.2
rep("| `src/methods/Method_Contract_Runner.py` | CODE-2: the command line (`pins`, `run`); `ADAPTERS` maps a method ID to its adapter: E_1, E_2, E_3, E_4, E_6, E_7, E_8, E_9, E_10, E_17, E_18, E_19 |",
    """| `src/methods/Method_Contract_Runner.py` | CODE-2: the command line (`pins`, `run`); `ADAPTERS` maps a method ID to its adapter: E_1, E_2, E_3, E_4, E_6, E_7, E_8, E_9, E_10, E_17, E_18, E_19 |
| `src/methods/Method_Walk_Forward.py`, `src/methods/_common/walk_forward.py` | WF-1A: `plan`, `run` and `status` for a batch (one contract run per variant and target, in order; resumes; stops at the first STOP-class result); `attempts.jsonl` binds each run to its batch; `load_plan` checks the plan's bytes and its search-log row |
| `src/evaluation/` | WF-1B: `numerics.py` (exact binomial tails, MR7's null, sigma, Clopper-Pearson; PERF-1's binary-splitting sum and guided bisection), `n1_generator.py` (SHAKE-256 fair draws), `n1.py` (N1, R = 10,000), `divisions.py`, `measures.py` (MR0-MR16), `outcome_reader.py` (the evaluator-only outcome read; development prefix only), `collect.py` (grids and frozen forecasts), `report.py` (the run order), `report_writer.py` (text, CSV, JSON), `seed_policies.py` (the announced table and strict record validation) and `seed_policies/`, `registry/MEASURE_REGISTRY_V1.json` and `FAMILY_REGISTRY_V1.json`, and the entry point `Method_Rankings_Report.py` (launched by `Run_Method_Rankings.bat`). It imports no method code (a static test) |
| `src/package_tools/method_retirement.py` and `archive/methods/E_001/r1/` | CODE-3: the retirement tooling; E_1 revision 1 archived (nothing in `src/` or `tests/` may refer to `archive/`; static and runtime checks) |""")
rep("| `src/methods/E_006/` | E_6: `beta_bernoulli.py` (exact Beta-Bernoulli with forgetting; the variant table) and `contract.py`; flag present |",
    "| `src/methods/E_006/` | E_6: `beta_bernoulli.py` (exact Beta-Bernoulli with forgetting; the variant table) and `contract.py`; released |")
rep("| `src/methods/E_003/`, `src/methods/E_004/` | E_3 and E_4: `variants.py` (the same six-row table) and `contract.py` (scores p(0) and p'(0)); flags present |",
    "| `src/methods/E_003/`, `src/methods/E_004/` | E_3 and E_4: `variants.py` (the same six-row table) and `contract.py` (scores p(0) and p'(0)); released |")
rep("| `src/methods/E_007/` .. `src/methods/E_010/` | Wave 1: `variants.py` and `contract.py` each (E_7 Beta shrinkage, E_8 hierarchical periods, E_9 decayed counts, E_10 two-window contrast); flags present |",
    "| `src/methods/E_007/` .. `src/methods/E_010/` | Wave 1: `variants.py` and `contract.py` each (E_7 Beta shrinkage, E_8 hierarchical periods, E_9 decayed counts, E_10 two-window contrast); released |")
rep("| `src/methods/E_002/`, `E_017/`, `E_018/`, `E_019/` | Wave 2: `variants.py` and `contract.py` each (E_2 interval alignment, E_17 binned hazard and Method A's log-age sign, E_18 four-law mixture with a KKT certificate, E_19 per-number periodic factor); flags present |",
    "| `src/methods/E_002/`, `E_017/`, `E_018/`, `E_019/` | Wave 2: `variants.py` and `contract.py` each (E_2 interval alignment, E_17 binned hazard and Method A's log-age sign, E_18 four-law mixture with a KKT certificate, E_19 per-number periodic factor); released |")
rep("| `src/methods/E_001/` and `src/methods/E_001_Historical_Appearance_Frequency.py` | E_1's modules and its legacy entry file (now gated by `legacy_gate`) |",
    "| `src/methods/E_001/` and `src/methods/E_001_Historical_Appearance_Frequency.py` | E_1 revision 2's modules and its legacy entry file (gated by `legacy_gate`, which names revision 2) |")

# ================================================================ section 7.3
rep("### 7.3 Powerball E_1 (accepted; frozen; revision 1)",
    "### 7.3 Powerball E_1 (accepted; revision 1 frozen and archived; revision 2 installed)")
rep("- E_1's contract path (`contract_adapters/e_001.py`) is synthetic-only: E_1's multi-game function accepts only `SYNTHETIC_CONTRACT_TEST` data.",
    "- **E_1 revision 2** (`86d12ea`; WF1-13, ER-1..ER-6): its multi-game function admits `REAL_DEVELOPMENT` as well, with revision 1's counting, ranking and tie order, so E_1 runs in the walk-forward batches; revision 1's seven files are archived unchanged under `archive/methods/E_001/r1/`. The goldens and frozen outputs below are revision 1's and stay as recorded.")

# ================================================================ section 7.4
rep_between('### 7.4 Tests', '### 7.5 Owner-run tools', """### 7.4 Tests

- **471 offline tests in 36 modules** (at `3fce327`). Since v1r6's 299: `test_rel1_release` 5 (REL-1), `test_wf1a_walk_forward` 22 (WF-1A), `test_code3_retirement` 11 and `test_e1r2_revision2` 13 (E1R2), WF-1B's ten modules (`test_wf1b_numerics` 21, `_n1_generator` 8, `_divisions` 17, `_measures` 33, `_outcome_reader` 6, `_report` 10, `_static` 4, `_crossplatform` 1, `_seed_policy` 11, `_n1_replay` 3; 114), and PERF-1's `test_perf1_numerics` 7. The suite runner in each package (`RUN_WF1B_SUITE.py`, `RUN_PERF1_SUITE.py`) runs each module in its own process, compares its count, allows only the four symlink skips, and (from v3) prints a failing module's details. Results: Linux (Claude, Python 3.13.17 and a 3.15.0b4 venv) all pass, LF and CRLF; Windows (Python 3.15.2): 464 pass with 4 symlink skips (T014 and the owner's WF-1B install), 471 pass with 4 symlink skips (T015, report `9eeb843`, and the owner's PERF-1 install).
- Manual form: `PYTHONPATH=src:src/methods:tests python -m unittest -v <module>` (Windows: `set PYTHONPATH=src;src\\methods;tests`). `test_wf1b_report` takes about 2.5 minutes; the whole suite about 9 minutes on the owner's PC.
- E2R-T12 starts up to six ordinary Python worker processes that finish normally; it needs the owner's approval for each run context (approved for every rehearsal and install so far). Read every test before running it; a name or an "offline" label is not proof that it is safe. Some accepted older tests read the development masters through the project's reader (rulebook rule 2.5), so a failing test's output is checked before it is relayed.

""")

# ================================================================ section 7.5
rep("- Masters: Powerball `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8` (last row 1576); Oz Lotto `4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f` (last row 1693); each ledger holds only INIT version 1.",
    """- Masters: Powerball `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8` (last row 1576); Oz Lotto `4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f` (last row 1693); each ledger holds only INIT version 1. **The readers (`game_draws_reader.py`, `outcome_reader.py`) accept only that single INIT line,** so any update, even a `NO_CHANGE` run, makes every method run and report refuse until a version-2 reader is designed (probe finding A1; section 10).
- **The walk-forward batches** (owner-run, `Run_Experiment.bat Method_Walk_Forward.py plan|run|status ...`, 31 October 2026): Powerball `wf-3347ad1160df45faaaab1e2eedcedd0f` (targets 1145-1576, 17,280 runs, about 80 minutes) and Oz Lotto `wf-a75988650fb04cc399f8f7409ea27243` (targets 1475-1693, 8,760 runs, about 35 minutes), every run `SUCCESS`. Run folders and `attempts.jsonl` stay local and git-ignored; each batch's `plan.json`, segment record and search-log row are committed.
- **The ranking reports** (owner-run, `Run_Method_Rankings.bat --game G --batch ID --first S --last L`; files in `results/method_rankings/<GAME>/`, scoring plan and ledgers in the git-ignored `results/real/development/scores/`): Oz Lotto 1474-1693 started 1 November 2026 at 09:55 and scored all 8,760 forecasts by 10:06, then spent until about 15:00 in the statistics stage (before PERF-1); COMPLETE, attempt `rr-4be324abd2e04dfd84b3e8087e308770`, search-log row 3, committed at `441daf2`. Powerball 1286-1576 was refused at its first step ("the plan file is not a valid, unaltered WF_BATCH_PLAN_V1"; nothing read or written); the cause was the two Powerball batch records rewritten with CRLF on the owner's computer (section 6); after the owner restored them and installed PERF-1, it ran in about 26 minutes (collect 22 min, N1 3 min 12 s, measures 13 s): COMPLETE, attempt `rr-97bb48617b994a8ea18332cd36bbc98f`, search-log row 4, committed at `608025c`. **The headline (development evidence, descriptive only):** in both games nothing departs from fair draws. Oz Lotto: family Bonferroni P 0.090, N1 maximum P 0.067; best single track p 0.0092 (the best of 80 is typically about 0.012 by chance). Powerball: main-number family Bonferroni P 1.0, N1 maximum P 0.73; Powerball-number family N1 maximum P 0.99; best single track p 0.096; the smallest single figure, one variant's Powerball-number ranking at p 0.0049, is one of 80 such figures (about 0.39 after allowing for that). **Claude may not open `results/`;** the owner attaches the `.txt` reports to the chat to share them.""")

# ================================================================ section 7.6
rep("Windows wrappers, venv activation and exit flow; `Run_Experiment.bat Method_Contract_Runner.py` on Windows (only the tests have run there); NTFS symlink semantics;",
    "The coordinator's Windows wrappers, venv activation and exit flow under the coordinator; NTFS symlink semantics;")
rep("the owner's data tools under 3.15; real scientific scoring; any real-data contract run; Mode H; FINAL; online acquisition; any gate-enabled coordination.",
    "the owner's data tools under 3.15; any master version 2; Mode H; FINAL; the prospective (next-draw) mode; online acquisition; any gate-enabled coordination; parallel batches (WF-1C). (Walk-forward batches, `Run_Experiment.bat` with the contract runner and the report tool have now run on Windows, owner-run.)")

# ================================================================ section 8.6
rep("- **Where:** `CLAUDE_CODE_WORKING_FOLDER_TREE/` (rulebook `CLAUDE.md` v0.2;",
    "- **Where:** `CLAUDE_CODE_WORKING_FOLDER_TREE/` (rulebook `CLAUDE.md` v0.3 from the snapshot (v0.2 before it);")
rep("- **Use it** to rehearse a code package on the owner's Windows machine before the real install (T003 for CODE-1, T004 for CODE-2, T005 for E_6, T006 for E_3/E_4, T007 for wave 1, T008 for wave 2), when the owner wants that.",
    "- **Use it** to rehearse a code package on the owner's Windows machine before the real install (T003 for CODE-1, T004 for CODE-2, T005 for E_6, T006 for E_3/E_4, T007 for wave 1, T008 for wave 2, T009 REL-1, T010 WF-1A, T011 E1R2, T012-T014 WF-1B, T015 PERF-1), when the owner wants that.")
rep("- **Never ask the runner to count or filter output** (T005: it redirected status output to a file outside the repository to count it, and could not delete the file). Ask for the whole output in the report, and count it yourself from the report.",
    """- **Never ask the runner to count or filter output** (T005: it redirected status output to a file outside the repository to count it, and could not delete the file). Ask for the whole output in the report, and count it yourself from the report.
- **`.claude/settings.json` refuses any shell command whose text matches a deny pattern,** including `Bash(*.bat*)`. T012 stopped because two commands named `Run_Method_Rankings.bat`; T013 named it by pattern (`Run_Method_Rankings.*`). Check every task file with `check_task_vs_deny.py` (section 12.2) before committing it. The runner also writes its report with its file tool when the report's text would be refused in a shell command.
- **The runner never runs `Run_Method_Rankings.bat` or `Method_Rankings_Report.py`** (report runs are the owner's); rulebook v0.3 (in the snapshot) adds them to rule 7 with every version of the two-site checker, and a matching deny entry in `.claude/settings.json` is the owner's edit.""")

# ================================================================ section 8.7
rep("Their mutation tools, method and contract-data generators and template builders are installed under `review/E6_Install_v2/tools/`, `review/E34_Install_v1/tools/`, `review/W1_Install_v1/tools/` and `review/W2_Install_v1/tools/`. A new chat can rebuild a package from these and check it against the recorded hashes.",
    "For REL-1 and WF-1A: `EX_082_Claude/` and `EX_084_Claude/` (candidates), `EX_086_Claude/REL1_Install_v2.zip` and `CLAUDE_CODE_WORKING_FOLDER_TREE/packages/WF1A_Install_v2.zip` (finals). For E1R2: `EX_092_Claude/`, `EX_094_Claude/` and `EX_096_Claude/` (final). For WF-1B: `EX_104_Claude/`, `EX_106_Claude/` (design), `EX_108_Claude/` and `EX_110_Claude/` (v1 and v2 with the source diff), `EX_112_Claude/` (v3, installed; `WF1B_Install_v3_candidate.zip`, `cfddb0150cb9ac26f015e13adcd8b72784de040cc6628b4aefb9ac7613ec5879`). For PERF-1: `EX_114_Claude/` (`PERF1_Install_v1_candidate.zip`, `f5f375001ca98c99a79d897e4e99e2c55fd6bd48d9b6635e1a1c74e68982b4bc`, with the source diff and timings). Their mutation tools, method and contract-data generators, registry builders and template builders are installed under `review/<PACKAGE>/tools/` (for example `review/WF1B_Install_v3/tools/` and `review/PERF1_Install_v1/tools/`). **From the snapshot on, the whole working tool set is also in `exchange/CLAUDE_WEB_TOOLS/`** (section 12.2). A new chat can rebuild a package from these and check it against the recorded hashes.")

# ================================================================ section 8.8 (append lessons)
rep("- **Run Python 3.15 checks in a venv with the project's dependencies;** a bare interpreter fails every module on `numpy` and `psutil` (wave 2, before the evidence run).",
    """- **Run Python 3.15 checks in a venv with the project's dependencies;** a bare interpreter fails every module on `numpy` and `psutil` (wave 2, before the evidence run).
- **Never invent a label or status word** that no ratified document defines (WF-1B v1 printed a made-up `BONFERRONI_GUARANTEED...` label; replaced by a boolean and fixed text). Use the vocabulary the specifications give, or ask.
- **Precision bugs hide in conversions:** WF-1B's huge-Fraction-to-decimal conversion lost bits until its numerator was widened (sigma 37.055 instead of 37.047 at p = 1e-300). Test extreme values against an independent route.
- **Canonical encoders already end their bytes with a newline;** adding another gave blank lines in the score ledgers. Records must not hold tuples (only lists). A default argument bound at definition time (`replicates=R`) stopped tests from patching R; use `None`. A function looked up through a module attribute can be patched; one held in a table at import time cannot.
- **Mutation survivors show weak tests:** an early outcome read, a Bonferroni M and a missing Monte Carlo line each survived until a test asserted them. Plan a mutant for each ordering, count and printed figure.
- **Task commands must pass the runner's deny list** (T012: `.bat` text). **Tests must be Windows-safe** (T013: an unguarded `symlink_to`). **Probes must not import package scripts in place** (a `__pycache__` crept into a package; rebuilt). Each cost one rehearsal round.
- **An exact method can be correct and still unusably slow:** WF-1B's exact Clopper-Pearson took over an hour per real report; full-size profiling on invented data found it in minutes (PERF-1). Profile at full size before the owner's first real run.""")

# ================================================================ section 9
rep("CODE-1 and CODE-2 give every method the release gate, create-only publication, receipts and traceability. A new method needs only its own pieces, and starts from the template, `doc/METHOD_TEMPLATE/` (draft 3; README and checklist), as every method since E_6 has:",
    "CODE-1 and CODE-2 give every method the release gate, create-only publication, receipts and traceability. A new method needs only its own pieces, and starts from the template, `doc/METHOD_TEMPLATE/` (draft 4; README and checklist), as every method since E_6 has:")
rep("4. **Release** (a separate small reviewed package; the owner's two actions): delete the flag; append a `SUPPORTED` entry for the same declaration. Then the method can run through the contract runner, on synthetic data.\n5. **Real data** stays a separate owner gate: `ENABLE_CONTRACT_REAL_DEVELOPMENT` is False (D2-2). Turning it on, the development walk-forward, preregistration and scoring are each their own reviewed, owner-approved steps.",
    "4. **Release** (a separate small reviewed package; the owner's two actions, as REL-1 did for 39 variants): delete the flag; append a `SUPPORTED` entry for the same declaration. Then the method can run through the contract runner.\n5. **Real data:** with `ENABLE_CONTRACT_REAL_DEVELOPMENT` on (WF1-3), a released method joins the next walk-forward batch the owner authorises; a batch holds the full cohort (ER-6), so a new method means a new batch per game, then a report. Preregistration, Mode H and FINAL stay separate gates.")
rep("Method A's predictor is E_17's `HAZARD_LOGAGE_SIGN_V1` (installed in wave 2), and its diagnostics A1-A5 are a later package after WF-1 (W2-3); Method B becomes E_45's specification in wave 3.",
    "Method A's predictor is E_17's `HAZARD_LOGAGE_SIGN_V1` (installed in wave 2), and its diagnostics A1-A5 are a later package after WF-1 (W2-3); Method B becomes E_45's specification in wave 3. Template draft 4 adds what releases, walk-forward batches, scoring and the Windows rehearsals taught (R-009).")

# ================================================================ section 10
rep_between('## 10. Next work, in order', '---\n\n## 11. Gates that stay closed', """## 10. Next work, in order (planned; the owner decides each step)

1. **Done since v1r6:** DOC-8; the new reviewer chat; REL-1, WF-1A and E_1 revision 2 with CODE-3 (rehearsals T009-T011); register v0.21 and v0.22 (DOC-9); the first walk-forward batches; SEED-1 (approved); WF-1B (design EX_104-EX_107, code EX_108-EX_113, rehearsals T012-T014, installed `24d192f`); PERF-1 (EX_114, EX_115 PASS; T015 PASS; installed `3fce327`); the first two ranking reports (`441daf2`, `608025c`); the two cold-read probes (section 12.8).
2. **Now:** the snapshot (this file, H-2 v1r8, register v0.23, Architecture v0.9, template draft 4, the settled exposure record, the rulebook update, `README.md`, the `results/` line-ending rule; `exchange/CLAUDE_WEB_TOOLS/`); then the chat switch.
3. **Next, towards the owner's goal of next-draw forecasts for the draws of the week of 9 November 2026** (`exchange/OWNER_ROADMAP.md` item 10c), designed together:
   - **Mode H:** each method tested once on the ten sealed holdout draws per game (R3 sections 3 and 6; V1), all ten scored, Powerball 1585 and 1586 flagged (HX-1). OPEN: the Mode H store (combined master or a separate store releasing one outcome at a time; R3 6.2), the study manifest and opening record, the `HOLDOUT_OPENED_<GAME>.json` record (defined only in code; probe A2), and the freeze-before-outcome mechanism;
   - **the results update:** the holdout and later draws added by the update process, **with a version-2 master reader** (probe A1: today every reader refuses any ledger beyond INIT version 1), master-version pinning (probe A6: `NO_CHANGE` rows share a SHA), and the owner's procedure for accepting a new version (probe A7);
   - **the prospective mode:** each method's forecast for the next draw, frozen and published before the draw (R3-D20: the timing proof, GitHub push evidence, is an OPEN implementation choice), scored after it;
   - then the owner decides whether to declare the system developed.
4. **WF-1C** (WORKERS-1; roadmap item 10d): the coordinator's limit 1 up to the logical processor count (24 on the owner's PC), default half; the walk-forward driver's `--workers`; a progress line; a `compare` command; the identity tests once. Its own design round, carrying EX_101's four obligations and EX_105's B01 and C02-C05 in full (EX_107). The owner chose (1 November 2026) to keep it after Mode H.
5. **Then, in the owner's order:** wave 3 (E_27, E_45 = Method B, E_26, E_28; template draft 4 is ready for it); the NL-means discussion (R-002); waves 4 to 11 (4 E_5, E_11, E_15, E_14, then E_13, E_12 and E_16 each in its own package; 5 E_37, E_33, E_35, E_34, E_39, E_36, E_38, E_40; 6 E_23, E_25, E_20, E_21, E_22, E_24; 7 E_32, E_29, E_30, E_31; 8 E_41, E_42, E_43, E_44, E_46, E_47; 9 machine learning E_49-E_53, with a dependency change; 10 E_57, E_60, E_58, E_59, E_61, E_62; 11 E_54, E_48); the ensembles last; the final performance study only when the owner activates it (R-006; roadmap item 22).
6. **Method A's diagnostics A1-A5** (W2-3): a separate package after WF-1; they need the seed policy (now approved) and a diagnostic report design.
7. **Coordinated contract runs** (D2-1), when the owner wants many methods run together.
8. **Still permission-gated, each separately:** each walk-forward batch and report run; walk-forward preregistration; Windows lifecycle and destructive gates (P2 closure, ERR-R2-02 / Option F final acceptance); allowlist entries; the in-sample engine (R3 17.13 stage 3); Mode H; FINAL and the production weekly loop; any master update.
9. **Housekeeping, owner's choice:** the data tools' first run under 3.15; later, delete `venv.bak` and Python 3.14; OPEN-N2; the duplicate exploration note in `doc/`; the old EX copies in `review/` (R-003); the deferred optionals R-007 (EX_111 O01) and R-010 (EX_113 O02, already in the runner template); R-008 (the verifier's wording for a missing file).

**Genuinely OPEN questions** (do not disguise as decided): walk-forward preregistration; the Mode H store and mechanics; the version-2 reader and master pinning; R3-D20's timing proof; E_54 feed timing; each remaining `FORMULA_OPEN` method's formula; E_63 and later identities; scientific allowlist activation; whether to scope the optional oracle prototypes (agreed position 10.3); WF-1C's open choices (the 60-worker cap, memory floor, WB-3/WB-4).

""")

# ================================================================ section 11
rep("This handover authorises nothing. In particular: no Windows lifecycle or destructive test; no real-data scientific evaluation; no real-data contract run; no holdout access;",
    "This handover authorises nothing. In particular: no Windows lifecycle or destructive test; no real-data batch or report run without the owner's authorisation of that run; no holdout access;")

# ================================================================ section 12 (new) + Appendix A
S12 = open(__file__.replace('make_h1_v1r7.py', 'section12.md'), 'rb').read().decode('ascii')
assert '\r' not in S12 and S12.startswith('## 12. Working knowledge') and S12.endswith('\n')
rep("---\n\n## Appendix A. Identities (non-self-referential)", "---\n\n" + S12 + "\n---\n\n## Appendix A. Identities (non-self-referential)")

rep("| H-2 v1r6 (current reviewer handover until v1r7 is installed) | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r6.md`, `db40f40ef22995fc65a949243001858f1d7d1285713c9954531ae6b601fc5616` |\n| H-1 v1r5 (predecessor) | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r5.md`, `1214bd971058ddd6cc680526fd80375bdbbd6db17397e41ba4c14ae5467101e1` |",
    "| H-2 v1r7 (current reviewer handover until v1r8 is installed) | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r7.md`, `a59ab8504d0d63d852d66efcc9491a05d3329656eb5164eef682df57da60ec38` |\n| H-1 v1r6 (predecessor) | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r6.md`, `a5f74126dfead7f5ea40a5999b3944e44fe7f0764d9bdef463df1075953f9509` |\n| H-1 v1r5 | `doc/HANDOVER/Claude_Primary_Handover_H1_v1r5.md`, `1214bd971058ddd6cc680526fd80375bdbbd6db17397e41ba4c14ae5467101e1` |")
rep("| Register v0.19 | `doc/RATIFICATION_REGISTER_v0_19.md`, `b3ae51fd162960b64a9d145a52646dceeb3aec5b91e4b359ad7166e5e4c8e6a0` |",
    "| Register v0.22 | `doc/RATIFICATION_REGISTER_v0_22.md`, `ca955cf23b5681a534e784b4a4852acd2e8d0ccd0484e34150a05c824c0fe56b` |")
rep("| Wave 2 final package | `exchange/EX_076_Claude/W2_Install_v1.zip`, `57ef34b67b8aa6cc023c5ea3d78c2940ab1a9875c3141626c5016355da53c429` |",
    """| Wave 2 final package | `exchange/EX_076_Claude/W2_Install_v1.zip`, `57ef34b67b8aa6cc023c5ea3d78c2940ab1a9875c3141626c5016355da53c429` |
| REL-1 install manifest | `review/REL1_Install_v2/INSTALL_MANIFEST_SHA256.txt`, `84781794be27ae39958d66a931272011f3e9b068c0929420027fbfa37228e3e3` |
| REL-1 final package | `exchange/EX_086_Claude/REL1_Install_v2.zip`, `3ca731fe22ffc10a2dd4f59fd5f5725f9f6c88553a426f12eea395795e1e4b36` |
| WF-1A install manifest | `review/WF1A_Install_v2/INSTALL_MANIFEST_SHA256.txt`, `8f9810949b02dfb832ab13d6e97720986f773eab09fd6b39621c42fcb107eb51` |
| WF-1A final package | `CLAUDE_CODE_WORKING_FOLDER_TREE/packages/WF1A_Install_v2.zip`, `9fa6577ab95d5a16931a6df7c056764f06a61282e2f78a497b2292610a9e3c06` |
| E1R2 install manifest | `review/E1R2_Install_v3/INSTALL_MANIFEST_SHA256.txt`, `57c90bbf6c8e5b30fa486ea804c759309812f955e1f05ee154549fbca4279bde` |
| E1R2 final package | `exchange/EX_096_Claude/E1R2_Install_v3.zip`, `8547fd37fea6e5dc6a1f1941322cc5844031f2351bd50fb4c1ee1179086a2394` |
| WF-1B install manifest | `review/WF1B_Install_v3/INSTALL_MANIFEST_SHA256.txt`, `d8b89e25ab937a2e737fc3a0dad28ba3e11380fb6b2cc5aa98be88f164baa033` |
| WF-1B installed package | `exchange/EX_112_Claude/WF1B_Install_v3_candidate.zip`, `cfddb0150cb9ac26f015e13adcd8b72784de040cc6628b4aefb9ac7613ec5879` |
| PERF-1 package | `exchange/EX_114_Claude/PERF1_Install_v1_candidate.zip`, `f5f375001ca98c99a79d897e4e99e2c55fd6bd48d9b6635e1a1c74e68982b4bc`; install manifest `review/PERF1_Install_v1/INSTALL_MANIFEST_SHA256.txt` `64faaa9f76f0d0b5228f2461f9b77d3e868556a3b5203a27ecc7fbfb82eb32e9` |
| The approved N1 seed record | `src/evaluation/seed_policies/N1_ROOT_NIST_C2_20261031T1030Z_V1.json`, `4c429266b6471c0939e2d0b2d3d4bd12f62300af7085e3e9283f0e14705a154a` |
| WF-1B registries | `src/evaluation/registry/MEASURE_REGISTRY_V1.json`, `133d5608c3772c3fb95a8cda586bc1ff822d5f8e003c11a386a84ae117ef9bcf`; `FAMILY_REGISTRY_V1.json`, `97299f32475e3e7311adc421f3dedf09f9a9c88aca2f8906adf4944904b341ac` |""")

# ================================================================ Appendix B
rep_between('## Appendix B. Changes in v1r6', '*End of H-1.*', """## Appendix B. Changes in v1r7

v1r7 refreshes v1r6 in place for the chat switch, with more detail than usual (owner, 1 November 2026). It changes no rule; where it states a rule, the ratified documents and the register prevail. Nothing in v1r6 was dropped except what is superseded below. v1r6's own change list stays in v1r6.

1. **Header and section 0:** the chat switch; baseline WF-1B v3 (`24d192f`); register v0.23; the reading list adds section 12 and `exchange/CLAUDE_WEB_TOOLS/`; a first-hour checklist.
2. **Section 1:** the reviewer chat continues (EX_077-EX_115); oversight through EX_115; for-the-record finals EX_086 and EX_102, and the packages folder.
3. **Section 2:** best-guess working while the owner is out; phone-only periods; the push hold; helpers. Section 2A is unchanged, byte for byte (the builder asserts the whole section).
4. **Section 4:** the WF-1, E1R2 and WF-1B supplement designs and the owner's performance proposal added; Architecture v0.9, template draft 4 and the settled exposure record; the register pointer moves to v0.23.
5. **Section 5:** the report windows; HX-1; the updater's bare launch and the two-site checker's Lott automation flagged; all 40 variants released and 364 contract-data files; the WF-1, WF-1B, SEED-1 and PERF-1 decisions; the fourth switch on; concurrency until WF-1C.
6. **Section 6:** four Windows symlink skips and hard links; the cross-platform pin; record files and line endings; exact arithmetic's run time.
7. **Section 7:** five code installs and DOC-8/DOC-9; the module map adds the driver, `src/evaluation/`, CODE-3 and the archive; E_1 revision 2; tests 471; the batches, the reports and the version-1-only readers; the not-tested list.
8. **Section 8:** T009-T015; the deny list; the runner never runs the report tool; rebuild records through PERF-1 and the tool folder; seven lessons added.
9. **Section 9:** template draft 4; releases and real data as they now work.
10. **Section 10:** rewritten: the snapshot, Mode H with the results update and the prospective mode, WF-1C, the waves.
11. **Section 11:** batch and report runs are per-run owner authorisations.
12. **Section 12 (new):** working knowledge.
13. **Appendix A:** current identities.

""")

# ================================================================ apply
for old, new in E:
    c = t.count(old)
    assert c == 1, (c, old[:90])
    assert new.isascii(), old[:60]
    t = t.replace(old, new)

# ================================================================ candidate 2: the cold-read test's gaps (1 Nov 2026)
R1_LOC = ("`doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` mentions draw numbers at or after "
          "the quarantine boundary on lines 14 (\"R1 v0.4 revision record\"), 59 and 62 (section 1), 81 (section 1.1a), "
          "926 and 928-931 (section 8A.2), 980 (section 10) and 1056-1057 (section 11). Skip those lines and their "
          "paragraphs entirely: do not read, print, quote or diff them (located by line number only, with "
          "`grep -n PATTERN FILE | cut -d: -f1`)")
E2 = [
    ("1. Clone `main`. Check that this file is the H-1 edition the current register names, and that the hashes in sections 4 and 7 and Appendix A match `git show HEAD:<path> | sha256sum`.",
     "1. Clone `main`. Check that this file's Git-content SHA-256 equals its line in the snapshot's manifest, `review/DOC10_Snapshot_v1/INSTALL_MANIFEST_SHA256.txt` (a file cannot name its own hash; later register editions record it), and that the hashes in sections 4 and 7 and Appendix A match `git show HEAD:<path> | sha256sum`."),
    ("and R-8..R-11 (problem framing, evidence sufficiency, declining unsafe tests, material findings outside a narrow scope).",
     "and R-8..R-11 (problem framing, evidence sufficiency, declining unsafe tests, material findings outside a narrow scope). R-8..R-11 are ratified (register; H2-TAKEOVER-O01): H-2's section 3 still calls them \"proposed for owner ratification\" only because its rights region is kept byte-identical; the register's ratification prevails."),
    ("No verifier, no PRE/POST/COMMITTED, no reviewer check of the install zip. Content review is unchanged.",
     "Until the snapshot these had no verifier. **DOC-10 (the snapshot) has one** (`VERIFY_DOC10_INSTALL.py`, pre/post/committed), because it also replaces files outside `doc/` and `review/` (`README.md`, `.gitattributes`, the Claude Code rulebook); a small document-only install may still use the short form. Content review is unchanged."),
    ("- **The exchange protocol** (`exchange/README.md` v0.4, `63c19e7`).",
     "- **The exchange protocol** (`exchange/README.md` v0.5, 1 November 2026, which brought v0.4 (`63c19e7`) into line with this section)."),
    ("Real weekly forecasting starts only after modelling is complete: train on all eligible draws before the target, predict, freeze and push before the draw, score afterwards, append the draw, repeat.",
     "Real weekly forecasting (**the prospective mode**, the owner's weekly session MH-1, section 10) starts once the owner declares the pipeline **developed** for the released cohort (GOAL-1); later waves keep adding methods afterwards. Each week: update the results, catch up missed draws in order, score the open forecast, then train on all eligible draws before the next target, predict, freeze and record it before the draw. How R3's FINAL mode maps onto this loop is OPEN for the Mode H design (section 10)."),
    ("| `METHOD_TEMPLATE/README.md` (and the other template files) | `9e993efafe1528e9a26470d6f557f4ba32d6042b5595b802727c462a7df4d41a` |",
     "| `METHOD_TEMPLATE/README.md`; `METHOD_SPECIFICATION_TEMPLATE.md` `82705363c26994cea253edd49416a4bc5a6f3cfcfe615ef2261cc2e61e0b9da5`; `CHANGES.md` `eda583e42f93c5734523e49e0f2c4fc849d16ce94a1f0b405b3d192287068ed8` (the other template files unchanged) | `9e993efafe1528e9a26470d6f557f4ba32d6042b5595b802727c462a7df4d41a` |"),
    ("- **The owner will not run `results_master update`**, even to test; it is gated by `HOLDOUT_OPENED_<GAME>.json`, which is not authorised.",
     "- **The owner will not run `results_master update`**, even to test, **until he separately approves the first update run at the Mode H stage** (an always-review subject); it is gated by `HOLDOUT_OPENED_<GAME>.json`, which is not authorised. Opening the holdout (writing that record) is also a separate owner approval; who or what writes it is designed in Mode H."),
    ("Until Mode H, all ten are treated as unseen**, and every rule above stays in force. The record is settled in the snapshot (section 4).",
     "Until Mode H, all ten are treated as unseen**, and every rule above stays in force. **HX-2 (owner, 1 November 2026):** the holdout is fixed and is never extended; Powerball 1587 and 1588 are ordinary post-holdout draws the same chat saw, and when the catch-up (MH-1) scores them those two catch-up scores carry the same flag (flagged draws remain fully valid and counted, no gap; the flag is information only); until then every rule for draws at or after 1577 applies to them. The record v0.3 is settled in the snapshot (section 4)."),
    ("When diffing documents containing the R1 draw-1587 paragraph, filter it out first.",
     "When diffing documents containing the R1 paragraphs that name quarantined draws, filter them out first. **Where they are:** " + R1_LOC + "."),
    ("- Never let a tool print a quarantined row or the R1 draw-1587 paragraph.",
     "- Never let a tool print a quarantined row or the R1 paragraphs that name quarantined draws (their line numbers are in section 5.1)."),
    ("| CODE-2: `run_contract_method` and the switch `ENABLE_CONTRACT_REAL_DEVELOPMENT = False` |",
     "| CODE-2: `run_contract_method` and the switch `ENABLE_CONTRACT_REAL_DEVELOPMENT` (True since WF-1A, WF1-3) |"),
    ("master-version pinning (probe A6: `NO_CHANGE` rows share a SHA)",
     "master-version pinning (probe A1: `NO_CHANGE` rows bump the version with the same SHA)"),
    ("| Exchange protocol v0.4 | `exchange/README.md` at `63c19e7`, `b08d9e2b62daf1f435c5c02b8908e447c1bc790b28d1d92c2866f110846b2256` |",
     "| Exchange protocol v0.5 | `exchange/README.md` (committed by Claude with the snapshot's candidate 2), as stored (CRLF) `722df2e0cdef406d04ab635ee0e1bb34dc51a654095315197855fd4670d732ba`; v0.4 at `63c19e7`, `b08d9e2b62daf1f435c5c02b8908e447c1bc790b28d1d92c2866f110846b2256` |"),
    ("| Register v0.22 | `doc/RATIFICATION_REGISTER_v0_22.md`, `ca955cf23b5681a534e784b4a4852acd2e8d0ccd0484e34150a05c824c0fe56b` |",
     "| Register v0.23 (installed with this file) | `doc/RATIFICATION_REGISTER_v0_23.md`, `22a6f2f7a213bbd86124fd77d52df7b0c0bdcf673298429f9341005bc8e51cdc` |\n| Register v0.22 | `doc/RATIFICATION_REGISTER_v0_22.md`, `ca955cf23b5681a534e784b4a4852acd2e8d0ccd0484e34150a05c824c0fe56b` |\n| H-2 v1r8 (installed with this file) | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8.md`, `4239f566eb4e7e4a938552a01709f169448c26514b7dc57837c7eb8238f4bcb2`; its blurb `17633e4ec5413d12ed3c2909819b9f899a156af22631a31ee3e1b6f145ea0d2a` |\n| Holdout exposure record v0.3 (installed with this file) | `doc/HOLDOUT_EXPOSURE_RECORD_v0_3.md`, `53a27b02535a3a7b8d66d4c8915f451b32e01fa95daafe932c671f4e0e45ad38` |\n| Architecture v0.9 (installed with this file) | `doc/Predictive_Randomness_Software_Architecture_Discussion_v0_9.md`, `3a88e6d166bf09385760a4c191006d2072e01b0f323cd242abf88604012de104` |\n| This file (H-1 v1r7) | identified by the DOC-10 manifest, `review/DOC10_Snapshot_v1/INSTALL_MANIFEST_SHA256.txt` |"),
    ("| Claude Code rulebook v0.2 | `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`, `12b50a5cadda0d5cef73106b75ec31051fd1c6b4cbe80ddafa387bd49936f562` |",
     "| Claude Code rulebook v0.3 (installed with this file) | `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`, `509e381ed612e7572940014d33f2724172a12a0da8a8a1e76020571ede63b56b` |\n| Claude Code rulebook v0.2 (until the snapshot) | `12b50a5cadda0d5cef73106b75ec31051fd1c6b4cbe80ddafa387bd49936f562` |"),
    ("- **The runner never runs `Run_Method_Rankings.bat` or `Method_Rankings_Report.py`**",
     "- **Before writing any task file:** check that `.claude/settings.json` holds the owner's deny entry for the report tool (`Bash(*Method_Rankings_Report*--game*)`, added by the owner after the snapshot install; if absent, ask him), then run `check_task_vs_deny.py` on the task file.\n- **The runner never runs `Run_Method_Rankings.bat` or `Method_Rankings_Report.py`**"),
    ("   - **Mode H:** each method tested once on the ten sealed holdout draws per game (R3 sections 3 and 6; V1), all ten scored, Powerball 1585 and 1586 flagged (HX-1).",
     "   - **Mode H:** every released variant forecasts each of the ten sealed holdout draws per game walk-forward (each from the draws before it; R3 sections 3 and 6; V1), all frozen before the holdout is opened, then scored once; all ten scored, Powerball 1585 and 1586 flagged (HX-1). OPEN: whether Mode H's ten steps also serve as the first catch-up steps of MH-1, and how the post-holdout draws are handled (Powerball 1587 and 1588 flagged when caught up, HX-2)."),
    ("   - **the prospective mode:** each method's forecast for the next draw, frozen and published before the draw (R3-D20: the timing proof, GitHub push evidence, is an OPEN implementation choice), scored after it;\n   - then the owner decides whether to declare the system developed.",
     "   - **the prospective mode** = the owner's weekly session MH-1 (section 12.8): each method's forecast for the next draw, frozen and recorded before the draw, scored after it. R3 sections 10.1(6) and 10.2 and R3-D20 name a GitHub push as the timing proof; under OFF-1 a ratified R3 amendment, or a ratified design that supersedes those clauses, must come before the first prospective forecast. How R3's FINAL mode relates to this loop is OPEN;\n   - then the owner decides whether to declare the system developed (GOAL-1: the pipeline is ready for the released cohort; later waves continue).\n   - **Schedule:** the draws are weekly, Oz Lotto on Tuesday and Powerball on Thursday; the goal is the draws of Tuesday 10 and Thursday 12 November 2026. The critical path: the snapshot installed; the design (reviewed, owner-ratified, version-2 reader first); the code (reviewed, rehearsed by Claude Code, installed); the owner's approvals to run the first update and open the holdout; Mode H; the first weekly session. **FB-1 (owner, 1 November 2026):** if that cannot be ready, the first forecasts slip a week rather than any review or rehearsal being cut; the catch-up covers the missed draws."),
    ("13. **Appendix A:** current identities.\n",
     "13. **Appendix A:** current identities.\n14. **Candidate 2 (after a cold-read test of this file by a fresh helper, 1 November 2026):** the 20 gaps it found fixed (`exchange/EX_116_Claude/cold_read_h1_gaps.md`): the prospective-mode, developed and FINAL terms; R3's push-based timing proof against OFF-1; Mode H stated precisely; HX-2 and FB-1; the schedule; who approves the first update; the R1 lines to skip, by line number; the switch in the module map; the 3.15 venv's packages; where the suite runs; document-only installs with a verifier; `exchange/README.md` v0.5; repository access; R-8..R-11 ratified; the source of the no-manual-Lott-check decision; Appendix A and section 0; the deny-entry check before a task file; `--mirror`.\n"),
]
for old, new in E2:
    c = t.count(old)
    assert c == 1, (c, old[:90])
    assert new.isascii(), old[:60]
    t = t.replace(old, new)
assert section(t, '### 2A. The owner\'s foundational points', '---\n\n## 3.') == S2A, 'section 2A changed'
assert '\r' not in t and t.isascii() and t.endswith('*End of H-1.*\n')
fills = re.findall(r'\[\[FILL: [^\]]*\]\]', t)
b = t.encode('ascii')
open(out, 'wb').write(b)
print(len(E), 'edits;', out, hashlib.sha256(b).hexdigest(), len(t.splitlines()), 'lines;', len(fills), 'placeholders')
for f in fills:
    print('  ', f)
