# Where the project is up to (the owner's roadmap)

Kept by the Claude web chat; updated at each milestone. Plain English. This is a working list, not
reviewed and not part of the rules: the ratification register is the record. US-ASCII, CRLF.
Last updated: 31 October 2026, after the code review passed (EX_085), you ratified register v0.21,
and you scheduled the deferred performance stage (item 22).

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

## Next, in the owner's order (decided 30 October 2026; replaces the earlier order of the same day)

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
10. NOW  - Releases and WF-1: switch these methods on, then run them on past draws (walk-forward:
           each past draw predicted only from the draws before it) with the scorer, so the project
           produces its first real measured results. The design passed review (EX_077 to EX_081)
           and you ratified it on 31 October 2026 (design v0.1r1, 03f95fbe). REL-1 and WF-1A passed
           code review (EX_082 to EX_085); you ratified register v0.21 and accepted both packages on
           31 October 2026. REL-1 is INSTALLED (6a1bed9) and WF-1A is INSTALLED (0d98706), both on
           31 October 2026, after their rehearsals T009 and T010; Claude verified both from GitHub.
           E_1 revision 2 (with CODE-3) is INSTALLED too (86d12ea, 31 October 2026; T011 PASS; verified
           from GitHub). All 40 variants can now run on past draws. Next: your first 40-variant Powerball
           batch (Claude leads you through it), then Oz Lotto when you say; then SEED-1 (6 November) and
           WF-1B, the scorer and report (it also adds a progress line to the batch driver).
           E_1 sits out the first batches: its frozen revision 1 accepts only invented data through the
           contract. You chose (WF1-13) a proper E_1 revision 2 that can run on past draws, with E_1's old
           runner moved to revision 2 too. It needs CODE-3 (the tool that archives an old revision) first.
           Its design passed review (EX_086 to EX_091) and you ratified it on 31 October 2026
           (v0.1r2); its coding has started and it installs after WF-1A. After it installs, a new batch over all 40 variants
           (you chose full-cohort batches, not ER-6's E_1-only plan) gives the first report.
           Four steps: REL-1 (switch the methods on), WF-1A (the walk-forward driver; you run it on
           real past draws, about 1-2 hours per game), SEED-1 (the NIST seed, announced for
           6 November), WF-1B (the scorer and report, with the fair-draw simulator).
11. NEXT - Wave 3, look-alike past draws:
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
