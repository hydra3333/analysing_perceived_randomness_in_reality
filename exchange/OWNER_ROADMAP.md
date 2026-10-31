# Where the project is up to (the owner's roadmap)

Kept by the Claude web chat; updated at each milestone. Plain English. This is a working list, not
reviewed and not part of the rules: the ratification register is the record. US-ASCII, CRLF.
Last updated: 1 November 2026, after WF-1B v3 passed review (EX_113) and you accepted it; item 10
condensed, and the next steps set out as items 10b to 10d.

## A few words used below

- **E_n:** the project's permanent name for method number n. The catalogue (R1 and R2) lists 62 of
  them, E_1 to E_62, each with a one-line idea. A method becomes real only when its exact rule is
  written, reviewed and coded; until then its catalogue entry is a placeholder.
- **Installed (not yet runnable):** the method's code and tests are in the repository and pass, but
  its registry entry says "not released" and its folder holds an IN_DEVELOPMENT flag, so every request
  to run it is refused before any data is read. A later small "release" package switches it on.
- **Released:** allowed to run, but still only on invented test data until WF-1 (below) is approved.

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
10. NOW  - Releases and WF-1: switch the methods on, run them on past draws (walk-forward: each past
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
           Left in this item, in order:
           a. Claude Code rehearses the v3 install (TASK_T014); you push its report; Claude checks it.
           b. You install WF1B_Install_v3 (Claude leads you step by step); Claude checks it.
           c. You run the two reports (Run_Method_Rankings.bat, one per game: Powerball draws
              1286-1576, Oz Lotto 1474-1693) and commit them; Claude and ChatGPT read them.
10b. NEXT - The snapshot (your request, 1 November 2026): one document package, reviewed by ChatGPT and
           ratified by you:
           - register v0.23 (EX_099 to EX_111, WORKERS-1, WB-0 to WB-2, the seed, the installs);
           - new editions of the two handovers (H-1 for Claude, H-2 for ChatGPT) with their blurbs;
           - Architecture v0.9 (the scorer and report, the walk-forward driver, where records live);
           - the Claude Code rulebook: the report tool joins rule 7's "never run" list, with the
             matching deny entry in .claude\settings.json (that file is yours to edit);
           - a short README.md for the repository;
           - settle the holdout exposure record (HOLDOUT_EXPOSURE_RECORD v0.2, still a candidate). You
             decided on 1 November 2026: record the exposure (a reviewer chat displayed Powerball
             1585-1588); Mode H scores all 10 holdout draws per game, with Powerball 1585 and 1586
             flagged; until then all 10 are treated as unseen, with every rule in force;
           - a Git line-ending rule so files under results/ are never converted on your PC.
10c. NEXT - Mode H, the results update and the prospective mode (your goal: forecasts for the draws of
           the week of 9 November 2026). Designed together, alongside the snapshot:
           - Mode H: each method tested once on the 10 sealed holdout draws per game (Powerball
             1577-1586, Oz Lotto 1694-1703);
           - the results update: the draws after the holdout added to the results, by the update
             process already designed;
           - the prospective mode: each method's forecast for the next draw, frozen and published
             before the draw;
           then you decide whether to declare the system developed.
10d. NEXT - WF-1C, the workers change (your decision WORKERS-1, 31 October 2026), in its own design
           round carrying EX_101's and EX_105's obligations: the coordinator's limit becomes 1 up to the
           machine's logical processor count (24 on your PC), default half (12); the walk-forward
           driver gets --workers (variants in parallel, same records at any worker count, clean stop);
           a progress line; a compare command; the identity tests run once. Until then the six-worker
           limit stands.
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
22. FINAL - Deferred performance study, only after everything else here and under "Later" (all the
           implementation, holdout work and clean-up), and only when you activate it (reminder R-006):
           measure first, then decide whether anything is worth speeding up. Your proposal:
           doc/Deferred_Performance_Engineering_Proposal_v0_1.md (v0.1, committed at 1050338).

The order within a wave may shift once its design starts. The NIST seed (reminder R-004) is settled
at the first method that uses random numbers; that is probably E_17 (Method A) in wave 2, if its
design keeps the simulated fair-draw comparison.

## Later (each its own package and decision)

- Releases of E_6, E_3, E_4, wave 1 and wave 2 (E_6's remember-everything version first), with step 10.
- Holdout testing (the sealed draws), and then real next-draw predictions from all methods together.
