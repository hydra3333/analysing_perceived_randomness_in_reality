## The integrated MHUP-A package, rulebook v0.5, the install of 13 November 2026, and design v0.1r7 (register v0.27)

Paths in this section are from the repository root. In this section, "this register" means register v0.27. Every commit named
here was checked by Claude from GitHub; the owner's Windows results are owner-reported, with Claude Code's reports in
`CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/`. This section records decisions already taken and events that happened; it makes
no new decision.

**The integrated package's development (9 to 11 November 2026).** Work list `exchange/CLAUDE_WEB_TOOLS/mhupa/integrated/PLAN.md`.
The owner's records and the reviewer's focused reviews are in `exchange/HO2_2026_11_10/`: the HO-2 closure and the GO for
items 1 and 2 (10 November); the items 1-2 review and the owner's decisions after it (N1: `-text` for the install records);
the item 3 review (N5, F2) and its follow-up (N4b, N5-C01/C02, F2-C04, REC-C01). The owner's decisions in this round: R-020
(g) option (i) (8 November; recorded in register v0.26 as open, now settled); N1; N4 and N4b (`-text` for three byte-checked
files); N5 option A (Appendix J step 10 on a barrier-free copy); the reviewer's point A (the release-record tool refuses
unless U is held by the package and E is gone); abandon-and-rebuild after a STOP at step 13 or 17 (REC-C01).

**RAT-28: rulebook v0.5 and the Appendix J amendments (owner, 11 November 2026, 19:31).** Drafts at `5e1a704`; the reviewer's
focused review (T016-C01 to C05, J-REVIEW); r2 at `19e45ff`; the reviewer's R-2 focused PASS. The owner's words: "I RATIFY the
substance of rulebook v0.5 and the proposed Appendix J amendments J-1 through J-4, including the two section 4.3 wording
corrections", the reviewer's two wording corrections W01 and W02 "approved for incorporation without another review", and the
T016 task design accepted in principle. Record:
`exchange/HO2_2026_11_10/MHUPA_Owner_Ratification_Rulebook_v05_AppJ_2026_11_11.md`. The final documents differ from r2 only by
their labels and W01/W02 (`exchange/CLAUDE_WEB_TOOLS/mhupa/t016/final/R2_TO_FINAL.diff`, at `398c0a2`). The same evening the
owner decided that restore after a STOP from Appendix J step 6 on is written per case (for the state the output shows,
reviewed, owner-approved), and gave the go for the freeze.
- **Rulebook v0.5** (`CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`): new section 2A, the one allowance for TASK_T016 (it ended
  with T016's report); rule 1 names Lotterywest-GOV (R-017); rule 7 adds `create_venv.bat`.
- **The Appendix J amendments** (`exchange/CLAUDE_WEB_TOOLS/mhupa/t016/final/APPENDIX_J_AMENDMENTS_RATIFIED.md`): J-1 step 10
  runs the suite on a barrier-free copy with only the six development data files; J-2 the step 10 negative tests; J-3 and J-4
  abandon and rebuild after a STOP at step 13, or at step 17 after the release commit (exceptional recovery only); section 4.3:
  40 baseline entries per game, and the install record's time is the time it is written. Folded into **design v0.1r7** (DOC-14,
  below).

**The freeze and the gates (11 to 13 November 2026).** Gate list:
`exchange/CLAUDE_WEB_TOOLS/mhupa/t016/final/INSTALLATION_STEPS_PROPOSED.md`. Each gate had the owner's own go.
- **Gate A, the freeze** (EX_163, `d4af894`): `MHUPA_Install_v1.zip`, SHA-256
  `9d8b74657880917bf8a367b083c5e5926bc6803ee989f74c934afdf98156cf76`; manifest SHA-256
  `8ad51e769dfb03592241fe1965b493fb605176620c8c93bd3f8a8b3de8a324b5`; base `c48ac3c`; E_1 revision 3's `effective_date`
  2026-11-11 (C01-EFF). It differs from the reviewed draft only by the date, the status and fingerprints, and the instructions'
  labels and restore wording. **EX_164:** the reviewer's PASS; the member hashes, draft beside frozen, at `60533e4`.
- **Gate B:** rulebook v0.5 and `inbox/TASK_T016.md` installed by Claude at `760e0c6`.
- **T016 PASS** (reports `0035a22` and `3f348a1`): Appendix J steps 0-18 in a task clone on Windows, the suite 571/571 with
  four symlink skips, the three expected refusals, F2 rows 5, 6 (the real venv: 27 distributions, no orphan), 7 and 10. Two
  disclosed recording deviations.
- **Gate D:** the owner's settings commit `138e185` adds five deny lines (F1).
- **Gate E:** F2 rows 8 and 9 PASS at the real root, run by the owner (record at `5211a42`).
- **Gate F, the live install (13 November 2026):** every Appendix J step 0-19 gave its expected line; the package commit
  `2860e86` and the release commit `effc179`, pushed by the owner. Claude verified it from GitHub (`81bc689`): the 71 package
  files equal the frozen package; no barrier committed; `RECORDS PASS: 1 install record(s), 2 release record(s), 80 released
  unretired entries`. E_1 revision 3 is released for both games; its release record's local date, 2026-11-13, is its release
  date for MH-1's rule.

**The post-install test fix (13 November 2026).** The whole suite on the installed `main` failed 8 of 571: two test modules
copied the repository's live install records and assumed the state before the install. The test-only fix r1 (`0a164fe`)
passed the reviewer (EX_165) and was run on Windows by TASK_T023 (EX_166's two corrections applied; in the inbox at
`95c35ca`; report `179699c`, PASS, 571/571). The owner committed the two files at `87c4219`; Claude verified both blobs against
the reviewed SHA-256 values. Not a code package: the files are outside the code closure and release nothing (EX_165).

**The owner's decisions of 13 November 2026** (record: `exchange/DECISIONS/OWNER_DECISIONS_2026_11_13_MHUPA_CLOSED.md`):
MHUP-A accepted and closed; (1) DOC-14, this register and design v0.1r7, documents the ratified decisions and is installed after
the owner's approval; (2) future isolated install rehearsals also run the whole suite in the post-release state, designed with
the next package, with no second suite run added to the live procedure; (3) MHUP-B is the next substantive priority: an
assessment first, no substantial design or coding before the owner authorises it; (4) KISS-1 stays deferred, with its agreed
scope (including method-registry usability and operational simplification), until the owner starts it.

**DOC-14 (this register's package).** Register v0.27 and design v0.1r7, written by Claude from the records; approved by the
owner on 13 November 2026 as documentation of decisions already ratified (not a new ratification). Design v0.1r7 is v0.1r6 with only RAT-28's
amendments in their ratified wording, by counted edits (`exchange/CLAUDE_WEB_TOOLS/doc14/make_design_v0_1r7.py`).

**Future actions (updating register v0.26's list; not authorisations).**
1. MHUP-B: the assessment first; its design only on the owner's authorisation; a post-release full-suite run in its
   rehearsals (decision 2).
2. Unchanged from registers v0.24 to v0.26: Q7 before Approval 2; the owner's backup confirmation and POC-suite choice at
   MHUP-A's approval; the owner's Approvals 1 to 4 per game, each separately; WF-1C; the method waves; the next full H-1 and H-2
   editions; KISS-1 when the owner asks.

**Out-of-date statements (register v0.27).** This register prevails, and the files are not edited:
- **Register v0.26, "Current status" and future actions 1 and 2:** done (above).
- **Design v0.1r6:** superseded by v0.1r7. It stays in `doc/` because ratified records cite it by name.
- **Rulebook v0.4:** superseded by v0.5 (installed at `760e0c6`).
- **Files in `exchange/` labelled DRAFT for MHUP-A, rulebook v0.5 or T016:** superseded by the final and frozen files named above.

| Document (path) | Author / check | Status and Git-content SHA-256 |
|---|---|---|
| `doc/RATIFICATION_REGISTER_v0_26.md` | Claude; checked by the reviewer (EX_160, EX_161) | OWNER-RATIFIED 8 Nov 2026 (RAT-27); superseded by this register; `366e966d6584d86681891eb84fe5363ae94ecac00f2943daab8fbc01ca125414` |
| `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md` | Claude, counted edits from v0.1r6 (`7332dd6c...`) | DOC-14, OWNER-APPROVED 13 Nov 2026; records RAT-28; `@@DESIGN_SHA@@` |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (rulebook v0.5) | Claude; checked by the reviewer (R-2 PASS of `19e45ff`) | OWNER-RATIFIED 11 Nov 2026 (RAT-28); installed at `760e0c6`; `fa7a5fe229be832880cda4704ed9e7d27af2f4b9462464f7af262e540acd5200` |
| `exchange/CLAUDE_WEB_TOOLS/mhupa/t016/final/APPENDIX_J_AMENDMENTS_RATIFIED.md` | Claude; as above | OWNER-RATIFIED 11 Nov 2026 (RAT-28); `6bdeb16405cf29b2bbef9fc5c3e1915741ac5ede6a0108869b0a7bda547301e9` |
| `exchange/EX_163_Claude/MHUPA_Install_v1.zip` | Claude; checked by the reviewer (EX_164) | The frozen MHUP-A package, installed 13 Nov 2026; `9d8b74657880917bf8a367b083c5e5926bc6803ee989f74c934afdf98156cf76` |

