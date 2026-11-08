@@VERSION@@
**Register version:** v0.26 CANDIDATE, 8 November 2026 (written by Claude; for the ChatGPT reviewer chat's check and the owner's ratification with DOC-13), recording DOC-12's installation, T022 and T021, the owner's decisions DEP-1 and GAIS-1, the Git history clean-up and its commit-ID crosswalk, the owner's later own commits, the integrated MHUP-A package's start, the Claude handover H-1 v1r10r1 (EX_157 to EX_159; RAT-26), and the DOC-13 documents (H-2 v1r10 delta, design v0.1r6, the new-method template draft 5, the repository README, and the move of superseded editions); @@SECTION@@
## DOC-12, T022, the history clean-up, the integrated package started, the Claude handover of 8 November, and DOC-13 (register v0.26)

Paths in this section are from the repository root. In this section, "this register" means register v0.26. Every commit named
here was checked by Claude from GitHub; the owner's Windows results are owner-reported. **Commit IDs: the 27 commits of 5 and 6
November 2026 listed in `exchange/HISTORY_CLEANUP_2026_11_06/commit-map.txt` were renumbered on 6 November 2026 (below); register
v0.25 and every other record written before the rewrite cite their old IDs; this register cites the new ones, with the old in
brackets where it helps.**

**DOC-12 installed (6 November 2026).** The owner installed H-2 v1r9 (with its introductory blurb as he used it) and register
v0.25, both ratified by RAT-25, at `fafa1ba` (old `377e27a`), and removed the candidate copies from `doc/`; Claude verified the
install from GitHub (`exchange/DOC12/install_doc12.py verify`: DOC12 VERIFY PASS).

**Windows evidence.** **T022 PASS** (6 November 2026; `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T022.md`, commit `e963e0e`,
old `2eb9abb`; Git SHA-256 `972d7b4e9df9d50d8ffb0eae64108f3a61bcd3527c1742d4bb56b2ce45d4e1ac`): MHUP-A slice 2 candidate v1r2,
the reviewed one, 570 tests including E2R-T12, 4 allowed symlink skips, in a task clone of `main` with the owner's then
`src/GAIS/` files present. One recorded deviation: step 8 was started detached with its output redirected, to time it (command,
arguments and folder unchanged); Claude accepted the evidence. **T021** (v1r1) was withdrawn unrun.

**The owner's decisions of 6 November 2026.**
- **DEP-1:** `pyahocorasick`, added by the owner to `DIRECT_PACKAGES` in `install_upgrade_dependencies_into_venv.bat`, is
  installed in the project venv for a GAIS test and approved as a dependency ("we keep it"). MHUP-A's environment freeze records
  it at Approval 1. Nothing in `src/` or `tests/` imports it.
- **GAIS-1:** the owner's GAIS thought experiments moved from `src/GAIS/` to the top-level `GAIS/` (owner commit `9d28b9f`, old
  `6b99029`), outside MHUP-A's code closure, with the third-party y-cruncher program untracked by `.gitignore`.

**The Git history clean-up (6 November 2026, about 11:00 to 11:30 Adelaide).** At the owner's request, led by Claude (the owner's
choice), reviewed by the ChatGPT reviewer chat (its proposal v0.1, assessment v0.1 and Gate A RECHECK PASS), and run by the owner
in gates B to E. Record: `exchange/HISTORY_CLEANUP_2026_11_06/` (`CLOSEOUT.md`, Git SHA-256
`bcd8881969190e6e3df6b8f608d2539eee05f698430f0cd7dadb6926cbe31842`; `commit-map.txt`, SHA-256
`52b27bb30b32e07cbaab14b2553d318d5071d26421bc40a222859b6302974d1c`).
- Removed from all history: `src/GAIS/OUTLANDISH_01/y-cruncher v0.8.7.9547b/` (246 files), the `ycruncher_digits` placeholder and
  two 1 MB `.bin` files; tool `git filter-repo --refs 54d161f^..main --invert-paths` with those paths.
- `main` 6b99029 -> `9d28b9f`; the tree `e8be5988e18f79d13cd1e34bbbf461f3659cca2c` is identical; 389 earlier commits keep their
  IDs; 27 were renumbered; a fresh clone went from 82.84 to 45.61 MiB packed (the same method before and after).
- **No file changed, so every document SHA-256 in every record still holds.** Only commit IDs moved: translate with
  `commit-map.txt` (old ID in column 1).
- The owner's decisions in the clean-up: Claude to lead; the loss of 15 commit signatures (all Claude's) accepted; the reviewer's
  bundle-restore test waived (a bundle of the old history is kept by the owner). The owner then cleaned his local `.git` (a copy
  kept first).

**The owner's later own commits (6 to 8 November 2026; not reviewed; recorded as facts).** OUTLANDISH work under `GAIS/`;
`.gitignore` lines for `GAIS/OUTLANDISH_01/large_artifacts/` and its configuration files; a new root `create_venv.bat` (creates
`.venv` only if it does not exist; never overwrites; installs nothing). No change under `src/`, `tests/`, `doc/` (outside his
handover copies) or the data folders.

**The integrated MHUP-A package started (owner's "go", 8 November 2026, about 18:13).** The reviewed code (slice 1 and slice 2
v1r2) was rebuilt on `main` `009c985` with the committed tools; it equals the reviewed overlay in 66 of 70 files, the other four
being `.gitignore` (the MHUP-A block now after the owner's new lines) and the three files carrying E_1 revision 3's date
(C01-EFF). A **preliminary** run of all 570 tests on Linux Python 3.13.18 and 3.15.0b4 had one expected failure on each (the test
pinning that date); the build now sets the test's date with the package date (`integrated/build_dev_integrated.sh`), and that
module then passed 8/8 on both. **The full suite on the final, date-frozen package, the mutation chains, the LF and CRLF
rehearsals and T016 are still to be run, on the final candidate** (EX_157 C03). The step 6 gate files are ten. Nothing is
installed. Work list: the H-1 v1r10r1 delta's section 7 and `exchange/CLAUDE_WEB_TOOLS/mhupa/integrated/PLAN.md`.

**R-020 (g), OPEN for the owner.** Appendix J's steps run `process_check.py` and `install_records.py`, which Claude Code's
rulebook v0.4 rule 7 forbids. Option (i): rulebook v0.5 allows only those two tools, only inside T016's synthetic, non-pushing
clone, from the package's staging folder, under the task file; option (ii): the owner runs T016's steps. The reviewer (EX_157
section 3) and Claude prefer (i), under the conditions recorded in `exchange/OWNER_REMINDERS.md`.

**The Claude handover of 8 November 2026 (RAT-26).** Because the Claude chat had grown long, Claude wrote H-1 v1r10, a working
delta on H-1 v1r8, and its blurb. The reviewer's focused documentary check **EX_157** (at `b38bd0a`) passed the crosswalk, A1's
order and the boundaries and found three corrections (C01 the test status overstated; C02 the gate count; C03 the order of work)
and four optional points; Claude applied all as **H-1 v1r10r1** (EX_158); the reviewer's recheck **EX_159** was PASS with one
editorial point (O05, stale pointers, tidied in the working files). **RAT-26 (owner, 8 November 2026, about 19:43):** the H-1
v1r10r1 delta and blurb ratified as working supplements to H-1 v1r8; installed by the owner in `doc/HANDOVER/` at `b866e42`.

**DOC-13 (this register's package; candidates for the reviewer's check and the owner's ratification).**
- **H-2 v1r10 delta and blurb:** the reviewer's insurance: a working supplement to the ratified H-2 v1r9, written by Claude from
  the records (the reviewer-rights region is not touched).
- **The design v0.1r6** (`Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r6.md`): v0.1r5 with amendment A1 folded in
  (the three passages A1 section 1 quotes, in 5.2, 5.4 and L-H2), the results source named Lotterywest-GOV where it means the
  source (LW-1), a new version line, and section 8's rulebook tool list brought to register v0.24's future action 1. Nothing else.
  Made by counted edits from the ratified v0.1r5 bytes (`exchange/CLAUDE_WEB_TOOLS/doc13/make_design_v0_1r6.py`). Once ratified,
  v0.1r6 is the design's current edition and A1 stays the ratified record of the amendment.
- **The new-method template draft 5:** the status line corrected (R-018 (c)); what MHUP-A changes for a new method once it is
  installed (release records and the release date, rosters that change only through an install, Mode H's fixed cohort) and the
  rule that a method never checks a run mode (E_1 revision 3's lesson). The code skeletons are unchanged.
- **The repository README:** a `GAIS/` row; the two venv tools among the root `.bat` files; where the handover deltas fit.
- **The move of superseded editions** (`exchange/DOC13/MOVES.txt`, 35 files): older editions that no current reading document
  names, moved into `doc/superseded/`, `doc/HANDOVER/superseded/` and `doc/contracts/superseded/`. Content unchanged; every hash
  still holds; earlier registers' path citations of those files are read with the move list. Older registers that current
  documents cite by name stay in `doc/`.
- **Not in DOC-13, on purpose:** the Claude Code rulebook v0.5 (it waits for R-020 (g)); Architecture v0.10 (with MHUP-B); R3,
  the E2R contract specification and the proposal (each when next edited; this register and register v0.24 prevail meanwhile);
  the holdout exposure record (after Q7); the next full H-1 and H-2 editions (after MHUP-A).

**Future actions (updating register v0.25's list; not authorisations).**
1. The owner's R-020 (g) decision, then the integrated MHUP-A package in the order of the H-1 v1r10r1 delta's section 7 (the final
   candidate with the date frozen; all evidence on it; the review request at the next free EX number).
2. Register v0.27 records the integrated package's review and install, rulebook v0.5, and anything DOC-13's review changes.
3. Unchanged from registers v0.24 and v0.25: MHUP-B and its timing route; Q7 before Approval 2; the owner's backup confirmation
   and POC-suite choice at MHUP-A's approval; WF-1C; the method waves; KISS-1 when asked.

**Out-of-date statements (register v0.26).** This register prevails, and the files are not edited:
- **Register v0.25 and records written before the rewrite:** commit IDs of the 27 renumbered commits: read with `commit-map.txt`.
- **Register v0.25, "T021 and T022 PENDING" and R-020 (e) and (f) as open:** settled above.
- **H-2 v1r9 sections 0 and 6:** read with the H-2 v1r10 delta (once ratified).
- **H-1 v1r10r1 section 2:** its pointer "section 7, item 8" means section 7, item 7 (EX_159 O05; for the next full H-1 edition).
- **Design v0.1r5:** superseded by v0.1r6 once ratified; until then v0.1r5 with A1 governs, as before.
- **The template draft 4:** superseded by draft 5 once ratified.

| Document (path) | Author / check | Status and Git-content SHA-256 (LF) |
|---|---|---|
| `doc/RATIFICATION_REGISTER_v0_25.md` | Claude; checked by the reviewer (EX_153, EX_155) | OWNER-RATIFIED 6 Nov 2026 (RAT-25); installed at `fafa1ba`; superseded by this register once ratified; `2ef9d17cfbc76c556e00d659677e411686c60aab263e1b0f0ef002930ee6d874` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v1r10r1_delta.md` | Claude; checked by the reviewer (EX_157, EX_159) | OWNER-RATIFIED 8 Nov 2026 (RAT-26) as a working supplement to H-1 v1r8; installed at `b866e42`; `e9cede8470aff5d05af1785702321be2b25b5c912a35e9ce636929efd2157c2f` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v1r10r1_introductory_blurb.md` | as above | as above; `f3c6bea057c29cf66c053bf2e55b40919d26715d3da1cdf8379c1eaf29122d41` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r10_delta.md` | Claude, from the records | DOC-13 candidate; `6421fc5a865c61646478843e45e23d569ce8e8db5bfcf1e5b882be13af5a6b78` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r10_introductory_blurb.md` | Claude | DOC-13 candidate; `a427d7c36f3f601e1ebff51256f62c558e6677b7746d4bfe501ad60416433f94` |
| `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r6.md` | Claude, counted edits from v0.1r5 (`e5fb491c...`) | DOC-13 candidate; `eb0e8070e53ebc9299273f6e4ddf1bb244f4847b922ab232e34b7c7bd71884f4` |
| `doc/METHOD_TEMPLATE/README.md` (draft 5) | Claude | DOC-13 candidate; `b32eb0f55710cc855a84321a79c00c22635dce3e0cd75ab476d890529d82c487` |
| `doc/METHOD_TEMPLATE/METHOD_SPECIFICATION_TEMPLATE.md` (draft 5) | Claude | DOC-13 candidate; `54d15e8f1fe42bdc51b87a57cfc1869bb3693465d5a88ec84cc3e543ddc33661` |
| `doc/METHOD_TEMPLATE/CHANGES.md` (draft 5) | Claude | DOC-13 candidate; `a955cc2e769cd227da7fcf75f03823bae64e1eba133033076dd4c1c8e8c3419f` |
| `README.md` (repository root) | Claude | DOC-13 candidate; `030de52691b04e84f8e03f3926c0cfbbf50bddc95517402ff6e9d6953d222d05` |
| `exchange/HISTORY_CLEANUP_2026_11_06/commit-map.txt` | git-filter-repo's own map | The crosswalk for the 27 renumbered commits; `52b27bb30b32e07cbaab14b2553d318d5071d26421bc40a222859b6302974d1c` |

@@STATUS@@
- **Current status (register v0.26 CANDIDATE; read this first).**
  - Since register v0.25 no reviewed code package was installed and no real-data run, results update, report, holdout opening or
    Mode H took place. MHUP-A is reviewed in slices and passed on Windows (T022) but is not installed; its integrated package is
    being built (preliminary evidence only so far).
  - Commit IDs of 5 and 6 November 2026 changed on 6 November (the crosswalk above); no file changed.
  - The owner's decision R-020 (g) is open; everything else waits on the integrated package's review and the owner's approvals.
