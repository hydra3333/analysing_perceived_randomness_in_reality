# Where the project is up to (the owner's roadmap)

Kept by the Claude web chat; updated at each milestone. Plain English. This is a working list, not
reviewed and not part of the rules: the ratification register is the record. US-ASCII, CRLF.
Last updated: 4 November 2026 (afternoon): the staged Claude handover (HO-2) COMPLETE; the replacement Claude
chat accepted and normal work authorised (option (a)); the direction document v0.3r1 installed at dfc2d13.
Plain-English direction: doc/Direction_for_operational_procedures_v0_3r1.md (v0.2r1 kept as history);
the stock-take record: exchange/STOCKTAKE_2026_11_02_v0_8.md.

## A few words used below

- **E_n:** the project's permanent name for method number n. The catalogue (R1 and R2) lists 62 of
  them, E_1 to E_62, each with a one-line idea. A method becomes real only when its exact rule is
  written, reviewed and coded; until then its catalogue entry is a placeholder.
- **Installed (not yet runnable):** the method's code and tests are in the repository and pass, but
  its registry entry says "not released" and its folder holds an IN_DEVELOPMENT flag, so every request
  to run it is refused before any data is read. A later small "release" package switches it on.
- **Released:** allowed to run. Since WF-1A (31 October 2026) released methods also run on the real
  development draws (walk-forward batches you authorise), never on the sealed holdout.
- **Prospective mode:** the weekly production loop (your MH-1): each week, per game, the results
  update, the catch-up of any missed draws, the scoring of the open forecast, and the next forecast.
- **Developed:** you declare the pipeline ready for the released methods; later waves keep adding
  methods afterwards.

## How every package goes (the routine)

1. Claude writes the design; ChatGPT reviews it; the owner decides.
2. Claude writes the code and tests; ChatGPT reviews them; the owner ratifies.
3. Claude Code rehearses the install on the owner's machine, in a throw-away copy.
4. The owner installs (check, copy, check, tests, commit, check, push).
5. Claude checks the result from GitHub; the next register edition records it.

## Done

1. DONE - The plan and specifications (proposal, architecture, method list R2, measuring rules R3),
   the safe launcher and coordinator, and the results-data tools.
2. DONE - The method "contract" (CODE-1, CODE-2): the shared rules every method plugs into, so each
   new method only supplies its own maths. It handles the release check, frozen records and the
   strict "only draws before the target" rule.
3. DONE - Claude Code set up as the local runner; it rehearses every install.
4. DONE - E_6, installed (not yet runnable). For each number separately, it keeps a running estimate
   of how often that number is drawn, starting from the fair-draw rate and updated after every draw.
   Three fixed versions: one remembers everything equally; two "forget" gradually, so older draws
   count for less (half their weight after about 1 year, or about 2 years).
5. DONE - The new-method template, draft 1 (doc/METHOD_TEMPLATE/): a commented starting kit and
   checklist for writing a new method. It is kept up to date whenever a method shows it should be.
6. DONE - E_3 and E_4, installed (not yet runnable). For each number, they fit a smooth curve to its
   drawn/not-drawn record over the last 52 or 104 draws. E_3 ranks numbers by where the curve says
   the next draw will be (its value there); E_4 by which way the curve is heading (its slope). Six
   fixed versions each: three curve-fitting styles, different curve shapes and window lengths.
7. DONE - The two handover documents brought up to date (H-1 for Claude, H-2 for ChatGPT), so a
   fresh chat can pick up the project with the same rules.
8. DONE - Wave 1, installed (not yet runnable), with the template's draft 2 (commit 947c370):
           E_7  counts pulled back towards the fair rate, so a short lucky run counts for less;
           E_9  counting where each older draw counts a fixed fraction less;
           E_10 the recent rate compared with the longer-run rate;
           E_8  each number's rate, with all numbers sharing information (by periods of 13, 26 or
                52 draws).
           Three fixed versions each, one shared counting helper, 268 tests passing on your PC and
           on Linux. The template's draft 2 adds what E_3/E_4 taught: shared helpers, methods that
           give scores but no probabilities, and a minimum number of past draws.

## Next, in the owner's order (decided 30 October 2026; items 10b to 10d added 1 November 2026)

9.  DONE - Wave 2, installed (not yet runnable), with the template's draft 3 (commit b61b1a2):
           E_2  favours numbers whose next draw would complete their usual gap (mean, middle, recent);
           E_17 = your Method A: the chance of coming up, by how long a number has been away, learned
                from the data, including your exact log-of-age rule;
           E_19 short repeating cycles (2, 3 or 4 draws), number by number;
           E_18 each number's gaps as a mix of four patterns (quick, fair, long absences, even).
           299 tests passing on your PC and on Linux.
9b. DONE - The handover documents brought up to date (commit 03f7da4): Claude's H-1 v1r6 and the
           reviewer's H-2 v1r7, each with an introductory blurb saved beside it, and register v0.20.
           The old ChatGPT chat had reached its limit, so Claude wrote both, on your instruction, with
           H-2's reviewer rights unchanged byte for byte. The new ChatGPT reviewer chat took over on
           30 October 2026: its takeover check found 0 BLOCKER, 0 CORRECTION and 1 OPTIONAL.
10. DONE - Releases and WF-1: switch the methods on, run them on past draws (walk-forward: each past
           draw predicted only from the draws before it), and score them, so the project produces
           its first real measured results.
           Done so far (all 31 October to 1 November 2026, each reviewed, ratified by you and checked
           by Claude from GitHub):
           - design v0.1r1 (EX_077 to EX_081); REL-1 INSTALLED (6a1bed9); WF-1A, the walk-forward
             driver, INSTALLED (0d98706); E_1 revision 2 with CODE-3 INSTALLED (86d12ea). All 40
             variants can run on past draws.
           - The two batches are DONE, every run SUCCESS, frozen and waiting to be scored:
             Powerball wf-3347ad1160df45faaaab1e2eedcedd0f (targets 1145-1576, 17,280 runs; 86a1a01);
             Oz Lotto wf-a75988650fb04cc399f8f7409ea27243 (targets 1475-1693, 8,760 runs; 8430a15).
           - Register v0.22 INSTALLED (2b1e7e3).
           - The N1 seed: you brought the pulse forward to 2026-10-31T10:30Z (EX_103, 92a6cef) and
             APPROVED it on 31 October (pulse 2007128). The 6 November pulse was never fetched.
           - WF-1B, the scorer and report: supplement design v0.1r1 ratified (EX_104 to EX_107; WB-0
             workers moved to WF-1C, WB-1 real results first, WB-2 seed in WF-1B). Code reviewed EX_108
             to EX_111: PASS. You accepted WF1B_Install_v2 on 1 November 2026 and deferred EX_111's
             optional O01 to a later package (reminder R-007).
           - Windows rehearsals: T012 and T013 stopped safely (a task-file wording fault, then one test
             that made a symlink, which Windows refuses; the other 462 tests passed on your PC). v3
             fixes that test only (EX_112); EX_113: PASS. You accepted v3 on 1 November 2026 and
             deferred EX_113's optional O02 (a label in the test runner; reminder R-010).
           - WF1B_Install_v3 INSTALLED (24d192f, 1 November 2026; T014 PASS; verified from GitHub).
           - First report runs (1 November): Oz Lotto started at 09:55 and was still in its statistics
             after an hour; Powerball was refused (its batch plan file differs on your PC, probably line
             endings; to be checked and restored).
           - PERF-1 (you approved it on 1 November, as a small piece brought forward from the performance
             study, coded and tested first and reviewed once): the exact uncertainty interval made fast
             with bit-identical results (the statistics stage: hours down to about 4 minutes on invented
             data), and progress lines for the report tool. Sent for review in EX_114; rehearsal T015.
           Left in this item, in order:
           - DONE (1 November 2026): EX_115 PERF-1 PASS; T015 PASS; PERF-1 INSTALLED (3fce327).
             Oz Lotto report committed (441daf2; about 4.5 hours before PERF-1). The Powerball batch
             records were restored (line endings) and its report committed (608025c; about 26 minutes).
             Both games: no method beats chance (development evidence only). Item 10 is complete.
10b. DONE - The snapshot (your request, 1 November 2026): one document package (DOC10_Snapshot_v1),
           sent to ChatGPT in EX_116 (candidate 2, after a cold-read test of H-1 by a fresh helper
           found 20 gaps, now fixed). EX_117: RECHECK with 3 corrections (a historical paragraph in the
           register, H-1's wording on stopping test jobs, a line-ending check after the pull); fixed in
           candidate 3, sent in EX_118. EX_119: one correction left (the line-ending checker must treat
           a nonempty file with no line ending as a STOP); fixed in candidate 4, sent in EX_120. EX_121: PASS. You ratified
           it on 1 November 2026; the final build (status lines only) is in EX_122. INSTALLED at
           7bb0bfd (1 November 2026; COMMITTED PASS, EOL PASS; verified by Claude from GitHub, 30 of 30
           manifest rows). Your settings.json deny line is committed at 905ecee. Next: the new Claude
           chat, started from doc/HANDOVER/Claude_Primary_Handover_H1_v1r7_introductory_blurb.md:
           - register v0.23 (EX_099 to EX_115, the installs, the two reports, your decisions);
           - new editions of the two handovers (H-1 for Claude, H-2 for ChatGPT) with their blurbs;
           - Architecture v0.9 (the scorer and report, the walk-forward driver, where records live);
           - the Claude Code rulebook: the report tool joins rule 7's "never run" list, with the
             matching deny entry in .claude\settings.json (that file is yours to edit);
           - a short README.md for the repository;
           - settle the holdout exposure record (HOLDOUT_EXPOSURE_RECORD v0.2, still a candidate). You
             decided on 1 November 2026: record the exposure (a reviewer chat displayed Powerball
             1585-1588); Mode H scores all 10 holdout draws per game, with Powerball 1585 and 1586
             flagged; until then all 10 are treated as unseen, with every rule in force;
           - a Git line-ending rule so files under results/ are never converted on your PC;
           - the findings of the two cold-read probes (1 November 2026: the results updater, and the
             performance plan), each settled in the documents or carried into the Mode H design.
10c. NEXT - Mode H, the results update and the prospective mode. Designed together by the new Claude
           chat. Plan (your ratification, 2 November 2026): Mode H and the weekly session installed by
           about 13-15 November, so the first forecasts frozen before a draw are Oz Lotto 1709
           (Tuesday 17 November) and Powerball 1592 (Thursday 19 November); the week of 9 November is a
           stretch only, and if it slips the catch-up covers the missed draws (FB-1). Design v0.1 was
           written (exchange/EX_123_Claude.zip, commit c01717d) but NOT sent to ChatGPT; it is replaced
           by v0.1r1 carrying the stock-take positions, cold-read twice by a fresh helper on 3 November
           2026 and sent to ChatGPT as EX_124 (reply EX_125). The cold read found that E_1 revision 2
           refuses every new run mode in its own code, so E_1 needs a revision 3 (same arithmetic) before
           it can take part in Mode H. Q10: you decided on 3 November 2026 to extend the ER-2r1
           one-package exception to E_1 revision 3 (recorded as owner-decided, open to revisiting if
           ChatGPT's review changes anything). ChatGPT's review EX_125 (3 November 2026): RECHECK, 5
           BLOCKER, 9 CORRECTION, 3 OPTIONAL, all accepted by Claude; it provisionally favours option A.
           Your decisions on 3 November 2026, after that review: Q1 = option A (Mode H as a precommitted
           holdout evaluation: plan and code frozen before opening, every forecast from draws before its
           target, nothing scored until all are frozen), the corrected design still to pass the recheck
           before you ratify it as a whole; B02 = implement MH-1's order exactly (predict N, reveal N,
           score N, then N+1) with a small orchestrator that alternates the two program halves per
           target; C03 = Lotterywest's published results are official and trusted as they stand, so no
           second-source check of a new draw is required in production (this supersedes, for production,
           the earlier independent-evidence wording of R2-C03 and the proposal; to be recorded in
           register v0.24). Design v0.1r2 went as EX_126; ChatGPT's EX_127 (3 November 2026): RECHECK, 5
           BLOCKER, 5 CORRECTION, 2 OPTIONAL, all accepted; it says one more narrow check should do.
           Your decisions on 3 November 2026 after EX_127: B04 = the results updater gains one small
           check, refusing to run while a game's holdout is open and Mode H not yet scored (a reviewed
           change to your tool); B04 = the Mode H environment freeze checks the installed files
           themselves (the Python program's hash and the SHA-256 that pip records for every installed
           file), not only package names and versions. Q11 decided 3 November 2026: official runs only
           through tickets written by the driver or the weekly forecasting half; hand-typed runs stay
           available as your unofficial diagnostic route (never scored into a ledger). Design v0.1r3
           went as EX_128 (reply EX_129): every EX_127 finding applied; two cold reads by a fresh
           helper (24 + 13 findings, all applied). One new point for you inside it: Run_Experiment.bat
           gains two interpreter options (-B, PYTHONPYCACHEPREFIX), so MHUP-A's approval asks you
           either to authorise one rerun of the Windows POC suite afterwards or to accept it unrun
           with the reason recorded. ChatGPT's EX_129 (3 November 2026): RECHECK, narrowly; 2 BLOCKER
           (B01 the first results update could add no draws or only some and then lock the study;
           B02 the install barrier does not stop the updater, and a short launch window before the
           new gate is only procedural), 2 CORRECTION (C01 an unfinished forecast set across a
           roster change; C02 the byte-code folder detail), all accepted. Your decisions (3 November
           2026): D1 = the updater's first update after opening writes only if it brings in every
           holdout draw (a fourth small updater addition); D2 = an install holds the updater's own
           lock; D3 = you don't launch the coordinator's POC path, the report tool or the walk-forward
           driver during an install, and accept the few-seconds gate-copy window (extended the same
           day). Design v0.1r4 went as EX_130; ChatGPT's EX_131 (3 November 2026): CONDITIONAL PASS -
           FIX AND PROCEED, one install-recovery safeguard (never restore while a process may be
           running), inserted as worded in v0.1r5 (EX_132, for the record; no further review round).
           RATIFIED by you on 3 November 2026 (about 20:42; MHUP-R), with the design's recommendations
           for Q2-Q6, Q8 and Q9; Q7 stays open. Then you paused the code until all the documents are
           updated, and decided the staged AI handover (HO-2): Claude is handed over first, the
           experienced ChatGPT reviewer stays throughout. NOW: DOC-11, the Claude handover package
           (register v0.24, H-1 v1r8 and its blurb, the design and the direction document in doc/, six
           review copies), tested by a fresh helper playing the new chat (20 gaps, fixed), then sent to
           ChatGPT for the Step 1.1 review (EX_133); ChatGPT's RECHECK (EX_134: three wording
           corrections, one editorial item) fixed in EX_135 with your naming decision LW-1
           (Lotterywest-GOV); ChatGPT's recheck EX_136 PASS; you ratified DOC-11 on 4 November 2026
           and installed it at 3d4fa3c (verified from GitHub, EX_138). DONE (4 November 2026): the new
           Claude chat started; ChatGPT checked its first reply and asked Q1-Q9, answered blind, all
           PASS; Q9 led to the direction document v0.3r1 (ChatGPT RECHECK, then PASS; ratified and
           installed by you at dfc2d13); your decisions on retrying after a STOP, interrupted sessions
           and Q9's E1-E4 (reminder R-018); you declared HO-2 complete and authorised normal work
           (EX_139, EX_140). DONE (4 November 2026): Claude's workspace proven (the whole suite on
           Python 3.13 and 3.15); you chose two review slices then one integrated MHUP-A package;
           slice 1 (the version-2 master rules, E_1 revision 3, one data kind, the binding and ticket
           gates, barrier P) coded on Fable, 506 tests passing on both Pythons, 67 mutants (61 caught,
           6 equivalent, 0 survived), sent to ChatGPT for code review as EX_141; ChatGPT's RECHECK
           (EX_142: three blockers - the frozen-pin binding, fail-closed evidence, the full ledger
           grammar for every ledger - and C01-C03), your C01 decision (effective_date = the integrated
           package's preparation date; the release record alone dates a release), the fixes as
           candidate v1r1 (507 tests, both Pythons; 87 mutants, 80 caught, 7 equivalent, 0 survived)
           sent as EX_143; ChatGPT's EX_144 (B01 PASS, two narrow residuals: blank JSONL lines and
           strict CSV quoting) fixed as candidate v1r2 and sent as EX_145 (507 tests, both Pythons; 90
           mutants, 81 caught, 9 equivalent, 0 survived); the reviewer's slice 2 watchpoints are reminder
           R-019. DONE (5 November 2026): ChatGPT's EX_146, slice 1 PASS (the review checkpoint only, not
           the integrated package). DONE (5 November 2026): slice 2 coded and tested on Linux (the Mode H
           batch kind and families, Method_Mode_H.py, the closure and environment freeze, the records tool,
           process_check.py, the updater v0.2, the launchers, the freeze-before-outcome rule, the rulebook
           v0.4; 561 tests on both Pythons; the slice 2 mutants) and sent for review as EX_147 (its
           interpretations listed for the reviewer; reminder R-020 for what the integrated package carries).
           DONE (5 November 2026): your Claude Code run of TASK_T018 (slice 1's 507 tests on Windows, in a
           task clone, read-only): SUITE PASS, so your real committed ledgers pass the full ledger grammar.
           TASK_T019 STOPPED correctly at step 5 (5 November 2026): its commands named .bat and updater
           paths that .claude/settings.json denies; the clone tool v0.4 now reads them from a plan file.
           NOW: ChatGPT's review of EX_147, and your Claude Code run of inbox/TASK_T020.md (slice 2's 561
           tests on Windows, the same read-only way; replaces T019); then any RECHECK;
           then the integrated install package with its rehearsals and T016. Installing it, its Windows
           rehearsal and MHUP-B each wait for your separate go. A ChatGPT reviewer handover is considered later, separately. The
           planning dates above are unchanged; FB-1 applies.
           The design:
           - Mode H: every released variant forecasts each of the 10 sealed holdout draws per game
             (Powerball 1577-1586, Oz Lotto 1694-1703), each from the draws before it, then scored
             once; Powerball 1585 and 1586 flagged (HX-1). Your preference (2 November 2026) is
             option A: the study plan and the code are frozen before the holdout is opened, every
             forecast uses only the draws before its target, and nothing is scored until all are
             frozen. Option B (reveal one result at a time) stays in the design as the alternative for
             ChatGPT's review; option C (all ten forecast from the development draws only) is
             withdrawn: with the same training draws every variant would produce the same scores ten
             times (the target's number enters only the tie-break and the record identity, so at most
             the order of tied numbers could differ), so C would test one scoring, not the weekly
             retraining. (Corrected 3 November 2026: the earlier wording "no released method uses its
             target's draw number" was wrong as stated; the withdrawal stands.) The register's phrase
             "all frozen before the
             holdout is opened" is amended to the wording above when the design is ratified;
           - the results update: the updater exists as code (your tool), but how it is used with
             Mode H is still to be designed. The critical gap: today every reader accepts only the
             first (version-1) results file, so a version-2 reader is needed first (probe A1). The
             first update run and the opening of the holdout each need your separate approval;
           - the prospective mode, your weekly session (MH-1): update, catch up missed draws in order,
             score the open forecast, freeze and publish the next one; PROSPECTIVE and CATCH-UP kept
             apart; Powerball 1587 and 1588 flagged when caught up (HX-2; flagged draws stay
             fully valid and counted, no gaps). Also ratified on 2 November 2026: the weekly command
             prints a status block per game (last accepted draw, last forecast, last scored draw,
             backlog, next target and its deadline, active variants, each target's label); exactly one
             open forecast per variant; nothing is ever scored twice; a draw whose result is not yet
             accepted is left open, never skipped; whether a caught-up draw counts as CATCH-UP is
             decided by a local install record written by each install (one record covers the methods
             installed so far), not by Git history (OFF-1);
           - your other inputs: everything runs offline, GitHub only an optional witness (OFF-1; R3's
             push-based timing proof must be amended first); the weekly path is incremental (EFF-1);
           - how frozen records behave (ratified 2 November 2026): a forecast is never changed; an
             accepted score is kept, and any new scoring run is added beside it, never over it; a
             league table is a view and is meant to change, so adding or retiring a method produces a
             new dated report while every earlier report stays as published. A retired revision's code
             and tests are archived and its registry entry becomes RETIRED, but its forecasts and
             scores stay where they are, with an index pointing at them;
           then you decide whether to declare the system developed.
10d. NEXT - WF-1C, the workers change (your decision WORKERS-1, 31 October 2026), in its own design
           round carrying EX_101's and EX_105's obligations: the coordinator's limit becomes 1 up to the
           machine's logical processor count (24 on your PC), default half (12); the walk-forward
           driver gets --workers (variants in parallel, same records at any worker count, clean stop);
           a progress line; a compare command; the identity tests run once. Open for its design: the
           60-worker cap, a 4 GiB memory floor, separate approvals for any real-data rerun and for
           Windows multi-process tests (EX_105 C03), and WB-3/WB-4. Until then the coordinator's
           six-worker limit stands, and the walk-forward driver runs one method run at a time.
11. NEXT - Wave 3, look-alike past draws (with the template's draft 4, reminder R-009):
           E_27 Nearest Neighbour of Historical Draw Sets - predict from what followed the past draws
                most like the latest one;
           E_45 = Method B - your second idea: the same with runs of recent draws, plus the
                never-occurring up/down patterns check;
           E_26 Draw-Level Geometry and Summary States; E_28 Markov Transitions of Draw Summaries.
12. NEXT - Discuss the NL-means idea (reminder R-002); any method it yields joins a later wave.
13. LATER - Wave 4: E_5 (your original: one model for all numbers together), E_11 change points,
           E_15 eras, E_14 calendar (uses dates); then, each in its own package, E_13 slow drift,
           E_12 hidden modes, E_16 slightly unequal ball weights.
14. LATER - Wave 5, curves and cycles: E_37 (reuses E_3/E_4's helper), E_33, E_35, E_34, E_39, E_36;
           heavy: E_38, E_40.
15. LATER - Wave 6, numbers acting together: E_23 pairs, E_25 association network, E_20, E_21, E_22;
           heavy: E_24 triplets.
16. LATER - Wave 7, the order the balls come out: E_32, E_29, E_30; heavy: E_31.
17. LATER - Wave 8, information and chaos-style methods: E_41, E_42; heavy: E_43, E_44, E_46, E_47.
18. LATER - Wave 9, machine learning (needs a new library, an owner-approved dependency change, and
           the NIST seed): E_49, E_50, E_51, E_52, E_53.
19. LATER - Wave 10, your pilot-wave-inspired family, one at a time: E_57, E_60, E_58, E_59, E_61, E_62.
20. LATER - Wave 11, outside data: E_54, E_48.
21. LAST  - Combinations of methods: E_55, E_56.
21b. LATER - After WF-1C, two efficiency items from the stock-take (ratified 2 November 2026, not
           before Mode H): a report that ranks across batches by reusing the frozen run records, so
           adding a method no longer needs every other method re-run; and the index for a retired
           revision's records. Added 4 November 2026 (your E1-E3, reminder R-018): the same design
           gives you one consolidated report with development, Mode H, CATCH-UP and PROSPECTIVE kept
           separate (no pooled score), checks how the WF-1B report recomputes its figures, and plans a
           later method's back-history over the post-holdout draws; forecasts by a later method for the
           ten holdout draws need their own reviewed design and count only as development evidence.
22. FINAL - Deferred performance study, only after everything else here and under "Later" (all the
           implementation, holdout work and clean-up), and only when you activate it (reminder R-006):
           measure first, then decide whether anything is worth speeding up. Your proposal:
           doc/Deferred_Performance_Engineering_Proposal_v0_1.md (v0.1, committed at 1050338).

The order within a wave may shift once its design starts. The NIST seed (reminder R-004) was settled
on 31 October 2026 for the scorer's fair-draw simulator (N1); a later method that uses random numbers
gets its own seed policy the same way.

## Later (each its own package and decision)

- Each new wave's methods are released and join the walk-forward batches, then the weekly session,
  as they are installed (the releases of E_6 to wave 2 were done at step 10).
