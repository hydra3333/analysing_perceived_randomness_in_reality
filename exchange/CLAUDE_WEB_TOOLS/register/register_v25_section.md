@@VERSION@@
**Register version:** v0.25 CANDIDATE 2, 6 November 2026 (written by Claude; NOT OWNER-RATIFIED: the ChatGPT reviewer chat ended on 6 November 2026; the new reviewer chat checked candidate 1 in its takeover, EX_153, and candidate 2 applies its corrections TAKEOVER-C01 to C05, C01 for its RECHECK), recording DOC-11's installation, the completion of the staged Claude handover (HO-2) with the owner's decisions HO2-A and Q9-E1 to Q9-E4, the direction document v0.3r1, the MHUP-A code reviews in two slices (EX_141 to EX_152) with the owner's decisions C01-EFF, A1-B and IIIB-1 and the ratification of design amendment A1 (A1-R), the owner's Windows runs T018 to T020, the Claude Code rulebook v0.4 and its clone tool v0.4, the owner's own commits of 5 and 6 November 2026, and the end of the reviewer chat with the emergency handovers; 
@@SECTION@@
## DOC-11 installed, HO-2 completed, MHUP-A reviewed in two slices, amendment A1, and the reviewer chat's end (register v0.25)

Paths in this section are from the repository root, except those beginning `HANDOVER/` or naming a design, register or
direction document, which are under `doc/`. In this section, "this register" means register v0.25, "the design" means
`Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r5.md` as amended by A1, and "MHUP-A" means the first MHUP-1 code
package.

**Who verified what.** Every commit named here was checked by Claude from GitHub. The owner's Windows results are
owner-reported. **This edition has not been reviewed:** the reviewer chat that reviewed every round below ended before this
edition was written. Its findings are quoted from its own committed messages.

**DOC-11 installed; the staged Claude handover (HO-2) completed (4 November 2026).**
- **The install:** the owner installed DOC-11 at `3d4fa3c`, comprising register v0.24, H-1 v1r8 and its blurb, the ratified
  design v0.1r5 and the direction document v0.2r1. Claude verified it from GitHub (EX_138, `20a3f40`).
- **The takeover:**
  - the replacement Claude chat read and verified the package and gave its first reply;
  - the reviewer chat asked questions Q1 to Q9, which the new chat answered without seeing the reviewer's assessment;
  - all nine were assessed PASS;
  - Q9 led to the direction document v0.3 and then **v0.3r1**: reviewer RECHECK, then focused recheck PASS.
  The records are EX_139 and EX_140 (`2061055`), with
  `exchange/EX_140_Claude/HO2_Owner_decisions_and_completion_2026_11_04.md`.
- **Direction v0.3r1 ratified and installed** by the owner (4 November 2026, about 16:35 Adelaide; document-only route) at
  `dfc2d13`, comprising:
  - `Direction_for_operational_procedures_v0_3r1.md` `9c781716b8313e052ec29203e79cf4745e3c172bc587e96a1fe1f4be2c84b985`;
  - `Direction_for_operational_procedures_v0_2r1_to_v0_3r1.diff` `ddf28688a981fd701f8b6c1c88e9be73f7d90d5eefca1206b000c086d58b4596`;
  - `review/Independent_ChatGPT_HO2_Q9_and_Direction_v0_3_RECHECK.md` `506b22a9127d7ec0a79322e2f5bc431494a0b35ae24457017c1ccb87a96985ca`.
  Claude verified all three blobs. v0.2r1 is kept as history.
- **Q9-E1 to Q9-E4** (owner, 4 November 2026, about 16:36, "yes to all recommendations stated here"; the full text is in the
  EX_140 member named above):
  - **E1:** complete historical coverage is a deferred objective. Every method eventually gets retrospective forecasts for every
    applicable past draw, including the ten original holdout draws. A later method's holdout forecasts come only through a
    separately designed, reviewed and owner-approved process. They are development evidence only, never part of the sealed Mode
    H study and never pre-draw.
  - **E2:** one consolidated owner-facing report, keeping development, Mode H, CATCH-UP and PROSPECTIVE separate, with sample
    sizes shown, comparisons on common draws and no misleading single score. It is designed with the cross-batch report after
    WF-1C.
  - **E3:** deterministic recalculation for a new report is not by itself a second accepted score. The actual WF-1B behaviour
    is to be verified in the cross-batch report's design, and accepted records are never altered.
  - **E4:** after GOAL-1 and the required installs and approvals, the owner's deliberate run of the reviewed
    `Run_Weekly_Session.bat` is that week's authorisation. This excludes unattended scheduling, unusual recovery, bypassing a
    STOP, and anything outside the approved scope. The results updater stays a separate operation.
- **HO2-A** (owner, 4 November 2026, about 16:37):
  - HO-2 is declared successfully completed;
  - the replacement Claude chat is accepted as primary designer and coder;
  - option (a), resumption of normal work, within the limits the decision lists;
  - the experienced reviewer chat stays in role.
  The owner's further decisions of that day on retries after a STOP and on interrupted sessions are carried as reminder R-018
  (a) and (d). They go into MHUP-B's checklist and the next full H-1 edition.

**MHUP-A: two review slices, then one integrated package (owner, 4 November 2026).** The owner chose to have MHUP-A's code
reviewed in two slices (R-2 HIGH each), followed by **one integrated install package** with its own full review. A slice PASS is
a review checkpoint only; it is not an install candidate.

**Slice 1** (version-2 master rules, E_1 revision 3, one data kind, the binding and ticket gates, barrier P):

| EX (commit) | Content | Outcome |
|---|---|---|
| EX_141 (`32cc0e3`; zip `83c4a74dc21044895d53670d1723d9b7bc2b537f14d41ef676584d0c4fe7cae9`) | Candidate v1: 506 tests in the suite, 505 run and passed on each of Python 3.13 and 3.15.0b4 (E2R-T12 excluded; EX_153 TAKEOVER-C03); 67 mutants (61 caught, 6 equivalent) | |
| EX_142 (inside `exchange/EX_143_Claude/`) | Review | **RECHECK.** B01: the official request's pin was not bound to the frozen plan or session pin. B02: invalid weekly evidence could be read as absent evidence. B03: an INIT-only leniency was wider than the ratified closed ledger grammar. C01 to C03. |
| EX_143 (`5573035`; zip `4ac92eb491b598dad9dcd17dccdc0d178171bfe73f92d12857f01f8178733c18`) | Candidate v1r1: 507 tests in the suite, 506 run and passed on each Python (E2R-T12 excluded); 87 mutants (80 caught, 7 equivalent) | |
| EX_144 (inside `exchange/EX_145_Claude/`) | Review | B01 PASS; two narrow residuals: blank JSONL lines; strict CSV quoting |
| EX_145 (`3d825b3`; zip `03a8ce832839616e5f7b0e457b40419bcd58f14004e701a4e7f21310a91409f9`) | Candidate v1r2: 507 tests in the suite, 506 run and passed on each Python (E2R-T12 excluded; all 507 ran on Windows in T018); 90 mutants (81 caught, 9 equivalent, 0 survived) | |
| EX_146 (`8aa16c3`) | Review | **slice 1 PASS** (review checkpoint only). Its watchpoints for slice 2 and the integrated package are carried as reminder R-019 (a) to (e). |

- **C01-EFF** (owner, 4 November 2026; EX_142 C01, EX_143): E_1 revision 3's `effective_date` is the integrated package's actual
  preparation date. It is set before that package's final review freezes the registry bytes and digests, and it is never the
  admission or release date. The release record alone dates a release.

**Slice 2** (the Mode H batch kind and families, `src/evaluation/Method_Mode_H.py` and `mode_h.py`, the closure and environment
freeze, the install and release records tool, `src/package_tools/process_check.py`, the results updater v0.2, the launchers, the
freeze-before-outcome rule, and the Claude Code rulebook v0.4):

| EX (commit) | Content | Outcome |
|---|---|---|
| EX_147 (`2eb6dfb`; zip `a5ac750f5699b3a5f99bfda6d5b67f3aa85a6754ccaecef7a61f8cbb26d1ef25`) | Candidate v1: 561 tests on both Pythons; 85 mutants (76 caught, 9 equivalent) | |
| EX_148 and its evidence supplement (`b45cb0d`) | Review | **RECHECK.** B01: the per-pair score ledger against design 5.2 and 5.4. B02: a partial three-file report. B03: the roster against the registry and the release records. B04: a ledger accepted without full validation. C01: non-Python process ancestors. (iii-b): a corrective scoring run after the seal. (vi). (ix): COMMITTED PASS, accepted as conditional. C02: evidence status. Also: marking a mutant equivalent because no test plants its fault is test non-detection, not equivalence. |
| EX_149 (`534af84`; zip `b89513fddba66e62e058c4a54f812b51cc2d1f41ef2f9d11b432aa1de1b13b46`) | Candidate v1r1 with the A1 draft: 569 tests; 99 mutants (85 caught, 14 equivalent with printed reasons) | |
| EX_150 (`c498103`) | Review | B02 to B04 and C01 **PASS**; A1 reviewed favourably; one new blocker, **B05**: a resumed scorer bound neither to the scoring plan `SCORING_STARTED` froze nor to a complete `SCORE_COMPLETE` |
| EX_151 (`8b5acaa`; zip `327aaf7413b39eb5249a7df62b1f14bba7655810d5accb55bb7518866828a094`; inner candidate `MHUPA_Slice2_Review_v1r2.zip` `67701220d761924cc9ee1703c613cb3bf48b8f978050115de9ef242d60b751bc`) | Candidate v1r2: B05 corrected; 570 tests on both Pythons; 5 targeted mutants caught | |
| EX_152 (`f7d90da`) | Review | **slice 2 PASS.** It permits preparing the one integrated MHUP-A install candidate for its own review. It is not an integrated PASS, an install authorisation, or authority to read holdout outcomes or run on real data. |

- **The candidate's base:** the v1r2 candidate's `overlay/` holds slice 1 and slice 2 together: 70 files against the base tree,
  main at `2061055`. It removes `src/results_master_v0_1.py`, which is replaced by v0.2.
- **The reviewer's evidence boundary** (stated in EX_146, EX_150 and EX_152): the reviewer inspected the full packaged source
  statically, verified the artefact identities, and reproduced each candidate-to-candidate diff byte for byte. It **did not
  execute** the tests or the mutation runner. The suite and mutation results are Claude's (Linux) and the owner's (Windows).
- **The owner's decisions during slice 2 (5 November 2026):**
  - **A1-B:** EX_148 B01 to be resolved by route (B), the one-step atomic score ledger, through a design amendment.
  - **IIIB-1:** the corrective scoring run after the Mode H seal is deferred to MHUP-B, with its route stated (A1 section 6).
  - **A1-R (A1 ratified):** after EX_150 the owner wrote "i hereby authorise and ratify that A1". The ratified record is
    `exchange/MHUP1_design_amendment_A1_RATIFIED.md` (`c498103`; Git blob SHA-256
    `f2506c02297808ea260d5fa3a5d18f79069d2a317004e85683271129383db4b8`).
    - Its sections 1 to 5 replace **only** the quoted per-pair provisions of the design's sections 5.2 and 5.4 and Appendix
      L-H2. In order: the scorer reads the holdout outcomes once and computes the complete ledger; publishes it atomically,
      create-only; validates the published ledger as it stands; and only then writes `SCORE_COMPLETE` (with the ledger's
      digest), resumes or publishes the report, and seals. The recovery states are those of A1 section 4: no ledger; the
      complete ledger without `SCORE_COMPLETE`, where no outcome is read and a refused ledger is a STOP; and after
      `SCORE_COMPLETE`. A resumed scorer is bound to its frozen scoring plan and to a complete `SCORE_COMPLETE` record
      (EX_153 TAKEOVER-C01).
    - Section 6 is the MHUP-B route for a corrective scoring run. It authorises no implementation in MHUP-A.
    - Section 7 is explanatory.
    - EX_152 section 3 confirmed that the ratified text's sections 1 to 7 equal the reviewed draft.

**The owner's Windows runs (Claude Code, read-only task clones; owner-reported, reports committed by the owner):**

| Task | Candidate | Result | Report commit |
|---|---|---|---|
| T018 | slice 1 v1r2, 507 tests | **PASS**. The committed real ledgers also pass the full ledger grammar. | `110eb41` |
| T019 | slice 2 v1 | **STOPPED correctly at step 5**: its command lines named paths that the owner's `.claude/settings.json` denies by their text | `56abdf4` |
| T020 | slice 2 v1, 561 tests | **PASS**: 4 allowed symlink skips, 16 minutes 55 seconds | `cba73e5` |
| T021 | slice 2 v1r1 | **PENDING** at the date of this edition | |
| T022 | slice 2 v1r2 | **PENDING** at the date of this edition | |

**Claude Code tooling** (Claude's commits in `CLAUDE_CODE_WORKING_FOLDER_TREE/` and `exchange/`):
- **Rulebook v0.4** (`CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`, committed at `87bf389`; Git blob SHA-256
  `a4c4cbfcbe783ba4063cfbc49e1dfc9582ccd052ae4b5f5453af001d4fecdc8a`; reviewed within slice 2):
  - rule 7 names, ahead of their installation, the MHUP-A programs the runner never runs: `Run_Evaluation.bat`, the Mode H
    command and its module, the walk-forward driver's Mode H plan mode, the process tool, the records tool and every version of
    the results updater.
- **The clone tool `tools/cc_clone.py` v0.4** reads denied paths from a plan file (`overlay --plan`, `verify-overlay`).
- **Claude's checker `exchange/CLAUDE_WEB_TOOLS/check_task_commands.py`** checks a task file's command lines against the deny
  list before it is sent.
- **Still to come:** the owner's `.claude/settings.json` deny lines for the MHUP-A programs (register v0.24, future action 1) are
  the owner's edit, made with MHUP-A's install. Naming Lotterywest-GOV in the rulebook's rule 1 (register v0.24 future action 1;
  reminder R-017) is also still to do. Rule 1 already forbids contacting any lottery website.

**The owner's own commits (5 and 6 November 2026; not reviewed; not part of MHUP-A).** `f1883df`, `653b80c`, `54d161f`,
`ece780a`, `456cefd` and `43dd069` (with merges `baf60fb` and `442597a`) added:
- `src/GAIS/` and `doc/GASI_thought_experiments/outlandish_01/`: the owner's "outlandish" thought experiments;
- three `.gitignore` lines for very large GAIS files;
- in `f1883df`, the package **`pyahocorasick`** in `DIRECT_PACKAGES` of `install_upgrade_dependencies_into_venv.bat`.

This register records these as facts only. They are the owner's work, not reviewed. Whether the dependency line is an approved
dependency change under the rules (H-1 section 2; register v0.24, "no ... dependency upgrade without the owner's separate
approval") is **OPEN for the owner** to state. The integrated MHUP-A package must allow for all three (reminder R-020 (d) to
(f)):
- the candidate's whole-file `.gitignore` predates the owner's lines;
- the environment freeze records whatever the venv holds at Approval 1;
- the code closure covers `src/`, and with it `src/GAIS/`.

**The reviewer chat's end and the emergency handovers (6 November 2026).**
- The ChatGPT reviewer chat that held the role from 30 October 2026 reached its conversation limit on 6 November 2026 **without
  writing its own handover**.
- On the owner's instruction, Claude wrote the following in `exchange/HANDOVER_2026_11_06/`, committing each in order of
  criticality (`c84e2dc`, `957a452`, `2660e46`, `dbde41f`):
  - H-1 v1r9, a delta on H-1 v1r8, with its blurb;
  - the owner's reminders and roadmap (R-016 overtaken; R-020 (d) to (f); R-022);
  - **H-2 v1r9 CANDIDATE**, reconstructed from H-2 v1r8 and the reviewer's own messages EX_142 to EX_152, with its blurb. Its
    builder asserts that the reviewer-rights region (`## 2.` to just before `## 4.`) is unchanged: 7,676 bytes, SHA-256
    `70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db`.
- **H-2 v1r8 stays the operative reviewer handover** until the owner ratifies a successor.
- A new reviewer chat's first task is its takeover check of H-2 v1r9 and of this register (reminder R-022).
- **The new reviewer's takeover (EX_153, 6 November 2026):**
  - The new ChatGPT reviewer chat accepted the role on the operative H-2 v1r8.
  - It verified that the reviewer-rights region and sections 1, 4 and 5 of H-2 v1r9 equal v1r8's (canonical LF).
  - It found no narrowing of its independence.
  - It found five documentation corrections, TAKEOVER-C01 to C05 (C01, the order of A1's ledger publication and validation,
    for RECHECK; the others FIX AND PROCEED), plus one optional line-ending qualification, O01. Candidate 2 of H-2 v1r9 and of
    this register applies them (Claude's EX_154).
  - The candidates copied into `doc/` by the owner at `929eff5` are candidate 1. They become authoritative only after ratification.
- **Claude's verification questions to the new reviewer** (EX_154, as the reviewer's questions Q1 to Q9 were for Claude in HO-2)
  are pending at the date of this edition. The owner's acceptance of the new reviewer follows them.
- Register v0.24's future action 8 said a ChatGPT reviewer handover would be "considered only after" HO-2. The reviewer chat's
  end has overtaken it.

**Future actions (updating register v0.24's list; not authorisations).**
1. **The new reviewer's takeover** (R-022): its check (EX_153), the corrections and its RECHECK of TAKEOVER-C01, its answers to Claude's
   verification questions (EX_154), then the owner's acceptance, all before the integrated MHUP-A package is sent.
2. **The owner's T021 and T022 reports.** A Windows failure is corrected before integration.
3. **The integrated MHUP-A install package** (register v0.24 future actions 1 and 2, now with A1 cited). It contains:
   - the installer and the verifier (design Appendix J steps 0 to 19, including the verifier's `released` phase);
   - the LF and CRLF rehearsals and T016;
   - E_1 revision 3's `effective_date` set to the preparation date (C01-EFF);
   - the package manifest's `release_entries` naming E_1 revision 3 for both games (R-020 (a));
   - the environment-freeze orphan rule (R-020 (b));
   - the owner's POC-suite rerun choice (R-020 (c));
   - the rebase onto the current main and the owner's own commits (R-020 (d) to (f));
   - R-019 (a), (d) and (e), checked in the assembled behaviour;
   - EX_148 (ix): the verifier proves both commits, the barrier order, and that the records agree with the repository.

   Its review assesses the assembled behaviour; it is not inferred from the slice PASSes (EX_152 section 5).
4. **MHUP-B** (register v0.24 future action 3). It is installed either before Approval 1, or only after a game's Mode H is
   sealed, and never while a holdout is opened and unsealed (design 4.4). The owner chooses the route, and the integrated install
   plan states it (EX_153). It adds:
   - the full shape of `FREEZE_LINE_V1` (R-019 (b));
   - the `FINAL_NEXT_DRAW`/`CATCH_UP` binding mutant re-run (R-019 (c));
   - A1 section 6's corrective scoring route;
   - Q9-E4 and R-018 (a) and (d) in its checklist.
5. **The next documentation package:**
   - this register, ratified after review;
   - the full H-1 and H-2 editions (folding in the v1r9 delta and candidate);
   - the design's next edition citing A1 and naming Lotterywest-GOV;
   - the template README's draft number (R-018 (c)).
6. **Unchanged from register v0.24:** future actions 4 to 7 and 9, and Q7 (OPEN).

**Out-of-date statements (register v0.25).** This register prevails, and the files are not edited:
- **The design v0.1r5, sections 5.2 and 5.4 and Appendix L-H2:** the per-pair score ledger provisions are replaced by A1 sections
  1 to 5.
- **Register v0.24, future action 8, and H-1 v1r8's blurb** ("the reviewer is not changing"): overtaken by the reviewer chat's
  end (above).
- **H-2 v1r8, sections 0 and 6:** checkpoint facts stop at 1 November 2026. Read H-2 v1r9 CANDIDATE's sections 0 and 6 for the
  facts, subject to the new reviewer's check; H-2 v1r8 remains the operative text of the reviewer's rights and procedure.
- **Register v0.24, "Current status":** extended by this section.

| Document (path) | Author / check | Status and Git-content SHA-256 (LF unless stated) |
|---|---|---|
| `RATIFICATION_REGISTER_v0_24.md` | Claude; checked by the reviewer chat (EX_133 to EX_136) | OWNER-RATIFIED 4 Nov 2026; installed at `3d4fa3c`; superseded by this register once ratified; `9d9fde67961d76fcc4823e97ac339c12e8b7e68ba309167652bd2c568f5c81ae` |
| `Direction_for_operational_procedures_v0_3r1.md` | Claude; reviewer RECHECK, then focused PASS | OWNER-RATIFIED 4 Nov 2026; installed at `dfc2d13`; `9c781716b8313e052ec29203e79cf4745e3c172bc587e96a1fe1f4be2c84b985` |
| `exchange/MHUP1_design_amendment_A1_RATIFIED.md` | Claude; reviewed by the reviewer chat (EX_150, EX_152) | OWNER-RATIFIED 5 Nov 2026 (A1-R); a record in `exchange/`, to be folded into the design's next edition; **stored CRLF bytes** (Git stores this file with CRLF; not reformatted; EX_153 TAKEOVER-C04) `f2506c02297808ea260d5fa3a5d18f79069d2a317004e85683271129383db4b8` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (rulebook v0.4) | Claude; reviewed within slice 2 (EX_147 to EX_152) | In force for the runner since `87bf389` (5 Nov 2026); `a4c4cbfcbe783ba4063cfbc49e1dfc9582ccd052ae4b5f5453af001d4fecdc8a` |
| `exchange/HANDOVER_2026_11_06/` (H-1 v1r9 delta, H-2 v1r9 CANDIDATE, both blurbs, README) | Claude, 6 Nov 2026 | Candidates, not ratified, not reviewed; identities in that folder's README |

@@STATUS@@
- **Current status (register v0.25 CANDIDATE; read this first).**
  - Since register v0.24 no reviewed code package was installed (nothing of MHUP-A, no production-science code), and no
    real-data run, results update, report, holdout opening or Mode H took place. The owner's own unreviewed additions, `src/GAIS/`
    and the `pyahocorasick` line, are recorded in the section above. They matter to MHUP-A's code-closure and environment
    accounting (EX_153 TAKEOVER-C02).
  - MHUP-A's two review slices have PASSED (EX_146, EX_152) and amendment A1 is ratified. Neither authorises an install or a
    run.
  - Next, in order:
    1. the new reviewer chat's takeover check;
    2. the owner's T021 and T022 reports;
    3. the integrated MHUP-A install package and its own review;
    4. its rehearsals and the owner's install;
    5. MHUP-B;
    6. the owner's Approvals 1 to 4 per game, each separately.
