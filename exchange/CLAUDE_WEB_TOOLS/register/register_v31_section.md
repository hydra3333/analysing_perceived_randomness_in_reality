## Mode H in both games, the readings, D5, the approach of 16 November 2026 and the MHUP-B design supplement (register v0.31)

Paths in this section are from the repository root. In this section, "this register" means register v0.31. Every commit named
here was checked by Claude from GitHub, and every hash was computed from Git's stored bytes. This section records decisions
already taken and events that happened; apart from RAT-34 below, it makes no new decision, and nothing in it authorises a
check, a run, a package or an install. The owner's exact words are in `exchange/DECISIONS/DECISION_LOG.md`, entries 7 to 61.

**The RAT-32 install.** H-1 v3, its blurb and register v0.30 were installed by the owner at **`5b4df41`** (15 November 2026,
about 18:06; entry 7): ZIP PASS, POST PASS, COMMITTED PASS; Claude's check from GitHub found exactly the three files with
their ratified SHA-256 values.

**The streamlined arrangement for Mode H** (the owner and the reviewer, 15 November 2026; EX_193, extended to Powerball by
EX_198): the owner gave his own go for each step; Claude checked every output before the next; the reviewer reviewed each
game's whole record afterwards, or at any STOP. A STOP stayed a STOP. Every owner CMD window is stored in `exchange/RUNS/`.

**The official-page check: a STOP, its cause and r2.** The read-only check of the official results page (prerequisite 3)
stopped on 15 November 2026 (entry 9): check r1 compared the draw numbers in page order with an oldest-first list, and the
real page lists the newest first. The cause was Claude's (every stand-in page had been oldest-first); nothing irreversible
had happened. The owner looked at both pages himself (entry 10: 26 draws each, newest first, no paging). Check **r2**
compares the numbers as a set, each once, with a 26-draw window
(`exchange/CLAUDE_WEB_TOOLS/modeh_readiness/gov_fetch_parse_smoke.py`,
Git blob `449b5cd3a974d34488eb1522b5a75809e8d212b1`; EX_194; the reviewer EX_195); evidence that the installed updater gives
identical records for oldest-first, newest-first and shuffled pages is in the same folder. r2: PASS (entry 11). The
readiness sheet became **r2d** (Git blob `7aa8c89cae16a94109cead60ee12aeee25091d3f`). Backups (entry 12) and the tree and
identity checks (entry 13) passed.

**Mode H, Oz Lotto (15 November 2026; entries 14 to 21).** Approval 1: the study manifest (40 variants, master version 1,
497 closure files, environment digest `5bf4eb8a36dd...`) and the opening record; the value-free witness push **`9eb5e33`**
(D3). Approval 2: the first live results update, 15 draws added (1694 to 1708), master version 2
(`63e3349333f8aa0485b7b067abe70249e39de81c6d02cda1a5710cf1041a4e9e`). Approval 3: the plan and the batch
`wf-5af149aef7444336a38e469146c95a20`, 400 of 400 forecasts SUCCESS. Approval 4: score attempt
`mh-ba0c301be2fb4c459492697d0137e7ed`, search-log row 8, 800 score lines and 400 rank lines; **SEALED 15 November 2026,
19:54**. Backups before and after. The reviewer's audit of the whole sequence: **EX_196, PASS WITH EVIDENCE LIMITATIONS**.

**Mode H, Powerball (16 November 2026; entries 24 to 37).** Claude's expected-state annex to r2d
(`POWERBALL_AFTER_OZLOTTO_ANNEX_r1.md`, Git blob `cc00da3665ed607ff49d2fdb92855eb1925dcef5`; EX_197; the reviewer EX_198).
The Powerball page recheck (r2) PASS; backups; tree check. Approval 1 and the witness push **`c302871`**. Approval 2: 15
draws added (1577 to 1591), master version 2 (`e4f2feb8b18fc2dbe389583a189fa26127a648f4da940dd76219ee282170f3e0`). Approval 3:
batch `wf-5085cd8feaf54cffb22823ab5869d5a8`, 400 of 400. Approval 4: score attempt `mh-24b3eb05319d4051be2f5e6ae1e6c8b8`,
search-log row 12, 800 and 400 lines; **SEALED 16 November 2026, 20:53**. The backup after the seal, checked with `/L`
(entry 37, closing EX_199 C01). The reviewer's audit: **EX_199, PASS WITH EVIDENCE LIMITATIONS**. **Mode H execution is
complete in both games, and the code and environment freeze ended at Powerball's seal.** HX-1 (Powerball 1585 and 1586) was
flagged and scored like any other draw.

**The OUTLANDISH_01 export (16 November 2026; entry 23).** At the owner's request Claude wrote a tool that writes Oz Lotto's
pre-holdout draws 1474 to 1693 from the committed version-1 master for the OUTLANDISH_01 side project
(`exchange/CLAUDE_WEB_TOOLS/outlandish_export/make_ozlotto_preholdout.py`, r3, Git blob
`8c4bec6950624287cdc15c7d2216b054453a36be`;
the reviewer's blocking finding on r2, a dynamic import, fixed and retested on two Pythons). The owner ran it and committed
`GAIS/OUTLANDISH_01/OZLOTTO_preholdout_only.csv` at `c528be4` (220 rows; SHA-256
`82557ea5ad01aef075b4031014714417eddbd7d7128666f464f79c416c9bd44c`). It is not evidence for this project.

**The readings of the two reports (D6; 16 November 2026; entries 38 to 41).** The owner gave both value-free reports to both
AIs together. Claude's reading (EX_201) was written first and held back, its SHA-256 committed (entry 38) before the
reviewer's independent reading (EX_200) was given; the two agree on the result and on every figure they share (EX_202).
The reviewer's replies are EX_203A (its unnumbered assessment of EX_201, renamed when its own EX_203 arrived) and EX_203;
Claude's are EX_204 and EX_205. **The record of the study, agreed by both AIs (EX_205 section 5, r2):**

> **Mode H (Oz Lotto draws 1694-1703; Powerball draws 1577-1586; both studies sealed).** No statistically significant
> predictive advantage was demonstrated under the predeclared Mode H tests. In each of the three predeclared MR7 families the
> Bonferroni family-adjusted P is above 5%: 1.000 (Oz Lotto main numbers), 0.672 (Powerball main numbers) and 0.920
> (Powerball number), each guaranteed under design 6.2A with all 80 tracks meeting its conditions. The three families were
> not jointly adjusted. The N1 maximum-statistic figures (0.570, 0.359, 0.306) are references, not confirmatory substitutes.
>
> **Limits.** Every track is LOW_N (ten scored draws). Over these ten draws, a single track would have needed at least 21 Oz
> Lotto main-number matches (versus about 10.43 expected) or 25 Powerball main-number matches (versus 14 expected) to pass
> the respective 80-track Bonferroni family test at 5%; the best observed were 17 and 22. These are rejection thresholds
> under the specified test, not a power calculation. A nonsignificant result is not evidence that every method is no better
> than chance, nor that the draws are random. The evidence is a retrospective precommitted holdout, not prospective.
> Powerball draws 1585 and 1586 carry HX-1 flags and were scored like any other draw.
>
> **Exploratory leads (recorded; not findings).** Powerball E_19:PERIODIC_T2 WORST (MR1 local N1-calibrated P 0.0005; 3
> Powerball-number hits in ten draws); Powerball E_17:HAZARD_BINS_C100 WORST (22 main matches); Oz Lotto E_4:POLY_LS_W104_D3
> TOP (17 main matches); Oz Lotto MR5.MAIN rank positions (best variant E_3:POLY_MINIMAX_W52_D3_H4, N1 reference P 0.0191).
>
> **Post hoc exploration (EX_201 sections 3.3 and 3.4; descriptive counts only, from heavily dependent tracks; no calibrated
> probability attaches to them).** Oz Lotto: TOP tracks 465 main matches against about 417 expected, WORST tracks 363; TOP
> ahead of WORST in 29 of 40 variants; 33 of 40 variants with a better-than-fair mean rank (22.95 against 24).
>
> **What may follow.** Nothing is tested again on the sealed holdouts. Any future test of a lead fixes its rule, outcome,
> measure, sample or window, threshold, multiplicity treatment and handling of correlated variants before genuinely new
> draws are evaluated, in an owner-approved design.

Kept as a separate paragraph, outside the Mode H result (EX_203A's broader point; EX_204 section 3):

> **Development evidence (a separate tier; H-1 v3 section 7.5).** The development walk-forward evaluation (26,040 forecasts:
> Oz Lotto 219 targets; Powerball 432 targets forecast, of which the 291-draw report window was scored) also showed no
> statistically significant advantage (Oz Lotto family Bonferroni P 0.090; Powerball main numbers 1.0). It is exploratory
> development evidence and is not combined with the holdout or with future prospective evidence.

**D5 (16 November 2026; entries 47 and 48).** The owner committed the Mode H results at **`c7622fa`** (named paths, 25
files): both masters and their ledgers at version 2, the search log, the two `MODE_H_BATCH_ID.json` records, each batch
folder (plan, segment record, `BATCH_COMPLETE`, `SCORING_STARTED`, `SCORE_COMPLETE`, `MODE_H_SEALED`) and the six report
files. Claude found the committed masters and the two report `.txt` files byte-identical to the values recorded at the
seals (Oz Lotto report `68112928b332666c8e2da6504b06e93a81295cf21682cd076d0a85e754ebd0e6`, Powerball report
`1bad6295f5af67845412983c3c37ae48156530dad3b12ce24ad3234cf4177ffc`). The git-ignored run folders, attempts ledgers and score
ledgers stay on the owner's PC and in his backups.

**The holdout exposure record is closed** (EX_206 Q3). Both holdouts are opened, scored and sealed, so
`doc/HOLDOUT_EXPOSURE_RECORD_v0_3.md` takes no further entries and is not edited. Its facts stand: HX-1 (Powerball 1585 and
1586, inside the holdout, flagged and scored in Mode H) and HX-2 (Powerball 1587 and 1588, which carry the exposure flag
when the weekly session scores them, design 6.4; the MHUP-B supplement keeps that flag).

**The approach the owner agreed on 16 November 2026 (entries 42 to 47; reviewed in EX_206; in force from RAT-34).** Record:
`exchange/DECISIONS/AGREED_APPROACH_2026_11_16.md`, with the rule-by-rule page `exchange/DECISIONS/RULES_AFTER_Q7_DRAFT_r2.md`.
After asking why the sealed holdouts could not be treated as ordinary data and why the AI chats could not read `results/`,
the owner decided, and the reviewer agreed with conditions (EX_206: Q1 to Q5):
1. **All draws are treated the same.** The AI chats may read draw values, the masters and the results. No holdout is needed
   for future method development. This replaces Q7 of 13 November 2026.
2. **Kept, unless the owner agrees an exception case by case:** no lottery website and no results search by any AI (the
   owner's updater is the only source); results count only when they come from the reviewed programs and their logged runs,
   and anything an AI computes in a chat is labelled suggestive; nothing runs on the owner's PC without his go. **Also kept
   (EX_206):** method-facing N-1 isolation, forecast identities and append-only evidence; already-known draws give
   development evidence only; the sealed Mode H records are never altered or rescored.
3. **Claude's writing** (entry 46): the limit to `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/` is removed, on the owner's
   condition that nothing is destroyed. Documents that have been reviewed and ratified are committed by Claude directly;
   code and tests still go by reviewed package, a Windows rehearsal and the owner's install; Claude never writes
   `source_data/`, `results/`, `transitory_data/`, `GAIS/` or the runner's and repository settings; nothing is deleted or
   overwritten; named paths only; no reset, clean or force push; Claude coordinates with the owner's Git activity.
4. **The reviewer** may commit its own EX replies to `exchange/` and its H-2 files to `doc/HANDOVER/` (entries 50 and 56).
5. **The local runner's rulebook (v0.5) is unchanged**; its rules 4 and 5 stay binding until MHUP-B's reviewed rulebook
   edition makes them read-only wording (EX_206 Q4).
6. **A new method re-ranks all draws** to the latest; superseded tables are archived, never overwritten.

**RAT-33: the MHUP-B design supplement (owner, 17 November 2026, 14:48; entry 61).** After the owner authorised the MHUP-B
design (entry 46), Claude wrote a supplement to the ratified design v0.1r7 from the owner's inputs
(`exchange/DECISIONS/MHUPB_DESIGN_INPUTS_2026_11_16.md`, D-1 to D-11) and his decisions: a full MHUP-B, not a small one
(entry 51); the holdout draws open to re-forecasting by every variant as development evidence, the sealed records kept as
separate history (entry 53); the overall measure scored per game (entry 55); a `current` folder and a permanent archive
(entry 58). Five review rounds: EX_207 (v0.1), EX_208 (v0.2: recheck; the reviewer's exact counterexample showed that five
normal-cut-off readings did not guarantee their error rate, and Claude reproduced it), EX_209 (v0.4), EX_211 (v0.5) and
**EX_213 (v0.6: focused design pass; ratification recommended with condition RC-1)**. v0.7 is v0.6 with RC-1. The owner
ratified `exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_v0_7_RATIFICATION_CANDIDATE.md` (SHA-256
`04c4f68a638fff7d93f06d25084d1454bdfc443e9aab6b0b12ffdfd8b5323d26`) and approved O-1 (the league table, its files and
folders), O-2 (OV-1, an exact evidence score per game with a bar of 40, as the one confirmatory forward test; everything else
secondary), O-3 (the window contract and the re-forecasting rules) and O-4's objective (scoring Powerball targets 1145 to
1285; the run needs its own go once its command is reviewed). It approves a design only; the code round's gates listed in
its header stand. With RAT-34 its bytes are also committed unchanged as
`doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_7.md`.

**H-1 v4 (17 November 2026).** A full edition built from H-1 v3's ratified bytes by counted edits and whole-part
replacements (`exchange/CLAUDE_WEB_TOOLS/h1v4/make_h1_v4.py`), with its blurb. Its new section 0B states the position after
Mode H and prevails over older statements; section 2A is byte-identical. A first DRAFT of 16 November 2026 (kept in
`exchange/CLAUDE_WEB_TOOLS/h1v4/out/`) was written at the owner's request for risk management. Sent with this register as
**EX_214** for the reviewer's documentary review. The reviewer wrote its own **H-2 v3 CANDIDATE** and blurb and committed
them (`5204c41`, `e631380`); it decides when to finalise them, and H-2 v2 r1 stays the installed reviewer handover until the
owner ratifies a successor.

**RAT-34 (pending).** The owner is asked to ratify this register, H-1 v4 and its blurb, and to confirm that the approach of
16 November 2026 comes into force with them. On ratification, only this register's version line, this paragraph and its
table's status cells, and H-1 v4's status line, change; Claude then commits the ratified files into `doc/` directly (this
register, H-1 v4 and its blurb, and the RAT-33 supplement) and checks them from GitHub.

**Future actions (replacing register v0.30's list; not authorisations).**
1. The reviewer's review of this register and H-1 v4 (EX_214); RAT-34; Claude's direct commit into `doc/` and its check.
2. The MHUP-B code plan in the supplement's eight layers, reviewed before any code; then the code, its review, the Windows
   rehearsal (with a full-suite run after step 18) and the owner's install, each on its own go. With the package: the
   runner's rulebook edition (rules 4 and 5), the R3 amendments (17.3.6 the window contract; 17.5A and the registries for
   OV-1), the E2R-1 amendments for `CATCH_UP` and `FINAL_NEXT_DRAW`, and the Architecture's next edition. OV-1 is registered
   before its first contributing draw, on the owner's go.
3. The Powerball 1145-1285 report run, on its own go once its command is reviewed.
4. Unchanged from earlier lists: WF-1C; the methods still to do (OUTLANDISH_01's family probably first); KISS-1 when the owner
   asks; the ideas backlog (P5); the next editions of R3, E2R-1, Architecture and the proposal; the newest-first and shuffled
   page cases in the updater's own tests (tests only); the reviewer's H-2 v3.

**Out-of-date statements (register v0.31).** This register prevails, and the files are not edited:
- **Register v0.30, future actions 1 and 2:** done (`5b4df41`; Mode H run and sealed).
- **H-1 v3:** its sections 0, 5, 10, 11 and 12.8 describe the state before Mode H and the rules before 16 November 2026;
  replaced by H-1 v4 at RAT-34.
- **H-2 v2 r1:** its statements before Mode H and its Q7 wording; overtaken by this register and the reviewer's H-2 v3 when
  ratified. Its rights region is unaffected.
- **Q7 wherever it is still written** (the design v0.1r7 section 9, H-2 v2 r1, the holdout exposure record, older H-1
  editions): replaced from RAT-34 by item 1 of the approach above.
- **R3 17.3.6 (the Phase 1 window cap at 1576 and 1693):** stands in the code until MHUP-B amends it by the ratified window
  contract.
- **The design v0.1r7 section 6.6 (the league table):** supplemented by RAT-33.
- **The readiness sheet r2d and the annex r1:** history; their work is done.

| Document (path) | Author / check | Status and Git-content SHA-256 |
|---|---|---|
| `doc/RATIFICATION_REGISTER_v0_30.md` | Claude, from the records | OWNER-RATIFIED 15 Nov 2026 (RAT-32); installed at `5b4df41`; superseded by this register; `2a6fe7b6758d882b46a6829cff6c73ddefa5381f9fe3851b72720ab40ccdd56c` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v3.md` and its blurb | Claude | OWNER-RATIFIED 15 Nov 2026 (RAT-32); installed at `5b4df41`; superseded by H-1 v4 at RAT-34; `ddefe7006aa17cfd0a9a8996bd7122aed537d8d66accee92b2e5d737aefbaa54`; blurb `d1df63bf18bc7becc96212ac0d76d519a2a5c4d6b367251116b294382573dd4d` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v4.md` | Claude, from H-1 v3 and the records | CANDIDATE for RAT-34; `@H1V4@` |
| `doc/HANDOVER/Claude_Primary_Handover_H1_v4_introductory_blurb.md` | Claude | CANDIDATE for RAT-34; `@H1V4B@` |
| `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_7.md` | Claude; the reviewer (EX_207 to EX_213) | OWNER-RATIFIED 17 Nov 2026 (RAT-33); the same bytes as `exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_v0_7_RATIFICATION_CANDIDATE.md`, as stored (CRLF) `04c4f68a638fff7d93f06d25084d1454bdfc443e9aab6b0b12ffdfd8b5323d26` |
| `exchange/DECISIONS/AGREED_APPROACH_2026_11_16.md` | the owner's decisions, recorded by Claude; the reviewer (EX_206) | OWNER DECISIONS 16 Nov 2026; in force from RAT-34; as stored `077cd5135415bfe3de10e9fe497ceb4cb6fc1e998e95625894db6c751b18e528` |
| `exchange/DECISIONS/RULES_AFTER_Q7_DRAFT_r2.md` | Claude; the reviewer (EX_206) | the rule-by-rule page behind the approach; as stored `7227eb0960de7a3a95271d20e80a79931c346b28731231e4cdfb02f0b913f7a0` |
| `exchange/EX_205_Claude.md` | Claude; agreed by the reviewer (EX_203) | the record of the study, section 5; as stored `357132df0fe3dc57d37f137a11730bf4e64136867471ba76a82fb4ea29f5b3f4` |
| `source_data/POWERBALL_results_master.csv`, `source_data/OZLOTTO_results_master.csv` (at `c7622fa`) | the owner's updater | master version 2; `e4f2feb8b18fc2dbe389583a189fa26127a648f4da940dd76219ee282170f3e0`; `63e3349333f8aa0485b7b067abe70249e39de81c6d02cda1a5710cf1041a4e9e` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3_CANDIDATE.md` and its blurb | the reviewer | CANDIDATE, not ratified; `b35f8acc22ec6ac71e5e37c92da5cd4cd6bf12972896dd305f73fa9c3be40e1d`; blurb `042b7f841e3dd18b92d76066461d390c798a7dc46d884698a264e226986aced0` |
| `exchange/DECISIONS/DECISION_LOG.md` and `exchange/CONTINUITY_NOW.md` | Claude, from the owner's words and the records | living files (P2, P0); no fixed hash; Git keeps their history |

