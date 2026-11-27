# The one tree tidy: what is kept, what is removed, and how (proposal v0.1)

Date: 28 November 2026. From the Claude web chat, for the reviewer's agreement and the owner's ratification.
**Status: PROPOSAL. Nothing in it is done or authorised. It is carried out only after QA and PROD exist.**

## 1. What is already agreed in principle (decision log entries 394 and 395)

- **No Git history is rewritten.** A reset would save about 5 MB (68 MB packed against 63 MB as one commit). An
  ordinary `git gc` is the owner's to run if he wishes.
- **One tidy, once,** after QA and PROD are made and their first fills agree with DEV's. An annotated tag is pushed
  on the last commit before it. What is removed from the tree stays in the history under that tag.
- **All future software development is in `a_p_r_i_r_DEV`.** The first system at the top level is retired.
- **The first system's `results/` are kept unchanged** (the sealed Mode H records, the first study's findings).
- **The tag keeps tracked files only.** Untracked and ignored files are covered by the owner's own full-tree
  backups, which he checks before he deletes any of them.
- **Proving a later change** (the reviewer's qualification): "a rebuild gives the same as before" proves a change
  that is meant to preserve behaviour. A scientific correction or a new method is proved by its own mathematics
  and its own tests, as now.

## 2. A correction of what Claude said earlier

Claude said three of the 280 tests depend on the first system. Three **read** it. But retiring the two
comparison tools takes more with it, and one part must stay:

- `deploy/compare_with_frozen.py` goes, and with it the whole of `tests/test_research_compare.py` (6 tests).
- `deploy/compare_updater_with_frozen.py` goes as a tool, and with it the 2 tests of the class
  `TheSameAsTheFrozenUpdater`. **But the other 25 updater tests use its invented pages and its invented trees**
  (`make_tree`, `InventedPages`, `page_text`, `invented_draw`, `load`, `HELD`, `TODAY`). Those helpers move,
  unchanged, into a fixtures file under `tests/`.
- So the suite goes from 280 tests to 272. No file under `src/` changes.
- One line of a comment in `src/updater/results_updater.py` names the retired tool. It is left as it is, so that
  the updater's fingerprint does not change; it is put right with the next real change to the updater.

## 3. The inventory

Sizes are of tracked files at `59f7a31` (5,024 files, 178 MB). The exact list of paths is produced at step P1.

### 3.1 Kept

| What | Where |
|---|---|
| The living system | `a_p_r_i_r_DEV/` (all of it, less the two tools and 8 tests of section 2) |
| The first system's results | `results/` (all 52 files, 44 MB; not one byte changed) |
| The runner | `CLAUDE_CODE_WORKING_FOLDER_TREE/` (all of it), `CLAUDE.md` at the root, `.claude/settings.json` |
| Root files | `.gitattributes`, `.gitignore` (both unchanged), `LICENSE`, `README.md` (rewritten: ten lines pointing to `a_p_r_i_r_DEV/README.md` and the archive index), `.vscode/` |
| The records | `exchange/DECISIONS/` (the decision log and the owner's decision records), `exchange/CONTINUITY_NOW.md`, `exchange/OWNER_REMINDERS.md`, `exchange/OWNER_ROADMAP.md`, `exchange/README.md` |
| The scheme and its papers | the eight papers of 26 November 2026 in `exchange/` (`Claude_*_20261126.md`, `ChatGPT_*_20261126.md`), this paper, `exchange/ChatGPT_to_Claude_Operations_Manual_Discussion_v0_1_20261125.md` |
| Handovers | in `doc/HANDOVER/`: the two in force with their blurbs (H-1 v18, H-2 v12, or their successors) |
| Standards | `doc/CODING_PRACTICES_v0_1.md`, `doc/FILE_FORM_STANDARD_v0_2.md` |
| The science | `doc/Predictive_Randomness_System_Specification_v0_6.md`, `doc/contracts/TIE_SHA256_V1_Ratified_Encoding_v0_2.md`, `doc/NUMERICAL_INTEGRITY_AND_RETRAINING_REFERENCE_v0_1.md`, `doc/HOLDOUT_EXPOSURE_RECORD_v0_3.md`, `doc/SAL_Powerball-Game-Rules_March-2026.pdf` |
| Method research and roadmaps | `doc/Predictive_Randomness_Research_Project_Proposal_v0_6.md`, `..._Experimental_Methods_Research_R1_v0_4.md`, `..._Experimental_Method_Specifications_R2_v0_5.md` with its two erratum records, `..._Evaluation_and_Reporting_Specifications_R3_v0_5.md`, `..._Method_Ranking_Measures_Proposal_v0_5.md`, the method designs (`..._Wave1_...`, `..._Wave2_...`, `..._E3_E4_...`, `..._E6_...`), `..._Future_Method_Priorities_v0_1_DRAFT.md`, `doc/Deferred_Performance_Engineering_Proposal_v0_1.md`, `doc/Claude_Research_Historical_Results_Sources_v2.md`, `doc/GASI_thought_experiments/` (the owner's method ideas A and B) |
| The register | `doc/RATIFICATION_REGISTER_v0_33.md` (the newest; later ratifications are in the decision log) |

### 3.2 Removed from the tree (kept in the history under the tag)

| What | Where | About |
|---|---|---|
| The first system's software | `src/`, `tests/`, `deploy/`, `archive/`, and at the root the six `Run_*.bat`, `Withdraw_Variant.bat`, the four environment scripts, `requirements.txt`, `ENVIRONMENT.example.ini`, `Claude_Safety_Review_POC_Coordinator_Termination_v2.md` | 696 files, 4 MB |
| Its tracked data stubs | `source_data/` (8 files), `transitory_data/` (7 files) at the top level | 15 files |
| The other project | `GAIS/` | 204 files, 3.6 MB |
| Old review copies | `review/` | 378 files, 18 MB |
| Finished correspondence | in `exchange/`: every `EX_nnn_*` message and folder (EX_001 to EX_333), `CLAUDE_WEB_TOOLS/` (all work packages), the stocktakes, the direction drafts, the takeover notes, `DOC8*`, `DOC12/`, `DOC13/`, `RUNS/`, `HO2_2026_11_10/`, `HISTORY_CLEANUP_2026_11_06/`, `ChatGPT_REVIEWER_H2V6/`, every `HANDOVER_*` folder (candidates), the other dated `ChatGPT_to_Claude_*` and `OUTLANDISH_01_*` notes | 3,060 files, 87 MB |
| Superseded documents | in `doc/`: every handover but the two in force, registers v0.1 to v0.32, `superseded/`, `METHOD_TEMPLATE/` (the first system's contract form), `experiments/`, `how_things_work/`, and the designs of the first system and of the 22 November redesign (Mode H, MHUP-B, deployment design v0.12, releases, E1 and E2R, the Windows POC, the architecture and AI-roles discussions, the direction papers, the stocktake) | 246 files, 16 MB |

In all 4,599 of the 5,024 tracked files and 129 MB, by Claude's count from these rules at `59f7a31`; 425 files
and 50 MB stay. Step P1 gives the list itself.

**For the reviewer to correct:** the doc keep list of 3.1 is Claude's reading of "current scientific specifications,
method research documents and roadmaps". Name any document to move from one table to the other.

### 3.3 Untracked files on the owner's PC (his to delete, by hand, after checking his backup)

The pull of step P5 removes only tracked files. What is left in the removed folders is untracked: the top-level
`.venv\`, `__pycache__` folders, the top-level `transitory_data\` and `source_data\` contents, anything under
`GAIS\`, leftover task clones under `CLAUDE_CODE_WORKING_FOLDER_TREE\scratch\`, and `D:\DELETE_ME\`. **Never
`a_p_r_i_r_DEV\source_data`, `a_p_r_i_r_DEV\results` or `a_p_r_i_r_DEV\.venv`:** step P6 names every folder by its
full path.

## 4. The procedure

Each step ends with a check. A check that fails is a STOP: nothing further is done, and nothing is undone.

- **P0. Before anything.** QA and PROD exist and their first fills agree with DEV's. No runner task is under way.
  The owner's full-tree backup is run again and its three external copies verify.
- **P1. The exact list (Claude).** A text file under `exchange/` naming every tracked path to be removed, made by
  commands from the rules of 3.2, with its count and total size. The reviewer reads it. **The owner ratifies this
  paper and that list (it would be RAT-69).** That ratification is his specific authority for the removal from
  the frozen top level, which no standing rule gives.
- **P2. The tag (Claude).** An annotated tag `before_tidy_<date>` on the last commit before the tidy, pushed.
  Check: `git ls-remote` shows it on GitHub at that commit.
- **P3. The living system's part (Claude; one commit in `a_p_r_i_r_DEV/`).** Section 2: the two tools and 8 tests
  out, the helpers moved, the README's two sections shortened. Checks: the 272 tests pass; the Git tree of
  `a_p_r_i_r_DEV/src` is the same object as at the tag (`git rev-parse <tag>:a_p_r_i_r_DEV/src` equals
  `HEAD:a_p_r_i_r_DEV/src`), which shows that the engine, the updater and every method are byte for byte
  unchanged, so no fingerprint changes and no tree rebuilds.
- **P4. The removal (Claude; one commit).** `git rm` of exactly the paths of the list; the short root `README.md`;
  one new file, `ARCHIVE_INDEX.md`, saying what was removed, the tag's name and commit, and how to read an old
  file (`git show <tag>:<path>`) or an old commit id. Checks: the commit removes exactly the listed paths and adds
  or changes only the two named files; the Git tree of `results` is the same object as at the tag; so is
  `a_p_r_i_r_DEV/src`.
- **P4a. The runner's rulebook v0.9 (Claude; a candidate; the owner ratifies).** It drops what described the first
  system and its orphan marker. **One real change:** the runner's own Python. Today the rulebook names the
  top-level `.venv`. Claude proposes that the runner use the real DEV tree's Python as an interpreter only
  (always `-I -B`; never `pip`; changing nothing of DEV), as it did for T031.
- **P5. The owner pulls.** Before it: `git status` clean. After it: `git status` clean; then
  `Run_Research.bat --no-update` in DEV, which must print **no REBUILD line** (the fingerprints are unchanged on
  his PC too). QA and PROD are not touched: nothing that was removed is in them.
- **P6. The owner deletes the untracked leftovers,** from a list of full paths Claude gives, after checking that
  his backup holds them.
- **P7. Afterwards.** H-1 and H-2 are refreshed; the continuity page is cut down to what is current; the decision
  log and the continuity page are converted to CRLF (the scheme's step 7).

**To undo it:** before P6, `git revert` of the two commits brings every tracked file back, byte for byte. After P6
the untracked files come from the owner's backup.

## 5. Three points for the owner

1. **`GAIS/` now, or at the tidy?** Claude recommends at the tidy, as part of the one operation. It can go today
   if he prefers; nothing depends on it.
2. **The runner's Python** (P4a): real DEV's Python as an interpreter only, so that the top-level `.venv` can go.
   The other choice is to keep the top-level `.venv` for the runner alone, with nothing left to rebuild it from.
3. **The runner's folder is kept whole,** old task files and reports included (80 files, 1.3 MB). They are the
   evidence of every run on his PC.

END.
